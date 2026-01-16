from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from agile_bot.bots.base_bot.src.actions.actions import Actions
    from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
    from agile_bot.bots.base_bot.src.repl_cli.cli_bot.cli_actions.cli_action import CLIAction


class CLIActions:
    
    def __init__(self, actions: Actions, session: REPLSession):
        self._actions = actions
        self._session = session
        self._cli_actions_cache = {}
    
    @property
    def current(self) -> Optional[CLIAction]:
        domain_action = self._actions.current
        if domain_action is None:
            return None
        return self._get_cli_action(domain_action.action_name)
    
    @property
    def next(self) -> Optional[CLIAction]:
        domain_next = self._actions.next()
        if domain_next is None:
            return None
        return self._get_cli_action(domain_next.action_name)
    
    @property
    def previous(self) -> Optional[CLIAction]:
        domain_prev = self._actions.previous()
        if domain_prev is None:
            return None
        return self._get_cli_action(domain_prev.action_name)
    
    @property
    def all(self) -> List[str]:
        return self._actions.names
    
    @property
    def names(self) -> List[str]:
        return self._actions.names
    
    def is_action_completed(self, name: str) -> bool:
        return self._actions.is_action_completed(name)
    
    def navigate_to(self, name: str) -> str:
        try:
            self._actions.navigate_to(name)
            return f"Navigated to action: {name}"
        except Exception as e:
            return f"Error navigating to action '{name}': {str(e)}"
    
    def get_action(self, name: str) -> Optional[CLIAction]:
        return self._get_cli_action(name)
    
    def find_by_name(self, name: str) -> Optional[CLIAction]:
        """Find action by name (alias for get_action to match domain API)"""
        return self.get_action(name)
    
    def _get_cli_action(self, name: str) -> Optional[CLIAction]:
        if name not in self._cli_actions_cache:
            domain_action = self._actions.find_by_name(name)
            if domain_action is None:
                return None
            
            from agile_bot.bots.base_bot.src.repl_cli.cli_bot.cli_actions.cli_action import CLIAction
            from agile_bot.bots.base_bot.src.repl_cli.cli_bot.cli_actions.cli_action_factory import CLIActionFactory
            
            cli_action = CLIActionFactory.create_cli_action(domain_action, self._session)
            self._cli_actions_cache[name] = cli_action
            return cli_action
        return self._cli_actions_cache[name]
    
    @property
    def domain_actions(self) -> Actions:
        return self._actions
    
    @property
    def help(self) -> str:
        """Get help for actions"""
        actions_list = ", ".join(self.all)
        lines = [
            "**Available Actions:**",
            f"  {actions_list}",
            "",
            "**Usage:**",
            "  actions.current          - access current action",
            "  actions.navigate_to(name) - navigate to specific action",
            "  actions.current.help     - get help for current action",
        ]
        return "\n".join(lines)
    
    def __iter__(self):
        """Make CLIActions iterable - yields CLIAction objects for each action"""
        for action_name in self._actions.names:
            yield self._get_cli_action(action_name)

