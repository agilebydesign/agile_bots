"""CLI wrapper for Scope with display formatting."""
from pathlib import Path
from typing import Optional
from ..actions.action_context import Scope
from .cli_base import CLIBase
from .formatters.output_formatter import OutputFormatter
from ..actions.validate.file_link_builder import FileLinkBuilder
from ..bot.workspace import get_python_workspace_root
from ..utils import build_test_file_link, build_test_class_link, build_test_method_link
import json
import re


class CLIScope(CLIBase):
    """CLI wrapper for Scope that adds display formatting."""
    
    def __init__(self, scope: Scope, workspace_directory: Path, formatter: OutputFormatter):
        super().__init__(formatter)
        self._scope = scope
        self._workspace_directory = workspace_directory
    
    @classmethod
    def from_state_file(cls, workspace_directory: Path, formatter: OutputFormatter) -> Optional['CLIScope']:
        """Load scope from bot state file and wrap it."""
        try:
            state_file = workspace_directory / 'behavior_action_state.json'
            if not state_file.exists():
                return None
            
            state_data = json.loads(state_file.read_text())
            scope_dict = state_data.get('scope')
            if not scope_dict:
                return None
            
            scope = Scope.from_dict(scope_dict)
            return cls(scope, workspace_directory, formatter)
        except Exception:
            return None
    
    def to_formatted_display(self) -> str:
        """Render scope with CLI-specific formatting (warnings, separators, and AI instructions)."""
        from agile_bot.bots.base_bot.src.actions.action_context import ScopeType
        lines = []
        
        scope_icon = self.formatter.scope_icon()
        file_icon = self.formatter.file_icon()
        
        # Scope section header
        lines.append(f"## {scope_icon} **Scope**")
        
        # Get plain scope display lines from domain object
        scope_lines = self._scope.to_display_lines(self._workspace_directory)
        
        # Extract filter value
        scope_value = None
        for line in scope_lines:
            if line.startswith("Scope Filter:"):
                scope_value = line.replace("Scope Filter:", "").strip()
                break
        
        # For file scopes, add wildcard if missing
        if self._scope.type == ScopeType.FILES and scope_value:
            # Add /* to the end if no wildcard present
            if not any(wildcard in scope_value for wildcard in ['*', '?', '[']):
                scope_value = scope_value.rstrip('/') + '/*'
        
        # Build story-graph.json path and link (only if files exist)
        story_graph_path = self._workspace_directory / 'docs' / 'stories' / 'story-graph.json'
        story_map_path = self._workspace_directory / 'docs' / 'stories' / 'story-map.drawio'
        links = ""
        
        # Get workspace root once if either file exists
        workspace_root = None
        if story_graph_path.exists() or story_map_path.exists():
            try:
                workspace_root = get_python_workspace_root()
            except (ValueError, AttributeError):
                pass
        
        # Graph link (to story-graph.json) - only if file exists
        if story_graph_path.exists() and workspace_root:
            try:
                rel_path = story_graph_path.relative_to(workspace_root)
                rel_path_str = str(rel_path).replace('\\', '/')
                links = f" | [Graph]({rel_path_str})"
            except (ValueError, AttributeError):
                pass
        
        # Map link (to story-map.drawio) - only if file exists
        if story_map_path.exists() and workspace_root:
            try:
                rel_path = story_map_path.relative_to(workspace_root)
                rel_path_str = str(rel_path).replace('\\', '/')
                links += f" | [map]({rel_path_str})"
            except (ValueError, AttributeError):
                pass
        
        lines.append(f"**Filter:** {scope_value}{links}")
        lines.append("")
        
        # Display scope items
        if self._scope.type == ScopeType.FILES:
            # Build hierarchical directory structure for files with hyperlinks
            tree_lines = self._build_file_tree_with_hyperlinks(scope_lines)
            lines.extend(tree_lines)
        else:
            # For story/other scopes, enhance with hyperlinks and display as markdown (not code block)
            enhanced_lines = self._enhance_story_lines_with_hyperlinks(scope_lines)
            for line in enhanced_lines:
                if line.startswith("Scope Filter:"):
                    continue
                lines.append(line)
        
        lines.append("")
        lines.append("")
        lines.append("- Work ONLY on this scope:")
        lines.append("- DO NOT work on all files or the entire story graph")
        lines.append("- Focus EXCLUSIVELY on the items listed above - do not work on the entire story graph or file system")
        lines.append("")
        lines.append("To change scope (pick ONE - setting a new scope replaces the previous):")
        lines.append("```powershell")
        lines.append("scope all                            # Clear scope, work on entire project")
        lines.append("scope showAll                        # Show entire story graph (no filtering)")
        lines.append('scope "Story Name"                   # Filter by story (replaces any file scope)')
        lines.append('scope "file:C:/path/to/**/*.py"      # Filter by files (replaces any story scope)')
        lines.append("```")
        
        return "\n".join(lines)
    
    def to_json_display(self) -> str:
        """Render scope as JSON for programmatic consumption.
        
        Returns JSON with:
        - filter: scope filter string
        - type: scope type (story, epic, files, etc.)
        - links: map/graph file links
        - storyGraph: filtered story graph data (for story/epic scopes)
        - files: list of files (for file scopes)
        """
        import json
        from agile_bot.bots.base_bot.src.actions.action_context import ScopeType
        
        # Build filter display value
        filter_value = ', '.join(self._scope.value) if isinstance(self._scope.value, list) else str(self._scope.value) if self._scope.value else "all"
        
        # Build links to graph/map files
        story_graph_path = self._workspace_directory / 'docs' / 'stories' / 'story-graph.json'
        story_map_path = self._workspace_directory / 'docs' / 'stories' / 'story-map.drawio'
        
        workspace_root = None
        if story_graph_path.exists() or story_map_path.exists():
            try:
                workspace_root = get_python_workspace_root()
            except (ValueError, AttributeError):
                pass
        
        links = {}
        if story_graph_path.exists() and workspace_root:
            try:
                rel_path = story_graph_path.relative_to(workspace_root)
                links['graph'] = str(rel_path).replace('\\', '/')
            except (ValueError, AttributeError):
                pass
        
        if story_map_path.exists() and workspace_root:
            try:
                rel_path = story_map_path.relative_to(workspace_root)
                links['map'] = str(rel_path).replace('\\', '/')
            except (ValueError, AttributeError):
                pass
        
        result = {
            "filter": filter_value,
            "type": self._scope.type.value if hasattr(self._scope.type, 'value') else str(self._scope.type),
            "links": links
        }
        
        # Get filtered story graph data directly by loading and filtering story-graph.json
        if self._scope.type in (ScopeType.STORY, ScopeType.EPIC, ScopeType.SHOW_ALL):
            story_graph_path = self._workspace_directory / 'docs' / 'stories' / 'story-graph.json'
            if story_graph_path.exists():
                try:
                    import json as json_module
                    full_graph = json_module.loads(story_graph_path.read_text(encoding='utf-8'))
                    # Use the scope's filter method to get filtered graph
                    filtered_graph = self._scope.filters_knowledge_graph(full_graph)
                    
                    # Enhance filtered graph with story file paths
                    self._add_story_file_paths_to_graph(filtered_graph, workspace_root)
                    
                    result["storyGraph"] = filtered_graph
                except Exception:
                    pass
        elif self._scope.type == ScopeType.FILES:
            # Get expanded file list
            scope_lines = self._scope.to_display_lines(self._workspace_directory)
            files = []
            for line in scope_lines:
                if line.startswith("Scope Filter:"):
                    continue
                path_str = line.strip().lstrip('- ').strip()
                if path_str and not path_str.endswith("(no files found)"):
                    files.append(path_str)
            result["files"] = files
        
        # Wrap JSON in markdown section for display
        scope_icon = self.formatter.scope_icon()
        json_str = json.dumps(result, indent=2)
        
        lines = []
        lines.append(f"## {scope_icon} **Scope**")
        lines.append("```json")
        lines.append(json_str)
        lines.append("```")
        
        return "\n".join(lines)
    
    def to_json_dict(self, include_story_graph: bool = False) -> dict:
        """Return scope data as a dictionary (without markdown formatting).
        
        Args:
            include_story_graph: If True, load and include full story graph data.
                                If False, only include filter/type/links (faster).
        
        Returns dict with:
        - filter: scope filter string
        - type: scope type (story, epic, files, etc.)
        - links: map/graph file links
        - storyGraph: filtered story graph data (for story/epic scopes) - only if include_story_graph=True
        - files: list of files (for file scopes)
        """
        import json as json_module
        from agile_bot.bots.base_bot.src.actions.action_context import ScopeType
        
        # Build filter display value
        filter_value = ', '.join(self._scope.value) if isinstance(self._scope.value, list) else str(self._scope.value) if self._scope.value else "all"
        
        # Build links to graph/map files
        story_graph_path = self._workspace_directory / 'docs' / 'stories' / 'story-graph.json'
        story_map_path = self._workspace_directory / 'docs' / 'stories' / 'story-map.drawio'
        
        workspace_root = None
        if story_graph_path.exists() or story_map_path.exists():
            try:
                workspace_root = get_python_workspace_root()
            except (ValueError, AttributeError):
                pass
        
        links = {}
        if story_graph_path.exists() and workspace_root:
            try:
                rel_path = story_graph_path.relative_to(workspace_root)
                links['graph'] = str(rel_path).replace('\\', '/')
            except (ValueError, AttributeError):
                pass
        
        if story_map_path.exists() and workspace_root:
            try:
                rel_path = story_map_path.relative_to(workspace_root)
                links['map'] = str(rel_path).replace('\\', '/')
            except (ValueError, AttributeError):
                pass
        
        result = {
            "filter": filter_value,
            "type": self._scope.type.value if hasattr(self._scope.type, 'value') else str(self._scope.type),
            "links": links
        }
        
        # Get filtered story graph data directly by loading and filtering story-graph.json
        if self._scope.type in (ScopeType.STORY, ScopeType.EPIC, ScopeType.SHOW_ALL):
            story_graph_path = self._workspace_directory / 'docs' / 'stories' / 'story-graph.json'
            if story_graph_path.exists():
                try:
                    full_graph = json_module.loads(story_graph_path.read_text(encoding='utf-8'))
                    # Use the scope's filter method to get filtered graph
                    filtered_graph = self._scope.filters_knowledge_graph(full_graph)
                    
                    # Enhance filtered graph with story file paths
                    self._add_story_file_paths_to_graph(filtered_graph, workspace_root)
                    
                    result["storyGraph"] = filtered_graph
                except Exception:
                    pass
        elif self._scope.type == ScopeType.FILES:
            # Get expanded file list
            scope_lines = self._scope.to_display_lines(self._workspace_directory)
            files = []
            for line in scope_lines:
                if line.startswith("Scope Filter:"):
                    continue
                path_str = line.strip().lstrip('- ').strip()
                if path_str and not path_str.endswith("(no files found)"):
                    files.append(path_str)
            result["files"] = files
        
        return result
    
    def _build_file_tree_with_hyperlinks(self, scope_lines: list) -> list:
        """Build a hierarchical directory tree from file paths with hyperlinks."""
        from pathlib import Path
        
        # Extract file paths from scope lines
        file_paths = []
        for line in scope_lines:
            if line.startswith("Scope Filter:"):
                continue
            # Remove leading "  - " and parse as path
            path_str = line.strip().lstrip('- ').strip()
            if path_str and not path_str.endswith("(no files found)"):
                # Path might be relative to workspace or absolute
                if Path(path_str).is_absolute():
                    file_paths.append(Path(path_str))
                else:
                    # Relative path - make it absolute relative to workspace
                    file_paths.append(self._workspace_directory / path_str)
        
        if not file_paths:
            return ["  (no files found)"]
        
        # Build tree structure, storing full paths at leaf nodes
        tree = {}
        
        for file_path in file_paths:
            # Resolve to absolute path
            abs_path = file_path.resolve() if file_path.exists() else file_path
            
            # Get relative path from workspace for display
            try:
                rel_path = abs_path.relative_to(self._workspace_directory)
                parts = rel_path.parts
            except ValueError:
                # If can't make relative, use absolute path parts
                parts = abs_path.parts
            
            current = tree
            for i, part in enumerate(parts):
                if part not in current:
                    current[part] = {}
                current = current[part]
            
            # Store the full absolute path at the leaf node
            # Use a special key to store the path
            if '_file_path' not in current:
                current['_file_path'] = abs_path
        
        # Render tree with hyperlinks (starting at indent level 0, with tree characters)
        link_builder = FileLinkBuilder(self._workspace_directory)
        return self._render_tree_with_hyperlinks(tree, 0, link_builder, Path(), "", True)
    
    def _render_tree_with_hyperlinks(self, tree: dict, indent_level: int, link_builder: FileLinkBuilder, 
                                     base_path: Path, prefix: str = "", is_last: bool = True) -> list:
        """Recursively render tree structure with hyperlinks for files, matching story indentation style with tree characters."""
        lines = []
        # Filter out the special _file_path key when iterating
        items = [(k, v) for k, v in tree.items() if k != '_file_path']
        
        # Sort items: directories first, then files (matching story display order)
        directories = []
        files = []
        for name, subtree in items:
            subtree_keys = [k for k in subtree.keys() if k != '_file_path']
            is_file = '_file_path' in subtree and len(subtree_keys) == 0
            if is_file:
                files.append((name, subtree))
            else:
                directories.append((name, subtree))
        
        all_items = directories + files
        
        for i, (name, subtree) in enumerate(all_items):
            is_last_item = (i == len(all_items) - 1)
            subtree_keys = [k for k in subtree.keys() if k != '_file_path']
            is_file = '_file_path' in subtree and len(subtree_keys) == 0
            
            # Build tree connector: └── for last item, ├── for others
            connector = "└── " if is_last_item else "├── "
            icon = self.formatter.file_icon() if is_file else "📁"
            
            # Build the full line: prefix (tree continuation from parents) + connector + icon + name
            # This matches the story rendering pattern where prefix contains all parent tree characters
            # and connector adds the current level's tree character
            line_content = prefix + connector + f"{icon} {name}"
            
            # For files, create hyperlink
            if is_file:
                file_path = subtree.get('_file_path')
                if file_path and file_path.exists():
                    # Create hyperlink - replace the name in line_content with hyperlinked version
                    try:
                        rel_path = file_path.relative_to(self._workspace_directory)
                        file_uri = link_builder.get_file_uri(str(rel_path))
                        line_content = prefix + connector + f"{icon} [{name}]({file_uri})"
                    except ValueError:
                        # If relative path fails, use absolute path
                        file_uri = link_builder.get_file_uri(str(file_path))
                        line_content = prefix + connector + f"{icon} [{name}]({file_uri})"
            
            # Add line with tree structure (prefix + connector), matching story display style
            lines.append(line_content)
            
            # Recurse for directories (update prefix for tree structure continuation)
            if not is_file:
                # Tree continuation: "    " (4 spaces) if last, "│   " (pipe + 3 spaces) if not last
                extension = "    " if is_last_item else "│   "
                lines.extend(self._render_tree_with_hyperlinks(
                    subtree, indent_level + 1, link_builder, base_path / name, 
                    prefix + extension, is_last_item))
        
        return lines
    
    def _enhance_story_lines_with_hyperlinks(self, scope_lines: list) -> list:
        """Enhance story lines with hyperlinks to story files and format as tree structure."""
        enhanced_lines = []
        epic_name = None
        
        # Pattern to match story/epic/sub-epic lines with optional test info
        # Format: "  🎯 Epic Name" or "    ⚙️ Sub Epic Name|TEST_FILE:file.py" or "      📝 Story Name|TEST_FILE:file.py|TEST_CLASS:ClassName"
        epic_pattern = re.compile(r'^(\s*)(🎯)\s+(.+?)(?:\|TEST_FILE:(.+))?$')
        sub_epic_pattern = re.compile(r'^(\s*)(⚙️)\s+(.+?)(?:\|TEST_FILE:(.+))?$')
        story_pattern = re.compile(r'^(\s*)(📝)\s+(.+?)(?:\|TEST_FILE:(.+?))?(?:\|TEST_CLASS:(.+))?$')
        
        # First pass: collect all items to determine tree structure, preserving indentation
        items = []
        for line in scope_lines:
            if line.startswith("Scope Filter:"):
                continue
            
            epic_match = epic_pattern.match(line)
            if epic_match:
                indent_level = len(epic_match.group(1)) // 2  # Each level is 2 spaces
                items.append(('epic', epic_match.group(3).strip(), indent_level, None, None))
                continue
            
            sub_epic_match = sub_epic_pattern.match(line)
            if sub_epic_match:
                indent_level = len(sub_epic_match.group(1)) // 2  # Each level is 2 spaces
                test_file = sub_epic_match.group(4) if sub_epic_match.lastindex >= 4 and sub_epic_match.group(4) else None
                items.append(('sub_epic', sub_epic_match.group(3).strip(), indent_level, None, test_file))
                continue
            
            story_match = story_pattern.match(line)
            if story_match:
                indent_level = len(story_match.group(1)) // 2  # Each level is 2 spaces
                test_file = story_match.group(4) if story_match.lastindex >= 4 and story_match.group(4) else None
                test_class = story_match.group(5) if story_match.lastindex >= 5 else None
                items.append(('story', story_match.group(3).strip(), indent_level, line, (test_file, test_class)))
                continue
        
        # Second pass: render with tree structure, respecting nesting levels
        epic_idx = -1
        sub_epic_indices = {}  # Track sub-epic indices by nesting level
        sub_epic_names = {}  # Track sub-epic names by nesting level (full nested path)
        sub_epic_test_files = {}  # Track sub-epic test_files by nesting level
        story_idx = -1
        
        for i, (item_type, item_name, indent_level, original_line, item_data) in enumerate(items):
            if item_type == 'epic':
                epic_name = item_name
                epic_idx = i
                sub_epic_indices = {}  # Reset sub-epic tracking for new epic
                sub_epic_names = {}  # Reset sub-epic names for new epic
                sub_epic_test_files = {}  # Reset sub-epic test_files for new epic
                story_idx = -1
                enhanced_lines.append(f"🎯 {epic_name}")
            
            elif item_type == 'sub_epic':
                # Track this sub-epic at its nesting level
                sub_epic_indices[indent_level] = i
                # Build full nested path: combine parent path with current name
                parent_indent = indent_level - 1
                if parent_indent >= 0 and parent_indent in sub_epic_names:
                    # Append to parent's path
                    sub_epic_names[indent_level] = sub_epic_names[parent_indent] + [item_name]
                else:
                    # First level sub-epic under epic
                    sub_epic_names[indent_level] = [item_name]
                
                # Track test_file from sub-epic (item_data is the test_file string)
                sub_epic_test_files[indent_level] = item_data
                story_idx = -1
                
                # Find siblings at the same nesting level
                has_siblings_at_level = any(
                    items[j][0] == 'sub_epic' and items[j][2] == indent_level 
                    for j in range(i + 1, len(items))
                )
                
                # Find children (stories or nested sub-epics) at deeper levels
                has_children = any(
                    (items[j][0] == 'story' or (items[j][0] == 'sub_epic' and items[j][2] > indent_level))
                    for j in range(i + 1, len(items))
                    if j < len(items) and items[j][2] > indent_level
                )
                
                # Build indentation prefix based on nesting level
                # Level 0 (directly under epic): 2 spaces + connector
                # Level 1 (nested sub-epic): 2 spaces + │   + connector
                # Level 2: 2 spaces + │   + │   + connector, etc.
                base_indent = "  " * indent_level
                
                # Build tree connector with vertical lines for parent levels
                connector_parts = []
                for level in range(indent_level):
                    # Check if there are siblings at this parent level after current position
                    has_siblings_at_parent = any(
                        items[k][0] == 'sub_epic' and items[k][2] == level
                        for k in range(i + 1, len(items))
                    )
                    # Check if there are items (stories or nested sub-epics) at this level or deeper
                    # that come after the current item
                    has_items_below = any(
                        items[k][2] > level
                        for k in range(i + 1, len(items))
                    )
                    # Show vertical line if there are siblings or items below at this parent level
                    if has_siblings_at_parent or has_items_below:
                        connector_parts.append("│   ")
                    else:
                        connector_parts.append("    ")
                
                prefix = "".join(connector_parts)
                
                # Determine connector for this level
                connector = "├── " if (has_siblings_at_level or has_children) else "└── "
                
                # Build sub-epic folder path for hyperlink (pass full nested path)
                sub_epic_folder_path = self._build_sub_epic_folder_path(epic_name, sub_epic_names[indent_level])
                
                # Add test file link if available
                test_file = item_data
                test_link = ""
                if test_file:
                    test_link = self._build_test_file_link(test_file)
                
                # Create hyperlink for sub-epic folder if it exists
                if sub_epic_folder_path and sub_epic_folder_path.exists():
                    try:
                        workspace_root = get_python_workspace_root()
                        rel_path = sub_epic_folder_path.relative_to(workspace_root)
                        rel_path_str = str(rel_path).replace('\\', '/')
                        enhanced_lines.append(f"{base_indent}{prefix}{connector}[⚙️ {item_name}]({rel_path_str}){test_link}")
                    except (ValueError, AttributeError):
                        # If relative path fails, use original format without folder link
                        enhanced_lines.append(f"{base_indent}{prefix}{connector}⚙️ {item_name}{test_link}")
                else:
                    # Folder doesn't exist, keep original formatting
                    enhanced_lines.append(f"{base_indent}{prefix}{connector}⚙️ {item_name}{test_link}")
            
            elif item_type == 'story':
                story_name = item_name
                
                # Find the parent sub-epic path at the appropriate nesting level (now a list)
                parent_indent_level = indent_level - 1
                parent_sub_epic_path = sub_epic_names.get(parent_indent_level) if parent_indent_level >= 0 else None
                
                # Build story file path (pass full nested path)
                story_file_path = self._build_story_file_path(epic_name, parent_sub_epic_path, story_name)
                
                # Find the parent sub-epic index at the appropriate nesting level
                parent_sub_epic_idx = -1
                parent_indent_level = indent_level - 1
                if parent_indent_level >= 0:
                    parent_sub_epic_idx = sub_epic_indices.get(parent_indent_level, -1)
                
                # Check if this is the last story at this nesting level
                is_last_story = True
                for j in range(i + 1, len(items)):
                    if items[j][0] == 'story' and items[j][2] == indent_level:
                        is_last_story = False
                        break
                    elif items[j][2] <= indent_level and items[j][0] != 'story':
                        break
                
                # Build indentation prefix based on nesting level
                base_indent = "  " * indent_level
                
                # Build tree connector with vertical lines for parent levels
                connector_parts = []
                for level in range(indent_level):
                    # Check if there are siblings at this parent level after current position
                    has_siblings_at_parent = any(
                        items[k][0] == 'sub_epic' and items[k][2] == level
                        for k in range(i + 1, len(items))
                    )
                    # Check if there are items (stories or nested sub-epics) at this level or deeper
                    # that come after the current item
                    has_items_below = any(
                        items[k][2] > level
                        for k in range(i + 1, len(items))
                    )
                    # Show vertical line if there are siblings or items below at this parent level
                    if has_siblings_at_parent or has_items_below:
                        connector_parts.append("│   ")
                    else:
                        connector_parts.append("    ")
                
                prefix = "".join(connector_parts)
                
                # Determine connector for this level
                connector = prefix + ("└── " if is_last_story else "├── ")
                
                if story_file_path and story_file_path.exists():
                    # For files with emojis in path, use relative path from workspace root
                    # Cursor resolves markdown links relative to workspace root, not workspace_directory
                    try:
                        workspace_root = get_python_workspace_root()
                        rel_path = story_file_path.relative_to(workspace_root)
                        # Use relative path as markdown link - Cursor will resolve it correctly
                        rel_path_str = str(rel_path).replace('\\', '/')
                        enhanced_lines.append(f"{connector}[📝 {story_name}]({rel_path_str})")
                    except (ValueError, AttributeError):
                        # If relative path fails, try vscode://file URI as fallback
                        link_builder = FileLinkBuilder(self._workspace_directory)
                        file_uri = link_builder.get_file_uri(str(story_file_path))
                        enhanced_lines.append(f"{connector}[📝 {story_name}]({file_uri})")
                else:
                    # File doesn't exist, keep original formatting
                    enhanced_lines.append(f"{connector}📝 {story_name}")
                
                # Add test class link if available
                # Get test_class from story's item_data (stories should not have test_file)
                _, test_class = item_data if item_data else (None, None)
                
                # Get test_file ONLY from parent sub-epic (stories should not have test_file)
                test_file = None
                parent_indent_level = indent_level - 1
                if parent_indent_level >= 0:
                    test_file = sub_epic_test_files.get(parent_indent_level)
                
                if test_file and test_class:
                    test_class_link = self._build_test_class_link(test_file, test_class)
                    if test_class_link:
                        enhanced_lines[-1] = enhanced_lines[-1] + test_class_link
        
        return enhanced_lines
    
    def _add_story_file_paths_to_graph(self, graph_data: dict, workspace_root: Optional[Path]) -> None:
        """Enhance story graph with story_file paths for each story node."""
        if not graph_data or not workspace_root:
            return
        
        epics = graph_data.get('epics', [])
        for epic in epics:
            epic_name = epic.get('name')
            if not epic_name:
                continue
            
            sub_epics = epic.get('sub_epics', [])
            for sub_epic in sub_epics:
                # Process sub-epic recursively with path tracking
                self._process_sub_epic_for_file_paths(sub_epic, epic_name, [], workspace_root)
    
    def _process_sub_epic_for_file_paths(self, sub_epic: dict, epic_name: str, parent_path: list, workspace_root: Path) -> None:
        """Recursively process sub-epic and its nested children to add file paths."""
        sub_epic_name = sub_epic.get('name')
        if not sub_epic_name:
            return
        
        # Build current path (parent path + current sub-epic)
        current_path = parent_path + [sub_epic_name]
        
        # Process nested sub-epics recursively
        nested_sub_epics = sub_epic.get('sub_epics', [])
        for nested_sub_epic in nested_sub_epics:
            self._process_sub_epic_for_file_paths(nested_sub_epic, epic_name, current_path, workspace_root)
        
        # Process stories in story_groups at this level
        story_groups = sub_epic.get('story_groups', [])
        for story_group in story_groups:
            stories = story_group.get('stories', [])
            for story in stories:
                self._add_story_file_to_node(story, epic_name, current_path, workspace_root)
        
        # Process stories directly in sub_epic
        direct_stories = sub_epic.get('stories', [])
        for story in direct_stories:
            self._add_story_file_to_node(story, epic_name, current_path, workspace_root)
    
    def _add_story_file_to_node(self, story_node: dict, epic_name: str, sub_epic_path: list, workspace_root: Path) -> None:
        """Add story_file path to a single story node."""
        story_name = story_node.get('name')
        if not story_name:
            return
        
        # Build story file path with full nested path
        story_file_path = self._build_story_file_path(epic_name, sub_epic_path, story_name)
        
        if story_file_path and story_file_path.exists():
            try:
                # Get relative path from workspace root
                rel_path = story_file_path.relative_to(workspace_root)
                story_node['story_file'] = str(rel_path).replace('\\', '/')
                story_node['story_file_exists'] = True
            except (ValueError, AttributeError):
                # If relative path fails, store absolute path
                story_node['story_file'] = str(story_file_path).replace('\\', '/')
                story_node['story_file_exists'] = True
        else:
            story_node['story_file_exists'] = False
    
    def _build_story_file_path(self, epic_name: Optional[str], sub_epic_path: Optional[list], story_name: str) -> Optional[Path]:
        """Build the file path for a story based on epic/nested sub-epic path/story names.
        
        Args:
            epic_name: The epic name
            sub_epic_path: List of nested sub-epic names (e.g., ["Invoke Bot Through Panel", "Manage Panel Session"])
            story_name: The story name
        """
        if not epic_name:
            return None
        
        # Build path: docs/stories/map/🎯 {epic_name}/⚙️ {sub_epic_1}/⚙️ {sub_epic_2}/.../📝 {story_name}.md
        map_dir = self._workspace_directory / 'docs' / 'stories' / 'map'
        epic_folder = f"🎯 {epic_name}"
        
        # Start with epic folder
        current_path = map_dir / epic_folder
        
        # Add all nested sub-epic folders
        if sub_epic_path:
            for sub_epic_name in sub_epic_path:
                if sub_epic_name and sub_epic_name != epic_name:
                    sub_epic_folder = f"⚙️ {sub_epic_name}"
                    current_path = current_path / sub_epic_folder
        
        # Add story file
        story_file = current_path / f"📝 {story_name}.md"
        
        # Fallback: if path doesn't exist and we have a sub_epic_path, try simpler paths
        if not story_file.exists() and sub_epic_path:
            # Try with just the last sub-epic name (backward compatibility)
            last_sub_epic = sub_epic_path[-1]
            if last_sub_epic != epic_name:
                fallback_path = map_dir / epic_folder / f"⚙️ {last_sub_epic}" / f"📝 {story_name}.md"
                if fallback_path.exists():
                    return fallback_path
            
            # Try directly under epic (backward compatibility)
            fallback_path = map_dir / epic_folder / f"📝 {story_name}.md"
            if fallback_path.exists():
                return fallback_path
        
        return story_file
    
    def _build_sub_epic_folder_path(self, epic_name: Optional[str], sub_epic_path: list) -> Optional[Path]:
        """Build the folder path for a sub-epic based on epic/nested sub-epic path.
        
        Args:
            epic_name: The epic name
            sub_epic_path: List of nested sub-epic names (e.g., ["Invoke Bot Through Panel", "Manage Panel Session"])
        """
        if not epic_name or not sub_epic_path:
            return None
        
        # Build path: docs/stories/map/🎯 {epic_name}/⚙️ {sub_epic_1}/⚙️ {sub_epic_2}/.../
        map_dir = self._workspace_directory / 'docs' / 'stories' / 'map'
        epic_folder = f"🎯 {epic_name}"
        
        # Start with epic folder
        folder_path = map_dir / epic_folder
        
        # Add all nested sub-epic folders
        for sub_epic_name in sub_epic_path:
            if sub_epic_name:
                sub_epic_folder = f"⚙️ {sub_epic_name}"
                folder_path = folder_path / sub_epic_folder
        
        return folder_path if folder_path.exists() and folder_path.is_dir() else None
    
    def _build_test_file_link(self, test_file: str) -> str:
        """Build link to test file."""
        return build_test_file_link(test_file, self._workspace_directory)
    
    def _build_test_class_link(self, test_file: str, test_class: str) -> str:
        """Build link to test class with line number."""
        return build_test_class_link(test_file, test_class, self._workspace_directory)
    
    def _add_story_file_paths_to_graph(self, filtered_graph: dict, workspace_root: Path) -> None:
        """Add story_file paths to each story in the filtered graph for panel consumption."""
        if 'epics' not in filtered_graph:
            return
        
        for epic in filtered_graph['epics']:
            epic_name = epic.get('name')
            if not epic_name or 'sub_epics' not in epic:
                continue
            
            for sub_epic in epic['sub_epics']:
                # Process sub-epic recursively with path tracking
                self._process_sub_epic_for_panel(sub_epic, epic_name, [], workspace_root)
    
    def _process_sub_epic_for_panel(self, sub_epic: dict, epic_name: str, parent_path: list, workspace_root: Path) -> None:
        """Recursively process sub-epic and its nested children for panel consumption."""
        sub_epic_name = sub_epic.get('name')
        if not sub_epic_name:
            return
        
        # Build current path (parent path + current sub-epic)
        current_path = parent_path + [sub_epic_name]
        
        # Add folder path for sub-epic
        sub_epic_folder_path = self._build_sub_epic_folder_path(epic_name, current_path)
        if sub_epic_folder_path and sub_epic_folder_path.exists():
            try:
                rel_path = sub_epic_folder_path.relative_to(workspace_root)
                sub_epic['sub_epic_folder'] = str(rel_path).replace('\\', '/')
                sub_epic['sub_epic_folder_exists'] = True
            except (ValueError, AttributeError):
                sub_epic['sub_epic_folder'] = str(sub_epic_folder_path).replace('\\', '/')
                sub_epic['sub_epic_folder_exists'] = True
        else:
            sub_epic['sub_epic_folder_exists'] = False
        
        # Add test link for sub-epic (feature) if test_file exists
        test_file = sub_epic.get('test_file')
        if test_file:
            test_link = self._build_test_file_link(test_file)
            if test_link:
                # Extract URL from markdown link: " | [Test](url)"
                import re
                match = re.search(r'\[Test\]\(([^)]+)\)', test_link)
                if match:
                    sub_epic['test_link'] = match.group(1)
        
        # Process nested sub-epics recursively
        if 'sub_epics' in sub_epic:
            for nested_sub_epic in sub_epic['sub_epics']:
                self._process_sub_epic_for_panel(nested_sub_epic, epic_name, current_path, workspace_root)
        
        # Process stories in story_groups at this level
        if 'story_groups' in sub_epic:
            for story_group in sub_epic['story_groups']:
                if 'stories' in story_group:
                    for story in story_group['stories']:
                        self._add_story_file_to_story_obj(story, epic_name, current_path, workspace_root)
        
        # Process stories directly at sub_epic level
        if 'stories' in sub_epic:
            for story in sub_epic['stories']:
                self._add_story_file_to_story_obj(story, epic_name, current_path, workspace_root)
    
    def _add_story_file_to_story_obj(self, story: dict, epic_name: str, sub_epic_path: list, workspace_root: Path) -> None:
        """Add story_file path to a single story object."""
        story_name = story.get('name')
        if not story_name:
            return
        
        # Build the story file path with full nested path
        story_file_path = self._build_story_file_path(epic_name, sub_epic_path, story_name)
        
        if story_file_path and story_file_path.exists():
            story['story_file_exists'] = True
            try:
                # Convert to relative path from workspace root
                if workspace_root:
                    rel_path = story_file_path.relative_to(workspace_root)
                    story['story_file'] = str(rel_path).replace('\\', '/')
                else:
                    story['story_file'] = str(story_file_path).replace('\\', '/')
            except (ValueError, AttributeError):
                # If relative path fails, use absolute path
                story['story_file'] = str(story_file_path).replace('\\', '/')
        else:
            story['story_file_exists'] = False
        
        # Use existing test link builder to get validated markdown link
        # Format: " | [Test](path)" or "" if file doesn't exist
        test_file = story.get('test_file')
        test_class = story.get('test_class')
        if test_file and test_class:
            test_link = self._build_test_class_link(test_file, test_class)
            if test_link:
                # Extract URL from markdown link: " | [Test](url)"
                import re
                match = re.search(r'\[Test\]\(([^)]+)\)', test_link)
                if match:
                    story['test_link'] = match.group(1)
        elif test_file:
            test_link = self._build_test_file_link(test_file)
            if test_link:
                # Extract URL from markdown link: " | [Test](url)"
                import re
                match = re.search(r'\[Test\]\(([^)]+)\)', test_link)
                if match:
                    story['test_link'] = match.group(1)
    
    @property
    def domain_scope(self) -> Scope:
        """Access the underlying domain Scope object."""
        return self._scope


