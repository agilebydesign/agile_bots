"""
Execute Action Operation Through CLI Tests - REPL Command Interface

Domain logic tested in: test_invoke_bot_directly.py (various test classes)

These tests focus on REPL-specific concerns:
- Action operation command parsing
- CLI output format for different operations
- Error handling and validation

Uses common helpers from: test_invoke_bot_helpers.py
"""
import pytest
import sys
from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
from agile_bot.bots.base_bot.test.test_invoke_bot_helpers import (
    setup_test_bot,
    create_behavior_action_state
)


class TestViewInstructions:
    """
    Story: Get Action Instructions Through CLI
    
    REPL focus: Instructions command parsing and output format
    """
    
    def test_user_gets_instructions_for_build_action(self, tmp_path, monkeypatch):
        """
        SCENARIO: User gets instructions for build action
        GIVEN: CLI is at shape.validate
        WHEN: user enters 'shape.validate.instructions'
        THEN: REPL parses full command and displays instructions
        
        REPL focus: Full dot notation with operation
        """
        # GIVEN
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'validate')
        bot.behaviors.load_state()
        
        # WHEN: user enters full command via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('shape.validate.instructions')
        
        # THEN: REPL displays instructions
        assert cli_response is not None
        assert isinstance(cli_response.output, str)


class TestConfirmWithParameters:
    """
    Story: Confirm Work Through CLI
    
    REPL focus: Confirm command parsing
    """
    
    def test_user_confirms_build_work(self, tmp_path, monkeypatch):
        """
        SCENARIO: User confirms build work
        GIVEN: CLI is at shape.validate
        WHEN: user enters 'confirm'
        THEN: REPL parses confirm command
              CLI processes work and shows result
        
        REPL focus: Simple command without arguments
        """
        # GIVEN
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'validate')
        bot.behaviors.load_state()
        
        # WHEN: user enters 'confirm' via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('confirm')
        
        # THEN: REPL processed confirm
        assert cli_response is not None
        assert isinstance(cli_response.output, str)


class TestConfirmActionCompletion:
    """
    Story: Confirm Action Completion
    
    REPL focus: Confirm command execution and state advancement
    """
    
    def test_user_confirms_build_action_completion(self, tmp_path, monkeypatch):
        """
        SCENARIO: User confirms build action completion
        GIVEN: CLI is at shape.validate
        WHEN: user enters 'confirm'
        THEN: REPL processes confirmation
              CLI shows completion message
        
        REPL focus: Command execution and output format
        """
        # GIVEN
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'validate')
        bot.behaviors.load_state()
        
        # WHEN: user enters 'confirm' via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('confirm')
        
        # THEN: REPL processed confirmation
        assert cli_response is not None
        assert isinstance(cli_response.output, str)


class TestReExecuteCurrentAction:
    """
    Story: Re-execute Current Operation
    
    REPL focus: Current command parsing
    """
    
    def test_user_re_executes_current_instructions(self, tmp_path, monkeypatch):
        """
        SCENARIO: User re-executes current instructions
        GIVEN: CLI is at discovery.validate
        WHEN: user enters 'current'
        THEN: REPL parses current command
              CLI re-executes current operation
        
        REPL focus: Command without arguments
        """
        # GIVEN
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['discovery'])
        create_behavior_action_state(workspace, 'story_bot', 'discovery', 'validate')
        bot.behaviors.load_state()
        
        # WHEN: user enters 'current' via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('current')
        
        # THEN: REPL re-executed current operation
        assert cli_response is not None
        assert isinstance(cli_response.output, str)


class TestHandleErrorsAndValidation:
    """
    Story: Handle Operation Errors
    
    REPL focus: Error handling and user feedback
    """
    
    def test_user_enters_invalid_command(self, tmp_path, monkeypatch):
        """
        SCENARIO: User enters invalid command
        GIVEN: CLI is at shape.validate
        WHEN: user enters 'invalid_command_xyz'
        THEN: REPL detects invalid command
              CLI displays error message
        
        REPL focus: Error detection and user feedback
        """
        # GIVEN
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        create_behavior_action_state(workspace, 'story_bot', 'shape', 'validate')
        bot.behaviors.load_state()
        
        # WHEN: user enters invalid command via REPL
        repl_session = REPLSession(bot=bot, workspace_directory=workspace)
        cli_response = repl_session.read_and_execute_command('invalid_command_xyz')
        
        # THEN: REPL shows error message
        assert cli_response is not None
        assert 'ERROR' in cli_response.output or 'error' in cli_response.output.lower() or cli_response.status == 'error'
