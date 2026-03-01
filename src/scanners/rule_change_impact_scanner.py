
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from pathlib import Path
import json
from scanners.scanner import Scanner
from scanners.violation import Violation
from scanners.eval_paths import EvalPaths

if TYPE_CHECKING:
    from scanners.resources.scan_context import ScanFilesContext


class RuleChangeImpactScanner(Scanner):

    def scan_with_context(self, context: 'ScanFilesContext') -> List[Dict[str, Any]]:
        paths = EvalPaths(self.rule.rule_file_path)
        if not paths.workspace_root:
            return []

        baseline = self._load_baseline(paths)
        if baseline is None:
            return [
                Violation(
                    rule=self.rule,
                    violation_message='No baseline found. Run validate with --save-baseline to create one before changing rules.',
                    location=str(paths.baseline_path),
                    severity='info'
                ).to_dict()
            ]

        current = self._collect_current_violations(context)
        return self._diff_violations(baseline, current, paths)

    def _load_baseline(self, paths: EvalPaths) -> Optional[List[Dict[str, Any]]]:
        bp = paths.baseline_path
        if not bp.exists():
            return None
        try:
            with open(bp, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('violations', [])
        except (json.JSONDecodeError, IOError):
            return None

    def _collect_current_violations(self, context: 'ScanFilesContext') -> List[Dict[str, Any]]:
        return []

    def _diff_violations(
        self,
        baseline: List[Dict[str, Any]],
        current: List[Dict[str, Any]],
        paths: EvalPaths,
    ) -> List[Dict[str, Any]]:
        baseline_keys = {self._violation_key(v) for v in baseline}
        current_keys = {self._violation_key(v) for v in current}

        violations = []

        for v in current:
            if self._violation_key(v) in (current_keys - baseline_keys):
                violations.append(
                    Violation(
                        rule=self.rule,
                        violation_message=f'NEW after rule change: {v.get("violation_message", "unknown")}',
                        location=v.get('location', 'unknown'),
                        severity='info'
                    ).to_dict()
                )

        for v in baseline:
            if self._violation_key(v) in (baseline_keys - current_keys):
                violations.append(
                    Violation(
                        rule=self.rule,
                        violation_message=f'RESOLVED by rule change: {v.get("violation_message", "unknown")}',
                        location=v.get('location', 'unknown'),
                        severity='info'
                    ).to_dict()
                )

        if not violations and baseline:
            violations.append(
                Violation(
                    rule=self.rule,
                    violation_message=f'No impact detected. Baseline has {len(baseline)} violations, current has {len(current)}.',
                    location=str(paths.baseline_path),
                    severity='info'
                ).to_dict()
            )

        return violations

    @staticmethod
    def _violation_key(v: Dict[str, Any]) -> str:
        rule = v.get('rule', '')
        msg = v.get('violation_message', '')
        loc = v.get('location', '')
        return f'{rule}|{loc}|{msg}'

    @staticmethod
    def save_baseline(workspace_root: Path, violations: List[Dict[str, Any]]) -> Path:
        eval_dir = workspace_root / 'eval'
        eval_dir.mkdir(exist_ok=True)
        baseline_path = eval_dir / 'baseline_violations.json'
        data = {
            'violations': violations,
            'count': len(violations),
        }
        with open(baseline_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return baseline_path
