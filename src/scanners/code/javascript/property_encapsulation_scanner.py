"""Scanner for Property Encapsulation in JavaScript code."""

from typing import List, Dict, Any
from pathlib import Path
import re
from scanners.code.javascript.js_code_scanner import JSCodeScanner
from scanners.violation import Violation
from scanners.resources.scan_context import FileScanContext


class PropertyEncapsulationScanner(JSCodeScanner):
    """Detects improper property encapsulation in JavaScript code.
    
    Checks for:
    - Methods that expose internal structure (return arrays, objects)
    - Methods using 'calculate' or 'compute' instead of getters
    """
    
    EXPOSED_STATE_PATTERNS = [
        r'\blist\b',
        r'\barray\b',
        r'\bdictionary\b',
        r'\bdict\b',
        r'\bmap\b',
        r'\bset\b',
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
            violations.extend(self._check_class_encapsulation(class_info, context.file_path))
        
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
    
    def _check_class_encapsulation(self, class_node: Dict, file_path: Path) -> List[Dict[str, Any]]:
        violations = []
        
        methods = self._find_methods(class_node)
        for method in methods:
            method_name = method.get('key', {}).get('name', '')
            method_name_lower = method_name.lower()
            
            # Skip private methods
            if method_name.startswith('_') or method_name.startswith('#'):
                continue
            
            # Check for 'calculate' or 'compute' patterns
            if method_name_lower.startswith('calculate') or method_name_lower.startswith('compute'):
                if self._looks_like_getter(method):
                    violations.append(
                        self._create_violation(
                            f'Method "{method_name}" uses calculate/compute. Consider using a getter "get{method_name[9:]}" to hide calculation timing.',
                            file_path,
                            method.get('loc', {}).get('start', {}).get('line')
                        )
                    )
            
            # Check method names for exposed collection patterns
            if re.search(r'get.*list|get.*array|get.*map|return.*list', method_name_lower):
                violations.append(
                    self._create_violation(
                        f'Method "{method_name}" exposes collection type in name. Use domain object name instead (e.g., "getHoldings" not "getHoldingsList").',
                        file_path,
                        method.get('loc', {}).get('start', {}).get('line')
                    )
                )
            
            # Check JSDoc for exposed types
            if method.get('leadingComments'):
                for comment in method.get('leadingComments', []):
                    comment_text = comment.get('value', '').lower()
                    if '@returns' in comment_text or '@return' in comment_text:
                        for pattern in self.EXPOSED_STATE_PATTERNS:
                            if re.search(pattern, comment_text):
                                violations.append(
                                    self._create_violation(
                                        f'Method "{method_name}" JSDoc indicates it returns a collection type. Consider returning a domain object instead.',
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
    
    def _looks_like_getter(self, method: Dict) -> bool:
        """Check if method looks like a simple getter."""
        method_value = method.get('value', {})
        params = method_value.get('params', [])
        
        # Has no parameters
        if len(params) > 0:
            return False
        
        # Has a return statement
        has_return = self._has_return_statement(method_value)
        return has_return
    
    def _has_return_statement(self, node: Dict) -> bool:
        """Check if node contains a return statement."""
        found = [False]
        
        def traverse(n):
            if isinstance(n, dict):
                if n.get('type') == 'ReturnStatement':
                    found[0] = True
                    return
                for value in n.values():
                    if found[0]:
                        return
                    if isinstance(value, list):
                        for item in value:
                            traverse(item)
                    else:
                        traverse(value)
            elif isinstance(n, list):
                for item in n:
                    if found[0]:
                        return
                    traverse(item)
        
        traverse(node)
        return found[0]
