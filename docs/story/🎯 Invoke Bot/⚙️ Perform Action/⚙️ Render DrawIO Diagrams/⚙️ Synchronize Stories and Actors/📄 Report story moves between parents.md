# 📄 Report story moves between parents

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/synchronize_graph_with_rendered_diagram/test_synchronize_stories_and_actors.py#L298)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Render DrawIO Diagrams](..) / [⚙️ Synchronize Stories and Actors](.)  
**Sequential Order:** 3.0
**Story Type:** user

## Story Description

Report story moves between parents functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-no-changes-reported-when-diagram-matches-original-for-story-positions"></a>
### Scenario: [No changes reported when diagram matches original for story positions](#scenario-no-changes-reported-when-diagram-matches-original-for-story-positions) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStoryMap} has same story structure as {StoryMap}
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} has {UpdateReport.moved_count} of zero
And {UpdateReport} has {UpdateReport.renames_count} of zero
```


<a id="scenario-story-moved-between-sub-epics-detected-as-move-not-new-plus-removed"></a>
### Scenario: [Story moved between sub-epics detected as move not new plus removed](#scenario-story-moved-between-sub-epics-detected-as-move-not-new-plus-removed) (happy_path)

**Steps:**
```gherkin
Given {DrawIOStory} in {DrawIOStoryMap} has different parent than in {StoryMap}
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} detects the {DrawIOStory} as moved not new plus removed
```

**StoryMove (story moved between parents):**

| name | from_parent | to_parent |
| --- | --- | --- |
| View Plans | Select Plan | Change Plan |


<a id="scenario-story-moved-across-epics-detected-as-move-not-new-plus-removed"></a>
### Scenario: [Story moved across epics detected as move not new plus removed](#scenario-story-moved-across-epics-detected-as-move-not-new-plus-removed) (edge_case)

**Steps:**
```gherkin
Given {DrawIOStory} in {DrawIOStoryMap} has parent in different {Epic} than in {StoryMap}
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} detects the {DrawIOStory} as moved not new plus removed
```

**Epic (additional for cross-epic move):**

| name |
| --- |
| Manage Mobile Plans |
| Billing |


**SubEpic (additional for cross-epic move):**

| name | parent |
| --- | --- |
| Select Plan | Manage Mobile Plans |
| View Invoice | Billing |


**StoryMove (cross-epic move):**

| name | from_parent | to_parent |
| --- | --- | --- |
| View Plans | Select Plan | View Invoice |


<a id="scenario-report-roundtrips-through-json-for-story-move-changes"></a>
### Scenario: [Report roundtrips through JSON for story move changes](#scenario-report-roundtrips-through-json-for-story-move-changes) (happy_path)

**Steps:**
```gherkin
Given {UpdateReport} has story move changes
When {UpdateReport}.to_dict() serializes to JSON
And {UpdateReport}.from_dict() restores from JSON
Then all {UpdateReport} fields survive the roundtrip
```

**UpdateReport (new stories):**

| name | parent |
| --- | --- |
| View Billing | View Invoice |


**UpdateReport (removed stories):**

| name | parent |
| --- | --- |
| Downgrade Plan | Change Plan |


**UpdateReport (moved stories):**

| name | from_parent | to_parent |
| --- | --- | --- |
| Compare Plans | Select Plan | Change Plan |


<a id="scenario-stories-from-removed-sub-epic-detected-as-moves-to-parent"></a>
### Scenario: [Stories from removed sub-epic detected as moves to parent](#scenario-stories-from-removed-sub-epic-detected-as-moves-to-parent) (edge_case)

**Steps:**
```gherkin
Given {SubEpic} has been removed from {DrawIOStoryMap}
And {DrawIOStory} previously under that {SubEpic} now sits at {Epic} level
When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) is executed
Then {UpdateReport} detects the {DrawIOStory} as moved to parent {Epic}
```

**StoryMove (story moved to epic when sub-epic removed):**

| name | from_parent | to_parent |
| --- | --- | --- |
| View Plans | Select Plan | Manage Mobile Plans |

