# 📄 Add Story to Increment

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Edit Increments](.)  
**Sequential Order:** 4.0
**Story Type:** user

## Story Description

Add Story to Increment functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User adds story to increment
  **then** Story Graph appends story name to increment stories array
  **and** persists to story-graph.json

- **When** User adds story that exists in graph
  **then** Story Graph validates story name exists in epics/sub-epics/stories
  **and** adds to increment

- **When** User adds story already in increment
  **then** System returns validation error
  **and** does not add duplicate

- **When** User adds story to increment via CLI increments."MVP".add_story story:"Validate Order"
  **then** CLI adds story
  **and** displays confirmation

- **When** User views increments in Panel
  **then** Panel shows unallocated increment area to the very left
  **and** displays all stories not in any increment in that area

- **When** User drags story from unallocated area onto increment row in Panel
  **then** Panel adds story to increment
  **and** refreshes increment display

- **When** User drags story from one increment row to another increment row in Panel
  **then** Panel adds story to target increment
  **and** removes story from source increment
  **and** refreshes increment display

## Scenarios

<a id="scenario-add-story-to-increment-by-story-name"></a>
### Scenario: [Add story to increment by story name](#scenario-add-story-to-increment-by-story-name) (happy_path)

**Steps:**
```gherkin
Given Story Graph has increment MVP and story Validate Order
When User adds story Validate Order to increment MVP
Then Story Graph appends story name to increment stories array
And Story Graph persists changes
```


<a id="scenario-add-non-existent-story-to-increment-returns-error"></a>
### Scenario: [Add non-existent story to increment returns error](#scenario-add-non-existent-story-to-increment-returns-error) (edge_case)

**Steps:**
```gherkin
Given Story Graph has no story named Missing Story
When User adds story Missing Story to increment MVP
Then System returns error
And Increment stories array remains unchanged
```


<a id="scenario-cli-adds-story-to-increment-and-displays-confirmation"></a>
### Scenario: [CLI adds story to increment and displays confirmation](#scenario-cli-adds-story-to-increment-and-displays-confirmation) (happy_path)

**Steps:**
```gherkin
Given Story Graph has increment MVP and story Validate Order
When User executes increments."MVP".add_story story:"Validate Order"
Then CLI adds story to increment
And CLI displays confirmation
```


<a id="scenario-panel-drag-from-unallocated-onto-increment-row-adds-story-and-refreshes"></a>
### Scenario: [Panel drag from unallocated onto increment row adds story and refreshes](#scenario-panel-drag-from-unallocated-onto-increment-row-adds-story-and-refreshes) (happy_path)

**Steps:**
```gherkin
Given Panel shows unallocated area with story Validate Order AND increment row MVP
When User drags story Validate Order from unallocated area onto increment MVP row
Then Panel adds story to increment
And Panel refreshes increment display
```


<a id="scenario-add-story-already-in-increment-returns-error"></a>
### Scenario: [Add story already in increment returns error](#scenario-add-story-already-in-increment-returns-error) (edge_case)

**Steps:**
```gherkin
Given increment MVP contains story Validate Order
When User adds story Validate Order to increment MVP
Then System returns validation error
And Increment stories array remains unchanged
```

