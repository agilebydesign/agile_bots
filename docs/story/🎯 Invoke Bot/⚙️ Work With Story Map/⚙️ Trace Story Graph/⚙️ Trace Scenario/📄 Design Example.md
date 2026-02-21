# 📄 Design Example

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/edit_story_map)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Trace Story Graph](..) / [⚙️ Trace Scenario](.)  
**Sequential Order:** 5.0
**Story Type:** user

## Story Description

Design Example functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

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

