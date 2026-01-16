# API Tests

## Overview

Some tests in this directory make real API calls to external services (e.g., `cursor-agent` CLI). These tests are marked with `@pytest.mark.api_required` and are **skipped by default** to keep test runs fast.

## Running Tests

### Default (Skip API Tests)
```bash
# Runs all tests EXCEPT slow API tests (fast, ~30-40 seconds)
pytest agile_bot/bots/base_bot/test/

# Or specifically for headless tests
pytest agile_bot/bots/base_bot/test/test_execute_in_headless_mode.py
```

**Result:** 14 tests run, 7 API tests skipped (~35 seconds)

### Include API Tests
```bash
# Run ONLY API tests (slow, 10+ minutes)
pytest agile_bot/bots/base_bot/test/ -m api_required

# Run ALL tests including API tests (very slow)
pytest agile_bot/bots/base_bot/test/ -m ""
```

**Result:** All 21 tests run (~10+ minutes)

## API Test Requirements

To run API tests, you need:

1. **cursor-agent CLI installed**
   - On Windows: Install in WSL Ubuntu
   ```bash
   wsl -d Ubuntu -e bash -c "curl https://cursor.com/install -fsS | bash"
   ```

2. **API Key configured**
   - Create file: `agile_bot/secrets/cursor_api_key.txt`
   - Add your Cursor API key to the file

## Timeout Configuration

API tests use configurable timeouts:
- **Production default:** 600 seconds (10 minutes)
- **Test default:** 30 seconds (fast operations)
- **Complex operations:** 120 seconds (complete workflows)

Adjust timeout via CLI:
```bash
python agile_bot/bots/base_bot/src/repl_cli/repl_main.py --headless --timeout 30 --message "Quick task"
```

## Test Categories

### Fast Tests (Always Run)
- `TestErrorRecovery` - Unit tests for error handling
- `TestHeadlessConfig` - Configuration loading
- `TestExecutionContext` - Context file handling
- `TestSessionLog` - Log file creation
- `TestCLIArgumentParsing` - CLI argument validation

### Slow API Tests (Skipped by Default)
- `TestExecuteDirectInstructionsViaCLI` - Pass-through message execution
- `TestExecuteSingleOperationViaCLI` - Single operation execution
- `TestExecuteCompleteActionViaCLI` - Complete action workflows
- `TestExecuteCompleteBehaviorViaCLI` - Complete behavior workflows
- `TestMonitorSessionViaCLI` - Session monitoring and logging

## CI/CD Considerations

For CI/CD pipelines:
- **PR checks:** Run fast tests only (default)
- **Nightly builds:** Run all tests including API tests with `-m ""`
- **Manual trigger:** Allow running API tests on-demand

Example CI configuration:
```yaml
# Fast tests for every commit
test-fast:
  script: pytest agile_bot/bots/base_bot/test/

# Slow tests for nightly builds
test-full:
  script: pytest agile_bot/bots/base_bot/test/ -m ""
  schedule: nightly
```

