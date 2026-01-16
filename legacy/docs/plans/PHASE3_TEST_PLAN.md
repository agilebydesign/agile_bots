# Phase 3: Testing Status End-to-End

**Goal**: Verify Status works across all channels before moving to next domain

**Key Principle**: Keep existing Epic/Sub-Epic/Story test structure intact. Only rename files (REPL → CLI).

---

## Test Files to Port/Create

| Test File | Source | Action | Notes |
|-----------|--------|--------|-------|
| `test_api_status.py` | `test_invoke_bot_directly.py` | **COPY** entire file | Direct API tests already work |
| `test_cli_status.py` | `test_navigate_behaviors_using_repl_commands.py`<br>`test_initialize_repl_session.py` | **RENAME** files | Just update REPL→CLI in names/imports |
| `test_panel_status.js` | Story scenario documents | **NEW** | Panel tests don't exist yet |

---

## 3.1 Direct API Tests

**File**: `agile_bot/test/test_api_status.py`  
**Source**: `test_invoke_bot_directly.py` (COPY ENTIRE FILE)

**Action**:
```bash
# Copy existing file - tests already work
cp agile_bot/bots/base_bot/test/test_invoke_bot_directly.py \
   agile_bot/test/test_api_status.py
```

**Keep**:
- ✓ All test classes with Epic/Sub-Epic/Story structure
- ✓ All helpers (`given_*`, `when_*`, `then_*`)
- ✓ All fixtures
- ✓ Test names and structure

**No Changes Needed** - These direct API tests already work with Bot domain objects.

**Test Classes Included**:
```python
# From test_invoke_bot_directly.py - keep ALL of these
class TestAccessBotPaths: ...
class TestLoadBotConfiguration: ...
class TestLoadBotBehaviors: ...
class TestInvokeBehaviorActionsInOrder: ...
class TestInsertContextIntoInstructions: ...
class TestInjectNextBehaviorReminder: ...
class TestCloseCurrentAction: ...
# ... etc (all test classes)
```

---

## 3.2 CLI Tests

**Files**: 
- `agile_bot/test/test_cli_navigate_and_status.py` (from `test_navigate_behaviors_using_repl_commands.py`)
- `agile_bot/test/test_cli_session.py` (from `test_initialize_repl_session.py`)

### 3.2a: test_cli_navigate_and_status.py

**Source**: `test_navigate_behaviors_using_repl_commands.py` (RENAME FILE)

**Action**:
```bash
# Rename file
cp agile_bot/bots/base_bot/test/test_navigate_behaviors_using_repl_commands.py \
   agile_bot/test/test_cli_navigate_and_status.py
```

**Changes**:
1. Update imports:
   ```python
   # OLD
   from agile_bot.bots.base_bot.src.repl_cli.repl_session import REPLSession
   
   # NEW  
   from agile_bot.src.cli.cli_session import CLISession
   ```

2. Update class names:
   ```python
   # OLD
   class TestExitREPL:
   
   # NEW
   class TestExitCLI:
   ```

3. Update variable names in tests:
   ```python
   # OLD
   repl_session = REPLSession(bot=bot, workspace_directory=workspace)
   
   # NEW
   cli_session = CLISession(bot=bot, workspace_directory=workspace)
   ```

**Keep ALL test classes**:
- `TestNavigateToBehaviorActionAndExecute`
- `TestNavigateSequentially`
- `TestExitCLI` (was `TestExitREPL`)
- `TestDisplayBotHierarchyTree` ← **Status tests here**
- `TestDisplayCurrentPosition` ← **Status tests here**

### 3.2b: test_cli_session.py

**Source**: `test_initialize_repl_session.py` (RENAME FILE)

**Action**:
```bash
# Rename file
cp agile_bot/bots/base_bot/test/test_initialize_repl_session.py \
   agile_bot/test/test_cli_session.py
```

**Changes**:
1. Update imports (same as above)
2. Update class names:
   ```python
   # OLD
   class TestStartREPLSession:
   class TestStartREPLInPipeMode:
   
   # NEW
   class TestStartCLISession:
   class TestStartCLIInPipeMode:
   ```

**Keep ALL test classes**:
- `TestStartCLISession` (was `TestStartREPLSession`)
- `TestStartCLIInPipeMode` (was `TestStartREPLInPipeMode`)
- `TestDisplayPipedModeInstructionsForAIAgents`
- `TestDetectAndConfigureTTYNonTTYInput` ← **Adapter selection tests here**
- `TestLoadWorkspaceContext`
- `TestDisplayCLIHeader`
- `TestDisplayHeadlessModeStatus`

---

## 3.3 Panel Tests

**File**: `agile_bot/test/test_panel_status.js`  
**Source**: Story scenario documents (NEW - doesn't exist yet)

**Action**: Write new tests based on story scenarios

**Story Scenarios to Implement**:

1. **Invoke Bot Through Panel > Manage Bot Information > Open Panel**
   - Scenario: Panel opens and displays bot status
   - Test: Panel subprocess requests status, receives JSON, renders HTML

2. **Invoke Bot Through Panel > Manage Bot Information > Refresh Panel**
   - Scenario: User clicks refresh, panel updates status
   - Test: Panel sends status command again, receives updated JSON

**Test Structure**:

```javascript
// test/test_panel_status.js
/**
 * Tests for Invoke Bot Through Panel Epic > Manage Bot Information Sub-Epic
 * 
 * Story Coverage:
 * - Open Panel (status display)
 * - Refresh Panel (status update)
 */

const { spawn } = require('child_process');
const assert = require('assert');
const path = require('path');

describe('Epic: Invoke Bot Through Panel', () => {
    
    describe('Sub-Epic: Manage Bot Information', () => {
        
        describe('Story: Open Panel', () => {
            
            it('Scenario: Panel opens and displays bot status', async () => {
                /**
                 * GIVEN: Bot is at exploration.validate
                 * WHEN: Panel subprocess sends 'status' command
                 * THEN: CLI returns Status JSON with current position
                 */
                
                // Test implementation...
            });
            
            it('Scenario: Panel displays status with no current action', async () => {
                /**
                 * GIVEN: Bot is idle (no current action)
                 * WHEN: Panel requests status
                 * THEN: Status JSON has null current_behavior/current_action
                 */
                
                // Test implementation...
            });
        });
        
        describe('Story: Refresh Panel', () => {
            
            it('Scenario: User clicks refresh button', async () => {
                /**
                 * GIVEN: Panel is open with status displayed
                 * WHEN: User clicks refresh
                 * THEN: Panel sends status command, receives updated JSON
                 */
                
                // Test implementation...
            });
        });
    });
    
    describe('Sub-Epic: Status View Rendering', () => {
        
        describe('Story: Render Status HTML', () => {
            
            it('Scenario: StatusView renders Status JSON to HTML', () => {
                /**
                 * GIVEN: Status JSON from CLI
                 * WHEN: StatusView.render() is called
                 * THEN: Returns HTML with progress path, stage, current action
                 */
                
                // Test implementation...
            });
        });
    });
});
```

**Test Fixtures Needed** (create these):
- `test/fixtures/bot_at_exploration_validate/` - Bot at exploration.validate state
- `test/fixtures/bot_idle/` - Bot with no current behavior/action  
- `test/fixtures/bot_at_shape_clarify/` - Bot at shape.clarify state

---

## Verification Checklist

**API Tests** (from existing `test_invoke_bot_directly.py`):
- [ ] File copied to `agile_bot/test/test_api_status.py`
- [ ] All test classes preserved
- [ ] Tests run and pass
- [ ] No structural changes made

**CLI Tests** (from existing REPL test files):
- [ ] `test_navigate_behaviors_using_repl_commands.py` → `test_cli_navigate_and_status.py`
- [ ] `test_initialize_repl_session.py` → `test_cli_session.py`
- [ ] Imports updated (REPLSession → CLISession)
- [ ] Class names updated (REPL → CLI)
- [ ] All test classes preserved
- [ ] Tests run and pass

**Panel Tests** (new):
- [ ] `test_panel_status.js` created
- [ ] Epic/Sub-Epic/Story structure used
- [ ] Scenarios from story documents implemented
- [ ] Test fixtures created
- [ ] Tests run and pass

---

## Run All Status Tests

```bash
# Run API tests
pytest agile_bot/test/test_api_status.py -v

# Run CLI tests  
pytest agile_bot/test/test_cli_navigate_and_status.py -v
pytest agile_bot/test/test_cli_session.py -v

# Run Panel tests
npm test agile_bot/test/test_panel_status.js
```

**Success Criteria**:
- All API tests pass (direct Bot method calls)
- All CLI tests pass (TTY and JSON modes)
- All Panel tests pass (subprocess communication and HTML rendering)
- Status works end-to-end across all three channels
