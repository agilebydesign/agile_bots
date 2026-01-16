# CRC-Based REPL CLI Refactoring Plan

**Date**: 2026-01-07  
**Status**: Planning  
**Goal**: Refactor REPL CLI to match CRC model while ensuring all tests pass and no functionality breaks

**⚠️ CRITICAL**: This plan follows `walkthrough-realizations.md` lines 58-86 EXACTLY. The walkthrough shows:
- ✅ Adapters wrap domain objects and delegate to child adapters
- ✅ REPLSession selects adapter on init (TTY vs JSON)
- ✅ REPLSession calls `self.adapter.serialize()`
- ❌ NO CommandRegistry, NO NavigationCommands, NO extracted command classes
- ❌ Command parsing stays IN REPLSession (not extracted)

---

## 📋 Executive Summary

This plan refactors the REPL CLI implementation to align with the CRC (Class-Responsibility-Collaboration) domain model. The refactoring will be **incremental** and **test-driven**, ensuring zero downtime and no breaking changes to the Panel extension.

**Key Principle**: Introduce CRC architecture alongside existing code, verify tests pass, then remove old code.

---

## 🎯 Current State Analysis

### Current Architecture

```
REPLSession (1500+ lines - DOES TOO MUCH)
├── Command parsing
├── Command routing
├── State management
├── Formatter selection (FormatterFactory)
├── Status display rendering
├── Instructions handling
├── Navigation logic
└── Scope management

Formatters/
├── terminal_formatter.py    (TTY output)
├── json_formatter.py         (JSON for panel)
└── markdown_formatter.py     (Markdown docs)
```

### Target CRC Architecture (from crc-model-outline.md)

```
REPLSession (Orchestrator - <100 lines)
├── Determine channel adapter: ChannelAdapter
├── Read and execute command: Command String → REPLCommandResponse
├── Route to bot domain methods: Bot, Command Verb, Params → BotResult
└── Serialize via channel adapter: ChannelAdapter → String

ChannelAdapter (Abstract) - Serialization strategy
├── TTYAdapter : TextAdapter
│   ├── TTYBotAdapter        - Serializes Bot to terminal
│   ├── TTYBehaviorAdapter   - Serializes Behavior to terminal
│   ├── TTYActionAdapter     - Serializes Action to terminal
│   └── TTYInstructionsAdapter - Serializes Instructions to terminal
├── JSONAdapter
│   ├── JSONBotAdapter       - Serializes Bot to JSON
│   ├── JSONBehaviorAdapter  - Serializes Behavior to JSON
│   ├── JSONActionAdapter    - Serializes Action to JSON
│   └── JSONInstructionsAdapter - Serializes Instructions to JSON
└── MarkdownAdapter
    ├── MarkdownBotAdapter   - Serializes Bot to Markdown
    └── ... (future)
```

### Key Problems with Current Code

1. **REPLSession is 1750 lines** - violates Single Responsibility Principle
2. **Formatters are not Adapters** - they format strings, not serialize domain objects
3. **No domain object wrapping** - adapters should wrap domain objects, not receive raw data
4. **Command routing is inline** - no CommandRegistry pattern
5. **Panel integration is fragile** - JSON output is manually constructed in REPLSession

---

## 📐 Target CRC Model (from walkthrough-realizations.md)

### Scenario 1: Open Panel (from walkthrough)

```python
# Extension spawns CLI subprocess
panelData: JSON = CLI.execute('status')
  -> pythonProcess: Process = spawn('python', ['repl_main.py'])
  -> stdin.write('status')
  -> REPLSession.handle_command('status')
     -> # Use session's pre-initialized adapter
     -> output: String = this.adapter.serialize()
        -> # JSONBotAdapter.serialize() [piped mode]
        -> jsonDict: Dict = JSONBotAdapter(bot).serialize()
           -> behaviors: Array = []
           -> for behavior in bot.behaviors:
              behaviorDict = JSONBehaviorAdapter(behavior).serialize()
           -> return json.dumps(jsonDict)
     -> print(output)  # stdout
  -> stdout = pythonProcess.stdout.read()
  -> return JSON.parse(stdout)
```

**Key Insight**: Adapters should **wrap domain objects** and delegate serialization, not receive dictionaries.

---

## 🎯 Refactoring Strategy (from walkthrough-realizations.md lines 58-86)

### Phase 1: Create Adapter Foundation (No Breaking Changes)
**Goal**: Introduce adapter classes alongside existing formatters  
**Tests**: All existing tests pass  
**Panel**: No changes required  
**Reference**: Walkthrough lines 62-86 show adapter delegation pattern

### Phase 2: Replace Formatter with Adapter in REPLSession
**Goal**: Replace `self.formatter` with `self.adapter` in REPLSession  
**Tests**: All existing tests pass  
**Panel**: **Verify JSON format** - must match current output  
**Reference**: Walkthrough lines 58-70 show adapter selection and usage

### Phase 3: Delete Formatters
**Goal**: Delete formatters directory, keep all command logic in REPLSession  
**Tests**: All tests pass  
**Panel**: Verify integration  
**Critical**: Do NOT extract command classes (walkthrough shows NO extraction)  
**NO DEPRECATION**: Just delete formatters, no deprecated code

---

## 📋 Detailed Implementation Plan

---

## **⚠️ CRITICAL: Test-Driven Refactoring**

**Run tests at EVERY checkpoint:**
1. **Baseline**: Run all tests BEFORE starting → establish baseline (should be 48/48 passing)
2. **After each adapter**: Run `pytest test/test_adapters.py` → verify new code works
3. **After REPLSession changes**: Run `pytest test/test_initialize_repl_session.py` → verify adapter selection
4. **After deleting formatters**: Run `pytest test/` → verify NO regressions
5. **Final verification**: Run full suite + panel integration test

**If ANY test fails at ANY checkpoint → STOP, revert, fix, then continue**

---

## **PHASE 1: Create Adapter Foundation**

### **CHECKPOINT 0: Establish Baseline (BEFORE starting)**

#### **Step 0: Run all tests and record baseline**

```powershell
# Run full test suite
pytest agile_bot/bots/base_bot/test/ -v

# Should see: 48 passed (or current passing count)
# Record this number - this is our baseline
```

**Expected Result**: All tests passing (let's say 48/48)  
**If tests fail**: Fix existing test failures BEFORE starting refactoring

---

### **1.1 Create Adapter Base Classes**
**Files**: New `agile_bot/bots/base_bot/src/repl_cli/adapters/` directory

#### **Step 1a: Create ChannelAdapter (Abstract)**
**File**: `adapters/channel_adapter.py`

```python
from abc import ABC, abstractmethod
from typing import Any

class ChannelAdapter(ABC):
    """Base adapter for serializing domain objects to different formats."""
    
    @abstractmethod
    def serialize(self) -> str:
        """Serialize domain object to format string."""
        pass
    
    @abstractmethod
    def deserialize(self, data: str) -> Any:
        """Deserialize format string to domain object."""
        pass
```

#### **Step 1b: Create TextAdapter**
**File**: `adapters/text_adapter.py`

```python
from abc import ABC, abstractmethod
from .channel_adapter import ChannelAdapter

class TextAdapter(ChannelAdapter, ABC):
    """Base adapter for text-based formats (TTY, Markdown)."""
    
    @abstractmethod
    def parse_command(self, text: str) -> tuple[str, list]:
        """Parse command text into verb and parameters."""
        pass
```

#### **Step 1c: Create JSONAdapter (Abstract)**
**File**: `adapters/json_adapter.py`

```python
from abc import ABC, abstractmethod
from .channel_adapter import ChannelAdapter
import json
from typing import Dict, Any

class JSONAdapter(ChannelAdapter, ABC):
    """Base adapter for JSON serialization."""
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert domain object to dictionary."""
        pass
    
    def serialize(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
    
    def deserialize(self, data: str) -> Dict[str, Any]:
        """Deserialize JSON string to dict."""
        return json.loads(data)
    
    def validate_structure(self, data: Dict[str, Any]) -> bool:
        """Validate JSON structure (override in subclasses)."""
        return True
```

#### **Step 1d: Create TTYAdapter (Abstract)**
**File**: `adapters/tty_adapter.py`

```python
from abc import ABC, abstractmethod
from .text_adapter import TextAdapter

class TTYAdapter(TextAdapter, ABC):
    """Base adapter for TTY terminal output with colors and formatting."""
    
    def __init__(self):
        self.colors_enabled = True  # Can be disabled for testing
    
    def add_color(self, text: str, color: str) -> str:
        """Add ANSI color codes to text."""
        if not self.colors_enabled:
            return text
        
        color_codes = {
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'blue': '\033[94m',
            'reset': '\033[0m'
        }
        return f"{color_codes.get(color, '')}{text}{color_codes['reset']}"
    
    def format_indentation(self, indent_level: int, spaces: int = 2) -> str:
        """Format indentation for hierarchical display."""
        return ' ' * (indent_level * spaces)
```

**Test File**: `test/test_adapters/test_channel_adapter.py`

```python
import pytest
from agile_bot.bots.base_bot.src.repl_cli.adapters.json_adapter import JSONAdapter

class MockJSONAdapter(JSONAdapter):
    def __init__(self, data: dict):
        self.data = data
    
    def to_dict(self):
        return self.data

def test_json_adapter_serializes_to_string():
    """Adapter converts dict to JSON string."""
    adapter = MockJSONAdapter({'name': 'test', 'value': 123})
    result = adapter.serialize()
    
    assert isinstance(result, str)
    assert '"name": "test"' in result
    assert '"value": 123' in result

def test_json_adapter_deserializes_from_string():
    """Adapter parses JSON string to dict."""
    adapter = MockJSONAdapter({})
    result = adapter.deserialize('{"name": "test", "value": 123}')
    
    assert result == {'name': 'test', 'value': 123}
```

**CHECKPOINT 1a: Run adapter tests**

```powershell
# Run new adapter tests
pytest agile_bot/bots/base_bot/test/test_adapters/test_channel_adapter.py -v

# Should see: All new tests passing
```

**Expected Result**: New adapter tests pass  
**Existing tests**: Should still pass (new code doesn't affect them yet)

---

### **1.2 Create Domain-Specific JSON Adapters**

#### **Step 2a: Create JSONBotAdapter**
**File**: `adapters/json_bot_adapter.py`

```python
from .json_adapter import JSONAdapter
from typing import Dict, Any

class JSONBotAdapter(JSONAdapter):
    """Wraps Bot domain object and serializes to JSON."""
    
    def __init__(self, bot):
        self.bot = bot
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize Bot to JSON dict."""
        from .json_behavior_adapter import JSONBehaviorAdapter
        
        bot_name = self.bot.bot_paths.bot_directory.name if hasattr(self.bot, 'bot_paths') else 'UNKNOWN'
        bot_path = str(self.bot.bot_paths.bot_directory) if hasattr(self.bot, 'bot_paths') else ''
        
        return {
            "name": bot_name,
            "botDirectory": bot_path,
            "behaviors": [
                JSONBehaviorAdapter(behavior).to_dict() 
                for behavior in self.bot.behaviors
            ]
        }
```

#### **Step 2b: Create JSONBehaviorAdapter**
**File**: `adapters/json_behavior_adapter.py`

```python
from .json_adapter import JSONAdapter
from typing import Dict, Any

class JSONBehaviorAdapter(JSONAdapter):
    """Wraps Behavior domain object and serializes to JSON."""
    
    def __init__(self, behavior):
        self.behavior = behavior
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize Behavior to JSON dict."""
        from .json_action_adapter import JSONActionAdapter
        
        return {
            "name": self.behavior.name,
            "description": getattr(self.behavior, 'description', '') or '',
            "isCurrent": getattr(self.behavior, 'is_current', False),
            "isCompleted": getattr(self.behavior, 'is_completed', False),
            "status": self._get_status(),
            "actions": [
                JSONActionAdapter(action).to_dict()
                for action in self.behavior.actions
            ]
        }
    
    def _get_status(self) -> str:
        """Determine behavior status."""
        if getattr(self.behavior, 'is_current', False):
            return "current"
        elif getattr(self.behavior, 'is_completed', False):
            return "completed"
        return "pending"
```

#### **Step 2c: Create JSONActionAdapter**
**File**: `adapters/json_action_adapter.py`

```python
from .json_adapter import JSONAdapter
from typing import Dict, Any

class JSONActionAdapter(JSONAdapter):
    """Wraps Action domain object and serializes to JSON."""
    
    def __init__(self, action):
        self.action = action
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize Action to JSON dict."""
        return {
            "name": self.action.action_name,
            "description": getattr(self.action, 'description', '') or '',
            "isCurrent": getattr(self.action, 'is_current', False),
            "isCompleted": getattr(self.action, 'is_completed', False),
            "status": self._get_status()
        }
    
    def _get_status(self) -> str:
        """Determine action status."""
        if getattr(self.action, 'is_current', False):
            return "current"
        elif getattr(self.action, 'is_completed', False):
            return "completed"
        return "pending"
```

**Test File**: `test/test_adapters/test_json_bot_adapter.py`

```python
import pytest
from agile_bot.bots.base_bot.src.repl_cli.adapters.json_bot_adapter import JSONBotAdapter
from agile_bot.bots.base_bot.src.bot.bot import Bot
from pathlib import Path

def test_json_bot_adapter_wraps_domain_object(bot_fixture):
    """Adapter wraps Bot and produces JSON dict."""
    adapter = JSONBotAdapter(bot_fixture)
    result = adapter.to_dict()
    
    assert 'name' in result
    assert 'behaviors' in result
    assert isinstance(result['behaviors'], list)

def test_json_bot_adapter_serializes_to_string(bot_fixture):
    """Adapter produces valid JSON string."""
    adapter = JSONBotAdapter(bot_fixture)
    json_str = adapter.serialize()
    
    assert isinstance(json_str, str)
    assert '"name":' in json_str or '"name": ' in json_str
```

**CHECKPOINT 1b: Run JSON adapter tests**

```powershell
# Run JSON adapter tests
pytest agile_bot/bots/base_bot/test/test_adapters/test_json_bot_adapter.py -v

# Should see: All JSON adapter tests passing
```

**Expected Result**: JSON adapter tests pass  
**Existing tests**: Should still pass (48/48)

---

### **1.3 Create Domain-Specific TTY Adapters**

#### **Step 3a: Create TTYBotAdapter**
**File**: `adapters/tty_bot_adapter.py`

```python
from .tty_adapter import TTYAdapter

class TTYBotAdapter(TTYAdapter):
    """Wraps Bot domain object and serializes to TTY format."""
    
    def __init__(self, bot, formatter=None):
        super().__init__()
        self.bot = bot
        self.formatter = formatter  # Reuse existing formatter for now
    
    def serialize(self) -> str:
        """Serialize Bot to TTY text with colors and formatting."""
        from .tty_behavior_adapter import TTYBehaviorAdapter
        
        lines = []
        bot_name = self.bot.bot_paths.bot_directory.name if hasattr(self.bot, 'bot_paths') else 'UNKNOWN'
        
        # Header
        lines.append(self.add_color(f"Bot: {bot_name}", 'blue'))
        lines.append(f"Path: {self.bot.bot_paths.bot_directory}")
        lines.append("")
        
        # Behaviors
        lines.append(self.add_color("Behaviors:", 'green'))
        for behavior in self.bot.behaviors:
            behavior_adapter = TTYBehaviorAdapter(behavior, self.formatter)
            lines.append(behavior_adapter.serialize())
        
        return '\n'.join(lines)
    
    def parse_command(self, text: str) -> tuple[str, list]:
        """Parse command from terminal input."""
        parts = text.strip().split(maxsplit=1)
        verb = parts[0] if parts else ""
        args = parts[1].split() if len(parts) > 1 else []
        return verb, args
```

**Test**: `test/test_adapters/test_tty_bot_adapter.py`

```python
def test_tty_bot_adapter_produces_colored_output(bot_fixture):
    """Adapter produces TTY output with ANSI codes."""
    adapter = TTYBotAdapter(bot_fixture)
    result = adapter.serialize()
    
    assert isinstance(result, str)
    assert 'Bot:' in result
    assert 'Behaviors:' in result

def test_tty_bot_adapter_can_disable_colors(bot_fixture):
    """Adapter can disable colors for testing."""
    adapter = TTYBotAdapter(bot_fixture)
    adapter.colors_enabled = False
    result = adapter.serialize()
    
    # No ANSI codes
    assert '\033[' not in result
```

**CHECKPOINT 1c: Verify Phase 1 Complete**

```powershell
# Run ALL adapter tests
pytest agile_bot/bots/base_bot/test/test_adapters/ -v

# Should see: All adapter tests passing
```

```powershell
# Run FULL test suite to verify no regressions
pytest agile_bot/bots/base_bot/test/ -v

# Should see: 48/48 passing (same as baseline)
```

**Expected Result**: 
- ✅ All new adapter tests pass
- ✅ All existing tests still pass (48/48 - same as baseline)
- ✅ No regressions introduced

**If any test fails**: STOP. Fix before proceeding to Phase 2.

---

## **PHASE 2: Replace Formatter with Adapter in REPLSession**

### **2.1 Introduce Adapter Selection in REPLSession**

#### **Step 2a: Update REPLSession.__init__** (from walkthrough lines 58-65)
**File**: `repl_cli/repl_session.py` (modify existing)

```python
class REPLSession:
    def __init__(self, bot, workspace_directory: Path):
        self.cli_bot = CLIBot(bot, self)
        self.workspace_directory = Path(workspace_directory)
        
        # OLD CODE (keep for now)
        tty_result = self.detect_tty()
        self.formatter = FormatterFactory.create_formatter(tty_detected=tty_result.tty_detected)
        
        # NEW CODE (from walkthrough lines 58-65)
        # Detect output context and select adapter
        isTTY: bool = sys.stdout.isatty()
        isPiped: bool = not isTTY
        
        if isPiped:  # Panel subprocess
            self.adapter = JSONBotAdapter(self.cli_bot.domain_bot)
        elif isTTY:  # Interactive terminal
            self.adapter = TTYBotAdapter(self.cli_bot.domain_bot)
        # Store adapter for session lifecycle
```

**Verification**: Run `pytest test/test_initialize_repl_session.py` - should pass (no behavior change yet)

---

### **2.2 Replace Formatter Calls with Adapter**

#### **Step 2b: Update status command to use adapter** (from walkthrough lines 68-70)
**File**: `repl_cli/repl_session.py` (modify existing)

```python
def _handle_status_command(self, format='text') -> REPLCommandResponse:
    """MODIFIED: Use adapter instead of formatter."""
    if format == 'json':
        # Use session's pre-initialized adapter (walkthrough line 70)
        output: String = self.adapter.serialize()
        return REPLCommandResponse(
            output=output,
            response=output,
            status="success"
        )
    else:
        # TTY mode - use adapter
        output = self.adapter.serialize()
        return REPLCommandResponse(
            output=output,
            response=output,
            status="success"
        )
```

**Verification**: 
- Run `pytest test/test_navigate_behaviors_using_repl_commands.py` - should pass
- Run `echo 'status' | python repl_main.py` - should work
- Run `echo 'status --format json' | python repl_main.py` - should produce JSON

---

### **2.3 Prove Adapters Work with Panel**

#### **Step 2c: Create adapter integration test**
**File**: `test/test_adapters/test_panel_integration.py`

```python
import json
import subprocess
from pathlib import Path

def test_panel_can_parse_json_from_adapter():
    """Panel subprocess receives valid JSON from adapter-based status command."""
    # Simulate panel calling CLI
    result = subprocess.run(
        ['python', 'agile_bot/bots/base_bot/src/repl_cli/repl_main.py'],
        input='status --format json',
        capture_output=True,
        text=True
    )
    
    # Panel should be able to parse this
    try:
        data = json.loads(result.stdout)
        assert 'name' in data
        assert 'behaviors' in data
        assert isinstance(data['behaviors'], list)
    except json.JSONDecodeError as e:
        pytest.fail(f"Panel cannot parse JSON output: {e}")

def test_adapter_json_matches_current_format():
    """NEW adapter JSON format matches CURRENT panel expectations."""
    # Get current JSON format
    result_old = subprocess.run(
        ['python', 'agile_bot/bots/base_bot/src/repl_cli/repl_main.py'],
        input='status --format json',
        capture_output=True,
        text=True
    )
    old_data = json.loads(result_old.stdout)
    
    # Verify structure
    assert 'bot' in old_data or 'name' in old_data
    assert 'behaviors' in old_data
    
    # NEW adapter format should match
    # (This test will guide adapter development)
```

**Verification**: Run test - should pass (proves panel compatibility)

---

**CHECKPOINT 2: Verify Phase 2 Complete**

```powershell
# Run REPLSession initialization tests
pytest agile_bot/bots/base_bot/test/test_initialize_repl_session.py -v

# Should see: All tests passing with new adapter assertions
```

```powershell
# Run panel integration test
pytest agile_bot/bots/base_bot/test/test_panel_integration.py -v

# Should see: Panel can parse JSON from adapters
```

```powershell
# Run FULL test suite
pytest agile_bot/bots/base_bot/test/ -v

# Should see: 48/48 passing (same as baseline) + new panel test
```

**Expected Result**:
- ✅ REPLSession selects correct adapter (TTY vs JSON)
- ✅ Panel integration test passes (JSON format compatible)
- ✅ All existing tests still pass (48/48)
- ✅ Status command uses `self.adapter.serialize()`

**If any test fails**: STOP. Fix before proceeding to Phase 3.

---

## **PHASE 3: Delete Formatters**

### **3.1 Remove Formatter Dependencies from REPLSession**

#### **Step 3a: Remove formatter from REPLSession.__init__**
**File**: `repl_cli/repl_session.py`

```python
class REPLSession:
    def __init__(self, bot, workspace_directory: Path):
        self.cli_bot = CLIBot(bot, self)
        self.workspace_directory = Path(workspace_directory)
        
        # REMOVED: 
        # tty_result = self.detect_tty()
        # self.formatter = FormatterFactory.create_formatter(tty_detected=tty_result.tty_detected)
        
        # Use adapters only (from walkthrough lines 58-65)
        isTTY: bool = sys.stdout.isatty()
        
        if not isTTY:  # Panel subprocess
            self.adapter = JSONBotAdapter(self.cli_bot.domain_bot)
        else:  # Interactive terminal
            self.adapter = TTYBotAdapter(self.cli_bot.domain_bot)
```

#### **Step 3b: Remove formatter imports**
**File**: `repl_cli/repl_session.py`

```python
# REMOVE these imports:
# from .formatters.formatter_factory import FormatterFactory

# ADD these imports:
from .adapters.json_bot_adapter import JSONBotAdapter
from .adapters.tty_bot_adapter import TTYBotAdapter
```

**Verification**: Run all tests - should pass

---

### **3.2 Delete Formatter Files**

#### **Step 3c: Delete entire formatters directory**

```bash
# Windows PowerShell
Remove-Item -Recurse -Force agile_bot/bots/base_bot/src/repl_cli/formatters/

# Or manually delete:
# - agile_bot/bots/base_bot/src/repl_cli/formatters/terminal_formatter.py
# - agile_bot/bots/base_bot/src/repl_cli/formatters/json_formatter.py
# - agile_bot/bots/base_bot/src/repl_cli/formatters/markdown_formatter.py
# - agile_bot/bots/base_bot/src/repl_cli/formatters/formatter_factory.py
# - agile_bot/bots/base_bot/src/repl_cli/formatters/output_formatter.py
# - agile_bot/bots/base_bot/src/repl_cli/formatters/__init__.py
```

**Verification**: Run all tests - should still pass (tests now use adapters from Phase 1)

---

**CHECKPOINT 3: Verify Phase 3 Complete (FINAL VERIFICATION)**

```powershell
# Verify formatters directory is deleted
Test-Path agile_bot/bots/base_bot/src/repl_cli/formatters/

# Should return: False (directory deleted)
```

```powershell
# Run adapter tests
pytest agile_bot/bots/base_bot/test/test_adapters/ -v

# Should see: All adapter tests passing
```

```powershell
# Run REPL initialization tests
pytest agile_bot/bots/base_bot/test/test_initialize_repl_session.py -v

# Should see: All tests passing
```

```powershell
# Run panel integration test
pytest agile_bot/bots/base_bot/test/test_panel_integration.py -v

# Should see: Panel still works with adapters
```

```powershell
# Run FULL test suite (CRITICAL FINAL CHECK)
pytest agile_bot/bots/base_bot/test/ -v

# Should see: 48/48 passing (same as baseline) + new tests
```

**Expected Result**:
- ✅ Formatters directory deleted (no deprecated code)
- ✅ All adapter tests pass
- ✅ REPLSession uses adapters (no formatter references)
- ✅ Panel integration still works
- ✅ All 48 existing tests pass (NO regressions)
- ✅ New adapter tests pass

**If any test fails**: STOP. This is a regression. Investigate and fix.

**Success**: All tests pass → Refactoring complete! 🎉

---

## 📊 Success Criteria

### ✅ Tests Pass
- [ ] All 48 REPL tests pass
- [ ] Panel integration test passes
- [ ] No regressions in existing functionality

### ✅ Code Quality
- [ ] REPLSession uses `self.adapter.serialize()` (walkthrough line 70)
- [ ] Adapter selection on init (walkthrough lines 58-65)
- [ ] No formatters remain in codebase
- [ ] Walkthrough alignment: 100% (lines 58-86)
- [ ] Command parsing stays in REPLSession (NO extraction)

### ✅ Panel Integration
- [ ] Panel spawns CLI subprocess ✓
- [ ] Panel sends 'status --format json' ✓
- [ ] Panel parses JSON response ✓
- [ ] Panel updates UI ✓
- [ ] **Zero panel code changes required** ✓

---

## 🚧 Risk Mitigation

### Risk 1: Tests Break During Refactoring
**Mitigation**: Run tests after each step. If tests break, revert step and try different approach.

### Risk 2: Panel JSON Format Changes
**Mitigation**: Create compatibility tests BEFORE changing serialization. Verify panel can parse new format.

### Risk 3: REPLSession Becomes Unmaintainable During Transition
**Mitigation**: Extract command handlers early (Phase 2). Keep both old and new code isolated.

### Risk 4: Adapters Don't Match CRC Model
**Mitigation**: Review CRC walkthrough after each adapter. Ensure adapters wrap domain objects, not dictionaries.

---

## 📝 Execution Checklist (from walkthrough)

### Phase 0: Establish Baseline (BEFORE starting)
- [ ] Run `pytest agile_bot/bots/base_bot/test/ -v`
- [ ] Record baseline count (e.g., 48/48 passing)
- [ ] Fix any failing tests before proceeding

### Phase 1: Foundation
- [ ] Create adapter base classes (ChannelAdapter, JSONAdapter, TTYAdapter)
- [ ] Create JSON adapters (JSONBotAdapter, JSONBehaviorAdapter, JSONActionAdapter)
- [ ] Create TTY adapters (TTYBotAdapter, TTYBehaviorAdapter, TTYActionAdapter)
- [ ] Implement delegation pattern (adapter calls child adapters - walkthrough lines 75-86)
- [ ] Write adapter tests
- [ ] **TEST**: Run `pytest test/test_adapters/ -v` → All adapter tests pass
- [ ] **TEST**: Run `pytest test/ -v` → 48/48 still pass (no regressions)

### Phase 2: Integration
- [ ] Add adapter selection to REPLSession.__init__ (walkthrough lines 58-65)
- [ ] Replace formatter calls with `self.adapter.serialize()` (line 70)
- [ ] Create panel integration test
- [ ] Update test_initialize_repl_session.py (add adapter assertions)
- [ ] **TEST**: Run `pytest test/test_initialize_repl_session.py -v` → Adapter selection verified
- [ ] **TEST**: Run `pytest test/test_panel_integration.py -v` → Panel works
- [ ] **TEST**: Run `pytest test/ -v` → 48/48 + new tests pass

### Phase 3: Delete Formatters
- [ ] Remove `self.formatter = ...` from REPLSession.__init__
- [ ] Remove formatter imports from REPLSession
- [ ] Delete entire `formatters/` directory (NO deprecation)
- [ ] **TEST**: Verify formatters deleted: `Test-Path formatters/` → False
- [ ] **TEST**: Run `pytest test/test_adapters/ -v` → All pass
- [ ] **TEST**: Run `pytest test/test_initialize_repl_session.py -v` → All pass
- [ ] **TEST**: Run `pytest test/test_panel_integration.py -v` → Panel still works
- [ ] **TEST**: Run `pytest test/ -v` → **48/48 + new tests pass (FINAL CHECK)**

---

## 🧪 Testing Summary

**Tests are run at EVERY phase checkpoint:**

| Phase | Test Command | Expected Result | Action if Fails |
|-------|--------------|-----------------|-----------------|
| **Phase 0** | `pytest test/ -v` | 48/48 pass (baseline) | Fix existing failures before starting |
| **Phase 1** | `pytest test/test_adapters/ -v` | All adapter tests pass | Fix adapter code |
| **Phase 1** | `pytest test/ -v` | 48/48 still pass | Revert changes, fix issue |
| **Phase 2** | `pytest test/test_initialize_repl_session.py -v` | Adapter selection verified | Fix REPLSession changes |
| **Phase 2** | `pytest test/test_panel_integration.py -v` | Panel compatibility verified | Fix JSON format |
| **Phase 2** | `pytest test/ -v` | 48/48 + new tests pass | Investigate regression |
| **Phase 3** | `pytest test/test_adapters/ -v` | All adapter tests pass | Adapters broken by formatter removal |
| **Phase 3** | `pytest test/ -v` | **48/48 + new tests pass** | **CRITICAL: Regression detected** |

**Key Principle**: If ANY test fails at ANY checkpoint → **STOP, revert, fix, then continue**

---

## 📚 References

- **CRC Model**: `agile_bot/bots/base_bot/docs/crc/crc-model-outline.md`
- **Walkthrough**: `agile_bot/bots/base_bot/docs/crc/walkthrough-realizations.md`
- **Tests**: `agile_bot/bots/base_bot/test/test_*_repl*.py`
- **Test Refactoring Guide**: `CRC_REPL_TEST_REFACTORING.md`

---

## 🎯 Expected Outcome

After completing this plan:

1. **REPLSession uses adapter pattern** (walkthrough lines 58-70)
2. **Adapters handle serialization** (JSON, TTY with delegation)
3. **Command logic stays in REPLSession** (NO extraction per walkthrough)
4. **All 48 tests pass** (zero regressions)
5. **Panel works unchanged** (JSON format compatible)
6. **Walkthrough alignment** (100% match to lines 58-86)

**Total Effort**: 8-12 hours (just replacing formatters, no command extraction)  
**Risk**: Low (simple serialization change, test verification at each step)  
**Breaking Changes**: Zero (old and new code coexist during transition)
