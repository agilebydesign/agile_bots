---
title: instructions-quality
priority: 2
---

## instructions-quality

Evaluate instruction quality across the bot/behavior/action chain. Checks for duplicated text
wordiness
vague language
and inconsistencies between instruction levels.

**DO**

Keep instructions concise
specific
and consistent across levels

Each instruction level (behavior
action
base action) should have a distinct purpose. Behavior sets context
action gives specific steps
base action provides the template.

```
Behavior: 'Create a story map capturing user journeys through epics and stories'
```

```
Action: 'Gather context for story mapping' (specific to clarify)
```

```
Base action: 'Review context, answer each question, save to clarification.json' (reusable template)
```

**DO NOT**

Do not duplicate instructions across levels or use vague language

Same instruction text repeated at behavior and action level adds noise. Vague words like 'consider'
'might'
'should probably' weaken guidance.

```
Duplicate: behavior says 'validate story structure' AND action says 'validate story structure'
```

```
Vague: 'You might want to consider checking the story names' -> 'Check each story name follows verb-noun format'
```