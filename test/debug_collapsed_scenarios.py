"""Debug: scenarios.render -> scenarios -> submit flow.
Run: pytest test/debug_collapsed_scenarios.py -v -s
"""
import os
from pathlib import Path

import pytest

from bot.bot import Bot
from cli.cli_session import CLISession


@pytest.fixture
def helper(tmp_path):
    repo_root = Path(__file__).parent.parent
    bot_dir = repo_root / 'bots' / 'story_bot'
    workspace = tmp_path / 'workspace'
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / 'scope.json').write_text('{}', encoding='utf-8')
    os.environ['BOT_DIRECTORY'] = str(bot_dir)
    os.environ['WORKING_AREA'] = str(workspace)
    config_path = bot_dir / 'bot_config.json'
    bot = Bot('story_bot', bot_dir, config_path, workspace_path=workspace)
    cli = CLISession(bot=bot, workspace_directory=workspace)
    return {'bot': bot, 'cli': cli}


def test_scenarios_render_then_scenarios_then_submit(helper):
    """
    GIVEN: CLI at scenarios.render
    WHEN: User runs 'scenarios' (behavior only), then 'submit'
    THEN: Submit should start from first action (clarify), NOT render
    """
    bot, cli = helper['bot'], helper['cli']

    # Step 1: Navigate to scenarios.render
    r1 = cli.execute_command('scenarios.render')
    print(f"[1] scenarios.render: {r1.status}")
    assert r1.status != 'error', r1.output

    # Check current action is render
    r_status1 = cli.execute_command('status')
    if hasattr(r_status1, 'output') and 'current_action' not in str(r_status1.output):
        bot_data = bot  # status returns bot in TTY mode
    else:
        bot_data = bot
    current_behavior = bot.behaviors.current.name if bot.behaviors.current else None
    current_action = bot.behaviors.current.actions.current_action_name if (bot.behaviors.current and bot.behaviors.current.actions) else None
    print(f"    After scenarios.render: behavior={current_behavior}, action={current_action}")
    assert current_action == 'render', f"Expected render, got {current_action}"

    # Step 2: Navigate to scenarios (behavior only - collapsed)
    r2 = cli.execute_command('scenarios')
    print(f"[2] scenarios (behavior only): {r2.status}")

    # Check current action - should be None (behavior level, no action stored)
    current_action_after = bot.behaviors.current.actions.current_action_name if (bot.behaviors.current and bot.behaviors.current.actions) else None
    first_action = bot._first_non_skip_action('scenarios') or (bot.behaviors.current.actions.names[0] if (bot.behaviors.current and bot.behaviors.current.actions.names) else None)
    print(f"    After scenarios: action={current_action_after} (expected None at behavior level), first_action={first_action}")

    assert current_action_after is None, (
        f"Collapsed behavior 'scenarios' should have no action in state, got {current_action_after}"
    )

    # Step 3: Submit - should submit from first action (submit uses first when at behavior level)
    r3 = cli.execute_command('submit')
    print(f"[3] submit: {r3.status}")
    assert r3.status == 'success', f"Submit should succeed, got: {r3.output}"
    if isinstance(r3.output, str) and 'behavior' in r3.output.lower():
        assert first_action in r3.output.lower(), (
            f"Submit should be from first workflow action {first_action}, output: {r3.output[:300]}"
        )


def test_submit_at_action_level_excludes_next_behavior(helper):
    """
    GIVEN: User at scenarios.render (action level)
    WHEN: User runs submit
    THEN: Instructions include only scenarios actions, NOT subsequent behaviors (tests, code)
    """
    bot = helper['bot']
    bot.behaviors.navigate_to('scenarios')
    bot.behaviors.current.actions.navigate_to('render')
    result = bot.submit_current_action()
    assert result.get('status') == 'success', result
    text = result.get('instructions', '') or ''
    # At action level, we must NOT append next behavior's instructions
    assert 'tests.clarify' not in text and 'tests.build' not in text, (
        "At action level (scenarios.render), submit should not include next behavior (tests)"
    )
    assert 'Action Instructions - render' in text or 'render' in text.lower(), (
        "Should include render action instructions"
    )
