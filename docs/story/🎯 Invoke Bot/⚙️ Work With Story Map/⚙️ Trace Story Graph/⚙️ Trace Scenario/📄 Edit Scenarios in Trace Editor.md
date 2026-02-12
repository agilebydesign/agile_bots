# 📄 Edit Scenarios in Trace Editor

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/edit_story_map)

**User:** Developer
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Trace Story Graph](..) / [⚙️ Trace Scenario](.)  
**Sequential Order:** 2
**Story Type:** user

## Story Description

Edit Scenarios in Trace Editor functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-"></a>
### Scenario: [](#scenario-) (happy_path)

**Steps:**
```gherkin
Given Scenario "{scenario_name}" is displayed with steps "{original_steps}"
When Developer edits the steps to "{updated_steps}" and triggers save via {save_trigger}
Then story-graph.json is updated with the new steps
```

**Examples:**

| Scenario Name | Original Steps | Updated Steps | Save Trigger |
| --- | --- | --- | --- |
| Approve Transfer | Given account is verified; When transfer is submitted; Then approval is recorded | Given account is verified and funded; When transfer is submitted; Then approval is recorded | blur |


<a id="scenario-"></a>
### Scenario: [](#scenario-) (edge_case)

**Steps:**
```gherkin
Given Scenario "{scenario_name}" is displayed with steps "{original_steps}"
When Developer edits the steps to "{updated_steps}" and triggers save via {save_trigger}
Then story-graph.json is updated with the new steps
```

**Examples:**

| Scenario Name | Original Steps | Updated Steps | Save Trigger |
| --- | --- | --- | --- |
| Approve Transfer | Given account is verified; When transfer is submitted; Then approval is recorded | Given account is verified; When transfer is submitted; Then approval is recorded and logged | Ctrl+S |


<a id="scenario-"></a>
### Scenario: [](#scenario-) (error_case)

**Steps:**
```gherkin
Given story-graph.json has state "{story_graph_state}" and Scenario "{scenario_name}" is displayed
When Developer edits the steps and triggers save via {save_trigger}
Then the trace editor shows error "{error_message}" and the file remains unchanged
```

**Examples:**

| Scenario Name | Story Graph State | Save Trigger | Error Message |
| --- | --- | --- | --- |
| Approve Transfer | read_only | Ctrl+S | Unable to save story-graph.json |

