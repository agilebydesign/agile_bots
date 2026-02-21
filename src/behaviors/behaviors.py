from __future__ import annotations
import json
import logging
import traceback
from pathlib import Path
from typing import List, Optional, Iterator, Tuple, Dict, Any, TYPE_CHECKING
from datetime import datetime
from bot_path import BotPath
from utils import read_json_file
from instructions.reminders import inject_reminder_to_instructions
from behaviors.behavior import Behavior
if TYPE_CHECKING:
    from bot import BotResult
logger = logging.getLogger(__name__)

class Behaviors:

    def __init__(self, bot_name: str, bot_paths: BotPath, allowed_behaviors: Optional[List[str]] = None):
        self.bot_name = bot_name
        self.bot_paths = bot_paths
        self._allowed_behaviors = allowed_behaviors
        self._behaviors: List['Behavior'] = []
        self._discover_behaviors()
        self._current_index: Optional[int] = None
        self.load_state()

    def _load_behavior_from_dir(self, item: Path) -> tuple:
        behavior_json_path = item / 'behavior.json'
        if not behavior_json_path.exists():
            return None
        try:
            config = read_json_file(behavior_json_path)
            order = config.get('order', 999)
            behavior = Behavior(name=item.name, bot_paths=self.bot_paths, bot_instance=None)
            return (order, behavior)
        except Exception as e:
            logger.warning(f'Failed to load behavior {item.name}: {e}')
            logger.debug(f'Traceback: {traceback.format_exc()}')
            return None

    def _discover_behaviors(self) -> None:
        behaviors_dir = self.bot_paths.bot_directory / 'behaviors'
        if not behaviors_dir.exists():
            return
        behavior_orders = []
        for item in behaviors_dir.iterdir():
            if not item.is_dir() or item.name.startswith('_') or item.name.startswith('.'):
                continue
            if self._allowed_behaviors is not None and item.name not in self._allowed_behaviors:
                continue
            result = self._load_behavior_from_dir(item)
            if result:
                behavior_orders.append(result)
        behavior_orders.sort(key=lambda x: x[0])
        self._behaviors = [behavior for _, behavior in behavior_orders]

    @property
    def current(self) -> Optional['Behavior']:
        if self._current_index is not None and 0 <= self._current_index < len(self._behaviors):
            return self._behaviors[self._current_index]
        return None

    @property
    def names(self) -> List[str]:
        return [b.name for b in self._behaviors]

    @property
    def completed_behaviors(self) -> List[str]:
        completed = []
        for behavior in self._behaviors:
            if behavior.is_completed:
                completed.append(behavior.name)
        return completed

    @property
    def remaining_behaviors(self) -> List['Behavior']:
        return [b for b in self._behaviors if not b.is_completed]

    @property
    def next_step_command(self) -> Optional[str]:
        current = self.current
        if not current:
            return None
        remaining_actions = current.actions.remaining_actions
        if remaining_actions:
            return f'/{self.bot_name}-{current.name} {remaining_actions[0]}'
        next_behavior = self.next()
        if next_behavior and next_behavior.actions.names:
            return f'/{self.bot_name}-{next_behavior.name} {next_behavior.actions.names[0]}'
        return None

    @property
    def first(self) -> Optional['Behavior']:
        return self._behaviors[0] if self._behaviors else None

    def is_empty(self) -> bool:
        return len(self._behaviors) == 0

    def find_by_name(self, behavior_name: str) -> Optional['Behavior']:
        for behavior in self._behaviors:
            if behavior.name == behavior_name:
                return behavior
        return None

    def next(self) -> Optional['Behavior']:
        next_index = self._current_index + 1
        if next_index < len(self._behaviors):
            return self._behaviors[next_index]
        return None

    def next_after(self, behavior: 'Behavior') -> Optional['Behavior']:
        """Return the behavior that comes after the given behavior in sequence."""
        for i, b in enumerate(self._behaviors):
            if b.name == behavior.name:
                if i + 1 < len(self._behaviors):
                    return self._behaviors[i + 1]
                return None
        return None

    def previous(self) -> Optional['Behavior']:
        if self._current_index is None or self._current_index <= 0:
            return None
        prev_index = self._current_index - 1
        if prev_index >= 0:
            return self._behaviors[prev_index]
        return None
    
    def advance(self) -> Dict[str, Any]:
        if not self.current:
            return {
                'status': 'error',
                'message': 'No current behavior set'
            }
        
        current_behavior = self.current
        actions = current_behavior.actions
        if actions.current is None and actions.names:
            actions.navigate_to(actions.names[0])
        
        if actions.is_final_action():
            actions.close_current()
            next_behavior = self.next()
            if next_behavior:
                self._current_index += 1
                self.save_state()
                if next_behavior.actions.names:
                    next_behavior.actions.navigate_to(next_behavior.actions.names[0])
                return {
                    'status': 'success',
                    'message': f'Advanced to behavior: {next_behavior.name}',
                    'behavior': next_behavior.name,
                    'action': next_behavior.actions.current.action_name if next_behavior.actions.current else None
                }
            return {
                'status': 'complete',
                'message': 'Workflow complete - no more behaviors'
            }
        
        actions.close_current()
        return {
            'status': 'success',
            'message': f'Advanced to action: {actions.current.action_name if actions.current else None}',
            'behavior': current_behavior.name,
            'action': actions.current.action_name if actions.current else None
        }
    
    def go_back(self) -> Dict[str, Any]:
        if not self.current:
            return {
                'status': 'error',
                'message': 'No current behavior set'
            }
        
        current_behavior = self.current
        back_result = current_behavior.actions.go_back()
        
        if back_result['status'] == 'success':
            return back_result
        
        prev_behavior = self.previous()
        if prev_behavior:
            self._current_index -= 1
            self.save_state()
            if prev_behavior.actions._actions:
                last_action_name = prev_behavior.actions.names[-1]
                prev_behavior.actions.navigate_to(last_action_name)
            return {
                'status': 'success',
                'message': f'Went back to behavior: {prev_behavior.name}',
                'behavior': prev_behavior.name,
                'action': prev_behavior.actions.current.action_name if prev_behavior.actions.current else None
            }
        
        return back_result

    def __iter__(self) -> Iterator['Behavior']:
        for behavior in self._behaviors:
            yield behavior

    def check_exists(self, behavior_name: str) -> bool:
        return self.find_by_name(behavior_name) is not None

    def navigate_to(self, behavior_name: str):
        behavior = self.find_by_name(behavior_name)
        if behavior is None:
            raise ValueError(f"Behavior '{behavior_name}' not found")
        
        for i, b in enumerate(self._behaviors):
            if b.name == behavior.name:
                self._current_index = i
                break
        
        if self.current and self.current.actions:
            self.current.actions.load_state()
        
        self.save_state()

    def close_current(self):
        if self._current_index is not None and self.current:
            if self.current.actions and self.current.actions.current:
                self.current.actions.close_current()
            next_behavior = self.next()
            if next_behavior:
                self._current_index += 1
                self.save_state()

    def _get_next_behavior_reminder(self) -> str:
        try:
            next_behavior = self.next()
            if next_behavior:
                return f"After completing this behavior, the next behavior in sequence is `{next_behavior.name}`. When the user is ready to continue, remind them: 'The next behavior in sequence is `{next_behavior.name}`. Would you like to continue with `{next_behavior.name}` or work on a different behavior?'"
        except Exception as e:
            logger.debug(f'Failed to get next behavior reminder: {e}')
            raise
        return ''

    def save_state(self):
        if self.current is None or self.bot_paths is None:
            return
        workspace_dir = self.bot_paths.workspace_directory
        state_file = workspace_dir / 'behavior_action_state.json'
        state_data = {}
        if state_file.exists():
            try:
                content = state_file.read_text(encoding='utf-8')
                # Try to parse JSON, but handle corrupted files gracefully
                try:
                    state_data = json.loads(content)
                except json.JSONDecodeError as e:
                    # If JSON is corrupted, try to extract the first valid JSON object
                    logger.warning(f'State file {state_file} has corrupted JSON: {e}. Attempting recovery...')
                    # Try to find the first complete JSON object
                    content_cleaned = content.strip()
                    # Find the first complete JSON object by looking for balanced braces
                    brace_count = 0
                    end_pos = -1
                    for i, char in enumerate(content_cleaned):
                        if char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                end_pos = i + 1
                                break
                    if end_pos > 0:
                        try:
                            state_data = json.loads(content_cleaned[:end_pos])
                            logger.info(f'Recovered state from corrupted file (first {end_pos} chars)')
                        except json.JSONDecodeError:
                            logger.warning(f'Could not recover state from corrupted file, starting fresh')
                            state_data = {}
                    else:
                        logger.warning(f'Could not find valid JSON object in corrupted file, starting fresh')
                        state_data = {}
            except Exception as e:
                logger.warning(f'Failed to load state file {state_file}: {e}. Starting with empty state.')
                state_data = {}
        state_data['current_behavior'] = f'{self.bot_name}.{self.current.name}'
        if self.current.actions and self.current.actions.current:
            state_data['current_action'] = f'{self.bot_name}.{self.current.name}.{self.current.actions.current.action_name}'
        state_data['timestamp'] = datetime.now().isoformat()
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(json.dumps(state_data, indent=2), encoding='utf-8')

    def _init_to_first_behavior(self) -> None:
        if self._behaviors:
            self._current_index = 0

    def _find_behavior_index(self, behavior_name: str) -> int:
        for i, behavior in enumerate(self._behaviors):
            if behavior.name == behavior_name:
                return i
        return -1

    def _extract_behavior_name_from_state(self, current_behavior_full: str) -> str:
        if not current_behavior_full:
            return None
        parts = current_behavior_full.split('.')
        if len(parts) >= 2:
            return '.'.join(parts[1:])
        return None

    def load_state(self):
        if self.bot_paths is None:
            self._init_to_first_behavior()
            return
        workspace_dir = self.bot_paths.workspace_directory
        state_file = workspace_dir / 'behavior_action_state.json'
        if not state_file.exists() or not self._behaviors:
            self._init_to_first_behavior()
            return
        try:
            state_data = json.loads(state_file.read_text(encoding='utf-8'))
            behavior_name = self._extract_behavior_name_from_state(state_data.get('current_behavior', ''))

            if behavior_name:
                idx = self._find_behavior_index(behavior_name)
                if idx >= 0:
                    self._current_index = idx
                    if self.current:
                        self.current.actions.load_state()
                    return
            self._init_to_first_behavior()
        except Exception:
            self._init_to_first_behavior()

            self._init_to_first_behavior()

    def initialize_state(self, confirmed_behavior: str):
        if self.bot_paths is None:
            raise ValueError('Cannot initialize state without bot_paths')
        behavior_obj = self.find_by_name(confirmed_behavior)
        if behavior_obj is None:
            raise ValueError(f"Behavior '{confirmed_behavior}' not found. Available behaviors: {', '.join(self.names)}.")
        workspace_dir = self.bot_paths.workspace_directory
        state_file = workspace_dir / 'behavior_action_state.json'
        action_names = behavior_obj.actions.names
        first_action = action_names[0] if action_names else 'clarify'
        self.navigate_to(confirmed_behavior)
        state_data = {'current_behavior': f'{self.bot_name}.{behavior_obj.name}', 'current_action': f'{self.bot_name}.{behavior_obj.name}.{first_action}', 'completed_actions': [], 'timestamp': datetime.now().isoformat()}
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(json.dumps(state_data, indent=2), encoding='utf-8')