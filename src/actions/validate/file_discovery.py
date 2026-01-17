import logging
from pathlib import Path
from typing import List, Optional
from bot_path import BotPath

class FileDiscovery:
    EXCLUDED_FILES = {'__init__.py'}

    def __init__(self, bot_paths: Optional[BotPath]=None, behavior_name: Optional[str]=None, exclude_patterns: List[str]=None):
        self.bot_paths = bot_paths
        self.behavior_name = behavior_name
        self.exclude_patterns = exclude_patterns or []

    def should_include_file(self, file_path: Path) -> bool:
        if file_path.name in self.EXCLUDED_FILES:
            return False
        if not self.exclude_patterns:
            return True
        return not self._matches_any_exclude_pattern(file_path)

    def _matches_any_exclude_pattern(self, file_path: Path) -> bool:
        file_path_str = str(file_path).replace('\\', '/')
        file_relative_str = self._get_relative_path_str(file_path)
        for pattern in self.exclude_patterns:
            if self._matches_exclude_pattern(file_path, file_path_str, file_relative_str, pattern):
                return True
        return False

    def _get_relative_path_str(self, file_path: Path) -> Optional[str]:
        if not (file_path.is_absolute() and self.bot_paths and self.bot_paths.workspace_directory):
            return None
        try:
            return str(file_path.relative_to(self.bot_paths.workspace_directory)).replace('\\', '/')
        except ValueError as e:
            logging.getLogger(__name__).debug(f'File not relative to workspace: {e}')
            raise

    def _matches_exclude_pattern(self, file_path: Path, file_path_str: str, file_relative_str: Optional[str], pattern: str) -> bool:
        pattern_normalized = pattern.replace('\\', '/')
        if pattern_normalized in file_path_str:
            return True
        if file_relative_str and pattern_normalized in file_relative_str:
            return True
        if self._matches_folder_pattern(file_path, pattern):
            return True
        return False

    def _matches_folder_pattern(self, file_path: Path, pattern: str) -> bool:
        pattern_path = Path(pattern)
        if pattern_path.exists() and pattern_path.is_dir():
            if self._is_file_in_folder(file_path, str(pattern_path)):
                return True
        if not pattern_path.is_absolute() and self.bot_paths and self.bot_paths.workspace_directory:
            resolved = self.bot_paths.workspace_directory / pattern_path
            if resolved.exists() and resolved.is_dir() and self._is_file_in_folder(file_path, str(resolved)):
                return True
        return False

    def _is_file_in_folder(self, file_path: Path, folder_pattern: str) -> bool:
        try:
            folder_path = Path(folder_pattern)
            if not (folder_path.is_absolute() or file_path.is_absolute()):
                return False
            return self._check_path_relative(file_path, folder_path)
        except Exception:
            return False

    def _check_path_relative(self, file_path: Path, folder_path: Path) -> bool:
        try:
            return file_path.is_relative_to(folder_path)
        except ValueError as e:
            logging.getLogger(__name__).debug(f'Path comparison failed (ValueError): {e}')
            raise

    def expand_directory_to_files(self, dir_path: Path) -> List[Path]:
        abs_dir_path = dir_path.resolve()
        abs_dir_str = str(abs_dir_path).replace('\\', '/')
        result = []
        for f in dir_path.rglob('*.py'):
            if not self.should_include_file(f):
                continue
            f_abs_str = str(f.resolve()).replace('\\', '/')
            if f_abs_str.startswith(abs_dir_str + '/') or f_abs_str == abs_dir_str:
                result.append(f)
        return result

    def discover_files_from_directory(self, dir_name: str) -> List[Path]:
        if not self.bot_paths:
            return []
        search_dir = self.bot_paths.workspace_directory / dir_name
        return self._collect_py_files_in_dir(search_dir)

    def _collect_py_files_in_dir(self, search_dir: Path) -> List[Path]:
        abs_dir_str = str(search_dir.resolve()).replace('\\', '/')
        discovered = []
        for f in search_dir.rglob('*.py'):
            if not self.should_include_file(f):
                continue
            f_abs_str = str(f.resolve()).replace('\\', '/')
            if f_abs_str.startswith(abs_dir_str + '/') or f_abs_str == abs_dir_str:
                discovered.append(f)
        return discovered

    def auto_discover_files(self, key: str) -> List[str]:
        if not self.bot_paths:
            return []
        dir_name = self._behavior_to_directory() if self.behavior_name else key
        search_dir = self.bot_paths.workspace_directory / dir_name
        return [str(f) for f in search_dir.rglob('*.py') if self.should_include_file(f)]

    def _behavior_to_directory(self) -> Optional[str]:
        if not self.behavior_name:
            return None
        if self.behavior_name == 'code':
            return 'src'
        return self.behavior_name