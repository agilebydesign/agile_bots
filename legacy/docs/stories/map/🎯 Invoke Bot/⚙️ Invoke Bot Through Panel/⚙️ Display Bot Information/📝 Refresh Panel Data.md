# 📝 Refresh Panel Data

**Navigation:** [📋 Story Map](../../../../../story-map.drawio)

**User:** User
**Path:** [🎯 Invoke Bot](../../..) / [⚙️ Invoke Bot Through Panel](../..) / [⚙️ Display Bot Information](.)  
**Sequential Order:** 3
**Story Type:** user

## Story Description

Allow users to manually refresh panel data to see the latest bot status and workflow state.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User clicks refresh button

  **then** Panel fetches latest CLI status

  **and** Panel re-renders with updated data

  **and** User's expansion state is preserved

## Scenarios

### Scenario: User refreshes panel successfully (happy_path)

**Steps:**
```gherkin
Given Panel is displaying current bot status
When User clicks refresh button in header
Then Panel executes CLI status command
And Panel updates to show latest workflow state
And Previously expanded sections remain expanded
```

### Scenario: Refresh preserves user interactions (happy_path)

**Steps:**
```gherkin
Given User has expanded "shape" behavior
And User has collapsed "discovery" behavior
When User clicks refresh button
Then "shape" behavior remains expanded after refresh
And "discovery" behavior remains collapsed after refresh
```

