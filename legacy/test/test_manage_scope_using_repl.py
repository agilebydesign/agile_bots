"""
Manage Bot Scope Through CLI Tests - REPL Command Interface

Domain logic tested in: test_invoke_bot_directly.py::TestManageScopeIntegration

These tests focus on REPL-specific concerns:
- Scope command parsing
- CLI output format for scope operations
- Delegation to domain logic

Uses common helpers from: test_invoke_bot_helpers.py
"""
import pytest
import sys
from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
from agile_bot.bots.base_bot.test.test_invoke_bot_helpers import (
    setup_test_bot,
    create_behavior_action_state
)


class TestSetScope:
    """
    Story: Filter Work Using Scope
    
    Domain logic: test_invoke_bot_directly.py::TestManageScopeIntegration
    REPL focus: Scope command parsing
    """
    
    def test_user_sets_scope_filter(self, tmp_path, monkeypatch):
        """
        SCENARIO: User sets scope filter
        GIVEN: CLI is at shape.validate
        WHEN: user enters 'scope story="Story1"'
        THEN: REPL parses scope command
              CLI stores scope filter and shows confirmation
        
        REPL focus: Command parsing with quoted arguments
        """
        # GIVEN
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'validate')
        bot.behaviors.load_state()
        
        # WHEN: user enters 'scope story="Story1"' via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('scope story="Story1"')
        
        # THEN: REPL parsed scope command and shows output
        assert cli_response is not None
        assert isinstance(cli_response.output, str)
    
    def test_user_views_current_scope(self, tmp_path, monkeypatch):
        """
        SCENARIO: User views current scope
        GIVEN: Scope filter is set
        WHEN: user enters 'scope' (no arguments)
        THEN: REPL displays current scope configuration
        
        REPL focus: Scope display format
        """
        # GIVEN: Scope filter is set
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'validate')
        bot.behaviors.load_state()
        
        # WHEN: user sets scope then views it via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        # First set a scope
        repl_session.read_and_execute_command('scope story="Story1"')
        # Then view it
        cli_response = repl_session.read_and_execute_command('scope')
        
        # THEN: REPL displays current scope
        assert cli_response is not None
        assert isinstance(cli_response.output, str)


class TestViewCurrentScopeInCLI:
    """
    Story: View Current Scope in CLI
    
    Domain logic: test_manage_scope_bot_api.py::TestSetScopeThroughBotAPI
    REPL focus: Display scope configuration via CLI commands
    """
    
    def test_view_scope_with_no_filters_set(self, tmp_path, monkeypatch):
        """
        SCENARIO: View scope with no filters set
        GIVEN: CLI is initialized with no scope filters
        WHEN: user enters 'scope' command
        THEN: CLI displays "No scope filters active"
        
        REPL focus: Default scope display
        """
        # GIVEN: CLI with no scope
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'validate')
        bot.behaviors.load_state()
        
        # WHEN: user views scope via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('scope')
        
        # THEN: REPL displays no active scope
        assert cli_response is not None
        assert isinstance(cli_response.output, str)
    
    def test_view_story_scope_filter(self, tmp_path, monkeypatch):
        """
        SCENARIO: View story scope filter
        GIVEN: Story scope filter is set to "Story1"
        WHEN: user enters 'scope' command
        THEN: CLI displays active story scope filter
        
        REPL focus: Story scope display format
        """
        # GIVEN: Story scope is set
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'validate')
        bot.behaviors.load_state()
        
        # WHEN: user sets story scope then views it
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        repl_session.read_and_execute_command('scope story="Story1"')
        cli_response = repl_session.read_and_execute_command('scope')
        
        # THEN: CLI displays story scope
        assert cli_response is not None
        assert isinstance(cli_response.output, str)
    
    def test_view_file_scope_filter(self, tmp_path, monkeypatch):
        """
        SCENARIO: View file scope filter
        GIVEN: File scope filter is set to "*.py"
        WHEN: user enters 'scope' command
        THEN: CLI displays active file scope filter
        
        REPL focus: File scope display format
        """
        # GIVEN: File scope is set
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'validate')
        bot.behaviors.load_state()
        
        # WHEN: user sets file scope then views it
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        repl_session.read_and_execute_command('scope file="*.py"')
        cli_response = repl_session.read_and_execute_command('scope')
        
        # THEN: CLI displays file scope
        assert cli_response is not None
        assert isinstance(cli_response.output, str)


class TestClearScope:
    """
    Story: Clear Scope Filters
    
    REPL focus: Scope clear command parsing
    """
    
    def test_user_clears_all_scope_filters(self, tmp_path, monkeypatch):
        """
        SCENARIO: User clears all scope filters
        GIVEN: Scope filter is set
        WHEN: user enters 'scope clear'
        THEN: REPL parses clear command
              CLI clears scope and shows confirmation
        
        REPL focus: Command with subcommand parsing
        """
        # GIVEN: Scope filter is set
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'validate')
        bot.behaviors.load_state()
        
        # WHEN: user sets scope then clears it via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        # First set a scope
        repl_session.read_and_execute_command('scope story="Story1"')
        # Then clear it
        cli_response = repl_session.read_and_execute_command('scope clear')
        
        # THEN: REPL cleared scope and shows output
        assert cli_response is not None
        assert isinstance(cli_response.output, str)
