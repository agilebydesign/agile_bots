"""Scanner for Delegation to Collection Classes in JavaScript code."""

from typing import List, Dict, Any
from pathlib import Path
from scanners.code.javascript.js_code_scanner import JSCodeScanner
from scanners.violation import Violation
from scanners.resources.scan_context import FileScanContext


class DelegationScanner(JSCodeScanner):
    """Detects improper delegation patterns in JavaScript code.
    
    Checks for:
    - Collection operations in non-collection classes
    - Methods with 'find by' patterns that aren't in collection classes
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
            violations.extend(self._check_class_delegation(class_info, context.file_path))
        
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
    
    def _check_class_delegation(self, class_node: Dict, file_path: Path) -> List[Dict[str, Any]]:
        violations = []
        
        class_name = class_node.get('id', {}).get('name', '')
        is_collection_class = self._is_collection_class(class_name)
        
        # Check all methods
        methods = self._find_methods(class_node)
        for method in methods:
            method_name = method.get('key', {}).get('name', '')
            method_name_lower = method_name.lower()
            
            # Check for 'find by' or 'filter by' patterns
            if ('find' in method_name_lower and 'by' in method_name_lower) or \
               ('filter' in method_name_lower and 'by' in method_name_lower) or \
               ('get' in method_name_lower and 'by' in method_name_lower):
                
                if not is_collection_class:
                    # Check if method has iteration
                    method_body = method.get('value', {})
                    if self._has_iteration(method_body):
                        violations.append(
                            self._create_violation(
                                f'Method "{method_name}" performs collection operations. Consider delegating to a collection class.',
                                file_path,
                                method.get('loc', {}).get('start', {}).get('line')
                            )
                        )
        
        return violations
    
    def _find_methods(self, class_node: Dict) -> List[Dict]:
        """Find all methods in class."""
        methods = []
        body = class_node.get('body', {}).get('body', [])
        for method in body:
            if method.get('type') == 'MethodDefinition':
                methods.append(method)
        return methods
    
    def _is_collection_class(self, class_name: str) -> bool:
        """Check if class name indicates it's a collection."""
        class_lower = class_name.lower()
        collection_indicators = ['collection', 'list', 'set', 'registry', 'repository', 'store', 'cache']
        
        # Check for plural form or explicit collection indicators
        if class_lower.endswith('s') and len(class_lower) > 3:
            return True
        
        return any(indicator in class_lower for indicator in collection_indicators)
    
    def _has_iteration(self, method_node: Dict) -> bool:
        """Check if method contains loops or array operations."""
        found_iteration = [False]
        
        def traverse(node):
            if isinstance(node, dict):
                node_type = node.get('type', '')
                
                # Check for loops
                if node_type in ['ForStatement', 'ForInStatement', 'ForOfStatement', 'WhileStatement']:
                    found_iteration[0] = True
                    return
                
                # Check for array methods (map, filter, find, etc.)
                if node_type == 'CallExpression':
                    callee = node.get('callee', {})
                    if callee.get('type') == 'MemberExpression':
                        property_name = callee.get('property', {}).get('name', '')
                        if property_name in ['map', 'filter', 'find', 'forEach', 'reduce', 'some', 'every']:
                            found_iteration[0] = True
                            return
                
                for value in node.values():
                    if found_iteration[0]:
                        return
                    if isinstance(value, list):
                        for item in value:
                            traverse(item)
                    else:
                        traverse(value)
            elif isinstance(node, list):
                for item in node:
                    if found_iteration[0]:
                        return
                    traverse(item)
        
        traverse(method_node)
        return found_iteration[0]
