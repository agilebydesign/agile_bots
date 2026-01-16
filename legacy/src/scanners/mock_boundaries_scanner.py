"""Scanner for validating mocks are only for external boundaries."""

from typing import List, Dict, Any, Optional
from pathlib import Path
import ast
import re
from .test_scanner import TestScanner
from .violation import Violation


class MockBoundariesScanner(TestScanner):
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, knowledge_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        violations.extend(self._check_mock_usage(content, file_path, rule_obj))
        
        return violations
    
    def _check_mock_usage(self, content: str, file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        lines = content.split('\n')
        
        mock_patterns = [
            r'@patch\s*\(',  # Python unittest.mock.patch
            r'@mock\.',  # Python mock decorator
            r'Mock\s*\(',  # Mock() constructor
            r'mock\.',  # mock. calls
            r'@pytest\.fixture.*mock',  # pytest mock fixtures
        ]
        
        # Internal code patterns (shouldn't be mocked)
        internal_patterns = [
            r'mock.*\b(validate|calculate|process|format|parse)\b',  # Internal business logic
            r'mock.*\b(helper|util|common|shared)\b',  # Internal helpers
        ]
        
        for line_num, line in enumerate(lines, 1):
            has_mock = any(re.search(pattern, line, re.IGNORECASE) for pattern in mock_patterns)
            
            if has_mock:
                is_internal = any(re.search(pattern, line, re.IGNORECASE) for pattern in internal_patterns)
                
                if is_internal:
                    violation = Violation(
                        rule=rule_obj,
                        violation_message=f'Line {line_num} mocks internal code - mocks should only be used for external boundaries (APIs, databases, file systems)',
                        location=str(file_path),
                        line_number=line_num,
                        severity='error'
                    ).to_dict()
                    violations.append(violation)
        
        return violations

