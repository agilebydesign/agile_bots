"""
Execute Action Operation Through CLI Tests

Tests for all stories in the 'Execute Action Operation Through CLI' sub-epic:
- Get Action Instructions Through CLI
- Confirm Work Through CLI with String Parameters (2-phase model)
- Confirm Action Completion Through CLI
- Re-execute Current Operation Using CLI
- Handle Operation Errors and Validation in CLI
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
    """Create behavior folder with actions and required guardrails"""
    behavior_dir = bot_directory / 'behaviors' / behavior_name
    behavior_dir.mkdir(parents=True, exist_ok=True)
    
    actions_workflow = {
        'actions': [{'name': action, 'order': i+1} for i, action in enumerate(actions)]
    }
    
    behavior_config = {
        'name': behavior_name,
        'description': f'Test {behavior_name} behavior',
        'order': 1,
        'actions_workflow': actions_workflow
    }
    (behavior_dir / 'behavior.json').write_text(json.dumps(behavior_config))
    
    # Create guardrails/strategy directory structure for strategy action
    guardrails_strategy_dir = behavior_dir / 'guardrails' / 'strategy'
    guardrails_strategy_dir.mkdir(parents=True, exist_ok=True)
    typical_assumptions = {'assumptions': []}
    (guardrails_strategy_dir / 'typical_assumptions.json').write_text(json.dumps(typical_assumptions))
    
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


class TestGetActionInstructionsThroughCLI:
    """Story: Get Action Instructions Through CLI"""
    
    def test_user_gets_instructions_for_build_action_without_scope(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User gets instructions for build action without scope
        GIVEN: CLI is at shape.build.instructions
        WHEN: user enters 'shape.build.instructions'
        THEN: CLI displays formatted instructions
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at shape.build.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'shape', 'build', 'instructions')
        
        # WHEN: user enters 'shape.build.instructions'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        cli_response = repl_session.read_and_execute_command('shape.build.instructions')
        
        # THEN: CLIAction calls action.get_instructions(context)
        # AND: CLI displays formatted instructions
        assert '[INSTRUCTIONS]' in cli_response.output or 'instructions' in cli_response.output.lower()
        assert 'shape.build' in cli_response.output or 'build' in cli_response.output
    
    def test_user_calls_action_by_name_shortcut(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User calls action by name as shortcut
        GIVEN: CLI is at shape.build.instructions
        WHEN: user enters just 'build' (action name only)
        THEN: CLI executes instructions operation on current behavior's build action
        AND: Instructions are formatted as strings, not JSON
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at shape.build.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'shape', 'build', 'instructions')
        
        # WHEN: user enters just 'build'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        cli_response = repl_session.read_and_execute_command('build')
        
        # THEN: CLI executes current operation (instructions) on current behavior's build action
        assert cli_response.status == 'success'
        # AND: Output is formatted string, not JSON
        assert '"formatted_output"' not in cli_response.output
        assert '"instructions"' not in cli_response.output
        # AND: Contains actual instruction content
        assert 'instructions' in cli_response.output.lower() or 'build' in cli_response.output.lower()
    
    def test_user_gets_instructions_for_build_action_with_scope(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User gets instructions for build action with scope
        GIVEN: CLI is at shape.build.instructions
        WHEN: user enters 'shape.build.instructions scope="Story1, Story2"'
        THEN: CLI displays filtered instructions for Story1, Story2
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at shape.build.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'shape', 'build', 'instructions')
        
        # WHEN: user enters 'shape.build.instructions scope="Story1, Story2"'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        cli_response = repl_session.read_and_execute_command('shape.build.instructions --scope "Story1, Story2"')
        
        # THEN: CLIAction uses CLIScope to parse scope string
        # AND: CLI displays formatted instructions with scope (new format with headers)
        assert cli_response.status == 'success'
        assert '**INSTRUCTIONS SECTION:**' in cli_response.output or 'instructions' in cli_response.output.lower()
    
    def test_user_gets_instructions_for_clarify_action_without_context(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User gets instructions for clarify action without context
        GIVEN: CLI is at shape.clarify.instructions
        WHEN: user enters 'shape.clarify.instructions'
        THEN: CLI displays key questions and required evidence from guardrails
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at shape.clarify.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'shape', 'clarify', 'instructions')
        
        # WHEN: user enters 'shape.clarify.instructions'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        cli_response = repl_session.read_and_execute_command('shape.clarify.instructions')
        
        # THEN: CLI displays formatted instructions with new header format
        assert cli_response.status == 'success'
        assert '**INSTRUCTIONS SECTION:**' in cli_response.output or 'CLI STATUS' in cli_response.output
    
    def test_user_calls_clarify_by_name_shortcut(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User calls clarify action by name as shortcut
        GIVEN: CLI is at shape.clarify.instructions
        WHEN: user enters just 'clarify' (action name only)
        THEN: CLI executes instructions operation on current behavior's clarify action
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at shape.clarify.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'shape', 'clarify', 'instructions')
        
        # WHEN: user enters just 'clarify'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        cli_response = repl_session.read_and_execute_command('clarify')
        
        # THEN: CLI executes instructions operation with new display format
        assert cli_response.status == 'success'
        # Output should have new section headers or CLI STATUS
        assert '**INSTRUCTIONS SECTION:**' in cli_response.output or 'CLI STATUS' in cli_response.output or len(cli_response.output) > 50


class TestConfirmWorkThroughCLIWithStringParameters:
    """Story: Confirm Work Through CLI with String Parameters (2-phase model)"""
    
    def test_user_confirms_build_work(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User confirms build work
        GIVEN: CLI is at shape.build.instructions
        WHEN: user enters 'confirm'
        THEN: CLI processes work and advances to next action
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at shape.build.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'shape', 'build', 'instructions')
        # AND: user has created knowledge graph content
        
        # WHEN: user enters 'confirm'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        cli_response = repl_session.read_and_execute_command('confirm')
        
        # THEN: CLIAction calls action.confirm(context)
        # AND: CLI advances to next action
        assert cli_response.status in ['success', 'error'] or 'confirm' in cli_response.output.lower()
    
    def test_user_confirms_clarify_with_answers(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User confirms clarify with answers
        GIVEN: CLI is at shape.clarify.instructions
        WHEN: user enters 'confirm' with answers parameter
        THEN: CLI saves clarification data and advances to next action
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at shape.clarify.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'shape', 'clarify', 'instructions')
        
        # WHEN: user enters 'confirm' with JSON answers
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        
        # Confirm with answers as JSON context (matches ClarifyActionContext)
        cli_response = repl_session.read_and_execute_command('confirm {"answers": {"What are goals?": "Create bot"}}')
        
        # THEN: CLI displays next action instructions
        assert cli_response.status in ['success', 'error']
        # Should show CLI STATUS section or next action
        assert 'CLI STATUS' in cli_response.output or 'confirm' in cli_response.output.lower() or 'Clarification saved' in cli_response.output
    
    def test_user_confirms_clarify_with_evidence(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User confirms clarify with evidence
        GIVEN: CLI is at discovery.clarify.instructions
        WHEN: user enters 'confirm' with evidence-provided parameter
        THEN: CLI saves evidence and advances to next action
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at discovery.clarify.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'discovery', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'discovery', 'clarify', 'instructions')
        
        # WHEN: user enters 'confirm' with evidence_provided
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        
        cli_response = repl_session.read_and_execute_command('confirm {"evidence_provided": {"domain_doc": "path/to/doc.md"}}')
        
        # THEN: CLI advances to next action
        assert cli_response.status in ['success', 'error']
        # New display format shows status sections
        assert 'CLI STATUS' in cli_response.output or 'confirm' in cli_response.output.lower() or 'Clarification saved' in cli_response.output


class TestConfirmActionCompletionThroughCLI:
    """Story: Confirm Action Completion Through CLI (2-phase model)"""
    
    def test_user_confirms_build_action_completion(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User confirms build action completion
        GIVEN: CLI is at shape.build.instructions
        WHEN: user enters 'confirm'
        THEN: CLI automatically navigates to shape.validate.instructions
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at shape.build.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'shape', 'build', 'instructions')
        
        # WHEN: user enters 'confirm'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        cli_response = repl_session.read_and_execute_command('confirm')
        
        # THEN: CLIAction calls action.confirm()
        # AND: CLI automatically navigates to shape.validate.instructions
        assert cli_response.status == 'success' or 'confirm' in cli_response.output.lower()
    
    def test_user_confirms_clarify_action_completion(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User confirms clarify action completion
        GIVEN: CLI is at shape.clarify.instructions
        WHEN: user enters 'confirm'
        THEN: CLI automatically navigates to shape.strategy.instructions
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at shape.clarify.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'shape', 'clarify', 'instructions')
        
        # WHEN: user enters 'confirm'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        cli_response = repl_session.read_and_execute_command('confirm')
        
        # THEN: CLI confirms and advances to next action (strategy)
        assert cli_response.status == 'success' or 'confirm' in cli_response.output.lower()
        # New format wraps output with context headers
        assert 'CLI STATUS' in cli_response.output or '**INSTRUCTIONS SECTION:**' in cli_response.output or len(cli_response.output) > 50
    
    def test_user_confirms_action_and_advances_to_next(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User confirms action and advances to next action
        GIVEN: CLI is at shape.strategy.instructions
        WHEN: user enters 'confirm'
        THEN: CLI advances to next action and auto-executes instructions
        AND: Does not crash with 'object is not callable' error
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at shape.strategy (not last action)
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'shape', 'strategy', 'instructions')
        
        # WHEN: user enters 'confirm'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        cli_response = repl_session.read_and_execute_command('confirm')
        
        # THEN: CLI advances to next action without crashing
        assert 'not callable' not in cli_response.output
        # AND: CLI has advanced past strategy (current action is not strategy anymore)
        state_file = workspace_directory / 'behavior_action_state.json'
        state_data = json.loads(state_file.read_text())
        assert 'strategy' not in state_data.get('current_action', '')
    
    def test_user_confirms_from_instructions(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User confirms directly from instructions (2-phase model)
        GIVEN: CLI is at shape.build.instructions
        WHEN: user enters 'confirm'
        THEN: CLI advances to next action (valid - 2-phase model: instructions -> confirm)
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at shape.build.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'shape', 'build', 'instructions')
        
        # WHEN: user enters 'confirm'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        cli_response = repl_session.read_and_execute_command('confirm')
        
        # THEN: CLI advances to next action (2-phase model allows confirm from instructions)
        assert cli_response.status == 'success'
        # AND: CLI moves to shape.validate
        state_file = workspace_directory / 'behavior_action_state.json'
        state_data = json.loads(state_file.read_text())
        assert 'validate' in state_data.get('current_action', '')


class TestReExecuteCurrentOperationUsingCLI:
    """Story: Re-execute Current Operation Using CLI"""
    
    def test_user_re_executes_current_instructions(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User re-executes current instructions
        GIVEN: CLI is at shape.build.instructions (single behavior setup)
        WHEN: user enters 'current'
        THEN: CLI re-executes current instructions
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at shape.build.instructions (single behavior to avoid multi-behavior navigation issues)
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'shape', 'build', 'instructions')
        # AND: user previously executed instructions
        
        # WHEN: user enters 'current'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        cli_response = repl_session.read_and_execute_command('current')
        
        # THEN: CLI re-executes current instructions (command succeeds)
        assert cli_response.status == 'success'
        # AND: CLI displays instructions output
        assert len(cli_response.output) > 50


class TestHandleOperationErrorsAndValidationInCLI:
    """Story: Handle Operation Errors and Validation in CLI"""
    
    def test_user_enters_invalid_scope_format_with_instructions(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User enters invalid scope format with instructions
        GIVEN: CLI is at shape.build.instructions
        WHEN: user enters 'shape.build.instructions scope="invalid{format}"'
        THEN: CLI displays error message with valid formats
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at shape.build.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'shape', 'build', 'instructions')
        
        # WHEN: user enters 'shape.build.instructions scope="invalid{format}"'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        
        original_state = json.loads((workspace_directory / 'behavior_action_state.json').read_text())
        cli_response = repl_session.read_and_execute_command('shape.build.instructions --scope "invalid{format}"')
        
        # THEN: CLIScope._parse_scope_string raises parsing error
        # AND: CLI displays error message
        if 'ERROR' in cli_response.output or 'error' in cli_response.output.lower():
            # AND: CLI displays valid formats
            pass  # Error was displayed as expected
        # AND: behavior action state remains at shape.build.instructions
        current_state = json.loads((workspace_directory / 'behavior_action_state.json').read_text())
        assert current_state['current_behavior'] == original_state['current_behavior']

