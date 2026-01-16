from pathlib import Path
from typing import Dict, Set, List, Optional
from ...generator.visitor import Visitor
from ...generator.help_context import BehaviorHelpContext, ActionHelpContext
from ...generator.action_data_collector import ActionDataCollector
from ..description_extractor import DescriptionExtractor
from ..formatter import CliTerminalFormatter

class REPLCursorCommandVisitor(Visitor):
    """Visitor that generates Cursor command files for REPL CLI using piped syntax."""
    
    def __init__(self, workspace_root: Path, repl_script_path: Path, bot=None):
        super().__init__(bot=bot)
        self.workspace_root = workspace_root
        self.repl_script_path = repl_script_path
        self.commands_dir: Optional[Path] = None
        self.piped_command: Optional[str] = None
        self.commands: Dict[str, Path] = {}
        self.current_command_files: Set[Path] = set()
        self._formatter: Optional[CliTerminalFormatter] = None
        self._description_extractor: Optional[DescriptionExtractor] = None
        self._data_collector: Optional[ActionDataCollector] = None
    
    @property
    def formatter(self) -> CliTerminalFormatter:
        if self._formatter is None:
            self._formatter = CliTerminalFormatter()
        return self._formatter
    
    @property
    def description_extractor(self) -> DescriptionExtractor:
        if self._description_extractor is None:
            self._description_extractor = DescriptionExtractor(self.bot_name, self.bot_directory, self.formatter)
        return self._description_extractor
    
    @property
    def data_collector(self) -> ActionDataCollector:
        if self._data_collector is None:
            self._data_collector = ActionDataCollector(
                bot=self.bot,
                bot_name=self.bot_name,
                bot_directory=self.bot_directory,
                description_extractor=self.description_extractor
            )
        return self._data_collector
    
    def visit_header(self, bot_name: str) -> None:
        self.commands_dir = self._ensure_commands_directory()
        self.piped_command = self._get_piped_command()
        self.current_command_files = self._get_current_command_files()
        self._generate_base_commands()
    
    def visit_behavior(self, context: BehaviorHelpContext) -> None:
        behavior_command = self._build_behavior_command(context.behavior_name)
        behavior_name_underscore = context.behavior_name.replace('-', '_')
        self.commands[f'{self.bot_name}_{behavior_name_underscore}'] = self._write_command_file(
            self.commands_dir / f'{self.bot_name}_{behavior_name_underscore}.md',
            behavior_command
        )
    
    def visit_action(self, context: ActionHelpContext) -> None:
        pass
    
    def visit_action_help_section_header(self) -> None:
        pass
    
    def visit_footer(self) -> None:
        self._remove_obsolete_command_files()
    
    def _ensure_commands_directory(self) -> Path:
        commands_dir = self.workspace_root / '.cursor' / 'commands'
        commands_dir.mkdir(parents=True, exist_ok=True)
        return commands_dir
    
    def _get_piped_command(self) -> str:
        rel_repl_script_path = self.repl_script_path.relative_to(self.workspace_root) if self.repl_script_path.is_absolute() else self.repl_script_path
        script_path_str = str(rel_repl_script_path).replace('\\', '/')
        return f"echo '${{1:command}}' | python {script_path_str}"
    
    def _get_current_command_files(self) -> Set[Path]:
        try:
            bot_prefix = f'{self.bot_name}_'
            existing_files = set()
            for file_path in self.commands_dir.glob(f'{bot_prefix}*.md'):
                existing_files.add(file_path)
            return existing_files
        except (FileNotFoundError, OSError):
            return set()
    
    def _generate_base_commands(self) -> None:
        base_command_content = self._build_base_repl_command()
        self.commands[f'{self.bot_name}'] = self._write_command_file(
            self.commands_dir / f'{self.bot_name}.md',
            base_command_content
        )
        
        # Generate separate status command
        status_command_content = self._build_status_command()
        self.commands[f'{self.bot_name}_status'] = self._write_command_file(
            self.commands_dir / f'{self.bot_name}_status.md',
            status_command_content
        )
    
    def _build_status_command(self) -> str:
        """Build a dedicated status command for quick access."""
        script_path_str = str(self.repl_script_path.relative_to(self.workspace_root) if self.repl_script_path.is_absolute() else self.repl_script_path).replace('\\', '/')
        bot_dir_str = str(self.bot_directory).replace('\\', '\\')
        workspace_str = str(self.workspace_root).replace('\\', '\\')
        
        lines = [
            f"# {self.bot_name}_status - Display Current Bot Status",
            "",
            "Display current position in workflow, active scope, and available commands.",
            "",
            "## Show Status",
            f"$env:BOT_DIRECTORY = '{bot_dir_str}'; $env:PYTHONPATH = '{workspace_str}'; echo 'status' | python {script_path_str}",
        ]
        return "\n".join(lines)
    
    def _build_base_repl_command(self) -> str:
        script_path_str = str(self.repl_script_path.relative_to(self.workspace_root) if self.repl_script_path.is_absolute() else self.repl_script_path).replace('\\', '/')
        bot_dir_str = str(self.bot_directory).replace('\\', '\\')
        workspace_str = str(self.workspace_root).replace('\\', '\\')
        
        lines = [
            f"# {self.bot_name} - REPL Status and Navigation",
            "",
            "## Status",
            f"$env:BOT_DIRECTORY = '{bot_dir_str}'; $env:PYTHONPATH = '{workspace_str}'; echo 'status' | python {script_path_str}",
            "",
            "## Help",
            f"$env:BOT_DIRECTORY = '{bot_dir_str}'; $env:PYTHONPATH = '{workspace_str}'; echo 'help' | python {script_path_str}",
            "",
            "## Navigation",
            f"$env:BOT_DIRECTORY = '{bot_dir_str}'; $env:PYTHONPATH = '{workspace_str}'; echo 'next' | python {script_path_str}",
            f"$env:BOT_DIRECTORY = '{bot_dir_str}'; $env:PYTHONPATH = '{workspace_str}'; echo 'back' | python {script_path_str}",
            "",
            "## Scope",
            f"$env:BOT_DIRECTORY = '{bot_dir_str}'; $env:PYTHONPATH = '{workspace_str}'; echo 'scope all' | python {script_path_str}",
            f"$env:BOT_DIRECTORY = '{bot_dir_str}'; $env:PYTHONPATH = '{workspace_str}'; echo 'scope \"${{1:story_name}}\"' | python {script_path_str}",
            "",
            "## Path",
            f"$env:BOT_DIRECTORY = '{bot_dir_str}'; $env:PYTHONPATH = '{workspace_str}'; echo 'path ${{1:project_path}}' | python {script_path_str}",
            "",
            "## Exit",
            f"$env:BOT_DIRECTORY = '{bot_dir_str}'; $env:PYTHONPATH = '{workspace_str}'; echo 'exit' | python {script_path_str}",
        ]
        return "\n".join(lines)
    
    def _build_behavior_command(self, behavior_name: str) -> str:
        script_path_str = str(self.repl_script_path.relative_to(self.workspace_root) if self.repl_script_path.is_absolute() else self.repl_script_path).replace('\\', '/')
        bot_dir_str = str(self.bot_directory).replace('\\', '\\')
        workspace_str = str(self.workspace_root).replace('\\', '\\')
        
        behavior = self.bot.behaviors.find_by_name(behavior_name)
        if not behavior:
            return ""
        
        action_names = []
        if self.data_collector:
            action_names = self.data_collector.get_behavior_actions(behavior)
        
        behavior_name_underscore = behavior_name.replace('-', '_')
        action_options = "|".join(action_names) if action_names else "action"
        
        lines = [
            f"# {self.bot_name}_{behavior_name_underscore} - Navigate to {behavior_name.capitalize()} Behavior",
            "",
            "## Navigate to Behavior",
            f"$env:BOT_DIRECTORY = '{bot_dir_str}'; $env:PYTHONPATH = '{workspace_str}'; echo '{behavior_name}' | python {script_path_str}",
            "",
            "## Navigate to Specific Action",
            f"$env:BOT_DIRECTORY = '{bot_dir_str}'; $env:PYTHONPATH = '{workspace_str}'; echo '{behavior_name}.${{1|{action_options}|}}' | python {script_path_str}",
            "",
        ]
        
        if action_names:
            lines.append("## Available Actions:")
            lines.append("")
            for action_name in action_names:
                action_desc = ""
                if self.data_collector:
                    action_desc = self.data_collector.get_action_description(action_name)
                    if action_desc:
                        short_desc = action_desc.split('\n')[0].split('.')[0]
                        lines.append(f"- {action_name} - {short_desc}")
                    else:
                        lines.append(f"- {action_name}")
                else:
                    lines.append(f"- {action_name}")
        
        return "\n".join(lines)
    
    def _build_action_command(self, behavior_name: str, action_name: str) -> str:
        script_path_str = str(self.repl_script_path.relative_to(self.workspace_root) if self.repl_script_path.is_absolute() else self.repl_script_path).replace('\\', '/')
        
        action_desc = ""
        if self.data_collector:
            action_desc = self.data_collector.get_action_description(action_name)
        
        short_desc = ""
        if action_desc:
            short_desc = action_desc.split('\n')[0].split('.')[0]
        
        behavior_name_underscore = behavior_name.replace('-', '_')
        action_name_underscore = action_name.replace('-', '_')
        
        lines = [
            f"# {self.bot_name}_{behavior_name_underscore}_{action_name_underscore} - Execute {behavior_name.capitalize()} {action_name.capitalize()} Action",
            "",
        ]
        
        if short_desc:
            lines.append(f"{short_desc}")
            lines.append("")
        
        lines.extend([
            "## Navigate to Action",
            f"echo '{behavior_name}.{action_name}' | python {script_path_str}",
            "",
            "## Get Instructions",
            f"echo '{behavior_name}.{action_name}.instructions' | python {script_path_str}",
            "",
            "## Submit Work",
            f"echo '{behavior_name}.{action_name}.submit${{1:+ }}${{1:--scope \"${{2:story_name}}\"}}' | python {script_path_str}",
            "",
            "## Confirm and Advance",
            f"echo '{behavior_name}.{action_name}.confirm' | python {script_path_str}",
        ])
        
        return "\n".join(lines)
    
    def _write_command_file(self, file_path: Path, command: str) -> Path:
        file_path.write_text(command, encoding='utf-8')
        return file_path
    
    def _remove_obsolete_command_files(self) -> None:
        current_file_paths = set(self.commands.values())
        for file_path in self.current_command_files:
            if file_path not in current_file_paths:
                file_path.unlink(missing_ok=True)
    
    def get_commands(self) -> Dict[str, Path]:
        return self.commands
