from pathlib import Path
from typing import Dict, Any, List, Optional
from ...scanners.code_scanner import CodeScanner
from ...scanners.scanner_registry import ScannerRegistry
from ...scanners.test_scanner import TestScanner
from ...utils import read_json_file

class Rule:

    def __init__(self, rule_file_path: Path, behavior_name: str, bot_name: str, rule_content: Optional[Dict[str, Any]]=None):
        self._rule_file_path = Path(rule_file_path)
        self._behavior_name = behavior_name
        self._bot_name = bot_name
        self._rule_content_param = rule_content
        self._init_rule_content()
        self._init_scanner()
        self._init_violation_tracking()

    def _init_rule_content(self) -> None:
        rule_content = self._rule_content_param
        if rule_content is not None:
            self._rule_content = rule_content
            self._rule_file = f'{self._rule_file_path.name}#embedded'
            self._name = rule_content.get('name', 'unknown') or self._rule_file_path.stem
        else:
            self._rule_content = read_json_file(self._rule_file_path)
            self._rule_file = self._rule_file_path.name
            self._name = self._rule_file.replace('.json', '') if self._rule_file else 'unknown'

    def _init_scanner(self) -> None:
        self._scanner_load_error: Optional[str] = None
        scanner_path = self._rule_content.get('scanner')
        if scanner_path:
            self._scanner, self._scanner_load_error = self._load_scanner(scanner_path)
        else:
            self._scanner = None

    def _init_violation_tracking(self) -> None:
        self._file_by_file_violations: List[Dict[str, Any]] = []
        self._cross_file_violations: List[Dict[str, Any]] = []
        self._scan_error: Optional[str] = None
        self._scanner_execution_status: Optional[str] = None

    def _load_scanner(self, scanner_module_path: str) -> tuple[Optional[type], Optional[str]]:
        scanner_registry = ScannerRegistry(self._bot_name)
        scanner_class, error = scanner_registry.loads_scanner_class_with_error(scanner_module_path)
        return (scanner_class, error)

    @property
    def name(self) -> str:
        return self._name

    @property
    def rule_file(self) -> str:
        return self._rule_file

    @property
    def behavior_name(self) -> str:
        return self._behavior_name

    @property
    def scanner(self):
        if not self._scanner:
            return None
        return self._scanner()

    @property
    def scanner_class(self) -> Optional[type]:
        return self._scanner

    @property
    def priority(self) -> int:
        return self._rule_content.get('priority', 999)
    
    @property
    def description(self) -> str:
        return self._rule_content.get('description', '')

    @property
    def examples(self) -> List[Dict[str, Any]]:
        return self._rule_content.get('examples', [])

    @property
    def scanner_path(self) -> Optional[str]:
        return self._rule_content.get('scanner')

    @property
    def rule_content(self) -> Dict[str, Any]:
        return self._rule_content

    @property
    def instruction(self) -> Optional[str]:
        return self._rule_content.get('instruction')

    @property
    def has_scanner(self) -> bool:
        return self._scanner is not None

    @property
    def scanner_load_error(self) -> Optional[str]:
        return self._scanner_load_error

    @property
    def scanner_execution_status(self) -> Optional[str]:
        return self._scanner_execution_status

    @scanner_execution_status.setter
    def scanner_execution_status(self, value: Optional[str]):
        self._scanner_execution_status = value

    @property
    def requires_two_pass_scan(self) -> bool:
        if not self._scanner:
            return False
        return issubclass(self._scanner, TestScanner) or issubclass(self._scanner, CodeScanner)

    def scan(self, knowledge_graph: Dict[str, Any], files: Optional[Dict[str, List[Path]]]=None, on_file_scanned: Optional[Any]=None, skip_cross_file: bool=False, changed_files: Optional[Dict[str, List[Path]]]=None, status_writer: Optional[Any]=None, max_cross_file_comparisons: int=20) -> Dict[str, Any]:
        if not self.has_scanner:
            return {}
        files = files or {}
        files_to_scan = changed_files if changed_files else files
        test_files = files_to_scan.get('test', [])
        code_files = files_to_scan.get('src', [])
        # For cross-file scanning: use scoped files if scope is active, otherwise all files
        # The 'files' parameter already contains scoped files when scope is active
        all_test_files = files.get('test', [])
        all_code_files = files.get('src', [])
        self._initialize_scan_state()
        try:
            scanner_instance = self._get_scanner_instance()
            self._execute_file_by_file_scan(scanner_instance, knowledge_graph, test_files, code_files, on_file_scanned)
            # Cross-file scan uses the same scoped files - all_test_files/all_code_files are already scoped
            self._execute_cross_file_scan(scanner_instance, skip_cross_file, test_files, code_files, all_test_files, all_code_files, status_writer, max_cross_file_comparisons)
            return self._build_scan_result()
        except Exception as e:
            self._scan_error = str(e)
            self._scanner_execution_status = f'EXECUTION_FAILED: {str(e)}'
            raise

    def _initialize_scan_state(self):
        self._file_by_file_violations = []
        self._cross_file_violations = []
        self._scan_error = None

    def _get_scanner_instance(self):
        scanner_instance = self.scanner
        if not scanner_instance:
            self._scanner_execution_status = 'EXECUTION_SKIPPED: Scanner instance is None'
            return None
        self._scanner_execution_status = 'EXECUTION_SUCCESS'
        return scanner_instance

    def _execute_file_by_file_scan(self, scanner_instance, knowledge_graph, test_files, code_files, on_file_scanned):
        violations_file_by_file = scanner_instance.scan(knowledge_graph, rule_obj=self, test_files=test_files, code_files=code_files, on_file_scanned=on_file_scanned)
        if violations_file_by_file is not None:
            if isinstance(violations_file_by_file, list):
                self._file_by_file_violations = violations_file_by_file
            else:
                self._file_by_file_violations = [violations_file_by_file] if violations_file_by_file else []
        else:
            self._file_by_file_violations = []
        if not hasattr(self, '_file_by_file_violations') or self._file_by_file_violations is None:
            self._file_by_file_violations = []

    def _execute_cross_file_scan(self, scanner_instance, skip_cross_file, test_files, code_files, all_test_files, all_code_files, status_writer=None, max_cross_file_comparisons=20):
        if not skip_cross_file and self.requires_two_pass_scan and hasattr(scanner_instance, 'scan_cross_file'):
            violations_cross_file = scanner_instance.scan_cross_file(rule_obj=self, test_files=test_files, code_files=code_files, all_test_files=all_test_files, all_code_files=all_code_files, status_writer=status_writer, max_cross_file_comparisons=max_cross_file_comparisons)
            if violations_cross_file:
                self._cross_file_violations = violations_cross_file

    def _build_scan_result(self):
        if self.requires_two_pass_scan:
            return {'file_by_file': {'violations': self._file_by_file_violations}, 'cross_file': {'violations': self._cross_file_violations}}
        else:
            return {'violations': self._file_by_file_violations}

    @property
    def violations(self) -> List[Dict[str, Any]]:
        all_violations = []
        if hasattr(self, '_file_by_file_violations'):
            all_violations.extend(self._file_by_file_violations)
        if hasattr(self, '_cross_file_violations'):
            all_violations.extend(self._cross_file_violations)
        return all_violations

    @property
    def file_by_file_violations(self) -> List[Dict[str, Any]]:
        return getattr(self, '_file_by_file_violations', [])

    @property
    def cross_file_violations(self) -> List[Dict[str, Any]]:
        return getattr(self, '_cross_file_violations', [])

    @property
    def scanner_results(self) -> Dict[str, Any]:
        if not hasattr(self, '_file_by_file_violations'):
            return {}
        if self.requires_two_pass_scan:
            result = {'file_by_file': {'violations': self._file_by_file_violations}, 'cross_file': {'violations': self._cross_file_violations}}
            if self._scan_error:
                result['file_by_file']['error'] = self._scan_error
            return result
        else:
            result = {'violations': self._file_by_file_violations}
            if self._scan_error:
                result['error'] = self._scan_error
            return result

    def _format_guidance(self, guidance_list: list, formatted: list) -> None:
        for guidance in guidance_list:
            desc = guidance.get('description', '')
            examples = guidance.get('example', [])
            if desc:
                formatted.append(f'\n{desc}')
            if examples:
                for ex in examples:
                    formatted.append(f'  - {ex}')
    
    def _format_examples(self, examples: list, formatted: list) -> None:
        for example in examples:
            desc = example.get('description', '')
            content = example.get('content', '')
            if isinstance(content, list):
                content = '\n'.join(content)
            if desc:
                formatted.append(f'- {desc}: {content}')
            else:
                formatted.append(f'- {content}')

    def _format_example_block(self, example_content: dict, label: str, formatted: list) -> None:
        desc = example_content.get('description', '')
        content = example_content.get('content', '')
        if isinstance(content, list):
            content = '\n'.join(content)
        formatted.append(f'\n**{label}:** {desc}')
        formatted.append(content)

    def _format_inline_examples(self, formatted: list) -> None:
        examples = self._rule_content.get('examples', [])
        for example in examples:
            if 'do' in example:
                self._format_example_block(example['do'], 'DO', formatted)
            if 'dont' in example:
                self._format_example_block(example['dont'], "DON'T", formatted)

    def _format_rule_section(self, section_key: str, header: str, formatted: list) -> None:
        """Helper to format a rule section (DO or DON'T) with description and guidance."""
        section = self._rule_content.get(section_key, {})
        desc = section.get('description', '')
        guidance = section.get('guidance', [])
        
        if desc or guidance:
            formatted.append(f'\n**{header}:**')
            if desc:
                formatted.append(f'{desc}')
            if guidance:
                self._format_guidance(guidance, formatted)

    def formatted_text(self) -> List[str]:
        formatted = []
        formatted.append(f'\n**Rule:** {self.rule_file}')
        if self.description:
            formatted.append(f'{self.description}')
        
        # DO section with description
        self._format_rule_section('do', 'DO', formatted)
        
        # DON'T section with description
        self._format_rule_section('dont', "DON'T", formatted)
        
        if 'examples' in self._rule_content:
            self._format_inline_examples(formatted)
        formatted.append('')
        return formatted

