"""
Build Knowledge Tests

Tests for all stories in the 'Build Knowledge' sub-epic:
- Track Activity for Build Knowledge Action
- Proceed To Render Output
- Load Story Graph Into Memory
- Create Build Scope
- Filter Knowledge Graph
"""
import pytest
from pathlib import Path
import json
from agile_bot.bots.base_bot.src.actions.build.build_action import BuildKnowledgeAction
from agile_bot.bots.base_bot.src.scanners.story_map import (
    StoryMap, Epic, SubEpic, StoryGroup, Story, Scenario, ScenarioOutline
)
from agile_bot.bots.base_bot.test.test_helpers import (
    bootstrap_env,
    create_knowledge_graph_template,
    get_bot_dir,
    given_file_created,
    given_directory_created,
    then_config_path_matches,
    then_instructions_merged_from_sources,
    given_story_graph_dict,
    when_story_graph_copied,
    when_item_accessed,
    then_nodes_match,
    then_children_match,
    then_stories_match,
    then_scenarios_match,
    then_scenario_outlines_match,
    given_template_variables,
    then_file_updated,
    then_instructions_match,
    given_action_outputs,
    given_action_duration,
    given_action_config_copied,
    given_behavior_instructions,
    given_action_setup,
    when_instructions_extracted,
    when_data_extracted,
    when_action_executes
)
from agile_bot.bots.base_bot.test.test_execute_behavior_actions import (
    verify_action_tracks_start,
    verify_action_tracks_completion,
    verify_workflow_transition,
    verify_workflow_saves_completed_action
)
# Use fixtures from conftest.py (bot_directory, workspace_directory)

def _create_behavior(bot_directory: Path, bot_name: str, behavior_name: str, workspace_directory: Path = None):
    """Create a real Behavior object for testing."""
    from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
    from agile_bot.bots.base_bot.src.bot.behavior import Behavior
    from agile_bot.bots.base_bot.test.test_helpers import create_actions_workflow_json
    from agile_bot.bots.base_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files
    
    bot_paths = BotPaths(bot_directory=bot_directory)
    if workspace_directory:
        bot_paths._workspace_directory = workspace_directory
    
    create_actions_workflow_json(bot_directory, behavior_name)
    create_minimal_guardrails_files(bot_directory, behavior_name, bot_name)
    
    behavior = Behavior(name=behavior_name, bot_paths=bot_paths, bot_instance=None)
    
    return behavior



def given_test_bot_directory_created(repo_root_or_tmp_path, bot_name: str = 'test_story_bot'):
    """Given: Test bot directory created."""
    test_bot_dir = repo_root_or_tmp_path / 'agile_bot' / 'bots' / bot_name
    test_bot_dir.mkdir(parents=True, exist_ok=True)
    return test_bot_dir

# Exception handling helpers removed

def given_build_outputs():
    """Given: Build knowledge action outputs."""
    return {'knowledge_items_count': 12, 'file_path': 'knowledge.json'}

def given_build_duration():
    """Given: Build knowledge action duration."""
    return 420

def given_base_and_behavior_instructions_setup(bot_directory, workspace_directory, bot_name, behavior, action):
    """Given: Base and behavior-specific instructions setup."""
    bootstrap_env(bot_directory, workspace_directory)
    given_base_instructions_copied_to_bot_directory(bot_directory, action)
    kg_dir = given_setup('directory_structure', bot_directory, behavior=behavior)
    given_behavior_specific_instructions_created(bot_directory, behavior, action, kg_dir)
    given_setup('config_and_template', bot_directory, kg_dir=kg_dir)
    # Create guardrails files (required for behavior loading)
    from agile_bot.bots.base_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files
    create_minimal_guardrails_files(bot_directory, behavior, bot_name)
    # Create behavior.json with actions_workflow that includes behavior instructions
    from agile_bot.bots.base_bot.test.test_helpers import create_actions_workflow_json
    create_actions_workflow_json(bot_directory, behavior, actions=[
        {
            "name": action,
            "order": 1,
            "next_action": "validate",
            "instructions": [f'{behavior}.{action} specific instructions']
        }
    ])
    return kg_dir

def given_base_instructions_only_setup(bot_directory, workspace_directory, bot_dir, behavior, action):
    """Given: Base instructions only setup (no behavior-specific instructions)."""
    bootstrap_env(bot_directory, workspace_directory)
    given_base_instructions_copied_to_bot_directory(bot_dir, action)
    kg_dir = given_setup('directory_structure', bot_dir, behavior=behavior)
    given_setup('config_and_template', bot_directory, kg_dir=kg_dir)
    from agile_bot.bots.base_bot.test.test_helpers import create_actions_workflow_json
    create_actions_workflow_json(bot_dir, behavior, actions=[
        {
            "name": action,
            "order": 1,
            "next_action": "validate"
        }
    ])
    return kg_dir

def given_base_instructions_text_extracted(instructions):
    """Given: Base instructions text extracted from instructions dict."""
    return '\n'.join(instructions.get('base_instructions', []))

def when_story_map_created(bot=None, test_instance=None, bot_directory=None):
    """
    Consolidated function for creating story map.
    Replaces: when_story_map_created_from_bot, when_story_map_created_from_mock_bot
    
    Args:
        bot: Bot instance (if provided, use directly)
        test_instance: Test instance (if bot not provided, use to create mock bot)
        bot_directory: Bot directory (if bot not provided, use with test_instance)
    """
    if bot is None:
        if test_instance is None or bot_directory is None:
            raise ValueError("Either bot must be provided, or both test_instance and bot_directory")
        bot = test_instance._create_mock_bot(bot_directory)
    return StoryMap.from_bot(bot)

# Exception handling helper removed

@pytest.fixture
def simple_story_graph():
    return {
        "epics": [
            {
                "name": "Build Knowledge",
                "sequential_order": 1,
                "sub_epics": [
                    {
                        "name": "Load Story Graph",
                        "sequential_order": 1,
                        "sub_epics": [],
                        "story_groups": [
                            {
                                "type": "and",
                                "connector": None,
                                "stories": [
                                    {
                                        "name": "Load Story Graph Into Memory",
                                        "sequential_order": 1,
                                        "connector": None,
                                        "users": ["Story Bot"],
                                        "story_type": "user",
                                        "sizing": "5 days",
                                        "scenarios": [
                                            {
                                                "name": "Story graph file exists",
                                                "type": "happy_path",
                                                "background": ["Given story graph file exists"],
                                                "steps": [
                                                    "When story graph is loaded",
                                                    "Then story map is created with epics"
                                                ]
                                            },
                                            {
                                                "name": "Story graph file missing",
                                                "type": "error_case",
                                                "background": [],
                                                "steps": [
                                                    "When story graph file does not exist",
                                                    "Then FileNotFoundError is raised"
                                                ]
                                            }
                                        ],
                                        "scenario_outlines": [
                                            {
                                                "name": "Load story graph with different formats",
                                                "type": "happy_path",
                                                "background": ["Given story graph file exists"],
                                                "steps": [
                                                    "When story graph is loaded from \"<file_path>\"",
                                                    "Then story map contains \"<expected_epics>\" epics"
                                                ],
                                                "examples": {
                                                    "columns": ["file_path", "expected_epics"],
                                                    "rows": [
                                                        ["story-graph.json", "2"],
                                                        ["story-graph-v2.json", "3"]
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "story_groups": []
            }
        ]
    }


@pytest.fixture
def story_map(simple_story_graph):
    return StoryMap(simple_story_graph)


# ============================================================================
# STORY: Track Activity for Build Knowledge Action
# ============================================================================

class TestTrackActivityForBuildKnowledgeAction:
    """Story: Track Activity for Build Knowledge Action - Tests activity tracking for build."""

    def test_track_activity_when_build_action_starts(self, bot_directory, workspace_directory):
        # Given: Bot directory and workspace directory are set up
        # When: Build knowledge action starts
        # Then: Activity is tracked (verified by verify_action_tracks_start)
        verify_action_tracks_start(bot_directory, workspace_directory, BuildKnowledgeAction, 'build')

    def test_track_activity_when_build_action_completes(self, bot_directory, workspace_directory):
        # Given: Build knowledge outputs and duration
        outputs = given_build_outputs()
        duration = given_build_duration()
        # When: Build knowledge action completes
        # Then: Activity is tracked with outputs and duration (verified by verify_action_tracks_completion)
        verify_action_tracks_completion(bot_directory, workspace_directory, BuildKnowledgeAction, 'build', outputs=outputs, duration=duration)


# ============================================================================
# STORY: Proceed To Render Output
# ============================================================================

class TestProceedToRenderOutput:
    """Story: Proceed To Render Output - Tests transition to render_output action."""

    def test_seamless_transition_from_build_to_validate(self, bot_directory, workspace_directory):
        """
        SCENARIO: Seamless Transition From Build Knowledge To Validate Rules
        """
        # Given: Bot directory and workspace directory are set up
        # When: Build knowledge action completes
        # Then: Workflow transitions to validate (verified by verify_workflow_transition)
        verify_workflow_transition(bot_directory, workspace_directory, 'build', 'validate')

    def test_workflow_state_captures_build_completion(self, bot_directory, workspace_directory):
        """
        SCENARIO: Workflow State Captures Build Knowledge Completion
        """
        # Given: Bot directory and workspace directory are set up
        # When: Build knowledge action completes
        # Then: Workflow state captures completion (verified by verify_workflow_saves_completed_action)
        verify_workflow_saves_completed_action(bot_directory, workspace_directory, 'build')

def given_setup(setup_type, bot_directory, **setup_params):
    """
    Consolidated function for BUILD KNOWLEDGE setup.
    Replaces: given_knowledge_graph_setup, given_knowledge_graph_setup_complete,
    given_knowledge_graph_config_and_template_created, given_knowledge_graph_directory_structure_created,
    given_knowledge_graph_directory_for_prioritization, given_environment_and_knowledge_graph_setup
    
    Args:
        setup_type: Type of setup ('knowledge_graph', 'knowledge_graph_complete', 'config_and_template',
                    'directory_structure', 'directory_for_prioritization', 'environment_and_kg')
        bot_directory: Bot directory path
        **setup_params: Additional parameters (behavior, template_name, workspace_directory, kg_dir)
    
    Returns:
        kg_dir Path or tuple depending on setup_type
    """
    behavior = setup_params.get('behavior', 'build')
    workspace_directory = setup_params.get('workspace_directory')
    template_name = setup_params.get('template_name', 'story-graph-outline.json')
    kg_dir = setup_params.get('kg_dir')
    
    # Create kg_dir if not provided
    if kg_dir is None:
        behavior_dir = bot_directory / 'behaviors' / behavior
        kg_dir = behavior_dir / 'content' / 'knowledge_graph'
        kg_dir.mkdir(parents=True, exist_ok=True)
    
    if setup_type == 'knowledge_graph' or setup_type == 'directory_structure':
        return kg_dir
    elif setup_type == 'knowledge_graph_complete':
        given_file_created(kg_dir, 'build_story_graph_outline.json', {'template': template_name})
        given_file_created(kg_dir, template_name, {'template': 'knowledge_graph', 'structure': {}})
        return kg_dir
    elif setup_type == 'config_and_template':
        config_file = kg_dir / 'build_story_graph_outline.json'
        config_file.write_text(
            json.dumps({
                'name': 'build_story_graph_outline',
                'path': 'docs/stories/',
                'template': 'story-graph-outline.json',
                'output': 'story-graph.json'
            }),
            encoding='utf-8'
        )
        template_file = kg_dir / 'story-graph-outline.json'
        template_file.write_text(
            json.dumps({
                '_explanation': {},
                'epics': []
            }),
            encoding='utf-8'
        )
        return config_file, template_file
    elif setup_type == 'directory_for_prioritization':
        return kg_dir
    elif setup_type == 'environment_and_kg':
        if workspace_directory:
            bootstrap_env(bot_directory, workspace_directory)
        return kg_dir
    else:
        raise ValueError(f"Unknown setup_type: {setup_type}")


# Backward-compatible aliases for consolidated functions
def given_knowledge_graph_directory_structure_created(bot_directory, behavior='build'):
    """Alias for given_setup('directory_structure', ...) - backward compatibility."""
    return given_setup('directory_structure', bot_directory, behavior=behavior)


def given_knowledge_graph_config_and_template_created(kg_dir):
    """Alias for given_setup('config_and_template', ...) - backward compatibility."""
    # This one needs the bot_directory, so we work backward from kg_dir
    # kg_dir is typically: bot_directory/behaviors/behavior/content/knowledge_graph
    bot_directory = kg_dir.parent.parent.parent.parent
    return given_setup('config_and_template', bot_directory, kg_dir=kg_dir)


# Use test_helpers.given_file_created instead
# Original patterns:
# - Given: Knowledge graph config file created
# - Given: Knowledge graph template file created








# Exception handling helpers removed


def given_base_instructions_copied_to_bot_directory(bot_directory: Path, action_name: str) -> Path:
    """Given: Base instructions copied to bot directory."""
    from agile_bot.bots.base_bot.test.test_helpers import get_base_actions_dir, get_test_base_actions_dir
    from agile_bot.bots.base_bot.src.bot.workspace import get_base_actions_directory
    import shutil
    import json
    repo_root = Path(__file__).parent.parent.parent.parent.parent
    actual_base_actions_dir = get_base_actions_dir(repo_root)
    actual_instructions_file = actual_base_actions_dir / action_name / 'action_config.json'
    
    # BaseActionConfig expects action_config.json in base_actions directory
    bot_base_actions_dir = get_base_actions_directory(bot_directory=bot_directory) / action_name
    bot_base_actions_dir.mkdir(parents=True, exist_ok=True)
    bot_instructions_file = bot_base_actions_dir / 'action_config.json'
    
    # Read source file and write to destination to avoid Windows file locking issues
    content = actual_instructions_file.read_text(encoding='utf-8')
    bot_instructions_file.write_text(content, encoding='utf-8')
    return bot_instructions_file


def given_behavior_specific_instructions_created(bot_directory: Path, behavior: str, action: str, kg_dir: Path) -> Path:
    """Given: Behavior-specific instructions created."""
    behavior_instructions_file = kg_dir / 'instructions.json'
    behavior_instructions_file.write_text(
        json.dumps({
            'behaviorName': behavior,
            'instructions': [f'{behavior}.{action} specific instructions']
        }),
        encoding='utf-8'
    )
    return behavior_instructions_file






def then_base_instructions_present(merged_instructions: dict):
    """Then: Base instructions present."""
    base_instructions_list = merged_instructions['base_instructions']
    assert isinstance(base_instructions_list, list)
    assert len(base_instructions_list) > 0
    base_instructions_text = ' '.join(base_instructions_list).lower()
    assert 'build knowledge graph' in base_instructions_text or 'knowledge graph' in base_instructions_text


def then_behavior_instructions_present(merged_instructions: dict):
    """Then: Behavior instructions present."""
    behavior_instructions_list = merged_instructions['behavior_instructions']
    assert isinstance(behavior_instructions_list, list)
    assert len(behavior_instructions_list) > 0


def then_behavior_instructions_contain_action(merged_instructions: dict, behavior: str, action: str):
    """Then: Behavior instructions contain action."""
    behavior_instructions_list = merged_instructions['behavior_instructions']
    instructions_text = ' '.join(behavior_instructions_list).lower()
    # Check that action is referenced in instructions (may or may not have behavior prefix)
    assert action in instructions_text, f"Behavior instructions should reference action '{action}'"








def then_nodes_match_expected_structure(nodes):
    """Then: Nodes match expected structure."""
    assert len(nodes) == 4
    assert isinstance(nodes[0], Epic)
    assert nodes[0].name == "Build Knowledge"
    assert isinstance(nodes[1], SubEpic)
    assert nodes[1].name == "Load Story Graph"
    assert isinstance(nodes[2], StoryGroup)
    assert isinstance(nodes[3], Story)
    assert nodes[3].name == "Load Story Graph Into Memory"


def then_location_matches(item, type=None, field=None):
    """
    Consolidated function for checking map location correctness.
    Replaces: then_epic_map_location_correct, then_sub_epic_map_location_correct,
    then_story_map_location_correct, then_scenario_map_location_correct,
    then_scenario_outline_map_location_correct
    
    Args:
        item: Epic, SubEpic, Story, Scenario, or ScenarioOutline instance
        type: Type hint ('epic', 'sub_epic', 'story', 'scenario', 'scenario_outline') - auto-detected if None
        field: Optional field name to check (e.g., 'sequential_order', 'sizing')
    """
    # Auto-detect type if not provided
    if type is None:
        from agile_bot.bots.base_bot.src.scanners.story_map import Epic, SubEpic, Story, Scenario, ScenarioOutline
        if isinstance(item, Epic):
            type = 'epic'
        elif isinstance(item, SubEpic):
            type = 'sub_epic'
        elif isinstance(item, Story):
            type = 'story'
        elif isinstance(item, Scenario):
            type = 'scenario'
        elif isinstance(item, ScenarioOutline):
            type = 'scenario_outline'
    
    # Expected locations based on type
    expected_locations = {
        'epic': {
            None: "epics[0].name",
            'sequential_order': "epics[0].sequential_order"
        },
        'sub_epic': {
            None: "epics[0].sub_epics[0].name"
        },
        'story': {
            None: "epics[0].sub_epics[0].story_groups[0].stories[0].name",
            'sizing': "epics[0].sub_epics[0].story_groups[0].stories[0].sizing"
        },
        'scenario': {
            None: "epics[0].sub_epics[0].story_groups[0].stories[0].scenarios[0].name"
        },
        'scenario_outline': {
            None: "epics[0].sub_epics[0].story_groups[0].stories[0].scenario_outlines[0].name"
        }
    }
    
    # Check default location (name)
    expected_default = expected_locations.get(type, {}).get(None)
    assert item.map_location() == expected_default
    
    # Check additional fields if applicable
    if type == 'epic':
        # Epic also checks sequential_order
        expected_seq = expected_locations.get(type, {}).get('sequential_order')
        assert item.map_location('sequential_order') == expected_seq
    elif type == 'story' and field == 'sizing':
        # Story can check sizing if requested
        expected_sizing = expected_locations.get(type, {}).get('sizing')
        assert item.map_location('sizing') == expected_sizing









def then_story_map_matches(story_map, epic=None):
    """
    Consolidated function for checking story map matches expected epic.
    Replaces: then_story_map_contains_test_epic, then_epics_contain_single_build_epic, then_epics_match
    
    Args:
        story_map: StoryMap instance or epics list
        epic: Epic name to check for. None = check for single epic (defaults to "Test Epic" for story_map, "Build Knowledge" for epics list)
    
    Returns:
        The epic if checking epics list, None otherwise
    """
    # Handle both story_map and epics list
    if isinstance(story_map, list):
        # It's an epics list
        epics = story_map
        assert len(epics) == 1
        assert isinstance(epics[0], Epic)
        expected_name = epic if epic is not None else "Build Knowledge"
        assert epics[0].name == expected_name
        return epics[0]
    else:
        # It's a story_map
        epics_list = story_map.epics()
        assert len(epics_list) == 1
        expected_name = epic if epic is not None else "Test Epic"
        assert epics_list[0].name == expected_name










# given_knowledge_graph_template_for_increments_created - use test_helpers.given_file_created instead
# Original patterns:
# - Given: Existing story graph created
# - Given: Knowledge graph config for increments created
# - Given: Knowledge graph template for increments created




def then_instructions_indicate_updating_existing_file(instructions: dict, expected_output: str):
    """Then: Instructions indicate updating existing file."""
    assert 'knowledge_graph_config' in instructions
    assert instructions['knowledge_graph_config']['output'] == expected_output
    assert 'template_path' in instructions


def given_test_variables_for_exploration() -> tuple[str, str]:
    """Given: Test variables for exploration behavior."""
    bot_name = 'story_bot'
    behavior = 'exploration'
    return bot_name, behavior


def given_test_variables_for_shape_build() -> tuple[str, str, str]:
    """Given: Test variables for shape build."""
    bot_name = 'test_bot'
    behavior = 'shape'
    action = 'build'
    return bot_name, behavior, action






def given_template_variables_test_setup(bot_directory: Path, workspace_directory: Path) -> tuple:
    """Given: Complete setup for template variables test.
    
    Sets up all prerequisites for testing template variable replacement:
    - Test variables (bot_name, behavior, action)
    - Environment bootstrap
    - Base instructions
    - Knowledge graph directory structure
    - Behavior-specific instructions
    - Behavior main instructions
    - Knowledge graph config and template
    - Knowledge graph template with schema
    - Validation rules
    
    
    """
    bot_name, behavior, action = given_test_variables_for_shape_build()
    bootstrap_env(bot_directory, workspace_directory)
    
    given_base_instructions_copied_to_bot_directory(bot_directory, action)
    kg_dir = given_setup('directory_structure', bot_directory, behavior=behavior)
    given_behavior_specific_instructions_created(bot_directory, behavior, action, kg_dir)
    from agile_bot.bots.base_bot.test.test_invoke_bot_directly import given_behavior_config
    # Create instructions.json via behavior config
    behavior_dir = bot_directory / 'behaviors' / behavior
    instructions_file = behavior_dir / 'instructions.json'
    instructions_file.write_text(
        json.dumps({
            'description': 'Shape the story map',
            'goal': 'Create initial story structure'
        }),
        encoding='utf-8'
    )
    given_setup('config_and_template', bot_directory, kg_dir=kg_dir)
    given_file_created(kg_dir, 'story-graph-outline.json', {
        '_explanation': {
            'epics': 'Top-level epics',
            'sub_epics': 'Sub-epic breakdowns'
        },
        'epics': []
    })
    from agile_bot.bots.base_bot.test.test_validate_knowledge_and_content_against_rules import given_rule_file_created
    given_rule_file_created(bot_directory, None, 'verb-noun-format', None, rule_type='verb_noun_format')
    
    return bot_name, behavior, action, kg_dir


def given_test_variables_for_prioritization() -> tuple[str, str]:
    """Given: Test variables for prioritization behavior."""
    bot_name = 'story_bot'
    behavior = 'prioritization'
    return bot_name, behavior






# Use test_helpers.given_file_created instead
# Original patterns:
# - Given: Knowledge graph config for story graph increments
# - Given: Knowledge graph template for increments


def then_story_graph_updated_with_increments(instructions: dict, story_graph_path: Path):
    """Then: Story graph updated with increments."""
    assert story_graph_path.exists()
    config = instructions['knowledge_graph_config']
    assert config['output'] == 'story-graph.json'
    assert 'template_path' in instructions






def when_epic_children_retrieved(parent, return_both=False):
    """
    Consolidated function for retrieving children from epic/sub-epic/story-group.
    Replaces: when_sub_epic_and_story_group_retrieved, when_epic_children_retrieved,
    when_sub_epic_children_retrieved, when_story_group_stories_retrieved
    
    Args:
        parent: Epic, SubEpic, or StoryGroup instance
        return_both: If True and parent is Epic, returns (sub_epic, story_group) tuple
    
    Returns:
        List of children, or (sub_epic, story_group) tuple if return_both=True
    """
    if return_both and hasattr(parent, 'children') and len(parent.children) > 0:
        # Special case: return both sub_epic and story_group
        sub_epic = parent.children[0]
        if hasattr(sub_epic, 'children') and len(sub_epic.children) > 0:
            story_group = sub_epic.children[0]
            return sub_epic, story_group
    return parent.children


def then_children_contain_single_sub_epic(children, expected_name: str = "Load Story Graph"):
    """Then: Children contain single sub epic."""
    assert len(children) == 1
    assert isinstance(children[0], SubEpic)
    assert children[0].name == expected_name
    return children[0]


def then_children_contain_single_story_group(children):
    """Then: Children contain single story group."""
    assert len(children) == 1
    assert isinstance(children[0], StoryGroup)
    return children[0]


def then_stories_contain_single_story(stories, expected_name: str = "Load Story Graph Into Memory"):
    """Then: Stories contain single story."""
    assert len(stories) == 1
    assert isinstance(stories[0], Story)
    assert stories[0].name == expected_name
    return stories[0]




def then_story_has_expected_properties(story):
    """Then: Story has expected properties."""
    assert story.name == "Load Story Graph Into Memory"
    assert story.users == ["Story Bot"]
    assert story.story_type == "user"
    assert story.sizing == "5 days"
    assert story.sequential_order == 1
    assert story.connector is None


def when_story_scenarios_retrieved(story):
    """When: Story scenarios retrieved."""
    return story.scenarios


def then_scenarios_contain_expected_scenarios(scenarios):
    """Then: Scenarios contain expected scenarios."""
    assert len(scenarios) == 2
    assert isinstance(scenarios[0], Scenario)
    assert scenarios[0].name == "Story graph file exists"
    assert scenarios[0].type == "happy_path"
    assert scenarios[1].name == "Story graph file missing"
    assert scenarios[1].type == "error_case"




def then_scenario_has_expected_properties(scenario):
    """Then: Scenario has expected properties."""
    assert scenario.name == "Story graph file exists"
    assert scenario.type == "happy_path"
    assert len(scenario.background) == 1
    assert scenario.background[0] == "Given story graph file exists"
    assert len(scenario.steps) == 2
    assert scenario.steps[0] == "When story graph is loaded"
    assert scenario.steps[1] == "Then story map is created with epics"


def when_story_scenario_outlines_retrieved(story):
    """When: Story scenario outlines retrieved."""
    return story.scenario_outlines


def then_scenario_outlines_contain_expected_outline(scenario_outlines):
    """Then: Scenario outlines contain expected outline."""
    assert len(scenario_outlines) == 1
    assert isinstance(scenario_outlines[0], ScenarioOutline)
    assert scenario_outlines[0].name == "Load story graph with different formats"




def then_scenario_outline_has_expected_examples(scenario_outline):
    """Then: Scenario outline has expected examples."""
    assert len(scenario_outline.examples_columns) == 2
    assert scenario_outline.examples_columns == ["file_path", "expected_epics"]
    assert len(scenario_outline.examples_rows) == 2
    assert scenario_outline.examples_rows[0] == ["story-graph.json", "2"]
    assert scenario_outline.examples_rows[1] == ["story-graph-v2.json", "3"]


# ============================================================================
# HELPER FUNCTIONS - Build Scope (Story: Create Build Scope)
# ============================================================================

def when_build_scope_instantiated(parameters: dict, bot_paths=None):
    """When: BuildScope instantiated with parameters."""
    from agile_bot.bots.base_bot.src.actions.build.build_scope import BuildScope
    return BuildScope(parameters, bot_paths)


def then_build_scope_contains(build_scope, expected_key: str, expected_value):
    """Then: BuildScope contains expected key-value."""
    assert expected_key in build_scope.scope
    assert build_scope.scope[expected_key] == expected_value


def then_build_scope_contains_all_expected(build_scope, expected_scope_contains: dict):
    """Then: BuildScope contains all expected key-value pairs."""
    for key, value in expected_scope_contains.items():
        then_build_scope_contains(build_scope, key, value)


def then_action_uses_build_scope_class(action: BuildKnowledgeAction, parameters: dict):
    """Then: Action uses BuildScope class (converts dict to typed context)."""
    from agile_bot.bots.base_bot.src.actions.action_context import ScopeActionContext, Scope, ScopeType
    
    # Convert dict parameters to typed context
    scope = None
    if 'scope' in parameters and parameters['scope']:
        scope_dict = parameters['scope']
        if isinstance(scope_dict, dict):
            scope_type = ScopeType(scope_dict.get('type', 'all'))
            scope = Scope(
                type=scope_type,
                value=scope_dict.get('value', []),
                exclude=scope_dict.get('exclude', [])
            )
    context = ScopeActionContext(scope=scope)
    
    # Verify action uses BuildScope by checking if scope is in instructions
    result = action.do_execute(context)
    assert 'instructions' in result
    assert 'scope' in result['instructions']
    scope_config = result['instructions']['scope']
    assert isinstance(scope_config, dict)


def given_build_parameters_with_scope(scope_type='all', scope_value=None):
    """Given: Build parameters with scope."""
    if scope_type == 'all':
        return {'scope': {'type': 'all'}}
    return {'scope': {'type': scope_type, 'value': scope_value}}


def given_build_parameters_with_story_names(story_names):
    """Given: Build parameters with story names."""
    if isinstance(story_names, str):
        story_names = [story_names]
    return {'story_names': story_names}


def given_build_parameters_with_increment_priorities(priorities):
    """Given: Build parameters with increment priorities."""
    if isinstance(priorities, int):
        priorities = [priorities]
    return {'increment_priorities': priorities}


def given_build_parameters_with_epic_names(epic_names):
    """Given: Build parameters with epic names."""
    if isinstance(epic_names, str):
        epic_names = [epic_names]
    return {'epic_names': epic_names}


# ============================================================================
# STORY: Inject Knowledge Graph Template for Build Knowledge
# ============================================================================

class TestInjectKnowledgeGraphTemplateForBuildKnowledge:
    """Story: Inject Knowledge Graph Template for Build Knowledge - Tests template injection."""

    def test_action_injects_knowledge_graph_template(self, bot_directory, workspace_directory):
        """
        SCENARIO: Action Injects Knowledge Graph Template
        """
        bot_name, behavior = given_test_variables_for_exploration()
        template_name = 'story-graph-explored-outline.json'
        
        kg_dir = given_setup('environment_and_kg', bot_directory, workspace_directory=workspace_directory, behavior=behavior)
        given_file_created(kg_dir, 'build_story_graph_outline.json', {'template': template_name})
        given_file_created(kg_dir, template_name, {'template': 'knowledge_graph', 'structure': {}})
        
        # Create guardrails files (required for strategy data injection)
        from agile_bot.bots.base_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files
        create_minimal_guardrails_files(bot_directory, behavior, bot_name)
        
        action_obj, instructions = when_action_executes('build', bot_directory, behavior, bot_name=bot_name, return_action=True)
        
        from agile_bot.bots.base_bot.test.test_helpers import then_instructions_contain
        then_instructions_contain(instructions, 'template_path', template_name=template_name)

    def test_action_loads_and_merges_instructions(self, bot_directory, workspace_directory):
        """
        SCENARIO: Action Loads And Merges Instructions
        GIVEN: Base and behavior-specific instructions exist
        WHEN: Action method is invoked
        THEN: Instructions are loaded from both locations and merged
        """
        bot_name, behavior, action = given_test_variables_for_shape_build()
        given_base_and_behavior_instructions_setup(bot_directory, workspace_directory, bot_name, behavior, action)
        
        action_obj, merged_instructions = when_action_executes('build', bot_directory, behavior, bot_name=bot_name, return_action=True, execute=False)
        
        then_instructions_merged_from_sources(merged_instructions, behavior, action, sources='both')
        then_base_instructions_present(merged_instructions)
        then_behavior_instructions_present(merged_instructions)
        then_behavior_instructions_contain_action(merged_instructions, behavior, action)

    def test_all_template_variables_are_replaced_in_instructions(self, bot_directory, workspace_directory):
        """
        SCENARIO: All Template Variables Are Replaced In Instructions
        GIVEN: Base instructions with {{rules}}, {{schema}}, {{description}}, {{instructions}} placeholders
        WHEN: Action loads and merges instructions with all injections
        THEN: All template variables are replaced with actual content
        """
        bot_name, behavior, action, kg_dir = given_template_variables_test_setup(bot_directory, workspace_directory)
        
        # Create a mock behavior object for the action
        behavior_obj = _create_behavior(bot_directory, bot_name, behavior)
        # Use new signature: action_name, behavior, action_config
        action_obj = BuildKnowledgeAction(behavior=behavior_obj, action_config=None)
        instructions = when_action_executes('build', bot_directory, behavior, action_obj=action_obj)
        
        base_instructions_text = given_base_instructions_text_extracted(instructions)
        from agile_bot.bots.base_bot.test.test_helpers import then_template_variables_replaced
        then_template_variables_replaced(base_instructions_text)


# ============================================================================
# STORY: Update Existing Knowledge Graph
# ============================================================================

class TestUpdateExistingKnowledgeGraph:
    """Story: Update Existing Knowledge Graph - Tests that build updates existing story-graph.json instead of creating a new file."""

    def test_behavior_updates_existing_story_graph_json(self, bot_directory, workspace_directory):
        """
        Test that prioritization behavior updates existing story-graph.json by adding increments array,
        rather than creating a separate story-graph-increments.json file.
        """
        bot_name, behavior = given_test_variables_for_prioritization()
        bootstrap_env(bot_directory, workspace_directory)
        
        existing_story_graph = given_story_graph_dict(epic='mob')
        stories_dir = workspace_directory / 'docs' / 'stories'
        story_graph_path = given_file_created(stories_dir, 'story-graph.json', existing_story_graph)
        
        kg_dir = given_setup('directory_for_prioritization', bot_directory, behavior=behavior)
        given_file_created(kg_dir, 'build_story_graph_increments.json', {
            "name": "build_story_graph_outline",
            "path": "docs/stories",
            "template": "story_graph_increments.json",
            "output": "story-graph.json"
        })
        given_file_created(kg_dir, 'story_graph_increments.json', {
            "_explanation": {},
            "epics": [],
            "increments": []
        })
        
        action_obj, instructions = when_action_executes('build', bot_directory, behavior, bot_name=bot_name, return_action=True, template_type='increments')
        
        then_instructions_indicate_updating_existing_file(instructions, 'story-graph.json')
        then_story_graph_updated_with_increments(instructions, story_graph_path)
        then_config_path_matches(instructions, 'docs/stories')


# ============================================================================
# STORY: Load Story Graph Into Memory
# ============================================================================

class TestLoadStoryGraphIntoMemory:
    """Story: Load Story Graph Into Memory - Tests loading story graph and creating StoryMap object model."""
    
    @staticmethod
    def _create_mock_bot(bot_directory: Path):
        """Helper: Create MockBot instance for testing StoryMap.from_bot().
        
        Used by: test_from_bot_loads_story_graph, test_from_bot_raises_when_file_not_found
        """
        class MockBot:
            def __init__(self, bot_directory):
                self.bot_directory = bot_directory
        
        return MockBot(bot_directory)
    
    def test_story_map_loads_epics(self, story_map):
        """
        SCENARIO: Story Map Loads Epics
        """
        # Given: Story map is loaded
        # When: Epics are retrieved from story map
        epics = when_item_accessed('epics', story_map)
        # Then: Epics contain single build knowledge epic
        then_story_map_matches(epics)
    
    def test_epic_has_sub_epics(self, story_map):
        """
        SCENARIO: Epic Has Sub Epics
        """
        # Given: Story map is loaded
        epics = when_item_accessed('epics', story_map)
        epic = then_story_map_matches(epics)
        # When: Epic children are retrieved
        children = when_epic_children_retrieved(epic)
        # Then: Children contain single sub epic
        then_children_contain_single_sub_epic(children)
    
    def test_sub_epic_has_story_groups(self, story_map):
        """
        SCENARIO: Sub Epic Has Story Groups
        """
        # Given: Story map is loaded
        epics = when_item_accessed('epics', story_map)
        epic = then_story_map_matches(epics)
        sub_epic = epic.children[0]
        # When: Sub epic children are retrieved
        children = when_epic_children_retrieved(sub_epic)
        # Then: Children contain single story group
        then_children_contain_single_story_group(children)
    
    def test_story_group_has_stories(self, story_map):
        """
        SCENARIO: Story Group Has Stories
        """
        # Given: Story map is loaded
        epics = when_item_accessed('epics', story_map)
        epic = then_story_map_matches(epics)
        sub_epic, story_group = when_epic_children_retrieved(epic, return_both=True)
        # When: Story group stories are retrieved
        stories = when_epic_children_retrieved(story_group)
        # Then: Stories contain single story
        then_stories_contain_single_story(stories)
    
    def test_story_has_properties(self, story_map):
        """
        SCENARIO: Story Has Properties
        """
        # Given: Story map is loaded
        # When: Story is retrieved from path
        story = when_item_accessed('story', story_map)
        # Then: Story has expected properties
        then_story_has_expected_properties(story)
    
    def test_story_has_scenarios(self, story_map):
        """
        SCENARIO: Story Has Scenarios
        """
        # Given: Story map is loaded
        story = when_item_accessed('story', story_map)
        # When: Story scenarios are retrieved
        scenarios = when_story_scenarios_retrieved(story)
        # Then: Scenarios contain expected scenarios
        then_scenarios_contain_expected_scenarios(scenarios)
    
    def test_scenario_has_properties(self, story_map):
        """
        SCENARIO: Scenario Has Properties
        """
        # Given: Story map is loaded
        story = when_item_accessed('story', story_map)
        # When: Scenario is retrieved from story
        scenario = when_item_accessed('scenario', story)
        # Then: Scenario has expected properties
        then_scenario_has_expected_properties(scenario)
    
    def test_scenario_default_test_method(self, story_map):
        """
        SCENARIO: Scenario Default Test Method
        """
        # Given: Story map is loaded
        story = when_item_accessed('story', story_map)
        # When: Scenario is retrieved from story
        scenario = when_item_accessed('scenario', story)
        # Then: Scenario has default test method
        assert scenario.default_test_method == "test_story_graph_file_exists"
    
    def test_story_has_scenario_outlines(self, story_map):
        """
        SCENARIO: Story Has Scenario Outlines
        """
        # Given: Story map is loaded
        story = when_item_accessed('story', story_map)
        # When: Story scenario outlines are retrieved
        scenario_outlines = when_story_scenario_outlines_retrieved(story)
        # Then: Scenario outlines contain expected outline
        then_scenario_outlines_contain_expected_outline(scenario_outlines)
    
    def test_scenario_outline_has_examples(self, story_map):
        """
        SCENARIO: Scenario Outline Has Examples
        """
        # Given: Story map is loaded
        story = when_item_accessed('story', story_map)
        # When: Scenario outline is retrieved from story
        scenario_outline = when_item_accessed('scenario_outline', story)
        # Then: Scenario outline has expected examples
        then_scenario_outline_has_expected_examples(scenario_outline)
    
    def test_story_default_test_class(self, story_map):
        """
        SCENARIO: Story Default Test Class
        """
        # Given: Story map is loaded
        # When: Story is retrieved from path
        story = when_item_accessed('story', story_map)
        # Then: Story has default test class
        assert story.default_test_class == "TestLoadStoryGraphIntoMemory"
    
    def test_story_map_walk_traverses_all_nodes(self, story_map):
        """
        SCENARIO: Story Map Walk Traverses All Nodes
        """
        # Given: Story map is loaded
        epics = when_item_accessed('epics', story_map)
        epic = when_item_accessed('epic', epics)
        # When: Story map is walked
        nodes = when_data_extracted(story_map, 'walk', epic=epic)
        # Then: Nodes match expected structure
        then_nodes_match_expected_structure(nodes)
    
    def test_map_location_for_epic(self, story_map):
        """
        SCENARIO: Map Location For Epic
        """
        # Given: Story map is loaded
        epics = when_item_accessed('epics', story_map)
        # When: First epic is retrieved
        epic = when_item_accessed('epic', epics)
        # Then: Epic map location is correct
        then_location_matches(epic)
    
    def test_map_location_for_sub_epic(self, story_map):
        """
        SCENARIO: Map Location For Sub Epic
        """
        # Given: Story map is loaded
        epics = when_item_accessed('epics', story_map)
        # When: Sub epic is retrieved from epics
        sub_epic = when_item_accessed('sub_epic', epics)
        # Then: Sub epic map location is correct
        then_location_matches(sub_epic)
    
    def test_map_location_for_story(self, story_map):
        """
        SCENARIO: Map Location For Story
        """
        # Given: Story map is loaded
        epics = when_item_accessed('epics', story_map)
        # When: Story is retrieved from epics
        story = when_item_accessed('story', epics)
        # Then: Story map location is correct
        then_location_matches(story)
    
    def test_scenario_map_location(self, story_map):
        """
        SCENARIO: Scenario Map Location
        """
        # Given: Story map is loaded
        epics = when_item_accessed('epics', story_map)
        # When: Scenario is retrieved from epics
        scenario = when_item_accessed('scenario', epics)
        # Then: Scenario map location is correct
        then_location_matches(scenario)
    
    def test_scenario_outline_map_location(self, story_map):
        """
        SCENARIO: Scenario Outline Map Location
        """
        # Given: Story map is loaded
        epics = when_item_accessed('epics', story_map)
        # When: Scenario outline is retrieved from epics
        scenario_outline = when_item_accessed('scenario_outline', epics)
        # Then: Scenario outline map location is correct
        then_location_matches(scenario_outline)
    
    def test_from_bot_loads_story_graph(self, tmp_path):
        """
        SCENARIO: From Bot Loads Story Graph
        """
        bot_directory = given_test_bot_directory_created(tmp_path)
        docs_dir = given_directory_created(bot_directory, directory_type='docs')
        story_graph = given_story_graph_dict()
        story_graph_path = given_file_created(docs_dir, 'story-graph.json', story_graph)
        story_map = when_story_map_created(test_instance=self, bot_directory=bot_directory)
        then_story_map_matches(story_map)
    
    def test_from_bot_with_path(self, tmp_path):
        """
        SCENARIO: From Bot With Path
        """
        # Given: Bot directory, docs directory, and story graph file are created
        bot_directory = given_test_bot_directory_created(tmp_path)
        docs_dir = given_directory_created(bot_directory, directory_type='docs')
        story_graph = given_story_graph_dict()
        story_graph_path = given_file_created(docs_dir, 'story-graph.json', story_graph)
        # When: Story map is created from bot
        story_map = StoryMap.from_bot(bot_directory)
        # Then: Story map contains test epic
        then_story_map_matches(story_map)
    
    # test_from_bot_raises_when_file_not_found removed - exception handling test
    
    def test_scenario_map_location(self, story_map):
        """
        SCENARIO: Scenario Map Location
        """
        # Given: Story map is loaded
        epics = when_item_accessed('epics', story_map)
        # When: Scenario is retrieved from epics
        scenario = when_item_accessed('scenario', epics)
        # Then: Scenario map location is correct
        then_location_matches(scenario)
    
    def test_scenario_outline_map_location(self, story_map):
        """
        SCENARIO: Scenario Outline Map Location
        """
        # Given: Story map is loaded
        epics = when_item_accessed('epics', story_map)
        # When: Scenario outline is retrieved from epics
        scenario_outline = when_item_accessed('scenario_outline', epics)
        # Then: Scenario outline map location is correct
        then_location_matches(scenario_outline)
    
    def test_from_bot_loads_story_graph(self, tmp_path):
        """
        SCENARIO: From Bot Loads Story Graph
        """
        bot_directory = given_test_bot_directory_created(tmp_path)
        docs_dir = given_directory_created(bot_directory, directory_type='docs')
        story_graph = given_story_graph_dict()
        story_graph_path = given_file_created(docs_dir, 'story-graph.json', story_graph)
        story_map = when_story_map_created(test_instance=self, bot_directory=bot_directory)
        then_story_map_matches(story_map)
    
    def test_from_bot_with_path(self, tmp_path):
        """
        SCENARIO: From Bot With Path
        """
        # Given: Bot directory, docs directory, and story graph file are created
        bot_directory = given_test_bot_directory_created(tmp_path)
        docs_dir = given_directory_created(bot_directory, directory_type='docs')
        story_graph = given_story_graph_dict()
        story_graph_path = given_file_created(docs_dir, 'story-graph.json', story_graph)
        # When: Story map is created from bot
        story_map = StoryMap.from_bot(bot_directory)
        # Then: Story map contains test epic
        then_story_map_matches(story_map)
    
    # test_from_bot_raises_when_file_not_found removed - exception handling test




# ============================================================================
# STORY: Create Build Scope (Sub-epic: Build Knowledge)
# ============================================================================

class TestCreateBuildScope:
    """Story: Create Build Scope (Sub-epic: Build Knowledge)"""
    
    @pytest.mark.parametrize("parameters,expected_scope_contains", [
        # Example 1: Scope 'all'
        ({'scope': {'type': 'all'}}, {'all': True}),
        # Example 2: Story names
        ({'scope': {'type': 'story', 'value': ['Story1']}}, {'story_names': ['Story1']}),
        # Example 3: Multiple story names
        ({'scope': {'type': 'story', 'value': ['Story1', 'Story2']}}, {'story_names': ['Story1', 'Story2']}),
        # Example 4: Increment priorities
        ({'scope': {'type': 'increment', 'value': [1]}}, {'increment_priorities': [1]}),
        # Example 5: Multiple increment priorities
        ({'scope': {'type': 'increment', 'value': [1, 2]}}, {'increment_priorities': [1, 2]}),
        # Example 6: Epic names
        ({'scope': {'type': 'epic', 'value': ['Epic A']}}, {'epic_names': ['Epic A']}),
        # Example 7: Multiple epic names
        ({'scope': {'type': 'epic', 'value': ['Epic A', 'Epic B']}}, {'epic_names': ['Epic A', 'Epic B']}),
        # Example 8: Increment names
        ({'scope': {'type': 'increment', 'value': ['Increment 1']}}, {'increment_names': ['Increment 1']}),
        # Example 9: No parameters (defaults to 'all')
        ({}, {'all': True}),
    ])
    def test_build_scope_created_with_different_parameter_combinations(self, parameters, expected_scope_contains):
        """
        SCENARIO: Build scope created with different parameter combinations
        GIVEN: Parameters dict with scope configuration
        WHEN: BuildScope instantiated with parameters
        THEN: BuildScope scope property returns expected configuration
        """
        # Given: Parameters dict
        # When: BuildScope instantiated
        build_scope = when_build_scope_instantiated(parameters)
        
        # Then: BuildScope scope property returns expected configuration
        then_build_scope_contains_all_expected(build_scope, expected_scope_contains)
    
    def test_build_scope_defaults_to_all_when_no_parameters(self):
        """
        SCENARIO: Build scope defaults to 'all' when no parameters provided
        GIVEN: Empty parameters dict
        WHEN: BuildScope instantiated
        THEN: Scope defaults to 'all'
        """
        # Given: Empty parameters
        parameters = {}
        
        # When: BuildScope instantiated
        build_scope = when_build_scope_instantiated(parameters)
        
        # Then: Scope defaults to 'all'
        then_build_scope_contains(build_scope, 'all', True)
    
    def test_action_uses_build_scope_to_define_build_scope(self, bot_directory, workspace_directory):
        """
        SCENARIO: Action uses BuildScope to define build scope
        GIVEN: BuildKnowledgeAction with parameters
        WHEN: Action executes with scope parameters
        THEN: Uses BuildScope class and includes scope in instructions
        """
        # Given: Environment bootstrapped
        bootstrap_env(bot_directory, workspace_directory)
        bot_name = 'story_bot'
        behavior_name = 'exploration'
        
        # Create behavior setup
        from agile_bot.bots.base_bot.test.test_helpers import create_actions_workflow_json
        from agile_bot.bots.base_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files
        create_actions_workflow_json(bot_directory, behavior_name)
        create_minimal_guardrails_files(bot_directory, behavior_name, bot_name)
        
        # Create knowledge graph directory and config
        kg_dir = given_directory_created(bot_directory, directory_type='knowledge_graph', behavior=behavior_name)
        given_setup('config_and_template', bot_directory, kg_dir=kg_dir)
        
        # Create behavior and action
        behavior = _create_behavior(bot_directory, bot_name, behavior_name, workspace_directory)
        action = BuildKnowledgeAction(behavior=behavior)
        parameters = given_build_parameters_with_scope('all')
        
        # When: Action executes with scope parameters
        # Then: Uses BuildScope class
        then_action_uses_build_scope_class(action, parameters)


# ============================================================================
# HELPER FUNCTIONS - Filter Knowledge Graph (Story: Filter Knowledge Graph)
# ============================================================================

def given_story_graph_with_epics_and_increments():
    """Given: Story graph with epics and increments."""
    return {
        'epics': [
            {
                'name': 'Epic A',
                'sub_epics': [
                    {
                        'name': 'Sub-epic A1',
                        'story_groups': [
                            {
                                'stories': [
                                    {'name': 'Story A1'},
                                    {'name': 'Story A2'}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                'name': 'Epic B',
                'sub_epics': [
                    {
                        'name': 'Sub-epic B1',
                        'story_groups': [
                            {
                                'stories': [
                                    {'name': 'Story B1'},
                                    {'name': 'Story B2'}
                                ]
                            }
                        ]
                    }
                ]
            }
        ],
        'increments': [
            {
                'name': 'Increment 1',
                'priority': 1,
                'epics': [
                    {
                        'name': 'Epic A',
                        'sub_epics': [
                            {
                                'name': 'Sub-epic A1',
                                'stories': [
                                    {'name': 'Story A1'},
                                    {'name': 'Story A2'}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                'name': 'Increment 2',
                'priority': 2,
                'epics': [
                    {
                        'name': 'Epic B',
                        'sub_epics': [
                            {
                                'name': 'Sub-epic B1',
                                'stories': [
                                    {'name': 'Story B1'},
                                    {'name': 'Story B2'}
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }


def when_scoping_parameter_filters_story_graph(scope_type, scope_value, story_graph):
    """When: ScopingParameter filters story graph."""
    from agile_bot.bots.base_bot.src.actions.scoping_parameter import ScopingParameter
    scope = {'type': scope_type}
    if scope_value is not None:
        scope['value'] = scope_value
    scoping_param = ScopingParameter(scope)
    return scoping_param.filter_story_graph(story_graph)


def then_story_graph_contains_epic(filtered_graph, epic_name):
    """Then: Story graph contains epic."""
    epic_names = [epic.get('name') for epic in filtered_graph.get('epics', [])]
    assert epic_name in epic_names


def then_story_graph_contains_story(filtered_graph, story_name):
    """Then: Story graph contains story."""
    story_names = []
    for epic in filtered_graph.get('epics', []):
        for sub_epic in epic.get('sub_epics', []):
            for story_group in sub_epic.get('story_groups', []):
                for story in story_group.get('stories', []):
                    if isinstance(story, dict):
                        story_names.append(story.get('name'))
                    else:
                        story_names.append(story)
    assert story_name in story_names


def then_story_graph_contains_increment(filtered_graph, increment_name):
    """Then: Story graph contains increment."""
    increment_names = [inc.get('name') for inc in filtered_graph.get('increments', [])]
    assert increment_name in increment_names


def then_story_graph_contains_all_epics(filtered_graph, expected_count):
    """Then: Story graph contains all epics."""
    assert len(filtered_graph.get('epics', [])) == expected_count


def then_story_graph_contains_all_increments(filtered_graph, expected_count):
    """Then: Story graph contains all increments."""
    assert len(filtered_graph.get('increments', [])) == expected_count


# ============================================================================
# STORY: Filter Knowledge Graph (Sub-epic: Build Knowledge)
# ============================================================================

class TestFilterKnowledgeGraph:
    """Story: Filter Knowledge Graph (Sub-epic: Build Knowledge)"""
    
    def test_filter_returns_all_when_scope_is_all(self):
        """
        SCENARIO: Filter returns all when scope is all
        GIVEN: Story graph with multiple epics and increments
        WHEN: ScopingParameter filters with scope type 'all'
        THEN: Story graph contains all epics and increments
        """
        # Given: Story graph with epics and increments
        story_graph = given_story_graph_with_epics_and_increments()
        
        # When: Filter with scope 'all'
        filtered_graph = when_scoping_parameter_filters_story_graph('all', None, story_graph)
        
        # Then: All epics and increments present
        then_story_graph_contains_all_epics(filtered_graph, 2)
        then_story_graph_contains_all_increments(filtered_graph, 2)
    
    def test_filter_by_story_names_returns_matching_stories(self):
        """
        SCENARIO: Filter by story names returns matching stories
        GIVEN: Story graph with multiple stories
        WHEN: ScopingParameter filters with story names
        THEN: Story graph contains only matching stories and their parent epics
        """
        # Given: Story graph with stories
        story_graph = given_story_graph_with_epics_and_increments()
        
        # When: Filter by story names
        filtered_graph = when_scoping_parameter_filters_story_graph('story', ['Story A1'], story_graph)
        
        # Then: Only matching story and its parent epic present
        then_story_graph_contains_epic(filtered_graph, 'Epic A')
        then_story_graph_contains_story(filtered_graph, 'Story A1')
        assert 'Epic B' not in [epic.get('name') for epic in filtered_graph.get('epics', [])]
    
    def test_filter_by_epic_names_returns_matching_epics(self):
        """
        SCENARIO: Filter by epic names returns matching epics
        GIVEN: Story graph with multiple epics
        WHEN: ScopingParameter filters with epic names
        THEN: Story graph contains only matching epics and their increments
        """
        # Given: Story graph with epics
        story_graph = given_story_graph_with_epics_and_increments()
        
        # When: Filter by epic names
        filtered_graph = when_scoping_parameter_filters_story_graph('epic', ['Epic A'], story_graph)
        
        # Then: Only matching epic present
        then_story_graph_contains_epic(filtered_graph, 'Epic A')
        assert 'Epic B' not in [epic.get('name') for epic in filtered_graph.get('epics', [])]
        then_story_graph_contains_increment(filtered_graph, 'Increment 1')
    
    def test_filter_by_increment_priorities_returns_matching_increments(self):
        """
        SCENARIO: Filter by increment priorities returns matching increments
        GIVEN: Story graph with increments having different priorities
        WHEN: ScopingParameter filters with increment priorities
        THEN: Story graph contains only matching increments and their stories
        """
        # Given: Story graph with increments
        story_graph = given_story_graph_with_epics_and_increments()
        
        # When: Filter by increment priorities
        filtered_graph = when_scoping_parameter_filters_story_graph('increment', [1], story_graph)
        
        # Then: Only matching increment present
        then_story_graph_contains_increment(filtered_graph, 'Increment 1')
        assert 'Increment 2' not in [inc.get('name') for inc in filtered_graph.get('increments', [])]
        then_story_graph_contains_epic(filtered_graph, 'Epic A')
    
    def test_filter_by_increment_names_returns_matching_increments(self):
        """
        SCENARIO: Filter by increment names returns matching increments
        GIVEN: Story graph with increments having different names
        WHEN: ScopingParameter filters with increment names
        THEN: Story graph contains only matching increments and their stories
        """
        # Given: Story graph with increments
        story_graph = given_story_graph_with_epics_and_increments()
        
        # When: Filter by increment names
        filtered_graph = when_scoping_parameter_filters_story_graph('increment', ['Increment 1'], story_graph)
        
        # Then: Only matching increment present
        then_story_graph_contains_increment(filtered_graph, 'Increment 1')
        assert 'Increment 2' not in [inc.get('name') for inc in filtered_graph.get('increments', [])]
        then_story_graph_contains_epic(filtered_graph, 'Epic A')