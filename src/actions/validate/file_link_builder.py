import logging
from pathlib import Path
from typing import Optional
from urllib.parse import quote

logger = logging.getLogger(__name__)

class FileLinkBuilder:

    def __init__(self, workspace_directory: Path):
        self.workspace_directory = workspace_directory

    def create_file_link(self, location: str, line_number: Optional[int] = None) -> str:
        if location == 'unknown' or not location:
            return f'`{location}`'
        try:
            return self.create_file_link_for_valid_location(location, line_number)
        except Exception as e:
            logger.debug(f'Failed to create file link for {location}: {e}')
            return self.create_file_link_fallback(location, line_number)

    def create_file_link_for_valid_location(self, location: str, line_number: Optional[int]) -> str:
        file_path = Path(location)
        is_absolute = file_path.is_absolute() or (len(location) > 1 and location[1] == ':') or location.startswith('\\\\')
        if not is_absolute:
            return f'[`{location}`]({self.get_file_uri(location, line_number)})'
        if not self.workspace_directory:
            file_uri = self.get_file_uri(location, line_number)
            return f'[`{Path(location).name}`]({file_uri})'
        return self.create_absolute_file_link(file_path, location, line_number)

    def create_absolute_file_link(self, file_path: Path, location: str, line_number: Optional[int]) -> str:
        try:
            rel_path = file_path.relative_to(self.workspace_directory)
            file_uri = self.get_file_uri(location, line_number)
            return f'[`{rel_path}`]({file_uri})'
        except ValueError as e:
            logger.debug(f'Could not get relative path for absolute file {file_path}: {e}')
            file_uri = self.get_file_uri(location, line_number)
            return f'[`{Path(location).name}`]({file_uri})'

    def create_file_link_fallback(self, location: str, line_number: Optional[int]) -> str:
        try:
            file_uri = self.get_file_uri(location, line_number)
            return f'[`{(Path(location).name if location else location)}`]({file_uri})'
        except Exception as e:
            logger.debug(f'Failed to create fallback link for {location}: {e}')
            if line_number:
                return f'`{location}:{line_number}`'
            return f'`{location}`'

    def get_file_uri(self, location: str, line_number: Optional[int] = None) -> str:
        try:
            resolved_path = self._resolve_file_path(location)
            file_str = self._normalize_path_string(str(resolved_path))
            return self._build_vscode_uri(file_str, line_number)
        except Exception as e:
            logger.debug(f'Failed to resolve file path for {location}: {e}')
            file_str = self._normalize_path_string(location)
            return self._build_vscode_uri(file_str, line_number)

    def _resolve_file_path(self, location: str) -> Path:
        file_path = Path(location)
        if file_path.is_absolute():
            return file_path.resolve() if file_path.exists() else file_path
        if self.workspace_directory:
            return (self.workspace_directory / file_path).resolve()
        return Path(location)

    def _normalize_path_string(self, path_str: str) -> str:
        file_str = path_str.replace('\\', '/')
        if len(file_str) >= 2 and file_str[1] == ':':
            file_str = file_str[0].upper() + ':' + file_str[2:]
        return file_str

    def _build_vscode_uri(self, file_str: str, line_number: Optional[int]) -> str:
        encoded_path = quote(file_str, safe='/:')
        vscode_uri = f'vscode://file/{encoded_path}'
        if line_number:
            vscode_uri = f'{vscode_uri}:{line_number}'
        return vscode_uri

    def get_relative_path(self, file_path: Path) -> str:
        try:
            if file_path.is_absolute() and self.workspace_directory:
                return str(file_path.relative_to(self.workspace_directory))
            if self.workspace_directory and (not file_path.is_absolute()):
                return self.get_relative_path_for_relative_file(file_path)
            return file_path.name
        except (ValueError, AttributeError) as e:
            logger.warning(f'Could not create relative path for {file_path}: {e}')
            return file_path.name

    def get_relative_path_for_relative_file(self, file_path: Path) -> str:
        try:
            resolved = (self.workspace_directory / file_path).resolve()
            return str(resolved.relative_to(self.workspace_directory))
        except (ValueError, AttributeError) as e:
            logger.debug(f'Could not get relative path for relative file {file_path}: {e}')
            return file_path.name

