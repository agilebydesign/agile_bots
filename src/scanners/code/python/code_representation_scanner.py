
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from pathlib import Path
import ast
from scanners.code.python.code_scanner import CodeScanner

if TYPE_CHECKING:
    from scanners.resources.scan_context import FileScanContext
from scanners.violation import Violation

class CodeRepresentationScanner(CodeScanner):
    """
    Scans for abstract terminology that should be concrete code representations.
    Detects:
    - Class names using abstract terms (concept, insight, pattern, knowledge)
    - Variable names using abstract terms
    """
    
    ABSTRACT_PATTERNS = [
        'concept',
        'insight',
        'pattern',
        'knowledge',
        'abstract',
        'metadata',
        'information',
        'data',
    ]
    
    def scan_file_with_context(self, context: 'FileScanContext') -> List[Dict[str, Any]]:
        file_path = context.file_path
        
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        # Check class names
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                violations.extend(self._check_class_name(node, file_path))
            elif isinstance(node, ast.FunctionDef):
                violations.extend(self._check_function_parameters(node, file_path))
        
        return violations
    
    def _check_class_name(self, class_node: ast.ClassDef, file_path: Path) -> List[Dict[str, Any]]:
        violations = []
        
        class_name_lower = class_node.name.lower()
        
        for pattern in self.ABSTRACT_PATTERNS:
            if pattern in class_name_lower:
                violations.append(
                    Violation(
                        rule=self.rule,
                        violation_message=f'Class "{class_node.name}" uses abstract terminology "{pattern}". Use concrete domain concepts that represent actual code.',
                        location=str(file_path),
                        line_number=class_node.lineno,
                        severity='info'
                    ).to_dict()
                )
                break
        
        return violations
    
    def _check_function_parameters(self, func_node: ast.FunctionDef, file_path: Path) -> List[Dict[str, Any]]:
        violations = []
        
        # Skip private methods
        if func_node.name.startswith('_'):
            return violations
        
        # Check parameter names for abstract terms
        for arg in func_node.args.args:
            param_name_lower = arg.arg.lower()
            
            for pattern in self.ABSTRACT_PATTERNS:
                if pattern in param_name_lower and arg.arg != 'self':
                    violations.append(
                        Violation(
                            rule=self.rule,
                            violation_message=f'Parameter "{arg.arg}" in "{func_node.name}" uses abstract terminology "{pattern}". Use concrete domain object names.',
                            location=str(file_path),
                            line_number=func_node.lineno,
                            severity='info'
                        ).to_dict()
                    )
                    break
        
        # Check parameter type annotations
        for arg in func_node.args.args:
            if arg.annotation and arg.arg != 'self':
                type_str = self._get_type_string(arg.annotation)
                type_str_lower = type_str.lower()
                
                for pattern in self.ABSTRACT_PATTERNS:
                    if pattern in type_str_lower:
                        violations.append(
                            Violation(
                                rule=self.rule,
                                violation_message=f'Parameter "{arg.arg}" type "{type_str}" uses abstract terminology. Use concrete type names.',
                                location=str(file_path),
                                line_number=func_node.lineno,
                                severity='info'
                            ).to_dict()
                        )
                        break
        
        return violations
    
    def _get_type_string(self, annotation: ast.expr) -> str:
        """Extract type as string from annotation."""
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Constant):
            return str(annotation.value)
        
        return ast.unparse(annotation) if hasattr(ast, 'unparse') else ''
