# 📄 Open Source File

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/edit_story_map)

**User:** Developer
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Trace Story Graph](..) / [⚙️ Trace Code](.)  
**Sequential Order:** 3
**Story Type:** user

## Story Description

Open Source File functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-"></a>
### Scenario: [](#scenario-) (happy_path)

**Steps:**
```gherkin
Given code node "{code_node}" has source file "{source_file}" at line {line_number}
When Developer clicks Open on the code node
Then the editor opens the file and navigates to line {line_number}
```

**Examples:**

| Code Node | Source File | Line Number | Expected Result |
| --- | --- | --- | --- |
| approve_transfer | src/transfers/transfer_service.py | 42 | file opens at line 42 |


<a id="scenario-"></a>
### Scenario: [](#scenario-) (edge_case)

**Steps:**
```gherkin
Given test node "{test_node}" is already open in the editor
And the test node points to line {line_number} in "{test_file}"
When Developer clicks Open on the test node
Then the editor focuses the existing tab, opens the file at the end, and shows a line not found warning
```

**Examples:**

| Test Node | Test File | Line Number | Expected Result |
| --- | --- | --- | --- |
| test_approve_transfer | test/transfers/test_trace_story.py | 900 | focus existing tab, open at end, show warning |


<a id="scenario-"></a>
### Scenario: [](#scenario-) (error_case)

**Steps:**
```gherkin
Given code node "{code_node}" has source file "{source_file}" with file state "{file_state}"
When Developer clicks Open on the code node
Then the trace editor shows error "{error_message}"
```

**Examples:**

| Code Node | Source File | File State | Error Message |
| --- | --- | --- | --- |
| missing_transfer_file | src/transfers/missing.py | missing | File not found |

