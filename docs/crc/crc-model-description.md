# Domain Model Description: Base Bot

**File Name**: `base-bot-domain-model-description.md`
**Location**: `base_bot/docs/stories/base-bot-domain-model-description.md`

## Solution Purpose
Domain model for Base Bot

---

## Domain Model Descriptions

### Module: actions


#### Base Action

**Key Responsibilities:**
- **Inject Instructions**: This responsibility involves collaboration with Behavior.
- **Load Relevant Content + Inject Into Instructions**: This responsibility involves collaboration with Content.
- **Save content changes**: This responsibility involves collaboration with Content.

#### Behavior Action State

**Key Responsibilities:**
- **Track current action**: This responsibility involves collaboration with Action.
- **Track completed actions**: This responsibility involves collaboration with Action, Activity Log.
- **Determine next action**: This responsibility involves collaboration with Action, Behavior.
- **Pause workflow**: This responsibility involves collaboration with Human, AI Chat.
- **Resume workflow**: This responsibility involves collaboration with Human, AI Chat.

#### Content

**Key Responsibilities:**
- **Render outputs**: This responsibility involves collaboration with Template, Renderer, Render Spec.
- **Synchronize formats**: This responsibility involves collaboration with Synchronizer, Extractor, Synchronizer Spec.
- **Save knowledge graph**: This responsibility involves collaboration with Knowledge Graph.
- **Load rendered content**: This responsibility involves collaboration with na.
- **Present rendered content**: This responsibility involves collaboration with na.

#### Guardrails

**Key Responsibilities:**
- **Provide required context**: This responsibility involves collaboration with Key Questions, Evidence.
- **Guide planning decisions**: This responsibility involves collaboration with Decision Criteria, Assumptions.
- **Define recommended human activity**: This responsibility involves collaboration with Human, Instructions.

#### Workflow State

**Key Responsibilities:**
- **Track current action**: This responsibility involves collaboration with Action.
- **Track completed actions**: This responsibility involves collaboration with Action, Activity Log.
- **Determine next action**: This responsibility involves collaboration with Action, Behavior.
- **Pause workflow**: This responsibility involves collaboration with Human, AI Chat.
- **Resume workflow**: This responsibility involves collaboration with Human, AI Chat.

### Module: actions.build


#### BuildKnowledgeAction

**Key Responsibilities:**
- **Inject knowledge graph template**: This responsibility involves collaboration with Behavior, Content, Knowledge Graph Spec, Knowledge Graph.
- **Inject builder instructions**: This responsibility involves collaboration with Behavior, Content, Build Instructions.
- **Save Knowledge graph**: This responsibility involves collaboration with Behavior, Content, Knowledge Graph.

### Module: actions.clarify


#### GatherContextAction

**Key Responsibilities:**
- **Inject gather context instructions**: This responsibility involves collaboration with Behavior, Guardrails, Required Clarifications.
- **Inject questions and evidence**: This responsibility involves collaboration with Behavior, Guardrails, Key Questions, Evidence.

### Module: actions.render


#### RenderOutputAction

**Key Responsibilities:**
- **Inject render output instructions**: This responsibility involves collaboration with Behavior, Content, Render Spec, Renderer.
- **Inject templates**: This responsibility involves collaboration with Behavior, Content, Render Spec, Template.
- **Inject transformers**: This responsibility involves collaboration with Behavior, Content, Transformer.
- **Load + inject structured content**: This responsibility involves collaboration with Behavior, Content, Knowledge Graph.

#### Renderer

**Key Responsibilities:**
- **Render complex output**: This responsibility involves collaboration with Template, Knowledge Graph, Transformer.
- **Render outputs using components in context**: This responsibility involves collaboration with AI Chat, Template, Content.

#### Template

**Key Responsibilities:**
- **Define output structure**: This responsibility involves collaboration with Placeholder.
- **Transform content**: This responsibility involves collaboration with Transformer, Content.
- **Load template**: This responsibility involves collaboration with Behavior, Content.

### Module: actions.rules


#### Rule

**Key Responsibilities:**
- **Validate content**: This responsibility involves collaboration with Knowledge Graph, Violations.
- **Find behavior specific rules from context**: This responsibility involves collaboration with Behavior.
- **Find common bot rules from context**: This responsibility involves collaboration with Base Bot.
- **Load + inject diagnostics results**: This responsibility involves collaboration with AI Chat, Violations, Corrections.
- **Suggest corrections**: This responsibility involves collaboration with Violations, Suggestions, Fixes.
- **Provide examples - Do**: This responsibility involves collaboration with Example, Description.
- **Provide examples - Dont**: This responsibility involves collaboration with Example, Description.
- **Specialized examples**: This responsibility involves collaboration with Language, Framework, Pattern.

#### ValidateRulesAction

**Key Responsibilities:**
- **Inject common bot rules**: This responsibility involves collaboration with Base Bot, Rules, Common Rules.
- **Inject behavior specific rules**: This responsibility involves collaboration with Behavior, Rules, Behavior Rules.
- **Load + inject content for validation**: This responsibility involves collaboration with Behavior, Content, Knowledge Graph, Rendered Outputs.

### Module: actions.strategy


#### PlanningAction

**Key Responsibilities:**
- **Inject planning instructions**: This responsibility involves collaboration with Behavior, Guardrails, Planning.
- **Inject decision criteria and assumptions**: This responsibility involves collaboration with Behavior, Guardrails, Decision Criteria, Assumptions, Recommended Human Activity.

### Module: actions.validate


#### CorrectBotAction

**Key Responsibilities:**
- **Inject correct bot instructions**: This responsibility involves collaboration with Behavior, Correct Bot Instructions.
- **Load + inject diagnostics results**: This responsibility involves collaboration with Content, Diagnostic Report, Violations, Suggestions.

### Module: agile_bot.bots.base_bot.src.synchronizers


#### Synchronizer

**Key Responsibilities:**
- **Synchronizes formats**: This responsibility involves collaboration with Source Format, Target Format.
- **Extracts from source**: This responsibility involves collaboration with Extractor, Source File.
- **Renders to target**: This responsibility involves collaboration with Renderer, Target File.
- **Validates sync**: This responsibility involves collaboration with Source, Target, Rules.
- **Get source_format**: This responsibility involves collaboration with String.
- **Get target_format**: This responsibility involves collaboration with String.
- **Get extractor**: This responsibility involves collaboration with Extractor.
- **Get renderer**: This responsibility involves collaboration with Renderer.

### Module: agile_bot.bots.story_bot.src.story_bot_cli


#### StoryBotCLI

**Key Responsibilities:**
- **Bootstraps environment**: This responsibility involves collaboration with BOT_DIRECTORY, WORKING_AREA, Bot Config.
- **Delegates to BaseBotCli**: This responsibility involves collaboration with Base Bot CLI, Bot Name, Bot Config Path.
- **Executes CLI**: This responsibility involves collaboration with Base Bot CLI, Command Arguments.
- **Get bot_directory**: This responsibility involves collaboration with Path.
- **Get workspace_directory**: This responsibility involves collaboration with Path.
- **Get bot_name**: This responsibility involves collaboration with String.
- **Get bot_config_path**: This responsibility involves collaboration with Path.

### Module: agile_bot.bots.story_bot.src.story_bot_mcp_server


#### ActionStateManager

**Key Responsibilities:**
- **Closes current action**: This responsibility involves collaboration with Current Action, Behavior, State File.
- **Loads action state**: This responsibility involves collaboration with Behavior, Action State, State File.
- **Determines next action**: This responsibility involves collaboration with Behavior, Action Names, Current Index.
- **Transitions to next action**: This responsibility involves collaboration with Behavior, Current Action, Next Action.
- **Detects behavior completion**: This responsibility involves collaboration with Current Action, Final Action, Behavior.
- **Transitions to next behavior**: This responsibility involves collaboration with Bot, Next Behavior, First Action.
- **Returns transition result**: This responsibility involves collaboration with Status, Completed Action, Next Action.
- **Handles out-of-order confirmation**: This responsibility involves collaboration with Behavior, Confirmation, State File.
- **Validates human confirmation**: This responsibility involves collaboration with Confirmed By, Timestamp.
- **Persists confirmation**: This responsibility involves collaboration with State File, Confirmation Data, JSON.
- **Get state_file**: This responsibility involves collaboration with Path.
- **Get current_action**: This responsibility involves collaboration with Action.
- **Get next_action**: This responsibility involves collaboration with Action.
- **Get behavior_complete**: This responsibility involves collaboration with Boolean.
- **Get out_of_order_confirmations**: This responsibility involves collaboration with Dict.

#### BehaviorToolGenerator

**Key Responsibilities:**
- **Generates behavior tool function**: This responsibility involves collaboration with Behavior, Trigger Patterns.
- **Routes to behavior**: This responsibility involves collaboration with Bot, Behavior Name.
- **Routes to action**: This responsibility involves collaboration with Behavior, Action Name.
- **Executes action**: This responsibility involves collaboration with Action, Parameters.
- **Returns result**: This responsibility involves collaboration with Bot Result, Status, Data.
- **Handles missing action**: This responsibility involves collaboration with Current Action, State.
- **Loads action state**: This responsibility involves collaboration with Behavior, Action State.
- **Get tool_name**: This responsibility involves collaboration with String.
- **Get tool_description**: This responsibility involves collaboration with String.
- **Get trigger_patterns**: This responsibility involves collaboration with List.

#### StoryBotMCPServer

**Key Responsibilities:**
- **Bootstraps environment**: This responsibility involves collaboration with BOT_DIRECTORY, WORKING_AREA, Bot Config.
- **Creates Bot instance**: This responsibility involves collaboration with Bot, Bot Config, Bot Directory.
- **Creates FastMCP server**: This responsibility involves collaboration with FastMCP, Server Name.
- **Registers bot tool**: This responsibility involves collaboration with Bot, Current Behavior, Current Action.
- **Registers behavior tools**: This responsibility involves collaboration with Bot, Behavior, Action, Tool Generator.
- **Registers utility tools**: This responsibility involves collaboration with Working Directory Manager, Action State Manager, Server Restart Manager.
- **Delegates to Bot**: This responsibility involves collaboration with Bot, Behavior, Action.
- **Runs MCP server**: This responsibility involves collaboration with FastMCP, Event Loop.
- **Get bot_directory**: This responsibility involves collaboration with Path.
- **Get workspace_directory**: This responsibility involves collaboration with Path.
- **Get bot**: This responsibility involves collaboration with Bot.
- **Get server**: This responsibility involves collaboration with FastMCP.

#### WorkingDirectoryManager

**Key Responsibilities:**
- **Gets working directory**: This responsibility involves collaboration with Workspace Directory, WORKING_AREA.
- **Sets working directory**: This responsibility involves collaboration with New Path, Persist Flag.
- **Validates path**: This responsibility involves collaboration with Path, Validation Rules.
- **Updates environment**: This responsibility involves collaboration with WORKING_AREA, Environment Variables.
- **Updates bot config**: This responsibility involves collaboration with Bot Config, Working Area, Persist Flag.
- **Persists to config**: This responsibility involves collaboration with Bot Config File, JSON.
- **Returns previous directory**: This responsibility involves collaboration with Previous Path, Workspace Directory.
- **Get working_directory**: This responsibility involves collaboration with Path.
- **Get previous_directory**: This responsibility involves collaboration with Path.
- **Get persisted**: This responsibility involves collaboration with Boolean.

### Module: agile_bot.bots.story_bot.src.synchronizers.domain_model.domain_model_synchronizer


#### DomainModelSynchronizer : Synchronizer

**Key Responsibilities:**
- **Syncs CRC text with story graph**: This responsibility involves collaboration with CRC Text, Story Graph, Domain Concepts.
- **Extracts domain concepts**: This responsibility involves collaboration with CRC Parser, Concept Extractor.
- **Renders domain concepts**: This responsibility involves collaboration with Concept Renderer, CRC Template.
- **Validates CRC format**: This responsibility involves collaboration with CRC Validator, Format Rules.
- **Preserves module paths**: This responsibility involves collaboration with Module Mapper, Code Structure.
- **Get crc_path**: This responsibility involves collaboration with Path.
- **Get story_graph_path**: This responsibility involves collaboration with Path.
- **Get domain_concepts**: This responsibility involves collaboration with List.

### Module: agile_bot.bots.story_bot.src.synchronizers.story_io.story_io_epic


#### StoryIOEpic

**Key Responsibilities:**
- **Owns features**: This responsibility involves collaboration with Feature List, Epic Context.
- **Calculates total stories**: This responsibility involves collaboration with Feature, Story Count.
- **Renders epic section**: This responsibility involves collaboration with Epic Renderer, Template.
- **Validates epic structure**: This responsibility involves collaboration with Epic Validator, Rules.
- **Get name**: This responsibility involves collaboration with String.
- **Get description**: This responsibility involves collaboration with String.
- **Get features**: This responsibility involves collaboration with List.
- **Get total_stories**: This responsibility involves collaboration with Integer.
- **Get sequential_order**: This responsibility involves collaboration with Float.

### Module: agile_bot.bots.story_bot.src.synchronizers.story_io.story_io_feature


#### StoryIOFeature

**Key Responsibilities:**
- **Owns stories**: This responsibility involves collaboration with Story List, Feature Context.
- **Calculates story count**: This responsibility involves collaboration with Story, Count.
- **Renders feature section**: This responsibility involves collaboration with Feature Renderer, Template.
- **Validates feature structure**: This responsibility involves collaboration with Feature Validator, Rules.
- **Get name**: This responsibility involves collaboration with String.
- **Get description**: This responsibility involves collaboration with String.
- **Get stories**: This responsibility involves collaboration with List.
- **Get story_count**: This responsibility involves collaboration with Integer.

### Module: agile_bot.bots.story_bot.src.synchronizers.story_io.story_io_increment


#### StoryIOIncrement

**Key Responsibilities:**
- **Owns story assignments**: This responsibility involves collaboration with Story List, Increment Context.
- **Manages priorities**: This responsibility involves collaboration with Priority Order, Story Sequence.
- **Calculates capacity**: This responsibility involves collaboration with Story Count, Capacity Limit.
- **Renders increment view**: This responsibility involves collaboration with Increment Renderer, Template.
- **Validates increment structure**: This responsibility involves collaboration with Increment Validator, Rules.
- **Get number**: This responsibility involves collaboration with Integer.
- **Get name**: This responsibility involves collaboration with String.
- **Get stories**: This responsibility involves collaboration with List.
- **Get capacity**: This responsibility involves collaboration with Integer.
- **Get priority_order**: This responsibility involves collaboration with List.

### Module: agile_bot.bots.story_bot.src.synchronizers.story_io.story_io_renderer


#### StoryIORenderer

**Key Responsibilities:**
- **Renders epic cells**: This responsibility involves collaboration with Epic, Cell Generator, XML.
- **Renders feature cells**: This responsibility involves collaboration with Feature, Cell Generator, XML.
- **Renders story cells**: This responsibility involves collaboration with Story, Cell Generator, XML.
- **Renders increment lanes**: This responsibility involves collaboration with Increment, Lane Generator, XML.
- **Calculates layout**: This responsibility involves collaboration with Layout Manager, Position Calculator.
- **Formats XML**: This responsibility involves collaboration with XML Formatter, Pretty Print.
- **Get cell_style**: This responsibility involves collaboration with String.
- **Get layout_config**: This responsibility involves collaboration with Dict.
- **Get xml_formatter**: This responsibility involves collaboration with XMLFormatter.

### Module: agile_bot.bots.story_bot.src.synchronizers.story_io.story_io_story


#### StoryIOStory

**Key Responsibilities:**
- **Owns acceptance criteria**: This responsibility involves collaboration with Criteria List, Story Context.
- **Owns increment assignment**: This responsibility involves collaboration with Increment, Priority.
- **Renders story card**: This responsibility involves collaboration with Story Renderer, Template.
- **Validates story format**: This responsibility involves collaboration with Story Validator, Rules.
- **Calculates position**: This responsibility involves collaboration with Position Manager, Layout.
- **Get name**: This responsibility involves collaboration with String.
- **Get description**: This responsibility involves collaboration with String.
- **Get acceptance_criteria**: This responsibility involves collaboration with List.
- **Get increment**: This responsibility involves collaboration with Integer.
- **Get priority**: This responsibility involves collaboration with Integer.
- **Get position**: This responsibility involves collaboration with Position.

### Module: agile_bot.bots.story_bot.src.synchronizers.story_io.story_io_synchronizer


#### StoryIOSynchronizer : Synchronizer

**Key Responsibilities:**
- **Syncs story graph with drawio**: This responsibility involves collaboration with Story Graph, Drawio File.
- **Extracts stories from drawio**: This responsibility involves collaboration with Drawio Parser, Story Components.
- **Renders stories to drawio**: This responsibility involves collaboration with Story Renderer, Drawio Generator.
- **Manages story positions**: This responsibility involves collaboration with Position Manager, Story Layout.
- **Updates increments**: This responsibility involves collaboration with Increment Manager, Priority Data.
- **Validates story structure**: This responsibility involves collaboration with Structure Validator, Story Rules.
- **Get story_graph_path**: This responsibility involves collaboration with Path.
- **Get drawio_path**: This responsibility involves collaboration with Path.
- **Get increments**: This responsibility involves collaboration with List.
- **Get epics**: This responsibility involves collaboration with List.
- **Get stories**: This responsibility involves collaboration with List.

### Module: bot


#### Base Bot

**Key Responsibilities:**
- **Executes Actions**: This responsibility involves collaboration with Workflow, Behavior, Action.
- **Track activity**: This responsibility involves collaboration with Behavior, Action.
- **Route to behaviors and actions**: This responsibility involves collaboration with Router, Trigger Words.
- **Persist content**: This responsibility involves collaboration with Content.
- **Manage Project State**: This responsibility involves collaboration with Project.
- **Render**: Render

#### Behavior

**Key Responsibilities:**
- **Perform Configured Actions**: This responsibility involves collaboration with Actions.
- **Invoke On Trigger Words**: This responsibility involves collaboration with List.
- **Inject Instructions**: This responsibility involves collaboration with Text.
- **Provide Guardrails**: This responsibility involves collaboration with GuardRails.
- **Provide Rules**: This responsibility involves collaboration with Rule, Validation.
- **Provide Content Specs**: This responsibility involves collaboration with Content.
- **Gets action by name**: This responsibility involves collaboration with Action, String.
- **Gets actions in sequence**: This responsibility involves collaboration with List, Action.

#### Behavior Workflow

**Key Responsibilities:**
- **Determine next Action**: This responsibility involves collaboration with Behavior, Action, State.
- **Track state**: This responsibility involves collaboration with Behavior, Action, State.

#### Specific Bot

**Key Responsibilities:**
- **Provide Behavior config**: This responsibility involves collaboration with Bot Config, Behavior.
- **Provide MCP config**: This responsibility involves collaboration with MCP Config.
- **Provide Renderers**: Provide Renderers
- **Provide Extractors**: Provide Extractors
- **Provide Synchronizer**: Provide Synchronizer
- **Provide Trigger Words**: Provide Trigger Words

### Module: display_panel.extension


#### BehaviorActionSection

**Key Responsibilities:**
- **Wraps behaviors**: This responsibility involves collaboration with Behaviors.
- **Renders behavior action tree**: This responsibility involves collaboration with Behavior, Action, Operation.
- **Shows current action indicator**: This responsibility involves collaboration with Action.
- **Shows completed status indicator**: This responsibility involves collaboration with Action.
- **Shows pending indicator**: This responsibility involves collaboration with Action.
- **Handles navigation to previous action**: This responsibility involves collaboration with Behaviors, StatusDataProvider.
- **Handles navigation to next action**: This responsibility involves collaboration with Behaviors, StatusDataProvider.
- **Handles rerun current action**: This responsibility involves collaboration with StatusDataProvider.
- **Handles behavior click to execute**: This responsibility involves collaboration with Behavior, StatusDataProvider.
- **Handles action click to execute**: This responsibility involves collaboration with Action, StatusDataProvider.
- **Expands and collapses behaviors**: Expands and collapses behaviors
- **Expands and collapses actions**: Expands and collapses actions
- **Updates action status indicators**: This responsibility involves collaboration with Action.

#### BotInformationSection

**Key Responsibilities:**
- **Wraps bot metadata**: This responsibility involves collaboration with Bot, Workspace.
- **Displays bot name**: This responsibility involves collaboration with Bot.
- **Displays workspace path**: This responsibility involves collaboration with Workspace.
- **Displays bot directory path**: This responsibility involves collaboration with Bot.
- **Displays company icon**: Displays company icon
- **Displays panel version**: Displays panel version
- **Renders bot selection**: This responsibility involves collaboration with BotRegistry.
- **Handles workspace path edits**: This responsibility involves collaboration with Workspace, StatusDataProvider.
- **Handles bot switching**: This responsibility involves collaboration with BotRegistry, StatusDataProvider.
- **Expands and collapses section**: Expands and collapses section
- **Truncates long paths with ellipsis**: Truncates long paths with ellipsis
- **Shows full path in tooltip**: Shows full path in tooltip

#### BotPanel

**Key Responsibilities:**
- **Wraps active bot**: This responsibility involves collaboration with Bot.
- **Contains available bots**: This responsibility involves collaboration with BotRegistry.
- **Contains sections**: This responsibility involves collaboration with BotInformationSection, BehaviorActionSection, ScopeSection, InstructionsSection.
- **Renders panel HTML**: This responsibility involves collaboration with HtmlRenderer.
- **Handles user messages**: This responsibility involves collaboration with VSCode, WebView.
- **Manages panel lifecycle**: This responsibility involves collaboration with VSCode.
- **Refreshes display**: This responsibility involves collaboration with StatusDataProvider, HtmlRenderer.
- **Opens files in editor**: This responsibility involves collaboration with VSCode.

#### BotRegistry

**Key Responsibilities:**
- **Stores available bot configurations**: This responsibility involves collaboration with Bot.
- **Validates bot names**: Validates bot names
- **Provides bot CLI paths**: This responsibility involves collaboration with Bot.

#### CliOutputAdapter

**Key Responsibilities:**
- **Parses CLI JSON output**: Parses CLI JSON output
- **Adapts CLI data to panel format**: Adapts CLI data to panel format
- **Extracts behavior hierarchy**: This responsibility involves collaboration with Behaviors.
- **Extracts scope information**: This responsibility involves collaboration with StoryGraph, FileList.
- **Extracts instructions data**: This responsibility involves collaboration with Instructions.

#### HtmlRenderer

**Key Responsibilities:**
- **Renders complete panel HTML**: This responsibility involves collaboration with BotPanel.
- **Renders bot information section**: This responsibility involves collaboration with BotInformationSection.
- **Renders behavior action section**: This responsibility involves collaboration with BehaviorActionSection.
- **Renders scope section**: This responsibility involves collaboration with ScopeSection.
- **Renders instructions section**: This responsibility involves collaboration with InstructionsSection.
- **Generates JavaScript for webview interactions**: Generates JavaScript for webview interactions
- **Escapes HTML entities**: Escapes HTML entities

#### InstructionsSection

**Key Responsibilities:**
- **Wraps current instructions**: This responsibility involves collaboration with Instructions.
- **Renders base instructions**: This responsibility involves collaboration with Instructions, Behavior, Action.
- **Renders clarify instructions**: This responsibility involves collaboration with Instructions, KeyQuestions, Evidence.
- **Renders strategy instructions**: This responsibility involves collaboration with Instructions, DecisionCriteria, Assumptions.
- **Renders build instructions**: This responsibility involves collaboration with Instructions, KnowledgeGraphSpec, Rules.
- **Renders validate instructions**: This responsibility involves collaboration with Instructions, Rules.
- **Renders render instructions**: This responsibility involves collaboration with Instructions, RenderSpec, Templates.
- **Renders raw instructions format**: This responsibility involves collaboration with Instructions.
- **Handles instruction submission to AI chat**: This responsibility involves collaboration with VSCode, Instructions.
- **Handles user edits to questions**: This responsibility involves collaboration with KeyQuestions.
- **Handles user edits to assumptions**: This responsibility involves collaboration with Assumptions.
- **Validates instructions selected**: This responsibility involves collaboration with Instructions.
- **Expands and collapses section**: Expands and collapses section

#### ScopeSection

**Key Responsibilities:**
- **Wraps story graph scope**: This responsibility involves collaboration with StoryGraph.
- **Wraps file scope**: This responsibility involves collaboration with FileList.
- **Renders story hierarchy**: This responsibility involves collaboration with StoryGraph.
- **Renders file list**: This responsibility involves collaboration with FileList.
- **Handles story search**: This responsibility involves collaboration with StoryGraph.
- **Handles file pattern search**: This responsibility involves collaboration with FileList.
- **Expands and collapses story nodes**: This responsibility involves collaboration with StoryGraph.
- **Opens story graph JSON**: This responsibility involves collaboration with VSCode, StoryGraph.
- **Opens story map diagram**: This responsibility involves collaboration with VSCode.
- **Opens epic folder**: This responsibility involves collaboration with VSCode, StoryGraph.
- **Opens sub-epic folder**: This responsibility involves collaboration with VSCode, StoryGraph.
- **Opens test file at class**: This responsibility involves collaboration with VSCode, StoryGraph.
- **Opens test file at scenario**: This responsibility involves collaboration with VSCode, StoryGraph.
- **Displays hierarchical matches**: This responsibility involves collaboration with StoryGraph.
- **Clears search**: Clears search

#### StatusDataProvider

**Key Responsibilities:**
- **Fetches CLI status via Python subprocess**: This responsibility involves collaboration with PythonREPL.
- **Switches current bot**: This responsibility involves collaboration with BotRegistry.
- **Updates workspace path**: This responsibility involves collaboration with Workspace.
- **Executes CLI commands**: This responsibility involves collaboration with PythonREPL.
- **Loads bot registry from JSON**: This responsibility involves collaboration with BotRegistry.
- **Provides available bot names**: This responsibility involves collaboration with BotRegistry.

### Module: ext


#### Router

**Key Responsibilities:**
- **Match trigger patterns**: This responsibility involves collaboration with Trigger Words, Route.
- **Route to MCP bot tool**: This responsibility involves collaboration with Base Bot, Trigger Words.
- **Route to behavior tool**: This responsibility involves collaboration with Behavior, Trigger Words.
- **Route to action tool**: This responsibility involves collaboration with Action, Trigger Words.
- **Forward to behavior**: This responsibility involves collaboration with Behavior, Base Bot.
- **Forward to action**: This responsibility involves collaboration with Action, Behavior.
- **Forward to current behavior and action**: This responsibility involves collaboration with Behavior, Action, Base Bot.

### Module: repl_cli


#### REPLSession

**Key Responsibilities:**
- **Runs REPL loop**: Runs REPL loop
- **Reads input from stdin or terminal**: Reads input from stdin or terminal
- **Parses command input**: This responsibility involves collaboration with CLIBot.
- **Routes commands to CLI bot**: This responsibility involves collaboration with CLIBot.
- **Displays status and results**: This responsibility involves collaboration with CLIBot.
- **Has CLI bot**: This responsibility involves collaboration with CLIBot.

### Module: repl_cli.cli_bot


#### CLIAction

**Key Responsibilities:**
- **Get name: str**: Get name: str
- **Get description: str**: Get description: str
- **Is current: bool**: Is current: bool
- **Is completed: bool**: Is completed: bool
- **Executes: ActionResult**: This responsibility involves collaboration with Action.
- **Wraps domain action**: This responsibility involves collaboration with Action.

#### CLIActions

**Key Responsibilities:**
- **Get all: List[CLIAction]**: This responsibility involves collaboration with CLIAction.
- **Get current: CLIAction**: This responsibility involves collaboration with CLIAction.
- **Find by name: CLIAction**: This responsibility involves collaboration with CLIAction.
- **Wraps domain actions**: This responsibility involves collaboration with Actions.

#### CLIBehavior

**Key Responsibilities:**
- **Get name: str**: Get name: str
- **Get description: str**: Get description: str
- **Get actions: CLIActions**: This responsibility involves collaboration with CLIActions.
- **Is current: bool**: Is current: bool
- **Wraps domain behavior**: This responsibility involves collaboration with Behavior.

#### CLIBehaviors

**Key Responsibilities:**
- **Get all: List[CLIBehavior]**: This responsibility involves collaboration with CLIBehavior.
- **Get current: CLIBehavior**: This responsibility involves collaboration with CLIBehavior.
- **Find by name: CLIBehavior**: This responsibility involves collaboration with CLIBehavior.
- **Wraps domain behaviors**: This responsibility involves collaboration with Behaviors.

#### CLIBot

**Key Responsibilities:**
- **Get name: str**: Get name: str
- **Get workspace directory: Path**: Get workspace directory: Path
- **Get behaviors: CLIBehaviors**: This responsibility involves collaboration with CLIBehaviors.
- **Get status text: str**: This responsibility involves collaboration with CLIBehaviors, CLIBehavior, CLIActions, CLIAction.
- **Wraps domain bot**: This responsibility involves collaboration with Bot.

### Module: workflow


#### BehaviorGraphBuilder

**Key Responsibilities:**
- **Read behavior workflow definitions**: This responsibility involves collaboration with Behavior, Behavior Config.
- **Create LangGraph StateGraph**: This responsibility involves collaboration with LangGraph, BotLangState.
- **Build node instances from actions**: This responsibility involves collaboration with BotLangActionNode, Action.
- **Connect nodes based on workflow order**: This responsibility involves collaboration with LangGraph, BotLangActionNode.

#### BotLangActionNode

**Key Responsibilities:**
- **Wrap action.execute(context) method**: This responsibility involves collaboration with Action, LangGraph.
- **Implement two-pass pattern**: This responsibility involves collaboration with Action, AI.
- **Support execution modes**: This responsibility involves collaboration with BotMode.
- **Provide LangGraph entry point**: This responsibility involves collaboration with LangGraph.

#### BotLangFlow

**Key Responsibilities:**
- **Execute nodes in sequence**: This responsibility involves collaboration with BotLangActionNode, BotLangFlowRunner.
- **Handle conditional branching**: This responsibility involves collaboration with Decision Node, BotLangState.
- **Support loops and iterations**: This responsibility involves collaboration with BotLangActionNode, BotLangState.
- **Pause at interactive points**: This responsibility involves collaboration with Human, BotMode.
- **Resume from checkpoint**: This responsibility involves collaboration with Checkpoint, BotLangFlowRunner.

#### BotLangFlowRunner

**Key Responsibilities:**
- **Load BotLangFlow Python files**: This responsibility involves collaboration with BotLangFlow, File System.
- **Compile graph with checkpointer**: This responsibility involves collaboration with LangGraph, SqliteSaver, Checkpoint.
- **Execute workflow graph**: This responsibility involves collaboration with LangGraph, BotLangActionNode, BotLangState.
- **Resume from checkpoint**: This responsibility involves collaboration with Checkpoint, BotLangState.

#### BotLangState

**Key Responsibilities:**
- **Contain story graph**: This responsibility involves collaboration with Story Graph.
- **Contain clarification data**: This responsibility involves collaboration with Key Questions, Evidence.
- **Contain strategy data**: This responsibility involves collaboration with Decision Criteria, Assumptions.
- **Contain context files**: This responsibility involves collaboration with Context.
- **Contain files dictionary**: This responsibility involves collaboration with Source Files, Test Files.
- **Contain workspace directory**: This responsibility involves collaboration with Workspace.
- **Contain workflow execution state**: This responsibility involves collaboration with Action, Instructions.

#### BotMode

**Key Responsibilities:**
- **Determine AI interaction**: This responsibility involves collaboration with BotLangActionNode, AI Client.
- **Control pause points**: This responsibility involves collaboration with BotLangActionNode, Human.

#### Checkpoint

**Key Responsibilities:**
- **Save workflow state**: This responsibility involves collaboration with BotLangState, BotLangFlowRunner.
- **Restore workflow state**: This responsibility involves collaboration with BotLangState, BotLangFlowRunner.
- **Track execution history**: This responsibility involves collaboration with BotLangState.
- **Enable resume capability**: This responsibility involves collaboration with BotLangFlow, BotLangFlowRunner.

---

## Source Material

**Primary Source:** `input.txt`
**Date Generated:** 2025-01-27
**Context:** Shape phase - Domain model extracted from story-graph.json
