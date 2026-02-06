from typing import List, Dict, Any, Optional, Union
from dataclasses import field
from .story_io_component import StoryIOComponent
from .story_io_epic import Epic
from .story_io_feature import Feature
from .story_io_story import Story
from .story_io_position import Boundary


class Increment(StoryIOComponent):
    
    def __init__(self, name: str, priority: Union[int, str] = 1,
                 position: Optional[Any] = None, boundary: Optional[Boundary] = None,
                 flag: bool = False, parent: Optional[StoryIOComponent] = None):
        priority_int = self._priority_to_int(priority)
        super().__init__(name, float(priority_int), position, boundary, flag, parent)
        self._priority_value = priority
        self._priority_int = priority_int
    
    @staticmethod
    def _priority_to_int(priority: Union[int, str]) -> int:
        if isinstance(priority, str):
            priority_map = {'NOW': 1, 'LATER': 2, 'SOON': 1, 'NEXT': 2}
            return priority_map.get(priority.upper(), 1)
        elif isinstance(priority, (int, float)):
            return int(priority)
        else:
            return 1
    
    @property
    def priority(self) -> Union[int, str]:
        return self._priority_value
    
    @property
    def priority_int(self) -> int:
        return self._priority_int
    
    @property
    def epics(self) -> List[Epic]:
        return [child for child in self.children if isinstance(child, Epic)]
    
    @property
    def sub_epics(self) -> List[Feature]:
        return [child for child in self.children if isinstance(child, Feature)]
    
    @property
    def features(self) -> List[Feature]:
        return self.sub_epics
    
    @property
    def stories(self) -> List[Story]:
        return [child for child in self.children if isinstance(child, Story)]
    
    @property
    def story_names(self) -> List[str]:
        return self._story_names if hasattr(self, '_story_names') else []
    
    @story_names.setter
    def story_names(self, names: List[str]) -> None:
        self._story_names = names
    
    def add_story(self, story: Story) -> None:
        if self.stories:
            last_story = max(self.stories, key=lambda s: s.position.y if s.position else 0)
            if last_story.position and last_story.boundary:
                base_y = last_story.boundary.bottom
            else:
                base_y = 450
        else:
            base_y = 450
        
        if self.stories and self.stories[-1].users:
            last_users = set(self.stories[-1].users)
            story_users = set(story.users)
            has_different_users = story_users != last_users
        else:
            has_different_users = bool(story.users)
        
        spacing = 60 if has_different_users else 55
        
        from .story_io_position import Position
        story.position = Position(
            self.boundary.x + 10 if self.boundary else 10,
            base_y + spacing
        )
        
        story.change_parent(self)
        
        if story.position and story.boundary:
            story_bottom = story.boundary.bottom
            if self.boundary and story_bottom > self.boundary.bottom:
                self.boundary = Boundary(
                    self.boundary.x,
                    self.boundary.y,
                    self.boundary.width,
                    story_bottom - self.boundary.y + 20
                )
    
    def synchronize(self) -> Dict[str, Any]:
        result = {
            'name': self.name,
            'priority': self._priority_value,
            'epics': [e.synchronize() for e in self.epics],
            'sub_epics': [f.synchronize() for f in self.sub_epics]
        }
        if hasattr(self, '_story_names') and self._story_names:
            result['stories'] = self._story_names
        else:
            result['stories'] = [s.synchronize() for s in self.stories]
        return result
    
    def synchronize_report(self) -> Dict[str, Any]:
        return {
            'increment': self.name,
            'priority': self._priority_value,
            'epics_count': len(self.epics),
            'sub_epics_count': len(self.sub_epics),
            'stories_count': len(self.story_names) if hasattr(self, '_story_names') else len(self.stories),
            'status': 'synchronized'
        }
    
    def compare(self, other: 'StoryIOComponent') -> Dict[str, Any]:
        if not isinstance(other, Increment):
            return {'match': False, 'reason': 'Type mismatch'}
        
        return {
            'match': self.name == other.name and self._priority_int == other._priority_int,
            'name_match': self.name == other.name,
            'priority_match': self._priority_int == other._priority_int,
            'stories_count_match': len(self.story_names) == len(other.story_names) if hasattr(self, '_story_names') and hasattr(other, '_story_names') else len(self.stories) == len(other.stories)
        }
    
    def render(self) -> Dict[str, Any]:
        result = {
            'name': self.name,
            'priority': self._priority_value,
        }
        
        if hasattr(self, '_relative_size'):
            result['relative_size'] = self._relative_size
        if hasattr(self, '_approach'):
            result['approach'] = self._approach
        if hasattr(self, '_focus'):
            result['focus'] = self._focus
        
        if self.epics:
            result['epics'] = [e.render() for e in self.epics]
        if self.sub_epics:
            result['sub_epics'] = [f.render() for f in self.sub_epics]
        
        if hasattr(self, '_story_names') and self._story_names:
            result['stories'] = self._story_names
        elif self.stories:
            result['stories'] = [s.render() for s in self.stories]
        
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result['type'] = 'increment'
        result['priority'] = self._priority_value
        result['epics'] = [e.to_dict() for e in self.epics]
        result['sub_epics'] = [f.to_dict() for f in self.sub_epics]
        if hasattr(self, '_story_names') and self._story_names:
            result['stories'] = self._story_names
        else:
            result['stories'] = [s.to_dict() for s in self.stories]
        return result


def _sort_stories_by_sequential_order(stories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(stories, key=lambda s: s.get("sequential_order", 0))


def get_increments_view(story_graph: Dict[str, Any]) -> Dict[str, Any]:
    increments = story_graph.get("increments", [])
    if not increments:
        return {
            "increments": [],
            "message": "No increments defined in story graph"
        }
    return {"increments": increments}


def format_increments_for_cli(story_graph: Dict[str, Any]) -> str:
    output_lines = []
    for increment in story_graph.get("increments", []):
        output_lines.append(f"{increment['name']}:")
        stories = increment.get("stories", [])
        if stories:
            for story in _sort_stories_by_sequential_order(stories):
                output_lines.append(f"  - {story['name']}")
        else:
            output_lines.append("  (no stories)")
    return "\n".join(output_lines)


def toggle_view(panel_state: Dict[str, Any]) -> Dict[str, Any]:
    current_view = panel_state.get("current_view", "Hierarchy")
    new_view = "Increment" if current_view == "Hierarchy" else "Hierarchy"
    return {
        "current_view": new_view,
        "toggle_label": current_view,
        "tooltip": f"Display {current_view} view"
    }


def render_increment_view(panel_state: Dict[str, Any]) -> Dict[str, Any]:
    columns = []
    for increment in panel_state.get("increments", []):
        stories = increment.get("stories", [])
        sorted_stories = _sort_stories_by_sequential_order(stories)
        column = {
            "name": increment["name"],
            "stories": sorted_stories,
            "read_only": True
        }
        if not stories:
            column["empty_message"] = "(no stories)"
        columns.append(column)
    return {
        "columns": columns,
        "controls_visible": False
    }
