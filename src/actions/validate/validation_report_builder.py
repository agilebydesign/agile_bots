from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from ...bot_path import BotPath
from .validation_stats import ValidationStats

class ValidationReportBuilder:

    def __init__(self, behavior_name: str, bot_paths: BotPath, workspace_directory: Path):
        self.behavior_name = behavior_name
        self.bot_paths = bot_paths
        self.workspace_directory = workspace_directory

    def build_header(self) -> List[str]:
        return [f"# Validation Report - {self.behavior_name.replace('_', ' ').title()}", '']

    def build_metadata(self) -> List[str]:
        return [f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", f'**Project:** {self.workspace_directory.name}', f'**Behavior:** {self.behavior_name}', f'**Action:** validate', '']

    def build_summary(self, validation_rules: List[Dict[str, Any]], files: Dict[str, List[Path]] = None) -> List[str]:
        total_rules = len(validation_rules)
        summary_text = self._build_summary_text(files)
        return ['## Summary', '', f'Validated {summary_text} against **{total_rules} validation rules**.', '']
    
    def _build_summary_text(self, files: Dict[str, List[Path]] = None) -> str:
        if not files:
            return 'content'
        test_files = files.get('test', [])
        code_files = files.get('src', [])
        clarification_file, planning_file, rendered_outputs = self._find_content_files()
        has_story_content = bool(clarification_file or planning_file or rendered_outputs)
        parts = []
        if has_story_content:
            parts.append('story map and domain model')
        if code_files:
            parts.append(f'{len(code_files)} code file(s)')
        if test_files:
            parts.append(f'{len(test_files)} test file(s)')
        if not parts:
            return 'content'
        return ' and '.join(parts)

    def build_content_validated(self, files: Dict[str, List[Path]], get_relative_path_fn, build_scanned_files_section_fn) -> List[str]:
        lines = ['## Content Validated', '']
        clarification_file, planning_file, rendered_outputs = self._find_content_files()
        if clarification_file:
            lines.append(f'- **Clarification:** `{clarification_file.name}`')
        if planning_file:
            lines.append(f'- **Planning:** `{planning_file.name}`')
        if rendered_outputs:
            lines.append('- **Rendered Outputs:**')
            for output in rendered_outputs:
                lines.append(f'  - `{output.name}`')
        test_files_scanned = [str(fp) for fp in files.get('test', [])]
        code_files_scanned = [str(fp) for fp in files.get('src', [])]
        lines.extend(build_scanned_files_section_fn('test', test_files_scanned, 'Test Files Scanned'))
        lines.extend(build_scanned_files_section_fn('src', code_files_scanned, 'Code Files Scanned'))
        lines.append('')
        return lines

    def _find_content_files(self) -> tuple:
        docs_path = self.bot_paths.documentation_path
        docs_dir = self.workspace_directory / docs_path
        clarification_file = docs_dir / 'clarification.json'
        planning_file = docs_dir / 'planning.json'
        clarification = clarification_file if clarification_file.exists() else None
        planning = planning_file if planning_file.exists() else None
        rendered_outputs = []
        rendered_patterns = ['*-story-map.md', '*-domain-model-description.md', '*-domain-model-diagram.md', 'story-graph.json', '*-increments.md']
        for pattern in rendered_patterns:
            for file_path in docs_dir.glob(pattern):
                rendered_outputs.append(file_path)
        return (clarification, planning, rendered_outputs)

    def build_instructions(self, instructions: Dict[str, Any]) -> List[str]:
        lines = ['## Validation Instructions', '']
        base_instructions = instructions.get('base_instructions', [])
        if base_instructions:
            lines.append('The following validation steps were performed:')
            lines.append('')
            for i, instruction in enumerate(base_instructions[:10], 1):
                lines.append(f'{i}. {instruction}')
            if len(base_instructions) > 10:
                lines.append(f'*... and {len(base_instructions) - 10} more instructions*')
        lines.append('')
        return lines

    def build_report_location(self, report_path: str) -> List[str]:
        return ['## Report Location', '', f'This report was automatically generated and saved to:', f'`{report_path}`', '']