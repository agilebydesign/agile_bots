from pathlib import Path
from typing import Dict, Any, Optional, TYPE_CHECKING
import json
import logging
from bot_path import BotPath
from utils import read_json_file
if TYPE_CHECKING:
    from build.story_graph_spec import StoryGraphSpec
logger = logging.getLogger(__name__)

class StoryGraph:

    def __init__(self, bot_paths: BotPath, workspace_directory: Path, require_file: bool=True, story_graph_spec: Optional['StoryGraphSpec']=None):
        self._bot_paths = bot_paths
        self._workspace_directory = workspace_directory
        self._story_graph_spec = story_graph_spec
        self._require_file = require_file
        self._path = self._determine_story_graph_path()
        self._content = self._load_story_graph_content()

    def _determine_story_graph_path(self):
        if self._story_graph_spec:
            config_data = self._story_graph_spec.config_data
            config_path_value = config_data.get('path', 'docs/stories')
            docs_path = Path(config_path_value.rstrip('/'))
            output_filename = config_data.get('output', 'story-graph.json')
            docs_dir = self._workspace_directory / docs_path
        else:
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
        
        import sys
        import os
        
        # Get file modification time
        file_mtime = os.path.getmtime(self._path)
        print(f"[DEBUG] StoryGraph: story-graph.json mtime={file_mtime}", file=sys.stderr)
        
        # Check when panel last edited the file
        panel_edit_time_file = self._path.parent / '.story-graph-panel-edit-time'
        panel_edit_time = 0
        if panel_edit_time_file.exists():
            try:
                with open(panel_edit_time_file, 'r') as f:
                    panel_edit_time = float(f.read().strip()) / 1000.0  # Convert ms to seconds
                print(f"[DEBUG] StoryGraph: Panel last edited at {panel_edit_time}", file=sys.stderr)
            except Exception as e:
                print(f"[DEBUG] StoryGraph: Failed to read panel edit time: {e}", file=sys.stderr)
        
        raw_content = read_json_file(self._path)
        
        # Only recalculate if file was modified AFTER panel's last edit
        # (meaning someone edited it outside the panel)
        if panel_edit_time > 0 and file_mtime <= panel_edit_time:
            # File last changed by panel or before panel edit - no external changes
            print(f"[DEBUG] StoryGraph: No external edits detected, using existing behaviors", file=sys.stderr)
            return raw_content
        
        # File changed externally (or no panel edit history) - recalculate behaviors
        print(f"[DEBUG] StoryGraph: External edit detected (file mtime {file_mtime} > panel edit {panel_edit_time}), recalculating", file=sys.stderr)
        
        # Use StoryMap to recalculate behaviors
        try:
            from story_graph.nodes import StoryMap
            story_map = StoryMap(raw_content, bot=None, recalculate_behaviors=True)
            # Convert back to dict with recalculated behaviors
            from story_graph.nodes import Epic
            content = {'epics': [story_map._epic_to_dict(epic) for epic in story_map._epics_list]}
            if 'increments' in raw_content:
                content['increments'] = raw_content['increments']
            
            return content
        except Exception as e:
            print(f"[DEBUG] StoryGraph: Failed to recalculate behaviors: {e}, using raw content", file=sys.stderr)
            return raw_content

    @property
    def story_graph_spec(self) -> Optional['StoryGraphSpec']:
        return self._story_graph_spec

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