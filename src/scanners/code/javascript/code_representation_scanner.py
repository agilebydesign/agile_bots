"""Scanner for Code Representation (avoiding abstract terminology) in JavaScript code."""

from typing import List, Dict, Any
from pathlib import Path
from scanners.code.javascript.js_code_scanner import JSCodeScanner
from scanners.violation import Violation
from scanners.resources.scan_context import FileScanContext


class CodeRepresentationScanner(JSCodeScanner):
    """Detects abstract terminology in JavaScript code.
    
    Checks for:
    - Class names using abstract terms
    - Parameter names using abstract terms
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
    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        violations = []
        
        if not context.exists or not str(context.file_path).endswith('.js'):
            return violations
        
        parsed = self._parse_js_file(context.file_path)
        if not parsed:
            return violations
        
        content, ast, lines = parsed
        
        # Find all class declarations
        classes = self._find_classes(ast)
        
        for class_info in classes:
            violations.extend(self._check_class_name(class_info, context.file_path))
            violations.extend(self._check_class_methods(class_info, context.file_path))
        
        return violations
    
    def _find_classes(self, ast: Dict) -> List[Dict]:
        """Extract all class declarations from AST."""
        classes = []
        
        def traverse(node):
            if isinstance(node, dict):
                if node.get('type') == 'ClassDeclaration':
                    classes.append(node)
                for value in node.values():
                    if isinstance(value, list):
                        for item in value:
                            traverse(item)
                    else:
                        traverse(value)
            elif isinstance(node, list):
                for item in node:
                    traverse(item)
        
        traverse(ast)
        return classes
    
    def _check_class_name(self, class_node: Dict, file_path: Path) -> List[Dict[str, Any]]:
        violations = []
        
        class_name = class_node.get('id', {}).get('name', '')
        class_name_lower = class_name.lower()
        
        for pattern in self.ABSTRACT_PATTERNS:
            if pattern in class_name_lower:
                violations.append(
                    self._create_violation(
                        f'Class "{class_name}" uses abstract terminology "{pattern}". Use concrete domain concepts that represent actual code.',
                        file_path,
                        class_node.get('loc', {}).get('start', {}).get('line')
                    )
                )
                break
        
        return violations
    
    def _check_class_methods(self, class_node: Dict, file_path: Path) -> List[Dict[str, Any]]:
        violations = []
        
        methods = self._find_methods(class_node)
        for method in methods:
            method_name = method.get('key', {}).get('name', '')
            
            # Skip private methods
            if method_name.startswith('_') or method_name.startswith('#'):
                continue
            
            # Check method parameters
            method_value = method.get('value', {})
            params = method_value.get('params', [])
            
            for param in params:
                param_name = ''
                
                if param.get('type') == 'Identifier':
                    param_name = param.get('name', '')
                elif param.get('type') == 'AssignmentPattern':
                    # Handle default parameters
                    left = param.get('left', {})
                    if left.get('type') == 'Identifier':
                        param_name = left.get('name', '')
                
                if param_name:
                    param_name_lower = param_name.lower()
                    
                    for pattern in self.ABSTRACT_PATTERNS:
                        if pattern in param_name_lower:
                            violations.append(
                                self._create_violation(
                                    f'Parameter "{param_name}" in "{method_name}" uses abstract terminology "{pattern}". Use concrete domain object names.',
                                    file_path,
                                    method.get('loc', {}).get('start', {}).get('line')
                                )
                            )
                            break
        
        return violations
    
    def _find_methods(self, class_node: Dict) -> List[Dict]:
        """Find all methods in class."""
        methods = []
        body = class_node.get('body', {}).get('body', [])
        for method in body:
            if method.get('type') == 'MethodDefinition':
                methods.append(method)
        return methods
