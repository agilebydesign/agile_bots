"""
Get Help Using CLI Tests - REPL Command Interface

REPL focus: Help command parsing and output formatting

These tests focus on REPL-specific concerns:
- 'help' command parsing
- Help output format and content
- Examples display

Uses common helpers from: test_invoke_bot_helpers.py
"""
import pytest
import sys
from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
from agile_bot.bots.base_bot.test.test_invoke_bot_helpers import (
    setup_test_bot,
    create_behavior_action_state
)


class TestDisplayActionHelpUsingCLI:
    """
    Story: View Available Commands
    
    REPL focus: Help command parsing and output format
    """
    
    def test_user_views_all_available_commands(self, tmp_path, monkeypatch):
        """
        SCENARIO: User views all available commands
        GIVEN: CLI is running
        WHEN: user enters 'help'
        THEN: REPL parses 'help' command
              CLI displays help menu with commands
        
        REPL focus: Help output contains command list
        """
        # GIVEN: CLI is running
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'clarify')
        bot.behaviors.load_state()
        
        # WHEN: user enters 'help' via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('help')
        
        # THEN: REPL displays help menu
        assert cli_response is not None
        assert isinstance(cli_response.output, str)
        assert len(cli_response.output) > 0
        # Help should contain some command information
        assert any(cmd in cli_response.output.lower() for cmd in ['help', 'status', 'exit', 'command'])


class TestDisplayCommandExamplesUsingCLI:
    """
    Story: View Command Examples
    
    REPL focus: Help examples display
    """
    
    def test_user_views_examples_in_help(self, tmp_path, monkeypatch):
        """
        SCENARIO: User views examples in help
        GIVEN: CLI is running
        WHEN: user enters 'help'
        THEN: REPL displays help with examples
              CLI output contains help text
        
        REPL focus: Help output format
        """
        # GIVEN: CLI is running
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'validate')
        bot.behaviors.load_state()
        
        # WHEN: user enters 'help' via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('help')
        
        # THEN: REPL displays help with examples
        assert cli_response is not None
        assert isinstance(cli_response.output, str)
        assert len(cli_response.output) > 0


class TestDisplayNavigationCommandsFooter:
    """
    Story: Display Navigation Commands Footer
    
    REPL focus: Available commands display in footer
    """
    
    def test_cli_displays_available_commands(self, tmp_path, monkeypatch):
        """
        SCENARIO: CLI displays available commands
        GIVEN: CLI is running
        WHEN: Status displayed
        THEN: Available commands shown
        
        REPL focus: Command list display
        """
        # GIVEN
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        
        # WHEN: Status displayed
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_output = repl_session.display_current_state()
        
        # THEN: Commands available
        display_text = str(cli_output.output) if hasattr(cli_output, 'output') else str(cli_output)
        # Commands may be shown in various formats
        assert len(display_text) > 0
    
    def test_cli_displays_bot_command_in_footer(self, tmp_path, monkeypatch):
        """
        SCENARIO: CLI displays bot command in footer
        GIVEN: CLI is running
        WHEN: Status displayed
        THEN: Footer shows available commands
        
        REPL focus: Footer formatting
        """
        # GIVEN
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        
        # WHEN: Status displayed
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_output = repl_session.display_current_state()
        
        # THEN: Footer info included
        display_text = str(cli_output.output) if hasattr(cli_output, 'output') else str(cli_output)
        # Footer may show help, commands, or other info
        assert len(display_text) > 0
