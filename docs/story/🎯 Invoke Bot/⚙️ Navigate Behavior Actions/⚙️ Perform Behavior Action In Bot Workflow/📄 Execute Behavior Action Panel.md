# 📄 Execute Behavior Action Panel

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/navigate_behavior_actions/test_perform_behavior_action_in_bot_workflow.py#L333)

**User:** User
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Navigate Behavior Actions](..) / [⚙️ Perform Behavior Action In Bot Workflow](.)  
**Sequential Order:** 1.0
**Story Type:** user

## Story Description

Execute Behavior Action Panel functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User clicks collapsed behavior (not skip)
  **then** System selects that behavior (empty circle → checkmark)
  **and** System does not navigate to an action
  **and** System does not execute

- **When** Behavior has execute set to skip
  **then** System displays that behavior's circle as grayed out and unchecked (no checkmark)
  **and** System treats that behavior as non-interactive (click does nothing)

- **When** User clicks Submit and behavior is collapsed
  **then** System submits the whole behavior (all actions) using manual / combine_with_next / skip logic

- **When** User clicks Submit and behavior is expanded
  **then** System submits the selected action or the first executable action

- **When** User clicks action (behavior expanded)
  **then** System displays that action as current
  **and** System expands action to display operations
  **and** System sets first operation as current
  **and** System executes first operation of that action

## Scenarios

<a id="scenario-skip-behavior-shows-grayed-unchecked-circle-and-is-non-interactive"></a>
### Scenario: [Skip behavior shows grayed unchecked circle and is non-interactive](#scenario-skip-behavior-shows-grayed-unchecked-circle-and-is-non-interactive) (happy_path)

**Steps:**
```gherkin
Given Panel displays behavior hierarchy
And prioritization behavior has execute set to skip
When Panel renders the behavior list
Then Panel shows prioritization's circle as grayed out
And Panel shows prioritization's circle as unchecked (no checkmark)
And User click on prioritization does nothing
```


<a id="scenario-collapsed-behavior-click-selects-only"></a>
### Scenario: [Collapsed behavior click selects only](#scenario-collapsed-behavior-click-selects-only) (happy_path)

**Steps:**
```gherkin
Given Panel displays behavior hierarchy
And discovery behavior is collapsed and not skip
When User clicks discovery behavior
Then Panel selects discovery behavior (empty circle → checkmark)
And Panel does not navigate to an action
And Bot does not execute
```


<a id="scenario-collapsed-submit-submits-whole-behavior"></a>
### Scenario: [Collapsed Submit submits whole behavior](#scenario-collapsed-submit-submits-whole-behavior) (happy_path)

**Steps:**
```gherkin
Given Panel displays behavior hierarchy
And shape behavior is collapsed and selected
When User clicks Submit
Then Panel submits the whole shape behavior (all actions)
And Bot runs shape using manual / combine_with_next / skip logic
```


<a id="scenario-expanded-action-click-navigates-and-executes"></a>
### Scenario: [Expanded action click navigates and executes](#scenario-expanded-action-click-navigates-and-executes) (happy_path)

**Steps:**
```gherkin
Given Panel displays expanded shape behavior
And Bot is at shape.clarify
When User clicks shape.strategy action
Then Bot navigates to shape.strategy
And Panel displays shape.strategy as current action
And Panel expands shape.strategy showing operations
And Bot executes shape.strategy.instructions operation
```


<a id="scenario-operation-click-executes-and-updates-current"></a>
### Scenario: [Operation click executes and updates current](#scenario-operation-click-executes-and-updates-current) (happy_path)

**Steps:**
```gherkin
Given Panel displays expanded shape.clarify action
And Operations are visible (instructions, execute, confirm)
When User clicks clarify.confirm operation
Then Bot executes clarify.confirm operation
And Panel displays confirm operation as current
```

