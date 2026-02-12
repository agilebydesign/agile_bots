# 📄 Submit Scope Instructions

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L298)

**User:** User
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Prepare Common Instructions For Behavior, Action, and Scope](.)  
**Sequential Order:** 7
**Story Type:** user

## Story Description

Submit Scope Instructions functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-scope-appears-in-instructions-display_content-markdown"></a>
### Scenario: [Scope appears in instructions display_content markdown](#scenario-scope-appears-in-instructions-display_content-markdown) (happy_path)  | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L301)

**Steps:**
```gherkin
GIVEN: Build action with story scope set
WHEN: Instructions are retrieved via action.get_instructions()
THEN: instructions.display_content contains "## Scope" section
AND: instructions.display_content contains story_graph markdown from scope.results
AND: bot.submit_instructions() can use display_content to submit scope instructions
```


<a id="scenario-domain-concepts-are-properly-serialized-in-json-story-graph"></a>
### Scenario: [Domain concepts are properly serialized in JSON story graph](#scenario-domain-concepts-are-properly-serialized-in-json-story-graph) (happy_path)  | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py#L356)

**Steps:**
```gherkin
GIVEN: Story graph with domain_concepts at epic and sub-epic levels
WHEN: Instructions are retrieved with scope
THEN: display_content contains JSON with domain_concepts properly serialized
AND: Domain concepts from both epic and sub-epic levels are included
```

