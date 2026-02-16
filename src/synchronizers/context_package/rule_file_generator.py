"""
Rule File Generator

Generates .mdc rule files from bot behavior.json files.
Output: workspace .cursor/rules/{bot_name}_{behavior}.mdc
"""
import json
import re
from pathlib import Path
from typing import Dict, Any, List


class RuleFileGenerator:
    """Generates .mdc rule files from bot behaviors for Cursor context package."""

    def __init__(self, bot_directory: Path, workspace_directory: Path):
        """Initialize with bot and workspace paths.

        Args:
            bot_directory: Path to bot directory (e.g. bots/story_bot)
            workspace_directory: Path to workspace for output .cursor/rules/
        """
        self.bot_directory = Path(bot_directory)
        self.workspace_directory = Path(workspace_directory)

    def generate(self) -> Dict[str, Any]:
        """Run generate context package command. Creates .mdc files in workspace .cursor/rules/.

        Returns:
            Dict with created_files, updated_files, and summary
        """
        bot_name = self.bot_directory.name
        behaviors_dir = self.bot_directory / "behaviors"
        created_files: List[str] = []

        if not behaviors_dir.exists():
            return {"created_files": [], "summary": "No behaviors directory"}

        for behavior_dir in sorted(behaviors_dir.iterdir()):
            if not behavior_dir.is_dir():
                continue
            behavior_name = behavior_dir.name
            behavior_json = self._load_behavior_json(behavior_dir)
            if behavior_json is None:
                continue
            content = self._build_rule_content(bot_name, behavior_name, behavior_json, behavior_dir)
            output_path = self._write_rule_file(bot_name, behavior_name, content)
            if output_path:
                created_files.append(str(output_path))

        return {"created_files": created_files, "summary": f"Created {len(created_files)} rule files"}

    def _load_behavior_json(self, behavior_dir: Path) -> Dict[str, Any] | None:
        behavior_file = behavior_dir / "behavior.json"
        if not behavior_file.exists():
            return None
        try:
            return json.loads(behavior_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None

    def _build_rule_content(
        self, bot_name: str, behavior_name: str, behavior: Dict[str, Any], behavior_dir: Path
    ) -> str:
        parts: List[str] = []

        parts.append(f"# {bot_name} {behavior_name} Behavior")
        parts.append("")
        parts.append(behavior.get("description", ""))
        parts.append("")
        parts.append("## Goal")
        parts.append(behavior.get("goal", ""))
        parts.append("")
        parts.append("## Inputs")
        parts.append(behavior.get("inputs", ""))
        parts.append("")
        parts.append("## Outputs")
        outputs = self._filter_story_graph_refs(behavior.get("outputs", ""))
        parts.append(outputs)
        parts.append("")

        self._add_trigger_words_section(behavior, parts)
        self._add_clarification_section(behavior_dir, behavior, parts)
        self._add_strategy_section(behavior_dir, behavior, parts)
        self._add_build_section(behavior_dir, behavior, parts)

        return "\n".join(parts).rstrip()

    def _add_trigger_words_section(self, behavior: Dict[str, Any], parts: List[str]) -> None:
        trigger = behavior.get("trigger_words", {}) or {}
        patterns = trigger.get("patterns", [])
        if not patterns:
            return
        parts.append("## When to use this behavior")
        parts.append("")
        parts.append("Use this behavior when:")
        for pattern in patterns:
            natural = self._regex_to_natural_language(pattern)
            parts.append(f"- {natural}")
        parts.append("")

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

    def _regex_to_natural_language(self, pattern: str) -> str:
        text = pattern.replace(r"\s+", " ").replace(r".*", " ").replace(".*", " ")
        text = re.sub(r"\\[a-zA-Z]", "", text)
        return text.strip() or pattern

    def _add_clarification_section(
        self, behavior_dir: Path, behavior: Dict[str, Any], parts: List[str]
    ) -> None:
        parts.append("## Clarification")
        parts.append("")
        parts.append(
            "Go through the context provided and answer the following questions. "
            "If you cannot answer a question from the available context, state "
            "[!] NOT ENOUGH INFORMATION - REQUIRES USER INPUT; do not guess or infer. "
            "Show these answers to the user before proceeding to strategy. "
            "Store answers in clarification.json for later session and save to clarification.strategy."
        )
        parts.append("")
        required = behavior_dir / "guardrails" / "required_context"
        if required.exists():
            key_questions = required / "key_questions.json"
            if key_questions.exists():
                try:
                    data = json.loads(key_questions.read_text(encoding="utf-8"))
                    for q in data.get("questions", []):
                        parts.append(f"- {q}")
                except (json.JSONDecodeError, OSError):
                    pass
            evidence = required / "evidence.json"
            if evidence.exists():
                try:
                    data = json.loads(evidence.read_text(encoding="utf-8"))
                    for e in data.get("evidence", []):
                        parts.append(f"- {e}")
                except (json.JSONDecodeError, OSError):
                    pass
        actions = behavior.get("actions_workflow", {}) or {}
        for action in actions.get("actions", []):
            if action.get("name") == "clarify":
                for inst in action.get("instructions", []):
                    if inst and "story-graph" not in inst.lower() and "story graph" not in inst.lower():
                        parts.append(inst)
                break
        parts.append("")

    def _add_strategy_section(
        self, behavior_dir: Path, behavior: Dict[str, Any], parts: List[str]
    ) -> None:
        parts.append("## Strategy")
        parts.append("")
        parts.append(
            "Review the context and clarification answers. Make decisions using the "
            "criteria below. Compile assumptions and document your decisions. "
            "If you have insufficient context for the strategy, state "
            "[!] NOT ENOUGH INFORMATION - REQUIRES USER INPUT and do not proceed to build. "
            "Save your strategy to strategy.json."
        )
        parts.append("")
        strategy_dir = behavior_dir / "guardrails" / "strategy"
        if strategy_dir.exists():
            assumptions = strategy_dir / "typical_assumptions.json"
            if assumptions.exists():
                try:
                    data = json.loads(assumptions.read_text(encoding="utf-8"))
                    for a in data.get("typical_assumptions", []):
                        parts.append(f"- {a}")
                except (json.JSONDecodeError, OSError):
                    pass
            decision_dir = strategy_dir / "decision_criteria"
            if decision_dir.exists():
                for f in sorted(decision_dir.glob("*.json")):
                    try:
                        data = json.loads(f.read_text(encoding="utf-8"))
                        parts.append(f"- {data.get('question', '')}: {data.get('options', [])}")
                    except (json.JSONDecodeError, OSError):
                        pass
        actions = behavior.get("actions_workflow", {}) or {}
        for action in actions.get("actions", []):
            if action.get("name") == "strategy":
                for inst in action.get("instructions", []):
                    if inst and "story-graph" not in inst.lower() and "story graph" not in inst.lower():
                        parts.append(inst)
                break
        parts.append("")

    def _add_build_section(
        self, behavior_dir: Path, behavior: Dict[str, Any], parts: List[str]
    ) -> None:
        parts.append("## Build")
        parts.append("")
        parts.append(
            "Build the story map using the rules mentioned below and the templates below."
        )
        parts.append("")
        parts.append("### Rules")
        parts.append("")
        self._add_rules_content(behavior_dir, parts)
        self._add_embedded_templates(behavior_dir, parts)

    def _rule_name_from_filename(self, path: Path) -> str:
        """Convert rule filename to readable header, e.g. verb_noun.json -> Verb Noun."""
        name = path.stem.replace("_", " ").replace("-", " ")
        return name.title()

    def _guidance_topic(self, desc: str, max_len: int = 50) -> str:
        """Extract a short topic from guidance description for subheader."""
        if not desc:
            return "Guidance"
        first_line = desc.split("\n")[0].strip()
        if len(first_line) <= max_len:
            return first_line
        return first_line[: max_len - 3].rsplit(" ", 1)[0] + "..."

    def _add_rules_content(self, behavior_dir: Path, parts: List[str]) -> None:
        rules_dir = behavior_dir / "rules"
        if not rules_dir.exists():
            parts.append("DO: Follow behavior instructions.")
            parts.append("")
            return
        rule_files: List[tuple[int, Path]] = []
        for f in rules_dir.glob("*.json"):
            if f.parent.name == "disabled":
                continue
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                rule_files.append((data.get("priority", 99), f))
            except (json.JSONDecodeError, OSError):
                pass
        rule_files.sort(key=lambda x: x[0])
        for idx, (_, f) in enumerate(rule_files, start=1):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                rule_name = self._rule_name_from_filename(f)
                parts.append("---")
                parts.append("")
                parts.append(f"#### Rule {idx}: {rule_name}")
                parts.append("")
                desc = self._filter_story_graph_refs(data.get("description", ""))
                if desc:
                    parts.append(desc)
                    parts.append("")
                do = data.get("do", {})
                if do:
                    do_desc = self._filter_story_graph_refs(do.get("description", ""))
                    if do_desc or do.get("guidance"):
                        parts.append("**DO**")
                        parts.append("")
                        if do_desc:
                            parts.append(do_desc)
                            parts.append("")
                        for g_idx, g in enumerate(do.get("guidance", []), start=1):
                            g_desc = self._filter_story_graph_refs(g.get("description", ""))
                            if g_desc or g.get("example"):
                                topic = self._guidance_topic(g_desc)
                                parts.append(f"*Guidance {g_idx}: {topic}*")
                                parts.append("")
                                if g_desc:
                                    parts.append(g_desc)
                                    parts.append("")
                                for ex in g.get("example", []):
                                    if ex and "story-graph" not in ex.lower() and "story graph" not in ex.lower():
                                        parts.append("```")
                                        parts.append(ex)
                                        parts.append("```")
                                        parts.append("")
                dont = data.get("dont", {})
                if dont:
                    dont_desc = self._filter_story_graph_refs(dont.get("description", ""))
                    if dont_desc or dont.get("guidance"):
                        parts.append("**DON'T**")
                        parts.append("")
                        if dont_desc:
                            parts.append(dont_desc)
                            parts.append("")
                        for g_idx, g in enumerate(dont.get("guidance", []), start=1):
                            g_desc = self._filter_story_graph_refs(g.get("description", ""))
                            if g_desc or g.get("example"):
                                topic = self._guidance_topic(g_desc)
                                parts.append(f"*Guidance {g_idx}: {topic}*")
                                parts.append("")
                                if g_desc:
                                    parts.append(g_desc)
                                    parts.append("")
                                for ex in g.get("example", []):
                                    if ex and "story-graph" not in ex.lower() and "story graph" not in ex.lower():
                                        parts.append("```")
                                        parts.append(ex)
                                        parts.append("```")
                                        parts.append("")
                parts.append("")
            except (json.JSONDecodeError, OSError):
                pass

    def _add_embedded_templates(self, behavior_dir: Path, parts: List[str]) -> None:
        render_dir = behavior_dir / "content" / "render"
        if not render_dir.exists():
            return
        # Collect all (output, template_path) pairs; include all templates even if output duplicates
        template_entries: List[tuple[str, Path]] = []
        seen_paths: set[Path] = set()
        for f in sorted(render_dir.glob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                template = data.get("template", "")
                output = data.get("output", "")
                drawio_file = data.get("drawio_file", "")
                template_path: Path | None = None
                if template:
                    template_path = (render_dir / template).resolve()
                    if not template_path.exists() or not output:
                        template_path = None
                elif drawio_file:
                    template_path = (render_dir / "templates" / drawio_file).resolve()
                    if not template_path.exists():
                        template_path = (render_dir / drawio_file).resolve()
                    if not template_path.exists():
                        template_path = None
                else:
                    template_path = None
                if template_path and output and template_path not in seen_paths:
                    seen_paths.add(template_path)
                    template_entries.append((output, template_path))
            except (json.JSONDecodeError, OSError):
                pass
        if not template_entries:
            return
        parts.append("### Templates")
        parts.append("")
        for output_name, template_path in sorted(template_entries, key=lambda x: (x[0], str(x[1]))):
            try:
                content = template_path.read_text(encoding="utf-8")
                ext = template_path.suffix.lower()
                lang = "drawio" if ext == ".drawio" else ext.lstrip(".")
                label = output_name
                if len([e for e in template_entries if e[0] == output_name]) > 1:
                    label = f"{output_name} ({template_path.name})"
                parts.append(f"#### {label}")
                parts.append("")
                parts.append(f"```{lang}")
                parts.append(content)
                parts.append("```")
                parts.append("")
            except OSError:
                pass

    def _write_rule_file(self, bot_name: str, behavior_name: str, content: str) -> Path | None:
        rules_dir = self.workspace_directory / ".cursor" / "rules"
        rules_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{bot_name}_{behavior_name}.mdc"
        output_path = rules_dir / filename
        output_path.write_text(content, encoding="utf-8")
        return output_path
