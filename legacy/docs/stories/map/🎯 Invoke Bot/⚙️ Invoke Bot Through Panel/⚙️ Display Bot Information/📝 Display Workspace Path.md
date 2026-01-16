# 📝 Display Workspace Path

**Navigation:** [📋 Story Map](../../../../../story-map.drawio)

**User:** Developer
**Path:** [🎯 Invoke Bot](../../..) / [⚙️ Invoke Bot Through Panel](../..) / [⚙️ Display Bot Information](.)  
**Sequential Order:** 4
**Story Type:** user

## Story Description

Display the workspace path in the panel header so developers can see which workspace directory the bot is operating in.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** Panel loads

  **then** Workspace path is displayed in header section

  **and** Path shows full directory path

  **and** Long paths are truncated with ellipsis for readability

## Scenarios

### Scenario: Workspace path displayed (happy_path)

**Steps:**
```gherkin
Given Panel is opened
When Panel renders header
Then Workspace path is displayed
And Path shows "c:\dev\augmented-teams\agile_bot\bots\base_bot"
```


### Scenario: Long workspace path truncated (happy_path)

**Steps:**
```gherkin
Given Workspace path exceeds 80 characters
When Panel renders header
Then Path is truncated with ellipsis
And Beginning and end of path are visible
```

