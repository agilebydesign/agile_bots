---
title: object-creation-and-selection
priority: 8
---

## object-creation-and-selection

Objects create themselves from their context. Factory/registry selects which implementation to use
but creation logic belongs to the object being created. Example: Order Creates from shopping cart: Order
Cart
Customer; ScannerRegistry Finds scanner for rule: Scanner
Rule.

**DO**

Objects create themselves
factory/registry selects implementations. Example: Order Creates from cart: Order
Cart
Customer (self-creation); ScannerRegistry Finds scanner: Scanner
Rule (selection)

Objects know how to create themselves from context

```
Order
```

```
    Creates from shopping cart: Order, Cart, Customer
```

```
    Creates from quote: Order, Quote, Customer
```

```
Trade
```

```
    Creates from rebalance recommendation: Trade, RebalanceRecommendation, Portfolio
```

```
    Creates from manual request: Trade, Symbol, Shares, TradeType
```

```
(Order and Trade know how to create themselves from different contexts)
```

Use factory/registry to select which implementation to use

```
ScannerRegistry
```

```
    Finds scanner for rule: Scanner, Rule
```

```
ImportPlacementScanner : Scanner
```

```
    Creates to scan scope: ImportPlacementScanner, Scope, Rule (self-creation)
```

```
    Scans imports: Violation, Block, ImportRules
```

```
(Registry selects which scanner, scanner creates itself)
```

Factory returns base type
caller uses polymorphically

```
ShippingCalculatorFactory
```

```
    Selects calculator for destination: ShippingCalculator, Destination
```

```
DomesticShippingCalculator : ShippingCalculator
```

```
    Calculates rate: Money, Weight, Distance
```

```
InternationalShippingCalculator : ShippingCalculator
```

```
    Calculates rate: Money, Weight, Country, CustomsFees
```

```
(Factory returns base type, caller doesn't know which implementation)
```

**DO NOT**

Don't delegate creation to other objects
don't hardcode type selection. Example: Cart Creates order (wrong) vs Order Creates from cart (right); Factory Creates scanner (wrong) vs Registry Finds scanner (right)

Don't have other objects create domain objects

```
Cart (WRONG: creates Order)
```

```
    Creates order: Order, Customer
```

```
Rule (WRONG: creates Violation)
```

```
    Creates violation: Violation, Block
```

```
(Order should create itself from Cart, Violation should create itself from Rule)
```

Don't have factory create objects - it selects
objects create themselves

```
ScannerFactory (WRONG: creates instead of selects)
```

```
    Creates import scanner: ImportPlacementScanner, Scope
```

```
    Creates naming scanner: NamingScanner, Scope
```

```
(Should be: Registry finds scanner, scanner creates itself)
```

Don't hardcode type selection in calling code

```
ScanOrchestrator (WRONG: hardcoded selection)
```

```
    Scans with import scanner: Violation, ImportPlacementScanner
```

```
    Scans with naming scanner: Violation, NamingScanner
```

```
(Should use factory to select, orchestrator uses base Scanner type)
```

Don't list all implementations in parent relationships

```
PaymentProcessor (WRONG: lists all implementations)
```

```
    Processes payment: Result, StripeGateway, PayPalGateway, SquareGateway
```

```
(Should use factory to select, processor uses base PaymentGateway type)
```