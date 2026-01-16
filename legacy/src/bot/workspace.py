from pathlib import Path
import os

def get_python_workspace_root() -> Path:
    return Path(__file__).parent.parent.parent.parent.parent.parent

def get_bot_directory() -> Path:
    bot_dir = os.environ.get('BOT_DIRECTORY')
    if not bot_dir:
        raise RuntimeError('BOT_DIRECTORY environment variable is not set. Entry points must bootstrap this before importing other modules.')
    return Path(bot_dir.strip())

def get_workspace_directory() -> Path:
    workspace = os.environ.get('WORKING_AREA') or os.environ.get('WORKING_DIR')
    if not workspace:
        raise RuntimeError('WORKING_AREA environment variable is not set. Entry points must bootstrap this before importing other modules.')
    return Path(workspace.strip())

def get_base_actions_directory(bot_directory: Path=None) -> Path:
    # Calculate relative to this file's location
    # workspace.py is at: base_bot/src/bot/workspace.py
    # Go up: bot -> src -> base_bot -> base_actions
    base_bot_dir = Path(__file__).parent.parent.parent
    return base_bot_dir / 'base_actions'

def get_behavior_folder(bot_name: str, behavior: str) -> Path:
    bot_directory = get_bot_directory()
    return bot_directory / 'behaviors' / behavior