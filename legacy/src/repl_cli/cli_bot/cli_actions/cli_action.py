from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any
import json
from ...cli_scope import CLIScope

if TYPE_CHECKING:
    from ...actions.action import Action
    from ...repl_cli.repl_session import REPLSession


class CLIAction:
    
    def __init__(self, action: Action, session: REPLSession):
        self._action = action
        self._session = session
    
    @property
    def name(self) -> str:
        return self._action.action_name
    
    @property
    def description(self) -> str:
        return self._action.description
    
    @property
    def status(self) -> str:
        if hasattr(self._action, 'is_completed') and self._action.is_completed:
            return "completed"
        return "pending"
    
    def instructions(self, args: str = "", context = None) -> str:
        try:
            # Update phase to 'instructions' to indicate we're at the instructions operation
            self._session.set_action_phase('instructions')
            # If a context object is provided, use it directly; otherwise parse from args
            if context is None:
                context = self._parse_args_to_context(args)
            result = self._action.get_instructions(context)
            formatted = self._format_result(result)
            
            # Prepend scope display if scope is set (CLI layer adds formatting)
            instructions_obj = self._action.instructions
            if instructions_obj.scope:
                cli_scope = CLIScope(
                    instructions_obj.scope, 
                    self._action.behavior.bot_paths.workspace_directory,
                    self._session.formatter
                )
                scope_display = cli_scope.to_formatted_display()
                formatted = scope_display + formatted
            
            return formatted
        except Exception as e:
            return f"Error getting instructions: {str(e)}"
    
    def confirm(self, args: str = "") -> str:
        try:
            # Update phase to 'confirming' to indicate we're at the confirm operation
            self._session.set_action_phase('confirming')
            context = self._parse_args_to_context(args) if args else self._action.context_class()
            result = self._action.confirm(context)
            return self._format_result(result)
        except Exception as e:
            return f"Error confirming: {str(e)}"
    
    def _parse_args_to_context(self, args: str):
        context_class = self._action.context_class
        if not args or args.strip() == "":
            return context_class()
        
        try:
            args_dict = json.loads(args)
            return context_class(**args_dict)
        except (json.JSONDecodeError, TypeError):
            return context_class()
    
    def _format_result(self, action_result: Any) -> str:
        if isinstance(action_result, dict):
            # First check for formatted_output (from get_instructions)
            if 'formatted_output' in action_result:
                return action_result['formatted_output']
            # Then check for output (from confirm)
            if 'output' in action_result:
                output = action_result['output']
                if isinstance(output, str):
                    return output
                return json.dumps(output, indent=2)
            return json.dumps(action_result, indent=2)
        if isinstance(action_result, str):
            return action_result
        return str(action_result)
    
    @property
    def domain_action(self) -> Action:
        return self._action
    
    @property
    def help(self) -> str:
        """Get help for this specific action"""
        from ...repl_cli.repl_help import ActionHelp
        action_help = ActionHelp(self._action, self.name)
        return action_help.help_text

