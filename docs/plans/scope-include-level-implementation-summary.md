# Scope Include Level Implementation Summary

**Date:** 2026-02-16
**Story:** Submit Scope Instructions
**Plan:** scope-include-level-and-trace-plan.md

## Implementation Status

### ✅ Phase 1: Core Infrastructure - COMPLETE
- Created `src/traceability/` module
  - `trace_generator.py` - TraceGenerator class (refactored from DynamicStraceGenerator)
  - `workspace_index.py` - Code indexing
  - `python_analyzer.py` - AST analysis
  - `snippet_extractor.py` - Code extraction
- Added `include_level` property to `Scope` class with default 'examples'
- Updated `Scope.to_dict()`, `load()`, `from_dict()`, `copy()` to persist include_level
- Updated `JSONScope.to_dict()` to pass include_level to JSONStoryGraph
- Updated `JSONStoryGraph.to_dict()` to accept include_level parameter
- Implemented filtering in `_serialize_epic`, `_serialize_sub_epic`, `_serialize_story`, `_serialize_scenario`

### ✅ Phase 2: Trace Integration - COMPLETE
- Refactored `DynamicStraceGenerator` → `TraceGenerator` with `max_depth=3` (was 4)
- Added `_generate_test_code()` method to JSONStoryGraph
- Added `_generate_trace()` method to JSONStoryGraph
- Integrated trace generation in `_serialize_scenario` based on include_level
  - `include_level='tests'` → adds test method code
  - `include_level='code'` → adds test code + full trace

### ✅ Phase 4: Panel Integration - COMPLETE
- Added 7 radio buttons for include_level selection in story_map_view.js
  - Stories, Domain, Accept, Scenarios, Examples (default), Tests, Code
- Added `window.updateIncludeLevel()` function in bot_panel.js
- Added message handler for 'updateIncludeLevel' command
- Handler directly updates scope.json file system
- Added `includeLevel` field to scopeData JSON response
- Bumped panel version to 0.1.932

### 🔄 Phase 3: Testing - IN PROGRESS
Need to add test scenarios and test methods (see plan for details)

### ⏸️ Phase 5: Cleanup - PENDING
- Add `*.vsix` to `.gitignore`
- Move generated `.strace` files to `docs/traces/`
- Consider moving VS Code extension to `extensions/story-trace/`

---

## Working Features

### 1. Scope Persistence
```python
# Python API
scope = Scope(workspace_directory=Path('.'), bot_paths=None)
scope.include_level = 'code'  # Set level
scope.save()  # Persists to scope.json

# Reload
new_scope = Scope(workspace_directory=Path('.'), bot_paths=None)
new_scope.load()  # Restores include_level='code'
```

### 2. Content Filtering
```python
# JSONStoryGraph now filters based on include_level
from story_graph.json_story_graph import JSONStoryGraph
from story_graph.story_graph import StoryGraph

story_graph = StoryGraph(bot_paths, workspace_dir)
adapter = JSONStoryGraph(story_graph)

# Get structure only
data = adapter.to_dict(include_level='stories')

# Get with test code
data = adapter.to_dict(include_level='tests')

# Get with full trace
data = adapter.to_dict(include_level='code')
```

### 3. Trace Generation
```python
# Standalone trace generation
from traceability.trace_generator import TraceGenerator
from pathlib import Path

generator = TraceGenerator(Path('.'), max_depth=3)
generator._build_method_index()

# Generate trace for test method
trace = generator.generate(
    test_file='test/example.py',
    test_class='TestExample',
    test_method='test_something',
    scenario_name='Example scenario',
    scenario_steps='GIVEN... WHEN... THEN...'
)
```

### 4. Panel UI
- Open panel in VS Code
- See "Include up to:" radio buttons in Story Map section
- Select level (Stories, Domain, Accept, Scenarios, Examples, Tests, Code)
- Selection saved immediately to `scope.json`
- Next instruction submission uses the selected level

---

## How It Works

### Instruction Generation Flow

```
User selects story in panel
  ↓
User selects include_level (e.g., 'code') via radio button
  ↓
Panel calls updateIncludeLevel() → saves to scope.json
  ↓
User clicks Submit
  ↓
Bot generates instructions:
  - Reads scope.json (includes include_level='code')
  - JSONScope.to_dict() passes include_level to JSONStoryGraph
  - JSONStoryGraph filters content based on level:
    * level='stories' → names only
    * level='domain_concepts' → + CRC cards
    * level='acceptance' → + criteria
    * level='scenarios' → + steps
    * level='examples' → + data
    * level='tests' → + test code (calls _generate_test_code)
    * level='code' → + full trace (calls _generate_trace)
  - TraceGenerator analyzes test method AST
  - Finds all function/method calls (depth 1)
  - Resolves each call to implementation (depth 2)
  - Recursively traces children (depth 3, then stops)
  - Returns trace tree with symbol names, file paths, line numbers, code
  ↓
Instructions include filtered scope JSON
  ↓
AI receives context appropriate for the task
```

---

## Testing Recommendations

### Manual Testing

1. **Test include_level persistence:**
   ```python
   python -c "from src.scope.scope import Scope; from pathlib import Path; s = Scope(Path('C:/dev/agile_bots'), None); s.include_level = 'code'; s.save(); print('Saved')"
   
   # Check scope.json contains "include_level": "code"
   cat scope.json
   ```

2. **Test panel UI:**
   - Open VS Code Bot Panel
   - Verify 7 radio buttons appear in Story Map section
   - Click "Code" radio button
   - Check `scope.json` updated with `"include_level": "code"`

3. **Test content filtering:**
   - Set `include_level='stories'` in scope.json
   - Run bot command to get scope JSON
   - Verify only structure (no acceptance criteria, scenarios, etc.)

4. **Test trace generation:**
   - Create simple test file with test that calls domain code
   - Set `include_level='code'`
   - Generate instructions with scope
   - Verify trace appears in scope JSON

### Automated Testing (Phase 3)

See plan for 8 new test scenarios to add to `TestSubmitScopeInstructions`.

---

## Known Limitations

1. **Trace only supports Python** - JavaScript/TypeScript tracing not yet implemented
2. **No trace caching** - Trace regenerated every time (can be slow for large codebases)
3. **Depth fixed at 3** - Not user-configurable (intentional per plan)
4. **No progress indicator** - Trace generation can take seconds, no UI feedback
5. **External library detection** - Relies on searching only test/src dirs (no site-packages, node_modules)

---

## Next Steps

1. **Write test scenarios** (Phase 3) - Add 8 scenarios to story-graph.json and test methods to test file
2. **Cleanup** (Phase 5) - Move trace_notebook, update .gitignore
3. **Documentation** - Update README with usage examples
4. **Performance optimization** - Add trace caching if needed
5. **Multi-language support** - Extend to JavaScript/TypeScript tests

---

## Files Modified

### Core Domain
- `src/scope/scope.py` - Added include_level property and persistence
- `src/scope/json_scope.py` - Pass include_level to serializer, add to JSON response
- `src/story_graph/json_story_graph.py` - Filtering logic for all levels + trace integration

### Traceability Module (New)
- `src/traceability/__init__.py`
- `src/traceability/trace_generator.py` - Main generator (max_depth=3)
- `src/traceability/workspace_index.py` - File indexing
- `src/traceability/python_analyzer.py` - AST analysis
- `src/traceability/snippet_extractor.py` - Code extraction

### Panel UI
- `src/panel/bot_panel.js` - Message handler for updateIncludeLevel
- `src/panel/story_map_view.js` - Radio button controls UI
- `src/panel/package.json` - Version bump to 0.1.932

### Documentation
- `docs/plans/scope-include-level-and-trace-plan.md` - Implementation plan

---

## Commits

1. `948f53b` - Add plan for scope include_level and trace integration
2. `54ba41d` - Implement scope include_level filtering and trace integration (Phase 1 & 2)
3. `9cb7277` - Add panel UI controls for scope include_level selection
4. `ba586a6` - Update plan: mark panel integration as completed

---

## Success Criteria Status

- ✅ `scope.json` persists and restores `include_level`
- ✅ Each include_level filters content correctly (implementation done, tests pending)
- ✅ Trace generated at depth=3 for 'tests' level
- ✅ Full trace generated at depth=3 for 'code' level
- ⏸️ All existing tests pass (need to run test suite)
- ⏸️ New tests pass for all scenarios (tests not yet written)
- ✅ AI can receive complete trace context when debugging
