---
title: review-and-expand-stories
priority: 14
---

## review-and-expand-stories

Review and expand stories based on new approach granularity. When planning decisions specify 'System stories' or detailed component interactions
MUST break down existing stories into component-interaction stories. The story count WILL increase. NOTE: This rule operates on a different axis than P13 (Consolidate Superficial Stories). P14 decomposes by system component behavior (different behaviors within one story). P13 eliminates data-value duplication (same behavior
different input values). Apply P13 first to consolidate data variations
then apply P14 to expand by component behavior.

**DO**

Break down stories into component interactions when System or Technology or Infrastructure approach is selected

When System/Technology/Infrastructure approach is chosen
expand user action stories into user + system component stories

```
Original: 'Group tokens from canvas into mob' (1 user story)
```

```
Expanded with System/ Technology/Infrastructure approach (3 stories):
```

```
  1. User groups tokens from canvas into mob (user action)
```

```
  2. Mob manager creates mob with all selected tokens (system/component)
```

```
  3. System assigns leader randomly (system/component)
```

```
Story count increased from 1 to 3
```

Review existing stories and identify where component interactions need to be made explicit

```
Original: 'User submits order' (1 story)
```

```
Expanded with System/ Technology/ Infrastructure approach (4 stories):
```

```
  1. User submits order with items (user action)
```

```
  2. Order validator validates order details (system)
```

```
  3. Inventory manager reserves items (system)
```

```
  4. System generates order confirmation (system)
```

```
Story count increased from 1 to 4
```

Break down payment and processing flows into discrete system component steps

```
Original: 'User pays for order' (1 story)
```

```
Expanded with System approach (5 stories):
```

```
  1. User enters payment information (user action)
```

```
  2. Payment validator validates payment details (system)
```

```
  3. Payment gateway processes transaction (system)
```

```
  4. Transaction recorder saves payment (system)
```

```
  5. System displays payment confirmation (system)
```

```
Story count increased from 1 to 5
```

**DO NOT**

Don't keep original stories without expansion when new approach requires component-level detail

Don't keep single user story when System approach requires showing component interactions

```
Keeping: 'Group tokens from canvas into mob' as single story
```

```
WRONG when System approach selected
```

```
Should expand to show: User action + Mob manager creates mob + System assigns leader
```

Don't assume story count stays the same when changing granularity approach

```
Planning says: 'Use System approach for component interactions'
```

```
Original count: 8 user stories
```

```
WRONG: Keep count at 8 stories
```

```
RIGHT: Expand to ~20-24 stories showing user actions + system components
```