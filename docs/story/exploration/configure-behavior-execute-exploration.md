# Perform Behavior Action In Bot Workflow - Increment Exploration (Configure Behavior Execute)

**Navigation:** [📋 Story Map](../map/story-map-outline.drawio) | [📊 Increments](../prioritization/story-map-increments.drawio)

## Stories (1 total)

### 📝 Configure Behavior Execute

**Acceptance Criteria:**
- **WHEN** User sets behavior execute to skip in Panel behavior dropdown
  **AND** User executes that behavior
  **THEN** Panel skips all actions in that behavior regardless of per-action setting
  **BUT** does not run any action

- **WHEN** User sets behavior execute to auto in Panel
  **AND** User executes that behavior
  **THEN** Panel runs auto and manual actions
  **AND** Panel skips actions marked skip

- **WHEN** User sets behavior execute to manual in Panel
  **AND** User executes that behavior
  **THEN** Panel performs each action according to that action's skip/auto/manual setting

- **WHEN** User runs cli.behaviors.shape.set_execute auto
  **THEN** CLI sets behavior execute to auto for that behavior

---

## Source Material

- docs/story/story-graph.json
- docs/story/clarification.json (exploration key)
- docs/story/strategy.json (exploration key)
- src/panel/behaviors_view.js
- src/cli/cli_session.py
- docs/story/bot_workspace.json
