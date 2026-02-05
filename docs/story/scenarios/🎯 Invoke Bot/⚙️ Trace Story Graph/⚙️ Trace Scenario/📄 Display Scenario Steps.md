# 📄 Display Scenario Steps

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** Developer
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Trace Story Graph](..) / [⚙️ Trace Scenario](.)  
**Sequential Order:** 1.0
**Story Type:** user

## Story Description

Display Scenario Steps functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** Developer views scenario
  **then** scenario steps display in given/when/then format

## Scenarios

<a id="scenario-scenario-steps-display-in-given-when-then-format"></a>
### Scenario: [Scenario steps display in given when then format](#scenario-scenario-steps-display-in-given-when-then-format) (happy_path)

**Steps:**
```gherkin
Given a story has a scenario with steps in story-graph.json
When the Developer selects the scenario in the trace editor
Then the steps display in given when then format
```


<a id="scenario-scenario-with-no-steps-shows-empty-state"></a>
### Scenario: [Scenario with no steps shows empty state](#scenario-scenario-with-no-steps-shows-empty-state) (edge_case)

**Steps:**
```gherkin
Given a story has a scenario with no steps in story-graph.json
When the Developer selects the scenario in the trace editor
Then the trace editor shows an empty steps state
```


<a id="scenario-unreadable-story-graph-shows-error"></a>
### Scenario: [Unreadable story graph shows error](#scenario-unreadable-story-graph-shows-error) (error_case)

**Steps:**
```gherkin
Given story-graph.json cannot be parsed
When the Developer selects the scenario in the trace editor
Then the trace editor shows an error and no steps are displayed
```

