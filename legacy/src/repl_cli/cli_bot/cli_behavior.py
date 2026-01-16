from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agile_bot.bots.base_bot.src.bot.behavior import Behavior
    from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
    from agile_bot.bots.base_bot.src.repl_cli.cli_bot.cli_actions.cli_actions import CLIActions


class CLIBehavior:
    
    def __init__(self, behavior: Behavior, session: REPLSession):
        self._behavior = behavior
        self._session = session
        self._cli_actions = None
    
    @property
    def name(self) -> str:
        return self._behavior.name
    
    @property
    def description(self) -> str:
        return self._behavior.description
    
    @property
    def is_completed(self) -> bool:
        return self._behavior.is_completed
    
    @property
    def status(self) -> str:
        if self._behavior.is_completed:
            return "completed"
        return "in_progress"
    
    @property
    def actions(self) -> CLIActions:
        if self._cli_actions is None:
            from agile_bot.bots.base_bot.src.repl_cli.cli_bot.cli_actions.cli_actions import CLIActions
            self._cli_actions = CLIActions(self._behavior.actions, self._session)
        return self._cli_actions
    
    @property
    def domain_behavior(self) -> Behavior:
        return self._behavior
    
    @property
    def help(self) -> str:
        """Get help for this specific behavior"""
        from agile_bot.bots.base_bot.src.repl_cli.repl_help import BehaviorHelp
        behavior_help = BehaviorHelp(self._behavior)
        return behavior_help.actions_list

