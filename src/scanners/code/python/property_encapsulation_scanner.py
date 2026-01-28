
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from pathlib import Path
import ast
import re
from scanners.code.python.code_scanner import CodeScanner

if TYPE_CHECKING:
    from scanners.resources.scan_context import FileScanContext
from scanners.violation import Violation

class PropertyEncapsulationScanner(CodeScanner):
    """
    Scans for proper property encapsulation.
    Detects:
    - Methods that expose internal structure (return lists, dicts instead of domain objects)
    - Methods using 'calculate' or 'compute' instead of properties
    """
    
    EXPOSED_STATE_PATTERNS = [
        r'\blist\b',
        r'\barray\b',
        r'\bdictionary\b',
        r'\bdict\b',
        r'\bset\b',
    ]
    
    def scan_file_with_context(self, context: 'FileScanContext') -> List[Dict[str, Any]]:
        file_path = context.file_path
        
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        # Check all classes for encapsulation issues
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                violations.extend(self._check_class_encapsulation(node, file_path))
        
        return violations
    
    def _check_class_encapsulation(self, class_node: ast.ClassDef, file_path: Path) -> List[Dict[str, Any]]:
        violations = []
        
        for method in class_node.body:
            if isinstance(method, ast.FunctionDef):
                method_name = method.name
                method_name_lower = method_name.lower()
                
                # Skip private and magic methods
                if method_name.startswith('_'):
                    continue
                
                # Check for 'calculate' or 'compute' patterns
                if method_name_lower.startswith('calculate') or method_name_lower.startswith('compute'):
                    # Check if this should be a property instead
                    if self._looks_like_property_getter(method):
                        violations.append(
                            Violation(
                                rule=self.rule,
                                violation_message=f'Method "{method_name}" uses calculate/compute. Consider using a property "get_X" to hide calculation timing.',
                                location=str(file_path),
                                line_number=method.lineno,
                                severity='warning'
                            ).to_dict()
                        )
                
                # Check return type hints for exposed collections
                if method.returns:
                    return_type = self._get_return_type_string(method.returns)
                    for pattern in self.EXPOSED_STATE_PATTERNS:
                        if re.search(pattern, return_type.lower()):
                            violations.append(
                                Violation(
                                    rule=self.rule,
                                    violation_message=f'Method "{method_name}" returns "{return_type}" which exposes internal structure. Consider returning a domain object instead.',
                                    location=str(file_path),
                                    line_number=method.lineno,
                                    severity='warning'
                                ).to_dict()
                            )
                            break
                
                # Check method names for exposed collection patterns
                if re.search(r'get.*list|get.*dict|get.*array|return.*list', method_name_lower):
                    violations.append(
                        Violation(
                            rule=self.rule,
                            violation_message=f'Method "{method_name}" exposes collection type in name. Use domain object name instead (e.g., "get_holdings" not "get_holdings_list").',
                            location=str(file_path),
                            line_number=method.lineno,
                            severity='info'
                        ).to_dict()
                    )
        
        return violations
    
    def _looks_like_property_getter(self, method: ast.FunctionDef) -> bool:
        """Check if method looks like a simple property getter."""
        # Has no parameters beyond self
        if len(method.args.args) > 1:
            return False
        
        # Has a return statement
        has_return = any(isinstance(node, ast.Return) for node in ast.walk(method))
        return has_return
    
    def _get_return_type_string(self, return_annotation: ast.expr) -> str:
        """Extract return type as string from annotation."""
        if isinstance(return_annotation, ast.Name):
            return return_annotation.id
        elif isinstance(return_annotation, ast.Subscript):
            # Handle List[X], Dict[X, Y], etc.
            if isinstance(return_annotation.value, ast.Name):
                return return_annotation.value.id
        elif isinstance(return_annotation, ast.Constant):
            return str(return_annotation.value)
        
        return ast.unparse(return_annotation) if hasattr(ast, 'unparse') else ''
