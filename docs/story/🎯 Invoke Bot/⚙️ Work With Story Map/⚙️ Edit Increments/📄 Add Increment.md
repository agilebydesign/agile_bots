# 📄 Add Increment

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Edit Increments](.)  
**Sequential Order:** 1.0
**Story Type:** user

## Story Description

Add Increment functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User selects existing increment AND adds increment with name
  **then** Story Graph inserts new increment after selected
  **and** assigns new increment priority equal to selected priority plus one
  **and** increments priority of all increments with priority greater than or equal to selected plus one by one
  **and** initializes empty stories array
  **and** persists to story-graph.json

- **When** User adds increment with no increment selected
  **then** Story Graph appends increment to end of list
  **and** assigns highest priority number (lowest delivery priority)
  **and** initializes empty stories array
  **and** persists to story-graph.json

- **When** User adds increment with duplicate name
  **then** System returns validation error
  **and** does not add increment

- **When** User adds increment via CLI increments.add name:"Increment Name" after:"MVP"
  **then** CLI inserts increment after MVP with bumped priorities
  **and** displays confirmation

- **When** User adds increment via CLI increments.add name:"Increment Name"
  **then** CLI appends increment to end with highest priority number
  **and** displays confirmation

- **When** User selects increment AND adds via Panel increment Add button
  **then** Panel shows name input
  **and** User submits
  **and** Panel inserts new increment after selected
  **and** Panel refreshes increment list

- **When** User adds via Panel increment Add button with no increment selected
  **then** Panel shows name input
  **and** User submits
  **and** Panel appends increment to end of list
  **and** Panel refreshes increment list

## Background

```gherkin
Given Story Graph has increments MVP (priority 1) and Phase 2 (priority 2)
```


## Scenarios

<a id="scenario-add-increment-after-selected-increment"></a>
### Scenario: [Add increment after selected increment](#scenario-add-increment-after-selected-increment) (happy_path)

**Steps:**
```gherkin
When User selects increment MVP AND adds increment with name Phase 1.5
Then Story Graph inserts new increment between MVP and Phase 2
And New increment has priority 2 (selected plus one)
And Phase 2 and all later increments have priority increased by 1
And Story Graph persists changes
```


<a id="scenario-add-increment-when-nothing-selected-appends-to-back"></a>
### Scenario: [Add increment when nothing selected appends to back](#scenario-add-increment-when-nothing-selected-appends-to-back) (happy_path)

**Steps:**
```gherkin
When User adds increment with name Phase 3 (no increment selected)
Then Story Graph appends increment to end of list
And New increment has highest priority number (lowest delivery priority)
And Story Graph persists changes
```


<a id="scenario-add-increment-with-duplicate-name-returns-error"></a>
### Scenario: [Add increment with duplicate name returns error](#scenario-add-increment-with-duplicate-name-returns-error) (edge_case)

**Steps:**
```gherkin
Given Story Graph has increment named MVP
When User adds increment with same name MVP
Then System identifies duplicate and returns error
And Story Graph remains unchanged
```


<a id="scenario-cli-adds-increment-after-mvp-with-bumped-priorities"></a>
### Scenario: [CLI adds increment after MVP with bumped priorities](#scenario-cli-adds-increment-after-mvp-with-bumped-priorities) (happy_path)

**Steps:**
```gherkin
When User executes increments.add name:"Phase 1.5" after:"MVP"
Then CLI inserts increment after MVP with bumped priorities
And CLI displays confirmation
```


<a id="scenario-cli-appends-increment-to-end-when-no-after-specified"></a>
### Scenario: [CLI appends increment to end when no after specified](#scenario-cli-appends-increment-to-end-when-no-after-specified) (happy_path)

**Steps:**
```gherkin
When User executes increments.add name:"Phase 3"
Then CLI appends increment to end with highest priority number
And CLI displays confirmation
```


<a id="scenario-panel-add-button-with-selection-inserts-after-selected-and-refreshes"></a>
### Scenario: [Panel Add button with selection inserts after selected and refreshes](#scenario-panel-add-button-with-selection-inserts-after-selected-and-refreshes) (happy_path)

**Steps:**
```gherkin
Given User has increment MVP selected in Panel increment view
When User clicks Add button AND enters name Phase 1.5 AND submits
Then Panel shows name input
And Panel inserts new increment after MVP
And Panel refreshes increment list
```

