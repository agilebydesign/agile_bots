from pathlib import Path
from typing import Dict, Optional
from ...bot.bot import Bot
from ...generator.orchestrator import Orchestrator
from .repl_cursor_command_visitor import REPLCursorCommandVisitor
import json
from ...utils import read_json_file

class REPLCursorCommandGenerator:
    
    def __init__(self, workspace_root: Path, bot_location: Path, bot_name: str):
        self.workspace_root = workspace_root
        self.bot_location = bot_location
        self.bot_name = bot_name
        self._bot: Optional[Bot] = None
    
    def _get_bot(self) -> Bot:
        if self._bot is None:
            bot_directory = self.workspace_root / self.bot_location
            config_path = bot_directory / 'bot_config.json'
            self._bot = Bot(bot_name=self.bot_name, bot_directory=bot_directory, config_path=config_path)
        return self._bot

    def generate_repl_cursor_commands(self, repl_script_path: Path, bot: Bot) -> Dict[str, Path]:
        visitor = REPLCursorCommandVisitor(
            workspace_root=self.workspace_root,
            repl_script_path=repl_script_path,
            bot=bot
        )
        orchestrator = Orchestrator(visitor)
        orchestrator.generate()
        
        commands = visitor.get_commands()
        
        self._create_powershell_script(repl_script_path)
        
        return commands

    def update_bot_registry(self, repl_script_path: Path) -> Path:
        registry_path = self._get_registry_path()
        registry = self._load_registry(registry_path)
        rel_repl_path = self._get_relative_repl_path(repl_script_path)
        
        if self.bot_name not in registry:
            registry[self.bot_name] = {}
        
        registry[self.bot_name]['repl_path'] = rel_repl_path
        
        if 'trigger_patterns' not in registry[self.bot_name]:
            registry[self.bot_name]['trigger_patterns'] = self._load_bot_trigger_patterns()
        
        if 'cli_path' not in registry[self.bot_name]:
            registry[self.bot_name]['cli_path'] = self._get_default_cli_path()
        
        registry_path.write_text(json.dumps(registry, indent=2, sort_keys=True), encoding='utf-8')
        return registry_path

    def _get_registry_path(self) -> Path:
        registry_path = self.workspace_root / 'agile_bot' / 'bots' / 'registry.json'
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        return registry_path

    def _load_registry(self, registry_path: Path) -> dict:
        if registry_path.exists():
            try:
                return read_json_file(registry_path)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}

    def _get_relative_repl_path(self, repl_script_path: Path) -> str:
        if repl_script_path.is_absolute():
            return str(repl_script_path.relative_to(self.workspace_root)).replace('\\', '/')
        return str(repl_script_path).replace('\\', '/')

    def _get_default_cli_path(self) -> str:
        return str(self.bot_location / 'src' / f'{self.bot_name}_cli.py').replace('\\', '/')

    def _load_bot_trigger_patterns(self) -> list:
        trigger_file = self.workspace_root / self.bot_location / 'trigger_words.json'
        try:
            trigger_data = read_json_file(trigger_file)
            return trigger_data.get('patterns', [])
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _create_powershell_script(self, repl_script_path: Path) -> Path:
        script_name = 'story_cli.ps1' if self.bot_name == 'story_bot' else f'{self.bot_name}_cli.ps1'
        script_file = self.workspace_root / 'agile_bot' / script_name
        rel_repl_path = self._get_relative_repl_path(repl_script_path)
        
        script_content = f"""# {self.bot_name.replace('_', ' ').title()} REPL CLI Launcher (Windows/PowerShell)
#
# Usage (for humans):
#   .\\{self.bot_name}_cli.ps1
#
# This launches the interactive REPL session for {self.bot_name}
# Bot behaviors are loaded from {self.bot_location.name} directory
# Working directory defaults to workspace root
#
# AI AGENTS:
#   Commands must be PIPED via echo, NOT passed as arguments!
#   PowerShell uses semicolons (;) to chain commands, NOT && (that's bash/cmd)
#   
#   WHAT DOES NOT WORK:
#     [X] python repl_main.py instructions
#     [X] python repl_main.py --command instructions
#   
#   WHAT WORKS:
#     [OK] echo 'instructions' | python repl_main.py
#   
#   Step 1: Set environment and pipe command:
#     cd {self.workspace_root}
#     $env:PYTHONPATH = "{self.workspace_root}"
#     $env:BOT_DIRECTORY = "{self.workspace_root}\\{self.bot_location}"
#     $env:WORKING_AREA = "<project_path>"  # e.g. demo\\mob_minion
#     echo "instructions" | python {rel_repl_path}
#   
#   Step 2: Read output, do work (create files, etc.)
#   Step 3: Pipe next command: echo "next" | python repl_main.py
#   Step 4: Repeat for each step in workflow
#   
#   REPL exits after each command - this is NORMAL in piped mode

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$WORKSPACE_ROOT = Split-Path -Parent $SCRIPT_DIR

# Set environment variables
$env:PYTHONPATH = $WORKSPACE_ROOT
$env:BOT_DIRECTORY = Join-Path $WORKSPACE_ROOT "{self.bot_location}"
# WORKING_AREA is read from bot_config.json by repl_main.py - don't set it here

# Launch REPL
$REPL_PATH = Join-Path $WORKSPACE_ROOT "{rel_repl_path}"
python $REPL_PATH
"""
        script_file.write_text(script_content, encoding='utf-8')
        return script_file
