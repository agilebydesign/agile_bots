---
title: consolidate-superficial-stories
priority: 13
---

## consolidate-superficial-stories

Consolidate similar stories that differ superficially. When multiple stories use the same logic and only differ in data values or enumeration
combine them into a single parameterized story. NOTE: This rule operates on a different axis than P14 (Expand System Stories). P13 eliminates data-value duplication (same behavior
different input values). P14 decomposes by system component interactions (different behaviors within one story). Apply P13 first to consolidate data variations
then apply P14 to expand the consolidated story by component behavior if needed.

**DO**

Identify and consolidate stories that differ only superficially (data values
enumeration)

Consolidate stories that use the same validation logic but differ only in the specific value being validated

```
Before consolidation:
```

```
  - User assigns strength ability
```

```
  - User assigns dexterity ability
```

```
  - User assigns constitution ability
```

```
  - User assigns intelligence ability
```

```
  - User assigns wisdom ability
```

```
  - User assigns charisma ability
```

```
After consolidation:
```

```
  - User assigns ability (STR, DEX, CON, INT, WIS, CHA)
```

```
(Same validation logic, different data values)
```

Consolidate stories that use the same calculation formula but differ only in which attribute is being calculated

```
Before consolidation:
```

```
  - System calculates strength modifier
```

```
  - System calculates dexterity modifier
```

```
  - System calculates constitution modifier
```

```
After consolidation:
```

```
  - System calculates ability modifiers
```

```
(Same calculation formula applied to different attributes)
```

Consolidate stories that perform the same operation on different entity types

```
Before consolidation:
```

```
  - User creates character
```

```
  - User creates weapon
```

```
  - User creates armor
```

```
  - User creates spell
```

```
After consolidation:
```

```
  - User creates game entity (character, weapon, armor, spell)
```

```
(Same creation operation, different entity types)
```

**DO NOT**

Don't keep stories separate when they differ only superficially

Don't enumerate every permutation when the logic is identical and only the data value changes

```
WRONG: Keep separate stories for each attribute:
```

```
  - User validates email format
```

```
  - User validates phone format
```

```
  - User validates postal code format
```

```
RIGHT: Consolidate to single story:
```

```
  - User validates input format (email, phone, postal code)
```

Don't split stories by data value when the business logic and validation rules are the same

```
WRONG: Separate story for each product type:
```

```
  - User adds book to cart
```

```
  - User adds electronics to cart
```

```
  - User adds clothing to cart
```

```
RIGHT: Single parameterized story:
```

```
  - User adds product to cart (book, electronics, clothing)
```

Don't create separate stories for each status transition when they follow the same workflow pattern

```
WRONG: One story per status:
```

```
  - User changes order to pending
```

```
  - User changes order to processing
```

```
  - User changes order to shipped
```

```
  - User changes order to delivered
```

```
RIGHT: Single workflow story:
```

```
  - User updates order status (pending, processing, shipped, delivered)
```