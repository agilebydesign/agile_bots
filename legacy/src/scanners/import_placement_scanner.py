"""Scanner for validating import statements are at the top of files."""

from typing import List, Dict, Any, Optional
from pathlib import Path
import ast
import re
import logging
from .code_scanner import CodeScanner
from .violation import Violation

logger = logging.getLogger(__name__)


class ImportPlacementScanner(CodeScanner):
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, knowledge_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        # Find the end of the import section (after docstrings/comments)
        import_section_end = self._find_import_section_end(lines)
        
        # Find all import statements and check if they're in the import section
        violations.extend(self._check_import_placement(lines, import_section_end, file_path, rule_obj))
        
        return violations
    
    def _find_import_section_end(self, lines: List[str]) -> int:
        import_section_end = 0
        
        # Skip leading blank lines
        while import_section_end < len(lines) and not lines[import_section_end].strip():
            import_section_end += 1
        
        # Skip module docstring (triple-quoted string)
        if import_section_end < len(lines):
            line = lines[import_section_end].strip()
            if line.startswith('"""') or line.startswith("'''"):
                # Find end of docstring
                quote_char = line[:3]
                import_section_end += 1
                while import_section_end < len(lines):
                    if quote_char in lines[import_section_end]:
                        import_section_end += 1
                        break
                    import_section_end += 1
        
        in_multiline_import = False
        # Skip blank lines, comments, imports, TYPE_CHECKING blocks, and try/except ImportError blocks after docstring
        while import_section_end < len(lines):
            line = lines[import_section_end].strip()
            if not line or line.startswith('#'):
                import_section_end += 1
            elif self._is_import_statement(line):
                # Check if this is a multi-line import (has opening paren without closing)
                if '(' in line and ')' not in line:
                    in_multiline_import = True
                import_section_end += 1
            elif in_multiline_import:
                # We're inside a multi-line import, keep going until we find the closing paren
                if ')' in line:
                    in_multiline_import = False
                import_section_end += 1
            elif self._is_type_checking_block_start(line):
                # Skip through the entire TYPE_CHECKING block
                import_section_end = self._skip_type_checking_block(lines, import_section_end)
            elif self._is_try_import_error_block_start(line):
                # Skip through the entire try/except ImportError block
                import_section_end = self._skip_try_import_error_block(lines, import_section_end)
            else:
                # Found non-import, non-comment, non-blank line - import section ends here
                break
        
        return import_section_end
    
    def _is_type_checking_block_start(self, line: str) -> bool:
        stripped = line.strip()
        # Match 'if TYPE_CHECKING:' pattern (may have comments after colon)
        return stripped.startswith('if TYPE_CHECKING:')
    
    def _skip_type_checking_block(self, lines: List[str], start_line: int) -> int:
        if start_line >= len(lines):
            return start_line
        
        type_checking_line = lines[start_line]
        base_indent = len(type_checking_line) - len(type_checking_line.lstrip())
        
        # Start after the 'if TYPE_CHECKING:' line
        current_line = start_line + 1
        
        # Skip through the block (all lines indented more than the 'if' statement)
        while current_line < len(lines):
            line = lines[current_line]
            stripped = line.strip()
            
            # Empty lines are allowed
            if not stripped:
                current_line += 1
                continue
            
            if stripped.startswith('#'):
                current_line += 1
                continue
            
            line_indent = len(line) - len(line.lstrip())
            if line_indent <= base_indent:
                break
            
            # This line is part of the TYPE_CHECKING block
            current_line += 1
        
        return current_line
    
    def _is_try_import_error_block_start(self, line: str) -> bool:
        stripped = line.strip()
        return stripped == 'try:' or stripped.startswith('try:')
    
    def _skip_try_import_error_block(self, lines: List[str], start_line: int) -> int:
        if start_line >= len(lines):
            return start_line
        
        try_line = lines[start_line]
        base_indent = len(try_line) - len(try_line.lstrip())
        
        # Start after the 'try:' line
        current_line = start_line + 1
        
        # Skip through the try block (all lines indented more than the 'try' statement)
        while current_line < len(lines):
            line = lines[current_line]
            stripped = line.strip()
            
            # Empty lines are allowed
            if not stripped:
                current_line += 1
                continue
            
            if stripped.startswith('#'):
                current_line += 1
                continue
            
            line_indent = len(line) - len(line.lstrip())
            if line_indent == base_indent:
                if stripped.startswith('except ImportError:') or stripped.startswith('except ImportError'):
                    # Skip through the except block too
                    current_line += 1
                    while current_line < len(lines):
                        except_line = lines[current_line]
                        except_stripped = except_line.strip()
                        except_indent = len(except_line) - len(except_line.lstrip())
                        
                        # Empty lines and comments in except block are allowed
                        if not except_stripped or except_stripped.startswith('#'):
                            current_line += 1
                            continue
                        
                        # If we're back to base indentation or less, except block is done
                        if except_indent <= base_indent:
                            break
                        
                        current_line += 1
                    break
                else:
                    # Not an except ImportError, block has ended
                    break
            
            # This line is part of the try block
            current_line += 1
        
        return current_line
    
    def _is_import_statement(self, line: str) -> bool:
        stripped = line.strip()
        
        # Must start with 'import ' or 'from ' (not just contain these words)
        if not (stripped.startswith('import ') or stripped.startswith('from ')):
            return False
        
        # For 'from X import Y' statements, must have ' import ' in the line
        if stripped.startswith('from '):
            return ' import ' in stripped
        
        # For 'import X' statements, must be at the start
        return stripped.startswith('import ')
    
    def _check_import_placement(
        self, 
        lines: List[str], 
        import_section_end: int,
        file_path: Path, 
        rule_obj: Any
    ) -> List[Dict[str, Any]]:
        violations = []
        content = '\n'.join(lines)
        
        try:
            tree = ast.parse(content, filename=str(file_path))
            import_nodes = self._find_import_nodes(tree)
            import_line_numbers = {node.lineno for node in import_nodes}
            function_def_lines = self._find_function_def_lines(tree)
        except (SyntaxError, Exception) as e:
            logger.debug(f'AST parsing failed for {file_path}, falling back to line-by-line checking: {type(e).__name__}: {e}')
            # If AST parsing fails, fall back to simple line-by-line checking
            import_line_numbers = set()
            function_def_lines = set()
        
        line_num = import_section_end
        while line_num < len(lines):
            line = lines[line_num]
            line_number_1_indexed = line_num + 1
            
            # Skip blank lines and comments
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                line_num += 1
                continue
            
            # Skip TYPE_CHECKING blocks (they're allowed to contain imports)
            if self._is_type_checking_block_start(stripped):
                line_num = self._skip_type_checking_block(lines, line_num)
                continue
            
            # Skip try/except ImportError blocks (they're allowed to contain imports)
            if self._is_try_import_error_block_start(stripped):
                line_num = self._skip_try_import_error_block(lines, line_num)
                continue
            
            is_import = False
            if import_line_numbers and line_number_1_indexed in import_line_numbers:
                # Use AST-detected imports (more accurate)
                is_import = True
            elif self._is_import_statement(line):
                # Fall back to pattern matching
                is_import = True
            
            if is_import:
                if function_def_lines and self._is_inside_function(line_number_1_indexed, function_def_lines, lines):
                    # Import inside function is allowed - skip it
                    line_num += 1
                    continue
                
                # Found import after import section - violation!
                violation = self._create_violation_with_snippet(
                    rule_obj=rule_obj,
                    violation_message='Import statement found after non-import code. Move all imports to the top of the file.',
                    file_path=file_path,
                    line_number=line_number_1_indexed,
                    severity='error',
                    content=content,
                    start_line=line_number_1_indexed
                )
                violations.append(violation)
            
            line_num += 1
        
        return violations
    
    def _find_import_nodes(self, tree: ast.AST) -> List[ast.stmt]:
        import_nodes = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                import_nodes.append(node)
        return import_nodes
    
    def _find_function_def_lines(self, tree: ast.AST) -> Dict[int, int]:
        function_ranges = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Get the end line of the function (approximate by finding the next def/class at same level)
                start_line = node.lineno
                end_line = self._find_function_end_line(node, tree)
                function_ranges[start_line] = end_line
        return function_ranges
    
    def _find_function_end_line(self, func_node: ast.FunctionDef, tree: ast.AST) -> int:
        if hasattr(func_node, 'end_lineno') and func_node.end_lineno:
            return func_node.end_lineno
        
        if func_node.body:
            last_stmt = func_node.body[-1]
            if hasattr(last_stmt, 'end_lineno') and last_stmt.end_lineno:
                return last_stmt.end_lineno
        
        logger.debug(f'Function node missing end_lineno at line {func_node.lineno}')
        return func_node.lineno
    
    def _is_inside_function(self, line_number: int, function_ranges: Dict[int, int], lines: List[str]) -> bool:
        for func_start, func_end in function_ranges.items():
            if func_start <= line_number <= func_end:
                return True
        return False













