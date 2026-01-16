import re
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from urllib.parse import quote
from ...bot_path import BotPath
logger = logging.getLogger(__name__)

class ValidationReportFormatter:

    def __init__(self, workspace_directory: Path):
        self.workspace_directory = workspace_directory

    def format_violation_line(self, violation: Dict[str, Any], create_file_link_fn, extract_test_info_fn, format_violation_message_fn) -> List[str]:
        location = violation.get('location', 'unknown')
        message = violation.get('violation_message', 'No message')
        severity = violation.get('severity', 'error')
        line_number = violation.get('line_number')
        severity_icon = '<span style="color: red;">[X]</span>' if severity == 'error' else '<span style="color: orange;">[!]</span>' if severity == 'warning' else '<span style="color: blue;">[i]</span>'
        location_link = create_file_link_fn(location, line_number)
        test_info = extract_test_info_fn(message, location, line_number)
        formatted_message = format_violation_message_fn(message)
        if test_info:
            return [f'- {severity_icon} **{severity.upper()}** - {location_link}: {test_info}']
        if '\n' not in formatted_message:
            return [f'- {severity_icon} **{severity.upper()}** - {location_link}: {formatted_message}']
        parts = formatted_message.split('\n')
        first_line = parts[0] if parts else formatted_message
        lines = [f'- {severity_icon} **{severity.upper()}** - {location_link}: {first_line}']
        lines.extend(self._format_multiline_message_parts(parts[1:]))
        return lines

    def _format_multiline_message_parts(self, remaining_parts: List[str]) -> List[str]:
        result = []
        in_code_block = False
        for part in remaining_parts:
            formatted = self._format_message_part(part, in_code_block)
            if part.strip().startswith('```'):
                in_code_block = not in_code_block
            result.append(formatted)
        return result

    def _format_message_part(self, part: str, in_code_block: bool) -> str:
        if part.strip().startswith('```') or in_code_block:
            return f'    {part}'
        if part.strip() == '':
            return ''
        return f'  {part}'

    def format_violation_message(self, message: str) -> str:
        return message

    def extract_test_info(self, message: str, location: str, line_number: Optional[int], get_file_uri_fn) -> Optional[str]:
        test_method_match = self._find_test_method_match(message)
        test_class_match = self._find_test_class_match(message)
        if not test_method_match and (not test_class_match):
            return None
        file_uri = get_file_uri_fn(location, line_number)
        try:
            message = self._replace_test_method_refs(message, test_method_match, file_uri)
            message = self._replace_test_class_refs(message, test_class_match, file_uri)
            return message
        except Exception as e:
            logger.warning(f'Failed to create test info links: {e}')
            return None

    def _find_test_method_match(self, message: str):
        patterns = ['Test\\s+method\\s+["\\\']([^"\\\']+)["\\\']', 'Test\\s+["\\\']([^"\\\']+)["\\\']', 'test\\s+method\\s+["\\\']([^"\\\']+)["\\\']']
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match
        return None

    def _find_test_class_match(self, message: str):
        patterns = ['Test\\s+class\\s+["\\\']([^"\\\']+)["\\\']', 'class\\s+["\\\']([^"\\\']+)["\\\']']
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match
        return None

    def _replace_test_method_refs(self, message: str, match, file_uri: str) -> str:
        if not match:
            return message
        name = match.group(1)
        replacement = f'Test method [{name}]({file_uri})'
        for old in [f'Test method "{name}"', f"Test method '{name}'", f'Test "{name}"', f"Test '{name}'", f'test method "{name}"', f"test method '{name}'"]:
            message = message.replace(old, replacement)
        return message

    def _replace_test_class_refs(self, message: str, match, file_uri: str) -> str:
        if not match:
            return message
        name = match.group(1)
        replacement = f'Test class [{name}]({file_uri})'
        for old in [f'Test class "{name}"', f"Test class '{name}'", f'class "{name}"', f"class '{name}'"]:
            message = message.replace(old, replacement)
        return message

    def create_file_link(self, location: str, line_number: Optional[int], get_file_uri_fn, get_relative_path_fn) -> str:
        if location == 'unknown' or not location:
            return f'`{location}`'
        try:
            return self._create_link_for_path(location, line_number, get_file_uri_fn, get_relative_path_fn)
        except Exception as e:
            logger.debug(f'Failed to create file link for {location}: {e}')
            return self._create_fallback_link(location, line_number, get_file_uri_fn)

    def _create_link_for_path(self, location: str, line_number: Optional[int], get_file_uri_fn, get_relative_path_fn) -> str:
        file_path = Path(location)
        is_absolute = file_path.is_absolute() or (len(location) > 1 and location[1] == ':') or location.startswith('\\\\')
        if not is_absolute:
            return f'[`{location}`]({get_file_uri_fn(location, line_number)})'
        if self.workspace_directory:
            try:
                rel_path = get_relative_path_fn(file_path)
                return f'[`{rel_path}`]({get_file_uri_fn(location, line_number)})'
            except ValueError as e:
                logger.debug(f'Could not get relative path for {file_path}: {e}')
        return f'[`{Path(location).name}`]({get_file_uri_fn(location, line_number)})'

    def _create_fallback_link(self, location: str, line_number: Optional[int], get_file_uri_fn) -> str:
        try:
            file_uri = get_file_uri_fn(location, line_number)
            return f'[`{(Path(location).name if location else location)}`]({file_uri})'
        except Exception as e:
            logger.debug(f'Failed to create fallback link for {location}: {e}')
            return f'`{location}:{line_number}`' if line_number else f'`{location}`'

    def get_file_uri(self, location: str, line_number: Optional[int]=None) -> str:
        try:
            resolved_path = self._resolve_file_path(location)
            return self._build_vscode_uri(str(resolved_path), line_number)
        except Exception as e:
            logger.debug(f'Failed to resolve file path for {location}: {e}')
            return self._build_vscode_uri(location, line_number)

    def _resolve_file_path(self, location: str) -> Path:
        file_path = Path(location)
        if file_path.is_absolute():
            return file_path.resolve() if file_path.exists() else file_path
        if self.workspace_directory:
            return (self.workspace_directory / file_path).resolve()
        return Path(location)

    def _build_vscode_uri(self, file_str: str, line_number: Optional[int]) -> str:
        file_str = file_str.replace('\\', '/')
        if len(file_str) >= 2 and file_str[1] == ':':
            file_str = file_str[0].upper() + ':' + file_str[2:]
        encoded_path = quote(file_str, safe='/:')
        uri = f'vscode://file/{encoded_path}'
        return f'{uri}:{line_number}' if line_number else uri

    def rule_name_to_anchor(self, rule_name: str) -> str:
        anchor = rule_name.replace('_', '-').lower()
        return f'#{anchor}'

    def get_relative_path(self, file_path: Path) -> str:
        try:
            if file_path.is_absolute() and self.workspace_directory:
                return str(file_path.relative_to(self.workspace_directory))
            if self.workspace_directory and (not file_path.is_absolute()):
                return self._get_relative_path_for_relative_file(file_path)
            return file_path.name
        except (ValueError, AttributeError) as e:
            logger.warning(f'Could not create relative path for {file_path}: {e}')
            return file_path.name

    def _get_relative_path_for_relative_file(self, file_path: Path) -> str:
        try:
            resolved = (self.workspace_directory / file_path).resolve()
            return str(resolved.relative_to(self.workspace_directory))
        except (ValueError, AttributeError) as e:
            logger.debug(f'Could not get relative path for relative file {file_path}: {e}')
            return file_path.name