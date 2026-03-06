---
title: match-specification-scenarios
priority: 14
---

## match-specification-scenarios

Tests must match specification scenarios exactly. Test names
steps
and assertions verify exactly what the scenario states. Use exact variable names and terminology from specification. Example: agent_name='story_bot' (from spec)
not name='bot'

**DO**

Test matches specification exactly. Example: GIVEN config exists
WHEN Agent(agent_name='story_bot')
THEN config_path == agents/base/agent.json

Test name and docstring match scenario

```
def test_agent_initializes_with_base_config():
```

```
    '''SCENARIO: Agent initializes with base configuration
```

```
    GIVEN: Base agent configuration exists
```

```
    WHEN: Agent is initialized with agent_name='story_bot'
```

```
    THEN: Agent sets up config path at agents/base/agent.json'''
```

Use exact variable names from specification

```
# Spec says: agent_name='story_bot', workspace_root='/test'
```

```
agent = Agent(agent_name='story_bot', workspace_root=workspace_root)
```

Assert exactly what scenario states - no more
no less

```
# Spec THEN: 'config_path at agents/base/agent.json'
```

```
expected = workspace_root / 'agents' / 'base' / 'agent.json'
```

```
assert agent.config_path == expected
```

**DO NOT**

Don't use different terminology or assert things not in specification. Example: assert agent._internal_flag (not in spec - wrong)

Don't use vague or different terminology

```
def test_agent_init():  # WRONG - spec says 'initializes with base config'
```

```
    '''Test agent'''  # WRONG - doesn't match spec
```

Don't use different variable names

```
name = 'story_bot'  # WRONG - spec says 'agent_name'
```

```
root = Path('/test')  # WRONG - spec says 'workspace_root'
```

Don't assert implementation details not in spec

```
assert agent._internal_flag == True  # WRONG - not in spec
```

```
assert agent.validate.called  # WRONG - implementation detail
```