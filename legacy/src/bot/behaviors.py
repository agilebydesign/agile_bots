from __future__ import annotations
import json
import logging
import traceback
from pathlib import Path
from typing import List, Optional, Iterator, Tuple, Dict, Any, TYPE_CHECKING
from datetime import datetime
from .bot_paths import BotPaths
from ..utils import read_json_file
from .reminders import inject_reminder_to_instructions
from .behavior import Behavior
if TYPE_CHECKING:
    from .bot import BotResult
logger = logging.getLogger(__name__)

class Behaviors:

    def __init__(self, bot_name: str, bot_paths: BotPaths, allowed_behaviors: Optional[List[str]] = None):
        # #region agent log
        import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_path.parent.mkdir(parents=True, exist_ok=True); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'behaviors.py:18','message':'Behaviors.__init__ entry','data':{'bot_name':bot_name},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H1'})+'\n'); log_file.close()
        # #endregion
        self.bot_name = bot_name
        self.bot_paths = bot_paths
        self._allowed_behaviors = allowed_behaviors  # Filter behaviors by bot_config.json if provided
        self._behaviors: List['Behavior'] = []
        # #region agent log
        import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'behaviors.py:22','message':'Before _discover_behaviors','data':{},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H1'})+'\n'); log_file.close()
        # #endregion
        self._discover_behaviors()
        # #region agent log
        import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'behaviors.py:22','message':'After _discover_behaviors','data':{'behavior_count':len(self._behaviors)},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H1'})+'\n'); log_file.close()
        # #endregion
        self._current_index: Optional[int] = None
        # #region agent log
        import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'behaviors.py:24','message':'Before load_state','data':{},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H1'})+'\n'); log_file.close()
        # #endregion
        self.load_state()
        # #region agent log
        import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'behaviors.py:24','message':'After load_state - Behaviors.__init__ exit','data':{},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H1'})+'\n'); log_file.close()
        # #endregion

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
            # Filter by allowed_behaviors from bot_config.json if provided
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
        """Get list of completed behavior names."""
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
        """Get the next behavior without changing current state."""
        next_index = self._current_index + 1
        if next_index < len(self._behaviors):
            return self._behaviors[next_index]
        return None
    
    def previous(self) -> Optional['Behavior']:
        """Get the previous behavior without changing current state."""
        if self._current_index is None or self._current_index <= 0:
            return None
        prev_index = self._current_index - 1
        if prev_index >= 0:
            return self._behaviors[prev_index]
        return None
    
    def advance(self) -> Dict[str, Any]:
        """Advance to the next action in the current behavior, or next behavior if at end.
        
        Returns:
            Dict with status and information about the advancement
        """
        if not self.current:
            return {
                'status': 'error',
                'message': 'No current behavior set'
            }
        
        # Try to advance within current behavior
        current_behavior = self.current
        next_action_result = current_behavior.actions.advance()
        
        if next_action_result['status'] == 'success':
            return next_action_result
        
        # If at end of behavior, try to advance to next behavior
        next_behavior = self.next()
        if next_behavior:
            self._current_index += 1
            self.save_state()
            # Navigate to first action of next behavior
            if next_behavior.actions._actions:
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
    
    def go_back(self) -> Dict[str, Any]:
        """Go back to the previous action in the current behavior, or previous behavior if at start.
        
        Returns:
            Dict with status and information about going back
        """
        if not self.current:
            return {
                'status': 'error',
                'message': 'No current behavior set'
            }
        
        # Try to go back within current behavior
        current_behavior = self.current
        back_result = current_behavior.actions.go_back()
        
        if back_result['status'] == 'success':
            return back_result
        
        # If at start of behavior actions, check if we can go to previous behavior
        # If no previous behavior, return the actions error message  
        prev_behavior = self.previous()
        if prev_behavior:
            self._current_index -= 1
            self.save_state()
            # Navigate to last action of previous behavior
            if prev_behavior.actions._actions:
                last_action_name = prev_behavior.actions.names[-1]
                prev_behavior.actions.navigate_to(last_action_name)
            return {
                'status': 'success',
                'message': f'Went back to behavior: {prev_behavior.name}',
                'behavior': prev_behavior.name,
                'action': prev_behavior.actions.current.action_name if prev_behavior.actions.current else None
            }
        
        # No previous behavior - return the action's error message
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
        
        target_index = None
        for i, b in enumerate(self._behaviors):
            if b.name == behavior.name:
                target_index = i
                self._current_index = i
                break
        
        # When navigating to a behavior: mark all actions in previous behaviors as complete,
        # clear all actions in future behaviors
        if target_index is not None and self.bot_paths:
            workspace_dir = self.bot_paths.workspace_directory
            state_file = workspace_dir / 'behavior_action_state.json'
            
            import json
            if state_file.exists():
                state_data = json.loads(state_file.read_text(encoding='utf-8'))
            else:
                state_data = {}
            
            completed_actions = state_data.get('completed_actions', [])
            
            # Mark all actions in previous behaviors as complete
            for i in range(target_index):
                past_behavior = self._behaviors[i]
                for action_name in past_behavior.actions.names:
                    action_state = f"{self.bot_name}.{past_behavior.name}.{action_name}"
                    # Check if already completed
                    is_completed = any(a.get('action_state') == action_state for a in completed_actions if isinstance(a, dict))
                    if not is_completed:
                        from datetime import datetime
                        completed_actions.append({
                            'action_state': action_state,
                            'timestamp': datetime.now().isoformat()
                        })
            
            # Remove completed actions from future behaviors
            actions_to_remove = set()
            for i in range(target_index + 1, len(self._behaviors)):
                future_behavior = self._behaviors[i]
                for action_name in future_behavior.actions.names:
                    action_state = f"{self.bot_name}.{future_behavior.name}.{action_name}"
                    actions_to_remove.add(action_state)
            
            state_data['completed_actions'] = [
                action for action in completed_actions 
                if isinstance(action, dict) and action.get('action_state') not in actions_to_remove
            ]
            state_file.parent.mkdir(parents=True, exist_ok=True)
            state_file.write_text(json.dumps(state_data, indent=2), encoding='utf-8')
        
        # Persist current_behavior and current_action to state file
        self.save_state()

    def close_current(self):
        if self._current_index is not None:
            next_behavior = self.next()
            if next_behavior:
                self._current_index += 1
                self.save_state()

    def _inject_next_behavior_reminder(self, result: dict, action_name: str=None) -> dict:
        if not self._is_final_behavior():
            return result
        if action_name and self.current:
            action_names = self.current.actions.names
            if action_names and action_name != action_names[-1]:
                return result
        reminder = self._get_next_behavior_reminder()
        if not reminder:
            return result
        return inject_reminder_to_instructions(result, reminder)

    def _is_final_behavior(self) -> bool:
        try:
            if self.current is None:
                return False
            if self.names and self.current.name == self.names[-1]:
                return True
        except Exception as e:
            logger.debug(f'Failed to check if behavior is final: {e}')
            raise
        return False

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
                state_data = json.loads(state_file.read_text(encoding='utf-8'))
            except Exception as e:
                logger.debug(f'Failed to load state file {state_file}: {e}')
                raise
        state_data['current_behavior'] = f'{self.bot_name}.{self.current.name}'
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
                    return
            self._init_to_first_behavior()
        except Exception:
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

    def get_entry_state_result(self) -> 'BotResult':
        from .bot import BotResult
        return BotResult(status='requires_confirmation', behavior='', action='', data={'message': f"**ENTRY STATE**\n\nNo behavior state found. Please select a behavior to start:\n\n{chr(10).join((f'- {b}' for b in self.names))}\n\nProvide 'confirmed_behavior' in parameters to proceed.", 'behaviors': self.names, 'requires_confirmation': True})

    def does_requested_match_current(self, requested_behavior: str) -> Tuple[bool, Optional[str], Optional[str]]:
        if not self.current:
            return (True, None, None)
        current_behavior = self.current.name
        requested_behavior_obj = self.find_by_name(requested_behavior)
        requested_matched = requested_behavior_obj.name if requested_behavior_obj else None
        next_behavior_obj = self.next()
        expected_next = next_behavior_obj.name if next_behavior_obj else None
        # Match if: valid behavior requested AND (staying in current OR at workflow end OR requesting next)
        matches = (
            requested_matched is not None
            and (
                requested_matched == current_behavior
                or expected_next is None
                or requested_matched == expected_next
            )
        )
        logger.debug(f'Behavior order check: requested={requested_behavior} ({requested_matched}), current={current_behavior}, expected_next={expected_next}, matches={matches}')
        return (matches, current_behavior, expected_next)