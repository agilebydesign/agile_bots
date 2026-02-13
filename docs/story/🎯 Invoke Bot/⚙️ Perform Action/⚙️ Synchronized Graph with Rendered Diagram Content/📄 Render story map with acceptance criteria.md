# 📄 Render story map with acceptance criteria

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L605)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Synchronized Graph with Rendered Diagram Content](.)  
**Sequential Order:** 3.0
**Story Type:** user

## Story Description

Render story map with acceptance criteria functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Background

**Common setup steps shared across all scenarios:**

```gherkin
Given {StoryMap} has {DrawIOStory} with acceptance_criteria
```

## Scenarios

<a id="scenario-render-exploration-diagram-with-ac-boxes-below-stories"></a>
### Scenario: [Render exploration diagram with AC boxes below stories](#scenario-render-exploration-diagram-with-ac-boxes-below-stories) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L607)

**Steps:**
```gherkin
When {DrawIOStoryMap} renders exploration from {StoryMap}
Then {DrawIOStoryMap} contains {DrawIOEpic} spanning {DrawIOSubEpic} spanning {DrawIOStory} with same layout as outline
And {DrawIOStory} cells styled per story_type as in outline
And acceptance criteria {DrawIOElement} boxes rendered below each {DrawIOStory}
And AC text formatted as When/Then in boxes
And actor labels positioned above {DrawIOStory} as in outline
```


<a id="scenario-ac-boxes-styled-and-positioned-below-story-with-extracted-step-text"></a>
### Scenario: [AC boxes styled and positioned below story with extracted step text](#scenario-ac-boxes-styled-and-positioned-below-story-with-extracted-step-text) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L618)

**Steps:**
```gherkin
When {DrawIOStoryMap} renders exploration from {StoryMap}
Then AC {DrawIOElement} boxes created wider than {DrawIOStory} cell
And AC boxes use rectangular shape with fill #fff2cc and stroke #d6b656 and left-aligned 8px text
And step text extracted from each acceptance_criteria entry
```


<a id="scenario-re-render-exploration-with-layoutdata-preserves-story-and-ac-box-positions"></a>
### Scenario: [Re-render exploration with LayoutData preserves story and AC box positions](#scenario-re-render-exploration-with-layoutdata-preserves-story-and-ac-box-positions) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L628)

**Steps:**
```gherkin
And {LayoutData} exists with saved positions for {DrawIOStory} and AC boxes
When {DrawIOStoryMap} renders exploration from {StoryMap}
Then {DrawIOStoryMap} applies {LayoutData} saved positions for {DrawIOStory} and AC {DrawIOElement} boxes
```


<a id="scenario-exploration-render-output-contains-story-and-ac-cells-with-correct-containment"></a>
### Scenario: [Exploration render output contains story and AC cells with correct containment](#scenario-exploration-render-output-contains-story-and-ac-cells-with-correct-containment) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L641)

**Steps:**
```gherkin
When {DrawIOStoryMap} renders exploration from {StoryMap}
Then output {DrawIOStoryMap} contains both {DrawIOStory} cells and AC {DrawIOElement} cells
And AC cells are contained within their parent {DrawIOStory} sub-tree in DrawIO XML
```


<a id="scenario-story-with-no-acceptance-criteria-renders-without-ac-boxes"></a>
### Scenario: [Story with no acceptance criteria renders without AC boxes](#scenario-story-with-no-acceptance-criteria-renders-without-ac-boxes) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L655)

**Steps:**
```gherkin
And {StoryMap} also has a {DrawIOStory} with no acceptance_criteria
When {DrawIOStoryMap} renders exploration from {StoryMap}
Then {DrawIOStory} without acceptance_criteria has no AC {DrawIOElement} boxes below it
And {DrawIOStory} with acceptance_criteria still has AC boxes rendered
```

