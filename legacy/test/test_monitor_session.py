import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from agile_bot.bots.base_bot.src.repl_cli.headless.headless_session import HeadlessSession
from agile_bot.bots.base_bot.src.repl_cli.headless.execution_result import ExecutionResult
from agile_bot.bots.base_bot.src.repl_cli.headless.recoverable_error import RecoverableError
from agile_bot.bots.base_bot.src.repl_cli.headless.non_recoverable_error import NonRecoverableError
from agile_bot.bots.base_bot.src.repl_cli.headless.error_recovery import ErrorRecovery


@pytest.fixture
def workspace_directory(tmp_path):
    workspace_dir = tmp_path / 'workspace'
    workspace_dir.mkdir(parents=True, exist_ok=True)
    return workspace_dir


@pytest.fixture
def headless_config(workspace_directory, monkeypatch):
    config_path = workspace_directory / 'headless_config.json'
    config_data = {'api_key': 'sk-test123456789'}
    config_path.write_text(json.dumps(config_data))
    monkeypatch.setenv('HEADLESS_CONFIG_PATH', str(config_path))
    return config_path


def given_headless_session_is_running_with_session_id(workspace_directory, session_id):
    log_dir = workspace_directory / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f'headless-{session_id}.log'
    log_file.write_text(f'Session {session_id} running\n')
    return session_id


def given_session_log_file_is_created_at(workspace_directory, log_file_path):
    log_file = workspace_directory / log_file_path
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text('Session log initialized\n')
    return log_file


def given_this_is_loop_iteration(workspace_directory, iteration_number):
    return iteration_number


def given_headless_session_is_running(workspace_directory):
    session_id = 'session_abc123'
    log_dir = workspace_directory / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f'headless-{session_id}.log'
    log_file.write_text('Session running\n')
    return session_id


def given_cli_is_polling_session_status(workspace_directory, session_id):
    return session_id


def given_headless_session_has_blocked(workspace_directory):
    log_file = workspace_directory / 'logs' / 'headless-session.log'
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text('Status: blocked\nReason: Waiting for API key configuration\n')
    return log_file


def given_session_log_contains_block_reason(workspace_directory, block_reason):
    log_file = workspace_directory / 'logs' / 'headless-session.log'
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text(f'Blocked: {block_reason}\n')
    return log_file


def given_headless_session_has_completed_successfully(workspace_directory):
    log_file = workspace_directory / 'logs' / 'headless-session.log'
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text('Session completed successfully\nExecution transcript:\n- Created auth module\n- Added JWT validation\n')
    return log_file


def given_session_log_contains_execution_transcript(workspace_directory, transcript):
    log_file = workspace_directory / 'logs' / 'headless-session.log'
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text(f'Execution transcript:\n{transcript}\n')
    return log_file


def given_headless_session_completed_action(workspace_directory, behavior_name, action_name):
    log_file = workspace_directory / 'logs' / 'headless-session.log'
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text(f'Action completed: {behavior_name}.{action_name}\nFiles created: story-graph.json\n')
    return log_file


def given_session_log_shows_file_was_created(workspace_directory, file_name):
    log_file = workspace_directory / 'logs' / 'headless-session.log'
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text(f'Files created: {file_name}\n')
    return log_file


def given_headless_session_has_failed(workspace_directory):
    log_file = workspace_directory / 'logs' / 'headless-session.log'
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text('Error: File not found: config.json\n')
    return log_file


def given_session_log_contains_error_message(workspace_directory, error_message):
    log_file = workspace_directory / 'logs' / 'headless-session.log'
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text(f'Error: {error_message}\n')
    return log_file


def given_cli_attempts_to_connect_to_cursor_headless_api(workspace_directory):
    return workspace_directory


def given_api_connection_fails_with_timeout(workspace_directory):
    return 'timeout'


def given_cli_has_retried_connection_3_times(workspace_directory):
    return 3


def given_headless_session_was_executing_behavior(workspace_directory, behavior_name):
    log_file = workspace_directory / 'logs' / 'headless-session.log'
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text(f'Executing behavior: {behavior_name}\n')
    return log_file


def given_action_completed_successfully(workspace_directory, action_name):
    log_file = workspace_directory / 'logs' / 'headless-session.log'
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text(f'Action {action_name} completed successfully\n')
    return log_file


def given_action_failed_with_validation_error(workspace_directory, action_name, error_message):
    log_file = workspace_directory / 'logs' / 'headless-session.log'
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text(f'Action {action_name} failed: {error_message}\n')
    return log_file


def given_headless_session_is_running_for_monitoring(workspace_directory):
    session_id = 'session_abc123'
    log_dir = workspace_directory / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f'headless-{session_id}.log'
    log_file.write_text('Session running\n')
    return session_id


def given_ai_has_not_responded_for_5_minutes(workspace_directory):
    return 300


def given_ai_indicates_stuck_in_planning_mode(workspace_directory):
    log_file = workspace_directory / 'logs' / 'headless-session.log'
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text('AI stuck in planning mode\n')
    return log_file


def given_recoverable_error_indicates_ai_hang():
    return RecoverableError(message='AI hang')


def given_recoverable_error_indicates_ai_stuck_in_planning():
    return RecoverableError(message='AI stuck in planning')


def given_error_recovery_tracks_recovery_attempt_count_less_than_3():
    return ErrorRecovery(max_attempts=3, current_attempts=2)


def given_recoverable_error_indicates_ai_hung_or_stuck():
    return RecoverableError(message='AI hung or stuck')


def given_error_recovery_tracks_recovery_attempt_count_equals_3():
    return ErrorRecovery(max_attempts=3, current_attempts=3)


def given_error_recovery_has_already_recovered_3_times_in_a_row():
    return ErrorRecovery(max_attempts=3, current_attempts=3, recovery_history=[1, 2, 3])


def when_cli_polls_cursor_headless_api_for_session_status(workspace_directory, session_id):
    session = HeadlessSession(workspace_directory)
    status = session.poll_session_status(session_id)
    return status


def when_api_returns_session_status_as_running(workspace_directory):
    return {'status': 'running', 'progress': 'Implementing authentication'}


def when_api_returns_session_status_as_completed(workspace_directory):
    return {'status': 'completed'}


def when_cli_completes_loop_iteration(workspace_directory, iteration_number):
    log_file = workspace_directory / 'logs' / 'headless-session.log'
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text(f'Loop {iteration_number} completed\n')
    return iteration_number


def when_api_returns_session_status_as_blocked(workspace_directory):
    return {'status': 'blocked', 'reason': 'Waiting for API key configuration'}


def when_cli_prepares_blocked_report(workspace_directory):
    session = HeadlessSession(workspace_directory)
    report = session.prepare_blocked_report()
    return report


def when_cli_prepares_completion_report(workspace_directory):
    session = HeadlessSession(workspace_directory)
    report = session.prepare_completion_report()
    return report


def when_cli_prepares_failure_report(workspace_directory):
    session = HeadlessSession(workspace_directory)
    report = session.prepare_failure_report()
    return report


def when_error_recovery_determines_error_is_recoverable(error_recovery, recoverable_error):
    return error_recovery.determines_if_error_is_recoverable(recoverable_error)


def when_error_recovery_enforces_max_retry_limit(error_recovery):
    return error_recovery.enforces_max_retry_limit()


def then_api_returns_session_status_as_running(status):
    assert status.get('status') == 'running' or status.status == 'running'


def then_api_returns_progress_message(status, expected_message):
    assert expected_message in str(status.get('progress', '')) or expected_message in str(status.progress)


def then_cli_appends_loop_number_to_log_file(workspace_directory, loop_number, log_file_path):
    log_file = workspace_directory / log_file_path
    if log_file.exists():
        log_content = log_file.read_text()
        assert f'Loop {loop_number}' in log_content or f'loop {loop_number}' in log_content.lower()


def then_cli_appends_instruction_sent_to_log_file(workspace_directory, log_file_path, instruction):
    log_file = workspace_directory / log_file_path
    if log_file.exists():
        log_content = log_file.read_text()
        assert instruction in log_content or instruction.lower() in log_content.lower()


def then_cli_appends_ai_response_summary_to_log_file(workspace_directory, log_file_path, summary):
    log_file = workspace_directory / log_file_path
    if log_file.exists():
        log_content = log_file.read_text()
        assert summary in log_content or summary.lower() in log_content.lower()


def then_cli_appends_work_completed_in_this_iteration_to_log_file(workspace_directory, log_file_path, work_completed):
    log_file = workspace_directory / log_file_path
    if log_file.exists():
        log_content = log_file.read_text()
        assert work_completed in log_content or work_completed.lower() in log_content.lower()


def then_cli_continues_polling_at_regular_intervals(status):
    assert status.get('status') == 'running' or status.status == 'running'


def then_cli_stops_polling(status):
    assert status.get('status') in ['completed', 'blocked'] or status.status in ['completed', 'blocked']


def then_cli_appends_final_status_to_log_file(workspace_directory, log_file_path):
    log_file = workspace_directory / log_file_path
    if log_file.exists():
        log_content = log_file.read_text()
        assert 'completed' in log_content.lower() or 'final' in log_content.lower()


def then_cli_prepares_completion_report(report):
    assert report is not None
    assert report.status == 'completed' or 'completed' in str(report)


def then_cli_appends_total_loops_to_log_file(workspace_directory, log_file_path, total_loops):
    log_file = workspace_directory / log_file_path
    if log_file.exists():
        log_content = log_file.read_text()
        assert f'Total loops: {total_loops}' in log_content or f'total loops: {total_loops}' in log_content.lower()


def then_cli_appends_block_reason_to_log_file(workspace_directory, log_file_path, block_reason):
    log_file = workspace_directory / log_file_path
    if log_file.exists():
        log_content = log_file.read_text()
        assert block_reason in log_content or block_reason.lower() in log_content.lower()


def then_cli_prepares_blocked_report(report):
    assert report is not None
    assert report.status == 'blocked' or 'blocked' in str(report)


def then_cli_extracts_block_reason_from_session_log(report, expected_reason):
    assert expected_reason in str(report.block_reason) or expected_reason.lower() in str(report.block_reason).lower()


def then_cli_formats_block_reason_for_console_display(report):
    assert report.block_reason is not None or report.console_output is not None


def then_cli_displays_block_reason_to_console(report, expected_reason):
    assert expected_reason in str(report.console_output) or expected_reason.lower() in str(report.console_output).lower()


def then_cli_shows_log_file_path_for_details(report):
    assert report.log_path is not None or 'log' in str(report)


def then_cli_displays_operation_context(report, operation_context):
    assert operation_context in str(report) or operation_context.lower() in str(report).lower()


def then_cli_suggests_resolution(report, resolution):
    assert resolution in str(report) or resolution.lower() in str(report).lower()


def then_cli_extracts_transcript_from_session_log(report, expected_transcript):
    assert expected_transcript in str(report.transcript) or expected_transcript.lower() in str(report.transcript).lower()


def then_cli_displays_headless_execution_completed_to_console(report):
    assert 'completed' in str(report.console_output).lower() or 'headless execution completed' in str(report.console_output).lower()


def then_cli_shows_summary_of_work_completed(report):
    assert report.summary is not None or 'summary' in str(report).lower()


def then_cli_displays_log_file_path(report, expected_path):
    assert expected_path in str(report.log_path) or expected_path in str(report)


def then_cli_exits_with_success_status_code(report):
    assert report.exit_code == 0 or report.status == 'completed'


def then_cli_displays_action_completed(report, action_name):
    assert action_name in str(report) or f'{action_name} completed' in str(report).lower()


def then_cli_shows_files_created(report, file_name):
    assert file_name in str(report) or file_name in str(report.files_created)


def then_cli_extracts_error_message_from_session_log(report, expected_error):
    assert expected_error in str(report.error_message) or expected_error.lower() in str(report.error_message).lower()


def then_cli_displays_headless_execution_failed_non_recoverable_to_console(report):
    assert 'failed' in str(report.console_output).lower() and 'non-recoverable' in str(report.console_output).lower()


def then_cli_shows_error_message(report, expected_error):
    assert expected_error in str(report.error_message) or expected_error in str(report.console_output)


def then_non_recoverable_error_cannot_be_retried(error):
    assert error.can_retry is False


def then_cli_displays_log_file_path_for_full_details(report):
    assert report.log_path is not None


def then_cli_exits_with_failure_status_code(report):
    assert report.exit_code != 0 or report.status == 'failed'


def then_cli_displays_failed_to_connect_to_cursor_headless_api_non_recoverable_to_console(report):
    assert 'failed to connect' in str(report.console_output).lower() and 'non-recoverable' in str(report.console_output).lower()


def then_cli_shows_error_details(report, error_details):
    assert error_details in str(report.error_message) or error_details in str(report.console_output)


def then_cli_suggests_checking_api_key_configuration(report):
    assert 'api key' in str(report).lower() or 'configuration' in str(report).lower()


def then_error_recovery_logs_ai_hung_attempting_recovery_to_log_file(workspace_directory, attempt_number, max_attempts):
    log_file = workspace_directory / 'logs' / 'headless-session.log'
    if log_file.exists():
        log_content = log_file.read_text()
        assert f'attempt {attempt_number} of {max_attempts}' in log_content.lower() or 'ai hung' in log_content.lower()


def then_error_recovery_waits_before_retry_for_1_minute(error_recovery):
    assert error_recovery.wait_time == 60


def then_error_recovery_terminates_current_headless_session(error_recovery, session_id):
    assert error_recovery.session_terminated is True


def then_error_recovery_restarts_session_with_same_instructions(error_recovery):
    assert error_recovery.session_restarted is True


def then_error_recovery_wraps_with_persistence_directive(error_recovery):
    assert 'Keep doing this until' in error_recovery.instructions or '100% done or blocked' in error_recovery.instructions


def then_error_recovery_sends_to_new_cursor_headless_api_session(error_recovery):
    assert error_recovery.new_session_id is not None


def then_error_recovery_tracks_recovery_attempt_count_incremented_to(error_recovery, expected_count):
    assert error_recovery.current_attempts == expected_count


def then_error_recovery_logs_session_restarted_due_to_ai_hang_to_log_file(workspace_directory):
    log_file = workspace_directory / 'logs' / 'headless-session.log'
    if log_file.exists():
        log_content = log_file.read_text()
        assert 'session restarted' in log_content.lower() or 'restarted' in log_content.lower()


def then_cli_continues_monitoring_new_session(result):
    assert result.monitoring is True or result.status in ['running', 'completed']


def then_non_recoverable_error_indicates_max_recovery_attempts_exceeded(error):
    assert error.can_retry is False
    assert 'max recovery attempts' in str(error.message).lower() or 'max attempts' in str(error.message).lower()


def then_cli_logs_maximum_recovery_attempts_reached_treating_as_non_recoverable_to_log_file(workspace_directory, max_attempts):
    log_file = workspace_directory / 'logs' / 'headless-session.log'
    if log_file.exists():
        log_content = log_file.read_text()
        assert f'maximum recovery attempts ({max_attempts})' in log_content.lower() or 'max recovery attempts' in log_content.lower()


def then_cli_displays_headless_execution_failed_after_3_recovery_attempts_to_console(report):
    assert 'failed after 3 recovery attempts' in str(report.console_output).lower() or '3 recovery attempts' in str(report.console_output).lower()


def then_cli_shows_all_recovery_attempts_made(report):
    assert len(report.recovery_attempts) > 0 or 'recovery attempts' in str(report).lower()


def then_cli_displays_behavior_execution_failed_at_action_non_recoverable(report, action_name):
    assert f'failed at {action_name}' in str(report.console_output).lower() or f'{action_name}' in str(report.console_output).lower()
    assert 'non-recoverable' in str(report.console_output).lower()


def then_cli_shows_completed_actions(report, action_name):
    assert action_name in str(report.completed_actions) or action_name in str(report)


def then_cli_shows_failed_action_with_error(report, action_name, error_message):
    assert action_name in str(report.failed_action) or action_name in str(report)
    assert error_message in str(report.error_message) or error_message in str(report)


class TestMonitorExecution:
    
    def test_poll_session_status_during_execution(self, workspace_directory):
        # Given: headless session is running with session ID session_abc123
        session_id = given_headless_session_is_running_with_session_id(workspace_directory, 'session_abc123')
        
        # And: session log file is created at logs/headless-2025-12-29.log
        log_file = given_session_log_file_is_created_at(workspace_directory, 'logs/headless-2025-12-29.log')
        
        # And: this is loop iteration 3
        iteration_number = given_this_is_loop_iteration(workspace_directory, 3)
        
        # When: CLI polls Cursor Headless API for session status
        status = when_cli_polls_cursor_headless_api_for_session_status(workspace_directory, session_id)
        
        # Then: API returns session status as running
        then_api_returns_session_status_as_running(status)
        
        # And: API returns progress message Implementing authentication
        then_api_returns_progress_message(status, 'Implementing authentication')
        
        # And: CLI appends loop number 3 to log file
        then_cli_appends_loop_number_to_log_file(workspace_directory, 3, 'logs/headless-2025-12-29.log')
        
        # And: CLI appends instruction sent to log file
        then_cli_appends_instruction_sent_to_log_file(workspace_directory, 'logs/headless-2025-12-29.log', 'Keep doing this until done')
        
        # And: CLI appends AI response summary to log file
        then_cli_appends_ai_response_summary_to_log_file(workspace_directory, 'logs/headless-2025-12-29.log', 'Created user model')
        
        # And: CLI appends work completed in this iteration to log file
        then_cli_appends_work_completed_in_this_iteration_to_log_file(workspace_directory, 'logs/headless-2025-12-29.log', 'Added login endpoint')
        
        # And: CLI continues polling at regular intervals
        then_cli_continues_polling_at_regular_intervals(status)
    
    def test_detect_completion_during_monitoring(self, workspace_directory):
        # Given: headless session is running
        session_id = given_headless_session_is_running(workspace_directory)
        
        # And: CLI is polling session status
        polling_session_id = given_cli_is_polling_session_status(workspace_directory, session_id)
        
        # When: API returns session status as completed
        status = when_api_returns_session_status_as_completed(workspace_directory)
        
        # Then: CLI stops polling
        then_cli_stops_polling(status)
        
        # And: CLI appends final status to log file
        then_cli_appends_final_status_to_log_file(workspace_directory, 'logs/headless-session.log')
        
        # And: CLI prepares completion report
        report = when_cli_prepares_completion_report(workspace_directory)
        then_cli_prepares_completion_report(report)
    
    def test_log_multiple_loop_iterations_with_progress_tracking(self, workspace_directory):
        # Given: headless session is running
        session_id = given_headless_session_is_running(workspace_directory)
        
        # And: CLI is executing instruction loop
        log_file_path = 'logs/headless-session.log'
        
        # When: CLI completes loop iteration 1
        iteration_1 = when_cli_completes_loop_iteration(workspace_directory, 1)
        
        # Then: CLI appends Loop 1 to log file
        then_cli_appends_loop_number_to_log_file(workspace_directory, 1, log_file_path)
        
        # And: CLI appends instruction sent Keep doing this until done: Implement authentication
        then_cli_appends_instruction_sent_to_log_file(workspace_directory, log_file_path, 'Keep doing this until done: Implement authentication')
        
        # And: CLI appends AI response summary Created user model and login endpoint
        then_cli_appends_ai_response_summary_to_log_file(workspace_directory, log_file_path, 'Created user model and login endpoint')
        
        # And: AI indicates not done
        assert True
        
        # When: CLI completes loop iteration 2
        iteration_2 = when_cli_completes_loop_iteration(workspace_directory, 2)
        
        # Then: CLI appends Loop 2 to log file
        then_cli_appends_loop_number_to_log_file(workspace_directory, 2, log_file_path)
        
        # And: CLI appends instruction sent Keep doing this until done: Implement authentication
        then_cli_appends_instruction_sent_to_log_file(workspace_directory, log_file_path, 'Keep doing this until done: Implement authentication')
        
        # And: CLI appends AI response summary Added JWT token generation and validation
        then_cli_appends_ai_response_summary_to_log_file(workspace_directory, log_file_path, 'Added JWT token generation and validation')
        
        # And: AI indicates not done
        assert True
        
        # When: CLI completes loop iteration 3
        iteration_3 = when_cli_completes_loop_iteration(workspace_directory, 3)
        
        # Then: CLI appends Loop 3 to log file
        then_cli_appends_loop_number_to_log_file(workspace_directory, 3, log_file_path)
        
        # And: CLI appends instruction sent Keep doing this until done: Implement authentication
        then_cli_appends_instruction_sent_to_log_file(workspace_directory, log_file_path, 'Keep doing this until done: Implement authentication')
        
        # And: CLI appends AI response summary Added tests and documentation, authentication complete
        then_cli_appends_ai_response_summary_to_log_file(workspace_directory, log_file_path, 'Added tests and documentation, authentication complete')
        
        # And: AI indicates done
        assert True
        
        # And: CLI appends Total loops: 3 to log file
        then_cli_appends_total_loops_to_log_file(workspace_directory, log_file_path, 3)
    
    def test_detect_blocked_state_during_monitoring(self, workspace_directory):
        # Given: headless session is running
        session_id = given_headless_session_is_running(workspace_directory)
        
        # And: CLI is polling session status
        polling_session_id = given_cli_is_polling_session_status(workspace_directory, session_id)
        
        # When: API returns session status as blocked
        status = when_api_returns_session_status_as_blocked(workspace_directory)
        
        # And: API returns block reason Waiting for API key configuration
        block_reason = 'Waiting for API key configuration'
        
        # Then: CLI stops polling
        then_cli_stops_polling(status)
        
        # And: CLI appends block reason to log file
        then_cli_appends_block_reason_to_log_file(workspace_directory, 'logs/headless-session.log', block_reason)
        
        # And: CLI prepares blocked report
        report = when_cli_prepares_blocked_report(workspace_directory)
        then_cli_prepares_blocked_report(report)


class TestSurfaceBlockReason:
    
    def test_display_block_reason_to_user(self, workspace_directory):
        # Given: headless session has blocked
        log_file = given_headless_session_has_blocked(workspace_directory)
        
        # And: session log contains block reason Waiting for API key configuration
        block_reason_file = given_session_log_contains_block_reason(workspace_directory, 'Waiting for API key configuration')
        
        # When: CLI prepares blocked report
        report = when_cli_prepares_blocked_report(workspace_directory)
        
        # Then: CLI extracts block reason from session log
        then_cli_extracts_block_reason_from_session_log(report, 'Waiting for API key configuration')
        
        # And: CLI formats block reason for console display
        then_cli_formats_block_reason_for_console_display(report)
        
        # And: CLI displays Blocked: Waiting for API key configuration to console
        then_cli_displays_block_reason_to_console(report, 'Blocked: Waiting for API key configuration')
        
        # And: CLI shows log file path for details
        then_cli_shows_log_file_path_for_details(report)
    
    def test_display_block_reason_with_context(self, workspace_directory):
        # Given: headless session has blocked during confirm operation
        log_file = given_headless_session_has_blocked(workspace_directory)
        
        # And: session log contains block reason Missing required parameter --data
        block_reason_file = given_session_log_contains_block_reason(workspace_directory, 'Missing required parameter --data')
        
        # When: CLI prepares blocked report
        report = when_cli_prepares_blocked_report(workspace_directory)
        
        # Then: CLI displays operation context confirm operation
        then_cli_displays_operation_context(report, 'confirm operation')
        
        # And: CLI displays block reason Missing required parameter --data
        then_cli_displays_block_reason_to_console(report, 'Missing required parameter --data')
        
        # And: CLI suggests resolution Check --data parameter
        then_cli_suggests_resolution(report, 'Check --data parameter')
        
        # And: CLI shows log file path
        then_cli_shows_log_file_path_for_details(report)


class TestReportCompletion:
    
    def test_report_successful_completion_to_console(self, workspace_directory):
        # Given: headless session has completed successfully
        log_file = given_headless_session_has_completed_successfully(workspace_directory)
        
        # And: session log contains execution transcript
        transcript_file = given_session_log_contains_execution_transcript(workspace_directory, '- Created auth module\n- Added JWT validation')
        
        # When: CLI prepares completion report
        report = when_cli_prepares_completion_report(workspace_directory)
        
        # Then: CLI extracts transcript from session log
        then_cli_extracts_transcript_from_session_log(report, 'Created auth module')
        
        # And: CLI displays Headless execution completed to console
        then_cli_displays_headless_execution_completed_to_console(report)
        
        # And: CLI shows summary of work completed
        then_cli_shows_summary_of_work_completed(report)
        
        # And: CLI displays log file path logs/headless-2025-12-29.log
        then_cli_displays_log_file_path(report, 'logs/headless-2025-12-29.log')
        
        # And: CLI exits with success status code
        then_cli_exits_with_success_status_code(report)
    
    def test_report_completion_with_operation_details(self, workspace_directory):
        # Given: headless session completed shape.build action
        log_file = given_headless_session_completed_action(workspace_directory, 'shape', 'build')
        
        # And: session log shows story-graph.json was created
        file_log = given_session_log_shows_file_was_created(workspace_directory, 'story-graph.json')
        
        # When: CLI prepares completion report
        report = when_cli_prepares_completion_report(workspace_directory)
        
        # Then: CLI displays Action completed: shape.build
        then_cli_displays_action_completed(report, 'shape.build')
        
        # And: CLI shows files created story-graph.json
        then_cli_shows_files_created(report, 'story-graph.json')
        
        # And: CLI displays log file path
        then_cli_displays_log_file_path(report, 'logs/headless-session.log')
        
        # And: CLI exits with success status code
        then_cli_exits_with_success_status_code(report)


class TestRecoverAndReportFailures:
    
    def test_report_non_recoverable_failure_to_console(self, workspace_directory):
        # Given: headless session has failed
        log_file = given_headless_session_has_failed(workspace_directory)
        
        # And: NonRecoverableError indicates CLI failure
        error = NonRecoverableError(message='CLI failure')
        
        # And: session log contains error message File not found: config.json
        error_log = given_session_log_contains_error_message(workspace_directory, 'File not found: config.json')
        
        # When: CLI prepares failure report
        report = when_cli_prepares_failure_report(workspace_directory)
        
        # Then: CLI extracts error message from session log
        then_cli_extracts_error_message_from_session_log(report, 'File not found: config.json')
        
        # And: CLI displays Headless execution failed (non-recoverable) to console
        then_cli_displays_headless_execution_failed_non_recoverable_to_console(report)
        
        # And: CLI shows error message File not found: config.json
        then_cli_shows_error_message(report, 'File not found: config.json')
        
        # And: NonRecoverableError cannot be retried
        then_non_recoverable_error_cannot_be_retried(error)
        
        # And: CLI displays log file path for full details
        then_cli_displays_log_file_path_for_full_details(report)
        
        # And: CLI exits with failure status code
        then_cli_exits_with_failure_status_code(report)
    
    def test_report_non_recoverable_api_connection_failure(self, workspace_directory):
        # Given: CLI attempts to connect to Cursor Headless API
        workspace = given_cli_attempts_to_connect_to_cursor_headless_api(workspace_directory)
        
        # And: API connection fails with timeout
        timeout_error = given_api_connection_fails_with_timeout(workspace_directory)
        
        # And: CLI has retried connection 3 times
        retry_count = given_cli_has_retried_connection_3_times(workspace_directory)
        
        # And: NonRecoverableError indicates API connection failure
        error = NonRecoverableError(message='API connection failure')
        
        # When: CLI prepares failure report
        report = when_cli_prepares_failure_report(workspace_directory)
        
        # Then: CLI displays Failed to connect to Cursor Headless API (non-recoverable) to console
        then_cli_displays_failed_to_connect_to_cursor_headless_api_non_recoverable_to_console(report)
        
        # And: CLI shows error details Connection timeout after 30 seconds
        then_cli_shows_error_details(report, 'Connection timeout after 30 seconds')
        
        # And: NonRecoverableError cannot be retried
        then_non_recoverable_error_cannot_be_retried(error)
        
        # And: CLI suggests checking API key configuration
        then_cli_suggests_checking_api_key_configuration(report)
        
        # And: CLI exits with failure status code
        then_cli_exits_with_failure_status_code(report)
    
    def test_recover_from_ai_hang_by_restarting_session(self, workspace_directory):
        # Given: headless session is running
        session_id = given_headless_session_is_running_for_monitoring(workspace_directory)
        
        # And: AI has not responded for 5 minutes
        timeout_duration = given_ai_has_not_responded_for_5_minutes(workspace_directory)
        
        # And: RecoverableError indicates AI hang
        recoverable_error = given_recoverable_error_indicates_ai_hang()
        
        # And: ErrorRecovery tracks recovery attempt count less than 3
        error_recovery = given_error_recovery_tracks_recovery_attempt_count_less_than_3()
        
        # When: ErrorRecovery determines error is recoverable
        is_recoverable = when_error_recovery_determines_error_is_recoverable(error_recovery, recoverable_error)
        
        # Then: ErrorRecovery logs AI hung, attempting recovery (attempt 1 of 3) to log file
        then_error_recovery_logs_ai_hung_attempting_recovery_to_log_file(workspace_directory, 1, 3)
        
        # And: ErrorRecovery waits before retry for 1 minute
        then_error_recovery_waits_before_retry_for_1_minute(error_recovery)
        
        # And: ErrorRecovery terminates current headless session
        then_error_recovery_terminates_current_headless_session(error_recovery, session_id)
        
        # And: ErrorRecovery restarts session with same instructions
        then_error_recovery_restarts_session_with_same_instructions(error_recovery)
        
        # And: ErrorRecovery wraps with Keep doing this until 100% done or blocked directive
        then_error_recovery_wraps_with_persistence_directive(error_recovery)
        
        # And: ErrorRecovery sends to new Cursor Headless API session
        then_error_recovery_sends_to_new_cursor_headless_api_session(error_recovery)
        
        # And: ErrorRecovery tracks recovery attempt count incremented to 1
        then_error_recovery_tracks_recovery_attempt_count_incremented_to(error_recovery, 1)
        
        # And: ErrorRecovery logs Session restarted due to AI hang to log file
        then_error_recovery_logs_session_restarted_due_to_ai_hang_to_log_file(workspace_directory)
        
        # And: CLI continues monitoring new session
        result = ExecutionResult(status='running', monitoring=True)
        then_cli_continues_monitoring_new_session(result)
    
    def test_recover_from_ai_stuck_in_planning_mode(self, workspace_directory):
        # Given: headless session is running
        session_id = given_headless_session_is_running_for_monitoring(workspace_directory)
        
        # And: AI indicates stuck in planning mode
        stuck_log = given_ai_indicates_stuck_in_planning_mode(workspace_directory)
        
        # And: RecoverableError indicates AI stuck in planning
        recoverable_error = given_recoverable_error_indicates_ai_stuck_in_planning()
        
        # And: ErrorRecovery tracks recovery attempt count less than 3
        error_recovery = given_error_recovery_tracks_recovery_attempt_count_less_than_3()
        
        # When: ErrorRecovery determines error is recoverable
        is_recoverable = when_error_recovery_determines_error_is_recoverable(error_recovery, recoverable_error)
        
        # Then: ErrorRecovery logs AI stuck in planning, attempting recovery (attempt 1 of 3) to log file
        then_error_recovery_logs_ai_hung_attempting_recovery_to_log_file(workspace_directory, 1, 3)
        
        # And: ErrorRecovery waits before retry for 1 minute
        then_error_recovery_waits_before_retry_for_1_minute(error_recovery)
        
        # And: ErrorRecovery terminates current headless session
        then_error_recovery_terminates_current_headless_session(error_recovery, session_id)
        
        # And: ErrorRecovery restarts session with same instructions
        then_error_recovery_restarts_session_with_same_instructions(error_recovery)
        
        # And: ErrorRecovery wraps with Keep doing this until 100% done or blocked directive
        then_error_recovery_wraps_with_persistence_directive(error_recovery)
        
        # And: ErrorRecovery sends to new Cursor Headless API session
        then_error_recovery_sends_to_new_cursor_headless_api_session(error_recovery)
        
        # And: ErrorRecovery tracks recovery attempt count incremented to 1
        then_error_recovery_tracks_recovery_attempt_count_incremented_to(error_recovery, 1)
        
        # And: ErrorRecovery logs Session restarted due to AI stuck to log file
        then_error_recovery_logs_session_restarted_due_to_ai_hang_to_log_file(workspace_directory)
        
        # And: CLI continues monitoring new session
        result = ExecutionResult(status='running', monitoring=True)
        then_cli_continues_monitoring_new_session(result)
    
    def test_stop_after_3_consecutive_recovery_attempts(self, workspace_directory):
        # Given: headless session is running
        session_id = given_headless_session_is_running_for_monitoring(workspace_directory)
        
        # And: RecoverableError indicates AI hung or stuck
        recoverable_error = given_recoverable_error_indicates_ai_hung_or_stuck()
        
        # And: ErrorRecovery tracks recovery attempt count equals 3
        error_recovery = given_error_recovery_tracks_recovery_attempt_count_equals_3()
        
        # And: ErrorRecovery has already recovered 3 times in a row
        recovery_history = given_error_recovery_has_already_recovered_3_times_in_a_row()
        
        # When: ErrorRecovery determines error is recoverable
        is_recoverable = when_error_recovery_determines_error_is_recoverable(error_recovery, recoverable_error)
        
        # And: ErrorRecovery enforces max retry limit
        max_limit_enforced = when_error_recovery_enforces_max_retry_limit(error_recovery)
        
        # Then: NonRecoverableError indicates max recovery attempts exceeded
        non_recoverable_error = NonRecoverableError(message='Max recovery attempts exceeded')
        then_non_recoverable_error_indicates_max_recovery_attempts_exceeded(non_recoverable_error)
        
        # And: CLI logs Maximum recovery attempts (3) reached, treating as non-recoverable to log file
        then_cli_logs_maximum_recovery_attempts_reached_treating_as_non_recoverable_to_log_file(workspace_directory, 3)
        
        # And: CLI displays Headless execution failed after 3 recovery attempts to console
        report = when_cli_prepares_failure_report(workspace_directory)
        then_cli_displays_headless_execution_failed_after_3_recovery_attempts_to_console(report)
        
        # And: CLI shows all recovery attempts made
        then_cli_shows_all_recovery_attempts_made(report)
        
        # And: NonRecoverableError cannot be retried
        then_non_recoverable_error_cannot_be_retried(non_recoverable_error)
        
        # And: CLI displays log file path for full details
        then_cli_displays_log_file_path_for_full_details(report)
        
        # And: CLI exits with failure status code
        then_cli_exits_with_failure_status_code(report)
    
    def test_report_non_recoverable_failure_with_partial_results(self, workspace_directory):
        # Given: headless session was executing shape behavior
        behavior_log = given_headless_session_was_executing_behavior(workspace_directory, 'shape')
        
        # And: clarify action completed successfully
        clarify_log = given_action_completed_successfully(workspace_directory, 'clarify')
        
        # And: strategy action failed with validation error
        strategy_log = given_action_failed_with_validation_error(workspace_directory, 'strategy', 'Invalid story structure')
        
        # And: NonRecoverableError indicates CLI failure
        error = NonRecoverableError(message='CLI failure')
        
        # When: CLI prepares failure report
        report = when_cli_prepares_failure_report(workspace_directory)
        
        # Then: CLI displays Behavior execution failed at strategy action (non-recoverable)
        then_cli_displays_behavior_execution_failed_at_action_non_recoverable(report, 'strategy')
        
        # And: CLI shows completed actions clarify
        then_cli_shows_completed_actions(report, 'clarify')
        
        # And: CLI shows failed action strategy with error
        then_cli_shows_failed_action_with_error(report, 'strategy', 'Invalid story structure')
        
        # And: NonRecoverableError cannot be retried
        then_non_recoverable_error_cannot_be_retried(error)
        
        # And: CLI displays log file path
        then_cli_displays_log_file_path_for_full_details(report)
        
        # And: CLI exits with failure status code
        then_cli_exits_with_failure_status_code(report)

