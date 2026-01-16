
(E) Invoke Bot
    (E) Init Project
        (S) Bot Behavior --> Initialize Project Location
        or (S) Bot Behavior --> Initialize Project Creates Context Folder
        or (S) Bot Behavior --> Input File Copied To Context Folder
        or (S) Bot Behavior --> Store Context Files
        or (S) Bot Behavior --> Guards Prevent Writes Without Project
        or (S) Stores Activity for Initialize Project Action
    (E) Invoke MCP
        (S) AI Chat --> Invoke Bot Tool
        or (S) Bot Behavior --> Load And Merge Behavior Action Instructions
        or (S) AI Chat --> Forward To Current Behavior and Current Action
        or (S) AI Chat --> Forward To Current Action
    (E) Invoke CLI
        (S) Human --> Invoke Bot CLI
        or (S) Human --> Invoke Bot Behavior CLI
        or (S) Human --> Invoke Bot Behavior Action CLI
        or (S) Human --> Get Help for Command Line Functions
    (E) Perform Behavior Action
        (S) Bot Behavior --> Find Behavior Folder
        or (S) Bot Behavior --> Execute Behavior
        or (S) Bot Behavior --> Invoke Behavior in Workflow Order
        or (S) Bot Behavior --> Invoke Behavior Actions in Workflow Order
        or (S) Bot Behavior --> Close Current Action
        (S) Bot Behavior --> Inject Next Behavior Reminder
        (S) Bot Behavior --> Load And Merge Behavior Action Instructions
(E) Execute Behavior Actions
    (E) Gather Context
        (S) Bot Behavior --> Inject Guardrails As Part Of Clarify Requirements
        or (S) Bot Behavior --> Track Activity for Gather Context Action
        or (S) Bot Behavior --> Store Clarification Data
        or (S) Bot Behavior --> Proceed To Decide Planning
    (E) Decide Planning Criteria Action
        (S) Bot Behavior --> Inject Planning Criteria Into Instructions
        or (S) Bot Behavior --> Track Activity for Planning Action
        or (S) Bot Behavior --> Save Final Assumptions and Decisions
        or (S) Bot Behavior --> Proceed To Build Knowledge
    (E) Build Knowledge
        (S) Bot Behavior --> Load Story Graph Into Memory
        opt (S) Bot Behavior --> Inject Knowledge Graph Template and Builder Instructions
        or (S) Bot Behavior --> Track Activity for Build Knowledge Action
        opt (S) Bot Behavior --> Update Existing Knowledge Graph
        or (S) Bot Behavior --> Proceed To Render Output
        (S) Bot Behavior --> proactively Validate knowledge against rules
    (E) Render Output
        (S) Bot Behavior --> Track Activity for Render Output Action
        or (S) Bot Behavior --> Proceed To Validate Rules
        or (S) Bot Behavior --> Load Render Configurations
        or (S) Bot Behavior --> Inject Template Instructions
        or (S) Bot Behavior --> Inject Synchronizer Instructions
    (E) Validate Knowledge & Content Against Rules
        (S) Bot Behavior --> Inject Validation Rules for Validate Rules Action
        or (S) Bot Behavior --> Track Activity for Validate Rules Action
        or (S) Bot Behavior --> Invoke Complete Validation Workflow
        (S) Bot Behavior --> Discovers Scanners
        (S) Scanner --> Run Scanners against Knowledge Graph
        or (S) Scanner --> Run AST Scanners against Knowledge Graph (OUT OF SCOPE)
        (S) Bot Behavior --> Validate Rules According To Scope
        (S) Bot Behavior --> Generate Violation Report
        (S) Bot Behavior --> Run Scanners Against Code
        (S) Bot Behavior --> Run Scanners Against Test Code
        (S) Bot Behavior --> Run All Scanners
        (S) Bot Behavior --> Report Validation and Error Handling
