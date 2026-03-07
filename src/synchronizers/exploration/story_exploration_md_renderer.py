"""
Render story graph to exploration markdown per increment.

Produces {increment_name_slug}-exploration.md for each increment using
story-exploration.md template.
"""
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


def _slugify(name: str) -> str:
    """Convert name to slug (lowercase, spaces to hyphens, alphanumeric)."""
    s = re.sub(r"[^\w\s-]", "", name.lower())
    return re.sub(r"[-\s]+", "-", s).strip("-")


def _find_story_by_name(story_graph: Dict[str, Any], story_name: str) -> Optional[Dict[str, Any]]:
    """Find story dict by name in story graph."""
    for epic in story_graph.get("epics", []):
        found = _find_story_in_node(epic, story_name)
        if found:
            return found
    return None


def _find_story_in_node(node: Dict[str, Any], story_name: str) -> Optional[Dict[str, Any]]:
    """Recursively find story in epic/sub_epic."""
    for group in node.get("story_groups", []):
        for story in group.get("stories", []):
            if story.get("name") == story_name:
                return story
    for sub in node.get("sub_epics", []):
        found = _find_story_in_node(sub, story_name)
        if found:
            return found
    return None


def _format_ac_for_md(ac: Dict[str, Any]) -> str:
    """Format acceptance criteria for markdown (WHEN/THEN/AND/BUT)."""
    text = ac.get("text", ac.get("name", ""))
    return f"- {text}"


def _render_story_section(story: Dict[str, Any]) -> str:
    """Render single story section for exploration md."""
    name = story.get("name", "")
    ac_list = story.get("acceptance_criteria", [])
    ac_lines = [_format_ac_for_md(ac) for ac in ac_list]
    ac_block = "\n".join(ac_lines) if ac_lines else "- (No acceptance criteria yet)"

    return f"""### 📝 {name}

**Acceptance Criteria:**  
{ac_block}

"""


def _render_stories_section(stories: List[Dict[str, Any]]) -> str:
    """Render all stories sections."""
    return "\n".join(_render_story_section(s) for s in stories)


def render_increment_exploration(
    story_graph: Dict[str, Any],
    increment: Dict[str, Any],
    template_content: str,
    story_map_filename: str = "story-map.txt",
    increments_filename: str = "story-map-increments.drawio",
    source_material: str = "Story map from Shape stage, Discovery refinements",
) -> str:
    """
    Render exploration markdown for one increment.

    Args:
        story_graph: Loaded story-graph.json
        increment: Increment dict with name, stories (list of story names)
        template_content: story-exploration.md template content
        story_map_filename: Filename for story map link
        increments_filename: Filename for increments link
        source_material: Source material placeholder text

    Returns:
        Rendered markdown content
    """
    increment_name = increment.get("name", "Unnamed Increment")
    increment_name_slug = _slugify(increment_name)
    story_names = increment.get("stories", [])

    stories_data: List[Dict[str, Any]] = []
    for name in story_names:
        story = _find_story_by_name(story_graph, name)
        if story:
            stories_data.append(story)

    story_count = len(stories_data)
    stories_section = _render_stories_section(stories_data)

    # Replace template placeholders
    content = template_content
    content = content.replace("{increment_name}", increment_name)
    content = content.replace("{increment_name_slug}", increment_name_slug)
    content = content.replace("{story_map_filename}", story_map_filename)
    content = content.replace("{increments_filename}", increments_filename)
    content = content.replace("{story_count}", str(story_count))
    content = content.replace("{source_material}", source_material)

    # Replace placeholder story blocks (### 📝 <Story Name> ... ) with actual stories
    placeholder_pattern = r"(### 📝 <Story Name>[\s\S]*?)(?=\n---)"
    content = re.sub(
        placeholder_pattern,
        (stories_section + "\n\n") if stories_section else "",
        content,
    )

    return content


def render_all_increment_explorations(
    story_graph_path: Path,
    template_path: Path,
    output_dir: Path,
    story_map_filename: str = "story-map.txt",
    increments_filename: str = "story-map-increments.drawio",
    source_material: str = "Story map from Shape stage, Discovery refinements",
) -> List[Path]:
    """
    Render exploration markdown for each increment.

    Args:
        story_graph_path: Path to story-graph.json
        template_path: Path to story-exploration.md template
        output_dir: Directory for output files
        story_map_filename: Filename for story map link
        increments_filename: Filename for increments link
        source_material: Source material text

    Returns:
        List of created output file paths
    """
    with open(story_graph_path, "r", encoding="utf-8") as f:
        story_graph = json.load(f)

    template_content = template_path.read_text(encoding="utf-8")
    increments = story_graph.get("increments", [])
    created: List[Path] = []

    output_dir.mkdir(parents=True, exist_ok=True)

    for increment in increments:
        content = render_increment_exploration(
            story_graph=story_graph,
            increment=increment,
            template_content=template_content,
            story_map_filename=story_map_filename,
            increments_filename=increments_filename,
            source_material=source_material,
        )
        slug = _slugify(increment.get("name", "unnamed"))
        output_path = output_dir / f"{slug}-exploration.md"
        output_path.write_text(content, encoding="utf-8")
        created.append(output_path)

    return created
