# 📄 Render as Part of Build and Validate Actions

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/test_render_content.py)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Render Content](.)  
**Sequential Order:** 7.0
**Story Type:** user

## Story Description

Render as Part of Build and Validate Actions functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User runs build from Panel
  **then** Panel invokes CLI (e.g. cli.behaviors.shape.build)
  **and** CLI subscribes to story-graph with debounce and runs build
  **and** CLI reports BuildInProcess while build is running
  **and** Panel watches CLI for status and shows BuildInProcess indicator
  **and** CLI is watching story-graph; when save is detected and debounce passes CLI starts render
  **and** CLI reports RenderInProcess while render is running
  **and** Panel shows RenderInProcess indicator
  **and** when render finishes successfully CLI reports completion and Panel shows completion indicator (e.g. checkmark)
  **and** when build or render fails CLI reports failed and Panel shows failed indicator
  **and** Panel periodically refreshes images so User sees updated render output
  **and** Panel is passive: it does not own the subscription or render trigger; CLI does

- **When** User runs validate from Panel
  **then** Panel invokes CLI (e.g. cli.behaviors.shape.validate)
  **and** CLI runs validate and watches validation status (updated periodically) for ValidationInProcess
  **and** CLI reports ValidationInProcess while validate is running
  **and** Panel watches CLI for status and shows ValidationInProcess indicator
  **and** validation report is written only at end; when save of validation report is detected and debounce passes CLI starts render
  **and** CLI reports RenderInProcess while render is running
  **and** Panel shows RenderInProcess indicator
  **and** when render finishes successfully CLI reports completion and Panel shows completion indicator
  **and** when validate or render fails CLI reports failed and Panel shows failed indicator
  **and** Panel periodically refreshes images
  **and** Panel is passive: it does not own the subscription or render trigger; CLI does

- **When** User runs build or validate from CLI (no Panel)
  **then** the same CLI flow runs
  **and** for build CLI subscribes to story-graph
  **and** for validate CLI watches validation status (periodic) and validation report (at end)
  **and** CLI runs the action
  **and** CLI reports BuildInProcess or ValidationInProcess
  **and** when save of output is detected and debounce passes CLI starts render
  **and** CLI reports RenderInProcess
  **and** when done CLI reports completion or failed
  **and** CLI reports to the terminal so the flow works without Panel

## Scenarios

### Scenario: Render as Part of Build and Validate Actions (happy_path)

**Steps:**
```gherkin
Given system is ready
When action executes
Then action completes successfully
```
