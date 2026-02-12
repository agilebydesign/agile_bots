# 📄 Handle Operation Errors and Validation in CLI

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L547)

**User:** User
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Prepare Common Instructions For Behavior, Action, and Scope](.)  
**Sequential Order:** 8
**Story Type:** user

## Story Description

Handle Operation Errors and Validation in CLI functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-invalid-command-shows-error"></a>
### Scenario: [Invalid command shows error](#scenario-invalid-command-shows-error) (happy_path)  | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L559)

**Steps:**
```gherkin
GIVEN: CLI is at shape.build
WHEN: user enters 'invalid_command'
THEN: CLI displays error message in appropriate channel format
```

