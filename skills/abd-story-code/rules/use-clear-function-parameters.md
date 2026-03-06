---
title: use-clear-function-parameters
priority: 99
---

## use-clear-function-parameters

CRITICAL: Function signatures must be simple and intention-revealing. Prefer 0-2 parameters. NEVER pass Dict[str
Any] or List[str] for complex data - create typed objects instead. Examples: parameters dict → ParametersObject
files dict → FilesCollection
exclude list → ExcludePatterns.