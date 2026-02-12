# 📄 Change Workspace Path panel

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** User
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Initialize Bot](..) / [⚙️ Set Workspace](.)  
**Sequential Order:** 2
**Story Type:** user

## Story Description

Change Workspace Path panel functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User changes workspace path
  **then** System displays updated workspace path
  **and** System displays behavior action state of new workspace

- **When** User sets workspace path
  **then** System persists workspace path value

- **When** Panel refreshes
  **then** System restores previously set workspace path

## Scenarios

<a id="scenario-user-changes-workspace-and-panel-displays-new-state"></a>
### Scenario: [User changes workspace and panel displays new state](#scenario-user-changes-workspace-and-panel-displays-new-state) (happy_path)

**Steps:**
```gherkin
Given Panel is open showing workspace at c:/dev/project_a
And Workspace at c:/dev/project_b exists with different bot state
When User changes workspace path to c:/dev/project_b
Then Panel displays c:/dev/project_b as current workspace
And Panel displays behavior action state from project_b
And Panel refreshes all sections with project_b data
```


<a id="scenario-user-changes-to-nonexistent-directory-shows-error"></a>
### Scenario: [User changes to nonexistent directory shows error](#scenario-user-changes-to-nonexistent-directory-shows-error) (error_case)

**Steps:**
```gherkin
Given Panel is open showing valid workspace
When User changes workspace path to non-existent directory
Then Panel displays error message
And Error message indicates directory not found
And Panel retains previous valid workspace
```


<a id="scenario-workspace-path-persists-after-panel-refresh"></a>
### Scenario: [Workspace path persists after panel refresh](#scenario-workspace-path-persists-after-panel-refresh) (happy_path)

**Steps:**
```gherkin
Given Panel is open showing default workspace c:/dev/project_a
When User changes workspace path to c:/dev/project_b
And Panel displays project_b workspace and state
And User refreshes panel
Then Panel displays c:/dev/project_b as current workspace
And Workspace path was persisted and restored
```


<a id="scenario-set-path-by-dragging-folder-to-panel"></a>
### Scenario: [Set path by dragging folder to panel](#scenario-set-path-by-dragging-folder-to-panel) (happy_path)

**Steps:**
```gherkin
Given Panel is open showing workspace at c:/dev/project_a
And Folder c:/dev/project_b exists in VS Code explorer
When User drags folder c:/dev/project_b from explorer to workspace text entry
Then Workspace text entry displays c:/dev/project_b
And Panel displays c:/dev/project_b as current workspace
And Panel displays behavior action state from project_b
```

