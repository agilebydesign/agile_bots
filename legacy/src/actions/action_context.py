"""Typed action context classes for type-safe CLI parameter handling.

This module defines the ActionContext hierarchy - typed dataclasses that replace
Dict[str, Any] parameters. Each action declares which context class it uses,
enabling type-safe parameter passing from CLI to action.execute().

The CLI parser generator reads these context classes to generate argument parsers.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from pathlib import Path
from enum import Enum


class ScopeType(Enum):
    ALL = 'all'
    SHOW_ALL = 'showAll'
    STORY = 'story'
    EPIC = 'epic'
    INCREMENT = 'increment'
    FILES = 'files'


class ValidationType(Enum):
    """Type of content a behavior validates by default."""
    STORY_GRAPH = 'story_graph'  # Validates story graph only
    FILES = 'files'  # Validates files only
    BOTH = 'both'  # Validates both story graph and files


@dataclass
class KnowledgeGraphFilter:
    """Filters content by knowledge graph nodes (stories, epics, increments).
    
    Used for filtering operations to specific parts of the story graph.
    """
    stories: List[str] = field(default_factory=list)
    epics: List[str] = field(default_factory=list)
    increments: List[int] = field(default_factory=list)
    
    def matches_story(self, story_name: str) -> bool:
        """Check if story matches filter."""
        if not self.stories:
            return True
        return story_name in self.stories
    
    def matches_epic(self, epic_name: str) -> bool:
        """Check if epic matches filter."""
        if not self.epics:
            return True
        return epic_name in self.epics
    
    def filter_knowledge_graph(self, knowledge_graph: Dict[str, Any]) -> Dict[str, Any]:
        """Filter knowledge graph to only nodes matching this filter.
        
        Searches ALL levels (epics, sub-epics, stories) regardless of filter type,
        matching the behavior of the text display output.
        """
        # Return full graph if no filters specified
        if not self.stories and not self.epics and not self.increments:
            return knowledge_graph
        
        # Collect all filter names (stories + epics) into one list for flexible matching
        all_filter_names = list(self.stories) + list(self.epics)
        
        def name_matches(name: str) -> bool:
            """Check if a name matches any filter value (case-insensitive partial match)."""
            return any(filter_name.lower() in name.lower() for filter_name in all_filter_names)
        
        filtered_graph = {'epics': []}
        epics = knowledge_graph.get('epics', [])
        
        for epic in epics:
            epic_name = epic.get('name', '')
            
            # Check if this epic matches - if so, include entire epic
            if name_matches(epic_name):
                filtered_graph['epics'].append(epic)
                continue
            
            # Check sub-epics and stories
            filtered_sub_epics = []
            for sub_epic in epic.get('sub_epics', []):
                sub_epic_name = sub_epic.get('name', '')
                
                # Check if sub-epic matches - if so, include entire sub-epic
                if name_matches(sub_epic_name):
                    filtered_sub_epics.append(sub_epic)
                    continue
                
                # Check if any story matches
                matching_story_groups = []
                for story_group in sub_epic.get('story_groups', []):
                    matching_stories = []
                    for story in story_group.get('stories', []):
                        if name_matches(story.get('name', '')):
                            matching_stories.append(story)
                    
                    if matching_stories:
                        matching_story_groups.append({
                            **story_group,
                            'stories': matching_stories
                        })
                
                # Also check stories at sub-epic level
                matching_direct_stories = []
                for story in sub_epic.get('stories', []):
                    if name_matches(story.get('name', '')):
                        matching_direct_stories.append(story)
                
                # Include sub-epic if we found matching stories
                if matching_story_groups or matching_direct_stories:
                    filtered_sub_epic = {**sub_epic}
                    if matching_story_groups:
                        filtered_sub_epic['story_groups'] = matching_story_groups
                    if matching_direct_stories:
                        filtered_sub_epic['stories'] = matching_direct_stories
                    filtered_sub_epics.append(filtered_sub_epic)
            
            # Include epic if we found matching sub-epics or stories
            if filtered_sub_epics:
                filtered_epic = {**epic, 'sub_epics': filtered_sub_epics}
                filtered_graph['epics'].append(filtered_epic)
        
        return filtered_graph


@dataclass
class FileFilter:
    """Filters files by path patterns.
    
    Supports glob patterns for include/exclude.
    """
    include_patterns: List[str] = field(default_factory=list)
    exclude_patterns: List[str] = field(default_factory=list)
    
    def matches_file(self, file_path: Path) -> bool:
        """Check if file matches the filter.
        
        Note: This method performs simple substring matching. For full glob pattern
        matching, use filter_files() which implements complete glob pattern support.
        """
        if not self.include_patterns:
            return True
        file_str = str(file_path)
        for pattern in self.include_patterns:
            if pattern in file_str:
                return True
        return False
    
    def filter_files(self, file_list: List[Path]) -> List[Path]:
        """Filter file list to only files matching this filter."""
        if not self.include_patterns and not self.exclude_patterns:
            return file_list
        
        from pathlib import PurePath
        filtered = []
        
        for file_path in file_list:
            file_str = str(file_path).replace('\\', '/')
            file_path_obj = PurePath(file_str)
            
            if self.include_patterns:
                matches_include = False
                for pattern in self.include_patterns:
                    pattern_normalized = pattern.replace('\\', '/')
                    try:
                        if (file_path_obj.match(pattern_normalized) or
                            file_path_obj.match(f'**/{pattern_normalized}') or
                            pattern_normalized in file_str):
                            matches_include = True
                            break
                    except (ValueError, TypeError):
                        if pattern_normalized in file_str:
                            matches_include = True
                            break
                
                if not matches_include:
                    continue
            
            if self.exclude_patterns:
                matches_exclude = False
                for pattern in self.exclude_patterns:
                    pattern_normalized = pattern.replace('\\', '/')
                    try:
                        if (file_path_obj.match(pattern_normalized) or
                            file_path_obj.match(f'**/{pattern_normalized}')):
                            matches_exclude = True
                            break
                    except (ValueError, TypeError):
                        pass
                
                if matches_exclude:
                    continue
            
            filtered.append(file_path)
        
        return filtered


@dataclass
class Scope:
    """Scope for filtering bot operations to specific content.
    
    Uses KnowledgeGraphFilter for story/epic/increment scoping
    and FileFilter for file-based scoping. Maintains backward compatibility
    with type/value/exclude API.
    
    The Scope object is responsible for its own persistence to the bot state file.
    """
    type: ScopeType = ScopeType.ALL
    value: List[str] = field(default_factory=list)
    exclude: List[str] = field(default_factory=list)
    skiprule: List[str] = field(default_factory=list)
    
    # New filter objects
    _knowledge_graph_filter: Optional[KnowledgeGraphFilter] = field(default=None, repr=False)
    _file_filter: Optional[FileFilter] = field(default=None, repr=False)
    
    def __post_init__(self):
        """Initialize filter objects from type/value/exclude."""
        # Create knowledge graph filter for story/epic/increment types
        if self.type in (ScopeType.STORY, ScopeType.EPIC, ScopeType.INCREMENT):
            if self.type == ScopeType.STORY:
                self._knowledge_graph_filter = KnowledgeGraphFilter(stories=self.value)
            elif self.type == ScopeType.EPIC:
                self._knowledge_graph_filter = KnowledgeGraphFilter(epics=self.value)
            elif self.type == ScopeType.INCREMENT:
                # Convert string values to integers
                increments = [int(v) if isinstance(v, str) and v.isdigit() else v for v in self.value]
                self._knowledge_graph_filter = KnowledgeGraphFilter(increments=increments)
        
        # Create file filter for files type
        if self.type == ScopeType.FILES:
            self._file_filter = FileFilter(
                include_patterns=self.value,
                exclude_patterns=self.exclude
            )
    
    @property
    def knowledge_graph_filter(self) -> Optional[KnowledgeGraphFilter]:
        """Get knowledge graph filter (lazy init if needed)."""
        return self._knowledge_graph_filter
    
    @property
    def file_filter(self) -> Optional[FileFilter]:
        """Get file filter (lazy init if needed)."""
        return self._file_filter
    
    def filters_knowledge_graph(self, knowledge_graph: Dict[str, Any]) -> Dict[str, Any]:
        """Filter knowledge graph using knowledge graph filter."""
        if self._knowledge_graph_filter:
            return self._knowledge_graph_filter.filter_knowledge_graph(knowledge_graph)
        return knowledge_graph
    
    def filters_files(self, file_list: List[Path]) -> List[Path]:
        """Filter file list using file filter."""
        if self._file_filter:
            return self._file_filter.filter_files(file_list)
        return file_list
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Scope':
        if not data:
            return cls()
        
        scope_type_str = data.get('type', 'all')
        try:
            scope_type = ScopeType(scope_type_str)
        except ValueError:
            raise ValueError(f"Invalid scope type: '{scope_type_str}'. Valid types: {[t.value for t in ScopeType]}")
        
        return cls(
            type=scope_type,
            value=data.get('value', []) if isinstance(data.get('value'), list) else [data.get('value')] if data.get('value') else [],
            exclude=data.get('exclude', []) if isinstance(data.get('exclude'), list) else [data.get('exclude')] if data.get('exclude') else [],
            skiprule=data.get('skiprule', []) if isinstance(data.get('skiprule'), list) else [data.get('skiprule')] if data.get('skiprule') else [],
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type.value,
            'value': self.value,
            'exclude': self.exclude,
            'skiprule': self.skiprule,
        }
    
    def apply_to_bot(self, workspace_directory: 'Path') -> None:
        """Clear old scope and store this scope to the bot state file.
        
        The Scope object is responsible for its own persistence.
        """
        import json
        state_file = self._get_state_file_path(workspace_directory)
        
        # Read existing state or create new
        if state_file.exists():
            try:
                state_data = json.loads(state_file.read_text())
            except (json.JSONDecodeError, IOError):
                state_data = {}
        else:
            state_data = {}
        
        # Clear old scope and store new scope
        state_data['scope'] = self.to_dict()
        
        # Write back to file
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(json.dumps(state_data, indent=2))
    
    @staticmethod
    def clear_from_bot(workspace_directory: 'Path') -> None:
        """Remove scope from the bot state file."""
        import json
        state_file = Scope._get_state_file_path(workspace_directory)
        
        if not state_file.exists():
            return
        
        try:
            state_data = json.loads(state_file.read_text())
            if 'scope' in state_data:
                del state_data['scope']
                state_file.write_text(json.dumps(state_data, indent=2))
        except (json.JSONDecodeError, IOError):
            pass
    
    @staticmethod
    def _get_state_file_path(workspace_directory: 'Path') -> 'Path':
        """Get path to the bot state file."""
        return workspace_directory / 'behavior_action_state.json'
    
    def to_display_lines(self, workspace_directory: 'Path') -> List[str]:
        """Render scope as display lines with hierarchical expansion.
        
        Returns plain text lines showing scope filter and matched items.
        """
        from pathlib import Path
        import json
        
        lines = []
        
        # Show the scope filter value
        filter_str = ', '.join(self.value) if isinstance(self.value, list) else str(self.value)
        lines.append(f"Scope Filter: {filter_str}")
        
        if self.type == ScopeType.SHOW_ALL:
            # Display the entire story graph
            story_graph_path = workspace_directory / 'docs' / 'stories' / 'story-graph.json'
            if story_graph_path.exists():
                try:
                    graph_data = json.loads(story_graph_path.read_text(encoding='utf-8'))
                    # Format all epics with their children
                    epics = graph_data.get('epics', [])
                    for epic in epics:
                        epic_lines = self._format_node_with_children(epic, 'epic', 0, workspace_directory, graph_data, epic.get('name', ''), epic.get('name', ''))
                        lines.extend(epic_lines)
                except Exception:
                    lines.append("  - (error loading story graph)")
        elif self.type == ScopeType.STORY or self.type == ScopeType.EPIC:
            story_graph_path = workspace_directory / 'docs' / 'stories' / 'story-graph.json'
            if story_graph_path.exists():
                try:
                    graph_data = json.loads(story_graph_path.read_text(encoding='utf-8'))
                    # Use the SAME filtering as JSON output
                    filtered_graph = self.filters_knowledge_graph(graph_data)
                    # Format the filtered graph for display
                    for epic in filtered_graph.get('epics', []):
                        epic_lines = self._format_node_with_children(epic, 'epic', 0, workspace_directory, filtered_graph, epic.get('name', ''), epic.get('name', ''))
                        lines.extend(epic_lines)
                except Exception:
                    # Fallback to simple list
                    for item in (self.value if isinstance(self.value, list) else [self.value]):
                        lines.append(f"  - {item}")
            else:
                for item in (self.value if isinstance(self.value, list) else [self.value]):
                    lines.append(f"  - {item}")
        elif self.type == ScopeType.FILES:
            # Expand file paths to show all actual files that will be scanned
            expanded_files = self._expand_file_paths(workspace_directory)
            if expanded_files:
                for file_path in sorted(expanded_files):
                    # Show relative path from workspace
                    try:
                        rel_path = file_path.relative_to(workspace_directory)
                        lines.append(f"  - {rel_path}")
                    except ValueError:
                        lines.append(f"  - {file_path}")
            else:
                # Fallback to showing the scope value if expansion fails
                for item in (self.value if isinstance(self.value, list) else [self.value]):
                    lines.append(f"  - {item} (no files found)")
        else:
            if isinstance(self.value, list):
                for item in self.value:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"  - {self.value}")
        
        return lines
    
    def _expand_file_paths(self, workspace_directory: 'Path') -> List['Path']:
        """Expand file scope paths to actual files that will be scanned."""
        from pathlib import Path
        import glob as glob_module
        
        all_files = []
        # Ensure value is treated as a list
        paths = self.value if isinstance(self.value, list) else [self.value]
        
        for path_str in paths:
            # Check if path contains glob patterns
            has_glob = any(char in path_str for char in ['*', '?', '['])
            
            if has_glob:
                # Handle glob patterns
                # If not absolute, make it relative to workspace
                if not Path(path_str).is_absolute():
                    pattern = str(workspace_directory / path_str)
                else:
                    pattern = path_str
                
                # Expand glob pattern
                matched_files = glob_module.glob(pattern, recursive=True)
                for match in matched_files:
                    match_path = Path(match)
                    if match_path.is_file():
                        all_files.append(match_path)
            else:
                # No glob pattern - handle as literal path
                file_path = Path(path_str)
                if not file_path.is_absolute():
                    file_path = workspace_directory / file_path
                
                # Expand directories to .py files
                if file_path.exists() and file_path.is_dir():
                    py_files = list(file_path.rglob('*.py'))
                    all_files.extend(py_files)
                elif file_path.exists() and file_path.is_file():
                    all_files.append(file_path)
        
        return all_files
    
    def _find_scope_matches_in_graph(self, graph_data: Dict[str, Any], scope_values: List[str], workspace_directory: 'Path') -> List[str]:
        """Find and display scope matches from story graph."""
        lines = []
        epics = graph_data.get('epics', [])
        
        for scope_val in scope_values:
            match_lines = self._search_for_scope_match(epics, scope_val, workspace_directory, graph_data)
            if match_lines:
                lines.extend(match_lines)
            else:
                lines.append(f"  - {scope_val} (no match)")
        
        return lines
    
    def _search_for_scope_match(self, epics: List[Dict], scope_val: str, workspace_directory: 'Path', graph_data: Dict[str, Any]) -> Optional[List[str]]:
        """Search for scope match and return formatted lines with full hierarchy."""
        for epic in epics:
            epic_name = epic.get('name', '')
            if self._matches_name(epic_name, scope_val):
                return self._format_node_with_children(epic, 'epic', 0, workspace_directory, graph_data, epic_name, epic_name)
            
            match_lines = self._search_sub_epics(epic.get('sub_epics', []), scope_val, workspace_directory, graph_data, epic_name)
            if match_lines:
                return match_lines
        
        return None
    
    def _search_sub_epics(self, sub_epics: List[Dict], scope_val: str, workspace_directory: 'Path', graph_data: Dict[str, Any], epic_name: str) -> Optional[List[str]]:
        """Search sub-epics for scope match."""
        for sub_epic in sub_epics:
            sub_epic_name = sub_epic.get('name', '')
            if self._matches_name(sub_epic_name, scope_val):
                return self._format_node_with_children(sub_epic, 'sub epic', 0, workspace_directory, graph_data, epic_name, sub_epic_name)
            
            match_lines = self._search_stories(sub_epic, scope_val, workspace_directory, graph_data, epic_name, sub_epic_name)
            if match_lines:
                return match_lines
        
        return None
    
    def _search_stories(self, sub_epic: Dict, scope_val: str, workspace_directory: 'Path', graph_data: Dict[str, Any], epic_name: str, sub_epic_name: str) -> Optional[List[str]]:
        """Search stories for scope match."""
        lines = []
        # Include epic and sub-epic in the hierarchy for context
        lines.append(f"🎯 {epic_name}")
        
        # Format sub-epic line with test_file info if available
        test_file = sub_epic.get('test_file')
        if test_file:
            lines.append(f"  ⚙️ {sub_epic_name}|TEST_FILE:{test_file}")
        else:
            lines.append(f"  ⚙️ {sub_epic_name}")
        
        for story_group in sub_epic.get('story_groups', []):
            for story in story_group.get('stories', []):
                if self._matches_name(story.get('name', ''), scope_val):
                    story_lines = self._format_node_with_children(story, 'story', 2, workspace_directory, graph_data, epic_name, sub_epic_name)
                    # Get test_file ONLY from parent sub-epic (stories should not have test_file)
                    # Add test_file to story lines
                    if test_file and story_lines:
                        test_class = story.get('test_class')
                        # Always add test_file if available, even if no test_class
                        if test_class and test_class != '?':
                            # Replace line to include test_file before test_class
                            story_lines[0] = story_lines[0].replace(
                                f"|TEST_CLASS:{test_class}",
                                f"|TEST_FILE:{test_file}|TEST_CLASS:{test_class}"
                            )
                        elif '|TEST_CLASS:' in story_lines[0]:
                            # No test_class but placeholder exists, add test_file
                            story_lines[0] = story_lines[0].replace(
                                f"|TEST_CLASS:",
                                f"|TEST_FILE:{test_file}|TEST_CLASS:"
                            )
                        else:
                            # No test_class marker, add test_file at end
                            story_lines[0] = story_lines[0] + f"|TEST_FILE:{test_file}"
                    lines.extend(story_lines)
                    return lines
        
        for story in sub_epic.get('stories', []):
            if self._matches_name(story.get('name', ''), scope_val):
                story_lines = self._format_node_with_children(story, 'story', 2, workspace_directory, graph_data, epic_name, sub_epic_name)
                # Get test_file ONLY from parent sub-epic (stories should not have test_file)
                # Add test_file to story lines
                if test_file and story_lines:
                    test_class = story.get('test_class')
                    # Always add test_file if available, even if no test_class
                    if test_class and test_class != '?':
                        # Replace line to include test_file before test_class
                        story_lines[0] = story_lines[0].replace(
                            f"|TEST_CLASS:{test_class}",
                            f"|TEST_FILE:{test_file}|TEST_CLASS:{test_class}"
                        )
                    elif '|TEST_CLASS:' in story_lines[0]:
                        # No test_class but placeholder exists, add test_file
                        story_lines[0] = story_lines[0].replace(
                            f"|TEST_CLASS:",
                            f"|TEST_FILE:{test_file}|TEST_CLASS:"
                        )
                    else:
                        # No test_class marker, add test_file at end
                        story_lines[0] = story_lines[0] + f"|TEST_FILE:{test_file}"
                lines.extend(story_lines)
                return lines
        
        return None
    
    def _matches_name(self, name: str, pattern: str) -> bool:
        """Check if pattern matches name (case-insensitive)."""
        return pattern.lower() in name.lower()
    
    def _format_node_with_children(self, node: Dict[str, Any], node_type: str, indent: int, 
                                   workspace_directory: 'Path', graph_data: Dict[str, Any],
                                   epic_name: str, sub_epic_name: str) -> List[str]:
        """Format a node and its children recursively with hyperlinks for stories."""
        lines = []
        prefix = "  " * indent
        name = node.get('name', 'Unknown')
        
        # Use emojis matching the story map folder structure
        emoji_map = {
            'epic': '🎯',
            'sub epic': '⚙️',
            'story': '📝'
        }
        emoji = emoji_map.get(node_type, '•')
        
        # For stories, append test_file and test_class info
        if node_type == 'story':
            test_class = node.get('test_class')
            # test_file will be passed from parent sub-epic via the line modification below
            # Only include test_class marker if there's an actual test class
            if test_class and test_class != '?':
                lines.append(f"{prefix}{emoji} {name}|TEST_CLASS:{test_class}")
            else:
                # No test_class - just add the story name (parent can add test_file if needed)
                lines.append(f"{prefix}{emoji} {name}")
            return lines
        
        # For sub-epics, append test_file info
        if node_type == 'sub epic':
            test_file = node.get('test_file')
            if test_file:
                lines.append(f"{prefix}{emoji} {name}|TEST_FILE:{test_file}")
            else:
                lines.append(f"{prefix}{emoji} {name}")
        else:
            # For epics, just show the name
            lines.append(f"{prefix}{emoji} {name}")
        
        # Update context for children
        current_epic_name = epic_name
        current_sub_epic_name = sub_epic_name
        current_test_file = node.get('test_file') if node_type == 'sub epic' else None
        
        if node_type == 'epic':
            current_epic_name = name
            current_sub_epic_name = name  # Epic-level stories use epic name as sub-epic
        elif node_type == 'sub epic':
            current_sub_epic_name = name  # Update to this sub-epic's name for its children
            current_test_file = node.get('test_file')
        
        # Add sub_epics
        for sub_epic in node.get('sub_epics', []):
            sub_epic_child_name = sub_epic.get('name', '')
            lines.extend(self._format_node_with_children(sub_epic, 'sub epic', indent + 1, 
                                                       workspace_directory, graph_data, 
                                                       current_epic_name, sub_epic_child_name))
        
        # Add stories from story_groups
        for story_group in node.get('story_groups', []):
            for story in story_group.get('stories', []):
                story_lines = self._format_node_with_children(story, 'story', indent + 1,
                                                           workspace_directory, graph_data,
                                                           current_epic_name, current_sub_epic_name)
                # Get test_file ONLY from parent sub-epic (stories should not have test_file)
                # Modify story lines to include test_file if available
                if current_test_file and story_lines:
                    test_class = story.get('test_class')
                    # Always add test_file if available, even if no test_class
                    if test_class and test_class != '?':
                        # Replace line to include test_file before test_class
                        story_lines[0] = story_lines[0].replace(
                            f"|TEST_CLASS:{test_class}",
                            f"|TEST_FILE:{current_test_file}|TEST_CLASS:{test_class}"
                        )
                    else:
                        # No test_class, just add test_file at end
                        story_lines[0] = story_lines[0] + f"|TEST_FILE:{current_test_file}"
                lines.extend(story_lines)
        
        # Add direct stories (some structures have this)
        for story in node.get('stories', []):
            story_lines = self._format_node_with_children(story, 'story', indent + 1,
                                                       workspace_directory, graph_data,
                                                       current_epic_name, current_sub_epic_name)
            # Get test_file ONLY from parent sub-epic (stories should not have test_file)
            # Modify story lines to include test_file if available
            if current_test_file and story_lines:
                test_class = story.get('test_class')
                # Always add test_file if available, even if no test_class
                if test_class and test_class != '?':
                    # Replace line to include test_file before test_class
                    story_lines[0] = story_lines[0].replace(
                        f"|TEST_CLASS:{test_class}",
                        f"|TEST_FILE:{current_test_file}|TEST_CLASS:{test_class}"
                    )
                else:
                    # No test_class, just add test_file at end
                    story_lines[0] = story_lines[0] + f"|TEST_FILE:{current_test_file}"
            lines.extend(story_lines)
        
        return lines


@dataclass
class ActionContext:
    pass


@dataclass
class ScopeActionContext(ActionContext):
    scope: Optional[Scope] = None


@dataclass
class ClarifyActionContext(ActionContext):
    answers: Optional[Dict[str, Any]] = None
    evidence_provided: Optional[Dict[str, Any]] = None
    context: Optional[str] = None


@dataclass
class StrategyActionContext(ActionContext):
    decisions_made: Optional[Dict[str, Any]] = None
    assumptions: Optional[List[str]] = None
    assumptions_made: Optional[List[str]] = None
    
    def __post_init__(self):
        """Normalize strategy context fields and keep backward compatibility."""
        # Default collections to empty to simplify downstream checks
        if self.decisions_made is None:
            object.__setattr__(self, 'decisions_made', {})
        if self.assumptions_made is None:
            object.__setattr__(self, 'assumptions_made', self.assumptions or [])
        # Keep legacy alias in sync
        if self.assumptions is None:
            object.__setattr__(self, 'assumptions', self.assumptions_made)
    
    def get_decisions(self) -> Dict[str, Any]:
        """Get all decision attributes (exclude assumption fields and internals)."""
        excluded = {'assumptions', 'assumptions_made', 'decisions_made'}
        decisions = dict(self.decisions_made or {})
        for key, value in self.__dict__.items():
            if key.startswith('_') or key in excluded or value is None:
                continue
            decisions[key] = value
        return decisions
    
    @property
    def assumptions_list(self) -> Optional[List[str]]:
        """Alias to keep existing code using context.assumptions working."""
        return self.assumptions or self.assumptions_made
    
    @assumptions_list.setter
    def assumptions_list(self, value: Optional[List[str]]):
        object.__setattr__(self, 'assumptions_made', value)
        object.__setattr__(self, 'assumptions', value)


@dataclass
class ValidateActionContext(ScopeActionContext):
    background: Optional[bool] = None
    skip_cross_file: bool = False
    all_files: bool = False
    force_full: bool = False  # Alias for all_files for backward compatibility
    max_cross_file_comparisons: int = 20  # Maximum number of files to compare against in cross-file duplication scan
    
    def __post_init__(self):
        # Sync force_full and all_files - they mean the same thing
        if self.force_full:
            object.__setattr__(self, 'all_files', True)
        elif self.all_files:
            object.__setattr__(self, 'force_full', True)


@dataclass
class RulesActionContext(ActionContext):
    message: Optional[str] = None


# Type alias for context class type hints
ContextClass = type





