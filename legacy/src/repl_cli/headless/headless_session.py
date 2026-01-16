import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List
from .headless_config import HeadlessConfig
from .execution_context import ExecutionContext
from .execution_result import ExecutionResult
from .session_log import SessionLog
from .recoverable_error import RecoverableError
from .non_recoverable_error import NonRecoverableError
from .error_recovery import ErrorRecovery
from .cursor_api import CursorHeadlessAPI, APIResponse
from ...bot.workspace import get_base_actions_directory
from ...utils import read_json_file


MAX_LOOPS = 50


def get_action_auto_confirm(action_name: str) -> bool:
    """Get auto_confirm setting for an action from its config file.
    
    Args:
        action_name: The action name (e.g., 'build', 'validate', 'clarify')
    
    Returns:
        True if action should auto-confirm, False otherwise (default)
    """
    # Normalize action names to their base directory names
    normalization_map = {
        'gather_context': 'clarify',
        'clarify_context': 'clarify', 
        'decide_strategy': 'strategy',
        'build_knowledge': 'build',
        'validate_rules': 'validate',
        'render_output': 'render'
    }
    normalized = normalization_map.get(action_name, action_name)
    
    config_path = get_base_actions_directory() / normalized / 'action_config.json'
    if not config_path.exists():
        return False
    
    try:
        config = read_json_file(config_path)
        return config.get('auto_confirm', False)
    except Exception:
        return False


class HeadlessSession:
    
    def __init__(self, workspace_directory: Path, config: Optional[HeadlessConfig] = None, timeout: int = 600):
        self.workspace_directory = workspace_directory
        self.config = config or HeadlessConfig.load()
        self.timeout = timeout  # API timeout in seconds (default 10 minutes, can be reduced for tests)
        self.session_id = None
        self.log = None
        self._api: Optional[CursorHeadlessAPI] = None
        self._error_recovery = ErrorRecovery()
    
    def invokes(
        self,
        message: str,
        context_file: Optional[Path] = None
    ) -> ExecutionResult:
        if not self.config.is_configured:
            raise NonRecoverableError('Headless mode not configured - API key required')
        
        context = self._loads_context(context_file)
        context_loaded = context_file is not None and context_file.exists()
        
        instructions = self._prepares_instructions(message, context)
        
        log_dir = self.workspace_directory / 'logs'
        self.log = SessionLog.creates_with_timestamped_path(log_dir)
        
        self.session_id = f'session_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        
        return self._executes_with_recovery(instructions, context_loaded)
    
    def continues_session(self, prompt: str) -> ExecutionResult:
        if not self._api:
            raise ValueError("No active session. Call invokes() first to start a session.")
        
        self.log.appends_response(f'Continuing session with new prompt')
        
        # cursor-agent is synchronous - when resumes_session returns, it's done
        # Output is streamed in real-time during execution
        response = self._api.resumes_session(prompt)
        
        # Log completion
        if response.done:
            self.log.appends_response(f'Completed: {response.message}')
            return ExecutionResult.creates_completed(
                log_path=self.log.log_path,
                session_id=self.session_id,
                context_loaded=False,  # Context already loaded in initial invokes()
                instructions=prompt,
                loop_count=1,
                loop_responses=[response.message]
            )
        
        if response.blocked:
            return self._create_blocked_result(response, prompt, context_loaded=False)
        
        # Shouldn't reach here since cursor-agent is synchronous
        raise NonRecoverableError('Unexpected: cursor-agent returned without done or blocked status')
    
    def invokes_operation(
        self,
        behavior: str,
        action: str,
        operation: str,
        context_file: Optional[Path] = None
    ) -> ExecutionResult:
        command = f'{behavior}.{action}.{operation}'
        message = f'Execute operation: {command}'
        
        result = self.invokes(message, context_file)
        result.operation = operation
        result.behavior = behavior
        result.action = action
        result.operations_executed = [operation]
        # Ensure context_loaded matches context_file state (invokes already sets it, but be explicit)
        result.context_loaded = context_file is not None and context_file.exists()
        result.context_included = context_file is not None and context_file.exists()
        
        if operation == 'confirm' and result.status == 'completed':
            result.action_completed = True
            result.operations_status['confirm'] = 'completed'
        
        return result
    
    def invokes_action(
        self,
        behavior: str,
        action: str,
        context_file: Optional[Path] = None
    ) -> ExecutionResult:
        operations = ['instructions', 'confirm']
        # Ensure context_loaded is set correctly (invokes sets it, but preserve it explicitly)
        context_loaded = context_file is not None and context_file.exists()
        
        # Initialize operations_executed list to accumulate operations across the loop
        operations_executed = []
        
        for operation in operations:
            message = f'Execute operation: {behavior}.{action}.{operation}'
            result = self.invokes(message, context_file)
            result.behavior = behavior
            result.action = action
            operations_executed.append(operation)
            result.operations_executed = operations_executed.copy()  # Set accumulated list
            result.operations_status[operation] = 'completed' if result.status == 'completed' else 'blocked'
            # Ensure context_loaded is preserved
            result.context_loaded = context_loaded
            
            if result.status == 'blocked':
                result.set_blocked_at_operation(operation, result.operations_executed)
                return result
            
            result.current_operation = operation
        
        result.action_completed = True
        return result
    
    def invokes_behavior(
        self,
        behavior: str,
        context_file: Optional[Path] = None
    ) -> ExecutionResult:
        actions = ['clarify', 'strategy', 'build', 'render', 'validate']
        # Ensure context_loaded is set correctly (invokes_action sets it, but preserve it explicitly)
        context_loaded = context_file is not None and context_file.exists()
        
        # Initialize actions_executed list to accumulate actions across the loop
        actions_executed = []
        
        final_result = None
        for action in actions:
            result = self.invokes_action(behavior, action, context_file)
            result.behavior = behavior
            actions_executed.append(action)
            result.actions_executed = actions_executed.copy()  # Set accumulated list
            result.actions_status[action] = 'completed' if result.action_completed else 'blocked'
            # Ensure context_loaded is preserved
            result.context_loaded = context_loaded
            
            if result.status == 'blocked':
                result.set_blocked_at_action(action, actions_executed.copy())
                return result
            
            final_result = result
        
        if final_result:
            final_result.behavior_completed = True
        return final_result
    
    def _is_truly_complete(self, original_instructions: str, message: str) -> bool:
        """Check if task is truly complete using a second AI to review the work.
        
        This provides a more thorough check by:
        1. Reviewing the full response (not just last paragraph)
        2. Checking what files were created/modified
        3. Verifying the work matches the original task requirements
        """
        # Get full response (last 3000 chars to keep context manageable but thorough)
        full_response = message.strip()
        response_excerpt = full_response[-3000:] if len(full_response) > 3000 else full_response
        
        # Get list of files created/modified in this session
        files_info = self._get_session_file_changes()
        
        check_prompt = f"""You are a thorough QA reviewer. Analyze if the AI has completed the ORIGINAL TASK correctly.

ORIGINAL TASK:
{original_instructions}

AI'S RESPONSE (last 3000 chars):
{response_excerpt}

FILES CREATED/MODIFIED:
{files_info}

Review the task requirements carefully:
1. Did the AI complete what was asked in the ORIGINAL TASK?
2. If the task said "do not make changes", did the AI follow that instruction?
3. If the task asked for a plan/document, was it created?
4. Is there any indication the AI is still working or needs to continue?
5. Did the AI wander off-task or do something different?

Based on your thorough analysis, answer with ONLY one word:
- "COMPLETE" if the AI has successfully finished the ORIGINAL TASK
- "OFFTASK" if the AI did something different from the original task
- "CONTINUE" if the AI is still working on the task or missed something

Your answer (one word only):"""
        
        try:
            checker_api = CursorHeadlessAPI(
                api_key=self.config.api_key,
                timeout=45,  # Increased timeout for more thorough check
                workspace_path=self.workspace_directory
            )
            
            check_response = checker_api.starts_session(check_prompt)
            answer = check_response.message.strip().upper()
            
            self.log.appends_response(f'Completion check: {answer}')
            
            # Stop if complete OR if AI went off-task
            return "COMPLETE" in answer or "OFFTASK" in answer
        except Exception as e:
            self.log.appends_response(f'Completion check failed: {e}, defaulting to continue')
            return False
    
    def _get_session_file_changes(self) -> str:
        """Get a summary of files created/modified during this session."""
        import subprocess
        try:
            # Get git status to see what changed
            result = subprocess.run(
                ['git', 'status', '--short'],
                cwd=self.workspace_directory,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                # Limit to first 20 files to keep context manageable
                if len(lines) > 20:
                    files_list = '\n'.join(lines[:20]) + f'\n... and {len(lines) - 20} more files'
                else:
                    files_list = '\n'.join(lines)
                return f"Git status:\n{files_list}"
            else:
                return "No files modified (git status clean)"
        except Exception as e:
            # If git fails, try to list recently modified files
            try:
                import os
                import time
                
                # Get files modified in last 5 minutes
                current_time = time.time()
                recent_files = []
                
                for root, dirs, files in os.walk(self.workspace_directory):
                    # Skip .git directory
                    if '.git' in root:
                        continue
                    for file in files:
                        filepath = Path(root) / file
                        try:
                            mtime = filepath.stat().st_mtime
                            if current_time - mtime < 300:  # 5 minutes
                                rel_path = filepath.relative_to(self.workspace_directory)
                                recent_files.append(str(rel_path))
                        except:
                            continue
                
                if recent_files:
                    # Limit to first 20 files
                    if len(recent_files) > 20:
                        files_list = '\n'.join(recent_files[:20]) + f'\n... and {len(recent_files) - 20} more files'
                    else:
                        files_list = '\n'.join(recent_files)
                    return f"Recently modified files:\n{files_list}"
                else:
                    return "No recently modified files detected"
            except Exception as e2:
                return f"Could not determine file changes: {e}"
    
    def _create_blocked_result(
        self,
        response: APIResponse,
        instructions: str,
        context_loaded: bool,
        loop_count: int = 1,
        loop_responses: list = None
    ) -> ExecutionResult:
        self.log.appends_response(f'Blocked: {response.block_reason or "Unknown reason"}')
        result = ExecutionResult.creates_blocked(
            log_path=self.log.log_path,
            session_id=self.session_id,
            context_loaded=context_loaded,
            instructions=instructions,
            loop_count=loop_count,
            loop_responses=loop_responses or [response.message]
        )
        result.block_reason = response.block_reason or 'Waiting for user input'
        return result
    
    def _loads_context(self, context_file: Optional[Path]) -> ExecutionContext:
        if context_file and context_file.exists():
            return ExecutionContext.loads_from_context_file(context_file)
        return ExecutionContext()
    
    def _prepares_instructions(
        self,
        message: str,
        context: ExecutionContext
    ) -> str:
        instructions = 'Keep doing this until 100% done or blocked:\n\n'
        instructions += message + '\n\n'
        
        if context.user_message:
            instructions += f'User Intent: {context.user_message}\n\n'
        
        if context.chat_history:
            instructions += 'Chat History:\n'
            for entry in context.chat_history:
                instructions += f'- {entry}\n'
            instructions += '\n'
        
        if context.file_references:
            instructions += 'File References:\n'
            for ref in context.file_references:
                instructions += f'- {ref}\n'
            instructions += '\n'
        
        wrapped = f'Keep doing this until 100% done or blocked:\n\n{instructions}'
        final = f'{wrapped}\n\nDo NOT ask questions or wait for user input - just complete the work autonomously.\n\nIf blocked, report reason clearly.'
        
        return final
    
    def _executes_with_recovery(self, instructions: str, context_loaded: bool) -> ExecutionResult:
        while self._error_recovery.can_retry():
            try:
                return self._executes_with_api(instructions, context_loaded)
            except RecoverableError as e:
                self._error_recovery.increment_attempt()
                self.log.appends_response(f'Recoverable error: {e}. Attempt {self._error_recovery.current_attempts}')
                
                if self._error_recovery.can_retry():
                    self._error_recovery.wait_before_retry(duration=2.0)
                    if self._api:
                        self._api.terminates_session()
                else:
                    raise NonRecoverableError(f'Max retries exceeded: {e}')
        
        raise NonRecoverableError('Execution failed after all retries')
    
    def _executes_with_api(self, instructions: str, context_loaded: bool) -> ExecutionResult:
        self._api = CursorHeadlessAPI(
            api_key=self.config.api_key, 
            timeout=self.timeout,
            workspace_path=self.workspace_directory
        )
        
        self.log.appends_response(f'Session {self.session_id} started')
        self.log.appends_response(f'Instructions: {instructions}')
        
        response = self._api.starts_session(instructions)
        self.session_id = response.session_id or self.session_id
        
        loop_count = 1
        loop_responses = [response.message]
        
        while loop_count < MAX_LOOPS:
            if response.blocked:
                return self._create_blocked_result(response, instructions, context_loaded, loop_count, loop_responses)
            
            if not response.done:
                raise NonRecoverableError('Unexpected: cursor-agent returned without done or blocked status')
            
            self.log.appends_response(f'Loop {loop_count}: {response.message}')
            
            if self._is_truly_complete(instructions, response.message):
                self.log.appends_response(f'Completed: Work is truly complete')
                return ExecutionResult.creates_completed(
                    log_path=self.log.log_path,
                    session_id=self.session_id,
                    context_loaded=context_loaded,
                    instructions=instructions,
                    loop_count=loop_count,
                    loop_responses=loop_responses
                )
            
            loop_count += 1
            if loop_count >= MAX_LOOPS:
                break
            
            self.log.appends_response(f'Loop {loop_count}: Continuing with original task...')
            continue_prompt = f"Continue working on the original task:\n\n{instructions}"
            response = self._api.resumes_session(continue_prompt)
            loop_responses.append(response.message)
        
        self.log.appends_response(f'Completed after {loop_count} loops')
        return ExecutionResult.creates_completed(
            log_path=self.log.log_path,
            session_id=self.session_id,
            context_loaded=context_loaded,
            instructions=instructions,
            loop_count=loop_count,
            loop_responses=loop_responses
        )
