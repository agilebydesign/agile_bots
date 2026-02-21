# Code Validation Report: Add Special Instructions

**Story:** Add Special Instructions  
**Scope:** Invoke Bot → Navigate Behavior Actions → Perform Behavior Action In Bot Workflow  
**Date:** 2026-02-20  
**Files scanned:** `src/bot/bot.py`, `src/cli/cli_session.py`, `src/instructions/instructions.py`, `test/invoke_bot/navigate_behavior_actions/test_perform_behavior_action_in_bot_workflow.py`

---

## Violations Found

### [Useless Comments / Docstrings] (8 in Add Special Instructions scope)

**1. stop_writing_useless_comments**
- Location: `test_perform_behavior_action_in_bot_workflow.TestAddSpecialInstructions`
- Status: Valid
- Source: Scanner
- Problem: Class docstring repeats story name and scenario purpose
- Fix: Remove class docstring
- Root Cause: Rule requires no docstrings; code must be self-explanatory

**2–7. stop_writing_useless_comments**
- Location: `test_perform_behavior_action_in_bot_workflow.TestAddSpecialInstructions` (6 test methods)
- Status: Valid
- Source: Scanner
- Problem: Gherkin-style docstrings (GIVEN/WHEN/THEN) document scenario steps
- Fix: Remove all docstrings; test names and step helpers document intent
- Root Cause: Rule: "No docstrings", "No test scenario comments"

**8. stop_writing_useless_comments**
- Location: `test_perform_behavior_action_in_bot_workflow` lines 507–509
- Status: Valid
- Source: Scanner
- Problem: Section header `# STORY: Add Special Instructions`
- Fix: Remove section header comments
- Root Cause: Rule: "DELETE ALL AI-WRITTEN COMMENTS"

---

### [Encapsulation] (2 in Add Special Instructions scope)

**9. enforce_encapsulation**
- Location: `bot.Bot.set_behavior_special_instructions`
- Status: Valid
- Source: Scanner
- Problem: Method returns `Dict[str, Any]` exposing internal structure
- Fix: Defer to broader Bot API refactor; all Bot methods (set_execution, submit_current_action, etc.) return dict for CLI/Panel compatibility
- Root Cause: Bot API convention; changing only these would create inconsistency

**10. enforce_encapsulation**
- Location: `bot.Bot.set_action_special_instructions`
- Status: Valid
- Source: Scanner
- Problem: Method returns `Dict[str, Any]` exposing internal structure
- Fix: Same as above; defer to broader Bot API refactor
- Root Cause: Bot API convention

---

### [Out of Scope / Pre-existing] (not in Add Special Instructions code)

- **chain_dependencies_properly:** `test_cli_complete_workflow_*` (TestExecuteEndToEndWorkflowUsingCLI) — parametrized `helper_class`; not in TestAddSpecialInstructions
- **enforce_encapsulation:** 23 other Bot/Instructions methods — pre-existing
- **place_imports_at_top:** `_activity_skip` before imports — module-level pattern, pre-existing
- **keep_classes_small:** Bot (1275 lines), CLISession (745 lines) — pre-existing
- **simplify_control_flow:** `execute`, `submit_current_action`, `run` — pre-existing
- **favor_code_representation:** `instructions.Instructions.update` parameter `data` — pre-existing
- **use_clear_function_parameters:** `_append_next_action_instructions_if_combine_next` — pre-existing
- **use_domain_language:** `generate_context_package` — pre-existing

---

## Summary

| Category | Count |
|----------|-------|
| Scanner violations in Add Special Instructions code | 10 |
| Valid, fixable in scope | 8 (stop_writing_useless_comments) |
| Valid, deferred (Broader refactor) | 2 (enforce_encapsulation) |
| False positive / Out of scope | 79 (other files, other stories) |

### Priority Fixes (in scope)
1. Remove `TestAddSpecialInstructions` class docstring
2. Remove 6 test method docstrings
3. Remove `# STORY: Add Special Instructions` section header

### Optional / Deferred
- Return typed result objects from `set_behavior_special_instructions` and `set_action_special_instructions` (requires Bot API refactor)

---

## Fixes Applied (2026-02-20)

- Removed `TestAddSpecialInstructions` class docstring
- Removed 6 test method docstrings (Gherkin-style)
- Removed `# STORY: Add Special Instructions` section header

**Result:** `stop_writing_useless_comments` violations reduced from 49 to 40 in scanned files. All 6 Add Special Instructions tests pass.
