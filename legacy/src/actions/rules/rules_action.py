from typing import Dict, Any, Type
from ..action import Action
from ..action_context import ActionContext, RulesActionContext
from .rules import Rules
from .rules_digest_guidance import RulesDigestGuidance


class RulesAction(Action):
    context_class: Type[ActionContext] = RulesActionContext

    def do_execute(self, context: RulesActionContext) -> Dict[str, Any]:
        instructions = self.instructions.copy()
        rules = Rules(behavior=self.behavior, bot_paths=self.behavior.bot_paths)
        rules_digest = rules.formatted_rules_digest()
        rule_names = self._get_rule_names(rules)
        
        self._add_rules_list_to_display(instructions, rule_names)
        self._add_user_message(instructions, context.message)
        self._add_rules_context(instructions, rules_digest, rule_names)
        
        return {'instructions': instructions.to_dict()}
    
    def _get_rule_names(self, rules: Rules) -> list:
        return [rule.name for rule in rules]
    
    def _add_rules_list_to_display(self, instructions, rule_names: list) -> None:
        instructions.add_display("")
        instructions.add_display(f"## Rules Available ({len(rule_names)} total)")
        instructions.add_display("")
        for idx, rule_name in enumerate(rule_names, 1):
            instructions.add_display(f"{idx}. {rule_name}")
        instructions.add_display("")
    
    def _add_user_message(self, instructions, message: str) -> None:
        if not message:
            return
        instructions.add("")
        instructions.add("**User Request:**")
        instructions.add(message)
        instructions.add("")
    
    def _add_rules_context(self, instructions, rules_digest: str, rule_names: list) -> None:
        instructions.add("")
        instructions.add(rules_digest)
        instructions.add("")
        RulesDigestGuidance().add_to(instructions)


