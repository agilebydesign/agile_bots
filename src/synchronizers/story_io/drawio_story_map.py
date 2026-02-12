import json
from pathlib import Path
from typing import List, Optional, Dict, Any, TYPE_CHECKING
from story_graph.nodes import StoryMap, Epic, SubEpic, Story, StoryGroup
from .story_io_position import Position, Boundary
from .drawio_element import DrawIOElement
from .drawio_story_node import DrawIOStoryNode, DrawIOEpic, DrawIOSubEpic, DrawIOStory
from .drawio_story_node_serializer import DrawIOStoryNodeSerializer
from .layout_data import LayoutData
from .update_report import UpdateReport


EPIC_Y = 120
EPIC_X_START = 20
SUB_EPIC_Y_OFFSET = 60
STORY_Y_OFFSET = 90
STORY_WIDTH = 120
STORY_HEIGHT = 50
STORY_SPACING = 10
CONTAINER_PADDING = 10
ACTOR_Y_OFFSET = -60
ACTOR_WIDTH = 40
ACTOR_HEIGHT = 20


class DrawIOStoryMap(StoryMap):

    def __init__(self, diagram_type: str = 'outline', story_graph: Dict[str, Any] = None):
        super().__init__(story_graph or {'epics': []})
        self._diagram_type = diagram_type
        self._drawio_epics: List[DrawIOEpic] = []
        self._all_nodes: List = []
        self._layout_data: Optional[LayoutData] = None

    @property
    def diagram_type(self) -> str:
        return self._diagram_type

    def get_epics(self) -> List[DrawIOEpic]:
        return list(self._drawio_epics)

    def get_sub_epics(self) -> List[DrawIOSubEpic]:
        result = []
        for epic in self._drawio_epics:
            result.extend(epic.get_sub_epics())
        return result

    def get_stories(self) -> List[DrawIOStory]:
        result = []
        for epic in self._drawio_epics:
            result.extend(epic.get_stories())
        return result

    def render_from_story_map(self, story_map: StoryMap,
                               layout_data: Optional[LayoutData] = None) -> Dict[str, Any]:
        self._layout_data = layout_data
        self._drawio_epics = []
        self._all_nodes = []

        epics = list(story_map.epics)
        if not epics:
            return {'epics': 0, 'sub_epic_count': 0, 'diagram_generated': True}

        x_pos = EPIC_X_START
        for epic in epics:
            drawio_epic = DrawIOStoryNodeSerializer.create_epic(
                epic.name, getattr(epic, 'sequential_order', 0) or 0)
            epic_width = self._render_epic(drawio_epic, epic, x_pos)
            x_pos += epic_width + STORY_SPACING
            self._drawio_epics.append(drawio_epic)
            self._all_nodes.append(drawio_epic)

        return {
            'epics': len(self._drawio_epics),
            'sub_epic_count': len(self.get_sub_epics()),
            'diagram_generated': True
        }

    def _render_epic(self, drawio_epic: DrawIOEpic, epic: Epic, x_pos: float) -> float:
        saved_pos = self._saved_position_for(f'EPIC|{drawio_epic.name}')
        drawio_epic.set_position(saved_pos.x if saved_pos else x_pos,
                                  saved_pos.y if saved_pos else EPIC_Y)

        sub_epic_x = drawio_epic.position.x + CONTAINER_PADDING
        sub_epic_y = drawio_epic.position.y + SUB_EPIC_Y_OFFSET

        for sub_epic in epic.sub_epics:
            drawio_se = DrawIOStoryNodeSerializer.create_sub_epic(
                sub_epic.name, getattr(sub_epic, 'sequential_order', 0) or 0)
            se_width = self._render_sub_epic(drawio_se, sub_epic, sub_epic_x, sub_epic_y)
            drawio_epic.add_child(drawio_se)
            self._all_nodes.append(drawio_se)
            sub_epic_x += se_width + STORY_SPACING

        drawio_epic.compute_container_dimensions_from_children()
        return drawio_epic.boundary.width

    def _render_sub_epic(self, drawio_se: DrawIOSubEpic, sub_epic,
                          x_pos: float, y_pos: float) -> float:
        saved_pos = self._saved_position_for(f'SUB_EPIC|{drawio_se.name}')
        drawio_se.set_position(saved_pos.x if saved_pos else x_pos,
                                saved_pos.y if saved_pos else y_pos)

        stories = self._collect_stories(sub_epic)
        stories.sort(key=lambda s: getattr(s, 'sequential_order', 0) or 0)

        story_x = drawio_se.position.x + CONTAINER_PADDING / 2
        story_y = drawio_se.position.y + STORY_Y_OFFSET

        for story in stories:
            story_type = getattr(story, 'story_type', 'user') or 'user'
            drawio_story = DrawIOStoryNodeSerializer.create_story(
                story.name, getattr(story, 'sequential_order', 0) or 0, story_type)
            drawio_story.set_position(story_x, story_y)
            drawio_story.set_size(STORY_WIDTH, STORY_HEIGHT)
            drawio_se.add_child(drawio_story)
            self._all_nodes.append(drawio_story)

            users = getattr(story, 'users', []) or []
            for user in users:
                user_name = user.name if hasattr(user, 'name') else str(user)
                actor = DrawIOStoryNodeSerializer.create_actor(user_name)
                actor.set_position(story_x + STORY_WIDTH / 2 - ACTOR_WIDTH / 2,
                                   story_y + ACTOR_Y_OFFSET)
                actor.set_size(ACTOR_WIDTH, ACTOR_HEIGHT)
                self._all_nodes.append(actor)

            story_x += STORY_WIDTH + STORY_SPACING

        drawio_se.compute_container_dimensions_from_children()
        return drawio_se.boundary.width

    def _collect_stories(self, sub_epic) -> list:
        return [c for c in sub_epic.children if isinstance(c, Story)]

    def _saved_position_for(self, key: str) -> Optional[Position]:
        if self._layout_data:
            return self._layout_data.position_for(key)
        return None

    def save(self, file_path: Path):
        xml_content = DrawIOStoryNodeSerializer.to_drawio_xml(self._all_nodes)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(xml_content, encoding='utf-8')

    def save_as_json(self, file_path: Path):
        data = self._to_story_graph_dict()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(data, indent=2), encoding='utf-8')

    def extract_layout(self) -> LayoutData:
        layout = LayoutData()
        for epic in self._drawio_epics:
            layout.set_entry(f'EPIC|{epic.name}',
                             epic.position.x, epic.position.y,
                             epic.boundary.width, epic.boundary.height)
            for se in epic.get_sub_epics():
                layout.set_entry(f'SUB_EPIC|{se.name}',
                                 se.position.x, se.position.y,
                                 se.boundary.width, se.boundary.height)
                for story in se.get_stories():
                    layout.set_entry(
                        f'STORY|{epic.name}|{se.name}|{story.name}',
                        story.position.x, story.position.y,
                        story.boundary.width, story.boundary.height)
        return layout

    def generate_update_report(self, original_story_map: StoryMap) -> UpdateReport:
        report = UpdateReport()
        orig_epics = list(original_story_map.epics)
        matched_originals = set()

        for ext_epic in self._drawio_epics:
            for idx, orig_epic in enumerate(orig_epics):
                if idx in matched_originals:
                    continue
                if ext_epic.name.lower() == orig_epic.name.lower():
                    matched_originals.add(idx)
                    ext_epic.generate_update_report_for_epic_subtree(orig_epic, report)
                    break

        for idx, orig_epic in enumerate(orig_epics):
            if idx not in matched_originals:
                report.add_missing_epic(orig_epic.name)

        return report

    def _to_story_graph_dict(self) -> Dict[str, Any]:
        epics = []
        for epic in self._drawio_epics:
            epic_dict = {
                'name': epic.name,
                'sequential_order': epic.sequential_order,
                'sub_epics': []
            }
            for se in epic.get_sub_epics():
                se_dict = {
                    'name': se.name,
                    'sequential_order': se.sequential_order,
                    'sub_epics': [],
                    'story_groups': [{
                        'type': 'and', 'connector': None,
                        'stories': [
                            {'name': s.name, 'sequential_order': s.sequential_order,
                             'story_type': s.story_type or 'user'}
                            for s in se.get_stories()
                        ]
                    }]
                }
                epic_dict['sub_epics'].append(se_dict)
            epics.append(epic_dict)
        return {'epics': epics}

    @classmethod
    def load(cls, file_path: Path) -> 'DrawIOStoryMap':
        content = file_path.read_text(encoding='utf-8')
        nodes = DrawIOStoryNodeSerializer.parse_nodes_from_xml(content)
        story_map = cls()
        epics = [n for n in nodes if isinstance(n, DrawIOEpic)]
        sub_epics = [n for n in nodes if isinstance(n, DrawIOSubEpic)]
        stories = [n for n in nodes if isinstance(n, DrawIOStory)]
        story_map._assign_stories_to_sub_epics_by_containment(sub_epics, stories)
        story_map._assign_sub_epics_to_epics_by_containment(epics, sub_epics)
        story_map._assign_sequential_order_from_position(epics, sub_epics, stories)
        story_map._drawio_epics = epics
        story_map._all_nodes = nodes
        return story_map

    def _assign_stories_to_sub_epics_by_containment(self, sub_epics, stories):
        for story in stories:
            story_center = story.boundary.center
            for se in sub_epics:
                if se.boundary.contains_position(story_center):
                    se.add_child(story)
                    break

    def _assign_sub_epics_to_epics_by_containment(self, epics, sub_epics):
        for se in sub_epics:
            se_center = se.boundary.center
            for epic in epics:
                if epic.boundary.contains_position(se_center):
                    epic.add_child(se)
                    break

    def _assign_sequential_order_from_position(self, epics, sub_epics, stories):
        for group in [epics, sub_epics, stories]:
            sorted_nodes = sorted(group, key=lambda n: (n.position.y, n.position.x))
            for idx, node in enumerate(sorted_nodes):
                node.sequential_order = float(idx + 1)
