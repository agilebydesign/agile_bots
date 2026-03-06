---
title: verb-noun-format
priority: 1
---

## verb-noun-format

Use verb-noun format consistently across all hierarchy levels. Actor --> verb noun [qualifiers]. Actor is documented separately
NOT in the name. Focus on specific actions with context.

**DO**

Use specific verb-noun format with actor documented separately. Example: 'Places Order' with actor=Customer

FORMAT: Actor --> verb noun [optional qualifiers]. Actor is documented separately in story metadata
NOT in name. Use base verb forms (infinitive/imperative)
not gerunds or third-person singular. Include specific objects and context qualifiers where needed. Focus on what users/code CAN DO
not what things ARE.

```
Epic: 'Manage Customer Orders', 'Process Online Payments'
```

```
Sub-Epic: 'Place New Order', 'Validate Credit Card Payment'
```

```
Story: 'User --> processes order payment'
```

```
Story: 'System --> validates submitted payments'
```

Stories describe REAL ACTIONS that can be performed
organized by lifecycle: Load â†’ Read â†’ Edit â†’ Render â†’ Synchronize â†’ Search â†’ Save

```
System --> loads order data
```

```
System --> validates payment
```

```
System --> generates XML
```

Actor is documented separately
NEVER in the story name itself

```
Places Order (actor: Customer)
```

```
Validates Payment (actor: System)
```

```
Updates Stock (actor: InventoryManager)
```

Use base verb forms for consistency across all hierarchy levels. Wrong: 'Selects Tokens' (3rd person)
'Selecting Tokens' (gerund).

```
Select Tokens
```

```
Group Minions
```

```
Process Payment
```

**DO NOT**

Don't include actor in name or use generic operations. Example: 'Customer Places Order' (WRONG) â†’ 'Places Order' with actor=Customer (CORRECT)

Never include actor name in the story/epic/sub-epic name - actor is documented separately in metadata. Wrong: 'Customer Places Order'. Correct: 'Places Order (actor: Customer)'.

```
Places Order (actor: Customer) not 'Customer Places Order'
```

```
Validates Payment (actor: OrderProcessor) not 'OrderProcessor Validates Payment'
```

```
Adds Product (actor: Cart) not 'Cart Adds Product'
```

Don't create generic operations without specificity
use noun-only names
capability-based names
or wrong verb forms

```
User --> processes payment (too generic - which payment?)
```

```
Payment Processing (noun-only, not verb-noun)
```

```
Order Management (capability, not action)
```

```
Selects Tokens (wrong verb form - should be 'Select Tokens')
```

Don't use capability nouns or structural descriptions - describe what things DO
not what they ARE or CONTAIN

```
PaymentValidator Contains Validation Logic
```

```
Cart Hierarchy Foundation
```

```
Product Represents Item
```

Transform capabilities and structural descriptions into concrete actions

```
'Contains Logic' â†’ System --> generates XML or System --> renders diagram
```

```
'Tracks Count' â†’ System --> reads count or System --> updates count
```

```
'Represents X' â†’ System --> creates X or System --> loads X
```