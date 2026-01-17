
from cli.adapters import MarkdownAdapter
from cli.base_hierarchical_adapter import BaseActionsAdapter

class MarkdownActions(BaseActionsAdapter, MarkdownAdapter):
    
    def __init__(self, actions):
        BaseActionsAdapter.__init__(self, actions, 'markdown')
        self.actions = actions
    
    def serialize(self) -> str:
        return super().serialize()
    
    def parse_command_text(self, text: str) -> tuple[str, str]:
        from utils import parse_command_text
        return parse_command_text(text)
