#!/usr/bin/env python3
"""Run CRC domain validation scanners on story graph."""
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rules.rule_loader import RuleLoader

class SimpleBotPaths:
    def __init__(self, bot_directory):
        self.bot_directory = Path(bot_directory)

def main():
    story_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("C:/dev/agile_bots_demo/vouchers/docs/story/story-graph.json")
    if not story_path.exists():
        print(f"Story graph not found: {story_path}")
        return []

    with open(story_path, encoding="utf-8") as f:
        story_graph = json.load(f)

    bot_path = Path(__file__).parent
    bot_paths = SimpleBotPaths(bot_directory=bot_path / "bots" / "crc_bot")
    loader = RuleLoader(bot_name="crc_bot", behavior_name="domain", bot_paths=bot_paths)
    rules = loader.load_behavior_rules()

    all_violations = []
    for rule in rules:
        if not rule.has_scanner:
            continue
        scanner = rule.scanner
        if scanner is None:
            print(f"{rule.name}: scanner load failed - {rule.scanner_load_error}")
            continue
        # Use scan_with_context (domain scanners accept context with story_graph)
        from scanners.resources.scan_context import ScanFilesContext, FileCollection  # noqa: E402
        context = ScanFilesContext(story_graph=story_graph, files=FileCollection())
        try:
            violations = scanner.scan_with_context(context)
            for v in violations:
                if isinstance(v, dict):
                    v["rule"] = rule.name
                all_violations.append(v)
            print(f"{rule.name}: {len(violations)} violations")
        except Exception as e:
            print(f"{rule.name}: ERROR - {e}")

    # Normalize to dicts
    out = []
    for v in all_violations:
        if isinstance(v, dict):
            out.append(v)
        else:
            out.append(v.to_dict() if hasattr(v, "to_dict") else {"raw": str(v)})
    print("\n--- VIOLATIONS ---")
    print(json.dumps(out, indent=2, default=str))
    return out

if __name__ == "__main__":
    main()
