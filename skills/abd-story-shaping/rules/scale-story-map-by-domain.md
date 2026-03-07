---
title: scale-story-map-by-domain
priority: 10
---

## scale-story-map-by-domain

Scaling concern: at small scale
domain objects with similar behavior can live together in a single sub-epic. As domain objects develop distinct behavior
break out by domain into parallel sub-epics with consistent stories under each. Domain First
Operation Second. After expanding stories per review_and_expand_stories
organize the resulting stories by domain
not by technology layer.

**DO**

At small scale keep domains together. As complexity grows
break out by domain with consistent stories. Domain First
Operation Second.

At small scale
keep related domain objects together

```
Single sub-epic 'Process Payment' with stories covering wire, ACH, and check together
```

```
Fine when there are only a few stories and the behavior is similar
```

```
Single sub-epic 'Render Diagram' covering epics, stories, and increments -- fine when each has 1-2 simple stories
```

As complexity grows
break out by domain with consistent stories under each

```
'Make Wire Payment', 'Make ACH Payment', 'Make Check Payment' as parallel sub-epics
```

```
Each has consistent stories: Collect Recipient Info, Validate Payment, Submit Payment
```

```
Plus unique stories where the domain demands it: Wire: Validate Intermediary Bank; ACH: Validate Routing Number
```

```
Signal to break out: domain objects have different behavior that makes shared stories confusing or untestable
```

When scaling
organize Domain First
Operation Second

```
Primary axis is the domain object (wire, ACH, check)
```

```
Operations (collect, validate, submit) are stories within each
```

```
This keeps related domain logic together instead of scattering it across operation-based groupings
```

After expanding stories (per review_and_expand_stories)
organize by domain

```
First expand a story into system/component interactions (per review_and_expand_stories)
```

```
Then group the expanded stories under domain-specific sub-epics -- not under technology-layer sub-epics
```

**DO NOT**

When scaling
do not group by operation or technology. Do not force the break-out prematurely.

When scaling
do not group by operation or technology

```
Sub-epic 'Validate All Payments' with stories for wire, ACH, and check mixed in -- groups by operation, not domain
```

```
Sub-epic 'Database Operations' with stories for saving wire, ACH, and check data -- groups by technology layer
```

Do not force the break-out prematurely

```
Creating 5 sub-epics when you only have 3 stories total -- keep them together until complexity demands separation
```

```
Naming sub-epics as bare nouns: 'Wire Transfer' -- still needs the operation verb: 'Make Wire Payment'
```