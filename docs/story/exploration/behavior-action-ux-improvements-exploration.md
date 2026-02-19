# Behavior Action Ux Improvements - Increment Exploration

**Navigation:** [📋 Story Map](../map/story-map-outline.drawio) | [📊 Increments](../prioritization/story-map-increments.drawio)



## Stories (5 total)

### Configure Action Execution

**Acceptance Criteria:**
- **WHEN** User opens behavior in Panel
  **THEN** Panel shows list of actions for that behavior
  **AND** Panel shows a toggle button group (Auto | Skip | Manual) per action

- **WHEN** User sets action to Skip via toggle
  **AND** User executes that behavior
  **THEN** Panel skips that action

- **WHEN** User sets action to Auto via toggle
  **AND** User executes that behavior
  **THEN** Panel executes that action as soon as previous action completes

- **WHEN** User sets action to Manual via toggle
  **AND** User executes that behavior
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
  **THEN** Panel runs auto and manual actions
  **AND** Panel skips actions marked skip

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
  **THEN** CLI stores that instruction for shape.clarify
  **AND** CLI includes it in next prompt

### Render as Part of Build and Validate Actions

**Acceptance Criteria:**

- **WHEN** User runs build from Panel
  **THEN** Panel invokes CLI (e.g. cli.behaviors.shape.build)
  **AND** CLI subscribes to story-graph with debounce and runs build
  **AND** CLI reports BuildInProcess while build is running
  **AND** Panel watches CLI for status and shows BuildInProcess indicator
  **AND** CLI is watching story-graph; when save is detected and debounce passes CLI starts render
  **AND** CLI reports RenderInProcess while render is running
  **AND** Panel shows RenderInProcess indicator
  **AND** when render finishes successfully CLI reports completion and Panel shows completion indicator (e.g. checkmark)
  **AND** when build or render fails CLI reports failed and Panel shows failed indicator
  **AND** Panel periodically refreshes images so User sees updated render output
  **AND** Panel is passive: it does not own the subscription or render trigger; CLI does

- **WHEN** User runs validate from Panel
  **THEN** Panel invokes CLI (e.g. cli.behaviors.shape.validate)
  **AND** CLI runs validate and watches validation status (updated periodically) for ValidationInProcess
  **AND** CLI reports ValidationInProcess while validate is running
  **AND** Panel watches CLI for status and shows ValidationInProcess indicator
  **AND** validation report is written only at end; when save of validation report is detected and debounce passes CLI starts render
  **AND** CLI reports RenderInProcess while render is running
  **AND** Panel shows RenderInProcess indicator
  **AND** when render finishes successfully CLI reports completion and Panel shows completion indicator
  **AND** when validate or render fails CLI reports failed and Panel shows failed indicator
  **AND** Panel periodically refreshes images
  **AND** Panel is passive: it does not own the subscription or render trigger; CLI does

- **WHEN** User runs build or validate from CLI (no Panel)
  **THEN** the same CLI flow runs
  **AND** for build CLI subscribes to story-graph
  **AND** for validate CLI watches validation status (periodic) and validation report (at end)
  **AND** CLI runs the action
  **AND** CLI reports BuildInProcess or ValidationInProcess
  **AND** when save of output is detected and debounce passes CLI starts render
  **AND** CLI reports RenderInProcess
  **AND** when done CLI reports completion or failed
  **AND** CLI reports to the terminal so the flow works without Panel

### Render Diagram Selected Node

**Acceptance Criteria:**
- **WHEN** User selects story node in Panel story tree
  **THEN** Panel action bar shows [Render diagram] [Save layout] [Clear layout] [Update graph] buttons

- **WHEN** User clicks [Render diagram] in Panel
  **THEN** Panel renders diagram for selected node scope

- **WHEN** User clicks [Save layout] in Panel
  **THEN** Panel persists layout to DrawIO file

- **WHEN** User clicks [Update graph] in Panel
  **THEN** Panel generates update report
  **AND** Panel applies changes to story-graph.json

- **WHEN** User runs cli.story_graph."Invoke Bot"."Act With Selected Node".render_diagram
  **THEN** CLI renders diagram for current scope
  **AND** CLI reports completion

---

## Source Material

Story graph: `docs/story/story-graph.json`
Increment: Behavior Action Ux Improvements (priority 7)
Scope: Configure Action Execution, Configure Behavior Execute, Add Special Instructions, Render as Part of Build and Validate Actions, Render Diagram Selected Node
