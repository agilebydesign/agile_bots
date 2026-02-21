# 📄 Remove Increment

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Edit Increments](.)  
**Sequential Order:** 2.0
**Story Type:** user

## Story Description

Remove Increment functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User removes increment by name
  **then** Story Graph removes increment from increments list
  **and** persists to story-graph.json

- **When** User removes increment that contains stories
  **then** Story Graph removes increment from increments list
  **and** stories within hierarchy are unaffected (only increment assignment list is removed)

- **When** User removes non-existent increment
  **then** System returns error
  **and** does not modify story graph

- **When** User removes increment via CLI increments.remove name:"MVP"
  **then** CLI removes increment
  **and** displays confirmation

- **When** User selects increment in Panel AND clicks Delete button
  **then** Panel prompts confirmation
  **and** User confirms
  **and** Panel refreshes increment list

## Scenarios

<a id="scenario-remove-increment-by-name"></a>
### Scenario: [Remove increment by name](#scenario-remove-increment-by-name) (happy_path)

**Steps:**
```gherkin
Given Story Graph has increment named MVP
When User removes increment MVP
Then Story Graph removes increment from list
And Story Graph persists changes
```


<a id="scenario-remove-non-existent-increment-returns-error"></a>
### Scenario: [Remove non-existent increment returns error](#scenario-remove-non-existent-increment-returns-error) (edge_case)

**Steps:**
```gherkin
Given Story Graph has no increment named Missing
When User removes increment Missing
Then System returns error
And Story Graph remains unchanged
```


<a id="scenario-cli-removes-increment-and-displays-confirmation"></a>
### Scenario: [CLI removes increment and displays confirmation](#scenario-cli-removes-increment-and-displays-confirmation) (happy_path)

**Steps:**
```gherkin
Given Story Graph has increment named MVP
When User executes increments.remove name:"MVP"
Then CLI removes increment
And CLI displays confirmation
```


<a id="scenario-panel-delete-button-prompts-confirmation-and-refreshes-list"></a>
### Scenario: [Panel Delete button prompts confirmation and refreshes list](#scenario-panel-delete-button-prompts-confirmation-and-refreshes-list) (happy_path)

**Steps:**
```gherkin
Given User has increment MVP selected in Panel increment view
When User clicks Delete button AND confirms
Then Panel prompts confirmation
And Panel refreshes increment list
```


<a id="scenario-remove-increment-that-contains-stories-leaves-hierarchy-unchanged"></a>
### Scenario: [Remove increment that contains stories leaves hierarchy unchanged](#scenario-remove-increment-that-contains-stories-leaves-hierarchy-unchanged) (edge_case)

**Steps:**
```gherkin
Given increment MVP contains story Validate Order
When User removes increment MVP
Then Story Graph removes increment from list
And Story Validate Order remains in epics/sub-epics hierarchy
And Story Graph persists changes
```

