---
title: story-map-existing-code
priority: 8
---

## story-map-existing-code

When creating story maps from code
start with the outermost layer (entry points)
analyze operations
create epics from higher-order goals
and lay out the story journey.

**DO**

Start with entry points and trace to epics and stories. Example: Operations 'render-outline
render-increments' → Goal 'Render StoryGraph' → Epic 'Render StoryGraph'

Step 1: Find Entry Points (CLI commands
UI entry points
MCP server tools
API contracts
acceptance tests)

```
CLI commands (main(), argparse)
```

```
UI entry points (routes, handlers, button clicks)
```

```
MCP server tools (names, parameters)
```

```
API contracts (REST, GraphQL, WSDL)
```

```
Acceptance tests (end-to-end, BDD)
```

Step 2: Analyze Operations (list operations
group by functional purpose)

Step 3: Create Epics from Goals (group operations by higher-order goals
create epics from goals NOT class structure)

```
Operations 'render-outline, render-increments' → Goal 'Render StoryGraph' → Epic 'Render StoryGraph'
```

Step 4: Create Sub-Epics from Behaviors (identify distinct behaviors for each epic
group into sub-epics)

```
Epic 'Render StoryGraph' → Sub-Epics 'Render Outline', 'Render Increments'
```

Step 5: Lay Out Story Journey (trace code flow: Start → Middle → End
include WHEN/WHY/OUTCOME/ACTOR
include error handling)

```
User --> invokes command, System --> validates input, System --> processes, System --> confirms
```

**DO NOT**

Don't start with internal classes or create epics from class structure. Example: Creating epics from class structure (WRONG) → Create epics from goals (CORRECT)

Don't start with internal classes instead of entry points - don't create epics from class structure instead of goals - don't create stories from every method call - don't miss context (when/why/outcome) in stories - don't make implementation details into stories

```
Starting with internal classes instead of entry points
```

```
Creating epics from class structure instead of goals
```

```
Creating stories from every method call
```

```
Missing context (when/why/outcome) in stories
```

```
Making implementation details into stories
```