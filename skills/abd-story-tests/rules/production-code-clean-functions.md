---
title: production-code-clean-functions
priority: 4
---

## production-code-clean-functions

Production code functions should do ONE thing
be under 20 lines
and have one level of abstraction. No hidden side effects. Name reveals complete behavior. Extract multiple concerns into separate functions. Example: load_config()
validate_config()
apply_config() - each does one thing

**DO**

Single responsibility
small focused functions. Example: initialize_from_config() calls validate_exists()
load_config()
validate_structure()
apply_config()

Each function does ONE thing

```
def load_config(path): return json.loads(path.read_text())
```

```
def validate_config(config): return all(k in config for k in required)
```

Keep functions under 20 lines

```
def initialize_from_config(path):
```

```
    validate_file_exists(path)
```

```
    config = load_config(path)
```

```
    validate_structure(config)
```

```
    apply_config(config)
```

One level of abstraction per function

```
# High level: initialize_from_config()
```

```
# Low level: _load_config(), _validate_structure(), _apply_config()
```

Extract complex logic into named helper functions

```
def _validate_config_structure(config):
```

```
    missing = [f for f in required if f not in config]
```

```
    if missing: raise ValueError(f'Missing: {missing}')
```

**DO NOT**

Don't make functions that do multiple unrelated things or are too long. Example: 50-line function that loads
validates
and applies config

Don't do multiple things in one function

```
def initialize(path):  # WRONG - does too much
```

```
    # loads file, parses JSON, validates schema,
```

```
    # checks fields, creates objects, saves state...
```

Don't exceed 20 lines

```
def process_everything():  # WRONG - 50+ lines
```

```
    # ... huge monolithic function ...
```

Don't mix abstraction levels

```
def initialize():
```

```
    if path.exists():  # Low level
```

```
        self.orchestrate_full_workflow()  # High level - WRONG mix
```

Don't hide side effects - name should reveal all behavior

```
def get_config():  # WRONG - also writes cache file secretly
```

```
    config = load(); cache.write(config); return config
```