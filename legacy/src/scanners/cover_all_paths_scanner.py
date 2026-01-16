"""Scanner for validating all behavior paths are covered by tests."""

from typing import List, Dict, Any, Optional
from pathlib import Path
import ast
from .test_scanner import TestScanner
from .violation import Violation
from .resources.ast_elements import Functions


class CoverAllPathsScanner(TestScanner):
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, knowledge_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        # Find all test methods
        functions = Functions(tree)
        test_methods = [function.node for function in functions.get_many_functions if function.node.name.startswith('test_')]
        
        for test_method in test_methods:
            # Check if test has actual code (not just pass/docstrings)
            found_code_node = None
            for stmt in test_method.body:
                if isinstance(stmt, ast.Pass):
                    continue
                elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, (ast.Constant, ast.Str)):
                    # Skip docstrings
                    continue
                else:
                    for node in ast.walk(stmt):
                        if isinstance(node, (ast.Call, ast.Assign, ast.Assert, ast.Return, ast.Raise)):
                            found_code_node = node
                            break
                    # Break outer loop if we found code
                    if found_code_node is not None:
                        break
            
            if found_code_node is None:
                # No code snippet for empty test method violations (method definition line)
                violations.append(Violation(
                    rule=rule_obj,
                    violation_message=f'Test method "{test_method.name}" has no actual test code - tests must exercise behavior paths, not just contain pass statements',
                    location=str(file_path),
                    line_number=test_method.lineno,
                    severity='error'
                ).to_dict())
        
        return violations

