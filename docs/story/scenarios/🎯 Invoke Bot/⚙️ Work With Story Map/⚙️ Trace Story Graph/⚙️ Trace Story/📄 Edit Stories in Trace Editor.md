# 📄 Edit Stories in Trace Editor

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** Developer
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Trace Story Graph](..) / [⚙️ Trace Story](.)  
**Sequential Order:** 2.0
**Story Type:** user

## Story Description

Edit Stories in Trace Editor functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-story-field-edits-save-on-blur"></a>
### Scenario: [Story field edits save on blur](#scenario-story-field-edits-save-on-blur) (happy_path)

**Steps:**
```gherkin
Given the trace editor shows a story from the strace file
When the Developer edits the story name and leaves the field
Then story-graph.json is updated with the new story name
```


<a id="scenario-unchanged-story-field-does-not-create-a-save"></a>
### Scenario: [Unchanged story field does not create a save](#scenario-unchanged-story-field-does-not-create-a-save) (edge_case)

**Steps:**
```gherkin
Given the trace editor shows a story
When the Developer focuses a story field and leaves it unchanged
Then story-graph.json is not modified
```


<a id="scenario-read-only-story-graph-shows-save-error"></a>
### Scenario: [Read-only story graph shows save error](#scenario-read-only-story-graph-shows-save-error) (error_case)

**Steps:**
```gherkin
Given story-graph.json is read-only
When the Developer edits a story field and presses Ctrl+S
Then the trace editor shows a save error and the file remains unchanged
```

