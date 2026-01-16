import logging
import fnmatch
from pathlib import Path
from typing import Dict, List, Optional

class RuleFilter:

    def __init__(self, bot_paths=None):
        self.bot_paths = bot_paths

    def filter_files(self, files: Dict[str, List[Path]], exclude_patterns: Optional[List[str]]=None) -> Dict[str, List[Path]]:
        if not exclude_patterns:
            return files
        filtered_files = {'test': [], 'src': []}
        all_files = self._collect_all_files(files)
        excluded_count = 0
        for file_type, file_path in all_files:
            if self._should_exclude_file(file_path, exclude_patterns):
                excluded_count += 1
            else:
                filtered_files[file_type].append(file_path)
        if excluded_count > 0:
            logging.getLogger(__name__).info(f'Excluded {excluded_count} files based on exclude patterns')
        return filtered_files

    def _collect_all_files(self, files: Dict[str, List[Path]]) -> List[tuple]:
        all_files = []
        if 'test' in files:
            all_files.extend([('test', f) for f in files['test']])
        if 'src' in files:
            all_files.extend([('src', f) for f in files['src']])
        return all_files

    def _should_exclude_file(self, file_path: Path, exclude_patterns: List[str]) -> bool:
        file_path_str = str(file_path).replace('\\', '/')
        file_relative_str = self._get_relative_path_str(file_path)
        for pattern in exclude_patterns:
            if self._matches_pattern(file_path, file_path_str, file_relative_str, pattern):
                return True
        return False

    def _get_relative_path_str(self, file_path: Path) -> Optional[str]:
        if not (file_path.is_absolute() and self.bot_paths and self.bot_paths.workspace_directory):
            return None
        try:
            return str(file_path.relative_to(self.bot_paths.workspace_directory)).replace('\\', '/')
        except ValueError:
            return None

    def _matches_pattern(self, file_path: Path, file_path_str: str, file_relative_str: Optional[str], pattern: str) -> bool:
        pattern_normalized = pattern.replace('\\', '/')
        if ':' in pattern:
            return self._matches_folder_include_pattern(file_path, pattern)
        if self._matches_path_pattern(file_path_str, file_relative_str, pattern_normalized):
            return True
        if self._matches_folder_pattern(file_path, pattern):
            return True
        if fnmatch.fnmatch(file_path_str, pattern) or fnmatch.fnmatch(file_path.name, pattern):
            return True
        return False

    def _matches_folder_include_pattern(self, file_path: Path, pattern: str) -> bool:
        folder_pattern, include_pattern = pattern.split(':', 1)
        return self._is_file_in_folder(file_path, folder_pattern) and (not fnmatch.fnmatch(file_path.name, include_pattern))

    def _matches_path_pattern(self, file_path_str: str, file_relative_str: Optional[str], pattern: str) -> bool:
        return pattern in file_path_str or (file_relative_str and pattern in file_relative_str)

    def _matches_folder_pattern(self, file_path: Path, pattern: str) -> bool:
        pattern_path = Path(pattern)
        if pattern_path.exists() and pattern_path.is_dir() and self._is_file_in_folder(file_path, str(pattern_path)):
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
        except Exception as e:
            logging.getLogger(__name__).debug(f'Path check failed: {e}')
            return False

    def _check_path_relative(self, file_path: Path, folder_path: Path) -> bool:
        try:
            return file_path.is_relative_to(folder_path)
        except ValueError as e:
            logging.getLogger(__name__).debug(f'Path comparison failed (ValueError): {e}')
            raise

