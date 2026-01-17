# Agile Bot CLI Launcher (Windows/PowerShell)
#
# Usage (for humans):
#   .\cli_execute.ps1
#
# This launches the interactive CLI session
# Bot behaviors are loaded from configured bot directory
# Working directory defaults to workspace root
#
# AI AGENTS:
#   Commands must be PIPED via echo, NOT passed as arguments!
#   PowerShell uses semicolons (;) to chain commands, NOT && (that's bash/cmd)
#   
#   WHAT DOES NOT WORK:
#     [X] python cli_main.py instructions
#     [X] python cli_main.py --command instructions
#   
#   WHAT WORKS:
#     [OK] echo 'instructions' | python cli_main.py
#   
#   Step 1: Set environment and pipe command:
#     cd C:\dev\agile_bots
#     $env:PYTHONPATH = "C:\dev\agile_bots\src"
#     $env:BOT_DIRECTORY = "C:\dev\agile_bots\bots\story_bot"
#     $env:WORKING_AREA = "<project_path>"  # e.g. demo\mob_minion
#     echo "status" | python src/cli/cli_main.py
#   
#   Step 2: Read output, do work (create files, etc.)
#   Step 3: Pipe next command: echo "next" | python cli_main.py
#   Step 4: Repeat for each step in workflow
#   
#   CLI exits after each command - this is NORMAL in piped mode

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$AGILE_BOT_DIR = Split-Path -Parent $SCRIPT_DIR

# Set environment variables - PYTHONPATH must point to src for scanner imports
$env:PYTHONPATH = Join-Path $AGILE_BOT_DIR "src"

# BOT_DIRECTORY should be set by the calling script (bot-specific wrapper)
# If not set, default to story_bot for backward compatibility
if (-not $env:BOT_DIRECTORY) {
    $env:BOT_DIRECTORY = Join-Path (Join-Path $AGILE_BOT_DIR "bots") "story_bot"
}

# Set WORKING_AREA if not already set
if (-not $env:WORKING_AREA) {
    $env:WORKING_AREA = $AGILE_BOT_DIR
}

# Launch CLI using relative path
$CLI_PATH = Join-Path (Join-Path (Join-Path $AGILE_BOT_DIR "src") "cli") "cli_main.py"
python $CLI_PATH
