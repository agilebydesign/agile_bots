"""Cursor Agent CLI client for executing AI instructions in headless mode.

Uses `cursor-agent` CLI tool with --print flag for non-interactive execution.
On Windows, runs via WSL (Ubuntu) since cursor-agent is Linux-only.
"""

import subprocess
import json
import sys
import os
import uuid
import time
import tempfile
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List
from .non_recoverable_error import NonRecoverableError
from .recoverable_error import RecoverableError


@dataclass
class APIResponse:
    status: str
    message: str
    session_id: Optional[str] = None
    progress: Optional[str] = None
    done: bool = False
    blocked: bool = False
    block_reason: Optional[str] = None
    raw_output: Optional[str] = None


class CursorHeadlessAPI:
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, timeout: int = 600, workspace_path: Optional[Path] = None, stream: bool = True):
        self.api_key = api_key
        self.model = model  # e.g., 'gpt-5', 'sonnet-4', 'sonnet-4-thinking'
        self.timeout = timeout  # Default 600 seconds (10 minutes), can be overridden for tests
        self.workspace_path = workspace_path  # Workspace directory for cursor-agent
        self.stream = stream  # Enable streaming output
        self._session_id: Optional[str] = None
        self._chat_id: Optional[str] = None  # cursor-agent chatId for session resumption
        self._last_output: Optional[str] = None
        self._is_windows = sys.platform == 'win32'
    
    @property
    def session_id(self) -> Optional[str]:
        return self._session_id
    
    @property
    def chat_id(self) -> Optional[str]:
        return self._chat_id
    
    def starts_session(self, instructions: str) -> APIResponse:
        self._session_id = str(uuid.uuid4())[:8]
        
        try:
            result = self._run_cursor_agent(instructions)
            
            if result.returncode != 0:
                error_msg = result.stderr.strip() if result.stderr else result.stdout.strip() or 'Unknown error'
                
                # Check for common errors
                if 'not found' in error_msg.lower() or 'not recognized' in error_msg.lower():
                    raise NonRecoverableError(
                        'cursor-agent not found. On Windows, install via WSL: '
                        'wsl -d Ubuntu -e bash -c "curl https://cursor.com/install -fsS | bash"'
                    )
                if 'unauthorized' in error_msg.lower() or 'authentication' in error_msg.lower():
                    raise NonRecoverableError(f'Authentication failed: {error_msg}')
                if 'rate limit' in error_msg.lower():
                    raise RecoverableError(f'Rate limited: {error_msg}')
                    
                raise RecoverableError(f'cursor-agent failed (exit {result.returncode}): {error_msg}')
            
            self._last_output = result.stdout
            response = self._parse_cursor_output(result.stdout)
            
            # Extract chatId from response for session resumption
            # cursor-agent should return chatId in the response
            if response.session_id:
                self._chat_id = response.session_id
            
            return response
            
        except FileNotFoundError as e:
            raise NonRecoverableError(
                f'cursor-agent command not found: {e}. '
                'On Windows, install via WSL: wsl -d Ubuntu -e bash -c "curl https://cursor.com/install -fsS | bash"'
            )
        except subprocess.TimeoutExpired:
            raise RecoverableError('cursor-agent timed out')
    
    def resumes_session(self, prompt: str) -> APIResponse:
        if not self._chat_id:
            raise ValueError("No active session to resume. Call starts_session() first.")
        
        try:
            result = self._run_cursor_agent(prompt, resume_chat_id=self._chat_id)
            
            if result.returncode != 0:
                error_msg = result.stderr.strip() if result.stderr else result.stdout.strip() or 'Unknown error'
                raise RecoverableError(f'cursor-agent failed (exit {result.returncode}): {error_msg}')
            
            self._last_output = result.stdout
            return self._parse_cursor_output(result.stdout)
            
        except subprocess.TimeoutExpired:
            raise RecoverableError('cursor-agent timed out')
    
    def _run_with_streaming(self, cmd: List[str]) -> subprocess.CompletedProcess:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',  # Replace invalid characters instead of crashing
            bufsize=1  # Line buffered
        )
        
        stdout_lines = []
        stderr_lines = []
        start_time = time.time()
        
        try:
            # Read stdout in real-time
            while True:
                # Check timeout
                if time.time() - start_time > self.timeout:
                    process.kill()
                    raise subprocess.TimeoutExpired(cmd, self.timeout)
                
                # Read line from stdout
                line = process.stdout.readline()
                if line:
                    stdout_lines.append(line)
                    # Parse and print cleaned output
                    self._print_cleaned_stream_line(line)
                
                # Check if process finished
                if process.poll() is not None:
                    # Read any remaining output
                    remaining = process.stdout.read()
                    if remaining:
                        stdout_lines.append(remaining)
                        for remaining_line in remaining.splitlines():
                            self._print_cleaned_stream_line(remaining_line)
                    break
                
                # Small sleep to avoid busy-waiting
                if not line:
                    time.sleep(0.01)
            
            stderr_output = process.stderr.read()
            if stderr_output:
                stderr_lines.append(stderr_output)
            
            return subprocess.CompletedProcess(
                args=cmd,
                returncode=process.returncode,
                stdout=''.join(stdout_lines),
                stderr=''.join(stderr_lines)
            )
            
        except Exception as e:
            process.kill()
            raise e
    
    def _print_cleaned_stream_line(self, line: str) -> None:
        line = line.strip()
        if not line:
            return
        
        try:
            data = json.loads(line)
            msg_type = data.get('type', '')
            
            # Skip system init and thinking deltas
            if msg_type in ('system', 'user'):
                return
            if msg_type == 'thinking':
                # Only show thinking completion
                if data.get('subtype') == 'completed':
                    print('[Thinking complete]')
                    sys.stdout.flush()
                return
            
            # Show assistant messages (the actual AI response)
            if msg_type == 'assistant':
                message = data.get('message', {})
                content = message.get('content', [])
                for item in content:
                    if item.get('type') == 'text':
                        text = item.get('text', '').strip()
                        if text:
                            print(text)
                            sys.stdout.flush()
                return
            
            # Show tool calls in a clean format
            if msg_type == 'tool_call':
                subtype = data.get('subtype', '')
                tool_call = data.get('tool_call', {})
                
                if subtype == 'started':
                    # Extract tool name
                    for tool_name, tool_data in tool_call.items():
                        if tool_name.endswith('ToolCall'):
                            tool_display = tool_name.replace('ToolCall', '')
                            args = tool_data.get('args', {})
                            
                            # Format based on tool type
                            if tool_display == 'read':
                                path = args.get('path', '')
                                print(f'[Reading: {path}]')
                            elif tool_display == 'write':
                                path = args.get('path', '')
                                print(f'[Writing: {path}]')
                            elif tool_display == 'grep':
                                pattern = args.get('pattern', '')
                                print(f'[Searching: {pattern}]')
                            elif tool_display == 'semSearch':
                                query = args.get('query', '')
                                print(f'[Semantic search: {query}]')
                            else:
                                print(f'[Tool: {tool_display}]')
                            sys.stdout.flush()
                return
            
            # Show result/error messages
            if msg_type == 'result':
                result_text = data.get('result', '')
                if result_text:
                    print(f'\n{result_text}\n')
                    sys.stdout.flush()
                return
                
        except json.JSONDecodeError:
            # Not JSON, might be plain text - print as is
            if line and not line.startswith('{'):
                print(line)
                sys.stdout.flush()
    
    def _run_cursor_agent(self, prompt: str, resume_chat_id: Optional[str] = None) -> subprocess.CompletedProcess:
        if self._is_windows:
            return self._run_via_wsl(prompt, resume_chat_id)
        else:
            return self._run_directly(prompt, resume_chat_id)
    
    def _run_via_wsl(self, prompt: str, resume_chat_id: Optional[str] = None) -> subprocess.CompletedProcess:
        temp_prompt_file = None
        temp_script_file = None
        
        try:
            if len(prompt) > 4000:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                    f.write(prompt)
                    temp_prompt_file = f.name
                
                temp_prompt_wsl = temp_prompt_file.replace('\\', '/').replace('C:', '/mnt/c').replace('c:', '/mnt/c')
                prompt_source = f'PROMPT="$(cat {temp_prompt_wsl})"'
            else:
                escaped = prompt.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')
                prompt_source = f'PROMPT="{escaped}"'
            
            if self.stream:
                cursor_cmd = '~/.local/bin/cursor-agent --print --output-format stream-json --stream-partial-output --force'
            else:
                cursor_cmd = '~/.local/bin/cursor-agent --print --output-format json --force'
            
            if self.api_key:
                cursor_cmd += f' --api-key "{self.api_key}"'
            
            if self.model:
                cursor_cmd += f' --model {self.model}'
            
            if resume_chat_id:
                cursor_cmd += f' --resume {resume_chat_id}'
            
            if self.workspace_path:
                path_str = str(self.workspace_path).replace('\\', '/')
                if path_str[1:3] == ':/':
                    drive_letter = path_str[0].lower()
                    wsl_path = f'/mnt/{drive_letter}{path_str[2:]}'
                else:
                    wsl_path = path_str
                cursor_cmd += f' --workspace "{wsl_path}"'
            
            script_content = f'''#!/bin/bash
{prompt_source}
{cursor_cmd} "$PROMPT"
'''
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False, encoding='utf-8') as f:
                f.write(script_content)
                temp_script_file = f.name
            
            temp_script_wsl = temp_script_file.replace('\\', '/').replace('C:', '/mnt/c').replace('c:', '/mnt/c')
            
            cmd = ['wsl', '-d', 'Ubuntu', '--', 'bash', temp_script_wsl]
            
            if self.stream:
                result = self._run_with_streaming(cmd)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)
            
            return result
            
        finally:
            if temp_prompt_file:
                try:
                    os.unlink(temp_prompt_file)
                except Exception as e:
                    logging.warning(f"Failed to delete temporary prompt file {temp_prompt_file}: {e}")
            if temp_script_file:
                try:
                    os.unlink(temp_script_file)
                except Exception as e:
                    logging.warning(f"Failed to delete temporary script file {temp_script_file}: {e}")
    
    def _run_directly(self, prompt: str, resume_chat_id: Optional[str] = None) -> subprocess.CompletedProcess:
        if self.stream:
            cmd = ['cursor-agent', '--print', '--output-format', 'stream-json', '--stream-partial-output', '--force']
        else:
            cmd = ['cursor-agent', '--print', '--output-format', 'json', '--force']
        
        if self.api_key:
            cmd.extend(['--api-key', self.api_key])
        
        if self.model:
            cmd.extend(['--model', self.model])
        
        # Add resume flag if continuing a session
        if resume_chat_id:
            cmd.extend(['--resume', resume_chat_id])
        
        # Add workspace path if provided
        if self.workspace_path:
            # Use forward slashes to avoid backslash issues
            workspace_str = str(self.workspace_path).replace('\\', '/')
            cmd.extend(['--workspace', workspace_str])
        
        cmd.append(prompt)
        
        if self.stream:
            # Stream output in real-time
            return self._run_with_streaming(cmd)
        else:
            return subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
    
    def sends_instruction(self, instruction: str) -> APIResponse:
        if not self._session_id:
            raise NonRecoverableError('No active session - call starts_session first')
        
        try:
            result = self._run_cursor_agent(instruction)
            
            if result.returncode != 0:
                error_msg = result.stderr.strip() if result.stderr else result.stdout.strip() or 'Unknown error'
                raise RecoverableError(f'cursor-agent failed: {error_msg}')
            
            self._last_output = result.stdout
            return self._parse_cursor_output(result.stdout)
            
        except subprocess.TimeoutExpired:
            raise RecoverableError('cursor-agent timed out')
    
    def polls_session_status(self) -> APIResponse:
        if not self._session_id:
            raise NonRecoverableError('No active session')
        
        # cursor-agent runs synchronously. By the time starts_session or resumes_session
        # returns, the process has completed. We instructed it to work autonomously,
        # so when the process exits, it's done.
        return APIResponse(
            status='completed',
            message='Session completed',
            session_id=self._session_id,
            done=True
        )
    
    def terminates_session(self) -> None:
        self._session_id = None
        self._last_output = None
    
    def _parse_cursor_output(self, output: str) -> APIResponse:
        if not output or not output.strip():
            return APIResponse(
                status='completed',
                message='No output',
                session_id=self._session_id,
                done=True,
                raw_output=output
            )
        
        # cursor-agent with stream-json outputs multiple JSON objects (one per line)
        # We don't need to parse them - the output was already printed in real-time
        # Just return done=True since the process has completed
        return APIResponse(
            status='completed',
            message='Completed',
            session_id=self._session_id,
            done=True,
            raw_output=output
        )
