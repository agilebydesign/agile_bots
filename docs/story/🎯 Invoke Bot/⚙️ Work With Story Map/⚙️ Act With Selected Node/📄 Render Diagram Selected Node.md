# 📄 Render Diagram Selected Node

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/edit_story_map/test_submit_scoped_action.py)

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

### Scenario: Render Diagram Selected Node (happy_path)

**Steps:**
```gherkin
Given system is ready
When action executes
Then action completes successfully
```
