from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from agile_bot.bots.base_bot.src.repl_cli.cli_bot.cli_bot import CLIBot
    from agile_bot.bots.base_bot.src.repl_cli.cli_bot.cli_behavior import CLIBehavior
    from agile_bot.bots.base_bot.src.repl_cli.cli_bot.cli_actions.cli_action import CLIAction


class StatusDisplay:
    
    def __init__(self, cli_bot: CLIBot):
        self.cli_bot = cli_bot
        self.header = HeaderDisplay()
        self.hierarchy = HierarchyTreeDisplay()
        self.footer = FooterDisplay()
        self.headless = HeadlessModeStatusDisplay()
    
    def render(self) -> str:
        header_text = self.header.render(self.cli_bot)
        hierarchy_text = self.hierarchy.render(self.cli_bot)
        headless_text = self.headless.render()
        footer_text = self.footer.render()
        
        return f"{header_text}\n\n{hierarchy_text}\n\n{headless_text}\n\n{footer_text}"


class HeaderDisplay:
    
    def render(self, cli_bot: CLIBot) -> str:
        bot_name = cli_bot.name.upper().replace('_', ' ')
        workspace_path = cli_bot.path
        
        header = f"{bot_name} CLI"
        header += f"\nBot Path: {cli_bot.bot_directory}"
        header += f"\nWorking Area: {workspace_path}"
        
        return header


class HierarchyTreeDisplay:
    
    def render(self, cli_bot: CLIBot) -> str:
        lines = []
        
        current_behavior = cli_bot.behaviors.current
        behaviors = cli_bot.behaviors.all
        
        for behavior_name in behaviors:
            behavior = cli_bot.behaviors.get_behavior(behavior_name)
            if behavior is None:
                continue
            
            is_current = current_behavior and behavior.name == current_behavior.name
            status_icon = "[*]" if is_current else "[ ]"
            
            lines.append(f"{status_icon} {behavior.name}")
            
            if is_current and behavior.actions:
                current_action = behavior.actions.current
                actions = behavior.actions.names
                
                for action_name in actions:
                    action = behavior.actions.get_action(action_name)
                    if action is None:
                        continue
                    
                    is_current_action = current_action and action.name == current_action.name
                    action_icon = "    [*]" if is_current_action else "    [ ]"
                    lines.append(f"{action_icon} {action.name}")
        
        return "\n".join(lines) if lines else "No behaviors loaded"


class HeadlessModeStatusDisplay:
    
    def __init__(self, workspace_directory=None):
        from pathlib import Path
        from agile_bot.bots.base_bot.src.repl_cli.headless.headless_config import HeadlessConfig
        try:
            self._config = HeadlessConfig.load()
        except Exception:
            self._config = None
        self._workspace_directory = Path(workspace_directory) if workspace_directory else None
        self._active_session = self._detect_active_session()
    
    @property
    def is_configured(self) -> bool:
        return self._config is not None and self._config.is_configured
    
    def _detect_active_session(self) -> dict:
        """Detect running headless session from log files."""
        from pathlib import Path
        
        if self._workspace_directory:
            log_dir = self._workspace_directory / 'logs'
        elif self._config:
            log_dir = self._config.log_dir
        else:
            return None
        
        if not log_dir.exists():
            return None
        
        # Look for headless session log files
        for log_file in log_dir.glob('headless-*.log'):
            # Extract session ID from filename
            session_id = log_file.stem.replace('headless-', '')
            return {
                'session_id': session_id,
                'log_path': str(log_file),
                'status': 'running'
            }
        
        return None
    
    def set_active_session(self, session_id: str, log_path: str) -> None:
        self._active_session = {'session_id': session_id, 'log_path': log_path, 'status': 'running'}
    
    def render(self) -> str:
        lines = ["Headless Mode:"]
        
        if self.is_configured:
            lines.append(f"  Status: Available (configured)")
            lines.append(f"  API Key: {self._config.api_key_prefix}")
            lines.append("")
            lines.append("  Usage:")
            lines.append("    python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless \"Your instruction\"")
            lines.append("")
            lines.append("  Examples:")
            lines.append("    python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless \"Create hello world\"")
            lines.append("    python agile_bot/bots/base_bot/src/repl_cli/repl_main.py --headless shape")
            lines.append("    python agile_bot/bots/base_bot/src/repl_cli/repl_main.py --headless shape.build")
            
            if self._active_session:
                lines.append("")
                lines.append("  Active Session:")
                lines.append(f"    Session ID: {self._active_session['session_id']}")
                lines.append(f"    Status: {self._active_session['status']}")
                lines.append(f"    Log: {self._active_session['log_path']}")
        else:
            lines.append("  Status: Unavailable (not configured)")
            lines.append("")
            lines.append("  To configure:")
            lines.append("    1. Install cursor-agent in WSL: wsl -d Ubuntu -e bash -c \"curl https://cursor.com/install -fsS | bash\"")
            lines.append("    2. Add API key to: agile_bot/secrets/cursor_api_key.txt")
        
        return "\n".join(lines)


class FooterDisplay:
    
    def render(self) -> str:
        commands = [
            "status",
            "back",
            "next",
            "help",
            "exit"
        ]
        return f"Commands: {' | '.join(commands)}"


class BreadcrumbVisitor:
    
    def __init__(self):
        self.breadcrumbs = []
    
    def visit_behavior(self, behavior: CLIBehavior) -> None:
        self.breadcrumbs.append(behavior.name)
    
    def visit_action(self, action: CLIAction) -> None:
        self.breadcrumbs.append(action.name)
    
    def get_output(self) -> str:
        return " > ".join(self.breadcrumbs)
    
    def reset(self) -> None:
        self.breadcrumbs = []

