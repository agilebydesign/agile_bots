#!/usr/bin/env python
"""
Run scenarios behavior validation scanners.

Loads Bot and scenarios behavior, creates ValidationContext with optional scope
for story graph (docs/story/story-graph.json), runs Rules.validate(), and prints
the violation summary.
"""
import sys
from pathlib import Path

# Add src to path
script_dir = Path(__file__).resolve().parent
workspace_root = script_dir.parent
src_root = workspace_root / "src"
if str(src_root) not in sys.path:
    sys.path.insert(0, str(src_root))
if str(workspace_root) not in sys.path:
    sys.path.insert(0, str(workspace_root))

from bot.bot import Bot
from actions.action_context import ValidateActionContext
from scope.scope import Scope, ScopeType
from rules.rules import Rules, ValidationContext


def main():
    bot_directory = workspace_root / "bots" / "story_bot"
    workspace_directory = workspace_root
    config_path = bot_directory / "bot_config.json"

    bot = Bot(
        bot_name="story_bot",
        bot_directory=bot_directory,
        config_path=config_path,
        workspace_path=workspace_directory,
    )

    behavior = bot.behaviors.find_by_name("scenarios")
    rules = Rules(behavior=behavior, bot_paths=behavior.bot_paths)

    # Optional: scope to specific story (e.g. "Configure Action Execution")
    # scope=None means validate entire story graph
    story_filter = sys.argv[1] if len(sys.argv) > 1 else None

    if story_filter:
        scope = Scope(workspace_directory, bot.bot_paths)
        scope.filter(ScopeType.STORY, [story_filter])
        context = ValidateActionContext(scope=scope)
    else:
        context = ValidateActionContext(scope=None)

    validation_context = ValidationContext.from_action_context(behavior, context)

    # Run validation
    rules.validate(validation_context)

    # Print violation summary
    summary = rules.violation_summary
    scope_label = f" (scope: {story_filter})" if story_filter else ""
    print(f"=== SCENARIOS VALIDATION{scope_label} ===")
    if summary:
        for line in summary:
            print(line)
        print(f"\nTotal: {len(summary)} rule(s) with violations")
    else:
        print("No violations found.")

    # Report scanner load errors
    for rule in rules:
        if hasattr(rule, "_scanner_load_error") and rule._scanner_load_error:
            print(f"\nScanner load error for {rule.name}: {rule._scanner_load_error}")

    # Report detailed violations when --verbose
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print("\n=== DETAILED VIOLATIONS ===")
        for rule in rules:
            for v in rule.file_by_file_violations:
                msg = v.get("violation_message", str(v))
                loc = v.get("location", "")
                print(f"\n[{rule.name}] {loc}\n  {msg}")

    # Save to file
    output_path = workspace_root / "docs" / "story" / "violations" / "scenarios-validation-summary.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"=== SCENARIOS VALIDATION{scope_label} ===\n\n")
        if summary:
            for line in summary:
                f.write(line + "\n")
            f.write(f"\nTotal: {len(summary)} rule(s) with violations\n")
        else:
            f.write("No violations found.\n")
    print(f"\nSummary saved to: {output_path}")


if __name__ == "__main__":
    main()
