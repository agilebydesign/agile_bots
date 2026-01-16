"""Scanner for validating mutable state is minimized."""

from typing import List, Dict, Any, Optional
from pathlib import Path
import ast
import re
from .code_scanner import CodeScanner
from .violation import Violation


class MinimizeMutableStateScanner(CodeScanner):
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, knowledge_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        violations.extend(self._check_mutable_patterns(lines, file_path, rule_obj))
        
        return violations
    
    def _check_mutable_patterns(self, lines: List[str], file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        mutable_patterns = [
            r'\.push\s*\(',  # Array mutation (JS)
            r'\.pop\s*\(',  # Array mutation (JS/Python)
            r'\.splice\s*\(',  # Array mutation (JS)
            r'\+\+\s*;',  # Increment mutation (JS)
            r'--\s*;',  # Decrement mutation (JS)
            r'=\s*\{.*\}\s*\.\w+\s*=',  # Object mutation
            r'\.append\s*\(',  # List mutation (Python)
            r'\.extend\s*\(',  # List mutation (Python)
            r'\.insert\s*\(',  # List mutation (Python)
            r'\.remove\s*\(',  # List mutation (Python)
            r'\.clear\s*\(',  # List/dict mutation (Python)
            r'\+=\s*1\s*$',  # counter += 1 (Python increment)
            r'-=\s*1\s*$',  # counter -= 1 (Python decrement)
            r'\w+\s*\+\+',  # variable++ (without semicolon, test files)
        ]
        
        for line_num, line in enumerate(lines, 1):
            for pattern in mutable_patterns:
                if re.search(pattern, line):
                    if 'test_' in line.lower() or 'def test' in line.lower():
                        continue
                    
                    # No code snippet for mutation pattern violations
                    violation = Violation(
                        rule=rule_obj,
                        violation_message=f'Line {line_num} mutates state - prefer immutable data structures (create new objects instead of mutating)',
                        location=str(file_path),
                        line_number=line_num,
                        severity='warning'
                    ).to_dict()
                    violations.append(violation)
                    break
        
        return violations

