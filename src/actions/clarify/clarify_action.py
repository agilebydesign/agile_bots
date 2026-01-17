from pathlib import Path
from typing import Dict, Any, Type
from actions.action import Action
from actions.action_context import ActionContext, ClarifyActionContext
from actions.clarify.required_context import RequiredContext
from actions.clarify.requirements_clarifications import RequirementsClarifications

class ClarifyContextAction(Action):
    context_class: Type[ActionContext] = ClarifyActionContext

    def __init__(self, behavior=None, action_config=None):
        super().__init__(behavior=behavior, action_config=action_config)
        self._required_context = RequiredContext(self.behavior.folder)

    @property
    def action_name(self) -> str:
        return 'clarify'

    @action_name.setter
    def action_name(self, value: str):
        raise AttributeError('action_name is read-only for ClarifyContextAction')

    @property
    def required_context(self) -> RequiredContext:
        return self._required_context

    @property
    def key_questions(self):
        return self.required_context.key_questions

    @property
    def evidence(self):
        return self.required_context.evidence

    def _prepare_instructions(self, instructions, context: ClarifyActionContext):
        instructions.set('guardrails', {'required_context': self.required_context.instructions})
        
        clarifications = RequirementsClarifications(
            behavior_name=self.behavior.name,
            bot_paths=self.behavior.bot_paths,
            required_context=self.required_context,
            key_questions_answered={},
            evidence_provided={}
        )
        saved_data = clarifications.load()
        if saved_data and self.behavior.name in saved_data:
            instructions.set('clarification', saved_data[self.behavior.name])
    

    def do_execute(self, context: ClarifyActionContext = None):
        if context is None:
            context = ClarifyActionContext()
        result = self.get_instructions(context)
        if context.answers or context.evidence_provided:
            self.save_clarification(context)
        return result

    def save_clarification(self, context: ClarifyActionContext):
        clarifications = RequirementsClarifications(
            behavior_name=self.behavior.name,
            bot_paths=self.behavior.bot_paths,
            required_context=self.required_context,
            key_questions_answered=context.answers or {},
            evidence_provided=context.evidence_provided or {},
            context=context.context
        )
        clarifications.save()