# 📄 Render stories and actors

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/synchronize_graph_with_rendered_diagram/test_synchronize_stories_and_actors.py#L167)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Render DrawIO Diagrams](..) / [⚙️ Synchronize Stories and Actors](.)  
**Sequential Order:** 1.0
**Story Type:** user

## Story Description

Render stories and actors functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-render-stories-and-actors-with-default-layout-positions-stories-below-deepest-sub-epic"></a>
### Scenario: [Render stories and actors with default layout positions stories below deepest sub-epic](#scenario-render-stories-and-actors-with-default-layout-positions-stories-below-deepest-sub-epic) (happy_path)

**Steps:**
```gherkin
Given no {LayoutData} exists for this diagram
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOStory} cells are positioned below deepest {DrawIOSubEpic}
And {DrawIOStoryMap.output} is valid DrawIO XML
```


<a id="scenario-parent-sub-epic-spans-all-child-stories-horizontally"></a>
### Scenario: [Parent sub-epic spans all child stories horizontally](#scenario-parent-sub-epic-spans-all-child-stories-horizontally) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStory} is rendered with {DrawIOStory.x} and {DrawIOStory.width}
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOSubEpic} horizontal boundary encompasses all its {DrawIOStory}
```

**DrawIOStory (rendered positions):**

| name | parent | x | width |
| --- | --- | --- | --- |
| Search Rooms | Check Availability | 10 | 120 |
| Check Dates | Check Availability | 140 | 120 |


**DrawIOSubEpic (expected span):**

| name | expected_x | expected_min_width |
| --- | --- | --- |
| Check Availability | 10 | 250 |


<a id="scenario-sibling-stories-do-not-overlap-horizontally"></a>
### Scenario: [Sibling stories do not overlap horizontally](#scenario-sibling-stories-do-not-overlap-horizontally) (edge_case)

**Steps:**
```gherkin
Given {DrawIOStory} is rendered with {DrawIOStory.x} and {DrawIOStory.width}
When {DrawIOStoryMap} renders outline from {StoryMap}
Then for each adjacent pair of sibling {DrawIOStory}: left x + width <= right x
```

**DrawIOStory (sibling positions under same parent):**

| name | parent | x | width |
| --- | --- | --- | --- |
| Search Rooms | Check Availability | 10 | 120 |
| Check Dates | Check Availability | 140 | 120 |
| Add Guest | Create Booking | 280 | 120 |


<a id="scenario-re-render-with-saved-layout-data-preserves-story-and-actor-positions"></a>
### Scenario: [Re-render with saved layout data preserves story and actor positions](#scenario-re-render-with-saved-layout-data-preserves-story-and-actor-positions) (happy_path)

**Steps:**
```gherkin
Given {LayoutData} exists with saved positions for {DrawIOStory}
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOStory} is rendered at {LayoutData.saved_x} {LayoutData.saved_y}
```

**LayoutData (saved positions for DrawIOStory):**

| story_name | saved_x | saved_y |
| --- | --- | --- |
| Search Rooms | 15 | 300 |
| Check Dates | 145 | 300 |
| Add Guest | 285 | 300 |
| Confirm Reservation | 415 | 300 |

