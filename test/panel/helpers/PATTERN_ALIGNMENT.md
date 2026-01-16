# JavaScript Helper Pattern Alignment with Python

## Pattern Consistency

JavaScript panel helpers now match Python CLI/domain helper naming conventions.

## Naming Patterns

### Python Helpers (Reference)
```python
# agile_bot/test/domain/helpers/behavior_helper.py
class BehaviorTestHelper(BaseHelper):
    def create_behavior_json(self, behavior_name, actions):
        """Create behavior.json file"""
    
    def assert_behavior_exists(self, behavior_name):
        """Assert behavior exists in bot"""

# agile_bot/test/domain/helpers/validate_helper.py
class ValidateTestHelper(BaseHelper):
    def create_validation_rules(self, behavior, rules):
        """Create validation rules file"""
    
    def assert_validate_instructions(self, instructions):
        """Assert validate instructions complete"""
    
    def scan_with_rule(self, rule, knowledge_graph):
        """Scan using rule"""
```

### JavaScript Helpers (Aligned)
```javascript
// agile_bot/test/panel/helpers/behaviors_view_test_helper.js
class BehaviorsViewTestHelper {
    create_behavior_with_actions(behaviorName, actionNames) {
        // Create behavior data structure
    }
    
    create_behaviors(behaviors) {
        // Create multiple behaviors
    }
    
    render_html(behaviorsData) {
        // Render view to HTML
    }
    
    assert_behavior_with_actions(html, behaviorName, actionNames) {
        // Assert behavior and actions present
    }
    
    assert_current_behavior_marked(html, behaviorName) {
        // Assert current behavior marked
    }
}

// agile_bot/test/panel/helpers/scope_view_test_helper.js
class ScopeViewTestHelper {
    create_story_scope(storyNames) {
        // Create story scope data
    }
    
    create_epic_scope(epicNames) {
        // Create epic scope data
    }
    
    render_html(scopeData) {
        // Render view to HTML
    }
    
    assert_scope_type(html, scopeType) {
        // Assert scope type displayed
    }
    
    assert_story_scope(html, storyNames) {
        // Assert story scope displayed
    }
}

// agile_bot/test/panel/helpers/instructions_view_test_helper.js
class InstructionsViewTestHelper {
    create_base_instructions(instructionLines) {
        // Create base instructions
    }
    
    create_validate_instructions(instructionLines, rules) {
        // Create validate instructions
    }
    
    render_html(instructionsData) {
        // Render view to HTML
    }
    
    assert_instructions_displayed(html, expectedLines) {
        // Assert instructions content
    }
    
    assert_submit_button_present(html) {
        // Assert submit button exists
    }
}
```

## Method Name Patterns

| Purpose | Python Pattern | JavaScript Pattern | Example |
|---------|----------------|-------------------|---------|
| **Create test data** | `create_*` | `create_*` | `create_behavior_json()` / `create_behavior_with_actions()` |
| **Execute action** | Direct verb | Direct verb | `scan_with_rule()` / `render_html()` |
| **Assert result** | `assert_*` | `assert_*` | `assert_validate_instructions()` / `assert_behavior_with_actions()` |
| **Factory helper** | `create_*` | `create_*` | `create_validation_rules()` / `create_story_scope()` |

## Before (BDD Style - REJECTED)
```javascript
// ❌ NOT aligned with Python patterns
givenSingleBehaviorWithActions()  // BDD-style "given"
whenViewRendersHTML()              // BDD-style "when"
thenHTMLContainsBehavior()         // BDD-style "then"
```

## After (Python-Aligned - CORRECT)
```javascript
// ✅ Aligned with Python patterns
create_behavior_with_actions()     // Matches Python create_*
render_html()                      // Direct action method
assert_behavior_with_actions()     // Matches Python assert_*
```

## Benefits of Alignment

1. **Consistency Across Languages**
   - JavaScript and Python helpers use same naming patterns
   - Reduces cognitive load when switching between test suites
   - Easier to understand for developers familiar with either

2. **Mirrors Proven Patterns**
   - Python CLI tests are successful and well-structured
   - JavaScript tests inherit same organizational principles
   - Reuses established best practices

3. **Clear Method Purpose**
   - `create_*` = Setup/factory methods
   - `assert_*` = Verification methods
   - Direct verbs = Action methods
   - No ambiguity about method role

## Example Test Structure

```javascript
class TestDisplayBehaviorHierarchy {
    constructor(workspaceDir) {
        this.helper = new BehaviorsViewTestHelper(workspaceDir, 'story_bot');
    }
    
    async testSingleBehaviorWithFiveActions() {
        /**
         * GIVEN: Bot at shape behavior with five actions
         * WHEN: Panel renders hierarchy
         * THEN: HTML shows behavior with all five actions
         */
        // Setup - create_* methods
        const behaviorData = this.helper.create_behavior_with_actions(
            'shape',
            ['clarify', 'strategy', 'validate', 'build', 'render']
        );
        
        // Action - direct verb methods
        const html = this.helper.render_html([behaviorData]);
        
        // Assert - assert_* methods
        this.helper.assert_behavior_with_actions(
            html,
            'shape',
            ['clarify', 'strategy', 'validate', 'build', 'render']
        );
    }
}
```

## Notes

- Scenario blocks in tests still use GIVEN/WHEN/THEN for documentation
- Method names use Python-aligned patterns (create_*, assert_*)
- This separates test documentation from implementation
- Best of both worlds: readable scenarios + consistent code
