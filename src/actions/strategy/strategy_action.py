from pathlib import Path
from typing import Dict, Any, Type
from ..action import Action
from ..action_context import ActionContext, StrategyActionContext
from .strategy import Strategy
from .strategy_decision import StrategyDecision

class StrategyAction(Action):
    context_class: Type[ActionContext] = StrategyActionContext

    def __init__(self, behavior=None, action_config=None):
        super().__init__(behavior=behavior, action_config=action_config)
        self._strategy = Strategy(self.behavior.folder)

    @property
    def action_name(self) -> str:
        return 'strategy'

    @action_name.setter
    def action_name(self, value: str):
        raise AttributeError('action_name is read-only for StrategyAction')

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @property
    def strategy_criteria(self):
        return self.strategy.strategy_criterias.strategy_criterias

    @property
    def typical_assumptions(self):
        return self.strategy.assumptions.assumptions
    
    def _prepare_instructions(self, instructions, context: StrategyActionContext):
        strategy_data = self.strategy.instructions
        
        saved_data = StrategyDecision.load_all(self.behavior.bot_paths)
        saved_behavior_data = saved_data.get(self.behavior.name, {}) if saved_data else {}
        
        combined_strategy_criteria = {}
        combined_assumptions = {}
        
        if strategy_data:
            criteria_template = strategy_data.get('strategy_criteria', {})
            combined_strategy_criteria['criteria'] = criteria_template
            
            assumptions_template = strategy_data.get('assumptions', {})
            if isinstance(assumptions_template, dict):
                if 'typical_assumptions' in assumptions_template:
                    combined_assumptions['typical_assumptions'] = assumptions_template.get('typical_assumptions', [])
                else:
                    combined_assumptions['typical_assumptions'] = assumptions_template
            elif isinstance(assumptions_template, list):
                combined_assumptions['typical_assumptions'] = assumptions_template
        
        saved_decisions = saved_behavior_data.get('decisions', {})
        if saved_decisions:
            combined_strategy_criteria['decisions_made'] = saved_decisions
        
        saved_assumptions = saved_behavior_data.get('assumptions', [])
        if saved_assumptions:
            combined_assumptions['assumptions_made'] = saved_assumptions
        
        if combined_strategy_criteria:
            instructions.set('strategy_criteria', combined_strategy_criteria)
        if combined_assumptions:
            instructions.set('assumptions', combined_assumptions)
    
        try:
            from ..clarify.requirements_clarifications import RequirementsClarifications
            from ..clarify.required_context import RequiredContext
            
            required_context = RequiredContext(self.behavior.folder)
            clarifications = RequirementsClarifications(
                behavior_name=self.behavior.name,
                bot_paths=self.behavior.bot_paths,
                required_context=required_context,
                key_questions_answered={},
                evidence_provided={}
            )
            saved_clarifications = clarifications.load()
            if saved_clarifications and self.behavior.name in saved_clarifications:
                instructions.set('clarification', saved_clarifications[self.behavior.name])
        except Exception:
            pass
    
    def _format_instructions_for_display(self, instructions) -> str:
        output_lines = super()._format_instructions_for_display(instructions).split('\n')
        
        instructions_dict = instructions.to_dict()
        
        strategy_criteria = instructions_dict.get('strategy_criteria', {})
        if strategy_criteria:
            output_lines.append("")
            output_lines.append("**Decisions:**")
            
            criteria_template = strategy_criteria.get('criteria', {})
            if criteria_template:
                for criteria_key, criteria_data in criteria_template.items():
                    output_lines.append("")
                    question = criteria_data.get('question', '')
                    if question:
                        output_lines.append(f"**{criteria_key}:** {question}")
                    else:
                        output_lines.append(f"**{criteria_key}:**")
                    options = criteria_data.get('options', [])
                    if options:
                        for option in options:
                            output_lines.extend(self._format_option(option))
            
            saved_decisions = strategy_criteria.get('decisions', {})
            if saved_decisions:
                output_lines.append("")
                output_lines.append("**Your Decisions:**")
                for decision_key, decision_value in saved_decisions.items():
                    output_lines.append("")
                    output_lines.append(f"**{decision_key}:**")
                    if isinstance(decision_value, list):
                        for item in decision_value:
                            output_lines.append(f"  - {item}")
                    else:
                        output_lines.append(f"  {decision_value}")
        
        assumptions = instructions_dict.get('assumptions', {})
        if assumptions:
            output_lines.append("")
            output_lines.append("**Assumptions:**")
            
            typical_assumptions = assumptions.get('typical_assumptions', [])
            if typical_assumptions:
                for assumption in typical_assumptions:
                    output_lines.append(f"- {assumption}")
            
            saved_assumptions = assumptions.get('assumptions', [])
            if saved_assumptions:
                output_lines.append("")
                output_lines.append("**Your Assumptions:**")
                for assumption in saved_assumptions:
                    output_lines.append(f"- {assumption}")
        
        return "\n".join(output_lines)

    def _format_option(self, option) -> list:
        lines = []
        if isinstance(option, dict):
            name = option.get('name', option.get('id', 'Unknown'))
            description = option.get('description', '')
            when_to_use = option.get('when_to_use', '')
            example = option.get('example', '')
            
            lines.append(f"  [{name}]")
            if description:
                lines.append(f"    {description}")
            if when_to_use:
                lines.append(f"    When: {when_to_use}")
            if example:
                lines.append(f"    Example:")
                for example_line in example.split('\n'):
                    lines.append(f"      {example_line}")
        else:
            lines.append(f"  - {option}")
        return lines

    def do_execute(self, context: StrategyActionContext = None):
        if context is None:
            context = StrategyActionContext()
        result = self.get_instructions(context)
        decisions = context.get_decisions()
        if decisions or context.assumptions:
            self.save_strategy(context)
        return result

    def save_strategy(self, context: StrategyActionContext):
        strategy_decision = StrategyDecision(
            behavior_name=self.behavior.name,
            bot_paths=self.behavior.bot_paths,
            strategy=self.strategy,
            decisions_made=context.get_decisions(),
            assumptions_made=context.assumptions or []
        )
        strategy_decision.save()