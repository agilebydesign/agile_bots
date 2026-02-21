# 📄 Report epic and sub-epic changes

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/synchronize_graph_with_rendered_diagram/test_synchronize_epics_and_sub_epics.py#L284)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Render DrawIO Diagrams](..) / [⚙️ Synchronize Epics and Sub-Epics](.)  
**Sequential Order:** 2.0
**Story Type:** user

## Story Description

Report epic and sub-epic changes functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-no-changes-reported-when-diagram-matches-original-for-epics-and-sub-epics"></a>
### Scenario: [No changes reported when diagram matches original for epics and sub-epics](#scenario-no-changes-reported-when-diagram-matches-original-for-epics-and-sub-epics) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has same sub-epic structure as {StoryMap}
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} has {UpdateReport.renames_count} of zero
And {UpdateReport} has {UpdateReport.new_count} of zero
And {UpdateReport} has {UpdateReport.removed_count} of zero
```


<a id="scenario-sub-epic-added-in-diagram-detected-as-new-in-report"></a>
### Scenario: [Sub-epic added in diagram detected as new in report](#scenario-sub-epic-added-in-diagram-detected-as-new-in-report) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has {DrawIOSubEpic} not present in {StoryMap}
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} lists {DrawIOSubEpic} as new
```

**DrawIOSubEpic (new in diagram):**

| name | parent |
| --- | --- |
| Nostro Reconciliation | Wire Transfers |


<a id="scenario-sub-epic-renamed-in-diagram-detected-as-rename-in-report"></a>
### Scenario: [Sub-epic renamed in diagram detected as rename in report](#scenario-sub-epic-renamed-in-diagram-detected-as-rename-in-report) (happy_path)

**Steps:**
```gherkin
Given {DrawIOSubEpic} in {DrawIOStoryMap} has different name than {StoryMap}
And {StoryMap} has the original name
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} pairs the {DrawIOSubEpic} as a rename match
```

**DrawIOSubEpic (renamed in diagram):**

| original_name | new_name | parent |
| --- | --- | --- |
| Correspondent Banking | Nostro Reconciliation | Wire Transfers |


<a id="scenario-report-roundtrips-through-json-for-epic-and-sub-epic-hierarchy-structure"></a>
### Scenario: [Report roundtrips through JSON for epic and sub-epic hierarchy structure](#scenario-report-roundtrips-through-json-for-epic-and-sub-epic-hierarchy-structure) (happy_path)

**Steps:**
```gherkin
Given {UpdateReport} has sub-epic changes
When {UpdateReport}.to_dict() serializes to JSON
And {UpdateReport}.from_dict() restores from JSON
Then all {UpdateReport} fields survive the roundtrip
```

**UpdateReport (renames):**

| original_name | new_name | parent |
| --- | --- | --- |
| Correspondent Banking | Nostro Reconciliation | Wire Transfers |


**UpdateReport (new sub-epics):**

| name | parent |
| --- | --- |
| FX Conversion | Wire Transfers |
| Cross-Border Settlement | Wire Transfers |


**UpdateReport (removed sub-epics):**

| name | parent |
| --- | --- |
| Domestic Wires | Wire Transfers |


<a id="scenario-report-lists-exact-fuzzy-new-and-removed-entities-for-epics"></a>
### Scenario: [Report lists exact fuzzy new and removed entities for epics](#scenario-report-lists-exact-fuzzy-new-and-removed-entities-for-epics) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} exists with content extracted from diagram
And {StoryMap} exists with known {DrawIOSubEpic} names
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} lists exact matches and fuzzy matches and new and removed {DrawIOSubEpic}
```

**DrawIOSubEpic (in diagram - includes exact, fuzzy, and new):**

| name | parent | match_type |
| --- | --- | --- |
| Correspondent Banking | Wire Transfers | exact |
| Nostro Reconciliation | Wire Transfers | fuzzy |
| FX Conversion | Wire Transfers | new |


<a id="scenario-only-hierarchical-cell-id-sub-epics-participate-in-rename-pairing"></a>
### Scenario: [Only hierarchical cell ID sub-epics participate in rename pairing](#scenario-only-hierarchical-cell-id-sub-epics-participate-in-rename-pairing) (edge_case)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has unmatched {DrawIOSubEpic} with both simple and hierarchical {DrawIOElement.cell_id}
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then only {DrawIOSubEpic} with hierarchical {DrawIOElement.cell_id} participate in rename pairing
And {DrawIOSubEpic} with simple {DrawIOElement.cell_id} are treated as new
```

**DrawIOSubEpic (unmatched in diagram):**

| name | parent |
| --- | --- |
| Nostro Reconciliation | Wire Transfers |
| FX Conversion | Wire Transfers |


**DrawIOElement (cell IDs for unmatched DrawIOSubEpic):**

| sub_epic_name | cell_id | id_type |
| --- | --- | --- |
| Nostro Reconciliation | epic-1/sub-epic-2 | hierarchical |
| FX Conversion | abc123 | simple |


<a id="scenario-all-simple-cell-id-sub-epics-treated-as-new-when-no-hierarchical-candidates"></a>
### Scenario: [All simple cell ID sub-epics treated as new when no hierarchical candidates](#scenario-all-simple-cell-id-sub-epics-treated-as-new-when-no-hierarchical-candidates) (edge_case)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has unmatched {DrawIOSubEpic} all with simple {DrawIOElement.cell_id}
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then no {DrawIOSubEpic} participate in rename pairing
And all unmatched {DrawIOSubEpic} are listed as new in {UpdateReport}
```

**DrawIOSubEpic (unmatched in diagram):**

| name | parent |
| --- | --- |
| Nostro Reconciliation | Wire Transfers |
| FX Conversion | Wire Transfers |


**DrawIOElement (all simple cell IDs):**

| sub_epic_name | cell_id | id_type |
| --- | --- | --- |
| Nostro Reconciliation | abc123 | simple |
| FX Conversion | xyz789 | simple |


<a id="scenario-story-rename-works-regardless-of-cell-id-format"></a>
### Scenario: [Story rename works regardless of cell ID format](#scenario-story-rename-works-regardless-of-cell-id-format) (edge_case)  | [Test](/test/invoke_bot/perform_action/synchronize_graph_with_rendered_diagram/test_synchronize_epics_and_sub_epics.py#L323)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has {DrawIOStory} with name different from {StoryMap} and any {DrawIOElement.cell_id} format
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} detects {DrawIOStory} rename regardless of {DrawIOElement.cell_id} format
And {DrawIOElement.cell_id} type filtering only applies to {DrawIOSubEpic} and {DrawIOEpic}
```

**DrawIOStory (renamed in diagram):**

| original_name | new_name | parent | cell_id |
| --- | --- | --- | --- |
| Validate SWIFT Code | Validate BIC Code | Correspondent Banking | abc123 |


<a id="scenario-removed-epics-and-sub-epics-flagged-as-large-deletions-in-report"></a>
### Scenario: [Removed epics and sub-epics flagged as large deletions in report](#scenario-removed-epics-and-sub-epics-flagged-as-large-deletions-in-report) (edge_case)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has fewer nodes than {StoryMap}
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} lists deleted nodes as removed
And {UpdateReport.large_deletions} flags entire missing {DrawIOEpic} or {DrawIOSubEpic}
```

**DrawIOSubEpic (missing from diagram):**

| name | parent | present_in_diagram |
| --- | --- | --- |
| Cross-Border Settlement | Wire Transfers | false |


**UpdateReport (large deletions):**

| deletion_type | name |
| --- | --- |
| missing_sub_epics | Cross-Border Settlement |

