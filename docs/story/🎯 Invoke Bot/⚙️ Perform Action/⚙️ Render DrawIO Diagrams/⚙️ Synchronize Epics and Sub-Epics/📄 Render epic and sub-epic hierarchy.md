# 📄 Render epic and sub-epic hierarchy

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/synchronize_graph_with_rendered_diagram/test_synchronize_epics_and_sub_epics.py#L156)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Render DrawIO Diagrams](..) / [⚙️ Synchronize Epics and Sub-Epics](.)  
**Sequential Order:** 1.0
**Story Type:** user

## Story Description

Render epic and sub-epic hierarchy functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-render-epic-and-sub-epic-hierarchy-with-default-layout-positions-epics-at-fixed-y-and-sub-epics-below"></a>
### Scenario: [Render epic and sub-epic hierarchy with default layout positions epics at fixed Y and sub-epics below](#scenario-render-epic-and-sub-epic-hierarchy-with-default-layout-positions-epics-at-fixed-y-and-sub-epics-below) (happy_path)

**Steps:**
```gherkin
Given no {LayoutData} exists for this diagram
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOStoryMap} contains {DrawIOEpic}
And {DrawIOEpic} contains {DrawIOSubEpic}
And each {DrawIOSubEpic} contains its {DrawIOStory}
And {DrawIOStoryMap.output} is valid DrawIO XML
```

**DrawIOStoryMap (render output):**

| output | is_valid_xml |
| --- | --- |
| story-map-outline.drawio | true |


<a id="scenario-parent-epic-spans-all-child-sub-epics-horizontally"></a>
### Scenario: [Parent epic spans all child sub-epics horizontally](#scenario-parent-epic-spans-all-child-sub-epics-horizontally) (happy_path)

**Steps:**
```gherkin
Given {DrawIOSubEpic} is rendered with {DrawIOSubEpic.x} and {DrawIOSubEpic.width}
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOEpic.x} is at or before the leftmost {DrawIOSubEpic.x}
And {DrawIOEpic.width} encompasses all {DrawIOSubEpic}
```

**DrawIOEpic (expected span):**

| name | expected_x | expected_min_width |
| --- | --- | --- |
| Payment Processing | 10 | 640 |


**DrawIOSubEpic (rendered positions):**

| name | x | width |
| --- | --- | --- |
| Authorize Payment | 10 | 200 |
| Settle Transaction | 220 | 200 |
| Issue Refund | 430 | 200 |


<a id="scenario-sibling-sub-epics-do-not-overlap-horizontally"></a>
### Scenario: [Sibling sub-epics do not overlap horizontally](#scenario-sibling-sub-epics-do-not-overlap-horizontally) (edge_case)

**Steps:**
```gherkin
Given {DrawIOSubEpic} is rendered with {DrawIOSubEpic.x} and {DrawIOSubEpic.width}
When {DrawIOStoryMap} renders outline from {StoryMap}
Then for each adjacent pair of {DrawIOSubEpic}: left x + width <= right x
```

**DrawIOSubEpic (rendered positions):**

| name | x | width |
| --- | --- | --- |
| Authorize Payment | 10 | 200 |
| Settle Transaction | 220 | 200 |
| Issue Refund | 430 | 200 |


<a id="scenario-re-render-with-saved-layout-data-preserves-epic-and-sub-epic-positions"></a>
### Scenario: [Re-render with saved layout data preserves epic and sub-epic positions](#scenario-re-render-with-saved-layout-data-preserves-epic-and-sub-epic-positions) (happy_path)

**Steps:**
```gherkin
Given {LayoutData} exists with saved positions for {DrawIOSubEpic}
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOSubEpic} is rendered at {LayoutData.saved_x} {LayoutData.saved_y} with {LayoutData.saved_w}
```

**LayoutData (saved positions for DrawIOSubEpic):**

| sub_epic_name | saved_x | saved_y | saved_w |
| --- | --- | --- | --- |
| Authorize Payment | 50 | 200 | 250 |
| Settle Transaction | 310 | 200 | 250 |
| Issue Refund | 570 | 200 | 250 |


<a id="scenario-render-completes-and-writes-valid-drawio-file-for-epic-hierarchy"></a>
### Scenario: [Render completes and writes valid DrawIO file for epic hierarchy](#scenario-render-completes-and-writes-valid-drawio-file-for-epic-hierarchy) (happy_path)

**Steps:**
```gherkin
Given no {LayoutData} exists for this diagram
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOStoryMap} is written to {DrawIOStoryMap.output_file}
And {DrawIOStoryMap.output} is valid DrawIO XML
And {DrawIOStoryMap.summary} reports correct counts
```

**DrawIOStoryMap (render output):**

| output_file |
| --- |
| story-map-outline.drawio |


<a id="scenario-nested-sub-epics-render-recursively-to-4-levels-of-depth"></a>
### Scenario: [Nested sub-epics render recursively to 4 levels of depth](#scenario-nested-sub-epics-render-recursively-to-4-levels-of-depth) (edge_case)

**Steps:**
```gherkin
Given {StoryMap} has {DrawIOSubEpic} nested 4 levels deep
And each {DrawIOSubEpic} has a parent {DrawIOSubEpic}
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOStoryMap} contains all {DrawIOSubEpic} at every depth
And each {DrawIOSubEpic} is rendered inside its parent
```

**DrawIOEpic:**

| name |
| --- |
| Wire Transfers |


**DrawIOSubEpic (nested hierarchy):**

| name | parent | depth |
| --- | --- | --- |
| Domestic Wires | Wire Transfers | 1 |
| Same-Day Settlement | Domestic Wires | 2 |
| Fedwire Submission | Same-Day Settlement | 3 |
| Fed Confirmation | Fedwire Submission | 4 |


<a id="scenario-both-parent-and-leaf-sub-epics-rendered-in-hierarchy"></a>
### Scenario: [Both parent and leaf sub-epics rendered in hierarchy](#scenario-both-parent-and-leaf-sub-epics-rendered-in-hierarchy) (happy_path)

**Steps:**
```gherkin
Given {StoryMap} has {DrawIOSubEpic} with {DrawIOSubEpic.role} of parent and leaf
And leaf {DrawIOSubEpic} contain {DrawIOStory}
When {DrawIOStoryMap} renders outline from {StoryMap}
Then parent {DrawIOSubEpic} is rendered as a container
And leaf {DrawIOSubEpic} is rendered with its {DrawIOStory} inside
```

**DrawIOEpic:**

| name |
| --- |
| Pharmacy |


**DrawIOSubEpic (hierarchy with roles):**

| name | parent | role |
| --- | --- | --- |
| Prescription Management | Pharmacy | parent |
| Verify Prescription | Prescription Management | parent |
| Dispense Medication | Verify Prescription | leaf |
| Check Interactions | Verify Prescription | leaf |


**DrawIOStory (children of leaf DrawIOSubEpic):**

| name | parent | story_type |
| --- | --- | --- |
| Check Dosage | Dispense Medication | user |
| Print Label | Dispense Medication | system |
| Log Dispensed | Dispense Medication | system |
| Lookup Drug DB | Check Interactions | user |
| Flag Conflict | Check Interactions | system |


<a id="scenario-nested-sub-epic-y-positions-increase-with-each-depth-level"></a>
### Scenario: [Nested sub-epic Y positions increase with each depth level](#scenario-nested-sub-epic-y-positions-increase-with-each-depth-level) (happy_path)

**Steps:**
```gherkin
Given {StoryMap} has {DrawIOSubEpic} nested multiple levels deep
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOSubEpic.expected_y} increases with each {DrawIOSubEpic.depth}
And deeper {DrawIOSubEpic} has larger Y than shallower
```

**DrawIOEpic:**

| name |
| --- |
| Wire Transfers |


**DrawIOSubEpic (expected Y by depth):**

| name | parent | depth | expected_y |
| --- | --- | --- | --- |
| Domestic Wires | Wire Transfers | 1 | 180 |
| Same-Day Settlement | Domestic Wires | 2 | 240 |
| Fedwire Submission | Same-Day Settlement | 3 | 300 |


<a id="scenario-single-level-sub-epic-renders-at-standard-y-position"></a>
### Scenario: [Single-level sub-epic renders at standard Y position](#scenario-single-level-sub-epic-renders-at-standard-y-position) (happy_path)

**Steps:**
```gherkin
Given {StoryMap} has {DrawIOEpic} with {DrawIOEpic.y} position
And {DrawIOEpic} has a single {DrawIOSubEpic} with no nesting
When {DrawIOStoryMap} renders outline from {StoryMap}
Then {DrawIOSubEpic.expected_y} equals {DrawIOEpic.y} plus {DrawIOSubEpic.standard_offset}
```

**DrawIOEpic:**

| name | y |
| --- | --- |
| Wealth Management | 120 |


**DrawIOSubEpic (single child):**

| name | parent | standard_offset | expected_y |
| --- | --- | --- | --- |
| Portfolio Rebalancing | Wealth Management | 60 | 180 |


<a id="scenario-nested-container-spans-children-at-every-depth-level"></a>
### Scenario: [Nested container spans children at every depth level](#scenario-nested-container-spans-children-at-every-depth-level) (edge_case)

**Steps:**
```gherkin
Given {StoryMap} has {DrawIOSubEpic} nested multiple levels deep
And each {DrawIOSubEpic} is rendered with {DrawIOSubEpic.x} and {DrawIOSubEpic.width}
When {DrawIOStoryMap} renders outline from {StoryMap}
Then for each parent {DrawIOSubEpic}: parent.x <= child.x
And for each parent {DrawIOSubEpic}: child.x + child.width <= parent.x + parent.width
```

**DrawIOEpic:**

| name |
| --- |
| KYC Processing |


**DrawIOSubEpic (containment verification):**

| name | parent | depth | x | width |
| --- | --- | --- | --- | --- |
| Customer Onboarding | KYC Processing | 1 | 10 | 500 |
| Verify Identity | Customer Onboarding | 2 | 20 | 230 |
| Check Compliance | Customer Onboarding | 2 | 260 | 230 |
| Run Sanctions Screen | Verify Identity | 3 | 30 | 100 |

