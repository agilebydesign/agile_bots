---
title: map-bidirectional-collaborators
priority: 4
---

## map-bidirectional-collaborators

Map domain concept collaborators bidirectionally. When concept A has a collaborator B (non-primitive)
concept B should have a corresponding responsibility that references A
describing the same relationship from B's perspective. Primitives (String
Number
Boolean
Date
Integer) are exceptions—they do not require bidirectional mapping.

**DO**

Describe the same relationship from both collaborators' perspectives

When A references B as collaborator
B should reference A—mapped perspectives of the same relationship

```
Campaign
```

```
    Generates vouchers: Voucher, VoucherCodeGenerator
```

```
Voucher
```

```
    Generated for a campaign: Campaign
```

```
(Campaign generates Voucher → Voucher is generated for Campaign. Same relationship, both perspectives.)
```

Use responsibility names that describe the relationship from each concept's viewpoint

```
Order
```

```
    Contains line items: LineItem
```

```
LineItem
```

```
    Belongs to order: Order
```

```
Portfolio
```

```
    Holds holdings: Holding
```

```
Holding
```

```
    Held in portfolio: Portfolio
```

```
(Each side describes the relationship from its own perspective.)
```

**DO NOT**

Don't leave collaborator relationships one-way or use mismatched collaborators

Don't have one-way collaborator—if A references B
B should reference A (unless B is primitive)

```
Campaign
```

```
    Generates vouchers: Voucher, VoucherCodeGenerator
```

```
Voucher
```

```
    (WRONG: no responsibility referencing Campaign—relationship is one-way)
```

```
(Voucher should have a responsibility like 'Generated for a campaign: Campaign')
```

Don't use mismatched collaborators—the bidirectional pair must describe the SAME relationship

```
Campaign
```

```
    Generates vouchers: Voucher, VoucherCodeGenerator
```

```
Voucher
```

```
    Inherits metadata from campaign: Campaign
```

```
(WRONG: 'Inherits metadata' describes a different aspect of the relationship than 'Generates vouchers'. They are not the same bidirectional pair.)
```

```
CORRECT:
```

```
Voucher
```

```
    Generated for a campaign: Campaign
```

```
(This maps to Campaign's 'Generates vouchers'—same relationship, both perspectives.)
```

Don't require bidirectional mapping for primitive collaborators

```
Voucher
```

```
    Is identified by code: String
```

```
(String is primitive—no need for 'String' to reference Voucher. Primitives are exceptions.)
```