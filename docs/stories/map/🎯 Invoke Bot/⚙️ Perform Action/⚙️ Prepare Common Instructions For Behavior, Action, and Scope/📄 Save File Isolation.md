# 📄 Save File Isolation

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L263)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Prepare Common Instructions For Behavior, Action, and Scope](.)  
**Sequential Order:** 5.4
**Story Type:** user

## Story Description

Save File Isolation functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-save-uses-test-workspace-not-production"></a>
### Scenario: [Save uses test workspace not production](#scenario-save-uses-test-workspace-not-production) (happy_path)  | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L266)

**Steps:**
```gherkin
GIVEN: Bot initialized with tmp_path workspace
WHEN: Saving any data
THEN: Data saved to tmp_path workspace, NOT production agile_bots/docs/stories
```

