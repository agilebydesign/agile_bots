# 📄 Edit Scenarios in Trace Editor

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** Developer
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Trace Story Graph](..) / [⚙️ Trace Scenario](.)  
**Sequential Order:** 3.0
**Story Type:** user

## Story Description

Edit Scenarios in Trace Editor functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** Developer modifies scenario steps
  **then** changes save to story-graph.json (on blur/Ctrl+S)

## Scenarios

<a id="scenario-scenario-step-edits-save-on-blur"></a>
### Scenario: [Scenario step edits save on blur](#scenario-scenario-step-edits-save-on-blur) (happy_path)

**Steps:**
```gherkin
Given a scenario is displayed in the trace editor
When the Developer edits scenario steps and leaves the field
Then story-graph.json is updated with the new steps
```


<a id="scenario-scenario-step-edits-save-on-ctrls"></a>
### Scenario: [Scenario step edits save on Ctrl+S](#scenario-scenario-step-edits-save-on-ctrls) (edge_case)

**Steps:**
```gherkin
Given a scenario is displayed in the trace editor
When the Developer edits scenario steps and presses Ctrl+S
Then story-graph.json is updated with the new steps
```


<a id="scenario-read-only-story-graph-shows-save-error-for-scenario-steps"></a>
### Scenario: [Read-only story graph shows save error for scenario steps](#scenario-read-only-story-graph-shows-save-error-for-scenario-steps) (error_case)

**Steps:**
```gherkin
Given story-graph.json is read-only
When the Developer edits scenario steps and presses Ctrl+S
Then the trace editor shows a save error and the file remains unchanged
```

