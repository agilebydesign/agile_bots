# 📄 Report acceptance criteria changes

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/synchronize_graph_with_rendered_diagram/test_synchronize_stories_and_actors.py#L363)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Render DrawIO Diagrams](..) / [⚙️ Synchronize Stories and Actors](.)  
**Sequential Order:** 4.0
**Story Type:** user

## Story Description

Report acceptance criteria changes functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-no-changes-reported-when-diagram-matches-original-for-acceptance-criteria"></a>
### Scenario: [No changes reported when diagram matches original for acceptance criteria](#scenario-no-changes-reported-when-diagram-matches-original-for-acceptance-criteria) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has same {AcceptanceCriteria} structure as {StoryMap}
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} has {UpdateReport.ac_added_count} of zero
And {UpdateReport} has {UpdateReport.ac_removed_count} of zero
```


<a id="scenario-ac-box-added-in-diagram-detected-as-new-in-report"></a>
### Scenario: [AC box added in diagram detected as new in report](#scenario-ac-box-added-in-diagram-detected-as-new-in-report) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has {DrawIOElement} AC box not present in {StoryMap}
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} lists the {AcceptanceCriteria} as new
```

**ACChange (acceptance criteria added):**

| story_name | added |
| --- | --- |
| Create Account | When balance checked then fee waived |


<a id="scenario-ac-box-removed-from-diagram-detected-as-removed-in-report"></a>
### Scenario: [AC box removed from diagram detected as removed in report](#scenario-ac-box-removed-from-diagram-detected-as-removed-in-report) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} lacks {DrawIOElement} AC box that {StoryMap} has
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} lists the {AcceptanceCriteria} as removed
```

**ACChange (acceptance criteria removed):**

| story_name | removed |
| --- | --- |
| Create Account | When duplicate SSN then rejection shown |


<a id="scenario-ac-moved-between-stories-detected-as-move-not-new-plus-removed"></a>
### Scenario: [AC moved between stories detected as move not new plus removed](#scenario-ac-moved-between-stories-detected-as-move-not-new-plus-removed) (happy_path)

**Steps:**
```gherkin
Given {DrawIOElement} AC box has moved from one {DrawIOStory} to another
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} detects the {AcceptanceCriteria} as moved not new plus removed
```

**ACChange (acceptance criteria moved between stories):**

| text | from_story | to_story |
| --- | --- | --- |
| When documents uploaded then verification started | Verify Identity | Create Account |


<a id="scenario-ac-boxes-assigned-to-stories-by-vertical-position-below-story-cells"></a>
### Scenario: [AC boxes assigned to stories by vertical position below story cells](#scenario-ac-boxes-assigned-to-stories-by-vertical-position-below-story-cells) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has AC {DrawIOElement} positioned below {DrawIOStory}
When {DrawIOStoryMap} extracts from diagram
Then each AC {DrawIOElement} is assigned to its {DrawIOStory} by vertical position
```


<a id="scenario-extract-assigns-ac-boxes-to-stories-by-vertical-position-and-containment"></a>
### Scenario: [Extract assigns AC boxes to stories by vertical position and containment](#scenario-extract-assigns-ac-boxes-to-stories-by-vertical-position-and-containment) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has AC {DrawIOElement} positioned below {DrawIOStory}
When {DrawIOStoryMap} extracts exploration from diagram
Then {DrawIOStoryMap} assigns AC cells to {DrawIOStory} by vertical position and containment
And AC text mapped back to {AcceptanceCriteria}
```


<a id="scenario-report-roundtrips-through-json-for-acceptance-criteria-changes"></a>
### Scenario: [Report roundtrips through JSON for acceptance criteria changes](#scenario-report-roundtrips-through-json-for-acceptance-criteria-changes) (happy_path)

**Steps:**
```gherkin
Given {UpdateReport} has acceptance criteria changes
When {UpdateReport}.to_dict() serializes to JSON
And {UpdateReport}.from_dict() restores from JSON
Then all {UpdateReport} fields survive the roundtrip
```

**UpdateReport (added AC):**

| story_name | text |
| --- | --- |
| Create Account | When balance checked then fee waived |


**UpdateReport (removed AC):**

| story_name | text |
| --- | --- |
| Verify Identity | When documents uploaded then verification started |


<a id="scenario-ac-box-with-whenthen-format-text-extracted-as-step-description"></a>
### Scenario: [AC box with When/Then format text extracted as step description](#scenario-ac-box-with-whenthen-format-text-extracted-as-step-description) (edge_case)

**Steps:**
```gherkin
Given AC {DrawIOElement} has {DrawIOElement.text} with When/Then format
When {DrawIOStoryMap} extracts exploration from diagram
Then {DrawIOStoryMap} extracts step description from {DrawIOElement.text}
And associates extracted step with the containing {DrawIOStory}
```

**DrawIOElement (AC box with When/Then format):**

| parent_story | text | text_format |
| --- | --- | --- |
| Create Account | When valid ID provided then account created | when_then |


<a id="scenario-ac-box-with-plain-text-format-treated-as-acceptance-criteria-without-step-extraction"></a>
### Scenario: [AC box with plain text format treated as acceptance criteria without step extraction](#scenario-ac-box-with-plain-text-format-treated-as-acceptance-criteria-without-step-extraction) (edge_case)

**Steps:**
```gherkin
Given AC {DrawIOElement} has {DrawIOElement.text} with plain format
When {DrawIOStoryMap} extracts exploration from diagram
Then {DrawIOStoryMap} treats {DrawIOElement.text} as plain {AcceptanceCriteria} description
And associates it with the containing {DrawIOStory} without step extraction
```

**DrawIOElement (AC box with plain text format):**

| parent_story | text | text_format |
| --- | --- | --- |
| Create Account | User must provide government-issued ID | plain |

