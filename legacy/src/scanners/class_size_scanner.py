"""Scanner for validating class size (keep classes small)."""

from typing import List, Dict, Any, Optional
from pathlib import Path
import ast
import logging
from .code_scanner import CodeScanner
from .violation import Violation
from .complexity_metrics import ComplexityMetrics
from .resources.ast_elements import Classes

logger = logging.getLogger(__name__)


class ClassSizeScanner(CodeScanner):
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, knowledge_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        classes = Classes(tree)
        for cls in classes.get_many_classes:
            violation = self._check_class_size(cls.node, file_path, rule_obj, content)
            if violation:
                violations.append(violation)
        
        return violations
    
    def _check_class_size(self, class_node: ast.ClassDef, file_path: Path, rule_obj: Any, content: str) -> Optional[Dict[str, Any]]:
        violations = []
        
        # 1. Line count (existing check)
        if hasattr(class_node, 'end_lineno') and class_node.end_lineno:
            class_size = class_node.end_lineno - class_node.lineno + 1
        else:
            class_size = len(class_node.body) * 10
        
        if class_size > 300:
            line_number = class_node.lineno if hasattr(class_node, 'lineno') else None
            violations.append(self._create_violation_with_snippet(
                rule_obj=rule_obj,
                violation_message=f'Class "{class_node.name}" is {class_size} lines - should be under 300 lines (extract related methods into separate classes)',
                file_path=file_path,
                line_number=line_number,
                severity='warning',
                content=content,
                ast_node=class_node,
                max_lines=10
            ))
        
        # 2. LCOM (Lack of Cohesion of Methods) - measures single responsibility via shared attributes
        # DISABLED: LCOM calculation commented out - not effective enough
        # Threshold 0.8 because LCOM now excludes simple getters and follows delegation
        # lcom = ComplexityMetrics.calculate_lcom(class_node)
        # if lcom > 0.8:
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
        
        # 3. Method count - DISABLED per user request
        # method_count = len([n for n in class_node.body if isinstance(n, ast.FunctionDef)])
        # if method_count > 15:
        #     line_number = class_node.lineno if hasattr(class_node, 'lineno') else None
        #     violations.append(Violation(
        #         rule=rule_obj,
        #         violation_message=(
        #             f'Class "{class_node.name}" has {method_count} methods - '
        #             f'consider if it has multiple responsibilities and should be split.'
        #         ),
        #         location=str(file_path),
        #         line_number=line_number,
        #         severity='info'
        #     ).to_dict())
        
        return violations[0] if violations else None

