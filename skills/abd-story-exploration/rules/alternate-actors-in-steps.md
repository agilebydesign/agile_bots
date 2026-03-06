---
title: alternate-actors-in-steps
priority: 3
---

## alternate-actors-in-steps

Alternate between actors every 1-2 steps. Scenarios should show back-and-forth interaction between user and system. Example: When user submits â†’ Then system validates â†’ When system displays â†’ Then user confirms.

**DO**

Alternate actors every 1-2 steps to show interaction flow. Example: When user â†’ Then system; When system â†’ Then actor

When actor acts
system responds

```
When user submits order
```

```
Then system validates payment
```

When system completes
actor reacts or system continues briefly

```
When system displays confirmation
```

```
Then user reviews details
```

System can chain 1-2 sequential actions before returning to actor

```
When user submits form
```

```
Then system validates input
```

```
And system saves data
```

```
When system displays result
```

```
Then user confirms
```

**DO NOT**

Don't have long runs of same actor without switching. Example: 5 consecutive 'system does X' steps without user interaction

Don't have more than 2 consecutive steps from same actor

```
Then system validates (1)
```

```
And system processes (2)
```

```
And system stores (3)
```

```
And system notifies (4) - TOO MANY consecutive system steps
```

Don't write scenarios where user acts multiple times without system response

```
When user enters name
```

```
And user enters email
```

```
And user enters password
```

```
And user clicks submit - should have system validation between steps
```