# 📄 Render increment lanes

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/synchronize_graph_with_rendered_diagram/test_synchronize_increments.py#L178)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Render DrawIO Diagrams](..) / [⚙️ Synchronize Increments](.)  
**Sequential Order:** 1.0
**Story Type:** user

## Story Description

Render increment lanes functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-render-increment-lanes-with-default-layout-positions-lanes-below-outline-by-priority"></a>
### Scenario: [Render increment lanes with default layout positions lanes below outline by priority](#scenario-render-increment-lanes-with-default-layout-positions-lanes-below-outline-by-priority) (happy_path)

**Steps:**
```gherkin
Given no {LayoutData} exists for this diagram
When {DrawIOStoryMap} renders increments from {StoryMap}
Then {DrawIOStory} cells are positioned within {Increment} lanes
And {DrawIOStoryMap.output} is valid DrawIO XML
```


<a id="scenario-re-render-with-saved-layout-data-preserves-epic-and-sub-epic-positions-and-recomputes-lane-positions"></a>
### Scenario: [Re-render with saved layout data preserves epic and sub-epic positions and recomputes lane positions](#scenario-re-render-with-saved-layout-data-preserves-epic-and-sub-epic-positions-and-recomputes-lane-positions) (happy_path)

**Steps:**
```gherkin
Given {LayoutData} exists with saved positions from previous render
When {DrawIOStoryMap} renders increments from {StoryMap}
Then {DrawIOStoryMap} applies {LayoutData} saved positions for {DrawIOStory} cells
```

**LayoutData (saved positions):**

| entity_type | name | saved_x | saved_y |
| --- | --- | --- | --- |
| DrawIOEpic | Fleet Management | 100 | 50 |
| DrawIOStory | View location | 200 | 150 |


<a id="scenario-render-completes-and-writes-drawio-file-with-correct-summary-for-increment-lanes"></a>
### Scenario: [Render completes and writes DrawIO file with correct summary for increment lanes](#scenario-render-completes-and-writes-drawio-file-with-correct-summary-for-increment-lanes) (happy_path)

**Steps:**
```gherkin
Given no {LayoutData} exists for this diagram
When {DrawIOStoryMap} renders increments from {StoryMap}
Then {DrawIOStoryMap} is written to {DrawIOStoryMap.output_file}
And {DrawIOStoryMap.output} is valid DrawIO XML
And {DrawIOStoryMap.summary} reports correct counts
```


<a id="scenario-all-increment-lane-cells-have-required-styles-for-extractor-detection"></a>
### Scenario: [All increment lane cells have required styles for extractor detection](#scenario-all-increment-lane-cells-have-required-styles-for-extractor-detection) (happy_path)

**Steps:**
```gherkin
Given no {LayoutData} exists for this diagram
When {DrawIOStoryMap} renders increments from {StoryMap}
Then all increment lane cells have whiteSpace wrap and html enabled and explicit fontSize
```


<a id="scenario-render-with-no-increments-defined-produces-outline-only-diagram"></a>
### Scenario: [Render with no increments defined produces outline-only diagram](#scenario-render-with-no-increments-defined-produces-outline-only-diagram) (edge_case)

**Steps:**
```gherkin
Given {StoryMap} has no {Increment} defined
When {DrawIOStoryMap} renders increments from {StoryMap}
Then {DrawIOStoryMap} renders without increment lane elements
```


<a id="scenario-increment-lanes-ordered-by-priority-with-y-positions-from-outline-bottom"></a>
### Scenario: [Increment lanes ordered by priority with Y positions from outline bottom](#scenario-increment-lanes-ordered-by-priority-with-y-positions-from-outline-bottom) (happy_path)

**Steps:**
```gherkin
Given {StoryMap} has {Increment} with {Increment.priority} values
When {DrawIOStoryMap} renders increments from {StoryMap}
Then lane order equals {Increment.priority} order
And lane Y positions derived from outline bottom and lane height
```

**Increment (with priority values):**

| name | priority |
| --- | --- |
| MVP | 1 |
| Phase 2 | 2 |
| Phase 3 | 3 |


<a id="scenario-actor-labels-rendered-above-stories-within-each-increment-lane-deduplicated-per-lane"></a>
### Scenario: [Actor labels rendered above stories within each increment lane deduplicated per lane](#scenario-actor-labels-rendered-above-stories-within-each-increment-lane-deduplicated-per-lane) (happy_path)

**Steps:**
```gherkin
Given {StoryMap} has {Increment} with {Story} that have {StoryUser} assigned
When {DrawIOStoryMap} renders increments from {StoryMap}
Then actor labels appear above {DrawIOStory} within each increment lane
And actor labels are deduplicated per lane
And each lane has its own deduplication scope
```

**StoryUser (assigns user to Story):**

| story_name | user_name |
| --- | --- |
| View location | Fleet Manager |
| Assign driver | Fleet Manager |
| Assign driver | Dispatcher |
| Schedule service | System |

