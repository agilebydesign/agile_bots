---
title: use-atomic-acceptance-criteria
priority: 7
---

## use-atomic-acceptance-criteria

Write atomic acceptance criteria. Avoid repeating common WHEN/THEN/AND blocks across multiple AC. State general case once
then only state what differs in variations. Example: WHEN node moves â†’ general behavior
WHEN position specified â†’ only state position difference.

**DO**

Write one AC for general case
additional AC only state what changes. Example: WHEN moves â†’ removes/adds/resequences; WHEN position specified â†’ adds at position instead of last

State general behavior once in first acceptance criteria

```
THEN node removes itself from current parent
```

```
AND node adds itself to target parent as last child
```

```
AND resequences siblings
```

Variations only state what differs from general case

```
WHEN position is specified
```

```
THEN node adds itself at specified position instead of last
```

Edge cases state only the edge behavior

```
WHEN position exceeds children count
```

```
THEN position adjusts to last
```

Use 'see previous' only when unavoidable - should be rare

```
WHEN User enters dot notation with position
```

```
THEN CLI parses dot notation and position parameter
```

```
AND resolves parent and child nodes [see previous acceptance criteria]
```

**DO NOT**

Don't repeat common WHEN/THEN/AND blocks. Example: Don't have 4 AC that all say 'removes from parent
adds to target
resequences' with slight variations

Don't repeat the same base logic across multiple acceptance criteria

```
THEN node removes itself from current parent
```

```
AND node adds itself to target parent as last child
```

```
AND resequences siblings
```

```
THEN node removes itself from current parent
```

```
AND node adds itself to target parent at specified position
```

```
AND resequences all children
```

```
THEN node removes itself from current parent
```

```
AND adjusts position to last
```

```
AND moves node to adjusted position
```

```
AND resequences siblings
```

Don't make variations repeat the full acceptance criteria

```
WHEN position specified
```

```
THEN node removes from parent
```

```
AND node adds at position
```

```
AND resequences all children
```