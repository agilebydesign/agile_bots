
from actions.markdown_action import MarkdownAction
from actions.validate.validate_action import ValidateRulesAction

class MarkdownValidateAction(MarkdownAction):
    
    def __init__(self, action: ValidateRulesAction, is_current: bool = False, is_completed: bool = False):
        super().__init__(action, is_current, is_completed)
    
    def serialize(self) -> str:
        return super().serialize()
    
    
    def parse_command_text(self, text: str) -> tuple[str, str]:
        from utils import parse_command_text
        return parse_command_text(text)
