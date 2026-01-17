# Generic Bot CLI Launcher (Windows/PowerShell)
#
# This is a reusable launcher that can be called by any bot-specific wrapper.
# It automatically detects the bot directory based on the calling script's location.
#
# Usage from bot-specific wrapper:
#   $AGILE_BOT_ROOT = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
#   & (Join-Path $AGILE_BOT_ROOT "scripts\bot_cli_launcher.ps1") -BotDirectory $PSScriptRoot

param(
    [Parameter(Mandatory=$true)]
    [string]$BotDirectory
)

# Validate bot directory exists
if (-not (Test-Path $BotDirectory)) {
    Write-Error "Bot directory not found: $BotDirectory"
    exit 1
}

# Set BOT_DIRECTORY environment variable
$env:BOT_DIRECTORY = $BotDirectory

# Determine agile_bots root (two levels up from bot directory)
$AGILE_BOT_DIR = Split-Path -Parent (Split-Path -Parent $BotDirectory)

# Call common CLI executor
$CLI_EXECUTE_PATH = Join-Path (Join-Path $AGILE_BOT_DIR "scripts") "cli_execute.ps1"

if (-not (Test-Path $CLI_EXECUTE_PATH)) {
    Write-Error "CLI executor not found: $CLI_EXECUTE_PATH"
    exit 1
}

& $CLI_EXECUTE_PATH
