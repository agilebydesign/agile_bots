---
title: keep-acceptance-criteria-consistent-across-connected-domains
priority: 2
---

## keep-acceptance-criteria-consistent-across-connected-domains

Scaling concern: at small scale
AC can cover multiple domain objects together. As domain objects develop distinct behavior
keep AC consistent in structure across connected domains. AC crossing multiple domain behaviors is a signal to split the story.

**DO**

At small scale keep AC together. As you scale
scope AC to one domain and keep structure consistent across connected domains.

At small scale
AC covering multiple domain objects together is acceptable

```
When user submits payment then system validates and routes -- covering wire and ACH together
```

```
Fine when each has simple, similar validation
```

```
A couple of AC per domain object in a shared story is manageable
```

As domain objects develop distinct behavior
write AC scoped to one domain

```
When user submits wire payment then system validates intermediary bank and routes to wire rail -- one payment type, one flow
```

```
When user submits ACH payment then system validates routing number and routes to ACH rail -- same pattern, scoped to ACH
```

```
When wire payment requires intermediary bank then system validates SWIFT code -- unique behavior, explicitly scoped to wire
```

Keep AC consistent in structure across connected domains

```
Wire and ACH stories both have AC following the same pattern: When user submits [type] payment then system validates [type-specific field] and routes to [type] rail
```

```
Same number of AC covering the same operations, with domain-specific details as the only variation
```

AC crossing multiple domains is the signal to split the story

```
If you find an AC mentioning both wire validation AND ACH routing, that story needs splitting into two -- one per payment type
```

**DO NOT**

When scaling
do not write AC that mixes domain behaviors or write inconsistent AC across connected domains.

When scaling
do not write AC that mixes domain object behaviors

```
When user submits payment then system validates wire rules AND ACH rules AND check rules -- too broad when each has distinct validation
```

```
When payment completes then wire gets confirmation AND ACH gets receipt AND check gets tracking number -- mixing 3 domains' outcomes in one AC
```

Do not write inconsistent AC across connected domains

```
Wire story has 5 detailed AC covering every validation step, ACH story has 1 vague AC -- keep the depth and structure parallel
```