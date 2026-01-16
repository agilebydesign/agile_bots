# 📝 Expand And Collapse Bot Information Section

**Navigation:** [📋 Story Map](../../../../../story-map.drawio)

**User:** Developer
**Path:** [🎯 Invoke Bot](../../..) / [⚙️ Invoke Bot Through Panel](../..) / [⚙️ Display Bot Information](.)  
**Sequential Order:** 7
**Story Type:** user

## Story Description

Expand and collapse the bot information section to show or hide workspace and bot path details.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** Developer clicks bot information header

  **then** Section expands to show workspace and bot path

  **or** Section collapses to hide details

  **and** Expansion state is preserved during refresh

## Scenarios

### Scenario: Bot information section collapsed (happy_path)

**Steps:**
```gherkin
Given Bot information section is expanded
When Developer clicks bot name header
Then Section collapses
And Workspace and bot path are hidden
And Arrow icon rotates to indicate collapsed state
```


### Scenario: Bot information section expanded (happy_path)

**Steps:**
```gherkin
Given Bot information section is collapsed
When Developer clicks bot name header
Then Section expands
And Workspace input and bot path are visible
And Arrow icon rotates to indicate expanded state
```

