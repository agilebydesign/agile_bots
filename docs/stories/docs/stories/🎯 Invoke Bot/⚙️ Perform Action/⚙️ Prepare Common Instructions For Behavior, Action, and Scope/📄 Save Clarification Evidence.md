# 📄 Save Clarification Evidence

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L94)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Prepare Common Instructions For Behavior, Action, and Scope](.)  
**Sequential Order:** 5.1
**Story Type:** user

## Story Description

Save Clarification Evidence functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-save-evidence-provided"></a>
### Scenario: [Save evidence provided](#scenario-save-evidence-provided) (happy_path)  | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L97)

**Steps:**
```gherkin
GIVEN: Bot with clarification requirements
WHEN: User provides evidence via Bot.save()
THEN: Evidence saved to clarification.json
```

