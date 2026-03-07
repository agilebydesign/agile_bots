---
title: stories-have-4-to-9-acceptance-criteria
priority: 2
---

## stories-have-4-to-9-acceptance-criteria

Stories should have 4-9 acceptance criteria. Fewer than 4 suggests incomplete exploration; more than 9 suggests story is too large and should be split. Example: Story with 6 AC (right-sized)
Story with 2 AC (under-explored)
Story with 15 AC (too large).

**DO**

Target 4-9 acceptance criteria per story. Example: Story with 5-7 AC covers happy path
edge cases
and error conditions

Include enough AC to cover the behavior completely

```
Story with 6 AC: happy path, validation error, authorization check, edge case, alternate flow, confirmation
```

Split stories that exceed 9 AC into smaller stories

```
Story with 12 AC split into: Story A (6 AC for core flow) + Story B (6 AC for advanced features)
```

Expand stories with fewer than 4 AC to cover missing cases

```
Story with 2 AC expanded to 5 AC by adding error handling, edge cases, and validation
```

**DO NOT**

Don't leave stories under-explored (<4 AC) or oversized (>9 AC). Example: Story with 2 AC (missing cases) or Story with 15 AC (too large)

Don't accept stories with fewer than 4 acceptance criteria

```
Story with only 2 AC: 'User logs in', 'System shows dashboard' (missing error cases, validation, edge cases)
```

Don't create stories with more than 9 acceptance criteria

```
Story with 15 AC covering login, profile, settings, notifications (should be 2-3 separate stories)
```

Don't count trivial or redundant AC to meet the minimum

```
Padding with 'System displays page', 'Page loads successfully' (not meaningful AC)
```