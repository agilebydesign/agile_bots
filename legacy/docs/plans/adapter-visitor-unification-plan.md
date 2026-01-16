# Adapter-Visitor Unification Plan

## Overview

This plan synchronizes the visitor pattern approach (used by `CursorCommandVisitor`) with all display adapters (TTY, Markdown, JSON) to create a unified hierarchical adapter pattern. This will eliminate duplicate traversal logic and provide a consistent approach for both display serialization and code generation.

## Current State Analysis

### Adapter Pattern (Display Adapters)

**Current Implementation:**
- Adapters wrap domain objects (Bot, Behaviors, Behavior, Actions)
- Child adapters are created **lazily** via `AdapterFactory.create()` when properties are accessed
- Each adapter handles its own traversal logic independently
- Example: `TTYBot` creates `TTYBehaviors` via factory when accessing `self.behaviors` property

**Files:**
- `agile_bot/src/bot/tty_bot.py` - Creates TTYBehaviors lazily
- `agile_bot/src/behaviors/tty_behavior.py` - Creates TTYActions lazily
- `agile_bot/src/actions/tty_actions.py` - Creates TTYAction instances lazily
- Similar pattern in `markdown_bot.py`, `json_bot.py`, etc.

**Traversal Pattern:**
```python
# In TTYBot.serialize()
tty_behaviors = AdapterFactory.create(self.bot.behaviors, 'tty')
# In TTYBehaviors
for behavior in self.behaviors:
    behavior_adapter = TTYBehavior(behavior, is_current=is_current)
# In TTYBehavior
actions_adapter = TTYActions(self.behavior.actions)
```

### Visitor Pattern (Code Generation)

**Current Implementation:**
- `CursorCommandVisitor` uses `Orchestrator` to traverse Bot → Behaviors → Behavior → Actions
- `Orchestrator` centralizes traversal logic and calls visitor methods
- Visitor methods (`visit_header`, `visit_behavior`, `visit_action`, `visit_footer`) are called during traversal
- Traversal happens at **runtime** during `generate()` call

**Files:**
- `agile_bot/src/cli/cursor/cursor_command_visitor.py` - Implements Visitor interface
- `agile_bot/src/cli/orchestrator.py` - Centralizes traversal logic
- `agile_bot/src/cli/visitor.py` - Abstract Visitor base class

**Traversal Pattern:**
```python
# Orchestrator.generate()
self.visitor.visit_header(self.bot_name)
for behavior in sorted_behaviors:
    self._visit_behavior(behavior)
    # Creates BehaviorHelpContext and calls visitor.visit_behavior()
self.visitor.visit_footer()
```

### Problems with Current Approach

1. **Duplicate Traversal Logic**: Both adapters and visitor pattern traverse the same Bot hierarchy, but with different approaches
2. **Inconsistent Timing**: Adapters create child adapters lazily (on-demand), visitor traverses eagerly (during generate())
3. **No Shared Base**: Adapters and visitors don't share common traversal logic
4. **Maintenance Burden**: Changes to hierarchy traversal require updates in multiple places
5. **Performance**: Lazy adapter creation means repeated factory calls for same objects

## Proposed Solution: BaseHierarchicalAdapter Pattern

### Core Concept

Create a `BaseHierarchicalAdapter` that:
- Builds the wrapped adapter hierarchy at **construction time** (not lazily)
- Centralizes traversal logic for Bot → Behaviors → Behavior → Actions
- Can be inherited by both display adapters (TTY, Markdown, JSON) and code generators (CursorCommandVisitor)
- Uses `AdapterFactory` to create child adapters during initialization

### Architecture

```
BaseHierarchicalAdapter (ABC)
├── BaseBotAdapter
│   ├── TTYBot
│   ├── MarkdownBot
│   └── JSONBot
├── BaseBehaviorsAdapter
│   ├── TTYBehaviors
│   ├── MarkdownBehaviors
│   └── JSONBehaviors
├── BaseBehaviorAdapter
│   ├── TTYBehavior
│   ├── MarkdownBehavior
│   └── JSONBehavior
├── BaseActionsAdapter
│   ├── TTYActions
│   ├── MarkdownActions
│   └── JSONActions
└── CursorCommandVisitor (also inherits Visitor)
```

### Key Design Decisions

1. **Construction-Time Hierarchy Building**: All child adapters are created in `__init__` via `_build_wrapped_hierarchy()`
2. **Factory Pattern**: Uses `AdapterFactory` to create child adapters (maintains existing factory pattern)
3. **Channel Parameter**: Base classes accept `channel` parameter ('tty', 'markdown', 'json', 'cursor')
4. **Separation of Concerns**: Base classes handle traversal/wrapping, subclasses handle formatting/generation
5. **Backward Compatibility**: Existing adapter interfaces (`serialize()`, properties) remain unchanged

## Implementation Plan

### Phase 1: Create Base Hierarchical Adapter Classes

#### 1.1 BaseHierarchicalAdapter (Abstract Base)

**File:** `agile_bot/src/cli/base_hierarchical_adapter.py`

```python
from abc import ABC, abstractmethod
from typing import Optional
from agile_bot.src.cli.adapter_factory import AdapterFactory

class BaseHierarchicalAdapter(ABC):
    def __init__(self, domain_object, channel: str, factory: Optional[AdapterFactory] = None):
        self.domain_object = domain_object
        self.channel = channel
        self.factory = factory or AdapterFactory
        self._build_wrapped_hierarchy()
    
    @abstractmethod
    def _build_wrapped_hierarchy(self):
        """Build wrapped adapter hierarchy at construction time."""
        pass
    
    @abstractmethod
    def serialize(self) -> str:
        """Serialize the wrapped hierarchy."""
        pass
```

#### 1.2 BaseBotAdapter

**File:** `agile_bot/src/cli/base_bot_adapter.py`

```python
from .base_hierarchical_adapter import BaseHierarchicalAdapter

class BaseBotAdapter(BaseHierarchicalAdapter):
    def __init__(self, bot, channel: str):
        super().__init__(bot, channel)
        self.bot = bot
        self._behaviors_adapter = None
    
    def _build_wrapped_hierarchy(self):
        if self.bot.behaviors:
            self._behaviors_adapter = self.factory.create(self.bot.behaviors, self.channel)
    
    @abstractmethod
    def format_header(self) -> str:
        pass
    
    @abstractmethod
    def format_bot_info(self) -> str:
        pass
    
    @abstractmethod
    def format_footer(self) -> str:
        pass
    
    def serialize(self) -> str:
        lines = []
        lines.append(self.format_header())
        lines.append(self.format_bot_info())
        if self._behaviors_adapter:
            lines.append(self._behaviors_adapter.serialize())
        lines.append(self.format_footer())
        return '\n'.join(lines)
```

#### 1.3 BaseBehaviorsAdapter

**File:** `agile_bot/src/cli/base_behaviors_adapter.py`

```python
from .base_hierarchical_adapter import BaseHierarchicalAdapter
from typing import List

class BaseBehaviorsAdapter(BaseHierarchicalAdapter):
    def __init__(self, behaviors, channel: str):
        super().__init__(behaviors, channel)
        self.behaviors = behaviors
        self._behavior_adapters: List = []
    
    def _build_wrapped_hierarchy(self):
        current_behavior_name = (
            self.behaviors.current.name 
            if self.behaviors.current 
            else None
        )
        sorted_behaviors = sorted(list(self.behaviors), key=lambda b: b.order)
        
        for behavior in sorted_behaviors:
            is_current = behavior.name == current_behavior_name
            behavior_adapter = self.factory.create(behavior, self.channel)
            behavior_adapter._is_current = is_current
            behavior_adapter._behavior = behavior
            self._behavior_adapters.append(behavior_adapter)
    
    def serialize(self) -> str:
        lines = []
        for behavior_adapter in self._behavior_adapters:
            lines.append(behavior_adapter.serialize())
        return '\n'.join(lines)
```

#### 1.4 BaseBehaviorAdapter

**File:** `agile_bot/src/cli/base_behavior_adapter.py`

```python
from .base_hierarchical_adapter import BaseHierarchicalAdapter

class BaseBehaviorAdapter(BaseHierarchicalAdapter):
    def __init__(self, behavior, channel: str, is_current: bool = False):
        super().__init__(behavior, channel)
        self.behavior = behavior
        self.is_current = is_current
        self._actions_adapter = None
    
    def _build_wrapped_hierarchy(self):
        if self.behavior.actions:
            self._actions_adapter = self.factory.create(self.behavior.actions, self.channel)
            if hasattr(self._actions_adapter, '_set_current_behavior'):
                self._actions_adapter._set_current_behavior(self.behavior)
    
    @abstractmethod
    def format_behavior_name(self) -> str:
        pass
    
    def serialize(self) -> str:
        lines = []
        lines.append(self.format_behavior_name())
        if self.is_current and self._actions_adapter:
            actions_output = self._actions_adapter.serialize()
            lines.append(self._indent_actions(actions_output))
        return '\n'.join(lines)
    
    def _indent_actions(self, actions_output: str) -> str:
        return '\n'.join(f"  {line}" if line else "" for line in actions_output.split('\n'))
```

#### 1.5 BaseActionsAdapter

**File:** `agile_bot/src/cli/base_actions_adapter.py`

```python
from .base_hierarchical_adapter import BaseHierarchicalAdapter
from typing import List

class BaseActionsAdapter(BaseHierarchicalAdapter):
    def __init__(self, actions, channel: str):
        super().__init__(actions, channel)
        self.actions = actions
        self._action_adapters: List = []
        self._current_behavior = None
    
    def _set_current_behavior(self, behavior):
        self._current_behavior = behavior
    
    def _build_wrapped_hierarchy(self):
        current_action_name = (
            self.actions.current.action_name 
            if self.actions.current 
            else None
        )
        for action in self.actions:
            is_current = action.action_name == current_action_name
            action_adapter = self.factory.create(action, self.channel)
            action_adapter._is_current = is_current
            action_adapter._action = action
            self._action_adapters.append(action_adapter)
    
    def serialize(self) -> str:
        lines = []
        for action_adapter in self._action_adapters:
            lines.append(action_adapter.serialize())
        return '\n'.join(lines)
```

### Phase 2: Refactor Existing Adapters

#### 2.1 Refactor TTYBot

**File:** `agile_bot/src/bot/tty_bot.py`

**Changes:**
- Inherit from `BaseBotAdapter` and `TTYAdapter`
- Remove lazy `AdapterFactory.create()` calls from properties
- Move hierarchy building to `_build_wrapped_hierarchy()`
- Keep existing `serialize()` logic but use pre-built `_behaviors_adapter`
- Implement abstract methods: `format_header()`, `format_bot_info()`, `format_footer()`

**Before:**
```python
class TTYBot(TTYAdapter):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @property
    def behaviors(self):
        tty_behaviors = AdapterFactory.create(self.bot.behaviors, 'tty')
        return tty_behaviors.serialize()
```

**After:**
```python
class TTYBot(BaseBotAdapter, TTYAdapter):
    def __init__(self, bot: Bot):
        BaseBotAdapter.__init__(self, bot, 'tty')
        TTYAdapter.__init__(self)
    
    def format_header(self) -> str:
        return self.header
    
    def format_bot_info(self) -> str:
        lines = []
        lines.append(self.name)
        lines.append(self.bot_paths)
        return '\n'.join(lines)
    
    def format_footer(self) -> str:
        return self.behavior_action_summary
```

#### 2.2 Refactor TTYBehaviors

**File:** `agile_bot/src/behaviors/tty_behavior.py`

**Changes:**
- Inherit from `BaseBehaviorsAdapter` and `TTYAdapter`
- Remove manual iteration and adapter creation
- Use pre-built `_behavior_adapters` from base class
- Keep existing `serialize()` logic

#### 2.3 Refactor TTYBehavior

**File:** `agile_bot/src/behaviors/tty_behavior.py`

**Changes:**
- Inherit from `BaseBehaviorAdapter` and `TTYAdapter`
- Remove lazy `TTYActions` creation
- Use pre-built `_actions_adapter` from base class
- Implement `format_behavior_name()`

#### 2.4 Refactor TTYActions

**File:** `agile_bot/src/actions/tty_actions.py`

**Changes:**
- Inherit from `BaseActionsAdapter` and `TTYAdapter`
- Remove manual iteration and adapter creation
- Use pre-built `_action_adapters` from base class

#### 2.5 Repeat for Markdown and JSON Adapters

Apply same refactoring pattern to:
- `MarkdownBot`, `MarkdownBehaviors`, `MarkdownBehavior`, `MarkdownActions`
- `JSONBot`, `JSONBehaviors`, `JSONBehavior`, `JSONActions`

### Phase 3: Refactor CursorCommandVisitor

#### 3.1 Update CursorCommandVisitor

**File:** `agile_bot/src/cli/cursor/cursor_command_visitor.py`

**Changes:**
- Inherit from `BaseBehaviorsAdapter` and `Visitor`
- Remove `Orchestrator` dependency (traversal handled by base class)
- Use pre-built `_behavior_adapters` from base class
- Override `serialize()` to generate command files instead of display output
- Keep existing `visit_behavior()` logic but adapt to use pre-built adapters

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
    def __init__(self, workspace_root: Path, bot_location: Path, bot: Bot, bot_name: str):
        Visitor.__init__(self, bot=bot)
        BaseBehaviorsAdapter.__init__(self, bot.behaviors, channel='cursor')
        # ... rest of init
    
    def serialize(self) -> str:
        self.commands_dir = self._ensure_commands_directory()
        self._generate_base_commands()
        for behavior_adapter in self._behavior_adapters:
            behavior_adapter.generate_command_file(self.commands_dir, self.commands)
        self._remove_obsolete_command_files()
        return ""
    
    def generate(self) -> Dict[str, Path]:
        self.serialize()
        return self.commands
```

#### 3.2 Update AdapterFactory

**File:** `agile_bot/src/cli/adapter_factory.py`

**Changes:**
- Add 'cursor' channel support for Behaviors
- Register `CursorCommandVisitor` as adapter for ('Behaviors', 'cursor')

### Phase 4: Update Orchestrator (Optional)

**Decision Point:** Keep `Orchestrator` for backward compatibility or remove it?

**Option A: Keep Orchestrator**
- Maintain `Orchestrator` for any code that still uses visitor pattern directly
- `CursorCommandVisitor` no longer needs it (uses base class traversal)
- Other potential visitors can still use it

**Option B: Remove Orchestrator**
- If no other code uses visitor pattern, remove `Orchestrator`
- Simplify codebase

**Recommendation:** Keep `Orchestrator` initially for backward compatibility, remove later if unused.

## Migration Strategy

### Step 1: Add Base Classes (Non-Breaking)

1. Create all `BaseHierarchicalAdapter` classes
2. Add to `AdapterFactory` registry (no changes to existing adapters yet)
3. Run tests to ensure no regressions

### Step 2: Refactor One Channel at a Time

**Order:** TTY → Markdown → JSON → Cursor

1. Refactor TTY adapters to use base classes
2. Run TTY-specific tests
3. Verify CLI output matches exactly
4. Repeat for Markdown, then JSON

### Step 3: Refactor CursorCommandVisitor

1. Update `CursorCommandVisitor` to inherit from `BaseBehaviorsAdapter`
2. Remove `Orchestrator` dependency
3. Test command generation
4. Verify generated command files match previous output

### Step 4: Cleanup

1. Remove unused `Orchestrator` if no longer needed
2. Remove duplicate traversal logic from adapters
3. Update documentation

## Testing Strategy

### Unit Tests

1. **Base Class Tests:**
   - Test `_build_wrapped_hierarchy()` creates correct adapter tree
   - Test hierarchy building with empty collections
   - Test hierarchy building with single/multiple items

2. **Adapter Tests:**
   - Test each refactored adapter produces identical output to before
   - Test TTY/Markdown/JSON adapters produce correct format
   - Test edge cases (no behaviors, no actions, etc.)

3. **Visitor Tests:**
   - Test `CursorCommandVisitor` generates same command files
   - Test command file content matches expected format

### Integration Tests

1. **CLI Output Tests:**
   - Run CLI in TTY mode, capture output, compare to expected
   - Run CLI in Markdown mode, capture output, compare to expected
   - Run CLI in JSON mode, parse output, verify structure

2. **Command Generation Tests:**
   - Run `generate.py` for story_bot
   - Verify all command files created correctly
   - Verify registry updated correctly

### Regression Tests

1. Run all existing CLI tests
2. Run all existing adapter tests
3. Verify no performance regressions (construction-time building should be faster than lazy)

## Benefits

1. **Unified Traversal Logic**: Single source of truth for Bot hierarchy traversal
2. **Consistent Pattern**: Both display adapters and code generators use same approach
3. **Performance**: Construction-time building eliminates repeated factory calls
4. **Maintainability**: Changes to hierarchy structure only require base class updates
5. **Extensibility**: Easy to add new channels (e.g., 'html', 'xml') by inheriting base classes
6. **Testability**: Base classes can be tested independently

## Risks and Mitigations

### Risk 1: Breaking Changes

**Mitigation:**
- Refactor one channel at a time
- Comprehensive test coverage before/after
- Keep old code until new code verified

### Risk 2: Performance Impact

**Mitigation:**
- Construction-time building should be faster (no repeated factory calls)
- Profile before/after to verify
- Can optimize base class if needed

### Risk 3: Complex Inheritance

**Mitigation:**
- Keep base classes simple and focused
- Clear separation: base handles traversal, subclass handles formatting
- Comprehensive documentation

## Success Criteria

1. ✅ All adapters produce identical output to before refactoring
2. ✅ `CursorCommandVisitor` generates identical command files
3. ✅ All tests pass
4. ✅ No performance regressions
5. ✅ Code is simpler and more maintainable
6. ✅ Base classes are reusable for future channels

## Timeline Estimate

- **Phase 1 (Base Classes):** 2-3 days
- **Phase 2 (Refactor Adapters):** 3-4 days
- **Phase 3 (Refactor Visitor):** 1-2 days
- **Phase 4 (Cleanup):** 1 day
- **Testing:** 2-3 days

**Total:** ~10-13 days

## Next Steps

1. Review and approve this plan
2. Create base class files
3. Write unit tests for base classes
4. Begin Phase 2 refactoring with TTY adapters
5. Iterate and refine based on findings
