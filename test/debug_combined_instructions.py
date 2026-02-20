"""Debug: build combined instructions (like submit does) and print which actions are included.
Run from repo root: python test/debug_combined_instructions.py"""
import json
import os
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
src = repo_root / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

os.environ.setdefault("BOT_DIRECTORY", str(repo_root / "bots" / "story_bot"))
workspace = Path(os.environ.get("WORKING_AREA", str(repo_root / "tmp_debug_workspace")))
workspace.mkdir(parents=True, exist_ok=True)
os.environ["WORKING_AREA"] = str(workspace)

# clarify, strategy, build = combine_next; validate, render = manual (not in file)
settings_path = workspace / "execution_settings.json"
settings = {f"story_bot.shape.{a}": "combine_next" for a in ["clarify", "strategy", "build"]}
settings_path.write_text(json.dumps(settings, indent=2), encoding="utf-8")

from instructions.instructions import Instructions
from bot.bot import Bot

config_path = Path(os.environ["BOT_DIRECTORY"]) / "bot_config.json"
bot = Bot(
    bot_name="story_bot",
    bot_directory=Path(os.environ["BOT_DIRECTORY"]),
    config_path=config_path,
    workspace_path=workspace,
)

# Print execution modes
print("Execution modes:")
for a in ["clarify", "strategy", "build", "validate", "render"]:
    print(f"  {a}: {bot.get_execution_mode('shape', a)}")

# Replicate submit_current_action combine logic
bot.behaviors.navigate_to("shape")
bot.behaviors.current.actions.navigate_to("clarify")
behavior = bot.behaviors.current
action = behavior.actions.current
instructions = action.get_instructions(include_scope=True)
last_appended = bot._append_next_action_instructions_if_combine_next(
    behavior, "shape", "clarify", action, instructions, context=None, include_scope=True
)

# Count "## Next action: X" and check combining text, deduplication
content = "\n".join(instructions.display_content) if hasattr(instructions, "display_content") else str(instructions)
next_actions = []
import re
for m in re.finditer(r"## Next action: (\w+)", content):
    next_actions.append(m.group(1))

print(f"\nlast_appended from combine: {last_appended}")
print(f"'## Next action:' sections: {next_actions}")

has_combining = "**Combined instructions:**" in content
has_next_text = "**Next:** Perform the following action" in content
behavior_count = content.count("## Behavior Instructions - shape")
print(f"\nCombining text at top: {has_combining}")
print(f"'Next' text between actions: {has_next_text}")
print(f"Behavior Instructions count (expect 1): {behavior_count}")

if has_combining and has_next_text and behavior_count == 1:
    print("\n[OK] Combined instructions: deduplication and combining text present")
else:
    print("\n[CHECK] Verify combining text and deduplication")
