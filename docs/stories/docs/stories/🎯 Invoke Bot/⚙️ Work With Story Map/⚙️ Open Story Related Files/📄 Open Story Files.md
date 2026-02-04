# 📄 Open Story Files

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** User
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Open Story Related Files](.)  
**Sequential Order:** 2.0
**Story Type:** user

## Story Description

Open Story Files functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User clicks graph link

  **then** System opens story-graph.json in editor

- **When** User clicks map link

  **then** System opens story-map.drawio in diagram viewer

- **When** System cannot open file

  **then** System displays error message

## Scenarios

<a id="scenario-user-opens-story-graph-json-file"></a>
### Scenario: [User opens story graph JSON file](#scenario-user-opens-story-graph-json-file) (happy_path)

**Steps:**
```gherkin
Given Panel displays scope section with graph link
When User clicks Graph link
Then VS Code opens story-graph.json in editor
And File is displayed with JSON syntax highlighting
```


<a id="scenario-user-opens-story-map-diagram"></a>
### Scenario: [User opens story map diagram](#scenario-user-opens-story-map-diagram) (happy_path)

**Steps:**
```gherkin
Given Panel displays scope section with map link
When User clicks map link
Then VS Code opens story-map.drawio in diagram viewer
And Diagram is displayed with Draw.io extension
```


<a id="scenario-user-clicks-link-to-non-existent-file-shows-error"></a>
### Scenario: [User clicks link to non-existent file shows error](#scenario-user-clicks-link-to-non-existent-file-shows-error) (error_case)

**Steps:**
```gherkin
Given Panel displays link to non-existent file
When User clicks link
Then Panel displays error message
And Error message indicates file not found
```


<a id="scenario-story-graph-and-map-links-always-visible-in-scope-header"></a>
### Scenario: [Story graph and map links always visible in scope header](#scenario-story-graph-and-map-links-always-visible-in-scope-header) (happy_path)

**Steps:**
```gherkin
Given Panel displays scope section
And Scope may be filtered or showing all stories
When User views scope header
Then story-graph.json link is always visible
And story-map.md link is always visible
And Links persist regardless of filter state
And Links are positioned consistently in header
```

