"""Base scanner for JavaScript test file validation."""

from typing import List, Dict, Any, Optional, Tuple, TYPE_CHECKING
from pathlib import Path
from scanners.scanner import Scanner
from scanners.violation import Violation
from scanners.code.javascript.js_code_scanner import JSCodeScanner

if TYPE_CHECKING:
    from scanners.resources.scan_context import ScanFilesContext, FileScanContext, CrossFileScanContext
    from actions.rules.rule import Rule


class JSTestScanner(JSCodeScanner):
    """Base class for JavaScript test file scanners.
    
    Inherits JavaScript parsing capabilities from JSCodeScanner.
    """
    
    def __init__(self, rule: 'Rule'):
        super().__init__(rule)
    
    def _empty_violation_list(self) -> List[Dict[str, Any]]:
        return []
    
    def scan_file_with_context(self, context: 'FileScanContext') -> List[Dict[str, Any]]:
        if not context.exists:
            return self._empty_violation_list()
        return self._empty_violation_list()
    
    def _parse_test_file(self, test_file_path: Path) -> Optional[Tuple[str, Dict]]:
        """Parse a JavaScript test file and return (content, AST)."""
        if not test_file_path.exists():
            return None
        
        try:
            content = test_file_path.read_text(encoding='utf-8')
            ast = self._parse_js_with_esprima(content, str(test_file_path))
            
            if ast is None:
                return None
            
            return (content, ast)
        except UnicodeDecodeError:
            return None
    
    def _get_all_test_files_parsed(
        self, 
        test_files: Optional[List[Path]]
    ) -> List[Tuple[Path, str, Dict]]:
        """Parse all test files and return list of (path, content, AST) tuples."""
        parsed_files = []
        if test_files:
            for test_file_path in test_files:
                parsed = self._parse_test_file(test_file_path)
                if parsed:
                    content, ast = parsed
                    parsed_files.append((test_file_path, content, ast))
        return parsed_files
