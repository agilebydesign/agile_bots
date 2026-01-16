# Remove Operations and Simplify Workflow Plan

## Overview

This plan removes the concept of "operations" (instructions, confirm) from the bot workflow. Actions now execute automatically when navigated to, and guardrails can be passed between actions at any time. Parameters now go directly on actions, not on operations.

## Goals

1. **Remove operations concept**: No more "instructions" or "confirm" operations under actions
2. **Auto-execute instructions**: Navigating to an action automatically executes its instructions
3. **Guardrails flow**: Guardrails can be passed between actions and updated at any time
4. **Update displays**: CLI and panel views no longer show operations
5. **Update documentation**: Help text and examples updated to reflect new workflow
6. **User-controlled advancement**: AI only moves to next action when user explicitly says they're done with current action

---

## PART 1: DOMAIN OBJECT CHANGES

### 1.1 ActionContext Base Class

**File:** `agile_bot/src/actions/action_context.py`

**Changes:**
- **ADD** `guardrails` field to base `ActionContext` class
- All context classes automatically inherit this field

```python
@dataclass
class ActionContext:
    guardrails: Optional[Dict[str, Any]] = None  # Guardrails from previous actions (can be updated at any time)
```

**Impact:** All actions can now accept guardrails via context

---

### 1.2 Action Base Class

**File:** `agile_bot/src/actions/action.py`

**Changes:**

1. **UPDATE** `get_instructions()` method (lines 316-357):
   - Load guardrails from context if provided
   - Merge guardrails into instructions automatically
   - Document that guardrails can be updated at any time

2. **ADD** `_save_guardrails_on_navigation()` method:
   - Template method for subclasses to override
   - Default implementation passes through existing guardrails
   - Called automatically when navigating away from action

3. **REMOVE** `confirm()` method (lines 523-546)
4. **REMOVE** `_do_confirm()` method (lines 548-554)

**Impact:** Actions no longer have separate confirm step - instructions execute automatically

---

### 1.3 ClarifyAction

**File:** `agile_bot/src/actions/clarify/clarify_action.py`

**Changes:**

1. **UPDATE** `_prepare_instructions()` method (lines 35-37):
   - Check for guardrails in context first
   - Use provided guardrails if available, otherwise load fresh

2. **ADD** `_save_guardrails_on_navigation()` method:
   - Save clarifications if answers/evidence/context provided
   - Return guardrails dict to pass to next action
   - Pass through existing guardrails if no new data

3. **REMOVE** `_do_confirm()` method (lines 39-83)

**Impact:** Clarify action saves guardrails automatically when navigating away

---

### 1.4 StrategyAction

**File:** `agile_bot/src/actions/strategy/strategy_action.py`

**Changes:**

1. **UPDATE** `_prepare_instructions()` method (lines 35-45):
   - Merge guardrails from context if provided
   - Include clarifications from previous action

2. **ADD** `_save_guardrails_on_navigation()` method:
   - Save strategy decisions if decisions/assumptions made
   - Return guardrails dict (includes clarifications + strategy)
   - Pass through existing guardrails if no new data

3. **REMOVE** `_do_confirm()` method (lines 47-76)

**Impact:** Strategy action saves guardrails automatically when navigating away

---

### 1.5 BuildAction

**File:** `agile_bot/src/actions/build/build_action.py`

**Changes:**

1. **UPDATE** `_prepare_instructions()` method (lines 45-91):
   - Load guardrails from context if provided
   - Merge clarifications and strategy decisions into instructions

2. **ADD** `_save_guardrails_on_navigation()` method:
   - Pass through guardrails unchanged (build doesn't modify guardrails)

3. **REMOVE** `_do_confirm()` method (lines 93-97)

**Impact:** Build action receives guardrails and passes them through

---

### 1.6 RenderAction and ValidateAction

**Files:** 
- `agile_bot/src/actions/render/render_action.py`
- `agile_bot/src/actions/validate/validate_action.py`

**Changes:**

1. **ADD** `_save_guardrails_on_navigation()` method:
   - Pass through guardrails unchanged (render/validate don't modify guardrails)

2. **REMOVE** `_do_confirm()` method if present

**Impact:** Render/validate actions pass guardrails through without modification

---

### 1.7 Actions Class

**File:** `agile_bot/src/actions/actions.py`

**Changes:**

1. **UPDATE** `navigate_to()` method (lines 122-148):
   - Accept optional `guardrails` parameter
   - Call `_save_guardrails_on_navigation()` on current action before navigating
   - Store guardrails for new action via `_pending_guardrails` attribute
   - Merge saved guardrails with provided guardrails

**Impact:** Guardrails flow automatically between actions during navigation

---

### 1.8 Bot Class

**File:** `agile_bot/src/bot/bot.py`

**Changes:**

1. **REMOVE** `confirm()` method (lines 169-208)

2. **UPDATE** `current()` method (lines 210-243):
   - Load `_pending_guardrails` from action if available
   - Set guardrails in context before calling `get_instructions()`
   - Clear `_pending_guardrails` after use

**Impact:** Bot no longer has confirm command, instructions execute automatically

---

## PART 2: CLI DISPLAY UPDATES

### 2.1 TTY Behaviors Adapter

**File:** `agile_bot/src/behaviors/tty_behavior.py`

**Changes:**

1. **REMOVE** operations display from behavior/action rendering
2. **UPDATE** action display to show only action name and status
3. **REMOVE** any references to operations in serialization

**Impact:** CLI no longer shows operations under actions

---

### 2.2 TTY Bot Adapter

**File:** `agile_bot/src/bot/tty_bot.py`

**Changes:**

1. **UPDATE** `run_instructions` property (lines 90-102):
   - Remove references to operations
   - Update examples to show `behavior.action` pattern only
   - Document that parameters go directly on actions

**Impact:** CLI help text reflects new workflow without operations

---

### 2.3 Help Domain Object

**File:** `agile_bot/src/help/help.py`

**Changes:**

1. **REMOVE** `OperationsHelp` class (lines 130-140)
2. **UPDATE** `ComponentsHelp` class:
   - Remove operations from components list
   - Update descriptions to reflect actions execute directly

3. **UPDATE** `CommandExamples` class (lines 60-73):
   - Remove examples with operations (e.g., `shape.build.submit`)
   - Update examples to show `behavior.action` pattern only
   - Show parameter examples on actions directly

**Impact:** Help system no longer references operations

---

### 2.4 CLI Session

**File:** `agile_bot/src/cli/cli_session.py`

**Changes:**

1. **VERIFY** `_route_to_behavior_action()` method (lines 205-230):
   - Ensure it handles `behavior.action` pattern correctly
   - Remove any operation parsing logic if present

2. **VERIFY** `_handle_action_shortcut()` method (lines 232-312):
   - Ensure action shortcuts work without operations
   - Parameters should be parsed as action context parameters

**Impact:** CLI routing works correctly without operations

---

## PART 3: PANEL VIEW UPDATES

### 3.1 BehaviorsView JavaScript

**File:** `agile_bot/src/behaviors/behaviors_view.js`

**Changes:**

1. **REMOVE** `renderOperation()` method (lines 303-323)
2. **UPDATE** `renderAction()` method (lines 275-301):
   - Remove operations rendering (lines 292-296)
   - Remove operations HTML generation
   - Actions display directly without operations sub-items

3. **UPDATE** `navigateAndExecute()` calls:
   - Change from `navigateAndExecute(behavior, action, operation)` 
   - To `navigateToAction(behavior, action)` or direct action execution
   - Parameters should be passed as action context, not operation parameters

**Impact:** Panel no longer displays operations under actions

---

### 3.2 Behavior Action Status Builder

**File:** `agile_bot/src/actions/behavior_action_status_builder.py`

**Changes:**

1. **UPDATE** `get_behavior_action_status_breadcrumbs()` method:
   - Remove operations from breadcrumb generation
   - Actions show directly without operation sub-items

2. **VERIFY** JSON structure generation:
   - Ensure `actions` array doesn't include `operations` property
   - Actions should have parameters directly, not under operations

**Impact:** Status JSON no longer includes operations structure

---

### 3.3 JSON Behaviors Adapter

**File:** `agile_bot/src/behaviors/json_behavior.py`

**Changes:**

1. **UPDATE** action serialization:
   - Remove `operations` property from action objects
   - Ensure action parameters are at action level, not operation level

**Impact:** JSON output doesn't include operations structure

---

## PART 4: DOCUMENTATION UPDATES

### 4.1 CLI Command Visitor

**File:** `agile_bot/src/cli/cursor/cursor_command_visitor.py`

**Changes:**

1. **UPDATE** command generation (lines 230-237):
   - Remove "Get Instructions" and "Confirm and Advance" sections
   - Update to show action execution with parameters directly
   - Show guardrails parameter examples

**Impact:** Generated commands reflect new workflow

---

### 4.2 Help Text Updates

**Files:**
- `agile_bot/src/help/markdown_help.py`
- `agile_bot/src/help/tty_help.py`

**Changes:**

1. **UPDATE** help text:
   - Remove operations from component lists
   - Update examples to show `behavior.action` pattern only
   - Document guardrails parameter usage
   - Explain that instructions execute automatically

**Impact:** Help documentation reflects simplified workflow

---

## PART 5: REMOVE AUTO-FORWARDING LOGIC

### 5.1 Actions Class - Remove Auto-Advancement

**File:** `agile_bot/src/actions/actions.py`

**Changes:**

1. **UPDATE** `close_current()` method (lines 150-172):
   - **REMOVE** automatic call to `_advance_to_next_action()` (line 170)
   - Action should be marked complete but NOT advance automatically
   - **IMPORTANT:** This method should only be called when user explicitly indicates completion
   - User must explicitly navigate to next action OR explicitly say "done" or "complete"

2. **UPDATE** `_get_next_action_reminder()` method (lines 226-236):
   - **UPDATE** reminder text to clarify user control
   - Change from: "After completing this action, the next action in sequence is `{next_action}`. When ready to continue, proceed with `{next_action}`."
   - To: "The next action in sequence is `{next_action}`. When you have completed this action and the user confirms they are done, navigate to `{next_action}`."
   - **CRITICAL:** Remind AI to wait for user confirmation before advancing

**Impact:** Actions no longer auto-advance - AI waits for user to say they're done before moving forward

---

### 5.2 Action Base Class - Remove Reminder Injection

**File:** `agile_bot/src/actions/action.py`

**Changes:**

1.  **UPDATE** `_inject_reminders_if_final()` method (lines 290-314):
** Update reminder text to NOT suggest auto-proceeding
   - Change language from "proceed to" to "navigate to when ready"

2. **VERIFY** `get_instructions()` method:
   - Ensure no auto-forwarding instructions are injected
   - Instructions should only describe the current action's work

**Impact:** No reminders suggesting auto-proceeding to next action

---

### 5.3 Reminders Module

**File:** `agile_bot/src/instructions/reminders.py`

**Changes:**

1. **UPDATE** `inject_reminder_to_instructions()` function:
   - Review reminder text format
   - Ensure reminders don't suggest auto-proceeding
   - Use language like "The next behavior/action is X. Navigate to it when ready."

**Impact:** Reminders inform but don't suggest auto-proceeding

---

### 5.4 Base Action Instructions

**Files:**
- `agile_bot/base_actions/build/build-instructions.txt`
- `agile_bot/base_actions/clarify/action_config.json` (if has instructions)
- `agile_bot/base_actions/strategy/action_config.json` (if has instructions)
- All other base action instruction files

**Changes:**

1. **SEARCH** for and **REMOVE/UPDATE** all instances of:
   - "proceed to next action"
   - "advance to next action"
   - "after completing this action, proceed to"
   - "when this action is complete, proceed to"
   - "MUST proceed to the next step"
   - Any language suggesting automatic advancement

2. **UPDATE** `build-instructions.txt` (line 71):
   - OLD: "When this action is complete, AI MUST pause and wait for human feedback. When human says 'done' or confirms completion, you MUST proceed to the next step: **decide_planning_criteria** (call the decide_planning_criteria action tool)."
   - NEW: "When this action is complete, AI MUST pause and wait for human feedback. When the user explicitly says they are done (e.g., 'done', 'complete', 'finished', 'ready to move on'), THEN you may navigate to the next action. Do NOT proceed until the user explicitly indicates completion."

3. **UPDATE** `build-instructions.txt` (line 57):
   - OLD: "DO NOT proceed to next action until storage is confirmed complete"
   - NEW: "Storage must be confirmed complete before the user navigates to the next action"

**Impact:** Base instructions don't instruct AI to auto-proceed

---

### 5.5 Behavior-Specific Instructions

**Files:**
- All `behavior.json` files in `agile_bot/bots/*/behaviors/*/behavior.json`
- All action config files in `agile_bot/bots/*/behaviors/*/actions/*/action_config.json`
- All instruction files in `agile_bot/bots/*/behaviors/*/instructions/` directories

**Changes:**

1. **SEARCH** all behavior-specific instruction files for:
   - "proceed to"
   - "advance to"
   - "after completing"
   - "when complete"
   - "MUST proceed"
   - "call the [next_action] action tool"
   - Any auto-forwarding language

2. **UPDATE** or **REMOVE** all instances

3. **SYSTEMATIC SEARCH COMMAND:**
   ```bash
   # Search all instruction files for auto-forwarding language
   grep -r "proceed to\|advance to\|after completing\|when complete\|MUST proceed" agile_bot/bots/*/behaviors/*/
   grep -r "proceed to\|advance to\|after completing\|when complete\|MUST proceed" agile_bot/base_actions/
   ```

**Impact:** Behavior-specific instructions don't suggest auto-proceeding

---

### 5.6 Render and Validate Actions

**Files:**
- `agile_bot/src/actions/render/render_action.py`
- `agile_bot/src/actions/validate/validate_action.py`

**Changes:**

1. **UPDATE** `inject_next_action_instructions()` method:
   - `render_action.py` line 166-167:
     - OLD: `return 'Proceed to validate action'`
     - NEW: `return 'The next action in sequence is validate. Navigate to it when the user indicates they are done with render.'`
   - `validate_action.py` line 269-270:
     - Already returns empty string (no change needed, or update to similar non-auto-forwarding message)

2. **REMOVE** `finalize_and_transition()` method:
   - `validate_action.py` lines 272-278
   - This method suggests auto-transitioning - remove it entirely

3. **SEARCH** for any calls to these methods and verify they don't cause auto-forwarding

**Impact:** Next action instructions inform but don't suggest auto-proceeding

---

### 5.7 MCP Server

**File:** `agile_bot/bots/story_bot/src/story_bot_mcp_server.py`

**Changes:**

1. **UPDATE** `close_current_action` tool (lines 93-116):
   - **REMOVE** automatic navigation to next action
   - **REMOVE** automatic navigation to next behavior
   - Tool should only mark action complete, NOT advance
   - Return status without auto-advancing

**Impact:** MCP tool doesn't auto-advance

---

### 5.8 AI Behavior Instructions

**File:** All instruction files (base and behavior-specific)

**Changes:**

1. **ADD** explicit instruction to all action instruction files:
   ```
   **CRITICAL WORKFLOW RULE:**
   - When this action's work is complete, PAUSE and wait for the user
   - DO NOT automatically navigate to the next action
   - ONLY navigate to the next action when the user explicitly says they are done
   - User completion signals: "done", "complete", "finished", "ready to move on", "next", etc.
   - If user says they're done, THEN navigate to the next action
   - If user doesn't say they're done, stay on current action
   ```

2. **UPDATE** all instruction files to include this rule at the end

**Impact:** AI clearly understands to wait for user completion signal before advancing

---

### 5.9 Verification Checklist - Auto-Forwarding

- [ ] `close_current()` does NOT call `_advance_to_next_action()` automatically
- [ ] `close_current()` only called when user explicitly indicates completion
- [ ] Reminders clarify that AI should wait for user confirmation
- [ ] Base instructions include explicit "wait for user done" rule
- [ ] Behavior-specific instructions include explicit "wait for user done" rule
- [ ] No instructions suggest auto-proceeding without user confirmation
- [ ] `inject_next_action_instructions()` methods removed
- [ ] `finalize_and_transition()` method removed
- [ ] MCP `close_current_action` doesn't auto-advance
- [ ] All instruction files reviewed for auto-forwarding language
- [ ] AI behavior clearly documented: only advance when user says "done"

---

## PART 6: TESTING AND VERIFICATION

### 6.1 Test Updates

**Files:**
- `agile_bot/test/panel/test_navigate_and_execute.js`
- `agile_bot/test/panel/test_manage_panel_session.js`
- Any other tests referencing operations or auto-forwarding

**Changes:**

1. **UPDATE** tests:
   - Remove operation-related test cases
   - Update tests to verify action execution without operations
   - Test guardrails flow between actions
   - Test parameter passing directly to actions
   - **VERIFY** actions do NOT auto-advance after completion
   - **VERIFY** user must explicitly navigate to next action

**Impact:** Tests verify new workflow correctly without auto-forwarding

---

### 6.2 Verification Checklist

- [ ] Actions execute automatically when navigated to
- [ ] Guardrails flow correctly from clarify → strategy → build → render/validate
- [ ] CLI displays actions without operations
- [ ] Panel displays actions without operations
- [ ] Help text updated to remove operations
- [ ] Parameters can be passed directly to actions
- [ ] Guardrails can be updated at any time
- [ ] No confirm() method exists
- [ ] Instructions property returns immediately when action executes
- [ ] **Actions do NOT auto-advance after completion**
- [ ] **AI only advances when user explicitly says they're done**
- [ ] **User completion signals clearly documented ("done", "complete", "finished", etc.)**
- [ ] **No reminders suggest auto-proceeding without user confirmation**
- [ ] **No instruction text mentions auto-forwarding without user confirmation**
- [ ] **All instruction files include explicit "wait for user done" rule**

---

## PART 7: MIGRATION NOTES

### 7.1 Breaking Changes

1. **CLI Commands:**
   - OLD: `behavior.action.instructions` or `behavior.action.confirm`
   - NEW: `behavior.action` (with parameters as action context)

2. **Panel Navigation:**
   - OLD: Click operation (instructions/confirm) under action
   - NEW: Click action directly (executes automatically)

3. **Parameters:**
   - OLD: Parameters on operations (e.g., `instructions --scope "Story"`)
   - NEW: Parameters on actions (e.g., `clarify --answers {...}`)

### 7.2 Guardrails Usage

**Documentation for CLI/MCP:**

- Guardrails can be passed to any action at any time
- Format: Pass guardrails dict via action context parameters
- Guardrails flow automatically: clarify → strategy → build → render/validate
- Guardrails can be updated: Pass new guardrails to any action to update them
- Actions save guardrails only when they have new data to save
- No separate "confirm" step - navigating to action executes instructions automatically

**Example:**
```
# Navigate to clarify - instructions execute automatically
clarify --answers {"q1": "answer1"}

# AI executes clarify action, then waits
# User says "done" or "complete" when finished with clarify
# AI then navigates to strategy - receives clarifications as guardrails
strategy --decisions {"decision1": "choice1"}

# AI executes strategy action, then waits
# User says "done" when finished with strategy
# AI then navigates to build - receives clarifications + strategy as guardrails
build --scope "Story Name"
```

**Key Principle:**
- Actions execute automatically when navigated to
- AI waits for user to say "done" before moving to next action
- User controls when to advance, not the AI

---

## SUMMARY

This refactoring simplifies the workflow by:
1. Removing the operations concept entirely
2. Making actions execute automatically when navigated to
3. Allowing guardrails to flow between actions and be updated at any time
4. Moving parameters directly to actions
5. Updating all displays (CLI and panel) to reflect this simpler model

The result is a cleaner, more intuitive workflow where actions are self-contained and guardrails flow naturally through the pipeline.
