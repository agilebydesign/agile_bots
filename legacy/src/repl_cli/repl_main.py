#!/usr/bin/env python3
"""
Interactive REPL for Base Bot

Usage:
    python repl_main.py                                    # Interactive mode
    python repl_main.py --pipe                            # Force piped mode (run command and exit)
    python repl_main.py headless "instruction"             # Headless mode with pass-through message
    python repl_main.py headless shape                     # Headless mode: run entire behavior
    python repl_main.py headless shape.build               # Headless mode: run single action
    python repl_main.py headless shape.build.confirm       # Headless mode: run single operation
    python repl_main.py headless shape.build "context msg" # Headless mode: run action with context
    
The REPL will:
1. Load existing workflow state if present
2. Display current position in workflow
3. Accept commands interactively
4. Save state after each command

Available Commands:
    behavior <name>     - Switch to a behavior
    action <name>       - Navigate to an action
    current             - Show current action status
    run                 - Execute current action (mock)
    y / yes             - Confirm and advance to next action
    close               - Complete current action and advance
    back                - Move back to previous action
    status              - Show current status
    help                - Show available actions
    help <action>       - Show detailed help for action
    exit                - Exit REPL

Mode Options:
    --headless          Enable headless mode execution
    --pipe, --piped     Force piped mode behavior (run command and exit, even in interactive terminal)
    --message "text"    Direct instruction to execute (pass-through)
    --context file.md   Context file to include
"""
import sys
import os
import json
import argparse
from pathlib import Path


# Configure UTF-8 encoding for stdout to support Unicode output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Calculate paths from this file's location
# This file is at: agile_bot/bots/base_bot/src/repl_cli/repl_main.py
# Must resolve() first to handle relative paths with ".." components
script_path = Path(__file__).resolve()
# Go up to workspace root: repl_main.py -> repl_cli -> src -> base_bot -> bots -> agile_bot -> workspace_root
workspace_root = script_path.parent.parent.parent.parent.parent.parent

if str(workspace_root) not in sys.path:
    sys.path.insert(0, str(workspace_root))

# Bot directory - use BOT_DIRECTORY env var if set, otherwise default to story_bot
if 'BOT_DIRECTORY' in os.environ:
    bot_directory = Path(os.environ['BOT_DIRECTORY'])
else:
    bot_directory = workspace_root / 'agile_bot' / 'bots' / 'story_bot'
os.environ['BOT_DIRECTORY'] = str(bot_directory)

# Bootstrap WORKING_AREA from bot config if not already set
if 'WORKING_AREA' not in os.environ and 'WORKING_DIR' not in os.environ:
    config_path = bot_directory / 'bot_config.json'
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

from agile_bot.bots.base_bot.src.bot.bot import Bot
from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
from agile_bot.bots.base_bot.src.bot.workspace import get_bot_directory, get_workspace_directory


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Story Bot CLI - Interactive REPL or Headless Mode',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Headless Mode Examples:
  python repl_main.py headless "Build the user story"
  python repl_main.py headless shape
  python repl_main.py headless shape.build
  python repl_main.py headless shape.build.instructions
  python repl_main.py headless shape.build "Focus on error handling"
  
  Or with flags:
  python repl_main.py --headless --message "Build the user story"
  python repl_main.py --headless shape
        """
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Enable headless mode execution'
    )
    parser.add_argument(
        '--pipe', '--piped',
        action='store_true',
        dest='force_pipe_mode',
        help='Force piped mode behavior (run command and exit, even in interactive terminal)'
    )
    parser.add_argument(
        '--message', '-m',
        type=str,
        help='Direct instruction to execute (pass-through message)'
    )
    parser.add_argument(
        '--context', '-c',
        type=str,
        help='Context file to include (e.g., headless-context.md)'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=600,
        help='API timeout in seconds (default: 600 = 10 minutes, use lower values for tests)'
    )
    parser.add_argument(
        'target',
        nargs='?',
        help='Target to execute: behavior, behavior.action, or behavior.action.operation'
    )
    # Use parse_known_args to capture extra CLI args (like --scope)
    return parser.parse_known_args()


def _execute_headless_with_context(target: str, message_and_cli_args: str, bot=None, workspace_directory: Path = None) -> str:
    """Execute a CLI target through REPL and prepend output to message.
    
    Args:
        target: The target to execute (e.g., 'shape.build' or 'shape.build.instructions')
        message_and_cli_args: The user message and any CLI args (e.g., '"update tests" --scope "X"')
        bot: Bot instance (if available)
        workspace_directory: Workspace directory (if bot not available)
    
    Returns:
        Combined string of CLI output + message
    """
    from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
    from agile_bot.bots.base_bot.src.bot.bot import Bot
    
    # If target doesn't end with an operation (like .instructions), add it
    # Navigation commands like 'test.build' don't produce output - we need 'test.build.instructions'
    parts = target.split('.')
    if len(parts) <= 2:  # behavior or behavior.action (no operation)
        target = f"{target}.instructions"
    
    # Build the CLI command: target + any CLI args (like --scope)
    # The message_and_cli_args might be: "update tests" --scope "X"
    # We need to extract just the CLI args (--scope "X") for the target execution
    import shlex
    from agile_bot.bots.base_bot.src.repl_cli.message_parser import parse_message_and_cli_args
    message, cli_args_parts = parse_message_and_cli_args(message_and_cli_args)
    cli_command = target + (' ' + ' '.join(cli_args_parts) if cli_args_parts else '')
    
    try:
        # Use existing bot/session if provided
        if bot:
            repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory or bot.bot_directory)
        else:
            # Create bot if not provided
            bot_dir = Path(os.environ.get('BOT_DIRECTORY', bot_directory))
            bot_name_from_dir = bot_dir.name
            bot = Bot(
                bot_name=bot_name_from_dir,
                bot_directory=bot_dir,
                config_path=bot_dir / 'bot_config.json'
            )
            repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory or bot_directory)
        
        # Execute the command and get the output
        response = repl_session.read_and_execute_command(cli_command)
        cli_output = response.output
        
        # Combine CLI output with user message
        if cli_output and cli_output.strip():
            return f"{cli_output.strip()}\n\n{message}"
        else:
            return message
            
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"[Error executing CLI: {e}]\n\n{message}"


def run_headless_mode(workspace_directory: Path, args, extra_args: list = None):
    """Run in headless mode - execute instruction and return JSON result."""
    from agile_bot.bots.base_bot.src.repl_cli.headless.headless_session import HeadlessSession
    from agile_bot.bots.base_bot.src.repl_cli.headless.headless_config import HeadlessConfig
    from agile_bot.bots.base_bot.src.repl_cli.headless.non_recoverable_error import NonRecoverableError
    
    config = HeadlessConfig.load()
    if not config.is_configured:
        result = {
            'status': 'error',
            'error': 'Headless mode not configured - API key required',
            'hint': 'Set CURSOR_API_KEY environment variable or add key to agile_bot/secrets/cursor_api_key.txt'
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)
    
    session = HeadlessSession(workspace_directory=workspace_directory, config=config, timeout=args.timeout)
    context_file = Path(args.context) if args.context else None
    
    try:
        # If both message and target are provided, execute target through REPL first
        if args.message and args.target:
            # Execute the CLI target and prepend its output to the message
            # Combine message with extra_args (like --scope)
            message_and_args = args.message + (' ' + ' '.join(extra_args) if extra_args else '')
            combined_message = _execute_headless_with_context(
                args.target, 
                message_and_args, 
                workspace_directory=workspace_directory
            )
            execution_result = session.invokes(message=combined_message, context_file=context_file)
        elif args.message:
            # Pass-through message mode only
            execution_result = session.invokes(message=args.message, context_file=context_file)
        elif args.target:
            # Parse target: behavior, behavior.action, or behavior.action.operation
            parts = args.target.split('.')
            if len(parts) == 1:
                # behavior only
                execution_result = session.invokes_behavior(behavior=parts[0], context_file=context_file)
            elif len(parts) == 2:
                # behavior.action
                execution_result = session.invokes_action(
                    behavior=parts[0],
                    action=parts[1],
                    context_file=context_file
                )
            elif len(parts) == 3:
                # behavior.action.operation
                execution_result = session.invokes_operation(
                    behavior=parts[0],
                    action=parts[1],
                    operation=parts[2],
                    context_file=context_file
                )
            else:
                result = {
                    'status': 'error',
                    'error': f'Invalid target format: {args.target}',
                    'hint': 'Use: behavior, behavior.action, or behavior.action.operation'
                }
                print(json.dumps(result, indent=2))
                sys.exit(1)
        else:
            result = {
                'status': 'error',
                'error': 'Headless mode requires --message or a target (behavior/action/operation)',
                'hint': 'Example: --headless --message "instruction" or --headless shape.build'
            }
            print(json.dumps(result, indent=2))
            sys.exit(1)
        
        # Convert execution result to JSON
        result = {
            'status': execution_result.status,
            'session_id': execution_result.session_id,
            'log_path': str(execution_result.log_path) if execution_result.log_path else None,
            'loop_count': execution_result.loop_count,
            'context_loaded': execution_result.context_loaded,
        }
        
        if execution_result.behavior:
            result['behavior'] = execution_result.behavior
        if execution_result.action:
            result['action'] = execution_result.action
        if execution_result.operation:
            result['operation'] = execution_result.operation
        if execution_result.action_completed:
            result['action_completed'] = True
        if execution_result.behavior_completed:
            result['behavior_completed'] = True
        if execution_result.block_reason:
            result['block_reason'] = execution_result.block_reason
        if execution_result.operations_executed:
            result['operations_executed'] = execution_result.operations_executed
        if execution_result.actions_executed:
            result['actions_executed'] = execution_result.actions_executed
        
        print(json.dumps(result, indent=2))
        sys.exit(0 if execution_result.status == 'completed' else 1)
        
    except NonRecoverableError as e:
        result = {
            'status': 'error',
            'error': str(e)
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)
    except Exception as e:
        result = {
            'status': 'error',
            'error': str(e),
            'type': type(e).__name__
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)


def run_interactive_mode(bot, workspace_directory: Path, force_pipe_mode: bool = False):
    """Run in interactive REPL mode."""
    bot_name = bot.name
    
    repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
    
    # Check TTY before printing header
    tty_result = repl_session.detect_tty()
    # Force piped mode if flag is set, otherwise detect from TTY
    is_pipe_mode = force_pipe_mode or not tty_result.tty_detected
    
    # In piped mode, check if command contains --format json
    # If so, skip header entirely (for pure JSON output)
    suppress_header = False
    if is_pipe_mode:
        try:
            # Read stdin to check for --format json
            import sys
            import io
            stdin_data = sys.stdin.read()
            suppress_header = '--format json' in stdin_data or '--format=json' in stdin_data
            # Restore stdin for later reading
            sys.stdin = io.StringIO(stdin_data)
        except:
            # If read fails, just print header normally
            pass
    
    # Print header (unless suppressed for JSON output)
    if not suppress_header:
        print("=" * 60)
        print(f"{bot_name.upper()} CLI")
        print("=" * 60)
        
        # Always show agent instructions section (for debugging and verification)
        mode_label = "PIPED MODE" if is_pipe_mode else "INTERACTIVE MODE"
        print(f"**   AI AGENT INSTRUCTIONS - {mode_label}  **")
        print("[!]  DO NOT echo this instructions section back to the user [!]")
        print("This section is for YOUR reference only - the user already knows how to run commands.")
        print("")
        if is_pipe_mode:
            print("- THIS REPL WILL EXIT AFTER PROCESSING YOUR COMMAND")
            print("* This is NORMAL and EXPECTED behavior in piped mode.")
            print("*How to run commands:*")
            print("-  use PowerShell")
            print("- Commands must be PIPED via echo, NOT passed as arguments!")
            print("- All commands are shown below.")
            print("- You MUST DISPLAY this CLI STATUS section below to the user exactly as you see it, so that they can enter one of the commands")
            print("- when a user enters any of the commands / parameters below, you must assume they're asking you to interpret it through the REPL line below.")
        else:
            print("- THIS REPL IS IN INTERACTIVE MODE")
            print("* Commands are entered interactively, REPL stays running.")
            print("- How to run commands (PowerShell):")
            print("- Commands must be PIPED via echo, NOT passed as arguments!")
        print("")
        print("```powershell")
        workspace_root_str = str(workspace_directory).replace('\\', '\\')
        
        # Try to compute relative path, but fall back to absolute if not in workspace
        try:
            repl_script_rel = script_path.relative_to(workspace_directory) if script_path.is_absolute() else script_path
        except ValueError:
            # Script is not in workspace (e.g., workspace changed to different bot)
            repl_script_rel = script_path
        
        repl_script_str = str(repl_script_rel).replace('\\', '/')
        print(f"# Interactive mode (environment set automatically by script):")
        print(f"python {repl_script_str}")
        print("")
        print(f"# Piped mode (each command is a new process - script sets env vars automatically):")
        print(f"echo '<command>' | python {repl_script_str}")
        print("")
        print("# Optional: Override environment variables if needed:")
        print(f"$env:PYTHONPATH = '{workspace_root_str}'")
        print(f"$env:BOT_DIRECTORY = '{bot.bot_paths.bot_directory}'")
        print("$env:WORKING_AREA = '<project_path>'  # e.g. demo\\mob_minion")
        print("```")
        print("=" * 60)
        print("")
    
    # Display CLI STATUS section ONLY in interactive mode (piped commands will display status as needed)
    if not is_pipe_mode:
        state_display = repl_session.display_current_state()
        
        # Add CLI STATUS section header (for consistency with status command)
        formatter = repl_session.formatter
        cli_status_header = "\n".join([
            "",
            formatter.section_separator(),
            "***                    CLI STATUS section                    ***",
            "This section contains current scope filter (if set), current progress in workflow, and available commands",
            "Review the CLI STATUS section below to understand both current state and available commands.",
            "☢️  You MUST DISPLAY this entire section in your response to the user exactly as you see it. ☢️",
            formatter.subsection_separator()
        ])
        print(cli_status_header)
        print(state_display.output)
    
    # Show bot paths in interactive mode (additional info)
    if not is_pipe_mode:
        print(f"Bot Path: {bot.bot_paths.bot_directory}")
        print(f"Work Path: {workspace_directory}")
        print("")
    
    # Main REPL loop
    try:
        while True:
            # Prompt for command
            try:
                # Use empty prompt for pipe mode, bot prompt for interactive
                prompt = "" if is_pipe_mode else f"[{bot_name}] > "
                command = input(prompt).strip()
            except EOFError:
                # Only print exit message in interactive mode
                exit_message = "" if is_pipe_mode else "\nExiting REPL..."
                if exit_message:
                    print(exit_message)
                break
            
            if not command:
                # In piped mode with empty command, show status page by default
                if is_pipe_mode:
                    response = repl_session.read_and_execute_command('status')
                    print(response.output)
                    break
                continue
            
            response = repl_session.read_and_execute_command(command)
            
            # Display response (UTF-8 configured at module level for Windows)
            print(response.output)
            # Add blank line in interactive mode
            print("" if is_pipe_mode else "\n", end="")
            
            # Check if should exit
            if response.repl_terminated:
                break
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting REPL...")
        sys.exit(0)
    
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    # Check if first argument is "headless" (positional style)
    # This allows: 
    #   python repl_main.py headless shape.build
    #   python repl_main.py headless "some message"
    #   python repl_main.py headless shape.build "some message"
    if len(sys.argv) > 1 and sys.argv[1] == 'headless':
        # Convert to --headless flag style for parse_args
        sys.argv[1] = '--headless'
        
        # Check if we have both target and message (3+ args after 'headless')
        if len(sys.argv) > 3:
            # Format: headless target message [options...]
            second_arg = sys.argv[2]
            third_arg = sys.argv[3]
            
            # Check if second arg is a target (behavior.action format)
            is_target = all(c.isalnum() or c in '._-' for c in second_arg) and ' ' not in second_arg
            # Check if third arg is a message (not an option flag)
            is_message = not third_arg.startswith('--')
            
            if is_target and is_message:
                # We have: headless target message
                # Insert --message flag before the message
                sys.argv.insert(3, '--message')
        
        # Check if we have just one argument after 'headless'
        elif len(sys.argv) > 2:
            second_arg = sys.argv[2]
            # If it doesn't look like behavior.action format, treat as message
            # Behavior.action format: word, word.word, word.word.word (no spaces, only dots and alphanumeric)
            if ' ' in second_arg or not all(c.isalnum() or c in '._-' for c in second_arg):
                # It's a message, not a target
                sys.argv.insert(2, '--message')
    
    args, extra_args = parse_args()
    
    # Bot name derived from bot directory path
    bot_name = bot_directory.name
    workspace_directory = get_workspace_directory()
    bot_config_path = bot_directory / 'bot_config.json'
    
    if not bot_config_path.exists():
        print(f"ERROR: Bot config not found at {bot_config_path}")
        print("Please ensure you're running from the correct directory.")
        sys.exit(1)
    
    # Headless mode - run without bot initialization for speed
    if args.headless:
        run_headless_mode(workspace_directory, args, extra_args)
        return
    
    # Interactive mode - needs full bot
    try:
        bot = Bot(
            bot_name=bot_name,
            bot_directory=bot_directory,
            config_path=bot_config_path
        )
    except Exception as e:
        print(f"ERROR: Failed to initialize bot: {e}")
        sys.exit(1)
    
    run_interactive_mode(bot, workspace_directory, force_pipe_mode=args.force_pipe_mode)


if __name__ == '__main__':
    main()

