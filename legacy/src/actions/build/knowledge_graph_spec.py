from pathlib import Path
from typing import Dict, Any, Optional, TYPE_CHECKING
from .knowledge_graph_template import KnowledgeGraphTemplate
from ..validate.story_graph import StoryGraph
from ...utils import read_json_file
if TYPE_CHECKING:
    from ...bot.bot_paths import BotPaths

class KnowledgeGraphSpec:

    def __init__(self, kg_dir: Path, bot_paths: 'BotPaths'):
        self._kg_dir = kg_dir
        self._bot_paths = bot_paths
        self._config_data: Dict[str, Any] = {}
        self._config_path: Optional[Path] = None
        self._template: Optional[KnowledgeGraphTemplate] = None
        self._knowledge_graph: Optional[StoryGraph] = None
        self._load_config()

    def _get_default_config(self) -> dict:
        return {'path': 'docs/stories', 'output': 'story-graph.json', 'template': None}

    def _load_config(self):
        if not self._kg_dir.exists():
            self._config_data = self._get_default_config()
            self._config_path = None
            return
        config_files = list(self._kg_dir.glob('*.json'))
        if not config_files:
            self._config_data = self._get_default_config()
            self._config_path = None
            return
        config_path = config_files[0]
        self._config_data = read_json_file(config_path)
        self._config_path = config_path

    @property
    def knowledge_graph(self) -> StoryGraph:
        if self._knowledge_graph is None:
            working_dir = self._bot_paths.workspace_directory
            self._knowledge_graph = StoryGraph(self._bot_paths, working_dir, require_file=False, knowledge_graph_spec=self)
        return self._knowledge_graph

    @property
    def output_path(self) -> str:
        return self._config_data.get('path', 'docs/stories')

    @property
    def output_filename(self) -> str:
        return self._config_data.get('output', 'story-graph.json')

    @property
    def template_filename(self) -> Optional[str]:
        template_filename = self._config_data.get('template')
        if not template_filename:
            return None
        return template_filename

    @property
    def template(self) -> Optional[KnowledgeGraphTemplate]:
        if self._template is None:
            template_filename = self.template_filename
            if not template_filename:
                return None
            self._template = KnowledgeGraphTemplate(self._kg_dir, template_filename)
        return self._template

    @property
    def config_data(self) -> Dict[str, Any]:
        return self._config_data

    @property
    def config_path(self) -> Optional[Path]:
        return self._config_path