# All Walkthroughs and Realizations

This document lists ALL walkthroughs/realizations, including those stored as realizations in domain concepts and those documented separately.

## Summary

- **Stored as Realizations in JSON**: 4 (Story Graph)
- **Documented in Walkthrough Files**: 11 total
  - Story Graph: 4 (same as JSON)
  - Panel/CLI: 7 (NOT stored as realizations)

---

## Part 1: Realizations Stored in story-graph.json

These are stored as `realization` arrays in domain concepts and are currently restored.

**Location**: `Invoke Bot > Work With Story Map > Edit Story Map`

### 1. StoryNode (Base) - Create Child Node with Specified Position
- **Scope**: `Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph.Create Child Story Node.Create child node with specified position`
- **File**: `docs/crc/walkthroughs/story-graph-walkthrough.md` (Scenario 1)
- **Status**: ✅ Stored in JSON

### 2. StoryNode (Base) - Delete Node Including Children (Cascade Delete)
- **Scope**: `Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph.Delete Story Node.Delete node including children (cascade delete)`
- **File**: `docs/crc/walkthroughs/story-graph-walkthrough.md` (Scenario 2)
- **Status**: ✅ Stored in JSON

### 3. SubEpic - SubEpic with SubEpics Cannot Create Story Child
- **Scope**: `Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph.Create Child Story Node.SubEpic with SubEpics cannot create Story child`
- **File**: `docs/crc/walkthroughs/story-graph-walkthrough.md` (Scenario 3)
- **Status**: ✅ Stored in JSON

### 4. Story - Story Creates Child and Adds to Correct Collection
- **Scope**: `Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph.Create Child Story Node.Story creates child and adds to correct collection`
- **File**: `docs/crc/walkthroughs/story-graph-walkthrough.md` (Scenario 4)
- **Status**: ✅ Stored in JSON

---

## Part 2: Walkthroughs Documented but NOT Stored as Realizations

These walkthroughs are documented in `docs/crc/walkthroughs/panel_cli_walkthroughs.md` but are **NOT** stored as `realization` arrays in domain concepts.

### 5. Panel - Open Panel
- **Scope**: `Invoke Bot Through Panel.Manage Bot Information.Open Panel`
- **Concepts Traced**: Panel, BotHeaderView, PathsSection, BehaviorsSection, ScopeSection, InstructionsSection
- **File**: `docs/crc/walkthroughs/panel_cli_walkthroughs.md` (Scenario 1)
- **Should be stored in**: Domain concepts for PanelView (Base) or related panel concepts
- **Location**: `Invoke Bot > Initialize Bot > Render Bot Interface` (or appropriate panel sub-epic)
- **Status**: ❌ NOT stored in JSON

### 6. Panel - Refresh Panel
- **Scope**: `Invoke Bot Through Panel.Manage Bot Information.Refresh Panel`
- **Concepts Traced**: Panel, BotHeaderView
- **File**: `docs/crc/walkthroughs/panel_cli_walkthroughs.md` (Scenario 2)
- **Should be stored in**: Domain concepts for PanelView (Base) or BotHeaderView
- **Location**: `Invoke Bot > Initialize Bot > Render Bot Interface`
- **Status**: ❌ NOT stored in JSON

### 7. BehaviorsSection - Display Hierarchy
- **Scope**: `Invoke Bot Through Panel.Navigate Behavior Action Status.Display Hierarchy`
- **Concepts Traced**: BehaviorsSection, BehaviorView
- **File**: `docs/crc/walkthroughs/panel_cli_walkthroughs.md` (Scenario 3)
- **Should be stored in**: Domain concepts for BehaviorsView or SectionView
- **Location**: `Invoke Bot > Navigate Behavior Actions > Display Behavior Action State`
- **Status**: ❌ NOT stored in JSON

### 8. BehaviorsSection - Execute Behavior Action
- **Scope**: `Invoke Bot Through Panel.Navigate Behavior Action Status.Execute Behavior Action`
- **Concepts Traced**: BehaviorsSection, BehaviorView, Bot, Behavior, Action
- **File**: `docs/crc/walkthroughs/panel_cli_walkthroughs.md` (Scenario 4)
- **Should be stored in**: Domain concepts for BehaviorsView or Base Bot
- **Location**: `Invoke Bot > Navigate Behavior Actions > Perform Behavior Action In Bot Workflow`
- **Status**: ❌ NOT stored in JSON

### 9. StoryGraphTabView - Display Story Scope Hierarchy
- **Scope**: `Invoke Bot Through Panel.Filter And Navigate Scope.Display Story Scope Hierarchy`
- **Concepts Traced**: StoryGraphTabView, EpicView, SubEpicView, StoryView
- **File**: `docs/crc/walkthroughs/panel_cli_walkthroughs.md` (Scenario 5)
- **Should be stored in**: Domain concepts for StoryMapView or EpicView
- **Location**: `Invoke Bot > Work With Story Map > Edit Story Map`
- **Status**: ❌ NOT stored in JSON

### 10. StoryGraphTabView - Filter Story Scope
- **Scope**: `Invoke Bot Through Panel.Filter And Navigate Scope.Filter Story Scope`
- **Concepts Traced**: StoryGraphTabView, ScopeSection, Scope
- **File**: `docs/crc/walkthroughs/panel_cli_walkthroughs.md` (Scenario 6)
- **Should be stored in**: Domain concepts for ScopeView or Scope
- **Location**: `Invoke Bot > Work With Story Map > Scope Stories > Manage Story Scope`
- **Status**: ❌ NOT stored in JSON

### 11. ClarifyInstructionsSection - Display Clarify Instructions
- **Scope**: `Invoke Bot Through Panel.Display Instructions.Display Clarify Instructions`
- **Concepts Traced**: ClarifyInstructionsSection, InstructionsSection
- **File**: `docs/crc/walkthroughs/panel_cli_walkthroughs.md` (Scenario 7)
- **Should be stored in**: Domain concepts for ClarifyInstructionsSection
- **Location**: `Invoke Bot > Perform Action > Clarify Requirements`
- **Status**: ❌ NOT stored in JSON

---

## Where the Missing Realizations Should Be Located

Based on the scopes and concepts traced, here's where each walkthrough should be stored as a realization:

### Panel/UI Concepts (Render Bot Interface sub-epic)
- **PanelView (Base)**: Scenarios 5, 6 (Open Panel, Refresh Panel)
- **SectionView**: Scenario 7 (Display Hierarchy)
- **BehaviorsView**: Scenarios 7, 8 (Display Hierarchy, Execute Behavior Action)

### Story Graph Concepts (Edit Story Map sub-epic)
- **StoryMapView**: Scenario 9 (Display Story Scope Hierarchy)
- **EpicView**: Scenario 9 (Display Story Scope Hierarchy)

### Scope Concepts (Manage Story Scope sub-epic)
- **ScopeView**: Scenario 10 (Filter Story Scope)
- **Scope**: Scenario 10 (Filter Story Scope)

### Action Concepts (Clarify Requirements sub-epic)
- **ClarifyInstructionsSection**: Scenario 11 (Display Clarify Instructions)

---

## Recommendation

The 7 Panel/CLI walkthroughs should be added as `realization` arrays to their respective domain concepts in `story-graph.json` to maintain consistency with the Story Graph realizations and enable traceability from domain concepts to stories.
