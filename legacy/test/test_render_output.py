"""
Render Output Tests

Tests for all stories in the 'Render Output' sub-epic:
- Track Activity for Render Output Action
- Proceed To Validate Rules
- Render Output Using Synchronizers
"""
import pytest
from pathlib import Path
import json
from agile_bot.bots.base_bot.src.actions.render.render_action import RenderOutputAction
from agile_bot.bots.base_bot.test.test_helpers import (
    bootstrap_env,
    create_activity_log_file,
    read_activity_log,
    then_activity_log_matches,
    given_activity_log,
    given_directory_created
)
from agile_bot.bots.base_bot.test.test_invoke_bot_directly import then_result_matches
from agile_bot.bots.base_bot.test.test_execute_behavior_actions import (
    verify_action_tracks_start,
    verify_action_tracks_completion,
    verify_workflow_transition,
    verify_workflow_saves_completed_action
)

# Use fixtures from conftest.py (bot_directory, workspace_directory)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def given_base_instructions_for_render_output_copied(bot_directory: Path):
    """Given: Base instructions for render_output copied."""
    from agile_bot.bots.base_bot.test.test_helpers import get_base_actions_dir, get_test_base_actions_dir
    import shutil
    repo_root = Path(__file__).parent.parent.parent.parent.parent
    actual_base_actions_dir = get_base_actions_dir(repo_root)
    # BaseActionConfig loads from action_config.json, not instructions.json
    # Action name is 'render', not 'render_output'
    actual_config_file = actual_base_actions_dir / 'render' / 'action_config.json'
    if not actual_config_file.exists():
        # Try render_output as fallback
        actual_config_file = actual_base_actions_dir / 'render_output' / 'action_config.json'
    bot_base_actions_dir = get_test_base_actions_dir(bot_directory) / 'render'
    bot_base_actions_dir.mkdir(parents=True, exist_ok=True)
    bot_config_file = bot_base_actions_dir / 'action_config.json'
    if actual_config_file.exists():
        shutil.copy2(actual_config_file, bot_config_file)
    else:
        # Create minimal config if file doesn't exist
        import json
        bot_config_file.write_text(json.dumps({
            "name": "render",
            "order": 5,
            "workflow": True,
            "instructions": [
                "render base instructions",
                "{{render_configs}}",
                "{{render_instructions}}"
            ]
        }), encoding='utf-8')
    return bot_config_file


def given_behavior_render_instructions_created(bot_directory: Path, behavior: str):
    """Given: Behavior render instructions created."""
    behavior_dir = bot_directory / 'behaviors' / behavior
    render_dir = behavior_dir / 'content' / 'render'
    render_dir.mkdir(parents=True, exist_ok=True)
    render_instructions_file = render_dir / 'instructions.json'
    render_instructions_file.write_text(
        json.dumps({
            'behaviorName': behavior,
            'instructions': ['Render all story files', 'Generate markdown output']
        }),
        encoding='utf-8'
    )
    return render_instructions_file


def given_render_configs_created(render_dir: Path, configs: list):
    """Given: Render configs created."""
    created_configs = []
    for config_data in configs:
        config_file = render_dir / f"{config_data['name']}.json"
        config_file.write_text(json.dumps(config_data), encoding='utf-8')
        created_configs.append(config_file)
    return created_configs


def when_render_output_action_created(bot_name: str, behavior: str, bot_directory: Path):
    """When: RenderOutputAction created."""
    from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
    from agile_bot.bots.base_bot.src.bot.behavior import Behavior
    # BaseActionConfig deleted - Action already has config loading
    from agile_bot.bots.base_bot.test.test_helpers import create_actions_workflow_json
    from agile_bot.bots.base_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files
    from conftest import create_base_actions_structure
    
    # Create base actions structure (required for action configs)
    create_base_actions_structure(bot_directory)
    
    # Create behavior.json and guardrails files
    create_actions_workflow_json(bot_directory, behavior)
    create_minimal_guardrails_files(bot_directory, behavior, bot_name)
    bot_paths = BotPaths(bot_directory=bot_directory)
    behavior_obj = Behavior(name=behavior, bot_paths=bot_paths)
    return RenderOutputAction(
        behavior=behavior_obj,
        action_config=None
    )


def when_render_output_action_loads_and_merges_instructions(bot_name: str, behavior: str, bot_directory: Path):
    """When: RenderOutputAction loads and merges instructions."""
    from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
    from agile_bot.bots.base_bot.src.bot.behavior import Behavior
    # BaseActionConfig deleted - Action already has config loading
    from agile_bot.bots.base_bot.test.test_helpers import create_actions_workflow_json
    from agile_bot.bots.base_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files
    
    # Create behavior.json and guardrails files
    create_actions_workflow_json(bot_directory, behavior)
    create_minimal_guardrails_files(bot_directory, behavior, bot_name)
    bot_paths = BotPaths(bot_directory=bot_directory)
    behavior_obj = Behavior(name=behavior, bot_paths=bot_paths)
    action_obj = RenderOutputAction(
        behavior=behavior_obj,
        action_config=None
    )
    # Call do_execute to trigger template variable replacement via _inject_render_data
    from agile_bot.bots.base_bot.src.actions.action_context import ScopeActionContext
    result = action_obj.do_execute(ScopeActionContext())
    instructions = result.get('instructions', {})
    return action_obj, instructions



def then_all_render_output_assertions_pass(base_instructions_text: str):
    """Then step: All render output assertions pass."""
    from agile_bot.bots.base_bot.test.test_helpers import then_template_variables_replaced, then_instructions_contain
    then_template_variables_replaced(base_instructions_text, type='render_configs')
    then_instructions_contain(base_instructions_text, 'render_required_fields')
    then_instructions_contain(base_instructions_text, 'render_field_values')
    then_template_variables_replaced(base_instructions_text, type='render_instructions')




def then_activity_log_file_does_not_exist(workspace_directory: Path):
    """Then: Activity log file does not exist."""
    log_file = workspace_directory / 'activity_log.json'
    assert not log_file.exists()
    return log_file


def when_render_output_action_tracks_start(bot_name: str, behavior: str, bot_directory: Path):
    """When: Render output action tracks start."""
    from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
    from agile_bot.bots.base_bot.src.bot.behavior import Behavior
    # BaseActionConfig deleted - Action already has config loading
    from agile_bot.bots.base_bot.test.test_helpers import create_actions_workflow_json
    from agile_bot.bots.base_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files
    # Create behavior.json and guardrails files
    create_actions_workflow_json(bot_directory, behavior)
    create_minimal_guardrails_files(bot_directory, behavior, bot_name)
    bot_paths = BotPaths(bot_directory=bot_directory)
    behavior_obj = Behavior(name=behavior, bot_paths=bot_paths)
    action = RenderOutputAction(
        behavior=behavior_obj,
        action_config=None
    )
    action.track_activity_on_start()
    return action


def then_activity_log_file_exists(log_file: Path):
    """Then: Activity log file exists."""
    assert log_file.exists()


def given_bot_name_and_behavior_for_discovery():
    """Given: Bot name and behavior for discovery."""
    bot_name = 'story_bot'
    behavior = 'discovery'
    return bot_name, behavior


def when_create_render_output_action(bot_name: str, behavior: str, bot_directory: Path):
    """When: Create render output action."""
    from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
    from agile_bot.bots.base_bot.src.bot.behavior import Behavior
    # BaseActionConfig deleted - Action already has config loading
    from agile_bot.bots.base_bot.test.test_helpers import create_actions_workflow_json
    from agile_bot.bots.base_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files
    # Create behavior.json and guardrails files
    create_actions_workflow_json(bot_directory, behavior)
    create_minimal_guardrails_files(bot_directory, behavior, bot_name)
    bot_paths = BotPaths(bot_directory=bot_directory)
    behavior_obj = Behavior(name=behavior, bot_paths=bot_paths)
    action = RenderOutputAction(
        behavior=behavior_obj,
        action_config=None
    )
    return action




def given_bot_name_and_behavior_for_shape():
    """Given: Bot name and behavior for shape."""
    bot_name = 'test_bot'
    behavior = 'shape'
    return bot_name, behavior


def given_render_dir_and_configs_setup(bot_directory: Path, behavior: str):
    """Given: Render dir and configs setup."""
    behavior_dir = bot_directory / 'behaviors' / behavior
    render_dir = behavior_dir / 'content' / 'render'
    render_dir.mkdir(parents=True, exist_ok=True)
    given_behavior_render_instructions_created(bot_directory, behavior)
    
    # Create template file if referenced in configs
    templates_dir = render_dir / 'templates'
    templates_dir.mkdir(parents=True, exist_ok=True)
    template_file = templates_dir / 'story-map.txt'
    template_file.write_text('Story Map Template', encoding='utf-8')
    
    given_render_configs_created(render_dir, [
        {
            'name': 'render_story_files',
            'type': 'synchronizer',
            'path': 'docs/stories',
            'input': 'story-graph.json',
            'synchronizer': 'synchronizers.story_scenarios.StoryScenariosSynchronizer',
            'output': 'docs/stories',
            'instructions': 'Render story-graph.json to story markdown files'
        },
        {
            'name': 'render_story_map_txt',
            'type': 'template',
            'path': 'docs/stories',
            'input': 'story-graph.json',
            'template': 'templates/story-map.txt',
            'output': 'story-map.txt',
            'instructions': 'Render story-graph.json to story-map.txt format'
        }
    ])
    return render_dir


def when_render_configs_formatted(configs=None, format_type='json', action_obj=None):
    """
    Consolidated function for formatting render configs.
    Replaces: when_format_render_configs
    
    Args:
        configs: Render configs dict (if None and action_obj provided, loads from action_obj)
        format_type: Format type (default 'json')
        action_obj: Action object (if provided and configs is None, loads configs from it)
    
    Returns:
        Formatted configs string
    """
    if configs is None:
        if action_obj is None:
            raise ValueError("Either configs or action_obj must be provided")
        configs = action_obj._config_loader.load_render_configs()
    
    if action_obj is not None:
        # Convert dict configs to RenderSpec objects if needed
        from agile_bot.bots.base_bot.src.actions.render.render_spec import RenderSpec
        if configs and isinstance(configs[0], dict):
            # Convert dict configs to RenderSpec objects
            render_specs = []
            for config_dict in configs:
                config_data = config_dict.get('config', config_dict)
                render_folder = action_obj._config_loader.find_render_folder()
                spec = RenderSpec(config_data, render_folder, action_obj.behavior.bot_paths)
                render_specs.append(spec)
            return action_obj._instruction_formatter.format_render_configs(render_specs)
        else:
            # Already RenderSpec objects
            return action_obj._instruction_formatter.format_render_configs(configs)
    else:
        # If no action_obj, assume configs is already a dict and format it
        import json
        return json.dumps(configs, indent=2) if format_type == 'json' else str(configs)


def then_formatted_configs_contain_sync_and_template(formatted: str):
    """Then: Formatted configs contain sync and template."""
    assert 'render_sync' in formatted
    assert 'render_template' in formatted


def then_formatted_configs_contain_synchronizer_fields(formatted: str):
    """Then: Formatted configs contain synchronizer fields."""
    assert 'Instructions:' in formatted or 'instructions' in formatted.lower()
    assert 'Synchronizer:' in formatted or 'synchronizer' in formatted.lower()
    assert 'synchronizers.test.TestSynchronizer' in formatted
    assert 'renderer_command' in formatted.lower() or 'Renderer Command:' in formatted
    assert 'render-test' in formatted
    assert 'Input:' in formatted or 'input' in formatted.lower()
    assert 'story-graph.json' in formatted
    assert 'Output:' in formatted or 'output' in formatted.lower()
    assert 'test-output.drawio' in formatted


def then_formatted_configs_contain_template_fields(formatted: str):
    """Then: Formatted configs contain template fields."""
    assert 'Template:' in formatted or 'template' in formatted.lower()
    assert 'templates/test-template.md' in formatted
    assert 'test-output.md' in formatted


def when_create_sync_and_template_configs(render_dir: Path):
    """When: Create sync and template configs."""
    sync_config = render_dir / 'render_sync.json'
    sync_config.write_text(
        json.dumps({
            'name': 'render_sync',
            'type': 'synchronizer',
            'path': 'docs/stories',
            'input': 'story-graph.json',
            'synchronizer': 'synchronizers.test.TestSynchronizer',
            'renderer_command': 'render-test',
            'output': 'test-output.drawio',
            'instructions': 'Test synchronizer instructions'
        }),
        encoding='utf-8'
    )
    
    template_config = render_dir / 'render_template.json'
    template_config.write_text(
        json.dumps({
            'name': 'render_template',
            'type': 'template',
            'path': 'docs/stories',
            'input': 'story-graph.json',
            'template': 'templates/test-template.md',
            'output': 'test-output.md',
            'instructions': 'Test template instructions'
        }),
        encoding='utf-8'
    )
    
    # Create the template file that the config references
    templates_dir = render_dir / 'templates'
    templates_dir.mkdir(parents=True, exist_ok=True)
    template_file = templates_dir / 'test-template.md'
    template_file.write_text('# Test Template\n\nThis is a test template.', encoding='utf-8')
    
    return sync_config, template_config


# ============================================================================
# STORY: Track Activity for Render Output Action
# ============================================================================

class TestTrackActivityForRenderOutputAction:
    """Story: Track Activity for Render Output Action - Tests activity tracking for render_output."""

    def test_track_activity_when_render_output_action_starts(self, bot_directory, workspace_directory):
        # Given: Bot directory and workspace directory are set up
        # When: Render output action starts
        # Then: Activity is tracked (verified by verify_action_tracks_start)
        verify_action_tracks_start(bot_directory, workspace_directory, RenderOutputAction, 'render', behavior='discovery')

    def test_track_activity_when_render_output_action_completes(self, bot_directory, workspace_directory):
        # Given: Bot directory and workspace directory are set up
        # When: Render output action completes with outputs and duration
        # Then: Activity is tracked (verified by verify_action_tracks_completion)
        verify_action_tracks_completion(
            bot_directory,
            workspace_directory,
            RenderOutputAction,
            'render',
            behavior='discovery',
            outputs={'files_generated_count': 3, 'file_paths': ['story-map.md', 'increments.md']},
            duration=180
        )

    def test_track_multiple_render_output_invocations_across_behaviors(self, workspace_directory):
        # Activity log is in workspace_directory
        given_activity_log(workspace_directory, return_file=False)
        
        then_activity_log_matches(
            workspace_directory,
            expected_count=2,
            expected_action_states=['story_bot.shape.render', 'story_bot.discovery.render']
        )

    def test_activity_log_creates_file_if_not_exists(self, bot_directory, workspace_directory):
        """
        SCENARIO: Activity Log Creates File If Not Exists
        GIVEN: workspace directory exists but no activity log
        WHEN: Action tracks activity
        THEN: Activity log file is created automatically
        """
        # Given: Workspace directory exists but no activity log
        # Bootstrap environment
        bootstrap_env(bot_directory, workspace_directory)
        
        log_file = then_activity_log_file_does_not_exist(workspace_directory)
        
        # When: Action tracks activity
        # Then: Activity log file is created automatically
        when_render_output_action_tracks_start('story_bot', 'discovery', bot_directory)
        
        # Then: Log file is created
        then_activity_log_file_exists(log_file)


# ============================================================================
# STORY: Proceed To Validate Rules
# ============================================================================

class TestProceedToValidateRules:
    """Story: Proceed To Validate - Tests transition to validate action."""

    def test_seamless_transition_from_validate_to_render_output(self, bot_directory, workspace_directory):
        """
        SCENARIO: Seamless Transition From Validate Rules To Render Output
        """
        # Given: Bot directory and workspace directory are set up
        # When: Validate rules action completes
        # Then: Workflow transitions to render_output (verified by verify_workflow_transition)
        verify_workflow_transition(bot_directory, workspace_directory, 'validate', 'render', behavior='discovery')

    def test_workflow_state_captures_render_output_completion(self, bot_directory, workspace_directory):
        """
        SCENARIO: Workflow State Captures Render Output Completion
        """
        # Given: Bot directory and workspace directory are set up
        # When: Render output action completes
        # Then: Workflow state captures completion (verified by verify_workflow_saves_completed_action)
        verify_workflow_saves_completed_action(bot_directory, workspace_directory, 'render')

    def test_render_output_action_executes_successfully(self, bot_directory, workspace_directory):
        """
        SCENARIO: Render Output Action Executes Successfully
        GIVEN: render_output action is initialized
        WHEN: Action is executed
        THEN: Action completes without errors
        """
        # Bootstrap environment
        bootstrap_env(bot_directory, workspace_directory)
        
        bot_name, behavior = given_bot_name_and_behavior_for_discovery()
        
        action = when_create_render_output_action(bot_name, behavior, bot_directory)
        
        # Action should initialize successfully
        then_result_matches(action, bot_name=bot_name, behavior=behavior)


# ============================================================================
# STORY: Inject Render Instructions and Configs
# ============================================================================

class TestInjectRenderInstructionsAndConfigs:
    """Story: Inject Render Instructions and Configs - Tests template variable injection."""

    def test_all_template_variables_are_replaced_in_instructions(self, bot_directory, workspace_directory):
        """
        SCENARIO: All template variables are replaced in final instructions
        GIVEN: Base instructions with {{render_configs}} and {{render_instructions}} placeholders
        WHEN: Action loads and merges instructions with all injections
        THEN: All template variables are replaced with actual content
        """
        bootstrap_env(bot_directory, workspace_directory)
        bot_name, behavior = given_bot_name_and_behavior_for_shape()
        
        render_dir = given_render_dir_and_configs_setup(bot_directory, behavior)
        
        # Create base actions structure first, then update render config with placeholders
        from conftest import create_base_actions_structure
        create_base_actions_structure(bot_directory)
        given_base_instructions_for_render_output_copied(bot_directory)
        
        action_obj, instructions = when_render_output_action_loads_and_merges_instructions(bot_name, behavior, bot_directory)
        
        base_instructions_text = '\n'.join(instructions.get('base_instructions', []))
        then_all_render_output_assertions_pass(base_instructions_text)

    def test_render_configs_format_includes_all_fields(self, bot_directory, workspace_directory):
        """
        SCENARIO: Formatted render_configs includes all fields referenced in instructions
        GIVEN: Render configs with instructions, synchronizer, template, input, output fields
        WHEN: Configs are formatted for injection
        THEN: All fields are present in formatted output
        """
        # Bootstrap
        bootstrap_env(bot_directory, workspace_directory)
        
        bot_name, behavior = given_bot_name_and_behavior_for_shape()
        render_dir = given_directory_created(bot_directory, directory_type='behavior_render', behavior=behavior)
        when_create_sync_and_template_configs(render_dir)
        
        # When: Action formats render configs
        action_obj = when_render_output_action_created(bot_name, behavior, bot_directory)
        
        formatted = when_render_configs_formatted(action_obj=action_obj)
        
        # Then: All fields are present
        then_formatted_configs_contain_sync_and_template(formatted)
        then_formatted_configs_contain_synchronizer_fields(formatted)
        then_formatted_configs_contain_template_fields(formatted)


# ============================================================================
# HELPER FUNCTIONS - Domain Classes (Stories 7-8: MergedInstructions Render)
# ============================================================================

from unittest.mock import Mock
from agile_bot.bots.base_bot.src.bot.merged_instructions import MergedInstructions
# BaseActionConfig deleted - Action already has config loading


def given_action_with_instructions(instructions: list):
    """Given: Action with instructions (BaseActionConfig merged into Action)."""
    from agile_bot.bots.base_bot.src.actions.action import Action
    action = Mock(spec=Action)
    action._base_config = {'instructions': instructions}
    action.instructions = instructions
    return action


def given_render_instructions(instructions: dict):
    """Given: Render instructions dict."""
    return instructions


def when_merged_instructions_instantiated(base_action_config, render_instructions=None):
    """When: MergedInstructions instantiated."""
    # Extract instructions from base_action_config if it's a Mock/object, otherwise use directly
    if hasattr(base_action_config, 'instructions'):
        base_instructions = base_action_config.instructions
    elif isinstance(base_action_config, list):
        base_instructions = base_action_config
    else:
        base_instructions = base_action_config
    return MergedInstructions(base_instructions, render_instructions)


def when_render_instructions_accessed(merged_instructions: MergedInstructions):
    """When: render_instructions property accessed."""
    return merged_instructions.render_instructions


def when_merge_called(merged_instructions: MergedInstructions):
    """When: merge() called."""
    return merged_instructions.merge()


def then_render_instructions_are(result: dict, expected: dict):
    """Then: Render instructions are expected."""
    assert result == expected


def then_render_instructions_is_none(result):
    """Then: Render instructions is None."""
    assert result is None


def then_merged_contains_base_instructions(merged: dict, expected: list):
    """Then: Merged dict contains base instructions."""
    assert merged['base_instructions'] == expected


def then_merged_contains_render_instructions(merged: dict, expected: dict):
    """Then: Merged dict contains render instructions."""
    assert 'render_instructions' in merged
    assert merged['render_instructions'] == expected


def then_merged_does_not_contain_render_instructions(merged: dict):
    """Then: Merged dict does not contain render instructions."""
    assert 'render_instructions' not in merged


# ============================================================================
# TEST CLASSES - Domain Classes (Stories 7-8: MergedInstructions Render)
# ============================================================================

class TestGetRenderInstructions:
    """Story: Get Render Instructions (Sub-epic: Render Output)"""
    
def then_render_instructions_matches_expected(result, expected_result):
    """Then: Render instructions matches expected result."""
    if expected_result is None:
        then_render_instructions_is_none(result)
    else:
        then_render_instructions_are(result, expected_result)


class TestGetRenderInstructions:
    """Story: Get Render Instructions (Sub-epic: Render Output)"""
    
    @pytest.mark.parametrize("render_instructions,expected_result", [
        # Example 1: Render instructions provided
        ({'instructions': ['render1', 'render2']}, {'instructions': ['render1', 'render2']}),
        # Example 2: No render instructions
        (None, None),
    ])
    def test_render_instructions_property_returns_provided_instructions_or_none(self, render_instructions, expected_result):
        """
        SCENARIO: Render instructions property returns provided instructions or None
        GIVEN: MergedInstructions with or without render instructions
        WHEN: render_instructions property accessed
        THEN: Returns render instructions dict when provided, None when not provided
        """
        # Given: BaseActionConfig and optional render instructions
        base_action_config = given_action_with_instructions(['base1'])
        
        # When: MergedInstructions instantiated and render_instructions accessed
        merged_instructions = when_merged_instructions_instantiated(base_action_config, render_instructions)
        result = when_render_instructions_accessed(merged_instructions)
        
        # Then: Render instructions are expected
        then_render_instructions_matches_expected(result, expected_result)


class TestMergeBaseAndRenderInstructions:
    """Story: Merge Base and Render Instructions (Sub-epic: Render Output)"""
    
    def test_merge_combines_base_and_render_instructions(self):
        """
        SCENARIO: Merge combines base and render instructions
        GIVEN: BaseActionConfig with ['base1', 'base2'] and render instructions {'instructions': ['render1', 'render2']}
        WHEN: merge() called
        THEN: Returns dict with base_instructions and render_instructions
        """
        # Given: BaseActionConfig and render instructions
        base_action_config = given_action_with_instructions(['base1', 'base2'])
        render_instructions = {'instructions': ['render1', 'render2']}
        
        # When: MergedInstructions instantiated and merge() called
        merged_instructions = when_merged_instructions_instantiated(base_action_config, render_instructions)
        result = when_merge_called(merged_instructions)
        
        # Then: Merged dict contains both instruction sets
        then_merged_contains_base_instructions(result, ['base1', 'base2'])
        then_merged_contains_render_instructions(result, render_instructions)
    
    def test_merge_handles_empty_render_instructions(self):
        """
        SCENARIO: Merge handles empty render instructions
        GIVEN: BaseActionConfig with ['base1'] and empty render instructions {}
        WHEN: merge() called
        THEN: Returns dict with base_instructions and empty render_instructions
        """
        # Given: BaseActionConfig with empty render instructions dict
        base_action_config = given_action_with_instructions(['base1'])
        render_instructions = {}
        
        # When: MergedInstructions instantiated and merge() called
        merged_instructions = when_merged_instructions_instantiated(base_action_config, render_instructions)
        result = when_merge_called(merged_instructions)
        
        # Then: Merged dict contains base instructions and empty render instructions
        then_merged_contains_base_instructions(result, ['base1'])
        then_merged_contains_render_instructions(result, render_instructions)


# ============================================================================
# STORY: Render Output Using Synchronizers
# ============================================================================

class TestRenderOutputUsingSynchronizers:
    """Story: Render Output Using Synchronizers - Tests automatic execution of synchronizers."""

    def test_synchronizers_are_executed_automatically(self, bot_directory, workspace_directory):
        """
        SCENARIO: Synchronizers are executed automatically during render action
        GIVEN: Render configs with synchronizers are defined
        WHEN: Render output action executes
        THEN: Synchronizers are executed automatically and outputs are generated
        """
        bootstrap_env(bot_directory, workspace_directory)
        bot_name, behavior = given_bot_name_and_behavior_for_shape()
        
        render_dir = given_directory_created(bot_directory, directory_type='behavior_render', behavior=behavior)
        
        # Create a test synchronizer config
        given_render_configs_created(render_dir, [
            {
                'name': 'render_domain_model_description',
                'type': 'synchronizer',
                'path': 'docs/stories',
                'input': 'story-graph.json',
                'synchronizer': 'synchronizers.domain_model.DomainModelDescriptionSynchronizer',
                'output': 'domain-model-description.md',
                'instructions': 'Generate domain model description'
            }
        ])
        
        # Create story-graph.json input file
        workspace_dir = workspace_directory
        docs_dir = workspace_dir / 'docs' / 'stories'
        docs_dir.mkdir(parents=True, exist_ok=True)
        story_graph_file = docs_dir / 'story-graph.json'
        story_graph_file.write_text(
            json.dumps({
                'epics': [],
                'domain_concepts': {}
            }),
            encoding='utf-8'
        )
        
        # When: Render output action executes
        action = when_render_output_action_created(bot_name, behavior, bot_directory)
        action.behavior.bot_paths._workspace_directory = workspace_dir
        from agile_bot.bots.base_bot.src.actions.action_context import ScopeActionContext
        result = action.do_execute(ScopeActionContext())
        
        # Then: Synchronizers were executed
        executed_specs = result.get('executed_specs', [])
        assert len(executed_specs) > 0
        
        executed_spec = executed_specs[0]
        # Returns config_data dict from RenderSpec, check for synchronizer in config
        assert 'synchronizer' in executed_spec

    def test_template_configs_remain_in_instructions(self, bot_directory, workspace_directory):
        """
        SCENARIO: Template configs remain in instructions for AI handling
        GIVEN: Render configs with both synchronizers and templates
        WHEN: Render output action executes
        THEN: Synchronizers are executed, templates remain in instructions
        """
        bootstrap_env(bot_directory, workspace_directory)
        bot_name, behavior = given_bot_name_and_behavior_for_shape()
        
        render_dir = given_directory_created(bot_directory, directory_type='behavior_render', behavior=behavior)
        
        # Create configs with both synchronizer and template
        given_render_configs_created(render_dir, [
            {
                'name': 'render_domain_model',
                'type': 'synchronizer',
                'path': 'docs/stories',
                'input': 'story-graph.json',
                'synchronizer': 'synchronizers.domain_model.DomainModelDescriptionSynchronizer',
                'output': 'domain-model.md',
                'instructions': 'Generate domain model'
            },
            {
                'name': 'render_story_map',
                'type': 'template',
                'path': 'docs/stories',
                'input': 'story-graph.json',
                'template': 'templates/story-map.txt',
                'output': 'story-map.txt',
                'instructions': 'Render story map using template'
            }
        ])
        
        # Create template file
        templates_dir = render_dir / 'templates'
        templates_dir.mkdir(parents=True, exist_ok=True)
        template_file = templates_dir / 'story-map.txt'
        template_file.write_text('Story Map Template', encoding='utf-8')
        
        # Create story-graph.json input file
        workspace_dir = workspace_directory
        docs_dir = workspace_dir / 'docs' / 'stories'
        docs_dir.mkdir(parents=True, exist_ok=True)
        story_graph_file = docs_dir / 'story-graph.json'
        story_graph_file.write_text(
            json.dumps({
                'epics': [],
                'domain_concepts': {}
            }),
            encoding='utf-8'
        )
        
        # When: Render output action executes
        action = when_render_output_action_created(bot_name, behavior, bot_directory)
        action.behavior.bot_paths._workspace_directory = workspace_dir
        from agile_bot.bots.base_bot.src.actions.action_context import ScopeActionContext
        result = action.do_execute(ScopeActionContext())
        
        # Then: Synchronizers executed, templates in instructions
        executed_specs = result.get('executed_specs', [])
        template_specs = result.get('template_specs', [])
        
        assert len(executed_specs) == 1
        # Check that executed spec has synchronizer (config_data format)
        executed_spec = executed_specs[0]
        assert 'synchronizer' in executed_spec
        
        # Filter for the render_story_map config specifically (there may be other configs like instructions.json)
        story_map_specs = [spec for spec in template_specs if spec.get('name') == 'render_story_map']
        assert len(story_map_specs) == 1, f"Expected 1 render_story_map spec, got {len(story_map_specs)} in {template_specs}"
        story_map_spec = story_map_specs[0]
        assert story_map_spec.get('name') == 'render_story_map'
        
        # Verify template config is in instructions
        instructions = result.get('instructions', {})
        render_configs_in_instructions = instructions.get('render_configs', [])
        story_map_in_instructions = [cfg for cfg in render_configs_in_instructions if cfg.get('name') == 'render_story_map']
        assert len(story_map_in_instructions) == 1, f"Expected 1 render_story_map in instructions"
        assert story_map_in_instructions[0]['name'] == 'render_story_map'

    def test_executed_synchronizers_info_in_instructions(self, bot_directory, workspace_directory):
        """
        SCENARIO: Executed synchronizers information is included in AI instructions
        GIVEN: Render configs with synchronizers
        WHEN: Render output action executes
        THEN: Instructions include information about executed synchronizers
        """
        bootstrap_env(bot_directory, workspace_directory)
        bot_name, behavior = given_bot_name_and_behavior_for_shape()
        
        render_dir = given_directory_created(bot_directory, directory_type='behavior_render', behavior=behavior)
        
        given_render_configs_created(render_dir, [
            {
                'name': 'render_domain_model',
                'type': 'synchronizer',
                'path': 'docs/stories',
                'input': 'story-graph.json',
                'synchronizer': 'synchronizers.domain_model.DomainModelDescriptionSynchronizer',
                'output': 'domain-model.md',
                'instructions': 'Generate domain model'
            }
        ])
        
        # Create story-graph.json input file
        workspace_dir = workspace_directory
        docs_dir = workspace_dir / 'docs' / 'stories'
        docs_dir.mkdir(parents=True, exist_ok=True)
        story_graph_file = docs_dir / 'story-graph.json'
        story_graph_file.write_text(
            json.dumps({
                'epics': [],
                'domain_concepts': {}
            }),
            encoding='utf-8'
        )
        
        # When: Render output action executes
        action = when_render_output_action_created(bot_name, behavior, bot_directory)
        action.behavior.bot_paths._workspace_directory = workspace_dir
        from agile_bot.bots.base_bot.src.actions.action_context import ScopeActionContext
        result = action.do_execute(ScopeActionContext())
        
        # Then: Instructions include executed synchronizers info
        instructions = result.get('instructions', {})
        base_instructions = '\n'.join(instructions.get('base_instructions', []))
        
        assert 'Synchronizers Already Executed' in base_instructions
        assert 'render_domain_model' in base_instructions
        assert 'EXECUTED' in base_instructions
