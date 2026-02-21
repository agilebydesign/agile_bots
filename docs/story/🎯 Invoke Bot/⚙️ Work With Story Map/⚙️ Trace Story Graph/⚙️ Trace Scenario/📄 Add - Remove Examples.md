# 📄 Add / Remove Examples

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/edit_story_map)

**User:** Developer
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Trace Story Graph](..) / [⚙️ Trace Scenario](.)  
**Sequential Order:** 4.0
**Story Type:** user

## Story Description

Add / Remove Examples functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-add-examples-creates-new-table"></a>
### Scenario: [Add examples creates new table](#scenario-add-examples-creates-new-table) (happy_path)

**Steps:**
```gherkin
Given Scenario "{scenario_name}" has examples state "{examples_state}"
When Developer clicks Add Examples
Then "{expected_result}"
```

**Examples:**

| Scenario Name | Examples State | Expected Result |
| --- | --- | --- |
| Approve Transfer | none | new examples table with focus on first cell |


<a id="scenario-remove-examples-table-updates-story-data"></a>
### Scenario: [Remove examples table updates story data](#scenario-remove-examples-table-updates-story-data) (edge_case)

**Steps:**
```gherkin
Given Scenario "{scenario_name}" has {table_count} examples tables
When Developer removes one examples table
Then "{expected_result}"
```

**Examples:**

| Scenario Name | Table Count | Expected Result |
| --- | --- | --- |
| Approve Transfer | 2 | one table removed and changes saved |


<a id="scenario-removing-last-examples-table-shows-empty-section"></a>
### Scenario: [Removing last examples table shows empty section](#scenario-removing-last-examples-table-shows-empty-section) (edge_case)

**Steps:**
```gherkin
Given Scenario "{scenario_name}" has {table_count} examples table
When Developer removes the last examples table
Then "{expected_result}"
```

**Examples:**

| Scenario Name | Table Count | Expected Result |
| --- | --- | --- |
| Approve Transfer | 1 | empty examples section with container |


<a id="scenario-save-failure-during-add-examples-shows-error"></a>
### Scenario: [Save failure during add examples shows error](#scenario-save-failure-during-add-examples-shows-error) (error_case)

**Steps:**
```gherkin
Given story-graph.json has state "{story_graph_state}" and Scenario "{scenario_name}" is displayed
When Developer clicks Add Examples
Then the trace editor shows error "{error_message}" and no examples table is created
```

**Examples:**

| Story Graph State | Scenario Name | Error Message |
| --- | --- | --- |
| read_only | Approve Transfer | Unable to save story-graph.json |

