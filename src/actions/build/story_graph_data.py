from pathlib import Path
from typing import Dict, Any, TYPE_CHECKING
from actions.build.story_graph_spec import StoryGraphSpec
if TYPE_CHECKING:
    from bot_path import BotPath
    from bot.behavior import Behavior

class StoryGraphData:

    def __init__(self, behavior: 'Behavior'):
        self._behavior = behavior
        sg_dir = behavior.folder / 'content' / 'story_graph'
        self._sg_dir = sg_dir
        self.story_graph_spec = StoryGraphSpec(self._sg_dir, behavior.bot_paths)
        self.story_graph_template = self.story_graph_spec.template

    @property
    def instructions(self) -> Dict[str, Any]:
        config_path = str(self.story_graph_spec.config_path) if self.story_graph_spec.config_path else None
        result = {'config_path': config_path}
        if self.story_graph_template:
            result['template_path'] = str(self.story_graph_template.template_path)
        else:
            result['template_path'] = None
        return result