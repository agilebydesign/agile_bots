import sys
import json
import re
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

from .repl_results import (
    REPLStateDisplay,
    REPLCommandResponse,
    TTYDetectionResult
)
from ..actions.action_context import Scope, ScopeType
from .cli_bot import CLIBot
from .formatters.output_formatter import OutputFormatter


class REPLSession:
    def __init__(self, bot, workspace_directory: Path):
        self.cli_bot = CLIBot(bot, self)
        self.workspace_directory = Path(workspace_directory)
        tty_result = self.detect_tty()
        
        # Formatter for display helpers (icons, separators)
        self.formatter = OutputFormatter()
    
    @property
    def bot(self):
        return self.cli_bot.domain_bot
    
    @property
    def current_behavior(self):
        return self.cli_bot.behaviors.current
    
    @property
    def current_action(self):
        behavior = self.current_behavior
        return behavior.actions.current if behavior else None
    
    @property
    def has_current_behavior(self) -> bool:
        return self.current_behavior is not None
    
    @property
    def has_current_action(self) -> bool:
        return self.current_action is not None
    
    @property
    def current_behavior_name(self) -> Optional[str]:
        behavior = self.current_behavior
        return behavior.name if behavior else None
    
    @property
    def current_action_name(self) -> Optional[str]:
        action = self.current_action
        return action.name if action else None
    
    @property
    def current_action_state(self) -> Optional[str]:
        if not self.has_current_action:
            return None
        return f"{self.bot.bot_name}.{self.current_behavior_name}.{self.current_action_name}"
    
    @property
    def current_behavior_state(self) -> Optional[str]:
        if not self.has_current_behavior:
            return None
        return f"{self.bot.bot_name}.{self.current_behavior_name}"
    
    @property
    def action_phase(self) -> str:
        action = self.current_action
        if action and hasattr(action.domain_action, 'phase'):
            return action.domain_action.phase
        # Fallback: read from state file
        state_file = self.workspace_directory / 'behavior_action_state.json'
        if state_file.exists():
            try:
                state_data = json.loads(state_file.read_text())
                return state_data.get('action_phase', 'not_started')
            except (json.JSONDecodeError, IOError) as e:
                logging.warning(f"Failed to read action phase from state file {state_file}: {e}")
        return 'not_started'
    
    def set_action_phase(self, phase: str) -> None:
        action = self.current_action
        if action and hasattr(action.domain_action, 'phase'):
            action.domain_action.phase = phase
        state_file = self.workspace_directory / 'behavior_action_state.json'
        if state_file.exists():
            try:
                state_data = json.loads(state_file.read_text())
                state_data['action_phase'] = phase
                state_file.write_text(json.dumps(state_data, indent=2))
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not update action phase in state file: {e}", file=sys.stderr)
    
    @property
    def stage_name(self) -> str:
        return self.action_phase
    
    @property
    def progress_path(self) -> str:
        if not self.has_current_action:
            return ""
        return f"{self.current_behavior_name}.{self.current_action_name}"
    
    @property
    def behavior_names(self) -> List[str]:
        return self.bot.behaviors.names if self.bot and self.bot.behaviors else []
    
    @property
    def completed_action_names(self) -> set:
        behavior = self.current_behavior
        if not behavior:
            return set()
        return {name for name in behavior.actions.names if behavior.actions.is_action_completed(name)}
    
    @property
    def completed_behaviors(self) -> List[str]:
        return self.bot.behaviors.completed_behaviors if self.bot else []
    
    def detect_tty(self) -> TTYDetectionResult:
        tty_detected = sys.stdin.isatty()
        return TTYDetectionResult(
            tty_detected=tty_detected,
            interactive_prompts_enabled=tty_detected
        )
    
    def get_progress_line(self) -> str:
        if not self.has_current_action:
            if not self._initialize_to_first_behavior_action():
                return "No active workflow"
            return self.get_progress_line()
        return f"Progress: {self.progress_path}.{self.stage_name}"
    
    def _initialize_to_first_behavior_action(self) -> bool:
        if not self.bot or not self.bot.behaviors or self.bot.behaviors.is_empty():
            return False
        first_behavior = self.bot.behaviors.first
        if not first_behavior or not first_behavior.actions.names:
            return False
        self.bot.behaviors.navigate_to(first_behavior.name)
        first_behavior.actions.navigate_to(first_behavior.actions.names[0])
        return True
    
    def display_current_state(self, full=False, auto_initialize=True, format='text', skip_scope=False) -> REPLStateDisplay:
        if not self.has_current_action:
            if auto_initialize and self._initialize_to_first_behavior_action():
                return self.display_current_state(full=full, auto_initialize=False, format=format)
            # No current action and either auto_initialize=False or initialization failed
            return REPLStateDisplay(
                output="No current position set\n\n  help          - Show detailed help\n  exit          - Exit REPL",
                state_loaded=False
            )
        
        lines = []
        formatter = self.formatter
        
        # Get bot name from bot_directory
        if self.bot and hasattr(self.bot, 'bot_paths'):
            bot_name = self.bot.bot_paths.bot_directory.name
        else:
            bot_name = 'UNKNOWN'
        
        # Bot section header
        lines.append(f"## {formatter.bot_icon()} Bot: {bot_name}")
        
        if self.bot:
            bot_path = self.bot.bot_paths.bot_directory if hasattr(self.bot, 'bot_paths') else 'Unknown'
            lines.append(f"**Bot Path:**")
            lines.append("```")
            lines.append(str(bot_path))
            lines.append("```")
        
        lines.append("")
        
        # Workspace section
        workspace_name = self.workspace_directory.name if hasattr(self.workspace_directory, 'name') else 'base_bot'
        lines.append(f"{formatter.workspace_icon()} **Workspace:** {workspace_name}")
        lines.extend(self._format_code_block(str(self.workspace_directory)))
        lines.append("")
        lines.append("To change path:")
        lines.extend(self._format_code_block("path demo/mob_minion              # Change to specific project\npath ../another_bot               # Change to relative path"))
        
        # Headless Mode section
        lines.append(formatter.subsection_separator())
        from agile_bot.bots.base_bot.src.repl_cli.status_display import HeadlessModeStatusDisplay
        headless_display = HeadlessModeStatusDisplay(workspace_directory=self.workspace_directory)
        lines.append(headless_display.render())
        
        # Scope section (thin line separator) - skip if scope is displayed elsewhere (e.g., in instructions)
        if not skip_scope:
            lines.append(formatter.subsection_separator())
            
            scope_display = self.cli_bot.get_scope_display(format=format)
            if scope_display:
                lines.append(scope_display)
            else:
                # No scope set - show brief message
                lines.append(f"{formatter.scope_icon()} Scope")
                lines.append(f"{formatter.scope_icon()} Current Scope: all (entire project)")
                lines.append("")
                lines.append("To change scope (pick ONE - setting a new scope replaces the previous):")
                lines.append("```powershell")
                lines.append("scope all                            # Clear scope, work on entire project")
                lines.append("scope showAll                        # Show entire story graph (no filtering)")
                lines.append('scope "Story Name"                   # Filter by story (replaces any file scope)')
                lines.append('scope "file:C:/path/to/**/*.py"      # Filter by files (replaces any story scope)')
                lines.append("```")
        
        if not skip_scope:
            lines.append(formatter.subsection_separator())
        else:
            # Still need a separator before progress section
            lines.append(formatter.subsection_separator())
        
        # Progress section
        lines.append(f"## {formatter.position_icon()} **Progress**")
        lines.extend(self._format_code_block(f"{self.progress_path}.{self.stage_name}"))
        lines.append("")
        
        # Show hierarchical status (Behaviors, Actions tree)
        # Use full tree for JSON format (extension panel), current branch for text format (terminal)
        if format == 'json':
            lines.append(self.cli_bot.status.full_hierarchical_status)
        else:
            lines.append(self.cli_bot.status.hierarchical_status)
        
        # Legacy compact summary for tests and quick glance
        behavior_names = self.behavior_names
        if behavior_names:
            lines.append("")
            lines.append(f"**Behaviors:** {' | '.join(behavior_names)}")
        current_behavior = self.current_behavior
        if current_behavior and current_behavior.actions:
            lines.append("**Actions:** " + " | ".join(current_behavior.actions.names))
            lines.append("")
        
        output = "\n".join(lines)
        
        return REPLStateDisplay(
            output=output,
            state_loaded=True,
            current_behavior=self.current_behavior_state,
            current_action=self.current_action_state,
            breadcrumbs=self.cli_bot.status.breadcrumbs
        )
    
    def get_context_header_for_ai(self, skip_scope=False) -> str:
        state_display = self.display_current_state(skip_scope=skip_scope)
        return state_display.output
    
    def _convert_domain_result_to_repl_response(self, result: Dict[str, Any], command: str) -> REPLCommandResponse:
        status = result.get('status', 'success')
        message = result.get('message', '')
        
        # Special handling for exit command
        if command == 'exit' or status == 'exit':
            return REPLCommandResponse(
                output=message or "Goodbye!",
                response="",
                status="exit",
                repl_terminated=True
            )
        
        # Special handling for help command
        if command == 'help':
            help_text = result.get('help_text', message)
            return REPLCommandResponse(
                output=help_text,
                response=help_text,
                status=status
            )
        
        # For scope and path commands, just show the message
        if command in ['scope', 'path']:
            return REPLCommandResponse(
                output=message,
                response=message,
                status=status
            )
        
        # For navigation commands, auto-execute instructions for new position (if successful)
        if command in ['next', 'back', 'advance', 'previous']:
            # If navigation failed (error or at_start/at_end status), just return the error message
            if status in ['error', 'at_start', 'at_end']:
                return REPLCommandResponse(
                    output=message,
                    response=message,
                    status='error'
                )
            # Navigation succeeded - auto-execute instructions for new position
            return self._handle_current_command(auto_execute_instructions=True)
        
        # Default: just return the message
        return REPLCommandResponse(
            output=message,
            response=message,
            status=status
        )
    
    def read_and_execute_command(self, command: str) -> REPLCommandResponse:
        command = command.strip()
        if not command:
            return REPLCommandResponse(output="", response="", status="empty")
        
        # Check for dot notation: first word must contain a dot (behavior.action format)
        # Avoid false positives from dots in arguments like "*.pyc" or file paths
        first_word = command.split()[0] if command.split() else ""
        if '.' in first_word and not first_word.startswith('--'):
            return self._handle_dot_notation(command)
        
        return self._handle_simple_command(command)
    
    def _handle_simple_command(self, command: str) -> REPLCommandResponse:
        parts = command.split(maxsplit=1)
        command_verb = parts[0].lower()
        command_args = parts[1] if len(parts) > 1 else ""
        
        # Meta commands
        if command_verb == 'help':
            return self._handle_help_command(command_args)
        if command_verb == 'status':
            # Parse --format argument
            format_arg = 'text'
            if command_args:
                args_list = command_args.split()
                for i, arg in enumerate(args_list):
                    if arg == '--format' and i + 1 < len(args_list):
                        format_arg = args_list[i + 1]
                        break
            return self._handle_status_command(format=format_arg)
        if command_verb == 'exit':
            return REPLCommandResponse(output="Goodbye!", response="Goodbye!", status="success", repl_terminated=True)
        if command_verb == 'current':
            return self._handle_current_command()
        if command_verb == 'no':
            state_display = self.display_current_state()
            return REPLCommandResponse(output=state_display.output, response="Remaining in current action", status="success")
        
        # Navigation commands
        if command_verb in ['next', 'advance']:
            return self._handle_next_command()
        if command_verb in ['back', 'previous']:
            return self._handle_back_command()
        
        # Workflow commands
        if command_verb == 'instructions':
            return self._handle_instructions_command(command_args)
        if command_verb == 'confirm':
            return self._handle_confirm_command(command_args)
        if command_verb == 'submit':
            return self._handle_submit_command(command_args)
        
        # State commands
        if command_verb == 'path':
            return self._handle_path_command(command_args)
        if command_verb == 'workspace':
            return self._handle_path_command(command_args)  # Alias for path
        if command_verb == 'scope':
            return self._handle_scope_command(command_args)
        
        # Headless mode command
        if command_verb == 'headless':
            return self._handle_headless_command(command_args)
        
        # Check if it's an action shortcut
        action_shortcuts = ["clarify", "strategy", "build", "validate", "render"]
        if command_verb in action_shortcuts:
            return self._handle_action_shortcut(command_verb, command_args)
        
        # Check if it's a behavior name
        behavior = self.cli_bot.behaviors.domain_behaviors.find_by_name(command_verb)
        if behavior:
            return self._handle_behavior_command(command_verb)
        
        return REPLCommandResponse(
            output=f"ERROR: Unknown command '{command_verb}'",
            response=f"ERROR: Unknown command '{command_verb}'",
            status="error"
        )
    
    def _handle_help_command(self, args: str = "") -> REPLCommandResponse:
        if not args:
            output = self.cli_bot.help.main_help
        else:
            if not self.has_current_behavior:
                return REPLCommandResponse(
                    output="ERROR: No current behavior set. Please select a behavior first.",
                    response="ERROR: No current behavior set",
                    status="error"
                )
            action_help = self.cli_bot.help.action_help(self.current_behavior_name, args)
            if not action_help:
                behavior_help = self.cli_bot.help.behavior_help(self.current_behavior_name)
                if not behavior_help:
                    available = ", ".join(self.cli_bot.behaviors.all)
                    return REPLCommandResponse(
                        output=f"ERROR: behavior '{self.current_behavior_name}' not found\nAvailable behaviors: {available}",
                        response=f"ERROR: behavior '{self.current_behavior_name}' not found",
                        status="error"
                    )
                output = f"ERROR: Action '{args}' not found"
            else:
                output = action_help.help_text
        
        # Wrap with context header
        header = self.get_context_header_for_ai()
        full_output = f"{output}\n{header}"
        return REPLCommandResponse(output=full_output, response=output, status="success")
    
    def _handle_status_command(self, format='text') -> REPLCommandResponse:
        """Handle status command - display current state.
        
        Returns formatted output (text or JSON format).
        """
        if format == 'json':
            return self._handle_status_command_json()
        
        # Use display_current_state for text format
        state_display = self.display_current_state(format='text')
        return REPLCommandResponse(output=state_display.output, response="", status="success")
    
    def _handle_status_command_json(self) -> REPLCommandResponse:
        """Handle status command with JSON output format.
        
        Returns JSON formatted status.
        """
        import json
        # Use display_current_state with JSON format
        state_display = self.display_current_state(format='json')
        
        # Wrap in JSON structure
        json_output = {
            "status": "success",
            "output": state_display.output,
            "current_behavior": state_display.current_behavior,
            "current_action": state_display.current_action,
            "breadcrumbs": state_display.breadcrumbs
        }
        
        return REPLCommandResponse(output=json.dumps(json_output, indent=2), response="", status="success")
    
    def _handle_current_command(self, auto_execute_instructions=False) -> REPLCommandResponse:
        if not self.has_current_action:
            return REPLCommandResponse(
                output="ERROR: No current action",
                response="ERROR: No current action",
                status="error"
            )
        
        # If called from navigation, auto-execute instructions
        if auto_execute_instructions:
            # Extract operation from progress (behavior.action.operation)
            progress = self.get_progress_line()
            if '.' in progress and 'Progress: ' in progress:
                parts = progress.replace('Progress: ', '').split('.')
                if len(parts) >= 3:
                    operation = parts[2]
                    if operation == 'instructions':
                        return self._handle_instructions_command("")
                    elif operation == 'confirm':
                        return REPLCommandResponse(
                            output="Cannot re-execute 'confirm'. Use 'next' or 'back' to navigate.",
                            response="Cannot re-execute confirm",
                            status="error"
                        )
            # Default: show instructions
            return self._handle_instructions_command("")
        
        # Otherwise, just show status without executing
        state_display = self.display_current_state()
        return REPLCommandResponse(
            output=state_display.output,
            response="Current position displayed",
            status="success"
        )
    
    def _handle_next_command(self) -> REPLCommandResponse:
        error_response = self._validate_current_action_and_behavior()
        if error_response:
            return error_response
        
        behavior = self.current_behavior
        
        # Try to advance to next action within current behavior
        next_action = behavior.actions.next
        if next_action:
            behavior.actions.domain_actions.navigate_to(next_action.name)
            return self._wrap_navigation_with_instructions()
        
        # At last action - try next behavior
        next_behavior = self.cli_bot.behaviors.next
        if next_behavior:
            if next_behavior.actions.names:
                self.navigate_to_behavior_action(next_behavior.name, next_behavior.actions.names[0])
            return self._wrap_navigation_with_instructions()
        
        return REPLCommandResponse(
            output="ERROR: Already at last action of last behavior",
            response="ERROR: Already at last action",
            status="error"
        )
    
    def _handle_back_command(self) -> REPLCommandResponse:
        error_response = self._validate_current_action_and_behavior()
        if error_response:
            return error_response
        
        behavior = self.current_behavior
        
        # Try to go back to previous action within current behavior
        prev_action = behavior.actions.previous
        if prev_action:
            behavior.actions.domain_actions.navigate_to(prev_action.name)
            return self._wrap_navigation_with_instructions()
        
        # At first action - try previous behavior's last action
        # Get previous behavior using domain behaviors directly
        current_idx = None
        behaviors_list = list(self.cli_bot.behaviors.domain_behaviors._behaviors)
        for idx, beh in enumerate(behaviors_list):
            if beh.name == behavior.name:
                current_idx = idx
                break
        
        if current_idx is not None and current_idx > 0:
            prev_behavior_domain = behaviors_list[current_idx - 1]
            prev_behavior = self.cli_bot.behaviors.get_behavior(prev_behavior_domain.name)
            if prev_behavior and prev_behavior.actions.names:
                last_action_name = prev_behavior.actions.names[-1]
                self.navigate_to_behavior_action(prev_behavior.name, last_action_name)
                return self._wrap_navigation_with_instructions()
        
        return REPLCommandResponse(
            output="ERROR: Already at first action of first behavior",
            response="ERROR: Already at first action",
            status="error"
        )
    
    def _handle_instructions_command(self, args: str = "") -> REPLCommandResponse:
        if not self.has_current_action:
            return REPLCommandResponse(
                output="ERROR: No current action to get instructions for",
                response="ERROR: No current action",
                status="error"
            )
        
        action = self.current_action
        
        # Parse CLI-style arguments if present
        context = None
        if args and args.strip().startswith('--'):
            cli_args = self._tokenize_cli_args(args)
            
            if cli_args:
                try:
                    from agile_bot.bots.base_bot.src.repl_cli.cli_context_builder import CliContextBuilder
                    builder = CliContextBuilder()
                    # Get the underlying action if this is a CLI wrapper
                    underlying_action = action._action if hasattr(action, '_action') else action
                    context = builder.build_context(underlying_action, cli_args)
                    
                    # Store scope if present in context - Scope manages its own persistence
                    if context and hasattr(context, 'scope') and context.scope:
                        context.scope.apply_to_bot(self.workspace_directory)
                except ValueError as e:
                    error_msg = str(e)
                    # Invalid scope type is a real validation error
                    if "Invalid scope type" in error_msg or "invalid_type" in error_msg:
                        return REPLCommandResponse(
                            output=f"ERROR: {error_msg}",
                            response=f"ERROR: {error_msg}",
                            status="error"
                        )
                    # Other errors like unknown parameters - just proceed without context
                    context = None
                except Exception:
                    # Any other parsing errors - proceed without context
                    context = None
        
        try:
            # Call with context if we have one, otherwise pass args as string
            if context:
                output = action.instructions(args="", context=context)
            else:
                output = action.instructions(args)
            
            # TEMPORARILY DISABLED: Auto-confirm behavior (for testing render instructions)
            # # Check if this action has auto_confirm
            # underlying_action = action._action if hasattr(action, '_action') else action
            # if hasattr(underlying_action, 'domain_action'):
            #     underlying_action = underlying_action.domain_action
            # auto_confirm = getattr(underlying_action, 'auto_confirm', False)
            # 
            # if auto_confirm:
            #     # Auto-confirm: show instructions then immediately run confirm
            #     instructions_response = self._wrap_with_context_header(output, "Instructions displayed (auto-confirm)")
            #     confirm_response = self._handle_confirm_command("")
            #     return REPLCommandResponse(
            #         output=instructions_response.output + "\n\n[Auto-confirmed]\n\n" + confirm_response.output,
            #         response="Instructions displayed and auto-confirmed",
            #         status=confirm_response.status
            #     )
            
            # No auto-confirm: show instructions and wait for human to run confirm
            return self._wrap_with_context_header(output, "Instructions displayed")
        except Exception as e:
            return REPLCommandResponse(
                output=f"ERROR getting instructions: {str(e)}",
                response=f"ERROR getting instructions: {str(e)}",
                status="error"
            )
    
    def _handle_confirm_command(self, args: str = "") -> REPLCommandResponse:
        if not self.has_current_action:
            return REPLCommandResponse(
                output="ERROR: No current action to confirm",
                response="ERROR: No current action",
                status="error"
            )
        
        behavior = self.current_behavior
        action = self.current_action
        current_behavior_name = behavior.name
        current_action_name = action.name
        
        try:
            # Check if this action has skip_confirm
            underlying_action = action._action if hasattr(action, '_action') else action
            if hasattr(underlying_action, 'domain_action'):
                underlying_action = underlying_action.domain_action
            skip_confirm = getattr(underlying_action, 'skip_confirm', False)
            
            # Call confirm on the action with any args (unless skip_confirm is set)
            if skip_confirm:
                result_output = f"[skip_confirm] Advancing without confirm for {current_action_name}"
            else:
                result_output = action.confirm(args)
            
            # Check if at last action BEFORE closing
            action_names = behavior.actions.names
            is_last_action = (current_action_name == action_names[-1] if action_names else False)
            
            # Mark current action as complete and advance
            behavior.actions.domain_actions.close_current()
            
            # If not at last action, advance to next action (user will run commands explicitly)
            if not is_last_action:
                return REPLCommandResponse(
                    output=result_output + "\n\n[Action confirmed. Use 'next' or run commands explicitly to continue.]",
                    response="Action confirmed",
                    status="success"
                )
            
            # At last action - behavior is complete
            self._mark_behavior_complete(current_behavior_name)
            
            # Check for next behavior
            next_behavior = self.cli_bot.behaviors.next
            if next_behavior:
                # Advance to next behavior (user will run commands explicitly)
                self.cli_bot.behaviors.domain_behaviors.close_current()
                if next_behavior.actions.names:
                    self.navigate_to_behavior_action(next_behavior.name, next_behavior.actions.names[0])
                    return REPLCommandResponse(
                        output=result_output + f"\n\n[Behavior complete. Advanced to {next_behavior.name}. Use 'next' or run commands explicitly to continue.]",
                        response="Behavior complete, advanced to next",
                        status="success"
                    )
            
            # No more behaviors - all complete
            return REPLCommandResponse(
                output=f"COMPLETE: {current_behavior_name} behavior finished\n\nALL BEHAVIORS COMPLETE!",
                response="COMPLETE: All behaviors finished",
                status="success"
            )
        except Exception as e:
            return REPLCommandResponse(
                output=f"ERROR confirming: {str(e)}",
                response=f"ERROR confirming: {str(e)}",
                status="error"
            )
    
    def _handle_submit_command(self, args: str = "") -> REPLCommandResponse:
        """Get full instructions from bot and submit to Cursor chat using keyboard automation."""
        import traceback
        
        # Get full instructions from bot (not clipboard)
        instructions_response = self._handle_instructions_command(args)
        
        if instructions_response.status == "error":
            return REPLCommandResponse(
                output=f"ERROR: Cannot get instructions\n{instructions_response.output}",
                response="No instructions available",
                status="error"
            )
        
        # Get the FULL instructions output (includes headers and CLI status)
        instructions_text = instructions_response.output
        
        if not instructions_text or len(instructions_text.strip()) == 0:
            return REPLCommandResponse(
                output="ERROR: Instructions are empty",
                response="Empty instructions",
                status="error"
            )
        
        # Copy full instructions to clipboard then automate
        try:
            import pyperclip
            import pyautogui
            import time
            
            # Copy to clipboard
            pyperclip.copy(instructions_text)
            time.sleep(0.2)
            
            # Ctrl+L to open chat
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.3)
            
            # Ctrl+V to paste
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.2)
            
            # Enter to submit
            pyautogui.press('enter')
            
            return REPLCommandResponse(
                output=f"SUCCESS: Full instructions submitted to Cursor chat!\n\nContent length: {len(instructions_text)} characters",
                response="Instructions submitted to Cursor chat successfully",
                status="success",
                action=self.current_action.name if self.has_current_action else None
            )
        except ImportError:
            return REPLCommandResponse(
                output="ERROR: pyautogui/pyperclip not installed. Run: pip install pyautogui pyperclip",
                response="Missing required packages",
                status="error"
            )
        except Exception as e:
            error_detail = traceback.format_exc()
            return REPLCommandResponse(
                output=f"ERROR: Automation failed\n{str(e)}\n\n{error_detail}",
                response=f"Error: {str(e)}",
                status="error"
            )
    
    def _handle_path_command(self, args: str = "") -> REPLCommandResponse:
        if not args:
            # Show current path
            current_path = self.workspace_directory
            return REPLCommandResponse(
                output=f"Current path: {current_path}",
                response=f"Current path: {current_path}",
                status="success"
            )
        
        # Change path
        result = self.cli_bot.change_path(args)
        return REPLCommandResponse(
            output=result['message'],
            response=result['message'],
            status=result['status']
        )
    
    def _handle_scope_command(self, args: str = "") -> REPLCommandResponse:
        if not args:
            # Show current scope
            output = self.cli_bot.get_scope_display()
            return REPLCommandResponse(
                output=output,
                response=output,
                status="success"
            )
        
        # Import Scope and ScopeType for all scope operations
        from agile_bot.bots.base_bot.src.actions.action_context import Scope, ScopeType
        
        # Handle "all" - clears the scope filter
        if args.lower() == 'all':
            result = self.cli_bot.clear_scope()
            return REPLCommandResponse(
                output=result['message'],
                response=result['message'],
                status=result['status']
            )
        
        # Handle "showAll" or "show_all" - shows entire story graph
        if args.lower() in ('showall', 'show_all'):
            scope = Scope(type=ScopeType.SHOW_ALL, value=[])
            result = self.cli_bot.set_scope(scope)
            return REPLCommandResponse(
                output=result['message'],
                response=result['message'],
                status=result['status']
            )
        
        # Parse and set scope
        if args.startswith(('file:', 'files:')):
            prefix = args.split(':', 1)[0].strip().lower()
            value_part = args.split(':', 1)[1].strip()
            scope_values_raw = [v.strip().strip('"').strip("'") for v in value_part.split(',') if v.strip()]
            scope_type = ScopeType.FILES
            scope_value = scope_values_raw
        else:
            scope_values_raw = [v.strip().strip('"').strip("'") for v in args.split(',') if v.strip()]
            
            # Strip "file:" or "files:" prefix if present (can happen when args are quoted)
            cleaned_values = []
            for v in scope_values_raw:
                if v.startswith('file:'):
                    cleaned_values.append(v[5:])  # Remove "file:" prefix
                elif v.startswith('files:'):
                    cleaned_values.append(v[6:])  # Remove "files:" prefix
                else:
                    cleaned_values.append(v)
            
            # Auto-detect if this looks like a file path (absolute or relative with separators)
            import os
            looks_like_path = any(
                os.path.isabs(v) or '\\' in v or '/' in v 
                for v in cleaned_values
            )
            if looks_like_path:
                scope_type = ScopeType.FILES
                scope_value = cleaned_values
            else:
                scope_type = ScopeType.STORY
                scope_value = cleaned_values
        
        scope = Scope(type=scope_type, value=scope_value)
        result = self.cli_bot.set_scope(scope)
        
        output = self.cli_bot.get_scope_display()
        
        return REPLCommandResponse(
            output=output,
            response=output,
            status=result['status'],
            scope_stored=True
        )
    
    def _validate_headless_ready(self, args: str) -> tuple[bool, REPLCommandResponse | None, any]:
        from agile_bot.bots.base_bot.src.repl_cli.headless.headless_config import HeadlessConfig
        
        # Check if args provided
        if not args:
            return False, REPLCommandResponse(
                output="ERROR: headless command requires a message\n"
                       "Usage: headless \"Your instruction here\"",
                response="Missing message argument",
                status="error"
            ), None
        
        # Check if headless mode is configured
        try:
            config = HeadlessConfig.load()
            if not config.is_configured:
                return False, REPLCommandResponse(
                    output="ERROR: Headless mode not configured. API key required.\n"
                           "To configure:\n"
                           "  1. Create file: agile_bot/secrets/cursor_api_key.txt\n"
                           "  2. Add your Cursor API key to the file\n"
                           "  3. Restart the REPL",
                    response="Headless mode not configured",
                    status="error"
                ), None
        except Exception as e:
            return False, REPLCommandResponse(
                output=f"ERROR: Failed to load headless config: {e}",
                response="Failed to load headless config",
                status="error"
            ), None
        
        return True, None, config
    
    def _parse_headless_args(self, args: str) -> tuple[str | None, str]:
        import shlex
        
        try:
            parsed_args = shlex.split(args)
        except ValueError:
            # If shlex fails, treat entire args as message
            return None, args.strip().strip('"').strip("'")
        
        if not parsed_args:
            return None, args.strip().strip('"').strip("'")
        
        first_arg = parsed_args[0]
        
        # Check if first arg looks like a target (behavior.action format)
        if '.' in first_arg and all(c.isalnum() or c in '._-' for c in first_arg):
            # It's a target
            target = first_arg
            rest_of_args = ' '.join(parsed_args[1:]) if len(parsed_args) > 1 else ""
            return target, rest_of_args
        else:
            # Not a target, everything is a message
            return None, args.strip().strip('"').strip("'")
    
    def _execute_operation_locally(self, target: str, cli_args: str = "") -> str:
        # Parse target
        parts = target.split('.')
        if len(parts) < 2:
            return f"[Error: Invalid target '{target}']"
        
        behavior_name = parts[0]
        action_name = parts[1]
        operation = parts[2] if len(parts) >= 3 else 'instructions'  # Default to instructions
        
        try:
            # Parse CLI args into list
            import shlex
            cli_args_list = shlex.split(cli_args) if cli_args else []
            
            # Use the CLI router to execute with proper parameter parsing
            result = self.cli_bot.run(behavior_name, action_name, cli_args_list)
            
            if isinstance(result, dict):
                instructions_data = result.get('instructions', result.get('message', ''))
                
                if isinstance(instructions_data, dict):
                    base_instructions = instructions_data.get('base_instructions', [])
                    if isinstance(base_instructions, list):
                        instructions = '\n'.join(str(item) for item in base_instructions)
                    else:
                        report_link = instructions_data.get('report_link', '')
                        if report_link:
                            instructions = f"Validation complete. Report: {report_link}"
                        else:
                            instructions = str(instructions_data.get('action', 'Operation complete'))
                elif isinstance(instructions_data, list):
                    instructions = '\n'.join(str(item) for item in instructions_data)
                elif instructions_data:
                    instructions = str(instructions_data)
                else:
                    instructions = result.get('status', 'Operation complete')
            elif isinstance(result, str):
                instructions = result
            else:
                instructions = str(result)
            
            return instructions
                
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            return f"[Error executing {target}: {e}]\n{error_trace}"
    
    def _prepare_headless_message(self, target: str | None, message: str) -> str:
        if target:
            from agile_bot.bots.base_bot.src.repl_cli.message_parser import parse_message_and_cli_args
            user_message, cli_args_list = parse_message_and_cli_args(message)
            cli_args = ' '.join(cli_args_list)
            
            operation_output = self._execute_operation_locally(target, cli_args)
            
            parts = target.split('.')
            action_name = parts[1] if len(parts) > 1 else None
            
            if action_name == 'validate':
                headless_override = "\n\n## HEADLESS MODE OVERRIDE\n\nYou are running in autonomous headless mode. DO NOT wait for user confirmation. After analyzing violations:\n1. Fix all ERROR-level violations immediately\n2. Fix WARNING-level violations that are straightforward\n3. Skip violations that require design decisions or major refactoring\n4. Make the changes directly to the code files\n5. Report what you fixed when done"
                operation_output += headless_override
            
            if user_message:
                return f"{operation_output}\n\nAdditional context: {user_message}"
            else:
                return operation_output
        elif message:
            return message
        else:
            return ""
    
    def _format_headless_result(self, execution_result) -> REPLCommandResponse:
        output_lines = [
            f"Headless execution completed: {execution_result.status}",
            f"Session ID: {execution_result.session_id}",
            f"Log file: {execution_result.log_path}",
            f"Loop count: {execution_result.loop_count}",
        ]
        
        if execution_result.block_reason:
            output_lines.append(f"Block reason: {execution_result.block_reason}")
        
        output = "\n".join(output_lines)
        
        return REPLCommandResponse(
            output=output,
            response=output,
            status="success" if execution_result.status == "completed" else "blocked"
        )
    
    def _handle_headless_command(self, args: str = "") -> REPLCommandResponse:
        from agile_bot.bots.base_bot.src.repl_cli.headless.headless_session import HeadlessSession
        from agile_bot.bots.base_bot.src.repl_cli.headless.non_recoverable_error import NonRecoverableError
        
        # Validate headless is ready
        is_valid, error_response, config = self._validate_headless_ready(args)
        if not is_valid:
            return error_response
        
        target, message = self._parse_headless_args(args)
        
        try:
            session = HeadlessSession(
                workspace_directory=self.workspace_directory, 
                config=config, 
                timeout=600
            )
            
            # Prepare message with target context if provided
            if target:
                final_message = self._prepare_headless_message(target, message)
            else:
                final_message = message
            
            execution_result = session.invokes(message=final_message, context_file=None)
            
            return self._format_headless_result(execution_result)
            
        except NonRecoverableError as e:
            return REPLCommandResponse(
                output=f"ERROR: {e}",
                response=str(e),
                status="error"
            )
        except Exception as e:
            return REPLCommandResponse(
                output=f"ERROR: Headless execution failed: {e}",
                response=str(e),
                status="error"
            )
    
    def _handle_behavior_command(self, behavior_name: str) -> REPLCommandResponse:
        behavior = self.cli_bot.behaviors.domain_behaviors.find_by_name(behavior_name)
        if not behavior:
            available = ", ".join(self.cli_bot.behaviors.all)
            return REPLCommandResponse(
                output=f"ERROR: behavior '{behavior_name}' not found\nAvailable behaviors: {available}",
                response=f"ERROR: behavior '{behavior_name}' not found",
                status="error"
            )
        
        if not behavior.actions.names:
            return REPLCommandResponse(
                output=f"ERROR: behavior '{behavior_name}' has no actions",
                response=f"ERROR: behavior '{behavior_name}' has no actions",
                status="error"
            )
        
        first_action_name = behavior.actions.names[0]
        try:
            self.navigate_to_behavior_action(behavior_name, first_action_name)
        except ValueError as e:
            return REPLCommandResponse(
                output=f"ERROR: {str(e)}",
                response=f"ERROR: {str(e)}",
                status="error"
            )
        return self._handle_instructions_command()
    
    def navigate_to_behavior_action(self, behavior_name: str, action_name: str):
        self.cli_bot.behaviors.domain_behaviors.navigate_to(behavior_name)
        behavior = self.cli_bot.behaviors.domain_behaviors.find_by_name(behavior_name)
        if behavior:
            # Navigate to action within the behavior
            try:
                behavior.actions.navigate_to(action_name)
            except ValueError as e:
                # Add behavior context to error message
                available_actions = ", ".join(behavior.actions.names)
                raise ValueError(f"Action '{action_name}' not found in behavior '{behavior_name}'. Available actions: {available_actions}")
        else:
            raise ValueError(f"Behavior '{behavior_name}' not found")
    
    def _wrap_navigation_with_instructions(self) -> REPLCommandResponse:
        return self._handle_instructions_command()
    
    def _wrap_with_context_header(self, content: str, response_msg: str) -> REPLCommandResponse:
        formatter = self.formatter
        # Skip scope in status header if we're in instructions phase (scope already shown at top of instructions)
        skip_scope = (self.action_phase == 'instructions')
        header = self.get_context_header_for_ai(skip_scope=skip_scope)
        
        # Instructions section header (thick line)
        instructions_header = "\n".join([
            "",
            formatter.section_separator(),
            "**INSTRUCTIONS SECTION:**",
            "☢️ This section contains both scope filter and a prompt that you must follow for the current action. ☢️",
            "☢️ You MUST follow the instructions below in this section to the letter. ☢️",
            formatter.subsection_separator()
        ])
        
        # CLI STATUS section header (comes after the actual content)
        cli_status_header = "\n".join([
            "",
            formatter.section_separator(),
            "***                    CLI STATUS section                    ***",
            "This section contains current scope filter (if set), current progress in workflow, and available commands",
            "Review the CLI STATUS section below to understand both current state and available commands.",
            "☢️  You MUST DISPLAY this entire section in your response to the user exactly as you see it. ☢️",
            formatter.subsection_separator()
        ])
        
        output = "\n".join([
            instructions_header,
            content,
            cli_status_header,
            header,
            formatter.section_separator()
        ])
        
        return REPLCommandResponse(
            output=output,
            response=response_msg,
            status="success",
            action=self.current_action.name if self.has_current_action else None
        )
    
    def _mark_behavior_complete(self, behavior_name: str) -> None:
        state_file = self.workspace_directory / 'behavior_action_state.json'
        if not state_file.exists():
            return
        try:
            state_data = json.loads(state_file.read_text())
            completed = state_data.get('completed_behaviors', [])
            if behavior_name not in completed:
                completed.append(behavior_name)
            state_data['completed_behaviors'] = completed
            state_file.write_text(json.dumps(state_data, indent=2))
        except (json.JSONDecodeError, IOError) as e:
            logging.warning(f"Failed to mark behavior {behavior_name} as complete in state file {state_file}: {e}")
    
    def _handle_dot_notation(self, command: str) -> REPLCommandResponse:
        # Parse dot notation: behavior.action.operation or action.operation or .operation
        parts = command.split()
        dot_path = parts[0]
        args = ' '.join(parts[1:]) if len(parts) > 1 else ""
        
        path_parts = dot_path.split('.')
        
        # . alone means current position
        if dot_path == '.':
            return self._handle_current_command()
        
        # .operation means current behavior.action, just execute operation
        if dot_path.startswith('.'):
            operation = path_parts[1] if len(path_parts) > 1 else ""
            if operation == 'instructions':
                return self._handle_instructions_command(args)
            elif operation == 'confirm':
                return self._handle_confirm_command(args)
            else:
                return REPLCommandResponse(
                    output=f"ERROR: Unknown operation '{operation}'\nUse: instructions or confirm",
                    response=f"ERROR: Unknown operation '{operation}'",
                    status="error"
                )
        
        # behavior.action.operation or behavior.action or action.operation
        if len(path_parts) == 3:
            # Full path: behavior.action.operation
            behavior_name, action_name, operation = path_parts
            
            # Validate operation first before navigating (to avoid state changes on error)
            if operation not in ('instructions', 'confirm'):
                return REPLCommandResponse(
                    output=f"ERROR: Unknown operation '{operation}'\nUse: instructions or confirm",
                    response=f"ERROR: Unknown operation '{operation}'",
                    status="error"
                )
            
            try:
                self.navigate_to_behavior_action(behavior_name, action_name)
            except ValueError as e:
                return REPLCommandResponse(
                    output=f"ERROR: {str(e)}",
                    response=f"ERROR: {str(e)}",
                    status="error"
                )
            
            if operation == 'instructions':
                return self._handle_instructions_command(args)
            elif operation == 'confirm':
                return self._handle_confirm_command(args)
        elif len(path_parts) == 2:
            # behavior.action or action.operation
            first, second = path_parts
            # Check if first part is a behavior name
            behavior = self.cli_bot.behaviors.domain_behaviors.find_by_name(first)
            if behavior:
                # It's behavior.action
                try:
                    self.navigate_to_behavior_action(first, second)
                except ValueError as e:
                    return REPLCommandResponse(
                        output=f"ERROR: {str(e)}",
                        response=f"ERROR: {str(e)}",
                        status="error"
                    )
                return self._handle_instructions_command(args)
            else:
                # Could be action.operation or invalid behavior
                # Check if we have a current behavior (for action.operation)
                if not self.has_current_behavior:
                    # No current behavior, so this must be an invalid behavior name
                    available_behaviors = ", ".join(self.cli_bot.behaviors.domain_behaviors.names)
                    return REPLCommandResponse(
                        output=f"ERROR: behavior '{first}' not found\nAvailable behaviors: {available_behaviors}",
                        response=f"ERROR: behavior '{first}' not found",
                        status="error"
                    )
                # Check if first part is a valid action in current behavior
                action = self.current_behavior.actions.find_by_name(first)
                if action:
                    # It's action.operation
                    action_name, operation = first, second
                    try:
                        self.current_behavior.actions.domain_actions.navigate_to(action_name)
                    except ValueError as e:
                        # Add behavior context to error message
                        behavior_name = self.current_behavior.name
                        available_actions = ", ".join(self.current_behavior.actions.names)
                        error_msg = f"Action '{action_name}' not found in behavior '{behavior_name}'. Available actions: {available_actions}"
                        return REPLCommandResponse(
                            output=f"ERROR: {error_msg}",
                            response=f"ERROR: Action '{action_name}' not found in behavior '{behavior_name}'",
                            status="error"
                        )
                    if operation == 'instructions':
                        return self._handle_instructions_command(args)
                    elif operation == 'confirm':
                        return self._handle_confirm_command(args)
                    else:
                        return REPLCommandResponse(
                            output=f"ERROR: Unknown operation '{operation}'",
                            response=f"ERROR: Unknown operation",
                            status="error"
                        )
                else:
                    # Not a behavior or action, must be invalid behavior
                    available_behaviors = ", ".join(self.cli_bot.behaviors.domain_behaviors.names)
                    return REPLCommandResponse(
                        output=f"ERROR: behavior '{first}' not found\nAvailable behaviors: {available_behaviors}",
                        response=f"ERROR: behavior '{first}' not found",
                        status="error"
                    )
        else:
            return REPLCommandResponse(
                output=f"ERROR: Invalid dot notation '{dot_path}'",
                response=f"ERROR: Invalid dot notation",
                status="error"
            )
    
    def _handle_action_shortcut(self, action_name: str, args_str: str) -> REPLCommandResponse:
        args_str = args_str.strip()
        
        # Parse CLI-style arguments (--message, --scope, etc.)
        cli_args = []
        subcommand = None
        
        if args_str:
            if args_str.startswith('--'):
                cli_args = self._tokenize_cli_args(args_str)
            else:
                parts = args_str.split(maxsplit=1)
                subcommand = parts[0].lower()
                if len(parts) > 1 and parts[1].startswith('--'):
                    cli_args = self._tokenize_cli_args(parts[1])
        
        if not subcommand:
            phase_map = {'not_started': 'instructions', 'instructions_given': 'confirm'}
            subcommand = phase_map.get(self.action_phase, 'instructions')
        
        if subcommand in ("instructions", "run", "execute") or cli_args:
            operation = "instructions" if subcommand == "instructions" else None
            return self._execute_action_with_args(action_name, cli_args, operation=operation)
        
        if subcommand == "confirm":
            if not self.has_current_behavior:
                return REPLCommandResponse(
                    output="ERROR: No current behavior set. Please select a behavior first.",
                    response="ERROR: No current behavior set",
                    status="error"
                )
            behavior = self.current_behavior
            action = behavior.actions.find_by_name(action_name)
            if not action:
                available = ", ".join(behavior.actions.names) if behavior else ""
                return REPLCommandResponse(
                    output=f"ERROR: action '{action_name}' not found\nAvailable actions: {available}",
                    response=f"ERROR: action '{action_name}' not found",
                    status="error"
                )
            try:
                behavior.actions.domain_actions.navigate_to(action_name)
            except ValueError as e:
                # Add behavior context to error message
                available_actions = ", ".join(behavior.actions.names)
                return REPLCommandResponse(
                    output=f"ERROR: Action '{action_name}' not found in behavior '{behavior.name}'. Available actions: {available_actions}",
                    response=f"ERROR: Action '{action_name}' not found in behavior '{behavior.name}'",
                    status="error"
                )
            return self._handle_confirm_command("")
        
        return REPLCommandResponse(
            output=f"ERROR: Unknown subcommand '{subcommand}'. Use 'instructions' or 'confirm'.",
            response=f"ERROR: Unknown subcommand '{subcommand}'",
            status="error"
        )
    
    def _tokenize_cli_args(self, args_str: str) -> list:
        import shlex
        try:
            return shlex.split(args_str)
        except ValueError:
            return args_str.split()
    
    def _convert_repl_scope_to_cli_format(self, cli_args: list) -> list:
        import json
        converted_args = []
        i = 0
        while i < len(cli_args):
            arg = cli_args[i]
            if arg == '--scope' and i + 1 < len(cli_args):
                scope_value = cli_args[i + 1]
                if scope_value.startswith(('file:', 'files:')):
                    prefix = 'file:' if scope_value.startswith('file:') else 'files:'
                    paths = scope_value[len(prefix):].split(',')
                    paths = [p.strip() for p in paths if p.strip()]
                    json_scope = json.dumps({"type": "files", "value": paths})
                    converted_args.append('--scope')
                    converted_args.append(json_scope)
                    i += 2
                else:
                    converted_args.append(arg)
                    converted_args.append(scope_value)
                    i += 2
            elif arg.startswith('--scope='):
                scope_value = arg.split('=', 1)[1]
                if scope_value.startswith(('file:', 'files:')):
                    prefix = 'file:' if scope_value.startswith('file:') else 'files:'
                    paths = scope_value[len(prefix):].split(',')
                    paths = [p.strip() for p in paths if p.strip()]
                    json_scope = json.dumps({"type": "files", "value": paths})
                    converted_args.append(f'--scope={json_scope}')
                    i += 1
                else:
                    converted_args.append(arg)
                    i += 1
            else:
                converted_args.append(arg)
                i += 1
        return converted_args
    
    def _execute_action_with_args(self, action_name: str, cli_args: list, operation: str = None) -> REPLCommandResponse:
        if not self.has_current_behavior:
            return REPLCommandResponse(
                output="ERROR: No current behavior set. Please select a behavior first.",
                response="ERROR: No current behavior set",
                status="error"
            )
        
        behavior = self.current_behavior
        action = behavior.actions.find_by_name(action_name)
        if not action:
            available = ", ".join(behavior.actions.names) if behavior else ""
            return REPLCommandResponse(
                output=f"ERROR: action '{action_name}' not found\nAvailable actions: {available}",
                response=f"ERROR: action '{action_name}' not found",
                status="error"
            )
        
        try:
            behavior.actions.navigate_to(action_name)
        except ValueError as e:
            # Add behavior context to error message
            available_actions = ", ".join(behavior.actions.names)
            return REPLCommandResponse(
                output=f"ERROR: Action '{action_name}' not found in behavior '{behavior.name}'. Available actions: {available_actions}",
                response=f"ERROR: Action '{action_name}' not found in behavior '{behavior.name}'",
                status="error"
            )
        
        # Parse CLI args into context if provided
        context = None
        if cli_args:
            import sys
            print(f"[DEBUG REPL] Parsing CLI args: {cli_args}", file=sys.stderr)
            try:
                from agile_bot.bots.base_bot.src.repl_cli.cli_context_builder import CliContextBuilder
                builder = CliContextBuilder()
                context = builder.build_context(action, cli_args)
                print(f"[DEBUG REPL] Built context: {context}", file=sys.stderr)
                
                # Store scope if present in context - Scope manages its own persistence
                if context and hasattr(context, 'scope') and context.scope:
                    print(f"[DEBUG REPL] Applying scope to bot: {context.scope}", file=sys.stderr)
                    context.scope.apply_to_bot(self.workspace_directory)
            except ValueError as e:
                print(f"[DEBUG REPL] ValueError: {e}", file=sys.stderr)
                error_msg = str(e)
                # Invalid scope type is a real validation error
                if "Invalid scope type" in error_msg or "invalid_type" in error_msg:
                    return REPLCommandResponse(
                        output=f"ERROR: {error_msg}",
                        response=f"ERROR: {error_msg}",
                        status="error"
                    )
                # Other errors like unknown parameters - just proceed without context
                context = None
            except Exception as e:
                print(f"[DEBUG REPL] Exception: {type(e).__name__}: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc(file=sys.stderr)
                # Any other parsing errors - proceed without context
                context = None
        
        # Call the action's instructions method directly
        try:
            output = action.instructions(args="", context=context)
            return self._wrap_with_context_header(output, f"Instructions for {action.name}")
        except Exception as e:
            return REPLCommandResponse(
                output=f"ERROR getting instructions: {str(e)}",
                response=f"ERROR getting instructions: {str(e)}",
                status="error"
            )
    
    def display_confirm_prompt(self) -> REPLStateDisplay:
        if not self.has_current_action:
            return REPLStateDisplay(output="ERROR: No current action", state_loaded=False)
        
        behavior = self.current_behavior
        if not behavior:
            return REPLStateDisplay(output="ERROR: behavior not found", state_loaded=False)
        
        next_action = behavior.actions.next()
        next_action_name = next_action.action_name if next_action else "none"
        
        output = "\n".join([
            f"EXECUTED {self.current_behavior_name}.{self.current_action_name}",
            "Results:",
            "[Mock results - not executing real action]",
            f"Continue to next action ({next_action_name})? (y/n/review)"
        ])
        
        return REPLStateDisplay(
            output=output,
            state_loaded=True,
            current_behavior=self.current_behavior_state,
            current_action=self.current_action_state
        )
    
    def _format_code_block(self, content: str) -> List[str]:
        """Format content as a code block with triple backticks."""
        return ["```", content, "```"]
    
    def _validate_current_action_and_behavior(self) -> Optional[REPLCommandResponse]:
        """Validate that current action and behavior exist. Returns error response if invalid, None if valid."""
        if not self.has_current_action:
            return REPLCommandResponse(
                output="ERROR: No current action",
                response="ERROR: No current action",
                status="error"
            )
        
        behavior = self.current_behavior
        if not behavior:
            return REPLCommandResponse(
                output="ERROR: No current behavior set. Please select a behavior first.",
                response="ERROR: No current behavior set",
                status="error"
            )
        
        return None
    
    def parse_command_parameters(self, args: str) -> Dict[str, Any]:
        params = {}
        if args is None or args == "":
            return params
        
        # Match --param "quoted value" or --param value
        pattern = r'--(\w+(?:-\w+)*)\s+(?:"([^"]*)"|\'([^\']*)\'|(\S+))'
        for match in re.finditer(pattern, args):
            param_name = match.group(1).replace('-', '_')
            value = match.group(2) or match.group(3) or match.group(4)
            params[param_name] = value
        
        return params
    
    def parse_scope_from_string(self, scope_str: str) -> Optional[Scope]:
        if not scope_str:
            return None
        try:
            data = json.loads(scope_str.replace("'", '"'))
            return Scope.from_dict(data)
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Invalid scope format: {e}")
    
    def get_stored_scope(self) -> Optional[Dict[str, Any]]:
        state_file = self._get_state_file_path()
        if not state_file.exists():
            return None
        try:
            state_data = json.loads(state_file.read_text())
            return state_data.get('scope')
        except (json.JSONDecodeError, KeyError):
            return None
    
    def _get_scope_display_lines(self) -> List[str]:
        scope_data = self.get_stored_scope()
        if not scope_data:
            return []
        
        # Use the Scope object's to_display_lines for consistency
        from agile_bot.bots.base_bot.src.actions.action_context import Scope
        try:
            scope = Scope.from_dict(scope_data)
            return scope.to_display_lines(self.workspace_directory)
        except Exception:
            # Fallback to simple display
            lines = []
            scope_type = scope_data.get('type', 'unknown')
            scope_value = scope_data.get('value', [])
            filter_str = ', '.join(scope_value) if isinstance(scope_value, list) else str(scope_value)
            lines.append(f"Scope Filter: {filter_str}")
            if isinstance(scope_value, list):
                for item in scope_value:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"  - {scope_value}")
            return lines
    
    def _find_scope_matches(self, graph_data: Dict[str, Any], scope_values: List[str]) -> List[str]:
        from agile_bot.bots.base_bot.src.actions.scope_matcher import find_scope_matches
        return find_scope_matches(graph_data, scope_values, use_emoji=False)
    
    def _get_state_file_path(self) -> Path:
        return self.workspace_directory / 'behavior_action_state.json'
    
