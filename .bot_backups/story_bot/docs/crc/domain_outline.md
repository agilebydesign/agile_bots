StoryBotMCPServer
    Bootstraps environment: BOT_DIRECTORY,WORKING_AREA,Bot Config
    Creates Bot instance: Bot,Bot Config,Bot Directory
    Creates FastMCP server: FastMCP,Server Name
    Registers bot tool: Bot,Current Behavior,Current Action
    Registers behavior tools: Bot,Behavior,Action,Tool Generator
    Registers utility tools: Working Directory Manager,Action State Manager,Server Restart Manager
    Delegates to Bot: Bot,Behavior,Action
    Runs MCP server: FastMCP,Event Loop
    Get bot_directory: Path
    Get workspace_directory: Path
    Get bot: Bot
    Get server: FastMCP

StoryBotCLI
    Bootstraps environment: BOT_DIRECTORY,WORKING_AREA,Bot Config
    Delegates to BaseBotCli: Base Bot CLI,Bot Name,Bot Config Path
    Executes CLI: Base Bot CLI,Command Arguments
    Get bot_directory: Path
    Get workspace_directory: Path
    Get bot_name: String
    Get bot_config_path: Path

BehaviorToolGenerator
    Generates behavior tool function: Behavior,Trigger Patterns
    Routes to behavior: Bot,Behavior Name
    Routes to action: Behavior,Action Name
    Executes action: Action,Parameters
    Returns result: Bot Result,Status,Data
    Handles missing action: Current Action,State
    Loads action state: Behavior,Action State
    Get tool_name: String
    Get tool_description: String
    Get trigger_patterns: List

WorkingDirectoryManager
    Gets working directory: Workspace Directory,WORKING_AREA
    Sets working directory: New Path,Persist Flag
    Validates path: Path
    Updates environment: WORKING_AREA,Environment Variables
    Updates bot config: Bot Config,Working Area,Persist Flag
    Persists to config: Bot Config File,JSON
    Returns previous directory: Previous Path,Workspace Directory
    Get working_directory: Path
    Get previous_directory: Path
    Get persisted: Boolean

ActionStateManager
    Closes current action: Current Action,Behavior,State File
    Loads action state: Behavior,Action State,State File
    Determines next action: Behavior,Action Names,Current Index
    Transitions to next action: Behavior,Current Action,Next Action
    Detects behavior completion: Current Action,Final Action,Behavior
    Transitions to next behavior: Bot,Next Behavior,First Action
    Returns transition result: Status,Completed Action,Next Action
    Handles out-of-order confirmation: Behavior,Confirmation,State File
    Validates human confirmation: Confirmed By,Timestamp
    Persists confirmation: State File,Confirmation Data,JSON
    Get state_file: Path
    Get current_action: Action
    Get next_action: Action
    Get behavior_complete: Boolean
    Get out_of_order_confirmations: Dict

ServerRestartManager
    Restarts MCP server: Workspace Root,Bot Name,Bot Location
    Terminates processes: Process List,Bot Name
    Clears cache: Python Cache,Module Cache
    Returns restart result: Status,Message
    Get workspace_root: Path
    Get bot_name: String
    Get bot_location: String

Synchronizer
    Synchronizes formats: Source Format,Target Format
    Extracts from source: Extractor,Source File
    Renders to target: Renderer,Target File
    Validates sync: Source,Target
    Get source_format: String
    Get target_format: String
    Get extractor: Extractor
    Get renderer: Renderer



DomainModelSynchronizer : Synchronizer
    Syncs CRC text with story graph: CRC Text,Story Graph,Domain Concepts
    Extracts domain concepts: CRC Parser,Concept Extractor
    Renders domain concepts: Concept Renderer,CRC Template
    Validates CRC format: CRC Validator
    Preserves module paths: Module Mapper,Code Structure
    Get crc_path: Path
    Get story_graph_path: Path
    Get domain_concepts: List


StoryIOSynchronizer : Synchronizer
    Syncs story graph with drawio: Story Graph,Drawio File
    Extracts stories from drawio: Drawio Parser,Story Components
    Renders stories to drawio: Story Renderer,Drawio Generator
    Manages story positions: Position Manager,Story Layout
    Updates increments: Increment Manager,Priority Data
    Validates story structure: Structure Validator
    Get story_graph_path: Path
    Get drawio_path: Path
    Get increments: List
    Get epics: List
    Get stories: List

StoryScenarioSynchronizer : Synchronizer
    Syncs scenario docs with graph: Scenario Files,Story Graph
    Extracts scenarios: Scenario Parser,Gherkin Parser
    Renders scenarios: Scenario Renderer,Template
    Validates scenario format: Scenario Validator
    Manages examples tables: Examples Parser,Test Data
    Get scenario_path: Path
    Get story_graph_path: Path
    Get scenarios: List

StoryTestsSynchronizer : Synchronizer
    Syncs test code with scenarios: Test Files,Scenario Files
    Extracts test cases: Test Parser,Test Extractor
    Renders test code: Test Renderer,Test Template
    Validates test structure: Test Validator
    Maps scenarios to tests: Scenario Mapper,Test Cases
    Get test_path: Path
    Get scenario_path: Path
    Get test_cases: List

StoryIONode
    Get children: StoryIONodes
    Calculates child count: StoryIONode
    Render: StoryIORenderer
    Validates structure: Validator
    Get sequential_order: Float
    Get name: String
    Get description: String
    Calculates position: Position Manager,Layout


StoryIOEpic : StoryIONode
    children: SubEpic List,Epic Context
    Render: StoryIORenderer
    Estimated Stories: Number, StoryIOStory
    Actual Stories: StoryIOStory

StoryIOSubEpic : StoryIONode
    children: Story List,SubEpic Context
    Render: StoryIORenderer

StoryIOStory : StoryIONode
    Children: StoryIOAcceptanceCriteria
    Render: StoryIORenderer
    Prioritized: Increment

StoryIOAcceptanceCriteria : StoryIONode
    Render: StoryIORenderer
    Get critera: String

StoryIOIncrement : StoryIONode
    Owns story assignments: Story List,Increment Context
    Manages priorities: Priority Order,Story Sequence
    Calculates capacity: Story Count,Capacity Limit
    Render: StoryIORenderer
    Get number: Integer
    Get stories: List
    Get capacity: Integer
    Get priority_order: List

StoryIOPosition
    Calculates position: X,Y,Grid Layout
    Validates bounds: Canvas Bounds
    Adjusts for overlap: Other Positions,Collision Detection
    Formats coordinates: X,Y,String Format
    Get x: Float
    Get y: Float
    Get width: Float
    Get height: Float

StoryIODiagram
    Owns diagram structure: Pages,Layers,Cells
    Manages XML structure: XML Tree,Drawio Schema
    Renders diagram: Diagram Renderer,XML Generator
    Validates diagram format: Diagram Validator
    Persists to file: File Writer,XML Formatter
    Get pages: List
    Get root_cell: Cell
    Get xml_tree: Element

StoryIORenderer
    Coordinates rendering: Epic,Feature,Story,Increment
    Calculates layout: Layout Manager,Position Calculator
    Formats XML: XML Formatter,Pretty Print
    Get cell_style: String
    Get layout_config: Dict
    Get xml_formatter: XMLFormatter

StoryMapDrawioSynchronizer : Synchronizer
    Syncs JSON to drawio: Story Graph,Drawio File,Direction
    Syncs drawio to JSON: Drawio File,Story Graph,Direction
    Extracts layout from drawio: Drawio Parser,Layout Extractor
    Merges layout with graph: Story Graph,Layout Data,Merger
    Validates sync consistency: Story Graph,Drawio
    Get story_graph_path: Path
    Get drawio_path: Path
    Get sync_direction: String

Instructions:
- Use clear, concise domain concepts and responsibilities.
- List each responsibility as: {responsibility}: {collaborator},{collaborator},...
- Only include meaningful relationships; avoid unnecessary boilerplate or filler.
- Ensure each domain concept is followed by its set of responsibilities.

