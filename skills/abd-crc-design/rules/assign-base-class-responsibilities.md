---
title: assign-base-class-responsibilities
priority: 2
---

## assign-base-class-responsibilities

When classes share responsibilities and collaborators
lift them into a base class. Use ': BaseClass' notation for inheritance. Reference base type in relationships instead of enumerating subtypes. Example: Scanner base with Scans/Reports; ImportPlacementScanner : Scanner adds Validates import ordering.

**DO**

Abstract shared responsibilities into base class
subclasses add specific ones. Example: Scanner base with Scans/Reports; ImportPlacementScanner : Scanner adds specific validation

Move repeated responsibilities and collaborators to base class

```
Scanner (base class with shared responsibilities)
```

```
    Scans scope for violations: Violation, Scope, Rule
```

```
    Reports violations: Violation, ViolationReport
```

```
ImportPlacementScanner : Scanner
```

```
    Validates import ordering: Boolean, Block, ImportRules
```

```
NamingConventionScanner : Scanner
```

```
    Validates identifier names: Boolean, Block, NamingRules
```

```
(Shared scan/report in base; specific validation in subclasses)
```

Reference base type in parent relationships

```
ScanOrchestrator
```

```
    Coordinates scan: Scan, Scanner, Scope (uses base Scanner type)
```

```
Scan
```

```
    Executes with scanner: Violation, Scanner, Rule (uses base Scanner type)
```

```
(Parent objects reference Scanner, not ImportPlacementScanner, NamingScanner, etc.)
```

Show inheritance clearly with ': BaseClass' notation

```
Payment (base class)
```

```
    Authorizes transaction: AuthorizationResult, PaymentGateway
```

```
    Get amount: Money
```

```
CreditCardPayment : Payment
```

```
    Validates card number: Boolean, CardNumber
```

```
    Validates expiration: Boolean, ExpirationDate
```

```
BankTransferPayment : Payment
```

```
    Validates routing number: Boolean, RoutingNumber
```

```
    Validates account number: Boolean, AccountNumber
```

```
(Subclasses inherit authorization, add specific validation)
```

**DO NOT**

Don't duplicate responsibilities or enumerate all subtypes. Example: Each scanner duplicating Scans/Reports (wrong) vs inheriting from Scanner base (right)

Don't repeat same responsibilities in every subclass

```
ImportPlacementScanner (WRONG: duplicates base responsibilities)
```

```
    Scans scope for violations: Violation, Scope, Rule
```

```
    Reports violations: Violation, ViolationReport
```

```
    Validates import ordering: Boolean, Block
```

```
NamingScanner (WRONG: duplicates base responsibilities)
```

```
    Scans scope for violations: Violation, Scope, Rule
```

```
    Reports violations: Violation, ViolationReport
```

```
    Validates names: Boolean, Block
```

```
(Scan/report duplicated - should be in base Scanner)
```

Don't list every concrete subtype when base type exists

```
ScanOrchestrator (WRONG: lists all concrete types)
```

```
    Coordinates scan: Scan, ImportPlacementScanner, NamingScanner, CommentScanner, ...
```

```
(Should use base Scanner type, not enumerate all scanners)
```