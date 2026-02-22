# 📄 Configure Behavior Execute

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/navigate_behavior_actions/test_perform_behavior_action_in_bot_workflow.py)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Navigate Behavior Actions](..) / [⚙️ Perform Behavior Action In Bot Workflow](.)  
**Sequential Order:** 12.5
**Story Type:** user

## Story Description

Configure Behavior Execute functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User sets behavior execute to skip in Panel behavior dropdown AND User executes that behavior
  **then** Panel skips all actions in that behavior regardless of per-action setting

- **When** User sets behavior execute to auto in Panel AND User executes that behavior
  **then** Panel runs auto and manual actions
  **and** Panel skips actions marked skip

- **When** User sets behavior execute to manual in Panel AND User executes that behavior
  **then** Panel performs each action according to that action's skip/auto/manual setting

- **When** User runs cli.behaviors.shape.set_execute auto
  **then** CLI sets behavior execute to auto for that behavior

## Scenarios

<a id="scenario-skip-behavior-is-dimmed-and-non-interactive"></a>
### Scenario: [Skip behavior is dimmed and non-interactive](#scenario-skip-behavior-is-dimmed-and-non-interactive) (happy_path)

**Steps:**
```gherkin
Given prioritization behavior has execute set to skip
When Panel displays behavior hierarchy
Then Panel shows prioritization as dimmed and non-interactive
And User click on prioritization does nothing
```


<a id="scenario-manual-behavior-submit-runs-each-action-per-its-setting"></a>
### Scenario: [Manual behavior submit runs each action per its setting](#scenario-manual-behavior-submit-runs-each-action-per-its-setting) (happy_path)

**Steps:**
```gherkin
Given shape behavior has execute set to manual
And shape has actions clarify (manual), strategy (auto)
When User selects collapsed shape and clicks Submit
Then Panel submits whole shape behavior
And Bot runs clarify (waits for submit) then strategy (auto after clarify completes)
```


<a id="scenario-combine-with-next-behavior-submit-aggregates-actions"></a>
### Scenario: [Combine with next behavior submit aggregates actions](#scenario-combine-with-next-behavior-submit-aggregates-actions) (happy_path)

**Steps:**
```gherkin
Given shape has execute combine_with_next, scenarios has execute manual
And shape and scenarios are consecutive non-skip behaviors
When User selects collapsed shape and clicks Submit
Then Panel submits whole shape behavior
And Bot combines shape's non-skip actions with scenarios' non-skip actions (or runs shape alone if scenarios is skip)
```

