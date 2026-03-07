---
title: enumerate-all-stories-explicitly
priority: 10
---

## enumerate-all-stories-explicitly

Enumerate ALL stories for increment(s) in focus explicitly (no ~X stories notation). Use story counts (~X stories) only for other increments. When applying new approach (System stories
component interactions)
MUST expand existing stories into component-level stories.

**DO**

List all stories explicitly for focus increment
including newly expanded stories

Explicitly enumerate every story in the focus increment with full story names

```
Increment 1 (FOCUS):
```

```
  - User enters character name
```

```
  - User assigns strength ability
```

```
  - User assigns dexterity ability
```

```
  - System validates ability scores
```

```
  - System calculates ability modifiers
```

```
  - User saves character
```

```
  - System stores character to file
```

```
  - User views character sheet
```

```
Increment 2: ~15 stories (not in focus, use count)
```

When new approach requires component interactions
expand stories from user actions into system/component stories

```
Original: 'Group tokens from canvas into mob' (1 story)
```

```
Expanded with System approach:
```

```
  - User groups tokens from canvas into mob (user action)
```

```
  - Mob manager creates mob with selected tokens (system)
```

```
  - System assigns leader randomly (system)
```

```
(1 story expanded to 3 stories showing component interactions)
```

Story count WILL increase when expanding for component-level granularity

```
Original approach: 8 user stories
```

```
After System/component approach: 23 stories
```

```
  - Original user action stories: 8
```

```
  - New system component stories: 15
```

```
(Expected increase when showing component interactions explicitly)
```

**DO NOT**

Don't use ~X notation for focus increment or keep original stories without expansion

Don't use story count notation (~X stories) for the focus increment

```
Increment 1 (FOCUS): ~8 stories (WRONG: should list all stories explicitly)
```

```
Should be: Increment 1 (FOCUS): User enters name, User assigns strength, User assigns dexterity, ... (all listed)
```

Don't keep original stories without expansion when new approach requires component-level detail

```
Keeping: 'Group tokens from canvas into mob' as single story
```

```
WRONG when System approach requires component interactions
```

```
Should expand to: User groups tokens (user), Mob manager creates mob (system), System assigns leader (system)
```