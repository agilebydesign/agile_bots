from pathlib import Path
from typing import Dict, Any, List
from ..actions.validate.validation_stats import ValidationStats

MAX_VIOLATION_DENSITY_FOR_GOOD_STATUS = 200
MAX_RULES_WITH_ERRORS_FOR_GOOD_STATUS = 5

class ScannerStatusFormatter:

    def __init__(self, check_violation_severities_fn, rule_name_to_anchor_fn):
        self.check_violation_severities = check_violation_severities_fn
        self.rule_name_to_anchor = rule_name_to_anchor_fn

    def build_scanner_status(self, validation_rules: List[Dict[str, Any]]) -> List[str]:
        lines = ['## Scanner Execution Status', '']
        categorized = self.categorize_scanner_rules(validation_rules)
        stats = self.build_scanner_stats(validation_rules, categorized)
        lines.extend(self.build_status_summary(stats))
        lines.append('')
        lines.extend(self.format_executed_rules_section(categorized['executed']))
        lines.extend(self.format_failed_rules_section(categorized['load_failed'], 'Scanner Load Failures', 'LOAD FAILED'))
        lines.extend(self.format_failed_rules_section(categorized['execution_failed'], 'Scanner Execution Failures', 'EXECUTION FAILED'))
        lines.extend(self.format_no_scanner_rules_section(categorized['no_scanner']))
        return lines

    def categorize_scanner_rules(self, validation_rules: List[Dict[str, Any]]) -> Dict:
        executed_rules = []
        load_failed_rules = []
        execution_failed_rules = []
        no_scanner_rules = []
        for rule_dict in validation_rules:
            category = self._get_rule_category(rule_dict)
            if category == 'executed':
                executed_rules.append(self._build_executed_rule_entry(rule_dict))
            elif category == 'load_failed':
                load_failed_rules.append(self._build_failed_rule_entry(rule_dict))
            elif category == 'execution_failed':
                execution_failed_rules.append(self._build_failed_rule_entry(rule_dict))
            elif category == 'no_scanner':
                no_scanner_rules.append(self._get_rule_file(rule_dict))
        return {'executed': executed_rules, 'load_failed': load_failed_rules, 'execution_failed': execution_failed_rules, 'no_scanner': no_scanner_rules}

    def _get_rule_category(self, rule_dict: Dict) -> str:
        scanner_status = rule_dict.get('scanner_status', {})
        status = scanner_status.get('status', 'UNKNOWN')
        
        if status == 'EXECUTED':
            return 'executed'
        if status == 'LOAD_FAILED':
            return 'load_failed'
        if status == 'EXECUTION_FAILED':
            return 'execution_failed'
        if status == 'NO_SCANNER':
            return 'no_scanner'
        return 'no_scanner'
    
    def _get_rule_file(self, rule_dict: Dict) -> str:
        return rule_dict.get('rule_file', 'unknown')
    
    def _build_executed_rule_entry(self, rule_dict: Dict) -> Dict:
        rule_file = self._get_rule_file(rule_dict)
        scanner_status = rule_dict.get('scanner_status', {})
        return self.build_executed_rule_info(rule_dict, rule_file, scanner_status)
    
    def _build_failed_rule_entry(self, rule_dict: Dict) -> Dict:
        rule_file = self._get_rule_file(rule_dict)
        scanner_status = rule_dict.get('scanner_status', {})
        return self._build_failed_rule_info(rule_file, scanner_status)

    def _build_failed_rule_info(self, rule_file: str, scanner_status: Dict) -> Dict:
        return {'rule': rule_file, 'scanner_path': scanner_status.get('scanner_path', 'unknown'), 'error': scanner_status.get('error', 'Unknown error')}

    def build_executed_rule_info(self, rule_dict: Dict, rule_file: str, scanner_status: Dict) -> Dict:
        violations = scanner_status.get('violations_found', 0)
        exec_status = scanner_status.get('execution_status', 'SUCCESS')
        scanner_results = rule_dict.get('scanner_results', {})
        has_errors, has_warnings = self.check_violation_severities(scanner_results)
        return {'rule': rule_file, 'violations': violations, 'execution_status': exec_status, 'scanner_path': scanner_status.get('scanner_path', 'unknown'), 'has_errors': has_errors, 'has_warnings': has_warnings}

    def build_scanner_stats(self, validation_rules: List[Dict], categorized: Dict) -> ValidationStats:
        executed = categorized['executed']
        total_with_scanners = len(executed) + len(categorized['load_failed']) + len(categorized['execution_failed'])
        total_violations = sum(r['violations'] for r in executed)
        rules_clean = sum(1 for r in executed if r['violations'] == 0 and not r['has_errors'] and not r['has_warnings'])
        rules_with_warnings = sum(1 for r in executed if r['has_warnings'] and not r['has_errors'])
        rules_with_errors = sum(1 for r in executed if r['has_errors'])
        return ValidationStats(total_rules=len(validation_rules), total_with_scanners=total_with_scanners, executed_count=len(executed), load_failed_count=len(categorized['load_failed']), execution_failed_count=len(categorized['execution_failed']), no_scanner_count=len(categorized['no_scanner']), total_violations=total_violations, rules_clean=rules_clean, rules_with_warnings=rules_with_warnings, rules_with_errors=rules_with_errors, executed_rules=executed)

    def format_executed_rules_section(self, executed_rules: List[Dict]) -> List[str]:
        if not executed_rules:
            return []
        lines = ['### 🟩 Successfully Executed Scanners', '']
        executed_rules.sort(key=lambda x: (-x['violations'], x['rule']))
        for rule_info in executed_rules:
            lines.extend(self.format_executed_rule_line(rule_info))
        lines.append('')
        return lines

    def format_executed_rule_line(self, rule_info: Dict) -> List[str]:
        violations = rule_info['violations']
        rule_name = Path(rule_info['rule']).stem if rule_info['rule'] else 'unknown'
        status_indicator, status_text = self.get_rule_status_indicator(rule_info, violations)
        violations_text = f'{violations} violation(s)' if violations > 0 else '0 violations'
        exec_status = rule_info.get('execution_status', 'SUCCESS')
        anchor_link = self.rule_name_to_anchor(rule_name)
        rule_display_name = rule_name.replace('_', ' ').title()
        details_link = self.build_details_link(rule_name, violations)
        status_suffix = f'({exec_status})' if exec_status != 'SUCCESS' else f'({status_text})'
        return [f'- {status_indicator} **[{rule_display_name}]({anchor_link})** - {violations_text} {status_suffix}{details_link}', f"  - Scanner: `{rule_info['scanner_path']}`"]

    def get_rule_status_indicator(self, rule_info: Dict, violations: int) -> tuple:
        if rule_info['has_errors']:
            return ('🟥', 'ERRORS')
        if rule_info['has_warnings']:
            return ('🟨', 'WARNINGS')
        if violations == 0:
            return ('🟩', 'CLEAN')
        return ('🟨', 'VIOLATIONS')

    def build_details_link(self, rule_name: str, violations: int) -> str:
        if violations <= 0:
            return ''
        violations_anchor = f"#{rule_name.replace('_', '-').lower()}-violations"
        return f' - [View Details]({violations_anchor})'

    def format_failed_rules_section(self, failed_rules: List[Dict], title: str, status: str) -> List[str]:
        if not failed_rules:
            return []
        lines = [f'### 🟥 {title}', '']
        for rule_info in failed_rules:
            rule_name = Path(rule_info['rule']).stem if rule_info['rule'] else 'unknown'
            anchor_link = self.rule_name_to_anchor(rule_name)
            rule_display_name = rule_name.replace('_', ' ').title()
            lines.append(f'- 🟥 **[{rule_display_name}]({anchor_link})** - {status}')
            lines.append(f"  - Scanner Path: `{rule_info['scanner_path']}`")
            lines.append(f"  - Error: `{rule_info['error']}`")
        lines.append('')
        return lines

    def format_no_scanner_rules_section(self, no_scanner_rules: List[str]) -> List[str]:
        if not no_scanner_rules:
            return []
        lines = ['### <span style="color: gray;">[i] Rules Without Scanners</span>', '']
        for rule_file in no_scanner_rules[:10]:
            rule_name = Path(rule_file).stem if rule_file else 'unknown'
            anchor_link = self.rule_name_to_anchor(rule_name)
            rule_display_name = rule_name.replace('_', ' ').title()
            lines.append(f'- <span style="color: gray;">[i]</span> **[{rule_display_name}]({anchor_link})** - No scanner configured')
        if len(no_scanner_rules) > 10:
            lines.append(f'- *... and {len(no_scanner_rules) - 10} more rules without scanners*')
        lines.append('')
        return lines

    def build_status_summary(self, stats: ValidationStats) -> List[str]:
        overall_status, overall_text = self.get_overall_status(stats)
        lines = [f'### {overall_status} Overall Status: {overall_text}', '', '| Status | Count | Description |', '|--------|-------|-------------|']
        lines.extend(self.build_summary_table_rows(stats))
        lines.extend(self.build_totals_summary(stats))
        return lines

    def get_overall_status(self, stats: ValidationStats) -> tuple:
        if self._has_critical_issues(stats):
            return ('🟥', 'CRITICAL ISSUES')
        if not stats.has_violations:
            return ('🟩', 'ALL CLEAN')
        return self._get_violation_status(stats)

    def _has_critical_issues(self, stats: ValidationStats) -> bool:
        return stats.execution_failed_count > 0 or stats.load_failed_count > 2

    def _get_violation_status(self, stats: ValidationStats) -> tuple:
        violation_density = stats.total_violations
        if violation_density < 150 and stats.rules_with_errors == 0:
            return ('🟩', 'HEALTHY')
        if violation_density < MAX_VIOLATION_DENSITY_FOR_GOOD_STATUS and stats.rules_with_errors <= MAX_RULES_WITH_ERRORS_FOR_GOOD_STATUS:
            return ('🟨', 'GOOD - Minor Issues')
        if stats.rules_with_errors > 0:
            return ('🟨', 'NEEDS ATTENTION')
        return ('🟨', 'WARNINGS FOUND')

    def build_summary_table_rows(self, stats: ValidationStats) -> List[str]:
        lines = []
        self._add_executed_row(lines, stats)
        self._add_clean_rules_row(lines, stats)
        self._add_warnings_row(lines, stats)
        self._add_errors_row(lines, stats)
        self._add_failed_rows(lines, stats)
        lines.append('')
        return lines

    def _add_executed_row(self, lines: List[str], stats: ValidationStats) -> None:
        if stats.executed_count > 0:
            desc = 'ran without errors' if stats.rules_clean > 0 else 'executed'
            lines.append(f'| 🟩 Executed Successfully | {stats.executed_count} | Scanners {desc} |')

    def _add_clean_rules_row(self, lines: List[str], stats: ValidationStats) -> None:
        if stats.rules_clean > 0:
            lines.append(f'| 🟩 Clean Rules | {stats.rules_clean} | No violations found |')

    def _add_warnings_row(self, lines: List[str], stats: ValidationStats) -> None:
        if stats.rules_with_warnings > 0:
            warning_count = sum((r['violations'] for r in stats.executed_rules if r.get('has_warnings') and (not r.get('has_errors'))))
            lines.append(f'| 🟨 Rules with Warnings | {stats.rules_with_warnings} | Found {warning_count} warning violation(s) |')

    def _add_errors_row(self, lines: List[str], stats: ValidationStats) -> None:
        if stats.rules_with_errors > 0:
            error_count = sum((r['violations'] for r in stats.executed_rules if r.get('has_errors')))
            lines.append(f'| 🟥 Rules with Errors | {stats.rules_with_errors} | Found {error_count} error violation(s) |')

    def _add_failed_rows(self, lines: List[str], stats: ValidationStats) -> None:
        if stats.load_failed_count > 0:
            lines.append(f'| 🟥 Load Failed | {stats.load_failed_count} | Scanner could not be loaded |')
        if stats.execution_failed_count > 0:
            lines.append(f'| 🟥 Execution Failed | {stats.execution_failed_count} | Scanner crashed during execution |')
        if stats.no_scanner_count > 0:
            lines.append(f'| [i] No Scanner | {stats.no_scanner_count} | Rule has no scanner configured |')

    def build_totals_summary(self, stats: ValidationStats) -> List[str]:
        lines = [f'**Total Rules:** {stats.total_rules}', f'- **Rules with Scanners:** {stats.total_with_scanners}', f'  - 🟩 **Executed Successfully:** {stats.executed_count}']
        if stats.load_failed_count > 0:
            lines.append(f'  - 🟥 **Load Failed:** {stats.load_failed_count}')
        if stats.execution_failed_count > 0:
            lines.append(f'  - 🟥 **Execution Failed:** {stats.execution_failed_count}')
        if stats.no_scanner_count > 0:
            lines.append(f'- [i] **Rules without Scanners:** {stats.no_scanner_count}')
        return lines

