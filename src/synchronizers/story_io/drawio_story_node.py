from typing import List, Optional, Any
from dataclasses import dataclass, field
from story_graph.nodes import StoryNode, Epic, SubEpic, Story, StoryGroup
from story_graph.domain import DomainConcept, StoryUser
from .drawio_element import DrawIOElement, STYLE_DEFAULTS
from .story_io_position import Position, Boundary
from .update_report import UpdateReport


# ---------------------------------------------------------------------------
# Row-based layout constants (matching reference diagram)
# ---------------------------------------------------------------------------
CELL_SIZE = 50           # Stories and actors are 50x50 squares
CELL_SPACING = 10        # Horizontal gap between cells
EPIC_Y = 120             # Y position of epic row
EPIC_HEIGHT = 60         # Height of epic bar
SUB_EPIC_HEIGHT = 60     # Height of sub-epic bar
ROW_GAP = 15             # Gap between rows
ACTOR_GAP = 25           # Extra gap before actor row
BAR_PADDING = 5          # Internal horizontal padding for bars
SPACING = CELL_SPACING   # alias kept for backward compatibility
CONTAINER_PADDING = BAR_PADDING


def _slug(name: str) -> str:
    return name.lower().replace(' ', '-')


def _max_sub_epic_depth(node) -> int:
    """Max nesting depth of sub-epics under a domain node.

    Returns 0 if node has no sub-epics, 1 for flat sub-epics,
    2 for one level of nesting, etc.
    """
    sub_epics = []
    if hasattr(node, 'sub_epics'):
        sub_epics = list(node.sub_epics)
    elif hasattr(node, 'children'):
        sub_epics = [c for c in node.children if isinstance(c, SubEpic)]
    if not sub_epics:
        return 0
    return 1 + max(_max_sub_epic_depth(se) for se in sub_epics)


class _RowPositions:
    """Computes absolute Y positions for every row in the story map.

    All epics share the same row layout so stories across different
    epics line up horizontally.
    """

    def __init__(self, max_depth: int):
        self.max_depth = max(max_depth, 1)

    def sub_epic_y(self, depth: int) -> float:
        return EPIC_Y + EPIC_HEIGHT + ROW_GAP + depth * (SUB_EPIC_HEIGHT + ROW_GAP)

    @property
    def actor_y(self) -> float:
        deepest = self.sub_epic_y(self.max_depth - 1)
        return deepest + SUB_EPIC_HEIGHT + ACTOR_GAP

    @property
    def story_y(self) -> float:
        return self.actor_y + CELL_SIZE + ROW_GAP


# ---------------------------------------------------------------------------
# DrawIO Story Nodes
# ---------------------------------------------------------------------------

@dataclass
class DrawIOStoryNode(StoryNode):
    _element: DrawIOElement = field(default=None, repr=False)

    def __post_init__(self):
        super().__post_init__()
        if self._element is None:
            self._element = DrawIOElement(cell_id=_slug(self.name), value=self.name)

    @property
    def children(self) -> List['StoryNode']:
        return list(self._children)

    @property
    def element(self) -> DrawIOElement:
        return self._element

    @property
    def position(self) -> Position:
        return self._element.position

    @property
    def boundary(self) -> Boundary:
        return self._element.boundary

    @property
    def fill(self) -> Optional[str]:
        return self._element.fill

    @property
    def stroke(self) -> Optional[str]:
        return self._element.stroke

    @property
    def font_color(self) -> Optional[str]:
        return self._element.font_color

    @property
    def shape(self) -> Optional[str]:
        return self._element.shape

    @property
    def cell_id(self) -> str:
        return self._element.cell_id

    def set_position(self, x: float, y: float):
        self._element.set_position(x, y)

    def set_size(self, width: float, height: float):
        self._element.set_size(width, height)

    def add_child(self, child: 'DrawIOStoryNode'):
        child._parent = self
        self._children.append(child)

    def compute_container_dimensions_from_children(self, spacing: float = SPACING) -> Boundary:
        """Kept for backward compatibility but not used in row-based layout."""
        return self._element.boundary

    def _saved_position_for(self, key: str, layout_data) -> Optional[Position]:
        if layout_data:
            return layout_data.position_for(key)
        return None

    def collect_all_nodes(self) -> list:
        """Collect self and all descendant nodes for serialization."""
        nodes = [self]
        for child in self._children:
            if hasattr(child, 'collect_all_nodes'):
                nodes.extend(child.collect_all_nodes())
            else:
                nodes.append(child)
        return nodes


@dataclass
class DrawIOEpic(Epic, DrawIOStoryNode):
    _parent: Optional[StoryNode] = field(default=None, repr=False)

    # Kept as class-level references for tests
    Y_DEFAULT = EPIC_Y
    X_START = 20
    SUB_EPIC_Y_OFFSET = ROW_GAP + EPIC_HEIGHT   # not used directly anymore

    def __post_init__(self):
        if self.domain_concepts is None:
            self.domain_concepts = []
        DrawIOStoryNode.__post_init__(self)
        self._element.apply_style_for_type('epic')

    @property
    def children(self) -> List['StoryNode']:
        return list(self._children)

    def get_sub_epics(self) -> List['DrawIOSubEpic']:
        return [c for c in self._children if isinstance(c, DrawIOSubEpic)]

    @property
    def sub_epics(self) -> List['DrawIOSubEpic']:
        return self.get_sub_epics()

    def get_stories(self) -> List['DrawIOStory']:
        stories = []
        for sub_epic in self.get_sub_epics():
            stories.extend(sub_epic.get_all_stories_recursive())
        return stories

    @property
    def all_stories(self) -> List['DrawIOStory']:
        return self.get_stories()

    def render_from_domain(self, epic: Epic, x_pos: float,
                            rows: _RowPositions = None,
                            layout_data=None) -> 'DrawIOEpic':
        """Render epic as a flat horizontal bar spanning its sub-epics.

        The epic does NOT visually contain its sub-epics; it sits on
        its own row and its width spans from the first to the last
        sub-epic underneath it.
        """
        from .drawio_story_node_serializer import DrawIOStoryNodeSerializer

        if rows is None:
            depth = _max_sub_epic_depth(epic)
            rows = _RowPositions(depth)

        epic_slug = _slug(self.name)
        self._element._cell_id = epic_slug

        cursor_x = x_pos + BAR_PADDING
        for sub_epic in epic.sub_epics:
            drawio_se = DrawIOStoryNodeSerializer.create_sub_epic(
                sub_epic.name, getattr(sub_epic, 'sequential_order', 0) or 0)
            cursor_x = drawio_se.render_from_domain(
                sub_epic, cursor_x, depth=0, rows=rows,
                layout_data=layout_data, path_prefix=epic_slug)
            self.add_child(drawio_se)
            cursor_x += CELL_SPACING

        # Remove trailing spacing
        if epic.sub_epics:
            cursor_x -= CELL_SPACING

        saved = self._saved_position_for(f'EPIC|{self.name}', layout_data)
        epic_x = saved.x if saved else x_pos
        epic_y = saved.y if saved else EPIC_Y
        self.set_position(epic_x, epic_y)
        self.set_size(max(cursor_x - x_pos + BAR_PADDING, 100), EPIC_HEIGHT)
        return self

    def collect_all_nodes(self) -> list:
        nodes = [self]
        for se in self.get_sub_epics():
            nodes.extend(se.collect_all_nodes())
        return nodes

    def generate_update_report_for_epic_subtree(self, original_epic, report: UpdateReport):
        extracted_sub_epics = sorted(self.get_sub_epics(), key=lambda s: s.sequential_order or 0)
        original_sub_epics = sorted(original_epic.sub_epics, key=lambda s: getattr(s, 'sequential_order', 0) or 0)

        for i, ext_se in enumerate(extracted_sub_epics):
            if i < len(original_sub_epics):
                orig_se = original_sub_epics[i]
                if ext_se.name != orig_se.name:
                    report.add_rename(ext_se.name, orig_se.name, confidence=1.0, parent=self.name)
                else:
                    report.add_exact_match(ext_se.name, orig_se.name, parent=self.name)
                ext_se.generate_update_report_for_sub_epic_subtree(orig_se, report)
            else:
                for story in ext_se.get_all_stories_recursive():
                    report.add_new_story(story.name, parent=ext_se.name)

        for i in range(len(extracted_sub_epics), len(original_sub_epics)):
            report.add_missing_sub_epic(original_sub_epics[i].name)


@dataclass
class DrawIOSubEpic(SubEpic, DrawIOStoryNode):
    _parent: Optional[StoryNode] = field(default=None, repr=False)

    # Kept for backward-compat references
    Y_OFFSET_FROM_PARENT = SUB_EPIC_HEIGHT + ROW_GAP
    STORY_Y_OFFSET = 0   # not used in row-based layout

    def __post_init__(self):
        if self.domain_concepts is None:
            self.domain_concepts = []
        DrawIOStoryNode.__post_init__(self)
        self._element.apply_style_for_type('sub_epic')
        if not hasattr(self, 'test_file'):
            self.test_file = None

    @property
    def children(self) -> List['StoryNode']:
        return list(self._children)

    def get_sub_epics(self) -> List['DrawIOSubEpic']:
        return [c for c in self._children if isinstance(c, DrawIOSubEpic)]

    def get_stories(self) -> List['DrawIOStory']:
        return sorted([c for c in self._children if isinstance(c, DrawIOStory)],
                       key=lambda s: s.sequential_order or 0)

    def get_all_stories_recursive(self) -> List['DrawIOStory']:
        stories = list(self.get_stories())
        for nested_se in self.get_sub_epics():
            stories.extend(nested_se.get_all_stories_recursive())
        return stories

    @property
    def all_stories(self) -> List['DrawIOStory']:
        return self.get_stories()

    def render_from_domain(self, sub_epic, x_cursor: float, depth: int,
                            rows: _RowPositions,
                            layout_data=None,
                            path_prefix: str = '') -> float:
        """Render sub-epic as a flat horizontal bar.

        Returns the x position of the right edge of this sub-epic's
        content (so the caller knows where to place the next sibling).
        """
        from .drawio_story_node_serializer import DrawIOStoryNodeSerializer

        se_path = f'{path_prefix}/{_slug(self.name)}' if path_prefix else _slug(self.name)
        self._element._cell_id = se_path

        nested = [c for c in sub_epic.children if isinstance(c, SubEpic)]
        start_x = x_cursor

        if nested:
            inner_x = x_cursor + BAR_PADDING
            for n in nested:
                drawio_n = DrawIOStoryNodeSerializer.create_sub_epic(
                    n.name, getattr(n, 'sequential_order', 0) or 0)
                inner_x = drawio_n.render_from_domain(
                    n, inner_x, depth + 1, rows, layout_data,
                    path_prefix=se_path)
                self.add_child(drawio_n)
                inner_x += CELL_SPACING
            inner_x -= CELL_SPACING  # remove trailing
            end_x = inner_x + BAR_PADDING
        else:
            stories = [c for c in sub_epic.children if isinstance(c, Story)]
            stories.sort(key=lambda s: getattr(s, 'sequential_order', 0) or 0)

            se_saved = self._saved_position_for(f'SUB_EPIC|{self.name}', layout_data)
            se_right = (se_saved.x + layout_data.boundary_for(f'SUB_EPIC|{self.name}').width) if (se_saved and layout_data and layout_data.boundary_for(f'SUB_EPIC|{self.name}')) else None
            se_left = x_cursor + BAR_PADDING

            story_x = se_left
            story_y = rows.story_y
            seen_actors: set = set()
            for story in stories:
                story_type = getattr(story, 'story_type', 'user') or 'user'
                drawio_story = DrawIOStoryNodeSerializer.create_story(
                    story.name, getattr(story, 'sequential_order', 0) or 0, story_type)
                story_path = f'{se_path}/{_slug(drawio_story.name)}' if se_path else _slug(drawio_story.name)
                has_saved = layout_data and layout_data.position_for(story_path)
                if has_saved:
                    drawio_story.render_from_domain(
                        story, story_x, story_y, rows.actor_y,
                        path_prefix=se_path, seen_actors=seen_actors,
                        layout_data=layout_data)
                else:
                    if se_right and story_x + CELL_SIZE > se_right:
                        story_x = se_left
                        story_y += CELL_SIZE + CELL_SPACING
                    drawio_story.render_from_domain(
                        story, story_x, story_y, rows.actor_y,
                        path_prefix=se_path, seen_actors=seen_actors,
                        layout_data=None)
                self.add_child(drawio_story)
                story_x += CELL_SIZE + CELL_SPACING
            if stories:
                story_x -= CELL_SPACING
            end_x = story_x + BAR_PADDING

        se_y = rows.sub_epic_y(depth)
        self.set_position(start_x, se_y)
        self.set_size(max(end_x - start_x, CELL_SIZE + 2 * BAR_PADDING),
                       SUB_EPIC_HEIGHT)
        return end_x

    def collect_all_nodes(self) -> list:
        nodes = [self]
        for se in self.get_sub_epics():
            nodes.extend(se.collect_all_nodes())
        for story in self.get_stories():
            nodes.extend(story.collect_all_nodes())
        return nodes

    def generate_update_report_for_sub_epic_subtree(self, original_sub_epic, report: UpdateReport):
        extracted_nested = sorted(self.get_sub_epics(), key=lambda s: s.sequential_order or 0)
        original_nested = sorted([c for c in original_sub_epic._children if isinstance(c, SubEpic)],
                                  key=lambda s: getattr(s, 'sequential_order', 0) or 0)

        for i, ext_nse in enumerate(extracted_nested):
            if i < len(original_nested):
                orig_nse = original_nested[i]
                if ext_nse.name != orig_nse.name:
                    report.add_rename(ext_nse.name, orig_nse.name, confidence=1.0, parent=self.name)
                else:
                    report.add_exact_match(ext_nse.name, orig_nse.name, parent=self.name)
                ext_nse.generate_update_report_for_sub_epic_subtree(orig_nse, report)
            else:
                for story in ext_nse.get_all_stories_recursive():
                    report.add_new_story(story.name, parent=ext_nse.name)

        for i in range(len(extracted_nested), len(original_nested)):
            report.add_missing_sub_epic(original_nested[i].name)

        extracted_stories = sorted(self.get_stories(), key=lambda s: s.sequential_order or 0)
        orig_stories = sorted([c for c in original_sub_epic.children if isinstance(c, Story)],
                               key=lambda s: getattr(s, 'sequential_order', 0) or 0)

        for i, ext_story in enumerate(extracted_stories):
            if i < len(orig_stories):
                if ext_story.name != orig_stories[i].name:
                    report.add_rename(ext_story.name, orig_stories[i].name, confidence=1.0, parent=self.name)
                else:
                    report.add_exact_match(ext_story.name, orig_stories[i].name, parent=self.name)
            else:
                report.add_new_story(ext_story.name, parent=self.name)

        for i in range(len(extracted_stories), len(orig_stories)):
            report.add_removed_story(orig_stories[i].name, parent=self.name)


@dataclass
class DrawIOStory(Story, DrawIOStoryNode):
    _parent: Optional[StoryNode] = field(default=None, repr=False)

    # Stories are 50x50 sticky-note squares
    WIDTH = CELL_SIZE
    HEIGHT = CELL_SIZE
    ACTOR_HEIGHT = CELL_SIZE
    ACTOR_SPACING = 2
    AC_MIN_WIDTH = 250
    AC_HEIGHT = 60
    AC_SPACING_Y = 10
    AC_CHAR_WIDTH = 6
    AC_PADDING = 10

    STORY_TYPE_STYLES = {
        'user': 'story_user',
        None: 'story_user',
        '': 'story_user',
        'system': 'story_system',
        'technical': 'story_technical',
    }

    def __post_init__(self):
        if self.users is None:
            self.users = []
        DrawIOStoryNode.__post_init__(self)
        style_key = self.STORY_TYPE_STYLES.get(self.story_type, 'story_user')
        self._element.apply_style_for_type(style_key)
        self._actor_elements: List[DrawIOElement] = []
        self._ac_elements: List[DrawIOElement] = []

    @property
    def children(self) -> List['StoryNode']:
        return list(self._children)

    def render_from_domain(self, story, x_pos: float, story_y: float,
                            actor_y: float = 0,
                            path_prefix: str = '',
                            seen_actors: set = None,
                            layout_data=None) -> 'DrawIOStory':
        story_path = f'{path_prefix}/{_slug(self.name)}' if path_prefix else _slug(self.name)
        self._element._cell_id = story_path

        saved = self._saved_position_for(story_path, layout_data)
        final_x = saved.x if saved else x_pos
        final_y = saved.y if saved else story_y
        self.set_position(final_x, final_y)
        self.set_size(CELL_SIZE, CELL_SIZE)

        # Actors placed directly above this story (deduplicated within sub-epic)
        users = getattr(story, 'users', []) or []
        for user in users:
            user_name = user.name if hasattr(user, 'name') else str(user)
            if seen_actors is not None:
                if user_name in seen_actors:
                    continue
                seen_actors.add(user_name)
            actor = DrawIOElement(
                cell_id=f'{story_path}/actor-{_slug(user_name)}',
                value=user_name)
            actor.apply_style_for_type('actor')
            actor.set_position(x_pos, actor_y)
            actor.set_size(CELL_SIZE, CELL_SIZE)
            self._actor_elements.append(actor)
        return self

    def render_ac_boxes(self, domain_story) -> List[DrawIOElement]:
        """Create acceptance criteria DrawIOElements below this story."""
        ac_list = getattr(domain_story, 'acceptance_criteria', []) or []
        if not ac_list:
            return []

        elements = []
        ac_y = self.position.y + self.HEIGHT + self.AC_SPACING_Y

        for idx, ac in enumerate(ac_list):
            text = self._format_ac_text(ac)
            if not text:
                continue
            ac_width = max(self.AC_MIN_WIDTH, len(text) * self.AC_CHAR_WIDTH + self.AC_PADDING * 2)
            ac_elem = DrawIOElement(
                cell_id=f'{self.cell_id}/ac-{idx}',
                value=text)
            ac_elem.apply_style_for_type('acceptance_criteria')
            ac_elem.set_position(self.position.x, ac_y)
            ac_elem.set_size(ac_width, self.AC_HEIGHT)
            elements.append(ac_elem)
            ac_y += self.AC_HEIGHT + self.AC_SPACING_Y

        self._ac_elements = elements
        return elements

    def _format_ac_text(self, ac) -> str:
        if hasattr(ac, 'name') and ac.name:
            return ac.name
        if isinstance(ac, str):
            return ac
        if isinstance(ac, dict):
            return ac.get('name', ac.get('description', ''))
        return str(ac) if ac else ''

    def collect_all_nodes(self) -> list:
        nodes = [self]
        nodes.extend(self._actor_elements)
        nodes.extend(self._ac_elements)
        return nodes



class DrawIOIncrementLane:
    """An increment lane (horizontal band) in the story map diagram."""

    LANE_HEIGHT = 100
    LABEL_WIDTH = 150
    STORY_Y_OFFSET = 25

    PRIORITY_COLORS = [
        '#f5f5f5',
        '#e8f5e9',
        '#e3f2fd',
        '#fff3e0',
        '#fce4ec',
    ]

    def __init__(self, name: str, priority: int, story_names: list):
        self.name = name
        self.priority = priority
        self.story_names = set(story_names)
        self._lane_element: Optional[DrawIOElement] = None
        self._label_element: Optional[DrawIOElement] = None
        self._story_copies: List[DrawIOElement] = []

    def render(self, index: int, y_start: float, total_width: float,
               stories: List['DrawIOStory']) -> float:
        lane_y = y_start + index * self.LANE_HEIGHT

        color_idx = min(self.priority, len(self.PRIORITY_COLORS) - 1)
        lane_slug = _slug(self.name)
        self._lane_element = DrawIOElement(cell_id=f'inc-lane/{lane_slug}', value='')
        self._lane_element.set_style(fill=self.PRIORITY_COLORS[color_idx], stroke='#cccccc')
        self._lane_element.set_position(0, lane_y)
        self._lane_element.set_size(total_width + 40, self.LANE_HEIGHT)

        self._label_element = DrawIOElement(cell_id=f'inc-label/{lane_slug}', value=self.name)
        self._label_element.apply_style_for_type('increment_lane')
        self._label_element.set_position(5, lane_y + 5)
        self._label_element.set_size(self.LABEL_WIDTH, 30)

        self._story_copies = []
        for story in stories:
            if story.name in self.story_names:
                copy = DrawIOElement(
                    cell_id=f'inc-lane/{lane_slug}/{story.cell_id}',
                    value=story.name)
                style_key = DrawIOStory.STORY_TYPE_STYLES.get(story.story_type, 'story_user')
                copy.apply_style_for_type(style_key)
                copy.set_position(story.position.x, lane_y + self.STORY_Y_OFFSET)
                copy.set_size(CELL_SIZE, CELL_SIZE)
                self._story_copies.append(copy)

        return self.LANE_HEIGHT

    def collect_all_elements(self) -> list:
        elements = []
        if self._lane_element:
            elements.append(self._lane_element)
        if self._label_element:
            elements.append(self._label_element)
        elements.extend(self._story_copies)
        return elements
