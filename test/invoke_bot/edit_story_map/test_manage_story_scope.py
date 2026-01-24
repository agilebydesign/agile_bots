"""
Test Manage Story Scope

SubEpic: Manage Story Scope
Parent Epic: Invoke Bot > Edit Story Map

Domain tests verify core scope management logic.
CLI tests verify command parsing and output formatting across TTY, Pipe, and JSON channels.
"""
import pytest
from pathlib import Path
import json
import os
from helpers.bot_test_helper import BotTestHelper
from helpers import TTYBotTestHelper, PipeBotTestHelper, JsonBotTestHelper
from story_graph import StoryMap
from scanners.story_map import Epic, SubEpic, StoryGroup, Story, Scenario, ScenarioOutline


# ============================================================================
# DOMAIN TESTS - Core Scope Logic
# ============================================================================

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

# ============================================================================
# CLI TESTS - Scope Operations via CLI Commands
# ============================================================================

class TestNavigateStoryGraphUsingCLI:
    """
    Story: Navigate Story Graph Using CLI
    
    Domain logic: test_manage_scope.py::TestNavigateStoryGraph
    CLI focus: Story graph navigation with scope filtering
    """
    
    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper
    ])
    def test_navigate_story_graph_with_scope_via_cli(self, tmp_path, helper_class):
        """
        SCENARIO: Navigate story graph with scope via CLI
        GIVEN: CLI session with story graph and scope
        WHEN: navigation commands used
        THEN: Navigation respects scope
        
        Domain: Tests in TestNavigateStoryGraph
        """
        # Given
        helper = helper_class(tmp_path)
        helper.domain.state.set_state('shape', 'clarify')
        
        # When - Set scope
        cli_response = helper.cli_session.execute_command('scope set story TestStory')
        
        # Then - Validate complete scope response
        helper.scope.assert_scope_shows_target(cli_response.output, 'story', 'TestStory')


# ============================================================================
# STORY: Display Scope
# CLI-specific story
# ============================================================================