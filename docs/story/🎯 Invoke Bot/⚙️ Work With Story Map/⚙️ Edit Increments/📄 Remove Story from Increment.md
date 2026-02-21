# 📄 Remove Story from Increment

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Edit Increments](.)  
**Sequential Order:** 5.0
**Story Type:** user

## Story Description

Remove Story from Increment functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User removes story from increment
  **then** Story Graph removes story name from increment stories array
  **and** persists to story-graph.json

- **When** User removes story from increment
  **then** Story node remains in epics/sub-epics hierarchy (only increment assignment changes)

- **When** User removes story not in increment
  **then** System returns error
  **and** does not modify increment

- **When** User removes story from increment via CLI increments."MVP".remove_story story:"Validate Order"
  **then** CLI removes story from increment
  **and** displays confirmation

- **When** User selects story in increment row AND clicks Remove in Panel increment view
  **then** Panel removes story from increment
  **and** story appears in unallocated area to the left
  **and** Panel refreshes display (no delete option in increment view)

## Scenarios

<a id="scenario-remove-story-from-increment"></a>
### Scenario: [Remove story from increment](#scenario-remove-story-from-increment) (happy_path)

**Steps:**
```gherkin
Given increment MVP contains story Validate Order
When User removes story Validate Order from increment MVP
Then Story Graph removes story name from increment stories array
And Story node remains in graph
And Story Graph persists changes
```


<a id="scenario-cli-removes-story-from-increment-and-displays-confirmation"></a>
### Scenario: [CLI removes story from increment and displays confirmation](#scenario-cli-removes-story-from-increment-and-displays-confirmation) (happy_path)

**Steps:**
```gherkin
Given increment MVP contains story Validate Order
When User executes increments."MVP".remove_story story:"Validate Order"
Then CLI removes story from increment
And CLI displays confirmation
```


<a id="scenario-panel-remove-button-moves-story-to-unallocated-area"></a>
### Scenario: [Panel Remove button moves story to unallocated area](#scenario-panel-remove-button-moves-story-to-unallocated-area) (happy_path)

**Steps:**
```gherkin
Given User views story Validate Order in increment MVP row in Panel
When User selects story AND clicks Remove in Panel increment view
Then Panel removes story from increment
And Story appears in unallocated area to the left
And Panel refreshes display
```


<a id="scenario-remove-story-not-in-increment-returns-error"></a>
### Scenario: [Remove story not in increment returns error](#scenario-remove-story-not-in-increment-returns-error) (edge_case)

**Steps:**
```gherkin
Given increment MVP does not contain story Validate Order
When User removes story Validate Order from increment MVP
Then System returns error
And Increment stories array remains unchanged
```

