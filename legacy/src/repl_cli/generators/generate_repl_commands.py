#!/usr/bin/env python3
"""
Generate REPL Cursor Command Files for a bot

Usage:
    python generate_repl_commands.py <bot_name>
    
Example:
    python generate_repl_commands.py story_bot
"""
from pathlib import Path
import sys

# Add workspace root to path
# Script is at: agile_bot/bots/base_bot/src/repl_cli/generators/generate_repl_commands.py
# Workspace root is: repl_cli -> src -> base_bot -> bots -> agile_bot -> workspace_root
script_dir = Path(__file__).parent.resolve()
workspace_root = script_dir.parent.parent.parent.parent.parent.parent
if str(workspace_root) not in sys.path:
    sys.path.insert(0, str(workspace_root))

import os
import json

# Bootstrap WORKING_AREA from bot config if not already set
if 'WORKING_AREA' not in os.environ and 'WORKING_DIR' not in os.environ:
    bot_location = Path(f'agile_bot/bots/story_bot')  # Default to story_bot for bootstrap
    config_path = workspace_root / bot_location / 'bot_config.json'
    if config_path.exists():
        try:
            bot_config = json.loads(config_path.read_text(encoding='utf-8'))
            if 'mcp' in bot_config and 'env' in bot_config['mcp']:
                mcp_env = bot_config['mcp']['env']
                if 'WORKING_AREA' in mcp_env:
                    os.environ['WORKING_AREA'] = mcp_env['WORKING_AREA']
            elif 'WORKING_AREA' in bot_config:
                os.environ['WORKING_AREA'] = bot_config['WORKING_AREA']
        except:
            pass
    
    # If still not set, default to workspace root
    if 'WORKING_AREA' not in os.environ:
        os.environ['WORKING_AREA'] = str(workspace_root)

from agile_bot.bots.base_bot.src.repl_cli.generators.repl_cursor_command_generator import REPLCursorCommandGenerator
from agile_bot.bots.base_bot.src.bot.bot import Bot

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_repl_commands.py <bot_name>")
        print("Example: python generate_repl_commands.py story_bot")
        sys.exit(1)
    
    bot_name = sys.argv[1]
    bot_location = Path(f'agile_bot/bots/{bot_name}')
    bot_directory = workspace_root / bot_location
    
    if not bot_directory.exists():
        print(f"Error: Bot directory not found: {bot_directory}")
        sys.exit(1)
    
    print("=" * 70)
    print(f"Generating REPL Cursor Commands for {bot_name}")
    print("=" * 70)
    print(f"Workspace root: {workspace_root}")
    print(f"Bot directory: {bot_directory}")
    print()
    
    try:
        bot = Bot(
            bot_name=bot_name,
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        
        repl_script_path = workspace_root / 'agile_bot/bots/base_bot/src/repl_cli/repl_main.py'
        
        generator = REPLCursorCommandGenerator(
            workspace_root=workspace_root,
            bot_location=bot_location,
            bot_name=bot_name
        )
        
        commands = generator.generate_repl_cursor_commands(repl_script_path, bot)
        registry_path = generator.update_bot_registry(repl_script_path)
        script_name = 'story_cli.ps1' if bot_name == 'story_bot' else f'{bot_name}_cli.ps1'
        powershell_script = workspace_root / 'agile_bot' / script_name
        
        print(f"[OK] Generated {len(commands)} REPL command files")
        print(f"[OK] Created PowerShell script: {powershell_script.relative_to(workspace_root)}")
        print(f"[OK] Updated registry: {registry_path}")
        print()
        print("Generated command files:")
        for cmd_name, cmd_path in sorted(commands.items()):
            print(f"  - {cmd_name}: {cmd_path.relative_to(workspace_root)}")
        
    except Exception as e:
        print(f"[ERROR] Failed to generate REPL commands: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
