# 📝 Collapse And Expand Bot Header

**Navigation:** [📋 Story Map](../../../../../story-map.drawio)

**User:** User
**Path:** [🎯 Invoke Bot](../../..) / [⚙️ Invoke Bot Through Panel](../..) / [⚙️ Display Bot Information](.)  
**Sequential Order:** 7
**Story Type:** user

## Story Description

Allow users to collapse and expand the bot header section to show or hide workspace and bot path details.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User clicks on bot name header

  **then** Header section toggles between expanded and collapsed

  **and** Expand icon rotates to indicate state

- **When** Header is collapsed

  **then** Workspace input and bot path are hidden

  **and** Only bot name and version remain visible

## Scenarios

### Scenario: Collapse bot header (happy_path)

**Steps:**
```gherkin
Given Bot header is expanded showing workspace details
When User clicks on bot name header
Then Header collapses smoothly with animation
And Workspace input and bot path are hidden
And Expand arrow points right (►)
```

### Scenario: Expand bot header (happy_path)

**Steps:**
```gherkin
Given Bot header is collapsed
When User clicks on bot name header
Then Header expands smoothly with animation
And Workspace input and bot path become visible
And Expand arrow points down (▼)
```

### Scenario: Header expansion state persists during refresh (happy_path)

**Steps:**
```gherkin
Given User has collapsed bot header
When User refreshes panel
Then Bot header remains collapsed after refresh
And User's preference is maintained
```

