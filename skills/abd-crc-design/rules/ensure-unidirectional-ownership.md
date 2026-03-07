---
title: ensure-unidirectional-ownership
priority: 9
---

## ensure-unidirectional-ownership

Ownership relationships must be unidirectional. If A owns B
B should not own A. References can be bidirectional
but ownership is one-way. Example: File Has blocks: Block (ownership down); Block References file: File (reference up).

**DO**

Ownership flows one-way down hierarchy
references can point any direction. Example: File Has blocks (ownership down); Block References file (reference up)

Show ownership with 'Has X' - flows down the hierarchy

```
Portfolio
```

```
    Has holdings: Holding (Portfolio owns Holdings)
```

```
Order
```

```
    Has line items: LineItem (Order owns LineItems)
```

```
File
```

```
    Has blocks: Block (File owns Blocks)
```

```
(Parent owns children - ownership flows down)
```

Show references with 'References X' - can point any direction

```
Block
```

```
    Has violations: Violation (Block owns Violations)
```

```
    References file: File (Block references its parent)
```

```
Violation
```

```
    References rule: Rule (Violation references the rule it violated)
```

```
    References block: Block (Violation references where it occurred)
```

```
(References can point up, down, or sideways)
```

Lowest component owns state
higher levels reference

```
Holding (lowest - owns its state)
```

```
    Get symbol: Symbol
```

```
    Get quantity: Quantity
```

```
    Calculates market value: Money, MarketPrice
```

```
Portfolio (higher - references holdings)
```

```
    Has holdings: Holding
```

```
    Calculates total value: Money, Holding, MarketPrice
```

```
(Holding owns Symbol/Quantity, Portfolio aggregates Holdings)
```

**DO NOT**

Don't create circular ownership or confuse ownership with references. Example: File Has blocks + Block Has file (wrong - circular) vs Block References file (right)

Don't create circular ownership (A owns B
B owns A)

```
File (WRONG: circular with Block)
```

```
    Has blocks: Block
```

```
Block (WRONG: circular with File)
```

```
    Has file: File
```

```
(Should be: File Has blocks, Block References file)
```

Don't confuse references with ownership

```
Violation (WRONG: claims ownership)
```

```
    Has rule: Rule
```

```
    Has block: Block
```

```
(Violation doesn't own Rule or Block - should be References)
```

Don't place ownership at wrong level

```
Scope (WRONG: owns violations at too high a level)
```

```
    Has violations: Violation
```

```
(Violations belong to Block or Scan, not Scope - Scope is too high)
```

Don't use bidirectional 'Has' relationships

```
Order (WRONG: bidirectional Has)
```

```
    Has customer: Customer
```

```
Customer (WRONG: bidirectional Has)
```

```
    Has orders: Order
```

```
(Should be: Customer Has orders, Order References customer)
```