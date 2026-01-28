
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from pathlib import Path
import ast
from scanners.code.python.code_scanner import CodeScanner

if TYPE_CHECKING:
    from scanners.resources.scan_context import FileScanContext
from scanners.violation import Violation

class DelegationScanner(CodeScanner):
    """
    Scans for proper delegation to collection classes.
    Detects:
    - Collection operations in non-collection classes (should delegate to collection)
    - Methods with 'find by' patterns that aren't in collection classes
    """
    
    def scan_file_with_context(self, context: 'FileScanContext') -> List[Dict[str, Any]]:
        file_path = context.file_path
        
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        # Check all classes for delegation issues
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                violations.extend(self._check_class_delegation(node, file_path))
        
        return violations
    
    def _check_class_delegation(self, class_node: ast.ClassDef, file_path: Path) -> List[Dict[str, Any]]:
        violations = []
        
        is_collection_class = self._is_collection_class(class_node.name)
        
        # Check methods for delegation patterns
        for method in class_node.body:
            if isinstance(method, ast.FunctionDef):
                method_name_lower = method.name.lower()
                
                # Check for 'find by' or 'filter by' patterns
                if ('find' in method_name_lower and 'by' in method_name_lower) or \
                   ('filter' in method_name_lower and 'by' in method_name_lower) or \
                   ('get' in method_name_lower and 'by' in method_name_lower):
                    
                    if not is_collection_class:
                        # Check if the method iterates over a collection
                        if self._has_iteration_or_comprehension(method):
                            violations.append(
                                Violation(
                                    rule=self.rule,
                                    violation_message=f'Method "{method.name}" performs collection operations. Consider delegating to a collection class.',
                                    location=str(file_path),
                                    line_number=method.lineno,
                                    severity='info'
                                ).to_dict()
                            )
        
        return violations
    
    def _is_collection_class(self, class_name: str) -> bool:
        """Check if class name indicates it's a collection."""
        class_lower = class_name.lower()
        collection_indicators = ['collection', 'list', 'set', 'registry', 'repository', 'store', 'cache']
        
        # Check for plural form (ends with 's') or explicit collection indicators
        if class_lower.endswith('s') and len(class_lower) > 3:
            return True
        
        return any(indicator in class_lower for indicator in collection_indicators)
    
    def _has_iteration_or_comprehension(self, method: ast.FunctionDef) -> bool:
        """Check if method contains loops or comprehensions over collections."""
        for node in ast.walk(method):
            if isinstance(node, (ast.For, ast.While, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                return True
            # Also check for filter(), map(), etc.
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in ['filter', 'map', 'any', 'all']:
                    return True
        return False
