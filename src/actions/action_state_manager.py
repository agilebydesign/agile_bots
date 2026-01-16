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
        import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_path.parent.mkdir(parents=True, exist_ok=True); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:35','message':'load_state entry','data':{'behavior_bot_name':self.behavior.bot_name,'behavior_name':self.behavior.name,'actions_count':len(actions_list),'action_names':[a.action_name for a in actions_list] if actions_list else []},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H3'})+'\n'); log_file.close()
        state_data = self._load_state_data()
        import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:37','message':'after _load_state_data','data':{'state_data_exists':state_data is not None,'current_behavior':state_data.get('current_behavior') if state_data else None,'current_action':state_data.get('current_action') if state_data else None},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H1,H4'})+'\n'); log_file.close()
        if state_data is None:
            import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:38','message':'state_data is None, setting default','data':{},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H1,H4'})+'\n'); log_file.close()
            self._set_default_index(actions_list, current_index_ref)
            return
        is_current = self._is_current_behavior(state_data)
        import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:40','message':'checking current behavior','data':{'is_current_behavior':is_current,'expected':f'{self.behavior.bot_name}.{self.behavior.name}','actual':state_data.get('current_behavior')},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H2'})+'\n'); log_file.close()
        if not is_current:
            import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:41','message':'not current behavior, setting default','data':{},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H2'})+'\n'); log_file.close()
            self._set_default_index(actions_list, current_index_ref)
            return
        if self._try_set_from_current_action(state_data, actions_list, current_index_ref):
            import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:43','message':'set from current_action','data':{'final_index':current_index_ref[0]},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H5'})+'\n'); log_file.close()
            return
        if self._try_set_from_completed_actions(state_data, actions_list, current_index_ref):
            import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:45','message':'set from completed_actions','data':{'final_index':current_index_ref[0]},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H5'})+'\n'); log_file.close()
            return
        import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:47','message':'fallback to default index','data':{},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H5'})+'\n'); log_file.close()
        self._set_default_index(actions_list, current_index_ref)

    def _load_state_data(self) -> Optional[dict]:
        state_file = self.behavior.bot_paths.workspace_directory / 'behavior_action_state.json'
        import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_path.parent.mkdir(parents=True, exist_ok=True); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:49','message':'_load_state_data entry','data':{'state_file_path':str(state_file),'file_exists':state_file.exists(),'workspace_dir':str(self.behavior.bot_paths.workspace_directory)},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H1'})+'\n'); log_file.close()
        if not state_file.exists():
            return None
        try:
            data = json.loads(state_file.read_text(encoding='utf-8'))
            import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:54','message':'state file read successfully','data':{'current_behavior':data.get('current_behavior'),'current_action':data.get('current_action')},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H1'})+'\n'); log_file.close()
            return data
        except Exception as e:
            import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:56','message':'error reading state file','data':{'error':str(e)},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H1'})+'\n'); log_file.close()
            return None

    def _is_current_behavior(self, state_data: dict) -> bool:
        expected = f'{self.behavior.bot_name}.{self.behavior.name}'
        return state_data.get('current_behavior', '') == expected

    def _set_default_index(self, actions_list: List, current_index_ref: list) -> None:
        if actions_list:
            current_index_ref[0] = 0

    def _try_set_from_current_action(self, state_data: dict, actions_list: List, current_index_ref: list) -> bool:
        current_action_full = state_data.get('current_action', '')
        import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_path.parent.mkdir(parents=True, exist_ok=True); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:66','message':'_try_set_from_current_action entry','data':{'current_action_full':current_action_full,'actions_count':len(actions_list),'action_names':[a.action_name for a in actions_list] if actions_list else []},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H3,H5'})+'\n'); log_file.close()
        if not current_action_full:
            return False
        parts = current_action_full.split('.')
        if len(parts) < 3:
            import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:71','message':'invalid current_action format','data':{'parts':parts},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H5'})+'\n'); log_file.close()
            return False
        action_name = parts[-1]
        import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:73','message':'extracted action name','data':{'action_name':action_name,'parts':parts},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H5'})+'\n'); log_file.close()
        for i, action in enumerate(actions_list):
            if action.action_name == action_name:
                current_index_ref[0] = i
                import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:76','message':'matched action, set index','data':{'action_name':action_name,'index':i},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H5'})+'\n'); log_file.close()
                return True
        import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:78','message':'action name not found in list','data':{'action_name':action_name,'available_names':[a.action_name for a in actions_list]},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H3,H5'})+'\n'); log_file.close()
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