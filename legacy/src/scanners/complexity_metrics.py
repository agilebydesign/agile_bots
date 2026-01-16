"""Shared complexity metrics calculations for scanners."""

from typing import Any, Dict, List, Set, Optional
import ast


class ComplexityMetrics:
    
    @staticmethod
    def cyclomatic_complexity(func_node: ast.FunctionDef) -> int:
        complexity = 1  # Base complexity
        
        for node in ast.walk(func_node):
            # Decision points
            if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With)):
                complexity += 1
            # Boolean operators add complexity
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            elif isinstance(node, ast.Assert):
                complexity += 1
        
        return complexity
    
    @staticmethod
    def cognitive_complexity(func_node: ast.FunctionDef) -> int:
        complexity = 0
        nesting_level = 0
        
        def visit_node(node: ast.AST, level: int):
            nonlocal complexity
            
            # Increment complexity for decision points
            if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1 + level  # Nesting adds to complexity
                # Visit children with increased nesting
                for child in ast.iter_child_nodes(node):
                    visit_node(child, level + 1)
            elif isinstance(node, ast.With):
                complexity += 1 + level
                for child in ast.iter_child_nodes(node):
                    visit_node(child, level + 1)
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1 + level
                for child in ast.iter_child_nodes(node):
                    visit_node(child, level)
            elif isinstance(node, ast.Assert):
                complexity += 1 + level
            else:
                # Visit children at same nesting level
                for child in ast.iter_child_nodes(node):
                    visit_node(child, level)
        
        for stmt in func_node.body:
            visit_node(stmt, 0)
        
        return complexity
    
    @staticmethod
    def max_nesting_depth(func_node: ast.FunctionDef) -> int:
        max_depth = 0
        
        def visit_node(node: ast.AST, depth: int):
            nonlocal max_depth
            max_depth = max(max_depth, depth)
            
            # Increase depth for nested structures
            if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.FunctionDef)):
                for child in ast.iter_child_nodes(node):
                    visit_node(child, depth + 1)
            else:
                for child in ast.iter_child_nodes(node):
                    visit_node(child, depth)
        
        for stmt in func_node.body:
            visit_node(stmt, 0)
        
        return max_depth
    
    @staticmethod
    def detect_responsibilities(func_node: ast.FunctionDef) -> List[str]:
        detailed = ComplexityMetrics.detect_responsibilities_with_examples(func_node)
        return sorted(list(detailed.keys()))
    
    @staticmethod
    def detect_responsibilities_with_examples(func_node: ast.FunctionDef) -> Dict[str, List[Dict[str, Any]]]:
        responsibilities: Dict[str, List[Dict[str, Any]]] = {}
        
        def add_example(resp_type: str, node: ast.AST):
            if resp_type not in responsibilities:
                responsibilities[resp_type] = []
            # Only keep first 2 examples per type to avoid verbose output
            if len(responsibilities[resp_type]) < 2:
                line = getattr(node, 'lineno', None)
                try:
                    code = ast.unparse(node) if hasattr(ast, 'unparse') else str(node)
                    if len(code) > 80:
                        code = code[:77] + '...'
                except:
                    code = '<code unavailable>'
                responsibilities[resp_type].append({'line': line, 'code': code})
        
        for node in ast.walk(func_node):
            # I/O operations - must be actual file/network operations, not dict methods
            if isinstance(node, ast.Call):
                func_name = ComplexityMetrics._get_call_name(node)
                if func_name and ComplexityMetrics._is_io_operation(func_name, node):
                    add_example('I/O', node)
            
            # Validation (assertions, checks, validations)
            if isinstance(node, ast.Assert):
                add_example('Validation', node)
            
            # Transformation (assignments with meaningful operations, not simple accessors)
            if isinstance(node, ast.Assign):
                if ComplexityMetrics._has_transformation(node):
                    add_example('Transformation', node)
            
            # Computation (math operations - but not simple comparisons or string ops)
            if isinstance(node, ast.BinOp):
                # Only count actual math, not string concatenation or list operations
                if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.FloorDiv)):
                    add_example('Computation', node)
        
        return responsibilities
    
    @staticmethod
    def _is_io_operation(func_name: str, call_node: ast.Call) -> bool:
        func_name_lower = func_name.lower()
        
        # Exclude common collection accessor methods (these are NOT I/O)
        non_io_methods = {
            'get', 'items', 'keys', 'values', 'pop', 'update', 'setdefault',
            'append', 'extend', 'insert', 'remove', 'clear', 'copy',
            'add', 'discard', 'union', 'intersection',
            'getattr', 'setattr', 'hasattr', 'isinstance', 'issubclass',
            'len', 'str', 'int', 'float', 'bool', 'list', 'dict', 'set', 'tuple',
            'format', 'join', 'split', 'strip', 'replace', 'lower', 'upper',
            'startswith', 'endswith', 'find', 'index', 'count'
        }
        if func_name_lower in non_io_methods:
            return False
        
        # These are actual I/O keywords
        io_keywords = ['open', 'read_file', 'write_file', 'load_json', 'save_json',
                       'read_text', 'write_text', 'read_bytes', 'write_bytes',
                       'fetch', 'request', 'post', 'download', 'upload',
                       'read_json', 'read_yaml', 'read_csv']
        
        if func_name_lower in io_keywords:
            return True
        if any(keyword in func_name_lower for keyword in ['read_', 'write_', 'load_', 'save_', 'fetch_']):
            return True
        
        # 'open' is I/O only if it's the builtin
        if func_name_lower == 'open':
            return True
        
        return False
    
    @staticmethod
    def _get_call_name(call_node: ast.Call) -> Optional[str]:
        if isinstance(call_node.func, ast.Name):
            return call_node.func.id
        elif isinstance(call_node.func, ast.Attribute):
            return call_node.func.attr
        return None
    
    @staticmethod
    def _has_transformation(assign_node: ast.Assign) -> bool:
        if not assign_node.value:
            return False
        
        if isinstance(assign_node.value, ast.Call):
            func_name = ComplexityMetrics._get_call_name(assign_node.value)
            if func_name:
                # Simple utilities are NOT transformations
                simple_utilities = {
                    'list', 'dict', 'set', 'tuple', 'str', 'int', 'float', 'bool',
                    'len', 'sorted', 'reversed', 'enumerate', 'zip', 'range',
                    'get', 'items', 'keys', 'values', 'copy', 'pop',
                    'strip', 'lower', 'upper', 'split', 'join', 'replace',
                    'startswith', 'endswith', 'format',
                    'append', 'extend', 'insert', 'remove', 'clear',
                    'add', 'discard', 'update',
                    'glob', 'exists', 'is_file', 'is_dir',
                    'relative_to', 'parent', 'name', 'stem', 'suffix'
                }
                if func_name.lower() in simple_utilities:
                    return False
            # Other function calls are transformations
            return True
        
        # List/dict comprehensions are transformations
        if isinstance(assign_node.value, (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)):
            return True
        
        # BinOp/UnaryOp - only count if it's actual transformation, not simple concatenation
        # (We handle this separately in detect_responsibilities for Computation)
        
        return False
    
    @staticmethod
    def calculate_lcom(class_node: ast.ClassDef) -> float:
        methods = [node for node in class_node.body if isinstance(node, ast.FunctionDef)]
        
        # Filter out simple property getters - they're data accessors, not real methods
        meaningful_methods = []
        for method in methods:
            if not ComplexityMetrics._is_simple_property_getter(method):
                meaningful_methods.append(method)
        
        if len(meaningful_methods) < 2:
            return 0.0  # Single method or no methods = perfect cohesion
        
        method_attributes = []
        for method in meaningful_methods:
            attrs = ComplexityMetrics._get_accessed_attributes(method, class_node)
            method_attributes.append(attrs)
        
        # Count pairs of methods that don't share attributes
        non_shared_pairs = 0
        total_pairs = 0
        
        for i in range(len(method_attributes)):
            for j in range(i + 1, len(method_attributes)):
                total_pairs += 1
                if not (method_attributes[i] & method_attributes[j]):
                    non_shared_pairs += 1
        
        if total_pairs == 0:
            return 0.0
        
        # LCOM = ratio of non-shared pairs to total pairs
        return non_shared_pairs / total_pairs
    
    @staticmethod
    def _is_simple_property_getter(method_node: ast.FunctionDef) -> bool:
        # Must have exactly one statement (or docstring + return)
        body = method_node.body
        
        # Skip docstring if present
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, (ast.Str, ast.Constant)):
            body = body[1:]
        
        # Must be exactly one return statement
        if len(body) != 1:
            return False
        
        stmt = body[0]
        if not isinstance(stmt, ast.Return):
            return False
        
        if stmt.value is None:
            return False
        
        if isinstance(stmt.value, ast.Attribute):
            if isinstance(stmt.value.value, ast.Name) and stmt.value.value.id == 'self':
                return True
        
        return False
    
    @staticmethod
    def _get_accessed_attributes(method_node: ast.FunctionDef, class_node: ast.ClassDef) -> Set[str]:
        attributes = set()
        
        class_attrs = set()
        for node in class_node.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        class_attrs.add(target.id)
        
        # Find attribute accesses in method
        for node in ast.walk(method_node):
            if isinstance(node, ast.Attribute):
                # Direct self.attr access
                if isinstance(node.value, ast.Name) and node.value.id == 'self':
                    attr_name = ComplexityMetrics._normalize_attr_name(node.attr)
                    attributes.add(attr_name)
                # Delegation: self.x.y - count as accessing 'x'
                elif isinstance(node.value, ast.Attribute):
                    if isinstance(node.value.value, ast.Name) and node.value.value.id == 'self':
                        attr_name = ComplexityMetrics._normalize_attr_name(node.value.attr)
                        attributes.add(attr_name)
            elif isinstance(node, ast.Name):
                if node.id in class_attrs:
                    attr_name = ComplexityMetrics._normalize_attr_name(node.id)
                    attributes.add(attr_name)
        
        return attributes
    
    @staticmethod
    def _normalize_attr_name(attr: str) -> str:
        if attr.startswith('_') and not attr.startswith('__'):
            return attr[1:]
        return attr
    
    @staticmethod
    def _get_method_code_sample(method: ast.FunctionDef) -> str:
        try:
            if not hasattr(ast, 'unparse'):
                return f'def {method.name}(...)'
            
            # Skip docstring if present
            body = method.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, (ast.Str, ast.Constant)):
                body = body[1:]
            
            if body:
                first_stmt = body[0]
                code = ast.unparse(first_stmt)
                # Truncate if too long
                if len(code) > 80:
                    code = code[:77] + '...'
                return code
            
            return f'def {method.name}(...)'
        except:
            return f'def {method.name}(...)'
    
    @staticmethod
    def detect_class_responsibilities(class_node: ast.ClassDef) -> List[str]:
        detailed = ComplexityMetrics.detect_class_responsibilities_with_examples(class_node)
        if len(detailed) > 3:
            return list(detailed.keys())
        return []
    
    @staticmethod
    def detect_class_responsibilities_with_examples(class_node: ast.ClassDef) -> Dict[str, List[Dict[str, Any]]]:
        methods = [node for node in class_node.body if isinstance(node, ast.FunctionDef)]
        
        if len(methods) == 0:
            return {}
        
        # Group methods by responsibility type with examples
        responsibility_groups: Dict[str, List[Dict[str, Any]]] = {}
        
        for method in methods:
            responsibilities_detailed = ComplexityMetrics.detect_responsibilities_with_examples(method)
            if not responsibilities_detailed:
                # Method has no detected responsibility - classify as General
                if 'General' not in responsibility_groups:
                    responsibility_groups['General'] = []
                if len(responsibility_groups['General']) < 2:
                    code_sample = ComplexityMetrics._get_method_code_sample(method)
                    responsibility_groups['General'].append({
                        'method': method.name,
                        'line': method.lineno,
                        'code': code_sample
                    })
            else:
                for resp_type, examples in responsibilities_detailed.items():
                    if resp_type not in responsibility_groups:
                        responsibility_groups[resp_type] = []
                    if len(responsibility_groups[resp_type]) < 2 and examples:
                        first_example = examples[0]
                        responsibility_groups[resp_type].append({
                            'method': method.name,
                            'line': first_example.get('line'),
                            'code': first_example.get('code', '')
                        })
        
        return responsibility_groups








