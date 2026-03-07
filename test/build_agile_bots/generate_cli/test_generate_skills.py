"""
Test Generate Skills

SubEpic: Generate Skills
Parent Epic: Build Agile Bots > Generate CLI

Story: Create Skill Files From Bot Behavior
Domain tests verify skill file generation from bot behaviors.
CLI tests verify generate_skills command executes on active bot.
All tests use tmp_path - no writes to production bot workspace.
"""
import json
import os
import pytest
from pathlib import Path

from cli.cli_session import CLISession
from synchronizers.context_package.skill_file_generator import SkillFileGenerator, _skill_name_from_bot_behavior


def given_bots_root_with_behavior(tmp_path: Path, bot_name: str, behavior_name: str) -> Path:
    """Given: Bots root exists with bot/behaviors/behavior directory."""
    bot_dir = tmp_path / "bots" / bot_name
    behavior_dir = bot_dir / "behaviors" / behavior_name
    behavior_dir.mkdir(parents=True)
    return tmp_path / "bots"


def given_behavior_with_valid_json(bots_root: Path, bot_name: str, behavior_name: str) -> Path:
    """Given: Behavior has valid behavior.json with behaviorName, description, goal, inputs, outputs."""
    behavior_dir = bots_root / bot_name / "behaviors" / behavior_name
    behavior_json = {
        "behaviorName": behavior_name,
        "description": "Test behavior",
        "goal": "Test goal",
        "inputs": "test inputs",
        "outputs": "test outputs",
    }
    (behavior_dir / "behavior.json").write_text(json.dumps(behavior_json, indent=2), encoding="utf-8")
    return behavior_dir


def when_generator_runs(bots_root: Path, skills_output: Path) -> dict:
    """When: Skill generator runs."""
    generator = SkillFileGenerator(bots_root=bots_root, skills_output=skills_output)
    return generator.generate()


def then_skill_directory_exists(skills_output: Path, skill_name: str) -> Path:
    """Then: Skill directory exists under skills_output."""
    skill_path = skills_output / skill_name
    assert skill_path.exists(), f"Expected skill directory at {skill_path}"
    assert skill_path.is_dir()
    return skill_path


def then_skill_has_required_files(skill_path: Path) -> None:
    """Then: Skill has SKILL.md, content/core.md, rules/, skill-config.json, scripts/build.py."""
    assert (skill_path / "SKILL.md").exists(), f"Expected SKILL.md at {skill_path}"
    assert (skill_path / "content" / "core.md").exists(), f"Expected content/core.md at {skill_path}"
    assert (skill_path / "skill-config.json").exists(), f"Expected skill-config.json at {skill_path}"
    assert (skill_path / "scripts" / "build.py").exists(), f"Expected scripts/build.py at {skill_path}"


class TestCreateSkillFilesFromBotBehavior:
    """Create Skill Files From Bot Behavior - Generator produces skill directories from bot behaviors."""

    def test_skill_name_from_bot_behavior_produces_abd_prefix(self):
        assert _skill_name_from_bot_behavior("story_bot", "shape") == "abd-story-shaping"
        assert _skill_name_from_bot_behavior("crc_bot", "domain") == "abd-crc-domain"
        assert _skill_name_from_bot_behavior("story_bot", "exploration") == "abd-story-exploration"

    def test_generator_produces_skill_per_behavior_when_bot_has_valid_behaviors(self, tmp_path):
        bots_root = given_bots_root_with_behavior(tmp_path, "story_bot", "shape")
        given_behavior_with_valid_json(bots_root, "story_bot", "shape")
        skills_output = tmp_path / "skills"
        skills_output.mkdir()

        result = when_generator_runs(bots_root, skills_output)

        assert "created_skills" in result
        assert "abd-story-shaping" in result["created_skills"]
        skill_path = then_skill_directory_exists(skills_output, "abd-story-shaping")
        then_skill_has_required_files(skill_path)

    def test_generator_writes_skill_md_with_yaml_frontmatter_and_sections(self, tmp_path):
        bots_root = given_bots_root_with_behavior(tmp_path, "story_bot", "shape")
        given_behavior_with_valid_json(bots_root, "story_bot", "shape")
        skills_output = tmp_path / "skills"
        skills_output.mkdir()

        when_generator_runs(bots_root, skills_output)

        skill_md = (skills_output / "abd-story-shaping" / "SKILL.md").read_text(encoding="utf-8")
        assert "---" in skill_md
        assert "name: abd-story-shaping" in skill_md
        assert "description:" in skill_md
        assert "## When to Apply" in skill_md
        assert "## Rules" in skill_md

    def test_generator_writes_content_core_with_behavior_goal_inputs_outputs(self, tmp_path):
        bots_root = given_bots_root_with_behavior(tmp_path, "story_bot", "shape")
        given_behavior_with_valid_json(bots_root, "story_bot", "shape")
        skills_output = tmp_path / "skills"
        skills_output.mkdir()

        when_generator_runs(bots_root, skills_output)

        core_md = (skills_output / "abd-story-shaping" / "content" / "core.md").read_text(encoding="utf-8")
        assert "## Behavior" in core_md
        assert "## Goal" in core_md
        assert "## Inputs" in core_md
        assert "## Outputs" in core_md
        assert "Test behavior" in core_md
        assert "Test goal" in core_md

    def test_generator_converts_rules_json_to_markdown_when_rules_exist(self, tmp_path):
        bots_root = given_bots_root_with_behavior(tmp_path, "story_bot", "shape")
        behavior_dir = given_behavior_with_valid_json(bots_root, "story_bot", "shape")
        rules_dir = behavior_dir / "rules"
        rules_dir.mkdir()
        (rules_dir / "valuable.json").write_text(
            json.dumps({
                "priority": 5,
                "description": "Stories must capture discrete behavior",
                "do": {"description": "Create stories that capture discrete behavior"},
                "dont": {"description": "Don't create raw data operations"},
            }),
            encoding="utf-8",
        )
        skills_output = tmp_path / "skills"
        skills_output.mkdir()

        when_generator_runs(bots_root, skills_output)

        rules_out = skills_output / "abd-story-shaping" / "rules"
        assert rules_out.exists()
        md_files = list(rules_out.glob("*.md"))
        assert len(md_files) >= 1
        valuable_md = rules_out / "valuable.md"
        assert valuable_md.exists()
        content = valuable_md.read_text(encoding="utf-8")
        assert "**DO**" in content
        assert "**DO NOT**" in content

    def test_generator_writes_skill_config_with_bot_path(self, tmp_path):
        bots_root = given_bots_root_with_behavior(tmp_path, "story_bot", "shape")
        given_behavior_with_valid_json(bots_root, "story_bot", "shape")
        skills_output = tmp_path / "skills"
        skills_output.mkdir()

        when_generator_runs(bots_root, skills_output)

        config = json.loads((skills_output / "abd-story-shaping" / "skill-config.json").read_text(encoding="utf-8"))
        assert config["name"] == "abd-story-shaping"
        assert config["version"] == "1.0.0"
        assert "story_bot" in config["bot_path"]
        assert "shape" in config["bot_path"]

    def test_generator_writes_scripts_build_py(self, tmp_path):
        bots_root = given_bots_root_with_behavior(tmp_path, "story_bot", "shape")
        given_behavior_with_valid_json(bots_root, "story_bot", "shape")
        skills_output = tmp_path / "skills"
        skills_output.mkdir()

        when_generator_runs(bots_root, skills_output)

        build_py = (skills_output / "abd-story-shaping" / "scripts" / "build.py").read_text(encoding="utf-8")
        assert "abd-story-shaping" in build_py
        assert "def main" in build_py
        assert "AGENTS.md" in build_py

    def test_build_py_produces_agents_md_for_skills_sh_portability(self, tmp_path):
        """Then: Running build.py produces AGENTS.md (portable skill for skills.sh)."""
        bots_root = given_bots_root_with_behavior(tmp_path, "story_bot", "shape")
        given_behavior_with_valid_json(bots_root, "story_bot", "shape")
        skills_output = tmp_path / "skills"
        skills_output.mkdir()

        when_generator_runs(bots_root, skills_output)

        skill_path = skills_output / "abd-story-shaping"
        build_script = skill_path / "scripts" / "build.py"
        assert build_script.exists()

        import subprocess
        result = subprocess.run(
            [os.environ.get("PYTHON", "python"), str(build_script)],
            cwd=str(skill_path),
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr or result.stdout

        agents_md = skill_path / "AGENTS.md"
        assert agents_md.exists(), "build.py should produce AGENTS.md"
        content = agents_md.read_text(encoding="utf-8")
        assert "Core Definitions" in content
        assert "Test behavior" in content

    def test_generator_adds_trigger_patterns_section_when_behavior_has_trigger_words(self, tmp_path):
        bots_root = given_bots_root_with_behavior(tmp_path, "story_bot", "shape")
        behavior_dir = bots_root / "story_bot" / "behaviors" / "shape"
        (behavior_dir / "behavior.json").write_text(
            json.dumps({
                "behaviorName": "shape",
                "description": "Test",
                "goal": "Test",
                "inputs": "",
                "outputs": "",
                "trigger_words": {"patterns": [r"shape\s+story", r"create\s+story\s+map"]},
            }, indent=2),
            encoding="utf-8",
        )
        skills_output = tmp_path / "skills"
        skills_output.mkdir()

        when_generator_runs(bots_root, skills_output)

        skill_md = (skills_output / "abd-story-shaping" / "SKILL.md").read_text(encoding="utf-8")
        assert "## Trigger Patterns" in skill_md

    def test_generator_skips_behavior_when_behavior_json_is_malformed(self, tmp_path):
        bots_root = given_bots_root_with_behavior(tmp_path, "story_bot", "shape")
        given_behavior_with_valid_json(bots_root, "story_bot", "shape")
        broken_dir = bots_root / "story_bot" / "behaviors" / "broken"
        broken_dir.mkdir()
        (broken_dir / "behavior.json").write_text("{ invalid json", encoding="utf-8")
        skills_output = tmp_path / "skills"
        skills_output.mkdir()

        result = when_generator_runs(bots_root, skills_output)

        assert "abd-story-shaping" in result["created_skills"]
        assert (skills_output / "abd-story-shaping").exists()
        assert not (skills_output / "abd-story-broken").exists()

    def test_generator_produces_multiple_skills_for_multiple_behaviors(self, tmp_path):
        bots_root = given_bots_root_with_behavior(tmp_path, "story_bot", "shape")
        given_behavior_with_valid_json(bots_root, "story_bot", "shape")
        exploration_dir = bots_root / "story_bot" / "behaviors" / "exploration"
        exploration_dir.mkdir()
        (exploration_dir / "behavior.json").write_text(
            json.dumps({
                "behaviorName": "exploration",
                "description": "Explore stories",
                "goal": "Explore",
                "inputs": "",
                "outputs": "",
            }, indent=2),
            encoding="utf-8",
        )
        skills_output = tmp_path / "skills"
        skills_output.mkdir()

        result = when_generator_runs(bots_root, skills_output)

        assert "abd-story-shaping" in result["created_skills"]
        assert "abd-story-exploration" in result["created_skills"]
        assert (skills_output / "abd-story-shaping").exists()
        assert (skills_output / "abd-story-exploration").exists()

    def test_generator_produces_skills_for_scenarios_tests_code_like_shape(self, tmp_path):
        """Scenarios, tests, and code behaviors produce skills with rules same as shape (Create Rule Files From Bot Behavior)."""
        bots_root = tmp_path / "bots"
        bots_root.mkdir()
        for behavior_name in ["shape", "scenarios", "tests", "code"]:
            given_bots_root_with_behavior(tmp_path, "story_bot", behavior_name)
            behavior_dir = given_behavior_with_valid_json(bots_root, "story_bot", behavior_name)
            rules_dir = behavior_dir / "rules"
            rules_dir.mkdir(exist_ok=True)
            (rules_dir / "example_rule.json").write_text(
                json.dumps({
                    "priority": 1,
                    "description": f"Rule for {behavior_name}",
                    "do": {"description": "Do this"},
                    "dont": {"description": "Don't do that"},
                }),
                encoding="utf-8",
            )
        skills_output = tmp_path / "skills"
        skills_output.mkdir()

        result = when_generator_runs(bots_root, skills_output)

        expected_skills = ["abd-story-shaping", "abd-story-scenarios", "abd-story-tests", "abd-story-code"]
        for skill_name in expected_skills:
            assert skill_name in result["created_skills"], f"Expected skill {skill_name}"
            skill_path = skills_output / skill_name
            assert skill_path.exists(), f"Expected skill dir at {skill_path}"
            then_skill_has_required_files(skill_path)
            rules_out = skill_path / "rules"
            assert rules_out.exists(), f"Expected rules/ for {skill_name}"
            md_files = list(rules_out.glob("*.md"))
            assert len(md_files) >= 1, f"Expected at least one rule .md for {skill_name}"


class TestGenerateSkillsViaCLI:
    """Generate skills via CLI - command executes on active bot."""

    def test_cli_generate_skills_creates_skill_directories_for_all_bots(self, tmp_path):
        bots_root = given_bots_root_with_behavior(tmp_path, "story_bot", "shape")
        given_behavior_with_valid_json(bots_root, "story_bot", "shape")
        (bots_root / "story_bot" / "bot_config.json").write_text(
            json.dumps({"name": "story_bot", "behaviors": ["shape"]}, indent=2),
            encoding="utf-8",
        )
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()
        bot_dir = bots_root / "story_bot"

        os.environ["BOT_DIRECTORY"] = str(bot_dir)
        os.environ["WORKING_AREA"] = str(workspace_dir)
        from bot.bot import Bot

        bot = Bot(
            bot_name="story_bot",
            bot_directory=bot_dir,
            config_path=bot_dir / "bot_config.json",
            workspace_path=workspace_dir,
        )
        cli_session = CLISession(bot=bot, workspace_directory=workspace_dir)

        response = cli_session.execute_command("generate_skills")

        assert response.status == "success"
        skills_dir = workspace_dir / "skills"
        assert skills_dir.exists()
        assert (skills_dir / "abd-story-shaping").exists()

    def test_cli_generate_skills_accepts_generate_skills_syntax(self, tmp_path):
        bots_root = given_bots_root_with_behavior(tmp_path, "story_bot", "shape")
        given_behavior_with_valid_json(bots_root, "story_bot", "shape")
        (bots_root / "story_bot" / "bot_config.json").write_text(
            json.dumps({"name": "story_bot", "behaviors": ["shape"]}, indent=2),
            encoding="utf-8",
        )
        workspace_dir = tmp_path / "workspace"
        workspace_dir.mkdir()
        bot_dir = bots_root / "story_bot"

        os.environ["BOT_DIRECTORY"] = str(bot_dir)
        os.environ["WORKING_AREA"] = str(workspace_dir)
        from bot.bot import Bot

        bot = Bot(
            bot_name="story_bot",
            bot_directory=bot_dir,
            config_path=bot_dir / "bot_config.json",
            workspace_path=workspace_dir,
        )
        cli_session = CLISession(bot=bot, workspace_directory=workspace_dir)

        response = cli_session.execute_command("generate skills")

        assert response.status == "success"
        assert (workspace_dir / "skills" / "abd-story-shaping").exists()
