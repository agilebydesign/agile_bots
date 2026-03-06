---
title: place-imports-at-top
priority: 15
---

## place-imports-at-top

Place all imports at top of test file
after docstrings
before code. Group: stdlib
third-party
then local. Example: import json; import pytest; from mymodule import MyClass

**DO**

All imports at top
grouped by type. Example: import json; import pytest; from agile_bot.bots... import X

Place all imports at top after docstring

```
'''Test module docstring.'''
```

```
import pytest
```

```
from pathlib import Path
```

```
from agile_bot.bots.base_bot... import ClarifyAction
```

Group imports: stdlib
third-party
local

```
# Standard library
```

```
import json
```

```
from pathlib import Path
```

```
# Third-party
```

```
import pytest
```

```
# Local
```

```
from agile_bot... import MyClass
```

**DO NOT**

Don't place imports inside functions or after code. Example: def test(): from pathlib import Path (wrong - import inside function)

Don't import inside test functions

```
def test_something():
```

```
    from pathlib import Path  # WRONG - put at top of file
```

Don't place imports after code

```
@pytest.fixture
```

```
def fixture(): pass
```

```
import pytest  # WRONG - should be at top
```

Don't mix import groups randomly

```
import json
```

```
from agile_bot... import X  # WRONG - local before third-party
```

```
import pytest
```