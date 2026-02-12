# 📄 Render story map

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L22)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Synchronized Graph with Rendered Diagram Content](.)  
**Sequential Order:** 1
**Story Type:** user

## Story Description

Render story map functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-render-outline-diagram-from-storymap-with-default-layout"></a>
### Scenario: [Render outline diagram from StoryMap with default layout](#scenario-render-outline-diagram-from-storymap-with-default-layout) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L24)

**Steps:**
```gherkin
Given {StoryMap} has {StoryMap.epics} with {DrawIOStoryNode.sequential_order} and nested {DrawIOSubEpic} and {DrawIOStory} nodes
And no {LayoutData} exists for this diagram
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOStoryMap} positions {DrawIOEpic} at top at fixed Y
And {DrawIOEpic} width equals combined width of its {DrawIOSubEpic} children
And {DrawIOSubEpic} positioned below {DrawIOEpic}
And {DrawIOSubEpic} width equals combined width of its {DrawIOStory} children
And {DrawIOStory} cells arranged left-to-right by {DrawIOStoryNode.sequential_order} with spacing
And actor labels positioned above {DrawIOStory} cells
And output is valid DrawIO XML written to {DrawIOStoryMap} file path
```


<a id="scenario-render-outline-diagram-from-storymap-with-saved-layoutdata"></a>
### Scenario: [Render outline diagram from StoryMap with saved LayoutData](#scenario-render-outline-diagram-from-storymap-with-saved-layoutdata) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L49)

**Steps:**
```gherkin
Given {StoryMap} has {StoryMap.epics} with {DrawIOEpic} and {DrawIOSubEpic} and {DrawIOStory} nodes
And {LayoutData} exists with saved positions for each {DrawIOStoryNode}
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOStoryMap} applies {LayoutData} saved positions for {DrawIOEpic} and {DrawIOSubEpic}
And {DrawIOStory} positions derived from {DrawIOStoryNode.sequential_order} left-to-right
And new {DrawIOStory} that would overlap existing nodes positioned below for manual placement
And other new {DrawIOStoryNode} get default spacing
```


<a id="scenario-storymap"></a>
### Scenario: [StoryMap](#scenario-storymap) (outline)  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L68)

**Steps:**
```gherkin
Given {StoryMap} has {StoryMap.epics} E epics and S {DrawIOSubEpic} and N {DrawIOStory}
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOStoryMap} contains exactly E {DrawIOEpic} cells and S {DrawIOSubEpic} cells and N {DrawIOStory} cells
And summary reports epics E and sub_epic_count S and diagram_generated true
```

**StoryMap (Get epics / sub-epics / stories):**

| StoryMap.epic_count | StoryMap.sub_epic_count | StoryMap.story_count |
| --- | --- | --- |
| 1 | 3 | 7 |
| 2 | 5 | 12 |


<a id="scenario-sub-epics-and-stories-ordered-by-sequential_order"></a>
### Scenario: [Sub-epics and stories ordered by sequential_order](#scenario-sub-epics-and-stories-ordered-by-sequential_order) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L80)

**Steps:**
```gherkin
Given {StoryMap} has {DrawIOSubEpic} with {DrawIOStoryNode.sequential_order} values
And each {DrawIOSubEpic} has {DrawIOStory} with {DrawIOStoryNode.sequential_order} values
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOSubEpic} cells ordered left-to-right by {DrawIOStoryNode.sequential_order}
And {DrawIOStory} cells within each {DrawIOSubEpic} ordered left-to-right by {DrawIOStoryNode.sequential_order}
```


<a id="scenario-drawiostory"></a>
### Scenario: [DrawIOStory](#scenario-drawiostory) (outline)  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L99)

**Steps:**
```gherkin
Given {StoryMap} has a {DrawIOStory} with {DrawIOStory.story_type}
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOStory} cell has fill {DrawIOElement.fill} and stroke {DrawIOElement.stroke} and font color {DrawIOElement.font_color}
```

**DrawIOStory (Get story type (user/system/technical) from style):**

| DrawIOStory.story_type | DrawIOElement.fill | DrawIOElement.stroke | DrawIOElement.font_color |
| --- | --- | --- | --- |
| user | #fff2cc | #d6b656 | black |
| (none) | #fff2cc | #d6b656 | black |
| system | #1a237e | #0d47a1 | white |
| technical | #000000 | #333333 | white |


<a id="scenario-drawioelement"></a>
### Scenario: [DrawIOElement](#scenario-drawioelement) (outline)  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L115)

**Steps:**
```gherkin
Given {StoryMap} has a {DrawIOStoryNode} of type {DrawIOStoryNode.node_type}
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOElement} cell has shape {DrawIOElement.shape} and fill {DrawIOElement.fill} and stroke {DrawIOElement.stroke} and font color {DrawIOElement.font_color}
```

**DrawIOElement (Cell style (fill, stroke, text)):**

| DrawIOStoryNode.node_type | DrawIOElement.shape | DrawIOElement.fill | DrawIOElement.stroke | DrawIOElement.font_color |
| --- | --- | --- | --- | --- |
| epic | rounded | #e1d5e7 | #9673a6 | black |
| sub_epic | rounded | #d5e8d4 | #82b366 | black |
| actor | fixed-aspect | #dae8fc | #6c8ebf | black (8px) |


<a id="scenario-render-completes-and-writes-drawio-file-to-specified-path"></a>
### Scenario: [Render completes and writes DrawIO file to specified path](#scenario-render-completes-and-writes-drawio-file-to-specified-path) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L129)

**Steps:**
```gherkin
Given {StoryMap} has been loaded from story graph
And output file path is specified for {DrawIOStoryMap}
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOStoryMap} is written to the specified file path
And summary reports epics count and sub_epic_count and diagram_generated
```


<a id="scenario-render-outline-from-empty-storymap-produces-empty-diagram"></a>
### Scenario: [Render outline from empty StoryMap produces empty diagram](#scenario-render-outline-from-empty-storymap-produces-empty-diagram) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L143)

**Steps:**
```gherkin
Given {StoryMap} has no {StoryMap.epics}
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOStoryMap} contains zero {DrawIOEpic} cells
And summary reports epics 0 and sub_epic_count 0 and diagram_generated true
```

