---
title: align-to-domain-model
priority: 2
---

## align-to-domain-model

Walkthrough scenarios must use exact concept names
responsibilities
Holding
MarketPrice' then use total_value: 150000.00 = Portfolio.calculate_total_value() with those exact collaborators

**DO**

Use domain concepts
responsibilities
and language exactly as defined in model. Example: Model has 'Order Calculates shipping cost by method: Money
ShippingAddress
ShippingMethod' -> walkthrough uses shipping: 12.50 = Order.calculate_shipping_cost_by_method() with exact collaborators

Use exact domain concept names from model. Example: If model defines Portfolio with 'Calculates total value: Money
Holding
MarketPrice' then use Portfolio.calculate_total_value() not PortfolioService.getValue()

```
If domain model defines:
```

```
Portfolio
```

```
    Calculates total value: Money, Holding, MarketPrice
```

```
    Evaluates risk score: RiskScore, RiskModel
```

```
Then walkthrough uses:
```

```
Portfolio
```

```
    total_value: 150000.00 = Portfolio.calculate_total_value()
```

```
        -> holdings: [<Holding AAPL>, <Holding GOOGL>] = Portfolio.get_holdings()
```

```
        -> prices: {AAPL: 150.00, GOOGL: 2800.00} = MarketPrice.get_current_prices(symbols: ['AAPL', 'GOOGL'])
```

```
        -> total: 150000.00 = Money.sum(holdings, prices)
```

```
        return total_value: 150000.00
```

```
(Uses Portfolio, Holding, MarketPrice, Money from domain model)
```

Use exact responsibility names from domain concepts. Example: Model says 'Calculates shipping cost by method' -> use calculate_shipping_cost_by_method() not get_shipping() or compute_shipping()

```
If concept has 'Calculates shipping cost by method', use that:
```

```
Order
```

```
    shipping: 12.50 = Order.calculate_shipping_cost_by_method()
```

```
        -> address: <ShippingAddress> = Order.get_shipping_address()
```

```
        -> method: 'Priority' = Order.get_shipping_method()
```

```
        -> cost: 12.50 = ShippingMethod.calculate_cost(address, method: 'Priority')
```

```
        return shipping: 12.50
```

```
(Don't change to 'get_shipping' or 'compute_shipping' - use exact name)
```

Use exact collaborator names from domain model. Example: Responsibility lists 'Money
ShippingAddress
ShippingMethod' -> use only those
not ShippingService or Calculator

```
If responsibility lists collaborators: 'Money, ShippingAddress, ShippingMethod'
```

```
Order
```

```
    shipping: 12.50 = Order.calculate_shipping_cost_by_method()
```

```
        -> address: <ShippingAddress> = Order.get_shipping_address()
```

```
        -> method: <ShippingMethod> = ShippingMethod.find(name: 'Priority')
```

```
        -> cost: 12.50 = ShippingMethod.calculate_cost(address, method)
```

```
        return shipping: Money(12.50)
```

```
(Uses ShippingAddress, ShippingMethod, Money - exact collaborators)
```

```
Then walkthrough traces:
```

```
Scope
```

```
    validation: [('Story1', True), ('Story2', False)] = Scope.validate_against_story_graph(graph)
```

```
        -> nodes: ['Story1', 'Story2'] = Scope.get_node_names()
```

```
        -> results: [('Story1', True), ('Story2', False)] = StoryGraph.check_nodes_exist(nodes)
```

```
        return validation: [('Story1', True), ('Story2', False)]
```

**DO NOT**

Don't invent new concepts
responsibilities
or change domain language. Example: Model has Portfolio -> don't use PortfolioValidator without adding it to model first; Model says 'Calculates total value' -> don't rename to get_total_value()

Don't introduce concepts not in domain model without updating it. Example: Using PortfolioValidator when model only has Portfolio (wrong) -> either use Portfolio.validates_holdings() or add PortfolioValidator to model first

```
BAD (if PortfolioValidator not in model):
```

```
-> validation: True = PortfolioValidator.validate(portfolio)
```

```
GOOD:
```

```
-> is_valid: True = Portfolio.validates_holdings()
```

```
    -> holdings: [...] = Portfolio.get_holdings()
```

```
    -> valid: True = Holding.validate_each(holdings)
```

```
    return is_valid: True
```

```
OR: Add PortfolioValidator to domain model FIRST, then use it
```

Don't rename responsibilities to match your preference. Example: Model says 'Calculates total value across holdings' (wrong to change) vs calculate_total_value_across_holdings() (right - exact match)

```
Domain model says: 'Calculates total value across holdings'
```

```
BAD:
```

```
-> total: 150000.00 = Portfolio.get_total_value()
```

```
-> sum: 150000.00 = Portfolio.compute_value()
```

```
GOOD:
```

```
-> total_value: 150000.00 = Portfolio.calculate_total_value_across_holdings()
```

```
(Use exact responsibility name from model)
```

Don't use collaborators not listed in responsibility. Example: Responsibility lists 'Money
Holding
MarketPrice' but adding PortfolioCache (wrong) vs using only listed collaborators (right)

```
If responsibility says: 'Calculates total value: Money, Holding, MarketPrice'
```

```
BAD (adds Portfolio Cache not in collaborators):
```

```
-> total: 150000.00 = Portfolio.calculate_total_value()
```

```
    -> cached: None = PortfolioCache.get(portfolio_id)
```

```
    -> holdings: [...] = Portfolio.get_holdings()
```

```
GOOD:
```

```
-> total_value: 150000.00 = Portfolio.calculate_total_value()
```

```
    -> holdings: [...] = Portfolio.get_holdings()
```

```
    -> prices: {...} = MarketPrice.get_current_prices(symbols)
```

```
    -> value: 150000.00 = Money.calculate_value(holdings, prices)
```

```
(Only use Money, Holding, MarketPrice - the listed collaborators)
```