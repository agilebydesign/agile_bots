# 📄 Save Clarification Answers

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L22)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Prepare Common Instructions For Behavior, Action, and Scope](.)  
**Sequential Order:** 5.0
**Story Type:** user

## Story Description

Save Clarification Answers functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-save-new-clarification-answers"></a>
### Scenario: [Save new clarification answers](#scenario-save-new-clarification-answers) (happy_path)  | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L25)

**Steps:**
```gherkin
GIVEN: Bot with no existing clarifications
WHEN: User saves answers via Bot.save()
THEN: Answers saved to clarification.json in test workspace
```


<a id="scenario-save-merges-with-existing-clarification-answers"></a>
### Scenario: [Save merges with existing clarification answers](#scenario-save-merges-with-existing-clarification-answers) (happy_path)  | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L60)

**Steps:**
```gherkin
GIVEN: Bot with existing clarification answers
WHEN: User saves additional/modified answers
THEN: New answers merged with existing, new overrides existing for same question
```

