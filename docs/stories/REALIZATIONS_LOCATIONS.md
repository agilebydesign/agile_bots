# Realizations in Story Graph

This document lists all domain concept realizations and their exact locations in the story graph hierarchy.

## Summary

**Total Realizations: 12**

- **Story Graph Realizations**: 4 (in `Invoke Bot > Work With Story Map > Edit Story Map`)
- **Panel/CLI Realizations**: 8 (distributed across multiple sub-epics)

---

## Part 1: Story Graph Realizations

**Location**: `Invoke Bot > Work With Story Map > Edit Story Map`

### 1. StoryNode (Base) - Realization 1

**Concept**: `StoryNode (Base)`  
**Module**: `story_graph.nodes`  
**Location**: `Invoke Bot > Work With Story Map > Edit Story Map`

**Scope**: `Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph.Create Child Story Node.Create child node with specified position`

**Scenario**: Parent node creates new child at specific position, shifting existing children and maintaining sequential order

**Walks**:
- Steps 1-2 (Initialize parent, validate position)
- Step 3 (Create child and insert at position)

**Model Updates**:
- Added 'Create child node with name and position' responsibility to StoryNode
- Added 'Validate child name unique among siblings' responsibility to StoryNode
- Added 'Adjust position to valid range' responsibility to StoryNode
- Added 'Resequence children after insert or delete' responsibility to StoryNode
- Added NodeValidator as collaborator for validation operations
- Added Parent as collaborator for delete operations

---

### 2. StoryNode (Base) - Realization 2

**Concept**: `StoryNode (Base)`  
**Module**: `story_graph.nodes`  
**Location**: `Invoke Bot > Work With Story Map > Edit Story Map`

**Scope**: `Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph.Delete Story Node.Delete node including children (cascade delete)`

**Scenario**: Node with descendants is deleted using cascade option, removing entire subtree and resequencing siblings

**Walks**:
- Steps 1-3 (Locate node, count descendants, initiate cascade delete)
- Steps 4-5 (Recursively delete descendants, remove from parent)

**Model Updates**:
- Added 'Delete self and handle children' responsibility to StoryNode
- Confirmed 'Resequence children after insert or delete' handles both insert and delete cases
- Added recursive deletion pattern for cascade deletes

---

### 3. SubEpic - Realization

**Concept**: `SubEpic`  
**Module**: `story_graph.sub_epic`  
**Location**: `Invoke Bot > Work With Story Map > Edit Story Map`

**Scope**: `Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph.Create Child Story Node.SubEpic with SubEpics cannot create Story child`

**Scenario**: SubEpic that already contains SubEpic children rejects attempt to add Story child, maintaining hierarchy rules

**Walks**:
- Steps 1-4 (Attempt Story creation, validate hierarchy, reject with error)

**Model Updates**:
- Added 'Create StoryGroup when first Story added' responsibility to SubEpic
- Added 'Check child type compatibility before add' responsibility to SubEpic
- Clarified that 'Validate cannot mix Sub-Epics and Stories' is used during create_child operations

---

### 4. Story - Realization

**Concept**: `Story`  
**Module**: `story_graph.story`  
**Location**: `Invoke Bot > Work With Story Map > Edit Story Map`

**Scope**: `Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph.Create Child Story Node.Story creates child and adds to correct collection`

**Scenario**: Story creates Scenario and AcceptanceCriteria children, routing each to separate collections with independent ordering

**Walks**:
- Steps 1-3 (Create Scenario child, route to scenarios collection)
- Steps 4-6 (Create AcceptanceCriteria child, route to separate collection with independent ordering)

**Model Updates**:
- Added 'Route child to correct collection by type' responsibility to Story
- Added ScenarioCollection and AcceptanceCriteriaCollection as collaborators
- Clarified that 'Maintain separate sequential ordering' means independent position counters per collection

---

## Part 2: Panel/CLI Realizations

### 5. PanelView (Base) - Realization 1

**Concept**: `PanelView (Base)`  
**Module**: `panel`  
**Location**: `Invoke Bot > Initialize Bot > Render Bot Interface`

**Scope**: `Invoke Bot Through Panel.Manage Bot Information.Open Panel`

**Scenario**: User activates panel command, extension creates panel and displays bot information by calling Python CLI, wrapping JSON response, and rendering all sections

**Walks**:
- Extension activation and panel creation
- Panel constructor and section rendering

---

### 6. PanelView (Base) - Realization 2

**Concept**: `PanelView (Base)`  
**Module**: `panel`  
**Location**: `Invoke Bot > Initialize Bot > Render Bot Interface`

**Scope**: `Invoke Bot Through Panel.Manage Bot Information.Refresh Panel`

**Scenario**: User clicks refresh button, panel calls CLI to get updated status, wraps new JSON, and re-renders all sections

**Walks**:
- User refresh action and CLI round-trip

---

### 7. BehaviorsView - Realization 1

**Concept**: `BehaviorsView`  
**Module**: `behaviors`  
**Location**: `Invoke Bot > Navigate Behavior Actions > Display Behavior Action State`

**Scope**: `Invoke Bot Through Panel.Navigate Behavior Action Status.Display Hierarchy`

**Scenario**: Panel displays behavior hierarchy with actions, user expands/collapses behaviors (instant), completion status from JSON

**Walks**:
- Rendering behavior hierarchy from JSON
- User expands behavior (client-side toggle)

---

### 8. BehaviorsView - Realization 2

**Concept**: `BehaviorsView`  
**Module**: `behaviors`  
**Location**: `Invoke Bot > Navigate Behavior Actions > Display Behavior Action State`

**Scope**: `Invoke Bot Through Panel.Navigate Behavior Action Status.Execute Behavior Action`

**Scenario**: User clicks behavior to execute, system navigates to behavior and executes first action via CLI

**Walks**:
- User executes behavior via CLI

---

### 9. StoryMapView - Realization

**Concept**: `StoryMapView`  
**Module**: `story_graph.story_map`  
**Location**: `Invoke Bot > Work With Story Map > Edit Story Map`

**Scope**: `Invoke Bot Through Panel.Filter And Navigate Scope.Display Story Scope Hierarchy`

**Scenario**: Panel displays nested epic/sub-epic/story/scenario hierarchy from story graph JSON, user can expand/collapse and navigate

**Walks**:
- Rendering 4-level nested hierarchy from JSON
- User opens epic folder via CLI

---

### 10. EpicView - Realization

**Concept**: `EpicView`  
**Module**: `story_graph.epic`  
**Location**: `Invoke Bot > Work With Story Map > Edit Story Map`

**Scope**: `Invoke Bot Through Panel.Filter And Navigate Scope.Display Story Scope Hierarchy`

**Scenario**: Panel displays nested epic/sub-epic/story/scenario hierarchy from story graph JSON, user can expand/collapse and navigate

**Walks**:
- Rendering 4-level nested hierarchy from JSON
- User opens epic folder via CLI

---

### 11. ScopeView - Realization

**Concept**: `ScopeView`  
**Module**: `scope`  
**Location**: `Invoke Bot > Work With Story Map > Scope Stories > Manage Story Scope`

**Scope**: `Invoke Bot Through Panel.Filter And Navigate Scope.Filter Story Scope`

**Scenario**: User types story name in filter, system calls CLI to update scope filter, returns filtered JSON, view re-renders with filtered hierarchy

**Walks**:
- User filters scope via CLI

---

### 12. ClarifyInstructionsSection - Realization

**Concept**: `ClarifyInstructionsSection`  
**Module**: `actions.clarify`  
**Location**: `Invoke Bot > Perform Action > Clarify Requirements`

**Scope**: `Invoke Bot Through Panel.Display Instructions.Display Clarify Instructions`

**Scenario**: When current action is clarify, panel displays ClarifyInstructionsSection with key questions in editable textareas, user edits answer, system saves via CLI

**Walks**:
- Rendering clarify-specific instructions from JSON
- User edits answer and saves via CLI

---

## Notes

- **Story Graph Realizations** (1-4): All relate to creating or deleting child nodes in the story graph hierarchy
- **Panel/CLI Realizations** (5-12): Document panel rendering, behavior navigation, scope filtering, and instruction display workflows
- All realizations include complete object flows showing method calls, parameters, and collaborations
- Full details including complete object flows are available in `story_graph_hierarchical_view.md`
- Realizations are stored as `realization` arrays in domain concepts in `story-graph.json`
