import logging
from pathlib import Path
from typing import Dict, Any, List, Callable, TYPE_CHECKING
from ..actions.clarify.requirements_clarifications import RequirementsClarifications
from ..actions.strategy.strategy_decision import StrategyDecision
if TYPE_CHECKING:
    from ..bot.behavior import Behavior
logger = logging.getLogger(__name__)

class ContextDataInjector:

    def __init__(self, behavior: 'Behavior'):
        self.behavior = behavior

    def _inject_data(self, instructions: Dict[str, Any], loader: Callable, key: str, messages: List[str]) -> list:
        bot_paths = self.behavior.bot_paths
        data = loader(bot_paths)
        if not data:
            return []
        instructions[key] = data
        return messages

    def inject_clarification_data(self, instructions: Dict[str, Any]) -> list:
        return self._inject_data(
            instructions,
            RequirementsClarifications.load_all,
            'clarification',
            []
        )

    def inject_strategy_data(self, instructions: Dict[str, Any]) -> list:
        return []

    def inject_context_files(self, instructions: Dict[str, Any]) -> list:
        bot_paths = self.behavior.bot_paths
        workspace_directory = bot_paths.workspace_directory
        docs_path = bot_paths.documentation_path
        context_dir = workspace_directory / docs_path / 'context'
        
        if not context_dir.exists():
            return []
        
        context_files = []
        for file_path in context_dir.iterdir():
            if file_path.is_file():
                context_files.append(file_path.name)
        
        if context_files:
            instructions['context_files'] = context_files
        return []