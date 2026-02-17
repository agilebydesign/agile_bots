
import json
from pathlib import Path
from typing import Optional

from cli.adapters import JSONAdapter
from story_graph.story_graph import StoryGraph

class JSONStoryGraph(JSONAdapter):
    
    # Level sets for include_level filtering (None = include all, skip checks)
    _LEVEL_DOMAIN = frozenset(['domain_concepts', 'acceptance', 'scenarios', 'examples', 'tests', 'code'])
    _LEVEL_ACCEPTANCE = frozenset(['acceptance', 'scenarios', 'examples', 'tests', 'code'])
    _LEVEL_SCENARIOS = frozenset(['scenarios', 'examples', 'tests', 'code'])
    _LEVEL_EXAMPLES = frozenset(['examples', 'tests', 'code'])
    _LEVEL_TESTS = frozenset(['tests', 'code'])
    
    def __init__(self, story_graph: StoryGraph):
        self.story_graph = story_graph
    
    @staticmethod
    def _level_includes(level_set: frozenset, include_level: Optional[str]) -> bool:
        """Return True when include_level is None (include all) or when include_level is in level_set."""
        return include_level is None or include_level in level_set
    
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
    
    def to_dict(self, include_level: Optional[str] = 'examples', generate_trace: bool = False) -> dict:
        """
        Serialize story graph with optional filtering by include_level.
        
        Args:
            include_level: One of 'stories', 'domain_concepts', 'acceptance', 
                          'scenarios', 'examples', 'tests', 'code'. Pass None to
                          include full content without level checks (faster).
            generate_trace: When True and include_level is 'tests' or 'code', add trace
                          to scenarios. Expensive - only set for instructions, not panel.
        """
        import time
        t0 = time.perf_counter()
        # Load domain objects and serialize them directly
        from story_graph.nodes import StoryMap
        story_map = StoryMap(self.story_graph.content, bot=None)
        t1 = time.perf_counter()
        
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
        
        # Create one TraceGenerator when generating trace (build index once, reuse across all scenarios)
        trace_generator = None
        if generate_trace and include_level in ('tests', 'code'):
            from traceability.trace_generator import TraceGenerator
            trace_generator = TraceGenerator(self.story_graph._workspace_directory, max_depth=1)
            trace_generator._build_method_index()
        
        # Serialize domain objects to JSON with include_level filtering
        content = {
            'epics': [self._serialize_epic(epic, epic_name_to_data, include_level, generate_trace, trace_generator) for epic in story_map._epics]
        }
        t2 = time.perf_counter()
        import sys
        msg = f"[PERF] json_story_graph StoryMap build: {(t1-t0)*1000:.0f}ms | serialize epics: {(t2-t1)*1000:.0f}ms"
        print(msg, file=sys.stderr, flush=True)
        try:
            wp = getattr(self.story_graph, '_workspace_directory', None)
            if wp:
                (wp / '.cursor').mkdir(parents=True, exist_ok=True)
                from datetime import datetime
                with open(wp / '.cursor' / 'panel-perf.log', 'a', encoding='utf-8') as f:
                    f.write(f"{datetime.now().isoformat()} {msg}\n")
        except Exception:
            pass
        
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
    
    def _serialize_epic(self, epic, name_to_data_map=None, include_level='examples', generate_trace=False, trace_generator=None) -> dict:
        """Serialize Epic object to dict by reading its properties with include_level filtering."""
        result = {
            'name': epic.name,
            'behavior_needed': epic.behavior_needed,
            'sub_epics': [self._serialize_sub_epic(child, name_to_data_map, include_level, generate_trace, trace_generator) for child in epic.children]
        }
        
        # Include domain_concepts if level >= 'domain_concepts'
        if self._level_includes(self._LEVEL_DOMAIN, include_level):
            # Serialize domain_concepts (Epic has DomainConcept objects)
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
            
            result['domain_concepts'] = domain_concepts_serialized
        
        return result
    
    def _serialize_sub_epic(self, sub_epic, name_to_data_map=None, include_level='examples', generate_trace=False, trace_generator=None) -> dict:
        """Serialize SubEpic object to dict by reading its properties with include_level filtering."""
        from story_graph.nodes import SubEpic, Story, StoryGroup
        
        result = {
            'name': sub_epic.name,
            'behavior_needed': sub_epic.behavior_needed,
            'behaviors_needed': sub_epic.behaviors_needed if hasattr(sub_epic, 'behaviors_needed') else [sub_epic.behavior_needed],
            'test_file': sub_epic.test_file if hasattr(sub_epic, 'test_file') else None,
            'test_class': sub_epic.test_class if hasattr(sub_epic, 'test_class') else None,
            'sub_epics': [],
            'story_groups': []
        }
        
        # Include domain_concepts if level >= 'domain_concepts'
        if self._level_includes(self._LEVEL_DOMAIN, include_level):
            # Serialize domain_concepts if they exist in original data (SubEpic doesn't have domain_concepts as dataclass field)
            domain_concepts_serialized = []
            if name_to_data_map and sub_epic.name in name_to_data_map:
                sub_epic_data = name_to_data_map[sub_epic.name]
                if 'domain_concepts' in sub_epic_data:
                    domain_concepts_raw = sub_epic_data['domain_concepts']
                    if domain_concepts_raw:
                        # Already dictionaries from JSON, so use as-is (includes realization field)
                        domain_concepts_serialized = domain_concepts_raw
            
            # Add domain_concepts if they were found
            if domain_concepts_serialized:
                result['domain_concepts'] = domain_concepts_serialized
        
        # Collect nested sub-epics and story groups
        current_story_group = None
        for child in sub_epic.children:
            if isinstance(child, SubEpic):
                result['sub_epics'].append(self._serialize_sub_epic(child, name_to_data_map, include_level, generate_trace, trace_generator))
            elif isinstance(child, StoryGroup):
                result['story_groups'].append(self._serialize_story_group(child, include_level, generate_trace, trace_generator))
            elif isinstance(child, Story):
                # Direct story child - add to unnamed story group
                if current_story_group is None:
                    current_story_group = {'name': None, 'stories': []}
                    result['story_groups'].append(current_story_group)
                current_story_group['stories'].append(self._serialize_story(child, include_level, generate_trace, trace_generator))
        
        return result
    
    def _serialize_story_group(self, story_group, include_level='examples', generate_trace=False, trace_generator=None) -> dict:
        """Serialize StoryGroup object to dict with include_level filtering."""
        return {
            'name': story_group.name if hasattr(story_group, 'name') else None,
            'stories': [self._serialize_story(story, include_level, generate_trace, trace_generator) for story in story_group.children]
        }
    
    def _serialize_story(self, story, include_level='examples', generate_trace=False, trace_generator=None) -> dict:
        """Serialize Story object to dict by reading its properties with include_level filtering."""
        result = {
            'name': story.name,
            'behavior_needed': story.behavior_needed,
            'behaviors_needed': story.behaviors_needed if hasattr(story, 'behaviors_needed') else [story.behavior_needed],
            'test_file': story.test_file if hasattr(story, 'test_file') else None,
            'test_class': story.test_class if hasattr(story, 'test_class') else None,
        }
        
        # Include acceptance criteria only if level >= 'acceptance'
        if self._level_includes(self._LEVEL_ACCEPTANCE, include_level):
            result['acceptance_criteria'] = [self._serialize_ac(ac) for ac in story.acceptance_criteria]
        
        # Include scenarios only if level >= 'scenarios'
        if self._level_includes(self._LEVEL_SCENARIOS, include_level):
            result['scenarios'] = [self._serialize_scenario(sc, include_level, story, generate_trace, trace_generator) for sc in story.scenarios]
        
        return result
    
    def _serialize_ac(self, ac) -> dict:
        """Serialize AcceptanceCriteria object."""
        return {
            'name': ac.name,
            'text': ac.name,
            'sequential_order': ac.sequential_order
        }
    
    def _serialize_scenario(self, scenario, include_level='examples', story=None, generate_trace=False, trace_generator=None) -> dict:
        """Serialize Scenario object to dict by reading its properties with include_level filtering."""
        result = {
            'name': scenario.name,
            'behavior_needed': scenario.behavior_needed,
            'test_method': scenario.test_method if hasattr(scenario, 'test_method') else None,
            'type': scenario.type if hasattr(scenario, 'type') else '',
            'sequential_order': scenario.sequential_order,
        }
        
        # Serialize background steps (if level >= 'scenarios')
        if self._level_includes(self._LEVEL_SCENARIOS, include_level):
            background_steps = []
            if hasattr(scenario, 'background'):
                for step in scenario.background:
                    if isinstance(step, str):
                        background_steps.append(step)
                    else:
                        background_steps.append(self._serialize_step(step))
            result['background'] = background_steps
            
            # Serialize main steps
            main_steps = []
            if hasattr(scenario, 'steps'):
                for step in scenario.steps:
                    if isinstance(step, str):
                        main_steps.append(step)
                    else:
                        main_steps.append(self._serialize_step(step))
            result['steps'] = main_steps
        
        # Include examples only if level >= 'examples'
        if self._level_includes(self._LEVEL_EXAMPLES, include_level):
            result['examples'] = scenario.examples if hasattr(scenario, 'examples') else None
        
        # Include test code if level >= 'tests'
        if self._level_includes(self._LEVEL_TESTS, include_level) and story:
            test_code_data = self._generate_test_code(scenario, story)
            if test_code_data:
                result['test'] = test_code_data
        
        # Include trace only when generate_trace=True (instructions path) and level is tests/code
        if generate_trace and include_level in ('tests', 'code') and story and trace_generator:
            trace_data = self._generate_trace(scenario, story, trace_generator)
            result['trace'] = trace_data if trace_data else []
        
        return result
    
    def _serialize_step(self, step) -> dict:
        """Serialize Step object to dict."""
        return {
            'text': step.text,
            'sequential_order': step.sequential_order
        }
    
    def _get_story_test_file(self, story) -> Optional[str]:
        """Get test_file from parent SubEpic (story.test_file is always None - never look there)."""
        parent = getattr(story, '_parent', None)
        while parent:
            if hasattr(parent, 'test_file') and parent.test_file:
                return parent.test_file
            parent = getattr(parent, '_parent', None)
        return None
    
    def _resolve_test_file_path(self, test_file: str) -> Path:
        """Resolve test_file (relative to test dir) to absolute path."""
        test_dir = self.story_graph._workspace_directory / getattr(
            self.story_graph._bot_paths, 'test_path', Path('test')
        )
        return test_dir / test_file
    
    def _generate_test_code(self, scenario, story) -> Optional[dict]:
        """Extract test method code for scenario.
        
        Args:
            scenario: Scenario object with test_method
            story: Parent Story object with test_class (test_file from parent SubEpic)
        
        Returns:
            Dict with test method code, file, and line number, or None if not found
        """
        if not hasattr(scenario, 'test_method') or not scenario.test_method:
            return None
        
        test_file = self._get_story_test_file(story)
        if not test_file:
            return None
        
        if not hasattr(story, 'test_class') or not story.test_class:
            return None
        
        test_file_path = self._resolve_test_file_path(test_file)
        if not test_file_path.exists():
            return None
        
        try:
            from traceability.trace_generator import TraceGenerator
            generator = TraceGenerator(self.story_graph._workspace_directory, max_depth=3)
            
            source = test_file_path.read_text(encoding='utf-8')
            lines = source.split('\n')
            
            code, start, end = generator._extract_method_from_class(
                source, lines, story.test_class, scenario.test_method
            )
            
            if code:
                return {
                    'method': scenario.test_method,
                    'file': str(test_file),
                    'line': start,
                    'code': code
                }
        except Exception:
            pass
        
        return None
    
    def _generate_trace(self, scenario, story, trace_generator) -> list:
        """Generate trace for scenario using shared trace generator (shallow: file/line/symbol only).
        
        Args:
            scenario: Scenario object with test_method
            story: Parent Story object with test_class (test_file from parent SubEpic)
            trace_generator: Pre-built TraceGenerator (index already built, reused across scenarios)
        
        Returns:
            List of trace sections: file, line, symbol (no code, no children for speed)
        """
        if not hasattr(scenario, 'test_method') or not scenario.test_method:
            return []
        
        test_file = self._get_story_test_file(story)
        if not test_file:
            return []
        
        if not hasattr(story, 'test_class') or not story.test_class:
            return []
        
        try:
            # Get test code (test_file is relative to test dir)
            test_file_path = self._resolve_test_file_path(test_file)
            if not test_file_path.exists():
                return []
            
            source = test_file_path.read_text(encoding='utf-8')
            lines = source.split('\n')
            
            # Extract test method
            test_code, test_start, test_end = trace_generator._extract_method_from_class(
                source, lines, story.test_class, scenario.test_method
            )
            
            if not test_code:
                return []
            
            # Analyze for calls
            calls = trace_generator._find_calls_in_code(test_code)
            
            # Build trace (shallow: file/line/symbol only, no code/children)
            trace_sections = []
            for call in calls:
                section = trace_generator._resolve_call(call, depth=1, shallow=True)
                if section:
                    trace_sections.append(section)
            
            return trace_sections
            
        except Exception:
            return []
    
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
