---
title: encapsulate-through-properties
priority: 5
---

## encapsulate-through-properties

Objects internalize their own state and functionality
accessed through properties. Avoid methods that receive external state the object should already own. Example: LineItem owns Product/Quantity
so Calculates extended price: Money
Discount (not Money
Product
Quantity
Discount).

**DO**

Objects own their state and expose it through properties. Example: LineItem owns Product/Quantity
Calculates extended price: Money
Discount (uses internal state)

Objects internalize state they need and expose through properties - callers don't pass that state back

```
LineItem (owns Product and Quantity as internal state)
```

```
    Get product: Product (property access)
```

```
    Get quantity: Quantity (property access)
```

```
    Calculates extended price: Money, Discount (uses internal state, only needs external Discount)
```

```
Holding (owns Symbol and Quantity as internal state)
```

```
    Get symbol: Symbol (property access)
```

```
    Get quantity: Quantity (property access)
```

```
    Calculates market value: Money, MarketPrice (uses internal state, only needs external price)
```

```
(Objects use their own internalized state, only receive what they don't own)
```

Hide internal representation behind clean property interface

```
Portfolio
```

```
    Get holdings: Holding (hides how holdings are stored)
```

```
    Calculates total value: Money, MarketPrice (hides internal aggregation)
```

```
Order
```

```
    Get line items: LineItem (hides collection type)
```

```
    Calculates subtotal: Money (hides iteration and calculation)
```

```
(Callers don't know if holdings are List, Array, Dictionary internally)
```

Use properties where state access makes sense
methods for complex behaviors

```
Trade
```

```
    Get symbol: Symbol (property - simple state)
```

```
    Get shares: Shares (property - simple state)
```

```
    Get execution price: Money (property - simple state)
```

```
    Executes through broker: ExecutionResult, Broker (method - complex behavior)
```

```
(Properties for state access, methods for actions with side effects)
```

**DO NOT**

Don't pass state to objects that should already own it. Example: LineItem Calculates: Money
Product
Quantity
Discount (wrong - passing owned state) vs Money
Discount (right)

Don't pass data to an object's method that the object should already have as properties

```
LineItem (WRONG: receiving data it should own)
```

```
    Calculates extended price: Money, Product, Quantity, Discount
```

```
Holding (WRONG: receiving data it should own)
```

```
    Calculates market value: Money, Symbol, Quantity, MarketPrice
```

```
(LineItem should own Product and Quantity, Holding should own Symbol and Quantity - don't pass them in)
```

Don't expose internal collection types through properties

```
Portfolio
```

```
    Get holdings list: List (WRONG: exposes internal type)
```

```
    Get holdings array: Array (WRONG: exposes internal type)
```

```
    Get holdings dictionary: Dictionary (WRONG: exposes internal structure)
```

```
(Should be: Get holdings: Holding - hide how they're stored)
```

Don't use methods where simple property access makes sense

```
Trade
```

```
    Retrieve symbol: Symbol (WRONG: method for simple property)
```

```
    Fetch shares count: Shares (WRONG: method for simple property)
```

```
    Compute execution price: Money (WRONG: method for property access)
```

```
(Should be: Get symbol, Get shares, Get execution price - simple property access)
```

Don't allow external manipulation of internal state

```
Portfolio
```

```
    Set holdings: List (WRONG: external manipulation)
```

```
    Modify positions: Position (WRONG: direct modification)
```

```
    Update holding list: List (WRONG: exposes internal structure)
```

```
(Should be: Adds holding: Holding, Removes holding: Holding - controlled mutation)
```