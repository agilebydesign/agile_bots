# Domain Model Description: Agile Bots

**File Name**: `agile-bots-domain-model-description.md`
**Location**: `agile_bots/docs/story/agile-bots-domain-model-description.md`

## Solution Purpose
Domain model for Agile Bots

---

## Domain Model Descriptions

### Module: exit_result


#### ExitResult

**Key Responsibilities:**
- **Get exit code**: This responsibility involves collaboration with Integer.
- **Get exit message**: This responsibility involves collaboration with String.
- **Get should cleanup**: This responsibility involves collaboration with Boolean.

#### JSONExitResult

**Key Responsibilities:**
- **Serialize exit result to JSON**: This responsibility involves collaboration with ExitResult, JSON String.
- **Include exit code**: This responsibility involves collaboration with Integer, JSON.
- **Include exit message**: This responsibility involves collaboration with String, JSON.
- **Wraps domain exit result**: This responsibility involves collaboration with ExitResult.

#### MarkdownExitResult

**Key Responsibilities:**
- **Serialize exit result to Markdown**: This responsibility involves collaboration with ExitResult, Markdown String.
- **Format exit documentation**: This responsibility involves collaboration with ExitResult, Markdown String.
- **Wraps domain exit result**: This responsibility involves collaboration with ExitResult.

#### TTYExitResult

**Key Responsibilities:**
- **Serialize exit result to TTY**: This responsibility involves collaboration with ExitResult, TTY String.
- **Format exit message**: This responsibility involves collaboration with Message, TTY String.
- **Wraps domain exit result**: This responsibility involves collaboration with ExitResult.

### Module: help


#### JSONHelp

**Key Responsibilities:**
- **Serialize help to JSON**: This responsibility involves collaboration with Help, Dict.
- **Include help sections**: This responsibility involves collaboration with Sections, Array.
- **Wraps domain help**: This responsibility involves collaboration with Help.

#### JSONStatus

**Key Responsibilities:**
- **Serialize status to JSON**: This responsibility involves collaboration with Status, JSON String.
- **Include progress path**: This responsibility involves collaboration with Progress Path, String.
- **Include stage name**: This responsibility involves collaboration with Stage Name, String.
- **Include current behavior**: This responsibility involves collaboration with Behavior Name, String.
- **Include current action**: This responsibility involves collaboration with Action Name, String.
- **Wraps domain status**: This responsibility involves collaboration with Status.

#### MarkdownHelp

**Key Responsibilities:**
- **Serialize help to Markdown**: This responsibility involves collaboration with Help, String.
- **Format help sections**: This responsibility involves collaboration with Sections, Markdown.
- **Wraps domain help**: This responsibility involves collaboration with Help.

#### MarkdownStatus

**Key Responsibilities:**
- **Serialize status to Markdown**: This responsibility involves collaboration with Status, Markdown String.
- **Format progress section**: This responsibility involves collaboration with Progress Path, Stage Name, Markdown String.
- **Format workflow state**: This responsibility involves collaboration with Status, Markdown String.
- **Wraps domain status**: This responsibility involves collaboration with Status.

#### Status

**Key Responsibilities:**
- **Get progress path**: This responsibility involves collaboration with String.
- **Get stage name**: This responsibility involves collaboration with String.
- **Get current behavior name**: This responsibility involves collaboration with String.
- **Get current action name**: This responsibility involves collaboration with String.
- **Get has current behavior**: This responsibility involves collaboration with Boolean.
- **Get has current action**: This responsibility involves collaboration with Boolean.

#### TTYHelp

**Key Responsibilities:**
- **Serialize help to TTY**: This responsibility involves collaboration with Help, String.
- **Format help sections**: This responsibility involves collaboration with Sections, String.
- **Wraps domain help**: This responsibility involves collaboration with Help.

#### TTYStatus

**Key Responsibilities:**
- **Serialize status to TTY**: This responsibility involves collaboration with Status, TTY String.
- **Format progress line**: This responsibility involves collaboration with Progress Path, Stage Name, TTY String.
- **Format hierarchical status**: This responsibility involves collaboration with Bot, Status, TTY String.
- **Wraps domain status**: This responsibility involves collaboration with Status.

### Module: story_graph.acceptance_criteria


#### AcceptanceCriteria

**Key Responsibilities:**
- **Get steps**: This responsibility involves collaboration with List[Step].

#### AcceptanceCriteriaView

**Key Responsibilities:**
- **Wraps acceptance criteria JSON**: This responsibility involves collaboration with AcceptanceCriteria JSON.
- **Displays criteria name**: This responsibility involves collaboration with String, AcceptanceCriteria JSON.
- **Displays criteria icon**: This responsibility involves collaboration with Image.
- **Displays steps as checklist**: This responsibility involves collaboration with List[Step], HTML.

#### JSONAcceptanceCriteria

**Key Responsibilities:**
- **Include steps**: This responsibility involves collaboration with List[Step], JSON Array.
- **Wraps domain acceptance criteria**: This responsibility involves collaboration with AcceptanceCriteria.

#### MarkdownAcceptanceCriteria

**Key Responsibilities:**
- **Format criteria as checklist**: This responsibility involves collaboration with List[Step], Markdown.
- **Format steps list**: This responsibility involves collaboration with List[Step], Markdown.
- **Wraps domain acceptance criteria**: This responsibility involves collaboration with AcceptanceCriteria.

#### TTYAcceptanceCriteria

**Key Responsibilities:**
- **Format steps**: This responsibility involves collaboration with List[Step], TTY String.
- **Format criteria list**: This responsibility involves collaboration with List[Step], TTY String.
- **Wraps domain acceptance criteria**: This responsibility involves collaboration with AcceptanceCriteria.

### Module: story_graph.epic


#### Epic

**Key Responsibilities:**
- **Test file property**: This responsibility involves collaboration with String.
- **Get all stories**: This responsibility involves collaboration with List[Story].
- **Get domain concepts**: This responsibility involves collaboration with List[DomainConcept].

#### EpicView

**Key Responsibilities:**
- **Wraps epic JSON**: This responsibility involves collaboration with Epic JSON.
- **Displays epic name**: This responsibility involves collaboration with String, Epic JSON.
- **Displays epic icon**: This responsibility involves collaboration with Image.
- **Displays sub epics**: This responsibility involves collaboration with SubEpicView, SubEpic JSON.
- **Opens epic folder**: This responsibility involves collaboration with CLI, Epic JSON.
- **Opens epic test file**: This responsibility involves collaboration with CLI, Epic JSON.

#### JSONEpic

**Key Responsibilities:**
- **Include domain concepts**: This responsibility involves collaboration with List[DomainConcept], JSON Array.
- **Wraps domain epic**: This responsibility involves collaboration with Epic.

#### MarkdownEpic

**Key Responsibilities:**
- **Format domain concepts table**: This responsibility involves collaboration with List[DomainConcept], Markdown.
- **Wraps domain epic**: This responsibility involves collaboration with Epic.

#### TTYEpic

**Key Responsibilities:**
- **Format domain concepts**: This responsibility involves collaboration with List[DomainConcept], TTY String.
- **Wraps domain epic**: This responsibility involves collaboration with Epic.

### Module: story_graph.nodes


#### InlineNameEditor

**Key Responsibilities:**
- **Enables inline editing mode**: This responsibility involves collaboration with DOM Element, Input Field.
- **Validates name in real-time**: This responsibility involves collaboration with StoryNode, Siblings Collection.
- **Saves name on blur or Enter**: This responsibility involves collaboration with StoryNode, Event.
- **Cancels on Escape**: This responsibility involves collaboration with Event, Original Value.
- **Shows validation messages**: This responsibility involves collaboration with ValidationMessageDisplay, Message.

#### JSONStoryNode

**Key Responsibilities:**
- **Serialize node to JSON**: This responsibility involves collaboration with StoryNode, JSON String.
- **Include name**: This responsibility involves collaboration with String, JSON.
- **Include sequential order**: This responsibility involves collaboration with Float, JSON.
- **Include children**: This responsibility involves collaboration with List[StoryNode], JSON Array.
- **Add child**: This responsibility involves collaboration with StoryNode, JSON Result.
- **Add child at position**: This responsibility involves collaboration with StoryNode, Position, JSON Result.
- **Delete child**: This responsibility involves collaboration with StoryNode, JSON Result.
- **Delete this node**: This responsibility involves collaboration with JSON Result.
- **Delete with children**: This responsibility involves collaboration with JSON Result.
- **Update name**: This responsibility involves collaboration with String, JSON Result.
- **Move to parent**: This responsibility involves collaboration with New Parent, Position, JSON Result.
- **Move after target**: This responsibility involves collaboration with Target StoryNode, JSON Result.
- **Move before target**: This responsibility involves collaboration with Target StoryNode, JSON Result.
- **Reorder children**: This responsibility involves collaboration with Start Pos, End Pos, JSON Result.
- **Automatically refresh story graph**: This responsibility involves collaboration with JSON Result.
- **Wraps domain story node**: This responsibility involves collaboration with StoryNode.

#### MarkdownStoryNode

**Key Responsibilities:**
- **Serialize node to Markdown**: This responsibility involves collaboration with StoryNode, Markdown String.
- **Format node header**: This responsibility involves collaboration with String, Sequential Order, Markdown.
- **Format children list**: This responsibility involves collaboration with List[StoryNode], Markdown.
- **Wraps domain story node**: This responsibility involves collaboration with StoryNode.

#### StoryNode (Base)

**Key Responsibilities:**
- **Serializes**: This responsibility involves collaboration with StoryNodeSerializer.
- **Get/Update name**: This responsibility involves collaboration with String.
- **Get node type**: This responsibility involves collaboration with String.
- **Get node ID**: This responsibility involves collaboration with String, StoryNode, StoryNodeNavigator.
- **Get parent**: This responsibility involves collaboration with StoryNode.
- **Get sequential order**: This responsibility involves collaboration with StoryNodeNavigator, Float.
- **Contains Children**: This responsibility involves collaboration with StoryNodeChildren.
- **Delete self**: This responsibility involves collaboration with StoryNodeSerializer.
- **Delete with children**: This responsibility involves collaboration with StoryNodeSerializer, StoryNodeChildren.
- **Get/Update test**: This responsibility involves collaboration with Test.

#### StoryNodeChildren

**Key Responsibilities:**
- **Get children**: This responsibility involves collaboration with List[StoryNode].
- **Find child by name**: This responsibility involves collaboration with String, StoryNode.
- **Delete child**: This responsibility involves collaboration with StoryNode.

#### StoryNodeNavigator

**Key Responsibilities:**
- **Build node ID from hierarchy path**: This responsibility involves collaboration with String, StoryNode.
- **Get parent**: This responsibility involves collaboration with StoryNode.
- **Move to parent**: This responsibility involves collaboration with New Parent, Position.
- **Move after**: This responsibility involves collaboration with StoryNode, sequential order.
- **Move before**: This responsibility involves collaboration with StoryNode, sequential order.
- **DetermineOrder**: This responsibility involves collaboration with FLoat, StoryNode.

#### StoryNodeSerializer

**Key Responsibilities:**
- **File**: This responsibility involves collaboration with File.
- **Create Node**: This responsibility involves collaboration with File, StoryNode.
- **Load Node**: This responsibility involves collaboration with File, StoryNode.
- **Update Node**: This responsibility involves collaboration with File, StoryNode.
- **Delete Node**: This responsibility involves collaboration with File, StoryNode.
- **From JSON**: This responsibility involves collaboration with JSON, StoryNode.
- **To JSON**: This responsibility involves collaboration with JSON, StoryNode.

#### StoryNodeView

**Key Responsibilities:**
- **Wraps story node JSON**: This responsibility involves collaboration with StoryNode JSON.
- **Toggles collapsed**: This responsibility involves collaboration with State.
- **Add child node**: This responsibility involves collaboration with StoryNode, Panel Result.
- **Add child at position**: This responsibility involves collaboration with StoryNode, Position, Panel Result.
- **Delete this node**: This responsibility involves collaboration with Panel Result.
- **Delete with children**: This responsibility involves collaboration with Panel Result.
- **Update node name**: This responsibility involves collaboration with String, Panel Result.
- **Move to parent**: This responsibility involves collaboration with New Parent, Position, Panel Result.
- **Move after target**: This responsibility involves collaboration with Target StoryNode, Panel Result.
- **Move before target**: This responsibility involves collaboration with Target StoryNode, Panel Result.
- **Drag and drop**: This responsibility involves collaboration with Drop Target, Position, Panel Result.
- **Reorder children**: This responsibility involves collaboration with Start Pos, End Pos, Panel Result.
- **Automatically refresh story graph**: This responsibility involves collaboration with Panel Result.

#### TTYStoryNode

**Key Responsibilities:**
- **Serialize node to TTY**: This responsibility involves collaboration with StoryNode, TTY String.
- **Format name**: This responsibility involves collaboration with String, TTY String.
- **Format sequential order**: This responsibility involves collaboration with Float, TTY String.
- **Format children**: This responsibility involves collaboration with List[StoryNode], TTY String.
- **Add child**: This responsibility involves collaboration with StoryNode, CLI Result.
- **Add child at position**: This responsibility involves collaboration with StoryNode, Position, CLI Result.
- **Delete child**: This responsibility involves collaboration with StoryNode, CLI Result.
- **Delete this node**: This responsibility involves collaboration with CLI Result.
- **Delete with children**: This responsibility involves collaboration with CLI Result.
- **Update name**: This responsibility involves collaboration with String, CLI Result.
- **Move to parent**: This responsibility involves collaboration with New Parent, Position, CLI Result.
- **Move after target**: This responsibility involves collaboration with Target StoryNode, CLI Result.
- **Move before target**: This responsibility involves collaboration with Target StoryNode, CLI Result.
- **Reorder children**: This responsibility involves collaboration with Start Pos, End Pos, CLI Result.
- **Automatically refresh story graph**: This responsibility involves collaboration with CLI Result.
- **Wraps domain story node**: This responsibility involves collaboration with StoryNode.

### Module: story_graph.scenario


#### JSONScenario

**Key Responsibilities:**
- **Include steps**: This responsibility involves collaboration with List[Step], JSON Array.
- **Include test method**: This responsibility involves collaboration with Test Method, JSON.
- **Wraps domain scenario**: This responsibility involves collaboration with Scenario.

#### MarkdownScenario

**Key Responsibilities:**
- **Format Gherkin scenario**: This responsibility involves collaboration with Scenario, Markdown.
- **Format steps as Given/When/Then**: This responsibility involves collaboration with List[Step], Markdown.
- **Wraps domain scenario**: This responsibility involves collaboration with Scenario.

#### Scenario

**Key Responsibilities:**
- **Test method property**: This responsibility involves collaboration with String.
- **Get test method**: This responsibility involves collaboration with String.
- **Get default test method**: This responsibility involves collaboration with String.
- **Get steps**: This responsibility involves collaboration with List[Step].

#### ScenarioView

**Key Responsibilities:**
- **Wraps scenario JSON**: This responsibility involves collaboration with Scenario JSON.
- **Displays scenario name**: This responsibility involves collaboration with String, Scenario JSON.
- **Displays scenario icon**: This responsibility involves collaboration with Image.
- **Opens test at scenario**: This responsibility involves collaboration with CLI, Scenario JSON.

#### TTYScenario

**Key Responsibilities:**
- **Format steps**: This responsibility involves collaboration with List[Step], TTY String.
- **Format test method**: This responsibility involves collaboration with Test Method, TTY String.
- **Wraps domain scenario**: This responsibility involves collaboration with Scenario.

### Module: story_graph.scenario_outline


#### JSONScenarioOutline

**Key Responsibilities:**
- **Include steps**: This responsibility involves collaboration with List[Step], JSON Array.
- **Include examples**: This responsibility involves collaboration with List[Dict], JSON Array.
- **Include test method**: This responsibility involves collaboration with Test Method, JSON.
- **Wraps domain scenario outline**: This responsibility involves collaboration with ScenarioOutline.

#### MarkdownScenarioOutline

**Key Responsibilities:**
- **Format Gherkin scenario outline**: This responsibility involves collaboration with ScenarioOutline, Markdown.
- **Format steps as Given/When/Then**: This responsibility involves collaboration with List[Step], Markdown.
- **Format examples table**: This responsibility involves collaboration with List[Dict], Markdown.
- **Wraps domain scenario outline**: This responsibility involves collaboration with ScenarioOutline.

#### ScenarioOutline

**Key Responsibilities:**
- **Test method property**: This responsibility involves collaboration with String.
- **Get test method**: This responsibility involves collaboration with String.
- **Get default test method**: This responsibility involves collaboration with String.
- **Get examples**: This responsibility involves collaboration with List[Dict].
- **Get steps**: This responsibility involves collaboration with List[Step].

#### ScenarioOutlineView

**Key Responsibilities:**
- **Wraps scenario outline JSON**: This responsibility involves collaboration with ScenarioOutline JSON.
- **Displays scenario outline name**: This responsibility involves collaboration with String, ScenarioOutline JSON.
- **Displays scenario outline icon**: This responsibility involves collaboration with Image.
- **Displays examples table**: This responsibility involves collaboration with List[Dict], Table HTML.
- **Opens test at scenario outline**: This responsibility involves collaboration with CLI, ScenarioOutline JSON.

#### TTYScenarioOutline

**Key Responsibilities:**
- **Format steps**: This responsibility involves collaboration with List[Step], TTY String.
- **Format examples**: This responsibility involves collaboration with List[Dict], TTY String.
- **Format test method**: This responsibility involves collaboration with Test Method, TTY String.
- **Wraps domain scenario outline**: This responsibility involves collaboration with ScenarioOutline.

### Module: story_graph.step


#### JSONStep

**Key Responsibilities:**
- **Include step text**: This responsibility involves collaboration with String, JSON.
- **Wraps domain step**: This responsibility involves collaboration with Step.

#### MarkdownStep

**Key Responsibilities:**
- **Format step as Gherkin**: This responsibility involves collaboration with Step, Markdown.
- **Wraps domain step**: This responsibility involves collaboration with Step.

#### Step

**Key Responsibilities:**
- **Get text**: This responsibility involves collaboration with String.

#### StepView

**Key Responsibilities:**
- **Wraps step JSON**: This responsibility involves collaboration with Step JSON.
- **Displays step text**: This responsibility involves collaboration with String, Step JSON.
- **Displays step icon**: This responsibility involves collaboration with Image.

#### TTYStep

**Key Responsibilities:**
- **Format step text**: This responsibility involves collaboration with String, TTY String.
- **Format step keyword**: This responsibility involves collaboration with String, TTY String.
- **Wraps domain step**: This responsibility involves collaboration with Step.

### Module: story_graph.story


#### JSONStory

**Key Responsibilities:**
- **Include users**: This responsibility involves collaboration with List[StoryUser], JSON Array.
- **Include test metadata**: This responsibility involves collaboration with Test File, Test Class, JSON.
- **Wraps domain story**: This responsibility involves collaboration with Story.

#### MarkdownStory

**Key Responsibilities:**
- **Format story card**: This responsibility involves collaboration with Story, Markdown.
- **Format users section**: This responsibility involves collaboration with List[StoryUser], Markdown.
- **Wraps domain story**: This responsibility involves collaboration with Story.

#### Story

**Key Responsibilities:**
- **Test class property**: This responsibility involves collaboration with String.
- **Get test class**: This responsibility involves collaboration with String.
- **Get default test class**: This responsibility involves collaboration with String.
- **Get story type**: This responsibility involves collaboration with String.
- **Get users**: This responsibility involves collaboration with List[StoryUser].
- **Get scenarios**: This responsibility involves collaboration with List[Scenario].
- **Get scenario outlines**: This responsibility involves collaboration with List[ScenarioOutline].
- **Get acceptance criteria**: This responsibility involves collaboration with List[AcceptanceCriteria].

#### StoryView

**Key Responsibilities:**
- **Wraps story JSON**: This responsibility involves collaboration with Story JSON.
- **Displays story name**: This responsibility involves collaboration with String, Story JSON.
- **Displays story icon**: This responsibility involves collaboration with Image.
- **Displays scenarios**: This responsibility involves collaboration with ScenarioView, Scenario JSON.
- **Opens test at class**: This responsibility involves collaboration with CLI, Story JSON.

#### TTYStory

**Key Responsibilities:**
- **Format users**: This responsibility involves collaboration with List[StoryUser], TTY String.
- **Format test metadata**: This responsibility involves collaboration with Test File, Test Class, TTY String.
- **Wraps domain story**: This responsibility involves collaboration with Story.

### Module: story_graph.story_group


#### StoryGroup


### Module: story_graph.story_map


#### JSONStoryMap

**Key Responsibilities:**
- **Serialize story map to JSON**: This responsibility involves collaboration with StoryMap, JSON String.
- **Include story graph**: This responsibility involves collaboration with Dict, JSON.
- **Include all epics**: This responsibility involves collaboration with List[Epic], JSON Array.
- **Wraps domain story map**: This responsibility involves collaboration with StoryMap.

#### MarkdownStoryMap

**Key Responsibilities:**
- **Serialize story map to Markdown**: This responsibility involves collaboration with StoryMap, Markdown String.
- **Format epic hierarchy**: This responsibility involves collaboration with List[Epic], Markdown.
- **Format story index**: This responsibility involves collaboration with List[Story], Markdown.
- **Wraps domain story map**: This responsibility involves collaboration with StoryMap.

#### StoryMap

**Key Responsibilities:**
- **Load from bot directory**: This responsibility involves collaboration with Bot, StoryMap.
- **Load from story graph**: This responsibility involves collaboration with File Path, StoryMap.
- **Walk nodes**: This responsibility involves collaboration with StoryNode, Iterator[StoryNode].
- **Get all stories**: This responsibility involves collaboration with List[Story].
- **Get all scenarios**: This responsibility involves collaboration with List[Scenario].
- **Get all domain concepts**: This responsibility involves collaboration with List[DomainConcept].
- **Find by name**: This responsibility involves collaboration with Name, StoryNode.
- **Find node by path**: This responsibility involves collaboration with Path String, StoryNode.
- **Get story graph dict**: This responsibility involves collaboration with Dict.
- **Get epics**: This responsibility involves collaboration with List[Epic].
- **Save to story graph**: This responsibility involves collaboration with File Path.
- **Reload from story graph**: This responsibility involves collaboration with File Path, StoryMap.
- **Validate graph structure**: This responsibility involves collaboration with Validation Result.

#### StoryMapView

**Key Responsibilities:**
- **Wraps story map JSON**: This responsibility involves collaboration with StoryMap JSON.
- **Renders story graph as tree hierarchy**: This responsibility involves collaboration with StoryNode, HTML.
- **Displays epic hierarchy**: This responsibility involves collaboration with EpicView, Epic JSON.
- **Shows context-appropriate action buttons**: This responsibility involves collaboration with StoryNode, ButtonSet.
- **Refreshes tree display**: This responsibility involves collaboration with StoryGraph, DOM.
- **Searches stories**: This responsibility involves collaboration with Filter, StoryGraph JSON.
- **Opens story graph file**: This responsibility involves collaboration with CLI, File JSON.
- **Opens story map file**: This responsibility involves collaboration with CLI, File JSON.
- **Delegates to InlineNameEditor**: This responsibility involves collaboration with InlineNameEditor, StoryNode.
- **Delegates to StoryNodeDragDropManager**: This responsibility involves collaboration with StoryNodeDragDropManager, StoryNode.

#### StoryNodeDragDropManager

**Key Responsibilities:**
- **Shows drag cursor with icon**: This responsibility involves collaboration with Cursor Style, Node Icon.
- **Validates drop target compatibility at UI level**: This responsibility involves collaboration with Source Node Type, Target Parent Type.
- **Shows no-drop cursor for incompatible targets**: This responsibility involves collaboration with Cursor Style.
- **Highlights valid drop target**: This responsibility involves collaboration with Target Element, CSS Class.
- **Delegates move to StoryNode domain operation**: This responsibility involves collaboration with StoryNode, Target Parent, Position.
- **Returns node to original on invalid drop**: This responsibility involves collaboration with Original Position, Animation.

#### TTYStoryMap

**Key Responsibilities:**
- **Serialize story map to TTY**: This responsibility involves collaboration with StoryMap, TTY String.
- **Format epics list**: This responsibility involves collaboration with List[Epic], TTY String.
- **Format story hierarchy**: This responsibility involves collaboration with StoryMap, TTY String.
- **Walk and format nodes**: This responsibility involves collaboration with StoryNode, TTY String.
- **Wraps domain story map**: This responsibility involves collaboration with StoryMap.

### Module: story_graph.story_user


#### JSONStoryUser

**Key Responsibilities:**
- **Serialize user to JSON**: This responsibility involves collaboration with StoryUser, JSON String.
- **Include user name**: This responsibility involves collaboration with String, JSON.
- **Include user list**: This responsibility involves collaboration with List[StoryUser], JSON Array.
- **Wraps domain story user**: This responsibility involves collaboration with StoryUser.

#### MarkdownStoryUser

**Key Responsibilities:**
- **Serialize user to Markdown**: This responsibility involves collaboration with StoryUser, Markdown String.
- **Format user badge**: This responsibility involves collaboration with StoryUser, Markdown.
- **Format user list**: This responsibility involves collaboration with List[StoryUser], Markdown.
- **Wraps domain story user**: This responsibility involves collaboration with StoryUser.

#### StoryUser

**Key Responsibilities:**
- **Get name**: This responsibility involves collaboration with String.
- **From string**: This responsibility involves collaboration with String, StoryUser.
- **From list**: This responsibility involves collaboration with List[String], List[StoryUser].
- **To string**: This responsibility involves collaboration with String.

#### StoryUserView

**Key Responsibilities:**
- **Wraps story user JSON**: This responsibility involves collaboration with StoryUser JSON.
- **Displays user name**: This responsibility involves collaboration with String, StoryUser JSON.
- **Displays user icon**: This responsibility involves collaboration with Image.
- **Filters stories by user**: This responsibility involves collaboration with StoryUser, Panel Result.

#### TTYStoryUser

**Key Responsibilities:**
- **Serialize user to TTY**: This responsibility involves collaboration with StoryUser, TTY String.
- **Format user name**: This responsibility involves collaboration with String, TTY String.
- **Format user list**: This responsibility involves collaboration with List[StoryUser], TTY String.
- **Wraps domain story user**: This responsibility involves collaboration with StoryUser.

### Module: story_graph.sub_epic


#### SubEpic

**Key Responsibilities:**
- **Test file property**: This responsibility involves collaboration with String.

#### SubEpicView

**Key Responsibilities:**
- **Wraps sub epic JSON**: This responsibility involves collaboration with SubEpic JSON.
- **Displays sub epic name**: This responsibility involves collaboration with String, SubEpic JSON.
- **Displays sub epic icon**: This responsibility involves collaboration with Image.
- **Displays nested sub epics**: This responsibility involves collaboration with SubEpicView, SubEpic JSON.
- **Displays stories**: This responsibility involves collaboration with StoryView, Story JSON.
- **Opens sub epic folder**: This responsibility involves collaboration with CLI, SubEpic JSON.
- **Opens sub epic test file**: This responsibility involves collaboration with CLI, SubEpic JSON.

### Module: story_graph.test


#### JSONTest

**Key Responsibilities:**
- **Serialize test to JSON**: This responsibility involves collaboration with Test, JSON String.
- **Include test file**: This responsibility involves collaboration with String, JSON.
- **Include test class**: This responsibility involves collaboration with String, JSON.
- **Include test method**: This responsibility involves collaboration with String, JSON.
- **Wraps domain test**: This responsibility involves collaboration with Test.

#### MarkdownTest

**Key Responsibilities:**
- **Serialize test to Markdown**: This responsibility involves collaboration with Test, Markdown String.
- **Format test link**: This responsibility involves collaboration with Test File, Test Class, Test Method, Markdown.
- **Wraps domain test**: This responsibility involves collaboration with Test.

#### TTYTest

**Key Responsibilities:**
- **Serialize test to TTY**: This responsibility involves collaboration with Test, TTY String.
- **Format test file**: This responsibility involves collaboration with String, TTY String.
- **Format test class**: This responsibility involves collaboration with String, TTY String.
- **Format test method**: This responsibility involves collaboration with String, TTY String.
- **Wraps domain test**: This responsibility involves collaboration with Test.

#### Test

**Key Responsibilities:**
- **Get test file**: This responsibility involves collaboration with String.
- **Get test class**: This responsibility involves collaboration with String.
- **Get test method**: This responsibility involves collaboration with String.
- **Get default test class**: This responsibility involves collaboration with String.
- **Get default test method**: This responsibility involves collaboration with String.
- **Build from story node**: This responsibility involves collaboration with StoryNode, TestMetadata.

#### TestView

**Key Responsibilities:**
- **Wraps test JSON**: This responsibility involves collaboration with Test JSON.
- **Displays test file**: This responsibility involves collaboration with String, Test JSON.
- **Displays test class**: This responsibility involves collaboration with String, Test JSON.
- **Displays test method**: This responsibility involves collaboration with String, Test JSON.
- **Opens test file**: This responsibility involves collaboration with CLI, Test JSON.
- **Opens test at class**: This responsibility involves collaboration with CLI, Test JSON.
- **Opens test at method**: This responsibility involves collaboration with CLI, Test JSON.

---

## Source Material

**Primary Source:** `input.txt`
**Date Generated:** 2025-01-27
**Context:** Shape phase - Domain model extracted from story-graph.json
