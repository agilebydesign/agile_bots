# 📝 Display And Edit Workspace Path

**Navigation:** [📋 Story Map](../../../../../story-map.drawio)

**User:** User
**Path:** [🎯 Invoke Bot](../../..) / [⚙️ Invoke Bot Through Panel](../..) / [⚙️ Display Bot Information](.)  
**Sequential Order:** 4
**Story Type:** user

## Story Description

Display the current workspace directory and allow users to change it to work with different project locations.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** Panel loads

  **then** Current workspace path is displayed in input field

- **When** User edits workspace path and presses Enter or clicks away

  **then** Bot switches to new workspace directory

  **and** Panel refreshes to show new workspace context

## Scenarios

### Scenario: Display current workspace path (happy_path)

**Steps:**
```gherkin
Given Bot is working in workspace "c:\dev\augmented-teams\agile_bot\bots\base_bot"
When User opens Bot Status Panel
Then Workspace input field shows current path
And Path is fully visible with scroll if too long
```

### Scenario: User changes workspace path (happy_path)

**Steps:**
```gherkin
Given Panel is showing current workspace
When User edits workspace path to "c:\dev\my-project"
And User presses Enter
Then Panel executes CLI command to update workspace
And Panel refreshes to show new workspace bot status
And Success message is displayed
```

### Scenario: Invalid workspace path shows error (error_path)

**Steps:**
```gherkin
Given User enters invalid or non-existent path
When User presses Enter to update workspace
Then Error message is displayed
And Workspace path reverts to previous valid path
```

