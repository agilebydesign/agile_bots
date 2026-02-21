# 📄 Report increment changes

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/synchronize_graph_with_rendered_diagram/test_synchronize_increments.py#L254)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Render DrawIO Diagrams](..) / [⚙️ Synchronize Increments](.)  
**Sequential Order:** 2.0
**Story Type:** user

## Story Description

Report increment changes functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-no-changes-reported-when-diagram-matches-original-for-increments"></a>
### Scenario: [No changes reported when diagram matches original for increments](#scenario-no-changes-reported-when-diagram-matches-original-for-increments) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has same {Increment} structure as {StoryMap}
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} reports zero increment changes
```


<a id="scenario-increment-lane-added-in-diagram-detected-as-new-in-report"></a>
### Scenario: [Increment lane added in diagram detected as new in report](#scenario-increment-lane-added-in-diagram-detected-as-new-in-report) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has a new {Increment} lane added by user
And original {StoryMap} does not have this {Increment}
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} lists the {Increment} as new
```

**Increment (new in diagram):**

| name | priority |
| --- | --- |
| Launch | 1 |
| Phase 2 | 2 |
| Phase 3 | 3 |


<a id="scenario-story-moved-between-increment-lanes-detected-as-move-in-report"></a>
### Scenario: [Story moved between increment lanes detected as move in report](#scenario-story-moved-between-increment-lanes-detected-as-move-in-report) (happy_path)

**Steps:**
```gherkin
Given {IncrementStory} has been moved from one {Increment} to another in {DrawIOStoryMap}
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} detects the {IncrementChange} as moved not new plus removed
```

**IncrementChange (story moved between increments):**

| increment_name | story_name | change_type |
| --- | --- | --- |
| Phase 2 | Update menu items | added |
| Launch | Update menu items | removed |


<a id="scenario-increment-lane-renamed-in-diagram-detected-as-rename-in-report"></a>
### Scenario: [Increment lane renamed in diagram detected as rename in report](#scenario-increment-lane-renamed-in-diagram-detected-as-rename-in-report) (happy_path)

**Steps:**
```gherkin
Given {Increment} lane has been renamed in {DrawIOStoryMap}
And original {StoryMap} has the original name
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} pairs the renamed {Increment} as a rename match
```

**Increment (renamed in diagram):**

| original_name | new_name |
| --- | --- |
| Phase 2 | Phase Two |


<a id="scenario-stories-assigned-to-increment-lanes-by-y-position"></a>
### Scenario: [Stories assigned to increment lanes by Y position](#scenario-stories-assigned-to-increment-lanes-by-y-position) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has {DrawIOStory} cells positioned below {Increment} lane elements
When {DrawIOStoryMap} extracts from diagram
Then each {DrawIOStory} is assigned to its {Increment} by vertical position
```


<a id="scenario-extract-assigns-stories-to-increment-lanes-by-y-position-with-priority-from-order"></a>
### Scenario: [Extract assigns stories to increment lanes by Y position with priority from order](#scenario-extract-assigns-stories-to-increment-lanes-by-y-position-with-priority-from-order) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} increments file contains {Increment} lane cells and {DrawIOStory} cells
When {DrawIOStoryMap} extracts increments from diagram
Then {DrawIOStoryMap} identifies {Increment} lanes from left side of diagram by style sorted top to bottom
And each {DrawIOStory} assigned to nearest lane within 100px by Y position
And each lane gets position-based {Increment.priority} and name from cell label
And extracted JSON written to file
```


<a id="scenario-report-roundtrips-through-json-for-increment-changes"></a>
### Scenario: [Report roundtrips through JSON for increment changes](#scenario-report-roundtrips-through-json-for-increment-changes) (happy_path)

**Steps:**
```gherkin
Given {UpdateReport} has increment changes
When {UpdateReport}.to_dict() serializes to JSON
And {UpdateReport}.from_dict() restores from JSON
Then all increment change fields survive the roundtrip
```

**UpdateReport (renamed increments):**

| original_name | new_name |
| --- | --- |
| Phase 2 | Phase Two |


**UpdateReport (new increments):**

| name | priority |
| --- | --- |
| Phase 3 | 3 |


**UpdateReport (removed increments):**

| name | priority |
| --- | --- |
| Beta | 4 |


**UpdateReport (moved stories):**

| story_name | from_increment | to_increment |
| --- | --- | --- |
| Update menu items | Launch | Phase 2 |


<a id="scenario-report-lists-exact-fuzzy-new-and-removed-stories-for-increments-view"></a>
### Scenario: [Report lists exact fuzzy new and removed stories for increments view](#scenario-report-lists-exact-fuzzy-new-and-removed-stories-for-increments-view) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has been extracted from diagram
And original {StoryMap} exists with known {Increment} names
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} lists exact matches and fuzzy matches and new and removed increments
```

**Increment (in diagram - includes exact, fuzzy, and new):**

| name | match_type |
| --- | --- |
| Launch | exact |
| Phase Two | fuzzy |
| Phase 3 | new |


**Increment (removed from diagram):**

| name |
| --- |
| Beta |


<a id="scenario-report-includes-removed-increments-and-new-order"></a>
### Scenario: [Report includes removed increments and new order](#scenario-report-includes-removed-increments-and-new-order) (edge_case)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has fewer {Increment} than original {StoryMap}
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} includes removed {Increment} and updated order
```

**Increment (removed from diagram):**

| name | priority |
| --- | --- |
| Phase 2 | 2 |


<a id="scenario-user-created-lane-detected-by-geometry-in-diagram"></a>
### Scenario: [User-created lane detected by geometry in diagram](#scenario-user-created-lane-detected-by-geometry-in-diagram) (edge_case)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has a user-created lane with simple {DrawIOElement.cell_id} and large rectangle geometry
When {DrawIOStoryMap} extracts increments from diagram
Then the user-created lane is detected as a new {Increment} by its geometry
```

**DrawIOElement (user-created lane geometry):**

| cell_id | geometry_width | geometry_height |
| --- | --- | --- |
| lane-user-1 | 800 | 200 |


<a id="scenario-orphan-story-dragged-into-lane-reported-as-added-to-increment"></a>
### Scenario: [Orphan story dragged into lane reported as added to increment](#scenario-orphan-story-dragged-into-lane-reported-as-added-to-increment) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStory} is unassigned in {DrawIOStoryMap} increments diagram
And user drags {DrawIOStory} into an {Increment} lane
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} reports {DrawIOStory} as added to that {Increment}
```

**IncrementChange (story added to increment):**

| increment_name | story_name | change_type |
| --- | --- | --- |
| Launch | Check delivery status | added |


<a id="scenario-story-in-multiple-lanes-produces-no-false-duplicate-reports"></a>
### Scenario: [Story in multiple lanes produces no false duplicate reports](#scenario-story-in-multiple-lanes-produces-no-false-duplicate-reports) (edge_case)

**Steps:**
```gherkin
Given {DrawIOStory} appears in multiple {Increment} lanes in {DrawIOStoryMap}
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} does not produce false duplicate or new entries
```

**IncrementStory (story in multiple increments):**

| increment_name | story_name |
| --- | --- |
| Launch | Create order |
| Phase 2 | Create order |


<a id="scenario-known-limitation-inserting-between-existing-lanes-uses-position-based-matching"></a>
### Scenario: [Known limitation inserting between existing lanes uses position-based matching](#scenario-known-limitation-inserting-between-existing-lanes-uses-position-based-matching) (edge_case)

**Steps:**
```gherkin
Given original {StoryMap} has {Increment} lanes [A, B, C]
And a new lane has been inserted between A and B in {DrawIOStoryMap}
When {DrawIOStoryMap} extracts increments from diagram
Then position-based matching maps extracted lane 1 to original A and lane 2 to original B
And the inserted lane may be misinterpreted as a rename of B without stable IDs
```

**Increment (original lanes):**

| name | priority |
| --- | --- |
| A | 1 |
| B | 2 |
| C | 3 |


<a id="scenario-story-not-within-threshold-of-any-lane-remains-unassigned"></a>
### Scenario: [Story not within threshold of any lane remains unassigned](#scenario-story-not-within-threshold-of-any-lane-remains-unassigned) (edge_case)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has {DrawIOStory} positioned more than 100px from any {Increment} lane
When {DrawIOStoryMap} extracts increments from diagram
Then that {DrawIOStory} is not assigned to any {Increment} lane
```

