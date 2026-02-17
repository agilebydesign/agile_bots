
import json
import re
from typing import Optional
from pathlib import Path
from cli.adapters import JSONAdapter
from scope.scope import Scope

class JSONScope(JSONAdapter):
    
    def __init__(self, scope: Scope):
        self.scope = scope
    
    @property
    def type(self):
        return self.scope.type
    
    @property
    def value(self):
        return self.scope.value
    
    @property
    def exclude(self):
        return self.scope.exclude
    
    @property
    def skiprule(self):
        return self.scope.skiprule
    
    @property
    def story_graph_filter(self):
        return self.scope.story_graph_filter
    
    @property
    def file_filter(self):
        return self.scope.file_filter
    
    def to_dict(self, apply_include_level: bool = False, strip_links_for_instructions: bool = False) -> dict:
        """
        Serialize scope to dict.
        
        Args:
            apply_include_level: When True, filter content by scope.include_level (for instructions
                injection and clipboard copy). When False, include full content without level checks
                (faster - use this when level filtering is not needed).
            strip_links_for_instructions: When True, remove links/test_files arrays from content
                (for instructions injection - keeps prompt lean; panel display keeps links).
        """
        result = {
            'type': self.scope.type.value,
            'filter': ', '.join(self.scope.value) if self.scope.value else '',
            'content': None,
            'graphLinks': [],
            'includeLevel': self.scope.include_level
        }
        
        if self.scope.type.value in ('story', 'showAll'):
            import time
            t0 = time.perf_counter()
            story_graph = self.scope._get_story_graph_results()
            t1 = time.perf_counter()
            if story_graph:
                # Check if we can use disk-cached enriched content
                # Only use cache when there's no active filter (showAll or story with no filter values)
                has_active_filter = self.scope.type.value == 'story' and self.scope.value
                
                # Use centralized path resolution
                if self.scope.bot_paths:
                    story_graph_path = self.scope.bot_paths.story_graph_paths.story_graph_path
                    cache_path = self.scope.bot_paths.story_graph_paths.story_graph_cache_path
                else:
                    story_graph_path = self.scope.workspace_directory / 'docs' / 'story' / 'story-graph.json'
                    cache_path = self.scope.workspace_directory / 'docs' / 'story' / '.story-graph-enriched-cache.json'
                
                content = None
                # CACHE DISABLED - Always regenerate to ensure behaviors are current
                # if not has_active_filter and story_graph_path.exists() and cache_path.exists():
                #     # Check if cache is still valid (cache mtime > source mtime)
                #     source_mtime = story_graph_path.stat().st_mtime
                #     cache_mtime = cache_path.stat().st_mtime
                #     
                #     if cache_mtime >= source_mtime:
                #         # Cache is valid - load it
                #         try:
                #             with open(cache_path, 'r', encoding='utf-8') as f:
                #                 content = json.load(f)
                #         except Exception:
                #             # Cache corrupted, regenerate
                #             content = None
                
                if content is None:
                    # Generate and enrich content (cache miss or invalid)
                    from story_graph.json_story_graph import JSONStoryGraph
                    graph_adapter = JSONStoryGraph(story_graph)
                    # Panel/scope view: use examples (fast, no trace). Instructions: use scope.include_level
                    include_level = self.scope.include_level if apply_include_level else 'examples'
                    # Trace is expensive - only for instructions when level is tests/code
                    generate_trace = strip_links_for_instructions and include_level in ('tests', 'code')
                    content = graph_adapter.to_dict(include_level=include_level, generate_trace=generate_trace).get('content', [])
                    t2 = time.perf_counter()
                    import sys
                    msg = f"[PERF] json_scope story_graph load: {(t1-t0)*1000:.0f}ms | graph.to_dict: {(t2-t1)*1000:.0f}ms"
                    print(msg, file=sys.stderr, flush=True)
                    try:
                        wp = getattr(self.scope, 'workspace_directory', None)
                        if wp:
                            (wp / '.cursor').mkdir(parents=True, exist_ok=True)
                            from datetime import datetime
                            with open(wp / '.cursor' / 'panel-perf.log', 'a', encoding='utf-8') as f:
                                f.write(f"{datetime.now().isoformat()} {msg}\n")
                    except Exception:
                        pass
                    
                    if content and 'epics' in content:
                        # Skip enrichment entirely for panel (no links, no filesystem scans)
                        if apply_include_level or strip_links_for_instructions:
                            enrich_scenarios = include_level in ('tests', 'code')
                            self._enrich_with_links(content['epics'], story_graph, enrich_scenarios)
                        if strip_links_for_instructions:
                            self._strip_links(content['epics'])
                        
                        # CACHE DISABLED - Don't write cache file
                        # # Write to disk cache only when there's no active filter
                        # if not has_active_filter:
                        #     try:
                        #         with open(cache_path, 'w', encoding='utf-8') as f:
                        #             json.dump(content, f, indent=2, ensure_ascii=False)
                        #     except Exception:
                        #         pass  # If cache write fails, just continue without it
                    else:
                        content = {'epics': []}
                
                result['content'] = content
                
                if self.scope.bot_paths:
                    # Use centralized path resolution for story map file
                    story_graph_paths = self.scope.bot_paths.story_graph_paths
                    # Story map is in the shape behavior folder
                    story_map_file = story_graph_paths.behavior_path('shape') / 'story-map.md'
                    if story_map_file.exists():
                        result['graphLinks'].append({
                            'text': 'map',
                            'url': str(story_map_file)
                        })
        elif self.scope.type.value == 'files':
            files = self.scope._get_file_results()
            result['content'] = [{'path': str(f)} for f in files]
        
        return result
    
    # For instructions: only keep name + structure from epic to story (stories level = name only)
    _EPIC_KEEP = frozenset(['name', 'sub_epics', 'domain_concepts'])
    _SUB_EPIC_KEEP = frozenset(['name', 'sub_epics', 'story_groups', 'domain_concepts'])
    _STORY_GROUP_KEEP = frozenset(['name', 'stories'])
    _STORY_KEEP = frozenset(['name', 'acceptance_criteria', 'scenarios'])
    _SCENARIO_KEEP = frozenset(['name', 'background', 'steps', 'examples', 'test', 'trace'])
    
    def _strip_links(self, epics: list) -> None:
        """For instructions: keep only name (+ structure) from epic to story."""
        for epic in epics:
            self._keep_only(epic, self._EPIC_KEEP)
            for sub_epic in epic.get('sub_epics', []):
                self._strip_sub_epic(sub_epic)
    
    def _strip_sub_epic(self, sub_epic: dict) -> None:
        self._keep_only(sub_epic, self._SUB_EPIC_KEEP)
        for nested in sub_epic.get('sub_epics', []):
            self._strip_sub_epic(nested)
        for story_group in sub_epic.get('story_groups', []):
            self._keep_only(story_group, self._STORY_GROUP_KEEP)
            for story in story_group.get('stories', []):
                self._keep_only(story, self._STORY_KEEP)
                for scenario in story.get('scenarios', []):
                    self._keep_only(scenario, self._SCENARIO_KEEP)
    
    def _keep_only(self, node: dict, allowed: frozenset) -> None:
        """Remove all keys not in allowed."""
        for key in list(node.keys()):
            if key not in allowed:
                del node[key]
    
    def _enrich_with_links(self, epics: list, story_graph, enrich_scenarios: bool = True):
        if not self.scope.workspace_directory or not self.scope.bot_paths:
            return
        
        test_dir = self.scope.workspace_directory / self.scope.bot_paths.test_path
        # Use centralized path resolution - scenarios are in the scenarios behavior folder
        scenarios_path = self.scope.bot_paths.story_graph_paths.scenarios_path
        exploration_path = self.scope.bot_paths.story_graph_paths.behavior_path('exploration')
        
        for epic in epics:
            epic_folder = scenarios_path / f"🎯 {epic['name']}"
            exploration_doc = self._get_exploration_doc_path(exploration_path, epic['name'])
            if exploration_doc or (epic_folder.exists() and epic_folder.is_dir()):
                if 'links' not in epic:
                    epic['links'] = []
                epic['links'].append({
                    'text': 'docs',
                    'url': str(exploration_doc or epic_folder),
                    'icon': 'document'
                })
            
            if 'sub_epics' in epic:
                for sub_epic in epic['sub_epics']:
                    self._enrich_sub_epic_with_links(
                        sub_epic,
                        test_dir,
                        scenarios_path,
                        epic['name'],
                        parent_sub_epic_name=None,
                        enrich_scenarios=enrich_scenarios
                    )
    
    def _enrich_sub_epic_with_links(
        self,
        sub_epic: dict,
        test_dir: Path,
        scenarios_path: Path,
        epic_name: str,
        parent_path: str = None,
        parent_sub_epic_name: Optional[str] = None,
        enrich_scenarios: bool = True
    ):
        if parent_path:
            sub_epic_doc_folder = Path(parent_path) / f"⚙️ {sub_epic['name']}"
        else:
            sub_epic_doc_folder = scenarios_path / f"🎯 {epic_name}" / f"⚙️ {sub_epic['name']}"
        
        if 'links' not in sub_epic:
            sub_epic['links'] = []
        
        # Multi-language, multi-file test discovery: find all files that partially match (e.g. test_some_sub_epic*.py, *.js)
        from utils import find_matching_test_files, name_to_test_stem
        import re
        primary_test_file = sub_epic.get('test_file') or ''
        if primary_test_file:
            p = Path(primary_test_file)
            stem = p.stem
            # Strip tier suffix (_server, _client, _e2e) and test suffix (.test, .spec) for pattern matching
            # e.g. "select-recipient_e2e.spec" -> "select-recipient"
            pattern = re.sub(r'(_server|_client|_e2e)?(\.test|\.spec)?$', '', stem)
            under_path = str(p.parent) if str(p.parent) != '.' else None
        else:
            pattern = name_to_test_stem(sub_epic.get('name') or '')
            under_path = None
        matching_rel = find_matching_test_files(test_dir, pattern, under_path or None)
        sub_epic['test_files'] = [str(test_dir / r) for r in matching_rel]
        if 'test_file' in sub_epic and sub_epic['test_file']:
            test_file_path = test_dir / sub_epic['test_file']
            if test_file_path.exists():
                sub_epic['links'].append({
                    'text': 'test',
                    'url': str(test_file_path),
                    'icon': 'test_tube'
                })
        
        exploration_path = self.scope.bot_paths.story_graph_paths.behavior_path('exploration') if self.scope.bot_paths else None
        exploration_doc = self._get_first_exploration_doc(
            exploration_path,
            [sub_epic['name'], parent_sub_epic_name, epic_name]
        )
        if exploration_doc or (sub_epic_doc_folder.exists() and sub_epic_doc_folder.is_dir()):
            sub_epic['links'].append({
                'text': 'docs',
                'url': str(exploration_doc or sub_epic_doc_folder),
                'icon': 'document'
            })
        
        if 'sub_epics' in sub_epic:
            for nested_sub_epic in sub_epic['sub_epics']:
                self._enrich_sub_epic_with_links(
                    nested_sub_epic,
                    test_dir,
                    scenarios_path,
                    epic_name,
                    str(sub_epic_doc_folder),
                    parent_sub_epic_name=sub_epic['name'],
                    enrich_scenarios=enrich_scenarios
                )
        
        if 'story_groups' in sub_epic:
            for story_group in sub_epic['story_groups']:
                if 'stories' in story_group:
                    for story in story_group['stories']:
                        self._enrich_story_with_links(
                            story, test_dir, sub_epic_doc_folder,
                            sub_epic.get('test_file'),
                            sub_epic.get('test_files') or [],
                            enrich_scenarios=enrich_scenarios
                        )

    def _get_exploration_doc_path(self, exploration_path: Optional[Path], node_name: str) -> Optional[Path]:
        if not exploration_path:
            return None
        slug = re.sub(r'[^a-z0-9]+', '-', node_name.lower()).strip('-')
        if not slug:
            return None
        candidate = exploration_path / f"{slug}-exploration.md"
        return candidate if candidate.exists() else None

    def _get_first_exploration_doc(self, exploration_path: Optional[Path], node_names: list) -> Optional[Path]:
        if not exploration_path:
            return None
        for name in node_names:
            if not name:
                continue
            candidate = self._get_exploration_doc_path(exploration_path, name)
            if candidate:
                return candidate
        return None
    
    def _enrich_story_with_links(
        self,
        story: dict,
        test_dir: Path,
        parent_doc_folder: Path,
        parent_test_file: str,
        parent_test_files: list,
        enrich_scenarios: bool = True,
    ):
        if 'links' not in story:
            story['links'] = []
        
        story_doc_file = parent_doc_folder / f"📄 {story['name']}.md"
        if story_doc_file.exists():
            story['links'].append({
                'text': 'story',
                'url': str(story_doc_file),
                'icon': 'document'
            })
        
        # test_file ALWAYS comes from parent sub-epic, never from the story itself
        test_file = parent_test_file
        test_class = story.get('test_class')
        story['test_files'] = parent_test_files  # all matching test files (multi-language) for "open all"
        
        # Create test links for ALL matching test files (front, back, e2e)
        if test_class and parent_test_files:
            from utils import find_js_test_class_line, find_test_class_line
            for test_file_rel in parent_test_files:
                test_file_path = Path(test_file_rel)
                if test_file_path.exists():
                    # Use JS-specific function for .js/.ts/.tsx files, Python AST for .py files
                    if test_file_path.suffix in ('.js', '.ts', '.tsx'):
                        line_number = find_js_test_class_line(test_file_path, test_class)
                    else:
                        line_number = find_test_class_line(test_file_path, test_class)
                    
                    if line_number:
                        test_url = f"{test_file_path}#L{line_number}"
                        story['links'].append({
                            'text': 'test',
                            'url': test_url,
                            'icon': 'test_tube'
                        })
        
        # Only enrich scenarios if requested (skip for 'scope showall' to avoid expensive AST parsing)
        if enrich_scenarios and 'scenarios' in story:
            for scenario in story['scenarios']:
                self._enrich_scenario_with_links(scenario, test_dir, test_file, test_class, parent_test_files)
    
    def _enrich_scenario_with_links(
        self,
        scenario: dict,
        test_dir: Path,
        story_test_file: str,
        story_test_class: str,
        story_test_files: list,
    ):
        test_method = scenario.get('test_method')
        scenario['test_files'] = story_test_files  # all matching test files for "open all"
        if story_test_file and test_method:
            test_file_path = test_dir / story_test_file
            if test_file_path.exists():
                # Use JS-specific function for .js files, Python AST for .py files
                if test_file_path.suffix == '.js':
                    from utils import find_js_test_method_line
                    line_number = find_js_test_method_line(test_file_path, test_method)
                else:
                    from utils import find_test_method_line
                    line_number = find_test_method_line(test_file_path, test_method)
                if line_number:
                    scenario['test_file'] = f"{test_file_path}#L{line_number}"
    
    def deserialize(self, data: str) -> dict:
        return json.loads(data)
