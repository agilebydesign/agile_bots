# LangGraph Orchestration - Increment Exploration

**Navigation:** [📋 Story Map](map/base-bot-story-map.md) | [📊 Increments](increments/story-map-increments.md)

**File Name**: `langgraph-orchestration-exploration.md`
**Location**: `agile_bot/bots/base_bot/docs/stories/langgraph-orchestration-exploration.md`

**Priority:** 9
**Relative Size:** Large

## Increment Purpose

Human developers and AI assistants execute complex multi-step workflows with pause/resume capability and checkpoint management so that workflows can be paused, resumed, and orchestrated with loops, conditionals, and human-in-the-loop interactions.

---

## Domain AC (Increment Level)

### Core Domain Concepts

- BotLangState: TypedDict that defines the state schema for LangGraph execution, containing story_graph, context, parameters, mode, current_action, completed_actions, and instructions
- BotLangActionNode: Wraps action.execute(context) method and provides LangGraph node entry point with two-pass pattern (get_instructions, confirm_with_response) supporting autonomous and interactive execution modes
- StateGraph: LangGraph's graph builder class that defines workflow structure with nodes and edges, compiled with checkpointer for execution
- BotLangFlowRunner: Loads workflow Python files, builds StateGraph, compiles graph with SqliteSaver checkpointer, executes graph with initial BotLangState, and supports resume from checkpoint via thread_id
- Checkpoint: Saves BotLangState with thread_id, restores BotLangState, enables resume capability, and stores checkpoint metadata (timestamp, node name)
- BotLangMode: Determines node execution behavior (autonomous vs interactive), controls AI interaction pattern, and manages workflow pause points
- SqliteSaver: LangGraph's checkpoint storage implementation that persists BotLangState to SQLite database with thread_id isolation
- BotLangFlow: Hand-written Python workflow definition that creates StateGraph with BotLangActionNodes and edges, supporting conditional routing, loops, and state transitions

---

### Domain Behaviors

- BotLangActionNode wraps action execution: Provides LangGraph node entry point via __call__ method and implements two-pass pattern for instructions and confirmation
- StateGraph defines workflow structure: Hand-written Python code that adds BotLangActionNodes and edges to create workflow graph topology
- BotLangFlowRunner executes workflows: Loads workflow Python file, builds StateGraph, compiles with SqliteSaver, and executes with BotLangState
- SqliteSaver manages checkpoints: Saves and restores BotLangState with thread_id for pause/resume capability
- BotLangMode controls node behavior: Determines autonomous (direct AI calls) vs interactive (pause for human) execution
- BotLangState flows through graph: Passed from node to node, updated by BotLangActionNodes, and persisted by SqliteSaver at each checkpoint
- BotLangFlow orchestrates execution: Defines workflow structure with nodes and edges, manages node sequence, conditional routing, and state transitions

---

### Domain Rules

- LangGraph is opt-in via --botlangflow flag: Default behavior/action code path remains untouched, LangGraph code is not invoked without flag
- Checkpoints use SqliteSaver: Checkpoint storage is separate from legacy behavior_action_state.json file
- BotLangActionNode supports two execution modes: Autonomous mode calls AI directly, interactive mode pauses for human input
- BotLangFlow definitions are hand-written Python files: Not generated from behavior.json, defined in orchestration/graphs/ directory
- Checkpoints include thread_id: Enables resume capability by loading checkpoint by thread_id from SqliteSaver
- BotLangState transitions are managed by LangGraph: State updates happen automatically through LangGraph's node execution and checkpointing system
- BotLangState schema is flow-specific: Each BotLangFlow defines its own BotLangState TypedDict schema
- BotLangFlowRunner is bot-specific: Each bot can extend or customize the runner for bot-specific orchestration needs
- BotLangActionNode adds state changes to BotLangState: Each node updates BotLangState with action results before returning to LangGraph

---

## Stories (10 total)

### 📝 Route to Default Behavior Action

**Acceptance Criteria:**
- **When** Bot receives CLI command without --botlangflow flag, **then** Bot routes via the default behavior/action path (existing router/forward logic)
- **When** Bot routes default path, **then** Bot preserves legacy behavior_action_state and activity log behavior
- **When** Bot routes default path, **then** LangGraph state/runner is not invoked
- **When** Bot routes default path, **then** Action receives the original context parameter unchanged

### 📝 Route to BotLangFlow

**Acceptance Criteria:**
- **When** Bot receives CLI command with --botlangflow <botlangflow_name>, **then** Bot detects --botlangflow parameter
- **When** Bot detects --botlangflow, **then** Bot routes to BotLangFlowRunner instead of default behavior/action flow
- **When** Bot routes to BotLangFlowRunner, **then** Bot builds initial BotLangState from CLI context (botlangflow_name, behavior, action, parameters)
- **When** Bot passes botlangflow_name and initial BotLangState to BotLangFlowRunner, **then** BotLangFlowRunner loads the BotLangFlow Python file matching botlangflow_name
- **When** BotLangFlowRunner loads BotLangFlow, **then** BotLangFlowRunner calls the flow's build function to create the StateGraph
- **When** StateGraph is created, **then** BotLangFlowRunner compiles the StateGraph with SqliteSaver checkpointer
- **When** Graph is compiled, **then** BotLangFlowRunner invokes the compiled graph with initial BotLangState and thread_id

### 📝 Invoke BotLangActionNode

**Acceptance Criteria:**
- **When** LangGraph invokes a node in the StateGraph, **then** LangGraph calls the node's __call__ method with current BotLangState
- **When** Node's __call__ is invoked, **then** BotLangActionNode receives BotLangState via __call__ entry point
- **When** BotLangActionNode receives BotLangState, **then** BotLangActionNode extracts behavior/action/context from BotLangState
- **When** BotLangActionNode extracts context, **then** BotLangActionNode invokes action.execute(context) with extracted context
- **When** action.execute completes, **then** BotLangActionNode adds state changes to BotLangState and returns updated BotLangState to LangGraph


### 📝 Prepare Action Instructions

**Acceptance Criteria:**
- **When** BotLangActionNode executes in autonomous or interactive mode, **then** BotLangActionNode calls get_instructions() method
- **When** get_instructions() is called, **then** get_instructions() invokes action.execute(context) to collect instructions
- **When** instructions are collected, **then** Instructions are returned as string ready for AI submission
- **When** Instructions are returned, **then** Action context is included in the instructions

### 📝 Process Bot Behavor Action Instructions Automatically

**Acceptance Criteria:**
- **When** BotLangActionNode executes in autonomous mode, **then** BotLangActionNode calls run_autonomous() method
- **When** run_autonomous() is called, **then** run_autonomous() submits instructions to AI via API client
- **When** Instructions are submitted, **then** BotLangActionNode waits for AI response

### 📝 Process Behavor Action Instructions Through AI Chat

**Acceptance Criteria:**
- **When** BotLangActionNode executes in interactive mode, **then** BotLangActionNode calls run_interactive() method
- **When** run_interactive() is called,  **then** BotLangActionNode returns dict with 'prompt' and 'needs_confirmation' flag
- **When** dict is returned, **then** BotLangFlow execution pauses at the interactive node
- **When** BotLangFlow pauses, **then** SqliteSaver saves checkpoint with BotLangState at the pause point with thread_id
- **When** checkpoint is saved, **then** human can review AI response and provide confirmation or feedback before flow resumes
- **When** human reviews the prompt and confirms or provides feedback, **then** the confirmation/feedback is submitted back to the bot, which is processed by LangGraph And the same bot action node.


### 📝 Confirm Behavor Action Instruction Response
**Acceptance Criteria:**
- **When** AI responds to instructions., **then** BotLangActionNode receives the response and calls confirm_with_response() to process the AI response
- **When** the Node confirm_with_response() 
  **then** the bot behavior action execute is called again with any necessary confirmation / state to save
  **and** action.execute() completes, **then** BotLangActionNode adds state changes to BotLangState with action results
  **and** Node execution completes, **then** LangGraph automatically saves checkpoint after node execution completes
  **and** LangGraph continues execution to the next node in the flow

### 📝 Return to chat and pause for human-in-the-loop Node
**Acceptance Criteria:**
- **When** BotLangFlow includes a dedicated human-in-the-loop node, **then** Node returns instructions/prompt to CLI
- **When** Node returns prompt, **then** CLI outputs prompt to chat interface
- **When** Prompt is output, **then** BotLangFlow execution pauses at that node
- **When** BotLangFlow pauses, **then** SqliteSaver saves checkpoint with BotLangState at pause point with thread_id
- **When** Checkpoint is saved, **then** Human can review prompt and provide response before BotLangFlow resumes

### 📝 Handle Execution Modes

**Acceptance Criteria:**
- **When** BotLangActionNode executes and BotLangState.mode is 'autonomous', **then** BotLangActionNode calls run_autonomous() which submits to AI and continues without pausing
- **When** BotLangActionNode executes and BotLangState.mode is 'interactive', **then** BotLangActionNode calls run_interactive() which returns prompt and pauses BotLangFlow
- **When** run_interactive() is called, **then** run_interactive() returns dict with 'prompt' and 'needs_confirmation' flag
- **When** Prompt is returned, **then** BotLangFlow execution pauses until human provides response via --continue
- **When** BotLangFlow pauses, **then** SqliteSaver preserves BotLangState in checkpoint with thread_id

### 📝 Resume BotLangFlow from Checkpoint

**Acceptance Criteria:**
- **When** User runs CLI with --continue flag and thread_id, **then** BotLangFlowRunner calls resume_from() with thread_id and optional checkpoint_id
- **When** resume_from() is called, **then** BotLangFlowRunner loads checkpoint from SqliteSaver using thread_id
- **When** Checkpoint is loaded, **then** SqliteSaver restores BotLangState from checkpoint
- **When** BotLangState is restored, **then** BotLangFlowRunner invokes compiled graph with restored BotLangState
- **When** Graph is invoked, **then** BotLangFlow continues execution from the paused node
- **When** Human provides response with --continue, **then** Response is added to BotLangState and passed to next node
- **When** Response is passed, **then** BotLangFlow proceeds with updated BotLangState

---


---

## Domain Rules Referenced

- LangGraph is opt-in via --workflow flag (zero breaking changes)
- Checkpoints use separate storage from legacy workflow files
- ActionNode implements two-pass pattern for all behavior/action combinations
- Workflow graphs are hand-written Python files, not generated
- StateAdapter provides base functionality with bot-specific extensions
- Execution modes determine autonomous vs interactive behavior

---

## Source Material

**Shape phase:**
- Primary source: `langgraph-orchestration.md` - Complete architecture and implementation plan
- Sections referenced: Architecture, Node Execution Model, Implementation Plan, Directory Structure
- Date generated: 2025-12-22
- Context note: LangGraph integration as optional orchestration layer

**Discovery phase:**
- Reads source from Shape phase
- Discovery Refinements: Elaborated on ActionNode responsibilities, BehaviorGraphBuilder workflow creation, LangGraphRunner checkpoint management, StateAdapter state loading patterns
- Additional sections referenced: State Files, Execution Flows, Node Execution Model

**Exploration phase:**
- Inherits source from story map
- Acceptance criteria added for the 7 LangGraph orchestration stories in increment 9
- Domain concepts refined: Added Checkpoint, ExecutionMode, LangGraph Workflow concepts
- Focus: Behavioral acceptance criteria for workflow orchestration, checkpoint management, and execution mode handling

