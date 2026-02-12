"""
Standalone utility functions for viewing / formatting increments.

These are pure-dict helpers with no dependency on legacy domain classes.
"""
from typing import List, Dict, Any


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
