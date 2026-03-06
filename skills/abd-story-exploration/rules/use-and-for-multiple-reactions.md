---
title: use-and-for-multiple-reactions
priority: 4
---

## use-and-for-multiple-reactions

Use 'And' to chain multiple system reactions to a single event. When system responds with more than one action
connect them with And. Example: When user submits â†’ Then system validates And system saves And system sends notification.

**DO**

Chain multiple reactions with And. Example: Then system validates And system saves And system notifies

Use And to connect multiple system reactions to one user action

```
When user submits order
```

```
Then system validates payment
```

```
And system reserves inventory
```

```
And system sends confirmation email
```

Group related system reactions together

```
When user clicks save
```

```
Then system validates data
```

```
And system persists changes
```

```
And system displays success message
```

Keep And chains to 2-4 reactions for readability

```
Then system processes request
```

```
And system updates status
```

```
And system notifies user
```

**DO NOT**

Don't write separate When/Then for each system reaction. Example: When user submits / Then system validates / When system validates / Then system saves (wrong)

Don't create separate Given/When/Then blocks for sequential system actions

```
When user submits
```

```
Then system validates
```

```
When system validates
```

```
Then system saves - WRONG: should use And system saves
```

Don't have excessively long And chains (more than 4 reactions)

```
Then system does A And B And C And D And E And F - TOO MANY: split into separate scenarios or steps
```