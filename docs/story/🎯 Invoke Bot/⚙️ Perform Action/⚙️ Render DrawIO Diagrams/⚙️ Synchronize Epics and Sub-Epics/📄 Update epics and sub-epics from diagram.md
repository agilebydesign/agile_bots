# 📄 Update epics and sub-epics from diagram

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/synchronize_graph_with_rendered_diagram/test_synchronize_epics_and_sub_epics.py#L373)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Render DrawIO Diagrams](..) / [⚙️ Synchronize Epics and Sub-Epics](.)  
**Sequential Order:** 3.0
**Story Type:** user

## Story Description

Update epics and sub-epics from diagram functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-apply-epic-and-sub-epic-changes-from-report-updates-story-graph"></a>
### Scenario: [Apply epic and sub-epic changes from report updates story graph](#scenario-apply-epic-and-sub-epic-changes-from-report-updates-story-graph) (happy_path)

**Steps:**
```gherkin
Given {UpdateReport} has sub-epic changes
When {UpdateReport} is applied to {StoryMap}
Then {StoryMap} reflects the sub-epic additions and removals from {UpdateReport}
```

**UpdateReport (new sub-epics):**

| name | parent |
| --- | --- |
| Supply Chain Analytics | Order Fulfillment |


**UpdateReport (removed sub-epics):**

| name | parent |
| --- | --- |
| Freight Routing | Order Fulfillment |


<a id="scenario-removed-sub-epic-reassigns-its-stories-by-position"></a>
### Scenario: [Removed sub-epic reassigns its stories by position](#scenario-removed-sub-epic-reassigns-its-stories-by-position) (happy_path)

**Steps:**
```gherkin
Given {DrawIOSubEpic} has been removed from {DrawIOStoryMap}
When {DrawIOStoryMap} extracts outline from diagram
Then extracted graph omits that {DrawIOSubEpic}
And {DrawIOStory} under it are reassigned by position (inside another {DrawIOSubEpic} or at {DrawIOEpic} level)
And {UpdateReport.large_deletions} flags the missing {DrawIOSubEpic}
```

**DrawIOSubEpic (removed from diagram):**

| name | parent | present_in_diagram |
| --- | --- | --- |
| Freight Routing | Order Fulfillment | false |


**DrawIOStory (orphaned by removal):**

| name | original_parent | reassigned_to |
| --- | --- | --- |
| Select Carrier | Freight Routing | Warehouse Management |
| Calculate Shipping | Freight Routing | Warehouse Management |


**UpdateReport (large deletions):**

| deletion_type | name |
| --- | --- |
| missing_sub_epics | Freight Routing |


<a id="scenario-removed-epic-removes-all-children-from-story-graph"></a>
### Scenario: [Removed epic removes all children from story graph](#scenario-removed-epic-removes-all-children-from-story-graph) (edge_case)

**Steps:**
```gherkin
Given {DrawIOEpic} has been removed from {DrawIOStoryMap}
When {DrawIOStoryMap} extracts outline from diagram
Then extracted graph omits that {DrawIOEpic} and all its {DrawIOSubEpic} and {DrawIOStory}
And {UpdateReport} lists those as removed
And {UpdateReport.large_deletions} includes missing_epics
```

**DrawIOEpic (removed from diagram):**

| name | present_in_diagram |
| --- | --- |
| Order Fulfillment | false |


**UpdateReport (large deletions):**

| deletion_type | name |
| --- | --- |
| missing_epics | Order Fulfillment |


<a id="scenario-renamed-sub-epic-in-diagram-updates-name-in-story-graph"></a>
### Scenario: [Renamed sub-epic in diagram updates name in story graph](#scenario-renamed-sub-epic-in-diagram-updates-name-in-story-graph) (happy_path)

**Steps:**
```gherkin
Given {DrawIOSubEpic} in {DrawIOStoryMap} has different name than in {StoryMap}
When {UpdateReport} is applied to {StoryMap}
Then {StoryMap} updates the sub-epic name to match {DrawIOSubEpic}
```

**DrawIOSubEpic (renamed in diagram):**

| original_name | new_name | parent |
| --- | --- | --- |
| Warehouse Management | Inventory Management | Order Fulfillment |


<a id="scenario-new-sub-epic-in-diagram-creates-it-in-story-graph"></a>
### Scenario: [New sub-epic in diagram creates it in story graph](#scenario-new-sub-epic-in-diagram-creates-it-in-story-graph) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has {DrawIOSubEpic} not present in {StoryMap}
When {UpdateReport} is applied to {StoryMap}
Then {StoryMap} creates the new {DrawIOSubEpic}
```

**DrawIOSubEpic (new in diagram):**

| name | parent |
| --- | --- |
| Last-Mile Delivery | Order Fulfillment |


<a id="scenario-end-to-end-render-then-report-then-update-for-epic-hierarchy"></a>
### Scenario: [End-to-end render then report then update for epic hierarchy](#scenario-end-to-end-render-then-report-then-update-for-epic-hierarchy) (happy_path)

**Steps:**
```gherkin
Given {StoryMap} has {DrawIOSubEpic}
When {DrawIOStoryMap} renders from {StoryMap}
And user modifies {DrawIOSubEpic} in diagram
And {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
And {UpdateReport} is applied to {StoryMap}
Then {StoryMap} reflects all sub-epic changes from diagram
```

**DrawIOSubEpic (after user modifications):**

| name | parent | change |
| --- | --- | --- |
| Warehouse Management | Order Fulfillment | unchanged |
| Supply Chain Analytics | Order Fulfillment | added |


<a id="scenario-extract-assigns-entities-to-parent-sub-epics-by-containment-and-sequential-order"></a>
### Scenario: [Extract assigns entities to parent sub-epics by containment and sequential order](#scenario-extract-assigns-entities-to-parent-sub-epics-by-containment-and-sequential-order) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} outline file contains {DrawIOEpic} and {DrawIOSubEpic} and {DrawIOStory} cells
When {DrawIOStoryMap} extracts outline from diagram
Then {DrawIOStoryMap} assigns each {DrawIOStory} to a {DrawIOSubEpic} by containment
And each {DrawIOSubEpic} has one story group with all its {DrawIOStory}
And {DrawIOStory.sequential_order} is assigned from top-to-bottom then left-to-right
And extracted JSON is written to file
```

**DrawIOStory (with assigned containment and order):**

| name | parent | sequential_order |
| --- | --- | --- |
| Receive Inventory | Warehouse Management | 1 |
| Pick Pack Ship | Warehouse Management | 2 |
| Select Carrier | Freight Routing | 1 |
| Calculate Shipping | Freight Routing | 2 |


<a id="scenario-sync-persists-layout-data-alongside-diagram"></a>
### Scenario: [Sync persists layout data alongside diagram](#scenario-sync-persists-layout-data-alongside-diagram) (happy_path)  | [Test](/test/invoke_bot/perform_action/synchronize_graph_with_rendered_diagram/test_synchronize_epics_and_sub_epics.py#L462)

**Steps:**
```gherkin
Given {DrawIOStoryMap} exists with content extracted from diagram
When sync completes
Then {LayoutData} is persisted to JSON file alongside the diagram
And {LayoutData} stores position and size for each {DrawIOEpic} and {DrawIOSubEpic} and {DrawIOStory}
And {LayoutData} is available for next render
```

**LayoutData (persisted positions):**

| entity_type | name | x | y | width | height |
| --- | --- | --- | --- | --- | --- |
| DrawIOEpic | Order Fulfillment | 10 | 100 | 600 | 80 |
| DrawIOSubEpic | Warehouse Management | 20 | 180 | 280 | 120 |
| DrawIOSubEpic | Freight Routing | 310 | 180 | 280 | 120 |
| DrawIOStory | Receive Inventory | 30 | 220 | 120 | 40 |
| DrawIOStory | Pick Pack Ship | 160 | 220 | 120 | 40 |


<a id="scenario-extract-from-empty-or-malformed-drawio-file-produces-error"></a>
### Scenario: [Extract from empty or malformed drawio file produces error](#scenario-extract-from-empty-or-malformed-drawio-file-produces-error) (error_case)

**Steps:**
```gherkin
Given {DrawIOStoryMap} file contains no valid {DrawIOEpic} or {DrawIOSubEpic} cells
When {DrawIOStoryMap} extracts outline from diagram
Then {DrawIOStoryMap} reports extraction error with zero nodes found
And no extracted JSON is written
```

**DrawIOStoryMap (empty/malformed):**

| diagram_type | output_file | nodes_found |
| --- | --- | --- |
| outline | empty-map.drawio | 0 |

