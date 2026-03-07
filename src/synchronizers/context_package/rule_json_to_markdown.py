"""
Rule JSON to Markdown Adapter

Converts rules/*.json (DO/DON'T structure) to rules/*.md for skill output.
"""
import json
from pathlib import Path
from typing import Dict, Any


class RuleJsonToMarkdownAdapter:
    """Converts a single rule JSON to markdown."""

    def convert(self, rule_json: Dict[str, Any], rule_name: str | None = None) -> str:
        """Convert rule JSON to markdown string.

        Args:
            rule_json: Parsed rule JSON (description, do, dont, priority)
            rule_name: Optional display name (e.g. from filename)

        Returns:
            Markdown string with DO/DO NOT sections
        """
        parts: list[str] = []

        title = rule_name or self._title_from_json(rule_json)
        parts.append("---")
        parts.append(f"title: {title}")
        priority = rule_json.get("priority", 99)
        parts.append(f"priority: {priority}")
        parts.append("---")
        parts.append("")
        parts.append(f"## {title}")
        parts.append("")

        desc = rule_json.get("description", "")
        if desc:
            parts.append(self._filter_story_graph_refs(desc))
            parts.append("")

        do = rule_json.get("do", {})
        if do:
            parts.append("**DO**")
            parts.append("")
            do_desc = self._filter_story_graph_refs(do.get("description", ""))
            if do_desc:
                parts.append(do_desc)
                parts.append("")
            for g in do.get("guidance", []):
                g_desc = self._filter_story_graph_refs(g.get("description", ""))
                if g_desc:
                    parts.append(g_desc)
                    parts.append("")
                for ex in g.get("example", []):
                    if ex and "story-graph" not in ex.lower() and "story graph" not in ex.lower():
                        parts.append("```")
                        parts.append(ex)
                        parts.append("```")
                        parts.append("")

        dont = rule_json.get("dont", {})
        if dont:
            parts.append("**DO NOT**")
            parts.append("")
            dont_desc = self._filter_story_graph_refs(dont.get("description", ""))
            if dont_desc:
                parts.append(dont_desc)
                parts.append("")
            for g in dont.get("guidance", []):
                g_desc = self._filter_story_graph_refs(g.get("description", ""))
                if g_desc:
                    parts.append(g_desc)
                    parts.append("")
                for ex in g.get("example", []):
                    if ex and "story-graph" not in ex.lower() and "story graph" not in ex.lower():
                        parts.append("```")
                        parts.append(ex)
                        parts.append("```")
                        parts.append("")

        return "\n".join(parts).rstrip()

    def _title_from_json(self, rule_json: Dict[str, Any]) -> str:
        """Extract title from description first line or default."""
        desc = rule_json.get("description", "")
        if desc:
            first = desc.split("\n")[0].strip()
            if len(first) <= 60:
                return first
            return first[:57] + "..."
        return "Rule"

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
        return "\n".join(filtered) if filtered else ""

    def convert_file(self, json_path: Path) -> str:
        """Load rule JSON from file and convert to markdown."""
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return ""
        name = json_path.stem.replace("_", "-").replace(" ", "-")
        return self.convert(data, rule_name=name)
