from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class ExecutionContext:
    user_message: str = ''
    chat_history: List[str] = field(default_factory=list)
    file_references: List[str] = field(default_factory=list)
    
    @classmethod
    def loads_from_context_file(cls, path: Path) -> 'ExecutionContext':
        if not path.exists():
            return cls()
        
        content = path.read_text()
        return cls._parses_content(content)
    
    @classmethod
    def _parses_content(cls, content: str) -> 'ExecutionContext':
        sections = _ContextSections()
        
        for line in content.split('\n'):
            sections.processes_line(line.strip())
        
        return cls(
            user_message=sections.user_message,
            chat_history=sections.chat_history,
            file_references=sections.file_references
        )


class _ContextSections:
    
    def __init__(self):
        self.user_message = ''
        self.chat_history = []
        self.file_references = []
        self._current_section = None
    
    def processes_line(self, line: str) -> None:
        if line.startswith('User Intent:'):
            self._current_section = 'user_message'
            self.user_message = line.replace('User Intent:', '').strip()
        elif line.startswith('Chat History:'):
            self._current_section = 'chat_history'
        elif line.startswith('File References:'):
            self._current_section = 'file_references'
        elif line.startswith('-'):
            self._appends_list_item(line[1:].strip())
    
    def _appends_list_item(self, item: str) -> None:
        if self._current_section == 'chat_history':
            self.chat_history.append(item)
        elif self._current_section == 'file_references':
            self.file_references.append(item)
