---
title: use-given-when-then-helpers
priority: 22
---

## use-given-when-then-helpers

Use reusable helper functions instead of inline code blocks of 4+ lines. Optimize for reusability
not exact step names. Place helpers at correct scope: story-level in class
sub-epic in module
epic in separate file. Example: given_config_exists()
when_agent_initialized()
then_agent_is_configured()

**DO**

Use Given/When/Then helper functions for setup
action
assertion. Example: given_bot_config_exists(); bot = when_bot_instantiated(); then_bot_uses_correct_directories(bot)

Given helpers for setup

```
config_path = given_bot_config_exists(workspace, 'test_bot', ['shape'])
```

When helpers for actions

```
bot = when_bot_is_instantiated('test_bot', bot_directory, config_path)
```

Then helpers for assertions

```
then_bot_uses_correct_directories(bot, bot_directory, workspace)
```

Place helpers at correct scope level

```
# Story-level: in test class
```

```
# Sub-epic: module level in test file
```

```
# Epic: separate test_<epic>_helpers.py file
```

```
# Global: conftest.py
```

**DO NOT**

Don't use inline operations of 4+ lines. Example: config_dir = ...; config_dir.mkdir(); config_file = ...; config_file.write_text() (wrong - extract to helper)

Don't use inline setup blocks of 4+ lines

```
# WRONG: 4+ lines inline
```

```
config_dir = workspace / 'config'; config_dir.mkdir()
```

```
config_file = config_dir / 'bot.json'; config_file.write_text('{}')
```

Don't use inline assertions of 4+ lines

```
# WRONG: 4+ lines inline
```

```
file = workspace / 'out.json'; data = json.loads(file.read_text())
```

```
assert 'key' in data; assert data['key'] == 'value'
```

Don't place helpers at wrong scope

```
# WRONG: Story-level helper in conftest.py
```

```
# WRONG: Epic-level helper in test class
```