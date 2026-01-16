# 📝 Display Version Number

**Navigation:** [📋 Story Map](../../../../../story-map.drawio)

**User:** Developer
**Path:** [🎯 Invoke Bot](../../..) / [⚙️ Invoke Bot Through Panel](../..) / [⚙️ Display Bot Information](.)  
**Sequential Order:** 1
**Story Type:** user

## Story Description

Display the bot version number in the panel header so developers can verify which version of the bot they are using.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** Panel loads

  **then** Version number is displayed in header next to "Agile Bots" title

  **and** Version format follows semantic versioning (e.g., "v0.24.104")

## Scenarios

### Scenario: Version number displayed in panel header (happy_path)

**Steps:**
```gherkin
Given Panel is opened
When Panel renders header
Then Version number is displayed as "Agile Bots v0.24.104"
And Version is positioned next to the title
```

