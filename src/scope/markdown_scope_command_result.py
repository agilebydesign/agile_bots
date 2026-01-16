
from agile_bot.src.cli.adapters import MarkdownAdapter
from agile_bot.src.scope.scope_command_result import ScopeCommandResult

class MarkdownScopeCommandResult(MarkdownAdapter):
    
    def __init__(self, scope_result: ScopeCommandResult):
        self.scope_result = scope_result
    
    def serialize(self) -> str:
        from agile_bot.src.scope.markdown_scope import MarkdownScope
        
        scope_adapter = MarkdownScope(self.scope_result.scope)
        scope_markdown = scope_adapter.serialize()
        
        return scope_markdown
    
    def parse_command_text(self, text: str) -> tuple[str, str]:
        from agile_bot.src.utils import parse_command_text
        return parse_command_text(text)