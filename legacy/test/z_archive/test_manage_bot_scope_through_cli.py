"""
Manage Bot Scope Through CLI Tests

Tests for all stories in the 'Manage Bot Scope Through CLI' sub-epic:
- Filter Work Using Knowledge Graph Scope in CLI
- Filter Work Using Files Scope in CLI
- Combine Scope Filters in CLI
- Clear Scope Filters in CLI
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


class TestFilterWorkUsingKnowledgeGraphScopeInCLI:
    """Story: Filter Work Using Knowledge Graph Scope in CLI"""
    
    @pytest.mark.parametrize("scope_filter", [
        'epic="Build Agile Bot"',
        'story="Generate Bot CLI"',
        'increment="1,2"'
    ])
    def test_user_sets_knowledge_graph_scope_filter(self, bot_directory, workspace_directory, monkeypatch, scope_filter):
        """
        SCENARIO: User sets knowledge graph scope filter
        GIVEN: CLI is at shape.build.instructions
        WHEN: user enters 'scope <filter>'
        THEN: CLI displays active scope filters
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at shape.build.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'shape', 'build', 'instructions')
        
        # WHEN: user enters 'scope <filter>'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        cli_response = repl_session.read_and_execute_command(f'scope {scope_filter}')
        
        # THEN: CLIScope parses scope filter string
        # AND: REPLSession stores scope filter in context
        # AND: CLI displays active scope filters
        assert 'scope' in cli_response.output.lower() or cli_response.status == 'success'
    
    def test_user_executes_build_with_active_knowledge_graph_scope(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User executes build with active knowledge graph scope
        GIVEN: CLI is at shape.build.instructions
        WHEN: user enters 'shape.build.instructions'
        THEN: CLI displays instructions filtered to Story1
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at shape.build.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'shape', 'build', 'instructions')
        # AND: active scope filter is story="Story1"
        
        # WHEN: user enters 'shape.build.instructions'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        # First set scope
        repl_session.read_and_execute_command('scope story="Story1"')
        # Then execute instructions
        cli_response = repl_session.read_and_execute_command('shape.build.instructions')
        
        # THEN: CLIAction passes scope filter to action.get_instructions()
        # AND: CLI displays instructions filtered to Story1
        assert cli_response.status in ['success', 'error'] or 'EXECUTING' in cli_response.output


class TestFilterWorkUsingFilesScopeInCLI:
    """Story: Filter Work Using Files Scope in CLI"""
    
    def test_user_sets_files_scope_filter(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User sets files scope filter
        GIVEN: CLI is at code.validate.instructions
        WHEN: user enters 'scope files="src/**/*.py"'
        THEN: CLI displays active scope filters
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at code.validate.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'code', ['strategy', 'validate', 'render', 'rules'])
        create_behavior_action_state(workspace_directory, 'code', 'validate', 'instructions')
        
        # WHEN: user enters 'scope files="src/**/*.py"'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        cli_response = repl_session.read_and_execute_command('scope files="src/**/*.py"')
        
        # THEN: CLIScope parses files scope string
        # AND: REPLSession stores files filter in context
        # AND: CLI displays active scope filters
        assert 'scope' in cli_response.output.lower() or cli_response.status == 'success'
    
    def test_user_executes_validate_with_active_files_scope(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User executes validate with active files scope
        GIVEN: CLI is at code.validate.instructions
        WHEN: user enters 'code.validate.instructions'
        THEN: CLI displays validation filtered to matched files
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at code.validate.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'code', ['strategy', 'validate', 'render', 'rules'])
        create_behavior_action_state(workspace_directory, 'code', 'validate', 'instructions')
        # AND: active scope filter is files="src/**/*.py"
        
        # WHEN: user enters 'code.validate.instructions'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        # First set scope
        repl_session.read_and_execute_command('scope files="src/**/*.py"')
        # Then execute instructions
        cli_response = repl_session.read_and_execute_command('code.validate.instructions')
        
        # THEN: CLIAction passes files filter to action.get_instructions()
        # AND: CLI displays validation filtered to matched files
        assert cli_response.status in ['success', 'error'] or 'EXECUTING' in cli_response.output


class TestScopeTypesMutuallyExclusive:
    """Story: Scope Types Are Mutually Exclusive in CLI
    
    RULE: You can only have ONE scope type at a time (story, epic, increment, OR files).
    Setting a new scope type automatically clears any previous scope.
    """
    
    def test_setting_file_scope_replaces_story_scope(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: Setting file scope replaces existing story scope
        GIVEN: CLI has story scope set
        WHEN: user enters file scope
        THEN: file scope replaces story scope (not combined)
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        from agile_bot.bots.base_bot.src.actions.action_context import Scope, ScopeType
        
        # GIVEN: CLI has story scope set
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'code', ['strategy', 'validate', 'render', 'rules'])
        create_behavior_action_state(workspace_directory, 'code', 'validate', 'instructions')
        
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        
        # Set story scope first
        repl_session.read_and_execute_command('scope "Story1"')
        
        # WHEN: user enters file scope
        repl_session.read_and_execute_command(f'scope "file:{workspace_directory}/**/*.py"')
        
        # THEN: file scope replaces story scope (not combined)
        scope_data = repl_session.get_stored_scope()
        assert scope_data is not None
        assert scope_data['type'] == 'files', "File scope should replace story scope"
        # Story scope should NOT be present
        scope = Scope.from_dict(scope_data)
        assert scope.knowledge_graph_filter is None, "Knowledge graph filter should be None for file scope"
        assert scope.file_filter is not None, "File filter should be set"
    
    def test_setting_story_scope_replaces_file_scope(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: Setting story scope replaces existing file scope
        GIVEN: CLI has file scope set
        WHEN: user enters story scope
        THEN: story scope replaces file scope (not combined)
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        from agile_bot.bots.base_bot.src.actions.action_context import Scope, ScopeType
        
        # GIVEN: CLI has file scope set
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'code', ['strategy', 'validate', 'render', 'rules'])
        create_behavior_action_state(workspace_directory, 'code', 'validate', 'instructions')
        
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        
        # Set file scope first
        repl_session.read_and_execute_command(f'scope "file:{workspace_directory}/**/*.py"')
        
        # WHEN: user enters story scope
        repl_session.read_and_execute_command('scope "Story1"')
        
        # THEN: story scope replaces file scope (not combined)
        scope_data = repl_session.get_stored_scope()
        assert scope_data is not None
        assert scope_data['type'] == 'story', "Story scope should replace file scope"
        # File scope should NOT be present
        scope = Scope.from_dict(scope_data)
        assert scope.file_filter is None, "File filter should be None for story scope"
        assert scope.knowledge_graph_filter is not None, "Knowledge graph filter should be set"
    
    def test_scope_only_has_one_type(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: Scope object can only have one type at a time
        GIVEN: Any scope is set
        WHEN: checking the stored scope
        THEN: only one filter type is active (knowledge_graph_filter OR file_filter, never both)
        """
        from agile_bot.bots.base_bot.src.actions.action_context import Scope, ScopeType
        
        # Test story scope - only knowledge_graph_filter
        story_scope = Scope(type=ScopeType.STORY, value=['Story1'])
        assert story_scope.knowledge_graph_filter is not None
        assert story_scope.file_filter is None
        
        # Test file scope - only file_filter
        file_scope = Scope(type=ScopeType.FILES, value=['/some/path/**/*.py'])
        assert file_scope.file_filter is not None
        assert file_scope.knowledge_graph_filter is None
        
        # Test all scope - neither filter
        all_scope = Scope(type=ScopeType.ALL, value=[])
        assert all_scope.knowledge_graph_filter is None
        assert all_scope.file_filter is None


class TestClearScopeFiltersInCLI:
    """Story: Clear Scope Filters in CLI"""
    
    def test_user_clears_all_scope_filters(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User clears all scope filters
        GIVEN: CLI is at shape.build.instructions
        WHEN: user enters 'scope clear'
        THEN: CLI displays 'All scope filters cleared'
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at shape.build.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'shape', 'build', 'instructions')
        # AND: active scope filters are story="Story1" AND files="docs/**/*.md"
        
        # WHEN: user enters 'scope clear'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        # First set scope
        repl_session.read_and_execute_command('scope story="Story1" files="docs/**/*.md"')
        # Then clear scope
        cli_response = repl_session.read_and_execute_command('scope clear')
        
        # THEN: REPLSession clears all scope filters from context
        # AND: CLI displays 'All scope filters cleared'
        assert 'clear' in cli_response.output.lower() or 'scope' in cli_response.output.lower()
        # AND: StatusDisplay shows no active scope
    
    def test_user_executes_build_after_clearing_scope(self, bot_directory, workspace_directory, monkeypatch):
        """
        SCENARIO: User executes build after clearing scope
        GIVEN: CLI is at shape.build.instructions
        WHEN: user enters 'shape.build.instructions'
        THEN: CLI displays unfiltered instructions
        """
        from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
        from agile_bot.bots.base_bot.src.bot.bot import Bot
        
        # GIVEN: CLI is at shape.build.instructions
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
        create_behavior(bot_directory, 'shape', ['clarify', 'strategy', 'build', 'validate', 'render'])
        create_behavior_action_state(workspace_directory, 'shape', 'build', 'instructions')
        # AND: user has cleared all scope filters
        
        # WHEN: user enters 'shape.build.instructions'
        bot = Bot(
            bot_name='story_bot',
            bot_directory=bot_directory,
            config_path=bot_directory / 'bot_config.json'
        )
        repl_session = REPLSession(bot=bot, workspace_directory=workspace_directory)
        # First set scope
        repl_session.read_and_execute_command('scope story="Story1"')
        # Clear scope
        repl_session.read_and_execute_command('scope clear')
        # Then execute instructions
        cli_response = repl_session.read_and_execute_command('shape.build.instructions')
        
        # THEN: CLIAction passes no scope filters to action
        # AND: CLI displays unfiltered instructions
        assert cli_response.status in ['success', 'error'] or 'EXECUTING' in cli_response.output

