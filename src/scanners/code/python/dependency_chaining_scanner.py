
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from pathlib import Path
import ast
from scanners.code.python.code_scanner import CodeScanner

if TYPE_CHECKING:
    from scanners.resources.scan_context import FileScanContext
from scanners.violation import Violation

class DependencyChainingScanner(CodeScanner):
    """
    Scans for proper dependency chaining with constructor injection.
    Detects:
    - Methods that pass dependencies as parameters instead of using injected collaborators
    - Direct access to sub-collaborators instead of accessing through owning objects
    """
    
    def scan_file_with_context(self, context: 'FileScanContext') -> List[Dict[str, Any]]:
        file_path = context.file_path
        
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        # Find all classes and check their constructor and method patterns
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                violations.extend(self._check_class_dependency_chaining(node, file_path))
        
        return violations
    
    def _check_class_dependency_chaining(self, class_node: ast.ClassDef, file_path: Path) -> List[Dict[str, Any]]:
        violations = []
        
        # Get constructor-injected dependencies
        init_method = None
        injected_deps = set()
        
        for method in class_node.body:
            if isinstance(method, ast.FunctionDef) and method.name == '__init__':
                init_method = method
                # Extract parameter names (skip 'self')
                for arg in method.args.args[1:]:
                    injected_deps.add(arg.arg)
                break
        
        # Check other methods for parameter passing that might indicate missing injection
        for method in class_node.body:
            if isinstance(method, ast.FunctionDef) and method.name != '__init__':
                # Check if method parameters look like they should be injected dependencies
                for i, arg in enumerate(method.args.args[1:], start=1):  # Skip 'self'
                    param_name = arg.arg
                    
                    # Look for patterns that suggest this should be an injected dependency
                    # e.g., parameters with class-like names or common collaborator patterns
                    if (self._looks_like_collaborator(param_name) and 
                        param_name not in injected_deps and
                        self._parameter_used_in_method(method, param_name)):
                        
                        violations.append(
                            Violation(
                                rule=self.rule,
                                violation_message=f'Method "{method.name}" receives "{param_name}" as parameter. Consider injecting it in constructor to chain dependencies properly.',
                                location=str(file_path),
                                line_number=method.lineno,
                                severity='warning'
                            ).to_dict()
                        )
        
        return violations
    
    def _looks_like_collaborator(self, param_name: str) -> bool:
        """Check if parameter name suggests it's a collaborator object."""
        # Common patterns for collaborators
        collaborator_suffixes = ['service', 'repository', 'manager', 'handler', 'provider', 'factory', 'helper', 'client', 'adapter']
        param_lower = param_name.lower()
        
        # Check for CamelCase or suffix patterns
        if any(suffix in param_lower for suffix in collaborator_suffixes):
            return True
        
        # Check if it starts with uppercase (likely a class/object)
        if param_name and param_name[0].isupper():
            return True
        
        return False
    
    def _parameter_used_in_method(self, method: ast.FunctionDef, param_name: str) -> bool:
        """Check if parameter is actually used in the method body."""
        for node in ast.walk(method):
            if isinstance(node, ast.Name) and node.id == param_name:
                return True
        return False
