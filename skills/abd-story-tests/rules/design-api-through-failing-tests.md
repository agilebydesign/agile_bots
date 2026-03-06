---
title: design-api-through-failing-tests
priority: 11
---

## design-api-through-failing-tests

Write tests against the REAL expected API BEFORE implementing code. Tests MUST fail initially. Set up real test data and call real API. Failure reveals complete API design. Example: project = Project(path=path); project.initialize() (doesn't exist yet -> fails -> drives implementation)

**DO**

Write test against real expected API that fails initially. Example: project = Project(path); project.initialize(); assert project.is_ready (fails until implemented)

Call the real expected API even if it doesn't exist

```
from mymodule import Project  # Will fail: ImportError
```

```
project = Project(path=path)
```

```
project.initialize()  # Will fail: AttributeError
```

Set up real test data (files
directories)

```
config_path = tmp_path / 'config.json'
```

```
config_path.write_text(json.dumps({'name': 'bot'}))
```

```
project = Project(config_path=config_path)  # Real file, real path
```

Assert real expected behavior

```
assert project.agent.name == 'story_bot'
```

```
assert project.config_path.exists()
```

**DO NOT**

Don't use placeholders
dummy values
or skip the failing step. Example: project = 'TODO' (wrong); assuming test passes first (wrong)

Don't use placeholder values

```
project = 'placeholder'  # WRONG - call real constructor
```

```
config = {}  # WRONG if real config has required fields
```

Don't skip the RED phase

```
# WRONG: Implementing code before test fails
```

```
# Test should fail with ImportError/AttributeError first
```

Don't write tests that pass immediately

```
def test_something(): assert True  # WRONG - proves nothing
```