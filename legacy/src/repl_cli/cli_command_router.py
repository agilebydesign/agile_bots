from typing import Dict, Any, List, TYPE_CHECKING
from ..bot.bot import BotResult
from ..actions.action_context import ActionContext
from .cli_context_builder import CliContextBuilder

if TYPE_CHECKING:
    from ..bot.behavior import Behavior
    from ..actions.action import Action

class CliCommandRouter:

    def __init__(self, bot):
        self.bot = bot
        self._context_builder = CliContextBuilder()

    def route_to_action(self, behavior_name: str, action_name: str, cli_args: List[str]):
        if action_name:
            if not behavior_name:
                return {'status': 'error', 'behavior': None, 'action': action_name, 'data': {'error': 'Behavior name is required when action name is provided'}}
            behavior_obj = self.bot.behaviors.find_by_name(behavior_name)
            if behavior_obj is None:
                return {'status': 'error', 'behavior': behavior_name, 'action': action_name, 'data': {'error': f"Behavior '{behavior_name}' not found"}}
            action_obj = behavior_obj.actions.find_by_name(action_name)
            if action_obj is None:
                return {'status': 'error', 'behavior': behavior_name, 'action': action_name, 'data': {'error': f"Action '{action_name}' not found in behavior '{behavior_name}'"}}
            return self._route_to_specific_action(behavior_obj, action_obj, cli_args)
        return self._route_to_behavior(behavior_name)
        # Note: _route_to_current_behavior_and_action not reached from here

    def _route_to_specific_action(self, behavior: 'Behavior', action: 'Action', cli_args: List[str]):
        behavior.actions.navigate_to(action.action_name)
        
        context = self._context_builder.build_context(action, cli_args)
        
        result_data = action.execute(context)
        result = BotResult('completed', behavior.name, action.action_name, result_data)
        return self._format_result(result)

    def _route_to_behavior(self, behavior_name: str):
        behavior_obj = self.bot.behaviors.find_by_name(behavior_name)
        if behavior_obj is None:
            return {'status': 'error', 'behavior': behavior_name, 'action': None, 'data': {'error': f"Behavior '{behavior_name}' not found"}}
        return self._execute_current_action(behavior_obj)

    def _route_to_current_behavior_and_action(self):
        current_behavior = self._navigate_to_first_behavior_if_needed()
        return self._execute_current_action(current_behavior)

    def _navigate_to_first_behavior_if_needed(self):
        current_behavior = self.bot.behaviors.current
        if current_behavior is None and self.bot.behaviors.first:
            self.bot.behaviors.navigate_to(self.bot.behaviors.first.name)
            current_behavior = self.bot.behaviors.current
        return current_behavior

    def _execute_current_action(self, behavior):
        if behavior is None:
            return {'status': 'error', 'behavior': None, 'action': None, 'data': {'error': 'No behavior provided'}}
        action = behavior.actions.forward_to_current()
        if action is None:
            return {'status': 'error', 'behavior': behavior.name, 'action': None, 'data': {'error': f"No current action found in behavior '{behavior.name}'"}}
        result_data = action.execute()
        result = BotResult('completed', behavior.name, action.action_name, result_data)
        return self._format_result(result)

    def _format_result(self, result) -> Dict[str, Any]:
        status = 'success' if result.status == 'completed' else result.status
        return {'status': status, 'behavior': result.behavior, 'action': result.action, 'data': result.data}
