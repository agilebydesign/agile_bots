---
title: bug-fix-test-first
priority: 5
---

## bug-fix-test-first

When production code breaks
follow test-first workflow: write failing test
verify failure
fix code
verify success. Never fix bugs without a failing test first. Example: test_mcp_tool_initializes_bot() fails -> fix initialization -> test passes

**DO**

Follow RED-GREEN-PRODUCTION workflow. Example: Write test reproducing bug -> Run test (RED) -> Fix minimal code -> Run test (GREEN) -> Run full suite

Write test that reproduces the bug before fixing

```
def test_mcp_tool_initializes_bot_before_invocation():
```

```
    # Reproduces: 'Bot not initialized' error
```

```
    server = MCPServer(); tool = server.get_tool(); result = tool.invoke()
```

```
    assert result.success
```

Verify test fails before fixing (RED)

```
# Run: pytest test_mcp_tool.py
```

```
# Expected: FAILED - AttributeError: Bot not initialized
```

```
# This proves we can reproduce the bug
```

Make minimal fix to pass the test (GREEN)

```
# Fix: Add self._bot = Bot() in MCPServer.__init__
```

```
# Run: pytest test_mcp_tool.py
```

```
# Expected: PASSED
```

Run full test suite to check for regressions

```
# Run: pytest tests/
```

```
# All tests pass -> Safe to deploy
```

**DO NOT**

Don't fix bugs directly without failing test first. Example: Editing production code without test -> deploying -> hoping it works (wrong)

Don't fix code before writing a failing test

```
# WRONG: Jump straight to fixing
```

```
# Edit mcp_server.py without test
```

```
# Deploy and hope for the best
```

Don't skip the RED step - verify test actually fails

```
# WRONG: Write test that passes immediately
```

```
def test_something(): assert True  # This proves nothing!
```

Don't make large changes - fix should be minimal

```
# WRONG: Refactor entire class while fixing one bug
```

```
# This introduces risk of new bugs
```