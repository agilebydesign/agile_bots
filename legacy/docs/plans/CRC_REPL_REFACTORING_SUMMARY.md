# CRC REPL Refactoring - Executive Summary

**Date**: 2026-01-07  
**Status**: Ready to Execute

**⚠️ CORRECTED**: This plan now follows `walkthrough-realizations.md` lines 58-86 EXACTLY.  
**What I got wrong initially**: Invented CommandRegistry, NavigationCommands, etc. (NOT in walkthrough)  
**What the walkthrough actually shows**: Just replace formatters with adapters. That's it.

**🧪 TEST-DRIVEN REFACTORING**: Run tests at EVERY checkpoint. If ANY test fails → STOP, revert, fix.

---

## 🎯 Goal

Refactor REPL CLI to match CRC domain model while **ensuring zero breaking changes** to tests and panel integration.

---

## 📊 Current vs. Target

### Current State
```
REPLSession (1750 lines)
├── Everything in one class
├── Formatters (terminal_formatter, json_formatter)
└── Inline command handling

Panel Integration
└── Spawns subprocess → sends 'status --format json' → parses JSON
```

### Target State (CRC Model - from walkthrough)
```
REPLSession (same size - just changes HOW it serializes)
├── Select adapter on init (TTY vs JSON based on isatty())
├── Store adapter for session lifecycle
├── handle_command() calls this.adapter.serialize()
└── Command parsing stays in REPLSession (NO extraction)

Adapters (wrap domain objects)
├── JSONBotAdapter(bot).serialize()
│   └── delegates to JSONBehaviorAdapter
│       └── delegates to JSONActionAdapter
├── TTYBotAdapter(bot).serialize()
│   └── delegates to TTYBehaviorAdapter
│       └── delegates to TTYActionAdapter
└── All command logic stays in REPLSession

Panel Integration
└── UNCHANGED - same JSON format
```

---

## 🚀 3-Phase Strategy (from walkthrough-realizations.md)

### Phase 1: Create Adapter Foundation ⚙️
**Outcome**: New adapters alongside existing formatters  
**Tests**: All pass ✅  
**Panel**: No changes ✅

**What we build** (from walkthrough lines 62-86):
- `adapters/channel_adapter.py` (abstract base)
- `adapters/json_adapter.py` (JSON serialization)
- `adapters/tty_adapter.py` (terminal output)
- `adapters/json_bot_adapter.py` (wraps Bot → JSON)
- `adapters/json_behavior_adapter.py` (wraps Behavior → JSON)
- `adapters/json_action_adapter.py` (wraps Action → JSON)
- `adapters/tty_bot_adapter.py` (wraps Bot → TTY)
- `adapters/tty_behavior_adapter.py` (wraps Behavior → TTY)
- `adapters/tty_action_adapter.py` (wraps Action → TTY)

**Key Pattern from walkthrough (lines 70-86)**: Adapter delegates to child adapters

```python
# JSONBotAdapter.serialize() [from walkthrough line 71-86]
jsonDict: Dict = {}
jsonDict['name'] = this.bot.name
jsonDict['behaviors'] = []
for behavior in this.bot.behaviors:
   behaviorAdapter: JSONBehaviorAdapter = JSONBehaviorAdapter(behavior)
   behaviorDict: Dict = behaviorAdapter.serialize()
      -> for action in this.behavior.actions:
         actionAdapter: JSONActionAdapter = JSONActionAdapter(action)
         actionDict: Dict = actionAdapter.serialize()
```

---

### Phase 2: Replace Formatter with Adapter in REPLSession 🔀
**Outcome**: REPLSession uses adapter instead of formatter  
**Tests**: All pass ✅  
**Panel**: **Verify JSON format** ⚠️

**What we do** (from walkthrough lines 58-70):

**REPLSession.__init__** (lines 58-65):
```python
# Detect output context and select adapter
isTTY: bool = sys.stdout.isatty()
isPiped: bool = not isTTY
if isPiped:  # Panel subprocess
   this.adapter = JSONBotAdapter(bot)
elif isTTY:  # Interactive terminal
   this.adapter = TTYBotAdapter(bot)
# Store adapter for session lifecycle
```

**REPLSession.handle_command** (lines 68-70):
```python
# Use session's pre-initialized adapter
output: String = this.adapter.serialize()
print(output)  # stdout
```

**CRITICAL**: Command parsing stays in REPLSession (walkthrough shows NO extracted command classes)

---

### Phase 3: Delete Formatters 🗑️
**Outcome**: Formatters deleted, adapters only  
**Tests**: All pass ✅  
**Panel**: No changes ✅

**What we do:**
1. Remove `self.formatter = FormatterFactory.create_formatter()` from REPLSession
2. Remove formatter imports from REPLSession
3. Delete entire `formatters/` directory (no deprecation, just delete)

**What we delete:**
- `formatters/terminal_formatter.py`
- `formatters/json_formatter.py`
- `formatters/markdown_formatter.py`
- `formatters/formatter_factory.py`
- `formatters/output_formatter.py`
- `formatters/__init__.py`

**What stays:**
- ALL command parsing logic in REPLSession
- REPLSession size: ~1750 lines (same as before)
- Command routing: stays in `_handle_simple_command()`

**Key Insight**: We're ONLY changing serialization, NOT extracting command logic. NO deprecated code - just delete it.

---

## 🎯 Panel Integration Strategy

### Panel Expects This JSON Format

```json
{
  "bot": {
    "name": "story_bot",
    "botDirectory": "C:/path/to/bot"
  },
  "behaviors": [
    {
      "name": "shape",
      "isCurrent": true,
      "isCompleted": false,
      "actions": [
        {
          "name": "clarify",
          "isCurrent": true,
          "isCompleted": false
        }
      ]
    }
  ]
}
```

### Minimal Panel Changes

**Option 1: Zero Panel Changes** (Preferred)
- Ensure `JSONBotAdapter.to_dict()` matches current format exactly
- Panel code remains unchanged
- Tests verify format compatibility

**Option 2: Minimal Panel Update** (If format must change)
```typescript
// Before: panel expects 'bot' top-level key
const botData = JSON.parse(stdout).bot;

// After: adapter returns bot data at top level
const botData = JSON.parse(stdout);
```

**Decision Point**: After Phase 3, compare adapter JSON with current format. If identical → Option 1. If different → Option 2 with minimal update.

---

## 🧪 Testing Strategy

**Run tests at EVERY checkpoint:**

1. **Phase 0 (Baseline)**: `pytest test/ -v` → Record baseline (48/48)
2. **Phase 1 (Adapters)**: `pytest test/test_adapters/ -v` → New tests pass
3. **Phase 1 (Regression)**: `pytest test/ -v` → 48/48 still pass
4. **Phase 2 (Integration)**: `pytest test/test_initialize_repl_session.py -v` → Adapters verified
5. **Phase 2 (Panel)**: `pytest test/test_panel_integration.py -v` → Panel works
6. **Phase 2 (Regression)**: `pytest test/ -v` → 48/48 + new tests pass
7. **Phase 3 (Final)**: `pytest test/ -v` → **48/48 + new tests pass (NO regressions)**

**If ANY test fails → STOP, revert, fix, continue**

---

## ✅ Success Criteria Checklist

### Tests
- [ ] All 48 REPL tests pass (baseline maintained)
- [ ] All panel integration tests pass
- [ ] Zero test regressions (48/48 → 48/48)
- [ ] New adapter tests pass

### Code Quality
- [ ] REPLSession uses adapter pattern (self.adapter.serialize())
- [ ] Adapters match walkthrough (wrap domain objects, delegate to child adapters)
- [ ] All formatters removed from codebase
- [ ] Command parsing stays in REPLSession (NO extraction per walkthrough)

### Panel Integration
- [ ] Panel spawns CLI subprocess ✓
- [ ] Panel parses JSON response ✓
- [ ] Panel renders UI correctly ✓
- [ ] Panel changes: **0-5 lines max**

### CRC Alignment
- [ ] Adapters wrap domain objects ✓
- [ ] JSONBotAdapter → JSONBehaviorAdapter → JSONActionAdapter delegation ✓
- [ ] Matches walkthrough-realizations.md pattern ✓
- [ ] No formatters remain ✓

---

## 🚧 Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Tests break during refactoring | Medium | High | Run tests after each step, revert if fail |
| Panel JSON format incompatible | Low | High | Create compatibility test BEFORE migration |
| Adapters don't match walkthrough | Low | Medium | Review walkthrough lines 58-86 after each adapter |
| Serialization produces different JSON | Low | High | Compare adapter output to current formatter output |

**Overall Risk**: **LOW** - Incremental approach with test verification at each step

---

## 📅 Execution Timeline (from walkthrough)

### Day 0: Establish Baseline (BEFORE starting)
- Run full test suite: `pytest agile_bot/bots/base_bot/test/ -v`
- Record baseline: Should be 48/48 passing
- **Checkpoint**: Baseline established ✅

### Day 1: Foundation (Phase 1)
- Create adapter base classes (ChannelAdapter, JSONAdapter, TTYAdapter)
- Create domain adapters (JSONBotAdapter, JSONBehaviorAdapter, JSONActionAdapter)
- Create TTY adapters (TTYBotAdapter, TTYBehaviorAdapter, TTYActionAdapter)
- Write adapter tests
- **Test Checkpoint**: 
  - Run `pytest test/test_adapters/ -v` → All adapter tests pass
  - Run `pytest test/ -v` → 48/48 still pass (no regressions)
- **Checkpoint**: Phase 1 complete ✅

### Day 2: Integration (Phase 2)
- Update REPLSession.__init__ to select adapter (lines 58-65 of walkthrough)
- Replace formatter calls with `self.adapter.serialize()` (line 70 of walkthrough)
- Create panel compatibility test
- Verify JSON format matches panel expectations
- **Test Checkpoint**:
  - Run `pytest test/test_initialize_repl_session.py -v` → Adapter selection verified
  - Run `pytest test/test_panel_integration.py -v` → Panel compatibility verified
  - Run `pytest test/ -v` → 48/48 + new tests pass
- **Checkpoint**: Phase 2 complete ✅

### Day 3: Delete Formatters (Phase 3)
- Remove `self.formatter` from REPLSession
- Remove formatter imports
- Delete entire `formatters/` directory (NO deprecation)
- **Final Test Checkpoint**:
  - Verify formatters deleted: `Test-Path formatters/` → False
  - Run `pytest test/test_adapters/ -v` → All adapter tests pass
  - Run `pytest test/test_initialize_repl_session.py -v` → All pass
  - Run `pytest test/test_panel_integration.py -v` → Panel still works
  - Run `pytest test/ -v` → **48/48 + new tests pass (NO regressions)**
- **Checkpoint**: Refactoring complete ✅

**Total Effort**: 3 days (8 hours/day) = 24 hours  
**Complexity**: Low (just replacing formatters with adapters)  
**Risk**: Low (no command extraction, just serialization change)

---

## 🎬 Next Steps

1. **Review this plan** with team
2. **Run current tests** to establish baseline
3. **Start Phase 1** - create adapter foundation
4. **After each phase** - run tests and verify
5. **Final checkpoint** - all tests pass, panel works

---

## 📞 Questions to Answer

### For User
1. ✅ Is this incremental approach acceptable?
2. ✅ Can we coexist with old formatters during transition?
3. ⚠️ What is current panel JSON format? (Need to verify compatibility)
4. ⚠️ Are you comfortable with 0-5 line panel update if needed?

### For Implementation
1. Should we create adapters in test-first or implementation-first order?
2. Should we extract all commands at once or one at a time?
3. Should we keep formatters as fallback after migration?

---

## 📖 References

- **Full Plan**: `CRC_REPL_REFACTORING_PLAN.md` (detailed steps)
- **CRC Model**: `crc/crc-model-outline.md` (target architecture)
- **Walkthrough**: `crc/walkthrough-realizations.md` (object flows)
- **Tests**: `test/test_*_repl*.py` (48 tests to preserve)

---

## 💡 Key Insights

### 1. Adapters Wrap Domain Objects
```python
# CORRECT (matches CRC walkthrough)
adapter = JSONBotAdapter(bot)  # Wraps domain object
json_str = adapter.serialize()  # Delegates to behavior adapters

# INCORRECT (current implementation)
json_dict = self._get_bot_info_json()  # Manually builds dict
json_str = json.dumps(json_dict)
```

### 2. Delegation Pattern
```python
# CRC Pattern: Adapter delegates to child adapters
class JSONBotAdapter:
    def to_dict(self):
        return {
            'name': self.bot.name,
            'behaviors': [
                JSONBehaviorAdapter(b).to_dict()  # Delegate to behavior adapter
                for b in self.bot.behaviors
            ]
        }
```

### 3. Orchestrator Pattern
```python
# REPLSession is thin orchestrator
class REPLSession:
    def read_and_execute_command(self, command: str):
        # Parse command
        verb, args = self.parser.parse(command)
        
        # Execute via registry
        result = self.commands.execute(verb, args)
        
        # Serialize via adapter
        output = self.adapter.serialize(result)
        
        return output
```

---

## 🎯 Expected Outcome

After completing this refactoring:

- ✅ **REPLSession**: Uses adapter pattern (walkthrough lines 58-70)
- ✅ **All tests pass**: 48/48 passing
- ✅ **Panel integration**: Works unchanged (or 0-5 line update)
- ✅ **Walkthrough alignment**: 100% match to lines 58-86
- ✅ **Formatters deleted**: Entire `formatters/` directory removed (no deprecation)
- ✅ **Command logic preserved**: Stays in REPLSession (no extraction)

**Ready to proceed?** Start with Phase 1 - Create Adapter Foundation.
