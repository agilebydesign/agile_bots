# 📄 Update increments from diagram

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/synchronize_graph_with_rendered_diagram/test_synchronize_increments.py#L395)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Render DrawIO Diagrams](..) / [⚙️ Synchronize Increments](.)  
**Sequential Order:** 3.0
**Story Type:** user

## Story Description

Update increments from diagram functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-apply-increment-move-transfers-story-between-increments-preserving-data"></a>
### Scenario: [Apply increment move transfers story between increments preserving data](#scenario-apply-increment-move-transfers-story-between-increments-preserving-data) (happy_path)

**Steps:**
```gherkin
Given {UpdateReport} contains an {IncrementChange} move from one {Increment} to another
When move is applied to {StoryMap}
Then {IncrementStory} is removed from source {Increment} and added to target {Increment}
And all increment fields are preserved
```

**IncrementChange (story moved between increments):**

| increment_name | story_name | change_type |
| --- | --- | --- |
| MVP | Publish event | removed |
| Phase 2 | Publish event | added |


<a id="scenario-removed-increment-deletes-entire-increment-from-story-graph"></a>
### Scenario: [Removed increment deletes entire increment from story graph](#scenario-removed-increment-deletes-entire-increment-from-story-graph) (edge_case)

**Steps:**
```gherkin
Given {UpdateReport} contains a removed {Increment}
When removal is applied to {StoryMap}
Then the entire {Increment} and its {IncrementStory} assignments are deleted from {StoryMap}
```

**Increment (removed):**

| name | priority |
| --- | --- |
| Phase 2 | 2 |


**IncrementStory (deleted with increment):**

| increment_name | story_name |
| --- | --- |
| Phase 2 | Register attendee |
| Phase 2 | Reserve venue |


<a id="scenario-renamed-increment-lane-in-diagram-updates-name-in-story-graph"></a>
### Scenario: [Renamed increment lane in diagram updates name in story graph](#scenario-renamed-increment-lane-in-diagram-updates-name-in-story-graph) (happy_path)

**Steps:**
```gherkin
Given {Increment} lane has been renamed in {DrawIOStoryMap}
When {UpdateReport} is applied to {StoryMap}
Then {StoryMap} updates the {Increment.name} to match diagram
```

**Increment (renamed in diagram):**

| original_name | new_name |
| --- | --- |
| Phase 2 | Phase Two |


<a id="scenario-new-increment-lane-in-diagram-creates-it-in-story-graph"></a>
### Scenario: [New increment lane in diagram creates it in story graph](#scenario-new-increment-lane-in-diagram-creates-it-in-story-graph) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has a new {Increment} not in original {StoryMap}
When {UpdateReport} is applied to {StoryMap}
Then {StoryMap} creates the new {Increment}
```

**Increment (new in diagram):**

| name | priority |
| --- | --- |
| MVP | 1 |
| Phase 2 | 2 |
| Phase 3 | 3 |


<a id="scenario-update-preserves-original-acceptance-criteria-for-matched-increment-stories"></a>
### Scenario: [Update preserves original acceptance criteria for matched increment stories](#scenario-update-preserves-original-acceptance-criteria-for-matched-increment-stories) (happy_path)

**Steps:**
```gherkin
Given {UpdateReport} has matched {Increment} between diagram and {StoryMap}
When {UpdateReport} is applied to {StoryMap}
Then original {AcceptanceCriteria} and scenarios are preserved for matched {IncrementStory}
```

**AcceptanceCriteria (preserved for matched IncrementStory):**

| text | parent_story |
| --- | --- |
| When event is published then it appears in catalog | Publish event |


<a id="scenario-end-to-end-render-then-report-then-update-for-increment-lanes"></a>
### Scenario: [End-to-end render then report then update for increment lanes](#scenario-end-to-end-render-then-report-then-update-for-increment-lanes) (happy_path)

**Steps:**
```gherkin
Given {StoryMap} has {Increment}
When {DrawIOStoryMap} renders from {StoryMap}
And user modifies increments in diagram
And {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
And {UpdateReport} is applied to {StoryMap}
Then {StoryMap} reflects all increment changes from diagram
```

**Increment (added by user):**

| name | priority |
| --- | --- |
| Phase 3 | 3 |


<a id="scenario-removing-non-existent-increment-returns-false"></a>
### Scenario: [Removing non-existent increment returns false](#scenario-removing-non-existent-increment-returns-false) (error_case)

**Steps:**
```gherkin
Given {UpdateReport} references an {Increment} that does not exist in {StoryMap}
When removal is applied to {StoryMap}
Then removal returns false and {StoryMap} is unchanged
```

**Increment (referenced but not in graph):**

| name |
| --- |
| Phase 4 |


<a id="scenario-update-increment-order-from-diagram-updates-priorities-in-story-graph"></a>
### Scenario: [Update increment order from diagram updates priorities in story graph](#scenario-update-increment-order-from-diagram-updates-priorities-in-story-graph) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has {Increment} lanes in a new order different from {StoryMap}
When {UpdateReport} is applied to {StoryMap}
Then {Increment.priority} in {StoryMap} are updated to match diagram order
```

**Increment (new order in diagram):**

| name | priority |
| --- | --- |
| Phase 2 | 1 |
| MVP | 2 |


<a id="scenario-no-changes-when-increment-priorities-already-match-diagram-order"></a>
### Scenario: [No changes when increment priorities already match diagram order](#scenario-no-changes-when-increment-priorities-already-match-diagram-order) (happy_path)

**Steps:**
```gherkin
Given {Increment.priority} in {StoryMap} already match {DrawIOStoryMap} diagram order
When {UpdateReport} is applied to {StoryMap}
Then no {Increment.priority} changes are made
```


<a id="scenario-extra-lanes-appended-and-fewer-lanes-leave-original-increments-unchanged"></a>
### Scenario: [Extra lanes appended and fewer lanes leave original increments unchanged](#scenario-extra-lanes-appended-and-fewer-lanes-leave-original-increments-unchanged) (edge_case)

**Steps:**
```gherkin
Given original {StoryMap} has fewer {Increment} lanes than {DrawIOStoryMap}
When {UpdateReport} is applied to {StoryMap}
Then extra {Increment} lanes are appended and original {Increment} unchanged
```

**Increment (appended):**

| name | priority |
| --- | --- |
| Phase 3 | 3 |

