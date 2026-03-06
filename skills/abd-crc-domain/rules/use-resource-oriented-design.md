---
title: use-resource-oriented-design
priority: 7
---

## use-resource-oriented-design

Use resource-oriented design where concepts represent resources with properties and behaviors. Focus on what the resource IS and HAS
not implementation operations.

**DO**

Model concepts as resources with properties and contained resources

Concepts represent resources that contain other resources and expose properties

```
Portfolio (resource)
```

```
    Get holdings: Holding (contains resources)
```

```
    Calculates total value: Money, Holding, MarketPrice (computed property)
```

```
    Evaluates risk score: RiskScore, RiskModel, Holding (computed property)
```

```
Order (resource)
```

```
    Get line items: LineItem (contains resources)
```

```
    Calculates subtotal: Money, LineItem (computed property)
```

```
    Get shipping address: ShippingAddress (contains resource)
```

```
(Resources contain other resources and expose simple/computed properties)
```

Use Get/Find to access resource properties and contained resources

```
Holding (resource)
```

```
    Get symbol: Symbol (simple property)
```

```
    Get quantity: Quantity (simple property)
```

```
    Calculates market value: Money, Symbol, MarketPrice (computed property)
```

```
Trade (resource)
```

```
    Get symbol: Symbol (simple property)
```

```
    Get shares: Shares (simple property)
```

```
    Calculates execution price: Money, Symbol, MarketPrice, TradingFees (computed property)
```

```
(Simple properties use Get; computed properties use business verbs)
```

Name concepts after resources (nouns)
not actions (verbs). Concepts represent things that exist in the domain.

```
Order (CORRECT: resource/noun - a thing that exists)
```

```
Instructions (CORRECT: resource/noun - a thing that exists)
```

```
HeadlessSession (CORRECT: resource/noun - a thing that exists)
```

```
ExecutionContext (CORRECT: resource/noun - a thing that exists)
```

```
InstructionPreparer (WRONG: action/verb - describes what something does, not what it is)
```

```
SessionMonitor (WRONG: action/verb - describes what something does, not what it is)
```

```
(Concept names must be RESOURCES/NOUNS that represent domain entities)
```

Use collaborators for complex resources with behavior/state. Use simple types for properties without sufficient complexity. Only create separate resource concepts when warranted.

```
Order (resource)
```

```
    Get order id: OrderId (simple property, no collaborator needed)
```

```
    Get order date: Date (simple property, no collaborator needed)
```

```
    Get line items: LineItem (complex: LineItem is separate resource with behavior)
```

```
    Calculates total with taxes: Money, TaxRate (TaxRate has enough complexity to be collaborator)
```

```
    Calculates shipping cost: Money, ShippingMethod (ShippingMethod has behavior, separate resource)
```

```
LineItem (separate resource - has sufficient complexity)
```

```
    Get product: Product
```

```
    Get quantity: Quantity (simple property)
```

```
    Calculates extended price: Money, Discount
```

```
HeadlessSession (resource)
```

```
    Get session id: SessionId (simple property, no separate concept)
```

```
    Get execution context: ExecutionContext (complex: separate resource with multiple responsibilities)
```

```
(OrderId, Date, Quantity, SessionId are simple - just properties. LineItem, Product, ShippingMethod, ExecutionContext have enough behavior/state to warrant separate resource concepts)
```

**DO NOT**

Don't violate encapsulation - objects should own their data
hide implementation details
and handle their own responsibilities

Don't pass information to another object's methods that the other object should already have as properties

```
LineItem (showing what LineItem receives)
```

```
    Calculates extended price: Money, Product, Quantity, Discount (WRONG: receiving Product and Quantity, but LineItem needs to owns these)
```

```
    Validates inventory: Boolean, Product, Quantity, InventoryService (WRONG: receiving Product and Quantity that it should already own)
```

```
Holding (showing what Holding receives)
```

```
    Calculates market value: Money, Symbol, Quantity, MarketPrice (WRONG: receiving Symbol and Quantity that it already owns)
```

```
    Validates allocation: Boolean, Symbol, Quantity, AllocationRule (WRONG: receiving Symbol and Quantity that it already owns)
```

```
(Should be: LineItem - Calculates extended price: Money, Discount; Holding - Calculates market value: Money, MarketPrice)
```

Don't expose inner workings of concept - hide implementation details behind clear interface

```
Portfolio
```

```
    Get holdings list: List (WRONG: exposes internal collection type)
```

```
    Get holdings array: Array (WRONG: exposes internal structure)
```

```
    Get holdings dictionary by symbol: Dictionary (WRONG: exposes internal organization)
```

```
Order
```

```
    Get line items as array: Array (WRONG: exposes implementation)
```

```
    Get payment transaction record: TransactionRecord (WRONG: exposes internal detail)
```

```
(Should be: Get holdings: Holding, Get line items: LineItem - hide how they're stored internally)
```

Don't mix multiple concepts together where responsibilities belong to a related collaborator

```
Order (WRONG: mixing Order and LineItem responsibilities)
```

```
    Get order id: OrderId
```

```
    Get line items: LineItem
```

```
    Calculates line item extended price: Money, Product, Quantity, Discount (WRONG: belongs to LineItem)
```

```
    Validates line item inventory: Boolean, Product, InventoryService (WRONG: belongs to LineItem)
```

```
Portfolio (WRONG: mixing Portfolio and Holding responsibilities)
```

```
    Get holdings: Holding
```

```
    Calculates holding market value: Money, Symbol, MarketPrice (WRONG: belongs to Holding)
```

```
    Validates holding allocation limits: Boolean, Symbol, AllocationRule (WRONG: belongs to Holding)
```

```
(Should be: LineItem calculates its own price, Holding calculates its own market value)
```

Don't hold responsibilities that belong to a collaborator—when many responsibilities reference the same collaborator or noun
that's a smell. Move those responsibilities to the collaborator and keep a link instead.

```
Voucher (WRONG: many redemption-related responsibilities)
```

```
    Defines redemption limit (redemptions allowed): Integer
```

```
    Tracks redemption count: Integer
```

```
    Is exhausted when fully redeemed: Boolean
```

```
    Is locked for redemption: Lock
```

```
    Is redeemed in: Redemption
```

```
(Smell: 'redemption' appears in many responsibilities—Voucher is holding too much. Move limit, count, exhaustion to Redemptions.)
```

```
Voucher (CORRECT: link to Redemptions for redemption state)
```

```
    Is identified by code: String
```

```
    Inherits metadata from campaign: Campaign
```

```
    Applies discount amount to order: Campaign
```

```
    isRedeemed: Redemptions, Lock
```

```
Redemptions (owns redemption data and behavior)
```

```
    has Maximum Redemptions: Number
```

```
    has Redemptions: Date Collection
```

```
    redeems A Voucher: Voucher
```

```
    redeemed by A Customer: Customer
```

```
    Is exhausted: Boolean
```

Don't use Manager/Service suffixes that imply operations rather than resources

```
PortfolioManager
```

```
    Manages holdings: Holding (WRONG: operation-oriented)
```

```
    Handles trades: Trade (WRONG: operation-oriented)
```

```
OrderService
```

```
    Services orders: Order (WRONG: operation-oriented)
```

```
(Should be: Portfolio with Get holdings, Calculates total value; Trade with Creates from recommendation)
```

Don't describe domain concepts as only data carriers with getters that have no actual domain behavior

```
Portfolio (WRONG: ONLY getters, no business behavior)
```

```
    Get account id: AccountId
```

```
    Get holdings: Holding
```

```
    Get creation date: Date
```

```
    Get last modified: Date
```

```
Order (WRONG: ONLY getters, no business behavior)
```

```
    Get order id: OrderId
```

```
    Get line items: LineItem
```

```
    Get customer id: CustomerId
```

```
    Get order date: Date
```

```
(Anemic domain models - simple getters are fine, but concepts need actual business behavior too: Calculates total value, Evaluates risk score, Validates inventory, Calculates shipping cost)
```

Don't name concepts after actions (Loader
Preparer
Builder
Monitor
Handler
Manager
Service). Name them after the resource itself.

```
InstructionPreparer (WRONG: named after action)
```

```
    Prepares instructions: Instructions
```

```
ContextLoader (WRONG: named after action)
```

```
    Loads context: ExecutionContext
```

```
SessionMonitor (WRONG: named after action)
```

```
    Monitors session: HeadlessSession
```

```
Instructions (CORRECT: resource name)
```

```
    Prepares for Cursor API: String
```

```
ExecutionContext (CORRECT: resource name)
```

```
    Loads from file: Path
```

```
HeadlessSession (CORRECT: resource name)
```

```
    Monitors execution status: SessionStatus
```

```
(Concept = NOUN/RESOURCE, Responsibility = VERB/ACTION)
```

Don't create separate resource concepts for simple data that should just be properties. Don't create anemic resources with no behavior.

```
OrderId (WRONG: separate concept with no behavior)
```

```
    Get value: String
```

```
OrderDate (WRONG: separate concept with no behavior)
```

```
    Get value: Date
```

```
SessionId (WRONG: separate concept with no behavior)
```

```
    Get value: String
```

```
(These should just be simple properties on their parent resource, not separate concepts in the domain model)
```