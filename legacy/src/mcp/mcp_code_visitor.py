import stat
from pathlib import Path
from typing import Dict, Any, List, Optional
from ..generator.visitor import Visitor
from ..generator.help_context import BehaviorHelpContext, ActionHelpContext
from ..generator.action_data_collector import ActionDataCollector
from ..repl_cli.description_extractor import DescriptionExtractor
from ..repl_cli.formatter import CliTerminalFormatter

class MCPCodeVisitor(Visitor):
    
    def __init__(self, workspace_root: Path, bot_location: Path, behaviors: List[str], bot=None):
        super().__init__(bot=bot)
        self.workspace_root = workspace_root
        self.bot_location = bot_location
        self.behaviors = behaviors
        self.tool_registrations = []
        self.trigger_words_map = {}
        self.server_file_path = None
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
    
    def visit_header(self, bot_name: str = None) -> None:
        # bot_name available from self.bot_name (inherited), parameter kept for interface compatibility
        for behavior in self.behaviors:
            trigger_words = self._load_trigger_words(behavior)
            self.trigger_words_map[behavior] = trigger_words
    
    def visit_behavior(self, context: BehaviorHelpContext) -> None:
        behavior_name = context.behavior_name
        trigger_patterns = self.trigger_words_map.get(behavior_name, [])
        description = self._build_behavior_tool_description(behavior_name, trigger_patterns)
        
        tool_code = self._generate_behavior_tool_code(behavior_name, description)
        self.tool_registrations.append(tool_code)
    
    def visit_action(self, context: ActionHelpContext) -> None:
        pass
    
    def visit_action_help_section_header(self) -> None:
        pass
    
    def visit_footer(self) -> None:
        self._create_mcp_server_file()
    
    def create_server_file(self) -> Path:
        if self.server_file_path is None:
            self._create_mcp_server_file()
        return self.server_file_path
    
    def _load_trigger_words(self, behavior: str) -> List[str]:
        if self.bot is None:
            return []
        behavior_obj = self.bot.behaviors.find_by_name(behavior)
        if behavior_obj is None:
            return []
        trigger_words = behavior_obj.trigger_words
        if isinstance(trigger_words, dict):
            return trigger_words.get('patterns', [])
        if isinstance(trigger_words, list):
            return trigger_words
        return []
    
    def _build_behavior_tool_description(self, behavior: str, trigger_patterns: List[str]) -> str:
        description = f'{behavior} behavior for {self.bot.bot_name}. Accepts optional action parameter and parameters dict.'
        if trigger_patterns:
            description += f"\nTrigger patterns: {', '.join(trigger_patterns[:5])}"
        return description
    
    def _generate_behavior_tool_code(self, behavior: str, description: str) -> str:
        escaped_description = description.replace("'", "\\'").replace('"', '\\"')
        return f'''    @mcp_server.tool(name='{behavior}', description='{escaped_description}')
    async def {behavior}_tool(action: str=None, parameters: dict=None):
        behavior_obj = bot.behaviors.find_by_name('{behavior}')
        if action:
            action_obj = behavior_obj.actions.find_by_name(action)
            result_data = action_obj.execute(parameters or {{}})
            return {{'status': 'completed', 'behavior': '{behavior}', 'action': action, 'data': result_data}}
        behavior_obj.actions.load_state()
        current_action = behavior_obj.actions.current
        result_data = current_action.execute(parameters or {{}})
        return {{'status': 'completed', 'behavior': '{behavior}', 'action': current_action.action_name, 'data': result_data}}'''
    
    def _create_mcp_server_file(self) -> Path:
        bot_dir = self.workspace_root / self.bot_location
        src_dir = bot_dir / 'src'
        src_dir.mkdir(parents=True, exist_ok=True)
        server_file = src_dir / f'{self.bot.bot_name}_mcp_server.py'
        self.server_file_path = server_file
        
        base_tools_code = self._generate_base_tools_code()
        behavior_tools_code = '\n\n'.join(self.tool_registrations)
        
        server_code = self._build_server_code(base_tools_code, behavior_tools_code)
        server_file.write_text(server_code, encoding='utf-8')
        self.server_file_path = server_file
        return server_file
    
    def _build_server_code(self, base_tools_code: str, behavior_tools_code: str) -> str:
        docstring = self._build_server_docstring()
        imports = self._build_server_imports()
        main_function = self._build_server_main_function(base_tools_code, behavior_tools_code)
        return f'''{docstring}
{imports}

{main_function}
'''
    
    def _build_server_docstring(self) -> str:
        bot_title = self.bot.bot_name.title().replace('_', ' ')
        return f'''"""
{bot_title} MCP Server Entry Point

Runnable MCP server for {self.bot.bot_name} using FastMCP with statically generated tools.
"""'''
    
    def _build_server_imports(self) -> str:
        return '''from pathlib import Path
import sys
import os
import json
from datetime import datetime
import logging

python_workspace_root = Path(__file__).parent.parent.parent.parent.parent
if str(python_workspace_root) not in sys.path:
    sys.path.insert(0, str(python_workspace_root))

bot_directory = Path(__file__).parent.parent
os.environ['BOT_DIRECTORY'] = str(bot_directory)

if 'WORKING_AREA' not in os.environ:
    config_path = bot_directory / 'bot_config.json'
    if config_path.exists():
        bot_config = json.loads(config_path.read_text(encoding='utf-8'))
        if 'mcp' in bot_config and 'env' in bot_config['mcp']:
            mcp_env = bot_config['mcp']['env']
            if 'WORKING_AREA' in mcp_env:
                os.environ['WORKING_AREA'] = mcp_env['WORKING_AREA']

from agile_bot.bots.base_bot.src.bot.workspace import (
    get_bot_directory,
    get_workspace_directory,
    get_python_workspace_root
)
from agile_bot.bots.base_bot.src.bot.bot import Bot, BotResult
from agile_bot.bots.base_bot.src.mcp.server_restart import restart_mcp_server
from fastmcp import FastMCP

logger = logging.getLogger(__name__)'''
    
    def _build_server_main_function(self, base_tools_code: str, behavior_tools_code: str) -> str:
        return f'''def main():
    """Main entry point for {self.bot_name} MCP server.

    Environment variables are bootstrapped before import:
    - BOT_DIRECTORY: Self-detected from script location
    - WORKING_AREA: Read from bot_config.json (or overridden by mcp.json env)
    
    All subsequent code reads from these environment variables.
    """
    bot_directory = get_bot_directory()
    workspace_directory = get_workspace_directory()
    
    bot = Bot(bot_name='{self.bot_name}', bot_directory=bot_directory, config_path=bot_directory / 'bot_config.json')
    
    server_name = '{self.bot.bot_name}'
    mcp_server = FastMCP(server_name)
    
    {base_tools_code}
    
    {behavior_tools_code}
    
    mcp_server.run()

if __name__ == '__main__':
    main()'''
    
    def _generate_base_tools_code(self) -> str:
        bot_tool_code = self._generate_bot_tool_code()
        get_working_dir_code = self._generate_get_working_dir_code()
        set_working_dir_code = self._generate_set_working_dir_code()
        close_action_code = self._generate_close_action_code()
        confirm_out_of_order_code = self._generate_confirm_out_of_order_code()
        restart_server_code = self._generate_restart_server_code()
        
        return '\n\n'.join([
            bot_tool_code,
            get_working_dir_code,
            set_working_dir_code,
            close_action_code,
            confirm_out_of_order_code,
            restart_server_code
        ])
    
    def _generate_bot_tool_code(self) -> str:
        return f'''    @mcp_server.tool(name='tool', description='Bot tool for {self.bot.bot_name} - routes to current behavior and action.')
    async def bot_tool(parameters: dict=None):
        current_behavior = bot.behaviors.current
        if current_behavior is None:
            if bot.behaviors.first:
                bot.behaviors.navigate_to(bot.behaviors.first.name)
                current_behavior = bot.behaviors.current
            else:
                raise ValueError('No behaviors available')
        if current_behavior is None:
            raise ValueError('No current behavior')
        action = current_behavior.actions.forward_to_current()
        result_data = action.execute(parameters or {{}})
        result = BotResult(status='completed', behavior=current_behavior.name, action=action.action_name, data=result_data)
        return {{'status': result.status, 'behavior': result.behavior, 'action': result.action, 'data': result.data}}'''
    
    def _generate_get_working_dir_code(self) -> str:
        return f'''    @mcp_server.tool(name='get_working_dir', description="Get the current working directory from WORKING_AREA. Triggers: where are we working, what's my location, show working directory")
    async def get_working_dir(input_file: str=None, project_dir: str=None):
        working_dir = get_workspace_directory()
        return {{'working_dir': str(working_dir), 'message': f'Working directory from WORKING_AREA: {{working_dir}}'}}'''
    
    def _generate_set_working_dir_code(self) -> str:
        return f'''    @mcp_server.tool(name='set_working_dir', description="Update the working directory (WORKING_AREA/WORKING_DIR). Triggers: update working directory, change working path, change working folder, set workspace")
    async def set_working_dir(new_path: str, persist: bool=True):
        if not new_path:
            return {{'error': 'missing_path', 'message': 'new_path is required'}}
        try:
            previous = str(bot.bot_paths.workspace_directory)
        except Exception:
            previous = None
        try:
            resolved = str(bot.bot_paths.update_workspace_directory(new_path, persist=persist))
            return {{'working_dir': resolved, 'previous_working_dir': previous, 'persisted': bool(persist), 'message': f'Working directory updated to {{resolved}}'}}
        except Exception as e:
            logger.error(f'Failed to set working directory: {{e}}', exc_info=True)
            return {{'error': 'failed_to_set_working_dir', 'message': str(e)}}'''
    
    def _generate_close_action_code(self) -> str:
        return f'''    @mcp_server.tool(name='close_current_action', description='Close current action tool for {self.bot.bot_name} - marks current action complete and transitions to next')
    async def close_current_action(parameters: dict=None):
        state_file = bot.bot_paths.workspace_directory / 'behavior_action_state.json'
        if not state_file.exists():
            return {{'error': 'No active state found', 'message': 'No behavior_action_state.json exists. Start a behavior first.'}}
        try:
            current_behavior = bot.behaviors.current
            current_behavior.actions.load_state()
            current_action = current_behavior.actions.current
            action_name = current_action.action_name
            action_names = current_behavior.actions.names
            is_final_action = action_name == action_names[-1] if action_names else False
            current_behavior.actions.close_current()
            new_action = current_behavior.actions.current
            behavior_complete = new_action is None or (is_final_action and new_action.action_name == action_name)
            if behavior_complete:
                next_behavior = bot.behaviors.next()
                if next_behavior:
                    bot.behaviors.navigate_to(next_behavior.name)
                    next_behavior.actions.load_state()
                    first_action = next_behavior.actions.current.action_name if next_behavior.actions.current else 'clarify'
                    return {{'status': 'completed', 'completed_action': action_name, 'completed_behavior': current_behavior.name, 'next_behavior': next_behavior.name, 'next_action': first_action, 'message': f"Behavior '{{current_behavior.name}}' complete. Transitioned to behavior '{{next_behavior.name}}', action '{{first_action}}'."}}
                return {{'status': 'completed', 'completed_action': action_name, 'completed_behavior': current_behavior.name, 'message': f"Action '{{action_name}}' marked complete. All behaviors complete."}}
            new_action_name = current_behavior.actions.current.action_name if current_behavior.actions.current else None
            return {{'status': 'completed', 'completed_action': action_name, 'next_action': new_action_name, 'message': f"Action '{{action_name}}' marked complete. Transitioned to '{{new_action_name}}'."}}
        except Exception as e:
            return {{'error': 'Failed to close current action', 'message': str(e)}}'''
    
    def _generate_confirm_out_of_order_code(self) -> str:
        return f'''    @mcp_server.tool(name='confirm_out_of_order', description='Confirm out-of-order behavior execution for {self.bot.bot_name} - MUST be called explicitly by HUMAN USER, NOT by AI assistant. AI must ask user to call this tool, never call it directly.')
    async def confirm_out_of_order(behavior: str):
        working_dir = get_workspace_directory()
        state_file = working_dir / 'behavior_action_state.json'
        try:
            state_data = json.loads(state_file.read_text(encoding='utf-8'))
            if 'out_of_order_confirmations' not in state_data:
                state_data['out_of_order_confirmations'] = {{}}
            state_data['out_of_order_confirmations'][behavior] = {{'confirmed_at': datetime.now().isoformat(), 'confirmed_by': 'human'}}
            state_file.write_text(json.dumps(state_data, indent=2), encoding='utf-8')
            return {{'status': 'confirmed', 'behavior': behavior, 'message': f"Out-of-order execution confirmed for behavior '{{behavior}}'. You may now execute this behavior.", 'confirmed_at': state_data['out_of_order_confirmations'][behavior]['confirmed_at']}}
        except Exception as e:
            return {{'error': 'Failed to confirm out-of-order execution', 'message': str(e)}}'''
    
    def _generate_restart_server_code(self) -> str:
        return f'''    @mcp_server.tool(name='restart_server', description='Restart MCP server for {self.bot.bot_name} - terminates processes, clears cache, and restarts to load code changes')
    async def restart_server(parameters: dict=None):
        try:
            workspace_root = get_python_workspace_root()
            bot_location = str(bot_directory.relative_to(workspace_root))
            result = restart_mcp_server(workspace_root=workspace_root, bot_name='{self.bot.bot_name}', bot_location=bot_location)
            return result
        except Exception as e:
            logger.error(f'Failed to restart MCP server: {{e}}', exc_info=True)
            return {{'status': 'error', 'error': 'Failed to restart server', 'message': str(e)}}'''
