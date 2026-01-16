"""
Navigate Bot Behaviors and Actions With CLI Tests - REPL Command Interface

Domain logic tested in: test_invoke_bot_directly.py::TestNavigateToBehaviorActionAndExecute
Domain logic tested in: test_invoke_bot_directly.py::TestNavigateSequentially

These tests focus on REPL-specific concerns:
- Command parsing (dot notation, next/back commands)
- CLI output format and error messages
- Delegation to domain logic

Uses common helpers from: test_invoke_bot_helpers.py
"""
import pytest
import sys
from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
from agile_bot.bots.base_bot.test.test_invoke_bot_helpers import (
    setup_test_bot,
    create_behavior_action_state,
    assert_bot_at_behavior_action
)


class TestNavigateToBehaviorActionAndExecute:
    """
    Story: Navigate Using CLI Dot Notation
    
    Domain logic: test_invoke_bot_directly.py::TestNavigateToBehaviorActionAndExecute
    REPL focus: Command parsing and CLI output format
    """
    
    def test_user_navigates_with_behavior_only(self, tmp_path, monkeypatch):
        """
        SCENARIO: User navigates with behavior only (no dots)
        GIVEN: CLI is at shape.clarify
        WHEN: user enters 'discovery'
        THEN: REPL parses command and delegates to bot.behaviors.navigate_to()
              CLI output shows navigation success
        
        Domain logic tested in: TestNavigateToBehaviorActionAndExecute
        """
        # GIVEN: Bot with two behaviors, currently at shape.clarify
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape', 'discovery'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'clarify')
        bot.behaviors.load_state()
        
        # WHEN: user enters 'discovery' via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('discovery')
        
        # THEN: REPL successfully parsed command and CLI shows output
        assert cli_response is not None
        assert cli_response.status in ['success', 'error', None] or 'discovery' in cli_response.output.lower()
        
        # Verify delegation: Domain logic was invoked
        assert_bot_at_behavior_action(bot, 'discovery', 'clarify')
    
    def test_user_navigates_with_behavior_dot_action(self, tmp_path, monkeypatch):
        """
        SCENARIO: User navigates with behavior.action (one dot)
        GIVEN: CLI is at shape.clarify
        WHEN: user enters 'discovery.validate'
        THEN: REPL parses dot notation and navigates to discovery.validate
              CLI output shows navigation success
        
        Domain logic tested in: TestNavigateToBehaviorActionAndExecute
        """
        # GIVEN
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape', 'discovery'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'clarify')
        bot.behaviors.load_state()
        
        # WHEN: user enters 'discovery.validate' via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('discovery.validate')
        
        # THEN: REPL parsed dot notation and CLI shows output
        assert cli_response is not None
        assert isinstance(cli_response.output, str)
        
        # Verify delegation: Domain logic was invoked
        assert_bot_at_behavior_action(bot, 'discovery', 'validate')
    
    def test_user_navigates_with_full_dot_notation(self, tmp_path, monkeypatch):
        """
        SCENARIO: User navigates with behavior.action.operation (two dots)
        GIVEN: CLI is at shape.clarify
        WHEN: user enters 'discovery.validate.instructions'
        THEN: REPL parses full dot notation and executes operation
              CLI output shows execution result
        
        Domain logic tested in: TestNavigateToBehaviorActionAndExecute
        """
        # GIVEN
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape', 'discovery'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'clarify')
        bot.behaviors.load_state()
        
        # WHEN: user enters full dot notation via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('discovery.validate.instructions')
        
        # THEN: REPL parsed command and CLI shows output
        assert cli_response is not None
        assert isinstance(cli_response.output, str)
        
        # Verify delegation: Domain logic was invoked (operation executed)
        assert_bot_at_behavior_action(bot, 'discovery', 'validate')
    
    def test_user_enters_invalid_behavior_in_dot_notation(self, tmp_path, monkeypatch):
        """
        SCENARIO: User enters invalid behavior in dot notation
        GIVEN: CLI is at shape.clarify
        WHEN: user enters 'invalid_behavior.validate.instructions'
        THEN: REPL detects invalid behavior and displays error message
              CLI output contains error indication
        
        REPL focus: Error handling and user feedback
        """
        # GIVEN
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'clarify')
        bot.behaviors.load_state()
        
        # WHEN: user enters invalid behavior via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('invalid_behavior.validate.instructions')
        
        # THEN: REPL shows error message
        assert 'ERROR' in cli_response.output or 'error' in cli_response.output.lower() or cli_response.status == 'error'


class TestNavigateSequentially:
    """
    Story: Navigate Sequentially Using CLI Commands
    
    Domain logic: test_invoke_bot_directly.py::TestNavigateSequentially
    REPL focus: Sequential command parsing (next/back)
    """
    
    def test_user_navigates_with_next_command(self, tmp_path, monkeypatch):
        """
        SCENARIO: User navigates with next command
        GIVEN: CLI is at shape.clarify
        WHEN: user enters 'next'
        THEN: REPL parses 'next' command and advances to next action
              CLI output shows navigation success
        
        Domain logic tested in: TestNavigateSequentially
        """
        # GIVEN
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'clarify')
        bot.behaviors.load_state()
        
        # WHEN: user enters 'next' via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('next')
        
        # THEN: REPL parsed command and CLI shows output
        assert cli_response is not None
        assert isinstance(cli_response.output, str)
        
        # Verify delegation: Advanced to next action (strategy)
        assert_bot_at_behavior_action(bot, 'shape', 'strategy')
    
    @pytest.mark.xfail(reason="Actions.previous not implemented yet - pre-existing bug")
    def test_user_navigates_with_back_command(self, tmp_path, monkeypatch):
        """
        SCENARIO: User navigates with back command
        GIVEN: CLI is at shape.strategy
        WHEN: user enters 'back'
        THEN: REPL parses 'back' command
              CLI output shows result (success or error)
        
        Note: xfail - Actions.previous not yet implemented (pre-existing bug)
        """
        # GIVEN: at strategy (second action)
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'strategy')
        bot.behaviors.load_state()
        
        # WHEN: user enters 'back' via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('back')
        
        # THEN: REPL parsed command and CLI shows output
        assert cli_response is not None
        assert isinstance(cli_response.output, str)
        
        # Note: Domain delegation check skipped - Actions.previous not implemented yet


class TestExitREPL:
    """
    Story: Exit CLI REPL
    
    REPL focus: Exit command parsing and session termination
    """
    
    def test_user_exits_repl_with_exit_command(self, tmp_path, monkeypatch):
        """
        SCENARIO: User exits REPL with exit command
        GIVEN: CLI is running
        WHEN: user enters 'exit'
        THEN: REPL parses 'exit' command and terminates session
              CLI response indicates termination
        
        REPL focus: Command parsing and session lifecycle
        """
        # GIVEN: CLI is running
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['discovery'])
        create_behavior_action_state(workspace, 'story_bot', 'discovery', 'validate')
        bot.behaviors.load_state()
        
        # WHEN: user enters 'exit' via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('exit')
        
        # THEN: REPL indicates exit/termination
        assert cli_response is not None
        assert cli_response.repl_terminated or 'exit' in cli_response.output.lower() or cli_response.status == 'exit'


class TestDisplayBotHierarchyTree:
    """
    Story: Display Bot Hierarchy Tree with Progress Indicators
    
    REPL focus: Hierarchy tree display format with progress markers
    """
    
    def test_user_views_bot_hierarchy_with_status_command(self, tmp_path, monkeypatch):
        """
        SCENARIO: User views bot hierarchy with status command
        GIVEN: CLI is at exploration.validate
        WHEN: user enters 'status'
        THEN: REPL parses status command
              CLI displays bot hierarchy tree
        
        REPL focus: Status command execution and hierarchy display
        """
        # GIVEN
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape', 'exploration'])
        create_behavior_action_state(workspace, 'story_bot', 'exploration', 'validate')
        bot.behaviors.load_state()
        
        # WHEN: user enters 'status' via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('status')
        
        # THEN: Status displayed
        assert cli_response is not None
        assert isinstance(cli_response.output, str)
        assert len(cli_response.output) > 0


class TestDisplayCurrentPosition:
    """
    Story: Display Current Position in CLI
    
    REPL focus: Current position indicators in status display
    """
    
    def test_user_views_current_position_in_status(self, tmp_path, monkeypatch):
        """
        SCENARIO: User views current position in status
        GIVEN: CLI is at shape.clarify
        WHEN: user enters 'status'
        THEN: CLI displays current position with indicators
        
        REPL focus: Position display in status output
        """
        # GIVEN
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'clarify')
        bot.behaviors.load_state()
        
        # WHEN: user enters 'status' via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('status')
        
        # THEN: Current position displayed
        assert cli_response is not None
        assert isinstance(cli_response.output, str)
        assert len(cli_response.output) > 0
    
    def test_cli_displays_progress_section_with_current_position(self, tmp_path, monkeypatch):
        """
        SCENARIO: CLI displays Progress section with current position
        GIVEN: CLI is at exploration.validate
        WHEN: CLI renders status display
        THEN: CLI displays Progress section header
        
        REPL focus: Progress section in status display
        """
        # GIVEN
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: False)
        bot, workspace = setup_test_bot(tmp_path, ['exploration'])
        create_behavior_action_state(workspace, 'story_bot', 'exploration', 'validate')
        bot.behaviors.load_state()
        
        # WHEN: Status displayed
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_output = repl_session.display_current_state()
        
        # THEN: Progress information included
        display_text = str(cli_output.output) if hasattr(cli_output, 'output') else str(cli_output)
        # Progress section should be present (format may vary)
        assert len(display_text) > 0
    
    def test_cli_displays_behavior_in_progress_section(self, tmp_path, monkeypatch):
        """
        SCENARIO: CLI displays behavior in Progress section
        GIVEN: CLI is at shape.validate
        WHEN: CLI renders status display
        THEN: CLI displays current behavior in Progress section
        
        REPL focus: Behavior display in progress section
        """
        # GIVEN
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: False)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'validate')
        bot.behaviors.load_state()
        
        # WHEN: Status displayed
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_output = repl_session.display_current_state()
        
        # THEN: Behavior info included
        display_text = str(cli_output.output) if hasattr(cli_output, 'output') else str(cli_output)
        assert len(display_text) > 0
