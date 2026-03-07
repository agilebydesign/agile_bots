---
title: use-object-flow-format
priority: 1
---

## use-object-flow-format

Write walkthrough realizations using explicit object flow notation with Object.method(param: value)
nested calls with -> indentation
and actual return values. Example: result: 'text' = Object.method(param: 'value') -> nested: True = Collaborator.check() return nested: True

**DO**

Use explicit notation showing objects
methods
parameters
and actual data values. Example: output: 'Build...' = REPLSession.run_repl_loop() -> command: {behavior: 'shape'} = CommandParser.parse_command(input_line: 'shape.build')

Show object
method
explicit parameters and return values with actual data. Example: output: 'Build knowledge graph...' = REPLSession.run_repl_loop() -> is_interactive: True = TTYDetector.is_interactive() -> command: {behavior: 'shape'
action: 'build'} = CommandParser.parse_command(input_line: 'shape.build.instructions')

```
REPLSession
```

```
    output: 'Build knowledge graph...\n\nSTORY_BOT CLI...' = REPLSession.run_repl_loop()
```

```
        -> is_interactive: True = TTYDetector.is_interactive()
```

```
        -> command: {behavior: 'shape', action: 'build', operation: 'instructions'} = CommandParser.parse_command(input_line: 'shape.build.instructions')
```

```
            -> behavior_name: 'shape' = CommandParser.extract_behavior(input_line: 'shape.build.instructions')
```

```
            return command: {behavior: 'shape', action: 'build', operation: 'instructions'}
```

```
        return output: 'Build knowledge graph...\n\nSTORY_BOT CLI...'
```

```
(Shows: Object.method(params), nested calls with ->, actual return values)
```

Use -> for nested calls to show delegation depth. Example: result: 'text' = Object.method() -> nested: value = Collaborator.method() -> deeper: data = Another.method() return deeper: data

```
CLIBot
```

```
    result: 'Scope set to: Story1, Story2' = CLIScope.set_scope(scope_string: 'Story1, Story2')
```

```
        -> scope: {type: STORY, value: ['Story1', 'Story2']} = CLIScope._parse_scope_string(scope_string: 'Story1, Story2')
```

```
            -> scope_type: STORY = Scope.infer_type(value: ['Story1', 'Story2'])
```

```
            return scope: {type: STORY, value: ['Story1', 'Story2'], filter: <KnowledgeGraphFilter>}
```

```
        return result: 'Scope set to: Story1, Story2'
```

```
(Each -> shows one level deeper in call stack)
```

Show actual data values in returns not class names. Example: -> command: {behavior: 'shape'
action: 'build'} = parse_command() NOT -> command = CommandResult()

```
GOOD:
```

```
-> command: {behavior: 'shape', action: 'build'} = parse_command(input: 'shape.build')
```

```
-> is_valid: True = validate(story: 'Story1')
```

```
-> result: 'Build complete' = execute()
```

```
BAD:
```

```
-> command = parse_command(input)
```

```
-> is_valid = validate(story)
```

```
-> result = CommandResult()
```

```
(Show actual values: strings, bools, dicts, lists - not class constructors)
```

Use result: value = method() format consistently. Example: validation: [('Story1'
True)] = Scope.validate_scope(story_graph) NOT validation = validate()

```
-> cli_behavior: <CLIBehavior wrapping shape> = CLIBot.behaviors.get_behavior(name: 'shape')
```

```
-> validation: [('Story1', True), ('Story2', True)] = Scope.validate_scope(story_graph)
```

```
-> status: 'STORY_BOT CLI\n[x] shape...' = StatusDisplay.render(CLIBot)
```

```
(Format: variable: actual_value = Object.method(param: value))
```

**DO NOT**

Don't use vague pseudo-code or hide object/method/parameter details. Example: command = parse_command(input) (wrong - no object
no data) vs command: {behavior: 'shape'} = CommandParser.parse_command(input_line: 'shape.build') (right)

Don't omit object names or method names. Example: command = parse_command(input) (wrong) vs command: {...} = CommandParser.parse_command(input_line: 'shape.build.instructions') (right)

```
BAD:
```

```
-> command = parse_command(input)
```

```
-> result = execute_operation(operation)
```

```
GOOD:
```

```
-> command: {...} = CommandParser.parse_command(input_line: 'shape.build.instructions')
```

```
-> result: '...' = cli_action.execute_operation(operation: 'instructions', args: '')
```

```
(Always show which object and which method)
```

Don't show class constructors as return values. Example: return Scope(type: STORY) (wrong) vs return scope: {type: STORY
filter: <KnowledgeGraphFilter>} (right)

```
BAD:
```

```
return CLIBehavior(domain_behavior)
```

```
return Scope(type: STORY, value: ['Story1'])
```

```
return KnowledgeGraphFilter()
```

```
GOOD:
```

```
return cli_behavior: <CLIBehavior wrapping shape>
```

```
return scope: {type: STORY, value: ['Story1'], filter: <KnowledgeGraphFilter>}
```

```
return filter: <KnowledgeGraphFilter>
```

```
(Show object instances with <>, or show data values, not constructors)
```

Don't use generic descriptions instead of actual flow. Example: 'Session processes command' (wrong) vs command: {behavior: 'shape'} = CommandParser.parse_command(input_line: 'shape.build') (right)

```
BAD:
```

```
Session processes command and returns result
```

```
Action executes and formats output
```

```
GOOD:
```

```
-> command: {behavior: 'shape', action: 'build'} = CommandParser.parse_command(input_line: 'shape.build.instructions')
```

```
-> result: 'Build knowledge graph...' = cli_action.execute_operation(operation: 'instructions')
```

```
    -> context: {} = CLIAction._parse_args_to_context(args: '')
```

```
    -> formatted: 'Build knowledge graph...' = CLIAction._format_result(instruction_dict)
```

```
    return result: 'Build knowledge graph...'
```

```
(Show actual method calls with actual data, not narrative descriptions)
```