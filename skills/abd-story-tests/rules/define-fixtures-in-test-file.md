---
title: define-fixtures-in-test-file
priority: 10
---

## define-fixtures-in-test-file

Define fixtures in the test file
not separate conftest.py. Truly reusable fixtures (file ops
location helpers) go in base conftest.py. Example: @pytest.fixture def workspace_root(tmp_path): return tmp_path / 'workspace'

**DO**

Define fixtures in same test file. Example: @pytest.fixture def config_file(tmp_path): ... (in test_agent.py)

Define fixtures in the test file that uses them

```
# In test_agent_configuration.py
```

```
@pytest.fixture
```

```
def workspace_root(tmp_path):
```

```
    workspace = tmp_path / 'workspace'; workspace.mkdir(); return workspace
```

Fixtures can depend on other fixtures

```
@pytest.fixture
```

```
def config_file(workspace_root):
```

```
    path = workspace_root / 'config.json'; path.write_text('{}'); return path
```

Truly reusable fixtures go in base conftest.py

```
# In agents/base/src/conftest.py (for reuse across all tests)
```

```
@pytest.fixture
```

```
def repo_root(): return Path(__file__).parent.parent.parent
```

**DO NOT**

Don't create separate conftest.py for agent-specific fixtures. Don't create shared files without explicit need.

Don't create conftest.py for single-test-file fixtures

```
# WRONG: src/conftest.py with fixtures only used by one test file
```

Don't put agent-specific fixtures in shared conftest

```
# WRONG: Base conftest with StoryBot-specific fixtures
```

Don't create shared fixture files without explicit need. If a fixture is only used in one file
keep it there. When you have obvious shared logic across sub-epics
place the shared base at the appropriate hierarchy level: sub-epic level helper if shared within one sub-epic
epic level helper if shared across sub-epics. This is not an excuse to create shared files preemptively.

```
# WRONG: Creating test_helpers/payment_base.py when only test_make_wire_payment.py uses it
```

```
# RIGHT: Keep fixtures in test_make_wire_payment.py until test_make_ach_payment.py also needs them
```

```
# RIGHT: When both wire and ACH test files need create_recipient(), move it to epic-level helper
```

```
# RIGHT: Sub-epic level helper if shared within one sub-epic, epic level if shared across sub-epics
```