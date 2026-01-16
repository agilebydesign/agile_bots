from pathlib import Path
from typing import Dict, Any, List


class _MarkdownHelper:
    """Minimal markdown formatting helper for validation output."""
    
    def format_heading(self, text: str, level: int = 1) -> str:
        """Format markdown heading."""
        return f"{'#' * level} {text}"
    
    def format_bold(self, text: str) -> str:
        """Format bold text."""
        return f"**{text}**"


class ValidationViolationsBuilder:

    def __init__(self, format_violation_line_fn):
        self._format_violation_line = format_violation_line_fn
        self._formatter = _MarkdownHelper()

    def build_violations(self, validation_rules: List[Dict[str, Any]]) -> List[str]:
        lines = [self._formatter.format_heading('Violations Found', level=2), '']
        file_by_file_violations_by_rule, cross_file_violations_by_rule = self._organize_violations(validation_rules)
        total_file_by_file = sum((len(v) for v in file_by_file_violations_by_rule.values()))
        total_cross_file = sum((len(v) for v in cross_file_violations_by_rule.values()))
        total_violations = total_file_by_file + total_cross_file
        if total_violations == 0:
            lines.append(f'🟢 {self._formatter.format_bold("No violations found.")} All rules passed validation.')
            lines.append('')
        else:
            lines.append(f'{self._formatter.format_bold("Total Violations:")} {total_violations}')
            lines.append(f'- {self._formatter.format_bold("File-by-File Violations:")} {total_file_by_file}')
            lines.append(f'- {self._formatter.format_bold("Cross-File Violations:")} {total_cross_file}')
            lines.append('')
            if file_by_file_violations_by_rule:
                lines.extend(self._build_violations_by_type(file_by_file_violations_by_rule, 'File-by-File Violations (Pass 1)', 'These violations were detected by scanning each file individually.'))
            if cross_file_violations_by_rule:
                lines.extend(self._build_violations_by_type(cross_file_violations_by_rule, 'Cross-File Violations (Pass 2)', 'These violations were detected by analyzing all files together to find patterns that span multiple files.'))
        return lines

    def _organize_violations(self, validation_rules: List[Dict[str, Any]]) -> tuple:
        file_by_file_violations_by_rule = {}
        cross_file_violations_by_rule = {}
        for rule_dict in validation_rules:
            rule_file = rule_dict.get('rule_file', 'unknown')
            scanner_results = rule_dict.get('scanner_results', {})
            rule_name = Path(rule_file).stem if rule_file else 'unknown'
            if 'file_by_file' in scanner_results or 'cross_file' in scanner_results:
                self._add_structured_violations(scanner_results, rule_name, file_by_file_violations_by_rule, cross_file_violations_by_rule)
            elif 'violations' in scanner_results:
                self._add_legacy_violations(scanner_results, rule_name, file_by_file_violations_by_rule)
        return (file_by_file_violations_by_rule, cross_file_violations_by_rule)

    def _add_structured_violations(self, scanner_results: Dict, rule_name: str, file_by_file_violations_by_rule: Dict, cross_file_violations_by_rule: Dict):
        file_by_file_violations = scanner_results.get('file_by_file', {}).get('violations', [])
        cross_file_violations = scanner_results.get('cross_file', {}).get('violations', [])
        if file_by_file_violations:
            file_by_file_violations_by_rule[rule_name] = file_by_file_violations
        if cross_file_violations:
            cross_file_violations_by_rule[rule_name] = cross_file_violations

    def _add_legacy_violations(self, scanner_results: Dict, rule_name: str, file_by_file_violations_by_rule: Dict):
        violations = scanner_results.get('violations', [])
        if violations:
            file_by_file_violations_by_rule[rule_name] = violations

    def _build_violations_by_type(self, violations_by_rule: Dict[str, List[Dict[str, Any]]], title: str, description: str) -> List[str]:
        lines = [self._formatter.format_heading(title, level=3), '', description, '']
        for rule_name, violations in violations_by_rule.items():
            violations_anchor_id = f"{rule_name.replace('_', '-').lower()}-violations"
            rule_display_name = rule_name.replace('_', ' ').title()
            heading_text = f'<span id="{violations_anchor_id}">{rule_display_name}: {len(violations)} violation(s)</span>'
            lines.append(self._formatter.format_heading(heading_text, level=4))
            lines.append('')
            for violation in violations:
                lines.extend(self._format_violation_line(violation))
            lines.append('')
        return lines
