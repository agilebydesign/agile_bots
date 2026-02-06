# 📄 Display Examples Table

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** Developer
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Trace Story Graph](..) / [⚙️ Trace Scenario](.)  
**Sequential Order:** 4.0
**Story Type:** user

## Story Description

Display Examples Table functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-examples-table-displays-with-headers-and-rows"></a>
### Scenario: [Examples table displays with headers and rows](#scenario-examples-table-displays-with-headers-and-rows) (happy_path)

**Steps:**
```gherkin
Given Scenario "{scenario_name}" includes an examples table with columns "{example_columns}" and row "{example_row}"
When Developer views the scenario in the trace editor
Then the examples table displays with "{expected_display}"
```

**Examples:**

| Scenario Name | Example Columns | Example Row | Expected Display |
| --- | --- | --- | --- |
| Approve Transfer | Transfer Type, Amount, Expected Outcome | Wire, 25000, Approved | table with headers and row values |


<a id="scenario-scenario-without-examples-shows-empty-section"></a>
### Scenario: [Scenario without examples shows empty section](#scenario-scenario-without-examples-shows-empty-section) (edge_case)

**Steps:**
```gherkin
Given Scenario "{scenario_name}" has examples state "{examples_state}"
When Developer views the scenario in the trace editor
Then the trace editor shows "{empty_section_ui}"
```

**Examples:**

| Scenario Name | Examples State | Empty Section UI |
| --- | --- | --- |
| Pending Review | none | Add Example button visible |


<a id="scenario-examples-table-with-many-rows-is-scrollable"></a>
### Scenario: [Examples table with many rows is scrollable](#scenario-examples-table-with-many-rows-is-scrollable) (edge_case)

**Steps:**
```gherkin
Given Scenario "{scenario_name}" includes an examples table with {row_count} rows
When Developer views the examples table
Then the table displays with "{expected_behavior}"
```

**Examples:**

| Scenario Name | Row Count | Expected Behavior |
| --- | --- | --- |
| Bulk Transfers | 50 | scrollable table with sticky headers |

