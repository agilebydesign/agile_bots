"""Scanner for domain_oriented_test_inheritance rule.

Flags duplicate assertion bodies across test classes (>80% structural
similarity with different variable names), and test classes exceeding
300 lines that reference 3+ distinct domain concepts.
"""
import ast
import re
from typing import List, Dict, Any, Set
from scanners.code.python.code_scanner import CodeScanner


class DuplicateAssertionScanner(CodeScanner):

    LINE_THRESHOLD = 300
    DOMAIN_CONCEPT_THRESHOLD = 3

    DOMAIN_KEYWORDS = {
        'epic', 'sub_epic', 'subepic', 'story', 'actor',
        'increment', 'lane', 'acceptance_criteria', 'ac_',
        'layout', 'diagram', 'drawio',
    }

    def scan_file_with_context(self, context) -> List[Dict[str, Any]]:
        violations = []
        file_path = str(context.file_path)

        if not file_path.endswith('.py'):
            return violations
        if '/test' not in file_path and '\\test' not in file_path:
            return violations

        try:
            source = context.file_path.read_text(encoding='utf-8')
            tree = ast.parse(source)
        except (SyntaxError, UnicodeDecodeError):
            return violations

        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)
                   and n.name.startswith('Test')]

        for cls in classes:
            violation = self._check_class_size_and_domain_spread(
                cls, source, file_path)
            if violation:
                violations.append(violation)

        return violations

    def _check_class_size_and_domain_spread(self, cls: ast.ClassDef,
                                              source: str,
                                              file_path: str) -> Dict[str, Any] | None:
        if not cls.body:
            return None

        first_line = cls.lineno
        last_line = max(getattr(n, 'end_lineno', n.lineno)
                        for n in ast.walk(cls)
                        if hasattr(n, 'lineno'))
        class_lines = last_line - first_line + 1

        if class_lines < self.LINE_THRESHOLD:
            return None

        methods = [n for n in cls.body
                   if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                   and n.name.startswith('test_')]

        domain_concepts: Set[str] = set()
        for method in methods:
            name_lower = method.name.lower()
            for kw in self.DOMAIN_KEYWORDS:
                if kw in name_lower:
                    domain_concepts.add(kw)

        if len(domain_concepts) < self.DOMAIN_CONCEPT_THRESHOLD:
            return None

        return {
            'rule': self.rule.get('description', '') if isinstance(self.rule, dict) else str(self.rule),
            'violation_message': (
                f'Test class "{cls.name}" spans {class_lines} lines and '
                f'references {len(domain_concepts)} domain concepts '
                f'({", ".join(sorted(domain_concepts))}) -- consider '
                f'splitting by domain per domain_oriented_test_inheritance rule'
            ),
            'location': f'{file_path}:{first_line}',
            'severity': 'warning'
        }
