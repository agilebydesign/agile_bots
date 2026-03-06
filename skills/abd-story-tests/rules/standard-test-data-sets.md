---
title: standard-test-data-sets
priority: 17
---

## standard-test-data-sets

Use standard
named test data sets across tests instead of recreating ad-hoc values. Example: STANDARD_STATE = {...}; helper.set_state(...); assert helper.get_state() == STANDARD_STATE.

**DO**

Define canonical data once (helper constants/factories) and reuse it so every test exercises the full domain object.

Centralize baseline data in helper factories/constants and reuse it

```
STANDARD_STATE = {
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

```
def test_uses_standard_state(self, tmp_path):
```

```
    helper = BotTestHelper(tmp_path)
```

```
    helper.set_state('shape', 'clarify', completed_actions=STANDARD_STATE['completed_actions'])
```

```
    assert helper.get_state() == STANDARD_STATE
```

When a scenario varies
derive from the standard data set with minimal overrides

```
def test_strategy_variation(self, tmp_path):
```

```
    helper = BotTestHelper(tmp_path)
```

```
    base_graph = {'stories': ['shape.clarify', 'shape.strategy']}
```

```
    variant = {**base_graph, 'stories': base_graph['stories'] + ['shape.validate']}
```

```
    actual = helper.create_story_graph(variant)
```

```
    assert actual['stories'] == variant['stories']
```

**DO NOT**

Do not create new ad-hoc values per test or assert only one field from a complex object.

Do not define slightly different inline dicts in every test

```
def test_one():
```

```
    state = {'current': 'shape.clarify', 'completed_actions': []}
```

```
def test_two():
```

```
    state = {'current': 'shape.strategy', 'completed_actions': ['a']}
```

```
# WRONG - create one standard state and reuse
```

Do not parametrize across individual fields when a standard fixture can be reused

```
@pytest.mark.parametrize('current,completed', [
```

```
    ('shape.clarify', []),
```

```
    ('shape.strategy', ['a'])
```

```
])
```

```
def test_state(current, completed):
```

```
    state = {'current': current, 'completed_actions': completed}
```

```
    assert state['current'].startswith('shape')  # WRONG - partial assertion
```