---
title: enumerate-all-ac-permutations
priority: 6
---

## enumerate-all-ac-permutations

Enumerate ALL acceptance criteria permutations. Apply exhaustive logic decomposition at AC level. Example: Valid input AC
Invalid input AC
Boundary AC
Error AC - cover all paths.

**DO**

List all validation paths and calculation branches. Example: When valid rank â†’ calculates modifier; When invalid rank â†’ shows error; When boundary rank â†’ handles edge case

Cover all validation paths explicitly

```
When user enters STR rank â†’ system validates (1-20 range)
```

```
When user enters invalid rank â†’ system shows error
```

```
When user enters valid rank â†’ system calculates modifier
```

Include happy path
error path
and edge cases

```
Happy: User submits valid form â†’ success
```

```
Error: User submits empty form â†’ validation error
```

```
Edge: User submits at boundary â†’ handles correctly
```

Cover all calculation branches

```
When rank is 10 â†’ modifier is 0
```

```
When rank is 20 â†’ modifier is +5
```

```
When rank is 1 â†’ modifier is -5
```

**DO NOT**

Don't skip AC permutations. Example: Only 'When user enters rank â†’ system saves' (missing validation and calculation ACs)

Don't skip validation paths

```
Only 'When user enters rank â†’ system saves' - MISSING: validation error AC, boundary AC
```

Don't assume happy path only

```
Only success AC without error handling - MISSING: what happens when validation fails?
```

Don't skip edge cases

```
Valid and invalid covered but no boundary conditions - MISSING: what happens at limits?
```