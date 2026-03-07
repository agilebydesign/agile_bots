---
title: call-production-code-directly
priority: 6
---

## call-production-code-directly

Call production code directly in tests. Let tests fail naturally if code doesn't exist. Don't comment out calls
mock business logic
or fake state. Only mock external boundaries. Example: agent = Agent(); agent.initialize() (not agent = Mock())

**DO**

Call production code directly
let it fail naturally. Example: agent = Agent(workspace); agent.initialize(config); assert agent.is_initialized

Call production code directly in tests

```
agent = Agent(agent_name='story_bot', workspace_root=workspace)
```

```
agent.initialize(config)
```

```
assert agent.is_initialized
```

Let tests fail with clear errors if code doesn't exist

```
# If initialize() doesn't exist: AttributeError: 'Agent' has no attribute 'initialize'
```

```
# This drives creation of the method
```

Only mock external boundaries when necessary

```
with patch('requests.get') as mock_get:  # External API - OK to mock
```

```
    mock_get.return_value.json.return_value = {'name': 'bot'}
```

**DO NOT**

Don't mock class under test
comment out calls
or fake state. Example: agent = Mock(spec=Agent) (wrong); agent._initialized = True (wrong)

Don't mock the class you're testing

```
agent = Mock(spec=Agent)  # WRONG - defeats purpose of test
```

Don't comment out production code calls

```
# agent.initialize()  # WRONG - test should fail!
```

Don't fake internal state

```
agent._initialized = True  # WRONG - bypasses the logic you're testing
```

Don't mock business logic

```
with patch('agent.validate_config'):  # WRONG - test the logic!
```