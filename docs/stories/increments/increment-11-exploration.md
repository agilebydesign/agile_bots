# REPL All Scope Parameters (Mock Backend) - Increment Exploration

**Navigation:** [Story Map](./map/story-map-outline.drawio) | [Increments](./increments/story-map-increments.txt)

**File Name**: `increment-11-exploration.md`
**Location**: `agile_bot/bots/base_bot/docs/stories/increment-11-exploration.md`

**Priority:** 11
**Relative Size:** Medium (16 stories)

---

## Increment Purpose

Delivers complete REPL user experience with real bot integration (test_story_bot) and stubbed action execution so that users can navigate workflows, set scope parameters, and execute operations without actual file saves or scanner runs.

---

## Domain AC (Increment Level)

### Core Domain Concepts

- **REPLSession**: Manages interactive session state and command processing
- **Scope**: Typed scope parameters (type, value, exclude) from `ActionContext`
- **ActionOperations**: Three-phase execution (instructions, submit, confirm)
- **BehaviorActionState**: Persisted workflow position and scope

### Domain Behaviors

- REPLSession routes commands to Bot
- Bot locates Behaviors and Actions
- Bot builds ActionContext with scope for Action execution
- BehaviorActionState persists workflow position and scope across commands

### Domain Rules

- Scope must be parsed before action execution
- Actions have three operations: instructions, submit, confirm
- test_story_bot provides real structure, stubbed execution
- State persists between REPL commands

---

## Stories (15 total)

### 1. Show Available Behaviors and Actions
**User:** REPLSession | **Type:** system

**Acceptance Criteria:**
- WHEN REPLSession starts with Bot
  THEN REPLSession displays Bot's available Behaviors
- WHEN user selects Behavior
  THEN REPLSession displays Behavior's available Actions
- WHEN actions are listed
  THEN Actions come from current Behavior

---

### 2. Navigate To Behavior
**User:** User | **Type:** user

**Acceptance Criteria:**
- WHEN user enters behavior name
  THEN REPLSession routes command to Bot
- WHEN Bot receives behavior navigation
  THEN Bot locates Behavior by name
  AND Bot updates BehaviorActionState with new current behavior
- WHEN Behavior is set as current
  THEN Bot executes first Action's instruction operation
  AND Bot returns Result with instructions
- WHEN REPLSession receives Result
  THEN REPLSession displays instructions to user

---

### 3. Navigate To Action
**User:** User | **Type:** user

**Acceptance Criteria:**
- WHEN user enters action name
  THEN REPLSession routes command to Bot
- WHEN Bot receives action navigation
  THEN Bot locates Action within current Behavior
  AND Bot updates BehaviorActionState with new current action
- WHEN Action is set as current
  THEN Bot executes Action's instruction operation
  AND Bot returns Result with instructions
- WHEN REPLSession receives Result
  THEN REPLSession displays instructions to user

---

### 4. Request Help
**User:** User | **Type:** user

**Acceptance Criteria:**
- WHEN user enters help command
  THEN REPLSession routes to Bot for help content
- WHEN Bot receives general help request
  THEN Bot gathers available commands, Behaviors, and current Behavior's Actions
  AND Bot returns Result with help overview
- WHEN REPLSession receives help Result
  THEN REPLSession displays available commands, Behaviors, and Actions

---

### 5. Request Status
**User:** User | **Type:** user

**Acceptance Criteria:**
- WHEN user enters status command
  THEN REPLSession routes to Bot for status
- WHEN Bot receives status request
  THEN Bot reads current BehaviorActionState
  AND Bot assembles current Behavior, Action, and scope into Result
- WHEN REPLSession receives status Result
  THEN REPLSession displays current Behavior and Action
- WHEN scope has been set for current Behavior/Action
  THEN REPLSession displays current scope 
- WHEN no scope has been set
  THEN REPLSession displays "No scope set"

---

### 6. Provide Context For Instructions
**User:** REPLSession | **Type:** system

**Acceptance Criteria:**
- WHEN user requests instructions operation
  THEN REPLSession gathers parameters from user input
- WHEN REPLSession has raw parameters
  THEN REPLSession parses parameters according to ActionContext schema
- WHEN parameters are parsed
  THEN REPLSession validates parameters against ActionContext requirements
- WHEN validation passes
  THEN REPLSession builds ActionContext with validated parameters
  AND REPLSession passes context to Bot for instruction operation
- WHEN validation fails
  THEN REPLSession displays validation errors to user
- WHEN user requests instructions without scope parameter
  AND REPLSession does not add stored scope to ActionContext
- WHEN BOT Retrieves action context from REPLSession that does not have scope added
  AND BOT has stored scope from the previous action.
  THEN BOT adds stored scope to ActionContext before processing it further

---

### 7. Provide Story Scope Context For Instructions
**User:** REPLSession | **Type:** system

**Acceptance Criteria:**
- WHEN user runs instructions command with story scope parameter
  THEN REPLSession gathers story scope parameters from command
  AND REPLSession parses scope type and values and validates it against Story Scope schema
  AND REPLSession creates a new Story Scope from the parameters
  AND REPLSession adds the new Story Scope to the Action Context
  AND passes the Action Context with Scope to the instruction operation
- WHEN validation fails
  THEN REPLSession displays story scope validation errors to user

---

### 8. Provide File Scope Context For Instructions
**User:** REPLSession | **Type:** system

**Acceptance Criteria:**
- WHEN user runs instructions command with file scope parameter
  THEN REPLSession gathers file scope parameters from command
  AND REPLSession parses file paths and validated it against File Scope schema
  AND REPLSession creates and new File Scope from the parameters
  AND REPLSession adds the new File Scope it to the Action Context
  AND passes the Action Context with Scope to the instruction operation
- WHEN validation fails
  THEN REPLSession displays file scope validation errors to user

---

### 9. Store Scope Context
**User:** Bot | **Type:** system

**Acceptance Criteria:**
- WHEN Bot receives Scope in context
  THEN Bot stores scope in BehaviorActionState
- WHEN BehaviorActionState is updated
  THEN Bot persists state to storage
- WHEN state is persisted
  THEN scope is available for subsequent action executions

---

### 10. Get Instructions and Display
**User:** User | **Type:** user

**Acceptance Criteria:**
- WHEN user requests instructions
  THEN REPLSession routes to Bot
- WHEN Bot receives instructions request
  THEN Bot delegates to current Action with ActionContext
  AND Action returns instructions
- WHEN Bot receives Action result
  THEN Bot returns Result to REPLSession for display

---

### 11. Submit Action and Display Results
**User:** User | **Type:** user

**Acceptance Criteria:**
- WHEN user enters submit command
  THEN REPLSession routes to Bot
- WHEN Bot receives submit
  THEN Bot delegates to current Action for submission
  AND Action processes submission (stubbed - no file writes)
- WHEN Action completes submission
  THEN Bot returns Result with submission summary to REPLSession for display

---

### 12. Confirm Action and Display Results
**User:** User | **Type:** user

**Acceptance Criteria:**
- WHEN user enters confirm command
  THEN REPLSession routes to Bot
- WHEN Bot receives confirm
  THEN Bot delegates to current Action for confirmation
  AND Action validates and confirms work
- WHEN confirmation succeeds
  THEN Bot returns Result with next action info to REPLSession for display
  AND Bot navigates to next action and returns instructions
  AND REPLSession returns result for display

---

### 13. Advance To Next Action
**User:** Bot | **Type:** system

**Acceptance Criteria:**
- WHEN current action is confirmed complete
  THEN Bot advances to next action in Behavior
- WHEN current action is last in Behavior
  THEN Bot advances to next Behavior's first action
- WHEN workflow position changes
  THEN Bot persists updated BehaviorActionState

---

### 14. Loop Back To Display State
**User:** REPLSession | **Type:** system

**Acceptance Criteria:**
- WHEN command execution completes
  THEN REPLSession gets state from Bot
  AND REPLSession displays current position
  AND REPLSession shows status before prompt
  AND REPLSession awaits next user input

---

### 15. Show Current Behavior Action Help
**User:** User | **Type:** user

**Acceptance Criteria:**
- WHEN user has navigated to a Behavior and Action
  AND user requests help
  THEN REPLSession routes help request to Bot
- WHEN Bot receives help request
  THEN Bot gathers current Behavior details
  AND Bot gathers current Action details
  AND Bot assembles parameters specific to Behavior/Action combination
- WHEN Bot returns help Result
  THEN REPLSession displays Behavior context
  AND REPLSession displays Action description
  AND REPLSession displays available parameters for this Behavior/Action

---

## Consolidation Decisions

- Merged scope parameter stories (basic, story, file) into single flow with different scope types
- Operations (instructions, submit, confirm) replace single "execute" concept
- Real bot integration uses test_story_bot with stubbed action internals
- Deleted redundant "Show Workflow Hierarchy Via Status Command" (merged into Request Status)
- Deleted "Execute Mock Action and Display Results" (replaced by operation-based stories)
- Deleted "Set Scope Parameter" (replaced by new scope context stories)
- Deleted "Enter Confirm Results" (duplicate of Confirm Action and Display Results)

---

## Delta from Increment 10

| Area | Increment 10 (Mock) | Increment 11 (Real Bot) |
|------|---------------------|-------------------------|
| Bot | Fake structure | Real Bot with Behaviors and Actions |
| Behaviors | Mock list | Bot's actual Behaviors |
| Actions | Mock list | Behavior's actual Actions |
| Parameters | Hardcoded display | Action's parameter metadata |
| Scope | Simple string | Scope domain object |
| State | Simple dict | BehaviorActionState with persistence |
| Execution | Mock message | Action execution (stubbed internals) |

---

## Source Material

- **Phase:** Exploration
- **Source:** story-graph.json, priority 11 increment
- **Templates:** story-graph-explored.json, story-exploration.md
- **Rules:** /story_bot-exploration-rules
- **Date Generated:** 2024-12-23
- **Context Note for Discovery:** This increment bridges mock REPL (Increment 10) with real backend (Increment 12) by using real bot structure with stubbed execution

