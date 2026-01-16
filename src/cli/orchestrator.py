from .visitor import Visitor
from .help_context import BehaviorHelpContext, ActionHelpContext

class Orchestrator:
    
    def __init__(self, visitor: Visitor):
        self.visitor = visitor
    
    @property
    def bot(self):
        return self.visitor.bot
    
    @property
    def bot_name(self) -> str:
        return self.visitor.bot_name
    
    @property
    def data_collector(self):
        return self.visitor.data_collector
    
    def generate(self) -> None:
        self.visitor.visit_header(self.bot_name)
        self._visit_behaviors()
        self._visit_action_help_section()
        self.visitor.visit_footer()
    
    def _visit_behaviors(self) -> None:
        if self.data_collector is None:
            return
        behaviors_list = list(self.bot.behaviors)
        sorted_behaviors = self.data_collector.sort_behaviors_for_display(behaviors_list)
        for behavior in sorted_behaviors:
            self._visit_behavior(behavior)
    
    def _visit_behavior(self, behavior) -> None:
        if self.data_collector is None:
            return
        behavior_name = behavior.name
        behavior_description = self.data_collector.get_behavior_description(behavior_name)
        actions = self.data_collector.get_behavior_actions(behavior)
        additional_options = self._get_additional_options(behavior_name)
        context = BehaviorHelpContext(
            bot_name=self.bot_name,
            behavior_name=behavior_name,
            behavior_description=behavior_description,
            actions=actions,
            behavior=behavior,
            additional_options=additional_options
        )
        self.visitor.visit_behavior(context)
    
    def _get_additional_options(self, behavior_name: str):
        if behavior_name == 'code':
            return {
                '--exclude <patterns>': "File patterns to exclude (e.g., '--exclude scanners folder')",
                '--skiprule <rules>': "Rule names to skip (e.g., '--skiprule eliminate_duplication')"
            }
        return None
    
    def _visit_action_help_section(self) -> None:
        if self.data_collector is None:
            return
        self.visitor.visit_action_help_section_header()
        for action_name in self.data_collector.action_order:
            self._visit_action(action_name)
    
    def _visit_action(self, action_name: str) -> None:
        if self.data_collector is None:
            return
        action_description = self.data_collector.get_action_description(action_name)
        parameters = self.data_collector.get_action_parameters(action_name)
        parameter_descriptions = self.data_collector.get_parameter_descriptions(action_name, parameters)
        context = ActionHelpContext(
            bot_name=self.bot_name,
            action_name=action_name,
            action_description=action_description,
            parameters=parameters,
            parameter_descriptions=parameter_descriptions
        )
        self.visitor.visit_action(context)

    def visit_actions_for_behavior(self, behavior_name: str) -> None:
        if self.data_collector is None:
            return
        behavior = self.bot.behaviors.find_by_name(behavior_name)
        if behavior is None:
            return
        action_names = self.data_collector.get_behavior_actions(behavior)
        for action_name in action_names:
            self._visit_action(action_name)
    
    def generate_for_all_actions(self) -> None:
        self.visitor.visit_header(self.bot_name)
        for behavior in self.bot.behaviors:
            for action in behavior.actions:
                self._visit_behavior_action(behavior, action)
        self.visitor.visit_footer()
    
    def _visit_behavior_action(self, behavior, action) -> None:
        context = ActionHelpContext(
            bot_name=self.bot_name,
            action_name=action.action_name,
            action_description="",
            parameters=[],
            parameter_descriptions={},
            behavior_name=behavior.name,
            action=action
        )
        self.visitor.visit_action(context)
