---
title: object-oriented-test-helpers
priority: 16
---

## object-oriented-test-helpers

Consolidate tests around object-oriented helpers/factories (e.g.
BotTestHelper test hopper) that build complete domain objects with standard data. Example: helper = BotTestHelper(tmp_path); helper.set_state('shape'
'clarify'); helper.assert_at_behavior_action('shape'
'clarify'). Avoid scattering many primitive parameters across parametrize blocks or inline setups.

**DO**

Use shared helper objects to create full test fixtures and assert against complete domain objects
not fragments.

Use BotTestHelper (or equivalent factory) as the single entry point for bot + workspace setup

```
def test_navigation_stays_on_shape(self, tmp_path):
```

```
    helper = BotTestHelper(tmp_path)
```

```
    helper.set_state('shape', 'clarify', completed_actions=['story_bot.shape.strategy'])
```

```
    helper.bot.behaviors.navigate_to('shape')
```

```
    helper.assert_at_behavior_action('shape', 'clarify')
```

Build complete domain objects once
then assert on the whole object (or dict) instead of single fields

```
def test_state_file_is_complete(self, tmp_path):
```

```
    helper = BotTestHelper(tmp_path)
```

```
    helper.set_state('shape', 'clarify', completed_actions=['story_bot.shape.strategy'])
```

```
    state = helper.get_state()
```

```
    assert state == {
```

```
        'current': 'story_bot.shape.clarify',
```

```
        'completed_actions': ['story_bot.shape.strategy']
```

```
    }
```

Start from a standard data set and vary only what the scenario needs (extend helper factories rather than adding parameters)

```
def test_story_graph_filter_by_scope(self, tmp_path):
```

```
    helper = BotTestHelper(tmp_path)
```

```
    standard_graph = {'stories': ['shape.clarify', 'shape.strategy']}
```

```
    story_graph = helper.create_story_graph(standard_graph)
```

```
    filtered = helper.bot.story_graph.filter_by_scope(story_graph, scope='shape')
```

```
    assert filtered['stories'] == standard_graph['stories']
```

**DO NOT**

Do not spread test setup across many primitive parameters or cherry-pick single values from partial objects.

Do not add @pytest.mark.parametrize with many primitive columns when a helper could return a ready domain object

```
@pytest.mark.parametrize('path,name,behavior,action,completed,log', [
```

```
    ('/tmp/p1', 'bot', 'shape', 'clarify', ['a'], {}),
```

```
    ('/tmp/p2', 'bot', 'shape', 'strategy', ['b'], {}),
```

```
])
```

```
def test_state(path, name, behavior, action, completed, log):
```

```
    # WRONG: scattered primitives instead of helper-built state
```

Do not hand-craft partial dicts in each test when a factory can return the whole object

```
def test_partial_state(self, tmp_path):
```

```
    state = {'current': 'story_bot.shape.clarify'}  # WRONG - missing completed_actions, brittle
```

```
    assert state['current'] == 'story_bot.shape.clarify'
```

Do not assert only one field from a complex object; verify the complete result built by the helper

```
def test_activity_log(self, tmp_path):
```

```
    log = helper.get_activity_log()
```

```
    assert log['events'][0]['action'] == 'clarify'  # WRONG - ignores rest of the log structure
```