---
title: use-but-for-negative-conditions
priority: 9
---

## use-but-for-negative-conditions

Use BUT to explicitly state negative conditions and constraints. When system prevents an action
validates a boundary
or enforces a rule
use BUT to state what does NOT happen. Example: WHEN invalid input THEN error AND returns message BUT does not save data.

**DO**

Add BUT clause to show what system prevents or does not do. Makes constraints explicit.

Use BUT to show what the system prevents

```
WHEN SubEpic creates Sub-Epic that has Stories children
```

```
THEN SubEpic identifies SubEpic already contains Stories
```

```
AND returns error indicating cannot create SubEpic under SubEpic with Stories
```

```
BUT prevents create operation
```

Use BUT to show what does not happen in error cases

```
WHEN User submits invalid form
```

```
THEN System validates input
```

```
AND System shows validation errors
```

```
BUT does not save data
```

Use BUT to clarify collection separation

```
WHEN Story creates Scenario
```

```
THEN Story adds Scenario to common scenario child collection
```

```
BUT Story does not add Scenario to acceptance criteria child collection
```

Use BUT to show boundary enforcement

```
WHEN User drags node over incompatible parent
```

```
THEN Panel shows no-drop cursor
```

```
BUT does not allow drop operation
```

**DO NOT**

Don't leave negative conditions implicit. Example: Don't say 'returns error' without stating what the system does NOT do

Don't omit the constraint being enforced

```
WHEN SubEpic creates Sub-Epic that has Stories
```

```
THEN SubEpic identifies SubEpic already contains Stories
```

```
AND returns error
```

Don't leave side effects unclear in error cases

```
WHEN validation fails
```

```
THEN System shows error message
```

Don't assume constraints are obvious

```
WHEN Story creates Scenario
```

```
THEN Story adds Scenario to scenario collection
```