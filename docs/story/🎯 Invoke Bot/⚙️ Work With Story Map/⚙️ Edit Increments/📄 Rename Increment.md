# 📄 Rename Increment

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Edit Increments](.)  
**Sequential Order:** 3.0
**Story Type:** user

## Story Description

Rename Increment functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User renames increment from old name to new name
  **then** Story Graph updates increment name in increments list
  **and** persists to story-graph.json

- **When** User renames increment to duplicate existing name
  **then** System returns validation error
  **and** does not rename

- **When** User renames increment
  **then** Story names in increment stories array remain unchanged (stories referenced by name)

- **When** User renames increment via CLI increments.rename from:"MVP" to:"Phase 1"
  **then** CLI updates increment
  **and** displays confirmation

- **When** User renames increment via Panel inline edit on increment name
  **then** Panel updates name on blur or Enter
  **and** refreshes display

## Scenarios

<a id="scenario-rename-increment-to-new-name"></a>
### Scenario: [Rename increment to new name](#scenario-rename-increment-to-new-name) (happy_path)

**Steps:**
```gherkin
Given Story Graph has increment named MVP
When User renames increment MVP to Phase 1
Then Story Graph updates increment name
And Story references in increment remain unchanged
And Story Graph persists changes
```


<a id="scenario-cli-renames-increment-and-displays-confirmation"></a>
### Scenario: [CLI renames increment and displays confirmation](#scenario-cli-renames-increment-and-displays-confirmation) (happy_path)

**Steps:**
```gherkin
Given Story Graph has increment named MVP
When User executes increments.rename from:"MVP" to:"Phase 1"
Then CLI updates increment
And CLI displays confirmation
```


<a id="scenario-panel-inline-edit-updates-increment-name-on-blur-or-enter"></a>
### Scenario: [Panel inline edit updates increment name on blur or Enter](#scenario-panel-inline-edit-updates-increment-name-on-blur-or-enter) (happy_path)

**Steps:**
```gherkin
Given User views increment MVP in Panel increment view
When User edits increment name inline to Phase 1 AND blurs or presses Enter
Then Panel updates name
And Panel refreshes display
```


<a id="scenario-rename-increment-to-duplicate-existing-name-returns-error"></a>
### Scenario: [Rename increment to duplicate existing name returns error](#scenario-rename-increment-to-duplicate-existing-name-returns-error) (edge_case)

**Steps:**
```gherkin
Given Story Graph has increments MVP and Phase 1
When User renames increment MVP to Phase 1
Then System returns validation error
And Story Graph remains unchanged
```

