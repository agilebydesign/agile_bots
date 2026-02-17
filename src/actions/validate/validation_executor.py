import logging
import traceback
from pathlib import Path
from typing import Dict, Any, List, TYPE_CHECKING
from rules.rules import Rules, ValidationContext, ValidationCallbacks
from actions.validate.validation_report_writer import ValidationReportWriter, StreamingValidationReportWriter
from actions.validate.file_link_builder import FileLinkBuilder
from bot.workspace import get_base_actions_directory
from utils import read_json_file
from scanners.schema_violation_scanner import SchemaViolationScanner

if TYPE_CHECKING:
    from action_context import ValidateActionContext

class ValidationExecutor:

    def __init__(self, behavior, rules: Rules):
        self.behavior = behavior
        self.rules = rules

    def execute_synchronous(self, context: 'ValidateActionContext') -> Dict[str, Any]:
        logger = logging.getLogger(__name__)
        try:
            validation_context = ValidationContext.from_action_context(behavior=self.behavior, context=context)
            logger.info(f'Files to validate: {sum((len(f) for f in validation_context.files.values()))} files')
            timestamp = getattr(context, 'timestamp', None)
            streaming_writer = self._setup_streaming_writer(validation_context, timestamp)
            result = self._inject_validation_instructions(validation_context, streaming_writer)
            self._finalize_reports(result, validation_context, streaming_writer)
            return result
        except Exception as e:
            self._log_error(e, context, logger)
            raise

    def _setup_streaming_writer(self, validation_context: ValidationContext, timestamp: str = None) -> StreamingValidationReportWriter:
        streaming_writer = StreamingValidationReportWriter(self.behavior.name, self.behavior.bot_paths, timestamp)
        streaming_writer.start(validation_context.files)
        validation_context.callbacks = ValidationCallbacks(on_scanner_start=streaming_writer.on_scanner_start, on_scanner_complete=streaming_writer.on_scanner_complete, on_file_scanned=streaming_writer.on_file_scanned)
        validation_context.status_writer = streaming_writer
        return streaming_writer

    def _finalize_reports(self, result: Dict[str, Any], validation_context: ValidationContext, streaming_writer: StreamingValidationReportWriter) -> None:
        instructions = result.get('instructions', {})
        validation_rules = instructions.get('validation_rules', [])
        streaming_writer.finish(instructions, validation_rules)
        writer = ValidationReportWriter(self.behavior.name, self.behavior.bot_paths, streaming_writer.timestamp)
        writer.write(instructions, validation_rules, validation_context.files)

    def _log_error(self, e: Exception, context: 'ValidateActionContext', logger) -> None:
        logger.error(f'Error in synchronous validation: {e}')
        logger.error(f'Error type: {type(e).__name__}, Context: scope={context.scope}, background={getattr(context, "background", None)}')
        logger.error(f'Full traceback:\n{traceback.format_exc()}')

    def _inject_validation_instructions(self, validation_context: ValidationContext, streaming_writer: StreamingValidationReportWriter) -> Dict[str, Any]:
        action_instructions = self._get_action_instructions()
        writer = ValidationReportWriter(self.behavior.name, self.behavior.bot_paths, streaming_writer.timestamp)
        report_path = writer.get_report_path()
        report_link = writer.get_report_hyperlink()
        
        # Run schema validation first - add violations to top of report
        schema_violations = self._run_schema_validation(validation_context)
        if schema_violations:
            self._add_schema_violations_to_instructions(action_instructions, schema_violations)
        
        if not self.rules:
            return self._build_no_rules_result(action_instructions, report_path, report_link)
        processed_rules = self.rules.validate(validation_context)
        scanner_status_info = self._collect_scanner_status(processed_rules)
        self._add_scanner_status_to_instructions(action_instructions, scanner_status_info)
        self._add_violation_summary_to_instructions(action_instructions, self.rules.violation_summary)
        action_instructions.append(f'\nValidation report: {report_link}')
        return {'instructions': self._build_instructions_dict(action_instructions, processed_rules, report_path, report_link, schema_violations)}

    def _get_action_instructions(self) -> List[str]:
        base_actions_path = get_base_actions_directory()
        config_path = base_actions_path / 'validate' / 'action_config.json'
        config = read_json_file(config_path)
        return config.get('instructions', [])

    def _build_no_rules_result(self, action_instructions, report_path, report_link):
        action_instructions.append(f'\nValidation report: {report_link}')
        return {'instructions': {'action': 'validate', 'behavior': self.behavior.name, 'base_instructions': action_instructions, 'validation_rules': [], 'content_to_validate': None, 'report_path': str(report_path), 'report_link': report_link}}

    def _collect_scanner_status(self, processed_rules):
        scanner_status_lines = []
        counts = {'executed': 0, 'load_failed': 0, 'execution_failed': 0, 'no_scanner': 0}
        for rule_dict in processed_rules:
            scanner_status = rule_dict.get('scanner_status', {})
            status = scanner_status.get('status', 'UNKNOWN')
            rule_file = rule_dict.get('rule_file', 'unknown')
            self._process_scanner_status(status, counts, scanner_status_lines, rule_file, scanner_status)
        return {'counts': counts, 'lines': scanner_status_lines}

    def _process_scanner_status(self, status, counts, scanner_status_lines, rule_file, scanner_status):
        if status == 'EXECUTED':
            counts['executed'] += 1
            return
        if status == 'LOAD_FAILED':
            counts['load_failed'] += 1
            self._add_failed_scanner_line(scanner_status_lines, rule_file, scanner_status, '[FAILED]')
            return
        if status == 'EXECUTION_FAILED':
            counts['execution_failed'] += 1
            self._add_failed_scanner_line(scanner_status_lines, rule_file, scanner_status, '[ERROR]')
            return
        if status == 'NO_SCANNER':
            counts['no_scanner'] += 1

    def _add_failed_scanner_line(self, scanner_status_lines, rule_file, scanner_status, prefix):
        scanner_path = scanner_status.get('scanner_path', 'unknown')
        error = scanner_status.get('error', 'Unknown error')
        scanner_status_lines.append(f'{prefix} {rule_file}: Scanner failed to load - {scanner_path}')
        scanner_status_lines.append(f'  Error: {error}')

    def _add_scanner_status_to_instructions(self, action_instructions, scanner_status_info):
        counts = scanner_status_info['counts']
        scanner_status_lines = scanner_status_info['lines']
        header = ['\n=== SCANNER EXECUTION STATUS ===', f"Successfully Executed: {counts['executed']}", f"Load Failed: {counts['load_failed']}", f"Execution Failed: {counts['execution_failed']}", f"No Scanner: {counts['no_scanner']}", '']
        if scanner_status_lines:
            header.extend(scanner_status_lines)
        else:
            header.append('All scanners executed successfully.')
        header.append('=== END SCANNER STATUS ===\n')
        action_instructions.extend(header)

    def _add_violation_summary_to_instructions(self, action_instructions, violation_summary):
        if violation_summary:
            edit_instructions = ['Based on code scanner diagnostics, edit the story graph to fix violations:', *violation_summary, 'Review each violation and update the story graph accordingly.']
            action_instructions.extend(edit_instructions)

    def _run_schema_validation(self, validation_context: ValidationContext) -> List[Dict[str, Any]]:
        """Run schema validation to detect fields not conforming to behavior template."""
        logger = logging.getLogger(__name__)
        try:
            scanner = SchemaViolationScanner(self.behavior, self.behavior.bot_paths)
            story_graph_content = validation_context.story_graph
            
            if not story_graph_content:
                logger.info("No story graph content to validate for schema")
                return []
            
            violations = scanner.scan(story_graph_content)
            
            if violations:
                logger.info(f"Schema validation found {len(violations)} violation(s)")
            else:
                logger.info("Schema validation passed - no violations found")
            
            return [v.to_dict() for v in violations]
        except Exception as e:
            logger.error(f"Error running schema validation: {e}")
            return []

    def _add_schema_violations_to_instructions(self, action_instructions: List[str], schema_violations: List[Dict[str, Any]]):
        """Add schema violations to the TOP of the validation instructions."""
        if not schema_violations:
            return
        
        # Insert at the beginning of instructions - these are critical
        header_lines = [
            "",
            "## âš ï¸ SCHEMA VIOLATIONS (MUST FIX FIRST)",
            "",
            f"Found {len(schema_violations)} field(s) that violate the template schema for **{self.behavior.name}** behavior.",
            "",
            "These fields are NOT allowed in this phase. Remove or relocate them:",
            ""
        ]
        
        for i, v in enumerate(schema_violations, 1):
            header_lines.append(f"**{i}. `{v['field_name']}`**")
            header_lines.append(f"   - Path: `{v['path']}`")
            header_lines.append(f"   - {v['message']}")
            header_lines.append("")
        
        header_lines.extend([
            "---",
            ""
        ])
        
        # Insert at position 0 (before other instructions)
        for line in reversed(header_lines):
            action_instructions.insert(0, line)

    def _build_instructions_dict(self, action_instructions, processed_rules, report_path, report_link, schema_violations=None):
        result = {
            'action': 'validate', 
            'behavior': self.behavior.name, 
            'base_instructions': action_instructions, 
            'validation_rules': processed_rules, 
            'content_to_validate': None, 
            'report_path': str(report_path), 
            'report_link': report_link, 
            'report_links': self._collect_report_links()
        }
        if schema_violations:
            result['schema_violations'] = schema_violations
        return result

    def _collect_report_links(self) -> List[str]:
        violations_dir = self.behavior.bot_paths.story_graph_paths.behavior_path(self.behavior.name) / 'violations'
        if not violations_dir.exists():
            return []
        report_files = sorted(
            violations_dir.glob(f'{self.behavior.name}-validation-report-*.md'),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        link_builder = FileLinkBuilder(self.behavior.bot_paths.workspace_directory)
        return [link_builder.create_file_link(str(report_file)) for report_file in report_files]