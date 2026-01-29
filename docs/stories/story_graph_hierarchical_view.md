# Story Graph: Epics, Sub-Epics, and Domain Concepts

This document shows the complete hierarchical structure of epics and sub-epics,
along with all domain concepts in full detail, including complete realization walks.


## Table of Contents

- [Story Graph: Epics, Sub-Epics, and Domain Concepts](#story-graph:-epics-sub-epics-and-domain-concepts)
- [Build Agile Bots](#build-agile-bots)
  - [Generate MCP Tools](#generate-mcp-tools)
  - [Generate CLI](#generate-cli)
- [Invoke Bot](#invoke-bot)
  - [Initialize Bot](#initialize-bot)
    - [Load Bot, Behavior, and Actions](#load-bot-behavior-and-actions)
    - [Initialize Bot Interface](#initialize-bot-interface)
    - [Render Bot Interface](#render-bot-interface)
    - [Set Workspace](#set-workspace)
  - [Work With Story Map](#work-with-story-map)
    - [Scope Files](#scope-files)
    - [Scope Stories](#scope-stories)
    - [Edit Story Map](#edit-story-map)
    - [Edit Increments](#edit-increments)
    - [Act With Selected Node](#act-with-selected-node)
  - [Navigate Behavior Actions](#navigate-behavior-actions)
    - [Navigate Behavior And Actions](#navigate-behavior-and-actions)
    - [Perform Behavior Action In Bot Workflow](#perform-behavior-action-in-bot-workflow)
    - [Display Behavior Action State](#display-behavior-action-state)
  - [Perform Action](#perform-action)
    - [Prepare Common Instructions For Behavior, Action, and Scope](#prepare-common-instructions-for-behavior-action-and-scope)
    - [Clarify Requirements](#clarify-requirements)
    - [Decide Strategy](#decide-strategy)
    - [Build Story Graph](#build-story-graph)
    - [Validate With Rules](#validate-with-rules)
    - [Render Content](#render-content)
    - [Use Rules In Prompt](#use-rules-in-prompt)
    - [Synchronize Graph From Rendered](#synchronize-graph-from-rendered)
  - [Get Help](#get-help)

# Build Agile Bots


## Generate MCP Tools


## Generate CLI


# Invoke Bot


## Initialize Bot


### Load Bot, Behavior, and Actions

    ## Domain Concepts (9 concepts)

      - **Base Bot**
        Module: `bot`
        Responsibilities:
          - Executes Actions
            Collaborators: Workflow, Behavior, Action
          - Execute behavior
            Collaborators: Behavior, BotResult
          - Execute current action
            Collaborators: BotResult
          - Navigate and execute
            Collaborators: Behavior, Action, ActionContext, BotResult
          - Validate behavior exists
            Collaborators: Behavior, Boolean
          - Validate action exists
            Collaborators: Behavior, Action, Boolean
          - Track activity
            Collaborators: Behavior, Action
          - Route to behaviors and actions
            Collaborators: Router, Trigger Words
          - Persist content
            Collaborators: Content
          - Manage Project State
            Collaborators: Project
          - Render
          - Get scope
            Collaborators: Scope (read-only property)
          - Get status
            Collaborators: Status
          - Navigate next
            Collaborators: NavigationResult
          - Navigate back
            Collaborators: NavigationResult
          - Get bot path
            Collaborators: BotPath
          - Get help
            Collaborators: Help
          - Exit
            Collaborators: ExitResult

      - **Specific Bot**
        Module: `bot`
        Responsibilities:
          - Provide Behavior config
            Collaborators: Bot Config, Behavior
          - Provide MCP config
            Collaborators: MCP Config
          - Provide Renderers
          - Provide Extractors
          - Provide Synchronizer
          - Provide Trigger Words

      - **TTYBot**
        Module: `bot`
        Responsibilities:
          - Execute behavior by name
            Collaborators: Behavior Name String, TTY String
          - Execute current action
            Collaborators: TTY String
          - Navigate and execute
            Collaborators: Dot Notation String, TTY String
          - Validate behavior exists
            Collaborators: Behavior Name String, TTY String (True/False)
          - Validate action exists
            Collaborators: Dot Notation String, TTY String (True/False)
          - Serialize entire bot to TTY
            Collaborators: Bot, TTY String
          - Bot header
            Collaborators: Bot Name, TTY String
          - Behaviors
            Collaborators: Bot, Behaviors, TTY Behaviors
          - Get status
            Collaborators: TTY String (delegates to TTYStatus)
          - Get scope
            Collaborators: TTY String (delegates to TTYScope)
          - Navigate next
            Collaborators: TTY String (delegates to TTYNavigation)
          - Navigate back
            Collaborators: TTY String (delegates to TTYNavigation)
          - Get bot path
            Collaborators: TTY String (delegates to TTYBotPath)
          - Get help
            Collaborators: TTY String (delegates to TTYHelp)
          - Exit
            Collaborators: TTY String (delegates to TTYExitResult)
          - Wraps domain bot
            Collaborators: Bot
        Inherits from: TTYAdapter

      - **JSONBot**
        Module: `bot`
        Responsibilities:
          - Execute behavior by name
            Collaborators: Behavior Name String, JSON String
          - Execute current action
            Collaborators: JSON String
          - Navigate and execute
            Collaborators: Dot Notation String, JSON String
          - Validate behavior exists
            Collaborators: Behavior Name String, JSON String
          - Validate action exists
            Collaborators: Dot Notation String, JSON String
          - Serialize bot to JSON
            Collaborators: Bot, JSON String
          - Include bot metadata
            Collaborators: Name, Directory, Paths
          - Behaviors
            Collaborators: Bot, Behaviors, JSON Behaviors
          - Get status
            Collaborators: JSON String (delegates to JSONStatus)
          - Get scope
            Collaborators: JSON String (delegates to JSONScope)
          - Navigate next
            Collaborators: JSON String (delegates to JSONNavigation)
          - Navigate back
            Collaborators: JSON String (delegates to JSONNavigation)
          - Get bot path
            Collaborators: JSON String (delegates to JSONBotPath)
          - Get help
            Collaborators: JSON String (delegates to JSONHelp)
          - Exit
            Collaborators: JSON String (delegates to JSONExitResult)
          - Wraps domain bot
            Collaborators: Bot
        Inherits from: JSONAdapter

      - **MarkdownBot**
        Module: `bot`
        Responsibilities:
          - Execute behavior by name
            Collaborators: Behavior Name String, Markdown String
          - Execute current action
            Collaborators: Markdown String
          - Navigate and execute
            Collaborators: Dot Notation String, Markdown String
          - Validate behavior exists
            Collaborators: Behavior Name String, Markdown String
          - Validate action exists
            Collaborators: Dot Notation String, Markdown String
          - Serialize bot to Markdown
            Collaborators: Bot, Markdown String
          - Format bot documentation
            Collaborators: Bot Name, Description, Markdown Header
          - Behaviors
            Collaborators: Bot, Behaviors, Markdown Behaviors
          - Get status
            Collaborators: Markdown String (delegates to MarkdownStatus)
          - Get scope
            Collaborators: Markdown String (delegates to MarkdownScope)
          - Navigate next
            Collaborators: Markdown String (delegates to MarkdownNavigation)
          - Navigate back
            Collaborators: Markdown String (delegates to MarkdownNavigation)
          - Get bot path
            Collaborators: Markdown String (delegates to MarkdownBotPath)
          - Get help
            Collaborators: Markdown String (delegates to MarkdownHelp)
          - Exit
            Collaborators: Markdown String (delegates to MarkdownExitResult)
          - Wraps domain bot
            Collaborators: Bot
        Inherits from: MarkdownAdapter

      - **Behavior**
        Module: `behaviors`
        Responsibilities:
          - Name
            Collaborators: String
          - Description
            Collaborators: String
          - Goal
            Collaborators: String
          - Folder
            Collaborators: Path
          - Is completed
            Collaborators: Boolean
          - Actions workflow
            Collaborators: List
          - Action Names
            Collaborators: List
          - Validation type
            Collaborators: ValidationType
          - CurrentAction
            Collaborators: Action
          - Guardrails
            Collaborators: Guardrails
          - Content
            Collaborators: Content
          - Rules
            Collaborators: Rules
          - Actions
            Collaborators: Actions

      - **TTYBehavior**
        Module: `behaviors`
        Responsibilities:
          - Serialize behavior to TTY
            Collaborators: Behavior, String
          - Format behavior line
            Collaborators: Behavior Name, Marker, Color
          - Format actions
            Collaborators: Actions, String
          - Wraps domain behavior
            Collaborators: Behavior
        Inherits from: TTYProgressAdapter

      - **JSONBehavior**
        Module: `behaviors`
        Responsibilities:
          - Serialize behavior to JSON dict
            Collaborators: Behavior, Dict
          - Include behavior metadata
            Collaborators: Name, Description, Status
          - Include actions
            Collaborators: Actions, Array
          - Wraps domain behavior
            Collaborators: Behavior
        Inherits from: JSONProgressAdapter

      - **MarkdownBehavior**
        Module: `behaviors`
        Responsibilities:
          - Serialize behavior to Markdown
            Collaborators: Behavior, String
          - Format behavior documentation
            Collaborators: Behavior Name, Description, Section
          - Format actions
            Collaborators: Actions, Markdown Subsections
          - Wraps domain behavior
            Collaborators: Behavior
        Inherits from: MarkdownProgressAdapter


### Initialize Bot Interface

    ## Domain Concepts (11 concepts)

      - **CLISession**
        Module: `cli`
        Responsibilities:
          - Runs CLI loop
          - Reads input from stdin or terminal
          - Determine channel adapter
            Collaborators: ChannelAdapter
          - Read and execute command
            Collaborators: Command String, CLICommandResponse
          - Parse command
            Collaborators: Command String, Command Verb, Params
          - Route to bot domain methods
            Collaborators: Bot, Command Verb, Params, BotResult
          - Serializes via channel adapter
            Collaborators: ChannelAdapter, String
          - Displays serialized output
            Collaborators: Stdout

      - **ChannelAdapter (Abstract)**
        Module: `cli`
        Responsibilities:
          - Serialize domain object to format
            Collaborators: Domain Object, Format
          - Deserialize format to domain object
            Collaborators: Format, Domain Object

      - **TextAdapter**
        Module: `cli`
        Responsibilities:
          - Parse command text
            Collaborators: Text String, Command, Params
        Inherits from: ChannelAdapter (Abstract)

      - **TTYAdapter**
        Module: `cli`
        Responsibilities:
          - Serialize to TTY text
            Collaborators: Domain Object, String
          - Deserialize TTY text
            Collaborators: String, Domain Object
          - Add color
            Collaborators: Text, Color
          - Format indentation
            Collaborators: Indent Level, Spaces
        Inherits from: TextAdapter (Abstract)

      - **TTYProgressAdapter**
        Module: `cli`
        Responsibilities:
          - Format line with marker
            Collaborators: Marker, Text, Indent
          - Render marker
            Collaborators: Is Completed, Is Current
        Inherits from: TTYAdapter (Abstract)

      - **JSONAdapter**
        Module: `cli`
        Responsibilities:
          - Serialize to JSON dict
            Collaborators: Dict
          - Deserialize JSON dict
            Collaborators: Dict, Domain Object
          - Convert to JSON string
            Collaborators: Dict, String
          - Parse JSON string
            Collaborators: String, Dict
          - Validate JSON structure
            Collaborators: Dict, Schema
        Inherits from: ChannelAdapter (Abstract)

      - **JSONProgressAdapter**
        Module: `cli`
        Responsibilities:
          - Include progress fields
            Collaborators: Is Completed, Is Current
          - Include completion markers
            Collaborators: Progress String
        Inherits from: JSONAdapter (Abstract)

      - **MarkdownAdapter**
        Module: `cli`
        Responsibilities:
          - Serialize to Markdown
            Collaborators: String
          - Deserialize Markdown
            Collaborators: String, Domain Object
          - Parse markdown sections
            Collaborators: Markdown, Sections
          - Format header
            Collaborators: Level, Text
          - Format list item
            Collaborators: Marker, Text, Indent
          - Format code block
            Collaborators: Language, Content
        Inherits from: TextAdapter (Abstract)

      - **MarkdownProgressAdapter**
        Module: `cli`
        Responsibilities:
          - Render progress marker
            Collaborators: Is Completed, Is Current, Marker String
          - Format progress line
            Collaborators: Name, Is Completed, Is Current, String
        Inherits from: MarkdownAdapter (Abstract)

      - **DotNotationParser**
        Module: `story_graph.story_map`
        Responsibilities:
          - Parses dot notation to node path
            Collaborators: Dot Notation String, Path Segments
          - Resolves node from path
            Collaborators: StoryGraph, Path Segments, StoryNode
          - Formats navigation error with valid paths
            Collaborators: Error Message, Valid Paths List
        Instantiated with: StoryGraph

      - **FileModificationMonitor**
        Module: `story_graph.story_map`
        Responsibilities:
          - Detects file modification
            Collaborators: File System, Last Modified Timestamp
          - Delegates reload to StoryGraph
            Collaborators: StoryGraph, File Path
          - Triggers panel refresh
            Collaborators: StoryMapView, DOM
          - Shows validation error notification
            Collaborators: Error Message, Panel Display
          - Retains previous valid graph on error
            Collaborators: Previous Graph, StoryGraph
        Instantiated with: File Path


### Render Bot Interface

    ## Domain Concepts (12 concepts)

      - **BotView**
        Module: `bot`
        Responsibilities:
          - Wraps bot JSON
            Collaborators: Bot JSON
          - Displays BotHeaderView
            Collaborators: BotHeaderView
          - Displays PathsSection
            Collaborators: PathsSection
          - Displays BehaviorsView
            Collaborators: BehaviorsView
          - Displays ScopeSection
            Collaborators: ScopeSection
          - Displays InstructionsSection
            Collaborators: InstructionsSection
        Inherits from: PanelView

      - **BotHeaderView**
        Module: `bot`
        Responsibilities:
          - Wraps bot JSON
            Collaborators: Bot JSON
          - Displays image
            Collaborators: Image
          - Displays title
            Collaborators: String, Bot JSON
          - Displays version number
            Collaborators: String, Bot JSON
          - Refreshes panel
            Collaborators: CLI
        Inherits from: PanelView

      - **PathsSection**
        Module: `bot`
        Responsibilities:
          - Wraps bot paths JSON
            Collaborators: BotPaths JSON
          - Displays bot directory
            Collaborators: String, BotPaths JSON
          - Edits workspace directory
            Collaborators: CLI, BotPaths JSON
          - Displays available bots
            Collaborators: AvailableBotsView
        Inherits from: SectionView

      - **AvailableBotsView**
        Module: `bot`
        Responsibilities:
          - Wraps bot registry JSON
            Collaborators: BotRegistry JSON
          - Displays available bots
            Collaborators: List, BotRegistry JSON
          - Selects bot
            Collaborators: CLI, Bot
        Inherits from: PanelView

      - **BehaviorsView**
        Module: `behaviors`
        Responsibilities:
          - Wraps behaviors JSON
            Collaborators: Behaviors JSON
          - Displays behavior names list
            Collaborators: List, Behavior JSON
          - Navigates to behavior
            Collaborators: CLI, Behavior
          - Toggles collapsed
            Collaborators: State, Behavior JSON
          - Displays tooltip
            Collaborators: String, Behavior JSON
          - Displays actions
            Collaborators: ActionsView
          - Executes behavior
            Collaborators: CLI, Behavior
          - Displays completion progress
            Collaborators: Status, Behavior JSON
          - Displays navigation
            Collaborators: NavigationView
        Inherits from: SectionView

      - **ActionsView**
        Module: `actions`
        Responsibilities:
          - Wraps actions JSON
            Collaborators: Actions JSON
          - Displays action names list
            Collaborators: List, Action JSON
          - Navigates to action
            Collaborators: CLI, Action
          - Displays status indicators
            Collaborators: Status, Action JSON
          - Executes action
            Collaborators: CLI, Action
          - Displays completion progress
            Collaborators: Progress, Action JSON
        Inherits from: PanelView

      - **PanelView (Base)**
        Module: `panel`
        Responsibilities:
          - Wraps JSON data
            Collaborators: JSON
          - Spawns subprocess
            Collaborators: CLI, Python Process
          - Sends command to CLI
            Collaborators: Command, Stdin
          - Receives JSON from CLI
            Collaborators: Stdout
          - Parses JSON
            Collaborators: String, Dict
          - Provides element ID
            Collaborators: String
          - Renders to HTML
            Collaborators: HTML, JSON

      - **SectionView**
        Module: `panel`
        Responsibilities:
          - Renders section header
            Collaborators: PanelHeader
          - Toggles collapsed state
            Collaborators: State
          - May contain subsections
            Collaborators: SubSectionView
        Inherits from: PanelView (Base)

      - **SubSectionView**
        Module: `panel`
        Responsibilities:
          - Toggles collapsed state
            Collaborators: State
        Inherits from: PanelView

      - **PanelHeader**
        Module: `panel`
        Responsibilities:
          - Displays header image
            Collaborators: Image
          - Displays title
            Collaborators: String

      - **ValidationMessageDisplay**
        Module: `story_graph.nodes`
        Responsibilities:
          - Shows warning message
            Collaborators: Message Text, DOM Element
          - Hides message
            Collaborators: DOM Element
          - Applies message styling
            Collaborators: CSS Class, Message Type

      - **ConfirmationDialog**
        Module: `panel`
        Responsibilities:
          - Shows confirmation inline
            Collaborators: Message, DOM Element
          - Shows confirm and cancel buttons
            Collaborators: Button Set
          - Invokes callback on confirm
            Collaborators: Callback Function
          - Hides confirmation on cancel
            Collaborators: DOM Element
        Instantiated with: Message, Callback


### Set Workspace


## Work With Story Map


### Scope Files


#### Set File Filter


#### Filter File Scope


### Scope Stories


#### Filter Scope of Stories


#### Manage Story Scope

      ## Domain Concepts (5 concepts)

        - **Scope**
          Module: `scope`
          Responsibilities:
            - Get filter
              Collaborators: String (read/write property)
            - Set filter
              Collaborators: String
            - Get results
              Collaborators: List (read-only property)
            - Apply filter to behaviors
              Collaborators: Behaviors, Filtered Behaviors
            - Apply filter to stories
              Collaborators: Stories, Filtered Stories
            - Clear filter
            - Get filter count
              Collaborators: Integer
            - Get is active
              Collaborators: Boolean

        - **TTYScope**
          Module: `scope`
          Responsibilities:
            - Serialize scope to TTY
              Collaborators: Scope, TTY String
            - Format filter display
              Collaborators: Filter String, TTY String
            - Format results list
              Collaborators: Results, TTY String
            - Format filter status
              Collaborators: Is Active, Count, TTY String
            - Wraps domain scope
              Collaborators: Scope
          Inherits from: TTYAdapter

        - **JSONScope**
          Module: `scope`
          Responsibilities:
            - Serialize scope to JSON
              Collaborators: Scope, JSON String
            - Include filter
              Collaborators: Filter String, String
            - Include results
              Collaborators: Results List, Array
            - Include filter metadata
              Collaborators: Is Active, Count, JSON
            - Wraps domain scope
              Collaborators: Scope
          Inherits from: JSONAdapter

        - **MarkdownScope**
          Module: `scope`
          Responsibilities:
            - Serialize scope to Markdown
              Collaborators: Scope, Markdown String
            - Format filter section
              Collaborators: Filter String, Markdown String
            - Format results list
              Collaborators: Results, Markdown List
            - Format filter documentation
              Collaborators: Scope, Markdown String
            - Wraps domain scope
              Collaborators: Scope
          Inherits from: MarkdownAdapter

        - **ScopeView**
          Module: `scope`
          Responsibilities:
            - Wraps scope JSON
              Collaborators: Scope JSON
            - Displays current filter
              Collaborators: String, Scope JSON
            - Edits filter
              Collaborators: CLI, Scope JSON
            - Displays filtered results
              Collaborators: List, Scope JSON
            - Clears filter
              Collaborators: CLI, Scope JSON
            - Displays filter status
              Collaborators: Is Active, Count, Scope JSON
          Inherits from: SectionView


#### Set Scope Using Filter Parts


### Edit Story Map

    ## Domain Concepts (61 concepts)

      - **StoryNode (Base)**
        Module: `story_graph.nodes`
        Responsibilities:
          - Serializes
            Collaborators: StoryNodeSerializer
          - Get/Update name
            Collaborators: String
          - Get node type
            Collaborators: String
          - Get node ID
            Collaborators: String, StoryNode, StoryNodeNavigator
          - Get parent
            Collaborators: StoryNode
          - Get sequential order
            Collaborators: StoryNodeNavigator, Float
          - Contains Children
            Collaborators: StoryNodeChildren
          - Delete self
            Collaborators: StoryNodeSerializer
          - Delete with children
            Collaborators: StoryNodeSerializer, StoryNodeChildren
          - Get/Update test
            Collaborators: Test

      - **StoryNodeChildren**
        Module: `story_graph.nodes`
        Responsibilities:
          - Get children
            Collaborators: List[StoryNode]
          - Find child by name
            Collaborators: String, StoryNode
          - Delete child
            Collaborators: StoryNode

      - **StoryNodeNavigator**
        Module: `story_graph.nodes`
        Responsibilities:
          - Build node ID from hierarchy path
            Collaborators: String, StoryNode
          - Get parent
            Collaborators: StoryNode
          - Move to parent
            Collaborators: New Parent, Position
          - Move after
            Collaborators: StoryNode, sequential order
          - Move before
            Collaborators: StoryNode, sequential order
          - DetermineOrder
            Collaborators: FLoat, StoryNode

      - **StoryNodeSerializer**
        Module: `story_graph.nodes`
        Responsibilities:
          - File
            Collaborators: File
          - Create Node
            Collaborators: File, StoryNode
          - Load Node
            Collaborators: File, StoryNode
          - Update Node
            Collaborators: File, StoryNode
          - Delete Node
            Collaborators: File, StoryNode
          - From JSON
            Collaborators: JSON, StoryNode
          - To JSON
            Collaborators: JSON, StoryNode

      - **TTYStoryNode**
        Module: `story_graph.nodes`
        Responsibilities:
          - Serialize node to TTY
            Collaborators: StoryNode, TTY String
          - Format name
            Collaborators: String, TTY String
          - Format sequential order
            Collaborators: Float, TTY String
          - Format children
            Collaborators: List[StoryNode], TTY String
          - Add child
            Collaborators: StoryNode, CLI Result
          - Add child at position
            Collaborators: StoryNode, Position, CLI Result
          - Delete child
            Collaborators: StoryNode, CLI Result
          - Delete this node
            Collaborators: CLI Result
          - Delete with children
            Collaborators: CLI Result
          - Update name
            Collaborators: String, CLI Result
          - Move to parent
            Collaborators: New Parent, Position, CLI Result
          - Move after target
            Collaborators: Target StoryNode, CLI Result
          - Move before target
            Collaborators: Target StoryNode, CLI Result
          - Reorder children
            Collaborators: Start Pos, End Pos, CLI Result
          - Automatically refresh story graph
            Collaborators: CLI Result
          - Wraps domain story node
            Collaborators: StoryNode
        Inherits from: TTYAdapter (Base)

      - **JSONStoryNode**
        Module: `story_graph.nodes`
        Responsibilities:
          - Serialize node to JSON
            Collaborators: StoryNode, JSON String
          - Include name
            Collaborators: String, JSON
          - Include sequential order
            Collaborators: Float, JSON
          - Include children
            Collaborators: List[StoryNode], JSON Array
          - Add child
            Collaborators: StoryNode, JSON Result
          - Add child at position
            Collaborators: StoryNode, Position, JSON Result
          - Delete child
            Collaborators: StoryNode, JSON Result
          - Delete this node
            Collaborators: JSON Result
          - Delete with children
            Collaborators: JSON Result
          - Update name
            Collaborators: String, JSON Result
          - Move to parent
            Collaborators: New Parent, Position, JSON Result
          - Move after target
            Collaborators: Target StoryNode, JSON Result
          - Move before target
            Collaborators: Target StoryNode, JSON Result
          - Reorder children
            Collaborators: Start Pos, End Pos, JSON Result
          - Automatically refresh story graph
            Collaborators: JSON Result
          - Wraps domain story node
            Collaborators: StoryNode
        Inherits from: JSONAdapter (Base)

      - **MarkdownStoryNode**
        Module: `story_graph.nodes`
        Responsibilities:
          - Serialize node to Markdown
            Collaborators: StoryNode, Markdown String
          - Format node header
            Collaborators: String, Sequential Order, Markdown
          - Format children list
            Collaborators: List[StoryNode], Markdown
          - Wraps domain story node
            Collaborators: StoryNode
        Inherits from: MarkdownAdapter (Base)

      - **StoryNodeView**
        Module: `story_graph.nodes`
        Responsibilities:
          - Wraps story node JSON
            Collaborators: StoryNode JSON
          - Toggles collapsed
            Collaborators: State
          - Add child node
            Collaborators: StoryNode, Panel Result
          - Add child at position
            Collaborators: StoryNode, Position, Panel Result
          - Delete this node
            Collaborators: Panel Result
          - Delete with children
            Collaborators: Panel Result
          - Update node name
            Collaborators: String, Panel Result
          - Move to parent
            Collaborators: New Parent, Position, Panel Result
          - Move after target
            Collaborators: Target StoryNode, Panel Result
          - Move before target
            Collaborators: Target StoryNode, Panel Result
          - Drag and drop
            Collaborators: Drop Target, Position, Panel Result
          - Reorder children
            Collaborators: Start Pos, End Pos, Panel Result
          - Automatically refresh story graph
            Collaborators: Panel Result
        Inherits from: PanelView (Base)

      - **StoryMap**
        Module: `story_graph.story_map`
        Responsibilities:
          - Load from bot directory
            Collaborators: Bot, StoryMap
          - Load from story graph
            Collaborators: File Path, StoryMap
          - Walk nodes
            Collaborators: StoryNode, Iterator[StoryNode]
          - Get all stories
            Collaborators: List[Story]
          - Get all scenarios
            Collaborators: List[Scenario]
          - Get all domain concepts
            Collaborators: List[DomainConcept]
          - Find by name
            Collaborators: Name, StoryNode
          - Find node by path
            Collaborators: Path String, StoryNode
          - Get story graph dict
            Collaborators: Dict
          - Get epics
            Collaborators: List[Epic]
          - Save to story graph
            Collaborators: File Path
          - Reload from story graph
            Collaborators: File Path, StoryMap
          - Validate graph structure
            Collaborators: Validation Result

      - **TTYStoryMap**
        Module: `story_graph.story_map`
        Responsibilities:
          - Serialize story map to TTY
            Collaborators: StoryMap, TTY String
          - Format epics list
            Collaborators: List[Epic], TTY String
          - Format story hierarchy
            Collaborators: StoryMap, TTY String
          - Walk and format nodes
            Collaborators: StoryNode, TTY String
          - Wraps domain story map
            Collaborators: StoryMap
        Inherits from: TTYAdapter

      - **JSONStoryMap**
        Module: `story_graph.story_map`
        Responsibilities:
          - Serialize story map to JSON
            Collaborators: StoryMap, JSON String
          - Include story graph
            Collaborators: Dict, JSON
          - Include all epics
            Collaborators: List[Epic], JSON Array
          - Wraps domain story map
            Collaborators: StoryMap
        Inherits from: JSONAdapter

      - **MarkdownStoryMap**
        Module: `story_graph.story_map`
        Responsibilities:
          - Serialize story map to Markdown
            Collaborators: StoryMap, Markdown String
          - Format epic hierarchy
            Collaborators: List[Epic], Markdown
          - Format story index
            Collaborators: List[Story], Markdown
          - Wraps domain story map
            Collaborators: StoryMap
        Inherits from: MarkdownAdapter

      - **StoryMapView**
        Module: `story_graph.story_map`
        Responsibilities:
          - Wraps story map JSON
            Collaborators: StoryMap JSON
          - Renders story graph as tree hierarchy
            Collaborators: StoryNode, HTML
          - Displays epic hierarchy
            Collaborators: EpicView, Epic JSON
          - Shows context-appropriate action buttons
            Collaborators: StoryNode, ButtonSet
          - Refreshes tree display
            Collaborators: StoryGraph, DOM
          - Searches stories
            Collaborators: Filter, StoryGraph JSON
          - Opens story graph file
            Collaborators: CLI, File JSON
          - Opens story map file
            Collaborators: CLI, File JSON
          - Delegates to InlineNameEditor
            Collaborators: InlineNameEditor, StoryNode
          - Delegates to StoryNodeDragDropManager
            Collaborators: StoryNodeDragDropManager, StoryNode
        Inherits from: PanelView
        Instantiated with: StoryGraph, PanelView

      - **Epic**
        Module: `story_graph.epic`
        Responsibilities:
          - Test file property
            Collaborators: String
          - Get all stories
            Collaborators: List[Story]
          - Get domain concepts
            Collaborators: List[DomainConcept]
        Inherits from: StoryNode

      - **TTYEpic**
        Module: `story_graph.epic`
        Responsibilities:
          - Format domain concepts
            Collaborators: List[DomainConcept], TTY String
          - Wraps domain epic
            Collaborators: Epic
        Inherits from: TTYStoryNode

      - **JSONEpic**
        Module: `story_graph.epic`
        Responsibilities:
          - Include domain concepts
            Collaborators: List[DomainConcept], JSON Array
          - Wraps domain epic
            Collaborators: Epic
        Inherits from: JSONStoryNode

      - **MarkdownEpic**
        Module: `story_graph.epic`
        Responsibilities:
          - Format domain concepts table
            Collaborators: List[DomainConcept], Markdown
          - Wraps domain epic
            Collaborators: Epic
        Inherits from: MarkdownStoryNode

      - **EpicView**
        Module: `story_graph.epic`
        Responsibilities:
          - Wraps epic JSON
            Collaborators: Epic JSON
          - Displays epic name
            Collaborators: String, Epic JSON
          - Displays epic icon
            Collaborators: Image
          - Displays sub epics
            Collaborators: SubEpicView, SubEpic JSON
          - Opens epic folder
            Collaborators: CLI, Epic JSON
          - Opens epic test file
            Collaborators: CLI, Epic JSON
        Inherits from: StoryNodeView

      - **SubEpic**
        Module: `story_graph.sub_epic`
        Responsibilities:
          - Test file property
            Collaborators: String
        Inherits from: StoryNode

      - **SubEpicView**
        Module: `story_graph.sub_epic`
        Responsibilities:
          - Wraps sub epic JSON
            Collaborators: SubEpic JSON
          - Displays sub epic name
            Collaborators: String, SubEpic JSON
          - Displays sub epic icon
            Collaborators: Image
          - Displays nested sub epics
            Collaborators: SubEpicView, SubEpic JSON
          - Displays stories
            Collaborators: StoryView, Story JSON
          - Opens sub epic folder
            Collaborators: CLI, SubEpic JSON
          - Opens sub epic test file
            Collaborators: CLI, SubEpic JSON
        Inherits from: StoryNodeView

      - **StoryGroup**
        Module: `story_graph.story_group`
        Inherits from: StoryNode

      - **Story**
        Module: `story_graph.story`
        Responsibilities:
          - Test class property
            Collaborators: String
          - Get test class
            Collaborators: String
          - Get default test class
            Collaborators: String
          - Get story type
            Collaborators: String
          - Get users
            Collaborators: List[StoryUser]
          - Get scenarios
            Collaborators: List[Scenario]
          - Get scenario outlines
            Collaborators: List[ScenarioOutline]
          - Get acceptance criteria
            Collaborators: List[AcceptanceCriteria]
        Inherits from: StoryNode

      - **TTYStory**
        Module: `story_graph.story`
        Responsibilities:
          - Format users
            Collaborators: List[StoryUser], TTY String
          - Format test metadata
            Collaborators: Test File, Test Class, TTY String
          - Wraps domain story
            Collaborators: Story
        Inherits from: TTYStoryNode

      - **JSONStory**
        Module: `story_graph.story`
        Responsibilities:
          - Include users
            Collaborators: List[StoryUser], JSON Array
          - Include test metadata
            Collaborators: Test File, Test Class, JSON
          - Wraps domain story
            Collaborators: Story
        Inherits from: JSONStoryNode

      - **MarkdownStory**
        Module: `story_graph.story`
        Responsibilities:
          - Format story card
            Collaborators: Story, Markdown
          - Format users section
            Collaborators: List[StoryUser], Markdown
          - Wraps domain story
            Collaborators: Story
        Inherits from: MarkdownStoryNode

      - **StoryView**
        Module: `story_graph.story`
        Responsibilities:
          - Wraps story JSON
            Collaborators: Story JSON
          - Displays story name
            Collaborators: String, Story JSON
          - Displays story icon
            Collaborators: Image
          - Displays scenarios
            Collaborators: ScenarioView, Scenario JSON
          - Opens test at class
            Collaborators: CLI, Story JSON
        Inherits from: StoryNodeView

      - **Scenario**
        Module: `story_graph.scenario`
        Responsibilities:
          - Test method property
            Collaborators: String
          - Get test method
            Collaborators: String
          - Get default test method
            Collaborators: String
          - Get steps
            Collaborators: List[Step]
        Inherits from: StoryNode

      - **TTYScenario**
        Module: `story_graph.scenario`
        Responsibilities:
          - Format steps
            Collaborators: List[Step], TTY String
          - Format test method
            Collaborators: Test Method, TTY String
          - Wraps domain scenario
            Collaborators: Scenario
        Inherits from: TTYStoryNode

      - **JSONScenario**
        Module: `story_graph.scenario`
        Responsibilities:
          - Include steps
            Collaborators: List[Step], JSON Array
          - Include test method
            Collaborators: Test Method, JSON
          - Wraps domain scenario
            Collaborators: Scenario
        Inherits from: JSONStoryNode

      - **MarkdownScenario**
        Module: `story_graph.scenario`
        Responsibilities:
          - Format Gherkin scenario
            Collaborators: Scenario, Markdown
          - Format steps as Given/When/Then
            Collaborators: List[Step], Markdown
          - Wraps domain scenario
            Collaborators: Scenario
        Inherits from: MarkdownStoryNode

      - **ScenarioView**
        Module: `story_graph.scenario`
        Responsibilities:
          - Wraps scenario JSON
            Collaborators: Scenario JSON
          - Displays scenario name
            Collaborators: String, Scenario JSON
          - Displays scenario icon
            Collaborators: Image
          - Opens test at scenario
            Collaborators: CLI, Scenario JSON
        Inherits from: StoryNodeView

      - **ScenarioOutline**
        Module: `story_graph.scenario_outline`
        Responsibilities:
          - Test method property
            Collaborators: String
          - Get test method
            Collaborators: String
          - Get default test method
            Collaborators: String
          - Get examples
            Collaborators: List[Dict]
          - Get steps
            Collaborators: List[Step]
        Inherits from: StoryNode

      - **TTYScenarioOutline**
        Module: `story_graph.scenario_outline`
        Responsibilities:
          - Format steps
            Collaborators: List[Step], TTY String
          - Format examples
            Collaborators: List[Dict], TTY String
          - Format test method
            Collaborators: Test Method, TTY String
          - Wraps domain scenario outline
            Collaborators: ScenarioOutline
        Inherits from: TTYStoryNode

      - **JSONScenarioOutline**
        Module: `story_graph.scenario_outline`
        Responsibilities:
          - Include steps
            Collaborators: List[Step], JSON Array
          - Include examples
            Collaborators: List[Dict], JSON Array
          - Include test method
            Collaborators: Test Method, JSON
          - Wraps domain scenario outline
            Collaborators: ScenarioOutline
        Inherits from: JSONStoryNode

      - **MarkdownScenarioOutline**
        Module: `story_graph.scenario_outline`
        Responsibilities:
          - Format Gherkin scenario outline
            Collaborators: ScenarioOutline, Markdown
          - Format steps as Given/When/Then
            Collaborators: List[Step], Markdown
          - Format examples table
            Collaborators: List[Dict], Markdown
          - Wraps domain scenario outline
            Collaborators: ScenarioOutline
        Inherits from: MarkdownStoryNode

      - **ScenarioOutlineView**
        Module: `story_graph.scenario_outline`
        Responsibilities:
          - Wraps scenario outline JSON
            Collaborators: ScenarioOutline JSON
          - Displays scenario outline name
            Collaborators: String, ScenarioOutline JSON
          - Displays scenario outline icon
            Collaborators: Image
          - Displays examples table
            Collaborators: List[Dict], Table HTML
          - Opens test at scenario outline
            Collaborators: CLI, ScenarioOutline JSON
        Inherits from: StoryNodeView

      - **AcceptanceCriteria**
        Module: `story_graph.acceptance_criteria`
        Responsibilities:
          - Get steps
            Collaborators: List[Step]
        Inherits from: StoryNode

      - **TTYAcceptanceCriteria**
        Module: `story_graph.acceptance_criteria`
        Responsibilities:
          - Format steps
            Collaborators: List[Step], TTY String
          - Format criteria list
            Collaborators: List[Step], TTY String
          - Wraps domain acceptance criteria
            Collaborators: AcceptanceCriteria
        Inherits from: TTYStoryNode

      - **JSONAcceptanceCriteria**
        Module: `story_graph.acceptance_criteria`
        Responsibilities:
          - Include steps
            Collaborators: List[Step], JSON Array
          - Wraps domain acceptance criteria
            Collaborators: AcceptanceCriteria
        Inherits from: JSONStoryNode

      - **MarkdownAcceptanceCriteria**
        Module: `story_graph.acceptance_criteria`
        Responsibilities:
          - Format criteria as checklist
            Collaborators: List[Step], Markdown
          - Format steps list
            Collaborators: List[Step], Markdown
          - Wraps domain acceptance criteria
            Collaborators: AcceptanceCriteria
        Inherits from: MarkdownStoryNode

      - **AcceptanceCriteriaView**
        Module: `story_graph.acceptance_criteria`
        Responsibilities:
          - Wraps acceptance criteria JSON
            Collaborators: AcceptanceCriteria JSON
          - Displays criteria name
            Collaborators: String, AcceptanceCriteria JSON
          - Displays criteria icon
            Collaborators: Image
          - Displays steps as checklist
            Collaborators: List[Step], HTML
        Inherits from: StoryNodeView

      - **Step**
        Module: `story_graph.step`
        Responsibilities:
          - Get text
            Collaborators: String
        Inherits from: StoryNode

      - **TTYStep**
        Module: `story_graph.step`
        Responsibilities:
          - Format step text
            Collaborators: String, TTY String
          - Format step keyword
            Collaborators: String, TTY String
          - Wraps domain step
            Collaborators: Step
        Inherits from: TTYStoryNode

      - **JSONStep**
        Module: `story_graph.step`
        Responsibilities:
          - Include step text
            Collaborators: String, JSON
          - Wraps domain step
            Collaborators: Step
        Inherits from: JSONStoryNode

      - **MarkdownStep**
        Module: `story_graph.step`
        Responsibilities:
          - Format step as Gherkin
            Collaborators: Step, Markdown
          - Wraps domain step
            Collaborators: Step
        Inherits from: MarkdownStoryNode

      - **StepView**
        Module: `story_graph.step`
        Responsibilities:
          - Wraps step JSON
            Collaborators: Step JSON
          - Displays step text
            Collaborators: String, Step JSON
          - Displays step icon
            Collaborators: Image
        Inherits from: StoryNodeView

      - **Test**
        Module: `story_graph.test`
        Responsibilities:
          - Get test file
            Collaborators: String
          - Get test class
            Collaborators: String
          - Get test method
            Collaborators: String
          - Get default test class
            Collaborators: String
          - Get default test method
            Collaborators: String
          - Build from story node
            Collaborators: StoryNode, TestMetadata

      - **TTYTest**
        Module: `story_graph.test`
        Responsibilities:
          - Serialize test to TTY
            Collaborators: Test, TTY String
          - Format test file
            Collaborators: String, TTY String
          - Format test class
            Collaborators: String, TTY String
          - Format test method
            Collaborators: String, TTY String
          - Wraps domain test
            Collaborators: Test
        Inherits from: TTYAdapter

      - **JSONTest**
        Module: `story_graph.test`
        Responsibilities:
          - Serialize test to JSON
            Collaborators: Test, JSON String
          - Include test file
            Collaborators: String, JSON
          - Include test class
            Collaborators: String, JSON
          - Include test method
            Collaborators: String, JSON
          - Wraps domain test
            Collaborators: Test
        Inherits from: JSONAdapter

      - **MarkdownTest**
        Module: `story_graph.test`
        Responsibilities:
          - Serialize test to Markdown
            Collaborators: Test, Markdown String
          - Format test link
            Collaborators: Test File, Test Class, Test Method, Markdown
          - Wraps domain test
            Collaborators: Test
        Inherits from: MarkdownAdapter

      - **TestView**
        Module: `story_graph.test`
        Responsibilities:
          - Wraps test JSON
            Collaborators: Test JSON
          - Displays test file
            Collaborators: String, Test JSON
          - Displays test class
            Collaborators: String, Test JSON
          - Displays test method
            Collaborators: String, Test JSON
          - Opens test file
            Collaborators: CLI, Test JSON
          - Opens test at class
            Collaborators: CLI, Test JSON
          - Opens test at method
            Collaborators: CLI, Test JSON
        Inherits from: PanelView

      - **StoryUser**
        Module: `story_graph.story_user`
        Responsibilities:
          - Get name
            Collaborators: String
          - From string
            Collaborators: String, StoryUser
          - From list
            Collaborators: List[String], List[StoryUser]
          - To string
            Collaborators: String

      - **TTYStoryUser**
        Module: `story_graph.story_user`
        Responsibilities:
          - Serialize user to TTY
            Collaborators: StoryUser, TTY String
          - Format user name
            Collaborators: String, TTY String
          - Format user list
            Collaborators: List[StoryUser], TTY String
          - Wraps domain story user
            Collaborators: StoryUser
        Inherits from: TTYAdapter

      - **JSONStoryUser**
        Module: `story_graph.story_user`
        Responsibilities:
          - Serialize user to JSON
            Collaborators: StoryUser, JSON String
          - Include user name
            Collaborators: String, JSON
          - Include user list
            Collaborators: List[StoryUser], JSON Array
          - Wraps domain story user
            Collaborators: StoryUser
        Inherits from: JSONAdapter

      - **MarkdownStoryUser**
        Module: `story_graph.story_user`
        Responsibilities:
          - Serialize user to Markdown
            Collaborators: StoryUser, Markdown String
          - Format user badge
            Collaborators: StoryUser, Markdown
          - Format user list
            Collaborators: List[StoryUser], Markdown
          - Wraps domain story user
            Collaborators: StoryUser
        Inherits from: MarkdownAdapter

      - **StoryUserView**
        Module: `story_graph.story_user`
        Responsibilities:
          - Wraps story user JSON
            Collaborators: StoryUser JSON
          - Displays user name
            Collaborators: String, StoryUser JSON
          - Displays user icon
            Collaborators: Image
          - Filters stories by user
            Collaborators: StoryUser, Panel Result
        Inherits from: PanelView

      - **StoryNode (Base)**
        Module: `story_graph.nodes`
        Responsibilities:
          - Execute action scoped to node: Action, Parameters
            Collaborators: Bot
          - Create child node with name and position
            Collaborators: StoryNodeChildren, NodeValidator
          - Delete self and handle children
            Collaborators: Parent, StoryNodeChildren
          - Validate child name unique among siblings
            Collaborators: StoryNodeChildren
          - Adjust position to valid range
            Collaborators: StoryNodeChildren
          - Resequence children after insert or delete
            Collaborators: StoryNodeChildren
        Realization:
          - Scope: Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph.Create Child Story Node.Create child node with specified position
            Scenario: Parent node creates new child at specific position, shifting existing children and maintaining sequential order
            Walks:
              - Steps 1-2 (Initialize parent, validate position)
                Object Flow:
                  parent_node: Epic = StoryGraph.get_epic(name: 'User Management')
                  existing_children: ['SubEpic A', 'SubEpic B'] = parent_node.get_children()
                  target_position: 1 = request.position
                  is_valid: True = parent_node.validate_position(position: 1, child_count: 2)
                    -> max_position: 2 = StoryNodeChildren.get_max_position(children: ['SubEpic A', 'SubEpic B'])
                    -> is_in_range: True = (position: 1 <= max_position: 2)
                       return is_in_range: True
                  return is_valid: True
              - Step 3 (Create child and insert at position)
                Object Flow:
                  new_child: SubEpic = parent_node.create_child(name: 'SubEpic C', position: 1)
                    -> is_duplicate: False = parent_node.validate_child_name_unique(name: 'SubEpic C')
                       -> existing_names: ['SubEpic A', 'SubEpic B'] = StoryNodeChildren.get_child_names()
                       -> is_unique: True = ('SubEpic C' not in existing_names)
                          return is_unique: True
                       return is_duplicate: False
                    -> child: SubEpic = SubEpic.create(name: 'SubEpic C', parent: Epic)
                    -> parent_node.resequence_children(insert_at: 1, new_child: child)
                       -> children_to_shift: ['SubEpic B'] = StoryNodeChildren.get_children_from_position(position: 1)
                       -> StoryNodeChildren.shift_positions(children: ['SubEpic B'], offset: 1)
                          SubEpic B.position = 1 + 1 = 2
                       -> StoryNodeChildren.insert(child: SubEpic C, position: 1)
                          SubEpic C.position = 1
                    -> final_order: ['SubEpic A', 'SubEpic C', 'SubEpic B'] = parent_node.get_children()
                       return final_order
                  return new_child: SubEpic
            Model Updates:
              - Added 'Create child node with name and position' responsibility to StoryNode
              - Added 'Validate child name unique among siblings' responsibility to StoryNode
              - Added 'Adjust position to valid range' responsibility to StoryNode
              - Added 'Resequence children after insert or delete' responsibility to StoryNode
              - Added NodeValidator as collaborator for validation operations
              - Added Parent as collaborator for delete operations
          - Scope: Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph.Delete Story Node.Delete node including children (cascade delete)
            Scenario: Node with descendants is deleted using cascade option, removing entire subtree and resequencing siblings
            Walks:
              - Steps 1-3 (Locate node, count descendants, initiate cascade delete)
                Object Flow:
                  parent_node: Epic = StoryGraph.get_epic(name: 'User Management')
                  target_node: SubEpic = parent_node.get_child(name: 'SubEpic B')
                  child_count: 2 = target_node.count_children()
                    -> direct_children: ['Story A', 'Story B'] = StoryNodeChildren.get_children()
                       return len(direct_children): 2
                  total_descendants: 5 = target_node.count_all_descendants()
                    -> count: 2 = child_count
                    -> for each child in direct_children:
                       -> child_descendants: 3 = child.count_all_descendants()
                          count = count + 1 + child_descendants = 2 + 1 + 2 = 5
                       return count: 5
                  cascade_flag: True = request.cascade
                  return {node: target_node, descendants: 5, cascade: True}
              - Steps 4-5 (Recursively delete descendants, remove from parent)
                Object Flow:
                  target_node.delete(cascade: True)
                    -> target_node.delete_all_descendants()
                       -> children: ['Story A', 'Story B'] = target_node.get_children()
                       -> for each child in children:
                          -> child.delete(cascade: True)
                             -> nested_children = child.get_children()
                             -> for each nested in nested_children:
                                -> nested.delete(cascade: True)
                                   # Recursively deletes scenarios under stories
                             -> child.remove_from_parent()
                          # Stories A and B and their scenarios deleted
                    -> target_node.remove_from_parent()
                       -> parent: Epic = target_node.parent
                       -> position: 1 = target_node.position
                       -> parent.remove_child(child: target_node)
                          -> StoryNodeChildren.remove(child: target_node)
                          -> parent.resequence_children(deleted_position: 1)
                             -> siblings_after: ['SubEpic C', 'SubEpic D'] = StoryNodeChildren.get_children_from_position(position: 2)
                             -> StoryNodeChildren.shift_positions(children: siblings_after, offset: -1)
                                SubEpic C.position = 2 - 1 = 1
                                SubEpic D.position = 3 - 1 = 2
                             -> final_children: ['SubEpic A', 'SubEpic C', 'SubEpic D'] = parent.get_children()
                                return final_children
                  return deleted: True
            Model Updates:
              - Added 'Delete self and handle children' responsibility to StoryNode
              - Confirmed 'Resequence children after insert or delete' handles both insert and delete cases
              - Added recursive deletion pattern for cascade deletes

      - **SubEpic**
        Module: `story_graph.sub_epic`
        Responsibilities:
          - Validate cannot mix Sub-Epics and Stories
            Collaborators: StoryNodeChildren
          - Create StoryGroup when first Story added
            Collaborators: StoryGroup
          - Check child type compatibility before add
            Collaborators: StoryNodeChildren
        Realization:
          - Scope: Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph.Create Child Story Node.SubEpic with SubEpics cannot create Story child
            Scenario: SubEpic that already contains SubEpic children rejects attempt to add Story child, maintaining hierarchy rules
            Walks:
              - Steps 1-4 (Attempt Story creation, validate hierarchy, reject with error)
                Object Flow:
                  subepic_node: SubEpic = StoryGraph.get_subepic(name: 'User Management')
                  existing_subepic: SubEpic = subepic_node.get_child(name: 'Authentication')
                  requested_child_type: 'Story' = request.child_type
                  can_add: False = subepic_node.check_child_type_compatibility(child_type: 'Story')
                    -> has_subepics: True = subepic_node.has_children_of_type(type: 'SubEpic')
                       -> children: [Authentication] = StoryNodeChildren.get_children()
                       -> subepic_count: 1 = len([c for c in children if c.type == 'SubEpic'])
                       -> has_subepics: True = (subepic_count: 1 > 0)
                          return has_subepics: True
                    -> is_compatible: False = SubEpic.validate_cannot_mix_subepics_and_stories(has_subepics: True, adding_type: 'Story')
                       -> if has_subepics: True and adding_type: 'Story':
                          return is_compatible: False
                    return can_add: False
                  error: ValidationError = SubEpic.create_hierarchy_error(message: 'Cannot create Story under SubEpic with SubEpics')
                  return error: ValidationError
            Model Updates:
              - Added 'Create StoryGroup when first Story added' responsibility to SubEpic
              - Added 'Check child type compatibility before add' responsibility to SubEpic
              - Clarified that 'Validate cannot mix Sub-Epics and Stories' is used during create_child operations

      - **Story**
        Module: `story_graph.story`
        Responsibilities:
          - Maintain separate sequential ordering for scenarios and acceptance criteria
            Collaborators: StoryNodeChildren
          - Route child to correct collection by type
            Collaborators: ScenarioCollection, AcceptanceCriteriaCollection
        Realization:
          - Scope: Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph.Create Child Story Node.Story creates child and adds to correct collection
            Scenario: Story creates Scenario and AcceptanceCriteria children, routing each to separate collections with independent ordering
            Walks:
              - Steps 1-3 (Create Scenario child, route to scenarios collection)
                Object Flow:
                  story_node: Story = StoryGraph.get_story(name: 'Validate Password')
                  child_type: 'Scenario' = request.child_type
                  child_name: 'Valid Password Entered' = request.child_name
                  new_scenario: Scenario = story_node.create_child(name: child_name, type: child_type)
                    -> target_collection: 'scenarios' = story_node.route_child_to_correct_collection(child_type: 'Scenario')
                       -> if child_type in ['Scenario', 'ScenarioOutline']:
                          return collection: 'scenarios'
                       -> elif child_type == 'AcceptanceCriteria':
                          return collection: 'acceptance_criteria'
                    -> scenario: Scenario = Scenario.create(name: 'Valid Password Entered', parent: story_node)
                    -> position: 0 = ScenarioCollection.get_next_position()
                    -> ScenarioCollection.add(child: scenario, position: 0)
                       scenario.position = 0
                    -> scenarios: ['Valid Password Entered'] = ScenarioCollection.get_all()
                    -> acceptance_criteria: [] = AcceptanceCriteriaCollection.get_all()
                       # Verify scenario NOT added to acceptance_criteria collection
                       return {scenarios: scenarios, acceptance_criteria: acceptance_criteria}
                  return new_scenario: Scenario
              - Steps 4-6 (Create AcceptanceCriteria child, route to separate collection with independent ordering)
                Object Flow:
                  ac_child_type: 'AcceptanceCriteria' = request.child_type
                  ac_name: 'Password Must Not Be Empty' = request.child_name
                  new_ac: AcceptanceCriteria = story_node.create_child(name: ac_name, type: ac_child_type)
                    -> target_collection: 'acceptance_criteria' = story_node.route_child_to_correct_collection(child_type: 'AcceptanceCriteria')
                       return collection: 'acceptance_criteria'
                    -> ac: AcceptanceCriteria = AcceptanceCriteria.create(name: 'Password Must Not Be Empty', parent: story_node)
                    -> ac_position: 0 = AcceptanceCriteriaCollection.get_next_position()
                       # Independent ordering from scenarios - both start at 0
                    -> AcceptanceCriteriaCollection.add(child: ac, position: 0)
                       ac.position = 0
                    -> scenarios: ['Valid Password Entered'] = ScenarioCollection.get_all()
                       # Verify AC NOT added to scenarios collection
                    -> acceptance_criteria: ['Password Must Not Be Empty'] = AcceptanceCriteriaCollection.get_all()
                       return {scenarios: scenarios, acceptance_criteria: acceptance_criteria}
                  return new_ac: AcceptanceCriteria
            Model Updates:
              - Added 'Route child to correct collection by type' responsibility to Story
              - Added ScenarioCollection and AcceptanceCriteriaCollection as collaborators
              - Clarified that 'Maintain separate sequential ordering' means independent position counters per collection

      - **InlineNameEditor**
        Module: `story_graph.nodes`
        Responsibilities:
          - Enables inline editing mode
            Collaborators: DOM Element, Input Field
          - Validates name in real-time
            Collaborators: StoryNode, Siblings Collection
          - Saves name on blur or Enter
            Collaborators: StoryNode, Event
          - Cancels on Escape
            Collaborators: Event, Original Value
          - Shows validation messages
            Collaborators: ValidationMessageDisplay, Message
        Instantiated with: StoryNode

      - **StoryNodeDragDropManager**
        Module: `story_graph.story_map`
        Responsibilities:
          - Shows drag cursor with icon
            Collaborators: Cursor Style, Node Icon
          - Validates drop target compatibility at UI level
            Collaborators: Source Node Type, Target Parent Type
          - Shows no-drop cursor for incompatible targets
            Collaborators: Cursor Style
          - Highlights valid drop target
            Collaborators: Target Element, CSS Class
          - Delegates move to StoryNode domain operation
            Collaborators: StoryNode, Target Parent, Position
          - Returns node to original on invalid drop
            Collaborators: Original Position, Animation
        Instantiated with: StoryGraph


### Edit Increments


### Act With Selected Node


## Navigate Behavior Actions


### Navigate Behavior And Actions

    ## Domain Concepts (9 concepts)

      - **NavigationView**
        Module: `behaviors`
        Responsibilities:
          - Wraps current action JSON
            Collaborators: Action JSON
          - Reruns action
            Collaborators: CLI, Action
          - Navigates to next action
            Collaborators: CLI, Action
          - Navigates to prev action
            Collaborators: CLI, Action
        Inherits from: PanelView

      - **NavigationResult**
        Module: `navigation`
        Responsibilities:
          - Get previous action
            Collaborators: Action
          - Get next action
            Collaborators: Action
          - Get can navigate back
            Collaborators: Boolean
          - Get can navigate next
            Collaborators: Boolean
          - Get navigation path
            Collaborators: String

      - **TTYNavigation**
        Module: `navigation`
        Responsibilities:
          - Serialize navigation to TTY
            Collaborators: NavigationResult, TTY String
          - Format navigation options
            Collaborators: Can Back, Can Next, TTY String
          - Format navigation path
            Collaborators: Path String, TTY String
          - Wraps domain navigation
            Collaborators: NavigationResult
        Inherits from: TTYAdapter

      - **JSONNavigation**
        Module: `navigation`
        Responsibilities:
          - Serialize navigation to JSON
            Collaborators: NavigationResult, JSON String
          - Include previous action
            Collaborators: Action, JSON
          - Include next action
            Collaborators: Action, JSON
          - Include navigation state
            Collaborators: Can Back, Can Next, JSON
          - Wraps domain navigation
            Collaborators: NavigationResult
        Inherits from: JSONAdapter

      - **MarkdownNavigation**
        Module: `navigation`
        Responsibilities:
          - Serialize navigation to Markdown
            Collaborators: NavigationResult, Markdown String
          - Format navigation section
            Collaborators: NavigationResult, Markdown String
          - Wraps domain navigation
            Collaborators: NavigationResult
        Inherits from: MarkdownAdapter

      - **BotPath**
        Module: `bot_path`
        Responsibilities:
          - Get bot directory
            Collaborators: Path
          - Get workspace directory
            Collaborators: Path
          - Get behaviors directory
            Collaborators: Path
          - Get config path
            Collaborators: Path
          - Get all paths
            Collaborators: Dict

      - **TTYBotPath**
        Module: `bot_path`
        Responsibilities:
          - Serialize bot path to TTY
            Collaborators: BotPath, TTY String
          - Format path display
            Collaborators: Path Name, Path Value, TTY String
          - Format all paths
            Collaborators: BotPath, TTY String
          - Wraps domain bot path
            Collaborators: BotPath
        Inherits from: TTYAdapter

      - **JSONBotPath**
        Module: `bot_path`
        Responsibilities:
          - Serialize bot path to JSON
            Collaborators: BotPath, JSON String
          - Include all paths
            Collaborators: Dict, JSON
          - Wraps domain bot path
            Collaborators: BotPath
        Inherits from: JSONAdapter

      - **MarkdownBotPath**
        Module: `bot_path`
        Responsibilities:
          - Serialize bot path to Markdown
            Collaborators: BotPath, Markdown String
          - Format paths section
            Collaborators: BotPath, Markdown String
          - Wraps domain bot path
            Collaborators: BotPath
        Inherits from: MarkdownAdapter


### Perform Behavior Action In Bot Workflow

    ## Domain Concepts (6 concepts)

      - **Base Action**
        Module: `actions`
        Responsibilities:
          - Inject Instructions
            Collaborators: Behavior
          - Load Relevant Content + Inject Into Instructions
            Collaborators: Content
          - Save content changes
            Collaborators: Content

      - **Base Action**
        Module: `actions`
        Responsibilities:
          - Inject Instructions
            Collaborators: Behavior
          - Load Relevant Content + Inject Into Instructions
            Collaborators: Content
          - Save content changes
            Collaborators: Content

      - **ActionStateManager**
        Module: `actions`
        Responsibilities:
          - Get state file path
            Collaborators: Path
          - Load or create state
            Collaborators: State File, Dict
          - Save state
            Collaborators: Action, State File
          - Load state
            Collaborators: Actions List, Current Index
          - Find action index
            Collaborators: Actions List, Action Name, Integer
          - Filter completed actions
            Collaborators: Completed Actions, Target Index, Actions List, List

      - **TTYAction**
        Module: `actions`
        Responsibilities:
          - Serialize action to TTY
            Collaborators: Action, String
          - Format action line
            Collaborators: Action Name, Marker, Indent
          - Wraps domain action
            Collaborators: Action
        Inherits from: TTYProgressAdapter

      - **JSONAction**
        Module: `actions`
        Responsibilities:
          - Serialize action to JSON dict
            Collaborators: Action, Dict
          - Include action metadata
            Collaborators: Name, Description, Status
          - Wraps domain action
            Collaborators: Action
        Inherits from: JSONProgressAdapter

      - **MarkdownAction**
        Module: `actions`
        Responsibilities:
          - Serialize action to Markdown
            Collaborators: Action, String
          - Format action documentation
            Collaborators: Action Name, Description, Subsection
          - Wraps domain action
            Collaborators: Action
        Inherits from: MarkdownProgressAdapter


### Display Behavior Action State


## Perform Action


### Prepare Common Instructions For Behavior, Action, and Scope

    ## Domain Concepts (7 concepts)

      - **ActionDataSubSection**
        Module: `actions`
        Responsibilities:
          - Wraps action JSON
            Collaborators: Action JSON
          - Displays action properties
            Collaborators: Object, Action JSON
        Inherits from: SubSectionView

      - **TTYInstructions**
        Module: `instructions`
        Responsibilities:
          - Serialize instructions to TTY
            Collaborators: Instructions, String
          - Format instruction sections
            Collaborators: Sections, String
          - Wraps domain instructions
            Collaborators: Instructions
        Inherits from: TTYAdapter

      - **JSONInstructions**
        Module: `instructions`
        Responsibilities:
          - Serialize instructions to JSON
            Collaborators: Instructions, Dict
          - Include instruction sections
            Collaborators: Sections, Array
          - Wraps domain instructions
            Collaborators: Instructions
        Inherits from: JSONAdapter

      - **MarkdownInstructions**
        Module: `instructions`
        Responsibilities:
          - Serialize instructions to Markdown
            Collaborators: Instructions, String
          - Format instruction sections
            Collaborators: Sections, Markdown
          - Wraps domain instructions
            Collaborators: Instructions
        Inherits from: MarkdownAdapter

      - **InstructionsSection**
        Module: `instructions`
        Responsibilities:
          - Wraps instructions JSON
            Collaborators: Instructions JSON
          - Wraps action JSON
            Collaborators: Action JSON
          - Displays base instructions subsection
            Collaborators: BaseInstructionsSubSection
          - Displays raw format subsection
            Collaborators: RawFormatSubSection
          - Submits to AI chat
            Collaborators: CLI, Instructions JSON
        Inherits from: SectionView (Base)

      - **BaseInstructionsSubSection**
        Module: `instructions`
        Responsibilities:
          - Wraps instructions JSON
            Collaborators: Instructions JSON
          - Displays behavior name
            Collaborators: String, Instructions JSON
          - Displays action name
            Collaborators: String, Instructions JSON
          - Displays  Instructions
            Collaborators: Instructions JSON
        Inherits from: SubSectionView

      - **RawFormatSubSection**
        Module: `instructions`
        Responsibilities:
          - Wraps instructions JSON
            Collaborators: Instructions JSON
          - Displays raw instructions
            Collaborators: String, Instructions JSON
        Inherits from: SubSectionView


### Clarify Requirements

    ## Domain Concepts (6 concepts)

      - **GatherContextAction**
        Module: `actions.clarify`
        Responsibilities:
          - Inject gather context instructions
            Collaborators: Behavior, Guardrails, Required Clarifications
          - Inject questions and evidence
            Collaborators: Behavior, Guardrails, Key Questions, Evidence

      - **TTYGatherContext**
        Module: `actions.clarify`
        Responsibilities:
          - Serialize clarify action to TTY
            Collaborators: GatherContextAction, TTY String
          - Format key questions
            Collaborators: Questions, Evidence, TTY String
          - Wraps domain action
            Collaborators: GatherContextAction
        Inherits from: TTYProgressAdapter

      - **JSONGatherContext**
        Module: `actions.clarify`
        Responsibilities:
          - Serialize clarify action to JSON
            Collaborators: GatherContextAction, JSON String
          - Include questions and evidence
            Collaborators: Questions, Evidence, JSON
          - Wraps domain action
            Collaborators: GatherContextAction
        Inherits from: JSONProgressAdapter

      - **MarkdownGatherContext**
        Module: `actions.clarify`
        Responsibilities:
          - Serialize clarify action to Markdown
            Collaborators: GatherContextAction, Markdown String
          - Format questions list
            Collaborators: Questions, Evidence, Markdown
          - Wraps domain action
            Collaborators: GatherContextAction
        Inherits from: MarkdownProgressAdapter

      - **ClarifyInstructionsSection**
        Module: `actions.clarify`
        Responsibilities:
          - Wraps clarify subsection
            Collaborators: ClarifyDataSubSection
        Inherits from: InstructionsSection

      - **ClarifyDataSubSection**
        Module: `actions.clarify`
        Responsibilities:
          - Wraps key questions JSON
            Collaborators: KeyQuestions JSON
          - Displays key questions
            Collaborators: List, KeyQuestion JSON
          - Updates evidence
            Collaborators: CLI, Evidence JSON
          - Edits answer
            Collaborators: CLI, KeyQuestion JSON
        Inherits from: SubSectionView


### Decide Strategy

    ## Domain Concepts (6 concepts)

      - **StrategyAction**
        Module: `actions.strategy`
        Responsibilities:
          - Inject Strategy instructions
            Collaborators: Behavior, Guardrails, Strategy
          - Inject decision criteria and assumptions
            Collaborators: Behavior, Guardrails, Decision Criteria, Assumptions, Recommended Human Activity

      - **TTYStrategy**
        Module: `actions.strategy`
        Responsibilities:
          - Serialize strategy action to TTY
            Collaborators: StrategyAction, TTY String
          - Format decision criteria
            Collaborators: Criteria, Assumptions, TTY String
          - Wraps domain action
            Collaborators: StrategyAction
        Inherits from: TTYProgressAdapter

      - **JSONStrategy**
        Module: `actions.strategy`
        Responsibilities:
          - Serialize strategy action to JSON
            Collaborators: StrategyAction, JSON String
          - Include criteria and assumptions
            Collaborators: Criteria, Assumptions, JSON
          - Wraps domain action
            Collaborators: StrategyAction
        Inherits from: JSONProgressAdapter

      - **MarkdownStrategy**
        Module: `actions.strategy`
        Responsibilities:
          - Serialize strategy action to Markdown
            Collaborators: StrategyAction, Markdown String
          - Format strategy documentation
            Collaborators: Criteria, Assumptions, Markdown
          - Wraps domain action
            Collaborators: StrategyAction
        Inherits from: MarkdownProgressAdapter

      - **StrategyInstructionsSection**
        Module: `actions.strategy`
        Responsibilities:
          - Wraps strategy subsection
            Collaborators: StrategyDataSubSection
        Inherits from: InstructionsSection

      - **StrategyDataSubSection**
        Module: `actions.strategy`
        Responsibilities:
          - Wraps strategy JSON
            Collaborators: Strategy JSON
          - Displays decision criteria
            Collaborators: List, DecisionCriteria JSON
          - Displays assumptions
            Collaborators: String, Assumptions JSON
          - Edits decision criterion
            Collaborators: CLI, DecisionCriterion JSON
          - Edits assumption
            Collaborators: CLI, Assumption JSON
        Inherits from: SubSectionView


### Build Story Graph

    ## Domain Concepts (6 concepts)

      - **BuildKnowledgeAction**
        Module: `actions.build`
        Responsibilities:
          - Inject knowledge graph template
            Collaborators: Behavior, Content, Knowledge Graph Spec, Knowledge Graph
          - Inject builder instructions
            Collaborators: Behavior, Content, Build Instructions
          - Save Knowledge graph
            Collaborators: Behavior, Content, Knowledge Graph

      - **TTYBuildKnowledge**
        Module: `actions.build`
        Responsibilities:
          - Serialize build action to TTY
            Collaborators: BuildKnowledgeAction, String
          - Format build status
            Collaborators: Status, TTY String
          - Wraps domain action
            Collaborators: BuildKnowledgeAction
        Inherits from: TTYProgressAdapter

      - **JSONBuildKnowledge**
        Module: `actions.build`
        Responsibilities:
          - Serialize build action to JSON
            Collaborators: BuildKnowledgeAction, JSON String
          - Include build metadata
            Collaborators: Knowledge Graph Spec, JSON
          - Wraps domain action
            Collaborators: BuildKnowledgeAction
        Inherits from: JSONProgressAdapter

      - **MarkdownBuildKnowledge**
        Module: `actions.build`
        Responsibilities:
          - Serialize build action to Markdown
            Collaborators: BuildKnowledgeAction, Markdown String
          - Format build documentation
            Collaborators: Knowledge Graph Spec, Markdown
          - Wraps domain action
            Collaborators: BuildKnowledgeAction
        Inherits from: MarkdownProgressAdapter

      - **BuildInstructionsSection**
        Module: `actions.build`
        Responsibilities:
          - Wraps build subsection
            Collaborators: BuildDataSubSection
        Inherits from: InstructionsSection

      - **BuildDataSubSection**
        Module: `actions.build`
        Responsibilities:
          - Wraps build JSON
            Collaborators: Build JSON
          - Displays knowledge graph spec
            Collaborators: Object, KnowledgeGraphSpec JSON
          - Displays graph structure
            Collaborators: Object, KnowledgeGraphSpec JSON
          - Displays builder instructions
            Collaborators: String, BuilderInstructions JSON
          - Opens graph file
            Collaborators: CLI, Path JSON
        Inherits from: SubSectionView


### Validate With Rules

    ## Domain Concepts (6 concepts)

      - **ValidateRulesAction**
        Module: `actions.validate`
        Responsibilities:
          - Inject common bot rules
            Collaborators: Base Bot, Rules, Common Rules
          - Inject behavior specific rules
            Collaborators: Behavior, Rules, Behavior Rules
          - Load + inject content for validation
            Collaborators: Behavior, Content, Knowledge Graph, Rendered Outputs

      - **TTYValidateRules**
        Module: `actions.validate`
        Responsibilities:
          - Serialize validate action to TTY
            Collaborators: ValidateRulesAction, TTY String
          - Format validation results
            Collaborators: Violations, TTY String
          - Wraps domain action
            Collaborators: ValidateRulesAction
        Inherits from: TTYProgressAdapter

      - **JSONValidateRules**
        Module: `actions.validate`
        Responsibilities:
          - Serialize validate action to JSON
            Collaborators: ValidateRulesAction, JSON String
          - Include violations and fixes
            Collaborators: Violations, Suggestions, JSON
          - Wraps domain action
            Collaborators: ValidateRulesAction
        Inherits from: JSONProgressAdapter

      - **MarkdownValidateRules**
        Module: `actions.validate`
        Responsibilities:
          - Serialize validate action to Markdown
            Collaborators: ValidateRulesAction, Markdown String
          - Format validation report
            Collaborators: Violations, Suggestions, Markdown
          - Wraps domain action
            Collaborators: ValidateRulesAction
        Inherits from: MarkdownProgressAdapter

      - **ValidateInstructionsSection**
        Module: `actions.validate`
        Responsibilities:
          - Wraps validate subsection
            Collaborators: ValidateDataSubSection
        Inherits from: InstructionsSection

      - **ValidateDataSubSection**
        Module: `actions.validate`
        Responsibilities:
          - Wraps validate JSON
            Collaborators: Validate JSON
          - Displays rules
            Collaborators: List, Rule JSON
          - Displays rule descriptions
            Collaborators: String, Rule JSON
          - Displays rule examples
            Collaborators: List, Rule JSON
          - Opens rule file
            Collaborators: CLI, Path JSON
        Inherits from: SubSectionView


### Render Content

    ## Domain Concepts (9 concepts)

      - **RenderOutputAction**
        Module: `actions.render`
        Responsibilities:
          - Inject render output instructions
            Collaborators: Behavior, Content, Render Spec, Renderer
          - Inject templates
            Collaborators: Behavior, Content, Render Spec, Template
          - Inject transformers
            Collaborators: Behavior, Content, Transformer
          - Load + inject structured content
            Collaborators: Behavior, Content, Knowledge Graph

      - **TTYRenderOutput**
        Module: `actions.render`
        Responsibilities:
          - Serialize render action to TTY
            Collaborators: RenderOutputAction, TTY String
          - Format render status
            Collaborators: Render Spec, TTY String
          - Wraps domain action
            Collaborators: RenderOutputAction
        Inherits from: TTYProgressAdapter

      - **JSONRenderOutput**
        Module: `actions.render`
        Responsibilities:
          - Serialize render action to JSON
            Collaborators: RenderOutputAction, JSON String
          - Include render spec
            Collaborators: Render Spec, Templates, JSON
          - Wraps domain action
            Collaborators: RenderOutputAction
        Inherits from: JSONProgressAdapter

      - **MarkdownRenderOutput**
        Module: `actions.render`
        Responsibilities:
          - Serialize render action to Markdown
            Collaborators: RenderOutputAction, Markdown String
          - Format render documentation
            Collaborators: Render Spec, Templates, Markdown
          - Wraps domain action
            Collaborators: RenderOutputAction
        Inherits from: MarkdownProgressAdapter

      - **Renderer**
        Module: `actions.render`
        Responsibilities:
          - Render complex output
            Collaborators: Template, Knowledge Graph, Transformer
          - Render outputs using components in context
            Collaborators: AI Chat, Template, Content

      - **Template**
        Module: `actions.render`
        Responsibilities:
          - Define output structure
            Collaborators: Placeholder
          - Transform content
            Collaborators: Transformer, Content
          - Load template
            Collaborators: Behavior, Content

      - **Content**
        Module: `actions.render`
        Responsibilities:
          - Render outputs
            Collaborators: Template, Renderer, Render Spec
          - Synchronize formats
            Collaborators: Synchronizer, Extractor, Synchronizer Spec
          - Save knowledge graph
            Collaborators: Knowledge Graph
          - Load rendered content
            Collaborators: na
          - Present rendered content
            Collaborators: na

      - **RenderInstructionsSection**
        Module: `actions.render`
        Responsibilities:
          - Wraps render subsection
            Collaborators: RenderDataSubSection
        Inherits from: InstructionsSection

      - **RenderDataSubSection**
        Module: `actions.render`
        Responsibilities:
          - Wraps render JSON
            Collaborators: Render JSON
          - Displays render spec
            Collaborators: Object, RenderSpec JSON
          - Displays templates
            Collaborators: List, Template JSON
          - Displays render instructions
            Collaborators: String, RenderInstructions JSON
          - Opens template file
            Collaborators: CLI, Path JSON
        Inherits from: SubSectionView


### Use Rules In Prompt

    ## Domain Concepts (2 concepts)

      - **Rule**
        Module: `behaviors`
        Responsibilities:
          - Validate content
            Collaborators: Knowledge Graph, Violations
          - Find behavior specific rules from context
            Collaborators: Behavior
          - Find common bot rules from context
            Collaborators: Base Bot
          - Load + inject diagnostics results
            Collaborators: AI Chat, Violations, Corrections
          - Suggest corrections
            Collaborators: Violations, Suggestions, Fixes
          - Provide examples - Do
            Collaborators: Example, Description
          - Provide examples - Dont
            Collaborators: Example, Description
          - Specialized examples
            Collaborators: Language, Framework, Pattern

      - **Guardrails**
        Module: `behaviors`
        Responsibilities:
          - Provide required context
            Collaborators: Key Questions, Evidence
          - Guide Strategy decisions
            Collaborators: Decision Criteria, Assumptions
          - Define recommended human activity
            Collaborators: Human, Instructions


### Synchronize Graph From Rendered


## Get Help

  ## Domain Concepts (11 concepts)

    - **TTYHelp**
      Module: `help`
      Responsibilities:
        - Serialize help to TTY
          Collaborators: Help, String
        - Format help sections
          Collaborators: Sections, String
        - Wraps domain help
          Collaborators: Help
      Inherits from: TTYAdapter

    - **JSONHelp**
      Module: `help`
      Responsibilities:
        - Serialize help to JSON
          Collaborators: Help, Dict
        - Include help sections
          Collaborators: Sections, Array
        - Wraps domain help
          Collaborators: Help
      Inherits from: JSONAdapter

    - **MarkdownHelp**
      Module: `help`
      Responsibilities:
        - Serialize help to Markdown
          Collaborators: Help, String
        - Format help sections
          Collaborators: Sections, Markdown
        - Wraps domain help
          Collaborators: Help
      Inherits from: MarkdownAdapter

    - **Status**
      Module: `help`
      Responsibilities:
        - Get progress path
          Collaborators: String
        - Get stage name
          Collaborators: String
        - Get current behavior name
          Collaborators: String
        - Get current action name
          Collaborators: String
        - Get has current behavior
          Collaborators: Boolean
        - Get has current action
          Collaborators: Boolean

    - **TTYStatus**
      Module: `help`
      Responsibilities:
        - Serialize status to TTY
          Collaborators: Status, TTY String
        - Format progress line
          Collaborators: Progress Path, Stage Name, TTY String
        - Format hierarchical status
          Collaborators: Bot, Status, TTY String
        - Wraps domain status
          Collaborators: Status
      Inherits from: TTYAdapter

    - **JSONStatus**
      Module: `help`
      Responsibilities:
        - Serialize status to JSON
          Collaborators: Status, JSON String
        - Include progress path
          Collaborators: Progress Path, String
        - Include stage name
          Collaborators: Stage Name, String
        - Include current behavior
          Collaborators: Behavior Name, String
        - Include current action
          Collaborators: Action Name, String
        - Wraps domain status
          Collaborators: Status
      Inherits from: JSONAdapter

    - **MarkdownStatus**
      Module: `help`
      Responsibilities:
        - Serialize status to Markdown
          Collaborators: Status, Markdown String
        - Format progress section
          Collaborators: Progress Path, Stage Name, Markdown String
        - Format workflow state
          Collaborators: Status, Markdown String
        - Wraps domain status
          Collaborators: Status
      Inherits from: MarkdownAdapter

    - **ExitResult**
      Module: `exit_result`
      Responsibilities:
        - Get exit code
          Collaborators: Integer
        - Get exit message
          Collaborators: String
        - Get should cleanup
          Collaborators: Boolean

    - **TTYExitResult**
      Module: `exit_result`
      Responsibilities:
        - Serialize exit result to TTY
          Collaborators: ExitResult, TTY String
        - Format exit message
          Collaborators: Message, TTY String
        - Wraps domain exit result
          Collaborators: ExitResult
      Inherits from: TTYAdapter

    - **JSONExitResult**
      Module: `exit_result`
      Responsibilities:
        - Serialize exit result to JSON
          Collaborators: ExitResult, JSON String
        - Include exit code
          Collaborators: Integer, JSON
        - Include exit message
          Collaborators: String, JSON
        - Wraps domain exit result
          Collaborators: ExitResult
      Inherits from: JSONAdapter

    - **MarkdownExitResult**
      Module: `exit_result`
      Responsibilities:
        - Serialize exit result to Markdown
          Collaborators: ExitResult, Markdown String
        - Format exit documentation
          Collaborators: ExitResult, Markdown String
        - Wraps domain exit result
          Collaborators: ExitResult
      Inherits from: MarkdownAdapter
