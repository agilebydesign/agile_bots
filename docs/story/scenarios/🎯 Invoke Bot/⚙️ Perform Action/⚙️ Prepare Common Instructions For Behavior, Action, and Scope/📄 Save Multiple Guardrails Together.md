# 📄 Save Multiple Guardrails Together

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L192)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Prepare Common Instructions For Behavior, Action, and Scope](.)  
**Sequential Order:** 5.3
**Story Type:** user

## Story Description

Save Multiple Guardrails Together functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-save-all-guardrails-at-once"></a>
### Scenario: [Save all guardrails at once](#scenario-save-all-guardrails-at-once) (happy_path)  | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L195)

**Steps:**
```gherkin
GIVEN: Bot with current behavior
WHEN: User saves answers, evidence, decisions, and assumptions together
THEN: All data saved to respective files
```


<a id="scenario-save-preserves-data-across-behaviors"></a>
### Scenario: [Save preserves data across behaviors](#scenario-save-preserves-data-across-behaviors) (happy_path)  | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L225)

**Steps:**
```gherkin
GIVEN: Multiple behaviors with saved guardrails
WHEN: Switching between behaviors and saving
THEN: Each behavior's data is preserved independently
```

