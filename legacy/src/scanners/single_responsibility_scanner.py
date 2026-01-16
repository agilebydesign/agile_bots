"""Scanner for validating single responsibility principle."""

from typing import List, Dict, Any, Optional
from pathlib import Path
import ast
import re
import logging
from .code_scanner import CodeScanner
from .violation import Violation
from .complexity_metrics import ComplexityMetrics
from .resources.ast_elements import Functions

logger = logging.getLogger(__name__)


class SingleResponsibilityScanner(CodeScanner):
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, knowledge_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        functions = Functions(tree)
        for function in functions.get_many_functions:
            violation = self._check_function_sr(function.node, file_path, rule_obj)
            if violation:
                violations.append(violation)
        
        return violations
    
    def _check_function_sr(self, func_node: ast.FunctionDef, file_path: Path, rule_obj: Any) -> Optional[Dict[str, Any]]:
        func_name = func_node.name.lower()
        
        # Skip test helper functions (even if they somehow got through)
        if func_name.startswith(('given_', 'when_', 'then_', 'test_')):
            return None
        
        violations = []
        
        # 1. Check name patterns (existing logic)
        name_violation = self._check_name_patterns(func_node, file_path, rule_obj)
        if name_violation:
            violations.append(name_violation)
        
        # 2. AST-based responsibility detection - DISABLED
        # The detect_responsibilities heuristic was too aggressive - it flagged 
        # implementation details (I/O, path math, assignments) as separate "responsibilities"
        # when they're really just steps in accomplishing ONE responsibility.
        # Example: A template class that loads from file was flagged for:
        #   - I/O (read_json_file)
        #   - Computation (path / filename)  
        #   - Transformation (storing result)
        # But these are all ONE responsibility: "manage template".
        # 
        # For real SRP violations, use:
        # - LCOM metric (low cohesion = methods don't share attributes)
        # - Name pattern detection ("validate_and_save" = two responsibilities)
        # - Manual review
        
        return violations[0] if violations else None
    
    def _check_name_patterns(self, func_node: ast.FunctionDef, file_path: Path, rule_obj: Any) -> Optional[Dict[str, Any]]:
        func_name = func_node.name.lower()
        
        action_verbs = [
            'validate', 'save', 'load', 'process', 'send', 'create', 'update', 'delete',
            'calculate', 'compute', 'transform', 'convert', 'parse', 'format', 'render',
            'execute', 'run', 'invoke', 'call', 'fetch', 'retrieve', 'store', 'write',
            'read', 'parse', 'build', 'generate', 'compile', 'extract', 'merge', 'split'
        ]
        
        verbs_pattern = '|'.join(action_verbs)
        for verb in action_verbs:
            pattern = rf'\b{verb}_and_({verbs_pattern})\b'
            if re.search(pattern, func_name):
                line_number = func_node.lineno if hasattr(func_node, 'lineno') else None
                try:
                    content = file_path.read_text(encoding='utf-8')
                    return self._create_violation_with_snippet(
                        rule_obj=rule_obj,
                        violation_message=f'Function "{func_node.name}" appears to have multiple responsibilities - split into separate functions',
                        file_path=file_path,
                        line_number=line_number,
                        severity='warning',
                        content=content,
                        ast_node=func_node,
                        max_lines=5
                    )
                except Exception:
                    return Violation(
                        rule=rule_obj,
                        violation_message=f'Function "{func_node.name}" appears to have multiple responsibilities - split into separate functions',
                        location=str(file_path),
                        line_number=line_number,
                        severity='warning'
                    ).to_dict()
        
        camel_case_pattern = r'([a-z]+)And([A-Z][a-z]+)'
        match = re.search(camel_case_pattern, func_node.name)
        if match:
            verb1 = match.group(1).lower()
            verb2 = match.group(2).lower()
            if verb1 in action_verbs and verb2 in action_verbs:
                line_number = func_node.lineno if hasattr(func_node, 'lineno') else None
                try:
                    content = file_path.read_text(encoding='utf-8')
                    return self._create_violation_with_snippet(
                        rule_obj=rule_obj,
                        violation_message=f'Function "{func_node.name}" appears to have multiple responsibilities - split into separate functions',
                        file_path=file_path,
                        line_number=line_number,
                        severity='warning',
                        content=content,
                        ast_node=func_node,
                        max_lines=5
                    )
                except Exception:
                    return Violation(
                        rule=rule_obj,
                        violation_message=f'Function "{func_node.name}" appears to have multiple responsibilities - split into separate functions',
                        location=str(file_path),
                        line_number=line_number,
                        severity='warning'
                    ).to_dict()
        
        return None
    
    def _check_class_sr(self, class_node: ast.ClassDef, file_path: Path, rule_obj: Any) -> Optional[Dict[str, Any]]:
        violations = []
        
        # 1. Method count - DISABLED per user request
        # method_count = len([n for n in class_node.body if isinstance(n, ast.FunctionDef)])
        # if method_count > 15:
        #     line_number = class_node.lineno if hasattr(class_node, 'lineno') else None
        #     violations.append(Violation(
        #         rule=rule_obj,
        #         violation_message=f'Class "{class_node.name}" has {method_count} methods - consider if it has multiple responsibilities',
        #         location=str(file_path),
        #         line_number=line_number,
        #         severity='info'
        #     ).to_dict())
        
        # 2. LCOM (Lack of Cohesion of Methods) - measures how related methods are
        # DISABLED: LCOM calculation commented out - not effective enough
        # Threshold raised to 0.8 because LCOM now excludes simple getters and follows delegation
        # lcom = ComplexityMetrics.calculate_lcom(class_node)
        # if lcom > 0.8:  # Low cohesion threshold
        #     line_number = class_node.lineno if hasattr(class_node, 'lineno') else None
        #     violations.append(Violation(
        #         rule=rule_obj,
        #         violation_message=(
        #             f'Class "{class_node.name}" has low cohesion (LCOM={lcom:.2f}) - '
        #             f'methods don\'t share many attributes, suggesting multiple responsibilities. '
        #             f'Consider splitting into separate classes.'
        #         ),
        #         location=str(file_path),
        #         line_number=line_number,
        #         severity='warning'
        #     ).to_dict())
        
        # 3. Responsibility detection - DISABLED
        # Same issue as function detection - flagging implementation details
        # (I/O, path math, assignments) as separate "responsibilities" when
        # they're really just steps in ONE responsibility.
        # Keep LCOM (above) which actually measures method cohesion.
        
        return violations[0] if violations else None
    
    def _format_responsibility_examples(self, responsibilities: dict) -> str:
        lines = []
        for resp_type, examples in sorted(responsibilities.items()):
            if examples:
                first_example = examples[0]
                line_num = first_example.get('line', '?')
                code = first_example.get('code', '')
                lines.append(f"**{resp_type}** (line {line_num}):\n```python\n{code}\n```")
        return '\n\n'.join(lines)
    
    def _format_class_responsibility_examples(self, responsibilities: dict) -> str:
        lines = []
        for resp_type, examples in sorted(responsibilities.items()):
            if examples:
                first_example = examples[0]
                method_name = first_example.get('method', '?')
                line_num = first_example.get('line', '?')
                code = first_example.get('code', '')
                lines.append(f"**{resp_type}** in `{method_name}()` (line {line_num}):\n```python\n{code}\n```")
        return '\n\n'.join(lines)

