import os
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, TYPE_CHECKING
from bot_path import BotPath
from scope.action_scope import ActionScope
from actions.validate.file_discovery import FileDiscovery
from bot_path.path_resolver import PathResolver

if TYPE_CHECKING:
    from action_context import ValidateActionContext

class ValidationScope(ActionScope):
    EXCLUDED_FILES = {'__init__.py'}

    def __init__(self, parameters: Dict[str, Any], bot_paths: Optional[BotPath]=None, behavior_name: Optional[str]=None):
        self._behavior_name = behavior_name
        exclude_patterns = []
        if 'scope' in parameters and isinstance(parameters.get('scope'), dict):
            exclude_patterns = parameters['scope'].get('exclude', [])
        if isinstance(exclude_patterns, str):
            exclude_patterns = [exclude_patterns]
        self._file_discovery = FileDiscovery(bot_paths, behavior_name, exclude_patterns)
        self._path_resolver = PathResolver(bot_paths)
        super().__init__(parameters, bot_paths)
        self._extract_skiprule_from_scope()
    
    @classmethod
    def from_context(cls, context: 'ValidateActionContext', bot_paths: Optional[BotPath] = None, behavior_name: Optional[str] = None) -> 'ValidationScope':
        params = {}
        if context.scope:
            params['scope'] = context.scope.to_dict()
        skip_cross_file = getattr(context, 'skip_cross_file', False)
        if skip_cross_file:
            params['skip_cross_file'] = skip_cross_file
        all_files = getattr(context, 'all_files', False)
        if all_files:
            params['all_files'] = all_files
        
        return cls(params, bot_paths, behavior_name)
    
    def _extract_skiprule_from_scope(self) -> None:
        skiprule = []
        if 'scope' in self._parameters and isinstance(self._parameters.get('scope'), dict):
            skiprule = self._parameters['scope'].get('skiprule', [])
        if isinstance(skiprule, str):
            skiprule = [skiprule]
        if skiprule:
            self._parameters['skiprule'] = skiprule

    def _expand_directory_to_files(self, dir_path: Path) -> List[Path]:
        return self._file_discovery.expand_directory_to_files(dir_path)

    def _behavior_to_directory(self) -> Optional[str]:
        if not self._behavior_name:
            return None
        if self._behavior_name == 'code':
            return 'src'
        return self._behavior_name

    def _build_scope(self):
        super()._build_scope()
        for key, value in self._parameters.items():
            if value is None or key == 'scope':
                continue
            if key == 'validate_all' and value is True:
                self._scope_config['all'] = True

    def _handle_scope_parameter(self, scope_value: Any) -> None:
        if not isinstance(scope_value, dict):
            return
        
        scope_type = scope_value.get('type')
        scope_val = scope_value.get('value')
        exclude_patterns = scope_value.get('exclude', [])
        skiprule = scope_value.get('skiprule', [])
        
        if exclude_patterns:
            if isinstance(exclude_patterns, str):
                exclude_patterns = [exclude_patterns]
            self._file_discovery = FileDiscovery(self._bot_paths, self._behavior_name, exclude_patterns)
        
        if skiprule:
            if isinstance(skiprule, str):
                skiprule = [skiprule]
            self._parameters['skiprule'] = skiprule
        
        if scope_type == 'files':
            if not isinstance(scope_val, list):
                scope_val = [scope_val]
            file_key = self._get_file_key_for_behavior()
            self._scope_config[file_key] = [str(Path(p)).replace('\\', '/') for p in scope_val]
        else:
            super()._handle_scope_parameter(scope_value)

    def files(self, key: str) -> List[Path]:
        files_list = self._auto_discover_if_needed(key, self._scope_config.get(key, []))
        resolved_paths = []
        for file_path_str in files_list:
            resolved_paths.extend(self._expand_path_if_needed(self._resolve_path(Path(file_path_str))))
        return resolved_paths

    def _auto_discover_if_needed(self, key, files_list):
        has_any_explicit_files = any((k in self._scope_config for k in ['src', 'test']))
        scope_dict = self._parameters.get('scope', {}) if isinstance(self._parameters.get('scope'), dict) else {}
        has_files_scope = scope_dict.get('type') == 'files'
        has_story_scope = scope_dict.get('type') == 'story'
        if not files_list and (not has_any_explicit_files) and (not has_files_scope) and (not has_story_scope) and self._bot_paths:
            discovered = self._auto_discover_files(key)
            if discovered:
                self._scope_config[key] = discovered
                return discovered
        return files_list

    def _resolve_path(self, file_path: Path) -> Path:
        return self._path_resolver.resolve_path(file_path)

    def _expand_path_if_needed(self, file_path: Path) -> List[Path]:
        return self._path_resolver.expand_path_if_needed(file_path, self._expand_directory_to_files)

    def all_files(self) -> Dict[str, List[Path]]:
        scope_dict = self._parameters.get('scope', {}) if isinstance(self._parameters.get('scope'), dict) else {}
        has_story_scope = scope_dict.get('type') == 'story'
        if has_story_scope:
            return {}
        
        if self._behavior_name:
            return self._handle_behavior_specific_files({})
        return self._handle_general_file_discovery({})

    def _handle_behavior_specific_files(self, all_files_dict):
        behavior_dir = self._behavior_to_directory()
        if not behavior_dir:
            return all_files_dict
        file_key = self._get_file_key_for_behavior()
        has_explicit_files = file_key in self._scope_config or behavior_dir in self._scope_config
        has_any_explicit_params = any((k in self._scope_config for k in ['src', 'test']))
        scope_dict = self._parameters.get('scope', {}) if isinstance(self._parameters.get('scope'), dict) else {}
        has_files_scope = scope_dict.get('type') == 'files'
        has_story_scope = scope_dict.get('type') == 'story'
        if not has_explicit_files and (not has_any_explicit_params) and (not has_files_scope) and (not has_story_scope):
            files = self._discover_files_from_directory(behavior_dir)
            if files:
                all_files_dict[file_key] = files
        elif has_explicit_files or has_any_explicit_params or has_files_scope:
            files = self._get_explicit_files_for_behavior(file_key, behavior_dir)
            if files:
                all_files_dict[file_key] = files
        return all_files_dict

    def _get_file_key_for_behavior(self):
        if self._behavior_name in ('tests', 'test'):
            return 'test'
        elif self._behavior_name == 'code':
            return 'src'
        else:
            return 'src'

    def _get_explicit_files_for_behavior(self, file_key, behavior_dir):
        has_files_scope = (self._parameters.get('scope', {}).get('type') == 'files' if isinstance(self._parameters.get('scope'), dict) else False)
        
        if file_key in self._scope_config:
            files = self.files(file_key)
            if files:
                return files
        
        if behavior_dir in self._scope_config:
            files = self.files(behavior_dir)
            if files:
                return files
        
        if has_files_scope:
            alternate_keys = ['test', 'src']
            for alt_key in alternate_keys:
                if alt_key != file_key and alt_key in self._scope_config:
                    files = self.files(alt_key)
                    if files:
                        return files
        
        return []

    def _handle_general_file_discovery(self, all_files_dict):
        has_any_explicit_params = any((k in self._scope_config for k in ['src', 'test']))
        scope_dict = self._parameters.get('scope', {}) if isinstance(self._parameters.get('scope'), dict) else {}
        has_files_scope = scope_dict.get('type') == 'files'
        has_story_scope = scope_dict.get('type') == 'story'
        file_keys = {'test', 'src'}
        if not has_any_explicit_params and not has_files_scope and not has_story_scope:
            self._discover_all_file_keys(file_keys, all_files_dict)
        else:
            self._discover_explicit_file_keys(file_keys, all_files_dict)
        return all_files_dict

    def _discover_all_file_keys(self, file_keys, all_files_dict):
        for key in file_keys:
            files = self.files(key)
            if files:
                all_files_dict[key] = files

    def _discover_explicit_file_keys(self, file_keys, all_files_dict):
        for key in file_keys:
            if key in self._scope_config:
                files = self.files(key)
                if files:
                    all_files_dict[key] = files

    def _discover_files_from_directory(self, dir_name: str) -> List[Path]:
        return self._file_discovery.discover_files_from_directory(dir_name)

    def _auto_discover_files(self, key: str) -> List[str]:
        return self._file_discovery.auto_discover_files(key)