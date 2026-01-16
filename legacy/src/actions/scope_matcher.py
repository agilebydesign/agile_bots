"""Shared utility for matching scope values against story graph structures."""

from typing import Dict, Any, List, Optional


def find_scope_matches(graph_data: Dict[str, Any], scope_values: List[str], use_emoji: bool = False) -> List[str]:
    """Find and display scope matches from story graph.
    
    Args:
        graph_data: Story graph data with epics structure
        scope_values: List of scope values to match
        use_emoji: If True, use emoji formatting; if False, use bracket formatting
        
    Returns:
        List of formatted match lines
    """
    lines = []
    epics = graph_data.get('epics', [])
    
    for scope_val in scope_values:
        match_lines = search_for_scope_match(epics, scope_val, use_emoji)
        if match_lines:
            lines.extend(match_lines)
        else:
            lines.append(f"  - {scope_val} (no match)")
    
    return lines


def search_for_scope_match(epics: List[Dict], scope_val: str, use_emoji: bool = False) -> Optional[List[str]]:
    """Search for scope match and return formatted lines with full hierarchy."""
    for epic in epics:
        if matches_name(epic.get('name', ''), scope_val):
            return format_node_with_children(epic, 'epic', 0, use_emoji)
        
        match_lines = search_sub_epics(epic.get('sub_epics', []), scope_val, use_emoji)
        if match_lines:
            return match_lines
    
    return None


def search_sub_epics(sub_epics: List[Dict], scope_val: str, use_emoji: bool = False) -> Optional[List[str]]:
    """Search sub-epics for scope match."""
    for sub_epic in sub_epics:
        if matches_name(sub_epic.get('name', ''), scope_val):
            return format_node_with_children(sub_epic, 'sub epic', 0, use_emoji)
        
        match_lines = search_stories(sub_epic, scope_val, use_emoji)
        if match_lines:
            return match_lines
    
    return None


def search_stories(sub_epic: Dict, scope_val: str, use_emoji: bool = False) -> Optional[List[str]]:
    """Search stories for scope match."""
    for story_group in sub_epic.get('story_groups', []):
        for story in story_group.get('stories', []):
            if matches_name(story.get('name', ''), scope_val):
                return format_node_with_children(story, 'story', 0, use_emoji)
    
    for story in sub_epic.get('stories', []):
        if matches_name(story.get('name', ''), scope_val):
            return format_node_with_children(story, 'story', 0, use_emoji)
    
    return None


def matches_name(name: str, pattern: str) -> bool:
    """Check if pattern matches name (case-insensitive)."""
    return pattern.lower() in name.lower()


def format_node_with_children(node: Dict[str, Any], node_type: str, indent: int, use_emoji: bool = False) -> List[str]:
    """Format a node and its children recursively.
    
    Args:
        node: Node dictionary with name and children
        node_type: Type of node ('epic', 'sub epic', 'story')
        indent: Indentation level
        use_emoji: If True, use emoji formatting; if False, use bracket formatting
        
    Returns:
        List of formatted lines
    """
    lines = []
    prefix = "  " * indent
    name = node.get('name', 'Unknown')
    
    if use_emoji:
        emoji_map = {
            'epic': '🎯',
            'sub epic': '⚙️',
            'story': '📝'
        }
        emoji = emoji_map.get(node_type, '•')
        lines.append(f"{prefix}{emoji} {name}")
    else:
        lines.append(f"{prefix}[{node_type}] {name}")
    
    # Don't recurse into stories - stop at story level
    if node_type == 'story':
        return lines
    
    # Add sub_epics
    for sub_epic in node.get('sub_epics', []):
        lines.extend(format_node_with_children(sub_epic, 'sub epic', indent + 1, use_emoji))
    
    # Add stories from story_groups
    for story_group in node.get('story_groups', []):
        for story in story_group.get('stories', []):
            lines.extend(format_node_with_children(story, 'story', indent + 1, use_emoji))
    
    # Add direct stories (some structures have this)
    for story in node.get('stories', []):
        lines.extend(format_node_with_children(story, 'story', indent + 1, use_emoji))
    
    return lines
