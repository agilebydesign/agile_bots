# 📄 Open Scenario Source

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** Developer
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Trace Story Graph](..) / [⚙️ Trace Scenario](.)  
**Sequential Order:** 3.0
**Story Type:** user

## Story Description

Open Scenario Source functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-open-scenario-source-from-trace-editor"></a>
### Scenario: [Open scenario source from trace editor](#scenario-open-scenario-source-from-trace-editor) (happy_path)

**Steps:**
```gherkin
Given the trace editor shows Scenario "{scenario_name}"
When Developer clicks Open on the scenario
Then "{story_graph_file}" opens at "{expected_location}"
```

**Examples:**

| Scenario Name | Story Graph File | Expected Location |
| --- | --- | --- |
| Approve Transfer | story-graph.json | scenario line 10503 |


<a id="scenario-scenario-names-with-punctuation-still-open-correctly"></a>
### Scenario: [Scenario names with punctuation still open correctly](#scenario-scenario-names-with-punctuation-still-open-correctly) (edge_case)

**Steps:**
```gherkin
Given the trace editor shows Scenario "{scenario_name}"
When Developer clicks Open on the scenario
Then "{story_graph_file}" opens at "{expected_location}"
```

**Examples:**

| Scenario Name | Story Graph File | Expected Location |
| --- | --- | --- |
| Approve Transfer: Level-2? | story-graph.json | scenario line with special characters |


<a id="scenario-missing-story-graph-shows-error-on-scenario-open"></a>
### Scenario: [Missing story graph shows error on scenario open](#scenario-missing-story-graph-shows-error-on-scenario-open) (error_case)

**Steps:**
```gherkin
Given story-graph.json has state "{story_graph_state}" and the trace editor shows Scenario "{scenario_name}"
When Developer clicks Open on the scenario
Then the trace editor shows error "{error_message}"
```

**Examples:**

| Scenario Name | Story Graph State | Error Message |
| --- | --- | --- |
| Approve Transfer | missing | story-graph.json not found |

