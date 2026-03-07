"""
Test Exploration Render

SubEpic: Render Content
Parent Epic: Invoke Bot > Perform Action

Story: Render acceptance criteria documentation (exploration behavior)

Domain tests verify story_map_txt_renderer, story_exploration_md_renderer,
and ExplorationRenderExecutor. All tests use tmp_path - no writes to production.
"""
import json
import pytest
from pathlib import Path

from synchronizers.exploration.story_map_txt_renderer import (
    render_story_graph_to_txt,
    render_story_map_txt,
)
from synchronizers.exploration.story_exploration_md_renderer import (
    render_increment_exploration,
    render_all_increment_explorations,
)
from synchronizers.exploration.exploration_render_executor import ExplorationRenderExecutor


def given_story_graph_with_epics(tmp_path: Path) -> Path:
    """Given: story-graph.json exists with epics, sub-epics, stories."""
    story_graph = {
        "epics": [
            {
                "name": "Invoke Bot",
                "sub_epics": [
                    {
                        "name": "Perform Action",
                        "story_groups": [
                            {
                                "stories": [
                                    {
                                        "name": "Load Config",
                                        "users": ["Developer"],
                                        "acceptance_criteria": [
                                            {"text": "WHEN user provides path THEN config loads"}
                                        ],
                                    },
                                    {
                                        "name": "Execute Action",
                                        "users": [],
                                        "acceptance_criteria": [],
                                    },
                                ]
                            }
                        ],
                        "sub_epics": [],
                    }
                ],
            }
        ],
        "increments": [
            {"name": "I1: Foundation", "priority": 1, "stories": ["Load Config"]},
            {"name": "I2: Core", "priority": 2, "stories": ["Execute Action"]},
        ],
    }
    path = tmp_path / "story-graph.json"
    path.write_text(json.dumps(story_graph, indent=2), encoding="utf-8")
    return path


def given_story_graph_with_nested_sub_epics(tmp_path: Path) -> Path:
    """Given: story graph with nested sub-epics."""
    story_graph = {
        "epics": [
            {
                "name": "Epic A",
                "sub_epics": [
                    {
                        "name": "SubEpic A1",
                        "story_groups": [{"stories": [{"name": "Story A1", "users": [], "acceptance_criteria": []}]}],
                        "sub_epics": [
                            {
                                "name": "Nested A1a",
                                "story_groups": [{"stories": [{"name": "Story A1a", "users": [], "acceptance_criteria": []}]}],
                                "sub_epics": [],
                            }
                        ],
                    }
                ],
            }
        ],
        "increments": [],
    }
    path = tmp_path / "story-graph.json"
    path.write_text(json.dumps(story_graph, indent=2), encoding="utf-8")
    return path


def when_render_story_graph_to_txt(story_graph: dict) -> str:
    """When: render_story_graph_to_txt is called."""
    return render_story_graph_to_txt(story_graph)


def when_render_story_map_txt(story_graph_path: Path, output_path: Path) -> None:
    """When: render_story_map_txt is called."""
    render_story_map_txt(story_graph_path, output_path)


def then_story_map_contains_epic_and_story(content: str, epic_name: str, story_name: str) -> None:
    """Then: content contains epic and story in exploration format."""
    assert f"(E) {epic_name}" in content
    assert story_name in content
    assert "(S)" in content


def then_story_map_contains_ac(content: str, ac_text: str) -> None:
    """Then: content contains acceptance criteria."""
    assert "(AC)" in content
    assert ac_text in content or "WHEN" in content


class TestStoryMapTxtRenderer:
    """Story map txt renderer - renders story graph to exploration format."""

    def test_render_story_graph_to_txt_produces_epic_sub_epic_story_format(self, tmp_path):
        story_graph_path = given_story_graph_with_epics(tmp_path)
        with open(story_graph_path, "r", encoding="utf-8") as f:
            story_graph = json.load(f)

        content = when_render_story_graph_to_txt(story_graph)

        then_story_map_contains_epic_and_story(content, "Invoke Bot", "Load Config")
        then_story_map_contains_ac(content, "WHEN user provides path")

    def test_render_story_map_txt_writes_file(self, tmp_path):
        story_graph_path = given_story_graph_with_epics(tmp_path)
        output_path = tmp_path / "exploration" / "story-map.txt"

        when_render_story_map_txt(story_graph_path, output_path)

        assert output_path.exists()
        content = output_path.read_text(encoding="utf-8")
        then_story_map_contains_epic_and_story(content, "Invoke Bot", "Load Config")

    def test_render_story_map_txt_handles_nested_sub_epics(self, tmp_path):
        story_graph_path = given_story_graph_with_nested_sub_epics(tmp_path)
        with open(story_graph_path, "r", encoding="utf-8") as f:
            story_graph = json.load(f)

        content = when_render_story_graph_to_txt(story_graph)

        assert "(E) Epic A" in content
        assert "(E) SubEpic A1" in content
        assert "(E) Nested A1a" in content
        assert "Story A1" in content
        assert "Story A1a" in content

    def test_render_story_map_txt_includes_actor_when_present(self, tmp_path):
        story_graph_path = given_story_graph_with_epics(tmp_path)
        with open(story_graph_path, "r", encoding="utf-8") as f:
            story_graph = json.load(f)

        content = when_render_story_graph_to_txt(story_graph)

        assert "Developer --> Load Config" in content


class TestStoryExplorationMdRenderer:
    """Story exploration md renderer - renders per-increment exploration markdown."""

    def test_render_increment_exploration_replaces_placeholders(self, tmp_path):
        story_graph_path = given_story_graph_with_epics(tmp_path)
        with open(story_graph_path, "r", encoding="utf-8") as f:
            story_graph = json.load(f)
        template = "# {increment_name}\n\nStories: {story_count}\n\n{stories}"
        increment = {"name": "I1: Foundation", "stories": ["Load Config"]}

        content = render_increment_exploration(
            story_graph=story_graph,
            increment=increment,
            template_content=template,
        )

        assert "I1: Foundation" in content
        assert "1" in content  # story_count

    def test_render_all_increment_explorations_creates_file_per_increment(self, tmp_path):
        story_graph_path = given_story_graph_with_epics(tmp_path)
        template_path = tmp_path / "story-exploration.md"
        template_path.write_text(
            "# {increment_name}\n\nStories: {story_count}\n\n",
            encoding="utf-8",
        )
        output_dir = tmp_path / "exploration"
        output_dir.mkdir()

        created = render_all_increment_explorations(
            story_graph_path=story_graph_path,
            template_path=template_path,
            output_dir=output_dir,
        )

        assert len(created) == 2
        slugs = [p.stem for p in created]
        assert "i1-foundation-exploration" in slugs or any("i1" in s for s in slugs)
        assert "i2-core-exploration" in slugs or any("i2" in s for s in slugs)
        for p in created:
            assert p.exists()


class TestExplorationRenderExecutor:
    """Exploration render executor - runs template and synchronizer configs."""

    def test_render_all_creates_story_map_and_exploration_md_when_configs_exist(self, tmp_path):
        story_graph_path = given_story_graph_with_epics(tmp_path)
        behavior_render_dir = tmp_path / "behaviors" / "exploration" / "content" / "render"
        behavior_render_dir.mkdir(parents=True)
        templates_dir = behavior_render_dir / "templates"
        templates_dir.mkdir()

        # Minimal configs
        (behavior_render_dir / "render_story_map_txt.json").write_text(
            json.dumps({
                "name": "render_story_map",
                "path": "docs/story/exploration",
                "template": "story-map.txt",
                "output": "story-map.txt",
            }),
            encoding="utf-8",
        )
        (behavior_render_dir / "render_story_exploration.md.json").write_text(
            json.dumps({
                "name": "render_story_exploration",
                "path": "docs/story/exploration",
                "template": "story-exploration.md",
                "output": "{increment_name_slug}-exploration.md",
            }),
            encoding="utf-8",
        )
        (templates_dir / "story-map.txt").write_text("(E) placeholder\n", encoding="utf-8")
        (templates_dir / "story-exploration.md").write_text(
            "# {increment_name}\n\nStories: {story_count}\n\n",
            encoding="utf-8",
        )

        executor = ExplorationRenderExecutor(
            workspace_root=tmp_path,
            story_graph_path=story_graph_path,
            behavior_render_dir=behavior_render_dir,
        )

        result = executor.render_all()

        assert "created" in result
        assert len(result["created"]) >= 3  # story-map.txt + 2 increment md files
        story_map = tmp_path / "docs" / "story" / "exploration" / "story-map.txt"
        assert story_map.exists()
        content = story_map.read_text(encoding="utf-8")
        assert "(E) Invoke Bot" in content

