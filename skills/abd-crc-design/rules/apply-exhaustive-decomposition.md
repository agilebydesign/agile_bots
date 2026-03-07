---
title: apply-exhaustive-decomposition
priority: 1
---

## apply-exhaustive-decomposition

Apply exhaustive logic decomposition. Cover all validation paths
calculation branches
and edge cases explicitly. Use inheritance for variations
not enumeration. Example: Order -> Creates
Validates
Calculates total
Submits (complete flow); ShippingCalculator base
InternationalShippingCalculator : ShippingCalculator (inheritance for variations).

**DO**

Cover all logic paths
use inheritance for variations. Example: Order -> Creates
Validates
Calculates
Submits (complete flow); ShippingCalculator base with InternationalShippingCalculator : ShippingCalculator subclass (inheritance)

Show complete flow including validation
calculation
and persistence steps

```
Order
```

```
    Creates from cart: Order, Cart, Customer
```

```
    Validates before submission: Boolean, InventoryService, PaymentGateway
```

```
    Calculates total: Money, LineItem, TaxRate, ShippingMethod
```

```
    Submits for fulfillment: FulfillmentRequest
```

```
(Complete flow: create → validate → calculate → submit - no steps skipped)
```

Use inheritance to handle variations instead of enumerating each permutation

```
ShippingCalculator (base - handles core calculation)
```

```
    Calculates rate: Money, Weight, Distance
```

```
InternationalShippingCalculator : ShippingCalculator
```

```
    Calculates rate: Money, Weight, Distance, Country, CustomsFees
```

```
(Base handles domestic, subclass extends with Country and customs)
```

Cover edge cases and alternative paths explicitly

```
Payment
```

```
    Authorizes transaction: AuthorizationResult, PaymentGateway
```

```
    Handles authorization failure: FailureResponse, AuthorizationResult
```

```
    Handles partial authorization: PartialResponse, RemainingBalance
```

```
(Success, failure, partial paths all covered)
```

**DO NOT**

Don't enumerate permutations or skip logic steps. Example: ShippingCalculator with Calculates standard/express/overnight domestic/international (wrong - enumerate) vs base + subclass (right)

Don't enumerate every permutation as separate methods - use inheritance

```
ShippingCalculator (WRONG: enumerates all permutations)
```

```
    Calculates standard domestic rate: Money, Weight, Distance
```

```
    Calculates express domestic rate: Money, Weight, Distance
```

```
    Calculates overnight domestic rate: Money, Weight, Distance
```

```
    Calculates standard international rate: Money, Weight, Distance, Country
```

```
    Calculates express international rate: Money, Weight, Distance, Country
```

```
(Should use base class + InternationalShippingCalculator subclass)
```

Don't skip validation or intermediate steps

```
Order (WRONG: skips validation and calculation)
```

```
    Creates from cart: Order, Cart
```

```
    Submits: FulfillmentRequest
```

```
(Missing: validation, inventory check, total calculation)
```

Don't hide error handling and edge cases

```
Payment (WRONG: only shows happy path)
```

```
    Authorizes transaction: AuthorizationResult, PaymentGateway
```

```
(Missing: failure handling, partial authorization paths)
```