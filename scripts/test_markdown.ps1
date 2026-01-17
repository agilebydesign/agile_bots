#!/usr/bin/env pwsh

$AGILE_BOT_DIR = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = $AGILE_BOT_DIR
$env:BOT_DIRECTORY = "$AGILE_BOT_DIR\bots\story_bot"

# Pipe status command to CLI for markdown output
echo 'status' | python "$AGILE_BOT_DIR\src\cli\cli_main.py"
