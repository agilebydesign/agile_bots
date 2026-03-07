---
title: place-at-lowest-level
priority: 4
---

## place-at-lowest-level

Place state and responsibilities at the lowest-level object that owns them. Delegate to lowest-level objects
chain dependencies through hierarchy. Example: Holding owns Symbol/Quantity and Calculates market value; Portfolio Has holdings and delegates to them.

**DO**

Place state and responsibilities at lowest owner
chain dependencies through hierarchy. Example: Holding owns Symbol/Quantity and Calculates market value; Portfolio Has holdings and delegates

Delegate responsibilities to the object that owns the data needed to fulfill them

```
Order
```

```
    Calculates total: Money, LineItem (delegates calculation to LineItems)
```

```
LineItem (owns Product and Quantity)
```

```
    Calculates extended price: Money, Discount (uses its own data)
```

```
(Each object handles responsibilities using data it already owns)
```

Place state at the lowest component that logically owns it

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
Portfolio (higher - aggregates but doesn't own holding state)
```

```
    Has holdings: Holding
```

```
    Calculates total value: Money, Holding (delegates to holdings)
```

```
(Symbol and Quantity belong to Holding, not Portfolio)
```

Chain dependencies - access sub-collaborators through their owning objects

```
WealthAdvisor
```

```
    Instantiated with: Client
```

```
    Creates portfolio: Portfolio, Client (uses injected Client)
```

```
    Evaluates risk tolerance: RiskTolerance, Client (gets from Client)
```

```
Client
```

```
    Instantiated with: AccountId, RiskProfile, InvestmentStrategy
```

```
    Get investment strategy: InvestmentStrategy
```

```
(WealthAdvisor accesses RiskProfile through Client, not directly)
```

Only create collection classes when there is collection-level logic

```
Holdings (collection class - has collection-level logic)
```

```
    Finds by symbol: Holding, Symbol
```

```
    Calculates total value: Money, Holding, MarketPrice
```

```
    Filters by asset class: Holding, AssetClass
```

```
(Holdings exists because find, filter, aggregate operate on the collection)
```

**DO NOT**

Don't place state/responsibilities too high
don't skip hierarchy levels. Example: Portfolio Calculates holding market value (wrong - doing Holding's work) vs Holding Calculates (right)

Don't have parent objects doing what child objects should do

```
Order (WRONG: doing LineItem's work)
```

```
    Calculates line item extended price: Money, Product, Quantity, Discount
```

```
Portfolio (WRONG: doing Holding's work)
```

```
    Calculates holding market value: Money, Symbol, Quantity, MarketPrice
```

```
(Should be: LineItem calculates its own price, Holding calculates its own value)
```

Don't skip levels in dependency chain

```
WealthAdvisor (WRONG: skips Client level)
```

```
    Instantiated with: Client
```

```
    Creates portfolio: Portfolio, AccountId, RiskProfile, InvestmentStrategy
```

```
(Should access RiskProfile and InvestmentStrategy through Client)
```

Don't create wrapper methods that just delegate down

```
Client (WRONG: wrapper methods)
```

```
    Gets portfolio holdings: Holding
```

```
    Gets portfolio total value: Money
```

```
(Navigate Client -> Portfolio -> Holdings instead of wrappers)
```

Don't create collection classes without collection-level logic

```
LineItems (WRONG: no collection logic)
```

```
    Get items: LineItem
```

```
(No find/filter/sort/aggregate logic - just use List<LineItem>)
```