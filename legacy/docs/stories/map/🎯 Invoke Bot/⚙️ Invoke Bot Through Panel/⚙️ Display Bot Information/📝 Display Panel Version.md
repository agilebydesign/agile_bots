# 📝 Display Panel Version

**Navigation:** [📋 Story Map](../../../../../story-map.drawio)

**User:** User
**Path:** [🎯 Invoke Bot](../../..) / [⚙️ Invoke Bot Through Panel](../..) / [⚙️ Display Bot Information](.)  
**Sequential Order:** 1
**Story Type:** user

## Story Description

Display the current panel version number in the header to help users identify which version they're using.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** Panel loads

  **then** Version number is displayed in header (e.g., "v0.24.104")

  **and** Version number is styled with reduced opacity for subtle display

## Scenarios

### Scenario: Panel displays version number on load (happy_path)

**Steps:**
```gherkin
Given Panel extension is installed
When User opens Bot Status Panel
Then Panel header shows "Agile Bots v{version_number}"
And Version number is visible but not prominent
```

