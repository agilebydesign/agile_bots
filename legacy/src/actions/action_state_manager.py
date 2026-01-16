import json
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime

class ActionStateManager:

    def __init__(self, behavior):
        self.behavior = behavior

    def get_state_file_path(self) -> Path:
        workspace_dir = self.behavior.bot_paths.workspace_directory
        return workspace_dir / 'behavior_action_state.json'

    def load_or_create_state(self, state_file: Path) -> dict:
        expected_behavior = f'{self.behavior.bot_name}.{self.behavior.name}'
        if state_file.exists():
            state_data = json.loads(state_file.read_text(encoding='utf-8'))
        else:
            state_data = {'current_behavior': expected_behavior, 'current_action': '', 'completed_actions': [], 'timestamp': datetime.now().isoformat()}
        if 'completed_actions' not in state_data:
            state_data['completed_actions'] = []
        return state_data

    def save_state(self, current_action_obj, state_file: Path):
        state_data = self.load_or_create_state(state_file)
        state_data['current_behavior'] = f'{self.behavior.bot_name}.{self.behavior.name}'
        if current_action_obj:
            state_data['current_action'] = f'{self.behavior.bot_name}.{self.behavior.name}.{current_action_obj.action_name}'
            state_data['timestamp'] = datetime.now().isoformat()
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(json.dumps(state_data, indent=2), encoding='utf-8')

    def load_state(self, actions_list: List, current_index_ref: list) -> None:
        state_data = self._load_state_data()
        if state_data is None:
            self._set_default_index(actions_list, current_index_ref)
            return
        if not self._is_current_behavior(state_data):
            self._set_default_index(actions_list, current_index_ref)
            return
        if self._try_set_from_current_action(state_data, actions_list, current_index_ref):
            return
        if self._try_set_from_completed_actions(state_data, actions_list, current_index_ref):
            return
        self._set_default_index(actions_list, current_index_ref)

    def _load_state_data(self) -> Optional[dict]:
        state_file = self.behavior.bot_paths.workspace_directory / 'behavior_action_state.json'
        if not state_file.exists():
            return None
        try:
            return json.loads(state_file.read_text(encoding='utf-8'))
        except Exception:
            return None

    def _is_current_behavior(self, state_data: dict) -> bool:
        expected = f'{self.behavior.bot_name}.{self.behavior.name}'
        return state_data.get('current_behavior', '') == expected

    def _set_default_index(self, actions_list: List, current_index_ref: list) -> None:
        if actions_list:
            current_index_ref[0] = 0

    def _try_set_from_current_action(self, state_data: dict, actions_list: List, current_index_ref: list) -> bool:
        current_action_full = state_data.get('current_action', '')
        if not current_action_full:
            return False
        parts = current_action_full.split('.')
        if len(parts) < 3:
            return False
        action_name = parts[-1]
        for i, action in enumerate(actions_list):
            if action.action_name == action_name:
                current_index_ref[0] = i
                return True
        return False

    def _try_set_from_completed_actions(self, state_data: dict, actions_list: List, current_index_ref: list) -> bool:
        completed_actions = state_data.get('completed_actions', [])
        expected_prefix = f'{self.behavior.bot_name}.{self.behavior.name}.'
        for completed in reversed(completed_actions):
            action_state = completed.get('action_state', '')
            if not action_state.startswith(expected_prefix):
                continue
            last_completed_name = action_state.split('.')[-1]
            index = self._find_action_index(actions_list, last_completed_name)
            if index is not None:
                current_index_ref[0] = index + 1 if index + 1 < len(actions_list) else index
                return True
        return False

    def _find_action_index(self, actions_list: List, action_name: str) -> Optional[int]:
        for i, action in enumerate(actions_list):
            if action.action_name == action_name:
                return i
        return None

    def find_action_index(self, actions_list: List, action_name: str) -> int:
        for i, action in enumerate(actions_list):
            if action.action_name == action_name:
                return i
        return -1

    def filter_completed_actions_after_target(self, completed_actions: list, target_index: int, actions_list: List) -> list:
        action_names_after_target = [a.action_name for a in actions_list[target_index + 1:]]
        expected_behavior_prefix = f'{self.behavior.bot_name}.{self.behavior.name}.'
        filtered = []
        for completed_action in completed_actions:
            action_state = completed_action.get('action_state', '')
            if not action_state.startswith(expected_behavior_prefix):
                filtered.append(completed_action)
                continue
            completed_action_name = action_state.split('.')[-1]
            if completed_action_name not in action_names_after_target:
                filtered.append(completed_action)
        return filtered