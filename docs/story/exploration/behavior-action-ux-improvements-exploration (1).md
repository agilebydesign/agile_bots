# Behavior Action Ux Improvements - Increment Exploration

**Navigation:** [📋 Story Map](../map/story-map-outline.drawio) | [📊 Increments](../prioritization/story-map-increments.drawio)



## Stories (5 total)

### Configure Action Execution

**Acceptance Criteria:**
- **WHEN** User opens behavior in Panel
  **THEN** Panel shows list of actions for that behavior AND Panel shows a toggle button group (Auto | Skip | Manual) per action
- **WHEN** User sets action to Skip via toggle
  **AND** User executes that behavior
  **THEN** Panel skips that action
- **WHEN** User sets action to Auto via toggle
  **THEN** Panel executes that action as soon as previous action completes
- **WHEN** User sets action to Manual via toggle
  **THEN** Panel requires User to click Execute for that action
- **WHEN** User runs cli.behaviors.shape.clarify.set_execution auto
  **THEN** CLI sets that action to auto execution

### Configure Behavior Execute

**Acceptance Criteria:**
- **WHEN** User sets behavior execute to skip in Panel behavior dropdown
  **AND** User executes that behavior
  **THEN** Panel skips all actions in that behavior regardless of per-action setting
- **WHEN** User sets behavior execute to auto in Panel
  **AND** User executes that behavior
  **THEN** Panel runs auto and manual actions AND Panel skips actions marked skip
- **WHEN** User sets behavior execute to manual in Panel
  **AND** User executes that behavior
  **THEN** Panel performs each action according to that action's skip/auto/manual setting
- **WHEN** User runs cli.behaviors.shape.set_execute auto
  **THEN** CLI sets behavior execute to auto for that behavior

### Add Special Instructions

**Acceptance Criteria:**
- **WHEN** User enters text in Panel behavior-level Special Instructions text area (beside shape, after toggle group above)
  **THEN** Panel stores that text for that behavior
- **WHEN** User enters text in Panel action-level Special Instructions text area (e.g. beside shape.clarify, same row)
  **THEN** Panel stores that text for that behavior and action
- **WHEN** User clicks Submit in Panel
  **THEN** Panel injects all special instructions from behavior and action levels into the prompt
- **WHEN** User runs cli.behaviors.shape.clarify.special_instructions "focus on edge cases"
  **THEN** CLI stores that instruction for shape.clarify AND CLI includes it in next prompt

### Render as Part of Build and Validate Actions

**Acceptance Criteria:**
- **WHEN** User starts a build (from CLI or Panel)
  **THEN** CLI subscribes to story-graph (e.g. file watcher or VS Code onDidSaveTextDocument when in editor) with debounce (e.g. 500 ms with no further saves)
- **WHEN** save of story-graph is detected
  **AND** debounce delay passes with no further saves
  **THEN** CLI understands build has finished (whether file was updated by CLI, AI, or editor) AND CLI starts render
- **WHEN** build runs and Panel is open
  **THEN** Panel shows BuildInProcess indicator AND Panel periodically checks (e.g. polls) to refresh images so User sees updated render output; Panel is passive and does not own subscription or render trigger
- **WHEN** User starts a validate (from CLI or Panel)
  **THEN** CLI subscribes to violation report output (e.g. file watcher or onDidSaveTextDocument when in editor) with debounce (e.g. 500 ms with no further saves)
- **WHEN** save of violation report is detected
  **AND** debounce delay passes with no further saves
  **THEN** CLI understands validation has finished (whether file was updated by CLI, AI, or editor) AND CLI starts render
- **WHEN** validate runs and Panel is open
  **THEN** Panel shows ValidationInProcess indicator AND Panel periodically checks to refresh images; Panel is passive and does not own subscription or render trigger
- **WHEN** render starts (driven by CLI)
  **THEN** CLI reports RenderInProcess; Panel shows RenderInProcess indicator if open
- **WHEN** render completes
  **THEN** CLI reports completion; Panel shows completion indicator (e.g. checkmark) if open
- **WHEN** User runs cli.behaviors.shape.build
  **THEN** CLI subscribes to story-graph, runs build, on save+debounce CLI starts render, CLI reports BuildInProcess then RenderInProcess then completion so flow works directly through CLI without Panel
- **WHEN** User runs validate (e.g. cli.behaviors.shape.validate)
  **THEN** CLI subscribes to violation report, runs validate, on save+debounce of violation report CLI starts render, CLI reports ValidationInProcess then RenderInProcess then completion so flow works directly through CLI without Panel

  

### Render Diagram Selected Node

**Acceptance Criteria:**
- **WHEN** User selects story node in Panel story tree
  **THEN** Panel action bar shows [Render diagram] [Save layout] [Clear layout] [Update graph] buttons
- **WHEN** User clicks [Render diagram] in Panel
  **THEN** Panel renders diagram for selected node scope
- **WHEN** User clicks [Save layout] in Panel
  **THEN** Panel persists layout to DrawIO file
- **WHEN** User clicks [Update graph] in Panel
  **THEN** Panel generates update report AND Panel applies changes to story-graph.json
- **WHEN** User runs cli.story_graph."Invoke Bot"."Act With Selected Node".render_diagram
  **THEN** CLI renders diagram for current scope AND CLI reports completion

---

## Source Material

Story graph: `docs/story/story-graph.json`  
Increment: Behavior Action Ux Improvements (priority 7)  
Scope: Configure Action Execution, Configure Behavior Execute, Add Special Instructions, Render as Part of Build and Validate Actions, Render Diagram Selected Node
