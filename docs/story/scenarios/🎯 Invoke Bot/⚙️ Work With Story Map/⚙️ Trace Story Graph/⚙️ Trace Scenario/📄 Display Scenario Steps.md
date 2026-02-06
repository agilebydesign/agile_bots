# 📄 Display Scenario Steps

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** Developer
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Trace Story Graph](..) / [⚙️ Trace Scenario](.)  
**Sequential Order:** 1.0
**Story Type:** user

## Story Description

Display Scenario Steps functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-scenario-steps-display-in-given-when-then-format"></a>
### Scenario: [Scenario steps display in given when then format](#scenario-scenario-steps-display-in-given-when-then-format) (happy_path)

**Steps:**
```gherkin
Given Story "{story_name}" is loaded with Scenario "{scenario_name}" and steps "{scenario_steps}"
When Developer selects Scenario "{scenario_name}" in the trace editor
Then the steps display in "{expected_format}" format
```

**Examples:**

| Story Name | Scenario Name | Scenario Steps | Expected Format |
| --- | --- | --- | --- |
| Wealth Transfer Overview | Approve Transfer | Given account is verified; When transfer is submitted; Then approval is recorded | given/when/then |


<a id="scenario-scenario-with-no-steps-shows-empty-state"></a>
### Scenario: [Scenario with no steps shows empty state](#scenario-scenario-with-no-steps-shows-empty-state) (edge_case)

**Steps:**
```gherkin
Given Story "{story_name}" is loaded with Scenario "{scenario_name}" and steps "{scenario_steps}"
When Developer selects Scenario "{scenario_name}" in the trace editor
Then the trace editor shows "{empty_state_message}"
```

**Examples:**

| Story Name | Scenario Name | Scenario Steps | Empty State Message |
| --- | --- | --- | --- |
| Wealth Transfer Overview | Pending Review | none | No steps available |


<a id="scenario-unreadable-story-graph-shows-error"></a>
### Scenario: [Unreadable story graph shows error](#scenario-unreadable-story-graph-shows-error) (error_case)

**Steps:**
```gherkin
Given story-graph.json has state "{story_graph_state}"
When Developer selects Scenario "{scenario_name}" in the trace editor
Then the trace editor shows error "{error_message}"
```

**Examples:**

| Story Graph State | Scenario Name | Error Message |
| --- | --- | --- |
| invalid_json | Approve Transfer | Unable to load story-graph.json |

