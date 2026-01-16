from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...bot.bot import Bot
    from ..repl_session import REPLSession

from .cli_behaviors import CLIBehaviors
from ..repl_help import REPLHelp
from ..repl_status import REPLStatus
from ..cli_command_router import CliCommandRouter
from typing import Dict, Any, List, Optional


class CLIBot:
    
    def __init__(self, bot: Bot, session: REPLSession):
        self._bot = bot
        self._session = session
        self._behaviors = CLIBehaviors(bot.behaviors, session)
        self._help = None  # Lazy-loaded
        self._status = None  # Lazy-loaded
    
    @property
    def name(self) -> str:
        return self._bot.name
    
    @property
    def path(self) -> str:
        return str(self._bot.bot_paths.workspace_directory)
    
    @property
    def behaviors(self) -> CLIBehaviors:
        return self._behaviors
    
    @property
    def bot_directory(self) -> str:
        return str(self._bot.bot_paths.bot_directory)
    
    @property
    def domain_bot(self) -> Bot:
        return self._bot
    
    @property
    def help(self) -> REPLHelp:
        if self._help is None:
            self._help = REPLHelp(self._bot)
        return self._help
    
    @property
    def status(self) -> REPLStatus:
        if self._status is None:
            self._status = REPLStatus(self, self._session, self._session.formatter)
        return self._status
    
    def change_path(self, new_path: str) -> dict:
        """Change the workspace path. Returns result dict with status and message."""
        import json
        from pathlib import Path
        
        workspace_directory = self._session.workspace_directory
        state_file = workspace_directory / 'behavior_action_state.json'
        
        if state_file.exists():
            state_data = json.loads(state_file.read_text())
        else:
            state_data = {}
        
        state_data['working_directory'] = new_path
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(json.dumps(state_data, indent=2))
        
        return {
            'status': 'success',
            'message': f'Path changed to: {new_path}',
            'path': new_path
        }
    
    def set_scope(self, scope) -> dict:
        """Set the scope filter. Scope manages its own persistence, ensuring only one scope exists."""
        # Scope object handles clearing old scope and storing itself
        scope.apply_to_bot(self._session.workspace_directory)
        
        display_lines = scope.to_display_lines(self._session.workspace_directory)
        return {
            'status': 'success',
            'message': f'Scope set to: {" ".join(display_lines)}',
            'scope': scope
        }
    
    def clear_scope(self) -> dict:
        """Clear the scope filter. Scope manages its own removal from state."""
        from agile_bot.bots.base_bot.src.actions.action_context import Scope
        Scope.clear_from_bot(self._session.workspace_directory)
        return {
            'status': 'success',
            'message': 'Scope filter cleared'
        }
    
    def get_scope_display(self, format='text') -> str:
        """Get the current scope display formatted by CLIScope.
        
        Args:
            format: 'text' for formatted display, 'json' for JSON output
        """
        scope_data = self._session.get_stored_scope()
        if scope_data:
            try:
                from agile_bot.bots.base_bot.src.actions.action_context import Scope
                from agile_bot.bots.base_bot.src.repl_cli.cli_scope import CLIScope
                scope = Scope.from_dict(scope_data)
                cli_scope = CLIScope(scope, self._session.workspace_directory, self._session.formatter)
                
                if format == 'json':
                    return cli_scope.to_json_display()
                else:
                    return cli_scope.to_formatted_display()
            except Exception as e:
                # Return formatted error with details for debugging
                return f"{self._session.formatter.scope_icon()} **Scope**\n{self._session.formatter.scope_icon()} Error loading scope: {str(e)}"
        return ""
    
    def run(self, behavior_name: Optional[str] = None, action_name: Optional[str] = None, cli_args: Optional[List[str]] = None) -> Dict[str, Any]:
        """Execute a behavior and/or action with CLI arguments.
        
        Args:
            behavior_name: Name of the behavior to execute
            action_name: Name of the action to execute (optional)
            cli_args: List of CLI arguments to pass to the action
            
        Returns:
            Dictionary with status, behavior, action, and data keys
        """
        router = CliCommandRouter(self._bot)
        return router.route_to_action(behavior_name, action_name, cli_args or [])

