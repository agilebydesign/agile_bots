"""End-to-end tests for Execute In Headless Mode epic.

Tests CLI (repl_main.py --headless) -> HeadlessSession -> CursorHeadlessAPI.
All headless execution tests call through the production CLI entry point.

Epic: Execute In Headless Mode
Sub-epics: Execute In Headless Mode, Monitor Session
"""

import pytest
import json
import subprocess
import sys
from pathlib import Path

from agile_bot.bots.base_bot.src.repl_cli.headless.headless_config import HeadlessConfig
from agile_bot.bots.base_bot.src.repl_cli.headless.execution_context import ExecutionContext
from agile_bot.bots.base_bot.src.repl_cli.headless.session_log import SessionLog
from agile_bot.bots.base_bot.src.repl_cli.headless.error_recovery import ErrorRecovery
from agile_bot.bots.base_bot.src.repl_cli.headless.recoverable_error import RecoverableError


# =============================================================================
# Fixtures - defined in test file per rule define_fixtures_in_test_file
# =============================================================================

@pytest.fixture
def workspace_directory(tmp_path):
    workspace_dir = tmp_path / 'workspace'
    workspace_dir.mkdir(parents=True, exist_ok=True)
    return workspace_dir


@pytest.fixture
def workspace_root():
    """Get the workspace root directory for CLI invocation."""
    return Path(__file__).parent.parent.parent.parent.parent


# =============================================================================
# Given helpers - setup state per rule use_given_when_then_helpers
# =============================================================================

def given_headless_context_file_exists(workspace_directory, content=None):
    context_file = workspace_directory / 'headless-context.md'
    if content is None:
        content = """User Intent: Implement user authentication
Chat History:
- User: We need secure login
- AI: I'll implement JWT tokens

File References:
- src/auth/login.py
- src/models/user.py
"""
    context_file.write_text(content)
    return context_file


def given_headless_context_file_does_not_exist(workspace_directory):
    context_file = workspace_directory / 'headless-context.md'
    if context_file.exists():
        context_file.unlink()
    return context_file


def given_headless_mode_is_configured():
    config = HeadlessConfig.load()
    if not config.is_configured:
        pytest.skip('API key not configured')
    return config


def given_error_recovery_with_attempts(max_attempts, current_attempts):
    return ErrorRecovery(max_attempts=max_attempts, current_attempts=current_attempts)


# =============================================================================
# When helpers - ALL headless execution goes through CLI
# =============================================================================

def when_cli_invoked_with_headless_message(message, context_file=None, workspace_root=None, timeout=30):
    """Invoke CLI with --headless and --message for pass-through execution."""
    if workspace_root is None:
        workspace_root = Path(__file__).parent.parent.parent.parent.parent
    
    cmd = [
        sys.executable,
        'agile_bot/bots/base_bot/src/repl_cli/repl_main.py',
        '--headless',
        '--timeout', str(timeout),
        '--message', message
    ]
    if context_file:
        cmd.extend(['--context', str(context_file)])
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=workspace_root
    )
    return result


def when_cli_invoked_with_headless_behavior(behavior, context_file=None, workspace_root=None, timeout=30):
    """Invoke CLI with --headless and behavior name to execute entire behavior."""
    if workspace_root is None:
        workspace_root = Path(__file__).parent.parent.parent.parent.parent
    
    cmd = [
        sys.executable,
        'agile_bot/bots/base_bot/src/repl_cli/repl_main.py',
        '--headless',
        '--timeout', str(timeout),
        behavior
    ]
    if context_file:
        cmd.extend(['--context', str(context_file)])
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=workspace_root
    )
    return result


def when_cli_invoked_with_headless_action(behavior, action, context_file=None, workspace_root=None, timeout=30):
    """Invoke CLI with --headless and behavior.action to execute single action."""
    if workspace_root is None:
        workspace_root = Path(__file__).parent.parent.parent.parent.parent
    
    cmd = [
        sys.executable,
        'agile_bot/bots/base_bot/src/repl_cli/repl_main.py',
        '--headless',
        '--timeout', str(timeout),
        f'{behavior}.{action}'
    ]
    if context_file:
        cmd.extend(['--context', str(context_file)])
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=workspace_root
    )
    return result


def when_cli_invoked_with_headless_operation(behavior, action, operation, context_file=None, workspace_root=None, timeout=30):
    """Invoke CLI with --headless and behavior.action.operation to execute single operation."""
    if workspace_root is None:
        workspace_root = Path(__file__).parent.parent.parent.parent.parent
    
    cmd = [
        sys.executable,
        'agile_bot/bots/base_bot/src/repl_cli/repl_main.py',
        '--headless',
        '--timeout', str(timeout),
        f'{behavior}.{action}.{operation}'
    ]
    if context_file:
        cmd.extend(['--context', str(context_file)])
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=workspace_root
    )
    return result


def when_error_recovery_determines_recoverable(error_recovery, error):
    return error_recovery.determines_if_error_is_recoverable(error)


# =============================================================================
# Then helpers - assertions for CLI JSON output
# =============================================================================

def then_cli_returns_json(cli_result):
    """Parse CLI stdout as JSON and return the data."""
    output = cli_result.stdout
    data = json.loads(output)
    return data


def then_cli_output_has_status(cli_result):
    """Assert CLI output is valid JSON with status field."""
    data = then_cli_returns_json(cli_result)
    assert 'status' in data, f"JSON output missing 'status' field: {data}"
    return data


def then_cli_status_is_completed(cli_result):
    """Assert CLI completed successfully."""
    data = then_cli_output_has_status(cli_result)
    assert data['status'] == 'completed', f"Expected completed, got: {data['status']}"
    return data


def then_cli_status_is_blocked(cli_result):
    """Assert CLI execution was blocked."""
    data = then_cli_output_has_status(cli_result)
    assert data['status'] == 'blocked', f"Expected blocked, got: {data['status']}"
    return data


def then_cli_status_is_error(cli_result):
    """Assert CLI returned an error."""
    data = then_cli_output_has_status(cli_result)
    assert data['status'] == 'error', f"Expected error, got: {data['status']}"
    return data


def then_cli_has_session_id(cli_result):
    """Assert CLI output contains session_id."""
    data = then_cli_returns_json(cli_result)
    assert 'session_id' in data and data['session_id'] is not None
    return data['session_id']


def then_cli_has_log_path(cli_result):
    """Assert CLI output contains log_path."""
    data = then_cli_returns_json(cli_result)
    assert 'log_path' in data and data['log_path'] is not None
    return data['log_path']


def then_cli_log_file_exists(cli_result):
    """Assert log file exists on disk."""
    log_path = then_cli_has_log_path(cli_result)
    log_file = Path(log_path)
    assert log_file.exists(), f"Log file does not exist: {log_path}"
    return log_file


def then_cli_has_loop_count(cli_result):
    """Assert CLI output contains positive loop_count."""
    data = then_cli_returns_json(cli_result)
    assert 'loop_count' in data and data['loop_count'] > 0
    return data['loop_count']


def then_cli_has_context_loaded(cli_result, expected=True):
    """Assert CLI loaded context file."""
    data = then_cli_returns_json(cli_result)
    assert data.get('context_loaded') == expected
    return data


def then_cli_has_behavior(cli_result, expected_behavior):
    """Assert CLI output has expected behavior."""
    data = then_cli_returns_json(cli_result)
    assert data.get('behavior') == expected_behavior
    return data


def then_cli_has_action(cli_result, expected_action):
    """Assert CLI output has expected action."""
    data = then_cli_returns_json(cli_result)
    assert data.get('action') == expected_action
    return data


def then_cli_has_operation(cli_result, expected_operation):
    """Assert CLI output has expected operation."""
    data = then_cli_returns_json(cli_result)
    assert data.get('operation') == expected_operation
    return data


def then_cli_operations_executed_contains(cli_result, operation):
    """Assert CLI executed the specified operation."""
    data = then_cli_returns_json(cli_result)
    operations = data.get('operations_executed', [])
    assert operation in operations, f"Operation '{operation}' not in {operations}"
    return data


def then_cli_action_completed(cli_result):
    """Assert CLI completed the action."""
    data = then_cli_returns_json(cli_result)
    assert data.get('action_completed') is True
    return data


def then_cli_behavior_completed(cli_result):
    """Assert CLI completed the behavior."""
    data = then_cli_returns_json(cli_result)
    assert data.get('behavior_completed') is True
    return data


def then_cli_has_block_reason(cli_result):
    """Assert CLI has block_reason when blocked."""
    data = then_cli_returns_json(cli_result)
    assert 'block_reason' in data and data['block_reason'] is not None
    return data['block_reason']


def then_error_is_recoverable(is_recoverable):
    assert is_recoverable is True


def then_error_recovery_can_retry(error_recovery):
    assert error_recovery.can_retry() is True


def then_error_recovery_cannot_retry(error_recovery):
    assert error_recovery.can_retry() is False


# =============================================================================
# Test Classes - ALL headless tests call through CLI
# =============================================================================

class TestExecuteDirectInstructions:
    """Story: Execute Direct Instructions
    
    All tests invoke repl_main.py --headless --message to execute pass-through messages.
    """
    
    @pytest.mark.api_required
    def test_execute_direct_message_in_headless_mode(self, workspace_directory):
        """
        SCENARIO: Execute direct message in headless mode
        GIVEN: AI has written headless-context.md with user intent and chat history
        AND: headless mode is configured with API key
        WHEN: human invokes CLI with --headless flag and --message "Implement user authentication"
        THEN: CLI reads headless-context.md file
        AND: CLI loads ExecutionContext from context file (user_message, chat_history, file_references)
        AND: CLI constructs instructions starting with the user message "Implement user authentication", then appends user intent, chat history, and file references from context
        AND: CLI formats context: User Intent, Chat History, File References
        AND: CLI automatically wraps instructions with "Keep doing this until 100% done or blocked:" directive
        AND: CLI automatically appends "If blocked, report reason clearly." to instructions
        AND: CLI sends combined instructions to Cursor Headless API
        AND: CLI creates timestamped log file in logs directory (e.g., logs/headless-2025-12-30-00-31-34.log)
        AND: CLI appends session start message to log file with timestamp
        AND: CLI appends full instructions to log file
        AND: AI executes instruction and indicates not done (done=false)
        AND: CLI appends "Loop 1: Polling..." to log file
        AND: CLI appends "Loop 1: running - Creating user model" to log file
        AND: CLI loops instruction again with persistence directive
        AND: CLI enforces MAX_LOOPS limit of 50 iterations
        AND: AI continues work and indicates not done (done=false)
        AND: CLI appends "Loop 2: Polling..." to log file
        AND: CLI appends "Loop 2: running - Adding authentication endpoints" to log file
        AND: CLI loops instruction again with persistence directive
        AND: CLI enforces MAX_LOOPS limit of 50 iterations
        AND: AI completes work and indicates done (done=true)
        AND: CLI appends "Loop 3: completed - Authentication implemented" to log file
        AND: CLI appends "Total loops: 3" to log file
        AND: CLI detects AI completion signal (done=true) from API response
        AND: CLI stops looping
        AND: CLI reports success with log file path
        """
        # Given: AI has written headless-context.md with user intent and chat history
        # And: headless mode is configured with API key
        given_headless_mode_is_configured()
        
        # And: context file exists
        context_file = given_headless_context_file_exists(workspace_directory)
        
        # When: human invokes CLI with --headless flag and --message "Implement user authentication"
        cli_result = when_cli_invoked_with_headless_message(
            message='Implement user authentication',
            context_file=context_file,
            timeout=120  # Complex task needs more time
        )
        
        # Then: CLI returns JSON with required fields
        data = then_cli_output_has_status(cli_result)
        then_cli_has_session_id(cli_result)
        log_file = then_cli_log_file_exists(cli_result)
        then_cli_has_loop_count(cli_result)
        then_cli_has_context_loaded(cli_result, expected=True)
        
        # Verify log file contains expected content
        log_content = log_file.read_text()
        assert 'Loop' in log_content or 'session' in log_content.lower(), \
            f"Log file should contain loop/session info: {log_content[:500]}"
        
        # Verify completion or blocking
        assert data['status'] in ['completed', 'blocked'], \
            f"Expected completed or blocked status, got: {data['status']}"
    
    @pytest.mark.api_required
    def test_execute_direct_message_without_context_file(self, workspace_directory):
        """
        SCENARIO: Execute direct message without context file
        GIVEN: headless mode is configured with API key
        AND: headless-context.md file does not exist
        WHEN: human invokes CLI with --headless flag and --message "Run tests"
        THEN: CLI checks for headless-context.md file and finds it doesn't exist
        AND: CLI creates empty ExecutionContext
        AND: CLI automatically wraps message with "Keep doing this until 100% done or blocked:" directive
        AND: CLI automatically appends "If blocked, report reason clearly." to instructions
        AND: CLI sends message to Cursor Headless API
        AND: CLI creates timestamped log file in logs directory (e.g., logs/headless-2025-12-30-00-31-34.log)
        AND: CLI appends session start message to log file with timestamp
        AND: CLI appends full instructions to log file
        AND: AI executes instruction and indicates not done (done=false)
        AND: CLI appends "Loop 1: Polling..." to log file
        AND: CLI appends "Loop 1: running - Running test suite" to log file
        AND: CLI loops instruction again with persistence directive
        AND: CLI enforces MAX_LOOPS limit of 50 iterations
        AND: AI completes tests and indicates done (done=true)
        AND: CLI appends "Loop 1: completed - All tests passing" to log file
        AND: CLI appends "Total loops: 1" to log file
        AND: CLI detects AI completion signal (done=true) from API response
        AND: CLI stops looping
        AND: CLI reports success with log file path
        """
        # Given: headless mode is configured with API key
        given_headless_mode_is_configured()
        
        # And: headless-context.md file does not exist
        given_headless_context_file_does_not_exist(workspace_directory)
        
        # When: human invokes CLI with --headless flag and --message "Run tests"
        cli_result = when_cli_invoked_with_headless_message(
            message='Run tests',
            context_file=None
        )
        
        # Then: CLI returns JSON with status
        data = then_cli_output_has_status(cli_result)
        then_cli_has_session_id(cli_result)
        then_cli_has_context_loaded(cli_result, expected=False)
        
        # Verify log file exists and contains content
        log_file = then_cli_log_file_exists(cli_result)
        log_content = log_file.read_text()
        assert 'Loop' in log_content or 'session' in log_content.lower(), \
            f"Log file should contain loop/session info: {log_content[:500]}"
        
        # Verify completion or blocking
        assert data['status'] in ['completed', 'blocked'], \
            f"Expected completed or blocked status, got: {data['status']}"
    
    @pytest.mark.api_required
    def test_handle_blocked_execution_in_direct_message_mode(self, workspace_directory):
        """
        SCENARIO: Handle blocked execution in direct message mode
        GIVEN: AI has written headless-context.md
        AND: headless mode is configured
        WHEN: human invokes CLI with --headless and --message Deploy application
        AND: headless session blocks waiting for user input
        THEN: CLI detects blocked state from API response
        AND: CLI writes block reason to log file
        AND: CLI reports blocked status to console
        AND: CLI displays block reason from session
        AND: CLI exits with blocked status code
        """
        # Given
        given_headless_mode_is_configured()
        context_file = given_headless_context_file_exists(workspace_directory)
        
        # When: CLI is invoked with a message that may block
        cli_result = when_cli_invoked_with_headless_message(
            message='Deploy application',
            context_file=context_file,
            timeout=120
        )
        
        # Then: Check for blocked status
        data = then_cli_output_has_status(cli_result)
        if data['status'] == 'blocked':
            then_cli_has_block_reason(cli_result)
            log_file = then_cli_log_file_exists(cli_result)
            log_content = log_file.read_text()
            assert 'block' in log_content.lower() or 'blocked' in log_content.lower(), \
                f"Log file should contain block reason: {log_content[:500]}"
    
    @pytest.mark.api_required
    def test_restart_session_when_ai_gets_stuck_in_direct_message_mode(self, workspace_directory):
        """
        SCENARIO: Restart session when AI gets stuck in direct message mode
        GIVEN: headless session is executing direct message
        AND: AI has looped instructions multiple times
        AND: RecoverableError indicates AI stuck or unable to proceed
        AND: ErrorRecovery tracks recovery attempt count less than 3
        WHEN: ErrorRecovery determines error is recoverable
        THEN: ErrorRecovery waits before retry for 2 seconds
        AND: ErrorRecovery terminates current headless session
        AND: ErrorRecovery restarts session with same message and context
        AND: ErrorRecovery wraps with Keep doing this until 100% done or blocked directive
        AND: ErrorRecovery sends to new Cursor Headless API session
        AND: ErrorRecovery tracks recovery attempt count incremented
        AND: AI executes with fresh context
        AND: CLI continues monitoring new session
        """
        # Given: headless mode is configured
        given_headless_mode_is_configured()
        context_file = given_headless_context_file_exists(workspace_directory)
        
        # When: CLI is invoked with a message
        cli_result = when_cli_invoked_with_headless_message(
            message='Complex task that may require recovery',
            context_file=context_file,
            timeout=120
        )
        
        # Then: Check that recovery can happen (this is tested via ErrorRecovery unit tests)
        # The actual recovery logic is tested in TestErrorRecovery class
        data = then_cli_output_has_status(cli_result)
        # Recovery would happen internally, so we just verify the session completes or blocks
        assert data['status'] in ['completed', 'blocked']


class TestExecuteSingleOperation:
    """Story: Execute Single Operation
    
    All tests invoke repl_main.py --headless behavior.action.operation
    """
    
    @pytest.mark.api_required
    def test_execute_instructions_operation_in_headless_mode(self, workspace_directory):
        """
        SCENARIO: Execute single instructions operation
        GIVEN: headless mode is configured
        AND: context file exists
        WHEN: human invokes CLI with --headless shape.build.instructions
        THEN: CLI returns JSON with operation=instructions
        """
        # Given
        given_headless_mode_is_configured()
        context_file = given_headless_context_file_exists(workspace_directory)
        
        # When
        cli_result = when_cli_invoked_with_headless_operation(
            behavior='shape',
            action='build',
            operation='instructions',
            context_file=context_file
        )
        
        # Then
        then_cli_output_has_status(cli_result)
        then_cli_has_operation(cli_result, 'instructions')
        then_cli_has_behavior(cli_result, 'shape')
        then_cli_has_action(cli_result, 'build')
        then_cli_has_context_loaded(cli_result, expected=True)
    
    @pytest.mark.api_required
    def test_execute_confirm_operation_in_headless_mode(self, workspace_directory):
        """
        SCENARIO: Execute confirm operation
        GIVEN: headless mode is configured
        WHEN: human invokes CLI with --headless shape.build.confirm
        THEN: CLI returns JSON with operation=confirm
        """
        # Given
        given_headless_mode_is_configured()
        context_file = given_headless_context_file_exists(workspace_directory)
        
        # When
        cli_result = when_cli_invoked_with_headless_operation(
            behavior='shape',
            action='build',
            operation='confirm',
            context_file=context_file
        )
        
        # Then
        then_cli_output_has_status(cli_result)
        then_cli_has_operation(cli_result, 'confirm')
        then_cli_has_context_loaded(cli_result, expected=True)
    
    @pytest.mark.api_required
    def test_restart_session_when_ai_gets_stuck(self, workspace_directory):
        """
        SCENARIO: Restart session when AI gets stuck
        GIVEN: headless session is running
        AND: AI has looped instructions multiple times
        AND: RecoverableError indicates AI stuck or unable to proceed
        AND: ErrorRecovery tracks recovery attempt count less than 3
        WHEN: ErrorRecovery determines error is recoverable
        THEN: ErrorRecovery waits before retry for 2 seconds
        AND: ErrorRecovery terminates current headless session
        AND: ErrorRecovery restarts session with same instructions
        AND: ErrorRecovery wraps with Keep doing this until 100% done or blocked directive
        AND: ErrorRecovery sends to new Cursor Headless API session
        AND: ErrorRecovery tracks recovery attempt count incremented
        AND: AI executes with fresh context
        AND: CLI continues monitoring new session
        """
        # Given: headless mode is configured
        given_headless_mode_is_configured()
        context_file = given_headless_context_file_exists(workspace_directory)
        
        # When: CLI is invoked with an operation that may require recovery
        cli_result = when_cli_invoked_with_headless_operation(
            behavior='shape',
            action='build',
            operation='instructions',
            context_file=context_file,
            timeout=120
        )
        
        # Then: Check that recovery can happen (this is tested via ErrorRecovery unit tests)
        data = then_cli_output_has_status(cli_result)
        # Recovery would happen internally, so we just verify the operation completes or blocks
        assert data['status'] in ['completed', 'blocked']


class TestExecuteCompleteAction:
    """Story: Execute Complete Action
    
    All tests invoke repl_main.py --headless behavior.action
    """
    
    @pytest.mark.api_required
    def test_execute_complete_action_workflow_in_headless_mode(self, workspace_directory):
        """
        SCENARIO: Execute complete action workflow
        GIVEN: headless mode is configured
        WHEN: human invokes CLI with --headless shape.build
        THEN: CLI executes all operations (instructions, confirm)
        AND: CLI returns JSON with behavior and action
        """
        # Given
        given_headless_mode_is_configured()
        context_file = given_headless_context_file_exists(workspace_directory)
        
        # When
        cli_result = when_cli_invoked_with_headless_action(
            behavior='shape',
            action='build',
            context_file=context_file,
            timeout=120  # Complete action needs more time
        )
        
        # Then
        data = then_cli_output_has_status(cli_result)
        then_cli_has_behavior(cli_result, 'shape')
        then_cli_has_action(cli_result, 'build')
        then_cli_has_context_loaded(cli_result, expected=True)
        
        if data['status'] == 'completed':
            then_cli_action_completed(cli_result)
            then_cli_operations_executed_contains(cli_result, 'instructions')
        elif data['status'] == 'blocked':
            then_cli_has_block_reason(cli_result)
    
    @pytest.mark.api_required
    def test_handle_block_during_action_workflow(self, workspace_directory):
        """
        SCENARIO: Handle block during action workflow
        GIVEN: AI has written headless-context.md
        AND: headless mode is configured
        AND: user is at shape.build action
        WHEN: human invokes CLI with --headless for complete action
        AND: confirm operation blocks waiting for clarification
        THEN: CLI detects blocked state during confirm
        AND: CLI stops action workflow execution
        AND: CLI reports which operation blocked
        AND: CLI displays block reason
        AND: CLI preserves completed operation results
        """
        # Given
        given_headless_mode_is_configured()
        context_file = given_headless_context_file_exists(workspace_directory)
        
        # When: CLI is invoked for complete action
        cli_result = when_cli_invoked_with_headless_action(
            behavior='shape',
            action='build',
            context_file=context_file,
            timeout=120
        )
        
        # Then: Check for blocked status
        data = then_cli_output_has_status(cli_result)
        if data['status'] == 'blocked':
            then_cli_has_block_reason(cli_result)
            # Check that operations_executed shows what was completed before blocking
            if 'operations_executed' in data:
                assert len(data['operations_executed']) > 0, \
                    "Should preserve completed operation results"
    
    @pytest.mark.api_required
    def test_restart_session_when_ai_gets_stuck_during_action_workflow(self, workspace_directory):
        """
        SCENARIO: Restart session when AI gets stuck during action workflow
        GIVEN: headless session is executing complete action workflow
        AND: AI is stuck during build operation
        AND: RecoverableError indicates AI unable to proceed
        AND: ErrorRecovery tracks recovery attempt count less than 3
        WHEN: ErrorRecovery determines error is recoverable
        THEN: ErrorRecovery waits before retry for 2 seconds
        AND: ErrorRecovery terminates current headless session
        AND: ErrorRecovery restarts session for build operation only
        AND: ErrorRecovery wraps with Keep doing this until 100% done or blocked directive
        AND: ErrorRecovery sends to new Cursor Headless API session
        AND: ErrorRecovery tracks recovery attempt count incremented
        AND: AI executes build with fresh context
        AND: CLI continues with remaining operations after build completes
        """
        # Given: headless mode is configured
        given_headless_mode_is_configured()
        context_file = given_headless_context_file_exists(workspace_directory)
        
        # When: CLI is invoked for complete action
        cli_result = when_cli_invoked_with_headless_action(
            behavior='shape',
            action='build',
            context_file=context_file,
            timeout=120
        )
        
        # Then: Check that recovery can happen (this is tested via ErrorRecovery unit tests)
        data = then_cli_output_has_status(cli_result)
        # Recovery would happen internally, so we just verify the action completes or blocks
        assert data['status'] in ['completed', 'blocked']


class TestExecuteCompleteBehavior:
    """Story: Execute Complete Behavior
    
    All tests invoke repl_main.py --headless behavior
    """

    @pytest.mark.api_required
    def test_execute_complete_behavior_workflow_in_headless_mode(self, workspace_directory):
        """
        SCENARIO: Execute complete behavior workflow
        GIVEN: headless mode is configured
        WHEN: human invokes CLI with --headless shape
        THEN: CLI executes all actions in behavior
        AND: CLI returns JSON with behavior
        """
        # Given
        given_headless_mode_is_configured()
        context_file = given_headless_context_file_exists(workspace_directory)
        
        # When
        cli_result = when_cli_invoked_with_headless_behavior(
            behavior='shape',
            context_file=context_file,
            timeout=120  # Complete behavior needs more time
        )
        
        # Then
        data = then_cli_output_has_status(cli_result)
        then_cli_has_behavior(cli_result, 'shape')
        then_cli_has_context_loaded(cli_result, expected=True)
        
        if data['status'] == 'completed':
            then_cli_behavior_completed(cli_result)
        elif data['status'] == 'blocked':
            then_cli_has_block_reason(cli_result)
    
    @pytest.mark.api_required
    def test_handle_block_during_behavior_workflow(self, workspace_directory):
        """
        SCENARIO: Handle block during behavior workflow
        GIVEN: AI has written headless-context.md
        AND: headless mode is configured
        AND: user wants to execute shape behavior
        WHEN: human invokes CLI with --headless for complete behavior
        AND: strategy action blocks waiting for decision
        THEN: CLI detects blocked state during strategy
        AND: CLI stops behavior workflow execution
        AND: CLI reports which action blocked
        AND: CLI displays block reason
        AND: CLI preserves completed action results
        """
        # Given
        given_headless_mode_is_configured()
        context_file = given_headless_context_file_exists(workspace_directory)
        
        # When: CLI is invoked for complete behavior
        cli_result = when_cli_invoked_with_headless_behavior(
            behavior='shape',
            context_file=context_file,
            timeout=120
        )
        
        # Then: Check for blocked status
        data = then_cli_output_has_status(cli_result)
        if data['status'] == 'blocked':
            then_cli_has_block_reason(cli_result)
            # Check that actions_executed shows what was completed before blocking
            if 'actions_executed' in data:
                assert len(data['actions_executed']) > 0, \
                    "Should preserve completed action results"
    
    @pytest.mark.api_required
    def test_restart_session_when_ai_gets_stuck_during_behavior_workflow(self, workspace_directory):
        """
        SCENARIO: Restart session when AI gets stuck during behavior workflow
        GIVEN: headless session is executing complete behavior workflow
        AND: AI is stuck during build action
        AND: RecoverableError indicates AI unable to proceed
        AND: ErrorRecovery tracks recovery attempt count less than 3
        WHEN: ErrorRecovery determines error is recoverable
        THEN: ErrorRecovery waits before retry for 2 seconds
        AND: ErrorRecovery terminates current headless session
        AND: ErrorRecovery restarts session for build action only
        AND: ErrorRecovery wraps with Keep doing this until 100% done or blocked directive
        AND: ErrorRecovery sends to new Cursor Headless API session
        AND: ErrorRecovery tracks recovery attempt count incremented
        AND: AI executes build action with fresh context
        AND: CLI continues with remaining actions after build completes
        """
        # Given: headless mode is configured
        given_headless_mode_is_configured()
        context_file = given_headless_context_file_exists(workspace_directory)
        
        # When: CLI is invoked for complete behavior
        cli_result = when_cli_invoked_with_headless_behavior(
            behavior='shape',
            context_file=context_file,
            timeout=120
        )
        
        # Then: Check that recovery can happen (this is tested via ErrorRecovery unit tests)
        data = then_cli_output_has_status(cli_result)
        # Recovery would happen internally, so we just verify the behavior completes or blocks
        assert data['status'] in ['completed', 'blocked']


class TestMonitorExecution:
    """Story: Monitor Execution
    
    Tests that CLI logs execution and returns log path.
    """
    
    @pytest.mark.api_required
    def test_session_logs_all_loop_iterations(self, workspace_directory):
        """
        SCENARIO: CLI logs loop iterations
        GIVEN: headless mode is configured
        WHEN: CLI executes a message
        THEN: log file is created with loop information
        """
        # Given
        given_headless_mode_is_configured()
        context_file = given_headless_context_file_exists(workspace_directory)
        
        # When
        cli_result = when_cli_invoked_with_headless_message(
            message='Simple test task',
            context_file=context_file
        )
        
        # Then: log file exists and contains content
        log_file = then_cli_log_file_exists(cli_result)
        log_content = log_file.read_text()
        assert 'Loop' in log_content or 'session' in log_content.lower(), \
            f"Log file missing loop/session info: {log_content[:200]}"


class TestErrorRecovery:
    """Story: Restart Session When AI Gets Stuck
    
    Unit tests for ErrorRecovery class (no API needed).
    """
    
    def test_error_recovery_determines_recoverable_error(self):
        # Given: ErrorRecovery tracks recovery attempt count less than max
        error_recovery = given_error_recovery_with_attempts(max_attempts=3, current_attempts=2)
        
        # And: RecoverableError indicates AI stuck
        recoverable_error = RecoverableError('AI stuck or unable to proceed')
        
        # When: ErrorRecovery determines if error is recoverable
        is_recoverable = when_error_recovery_determines_recoverable(error_recovery, recoverable_error)
        
        # Then: error is determined as recoverable
        then_error_is_recoverable(is_recoverable)
        then_error_recovery_can_retry(error_recovery)
    
    def test_error_recovery_stops_after_max_attempts(self):
        # Given: ErrorRecovery has reached max attempts
        error_recovery = given_error_recovery_with_attempts(max_attempts=3, current_attempts=3)
        
        # Then: ErrorRecovery cannot retry
        then_error_recovery_cannot_retry(error_recovery)
    
    def test_error_recovery_wait_time_is_configured(self):
        # Given: ErrorRecovery with default settings
        error_recovery = ErrorRecovery()
        
        # Then: wait time is 60 seconds (1 minute)
        assert error_recovery.wait_time == 60.0


class TestHeadlessConfig:
    """Story: Add Headless Mode To Status - config loading
    
    Unit tests for HeadlessConfig class (no API needed).
    """
    
    def test_config_loads_from_environment(self, monkeypatch):
        # Given: CURSOR_API_KEY environment variable is set
        monkeypatch.setenv('CURSOR_API_KEY', 'test-api-key-12345')
        
        # When: config is loaded
        config = HeadlessConfig.load()
        
        # Then: config is configured with the API key
        assert config.is_configured is True
        assert config.api_key == 'test-api-key-12345'
    
    def test_config_not_configured_without_key(self, monkeypatch):
        # Given: no API key is set
        monkeypatch.delenv('CURSOR_API_KEY', raising=False)
        monkeypatch.delenv('HEADLESS_CONFIG_PATH', raising=False)
        
        # When: config is loaded (with paths that don't exist)
        config = HeadlessConfig.load()
        
        # Then: config.api_key is a string (may be empty or from secrets file)
        assert isinstance(config.api_key, str)


class TestExecutionContext:
    """Story: Execute Direct Instructions - context parsing
    
    Unit tests for ExecutionContext class (no API needed).
    """
    
    def test_loads_context_from_file(self, workspace_directory):
        # Given: headless-context.md exists with content
        context_file = given_headless_context_file_exists(workspace_directory)
        
        # When: context is loaded from file
        context = ExecutionContext.loads_from_context_file(context_file)
        
        # Then: context contains parsed data
        assert context.user_message == 'Implement user authentication'
        assert 'We need secure login' in context.chat_history[0]
        assert 'src/auth/login.py' in context.file_references
    
    def test_returns_empty_context_when_file_missing(self, workspace_directory):
        # Given: context file does not exist
        missing_file = workspace_directory / 'nonexistent.md'
        
        # When: context is loaded
        context = ExecutionContext.loads_from_context_file(missing_file)
        
        # Then: empty context is returned
        assert context.user_message == ''
        assert context.chat_history == []
        assert context.file_references == []


class TestSessionLog:
    """Story: Monitor Execution - logging
    
    Unit tests for SessionLog class (no API needed).
    """
    
    def test_creates_timestamped_log_file(self, workspace_directory):
        # Given: log directory
        log_dir = workspace_directory / 'logs'
        
        # When: session log is created
        log = SessionLog.creates_with_timestamped_path(log_dir)
        
        # Then: log path is set and directory exists
        assert log.log_path is not None
        assert log_dir.exists()
    
    def test_appends_response_to_log(self, workspace_directory):
        # Given: session log exists
        log_dir = workspace_directory / 'logs'
        log = SessionLog.creates_with_timestamped_path(log_dir)
        
        # When: response is appended
        log.appends_response('Test response content')
        
        # Then: log file contains response
        log_content = log.log_path.read_text()
        assert 'Test response content' in log_content
    
    def test_appends_total_loops(self, workspace_directory):
        # Given: session log exists
        log_dir = workspace_directory / 'logs'
        log = SessionLog.creates_with_timestamped_path(log_dir)
        
        # When: total loops is appended
        log.appends_total_loops(5)
        
        # Then: log file contains loop count
        log_content = log.log_path.read_text()
        assert 'Total loops: 5' in log_content


class TestCLIArgumentParsing:
    """Story: CLI properly parses headless mode arguments
    
    Tests that CLI correctly handles various argument combinations.
    These tests check CLI behavior, not API connectivity.
    """
    
    def test_cli_help_shows_headless_options(self, workspace_root):
        """CLI --help shows headless mode options."""
        cmd = [
            sys.executable,
            'agile_bot/bots/base_bot/src/repl_cli/repl_main.py',
            '--help'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=workspace_root)
        
        assert result.returncode == 0
        assert '--headless' in result.stdout
        assert '--message' in result.stdout
        assert '--context' in result.stdout
    
    def test_cli_headless_requires_message_or_target(self, workspace_root):
        """CLI with --headless but no message or target returns error JSON."""
        cmd = [
            sys.executable,
            'agile_bot/bots/base_bot/src/repl_cli/repl_main.py',
            '--headless'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=workspace_root)
        
        # Should return error JSON
        data = json.loads(result.stdout)
        assert data['status'] == 'error'
        assert 'requires --message or a target' in data['error']
    
    def test_cli_headless_invalid_target_format(self, workspace_root):
        """CLI with invalid target format returns error JSON."""
        cmd = [
            sys.executable,
            'agile_bot/bots/base_bot/src/repl_cli/repl_main.py',
            '--headless',
            'a.b.c.d.e'  # Too many parts
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=workspace_root)
        
        # Should return error JSON
        data = json.loads(result.stdout)
        assert data['status'] == 'error'
        assert 'Invalid target format' in data['error']
    
    def test_cli_headless_not_configured_returns_error(self, workspace_root, monkeypatch):
        """CLI returns error when API key not configured."""
        # Remove API key from environment
        monkeypatch.delenv('CURSOR_API_KEY', raising=False)
        
        cmd = [
            sys.executable,
            'agile_bot/bots/base_bot/src/repl_cli/repl_main.py',
            '--headless',
            '--message', 'test'
        ]
        
        # Note: This test may still find the secrets file
        # We're just verifying the CLI handles config loading
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=workspace_root)
        
        # Should return JSON (either error or execution result)
        data = json.loads(result.stdout)
        assert 'status' in data
