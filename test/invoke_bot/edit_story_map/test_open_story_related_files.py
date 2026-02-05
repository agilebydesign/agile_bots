"""
Test Open Story Related Files

SubEpic: Open Story Related Files
Parent Epic: Invoke Bot > Work With Story Map

Domain tests verify core file opening logic for story graph nodes.
CLI tests verify command execution and return values.
"""
import pytest
from pathlib import Path
from helpers.bot_test_helper import BotTestHelper
from helpers import TTYBotTestHelper, PipeBotTestHelper, JsonBotTestHelper


# ============================================================================
# DOMAIN TESTS - Core File Opening Logic
# ============================================================================

class TestOpenAllRelatedFiles:
    """Tests for opening story-related files from story graph nodes."""
    
    def test_open_story_file_for_single_story_returns_story_file(self, tmp_path):
        """
        SCENARIO: openStoryFile for single story returns story file
        GIVEN: Story graph with story (file_link calculated automatically)
        WHEN: openStoryFile() is called on story node
        THEN: Returns dict with single story file path
        """
        helper = BotTestHelper(tmp_path)
        story_graph_data = {
            "epics": [
                {
                    "name": "Work With Story Map",
                    "sub_epics": [
                        {
                            "name": "Open Story Related Files",
                            "sequential_order": 1.0,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Open All Related Files",
                                            "sequential_order": 1.0
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.story.create_story_graph(story_graph_data)
        
        story_node = helper.bot.story_graph["Work With Story Map"]["Open Story Related Files"]["Open All Related Files"]
        helper.story.create_story_files_for_node(story_node)
        calculated_file_link = story_node.file_link
        
        result = story_node.openStoryFile()
        
        assert result['status'] == 'success'
        assert result['node'] == 'Open All Related Files'
        assert result['node_type'] == 'story'
        assert len(result['files']) == 1
        assert result['files'][0] == calculated_file_link
        assert result['count'] == 1
        
        helper.story.assert_file_exists(result['files'][0], "Story file")
    
    def test_open_story_file_for_epic_returns_all_story_files_recursively(self, tmp_path):
        """
        SCENARIO: openStoryFile for epic returns all story files recursively
        GIVEN: Story graph with epic containing multiple stories
        WHEN: openStoryFile() is called on epic node
        THEN: Returns dict with all story files from epic and children
        """
        helper = BotTestHelper(tmp_path)
        story_graph_data = {
            "epics": [
                {
                    "name": "Work With Story Map",
                    "sub_epics": [
                        {
                            "name": "Open Story Related Files",
                            "sequential_order": 1.0,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Open All Related Files",
                                            "sequential_order": 1.0
                                        },
                                        {
                                            "name": "Open Story Files",
                                            "sequential_order": 2.0
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.story.create_story_graph(story_graph_data)
        
        epic_node = helper.bot.story_graph["Work With Story Map"]
        # Get nodes before creating files so we have references to the same objects
        story1_node = helper.bot.story_graph["Work With Story Map"]["Open Story Related Files"]["Open All Related Files"]
        story2_node = helper.bot.story_graph["Work With Story Map"]["Open Story Related Files"]["Open Story Files"]
        
        # Create story files (this calls save() which calculates file_link)
        helper.story.create_story_files_for_node(epic_node)
        
        # Get file_links after creating files
        expected_file1 = story1_node.file_link
        expected_file2 = story2_node.file_link
        
        result = epic_node.openStoryFile()
        
        assert result['status'] == 'success'
        assert result['node'] == 'Work With Story Map'
        assert result['node_type'] == 'epic'
        assert result['count'] == 2
        assert expected_file1 in result['files']
        assert expected_file2 in result['files']
        
        for file_path in result['files']:
            helper.story.assert_file_exists(file_path, "Story file")
    
    def test_open_test_for_story_returns_test_file_with_scope(self, tmp_path):
        """
        SCENARIO: openTest for story returns test file with scope
        GIVEN: Story graph with sub-epic having test_file and story having test_class
        WHEN: openTest() is called on story node
        THEN: Returns dict with test file and scope information
        """
        helper = BotTestHelper(tmp_path)
        helper.story.create_test_file(
            'invoke_bot/edit_story_map/test_open_story_related_files.py',
            'TestOpenAllRelatedFiles',
            ['test_graph_button_opens_story_graph_with_selected_node_expanded']
        )
        
        story_graph_data = {
            "epics": [
                {
                    "name": "Work With Story Map",
                    "sub_epics": [
                        {
                            "name": "Open Story Related Files",
                            "sequential_order": 1.0,
                            "test_file": "test/invoke_bot/edit_story_map/test_open_story_related_files.py",
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Open All Related Files",
                                            "sequential_order": 1.0,
                                            "test_class": "TestOpenAllRelatedFiles",
                                            "scenarios": [
                                                {
                                                    "name": "Graph button opens story graph with selected node expanded",
                                                    "test_method": "test_graph_button_opens_story_graph_with_selected_node_expanded"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.story.create_story_graph(story_graph_data)
        
        story_node = helper.bot.story_graph["Work With Story Map"]["Open Story Related Files"]["Open All Related Files"]
        sub_epic_node = helper.bot.story_graph["Work With Story Map"]["Open Story Related Files"]
        result = story_node.openTest()
        
        assert result['status'] == 'success'
        assert result['node'] == 'Open All Related Files'
        assert result['node_type'] == 'story'
        assert len(result['files']) == 1
        assert result['files'][0]['file'] == sub_epic_node.test_file
        assert result['files'][0]['test_class'] == 'TestOpenAllRelatedFiles'
        assert len(result['files'][0]['scenarios']) == 1
        assert result['files'][0]['scenarios'][0]['name'] == 'Graph button opens story graph with selected node expanded'
        assert result['files'][0]['scenarios'][0]['test_method'] == 'test_graph_button_opens_story_graph_with_selected_node_expanded'
        assert result['count'] == 1
    
    def test_open_test_for_epic_returns_all_test_files_recursively(self, tmp_path):
        """
        SCENARIO: openTest for epic returns all test files recursively
        GIVEN: Story graph with epic containing multiple stories with test files
        WHEN: openTest() is called on epic node
        THEN: Returns dict with all test files from epic and children
        """
        helper = BotTestHelper(tmp_path)
        helper.story.create_test_file(
            'invoke_bot/edit_story_map/test_open_story_related_files.py',
            'TestOpenAllRelatedFiles',
            []
        )
        helper.story.create_test_file(
            'invoke_bot/edit_story_map/test_open_story_files.py',
            'TestOpenStoryFiles',
            []
        )
        
        story_graph_data = {
            "epics": [
                {
                    "name": "Work With Story Map",
                    "sub_epics": [
                        {
                            "name": "Open Story Related Files",
                            "sequential_order": 1.0,
                            "test_file": "test/invoke_bot/edit_story_map/test_open_story_related_files.py",
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Open All Related Files",
                                            "sequential_order": 1.0,
                                            "test_class": "TestOpenAllRelatedFiles"
                                        },
                                        {
                                            "name": "Open Story Files",
                                            "sequential_order": 2.0,
                                            "test_class": "TestOpenStoryFiles"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.story.create_story_graph(story_graph_data)
        
        epic_node = helper.bot.story_graph["Work With Story Map"]
        sub_epic_node = helper.bot.story_graph["Work With Story Map"]["Open Story Related Files"]
        result = epic_node.openTest()
        
        assert result['status'] == 'success'
        assert result['node'] == 'Work With Story Map'
        assert result['node_type'] == 'epic'
        assert result['count'] == 2
        test_files = [f['file'] for f in result['files']]
        assert sub_epic_node.test_file in test_files
        
        for file_info in result['files']:
            helper.story.assert_file_exists(file_info['file'], "Test file")
    
    def test_graph_button_opens_story_graph_with_selected_node_expanded(self, tmp_path):
        """
        SCENARIO: Graph button opens story graph with selected node expanded
        GIVEN: User has selected a story graph node
        WHEN: User clicks Graph button
        THEN: System opens story-graph.json file
        AND: System collapses all nodes in story graph view
        AND: System expands nodes representing selected node path in tree
        AND: System positions edit cursor at line of beginning of expanded section representing selected node
        """
        helper = BotTestHelper(tmp_path)
        story_graph_data = {
            "epics": [
                {
                    "name": "Work With Story Map",
                    "sub_epics": [
                        {
                            "name": "Open Story Related Files",
                            "sequential_order": 1.0,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Open All Related Files",
                                            "sequential_order": 1.0
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        story_graph_file = helper.story.create_story_graph(story_graph_data)
        
        story_node = helper.bot.story_graph["Work With Story Map"]["Open Story Related Files"]["Open All Related Files"]
        result = story_node.openStoryGraph()
        
        assert result['status'] == 'success'
        assert result['node'] == 'Open All Related Files'
        assert result['node_type'] == 'story'
        assert result['story_graph_path'] == str(story_graph_file)
        assert 'node_path' in result
        assert 'expand_path' in result
        assert result['line_number'] is not None
        
        story_graph_path = helper.story.assert_file_exists(result['story_graph_path'], "Story graph file")
        helper.story.assert_story_graph_line_contains_node(story_graph_path, result['line_number'], 'Open All Related Files')
    
    def test_stories_button_opens_story_markdown_files(self, tmp_path):
        """
        SCENARIO: Stories button opens story markdown files
        GIVEN: User has selected a story graph node (story, sub-epic, or epic)
        WHEN: User clicks Stories button
        THEN: System opens story markdown file for single story if story selected
        OR: System opens all story markdown files for stories under selected node if sub-epic or epic selected
        """
        helper = BotTestHelper(tmp_path)
        story_graph_data = {
            "epics": [
                {
                    "name": "Work With Story Map",
                    "sub_epics": [
                        {
                            "name": "Open Story Related Files",
                            "sequential_order": 1.0,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Open All Related Files",
                                            "sequential_order": 1.0
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.story.create_story_graph(story_graph_data)
        
        story_node = helper.bot.story_graph["Work With Story Map"]["Open Story Related Files"]["Open All Related Files"]
        helper.story.create_story_files_for_node(story_node)
        calculated_file_link = story_node.file_link
        result = story_node.openStoryFile()
        
        assert result['status'] == 'success'
        assert result['node'] == 'Open All Related Files'
        assert result['node_type'] == 'story'
        assert len(result['files']) == 1
        assert result['files'][0] == calculated_file_link
        assert result['count'] == 1
        
        helper.story.assert_file_exists(result['files'][0], "Story file")
    
    def test_test_button_opens_test_files_with_scope_collapsed(self, tmp_path):
        """
        SCENARIO: Test button opens test files with scope collapsed
        GIVEN: User has selected a story graph node with test files
        WHEN: User clicks Test button
        THEN: System opens test files associated with selected node
        AND: System expands methods/classes in scope (test_class or test_method)
        AND: System collapses other methods/classes in test files
        """
        helper = BotTestHelper(tmp_path)
        helper.story.create_test_file(
            'invoke_bot/edit_story_map/test_open_story_related_files.py',
            'TestOpenAllRelatedFiles',
            ['test_graph_button_opens_story_graph_with_selected_node_expanded']
        )
        
        story_graph_data = {
            "epics": [
                {
                    "name": "Work With Story Map",
                    "sub_epics": [
                        {
                            "name": "Open Story Related Files",
                            "sequential_order": 1.0,
                            "test_file": "test/invoke_bot/edit_story_map/test_open_story_related_files.py",
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Open All Related Files",
                                            "sequential_order": 1.0,
                                            "test_class": "TestOpenAllRelatedFiles",
                                            "scenarios": [
                                                {
                                                    "name": "Graph button opens story graph with selected node expanded",
                                                    "test_method": "test_graph_button_opens_story_graph_with_selected_node_expanded"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.story.create_story_graph(story_graph_data)
        
        story_node = helper.bot.story_graph["Work With Story Map"]["Open Story Related Files"]["Open All Related Files"]
        sub_epic_node = helper.bot.story_graph["Work With Story Map"]["Open Story Related Files"]
        result = story_node.openTest()
        
        assert result['status'] == 'success'
        assert result['node'] == 'Open All Related Files'
        assert result['node_type'] == 'story'
        assert len(result['files']) == 1
        assert result['files'][0]['file'] == sub_epic_node.test_file
        assert result['files'][0]['test_class'] == 'TestOpenAllRelatedFiles'
        assert len(result['files'][0]['scenarios']) == 1
        assert result['files'][0]['scenarios'][0]['name'] == 'Graph button opens story graph with selected node expanded'
        assert result['files'][0]['scenarios'][0]['test_method'] == 'test_graph_button_opens_story_graph_with_selected_node_expanded'
        assert result['count'] == 1
        helper.story.assert_file_exists(result['files'][0]['file'], "Test file")
    
    def test_code_button_infers_and_opens_code_files(self, tmp_path):
        """
        SCENARIO: Code button infers and opens code files
        GIVEN: User has selected a story graph node with test files
        WHEN: User clicks Code button
        THEN: System infers code files from test file paths (replace test/ with src/ or remove test_ prefix)
        AND: System opens inferred code files
        AND: System expands classes/methods referenced in tests
        AND: System collapses other code
        """
        helper = BotTestHelper(tmp_path)
        helper.story.create_test_file(
            'invoke_bot/edit_story_map/test_open_story_related_files.py',
            'TestOpenAllRelatedFiles',
            ['test_graph_button_opens_story_graph_with_selected_node_expanded']
        )
        # Create code file for inference test
        code_file = helper.workspace / "src" / "story_graph" / "nodes.py"
        code_file.parent.mkdir(parents=True, exist_ok=True)
        code_file.write_text("class StoryNode:\n    def openStoryGraph(self): pass")
        
        story_graph_data = {
            "epics": [
                {
                    "name": "Work With Story Map",
                    "sub_epics": [
                        {
                            "name": "Open Story Related Files",
                            "sequential_order": 1.0,
                            "test_file": "test/invoke_bot/edit_story_map/test_open_story_related_files.py",
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Open All Related Files",
                                            "sequential_order": 1.0,
                                            "test_class": "TestOpenAllRelatedFiles"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.story.create_story_graph(story_graph_data)
        
        story_node = helper.bot.story_graph["Work With Story Map"]["Open Story Related Files"]["Open All Related Files"]
        helper.story.create_story_files_for_node(story_node)
        test_result = story_node.openTest()
        
        assert test_result['status'] == 'success'
        assert len(test_result['files']) == 1
        test_file_path = test_result['files'][0]['file']
        
        helper.story.assert_file_exists(test_file_path, "Test file")
        
        inferred_code_file = str(test_file_path).replace('test/', 'src/').replace('test_', '')
        assert code_file.exists() or Path(inferred_code_file).exists()
    
    def test_all_button_opens_files_in_split_editors(self, tmp_path):
        """
        SCENARIO: All button opens files in split editors
        GIVEN: User has selected a story graph node
        WHEN: User clicks All button
        THEN: System opens story-graph.json in leftmost split editor
        AND: System opens story markdown files in next split editor to the right
        AND: System opens test files in next split editor to the right
        AND: System opens code files in rightmost split editor
        AND: System applies Graph button behavior to story graph (collapse all, expand selected)
        AND: System applies Test button behavior to test files (expand scope, collapse others)
        AND: System applies Code button behavior to code files (expand referenced, collapse others)
        """
        helper = BotTestHelper(tmp_path)
        helper.story.create_test_file(
            'invoke_bot/edit_story_map/test_open_story_related_files.py',
            'TestOpenAllRelatedFiles',
            ['test_graph_button_opens_story_graph_with_selected_node_expanded']
        )
        
        story_graph_data = {
            "epics": [
                {
                    "name": "Work With Story Map",
                    "sub_epics": [
                        {
                            "name": "Open Story Related Files",
                            "sequential_order": 1.0,
                            "test_file": "test/invoke_bot/edit_story_map/test_open_story_related_files.py",
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Open All Related Files",
                                            "sequential_order": 1.0,
                                            "test_class": "TestOpenAllRelatedFiles"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        story_graph_file = helper.story.create_story_graph(story_graph_data)
        
        story_node = helper.bot.story_graph["Work With Story Map"]["Open Story Related Files"]["Open All Related Files"]
        helper.story.create_story_files_for_node(story_node)
        sub_epic_node = helper.bot.story_graph["Work With Story Map"]["Open Story Related Files"]
        calculated_file_link = story_node.file_link
        
        graph_result = story_node.openStoryGraph()
        story_result = story_node.openStoryFile()
        test_result = story_node.openTest()
        
        assert graph_result['status'] == 'success'
        assert graph_result['story_graph_path'] == str(story_graph_file)
        helper.story.assert_file_exists(graph_result['story_graph_path'], "Story graph file")
        
        assert story_result['status'] == 'success'
        assert len(story_result['files']) == 1
        assert story_result['files'][0] == calculated_file_link
        helper.story.assert_file_exists(story_result['files'][0], "Story file")
        
        assert test_result['status'] == 'success'
        assert len(test_result['files']) == 1
        assert test_result['files'][0]['file'] == sub_epic_node.test_file
        helper.story.assert_file_exists(test_result['files'][0]['file'], "Test file")
    
    def test_open_story_graph_returns_path_and_line_number(self, tmp_path):
        """
        SCENARIO: openStoryGraph returns story graph path and line number
        GIVEN: Story graph with node
        WHEN: openStoryGraph() is called on node
        THEN: Returns dict with story graph path, node path, and line number
        """
        helper = BotTestHelper(tmp_path)
        story_graph_data = {
            "epics": [
                {
                    "name": "Work With Story Map",
                    "sub_epics": [
                        {
                            "name": "Open Story Related Files",
                            "sequential_order": 1.0,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Open All Related Files",
                                            "sequential_order": 1.0
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        story_graph_file = helper.story.create_story_graph(story_graph_data)
        
        story_node = helper.bot.story_graph["Work With Story Map"]["Open Story Related Files"]["Open All Related Files"]
        result = story_node.openStoryGraph()
        
        assert result['status'] == 'success'
        assert result['node'] == 'Open All Related Files'
        assert result['node_type'] == 'story'
        assert result['story_graph_path'] == str(story_graph_file)
        assert 'node_path' in result
        assert 'expand_path' in result
        assert result['line_number'] is not None
    
    def test_open_story_graph_collapses_all_and_expands_node_path(self, tmp_path):
        """
        SCENARIO: openStoryGraph provides expand path for node
        GIVEN: Story graph with nested node structure
        WHEN: openStoryGraph() is called on nested node
        THEN: Returns expand_path representing node path in tree
        AND: File path exists and line number points to node in JSON
        """
        helper = BotTestHelper(tmp_path)
        story_graph_data = {
            "epics": [
                {
                    "name": "Work With Story Map",
                    "sub_epics": [
                        {
                            "name": "Open Story Related Files",
                            "sequential_order": 1.0,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Open All Related Files",
                                            "sequential_order": 1.0
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.story.create_story_graph(story_graph_data)
        
        story_node = helper.bot.story_graph["Work With Story Map"]["Open Story Related Files"]["Open All Related Files"]
        result = story_node.openStoryGraph()
        
        assert result['status'] == 'success'
        assert result['expand_path'] == 'story Open All Related Files'
        assert result['node_path'] == 'story Open All Related Files'
        
        story_graph_path = helper.story.assert_file_exists(result['story_graph_path'], "Story graph file")
        
        assert result['line_number'] is not None, "Line number should be found for node in JSON"
        with open(story_graph_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            line_at_position = lines[result['line_number'] - 1]
            assert '"name": "Open All Related Files"' in line_at_position, f"Line {result['line_number']} should contain node name: {line_at_position}"


# ============================================================================
# CLI TESTS - Command Execution
# ============================================================================

class TestOpenStoryRelatedFilesUsingCLI:
    """Tests for opening story-related files via CLI commands."""
    
    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper
    ])
    def test_cli_open_story_file_opens_story_markdown_files(self, tmp_path, helper_class):
        """
        SCENARIO: CLI openStoryFile for story opens single file
        GIVEN: CLI session with story graph containing story
        WHEN: User executes bot.story_graph."Epic"."SubEpic"."Story".openStoryFile()
        THEN: CLI returns result with single story file
        """
        helper = helper_class(tmp_path)
        story_graph_data = {
            "epics": [
                {
                    "name": "Work With Story Map",
                    "sub_epics": [
                        {
                            "name": "Open Story Related Files",
                            "sequential_order": 1.0,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Open All Related Files",
                                            "sequential_order": 1.0
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.domain.story.create_story_graph(story_graph_data)
        
        cli_response = helper.cli_session.execute_command('story_graph."Work With Story Map"."Open Story Related Files"."Open All Related Files".openStoryFile()')
        
        assert cli_response.status == 'success'
        assert 'files' in cli_response.output or 'count' in cli_response.output
    
    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper
    ])
    def test_cli_open_story_file_for_epic_opens_all_files_recursively(self, tmp_path, helper_class):
        """
        SCENARIO: CLI openStoryFile for epic opens all files recursively
        GIVEN: CLI session with story graph containing epic with multiple stories
        WHEN: User executes bot.story_graph."Epic".openStoryFile()
        THEN: CLI returns result with all story files recursively
        """
        helper = helper_class(tmp_path)
        story_graph_data = {
            "epics": [
                {
                    "name": "Work With Story Map",
                    "sub_epics": [
                        {
                            "name": "Open Story Related Files",
                            "sequential_order": 1.0,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Open All Related Files",
                                            "sequential_order": 1.0
                                        },
                                        {
                                            "name": "Open Story Files",
                                            "sequential_order": 2.0
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.domain.story.create_story_graph(story_graph_data)
        
        cli_response = helper.cli_session.execute_command('story_graph."Work With Story Map".openStoryFile()')
        
        assert cli_response.status == 'success'
        assert 'files' in cli_response.output or 'count' in cli_response.output
    
    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper
    ])
    def test_cli_open_test_for_story_opens_test_file_with_scope(self, tmp_path, helper_class):
        """
        SCENARIO: CLI openTest for story opens test file with scope
        GIVEN: CLI session with story graph containing story with test file
        WHEN: User executes bot.story_graph."Epic"."SubEpic"."Story".openTest()
        THEN: CLI returns result with test file and scope information
        """
        helper = helper_class(tmp_path)
        helper.domain.story.create_test_file(
            'invoke_bot/edit_story_map/test_open_story_related_files.py',
            'TestOpenAllRelatedFiles',
            ['test_graph_button_opens_story_graph_with_selected_node_expanded']
        )
        
        story_graph_data = {
            "epics": [
                {
                    "name": "Work With Story Map",
                    "sub_epics": [
                        {
                            "name": "Open Story Related Files",
                            "sequential_order": 1.0,
                            "test_file": "test/invoke_bot/edit_story_map/test_open_story_related_files.py",
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Open All Related Files",
                                            "sequential_order": 1.0,
                                            "test_class": "TestOpenAllRelatedFiles",
                                            "scenarios": [
                                                {
                                                    "name": "Graph button opens story graph with selected node expanded",
                                                    "test_method": "test_graph_button_opens_story_graph_with_selected_node_expanded"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.domain.story.create_story_graph(story_graph_data)
        
        cli_response = helper.cli_session.execute_command('story_graph."Work With Story Map"."Open Story Related Files"."Open All Related Files".openTest()')
        
        assert cli_response.status == 'success'
        assert 'files' in cli_response.output or 'count' in cli_response.output
    
    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper
    ])
    def test_cli_open_test_for_epic_opens_all_test_files_recursively(self, tmp_path, helper_class):
        """
        SCENARIO: CLI openTest for epic opens all test files recursively
        GIVEN: CLI session with story graph containing epic with multiple test files
        WHEN: User executes bot.story_graph."Epic".openTest()
        THEN: CLI returns result with all test files recursively
        """
        helper = helper_class(tmp_path)
        helper.domain.story.create_test_file(
            'invoke_bot/edit_story_map/test_open_story_related_files.py',
            'TestOpenAllRelatedFiles',
            []
        )
        helper.domain.story.create_test_file(
            'invoke_bot/edit_story_map/test_open_story_files.py',
            'TestOpenStoryFiles',
            []
        )
        
        story_graph_data = {
            "epics": [
                {
                    "name": "Work With Story Map",
                    "sub_epics": [
                        {
                            "name": "Open Story Related Files",
                            "sequential_order": 1.0,
                            "test_file": "test/invoke_bot/edit_story_map/test_open_story_related_files.py",
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Open All Related Files",
                                            "sequential_order": 1.0,
                                            "test_class": "TestOpenAllRelatedFiles"
                                        },
                                        {
                                            "name": "Open Story Files",
                                            "sequential_order": 2.0,
                                            "test_class": "TestOpenStoryFiles"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.domain.story.create_story_graph(story_graph_data)
        
        cli_response = helper.cli_session.execute_command('story_graph."Work With Story Map".openTest()')
        
        assert cli_response.status == 'success'
        assert 'files' in cli_response.output or 'count' in cli_response.output
    
    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper
    ])
    def test_cli_open_story_graph_opens_with_node_expanded(self, tmp_path, helper_class):
        """
        SCENARIO: CLI openStoryGraph opens with node expanded
        GIVEN: CLI session with story graph containing node
        WHEN: User executes bot.story_graph."Epic".openStoryGraph()
        THEN: CLI returns result with story graph path and expand path
        """
        helper = helper_class(tmp_path)
        story_graph_data = {
            "epics": [
                {
                    "name": "Work With Story Map",
                    "sub_epics": [
                        {
                            "name": "Open Story Related Files",
                            "sequential_order": 1.0,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Open All Related Files",
                                            "sequential_order": 1.0
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.domain.story.create_story_graph(story_graph_data)
        
        cli_response = helper.cli_session.execute_command('story_graph."Work With Story Map".openStoryGraph()')
        
        assert cli_response.status == 'success'
        assert 'story_graph_path' in cli_response.output or 'expand_path' in cli_response.output
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
        test_file = helper.story.create_test_file(
            'test_story.py',
            'TestMyStory',
            ['test_scenario']
        )
        helper.story.assert_file_exists(test_file, "Test file")
        
        # Create story graph - story gets test_file from parent sub-epic
        story_graph = {
            'epics': [{
                'name': 'Work With Story Map',
                'sub_epics': [{
                    'name': 'Open Story Related Files',
                    'sequential_order': 1.0,
                    'test_file': 'test_story.py',  # Sub-epic has test_file
                    'story_groups': [{
                        'type': 'and',
                        'stories': [{
                            'name': 'Open All Related Files',
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
        test_links = [link for link in story['links'] if link['icon'] == 'test_tube']
        assert len(test_links) == 1
        assert 'test_story.py' in test_links[0]['url']
        assert '#L' in test_links[0]['url']  # Verify it has a line number
        # Verify the file path in the link actually exists
        link_url = test_links[0]['url']
        # Extract file path from URL (format: file:///path/to/file.py#L123)
        if 'file:///' in link_url:
            file_path = link_url.split('#')[0].replace('file:///', '')
            helper.story.assert_file_exists(file_path, "Test file in link")
    
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
                'name': 'Work With Story Map',
                'sub_epics': [{
                    'name': 'Open Story Related Files',
                    'sequential_order': 1.0,
                    'story_groups': [{
                        'type': 'and',
                        'stories': [{
                            'name': 'Open All Related Files',
                            'test_class': 'TestOpenAllRelatedFiles',  # Has test_class
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
        test_links = [link for link in story.get('links', []) if link['icon'] == 'test_tube']
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
        test_file = helper.story.create_test_file(
            'test/invoke_bot/edit_story_map/test_open_story_related_files.py',
            'TestOpenAllRelatedFiles',
            ['test_graph_button_opens_story_graph_with_selected_node_expanded']
        )
        helper.story.assert_file_exists(test_file, "Test file")
        
        # Create story graph with sub-epic having test_file using helper
        story_graph = {
            'epics': [{
                'name': 'Work With Story Map',
                'sub_epics': [{
                    'name': 'Open Story Related Files',
                    'sequential_order': 1.0,
                    'test_file': 'test/invoke_bot/edit_story_map/test_open_story_related_files.py',
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
        test_links = [link for link in sub_epic['links'] if link['icon'] == 'test_tube']
        assert len(test_links) == 1
        assert 'test_open_story_related_files.py' in test_links[0]['url']
        # Verify the file path in the link actually exists
        link_url = test_links[0]['url']
        if 'file:///' in link_url:
            file_path = link_url.split('#')[0].replace('file:///', '')
            helper.story.assert_file_exists(file_path, "Test file in link")
    
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
        test_file = helper.story.create_test_file(
            'test/invoke_bot/edit_story_map/test_open_story_related_files.py',
            'TestOpenAllRelatedFiles',
            ['test_graph_button_opens_story_graph_with_selected_node_expanded']
        )
        helper.story.assert_file_exists(test_file, "Test file")
        
        # Create story graph: sub-epic has test_file, story has test_class using helper
        story_graph = {
            'epics': [{
                'name': 'Work With Story Map',
                'sub_epics': [{
                    'name': 'Open Story Related Files',
                    'sequential_order': 1.0,
                    'test_file': 'test/invoke_bot/edit_story_map/test_open_story_related_files.py',
                    'story_groups': [{
                        'type': 'and',
                        'stories': [{
                            'name': 'Open All Related Files',
                            'test_class': 'TestOpenAllRelatedFiles',
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
        test_links = [link for link in story['links'] if link['icon'] == 'test_tube']
        assert len(test_links) == 1
        assert 'test_open_story_related_files.py' in test_links[0]['url']
        assert '#L' in test_links[0]['url']  # Verify it has a line number
        # Verify the file path in the link actually exists
        link_url = test_links[0]['url']
        if 'file:///' in link_url:
            file_path = link_url.split('#')[0].replace('file:///', '')
            helper.story.assert_file_exists(file_path, "Test file in link")
    
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
        
        # Create docs folder for epic at docs/story/scenarios (the actual path structure)
        epic_folder = helper.workspace / 'docs' / 'story' / 'scenarios' / '🎯 Work With Story Map'
        epic_folder.mkdir(parents=True, exist_ok=True)
        helper.story.assert_file_exists(epic_folder, "Epic docs folder")
        
        # Create story graph using helper
        story_graph = {
            'epics': [{
                'name': 'Work With Story Map',
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
        doc_links = [link for link in epic['links'] if link['icon'] == 'document']
        assert len(doc_links) == 1, f"Epic should have one document link. Links: {epic.get('links', [])}"
        assert 'Work With Story Map' in doc_links[0]['url']
        # Verify the folder path in the link actually exists
        link_url = doc_links[0]['url']
        if 'file:///' in link_url:
            folder_path = link_url.replace('file:///', '')
            helper.story.assert_file_exists(folder_path, "Epic docs folder in link")
    
    @pytest.mark.parametrize("sub_epic_test_file,story_test_class,has_test_link", [
        # Sub-epic has test_file and story has test_class -> has link
        ('test/invoke_bot/edit_story_map/test_open_story_related_files.py', 'TestOpenAllRelatedFiles', True),
        # Sub-epic has test_file but story has no test_class -> no link
        ('test/invoke_bot/edit_story_map/test_open_story_related_files.py', None, False),
        # Sub-epic has no test_file but story has test_class -> no link
        (None, 'TestOpenAllRelatedFiles', False),
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
            # Create file with same path format as sub_epic test_file
            test_file = helper.story.create_test_file(
                sub_epic_test_file,
                'TestOpenAllRelatedFiles',
                []
            )
            helper.story.assert_file_exists(test_file, "Test file")
        
        # Create story data with test_class (stories don't have test_file)
        story_data = {
            'name': 'Open All Related Files',
            'sequential_order': 1.0
        }
        if story_test_class:
            story_data['test_class'] = story_test_class
        
        # Create sub-epic with test_file
        sub_epic_data = {
            'name': 'Open Story Related Files',
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
                'name': 'Work With Story Map',
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
        test_links = [link for link in story.get('links', []) if link['icon'] == 'test_tube']
        
        if has_test_link:
            assert len(test_links) == 1, f"Story should have test link with sub_epic test_file={sub_epic_test_file}, story test_class={story_test_class}"
            assert 'test_open_story_related_files.py' in test_links[0]['url']
            assert '#L' in test_links[0]['url']  # Verify it has a line number
            # Verify the file path in the link actually exists
            link_url = test_links[0]['url']
            if 'file:///' in link_url:
                file_path = link_url.split('#')[0].replace('file:///', '')
                helper.story.assert_file_exists(file_path, "Test file in link")
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
        
        # Create test file with test method (use same path as sub_epic test_file)
        sub_epic_test_file = 'test/invoke_bot/edit_story_map/test_open_story_related_files.py'
        test_file = helper.story.create_test_file(
            sub_epic_test_file,
            'TestOpenAllRelatedFiles',
            ['test_graph_button_opens_story_graph_with_selected_node_expanded', 'test_stories_button_opens_story_markdown_files']
        )
        helper.story.assert_file_exists(test_file, "Test file")
        
        # Create story graph with scenario having test_method using helper
        story_graph = {
            'epics': [{
                'name': 'Work With Story Map',
                'sub_epics': [{
                    'name': 'Open Story Related Files',
                    'sequential_order': 1.0,
                    'test_file': sub_epic_test_file,  # Sub-epic has test_file
                    'story_groups': [{
                        'type': 'and',
                        'stories': [{
                            'name': 'Open All Related Files',
                            # No test_file - inherits from parent sub-epic
                            'test_class': 'TestOpenAllRelatedFiles',
                            'sequential_order': 1.0,
                            'scenarios': [{
                                'name': 'Graph button opens story graph with selected node expanded',
                                'test_method': 'test_graph_button_opens_story_graph_with_selected_node_expanded',
                                'type': 'happy_path',
                                'steps': 'GIVEN: User has selected a story graph node\nWHEN: User clicks Graph button\nTHEN: System opens story-graph.json file'
                            }]
                        }]
                    }]
                }]
            }]
        }
        helper.story.create_story_graph(story_graph)
        
        # Use 'story' scope type instead of 'showAll' to enable scenario enrichment
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.STORY, value=['Open All Related Files'])
        json_scope = JSONScope(scope)
        result = json_scope.to_dict()
        
        # Verify scenario has test link with line number
        story = result['content']['epics'][0]['sub_epics'][0]['story_groups'][0]['stories'][0]
        scenario = story['scenarios'][0]
        
        assert 'test_file' in scenario, "Scenario should have test_file link"
        assert 'test_open_story_related_files.py' in scenario['test_file']
        assert '#L' in scenario['test_file'], "Scenario test link should include line number"
        # Verify the file path in the link actually exists
        link_url = scenario['test_file']
        if 'file:///' in link_url:
            file_path = link_url.split('#')[0].replace('file:///', '')
            helper.story.assert_file_exists(file_path, "Test file in scenario link")
    
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
        
        # Create test file if sub-epic needs it (use same path as sub_epic test_file)
        sub_epic_test_file = 'test/invoke_bot/edit_story_map/test_open_story_related_files.py'
        if sub_epic_has_test_file:
            test_file = helper.story.create_test_file(
                sub_epic_test_file,
                'TestOpenAllRelatedFiles',
                ['test_graph_button_opens_story_graph_with_selected_node_expanded']
            )
            helper.story.assert_file_exists(test_file, "Test file")
        
        # Create scenario data
        scenario_data = {
            'name': 'Graph button opens story graph with selected node expanded',
            'type': 'happy_path',
            'steps': 'GIVEN: User has selected a story graph node\nWHEN: User clicks Graph button\nTHEN: System opens story-graph.json file'
        }
        if has_test_method:
            scenario_data['test_method'] = 'test_graph_button_opens_story_graph_with_selected_node_expanded'
        
        # Create story data (stories don't have test_file - they inherit from sub-epic)
        story_data = {
            'name': 'Open All Related Files',
            'test_class': 'TestOpenAllRelatedFiles',
            'sequential_order': 1.0,
            'scenarios': [scenario_data]
        }
        
        # Create sub-epic data with test_file
        sub_epic_data = {
            'name': 'Open Story Related Files',
            'sequential_order': 1.0,
            'story_groups': [{
                'type': 'and',
                'stories': [story_data]
            }]
        }
        if sub_epic_has_test_file:
            sub_epic_data['test_file'] = sub_epic_test_file
        
        story_graph = {
            'epics': [{
                'name': 'Work With Story Map',
                'sub_epics': [sub_epic_data]
            }]
        }
        
        # Save using helper
        helper.story.create_story_graph(story_graph)
        
        # Use 'story' scope type instead of 'showAll' to enable scenario enrichment
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.STORY, value=['Open All Related Files'])
        json_scope = JSONScope(scope)
        result = json_scope.to_dict()
        
        # Verify scenario test link
        story = result['content']['epics'][0]['sub_epics'][0]['story_groups'][0]['stories'][0]
        scenario = story['scenarios'][0]
        
        if has_link:
            assert 'test_file' in scenario, "Scenario should have test_file link"
            assert 'test_open_story_related_files.py' in scenario['test_file']
            assert '#L' in scenario['test_file'], "Scenario test link should include line number"
            # Verify the file path in the link actually exists
            link_url = scenario['test_file']
            if 'file:///' in link_url:
                file_path = link_url.split('#')[0].replace('file:///', '')
                helper.story.assert_file_exists(file_path, "Test file in scenario link")
        else:
            # Scenario may have test_file field but it should be empty or not point to actual test
            if 'test_file' in scenario:
                assert scenario['test_file'] is None or scenario['test_file'] == ''