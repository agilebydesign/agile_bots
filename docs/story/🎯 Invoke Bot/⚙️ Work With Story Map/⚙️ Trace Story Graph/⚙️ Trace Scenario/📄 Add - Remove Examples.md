# 📄 Add / Remove Examples

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/edit_story_map)

**User:** Developer
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Trace Story Graph](..) / [⚙️ Trace Scenario](.)  
**Sequential Order:** 5.0
**Story Type:** user

## Story Description

Add / Remove Examples functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-"></a>
### Scenario: [](#scenario-) (happy_path)

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


<a id="scenario-"></a>
### Scenario: [](#scenario-) (edge_case)

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


<a id="scenario-"></a>
### Scenario: [](#scenario-) (edge_case)

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


<a id="scenario-"></a>
### Scenario: [](#scenario-) (error_case)

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

