# Adapter-Visitor Synchronization Plan

## Overview

This plan outlines the refactoring to synchronize the adapter pattern (used for display serialization) with the visitor pattern (used for code generation), creating a unified hierarchical traversal and wrapping approach.

## Current State Analysis

### Adapter Pattern (Display Serialization)

**Current Implementation:**
- Adapters wrap domain objects (Bot, Behaviors, Behavior, Actions)
- Child adapters are created lazily via `AdapterFactory.create()` during property access or `serialize()` calls
- Each adapter handles its own traversal logic
- Hierarchy is built on-demand during serialization

**Example Flow:**
```
TTYBot.__init__(bot)
  → TTYBot.serialize()
    → Accesses self.behaviors property
      → Creates TTYBehaviors via AdapterFactory.create(bot.behaviors, 'tty')
        → TTYBehaviors.serialize()
          → Iterates behaviors, creates TTYBehavior for each
            → TTYBehavior.serialize()
              → Creates TTYActions via AdapterFactory.create(behavior.actions, 'tty')
                → TTYActions.serialize()
                  → Creates TTYAction for each action
```

**Issues:**
- Adapter creation happens repeatedly during serialization
- Traversal logic is duplicated across adapters
- No centralized hierarchy building
- Child adapters are recreated on each property access

### Visitor Pattern (Code Generation)

**Current Implementation:**
- `Orchestrator` traverses Bot → Behaviors → Behavior → Actions
- Calls visitor methods (`visit_header`, `visit_behavior`, `visit_action`, `visit_footer`)
- `CursorCommandVisitor` implements these methods to generate command files
- Traversal logic is centralized in `Orchestrator`

**Example Flow:**
```
Orchestrator.generate()
  → visit_header()
  → _visit_behaviors()
    → For each behavior: _visit_behavior()
      → Creates BehaviorHelpContext
      → visitor.visit_behavior(context)
  → _visit_action_help_section()
    → For each action: _visit_action()
      → Creates ActionHelpContext
      → visitor.visit_action(context)
  → visit_footer()
```

**Issues:**
- Different traversal approach than adapters
- Context objects (BehaviorHelpContext, ActionHelpContext) are separate from domain objects
- No unified pattern with adapters

## Proposed Solution: BaseHierarchicalAdapter Pattern

### Core Concept

Create a base class that:
1. **Builds wrapped hierarchy at construction time** (not lazily)
2. **Centralizes traversal logic** (similar to Orchestrator)
3. **Unifies adapter wrapping and visitor traversal**
4. **Eliminates repeated adapter creation**

### Architecture

```
BaseHierarchicalAdapter (ABC)
├── __init__(domain_object, channel, factory)
│   └── Calls _build_wrapped_hierarchy() at construction
├── _build_wrapped_hierarchy() (abstract)
│   └── Traverses domain object and wraps children using factory
└── serialize() (abstract)
    └── Assembles output from pre-built hierarchy

BaseBotAdapter(BaseHierarchicalAdapter)
├── _build_wrapped_hierarchy()
│   └── Wraps bot.behaviors → BaseBehaviorsAdapter
└── serialize()
    └── Assembles header + bot info + behaviors.serialize() + footer

BaseBehaviorsAdapter(BaseHierarchicalAdapter)
├── _build_wrapped_hierarchy()
│   └── Wraps each behavior → BaseBehaviorAdapter
└── serialize()
    └── Iterates behavior_adapters, calls serialize() on each

BaseBehaviorAdapter(BaseHierarchicalAdapter)
├── _build_wrapped_hierarchy()
│   └── Wraps behavior.actions → BaseActionsAdapter
└── serialize()
    └── Assembles behavior name + actions.serialize()

BaseActionsAdapter(BaseHierarchicalAdapter)
├── _build_wrapped_hierarchy()
│   └── Wraps each action → ActionAdapter
└── serialize()
    └── Iterates action_adapters, calls serialize() on each
```

### Benefits

1. **Single traversal**: Hierarchy built once at construction
2. **Unified pattern**: Both display adapters and code generators use same base
3. **Performance**: No repeated adapter creation
4. **Maintainability**: Traversal logic centralized
5. **Consistency**: Same approach for all hierarchical adapters

## Implementation Plan

### Phase 1: Create Base Classes

#### 1.1 BaseHierarchicalAdapter
**File:** `agile_bot/src/cli/base_hierarchical_adapter.py`

**Responsibilities:**
- Abstract base class for all hierarchical adapters
- Stores domain object, channel, and factory
- Calls `_build_wrapped_hierarchy()` in `__init__`
- Provides abstract methods for subclasses

**Key Methods:**
- `__init__(domain_object, channel, factory=None)`
- `_build_wrapped_hierarchy()` (abstract)
- `serialize()` (abstract)

#### 1.2 BaseBotAdapter
**File:** `agile_bot/src/cli/base_bot_adapter.py`

**Responsibilities:**
- Handles Bot → Behaviors wrapping
- Builds behaviors adapter at construction
- Provides abstract formatting methods

**Key Methods:**
- `_build_wrapped_hierarchy()`: Creates behaviors adapter
- `format_header()` (abstract)
- `format_bot_info()` (abstract)
- `format_footer()` (abstract)
- `serialize()`: Assembles header + bot info + behaviors + footer

#### 1.3 BaseBehaviorsAdapter
**File:** `agile_bot/src/cli/base_behaviors_adapter.py`

**Responsibilities:**
- Handles Behaviors → Behavior wrapping
- Builds behavior adapters list at construction
- Tracks current behavior

**Key Methods:**
- `_build_wrapped_hierarchy()`: Creates behavior adapter for each behavior
- `serialize()`: Iterates behavior adapters, calls serialize()

#### 1.4 BaseBehaviorAdapter
**File:** `agile_bot/src/cli/base_behavior_adapter.py`

**Responsibilities:**
- Handles Behavior → Actions wrapping
- Builds actions adapter at construction
- Tracks is_current flag

**Key Methods:**
- `_build_wrapped_hierarchy()`: Creates actions adapter
- `format_behavior_name()` (abstract)
- `_indent_actions()`: Helper for indenting actions output
- `serialize()`: Assembles behavior name + actions

#### 1.5 BaseActionsAdapter
**File:** `agile_bot/src/cli/base_actions_adapter.py`

**Responsibilities:**
- Handles Actions → Action wrapping
- Builds action adapters list at construction
- Tracks current action

**Key Methods:**
- `_build_wrapped_hierarchy()`: Creates action adapter for each action
- `serialize()`: Iterates action adapters, calls serialize()

### Phase 2: Refactor Display Adapters

#### 2.1 Refactor TTY Adapters

**Files to Update:**
- `agile_bot/src/bot/tty_bot.py`
- `agile_bot/src/behaviors/tty_behavior.py`
- `agile_bot/src/actions/tty_actions.py`

**Changes:**
- `TTYBot` inherits from `BaseBotAdapter` and `TTYAdapter`
- `TTYBehaviors` inherits from `BaseBehaviorsAdapter` and `TTYAdapter`
- `TTYBehavior` inherits from `BaseBehaviorAdapter` and `TTYAdapter`
- `TTYActions` inherits from `BaseActionsAdapter` and `TTYAdapter`
- Remove lazy adapter creation from properties
- Implement abstract formatting methods
- Simplify `serialize()` to use pre-built hierarchy

**Before:**
```python
class TTYBot(TTYAdapter):
    @property
    def behaviors(self):
        from agile_bot.src.cli.adapter_factory import AdapterFactory
        tty_behaviors = AdapterFactory.create(self.bot.behaviors, 'tty')
        return tty_behaviors.serialize()
```

**After:**
```python
class TTYBot(BaseBotAdapter, TTYAdapter):
    def format_header(self) -> str:
        return self.header
    
    def format_bot_info(self) -> str:
        return f"{self.name}\n{self.bot_paths}"
    
    def format_footer(self) -> str:
        return self.behavior_action_summary
```

#### 2.2 Refactor Markdown Adapters

**Files to Update:**
- `agile_bot/src/bot/markdown_bot.py`
- `agile_bot/src/behaviors/markdown_behavior.py`
- `agile_bot/src/actions/markdown_actions.py` (if exists)

**Changes:**
- Same pattern as TTY adapters
- Inherit from base hierarchical adapters
- Implement channel-specific formatting methods

#### 2.3 Refactor JSON Adapters

**Files to Update:**
- `agile_bot/src/bot/json_bot.py`
- `agile_bot/src/behaviors/json_behavior.py`
- `agile_bot/src/actions/json_actions.py` (if exists)

**Changes:**
- Same pattern as TTY adapters
- JSON adapters may use `to_dict()` instead of `serialize()`
- May need to adjust base class interface for JSON

### Phase 3: Refactor Code Generation Visitor

#### 3.1 Refactor CursorCommandVisitor

**File:** `agile_bot/src/cli/cursor/cursor_command_visitor.py`

**Changes:**
- Inherit from `BaseBehaviorsAdapter` and `Visitor`
- Use hierarchical adapter pattern for traversal
- Remove dependency on `Orchestrator` for traversal
- Keep visitor methods for code generation logic

**Before:**
```python
class CursorCommandVisitor(Visitor):
    def generate(self) -> Dict[str, Path]:
        orchestrator = Orchestrator(self)
        orchestrator.generate()
        return self.commands
```

**After:**
```python
class CursorCommandVisitor(BaseBehaviorsAdapter, Visitor):
    def __init__(self, workspace_root, bot_location, bot, bot_name):
        Visitor.__init__(self, bot=bot)
        BaseBehaviorsAdapter.__init__(self, bot.behaviors, channel='cursor')
        # ... other initialization
    
    def _build_wrapped_hierarchy(self):
        # Build CursorBehaviorWrapper for each behavior
        # Similar to BaseBehaviorsAdapter but creates CursorBehaviorWrapper
    
    def serialize(self) -> str:
        # Generate command files using pre-built hierarchy
        # Call visit methods on behavior adapters
        return ""
```

#### 3.2 Create CursorBehaviorWrapper

**File:** `agile_bot/src/cli/cursor/cursor_behavior_wrapper.py`

**Responsibilities:**
- Wraps Behavior for Cursor command generation
- Inherits from `BaseBehaviorAdapter`
- Implements command file generation logic

### Phase 4: Update AdapterFactory

#### 4.1 Support Channel-Specific Base Classes

**File:** `agile_bot/src/cli/adapter_factory.py`

**Changes:**
- May need to adjust factory to work with new base classes
- Ensure factory creates adapters with correct inheritance
- Verify channel parameter is passed correctly

### Phase 5: Testing and Validation

#### 5.1 Unit Tests

**Test Files:**
- `agile_bot/test/test_tty_bot.py` (if exists)
- `agile_bot/test/test_markdown_bot.py` (if exists)
- `agile_bot/test/test_json_bot.py` (if exists)
- `agile_bot/test/test_cursor_command_visitor.py` (if exists)

**Test Cases:**
- Verify hierarchy is built at construction time
- Verify no repeated adapter creation
- Verify output format matches current implementation
- Verify all three channels (TTY, Markdown, JSON) work correctly

#### 5.2 Integration Tests

**Test Files:**
- `agile_bot/test/CLI/test_initialize_cli_session.py`
- `agile_bot/test/CLI/test_navigate_behaviors_using_cli_commands.py`
- Other CLI test files

**Test Cases:**
- Verify CLI output matches expected format
- Verify all commands work correctly
- Verify no performance regressions

#### 5.3 Code Generation Tests

**Test Files:**
- Tests for `generate.py` scripts

**Test Cases:**
- Verify Cursor commands are generated correctly
- Verify registry is updated correctly
- Verify no missing command files

## Migration Strategy

### Step-by-Step Approach

1. **Create base classes** (Phase 1)
   - Implement all base hierarchical adapter classes
   - Add unit tests for base classes
   - Verify base classes work in isolation

2. **Migrate one adapter type** (Phase 2.1)
   - Start with TTY adapters (most complex)
   - Refactor one adapter at a time (Bot → Behaviors → Behavior → Actions)
   - Run tests after each adapter migration
   - Verify output matches current implementation

3. **Migrate other channels** (Phase 2.2, 2.3)
   - Migrate Markdown adapters
   - Migrate JSON adapters
   - Run tests after each channel

4. **Migrate code generation** (Phase 3)
   - Refactor CursorCommandVisitor
   - Create CursorBehaviorWrapper
   - Run code generation tests

5. **Cleanup** (Phase 4, 5)
   - Update AdapterFactory if needed
   - Remove old traversal logic
   - Remove Orchestrator dependency from adapters (keep for backward compatibility if needed)
   - Update documentation

### Backward Compatibility

- Keep `Orchestrator` class for any code that still uses it
- Ensure existing adapter interfaces remain unchanged
- Verify all existing tests pass

## Success Criteria

1. ✅ All adapters use BaseHierarchicalAdapter pattern
2. ✅ Hierarchy is built at construction time (not lazily)
3. ✅ No repeated adapter creation during serialization
4. ✅ CursorCommandVisitor uses same pattern as display adapters
5. ✅ All existing tests pass
6. ✅ CLI output format unchanged
7. ✅ Code generation output unchanged
8. ✅ Performance improved (no repeated adapter creation)

## Risks and Mitigation

### Risk 1: Breaking Changes
**Mitigation:** Migrate one adapter at a time, run tests after each change

### Risk 2: Performance Regression
**Mitigation:** Profile before/after, ensure construction-time building is faster

### Risk 3: Complex Inheritance
**Mitigation:** Use composition where inheritance becomes too complex

### Risk 4: JSON Adapters May Need Different Interface
**Mitigation:** Create JSON-specific base class if needed, or adjust interface

## Future Enhancements

1. **Caching**: Cache adapter instances if same domain object is adapted multiple times
2. **Lazy Loading**: Option to build hierarchy lazily for very large hierarchies
3. **Visitor Integration**: Make base classes work seamlessly with visitor pattern
4. **Type Safety**: Add type hints for better IDE support

## Timeline Estimate

- **Phase 1**: 2-3 days (base classes)
- **Phase 2**: 3-4 days (display adapters)
- **Phase 3**: 2-3 days (code generation)
- **Phase 4**: 1 day (factory updates)
- **Phase 5**: 2-3 days (testing)

**Total: 10-14 days**

## References

- Current adapter implementations: `agile_bot/src/bot/tty_bot.py`, `agile_bot/src/behaviors/tty_behavior.py`
- Current visitor implementation: `agile_bot/src/cli/cursor/cursor_command_visitor.py`
- Current orchestrator: `agile_bot/src/cli/orchestrator.py`
- Adapter factory: `agile_bot/src/cli/adapter_factory.py`
