## Module: exit_result

ExitResult
    Get exit code: Integer  
    Get exit message: String  
    Get should cleanup: Boolean  

JSONExitResult
    Serialize exit result to JSON: ExitResult,JSON String  
    Include exit code: Integer,JSON  
    Include exit message: String,JSON  
    Wraps domain exit result: ExitResult  

MarkdownExitResult
    Serialize exit result to Markdown: ExitResult,Markdown String  
    Format exit documentation: ExitResult,Markdown String  
    Wraps domain exit result: ExitResult  

TTYExitResult
    Serialize exit result to TTY: ExitResult,TTY String  
    Format exit message: Message,TTY String  
    Wraps domain exit result: ExitResult  


## Module: help

JSONHelp
    Serialize help to JSON: Help,Dict  
    Include help sections: Sections,Array  
    Wraps domain help: Help  

JSONStatus
    Serialize status to JSON: Status,JSON String  
    Include progress path: Progress Path,String  
    Include stage name: Stage Name,String  
    Include current behavior: Behavior Name,String  
    Include current action: Action Name,String  
    Wraps domain status: Status  

MarkdownHelp
    Serialize help to Markdown: Help,String  
    Format help sections: Sections,Markdown  
    Wraps domain help: Help  

MarkdownStatus
    Serialize status to Markdown: Status,Markdown String  
    Format progress section: Progress Path,Stage Name,Markdown String  
    Format workflow state: Status,Markdown String  
    Wraps domain status: Status  

Status
    Get progress path: String  
    Get stage name: String  
    Get current behavior name: String  
    Get current action name: String  
    Get has current behavior: Boolean  
    Get has current action: Boolean  

TTYHelp
    Serialize help to TTY: Help,String  
    Format help sections: Sections,String  
    Wraps domain help: Help  

TTYStatus
    Serialize status to TTY: Status,TTY String  
    Format progress line: Progress Path,Stage Name,TTY String  
    Format hierarchical status: Bot,Status,TTY String  
    Wraps domain status: Status  


## Module: story_graph.acceptance_criteria

AcceptanceCriteria
    Get steps: List[Step]  

AcceptanceCriteriaView
    Wraps acceptance criteria JSON: AcceptanceCriteria JSON  
    Displays criteria name: String,AcceptanceCriteria JSON  
    Displays criteria icon: Image  
    Displays steps as checklist: List[Step],HTML  

JSONAcceptanceCriteria
    Include steps: List[Step],JSON Array  
    Wraps domain acceptance criteria: AcceptanceCriteria  

MarkdownAcceptanceCriteria
    Format criteria as checklist: List[Step],Markdown  
    Format steps list: List[Step],Markdown  
    Wraps domain acceptance criteria: AcceptanceCriteria  

TTYAcceptanceCriteria
    Format steps: List[Step],TTY String  
    Format criteria list: List[Step],TTY String  
    Wraps domain acceptance criteria: AcceptanceCriteria  


## Module: story_graph.epic

Epic
    Test file property: String  
    Get all stories: List[Story]  
    Get domain concepts: List[DomainConcept]  

EpicView
    Wraps epic JSON: Epic JSON  
    Displays epic name: String,Epic JSON  
    Displays epic icon: Image  
    Displays sub epics: SubEpicView,SubEpic JSON  
    Opens epic folder: CLI,Epic JSON  
    Opens epic test file: CLI,Epic JSON  

JSONEpic
    Include domain concepts: List[DomainConcept],JSON Array  
    Wraps domain epic: Epic  

MarkdownEpic
    Format domain concepts table: List[DomainConcept],Markdown  
    Wraps domain epic: Epic  

TTYEpic
    Format domain concepts: List[DomainConcept],TTY String  
    Wraps domain epic: Epic  


## Module: story_graph.nodes

InlineNameEditor
    Enables inline editing mode: DOM Element,Input Field  
    Validates name in real-time: StoryNode,Siblings Collection  
    Saves name on blur or Enter: StoryNode,Event  
    Cancels on Escape: Event,Original Value  
    Shows validation messages: ValidationMessageDisplay,Message  

JSONStoryNode
    Serialize node to JSON: StoryNode,JSON String  
    Include name: String,JSON  
    Include sequential order: Float,JSON  
    Include children: List[StoryNode],JSON Array  
    Add child: StoryNode,JSON Result  
    Add child at position: StoryNode,Position,JSON Result  
    Delete child: StoryNode,JSON Result  
    Delete this node: JSON Result  
    Delete with children: JSON Result  
    Update name: String,JSON Result  
    Move to parent: New Parent,Position,JSON Result  
    Move after target: Target StoryNode,JSON Result  
    Move before target: Target StoryNode,JSON Result  
    Reorder children: Start Pos,End Pos,JSON Result  
    Automatically refresh story graph: JSON Result  
    Wraps domain story node: StoryNode  

MarkdownStoryNode
    Serialize node to Markdown: StoryNode,Markdown String  
    Format node header: String,Sequential Order,Markdown  
    Format children list: List[StoryNode],Markdown  
    Wraps domain story node: StoryNode  

StoryNode (Base)
    Serializes: StoryNodeSerializer  
    Get/Update name: String  
    Get node type: String  
    Get node ID: String,StoryNode,StoryNodeNavigator  
    Get parent: StoryNode  
    Get sequential order: StoryNodeNavigator,Float  
    Contains Children: StoryNodeChildren  
    Delete self: StoryNodeSerializer  
    Delete with children: StoryNodeSerializer,StoryNodeChildren  
    Get/Update test: Test  

StoryNodeChildren
    Get children: List[StoryNode]  
    Find child by name: String,StoryNode  
    Delete child: StoryNode  

StoryNodeNavigator
    Build node ID from hierarchy path: String,StoryNode  
    Get parent: StoryNode  
    Move to parent: New Parent,Position  
    Move after: StoryNode,sequential order  
    Move before: StoryNode,sequential order  
    DetermineOrder: FLoat,StoryNode  

StoryNodeSerializer
    File: File  
    Create Node: File,StoryNode  
    Load Node: File,StoryNode  
    Update Node: File,StoryNode  
    Delete Node: File,StoryNode  
    From JSON: JSON,StoryNode  
    To JSON: JSON,StoryNode  

StoryNodeView
    Wraps story node JSON: StoryNode JSON  
    Toggles collapsed: State  
    Add child node: StoryNode,Panel Result  
    Add child at position: StoryNode,Position,Panel Result  
    Delete this node: Panel Result  
    Delete with children: Panel Result  
    Update node name: String,Panel Result  
    Move to parent: New Parent,Position,Panel Result  
    Move after target: Target StoryNode,Panel Result  
    Move before target: Target StoryNode,Panel Result  
    Drag and drop: Drop Target,Position,Panel Result  
    Reorder children: Start Pos,End Pos,Panel Result  
    Automatically refresh story graph: Panel Result  

TTYStoryNode
    Serialize node to TTY: StoryNode,TTY String  
    Format name: String,TTY String  
    Format sequential order: Float,TTY String  
    Format children: List[StoryNode],TTY String  
    Add child: StoryNode,CLI Result  
    Add child at position: StoryNode,Position,CLI Result  
    Delete child: StoryNode,CLI Result  
    Delete this node: CLI Result  
    Delete with children: CLI Result  
    Update name: String,CLI Result  
    Move to parent: New Parent,Position,CLI Result  
    Move after target: Target StoryNode,CLI Result  
    Move before target: Target StoryNode,CLI Result  
    Reorder children: Start Pos,End Pos,CLI Result  
    Automatically refresh story graph: CLI Result  
    Wraps domain story node: StoryNode  


## Module: story_graph.scenario

JSONScenario
    Include steps: List[Step],JSON Array  
    Include test method: Test Method,JSON  
    Wraps domain scenario: Scenario  

MarkdownScenario
    Format Gherkin scenario: Scenario,Markdown  
    Format steps as Given/When/Then: List[Step],Markdown  
    Wraps domain scenario: Scenario  

Scenario
    Test method property: String  
    Get test method: String  
    Get default test method: String  
    Get steps: List[Step]  

ScenarioView
    Wraps scenario JSON: Scenario JSON  
    Displays scenario name: String,Scenario JSON  
    Displays scenario icon: Image  
    Opens test at scenario: CLI,Scenario JSON  

TTYScenario
    Format steps: List[Step],TTY String  
    Format test method: Test Method,TTY String  
    Wraps domain scenario: Scenario  


## Module: story_graph.scenario_outline

JSONScenarioOutline
    Include steps: List[Step],JSON Array  
    Include examples: List[Dict],JSON Array  
    Include test method: Test Method,JSON  
    Wraps domain scenario outline: ScenarioOutline  

MarkdownScenarioOutline
    Format Gherkin scenario outline: ScenarioOutline,Markdown  
    Format steps as Given/When/Then: List[Step],Markdown  
    Format examples table: List[Dict],Markdown  
    Wraps domain scenario outline: ScenarioOutline  

ScenarioOutline
    Test method property: String  
    Get test method: String  
    Get default test method: String  
    Get examples: List[Dict]  
    Get steps: List[Step]  

ScenarioOutlineView
    Wraps scenario outline JSON: ScenarioOutline JSON  
    Displays scenario outline name: String,ScenarioOutline JSON  
    Displays scenario outline icon: Image  
    Displays examples table: List[Dict],Table HTML  
    Opens test at scenario outline: CLI,ScenarioOutline JSON  

TTYScenarioOutline
    Format steps: List[Step],TTY String  
    Format examples: List[Dict],TTY String  
    Format test method: Test Method,TTY String  
    Wraps domain scenario outline: ScenarioOutline  


## Module: story_graph.step

JSONStep
    Include step text: String,JSON  
    Wraps domain step: Step  

MarkdownStep
    Format step as Gherkin: Step,Markdown  
    Wraps domain step: Step  

Step
    Get text: String  

StepView
    Wraps step JSON: Step JSON  
    Displays step text: String,Step JSON  
    Displays step icon: Image  

TTYStep
    Format step text: String,TTY String  
    Format step keyword: String,TTY String  
    Wraps domain step: Step  


## Module: story_graph.story

JSONStory
    Include users: List[StoryUser],JSON Array  
    Include test metadata: Test File,Test Class,JSON  
    Wraps domain story: Story  

MarkdownStory
    Format story card: Story,Markdown  
    Format users section: List[StoryUser],Markdown  
    Wraps domain story: Story  

Story
    Test class property: String  
    Get test class: String  
    Get default test class: String  
    Get story type: String  
    Get users: List[StoryUser]  
    Get scenarios: List[Scenario]  
    Get scenario outlines: List[ScenarioOutline]  
    Get acceptance criteria: List[AcceptanceCriteria]  

StoryView
    Wraps story JSON: Story JSON  
    Displays story name: String,Story JSON  
    Displays story icon: Image  
    Displays scenarios: ScenarioView,Scenario JSON  
    Opens test at class: CLI,Story JSON  

TTYStory
    Format users: List[StoryUser],TTY String  
    Format test metadata: Test File,Test Class,TTY String  
    Wraps domain story: Story  


## Module: story_graph.story_group

StoryGroup


## Module: story_graph.story_map

JSONStoryMap
    Serialize story map to JSON: StoryMap,JSON String  
    Include story graph: Dict,JSON  
    Include all epics: List[Epic],JSON Array  
    Wraps domain story map: StoryMap  

MarkdownStoryMap
    Serialize story map to Markdown: StoryMap,Markdown String  
    Format epic hierarchy: List[Epic],Markdown  
    Format story index: List[Story],Markdown  
    Wraps domain story map: StoryMap  

StoryMap
    Load from bot directory: Bot,StoryMap  
    Load from story graph: File Path,StoryMap  
    Walk nodes: StoryNode,Iterator[StoryNode]  
    Get all stories: List[Story]  
    Get all scenarios: List[Scenario]  
    Get all domain concepts: List[DomainConcept]  
    Find by name: Name,StoryNode  
    Find node by path: Path String,StoryNode  
    Get story graph dict: Dict  
    Get epics: List[Epic]  
    Save to story graph: File Path  
    Reload from story graph: File Path,StoryMap  
    Validate graph structure: Validation Result  

StoryMapView
    Wraps story map JSON: StoryMap JSON  
    Renders story graph as tree hierarchy: StoryNode,HTML  
    Displays epic hierarchy: EpicView,Epic JSON  
    Shows context-appropriate action buttons: StoryNode,ButtonSet  
    Refreshes tree display: StoryGraph,DOM  
    Searches stories: Filter,StoryGraph JSON  
    Opens story graph file: CLI,File JSON  
    Opens story map file: CLI,File JSON  
    Delegates to InlineNameEditor: InlineNameEditor,StoryNode  
    Delegates to StoryNodeDragDropManager: StoryNodeDragDropManager,StoryNode  

StoryNodeDragDropManager
    Shows drag cursor with icon: Cursor Style,Node Icon  
    Validates drop target compatibility at UI level: Source Node Type,Target Parent Type  
    Shows no-drop cursor for incompatible targets: Cursor Style  
    Highlights valid drop target: Target Element,CSS Class  
    Delegates move to StoryNode domain operation: StoryNode,Target Parent,Position  
    Returns node to original on invalid drop: Original Position,Animation  

TTYStoryMap
    Serialize story map to TTY: StoryMap,TTY String  
    Format epics list: List[Epic],TTY String  
    Format story hierarchy: StoryMap,TTY String  
    Walk and format nodes: StoryNode,TTY String  
    Wraps domain story map: StoryMap  


## Module: story_graph.story_user

JSONStoryUser
    Serialize user to JSON: StoryUser,JSON String  
    Include user name: String,JSON  
    Include user list: List[StoryUser],JSON Array  
    Wraps domain story user: StoryUser  

MarkdownStoryUser
    Serialize user to Markdown: StoryUser,Markdown String  
    Format user badge: StoryUser,Markdown  
    Format user list: List[StoryUser],Markdown  
    Wraps domain story user: StoryUser  

StoryUser
    Get name: String  
    From string: String,StoryUser  
    From list: List[String],List[StoryUser]  
    To string: String  

StoryUserView
    Wraps story user JSON: StoryUser JSON  
    Displays user name: String,StoryUser JSON  
    Displays user icon: Image  
    Filters stories by user: StoryUser,Panel Result  

TTYStoryUser
    Serialize user to TTY: StoryUser,TTY String  
    Format user name: String,TTY String  
    Format user list: List[StoryUser],TTY String  
    Wraps domain story user: StoryUser  


## Module: story_graph.sub_epic

SubEpic
    Test file property: String  

SubEpicView
    Wraps sub epic JSON: SubEpic JSON  
    Displays sub epic name: String,SubEpic JSON  
    Displays sub epic icon: Image  
    Displays nested sub epics: SubEpicView,SubEpic JSON  
    Displays stories: StoryView,Story JSON  
    Opens sub epic folder: CLI,SubEpic JSON  
    Opens sub epic test file: CLI,SubEpic JSON  


## Module: story_graph.test

JSONTest
    Serialize test to JSON: Test,JSON String  
    Include test file: String,JSON  
    Include test class: String,JSON  
    Include test method: String,JSON  
    Wraps domain test: Test  

MarkdownTest
    Serialize test to Markdown: Test,Markdown String  
    Format test link: Test File,Test Class,Test Method,Markdown  
    Wraps domain test: Test  

TTYTest
    Serialize test to TTY: Test,TTY String  
    Format test file: String,TTY String  
    Format test class: String,TTY String  
    Format test method: String,TTY String  
    Wraps domain test: Test  

Test
    Get test file: String  
    Get test class: String  
    Get test method: String  
    Get default test class: String  
    Get default test method: String  
    Build from story node: StoryNode,TestMetadata  

TestView
    Wraps test JSON: Test JSON  
    Displays test file: String,Test JSON  
    Displays test class: String,Test JSON  
    Displays test method: String,Test JSON  
    Opens test file: CLI,Test JSON  
    Opens test at class: CLI,Test JSON  
    Opens test at method: CLI,Test JSON  

