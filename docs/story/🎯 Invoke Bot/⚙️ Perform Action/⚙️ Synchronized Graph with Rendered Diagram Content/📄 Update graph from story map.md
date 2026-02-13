# 📄 Update graph from story map

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L667)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Synchronized Graph with Rendered Diagram Content](.)  
**Sequential Order:** 4.0
**Story Type:** user

## Story Description

Update graph from story map functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-extract-outline-assigns-stories-to-sub-epics-by-containment-and-sequential-order"></a>
### Scenario: [Extract outline assigns stories to sub-epics by containment and sequential order](#scenario-extract-outline-assigns-stories-to-sub-epics-by-containment-and-sequential-order) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L669)

**Steps:**
```gherkin
Given {DrawIOStoryMap} outline file contains {DrawIOEpic} and {DrawIOSubEpic} and {DrawIOStory} cells
When {DrawIOStoryMap} extracts outline from {DrawIOStoryMap}
Then {DrawIOStoryMap} assigns each {DrawIOStory} to a {DrawIOSubEpic} by containment (story center inside sub-epic box)
And each {DrawIOSubEpic} has one story group with all its {DrawIOStory} nodes
And {DrawIOStoryMap} assigns {DrawIOStoryNode.sequential_order} from top-to-bottom then left-to-right
And extracted JSON is written to file
```


<a id="scenario-updatereport-lists-exact-fuzzy-new-and-removed-stories"></a>
### Scenario: [UpdateReport lists exact fuzzy new and removed stories](#scenario-updatereport-lists-exact-fuzzy-new-and-removed-stories) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L685)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has been extracted from diagram
And original {StoryMap} exists
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs
Then {UpdateReport} lists exact matches where {DrawIOStoryNode} name equals {StoryMap} node name
And {UpdateReport} lists fuzzy matches where names differ but match with confidence
And {UpdateReport} lists new stories present in {DrawIOStoryMap} but not in {StoryMap}
And {UpdateReport} lists removed stories present in {StoryMap} but not in {DrawIOStoryMap}
```


<a id="scenario-storymap-updated-from-outline-diagram-applies-report-changes"></a>
### Scenario: [StoryMap updated from outline diagram applies report changes](#scenario-storymap-updated-from-outline-diagram-applies-report-changes) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L699)

**Steps:**
```gherkin
Given {UpdateReport} has been generated from {DrawIOStoryMap} vs {StoryMap}
When {StoryMap}.update({DrawIOStoryMap}, {UpdateReport}) runs
Then {StoryMap} applies exact match updates from {UpdateReport}
And {StoryMap} applies fuzzy match renames from {UpdateReport}
And new stories added to {StoryMap}
And removed stories flagged in {StoryMap}
```


<a id="scenario-renamed-or-reordered-nodes-flagged-as-fuzzy-matches-in-updatereport"></a>
### Scenario: [Renamed or reordered nodes flagged as fuzzy matches in UpdateReport](#scenario-renamed-or-reordered-nodes-flagged-as-fuzzy-matches-in-updatereport) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L711)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has a {DrawIOStoryNode} with name changed from original
And {StoryMap} has the original {DrawIOStoryNode} name
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs
Then {UpdateReport} flags the renamed node as a fuzzy match
And {UpdateReport} records both old and new name
```


<a id="scenario-deleted-nodes-listed-as-removed-and-large-deletions-flagged"></a>
### Scenario: [Deleted nodes listed as removed and large deletions flagged](#scenario-deleted-nodes-listed-as-removed-and-large-deletions-flagged) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L726)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has nodes removed by user
And {StoryMap} has the original nodes
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs
Then {UpdateReport} lists deleted nodes as removed
And {UpdateReport}.large_deletions flags entire missing {DrawIOEpic} or {DrawIOSubEpic}
```


<a id="scenario-sync-persists-layoutdata-alongside-diagram"></a>
### Scenario: [Sync persists LayoutData alongside diagram](#scenario-sync-persists-layoutdata-alongside-diagram) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L737)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has been extracted from diagram
When sync completes
Then {LayoutData} persisted to JSON file alongside the diagram
And {LayoutData} stores position and size for each {DrawIOEpic} and {DrawIOSubEpic} and {DrawIOStory}
And {LayoutData} available for next render
```


<a id="scenario-moved-story-gets-recomputed-sequential-order-from-new-position"></a>
### Scenario: [Moved story gets recomputed sequential order from new position](#scenario-moved-story-gets-recomputed-sequential-order-from-new-position) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L750)

**Steps:**
```gherkin
Given {DrawIOStory} has been moved to a new position in {DrawIOStoryMap}
When {DrawIOStoryMap} extracts from {DrawIOStoryMap}
Then {DrawIOStoryMap} recomputes {DrawIOStoryNode.sequential_order} from left-to-right and vertical position
And {UpdateReport} matches the moved {DrawIOStory} to original
And merged output updates the matched {DrawIOStory} with new order
```


<a id="scenario-single-story-deleted-keeps-original-structure-and-flags-if-many-missing"></a>
### Scenario: [Single story deleted keeps original structure and flags if many missing](#scenario-single-story-deleted-keeps-original-structure-and-flags-if-many-missing) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L761)

**Steps:**
```gherkin
Given one {DrawIOStory} cell has been removed from {DrawIOStoryMap}
When {DrawIOStoryMap} extracts from {DrawIOStoryMap}
Then extracted graph omits that {DrawIOStory}
And {UpdateReport} lists it as removed
And merged output keeps original {StoryMap} structure with only matched stories updated
And if many {DrawIOStory} from one {DrawIOEpic} are missing the {UpdateReport} flags that {DrawIOEpic}
```


<a id="scenario-deleted-sub-epic-reassigns-its-stories-by-position"></a>
### Scenario: [Deleted sub-epic reassigns its stories by position](#scenario-deleted-sub-epic-reassigns-its-stories-by-position) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L773)

**Steps:**
```gherkin
Given a {DrawIOSubEpic} box has been removed from {DrawIOStoryMap}
When {DrawIOStoryMap} extracts from {DrawIOStoryMap}
Then extracted graph omits that {DrawIOSubEpic}
And {DrawIOStory} nodes under it are reassigned by where they sit (inside another {DrawIOSubEpic} box or at {DrawIOEpic} level)
And {UpdateReport} flags the missing {DrawIOSubEpic} in large_deletions
```


<a id="scenario-deleted-epic-removes-all-children-and-flags-large-deletions"></a>
### Scenario: [Deleted epic removes all children and flags large deletions](#scenario-deleted-epic-removes-all-children-and-flags-large-deletions) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L784)

**Steps:**
```gherkin
Given a {DrawIOEpic} box has been removed from {DrawIOStoryMap}
When {DrawIOStoryMap} extracts from {DrawIOStoryMap}
Then extracted graph omits that {DrawIOEpic} and all its {DrawIOSubEpic} and {DrawIOStory}
And {UpdateReport} lists those stories as removed
And {UpdateReport}.large_deletions includes missing_epics
```


<a id="scenario-extract-from-empty-or-malformed-drawio-file-produces-error"></a>
### Scenario: [Extract from empty or malformed DrawIO file produces error](#scenario-extract-from-empty-or-malformed-drawio-file-produces-error) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L795)

**Steps:**
```gherkin
Given {DrawIOStoryMap} file contains no valid {DrawIOEpic} or {DrawIOSubEpic} cells
When {DrawIOStoryMap} extracts outline from {DrawIOStoryMap}
Then {DrawIOStoryMap} reports extraction error with zero nodes found
And no extracted JSON is written
```

