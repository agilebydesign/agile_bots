# 📄 Update story graph from map acceptance criteria

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L820)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Synchronized Graph with Rendered Diagram Content](.)  
**Sequential Order:** 6.0
**Story Type:** user

## Story Description

Update story graph from map acceptance criteria functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Background

**Common setup steps shared across all scenarios:**

```gherkin
Given {DrawIOStoryMap} exploration file exists with {DrawIOStory} cells and AC {DrawIOElement} boxes
```

## Scenarios

<a id="scenario-extract-exploration-maps-ac-boxes-to-stories-by-position-and-containment"></a>
### Scenario: [Extract exploration maps AC boxes to stories by position and containment](#scenario-extract-exploration-maps-ac-boxes-to-stories-by-position-and-containment) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L822)

**Steps:**
```gherkin
When {DrawIOStoryMap} extracts exploration from {DrawIOStoryMap}
Then {DrawIOStoryMap} assigns AC cells to {DrawIOStory} by vertical position and containment below story cells
And AC text mapped back to story acceptance_criteria or steps
```


<a id="scenario-whenthen-ac-text-extracted-as-step-descriptions"></a>
### Scenario: [When/Then AC text extracted as step descriptions](#scenario-whenthen-ac-text-extracted-as-step-descriptions) ()

**Steps:**
```gherkin
And AC {DrawIOElement} box has When/Then format text
When {DrawIOStoryMap} extracts exploration from {DrawIOStoryMap}
Then {DrawIOStoryMap} extracts step description from AC box text
And associates extracted step with the containing {DrawIOStory}
```


<a id="scenario-merge-preserves-original-ac-for-matched-stories-from-exploration-view"></a>
### Scenario: [Merge preserves original AC for matched stories from exploration view](#scenario-merge-preserves-original-ac-for-matched-stories-from-exploration-view) ()

**Steps:**
```gherkin
And {UpdateReport} has been generated from {DrawIOStoryMap} exploration vs {StoryMap}
When {StoryMap}.update({DrawIOStoryMap}, {UpdateReport}) runs for exploration view
Then {StoryMap} applies report changes for matched stories
And {StoryMap} preserves original acceptance_criteria and steps for matched stories
And extracted AC does not overwrite original AC in {StoryMap}
```


<a id="scenario-added-or-removed-ac-boxes-reflected-in-extracted-graph-and-updatereport"></a>
### Scenario: [Added or removed AC boxes reflected in extracted graph and UpdateReport](#scenario-added-or-removed-ac-boxes-reflected-in-extracted-graph-and-updatereport) ()

**Steps:**
```gherkin
And new AC {DrawIOElement} boxes exist below a {DrawIOStory} in {DrawIOStoryMap}
And existing AC boxes have been removed from another {DrawIOStory}
When {DrawIOStoryMap} extracts exploration from {DrawIOStoryMap}
Then extracted graph reflects new AC for the first {DrawIOStory}
And extracted graph omits removed AC for the second {DrawIOStory}
And {UpdateReport} reflects these structural changes
```


<a id="scenario-ac-cells-assigned-to-stories-by-vertical-position-below-story-cells"></a>
### Scenario: [AC cells assigned to stories by vertical position below story cells](#scenario-ac-cells-assigned-to-stories-by-vertical-position-below-story-cells) ()

**Steps:**
```gherkin
And multiple {DrawIOStory} cells have AC {DrawIOElement} boxes positioned below them
When {DrawIOStoryMap} extracts exploration from {DrawIOStoryMap}
Then each AC {DrawIOElement} assigned to the {DrawIOStory} it is contained below based on vertical position
And no AC box left unassigned when positioned within a {DrawIOStory} column
```


<a id="scenario-ac-box-text-not-in-whenthen-format-treated-as-plain-acceptance_criteria"></a>
### Scenario: [AC box text not in When/Then format treated as plain acceptance_criteria](#scenario-ac-box-text-not-in-whenthen-format-treated-as-plain-acceptance_criteria) ()

**Steps:**
```gherkin
And AC {DrawIOElement} box has text that is not in When/Then format
When {DrawIOStoryMap} extracts exploration from {DrawIOStoryMap}
Then {DrawIOStoryMap} treats AC text as plain acceptance_criteria description
And associates it with the containing {DrawIOStory} without step extraction
```

