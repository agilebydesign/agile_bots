---
title: helper-extraction-and-reuse
priority: 13
---

## helper-extraction-and-reuse

Extract duplicate test setup to reusable helper functions. Keep test bodies focused on specific behavior. Example: create_agent_with_config()
create_config_file()
verify_agent_initialized() - reusable across tests

**DO**

Extract duplicate setup to reusable helpers. Example: create_agent_with_config(name
workspace
config) returns initialized Agent

Create factory helpers for common object creation

```
def create_agent_with_config(name, workspace, config):
```

```
    agent = Agent(name, workspace); agent.set_config(config); agent.initialize(); return agent
```

Create file setup helpers

```
def create_config_file(workspace, agent_name):
```

```
    path = workspace / 'config.json'; path.write_text(json.dumps({'name': agent_name})); return path
```

Create verification helpers for common assertions

```
def verify_agent_initialized(agent, expected_name):
```

```
    assert agent.is_initialized; assert agent.name == expected_name
```

Keep test bodies focused using helpers

```
def test_agent_loads_config():
```

```
    agent = create_agent_with_config('bot', workspace, {})
```

```
    verify_agent_initialized(agent, 'bot')
```

**DO NOT**

Don't duplicate setup code across tests. Example: Same 10 lines of setup in every test method (wrong - extract to helper)

Don't duplicate setup code in every test

```
# WRONG: Same setup in 5 tests
```

```
def test_1(): workspace = tmp_path / 'w'; workspace.mkdir(); agent = Agent(w)...
```

```
def test_2(): workspace = tmp_path / 'w'; workspace.mkdir(); agent = Agent(w)...
```

Don't inline complex setup in test body

```
def test_loads_config():
```

```
    # WRONG: 20 lines of setup inline
```

```
    config_dir = workspace / 'agents' / 'base'; config_dir.mkdir(parents=True)...
```

Don't mix setup and assertions

```
# WRONG: Setup, assert, more setup, assert, mixed together
```