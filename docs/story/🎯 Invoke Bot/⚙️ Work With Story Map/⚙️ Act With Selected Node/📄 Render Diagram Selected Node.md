# 📄 Render Diagram Selected Node

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/edit_story_map/test_submit_scoped_action.py#L1669)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Act With Selected Node](.)  
**Sequential Order:** 5.0
**Story Type:** user

## Story Description

Render Diagram Selected Node functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User selects story node in Panel story tree
  **then** Panel action bar shows [Render diagram] [Save layout] [Clear layout] [Update graph] buttons

- **When** User clicks [Render diagram] in Panel
  **then** Panel renders diagram for selected node scope

- **When** User clicks [Save layout] in Panel
  **then** Panel persists layout to DrawIO file

- **When** User clicks [Update graph] in Panel
  **then** Panel generates update report
  **and** Panel applies changes to story-graph.json

- **When** User runs cli.story_graph."Invoke Bot"."Act With Selected Node".render_diagram
  **then** CLI renders diagram for current scope
  **and** CLI reports completion

## Scenarios

<a id="scenario-panel-action-bar-successfully-shows-diagram-buttons-when-storynode-selected"></a>
### Scenario: [Panel action bar successfully shows diagram buttons when StoryNode selected](#scenario-panel-action-bar-successfully-shows-diagram-buttons-when-storynode-selected) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_submit_scoped_action.py#L1675)

**Steps:**
```gherkin
Given StoryNode is selected in StoryMap tree
When Panel displays action bar for selected node
Then Panel shows Render diagram, Save layout, Clear layout, Update graph buttons
```


<a id="scenario-panel-renders-diagram-for-selected-node-scope"></a>
### Scenario: [Panel renders diagram for selected node scope](#scenario-panel-renders-diagram-for-selected-node-scope) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_submit_scoped_action.py#L1687)

**Steps:**
```gherkin
Given StoryNode is selected in StoryMap tree
When User clicks Render diagram in Panel
Then Panel renders diagram for selected node scope
```


<a id="scenario-panel-persists-layout-to-drawio-file"></a>
### Scenario: [Panel persists layout to DrawIO file](#scenario-panel-persists-layout-to-drawio-file) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_submit_scoped_action.py#L1697)

**Steps:**
```gherkin
Given StoryNode is selected and diagram is rendered
When User clicks Save layout in Panel
Then Panel persists layout to DrawIO file
```


<a id="scenario-panel-generates-update-report-and-applies-changes-to-story-graph"></a>
### Scenario: [Panel generates update report and applies changes to story graph](#scenario-panel-generates-update-report-and-applies-changes-to-story-graph) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_submit_scoped_action.py#L1707)

**Steps:**
```gherkin
Given Diagram has changes from StoryMap
When User clicks Update graph in Panel
Then Panel generates UpdateReport
And Panel applies changes to story-graph.json
```


<a id="scenario-cli-renders-diagram-for-current-scope-and-reports-completion"></a>
### Scenario: [CLI renders diagram for current scope and reports completion](#scenario-cli-renders-diagram-for-current-scope-and-reports-completion) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_submit_scoped_action.py#L1719)

**Steps:**
```gherkin
Given scope is set to Act With Selected Node path
When User runs cli.story_graph render_diagram
Then CLI renders diagram for current scope
And CLI reports completion
```


<a id="scenario-diagram-renders-for-empty-storynode-scope"></a>
### Scenario: [Diagram renders for empty StoryNode scope](#scenario-diagram-renders-for-empty-storynode-scope) (edge_case)  | [Test](/test/invoke_bot/edit_story_map/test_submit_scoped_action.py#L1738)

**Steps:**
```gherkin
Given StoryNode scope is empty
When User clicks Render diagram in Panel
Then Panel renders diagram with empty layout
```


<a id="scenario-diagram-render-fails-when-storynode-not-found"></a>
### Scenario: [Diagram render fails when StoryNode not found](#scenario-diagram-render-fails-when-storynode-not-found) (error_case)  | [Test](/test/invoke_bot/edit_story_map/test_submit_scoped_action.py#L1749)

**Steps:**
```gherkin
Given StoryNode is not in StoryMap
When User clicks Render diagram in Panel
Then Panel reports error and does not render
```

