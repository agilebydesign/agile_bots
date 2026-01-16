# Increment 11 Implementation Plan
## "REPL All Scope Parameters (Mock Backend)" - Complete User Experience

**Created:** 2024-12-23  
**Status:** Planning  
**Goal:** Create complete user experience with real bot, stubbed execution (no saves/renders/scanners)

---

## Overview

Increment 11 focuses on creating a complete REPL user experience where:
- Navigation and parameters work with a **real bot** (`test_story_bot`)
- Action execution uses **stubbed operations** (no file saves, no scanner runs)
- Actions are refactored to have **three operations**: `instructions`, `submit`, `confirm`
- **Output uses real rendering** - formatters and output builders from legacy CLI for proper display

**Goal**: Make this look as close to the **real production experience** as possible. The only things stubbed are the actual save/scan operations - everything else (navigation, parameters, rendering, formatting) should be production-quality.

---

## Increment 11 Stories (17 Total)

From `story-graph.json` priority 11:

1. Show Available Behaviors and Actions
2. Navigate To Behavior
3. Navigate To Action
4. Request Help
5. Request Status
6. Provide Context For Instructions *(NEW)*
7. Provide Story Scope Context For Instructions *(NEW)*
8. Provide File Scope Context For Instructions *(NEW)*
9. Store Scope Context *(NEW)*
10. Get Instructions and Display *(NEW)*
11. Submit Action and Display Results *(NEW)*
12. Confirm Action and Display Results *(NEW)*
13. Enter Confirm Results
14. Advance To Next Action
15. Loop Back To Display State
16. Show Action Parameter Help
17. Format CLI Output For Chat *(NEW)*

---

## Prerequisite: Reuse Legacy CLI Patterns

Before implementation, review and reuse existing CLI helper classes. These have been well-tested and should be leveraged in the REPL implementation.

### CLI Helpers to Reuse (from `src/cli/`)

| Class | Purpose | Reuse In REPL |
|-------|---------|---------------|
| **CliContextBuilder** | Builds typed ActionContext from CLI args, parses Scope | Scope parameter handling in REPL |
| **CliParameterParser** | Parses CLI arguments, handles JSON scope, key=value pairs | REPL command parsing |
| **CliCommandRouter** | Routes to behaviors/actions, executes with context | REPL action execution |
| **CliTerminalFormatter** | Formats output (headers, errors, status markers) | REPL display formatting, pipe mode output |
| **ActionDataCollector** | Collects action metadata, parameters, descriptions | REPL help/parameter display |
| **DescriptionExtractor** | Extracts descriptions from behavior/action configs | REPL help text |
| **ParameterInfoBuilder** | Builds parameter info with placeholders | REPL parameter prompts |
| **TypeHintConverter** | Converts Python type hints to CLI types | REPL parameter type display |

### Visitor Patterns to Reuse

| Visitor | Purpose | Reuse In REPL |
|---------|---------|---------------|
| **CliHelpRendererVisitor** | Renders help output for behaviors/actions | REPL help command |
| **CliCodeVisitor** | Generates CLI code | Generator for REPL commands |
| **CommandFileVisitor** | Generates Cursor command files | Generator for REPL shortcuts |

### Key Classes to Import/Extend in REPL

```python
# In repl_cli modules, reuse these patterns:

from agile_bot.bots.base_bot.src.cli.cli_context_builder import CliContextBuilder
from agile_bot.bots.base_bot.src.cli.cli_parameter_parser import CliParameterParser
from agile_bot.bots.base_bot.src.cli.formatter import CliTerminalFormatter
from agile_bot.bots.base_bot.src.cli.action_data_collector import ActionDataCollector
from agile_bot.bots.base_bot.src.actions.action_context import Scope, ScopeType
```

### Scope Handling Pattern (from CliContextBuilder)

```python
# Existing scope parsing logic to reuse:
def _parse_scope_config(self, json_str: str) -> Optional[Scope]:
    if not json_str:
        return None
    data = json.loads(json_str.replace("'", '"'))
    return Scope.from_dict(data)
```

### Parameter Parsing Pattern (from CliParameterParser)

```python
# Existing patterns for:
# - Parsing key=value pairs
# - Handling JSON dict syntax (scope parameter)
# - File path detection
# - Context argument handling
```

### Existing REPL CLI Modules (in `src/repl_cli/`)

| Module | Purpose | Status |
|--------|---------|--------|
| `repl_session.py` | REPL session state management | Exists - extend for scope |
| `repl_commands/` | Command handlers (navigation, workflow, meta) | Exists - add scope commands |
| `repl_status.py` | Status display | Exists - add scope display |
| `repl_help.py` | Help display | Exists - leverage ActionDataCollector |
| `repl_results.py` | Result types (REPLStateDisplay, REPLCommandResponse) | Exists - extend for operations |

### Integration Points

1. **Scope Parameters**: 
   - Use `CliContextBuilder._parse_scope_config()` for parsing
   - Use `Scope` dataclass for storage
   - Store in `BehaviorActionState` for persistence

2. **Parameter Display**:
   - Use `ActionDataCollector.get_action_parameters()` for parameter list
   - Use `ActionDataCollector.get_parameter_descriptions()` for help text

3. **Help Rendering**:
   - Use `CliTerminalFormatter` for consistent formatting
   - Use `CliHelpRendererVisitor` pattern for structured output

4. **Command Routing**:
   - Use `CliCommandRouter` pattern for action execution
   - Extend with operation-specific routing (`instructions`, `submit`, `confirm`)

5. **Pipe Mode Output (Format CLI Output For Chat)**:
   - When stdin is NOT a TTY (pipe mode), format output for AI chat consumption
   - Use `CliTerminalFormatter` for structured markdown output
   - Use `CliHelpRendererVisitor` patterns for help/status rendering
   - Output must be properly formatted for AI to display to user

---

## Step 1: Rationalize Stories

### 1.1 Stories to DELETE from story-graph.json

These stories exist in the story-graph but are NOT in any increment:

| Story Name | Location | Reason |
|------------|----------|--------|
| Show Workflow Hierarchy Via Status Command | ~line 4212 | Redundant with "Request Status" |
| Execute Mock Action and Display Results | ~line 5062 | Replaced by operation-based stories |
| Set Scope Parameter | ~line 4563 | Replaced by new scope context stories |

### 1.2 Stories to RENAME in story-graph.json

| Current Name | New Name (from increment) |
|--------------|---------------------------|
| Display Behaviors and Actions on Startup | Show Available Behaviors and Actions |
| Navigate with Back/Next/Current | Navigate Within Behavior |

### 1.3 Stories to CREATE in story-graph.json

New stories for Increment 11 (need full definitions):

1. **Provide Context For Instructions**
   - User: User
   - Type: user
   - Purpose: Load base context from BehaviorActionState for instructions call

2. **Provide Story Scope Context For Instructions**
   - User: User
   - Type: user
   - Purpose: Accept story scope parameters (scope.type=story, scope.value=['Story Name'])

3. **Provide File Scope Context For Instructions**
   - User: User
   - Type: user
   - Purpose: Accept file scope parameters (scope.type=files, scope.value=['path'], scope.exclude=['pattern'])

4. **Store Scope Context**
   - User: CLI
   - Type: system
   - Purpose: Persist scope parameters to BehaviorActionState

5. **Get Instructions and Display**
   - User: User
   - Type: user
   - Purpose: Call action.get_instructions(context), display formatted results

6. **Submit Action and Display Results**
   - User: User
   - Type: user
   - Purpose: Call action.submit(context), display success (stubbed saves)

7. **Confirm Action and Display Results**
   - User: User
   - Type: user
   - Purpose: Call action.confirm(context), mark complete, show next action

8. **Display Confirm and Continue Prompt** *(if not exists)*
   - User: CLI
   - Type: system
   - Purpose: Show prompt after execution with next action option

9. **Loop Back To Display State** *(if not exists)*
   - User: CLI
   - Type: system
   - Purpose: Return to state display after command execution

10. **Format CLI Output For Chat**
    - User: CLI
    - Type: system
    - Purpose: Format REPL output for AI chat consumption (pipe mode)
    - Notes: When not in TTY mode but in pipe mode, use formatters and output builders from legacy CLI for proper rendered output that AI can display to user

---

## Step 2: Exploration (Acceptance Criteria)

**CRITICAL**: Exploration is a two-phase process:
1. **Phase 2A**: Update `story-graph.json` with acceptance criteria (following template)
2. **Phase 2B**: Render increment exploration document (using proper template)

### Phase 2A: Update story-graph.json

Before rendering any documents, update each story in `story-graph.json` with acceptance criteria following the `story-graph-explored.json` template pattern.

#### Execute Exploration Rules First

```bash
python agile_bot/bots/story_bot/src/story_bot_cli.py --behavior exploration --action rules --message "Guide me to write acceptance criteria for Increment 11 stories following all exploration rules"
```

**MANDATORY**: Follow ALL rules from `/story_bot-exploration-rules` when updating the story graph.

#### Acceptance Criteria Format (from template)

```json
{
  "name": "Story Name",
  "sequential_order": 1,
  "connector": null,
  "users": ["User"],
  "story_type": "user",
  "optional": false,
  "priority": 11,
  "Steps": null,
  "acceptance_criteria": [
    "WHEN [condition]\nTHEN [outcome]",
    "WHEN [condition]\nTHEN [outcome] AND [additional outcome]"
  ]
}
```

**Format Rules:**
- Each acceptance criteria is a SINGLE string with WHEN/THEN pair
- WHEN and THEN on separate lines (use `\n` for newline)
- THEN and its AND must be together on the same line
- Each WHEN condition starts a new acceptance criteria

#### Stories to Update in story-graph.json

| # | Story | Type | Delta Focus |
|---|-------|------|-------------|
| 1 | Show Available Behaviors and Actions | EXISTING | Real bot behaviors vs mock list |
| 2 | Navigate To Behavior | EXISTING | Real behavior navigation vs mock |
| 3 | Navigate To Action | EXISTING | Real action navigation vs mock |
| 4 | Request Help | EXISTING | Real action parameters from context_class |
| 5 | Request Status | EXISTING | Real workflow state from bot |
| 6 | Provide Context For Instructions | NEW | Load real BehaviorActionState |
| 7 | Provide Story Scope Context For Instructions | NEW | Parse real Scope |
| 8 | Provide File Scope Context For Instructions | NEW | Parse real file scope |
| 9 | Store Scope Context | NEW | Persist to real state file |
| 10 | Get Instructions and Display | NEW | Call real action.get_instructions() (stubbed internals) |
| 11 | Submit Action and Display Results | NEW | Call real action.submit() (stubbed saves) |
| 12 | Confirm Action and Display Results | NEW | Call real action.confirm() |
| 13 | Enter Confirm Results | EXISTING | Process confirm with real state update |
| 14 | Advance To Next Action | EXISTING | Real workflow advancement |
| 15 | Loop Back To Display State | NEW | Real state display loop |
| 16 | Show Action Parameter Help | EXISTING | Real parameters from ActionDataCollector |
| 17 | Format CLI Output For Chat | NEW | Use legacy CLI formatters/output builders for pipe mode |

#### Delta Focus for Existing Stories

For stories that already exist with mock implementations, acceptance criteria must focus on:

**What changes from MOCK to REAL (with test_story_bot)?**

| Aspect | Mock Mode (Increment 10) | Real Mode (Increment 11) |
|--------|--------------------------|--------------------------|
| Bot | Fake bot structure | Real `test_story_bot` with full structure |
| Behaviors | Mock list ["shape", "discovery", ...] | Loaded from `bot_config.json` |
| Actions | Mock list ["clarify", "strategy", ...] | Loaded from behavior configs |
| Parameters | Hardcoded display | From `action.context_class` via `ActionDataCollector` |
| Scope | Simple string storage | Parsed `Scope` object |
| State | Simple dict | Real `BehaviorActionState` with persistence |
| Execution | Mock "EXECUTING" message | Real action methods (stubbed internals) |

**Example Delta Acceptance Criteria:**

```
// EXISTING story with delta focus
"name": "Show Available Behaviors and Actions",
"acceptance_criteria": [
  "WHEN REPL starts with test_story_bot\nTHEN CLI displays behaviors loaded from bot_config.json",
  "WHEN behavior list is displayed\nTHEN behaviors match test_story_bot.behaviors.names",
  "WHEN action list is displayed\nTHEN actions come from current behavior's action_names property"
]
```

### Phase 2B: Render Increment Exploration Document

After updating story-graph.json, render ONE increment-level exploration document.

#### Output Location

`agile_bot/bots/base_bot/docs/stories/increment-11-exploration.md`

#### Template (from story-exploration.md)

```markdown
# REPL All Scope Parameters (Mock Backend) - Increment Exploration

**Navigation:** [📋 Story Map](./map/story-map-outline.drawio) | [📊 Increments](./increments/story-map-increments.txt)

**File Name**: `increment-11-exploration.md`
**Location**: `agile_bot/bots/base_bot/docs/stories/increment-11-exploration.md`

**Priority:** 11
**Relative Size:** Medium (17 stories)

## Increment Purpose

Delivers complete REPL user experience with real bot integration (test_story_bot) and stubbed action execution so that users can navigate workflows, set scope parameters, and execute operations without actual file saves or scanner runs.

---

## Domain AC (Increment Level)

### Core Domain Concepts

- REPLSession: Manages interactive session state and command processing
- Scope: Typed scope parameters (type, value, exclude)
- ActionOperations: Three-phase execution (instructions, submit, confirm)
- BehaviorActionState: Persisted workflow position and scope

### Domain Behaviors

- REPLSession routes commands to action operations
- CliContextBuilder parses scope parameters into Scope
- ActionDataCollector provides real parameter metadata
- BehaviorActionState persists scope across commands

### Domain Rules

- Scope must be parsed before action execution
- Actions have three operations: instructions, submit, confirm
- test_story_bot provides real structure, stubbed execution
- State persists between REPL commands

---

## Stories (17 total)

{stories_with_ac from story-graph.json}

---

## Consolidation Decisions

- Merged scope parameter stories (basic, story, file) into single flow with different scope types
- Operations (instructions, submit, confirm) replace single "execute" concept
- Real bot integration uses test_story_bot with stubbed action internals

---

## Delta from Increment 10

| Area | Increment 10 (Mock) | Increment 11 (Real Bot) |
|------|---------------------|-------------------------|
| Bot | Fake structure | Real test_story_bot |
| Scope | String storage | Parsed Scope |
| Execution | Mock messages | Real action methods (stubbed) |
| Parameters | Hardcoded | From ActionDataCollector |

---

## Source Material

- **Phase:** Exploration
- **Source:** story-graph.json, priority 11 increment
- **Templates:** story-graph-explored.json, story-exploration.md
- **Rules:** /story_bot-exploration-rules
```

---

## ⏸️ CHECKPOINT: Human Review After Exploration

**STOP HERE** after Step 2 is complete.

Before proceeding to Step 3 (Scenarios):
1. Human reviews all acceptance criteria added to story-graph.json
2. Human reviews increment-11-exploration.md document
3. Human confirms delta focus is correct (mock vs real)
4. Human approves acceptance criteria before creating scenarios

**Do not proceed to Step 3 until human approval is given.**

---

## Step 3: Scenarios (BDD)

After exploration is complete and acceptance criteria are in story-graph.json, create scenarios for ALL 16 stories.

### Process

Scenarios are created based on the acceptance criteria defined in Step 2.

**Step 3A: Load Scenario Rules**

```bash
python agile_bot/bots/story_bot/src/story_bot_cli.py --behavior scenarios --action rules --message "Guide me to write scenarios for Increment 11 stories"
```

**Step 3B: Build Scenarios**

```bash
python agile_bot/bots/story_bot/src/story_bot_cli.py --behavior scenarios --action build --scope "{'type': 'increment', 'value': [11]}"
```

**Step 3C: Validate Scenarios**

```bash
python agile_bot/bots/story_bot/src/story_bot_cli.py --behavior scenarios --action validate --scope "{'type': 'increment', 'value': [11]}"
```

### Scenario Creation Guidelines

- Scenarios are derived FROM the acceptance criteria created in Step 2
- Follow ALL rules from `/story_bot-scenarios-rules`
- Each acceptance criteria WHEN/THEN becomes the basis for one or more scenarios
- Use Scenario Outlines where examples table makes sense
- Focus on real bot behavior with stubbed execution (no file saves, no scanner runs)

---

## ⏸️ CHECKPOINT: Human Review After Scenarios

**STOP HERE** after Step 3 is complete.

Before proceeding to Step 4 (TDD Implementation):
1. Human reviews all acceptance criteria in story-graph.json
2. Human reviews increment-11-exploration.md
3. Human reviews all generated scenarios
4. Human approves scenarios before writing tests

**Do not proceed to Step 4 until human approval is given.**

---

## Step 4: TDD Implementation (After Human Approval)

Once scenarios are approved, proceed with TDD:
1. **Write tests** based on approved scenarios
2. **Implement code** to make tests pass
3. **Manual testing** to verify end-to-end experience

### 4.1 Refactor Action Classes

Add three new methods to base `Action` class:

```python
class Action:
    # Keep execute() for backward compatibility
    
    def get_instructions(self, context: ActionContext = None) -> Dict[str, Any]:
        """Returns AI instructions without running scanners or saving files.
        
        This is the first phase of the three-phase action pattern.
        Loading/reading files is allowed. Writing files is NOT allowed.
        
        Stubs:
        - CodeScanner calls → empty violations
        - Knowledge graph loading → We can use the story graph in Story Test Bot
        - No file writes
        """
        
    def submit(self, context: ActionContext = None) -> Dict[str, Any]:
        """Process submitted work - saves files and performs side effects.
        
        Returns success message and list of files that would be saved.
        """
        
    def confirm(self, context: ActionContext = None) -> Dict[str, Any]:
        """Mark action complete and advance to next action.
        
        Updates workflow state and returns next action info.
        """
```

### 4.2 Test File Structure

Update `test_run_interactive_repl.py`:

```python
# Add test classes for new stories
class TestProvideContextForInstructions:
    """Tests for loading base context for instructions."""
    
class TestProvideStoryScopeContext:
    """Tests for story scope parameter handling."""
    
class TestProvideFileScopeContext:
    """Tests for file scope parameter handling."""
    
class TestStoreScopeContext:
    """Tests for persisting scope in state."""
    
class TestGetInstructionsAndDisplay:
    """Tests for instructions operation with real bot, stubbed execution."""
    
class TestSubmitActionAndDisplay:
    """Tests for submit operation with stubbed saves."""
    
class TestConfirmActionAndDisplay:
    """Tests for confirm operation with state advancement."""
```

### 4.3 Wire in test_story_bot

Create/configure `test_story_bot` for testing:

```
agile_bot/bots/test_story_bot/
├── bot_config.json          # Minimal config for testing
├── behaviors/
│   ├── shape/
│   │   ├── behavior.json
│   │   └── actions/...
│   └── ... (other behaviors)
└── docs/
    └── stories/
        └── story-graph.json  # Test fixture
```

### 4.4 TDD Cycle for Each Story

1. **RED**: Write failing test based on scenario
2. **GREEN**: Implement minimum code to pass
3. **REFACTOR**: Clean up while tests pass

---

## Execution Checklist

### Prerequisite: Review CLI Patterns
- [ ] Review `CliContextBuilder` for scope parsing patterns
- [ ] Review `CliParameterParser` for argument parsing patterns
- [ ] Review `CliCommandRouter` for action execution patterns
- [ ] Review `CliTerminalFormatter` for output formatting
- [ ] Review `ActionDataCollector` for parameter/help data
- [ ] Identify reusable components for REPL scope handling
- [ ] Document integration points between CLI and REPL modules

### Step 1: Rationalize Stories
- [ ] Delete "Show Workflow Hierarchy Via Status Command" from story-graph.json
- [ ] Delete "Execute Mock Action and Display Results" from story-graph.json
- [ ] Delete "Set Scope Parameter" from story-graph.json
- [ ] Rename "Display Behaviors and Actions on Startup" → "Show Available Behaviors and Actions"
- [ ] Rename "Navigate with Back/Next/Current" → "Navigate Within Behavior"
- [ ] Add 7 new story definitions to story-graph.json

### Step 2A: Update story-graph.json with Acceptance Criteria
- [ ] Execute `/story_bot-exploration-rules` to load all exploration rules
- [ ] Follow ALL rules when writing acceptance criteria
- [ ] Update AC: Show Available Behaviors and Actions (delta: real bot behaviors)
- [ ] Update AC: Navigate To Behavior (delta: real behavior navigation)
- [ ] Update AC: Navigate To Action (delta: real action navigation)
- [ ] Update AC: Request Help (delta: real parameters from context_class)
- [ ] Update AC: Request Status (delta: real workflow state)
- [ ] Add AC: Provide Context For Instructions (NEW)
- [ ] Add AC: Provide Story Scope Context For Instructions (NEW)
- [ ] Add AC: Provide File Scope Context For Instructions (NEW)
- [ ] Add AC: Store Scope Context (NEW)
- [ ] Add AC: Get Instructions and Display (NEW)
- [ ] Add AC: Submit Action and Display Results (NEW)
- [ ] Add AC: Confirm Action and Display Results (NEW)
- [ ] Update AC: Enter Confirm Results (delta: real state update)
- [ ] Update AC: Advance To Next Action (delta: real workflow advancement)
- [ ] Add AC: Loop Back To Display State (NEW)
- [ ] Update AC: Show Action Parameter Help (delta: real ActionDataCollector)
- [ ] Add AC: Format CLI Output For Chat (NEW - legacy formatters in pipe mode)

### Step 2B: Render Increment Exploration Document
- [ ] Create `increment-11-exploration.md` using story-exploration.md template
- [ ] Include all stories with acceptance criteria from story-graph.json
- [ ] Document Delta from Increment 10 (mock vs real)
- [ ] Document consolidation decisions
- [ ] Reference source material and rules followed

### ⏸️ CHECKPOINT: Human Review After Exploration
- [ ] **STOP** - Wait for human review of story-graph.json acceptance criteria
- [ ] **STOP** - Wait for human review of increment-11-exploration.md
- [ ] **APPROVAL** - Human approves before proceeding to Step 3

### Step 3: Scenarios
- [ ] Execute `/story_bot-scenarios-rules` to load all scenario rules
- [ ] Run `--behavior scenarios --action build` for Increment 11
- [ ] Run `--behavior scenarios --action validate` for Increment 11
- [ ] Fix any validation errors
- [ ] Ensure scenarios derive from acceptance criteria in story-graph.json

### ⏸️ CHECKPOINT: Human Review After Scenarios
- [ ] **STOP** - Wait for human review of all generated scenarios
- [ ] **APPROVAL** - Human approves before proceeding to Step 4

### Step 4: TDD (After Human Approval)
- Update scenarios and test data based on the new signatures as well as for the new stories.
- [ ] Refactor Action base class with three-method pattern
- [ ] Refactor ClarifyAction 
- [ ] Refactor StrategyAction 
- [ ] Refactor BuildAction with stubbed Knowledge. Graph createing update
- [ ] Refactor ValidateAction with stubbed scanning
- [ ] Refactor RenderAction with stubbed rendering
- [ ] Configure test_story_bot
- [ ] Write tests for each story (RED)
- [ ] Implement each story (GREEN)
- [ ] Refactor and clean up

### Step 5: Manual Testing
- [ ] Test complete user experience end-to-end
- [ ] Verify navigation works with real test_story_bot
- [ ] Verify scope parameters work correctly
- [ ] Verify instructions/submit/confirm operations work
- [ ] Verify state persistence across commands
- [ ] Document any issues found

---

## Dependencies

- **Increment 10** must be complete (basic REPL navigation)
- **test_story_bot** folder needs to be configured
- **Action refactoring** must happen before execution tests

---

## Success Criteria

1. All 16 stories have acceptance criteria in story-graph.json (human approved)
2. Increment exploration document created and reviewed
3. All 16 stories have Gherkin scenarios (human approved)
4. All tests pass using real `test_story_bot` with stubbed execution
5. Actions support `get_instructions()`, `submit()`, `confirm()` operations
6. No actual file saves, scanner runs, or renders during testing
7. Manual testing confirms complete user experience works end-to-end

