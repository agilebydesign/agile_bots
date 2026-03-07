"""
Skill File Generator

Generates abd-{bot}-{behavior} skills from bot behaviors.
Output: workspace skills/{skill_name}/ with SKILL.md, content/*.md, rules/*.md, scripts/build.py, skill-config.json
"""
import json
import re
from pathlib import Path
from typing import Dict, Any, List

from .rule_json_to_markdown import RuleJsonToMarkdownAdapter


_BEHAVIOR_SLUG_OVERRIDES: Dict[str, str] = {
    "shape": "shaping",
}


def _skill_name_from_bot_behavior(bot_name: str, behavior_name: str) -> str:
    """abd-story-shaping, abd-crc-domain."""
    bot_slug = bot_name.replace("_bot", "").replace("_", "-")
    behavior_slug = _BEHAVIOR_SLUG_OVERRIDES.get(behavior_name, behavior_name).replace("_", "-")
    return f"abd-{bot_slug}-{behavior_slug}"


class SkillFileGenerator:
    """Generates skill directories from bot behaviors."""

    def __init__(self, bots_root: Path, skills_output: Path):
        """Initialize with bots root and skills output path.

        Args:
            bots_root: Path to bots directory (e.g. agile_bots/bots)
            skills_output: Path for output skills (e.g. agile_bots/skills)
        """
        self.bots_root = Path(bots_root)
        self.skills_output = Path(skills_output)
        self.rule_adapter = RuleJsonToMarkdownAdapter()

    def generate(self) -> Dict[str, Any]:
        """Run skill generation. Creates skill directories under skills_output.

        Returns:
            Dict with created_skills, created_files, and summary
        """
        created_skills: List[str] = []
        created_files: List[str] = []

        if not self.bots_root.exists():
            return {"created_skills": [], "created_files": [], "summary": "No bots directory"}

        for bot_dir in sorted(self.bots_root.iterdir()):
            if not bot_dir.is_dir() or bot_dir.name.startswith("."):
                continue
            behaviors_dir = bot_dir / "behaviors"
            if not behaviors_dir.exists():
                continue
            bot_name = bot_dir.name

            for behavior_dir in sorted(behaviors_dir.iterdir()):
                if not behavior_dir.is_dir():
                    continue
                behavior_name = behavior_dir.name
                behavior_json = self._load_behavior_json(behavior_dir)
                if behavior_json is None:
                    continue

                skill_name = _skill_name_from_bot_behavior(bot_name, behavior_name)
                skill_path = self.skills_output / skill_name
                skill_path.mkdir(parents=True, exist_ok=True)

                files = self._generate_skill(skill_name, bot_name, behavior_name, behavior_json, behavior_dir, skill_path)
                created_skills.append(skill_name)
                created_files.extend(files)

        return {
            "created_skills": created_skills,
            "created_files": created_files,
            "summary": f"Created {len(created_skills)} skills",
        }

    def _load_behavior_json(self, behavior_dir: Path) -> Dict[str, Any] | None:
        behavior_file = behavior_dir / "behavior.json"
        if not behavior_file.exists():
            return None
        try:
            return json.loads(behavior_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None

    def _generate_skill(
        self,
        skill_name: str,
        bot_name: str,
        behavior_name: str,
        behavior: Dict[str, Any],
        behavior_dir: Path,
        skill_path: Path,
    ) -> List[str]:
        """Generate one skill directory. Returns list of created file paths."""
        created: List[str] = []

        # SKILL.md
        skill_md = self._build_skill_md(skill_name, bot_name, behavior_name, behavior, behavior_dir)
        (skill_path / "SKILL.md").write_text(skill_md, encoding="utf-8")
        created.append(str(skill_path / "SKILL.md"))

        # content/
        content_dir = skill_path / "content"
        content_dir.mkdir(exist_ok=True)
        core_md = self._build_content_core(bot_name, behavior_name, behavior, behavior_dir)
        (content_dir / "core.md").write_text(core_md, encoding="utf-8")
        created.append(str(content_dir / "core.md"))
        # content/process.md from actions_workflow
        process_md = self._build_content_process(behavior)
        if process_md:
            (content_dir / "process.md").write_text(process_md, encoding="utf-8")
            created.append(str(content_dir / "process.md"))
        # content/output.md from outputs
        output_md = self._build_content_output(behavior)
        if output_md:
            (content_dir / "output.md").write_text(output_md, encoding="utf-8")
            created.append(str(content_dir / "output.md"))
        # Copy behavior content/*.md (e.g. README.md)
        for fp in self._copy_behavior_content_md(behavior_dir, content_dir):
            created.append(str(fp))

        # rules/*.md
        rules_dir = skill_path / "rules"
        rules_dir.mkdir(exist_ok=True)
        rule_files = list(self._generate_rules_markdown(behavior_dir, rules_dir))
        for fp in rule_files:
            created.append(str(fp))
        if not rule_files:
            readme = rules_dir / "README.md"
            readme.write_text(
                "# Rules\n\nNo behavior-specific rules. Apply general quality and domain guidelines.\n",
                encoding="utf-8",
            )
            created.append(str(readme))

        # skill-config.json
        config = {
            "name": skill_name,
            "version": "1.0.0",
            "bot_path": f"../../bots/{bot_name}/behaviors/{behavior_name}",
        }
        (skill_path / "skill-config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
        created.append(str(skill_path / "skill-config.json"))

        # scripts/build.py
        scripts_dir = skill_path / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        build_py = self._build_script_py(skill_name)
        (scripts_dir / "build.py").write_text(build_py, encoding="utf-8")
        created.append(str(scripts_dir / "build.py"))

        return created

    def _build_skill_md(
        self,
        skill_name: str,
        bot_name: str,
        behavior_name: str,
        behavior: Dict[str, Any],
        behavior_dir: Path,
    ) -> str:
        desc = behavior.get("description", "")
        goal = behavior.get("goal", "")
        parts = [
            "---",
            f"name: {skill_name}",
            f"description: {desc} Use when {goal.lower()}.",
            "license: MIT",
            "metadata:",
            "  author: agilebydesign",
            '  version: "1.0.0"',
            "---",
            "",
            f"# {skill_name.replace('-', ' ').title()}",
            "",
            desc,
            "",
            "## When to Apply",
            "",
            f"Use this skill when: {goal}",
            "",
            "## Rules",
            "",
            "See `rules/` for DO/DO NOT guidance.",
            "",
        ]
        self._add_trigger_words(behavior, parts)
        return "\n".join(parts).rstrip()

    def _add_trigger_words(self, behavior: Dict[str, Any], parts: List[str]) -> None:
        trigger = behavior.get("trigger_words", {}) or {}
        patterns = trigger.get("patterns", [])
        if not patterns:
            return
        parts.append("## Trigger Patterns")
        parts.append("")
        for p in patterns[:10]:
            natural = re.sub(r"\\[a-zA-Z]", "", p.replace(r"\s+", " ").replace(r".*", " "))
            parts.append(f"- {natural.strip() or p}")
        if len(patterns) > 10:
            parts.append(f"- ... and {len(patterns) - 10} more")
        parts.append("")

    def _build_content_core(
        self,
        bot_name: str,
        behavior_name: str,
        behavior: Dict[str, Any],
        behavior_dir: Path,
    ) -> str:
        parts = [
            "# Core Definitions",
            "",
            "## Behavior",
            "",
            f"**{behavior_name}** — {behavior.get('description', '')}",
            "",
            "## Goal",
            "",
            behavior.get("goal", ""),
            "",
            "## Inputs",
            "",
            behavior.get("inputs", ""),
            "",
            "## Outputs",
            "",
            self._filter_story_graph_refs(behavior.get("outputs", "")),
            "",
        ]
        self._add_guardrails_sections(behavior_dir, parts)
        return "\n".join(parts).rstrip()

    def _build_content_process(self, behavior: Dict[str, Any]) -> str:
        """Build process.md from actions_workflow."""
        workflow = behavior.get("actions_workflow", {}) or {}
        actions = workflow.get("actions", [])
        if not actions:
            return ""
        parts = ["# Process", "", "## Action Flow", ""]
        for i, a in enumerate(actions, 1):
            name = a.get("name", "")
            instructions = a.get("instructions", [])
            inst_text = " ".join(s for s in instructions if isinstance(s, str) and s.strip())
            parts.append(f"### {i}. {name}")
            parts.append("")
            if inst_text:
                parts.append(inst_text[:500] + ("..." if len(inst_text) > 500 else ""))
            parts.append("")
        return "\n".join(parts).rstrip()

    def _build_content_output(self, behavior: Dict[str, Any]) -> str:
        """Build output.md from behavior outputs."""
        outputs = behavior.get("outputs", "")
        if not outputs:
            return ""
        parts = ["# Outputs", "", "## Artifacts", ""]
        for item in [s.strip().rstrip(",") for s in outputs.replace(",", "\n").split("\n") if s.strip()]:
            parts.append(f"- {item}")
        parts.append("")
        return "\n".join(parts).rstrip()

    def _copy_behavior_content_md(self, behavior_dir: Path, content_dir: Path) -> List[Path]:
        """Copy behavior content/*.md into skill content/ (avoid overwriting core/process/output)."""
        src = behavior_dir / "content"
        created: List[Path] = []
        if not src.exists():
            return created
        reserved = {"core", "process", "output"}
        for f in src.glob("*.md"):
            if f.stem.lower() in reserved:
                continue
            out_path = content_dir / f.name
            try:
                out_path.write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
                created.append(out_path)
            except (OSError, UnicodeDecodeError):
                pass
        return created

    def _add_guardrails_sections(self, behavior_dir: Path, parts: List[str]) -> None:
        guardrails = behavior_dir / "guardrails"
        if not guardrails.exists():
            return
        # Key questions from required_context
        req_ctx = guardrails / "required_context"
        if req_ctx.exists():
            for f in req_ctx.glob("*.json"):
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    questions = data.get("key_questions", [])
                    if questions:
                        parts.append("## Key Questions")
                        parts.append("")
                        for q in questions:
                            text = q.get("question", q) if isinstance(q, dict) else str(q)
                            parts.append(f"- {text}")
                        parts.append("")
                except (json.JSONDecodeError, OSError):
                    pass

    def _filter_story_graph_refs(self, text: str) -> str:
        if not text:
            return text
        lines = text.replace(",", "\n").split("\n")
        filtered = [
            line.strip().rstrip(",")
            for line in lines
            if line.strip()
            and "story-graph" not in line.lower()
            and "story graph" not in line.lower()
        ]
        return ", ".join(filtered) if filtered else ""

    def _generate_rules_markdown(self, behavior_dir: Path, rules_dir: Path) -> List[Path]:
        rules_src = behavior_dir / "rules"
        created: List[Path] = []
        if not rules_src.exists():
            return created
        rule_files: List[tuple[int, Path]] = []
        for f in rules_src.glob("*.json"):
            if f.parent.name == "disabled":
                continue
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                rule_files.append((data.get("priority", 99), f))
            except (json.JSONDecodeError, OSError):
                pass
        rule_files.sort(key=lambda x: x[0])
        for _, f in rule_files:
            md_content = self.rule_adapter.convert_file(f)
            if md_content:
                md_name = f.stem.replace("_", "-") + ".md"
                out_path = rules_dir / md_name
                out_path.write_text(md_content, encoding="utf-8")
                created.append(out_path)
        return created

    def _build_script_py(self, skill_name: str) -> str:
        return f'''"""Build AGENTS.md for {skill_name}. Portable skill for skills.sh install."""
from pathlib import Path

_CONTENT_ORDER = ["core", "process", "output", "strategy", "validation", "script-invocation"]
_CONTENT_STEMS = {{s.lower() for s in _CONTENT_ORDER}}


def main():
    skill_dir = Path(__file__).resolve().parent.parent
    content_dir = skill_dir / "content"
    rules_dir = skill_dir / "rules"
    out_path = skill_dir / "AGENTS.md"

    parts = []
    # Content in defined order
    for stem in _CONTENT_ORDER:
        f = content_dir / (stem + ".md")
        if f.exists():
            parts.append(f.read_text(encoding="utf-8"))
    # Remaining content/*.md alphabetically
    for f in sorted(content_dir.glob("*.md")):
        if f.stem.lower() not in _CONTENT_STEMS:
            parts.append(f.read_text(encoding="utf-8"))
    # Rules
    if rules_dir.exists():
        for f in sorted(rules_dir.glob("*.md")):
            parts.append(f.read_text(encoding="utf-8"))

    out_path.write_text("\\n\\n---\\n\\n".join(parts), encoding="utf-8")
    print(f"Wrote {{out_path}}")
    return str(out_path)


if __name__ == "__main__":
    main()
'''
