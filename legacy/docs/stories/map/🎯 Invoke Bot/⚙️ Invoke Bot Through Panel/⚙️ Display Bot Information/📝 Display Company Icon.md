# 📝 Display Company Icon

**Navigation:** [📋 Story Map](../../../../../story-map.drawio)

**User:** User
**Path:** [🎯 Invoke Bot](../../..) / [⚙️ Invoke Bot Through Panel](../..) / [⚙️ Display Bot Information](.)  
**Sequential Order:** 2
**Story Type:** user

## Story Description

Display the company icon in the panel header for branding and visual identification.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** Panel loads

  **then** Company icon is displayed in main header

  **and** Icon is loaded from extension resources

## Scenarios

### Scenario: Company icon displays in header (happy_path)

**Steps:**
```gherkin
Given Panel extension has company_icon.png bundled
When User opens Bot Status Panel
Then Company icon is displayed at top of panel
And Icon renders correctly without errors
```

### Scenario: Icon fails to load gracefully (error_path)

**Steps:**
```gherkin
Given Company icon file cannot be loaded
When Panel attempts to render header
Then Icon space is preserved
And Error is logged to console
And Panel continues to function normally
```

