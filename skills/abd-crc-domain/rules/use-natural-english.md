---
title: use-natural-english
priority: 6
---

## use-natural-english

Use natural English for responsibility names. Responsibilities should read like natural language method calls
using proper grammar and clear intent.

**DO**

Write responsibilities in natural English that clearly express intent

Use verbs with clear nouns that read naturally

```
Portfolio
```

```
    Get holdings: Holding
```

```
    Calculates total value with market prices: Money, Holding, MarketPrice
```

```
    Evaluates risk score: RiskScore, RiskModel, Holding
```

```
Order
```

```
    Get line items: LineItem
```

```
    Calculates subtotal from items: Money, LineItem
```

```
    Finds by order number: Order, OrderNumber
```

```
(Reads naturally: 'Portfolio calculates total value', 'Order finds by order number')
```

Use proper articles and prepositions when they improve clarity

```
Trade
```

```
    Creates from rebalance recommendation: Trade, RebalanceRecommendation
```

```
    Calculates execution price: Money, Symbol, MarketPrice, TradingFees
```

```
Holding
```

```
    Finds by symbol: Holding, Symbol
```

```
    Calculates market value: Money, Symbol, MarketPrice
```

```
(Natural phrases: 'Creates from rebalance recommendation', 'Calculates execution price')
```

**DO NOT**

Don't use awkward phrasing or overly technical grammar

Don't use awkward abbreviations or shorthand that doesn't read naturally

```
Portfolio
```

```
    Gt hldgs: Holding (WRONG: abbreviations)
```

```
    Calc ttl val: Money (WRONG: abbreviations)
```

```
Order
```

```
    Fnd ord num: OrderNumber (WRONG: abbreviations)
```

```
    Proc pmt: Payment (WRONG: abbreviations)
```

```
(Should be: Get holdings, Calculates total value, Finds by order number)
```

Don't use overly verbose or awkward phrasing

```
Portfolio
```

```
    Performs the operation of getting all holdings: Holding (WRONG: verbose)
```

```
    Executes calculation for determining total value: Money (WRONG: verbose)
```

```
(Should be: Get holdings: Holding, Calculates total value: Money, Holding)
```

Don't use technical jargon when simple English works

```
Order
```

```
    Instantiates line item collection: LineItem (WRONG: technical)
```

```
    Aggregates monetary units: Money (WRONG: technical)
```

```
Payment
```

```
    Retrieves authorization token: AuthorizationCode (WRONG: overly technical)
```

```
(Should be: Get line items: LineItem, Calculates subtotal: Money, Authorizes transaction: AuthorizationCode)
```