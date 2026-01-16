"""
Common Test Helpers for Invoke Bot Tests

Provides reusable helpers for bot setup and assertions used across:
- test_invoke_bot_directly.py (Direct invocation)
- test_navigate_behaviors_using_repl_commands.py (REPL commands)
- All other navigation and REPL test files

DRY principle: setup bot once, reuse everywhere

NOTE: This file is in the OLD test area (base_bot/test/) and will eventually be removed.
New tests in agile_bot/test/ use test_bot_setup_helpers.py instead.
"""
import os
import json
from pathlib import Path

from agile_bot.bots.base_bot.src.bot.bot import Bot

import sys
repo_root = Path(__file__).parent.parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from agile_bot.test.domain.test_helpers import (
    create_actions_workflow_json,
    create_base_actions_structure,
    bootstrap_env,
    create_bot_config_file
)
from agile_bot.test.test_execute_behavior_actions import create_minimal_guardrails_files


# ============================================================================
# BOT SETUP HELPERS - Used by Direct and REPL tests
# ============================================================================

def setup_test_bot(tmp_path, behaviors: list[str]) -> tuple[Bot, Path]:
    """
    Setup test bot with behaviors for Invoke Bot tests.
    
    Returns: (bot, workspace_dir)
    
    Used by:
    - test_invoke_bot_directly.py (Direct invocation)
    - test_navigate_behaviors_using_repl_commands.py (REPL commands)
    - All other navigation and REPL test files
    
    Args:
        tmp_path: pytest tmp_path fixture
        behaviors: List of behavior names to create (e.g., ['shape', 'discovery'])
    
    Returns:
        tuple: (Bot instance, workspace_directory Path)
        
    Example:
        bot, workspace = setup_test_bot(tmp_path, ['shape', 'discovery'])
        bot.behaviors.navigate_to('shape')
    """
    bot_dir = tmp_path / 'agile_bot' / 'bots' / 'story_bot'
    workspace_dir = tmp_path / 'workspace'
    bot_dir.mkdir(parents=True, exist_ok=True)
    workspace_dir.mkdir(parents=True, exist_ok=True)

    create_base_actions_structure(bot_dir)
    create_bot_config_file(bot_dir, 'story_bot', behaviors)

    for idx, behavior_name in enumerate(behaviors, start=1):
        create_actions_workflow_json(bot_dir, behavior_name, order=idx)
        create_minimal_guardrails_files(bot_dir, behavior_name, 'story_bot')

    bootstrap_env(bot_dir, workspace_dir)
    bot = Bot(
        bot_name='story_bot',
        bot_directory=bot_dir,
        config_path=bot_dir / 'bot_config.json'
    )
    return bot, workspace_dir


def create_behavior_action_state(workspace_dir: Path, bot_name: str, 
                                  behavior: str, action: str,
                                  operation: str = 'instructions') -> Path:
    """
    Create behavior_action_state.json file with specified state.
    
    Used by:
    - REPL tests (need initial state for command parsing)
    - Direct tests (need state for sequential navigation)
    
    Args:
        workspace_dir: Workspace directory path
        bot_name: Bot name (e.g., 'story_bot')
        behavior: Behavior name (e.g., 'shape')
        action: Action name (e.g., 'clarify')
        operation: Operation name (default: 'instructions')
        
    Returns:
        Path: state_file path
        
    Example:
        state_file = create_behavior_action_state(
            workspace, 'story_bot', 'shape', 'clarify', 'instructions'
        )
    """
    state_data = {
        'current_behavior': f'{bot_name}.{behavior}',
        'current_action': f'{bot_name}.{behavior}.{action}',
        'operation': operation,
        'working_directory': str(workspace_dir),
        'timestamp': '2025-12-26T10:00:00.000000'
    }
    
    state_file = workspace_dir / 'behavior_action_state.json'
    state_file.write_text(json.dumps(state_data), encoding='utf-8')
    return state_file


def read_behavior_action_state(workspace_dir: Path) -> dict:
    """
    Read and parse behavior_action_state.json.
    
    Used by:
    - Direct tests (verify state persistence)
    - REPL tests (verify command updates state)
    
    Returns:
        dict: Parsed state data
        
    Example:
        state = read_behavior_action_state(workspace)
        assert state['current_behavior'] == 'story_bot.shape'
    """
    state_file = workspace_dir / 'behavior_action_state.json'
    assert state_file.exists(), "State file should exist"
    return json.loads(state_file.read_text(encoding='utf-8'))


# ============================================================================
# ASSERTION HELPERS - Verify expected outcomes
# ============================================================================

def assert_bot_at_behavior_action(bot: Bot, behavior_name: str, 
                                   action_name: str):
    """
    Assert bot is at specified behavior and action.
    
    Used by:
    - Direct tests (verify navigation worked)
    - REPL tests (verify command navigated correctly)
    
    Example:
        assert_bot_at_behavior_action(bot, 'shape', 'clarify')
    """
    assert bot.behaviors.current.name == behavior_name
    assert bot.behaviors.current.actions.current_action_name == action_name


def assert_state_file_shows_behavior_action(workspace_dir: Path, 
                                              bot_name: str,
                                              behavior: str, 
                                              action: str):
    """
    Assert state file shows expected behavior and action.
    
    Used by:
    - Direct tests (verify state persistence)
    - REPL tests (verify commands persist state)
    
    Example:
        assert_state_file_shows_behavior_action(
            workspace, 'story_bot', 'shape', 'clarify'
        )
    """
    state = read_behavior_action_state(workspace_dir)
    assert state['current_behavior'] == f'{bot_name}.{behavior}'
    assert state['current_action'].startswith(f'{bot_name}.{behavior}.{action}')


def assert_action_in_completed_list(workspace_dir: Path, bot_name: str,
                                      behavior: str, action: str):
    """
    Assert action appears in completed_actions list in state file.
    
    Used by:
    - Direct tests (verify close_current marked action complete)
    - Sequential navigation tests
    
    Example:
        assert_action_in_completed_list(workspace, 'story_bot', 'shape', 'clarify')
    """
    state = read_behavior_action_state(workspace_dir)
    completed = [a.get('action_state') for a in state.get('completed_actions', [])]
    assert f'{bot_name}.{behavior}.{action}' in completed


# ============================================================================
# SCOPE ASSERTION HELPERS - Verify scope configuration
# ============================================================================

def assert_scope_is_set(bot: Bot, scope_type: str, scope_value: list):
    """
    Assert bot scope is set with specified type and value.
    
    Used by:
    - Manage Scope tests
    
    Example:
        assert_scope_is_set(bot, 'story', ['Epic Name'])
    """
    assert bot.scope.type == scope_type
    assert bot.scope.value == scope_value
    assert bot.scope.is_active()


def assert_scope_is_cleared(bot: Bot):
    """
    Assert bot scope is cleared (not active).
    
    Used by:
    - Manage Scope tests
    
    Example:
        assert_scope_is_cleared(bot)
    """
    assert not bot.scope.is_active()
    assert bot.scope.type is None


# ============================================================================
# ACTIVITY LOG HELPERS - Track action execution
# ============================================================================

def read_activity_log(workspace_dir: Path) -> list:
    """
    Read and parse activity_log.json.
    
    Used by:
    - Track Activity tests
    
    Returns:
        list: Parsed activity log entries
        
    Example:
        activity_log = read_activity_log(workspace)
        assert len(activity_log) > 0
    """
    activity_log_file = workspace_dir / 'activity_log.json'
    if not activity_log_file.exists():
        return []
    return json.loads(activity_log_file.read_text(encoding='utf-8'))


def assert_activity_logged(workspace_dir: Path, action_state: str, 
                            event_type: str):
    """
    Assert action is logged in activity log with specified event type.
    
    Used by:
    - Track Activity tests
    
    Args:
        workspace_dir: Workspace directory path
        action_state: Action state (e.g., 'story_bot.shape.clarify')
        event_type: Event type (e.g., 'start', 'complete')
        
    Example:
        assert_activity_logged(workspace, 'story_bot.shape.clarify', 'start')
    """
    activity_log = read_activity_log(workspace_dir)
    matching_entries = [
        entry for entry in activity_log
        if entry.get('action_state') == action_state 
        and entry.get('event') == event_type
    ]
    assert len(matching_entries) > 0, \
        f"No {event_type} event found for {action_state} in activity log"

