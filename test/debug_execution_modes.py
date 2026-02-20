"""Debug: print execution modes for each action, then run shape.clarify + submit.
Run from repo root: python test/debug_execution_modes.py
Uses WORKING_AREA env if set, else tmp_debug_workspace."""
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

# Ensure clarify, strategy, build = combine_next; validate, render NOT set (default manual)
settings_path = workspace / "execution_settings.json"
settings = {}
if settings_path.exists():
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
# Only set combine_next for clarify, strategy, build
for action in ["clarify", "strategy", "build"]:
    settings[f"story_bot.shape.{action}"] = "combine_next"
# Explicitly ensure validate and render are manual (or absent = manual)
for action in ["validate", "render"]:
    settings.pop(f"story_bot.shape.{action}", None)  # remove so default manual
settings_path.write_text(json.dumps(settings, indent=2), encoding="utf-8")
print("execution_settings.json:", json.dumps(settings, indent=2))

from bot.bot import Bot
from cli.cli_session import CLISession

config_path = Path(os.environ["BOT_DIRECTORY"]) / "bot_config.json"
bot = Bot(
    bot_name="story_bot",
    bot_directory=Path(os.environ["BOT_DIRECTORY"]),
    config_path=config_path,
    workspace_path=workspace,
)
session = CLISession(bot=bot, workspace_directory=workspace, mode=None)

# Print execution mode for each shape action
print("\nExecution modes (shape):")
for action_name in ["clarify", "strategy", "build", "validate", "render"]:
    mode = bot.get_execution_mode("shape", action_name)
    print(f"  {action_name}: {mode}")

# 1. Navigate to shape.clarify
session.execute_command("shape.clarify")
print(f"\nAfter shape.clarify: current = {bot.behaviors.current.actions.current_action_name}")

# 2. Submit - capture what gets submitted
response = session.execute_command("submit")
out = response.output
print(f"\nAfter submit: current = {bot.behaviors.current.actions.current_action_name}")

# Check what "Next action" sections appear in submitted instructions
# (We can't easily get the clipboard content, but submit returns status - check response)
has_validate = "validate" in out.lower()
has_render = "render" in out.lower()
print(f"\nSubmit response mentions validate: {has_validate}, render: {has_render}")
print("--- Response output (first 800 chars) ---")
print(out[:800] if len(out) > 800 else out)
print("---")
