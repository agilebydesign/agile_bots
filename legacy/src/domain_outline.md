ActionNode
    Wrap action execution: Action,Behavior
    Get instructions from action: Action
    Confirm with response: Action,AI Chat
    Run in autonomous mode: AI Client,ExecutionMode
    Run in interactive mode: Human,ExecutionMode

Base Action
    Inject Instructions: Behavior
    Load Relevant Content + Inject Into Instructions: Content
    Save content changes: Content

Base Action Node
    Provide abstract node interface: ActionNode
    Define two-pass pattern: ActionNode

Base Bot
    Executes Actions: Workflow,Behavior,Action
    Track activity: Behavior,Action
    Route to behaviors and actions: Router,Trigger Words
    Persist content: Content
    Manage Project State: Project
    Render: 

Behavior
    Perform Configured Actions: Actions
    Invoke On Trigger Words: List
    Inject Instructions: Text
    Provide Guardrails: GuardRails
    Provide Rules: Rule,Validation
    Provide Content Specs: Content

Behavior Graph Builder
    Read behavior workflow configuration: Behavior,Workflow
    Create nodes from actions: Action,ActionNode
    Create edges from next_action relationships: Workflow,Action
    Build StateGraph structure: Workflow,LangGraph

Behavior Workflow
    Determine next Action: Behavior,Action,State
    Track state: Behavior,Action,State

Checkpoint
    Save workflow state: State,LangGraphRunner
    Restore workflow state: State,LangGraphRunner
    Track execution history: State
    Enable resume capability: Workflow,LangGraphRunner

ExecutionMode
    Determine AI interaction: ActionNode,AI Client
    Control pause points: ActionNode,Human

GatherContextAction
    Inject gather context instructions: Behavior,Guardrails,Required Clarifications
    Inject questions and evidence: Behavior,Guardrails,Key Questions,Evidence

Guardrails
    Provide required context: Key Questions,Evidence
    Guide planning decisions: Decision Criteria,Assumptions
    Define recommended human activity: Human,Instructions

LangGraphRunner
    Load workflow definition: Workflow,Behavior
    Compile graph with checkpointer: Workflow,Checkpoint
    Execute workflow graph: Workflow,ActionNode
    Manage checkpoint storage: Checkpoint
    Resume from checkpoint: Checkpoint,Workflow

Project
    Move project to working area: Working Directory
    Save project in context: Working Directory,Workflow State
    Update project area: Working Directory,Content

Router
    Match trigger patterns: Trigger Words,Route
    Route to MCP bot tool: Base Bot,Trigger Words
    Route to behavior tool: Behavior,Trigger Words
    Route to action tool: Action,Trigger Words
    Forward to behavior: Behavior,Base Bot
    Forward to action: Action,Behavior
    Forward to current behavior and action: Behavior,Action,Base Bot

Specific Bot
    Provide Behavior config: Bot Config,Behavior
    Provide MCP config: MCP Config
    Provide Renderers: 
    Provide Extractors: 
    Provide Synchronizer: 
    Provide Trigger Words: 

Workflow
    Execute nodes in sequence: ActionNode,LangGraphRunner
    Handle conditional branching: Decision Node,State
    Support loops and iterations: ActionNode,State
    Pause at interactive points: Human,ExecutionMode
    Resume from checkpoint: Checkpoint,LangGraphRunner

Workflow State
    Track current action: Action
    Track completed actions: Action,Activity Log
    Determine next action: Action,Behavior
    Pause workflow: Human,AI Chat
    Resume workflow: Human,AI Chat
