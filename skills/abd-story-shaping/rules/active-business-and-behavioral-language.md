---
title: active-business-and-behavioral-language
priority: 2
---

## active-business-and-behavioral-language

Use active business language focused on user/system behavior. Describe what actors do with clear action verbs
not technical implementation or passive constructions.

**DO**

Use active voice with business language. Example: 'User --> submit order' (active voice
base verb form
business language describing what actor does)

Use base verb forms (infinitive/imperative) to describe what happens in active voice with business language focused on user/system behavior

```
User --> submit order
```

```
System --> validate payment
```

```
Customer --> place order
```

```
Admin --> approve request
```

Action verbs that describe user/system behavior clearly - use base verb forms like submit
view
validate
send
display
place
edit
create
load
save
invoke
process
generate
update

```
User --> submit form
```

```
Customer --> view product catalog
```

```
System --> validate input data
```

```
Admin --> send notification
```

```
System --> display results
```

```
User --> place order
```

```
Developer --> edit configuration
```

```
System --> create report
```

```
User --> load dashboard
```

```
System --> save changes
```

```
User --> invoke command
```

```
System --> process payment
```

```
System --> generate invoice
```

```
Admin --> update settings
```

Prefer user/system stories over technical stories - transform technical language into business behavior. Wrong: 'Set up database schema' (technical). Correct: 'System --> store user data' (business
user story).

```
System --> store user data (not 'Set up database schema')
```

```
System --> expose user data via API (not 'Create API endpoint')
```

```
Developer --> verify story behavior (not 'Write unit tests')
```

When technical stories are necessary
mark with story_type: 'technical' and keep minimal and focused

```
System --> migrate legacy data format (story_type: 'technical')
```

```
Developer --> refactor authentication module (story_type: 'technical')
```

**DO NOT**

Don't use passive voice or technical implementation language. Example: 'Order is submitted' (passive voice
unclear actor) â†' 'User --> submit order' (active voice
base verb form
clear actor)

Don't describe behaviors passively or vaguely - always use active voice with base verb forms that clearly identifies who performs the action. Wrong: 'Order is submitted' (passive - by whom?). Correct: 'User --> submit order' (active
base verb
clear actor).

```
User --> submit order (not 'Order is submitted')
```

```
System --> validate payment (not 'Payment gets validated')
```

```
User --> place order (not 'Order is placed by user')
```

Don't use technical implementation details or development task language - focus on business behavior. Wrong: 'Developer --> write code'
'Developer --> create class'. Correct: 'Developer --> implement feature'
'System --> store data'.

```
Developer --> write code
```

```
Developer --> create class
```

```
Developer --> add method
```

```
Developer --> set up CI/CD
```

```
Developer --> configure database
```

```
Developer --> install package
```

```
Developer --> implement order system
```

```
Developer --> create database schema
```

```
System --> query database
```

```
System --> call API
```

```
System --> update table
```

Development task verbs to avoid - these describe implementation
not business behavior. Use business language instead.

```
Developer --> implement feature (avoid)
```

```
Developer --> create module (avoid)
```

```
Developer --> refactor code (avoid)
```

```
Developer --> optimize performance (avoid)
```

```
Developer --> fix bug (avoid)
```

```
Developer --> build system (avoid)
```

```
Developer --> set up infrastructure (avoid)
```