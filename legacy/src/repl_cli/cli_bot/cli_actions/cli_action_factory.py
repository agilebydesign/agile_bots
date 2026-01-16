from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agile_bot.bots.base_bot.src.actions.action import Action
    from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
    from agile_bot.bots.base_bot.src.repl_cli.cli_bot.cli_actions.cli_action import CLIAction


class CLIActionFactory:
    
    @staticmethod
    def create_cli_action(action: Action, session: REPLSession) -> CLIAction:
        action_name = action.action_name
        
        if action_name == 'build':
            from agile_bot.bots.base_bot.src.repl_cli.cli_bot.cli_actions.build_cli_action import BuildCLIAction
            return BuildCLIAction(action, session)
        elif action_name == 'validate':
            from agile_bot.bots.base_bot.src.repl_cli.cli_bot.cli_actions.validate_cli_action import ValidateCLIAction
            return ValidateCLIAction(action, session)
        elif action_name == 'render':
            from agile_bot.bots.base_bot.src.repl_cli.cli_bot.cli_actions.render_cli_action import RenderCLIAction
            return RenderCLIAction(action, session)
        elif action_name == 'clarify':
            from agile_bot.bots.base_bot.src.repl_cli.cli_bot.cli_actions.clarify_cli_action import ClarifyCLIAction
            return ClarifyCLIAction(action, session)
        elif action_name == 'strategy':
            from agile_bot.bots.base_bot.src.repl_cli.cli_bot.cli_actions.strategy_cli_action import StrategyCLIAction
            return StrategyCLIAction(action, session)
        else:
            from agile_bot.bots.base_bot.src.repl_cli.cli_bot.cli_actions.cli_action import CLIAction
            return CLIAction(action, session)

