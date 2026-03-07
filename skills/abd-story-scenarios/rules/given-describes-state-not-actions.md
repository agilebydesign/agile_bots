---
title: given-describes-state-not-actions
priority: 3
---

## given-describes-state-not-actions

Given statements describe STATE/PRECONDITIONS
not actions or functionality. Given = what exists before test. When = first action. Then = expected behavior. Example: Given user is logged in (state)
not Given user logs in (action).

**DO**

Given describes state/preconditions only. Example: 'Given user is logged in' (state)
'Given character sheet exists' (precondition)

Use state language - what EXISTS
not what HAPPENS

```
Given user is logged in
```

```
Given character sheet exists
```

```
Given workflow state is persisted
```

```
Given bot has behavior configured as 'shape'
```

First action is always When
never Given

```
Given bot is configured (STATE)
```

```
When Tool invokes method (ACTION)
```

```
Then Action loads instructions (OUTCOME)
```

Preconditions describe what's true BEFORE the action

```
Given activity log is initialized (precondition)
```

```
When action completes (trigger)
```

```
Then activity log captures data (functionality being tested)
```

**DO NOT**

Don't describe actions
UI navigation
or functionality in Given. Example: 'Given user logs in' (action - wrong)
'Given User is on PaymentDetails step' (navigation - wrong)

Don't use action verbs in Given - clicking
sending
calling are When actions

```
Given user clicks button (WRONG)
```

```
Given system sends message (WRONG)
```

```
Given API is called (WRONG)
```

```
Given tool executes (WRONG)
```

Don't describe UI position/navigation as state - 'is on page' is navigation
not domain state

```
Given User is on PaymentDetails step (WRONG - navigation, not state)
```

```
Given User is viewing the form (WRONG - UI position)
```

```
Given User is at Step 2 (WRONG - navigation position)
```

```
CORRECT: Given {WirePayment} creation is in progress
```

```
CORRECT: Given {PaymentDetails} requires {Account} selection
```

```
CORRECT: Given {User} has initiated {WirePayment} with {Recipient}
```

Don't describe functionality being tested in Given - that's what Then is for

```
Given activity log tracks: timestamp, action_state (WRONG - this is functionality to test in Then)
```

Don't use past tense actions in Given

```
Given Tool has invoked method (WRONG - 'invoked' is action)
```

```
Given user has clicked (WRONG - 'clicked' is action)
```