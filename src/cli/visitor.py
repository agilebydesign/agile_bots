from abc import ABC, abstractmethod
from typing import Optional
from .help_context import BehaviorHelpContext, ActionHelpContext

class Visitor(ABC):
    
    def __init__(self, bot=None):
        self._bot = bot
    
    @property
    def bot(self):
        return self._bot
    
    @property
    def bot_name(self) -> Optional[str]:
        return self._bot.bot_name if self._bot else None
    
    @property
    def bot_directory(self):
        return self._bot.bot_paths.bot_directory if self._bot else None
    
    @property
    def data_collector(self):
        return None
    
    @abstractmethod
    def visit_header(self, bot_name: str) -> None:
        pass
    
    @abstractmethod
    def visit_behavior(self, context: BehaviorHelpContext) -> None:
        pass
    
    @abstractmethod
    def visit_action(self, context: ActionHelpContext) -> None:
        pass
    
    @abstractmethod
    def visit_action_help_section_header(self) -> None:
        pass
    
    def visit_footer(self) -> None:
        pass
