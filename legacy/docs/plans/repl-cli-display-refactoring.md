=== Story Graph ===# Design Model

## Object-Oriented Design Patterns

### Domain Concepts with Responsibilities

## Epic: REPL CLI Display Architecture

### REPLSession

**Responsibilities:**
- Orchestrates REPL command handling: CommandRegistry, CLIBot, OutputFormatter
- Renders status display: CLIStatusScreen, CLIBot
- Dispatches commands via CommandRegistry
- Has: CommandRegistry, CLIBot, OutputFormatter

### CLIStatusScreen

**Responsibilities:**
- Renders complete status screen: CLIStatusHeaderComponent, DashboardHeaderComponent, HeadlessModeComponent, ScopeDisplayComponent, ProgressDisplayComponent, CommandsMenuComponent
- Has: DashboardHeaderComponent, HeadlessModeComponent, ScopeDisplayComponent, ProgressDisplayComponent, CommandsMenuComponent



**Screen Example (Complete Status Display):**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
***                    CLI STATUS section                    ***
This section contains current scope filter (if set), current progress in workflow, and available commands
Review the CLI STATUS section below to understand both current state and available commands.
☢️  You MUST DISPLAY this entire section in your response to the user exactly as you see it. ☢️
────────────────────────────────────────────────────────────
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 🤖 Bot: story_bot
**Bot Path:**
C:\dev\augmented-teams\agile_bot\bots\story_bot

📂 **Workspace:** base_bot
C:\dev\augmented-teams\agile_bot\bots\base_bot

To change path:
path demo/mob_minion              # Change to specific project
path ../another_bot               # Change to relative path
────────────────────────────────────────────────────────────
Headless Mode:
  Status: Available (configured)
  API Key: key_2780b8...

  Usage:
    python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless "Your instruction"

  Examples:
    python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless "Create hello world"
    python agile_bot/bots/base_bot/src/repl_cli/repl_main.py --headless shape
    python agile_bot/bots/base_bot/src/repl_cli/repl_main.py --headless shape.build

  Active Session:
    Session ID: 2025-12-30-01-31-17
    Status: running
    Log: C:\dev\augmented-teams\agile_bot\bots\base_bot\logs\headless-2025-12-30-01-31-17.log
────────────────────────────────────────────────────────────
🎯 Scope
🎯 Current Scope: all (entire project)

To change scope (pick ONE - setting a new scope replaces the previous):
scope all                            # Clear scope, work on entire project
scope "Story Name"                   # Filter by story (replaces any file scope)
scope "file:C:/path/to/**/*.py"      # Filter by files (replaces any story scope)
────────────────────────────────────────────────────────────
## 📍 **Progress**
**Current Position:**
shape.clarify.instructions

- ➤ shape - Outline a story map made up of epics, sub-epics, and stories
  - ➤ clarify - Gather context by asking required questions and collecting evidence in order to increase understanding
    - ➤ instructions
    - ☐ submit
    - ☐ confirm
  - ☐ strategy
  - ☐ build
  - ☐ validate
  - ☐ render
- ☐ prioritization
- ☐ discovery
- ☐ exploration
- ☐ scenarios
- ☐ tests
- ☐ code

Run:
echo 'behavior.action' | python repl_main.py           # Defaults to 'instructions' operation
echo 'behavior.action.operation' | python repl_main.py  # Runs operation

**Args:**
--scope "Epic, Sub Epic, Story"      # Filter by story names
--scope "file:path/one,path/two"     # Filter by file paths
--headless                             # Execute autonomously without user input
────────────────────────────────────────────────────────────
## 💻 **Commands:**
**status | back | current | next | path [dir] | scope [filter] | headless "msg" | help | exit**

// Run
echo '[command]' | python repl_main.py
// to invoke commands

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Behaviors:** shape | prioritization | discovery | exploration | scenarios | tests | code
**Actions:** clarify | strategy | build | validate | render

### DisplayComponent

**Responsibilities:**
- Renders display fragment: OutputFormatter
- Has: OutputFormatter

### DisplayInfoComponent : DisplayComponent

**Responsibilities:**
- Renders using CLIBase subclass
- Has: CLIBase

### CLIStatusHeaderComponent : DisplayComponent

**Responsibilities:**
- Renders CLI STATUS section header: OutputFormatter
- Formats warning text for AI: OutputFormatter
- Applies header separators: OutputFormatter

---

**Screen Example:**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
***                    CLI STATUS section                    ***
This section contains current scope filter (if set), current progress in workflow, and available commands
Review the CLI STATUS section below to understand both current state and available commands.
☢️  You MUST DISPLAY this entire section in your response to the user exactly as you see it. ☢️
────────────────────────────────────────────────────────────
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### DashboardHeaderComponent : DisplayComponent

**Responsibilities:**
- Renders bot and workspace information as a unified header: BotInfoComponent, WorkspaceInfoComponent, OutputFormatter
- Applies separator lines above and below the header group: OutputFormatter
- Has: BotInfoComponent, WorkspaceInfoComponent

---

**Screen Example:**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
## 🤖 Bot: story_bot  
**Bot Path:**  
C:\dev\augmented-teams\agile_bot\bots\story_bot  

📂 **Workspace:** base_bot  
C:\dev\augmented-teams\agile_bot\bots\base_bot  

To change path:  
path demo/mob_minion              # Change to specific project  
path ../another_bot               # Change to relative path  
────────────────────────────────────────────────────────────  

### BotInfoComponent : DisplayInfoComponent

**Responsibilities:**
- Renders bot name and path: CLIBot
- Formats bot icon and metadata: CLIBot
- Has: CLIBot

---

**Screen Example:**

## 🤖 Bot: story_bot  
**Bot Path:**  
C:\dev\augmented-teams\agile_bot\bots\story_bot  

### WorkspaceInfoComponent : DisplayInfoComponent

**Responsibilities:**
- Renders workspace name and path: CLIPath
- Formats path change instructions: CLIPath
- Has: CLIPath

---

**Screen Example:**

📂 **Workspace:** base_bot  
C:\dev\augmented-teams\agile_bot\bots\base_bot  

To change path:  
path demo/mob_minion              # Change to specific project  
path ../another_bot               # Change to relative path  
────────────────────────────────────────────────────────────  

### HeadlessModeComponent : DisplayComponent

**Responsibilities:**
- Renders headless mode status: HeadlessConfig, OutputFormatter
- Formats usage examples: HeadlessConfig, OutputFormatter
- Displays active session info: HeadlessConfig, Path, OutputFormatter
- Has: HeadlessConfig

---

**Screen Example:**

Headless Mode:  
  Status: Available (configured)  
  API Key: key_2780b8...  

  Usage:  
    python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless "Your instruction"  

  Examples:  
    python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless "Create hello world"  
    python agile_bot/bots/base_bot/src/repl_cli/repl_main.py --headless shape  
    python agile_bot/bots/base_bot/src/repl_cli/repl_main.py --headless shape.build  

  Active Session:  
    Session ID: 2025-12-30-01-31-17  
    Status: running  
    Log: C:\dev\augmented-teams\agile_bot\bots\base_bot\logs\headless-2025-12-30-01-31-17.log  
────────────────────────────────────────────────────────────  

### ScopeDisplayComponent : DisplayInfoComponent

**Responsibilities:**
- Renders scope filter display: CLIScope
- Formats scope items: CLIScope
- Adds scope change instructions: CLIScope
- Adds AI warning messages: CLIScope
- Has: CLIScope

---

**Screen Example (All Scope):**

🎯 Scope  
🎯 Current Scope: all (entire project)  

To change scope (pick ONE - setting a new scope replaces the previous):  
scope all                            # Clear scope, work on entire project  
scope "Story Name"                   # Filter by story (replaces any file scope)  
scope "file:C:/path/to/**/*.py"      # Filter by files (replaces any story scope)  
────────────────────────────────────────────────────────────  

**Screen Example (Story Scope):**

## 🎯 **Scope**  
**Filter:** Generate Bot Tools, Generate BOT CLI code  

📝 Generate Bot Tools  
📝 Generate BOT CLI code  


- Work ONLY on this scope:  
- DO NOT work on all files or the entire story graph  
- Focus EXCLUSIVELY on the items listed above - do not work on the entire story graph or file system  

To change scope (pick ONE - setting a new scope replaces the previous):  
scope all                            # Clear scope, work on entire project  
scope "Story Name"                   # Filter by story (replaces any file scope)  
scope "file:C:/path/to/**/*.py"      # Filter by files (replaces any story scope)  

**Screen Example (File Scope):**

## 🎯 **Scope**  
**Filter:** agile_bot/bots/base_bot/src/repl_cli/**/*.py  

  (no files found)  


- Work ONLY on this scope:  
- DO NOT work on all files or the entire story graph  
- Focus EXCLUSIVELY on the items listed above - do not work on the entire story graph or file system  

To change scope (pick ONE - setting a new scope replaces the previous):  
scope all                            # Clear scope, work on entire project  
scope "Story Name"                   # Filter by story (replaces any file scope)  
scope "file:C:/path/to/**/*.py"      # Filter by files (replaces any story scope)  

### ProgressDisplayComponent : DisplayInfoComponent

**Responsibilities:**
- Renders current position: CLIBehaviors, CLIBehavior
- Formats behavior/action hierarchy tree: CLIBehaviors, CLIBehavior, CLIAction
- Shows completion status icons: CLIBehaviors, CLIBehavior
- Has: CLIBehaviors

---

**Screen Example:**

## 📍 **Progress**  
**Current Position:**  
shape.clarify.instructions  

- ➤ shape - Outline a story map made up of epics, sub-epics, and stories  
  - ➤ clarify - Gather context by asking required questions and collecting evidence in order to increase understanding  
    - ➤ instructions  
    - ☐ submit  
    - ☐ confirm  
  - ☐ strategy  
  - ☐ build  
  - ☐ validate  
  - ☐ render  
- ☐ prioritization  
- ☐ discovery  
- ☐ exploration  
- ☐ scenarios  
- ☐ tests  
- ☐ code  

Run:  
echo 'behavior.action' | python repl_main.py           # Defaults to 'instructions' operation  
echo 'behavior.action.operation' | python repl_main.py  # Runs operation  

**Args:**  
--scope "Epic, Sub Epic, Story"      # Filter by story names  
--scope "file:path/one,path/two"     # Filter by file paths  
--headless                             # Execute autonomously without user input  
────────────────────────────────────────────────────────────  

### CommandsMenuComponent : DisplayComponent

**Responsibilities:**
- Renders available commands: CommandsMenu, OutputFormatter
- Formats command usage examples: CommandsMenu, OutputFormatter
- Has: CommandsMenu

---

**Screen Example:**

## 💻 **Commands:**  
**status | back | current | next | path [dir] | scope [filter] | headless "msg" | help | exit**  

// Run  
echo '[command]' | python repl_main.py  
// to invoke commands  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  

**Behaviors:** shape | prioritization | discovery | exploration | scenarios | tests | code  
**Actions:** clarify | strategy | build | validate | render  

### HeadlessConfig

**Responsibilities:**
- Loads configuration from file system
- Validates API key configuration
- Provides API key prefix
- Indicates if configured

### CLIScope : CLIBase

**Responsibilities:**
- Wraps domain scope: Scope
- Formats scope display with CLI styling: Scope, OutputFormatter

### CLIPath : CLIBase

**Responsibilities:**
- Wraps path: Path
- Formats path in code blocks: Path, OutputFormatter
- Formats path change instructions: OutputFormatter

### CLIBehaviors : CLIBase

**Responsibilities:**
- Wraps behaviors collection: Behaviors
- Formats behavior hierarchy: Behaviors, CLIBehavior, CLIAction, OutputFormatter
- Tracks current position: Behaviors, CLIBehavior

### CommandRegistry

**Responsibilities:**
- Central registry of all REPL commands
- Maps command names to handler methods
- Provides command metadata (help text, display format, parameters)
- Distinguishes between CLI navigation commands and Action operation commands
- Has: List of Command objects

### Command

**Responsibilities:**
- Represents a single command with its metadata
- Name, aliases, handler method reference
- Help text and parameter signature
- Display format for status/help screens
- Command category (navigation, action, meta)

### CLINavigationCommand : Command

**Responsibilities:**
- Commands handled by REPLSession (status, help, next, back, current, path, scope, headless)
- Handler: REPLSession method reference
- Parameters: Derived from method signature
- Help: Generated from docstring and signature

### ActionOperationCommand : Command

**Responsibilities:**
- Commands that delegate to Action domain methods (instructions, submit, confirm)
- Handler: Action method reference (via current action)
- Parameters: Derived from Action.context_class fields
- Help: Generated from action config and context class
- Dynamically available based on current action

### CommandsMenu

**Responsibilities:**
- Renders command list from CommandRegistry
- Formats command usage examples from Command metadata
- Has: CommandRegistry

---

**Screen Example (Help Command Output):**

Core Commands:
  echo '[behavior.][action.]operation' | python repl_main.py  - navigate and perform operation
  echo '[behavior][.action]' | python repl_main.py           - navigate to behavior/action

  Available Components:
    behaviors   -> shape | prioritization | discovery | exploration | scenarios | tests | code

    actions:
      clarify      - Gather context and answer key questions
      strategy     - Plan the approach for this behavior
      build        - Execute the main work of this behavior
      validate     - Verify work meets requirements
      render       - Generate final outputs and artifacts

    operations:
      instructions  [context, scope, or action-specific params]
      submit        [scope, decisions, assumptions, or action-specific params]
      confirm

  Examples:
    echo '.' | python repl_main.py                -> Execute current behavior.action.operation
    echo 'shape' | python repl_main.py            -> Jump to behavior and execute first action.operation
    echo 'build' | python repl_main.py            -> Jump to action and execute first operation
    echo 'submit scope="s1"' | python repl_main.py -> Jump to operation with params and execute
    echo 'shape.build' | python repl_main.py      -> Jump to behavior.action and execute first operation
    echo 'shape.build.submit' | python repl_main.py -> Jump to behavior.action.operation and execute
    python repl_main.py headless shape            -> Execute behavior in headless mode (unattended)

  Other Commands:
    echo 'status' | python repl_main.py           - Show full workflow hierarchy
    echo 'back' | python repl_main.py             - Go back to previous action
    echo 'current' | python repl_main.py          - Re-execute current operation
    echo 'next' | python repl_main.py             - Advance to next action
    echo 'path [dir]' | python repl_main.py       - Show/set working directory
    echo 'scope C:\full\path' | python repl_main.py - Set scope to COMPLETE folder path
    echo 'scope all' | python repl_main.py        - Clear scope filter
    echo 'headless "message"' | python repl_main.py - Execute message in headless mode
    echo 'help' | python repl_main.py             - Show this help
    echo 'exit' | python repl_main.py             - Exit CLI

  Scope Command Details:
    IMPORTANT: You can only have ONE scope type at a time (story OR files, never both).
    Setting a new scope REPLACES any previous scope.

    When passing file/folder paths to scope, you MUST provide the COMPLETE
    folder structure. Use ABSOLUTE paths or FULL relative paths from the work path.

    Usage (pick ONE - each replaces the previous scope):
      echo 'scope' | python repl_main.py                           - Show current scope
      echo 'scope all' | python repl_main.py                       - Clear scope filter
      echo 'scope "Story Name"' | python repl_main.py              - Filter by story (replaces file scope)
      echo 'scope "file:C:/path/to/src/**/*.py"' | python repl_main.py - Filter by files (replaces story scope)

    Examples (CORRECT - each sets a SINGLE scope type):
      scope "Enter Password, Authenticate User"                                        - Story scope
      scope "file:C:/dev/augmented-teams/agile_bot/bots/base_bot/src/**/*.py"          - File scope with glob

    Examples (INCORRECT - DO NOT USE):
      scope src              [X] partial path - missing parent directories
      scope repl_cli         [X] folder name only - incomplete structure
      scope ..\src           [X] relative navigation - use complete paths

  Headless Mode:
    Status: Available (API key configured)

    Usage:
      python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless "Your instruction"
      python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless shape.build
      python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless shape.build "context message"

    Commands:
      headless "text"                    Execute pass-through instruction
      headless shape                      Execute entire behavior
      headless shape.build                Execute single action
      headless shape.build.submit         Execute single operation
      headless shape.build "message"      Execute action with context message

    Options:
      --context file.md    Context file to include
      --timeout N          API timeout in seconds (default: 600, use 30 for tests)

    Examples:
      python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless "Create hello world function"
      python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless shape
      python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless shape.build --timeout 30
      python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless shape.build "Focus on error handling"
      python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless "Build feature" --context context.md

### DomainObject

**Responsibilities:**

### Bot : DomainObject

**Responsibilities:**

### Behavior : DomainObject

**Responsibilities:**

### Action : DomainObject

**Responsibilities:**

### CLIBase

**Responsibilities:**
- Has: OutputFormatter

### CLIBot : CLIBase

**Responsibilities:**
- Wraps domain bot: Bot

---

**Screen Example:**

## 🤖 Bot: story_bot  
**Bot Path:**  
C:\dev\augmented-teams\agile_bot\bots\story_bot  

### CLIBehaviors : CLIBase

**Responsibilities:**
- Wraps domain behaviors collection: Behaviors

---

**Screen Example:**

- ➤ shape - Outline a story map made up of epics, sub-epics, and stories  
  - ➤ clarify - Gather context by asking required questions and collecting evidence in order to increase understanding  
    - ➤ instructions  
    - ☐ submit  
    - ☐ confirm  
  - ☐ strategy  
  - ☐ build  
  - ☐ validate  
  - ☐ render  
- ☐ prioritization  
- ☐ discovery  
- ☐ exploration  
- ☐ scenarios  
- ☐ tests  
- ☐ code  

### CLIBehavior : CLIBase

**Responsibilities:**
- Wraps domain behavior: Behavior

---

**Screen Example:**

- ➤ shape - Outline a story map made up of epics, sub-epics, and stories  
  - ➤ clarify - Gather context by asking required questions and collecting evidence in order to increase understanding  
    - ➤ instructions  
    - ☐ submit  
    - ☐ confirm  
  - ☐ strategy  
  - ☐ build  
  - ☐ validate  
  - ☐ render  

### CLIAction : CLIBase

**Responsibilities:**
- Wraps domain action: Action

---

**Screen Example:**

  - ➤ clarify - Gather context by asking required questions and collecting evidence in order to increase understanding  
    - ➤ instructions  
    - ☐ submit  
    - ☐ confirm  

### CLIScope : CLIBase

**Responsibilities:**
- Wraps domain scope: Scope
- Formats scope display with CLI styling: Scope, OutputFormatter

---

**Screen Example (Story Scope):**

## 🎯 **Scope**  
**Filter:** Generate Bot Tools, Generate BOT CLI code  

📝 Generate Bot Tools  
📝 Generate BOT CLI code  

**Screen Example (All Scope):**

🎯 Scope  
🎯 Current Scope: all (entire project)  

### CLIPath : CLIBase

**Responsibilities:**
- Wraps path: Path
- Formats path in code blocks: Path, OutputFormatter

---

**Screen Example:**

📂 **Workspace:** base_bot  
C:\dev\augmented-teams\agile_bot\bots\base_bot  

To change path:  
path demo/mob_minion              # Change to specific project  
path ../another_bot               # Change to relative path  







-------------------
## Command Architecture

### Command Types

**1. CLI Navigation Commands**
- Handled by: REPLSession methods
- Examples: status, help, next, back, current, path, scope, headless, exit
- Execution: Direct method call on REPLSession
- Parameters: Extracted from method signature using inspect
- Help: Generated from method docstring

**2. Action Operation Commands**
- Handled by: Action domain methods
- Examples: instructions, submit, confirm
- Execution: Delegated to current_action.{operation}()
- Parameters: Extracted from Action.context_class dataclass fields
- Help: Generated from action config + context class annotations

### CommandRegistry Structure

```
CommandRegistry
├── register_cli_command(name, method, aliases, category)
├── register_action_command(name, operation, context_class)
├── get_command(name) → Command
├── get_all_commands() → List[Command]
├── get_commands_by_category(category) → List[Command]
└── execute(command_name, args) → REPLCommandResponse

Command
├── name: str
├── aliases: List[str]
├── handler: Callable (method reference)
├── category: CommandCategory (navigation, action, meta)
├── parameters: List[Parameter] (from signature/context_class)
├── help_text: str (from docstring/config)
├── display_format: str (for status screen)
└── execute(args) → REPLCommandResponse
```

### Integration Points

**REPLSession._handle_simple_command():**
```python
def _handle_simple_command(self, command: str) -> REPLCommandResponse:
    parts = command.split(maxsplit=1)
    command_verb = parts[0].lower()
    command_args = parts[1] if len(parts) > 1 else ""
    
    # Use CommandRegistry instead of if/elif chain
    cmd = self.command_registry.get_command(command_verb)
    if cmd:
        return cmd.execute(command_args)
    
    # Fallback: behavior/action shortcuts
    ...
```

**CommandsMenuComponent:**
```python
def render(self) -> str:
    # Get commands from registry instead of hardcoded list
    nav_commands = self.command_registry.get_commands_by_category("navigation")
    action_commands = self.command_registry.get_commands_by_category("action")
    
    # Format using Command.display_format
    ...
```

**REPLHelp:**
```python
def generate_help(self) -> str:
    # Get all commands from registry
    commands = self.command_registry.get_all_commands()
    
    # Use Command.help_text and Command.parameters
    for cmd in commands:
        help_lines.append(f"{cmd.name} - {cmd.help_text}")
        for param in cmd.parameters:
            help_lines.append(f"  --{param.name} {param.type}")
    ...
```

### Example: Command Registration

**In REPLSession.__init__():**
```python
self.command_registry = CommandRegistry(self)

# Register CLI navigation commands
self.command_registry.register_cli_command(
    name="status",
    method=self._handle_status_command,
    aliases=[],
    category="meta",
    display_format="status"
)

self.command_registry.register_cli_command(
    name="next",
    method=self._handle_next_command,
    aliases=["advance"],
    category="navigation",
    display_format="next"
)

self.command_registry.register_cli_command(
    name="scope",
    method=self._handle_scope_command,
    aliases=[],
    category="state",
    display_format="scope [filter]"
)

# Action operation commands are registered dynamically
# when an action becomes current
```

**When navigating to an action:**
```python
def navigate_to_action(self, action_name: str):
    # ... navigation logic ...
    
    # Register action operation commands based on current action
    action = self.current_action
    self.command_registry.register_action_commands(action)
    # This inspects action.context_class to get parameters
    # and registers: instructions, submit, confirm
```

### Benefits

1. **Single Source of Truth**: All command metadata in one place
2. **Automatic Help Generation**: Parameters extracted from signatures
3. **Easy to Extend**: Add new commands by registering, not editing multiple files
4. **Type Safety**: Command.parameters preserves type information
5. **Testability**: Can mock CommandRegistry for testing
6. **Discoverability**: Can enumerate all available commands programmatically
7. **Dynamic Commands**: Action commands appear/disappear based on current action
8. **Consistent Display**: All components use Command.display_format

-------------------
CRC Walkthroughs


