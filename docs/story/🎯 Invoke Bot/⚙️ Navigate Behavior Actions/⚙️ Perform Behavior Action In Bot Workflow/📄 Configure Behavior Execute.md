# 📄 Configure Behavior Execute

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/navigate_behavior_actions/test_perform_behavior_action_in_bot_workflow.py)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Navigate Behavior Actions](..) / [⚙️ Perform Behavior Action In Bot Workflow](.)  
**Sequential Order:** 12.5
**Story Type:** user

## Story Description

Configure Behavior Execute functionality for the mob minion system. **Behavior-level** configuration (skip, combine with next, manual per behavior), not action-level.

**Flow example:** shape (combine with next), prioritization (skip), exploration (skip), scenarios (manual) → run shape's non-skip actions together, skip prioritization, skip exploration, run scenarios (each action per its setting). Behavior skip is the same as action skip: skip entire behavior.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User sets behavior execute to skip in Panel behavior dropdown AND User executes that behavior
  **then** Panel skips all actions in that behavior regardless of per-action setting

- **When** User sets behavior execute to combine with next in Panel AND User selects behavior (actions collapsed inside) AND User clicks Submit Instructions
  **then** Panel combines that behavior's non-skip actions with the next non-skip behavior's non-skip actions into one aggregated instruction block (or runs that behavior's actions alone if next is skip, then continues to the next behavior after that and runs it if able)
  **and** Panel skips actions marked skip

- **When** User sets behavior execute to manual in Panel AND User executes that behavior
  **then** Panel performs each action according to that action's auto/manual setting

- **When** User runs cli.behaviors.shape.set_execute combine_with_next
  **then** CLI sets behavior execute to combine with next for that behavior

## Scenarios

### Scenario: Configure Behavior Execute (happy_path)

**Steps:**
```gherkin
Given system is ready
When action executes
Then action completes successfully
```
