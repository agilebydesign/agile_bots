# 📄 Rename Story in Increment

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Edit Increments](.)  
**Sequential Order:** 6.0
**Story Type:** user

## Story Description

Rename Story in Increment functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User renames story node in graph
  **then** Story Graph updates story name in epics/sub-epics hierarchy
  **and** updates matching entries in all increment stories arrays

- **When** Story is renamed
  **then** All increments that contained old story name now contain new story name

- **When** User renames story to duplicate name in same parent
  **then** System returns validation error
  **and** does not rename

- **When** User renames story via CLI story_map."Epic"."SubEpic"."Story".rename name:"New Name"
  **then** CLI updates story in graph
  **and** updates increment references
  **and** displays confirmation

- **When** User renames story via Panel inline edit on story name
  **then** Panel updates story name in hierarchy
  **and** updates increment view of story to show new name (both story node and increment display reflect change)

## Scenarios

<a id="scenario-rename-story-node-updates-all-increment-references"></a>
### Scenario: [Rename story node updates all increment references](#scenario-rename-story-node-updates-all-increment-references) (happy_path)

**Steps:**
```gherkin
Given story Validate Order exists in increment MVP
When User renames story node Validate Order to Validate Order Items
Then Story Graph updates story name in epics hierarchy
And Story Graph updates story name in all increments that reference it
And Story Graph persists changes
```


<a id="scenario-cli-renames-story-and-updates-increment-references"></a>
### Scenario: [CLI renames story and updates increment references](#scenario-cli-renames-story-and-updates-increment-references) (happy_path)

**Steps:**
```gherkin
Given story Validate Order exists in increment MVP
When User executes story_map."Epic"."SubEpic"."Validate Order".rename name:"Validate Order Items"
Then CLI updates story in graph
And CLI updates increment references
And CLI displays confirmation
```


<a id="scenario-panel-inline-edit-updates-story-name-in-hierarchy-and-increment-view"></a>
### Scenario: [Panel inline edit updates story name in hierarchy and increment view](#scenario-panel-inline-edit-updates-story-name-in-hierarchy-and-increment-view) (happy_path)

**Steps:**
```gherkin
Given story Validate Order is displayed in hierarchy and in increment MVP row
When User edits story name inline to Validate Order Items AND blurs or presses Enter
Then Panel updates story name in hierarchy
And Panel updates increment view to show new name
And Both views reflect change
```


<a id="scenario-rename-story-to-duplicate-name-in-same-parent-returns-error"></a>
### Scenario: [Rename story to duplicate name in same parent returns error](#scenario-rename-story-to-duplicate-name-in-same-parent-returns-error) (edge_case)

**Steps:**
```gherkin
Given Story Graph has stories Validate Order and Validate Order Items in same parent
When User renames story Validate Order to Validate Order Items
Then System returns validation error
And Story Graph remains unchanged
```

