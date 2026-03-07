---
title: test-observable-behavior
priority: 12
---

## test-observable-behavior

Test observable behavior
not implementation details. Verify public API and visible state changes. Don't assert on private methods or internal flags. Example: assert agent.config_path.exists() (observable); not assert agent._internal_flag (private)

**DO**

Test observable outcomes through public API. Example: assert agent.config_path == expected; assert agent.is_initialized (public properties)

Assert on public properties and return values

```
assert agent.config_path == expected_path  # Public property
```

```
assert agent.is_initialized  # Public property
```

Assert on observable file system state

```
assert agent.config_path.exists()  # File was created
```

```
assert output_file.read_text() == expected_content
```

Test WHAT happens
not HOW

```
# Test: 'config is loaded' not 'json.loads was called'
```

```
assert agent.config['name'] == 'bot'
```

**DO NOT**

Don't test private state or implementation details. Example: assert agent._initialized (wrong); assert agent._config_cache (wrong)

Don't assert on private attributes

```
assert agent._initialized  # WRONG - private
```

```
assert agent._config_cache is not None  # WRONG - implementation detail
```

Don't assert on internal method calls

```
assert agent._setup_called  # WRONG - implementation
```

```
assert len(agent._internal_list) == 3  # WRONG - private
```

Don't test HOW something is done

```
# WRONG: Testing that specific method was called
```

```
assert mock_parser.parse.called  # Test the RESULT instead
```