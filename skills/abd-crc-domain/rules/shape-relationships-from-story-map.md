---
title: shape-relationships-from-story-map
priority: 11
---

## shape-relationships-from-story-map

Shape domain concept relationships from the story map. Collaborators should come from stories showing how concepts work together to accomplish user goals.

**DO**

Derive collaborators from story interactions

Identify collaborators from stories showing how concepts interact to deliver value

```
Story: User rebalances portfolio to target allocation
```

```
Derived concepts:
```

```
RebalanceRecommendation
```

```
    Generates trades to achieve target allocation: Trade, Portfolio, TargetAllocation
```

```
    Compares current allocation to target: AllocationDifference, Portfolio, TargetAllocation
```

```
Portfolio
```

```
    Get holdings: Holding
```

```
    Calculates current allocation: Allocation, Holding
```

```
(Collaborators Portfolio, TargetAllocation, Trade, AllocationDifference come from story)
```

**DO NOT**

Don't invent collaborators not present in stories

Don't add collaborators that aren't implied by the stories

```
Story: User creates order
```

```
Order
```

```
    Get audit log: AuditLog (WRONG: not in story)
```

```
    Get version history: Version (WRONG: not in story)
```

```
(Audit, versioning not mentioned in stories - don't add)
```