---
title: respect-existing-delegation
priority: 2
---

## respect-existing-delegation

DO NOT add responsibilities that are already fulfilled through delegation to existing collaborators. If a class has a collaborator whose domain already covers an operation
the class orchestrates through that collaborator - it doesn't duplicate the work. Example: StoryNode has StoryNodeChildren collaborator
so Add child/Remove child/Find child are already handled - don't add them again.

**DO**

Add ONLY responsibilities that are NEW business rules
coordinate multiple collaborators
or introduce NEW capabilities not covered by existing collaborators

Add NEW business constraints that are unique to the class - not generic operations

```
SubEpic
```

```
    Contains Children: StoryNodeChildren
```

```
    Validate cannot mix Sub-Epics and Stories: StoryNodeChildren
```

```
(Validation is NEW constraint specific to SubEpic - not a generic child operation)
```

Add coordination logic that spans multiple collaborators or collections

```
Story
```

```
    Contains Children: StoryNodeChildren
```

```
    Maintain separate sequential ordering for scenarios and acceptance criteria: StoryNodeChildren
```

```
(Coordination of ordering rules across multiple child types - not just 'add child')
```

Add NEW capabilities that delegate to NEW collaborators not previously used

```
StoryNode
```

```
    Serializes: StoryNodeSerializer
```

```
    Contains Children: StoryNodeChildren
```

```
    Execute action scoped to node: Action,Parameters,Bot
```

```
(NEW capability delegating to Bot - not covered by existing collaborators)
```

Trust that existing collaborators already handle their domain - don't restate their work

```
StoryNode
```

```
    Contains Children: StoryNodeChildren
```

```
    (DON'T add: Add child, Remove child, Find child - StoryNodeChildren already handles)
```

```
StoryNode
```

```
    Serializes: StoryNodeSerializer
```

```
    (DON'T add: Save to file, Load from file - StoryNodeSerializer already handles)
```

```
StoryNode
```

```
    Get position: StoryNodeNavigator
```

```
    (DON'T add: Move to parent, Move after - StoryNodeNavigator already handles)
```

**DO NOT**

Don't add responsibilities that restate what existing collaborators already do. Don't add child operations when you have a Children collection. Don't add serialization when you have a Serializer. Don't add navigation when you have a Navigator.

Don't duplicate operations already handled by Collection/Children collaborators

```
StoryNode (WRONG: duplicating StoryNodeChildren's work)
```

```
    Contains Children: StoryNodeChildren
```

```
    Create child: Name,Position,ChildNodeFactory,StoryNodeChildren
```

```
    Add existing child: StoryNode,Position,StoryNodeChildren
```

```
    Remove child: StoryNode,StoryNodeChildren
```

```
    Find child by name: Name,StoryNodeChildren
```

```
    Resequence children: Position,StoryNodeChildren
```

```
(All of these are already handled by StoryNodeChildren - don't add them!)
```

Don't duplicate operations already handled by Serializer/Persister collaborators

```
StoryMap (WRONG: duplicating StoryNodeSerializer's work)
```

```
    Serializes: StoryNodeSerializer
```

```
    Write updated graph to file: File,StoryNodeSerializer
```

```
    Verify write successful: File
```

```
    Load from file: File,StoryNodeSerializer
```

```
    Update node in storage: StoryNode,File
```

```
(All of these are already handled by StoryNodeSerializer - don't add them!)
```

Don't duplicate operations already handled by Navigator/Positioner collaborators

```
StoryNode (WRONG: duplicating StoryNodeNavigator's work)
```

```
    Get position: StoryNodeNavigator
```

```
    Move to parent: Parent,Position,StoryNodeNavigator
```

```
    Move after: StoryNode,StoryNodeNavigator
```

```
    Move before: StoryNode,StoryNodeNavigator
```

```
    Calculate position: Float,StoryNodeNavigator
```

```
(All of these are already handled by StoryNodeNavigator - don't add them!)
```

Don't expand 'Get X' into low-level implementation steps when collaborator already exists

```
Story (WRONG: expanding what StoryNodeChildren already handles)
```

```
    Contains Children: StoryNodeChildren
```

```
    Get scenarios: List[Scenario],StoryNodeChildren
```

```
    Get scenario outlines: List[ScenarioOutline],StoryNodeChildren
```

```
    Get acceptance criteria: List[AcceptanceCriteria],StoryNodeChildren
```

```
    Add to scenario collection: Scenario,StoryNodeChildren
```

```
    Add to acceptance criteria collection: AcceptanceCriteria,StoryNodeChildren
```

```
(StoryNodeChildren already provides access to all children - these are implementation details)
```

Don't add 'Rename' or 'Update name' when base class already has 'Get/Update name'

```
StoryNode (base class already has)
```

```
    Get/Update name: String
```

```
Epic : StoryNode (WRONG: duplicating base's work)
```

```
    Rename: Name,StoryNodeChildren
```

```
    Update name: String,StoryNodeChildren
```

```
(Base class already handles name updates - don't duplicate!)
```

Don't add validation steps that are generic 'before save' checks

```
StoryMap (WRONG: low-level validation steps)
```

```
    Serializes: StoryNodeSerializer
```

```
    Check all node references valid: StoryNode,GraphValidator
```

```
    Check sequential order consistency: StoryNode,GraphValidator
```

```
    Prevent persistence on violations
```

```
    Roll back in-memory changes on failure
```

```
(These are implementation details of persistence - GraphValidator already handles)
```