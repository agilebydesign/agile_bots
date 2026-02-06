# 📄 Edit Code Step

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** Developer
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Trace Story Graph](..) / [⚙️ Trace Code](.)  
**Sequential Order:** 2.0
**Story Type:** user

## Story Description

Edit Code Step functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-edit-implementation-code-saves-to-source-file"></a>
### Scenario: [Edit implementation code saves to source file](#scenario-edit-implementation-code-saves-to-source-file) (happy_path)

**Steps:**
```gherkin
Given code node "{code_node}" is displayed with source file "{source_file}"
When Developer edits the code and triggers save via {save_trigger}
Then the source file is updated and a save confirmation indicator is shown
```

**Examples:**

| Code Node | Source File | Save Trigger | Expected Result |
| --- | --- | --- | --- |
| build_transfer_view | src/transfers/transfer_view.py | blur | source file saved |


<a id="scenario-edit-test-code-saves-to-test-file"></a>
### Scenario: [Edit test code saves to test file](#scenario-edit-test-code-saves-to-test-file) (edge_case)

**Steps:**
```gherkin
Given test node "{test_node}" is displayed with test file "{test_file}"
When Developer edits the test code and triggers save via {save_trigger}
Then the test file is updated
```

**Examples:**

| Test Node | Test File | Save Trigger | Expected Result |
| --- | --- | --- | --- |
| test_transfer_approval | test/transfers/test_transfer_approval.py | Ctrl+S | test file saved |


<a id="scenario-save-failure-preserves-edits"></a>
### Scenario: [Save failure preserves edits](#scenario-save-failure-preserves-edits) (error_case)

**Steps:**
```gherkin
Given code node "{code_node}" is displayed and the source file has state "{file_state}"
When Developer edits the code and triggers save
Then a save error indicator is shown with message "{error_message}" and the edits remain in the editor
```

**Examples:**

| Code Node | File State | Error Message |
| --- | --- | --- |
| build_transfer_view | read_only | Unable to save source file |

