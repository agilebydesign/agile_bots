---
title: self-documenting-tests
priority: 17
---

## self-documenting-tests

Tests are self-documenting through code structure. Don't add verbose comments explaining failures. Imports
calls
and assertions show the API design. Let code speak for itself. Example: generator = MCPServerGenerator(bot_name
config_path); server = generator.generate_server()

**DO**

Let code structure document the test. Example: generator = MCPServerGenerator(name
config); file = generator.generate() - API is clear

Imports show required modules

```
from agile_bot.bots.base_bot.src.mcp_generator import MCPServerGenerator
```

```
# Import documents what module is needed
```

Constructor calls show required parameters

```
generator = MCPServerGenerator(bot_name=name, config_path=path, workspace_root=root)
```

```
# Parameters document the API contract
```

Method calls show available operations

```
server_file = generator.generate_server()
```

```
# Method name documents the capability
```

Assertions show expected behavior

```
assert server_file.exists()
```

```
assert 'test_bot' in server_file.read_text()
```

```
# Assertions document what should happen
```

**DO NOT**

Don't add verbose comments explaining obvious things. Example: # This will fail because API doesn't exist yet (unnecessary)

Don't state the obvious in comments

```
# This test will fail because the method doesn't exist  # WRONG - unnecessary
```

```
# The import will fail  # WRONG - let it fail
```

Don't explain what the code already shows

```
# Create an agent with the name 'bot'
```

```
agent = Agent(name='bot')  # WRONG - code is self-explanatory
```

Don't add TODO comments for obvious API needs

```
# TODO: Need to implement generate_server method  # WRONG - failing test shows this
```