"""Scanner for validating consistent naming across codebase."""

from typing import List, Dict, Any, Optional
from pathlib import Path
import ast
import logging
from .code_scanner import CodeScanner
from .violation import Violation
from collections import defaultdict
from .resources.ast_elements import Functions, Classes

logger = logging.getLogger(__name__)


class ConsistentNamingScanner(CodeScanner):
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, knowledge_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        function_names = []
        class_names = []
        
        functions = Functions(tree)
        for function in functions.get_many_functions:
            # Skip private methods and special methods
            if not (function.node.name.startswith('_') and function.node.name != '__init__'):
                function_names.append(function.node.name)
        
        classes = Classes(tree)
        for cls in classes.get_many_classes:
            class_names.append(cls.node.name)
        
        # Classes often use PascalCase while functions use snake_case - that's OK
        violations.extend(self._check_naming_consistency(function_names, class_names, file_path, rule_obj))
        
        return violations
    
    def _check_naming_consistency(self, function_names: List[str], class_names: List[str], file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        if not function_names:
            return violations
        
        # Python convention: functions use snake_case, classes use PascalCase
        has_snake_case = any('_' in name for name in function_names)
        has_camel_case = any(name[0].isupper() and '_' not in name for name in function_names if name)
        
        # Only flag if there's a significant mix (more than 1 camelCase function)
        camel_case_count = sum(1 for name in function_names if name and name[0].isupper() and '_' not in name)
        
        if has_snake_case and camel_case_count > 1:
            violation = Violation(
                rule=rule_obj,
                violation_message=f'File mixes snake_case and camelCase naming conventions ({camel_case_count} camelCase functions) - use consistent naming style (snake_case for functions)',
                location=str(file_path),
                severity='warning'
            ).to_dict()
            violations.append(violation)
        
        return violations

