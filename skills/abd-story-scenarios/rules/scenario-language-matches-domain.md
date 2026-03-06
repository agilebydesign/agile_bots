---
title: scenario-language-matches-domain
priority: 1
---

## scenario-language-matches-domain

Scenario language MUST use domain concept terminology. Given/When/Then steps should reference domain entities and concepts
not UI elements or technical implementation details.

**DO**

Use domain language in scenario steps - reference domain concepts by name.

Reference domain concepts in Given steps (state
not actions)

```
DOMAIN MODEL:
```

```
  Enterprise (enterprise_id, name)
```

```
    └── User (user_id, name, role)
```

```
    └── Recipient (recipient_id, name, bank_info)
```

```
Given an Enterprise with active Recipients
```

```
And a User with wire payment permissions
```

Reference domain concepts in When steps (domain actions)

```
When the User selects a Recipient
```

```
And enters the PaymentAmount
```

Reference domain concepts in Then steps (domain outcomes)

```
Then the WirePayment is created with status pending
```

```
And the Recipient receives notification
```

**DO NOT**

Don't use UI element names
technical implementation terms
or generic words instead of domain concepts.

Don't use UI/technical terms in Given steps

```
Given the recipient list page is loaded
```

```
Given the user has clicked the wire button
```

```
Given the dropdown shows recipients
```

Don't use UI actions on UI elements in When steps

```
When the user clicks the dropdown
```

```
And types in the input field
```

```
When user clicks the table row
```

Don't use UI verification in Then steps

```
Then the success message is displayed
```

```
And the green checkmark appears
```

```
Then the modal displays account info
```

Don't use generic terms when domain concepts exist

```
Given the user has items
```

```
When they select an item
```

```
Then the thing is processed
```

Don't use the wrong domain concept for the context. When multiple concepts represent the same entity in different contexts
use the one that matches where the entity actually lives.

```
WRONG - DrawIOEpic is a diagram cell, but this entity lives in the StoryMap:
```

```
  Given {DrawIOEpic} exists in {StoryMap}  (an Epic exists in StoryMap, not a DrawIOEpic)
```

```
  And {DrawIOSubEpic} exists under {DrawIOEpic}  (SubEpic under Epic in the StoryMap)
```

```
CORRECT - use the concept that matches where it lives:
```

```
  Given {Epic} exists in {StoryMap}  (Epic is a StoryMap entity)
```

```
  And {SubEpic} exists under {Epic}  (SubEpic is a StoryMap entity)
```

```
  ...
```

```
  Then {DrawIOEpic} cells are rendered  (DrawIOEpic is the diagram representation)
```

Don't use abstract descriptions when concrete {Concept.property} references are available. If the table has the specific values
reference them.

```
WRONG - vague, abstracts away what's actually configured/derived:
```

```
  And {DrawIOStoryMap} is configured for rendering
```

```
  And {DrawIOStoryMap} exists with content derived from {StoryMap}
```

```
CORRECT - reference the concrete property or state:
```

```
  And {DrawIOStoryMap} is configured with {DrawIOStoryMap.diagram_type}
```

```
  And {DrawIOStoryMap} has been rendered from {StoryMap}
```