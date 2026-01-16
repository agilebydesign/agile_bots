from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ...bot.behaviors import Behaviors
    from ..repl_session import REPLSession

from .cli_behavior import CLIBehavior


class CLIBehaviors:
    
    def __init__(self, behaviors: Behaviors, session: REPLSession):
        self._behaviors = behaviors
        self._session = session
        self._cli_behaviors_cache = {}
    
    @property
    def current(self) -> Optional[CLIBehavior]:
        domain_behavior = self._behaviors.current
        if domain_behavior is None:
            return None
        return self._get_cli_behavior(domain_behavior.name)
    
    @property
    def next(self) -> Optional[CLIBehavior]:
        current_behavior = self._behaviors.current
        if not current_behavior:
            return None
        behaviors_list = self._behaviors._behaviors
        current_index = behaviors_list.index(current_behavior)
        if current_index + 1 < len(behaviors_list):
            next_behavior = behaviors_list[current_index + 1]
            return self._get_cli_behavior(next_behavior.name)
        return None
    
    @property
    def all(self) -> List[str]:
        return self._behaviors.names
    
    def navigate_to(self, name: str) -> str:
        try:
            self._behaviors.navigate_to(name)
            return f"Navigated to behavior: {name}"
        except Exception as e:
            return f"Error navigating to behavior '{name}': {str(e)}"
    
    def get_behavior(self, name: str) -> Optional[CLIBehavior]:
        return self._get_cli_behavior(name)
    
    def _get_cli_behavior(self, name: str) -> Optional[CLIBehavior]:
        if name not in self._cli_behaviors_cache:
            for behavior in self._behaviors._behaviors:
                if behavior.name == name:
                    self._cli_behaviors_cache[name] = CLIBehavior(behavior, self._session)
                    return self._cli_behaviors_cache[name]
            return None
        return self._cli_behaviors_cache[name]
    
    @property
    def domain_behaviors(self) -> Behaviors:
        return self._behaviors
    
    @property
    def help(self) -> str:
        """Get help for behaviors"""
        behaviors_list = ", ".join(self.all)
        lines = [
            "**Available Behaviors:**",
            f"  {behaviors_list}",
            "",
            "**Usage:**",
            "  bot.behaviors.current          - access current behavior",
            "  bot.behaviors.navigate_to(name) - navigate to specific behavior",
            "  bot.behaviors.current.help     - get help for current behavior",
        ]
        return "\n".join(lines)
    
    def __iter__(self):
        """Make CLIBehaviors iterable - yields CLIBehavior objects for each behavior"""
        for behavior in self._behaviors._behaviors:
            yield self._get_cli_behavior(behavior.name)

