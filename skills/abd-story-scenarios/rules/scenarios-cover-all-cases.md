---
title: scenarios-cover-all-cases
priority: 5
---

## scenarios-cover-all-cases

Scenarios must cover happy path
edge cases
and error cases based on acceptance criteria. Example: Valid input → success; Boundary value → validates; Invalid input → error message.

**DO**

Cover all case types: happy path
edge cases
error cases. Example: User enters valid data → success; User enters boundary → validates; User enters invalid → error

Include happy path scenario

```
Scenario: User enters valid data - When user submits valid form Then system saves successfully
```

Include edge case scenarios

```
Scenario: User enters boundary value - When user enters maximum allowed value Then system validates correctly
```

Include error case scenarios

```
Scenario: User enters invalid data - When user submits empty form Then system shows validation error
```

**DO NOT**

Don't skip case types. Example: Only happy path scenarios (missing edge and error cases)

Don't cover only happy path

```
Only 'User submits valid data' scenario - MISSING edge cases and error cases
```

Don't assume error handling is implicit

```
No explicit error scenarios - must show what happens when things fail
```