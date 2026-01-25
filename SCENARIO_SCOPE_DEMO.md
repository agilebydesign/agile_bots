# Scenario-Level Scope Submission Feature

## Overview

The scope submission functionality has been extended to work with **Scenario** nodes in addition to Epic, SubEpic, and Story nodes. This allows you to determine the behavior needed at the scenario level based on whether it has a test method or not.

## Implementation

### Changes Made

1. **Added `behavior_needed` property to `Scenario` class** (`src/story_graph/nodes.py`)
   - Returns `"code"` if the scenario has a test method (ready for implementation)
   - Returns `"test"` if the scenario has no test method (needs test)
   - Note: ScenarioOutline has been merged into Scenario (scenarios can now optionally have an `examples` field)

2. **Added behavior enrichment to JSON scope** (`src/scope/json_scope.py`)
   - Scenarios now include their `behavior` property in the JSON sent to the panel
   - This allows the panel to display the correct behavior indicator

3. **Added tests** (`test/invoke_bot/edit_story_map/test_manage_story_scope.py`)
   - Tests verify that scenarios correctly determine their behavior based on test method presence

## Behavior Hierarchy

The complete hierarchy from top to bottom is now:

```
Epic
  └─> SubEpic
       └─> Story
            ├─> code: All scenarios have tests
            ├─> test: Has scenarios (some/no tests)
            ├─> scenario: Has acceptance criteria but no scenarios
            └─> explore: No acceptance criteria
            
            └─> Scenario (NEW!)
                 ├─> code: Has test method
                 └─> test: No test method
```

## Usage Example

```python
from story_graph.nodes import Scenario

# Scenario with test method -> ready for code implementation
scenario1 = Scenario(
    name="User uploads valid file",
    sequential_order=1.0,
    test_method="test_user_uploads_valid_file"
)
print(scenario1.behavior_needed)  # Output: "code"

# Scenario without test method -> needs test
scenario2 = Scenario(
    name="User downloads file",
    sequential_order=2.0,
    test_method=None
)
print(scenario2.behavior_needed)  # Output: "test"
```

## How It Works

When you submit scope for a scenario:

1. The system checks if the scenario has a `test_method` property set
2. If `test_method` exists and is not empty:
   - Returns `"code"` behavior (scenario is ready for code implementation)
3. If `test_method` is None or empty:
   - Returns `"test"` behavior (scenario needs a test to be written)

This follows the same pattern as Story and SubEpic nodes, maintaining consistency throughout the hierarchy.

## Testing

Tests have been added to verify the functionality:

```bash
# Run the scenario behavior tests
python -m pytest test/invoke_bot/edit_story_map/test_manage_story_scope.py::TestDetermineBehaviorForScenario -v
```

All tests pass successfully:
- ✅ Scenario with test method → returns "code"
- ✅ Scenario without test method → returns "test"
- ✅ Scenario with empty string test method → returns "test"

## Benefits

- **Consistent API**: Scenarios now follow the same pattern as other node types
- **Fine-grained control**: You can now submit scope at the scenario level
- **Clear behavior determination**: Easy to understand what work needs to be done for each scenario
- **Test-driven workflow**: Supports a test-first approach where you can identify which scenarios need tests vs implementation
