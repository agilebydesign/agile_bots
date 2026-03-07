---
title: integrate-and-organize-concepts
priority: 1
---

## integrate-and-organize-concepts

Integrate related capabilities under parent concepts and organize by business domain. Avoid noun redundancy by nesting related capabilities together
group by business capabilities not technical layers.

**DO**

Integrate related capabilities under parent concepts
organize by business domain

Nest related capabilities under a single domain concept instead of creating separate concepts with the same noun

```
Character Animation (parent domain concept)
```

```
    Plays walk animation: AnimationClip, CharacterState
```

```
    Plays run animation: AnimationClip, CharacterState
```

```
    Transitions to jump: AnimationClip, CharacterState, JumpTrigger
```

```
    Blends idle animations: AnimationClip, CharacterState, BlendWeight
```

```
(One concept with multiple responsibilities, not separate Walk Animation, Run Animation concepts)
```

Integrate all related capabilities as responsibilities under a single parent concept

```
Portfolio (parent integrating related capabilities)
```

```
    Get holdings: Holding
```

```
    Calculates total value across all holdings: Money, Holding, MarketPrice
```

```
    Evaluates risk score with market conditions: RiskScore, RiskModel, MarketData
```

```
    Analyzes asset allocation distribution: Allocation, Holding, TargetAllocation
```

```
    Finds by account identifier: AccountId
```

```
(All portfolio-related capabilities integrated under Portfolio)
```

Group concepts around business capabilities and subject areas that collaborate frequently

```
Order Management Domain:
```

```
Order
```

```
    Creates from shopping cart: Cart, Customer
```

```
    Calculates total with taxes: Money, LineItem, TaxRate
```

```
    Validates inventory before submission: LineItem, InventoryService
```

```
LineItem
```

```
    Get product: Product
```

```
    Get quantity: Quantity
```

```
    Calculates extended price: Money, Product, Quantity, Discount
```

```
(Grouped by Order Management business capability)
```

Use subject-area nouns when domains are genuinely separate and cannot be integrated

```
Combat (distinct subject area)
```

```
    Executes attack sequence: CombatAnimation, Target, Weapon
```

```
    Calculates damage with modifiers: Damage, Target, Weapon, CriticalHit
```

```
Movement (distinct subject area)
```

```
    Animates locomotion: MovementAnimation, Terrain, Speed
```

```
    Calculates velocity with terrain effects: Speed, Terrain, Slope
```

```
(Separate concepts because combat and movement are distinct domains)
```

**DO NOT**

Don't create redundant/fragmented concepts or group by technical layers

Don't create separate concepts with the same noun when they should be integrated under one parent

```
Walk Animation (WRONG: redundant noun)
```

```
    Get walk sequence: AnimationClip
```

```
Run Animation (WRONG: redundant noun)
```

```
    Get run sequence: AnimationClip
```

```
Jump Animation (WRONG: redundant noun)
```

```
    Get jump sequence: AnimationClip
```

```
(Should be integrated under Character Animation)
```

Don't split related capabilities into separate sibling concepts

```
PortfolioValue (WRONG: separate concept)
```

```
    Get total value: Money
```

```
PortfolioRisk (WRONG: separate concept)
```

```
    Get risk score: RiskScore
```

```
PortfolioAllocation (WRONG: separate concept)
```

```
    Get asset allocation: Allocation
```

```
(Should be integrated into Portfolio as responsibilities)
```

Don't group concepts by technical layers like Data
Business Logic
Presentation

```
Data Layer: (WRONG: technical grouping)
```

```
    OrderData, LineItemData, ProductData
```

```
Business Logic Layer: (WRONG: technical grouping)
```

```
    OrderProcessor, LineItemCalculator, ProductValidator
```

```
(Should be grouped by Order Management domain)
```

Don't organize by implementation patterns like Factories
Builders
Repositories

```
Factories: (WRONG: implementation pattern grouping)
```

```
    OrderFactory, TradeFactory, PortfolioFactory
```

```
(Should be: Order with 'Creates from cart', Trade with 'Creates from recommendation' in respective domains)
```