from pathlib import Path
from typing import Dict, Any, Type
from ..action import Action
from ..action_context import ActionContext, ClarifyActionContext
from .required_context import RequiredContext
from .requirements_clarifications import RequirementsClarifications

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
        """Load required questions and evidence into instructions."""
        instructions.set('guardrails', {'required_context': self.required_context.instructions})
    
    def _do_confirm(self, context: ClarifyActionContext) -> Dict[str, Any]:
        """Save clarification answers to clarification.json."""
        if context.answers or context.evidence_provided or context.context:
            clarifications = RequirementsClarifications(
                behavior_name=self.behavior.name,
                bot_paths=self.behavior.bot_paths,
                required_context=self.required_context,
                key_questions_answered=context.answers or {},
                evidence_provided=context.evidence_provided or {},
                context=context.context
            )
            clarifications.save()
            
            # Get the file path where it was saved
            saved_path = clarifications.file_path
            
            # Count what was saved
            questions_count = len(context.answers or {})
            evidence_count = len(context.evidence_provided or {})
            has_context = bool(context.context)
            
            # Build detailed message
            message_parts = []
            if questions_count > 0:
                message_parts.append(f"{questions_count} question(s) and answer(s)")
            if evidence_count > 0:
                message_parts.append(f"{evidence_count} evidence item(s)")
            if has_context:
                if isinstance(context.context, list):
                    message_parts.append(f"{len(context.context)} context item(s)")
                else:
                    message_parts.append("context")
            
            saved_items = " and ".join(message_parts) if message_parts else "data"
            
            return {
                'message': f'Clarification saved: {saved_items} saved to {saved_path}',
                'saved_path': str(saved_path),
                'questions_answered': questions_count,
                'evidence_count': evidence_count,
                'has_context': has_context,
                'answers': context.answers or {},
                'evidence_provided': context.evidence_provided or {},
                'context': context.context
            }
        
        return {'message': 'No clarification data to save'}

    def do_execute(self, context: ClarifyActionContext) -> Dict[str, Any]:
        """Legacy execute - calls get_instructions then confirm."""
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