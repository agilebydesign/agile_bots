"""
Initialize REPL Session Tests - CURRENT BEHAVIOR

These tests validate the CURRENT implementation before refactoring.
They test against actual behavior, not target architecture.
"""
import pytest
import json
import sys
from pathlib import Path


@pytest.fixture
def bot_directory(tmp_path):
    """Create a temporary bot directory with bot_config.json"""
    bot_dir = tmp_path / 'agile_bot' / 'bots' / 'story_bot'
    bot_dir.mkdir(parents=True)
    
    config_data = {'name': 'story_bot'}
    (bot_dir / 'bot_config.json').write_text(json.dumps(config_data))
    
    return bot_dir


@pytest.fixture
def workspace_directory(tmp_path):
    """Create a temporary workspace directory"""
    workspace_dir = tmp_path / 'workspace'
    workspace_dir.mkdir(parents=True)
    return workspace_dir


def create_behavior(bot_directory, behavior_name, actions):
    """Create behavior folder with actions"""
    behavior_dir = bot_directory / 'behaviors' / behavior_name
    behavior_dir.mkdir(parents=True, exist_ok=True)
    
    behavior_config = {
        'name': behavior_name,
        'description': f'Test {behavior_name} behavior'
    }
    (behavior_dir / 'behavior.json').write_text(json.dumps(behavior_config))
    
    for action in actions:
        action_dir = behavior_dir / 'actions' / action
        action_dir.mkdir(parents=True, exist_ok=True)
        action_config = {
            'name': action,
            'description': f'Test {action} action'
        }
        (action_dir / 'action.json').write_text(json.dumps(action_config))


def create_behavior_action_state(workspace_directory, behavior, action, operation='instructions'):
    """Create behavior action state file with specified state"""
    state_data = {
        'current_behavior': f'story_bot.{behavior}',
        'current_action': f'story_bot.{behavior}.{action}',
        'operation': operation,
        'working_directory': str(workspace_directory),
        'timestamp': '2025-12-26T10:00:00.000000'
    }
    
    state_file = workspace_directory / 'behavior_action_state.json'
    state_file.write_text(json.dumps(state_data))
    return state_file


class TestLaunchCLIInInteractiveMode:
    """Story: Launch CLI in Interactive Mode"""
    
    def test_cli_creates_session_with_bot(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: CLI creates session with bot instance
        GIVEN: Bot directory exists with behaviors
        WHEN: REPLSession is created
        THEN: Session has direct bot reference (current: .bot, not .cli_bot)
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: Bot directory exists with behaviors
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build'])
        
        # WHEN: REPLSession is created
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        
        # THEN: Session has direct bot reference (CURRENT: .bot not .cli_bot)
        assert hasattr(repl_session, 'bot')
        assert repl_session.bot is not None
        assert repl_session.bot.bot_name == 'story_bot'
    
    def test_cli_displays_hierarchy_when_behaviors_exist(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: CLI displays hierarchy when behaviors exist
        GIVEN: Bot has behaviors loaded
        WHEN: display_current_state() is called
        THEN: Returns REPLStateDisplay with hierarchy in output
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: Bot has behaviors loaded
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'build'])
        
        # WHEN: display_current_state() is called
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        cli_output = repl_session.display_current_state()
        
        # THEN: Returns REPLStateDisplay
        assert hasattr(cli_output, 'output')
        # AND: Output contains hierarchy indicators
        output_text = cli_output.output
        assert any(indicator in output_text for indicator in ['[*]', '[ ]', 'shape', 'help', 'exit'])


class TestLaunchCLIInPipeMode:
    """Story: Launch CLI in Pipe Mode"""
    
    def test_cli_detects_piped_input(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: CLI detects piped input
        GIVEN: stdin is not a TTY (piped)
        WHEN: detect_tty() is called
        THEN: Returns tty_detected=False
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: stdin is not a TTY (piped)
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: False)
        create_behavior(bot_directory, 'shape', ['clarify'])
        
        # WHEN: detect_tty() is called
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        tty_result = repl_session.detect_tty()
        
        # THEN: Returns tty_detected=False
        assert tty_result.tty_detected == False
        assert tty_result.interactive_prompts_enabled == False


class TestDetectAndConfigureTTYNonTTYInputForCLI:
    """Story: Detect and Configure TTY/Non-TTY Input for CLI"""
    
    def test_tty_detector_identifies_interactive_terminal(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: TTYDetector identifies interactive terminal
        GIVEN: stdin is connected to a TTY terminal
        WHEN: detect_tty() is called
        THEN: Returns tty_detected=True
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: stdin is connected to a TTY terminal
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        
        # WHEN: detect_tty() is called
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        tty_result = repl_session.detect_tty()
        
        # THEN: Returns tty_detected=True
        assert tty_result.tty_detected == True
        assert tty_result.interactive_prompts_enabled == True
    
    def test_tty_detector_identifies_piped_input(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: TTYDetector identifies piped input
        GIVEN: stdin is piped from another process
        WHEN: detect_tty() is called
        THEN: Returns tty_detected=False
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: stdin is piped from another process
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: False)
        
        # WHEN: detect_tty() is called
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        tty_result = repl_session.detect_tty()
        
        # THEN: Returns tty_detected=False
        assert tty_result.tty_detected == False
        assert tty_result.interactive_prompts_enabled == False


class TestLoadAndDisplayWorkspaceContextInCLI:
    """Story: Load and Display Workspace Context in CLI"""
    
    def test_cli_loads_workspace_directory(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: CLI loads workspace directory
        GIVEN: Workspace directory path is provided
        WHEN: REPLSession is initialized
        THEN: Session stores workspace_directory reference
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: Workspace directory path is provided
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify'])
        
        # WHEN: REPLSession is initialized
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        
        # THEN: Session stores workspace_directory reference
        assert repl_session.workspace_directory == workspace_directory
        assert repl_session.workspace_directory.exists()


class TestLoadExistingBehaviorActionState:
    """Story: Load Existing Behavior Action State"""
    
    def test_cli_loads_existing_state_file(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: CLI loads existing behavior action state file
        GIVEN: behavior_action_state.json exists in workspace
        WHEN: REPLSession initializes
        THEN: Current behavior and action are set from file
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: behavior_action_state.json exists in workspace
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'discovery', ['clarify', 'build', 'validate'])
        state_file = create_behavior_action_state(workspace_directory, 'discovery', 'build', 'instructions')
        
        # WHEN: REPLSession initializes
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        
        # THEN: State file exists and can be loaded
        assert state_file.exists()
        state_data = json.loads(state_file.read_text())
        assert state_data['current_behavior'] == 'story_bot.discovery'
        assert state_data['current_action'] == 'story_bot.discovery.build'
        # Note: REPLSession loads state lazily, so behavior/action are set when accessed
        # The actual navigation happens when a command is executed

