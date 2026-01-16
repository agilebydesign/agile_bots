# Adapter-Visitor Synchronization Plan

## Overview

This plan outlines the refactoring to synchronize the adapter pattern (wrapping domain objects) with the visitor pattern (orchestrating traversal) into a unified hierarchical adapter approach. The goal is to eliminate duplicate traversal logic and ensure consistent hierarchy building across all adapters and code generators.

## Current State Analysis

### Adapter Pattern (Current)
- **Location**: `agile_bot/src/bot/tty_bot.py`, `agile_bot/src/behaviors/tty_behavior.py`, `agile_bot/src/actions/tty_actions.py`
- **Approach**: Lazy hierarchy building during serialization
- **Pattern**: 
  - Adapters wrap domain objects (Bot, Behaviors, Behavior, Actions)
  - Child adapters created on-demand via `AdapterFactory.create()` in properties/methods
  - Hierarchy built repeatedly during each `serialize()` call
  - Example: `TTYBot` creates `TTYBehaviors` adapter in `progress` property, which creates `TTYBehavior` adapters, which create `TTYActions` adapters

### Visitor Pattern (Current)
- **Location**: `agile_bot/src/cli/orchestrator.py`, `agile_bot/src/cli/cursor/cursor_command_visitor.py`
- **Approach**: Explicit traversal orchestration
- **Pattern**:
  - `Orchestrator` traverses Bot → Behaviors → Behavior → Actions
  - Calls visitor methods (`visit_header`, `visit_behavior`, `visit_action`, `visit_footer`)
  - `CursorCommandVisitor` uses this to generate command files
  - Hierarchy built once during traversal

### Problems Identified

1. **Duplicate Traversal Logic**: Both adapters and visitors traverse the same Bot-Behaviors-Actions hierarchy, but with different approaches
2. **Repeated Adapter Creation**: Adapters create child adapters multiple times during serialization (inefficient)
3. **Inconsistent Patterns**: Display adapters use lazy creation, code generators use explicit traversal
4. **Maintenance Burden**: Changes to hierarchy structure require updates in multiple places

## Proposed Solution: Hierarchical Adapter Pattern

### Core Concept

Create a `BaseHierarchicalAdapter` that builds the wrapped adapter hierarchy at construction time, using visitor-like traversal logic. This unifies both display adapters and code generators under a single pattern.

### Architecture

```
BaseHierarchicalAdapter (ABC)
├── _build_wrapped_hierarchy() [abstract]
├── serialize() [abstract]
└── Uses AdapterFactory to create child adapters

BaseBotAdapter(BaseHierarchicalAdapter)
├── Wraps Bot → Behaviors
├── _build_wrapped_hierarchy() builds BehaviorsAdapter
└── serialize() formats header, bot info, behaviors, footer

BaseBehaviorsAdapter(BaseHierarchicalAdapter)
├── Wraps Behaviors → List[BehaviorAdapter]
├── _build_wrapped_hierarchy() builds BehaviorAdapters
└── serialize() formats all behaviors

BaseBehaviorAdapter(BaseHierarchicalAdapter)
├── Wraps Behavior → ActionsAdapter
├── _build_wrapped_hierarchy() builds ActionsAdapter
└── serialize() formats behavior name and actions

BaseActionsAdapter(BaseHierarchicalAdapter)
├── Wraps Actions → List[ActionAdapter]
├── _build_wrapped_hierarchy() builds ActionAdapters
└── serialize() formats all actions
```

## Implementation Plan

### Phase 1: Create Base Hierarchical Adapter Classes

#### 1.1 Create `BaseHierarchicalAdapter`
- **File**: `agile_bot/src/cli/base_hierarchical_adapter.py`
- **Purpose**: Abstract base class for all hierarchical adapters
- **Key Methods**:
  - `__init__(domain_object, channel, factory)` - Calls `_build_wrapped_hierarchy()`
  - `_build_wrapped_hierarchy()` [abstract] - Builds adapter tree at construction
  - `serialize()` [abstract] - Formats output using pre-built hierarchy

#### 1.2 Create `BaseBotAdapter`
- **File**: `agile_bot/src/cli/base_bot_adapter.py`
- **Inherits**: `BaseHierarchicalAdapter`
- **Purpose**: Base for Bot adapters (TTY, Markdown, JSON)
- **Key Methods**:
  - `_build_wrapped_hierarchy()` - Creates `BehaviorsAdapter` if `bot.behaviors` exists
  - `format_header()` [abstract] - Channel-specific header formatting
  - `format_bot_info()` [abstract] - Channel-specific bot info formatting
  - `format_footer()` [abstract] - Channel-specific footer formatting
  - `serialize()` - Assembles header + bot info + behaviors + footer

#### 1.3 Create `BaseBehaviorsAdapter`
- **File**: `agile_bot/src/cli/base_behaviors_adapter.py`
- **Inherits**: `BaseHierarchicalAdapter`
- **Purpose**: Base for Behaviors adapters
- **Key Methods**:
  - `_build_wrapped_hierarchy()` - Creates `BehaviorAdapter` for each behavior, marks current
  - `serialize()` - Formats all behavior adapters

#### 1.4 Create `BaseBehaviorAdapter`
- **File**: `agile_bot/src/cli/base_behavior_adapter.py`
- **Inherits**: `BaseHierarchicalAdapter`
- **Purpose**: Base for Behavior adapters
- **Key Methods**:
  - `_build_wrapped_hierarchy()` - Creates `ActionsAdapter` if `behavior.actions` exists
  - `format_behavior_name()` [abstract] - Channel-specific behavior name formatting
  - `serialize()` - Formats behavior name + actions (if current)

#### 1.5 Create `BaseActionsAdapter`
- **File**: `agile_bot/src/cli/base_actions_adapter.py`
- **Inherits**: `BaseHierarchicalAdapter`
- **Purpose**: Base for Actions adapters
- **Key Methods**:
  - `_build_wrapped_hierarchy()` - Creates `ActionAdapter` for each action, marks current
  - `serialize()` - Formats all action adapters

### Phase 2: Refactor TTY Adapters

#### 2.1 Refactor `TTYBot`
- **File**: `agile_bot/src/bot/tty_bot.py`
- **Changes**:
  - Inherit from `BaseBotAdapter` and `TTYAdapter`
  - Remove lazy adapter creation from properties
  - Implement `format_header()`, `format_bot_info()`, `format_footer()`
  - Simplify `serialize()` to use pre-built hierarchy

#### 2.2 Refactor `TTYBehaviors`
- **File**: `agile_bot/src/behaviors/tty_behavior.py`
- **Changes**:
  - Inherit from `BaseBehaviorsAdapter` and `TTYAdapter`
  - Remove lazy adapter creation
  - Use pre-built `_behavior_adapters` list in `serialize()`

#### 2.3 Refactor `TTYBehavior`
- **File**: `agile_bot/src/behaviors/tty_behavior.py`
- **Changes**:
  - Inherit from `BaseBehaviorAdapter` and `TTYAdapter`
  - Implement `format_behavior_name()`
  - Use pre-built `_actions_adapter` in `serialize()`

#### 2.4 Refactor `TTYActions`
- **File**: `agile_bot/src/actions/tty_actions.py`
- **Changes**:
  - Inherit from `BaseActionsAdapter` and `TTYAdapter`
  - Use pre-built `_action_adapters` list in `serialize()`

### Phase 3: Refactor Markdown Adapters

#### 3.1 Refactor `MarkdownBot`
- **File**: `agile_bot/src/bot/markdown_bot.py`
- **Changes**: Same pattern as TTY adapters

#### 3.2 Refactor `MarkdownBehaviors`
- **File**: `agile_bot/src/behaviors/markdown_behavior.py`
- **Changes**: Same pattern as TTY adapters

#### 3.3 Refactor `MarkdownBehavior`
- **File**: `agile_bot/src/behaviors/markdown_behavior.py`
- **Changes**: Same pattern as TTY adapters

#### 3.4 Refactor `MarkdownActions`
- **File**: `agile_bot/src/actions/markdown_actions.py` (may need to be created)
- **Changes**: Same pattern as TTY adapters

### Phase 4: Refactor JSON Adapters

#### 4.1 Refactor `JSONBot`
- **File**: `agile_bot/src/bot/json_bot.py`
- **Changes**: Same pattern, but JSON uses `to_dict()` instead of `serialize()`
- **Note**: May need to adapt pattern for dictionary-based serialization

#### 4.2 Refactor JSON Behaviors/Behavior/Actions
- **Files**: `agile_bot/src/behaviors/json_behavior.py`, `agile_bot/src/actions/json_actions.py`
- **Changes**: Adapt pattern for dictionary-based serialization

### Phase 5: Refactor CursorCommandVisitor

#### 5.1 Update `CursorCommandVisitor`
- **File**: `agile_bot/src/cli/cursor/cursor_command_visitor.py`
- **Changes**:
  - Inherit from `BaseBehaviorsAdapter` and `Visitor`
  - Use `_build_wrapped_hierarchy()` to build `CursorBehaviorWrapper` adapters
  - Remove dependency on `Orchestrator` for traversal (keep for context building)
  - Use pre-built hierarchy in `generate()` method

#### 5.2 Create `CursorBehaviorWrapper`
- **File**: `agile_bot/src/cli/cursor/cursor_behavior_wrapper.py`
- **Purpose**: Wrapper that inherits from `BaseBehaviorAdapter` for Cursor command generation
- **Changes**: Handles behavior-specific command file generation

### Phase 6: Testing and Validation

#### 6.1 Update Tests
- Verify TTY output matches exactly (no regression)
- Verify Markdown output matches exactly (no regression)
- Verify JSON output matches exactly (no regression)
- Verify Cursor command generation still works

#### 6.2 Performance Testing
- Measure adapter creation time (should be faster - built once vs. multiple times)
- Measure serialization time (should be similar or faster)

#### 6.3 Integration Testing
- Test full CLI status output in all three modes
- Test Cursor command generation
- Test all existing CLI commands

## Benefits

1. **Single Source of Truth**: Traversal logic centralized in base classes
2. **Performance**: Hierarchy built once at construction, not repeatedly during serialization
3. **Consistency**: All adapters follow same pattern
4. **Maintainability**: Changes to hierarchy structure only need updates in base classes
5. **Extensibility**: Easy to add new channel adapters (e.g., HTML, XML)

## Migration Strategy

1. **Incremental**: Refactor one adapter type at a time (TTY → Markdown → JSON → Visitor)
2. **Backward Compatible**: Keep existing adapter interfaces during migration
3. **Test-Driven**: Write tests first, then refactor to pass
4. **Rollback Plan**: Keep old adapter code until new code is fully validated

## Risks and Mitigations

### Risk 1: Breaking Changes
- **Mitigation**: Maintain backward compatibility, extensive testing

### Risk 2: Performance Regression
- **Mitigation**: Benchmark before/after, optimize if needed

### Risk 3: Complexity Increase
- **Mitigation**: Keep base classes simple, document clearly

## Success Criteria

1. All existing tests pass
2. No performance regression
3. Code is more maintainable (fewer lines, clearer structure)
4. New adapters can be added easily
5. Visitor and adapter patterns are unified

## Timeline Estimate

- Phase 1: 2-3 days (base classes)
- Phase 2: 2-3 days (TTY adapters)
- Phase 3: 1-2 days (Markdown adapters)
- Phase 4: 1-2 days (JSON adapters)
- Phase 5: 2-3 days (CursorCommandVisitor)
- Phase 6: 2-3 days (testing)

**Total**: ~10-16 days

## Next Steps

1. Review and approve this plan
2. Create base hierarchical adapter classes
3. Refactor TTY adapters as proof of concept
4. Validate approach with tests
5. Continue with remaining adapters
