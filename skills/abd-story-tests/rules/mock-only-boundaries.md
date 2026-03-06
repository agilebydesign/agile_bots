---
title: mock-only-boundaries
priority: 8
---

## mock-only-boundaries

Mock ONLY at architectural boundaries: external APIs
network
uncontrollable services. Don't mock internal business logic
classes under test
or file operations (use temp files). Example: patch('requests.get') (OK); patch('agent.validate') (wrong)

**DO**

Mock only external dependencies you can't control. Example: with patch('requests.get') as mock: (external API - OK to mock)

Mock external APIs

```
with patch('requests.get') as mock_get:
```

```
    mock_get.return_value.json.return_value = {'name': 'bot'}
```

```
    agent = Agent.from_remote_config('http://api.com/config')
```

Mock external services (monitoring
logging to external)

```
with patch('monitoring.send_metric') as mock_send:
```

```
    agent = Agent('bot', Path('/tmp'))
```

```
    mock_send.assert_called_with('agent.initialized')
```

Use real temp files instead of mocking file I/O

```
config_file = tmp_path / 'config.json'
```

```
config_file.write_text('{"name": "bot"}')
```

```
agent = Agent.from_config_file(config_file)  # Real file, no mock
```

**DO NOT**

Don't mock internal logic
class under test
or file I/O. Example: with patch('agent.validate_config') (wrong - test the logic!)

Don't mock the class you're testing

```
agent = Mock(spec=Agent)  # WRONG - defeats purpose of test
```

Don't mock internal business logic

```
with patch('agent.validate_config'):  # WRONG - test the validation!
```

Don't mock file operations when temp files work

```
with patch('pathlib.Path.read_text'):  # WRONG - use real temp file
```

Don't mock collaborators that are simple value objects

```
config = Mock()  # WRONG if Config is just a dict/dataclass - use real one
```