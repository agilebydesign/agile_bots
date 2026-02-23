#!/usr/bin/env python
"""
Run code behavior validation scanners.

Loads Bot and code behavior, creates ValidationContext with optional scope
for story graph (docs/story/story-graph.json), runs Rules.validate(), and prints
the violation summary.

Usage:
  python scripts/run_code_validation.py [story_filter]
  python scripts/run_code_validation.py "Configure Behavior Execute"
  python scripts/run_code_validation.py "Configure Behavior Execute" --files "src/bot/bot.py,src/cli/*.py"
  python scripts/run_code_validation.py "Configure Behavior Execute" --skiprule eliminate_duplication

When story_filter is provided, story graph is filtered to that story.
Pass --skiprule RULE_NAME to skip slow rules (e.g. eliminate_duplication).
By default, code files are discovered from the story's test file imports.
Pass --files to override with explicit paths (comma-separated, globs supported).
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

STORY_CODE_FILES = {
    "Configure Action Execution": [
        "src/bot/bot.py",
        "src/cli/cli_session.py",
        "src/panel/behaviors_view.js",
        "src/panel/bot_panel.js",
        "src/scope/json_scope.py",
        "src/scope/scope.py",
    ],
    "Configure Behavior Execute": [
        "src/bot/bot.py",
        "src/cli/cli_session.py",
        "src/panel/behaviors_view.js",
        "src/panel/bot_panel.js",
        "src/scope/json_scope.py",
        "src/scope/scope.py",
    ],
    "Add Special Instructions": [
        "src/bot/bot.py",
        "src/bot/json_bot.py",
        "src/cli/cli_session.py",
        "src/instructions/instructions.py",
        "src/panel/behaviors_view.js",
        "test/invoke_bot/navigate_behavior_actions/test_perform_behavior_action_in_bot_workflow.py",
    ],
}


def _expand_file_paths(workspace: Path, paths: list[str]) -> list[str]:
    result = []
    for p in paths:
        path_str = p.replace("\\", "/")
        if "*" in path_str or "?" in path_str:
            matched = list(workspace.glob(path_str))
            result.extend(str(m) for m in matched if m.is_file())
        else:
            full = workspace / path_str
            if full.exists() and full.is_file():
                result.append(str(full))
    return result


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

    behavior = bot.behaviors.find_by_name("code")
    rules = Rules(behavior=behavior, bot_paths=behavior.bot_paths)

    args = sys.argv[1:]
    story_filter = args[0] if args and not args[0].startswith("--") else None
    explicit_files = None
    skiprule = []
    if "--files" in args:
        idx = args.index("--files")
        if idx + 1 < len(args):
            explicit_files = [p.strip() for p in args[idx + 1].split(",")]
    if "--skiprule" in args:
        idx = args.index("--skiprule")
        if idx + 1 < len(args):
            skiprule = [r.strip() for r in args[idx + 1].split(",")]

    if story_filter:
        scope = Scope(workspace_directory, bot.bot_paths)
        if explicit_files:
            file_paths = _expand_file_paths(workspace_directory, explicit_files)
            scope.filter(ScopeType.FILES, file_paths, [], skiprule)
        elif story_filter in STORY_CODE_FILES:
            file_paths = _expand_file_paths(workspace_directory, STORY_CODE_FILES[story_filter])
            scope.filter(ScopeType.FILES, file_paths, [], skiprule)
        else:
            scope.filter(ScopeType.STORY, [story_filter], [], skiprule)
        context = ValidateActionContext(scope=scope)
    else:
        scope = Scope(workspace_directory, bot.bot_paths) if skiprule else None
        if scope:
            scope.filter(ScopeType.ALL, [], [], skiprule)
            context = ValidateActionContext(scope=scope)
        else:
            context = ValidateActionContext(scope=None)

    validation_context = ValidationContext.from_action_context(behavior, context)
    file_count = sum(len(v) for v in validation_context.files.values())
    print(f"Scanning {file_count} file(s)...")

    rules.validate(validation_context)

    summary = rules.violation_summary
    scope_label = f" (scope: {story_filter})" if story_filter else ""
    print(f"=== CODE VALIDATION{scope_label} ===")
    if summary:
        for line in summary:
            print(line)
        print(f"\nTotal: {len(summary)} rule(s) with violations")
    else:
        print("No violations found.")

    for rule in rules:
        if hasattr(rule, "_scanner_load_error") and rule._scanner_load_error:
            print(f"\nScanner load error for {rule.name}: {rule._scanner_load_error}")

    verbose = "--verbose" in sys.argv
    if verbose:
        print("\n=== DETAILED VIOLATIONS ===")
        for rule in rules:
            for v in rule.file_by_file_violations:
                msg = v.get("violation_message", str(v))
                loc = v.get("location", "")
                line = f"\n[{rule.name}] {loc}\n  {msg}"
                try:
                    print(line)
                except UnicodeEncodeError:
                    enc = getattr(sys.stdout, "encoding", "utf-8") or "utf-8"
                    print(line.encode(enc, errors="replace").decode(enc))

    output_path = workspace_root / "docs" / "story" / "violations" / "code-validation-summary.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"=== CODE VALIDATION{scope_label} ===\n\n")
        if summary:
            for line in summary:
                f.write(line + "\n")
            f.write(f"\nTotal: {len(summary)} rule(s) with violations\n")
        else:
            f.write("No violations found.\n")
    print(f"\nSummary saved to: {output_path}")


if __name__ == "__main__":
    main()
