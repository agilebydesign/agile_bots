import logging
import threading
import traceback
from pathlib import Path
from typing import Dict, Any, TYPE_CHECKING
from datetime import datetime
from actions.validate.validation_scope import ValidationScope

if TYPE_CHECKING:
    from action_context import ValidateActionContext

class BackgroundValidationHandler:

    def __init__(self, behavior, validation_executor):
        self.behavior = behavior
        self.validation_executor = validation_executor

    def execute_background(self, context: 'ValidateActionContext', track_completion_fn) -> Dict[str, Any]:
        total_files = self._get_file_count(context)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        status_path = self._get_status_path(timestamp)
        context.timestamp = timestamp
        self._start_validation_thread(context, track_completion_fn, status_path)
        status_path_relative = status_path.relative_to(self.behavior.bot_paths.workspace_directory)
        return self._build_background_response(status_path_relative, total_files)

    def _get_file_count(self, context: 'ValidateActionContext') -> int:
        try:
            files = ValidationScope.from_context(context, self.behavior.bot_paths, behavior_name=self.behavior.name).all_files()
            return sum((len(f) for f in files.values()))
        except Exception as e:
            logging.getLogger(__name__).warning(f'Could not pre-compute file count: {e}')
            return 0

    def _get_status_path(self, timestamp: str) -> Path:
        docs_path = self.behavior.bot_paths.documentation_path
        reports_dir = self.behavior.bot_paths.workspace_directory / docs_path / 'reports'
        reports_dir.mkdir(parents=True, exist_ok=True)
        return reports_dir / f'{self.behavior.name}-validation-status-{timestamp}.md'

    def _start_validation_thread(self, context: 'ValidateActionContext', track_completion_fn, status_path: Path) -> None:

        def run_validation():
            self._run_validation_task(context, track_completion_fn, status_path)
        threading.Thread(target=run_validation, daemon=False, name='ValidationThread').start()

    def _run_validation_task(self, context: 'ValidateActionContext', track_completion_fn, status_path: Path) -> None:
        logger = logging.getLogger(__name__)
        try:
            result = self.validation_executor.execute_synchronous(context)
            track_completion_fn(outputs=result)
            logger.info('Background validation completed successfully')
        except Exception as e:
            self._handle_validation_error(e, track_completion_fn, status_path, logger)

    def _handle_validation_error(self, e: Exception, track_completion_fn, status_path: Path, logger) -> None:
        track_completion_fn(outputs={'error': str(e)})
        logger.error(f'Background validation failed: {e}')
        traceback.print_exc()
        try:
            status_path.parent.mkdir(parents=True, exist_ok=True)
            with open(status_path, 'a', encoding='utf-8') as f:
                f.write(f'\n\n## ERROR\n\nValidation failed with error: {e}\n')
        except Exception as status_err:
            logger.error(f'Could not write error to status file: {status_err}')

    def _build_background_response(self, status_path_relative: Path, total_files: int) -> Dict[str, Any]:
        return {'instructions': {'base_instructions': self._get_background_instructions(status_path_relative, total_files)}, '_background_execution': True, 'background': True, 'status_file': str(status_path_relative), 'total_files': total_files}

    def _get_background_instructions(self, status_path_relative: Path, total_files: int) -> list:
        return ['', '=' * 70, '**VALIDATION RUNNING IN BACKGROUND**', '=' * 70, '', '**CRITICAL: YOU MUST POLL THE STATUS FILE EVERY 10 SECONDS UNTIL VALIDATION COMPLETES**', '', f'Validation has been started in the background. It will scan {total_files} file(s).', '', '**Status File:**', f'  {status_path_relative}', '', '**AI ASSISTANT DIRECTIVES:**', '1. YOU MUST read the status file every 10 seconds to check progress', '2. YOU MUST report the current status summary to the user each time you check', '3. Continue polling every 10 seconds until validation is complete', '4. When complete, YOU MUST read and report the final summary from the status file', '5. Also check the full report at: docs/story/code-validation-report.md', '', 'The validation is running asynchronously and will update the status file in real-time.', 'The status file shows progress as scanners complete their work.', '', '**Status File Location:**', f'  {status_path_relative}', '', '**Report File Location (when complete):**', '  docs/story/code-validation-report.md', '', '=' * 70, '']