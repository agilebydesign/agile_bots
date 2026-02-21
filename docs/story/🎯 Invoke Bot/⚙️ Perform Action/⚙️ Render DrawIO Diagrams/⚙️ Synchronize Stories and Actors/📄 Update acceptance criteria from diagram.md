# 📄 Update acceptance criteria from diagram

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/synchronize_graph_with_rendered_diagram/test_synchronize_stories_and_actors.py#L525)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Render DrawIO Diagrams](..) / [⚙️ Synchronize Stories and Actors](.)  
**Sequential Order:** 6.0
**Story Type:** user

## Story Description

Update acceptance criteria from diagram functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-apply-acceptance-criteria-changes-from-report-updates-story-graph"></a>
### Scenario: [Apply acceptance criteria changes from report updates story graph](#scenario-apply-acceptance-criteria-changes-from-report-updates-story-graph) (happy_path)

**Steps:**
```gherkin
Given {UpdateReport} has acceptance criteria changes
When {UpdateReport} is applied to {StoryMap}
Then {StoryMap} reflects the {AcceptanceCriteria} additions and removals from {UpdateReport}
```

**ACChange (acceptance criteria changes in UpdateReport):**

| story_name | criteria_text | change_type |
| --- | --- | --- |
| Search catalog | When catalog is searched then results display within 2 seconds | removed |
| Enroll in section | When student has prerequisites then enrollment succeeds | added |


<a id="scenario-apply-ac-move-transfers-between-stories-preserving-data"></a>
### Scenario: [Apply AC move transfers between stories preserving data](#scenario-apply-ac-move-transfers-between-stories-preserving-data) (happy_path)

**Steps:**
```gherkin
Given {UpdateReport} contains an {AcceptanceCriteria} move from one {Story} to another
When move is applied to {StoryMap}
Then {AcceptanceCriteria} is removed from source {Story} and added to target {Story}
And all {AcceptanceCriteria} fields are preserved
```

**ACChange (move from one story to another):**

| text | from_story | to_story |
| --- | --- | --- |
| When catalog is searched then results display within 2 seconds | Search catalog | Add to cart |


<a id="scenario-story-split-distributes-ac-correctly-to-new-and-original-stories"></a>
### Scenario: [Story split distributes AC correctly to new and original stories](#scenario-story-split-distributes-ac-correctly-to-new-and-original-stories) (edge_case)

**Steps:**
```gherkin
Given {Story} has been split in diagram with some {AcceptanceCriteria} moved to a new {DrawIOStory}
When {UpdateReport} is applied to {StoryMap}
Then {AcceptanceCriteria} is distributed correctly between original and new {Story}
And no {AcceptanceCriteria} is lost in the split
```

**DrawIOStory (original and new after split):**

| name | parent | story_type |
| --- | --- | --- |
| Search catalog | Browse Courses | user |
| Filter by department | Browse Courses | user |


**AcceptanceCriteria (distributed between stories):**

| text | parent_story | sequential_order |
| --- | --- | --- |
| When catalog is searched then results display within 2 seconds | Search catalog | 1.0 |
| When department filter applied then results narrow | Filter by department | 1.0 |


<a id="scenario-update-preserves-original-acceptance-criteria-for-matched-stories"></a>
### Scenario: [Update preserves original acceptance criteria for matched stories](#scenario-update-preserves-original-acceptance-criteria-for-matched-stories) (happy_path)

**Steps:**
```gherkin
Given {UpdateReport} has matched {AcceptanceCriteria} between diagram and {StoryMap}
When {UpdateReport} is applied to {StoryMap}
Then original {AcceptanceCriteria.text} and scenarios are preserved for matched {AcceptanceCriteria}
```


<a id="scenario-end-to-end-render-then-report-then-update-for-acceptance-criteria"></a>
### Scenario: [End-to-end render then report then update for acceptance criteria](#scenario-end-to-end-render-then-report-then-update-for-acceptance-criteria) (happy_path)

**Steps:**
```gherkin
Given {StoryMap} has {AcceptanceCriteria}
When {DrawIOStoryMap} renders from {StoryMap}
And user modifies acceptance criteria in diagram
And {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
And {UpdateReport} is applied to {StoryMap}
Then {StoryMap} reflects all acceptance criteria changes from diagram
```

