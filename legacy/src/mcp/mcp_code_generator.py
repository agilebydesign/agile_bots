from pathlib import Path
from typing import Dict, Any, List
from .mcp_code_visitor import MCPCodeVisitor
from ..repl_cli.formatter import CliTerminalFormatter
from ..bot.bot import Bot
from ..generator.orchestrator import Orchestrator

class MCPCodeGenerator:

    def __init__(self, bot_name: str, bot_directory: Path):
        self.bot_name = bot_name
        self.bot_directory = bot_directory

    def generate_server_entry_point(self, behaviors: List[str], bot: Bot) -> Path:
        workspace_root = self.bot_directory.parent.parent.parent.parent.parent
        formatter = CliTerminalFormatter()
        
        mcp_visitor = MCPCodeVisitor(
            workspace_root,
            self.bot_directory,
            behaviors,
            bot=bot
        )
        
        generator = Orchestrator(mcp_visitor)
        generator.generate()
        
        return mcp_visitor.create_server_file()







