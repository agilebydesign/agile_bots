(E) Build Agile Bots
    (E) Generate MCP Tools
        (S) Generate Bot Tools
        (S) Generate Behavior Tools
        (S) Generate MCP Bot Server
        (S) Generate Behavior Action Tools
        (S) Restart MCP Server To Load Code Changes
    (E) Generate CLI
        (S) Generate BOT CLI code
        or (S) Generate Cursor Command Files
(E) Invoke Bot
    (E) Init Project
        (S) Initialize Project Location
        or (S) Input File Copied To Context Folder
        or (S) Store Context Files
        or (S) Guards Prevent Writes Without Project
        or (S) Invoke Bot Tool
        or (S) Load And Merge Behavior Action Instructions
        or (S) Forward To Current Behavior and Current Action
        or (S) Forward To Current Action
    (E) Invoke CLI
        (S) Invoke Bot CLI
        or (S) Invoke Bot Behavior CLI
        or (S) Invoke Bot Behavior Action CLI
        or (S) Get Help for Command Line Functions
    (E) Perform Behavior Action
        (S) Find Behavior Folder
        or (S) Execute Behavior
        or (S) Invoke Behavior in Workflow Order
        or (S) Invoke Behavior Actions in Workflow Order
        or (S) Close Current Action
        (S) Inject Next Behavior Reminder
        (S) Load And Merge Behavior Action Instructions
(E) Execute Behavior Actions
    (E) Gather Context
        (S) Inject Guardrails As Part Of Clarify Requirements
        or (S) Track Activity for Gather Context Action
        or (S) Store Clarification Data
        or (S) Proceed To Decide Planning
    (E) Decide Planning Criteria Action
        (S) Inject Planning Criteria Into Instructions
        or (S) Track Activity for Planning Action
        or (S) Save Final Assumptions and Decisions
        or (S) Proceed To Build Knowledge
    (E) Build Knowledge
        (S) Load Story Graph Into Memory
        opt (S) Inject Knowledge Graph Template and Builder Instructions
        or (S) Track Activity for Build Knowledge Action
        opt (S) Update Existing Knowledge Graph
        or (S) Proceed To Render Output
        (S) proactively Validate knowledge against rules
(see Validate Knowledge & Content Against Rules)
THEN BuildKnowledgeAction tells AI to notify the user of what corrections it made as part of presenting the fact that it's done building knowledge.
    (E) Render Output
        (S) Track Activity for Render Output Action
        or (S) Proceed To Validate Rules
        or (S) Load Render Configurations
        or (S) Inject Template Instructions
        or (S) Inject Synchronizer Instructions
    (E) Validate Knowledge & Content Against Rules
        (S) Inject Validation Rules for Validate Rules Action
        or (S) Track Activity for Validate Rules Action
        or (S) Invoke Complete Validation Workflow
        (S) Discovers Scanners
        (S) Run Scanners against Knowledge Graph
        or (S) Run AST Scanners against Knowledge Graph (OUT OF SCOPE)
        (S) Validate Rules According To Scope
        (S) Generate Violation Report
        (S) Run Scanners Against Code
        (S) Run Scanners Against Test Code
        (S) Run All Scanners
        (S) Report Validation and Error Handling
