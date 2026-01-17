# Story Bot CLI Launcher (Windows/PowerShell)
#
# Usage (for humans):
#   .\story_cli.ps1
#
# This launches the interactive CLI session for story_bot
# Bot behaviors are loaded from story_bot directory
# Working directory defaults to workspace root

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$AGILE_BOT_DIR = Split-Path -Parent (Split-Path -Parent $SCRIPT_DIR)
$WORKSPACE_ROOT = Split-Path -Parent $AGILE_BOT_DIR

# Set BOT_DIRECTORY for story_bot before calling common script
$env:BOT_DIRECTORY = $SCRIPT_DIR

# Call common CLI executor
$CLI_EXECUTE_PATH = Join-Path (Join-Path $AGILE_BOT_DIR "scripts") "cli_execute.ps1"
& $CLI_EXECUTE_PATH
