from pathlib import Path
import json
import logging
from typing import Dict, Any
from ..utils import read_json_file
from ..bot.bot import Bot
from ..bot.workspace import get_python_workspace_root, get_base_actions_directory, get_workspace_directory
from .mcp_code_generator import MCPCodeGenerator
from .mcp_config_generator import MCPConfigGenerator

class MCPServerGenerator:

    def __init__(self, bot_directory: Path):
        self.bot_directory = Path(bot_directory)
        self.bot_name = self.bot_directory.name
        self.config_path = self.bot_directory / 'bot_config.json'
        self.bot = None
        self.code_generator = MCPCodeGenerator(self.bot_name, self.bot_directory)
        self.config_generator = MCPConfigGenerator(self.bot_name, self.bot_directory, self.config_path)
        self.workflow_actions = self._discover_workflow_actions()
        self.independent_actions = self._discover_independent_actions()

    def _discover_workflow_actions(self) -> list:
        base_actions_path = get_base_actions_directory()
        workflow_actions = []
        for item in base_actions_path.iterdir():
            if item.is_dir() and (not item.name.startswith('.')):
                action_name = item.name
                workflow_actions.append(action_name)
        return sorted(workflow_actions)

    def _discover_independent_actions(self) -> list:
        base_actions_path = get_base_actions_directory()
        independent_actions = []
        for item in base_actions_path.iterdir():
            if item.is_dir() and (not item.name.startswith('.')):
                independent_actions.append(item.name)
        return independent_actions

    def _ensure_bot_initialized(self) -> None:
        """Ensure bot instance is initialized. Used by methods that need bot access."""
        if self.bot is None:
            if not self.config_path.exists():
                raise FileNotFoundError(f'Bot Config not found at {self.config_path}')
            try:
                read_json_file(self.config_path)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(f'Malformed Bot Config at {self.config_path}: {e.msg}', e.doc, e.pos)
            self.bot = Bot(bot_name=self.bot_name, bot_directory=self.bot_directory, config_path=self.config_path)

    def _get_bot_behaviors(self) -> list:
        if self.bot and hasattr(self.bot, 'behaviors'):
            behaviors_collection = self.bot.behaviors
            if hasattr(behaviors_collection, 'names'):
                return behaviors_collection.names
        return []

    def _infer_working_dir_from_parameters(self, parameters: dict) -> Path:
        return get_workspace_directory()

    def _execute_entry_workflow(self, working_dir: Path, parameters: dict) -> dict:
        stories_dir = working_dir / 'docs' / 'stories'
        existing_artifacts = []
        if stories_dir.exists():
            bot_behaviors = self._get_bot_behaviors()
            for behavior in bot_behaviors:
                behavior_artifacts = self._check_behavior_artifacts(stories_dir, behavior)
                if behavior_artifacts:
                    existing_artifacts.append({'behavior': behavior, 'artifacts': behavior_artifacts})
        earliest_missing = None
        bot_behaviors = self._get_bot_behaviors()
        for behavior in bot_behaviors:
            has_artifacts = any((a['behavior'] == behavior for a in existing_artifacts))
            if not has_artifacts:
                earliest_missing = behavior
                break
        if earliest_missing is None:
            earliest_missing = bot_behaviors[-1] if bot_behaviors else None
        message = f'**ENTRY STATE - No behavior_action_state.json found**\n\n'
        message += f'Checking for existing artifacts in `{stories_dir}`...\n\n'
        if existing_artifacts:
            message += '**Found existing artifacts:**\n'
            for artifact in existing_artifacts:
                message += f"- {artifact['behavior']}: {', '.join(artifact['artifacts'])}\n"
            message += '\n'
        else:
            message += 'No existing artifacts found.\n\n'
        message += f'**Suggested starting behavior:** `{earliest_missing}`\n\n'
        message += '**Available behaviors:**\n'
        bot_behaviors = self._get_bot_behaviors()
        for i, behavior in enumerate(bot_behaviors, 1):
            status = '✓' if any((a['behavior'] == behavior for a in existing_artifacts)) else ' '
            message += f'{i}. [{status}] {behavior}\n'
        message += '\n**Please confirm which behavior to start with.**\n'
        if earliest_missing and earliest_missing in bot_behaviors:
            message += f"Reply with the behavior name (e.g., '{earliest_missing}') or number (e.g., '{bot_behaviors.index(earliest_missing) + 1}')."
        else:
            message += f"Reply with the behavior name (e.g., '{earliest_missing}')."
        return {'status': 'requires_confirmation', 'message': message, 'suggested_behavior': earliest_missing, 'available_behaviors': bot_behaviors, 'existing_artifacts': existing_artifacts, 'working_dir': str(working_dir)}

    def _check_behavior_artifacts(self, stories_dir: Path, behavior: str) -> list:
        artifacts = []
        patterns = {'shape': ['*story_map*', '*epic*', '*sub_epic*', '*feature*'], 'prioritization': ['*increment*', '*priority*', '*backlog*'], 'arrange': ['*arrangement*', '*execution_order*'], 'discovery': ['*discovery*', '*flow*', '*rules*'], 'exploration': ['*exploration*', '*criteria*'], 'scenarios': ['*.feature', '*scenario*'], 'tests': ['*test*.py', '*_test.py', 'test_*.py']}
        behavior_patterns = patterns.get(behavior, [])
        for pattern in behavior_patterns:
            matches = list(stories_dir.rglob(pattern))
            for match in matches:
                if match.is_file():
                    artifacts.append(match.name)
        return artifacts

    def _load_trigger_words_from_behavior_folder(self, behavior: str, action: str=None) -> list:
        self._ensure_bot_initialized()
        behavior_obj = self.bot.behaviors.find_by_name(behavior)
        if behavior_obj is None:
            return []
        trigger_words = behavior_obj.trigger_words
        if isinstance(trigger_words, dict):
            return trigger_words.get('patterns', [])
        if isinstance(trigger_words, list):
            return trigger_words
        return []

    def generate_bot_config_file(self, behaviors: list) -> Path:
        return self.config_generator.generate_bot_config_file(behaviors)

    def generate_server_entry_point(self) -> Path:
        self._ensure_bot_initialized()
        behaviors = self._get_bot_behaviors()
        return self.code_generator.generate_server_entry_point(behaviors, self.bot)

    def generate_cursor_mcp_config(self) -> Dict:
        return self.config_generator.generate_cursor_mcp_config()

    def discover_behaviors_from_folders(self) -> list:
        self._ensure_bot_initialized()
        return self._get_bot_behaviors()

    def generate_server(self, behaviors: list=None) -> Dict[str, Path]:
        if behaviors is None:
            behaviors = self.discover_behaviors_from_folders()
        bot_config_path = self.generate_bot_config_file(behaviors)
        server_entry_path = self.generate_server_entry_point()
        mcp_config = self.generate_cursor_mcp_config()
        return {'bot_config': bot_config_path, 'server_entry': server_entry_path, 'mcp_config': mcp_config}

    def generate_awareness_files(self) -> Dict[str, Path]:
        self._ensure_bot_initialized()
        rules_path = self.config_generator.generate_workspace_rules_file(self.discover_behaviors_from_folders, self._load_behavior_trigger_info)
        return {'rules_file': rules_path}

    def _extract_trigger_words(self, trigger_words_data) -> list:
        if isinstance(trigger_words_data, dict):
            return trigger_words_data.get('patterns', [])
        if isinstance(trigger_words_data, list):
            return trigger_words_data
        return []

    def _load_behavior_trigger_info(self, behavior: str) -> dict:
        self._ensure_bot_initialized()
        behavior_obj = self.bot.behaviors.find_by_name(behavior)
        if behavior_obj is None:
            return None
        try:
            description = behavior_obj.description
            trigger_words = self._extract_trigger_words(behavior_obj.trigger_words)
            if not trigger_words:
                trigger_words = self._load_trigger_words_from_behavior_folder(behavior=behavior, action=None)
            return {'description': description, 'trigger_words': trigger_words}
        except Exception as e:
            logging.getLogger(__name__).debug(f'Failed to load trigger words for {behavior}: {e}')
            return None