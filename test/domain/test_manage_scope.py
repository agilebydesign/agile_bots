
import pytest
from pathlib import Path
from domain.bot_test_helper import BotTestHelper
from scope.action_scope import ActionScope
from scanners.story_map import (
    StoryMap, Epic, SubEpic, StoryGroup, Story, Scenario, ScenarioOutline
)


# ================================================================================
# SUB-EPIC: Manage Scope
# ================================================================================

class TestCreateScope:
    
    @pytest.mark.parametrize("parameters,expected_scope_contains", [
        # Scope 'all'
        ({'scope': {'type': 'all'}}, {'all': True}),
        # Single story
        ({'scope': {'type': 'story', 'value': ['Story1']}}, {'story_names': ['Story1']}),
        # Multiple stories
        ({'scope': {'type': 'story', 'value': ['Story1', 'Story2']}}, {'story_names': ['Story1', 'Story2']}),
        # Single increment priority
        ({'scope': {'type': 'increment', 'value': [1]}}, {'increment_priorities': [1]}),
        # Multiple increment priorities
        ({'scope': {'type': 'increment', 'value': [1, 2]}}, {'increment_priorities': [1, 2]}),
        # Single epic
        ({'scope': {'type': 'epic', 'value': ['Epic A']}}, {'epic_names': ['Epic A']}),
        # Multiple epics
        ({'scope': {'type': 'epic', 'value': ['Epic A', 'Epic B']}}, {'epic_names': ['Epic A', 'Epic B']}),
        # Increment by name
        ({'scope': {'type': 'increment', 'value': ['Increment 1']}}, {'increment_names': ['Increment 1']}),
        # No parameters defaults to 'all'
        ({}, {'all': True}),
    ])
    def test_scope_created_with_different_parameter_combinations(self, tmp_path, parameters, expected_scope_contains):
        """
        SCENARIO: Scope created with different parameter combinations
        GIVEN: Parameters dict with scope configuration
        WHEN: ActionScope instantiated with parameters
        THEN: ActionScope scope property returns expected configuration
        """
        helper = BotTestHelper(tmp_path)
        action_scope = ActionScope(parameters, None)
        
        helper.build.assert_build_scope_matches(action_scope, expected_scope_contains)
    
    def test_scope_defaults_to_all_when_no_parameters(self, tmp_path):
        """
        SCENARIO: Scope defaults to 'all' when no parameters provided
        GIVEN: Empty parameters dict
        WHEN: ActionScope instantiated
        THEN: Scope defaults to 'all'
        """
        helper = BotTestHelper(tmp_path)
        parameters = {}
        
        action_scope = ActionScope(parameters, None)
        
        helper.build.assert_build_scope_contains(action_scope, 'all', True)

class TestFilterScopeByStories:
    
    def test_filter_returns_all_when_scope_is_all(self, tmp_path):
        """
        SCENARIO: Filter returns all when scope is all
        GIVEN: Story graph with multiple epics and increments
        WHEN: Filter with scope type 'all'
        THEN: Story graph contains all epics and increments
        """
        helper = BotTestHelper(tmp_path)
        story_graph = helper.story.story_graph_with_epics_and_increments()
        
        filtered_graph = helper.scope.filter_story_graph('build', 'all', None, story_graph=story_graph)
        
        helper.scope.assert_story_graph_contains_all_epics(filtered_graph, 2)
        helper.scope.assert_story_graph_contains_all_increments(filtered_graph, 2)
    
    def test_filter_by_single_story_name_returns_matching_story(self, tmp_path):
        """
        SCENARIO: Filter by single story name returns matching story
        GIVEN: Story graph with multiple stories
        WHEN: Filter with single story name
        THEN: Story graph contains only matching story and its parent epic
        """
        helper = BotTestHelper(tmp_path)
        story_graph = helper.story.story_graph_with_epics_and_increments()
        
        filtered_graph = helper.scope.filter_story_graph('build', 'story', ['Story A1'], story_graph=story_graph)
        
        helper.scope.assert_story_graph_contains_epic(filtered_graph, 'Epic A')
        helper.scope.assert_story_graph_contains_story(filtered_graph, 'Story A1')
        assert 'Epic B' not in [epic.get('name') for epic in filtered_graph.get('epics', [])]
    
    def test_filter_by_single_epic_name_returns_matching_epic(self, tmp_path):
        """
        SCENARIO: Filter by single epic name returns matching epic
        GIVEN: Story graph with multiple epics
        WHEN: Filter with single epic name
        THEN: Story graph contains only matching epic and its increments
        """
        helper = BotTestHelper(tmp_path)
        story_graph = helper.story.story_graph_with_epics_and_increments()
        
        filtered_graph = helper.scope.filter_story_graph('build', 'epic', ['Epic A'], story_graph=story_graph)
        
        helper.scope.assert_story_graph_contains_epic(filtered_graph, 'Epic A')
        assert 'Epic B' not in [epic.get('name') for epic in filtered_graph.get('epics', [])]
        helper.scope.assert_story_graph_contains_increment(filtered_graph, 'Increment 1')
    
    def test_filter_by_increment_priorities_returns_matching_increments(self, tmp_path):
        """
        SCENARIO: Filter by increment priorities returns matching increments
        GIVEN: Story graph with increments having different priorities
        WHEN: Filter with increment priorities
        THEN: Story graph contains only matching increments and their stories
        """
        helper = BotTestHelper(tmp_path)
        story_graph = helper.story.story_graph_with_epics_and_increments()
        
        filtered_graph = helper.scope.filter_story_graph('build', 'increment', [1], story_graph=story_graph)
        
        helper.scope.assert_story_graph_contains_increment(filtered_graph, 'Increment 1')
        assert 'Increment 2' not in [inc.get('name') for inc in filtered_graph.get('increments', [])]
        helper.scope.assert_story_graph_contains_epic(filtered_graph, 'Epic A')
    
    def test_filter_by_increment_names_returns_matching_increments(self, tmp_path):
        """
        SCENARIO: Filter by increment names returns matching increments
        GIVEN: Story graph with increments having different names
        WHEN: Filter with increment names
        THEN: Story graph contains only matching increments and their stories
        """
        helper = BotTestHelper(tmp_path)
        story_graph = helper.story.story_graph_with_epics_and_increments()
        
        filtered_graph = helper.scope.filter_story_graph('build', 'increment', ['Increment 1'], story_graph=story_graph)
        
        helper.scope.assert_story_graph_contains_increment(filtered_graph, 'Increment 1')
        assert 'Increment 2' not in [inc.get('name') for inc in filtered_graph.get('increments', [])]
        helper.scope.assert_story_graph_contains_epic(filtered_graph, 'Epic A')
    
    def test_filter_returns_parent_epic_when_child_story_matches(self, tmp_path):
        """
        SCENARIO: Filter returns parent epic when child story matches
        GIVEN: Story graph with epic containing story
        WHEN: Scope set to story name
        THEN: Story and parent epic are both returned
        """
        helper = BotTestHelper(tmp_path)
        story_graph = helper.story.story_graph_with_epics_and_increments()
        
        filtered_graph = helper.scope.filter_story_graph('build', 'story', ['Story A1'], story_graph=story_graph)
        
        helper.scope.assert_story_graph_contains_story(filtered_graph, 'Story A1')
        helper.scope.assert_story_graph_contains_epic(filtered_graph, 'Epic A')

class TestFilterScopeByFiles:
    """Tests for FileFilter functionality within scope operations."""
    
    def test_file_filter_includes_matching_files(self):
        """FileFilter includes files matching include patterns."""
        from scope import FileFilter
        from pathlib import Path
        
        files = [
            Path('test/test_file1.py'),
            Path('test/test_file2.py'),
            Path('src/source_file.py'),
            Path('docs/readme.md')
        ]
        
        file_filter = FileFilter(include_patterns=['**/test*.py'])
        filtered = file_filter.filter_files(files)
        
        assert len(filtered) == 2
        assert Path('test/test_file1.py') in filtered
        assert Path('test/test_file2.py') in filtered
        assert Path('src/source_file.py') not in filtered
    
    def test_file_filter_excludes_matching_files(self):
        """
        SCENARIO: FileFilter excludes files matching exclude patterns
        GIVEN: A list of files and a FileFilter with exclude patterns
        WHEN: filter_files() is called
        THEN: Files matching exclude patterns are removed
        """
        from scope import FileFilter
        from pathlib import Path
        
        # GIVEN: A list of files
        files = [
            Path('test/test_file1.py'),
            Path('test/test_file2.py'),
            Path('test/__pycache__/cached.pyc'),
            Path('test/.pytest_cache/file.py')
        ]
        
        # AND: A FileFilter with exclude pattern for cache files
        file_filter = FileFilter(exclude_patterns=['**/__pycache__/**', '**/.pytest_cache/**'])
        
        # WHEN: filter_files() is called
        filtered = file_filter.filter_files(files)
        
        # THEN: Cache files are excluded
        assert len(filtered) == 2
        assert Path('test/test_file1.py') in filtered
        assert Path('test/test_file2.py') in filtered
    
    def test_file_filter_combines_include_and_exclude(self):
        """
        SCENARIO: FileFilter combines include and exclude patterns
        GIVEN: A list of files and a FileFilter with both include and exclude patterns
        WHEN: filter_files() is called
        THEN: Files must match include AND not match exclude
        """
        from scope import FileFilter
        from pathlib import Path
        
        # GIVEN: A list of files
        files = [
            Path('test/test_execute_in_headless_mode.py'),
            Path('test/test_monitor_session.py'),
            Path('test/test_helpers.py'),
            Path('src/source.py')
        ]
        
        # AND: A FileFilter with include for test files and exclude for helpers
        file_filter = FileFilter(
            include_patterns=['**/test*.py'],
            exclude_patterns=['**/*helpers*.py']
        )
        
        # WHEN: filter_files() is called
        filtered = file_filter.filter_files(files)
        
        # THEN: Test files are included except helpers
        assert len(filtered) == 2
        assert Path('test/test_execute_in_headless_mode.py') in filtered
        assert Path('test/test_monitor_session.py') in filtered
        assert Path('test/test_helpers.py') not in filtered
    
    def test_file_filter_returns_all_when_no_patterns(self):
        """
        SCENARIO: FileFilter returns all files when no patterns specified
        GIVEN: A list of files and a FileFilter with no patterns
        WHEN: filter_files() is called
        THEN: All files are returned
        """
        from scope import FileFilter
        from pathlib import Path
        
        # GIVEN: A list of files
        files = [
            Path('test/test_file1.py'),
            Path('src/source.py'),
            Path('docs/readme.md')
        ]
        
        # AND: A FileFilter with no patterns
        file_filter = FileFilter()
        
        # WHEN: filter_files() is called
        filtered = file_filter.filter_files(files)
        
        # THEN: All files are returned
        assert len(filtered) == 3
        assert all(f in filtered for f in files)
    
    def test_file_filter_handles_specific_file_paths(self):
        """
        SCENARIO: FileFilter handles specific file paths (not just globs)
        GIVEN: A list of files and a FileFilter with specific file path
        WHEN: filter_files() is called
        THEN: Only the specific file is included
        """
        from scope import FileFilter
        from pathlib import Path
        
        # GIVEN: A list of files
        files = [
            Path('test/test_execute_in_headless_mode.py'),
            Path('test/test_monitor_session.py'),
            Path('test/test_helpers.py')
        ]
        
        # AND: A FileFilter with specific file path
        file_filter = FileFilter(include_patterns=['**/test_execute_in_headless_mode.py'])
        
        # WHEN: filter_files() is called
        filtered = file_filter.filter_files(files)
        
        # THEN: Only the specific file is included
        assert len(filtered) == 1
        assert Path('test/test_execute_in_headless_mode.py') in filtered
    
    def test_file_discovery_and_filtering_integration(self):
        """
        SCENARIO: File discovery and filtering work together
        GIVEN: A FileDiscovery component and a FileFilter
        WHEN: Files are discovered and then filtered
        THEN: Only matching files are returned
        
        This test verifies the integration between FileDiscovery and FileFilter,
        which was the core fix for the validation scope bug.
        """
        from scope import FileFilter
        from pathlib import Path
        
        # GIVEN: A list of discovered files (simulating FileDiscovery output)
        discovered_files = [
            Path('test/test_execute_in_headless_mode.py'),
            Path('test/test_monitor_session.py'),
            Path('test/test_helpers.py'),
            Path('test/__pycache__/cached.pyc')
        ]
        
        # AND: A FileFilter for specific files
        file_filter = FileFilter(
            include_patterns=['**/test_execute_in_headless_mode.py', '**/test_monitor_session.py'],
            exclude_patterns=['**/__pycache__/**']
        )
        
        # WHEN: Files are filtered
        filtered_files = file_filter.filter_files(discovered_files)
        
        # THEN: Only matching files are returned
        assert len(filtered_files) == 2
        assert Path('test/test_execute_in_headless_mode.py') in filtered_files
        assert Path('test/test_monitor_session.py') in filtered_files
        assert Path('test/test_helpers.py') not in filtered_files
        assert Path('test/__pycache__/cached.pyc') not in filtered_files

class TestPersistScope:
    
    def test_scope_persists_across_bot_invocations(self, tmp_path):
        """
        SCENARIO: Scope persists across bot invocations
        GIVEN: Bot with scope set
        WHEN: Bot is reloaded
        THEN: Scope is restored from workflow state
        """
        # TODO: Implement scope persistence tests
        pass
    
    def test_scope_persists_after_action_execution(self, tmp_path):
        """
        SCENARIO: Scope persists after action execution
        GIVEN: Bot with scope set
        WHEN: Action executes and completes
        THEN: Scope remains active for next action
        """
        # TODO: Implement
        pass

class TestClearScope:
    
    def test_clear_scope_with_show_all_parameter(self, tmp_path):
        """
        SCENARIO: Clear scope with show_all parameter
        GIVEN: Bot with scope set
        WHEN: Scope cleared with show_all=True
        THEN: Scope is cleared and all content is shown
        """
        # TODO: Implement clear scope tests
        pass
    
    def test_clear_scope_without_show_all_parameter(self, tmp_path):
        """
        SCENARIO: Clear scope without show_all parameter
        GIVEN: Bot with scope set
        WHEN: Scope cleared without show_all parameter
        THEN: Scope is cleared
        """
        # TODO: Implement
        pass
    
    def test_actions_after_clear_process_all_content(self, tmp_path):
        """
        SCENARIO: Actions after clear process all content
        GIVEN: Bot had scope set, then cleared
        WHEN: Action executes
        THEN: Action processes all content without filtering
        """
        # TODO: Implement
        pass

class TestExecuteActionsWithScope:
    
    def test_build_action_includes_scope_in_instructions(self, tmp_path):
        """
        SCENARIO: Build action includes scope in instructions
        GIVEN: Build action with story scope
        WHEN: Instructions are retrieved
        THEN: Instructions contain scope configuration
        """
        from actions.action_context import ScopeActionContext
        from scope import Scope, StoryGraphFilter
        
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('shape')
        action = helper.bot.behaviors.current.actions.find_by_name('build')
        
        from scope import ScopeType
        scope = Scope(workspace_directory=tmp_path)
        scope.filter(type=ScopeType.STORY, value=['Story1', 'Story2'])
        context = ScopeActionContext(scope=scope)
        
        instructions = action.get_instructions(context)
        
        assert 'scope' in instructions
        assert instructions['scope'] is not None
        assert isinstance(instructions['scope'], dict)
    
    def test_validate_action_accepts_scope_context(self, tmp_path):
        """
        SCENARIO: Validate action accepts scope context
        GIVEN: Validate action with story scope and story graph file
        WHEN: Instructions are retrieved
        THEN: No errors occur and scope is processed
        """
        from actions.action_context import ValidateActionContext
        from scope import Scope, StoryGraphFilter
        
        helper = BotTestHelper(tmp_path)
        
        # Create story graph file (validate requires it)
        story_graph = helper.story.given_story_graph_dict(epic='exploration')
        stories_dir = helper.workspace / 'docs' / 'stories'
        helper.files.given_file_created(stories_dir, 'story-graph.json', story_graph)
        
        helper.bot.behaviors.navigate_to('exploration')
        action = helper.bot.behaviors.current.actions.find_by_name('validate')
        
        from scope import ScopeType
        scope = Scope(workspace_directory=tmp_path)
        scope.filter(type=ScopeType.STORY, value=['Story1'])
        context = ValidateActionContext(scope=scope)
        
        # Should not raise an error
        instructions = action.get_instructions(context)
        assert instructions is not None
        # Validate uses ScopeActionContext (via ValidateActionContext)
        assert hasattr(context, 'scope')
    
    def test_render_action_accepts_scope_context(self, tmp_path):
        """
        SCENARIO: Render action accepts scope context
        GIVEN: Render action with story scope
        WHEN: Instructions are retrieved
        THEN: No errors occur (render supports ScopeActionContext)
        """
        from actions.action_context import ScopeActionContext
        from scope import Scope, ScopeType
        
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('exploration')
        action = helper.bot.behaviors.current.actions.find_by_name('render')
        
        scope = Scope(workspace_directory=tmp_path)
        scope.filter(type=ScopeType.STORY, value=['Story1'])
        context = ScopeActionContext(scope=scope)
        
        # Should not raise an error
        instructions = action.get_instructions(context)
        assert instructions is not None
    
    def test_clarify_action_does_not_support_scope(self, tmp_path):
        """
        SCENARIO: Clarify action does not support scope
        GIVEN: Clarify action
        WHEN: Context is checked
        THEN: Uses ClarifyActionContext (not ScopeActionContext)
        """
        from actions.action_context import ClarifyActionContext
        
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('shape')
        action = helper.bot.behaviors.current.actions.find_by_name('clarify')
        
        # Clarify uses ClarifyActionContext, not ScopeActionContext
        assert action.context_class == ClarifyActionContext
        assert not hasattr(action.context_class(), 'scope')
    
    def test_strategy_action_does_not_support_scope(self, tmp_path):
        """
        SCENARIO: Strategy action does not support scope
        GIVEN: Strategy action
        WHEN: Context is checked
        THEN: Uses StrategyActionContext (not ScopeActionContext)
        """
        from actions.action_context import StrategyActionContext
        
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('shape')
        action = helper.bot.behaviors.current.actions.find_by_name('strategy')
        
        # Strategy uses StrategyActionContext, not ScopeActionContext
        assert action.context_class == StrategyActionContext
        assert not hasattr(action.context_class(), 'scope')

class TestNavigateStoryGraph:
    
    @staticmethod
    def _create_mock_bot(bot_directory: Path):
        """Helper: Create MockBot instance for testing StoryMap.from_bot().
        
        Used by: test_from_bot_loads_story_graph, test_from_bot_raises_when_file_not_found
        """
        class MockBot:
            def __init__(self, bot_directory):
                self.bot_directory = bot_directory
        
        return MockBot(bot_directory)
    
    def test_story_map_loads_epics(self, tmp_path):
        """
        SCENARIO: Story Map Loads Epics
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        # When: Epics are retrieved from story map
        epics = helper.story.when_item_accessed('epics', story_map)
        # Then: Epics contain single build knowledge epic
        helper.story.assert_story_map_matches(epics)
    
    def test_epic_has_sub_epics(self, tmp_path):
        """
        SCENARIO: Epic Has Sub Epics
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        epics = helper.story.when_item_accessed('epics', story_map)
        epic = helper.story.assert_story_map_matches(epics)
        # When: Epic children are retrieved
        children = epic.children
        # Then: Children contain single sub epic
        assert len(children) == 1
        assert isinstance(children[0], SubEpic)
        assert children[0].name == "Load Story Graph"
    
    def test_sub_epic_has_story_groups(self, tmp_path):
        """
        SCENARIO: Sub Epic Has Story Groups
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        epics = helper.story.when_item_accessed('epics', story_map)
        epic = helper.story.assert_story_map_matches(epics)
        sub_epic = epic.children[0]
        # When: Sub epic children are retrieved
        children = sub_epic.children
        # Then: Children contain single story group
        assert len(children) == 1
        assert isinstance(children[0], StoryGroup)
    
    def test_story_group_has_stories(self, tmp_path):
        """
        SCENARIO: Story Group Has Stories
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        epics = helper.story.when_item_accessed('epics', story_map)
        epic = helper.story.assert_story_map_matches(epics)
        sub_epic = epic.children[0]
        story_group = sub_epic.children[0]
        # When: Story group stories are retrieved
        stories = story_group.children
        # Then: Stories contain single story
        assert len(stories) == 1
        assert isinstance(stories[0], Story)
        assert stories[0].name == "Load Story Graph Into Memory"
    
    def test_story_has_properties(self, tmp_path):
        """
        SCENARIO: Story Has Properties
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        # When: Story is retrieved from path
        story = helper.story.when_item_accessed('story', story_map)
        # Then: Story has expected properties
        assert story.name == "Load Story Graph Into Memory"
        assert story.users == ["Story Bot"]
        assert story.story_type == "user"
        assert story.sizing == "5 days"
        assert story.sequential_order == 1
        assert story.connector is None
    
    def test_story_has_scenarios(self, tmp_path):
        """
        SCENARIO: Story Has Scenarios
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        story = helper.story.when_item_accessed('story', story_map)
        # When: Story scenarios are retrieved
        scenarios = story.scenarios
        # Then: Scenarios contain expected scenarios
        assert len(scenarios) == 2
        assert isinstance(scenarios[0], Scenario)
        assert scenarios[0].name == "Story graph file exists"
        assert scenarios[0].type == "happy_path"
        assert scenarios[1].name == "Story graph file missing"
        assert scenarios[1].type == "error_case"
    
    def test_scenario_has_properties(self, tmp_path):
        """
        SCENARIO: Scenario Has Properties
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        story = helper.story.when_item_accessed('story', story_map)
        # When: Scenario is retrieved from story
        scenario = helper.story.when_item_accessed('scenario', story)
        # Then: Scenario has expected properties
        assert scenario.name == "Story graph file exists"
        assert scenario.type == "happy_path"
        assert len(scenario.background) == 1
        assert scenario.background[0] == "Given story graph file exists"
        assert len(scenario.steps) == 2
        assert scenario.steps[0] == "When story graph is loaded"
        assert scenario.steps[1] == "Then story map is created with epics"
    
    def test_scenario_default_test_method(self, tmp_path):
        """
        SCENARIO: Scenario Default Test Method
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        story = helper.story.when_item_accessed('story', story_map)
        # When: Scenario is retrieved from story
        scenario = helper.story.when_item_accessed('scenario', story)
        # Then: Scenario has default test method
        assert scenario.default_test_method == "test_story_graph_file_exists"
    
    def test_story_has_scenario_outlines(self, tmp_path):
        """
        SCENARIO: Story Has Scenario Outlines
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        story = helper.story.when_item_accessed('story', story_map)
        # When: Story scenario outlines are retrieved
        scenario_outlines = story.scenario_outlines
        # Then: Scenario outlines contain expected outline
        assert len(scenario_outlines) == 1
        assert isinstance(scenario_outlines[0], ScenarioOutline)
        assert scenario_outlines[0].name == "Load story graph with different formats"
    
    def test_scenario_outline_has_examples(self, tmp_path):
        """
        SCENARIO: Scenario Outline Has Examples
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        story = helper.story.when_item_accessed('story', story_map)
        # When: Scenario outline is retrieved from story
        scenario_outline = helper.story.when_item_accessed('scenario_outline', story)
        # Then: Scenario outline has expected examples
        assert len(scenario_outline.examples_columns) == 2
        assert scenario_outline.examples_columns == ["file_path", "expected_epics"]
        assert len(scenario_outline.examples_rows) == 2
        assert scenario_outline.examples_rows[0] == ["story-graph.json", "2"]
        assert scenario_outline.examples_rows[1] == ["story-graph-v2.json", "3"]
    
    def test_story_default_test_class(self, tmp_path):
        """
        SCENARIO: Story Default Test Class
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        # When: Story is retrieved from path
        story = helper.story.when_item_accessed('story', story_map)
        # Then: Story has default test class
        assert story.default_test_class == "TestLoadStoryGraphIntoMemory"
    
    def test_story_map_walk_traverses_all_nodes(self, tmp_path):
        """
        SCENARIO: Story Map Walk Traverses All Nodes
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        epics = helper.story.when_item_accessed('epics', story_map)
        epic = helper.story.when_item_accessed('epic', epics)
        # When: Story map is walked
        nodes = list(story_map.walk(epic))
        # Then: Nodes match expected structure
        assert len(nodes) == 4
        assert isinstance(nodes[0], Epic)
        assert nodes[0].name == "Build Knowledge"
        assert isinstance(nodes[1], SubEpic)
        assert nodes[1].name == "Load Story Graph"
        assert isinstance(nodes[2], StoryGroup)
        assert isinstance(nodes[3], Story)
        assert nodes[3].name == "Load Story Graph Into Memory"
    
    def test_map_location_for_epic(self, tmp_path):
        """
        SCENARIO: Map Location For Epic
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        epics = helper.story.when_item_accessed('epics', story_map)
        # When: First epic is retrieved
        epic = helper.story.when_item_accessed('epic', epics)
        # Then: Epic map location is correct
        helper.story.assert_map_location_matches(epic)
    
    def test_map_location_for_sub_epic(self, tmp_path):
        """
        SCENARIO: Map Location For Sub Epic
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        epics = helper.story.when_item_accessed('epics', story_map)
        # When: Sub epic is retrieved from epics
        sub_epic = helper.story.when_item_accessed('sub_epic', epics)
        # Then: Sub epic map location is correct
        helper.story.assert_map_location_matches(sub_epic)
    
    def test_map_location_for_story(self, tmp_path):
        """
        SCENARIO: Map Location For Story
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        epics = helper.story.when_item_accessed('epics', story_map)
        # When: Story is retrieved from epics
        story = helper.story.when_item_accessed('story', epics)
        # Then: Story map location is correct
        helper.story.assert_map_location_matches(story)
    
    def test_scenario_map_location(self, tmp_path):
        """
        SCENARIO: Scenario Map Location
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        epics = helper.story.when_item_accessed('epics', story_map)
        # When: Scenario is retrieved from epics
        scenario = helper.story.when_item_accessed('scenario', epics)
        # Then: Scenario map location is correct
        helper.story.assert_map_location_matches(scenario)
    
    def test_scenario_outline_map_location(self, tmp_path):
        """
        SCENARIO: Scenario Outline Map Location
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        epics = helper.story.when_item_accessed('epics', story_map)
        # When: Scenario outline is retrieved from epics
        scenario_outline = helper.story.when_item_accessed('scenario_outline', epics)
        # Then: Scenario outline map location is correct
        helper.story.assert_map_location_matches(scenario_outline)
    
    def test_from_bot_loads_story_graph(self, tmp_path):
        """
        SCENARIO: From Bot Loads Story Graph
        """
        # Use custom bot directory to avoid modifying production bot
        helper = BotTestHelper(tmp_path, bot_directory=tmp_path / 'bot')
        stories_dir = helper.bot_directory / 'docs' / 'stories'
        stories_dir.mkdir(parents=True, exist_ok=True)
        story_graph = helper.story.given_story_graph_dict()
        story_graph_path = helper.files.given_file_created(stories_dir, 'story-graph.json', story_graph)
        story_map = StoryMap.from_bot(helper.bot_directory)
        helper.story.assert_story_map_matches(story_map)
    
    def test_from_bot_with_path(self, tmp_path):
        """
        SCENARIO: From Bot With Path
        """
        # Given: Bot directory, docs directory, and story graph file are created
        # Use custom bot directory to avoid modifying production bot
        helper = BotTestHelper(tmp_path, bot_directory=tmp_path / 'bot')
        stories_dir = helper.bot_directory / 'docs' / 'stories'
        stories_dir.mkdir(parents=True, exist_ok=True)
        story_graph = helper.story.given_story_graph_dict()
        story_graph_path = helper.files.given_file_created(stories_dir, 'story-graph.json', story_graph)
        # When: Story map is created from bot
        story_map = StoryMap.from_bot(helper.bot_directory)
        # Then: Story map contains test epic
        helper.story.assert_story_map_matches(story_map)
    
    def test_scenario_map_location_duplicate(self, tmp_path):
        """
        SCENARIO: Scenario Map Location
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        epics = helper.story.when_item_accessed('epics', story_map)
        # When: Scenario is retrieved from epics
        scenario = helper.story.when_item_accessed('scenario', epics)
        # Then: Scenario map location is correct
        helper.story.assert_map_location_matches(scenario)
    
    def test_scenario_outline_map_location_duplicate(self, tmp_path):
        """
        SCENARIO: Scenario Outline Map Location
        """
        # Given: Story map is loaded
        helper = BotTestHelper(tmp_path)
        story_map = helper.story.create_story_map()
        epics = helper.story.when_item_accessed('epics', story_map)
        # When: Scenario outline is retrieved from epics
        scenario_outline = helper.story.when_item_accessed('scenario_outline', epics)
        # Then: Scenario outline map location is correct
        helper.story.assert_map_location_matches(scenario_outline)

class TestEnrichScopeWithLinks:
    """Tests for link enrichment in JSON scope (test icons and doc links)."""
    
    def test_story_with_test_file_and_class_gets_test_link(self, tmp_path):
        """
        SCENARIO: Story with test_file and test_class gets test tube icon link
        GIVEN: Story graph with story having test_file and test_class
        AND: Test file exists on disk
        WHEN: Scope is enriched with links
        THEN: Story has test_tube icon link pointing to test file
        """
        from scope.json_scope import JSONScope
        from scope import Scope, ScopeType
        
        helper = BotTestHelper(tmp_path)
        
        # Create test file
        test_dir = helper.workspace / 'test'
        test_dir.mkdir(exist_ok=True)
        test_file = test_dir / 'test_story.py'
        test_file.write_text('class TestMyStory:\n    def test_scenario(self):\n        pass')
        
        # Create story graph - story gets test_file from parent sub-epic
        story_graph = {
            'epics': [{
                'name': 'Test Epic',
                'sub_epics': [{
                    'name': 'Test Sub Epic',
                    'sequential_order': 1.0,
                    'test_file': 'test_story.py',  # Sub-epic has test_file
                    'story_groups': [{
                        'type': 'and',
                        'stories': [{
                            'name': 'Test Story',
                            # No test_file - inherits from parent sub-epic
                            'test_class': 'TestMyStory',
                            'sequential_order': 1.0
                        }]
                    }]
                }]
            }]
        }
        helper.story.create_story_graph(story_graph)
        
        # Create scope and get results
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.SHOW_ALL)
        json_scope = JSONScope(scope)
        result = json_scope.to_dict()
        
        # Verify test link was added
        story = result['content']['epics'][0]['sub_epics'][0]['story_groups'][0]['stories'][0]
        assert 'links' in story
        test_links = [l for l in story['links'] if l['icon'] == 'test_tube']
        assert len(test_links) == 1
        assert 'test_story.py' in test_links[0]['url']
        assert 'TestMyStory' in test_links[0]['url']
    
    def test_story_without_test_file_gets_no_test_link(self, tmp_path):
        """
        SCENARIO: Story with test_class but no test_file gets no test icon
        GIVEN: Story graph with story having test_class but no test_file
        WHEN: Scope is enriched with links
        THEN: Story has no test_tube icon link
        """
        from scope.json_scope import JSONScope
        from scope import Scope, ScopeType
        
        helper = BotTestHelper(tmp_path)
        
        # Create story graph with only test_class using helper
        story_graph = {
            'epics': [{
                'name': 'Test Epic',
                'sub_epics': [{
                    'name': 'Test Sub Epic',
                    'sequential_order': 1.0,
                    'story_groups': [{
                        'type': 'and',
                        'stories': [{
                            'name': 'Test Story',
                            'test_class': 'TestMyStory',  # Has test_class
                            # No test_file
                            'sequential_order': 1.0
                        }]
                    }]
                }]
            }]
        }
        helper.story.create_story_graph(story_graph)
        
        # Create scope and get results
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.SHOW_ALL)
        json_scope = JSONScope(scope)
        result = json_scope.to_dict()
        
        # Verify no test link was added
        story = result['content']['epics'][0]['sub_epics'][0]['story_groups'][0]['stories'][0]
        test_links = [l for l in story.get('links', []) if l['icon'] == 'test_tube']
        assert len(test_links) == 0
    
    def test_sub_epic_with_test_file_gets_test_link(self, tmp_path):
        """
        SCENARIO: Sub-epic with test_file gets test tube icon link
        GIVEN: Story graph with sub-epic having test_file
        AND: Test file exists on disk
        WHEN: Scope is enriched with links
        THEN: Sub-epic has test_tube icon link pointing to test file
        """
        from scope.json_scope import JSONScope
        from scope import Scope, ScopeType
        
        helper = BotTestHelper(tmp_path)
        
        # Create test file
        test_dir = helper.workspace / 'test'
        test_dir.mkdir(exist_ok=True)
        test_file = test_dir / 'test_sub_epic.py'
        test_file.write_text('def test_something():\n    pass')
        
        # Create story graph with sub-epic having test_file using helper
        story_graph = {
            'epics': [{
                'name': 'Test Epic',
                'sub_epics': [{
                    'name': 'Test Sub Epic',
                    'sequential_order': 1.0,
                    'test_file': 'test_sub_epic.py',
                    'story_groups': []
                }]
            }]
        }
        helper.story.create_story_graph(story_graph)
        
        # Create scope and get results
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.SHOW_ALL)
        json_scope = JSONScope(scope)
        result = json_scope.to_dict()
        
        # Verify test link was added
        sub_epic = result['content']['epics'][0]['sub_epics'][0]
        assert 'links' in sub_epic
        test_links = [l for l in sub_epic['links'] if l['icon'] == 'test_tube']
        assert len(test_links) == 1
        assert 'test_sub_epic.py' in test_links[0]['url']
    
    def test_story_inherits_test_file_from_sub_epic(self, tmp_path):
        """
        SCENARIO: Story inherits test_file from parent sub-epic
        GIVEN: Sub-epic with test_file and story with test_class but no test_file
        AND: Test file exists on disk
        WHEN: Scope is enriched with links
        THEN: Story gets test_tube icon link using parent's test_file
        """
        from scope.json_scope import JSONScope
        from scope import Scope, ScopeType
        
        helper = BotTestHelper(tmp_path)
        
        # Create test file
        test_dir = helper.workspace / 'test'
        test_dir.mkdir(exist_ok=True)
        test_file = test_dir / 'test_sub_epic.py'
        test_file.write_text('class TestMyStory:\n    pass')
        
        # Create story graph: sub-epic has test_file, story has test_class using helper
        story_graph = {
            'epics': [{
                'name': 'Test Epic',
                'sub_epics': [{
                    'name': 'Test Sub Epic',
                    'sequential_order': 1.0,
                    'test_file': 'test_sub_epic.py',
                    'story_groups': [{
                        'type': 'and',
                        'stories': [{
                            'name': 'Test Story',
                            'test_class': 'TestMyStory',
                            # No test_file - should inherit from parent
                            'sequential_order': 1.0
                        }]
                    }]
                }]
            }]
        }
        helper.story.create_story_graph(story_graph)
        
        # Create scope and get results
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.SHOW_ALL)
        json_scope = JSONScope(scope)
        result = json_scope.to_dict()
        
        # Verify story got test link using parent's test_file
        story = result['content']['epics'][0]['sub_epics'][0]['story_groups'][0]['stories'][0]
        assert 'links' in story
        test_links = [l for l in story['links'] if l['icon'] == 'test_tube']
        assert len(test_links) == 1
        assert 'test_sub_epic.py' in test_links[0]['url']
        assert 'TestMyStory' in test_links[0]['url']
    
    def test_epic_with_docs_folder_gets_document_link(self, tmp_path):
        """
        SCENARIO: Epic with docs folder gets document icon link
        GIVEN: Epic and corresponding docs/map folder exists
        WHEN: Scope is enriched with links
        THEN: Epic has document icon link pointing to docs folder
        """
        from scope.json_scope import JSONScope
        from scope import Scope, ScopeType
        
        helper = BotTestHelper(tmp_path)
        
        # Create docs folder for epic at docs/stories/map (the actual path structure)
        epic_folder = helper.workspace / 'docs' / 'stories' / 'map' / '🎯 Test Epic'
        epic_folder.mkdir(parents=True, exist_ok=True)
        
        # Create story graph using helper
        story_graph = {
            'epics': [{
                'name': 'Test Epic',
                'sub_epics': []
            }]
        }
        helper.story.create_story_graph(story_graph)
        
        # Create scope and get results
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.SHOW_ALL)
        json_scope = JSONScope(scope)
        result = json_scope.to_dict()
        
        # Verify document link was added
        epic = result['content']['epics'][0]
        assert 'links' in epic, f"Epic should have links. Epic data: {epic}"
        doc_links = [l for l in epic['links'] if l['icon'] == 'document']
        assert len(doc_links) == 1, f"Epic should have one document link. Links: {epic.get('links', [])}"
        assert '🎯 Test Epic' in doc_links[0]['url']
    
    @pytest.mark.parametrize("sub_epic_test_file,story_test_class,has_test_link", [
        # Sub-epic has test_file and story has test_class -> has link
        ('test_story.py', 'TestMyStory', True),
        # Sub-epic has test_file but story has no test_class -> no link
        ('test_story.py', None, False),
        # Sub-epic has no test_file but story has test_class -> no link
        (None, 'TestMyStory', False),
        # Neither sub-epic test_file nor story test_class -> no link
        (None, None, False),
    ])
    def test_story_test_link_combinations(self, tmp_path, sub_epic_test_file, story_test_class, has_test_link):
        """
        SCENARIO: Story test link appears based on sub-epic test_file and story test_class
        GIVEN: Sub-epic with/without test_file and story with/without test_class
        WHEN: Scope is enriched with links
        THEN: Test link appears only when sub-epic has test_file AND story has test_class
        """
        from scope.json_scope import JSONScope
        from scope import Scope, ScopeType
        
        helper = BotTestHelper(tmp_path)
        
        # Create test file if specified on sub-epic
        if sub_epic_test_file:
            test_dir = helper.workspace / 'test'
            test_dir.mkdir(exist_ok=True)
            test_path = test_dir / sub_epic_test_file
            test_path.write_text('class TestMyStory:\n    pass')
        
        # Create story data with test_class (stories don't have test_file)
        story_data = {
            'name': 'Test Story',
            'sequential_order': 1.0
        }
        if story_test_class:
            story_data['test_class'] = story_test_class
        
        # Create sub-epic with test_file
        sub_epic_data = {
            'name': 'Test Sub Epic',
            'sequential_order': 1.0,
            'story_groups': [{
                'type': 'and',
                'stories': [story_data]
            }]
        }
        if sub_epic_test_file:
            sub_epic_data['test_file'] = sub_epic_test_file
        
        story_graph = {
            'epics': [{
                'name': 'Test Epic',
                'sub_epics': [sub_epic_data]
            }]
        }
        
        # Save using helper
        helper.story.create_story_graph(story_graph)
        
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.SHOW_ALL)
        json_scope = JSONScope(scope)
        result = json_scope.to_dict()
        
        # Verify test link presence
        story = result['content']['epics'][0]['sub_epics'][0]['story_groups'][0]['stories'][0]
        test_links = [l for l in story.get('links', []) if l['icon'] == 'test_tube']
        
        if has_test_link:
            assert len(test_links) == 1, f"Story should have test link with sub_epic test_file={sub_epic_test_file}, story test_class={story_test_class}"
            assert sub_epic_test_file in test_links[0]['url']
            assert story_test_class in test_links[0]['url']
        else:
            assert len(test_links) == 0, f"Story should not have test link with sub_epic test_file={sub_epic_test_file}, story test_class={story_test_class}"
    
    def test_scenario_with_test_method_gets_test_link(self, tmp_path):
        """
        SCENARIO: Scenario with test_method gets test link
        GIVEN: Story with scenario having test_method
        AND: Test file exists with that method
        WHEN: Scope is enriched with links
        THEN: Scenario has test link with line number
        """
        from scope.json_scope import JSONScope
        from scope import Scope, ScopeType
        
        helper = BotTestHelper(tmp_path)
        
        # Create test file with test method
        test_dir = helper.workspace / 'test'
        test_dir.mkdir(exist_ok=True)
        test_file = test_dir / 'test_story.py'
        test_file.write_text('''class TestMyStory:
    def test_happy_path(self):
        pass
    
    def test_error_case(self):
        pass
''')
        
        # Create story graph with scenario having test_method using helper
        story_graph = {
            'epics': [{
                'name': 'Test Epic',
                'sub_epics': [{
                    'name': 'Test Sub Epic',
                    'sequential_order': 1.0,
                    'test_file': 'test_story.py',  # Sub-epic has test_file
                    'story_groups': [{
                        'type': 'and',
                        'stories': [{
                            'name': 'Test Story',
                            # No test_file - inherits from parent sub-epic
                            'test_class': 'TestMyStory',
                            'sequential_order': 1.0,
                            'scenarios': [{
                                'name': 'Happy path scenario',
                                'test_method': 'test_happy_path',
                                'type': 'happy_path',
                                'steps': 'Given X\nWhen Y\nThen Z'
                            }]
                        }]
                    }]
                }]
            }]
        }
        helper.story.create_story_graph(story_graph)
        
        # Use 'story' scope type instead of 'showAll' to enable scenario enrichment
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.STORY, value=['Test Story'])
        json_scope = JSONScope(scope)
        result = json_scope.to_dict()
        
        # Verify scenario has test link with line number
        story = result['content']['epics'][0]['sub_epics'][0]['story_groups'][0]['stories'][0]
        scenario = story['scenarios'][0]
        
        assert 'test_file' in scenario, "Scenario should have test_file link"
        assert 'test_story.py' in scenario['test_file']
        assert '#L' in scenario['test_file'], "Scenario test link should include line number"
    
    @pytest.mark.parametrize("has_test_method,sub_epic_has_test_file,has_link", [
        # Scenario with test_method and sub-epic has test_file -> has link
        (True, True, True),
        # Scenario with test_method but sub-epic has no test_file -> no link
        (True, False, False),
        # Scenario without test_method but sub-epic has test_file -> no link
        (False, True, False),
        # Scenario without test_method and sub-epic without test_file -> no link
        (False, False, False),
    ])
    def test_scenario_test_link_combinations(self, tmp_path, has_test_method, sub_epic_has_test_file, has_link):
        """
        SCENARIO: Scenario test link appears based on test_method and sub-epic test_file
        GIVEN: Scenario with/without test_method and sub-epic with/without test_file
        WHEN: Scope is enriched with links
        THEN: Test link appears only when scenario has test_method and sub-epic has test_file
        """
        from scope.json_scope import JSONScope
        from scope import Scope, ScopeType
        
        helper = BotTestHelper(tmp_path)
        
        # Create test file if sub-epic needs it
        if sub_epic_has_test_file:
            test_dir = helper.workspace / 'test'
            test_dir.mkdir(exist_ok=True)
            test_file = test_dir / 'test_story.py'
            test_file.write_text('class TestMyStory:\n    def test_scenario(self):\n        pass')
        
        # Create scenario data
        scenario_data = {
            'name': 'Test Scenario',
            'type': 'happy_path',
            'steps': 'Given X\nWhen Y\nThen Z'
        }
        if has_test_method:
            scenario_data['test_method'] = 'test_scenario'
        
        # Create story data (stories don't have test_file - they inherit from sub-epic)
        story_data = {
            'name': 'Test Story',
            'test_class': 'TestMyStory',
            'sequential_order': 1.0,
            'scenarios': [scenario_data]
        }
        
        # Create sub-epic data with test_file
        sub_epic_data = {
            'name': 'Test Sub Epic',
            'sequential_order': 1.0,
            'story_groups': [{
                'type': 'and',
                'stories': [story_data]
            }]
        }
        if sub_epic_has_test_file:
            sub_epic_data['test_file'] = 'test_story.py'
        
        story_graph = {
            'epics': [{
                'name': 'Test Epic',
                'sub_epics': [sub_epic_data]
            }]
        }
        
        # Save using helper
        helper.story.create_story_graph(story_graph)
        
        # Use 'story' scope type instead of 'showAll' to enable scenario enrichment
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.STORY, value=['Test Story'])
        json_scope = JSONScope(scope)
        result = json_scope.to_dict()
        
        # Verify scenario test link
        story = result['content']['epics'][0]['sub_epics'][0]['story_groups'][0]['stories'][0]
        scenario = story['scenarios'][0]
        
        if has_link:
            assert 'test_file' in scenario, "Scenario should have test_file link"
            assert 'test_story.py' in scenario['test_file']
        else:
            # Scenario may have test_file field but it should be empty or not point to actual test
            if 'test_file' in scenario:
                assert scenario['test_file'] is None or scenario['test_file'] == ''
