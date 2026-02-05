# 📄 Open Scenario Source

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** Developer
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Trace Story Graph](..) / [⚙️ Trace Scenario](.)  
**Sequential Order:** 4.0
**Story Type:** user

## Story Description

Open Scenario Source functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** Developer clicks Open on scenario
  **then** story-graph.json opens at scenario line

## Scenarios

<a id="scenario-open-scenario-source-from-trace-editor"></a>
### Scenario: [Open scenario source from trace editor](#scenario-open-scenario-source-from-trace-editor) (happy_path)

**Steps:**
```gherkin
Given the trace editor shows a scenario
When the Developer clicks Open on the scenario
Then story-graph.json opens at the scenario line
```


<a id="scenario-scenario-names-with-punctuation-still-open-correctly"></a>
### Scenario: [Scenario names with punctuation still open correctly](#scenario-scenario-names-with-punctuation-still-open-correctly) (edge_case)

**Steps:**
```gherkin
Given a scenario name includes spaces and punctuation
When the Developer clicks Open on the scenario
Then story-graph.json opens at the scenario line
```


<a id="scenario-missing-story-graph-shows-error-on-scenario-open"></a>
### Scenario: [Missing story graph shows error on scenario open](#scenario-missing-story-graph-shows-error-on-scenario-open) (error_case)

**Steps:**
```gherkin
Given story-graph.json is missing
When the Developer clicks Open on the scenario
Then the trace editor shows an error and no file is opened
```

