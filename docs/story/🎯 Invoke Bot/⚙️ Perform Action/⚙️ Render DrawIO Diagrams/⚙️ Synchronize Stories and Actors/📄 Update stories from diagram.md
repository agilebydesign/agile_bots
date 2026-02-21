# 📄 Update stories from diagram

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/synchronize_graph_with_rendered_diagram/test_synchronize_stories_and_actors.py#L429)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Render DrawIO Diagrams](..) / [⚙️ Synchronize Stories and Actors](.)  
**Sequential Order:** 5.0
**Story Type:** user

## Story Description

Update stories from diagram functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-apply-story-move-transfers-between-sub-epics-preserving-data"></a>
### Scenario: [Apply story move transfers between sub-epics preserving data](#scenario-apply-story-move-transfers-between-sub-epics-preserving-data) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStory} has been moved to a new position in {DrawIOStoryMap}
When {DrawIOStoryMap} extracts and generates {UpdateReport}
Then {DrawIOStory.sequential_order} is recomputed from new left-to-right position
And {UpdateReport} matches the moved {DrawIOStory} to original
```

**StoryMove (describes move):**

| name | from_parent | to_parent |
| --- | --- | --- |
| List available units | List Properties | Screen Tenants |


<a id="scenario-apply-story-move-preserves-all-story-fields"></a>
### Scenario: [Apply story move preserves all story fields](#scenario-apply-story-move-preserves-all-story-fields) (happy_path)

**Steps:**
```gherkin
Given {UpdateReport} contains a {StoryMove} for {DrawIOStory}
When {StoryMove} is applied to {StoryMap}
Then {Story.acceptance_criteria} are preserved after move
And {Story.scenarios} are preserved after move
And {Story.users} and {Story.story_type} are preserved after move
```

**StoryMove (for story being moved):**

| name | from_parent | to_parent |
| --- | --- | --- |
| List available units | List Properties | Screen Tenants |


<a id="scenario-apply-cross-epic-story-move-preserves-acceptance-criteria-and-scenarios"></a>
### Scenario: [Apply cross-epic story move preserves acceptance criteria and scenarios](#scenario-apply-cross-epic-story-move-preserves-acceptance-criteria-and-scenarios) (edge_case)

**Steps:**
```gherkin
Given {DrawIOStory} has been moved from {SubEpic} under one {Epic} to {SubEpic} under a different {Epic}
When cross-epic {StoryMove} is applied to {StoryMap}
Then {Story.acceptance_criteria} survive the cross-epic move
And {Story.scenarios} survive the cross-epic move
```

**Epic (additional for cross-epic move):**

| name |
| --- |
| Property Management |
| Tenant Services |


**SubEpic (additional for cross-epic move):**

| name | parent |
| --- | --- |
| List Properties | Property Management |
| Screen Tenants | Tenant Services |


**StoryMove (cross-epic move):**

| name | from_parent | to_parent |
| --- | --- | --- |
| List available units | List Properties | Screen Tenants |


<a id="scenario-removed-story-keeps-original-structure-and-flags-if-many-missing-from-epic"></a>
### Scenario: [Removed story keeps original structure and flags if many missing from epic](#scenario-removed-story-keeps-original-structure-and-flags-if-many-missing-from-epic) (edge_case)

**Steps:**
```gherkin
Given one {DrawIOStory} cell has been removed from {DrawIOStoryMap}
When {DrawIOStoryMap} extracts from diagram
Then extracted graph omits that {DrawIOStory}
And {UpdateReport} lists it as removed
And if many {DrawIOStory} from one {Epic} are missing the {UpdateReport} flags that {Epic}
```

**DrawIOStory (removed from diagram):**

| name | parent |
| --- | --- |
| List available units | List Properties |


<a id="scenario-moved-stories-preserved-when-sub-epic-removed-from-diagram"></a>
### Scenario: [Moved stories preserved when sub-epic removed from diagram](#scenario-moved-stories-preserved-when-sub-epic-removed-from-diagram) (edge_case)

**Steps:**
```gherkin
Given {DrawIOStory} has been moved to another {SubEpic} in {DrawIOStoryMap}
And the original {SubEpic} is being removed
When {UpdateReport} is applied (moves before removes)
Then moved {Story} survives the {SubEpic} removal
```

**StoryMove (describes move before sub-epic removal):**

| name | from_parent | to_parent |
| --- | --- | --- |
| List available units | List Properties | Screen Tenants |


<a id="scenario-unmoved-stories-removed-with-sub-epic-when-sub-epic-removed-from-diagram"></a>
### Scenario: [Unmoved stories removed with sub-epic when sub-epic removed from diagram](#scenario-unmoved-stories-removed-with-sub-epic-when-sub-epic-removed-from-diagram) (edge_case)

**Steps:**
```gherkin
Given {DrawIOStory} was NOT moved to another {SubEpic}
And the {SubEpic} is being removed
When {UpdateReport} is applied
Then unmoved {Story} is removed along with its {SubEpic}
```

**SubEpic (being removed):**

| name | parent |
| --- | --- |
| List Properties | Property Management |


**Story (unmoved, removed with sub-epic):**

| name | parent |
| --- | --- |
| List available units | List Properties |
| Schedule viewings | List Properties |


<a id="scenario-move-to-renamed-sub-epic-updates-correctly-in-story-graph"></a>
### Scenario: [Move to renamed sub-epic updates correctly in story graph](#scenario-move-to-renamed-sub-epic-updates-correctly-in-story-graph) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStory} has been renamed in {DrawIOStoryMap}
When {UpdateReport} is applied to {StoryMap}
Then {StoryMap} updates the story name to match {DrawIOStory}
```

**DrawIOStory (renamed in diagram):**

| original_name | new_name | parent |
| --- | --- | --- |
| List available units | List all units | List Properties |


<a id="scenario-move-to-new-sub-epic-creates-it-and-transfers-story"></a>
### Scenario: [Move to new sub-epic creates it and transfers story](#scenario-move-to-new-sub-epic-creates-it-and-transfers-story) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has a new {DrawIOStory} not in original {StoryMap}
When {UpdateReport} is applied to {StoryMap}
Then {StoryMap} creates the new {Story}
```

**DrawIOStory (new in diagram):**

| name | parent | story_type |
| --- | --- | --- |
| Process applications | Screen Tenants | user |


<a id="scenario-end-to-end-render-then-report-then-update-for-story-moves"></a>
### Scenario: [End-to-end render then report then update for story moves](#scenario-end-to-end-render-then-report-then-update-for-story-moves) (happy_path)

**Steps:**
```gherkin
Given {StoryMap} has {Story}
When {DrawIOStoryMap} renders from {StoryMap}
And user modifies stories in diagram
And {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
And {UpdateReport} is applied to {StoryMap}
Then {StoryMap} reflects all story changes from diagram
```

**StoryMove (user modification):**

| name | from_parent | to_parent |
| --- | --- | --- |
| List available units | List Properties | Screen Tenants |

