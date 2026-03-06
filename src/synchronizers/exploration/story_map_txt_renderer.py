"""
Render story graph to exploration story-map.txt format.

Output format:
(E) Epic Name
    (E) Sub-Epic Name
        (S) Actor --> Story Name
            (AC) WHEN ... THEN ...
"""
import json
from pathlib import Path
from typing import Any, Dict, List


def _actor_for_story(story: Dict[str, Any]) -> str:
    """Get actor string for story (users[0] or empty)."""
    users = story.get("users", [])
    return users[0] if users else ""


def _render_ac(ac: Dict[str, Any], indent: str) -> str:
    """Render single acceptance criteria."""
    text = ac.get("text", ac.get("name", ""))
    return f"{indent}(AC) {text}"


def _render_story(story: Dict[str, Any], indent: str) -> List[str]:
    """Render story with acceptance criteria."""
    lines = []
    actor = _actor_for_story(story)
    story_name = story.get("name", "")
    story_line = f"{actor} --> {story_name}" if actor else story_name
    lines.append(f"{indent}(S) {story_line}")

    ac_list = story.get("acceptance_criteria", [])
    ac_indent = indent + "    "
    for ac in ac_list:
        lines.append(_render_ac(ac, ac_indent))

    return lines


def _render_story_group(group: Dict[str, Any], indent: str, is_first_group: bool) -> List[str]:
    """Render story group with connector logic."""
    lines = []
    connector = group.get("connector")
    if not is_first_group and connector:
        lines.append(f"{indent[:-4]}{connector}")

    stories = group.get("stories", [])
    for story in stories:
        lines.extend(_render_story(story, indent))

    return lines


def _render_sub_epic(sub_epic: Dict[str, Any], indent: str) -> List[str]:
    """Recursively render sub-epic with nested structure."""
    lines = []
    name = sub_epic.get("name", "")
    lines.append(f"{indent}(E) {name}")

    child_indent = indent + "    "
    story_groups = sub_epic.get("story_groups", [])
    if story_groups:
        for idx, group in enumerate(story_groups):
            lines.extend(
                _render_story_group(group, child_indent, is_first_group=(idx == 0))
            )

    for nested in sub_epic.get("sub_epics", []):
        lines.extend(_render_sub_epic(nested, child_indent))

    return lines


def render_story_graph_to_txt(story_graph: Dict[str, Any]) -> str:
    """
    Render story graph to exploration story-map.txt format.

    Args:
        story_graph: Loaded story-graph.json dict

    Returns:
        Rendered text content
    """
    lines = []
    epics = story_graph.get("epics", [])

    for epic in epics:
        name = epic.get("name", "")
        lines.append(f"(E) {name}")

        for sub_epic in epic.get("sub_epics", []):
            lines.extend(_render_sub_epic(sub_epic, "    "))

        lines.append("")  # blank between epics

    return "\n".join(lines).rstrip()


def render_story_map_txt(story_graph_path: Path, output_path: Path) -> None:
    """
    Read story-graph.json and write story-map.txt.

    Args:
        story_graph_path: Path to story-graph.json
        output_path: Path to output story-map.txt
    """
    with open(story_graph_path, "r", encoding="utf-8") as f:
        story_graph = json.load(f)

    content = render_story_graph_to_txt(story_graph)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
