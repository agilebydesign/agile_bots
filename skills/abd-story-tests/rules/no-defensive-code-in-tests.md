---
title: no-defensive-code-in-tests
priority: 3
---

## no-defensive-code-in-tests

Tests must NEVER contain guard clauses
defensive conditionals
or fallback paths. We control test setup - if it's wrong
the test MUST fail immediately. Guard clauses hide problems. Tests should assume positive outcomes. Example: Just call the code directly
don't wrap in if-checks

**DO**

Assume correct setup - let test fail if wrong. Example: behavior = Behavior(name='shape') then assert behavior.name == 'shape'

Call code directly without checking preconditions

```
behavior = Behavior(name='shape', bot_paths=bot_paths)
```

```
assert behavior.name == 'shape'
```

Assert the specific behavior path is taken

```
result = execute_behavior(mode='agile')
```

```
assert result.mode == 'agile'
```

```
assert result.used_fallback is False
```

Let test fail if setup is wrong - this is valuable information

```
config = agent.load_config(config_file)  # Will fail if file missing - GOOD
```

**DO NOT**

Don't add if-checks
type guards
or fallback handling in tests. Example: if behavior_file.exists(): (wrong - test should fail if it doesn't)

Don't check file existence before using file

```
if behavior_file.exists():  # WRONG
```

```
    behavior = Behavior(...)  # Test should fail if file missing!
```

Don't check variable types in tests

```
if isinstance(behavior_obj, Behavior):  # WRONG
```

```
    assert len(behavior_obj.actions) > 0  # Test should fail if wrong type!
```

Don't let fallback paths pass tests

```
result = execute_behavior(mode=None)
```

```
assert result.stage == 'default_flow'  # WRONG - testing fallback not requirement
```

Don't add try/except around test code

```
try:  # WRONG
```

```
    result = process()
```

```
except:  # Don't catch - let test fail!
```