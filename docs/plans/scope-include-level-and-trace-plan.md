# Scope Include Level and Trace Integration Plan

**Date:** 2026-02-16
**Goal:** Add granular control over scope content depth with integrated traceability from Stories → Tests → Code

## Background

Currently, when submitting instructions with scope, the system includes the full story graph up to examples level. This creates large context that isn't always needed. Additionally, we have a trace prototype (`src/trace_notebook/`) that traces from Epics → Stories → Scenarios → Tests → Code, but it's not integrated with the instruction generation flow.

This plan integrates both features:
1. **Include Level Control**: Add `include_level` property to scope for filtering content depth
2. **Trace Integration**: Move trace prototype to `src/traceability/` and integrate with scope serialization

## Current Instruction Format with Scope

When scope is set and instructions are generated, the format looks like this:

```markdown
## Scope

**Story Scope:** Submit Scope Instructions

Please only work on the following scope.

Scope Filter: "Submit Scope Instructions"

Scope:

{
  "path": "C:\\dev\\agile_bots\\docs\\story\\story-graph.json",
  "has_epics": true,
  "has_increments": false,
  "has_domain_concepts": true,
  "epic_count": 1,
  "content": {
    "epics": [
      {
        "name": "Invoke Bot",
        "behavior_needed": "code",
        "domain_concepts": [],
        "sub_epics": [
          {
            "name": "Perform Action",
            "sub_epics": [
              {
                "name": "Prepare Common Instructions For Behavior, Action, and Scope",
                "test_file": "invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py",
                "story_groups": [
                  {
                    "stories": [
                      {
                        "name": "Submit Scope Instructions",
                        "test_class": "TestSubmitScopeInstructions",
                        "acceptance_criteria": [],
                        "scenarios": [
                          {
                            "name": "Scope appears in instructions display_content markdown",
                            "test_method": "test_scope_appears_in_instructions_display_content",
                            "type": "happy_path",
                            "steps": [...]
                          }
                        ]
                      }
                    ]
                  }
                ],
                "domain_concepts": [...]
              }
            ]
          }
        ]
      }
    ]
  }
}

---

# Behavior: code

## Behavior Instructions - code

The purpose of this behavior is to generate production source code...

## Action Instructions - rules

The purpose of this action is to load behavior-specific rules...

---

**Look for context in the following locations:**
- in this message and chat history
- `C:/dev/agile_bots/docs/story/story-graph.json` - the story graph
- `C:/dev/agile_bots/docs/story/strategy.json` - strategy decisions
- `C:/dev/agile_bots/docs/story/clarification.json` - clarification answers
- `C:/dev/agile_bots/test/` and `C:/dev/agile_bots/src/` - existing code
- any folder named `context/` - additional context files

### Key Questions
[Behavior-specific questions]

### Evidence
[Behavior-specific evidence]

### Decisions
[User's decisions]

### Assumptions
[User's assumptions]
```

**Key Observations:**
1. Scope section appears FIRST before behavior instructions
2. Full story graph hierarchy included (epic → sub-epic → story → scenarios)
3. All fields included: acceptance_criteria, scenarios, steps, examples, domain_concepts
4. No filtering currently - everything is sent
5. Format is markdown with JSON embedded in code block
6. Each behavior (scenarios, tests, code) has its own rules/questions/evidence sections

**Problem:** This creates massive context when:
- Multiple stories in scope
- Deep nesting with many sub-epics
- Rich domain_concepts with realizations
- Many scenarios with detailed steps

**Solution:** Add `include_level` to filter what's included in the `content.epics[].sub_epics[].stories[]` structure.

## Use Case

**Primary:** When debugging a story, quickly generate full trace context for AI assistance
- User sets `include_level='code'` in panel via radio buttons
- Submits instructions with scope
- AI receives complete trace from Story → Scenario → Test → Implementation code

**Secondary:** Reduce context size for simple queries
- User sets `include_level='stories'` for structural questions
- User sets `include_level='scenarios'` for understanding behavior

---

## Include Levels

### Level Hierarchy (Cumulative)

1. **stories** - Structure only (epic/sub-epic/story names)
2. **acceptance** - + Acceptance criteria text
3. **scenarios** - + Scenario names and steps
4. **examples** - + Example data tables (CURRENT DEFAULT)
5. **tests** - + Test method code (depth=3, test infrastructure only)
6. **code** - + Full implementation trace (depth=3, includes domain code)

### Trace Depth Strategy

**Tests Level (depth=3):**
```
Test Method
  └─ Test Helper (level 1)
      └─ Test Fixture (level 2)
          └─ Test Util (level 3) [STOP]
```
- Only traces within `test/` directory
- Shows test infrastructure without implementation

**Code Level (depth=3):**
```
Test Method
  └─ DomainClass.__init__ (level 1)
      └─ DomainMethod.execute() (level 2)
          └─ HelperClass.process() (level 3) [STOP]
```
- Traces into `src/` directory
- Stops before external libraries (naturally excluded by searching only workspace code)

---

## Story Changes

**Story:** Submit Scope Instructions  
**Location:** `docs/story/story-graph.json` line ~15996  
**Sub-epic:** Prepare Common Instructions For Behavior, Action, and Scope  
**Test Class:** `TestSubmitScopeInstructions`

### New Scenarios to Add

1. **Scope with include_level persists in scope.json**
   - GIVEN: User sets include_level to 'code'
   - WHEN: Scope is saved
   - THEN: include_level='code' persisted to scope.json
   - AND: Reloading scope restores include_level='code'

2. **Scope with include_level='stories' filters to structure**
   - GIVEN: Story graph with acceptance criteria, scenarios, examples
   - WHEN: include_level='stories' and instructions retrieved
   - THEN: Scope content contains only epic/sub-epic/story names
   - AND: No acceptance criteria, scenarios, examples, tests, or code

3. **Scope with include_level='acceptance' includes criteria**
   - GIVEN: Story graph with acceptance criteria
   - WHEN: include_level='acceptance'
   - THEN: Scope includes structure + acceptance criteria
   - AND: No scenarios, examples, tests, or code

4. **Scope with include_level='scenarios' includes steps**
   - GIVEN: Story graph with scenarios
   - WHEN: include_level='scenarios'
   - THEN: Scope includes structure + criteria + scenario steps
   - AND: No examples, tests, or code

5. **Scope with include_level='examples' includes data (default)**
   - GIVEN: Story graph with example tables
   - WHEN: include_level='examples' (default)
   - THEN: Scope includes structure + criteria + scenarios + examples
   - AND: No tests or code (current behavior maintained)

6. **Scope with include_level='tests' includes test code**
   - GIVEN: Story with test_file, test_class, test_method
   - AND: Test file exists with actual test code
   - WHEN: include_level='tests'
   - THEN: Scope includes test method code
   - AND: Trace depth limited to 3 levels
   - AND: Only traces test infrastructure (test/ directory)

7. **Scope with include_level='code' includes full trace**
   - GIVEN: Story with test that calls domain code
   - AND: Domain code exists in src/ directory
   - WHEN: include_level='code'
   - THEN: Scope includes full trace to implementation
   - AND: Trace depth limited to 3 levels
   - AND: Traces into src/ directory (domain code)

---

## Test Changes

**Test File:** `test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.py`  
**Test Class:** `TestSubmitScopeInstructions` (starting line ~298)

### Existing Tests (Keep)
- ✓ `test_scope_appears_in_instructions_display_content` 
- ✓ `test_domain_concepts_serialized_in_json_story_graph`

### New Tests to Add

```python
class TestSubmitScopeInstructions:
    """Story: Submit Scope Instructions"""
    
    # ... existing tests ...
    
    def test_include_level_persisted_in_scope_json(self, tmp_path):
        """
        SCENARIO: Scope with include_level persists in scope.json
        GIVEN: User sets include_level to 'code'
        WHEN: Scope is saved
        THEN: include_level='code' persisted to scope.json
        AND: Reloading scope restores include_level='code'
        """
        helper = BotTestHelper(tmp_path)
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        
        # Set include_level
        scope.include_level = 'code'
        scope.save()
        
        # Verify persisted
        scope_file = helper.workspace / 'scope.json'
        scope_data = json.loads(scope_file.read_text())
        assert scope_data['include_level'] == 'code'
        
        # Verify restored
        new_scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        new_scope.load()
        assert new_scope.include_level == 'code'
    
    def test_scope_with_include_level_stories_only(self, tmp_path):
        """
        SCENARIO: Scope with include_level='stories' filters to structure
        GIVEN: Story graph with acceptance criteria, scenarios, examples
        WHEN: include_level='stories' and instructions retrieved
        THEN: Scope content contains only epic/sub-epic/story names
        AND: No acceptance criteria, scenarios, examples, tests, or code
        """
        helper = BotTestHelper(tmp_path)
        
        # Create full story graph
        story_graph = helper.story.given_story_graph_dict(
            epic='TestEpic',
            sub_epic='TestSubEpic',
            story='TestStory',
            acceptance_criteria=['Criteria 1', 'Criteria 2'],
            scenarios=[{
                'name': 'Happy path',
                'steps': 'Given... When... Then...',
                'examples': [{'input': 'test'}]
            }]
        )
        helper.files.given_file_created(
            helper.workspace / 'docs' / 'story',
            'story-graph.json',
            story_graph
        )
        
        # Set scope with include_level='stories'
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.STORY, value=['TestStory'])
        scope.include_level = 'stories'
        scope.apply_to_bot()
        
        # Get instructions
        helper.bot.behaviors.navigate_to('shape')
        action = helper.bot.behaviors.current.actions.find_by_name('build')
        context = ScopeActionContext(scope=scope)
        instructions = action.get_instructions(context)
        
        # Verify only structure included
        content = instructions.display_content
        assert 'TestEpic' in '\n'.join(content)
        assert 'TestSubEpic' in '\n'.join(content)
        assert 'TestStory' in '\n'.join(content)
        
        # Verify filtered out
        assert 'Criteria 1' not in '\n'.join(content)
        assert 'Happy path' not in '\n'.join(content)
        assert 'Given... When... Then...' not in '\n'.join(content)
    
    def test_scope_with_include_level_tests(self, tmp_path):
        """
        SCENARIO: Scope with include_level='tests' includes test code
        GIVEN: Story with test_file, test_class, test_method
        AND: Test file exists with actual test code
        WHEN: include_level='tests'
        THEN: Scope includes test method code
        AND: Trace depth limited to 3 levels
        AND: Only traces test infrastructure (test/ directory)
        """
        helper = BotTestHelper(tmp_path)
        
        # Create test file
        test_code = '''
import pytest

class TestStory:
    def test_scenario(self, helper):
        """Test scenario implementation"""
        result = helper.execute_test()
        assert result.success
        
class TestHelper:
    def execute_test(self):
        return TestResult(success=True)
'''
        test_file = helper.workspace / 'test' / 'test_story.py'
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text(test_code)
        
        # Create story graph with test links
        story_graph = helper.story.given_story_graph_dict(
            epic='TestEpic',
            sub_epic='TestSubEpic',
            story='TestStory',
            test_file='test/test_story.py',
            test_class='TestStory',
            scenarios=[{
                'name': 'Test scenario',
                'test_method': 'test_scenario'
            }]
        )
        helper.files.given_file_created(
            helper.workspace / 'docs' / 'story',
            'story-graph.json',
            story_graph
        )
        
        # Set scope with include_level='tests'
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.STORY, value=['TestStory'])
        scope.include_level = 'tests'
        scope.apply_to_bot()
        
        # Get instructions
        helper.bot.behaviors.navigate_to('shape')
        action = helper.bot.behaviors.current.actions.find_by_name('build')
        context = ScopeActionContext(scope=scope)
        instructions = action.get_instructions(context)
        
        # Verify test code included
        content = '\n'.join(instructions.display_content)
        assert 'def test_scenario(self, helper):' in content
        assert 'result = helper.execute_test()' in content
        
        # Verify trace includes test helper (depth 1)
        assert 'TestHelper.execute_test' in content or 'execute_test' in content
    
    def test_scope_with_include_level_code(self, tmp_path):
        """
        SCENARIO: Scope with include_level='code' includes full trace
        GIVEN: Story with test that calls domain code
        AND: Domain code exists in src/ directory
        WHEN: include_level='code'
        THEN: Scope includes full trace to implementation
        AND: Trace depth limited to 3 levels
        AND: Traces into src/ directory (domain code)
        """
        helper = BotTestHelper(tmp_path)
        
        # Create domain code
        domain_code = '''
class StoryProcessor:
    def __init__(self, name):
        self.name = name
    
    def process(self):
        result = self._execute()
        return result
    
    def _execute(self):
        return {"status": "success"}
'''
        domain_file = helper.workspace / 'src' / 'processor.py'
        domain_file.parent.mkdir(parents=True, exist_ok=True)
        domain_file.write_text(domain_code)
        
        # Create test that calls domain code
        test_code = '''
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.processor import StoryProcessor

class TestStory:
    def test_scenario(self):
        """Test with domain code"""
        processor = StoryProcessor("test")
        result = processor.process()
        assert result["status"] == "success"
'''
        test_file = helper.workspace / 'test' / 'test_story.py'
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text(test_code)
        
        # Create story graph
        story_graph = helper.story.given_story_graph_dict(
            epic='TestEpic',
            sub_epic='TestSubEpic',
            story='TestStory',
            test_file='test/test_story.py',
            test_class='TestStory',
            scenarios=[{
                'name': 'Test scenario',
                'test_method': 'test_scenario'
            }]
        )
        helper.files.given_file_created(
            helper.workspace / 'docs' / 'story',
            'story-graph.json',
            story_graph
        )
        
        # Set scope with include_level='code'
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.STORY, value=['TestStory'])
        scope.include_level = 'code'
        scope.apply_to_bot()
        
        # Get instructions
        helper.bot.behaviors.navigate_to('shape')
        action = helper.bot.behaviors.current.actions.find_by_name('build')
        context = ScopeActionContext(scope=scope)
        instructions = action.get_instructions(context)
        
        # Verify full trace included
        content = '\n'.join(instructions.display_content)
        
        # Test method
        assert 'def test_scenario(self):' in content
        
        # Domain code (level 1)
        assert 'StoryProcessor.__init__' in content or 'class StoryProcessor' in content
        
        # Domain method (level 2)
        assert 'def process(self):' in content or 'processor.process' in content
        
        # Trace should show nested structure
        assert 'src/processor.py' in content
```

---

## Code Changes

### 1. Reorganize Trace Prototype

**Current Location:** `src/trace_notebook/`  
**New Location:** `src/traceability/`

**Files to Move:**
```
src/trace_notebook/strace_generator.py → src/traceability/trace_generator.py
src/trace_notebook/cli/workspace_index.py → src/traceability/workspace_index.py
src/trace_notebook/cli/python_analyzer.py → src/traceability/python_analyzer.py
src/trace_notebook/cli/snippet_extractor.py → src/traceability/snippet_extractor.py
```

**Files to Keep (for now):**
```
src/trace_notebook/cli/trace_cli.py (optional - CLI daemon for future interactive use)
src/trace_notebook/ext/ (VS Code extension - separate later to extensions/)
src/trace_notebook/*.strace (generated files - move to docs/traces/ or .gitignore)
```

**Cleanup:**
```
src/trace_notebook/ext/*.vsix (30+ VSIX builds) → Add to .gitignore, keep only latest
```

### 2. Domain Model Changes

**File:** `src/scope/scope.py`

```python
class Scope:
    def __init__(self, workspace_directory: Path, bot_paths=None):
        # ... existing ...
        self.include_level: str = 'examples'  # NEW: default level
    
    def to_dict(self) -> dict:
        """Serialize scope including include_level"""
        return {
            'type': self.type.value,
            'value': self.value,
            'exclude': self.exclude,
            'skiprule': self.skiprule,
            'include_level': self.include_level  # NEW
        }
    
    def load(self):
        """Load scope from scope.json including include_level"""
        scope_file = self.workspace_directory / 'scope.json'
        if not scope_file.exists():
            return
        
        scope_data = json.loads(scope_file.read_text())
        self.type = ScopeType(scope_data.get('type', 'all'))
        self.value = scope_data.get('value', [])
        self.exclude = scope_data.get('exclude', [])
        self.skiprule = scope_data.get('skiprule', [])
        self.include_level = scope_data.get('include_level', 'examples')  # NEW
```

### 3. Adapter Changes

**File:** `src/scope/json_scope.py` (lines 77-81)

```python
def to_dict(self) -> dict:
    # ... existing code ...
    
    if self.scope.type.value in ('story', 'showAll'):
        story_graph = self.scope._get_story_graph_results()
        if story_graph:
            # ... cache logic ...
            
            if content is None:
                # Generate with include_level filtering
                from story_graph.json_story_graph import JSONStoryGraph
                graph_adapter = JSONStoryGraph(story_graph)
                
                # NEW: Pass include_level to serializer
                include_level = self.scope.include_level
                content = graph_adapter.to_dict(include_level=include_level).get('content', [])
                
                # ... rest of existing code ...
```

### 4. Story Graph Serialization Changes

**File:** `src/story_graph/json_story_graph.py`

```python
def to_dict(self, include_level: str = 'examples') -> dict:
    """
    Serialize story graph with optional filtering by include_level.
    
    Args:
        include_level: One of 'stories', 'acceptance', 'scenarios', 
                      'examples', 'tests', 'code'
    """
    # Load domain objects
    from story_graph.nodes import StoryMap
    story_map = StoryMap(self.story_graph.content, bot=None)
    
    # ... existing epic_name_to_data mapping ...
    
    # Serialize with include_level
    content = {
        'epics': [
            self._serialize_epic(epic, epic_name_to_data, include_level) 
            for epic in story_map._epics
        ]
    }
    
    # ... rest of existing code ...
    
    return {
        'path': str(self.story_graph.path),
        'has_epics': self.story_graph.has_epics,
        'has_increments': self.story_graph.has_increments,
        'has_domain_concepts': self.story_graph.has_domain_concepts,
        'epic_count': self.story_graph.epic_count,
        'content': content
    }

def _serialize_epic(self, epic, name_to_data_map=None, include_level='examples') -> dict:
    """Serialize Epic with include_level filtering"""
    result = {
        'name': epic.name,
        'behavior_needed': epic.behavior_needed,
        'domain_concepts': [],  # ... existing logic ...
        'sub_epics': [
            self._serialize_sub_epic(child, name_to_data_map, include_level) 
            for child in epic.children
        ]
    }
    return result

def _serialize_sub_epic(self, sub_epic, name_to_data_map=None, include_level='examples') -> dict:
    """Serialize SubEpic with include_level filtering"""
    # ... existing code ...
    
    for child in sub_epic.children:
        if isinstance(child, Story):
            result['story_groups'][-1]['stories'].append(
                self._serialize_story(child, include_level)
            )
    
    return result

def _serialize_story(self, story, include_level='examples') -> dict:
    """Serialize Story with include_level filtering"""
    result = {
        'name': story.name,
        'behavior_needed': story.behavior_needed,
        'test_file': story.test_file if hasattr(story, 'test_file') else None,
        'test_class': story.test_class if hasattr(story, 'test_class') else None,
    }
    
    # Include acceptance criteria if level >= 'acceptance'
    if include_level in ['acceptance', 'scenarios', 'examples', 'tests', 'code']:
        result['acceptance_criteria'] = [
            self._serialize_ac(ac) for ac in story.acceptance_criteria
        ]
    
    # Include scenarios if level >= 'scenarios'
    if include_level in ['scenarios', 'examples', 'tests', 'code']:
        result['scenarios'] = [
            self._serialize_scenario(sc, include_level) 
            for sc in story.scenarios
        ]
    
    return result

def _serialize_scenario(self, scenario, include_level='examples') -> dict:
    """Serialize Scenario with include_level filtering and optional trace"""
    result = {
        'name': scenario.name,
        'behavior_needed': scenario.behavior_needed,
        'test_method': scenario.test_method if hasattr(scenario, 'test_method') else None,
        'type': scenario.type if hasattr(scenario, 'type') else '',
        'sequential_order': scenario.sequential_order,
    }
    
    # Include background/steps if level >= 'scenarios'
    if include_level in ['scenarios', 'examples', 'tests', 'code']:
        result['background'] = self._serialize_steps(scenario.background)
        result['steps'] = self._serialize_steps(scenario.steps)
    
    # Include examples if level >= 'examples'
    if include_level in ['examples', 'tests', 'code']:
        result['examples'] = scenario.examples if hasattr(scenario, 'examples') else None
    
    # Include test code if level >= 'tests'
    if include_level in ['tests', 'code']:
        result['test'] = self._generate_test_code(scenario)
    
    # Include full trace if level == 'code'
    if include_level == 'code':
        result['trace'] = self._generate_trace(scenario, include_implementation=True)
    
    return result

def _generate_test_code(self, scenario) -> Optional[dict]:
    """Extract test method code for scenario"""
    if not hasattr(scenario, 'test_method') or not scenario.test_method:
        return None
    
    # Get parent story to find test_file and test_class
    story = scenario._parent  # Assuming parent is set during construction
    if not story or not hasattr(story, 'test_file') or not story.test_file:
        return None
    
    test_file = self.story_graph._workspace_directory / story.test_file
    if not test_file.exists():
        return None
    
    # Use trace generator to extract test method
    from traceability.trace_generator import TraceGenerator
    generator = TraceGenerator(self.story_graph._workspace_directory, max_depth=3)
    
    try:
        source = test_file.read_text(encoding='utf-8')
        lines = source.split('\n')
        code, start, end = generator._extract_method_from_class(
            source, lines, story.test_class, scenario.test_method
        )
        
        if code:
            return {
                'method': scenario.test_method,
                'file': str(story.test_file),
                'line': start,
                'code': code
            }
    except Exception:
        pass
    
    return None

def _generate_trace(self, scenario, include_implementation=False) -> list:
    """Generate trace for scenario using trace generator"""
    if not hasattr(scenario, 'test_method') or not scenario.test_method:
        return []
    
    story = scenario._parent
    if not story or not hasattr(story, 'test_file') or not story.test_file:
        return []
    
    from traceability.trace_generator import DynamicStraceGenerator
    generator = DynamicStraceGenerator(
        self.story_graph._workspace_directory,
        max_depth=3
    )
    
    try:
        # Build method index
        generator._build_method_index()
        
        # Get test code
        test_file = self.story_graph._workspace_directory / story.test_file
        source = test_file.read_text(encoding='utf-8')
        lines = source.split('\n')
        
        # Extract test method
        test_code, test_start, test_end = generator._extract_method_from_class(
            source, lines, story.test_class, scenario.test_method
        )
        
        if not test_code:
            return []
        
        # Analyze for calls
        calls = generator._find_calls_in_code(test_code)
        
        # Build trace
        trace_sections = []
        for call in calls:
            section = generator._resolve_call(call, depth=1)
            if section:
                trace_sections.append(section)
        
        return trace_sections
        
    except Exception:
        return []
```

### 5. Trace Generator Refactoring

**File:** `src/traceability/trace_generator.py` (renamed from `strace_generator.py`)

**Changes:**
- Remove `StraceGenerator` (older version)
- Keep `DynamicStraceGenerator`
- Rename `DynamicStraceGenerator` → `TraceGenerator`
- Ensure `max_depth=3` is the default
- Ensure it only searches workspace directories (test/, src/)

```python
class TraceGenerator:
    """Generate trace by analyzing code - no hardcoding."""
    
    def __init__(self, workspace: Path, max_depth: int = 3):
        self.workspace = workspace
        self.max_depth = max_depth  # Default to 3
        self.seen_symbols = set()
        self._file_cache = {}
        self._method_index = None
    
    # ... rest of existing DynamicStraceGenerator code ...
```

---

## Panel Changes (Future)

**File:** `src/panel/bot_panel.js`

Add radio button controls for include_level in the scope section:

```javascript
// In renderScopeSection()
const includeLevelControls = `
  <div class="include-level-controls">
    <label>Include up to:</label>
    <div class="radio-group">
      <input type="radio" name="includeLevel" value="stories" ${includeLevel === 'stories' ? 'checked' : ''}>
      <label>Stories</label>
      
      <input type="radio" name="includeLevel" value="acceptance" ${includeLevel === 'acceptance' ? 'checked' : ''}>
      <label>Acceptance</label>
      
      <input type="radio" name="includeLevel" value="scenarios" ${includeLevel === 'scenarios' ? 'checked' : ''}>
      <label>Scenarios</label>
      
      <input type="radio" name="includeLevel" value="examples" ${includeLevel === 'examples' ? 'checked' : ''}>
      <label>Examples</label>
      
      <input type="radio" name="includeLevel" value="tests" ${includeLevel === 'tests' ? 'checked' : ''}>
      <label>Tests</label>
      
      <input type="radio" name="includeLevel" value="code" ${includeLevel === 'code' ? 'checked' : ''}>
      <label>Code</label>
    </div>
  </div>
`;

// On change, update scope
document.querySelectorAll('input[name="includeLevel"]').forEach(radio => {
  radio.addEventListener('change', async (e) => {
    const level = e.target.value;
    const result = await this.cliClient.execute(`scope include_level=${level}`);
    // Refresh panel to show updated scope
    this.refresh();
  });
});
```

---

## Implementation Steps

### Phase 1: Core Infrastructure (Domain + Serialization)
1. ✅ Move trace prototype to `src/traceability/`
2. ✅ Add `include_level` property to `Scope` class
3. ✅ Update `Scope.to_dict()` and `Scope.load()` to persist `include_level`
4. ✅ Update `JSONScope.to_dict()` to pass `include_level` to serializer
5. ✅ Update `JSONStoryGraph.to_dict()` to accept `include_level` parameter
6. ✅ Implement filtering logic in all `_serialize_*` methods

### Phase 2: Trace Integration
7. ✅ Refactor `DynamicStraceGenerator` → `TraceGenerator`
8. ✅ Add `_generate_test_code()` to `JSONStoryGraph`
9. ✅ Add `_generate_trace()` to `JSONStoryGraph`
10. ✅ Integrate trace generation when `include_level='tests'` or `'code'`

### Phase 3: Testing
11. ✅ Add new scenarios to story-graph.json
12. ✅ Write tests for include_level persistence
13. ✅ Write tests for each include_level filtering
14. ✅ Write tests for trace generation (tests and code levels)
15. ✅ Run existing tests to ensure no regression

### Phase 4: Panel Integration (Future)
16. ⏸️ Add radio button controls to panel
17. ⏸️ Add CLI command `scope include_level=<level>`
18. ⏸️ Update panel to persist include_level selection

### Phase 5: Cleanup
19. ✅ Add `*.vsix` to `.gitignore`
20. ✅ Move generated `.strace` files to `docs/traces/`
21. ✅ Update documentation

---

## Expected Output Example

When user sets `include_level='code'` and submits:

```markdown
## Scope

**Story Scope:** Generate Bot Tools

Scope:

{
  "epics": [{
    "name": "Build Agile Bots",
    "sub_epics": [{
      "name": "Generate MCP Tools",
      "stories": [{
        "name": "Generate Bot Tools",
        "acceptance_criteria": [
          "Generator creates tool for test bot"
        ],
        "scenarios": [{
          "name": "Generator creates tool for test bot",
          "steps": "GIVEN story_bot with test behavior...",
          "test": {
            "method": "test_generator_creates_tool_for_test_bot",
            "file": "test/build_agile_bots/test_generate_mcp_tools.py",
            "line": 45,
            "code": "def test_generator_creates_tool_for_test_bot(self, tmp_path):\n    helper = BotTestHelper(tmp_path)\n    generator = BotToolsGenerator(helper.bot)\n    result = generator.generate()\n    assert result.success"
          },
          "trace": [
            {
              "symbol": "BotToolsGenerator.__init__",
              "file": "src/generator/bot_tools_generator.py",
              "line": 12,
              "depth": 1,
              "code": "def __init__(self, bot):\n    self.bot = bot\n    self.template_loader = TemplateLoader()",
              "children": [
                {
                  "symbol": "TemplateLoader.__init__",
                  "file": "src/generator/template_loader.py",
                  "line": 8,
                  "depth": 2,
                  "code": "def __init__(self):\n    self.templates = {}"
                }
              ]
            },
            {
              "symbol": "BotToolsGenerator.generate",
              "file": "src/generator/bot_tools_generator.py",
              "line": 28,
              "depth": 1,
              "code": "def generate(self):\n    template = self.template_loader.load('bot_tool.py.jinja')\n    return self._render(template)"
            }
          ]
        }]
      }]
    }]
  }]
}
```

---

## Success Criteria

- ✅ `scope.json` persists and restores `include_level`
- ✅ Each include_level filters content correctly
- ✅ Trace generated at depth=3 for 'tests' level
- ✅ Full trace generated at depth=3 for 'code' level
- ✅ All existing tests pass (no regression)
- ✅ New tests pass for all scenarios
- ✅ AI receives complete trace context when debugging

---

## Future Enhancements

1. **Panel Radio Buttons**: Add UI controls for include_level selection
2. **CLI Command**: `scope include_level=code` to set from CLI
3. **VS Code Extension**: Separate `src/trace_notebook/ext/` to `extensions/story-trace/`
4. **Interactive Trace Explorer**: Use `trace_cli.py` daemon for panel-based trace exploration
5. **Trace Caching**: Cache generated traces to avoid re-parsing on every instruction generation
6. **Configurable Depth**: Allow override of max_depth=3 via `scope.trace_depth`
7. **Multi-language Support**: Extend trace to JavaScript/TypeScript test files
