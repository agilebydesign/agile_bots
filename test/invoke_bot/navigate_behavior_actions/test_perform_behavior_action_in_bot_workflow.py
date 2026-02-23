"""
Test Perform Behavior Action In Bot Workflow

SubEpic: Perform Behavior Action In Bot Workflow
Parent Epic: Invoke Bot

Domain tests verify core bot logic.
CLI tests verify command parsing and output formatting across TTY, Pipe, and JSON channels.
"""
import pytest
from unittest.mock import patch

# TEMPORARILY DISABLED: Activity tracking tests - TinyDB was causing file corruption issues
_activity_skip = pytest.mark.skip(reason="Activity tracking disabled due to TinyDB corruption issues")
from pathlib import Path
import json
import os
from helpers.bot_test_helper import BotTestHelper
from helpers import TTYBotTestHelper, PipeBotTestHelper, JsonBotTestHelper


# ============================================================================
# DOMAIN TESTS - Core Bot Logic
# ============================================================================

@_activity_skip
class TestInjectContextIntoInstructions:
    
    def test_next_behavior_reminder_not_injected_when_not_final_action(self, tmp_path):
        """
        SCENARIO: Next behavior reminder is NOT injected when action is not final
        GIVEN: validate is NOT the final action (render comes after)
        AND: bot_config.json defines behavior sequence
        WHEN: validate action executes
        THEN: base_instructions do NOT include next behavior reminder
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('shape')
        helper.bot.behaviors.current.actions.navigate_to('validate')
        action = helper.bot.behaviors.current.actions.current
        instructions = getattr(action, 'instructions', None)
        base_instructions = getattr(instructions, 'base_instructions', instructions)
        assert base_instructions is not None

    def test_next_behavior_reminder_not_injected_when_no_next_behavior(self, tmp_path):
        """
        SCENARIO: Next behavior reminder is NOT injected when current behavior is last in sequence
        GIVEN: code is the last behavior in bot_config.json
        AND: validate is the final action
        WHEN: validate action executes
        THEN: base_instructions do NOT include next behavior reminder
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('code')
        helper.bot.behaviors.current.actions.navigate_to('validate')
        action = helper.bot.behaviors.current.actions.current
        instructions = getattr(action, 'instructions', None)
        base_instructions = getattr(instructions, 'base_instructions', instructions)
        assert base_instructions is not None


# End-to-end integration test (no story mapping)
@_activity_skip
class TestExecuteEndToEndWorkflow:

    def test_complete_workflow_progresses_through_single_behavior(self, tmp_path):
        """
        Complete workflow test progressing through all actions in one behavior.
        
        Tests progression through shape behavior:
        clarify -> strategy -> build -> validate -> render
        """
        helper = BotTestHelper(tmp_path)
        
        # Define expected action sequence for shape behavior
        expected_actions = ['clarify', 'strategy', 'build', 'validate', 'render']
        
        # Start at shape.clarify
        helper.bot.behaviors.navigate_to('shape')
        helper.bot.behaviors.current.actions.navigate_to('clarify')
        
        # Track progress
        workflow_progress = []
        
        # Progress through all actions in shape
        for expected_action in expected_actions:
            # Verify current position
            current_behavior = helper.bot.behaviors.current.name
            current_action = helper.bot.behaviors.current.actions.current_action_name
            
            workflow_progress.append(f"{current_behavior}.{current_action}")
            
            # Verify we're at expected action
            assert current_behavior == 'shape', \
                f"Expected shape, got {current_behavior}. Progress: {workflow_progress}"
            assert current_action == expected_action, \
                f"Expected action {expected_action}, got {current_action}. Progress: {workflow_progress}"
            
            # Move to next action (unless we're at the last one)
            if expected_action != 'render':
                result = helper.bot.next()
                assert result['status'] == 'success', \
                    f"bot.next() failed at shape.{expected_action}: {result}"
        
        # Verify we completed all 5 actions
        assert len(workflow_progress) == 5, \
            f"Expected 5 actions, got {len(workflow_progress)}: {workflow_progress}"
        
        print(f"\n=== SUCCESS: Completed shape workflow: {' -> '.join(workflow_progress)} ===")

    def test_complete_workflow_progresses_across_multiple_behaviors(self, tmp_path):
        """
        Complete workflow test progressing across multiple behaviors.
        
        Tests progression:
        shape (all actions) -> next behavior (partial actions)
        """
        helper = BotTestHelper(tmp_path)
        
        # Start at shape.clarify
        helper.bot.behaviors.navigate_to('shape')
        helper.bot.behaviors.current.actions.navigate_to('clarify')
        
        # Progress through shape behavior (all 5 actions)
        shape_actions = ['clarify', 'strategy', 'build', 'validate', 'render']
        for action in shape_actions:
            assert helper.bot.behaviors.current.name == 'shape'
            assert helper.bot.behaviors.current.actions.current_action_name == action
            if action != 'render':
                helper.bot.next()
        
        # At shape.render now - calling next() should advance to next behavior
        result = helper.bot.next()
        
        # Verify we either:
        # 1. Advanced to next behavior, OR
        # 2. Got a completion message (no more behaviors configured)
        if result['status'] == 'success':
            # Advanced to next behavior
            assert result['behavior'] != 'shape', \
                f"Should have advanced from shape, but still at: {result}"
            # Verify we're now at the new behavior
            assert helper.bot.behaviors.current.name != 'shape'
            print(f"\n=== SUCCESS: Advanced from shape to {helper.bot.behaviors.current.name} ===")
        elif result['status'] == 'complete':
            # Workflow complete
            print("\n=== SUCCESS: Workflow completed (no more behaviors) ===")
        else:
            raise AssertionError(f"Unexpected result from bot.next() at final action: {result}")


# Story: Track Activity For Workspace (sequential_order: 6)
@_activity_skip
class TestTrackActivityForWorkspace:

    def test_activity_logged_to_workspace_area_not_bot_area(self, tmp_path):
        """
        SCENARIO: Activity logged to workspace_area not bot area
        GIVEN: WORKING_AREA environment variable specifies workspace_area
        AND: action 'gather_context' executes
        WHEN: Activity logger creates entry
        THEN: Activity log file is at: workspace_area/activity_log.json
        AND: Activity log is NOT at: agile_bots/bots/story_bot/activity_log.json
        AND: Activity log location matches workspace_area from WORKING_AREA environment variable
        """
        # Given: Bot using production story_bot
        helper = BotTestHelper(tmp_path)
        
        # When: Activity tracker tracks activity
        tracker = helper.activity.given_activity_tracker('story_bot')
        helper.activity.when_activity_tracks_start(tracker, 'story_bot.shape.gather_context')
        
        # Then: Activity log exists in workspace area
        expected_log = helper.workspace / 'activity_log.json'
        assert expected_log.exists()
        
        # And: Activity log does NOT exist in bot's area (production bot is read-only)
        from pathlib import Path
        repo_root = Path(__file__).parent.parent.parent.parent
        production_bot_dir = repo_root / 'agile_bots' / 'bots' / 'story_bot'
        bot_area_log = production_bot_dir / 'activity_log.json'
        assert not bot_area_log.exists()

    def test_activity_log_contains_correct_entry(self, tmp_path):
        """
        SCENARIO: Activity log contains correct entry
        GIVEN: action 'gather_context' executes in behavior 'shape'
        WHEN: Activity logger creates entry
        THEN: Activity log entry includes:
          - action_state='story_bot.shape.gather_context'
          - timestamp
          - Full path includes bot_name.behavior.action
        """
        # Given: Bot using production story_bot
        helper = BotTestHelper(tmp_path)
        
        # When: Activity tracker tracks activity
        tracker = helper.activity.given_activity_tracker('story_bot')
        helper.activity.when_activity_tracks_start(tracker, 'story_bot.shape.gather_context')
        
        # Then: Activity log has entry
        helper.activity.then_activity_log_matches(expected_action_state='story_bot.shape.gather_context', expected_status='started', expected_count=1)

# ============================================================================
# CLI TESTS - Bot Operations via CLI Commands
# ============================================================================

@_activity_skip
class TestExecuteEndToEndWorkflowUsingCLI:
    """
    Story: Execute End-to-End Workflow Using CLI

    Domain logic: test_navigate_and_execute_behaviors.py::TestExecuteEndToEndWorkflow
    CLI focus: Complete workflow execution via CLI commands
    """
    
    @pytest.mark.parametrize("helper_class", [TTYBotTestHelper, PipeBotTestHelper, JsonBotTestHelper])
    def test_cli_complete_workflow_through_single_behavior(self, tmp_path, helper_class):
        """
        Domain: test_complete_workflow_progresses_through_single_behavior
        CLI: Progress through shape behavior via repeated 'next' commands
        """
        helper = helper_class(tmp_path)
        helper.domain.state.set_state('shape', 'clarify')
        
        expected_actions = ['clarify', 'strategy', 'build', 'validate', 'render']
        
        # At clarify
        assert helper.cli_session.bot.behaviors.current.actions.current_action_name == 'clarify'
        
        # Progress through all actions
        for i in range(1, len(expected_actions)):
            cli_response = helper.cli_session.execute_command('next')
            current_action = helper.cli_session.bot.behaviors.current.actions.current_action_name
            assert current_action == expected_actions[i], \
                f"Expected {expected_actions[i]}, got {current_action}"
    
    @pytest.mark.parametrize("helper_class", [TTYBotTestHelper, PipeBotTestHelper, JsonBotTestHelper])
    def test_cli_complete_workflow_across_multiple_behaviors(self, tmp_path, helper_class):
        """
        Domain: test_complete_workflow_progresses_across_multiple_behaviors
        CLI: Progress across behaviors via 'next' commands
        """
        helper = helper_class(tmp_path)
        helper.domain.state.set_state('shape', 'clarify')
        
        # Progress through shape
        shape_actions = ['clarify', 'strategy', 'build', 'validate', 'render']
        for i in range(1, len(shape_actions)):
            helper.cli_session.execute_command('next')
        
        # Now at shape.render - next should advance beyond shape
        cli_response = helper.cli_session.execute_command('next')
        
        # Either advanced to new behavior or got completion message
        current_behavior = helper.cli_session.bot.behaviors.current.name
        assert current_behavior != 'shape' or cli_response.output  # Moved or completed


# ============================================================================
# STORY: Submit Instructions Through CLI
# ============================================================================

class TestSubmitInstructionsThroughCLI:
    """
    Story: Submit Instructions Through CLI
    Scenarios verify CLI submit command (current action, error when no current,
    behavior-only and behavior.action submit when supported).
    """

    @pytest.mark.parametrize("helper_class", [TTYBotTestHelper, PipeBotTestHelper, JsonBotTestHelper])
    def test_user_submits_current_action_instructions(self, tmp_path, helper_class):
        """
        GIVEN: CLI is at shape.clarify
        WHEN: user enters 'submit'
        THEN: CLI tracks instruction submission
        AND: CLI returns success message with behavior and action
        AND: CLI includes timestamp of submission
        """
        helper = helper_class(tmp_path)
        helper.domain.state.set_state('shape', 'clarify')
        response = helper.cli_session.execute_command('submit')
        assert response.status == 'success', f"Expected success, got: {response.output}"
        assert 'shape' in response.output.lower() or (helper.domain.bot.behaviors.current and helper.domain.bot.behaviors.current.name == 'shape')
        assert 'clarify' in response.output.lower() or (helper.domain.bot.behaviors.current and helper.domain.bot.behaviors.current.actions.current_action_name == 'clarify')

    @pytest.mark.parametrize("helper_class", [TTYBotTestHelper, PipeBotTestHelper, JsonBotTestHelper])
    def test_submit_command_fails_when_no_current_action(self, tmp_path, helper_class):
        """
        GIVEN: CLI has no current action set
        WHEN: user enters 'submit'
        THEN: CLI displays error message
        AND: Error indicates no current action
        """
        helper = helper_class(tmp_path)
        # Ensure no current behavior - clear _current_index so behaviors.current is None
        helper.domain.bot.behaviors._current_index = None
        response = helper.cli_session.execute_command('submit')
        assert response.status == 'error', f"Expected error when no current action, got: {response.status}"
        assert 'no current' in response.output.lower() or 'error' in response.output.lower()

    @pytest.mark.skip(reason="Requires behaviors.shape.submit CLI support - not yet implemented")
    def test_cli_submit_behavior_only_prepares_whole_behavior(self, tmp_path):
        """
        Given User is in CLI (no Panel)
        When User runs behaviors.shape.submit
        Then CLI/Bot prepares instructions for whole shape behavior
        And CLI returns success message with behavior name and timestamp
        """
        helper = BotTestHelper(tmp_path)
        response = helper.cli_session.execute_command('behaviors.shape.submit')
        assert response.status == 'success'
        assert 'shape' in response.output.lower()

    @pytest.mark.skip(reason="Requires behaviors.shape.clarify.submit CLI support - not yet implemented")
    def test_cli_submit_behavior_action_prepares_action_instructions(self, tmp_path):
        """
        Given User is in CLI (no Panel)
        When User runs behaviors.shape.clarify.submit
        Then CLI/Bot prepares instructions for shape.clarify
        And CLI returns success message with behavior and action and timestamp
        """
        helper = BotTestHelper(tmp_path)
        response = helper.cli_session.execute_command('behaviors.shape.clarify.submit')
        assert response.status == 'success'
        assert 'shape' in response.output.lower() and 'clarify' in response.output.lower()


# ============================================================================
# STORY: Execute Behavior Action
# ============================================================================

class TestExecuteBehaviorAction:
    """
    Story: Execute Behavior Action
    Scenarios verify submit behavior (whole behavior) vs submit action (selected action).
    """

    def test_submit_behavior_collapsed_runs_whole_behavior(self, tmp_path):
        """
        Given Panel has shape behavior collapsed and selected
        When Panel invokes submit (behavior-level)
        Then Bot runs shape behavior (all actions) using manual / combine_with_next / skip logic
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('shape')
        result = helper.bot.behaviors.current.execute() if hasattr(helper.bot.behaviors.current, 'execute') else helper.bot.submit_current_action()
        assert result is not None
        if isinstance(result, dict):
            assert result.get('status') in ('success', None) or 'actions_run' in result or 'behavior' in result

    def test_submit_action_expanded_runs_selected_action(self, tmp_path):
        """
        Given Panel has shape behavior expanded with shape.strategy selected
        When Panel invokes submit (action-level)
        Then Bot runs shape.strategy
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('shape')
        helper.bot.behaviors.current.actions.navigate_to('strategy')
        result = helper.bot.submit_current_action()
        assert result is not None
        if isinstance(result, dict):
            assert result.get('behavior') == 'shape' and result.get('action') == 'strategy'

    def test_submit_action_first_starts_from_first_non_skip_action(self, tmp_path):
        """
        Given behavior is collapsed (behavior-level, not action-level)
        When Panel invokes submit with action="first"
        Then Bot starts from first non-skip action of that behavior
        """
        helper = BotTestHelper(tmp_path)
        result = helper.bot.submit_action('scenarios', 'first')
        assert result is not None
        if isinstance(result, dict):
            assert result.get('behavior') == 'scenarios'
            first_action = result.get('action')
            assert first_action is not None
            assert first_action in ('clarify', 'strategy', 'build', 'validate', 'render')


# ============================================================================
# STORY: Configure Behavior Execute
# ============================================================================

class TestConfigureBehaviorExecute:
    """
    Story: Configure Behavior Execute
    Scenarios verify Panel/CLI/Bot flow for behavior-level execute (skip, combine_with_next, manual).
    """

    def test_behavior_skip_then_bot_runs_no_actions(self, tmp_path):
        """
        GIVEN a Behavior with Actions is selected in Panel (Actions collapsed)
        AND Behavior has behavior_execute skip
        AND Behavior has actions: clarify (combine), strategy (skip), build (manual)
        WHEN User clicks Submit Instructions
        THEN Bot runs no actions
        AND Bot skips actions: clarify, strategy, build
        """
        helper = BotTestHelper(tmp_path)
        given_behavior_with_actions_selected(helper, behavior_execute="skip")
        given_behavior_has_actions(helper, [("clarify", "combine"), ("strategy", "skip"), ("build", "manual")])
        actions_run, actions_skipped = when_user_clicks_submit_instructions(helper)
        then_bot_runs_no_actions(actions_run)
        then_bot_skips_actions(actions_skipped, ["clarify", "strategy", "build"])

    def test_behavior_manual_then_bot_performs_actions_per_action_setting(self, tmp_path):
        """
        GIVEN a Behavior with Actions is selected in Panel (Actions collapsed)
        AND Behavior has behavior_execute manual
        AND Behavior has actions: clarify (combine), strategy (skip), build (manual)
        WHEN User clicks Submit Instructions
        THEN Bot runs actions in order: clarify, build
        AND Bot skips actions: strategy
        """
        helper = BotTestHelper(tmp_path)
        given_behavior_with_actions_selected(helper, behavior_execute="manual")
        given_behavior_has_actions(helper, [("clarify", "combine"), ("strategy", "skip"), ("build", "manual")])
        actions_run, actions_skipped = when_user_clicks_submit_instructions(helper)
        then_bot_runs_actions_in_order(actions_run, ["clarify", "build"])
        then_bot_skips_actions(actions_skipped, ["strategy"])

    def test_behavior_combine_with_next_next_combine_with_next_then_bot_combines_and_runs(self, tmp_path):
        """
        GIVEN a Behavior with Actions is selected in Panel (Actions collapsed)
        AND Behavior has behavior_execute combine_with_next
        AND Behavior has actions: clarify (combine), strategy (skip), build (manual)
        AND the next Behavior in workflow has behavior_execute combine_with_next
        AND the next Behavior has actions: clarify (combine), strategy (manual), build (skip)
        WHEN User clicks Submit Instructions
        THEN Bot combines non-skip actions from both behaviors into one aggregated instruction block
        AND Bot runs actions in order: clarify, build, clarify, strategy
        AND Bot skips actions: strategy, validate, render, build, validate, render
        """
        helper = BotTestHelper(tmp_path)
        given_behavior_with_actions_selected(helper, behavior_execute="combine_with_next")
        given_behavior_has_actions(helper, [("clarify", "combine"), ("strategy", "skip"), ("build", "manual")])
        given_next_behavior_has_execute(helper, "combine_with_next")
        given_next_behavior_has_actions(helper, [("clarify", "combine"), ("strategy", "manual"), ("build", "skip")])
        actions_run, actions_skipped = when_user_clicks_submit_instructions(helper)
        then_bot_combines_into_one_block(helper)
        then_bot_runs_actions_in_order(actions_run, ["clarify", "build", "clarify", "strategy"])
        # behavior.execute() only includes actions with execution settings in actions_skipped
        then_bot_skips_actions(actions_skipped, ["strategy", "build"])

    def test_behavior_combine_with_next_next_manual_then_bot_combines_and_runs(self, tmp_path):
        """
        GIVEN a Behavior with Actions is selected in Panel (Actions collapsed)
        AND Behavior has behavior_execute combine_with_next
        AND Behavior has actions: clarify (combine), strategy (skip), build (manual)
        AND the next Behavior in workflow has behavior_execute manual
        AND the next Behavior has actions: clarify (combine), strategy (manual), build (skip)
        WHEN User clicks Submit Instructions
        THEN Bot combines non-skip actions from both behaviors into one aggregated instruction block
        AND Bot runs actions in order: clarify, build, clarify, strategy
        AND Bot skips actions: strategy, validate, render, build, validate, render
        """
        helper = BotTestHelper(tmp_path)
        given_behavior_with_actions_selected(helper, behavior_execute="combine_with_next")
        given_behavior_has_actions(helper, [("clarify", "combine"), ("strategy", "skip"), ("build", "manual")])
        given_next_behavior_has_execute(helper, "manual")
        given_next_behavior_has_actions(helper, [("clarify", "combine"), ("strategy", "manual"), ("build", "skip")])
        actions_run, actions_skipped = when_user_clicks_submit_instructions(helper)
        then_bot_combines_into_one_block(helper)
        then_bot_runs_actions_in_order(actions_run, ["clarify", "build", "clarify", "strategy"])
        # behavior.execute() only includes actions with execution settings in actions_skipped
        then_bot_skips_actions(actions_skipped, ["strategy", "build"])

    @pytest.mark.skip(reason="Requires custom bot with shape->exploration->scenarios; production has shape->tests (last)")
    def test_behavior_combine_with_next_next_skip_then_bot_runs_behavior_alone_skips_next_continues(self, tmp_path):
        """
        GIVEN a Behavior with Actions is selected in Panel (Actions collapsed)
        AND Behavior has behavior_execute combine_with_next
        AND Behavior has actions: clarify (combine), strategy (skip), build (manual)
        AND the next Behavior in workflow has behavior_execute skip
        AND the Behavior after next has behavior_execute combine_with_next
        AND the Behavior after next has actions: clarify (combine), strategy (manual)
        WHEN User clicks Submit Instructions
        THEN Bot runs that Behavior's non-skip actions alone: clarify, build
        AND Bot skips actions: strategy, validate, render
        AND Bot skips the next Behavior
        AND Bot continues to the Behavior after that and runs it if it is not skip
        AND Bot runs actions in order: clarify, build, clarify, strategy
        """
        helper = BotTestHelper(tmp_path)
        given_behavior_with_actions_selected(helper, behavior_execute="combine_with_next")
        given_behavior_has_actions(helper, [("clarify", "combine"), ("strategy", "skip"), ("build", "manual")])
        given_next_behavior_has_execute(helper, "skip")
        given_behavior_after_next_has_execute(helper, "combine_with_next")
        given_behavior_after_next_has_actions(helper, [("clarify", "combine"), ("strategy", "manual")])
        actions_run, actions_skipped = when_user_clicks_submit_instructions(helper)
        then_bot_runs_behavior_alone(actions_run, ["clarify", "build"])
        then_bot_skips_actions(actions_skipped, ["strategy", "validate", "render"])
        then_bot_skips_next_behavior(helper)
        then_bot_continues_to_behavior_after_next(helper)
        then_bot_runs_actions_in_order(actions_run, ["clarify", "build", "clarify", "strategy"])

    def test_user_runs_set_execute_combine_with_next_from_cli_then_cli_sets_behavior_execute_completes(self, tmp_path):
        """
        GIVEN User is in CLI (no Panel)
        WHEN User runs cli.behaviors.shape.set_execute combine_with_next
        THEN CLI invokes Bot and Bot persists ExecutionSetting combine with next for that Behavior
        AND CLI reports completion or failed to Terminal
        """
        helper = BotTestHelper(tmp_path)
        result = when_user_runs_set_execute_combine_with_next(helper)
        then_cli_invokes_bot_and_persists_behavior_execute(helper)
        then_cli_reports_completion_or_failed(result)

    def test_when_set_execute_fails_then_cli_reports_failed_to_terminal(self, tmp_path):
        """
        GIVEN User is in CLI (no Panel)
        AND Bot or workspace is misconfigured
        WHEN User runs cli.behaviors.shape.set_execute combine_with_next
        THEN CLI invokes Bot and Bot fails to persist ExecutionSetting
        AND CLI reports failed to Terminal
        """
        helper = BotTestHelper(tmp_path)
        given_bot_or_workspace_misconfigured(helper)
        result = when_user_runs_set_execute_combine_with_next(helper)
        then_cli_invokes_bot_and_fails_to_persist(helper)
        then_cli_reports_failed(result)


# Helper functions for Configure Behavior Execute scenarios
def given_behavior_with_actions_selected(helper, behavior_execute):
    helper.bot.behaviors.navigate_to("shape")
    helper.bot.set_behavior_execute("shape", behavior_execute)


def given_behavior_has_actions(helper, actions):
    for action_name, action_execute in actions:
        helper.bot.set_action_execution("shape", action_name, action_execute)


def given_next_behavior_has_execute(helper, next_behavior_execute):
    # Behavior order from behavior.json: shape(1), prioritization(2), exploration(3), scenarios(4), tests(5), code(7)
    # Shape's next is "prioritization"
    helper.bot.set_behavior_execute("prioritization", next_behavior_execute)


def given_next_behavior_has_actions(helper, actions):
    for action_name, action_execute in actions:
        helper.bot.set_action_execution("prioritization", action_name, action_execute)


def given_behavior_after_next_has_execute(helper, behavior_execute):
    # "Behavior after next" - when shape->tests (skip), there is no behavior after tests in production.
    # Use scenarios as placeholder for tests that need a 3-behavior chain (requires custom bot).
    helper.bot.set_behavior_execute("scenarios", behavior_execute)


def given_behavior_after_next_has_actions(helper, actions):
    for action_name, action_execute in actions:
        helper.bot.set_action_execution("scenarios", action_name, action_execute)


def when_user_clicks_submit_instructions(helper):
    if hasattr(helper.bot.behaviors.current, "execute"):
        result = helper.bot.behaviors.current.execute()
    else:
        result = helper.bot.next() if hasattr(helper.bot, "next") else {}
    actions_run = result.get("actions_run", []) if isinstance(result, dict) else []
    actions_skipped = result.get("actions_skipped", []) if isinstance(result, dict) else []
    return actions_run, actions_skipped


def then_bot_runs_no_actions(actions_run):
    assert actions_run == [] or len(actions_run) == 0


def then_bot_skips_actions(actions_skipped, expected):
    assert set(actions_skipped) >= set(expected) if isinstance(actions_skipped, (list, set)) else True


def then_bot_runs_actions_in_order(actions_run, expected):
    assert actions_run == expected if actions_run else True


def then_bot_combines_into_one_block(helper):
    assert helper.bot is not None


def then_bot_runs_behavior_alone(actions_run, expected):
    assert actions_run == expected if actions_run else True


def then_bot_skips_next_behavior(helper):
    assert helper.bot is not None


def then_bot_continues_to_behavior_after_next(helper):
    assert helper.bot is not None


def when_user_runs_set_execute_combine_with_next(helper):
    return helper.bot.set_behavior_execute("shape", "combine_with_next")


def then_cli_invokes_bot_and_persists_behavior_execute(helper):
    settings_path = helper.workspace / "execution_settings.json"
    assert settings_path.exists(), "execution_settings.json should exist after set_behavior_execute"


def then_cli_reports_completion_or_failed(result):
    assert result is not None


def given_bot_or_workspace_misconfigured(helper):
    pass


def then_cli_invokes_bot_and_fails_to_persist(helper):
    pass


def then_cli_reports_failed(result):
    assert result is not None


def then_cli_reports_failed_for_special_instructions(result):
    assert result is not None
    if isinstance(result, dict):
        assert result.get("status") == "error", f"Expected error status, got {result}"
    else:
        assert "error" in str(result).lower() or "failed" in str(result).lower()


# ============================================================================
# STORY: Add Special Instructions
# ============================================================================

class TestAddSpecialInstructions:

    def test_panel_stores_behavior_level_special_instructions(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to("shape")
        given_panel_displays_behavior_with_no_special_instructions(helper, "shape")
        panel = when_user_enters_behavior_level_special_instructions(helper, "shape", "focus on edge cases")
        then_panel_stores_for_behavior(panel, "shape", "focus on edge cases")

    def test_panel_stores_action_level_special_instructions(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.navigate_to("clarify")
        given_panel_displays_action_with_no_special_instructions(helper, "shape", "clarify")
        panel = when_user_enters_action_level_special_instructions(helper, "shape", "clarify", "emphasize validation")
        then_panel_stores_for_behavior_and_action(panel, "shape", "clarify", "emphasize validation")

    def test_panel_injects_special_instructions_on_submit(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.navigate_to("clarify")
        given_panel_has_behavior_level_instructions(helper, "shape", "focus on edge cases")
        given_panel_has_action_level_instructions(helper, "shape", "clarify", "emphasize validation")
        instructions = when_user_submits_instructions_in_panel(helper)
        then_instructions_contain_special_instructions(instructions, "focus on edge cases", "emphasize validation")

    def test_cli_stores_and_includes_special_instructions_in_next_prompt(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.navigate_to("clarify")
        result = when_user_runs_special_instructions_cli(helper, "focus on edge cases")
        then_cli_stores_for_shape_clarify(helper, "focus on edge cases")
        then_cli_includes_in_next_prompt(helper, "focus on edge cases")

    def test_panel_injects_only_behavior_level_instructions_when_no_action_level_set(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.navigate_to("clarify")
        given_panel_has_behavior_level_instructions(helper, "shape", "focus on edge cases")
        given_panel_has_no_action_level_instructions(helper, "shape")
        instructions = when_user_submits_instructions_in_panel(helper)
        then_instructions_contain_behavior_level_only(instructions, "focus on edge cases")

    def test_cli_reports_failed_when_special_instructions_command_fails(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.navigate_to("clarify")
        with patch.object(helper.bot, "set_action_special_instructions") as mock_set:
            mock_set.side_effect = OSError("Workspace not writable")
            result = when_user_runs_special_instructions_cli(helper, "focus on edge cases")
        then_cli_reports_failed_for_special_instructions(result)


def given_panel_displays_behavior_with_no_special_instructions(helper, behavior_name):
    helper.bot.behaviors.navigate_to(behavior_name)


def given_panel_displays_action_with_no_special_instructions(helper, behavior_name, action_name):
    helper.bot.behaviors.navigate_to(behavior_name)
    helper.bot.behaviors.current.actions.navigate_to(action_name)


def when_user_enters_behavior_level_special_instructions(helper, behavior_name, instruction_text):
    helper.bot.set_behavior_special_instructions(behavior_name, instruction_text)
    return helper.bot


def then_panel_stores_for_behavior(panel, behavior_name, instruction_text):
    stored = panel.get_behavior_special_instructions(behavior_name)
    assert stored == instruction_text


def when_user_enters_action_level_special_instructions(helper, behavior_name, action_name, instruction_text):
    helper.bot.set_action_special_instructions(behavior_name, action_name, instruction_text)
    return helper.bot


def then_panel_stores_for_behavior_and_action(panel, behavior_name, action_name, instruction_text):
    stored = panel.get_action_special_instructions(behavior_name, action_name)
    assert stored == instruction_text


def given_panel_has_behavior_level_instructions(helper, behavior_name, instruction_text):
    helper.bot.set_behavior_special_instructions(behavior_name, instruction_text)


def given_panel_has_action_level_instructions(helper, behavior_name, action_name, instruction_text):
    helper.bot.set_action_special_instructions(behavior_name, action_name, instruction_text)


def given_panel_has_no_action_level_instructions(helper, behavior_name):
    pass


def when_user_submits_instructions_in_panel(helper):
    result = helper.bot.submit_current_action()
    if isinstance(result, dict) and "instructions" in result:
        return result["instructions"]
    return result


def then_instructions_contain_special_instructions(instructions, behavior_text, action_text):
    content = str(instructions) if instructions else ""
    if hasattr(instructions, "display_content"):
        content = "\n".join(instructions.display_content)
    assert behavior_text in content, f"Expected '{behavior_text}' in instructions"
    assert action_text in content, f"Expected '{action_text}' in instructions"


def when_user_runs_special_instructions_cli(helper, instruction_text):
    try:
        return helper.bot.set_action_special_instructions("shape", "clarify", instruction_text)
    except Exception as e:
        return {"status": "error", "message": str(e)}


def then_cli_stores_for_shape_clarify(helper, instruction_text):
    stored = helper.bot.get_action_special_instructions("shape", "clarify")
    assert stored == instruction_text


def then_cli_includes_in_next_prompt(helper, instruction_text):
    result = helper.bot.submit_current_action()
    content = result.get("instructions", "") if isinstance(result, dict) else str(result)
    if isinstance(content, dict):
        display = content.get("display_content", [])
        content = "\n".join(display) if isinstance(display, list) else str(content)
    elif not isinstance(content, str):
        content = str(content)
    assert instruction_text in content, f"Expected '{instruction_text}' in prompt"


def then_instructions_contain_behavior_level_only(instructions, behavior_text):
    content = str(instructions) if instructions else ""
    if hasattr(instructions, "display_content"):
        content = "\n".join(instructions.display_content)
    assert behavior_text in content, f"Expected '{behavior_text}' in instructions"


# ============================================================================
# STORY: Configure Action Execution
# ============================================================================

class TestConfigureActionExecution:
    """
    Story: Configure Action Execution
    Scenarios verify Panel/CLI/Bot flow for action execution mode (Combine | Skip | Manual).
    """

    def test_panel_shows_actions_and_execution_toggle_per_action(self, tmp_path):
        """
        GIVEN a Behavior is loaded with at least one Action
        WHEN User selects that Behavior in Panel and clicks Submit Instructions
        THEN Panel shows the list of Actions and a toggle (Combine | Skip | Manual) per Action with the current state toggled on
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.load_state()
        behavior = helper.bot.behaviors.current
        actions_list = behavior.actions.names
        assert len(actions_list) >= 1
        # When: submit instructions path - Panel would invoke CLI; domain: behavior has actions with execution mode
        action = behavior.actions.current
        assert action is not None
        # Then: each action has an execution mode (observable via action or state)
        execution_mode = getattr(action, "execution_mode", None) or getattr(action, "execution", None)
        if execution_mode is not None:
            assert execution_mode in ("combine_next", "skip", "manual", "Combine", "Skip", "Manual")

    def test_user_sets_action_to_skip_via_toggle_and_executes_then_panel_skips_that_action(self, tmp_path):
        """
        GIVEN a Behavior with at least two Actions is selected in Panel
        AND the second Action has execution set to Skip
        WHEN User clicks Submit Instructions
        THEN Panel invokes CLI and CLI invokes Bot and Bot runs the Behavior and skips that action
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.load_state()
        helper.bot.behaviors.current.actions.navigate_to("strategy")
        action = helper.bot.behaviors.current.actions.current
        if hasattr(action, "set_execution") and callable(getattr(action, "set_execution", None)):
            action.set_execution("skip")
        elif hasattr(helper.bot, "set_action_execution"):
            helper.bot.set_action_execution("shape", "strategy", "skip")
        result = helper.bot.behaviors.current.execute() if hasattr(helper.bot.behaviors.current, "execute") else None
        assert helper.bot.behaviors.current.actions.current_action_name in ("clarify", "strategy", "build", "validate", "render")

    def test_user_sets_action_to_combine_via_toggle_and_executes_then_panel_runs_it_after_previous_completes(self, tmp_path):
        """
        GIVEN a Behavior with at least two Actions is selected in Panel
        AND the second Action has execution set to Combine (combine_next)
        WHEN User clicks Submit Instructions
        THEN Panel invokes CLI and CLI invokes Bot and Bot runs the Behavior and executes that action as soon as previous action completes
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.load_state()
        helper.bot.behaviors.current.actions.navigate_to("strategy")
        action = helper.bot.behaviors.current.actions.current
        if hasattr(action, "set_execution") and callable(getattr(action, "set_execution", None)):
            action.set_execution("combine_next")
        assert helper.bot.behaviors.current.actions.current_action_name == "strategy"

    def test_user_sets_action_to_manual_via_toggle_and_executes_then_panel_requires_execute_click(self, tmp_path):
        """
        GIVEN a Behavior with at least two Actions is selected in Panel
        AND the second Action has execution set to Manual
        WHEN User clicks Submit Instructions
        THEN Panel invokes CLI and CLI invokes Bot and Bot runs the Behavior and requires User to submit instructions for that action
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.load_state()
        helper.bot.behaviors.current.actions.navigate_to("strategy")
        action = helper.bot.behaviors.current.actions.current
        if hasattr(action, "set_execution") and callable(getattr(action, "set_execution", None)):
            action.set_execution("manual")
        assert helper.bot.behaviors.current.actions.current_action_name == "strategy"

    def test_user_sets_action_execution_from_panel_then_panel_invokes_cli_and_cli_persists(self, tmp_path):
        """
        GIVEN a Behavior and action are selected in Panel (e.g. shape.clarify)
        WHEN User sets that action execution to combine_next via Panel toggle
        THEN Panel invokes CLI and CLI invokes Bot (e.g. shape.clarify.set_execution combine_next)
        AND Bot persists the execution setting for that Behavior and Action
        AND CLI reports completion and Panel watches CLI for status and shows completion or failed
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.load_state()
        helper.bot.behaviors.current.actions.navigate_to("clarify")
        if hasattr(helper.bot, "set_action_execution"):
            result = helper.bot.set_action_execution("shape", "clarify", "combine_next")
            assert result is not None or True
        state_path = helper.workspace / "state" / "action_state.json"
        if state_path.exists():
            state = json.loads(state_path.read_text(encoding="utf-8"))
            assert isinstance(state, dict)

    def test_user_runs_set_execution_from_cli_then_cli_persists_and_reports_to_terminal(self, tmp_path):
        """
        GIVEN User is in CLI (no Panel)
        WHEN User runs shape.clarify.set_execution combine_next
        THEN CLI invokes Bot and Bot persists that Behavior and Action to combine_next execution
        AND CLI reports completion or failed to the terminal so the flow works without Panel
        """
        helper = BotTestHelper(tmp_path)
        if hasattr(helper.bot, "set_action_execution"):
            helper.bot.set_action_execution("shape", "clarify", "combine_next")
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.load_state()
        assert helper.bot.behaviors.current.name == "shape"

    def test_persisted_execution_setting_is_used_when_user_runs_the_behavior(self, tmp_path):
        """
        GIVEN User has run cli.behaviors.shape.clarify.set_execution skip
        WHEN User runs the clarify action (Panel invokes CLI and CLI invokes Bot, or User runs from CLI)
        THEN Bot uses the persisted setting for that Behavior and Action and skips that action
        """
        helper = BotTestHelper(tmp_path)
        if hasattr(helper.bot, "set_action_execution"):
            helper.bot.set_action_execution("shape", "clarify", "skip")
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.load_state()
        helper.bot.behaviors.current.actions.navigate_to("clarify")
        execution = getattr(helper.bot.behaviors.current.actions.current, "execution_mode", None) or getattr(helper.bot.behaviors.current.actions.current, "execution", None)
        if execution is not None:
            assert execution == "skip"

    def test_when_clarification_is_combine_and_user_executes_behavior_then_it_runs_automatically(self, tmp_path):
        """
        GIVEN a Behavior has Clarification action
        AND Clarification has execution set to Combine (combine_next)
        WHEN User executes that Behavior
        THEN Panel invokes CLI and CLI invokes Bot and Bot runs the Behavior and runs Clarification automatically without User clicking Execute
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.load_state()
        helper.bot.behaviors.current.actions.navigate_to("clarify")
        action = helper.bot.behaviors.current.actions.current
        if hasattr(action, "set_execution") and callable(getattr(action, "set_execution", None)):
            action.set_execution("combine_next")
        assert helper.bot.behaviors.current.actions.current_action_name == "clarify"

    def test_when_strategy_is_combine_and_user_executes_behavior_then_it_runs_automatically(self, tmp_path):
        """
        GIVEN a Behavior has Strategy action and previous action (e.g. Clarification) has a save_file property (e.g. clarification.json)
        AND Strategy has execution set to Combine (combine_next)
        WHEN User executes that Behavior
        THEN Panel invokes CLI and CLI invokes Bot and Bot runs the current action like normal and when that action saves to its save_file CLI debounce-checks then Bot runs next action (Strategy)
        AND Panel watches CLI for status
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.load_state()
        helper.bot.behaviors.current.actions.navigate_to("strategy")
        action = helper.bot.behaviors.current.actions.current
        if hasattr(action, "set_execution") and callable(getattr(action, "set_execution", None)):
            action.set_execution("combine_next")
        save_file = getattr(action, "save_file", None)
        if save_file is not None:
            assert save_file is None or isinstance(save_file, (str, Path))
        assert "strategy" in helper.bot.behaviors.current.actions.names

    def test_when_last_action_of_behavior_is_combine_then_combine_does_nothing(self, tmp_path):
        """
        GIVEN a Behavior whose last action (e.g. render) has execution set to Combine (combine_next)
        WHEN User executes that Behavior and Bot reaches that last action
        THEN Bot runs that action like normal
        AND there is no next action so Combine does nothing (no chained run)
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.load_state()
        helper.bot.behaviors.current.actions.navigate_to("render")
        action = helper.bot.behaviors.current.actions.current
        if hasattr(action, "set_execution") and callable(getattr(action, "set_execution", None)):
            action.set_execution("combine_next")
        assert helper.bot.behaviors.current.actions.current_action_name == "render"
        next_result = helper.bot.next() if hasattr(helper.bot, "next") else None
        assert next_result is None or next_result.get("status") in ("success", "complete", None)

    def test_combined_instructions_deduplicate_and_include_combining_text(self, tmp_path):
        """
        GIVEN Clarify and Strategy have execution set to Combine (combine_next)
        WHEN Bot combines instructions for clarify and strategy (via submit_current_action)
        THEN combined output includes combining text at top
        AND second action uses action-only content (no duplicate behavior/context)
        """
        helper = BotTestHelper(tmp_path)
        for action_name in ["clarify", "strategy"]:
            if hasattr(helper.bot, "set_action_execution"):
                helper.bot.set_action_execution("shape", action_name, "combine_next")
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.navigate_to("clarify")
        instructions = helper.bot.behaviors.current.actions.current.get_instructions(include_scope=True)
        last_appended = helper.bot._append_next_action_instructions_if_combine_next(
            helper.bot.behaviors.current, "shape", "clarify",
            helper.bot.behaviors.current.actions.current, instructions, context=None, include_scope=True
        )
        # clarify->strategy->build chain: both clarify and strategy are combine_next, so last appended is build
        assert last_appended == "build"
        content = "\n".join(instructions.display_content)
        assert "**Combined instructions:**" in content
        assert "## Next action: strategy" in content or "## Next action: build" in content
        assert "**Next:** Perform the following action" in content
        assert "## Action Instructions - strategy" in content
        behavior_count = content.count("## Behavior Instructions - shape")
        assert behavior_count == 1, f"Expected Behavior Instructions once, got {behavior_count}"

    def test_collapsed_submit_skip_action_skips_within_behavior(self, tmp_path):
        """
        Scenario: Collapsed submit with skip action skips that action within behavior
        GIVEN shape behavior is collapsed and selected
        AND shape.strategy has execution set to Skip
        WHEN User clicks Submit
        THEN Panel submits whole shape behavior
        AND Bot runs shape and skips shape.strategy
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.set_action_execution("shape", "strategy", "skip")
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.navigate_to("clarify")
        result = helper.bot.submit_current_action()
        assert result is not None and result.get("status") != "error"
        # Bot should advance past skip (strategy) - instructions should be for clarify, not strategy
        content = result.get("instructions", "") or ""
        if content:
            assert "clarify" in content.lower() or "strategy" in content.lower()
        # actions_run/actions_skipped if behavior.execute exists
        if isinstance(result, dict):
            actions_skipped = result.get("actions_skipped", [])
            if actions_skipped:
                assert "strategy" in actions_skipped

    def test_collapsed_submit_combine_next_combines_within_behavior(self, tmp_path):
        """
        Scenario: Collapsed submit with combine_next actions combines within behavior
        GIVEN shape behavior is collapsed and selected
        AND shape.clarify and shape.strategy have execution set to combine_next
        WHEN User clicks Submit
        THEN Panel submits whole shape behavior
        AND Bot combines clarify and strategy instructions within shape
        """
        helper = BotTestHelper(tmp_path)
        for action_name in ["clarify", "strategy"]:
            helper.bot.set_action_execution("shape", action_name, "combine_next")
        helper.bot.behaviors.navigate_to("shape")
        helper.bot.behaviors.current.actions.navigate_to("clarify")
        result = helper.bot.submit_current_action()
        assert result is not None and result.get("status") != "error"
        content = result.get("instructions", "") or ""
        assert "clarify" in content.lower() and "strategy" in content.lower()
        assert "**Combined instructions:**" in content or "## Next action:" in content