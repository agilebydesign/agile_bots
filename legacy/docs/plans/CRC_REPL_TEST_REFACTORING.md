# CRC REPL Test Refactoring Guide

**Date**: 2026-01-07  
**Purpose**: Show how to refactor EXISTING tests to work with adapter pattern (from walkthrough lines 58-86)

---

## 🎯 Test Files That Need Updates

### Category 1: Formatter Tests → Adapter Tests
- **`test/test_formatters.py`** → Rename to `test/test_adapters.py`, update to test adapters

### Category 2: REPLSession Tests (Verify adapter selection)
- **`test/test_initialize_repl_session.py`** → Update to verify `self.adapter` selection
- **`test/test_navigate_behaviors_using_repl_commands.py`** → Review (probably no changes)

### Category 3: Instructions Display Tests (Verify adapter output)
- **`test/test_display_clarify_instructions_using_repl.py`** → Review (probably no changes)
- **`test/test_display_build_instructions_using_repl.py`** → Review (probably no changes)
- **`test/test_display_render_instructions_using_repl.py`** → Review (probably no changes)
- **`test/test_display_strategy_instructions_using_repl.py`** → Review (probably no changes)
- **`test/test_display_validate_instructions_using_repl.py`** → Review (probably no changes)

---

## 📋 Refactoring Strategy

### Phase 1: Rename test_formatters.py → test_adapters.py
1. Keep test structure (TestTerminalFormatter → TestTTYBotAdapter)
2. Update imports (formatter classes → adapter classes)
3. Update assertions (same behavior, different class names)

### Phase 2: Update REPLSession initialization tests
1. Verify `self.adapter` exists (not `self.formatter`)
2. Verify correct adapter type selected (TTY vs JSON)
3. Keep all existing test scenarios

### Phase 3: Review instruction display tests
1. Tests should still call `repl_session.read_and_execute_command()`
2. Adapters are internal implementation (tests don't change!)
3. Only update if test directly inspects formatter

---

## 🔧 Detailed Refactoring Examples

### Example 1: test_formatters.py → test_adapters.py

#### BEFORE (test_formatters.py lines 1-76)
```python
import pytest
from agile_bot.bots.base_bot.src.repl_cli.formatters.terminal_formatter import TerminalFormatter
from agile_bot.bots.base_bot.src.repl_cli.formatters.markdown_formatter import MarkdownFormatter

def given_terminal_formatter():
    return TerminalFormatter()

def then_separator_equals(formatter, expected_separator):
    result = formatter.section_separator()
    assert result == expected_separator

class TestTerminalFormatter:
    
    def test_returns_dashes_for_section_separator(self):
        formatter = given_terminal_formatter()
        then_separator_equals(formatter, "=" * 60)
    
    def test_returns_completed_status_marker(self):
        formatter = given_terminal_formatter()
        result = formatter.status_marker(is_current=False, is_completed=True)
        assert result == "[OK]"
```

#### AFTER (test_adapters.py)
```python
import pytest
from agile_bot.bots.base_bot.src.repl_cli.adapters.tty_bot_adapter import TTYBotAdapter
from agile_bot.bots.base_bot.src.repl_cli.adapters.json_bot_adapter import JSONBotAdapter
from agile_bot.bots.base_bot.test.test_invoke_bot_helpers import setup_test_bot

def given_tty_bot_adapter(bot):
    """Create TTY adapter wrapping bot"""
    return TTYBotAdapter(bot)

def given_json_bot_adapter(bot):
    """Create JSON adapter wrapping bot"""
    return JSONBotAdapter(bot)

class TestTTYBotAdapter:
    """
    Story: Serialize Bot to TTY Format
    Tests: TTY adapter wraps Bot and produces terminal output
    """
    
    def test_adapter_wraps_bot_and_serializes(self, tmp_path):
        """
        SCENARIO: Adapter serializes bot to TTY string
        GIVEN: Bot with behaviors
        WHEN: TTYBotAdapter(bot).serialize()
        THEN: Returns string with bot information
        """
        # GIVEN
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        
        # WHEN
        adapter = given_tty_bot_adapter(bot)
        result = adapter.serialize()
        
        # THEN
        assert isinstance(result, str)
        assert 'Bot:' in result or 'story_bot' in result
    
    def test_adapter_includes_behavior_information(self, tmp_path):
        """
        SCENARIO: Adapter includes behavior hierarchy
        GIVEN: Bot with behaviors
        WHEN: TTYBotAdapter serializes
        THEN: Output includes behavior names
        """
        # GIVEN
        bot, workspace = setup_test_bot(tmp_path, ['shape', 'discovery'])
        
        # WHEN
        adapter = given_tty_bot_adapter(bot)
        result = adapter.serialize()
        
        # THEN
        assert 'shape' in result.lower() or 'discovery' in result.lower()

class TestJSONBotAdapter:
    """
    Story: Serialize Bot to JSON Format
    Tests: JSON adapter wraps Bot and produces JSON string
    """
    
    def test_adapter_produces_valid_json(self, tmp_path):
        """
        SCENARIO: Adapter serializes bot to JSON
        GIVEN: Bot with behaviors
        WHEN: JSONBotAdapter(bot).serialize()
        THEN: Returns valid JSON string
        """
        # GIVEN
        bot, workspace = setup_test_bot(tmp_path, ['shape'])
        
        # WHEN
        adapter = given_json_bot_adapter(bot)
        json_string = adapter.serialize()
        
        # THEN
        import json
        data = json.loads(json_string)  # Must parse without error
        assert 'name' in data or 'behaviors' in data
    
    def test_adapter_delegates_to_behavior_adapter(self, tmp_path):
        """
        SCENARIO: Adapter delegates to JSONBehaviorAdapter (walkthrough lines 75-86)
        GIVEN: Bot with behaviors
        WHEN: JSONBotAdapter serializes
        THEN: Output includes behavior data from JSONBehaviorAdapter
        """
        # GIVEN
        bot, workspace = setup_test_bot(tmp_path, ['shape', 'discovery'])
        
        # WHEN
        adapter = given_json_bot_adapter(bot)
        json_string = adapter.serialize()
        
        # THEN
        import json
        data = json.loads(json_string)
        assert 'behaviors' in data
        assert isinstance(data['behaviors'], list)
        if data['behaviors']:
            behavior = data['behaviors'][0]
            assert 'name' in behavior
            assert 'actions' in behavior  # From JSONBehaviorAdapter
```

**Key Changes:**
1. ✅ Import adapters instead of formatters
2. ✅ Use `setup_test_bot()` to create real Bot (adapters wrap domain objects)
3. ✅ Test `serialize()` method (not individual formatting methods)
4. ✅ Verify delegation pattern (JSON adapter calls JSONBehaviorAdapter)
5. ✅ Follow story graph structure (class = story, method = scenario)

---

### Example 2: test_initialize_repl_session.py

#### BEFORE (lines 49-73)
```python
def test_cli_launches_in_interactive_mode(self, tmp_path, monkeypatch):
    # GIVEN: Interactive mode (TTY detected)
    monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
    bot, workspace = setup_test_bot(tmp_path, ['shape'])
    
    # WHEN: REPLSession initializes in interactive mode
    repl_session = REPLSession(bot=bot, workspace_directory=workspace)
    cli_output = repl_session.display_current_state()
    
    # THEN: REPLSession wraps Bot
    assert repl_session.bot is not None
    assert repl_session.bot.bot_name == 'story_bot'
    
    # AND: CLI displays state
    display_output = cli_output.output
    assert 'No behaviors available' in display_output or 'shape' in display_output.lower()
```

#### AFTER (add adapter verification)
```python
def test_cli_launches_in_interactive_mode(self, tmp_path, monkeypatch):
    """
    SCENARIO: CLI launches in interactive mode
    GIVEN: TTY detected (interactive terminal)
    WHEN: REPLSession initializes
    THEN: REPLSession selects TTYBotAdapter (walkthrough lines 63-64)
    """
    # GIVEN: Interactive mode (TTY detected)
    monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
    bot, workspace = setup_test_bot(tmp_path, ['shape'])
    
    # WHEN: REPLSession initializes in interactive mode
    repl_session = REPLSession(bot=bot, workspace_directory=workspace)
    
    # THEN: REPLSession wraps Bot
    assert repl_session.bot is not None
    assert repl_session.bot.bot_name == 'story_bot'
    
    # AND: Adapter selected for TTY mode (NEW - from walkthrough)
    from agile_bot.bots.base_bot.src.repl_cli.adapters.tty_bot_adapter import TTYBotAdapter
    assert hasattr(repl_session, 'adapter')
    assert isinstance(repl_session.adapter, TTYBotAdapter)
    
    # AND: CLI displays state (unchanged)
    cli_output = repl_session.display_current_state()
    display_output = cli_output.output
    assert 'No behaviors available' in display_output or 'shape' in display_output.lower()
```

**Key Changes:**
1. ✅ Add assertion: `assert hasattr(repl_session, 'adapter')`
2. ✅ Verify adapter type: `assert isinstance(repl_session.adapter, TTYBotAdapter)`
3. ✅ Keep existing assertions (bot wrapping, output display)
4. ✅ Reference walkthrough in docstring

---

#### BEFORE (lines 106-127 - pipe mode test)
```python
def test_cli_launches_in_pipe_mode(self, tmp_path, monkeypatch):
    # GIVEN: Pipe mode (non-TTY detected)
    monkeypatch.setattr(sys.stdin, 'isatty', lambda: False)
    bot, workspace = setup_test_bot(tmp_path, ['shape'])
    
    # WHEN: REPLSession initializes in pipe mode
    repl_session = REPLSession(bot=bot, workspace_directory=workspace)
    
    # THEN: REPLSession wraps Bot
    assert repl_session.bot is not None
    
    # AND: TTY detection shows non-interactive
    tty_result = repl_session.detect_tty()
    assert tty_result.tty_detected == False
```

#### AFTER (add adapter verification)
```python
def test_cli_launches_in_pipe_mode(self, tmp_path, monkeypatch):
    """
    SCENARIO: CLI launches in pipe mode
    GIVEN: Non-TTY detected (piped input from panel)
    WHEN: REPLSession initializes
    THEN: REPLSession selects JSONBotAdapter (walkthrough lines 61-62)
    """
    # GIVEN: Pipe mode (non-TTY detected)
    monkeypatch.setattr(sys.stdin, 'isatty', lambda: False)
    bot, workspace = setup_test_bot(tmp_path, ['shape'])
    
    # WHEN: REPLSession initializes in pipe mode
    repl_session = REPLSession(bot=bot, workspace_directory=workspace)
    
    # THEN: REPLSession wraps Bot
    assert repl_session.bot is not None
    
    # AND: Adapter selected for JSON mode (NEW - from walkthrough)
    from agile_bot.bots.base_bot.src.repl_cli.adapters.json_bot_adapter import JSONBotAdapter
    assert hasattr(repl_session, 'adapter')
    assert isinstance(repl_session.adapter, JSONBotAdapter)
    
    # AND: TTY detection shows non-interactive (unchanged)
    tty_result = repl_session.detect_tty()
    assert tty_result.tty_detected == False
```

**Key Changes:**
1. ✅ Verify `JSONBotAdapter` selected when non-TTY (walkthrough line 62)
2. ✅ Keep existing TTY detection test
3. ✅ Reference walkthrough in docstring

---

### Example 3: test_navigate_behaviors_using_repl_commands.py

#### Tests in this file probably DON'T need changes!

**Reason**: These tests call `repl_session.read_and_execute_command('status')` which is a **public API**.  
The adapter is an **internal implementation detail**.  
Tests should continue to verify output, not inspect internal adapter.

#### IF a test directly checks `self.formatter`:
```python
# BEFORE (if exists)
def test_status_uses_formatter(self):
    # ...
    assert repl_session.formatter is not None  # ❌ WRONG

# AFTER
def test_status_produces_output(self):
    # ...
    result = repl_session.read_and_execute_command('status')
    assert result.output is not None  # ✅ RIGHT - test behavior, not implementation
```

**Key Principle**: Tests should verify **observable behavior** (output), not **implementation details** (formatter/adapter).

---

### Example 4: test_display_*_instructions_using_repl.py Files

#### These tests probably DON'T need changes!

**Reason**: They test instructions output through public API:
```python
response = repl_session.read_and_execute_command('clarify.instructions')
assert 'key questions' in response.output.lower()
```

#### ONLY update if test directly references formatter:
```python
# BEFORE (if exists)
def test_uses_json_formatter_in_pipe_mode():
    assert isinstance(repl_session.formatter, JSONFormatter)  # ❌ WRONG

# AFTER
def test_produces_json_in_pipe_mode():
    result = repl_session.read_and_execute_command('status --format json')
    import json
    data = json.loads(result.output)  # ✅ RIGHT - verify output format
    assert 'behaviors' in data
```

---

## ✅ Test Refactoring Checklist

### Phase 1: Rename and Update Formatter Tests
- [ ] Rename `test/test_formatters.py` → `test/test_adapters.py`
- [ ] Update imports (formatters → adapters)
- [ ] Update class names (TestTerminalFormatter → TestTTYBotAdapter)
- [ ] Update test methods to use `setup_test_bot()` and create real Bot
- [ ] Verify adapters wrap domain objects (not raw data)
- [ ] Test `serialize()` method (not individual formatting methods)
- [ ] Run: `pytest test/test_adapters.py` - all pass

### Phase 2: Update REPLSession Initialization Tests
- [ ] Open `test/test_initialize_repl_session.py`
- [ ] Add adapter verification to `test_cli_launches_in_interactive_mode`:
  - `assert isinstance(repl_session.adapter, TTYBotAdapter)`
- [ ] Add adapter verification to `test_cli_launches_in_pipe_mode`:
  - `assert isinstance(repl_session.adapter, JSONBotAdapter)`
- [ ] Keep all existing assertions (they still apply)
- [ ] Run: `pytest test/test_initialize_repl_session.py` - all pass

### Phase 3: Review Other Test Files (Check for Formatter References)
- [ ] Scan `test/test_navigate_behaviors_using_repl_commands.py`
  - If tests check `self.formatter` → remove those assertions
  - If tests verify output → keep as-is (they test behavior)
- [ ] Scan `test/test_display_*_instructions_using_repl.py` files
  - If tests call public API → keep as-is
  - If tests inspect formatter → update to verify output format
- [ ] Search for any other formatter references: `grep -r "formatter" test/`
  - Remove assertions about formatters
  - Keep tests that verify output
- [ ] Run: `pytest test/` - all 48 tests pass

### Phase 4: Add Panel Integration Test
- [ ] Create `test/test_panel_integration.py`
- [ ] Test: Panel spawns CLI, sends 'status --format json', parses response
- [ ] Verify JSON structure matches panel expectations
- [ ] Run: `pytest test/test_panel_integration.py` - passes

---

## 🎯 Success Criteria

After refactoring tests:

1. **All 48 tests pass** (no regressions)
2. **test_adapters.py** tests adapter delegation pattern (walkthrough lines 75-86)
3. **test_initialize_repl_session.py** verifies adapter selection (walkthrough lines 58-65)
4. **Other tests unchanged** (they test public API, not implementation)
5. **Panel integration test added** (proves JSON compatibility)

---

## 📚 Key Testing Principles (from user's rules)

1. **use_domain_language**: Test names = plain English stories
   - ✅ `test_adapter_wraps_bot_and_serializes`
   - ❌ `test_adapt_serialize_impl`

2. **call_production_code_directly**: No mocking adapters/formatters
   - ✅ `adapter = TTYBotAdapter(bot); result = adapter.serialize()`
   - ❌ `adapter = Mock(spec=TTYBotAdapter)`

3. **test_observable_behavior**: Test output, not internals
   - ✅ `assert 'behaviors' in json.loads(result)`
   - ❌ `assert repl_session.adapter.internal_state == 'ready'`

4. **match_specification_scenarios**: Tests verify walkthrough flows
   - ✅ Docstring references "walkthrough lines 58-65"
   - ✅ Test verifies adapter selection as shown in walkthrough

5. **use_class_based_organization**: Structure matches story graph
   - File = sub-epic: `test_adapters.py`
   - Class = story: `TestTTYBotAdapter`, `TestJSONBotAdapter`
   - Method = scenario: `test_adapter_wraps_bot_and_serializes`

---

## 🚀 Next Steps

1. **Review this guide** - ensure test changes match walkthrough
2. **Start with test_formatters.py** - rename and refactor to test_adapters.py
3. **Update test_initialize_repl_session.py** - add adapter verification
4. **Run full test suite** - verify all 48 tests pass
5. **Create panel integration test** - prove JSON compatibility

**Ready to refactor tests?** Start with Phase 1: test_formatters.py → test_adapters.py
