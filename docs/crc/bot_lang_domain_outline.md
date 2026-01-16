## Module: BotLang

BotLangActionNode
    Wrap action execution: Action,Behavior
    Get instructions from action: Action
    Confirm with response: Action,AI Chat
    Run in autonomous mode: AI Client,BotLangMode
    Run in interactive mode: Human,BotLangMode

BotLangFlow
    Execute nodes in sequence: BotLangActionNode,BotLangFlowRunner
    Handle conditional branching: Decision Node,BotLangState
    Support loops and iterations: BotLangActionNode,BotLangState
    Pause at interactive points: Human,BotLangMode
    Resume from checkpoint: Checkpoint,BotLangFlowRunner

BotLangFlowRunner
    Compile graph with checkpointer: BotLangFlow,Checkpoint
    Execute workflow graph: BotLangFlow,BotLangActionNode
    Manage checkpoint storage: Checkpoint
    Resume from checkpoint: Checkpoint,BotLangFlow

BotLangState
    Contain story graph: Story Graph
    Contain clarification data: Key Questions,Evidence
    Contain strategy data: Decision Criteria,Assumptions
    Contain context files: Context
    Contain files dictionary: Source Files,Test Files
    Contain workspace directory: Workspace
    Contain workflow execution state: Action,Instructions

BotLangMode
    Determine AI interaction: BotLangActionNode,AI Client
    Control pause points: BotLangActionNode,Human

Checkpoint
    Save workflow state: BotLangState,BotLangFlowRunner
    Restore workflow state: BotLangState,BotLangFlowRunner
    Track execution history: BotLangState
    Enable resume capability: BotLangFlow,BotLangFlowRunner


## Module: actions

Base Action
    Inject Instructions: Behavior
    Load Relevant Content + Inject Into Instructions: Content
    Save content changes: Content

Guardrails
    Provide required context: Key Questions,Evidence
    Guide planning decisions: Decision Criteria,Assumptions
    Define recommended human activity: Human,Instructions

Behavior Action State
    Track current action: Action
    Track completed actions: Action,Activity Log
    Determine next action: Action,Behavior
    Pause workflow: Human,AI Chat
    Resume workflow: Human,AI Chat

Action
    Execute behavior action: Behavior,Workspace
    Get instructions: Behavior,Guardrails,Content
    Save results: Content,Workspace

Actions
    Manage action collection: Action,ActionFactory
    Track current action: Action,ActionStateManager
    Navigate between actions: Action,Behavior

ActionFactory
    Create action instances: Action,Behavior
    Resolve action dependencies: Behavior,Workspace

ActionContext
    Provide execution context: Workspace,Behavior
    Supply workspace path: Path
    Supply behavior config: Behavior

ActivityTracker
    Track action execution: Action,Activity Log
    Record activity log: Action,Timestamp

ActionStateManager
    Manage action state: Action,State
    Persist state to disk: File,JSON
    Load previous state: File,JSON

Instructions
    Format instructions for AI: Template,Context
    Inject context data: Behavior,Content

ContextDataInjector
    Inject behavior context: Behavior,Instructions
    Inject guardrails: Guardrails,Instructions
    Inject content specs: Content,Instructions

ScopingParameter
    Parse scope parameters: String,Dict
    Validate scope type: ScopeType

ActionScope
    Base scope class: Scope,Parameters
    Define action scope: ScopeType,Values
    Filter by epic/story/increment: StoryGraph
    Get story names from scope: StoryGraph,Names

Content
    Render outputs: Template,Renderer,Render Spec
    Synchronize formats: Synchronizer,Extractor
    Save knowledge graph: Knowledge Graph,File
    Load rendered content: File,Path
    Present rendered content: AI Chat

Workflow State
    Track current action: Action
    Track completed actions: Action,Activity Log
    Determine next action: Action,Behavior
    Pause workflow: Human,AI Chat
    Resume workflow: Human,AI Chat


## Module: actions.clarify

ClarifyContextAction
    Prepare clarify instructions: RequiredContext,Instructions
    Submit clarification answers: Answers,Evidence,Context
    Save clarifications: RequirementsClarifications

RequiredContext
    Load guardrails: KeyQuestions,Evidence
    Provide instructions: Questions,Evidence

KeyQuestions
    Load questions from JSON: Path,Questions
    Provide questions list: Questions

Evidence
    Load evidence from JSON: Path,Evidence
    Provide evidence list: Evidence

RequirementsClarifications
    Persist clarifications to JSON: Answers,Evidence,Context
    Load clarifications from JSON: BehaviorName,Data
    Merge clarification data: Existing,New


## Module: actions.strategy

StrategyAction
    Prepare strategy instructions: Strategy,Instructions
    Submit strategy decisions: Decisions,Assumptions
    Save strategy decisions: StrategyDecision

Strategy
    Load guardrails: StrategyCriterias,Assumptions
    Provide instructions: DecisionCriteria,Assumptions

StrategyCriterias
    Load criteria from JSON: Path,Criterias
    Provide criteria collection: StrategyCriteria

StrategyCriteria
    Define single criterion: Question,Options,Outcome
    Structure decision data: JSON

Assumptions
    Load assumptions from JSON: Path,Assumptions
    Provide assumptions list: Assumptions

StrategyDecision
    Persist strategy decisions to JSON: Decisions,Assumptions
    Load decisions from JSON: BehaviorName,Data
    Merge decision data: Existing,New

JsonPersistent
    Serialize to JSON: Data,File
    Load from JSON: File,Data
    Merge data: Existing,New


## Module: actions.build

BuildKnowledgeAction
    Prepare build instructions: Knowledge,Rules,Scope
    Inject knowledge graph template: Template,Instructions
    Inject rules: Rules,Instructions
    Submit build results: KnowledgeGraph

Knowledge
    Load knowledge graph spec: KnowledgeGraphSpec
    Provide file path references: ConfigPath,TemplatePath

KnowledgeGraphSpec
    Load config from JSON: Path,Config
    Load template: KnowledgeGraphTemplate
    Provide output path: Path,Filename

KnowledgeGraphTemplate
    Load template from file: Path,Template
    Check template exists: Exists

BuildScope : ActionScope
    Define build scope: ScopeType,Values
    Get story names from scope: StoryGraph,Names
    Default to 'all' when unspecified: Scope


## Module: actions.render

RenderOutputAction
    Prepare render instructions: RenderSpecs,Instructions
    Execute synchronizers: RenderSpecs,Synchronizers
    Submit render results: ExecutedSpecs,TemplateSpecs

RenderConfigLoader
    Load render specs: Path,RenderSpec
    Load render instructions: Path,Instructions

RenderInstructionBuilder
    Inject render data: Instructions,RenderSpecs
    Format render instructions: Instructions

RenderSpec
    Load configuration: File,Config
    Execute synchronizer: Synchronizer,Result
    Track execution status: Executed,Failed

Synchronizer
    Transform data to output: Data,Output
    Execute transformation: Input,Output

Template
    Load template content: Path,Content
    Provide template structure: Structure


## Module: actions.rules



Rule
    Validate content: Content,Violations
    Find behavior specific rules: Behavior,Rules
    Find common bot rules: Base Bot,Rules
    Load diagnostics results: Violations,Corrections
    Suggest corrections: Violations,Suggestions
    Provide examples - Do: Examples,Description
    Provide examples - Dont: Examples,Description
    Specialized examples: Language,Framework,Pattern

RuleLoader
    Load rules from disk: File,Path
    Parse rule JSON: JSON,Rule

RuleFilter
    Filter rules by criteria: Criteria,Rules
    Apply exclusions: Exclusions,Rules

Rules
    Manage rule collection: Rule,RuleLoader
    Execute validation: Content,Scanner

RulesDigestGuidance
    Generate rule summaries: Rules,Summary
    Format for AI context: Rules,Instructions

ValidationCallbacks
    Handle validation events: Event,Handler
    Report progress: Progress,Status

ValidationContext
    Provide validation context: Context,Config
    Supply rule configuration: Rules,Config


## Module: actions.validate

ValidateRulesAction
    Prepare validation instructions: Rules,ScannerResults
    Run scanners: ValidationExecutor,Context
    Format rules with file paths: Rules,Instructions
    Submit validation results: Report,Violations

ValidationExecutor
    Execute synchronous validation: Context,Rules
    Run scanner batch: Scanner,Files
    Collect results: Violations,Stats

ValidationReportBuilder
    Build validation report: Violations,Stats
    Aggregate violations: Violations,Summary

ValidationReportFormatter
    Format report output: Report,Format
    Generate markdown: Report,Markdown

ValidationReportWriter
    Write report to disk: Report,File
    Stream output to status file: Report,Stream

ValidationScope : ActionScope
    Define validation scope: ScopeType,Files
    Filter files: Files,Patterns
    Handle file discovery: FileDiscovery,PathResolver
    Support 'files' scope type: Files,Exclude,Skiprule

ValidationStats
    Track validation statistics: Stats,Counts
    Count violations: Violations,Total

KnowledgeGraph
    Load story graph: StoryGraph,File
    Validate structure: Graph,Schema

StoryGraph
    Represent story graph data: Graph,Nodes
    Navigate graph structure: Nodes,Links

FileDiscovery
    Discover files to validate: Path,Patterns
    Apply filters: Files,Filters

FileLinkBuilder
    Build file links: Path,URL
    Generate URLs: File,URL

PathResolver
    Resolve file paths: Path,Workspace
    Handle workspace roots: Workspace,Path

BackgroundValidationHandler
    Handle background validation: Validation,Async
    Manage async execution: Task,Result

ViolationFormatter
    Format violation output: Violation,Format
    Generate messages: Violation,Message


## Module: bot

Bot
    Load bot configuration: BotConfig,BotPaths
    Manage behaviors: Behaviors,Collection
    Provide bot metadata: Name,Description,Goal
    Provide help: Topic,HelpText
    Handle scope: ScopeFilter,Scope
    Handle path: WorkingDirectory,Path

Behavior
    Load behavior configuration: BehaviorConfig,BotPaths
    Manage actions: Actions,Workflow
    Provide behavior metadata: Name,Description,Goal,Order
    Provide trigger words: TriggerWords
    Provide guardrails: Guardrails
    Provide content: Content
    Provide rules: Rules
    Check completion status: IsCompleted
    Match trigger words: Text,Matches

Behaviors
    Discover behaviors: BehaviorDirectory,Behaviors
    Manage behavior collection: Behavior,List
    Track current behavior: Current,Index
    Navigate behaviors: NavigateTo,Current
    Advance through workflow: Advance,Next
    Go back in workflow: GoBack,Previous
    Load and save state: StateFile,JSON
    Initialize state: ConfirmedBehavior,State

BotPaths
    Resolve workspace directory: Path,Environment
    Resolve bot directory: Path,Environment
    Resolve base actions directory: Path
    Resolve documentation path: Path
    Update workspace directory: NewPath,Persist
    Resolve path parameters: Parameters,Absolute

BotResult
    Structure bot results: Status,Behavior,Action,Data
    Track execution context: Behavior,Action

MergedInstructions
    Merge instruction sources: BaseInstructions,RenderInstructions
    Provide merged result: Dictionary

Workspace
    Get workspace directory: Environment,Path
    Get bot directory: Environment,Path
    Get base actions directory: Path
    Get behavior folder: BotName,BehaviorName,Path


## Module: ext

Router
    Match trigger patterns: Trigger Words,Route
    Route to MCP bot tool: Base Bot,Trigger Words
    Route to behavior tool: Behavior,Trigger Words
    Route to action tool: Action,Trigger Words
    Forward to behavior: Behavior,Base Bot
    Forward to action: Action,Behavior
    Forward to current behavior and action: Behavior,Action,Base Bot

TriggerRouter
    Match trigger patterns: Pattern,Route
    Route to behaviors: Behavior,Pattern

TriggerWords
    Define trigger patterns: Pattern,Regex
    Match user input: Input,Pattern

BehaviorMatcher
    Match behavior triggers: Trigger,Behavior
    Find target behavior: Name,Behavior

BotMatcher
    Match bot triggers: Trigger,Bot
    Route to bot: Name,Bot

ActionTriggers
    Define action triggers: Trigger,Action
    Match action names: Name,Action

BehaviorTriggers
    Define behavior triggers: Trigger,Behavior
    Match behavior names: Name,Behavior

BotTriggers
    Define bot triggers: Trigger,Bot
    Match bot names: Name,Bot


## Module: story_graph

DomainConcept
    Represent domain concept: Concept,Responsibilities
    Hold responsibilities: Responsibility,Collaborator

Responsibility
    Define responsibility: Name,Description
    List collaborators: Collaborator,List

Collaborator
    Represent collaborator: Name,Concept
    Link to concept: Concept,Link

StoryUser
    Represent story user: User,Type
    Define user type: Type,Role

Epic
    Represent epic: Name,SubEpics
    Contain sub-epics: SubEpic,List

SubEpic
    Represent sub-epic: Name,Stories
    Contain stories: Story,List

Story
    Represent story: Name,Scenarios
    Contain scenarios: Scenario,List

Scenario
    Represent scenario: Name,Steps
    Define test cases: Steps,Examples

ScenarioOutline
    Represent scenario outline: Name,Examples
    Include examples table: Examples,Table

AcceptanceCriteria
    Define acceptance criteria: Criteria,Requirements
    Structure requirements: Given,When,Then

Step
    Represent scenario step: Type,Action
    Define Given/When/Then: Type,Description

StoryMap
    Represent story map: Epics,Hierarchy
    Navigate hierarchy: Nodes,Links

StoryNode
    Represent story node: Node,Type
    Link to parent/children: Parent,Children

StoryGroup
    Group related stories: Stories,Theme
    Organize by theme: Theme,Stories


## Module: mcp

MCPServer
    Define MCP server: Server,Tools
    Configure tools: Tools,Config

MCPServerGenerator
    Generate MCP server code: Server,Code
    Create server files: Files,Output

MCPCodeGenerator
    Generate MCP code: Code,Template
    Format tool definitions: Tools,Format

MCPCodeVisitor
    Visit code elements: AST,Elements
    Extract tool info: Elements,Tools

MCPConfigGenerator
    Generate MCP config: Config,JSON
    Format JSON: JSON,Output

ServerDeployer
    Deploy MCP server: Server,Deploy
    Install dependencies: Dependencies,Install

ToolCatalog
    Catalog MCP tools: Tools,Catalog
    Track tool entries: Entry,List

ToolEntry
    Represent tool entry: Entry,Metadata
    Define tool metadata: Name,Description,Parameters

DeploymentResult
    Structure deployment result: Result,Status
    Track success/failure: Success,Error


## Module: scanners

Scanner
    Base scanner interface: Interface,Abstract
    Execute validation: Content,Violations
    Scan files and blocks: Files,Blocks,Violations

CodeScanner : Scanner
    Scan code files: Files,AST
    Validate code patterns: Pattern,Violations

DomainScanner : Scanner
    Scan domain concepts: StoryGraph,Concepts
    Validate domain model: Concepts,Violations

StoryScanner : Scanner
    Scan story nodes: StoryGraph,Stories
    Validate story structure: Structure,Violations

TestScanner : Scanner
    Scan test files: Files,Tests
    Validate test quality: Quality,Violations

ScannerRegistry
    Register scanners: Scanner,Registry
    Load scanner modules: Module,Scanner

ScannerLoader
    Load scanner classes: Class,Scanner
    Instantiate scanners: Scanner,Instance

ScannerOrchestrator
    Orchestrate scanner execution: Scanners,Execution
    Collect results: Results,Violations

Violation
    Represent validation violation: Location,Message
    Include location and message: Line,Column,Text

ScannerStatusFormatter
    Format scanner status: Status,Format
    Display progress: Progress,Display

ScannerExecutionError
    Handle scanner errors: Error,Message
    Format error messages: Error,Format

ValidationScannerStatusBuilder
    Build scanner status: Scanner,Status
    Track progress: Scanner,Progress

Scope
    Represent code scope: Level,Parent
    Track nesting: Depth,Parent

Scan
    Represent scan result: Result,Violations
    Hold violations: Violations,List

Note: 100+ specific scanner implementations (e.g., DuplicationScanner, SpecificityScanner, 
BusinessReadableTestNamesScanner, etc.) inherit from CodeScanner, DomainScanner, StoryScanner, 
or TestScanner and reside in the scanners/ directory.


## Module: scanners.code

File
    Represent file: Path,Content
    Parse content: Content,AST
    Read and parse Python files: Path,AST

Line
    Represent line: Number,Text
    Track position: Number,Column

Block
    Represent code block: Start,End
    Define boundaries: Lines,Scope

BlockExtractor
    Extract code blocks: Content,Blocks
    Identify structure: AST,Blocks

ASTElement
    Base AST element: Node,Properties
    Common properties: Type,Location

Class
    Represent class: Name,Methods
    Hold methods: Methods,List
    Check if test class: Name,Boolean

Classes
    Collection of classes: Class,List
    Navigate by name: Name,Class
    Extract from AST: AST,Classes

Function
    Represent function: Name,Parameters
    Hold parameters: Parameters,List
    Check if test function: Name,Boolean

Functions
    Collection of functions: Function,List
    Navigate by name: Name,Function
    Extract from AST: AST,Functions

Import
    Represent import: Module,Name
    Track module: Module,Path

Imports
    Collection of imports: Import,List
    Find duplicates: Import,Duplicates
    Extract from AST: AST,Imports

IfStatement
    Represent if statement: Condition,Body
    Track conditions: Condition,Branches

IfStatements
    Collection of if statements: Statement,List
    Count nesting: Depth,Count
    Extract from AST: AST,IfStatements

TryBlock
    Represent try block: Body,Handlers
    Track handlers: Except,Finally

TryBlocks
    Collection of try blocks: Block,List
    Find patterns: Pattern,Violations
    Extract from AST: AST,TryBlocks


## Module: generator

Orchestrator
    Orchestrate generation: Tasks,Visitors
    Coordinate visitors: Visitor,Execution

Visitor
    Visit code elements: AST,Elements
    Extract information: Elements,Data

ActionDataCollector
    Collect action data: Action,Metadata
    Build action metadata: Name,Parameters,Description

ActionHelpContext
    Build action help: Action,Help
    Format action info: Name,Description,Parameters

BehaviorHelpContext
    Build behavior help: Behavior,Help
    Format behavior info: Name,Description,Actions