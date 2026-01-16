# Adapter Hierarchical Refactoring Plan

## Goal
Unify all adapters (TTY, Markdown, JSON) to use the same hierarchical traversal pattern as CursorCommandVisitor. Traversal builds adapter wrapper hierarchy at construction time, not during serialization.

## Unification Model

### Unified Architecture: Shared Traversal Base

#### Base Hierarchical Adapter Classes

```
BaseHierarchicalAdapter (ABC)
├── __init__(domain_object, channel, factory)
│   └── Calls _build_wrapped_hierarchy() [construction-time]
├── _build_wrapped_hierarchy() [abstract]
│   └── Traverses domain object and builds adapter tree
└── serialize() [abstract]
    └── Walks already-built adapter tree

BaseBehaviorsAdapter (inherits BaseHierarchicalAdapter)
├── _build_wrapped_hierarchy() [concrete implementation]
│   ├── Sorts behaviors by order
│   ├── Determines current behavior
│   └── Creates wrapped Behavior adapters via Factory
│       └── Stores in _behavior_adapters list
└── serialize() [concrete implementation]
    └── Calls serialize() on each wrapped Behavior adapter
```

#### Command Generator: CursorCommandGenerator

**What it really is:**
- **Not a Visitor pattern** - it's a **generator** that creates Cursor command files
- Current implementation incorrectly uses Visitor + Orchestrator pattern
- **Purpose**: Generate `.md` command files in `.cursor/commands/` directory
- **Current flow**: Orchestrator.generate() → traverses → calls visitor.visit_behavior() → writes file

**The Problem:**
- Visitor + Orchestrator is redundant complexity
- Orchestrator just traverses and calls visit methods - this is what BaseBehaviorsAdapter already does
- Visitor interface (visit_* methods) is unnecessary - just need to generate files

**After Unification:**
```
CursorCommandGenerator → BaseBehaviorsAdapter

Construction (__init__):
├── BaseBehaviorsAdapter.__init__(bot.behaviors, 'cursor')
│   └── _build_wrapped_hierarchy() called automatically
│       ├── Sorts behaviors by order (same logic as TTYBehaviors!)
│       ├── Creates CursorBehaviorWrapper for each behavior
│       └── Stores in _behavior_adapters list
└── Sets up workspace_root, bot_location, commands dict

Generation (serialize()):
├── Overrides BaseBehaviorsAdapter.serialize()
├── Creates commands directory
├── Generates base commands (crc_bot.md, crc_bot_status.md)
├── Iterates through _behavior_adapters (already built at construction!)
│   └── For each CursorBehaviorWrapper:
│       └── Calls generate_command_file()
│           └── Writes behavior command file (crc_bot_walkthrough.md)
└── Removes obsolete command files

Key Insight:
- It's just a generator, not a visitor pattern
- Same traversal as TTYBehaviors (from BaseBehaviorsAdapter)
- Different output: writes files instead of returning strings
- No Visitor interface needed
- No Orchestrator needed
```

**Simplification:**
- Rename `CursorCommandVisitor` → `CursorCommandGenerator` (more accurate name)
- Remove Visitor inheritance (not a visitor pattern)
- Remove Orchestrator dependency (traversal in base class)
- Just inherit BaseBehaviorsAdapter and override serialize() to write files

#### Adapter Pattern: TTYBehaviors

```
TTYBehaviors → BaseBehaviorsAdapter, TTYAdapter

Construction (__init__):
├── BaseBehaviorsAdapter.__init__(behaviors, 'tty')
│   └── _build_wrapped_hierarchy() called automatically
│       ├── Sorts behaviors by order
│       ├── Creates TTYBehavior adapter for each behavior
│       └── Stores in _behavior_adapters list
└── No additional setup needed

Serialization (serialize()):
├── Uses BaseBehaviorsAdapter.serialize() as-is
├── Iterates through _behavior_adapters (already built!)
│   └── For each TTYBehavior:
│       └── Calls serialize()
│           └── Returns formatted string ("- ➤ Behavior Name")
└── Joins all behavior strings with newlines

Key: Same traversal as CursorCommandVisitor, but returns formatted string
```

#### Adapter Pattern: TTYBot

```
TTYBot → BaseBotAdapter, TTYAdapter

Construction (__init__):
├── BaseBotAdapter.__init__(bot, 'tty')
│   └── _build_wrapped_hierarchy() called automatically
│       └── Creates TTYBehaviors adapter
│           └── Stores in _behaviors_adapter
└── Sets up bot-specific properties

Serialization (serialize()):
├── Uses BaseBotAdapter.serialize() (or overrides for custom assembly)
├── Calls format_header() → Returns CLI STATUS header
├── Calls format_bot_info() → Returns bot name and paths
├── Calls _behaviors_adapter.serialize() → Returns formatted behaviors
└── Calls format_footer() → Returns behavior/action summary

Key: Delegates to _behaviors_adapter which uses shared traversal
```

### Shared Traversal Logic

```
┌─────────────────────────────────────────────────────────────┐
│  BaseBehaviorsAdapter._build_wrapped_hierarchy()            │
│  [Called once at construction time]                         │
│                                                             │
│  current_behavior_name = behaviors.current.name             │
│  sorted_behaviors = sorted(behaviors, key=lambda b: b.order)│
│                                                             │
│  for behavior in sorted_behaviors:                          │
│      is_current = behavior.name == current_behavior_name    │
│      adapter = factory.create(behavior, self.channel)      │
│      adapter._is_current = is_current                       │
│      self._behavior_adapters.append(adapter)                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Inherited by ALL:
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
        ▼                                       ▼
┌──────────────────────┐            ┌──────────────────────┐
│ CursorCommandVisitor │            │   TTYBehaviors        │
│                      │            │   MarkdownBehaviors   │
│ Construction:        │            │   JSONBehaviors        │
│ - Builds hierarchy  │            │                       │
│ - Stores wrappers    │            │ Construction:        │
│                      │            │ - Builds hierarchy    │
│ Serialization:       │            │ - Stores adapters     │
│ - Writes .md files   │            │                       │
│ - Uses same tree     │            │ Serialization:        │
│                      │            │ - Returns strings     │
│                      │            │ - Uses same tree      │
└──────────────────────┘            └──────────────────────┘
```

### Complete Inheritance Structure

```
BaseHierarchicalAdapter (ABC)
├── _build_wrapped_hierarchy() [abstract]
└── serialize() [abstract]

BaseBotAdapter
├── _build_wrapped_hierarchy() → creates _behaviors_adapter
└── serialize() → format_header() + format_bot_info() + _behaviors_adapter.serialize() + format_footer()

BaseBehaviorsAdapter
├── _build_wrapped_hierarchy() → creates _behavior_adapters list
└── serialize() → calls serialize() on each _behavior_adapter

BaseBehaviorAdapter
├── _build_wrapped_hierarchy() → creates _actions_adapter
└── serialize() → format_behavior_name() + (if current) _actions_adapter.serialize()

BaseActionsAdapter
├── _build_wrapped_hierarchy() → creates _action_adapters list
└── serialize() → calls serialize() on each _action_adapter

Channel Adapters (formatting only):
├── TTYAdapter → provides add_bold(), add_color(), etc.
├── MarkdownAdapter → provides format_header(), format_list_item(), etc.
└── JSONAdapter → provides to_dict()

Concrete Implementations:
├── CursorCommandVisitor → BaseBehaviorsAdapter, Visitor
│   └── Overrides serialize() to write files
├── TTYBot → BaseBotAdapter, TTYAdapter
│   └── Implements format_header(), format_bot_info(), format_footer()
├── TTYBehaviors → BaseBehaviorsAdapter, TTYAdapter
│   └── Uses serialize() as-is
├── TTYBehavior → BaseBehaviorAdapter, TTYAdapter
│   └── Implements format_behavior_name()
├── TTYActions → BaseActionsAdapter, TTYAdapter
│   └── Uses serialize() as-is
└── TTYAction → TTYAdapter (leaf, no hierarchy)
    └── Implements serialize() directly
```

### The Key Insight: Shared Traversal Logic

```
┌─────────────────────────────────────────────────────────────┐
│  BaseBehaviorsAdapter._build_wrapped_hierarchy()            │
│                                                             │
│  current_behavior_name = behaviors.current.name             │
│  sorted_behaviors = sorted(behaviors, key=lambda b: b.order)│
│                                                             │
│  for behavior in sorted_behaviors:                          │
│      is_current = behavior.name == current_behavior_name    │
│      adapter = factory.create(behavior, channel)            │
│      adapter._is_current = is_current                       │
│      self._behavior_adapters.append(adapter)                │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Used by BOTH:
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
        ▼                                       ▼
┌──────────────────────┐            ┌──────────────────────┐
│ CursorCommandVisitor │            │   TTYBehaviors       │
│                      │            │                      │
│ Inherits traversal  │            │ Inherits traversal  │
│ Overrides serialize()│            │ Inherits serialize()│
│ to write files       │            │ to return string    │
└──────────────────────┘            └──────────────────────┘
```

### Unified Inheritance Structure

```
BaseHierarchicalAdapter (provides traversal)
├── _build_wrapped_hierarchy() [abstract]
└── serialize() [abstract]

BaseBehaviorsAdapter (implements traversal for Behaviors)
├── _build_wrapped_hierarchy() [concrete - shared logic]
└── serialize() [concrete - walks tree]

    ├── CursorCommandVisitor
    │   ├── Inherits: BaseBehaviorsAdapter (traversal)
    │   ├── Inherits: Visitor (visit methods)
    │   └── Overrides: serialize() to write files
    │
    ├── TTYBehaviors
    │   ├── Inherits: BaseBehaviorsAdapter (traversal)
    │   ├── Inherits: TTYAdapter (formatting helpers)
    │   └── Uses: serialize() as-is (returns string)
    │
    ├── MarkdownBehaviors
    │   ├── Inherits: BaseBehaviorsAdapter (traversal)
    │   ├── Inherits: MarkdownAdapter (formatting helpers)
    │   └── Uses: serialize() as-is (returns string)
    │
    └── JSONBehaviors
        ├── Inherits: BaseBehaviorsAdapter (traversal)
        ├── Inherits: JSONAdapter (formatting helpers)
        └── Overrides: serialize() to return dict/list
```

### What Gets Unified

1. **Traversal Logic**: Single implementation in BaseBehaviorsAdapter._build_wrapped_hierarchy()
2. **Construction-Time Building**: Both patterns build hierarchy in __init__, not during use
3. **Sorting**: Same sorting logic (by behavior.order) for all adapters
4. **Current State**: Same logic to determine is_current for behaviors/actions
5. **Factory Usage**: Both use AdapterFactory to create child adapters

### What Remains Different

1. **Output Format**: 
   - CursorCommandVisitor writes .md files
   - TTYBehaviors returns formatted string
   - JSONBehaviors returns dict/list
2. **Formatting Methods**: Each channel implements its own formatting (format_header, format_behavior_name, etc.)
3. **Purpose**: Visitor generates files, Adapters format display

## Example Commands

### Base Bot Command (crc_bot)

Generated by `CursorCommandVisitor._build_base_command()`:

```markdown
# crc_bot - CLI Status and Navigation

## Status
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'status' | python -m agile_bot.src.cli.cli_main

## Help
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'help' | python -m agile_bot.src.cli.cli_main

## Navigation
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'next' | python -m agile_bot.src.cli.cli_main
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'back' | python -m agile_bot.src.cli.cli_main

## Scope
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'scope all' | python -m agile_bot.src.cli.cli_main
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'scope "${1:story_name}"' | python -m agile_bot.src.cli.cli_main

## Path
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'path ${1:project_path}' | python -m agile_bot.src.cli.cli_main

## Exit
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'exit' | python -m agile_bot.src.cli.cli_main
```

### Behavior Command (crc_bot_walkthrough)

Generated by `CursorCommandVisitor._build_behavior_command()`:

```markdown
# crc_bot_walkthrough - Navigate to Walkthrough Behavior

## Navigate to Behavior
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'walkthrough' | python -m agile_bot.src.cli.cli_main

## Navigate to Specific Action
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'walkthrough.${1|rules|clarify|strategy|build|validate|render|}' | python -m agile_bot.src.cli.cli_main

## Available Actions:

- rules - Load behavior-specific rules into AI context for guidance on writing compliant content
- clarify - Gather context by asking required questions and collecting evidence in order to increase understanding
- strategy - decide approach by capturing assumptions and decision criteria
- build - Build knowledge graph for build
- validate - Validate knowledge graph and/or artifacts against behavior-specific rules, checking for violations and compliance
- render - Render output documents and artifacts from knowledge graph using templates and synchronizers
```

### Action Command (crc_bot_walkthrough_rules)

Generated by `CursorCommandVisitor._build_action_command()`:

```markdown
# crc_bot_walkthrough_rules - Execute Walkthrough Rules Action

Load behavior-specific rules into AI context for guidance on writing compliant content

## Navigate to Action
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'walkthrough.rules' | python -m agile_bot.src.cli.cli_main

## Get Instructions
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'walkthrough.rules.instructions' | python -m agile_bot.src.cli.cli_main

## Submit Work
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'walkthrough.rules.submit${1:+ }${1:--scope "${2:story_name}"}' | python -m agile_bot.src.cli.cli_main

## Confirm and Advance
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'walkthrough.rules.confirm' | python -m agile_bot.src.cli.cli_main
```

### Action Command (crc_bot_walkthrough_build)

Generated by `CursorCommandVisitor._build_action_command()`:

```markdown
# crc_bot_walkthrough_build - Execute Walkthrough Build Action

Build knowledge graph for build

## Navigate to Action
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'walkthrough.build' | python -m agile_bot.src.cli.cli_main

## Get Instructions
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'walkthrough.build.instructions' | python -m agile_bot.src.cli.cli_main

## Submit Work
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'walkthrough.build.submit${1:+ }${1:--scope "${2:story_name}"}' | python -m agile_bot.src.cli.cli_main

## Confirm and Advance
$env:BOT_DIRECTORY = 'C:\dev\augmented-teams\agile_bot\bots\crc_bot'; $env:PYTHONPATH = 'C:\dev\augmented-teams'; echo 'walkthrough.build.confirm' | python -m agile_bot.src.cli.cli_main
```

### Command Generation Flow

1. **CursorCommandVisitor** (inherits BaseBehaviorsAdapter)
   - `_build_wrapped_hierarchy()` traverses `bot.behaviors`
   - Creates `CursorBehaviorWrapper` for each behavior
   - Stores in `_behavior_adapters` list

2. **CursorBehaviorWrapper** (inherits BaseBehaviorAdapter)
   - `_build_wrapped_hierarchy()` traverses `behavior.actions`
   - Creates action adapters (or generates action commands)
   - `serialize()` generates behavior command file

3. **Command File Generation**
   - Base command: `_build_base_command()` → `crc_bot.md`
   - Behavior command: `_build_behavior_command()` → `crc_bot_walkthrough.md`
   - Action commands: `_build_action_command()` → `crc_bot_walkthrough_rules.md`, `crc_bot_walkthrough_build.md`, etc. (one per action)

## Current State

### CursorCommandVisitor (Already Refactored)
- Uses Visitor pattern with Orchestrator
- Generates command files by traversing bot.behaviors → behavior.actions
- No hierarchical adapter pattern yet

### TTY/Markdown/JSON Adapters (Current Pattern)
- Each adapter manually creates child adapters during serialization
- TTYBot creates TTYBehaviors via AdapterFactory in serialize()
- TTYBehaviors creates TTYBehavior adapters in serialize()
- TTYBehavior creates TTYActions in serialize()
- Repeated adapter creation on every serialize() call

### Problem
- Duplicate traversal logic across adapters
- Adapters created repeatedly during serialization
- No shared base for hierarchy traversal
- Visitor pattern and adapter pattern are separate

## Proposed Architecture

### Base Hierarchical Adapter Classes

Create `agile_bot/src/cli/base_hierarchical_adapter.py`:

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from agile_bot.src.cli.adapter_factory import AdapterFactory

class BaseHierarchicalAdapter(ABC):
    def __init__(self, domain_object, channel: str, factory: Optional[AdapterFactory] = None):
        self.domain_object = domain_object
        self.channel = channel
        self.factory = factory or AdapterFactory
        self._build_wrapped_hierarchy()

    @abstractmethod
    def _build_wrapped_hierarchy(self):
        pass

    @abstractmethod
    def serialize(self) -> str:
        pass

class BaseBotAdapter(BaseHierarchicalAdapter):
    def __init__(self, bot, channel: str):
        super().__init__(bot, channel)
        self.bot = bot
        self._behaviors_adapter = None

    def _build_wrapped_hierarchy(self):
        if self.bot.behaviors:
            self._behaviors_adapter = self.factory.create(
                self.bot.behaviors,
                self.channel
            )

    def serialize(self) -> str:
        lines = []
        lines.append(self.format_header())
        lines.append(self.format_bot_info())
        if self._behaviors_adapter:
            lines.append(self._behaviors_adapter.serialize())
        lines.append(self.format_footer())
        return '\n'.join(lines)

    @abstractmethod
    def format_header(self) -> str:
        pass

    @abstractmethod
    def format_bot_info(self) -> str:
        pass

    @abstractmethod
    def format_footer(self) -> str:
        pass

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

class BaseBehaviorAdapter(BaseHierarchicalAdapter):
    def __init__(self, behavior, channel: str, is_current: bool = False):
        super().__init__(behavior, channel)
        self.behavior = behavior
        self.is_current = is_current
        self._actions_adapter = None

    def _build_wrapped_hierarchy(self):
        if self.behavior.actions:
            self._actions_adapter = self.factory.create(
                self.behavior.actions,
                self.channel
            )
            if hasattr(self._actions_adapter, '_set_current_behavior'):
                self._actions_adapter._set_current_behavior(self.behavior)

    def serialize(self) -> str:
        lines = []
        lines.append(self.format_behavior_name())
        if self.is_current and self._actions_adapter:
            actions_output = self._actions_adapter.serialize()
            lines.append(self._indent_actions(actions_output))
        return '\n'.join(lines)

    @abstractmethod
    def format_behavior_name(self) -> str:
        pass

    def _indent_actions(self, actions_output: str) -> str:
        return '\n'.join(f"  {line}" if line else "" for line in actions_output.split('\n'))

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

## Refactoring Steps

### Phase 1: Create Base Classes
1. Create `agile_bot/src/cli/base_hierarchical_adapter.py`
2. Implement BaseHierarchicalAdapter, BaseBotAdapter, BaseBehaviorsAdapter, BaseBehaviorAdapter, BaseActionsAdapter
3. Add tests for base traversal logic

### Phase 2: Refactor TTY Adapters
1. **TTYBot** (`agile_bot/src/bot/tty_bot.py`)
   - Inherit from BaseBotAdapter, TTYAdapter
   - Move traversal logic to base class
   - Keep formatting methods (format_header, format_bot_info, format_footer)
   - Remove manual AdapterFactory.create() calls from serialize()

2. **TTYBehaviors** (`agile_bot/src/behaviors/tty_behavior.py`)
   - Inherit from BaseBehaviorsAdapter, TTYAdapter
   - Remove all traversal logic (handled by base)
   - Keep names property if needed for summary

3. **TTYBehavior** (`agile_bot/src/behaviors/tty_behavior.py`)
   - Inherit from BaseBehaviorAdapter, TTYAdapter
   - Implement format_behavior_name()
   - Remove manual TTYActions creation

4. **TTYActions** (`agile_bot/src/actions/tty_actions.py`)
   - Inherit from BaseActionsAdapter, TTYAdapter
   - Remove traversal logic
   - Keep names property if needed

5. **TTYAction** (`agile_bot/src/actions/tty_action.py`)
   - No change (leaf node, no hierarchy)

### Phase 3: Refactor Markdown Adapters
1. **MarkdownBot** (`agile_bot/src/bot/markdown_bot.py`)
   - Inherit from BaseBotAdapter, MarkdownAdapter
   - Implement format_header, format_bot_info, format_footer

2. **MarkdownBehaviors** (`agile_bot/src/behaviors/markdown_behavior.py`)
   - Inherit from BaseBehaviorsAdapter, MarkdownAdapter

3. **MarkdownBehavior** (`agile_bot/src/behaviors/markdown_behavior.py`)
   - Inherit from BaseBehaviorAdapter, MarkdownAdapter
   - Implement format_behavior_name()

4. **MarkdownActions** (`agile_bot/src/actions/markdown_actions.py`)
   - Inherit from BaseActionsAdapter, MarkdownAdapter

### Phase 4: Refactor JSON Adapters
1. **JSONBot** (`agile_bot/src/bot/json_bot.py`)
   - Inherit from BaseBotAdapter, JSONAdapter
   - Implement format_header, format_bot_info, format_footer
   - Override serialize() to build JSON structure instead of lines

2. **JSONBehaviors** (`agile_bot/src/behaviors/json_behavior.py`)
   - Inherit from BaseBehaviorsAdapter, JSONAdapter
   - Override serialize() to return list/dict instead of lines

3. **JSONBehavior** (`agile_bot/src/behaviors/json_behavior.py`)
   - Inherit from BaseBehaviorAdapter, JSONAdapter
   - Override serialize() for JSON structure

4. **JSONActions** (`agile_bot/src/actions/json_actions.py`)
   - Inherit from BaseActionsAdapter, JSONAdapter
   - Override serialize() for JSON structure

### Phase 5: Refactor CursorCommandVisitor
1. **CursorCommandVisitor** (`agile_bot/src/cli/cursor/cursor_command_visitor.py`)
   - Inherit from BaseBehaviorsAdapter, Visitor
   - Override _build_wrapped_hierarchy() to create CursorBehaviorWrapper instead of generic adapters
   - Move generate() logic into serialize()
   - Remove Orchestrator dependency (traversal handled by base)

2. **CursorBehaviorWrapper** (new or existing)
   - Inherit from BaseBehaviorAdapter
   - Implement format_behavior_name() to generate command file
   - Override serialize() to write files instead of returning string

### Phase 6: Update AdapterFactory
1. Ensure factory can create adapters with is_current parameter
2. Update registry if needed for new inheritance patterns
3. Test factory creates correct adapter types

### Phase 7: Handle Non-Hierarchical Adapters
Some adapters don't have hierarchy (Scope, Help, ExitResult, etc.):
- Keep existing pattern (no BaseHierarchicalAdapter)
- Only Bot → Behaviors → Behavior → Actions use hierarchical pattern

## Benefits

1. **Single traversal logic**: All hierarchical adapters use same base classes
2. **Construction-time wrapping**: Adapters created once, not repeatedly
3. **Consistent ordering**: All adapters sort behaviors/actions the same way
4. **Easier to extend**: New channels inherit traversal automatically
5. **Performance**: No repeated adapter creation during serialization
6. **Unified pattern**: Visitor and adapter patterns share same traversal

## Testing Strategy

1. **Unit tests** for base classes:
   - Traversal builds correct hierarchy
   - serialize() walks hierarchy correctly
   - Sorting works as expected

2. **Integration tests** for each channel:
   - TTY output matches current output
   - Markdown output matches current output
   - JSON output matches current output
   - Cursor commands generated correctly

3. **Regression tests**:
   - All existing adapter tests pass
   - CLI output unchanged
   - Command generation unchanged

## Migration Notes

- Adapters can be refactored incrementally (one channel at a time)
- Keep old code until new code tested
- Update tests as adapters are refactored
- Non-hierarchical adapters remain unchanged

## Files to Modify

### New Files
- `agile_bot/src/cli/base_hierarchical_adapter.py`

### Modified Files
- `agile_bot/src/bot/tty_bot.py`
- `agile_bot/src/bot/markdown_bot.py`
- `agile_bot/src/bot/json_bot.py`
- `agile_bot/src/behaviors/tty_behavior.py`
- `agile_bot/src/behaviors/markdown_behavior.py`
- `agile_bot/src/behaviors/json_behavior.py`
- `agile_bot/src/actions/tty_actions.py`
- `agile_bot/src/actions/markdown_actions.py`
- `agile_bot/src/actions/json_actions.py`
- `agile_bot/src/cli/cursor/cursor_command_visitor.py`
- `agile_bot/src/cli/adapter_factory.py` (if needed)

### Unchanged Files
- All non-hierarchical adapters (Scope, Help, ExitResult, etc.)
- Leaf adapters (TTYAction, JSONAction, etc.)

## Implementation Order

1. Create base classes and tests
2. Refactor TTY adapters (most used, easiest to test)
3. Refactor Markdown adapters
4. Refactor JSON adapters (may need custom serialize() overrides)
5. Refactor CursorCommandVisitor
6. Update factory and registry
7. Remove old traversal code
8. Update documentation
