---
title: use-scenario-outline-when-needed
priority: 6
---

## use-scenario-outline-when-needed

Use Scenario Outline with Examples when story warrants concrete data: formulas need validation
domain has named entities
parameter variations exist. Example: Calculate ability modifier with Examples table Rank 10→0
Rank 12→+1
Rank 14→+2.

**DO**

Scenario Outline for formulas
domain entities
or data variations. Example: Scenario Outline: Calculate modifier with Examples table showing input→output pairs

Use for formula validation with concrete values

```
Scenario Outline: Calculate ability modifier - Examples: | Rank | Modifier | | 10 | 0 | | 12 | +1 | | 14 | +2 |
```

Use for domain entities with named variations

```
Scenario Outline: Process payment - Examples: | Payment Type | Fee | | credit_card | 2.9% | | bank_transfer | 0.5% |
```

**DO NOT**

Don't use Scenario Outline for simple behaviors. Example: Scenario Outline: User clicks button (too simple - use regular scenario)

Don't use Outline for single-case scenarios

```
Scenario Outline: User clicks button (WRONG - too simple, no data variations)
```

Don't use Outline when there's only one example

```
Scenario Outline with Examples table having only 1 row - just use regular Scenario
```