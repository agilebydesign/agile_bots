---
title: write-concrete-scenarios
priority: 7
---

## write-concrete-scenarios

Parameterize domain concepts in scenarios using {Concept} notation for objects and {Concept.property} for specific attributes. Every {parameter} in Background/Steps MUST have corresponding example table. Use object references
not column names directly.

**DO**

Use {Concept} for object references
{Concept.property} for specific attributes. Connect to example tables.

Use {Concept} to reference domain objects
{Concept.property} for specific attributes

```
Given {User} is logged into ChannelOne 2.0
```

```
And {User} is entitled to {Entitlement}
```

```
And {Enterprise} has wire service enabled
```

```
When {Account} with {Account.activation_status} is selected
```

```
Then {WirePayment} holds {PaymentAmount.amount}
```

```
({Concept} = object reference, {Concept.property} = specific attribute when needed)
```

Background steps MUST have corresponding example tables

```
Background:
```

```
  Given {User} is logged into ChannelOne 2.0
```

```
  And {User} is entitled to {Entitlement}
```

```
  And {Enterprise} has wire service enabled
```

```
Example Tables (IDs omitted - they are implementation concerns):
```

```
User:
```

```
| user_name | user_role     |
```

```
| Jane Doe  | Wire Operator |
```

```
Entitlement (assigned entitlements for wire functions):
```

```
| entitlement_name     | entitlement_status |
```

```
| WirePayment.Create   | Granted            |
```

```
Enterprise:
```

```
| enterprise_name | wire_service_enabled |
```

```
| Acme Corp       | Yes                  |
```

Work backwards to base data - trace what must exist for scenario to be possible

```
Scenario: User enters payment amount
```

```
WORKING BACKWARDS:
```

```
- User enters PaymentAmount → User must exist
```

```
- User must exist → User must belong to Enterprise
```

```
- User must have Entitlement → Entitlement linked to User
```

```
- PaymentAmount entered on Account → Account must exist
```

```
- Account must belong to Enterprise → Account linked to Enterprise
```

```
BASE DATA REQUIRED:
```

```
1. Enterprise (root)
```

```
2. User (belongs to Enterprise)
```

```
3. Entitlement (granted to User)
```

```
4. Account (owned by Enterprise)
```

Each {Concept} maps to one example table - table columns are the concept's attributes

```
When {User} enters a {PaymentAmount}
```

```
Then {WirePayment} holds {PaymentAmount}
```

```
{PaymentAmount} in step maps to PaymentAmount table
```

```
Table columns ARE the concept's attributes - don't repeat them in the step
```

```
PaymentAmount (represents monetary value with currency):
```

```
| amount     | currency | formatted_display |
```

```
| 10000.00   | USD      | $10,000.00        |
```

Relate concepts using collaboration language from domain model

```
DOMAIN MODEL:
```

```
  WirePayment: 'holds payment amount and currency' -> [PaymentAmount]
```

```
  PaymentAmount: 'validated against transactional limits' -> [TransactionalLimit]
```

```
STEPS USE COLLABORATION VERBS:
```

```
  Then {WirePayment} holds {PaymentAmount}
```

```
  And {PaymentAmount} is validated against {TransactionalLimit}
```

```
(Concepts connected via their domain responsibilities, not jammed together)
```

Use domain collaborative language in table headers

```
Account (owned by enterprise):
```

```
| account_name           | current_balance |
```

```
| Acme Operating Account | $50,000.00      |
```

```
(Table name is concept, parenthetical is collaboration. No ID columns.)
```

**DO NOT**

Don't hardcode values without examples
don't use non-domain placeholders
don't skip base data dependencies.

Don't hardcode values inline without {parameter} and examples

```
Given User Jane Doe is logged in (WRONG - hardcoded, no {User} parameter)
```

```
Given User enters $10,000.00 (WRONG - hardcoded, no {PaymentAmount} parameter)
```

```
CORRECT: Given {User} enters {PaymentAmount}
```

Don't use arbitrary placeholder names - use domain concept names

```
Given <the_user> enters <amount> (WRONG - arbitrary names)
```

```
Given {some_value} is entered (WRONG - not a domain concept)
```

```
CORRECT: Given {User} enters a {PaymentAmount}
```

Don't put two {parameters} together without relating them in English

```
When {User} enters {PaymentAmount} {amount} (WRONG - {amount} is an attribute of PaymentAmount)
```

```
Then {WirePayment} {PaymentAmount} is saved (WRONG - concepts jammed together)
```

```
Given {Enterprise} {User} is logged in (WRONG - no relationship expressed)
```

```
CORRECT: When {User} enters a {PaymentAmount}
```

```
CORRECT: Then {WirePayment} holds {PaymentAmount}
```

```
CORRECT: Given {User} belonging to {Enterprise} is logged in
```

```
USE COLLABORATION LANGUAGE to relate concepts:
```

```
  {WirePayment} 'holds' {PaymentAmount} (from domain responsibility)
```

```
  {User} 'belonging to' {Enterprise} (from domain relationship)
```

Don't skip base data dependencies

```
Given User enters payment amount
```

```
(WRONG - no Enterprise, no Entitlement, no Account)
```

```
Must trace backwards: PaymentAmount → Account → Enterprise
```

```
                      User → Entitlement → Enterprise
```

Don't use calculated values as a substitute for source data. If a report has renames_count=1
show the actual renamed entity. Counts
booleans
and summaries are outputs - the scenario needs the inputs that produce them.

```
WRONG - calculated output without the source data that creates it:
```

```
  UpdateReport: | renames_count | new_count | | 1 | 2 |
```

```
CORRECT - source entities that the report is built from:
```

```
  UpdateReport (renames): | original_name | new_name | parent |
```

```
                          | Banking | Reconciliation | Wire Transfers |
```

```
  UpdateReport (new):     | name | parent |
```

```
                          | FX Conversion | Wire Transfers |
```

```
(The scenario specifies WHAT was renamed and added - not just how many)
```

Don't describe UI state as Given - describe data state

```
Given User is on PaymentDetails step (WRONG - UI navigation state)
```

```
CORRECT: Given {User} has selected {Account} belonging to {Enterprise}
```

```
(Data state - the selections that exist, not where the user 'is')
```

Don't omit examples for Background steps

```
Background:
```

```
  Given user is logged into ChannelOne 2.0
```

```
  And user is entitled to create wire payments
```

```
(WRONG - no example tables showing User, Entitlement)
```

```
CORRECT: Background steps have their own example tables
```