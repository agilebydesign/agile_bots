"""
Test Diagram Action Bar

Domain tests: Bot API for diagram actions (get_diagram_action_bar_buttons, render, save, update).
CLI tests: render_diagram command routes correctly.
Panel tests: in test_diagram_action_bar.js (rendering, button layout).

Uses generic fixture names (EpicA, SubEpicB). No story-specific identifiers.
"""
import json
import pytest
from pathlib import Path
from scope.scope import ScopeType

from helpers.bot_test_helper import BotTestHelper
from helpers import TTYBotTestHelper, PipeBotTestHelper, JsonBotTestHelper


def _given_story_map_with_epic_and_subepic(tmp_path, epic_name="EpicA", subepic_name="SubEpicB"):
    """Given StoryMap has epic and sub-epic (generic names for domain/CLI tests)."""
    helper = BotTestHelper(tmp_path)
    helper.story.create_story_graph_with_child("Epic", epic_name, subepic_name)
    return helper


class TestDiagramActionBarDomain:
    """
    Domain tests: Bot returns diagram action bar buttons, render/save/update for scoped node.
    No CLI. Uses generic fixture names (EpicA, SubEpicB).
    """

    def test_bot_returns_diagram_action_bar_buttons_for_story_node(self, tmp_path):
        helper = _given_story_map_with_epic_and_subepic(tmp_path)
        node = helper.bot.story_map.find_node("SubEpicB")
        assert node is not None
        buttons = helper.bot.get_diagram_action_bar_buttons(node)
        assert "Render diagram" in buttons or "render" in str(buttons).lower()

    def test_bot_render_diagram_for_scope_returns_status(self, tmp_path):
        helper = _given_story_map_with_epic_and_subepic(tmp_path)
        helper.bot._scope.filter(ScopeType.STORY, ["SubEpicB"])
        helper.bot._scope.save()
        result = helper.bot.render_diagram_for_scope()
        assert "status" in result or "diagram" in str(result).lower()

    def test_bot_save_layout_to_drawio_returns_status_or_path(self, tmp_path):
        helper = _given_story_map_with_epic_and_subepic(tmp_path)
        result = helper.bot.save_layout_to_drawio()
        assert "status" in result or "path" in str(result).lower()

    def test_bot_update_graph_from_diagram_returns_status_or_report(self, tmp_path):
        helper = _given_story_map_with_epic_and_subepic(tmp_path)
        result = helper.bot.update_graph_from_diagram()
        assert "status" in result or "report" in str(result).lower()

    def test_bot_render_diagram_for_empty_scope_returns_status(self, tmp_path):
        helper = _given_story_map_with_epic_and_subepic(tmp_path)
        helper.bot._scope.filter(ScopeType.STORY, ["SubEpicB"])
        helper.bot._scope.save()
        result = helper.bot.render_diagram_for_scope()
        assert "status" in result
        assert result.get("status") in ("success", "complete") or "diagram" in str(result).lower()

    def test_bot_render_diagram_fails_when_scope_node_not_in_story_map(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        helper.story.create_story_graph_with_child("Epic", "EpicA", "OtherNode")
        helper.bot._scope.filter(ScopeType.STORY, ["MissingNode"])
        helper.bot._scope.save()
        result = helper.bot.render_diagram_for_scope()
        assert result.get("status") == "error" or "error" in str(result).lower()


class TestDiagramActionBarCLI:
    """
    CLI tests: render_diagram command routes correctly.
    Uses generic scope path (EpicA, SubEpicB).
    """

    @pytest.mark.parametrize("helper_class", [TTYBotTestHelper, PipeBotTestHelper, JsonBotTestHelper])
    def test_cli_render_diagram_for_scope_reports_completion(self, tmp_path, helper_class):
        helper = helper_class(tmp_path)
        helper.domain.story.create_story_graph_with_child("Epic", "EpicA", "SubEpicB")
        cli_response = helper.cli_session.execute_command(
            'story_graph."EpicA"."SubEpicB".render_diagram'
        )
        output = cli_response.output
        if output.strip().startswith("{"):
            data = json.loads(output)
            assert data.get("status") in ("success", "complete")
        else:
            assert "success" in output.lower() or "complete" in output.lower()
