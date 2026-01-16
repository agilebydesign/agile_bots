import importlib
from pathlib import Path
from typing import Dict, Any, TYPE_CHECKING
from .action import Action as BaseAction
from ..bot.workspace import get_base_actions_directory
from ..utils import read_json_file
if TYPE_CHECKING:
    from .action import Action
    from ..bot.behavior import Behavior

class ActionFactory:

    def __init__(self, behavior: 'Behavior'):
        self.behavior = behavior

    @staticmethod
    def get_action_class(action_name: str):
        action_module_mapping = {
            'clarify': ('clarify', 'clarify_action', 'ClarifyContextAction'),
            'strategy': ('strategy', 'strategy_action', 'StrategyAction'),
            'build': ('build', 'build_action', 'BuildKnowledgeAction'),
            'validate': ('validate', 'validate_action', 'ValidateRulesAction'),
            'render': ('render', 'render_action', 'RenderOutputAction'),
            'rules': ('rules', 'rules_action', 'RulesAction'),
        }
        mapping = action_module_mapping.get(action_name)
        if not mapping:
            return None
        module_name, module_file, class_name = mapping
        module_path = f'agile_bot.bots.base_bot.src.actions.{module_name}.{module_file}'
        try:
            module = importlib.import_module(module_path)
            return getattr(module, class_name)
        except (ModuleNotFoundError, AttributeError):
            return None

    def create_action_instance(self, action_name: str, action_config: Dict[str, Any]) -> 'Action':
        action_class_path = self._resolve_action_class_path(action_name, action_config)
        action_class = self._load_action_class(action_name, action_class_path)
        return self._instantiate_action(action_class, action_name, action_config)

    def _resolve_action_class_path(self, action_name: str, action_config: Dict[str, Any]) -> str:
        custom_class = action_config.get('action_class') or action_config.get('custom_class')
        if not custom_class:
            normalized = 'render' if action_name == 'render_output' else action_name
            base_config = read_json_file(get_base_actions_directory() / normalized / 'action_config.json')
            custom_class = base_config.get('action_class') or base_config.get('custom_class')
        if custom_class:
            return custom_class
        return self._get_default_action_class_path(action_name)

    def _get_default_action_class_path(self, action_name: str) -> str:
        action_module_mapping = {'clarify': ('clarify', 'clarify_action', 'ClarifyContextAction'), 'strategy': ('strategy', 'strategy_action', 'StrategyAction'), 'decide_strategy': ('strategy', 'strategy_action', 'StrategyAction'), 'build': ('build', 'build_action', 'BuildKnowledgeAction'), 'build_knowledge': ('build', 'build_action', 'BuildKnowledgeAction'), 'validate': ('validate', 'validate_action', 'ValidateRulesAction'), 'render': ('render', 'render_action', 'RenderOutputAction'), 'render_output': ('render', 'render_action', 'RenderOutputAction')}
        mapping = action_module_mapping.get(action_name)
        if mapping:
            module_name, module_file, class_name = mapping
            return f'agile_bot.bots.base_bot.src.actions.{module_name}.{module_file}.{class_name}'
        class_name = action_name.title().replace('_', '') + 'Action'
        return f'agile_bot.bots.base_bot.src.actions.{action_name}.{action_name}_action.{class_name}'

    def _load_action_class(self, action_name: str, action_class_path: str):
        module_path, class_name = action_class_path.rsplit('.', 1)
        try:
            module = importlib.import_module(module_path)
        except ModuleNotFoundError as e:
            raise ValueError(f"Action '{action_name}' cannot be loaded: module '{module_path}' not found.") from e
        try:
            return getattr(module, class_name)
        except AttributeError as e:
            raise ValueError(f"Action '{action_name}' cannot be loaded: class '{class_name}' not found.") from e

    def _instantiate_action(self, action_class, action_name: str, action_config: Dict[str, Any]):
        if action_class is BaseAction:
            return action_class(action_name=action_name, behavior=self.behavior, action_config=action_config)
        return action_class(behavior=self.behavior, action_config=action_config)