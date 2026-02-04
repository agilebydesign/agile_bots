
import json
from cli.adapters import JSONAdapter
from story_graph.story_graph import StoryGraph

class JSONStoryGraph(JSONAdapter):
    
    def __init__(self, story_graph: StoryGraph):
        self.story_graph = story_graph
    
    @property
    def path(self):
        return self.story_graph.path
    
    @property
    def has_epics(self):
        return self.story_graph.has_epics
    
    @property
    def has_increments(self):
        return self.story_graph.has_increments
    
    @property
    def has_domain_concepts(self):
        return self.story_graph.has_domain_concepts
    
    @property
    def epic_count(self):
        return self.story_graph.epic_count
    
    @property
    def content(self):
        return self.story_graph.content
    
    def to_dict(self) -> dict:
        # Load domain objects and serialize them directly
        from story_graph.nodes import StoryMap
        story_map = StoryMap(self.story_graph.content, bot=None)
        
        # Create a mapping of epic/sub-epic names to their original JSON data for domain_concepts lookup
        # Recursively collect all nested sub-epics
        epic_name_to_data = {}
        def collect_sub_epics(epic_or_sub_epic_data):
            """Recursively collect all sub-epics from nested structure."""
            name = epic_or_sub_epic_data.get('name')
            if name:
                epic_name_to_data[name] = epic_or_sub_epic_data
            for sub_epic_data in epic_or_sub_epic_data.get('sub_epics', []):
                collect_sub_epics(sub_epic_data)
        
        for epic_data in self.story_graph.content.get('epics', []):
            collect_sub_epics(epic_data)
        
        # Serialize domain objects to JSON by reading their properties
        content = {
            'epics': [self._serialize_epic(epic, epic_name_to_data) for epic in story_map._epics]
        }
        
        # Add increments and other top-level fields from original content
        if 'increments' in self.story_graph.content:
            content['increments'] = self.story_graph.content['increments']
        
        # Add domain_concepts if they exist at top level
        if 'domain_concepts' in self.story_graph.content:
            # Serialize domain_concepts if they are DomainConcept objects
            domain_concepts_raw = self.story_graph.content['domain_concepts']
            if domain_concepts_raw and isinstance(domain_concepts_raw, list) and len(domain_concepts_raw) > 0:
                from story_graph.domain import DomainConcept
                # Check if first item is already a dict or a DomainConcept object
                if isinstance(domain_concepts_raw[0], dict):
                    content['domain_concepts'] = domain_concepts_raw
                else:
                    content['domain_concepts'] = [dc.to_dict() if hasattr(dc, 'to_dict') else dc.__dict__ for dc in domain_concepts_raw]
            else:
                content['domain_concepts'] = domain_concepts_raw
        
        return {
            'path': str(self.story_graph.path),
            'has_epics': self.story_graph.has_epics,
            'has_increments': self.story_graph.has_increments,
            'has_domain_concepts': self.story_graph.has_domain_concepts,
            'epic_count': self.story_graph.epic_count,
            'content': content
        }
    
    def _serialize_epic(self, epic, name_to_data_map=None) -> dict:
        """Serialize Epic object to dict by reading its properties."""
        # Serialize domain_concepts properly (they are DomainConcept objects)
        domain_concepts_serialized = []
        if hasattr(epic, 'domain_concepts') and epic.domain_concepts:
            from story_graph.domain import DomainConcept
            # Get original data to preserve realization field
            epic_data = None
            if name_to_data_map and epic.name in name_to_data_map:
                epic_data = name_to_data_map[epic.name]
            
            for dc in epic.domain_concepts:
                dc_dict = dc.to_dict()
                # Add realization from original data if it exists
                if epic_data and 'domain_concepts' in epic_data:
                    for orig_dc in epic_data['domain_concepts']:
                        if orig_dc.get('name') == dc.name and 'realization' in orig_dc:
                            dc_dict['realization'] = orig_dc['realization']
                domain_concepts_serialized.append(dc_dict)
        # Fallback: check original data if domain_concepts not loaded into object
        elif name_to_data_map and epic.name in name_to_data_map:
            epic_data = name_to_data_map[epic.name]
            if 'domain_concepts' in epic_data:
                domain_concepts_serialized = epic_data['domain_concepts']
        
        return {
            'name': epic.name,
            'behavior_needed': epic.behavior_needed,
            'domain_concepts': domain_concepts_serialized,
            'sub_epics': [self._serialize_sub_epic(child, name_to_data_map) for child in epic.children]
        }
    
    def _serialize_sub_epic(self, sub_epic, name_to_data_map=None) -> dict:
        """Serialize SubEpic object to dict by reading its properties."""
        from story_graph.nodes import SubEpic, Story, StoryGroup
        
        # Serialize domain_concepts if they exist in original data (SubEpic doesn't have domain_concepts as dataclass field)
        domain_concepts_serialized = []
        if name_to_data_map and sub_epic.name in name_to_data_map:
            sub_epic_data = name_to_data_map[sub_epic.name]
            if 'domain_concepts' in sub_epic_data:
                domain_concepts_raw = sub_epic_data['domain_concepts']
                if domain_concepts_raw:
                    # Already dictionaries from JSON, so use as-is (includes realization field)
                    domain_concepts_serialized = domain_concepts_raw
        
        result = {
            'name': sub_epic.name,
            'behavior_needed': sub_epic.behavior_needed,
            'behaviors_needed': sub_epic.behaviors_needed if hasattr(sub_epic, 'behaviors_needed') else [sub_epic.behavior_needed],
            'test_file': sub_epic.test_file if hasattr(sub_epic, 'test_file') else None,
            'test_class': sub_epic.test_class if hasattr(sub_epic, 'test_class') else None,
            'sub_epics': [],
            'story_groups': []
        }
        
        # Add domain_concepts if they were found
        if domain_concepts_serialized:
            result['domain_concepts'] = domain_concepts_serialized
        
        # Collect nested sub-epics and story groups
        current_story_group = None
        for child in sub_epic.children:
            if isinstance(child, SubEpic):
                result['sub_epics'].append(self._serialize_sub_epic(child, name_to_data_map))
            elif isinstance(child, StoryGroup):
                result['story_groups'].append(self._serialize_story_group(child))
            elif isinstance(child, Story):
                # Direct story child - add to unnamed story group
                if current_story_group is None:
                    current_story_group = {'name': None, 'stories': []}
                    result['story_groups'].append(current_story_group)
                current_story_group['stories'].append(self._serialize_story(child))
        
        return result
    
    def _serialize_story_group(self, story_group) -> dict:
        """Serialize StoryGroup object to dict."""
        return {
            'name': story_group.name if hasattr(story_group, 'name') else None,
            'stories': [self._serialize_story(story) for story in story_group.children]
        }
    
    def _serialize_story(self, story) -> dict:
        """Serialize Story object to dict by reading its properties."""
        return {
            'name': story.name,
            'behavior_needed': story.behavior_needed,
            'behaviors_needed': story.behaviors_needed if hasattr(story, 'behaviors_needed') else [story.behavior_needed],
            'test_file': story.test_file if hasattr(story, 'test_file') else None,
            'test_class': story.test_class if hasattr(story, 'test_class') else None,
            'acceptance_criteria': [self._serialize_ac(ac) for ac in story.acceptance_criteria],
            'scenarios': [self._serialize_scenario(sc) for sc in story.scenarios]
        }
    
    def _serialize_ac(self, ac) -> dict:
        """Serialize AcceptanceCriteria object."""
        return {
            'name': ac.name,
            'text': ac.name,
            'sequential_order': ac.sequential_order
        }
    
    def _serialize_scenario(self, scenario) -> dict:
        """Serialize Scenario object to dict by reading its properties."""
        # Serialize background steps
        background_steps = []
        if hasattr(scenario, 'background'):
            for step in scenario.background:
                if isinstance(step, str):
                    background_steps.append(step)
                else:
                    background_steps.append(self._serialize_step(step))
        
        # Serialize main steps
        main_steps = []
        if hasattr(scenario, 'steps'):
            for step in scenario.steps:
                if isinstance(step, str):
                    main_steps.append(step)
                else:
                    main_steps.append(self._serialize_step(step))
        
        return {
            'name': scenario.name,
            'behavior_needed': scenario.behavior_needed,
            'test_method': scenario.test_method if hasattr(scenario, 'test_method') else None,
            'type': scenario.type if hasattr(scenario, 'type') else '',
            'sequential_order': scenario.sequential_order,
            'background': background_steps,
            'steps': main_steps,
            'examples': scenario.examples if hasattr(scenario, 'examples') else None
        }
    
    def _serialize_step(self, step) -> dict:
        """Serialize Step object to dict."""
        return {
            'text': step.text,
            'sequential_order': step.sequential_order
        }
    
    def deserialize(self, data: str) -> dict:
        from utils import sanitize_json_string
        try:
            # Try parsing as-is first
            return json.loads(data)
        except ValueError as e:
            # If parsing fails due to control characters, sanitize and retry
            if 'control character' in str(e).lower() or 'Invalid' in str(e):
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"[JSONStoryGraph] JSON parse error, sanitizing and retrying: {str(e)}")
                sanitized = sanitize_json_string(data)
                return json.loads(sanitized)
            raise
