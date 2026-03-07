---
title: favor-code-representation
priority: 3
---

## favor-code-representation

Keep domain model tightly aligned to code it represents
use actual class names and method signatures
not prose descriptions. Show collaborators as types
not descriptions. Avoid over conceptualization.

**DO**

Keep code and domain model tightly aligned

Use actual class names and method-like responsibility names with typed collaborators that represents future or actual implementation code

```
Portfolio
```

```
    Get holdings: Holding
```

```
    Get total value: Money, Holding
```

```
    Get risk score: RiskScore, RiskModel, Holding
```

```
Holding
```

```
    Get symbol: Symbol
```

```
    Get quantity: Quantity
```

```
    Get market value: Money, Symbol, MarketPrice
```

```
(Class names: Portfolio, Holding. Collaborator types: Money, Symbol, Quantity)
```

Use meaningful business-oriented responsibility names that clearly express domain intent

```
Order
```

```
    Creates from shopping cart: Cart, Customer
```

```
    Calculates total with taxes and shipping: Money, LineItem, TaxRate, ShippingMethod
```

```
    Validates inventory availability: LineItem, InventoryService
```

```
    Applies promotional discount: Money, PromotionCode, LineItem
```

```
RebalanceRecommendation
```

```
    Generates trades to achieve target allocation: Trade, Portfolio, TargetAllocation
```

```
    Compares current allocation to target: AllocationDifference, Portfolio, TargetAllocation
```

```
    Minimizes transaction costs: Money, Trade, TradingFees
```

```
(Clear business intent: creates, calculates, validates, applies, generates, compares, minimizes)
```

**DO NOT**

Don't use prose descriptions or vague terms

Don't use long prose sentences as concept names - use concise class names that could exist in code

```
Collection of customer investments that aggregates all holdings and provides real-time portfolio valuation with risk scoring capabilities (WRONG: long prose sentence)
```

```
    Calculates total value across all holdings: Money
```

```
    Determines risk score based on volatility: RiskScore
```

```
(Should be: Portfolio - concise class name. Note: Meaningful responsibility names like 'Calculates total value across all holdings' are perfectly fine!)
```

Don't use prose descriptions for collaborator types - use actual type names that could exist in code

```
Portfolio
```

```
    Calculates risk score across holdings: detailed object containing volatility calculations and risk metrics (WRONG: prose for type)
```

```
    Determines total portfolio value: the monetary sum of all current holdings at market prices (WRONG: prose for type)
```

```
(Should be: Calculates risk score across holdings: RiskScore, RiskModel, Holding with actual type names)
```

Don't use prose sentences for concept names even when responsibilities are correct

```
Order that manages customer purchases and tracks items (WRONG: prose sentence for concept)
```

```
    Get line items: LineItem
```

```
    Get subtotal: Money
```

```
(Should be: Order as class name. Note: 'Get line items' is fine - descriptive responsibility names are good)
```