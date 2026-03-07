---
title: map-table-columns-to-scenario-parameters
priority: 9
---

## map-table-columns-to-scenario-parameters

Map example tables to {Concept} references bidirectionally. Every example table maps to a {Concept} in Background/Steps. Use {Concept} for object references and {Concept.property} for specific attributes. Keep tables minimal and domain-focused.

**DO**

Bidirectional mapping: Example table name ↔ {Concept} reference in steps.

Every {Concept} in Background/Steps has a matching example table

```
Given {User} is logged in → 'User' example table exists
```

```
And {User} is entitled to {Entitlement} → Both 'User' and 'Entitlement' tables exist
```

Every example table is referenced as {Concept} in steps

```
'User' table → Steps contain {User}
```

```
'Enterprise' table → Steps contain {Enterprise}
```

Use {Concept.property} when a specific attribute is important

```
Given {Account} with {Account.activation_status}
```

```
Then {Recipient.status} is Active
```

```
And {WirePayment} holds {PaymentAmount.amount}
```

Verification properties must be referenced in Then steps

```
'is_active' column → Then step uses {Recipient.is_active}
```

```
'expected_balance' column → Then {Account.expected_balance} is shown
```

**DO NOT**

Don't use <column_name> notation - use {Concept} or {Concept.property}. Don't have orphaned tables or references.

Don't use <column_name> notation - use {Concept} references

```
WRONG: Given User <user_name> is logged in
```

```
CORRECT: Given {User} is logged in
```

Don't have {Concept} without matching example table

```
Steps use {PaymentAmount} but no 'PaymentAmount' example table exists (WRONG)
```

Don't have example tables not referenced in steps

```
'ApprovalWorkflow' table exists but no {ApprovalWorkflow} in steps (WRONG)
```

Don't use column names directly in step text

```
WRONG: Given User <user_name> with <entitlement_name>
```

```
CORRECT: Given {User} is entitled to {Entitlement}
```