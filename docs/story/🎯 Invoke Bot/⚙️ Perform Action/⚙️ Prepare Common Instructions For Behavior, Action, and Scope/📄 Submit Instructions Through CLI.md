# 📄 Submit Instructions Through CLI

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** User
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Prepare Common Instructions For Behavior, Action, and Scope](.)  
**Sequential Order:** 2.0
**Story Type:** user

## Story Description

Submit Instructions Through CLI functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User executes submit command
  **then** System tracks instruction submission
  **and** System returns success status with timestamp

- **When** User runs CLI submit with behavior only (e.g. behaviors.shape.submit)
  **then** System prepares instructions for the whole behavior (all actions per manual / combine_with_next / skip)
  **and** System returns success status with timestamp

- **When** User runs CLI submit with behavior and action (e.g. behaviors.shape.clarify.submit)
  **then** System prepares instructions for that action
  **and** System returns success status with timestamp

## Scenarios

<a id="scenario-user-submits-current-action-instructions"></a>
### Scenario: [User submits current action instructions](#scenario-user-submits-current-action-instructions) (happy_path)

**Steps:**
```gherkin
GIVEN: CLI is at shape.clarify
WHEN: user enters 'submit'
THEN: CLI tracks instruction submission
AND: CLI returns success message with behavior and action
AND: CLI includes timestamp of submission
```


<a id="scenario-submit-command-fails-when-no-current-action"></a>
### Scenario: [Submit command fails when no current action](#scenario-submit-command-fails-when-no-current-action) (error)

**Steps:**
```gherkin
GIVEN: CLI has no current action set
WHEN: user enters 'submit'
THEN: CLI displays error message
AND: Error indicates no current action
```


<a id="scenario-cli-submit-with-behavior-only-prepares-whole-behavior-instructions"></a>
### Scenario: [CLI submit with behavior only prepares whole-behavior instructions](#scenario-cli-submit-with-behavior-only-prepares-whole-behavior-instructions) (happy_path)

**Steps:**
```gherkin
Given User is in CLI (no Panel)
When User runs behaviors.shape.submit
Then CLI/Bot prepares instructions for whole shape behavior (all actions per manual/combine_with_next/skip)
And CLI returns success message with behavior name and timestamp
```


<a id="scenario-cli-submit-with-behavior-and-action-prepares-action-instructions"></a>
### Scenario: [CLI submit with behavior and action prepares action instructions](#scenario-cli-submit-with-behavior-and-action-prepares-action-instructions) (happy_path)

**Steps:**
```gherkin
Given User is in CLI (no Panel)
When User runs behaviors.shape.clarify.submit
Then CLI/Bot prepares instructions for shape.clarify
And CLI returns success message with behavior and action and timestamp
```

