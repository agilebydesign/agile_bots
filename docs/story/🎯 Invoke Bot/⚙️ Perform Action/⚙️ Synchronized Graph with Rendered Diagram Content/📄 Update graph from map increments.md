# 📄 Update graph from map increments

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L806)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Synchronized Graph with Rendered Diagram Content](.)  
**Sequential Order:** 5.0
**Story Type:** user

## Story Description

Update graph from map increments functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-extract-increments-assigns-stories-to-lanes-by-y-position-with-priority-from-order"></a>
### Scenario: [Extract increments assigns stories to lanes by Y position with priority from order](#scenario-extract-increments-assigns-stories-to-lanes-by-y-position-with-priority-from-order) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L808)

**Steps:**
```gherkin
Given {DrawIOStoryMap} increments file contains increment lane cells and {DrawIOStory} cells
When {DrawIOStoryMap} extracts increments from {DrawIOStoryMap}
Then {DrawIOStoryMap} identifies increment lanes from left side of diagram by style sorted top to bottom
And each {DrawIOStory} assigned to nearest lane within 100px by Y position
And each lane gets position-based priority and name from cell label
And extracted JSON written to file
```


<a id="scenario-updatereport-generated-for-increments-view-with-story-level-matches"></a>
### Scenario: [UpdateReport generated for increments view with story-level matches](#scenario-updatereport-generated-for-increments-view-with-story-level-matches) ()

**Steps:**
```gherkin
Given {DrawIOStoryMap} increments have been extracted
And original {StoryMap} provided
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs for increments view
Then {UpdateReport} lists story-level exact matches and fuzzy matches and new stories and removed stories
And increment membership in extracted reflects {DrawIOStoryMap} lane positions
```


<a id="scenario-story-moved-between-increments-reflected-in-extracted-graph"></a>
### Scenario: [Story moved between increments reflected in extracted graph](#scenario-story-moved-between-increments-reflected-in-extracted-graph) ()

**Steps:**
```gherkin
Given {DrawIOStory} has been moved from one increment lane to another in {DrawIOStoryMap}
When {DrawIOStoryMap} extracts increments from {DrawIOStoryMap}
Then extracted graph reflects new increment membership for that {DrawIOStory} based on Y position
```


<a id="scenario-merge-preserves-original-ac-and-updates-story-fields-with-position-based-increment-matching"></a>
### Scenario: [Merge preserves original AC and updates story fields with position-based increment matching](#scenario-merge-preserves-original-ac-and-updates-story-fields-with-position-based-increment-matching) ()

**Steps:**
```gherkin
Given {UpdateReport} has been generated from {DrawIOStoryMap} increments vs {StoryMap}
When {StoryMap}.update({DrawIOStoryMap}, {UpdateReport}) runs for increments view
Then {StoryMap} preserves original acceptance_criteria and steps
And {StoryMap} updates {DrawIOStory} fields (users, sequential_order) from extracted
And increments matched by position (first extracted lane to first original lane)
And renamed increments updated
And extra lanes appended as new increments
And merge does not remove increments or replace which stories belong to which increment
```


<a id="scenario-new-increment-lane-at-bottom-appended-as-new-increment"></a>
### Scenario: [New increment lane at bottom appended as new increment](#scenario-new-increment-lane-at-bottom-appended-as-new-increment) ()

**Steps:**
```gherkin
Given a new increment lane exists at the bottom of {DrawIOStoryMap}
When {DrawIOStoryMap} extracts increments from {DrawIOStoryMap}
And {StoryMap}.update({DrawIOStoryMap}, {UpdateReport}) runs
Then extracted graph has one more increment
And merge appends the new lane as a new increment in {StoryMap}
```


<a id="scenario-removed-increment-lane-stays-in-merged-with-its-original-stories"></a>
### Scenario: [Removed increment lane stays in merged with its original stories](#scenario-removed-increment-lane-stays-in-merged-with-its-original-stories) ()

**Steps:**
```gherkin
Given an increment lane has been removed from {DrawIOStoryMap}
When {DrawIOStoryMap} extracts increments from {DrawIOStoryMap}
Then extracted has fewer lanes
And {DrawIOStory} from deleted lane reassigned to nearest remaining lane in extracted
When {StoryMap}.update({DrawIOStoryMap}, {UpdateReport}) runs
Then merge does not remove the increment from {StoryMap}
And removed lane stays in merged {StoryMap} with its original stories
```


<a id="scenario-renamed-increment-lane-updated-by-position-based-matching"></a>
### Scenario: [Renamed increment lane updated by position-based matching](#scenario-renamed-increment-lane-updated-by-position-based-matching) ()

**Steps:**
```gherkin
Given an increment lane has been renamed in {DrawIOStoryMap}
When {DrawIOStoryMap} extracts increments from {DrawIOStoryMap}
And {StoryMap}.update({DrawIOStoryMap}, {UpdateReport}) runs
Then merge treats the lane at that position as the same increment
And updates its name in {StoryMap}
```


<a id="scenario-storymap"></a>
### Scenario: [StoryMap](#scenario-storymap) (outline)

**Steps:**
```gherkin
Given original {StoryMap} has {StoryMap.increment_count} increment lanes
And extracted {DrawIOStoryMap} has {DrawIOStoryMap.increment_count} increment lanes
When {StoryMap}.update({DrawIOStoryMap}, {UpdateReport}) runs
Then {UpdateReport.merge_result}
```

**StoryMap (Update from other):**

| StoryMap.increment_count | DrawIOStoryMap.increment_count | UpdateReport.merge_result |
| --- | --- | --- |
| 3 | 5 | extra 2 lanes appended as new increments |
| 5 | 3 | original lanes 4 and 5 remain unchanged (merge does not remove) |


<a id="scenario-known-inserting-lane-between-existing-may-misinterpret-without-stable-ids"></a>
### Scenario: [KNOWN: inserting lane between existing may misinterpret without stable IDs](#scenario-known-inserting-lane-between-existing-may-misinterpret-without-stable-ids) ()

**Steps:**
```gherkin
Given original {StoryMap} has increment lanes [A, B, C]
And a new lane has been inserted between A and B in {DrawIOStoryMap}
When {DrawIOStoryMap} extracts increments from {DrawIOStoryMap}
Then position-based matching maps extracted lane 1 to original A and lane 2 to original B
And the inserted lane may be misinterpreted as a rename of B without stable IDs
```


<a id="scenario-story-not-within-100px-of-any-lane-remains-unassigned-in-extracted"></a>
### Scenario: [Story not within 100px of any lane remains unassigned in extracted](#scenario-story-not-within-100px-of-any-lane-remains-unassigned-in-extracted) ()

**Steps:**
```gherkin
Given {DrawIOStoryMap} increments file has {DrawIOStory} positioned more than 100px from any increment lane
When {DrawIOStoryMap} extracts increments from {DrawIOStoryMap}
Then that {DrawIOStory} is not assigned to any increment lane in extracted graph
```

