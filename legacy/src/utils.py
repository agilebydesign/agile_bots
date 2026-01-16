from pathlib import Path
import json
import sys
import ast
from typing import Dict, Any, Optional

def read_json_file(file_path: Path) -> Dict[str, Any]:
    if not file_path.exists():
        raise FileNotFoundError(f'File not found: {file_path}')
    return json.loads(file_path.read_text(encoding='utf-8'))

class TerminalFormatter:
    RESET = '\x1b[0m'
    BLACK = '\x1b[30m'
    RED = '\x1b[31m'
    GREEN = '\x1b[32m'
    YELLOW = '\x1b[33m'
    BLUE = '\x1b[34m'
    MAGENTA = '\x1b[35m'
    CYAN = '\x1b[36m'
    WHITE = '\x1b[37m'
    BRIGHT_BLACK = '\x1b[90m'
    BRIGHT_RED = '\x1b[91m'
    BRIGHT_GREEN = '\x1b[92m'
    BRIGHT_YELLOW = '\x1b[93m'
    BRIGHT_BLUE = '\x1b[94m'
    BRIGHT_MAGENTA = '\x1b[95m'
    BRIGHT_CYAN = '\x1b[96m'
    BRIGHT_WHITE = '\x1b[97m'
    BOLD = '\x1b[1m'
    DIM = '\x1b[2m'
    UNDERLINE = '\x1b[4m'

    def __init__(self, enabled: Optional[bool]=None):
        should_enable = enabled if enabled is not None else self._supports_color()
        if not should_enable:
            self._disable_colors()

    @staticmethod
    def _supports_color() -> bool:
        if sys.platform == 'win32':
            return True
        return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

    def _disable_colors(self):
        for attr in dir(self):
            if not attr.startswith('_') and attr.isupper():
                setattr(self, attr, '')

    def format(self, text: str, *styles: str) -> str:
        style_codes = ''.join((getattr(self, style, '') for style in styles))
        return f'{style_codes}{text}{self.RESET}'

    def header(self, text: str) -> str:
        return self.format(text, 'BOLD', 'CYAN')

    def command(self, text: str) -> str:
        return self.format(text, 'BOLD', 'GREEN')

    def label(self, text: str) -> str:
        return self.format(text, 'DIM')

    def success(self, text: str) -> str:
        return self.format(text, 'GREEN')

    def error(self, text: str) -> str:
        return self.format(text, 'RED')

    def warning(self, text: str) -> str:
        return self.format(text, 'YELLOW')

    def info(self, text: str) -> str:
        return self.format(text, 'BLUE')

    def separator(self, char: str='=', length: int=70) -> str:
        return self.format(char * length, 'BRIGHT_BLACK')
_default_formatter = None

def get_formatter(enabled: Optional[bool]=None) -> TerminalFormatter:
    global _default_formatter
    if _default_formatter is None or enabled is not None:
        _default_formatter = TerminalFormatter(enabled=enabled)
    return _default_formatter


# Test Link Builder Functions
# Used by CLI scope display and story document synchronizers

def build_test_file_link(test_file: str, workspace_directory: Path, story_file_path: Optional[Path] = None) -> str:
    """
    Build link to test file.
    
    Args:
        test_file: Name of test file (e.g., 'test_example.py')
        workspace_directory: Path to workspace directory
        story_file_path: Optional path to story markdown file (generates absolute path from workspace root)
    
    Returns:
        Markdown link string like ' | [Test](path/to/test.py)' or empty string if not found
    """
    if not test_file:
        return ""
    try:
        from agile_bot.bots.base_bot.src.bot.workspace import get_python_workspace_root
        workspace_root = get_python_workspace_root()
        test_file_path = workspace_root / 'agile_bot' / 'bots' / 'base_bot' / 'test' / test_file
        if not test_file_path.exists():
            return ""
        
        # If story_file_path provided, use absolute path from workspace root (starts with /)
        # VS Code/Cursor resolves /path as relative to workspace root
        if story_file_path:
            rel_path = test_file_path.relative_to(workspace_root)
            rel_path_str = '/' + str(rel_path).replace('\\', '/')
            return f" | [Test]({rel_path_str})"
        
        rel_path = test_file_path.relative_to(workspace_root)
        rel_path_str = str(rel_path).replace('\\', '/')
        return f" | [Test]({rel_path_str})"
    except (ValueError, AttributeError):
        # Fallback: try relative to workspace_directory
        test_file_path = workspace_directory / 'test' / test_file
        if not test_file_path.exists():
            return ""
        from agile_bot.bots.base_bot.src.actions.validate.file_link_builder import FileLinkBuilder
        link_builder = FileLinkBuilder(workspace_directory)
        file_uri = link_builder.get_file_uri(str(test_file_path))
        return f" | [Test]({file_uri})"


def build_test_class_link(test_file: str, test_class: str, workspace_directory: Path, story_file_path: Optional[Path] = None) -> str:
    """
    Build link to test class with line number.
    
    Args:
        test_file: Name of test file (e.g., 'test_example.py')
        test_class: Name of test class (e.g., 'TestMyFeature')
        workspace_directory: Path to workspace directory
        story_file_path: Optional path to story markdown file (generates absolute path from workspace root)
    
    Returns:
        Markdown link string like ' | [Test](path/to/test.py#L123)' or empty string if not found
    """
    if not test_file or not test_class or test_class == '?':
        return ""
    
    try:
        from agile_bot.bots.base_bot.src.bot.workspace import get_python_workspace_root
        workspace_root = get_python_workspace_root()
        test_file_path = workspace_root / 'agile_bot' / 'bots' / 'base_bot' / 'test' / test_file
        if not test_file_path.exists():
            return ""
        
        # Find line number of test class using AST
        line_number = find_test_class_line(test_file_path, test_class)
        
        # Only create link if we found the line number
        # Don't create link without line number as it may default to line 1
        if not line_number:
            return ""
        
        # If story_file_path provided, use absolute path from workspace root (starts with /)
        # VS Code/Cursor resolves /path as relative to workspace root
        if story_file_path:
            rel_path = test_file_path.relative_to(workspace_root)
            rel_path_str = '/' + str(rel_path).replace('\\', '/')
            return f" | [Test]({rel_path_str}#L{line_number})"
        
        # Use relative path with line number using #L format
        # VS Code/Cursor markdown links use #L123 format for line numbers
        rel_path = test_file_path.relative_to(workspace_root)
        rel_path_str = str(rel_path).replace('\\', '/')
        return f" | [Test]({rel_path_str}#L{line_number})"
    except (ValueError, AttributeError):
        # Fallback: try relative to workspace_directory
        test_file_path = workspace_directory / 'test' / test_file
        if not test_file_path.exists():
            return ""
        
        # Find line number of test class using AST
        line_number = find_test_class_line(test_file_path, test_class)
        
        # Only create link if we found the line number
        # Don't create link without line number as it may default to line 1
        if not line_number:
            return ""
        
        # Use relative path with line number using #L format
        # VS Code/Cursor markdown links use #L123 format for line numbers
        try:
            from agile_bot.bots.base_bot.src.bot.workspace import get_python_workspace_root
            workspace_root = get_python_workspace_root()
            rel_path = test_file_path.relative_to(workspace_root)
            rel_path_str = str(rel_path).replace('\\', '/')
            return f" | [Test]({rel_path_str}#L{line_number})"
        except (ValueError, AttributeError):
            # Fallback: use vscode://file URI if relative path fails
            from agile_bot.bots.base_bot.src.actions.validate.file_link_builder import FileLinkBuilder
            link_builder = FileLinkBuilder(workspace_directory)
            file_uri = link_builder.get_file_uri(str(test_file_path), line_number)
            return f" | [Test]({file_uri})"


def build_test_method_link(test_file: str, test_method: str, workspace_directory: Path, story_file_path: Optional[Path] = None) -> str:
    """
    Build link to test method with line number.
    
    Args:
        test_file: Name of test file (e.g., 'test_example.py')
        test_method: Name of test method (e.g., 'test_my_scenario')
        workspace_directory: Path to workspace directory
        story_file_path: Optional path to story markdown file (generates absolute path from workspace root)
    
    Returns:
        Markdown link string like ' | [Test](path/to/test.py#L456)' or empty string if not found
    """
    if not test_file or not test_method or test_method == '?':
        return ""
    
    try:
        from agile_bot.bots.base_bot.src.bot.workspace import get_python_workspace_root
        workspace_root = get_python_workspace_root()
        test_file_path = workspace_root / 'agile_bot' / 'bots' / 'base_bot' / 'test' / test_file
        if not test_file_path.exists():
            return ""
        
        # Find line number of test method using AST
        line_number = find_test_method_line(test_file_path, test_method)
        
        # Only create link if we found the line number
        # Don't create link without line number as it may default to line 1
        if not line_number:
            return ""
        
        # If story_file_path provided, use absolute path from workspace root (starts with /)
        # VS Code/Cursor resolves /path as relative to workspace root
        if story_file_path:
            rel_path = test_file_path.relative_to(workspace_root)
            rel_path_str = '/' + str(rel_path).replace('\\', '/')
            return f" | [Test]({rel_path_str}#L{line_number})"
        
        # Use relative path with line number using #L format
        # VS Code/Cursor markdown links use #L123 format for line numbers
        rel_path = test_file_path.relative_to(workspace_root)
        rel_path_str = str(rel_path).replace('\\', '/')
        return f" | [Test]({rel_path_str}#L{line_number})"
    except (ValueError, AttributeError):
        # Fallback: try relative to workspace_directory
        test_file_path = workspace_directory / 'test' / test_file
        if not test_file_path.exists():
            return ""
        
        # Find line number of test method using AST
        line_number = find_test_method_line(test_file_path, test_method)
        
        # Only create link if we found the line number
        # Don't create link without line number as it may default to line 1
        if not line_number:
            return ""
        
        # Use relative path with line number using #L format
        # VS Code/Cursor markdown links use #L123 format for line numbers
        try:
            from agile_bot.bots.base_bot.src.bot.workspace import get_python_workspace_root
            workspace_root = get_python_workspace_root()
            rel_path = test_file_path.relative_to(workspace_root)
            rel_path_str = str(rel_path).replace('\\', '/')
            return f" | [Test]({rel_path_str}#L{line_number})"
        except (ValueError, AttributeError):
            # Fallback: use vscode://file URI if relative path fails
            from agile_bot.bots.base_bot.src.actions.validate.file_link_builder import FileLinkBuilder
            link_builder = FileLinkBuilder(workspace_directory)
            file_uri = link_builder.get_file_uri(str(test_file_path), line_number)
            return f" | [Test]({file_uri})"


def find_test_class_line(test_file_path: Path, test_class_name: str) -> Optional[int]:
    """
    Find the line number of a test class definition.
    
    Args:
        test_file_path: Path to test file
        test_class_name: Name of test class
    
    Returns:
        Line number (1-based) or None if not found
    """
    if not test_file_path.exists() or not test_class_name or test_class_name == '?':
        return None
    try:
        content = test_file_path.read_text(encoding='utf-8')
        tree = ast.parse(content, filename=str(test_file_path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == test_class_name:
                # ast.lineno is 1-based, which is correct for markdown links
                return node.lineno
    except SyntaxError:
        # If there's a syntax error, we can't parse the file
        # Return None so we don't create a broken link
        return None
    except Exception:
        # For any other exception, return None
        # Don't create a link if we can't find the class
        return None
    return None


def find_test_method_line(test_file_path: Path, test_method_name: str) -> Optional[int]:
    """
    Find the line number of a test method definition.
    
    Args:
        test_file_path: Path to test file
        test_method_name: Name of test method
    
    Returns:
        Line number (1-based) or None if not found
    """
    if not test_file_path.exists() or not test_method_name or test_method_name == '?':
        return None
    try:
        content = test_file_path.read_text(encoding='utf-8')
        tree = ast.parse(content, filename=str(test_file_path))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == test_method_name:
                # ast.lineno is 1-based, which is correct for markdown links
                return node.lineno
    except SyntaxError:
        # If there's a syntax error, we can't parse the file
        # Return None so we don't create a broken link
        return None
    except Exception:
        # For any other exception, return None
        # Don't create a link if we can't find the method
        return None
    return None