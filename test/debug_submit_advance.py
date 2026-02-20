"""Test: submit combines and advances to validate. Run from repo root: python test/debug_submit_advance.py"""
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

os.environ["BOT_DIRECTORY"] = str(repo_root / "bots" / "story_bot")
workspace = repo_root / "tmp_debug_workspace"
workspace.mkdir(parents=True, exist_ok=True)
os.environ["WORKING_AREA"] = str(workspace)

# clarify, strategy, build = combine_next so submit combines them and advances to validate
settings_path = workspace / "execution_settings.json"
settings_path.write_text(
    json.dumps({
        "story_bot.shape.clarify": "combine_next",
        "story_bot.shape.strategy": "combine_next",
        "story_bot.shape.build": "combine_next",
    }, indent=2),
    encoding="utf-8",
)
print("Wrote execution_settings: clarify, strategy, build = combine_next")

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

# 1. Navigate to shape.clarify (should NOT combine - just clarify)
session.execute_command("shape.clarify")
before = bot.behaviors.current.actions.current_action_name
print(f"After shape.clarify: current action = {before}")

# 2. Submit (should combine clarify+strategy+build and advance to validate)
response = session.execute_command("submit")
after = bot.behaviors.current.actions.current_action_name
print(f"After submit: current action = {after}")

if after == "validate":
    print("[OK] Submit advanced to validate as expected")
else:
    print(f"[FAIL] Expected current=validate, got {after}")
