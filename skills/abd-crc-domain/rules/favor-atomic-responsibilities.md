---
title: favor-atomic-responsibilities
priority: 6
---

## favor-atomic-responsibilities

Favor atomic responsibilities: one responsibility = one behavior. Describe what the concept does (verbs)
not outcomes it prevents. Use noun phrases for property access
verb phrases for behaviors.

**DO**

Keep responsibilities atomic and behavior-focused

One responsibility = one behavior. Do not pack multiple conditions (on X
Y
or Z) into a single responsibility.

```
Lock (CORRECT)
```

```
    Acquires lock for voucher: Voucher, TimeStamp
```

```
    is Locked at a Time: TimeStamp
```

```
    expires Lock: TimeStamp, Lock Duration
```

```
    Releases lock for Voucher: Voucher
```

```
Lock (WRONG)
```

```
    Releases lock on unlock, redemption complete, or timeout: Voucher
```

```
(Split into separate responsibilities: Acquires, expires, Releases)
```

Describe behavior (what it does)
not outcome (what it prevents). Use verbs like Acquires
Releases
expires.

```
Lock (CORRECT)
```

```
    Acquires lock for voucher: Voucher, TimeStamp
```

```
    Releases lock for Voucher: Voucher
```

```
Lock (WRONG)
```

```
    Prevents concurrent redemption of same voucher: Voucher
```

```
    Issues lock token: String
```

```
(Prevents/Issues describe outcomes; Acquires/Releases describe behavior)
```

Use noun phrases for property access (Get/Find)
verb phrases for behaviors that perform actions.

```
Order (resource)
```

```
    Get order id: OrderId (property access - noun phrase)
```

```
    Get line items: LineItem (property access - noun phrase)
```

```
    Calculates total with taxes: Money, TaxRate (behavior - verb phrase)
```

```
    Validates inventory availability: LineItem, InventoryService (behavior - verb phrase)
```

```
(Property access = noun phrases. Behaviors = verb phrases describing actions)
```

**DO NOT**

Don't pack responsibilities or describe outcomes instead of behavior

Don't pack multiple conditions into one responsibility (on X
Y
or Z).

```
Releases lock on unlock, redemption complete, or timeout: Voucher (WRONG)
```

```
Split into: Acquires lock, expires Lock, Releases lock for Voucher
```

Don't use outcome phrasing (Prevents
Issues) when behavior phrasing is clearer.

```
Prevents concurrent redemption of same voucher: Voucher (WRONG)
```

```
Issues lock token: String (WRONG)
```

```
Use: Acquires lock for voucher, is Locked at a Time
```