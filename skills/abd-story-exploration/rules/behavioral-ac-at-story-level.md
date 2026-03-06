---
title: behavioral-ac-at-story-level
priority: 4
---

## behavioral-ac-at-story-level

not technical implementation. Example: "WHEN user enters name THEN system saves to character sheet"

**DO**

Use behavioral language describing user actions and system responses. Example: "WHEN action completes THEN system saves state AND system shows success"

Use behavioral terms that describe what happens
not how it's implemented

```
"WHEN user enters name THEN system saves character information" (behavioral)
```

```
"WHEN user submits form THEN system validates data AND system displays confirmation" (behavioral)
```

Focus on user-observable outcomes and system responses

```
"WHEN user clicks save THEN system persists changes AND system shows success message"
```

```
"WHEN user loads page THEN system displays saved data"
```

WHEN/THEN/AND can be on separate lines in the array - this is acceptable

```
["WHEN user enters name", "THEN system saves", "AND system displays confirmation"] - This format is OK
```

**DO NOT**

Don't use technical implementation terms like config
json
api
sql
class
method. Example: "WHEN system parses JSON config" (technical - use behavioral language instead)

Don't use technical file format terms

```
"THEN system saves to JSON file" - WRONG: use "system saves configuration data"
```

```
"THEN system parses XML" - WRONG: use "system processes data"
```

Don't use programming terms

```
"THEN system calls method" - WRONG: use "system performs action"
```

```
"THEN class instantiates" - WRONG: use "system creates instance"
```

Don't use database or API terminology

```
"THEN system executes SQL query" - WRONG: use "system retrieves data"
```

```
"THEN API endpoint returns" - WRONG: use "system responds with data"
```