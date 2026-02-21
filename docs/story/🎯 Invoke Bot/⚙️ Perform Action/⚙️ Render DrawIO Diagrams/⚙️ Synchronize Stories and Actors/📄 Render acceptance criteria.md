# 📄 Render acceptance criteria

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/synchronize_graph_with_rendered_diagram/test_synchronize_stories_and_actors.py#L224)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Render DrawIO Diagrams](..) / [⚙️ Synchronize Stories and Actors](.)  
**Sequential Order:** 2.0
**Story Type:** user

## Story Description

Render acceptance criteria functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-render-acceptance-criteria-with-default-layout-positions-ac-boxes-below-stories"></a>
### Scenario: [Render acceptance criteria with default layout positions AC boxes below stories](#scenario-render-acceptance-criteria-with-default-layout-positions-ac-boxes-below-stories) (happy_path)

**Steps:**
```gherkin
Given no {LayoutData} exists for this diagram
When {DrawIOStoryMap} renders exploration from {StoryMap}
Then {DrawIOElement} AC boxes are positioned below each {DrawIOStory}
And {DrawIOStoryMap.output} is valid DrawIO XML
```


<a id="scenario-re-render-with-saved-layout-data-preserves-story-and-ac-box-positions"></a>
### Scenario: [Re-render with saved layout data preserves story and AC box positions](#scenario-re-render-with-saved-layout-data-preserves-story-and-ac-box-positions) (happy_path)

**Steps:**
```gherkin
Given {LayoutData} exists with saved positions for {DrawIOStory} and {DrawIOElement}
When {DrawIOStoryMap} renders exploration from {StoryMap}
Then {DrawIOStory} and {DrawIOElement} AC boxes are rendered at {LayoutData} saved positions
```

**LayoutData (saved positions):**

| entity_type | name | saved_x | saved_y |
| --- | --- | --- | --- |
| DrawIOStory | Add to Cart | 10 | 300 |
| DrawIOElement | When product in stock... | 10 | 360 |
| DrawIOElement | When product out of stock... | 10 | 400 |


<a id="scenario-render-with-no-acceptance-criteria-produces-story-without-ac-boxes"></a>
### Scenario: [Render with no acceptance criteria produces story without AC boxes](#scenario-render-with-no-acceptance-criteria-produces-story-without-ac-boxes) (edge_case)

**Steps:**
```gherkin
Given {Story} has no {AcceptanceCriteria} defined
When {DrawIOStoryMap} renders exploration from {StoryMap}
Then {DrawIOStoryMap} renders {DrawIOStory} without {DrawIOElement} AC boxes
```


<a id="scenario-render-acceptance-criteria-boxes-below-stories-in-exploration-diagram"></a>
### Scenario: [Render acceptance criteria boxes below stories in exploration diagram](#scenario-render-acceptance-criteria-boxes-below-stories-in-exploration-diagram) (happy_path)

**Steps:**
```gherkin
Given no {LayoutData} exists for this diagram
When {DrawIOStoryMap} renders exploration from {StoryMap}
Then {DrawIOStoryMap} contains {DrawIOEpic} spanning {DrawIOSubEpic} spanning {DrawIOStory}
And {DrawIOElement} AC boxes are rendered below each {DrawIOStory}
And AC text is formatted as When/Then in {DrawIOElement} boxes
And actor labels are positioned above {DrawIOStory}
```


<a id="scenario-ac-boxes-styled-with-correct-fill-stroke-and-positioned-below-story"></a>
### Scenario: [AC boxes styled with correct fill stroke and positioned below story](#scenario-ac-boxes-styled-with-correct-fill-stroke-and-positioned-below-story) (happy_path)

**Steps:**
```gherkin
Given no {LayoutData} exists for this diagram
When {DrawIOStoryMap} renders exploration from {StoryMap}
Then {DrawIOElement} AC boxes are wider than {DrawIOStory} cell
And {DrawIOElement} uses {DrawIOElement.fill} of #fff2cc and {DrawIOElement.stroke} of #d6b656
And {DrawIOElement} has left-aligned 8px text
```

**DrawIOElement (AC box styling):**

| fill | stroke | text_align | font_size |
| --- | --- | --- | --- |
| #fff2cc | #d6b656 | left | 8 |


<a id="scenario-rendered-output-contains-story-and-ac-cells-with-correct-containment"></a>
### Scenario: [Rendered output contains story and AC cells with correct containment](#scenario-rendered-output-contains-story-and-ac-cells-with-correct-containment) (happy_path)

**Steps:**
```gherkin
Given no {LayoutData} exists for this diagram
When {DrawIOStoryMap} renders exploration from {StoryMap}
Then output {DrawIOStoryMap} contains both {DrawIOStory} cells and {DrawIOElement} AC cells
And {DrawIOElement} AC cells are contained within their parent {DrawIOStory} sub-tree in DrawIO XML
```

