# Status Domain Test Porting Guide

**Date**: 2026-01-08  
**Purpose**: Specify exactly which existing tests to port for Status domain implementation

---

## Test Porting Strategy

**KEEP** existing Epic/Sub-Epic/Story test structure  
**RENAME** files only (REPL → CLI)  
**UPDATE** imports and class names (REPLSession → CLISession)  
**DO NOT** restructure tests or change test organization

**CRITICAL: Mode-Specific Testing Pattern**

For **EVERY** CLI feature, create three mode-specific test stories:
1. **Interactive Mode (TTY)** - Auto-detected when `sys.stdin.isatty() == True`
2. **Piped Mode (Markdown)** - Auto-detected when `sys.stdin.isatty() == False`
3. **JSON Mode** - Explicitly set via `CLISession(..., mode='json')`

Each mode story verifies the same functionality but with mode-appropriate format expectations (TTY/Markdown/JSON).

---

## Files to Port

### 1. Direct API Tests (Already Work)

**Source**: `test_invoke_bot_directly.py`  
**Destination**: Copy to `agile_bot/test/test_api_status.py`  
**Action**: **COPY ENTIRE FILE** - no changes needed

**Reason**: These tests already test Bot domain methods directly. They work as-is for Status.

**Test Classes** (keep all):
- All existing test classes with Epic/Sub-Epic/Story structure
- All helper functions (`given_*`, `when_*`, `then_*`)
- All fixtures

---

## CLI Features (All Require Three Mode Stories)

### 2. Launch CLI

**Source**: `test_initialize_repl_session.py`  
**Destination**: Rename to `agile_bot/test/test_initialize_cli_session.py`  
**Action**: **RENAME FILE + UPDATE IMPORTS + ADD MODE STORIES**

#### Interactive Mode (TTY)

```python
class TestStartCLISessionInTTYMode:
    """
    Story: Launch CLI in Interactive Mode (TTY Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Initialize CLI Session
    """
    def test_cli_launches_in_interactive_mode(...)
    def test_cli_loads_existing_behavior_action_state_on_launch(...)
    def test_cli_displays_status_on_launch(...)  # Verifies TTY format
    def test_cli_displays_header_section(...)  # Verifies TTY header format
    def test_cli_displays_bot_section(...)  # Verifies TTY bot section format
```

#### Piped Mode (Markdown)

```python
class TestStartCLISessionInPipeMode:
    """
    Story: Launch CLI in Pipe Mode (Markdown Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Initialize CLI Session
    """
    def test_cli_launches_in_pipe_mode(...)
    def test_cli_displays_status_in_markdown_format(...)  # Verifies markdown format
    def test_cli_displays_header_section_in_markdown(...)  # Verifies markdown header
    def test_cli_displays_bot_section_in_markdown(...)  # Verifies markdown bot section
```

#### JSON Mode

```python
class TestStartCLISessionInJSONMode:
    """
    Story: Launch CLI in JSON Mode
    Epic: Invoke Bot Through CLI
    Sub-Epic: Initialize CLI Session
    """
    def test_cli_launches_in_json_mode(...)  # JSON mode initialization
    def test_cli_displays_status_in_json_format(...)  # Verifies JSON format
    def test_cli_displays_header_section_in_json(...)  # Verifies JSON header
    def test_cli_displays_bot_section_in_json(...)  # Verifies JSON bot section
```

**Additional Stories** (not mode-specific):
- `TestDetectAndConfigureTTYNonTTYInput` - Tests mode detection
- `TestLoadWorkspaceContext` - Tests workspace loading

**Changes to Make**:
1. Rename file: `test_initialize_repl_session.py` → `test_initialize_cli_session.py`
2. Update imports:
   ```python
   # OLD
   from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
   
   # NEW
   from agile_bot.src.cli.cli_session import CLISession
   ```
3. Update class names:
   - `TestStartREPLSession` → `TestStartCLISessionInTTYMode`
   - `TestStartREPLInPipeMode` → `TestStartCLISessionInPipeMode`
   - Add new: `TestStartCLISessionInJSONMode`
4. Update variable names:
   ```python
   # OLD
   repl_session = REPLSession(...)
   
   # NEW
   cli_session = CLISession(...)  # For TTY/Markdown (auto-detect)
   cli_session = CLISession(..., mode='json')  # For JSON (explicit)
   ```

---

### 3. Navigate Using CLI Dot Notation

**Source**: `test_navigate_behaviors_using_repl_commands.py`  
**Destination**: Rename to `agile_bot/test/test_navigate_behaviors_using_cli_commands.py`  
**Action**: **RENAME FILE + UPDATE IMPORTS + ADD MODE STORIES**

#### Interactive Mode (TTY)

```python
class TestNavigateToBehaviorActionAndExecuteInTTYMode:
    """
    Story: Navigate to Behavior Action and Execute (TTY Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Navigate Behavior Action Status
    """
    def test_user_navigates_with_behavior_only(...)  # Verifies TTY output format
    def test_user_navigates_with_behavior_dot_action(...)  # Verifies TTY output format
    def test_user_navigates_with_full_dot_notation(...)  # Verifies TTY output format
    def test_user_enters_invalid_behavior_in_dot_notation(...)  # Verifies TTY error format
```

#### Piped Mode (Markdown)

```python
class TestNavigateToBehaviorActionAndExecuteInPipeMode:
    """
    Story: Navigate to Behavior Action and Execute (Markdown Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Navigate Behavior Action Status
    """
    def test_user_navigates_with_behavior_only(...)  # Verifies markdown output format
    def test_user_navigates_with_behavior_dot_action(...)  # Verifies markdown output format
    def test_user_navigates_with_full_dot_notation(...)  # Verifies markdown output format
    def test_user_enters_invalid_behavior_in_dot_notation(...)  # Verifies markdown error format
```

#### JSON Mode

```python
class TestNavigateToBehaviorActionAndExecuteInJSONMode:
    """
    Story: Navigate to Behavior Action and Execute (JSON Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Navigate Behavior Action Status
    """
    def test_user_navigates_with_behavior_only(...)  # Verifies JSON output format
    def test_user_navigates_with_behavior_dot_action(...)  # Verifies JSON output format
    def test_user_navigates_with_full_dot_notation(...)  # Verifies JSON output format
    def test_user_enters_invalid_behavior_in_dot_notation(...)  # Verifies JSON error format
```

**Changes to Make**:
1. Rename file: `test_navigate_behaviors_using_repl_commands.py` → `test_navigate_behaviors_using_cli_commands.py`
2. Update imports: `REPLSession` → `CLISession`
3. Split existing test class into three mode-specific classes
4. Update variable names: `repl_session` → `cli_session` (with appropriate mode)

---

### 4. Navigate Using Next/Back Commands

**Source**: `test_navigate_behaviors_using_repl_commands.py`  
**Destination**: Same file as above  
**Action**: **ADD MODE STORIES**

#### Interactive Mode (TTY)

```python
class TestNavigateSequentiallyInTTYMode:
    """
    Story: Navigate Sequentially (TTY Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Navigate Behavior Action Status
    """
    def test_user_navigates_with_next_command(...)  # Verifies TTY output format
    def test_user_navigates_with_back_command(...)  # Verifies TTY output format
```

#### Piped Mode (Markdown)

```python
class TestNavigateSequentiallyInPipeMode:
    """
    Story: Navigate Sequentially (Markdown Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Navigate Behavior Action Status
    """
    def test_user_navigates_with_next_command(...)  # Verifies markdown output format
    def test_user_navigates_with_back_command(...)  # Verifies markdown output format
```

#### JSON Mode

```python
class TestNavigateSequentiallyInJSONMode:
    """
    Story: Navigate Sequentially (JSON Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Navigate Behavior Action Status
    """
    def test_user_navigates_with_next_command(...)  # Verifies JSON output format
    def test_user_navigates_with_back_command(...)  # Verifies JSON output format
```

---

### 5. Display Status

**Source**: `test_navigate_behaviors_using_repl_commands.py`  
**Destination**: Same file as above  
**Action**: **ADD MODE STORIES**

#### Interactive Mode (TTY)

```python
class TestDisplayBotHierarchyTreeInTTYMode:
    """
    Story: Display Bot Hierarchy Tree with Progress Indicators (TTY Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Navigate Behavior Action Status
    """
    def test_user_views_bot_hierarchy_with_status_command(...)  # Verifies TTY format
    def test_user_views_current_position_in_status(...)  # Verifies TTY format
    def test_cli_displays_progress_section_with_current_position(...)  # Verifies TTY format
    def test_cli_displays_behavior_in_progress_section(...)  # Verifies TTY format
```

#### Piped Mode (Markdown)

```python
class TestDisplayBotHierarchyTreeInPipeMode:
    """
    Story: Display Bot Hierarchy Tree with Progress Indicators (Markdown Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Navigate Behavior Action Status
    """
    def test_user_views_bot_hierarchy_with_status_command(...)  # Verifies markdown format
    def test_user_views_current_position_in_status(...)  # Verifies markdown format
    def test_cli_displays_progress_section_with_current_position(...)  # Verifies markdown format
    def test_cli_displays_behavior_in_progress_section(...)  # Verifies markdown format
```

#### JSON Mode

```python
class TestDisplayBotHierarchyTreeInJSONMode:
    """
    Story: Display Bot Hierarchy Tree with Progress Indicators (JSON Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Navigate Behavior Action Status
    """
    def test_user_views_bot_hierarchy_with_status_command(...)  # Verifies JSON format
    def test_user_views_current_position_in_status(...)  # Verifies JSON format
    def test_cli_displays_progress_section_with_current_position(...)  # Verifies JSON format
    def test_cli_displays_behavior_in_progress_section(...)  # Verifies JSON format
```

---

### 6. Get Action Instructions Through CLI

**Source**: `test_execute_actions_using_repl.py`  
**Destination**: Rename to `agile_bot/test/test_execute_actions_using_cli.py`  
**Action**: **RENAME FILE + UPDATE IMPORTS + ADD MODE STORIES**

#### Interactive Mode (TTY)

```python
class TestViewInstructionsInTTYMode:
    """
    Story: Get Action Instructions Through CLI (TTY Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Execute Actions Using CLI
    """
    def test_user_gets_instructions_for_build_action(...)  # Verifies TTY format
```

#### Piped Mode (Markdown)

```python
class TestViewInstructionsInPipeMode:
    """
    Story: Get Action Instructions Through CLI (Markdown Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Execute Actions Using CLI
    """
    def test_user_gets_instructions_for_build_action(...)  # Verifies markdown format
```

#### JSON Mode

```python
class TestViewInstructionsInJSONMode:
    """
    Story: Get Action Instructions Through CLI (JSON Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Execute Actions Using CLI
    """
    def test_user_gets_instructions_for_build_action(...)  # Verifies JSON format
```

---

### 7. Confirm Work Through CLI

**Source**: `test_execute_actions_using_repl.py`  
**Destination**: Same file as above  
**Action**: **ADD MODE STORIES**

#### Interactive Mode (TTY)

```python
class TestConfirmWithParametersInTTYMode:
    """
    Story: Confirm Work Through CLI (TTY Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Execute Actions Using CLI
    """
    def test_user_confirms_build_work(...)  # Verifies TTY format
```

#### Piped Mode (Markdown)

```python
class TestConfirmWithParametersInPipeMode:
    """
    Story: Confirm Work Through CLI (Markdown Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Execute Actions Using CLI
    """
    def test_user_confirms_build_work(...)  # Verifies markdown format
```

#### JSON Mode

```python
class TestConfirmWithParametersInJSONMode:
    """
    Story: Confirm Work Through CLI (JSON Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Execute Actions Using CLI
    """
    def test_user_confirms_build_work(...)  # Verifies JSON format
```

---

### 8. Filter Work Using Scope

**Source**: `test_manage_scope_using_repl.py`  
**Destination**: Rename to `agile_bot/test/test_manage_scope_using_cli.py`  
**Action**: **RENAME FILE + UPDATE IMPORTS + ADD MODE STORIES**

#### Interactive Mode (TTY)

```python
class TestSetScopeInTTYMode:
    """
    Story: Filter Work Using Scope (TTY Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Manage Scope Using CLI
    """
    def test_user_sets_scope_filter(...)  # Verifies TTY format
    def test_user_views_current_scope(...)  # Verifies TTY format
```

#### Piped Mode (Markdown)

```python
class TestSetScopeInPipeMode:
    """
    Story: Filter Work Using Scope (Markdown Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Manage Scope Using CLI
    """
    def test_user_sets_scope_filter(...)  # Verifies markdown format
    def test_user_views_current_scope(...)  # Verifies markdown format
```

#### JSON Mode

```python
class TestSetScopeInJSONMode:
    """
    Story: Filter Work Using Scope (JSON Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Manage Scope Using CLI
    """
    def test_user_sets_scope_filter(...)  # Verifies JSON format
    def test_user_views_current_scope(...)  # Verifies JSON format
```

---

### 9. View Available Commands (Help)

**Source**: `test_get_help_using_repl.py`  
**Destination**: Rename to `agile_bot/test/test_get_help_using_cli.py`  
**Action**: **RENAME FILE + UPDATE IMPORTS + ADD MODE STORIES**

#### Interactive Mode (TTY)

```python
class TestDisplayActionHelpUsingCLIInTTYMode:
    """
    Story: View Available Commands (Help) (TTY Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Get Help Using CLI
    """
    def test_user_views_all_available_commands(...)  # Verifies TTY format
    def test_user_views_examples_in_help(...)  # Verifies TTY format
```

#### Piped Mode (Markdown)

```python
class TestDisplayActionHelpUsingCLIInPipeMode:
    """
    Story: View Available Commands (Help) (Markdown Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Get Help Using CLI
    """
    def test_user_views_all_available_commands(...)  # Verifies markdown format
    def test_user_views_examples_in_help(...)  # Verifies markdown format
```

#### JSON Mode

```python
class TestDisplayActionHelpUsingCLIInJSONMode:
    """
    Story: View Available Commands (Help) (JSON Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Get Help Using CLI
    """
    def test_user_views_all_available_commands(...)  # Verifies JSON format
    def test_user_views_examples_in_help(...)  # Verifies JSON format
```

---

### 10. Exit CLI Session

**Source**: `test_navigate_behaviors_using_repl_commands.py`  
**Destination**: Same file as above  
**Action**: **ADD MODE STORIES**

#### Interactive Mode (TTY)

```python
class TestExitCLIInTTYMode:
    """
    Story: Exit CLI Session (TTY Mode)
    Epic: Invoke Bot Through CLI
    """
    def test_user_exits_cli_with_exit_command(...)  # Verifies TTY format
```

#### Piped Mode (Markdown)

```python
class TestExitCLIInPipeMode:
    """
    Story: Exit CLI Session (Markdown Mode)
    Epic: Invoke Bot Through CLI
    """
    def test_user_exits_cli_with_exit_command(...)  # Verifies markdown format
```

#### JSON Mode

```python
class TestExitCLIInJSONMode:
    """
    Story: Exit CLI Session (JSON Mode)
    Epic: Invoke Bot Through CLI
    """
    def test_user_exits_cli_with_exit_command(...)  # Verifies JSON format
```

---

### 11. Handle Operation Errors

**Source**: `test_execute_actions_using_repl.py`  
**Destination**: Same file as above  
**Action**: **ADD MODE STORIES**

#### Interactive Mode (TTY)

```python
class TestHandleErrorsAndValidationInTTYMode:
    """
    Story: Handle Operation Errors (TTY Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Execute Actions Using CLI
    """
    def test_user_enters_invalid_command(...)  # Verifies TTY error format
```

#### Piped Mode (Markdown)

```python
class TestHandleErrorsAndValidationInPipeMode:
    """
    Story: Handle Operation Errors (Markdown Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Execute Actions Using CLI
    """
    def test_user_enters_invalid_command(...)  # Verifies markdown error format
```

#### JSON Mode

```python
class TestHandleErrorsAndValidationInJSONMode:
    """
    Story: Handle Operation Errors (JSON Mode)
    Epic: Invoke Bot Through CLI
    Sub-Epic: Execute Actions Using CLI
    """
    def test_user_enters_invalid_command(...)  # Verifies JSON error format
```

---

## Panel Tests (NEW - No Existing Tests)

**Source**: Story scenarios from `docs/stories/` and `docs/crc/walkthrough-realizations.md`  
**Destination**: Create new `agile_bot/test/test_panel_status.js`  
**Action**: **WRITE NEW TESTS** (panel tests don't exist yet)

**Note**: Panel tests use JSON mode exclusively (web views consume JSON)

**Test Structure** (follow Epic/Sub-Epic/Story pattern):

```javascript
/**
 * Epic: Invoke Bot Through Panel
 * Sub-Epic: Manage Bot Information
 * Story: Open Panel
 */
describe('Open Panel', () => {
    it('should receive Status JSON from CLI subprocess', async () => {
        // Walkthrough Scenario 1, lines 37-90
    });
    
    it('should handle Status JSON when no current action', async () => {
        // Edge case: idle bot
    });
});

/**
 * Epic: Invoke Bot Through Panel
 * Sub-Epic: Manage Bot Information
 * Story: Refresh Panel
 */
describe('Refresh Panel', () => {
    it('should refresh status when user clicks refresh', async () => {
        // Walkthrough Scenario 2, lines 124-164
    });
});

/**
 * Epic: Invoke Bot Through Panel
 * Sub-Epic: Manage Bot Information
 * Story: Render Status View
 */
describe('StatusView HTML Rendering', () => {
    it('should render Status JSON to HTML', () => {
        // Walkthrough Scenario 1, lines 95-116
    });
    
    it('should render Status with no current action', () => {
        // Edge case: idle status rendering
    });
});
```

**Based On**:
- `docs/crc/walkthrough-realizations.md` Scenario 1 (lines 37-116)
- `docs/crc/walkthrough-realizations.md` Scenario 2 (lines 124-164)

---

## Summary

| Feature | Source File | Destination File | Action | Mode Stories Required |
|---------|-------------|------------------|--------|---------------------|
| Launch CLI | `test_initialize_repl_session.py` | `test_initialize_cli_session.py` | RENAME + ADD MODES | ✅ TTY, Markdown, JSON |
| Navigate Dot Notation | `test_navigate_behaviors_using_repl_commands.py` | `test_navigate_behaviors_using_cli_commands.py` | RENAME + ADD MODES | ✅ TTY, Markdown, JSON |
| Navigate Next/Back | Same as above | Same as above | ADD MODES | ✅ TTY, Markdown, JSON |
| Display Status | Same as above | Same as above | ADD MODES | ✅ TTY, Markdown, JSON |
| Get Instructions | `test_execute_actions_using_repl.py` | `test_execute_actions_using_cli.py` | RENAME + ADD MODES | ✅ TTY, Markdown, JSON |
| Confirm Work | Same as above | Same as above | ADD MODES | ✅ TTY, Markdown, JSON |
| Filter Scope | `test_manage_scope_using_repl.py` | `test_manage_scope_using_cli.py` | RENAME + ADD MODES | ✅ TTY, Markdown, JSON |
| View Help | `test_get_help_using_repl.py` | `test_get_help_using_cli.py` | RENAME + ADD MODES | ✅ TTY, Markdown, JSON |
| Exit CLI | Same as Navigate | Same as Navigate | ADD MODES | ✅ TTY, Markdown, JSON |
| Handle Errors | Same as Execute | Same as Execute | ADD MODES | ✅ TTY, Markdown, JSON |
| Panel Tests | N/A (new) | `test_panel_status.js` | CREATE NEW | JSON only (web views) |

**Total Tests**: ~150+ tests (existing tests split into 3 modes each + new panel tests)

**Epic/Sub-Epic/Story Structure**: **PRESERVED** - no changes to test organization

**Only Changes**:
- File names (REPL → CLI)
- Import paths (old base_bot paths → new agile_bot paths)
- Class names (REPL → CLI, add mode suffix)
- Variable names (repl_session → cli_session)
- **NEW**: Split each feature into 3 mode-specific test classes

**Test Methodology**:
- Tests use **hard-coded expected values**, NOT adapter-generated values
- Tests verify exact format returned by adapters (TTY/Markdown/JSON syntax)
- Mode selection: Auto-detect for TTY/Markdown, explicit `mode='json'` for JSON
