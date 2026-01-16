"""
Supervised Session - A simple but intelligent supervision loop.

Flow:
1. BOT 1 (Executor) -> Does work, produces output
2. BOT 2 (Reviewer) -> Examines output thoroughly
   - On track -> Continue to next step
   - Off track -> UNDO changes, redirect to original prompt
   - Exception -> Fix code OR chunk if AI-related (context too big)
3. Loop until done, with chunking support for large plans
4. Continue mode support for multi-step execution
"""
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

from .headless_session import HeadlessSession
from .task_supervisor import TaskSupervisor, ReviewResult, SupervisionResult
from .context_injector import ContextInjector
from .execution_result import ExecutionResult
from .non_recoverable_error import NonRecoverableError


MAX_OFF_TRACK_RETRIES = 3
MAX_UNDO_OPERATIONS = 5


@dataclass
class SupervisedResult:
    """Result of supervised execution."""
    status: str  # 'completed', 'blocked', 'failed', 'off_track_limit'
    message: str
    iterations_completed: int
    total_iterations: int
    undo_count: int
    off_track_count: int
    files_changed: List[str] = field(default_factory=list)
    execution_log: List[str] = field(default_factory=list)


class SupervisedSession:
    """
    A session that supervises executor bot output and ensures task compliance.
    
    Key features:
    - Reviews all executor output against original task
    - Detects off-track work and redirects
    - Can undo changes when needed
    - Chunks large plans into iterations
    - Builds rich context from file/rule/story references
    """
    
    def __init__(
        self,
        workspace_path: Path,
        timeout: int = 600
    ):
        self.workspace_path = workspace_path
        self.timeout = timeout
        self._headless: Optional[HeadlessSession] = None
        self._supervisor: Optional[TaskSupervisor] = None
        self._injector: Optional[ContextInjector] = None
        self._execution_log: List[str] = []
        self._off_track_count: int = 0
        self._undo_count: int = 0
    
    def _log(self, message: str) -> None:
        """Add entry to execution log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self._execution_log.append(entry)
        print(entry)  # Also print for visibility
    
    def _save_git_state(self) -> Optional[str]:
        """Save current git state for potential undo."""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.workspace_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return None
    
    def _undo_changes(self) -> bool:
        """Undo all uncommitted changes."""
        try:
            # Checkout all tracked files
            subprocess.run(
                ['git', 'checkout', '--', '.'],
                cwd=self.workspace_path,
                capture_output=True,
                timeout=30
            )
            # Clean untracked files (but not ignored ones)
            subprocess.run(
                ['git', 'clean', '-fd'],
                cwd=self.workspace_path,
                capture_output=True,
                timeout=30
            )
            self._undo_count += 1
            self._log(f"UNDO #{self._undo_count}: Changes reverted")
            return True
        except Exception as e:
            self._log(f"UNDO FAILED: {e}")
            return False
    
    def _get_files_changed(self) -> List[str]:
        """Get list of changed files."""
        try:
            result = subprocess.run(
                ['git', 'status', '--short'],
                cwd=self.workspace_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        except Exception:
            pass
        return []
    
    def execute_with_supervision(
        self,
        prompt: str,
        plan_file: Optional[Path] = None
    ) -> SupervisedResult:
        """
        Execute a task with full supervision.
        
        Args:
            prompt: The original task/prompt
            plan_file: Optional path to a plan file (will be chunked if large)
        
        Returns:
            SupervisedResult with execution details
        """
        self._log("Starting supervised execution")
        
        # Initialize components
        self._headless = HeadlessSession(self.workspace_path, timeout=self.timeout)
        self._supervisor = TaskSupervisor(
            self.workspace_path,
            prompt,
            plan_file
        )
        self._injector = ContextInjector(self.workspace_path)
        
        # Save git state for undo capability
        self._supervisor.save_git_state()
        
        # Check if we need to chunk
        total_iterations = self._supervisor.total_chunks if self._supervisor.total_chunks > 0 else 1
        current_iteration = 0
        
        self._log(f"Plan has {total_iterations} iteration(s)")
        
        while current_iteration < total_iterations:
            current_iteration += 1
            self._log(f"--- ITERATION {current_iteration}/{total_iterations} ---")
            
            # Build the prompt for this iteration
            if self._supervisor.total_chunks > 0:
                chunk = self._supervisor.get_current_chunk()
                if chunk:
                    iteration_prompt = self._supervisor.build_chunk_prompt(chunk)
                else:
                    iteration_prompt = prompt
            else:
                # No chunking, use full prompt with constraints
                iteration_prompt = self._injector.build_constrained_prompt(
                    prompt,
                    iteration_number=current_iteration,
                    total_iterations=total_iterations
                )
            
            # Execute with the executor bot
            self._log("Executor: Starting work...")
            try:
                result = self._headless.invokes(iteration_prompt)
            except Exception as e:
                self._log(f"Executor EXCEPTION: {e}")
                # Try to fix or chunk
                if "context" in str(e).lower() or "token" in str(e).lower():
                    self._log("AI limit detected - need chunking")
                    # TODO: Implement dynamic re-chunking
                    return SupervisedResult(
                        status='failed',
                        message=f"AI context limit: {e}",
                        iterations_completed=current_iteration - 1,
                        total_iterations=total_iterations,
                        undo_count=self._undo_count,
                        off_track_count=self._off_track_count,
                        execution_log=self._execution_log
                    )
                else:
                    return SupervisedResult(
                        status='failed',
                        message=f"Executor error: {e}",
                        iterations_completed=current_iteration - 1,
                        total_iterations=total_iterations,
                        undo_count=self._undo_count,
                        off_track_count=self._off_track_count,
                        execution_log=self._execution_log
                    )
            
            # Now review the output with the reviewer bot
            self._log("Reviewer: Examining output...")
            files_changed = self._get_files_changed()
            
            review_prompt = self._supervisor.build_review_prompt(
                result.message if hasattr(result, 'message') else str(result),
                files_changed
            )
            
            try:
                review_result = self._headless.invokes(review_prompt)
                supervision = self._supervisor.parse_review_response(
                    review_result.message if hasattr(review_result, 'message') else str(review_result)
                )
            except Exception as e:
                self._log(f"Reviewer EXCEPTION: {e}")
                # Assume on track if reviewer fails
                supervision = SupervisionResult(
                    result=ReviewResult.ON_TRACK,
                    message="Reviewer failed, assuming on track",
                    should_continue=True,
                    files_changed=files_changed
                )
            
            self._log(f"Review result: {supervision.result.value}")
            
            # Handle review result
            if supervision.result == ReviewResult.COMPLETE:
                self._log("Iteration COMPLETE")
                if self._supervisor.total_chunks > 0:
                    self._supervisor.advance_to_next_chunk()
                continue
            
            elif supervision.result == ReviewResult.ON_TRACK:
                self._log("On track, continuing")
                if self._supervisor.total_chunks > 0:
                    self._supervisor.advance_to_next_chunk()
                continue
            
            elif supervision.result == ReviewResult.OFF_TRACK:
                self._off_track_count += 1
                self._log(f"OFF TRACK (count: {self._off_track_count}): {supervision.message}")
                
                if self._off_track_count >= MAX_OFF_TRACK_RETRIES:
                    self._log("Max off-track retries exceeded")
                    return SupervisedResult(
                        status='off_track_limit',
                        message=f"Executor went off-track {self._off_track_count} times",
                        iterations_completed=current_iteration - 1,
                        total_iterations=total_iterations,
                        undo_count=self._undo_count,
                        off_track_count=self._off_track_count,
                        files_changed=files_changed,
                        execution_log=self._execution_log
                    )
                
                # UNDO and retry
                if supervision.should_undo or self._undo_count < MAX_UNDO_OPERATIONS:
                    self._undo_changes()
                    current_iteration -= 1  # Retry this iteration
                    self._log("Will retry with stronger prompt")
                    continue
            
            elif supervision.result == ReviewResult.EXCEPTION:
                self._log(f"Exception detected: {supervision.exception_info}")
                # Could try to fix, for now just fail
                return SupervisedResult(
                    status='failed',
                    message=f"Exception: {supervision.exception_info}",
                    iterations_completed=current_iteration - 1,
                    total_iterations=total_iterations,
                    undo_count=self._undo_count,
                    off_track_count=self._off_track_count,
                    files_changed=files_changed,
                    execution_log=self._execution_log
                )
            
            elif supervision.result == ReviewResult.NEEDS_CHUNKING:
                self._log("Context too large, needs chunking")
                # TODO: Implement dynamic re-chunking
                return SupervisedResult(
                    status='failed',
                    message="Context too large, needs smaller chunks",
                    iterations_completed=current_iteration - 1,
                    total_iterations=total_iterations,
                    undo_count=self._undo_count,
                    off_track_count=self._off_track_count,
                    files_changed=files_changed,
                    execution_log=self._execution_log
                )
        
        # All iterations complete
        self._log("=== ALL ITERATIONS COMPLETE ===")
        return SupervisedResult(
            status='completed',
            message="Task completed successfully",
            iterations_completed=total_iterations,
            total_iterations=total_iterations,
            undo_count=self._undo_count,
            off_track_count=self._off_track_count,
            files_changed=self._get_files_changed(),
            execution_log=self._execution_log
        )
    
    def continue_session(self, prompt: str) -> SupervisedResult:
        """
        Continue an existing session with a new prompt.
        
        Use this when processing in chunks with "ask for more" pattern.
        """
        if not self._headless:
            raise NonRecoverableError("No active session. Call execute_with_supervision first.")
        
        self._log(f"Continuing session: {prompt[:50]}...")
        
        # Build constrained continuation prompt
        constrained = self._injector.build_constrained_prompt(prompt) if self._injector else prompt
        
        try:
            result = self._headless.continues_session(constrained)
            return SupervisedResult(
                status='completed' if result.status == 'completed' else 'blocked',
                message=result.message if hasattr(result, 'message') else str(result),
                iterations_completed=1,
                total_iterations=1,
                undo_count=self._undo_count,
                off_track_count=self._off_track_count,
                files_changed=self._get_files_changed(),
                execution_log=self._execution_log
            )
        except Exception as e:
            return SupervisedResult(
                status='failed',
                message=str(e),
                iterations_completed=0,
                total_iterations=1,
                undo_count=self._undo_count,
                off_track_count=self._off_track_count,
                execution_log=self._execution_log
            )
