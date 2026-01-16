# 📝 Display Bot Path

**Navigation:** [📋 Story Map](../../../../../story-map.drawio)

**User:** Developer
**Path:** [🎯 Invoke Bot](../../..) / [⚙️ Invoke Bot Through Panel](../..) / [⚙️ Display Bot Information](.)  
**Sequential Order:** 6
**Story Type:** user

## Story Description

Display the bot directory path in the panel header so developers can see which bot instance is active.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** Panel loads

  **then** Bot path is displayed in header section

  **and** Path shows full bot directory (e.g., "c:\dev\augmented-teams\agile_bot\bots\story_bot")

  **and** Path is read-only (not editable)

## Scenarios

### Scenario: Bot path displayed (happy_path)

**Steps:**
```gherkin
Given Panel is opened
When Panel renders header
Then Bot path label "Bot Path:" is displayed
And Bot directory path is shown below workspace path
And Path displays "c:\dev\augmented-teams\agile_bot\bots\story_bot"
```

