import logging
import re
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from urllib.parse import quote
from bot_path import BotPath
from actions.validate.validation_report_builder import ValidationReportBuilder
from actions.validate.validation_report_formatter import ValidationReportFormatter
from scanners.scanner_status_formatter import ScannerStatusFormatter
from scanners.validation_scanner_status_builder import ValidationScannerStatusBuilder
from actions.validate.file_link_builder import FileLinkBuilder
from actions.validate.violation_formatter import ViolationFormatter
logger = logging.getLogger(__name__)

def ensure_reports_directory(bot_paths: BotPath, workspace_directory: Path) -> Path:
    docs_path = bot_paths.documentation_path
    docs_dir = workspace_directory / docs_path / 'reports'
    docs_dir.mkdir(parents=True, exist_ok=True)
    return docs_dir

class StreamingValidationReportWriter:

    def __init__(self, behavior_name: str, bot_paths: BotPath, timestamp: str = None):
        self.behavior_name = behavior_name
        self.bot_paths = bot_paths
        self.workspace_directory = bot_paths.workspace_directory
        self._timestamp = timestamp or datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self._status_file = None
        self._files_scanned: Dict[str, List[Path]] = {}
        self._scanner_results: List[Dict[str, Any]] = []
        self._total_violations = 0
        self._executed_count = 0
        self._current_rule_name = ''
        self._total_files = 0
        self._files_processed = 0
        self._status_path = ''

    def start(self, files: Dict[str, List[Path]]) -> None:
        self._files_scanned = files
        self._status_path = self._get_status_path()
        Path(self._status_path).parent.mkdir(parents=True, exist_ok=True)
        self._status_file = open(self._status_path, 'w', encoding='utf-8')
        test_files = files.get('test', [])
        src_files = files.get('src', [])
        total_files = len(src_files) + len(test_files)
        self._write_line(f'# Validation Status - {self.behavior_name}')
        self._write_line(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self._write_line(f'Files: {total_files}')
        self._write_line('')
        self._flush()
        print(f'\n[VALIDATION] Scanning {total_files} file(s) in scope...', file=sys.stderr)
        sys.stderr.flush()

    def on_scanner_start(self, rule_file: str, scanner_path: str) -> None:
        self._current_rule_name = Path(rule_file).stem if rule_file else 'unknown'
        print(f'[SCANNING] {self._current_rule_name}', file=sys.stderr, end='', flush=True)

    def on_file_scanned(self, file_path: 'Path', violations: List[Dict[str, Any]], rule_obj: Any) -> None:
        print('.', file=sys.stderr, end='', flush=True)
        if not violations:
            return
        self._total_violations += len(violations)
        file_name = file_path.name if file_path else 'unknown'
        rule_name = rule_obj.name if rule_obj else self._current_rule_name
        self._write_file_violations_header(rule_name, file_name, len(violations))
        self._write_violations(violations)
        self._write_line('---')
        self._write_line('')
        self._flush()

    def _write_file_violations_header(self, rule_name: str, file_name: str, count: int) -> None:
        self._write_line(f'## {rule_name}')
        self._write_line(f'**{file_name}** - {count} violation(s)')
        self._write_line('')

    def _write_violations(self, violations: List) -> None:
        for violation in violations:
            self._write_single_violation(violation)

    def _extract_violation_fields(self, violation) -> tuple:
        if hasattr(violation, 'violation_message'):
            message = violation.violation_message
            severity = violation.severity
            line_number = violation.line_number
        else:
            message = violation.get('violation_message', 'No message')
            severity = violation.get('severity', 'error')
            line_number = violation.get('line_number')
        return (message, severity, line_number)

    def _write_single_violation(self, violation) -> None:
        message, severity, line_number = self._extract_violation_fields(violation)
        severity_icon = '[X]' if severity == 'error' else '[!]' if severity == 'warning' else '[i]'
        line_info = f' (line {line_number})' if line_number else ''
        self._write_line(f'{severity_icon} {severity.upper()}{line_info}')
        self._write_line(f'{message}')
        self._write_line('')

    def on_scanner_complete(self, rule_result: Dict[str, Any]) -> None:
        self._scanner_results.append(rule_result)
        scanner_status = rule_result.get('scanner_status', {})
        status = scanner_status.get('status', 'UNKNOWN')
        if status == 'EXECUTED':
            self._handle_executed_status(scanner_status, rule_result)
        elif status == 'LOAD_FAILED':
            print(f' [LOAD FAILED]', file=sys.stderr, flush=True)
        elif status == 'EXECUTION_FAILED':
            print(f' [EXEC FAILED]', file=sys.stderr, flush=True)

    def _handle_executed_status(self, scanner_status, rule_result):
        self._executed_count += 1
        violations_count = scanner_status.get('violations_found', 0)
        has_errors = self._check_for_errors(rule_result)
        if violations_count > 0:
            icon = ' [X]' if has_errors else ' [!]'
            print(f'{icon} {violations_count}', file=sys.stderr, flush=True)
        else:
            print(f' [OK]', file=sys.stderr, flush=True)

    def _check_for_errors(self, rule_result):
        scanner_results = rule_result.get('scanner_results', {})
        file_by_file_violations = scanner_results.get('file_by_file', {}).get('violations', [])
        cross_file_violations = scanner_results.get('cross_file', {}).get('violations', [])
        
        file_by_file_errors = any((v.severity == 'error' if hasattr(v, 'severity') else v.get('severity') == 'error' for v in file_by_file_violations))
        cross_file_errors = any((v.severity == 'error' if hasattr(v, 'severity') else v.get('severity') == 'error' for v in cross_file_violations))
        return file_by_file_errors or cross_file_errors

    def finish(self, instructions: Dict[str, Any], validation_rules: List[Dict[str, Any]]) -> None:
        if not self._status_file:
            return
        self._write_line(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self._write_line(f'Total violations: {self._total_violations}')
        self._write_line(f'Scanners executed: {self._executed_count}')
        self._status_file.close()
        self._status_file = None
        print(f'\n[COMPLETE] {self._total_violations} violations, {self._executed_count} scanners', file=sys.stderr)
        sys.stderr.flush()

    def _write_line(self, line: str) -> None:
        if self._status_file:
            self._status_file.write(line + '\n')

    def _flush(self) -> None:
        if self._status_file:
            self._status_file.flush()

    def write_cross_file_progress(self, message: str) -> None:
        self._write_line(message)
        self._flush()

    def _get_status_path(self) -> str:
        docs_dir = ensure_reports_directory(self.bot_paths, self.workspace_directory)
        status_file = docs_dir / f'{self.behavior_name}-validation-status-{self._timestamp}.md'
        return str(status_file)

    @property
    def timestamp(self) -> str:
        return self._timestamp

class ValidationReportWriter:

    def __init__(self, behavior_name: str, bot_paths: BotPath, timestamp: str = None):
        self.behavior_name = behavior_name
        self.bot_paths = bot_paths
        self.workspace_directory = bot_paths.workspace_directory
        self._timestamp = timestamp or datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.builder = ValidationReportBuilder(behavior_name, bot_paths, self.workspace_directory)
        self.formatter = ValidationReportFormatter(self.workspace_directory)
        self.file_link_builder = FileLinkBuilder(self.workspace_directory)
        self.scanner_status_formatter = ScannerStatusFormatter(self._check_violation_severities, self.formatter.rule_name_to_anchor)
        self.scanner_status_builder = ValidationScannerStatusBuilder(self._check_violation_severities, self.formatter.rule_name_to_anchor)
        self.violation_formatter = ViolationFormatter(
            lambda v: self._format_violation_line(v),
            lambda msg, loc, ln: self._extract_test_info(msg, loc, ln),
            self.formatter.format_violation_message
        )

    def _check_violation_severities(self, scanner_results: Dict[str, Any]) -> tuple:
        has_errors = False
        has_warnings = False
        for key in ('file_by_file', 'cross_file'):
            if key not in scanner_results:
                continue
            errors, warnings = self._check_violations_in_key(scanner_results[key])
            if errors:
                has_errors = True
            if warnings:
                has_warnings = True
            if has_errors and has_warnings:
                return (True, True)
        return (has_errors, has_warnings)

    def _check_violations_in_key(self, violations_data: Dict[str, Any]) -> tuple:
        has_errors = False
        has_warnings = False
        for v in violations_data.get('violations', []):
            severity = v.severity if hasattr(v, 'severity') else v.get('severity')
            if severity == 'error':
                has_errors = True
            elif severity == 'warning':
                has_warnings = True
            if has_errors and has_warnings:
                return (True, True)
        return (has_errors, has_warnings)

    def write(self, instructions: Dict[str, Any], validation_rules: List[Dict[str, Any]], files: Dict[str, List[Path]]) -> None:
        report_path = self._get_report_path()
        logger.info(f'Writing validation report to: {report_path}')
        try:
            self._write_report_file(report_path, instructions, validation_rules, files)
            logger.info('Report file written successfully')
        except Exception as e:
            self._log_write_error(e, report_path)
            raise

    def _write_report_file(self, report_path: str, instructions: Dict[str, Any], validation_rules: List[Dict[str, Any]], files: Dict[str, List[Path]]) -> None:
        report_file = Path(report_path)
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            self._write_section(f, self.builder.build_header())
            self._write_section(f, self.builder.build_metadata())
            self._write_section(f, self.builder.build_summary(validation_rules, files))
            self._write_section(f, self.builder.build_content_validated(files, self.file_link_builder.get_relative_path, self._build_scanned_files_section))
            self._write_section(f, self.scanner_status_formatter.build_scanner_status(validation_rules))
            self._write_section(f, self.scanner_status_builder.build_validation_rules(validation_rules))
            self._write_section(f, self.violation_formatter.build_violations(validation_rules))
            self._write_section(f, self.builder.build_instructions(instructions))
            self._write_section(f, self.builder.build_report_location(report_path))
    
    def _write_section(self, file_handle, lines: List[str]) -> None:
        file_handle.write('\n'.join(lines) + '\n')
        file_handle.flush()

    def _log_write_error(self, e: Exception, report_path: str) -> None:
        logger.error(f'Error writing report: {type(e).__name__}: {e}')
        logger.error(f'Report path: {report_path}')
        logger.error(f'Traceback:\n{traceback.format_exc()}')

    def get_report_path(self) -> Path:
        docs_dir = ensure_reports_directory(self.bot_paths, self.workspace_directory)
        report_file = docs_dir / f'{self.behavior_name}-validation-report-{self._timestamp}.md'
        return report_file

    def _get_report_path(self) -> str:
        return str(self.get_report_path())

    def get_report_hyperlink(self) -> str:
        report_path = self.get_report_path()
        try:
            resolved_path = report_path.resolve() if report_path.exists() else report_path
            file_str = str(resolved_path).replace('\\', '/')
            if len(file_str) >= 2 and file_str[1] == ':':
                file_str = file_str[0].upper() + ':' + file_str[2:]
            encoded_path = quote(file_str, safe='/:')
            vscode_uri = f'vscode://file/{encoded_path}'
            try:
                rel_path = str(report_path.relative_to(self.workspace_directory))
            except ValueError:
                rel_path = str(report_path)
            return f'[{rel_path}]({vscode_uri})'
        except Exception as e:
            logger.warning(f'Could not create report hyperlink: {e}')
            return str(report_path)

    def _build_scanned_files_section(self, file_type: str, files_scanned: List[str], section_title: str) -> List[str]:
        lines = []
        if files_scanned:
            logger.info(f'{section_title} from content_info: {len(files_scanned)} files')
            lines.append(f'- **{section_title}:**')
            for file_str in sorted(files_scanned):
                file_path = Path(file_str)
                rel_path = self.file_link_builder.get_relative_path(file_path)
                lines.append(f'  - `{rel_path}`')
            lines.append(f'  - **Total:** {len(files_scanned)} {file_type} file(s)')
        return lines

    def _format_violation_line(self, violation: Dict[str, Any]) -> List[str]:
        if hasattr(violation, 'location') and not isinstance(violation, dict):
            location = violation.location
            message = violation.violation_message
            severity = violation.severity
            line_number = violation.line_number
        else:
            location = violation.get('location', 'unknown')
            message = violation.get('violation_message', 'No message')
            severity = violation.get('severity', 'error')
            line_number = violation.get('line_number')
        severity_icon = '<span style="color: red;">[X]</span>' if severity == 'error' else '<span style="color: orange;">[!]</span>' if severity == 'warning' else '<span style="color: blue;">[i]</span>'
        location_link = self.file_link_builder.create_file_link(location, line_number)
        test_info = self._extract_test_info(message, location, line_number)
        formatted_message = self.formatter.format_violation_message(message)
        if test_info:
            return [f'- {severity_icon} **{severity.upper()}** - {location_link}: {test_info}']
        if '\n' not in formatted_message:
            return [f'- {severity_icon} **{severity.upper()}** - {location_link}: {formatted_message}']
        parts = formatted_message.split('\n')
        first_line = parts[0] if parts else formatted_message
        lines = [f'- {severity_icon} **{severity.upper()}** - {location_link}: {first_line}']
        lines.extend(self.violation_formatter.format_multiline_message_parts(parts[1:]))
        return lines

    def _extract_test_info(self, message: str, location: str, line_number: Optional[int] = None) -> Optional[str]:
        test_method_patterns = ['Test\\s+method\\s+["\\\']([^"\\\']+)["\\\']', 'Test\\s+["\\\']([^"\\\']+)["\\\']', 'test\\s+method\\s+["\\\']([^"\\\']+)["\\\']']
        test_class_patterns = ['Test\\s+class\\s+["\\\']([^"\\\']+)["\\\']', 'class\\s+["\\\']([^"\\\']+)["\\\']']
        test_method_match = None
        for pattern in test_method_patterns:
            test_method_match = re.search(pattern, message, re.IGNORECASE)
            if test_method_match:
                break
        test_class_match = None
        for pattern in test_class_patterns:
            test_class_match = re.search(pattern, message, re.IGNORECASE)
            if test_class_match:
                break
        if not test_method_match and (not test_class_match):
            return None
        file_uri = self.file_link_builder.get_file_uri(location, line_number)
        try:
            if test_method_match:
                test_method_name = test_method_match.group(1)
                replacement = f'Test method [{test_method_name}]({file_uri})'
                for old_pattern in [f'Test method "{test_method_name}"', f"Test method '{test_method_name}'", f'Test "{test_method_name}"', f"Test '{test_method_name}'", f'test method "{test_method_name}"', f"test method '{test_method_name}'"]:
                    message = message.replace(old_pattern, replacement)
            if test_class_match:
                test_class_name = test_class_match.group(1)
                replacement = f'Test class [{test_class_name}]({file_uri})'
                for old_pattern in [f'Test class "{test_class_name}"', f"Test class '{test_class_name}'", f'class "{test_class_name}"', f"class '{test_class_name}'"]:
                    message = message.replace(old_pattern, replacement)
        except Exception as e:
            logger.warning(f'Failed to create test info links: {e}, returning original message')
            return None
        return message