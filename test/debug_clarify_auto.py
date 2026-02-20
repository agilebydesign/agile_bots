"""One-off debug: run shape.clarify with clarify set to auto and print instructions. Run from repo root: python test/debug_clarify_auto.py"""
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

# Persist execution_settings.json: clarify and strategy auto so we get clarify -> strategy -> build
settings_path = workspace / "execution_settings.json"
settings_path.write_text(
    json.dumps({
        "story_bot.shape.clarify": "auto",
        "story_bot.shape.strategy": "auto",
        "story_bot.shape.build": "auto",
    }, indent=2),
    encoding="utf-8",
)
print("Wrote", settings_path, "-> shape.clarify=auto, shape.strategy=auto, shape.build=auto")

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

# Run shape.clarify (should return clarify + strategy + build when clarify and strategy are auto)
response = session.execute_command("shape.clarify")
out = response.output
# Check chain: Next action: strategy, Next action: build
has_strategy = "## Next action: strategy" in out or "Next action: strategy" in out
has_build = "## Next action: build" in out or "Next action: build" in out
print("--- OUTPUT (first 5000 chars, ASCII-safe) ---")
print(out[:5000].encode("ascii", errors="replace").decode() if len(out) > 5000 else out.encode("ascii", errors="replace").decode())
if len(out) > 5000:
    print("...")
print("--- END (total", len(out), "chars) ---")
if has_strategy and has_build:
    print("[OK] Chain clarify -> strategy -> build present")
elif has_strategy:
    print("[PARTIAL] strategy present, build MISSING")
else:
    print("[MISSING] strategy and/or build not found in output")
