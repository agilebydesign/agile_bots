"""
DrawIOStoryMap - Domain model for rendering story maps to DrawIO.

Orchestrates rendering by delegating to domain nodes. Each node
(DrawIOEpic, DrawIOSubEpic, DrawIOStory, DrawIOIncrementLane) owns
its own rendering logic.  This class only coordinates creation order
and collects nodes for serialization.
"""
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from story_graph.nodes import StoryMap, Epic, SubEpic, Story, StoryGroup
from .drawio_story_node import (
    DrawIOStoryNode, DrawIOEpic, DrawIOSubEpic, DrawIOStory,
    DrawIOIncrementLane, SPACING, CONTAINER_PADDING,
    _max_sub_epic_depth, _RowPositions, CELL_SPACING,
)
from .drawio_story_node_serializer import DrawIOStoryNodeSerializer
from .layout_data import LayoutData
from .update_report import UpdateReport


class DrawIOStoryMap(StoryMap):

    def __init__(self, diagram_type: str = 'outline', story_graph: Dict[str, Any] = None):
        super().__init__(story_graph or {'epics': []})
        self._diagram_type = diagram_type
        self._drawio_epics: List[DrawIOEpic] = []
        self._extra_nodes: List = []          # increment lanes, AC boxes, etc.
        self._layout_data: Optional[LayoutData] = None

    @property
    def diagram_type(self) -> str:
        return self._diagram_type

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

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

    def get_total_width(self) -> float:
        """Rightmost edge of the rendered outline content."""
        if not self._drawio_epics:
            return 0
        return max(e.boundary.right for e in self._drawio_epics)

    def get_bottom_y(self) -> float:
        """Lowest Y coordinate of any outline element (sub-epics or stories)."""
        bottom = 0
        for story in self.get_stories():
            b = story.position.y + story.boundary.height
            if b > bottom:
                bottom = b
        for se in self.get_sub_epics():
            b = se.position.y + se.boundary.height
            if b > bottom:
                bottom = b
        return bottom

    # ------------------------------------------------------------------
    # Render – Outline
    # ------------------------------------------------------------------

    def render_from_story_map(self, story_map: StoryMap,
                               layout_data: Optional[LayoutData] = None) -> Dict[str, Any]:
        """Render outline diagram.  Each node renders itself.

        Computes global row positions first so all epics share the
        same Y levels, then lays out epics left-to-right.
        """
        self._layout_data = layout_data
        self._drawio_epics = []
        self._extra_nodes = []

        epics = list(story_map.epics)
        if not epics:
            return {'epics': 0, 'sub_epic_count': 0, 'diagram_generated': True}

        # Global max depth → consistent rows across all epics
        max_depth = max(_max_sub_epic_depth(epic) for epic in epics)
        rows = _RowPositions(max_depth)

        x_pos = DrawIOEpic.X_START
        for epic in epics:
            drawio_epic = DrawIOStoryNodeSerializer.create_epic(
                epic.name, getattr(epic, 'sequential_order', 0) or 0)
            drawio_epic.render_from_domain(epic, x_pos, rows, layout_data)
            self._drawio_epics.append(drawio_epic)
            x_pos = drawio_epic.boundary.right + CELL_SPACING

        return {
            'epics': len(self._drawio_epics),
            'sub_epic_count': len(self.get_sub_epics()),
            'diagram_generated': True,
        }

    # ------------------------------------------------------------------
    # Render – Increments  (outline + increment lanes below)
    # ------------------------------------------------------------------

    def render_increments_from_story_map(
            self, story_map: StoryMap,
            increments_data: list,
            layout_data: Optional[LayoutData] = None) -> Dict[str, Any]:
        """Render outline first, then add increment lanes at the bottom."""
        summary = self.render_from_story_map(story_map, layout_data)

        y_start = self.get_bottom_y() + 50
        total_width = self.get_total_width()
        all_stories = self.get_stories()

        for idx, inc_data in enumerate(increments_data):
            story_names = []
            for s in inc_data.get('stories', []):
                story_names.append(s.get('name', '') if isinstance(s, dict) else str(s))

            lane = DrawIOIncrementLane(
                name=inc_data.get('name', f'Increment {idx + 1}'),
                priority=inc_data.get('priority', idx + 1),
                story_names=story_names)
            lane.render(idx, y_start, total_width, all_stories)
            self._extra_nodes.extend(lane.collect_all_elements())

        summary['increments'] = len(increments_data)
        return summary

    # ------------------------------------------------------------------
    # Render – Exploration / Acceptance Criteria
    # ------------------------------------------------------------------

    def render_exploration_from_story_map(
            self, story_map: StoryMap,
            layout_data: Optional[LayoutData] = None,
            scope: Optional[str] = None) -> Dict[str, Any]:
        """Render outline first, then add AC boxes below stories."""
        summary = self.render_from_story_map(story_map, layout_data)

        domain_stories = self._collect_domain_stories(story_map, scope)
        for drawio_story in self.get_stories():
            domain_story = domain_stories.get(drawio_story.name)
            if domain_story and domain_story.has_acceptance_criteria():
                ac_elems = drawio_story.render_ac_boxes(domain_story)
                self._extra_nodes.extend(ac_elems)

        summary['exploration'] = True
        if scope:
            summary['scope'] = scope
        return summary

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, file_path: Path):
        all_nodes = self._collect_all_nodes()
        xml_content = DrawIOStoryNodeSerializer.to_drawio_xml(all_nodes)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(xml_content, encoding='utf-8')

    def save_as_json(self, file_path: Path):
        data = self._to_story_graph_dict()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(data, indent=2), encoding='utf-8')

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def extract_layout(self) -> LayoutData:
        layout = LayoutData()
        for epic in self._drawio_epics:
            layout.set_entry(f'EPIC|{epic.name}',
                             epic.position.x, epic.position.y,
                             epic.boundary.width, epic.boundary.height)
            layout.set_entry(epic.cell_id,
                             epic.position.x, epic.position.y,
                             epic.boundary.width, epic.boundary.height)
            for se in epic.get_sub_epics():
                self._extract_layout_for_sub_epic(layout, epic.name, se)
        return layout

    def _extract_layout_for_sub_epic(self, layout: LayoutData, epic_name: str,
                                      se: DrawIOSubEpic):
        layout.set_entry(f'SUB_EPIC|{se.name}',
                         se.position.x, se.position.y,
                         se.boundary.width, se.boundary.height)
        layout.set_entry(se.cell_id,
                         se.position.x, se.position.y,
                         se.boundary.width, se.boundary.height)
        for nested_se in se.get_sub_epics():
            self._extract_layout_for_sub_epic(layout, epic_name, nested_se)
        for story in se.get_stories():
            layout.set_entry(
                f'STORY|{epic_name}|{se.name}|{story.name}',
                story.position.x, story.position.y,
                story.boundary.width, story.boundary.height)
            layout.set_entry(story.cell_id,
                             story.position.x, story.position.y,
                             story.boundary.width, story.boundary.height)

    # ------------------------------------------------------------------
    # Update report
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Dict conversion
    # ------------------------------------------------------------------

    def _to_story_graph_dict(self) -> Dict[str, Any]:
        epics = []
        for epic in self._drawio_epics:
            epic_dict = {
                'name': epic.name,
                'sequential_order': epic.sequential_order,
                'sub_epics': [self._sub_epic_to_dict(se) for se in epic.get_sub_epics()]
            }
            epics.append(epic_dict)
        return {'epics': epics}

    def _sub_epic_to_dict(self, se: DrawIOSubEpic) -> Dict[str, Any]:
        nested_sub_epics = se.get_sub_epics()
        if nested_sub_epics:
            return {
                'name': se.name,
                'sequential_order': se.sequential_order,
                'sub_epics': [self._sub_epic_to_dict(n) for n in nested_sub_epics],
                'story_groups': []
            }
        return {
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

    # ------------------------------------------------------------------
    # Load from DrawIO file (reverse direction)
    # ------------------------------------------------------------------

    @classmethod
    def load(cls, file_path: Path) -> 'DrawIOStoryMap':
        content = file_path.read_text(encoding='utf-8')
        nodes, parent_map = DrawIOStoryNodeSerializer.parse_nodes_from_xml(content)
        story_map = cls()

        nodes_by_id = {}
        for n in nodes:
            nodes_by_id[n.cell_id] = n

        epics = [n for n in nodes if isinstance(n, DrawIOEpic)]
        sub_epics = [n for n in nodes if isinstance(n, DrawIOSubEpic)]
        stories = [n for n in nodes if isinstance(n, DrawIOStory)]

        story_map._assign_by_parent_map(nodes_by_id, parent_map, epics, sub_epics, stories)
        story_map._assign_sequential_order_from_position(epics, sub_epics, stories)
        story_map._drawio_epics = epics

        classified = set()
        for e in epics:
            classified.add(id(e))
            for se in e.get_sub_epics():
                classified.add(id(se))
                for s in se.get_stories():
                    classified.add(id(s))
        story_map._extra_nodes = [n for n in nodes if id(n) not in classified]
        return story_map

    # ------------------------------------------------------------------
    # Internal helpers (load direction)
    # ------------------------------------------------------------------

    def _assign_by_parent_map(self, nodes_by_id, parent_map, epics, sub_epics, stories):
        all_nodes = list(epics) + list(sub_epics) + list(stories)
        for node in all_nodes:
            cell_id = node.cell_id
            if '/' not in cell_id:
                continue
            found = False
            parts = cell_id.split('/')
            for cut in range(len(parts) - 1, 0, -1):
                candidate = '/'.join(parts[:cut])
                parent_node = nodes_by_id.get(candidate)
                if parent_node and parent_node is not node:
                    parent_node.add_child(node)
                    found = True
                    break
            if found:
                continue
            pid = parent_map.get(cell_id, '')
            parent_from_attr = nodes_by_id.get(pid)
            if parent_from_attr and parent_from_attr is not node:
                parent_from_attr.add_child(node)
                continue

        for se in sub_epics:
            if se._parent is not None:
                continue
            for epic in epics:
                if epic.boundary.contains_position(se.boundary.center):
                    epic.add_child(se)
                    break

        for story in stories:
            if story._parent is not None:
                continue
            for se in sub_epics:
                if se.boundary.contains_position(story.boundary.center):
                    se.add_child(story)
                    break

    def _assign_sequential_order_from_position(self, epics, sub_epics, stories):
        for group in [epics, sub_epics, stories]:
            sorted_nodes = sorted(group, key=lambda n: (n.position.y, n.position.x))
            for idx, node in enumerate(sorted_nodes):
                node.sequential_order = float(idx + 1)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _collect_all_nodes(self) -> list:
        """Walk the tree and gather every renderable node."""
        nodes = []
        for epic in self._drawio_epics:
            nodes.extend(epic.collect_all_nodes())
        nodes.extend(self._extra_nodes)
        return nodes

    def _collect_domain_stories(self, story_map: StoryMap,
                                 scope: Optional[str] = None) -> dict:
        """Build name→Story lookup, optionally filtered by scope (increment name)."""
        result: Dict[str, Story] = {}
        scope_names = None
        if scope:
            for inc in story_map.story_graph.get('increments', []):
                if inc.get('name') == scope:
                    scope_names = set()
                    for s in inc.get('stories', []):
                        scope_names.add(s.get('name', '') if isinstance(s, dict) else str(s))
                    break

        for epic in story_map.epics:
            for sub_epic in epic.sub_epics:
                self._gather_stories(sub_epic, result, scope_names)
        return result

    def _gather_stories(self, sub_epic, result: dict, scope_names):
        for child in sub_epic.children:
            if isinstance(child, Story):
                if scope_names is None or child.name in scope_names:
                    result[child.name] = child
            elif isinstance(child, SubEpic):
                self._gather_stories(child, result, scope_names)
            elif isinstance(child, StoryGroup):
                for story in child.children:
                    if isinstance(story, Story):
                        if scope_names is None or story.name in scope_names:
                            result[story.name] = story
