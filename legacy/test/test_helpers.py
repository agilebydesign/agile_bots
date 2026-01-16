"""
Common Test Helpers - Used Across Multiple Epics

This file contains helper functions that are used across MULTIPLE epics and sub-epics.
These are truly common/shared utilities, not sub-epic-specific helpers.

NOTE: This file does not follow the test_<sub_epic_name>.py naming convention because
it contains common helpers spanning multiple epics. Sub-epic-specific helpers should
be placed in test_<sub_epic_name>_helpers.py files.

For sub-epic-specific helpers, see:
- test_generate_mcp_tools.py (Generate MCP Tools sub-epic - helpers merged into main file)
- test_perform_behavior_action.py (Perform Behavior Action sub-epic - helpers merged into main file)
"""
import json
import os
from pathlib import Path
import pytest
from agile_bot.bots.base_bot.src.bot.bot import Behavior


# ============================================================================
# PATH HELPERS - Centralized path calculations
# ============================================================================

def get_bot_dir(repo_root: Path, bot_name: str) -> Path:
    """Get bot directory path (where bot code lives)."""
    return repo_root / 'agile_bot' / 'bots' / bot_name

def get_activity_log_path(workspace_dir: Path) -> Path:
    """Get activity_log.json path (in workspace directory)."""
    return workspace_dir / 'activity_log.json'

def get_behavior_action_state_path(workspace_dir: Path) -> Path:
    """Get behavior_action_state.json path (in workspace directory)."""
    return workspace_dir / 'behavior_action_state.json'

def get_bot_config_path(bot_dir: Path) -> Path:
    """Get bot config path (in bot directory)."""
    return bot_dir / 'config' / 'bot_config.json'

def get_behavior_dir(bot_dir: Path, behavior: str) -> Path:
    """Get behavior directory path (in bot directory)."""
    return bot_dir / 'behaviors' / behavior

def get_base_bot_dir(repo_root: Path) -> Path:
    """Get test_base_bot directory path for tests (not production base_bot)."""
    return repo_root / 'agile_bot' / 'bots' / 'test_base_bot'

def get_base_actions_dir(repo_root: Path) -> Path:
    """Get base_actions directory path from test_base_bot."""
    return get_base_bot_dir(repo_root) / 'base_actions'

def get_test_base_actions_dir(bot_directory: Path) -> Path:
    """Get base_actions directory, redirecting base_bot to test_base_bot.
    
    If bot_directory is base_bot (production), redirects to test_base_bot/base_actions.
    Otherwise, uses bot_directory/base_actions.
    """
    # If bot_directory is base_bot, redirect to test_base_bot
    if bot_directory.name == 'base_bot':
        # Infer repo_root from bot_directory: agile_bot/bots/base_bot -> repo_root
        repo_root = bot_directory.parent.parent.parent
        return get_base_actions_dir(repo_root)
    # Otherwise use the bot_directory's base_actions
    return bot_directory / 'base_actions'

def get_base_bot_rules_dir(repo_root: Path) -> Path:
    """Get base_bot rules directory path."""
    return get_base_bot_dir(repo_root) / 'rules'

def bootstrap_env(bot_dir: Path, workspace_dir: Path):
    """Bootstrap environment variables for tests."""
    os.environ['BOT_DIRECTORY'] = str(bot_dir)
    os.environ['WORKING_AREA'] = str(workspace_dir)

def update_bot_config_with_working_area(bot_dir: Path, workspace_dir: Path) -> Path:
    """Update bot_config.json with WORKING_AREA field."""
    # Create bot_config.json in root (matches actual code behavior)
    config_path = bot_dir / 'bot_config.json'
    
    # Load existing config if it exists, otherwise create new
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, FileNotFoundError):
            config = {}
    else:
        config = {}
    
    # Add WORKING_AREA
    config['WORKING_AREA'] = str(workspace_dir)
    config_path.write_text(json.dumps(config, indent=2), encoding='utf-8')
    return config_path

# Import conftest functions when needed: from conftest import create_bot_config_file

def create_activity_log_file(workspace_dir: Path) -> Path:
    """Create activity log file in workspace directory."""
    log_file = get_activity_log_path(workspace_dir)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text(json.dumps({'_default': {}}), encoding='utf-8')
    return log_file

# Import conftest functions when needed: from conftest import create_workflow_state_file

def create_guardrails_files(bot_dir: Path, behavior: str, questions: list, evidence: list) -> tuple:
    """Create guardrails files in behavior folder with specific content."""
    guardrails_dir = get_behavior_dir(bot_dir, behavior) / 'guardrails' / 'required_context'
    guardrails_dir.mkdir(parents=True, exist_ok=True)
    
    questions_file = guardrails_dir / 'key_questions.json'
    questions_file.write_text(json.dumps({'questions': questions}), encoding='utf-8')
    
    evidence_file = guardrails_dir / 'evidence.json'
    evidence_file.write_text(json.dumps({'evidence': evidence}), encoding='utf-8')
    
    return questions_file, evidence_file

def create_planning_guardrails(bot_dir: Path, behavior: str, assumptions: list, criteria: dict) -> tuple:
    """Create planning guardrails (alias for create_strategy_guardrails for backward compatibility)."""
    return create_strategy_guardrails(bot_dir, behavior, assumptions, criteria)

def create_strategy_guardrails(bot_dir: Path, behavior: str, assumptions: list, criteria: dict) -> tuple:
    """Create strategy guardrails in behavior folder."""
    # Strategy class expects guardrails/strategy/ directory (not planning/)
    guardrails_dir = get_behavior_dir(bot_dir, behavior) / 'guardrails' / 'strategy'
    guardrails_dir.mkdir(parents=True, exist_ok=True)
    
    assumptions_file = guardrails_dir / 'typical_assumptions.json'
    assumptions_file.write_text(json.dumps({'assumptions': assumptions}), encoding='utf-8')
    
    criteria_dir = guardrails_dir / 'strategy_criteria'
    criteria_dir.mkdir(exist_ok=True)
    criteria_file = criteria_dir / 'test_criteria.json'
    criteria_file.write_text(json.dumps(criteria), encoding='utf-8')
    
    return assumptions_file, criteria_file

def create_knowledge_graph_template(bot_dir: Path, behavior: str, template_name: str) -> Path:
    """Create knowledge graph template in behavior folder."""
    kg_dir = get_behavior_dir(bot_dir, behavior) / 'content' / 'knowledge_graph'
    kg_dir.mkdir(parents=True, exist_ok=True)
    
    template_file = kg_dir / f'{template_name}.json'
    template_file.write_text(json.dumps({'template': 'knowledge_graph'}), encoding='utf-8')
    return template_file

def create_validation_rules(bot_dir: Path, behavior: str, rules: list) -> Path:
    """Create validation rules in behavior folder."""
    rules_dir = get_behavior_dir(bot_dir, behavior) / '3_rules'
    rules_dir.mkdir(parents=True, exist_ok=True)
    
    rules_file = rules_dir / 'validation_rules.json'
    rules_file.write_text(json.dumps({'rules': rules}), encoding='utf-8')
    return rules_file

def create_common_rules(repo_root: Path, rules: list) -> Path:
    """Create common rules in base_bot directory."""
    rules_dir = get_base_bot_rules_dir(repo_root)
    rules_dir.mkdir(parents=True, exist_ok=True)
    
    rules_file = rules_dir / 'common_rules.json'
    rules_file.write_text(json.dumps({'rules': rules}), encoding='utf-8')
    return rules_file

# ============================================================================
# BASE INSTRUCTIONS HELPERS - Epic-level helpers for Invoke Bot epic
# ============================================================================

def create_base_instructions(bot_directory: Path):
    """Create base action configs in bot_directory (no fallback to repo root).
    
    If bot_directory is base_bot, redirects to test_base_bot/base_actions.
    """
    base_actions = get_test_base_actions_dir(bot_directory)
    # Action folders no longer have number prefixes
    actions = ['clarify', 'strategy', 'build', 'validate', 'render']
    orders = [1, 2, 3, 4, 5]
    next_actions = ['strategy', 'build', 'validate', 'render', None]
    
    for action, order, next_action in zip(actions, orders, next_actions):
        action_dir = base_actions / action
        action_dir.mkdir(parents=True, exist_ok=True)
        config = {
            'name': action,
            'workflow': True,
            'order': order,
            'instructions': [f'{action} base instructions']
        }
        if next_action:
            config['next_action'] = next_action
        config_file = action_dir / 'action_config.json'
        config_file.write_text(json.dumps(config), encoding='utf-8')


def create_base_action_instructions(bot_directory: Path, action: str) -> Path:
    """Create base action config for specific action in bot_directory (no fallback).
    
    If bot_directory is base_bot, redirects to test_base_bot/base_actions.
    """
    base_actions_dir = get_test_base_actions_dir(bot_directory)
    
    # Action folders no longer have number prefixes
    action_dir = base_actions_dir / action
    action_dir.mkdir(parents=True, exist_ok=True)
    
    config = {
        'name': action,
        'workflow': True,
        'order': 1,
        'instructions': [f'{action} base instructions']
    }
    config_file = action_dir / 'action_config.json'
    config_file.write_text(json.dumps(config), encoding='utf-8')
    return config_file


def create_behavior_folder(bot_dir: Path, folder_name: str) -> Path:
    """Create behavior folder in bot directory."""
    behavior_dir = get_behavior_dir(bot_dir, folder_name)
    behavior_dir.mkdir(parents=True, exist_ok=True)
    return behavior_dir

def create_behavior_action_instructions(bot_dir: Path, behavior: str, action: str) -> Path:
    """Create behavior-specific action instructions."""
    instructions_dir = get_behavior_dir(bot_dir, behavior) / action
    instructions_dir.mkdir(parents=True, exist_ok=True)
    
    instructions_file = instructions_dir / 'instructions.json'
    instructions_file.write_text(json.dumps({
        'instructions': [f'{behavior}.{action} specific instructions']
    }), encoding='utf-8')
    return instructions_file


def create_actions_workflow_json(bot_directory: Path, behavior_name: str, actions: list = None, order: int = None) -> Path:
    """Given step: Behavior exists with actions workflow.
    
    Creates behavior.json file for a behavior (new format).
    
    Used across multiple epics:
    - Generate MCP Tools (Build Agile Bots epic)
    - Generate CLI (Build Agile Bots epic)
    - Invoke Bot (Invoke Bot epic)
    - Execute Behavior Actions (Execute Behavior Actions epic)
    - Validate Rules (Execute Behavior Actions epic)
    
    Args:
        bot_directory: Path to bot directory
        behavior_name: Name of the behavior
        actions: Optional list of action configs. If None, creates default actions.
        order: Optional order number for behavior. If None, behavior.json will not have order field.
    
    """
    import json
    behavior_dir = bot_directory / 'behaviors' / behavior_name
    behavior_dir.mkdir(parents=True, exist_ok=True)
    
    if actions is None:
        # Standard workflow order - using actual action names: clarify, strategy, build, validate, render
        # Note: 'build' action class doesn't exist yet, so it's excluded until BuildAction is implemented
        actions = [
            {
                "name": "clarify",
                "order": 1,
                "next_action": "strategy",
                "instructions": [
                    f"Follow agile_bot/bots/test_base_bot/base_actions/clarify/action_config.json",
                    f"Test instructions for clarify in {behavior_name}"
                ]
            },
            {
                "name": "strategy",
                "order": 2,
                "next_action": "validate",
                "instructions": [
                    f"Follow agile_bot/bots/test_base_bot/base_actions/strategy/action_config.json",
                    f"Test instructions for strategy in {behavior_name}"
                ]
            },
            {
                "name": "validate",
                "order": 3,
                "next_action": "render",
                "instructions": [
                    f"Follow agile_bot/bots/test_base_bot/base_actions/validate/action_config.json",
                    f"Test instructions for validate in {behavior_name}"
                ]
            },
            {
                "name": "render",
                "order": 4,
                "instructions": [
                    f"Follow agile_bot/bots/test_base_bot/base_actions/render/action_config.json",
                    f"Test instructions for render in {behavior_name}"
                ]
            }
        ]
    
    # Create behavior.json with all sections matching production structure
    behavior_config = {
        "behaviorName": behavior_name.split('_')[-1] if '_' in behavior_name and behavior_name[0].isdigit() else behavior_name,
        "description": f"Test behavior: {behavior_name}",
        "goal": f"Test goal for {behavior_name}",
        "inputs": "Test inputs",
        "outputs": "Test outputs",
        "baseActionsPath": "agile_bot/bots/test_base_bot/base_actions",
        "instructions": [
            f"**BEHAVIOR WORKFLOW INSTRUCTIONS:**",
            "",
            f"Test instructions for {behavior_name}."
        ],
        "actions_workflow": {
            "actions": actions
        },
        "trigger_words": {
            "description": f"Trigger words for {behavior_name}",
            "patterns": [f"test.*{behavior_name}"]
        }
    }
    
    # Add order field if provided (matches production structure)
    if order is not None:
        behavior_config["order"] = order
    
    behavior_file = behavior_dir / 'behavior.json'
    behavior_file.write_text(json.dumps(behavior_config, indent=2), encoding='utf-8')
    return behavior_file

def create_base_actions_structure(bot_directory: Path):
    """Create base actions directory structure in bot_directory (no fallback).
    
    Creates base_actions directory with action_config.json files.
    
    If bot_directory is base_bot, redirects to test_base_bot/base_actions.
    
    NOTE: This is kept for backward compatibility. New tests should use actions-workflow.json instead.
    """
    base_actions_dir = get_test_base_actions_dir(bot_directory)
    
    # Actions no longer have number prefixes - use clean names
    actions = [
        ('clarify', 1, 'strategy'),
        ('strategy', 2, 'build'),
        ('build', 3, 'validate'),
        ('validate', 4, 'render'),
        ('render', 5, None)
    ]
    
    for action_name, order, next_action in actions:
        action_dir = base_actions_dir / action_name
        action_dir.mkdir(parents=True, exist_ok=True)
        
        # Create action_config.json
        config = {
            'name': action_name,
            'workflow': True,
            'order': order
        }
        if next_action:
            config['next_action'] = next_action
        
        (action_dir / 'action_config.json').write_text(json.dumps(config), encoding='utf-8')
    

def given_activity_log(workspace_directory: Path, entries: list = None, **params):
    """
    Consolidated function for creating activity log with entries.
    Replaces: given_activity_log_with_entries, given_activity_log_contains_entries,
    given_activity_log_with_multiple_entries
    
    Args:
        workspace_directory: Workspace directory path
        entries: List of activity log entries (if None, creates default multiple entries)
        **params: Additional parameters:
            - return_file: If True, return log file path (default: False)
    
    Returns:
        Log file Path if return_file=True, otherwise None
    """
    workspace_directory.mkdir(parents=True, exist_ok=True)
    log_file = workspace_directory / 'activity_log.json'
    from tinydb import TinyDB
    
    with TinyDB(log_file) as db:
        if entries is None:
            # Default: create multiple entries (for given_activity_log_with_multiple_entries)
            db.insert({'action_state': 'story_bot.shape.render', 'timestamp': '09:00'})
            db.insert({'action_state': 'story_bot.discovery.render', 'timestamp': '10:00'})
        else:
            # Use provided entries
            for entry in entries:
                db.insert(entry)
    
    return log_file if params.get('return_file', False) else None


def read_activity_log(workspace_dir: Path) -> list:
    """Read activity log from workspace directory."""
    log_file = get_activity_log_path(workspace_dir)
    from tinydb import TinyDB
    with TinyDB(log_file) as db:
        return db.all()

# verify_workflow_saves_completed_action, then_workflow_current_state_is, then_completed_actions_include,
# _create_validate_action, _create_gather_context_action, _create_action_with_provided_class,
# _create_action_with_default_class, given_environment_bootstrapped_and_action_initialized
# - These are epic-level helpers for "Execute Behavior Actions" epic, moved to test_execute_behavior_actions.py
# Import from: from agile_bot.bots.base_bot.test.test_execute_behavior_actions import ...

# ============================================================================
# COMMON GIVEN/WHEN/THEN HELPERS - Used across multiple test files
# ============================================================================

def given_bot_name_and_behavior_setup(bot_name: str = 'story_bot', behavior: str = 'shape'):
    """Given: Bot name and behavior setup.
    
    """
    return bot_name, behavior


def given_bot_name_and_behaviors_setup(bot_name: str = 'story_bot', behaviors: list = None):
    """Given: Bot name and behaviors setup (plural behaviors).
    
    """
    if behaviors is None:
        behaviors = ['shape']
    return bot_name, behaviors

# ============================================================================
# BOT INSTANCE HELPERS - Epic-level helpers for Invoke Bot epic
# ============================================================================

def given_bot_instance_created(bot_name: str, bot_directory: Path, config_path: Path):
    """Given: Bot instance created."""
    from agile_bot.bots.base_bot.src.bot.bot import Bot
    return Bot(bot_name=bot_name, bot_directory=bot_directory, config_path=config_path)


def when_bot_is_created(bot_name: str, bot_directory: Path, config_path: Path):
    """When: Bot is created."""
    from agile_bot.bots.base_bot.src.bot.bot import Bot
    return Bot(bot_name=bot_name, bot_directory=bot_directory, config_path=config_path)



def then_activity_logged_with_action_state(log_file_or_workspace: Path, expected_action_state: str):
    """Then: Activity logged with expected action_state.
    
    Accepts either log_file Path or workspace_directory Path.
    """
    from tinydb import TinyDB
    if (log_file_or_workspace / 'activity_log.json').exists():
        # It's a workspace directory
        log_file = log_file_or_workspace / 'activity_log.json'
    else:
        # It's already a log file
        log_file = log_file_or_workspace
    
    with TinyDB(log_file) as db:
        entries = db.all()
        # Debug: print all entries if assertion fails
        if not any(entry.get('action_state') == expected_action_state for entry in entries):
            actual_states = [entry.get('action_state') for entry in entries]
            raise AssertionError(
                f"Expected action_state '{expected_action_state}' not found in activity log. "
                f"Actual entries: {actual_states}"
            )

def then_completion_entry_logged_with_outputs(log_file_or_workspace: Path, expected_outputs: dict = None, expected_duration: int = None):
    """Then: Completion entry logged with outputs and duration.
    
    Accepts either log_file Path or workspace_directory Path.
    """
    from tinydb import TinyDB
    if (log_file_or_workspace / 'activity_log.json').exists():
        # It's a workspace directory
        log_file = log_file_or_workspace / 'activity_log.json'
    else:
        # It's already a log file
        log_file = log_file_or_workspace
    
    with TinyDB(log_file) as db:
        entries = db.all()
        completion_entry = next((e for e in entries if 'outputs' in e), None)
        assert completion_entry is not None
        if expected_outputs is not None:
            assert completion_entry['outputs'] == expected_outputs
        if expected_duration is not None:
            assert completion_entry['duration'] == expected_duration

# ============================================================================
# CONSOLIDATED GIVEN/WHEN/THEN HELPERS - Previously duplicated across files
# ============================================================================

def given_directory_created(directory, **params):
    """
    Consolidated function for creating directories.
    Replaces: given_workspace_directory_created, given_docs_stories_directory_exists,
    given_knowledge_graph_directory_created, given_docs_directory_created,
    given_knowledge_graph_directory_for_prioritization, given_behavior_render_directory_created
    
    Args:
        directory: Base directory path (workspace_directory, bot_directory, etc.)
        **params: Additional parameters:
            - directory_type: Type of directory ('workspace', 'docs_stories', 'knowledge_graph',
                            'docs', 'knowledge_graph_prioritization', 'behavior_render')
            - behavior: Behavior name (required for knowledge_graph, behavior_render)
    
    Returns:
        Created directory Path (always returns path for non-workspace types)
    """
    directory_type = params.get('directory_type', 'workspace')
    behavior = params.get('behavior')
    
    if directory_type == 'workspace':
        directory.mkdir(parents=True, exist_ok=True)
        return directory
    
    elif directory_type == 'docs_stories':
        docs_dir = directory / 'docs' / 'stories'
        docs_dir.mkdir(parents=True, exist_ok=True)
        return docs_dir
    
    elif directory_type == 'knowledge_graph':
        if not behavior:
            raise ValueError("behavior parameter required for knowledge_graph directory")
        behavior_dir = directory / 'behaviors' / behavior
        kg_dir = behavior_dir / 'content' / 'knowledge_graph'
        kg_dir.mkdir(parents=True, exist_ok=True)
        return kg_dir
    
    elif directory_type == 'docs':
        docs_dir = directory / "docs" / "stories"
        docs_dir.mkdir(parents=True, exist_ok=True)
        return docs_dir
    
    elif directory_type == 'knowledge_graph_prioritization':
        if not behavior:
            raise ValueError("behavior parameter required for knowledge_graph_prioritization directory")
        behavior_dir = directory / 'behaviors' / behavior
        kg_dir = behavior_dir / 'content' / 'knowledge_graph'
        kg_dir.mkdir(parents=True, exist_ok=True)
        return kg_dir
    
    elif directory_type == 'behavior_render':
        if not behavior:
            raise ValueError("behavior parameter required for behavior_render directory")
        behavior_dir = directory / 'behaviors' / behavior
        render_dir = behavior_dir / 'content' / 'render'
        render_dir.mkdir(parents=True, exist_ok=True)
        # instructions.json is mandatory when render folder exists
        instructions_file = render_dir / 'instructions.json'
        if not instructions_file.exists():
            instructions_file.write_text(
                json.dumps({
                    'behaviorName': behavior,
                    'instructions': [f'Render outputs for {behavior} behavior']
                }),
                encoding='utf-8'
            )
        return render_dir
    
    else:
        raise ValueError(f"Unknown directory_type: {directory_type}")


def given_file_created(directory: Path, filename: str, content, file_type: str = 'json') -> Path:
    """Consolidated file creation helper.
    
    Replaces:
    - given_behavior_json_file_created
    - given_story_graph_file_exists
    - given_story_graph_file_with_content
    - given_story_graph_file_with_invalid_json
    - given_test_file_created_with_content
    - given_test_file_for_validate_code_files_action
    - given_source_file_for_validate_code_files_action
    - given_knowledge_graph_file_created
    - given_story_graph_file_created
    - given_existing_story_graph_created
    - given_knowledge_graph_config_file_created
    - given_knowledge_graph_template_file_created
    - given_knowledge_graph_config_for_increments_created
    - given_knowledge_graph_template_for_increments_created
    - given_knowledge_graph_config_for_story_graph_increments
    - given_knowledge_graph_template_for_increments
    - given_knowledge_graph_template_with_schema_created
    - given_test_file_for_scanner_type
    - when_create_knowledge_behavior_file
    - when_create_code_behavior_file
    - when_create_behavior_file_with_config
    
    Args:
        directory: Directory where file should be created
        filename: Name of the file
        content: Content to write (dict for JSON, str for text)
        file_type: 'json' or 'text' (default: 'json')
    
    Returns:
        Path to created file
    """
    directory.mkdir(parents=True, exist_ok=True)
    file_path = directory / filename
    
    if file_type == 'json':
        if isinstance(content, dict):
            file_path.write_text(json.dumps(content, indent=2), encoding='utf-8')
        elif isinstance(content, str):
            # If content is already a JSON string, write it directly
            file_path.write_text(content, encoding='utf-8')
        else:
            file_path.write_text(json.dumps(content, indent=2), encoding='utf-8')
    else:
        # Text file
        file_path.write_text(str(content), encoding='utf-8')
    
    return file_path


def given_files_created(directory: Path, filenames: list, file_type: str = 'json') -> list:
    """Consolidates: given_test_files_for_validate_code_files_action, given_source_files_for_validate_code_files_action
    
    Given: Multiple files created in the specified directory.
    
    Args:
        directory: Directory where files should be created
        filenames: List of tuples (filename, content) or list of filenames (if content is None, creates empty files)
        file_type: 'json' or 'text' (default: 'json')
    
    Returns:
        List of Path objects for created files
    """
    created_files = []
    for item in filenames:
        if isinstance(item, tuple):
            filename, content = item
        else:
            filename = item
            content = '' if file_type == 'text' else {}
        
        file_path = given_file_created(directory, filename, content, file_type=file_type)
        created_files.append(file_path)
    
    return created_files


def given_environment_setup(bot_dir: Path, workspace_dir: Path, behaviors: list = None, setup_type: str = 'standard', bot_name: str = 'story_bot', **kwargs) -> Path:
    """Consolidated environment setup helper.
    
    Replaces:
    - given_test_environment_setup
    - given_bot_name_behaviors_and_config_setup
    - given_bot_config_and_behavior_setup
    - given_bot_environment_bootstrapped
    - when_bot_and_workflow_file_created
    - given_environment_and_behavior_directory
    - given_environment_and_bot
    - given_environment_bootstrapped_for_workflow_resume
    - given_environment_setup_for_final_action_test
    - given_environment_setup_for_non_final_action_test
    - given_environment_setup_for_last_behavior_test
    
    Args:
        bot_dir: Bot directory path
        workspace_dir: Workspace directory path
        behaviors: List of behavior names (default: ['shape', 'discovery'])
        setup_type: Type of setup - 'standard', 'minimal', 'final_action', 'non_final_action', 'last_behavior', 'resume'
        bot_name: Bot name (default: 'story_bot')
        **kwargs: Additional setup parameters
    
    Returns:
        Path to bot config file
    """
    from conftest import create_base_actions_structure, create_bot_config_file
    from agile_bot.bots.base_bot.test.test_helpers import create_actions_workflow_json
    
    if behaviors is None:
        behaviors = ['shape', 'discovery']
    
    # Always bootstrap environment
    bootstrap_env(bot_dir, workspace_dir)
    
    if setup_type == 'minimal':
        # Minimal setup: bootstrap, create bot config, and base_actions
        create_base_actions_structure(bot_dir)
        return create_bot_config_file(bot_dir, bot_name, behaviors)
    
    # Standard and other setups: create base actions structure
    create_base_actions_structure(bot_dir)
    config_path = create_bot_config_file(bot_dir, bot_name, behaviors)
    
    # Create behaviors
    for i, behavior_name in enumerate(behaviors, start=1):
        if setup_type == 'final_action' and behavior_name == 'shape':
            # Special handling for final action test
            from agile_bot.bots.base_bot.test.test_invoke_bot_directly import given_workflow_config
            given_workflow_config(bot_dir, behaviors=['shape'], final_action='validate')
        elif setup_type == 'last_behavior' and behavior_name == 'discovery':
            # Special handling for last behavior test
            create_actions_workflow_json(
                bot_directory=bot_dir,
                behavior_name='discovery',
                actions=[
                    {'name': 'clarify', 'order': 1, 'next_action': 'strategy'},
                    {'name': 'strategy', 'order': 2, 'next_action': 'build'},
                    {'name': 'build', 'order': 3, 'next_action': 'render'},
                    {'name': 'render', 'order': 4}
                ],
                order=i
            )
        else:
            create_actions_workflow_json(bot_dir, behavior_name, order=i if setup_type in ['final_action', 'last_behavior'] else None)
    
    # Always create guardrails files (required for Behavior initialization)
    from agile_bot.bots.base_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files
    for behavior_name in behaviors:
        create_minimal_guardrails_files(bot_dir, behavior_name, bot_name)
    
    # Additional setup based on type
    if setup_type in ['final_action', 'non_final_action', 'last_behavior', 'standard']:
        # Create knowledge graph configs if needed
        from agile_bot.bots.base_bot.test.test_build_knowledge import (
            given_setup
        )
        for behavior_name in behaviors:
            behavior_file = bot_dir / 'behaviors' / behavior_name / 'behavior.json'
            if behavior_file.exists():
                import json
                behavior_config = json.loads(behavior_file.read_text(encoding='utf-8'))
                actions = behavior_config.get('actions_workflow', {}).get('actions', [])
                if any(action.get('name') == 'build' for action in actions):
                    kg_dir = given_setup('directory_structure', bot_dir, behavior=behavior_name)
                    given_setup('config_and_template', bot_dir, kg_dir=kg_dir)
        
        # Create story graph file using centralized given_story_graph function
        given_story_graph(workspace_dir, {
            'epics': [],
            'solution': {'name': 'Test Solution'}
        })
    
    if setup_type == 'resume':
        # Setup for workflow resume
        from agile_bot.bots.base_bot.test.test_invoke_bot_directly import given_completed_action
        if 'behavior' in kwargs and 'action' in kwargs:
            completed_actions = given_completed_action(bot_name, kwargs['behavior'], kwargs['action'])
            # Additional resume setup can be added here
    
    return config_path

def given_workflow_config(bot_directory: Path, behaviors: list = None, actions: list = None, final_action: str = None) -> None:
    """Consolidated workflow configuration helper.
    
    Replaces:
    - given_standard_workflow_states
    - given_standard_workflow_actions_config
    - given_action_configs_exist_for_workflow_actions
    - given_base_actions_exist_with_transitions
    - given_behaviors_exist_with_workflow
    - given_behavior_workflow_with_validate_as_final
    - given_workflow_created
    - when_create_workflow_with_states_and_transitions
    - given_standard_workflow_states_and_transitions
    - given_standard_states_and_transitions
    - given_expected_transitions_list
    
    Args:
        bot_directory: Bot directory path
        behaviors: List of behavior names (default: ['shape', 'discovery'])
        actions: List of action configs (default: standard workflow actions)
        final_action: Name of final action (default: 'render')
    """
    from conftest import create_base_actions_structure
    from agile_bot.bots.base_bot.test.test_helpers import create_actions_workflow_json, get_test_base_actions_dir
    from agile_bot.bots.base_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files
    
    if behaviors is None:
        behaviors = ['shape', 'discovery']
    
    if actions is None:
        # Standard workflow actions
        actions = [
            ('clarify', 'clarify', 1, 'strategy'),
            ('strategy', 'strategy', 2, 'build'),
            ('build', 'build', 3, 'validate'),
            ('validate', 'validate', 4, 'render' if final_action != 'validate' else None),
            ('render', 'render', 5, None)
        ]
    
    # Create base actions structure
    create_base_actions_structure(bot_directory)
    
    # Create base action configs with transitions
    base_actions_dir = get_test_base_actions_dir(bot_directory)
    for folder_name, action_name, order, next_action in actions:
        if next_action is None and action_name != final_action:
            continue  # Skip if this isn't the final action
        action_dir = base_actions_dir / folder_name
        action_dir.mkdir(parents=True, exist_ok=True)
        action_config = {
            'name': action_name,
            'workflow': True,
            'order': order
        }
        if next_action:
            action_config['next_action'] = next_action
        (action_dir / 'action_config.json').write_text(json.dumps(action_config), encoding='utf-8')
    
    # Create behaviors with workflow
    bot_name = bot_directory.name if bot_directory.name in ['story_bot', 'test_story_bot'] else 'story_bot'
    for behavior in behaviors:
        if final_action == 'validate' and behavior == 'shape':
            # Special case: validate as final
            create_actions_workflow_json(
                bot_directory=bot_directory,
                behavior_name=behavior,
                actions=[
                    {'name': 'clarify', 'order': 1, 'next_action': 'strategy'},
                    {'name': 'strategy', 'order': 2, 'next_action': 'build'},
                    {'name': 'build', 'order': 3, 'next_action': 'validate'},
                    {'name': 'validate', 'order': 4}
                ]
            )
        else:
            create_actions_workflow_json(bot_directory, behavior)
        create_minimal_guardrails_files(bot_directory, behavior, bot_name)
        
        # Create knowledge graph configs if behavior has 'build' action
        behavior_file = bot_directory / 'behaviors' / behavior / 'behavior.json'
        if behavior_file.exists():
            import json
            behavior_config = json.loads(behavior_file.read_text(encoding='utf-8'))
            workflow_actions = behavior_config.get('actions_workflow', {}).get('actions', [])
            if any(action.get('name') == 'build' for action in workflow_actions):
                from agile_bot.bots.base_bot.test.test_build_knowledge import (
                    given_setup
                )
                kg_dir = given_setup('directory_structure', bot_directory, behavior=behavior)
                given_setup('config_and_template', bot_directory, kg_dir=kg_dir)



def given_environment_bootstrapped_and_activity_log_initialized(bot_directory: Path, workspace_directory: Path):
    """Given: Environment bootstrapped and activity log initialized."""
    bootstrap_env(bot_directory, workspace_directory)
    log_file = create_activity_log_file(workspace_directory)
    return log_file


# _create_action_with_default_class, given_environment_bootstrapped_and_action_initialized
# - moved to test_execute_behavior_actions.py



# These are specific to Perform Behavior Action sub-epic

def then_file_exists(file_path):
    """Then: File exists at path.
    
    Consolidated function that replaces:
    - then_state_file_exists(state_file)
    - then_state_file_exists_at_path(state_file)
    - then_file_exists_at_path(file_path)
    """
    from pathlib import Path
    if isinstance(file_path, str):
        file_path = Path(file_path)
    assert file_path.exists(), f"File should exist at {file_path}"


def then_file_does_not_exist(file_path):
    """Then: File does not exist at path.
    
    Consolidated function that replaces:
    - then_state_file_does_not_exist(state_file)
    - then_state_file_does_not_exist_at_path(state_file)
    - then_file_does_not_exist_at_path(file_path)
    """
    from pathlib import Path
    if isinstance(file_path, str):
        file_path = Path(file_path)
    assert not file_path.exists(), f"File should NOT exist at {file_path}"


def given_activity_tracker(workspace_directory, bot_name='story_bot'):
    """Given: Activity tracker created.
    
    Consolidated function that replaces:
    - given_activity_tracker_created(workspace_directory)
    - given_activity_tracker_created(workspace_directory, bot_name)
    """
    from agile_bot.bots.base_bot.src.actions.activity_tracker import ActivityTracker
    from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
    bot_paths = BotPaths(workspace_path=workspace_directory)
    return ActivityTracker(bot_paths=bot_paths, bot_name=bot_name)


def when_activity_tracks_start(tracker, action_state):
    """When: Activity tracker tracks start.
    
    Consolidated function that replaces:
    - when_track_activity_start(tracker, action_state)
    - when_activity_tracker_tracks_start(tracker, bot_name, behavior, action)
    
    Args:
        tracker: ActivityTracker instance
        action_state: Action state string (e.g., 'bot_name.behavior.action') or dict with bot_name, behavior, action
    """
    from agile_bot.bots.base_bot.src.actions.activity_tracker import ActionState
    
    if isinstance(action_state, str):
        # Parse action_state like 'bot_name.behavior.action'
        parts = action_state.split('.')
        if len(parts) == 3:
            bot_name, behavior, action = parts
            tracker.track_start(ActionState(bot_name, behavior, action))
        else:
            raise ValueError(f"Invalid action_state format: {action_state}")
    elif isinstance(action_state, dict):
        tracker.track_start(ActionState(action_state['bot_name'], action_state['behavior'], action_state['action']))
    else:
        raise ValueError(f"Invalid action_state type: {type(action_state)}")


def then_environment_variables_not_set(var_names):
    """Then: Environment variables are not set.
    
    Consolidated function that replaces:
    - then_environment_variables_not_set_check(var_names)
    
    Args:
        var_names: Variable names to check (can be list or *args)
    """
    import os
    if isinstance(var_names, str):
        var_names = [var_names]
    for var_name in var_names:
        assert var_name not in os.environ or os.environ[var_name] == '', \
            f"Environment variable {var_name} should not be set, but has value: {os.environ.get(var_name)}"


def then_function_returns_same_value(func, value):
    """Then: Function returns same value on multiple calls.
    
    Consolidated function that replaces:
    - then_function_returns_same_value_check(func, value)
    """
    result1 = func()
    result2 = func()
    result3 = func()
    assert result1 == value and result2 == value and result3 == value, \
        f"Function should return {value} consistently, got {result1}, {result2}, {result3}"


def then_environment_variable_matches(var_name, expected_value):
    """Then: Environment variable matches expected value.
    
    Consolidated function that replaces:
    - then_environment_variable_matches_expected(var_name, expected_value)
    """
    import os
    from pathlib import Path
    actual_value = os.environ.get(var_name)
    if isinstance(expected_value, Path):
        expected_value = str(expected_value)
    if isinstance(actual_value, Path):
        actual_value = str(actual_value)
    assert actual_value == expected_value, \
        f"Environment variable {var_name} mismatch: expected {expected_value}, got {actual_value}"


def then_function_returns_path(func, expected_path):
    """Then: Function returns expected path.
    
    Consolidated function that replaces:
    - then_function_returns_path_check(func, expected_path)
    """
    from pathlib import Path
    actual_path = func()
    if isinstance(actual_path, str):
        actual_path = Path(actual_path)
    if isinstance(expected_path, str):
        expected_path = Path(expected_path)
    assert actual_path == expected_path, \
        f"Function should return {expected_path}, got {actual_path}"


def then_violation_has_field(violation, field, value):
    """Then: Violation has expected field value.
    
    Consolidated function that replaces:
    - then_violation_has_expected_line_number(violation, expected_line_number)
    - then_violation_has_expected_location(violation, expected_location)
    - then_violation_has_expected_message(violation, expected_message)
    - then_violation_has_expected_severity(violation, expected_severity)
    
    Args:
        violation: Violation dict
        field: Field name to check ('line_number', 'location', 'violation_message', 'severity', etc.)
        value: Expected value (for violation_message, checks if value is 'in' the message)
    """
    # Map common field names
    field_mapping = {
        'line_number': 'line_number',
        'location': 'location',
        'message': 'violation_message',
        'violation_message': 'violation_message',
        'severity': 'severity'
    }
    actual_field = field_mapping.get(field, field)
    assert actual_field in violation, f"Violation missing field '{actual_field}': {violation}"
    
    # For violation_message, use 'in' check; for others use exact match
    if actual_field == 'violation_message':
        assert value in violation[actual_field], \
            f"Expected message '{value}' not found in '{violation[actual_field]}'"
    else:
        assert violation[actual_field] == value, \
            f"Violation {actual_field} mismatch: expected {value}, got {violation[actual_field]}"


def given_config_dict(config_type: str, **config_data) -> dict:
    """Given: Config dictionary.
    
    Consolidates: given_state_file(state_file), given_file_paths(files), 
    given_actions_workflow_dict(actions), given_behavior_config_dict(name, actions=None, **kwargs),
    given_action_config_dict(action_name, config), given_action_config_dict_created(action_name, config),
    given_behavior_instructions_dict(behavior, instructions), given_behavior_instructions_dict_created(behavior, instructions)
    
    Creates different types of config dictionaries based on config_type:
    - 'state_file': Creates state_data dict with current_behavior, current_action, completed_actions, timestamp
    - 'file_paths': Creates file_paths dict/list
    - 'actions_workflow': Creates actions_workflow dict with actions list
    - 'behavior_config': Creates behavior_config dict with description, goal, inputs, outputs, actions_workflow, etc.
    - 'action_config': Creates action_config dict (if config provided, uses it; otherwise creates from action_name)
    - 'behavior_instructions': Creates behavior instructions dict
    
    Note: given_bot_paths() and given_rule_object_for_scanner() return objects, not dicts, 
    so they are not part of this consolidation.
    """
    if config_type == 'state_file':
        return {
            'current_behavior': config_data.get('current_behavior', ''),
            'current_action': config_data.get('current_action', ''),
            'completed_actions': config_data.get('completed_actions', []),
            'timestamp': config_data.get('timestamp', '2025-12-04T16:00:00.000000')
        }
    elif config_type == 'file_paths':
        files = config_data.get('files', [])
        if isinstance(files, list):
            return {'files': files}
        return files if isinstance(files, dict) else {}
    elif config_type == 'actions_workflow':
        actions = config_data.get('actions', [])
        return {'actions': actions}
    elif config_type == 'behavior_config':
        behavior_config = {
            'description': config_data.get('description', ''),
            'goal': config_data.get('goal', ''),
            'inputs': config_data.get('inputs', []),
            'outputs': config_data.get('outputs', []),
        }
        if 'actions' in config_data:
            behavior_config['actions_workflow'] = {'actions': config_data['actions']}
        elif 'actions_workflow' in config_data:
            behavior_config['actions_workflow'] = config_data['actions_workflow']
        if 'instructions' in config_data:
            behavior_config['instructions'] = config_data['instructions']
        if 'trigger_words' in config_data:
            behavior_config['trigger_words'] = config_data['trigger_words']
        if 'behaviorName' in config_data:
            behavior_config['behaviorName'] = config_data['behaviorName']
        if 'order' in config_data:
            behavior_config['order'] = config_data['order']
        return behavior_config
    elif config_type == 'action_config':
        # If config provided, use it; otherwise create from action_name
        if 'config' in config_data:
            return config_data['config']
        action_name = config_data.get('action_name', 'clarify')
        return {
            'name': action_name,
            'workflow': config_data.get('workflow', True),
            'order': config_data.get('order', 1),
            'instructions': config_data.get('instructions', [f'{action_name} instructions'])
        }
    elif config_type == 'behavior_instructions':
        # Create behavior instructions dict
        behavior = config_data.get('behavior', 'shape')
        instructions = config_data.get('instructions', {})
        if isinstance(instructions, dict):
            return instructions
        elif isinstance(instructions, list):
            return {'instructions': instructions}
        else:
            return {'instructions': [instructions] if instructions else []}
    else:
        raise ValueError(f"Unknown config_type: {config_type}")


def given_story_graph(workspace_directory: Path, story_graph: dict = None, docs_path: str = 'docs/stories', filename: str = 'story-graph.json') -> Path:
    """Given: Story graph created.
    
    Centralized function for creating story graph files in tests.
    This is the ONLY function that should create story graph files.
    All other functions should use this instead of creating story graphs directly.
    
    Args:
        workspace_directory: Workspace directory path
        story_graph: Story graph dict (default: {'epics': []})
        docs_path: Relative path from workspace to docs directory (default: 'docs/stories')
        filename: Story graph filename (default: 'story-graph.json')
    
    Returns:
        Path to created story graph file
    """
    if story_graph is None:
        story_graph = {'epics': []}
    
    docs_dir = workspace_directory / docs_path
    return given_file_created(docs_dir, filename, story_graph)


def given_action_initialized(action_type, bot_directory, bot_name='story_bot', behavior='exploration', **kwargs):
    """Given: Action initialized.
    
    Consolidated function that replaces:
    - given_validate_action_initialized(bot_directory, bot_name, behavior, create_story_graph, workspace_directory)
    - given_validate_action_created(bot_directory, bot_name, behavior)
    - given_validate_action_for_test_bot(test_bot_dir, bot_name, behavior)
    - given_gather_context_action_is_initialized(bot_directory, bot_name, behavior_name)
    - given_strategy_action_is_initialized(bot_directory, bot_name, behavior_name)
    
    Args:
        action_type: Type of action ('validate', 'gather_context', 'strategy', etc.)
        bot_directory: Bot directory path
        bot_name: Bot name (default: 'story_bot')
        behavior: Behavior name (default: 'exploration')
        **kwargs: Additional parameters:
            - create_story_graph: If True, create story graph using given_story_graph (default: True for validate)
            - workspace_directory: Workspace directory (if None, uses bot_directory.parent / 'workspace')
    
    Note: Story graph creation is now handled by given_story_graph. If create_story_graph=True,
    it will call given_story_graph to create the file. This ensures consistency.
    """
    from pathlib import Path
    from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
    from agile_bot.bots.base_bot.test.test_helpers import create_actions_workflow_json, bootstrap_env
    from agile_bot.bots.base_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files
    from agile_bot.bots.base_bot.test.test_invoke_mcp import given_base_actions_setup
    
    workspace_directory = kwargs.get('workspace_directory')
    if workspace_directory is None:
        workspace_directory = bot_directory.parent / 'workspace'
    workspace_directory = Path(workspace_directory)
    workspace_directory.mkdir(parents=True, exist_ok=True)
    bootstrap_env(bot_directory, workspace_directory)
    
    create_actions_workflow_json(bot_directory, behavior)
    given_base_actions_setup(bot_directory)
    create_minimal_guardrails_files(bot_directory, behavior, bot_name)
    
    # Always create BotPaths with workspace_directory to ensure consistency
    bot_paths = BotPaths(workspace_path=workspace_directory, bot_directory=bot_directory)
    
    if action_type == 'validate':
        create_story_graph = kwargs.get('create_story_graph', True)
        if create_story_graph:
            # Use centralized given_story_graph function
            given_story_graph(workspace_directory)
        
        from agile_bot.bots.base_bot.src.actions.validate.validate_action import ValidateRulesAction
        from agile_bot.bots.base_bot.src.bot.behavior import Behavior
        behavior_obj = Behavior(name=behavior, bot_paths=bot_paths)
        return ValidateRulesAction(behavior=behavior_obj, action_config=None)
    elif action_type == 'gather_context':
        from agile_bot.bots.base_bot.src.actions.clarify.clarify_action import ClarifyContextAction
        from agile_bot.bots.base_bot.src.bot.behavior import Behavior
        behavior_obj = Behavior(name=behavior, bot_paths=bot_paths)
        return ClarifyContextAction(behavior=behavior_obj, action_config=None)
    elif action_type == 'strategy':
        from agile_bot.bots.base_bot.src.actions.strategy.strategy_action import StrategyAction
        from agile_bot.bots.base_bot.src.bot.behavior import Behavior
        behavior_obj = Behavior(name=behavior, bot_paths=bot_paths)
        return StrategyAction(behavior=behavior_obj, action_config=None)
    else:
        raise ValueError(f"Unknown action_type: {action_type}")


def when_action_tracks_start(action):
    """When: Action tracks start.
    
    Consolidated function that replaces:
    - when_validate_action_tracks_start(action)
    - when_action_tracks_activity_on_start(action)
    """
    action.track_activity_on_start()


def when_action_tracks_completion(action, outputs=None, duration=None):
    """When: Action tracks completion.
    
    Consolidated function that replaces:
    - when_validate_action_tracks_completion(action, outputs, duration)
    - when_action_tracks_activity_on_completion(action, outputs, duration)
    """
    action.track_activity_on_completion(outputs=outputs, duration=duration)


def when_action_finalizes(action, next_action=None):
    """When: Action finalizes.
    
    Consolidates: when_action_finalizes_and_transitions(action, next_action)
    """
    return action.finalize_and_transition(next_action=next_action)


def when_action_injects(action, content='next_action'):
    """When: Action injects content.
    
    Consolidates:
    - when_action_injects_next_action_instructions(action)
    - when_action_injects_questions_and_evidence(action)
    - when_action_injects_strategy_criteria_and_assumptions(action)
    
    Args:
        action: Action instance
        content: Type of content to inject ('next_action', 'questions_and_evidence', 'strategy_criteria_and_assumptions')
    """
    if content == 'next_action':
        return action.inject_next_action_instructions()
    elif content == 'questions_and_evidence':
        # For gather_context actions, call do_execute to get instructions with guardrails injected
        from agile_bot.bots.base_bot.src.actions.action_context import ClarifyActionContext
        result = action.do_execute(ClarifyActionContext())
        instructions = result.get('instructions', {})
        return instructions
    elif content == 'strategy_criteria_and_assumptions':
        # For strategy actions, call do_execute to get instructions with planning criteria injected
        from agile_bot.bots.base_bot.src.actions.action_context import StrategyActionContext
        result = action.do_execute(StrategyActionContext())
        instructions = result.get('instructions', {})
        return instructions
    else:
        raise ValueError(f"Unknown content type: {content}")


def when_scanner_scans(scanner_instance, bad_example, rule_obj, scanner_type='auto'):
    """When: Scanner scans files/knowledge graph.
    
    Consolidated function that replaces:
    - when_test_scanner_scans_files(scanner_instance, bad_example, rule_obj)
    - when_code_scanner_scans_files(scanner_instance, bad_example, rule_obj)
    - when_story_scanner_scans_knowledge_graph(scanner_instance, bad_example, rule_obj)
    - when_execute_scanner_based_on_type(scanner_instance, bad_example, rule_obj)
    
    Args:
        scanner_instance: Scanner instance (TestScanner, CodeScanner, or StoryScanner)
        bad_example: Dict containing test_files, code_files, or knowledge_graph
        rule_obj: Rule object
        scanner_type: Type of scanner ('test', 'code', 'story', or 'auto' to detect)
    """
    from pathlib import Path
    from agile_bot.bots.base_bot.src.scanners.test_scanner import TestScanner
    from agile_bot.bots.base_bot.src.scanners.code_scanner import CodeScanner
    
    # Auto-detect scanner type if not specified
    if scanner_type == 'auto':
        if isinstance(scanner_instance, TestScanner):
            scanner_type = 'test'
        elif isinstance(scanner_instance, CodeScanner):
            scanner_type = 'code'
        else:
            scanner_type = 'story'
    
    violations = []
    
    if scanner_type == 'test':
        test_files = bad_example.get('test_files', [])
        knowledge_graph = bad_example.get('knowledge_graph', {})
        for test_file_path in test_files:
            file_path = Path(test_file_path)
            file_violations = scanner_instance.scan_test_file(file_path, rule_obj, knowledge_graph)
            violations.extend(file_violations)
    elif scanner_type == 'code':
        code_files = bad_example.get('code_files', [])
        knowledge_graph = bad_example.get('knowledge_graph', {})
        for code_file_path in code_files:
            file_path = Path(code_file_path)
            file_violations = scanner_instance.scan_code_file(file_path, rule_obj, knowledge_graph)
            violations.extend(file_violations)
    else:  # story scanner
        knowledge_graph = bad_example.get('knowledge_graph', {})
        violations = scanner_instance.scan(knowledge_graph, rule_obj)
    
    return violations


def then_activity_log_matches(workspace_directory, log_file=None, **checks):
    """Then: Activity log matches expected values.
    
    Consolidated function that replaces:
    - then_completion_entry_has_workflow_complete_flag(workspace_directory)
    - then_activity_log_has_entries_with_action_states(workspace_directory, expected_count, expected_action_states)
    - then_activity_log_has_entry_count_and_last_action_state(workspace_directory, expected_count, expected_last_action_state)
    - then_activity_log_contains_entries(log_file, expected_entries)
    - then_activity_log_has_two_entries_with_expected_states(workspace_directory)
    - then_activity_log_matches_expected(workspace_directory, expected_entries)
    - then_activity_log_at_path(workspace_directory, expected_entries)
    - then_activity_log_has_entry_with_action_state(workspace_directory, expected_action_state, expected_status)
    
    Args:
        workspace_directory: Workspace directory path (used if log_file not provided)
        log_file: Optional Path to log file (if provided, used instead of workspace_directory/activity_log.json)
        **checks: Checks to perform:
            - expected_count: Expected number of entries
            - expected_action_state: Expected action_state in entry (single value)
            - expected_action_states: List of expected action_states (one per entry in order)
            - expected_last_action_state: Expected action_state of last entry
            - expected_status: Expected status in entry
            - expected_entries: List of expected entry dicts (matched by action_state, not exact match)
            - workflow_complete: Check that completion entry has workflow_complete flag in outputs
    """
    from pathlib import Path
    from tinydb import TinyDB
    
    if log_file is None:
        log_file = workspace_directory / 'activity_log.json'
    
    if not log_file.exists():
        if 'expected_count' in checks and checks['expected_count'] == 0:
            return  # No entries expected, file doesn't exist - that's fine
        assert False, f"Activity log file does not exist at {log_file}"
    
    with TinyDB(log_file) as db:
        entries = db.all()
        
        if 'expected_count' in checks:
            assert len(entries) == checks['expected_count'], \
                f"Expected {checks['expected_count']} entries, got {len(entries)}"
        
        if 'expected_action_states' in checks:
            # Check that entries match expected_action_states list in order
            expected_states = checks['expected_action_states']
            assert len(entries) == len(expected_states), \
                f"Expected {len(expected_states)} entries, got {len(entries)}"
            for i, expected_state in enumerate(expected_states):
                assert entries[i].get('action_state') == expected_state, (
                    f"Entry {i} should have action_state '{expected_state}', got '{entries[i].get('action_state')}'"
                )
        
        if 'expected_last_action_state' in checks:
            # Check last entry's action_state
            assert len(entries) > 0, "No entries in activity log"
            assert entries[-1].get('action_state') == checks['expected_last_action_state'], (
                f"Last entry should have action_state '{checks['expected_last_action_state']}', "
                f"got '{entries[-1].get('action_state')}'"
            )
        
        if 'expected_action_state' in checks:
            matching_entries = [e for e in entries if e.get('action_state') == checks['expected_action_state']]
            assert len(matching_entries) > 0, \
                f"No entry found with action_state={checks['expected_action_state']}"
            if 'expected_status' in checks:
                assert matching_entries[0].get('status') == checks['expected_status'], \
                    f"Expected status {checks['expected_status']}, got {matching_entries[0].get('status')}"
        
        if 'workflow_complete' in checks and checks['workflow_complete']:
            # Check that completion entry has workflow_complete flag in outputs
            completion_entry = next((e for e in entries if 'outputs' in e), None)
            assert completion_entry is not None, "No completion entry found with outputs"
            assert completion_entry['outputs'].get('workflow_complete') is True, \
                "Completion entry does not have workflow_complete flag set to True"
        
        if 'expected_entries' in checks:
            # Match entries by action_state (not exact match)
            expected_entries = checks['expected_entries']
            assert len(entries) == len(expected_entries), \
                f"Expected {len(expected_entries)} entries, got {len(entries)}"
            for expected_entry in expected_entries:
                expected_action_state = expected_entry.get('action_state')
                assert any(
                    entry.get('action_state') == expected_action_state
                    for entry in entries
                ), f"No entry found with action_state '{expected_action_state}'"


def then_scanners_match(behavior, count=None, structure_valid=None):
    """Then: Scanners match expected values.
    
    Consolidated function that replaces:
    - then_scanners_discovered_with_expected_count_and_valid_structure(behavior, expected_scanner_count)
    
    Args:
        behavior: Behavior instance to check scanners from
        count: Expected number of scanner classes (optional)
        structure_valid: Whether to validate scanner structure (default: True if count is provided)
    """
    # Get scanners from rules (scanners belong to rules, not behaviors)
    rules = behavior.rules
    scanners = [rule.scanner_class for rule in rules if rule.scanner_class]
    
    if count is not None:
        assert len(scanners) == count, (
            f"Expected {count} scanner classes discovered, got {len(scanners)}"
        )
        assert len(rules) >= count, (
            f"Expected at least {count} rules, got {len(rules)}"
        )
    
    # Validate structure if requested (default: True if count is provided)
    if structure_valid is None:
        structure_valid = count is not None
    
    if structure_valid:
        for scanner_class in scanners:
            assert isinstance(scanner_class, type), (
                f"Discovered scanner must be a class, got: {type(scanner_class)}"
            )
        for rule in rules:
            assert rule.has_scanner, f"Rule {rule.name} should have a scanner attached"
            scanner = rule.scanner
            assert scanner is not None, f"Rule {rule.name} should have a scanner instance"


def then_instructions_have_structure(instructions, structure='validation_rules'):
    """Then: Instructions have expected structure.
    
    Consolidated function that replaces:
    - then_validation_rules_have_expected_structure(instructions)
    
    Args:
        instructions: Instructions dict to check
        structure: Structure type to validate ('validation_rules' or custom structure dict)
    """
    if structure == 'validation_rules':
        # Default validation_rules structure check
        assert 'validation_rules' in instructions, "Instructions must contain 'validation_rules' key"
        validation_rules = instructions['validation_rules']
        assert len(validation_rules) > 0, "Instructions should contain validation rules"
        
        # Validate each rule structure (accepts Rule objects or dicts)
        from agile_bot.bots.base_bot.src.actions.rules.rule import Rule
        from agile_bot.bots.base_bot.test.test_validate_knowledge_and_content_against_rules import validate_violation_structure
        
        for rule in validation_rules:
            # Handle Rule objects (new format)
            if isinstance(rule, Rule):
                assert hasattr(rule, 'rule_file'), f"Rule object must have 'rule_file' attribute"
                assert hasattr(rule, 'rule_content'), f"Rule object must have 'rule_content' attribute"
                rule_file = str(rule.rule_file)
                rule_content = rule.rule_content
            elif isinstance(rule, dict):
                # Backward compatibility: dict format (from rules.validate() which returns dicts)
                assert 'rule_content' in rule, f"Rule dict must contain 'rule_content' key: {rule}"
                rule_content = rule['rule_content']
                rule_file = rule.get('rule_file', 'unknown')
                # If dict has scanner_results, validate it
                if 'scanner_results' in rule:
                    scanner_results = rule['scanner_results']
                    if 'violations' in scanner_results:
                        violations = scanner_results['violations']
                        assert isinstance(violations, list), "Scanner results should contain violations list"
                        for violation in violations:
                            assert validate_violation_structure(violation, ['rule', 'line_number', 'location', 'violation_message', 'severity']), (
                                f"Violation missing required fields: {violation}"
                            )
            else:
                raise AssertionError(f"Rule should be a Rule object or dict, got: {type(rule)}")
            
            # Validate rule_content has scanner if it's a dict
            if isinstance(rule_content, dict):
                assert 'scanner' in rule_content, f"Rule content must contain 'scanner' key: {rule_content}"
                scanner_path = rule_content['scanner']
                assert scanner_path is not None, f"Rule should have a scanner attached: {rule_file}"
        
        assert 'base_instructions' in instructions, "Instructions must contain 'base_instructions' key"
        base_instructions = instructions['base_instructions']
        assert isinstance(base_instructions, list), "Base instructions should be a list"
    elif isinstance(structure, dict):
        # Custom structure check - structure dict specifies required keys and their types/validators
        for key, validator in structure.items():
            assert key in instructions, f"Instructions must contain '{key}' key"
            if callable(validator):
                validator(instructions[key])
            elif isinstance(validator, type):
                assert isinstance(instructions[key], validator), f"'{key}' should be of type {validator.__name__}"
            elif isinstance(validator, list):
                # List of allowed values
                assert instructions[key] in validator, f"'{key}' should be one of {validator}"

def then_config_path_matches(instructions, config_path, config_key='knowledge_graph_config'):
    """Then: Config path matches expected.
    
    Consolidated function that replaces:
    - then_config_path_matches_expected(instructions, expected_path)
    
    Args:
        instructions: Instructions dict containing config
        config_path: Expected config path value
        config_key: Key in instructions that contains the config (default: 'knowledge_graph_config')
    """
    assert config_key in instructions, f"Instructions must contain '{config_key}' key"
    config = instructions[config_key]
    assert 'path' in config, f"Config must contain 'path' key"
    assert config['path'] == config_path, f"Expected config path '{config_path}', got '{config['path']}'"


def then_instructions_merged_from_sources(merged_instructions, behavior, action, sources='both'):
    """Then: Instructions merged from sources.
    
    Consolidated function that replaces:
    - then_instructions_merged_from_both_sources(merged_instructions, behavior, action)
    - then_base_instructions_only_present(merged_instructions, behavior, action)
    
    Args:
        merged_instructions: Merged instructions dict to check
        behavior: Expected behavior name
        action: Expected action name
        sources: Which sources should be present ('both', 'base_only', or 'behavior_only')
    """
    assert merged_instructions['action'] == action, f"Expected action '{action}', got '{merged_instructions.get('action')}'"
    assert merged_instructions['behavior'] == behavior, f"Expected behavior '{behavior}', got '{merged_instructions.get('behavior')}'"
    
    if sources == 'both':
        assert 'base_instructions' in merged_instructions, "Instructions must contain 'base_instructions' key"
        assert 'behavior_instructions' in merged_instructions, "Instructions must contain 'behavior_instructions' key"
    elif sources == 'base_only':
        assert 'base_instructions' in merged_instructions, "Instructions must contain 'base_instructions' key"
        assert merged_instructions.get('behavior_instructions', []) == [], "Behavior instructions should be empty"
    elif sources == 'behavior_only':
        assert 'behavior_instructions' in merged_instructions, "Instructions must contain 'behavior_instructions' key"
        assert merged_instructions.get('base_instructions', []) == [], "Base instructions should be empty"


def then_action_instructions_match(action, knowledge_graph=None, test_files=None):
    """Then: Action instructions match expected.
    
    Consolidated function that replaces:
    - then_inject_validation_instructions_result_has_instructions(action, knowledge_graph, test_file_paths)
    
    Args:
        action: Action instance to check instructions from
        knowledge_graph: Expected knowledge graph dict (optional)
        test_files: Expected test file paths list (optional)
    """
    from agile_bot.bots.base_bot.src.actions.rules.rules import ValidationContext, ValidationCallbacks
    files = {'test': test_files} if test_files else {}
    validation_context = ValidationContext(
        knowledge_graph=knowledge_graph,
        files=files,
        callbacks=ValidationCallbacks(),
        skiprule=[],
        exclude=[],
        skip_cross_file=False,
        behavior=action.behavior,
        bot_paths=action.behavior.bot_paths,
        working_dir=action.behavior.bot_paths.workspace_directory
    )
    result_direct = action.injectValidationInstructions(validation_context)
    assert 'instructions' in result_direct, "Result should contain 'instructions' key"
    return result_direct


def then_scanner_class_loaded(scanner_class, error_msg=None):
    """Then: Scanner class loaded successfully.
    
    Consolidated function that replaces:
    - then_scanner_class_loaded_successfully(scanner_class, error_msg)
    
    Args:
        scanner_class: Scanner class that was loaded (or None if failed)
        error_msg: Optional error message if loading failed
    """
    assert scanner_class is not None, f"Failed to load scanner: {error_msg or 'Unknown error'}"


def when_scanner_created(scanner_class):
    """When: Scanner instance created.
    
    Consolidated function that replaces:
    - when_scanner_instance_created(scanner_class)
    
    Args:
        scanner_class: Scanner class to instantiate
    """
    return scanner_class()


def when_scanner_scans(scanner_instance, bad_example, rule_obj, scanner_type='auto'):
    """When: Scanner scans files/knowledge graph.
    
    Consolidated function that replaces:
    - when_test_scanner_scans_files(scanner_instance, bad_example, rule_obj)
    - when_code_scanner_scans_files(scanner_instance, bad_example, rule_obj)
    - when_story_scanner_scans_knowledge_graph(scanner_instance, bad_example, rule_obj)
    - when_execute_scanner_based_on_type(scanner_instance, bad_example, rule_obj)
    
    Args:
        scanner_instance: Scanner instance (may be unused if scanner_type='auto' and using rule.scan())
        bad_example: Dict containing test_files, code_files, and/or knowledge_graph
        rule_obj: Rule object to scan with
        scanner_type: Type of scanner ('auto', 'test', 'code', 'story'). 'auto' uses rule.scan() (preferred)
    """
    from pathlib import Path
    from agile_bot.bots.base_bot.src.scanners.test_scanner import TestScanner
    from agile_bot.bots.base_bot.src.scanners.code_scanner import CodeScanner
    
    if scanner_type == 'auto':
        # NEW DOMAIN MODEL: Use rule.scan() instead of calling scanner directly
        kg = {}
        test_files = []
        code_files = []
        
        if bad_example:
            # Extract knowledge graph (everything except test_files/code_files)
            kg = {k: v for k, v in bad_example.items() if k not in ['test_files', 'code_files']}
            
            # Extract test files
            if 'test_files' in bad_example:
                test_files = [Path(tf) for tf in bad_example['test_files']]
            
            # Extract code files
            if 'code_files' in bad_example:
                code_files = [Path(cf) for cf in bad_example['code_files']]
        
        # Use rule.scan() which handles scanner instantiation and calling
        files_dict = {}
        if test_files:
            files_dict['test'] = test_files
        if code_files:
            files_dict['src'] = code_files
        
        # Call rule.scan() which returns scanner_results dict
        scanner_results = rule_obj.scan(kg, files=files_dict if files_dict else None)
        
        # Extract violations from scanner_results
        violations = []
        if 'violations' in scanner_results:
            violations = scanner_results['violations']
        elif 'file_by_file' in scanner_results:
            violations.extend(scanner_results['file_by_file'].get('violations', []))
        if 'cross_file' in scanner_results:
            violations.extend(scanner_results['cross_file'].get('violations', []))
        
        return violations
    
    elif scanner_type == 'test':
        # Legacy: Test scanner scans files
        violations = []
        test_files_to_scan = []
        if bad_example and 'test_files' in bad_example:
            test_files_to_scan = [Path(tf) for tf in bad_example['test_files']]
        
        kg = {}
        if bad_example:
            kg = {k: v for k, v in bad_example.items() if k not in ['test_files', 'code_files']}
        
        for test_file_path in test_files_to_scan:
            file_violations = scanner_instance.scan_test_file(test_file_path, rule_obj, kg)
            violations.extend(file_violations)
        
        return violations
    
    elif scanner_type == 'code':
        # Legacy: Code scanner scans files
        violations = []
        if bad_example and 'code_files' in bad_example:
            for code_file_path in bad_example['code_files']:
                file_path = Path(code_file_path)
                file_violations = scanner_instance.scan_code_file(file_path, rule_obj)
                violations.extend(file_violations)
        return violations
    
    elif scanner_type == 'story':
        # Legacy: Story scanner scans knowledge graph
        kg = bad_example if bad_example else {}
        return scanner_instance.scan(kg, rule_obj)
    
    else:
        raise ValueError(f"Unknown scanner_type: {scanner_type}. Must be 'auto', 'test', 'code', or 'story'")


def when_story_graph_updated(story_graph_path, story_graph, scope=None):
    """When: Story graph updated with optional scope.
    
    Consolidated function that replaces:
    - when_add_scope_to_story_graph_file(story_graph_path, story_graph, scope_config)
    - when_add_scope_to_story_graph_if_provided(story_graph_path, story_graph, scope_config)
    
    Args:
        story_graph_path: Path to story graph file
        story_graph: Story graph dict to update
        scope: Optional scope config dict to add to story graph (uses '_validation_scope' key)
    """
    import json
    from pathlib import Path
    
    story_graph_path = Path(story_graph_path)
    
    # If scope is provided, add it to the story graph using '_validation_scope' key
    if scope is not None:
        story_graph['_validation_scope'] = scope
    
    # Write updated story graph to file
    story_graph_path.write_text(json.dumps(story_graph, indent=2), encoding='utf-8')

def then_instructions_contain(instructions, content_type, **content_params):
    """Consolidates: then_base_instructions_include_next_behavior_reminder, then_reminder_contains_prompt_text, then_instructions_contain_guardrails, then_instructions_contain_strategy_criteria_and_assumptions, then_instructions_contain_template_path, then_instructions_contain_validation_rules, then_render_configs_include_all_required_fields, then_specific_field_values_present
    
    Then: Instructions contain specified content type.
    content_type can be: 'next_behavior_reminder', 'reminder_prompt_text', 'guardrails', 'strategy_criteria_and_assumptions', 'template_path', 'validation_rules', 'render_required_fields', 'render_field_values'
    """
    from pathlib import Path
    
    if content_type == 'next_behavior_reminder':
        # instructions is action_result dict
        instructions_dict = instructions.get('instructions', {}) if isinstance(instructions, dict) else instructions
        assert instructions_dict, f"No instructions found. Result: {instructions}"
        base_instructions_list = instructions_dict.get('base_instructions', [])
        reminder_found = False
        next_behavior_found = False
        for i, instruction in enumerate(base_instructions_list):
            if 'NEXT BEHAVIOR REMINDER' in instruction:
                reminder_found = True
                if i + 1 < len(base_instructions_list):
                    next_instruction = base_instructions_list[i + 1]
                    if 'prioritization' in next_instruction.lower():
                        next_behavior_found = True
        assert reminder_found, "base_instructions should include 'NEXT BEHAVIOR REMINDER' section"
        assert next_behavior_found, "Reminder should mention 'prioritization' as the next behavior"
        return base_instructions_list
    
    elif content_type == 'reminder_prompt_text':
        # instructions is base_instructions_list
        instructions_text = ' '.join(instructions) if isinstance(instructions, list) else instructions
        assert 'next behavior in sequence' in instructions_text.lower(), "Reminder should contain 'next behavior in sequence' text"
        assert 'would you like to continue' in instructions_text.lower() or 'work on a different behavior' in instructions_text.lower(), "Reminder should contain prompt asking user if they want to continue"
    
    elif content_type == 'guardrails':
        # instructions is dict
        assert 'guardrails' in instructions
        assert 'required_context' in instructions['guardrails']
        assert 'key_questions' in instructions['guardrails']['required_context']
        assert instructions['guardrails']['required_context']['key_questions'] == content_params.get('expected_questions', [])
        assert 'evidence' in instructions['guardrails']['required_context']
        assert instructions['guardrails']['required_context']['evidence'] == content_params.get('expected_evidence', [])
    
    elif content_type == 'strategy_criteria_and_assumptions':
        # instructions is dict
        assert 'strategy_criteria' in instructions
        assert 'assumptions' in instructions
        assert instructions['assumptions'] == content_params.get('expected_assumptions', [])
        assert instructions['strategy_criteria'] is not None
    
    elif content_type == 'template_path':
        # instructions is dict
        template_name = content_params.get('template_name')
        assert 'knowledge_graph_template' in instructions
        assert 'template_path' in instructions
        assert template_name in instructions['template_path']
        # Note: template_path may be relative, so we only check it's set, not that it exists
    
    elif content_type == 'validation_rules':
        # instructions is dict
        assert 'validation_rules' in instructions, "Instructions must contain 'validation_rules' key"
        return instructions['validation_rules']
    
    elif content_type == 'render_required_fields':
        # instructions is base_instructions_text string
        assert instructions.strip() != ''
        assert 'render' in instructions.lower() or 'template' in instructions.lower() or 'output' in instructions.lower()
    
    elif content_type == 'render_field_values':
        # instructions is base_instructions_text string
        assert instructions.strip() != ''
        assert 'render' in instructions.lower() or 'scenario' in instructions.lower() or 'template' in instructions.lower()
    
    else:
        raise ValueError(f"Unknown content_type: {content_type}")

def then_instructions_do_not_contain(instructions, content_type):
    """Consolidates: then_base_instructions_do_not_include_next_behavior_reminder, then_no_next_action_instructions_injected, then_instructions_do_not_contain_guardrails, then_instructions_do_not_contain_strategy_data
    
    Then: Instructions do not contain specified content type.
    content_type can be: 'next_behavior_reminder', 'next_action_instructions', 'guardrails', 'strategy_data'
    """
    if content_type == 'next_behavior_reminder':
        # instructions is action_result dict or BotResult object
        if hasattr(instructions, 'data'):
            instructions_dict = instructions.data.get('instructions', {})
        else:
            instructions_dict = instructions.get('instructions', {}) if isinstance(instructions, dict) else instructions
        base_instructions_list = instructions_dict.get('base_instructions', [])
        instructions_text = ' '.join(base_instructions_list)
        assert 'NEXT BEHAVIOR REMINDER' not in instructions_text, "base_instructions should NOT include 'NEXT BEHAVIOR REMINDER' when action is not final"
    
    elif content_type == 'next_action_instructions':
        # instructions is string
        assert instructions == '' or 'complete' in instructions.lower()
    
    elif content_type == 'guardrails':
        # instructions is dict
        assert 'guardrails' not in instructions or instructions['guardrails'] == {}
    
    elif content_type == 'strategy_data':
        # instructions is dict
        assert 'strategy_criteria' not in instructions or instructions['strategy_criteria'] == {}
        assert 'assumptions' not in instructions or instructions['assumptions'] == []
    
    else:
        raise ValueError(f"Unknown content_type: {content_type}")

def then_template_variables_replaced(instructions_text, type=None):
    """
    Consolidated function for checking template variable replacement.
    Replaces: then_all_template_variables_replaced, then_render_configs_template_variable_replaced,
    then_render_instructions_template_variable_replaced
    
    Args:
        instructions_text: The instructions text to check
        type: Type of template variables to check. None (default) = all build knowledge variables,
              'render_configs' = render configs variables, 'render_instructions' = render instructions variables
    """
    if type is None or type == 'build':
        # Check all build knowledge template variables
        assert '{{rules}}' not in instructions_text
        assert 'verb-noun format' in instructions_text or 'verb-noun-format' in instructions_text
        instructions_lower = instructions_text.lower()
        assert 'epics' in instructions_lower or 'top-level epics' in instructions_lower
        assert '{{instructions}}' not in instructions_text
        assert 'Use verb-noun format' in instructions_text or 'Follow INVEST principles' in instructions_text
    
    elif type == 'render_configs':
        # Check render configs template variables
        assert '{{render_configs}}' not in instructions_text
        # Content may vary by render specs; just ensure some render config text is present
        assert 'render' in instructions_text.lower()
    
    elif type == 'render_instructions':
        # Check render instructions template variables
        assert '{{render_configs}}' not in instructions_text
        assert '{{render_instructions}}' not in instructions_text
        # Ensure render instructions content was injected (non-empty)
        assert instructions_text.strip() != ''

def then_item_matches(item, expected=None, item_type=None, **checks):
    """Then: Item matches expected values.
    
    Consolidated function that handles matching for various item types:
    - result.action matches expected_action
    - state_file matches expected_state
    - instructions match expected content
    - behavior_config matches expected config
    - etc.
    
    Args:
        item: The item to check (result, state_file, instructions, etc.)
        expected: Expected value(s) - can be a single value or dict (optional if using **checks)
        item_type: Optional type hint ('result', 'state_file', 'instructions', 'behavior_config', etc.)
        **checks: Additional checks to perform (e.g., action='clarify', behavior='shape')
    """
    from pathlib import Path
    
    # Auto-detect item_type if not provided
    if item_type is None:
        if hasattr(item, 'action'):
            item_type = 'result'
        elif isinstance(item, Path) and item.suffix == '.json':
            item_type = 'state_file'
        elif isinstance(item, dict) and 'instructions' in item:
            item_type = 'instructions'
        elif isinstance(item, dict) and 'behaviorName' in item:
            item_type = 'behavior_config'
    
    if item_type == 'result' or (hasattr(item, 'action')):
        # Handle BotResult or result objects
        if hasattr(item, 'action'):
            # If expected is a string, use it as the expected action
            if isinstance(expected, str):
                assert item.action == expected, f"Expected action {expected}, got {item.action}"
            # Otherwise check **checks for 'action'
            elif 'action' in checks:
                assert item.action == checks['action'], f"Expected action {checks['action']}, got {item.action}"
        if 'behavior' in checks:
            actual_behavior = getattr(item, 'behavior', None)
            assert actual_behavior == checks['behavior'], f"Expected behavior {checks['behavior']}, got {actual_behavior}"
        if 'status' in checks:
            actual_status = getattr(item, 'status', None)
            assert actual_status == checks['status'], f"Expected status {checks['status']}, got {actual_status}"
    elif item_type == 'state_file' or (isinstance(item, Path) and item.exists()):
        # Handle state file matching
        import json
        if isinstance(item, Path) and item.exists():
            state_data = json.loads(item.read_text())
            if isinstance(expected, dict):
                for key, value in expected.items():
                    assert state_data.get(key) == value, f"State file {key} mismatch: expected {value}, got {state_data.get(key)}"
            elif 'action' in checks:
                assert state_data.get('current_action') == checks['action']
    elif item_type == 'instructions' or (isinstance(item, dict) and 'instructions' in item):
        # Handle instructions matching
        if isinstance(expected, (list, str)):
            if isinstance(expected, str):
                expected = [expected]
            assert item.get('instructions') == expected, \
                f"Instructions mismatch: expected {expected}, got {item.get('instructions')}"
        elif isinstance(expected, dict):
            for key, value in expected.items():
                assert item.get(key) == value, f"Instructions {key} mismatch: expected {value}, got {item.get(key)}"
    elif item_type == 'behavior_config' or (isinstance(item, dict) and 'behaviorName' in item):
        # Handle behavior config matching
        if isinstance(expected, dict):
            for key, value in expected.items():
                assert item.get(key) == value, f"Behavior config {key} mismatch: expected {value}, got {item.get(key)}"
        # Also check **checks
        for key, value in checks.items():
            assert item.get(key) == value, f"Behavior config {key} mismatch: expected {value}, got {item.get(key)}"
    else:
        # Generic matching
        if isinstance(expected, dict):
            for key, value in expected.items():
                if hasattr(item, key):
                    assert getattr(item, key) == value, f"{key} mismatch: expected {value}, got {getattr(item, key)}"
                elif isinstance(item, dict):
                    assert item.get(key) == value, f"{key} mismatch: expected {value}, got {item.get(key)}"
        else:
            assert item == expected, f"Item mismatch: expected {expected}, got {item}"


# ============================================================================
# TEST CLASSES - Tests for utility functions (merged from test_utils.py)
# ============================================================================

@pytest.fixture
def bot_directory(tmp_path):
    """Fixture: Temporary bot directory."""
    bot_dir = tmp_path / 'agile_bot' / 'bots' / 'test_bot'
    bot_dir.mkdir(parents=True)
    return bot_dir


def create_behavior_folder_with_json(bot_dir: Path, folder_name: str) -> Path:
    """Helper: Create behavior folder in bot directory with behavior.json.
    
    Uses create_behavior_folder from test_helpers and adds behavior.json creation.
    """
    behavior_folder = create_behavior_folder(bot_dir, folder_name)
    
    # Create behavior.json file (required for TestFindBehaviorFolder tests)
    behavior_config = {
        "behaviorName": folder_name.split('_')[-1] if '_' in folder_name and folder_name[0].isdigit() else folder_name,
        "description": f"Test behavior: {folder_name}",
        "goal": f"Test goal for {folder_name}",
        "inputs": "Test inputs",
        "outputs": "Test outputs",
        "baseActionsPath": "agile_bot/bots/test_base_bot/base_actions",
        "instructions": [
            f"**BEHAVIOR WORKFLOW INSTRUCTIONS:**",
            "",
            f"Test instructions for {folder_name}."
        ],
        "actions_workflow": {
            "actions": [
                {"name": "clarify", "order": 1, "next_action": "strategy"},
                {"name": "strategy", "order": 2, "next_action": "build"},
                {"name": "build", "order": 3, "next_action": "validate"},
                {"name": "validate", "order": 4, "next_action": "render"},
                {"name": "render", "order": 5}
            ]
        },
        "trigger_words": {
            "description": f"Trigger words for {folder_name}",
            "patterns": [f"test.*{folder_name}"],
            "priority": 10
        }
    }
    behavior_file = behavior_folder / 'behavior.json'
    behavior_file.write_text(json.dumps(behavior_config, indent=2), encoding='utf-8')
    
    # Create base_actions structure - no fallback in production code
    base_actions_dir = bot_dir / 'base_actions'
    action_configs = [
        ('clarify', 1), ('strategy', 2), ('build', 3), ('validate', 4), ('render', 5)
    ]
    for action_name, order in action_configs:
        action_dir = base_actions_dir / action_name
        action_dir.mkdir(parents=True, exist_ok=True)
        (action_dir / 'action_config.json').write_text(json.dumps({
            'name': action_name, 'order': order, 'instructions': [f'{action_name} base instructions']
        }), encoding='utf-8')
    
    return behavior_folder


class TestFindBehaviorFolder:
    """Tests for find_behavior_folder utility function."""

    def test_finds_behavior_folder_with_number_prefix(self, bot_directory):
        """
        SCENARIO: Find behavior folder with number prefix
        GIVEN: Behavior folder exists with name 'tests'
        WHEN: find_behavior_folder is called with behavior name (tests)
        THEN: Returns path to folder 'tests'
        """
        # Given: Create numbered behavior folder
        bot_name = 'test_bot'
        folder_name = 'tests'
        behavior_name = 'tests'
        
        behavior_folder = create_behavior_folder_with_json(bot_directory, folder_name)
        
        # When: Behavior folders are directly named (no numbered prefixes)
        found_folder = bot_directory / 'behaviors' / behavior_name
        
        # Then: Returns numbered folder
        assert found_folder == behavior_folder
        assert found_folder.name == 'tests'

    def test_finds_shape_folder_with_number_prefix(self, bot_directory):
        """
        SCENARIO: Find shape folder with number prefix
        GIVEN: Behavior folder exists with name 'shape'
        WHEN: find_behavior_folder is called with behavior name (shape)
        THEN: Returns path to folder 'shape'
        """
        # Given: Create numbered behavior folder
        bot_name = 'story_bot'
        behavior_folder = create_behavior_folder(bot_directory, 'shape')
        
        # When: Behavior folders are directly named
        found_folder = bot_directory / 'behaviors' / 'shape'
        
        # Then: Returns numbered folder
        assert found_folder == behavior_folder
        assert found_folder.name == 'shape'

    def test_finds_exploration_folder_with_number_prefix(self, bot_directory):
        """
        SCENARIO: Find exploration folder with number prefix
        GIVEN: Behavior folder exists with name 'exploration'
        WHEN: find_behavior_folder is called with behavior name (exploration)
        THEN: Returns path to folder 'exploration'
        """
        # Given
        bot_name = 'story_bot'
        behavior_folder = create_behavior_folder(bot_directory, 'exploration')
        
        # When: Behavior folders are directly named
        found_folder = bot_directory / 'behaviors' / 'exploration'
        
        # Then
        assert found_folder == behavior_folder
        assert found_folder.name == 'exploration'

    # test_raises_error_when_behavior_folder_not_found removed - exception handling test

    def test_handles_prioritization_folder_with_prefix(self, bot_directory):
        """
        SCENARIO: Handles Prioritization Folder With Prefix
        GIVEN: Behavior folder exists as 'prioritization'
        WHEN: find_behavior_folder is called with behavior name (prioritization)
        THEN: Returns path to 'prioritization'
        """
        # Given
        bot_name = 'story_bot'
        behavior_folder = create_behavior_folder(bot_directory, 'prioritization')
        
        # When: Behavior folders are directly named
        found_folder = bot_directory / 'behaviors' / 'prioritization'
        
        # Then
        assert found_folder == behavior_folder
        assert found_folder.name == 'prioritization'

    def test_handles_scenarios_folder_with_prefix(self, bot_directory):
        """
        SCENARIO: Handles Scenarios Folder With Prefix
        GIVEN: Behavior folder exists as 'scenarios'
        WHEN: find_behavior_folder is called with behavior name (scenarios)
        THEN: Returns path to 'scenarios'
        """
        # Given
        bot_name = 'story_bot'
        behavior_folder = create_behavior_folder(bot_directory, 'scenarios')
        
        # When: Behavior folders are directly named
        found_folder = bot_directory / 'behaviors' / 'scenarios'
        
        # Then
        assert found_folder == behavior_folder
        assert found_folder.name == 'scenarios'

    def test_handles_examples_folder_with_prefix(self, bot_directory):
        """
        SCENARIO: Handles Examples Folder With Prefix
        GIVEN: Behavior folder exists as 'examples'
        WHEN: find_behavior_folder is called with behavior name (examples)
        THEN: Returns path to 'examples'
        """
        # Given
        bot_name = 'story_bot'
        behavior_folder = create_behavior_folder(bot_directory, 'examples')
        
        # When: Behavior folders are directly named
        found_folder = bot_directory / 'behaviors' / 'examples'
        
        # Then
        assert found_folder == behavior_folder
        assert found_folder.name == 'examples'


def given_story_graph_dict(minimal=False, scope_type=None, epic=None):
    """Given: Story graph dictionary.
    
    Consolidated function that replaces:
    - given_minimal_story_graph_for_test_file_scope()
    - given_story_graph_for_multiple_test_files()
    - given_test_story_graph()
    - given_existing_story_graph_with_mob_epic()
    
    Args:
        minimal: If True, returns minimal story graph for test file scope
        scope_type: Type of scope ('multiple_test_files' for multiple test files)
        epic: Epic name ('mob' for mob epic, None for default)
    
    Returns:
        Story graph dictionary
    """
    if minimal:
        return {
            "epics": [
                {
                    "name": "Places Order",
                    "sub_epics": [
                        {
                            "name": "Validates Payment",
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Place Order",
                                            "scenarios": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    elif scope_type == 'multiple_test_files':
        return {
            "epics": [
                {
                    "name": "Manage Orders",
                    "sub_epics": [
                        {
                            "name": "Create Order",
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Place Order",
                                            "scenarios": []
                                        },
                                        {
                                            "name": "Cancel Order",
                                            "scenarios": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    elif epic == 'mob':
        return {
            "epics": [
                {
                    "name": "Manage Mobs",
                    "sequential_order": 1,
                    "estimated_stories": 6,
                    "domain_concepts": [
                        {
                            "name": "Mob",
                            "responsibilities": [
                                {
                                    "name": "Groups minions together for coordinated action",
                                    "collaborators": ["Minion"]
                                }
                            ]
                        }
                    ],
                    "sub_epics": []
                }
            ]
        }
    else:
        # Default: test story graph
        return {
            "epics": [
                {
                    "name": "Test Epic",
                    "sequential_order": 1,
                    "sub_epics": [],
                    "story_groups": []
                }
            ]
        }


def when_story_graph_copied(story_graph):
    """When: Copy story graph for test.
    
    Consolidated function that replaces:
    - when_copy_story_graph_for_test(story_graph)
    
    Args:
        story_graph: Story graph dictionary to copy
    
    Returns:
        Copy of story graph dictionary
    """
    return story_graph.copy()


def when_data_extracted(source, extract_type, **extract_params):
    """When: Extract data from source.
    
    Consolidated function that replaces:
    - when_stories_extracted(story_graph, extract_method, as_set=False)
    - when_convert_expected_stories_to_set(expected_stories_in_scope, story_graph, extract_method)
    - when_violations_extracted(story_graph, extract_method, as_set=False)
    - when_convert_expected_violations_to_set(expected_violations_list, expected_stories_in_scope_set, story_graph, extract_method)
    - when_scope_extracted(story_graph, method, get_expected=None)
    - when_test_scope_extraction_with_increment_priorities(story_graph, get_expected_method)
    - when_test_scope_extraction_with_epic_names(story_graph, get_expected_method)
    - when_test_scope_extraction_with_multiple_epics(story_graph, get_expected_method)
    - when_test_scope_extraction_with_story_names(story_graph, get_expected_method)
    - when_test_case_extracted(test_case)
    - when_extract_test_case_data(test_case)
    
    Args:
        source: Source to extract from (story_graph dict, test_case dict, etc.)
        extract_type: Type of extraction ('stories', 'violations', 'scope', 'test_case', 'convert_to_set')
        **extract_params: Additional parameters:
            - extract_method: Method to extract stories/violations
            - as_set: If True, return as set (default: False)
            - expected_stories_in_scope: Expected stories list/set (for convert_to_set)
            - expected_stories_in_scope_set: Expected stories set (for violations)
            - expected_violations_list: Expected violations list (for violations)
            - method: Method for scope extraction
            - get_expected: Function to get expected values (for scope extraction)
            - scope_config: Scope configuration dict (for scope extraction)
    
    Returns:
        Extracted data (list, set, or dict depending on extract_type)
    """
    if extract_type == 'stories':
        extract_method = extract_params.get('extract_method')
        as_set = extract_params.get('as_set', False)
        story_graph = source
        stories = []
        for epic in story_graph['epics']:
            extract_method(epic, stories)
        return set(stories) if as_set else stories
    elif extract_type == 'violations':
        extract_method = extract_params.get('extract_method')
        as_set = extract_params.get('as_set', False)
        story_graph = source
        violations = []
        for epic in story_graph['epics']:
            extract_method(epic, violations)
        return set(violations) if as_set else violations
    elif extract_type == 'convert_to_set':
        expected_stories_in_scope = extract_params.get('expected_stories_in_scope')
        story_graph = source
        extract_method = extract_params.get('extract_method')
        if isinstance(expected_stories_in_scope, list):
            return set(expected_stories_in_scope)
        elif expected_stories_in_scope is None:
            expected_stories_in_scope_set = set()
            for epic in story_graph['epics']:
                extract_method(epic, expected_stories_in_scope_set)
            return expected_stories_in_scope_set
        else:
            return expected_stories_in_scope
    elif extract_type == 'convert_violations_to_set':
        expected_violations_list = extract_params.get('expected_violations_list')
        expected_stories_in_scope_set = extract_params.get('expected_stories_in_scope_set', set())
        story_graph = source
        extract_method = extract_params.get('extract_method')
        if isinstance(expected_violations_list, list):
            return set(expected_violations_list)
        elif expected_violations_list is None:
            stories_with_scenarios = {"Select And Capture Tokens"}
            if expected_stories_in_scope_set:
                return expected_stories_in_scope_set - stories_with_scenarios
            else:
                all_story_names = set()
                for epic in story_graph['epics']:
                    extract_method(epic, all_story_names)
                return all_story_names - stories_with_scenarios
        else:
            return set()
    elif extract_type == 'scope':
        story_graph = source
        method = extract_params.get('method')
        get_expected = extract_params.get('get_expected')
        scope_config = extract_params.get('scope_config')
        if scope_config and get_expected:
            return get_expected(scope_config, story_graph)
        elif scope_config and method:
            # If method is provided but it's actually get_expected (same signature)
            return method(scope_config, story_graph)
        elif method:
            return method(story_graph)
        else:
            raise ValueError("Either get_expected or method must be provided for scope extraction")
    elif extract_type == 'test_case':
        test_case = source
        scope_config = test_case.get('scope_config', {})
        expected_stories_in_scope = test_case.get('expected_stories_in_scope')
        expected_violations_list = test_case.get('expected_violations')
        return scope_config, expected_stories_in_scope, expected_violations_list
    elif extract_type == 'walk':
        # BUILD KNOWLEDGE: Walk story map
        story_map = source
        walk_type = extract_params.get('walk_type', 'epics')
        epic = extract_params.get('epic')
        if walk_type == 'epics':
            if epic:
                return list(story_map.walk(epic))
            else:
                # Walk from first epic
                epics = story_map.epics()
                if epics:
                    return list(story_map.walk(epics[0]))
                return []
    else:
        raise ValueError(f"Unknown extract_type: {extract_type}")


def given_file_paths(files):
    """Given: File paths.
    
    Consolidated function that replaces:
    - given_test_file_paths_for_knowledge_graph(test_file)
    
    Args:
        files: Single Path or list of Paths
    
    Returns:
        List of Path objects
    """
    from pathlib import Path
    if isinstance(files, (list, tuple)):
        return [Path(str(f)) for f in files]
    else:
        return [Path(str(files))]


def given_scanner_spy(scanner_type='test', record=None):
    """Given: Scanner spy for testing.
    
    Consolidated function that replaces:
    - given_spy_test_scanner_that_records_knowledge_graph()
    
    Args:
        scanner_type: Type of scanner ('test' for TestScanner)
        record: What to record ('knowledge_graph' to record knowledge graphs)
    
    Returns:
        Tuple of (recorded_data_list, SpyScannerClass)
    """
    from typing import Dict, List, Any
    from agile_bot.bots.base_bot.src.scanners.test_scanner import TestScanner
    
    if scanner_type == 'test' and record == 'knowledge_graph':
        received_knowledge_graphs = []
        
        class SpyTestScanner(TestScanner):
            def scan(self, knowledge_graph: Dict[str, Any], rule_obj: Any = None) -> List[Dict[str, Any]]:
                """Spy that records knowledge_graph and checks for test_files."""
                received_knowledge_graphs.append(knowledge_graph.copy())
                return []
        
        return received_knowledge_graphs, SpyTestScanner
    else:
        raise ValueError(f"Unsupported scanner_type={scanner_type}, record={record}")


def when_item_accessed(item_type, source, **access_params):
    """When: Access item from source.
    
    Consolidated function that replaces:
    - when_epic_retrieved(epics, index=None, type=None)
    - when_first_epic_retrieved(epics)
    - when_sub_epic_retrieved_from_epics(epics)
    - when_story_retrieved_from_epics(epics)
    - when_scenario_retrieved_from_epics(epics)
    - when_scenario_outline_retrieved_from_epics(epics)
    - when_story_map_epics_retrieved(story_map)
    - when_story_retrieved(epic, story_name)
    - when_story_retrieved_from_epic(epic, story_name)
    - when_scenario_retrieved(story, scenario_name)
    - when_scenario_retrieved_from_story(story, scenario_name)
    - when_scenario_outline_retrieved(scenario, outline_name)
    - when_scenario_outline_retrieved_from_scenario(scenario, outline_name)
    
    Args:
        item_type: Type of item ('epic', 'sub_epic', 'story', 'scenario', 'scenario_outline', 'epics')
        source: Source to access from (epics list, story_map, epic, story, etc.)
        **access_params: Additional parameters:
            - index: Index to access (default: 0 for first item)
            - name: Name to search for (for story/scenario/outline)
            - story_map: StoryMap instance (if accessing epics from story_map)
    
    Returns:
        The accessed item
    """
    index = access_params.get('index', 0)
    name = access_params.get('name')
    
    if item_type == 'epics':
        # Access epics from story_map
        story_map = source
        return story_map.epics()
    elif item_type == 'epic':
        if hasattr(source, 'epics'):  # It's a story_map
            epics = source.epics()
        else:  # It's an epics list
            epics = source
        return epics[index] if index is not None else epics[0]
    elif item_type == 'sub_epic':
        epics = source if isinstance(source, list) else source.epics()
        return epics[0].children[0]
    elif item_type == 'story':
        if name:
            # Search by name
            epic = source if hasattr(source, 'children') else source.epics()[0]
            for sub_epic in epic.children:
                for story_group in sub_epic.children:
                    for story in story_group.children:
                        if story.name == name:
                            return story
            raise ValueError(f"Story '{name}' not found")
        elif hasattr(source, 'epics'):  # It's a story_map
            return source.epics()[0].children[0].children[0].children[0]
        elif hasattr(source, 'children'):  # It's an epic
            return source.children[0].children[0].children[0]
        else:  # It's an epics list
            return source[0].children[0].children[0].children[0]
    elif item_type == 'scenario':
        if name:
            # Search by name
            story = source if hasattr(source, 'scenarios') else when_item_accessed('story', source)
            for scenario in story.scenarios:
                if scenario.name == name:
                    return scenario
            raise ValueError(f"Scenario '{name}' not found")
        elif hasattr(source, 'scenarios'):  # It's a story
            return source.scenarios[index]
        else:  # It's epics list
            story = when_item_accessed('story', source)
            return story.scenarios[index]
    elif item_type == 'scenario_outline':
        if name:
            # Search by name
            scenario = source if hasattr(source, 'examples_columns') else when_item_accessed('scenario', source)
            for outline in scenario.scenario_outlines if hasattr(scenario, 'scenario_outlines') else []:
                if outline.name == name:
                    return outline
            raise ValueError(f"Scenario outline '{name}' not found")
        elif hasattr(source, 'scenario_outlines'):  # It's a story
            return source.scenario_outlines[index]
        else:  # It's epics list
            story = when_item_accessed('story', source)
            return story.scenario_outlines[index]
    else:
        raise ValueError(f"Unknown item_type: {item_type}")


def then_nodes_match(nodes, expected_count=None, expected_names=None):
    """Then: Nodes match expected count and names.
    
    Consolidated function that replaces:
    - then_epic_nodes_match(epic_nodes, expected_count, expected_names)
    - then_story_nodes_match(story_nodes, expected_count, expected_names)
    
    Args:
        nodes: List of nodes to check
        expected_count: Expected number of nodes (None = don't check count)
        expected_names: Expected names (list or None = don't check names)
    """
    if expected_count is not None:
        assert len(nodes) == expected_count, f"Expected {expected_count} nodes, got {len(nodes)}"
    if expected_names is not None:
        actual_names = [node.name for node in nodes]
        assert actual_names == expected_names, f"Expected names {expected_names}, got {actual_names}"


def then_children_match(parent, expected_count=None, expected_names=None):
    """Then: Children match expected count and names.
    
    Consolidated function that replaces:
    - then_epic_children_match(epic, expected_count, expected_names)
    - then_story_group_children_match(story_group, expected_count, expected_names)
    
    Args:
        parent: Parent item (Epic, SubEpic, StoryGroup, etc.)
        expected_count: Expected number of children (None = don't check count)
        expected_names: Expected names (list or None = don't check names)
    """
    children = parent.children
    if expected_count is not None:
        assert len(children) == expected_count, f"Expected {expected_count} children, got {len(children)}"
    if expected_names is not None:
        actual_names = [child.name for child in children]
        assert actual_names == expected_names, f"Expected names {expected_names}, got {actual_names}"


def then_stories_match(expected, actual):
    """Then: Stories match expected.
    
    Consolidated function that replaces:
    - then_expected_stories_match_actual(expected_stories, actual_stories)
    - then_stories_match_expected(actual_stories, expected_stories)
    
    Args:
        expected: Expected stories (set, list, or dict)
        actual: Actual stories (set, list, or dict)
    """
    if isinstance(expected, set) and isinstance(actual, set):
        assert expected == actual, f"Expected {expected}, got {actual}"
    elif isinstance(expected, list) and isinstance(actual, list):
        assert set(expected) == set(actual), f"Expected {expected}, got {actual}"
    else:
        assert expected == actual, f"Expected {expected}, got {actual}"


def then_scenarios_match(story, expected_count=None, expected_names=None):
    """Then: Scenarios match expected count and names.
    
    Consolidated function that replaces:
    - then_story_scenarios_match_expected(story, expected_scenarios)
    
    Args:
        story: Story instance
        expected_count: Expected number of scenarios (None = don't check count)
        expected_names: Expected names (list or None = don't check names)
    """
    scenarios = story.scenarios
    if expected_count is not None:
        assert len(scenarios) == expected_count, f"Expected {expected_count} scenarios, got {len(scenarios)}"
    if expected_names is not None:
        actual_names = [scenario.name for scenario in scenarios]
        assert actual_names == expected_names, f"Expected names {expected_names}, got {actual_names}"


def then_scenario_outlines_match(scenario, expected_count=None, expected_names=None):
    """Then: Scenario outlines match expected count and names.
    
    Consolidated function that replaces:
    - then_scenario_outlines_match_expected(scenario, expected_scenarios)
    
    Args:
        scenario: Scenario or Story instance (if Story, checks scenario_outlines)
        expected_count: Expected number of scenario outlines (None = don't check count)
        expected_names: Expected names (list or None = don't check names)
    """
    from agile_bot.bots.base_bot.src.scanners.story_map import Story
    if isinstance(scenario, Story):
        outlines = scenario.scenario_outlines
    else:
        outlines = scenario.scenario_outlines if hasattr(scenario, 'scenario_outlines') else []
    if expected_count is not None:
        assert len(outlines) == expected_count, f"Expected {expected_count} scenario outlines, got {len(outlines)}"
    if expected_names is not None:
        actual_names = [outline.name for outline in outlines]
        assert actual_names == expected_names, f"Expected names {expected_names}, got {actual_names}"


def given_template_variables(template_content, variables):
    """Given: Template variables dictionary.
    
    Consolidated function that replaces:
    - given_template_variables_dict(template_content, variables)
    
    Args:
        template_content: Template content string
        variables: Variables dictionary
    
    Returns:
        Variables dictionary
    """
    return variables


def then_file_updated(file_path, expected_content):
    """Then: File updated with expected content.
    
    Consolidated function that replaces:
    - then_knowledge_graph_file_updated_with_template_variables(kg_file, expected_content)
    
    Args:
        file_path: Path to file
        expected_content: Expected content (dict or string)
    """
    from pathlib import Path
    import json
    file_path = Path(file_path)
    assert file_path.exists(), f"File {file_path} does not exist"
    actual_content = json.loads(file_path.read_text(encoding='utf-8')) if isinstance(expected_content, dict) else file_path.read_text(encoding='utf-8')
    if isinstance(expected_content, dict):
        assert actual_content == expected_content, f"Expected {expected_content}, got {actual_content}"
    else:
        assert actual_content == expected_content, f"Expected {expected_content}, got {actual_content}"


def then_instructions_match(instructions, expected_content):
    """Then: Instructions match expected content.
    
    Consolidated function that replaces:
    - then_instructions_match_expected(instructions, expected_content)
    
    Args:
        instructions: Instructions dict or string
        expected_content: Expected content (dict or string)
    """
    if isinstance(expected_content, dict) and isinstance(instructions, dict):
        assert instructions == expected_content, f"Expected {expected_content}, got {instructions}"
    else:
        assert str(instructions) == str(expected_content), f"Expected {expected_content}, got {instructions}"


def given_action_outputs(outputs):
    """Given: Action outputs dictionary.
    
    Consolidated function that replaces:
    - given_action_outputs_dict(outputs)
    
    Args:
        outputs: Outputs dictionary
    
    Returns:
        Outputs dictionary
    """
    return outputs


def given_action_duration(duration):
    """Given: Action duration in seconds.
    
    Consolidated function that replaces:
    - given_action_duration_seconds(duration)
    
    Args:
        duration: Duration in seconds
    
    Returns:
        Duration value
    """
    return duration


def given_action_config_copied(source_config, target_config):
    """Given: Action config copied from source.
    
    Consolidated function that replaces:
    - given_action_config_copied_from_source(source_config, target_config)
    
    Args:
        source_config: Source config dict
        target_config: Target config dict (will be updated)
    
    Returns:
        Updated target_config
    """
    target_config.update(source_config)
    return target_config


def given_behavior_instructions(behavior, instructions):
    """Given: Behavior instructions dictionary.
    
    Consolidated function that replaces:
    - given_behavior_instructions_dict(behavior, instructions)
    
    Args:
        behavior: Behavior name
        instructions: Instructions dict
    
    Returns:
        Instructions dictionary
    """
    return instructions


def given_action_setup(action_type, bot_directory, behavior):
    """Given: Action setup for build action.
    
    Consolidated function that replaces:
    - given_build_action_setup(bot_directory, behavior)
    
    Args:
        action_type: Type of action ('build')
        bot_directory: Bot directory path
        behavior: Behavior name
    
    Returns:
        Action instance or setup result
    """
    from pathlib import Path
    from conftest import create_base_actions_structure
    from agile_bot.bots.base_bot.test.test_helpers import bootstrap_env
    from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
    from agile_bot.bots.base_bot.src.bot.behavior import Behavior
    from agile_bot.bots.base_bot.src.actions.build.build_action import BuildKnowledgeAction
    
    create_base_actions_structure(bot_directory)
    bot_paths = BotPaths(bot_directory=bot_directory)
    behavior_obj = Behavior(name=behavior, bot_paths=bot_paths, bot_instance=None)
    action_obj = BuildKnowledgeAction(behavior=behavior_obj, action_config=None)
    return action_obj


def when_instructions_extracted(instructions, extract_type):
    """When: Extract template variables from instructions.
    
    Consolidated function that replaces:
    - when_extract_template_variables_from_instructions(instructions)
    
    Args:
        instructions: Instructions dict or string
        extract_type: Type of extraction ('template_variables')
    
    Returns:
        Extracted template variables dict
    """
    if extract_type == 'template_variables':
        import re
        if isinstance(instructions, dict):
            instructions_str = str(instructions)
        else:
            instructions_str = instructions
        # Find all {{variable}} patterns
        pattern = r'\{\{(\w+)\}\}'
        matches = re.findall(pattern, instructions_str)
        return {var: None for var in set(matches)}
    else:
        raise ValueError(f"Unknown extract_type: {extract_type}")


def when_action_executes(action_type, bot_directory, behavior, **execution_params):
    """When: Action executes.
    
    Consolidated function that replaces BUILD KNOWLEDGE functions:
    - when_build_action_injects_template(bot_name, behavior, bot_directory)
    - when_build_action_loads_and_merges_instructions(bot_name, behavior, bot_directory)
    - when_build_action_loads_and_injects_all_instructions(action_obj)
    - when_build_action_injects_template_for_increments(bot_name, behavior, bot_directory)
    
    Args:
        action_type: Type of action ('build')
        bot_directory: Bot directory path
        behavior: Behavior name
        **execution_params: Additional parameters:
            - bot_name: Bot name (default: 'story_bot')
            - action_obj: Existing action object (if provided, uses it instead of creating new)
            - return_action: If True, returns (action_obj, instructions) tuple (default: False)
            - execute: If True, executes action (default: True for build)
            - template_type: Template type ('default' or 'increments')
    
    Returns:
        instructions dict, or (action_obj, instructions) tuple if return_action=True
    """
    from pathlib import Path
    from conftest import create_base_actions_structure
    from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
    from agile_bot.bots.base_bot.src.bot.behavior import Behavior
    from agile_bot.bots.base_bot.src.actions.build.build_action import BuildKnowledgeAction
    import json
    
    bot_name = execution_params.get('bot_name', 'story_bot')
    action_obj = execution_params.get('action_obj')
    return_action = execution_params.get('return_action', False)
    execute = execution_params.get('execute', True)
    template_type = execution_params.get('template_type', 'default')
    
    if action_obj is None:
        # Create action object
        create_base_actions_structure(bot_directory)
        
        if action_type == 'build':
            # For build actions, we need to create behavior
            # Use the same pattern as _create_behavior from test_build_knowledge.py
            from agile_bot.bots.base_bot.test.test_helpers import create_actions_workflow_json
            from agile_bot.bots.base_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files
            
            create_actions_workflow_json(bot_directory, behavior)
            create_minimal_guardrails_files(bot_directory, behavior, bot_name)
            
            bot_paths = BotPaths(bot_directory=bot_directory)
            behavior_obj = Behavior(name=behavior, bot_paths=bot_paths, bot_instance=None)
            
            # Check if we need action_config from behavior.json
            action_config = None
            behavior_json_path = bot_directory / 'behaviors' / behavior / 'behavior.json'
            if behavior_json_path.exists():
                behavior_config_data = json.loads(behavior_json_path.read_text(encoding='utf-8'))
                actions_workflow = behavior_config_data.get('actions_workflow', {}).get('actions', [])
                for action_dict in actions_workflow:
                    if action_dict.get('name') == 'build':
                        action_config = action_dict
                        break
            
            action_obj = BuildKnowledgeAction(behavior=behavior_obj, action_config=action_config)
        else:
            raise ValueError(f"Unsupported action_type: {action_type}")
    
    if execute:
        # Execute action with typed context
        from agile_bot.bots.base_bot.src.actions.action_context import ScopeActionContext
        result = action_obj.do_execute(ScopeActionContext())
        instructions = result.get('instructions', result)
    else:
        # Just return merged instructions without executing
        instructions = action_obj.instructions.copy()
        instructions['action'] = action_type
        instructions['behavior'] = behavior
        if hasattr(action_obj, '_base_config') and action_obj._base_config:
            instructions['behavior_instructions'] = action_obj._base_config.get('instructions', [])
    
    if return_action:
        return action_obj, instructions
    else:
        return instructions


