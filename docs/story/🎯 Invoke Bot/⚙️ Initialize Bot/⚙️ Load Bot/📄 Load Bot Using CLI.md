# 📄 Load Bot Using CLI

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** User
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Initialize Bot](..) / [⚙️ Load Bot](.)  
**Sequential Order:** 6.0
**Story Type:** user

## Story Description

Load Bot Using CLI functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-cli-session-loads-bot-with-name-and-workspace"></a>
### Scenario: [CLI session loads bot with name and workspace](#scenario-cli-session-loads-bot-with-name-and-workspace) (happy_path)

**Steps:**
```gherkin
GIVEN: CLI session initialized
WHEN: Bot accessed via CLI
THEN: Bot has correct name and workspace
```


<a id="scenario-bot-name-property-accessible-via-cli-session"></a>
### Scenario: [Bot name property accessible via CLI session](#scenario-bot-name-property-accessible-via-cli-session) (happy_path)

**Steps:**
```gherkin
GIVEN: CLI session initialized
WHEN: Bot name accessed
THEN: Returns correct bot name
```

