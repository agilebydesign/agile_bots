# CLI Chain Operations Plan

## Overview

This plan documents the "Chain Multiple Operations through CLI" epic which enables executing multiple bot operations in a single command, aggregating instructions, and saving reusable command chains as named flows.

**Epic Goal:** Allow users to chain multiple behavior/action combinations in a single CLI call, with the backend aggregating instructions and supporting sequential submit/confirm patterns. Enable saving these chains as reusable "bot flows" for common workflows.

## Use Cases

### Vibe Code
```bash
all.build.instructions --context "I want to create an application that can do..."
```
Runs build instructions for all behaviors to get initial direction.

### One Shot
```bash
all.all.instructions --context "I want a story that does..."
```
Runs all behaviors, all actions, all operations in sequence - AI asks clarifying questions and figures out strategy.

### Publish
```bash
all.render.instructions
```
Ensures all documentation is up to date with latest story_graph changes.

### Plan
```bash
[discovery,exploration,scenarios].[build,render].instructions
```
Runs build then render for discovery, exploration, and scenarios behaviors.

### Document
```bash
[tests,scenarios,discovery].[instructions,submit] --scope "c:/dev/.../repl/"
```
Runs instructions then submit for tests, scenarios, and discovery in sequence.

### TDD
```bash
[scenarios,tests,code].[render,build,validate].instructions --scope "Load All Registered Bots"
```
Build and validate on scenarios, tests, then code for a specific story/epic scope.

## Increments

### Increment 1: All with Instructions (Priority 14)
**Goal:** Execute single operation across all behaviors or all actions

**Examples:**
- `all.build.instructions` - Build for all behaviors
- `discovery.all.instructions` - All actions for discovery behavior
- `all.all.instructions` - Everything everywhere

### Increment 2: Bracket Notation for Multiple Selections (Priority 15)
**Goal:** Select specific behaviors/actions using bracket notation

**Examples:**
- `[discovery,exploration].build.instructions` - Build for selected behaviors
- `discovery.[build,render].instructions` - Selected actions for one behavior
- `[discovery,exploration].[build,render].instructions` - Matrix of behaviors × actions

### Increment 3: Multi-Phase with Submit/Confirm (Priority 16)
**Goal:** Chain operations with submit and confirm steps

**Examples:**
- `discovery.[instructions,submit]` - Instructions then auto-submit
- `[scenarios,tests].[instructions,submit,confirm]` - Full workflow with confirmation
- `all.[build,submit,validate,confirm]` - Complete build-validate cycle

### Increment 4: Order Enforcement with Signatures (Priority 17)
**Goal:** Ensure AI executes chained operations in correct order with verification

**Examples:**
- `[scenarios,tests,code].[build,validate].instructions --verify`
- Backend generates signature of expected operation sequence
- AI must include signature when submitting to prove correct execution order
- System validates signature and reports any missed/out-of-order operations

---

## Increment 1: All with Instructions

### Stories

#### 1. Execute Operation on All Behaviors
**Epic:** Execute Action Operation Through CLI  
**Sequential Order:** 7  
**Story Type:** User  
**Actor:** User

**Purpose:** Execute a single action (like build or render) across all registered behaviors in the current bot.

**Implementation Notes:**
- Syntax: `all.<action>.instructions` or `all.<action>`
- Backend iterates through all behaviors in bot_config
- For each behavior, execute the specified action
- Aggregate all instruction outputs into single response
- Each behavior's instructions shown as separate block with header
- Format:
  ```
  === Behavior: discovery ===
  [instructions for discovery.build]
  
  === Behavior: exploration ===
  [instructions for exploration.build]
  
  === Behavior: scenarios ===
  [instructions for scenarios.build]
  ```

**Acceptance Criteria:**
- `all.<action>` executes action for every behavior
- Instructions aggregated in readable format
- Each behavior block clearly labeled
- Errors in one behavior don't stop others
- Summary shows which behaviors succeeded/failed

---

#### 2. Execute All Actions on Single Behavior
**Epic:** Execute Action Operation Through CLI  
**Sequential Order:** 8  
**Story Type:** User  
**Actor:** User

**Purpose:** Execute all actions (clarify, strategy, build, validate, render) for a specific behavior.

**Implementation Notes:**
- Syntax: `<behavior>.all.instructions` or `<behavior>.all`
- Backend iterates through all actions in behavior workflow
- Executes in workflow order (respecting action_config order)
- Aggregates instructions from each action
- Format:
  ```
  === Action: clarify ===
  [instructions for clarify]
  
  === Action: strategy ===
  [instructions for strategy]
  
  === Action: build ===
  [instructions for build]
  
  === Action: validate ===
  [instructions for validate]
  
  === Action: render ===
  [instructions for render]
  ```

**Acceptance Criteria:**
- `<behavior>.all` executes all workflow actions
- Actions execute in configured order
- Independent actions (rules, help) excluded from `.all`
- Instructions aggregated with action headers
- Summary of execution results

---

#### 3. Execute Operation on All Behaviors and All Actions
**Epic:** Execute Action Operation Through CLI  
**Sequential Order:** 9  
**Story Type:** User  
**Actor:** User

**Purpose:** Execute all actions across all behaviors - complete bot workflow in one command.

**Implementation Notes:**
- Syntax: `all.all.instructions` or `all.all`
- Matrix execution: for each behavior, run all actions
- Massive output - needs good organization
- Consider adding `--summary` flag for condensed view
- Format:
  ```
  === Behavior: discovery ===
    --- Action: clarify ---
    [instructions]
    --- Action: strategy ---
    [instructions]
    --- Action: build ---
    [instructions]
  
  === Behavior: exploration ===
    --- Action: clarify ---
    [instructions]
    ...
  ```

**Acceptance Criteria:**
- Executes complete matrix of behaviors × actions
- Organized hierarchical output
- Option for summary view
- Performance acceptable for large bots
- Clear progress indicators

---

#### 4. Display Aggregated Instructions with Segmentation
**Epic:** Display Bot State Using CLI  
**Sequential Order:** 6  
**Story Type:** System  
**Actor:** CLI

**Purpose:** Display chained operation instructions in clear segments with headers and separators.

**Implementation Notes:**
- Each operation's instructions displayed as separate block
- Headers show context: behavior name, action name
- Visual separators between blocks (=== or ---)
- Summary section at end with:
  - Total operations executed
  - Success/failure count
  - Estimated tokens/complexity
  - Next steps recommendation
- Support for different output formats (detailed, summary, JSON)

**Acceptance Criteria:**
- Clear visual hierarchy in output
- Headers identify behavior/action context
- Separators between instruction blocks
- Summary section provides overview
- Readable in both TTY and piped modes

---

## Increment 2: Bracket Notation for Multiple Selections

### Stories

#### 5. Parse Bracket Notation for Behavior Selection
**Epic:** Navigate Bot Behaviors and Actions With CLI  
**Sequential Order:** 5  
**Story Type:** System  
**Actor:** CLI

**Purpose:** Parse bracket notation `[behavior1,behavior2,behavior3]` to select specific behaviors.

**Implementation Notes:**
- Syntax: `[discovery,exploration,scenarios].<action>`
- Parser extracts list of behaviors from brackets
- Validates each behavior exists
- Executes action for each behavior in list order
- Supports both behavior names and indices (future)
- Error handling for invalid behavior names

**Acceptance Criteria:**
- Correctly parses bracket notation
- Validates all behaviors exist
- Maintains order specified in brackets
- Clear error messages for invalid names
- Works with all action types

---

#### 6. Parse Bracket Notation for Action Selection
**Epic:** Navigate Bot Behaviors and Actions With CLI  
**Sequential Order:** 6  
**Story Type:** System  
**Actor:** CLI

**Purpose:** Parse bracket notation `[build,validate,render]` to select specific actions.

**Implementation Notes:**
- Syntax: `<behavior>.[build,validate,render]`
- Parser extracts list of actions from brackets
- Validates actions exist for behavior
- Executes in list order (not workflow order)
- Supports workflow and independent actions
- Can mix action types in one chain

**Acceptance Criteria:**
- Correctly parses action brackets
- Validates actions exist for behavior
- Executes in specified order
- Supports independent actions
- Clear error messages

---

#### 7. Execute Matrix of Behaviors and Actions
**Epic:** Execute Action Operation Through CLI  
**Sequential Order:** 10  
**Story Type:** User  
**Actor:** User

**Purpose:** Execute multiple actions across multiple behaviors in matrix pattern.

**Implementation Notes:**
- Syntax: `[behavior1,behavior2].[action1,action2]`
- Matrix execution: for each behavior, run each action
- Example: `[discovery,exploration].[build,render]` runs:
  - discovery.build
  - discovery.render
  - exploration.build
  - exploration.render
- Order: iterate behaviors outer, actions inner
- Aggregate all results with clear structure

**Acceptance Criteria:**
- Matrix execution works correctly
- Output clearly shows behavior/action combinations
- Order is predictable (behaviors outer, actions inner)
- All combinations executed even if some fail
- Summary shows matrix results

---

## Increment 3: Multi-Phase with Submit/Confirm

### Stories

#### 8. Execute Instructions Phase
**Epic:** Execute Action Operation Through CLI  
**Sequential Order:** 11  
**Story Type:** System  
**Actor:** CLI

**Purpose:** Execute the "instructions" phase which generates AI instructions without execution.

**Implementation Notes:**
- Phase: `instructions` - generates AI guidance
- Backend prepares instruction content
- Does NOT execute action, only generates instructions
- Instructions include:
  - Context about current state
  - What AI should do
  - Rules to follow
  - Expected output format
- Can be chained: `discovery.[instructions,submit]`

**Acceptance Criteria:**
- Instructions phase generates proper guidance
- No execution side effects
- Output formatted for AI consumption
- Can be first step in chain
- Supports all action types

---

#### 9. Execute Submit Phase
**Epic:** Execute Action Operation Through CLI  
**Sequential Order:** 12  
**Story Type:** System  
**Actor:** CLI

**Purpose:** Execute the "submit" phase which takes AI-generated content and commits it.

**Implementation Notes:**
- Phase: `submit` - persists content from AI
- Expects content from previous phase (instructions)
- Validates content meets requirements
- Writes to appropriate files/storage
- Updates workflow state if needed
- Confirms completion to user

**Acceptance Criteria:**
- Submit phase persists content correctly
- Validates content before committing
- Updates state appropriately
- Clear success/failure messages
- Can follow instructions phase

---

#### 10. Execute Confirm Phase
**Epic:** Execute Action Operation Through CLI  
**Sequential Order:** 13  
**Story Type:** System  
**Actor:** CLI

**Purpose:** Execute the "confirm" phase which validates submitted content and marks action complete.

**Implementation Notes:**
- Phase: `confirm` - validates and finalizes
- Runs validation rules on submitted content
- Updates workflow state to completed
- Triggers next action if auto_progress enabled
- Generates confirmation report

**Acceptance Criteria:**
- Confirm phase validates content
- Workflow state updated correctly
- Auto-progress works if configured
- Validation results shown clearly
- Can be final step in chain

---

#### 11. Chain Phases with Aggregated Output
**Epic:** Execute Action Operation Through CLI  
**Sequential Order:** 14  
**Story Type:** User  
**Actor:** User

**Purpose:** Chain multiple phases (instructions, submit, confirm) with output aggregation.

**Implementation Notes:**
- Syntax: `behavior.[instructions,submit,confirm]`
- Each phase executes in order
- Output from one phase flows to next
- Aggregated display shows each phase:
  ```
  === Phase: instructions ===
  [AI instructions generated]
  
  === Phase: submit ===
  [Content submitted successfully]
  
  === Phase: confirm ===
  [Validation passed, action completed]
  ```
- Phases can be mixed with actions: `[build,submit,validate,confirm]`

**Acceptance Criteria:**
- Phases execute in sequence
- Data flows between phases
- Clear phase boundaries in output
- Can mix phases and actions
- Error in one phase stops chain appropriately

---

## Increment 4: Order Enforcement with Signatures

### Stories

#### 12. Generate Operation Sequence Signature
**Epic:** Execute Action Operation Through CLI  
**Sequential Order:** 15  
**Story Type:** System  
**Actor:** CLI

**Purpose:** Generate cryptographic signature representing expected operation sequence.

**Implementation Notes:**
- When chain command executed with `--verify` flag
- Backend generates signature of operation sequence
- Signature includes:
  - Operation names in order
  - Timestamps
  - Scope/context parameters
  - Expected outputs
- Signature embedded in instructions for AI
- AI must include signature when submitting

**Acceptance Criteria:**
- Signature generated for command chains
- Includes all operation details
- Embedded in AI instructions
- Secure enough to detect tampering
- Works with all chain types

---

#### 13. Validate Operation Sequence on Submit
**Epic:** Execute Action Operation Through CLI  
**Sequential Order:** 16  
**Story Type:** System  
**Actor:** CLI

**Purpose:** Validate AI executed operations in correct order by checking signature.

**Implementation Notes:**
- On submit with signature, backend validates:
  - All operations were executed
  - Operations in correct order
  - No operations skipped
  - No extra operations added
- If validation fails:
  - Generate detailed error report
  - Show which operations were missed/wrong order
  - Provide corrective instructions for AI
  - Do NOT commit content
- If validation passes:
  - Proceed with normal submit/confirm

**Acceptance Criteria:**
- Signature validation works correctly
- Detects missing operations
- Detects wrong order
- Generates helpful error messages
- Provides recovery instructions for AI
- Prevents invalid submissions

---

## Bot Flows: Saved Command Chains

### Stories

#### 14. Define Bot Flow Configuration
**Epic:** Initialize REPL Session  
**Sequential Order:** 7  
**Story Type:** System  
**Actor:** CLI

**Purpose:** Define structure for saving command chains as named "bot flows" in bot_config.

**Implementation Notes:**
- Bot flows stored in bot_config.json:
  ```json
  {
    "bot_flows": {
      "vibe": {
        "command": "all.build.instructions",
        "description": "Get initial direction for application",
        "prompt_for": ["context"]
      },
      "publish": {
        "command": "all.render.instructions",
        "description": "Update all documentation"
      },
      "plan": {
        "command": "[discovery,exploration,scenarios].[build,render].instructions",
        "description": "Plan work for story behaviors"
      },
      "tdd": {
        "command": "[scenarios,tests,code].[build,validate].instructions",
        "description": "Test-driven development flow",
        "prompt_for": ["scope"]
      }
    }
  }
  ```
- Flows can prompt for parameters
- Flows can include default scopes/contexts

**Acceptance Criteria:**
- Bot flow structure defined in schema
- Supports all chain syntax
- Can specify parameter prompts
- Can include defaults
- Validated on load

---

#### 15. Execute Bot Flow by Name
**Epic:** Execute Action Operation Through CLI  
**Sequential Order:** 17  
**Story Type:** User  
**Actor:** User

**Purpose:** Execute saved bot flow by name instead of typing full command.

**Implementation Notes:**
- Syntax: `flow <flow_name>` or `@<flow_name>`
- Example: `flow vibe` or `@vibe`
- Loads flow definition from bot_config
- Prompts for any required parameters
- Substitutes parameters into command
- Executes resulting chain command
- Can override parameters: `flow tdd --scope "My Story"`

**Acceptance Criteria:**
- Can execute flow by name
- Prompts for required params
- Can override params via CLI
- Clear error if flow doesn't exist
- Works in TTY and piped mode

---

#### 16. Display Available Bot Flows
**Epic:** Display Bot State Using CLI  
**Sequential Order:** 7  
**Story Type:** User  
**Actor:** User

**Purpose:** Display all available bot flows with descriptions in command bar.

**Implementation Notes:**
- Command: `flows` or `list-flows`
- Shows table of available flows:
  ```
  Available Bot Flows:
  
  Name      Description                              Command
  ────────  ────────────────────────────────────────  ─────────────────────────────
  vibe      Get initial direction for application     all.build.instructions
  publish   Update all documentation                  all.render.instructions
  plan      Plan work for story behaviors             [discovery,exploration,scenarios].[build,render].instructions
  tdd       Test-driven development flow              [scenarios,tests,code].[build,validate].instructions
  ```
- Include in help text
- Show in footer/command bar
- Highlight commonly used flows

**Acceptance Criteria:**
- Lists all defined flows
- Shows descriptions
- Shows commands
- Formatted for readability
- Included in help system

---

#### 17. Create Custom Bot Flow from Command
**Epic:** Execute Action Operation Through CLI  
**Sequential Order:** 18  
**Story Type:** User  
**Actor:** User

**Purpose:** Save a command chain as a named bot flow for reuse.

**Implementation Notes:**
- Syntax: `save-flow <name> <command> [--description "..."]`
- Example: `save-flow myflow "[discovery,tests].[build,validate]" --description "My custom flow"`
- Validates command syntax
- Adds flow to bot_config.json
- Flow immediately available for use
- Can overwrite existing flow with `--force`

**Acceptance Criteria:**
- Can save command as named flow
- Validates command syntax
- Persists to bot_config
- Immediately usable
- Can update existing flows with --force
- Cannot overwrite without --force

---

## Technical Implementation

### Files to Create/Modify

#### New Files
- `agile_bot/bots/base_bot/src/repl_cli/chain_parser.py` - Parse chain notation
- `agile_bot/bots/base_bot/src/repl_cli/chain_executor.py` - Execute chained operations
- `agile_bot/bots/base_bot/src/repl_cli/phase_executor.py` - Execute phases (instructions/submit/confirm)
- `agile_bot/bots/base_bot/src/repl_cli/signature_validator.py` - Generate/validate signatures
- `agile_bot/bots/base_bot/src/repl_cli/flow_manager.py` - Manage bot flows

#### Modified Files
- `agile_bot/bots/base_bot/src/repl_cli/command_parser.py` - Add chain syntax support
- `agile_bot/bots/base_bot/src/repl_cli/executor.py` - Route to chain executor
- `agile_bot/bots/base_bot/src/repl_cli/display.py` - Display aggregated output
- `agile_bot/bots/base_bot/src/bot/bot_config.py` - Add bot_flows schema
- `agile_bot/bots/base_bot/base_actions/*/action_config.json` - Add phase support

### Domain Model

#### New Domain Concepts (Emphasized)

**ChainCommand:** A command that executes multiple operations in sequence
- Behaviors: List of behavior names or "all"
- Actions: List of action names or "all"  
- Phases: List of phases (instructions, submit, confirm)
- Scope: Optional scope parameter
- Context: Optional context parameter

**BehaviorSelector:** Selects which behaviors to execute
- All: Execute for all behaviors
- List: Execute for specific behaviors `[behavior1,behavior2]`
- Single: Execute for one behavior

**ActionSelector:** Selects which actions to execute
- All: Execute all workflow actions
- List: Execute specific actions `[action1,action2]`
- Single: Execute one action

**PhaseSelector:** Selects which phases to execute
- Instructions: Generate AI instructions only
- Submit: Persist AI-generated content
- Confirm: Validate and finalize
- Can be combined: `[instructions,submit,confirm]`

**OperationSequence:** Ordered list of operations to execute
- Sequence: List of (behavior, action, phase) tuples
- Signature: Cryptographic hash of expected sequence
- Actual: What was actually executed (for validation)

**BotFlow:** Named, reusable command chain
- Name: Flow identifier
- Command: Chain command template
- Description: Human-readable description
- Parameters: Prompted parameters (context, scope, etc.)
- Defaults: Default parameter values

**AggregatedOutput:** Combined output from multiple operations
- Segments: List of operation outputs
- Headers: Behavior/action/phase context for each segment
- Summary: Overall execution results
- Format: Display format (detailed, summary, JSON)

#### Extended Domain Concepts

**Command (extended):** Add chain command support
- ChainSyntax: Parse bracket notation and dot notation chains
- FlowExecution: Execute saved bot flows

**Executor (extended):** Add chain execution capability
- SequenceExecution: Execute operation sequences
- OutputAggregation: Combine outputs from multiple operations

**Display (extended):** Add segmented output support
- SegmentHeaders: Show behavior/action/phase context
- SummarySection: Aggregate results overview

## Testing Strategy

### Increment 1 Tests
- Test `all.build` across multiple behaviors
- Test `behavior.all` across multiple actions
- Test `all.all` complete matrix
- Test output aggregation and formatting
- Test error handling (one behavior fails)

### Increment 2 Tests
- Test bracket parsing for behaviors
- Test bracket parsing for actions
- Test matrix execution `[b1,b2].[a1,a2]`
- Test invalid behavior/action names
- Test order preservation

### Increment 3 Tests
- Test instructions phase execution
- Test submit phase execution
- Test confirm phase execution
- Test phase chaining
- Test phase + action mixing

### Increment 4 Tests
- Test signature generation
- Test signature validation (success)
- Test signature validation (failure - missing operation)
- Test signature validation (failure - wrong order)
- Test error recovery instructions

### Bot Flows Tests
- Test flow definition in bot_config
- Test flow execution by name
- Test flow parameter prompting
- Test flow listing
- Test flow creation/saving
- Test flow overwrite protection

## Success Criteria

### Increment 1
- [ ] Can execute operation on all behaviors
- [ ] Can execute all operations on one behavior
- [ ] Can execute all operations on all behaviors
- [ ] Output is clearly segmented and readable
- [ ] Errors in one operation don't stop others

### Increment 2
- [ ] Bracket notation parsed correctly
- [ ] Can select multiple behaviors
- [ ] Can select multiple actions
- [ ] Matrix execution works
- [ ] Order is preserved

### Increment 3
- [ ] Instructions phase generates AI guidance
- [ ] Submit phase persists content
- [ ] Confirm phase validates and finalizes
- [ ] Phases can be chained
- [ ] Phases can mix with actions

### Increment 4
- [ ] Signatures generated for chains
- [ ] Signatures validated on submit
- [ ] Validation detects missing/wrong order operations
- [ ] Error messages guide AI to fix
- [ ] Invalid submissions rejected

### Bot Flows
- [ ] Flows defined in bot_config
- [ ] Flows executed by name
- [ ] Flows list available
- [ ] Custom flows can be saved
- [ ] Flows can prompt for parameters

## Development Process

### For Each Increment

#### 1. Shape Phase
Use `/story_bot-shape-rules` to:
- Define domain concepts
- Map user journeys
- Identify key scenarios

#### 2. Prioritization Phase  
Use `/story_bot-prioritization-rules` to:
- Order stories within increment
- Define dependencies
- Set acceptance criteria

#### 3. Exploration Phase
Use `/story_bot-exploration-rules` to:
- Write detailed acceptance criteria
- Define Given/When/Then scenarios
- Specify test cases

#### 4. Design Phase
Use `/crc_bot-design-rules` to:
- Design classes and collaborators
- Define responsibilities
- Map interactions

#### 5. Scenarios Phase
Use `/story_bot-scenarios` to:
- Write BDD scenarios for each story
- Follow epic file naming: `cli-chain-operations`
- Story class pattern: `ChainOperationsStories`

#### 6. Walkthrough Phase
Use `/crc_bot-walkthrough` to:
- Explore unique flows
- Validate design decisions
- Find edge cases

#### 7. Tests Phase
Use `/story_bot-tests-rules` to:
- Write unit tests for new classes
- Write integration tests for chains
- Follow test structure guidelines

#### 8. Code Phase
Use `/story_bot-code-rules` to:
- Implement chain parser
- Implement chain executor
- Implement flow manager
- Follow clean code practices

#### 9. Validation Phase
- Run all tests: `pytest agile_bot/bots/base_bot/test/`
- Fix any failures
- Validate against all rules
- Manual testing of example chains

## Notes

### Design Considerations

**Why Aggregated Instructions?**
- AI gets complete context in one response
- Backend prepares all necessary information
- Reduces back-and-forth API calls
- AI can see full scope before acting

**Why Phases?**
- Separates instruction generation from execution
- Allows review before commit
- Enables AI to plan multi-step workflows
- Supports verification of correct execution

**Why Bot Flows?**
- Common workflows become one-command operations
- Reduces cognitive load on users
- Captures team conventions
- Makes CLI more approachable for new users

**Why Signature Verification?**
- Ensures AI actually executed all steps
- Prevents partial execution bugs
- Catches when AI skips or reorders operations
- Provides clear recovery instructions

### Future Enhancements
- Flow templates with variables
- Flow composition (flows calling other flows)
- Conditional execution in chains
- Parallel execution where possible
- Flow libraries shared across bots
- Visual flow builder/editor

---

**Created:** 2025-12-27  
**Epic:** Chain Multiple Operations through CLI  
**Increments:** 14-17  
**Status:** Planning

