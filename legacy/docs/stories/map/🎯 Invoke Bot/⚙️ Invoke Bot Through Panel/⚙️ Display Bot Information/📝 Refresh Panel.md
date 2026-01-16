# 📝 Refresh Panel

**Navigation:** [📋 Story Map](../../../../../story-map.drawio)

**User:** Developer
**Path:** [🎯 Invoke Bot](../../..) / [⚙️ Invoke Bot Through Panel](../..) / [⚙️ Display Bot Information](.)  
**Sequential Order:** 3
**Story Type:** user

## Story Description

Refresh the panel to update bot status and see latest changes.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** Developer clicks refresh button

  **then** Panel re-fetches bot status from CLI

  **and** Panel updates all displayed information

  **and** Current expansion state is preserved

## Scenarios

### Scenario: Refresh updates panel data (happy_path)

**Steps:**
```gherkin
Given Panel is displaying bot status
When Developer clicks refresh button
Then Panel executes CLI status command
And Panel updates displayed information
And Behavior/action expansion states are preserved
```

