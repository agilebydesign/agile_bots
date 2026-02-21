# 📄 Story Deleted in Hierarchy Cascades to Increment

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Edit Increments](.)  
**Sequential Order:** 7.0
**Story Type:** user

## Story Description

Story Deleted in Hierarchy Cascades to Increment functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User deletes story in story hierarchy
  **then** Story Graph removes story from hierarchy
  **and** removes story name from all increment stories arrays that reference it

## Scenarios

<a id="scenario-delete-story-in-hierarchy-removes-from-all-increments"></a>
### Scenario: [Delete story in hierarchy removes from all increments](#scenario-delete-story-in-hierarchy-removes-from-all-increments) (happy_path)

**Steps:**
```gherkin
Given story Validate Order exists in increments MVP and Phase 2
When User deletes story Validate Order from story hierarchy
Then Story Graph removes story from epics/sub-epics hierarchy
And Story Graph removes story name from all increment stories arrays
And Story Graph persists changes
```

