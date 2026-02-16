"""
Test Generate Cursor Context Package

SubEpic: Generate Cursor Context Package
Parent Epic: Build Agile Bots > Generate CLI

Story: Create Rule Files From Bot Behavior
Domain tests verify rule file generation from bot behaviors.
CLI tests verify generate_context_package command executes on active bot.
All tests use tmp_path - no writes to production bot workspace.
"""
import json
import os
import pytest
from pathlib import Path

from cli.cli_session import CLISession
from synchronizers.context_package.rule_file_generator import RuleFileGenerator


def given_bot_with_behaviors_directory(tmp_path: Path, bot_name: str) -> Path:
    """Given: Bot exists with behaviors directory."""
    bot_dir = tmp_path / "bots" / bot_name
    behaviors_dir = bot_dir / "behaviors"
    behaviors_dir.mkdir(parents=True)
    return bot_dir


def given_behavior_with_valid_json(bot_dir: Path, behavior_name: str) -> Path:
    """Given: Behavior has valid behavior.json with behaviorName, description, goal, inputs, outputs."""
    behavior_dir = bot_dir / "behaviors" / behavior_name
    behavior_dir.mkdir(parents=True)
    behavior_json = {
        "behaviorName": behavior_name,
        "description": "Test behavior",
        "goal": "Test goal",
        "inputs": "test inputs",
        "outputs": "test outputs",
    }
    (behavior_dir / "behavior.json").write_text(json.dumps(behavior_json, indent=2), encoding="utf-8")
    return behavior_dir


def when_generator_runs(bot_dir: Path, workspace_dir: Path) -> dict:
    """When: Generator runs generate context package command."""
    generator = RuleFileGenerator(bot_directory=bot_dir, workspace_directory=workspace_dir)
    return generator.generate()


def then_rule_files_exist_in_cursor_rules(workspace_dir: Path, expected_count: int) -> None:
    """Then: .mdc rule files exist in workspace .cursor/rules/ folder."""
    rules_dir = workspace_dir / ".cursor" / "rules"
    assert rules_dir.exists(), f"Expected .cursor/rules/ directory at {rules_dir}"
    mdc_files = list(rules_dir.glob("*.mdc"))
    assert len(mdc_files) == expected_count, f"Expected {expected_count} .mdc files, found {len(mdc_files)}"


class TestCreateRuleFilesFromBotBehavior:
    """Create Rule Files From Bot Behavior - Generator produces .mdc rule files from bot behaviors."""

    def test_generator_produces_rule_file_per_behavior_when_bot_has_valid_behaviors(self, tmp_path):
        bot_name = "story_bot"
        behavior_name = "shape"
        bot_dir = given_bot_with_behaviors_directory(tmp_path, bot_name)
        given_behavior_with_valid_json(bot_dir, behavior_name)
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        result = when_generator_runs(bot_dir, workspace_dir)

        then_rule_files_exist_in_cursor_rules(workspace_dir, expected_count=1)
        rule_file = workspace_dir / ".cursor" / "rules" / f"{bot_name}_{behavior_name}.mdc"
        assert rule_file.exists(), f"Expected rule file at {rule_file}"

    def test_generator_writes_rule_file_header_with_title_subtitle_and_sections(self, tmp_path):
        bot_dir = given_bot_with_behaviors_directory(tmp_path, "story_bot")
        given_behavior_with_valid_json(bot_dir, "shape")
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        when_generator_runs(bot_dir, workspace_dir)

        rule_file = workspace_dir / ".cursor" / "rules" / "story_bot_shape.mdc"
        assert rule_file.exists()
        content = rule_file.read_text(encoding="utf-8")
        assert "# story_bot shape Behavior" in content
        assert "Goal" in content
        assert "Inputs" in content
        assert "Outputs" in content

    def test_generator_adds_trigger_words_section_from_behavior_json_patterns(self, tmp_path):
        bot_dir = given_bot_with_behaviors_directory(tmp_path, "story_bot")
        behavior_dir = bot_dir / "behaviors" / "shape"
        behavior_dir.mkdir(parents=True)
        behavior_json = {
            "behaviorName": "shape",
            "description": "Test",
            "goal": "Test",
            "inputs": "",
            "outputs": "",
            "trigger_words": {"patterns": [r"shape\s+story", r"create\s+story\s+map"]},
        }
        (behavior_dir / "behavior.json").write_text(json.dumps(behavior_json, indent=2), encoding="utf-8")
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        when_generator_runs(bot_dir, workspace_dir)

        rule_file = workspace_dir / ".cursor" / "rules" / "story_bot_shape.mdc"
        content = rule_file.read_text(encoding="utf-8")
        assert "## When to use this behavior" in content
        assert "Use this behavior when:" in content

    def test_generator_merges_clarification_section_from_guardrails_and_base_actions(self, tmp_path):
        bot_dir = given_bot_with_behaviors_directory(tmp_path, "story_bot")
        given_behavior_with_valid_json(bot_dir, "shape")
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        when_generator_runs(bot_dir, workspace_dir)

        rule_file = workspace_dir / ".cursor" / "rules" / "story_bot_shape.mdc"
        content = rule_file.read_text(encoding="utf-8")
        assert "## Clarification" in content
        assert "NOT ENOUGH INFORMATION" in content

    def test_generator_merges_strategy_section_from_guardrails_and_base_actions(self, tmp_path):
        bot_dir = given_bot_with_behaviors_directory(tmp_path, "story_bot")
        given_behavior_with_valid_json(bot_dir, "shape")
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        when_generator_runs(bot_dir, workspace_dir)

        rule_file = workspace_dir / ".cursor" / "rules" / "story_bot_shape.mdc"
        content = rule_file.read_text(encoding="utf-8")
        assert "## Strategy" in content

    def test_generator_adds_build_section_with_rules_and_embedded_templates(self, tmp_path):
        bot_dir = given_bot_with_behaviors_directory(tmp_path, "story_bot")
        behavior_dir = given_behavior_with_valid_json(bot_dir, "shape")
        render_dir = behavior_dir / "content" / "render"
        render_dir.mkdir(parents=True)
        templates_dir = render_dir / "templates"
        templates_dir.mkdir()
        (templates_dir / "story-map.txt").write_text("Story Map Template", encoding="utf-8")
        (render_dir / "render_story_map.json").write_text(
            json.dumps({
                "template": "templates/story-map.txt",
                "output": "story-map.txt",
            }),
            encoding="utf-8",
        )
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        when_generator_runs(bot_dir, workspace_dir)

        rule_file = workspace_dir / ".cursor" / "rules" / "story_bot_shape.mdc"
        content = rule_file.read_text(encoding="utf-8")
        assert "## Build" in content
        assert "Now you're ready to build" in content
        assert "### Rules" in content
        assert "### Templates" in content
        assert "#### story-map.txt" in content
        assert "Story Map Template" in content

    def test_generator_processes_rules_directory_and_formats_do_dont_blocks(self, tmp_path):
        bot_dir = given_bot_with_behaviors_directory(tmp_path, "story_bot")
        given_behavior_with_valid_json(bot_dir, "shape")
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        when_generator_runs(bot_dir, workspace_dir)

        rule_file = workspace_dir / ".cursor" / "rules" / "story_bot_shape.mdc"
        content = rule_file.read_text(encoding="utf-8")
        assert "## Rules" in content
        assert "DO" in content or "DON'T" in content

    def test_generator_outputs_mdc_files_to_workspace_cursor_rules_folder(self, tmp_path):
        bot_dir = given_bot_with_behaviors_directory(tmp_path, "story_bot")
        given_behavior_with_valid_json(bot_dir, "shape")
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        result = when_generator_runs(bot_dir, workspace_dir)

        then_rule_files_exist_in_cursor_rules(workspace_dir, expected_count=1)
        assert "created_files" in result or "summary" in result

    def test_generator_skips_behavior_when_behavior_json_is_malformed(self, tmp_path):
        bot_dir = given_bot_with_behaviors_directory(tmp_path, "story_bot")
        given_behavior_with_valid_json(bot_dir, "shape")
        malformed_dir = bot_dir / "behaviors" / "broken"
        malformed_dir.mkdir()
        (malformed_dir / "behavior.json").write_text("{ invalid json", encoding="utf-8")
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        result = when_generator_runs(bot_dir, workspace_dir)

        then_rule_files_exist_in_cursor_rules(workspace_dir, expected_count=1)
        rule_file = workspace_dir / ".cursor" / "rules" / "story_bot_shape.mdc"
        assert rule_file.exists()

    def test_generator_produces_rule_file_when_bot_has_single_behavior(self, tmp_path):
        bot_name = "story_bot"
        behavior_name = "shape"
        bot_dir = given_bot_with_behaviors_directory(tmp_path, bot_name)
        given_behavior_with_valid_json(bot_dir, behavior_name)
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        when_generator_runs(bot_dir, workspace_dir)

        rule_file = workspace_dir / ".cursor" / "rules" / f"{bot_name}_{behavior_name}.mdc"
        assert rule_file.exists()
        assert rule_file.suffix == ".mdc"


class TestGenerateContextPackageViaCLI:
    """Generate context package via CLI - command executes on active bot."""

    def test_cli_generate_context_package_creates_rule_files_for_active_bot(self, tmp_path):
        bot_name = "story_bot"
        bot_dir = given_bot_with_behaviors_directory(tmp_path, bot_name)
        given_behavior_with_valid_json(bot_dir, "shape")
        (bot_dir / "bot_config.json").write_text(
            json.dumps({"name": bot_name, "behaviors": ["shape"]}, indent=2),
            encoding="utf-8",
        )
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        os.environ["BOT_DIRECTORY"] = str(bot_dir)
        os.environ["WORKING_AREA"] = str(workspace_dir)
        from bot.bot import Bot

        bot = Bot(
            bot_name=bot_name,
            bot_directory=bot_dir,
            config_path=bot_dir / "bot_config.json",
            workspace_path=workspace_dir,
        )
        cli_session = CLISession(bot=bot, workspace_directory=workspace_dir)

        response = cli_session.execute_command("generate_context_package")

        assert response.status == "success"
        then_rule_files_exist_in_cursor_rules(workspace_dir, expected_count=1)
        rule_file = workspace_dir / ".cursor" / "rules" / f"{bot_name}_shape.mdc"
        assert rule_file.exists()

    def test_cli_generate_context_package_accepts_generate_context_package_syntax(self, tmp_path):
        bot_name = "story_bot"
        bot_dir = given_bot_with_behaviors_directory(tmp_path, bot_name)
        given_behavior_with_valid_json(bot_dir, "shape")
        (bot_dir / "bot_config.json").write_text(
            json.dumps({"name": bot_name, "behaviors": ["shape"]}, indent=2),
            encoding="utf-8",
        )
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()

        os.environ["BOT_DIRECTORY"] = str(bot_dir)
        os.environ["WORKING_AREA"] = str(workspace_dir)
        from bot.bot import Bot

        bot = Bot(
            bot_name=bot_name,
            bot_directory=bot_dir,
            config_path=bot_dir / "bot_config.json",
            workspace_path=workspace_dir,
        )
        cli_session = CLISession(bot=bot, workspace_directory=workspace_dir)

        response = cli_session.execute_command("generate context package")

        assert response.status == "success"
        then_rule_files_exist_in_cursor_rules(workspace_dir, expected_count=1)
