"""Scanner for Dependency Chaining in JavaScript code."""

from typing import List, Dict, Any
from pathlib import Path
from scanners.code.javascript.js_code_scanner import JSCodeScanner
from scanners.violation import Violation
from scanners.resources.scan_context import FileScanContext


class DependencyChainingScanner(JSCodeScanner):
    """Detects improper dependency chaining in JavaScript code.
    
    Checks for:
    - Methods receiving dependencies as parameters instead of constructor injection
    - Direct access to sub-collaborators
    """
    
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
            violations.extend(self._check_class_dependency_chaining(class_info, context.file_path))
        
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
    
    def _check_class_dependency_chaining(self, class_node: Dict, file_path: Path) -> List[Dict[str, Any]]:
        violations = []
        
        # Get constructor parameters
        constructor_params = set()
        constructor = self._find_constructor(class_node)
        if constructor:
            for param in constructor.get('params', []):
                if param.get('type') == 'Identifier':
                    constructor_params.add(param.get('name', ''))
        
        # Check all methods for parameter-passed dependencies
        methods = self._find_methods(class_node)
        for method in methods:
            method_name = method.get('key', {}).get('name', '')
            
            # Skip constructor
            if method_name == 'constructor':
                continue
            
            # Check method parameters
            params = method.get('value', {}).get('params', [])
            for param in params:
                if param.get('type') == 'Identifier':
                    param_name = param.get('name', '')
                    
                    if self._looks_like_collaborator(param_name) and param_name not in constructor_params:
                        violations.append(
                            self._create_violation(
                                f'Method "{method_name}" receives "{param_name}" as parameter. Consider injecting it in constructor to chain dependencies properly.',
                                file_path,
                                method.get('loc', {}).get('start', {}).get('line')
                            )
                        )
        
        return violations
    
    def _find_constructor(self, class_node: Dict) -> Dict:
        """Find constructor method in class."""
        body = class_node.get('body', {}).get('body', [])
        for method in body:
            if method.get('type') == 'MethodDefinition':
                if method.get('key', {}).get('name') == 'constructor':
                    return method.get('value', {})
        return {}
    
    def _find_methods(self, class_node: Dict) -> List[Dict]:
        """Find all methods in class."""
        methods = []
        body = class_node.get('body', {}).get('body', [])
        for method in body:
            if method.get('type') == 'MethodDefinition':
                methods.append(method)
        return methods
    
    def _looks_like_collaborator(self, param_name: str) -> bool:
        """Check if parameter name suggests it's a collaborator object."""
        collaborator_suffixes = ['service', 'repository', 'manager', 'handler', 'provider', 'factory', 'helper', 'client', 'adapter']
        param_lower = param_name.lower()
        
        if any(suffix in param_lower for suffix in collaborator_suffixes):
            return True
        
        # Check if it starts with uppercase (likely a class/object)
        if param_name and param_name[0].isupper():
            return True
        
        return False
