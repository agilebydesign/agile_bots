---
title: map-sequential-spine-vs-optional-paths
priority: 1
---

## map-sequential-spine-vs-optional-paths

When mapping stories
carefully distinguish between sequential spine (essential path) and optional paths
alternate routes
or additional functionality that is not strictly essential. Sequential stories form the mandatory flow; optional stories are alternatives
enhancements
or non-essential features.

**DO**

Identify the essential spine and mark optional paths clearly

Identify the minimum mandatory sequential flow required to deliver core value

```
User Registration Flow (spine):
```

```
  1. User enters email and password (sequential_order: 1, mandatory)
```

```
  2. User verifies email via link (sequential_order: 2, mandatory)
```

```
  3. User completes basic profile (sequential_order: 3, mandatory)
```

```
  4. User views dashboard (sequential_order: 4, mandatory)
```

Mark alternative authentication or workflow paths as optional since only one path is needed

```
User Authentication (spine + alternate):
```

```
  1. User enters credentials (sequential_order: 1, mandatory)
```

```
  2a. User logs in with email/password (sequential_order: 2, mandatory spine)
```

```
  2b. User logs in with Google (sequential_order: 2, optional: true alternate)
```

```
  2c. User logs in with Facebook (sequential_order: 2, optional: true alternate)
```

```
  3. User views dashboard (sequential_order: 3, mandatory)
```

Mark customization
personalization
and nice-to-have features as optional enhancements that branch from the spine

```
Dashboard Flow (spine + enhancements):
```

```
  1. User logs in (sequential_order: 1, mandatory)
```

```
  2. User views default dashboard (sequential_order: 2, mandatory)
```

```
  3. User customizes dashboard layout (optional: true, priority: 1 enhancement)
```

```
  4. User sets dashboard preferences (optional: true, priority: 2 enhancement)
```

```
  5. User shares dashboard with team (optional: true, priority: 3 enhancement)
```

Mark error handling and edge case scenarios as optional since the happy path is the essential spine

```
Order Processing (spine + error handling):
```

```
  1. Customer enters order details (sequential_order: 1, mandatory)
```

```
  2. System validates order (sequential_order: 2, mandatory)
```

```
  3. System processes payment (sequential_order: 3, mandatory)
```

```
  3a. System handles payment failure (optional: true, priority: 1 error handling)
```

```
  3b. System retries failed payment (optional: true, priority: 2 error handling)
```

```
  4. System confirms order (sequential_order: 4, mandatory)
```

**DO NOT**

Don't mark everything as sequential
don't omit optional markers

Don't treat alternative authentication methods as separate sequential steps - only one method is needed so alternatives should be optional

```
User Authentication (WRONG - all marked as spine):
```

```
  1. User enters credentials (sequential_order: 1)
```

```
  2. User logs in with email (sequential_order: 2)
```

```
  3. User logs in with Google (sequential_order: 3)
```

```
  4. User logs in with Facebook (sequential_order: 4)
```

```
Why Wrong: Only one authentication method is needed. Google and Facebook should be optional: true alternates.
```

Don't treat customization and enhancement features as part of the mandatory sequential spine - mark them as optional

```
Dashboard Flow (WRONG - enhancements marked as spine):
```

```
  1. User views dashboard (sequential_order: 1)
```

```
  2. User customizes layout (sequential_order: 2)
```

```
  3. User sets preferences (sequential_order: 3)
```

```
  4. User shares dashboard (sequential_order: 4)
```

```
Why Wrong: Only viewing dashboard is mandatory. Customization, preferences, and sharing should be optional: true enhancements.
```

Don't forget to mark error handling and edge cases as optional - they're not part of the essential happy path spine

```
Order Processing (WRONG - no optional markers):
```

```
  1. Customer enters order (sequential_order: 1)
```

```
  2. System processes payment (sequential_order: 2)
```

```
  3. System handles payment failure (sequential_order: 3)
```

```
  4. System retries payment (sequential_order: 4)
```

```
  5. System confirms order (sequential_order: 5)
```

```
Why Wrong: Payment failure and retry are error handling, not mandatory spine. Should be marked optional: true.
```