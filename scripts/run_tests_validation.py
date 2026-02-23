#!/usr/bin/env python
"""
Run tests behavior validation scanners.

Loads Bot and tests behavior, creates ValidationContext with optional scope
for story graph (docs/story/story-graph.json), runs Rules.validate(), and prints
the violation summary.
"""
import sys
from pathlib import Path

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

    behavior = bot.behaviors.find_by_name("tests")
    rules = Rules(behavior=behavior, bot_paths=behavior.bot_paths)

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    story_filter = args[0] if args else None
    use_files = "--files" in sys.argv
    files_arg_idx = sys.argv.index("--files") if "--files" in sys.argv else -1
    explicit_files = sys.argv[files_arg_idx + 1].split(",") if files_arg_idx >= 0 and files_arg_idx + 1 < len(sys.argv) else None

    if explicit_files and use_files:
        scope = Scope(workspace_directory, bot.bot_paths)
        scope.filter(ScopeType.FILES, [p.strip() for p in explicit_files])
        context = ValidateActionContext(scope=scope)
    elif story_filter:
        scope = Scope(workspace_directory, bot.bot_paths)
        scope.filter(ScopeType.STORY, [story_filter])
        context = ValidateActionContext(scope=scope)
    else:
        context = ValidateActionContext(scope=None)

    validation_context = ValidationContext.from_action_context(behavior, context)

    file_count = sum(len(v) for v in validation_context.files.values())
    print(f"Scanning {file_count} test file(s)...")

    rules.validate(validation_context)

    summary = rules.violation_summary
    scope_label = f" (scope: {story_filter})" if story_filter else ""
    print(f"=== TESTS VALIDATION{scope_label} ===")
    if summary:
        for line in summary:
            print(line)
        print(f"\nTotal: {len(summary)} rule(s) with violations")
    else:
        print("No violations found.")

    for rule in rules:
        if hasattr(rule, "_scanner_load_error") and rule._scanner_load_error:
            print(f"\nScanner load error for {rule.name}: {rule._scanner_load_error}")

    if "--verbose" in sys.argv:
        print("\n=== DETAILED VIOLATIONS ===")
        for rule in rules:
            for v in rule.file_by_file_violations:
                msg = v.get("violation_message", str(v))
                loc = v.get("location", "")
                print(f"\n[{rule.name}] {loc}\n  {msg}")

    output_path = workspace_root / "docs" / "story" / "violations" / "tests-validation-summary.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"=== TESTS VALIDATION{scope_label} ===\n\n")
        if summary:
            for line in summary:
                f.write(line + "\n")
            f.write(f"\nTotal: {len(summary)} rule(s) with violations\n")
        else:
            f.write("No violations found.\n")
    print(f"\nSummary saved to: {output_path}")


if __name__ == "__main__":
    main()
