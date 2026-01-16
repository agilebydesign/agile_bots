from pathlib import Path
from typing import Dict, Any, Optional, TYPE_CHECKING
import json
import logging
from ...bot.bot_paths import BotPaths
from ...utils import read_json_file
if TYPE_CHECKING:
    from ..build.knowledge_graph_spec import KnowledgeGraphSpec
logger = logging.getLogger(__name__)

class StoryGraph:

    def __init__(self, bot_paths: BotPaths, workspace_directory: Path, require_file: bool=True, knowledge_graph_spec: Optional['KnowledgeGraphSpec']=None):
        self._bot_paths = bot_paths
        self._workspace_directory = workspace_directory
        self._knowledge_graph_spec = knowledge_graph_spec
        self._require_file = require_file
        self._path = self._determine_story_graph_path()
        self._content = self._load_story_graph_content()

    def _determine_story_graph_path(self):
        if self._knowledge_graph_spec:
            config_data = self._knowledge_graph_spec.config_data
            config_path_value = config_data.get('path', 'docs/stories')
            docs_path = Path(config_path_value.rstrip('/'))
            output_filename = config_data.get('output', 'story-graph.json')
            docs_dir = self._workspace_directory / docs_path
        else:
            # documentation_path is already relative to workspace, so use it directly
            docs_path = self._bot_paths.documentation_path
            output_filename = 'story-graph.json'
            docs_dir = self._workspace_directory / docs_path
        return docs_dir / output_filename

    def _load_story_graph_content(self):
        if not self._path.exists():
            if self._require_file:
                logger.error(f'Story graph file not found at {self._path}')
                raise FileNotFoundError(f'Story graph file (story-graph.json) not found in {self._path.parent}. Cannot validate rules without story graph. Expected story graph to be created by build action before validate.')
            return {}
        return read_json_file(self._path)

    @property
    def knowledge_graph_spec(self) -> Optional['KnowledgeGraphSpec']:
        return self._knowledge_graph_spec

    @property
    def content(self) -> Dict[str, Any]:
        return self._content

    @property
    def path(self) -> Path:
        return self._path

    @property
    def has_epics(self) -> bool:
        return 'epics' in self._content

    @property
    def has_increments(self) -> bool:
        return 'increments' in self._content

    @property
    def has_domain_concepts(self) -> bool:
        return any(('domain_concepts' in epic for epic in self._content.get('epics', [])))

    @property
    def epic_count(self) -> int:
        return len(self._content.get('epics', []))

    def __getitem__(self, key: str) -> Any:
        return self._content[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._content[key] = value

    def get(self, key: str, default: Any=None) -> Any:
        return self._content.get(key, default)