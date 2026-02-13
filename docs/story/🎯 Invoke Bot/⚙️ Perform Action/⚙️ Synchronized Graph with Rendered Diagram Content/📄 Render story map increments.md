# 📄 Render story map increments

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L534)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Synchronized Graph with Rendered Diagram Content](.)  
**Sequential Order:** 2.0
**Story Type:** user

## Story Description

Render story map increments functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-render-increments-diagram-with-stories-assigned-to-increment-lanes"></a>
### Scenario: [Render increments diagram with stories assigned to increment lanes](#scenario-render-increments-diagram-with-stories-assigned-to-increment-lanes) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L536)

**Steps:**
```gherkin
Given {StoryMap} has {StoryMap.epics} with {DrawIOSubEpic} and {DrawIOStory} nodes
And {StoryMap} has increments with stories assigned to each increment
When {DrawIOStoryMap} renders increments from {StoryMap}
Then {DrawIOStoryMap} contains {DrawIOEpic} spanning {DrawIOSubEpic} spanning {DrawIOStory}
And increment lanes rendered with {DrawIOStory} cells assigned to lanes from story graph increments
And actor labels positioned above {DrawIOStory} within each lane
And {DrawIOStory} cells styled per story_type as in outline
```


<a id="scenario-increment-lanes-ordered-by-priority-with-y-positions-from-outline-bottom"></a>
### Scenario: [Increment lanes ordered by priority with Y positions from outline bottom](#scenario-increment-lanes-ordered-by-priority-with-y-positions-from-outline-bottom) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L549)

**Steps:**
```gherkin
Given {StoryMap} has increments with priority values
When {DrawIOStoryMap} renders increments from {StoryMap}
Then lane order equals increment priority order
And lane Y positions derived from outline bottom and lane height
```


<a id="scenario-re-render-increments-with-existing-layoutdata-recomputes-lane-positions"></a>
### Scenario: [Re-render increments with existing LayoutData recomputes lane positions](#scenario-re-render-increments-with-existing-layoutdata-recomputes-lane-positions) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L560)

**Steps:**
```gherkin
Given {StoryMap} has increments with {DrawIOStory} assigned
And {LayoutData} exists with saved positions for {DrawIOEpic} and {DrawIOSubEpic}
When {DrawIOStoryMap} renders increments from {StoryMap}
Then {DrawIOStoryMap} applies {LayoutData} saved positions for {DrawIOEpic} and {DrawIOSubEpic}
And increment lane Y positions computed from outline bottom and lane height
And saved layout for increment lanes not applied on re-render
```


<a id="scenario-render-increments-completes-and-summary-includes-increment-count"></a>
### Scenario: [Render increments completes and summary includes increment count](#scenario-render-increments-completes-and-summary-includes-increment-count) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L574)

**Steps:**
```gherkin
Given {StoryMap} has increments
When {DrawIOStoryMap} renders increments from {StoryMap}
Then {DrawIOStoryMap} is written to file
And summary includes increment count
```


<a id="scenario-increment-lane-cells-styled-for-extractor-detection"></a>
### Scenario: [Increment lane cells styled for extractor detection](#scenario-increment-lane-cells-styled-for-extractor-detection) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L584)

**Steps:**
```gherkin
Given {StoryMap} has increments
When {DrawIOStoryMap} renders increments from {StoryMap}
Then increment lane {DrawIOElement} cells have fill #f5f5f5 and stroke #666666 and bold text and black font
And lane cell style has strokeColor and x less than 0 consistent with {DrawIOStoryMap}.get_increments_and_boundaries
```


<a id="scenario-render-increments-with-no-increments-defined-produces-outline-only-diagram"></a>
### Scenario: [Render increments with no increments defined produces outline-only diagram](#scenario-render-increments-with-no-increments-defined-produces-outline-only-diagram) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L594)

**Steps:**
```gherkin
Given {StoryMap} has {StoryMap.epics} but no increments defined
When {DrawIOStoryMap} renders increments from {StoryMap}
Then {DrawIOStoryMap} contains {DrawIOEpic} and {DrawIOSubEpic} and {DrawIOStory} without increment lanes
And summary reports increment count 0
```

