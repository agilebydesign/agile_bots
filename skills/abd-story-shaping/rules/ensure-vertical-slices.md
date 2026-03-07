---
title: ensure-vertical-slices
priority: 9
---

## ensure-vertical-slices

Ensure increments remain vertical slices (end-to-end flows across multiple epics/features
NOT horizontal layers). Each increment must deliver a complete working flow.

**DO**

Design increments as vertical slices with end-to-end flows

Include partial features from multiple epics in each increment to create complete end-to-end working flow

```
Increment 1: Basic Order Flow
```

```
  Epic: Order Entry (2/5) - create order with name and item, validate basic info
```

```
  Epic: Payment Processing (1/3) - process payment manually via admin tool
```

```
  Epic: Order Storage (1/3) - save order to file
```

```
  Epic: Order Display (1/4) - view order confirmation
```

```
  Result: Complete flow from order entry through payment to confirmation
```

Each increment demonstrates working software from start to finish
not just one layer

```
Increment 1: Manual Character Creation
```

```
  Epic: Character Creation (2/8) - enter character name, assign basic abilities manually
```

```
  Epic: Character Storage (1/3) - save character to file
```

```
  Epic: Character Display (1/5) - view basic character sheet
```

```
  Result: Can create, save, and view a character (complete vertical slice)
```

**DO NOT**

Don't create horizontal layer increments that complete one epic at a time

Don't complete all features in one epic before moving to the next epic

```
Increment 1: Complete Epic A (all features done)
```

```
Increment 2: Complete Epic B (all features done)
```

```
WRONG: This creates horizontal layers that can't be tested end-to-end until final increment
```

Don't create increments that only touch one part of the system without complete flow

```
Increment 1: Order Entry Complete
```

```
  Epic: Order Entry (8/8) - all order entry features complete
```

```
  NO payment, NO storage, NO confirmation
```

```
WRONG: Can't deliver working software, can't test end-to-end flow
```