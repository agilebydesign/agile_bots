from pathlib import Path
import json
from typing import Dict, Any
from ..bot.bot import Bot

class MCPServer:

    def __init__(self, bot_name: str, bot_directory: Path, config_path: Path):
        self.bot_name = bot_name
        self.bot_directory = Path(bot_directory)
        self.config_path = Path(config_path)
        self.bot = None

    def start(self):
        self.bot = Bot(bot_name=self.bot_name, bot_directory=self.bot_directory, config_path=self.config_path)

    def invoke_tool(self, tool_name: str, parameters: Dict[str, Any]):
        if self.bot is None:
            raise RuntimeError('Bot not initialized. Call start() first.')
        parameters = self._resolve_path_parameters(parameters)
        parameters = self._extract_behavior_action_from_tool_name(tool_name, parameters)
        return self.bot.invoke_tool(tool_name, parameters)

    def _resolve_path_parameters(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        if self.bot.bot_paths:
            return self.bot.bot_paths.resolve_path_parameters(parameters)
        return parameters

    def _extract_behavior_action_from_tool_name(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        parts = tool_name.split('_')
        if len(parts) < 3:
            return parameters
        without_bot_name = '_'.join(parts[2:])
        behavior, action = self._parse_behavior_action(without_bot_name)
        if behavior and action:
            parameters['behavior'] = behavior
            parameters['action'] = action
        return parameters

    def _parse_behavior_action(self, tool_suffix: str) -> tuple:
        action_keywords = ['clarify', 'strategy', 'build', 'render', 'validate', 'test_validate']
        for action_keyword in action_keywords:
            if tool_suffix.endswith(action_keyword):
                action = action_keyword
                behavior = tool_suffix[:-(len(action_keyword) + 1)]
                return (behavior, action)
        return (None, None)