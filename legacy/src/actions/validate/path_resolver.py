import os
from pathlib import Path
from typing import Optional, List
from ...bot.bot_paths import BotPaths

class PathResolver:

    def __init__(self, bot_paths: Optional[BotPaths]=None):
        self.bot_paths = bot_paths
        self._repo_root: Optional[Path] = None
        if self.bot_paths:
            self._repo_root = self._find_repo_root()

    def resolve_path(self, file_path: Path) -> Path:
        if file_path.is_absolute():
            return file_path
        if self._repo_root:
            return self._resolve_with_repo_root(file_path)
        return self._resolve_with_workspace_or_cwd(file_path)

    def _resolve_with_repo_root(self, file_path: Path) -> Path:
        candidate = self._repo_root / file_path
        if candidate.exists():
            return candidate
        workspace_candidate = self._try_workspace_path(file_path)
        return workspace_candidate if workspace_candidate else candidate

    def _resolve_with_workspace_or_cwd(self, file_path: Path) -> Path:
        if self.bot_paths and self.bot_paths.workspace_directory:
            return self.bot_paths.workspace_directory / file_path
        return Path(os.getcwd()) / file_path

    def _try_workspace_path(self, file_path: Path) -> Optional[Path]:
        if not (self.bot_paths and self.bot_paths.workspace_directory):
            return None
        candidate = self.bot_paths.workspace_directory / file_path
        return candidate if candidate.exists() else None

    def expand_path_if_needed(self, file_path: Path, expand_fn) -> List[Path]:
        path_str = str(file_path)
        
        if '*' in path_str or '?' in path_str:
            base_path = self._repo_root if self._repo_root else (self.bot_paths.workspace_directory if self.bot_paths else Path.cwd())
            matched_paths = list(base_path.glob(path_str))
            return [p for p in matched_paths if p.is_file()]
        
        if file_path.exists() and file_path.is_dir():
            return expand_fn(file_path)
        elif file_path.exists() and file_path.is_file():
            return [file_path]
        else:
            return [file_path]

    def _find_repo_root(self) -> Optional[Path]:
        if not self.bot_paths:
            return None
        workspace_path = self.bot_paths.workspace_directory
        current = workspace_path.resolve()
        for i in range(10):
            if (current / '.git').exists():
                return current
            if current.parent == current:
                break
            current = current.parent
        return None