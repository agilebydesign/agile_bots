---
title: background-vs-scenario-setup
priority: 4
---

## background-vs-scenario-setup

Background = shared setup for 3+ scenarios (Given/And only
no When/Then). Background steps MUST use {Concept} notation to reference domain objects. Use {Concept.property} when a specific attribute is important. Don't repeat Background in Steps.

**DO**

Use Background for shared context with {Concept} references to example tables.

Background steps use {Concept} to reference domain objects

```
Background:
```

```
  Given {User} is logged into ChannelOne 2.0
```

```
  And {User} is entitled to {Entitlement}
```

```
  And {Enterprise} has wire service enabled
```

```
Each {Concept} maps to an example table:
```

```
  {User} → User table
```

```
  {Entitlement} → Entitlement table
```

```
  {Enterprise} → Enterprise table
```

Use {Concept.property} when a specific attribute matters

```
Given {Account} with {Account.activation_status} is available
```

```
And {Recipient} with {Recipient.status} is Active
```

```
({Concept.property} highlights important attributes)
```

Use Background when 3+ scenarios share same Given steps

```
Background:
```

```
  Given {User} is logged in
```

```
  And {Character} exists
```

```
(Used by 5 scenarios - all need logged-in user with character)
```

Background contains only Given/And - state setup
no actions

```
Background:
```

```
  Given {Agent} is initialized
```

```
  And {Project} is finished initializing
```

```
(State only - no When/Then, no action verbs)
```

**DO NOT**

Don't use hardcoded values or column names in Background - use {Concept} notation. Don't include When/Then.

Don't use hardcoded values or <column_name> notation

```
WRONG - hardcoded:
```

```
  Given user is logged into ChannelOne 2.0
```

```
  And user is entitled to create wire payments
```

```
WRONG - column names:
```

```
  Given User <user_name> is logged in
```

```
  And User is entitled to <entitlement_name>
```

```
CORRECT - object references:
```

```
  Given {User} is logged into ChannelOne 2.0
```

```
  And {User} is entitled to {Entitlement}
```

Don't include actions or When/Then in Background

```
Background: Given user logs in (WRONG - 'logs in' is action)
```

```
Background: When user clicks button (WRONG - When in Background)
```

```
Background: Then system is ready (WRONG - Then in Background)
```

Don't repeat Background steps in scenario Steps

```
Background: Given {User} is logged in
```

```
Scenario: Test project
```

```
  Steps:
```

```
    Given {User} is logged in  <-- WRONG - already in Background
```

```
    When {Agent} loads project...
```