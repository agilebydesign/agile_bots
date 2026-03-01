
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from pathlib import Path
import json
from scanners.scanner import Scanner
from scanners.violation import Violation

if TYPE_CHECKING:
    from scanners.resources.scan_context import ScanFilesContext


class ClarificationCompletenessScanner(Scanner):

    PLACEHOLDER_MARKERS = [
        '[!] NOT ENOUGH INFORMATION',
        'REQUIRES USER INPUT',
        'TODO',
        'TBD',
    ]

    def scan_with_context(self, context: 'ScanFilesContext') -> List[Dict[str, Any]]:
        behavior_dir = self._get_behavior_dir()
        if not behavior_dir:
            return []

        workspace_root = self._get_workspace_root(behavior_dir)
        if not workspace_root:
            return []

        behavior_name = behavior_dir.name
        expected_questions = self._load_expected_questions(behavior_dir)
        actual_answers = self._load_actual_answers(workspace_root, behavior_name)

        violations = []
        violations.extend(self._check_missing_answers(expected_questions, actual_answers))
        violations.extend(self._check_placeholder_answers(expected_questions, actual_answers))
        violations.extend(self._check_orphaned_answers(expected_questions, actual_answers))
        return violations

    def _get_behavior_dir(self) -> Optional[Path]:
        rule_path = self.rule.rule_file_path
        if not rule_path:
            return None
        return rule_path.parent.parent

    def _get_workspace_root(self, behavior_dir: Path) -> Optional[Path]:
        current = behavior_dir
        for _ in range(10):
            current = current.parent
            if (current / 'docs' / 'story').is_dir():
                return current
            if current == current.parent:
                break
        return None

    def _load_expected_questions(self, behavior_dir: Path) -> List[str]:
        key_questions_path = behavior_dir / 'guardrails' / 'required_context' / 'key_questions.json'
        if not key_questions_path.exists():
            return []
        try:
            with open(key_questions_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('questions', [])
        except (json.JSONDecodeError, IOError):
            return []

    def _load_actual_answers(self, workspace_root: Path, behavior_name: str) -> Dict[str, str]:
        clarification_path = workspace_root / 'docs' / 'story' / 'clarification.json'
        if not clarification_path.exists():
            return {}
        try:
            with open(clarification_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            behavior_data = data.get(behavior_name, {})
            return behavior_data.get('key_questions', {}).get('answers', {})
        except (json.JSONDecodeError, IOError):
            return {}

    def _check_missing_answers(
        self, expected: List[str], actual: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        violations = []
        actual_keys_lower = {k.lower(): k for k in actual}

        for question in expected:
            if question not in actual and question.lower() not in actual_keys_lower:
                violations.append(
                    Violation(
                        rule=self.rule,
                        violation_message=f'Key question not answered: "{self._truncate(question, 80)}"',
                        location='clarification.json',
                        severity='error'
                    ).to_dict()
                )
        return violations

    def _check_placeholder_answers(
        self, expected: List[str], actual: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        violations = []
        for question in expected:
            answer = actual.get(question, '')
            if not answer:
                continue

            if not answer.strip():
                violations.append(
                    Violation(
                        rule=self.rule,
                        violation_message=f'Key question has empty answer: "{self._truncate(question, 80)}"',
                        location='clarification.json',
                        severity='warning'
                    ).to_dict()
                )
                continue

            answer_upper = answer.upper()
            for marker in self.PLACEHOLDER_MARKERS:
                if marker in answer_upper:
                    violations.append(
                        Violation(
                            rule=self.rule,
                            violation_message=f'Key question needs user input: "{self._truncate(question, 80)}" (contains "{marker}")',
                            location='clarification.json',
                            severity='warning'
                        ).to_dict()
                    )
                    break

        return violations

    def _check_orphaned_answers(
        self, expected: List[str], actual: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        violations = []
        expected_lower = {q.lower() for q in expected}
        for question in actual:
            if question.lower() not in expected_lower:
                violations.append(
                    Violation(
                        rule=self.rule,
                        violation_message=f'Orphaned answer not in guardrails template: "{self._truncate(question, 80)}"',
                        location='clarification.json',
                        severity='info'
                    ).to_dict()
                )
        return violations

    @staticmethod
    def _truncate(text: str, max_len: int) -> str:
        if len(text) <= max_len:
            return text
        return text[:max_len - 3] + '...'
