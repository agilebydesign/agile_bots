---
title: use-channel-specific-language
priority: 8
---

## use-channel-specific-language

Use channel-specific language with concrete examples. For Domain/API: show actual method calls. For CLI: show actual command syntax. For Panel/UI: show actual interactions and display elements. Don't use generic 'Bot does X' or 'System does Y' - be specific to the channel.

**DO**

Frame acceptance criteria in terms of how that channel actually works. Domain: method calls. CLI: command syntax. Panel: UI interactions.

Domain/API stories: Use actual resource/object names and method signatures

```
THEN parent Story Node creates new child node of appropriate type
```

```
(Example: child = bot.story_graph.epics["epic name"].createChild("child name"))
```

CLI stories: Show actual command syntax with dot notation or flags

```
WHEN User enters dot notation to create new child
```

```
EXAMPLE: cli.story_graph."Invoke Bot".create_sub_epic."Manage Bot Information"
```

```
THEN CLI parses dot notation path to parent node
```

Panel/UI stories: Show specific UI elements
interactions
and visual feedback

```
WHEN User selects Epic node in Story Tree
```

```
THEN Panel shows "Create Sub-Epic" button in action panel to the right
```

```
BUT does not show "Create Story" button
```

Include concrete examples in parentheses showing actual usage

```
(Example: child = bot.story_graph.epics["epic name"].createChild("child name", 2))
```

```
(Example: cli.story_graph."Invoke Bot".move_to."Other Epic".at_position.2)
```

**DO NOT**

Don't use generic 'Bot'
'System'
or 'User' without showing how it actually works in that channel. Example: Don't say 'Bot creates node' - show the actual API call or command

Don't use generic domain language that could apply to any channel

```
WHEN Bot creates child node
```

```
THEN Bot validates parent exists
```

```
AND Bot adds child to parent
```

Don't describe UI interactions without showing actual UI elements

```
WHEN User creates node in panel
```

```
THEN Panel displays node
```

Don't describe CLI without showing actual command syntax

```
WHEN User enters command to move node
```

```
THEN CLI validates command
```

```
AND CLI executes move
```

Don't omit examples for domain/API stories

```
THEN node adds itself to target
```