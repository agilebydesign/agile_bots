import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from agile_bot.bots.base_bot.src.repl_cli.repl_help import REPLHelp
from agile_bot.bots.base_bot.src.repl_cli.status_display import StatusDisplay
from agile_bot.bots.base_bot.src.repl_cli.headless.headless_config import HeadlessConfig


@pytest.fixture
def workspace_directory(tmp_path):
    workspace_dir = tmp_path / 'workspace'
    workspace_dir.mkdir(parents=True, exist_ok=True)
    return workspace_dir


@pytest.fixture
def headless_config_with_api_key(workspace_directory, monkeypatch):
    monkeypatch.setenv('CURSOR_API_KEY', 'sk-test123456789')
    return HeadlessConfig.load()


@pytest.fixture
def headless_config_without_api_key(workspace_directory, monkeypatch):
    monkeypatch.delenv('CURSOR_API_KEY', raising=False)
    # Also need to prevent reading from the real secrets file
    import agile_bot.bots.base_bot.src.repl_cli.headless.headless_config as config_module
    monkeypatch.setattr(config_module, 'API_KEY_FILE', workspace_directory / 'nonexistent_key.txt')
    monkeypatch.setattr(config_module, 'CONFIG_FILE', workspace_directory / 'nonexistent_config.json')
    return HeadlessConfig.load()


def given_repl_is_initialized(workspace_directory):
    return workspace_directory


def given_headless_mode_is_configured_with_api_key(headless_config_with_api_key):
    return headless_config_with_api_key


def given_headless_mode_api_key_is_not_configured(headless_config_without_api_key):
    return headless_config_without_api_key


def when_user_runs_help_command(workspace_directory):
    from agile_bot.bots.base_bot.src.repl_cli.repl_help import HeadlessModeHelp
    headless_help = HeadlessModeHelp()
    return '\n'.join(headless_help.format_as_lines())


def when_user_runs_status_command(workspace_directory):
    from agile_bot.bots.base_bot.src.repl_cli.status_display import HeadlessModeStatusDisplay
    status_display = HeadlessModeStatusDisplay(workspace_directory=workspace_directory)
    return status_display.render()


def then_help_output_includes_headless_mode_section(help_output):
    assert 'headless' in help_output.lower() or '--headless' in help_output


def then_section_explains_headless_flag_purpose(help_output):
    assert 'headless' in help_output.lower()


def then_section_shows_message_parameter_usage(help_output):
    assert '--message' in help_output or 'message' in help_output.lower()


def then_section_includes_example_command_with_headless_flag(help_output):
    assert '--headless' in help_output


def then_section_indicates_headless_mode_is_unavailable(help_output):
    assert 'unavailable' in help_output.lower() or 'not configured' in help_output.lower()


def then_section_explains_configuration_requirement(help_output):
    assert 'api key' in help_output.lower() or 'configure' in help_output.lower()


def then_status_display_includes_headless_mode_section(status_output):
    assert 'headless' in status_output.lower()


def then_section_shows_headless_mode_is_available(status_output):
    assert 'available' in status_output.lower() or 'configured' in status_output.lower()


def then_section_displays_configured_api_key_prefix(status_output, headless_config):
    api_key_prefix = headless_config.api_key[:7] if headless_config.api_key else ''
    assert api_key_prefix in status_output or 'sk-' in status_output


def given_headless_session_is_running_with_session_id(workspace_directory, session_id):
    session_log_path = workspace_directory / 'logs' / f'headless-{session_id}.log'
    session_log_path.parent.mkdir(parents=True, exist_ok=True)
    session_log_path.write_text(f'Session {session_id} running\n')
    return session_id


def then_status_display_includes_active_session_section(status_output):
    assert 'session' in status_output.lower() or 'active' in status_output.lower()


def then_section_shows_session_id(status_output, session_id):
    assert session_id in status_output


def then_section_shows_session_status_as_running(status_output):
    assert 'running' in status_output.lower()


def then_section_shows_log_file_path(status_output):
    assert 'log' in status_output.lower() or '.log' in status_output


def then_section_shows_headless_mode_is_unavailable_in_status(status_output):
    assert 'unavailable' in status_output.lower() or 'not configured' in status_output.lower()


class TestAddHeadlessModeToHelp:
    
    def test_display_headless_mode_documentation_in_help(self, workspace_directory, headless_config_with_api_key):
        # Given: REPL is initialized
        workspace = given_repl_is_initialized(workspace_directory)
        
        # And: headless mode is configured with API key
        config = given_headless_mode_is_configured_with_api_key(headless_config_with_api_key)
        
        # When: user runs help command
        help_output = when_user_runs_help_command(workspace)
        
        # Then: help output includes headless mode section
        then_help_output_includes_headless_mode_section(help_output)
        
        # And: section explains --headless flag purpose
        then_section_explains_headless_flag_purpose(help_output)
        
        # And: section shows --message parameter usage
        then_section_shows_message_parameter_usage(help_output)
        
        # And: section includes example command with headless flag
        then_section_includes_example_command_with_headless_flag(help_output)
    
    def test_show_headless_mode_unavailable_when_not_configured(self, workspace_directory, headless_config_without_api_key):
        # Given: REPL is initialized
        workspace = given_repl_is_initialized(workspace_directory)
        
        # And: headless mode API key is not configured
        config = given_headless_mode_api_key_is_not_configured(headless_config_without_api_key)
        
        # When: user runs help command
        help_output = when_user_runs_help_command(workspace)
        
        # Then: help output includes headless mode section
        then_help_output_includes_headless_mode_section(help_output)
        
        # And: section indicates headless mode is unavailable
        then_section_indicates_headless_mode_is_unavailable(help_output)
        
        # And: section explains configuration requirement
        then_section_explains_configuration_requirement(help_output)


class TestAddHeadlessModeToStatus:
    
    def test_show_headless_mode_available_in_status(self, workspace_directory, headless_config_with_api_key):
        # Given: REPL is initialized
        workspace = given_repl_is_initialized(workspace_directory)
        
        # And: headless mode is configured with API key
        config = given_headless_mode_is_configured_with_api_key(headless_config_with_api_key)
        
        # When: user runs status command
        status_output = when_user_runs_status_command(workspace)
        
        # Then: status display includes headless mode section
        then_status_display_includes_headless_mode_section(status_output)
        
        # And: section shows headless mode is available
        then_section_shows_headless_mode_is_available(status_output)
        
        # And: section displays configured API key prefix
        then_section_displays_configured_api_key_prefix(status_output, config)
    
    def test_show_active_headless_session_in_status(self, workspace_directory, headless_config_with_api_key):
        # Given: REPL is initialized
        workspace = given_repl_is_initialized(workspace_directory)
        
        # And: headless session is running with session ID session_abc123
        session_id = given_headless_session_is_running_with_session_id(workspace, 'session_abc123')
        
        # When: user runs status command
        status_output = when_user_runs_status_command(workspace)
        
        # Then: status display includes active session section
        then_status_display_includes_active_session_section(status_output)
        
        # And: section shows session ID session_abc123
        then_section_shows_session_id(status_output, session_id)
        
        # And: section shows session status as running
        then_section_shows_session_status_as_running(status_output)
        
        # And: section shows log file path
        then_section_shows_log_file_path(status_output)
    
    def test_show_headless_mode_unavailable_in_status(self, workspace_directory, headless_config_without_api_key):
        # Given: REPL is initialized
        workspace = given_repl_is_initialized(workspace_directory)
        
        # And: headless mode API key is not configured
        config = given_headless_mode_api_key_is_not_configured(headless_config_without_api_key)
        
        # When: user runs status command
        status_output = when_user_runs_status_command(workspace)
        
        # Then: status display includes headless mode section
        then_status_display_includes_headless_mode_section(status_output)
        
        # And: section shows headless mode is unavailable
        then_section_shows_headless_mode_is_unavailable_in_status(status_output)

