from pathlib import Path
from typing import Dict, Any, TYPE_CHECKING
from .knowledge_graph_spec import KnowledgeGraphSpec
if TYPE_CHECKING:
    from ...bot.bot_paths import BotPaths
    from ...bot.behavior import Behavior

class Knowledge:

    def __init__(self, behavior: 'Behavior'):
        self._behavior = behavior
        kg_dir = behavior.folder / 'content' / 'knowledge_graph'
        self._kg_dir = kg_dir
        self.knowledge_graph_spec = KnowledgeGraphSpec(self._kg_dir, behavior.bot_paths)
        self.knowledge_graph_template = self.knowledge_graph_spec.template

    @property
    def instructions(self) -> Dict[str, Any]:
        # Return only file path references, not full content
        config_path = str(self.knowledge_graph_spec.config_path) if self.knowledge_graph_spec.config_path else None
        result = {'config_path': config_path}
        if self.knowledge_graph_template:
            result['template_path'] = str(self.knowledge_graph_template.template_path)
        else:
            result['template_path'] = None
        return result