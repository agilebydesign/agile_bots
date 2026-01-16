

Router
    Match trigger patterns: Trigger Words,Route
    Route to MCP bot tool: Base Bot,Trigger Words
    Route to behavior tool: Behavior,Trigger Words
    Route to action tool: Action,Trigger Words
    Forward to behavior: Behavior,Base Bot
    Forward to action: Action,Behavior
    Forward to current behavior and action: Behavior,Action,Base Bot


## Module: cli

CLISession
    Runs CLI loop: 
    Reads input from stdin or terminal: 
    Determine channel adapter: ChannelAdapter
    Read and execute command: Command String,CLICommandResponse
    Parse command: Command String,Command Verb,Params
    Route to bot domain methods: Bot,Command Verb,Params,BotResult
    Serializes via channel adapter: ChannelAdapter,String
    Displays serialized output: Stdout
    

ChannelAdapter (Abstract)
    Serialize domain object to format: Domain Object,Format
    Deserialize format to domain object: Format,Domain Object

TextAdapter : ChannelAdapter (Abstract)
    Parse command text: Text String,Command,Params

TTYAdapter : TextAdapter (Abstract)
    Serialize to TTY text: Domain Object,String
    Deserialize TTY text: String,Domain Object
    Add color: Text,Color
    Format indentation: Indent Level,Spaces

TTYProgressAdapter : TTYAdapter (Abstract)
    Format line with marker: Marker,Text,Indent
    Render marker: Is Completed,Is Current

JSONAdapter : ChannelAdapter (Abstract)
    Serialize to JSON dict: Dict
    Deserialize JSON dict: Dict, Domain Object
    Convert to JSON string: Dict, String
    Parse JSON string: String, Dict
    Validate JSON structure: Dict, Schema

JSONProgressAdapter : JSONAdapter (Abstract)
    Include progress fields: Is Completed, Is Current
    Include completion markers: Progress String

MarkdownAdapter : TextAdapter (Abstract)
    Serialize to Markdown: String
    Deserialize Markdown: String, Domain Object
    Parse markdown sections: Markdown, Sections
    Format header: Level,Text
    Format list item: Marker, Text, Indent
    Format code block: Language, Content

MarkdownProgressAdapter : MarkdownAdapter (Abstract)
    Render progress marker: Is Completed, Is Current, Marker String
    Format progress line: Name, Is Completed, Is Current, String

## Module: bot_panel

PanelView (Base)
    Wraps JSON data: JSON
    Spawns subprocess: CLI,Python Process
    Sends command to CLI: Command,Stdin
    Receives JSON from CLI: Stdout
    Parses JSON: String,Dict
    Provides element ID: String
    Renders to HTML: HTML,JSON

SectionView : PanelView (Base)
    Renders section header: PanelHeader
    Toggles collapsed state: State
    May contain subsections: SubSectionView

SubSectionView: PanelView
    Toggles collapsed state: State

PanelHeader
    Displays header image: Image
    Displays title: String
    
##  Module: bot
Base Bot
    Executes Actions: Workflow,Behavior,Action
    Execute behavior: Behavior,BotResult
    Execute current action: BotResult
    Navigate and execute: Behavior,Action,ActionContext,BotResult
    Validate behavior exists: Behavior,Boolean
    Validate action exists: Behavior,Action,Boolean
    Track activity: Behavior,Action
    Route to behaviors and actions: Router,Trigger Words
    Persist content: Content
    Manage Project State: Project
    Render: 
    Get scope: Scope (read-only property)
    Get status: Status
    Navigate next: NavigationResult
    Navigate back: NavigationResult
    Get bot path: BotPath
    Get help: Help
    Exit: ExitResult 

Specific Bot
    Provide Behavior config: Bot Config,Behavior
    Provide MCP config: MCP Config
    Provide Renderers: 
    Provide Extractors: 
    Provide Synchronizer: 
    Provide Trigger Words: 

TTYBot : TTYAdapter
    Execute behavior by name: Behavior Name String,TTY String
    Execute current action: TTY String
    Navigate and execute: Dot Notation String,TTY String
    Validate behavior exists: Behavior Name String,TTY String (True/False)
    Validate action exists: Dot Notation String,TTY String (True/False)
    Serialize entire bot to TTY: Bot,TTY String
    Bot header: Bot Name,TTY String
    Behaviors: Bot, Behaviors,TTY Behaviors
    Get status: TTY String (delegates to TTYStatus)
    Get scope: TTY String (delegates to TTYScope)
    Navigate next: TTY String (delegates to TTYNavigation)
    Navigate back: TTY String (delegates to TTYNavigation)
    Get bot path: TTY String (delegates to TTYBotPath)
    Get help: TTY String (delegates to TTYHelp)
    Exit: TTY String (delegates to TTYExitResult)
    Wraps domain bot: Bot

JSONBot : JSONAdapter
    Execute behavior by name: Behavior Name String,JSON String
    Execute current action: JSON String
    Navigate and execute: Dot Notation String,JSON String
    Validate behavior exists: Behavior Name String,JSON String
    Validate action exists: Dot Notation String,JSON String
    Serialize bot to JSON: Bot,JSON String
    Include bot metadata: Name,Directory,Paths
    Behaviors: Bot, Behaviors,JSON Behaviors
    Get status: JSON String (delegates to JSONStatus)
    Get scope: JSON String (delegates to JSONScope)
    Navigate next: JSON String (delegates to JSONNavigation)
    Navigate back: JSON String (delegates to JSONNavigation)
    Get bot path: JSON String (delegates to JSONBotPath)
    Get help: JSON String (delegates to JSONHelp)
    Exit: JSON String (delegates to JSONExitResult)
    Wraps domain bot: Bot

MarkdownBot : MarkdownAdapter
    Execute behavior by name: Behavior Name String,Markdown String
    Execute current action: Markdown String
    Navigate and execute: Dot Notation String,Markdown String
    Validate behavior exists: Behavior Name String,Markdown String
    Validate action exists: Dot Notation String,Markdown String
    Serialize bot to Markdown: Bot,Markdown String
    Format bot documentation: Bot Name,Description,Markdown Header
    Behaviors: Bot, Behaviors,Markdown Behaviors
    Get status: Markdown String (delegates to MarkdownStatus)
    Get scope: Markdown String (delegates to MarkdownScope)
    Navigate next: Markdown String (delegates to MarkdownNavigation)
    Navigate back: Markdown String (delegates to MarkdownNavigation)
    Get bot path: Markdown String (delegates to MarkdownBotPath)
    Get help: Markdown String (delegates to MarkdownHelp)
    Exit: Markdown String (delegates to MarkdownExitResult)
    Wraps domain bot: Bot

BotView: PanelView
    Wraps bot JSON: Bot JSON
    Displays BotHeaderView: BotHeaderView
    Displays PathsSection: PathsSection
    Displays BehaviorsView: BehaviorsView
    Displays ScopeSection: ScopeSection
    Displays InstructionsSection: InstructionsSection

BotHeaderView: PanelView
    Wraps bot JSON: Bot JSON
    Displays image: Image
    Displays title: String,Bot JSON
    Displays version number: String,Bot JSON
    Refreshes panel: CLI

PathsSection : SectionView
    Wraps bot paths JSON: BotPaths JSON
    Displays bot directory: String, BotPaths JSON
    Edits workspace directory: CLI, BotPaths JSON
    Displays available bots: AvailableBotsView

AvailableBotsView : PanelView
    Wraps bot registry JSON: BotRegistry JSON
    Displays available bots: List,BotRegistry JSON
    Selects bot: CLI,Bot


## Module: behaviors

Behavior
    Name: String
    Description: String
    Goal: String
    Folder: Path
    Is completed: Boolean
    Actions workflow: List
    Action Names: List
    Validation type: ValidationType
    CurrentAction: Action
    Guardrails: Guardrails
    Content: Content
    Rules: Rules
    Actions: Actions

    
Rule
    Validate content: Knowledge Graph,Violations
    Find behavior specific rules from context: Behavior
    Find common bot rules from context: Base Bot
    Load + inject diagnostics results: AI Chat,Violations,Corrections
    Suggest corrections: Violations,Suggestions,Fixes
    Provide examples - Do: Example,Description
    Provide examples - Dont: Example,Description
    Specialized examples: Language,Framework,Pattern


Guardrails
    Provide required context: Key Questions,Evidence
    Guide Strategy decisions: Decision Criteria,Assumptions
    Define recommended human activity: Human,Instructions

---------------------------

TTYBehavior : TTYProgressAdapter
    Serialize behavior to TTY: Behavior,String
    Format behavior line: Behavior Name,Marker,Color
    Format actions: Actions,String
    Wraps domain behavior: Behavior

JSONBehavior : JSONProgressAdapter
    Serialize behavior to JSON dict: Behavior,Dict
    Include behavior metadata: Name,Description,Status
    Include actions: Actions,Array
    Wraps domain behavior: Behavior

MarkdownBehavior : MarkdownProgressAdapter
    Serialize behavior to Markdown: Behavior,String
    Format behavior documentation: Behavior Name,Description,Section
    Format actions: Actions,Markdown Subsections
    Wraps domain behavior: Behavior

BehaviorsView : SectionView
    Wraps behaviors JSON: Behaviors JSON
    Displays behavior names list: List,Behavior JSON
    Navigates to behavior: CLI,Behavior
    Toggles collapsed: State,Behavior JSON
    Displays tooltip: String,Behavior JSON
    Displays actions: ActionsView
    Executes behavior: CLI,Behavior
    Displays completion progress: Status,Behavior JSON
    Displays navigation: NavigationView

NavigationView : PanelView  
    Wraps current action JSON: Action JSON
    Reruns action: CLI,Action
    Navigates to next action: CLI,Action
    Navigates to prev action: CLI,Action




## Module: actions

Base Action
    Inject Instructions: Behavior
    Load Relevant Content + Inject Into Instructions: Content
    Save content changes: Content

Base Action
    Inject Instructions: Behavior
    Load Relevant Content + Inject Into Instructions: Content
    Save content changes: Content

ActionStateManager
    Get state file path: Path
    Load or create state: State File,Dict
    Save state: Action,State File
    Load state: Actions List,Current Index
    Find action index: Actions List,Action Name,Integer
    Filter completed actions: Completed Actions,Target Index,Actions List,List

TTYAction : TTYProgressAdapter
    Serialize action to TTY: Action,String
    Format action line: Action Name,Marker,Indent
    Wraps domain action: Action

JSONAction : JSONProgressAdapter
    Serialize action to JSON dict: Action,Dict
    Include action metadata: Name,Description,Status
    Wraps domain action: Action

MarkdownAction : MarkdownProgressAdapter
    Serialize action to Markdown: Action,String
    Format action documentation: Action Name,Description,Subsection
    Wraps domain action: Action

ActionsView : PanelView
    Wraps actions JSON: Actions JSON
    Displays action names list: List,Action JSON
    Navigates to action: CLI,Action
    Displays status indicators: Status,Action JSON
    Executes action: CLI, Action
    Displays completion progress: Progress,Action JSON

ActionDataSubSection : SubSectionView
    Wraps action JSON: Action JSON
    Displays action properties: Object,Action JSON

## Module: instructions

TTYInstructions : TTYAdapter
    Serialize instructions to TTY: Instructions,String
    Format instruction sections: Sections,String
    Wraps domain instructions: Instructions

JSONInstructions : JSONAdapter
    Serialize instructions to JSON: Instructions,Dict
    Include instruction sections: Sections,Array
    Wraps domain instructions: Instructions

MarkdownInstructions : MarkdownAdapter
    Serialize instructions to Markdown: Instructions,String
    Format instruction sections: Sections,Markdown
    Wraps domain instructions: Instructions

InstructionsSection : SectionView (Base)
    Wraps instructions JSON: Instructions JSON
    Wraps action JSON: Action JSON
    Displays base instructions subsection: BaseInstructionsSubSection
    Displays raw format subsection: RawFormatSubSection
    Submits to AI chat: CLI,Instructions JSON

BaseInstructionsSubSection : SubSectionView
    Wraps instructions JSON: Instructions JSON
    Displays behavior name: String,Instructions JSON
    Displays action name: String,Instructions JSON
    Displays  Instructions: Instructions JSON

RawFormatSubSection : SubSectionView
    Wraps instructions JSON: Instructions JSON
    Displays raw instructions: String,Instructions JSON


## Module: actions.build

BuildKnowledgeAction
    Inject knowledge graph template: Behavior,Content,Knowledge Graph Spec,Knowledge Graph
    Inject builder instructions: Behavior,Content,Build Instructions
    Save Knowledge graph: Behavior,Content,Knowledge Graph

TTYBuildKnowledge : TTYProgressAdapter
    Serialize build action to TTY: BuildKnowledgeAction,String
    Format build status: Status,TTY String
    Wraps domain action: BuildKnowledgeAction

JSONBuildKnowledge : JSONProgressAdapter
    Serialize build action to JSON: BuildKnowledgeAction,JSON String
    Include build metadata: Knowledge Graph Spec,JSON
    Wraps domain action: BuildKnowledgeAction

MarkdownBuildKnowledge : MarkdownProgressAdapter
    Serialize build action to Markdown: BuildKnowledgeAction,Markdown String
    Format build documentation: Knowledge Graph Spec,Markdown
    Wraps domain action: BuildKnowledgeAction

BuildInstructionsSection : InstructionsSection
    Wraps build subsection: BuildDataSubSection

BuildDataSubSection : SubSectionView
    Wraps build JSON: Build JSON
    Displays knowledge graph spec: Object,KnowledgeGraphSpec JSON
    Displays graph structure: Object,KnowledgeGraphSpec JSON
    Displays builder instructions: String,BuilderInstructions JSON
    Opens graph file: CLI,Path JSON


## Module: actions.clarify

GatherContextAction
    Inject gather context instructions: Behavior,Guardrails,Required Clarifications
    Inject questions and evidence: Behavior,Guardrails,Key Questions,Evidence

TTYGatherContext : TTYProgressAdapter
    Serialize clarify action to TTY: GatherContextAction,TTY String
    Format key questions: Questions,Evidence,TTY String
    Wraps domain action: GatherContextAction

JSONGatherContext : JSONProgressAdapter
    Serialize clarify action to JSON: GatherContextAction,JSON String
    Include questions and evidence: Questions,Evidence,JSON
    Wraps domain action: GatherContextAction

MarkdownGatherContext : MarkdownProgressAdapter
    Serialize clarify action to Markdown: GatherContextAction,Markdown String
    Format questions list: Questions,Evidence,Markdown
    Wraps domain action: GatherContextAction

ClarifyInstructionsSection : InstructionsSection
    Wraps clarify subsection: ClarifyDataSubSection

ClarifyDataSubSection : SubSectionView
    Wraps key questions JSON: KeyQuestions JSON
    Displays key questions: List,KeyQuestion JSON
    Updates evidence: CLI,Evidence JSON
    Edits answer: CLI,KeyQuestion JSON


## Module: actions.render

RenderOutputAction
    Inject render output instructions: Behavior,Content,Render Spec,Renderer
    Inject templates: Behavior,Content,Render Spec,Template
    Inject transformers: Behavior,Content,Transformer
    Load + inject structured content: Behavior,Content,Knowledge Graph

TTYRenderOutput : TTYProgressAdapter
    Serialize render action to TTY: RenderOutputAction,TTY String
    Format render status: Render Spec,TTY String
    Wraps domain action: RenderOutputAction

JSONRenderOutput : JSONProgressAdapter
    Serialize render action to JSON: RenderOutputAction,JSON String
    Include render spec: Render Spec,Templates,JSON
    Wraps domain action: RenderOutputAction

MarkdownRenderOutput : MarkdownProgressAdapter
    Serialize render action to Markdown: RenderOutputAction,Markdown String
    Format render documentation: Render Spec,Templates,Markdown
    Wraps domain action: RenderOutputAction

Renderer
    Render complex output: Template,Knowledge Graph,Transformer
    Render outputs using components in context: AI Chat,Template,Content

Template
    Define output structure: Placeholder
    Transform content: Transformer,Content
    Load template: Behavior,Content
Content
    Render outputs: Template,Renderer,Render Spec
    Synchronize formats: Synchronizer,Extractor,Synchronizer Spec
    Save knowledge graph: Knowledge Graph
    Load rendered content: na
    Present rendered content: na

RenderInstructionsSection : InstructionsSection
    Wraps render subsection: RenderDataSubSection

RenderDataSubSection : SubSectionView
    Wraps render JSON: Render JSON
    Displays render spec: Object,RenderSpec JSON
    Displays templates: List,Template JSON
    Displays render instructions: String,RenderInstructions JSON
    Opens template file: CLI,Path JSON

## Module: actions.validate

ValidateRulesAction
    Inject common bot rules: Base Bot,Rules,Common Rules
    Inject behavior specific rules: Behavior,Rules,Behavior Rules
    Load + inject content for validation: Behavior,Content,Knowledge Graph,Rendered Outputs

TTYValidateRules : TTYProgressAdapter
    Serialize validate action to TTY: ValidateRulesAction,TTY String
    Format validation results: Violations,TTY String
    Wraps domain action: ValidateRulesAction

JSONValidateRules : JSONProgressAdapter
    Serialize validate action to JSON: ValidateRulesAction,JSON String
    Include violations and fixes: Violations,Suggestions,JSON
    Wraps domain action: ValidateRulesAction

MarkdownValidateRules : MarkdownProgressAdapter
    Serialize validate action to Markdown: ValidateRulesAction,Markdown String
    Format validation report: Violations,Suggestions,Markdown
    Wraps domain action: ValidateRulesAction

ValidateInstructionsSection : InstructionsSection
    Wraps validate subsection: ValidateDataSubSection

ValidateDataSubSection : SubSectionView
    Wraps validate JSON: Validate JSON
    Displays rules: List,Rule JSON
    Displays rule descriptions: String,Rule JSON
    Displays rule examples: List,Rule JSON
    Opens rule file: CLI,Path JSON

## Module: actions.strategy

StrategyAction
    Inject Strategy instructions: Behavior,Guardrails,Strategy
    Inject decision criteria and assumptions: Behavior,Guardrails,Decision Criteria,Assumptions,Recommended Human Activity

TTYStrategy : TTYProgressAdapter
    Serialize strategy action to TTY: StrategyAction,TTY String
    Format decision criteria: Criteria,Assumptions,TTY String
    Wraps domain action: StrategyAction

JSONStrategy : JSONProgressAdapter
    Serialize strategy action to JSON: StrategyAction,JSON String
    Include criteria and assumptions: Criteria,Assumptions,JSON
    Wraps domain action: StrategyAction

MarkdownStrategy : MarkdownProgressAdapter
    Serialize strategy action to Markdown: StrategyAction,Markdown String
    Format strategy documentation: Criteria,Assumptions,Markdown
    Wraps domain action: StrategyAction

StrategyInstructionsSection : InstructionsSection
    Wraps strategy subsection: StrategyDataSubSection

StrategyDataSubSection : SubSectionView
    Wraps strategy JSON: Strategy JSON
    Displays decision criteria: List,DecisionCriteria JSON
    Displays assumptions: String,Assumptions JSON
    Edits decision criterion: CLI,DecisionCriterion JSON
    Edits assumption: CLI,Assumption JSON


## Module: scope

TTYScope : TTYAdapter
    Serialize scope to TTY: Scope,String
    Format scope type: Scope Type,String
    Format scope values: List,String
    Wraps domain scope: Scope

JSONScope : JSONAdapter
    Serialize scope to JSON dict: Scope,Dict
    Include scope type: Scope Type,String
    Include scope values: List,Array
    Include filtered files: Files,Array
    Wraps domain scope: Scope

MarkdownScope : MarkdownAdapter
    Serialize scope to Markdown: Scope,String
    Format scope documentation: Scope Type,Values,Section
    Wraps domain scope: Scope

ScopeSection : SectionView
    Wraps scope JSON: Scope JSON
    Displays filtered files: FileListTabView
    Filters story graph: CLI,Scope JSON
    Filters files: CLI,Scope JSON
    Clears filter: CLI,Scope JSON
    Displays story graph: StoryGraphTabView
 
StoryGraphTabView : PanelView
    Wraps story map JSON: StoryMap JSON
    Displays epic hierarchy: EpicView,Epic JSON
    Searches stories: Filter,StoryGraph JSON
    Opens story graph file: CLI,File JSON
    Opens story map file: CLI,File JSON

FileListTabView : PanelView
    Wraps file list JSON: Path JSON
    Displays file names: List,Path JSON
    Searches files: Filter,Path JSON
    Opens file: CLI,Path JSON


# Module: story_graph

## Domain 
DomainModule
    Contains domain objects: List[DomainConcept]
    Get submodules: List[Module]
    Get parent module: Module

DomainConcept
    Get name: String
    Get responsibilities: List[Responsibility]
    From dict: Dict,DomainConcept
    To dict: Dict

Responsibility
    Get name: String
    Get collaborators: List[Collaborator]
    From dict: Dict,Responsibility
    To dict: Dict

Collaborator
    Get name: String
    From string: String,Collaborator
    To string: String

TTYDomainConcept : TTYAdapter
    Serialize domain concept to TTY: DomainConcept,TTY String
    Format responsibilities: List[Responsibility],TTY String
    Format CRC card: DomainConcept,TTY String
    Wraps domain concept: DomainConcept

JSONDomainConcept : JSONAdapter
    Serialize domain concept to JSON: DomainConcept,JSON String
    Include responsibilities: List[Responsibility],JSON Array
    Wraps domain concept: DomainConcept

MarkdownDomainConcept : MarkdownAdapter
    Serialize domain concept to Markdown: DomainConcept,Markdown String
    Format CRC table: DomainConcept,Markdown
    Format responsibilities section: List[Responsibility],Markdown
    Wraps domain concept: DomainConcept



## Stories
StoryMap
    Load from bot directory: Bot,StoryMap
    Walk nodes: StoryNode,Iterator[StoryNode]
    Get all stories: List[Story]
    Get all scenarios: List[Scenario]
    Get all domain concepts: List[DomainConcept]
    Find epic by name: Epic Name,Epic
    Find story by name: Story Name,Story
    Get story graph JSON: Dict
    Get epics: List[Epic]

Epic : StoryNode
    Get all stories: List[Story]
    Find sub epic by name: Sub Epic Name,SubEpic
    Get domain concepts: List[DomainConcept]
    Get children: List[StoryNode]
    From dict: Dict,Epic
    To dict: Dict

SubEpic : StoryNode
    Get sequential order: Float
    Get children: List[StoryNode]
    Get parent: StoryNode
    From dict: Dict,SubEpic
    To dict: Dict

StoryGroup : StoryNode
    Get sequential order: Float
    Get children: List[StoryNode]
    Get parent: StoryNode
    From dict: Dict,StoryGroup
    To dict: Dict

Story : StoryNode
    Get sequential order: Float
    Get connector: String
    Get story type: String
    Get users: List[StoryUser]
    Get test file: String
    Get test class: String
    Get default test class: String
    Get scenarios: List[Scenario]
    Get scenario outlines: List[ScenarioOutline]
    Get acceptance criteria: List[AcceptanceCriteria]
    Get children: List[StoryNode]
    Get parent: StoryNode
    From dict: Dict,Story
    To dict: Dict

Scenario : StoryNode
    Get sequential order: Float
    Get test method: String
    Get default test method: String
    Get parent: Story
    Get steps: List[Step]
    Get children: List[Step]
    From dict: Dict,Scenario
    To dict: Dict

ScenarioOutline : StoryNode
    Get sequential order: Float
    Get test method: String
    Get default test method: String
    Get examples: List[Dict]
    Get parent: Story
    Get steps: List[Step]
    Get children: List[Step]
    From dict: Dict,ScenarioOutline
    To dict: Dict

AcceptanceCriteria : StoryNode
    Get sequential order: Float
    Get parent: Story
    Get steps: List[Step]
    Get children: List[Step]
    From dict: Dict,AcceptanceCriteria
    To dict: Dict

Step : StoryNode
    Get sequential order: Float
    Get text: String
    Get parent: StoryNode
    Get children: List[StoryNode]
    From dict: Dict,Step
    To dict: Dict

StoryUser
    Get name: String
    From string: String,StoryUser
    From list: List[String],List[StoryUser]
    To string: String


TTYStoryMap : TTYAdapter
    Serialize story map to TTY: StoryMap,TTY String
    Format epics list: List[Epic],TTY String
    Format story hierarchy: StoryMap,TTY String
    Walk and format nodes: StoryNode,TTY String
    Wraps domain story map: StoryMap

JSONStoryMap : JSONAdapter
    Serialize story map to JSON: StoryMap,JSON String
    Include story graph: Dict,JSON
    Include all epics: List[Epic],JSON Array
    Wraps domain story map: StoryMap

MarkdownStoryMap : MarkdownAdapter
    Serialize story map to Markdown: StoryMap,Markdown String
    Format epic hierarchy: List[Epic],Markdown
    Format story index: List[Story],Markdown
    Wraps domain story map: StoryMap

TTYStoryNode : TTYAdapter (Base)
    Serialize node to TTY: StoryNode,TTY String
    Format name: String,TTY String
    Format sequential order: Float,TTY String
    Format children: List[StoryNode],TTY String
    Wraps domain story node: StoryNode

JSONStoryNode : JSONAdapter (Base)
    Serialize node to JSON: StoryNode,JSON String
    Include name: String,JSON
    Include sequential order: Float,JSON
    Include children: List[StoryNode],JSON Array
    Wraps domain story node: StoryNode

MarkdownStoryNode : MarkdownAdapter (Base)
    Serialize node to Markdown: StoryNode,Markdown String
    Format node header: String,Sequential Order,Markdown
    Format children list: List[StoryNode],Markdown
    Wraps domain story node: StoryNode

TTYEpic : TTYStoryNode
    Format domain concepts: List[DomainConcept],TTY String
    Wraps domain epic: Epic

JSONEpic : JSONStoryNode
    Include domain concepts: List[DomainConcept],JSON Array
    Wraps domain epic: Epic

MarkdownEpic : MarkdownStoryNode
    Format domain concepts table: List[DomainConcept],Markdown
    Wraps domain epic: Epic

TTYStory : TTYStoryNode
    Format users: List[StoryUser],TTY String
    Format connector: String,TTY String
    Format test metadata: Test File,Test Class,TTY String
    Wraps domain story: Story

JSONStory : JSONStoryNode
    Include users: List[StoryUser],JSON Array
    Include test metadata: Test File,Test Class,JSON
    Wraps domain story: Story

MarkdownStory : MarkdownStoryNode
    Format story card: Story,Markdown
    Format users section: List[StoryUser],Markdown
    Wraps domain story: Story

TTYScenario : TTYStoryNode
    Format steps: List[Step],TTY String
    Format test method: Test Method,TTY String
    Wraps domain scenario: Scenario

JSONScenario : JSONStoryNode
    Include steps: List[Step],JSON Array
    Include test method: Test Method,JSON
    Wraps domain scenario: Scenario

MarkdownScenario : MarkdownStoryNode
    Format Gherkin scenario: Scenario,Markdown
    Format steps as Given/When/Then: List[Step],Markdown
    Wraps domain scenario: Scenario


StoryMapView : PanelView
    Wraps story map JSON: StoryMap JSON
    Displays epic hierarchy: EpicView,Epic JSON
    Searches stories: Filter,StoryGraph JSON
    Opens story graph file: CLI,File JSON
    Opens story map file: CLI,File JSON

EpicView : PanelView
    Wraps epic JSON: Epic JSON
    Displays epic name: String,Epic JSON
    Displays epic icon: Image
    Displays sub epics: SubEpicView,SubEpic JSON
    Toggles collapsed: State
    Opens epic folder: CLI,Epic JSON
    Opens epic test file: CLI,Epic JSON

SubEpicView : PanelView
    Wraps sub epic JSON: SubEpic JSON
    Displays sub epic name: String,SubEpic JSON
    Displays sub epic icon: Image
    Displays nested sub epics: SubEpicView,SubEpic JSON
    Displays stories: StoryView,Story JSON
    Toggles collapsed: State
    Opens sub epic folder: CLI,SubEpic JSON
    Opens sub epic test file: CLI,SubEpic JSON

StoryView : PanelView
    Wraps story JSON: Story JSON
    Displays story name: String,Story JSON
    Displays story icon: Image
    Displays scenarios: ScenarioView,Scenario JSON
    Toggles collapsed: State
    Opens test at class: CLI,Story JSON

ScenarioView : PanelView
    Wraps scenario JSON: Scenario JSON
    Displays scenario name: String,Scenario JSON
    Displays scenario icon: Image
    Opens test at scenario: CLI,Scenario JSON


## help

TTYHelp : TTYAdapter
    Serialize help to TTY: Help,String
    Format help sections: Sections,String
    Wraps domain help: Help

JSONHelp : JSONAdapter
    Serialize help to JSON: Help,Dict
    Include help sections: Sections,Array
    Wraps domain help: Help

MarkdownHelp : MarkdownAdapter
    Serialize help to Markdown: Help,String
    Format help sections: Sections,Markdown
    Wraps domain help: Help


### status

Status
    Get progress path: String
    Get stage name: String
    Get current behavior name: String
    Get current action name: String
    Get has current behavior: Boolean
    Get has current action: Boolean

TTYStatus : TTYAdapter
    Serialize status to TTY: Status,TTY String
    Format progress line: Progress Path,Stage Name,TTY String
    Format hierarchical status: Bot,Status,TTY String
    Wraps domain status: Status

JSONStatus : JSONAdapter
    Serialize status to JSON: Status,JSON String
    Include progress path: Progress Path,String
    Include stage name: Stage Name,String
    Include current behavior: Behavior Name,String
    Include current action: Action Name,String
    Wraps domain status: Status

MarkdownStatus : MarkdownAdapter
    Serialize status to Markdown: Status,Markdown String
    Format progress section: Progress Path,Stage Name,Markdown String
    Format workflow state: Status,Markdown String
    Wraps domain status: Status


## Module: scope

Scope
    Get filter: String (read/write property)
    Set filter: String
    Get results: List (read-only property)
    Apply filter to behaviors: Behaviors,Filtered Behaviors
    Apply filter to stories: Stories,Filtered Stories
    Clear filter: 
    Get filter count: Integer
    Get is active: Boolean

TTYScope : TTYAdapter
    Serialize scope to TTY: Scope,TTY String
    Format filter display: Filter String,TTY String
    Format results list: Results,TTY String
    Format filter status: Is Active,Count,TTY String
    Wraps domain scope: Scope

JSONScope : JSONAdapter
    Serialize scope to JSON: Scope,JSON String
    Include filter: Filter String,String
    Include results: Results List,Array
    Include filter metadata: Is Active,Count,JSON
    Wraps domain scope: Scope

MarkdownScope : MarkdownAdapter
    Serialize scope to Markdown: Scope,Markdown String
    Format filter section: Filter String,Markdown String
    Format results list: Results,Markdown List
    Format filter documentation: Scope,Markdown String
    Wraps domain scope: Scope

ScopeView : SectionView
    Wraps scope JSON: Scope JSON
    Displays current filter: String,Scope JSON
    Edits filter: CLI,Scope JSON
    Displays filtered results: List,Scope JSON
    Clears filter: CLI,Scope JSON
    Displays filter status: Is Active,Count,Scope JSON


## Module: navigation

NavigationResult
    Get previous action: Action
    Get next action: Action
    Get can navigate back: Boolean
    Get can navigate next: Boolean
    Get navigation path: String

TTYNavigation : TTYAdapter
    Serialize navigation to TTY: NavigationResult,TTY String
    Format navigation options: Can Back,Can Next,TTY String
    Format navigation path: Path String,TTY String
    Wraps domain navigation: NavigationResult

JSONNavigation : JSONAdapter
    Serialize navigation to JSON: NavigationResult,JSON String
    Include previous action: Action,JSON
    Include next action: Action,JSON
    Include navigation state: Can Back,Can Next,JSON
    Wraps domain navigation: NavigationResult

MarkdownNavigation : MarkdownAdapter
    Serialize navigation to Markdown: NavigationResult,Markdown String
    Format navigation section: NavigationResult,Markdown String
    Wraps domain navigation: NavigationResult


## Module: bot_path

BotPath
    Get bot directory: Path
    Get workspace directory: Path
    Get behaviors directory: Path
    Get config path: Path
    Get all paths: Dict

TTYBotPath : TTYAdapter
    Serialize bot path to TTY: BotPath,TTY String
    Format path display: Path Name,Path Value,TTY String
    Format all paths: BotPath,TTY String
    Wraps domain bot path: BotPath

JSONBotPath : JSONAdapter
    Serialize bot path to JSON: BotPath,JSON String
    Include all paths: Dict,JSON
    Wraps domain bot path: BotPath

MarkdownBotPath : MarkdownAdapter
    Serialize bot path to Markdown: BotPath,Markdown String
    Format paths section: BotPath,Markdown String
    Wraps domain bot path: BotPath


## Module: exit_result

ExitResult
    Get exit code: Integer
    Get exit message: String
    Get should cleanup: Boolean

TTYExitResult : TTYAdapter
    Serialize exit result to TTY: ExitResult,TTY String
    Format exit message: Message,TTY String
    Wraps domain exit result: ExitResult

JSONExitResult : JSONAdapter
    Serialize exit result to JSON: ExitResult,JSON String
    Include exit code: Integer,JSON
    Include exit message: String,JSON
    Wraps domain exit result: ExitResult

MarkdownExitResult : MarkdownAdapter
    Serialize exit result to Markdown: ExitResult,Markdown String
    Format exit documentation: ExitResult,Markdown String
    Wraps domain exit result: ExitResult