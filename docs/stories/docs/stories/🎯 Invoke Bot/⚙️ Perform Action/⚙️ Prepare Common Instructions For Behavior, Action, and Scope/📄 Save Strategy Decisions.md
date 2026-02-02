# 📄 Save Strategy Decisions

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L127)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Prepare Common Instructions For Behavior, Action, and Scope](.)  
**Sequential Order:** 5.2
**Story Type:** user

## Story Description

Save Strategy Decisions functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-save-strategy-decisions"></a>
### Scenario: [Save strategy decisions](#scenario-save-strategy-decisions) (happy_path)  | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L130)

**Steps:**
```gherkin
GIVEN: Bot with strategy decision criteria
WHEN: User makes decisions via Bot.save()
THEN: Only chosen decisions saved (not entire criteria template)
```


<a id="scenario-save-strategy-assumptions"></a>
### Scenario: [Save strategy assumptions](#scenario-save-strategy-assumptions) (happy_path)  | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L161)

**Steps:**
```gherkin
GIVEN: Bot with strategy context
WHEN: User saves assumptions via Bot.save()
THEN: Assumptions saved to strategy.json
```

