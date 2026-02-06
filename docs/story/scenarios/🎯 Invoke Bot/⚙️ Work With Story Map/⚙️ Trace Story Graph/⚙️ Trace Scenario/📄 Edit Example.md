# 📄 Edit Example

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** Developer
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Trace Story Graph](..) / [⚙️ Trace Scenario](.)  
**Sequential Order:** 6.0
**Story Type:** user

## Story Description

Edit Example functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-add-example-row-appends-empty-cells"></a>
### Scenario: [Add example row appends empty cells](#scenario-add-example-row-appends-empty-cells) (happy_path)

**Steps:**
```gherkin
Given Scenario "{scenario_name}" has an examples table with columns "{columns}" and row "{existing_row}"
When Developer clicks Add Row
Then a new empty row is added and focus moves to the first cell
```

**Examples:**

| Scenario Name | Columns | Existing Row | Expected Result |
| --- | --- | --- | --- |
| Approve Transfer | Transfer Type, Amount | Wire, 25000 | row added with empty cells and focus on first cell |


<a id="scenario-deleting-last-row-leaves-headers-intact"></a>
### Scenario: [Deleting last row leaves headers intact](#scenario-deleting-last-row-leaves-headers-intact) (edge_case)

**Steps:**
```gherkin
Given Scenario "{scenario_name}" has an examples table with columns "{columns}" and {row_count} row
When Developer deletes the last row
Then the table remains with headers and no rows
```

**Examples:**

| Scenario Name | Columns | Row Count | Expected Result |
| --- | --- | --- | --- |
| Approve Transfer | Transfer Type, Amount | 1 | headers remain with zero rows |


<a id="scenario-duplicate-column-name-shows-validation-error"></a>
### Scenario: [Duplicate column name shows validation error](#scenario-duplicate-column-name-shows-validation-error) (error_case)

**Steps:**
```gherkin
Given Scenario "{scenario_name}" has columns "{existing_columns}"
When Developer adds a column named "{new_column_name}"
Then the trace editor shows error "{error_message}" and does not add the column
```

**Examples:**

| Scenario Name | Existing Columns | New Column Name | Error Message |
| --- | --- | --- | --- |
| Approve Transfer | Transfer Type, Amount | Amount | Column name already exists |

