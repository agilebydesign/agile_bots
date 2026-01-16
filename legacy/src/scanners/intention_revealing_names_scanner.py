"""Scanner for validating intention-revealing names in code."""

from typing import List, Dict, Any, Optional
from pathlib import Path
import ast
import re
import logging
from .code_scanner import CodeScanner
from .violation import Violation
from .resources.ast_elements import Functions, Classes

logger = logging.getLogger(__name__)


class IntentionRevealingNamesScanner(CodeScanner):
    
    def __init__(self):
        super().__init__()
        self.knowledge_graph = None
    
    def scan(self, knowledge_graph: Dict[str, Any], rule_obj: Any = None, test_files: Optional[List['Path']] = None, code_files: Optional[List['Path']] = None, on_file_scanned: Optional[Any] = None) -> List[Dict[str, Any]]:
        self.knowledge_graph = knowledge_graph
        return super().scan(knowledge_graph, rule_obj, test_files=test_files, code_files=code_files, on_file_scanned=on_file_scanned)
    
    # Acceptable domain terms that are well-known and intention-revealing
    ACCEPTABLE_DOMAIN_TERMS = {
        'scan', 'scan_test_file', 'scan_code_file', 'scan_cross_file',  # Scanner interface methods
        'parse', 'render', 'build', 'load', 'save', 'read', 'write',  # Common operations
        'get', 'set', 'has', 'is', 'can',  # Common predicate/getter patterns
        'init', '__init__', '__str__', '__repr__', '__eq__',  # Special methods
    }
    
    # Acceptable generic names in specific contexts (e.g., callback parameters, event handlers)
    ACCEPTABLE_CONTEXT_NAMES = {
        'data',  # Acceptable in data processing contexts
        'value',  # Acceptable in transformation contexts
        'item',  # Acceptable in iteration contexts
        'result',  # Acceptable as return value name
    }
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, knowledge_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        if not file_path.exists():
            return violations
        
        # Extract domain terms from knowledge graph (using enhanced extraction from CodeScanner base class)
        domain_terms = set()
        if self.knowledge_graph:
            domain_terms = self._extract_domain_terms(self.knowledge_graph)
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        docstring_ranges = self._get_docstring_ranges(tree)
        
        violations.extend(self._check_variable_names(tree, file_path, rule_obj, content, domain_terms, docstring_ranges))
        
        violations.extend(self._check_function_names(tree, file_path, rule_obj, domain_terms))
        
        violations.extend(self._check_class_names(tree, file_path, rule_obj, domain_terms))
        
        return violations
    
    def _check_variable_names(self, tree: ast.AST, file_path: Path, rule_obj: Any, content: str, domain_terms: set = None, docstring_ranges: List[tuple] = None) -> List[Dict[str, Any]]:
        violations = []
        
        if domain_terms is None:
            domain_terms = set()
        if docstring_ranges is None:
            docstring_ranges = []
        
        # Generic names that should be flagged (excluding acceptable context names and domain terms)
        generic_names = ['info', 'thing', 'stuff', 'temp']
        
        # Collect all acceptable single-letter variable NAMES (those defined in loops, comprehensions, exceptions, etc.)
        # We collect just the names (not line numbers) because once a var is defined in a loop,
        # it's acceptable to use that single-letter name throughout that scope
        acceptable_single_letter_names = self._collect_loop_and_comprehension_var_names(tree)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                var_name = node.id
                
                # Skip if node is inside a docstring or comment
                if self._is_in_docstring_or_comment(node, content, docstring_ranges):
                    continue
                
                # Skip if it's a store context (assignment target) - check if it's acceptable in context
                if isinstance(node.ctx, ast.Store):
                    if self._is_acceptable_in_context(node, tree, content):
                        continue
                
                # ONLY allow in loops, comprehensions, exception handlers, lambdas
                # i, j, k are always allowed (classic loop counters)
                # _ is always allowed (unused value convention)
                always_allowed = {'i', 'j', 'k', '_'}
                if len(var_name) == 1:
                    if var_name in always_allowed:
                        continue  # Always OK
                    if var_name in acceptable_single_letter_names:
                        continue  # OK - it's a loop/comprehension/exception variable
                    # Not in an acceptable context - flag it
                    violations.append(self._create_generic_name_violation(
                        rule_obj, file_path, node, var_name, 'variable', 'single-letter'
                    ))
                    continue
                
                var_name_lower = var_name.lower()
                if var_name_lower in generic_names:
                    if var_name_lower in domain_terms:
                        continue
                    if not self._is_acceptable_in_context(node, tree, content):
                        violations.append(self._create_generic_name_violation(
                            rule_obj, file_path, node, var_name, 'variable', 'generic'
                        ))
                # Also check if variable name matches domain terms using compound term matching
                elif domain_terms:
                    # Use compound term matching (from CodeScanner base class)
                    if self._matches_domain_term(var_name, domain_terms):
                        continue  # Matches domain term - likely acceptable
        
        return violations
    
    def _create_generic_name_violation(
        self, 
        rule_obj: Any, 
        file_path: Path, 
        node: ast.AST, 
        name: str, 
        name_type: str, 
        issue_type: str,
        severity: str = 'error'
    ) -> Dict[str, Any]:
        line_number = node.lineno if hasattr(node, 'lineno') else None
        
        if issue_type == 'single-letter':
            message = f'{name_type.capitalize()} "{name}" uses single-letter name - use intention-revealing name'
        elif name_type == 'function':
            message = f'Function "{name}" uses generic name - use intention-revealing name that explains purpose'
        elif name_type == 'class':
            message = f'Class "{name}" uses generic name - use intention-revealing name that explains purpose'
        else:  # variable generic
            message = f'Variable "{name}" uses generic name - use intention-revealing name'
        
        try:
            content = file_path.read_text(encoding='utf-8')
            return self._create_violation_with_snippet(
                rule_obj=rule_obj,
                violation_message=message,
                file_path=file_path,
                line_number=line_number,
                severity=severity,
                content=content,
                ast_node=node,
                max_lines=3
            )
        except Exception:
            return Violation(
                rule=rule_obj,
                violation_message=message,
                location=str(file_path),
                line_number=line_number,
                severity=severity
            ).to_dict()
    
    def _collect_loop_and_comprehension_var_names(self, tree: ast.AST) -> set:
        acceptable_names = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                self._add_target_var_names(node.target, acceptable_names)
            
            # Exception handlers
            elif isinstance(node, ast.ExceptHandler):
                if node.name:
                    acceptable_names.add(node.name)
            
            # List/Set/Dict comprehensions and generator expressions
            elif isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                for generator in node.generators:
                    self._add_target_var_names(generator.target, acceptable_names)
            
            # Lambda parameters
            elif isinstance(node, ast.Lambda):
                for arg in node.args.args:
                    acceptable_names.add(arg.arg)
            
            elif isinstance(node, ast.With):
                for item in node.items:
                    if item.optional_vars:
                        self._add_target_var_names(item.optional_vars, acceptable_names)
        
        return acceptable_names
    
    def _add_target_var_names(self, target: ast.AST, acceptable_names: set):
        if isinstance(target, ast.Name):
            acceptable_names.add(target.id)
        elif isinstance(target, ast.Tuple):
            for elt in target.elts:
                self._add_target_var_names(elt, acceptable_names)
    
    def _is_acceptable_in_context(self, node: ast.Name, tree: ast.AST, content: str) -> bool:
        # Check if it's a function parameter (acceptable for generic names in some contexts)
        # This is a simplified check - in practice, you'd traverse the AST to find the function definition
        # For now, we'll be more lenient and only flag obvious violations
        
        # (This is a simplified heuristic - full implementation would require AST traversal)
        return False
    
    def _check_function_names(self, tree: ast.AST, file_path: Path, rule_obj: Any, domain_terms: set = None) -> List[Dict[str, Any]]:
        violations = []
        
        if domain_terms is None:
            domain_terms = set()
        
        functions = Functions(tree)
        for function in functions.get_many_functions:
            func_name = function.node.name
            func_name_lower = func_name.lower()
            
            # Skip private methods and special methods
            if func_name.startswith('_') and func_name != '__init__':
                continue
            
            if func_name_lower in self.ACCEPTABLE_DOMAIN_TERMS:
                continue
            
            if domain_terms:
                if self._matches_domain_term(func_name, domain_terms):
                    continue  # Matches domain term - likely acceptable
            
            generic_names = ['process', 'handle', 'do', 'execute', 'run', 'main']
            # Only flag if it's standalone generic name, not part of a descriptive name
            if func_name_lower in generic_names and len(func_name.split('_')) == 1:
                violations.append(self._create_generic_name_violation(
                    rule_obj, file_path, function.node, func_name, 'function', 'generic'
                ))
        
        return violations
    
    def _check_class_names(self, tree: ast.AST, file_path: Path, rule_obj: Any, domain_terms: set = None) -> List[Dict[str, Any]]:
        violations = []
        
        if domain_terms is None:
            domain_terms = set()
        
        # Acceptable class name patterns (e.g., Scanner, CodeScanner, TestScanner are OK)
        acceptable_class_patterns = ['Scanner', 'CodeScanner', 'TestScanner', 'StoryScanner']
        
        classes = Classes(tree)
        for cls in classes.get_many_classes:
            class_name = cls.node.name
            class_name_lower = class_name.lower()
            
            if any(pattern in class_name for pattern in acceptable_class_patterns):
                continue
            
            if domain_terms:
                if self._matches_domain_term(class_name, domain_terms):
                    continue  # Matches domain term - likely acceptable
            
            generic_names = ['Manager', 'Handler', 'Processor', 'Util', 'Helper', 'Service']
            # Only flag if class name IS the generic name or ends with it without descriptive prefix
            if class_name in generic_names:
                violations.append(self._create_generic_name_violation(
                    rule_obj, file_path, cls.node, class_name, 'class', 'generic', 'error'
                ))
            # Flag if class name ends with generic name without descriptive prefix (e.g., "MyHandler" is OK, "Handler" is not)
            elif any(class_name.endswith(g) and len(class_name) <= len(g) + 2 for g in generic_names):
                violations.append(self._create_generic_name_violation(
                    rule_obj, file_path, cls.node, class_name, 'class', 'generic', 'warning'
                ))
        
        return violations
    
    def _is_in_small_loop(self, node: ast.Name) -> bool:
        parent = getattr(node, 'parent', None)
        if parent and isinstance(parent, ast.For):
            if isinstance(parent.iter, ast.Call):
                if isinstance(parent.iter.func, ast.Name) and parent.iter.func.id == 'range':
                    return True
            # Also allow iteration over small lists/tuples (common pattern)
            elif isinstance(parent.iter, (ast.List, ast.Tuple)):
                if len(parent.iter.elts) <= 5:  # Small collection
                    return True
        return False
    
    def _get_docstring_ranges(self, tree: ast.AST) -> List[tuple]:
        docstring_ranges = []
        
        def visit_node(node):
            if hasattr(node, 'body') and isinstance(node.body, list) and len(node.body) > 0:
                first_stmt = node.body[0]
                if isinstance(first_stmt, ast.Expr):
                    # Docstring is an expression with a constant string
                    if isinstance(first_stmt.value, (ast.Constant, ast.Str)):
                        if isinstance(first_stmt.value, ast.Constant):
                            docstring_value = first_stmt.value.value
                        else:  # ast.Str (Python < 3.8)
                            docstring_value = first_stmt.value.s
                        
                        if isinstance(docstring_value, str):
                            start_line = first_stmt.lineno if hasattr(first_stmt, 'lineno') else None
                            if start_line:
                                # Count lines in docstring content
                                docstring_lines = docstring_value.count('\n')
                                end_line = start_line + docstring_lines + 2
                                docstring_ranges.append((start_line, end_line))
            
            # Recursively visit child nodes
            for child in ast.iter_child_nodes(node):
                visit_node(child)
        
        visit_node(tree)
        return docstring_ranges
    
    def _is_in_docstring_or_comment(self, node: ast.AST, content: str, docstring_ranges: List[tuple]) -> bool:
        if not hasattr(node, 'lineno'):
            return False
        
        line_number = node.lineno
        
        for start_line, end_line in docstring_ranges:
            if start_line <= line_number <= end_line:
                return True
        
        lines = content.split('\n')
        if line_number <= len(lines):
            line = lines[line_number - 1].strip()
            if line.startswith('#'):
                return True
            # This is a heuristic - Python doesn't have true multi-line comments, but docstrings can appear as comments
            if line.startswith('"""') or line.startswith("'''"):
                return True
        
        return False

