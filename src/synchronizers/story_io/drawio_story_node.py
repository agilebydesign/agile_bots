from typing import List, Optional, Any
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from story_graph.nodes import StoryNode, Epic, SubEpic, Story, StoryGroup
from story_graph.domain import DomainConcept, StoryUser
from .drawio_element import DrawIOElement, STYLE_DEFAULTS
from .story_io_position import Position, Boundary
from .update_report import UpdateReport


@dataclass
class DrawIOStoryNode(StoryNode):
    _element: DrawIOElement = field(default=None, repr=False)

    def __post_init__(self):
        super().__post_init__()
        if self._element is None:
            self._element = DrawIOElement(cell_id=self.name.lower().replace(' ', '-'), value=self.name)

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

    def compute_container_dimensions_from_children(self, spacing: float = 10.0) -> Boundary:
        if not self._children:
            return self._element.boundary
        child_boundaries = [c.boundary for c in self._children if hasattr(c, 'boundary')]
        if not child_boundaries:
            return self._element.boundary
        total_width = sum(b.width for b in child_boundaries) + spacing * (len(child_boundaries) - 1)
        max_height = max(b.height for b in child_boundaries)
        padding = 10
        self._element.set_size(total_width + 2 * padding, max_height + 90)
        return self._element.boundary


@dataclass
class DrawIOEpic(Epic, DrawIOStoryNode):
    _parent: Optional[StoryNode] = field(default=None, repr=False)

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
            stories.extend(sub_epic.get_stories())
        return stories

    @property
    def all_stories(self) -> List['DrawIOStory']:
        return self.get_stories()

    def generate_update_report_for_epic_subtree(self, original_epic, report: UpdateReport):
        extracted_sub_epics = self.get_sub_epics()
        original_sub_epics = original_epic.sub_epics
        matched_originals = set()
        for extracted_se in extracted_sub_epics:
            for idx, orig_se in enumerate(original_sub_epics):
                if idx not in matched_originals and extracted_se.name.lower() == orig_se.name.lower():
                    matched_originals.add(idx)
                    extracted_se.generate_update_report_for_sub_epic_subtree(orig_se, report)
                    break
            else:
                for story in extracted_se.get_stories():
                    report.add_new_story(story.name, parent=extracted_se.name)
        for idx, orig_se in enumerate(original_sub_epics):
            if idx not in matched_originals:
                report.add_missing_sub_epic(orig_se.name)


@dataclass
class DrawIOSubEpic(SubEpic, DrawIOStoryNode):
    _parent: Optional[StoryNode] = field(default=None, repr=False)

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

    def get_stories(self) -> List['DrawIOStory']:
        return sorted([c for c in self._children if isinstance(c, DrawIOStory)],
                       key=lambda s: s.sequential_order or 0)

    @property
    def all_stories(self) -> List['DrawIOStory']:
        return self.get_stories()

    def generate_update_report_for_sub_epic_subtree(self, original_sub_epic, report: UpdateReport):
        extracted_stories = self.get_stories()
        orig_stories = [c for c in original_sub_epic.children if isinstance(c, Story)]

        matched_originals = set()
        for ext_story in extracted_stories:
            ext_story.match_against_originals(orig_stories, matched_originals, report, parent=self.name)
        for idx, orig_s in enumerate(orig_stories):
            if idx not in matched_originals:
                report.add_removed_story(orig_s.name, parent=self.name)


@dataclass
class DrawIOStory(Story, DrawIOStoryNode):
    _parent: Optional[StoryNode] = field(default=None, repr=False)

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

    @property
    def children(self) -> List['StoryNode']:
        return list(self._children)

    def match_against_originals(self, original_stories: list, matched_originals: set,
                                 report: UpdateReport, parent: str = ''):
        for idx, orig in enumerate(original_stories):
            if idx in matched_originals:
                continue
            if self.name.lower() == orig.name.lower():
                matched_originals.add(idx)
                report.add_exact_match(self.name, orig.name, parent=parent)
                return

        best_ratio = 0.0
        best_idx = -1
        best_orig_name = ''
        for idx, orig in enumerate(original_stories):
            if idx in matched_originals:
                continue
            ratio = SequenceMatcher(None, self.name.lower(), orig.name.lower()).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_idx = idx
                best_orig_name = orig.name

        if best_ratio >= 0.7 and best_idx >= 0:
            matched_originals.add(best_idx)
            report.add_fuzzy_match(self.name, best_orig_name, confidence=best_ratio, parent=parent)
            return

        report.add_new_story(self.name, parent=parent)
