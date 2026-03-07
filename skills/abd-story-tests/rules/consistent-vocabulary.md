---
title: consistent-vocabulary
priority: 2
---

## consistent-vocabulary

Use ONE word per concept across entire codebase. Pick consistent vocabulary: create (not build/make/construct)
verify (not check/assert/validate)
load (not fetch/get/retrieve). Use intention-revealing names that describe behavior. Example: create_agent()
verify_initialized()
load_config() - same verbs everywhere

**DO**

Use same word for same concept everywhere. Example: create_agent()
create_config()
create_workspace() - all use 'create'

Use 'create_*' consistently for all creation

```
def create_agent(name):
```

```
def create_config(workspace):
```

```
def create_workspace(tmp_path):
```

Use 'verify_*' consistently for all assertions

```
def verify_agent_initialized(agent):
```

```
def verify_config_valid(config):
```

```
def verify_file_exists(path):
```

Use 'load_*' consistently for reading data

```
def load_config(workspace):
```

```
def load_graph(path):
```

```
def load_data(file):
```

Document vocabulary choices in test file docstring

```
"""Vocabulary: create_* (objects), verify_* (assertions), load_* (files), setup_* (preconditions)"""
```

**DO NOT**

Don't mix synonyms for same concept. Example: create_agent() + build_config() + make_workspace() (wrong - pick one verb)

Don't mix create/build/make/construct

```
def create_agent():
```

```
def build_config():  # WRONG - use create_config
```

```
def make_workspace():  # WRONG
```

Don't mix verify/check/assert/validate randomly

```
def verify_agent():
```

```
def check_config():  # WRONG - use verify_config
```

```
def assert_file():  # WRONG
```

Don't use vague or abbreviated names

```
def setup(data):  # WRONG - setup what?
```

```
def do_thing(obj):  # WRONG
```

```
def test1(self):  # WRONG
```