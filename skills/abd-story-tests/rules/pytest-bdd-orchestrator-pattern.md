---
title: pytest-bdd-orchestrator-pattern
priority: 19
---

## pytest-bdd-orchestrator-pattern

Use pytest with orchestrator pattern for story-based tests. NO FEATURE FILES. Test classes contain orchestrator methods (under 20 lines) showing Given-When-Then flow by calling helper functions. Example: def test_agent_loads_config(): given_config_exists(); agent = when_agent_initialized(); then_agent_is_configured(agent)

**DO**

Orchestrator pattern: test shows flow
delegates to helpers. Example: # Given; create_config_file(); # When; agent.initialize(); # Then; assert agent.is_initialized

Test methods show Given-When-Then flow (under 20 lines)

```
def test_agent_loads_config():
```

```
    # Given: Config exists
```

```
    config_file = create_config_file(workspace)
```

```
    # When: Agent initialized
```

```
    agent = Agent(workspace).initialize()
```

```
    # Then: Config loaded
```

```
    assert agent.is_initialized
```

Helper functions handle details (under 20 lines each)

```
def create_config_file(workspace, name='bot'):
```

```
    path = workspace / 'config.json'; path.write_text('{}')
```

```
    return path
```

Test classes under 300 lines

```
class TestAgentConfiguration:
```

```
    # Multiple test methods, each under 20 lines
```

```
    # Extract shared setup to helpers
```

**DO NOT**

Don't use feature files or inline complex setup. Example: @given('config exists') def step(): ... (wrong - use pytest directly)

Don't use feature files or step definitions

```
# WRONG: Feature file approach
```

```
@given('config exists')
```

```
def step_config_exists(): ...
```

Don't inline complex setup in tests

```
def test_agent():
```

```
    # WRONG: 15 lines of setup inline
```

```
    config_dir = workspace / 'config'; config_dir.mkdir()...
```

Don't exceed 20 lines in test methods

```
def test_complex():  # WRONG - 40 lines
```

```
    # Extract to helpers!
```