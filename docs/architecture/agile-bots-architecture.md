# Agile Bots Architecture - VS Code Extension

## Table of Contents

- [Agile Bots Architecture - VS Code Extension](#agile-bots-architecture---vs-code-extension)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Architecture Layers](#architecture-layers)
  - [File Structure](#file-structure)
    - [Why This Structure?](#why-this-structure)
  - [Example](#example)
    - [Domain Participants](#domain-participants)
    - [Architecture](#architecture)
      - [Classes](#classes)
      - [Flow](#flow)
        - [Walkthrough Notation](#walkthrough-notation)
        - [Walkthrough](#walkthrough)

---

## Overview

This document describes the architecture of the agile_bots VS Code extension, which provides an AI-powered workflow for managing agile development artifacts (stories, epics, scenarios). The architecture prioritizes:

1. **Behavior-driven workflow** - organizing interactions by bot behaviors and actions
2. **Clean Architecture principles** - clear separation between presentation, application, domain, and infrastructure
3. **Persistent process architecture** - long-lived Python CLI for stateful command execution
4. **Domain-driven instruction generation** - actions build context-aware instructions from rules and scope

The extension uses a **persistent Python CLI process** for command execution, enabling stateful interactions with the bot's behavior/action workflow without spawning new processes for each command.

---

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────────────┐
│  PRESENTATION (Webview HTML/JavaScript)                             │
│  ───────────────────────────────────────────────────────────────    │
│  Tech: HTML, Vanilla JavaScript, CSS                                │
│  Impl: behaviors_client.js, instructions_client.js, webview HTML    │
│  Role: Render UI, capture user input (behavior/action buttons),     │
│        manage local UI state, display bot status                    │
└─────────────────────────────────────────────────────────────┬───────┘
                                                              │ vscode.postMessage
┌─────────────────────────────────────────────────────────────▼───────┐
│  INTERFACE ADAPTERS (VS Code Extension)                             │
│  ─────────────────────────────────────────────────────────────────  │
│  Tech: VS Code Extension API (Node.js)                              │
│  Impl: extension.js, bot_panel.js, behaviors_manager.js             │
│  Role: Translate webview messages ↔ CLI commands,                   │
│        manage webview lifecycle, spawn/manage Python process        │
└─────────────────────────────────────────────────────────────┬───────┘
                                                              │ stdin/stdout IPC
┌─────────────────────────────────────────────────────────────▼───────┐
│  PROCESS BOUNDARY (Persistent Python CLI)                           │
│  ─────────────────────────────────────────────────────────────────  │
│  Tech: Python subprocess (persistent), JSON communication           │
│  Impl: cli_main.py, cli_session.py                                  │
│  Role: Parse CLI commands, route to bot methods,                    │
│        serialize responses as JSON with END_MARKER                  │
└─────────────────────────────────────────────────────────────┬───────┘
                                                              │ Method calls
┌─────────────────────────────────────────────────────────────▼───────┐
│  APPLICATION (Bot Orchestration)                                    │
│  ───────────────────────                                            │
│  Tech: Plain Python classes (NO framework - intentional)            │
│  Impl: bot.py, behaviors.py, behavior.py                            │
│  Role: Orchestrate behavior/action workflow, manage state,          │
│        coordinate scope and story graph context                     │
└─────────────────────────────────────────────────────────────┬───────┘
                                                              │ Function calls
┌─────────────────────────────────────────────────────────────▼───────┐
│  DOMAIN CORE (Actions, Rules, Instructions)                         │
│  ───────────                                                        │
│  Tech: Plain Python (entity classes, business rules)                │
│  Impl: action.py, actions.py, action_context.py                     │
│  Role: Action-specific instructions (build, render, validate),      │
│        business rules enforcement, scope filtering                  │
│  Note: Actions are STATELESS - they receive context, return text    │
└─────────────────────────────────────────────────────────────┬───────┘
                                                              │ Reads from
┌─────────────────────────────────────────────────────────────▼───────┐
│  INFRASTRUCTURE (File System, Story Graph)                          │
│  ──────────────                                                     │
│  Tech: Python Pathlib, JSON, Markdown parsers                       │
│  Impl: story_graph.py, bot_path.py, scope.py                        │
│  Role: Load story graphs, read markdown files,                      │
│        traverse workspace directories, cache story data             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## File Structure

The agile_bots extension organizes code by **domain within technical layer**. Within each layer, code is grouped by domain concern—for example, `src/panel/behaviors/` contains client-side JS (webview), server-side JS (extension host), HTML templates, and CSS all together:

### Why This Structure?

| Principle | Benefit |
|-----------|--------|
| **Domain-first within layer** | All behaviors UI code lives in `src/panel/behaviors/`—client JS, manager JS, HTML, CSS. Changes to behaviors UI rarely touch other folders. |
| **Clear language boundary** | JavaScript extension code in `src/panel/`, Python CLI code at `src/` level. No mixing of concerns. |
| **Localize dependencies** | When a feature changes (e.g., behaviors panel), you edit files in one folder—not scattered across `client/`, `server/`, `styles/`. |
| **Reusable bot logic** | Python bot/behaviors/actions work standalone via CLI or can be embedded in other tools. |
| **Testable layers** | Each layer (webview, extension, CLI, bot, actions) can be tested independently. |
| **Persistent process** | Single Python process handles all commands - faster than spawning per-command. |

**Pattern (domain-first within layer):**

```
agile_bots/
├── src/
│   ├── panel/                       # VS Code Extension (Interface Adapters + Presentation)
│   │   ├── extension.js             # Extension entry point, command registration
│   │   ├── panel_view.js            # Base class: spawns Python CLI, stdin/stdout IPC
│   │   │
│   │   ├── bot/                     # Bot panel domain (ALL bot panel code together)
│   │   │   ├── bot_panel.js         # Extension host: webview lifecycle, message routing
│   │   │   └── bot_view.js          # Extension host: bot data management, CLI execution
│   │   │
│   │   ├── behaviors/               # Behaviors domain (ALL behaviors UI code together)
│   │   │   ├── behaviors_client.js  # Webview: button click handlers (runs in browser)
│   │   │   ├── behaviors_manager.js # Extension host: message routing, CLI dispatch
│   │   │   ├── behaviors_view.js    # Extension host: HTML rendering logic
│   │   │   ├── behaviors_section.html  # Template: behaviors section markup
│   │   │   └── behaviors.css        # Styles: behaviors-specific CSS
│   │   │
│   │   └── instructions/            # Instructions domain (ALL instructions UI code together)
│   │       ├── instructions_client.js  # Webview: instruction display handlers
│   │       ├── instructions_manager.js # Extension host: message routing
│   │       └── instructions.css     # Styles: instructions-specific CSS
│   │
│   ├── cli/                         # Python CLI (Process Boundary)
│   │   ├── cli_main.py              # Entry point, process loop, JSON output
│   │   └── cli_session.py           # Command parsing, verb routing to Bot
│   │
│   ├── bot/                         # Application Layer (Bot Orchestration)
│   │   ├── bot.py                   # Main Bot class, behavior/action orchestration
│   │   ├── behaviors.py             # Behaviors collection, navigation, state
│   │   └── behavior.py              # Single behavior with actions collection
│   │
│   ├── behaviors/                   # Behavior implementations
│   │   ├── behavior.py              # Base Behavior class
│   │   └── behaviors.py             # Behaviors collection manager
│   │
│   ├── actions/                     # Domain Core (Action implementations)
│   │   ├── action.py                # Base Action class, get_instructions()
│   │   ├── actions.py               # Actions collection per behavior
│   │   ├── action_context.py        # Context object passed to actions
│   │   ├── build/                   # Build action implementation
│   │   ├── render/                  # Render action implementation
│   │   ├── validate/                # Validate action implementation
│   │   └── clarify/                 # Clarify action implementation
│   │
│   ├── scope/                       # Scope filtering (Infrastructure)
│   │   └── scope.py                 # Scope entity, story/file filtering
│   │
│   ├── story_graph/                 # Story graph loading (Infrastructure)
│   │   └── story_map.py             # StoryMap, StoryNode entities
│   │
│   └── bot_path/                    # Path resolution (Infrastructure)
│       └── bot_path.py              # Workspace/bot directory resolution
│
├── base_actions/                    # Action templates (shared across bots)
│   ├── build/
│   │   ├── action_config.json       # Action metadata
│   │   └── rules.md                 # Instruction template
│   ├── render/
│   ├── validate/
│   └── clarify/
│
├── bots/                            # Bot instances
│   ├── story_bot/
│   │   ├── bot_config.json          # Bot configuration
│   │   └── behaviors.json           # Behavior definitions
│   └── architecture_bot/
│
└── docs/
    └── stories/
        └── story-graph.json         # Story hierarchy data
```

---

## Example

Story: Configure Action Execution (Skip / Combine with Next)

```gherkin
Background:
  Given Developer has VS Code open with agile_bots extension
  And Bot panel webview is displayed
  And story_bot is the active bot
  And "exploration" behavior is selected (collapsed in panel)

Scenario: User submits behavior (collapsed) and behavior has actions set to skip
  Given Behavior "exploration" has the following action settings:
    | action   | execute_mode    |
    | clarify  | skip            |
    | strategy | skip            |
    | build    | combine_next    |
    | validate | combine_next    |
    | render   | combine_next    |
  When User clicks "Submit to Chat" button
  Then Bot skips clarify action (no instructions generated)
  And Bot skips strategy action (no instructions generated)
  And Bot combines build + validate + render instructions into single block
  And Combined instructions are copied to clipboard
  And instructions are pasted to Chat automatically
```

---

### Domain Participants

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AGILE BOTS WORKFLOW DOMAIN                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────────┐         contains          ┌──────────────┐              │
│   │     Bot      │◆──────────────────────────│  Behaviors   │              │
│   │              │                            │              │              │
│   │ • name       │         manages            │ • items[]    │              │
│   │ • workspace  │◆────────┐                 │ • current    │              │
│   │ • config     │         │                 │ • navigate() │              │
│   └──────────────┘         │                 └──────────────┘              │
│          │                 │                        │                       │
│          │ creates         │                        │ contains              │
│          ▼                 │                        ▼                       │
│   ┌──────────────┐         │                 ┌──────────────┐              │
│   │ActionContext │         │                 │   Behavior   │              │
│   │              │         └────────────────▶│              │              │
│   │ • scope      │                            │ • name       │◆──────┐      │
│   │ • story_map  │                            │ • actions    │       │      │
│   │ • bot_paths  │                            │ • config     │       │      │
│   └──────────────┘                            └──────────────┘       │      │
│          │                                           │         contains     │
│          │ passed to                                 │               │      │
│          │                                           │               ▼      │
│          │                                           │        ┌──────────┐  │
│          │                                           │        │ Actions  │  │
│          │                                           └───────▶│          │  │
│          │                                                    │ • items[]│  │
│          │                                                    │ • current│  │
│          │                                                    └──────────┘  │
│          │                                                          │       │
│          │                                                          │       │
│          │                                                    contains      │
│          │                                                          │       │
│          │                                                          ▼       │
│          │                                                   ┌──────────────┐   │
│          │                                                   │  Action      │   │
│          └──────────────────────────────────────────────────▶│              │   │
│                                                              │ • name       │   │
│                                   get_instructions(context)  │ • config     │   │
│                                                              │ • order      │   │
│                                                              │ • exec_mode  │   │
│                                                              └──────────────┘   │
│                                                                    │            │
│                               exec_mode: skip | combine_next | manual          │
│                                                                    │            │
│                                                                    │ reads      │
│                                                                    ▼        │
│   ┌──────────────┐                                         ┌────────────┐   │
│   │    Scope     │                                         │   Rules    │   │
│   │              │                                         │            │   │
│   │ • type       │                                         │ • template │   │
│   │ • value      │                                         │ • format() │   │
│   │ • filter()   │                                         └────────────┘   │
│   └──────────────┘                                                          │
│          │                                                                  │
│          │ filters                                                          │
│          ▼                                                                  │
│   ┌──────────────┐         contains          ┌──────────────┐              │
│   │  StoryMap    │◆──────────────────────────│  StoryNode   │              │
│   │              │                            │              │              │
│   │ • nodes[]    │                            │ • name       │              │
│   │ • find_node()│                            │ • type       │              │
│   │ • filter()   │                            │ • children[] │              │
│   └──────────────┘                            └──────────────┘              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Concept | Module | Responsibility | Collaborators |
|---------|--------|---------------|---------------|
| **Bot** | `bot` | Orchestrates behavior/action workflow; manages current state; creates contexts | Behaviors, ActionContext, Scope, StoryMap |
| **Behaviors** | `behaviors` | Collection of Behavior instances; tracks current behavior; navigates between behaviors | Behavior |
| **Behavior** | `behavior` | Represents a workflow phase (exploration, shape, scenarios); contains Actions collection | Actions, Bot |
| **Actions** | `actions` | Collection of Action instances; tracks current action; navigates between actions | Action |
| **Action** | `action` | Stateless instruction builder; generates formatted instructions from rules + context | ActionContext, Rules, ExecuteMode |
| **ExecuteMode** | `execution_settings` | Per-action setting: `skip` (no instructions), `combine_next` (merge with following), `manual` (stop after) | Action, Bot |
| **ActionContext** | `action_context` | Carries scope, story_map, and bot_paths to actions | Scope, StoryMap, BotPath |
| **Scope** | `scope` | Filters story graph/files based on user selection; serializes to JSON | StoryMap |
| **StoryMap** | `story_graph` | Loads and traverses story graph JSON; provides node access | StoryNode |
| **StoryNode** | `story_graph` | Represents a story/epic/scenario in the graph; holds metadata | StoryMap |
| **Rules** | `base_actions/*/rules.md` | Markdown templates for action-specific instructions | Action |

---

### Architecture

#### Classes

| Class | Layer | Package | Responsibility |
|-------|-------|---------|----------------|
| **behaviors_client.js** | Presentation | `src/panel/behaviors/` | Webview JavaScript; handles button clicks; posts messages to extension |
| **BotPanel** | Interface | `src/panel/bot/` | VS Code webview manager; routes messages to managers; updates UI |
| **BehaviorsManager** | Interface | `src/panel/behaviors/` | Translates webview messages to CLI commands; handles responses |
| **PanelView** | Interface | `src/panel/` | Spawns persistent Python process; handles stdin/stdout IPC with END_MARKER |
| **CLISession** | Process Boundary | `src/cli/` | Parses CLI commands (e.g., "submit story build"); routes to Bot methods |
| **Bot** | Application | `src/bot/` | Orchestrates behavior/action navigation; builds ActionContext; calls submit_action() |
| **Behaviors** | Application | `src/bot/` | Collection managing Behavior instances with navigate_to() and current tracking |
| **Behavior** | Application | `src/bot/` | Represents workflow phase; contains Actions collection |
| **Actions** | Application | `src/actions/` | Collection managing Action instances with navigate_to() and current tracking |
| **Action** | Domain | `src/actions/` | Stateless instruction generator: get_instructions(context) → str |
| **ActionContext** | Domain | `src/actions/` | Value object carrying scope, story_map, and bot_paths to actions |
| **Scope** | Infrastructure | `src/scope/` | Filters story graph by user selection; persists scope state |
| **StoryMap** | Infrastructure | `src/story_graph/` | Loads story-graph.json; provides traversal and filtering methods |
| **BotPath** | Infrastructure | `src/bot_path/` | Resolves workspace/bot directories; handles path conventions |

#### Flow 

Example: User submits behavior (collapsed) with actions set to skip/combine_next

📊 **[View Sequence Diagram](flow-submit-behavior-skip-combine.mmd)**

##### Walkthrough Notation

```
result: <actual_value> = Object.method(param: value)
    -> nested_result: <value> = Collaborator.method()
        -> deeper: <value> = Another.method()
        return deeper: <value>
    return result: <actual_value>
```

##### Walkthrough

```
behaviors_client.js (Webview Presentation)
    # Entry point: User clicks "Submit to Chat" button in webview
    # Behavior "exploration" is collapsed (no specific action selected)
    submitToChat()
        
        # Client posts message to VS Code extension host
        -> vscode.postMessage({ command: 'sendToChat' })
        
            ─────────── MESSAGE CROSSES WEBVIEW BOUNDARY ───────────
            # MESSAGE CROSSES IPC BOUNDARY: webview -> extension host
            
                BotPanel (VS Code Extension - Interface Adapter)
                    # Extension receives message via onDidReceiveMessage handler
                    -> case "sendToChat":
                    
                        # Get current behavior from cached bot data
                        # Note: currentAction is null because behavior is collapsed
                        -> currentBehavior = this._botView.botData.behaviors.current_behavior
                           # "exploration"
                        -> currentAction = this._botView.botData.behaviors.current_action
                           # null (behavior collapsed)
                        
                        # Build CLI command - behavior only (no action specified)
                        -> submitCmd = `submit ${currentBehavior}`
                           # "submit exploration"
                        
                        # Execute via shared CLI (PanelView)
                        -> result = this._botView.execute(submitCmd)
                        
                            PanelView (Interface Adapter - Process Manager)
                                # Write command to Python process stdin
                                -> this._pythonProcess.stdin.write(submitCmd + '\n')
                                
                                ─────────── COMMAND CROSSES PROCESS BOUNDARY ───────────
                                # COMMAND CROSSES IPC BOUNDARY: Node.js -> Python
                                
                                    cli_main.py (Python CLI - Process Entry)
                                        # Read command from stdin, delegate to session
                                        -> response = cli_session.execute_command(cmd)
                                        
                                            CLISession (Process Boundary)
                                                # Parse command into verb and args
                                                -> verb, args = self._parse_command(cmd)
                                                   # verb="submit", args="exploration"
                                                
                                                # Route to submit handler
                                                -> handler = self._get_command_handler("submit")
                                                -> result = self._handle_submit(verb, args)
                                                
                                                    # Only behavior_name provided (no action)
                                                    -> behavior_name = args.strip()
                                                       # "exploration"
                                                    
                                                    # Delegate to Bot.submit_current_action()
                                                    # (behavior-level submit when no action specified)
                                                    -> result = self.bot.submit_current_action()
                                                    
                                                        Bot (Application Layer)
                                                            # Navigate to the specified behavior
                                                            -> self.behaviors.navigate_to("exploration")
                                                            -> behavior = self.behaviors.current
                                                            
                                                            # Build instructions with skip/combine_next logic
                                                            -> instructions, last_appended = self._build_instructions_with_combine(
                                                                   behavior_name=None, action_name=None, scope=None)
                                                            
                                                                # Check execution mode for current action (clarify)
                                                                -> execution_mode: 'skip' = self.get_execution_mode(behavior_name: 'exploration', action_name: 'clarify')
                                                                    # Read from logs/execution_settings.json
                                                                    -> path: Path = self.workspace_directory / 'logs' / 'execution_settings.json'
                                                                    -> data: {...} = json.loads(path.read_text())
                                                                    -> key: 'story_bot.exploration.clarify' = f"{self.bot_name}.{behavior_name}.{action_name}"
                                                                    -> mode: 'skip' = data.get(key, 'manual')
                                                                    return execution_mode: 'skip'
                                                                
                                                                # Skip logic: loop to find first non-skip action
                                                                # (execution_mode == 'skip' triggers while loop)
                                                                -> action_names: ['clarify', 'strategy', 'build', 'validate', 'render'] = behavior.action_names
                                                                -> idx: 0 = action_names.index('clarify')
                                                                
                                                                # while idx + 1 < len(action_names):
                                                                #   idx: 1 -> next_name: 'strategy'
                                                                -> next_mode: 'skip' = self.get_execution_mode('exploration', 'strategy')
                                                                    -> key: 'story_bot.exploration.strategy' = f"{self.bot_name}.exploration.strategy"
                                                                    -> mode: 'skip' = data.get(key, 'manual')
                                                                    return next_mode: 'skip'
                                                                # 'strategy' is also skip, continue loop
                                                                
                                                                #   idx: 2 -> next_name: 'build'
                                                                -> next_mode: 'combine_next' = self.get_execution_mode('exploration', 'build')
                                                                    -> key: 'story_bot.exploration.build' = f"{self.bot_name}.exploration.build"
                                                                    -> mode: 'combine_next' = data.get(key, 'manual')
                                                                    return next_mode: 'combine_next'
                                                                # 'build' is not skip - break loop and navigate
                                                                
                                                                -> behavior.actions.navigate_to('build')
                                                                -> self.behaviors.save_state()
                                                                -> action: <Action 'build'> = behavior.actions.current
                                                                -> current_action_name: 'build' = action.action_name
                                                                
                                                                # Create context for build action
                                                                -> context: <ActionContext> = action.context_class()
                                                                -> self._scope.load()
                                                                -> context.scope: <Scope> = self._scope
                                                                
                                                                # Now build instructions starting from 'build' with combine_next
                                                                -> built: (instructions, last_appended) = self._build_instructions_with_combine(
                                                                       behavior_name: 'exploration', action_name: 'build', scope: None)
                                                                    
                                                                    # Get build action instructions
                                                                    -> instructions: <MarkdownInstructions> = action.get_instructions(context, include_scope: True)
                                                                    
                                                                        Action (Domain Core)
                                                                            -> template: '...' = self._load_rules_template()
                                                                            -> formatted: '...' = self._context_data_injector.inject(template, context)
                                                                            return instructions: <MarkdownInstructions>
                                                                    
                                                                    # execution_mode is 'combine_next' - append next actions
                                                                    -> last_appended: 'render' = self._append_next_action_instructions_if_combine_next(
                                                                           behavior, 'exploration', 'build', action, instructions)
                                                                        
                                                                        # Loop through remaining actions
                                                                        #   idx: 2 ('build'), check idx+1: 'validate'
                                                                        -> next_mode: 'combine_next' = self.get_execution_mode('exploration', 'validate')
                                                                        -> next_action: <Action 'validate'> = behavior.actions.find_by_name('validate')
                                                                        # First append - add header
                                                                        -> instructions._display_content.insert(0, '**Combined instructions:** ...')
                                                                        -> next_instructions: '...' = next_action.get_instructions(None, include_scope: False)
                                                                        -> instructions.add_display('---', '## Next action: validate', ...)
                                                                        -> last_appended: 'validate' = 'validate'
                                                                        
                                                                        #   idx: 3 ('validate'), check idx+1: 'render'
                                                                        -> next_mode: 'combine_next' = self.get_execution_mode('exploration', 'render')
                                                                        -> next_action: <Action 'render'> = behavior.actions.find_by_name('render')
                                                                        -> next_instructions: '...' = next_action.get_instructions(None, include_scope: False)
                                                                        -> instructions.add_display('---', '## Next action: render', ...)
                                                                        -> last_appended: 'render' = 'render'
                                                                        
                                                                        #   idx: 4 ('render'), idx+1 >= len - exit loop
                                                                        return last_appended: 'render'
                                                                    
                                                                    # Result: build + validate + render combined
                                                                    # Skipped: clarify, strategy (never processed)
                                                                    return (instructions: <MarkdownInstructions>, last_appended: 'render')
                                                            
                                                            # Submit combined instructions (copy to clipboard)
                                                            -> result = self.submit_instructions(
                                                                   instructions, behavior.name, last_appended)
                                                            
                                                                # Copy to system clipboard
                                                                -> pyperclip.copy(instructions)
                                                                
                                                                # Return success result with skip/run info
                                                                return {
                                                                    'status': 'success',
                                                                    'behavior': 'exploration',
                                                                    'action': 'render',  # last_appended
                                                                    'actions_run': ['build', 'validate', 'render'],
                                                                    'actions_skipped': ['clarify', 'strategy'],
                                                                    'instructions_length': len(instructions),
                                                                    'clipboard_status': 'copied'
                                                                }
                                                            
                                                            # Save state with last executed action
                                                            -> self.behaviors.save_state()
                                                            
                                                            return result
                                                    
                                                    return result
                                                
                                                # Format response as JSON
                                                -> return CLICommandResponse(output=json.dumps(result))
                                        
                                        # Write JSON response + END_MARKER to stdout
                                        -> sys.stdout.write(json_response + '\n<<<END_OF_RESPONSE>>>\n')
                                        -> sys.stdout.flush()
                                
                                ─────────────────────────────────────────────────────────────────
                                # RESPONSE CROSSES PROCESS BOUNDARY: Python -> Node.js
                                
                                # PanelView accumulates stdout until END_MARKER
                                -> this._responseBuffer += chunk
                                -> if (buffer.includes('<<<END_OF_RESPONSE>>>'))
                                    -> json = buffer.split('<<<END_OF_RESPONSE>>>')[0]
                                    -> parsed = JSON.parse(json)
                                    -> this._pendingResolve(parsed)
                                
                                return parsed
                        
                        # Handle result in extension
                        -> if (result.status === 'success')
                            -> vscode.window.showInformationMessage('Instructions submitted to chat!')
                            # Result includes:
                            #   actions_run: ['build', 'validate', 'render']
                            #   actions_skipped: ['clarify', 'strategy']
                        
            ─────────────────────────────────────────────────────────────────
            # UI UPDATE CROSSES BACK TO WEBVIEW
            
        # User sees success notification
        # Combined instructions (build + validate + render) are in clipboard and pasted in Chat
        # Clarify and strategy were skipped (no instructions generated)
```
