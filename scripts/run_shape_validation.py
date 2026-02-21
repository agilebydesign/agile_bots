#!/usr/bin/env python
"""
Run shape behavior validation scanners programmatically.

Loads Bot and shape behavior, creates ValidationContext with scope for story graph
(docs/story/story-graph.json), runs Rules.validate(), and prints the violation summary.
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

    behavior = bot.behaviors.find_by_name("shape")
    rules = Rules(behavior=behavior, bot_paths=behavior.bot_paths)

    # Scope for full story graph (docs/story/story-graph.json)
    # scope=None means validate entire story graph
    context = ValidateActionContext(scope=None)
    validation_context = ValidationContext.from_action_context(behavior, context)

    # Run validation
    rules.validate(validation_context)

    # Print violation summary
    summary = rules.violation_summary
    if summary:
        print("=== VIOLATION SUMMARY ===")
        for line in summary:
            print(line)
        print(f"\nTotal: {len(summary)} rule(s) with violations")
    else:
        print("No violations found.")

    # Optionally save to file
    output_path = workspace_root / "docs" / "story" / "violations" / "shape-validation-summary.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=== SHAPE BEHAVIOR VALIDATION SUMMARY ===\n\n")
        if summary:
            for line in summary:
                f.write(line + "\n")
            f.write(f"\nTotal: {len(summary)} rule(s) with violations\n")
        else:
            f.write("No violations found.\n")
    print(f"\nSummary saved to: {output_path}")


if __name__ == "__main__":
    main()
