# 📝 Display Bot Directory Path

**Navigation:** [📋 Story Map](../../../../../story-map.drawio)

**User:** User
**Path:** [🎯 Invoke Bot](../../..) / [⚙️ Invoke Bot Through Panel](../..) / [⚙️ Display Bot Information](.)  
**Sequential Order:** 5
**Story Type:** user

## Story Description

Display the bot directory path as read-only information to show users where the bot configuration is located.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** Panel loads

  **then** Bot directory path is displayed below workspace input

  **and** Path is truncated if too long with ellipsis in middle

  **and** Full path is shown in tooltip on hover

## Scenarios

### Scenario: Display bot directory path (happy_path)

**Steps:**
```gherkin
Given Bot is located at "c:\dev\augmented-teams\agile_bot\bots\story_bot"
When User opens Bot Status Panel
Then Bot Path label shows truncated path if needed
And Hovering over path shows full path in tooltip
```

### Scenario: Long path is truncated appropriately (happy_path)

**Steps:**
```gherkin
Given Bot path exceeds 80 characters
When Panel renders bot directory display
Then Path is truncated with "..." in middle
And Beginning and end of path remain visible
And Full path is available in tooltip
```

