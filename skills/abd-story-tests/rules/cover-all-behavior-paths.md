---
title: cover-all-behavior-paths
priority: 7
---

## cover-all-behavior-paths

Cover all behavior paths: normal (happy path)
edge cases
and failure scenarios. Each distinct behavior needs its own focused test. Tests must be independent. Example: test_loads_valid_config()
test_loads_empty_config()
test_raises_error_when_file_missing()

**DO**

Test normal
edge
and failure paths separately. Example: test_loads_valid_config() (happy)
test_loads_empty_config() (edge)
test_raises_when_missing() (failure)

Test normal/happy path

```
def test_loads_valid_configuration_from_file():
```

```
    config = agent.load_config(config_file)
```

```
    assert config['name'] == 'story_bot'
```

Test edge cases

```
def test_loads_empty_configuration_file():
```

```
    config = agent.load_config(empty_file)
```

```
    assert config == {}
```

Test failure scenarios

```
def test_raises_error_when_config_file_missing():
```

```
    with pytest.raises(FileNotFoundError):
```

```
        agent.load_config(Path('nonexistent.json'))
```

Each test is independent - can run in any order

```
# No shared state between tests
```

```
# Each test sets up its own data
```

**DO NOT**

Don't test only happy path or combine multiple behaviors in one test. Example: Single test for both success and failure (wrong)

Don't skip edge cases or failure paths

```
# WRONG: Only happy path tested
```

```
def test_loads_config(): ...  # What about empty? Missing? Invalid?
```

Don't combine multiple behaviors in one test

```
# WRONG: Tests both success and failure
```

```
def test_config_loading():
```

```
    # loads valid... then tests invalid... too much in one test
```

Don't make tests dependent on each other

```
# WRONG: test_2 depends on test_1 creating a file
```

```
def test_1(): create_file()
```

```
def test_2(): read_file()  # Fails if run alone!
```