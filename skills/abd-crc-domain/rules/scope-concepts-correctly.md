---
title: scope-concepts-correctly
priority: 3
---

## scope-concepts-correctly

Scope domain concepts correctly - place at the most specific level where relevant and ensure they represent complete functional capabilities. Use 'local' scope for single sub-epic concepts
'global' for shared concepts. Concepts should be complete functional units
not fragments.

**DO**

Place concepts at correct scope level and ensure functional completeness

Place concepts locally when they're only relevant to one sub-epic

```
Sub-Epic: Assign Character Ability
```

```
  domain_concepts (local scope):
```

```
    AbilityScore
```

```
        Get value: Number
```

```
        Calculates modifier from score: Number, AbilityScore
```

```
    PointBuyCalculator
```

```
        Calculates remaining points: Number, AbilityScore, PointBuyLimit
```

```
        Validates point distribution: Boolean, AbilityScore, PointBuyRules
```

```
(Only used within this sub-epic, so placed locally)
```

Elevate concepts to parent when shared across multiple sub-epics

```
Epic: Manage Characters
```

```
  domain_concepts (global scope):
```

```
    Character
```

```
        Get name: Name
```

```
        Get abilities: AbilityScore
```

```
        Calculates total level: Number, ExperiencePoints
```

```
        Advances to next level: Character, ExperiencePoints, LevelRequirements
```

```
Sub-Epic: Character Creation (uses global Character)
```

```
Sub-Epic: Character Advancement (uses global Character)
```

```
Sub-Epic: Character Display (uses global Character)
```

```
(Character shared by multiple sub-epics, so placed at epic level)
```

Define concepts that represent complete functional capabilities with all necessary responsibilities

```
RebalanceRecommendation (complete functional unit)
```

```
    Generates trades to achieve target: Trade, Portfolio, TargetAllocation
```

```
    Compares current to target allocation: AllocationDifference, Portfolio, TargetAllocation
```

```
    Explains rebalance rationale: Rationale, AllocationDifference, MarketConditions
```

```
    Minimizes transaction costs: Money, Trade, TradingFees
```

```
(Complete: can produce recommendation with all supporting data and rationale)
```

Scope concepts to meaningful business capabilities that can accomplish something alone

```
Order (complete business capability)
```

```
    Creates from shopping cart: Cart, Customer
```

```
    Get line items: LineItem
```

```
    Calculates subtotal from items: Money, LineItem
```

```
    Calculates tax based on location: Money, LineItem, TaxRate, ShippingAddress
```

```
    Calculates total with shipping: Money, LineItem, TaxRate, ShippingMethod
```

```
    Validates inventory availability: Boolean, LineItem, InventoryService
```

```
(Complete: represents full order capability with validation and calculations)
```

**DO NOT**

Don't place concepts at wrong scope level or create incomplete fragments

Don't place all concepts globally by default

```
Epic: Manage Orders
```

```
  domain_concepts (global):
```

```
    Order, LineItem, ShippingAddress, BillingAddress, PaymentMethod, TaxCalculator, DiscountCalculator, ShippingCalculator (WRONG: all global)
```

```
(TaxCalculator, DiscountCalculator only used in 'Calculate Totals' sub-epic - should be local)
```

Don't keep concepts local when they're used by multiple sub-epics

```
Sub-Epic: Create Order
```

```
  domain_concepts (local):
```

```
    Order
```

```
        Get line items: LineItem
```

```
Sub-Epic: Display Order (WRONG: also defines Order locally)
```

```
  domain_concepts (local):
```

```
    Order
```

```
        Get line items: LineItem
```

```
(Order duplicated - should be elevated to epic level)
```

Don't split concepts into fragments that can't accomplish anything alone

```
TradeData (WRONG: fragment)
```

```
    Get symbol: Symbol
```

```
    Get shares: Shares
```

```
TradeCalculator (WRONG: fragment)
```

```
    Get price: Money
```

```
(Fragments - should be combined into Trade with complete responsibilities)
```

Don't create concepts that are just implementation details without functional purpose

```
OrderValidator (WRONG: implementation detail)
```

```
    Validates data: Boolean
```

```
(Should be part of Order: Order validates itself during creation)
```