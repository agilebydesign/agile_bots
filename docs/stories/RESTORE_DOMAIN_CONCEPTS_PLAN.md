# Plan to Restore Domain Concepts to Story Graph

## Summary

**Status**: All `domain_concepts` have been deleted from the current `story-graph.json`. The old file (`Story_graph_old.json`) contains 175 domain concepts that need to be restored to the appropriate domain-oriented sub_epics.

**Approach**: Concepts are mapped to the **lowest-level sub_epics** based on their domain functionality, not by channel (TTY/JSON/Markdown). Channel-specific variants are included with their base concepts.

## Mapping Strategy

Domain concepts are mapped to **lowest-level sub_epics** (those with no sub_epics themselves) based on their functional domain. Channel-specific variants (TTY, JSON, Markdown) are grouped with their base concepts.

## Final Concept Mapping

### 1. Invoke Bot.Initialize Bot.Load Bot, Behavior, and Actions
**9 concepts**: Bot, Behavior, and their channel variants
- Base Bot, Specific Bot
- Behavior
- TTYBot, JSONBot, MarkdownBot
- TTYBehavior, JSONBehavior, MarkdownBehavior

### 2. Invoke Bot.Initialize Bot.Initialize Bot Interface
**11 concepts**: CLI/REPL infrastructure
- CLISession
- ChannelAdapter (Abstract), TextAdapter
- TTYAdapter, TTYProgressAdapter
- JSONAdapter, JSONProgressAdapter
- MarkdownAdapter, MarkdownProgressAdapter
- DotNotationParser
- FileModificationMonitor

### 3. Invoke Bot.Initialize Bot.Render Bot Interface
**12 concepts**: UI rendering infrastructure
- BotView, BotHeaderView, AvailableBotsView
- BehaviorsView, ActionsView, PathsSection
- PanelView (Base), SectionView, SubSectionView
- PanelHeader, ConfirmationDialog, ValidationMessageDisplay

### 4. Invoke Bot.Navigate Behavior Actions.Navigate Behavior And Actions
**9 concepts**: Navigation
- NavigationResult, NavigationView, BotPath
- TTYNavigation, JSONNavigation, MarkdownNavigation
- TTYBotPath, JSONBotPath, MarkdownBotPath

### 5. Invoke Bot.Navigate Behavior Actions.Perform Behavior Action In Bot Workflow
**6 concepts**: Action execution
- Base Action, ActionStateManager
- TTYAction, JSONAction, MarkdownAction

### 6. Invoke Bot.Perform Action.Clarify Requirements
**6 concepts**: Clarify action
- GatherContextAction
- ClarifyInstructionsSection, ClarifyDataSubSection
- TTYGatherContext, JSONGatherContext, MarkdownGatherContext

### 7. Invoke Bot.Perform Action.Decide Strategy
**6 concepts**: Strategy action
- StrategyAction
- StrategyInstructionsSection, StrategyDataSubSection
- TTYStrategy, JSONStrategy, MarkdownStrategy

### 8. Invoke Bot.Perform Action.Build Story Graph
**6 concepts**: Build action
- BuildKnowledgeAction
- BuildInstructionsSection, BuildDataSubSection
- TTYBuildKnowledge, JSONBuildKnowledge, MarkdownBuildKnowledge

### 9. Invoke Bot.Perform Action.Validate With Rules
**6 concepts**: Validate action
- ValidateRulesAction
- ValidateInstructionsSection, ValidateDataSubSection
- TTYValidateRules, JSONValidateRules, MarkdownValidateRules

### 10. Invoke Bot.Perform Action.Render Content
**9 concepts**: Render action
- RenderOutputAction, Renderer, Template, Content
- RenderInstructionsSection, RenderDataSubSection
- TTYRenderOutput, JSONRenderOutput, MarkdownRenderOutput

### 11. Invoke Bot.Perform Action.Use Rules In Prompt
**2 concepts**: Rules
- Rule, Guardrails

### 12. Invoke Bot.Perform Action.Prepare Common Instructions For Behavior, Action, and Scope
**7 concepts**: Common instructions
- InstructionsSection, BaseInstructionsSubSection, ActionDataSubSection, RawFormatSubSection
- TTYInstructions, JSONInstructions, MarkdownInstructions

### 13. Invoke Bot.Work With Story Map.Edit Story Map
**61 concepts**: Story graph nodes and infrastructure
- StoryNode (Base), StoryNodeChildren, StoryNodeNavigator, StoryNodeSerializer
- StoryMap, StoryMapView
- Epic, SubEpic, Story, StoryGroup
- Scenario, ScenarioOutline, AcceptanceCriteria
- Step, Test, StoryUser
- All channel variants (TTY/JSON/Markdown) of story graph concepts
- StoryNodeView, EpicView, SubEpicView, StoryView, etc.
- InlineNameEditor

### 14. Invoke Bot.Work With Story Map.Scope Stories.Manage Story Scope
**5 concepts**: Scope management
- Scope, ScopeView
- TTYScope, JSONScope, MarkdownScope

### 15. Invoke Bot.Get Help
**11 concepts**: Help and status
- Status, Help, ExitResult
- TTYStatus, JSONStatus, MarkdownStatus
- TTYHelp, JSONHelp, MarkdownHelp
- TTYExitResult, JSONExitResult, MarkdownExitResult

## Unmapped Concepts (9)

These are meta-concepts or formatting artifacts that don't need to be in specific sub_epics:
- DomainModule, DomainConcept, Responsibility, Collaborator (meta-concepts)
- TTYDomainConcept, JSONDomainConcept, MarkdownDomainConcept (meta-concept variants)
- "---------------------------" (separator)
- "### status" (formatting artifact)

## Implementation Steps

### Step 1: Load Mapping Data
✅ **COMPLETED** - Mapping created and saved to `docs/stories/final_concept_mapping.json`

### Step 2: Restore Concepts to story-graph.json
**ACTION REQUIRED**: Execute restoration script to add domain_concepts to each sub_epic

### Step 3: Validation
- Verify JSON syntax is valid
- Verify all 166 concepts are restored (9 unmapped intentionally)
- Verify concepts are in correct sub_epic locations
- Verify no duplicate concepts within sub_epics

## Files Created

1. `final_concept_mapping.json` - Final mapping of concepts to sub_epics (ready for restoration)
2. `extracted_domain_concepts.json` - Original extracted concepts from old file

## Next Steps

1. **Execute restoration script** to add concepts to story-graph.json
2. **Validate** the restored structure
3. **Test** that the concepts are correctly placed
