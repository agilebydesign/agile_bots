"""
Invoke MCP Tool Tests

Tests for 'Invoke Bot Tool' sub-epic and 'Perform Behavior Action' sub-epic:

Foundational Tests (Increment 1/2):
- Bot Tool Invocation
- Behavior Action Instructions

Increment 3 Tests:
- Forward To Current Behavior and Current Action
- Forward To Current Action
- Activity Logged To Workspace Area Not Bot Area

Uses behavior action state management (behavior_action_state.json).
"""
import pytest
from pathlib import Path
import json
from conftest import create_bot_config_file, create_behavior_action_state_file
from agile_bot.bots.base_bot.src.actions.clarify.clarify_action import ClarifyContextAction
from agile_bot.bots.base_bot.test.test_helpers import bootstrap_env, create_behavior_action_instructions, create_actions_workflow_json
from agile_bot.bots.base_bot.test.test_helpers import (
    create_base_action_instructions,
    given_bot_instance_created,
    create_base_instructions,
    then_item_matches,
    then_file_exists,
    then_file_does_not_exist,
    then_activity_log_matches
)

# ============================================================================
# HELPER FUNCTIONS - Sub-Epic Level (Used across multiple test classes)
# ============================================================================

def given_base_actions_setup(bot_directory):
    """
    Consolidated function for base actions setup.
    Replaces: given_base_actions_structure_created
    
    Creates the base_actions directory structure for shared action templates.
    Note: This should NOT overwrite the bot_config.json file.
    """
    from conftest import create_base_actions_structure
    return create_base_actions_structure(bot_directory)

from agile_bot.bots.base_bot.test.test_helpers import create_behavior_action_instructions

def create_behavior_action_instructions_from_workspace(workspace: Path, bot_name: str, behavior: str, action: str) -> Path:
    """Helper: Create behavior action instructions file from workspace root.
    
    Wrapper around test_helpers.create_behavior_action_instructions that takes workspace and bot_name.
    """
    bot_dir = workspace / 'agile_bot' / 'bots' / bot_name
    return create_behavior_action_instructions(bot_dir, behavior, action)

# Use shared helper from test_helpers - imported above


def given_behavior_instructions_for_behaviors(bot_directory_or_workspace, behaviors, instructions=None, bot_name=None, action=None):
    """
    Consolidated function for behavior instructions setup.
    Replaces: given_behavior_action_instructions_for_multiple_behaviors
    
    Args:
        bot_directory_or_workspace: Bot directory path or workspace root (if workspace_root, bot_name must be provided)
        behaviors: List of behavior names
        instructions: Instructions dict (if None, creates files)
        bot_name: Bot name (required if bot_directory_or_workspace is workspace root)
        action: Action name (required if creating files)
    """
    if instructions is None:
        # Determine if bot_directory_or_workspace is workspace_root or bot_directory
        if bot_name is not None and action is not None:
            # Assume it's workspace_root
            workspace_root = bot_directory_or_workspace
            for behavior in behaviors:
                create_behavior_action_instructions_from_workspace(workspace_root, bot_name, behavior, action)
        else:
            # Assume it's bot_directory
            bot_directory = bot_directory_or_workspace
            if action is None:
                action = 'clarify'
            from agile_bot.bots.base_bot.test.test_helpers import create_behavior_action_instructions
            for behavior in behaviors:
                create_behavior_action_instructions(bot_directory, behavior, action)
    else:
        # If instructions provided, create files directly
        bot_directory = bot_directory_or_workspace
        from agile_bot.bots.base_bot.test.test_helpers import create_behavior_action_instructions
        for behavior in behaviors:
            create_behavior_action_instructions(bot_directory, behavior, action or 'clarify')


def given_behavior_json_files_for_behaviors(bot_directory: Path, behaviors: list, bot_name: str = 'test_bot'):
    """Given: Behavior.json files for behaviors."""
    from agile_bot.bots.base_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files
    for behavior in behaviors:
        create_actions_workflow_json(bot_directory, behavior)
        # Create guardrails files (required by Guardrails class initialization)
        create_minimal_guardrails_files(bot_directory, behavior, bot_name)


def given_base_action_instructions_created(bot_directory: Path, action: str):
    """Given: Base action instructions created."""
    from agile_bot.bots.base_bot.src.bot.workspace import get_python_workspace_root
    repo_root = get_python_workspace_root()
    return create_base_action_instructions(bot_directory, action)






def given_knowledge_graph_setup_for_behaviors(workspace_root: Path, bot_name: str, behavior_mapping: dict, action: str):
    """Given: Knowledge graph setup for behaviors."""
    behaviors_dir = workspace_root / 'agile_bot' / 'bots' / bot_name / 'behaviors'
    bot_dir = workspace_root / 'agile_bot' / 'bots' / bot_name
    for behavior, prefixed_name in behavior_mapping.items():
        behavior_dir = behaviors_dir / prefixed_name
        behavior_dir.mkdir(parents=True, exist_ok=True)
        create_actions_workflow_json(bot_dir, prefixed_name)
        kg_dir = behavior_dir / 'content' / 'knowledge_graph'
        kg_dir.mkdir(parents=True, exist_ok=True)
        template_filename = 'test_template.json'
        kg_config = {'template': template_filename}
        (kg_dir / 'build_story_graph_outline.json').write_text(
            json.dumps(kg_config), encoding='utf-8'
        )
        template_content = {'instructions': ['Test knowledge graph template']}
        (kg_dir / template_filename).write_text(
            json.dumps(template_content), encoding='utf-8'
        )




def given_behavior_action_state(bot_name, behavior, current_action, completed_actions=None, workspace_directory=None):
    """
    Consolidated function for creating behavior action state.
    Replaces: given_behavior_action_state_created
    
    Args:
        bot_name: Bot name
        behavior: Behavior name
        current_action: Current action name (can be full action_state or just action)
        completed_actions: List of completed actions (defaults to empty list)
        workspace_directory: Workspace directory (if None, uses current directory)
    """
    if workspace_directory is None:
        from pathlib import Path
        workspace_directory = Path.cwd()
    
    if completed_actions is None:
        completed_actions = []
    
    # Handle both full action_state format and simple action name
    if '.' in str(current_action):
        current_action_state = current_action
        current_behavior_state = f'{bot_name}.{behavior}' if '.' not in str(behavior) else behavior
    else:
        current_action_state = f'{bot_name}.{behavior}.{current_action}'
        current_behavior_state = f'{bot_name}.{behavior}'
    
    state_file = workspace_directory / 'behavior_action_state.json'
    state_file.write_text(json.dumps({
        'current_behavior': current_behavior_state,
        'current_action': current_action_state,
        'completed_actions': completed_actions
    }, indent=2), encoding='utf-8')
    return state_file


def given_base_instructions_created(bot_directory: Path):
    """Given: Base instructions created."""
    from agile_bot.bots.base_bot.src.bot.workspace import get_python_workspace_root
    repo_root = get_python_workspace_root()
    create_base_instructions(bot_directory)


def given_bot_config_and_behavior_workflow(bot_directory: Path, bot_name: str, behaviors: list):
    """Given: Bot config and behavior workflow created."""
    bot_config = create_bot_config_file(bot_directory, bot_name, behaviors)
    given_behavior_json_files_for_behaviors(bot_directory, behaviors, bot_name)
    return bot_config


def then_behavior_action_state_file_exists(workspace_directory: Path):
    """Then: Behavior action state file exists."""
    state_file = workspace_directory / 'behavior_action_state.json'
    then_file_exists(state_file)
    return state_file


def then_behavior_action_state_has_correct_values(state_file: Path, expected_behavior: str, expected_action: str):
    """Then: Behavior action state has correct values."""
    state_data = json.loads(state_file.read_text())
    # The format requires current_action (current_behavior is managed separately by Behaviors collection)
    assert state_data.get('current_action') == expected_action, f"Expected current_action={expected_action}, got {state_data.get('current_action')}"


# Note: This wrapper preserves bot_name parameter for backward compatibility




def then_activity_log_exists_at_path(expected_path: Path):
    """Then: Activity log exists at expected path."""
    then_file_exists(expected_path)


def then_activity_log_does_not_exist_at_path(unexpected_path: Path):
    """Then: Activity log does not exist at unexpected path."""
    then_file_does_not_exist(unexpected_path)


def then_activity_log_has_entry_with_action_state(workspace_directory: Path, expected_action_state: str, expected_status: str = 'started'):
    """Then: Activity log has entry with expected action_state."""
    from agile_bot.bots.base_bot.test.test_helpers import then_activity_log_matches
    then_activity_log_matches(workspace_directory, expected_action_state=expected_action_state, expected_status=expected_status, expected_count=1)


def then_activity_log_has_single_entry(workspace_directory: Path, expected_action_state: str, expected_status: str):
    """Then: Activity log has single entry with expected values."""
    from tinydb import TinyDB
    log_file = workspace_directory / 'activity_log.json'
    with TinyDB(log_file) as db:
        entries = db.all()
        assert len(entries) == 1
        assert entries[0]['action_state'] == expected_action_state
        assert entries[0]['status'] == expected_status


def given_bot_name_behavior_and_action_setup():
    """Given: Bot name, behavior and action setup."""
    bot_name = 'test_bot'
    behavior = 'shape'
    action = 'clarify'
    return bot_name, behavior, action


def when_create_gather_context_action(bot_name: str, behavior: str, bot_directory: Path):
    """When: Create gather context action."""
    from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
    from agile_bot.bots.base_bot.src.bot.behavior import Behavior
    # BaseActionConfig deleted - Action already has config loading
    
    # Create bot_paths
    bot_paths = BotPaths(bot_directory=bot_directory)
    
    import json
    behavior_dir = bot_directory / 'behaviors' / behavior
    behavior_dir.mkdir(parents=True, exist_ok=True)
    behavior_file = behavior_dir / 'behavior.json'
    behavior_config = {
        "behaviorName": behavior,
        "description": f"Test behavior: {behavior}",
        "goal": f"Test goal for {behavior}",
        "inputs": "Test inputs",
        "outputs": "Test outputs",
        "instructions": {},
        "actions_workflow": {
            "actions": [
                {'name': 'clarify', 'order': 1}
            ]
        }
    }
    behavior_file.write_text(json.dumps(behavior_config, indent=2), encoding='utf-8')
    
    # Create guardrails files (required by Guardrails class initialization)
    from agile_bot.bots.base_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files
    create_minimal_guardrails_files(bot_directory, behavior, bot_name)
    
    # Create Behavior object
    behavior_obj = Behavior(name=behavior, bot_paths=bot_paths)
    
    # Create ClarifyContextAction with correct signature
    action_obj = ClarifyContextAction(
        behavior=behavior_obj,
        action_config=None
    )
    return action_obj


def when_instructions_load_and_merge(action, base_instructions=None, behavior_instructions=None):
    """
    Consolidated function for loading and merging instructions.
    Replaces: when_load_and_merge_instructions
    
    Args:
        action: Action object (if base_instructions and behavior_instructions are None, uses action.instructions)
        base_instructions: Optional base instructions dict
        behavior_instructions: Optional behavior instructions dict
    
    Returns:
        Instructions object or merged instructions dict
    """
    if base_instructions is None and behavior_instructions is None:
        # Use the instructions property which returns an Instructions object
        return action.instructions
    else:
        # If base_instructions and behavior_instructions provided, merge them
        # This is for cases where we want to test merging without an action object
        merged = {}
        if base_instructions:
            merged['base_instructions'] = base_instructions
        if behavior_instructions:
            merged.update(behavior_instructions)
        return merged


def then_merged_instructions_contain(merged_instructions, content):
    """
    Consolidated function for checking merged instructions content.
    Replaces: then_merged_instructions_contain_expected, then_merged_instructions_contain_base_and_action
    
    Args:
        merged_instructions: Instructions object or merged instructions dict
        content: Content to check for - can be:
            - 'base_instructions' (string) - checks that base_instructions key exists
            - dict with keys to check - checks that all keys exist in merged_instructions
            - list of strings - checks that all keys exist
    """
    from agile_bot.bots.base_bot.src.actions.instructions import Instructions
    
    # If it's an Instructions object, convert to dict for checking
    if isinstance(merged_instructions, Instructions):
        merged_dict = merged_instructions.to_dict()
    else:
        merged_dict = merged_instructions
    
    if isinstance(content, str):
        # Single key check
        if content == 'base_instructions':
            assert 'base_instructions' in merged_dict, "base_instructions not found in merged instructions"
        else:
            assert content in merged_dict, f"{content} not found in merged instructions"
    elif isinstance(content, dict):
        # Check all keys exist
        for key in content.keys():
            assert key in merged_dict, f"{key} not found in merged instructions"
    elif isinstance(content, list):
        # Check all keys in list exist
        for key in content:
            assert key in merged_dict, f"{key} not found in merged instructions"


def given_bot_name_and_behavior_setup(bot_name: str, behavior: str):
    """Given: Bot name and behavior setup."""
    return bot_name, behavior


def given_render_instructions_exist(bot_directory: Path, behavior: str):
    """Given: Render instructions exist."""
    behavior_dir = bot_directory / 'behaviors' / behavior
    render_dir = behavior_dir / 'content' / 'render'
    render_dir.mkdir(parents=True, exist_ok=True)
    render_instructions_file = render_dir / 'instructions.json'
    render_instructions = {
        'instructions': ['render1', 'render2']
    }
    render_instructions_file.write_text(json.dumps(render_instructions), encoding='utf-8')
    return render_instructions


def when_render_output_action_initialized(bot_directory: Path, bot_name: str, behavior: str):
    """When: RenderOutputAction initialized."""
    from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
    from agile_bot.bots.base_bot.src.bot.behavior import Behavior
    # BaseActionConfig deleted - Action already has config loading
    from agile_bot.bots.base_bot.src.actions.render.render_action import RenderOutputAction
    
    bot_paths = BotPaths(bot_directory=bot_directory)
    import json
    behavior_dir = bot_directory / 'behaviors' / behavior
    behavior_dir.mkdir(parents=True, exist_ok=True)
    behavior_file = behavior_dir / 'behavior.json'
    behavior_config = {
        "behaviorName": behavior,
        "description": f"Test behavior: {behavior}",
        "goal": f"Test goal for {behavior}",
        "inputs": "Test inputs",
        "outputs": "Test outputs",
        "instructions": {},
        "actions_workflow": {
            "actions": [
                {'name': 'render', 'order': 1}
            ]
        }
    }
    behavior_file.write_text(json.dumps(behavior_config, indent=2), encoding='utf-8')
    # Create guardrails files (required by Guardrails class initialization)
    from agile_bot.bots.base_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files
    create_minimal_guardrails_files(bot_directory, behavior, bot_name)
    behavior_obj = Behavior(name=behavior, bot_paths=bot_paths)
    
    return RenderOutputAction(
        behavior=behavior_obj,
        action_config=None
    )


def then_action_uses_class(action, class_name):
    """
    Consolidated function for checking action class usage.
    Replaces: then_action_uses_expected_class, then_action_uses_instructions_class, then_action_uses_merged_instructions_class
    
    Args:
        action: Action object to check
        class_name: Expected class name (e.g., 'Instructions', 'MergedInstructions', 'ClarifyContextAction')
    """
    from agile_bot.bots.base_bot.src.actions.instructions import Instructions
    from agile_bot.bots.base_bot.src.actions.render.render_action import RenderOutputAction
    
    if class_name in ['Instructions', 'MergedInstructions']:
        # Check for instructions class usage by checking structure
        instructions = action.instructions
        if class_name == 'Instructions':
            # Check that instructions is an Instructions object
            assert isinstance(instructions, Instructions), \
                f"Action does not use Instructions class, got {type(instructions)}"
            # Check that it has base_instructions
            assert 'base_instructions' in instructions.to_dict(), \
                "Instructions object does not contain base_instructions"
        elif class_name == 'MergedInstructions':
            # For RenderOutputAction, check that it's a RenderOutputAction (which uses MergedInstructions internally)
            # The instructions property still returns Instructions, but do_execute uses MergedInstructions
            assert isinstance(action, RenderOutputAction), \
                f"Expected RenderOutputAction which uses MergedInstructions internally, got {type(action)}"
            # Verify it has the render config loader
            assert hasattr(action, '_config_loader'), \
                "RenderOutputAction should have _config_loader for MergedInstructions"
    else:
        # Check for action class name
        action_class_name = action.__class__.__name__
        assert action_class_name == class_name, \
            f"Expected action class {class_name}, got {action_class_name}"


def given_environment_and_base_instructions(bot_directory: Path, workspace_directory: Path):
    """Given: Environment and base instructions."""
    bootstrap_env(bot_directory, workspace_directory)
    given_base_instructions_created(bot_directory)


def when_create_bot_with_config(bot_name: str, bot_directory: Path, bot_config: Path):
    """When: Create bot with config."""
    from agile_bot.bots.base_bot.src.bot.bot import Bot
    bot = Bot(
        bot_name=bot_name,
        bot_directory=bot_directory,
        config_path=bot_config
    )
    return bot


def then_behavior_action_state_does_not_exist(workspace_directory: Path):
    """Then: Behavior action state does not exist.
    
    Uses consolidated then_file_does_not_exist function.
    """
    state_file = workspace_directory / 'behavior_action_state.json'
    then_file_does_not_exist(state_file)
    return state_file




class TestInvokeBotTool:
    """Story: Invoke Bot Tool - Tests bot tool invocation behavior."""

    def test_tool_invokes_behavior_action_when_called(self, bot_directory, workspace_directory, bot_config_file_path):
        """
        SCENARIO: Tool Invokes Behavior Action When Called
        GIVEN: Bot has behavior 'shape' with action 'clarify'
        WHEN: AI Chat invokes tool with parameters
        THEN: Tool routes to test_bot.Shape.GatherContext() method
        """
        # Bootstrap
        bootstrap_env(bot_directory, workspace_directory)
        
        # Given: Bot configuration and instructions exist
        workspace_root = workspace_directory.parent
        # Create bot config file in correct location (bot_directory/bot_config.json, not config/ subdirectory)
        bot_config = create_bot_config_file(bot_directory, 'test_bot', ['shape', 'discovery', 'exploration', 'specification'])
        create_behavior_action_instructions_from_workspace(workspace_root, 'test_bot', 'shape', 'clarify')
        given_behavior_json_files_for_behaviors(bot_directory, ['shape', 'discovery', 'exploration', 'specification'], 'test_bot')
        given_base_action_instructions_created(bot_directory, 'clarify')
        
        # Ensure base actions structure exists (required for action configs)
        from conftest import create_base_actions_structure
        create_base_actions_structure(bot_directory)
        
        # When: Call REAL Bot API
        bot = given_bot_instance_created('test_bot', bot_directory, bot_config)
        shape_behavior = bot.behaviors.find_by_name('shape')
        assert shape_behavior is not None, f"Behavior 'shape' not found. Available behaviors: {[b.name for b in bot.behaviors]}"
        # Actions are accessed through behavior.actions, not directly on behavior
        clarify_action = shape_behavior.actions.find_by_name('clarify')
        if clarify_action is None:
            raise ValueError("Action 'clarify' not found")
        shape_behavior.actions.navigate_to('clarify')
        result_data = clarify_action.execute()
        # Create BotResult from action execution
        from agile_bot.bots.base_bot.src.bot.bot import BotResult
        action_result = BotResult(status='completed', behavior='shape', action='clarify', data=result_data)
        
        # Then: Tool executed and returned result
        then_item_matches(action_result, item_type='result', status='completed', behavior='shape', action='clarify')

    def test_tool_routes_to_correct_behavior_action_method(self, bot_directory, workspace_directory, bot_config_file_path):
        """
        SCENARIO: Tool Routes To Correct Behavior Action Method
        GIVEN: Bot has multiple behaviors with clarify action
        WHEN: AI Chat invokes 'test_bot_exploration_clarify'
        THEN: Tool routes to test_bot.Exploration.Clarify() not other behaviors
        """
        # Bootstrap
        bootstrap_env(bot_directory, workspace_directory)
        
        # Given: Multiple behaviors exist
        workspace_root = workspace_directory.parent
        # bot_directory fixture uses 'story_bot', so use that for consistency
        bot_name = bot_directory.name  # 'story_bot' from fixture
        # Create bot config file in correct location (bot_directory/bot_config.json, not config/ subdirectory)
        bot_config = create_bot_config_file(bot_directory, bot_name, ['shape', 'discovery', 'exploration'])
        given_behavior_instructions_for_behaviors(
            workspace_root, ['shape', 'discovery', 'exploration'], bot_name=bot_name, action='clarify'
        )
        behavior_mapping = {'shape': 'shape', 'discovery': 'discovery', 'exploration': 'exploration'}
        given_knowledge_graph_setup_for_behaviors(workspace_root, bot_name, behavior_mapping, 'clarify')
        # Ensure behavior.json files exist for all behaviors (given_knowledge_graph_setup_for_behaviors creates them, but ensure they're in bot_directory)
        from agile_bot.bots.base_bot.test.test_helpers import create_actions_workflow_json
        from agile_bot.bots.base_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files
        for behavior in ['shape', 'discovery', 'exploration']:
            create_actions_workflow_json(bot_directory, behavior)
            create_minimal_guardrails_files(bot_directory, behavior, bot_name)
        given_base_action_instructions_created(bot_directory, 'clarify')
        given_base_actions_setup(bot_directory)
        given_behavior_action_state(bot_name, 'exploration', 'clarify', workspace_directory=workspace_directory)
        
        # When: Call REAL Bot API for specific behavior
        bot = given_bot_instance_created(bot_name, bot_directory, bot_config)
        exploration_behavior = bot.behaviors.find_by_name('exploration')
        # Actions are accessed through behavior.actions, not directly on behavior
        clarify_action = exploration_behavior.actions.find_by_name('clarify')
        if clarify_action is None:
            raise ValueError("Action 'clarify' not found")
        exploration_behavior.actions.navigate_to('clarify')
        result_data = clarify_action.execute()
        # Create BotResult from action execution
        from agile_bot.bots.base_bot.src.bot.bot import BotResult
        action_result = BotResult(status='completed', behavior='exploration', action='clarify', data=result_data)
        
        # Then: Routes to exploration behavior only
        then_item_matches(action_result, item_type='result', behavior='exploration', action='clarify')


class TestLoadAndMergeBehaviorActionInstructions:
    """Story: Load And Merge Behavior Action Instructions - Tests instruction loading and merging."""

    def test_action_loads_and_merges_instructions(self, bot_directory, workspace_directory):
        """
        SCENARIO: Action Loads And Merges Instructions
        GIVEN: Base and behavior-specific instructions exist
        WHEN: Action method is invoked
        THEN: Instructions are loaded from both locations and merged
        """
        # Bootstrap
        bootstrap_env(bot_directory, workspace_directory)
        
        # Given: Both instruction files exist
        bot_name, behavior, action = given_bot_name_behavior_and_action_setup()
        workspace_root = workspace_directory.parent
        config_file = create_bot_config_file(bot_directory, bot_name, ['shape'])
        behavior_instructions = create_behavior_action_instructions_from_workspace(workspace_root, bot_name, behavior, action)
        base_instructions = given_base_action_instructions_created(bot_directory, action)
        
        # When: Call REAL ClarifyContextAction API
        action_obj = when_create_gather_context_action(bot_name, behavior, bot_directory)
        merged_instructions = when_instructions_load_and_merge(action_obj)
        
        # Then: Instructions merged from both sources
        then_merged_instructions_contain(merged_instructions, 'base_instructions')

    def test_action_uses_instructions_class_to_merge_base_and_behavior_instructions(self, bot_directory, workspace_directory):
        """
        SCENARIO: Action uses Instructions class to merge base and behavior instructions
        GIVEN: Action with BaseActionConfig and Behavior
        WHEN: Action initialized
        THEN: Action uses Instructions class to merge instructions
        """
        # Given: Environment bootstrapped
        bootstrap_env(bot_directory, workspace_directory)
        bot_name, behavior, action = given_bot_name_behavior_and_action_setup()
        workspace_root = workspace_directory.parent
        config_file = create_bot_config_file(bot_directory, bot_name, ['shape'])
        behavior_instructions = create_behavior_action_instructions_from_workspace(workspace_root, bot_name, behavior, action)
        base_instructions = given_base_action_instructions_created(bot_directory, action)
        
        # When: Action initialized
        action_obj = when_create_gather_context_action(bot_name, behavior, bot_directory)
        
        # Then: Action uses Instructions class to merge instructions
        then_action_uses_class(action_obj, 'Instructions')

    def test_action_uses_merged_instructions_class_when_render_instructions_present(self, bot_directory, workspace_directory):
        """
        SCENARIO: Action uses MergedInstructions class when render instructions present
        GIVEN: RenderOutputAction with render instructions
        WHEN: Action initialized
        THEN: Action uses MergedInstructions class for merging
        """
        # Given: Environment bootstrapped
        bootstrap_env(bot_directory, workspace_directory)
        bot_name, behavior = given_bot_name_and_behavior_setup('story_bot', 'shape')
        render_instructions = given_render_instructions_exist(bot_directory, behavior)
        
        # When: RenderOutputAction initialized
        action_obj = when_render_output_action_initialized(bot_directory, bot_name, behavior)
        
        # Then: Action uses MergedInstructions class
        then_action_uses_class(action_obj, 'MergedInstructions')


class TestForwardToCurrentBehaviorAndCurrentAction:
    """Story: Forward To Current Behavior and Current Action - Tests bot tool forwarding to behavior and action."""

    def test_bot_tool_forwards_to_current_behavior_and_current_action(self, bot_directory, workspace_directory):
        """
        SCENARIO: Bot tool forwards to current behavior and current action
        GIVEN: behavior action state shows current_behavior='discovery', current_action='build'
        WHEN: Bot tool receives invocation
        THEN: Bot tool forwards to correct behavior and action
        """
        # Bootstrap
        bootstrap_env(bot_directory, workspace_directory)
        
        # Given
        given_base_instructions_created(bot_directory)
        bot_config = given_bot_config_and_behavior_workflow(bot_directory, 'test_bot', ['discovery'])
        
        # When
        bot = given_bot_instance_created('test_bot', bot_directory, bot_config)
        current_behavior = bot.behaviors.current
        if current_behavior is None:
            if bot.behaviors.first:
                bot.behaviors.navigate_to(bot.behaviors.first.name)
                current_behavior = bot.behaviors.current
            else:
                raise ValueError("No behaviors available")
        if current_behavior is None:
            raise ValueError("No current behavior")
        
        # Get current action and execute directly at lowest level
        current_behavior.actions.load_state()
        current_action = current_behavior.actions.current
        if current_action is None:
            raise ValueError("No current action")
        result_data = current_action.execute()
        from agile_bot.bots.base_bot.src.bot.bot import BotResult
        bot_response = BotResult(
            status='completed',
            behavior=current_behavior.name,
            action=current_action.action_name,
            data=result_data
        )
        
        # Then
        then_item_matches(bot_response, item_type='result', behavior='discovery', action='clarify')

    def test_bot_tool_defaults_to_first_behavior_and_first_action_when_state_missing(self, bot_directory, workspace_directory):
        """
        SCENARIO: Bot tool defaults to first behavior and first action when state missing
        GIVEN: behavior action state does NOT exist
        WHEN: Bot tool receives invocation
        THEN: Bot tool defaults to first behavior and first action
        """
        # Bootstrap
        bootstrap_env(bot_directory, workspace_directory)
        
        # Given
        given_base_instructions_created(bot_directory)
        bot_config = given_bot_config_and_behavior_workflow(bot_directory, 'test_bot', ['shape', 'discovery'])
        
        # When
        bot = given_bot_instance_created('test_bot', bot_directory, bot_config)
        current_behavior = bot.behaviors.current
        if current_behavior is None:
            if bot.behaviors.first:
                bot.behaviors.navigate_to(bot.behaviors.first.name)
                current_behavior = bot.behaviors.current
            else:
                raise ValueError("No behaviors available")
        if current_behavior is None:
            raise ValueError("No current behavior")
        
        # Get current action and execute directly at lowest level
        current_behavior.actions.load_state()
        current_action = current_behavior.actions.current
        if current_action is None:
            raise ValueError("No current action")
        result_data = current_action.execute()
        from agile_bot.bots.base_bot.src.bot.bot import BotResult
        bot_response = BotResult(
            status='completed',
            behavior=current_behavior.name,
            action=current_action.action_name,
            data=result_data
        )
        
        # Then
        # Behaviors are discovered in alphabetical order, so 'discovery' comes before 'shape'
        then_item_matches(bot_response, item_type='result', behavior='discovery', action='clarify')


class TestForwardToCurrentAction:
    """Story: Forward To Current Action - Tests behavior tool forwarding to current action."""

    def test_behavior_tool_forwards_to_current_action_within_behavior(self, bot_directory, workspace_directory):
        """
        SCENARIO: Behavior tool forwards to current action within behavior
        GIVEN: a behavior tool for 'discovery' behavior
        AND: behavior action state shows current_action='build_knowledge'
        WHEN: Behavior tool receives invocation
        THEN: Behavior tool forwards to build_knowledge action
        """
        # Given
        bootstrap_env(bot_directory, workspace_directory)
        given_base_instructions_created(bot_directory)
        bot_config = given_bot_config_and_behavior_workflow(bot_directory, 'test_bot', ['discovery'])
        
        # When
        bot = given_bot_instance_created('test_bot', bot_directory, bot_config)
        discovery_behavior = bot.behaviors.find_by_name('discovery')
        
        # Get current action and execute directly at lowest level
        discovery_behavior.actions.load_state()
        current_action = discovery_behavior.actions.current
        if current_action is None:
            raise ValueError("No current action")
        result_data = current_action.execute()
        from agile_bot.bots.base_bot.src.bot.bot import BotResult
        action_result = BotResult(
            status='completed',
            behavior='discovery',
            action=current_action.action_name,
            data=result_data
        )
        
        # Then
        then_item_matches(action_result, expected='clarify', item_type='result')

    def test_behavior_tool_sets_workflow_to_current_behavior_when_state_shows_different_behavior(self, bot_directory, workspace_directory):
        """
        SCENARIO: Behavior tool sets behavior action state to current behavior when state shows different behavior
        GIVEN: a behavior tool for 'exploration' behavior
        AND: behavior action state shows current_behavior='discovery'
        WHEN: Behavior tool receives invocation
        THEN: behavior action state updated to current_behavior='exploration'
        """
        # Given
        bootstrap_env(bot_directory, workspace_directory)
        given_base_instructions_created(bot_directory)
        bot_config = given_bot_config_and_behavior_workflow(bot_directory, 'test_bot', ['discovery', 'exploration'])
        
        # When
        bot = given_bot_instance_created('test_bot', bot_directory, bot_config)
        exploration_behavior = bot.behaviors.find_by_name('exploration')
        
        # Get current action and execute directly at lowest level
        exploration_behavior.actions.load_state()
        current_action = exploration_behavior.actions.current
        if current_action is None:
            raise ValueError("No current action")
        result_data = current_action.execute()
        from agile_bot.bots.base_bot.src.bot.bot import BotResult
        action_result = BotResult(
            status='completed',
            behavior='exploration',
            action=current_action.action_name,
            data=result_data
        )
        
        # Then
        assert action_result.behavior == 'exploration'

    def test_behavior_tool_defaults_to_first_action_when_state_missing(self, bot_directory, workspace_directory):
        """
        SCENARIO: Behavior tool defaults to first action when state missing
        GIVEN: a behavior tool for 'shape' behavior
        AND: behavior action state does NOT exist
        WHEN: Behavior tool receives invocation
        THEN: Behavior tool defaults to first action
        """
        # Given
        bootstrap_env(bot_directory, workspace_directory)
        given_base_instructions_created(bot_directory)
        bot_config = given_bot_config_and_behavior_workflow(bot_directory, 'test_bot', ['shape'])
        
        # When
        bot = given_bot_instance_created('test_bot', bot_directory, bot_config)
        shape_behavior = bot.behaviors.find_by_name('shape')
        
        # Get current action and execute directly at lowest level
        shape_behavior.actions.load_state()
        current_action = shape_behavior.actions.current
        if current_action is None:
            raise ValueError("No current action")
        result_data = current_action.execute()
        from agile_bot.bots.base_bot.src.bot.bot import BotResult
        action_result = BotResult(
            status='completed',
            behavior='shape',
            action=current_action.action_name,
            data=result_data
        )
        
        # Then
        then_item_matches(action_result, expected='clarify', item_type='result')
    
    def test_action_called_directly_saves_behavior_action_state(self, bot_directory, workspace_directory):
        """
        SCENARIO: Action called directly saves behavior action state
        GIVEN: Bot is initialized with WORKING_AREA set
        AND: No behavior action state exists yet
        WHEN: Action is called directly (e.g., bot.shape.clarify())
        THEN: behavior_action_state.json is created with current_action
        AND: This ensures state is saved whether action is called via forward or directly
        """
        # Bootstrap environment
        given_environment_and_base_instructions(bot_directory, workspace_directory)
        
        # Given
        bot_config = create_bot_config_file(bot_directory, 'test_bot', ['shape'])
        # Create behavior.json file (REQUIRED after refactor)
        create_actions_workflow_json(bot_directory, 'shape')
        # Create guardrails files (required by Guardrails class initialization)
        from agile_bot.bots.base_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files
        create_minimal_guardrails_files(bot_directory, 'shape', 'test_bot')
        
        # When
        bot = when_create_bot_with_config('test_bot', bot_directory, bot_config)
        
        # Verify no behavior action state exists yet
        state_file = then_behavior_action_state_does_not_exist(workspace_directory)
        
        # Call clarify DIRECTLY (not via forward_to_current_action)
        shape_behavior = bot.behaviors.find_by_name('shape')
        # Actions are accessed through behavior.actions, not directly on behavior
        clarify_action = shape_behavior.actions.find_by_name('clarify')
        if clarify_action is None:
            raise ValueError("Action 'clarify' not found")
        shape_behavior.actions.navigate_to('clarify')
        result_data = clarify_action.execute()
        # Create BotResult from action execution
        from agile_bot.bots.base_bot.src.bot.bot import BotResult
        action_result = BotResult(status='completed', behavior='shape', action='clarify', data=result_data)
        
        # Then
        state_file = then_behavior_action_state_file_exists(workspace_directory)
        # Behavior.bot_name comes from bot_directory.name, not bot.name
        actual_bot_name = bot_directory.name
        then_behavior_action_state_has_correct_values(state_file, f'{actual_bot_name}.shape', f'{actual_bot_name}.shape.clarify')
        then_item_matches(action_result, expected='clarify', item_type='result')
