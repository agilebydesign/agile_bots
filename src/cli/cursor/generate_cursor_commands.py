#!/usr/bin/env python3
"""Generate cursor commands for story_bot and crc_bot"""

import sys
from pathlib import Path

# Add src to path
workspace_root = Path(__file__).parent
src_path = workspace_root / 'src'
sys.path.insert(0, str(src_path))

from bot.bot import Bot
from cli.cursor.cursor_command_visitor import CursorCommandGenerator

def generate_commands_for_bot(bot_name: str):
    """Generate cursor commands for a specific bot"""
    print(f"\n{'='*60}")
    print(f"Generating cursor commands for: {bot_name}")
    print(f"{'='*60}")
    
    # Find bot directory
    bot_dir = workspace_root / 'bots' / bot_name
    if not bot_dir.exists():
        print(f"ERROR: Bot directory not found: {bot_dir}")
        return False
    
    # Check for bot_config.json
    bot_config_path = bot_dir / 'bot_config.json'
    if not bot_config_path.exists():
        print(f"ERROR: bot_config.json not found at: {bot_config_path}")
        return False
    
    try:
        # Set BOT_DIRECTORY environment variable (required for base_actions lookup)
        import os
        os.environ['BOT_DIRECTORY'] = str(bot_dir)
        
        # Create bot instance
        print(f"Loading bot from: {bot_dir}")
        bot = Bot(
            bot_name=bot_name,
            bot_directory=bot_dir,
            config_path=bot_config_path,
            workspace_path=workspace_root
        )
        
        # Create cursor command generator
        print(f"Creating command generator...")
        generator = CursorCommandGenerator(
            workspace_root=workspace_root,
            bot_location=bot_dir,
            bot=bot,
            bot_name=bot_name
        )
        
        # Generate commands
        print(f"Generating commands...")
        commands = generator.generate()
        
        # Report results
        print(f"\n[OK] Generated {len(commands)} cursor commands:")
        for cmd_name, cmd_path in commands.items():
            print(f"  - {cmd_name}: {cmd_path.relative_to(workspace_root)}")
        
        print(f"\n[OK] Commands written to: .cursor/commands/")
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to generate commands for {bot_name}")
        print(f"  {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Generate cursor commands for all bots"""
    print("\n" + "="*60)
    print("Cursor Command Generator")
    print("="*60)
    
    bots = ['story_bot', 'crc_bot']
    results = {}
    
    for bot_name in bots:
        success = generate_commands_for_bot(bot_name)
        results[bot_name] = success
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for bot_name, success in results.items():
        status = "[SUCCESS]" if success else "[FAILED]"
        print(f"{status}: {bot_name}")
    
    all_success = all(results.values())
    print("\n" + ("="*60))
    if all_success:
        print("[OK] All cursor commands generated successfully!")
    else:
        print("[ERROR] Some commands failed to generate")
        sys.exit(1)

if __name__ == '__main__':
    main()
