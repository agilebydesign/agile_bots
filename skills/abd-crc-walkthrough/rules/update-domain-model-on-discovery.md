---
title: update-domain-model-on-discovery
priority: 5
---

## update-domain-model-on-discovery

When walkthrough reveals missing responsibilities
collaborators
or concepts
then continue walkthrough

**DO**

note in walkthrough doc
continue tracing

When discovering missing responsibility
ShippingAddress

```
During walkthrough:
```

```
Order
```

```
    total: 112.50 = Order.calculate_total()
```

```
        -> shipping: 12.50 = Order.calculate_shipping() [MISSING FROM MODEL]
```

```
{
```

```
  "concept_name": "Order",
```

```
  "responsibilities": [
```

```
    "Calculates total: Money, LineItem, ShippingMethod",
```

```
    "Calculates shipping cost by method: Money, ShippingAddress, ShippingMethod"  // ADDED
```

```
  ]
```

```
}
```

```
Document in walkthrough:
```

```
**Model Updates Discovered**
```

```
- Order: Added 'Calculates shipping cost by method: Money, ShippingAddress, ShippingMethod'
```

```
(Update model, document change, continue walkthrough)
```

When discovering missing collaborator
LineItem' but walkthrough needs TaxRate -> update to 'Calculates total: Money
LineItem

```
During walkthrough:
```

```
Order
```

```
    total: 115.00 = Order.calculate_total()
```

```
        -> subtotal: 100.00 = LineItem.calculate_subtotal(items)
```

```
        -> tax: 15.00 = TaxRate.calculate(subtotal) [TaxRate NOT IN COLLABORATORS]
```

```
{
```

```
  "concept_name": "Order",
```

```
  "responsibilities": [
```

```
    "Calculates total: Money, LineItem, TaxRate"  // ADDED TaxRate
```

```
  ]
```

```
}
```

```
Document in walkthrough:
```

```
**Model Updates Discovered**
```

```
- Order 'Calculates total': Added TaxRate collaborator
```

```
(Add collaborator to existing responsibility in model)
```

When discovering new concept

```
During walkthrough:
```

```
Scope
```

```
    validation: [('Story1', True), ('Story2', False)] = Scope.validate_scope(graph)
```

```
        -> results: <ValidationResult> = KnowledgeGraphFilter.check_nodes(...) [NEW CONCEPT NEEDED]
```

```
{
```

```
  "concept_name": "ValidationResult",
```

```
  "responsibilities": [
```

```
    "Shows valid nodes: List[NodeName]",
```

```
    "Shows invalid nodes: List[NodeName]",
```

```
    "Formats as display string: str"
```

```
  ],
```

```
  "collaborators": []
```

```
}
```

```
Document in walkthrough:
```

```
**New Concepts Discovered**
```

```
- ValidationResult: Results of validating scope nodes
```

```
(Create new concept, document discovery, continue)
```

Document all model updates in walkthrough realization document. Example: In 'Model Updates Discovered' section list all added responsibilities
modified collaborators
and new concepts with rationale

```
In walkthrough-realizations.md:
```

```
## Model Updates Discovered
```

```
### New Responsibilities Added
```

```
**Scope**
```

```
- Rationale: Walkthrough showed validation needed but wasn't in model
```

```
**Order**
```

```
- Added: 'Calculates shipping cost by method: Money, ShippingAddress, ShippingMethod'
```

```
- Rationale: Shipping calculation flow required this responsibility
```

```
### Responsibilities Modified
```

```
**Order**
```

```
- Changed: 'Calculates total: Money, LineItem' → 'Calculates total: Money, LineItem, TaxRate'
```

```
- Rationale: Tax calculation discovered as necessary collaborator
```

```
### New Concepts Discovered
```

```
**ValidationResult**
```

```
- Description: Results of validating scope nodes
```

```
- Responsibilities: Shows valid/invalid nodes, Formats display
```

```
- Rationale: Needed structured validation data
```

```
(Complete documentation of all model changes)
```

**DO NOT**

Don't continue with missing responsibilities without updating model. Example: Discover Order.calculate_shipping() not in model but keep tracing (wrong) vs add 'Calculates shipping: Money

```
BAD:
```

```
Order
```

```
    total: 112.50 = Order.calculate_total()
```

```
        -> shipping: 12.50 = Order.calculate_shipping() [MISSING]
```

```
    return total: 112.50
```

```
(Continues without updating model - leaves gap)
```

```
GOOD:
```

```
Order
```

```
    total: 112.50 = Order.calculate_total()
```

```
        -> shipping: 12.50 = Order.calculate_shipping() [MISSING FROM MODEL]
```

```
'Calculates shipping cost by method: Money, ShippingAddress, ShippingMethod'
```

```
Then continue walkthrough:
```

```
Order
```

```
    total: 112.50 = Order.calculate_total()
```

```
        -> shipping: 12.50 = Order.calculate_shipping()
```

```
            -> method: <ShippingMethod> = Order.get_shipping_method()
```

```
    return total: 112.50
```

```
(Updates model first, then continues with complete trace)
```

```
BAD:
```

```
-> validation: <ValidationResult> = Scope.validate_scope(graph)
```

```
(Uses new concept but doesn't add to model)
```

```
GOOD:
```

```
-> validation: <ValidationResult> = Scope.validate_scope(graph) [NEW CONCEPT]
```

```
{
```

```
  "concept_name": "ValidationResult",
```

```
  "responsibilities": [
```

```
    "Shows valid nodes: List[NodeName]",
```

```
    "Shows invalid nodes: List[NodeName]"
```

```
  ]
```

```
}
```

```
Document: ValidationResult added as new concept
```

```
(Creates concept in model before using)
```

```
BAD:
```

```
But walkthrough document has no 'Model Updates Discovered' section
```

```
(Model updated but changes not documented)
```

```
GOOD:
```

```
   Order adds 'Calculates shipping: Money, ShippingMethod'
```

```
2. Document in walkthrough:
```

```
   ## Model Updates Discovered
```

```
   ### New Responsibilities Added
```

```
   **Order**
```

```
   - Added: 'Calculates shipping: Money, ShippingMethod'
```

```
   - Rationale: Shipping calculation required in Order.calculate_total() flow
```

```
(Both model and documentation updated)
```

```
BAD:
```

```
Order 'Calculates total: Money, LineItem'
```

```
But walkthrough uses:
```

```
-> tax: 15.00 = TaxRate.calculate(subtotal)
```

```
(TaxRate used but not in collaborators list)
```

```
GOOD:
```

```
Order 'Calculates total: Money, LineItem, TaxRate'
```

```
Then walkthrough:
```

```
-> tax: 15.00 = TaxRate.calculate(subtotal)
```

```
Document:
```

```
Order 'Calculates total': Added TaxRate collaborator
```

```
(Collaborator added to model before use)
```