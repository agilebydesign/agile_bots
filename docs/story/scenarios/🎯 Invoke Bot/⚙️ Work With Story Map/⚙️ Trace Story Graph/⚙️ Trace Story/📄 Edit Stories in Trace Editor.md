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

<a id="scenario-story-name-edit-saves-on-blur"></a>
### Scenario: [Story name edit saves on blur](#scenario-story-name-edit-saves-on-blur) (happy_path)

**Steps:**
```gherkin
Given Story "{original_name}" is displayed in trace editor
When Developer changes story name to "{updated_name}" and triggers save via {save_trigger}
Then story-graph.json contains Story with name "{updated_name}"
And Trace Editor shows save confirmation indicator
```

**Examples:**

| Original Name | Updated Name | Save Trigger |
| --- | --- | --- |
| Approve Wealth Transfer | Approve Wire Transfer | blur |
| Reject Wealth Transfer | Reject Suspicious Transfer | Ctrl+S |


<a id="scenario-unchanged-story-field-skips-save"></a>
### Scenario: [Unchanged story field skips save](#scenario-unchanged-story-field-skips-save) (edge_case)

**Steps:**
```gherkin
Given Story "{story_name}" is displayed in trace editor
And field "{field_name}" has value "{current_value}"
When Developer focuses field "{field_name}" and leaves without changes
Then story-graph.json modification timestamp is unchanged
And Trace Editor shows no save indicator
```

**Examples:**

| Story Name | Field Name | Current Value |
| --- | --- | --- |
| Approve Wealth Transfer | name | Approve Wealth Transfer |
| Approve Wealth Transfer | users | Developer, Compliance Officer |


<a id="scenario-read-only-file-shows-save-error-and-preserves-edits"></a>
### Scenario: [Read-only file shows save error and preserves edits](#scenario-read-only-file-shows-save-error-and-preserves-edits) (error_case)

**Steps:**
```gherkin
Given story-graph.json has file state "{file_state}"
And Story "{story_name}" is displayed in trace editor
When Developer changes story name to "{updated_name}" and triggers save via {save_trigger}
Then Trace Editor shows error message "{error_message}"
And story-graph.json still contains Story with name "{story_name}"
And Trace Editor preserves "{updated_name}" in the editor field
```

**Examples:**| File State | Story Name | Updated Name | Save Trigger | Error Message |
| --- | --- | --- | --- | --- |
| read-only | Approve Wealth Transfer | Approve Wire Transfer | Ctrl+S | Cannot save: story-graph.json is read-only |
| locked by another process | Reject Wealth Transfer | Reject Transfer | blur | Cannot save: file is locked |