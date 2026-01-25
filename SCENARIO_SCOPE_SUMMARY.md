# Scenario-Level Scope Submission - Implementation Summary

## Overview
Extended scope submission functionality to work with **Scenario** nodes (in addition to Epic, SubEpic, and Story nodes).

## Changes Made

### 1. Backend Logic (`src/story_graph/nodes.py`)
- ✅ Added `behavior_needed` property to `Scenario` class
  - Returns `"code"` if scenario has a `test_method` (ready for implementation)
  - Returns `"test"` if scenario has no `test_method` (needs test)
- Note: `ScenarioOutline` has been merged into `Scenario` (scenarios can now optionally have an `examples` field for data-driven testing)

### 2. Panel JSON Enrichment (`src/scope/json_scope.py`)
- ✅ Updated `_enrich_scenario_with_links()` to add `behavior` field to scenarios
- ✅ This ensures the behavior information is available to the panel
- The behavior is calculated using the same logic as the backend: `'code'` if `test_method` exists, otherwise `'test'`

### 3. Tests (`test/invoke_bot/edit_story_map/test_manage_story_scope.py`)
- ✅ Added `TestDetermineBehaviorForScenario` class with parameterized tests
- ✅ Tests verify scenarios correctly determine their behavior:
  - Scenario with test method → returns `"code"`
  - Scenario without test method → returns `"test"`
  - Scenario with empty string test method → returns `"test"`

## Behavior Hierarchy (Complete)

```
Epic
  └─> SubEpic
       └─> Story
            ├─> code: All scenarios have tests
            ├─> test: Has scenarios (some/no tests)
            ├─> scenario: Has acceptance criteria but no scenarios
            └─> explore: No acceptance criteria
            
            └─> Scenario ✨ NEW! ✨
                 ├─> code: Has test method
                 └─> test: No test method
```

## Panel Support

### What Works Automatically ✅
- **Generic click handlers**: Panel already handles `data-node-type` and `data-behavior` attributes generically
- **Behavior enrichment**: Scenarios now have their `behavior` property in the JSON response
- **Submit logic**: Backend scope submission works for any node type

### What May Need Updates ⚠️
If scenarios are not currently displayed as clickable nodes in the panel's story graph tree view, you'll need to:
1. Update the HTML generation to render scenarios as selectable nodes
2. Add the appropriate `data-node-type="Scenario"` and `data-behavior="code|test"` attributes

## Testing

Run the scenario behavior tests:
```bash
python -m pytest test/invoke_bot/edit_story_map/test_manage_story_scope.py::TestDetermineBehaviorForScenario -v
```

Verify with direct Python:
```bash
python -c "from story_graph.nodes import Scenario; s1 = Scenario('test', 1.0, test_method='test_foo'); print(f'With test: {s1.behavior_needed}'); s2 = Scenario('test2', 2.0, test_method=None); print(f'Without test: {s2.behavior_needed}')"
```

Expected output:
```
With test: code
Without test: test
```

## Files Modified

1. `src/story_graph/nodes.py` - Added `behavior_needed` property to Scenario
2. `src/scope/json_scope.py` - Added behavior enrichment for scenarios
3. `test/invoke_bot/edit_story_map/test_manage_story_scope.py` - Added scenario behavior tests

## Next Steps

1. **Test in the panel**: Open the panel and check if scenarios are displayed as clickable nodes
2. **If scenarios aren't visible**: Update panel HTML generation to render scenarios with proper attributes
3. **Test scope submission**: Try clicking on a scenario and using the submit button
4. **Verify behavior indicators**: Check that scenarios show the correct behavior icon (code vs test)
