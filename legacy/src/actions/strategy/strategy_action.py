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
        """Add strategy data (criteria, assumptions, activities) to instructions."""
        instructions.update(self.strategy.instructions)
    
    def _do_confirm(self, context: StrategyActionContext) -> Dict[str, Any]:
        """Save strategy decisions and assumptions to strategy.json."""
        decisions = context.get_decisions()
        if decisions or context.assumptions:
            self.save_strategy(context)
            
            # Count what was saved
            decisions_count = len(decisions)
            assumptions_count = len(context.assumptions or [])
            
            # Build detailed message
            message_parts = []
            if decisions_count > 0:
                message_parts.append(f"{decisions_count} decision(s)")
            if assumptions_count > 0:
                message_parts.append(f"{assumptions_count} assumption(s)")
            
            saved_items = " and ".join(message_parts) if message_parts else "data"
            
            # Get file path
            saved_path = self.behavior.bot_paths.workspace_directory / 'docs' / 'stories' / 'strategy.json'
            
            return {
                'message': f'Strategy saved: {saved_items} saved to {saved_path}',
                'saved_path': str(saved_path),
                'choices': decisions,
                'assumptions': context.assumptions or []
            }
        
        return {'message': 'No strategy data to save'}
    
    def _format_instructions_for_display(self, instructions) -> str:
        """Format strategy data for REPL display."""
        # Get base formatting first (includes scope warning if set)
        output_lines = super()._format_instructions_for_display(instructions).split('\n')
        
        # Get the instruction data
        instructions_dict = instructions.to_dict()
        
        # Format strategy criteria
        strategy_criteria = instructions_dict.get('strategy_criteria', {})
        if strategy_criteria:
            output_lines.append("")
            output_lines.append("**Decisions:**")
            for criteria_key, criteria_data in strategy_criteria.items():
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
        
        # Format assumptions
        assumptions = instructions_dict.get('assumptions', [])
        if assumptions:
            output_lines.append("")
            output_lines.append("**Assumptions:**")
            for assumption in assumptions:
                output_lines.append(f"- {assumption}")
        
        return "\n".join(output_lines)

    def _format_option(self, option) -> list:
        """Format a single decision criteria option for display."""
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

    def do_execute(self, context: StrategyActionContext) -> Dict[str, Any]:
        instructions = self.instructions.copy()
        instructions.update(self.strategy.instructions)
        decisions = context.get_decisions()
        if decisions or context.assumptions:
            self.save_strategy(context)
        return {'instructions': instructions.to_dict()}

    def save_strategy(self, context: StrategyActionContext):
        strategy_decision = StrategyDecision(
            behavior_name=self.behavior.name,
            bot_paths=self.behavior.bot_paths,
            strategy=self.strategy,
            decisions_made=context.get_decisions(),
            assumptions_made=context.assumptions or []
        )
        strategy_decision.save()