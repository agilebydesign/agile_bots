# Panel Domain Refactoring Plan

**Date**: 2026-01-10  
**Status**: Planning  
**Approach**: Domain-oriented panel views matching CLI adapter pattern

---

## Executive Summary

Refactor panel JavaScript/HTML code to follow the same domain-oriented architecture as the CLI adapters. Each domain folder contains its own panel view that handles JSON round-trip communication with the new CLI in JSON mode, HTML rendering, and event handling.

**Key Principle**: Panel views live in domain folders (`src/<domain>/<domain>_view.js`), not in a separate `panel/` folder. Only base classes remain in `panel/`.

**Visual Mapping Requirement**: All panel views must render HTML that exactly matches the screenshots in `agile_bot/docs/panel/invoke-bot-panel-screens.md`. Tests must use hard-coded HTML verification (like CLI tests) to ensure exact UI structure matches the visual specifications.

---

## Current State Analysis

### Legacy Panel Structure
```
agile_bot/legacy/src/display_panel/extension/
├── status_panel.js          # Main panel controller (singleton)
├── status_data_provider.js  # CLI communication layer
├── cli_output_adapter.js    # Parses CLI output to JSON
├── html_renderer.js         # Renders HTML from structured data
├── status_parser.js         # Legacy parsing logic
└── extension.js             # VS Code extension entry point
```

### New Domain-Oriented Structure (Target)
```
agile_bot/src/
├── panel/
│   └── panel_view.js        # Base class ONLY (no domain logic)
├── bot/
│   ├── bot.py
│   ├── json_bot.py
│   ├── tty_bot.py
│   ├── markdown_bot.py
│   └── bot_view.js          # Main panel orchestrator
├── behaviors/
│   ├── behavior.py
│   ├── json_behavior.py
│   ├── tty_behavior.py
│   ├── markdown_behavior.py
│   └── behaviors_view.js    # Behaviors section view
├── scope/
│   ├── scope.py
│   ├── json_scope.py
│   ├── tty_scope.py
│   ├── markdown_scope.py
│   └── scope_view.js        # Scope section view
└── ... (other domains)
```

---

## Architecture Pattern

### Domain View Pattern (Following Status Example)

Each domain view follows this pattern:

```javascript
// src/<domain>/<domain>_view.js
const PanelView = require('../panel/panel_view');

class <Domain>View extends PanelView {
    constructor(<domain>JSON, cli) {
        super(cli);
        this.<domain>Data = <domain>JSON;
    }
    
    /**
     * Render domain JSON to HTML.
     * @returns {string} HTML string
     */
    render() {
        // Extract data from this.<domain>Data
        // Return HTML string
    }
    
    /**
     * Handle user events (clicks, input, etc.).
     * @param {string} eventType - Type of event
     * @param {Object} eventData - Event data
     */
    async handleEvent(eventType, eventData) {
        // Send command to CLI via this.cli
        // Update local state
        // Return updated JSON or trigger re-render
    }
    
    /**
     * Refresh data from CLI.
     * @returns {Promise<Object>} Updated domain JSON
     */
    async refresh() {
        const command = this.getRefreshCommand(); // e.g., 'status', 'scope'
        const jsonData = await this.cli.execute(command);
        this.<domain>Data = jsonData;
        return jsonData;
    }
    
    /**
     * Get CLI command for refreshing this domain.
     * @returns {string} CLI command
     */
    getRefreshCommand() {
        return '<domain>'; // Override in subclasses
    }
}
```

### CLI Communication Pattern

All panel views communicate with CLI via JSON mode (piped stdin/stdout):

```javascript
// In PanelView base class (already implemented)
async execute(command) {
    // Spawn Python CLI subprocess
    // Send command via stdin
    // Parse JSON from stdout
    // Return parsed JSON object
}
```

**CLI Command Format**:
- Commands sent as plain strings: `"status"`, `"scope"`, etc.
- CLI detects piped mode (`not sys.stdin.isatty()`) and outputs JSON
- JSON matches domain adapter output (e.g., `JSONBot.to_dict()`)
- **Important**: The `status` command returns the Bot object itself (see `cli_session.py` line 66-67), so `"status"` and the bot JSON are the same thing

---

## Implementation Plan

### Phase 1: Update PanelView Base Class

**Goal**: Ensure base class supports domain-oriented pattern

**Location**: `agile_bot/src/panel/panel_view.js`

**Changes**:
1. ✅ Already has `execute(command)` method for CLI communication
2. ✅ Already has `getElementId()` for unique DOM IDs
3. Add helper method for spawning CLI subprocess:
   ```javascript
   spawnCLI() {
       const cliPath = path.join(__dirname, '../cli/cli_main.py');
       this.pythonProcess = spawn('python', [cliPath], {
           cwd: this.workspaceDirectory
       });
       return this.pythonProcess;
   }
   ```
4. Add workspace directory to constructor:
   ```javascript
   constructor(cli, workspaceDirectory) {
       this.cli = cli;
       this.workspaceDirectory = workspaceDirectory;
   }
   ```

**Verification**:
- [ ] Base class supports domain view pattern
- [ ] CLI communication works in JSON mode
- [ ] Workspace directory is properly passed

---

### Phase 2: Create Bot Domain View (Main Orchestrator)

**Goal**: Create main panel controller that orchestrates all domain views

**Location**: `agile_bot/src/bot/bot_view.js`

**Responsibilities** (from CRC model):
- Wraps bot JSON
- Displays BotHeaderView
- Displays PathsSection
- Displays BehaviorsView
- Displays ScopeSection
- Displays InstructionsSection

**Implementation**:

```javascript
// src/bot/bot_view.js
const PanelView = require('../panel/panel_view');
const BotHeaderView = require('./bot_header_view');
const PathsSection = require('./paths_section');
const BehaviorsView = require('../behaviors/behaviors_view');
const ScopeSection = require('../scope/scope_view');
const InstructionsSection = require('../instructions/instructions_view');

class BotView extends PanelView {
    constructor(botJSON, cli, workspaceDirectory) {
        super(cli, workspaceDirectory);
        this.botData = botJSON;
        
        // Initialize domain views
        this.headerView = new BotHeaderView(botJSON, cli, workspaceDirectory);
        this.pathsSection = new PathsSection(botJSON.paths, cli, workspaceDirectory);
        this.behaviorsView = new BehaviorsView(botJSON.behaviors, cli, workspaceDirectory);
        this.scopeSection = new ScopeSection(botJSON.scope, cli, workspaceDirectory);
        this.instructionsSection = new InstructionsSection(
            botJSON.instructions, 
            botJSON.current_action,
            cli, 
            workspaceDirectory
        );
    }
    
    render() {
        return `
            <div class="bot-view">
                ${this.headerView.render()}
                ${this.pathsSection.render()}
                ${this.behaviorsView.render()}
                ${this.scopeSection.render()}
                ${this.instructionsSection.render()}
            </div>
        `;
    }
    
    async refresh() {
        // "status" command returns the Bot object itself
        const botJSON = await this.cli.execute('status');
        // Update all domain views with new data
        this.headerView.update(botJSON);
        this.pathsSection.update(botJSON.bot_paths || botJSON);
        this.behaviorsView.update(botJSON.behaviors);
        this.scopeSection.update(botJSON.scope);
        this.instructionsSection.update(botJSON.instructions, botJSON.current_action);
        return botJSON;
    }
    
    async handleEvent(eventType, eventData) {
        // Route events to appropriate domain view
        switch (eventType) {
            case 'refresh':
                return await this.refresh();
            case 'executeBehavior':
                return await this.behaviorsView.handleEvent('execute', eventData);
            case 'updateScope':
                return await this.scopeSection.handleEvent('updateFilter', eventData);
            // ... other events
        }
    }
}

module.exports = BotView;
```

**Migration from Legacy**:
- `status_panel.js` → `bot_view.js` (main orchestrator)
- `status_data_provider.js` → Use `PanelView.execute()` directly
- `cli_output_adapter.js` → Not needed (CLI outputs JSON directly)
- `html_renderer.js` → Split into domain views

**Note**: The `status` command returns the Bot object itself (see `cli_session.py` line 66-67), not a separate Status domain. All status information (current_behavior, progress_path, etc.) is part of the Bot JSON structure.

**Verification**:
- [ ] BotView orchestrates all domain views
- [ ] Refresh works end-to-end
- [ ] Events route to correct domain views
- [ ] Bot JSON contains all status information (no separate Status domain)

---

### Phase 3: Create Domain Section Views

**Goal**: Create panel views for each domain that needs UI representation

**Domains to Implement** (in priority order):

#### 3.1 BotHeaderView
**Location**: `agile_bot/src/bot/bot_header_view.js`

**Responsibilities** (from CRC model):
- Displays image
- Displays title
- Displays version number
- Refreshes panel

**Migration**: Extract from `html_renderer.js` header section

#### 3.2 PathsSection
**Location**: `agile_bot/src/bot/paths_section.js`

**Responsibilities** (from CRC model):
- Displays bot directory
- Edits workspace directory
- Displays available bots

**Migration**: Extract from `html_renderer.js` paths section

#### 3.3 BehaviorsView
**Location**: `agile_bot/src/behaviors/behaviors_view.js`

**Responsibilities** (from CRC model):
- Displays behavior names list
- Navigates to behavior
- Toggles collapsed
- Displays tooltip
- Displays actions
- Executes behavior
- Displays completion progress
- Displays navigation

**Migration**: Extract from `html_renderer.js` behaviors section

#### 3.4 ScopeSection
**Location**: `agile_bot/src/scope/scope_view.js`

**Responsibilities** (from CRC model):
- Displays filtered files
- Filters story graph
- Filters files
- Clears filter
- Displays story graph

**Migration**: Extract from `html_renderer.js` scope section

#### 3.5 InstructionsSection
**Location**: `agile_bot/src/instructions/instructions_view.js`

**Responsibilities** (from CRC model):
- Wraps instructions JSON
- Wraps action JSON
- Displays base instructions subsection
- Displays raw format subsection
- Submits to AI chat

**Migration**: Extract from `html_renderer.js` instructions section

**Action-Specific Subclasses**:
- `ClarifyInstructionsSection` (from CRC model)
- `StrategyInstructionsSection`
- `BuildInstructionsSection`
- `ValidateInstructionsSection`
- `RenderInstructionsSection`

---

### Phase 4: Update VS Code Extension Entry Point

**Goal**: Update extension to use new domain-oriented views

**Location**: `agile_bot/src/panel/extension.js` (NEW FILE)

**Implementation**:

```javascript
// src/panel/extension.js
const vscode = require('vscode');
const path = require('path');
const BotView = require('../bot/bot_view');
const PanelView = require('./panel_view');

class CLIClient extends PanelView {
    constructor(workspaceDirectory) {
        super(null, workspaceDirectory);
        this.workspaceDirectory = workspaceDirectory;
    }
    
    async execute(command) {
        // Spawn CLI subprocess
        this.spawnCLI();
        
        // Send command
        this.sendCommand(command);
        
        // Receive JSON
        return await this.receiveJSON();
    }
}

let currentPanel = undefined;

function activate(context) {
    const command = vscode.commands.registerCommand('agilebot.viewPanel', () => {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot) {
            vscode.window.showErrorMessage('No workspace folder open');
            return;
        }
        
        const column = vscode.ViewColumn.Two;
        
        if (currentPanel) {
            currentPanel.reveal(column);
            return;
        }
        
        const panel = vscode.window.createWebviewPanel(
            'agilebot.botPanel',
            'Bot Status Dashboard',
            column,
            {
                enableScripts: true,
                retainContextWhenHidden: false
            }
        );
        
        // Create CLI client
        const cli = new CLIClient(workspaceRoot);
        
        // Initialize BotView
        async function updatePanel() {
            try {
                // "status" command returns the Bot object itself
                const botJSON = await cli.execute('status');
                const botView = new BotView(botJSON, cli, workspaceRoot);
                
                // Handle webview messages
                panel.webview.onDidReceiveMessage(async (message) => {
                    const result = await botView.handleEvent(message.command, message.data);
                    if (result) {
                        updatePanel(); // Refresh after event
                    }
                });
                
                panel.webview.html = botView.render();
            } catch (error) {
                panel.webview.html = `<html><body>Error: ${error.message}</body></html>`;
            }
        }
        
        updatePanel();
        
        panel.onDidDispose(() => {
            currentPanel = undefined;
        });
        
        currentPanel = panel;
    });
    
    context.subscriptions.push(command);
}

function deactivate() {}

module.exports = { activate, deactivate };
```

**Migration**: 
- `legacy/src/display_panel/extension/extension.js` → `src/panel/extension.js`
- Remove dependency on `status_panel.js`, `status_data_provider.js`, `cli_output_adapter.js`

---

### Phase 5: Create JavaScript Tests

**Goal**: Create comprehensive tests for panel views using given-when-then format

**Test Framework**: Node.js built-in `node:test` module (matches existing `test_invoke_bot_through_panel.js`)

**Test Structure** (class-based with given-when-then):

**CRITICAL: Follow ALL Test Rules from `agile_bot/bots/story_bot/behaviors/tests/rules/`:**

1. **Test File Naming**: Files named after sub-epics (from story-graph.json `test_file`):
   - `test_manage_panel_session.js` (Sub-epic: Manage Panel Session)
   - `test_navigate_and_execute.js` (Sub-epic: Navigate And Execute Behaviors Through Panel)
   - `test_manage_scope.js` (Sub-epic: Manage Scope Through Panel)
   - `test_display_instructions.js` (Sub-epic: Display Action Instructions Through Panel)

2. **Test Class Naming**: Classes match EXACT story names from story-graph.json `test_class`:
   - `TestOpenPanel`, `TestDisplaySessionStatus`, `TestChangeWorkspacePath`, `TestSwitchBot`, `TestTogglePanelSection`
   - `TestDisplayHierarchy`, `TestNavigateBehaviorAction`, `TestExecuteBehaviorAction`
   - `TestDisplayStoryScopeHierarchy`, `TestFilterStoryScope`
   - `TestDisplayClarifyInstructions`, `TestDisplayStrategyInstructions`, etc.

3. **Test Method Naming**: Methods match EXACT scenario `test_method` from story-graph.json:
   - `test_user_opens_panel_via_command_palette_happy_path`
   - `test_panel_displays_behavior_tree_with_progress_indicators`
   - `test_user_filters_scope_by_story_name`

4. **Exact Language from story-graph.json**:
   - Scenario titles in JSDoc comments must match `scenario.title` exactly
   - Given-When-Then steps in JSDoc comments must match `scenario.steps` exactly
   - Test code comments must use the exact step language from story-graph.json

5. **Orchestrator Pattern**: Test methods show Given-When-Then flow (under 20 lines), helpers do the work

6. **Given-When-Then Helpers**: Extract setup/action/assertion to reusable helpers:
   - `given_bot_at_behavior_action(workspacePath, botDir, behaviorName, actionName)`
   - `when_panel_renders(botJSON, workspacePath)`
   - `then_panel_displays_bot_name(html, expectedName)`

7. **ASCII-Only**: No Unicode characters in test code (use `[PASS]`, `[ERROR]`, `->` instead of checkmarks/arrows)

8. **Exact Variable Names**: Use exact variable names from story-graph.json scenarios

9. **Call Production Code Directly**: Use real CLI, real views, no mocks (except external boundaries)

10. **Test Observable Behavior**: Assert on HTML output, not implementation details

11. **Match Specification Scenarios Exactly**: Test names, steps, and assertions verify exactly what scenario states

12. **Hard-Coded HTML Verification**: Use comprehensive regex patterns to verify exact HTML structure, CSS classes, data attributes, event handlers, element order, text content

This ensures tests are traceable back to user stories and scenarios, and follow all established test rules.

```javascript
// test/panel/test_manage_panel_session.js
// Sub-epic: Manage Panel Session
// Stories: Open Panel, Display Session Status, Change Workspace Path, Switch Bot, Toggle Panel Section

const { test } = require('node:test');
const assert = require('assert');
const { spawn } = require('child_process');
const path = require('path');
const BotView = require('../src/bot/bot_view');

function spawnCLI(workspacePath, botDirectory) {
    const cliScript = path.join(__dirname, '../src/cli/cli_main.py');
    const env = {
        ...process.env,
        PYTHONPATH: path.join(__dirname, '../../..'),
        BOT_DIRECTORY: botDirectory,
        WORKING_AREA: workspacePath
    };
    
    const pythonProcess = spawn('python', [cliScript], {
        cwd: workspacePath,
        env: env,
        stdio: ['pipe', 'pipe', 'pipe']
    });
    
    return pythonProcess;
}

function sendCommand(process, command) {
    return new Promise((resolve, reject) => {
        let buffer = '';
        let errorBuffer = '';
        const timeout = setTimeout(() => {
            reject(new Error(`Timeout waiting for JSON response. Received: ${buffer}, Errors: ${errorBuffer}`));
        }, 5000);
        
        const stdoutHandler = (data) => {
            buffer += data.toString();
            try {
                const jsonData = JSON.parse(buffer.trim());
                clearTimeout(timeout);
                process.stdout.removeListener('data', stdoutHandler);
                process.stderr.removeListener('data', stderrHandler);
                resolve(jsonData);
            } catch (e) {
            }
        };
        
        const stderrHandler = (data) => {
            errorBuffer += data.toString();
        };
        
        process.stdout.on('data', stdoutHandler);
        process.stderr.on('data', stderrHandler);
        
        process.stdin.write(command + '\n');
        process.stdin.end();
    });
}

test('TestOpenPanel', { concurrency: false }, async (t) => {
    
    await t.test('test_user_opens_panel_via_command_palette_happy_path', async () => {
        /**
         * SCENARIO: User opens panel via command palette
         * Story: Open Panel
         * Steps from story-graph.json:
         *   Given VS Code workspace with bot installed
         *   When User executes 'Open Status Panel' command
         *   Then Panel webview appears
         *   And Panel displays bot name
         *   And Panel displays workspace path
         *   And Panel displays behavior action section
         *   And Panel displays scope section
         *   And Panel displays instructions section
         */
        const tmpPath = path.join(__dirname, '../../demo/mob_minion');
        const botDir = path.join(__dirname, '../bots/story_bot');
        
        const pythonProcess = spawnCLI(tmpPath, botDir);
        
        try {
            // Given VS Code workspace with bot installed
            const botJSON = await sendCommand(pythonProcess, 'status');
            
            // When User executes 'Open Status Panel' command (BotView renders)
            const botView = new BotView(botJSON, tmpPath);
            const html = botView.render();
            
            // Then Panel webview appears (HTML is generated)
            assert(typeof html === 'string');
            assert(html.length > 0);
            
            // And Panel displays bot name
            assert(html.includes(botJSON.name));
            
            // And Panel displays workspace path
            assert(/workspace|workspacePath|workspace.*path/i.test(html));
            
            // And Panel displays behavior action section
            assert(/<div[^>]*class="[^"]*behaviors-section[^"]*"[^>]*>/.test(html));
            assert(/<div[^>]*class="[^"]*collapsible-section[^"]*"[^>]*>/.test(html));
            assert(/<div[^>]*class="[^"]*collapsible-header[^"]*"[^>]*onclick="toggleSection\('behaviors-content'\)"[^>]*>/.test(html));
            assert(html.includes('Behavior Action Status'));
            assert(html.includes('id="behaviors-content"'));
            
            // And Panel displays scope section
            assert(/<div[^>]*class="[^"]*scope-section[^"]*"[^>]*>/.test(html));
            assert(/<div[^>]*class="[^"]*collapsible-header[^"]*"[^>]*onclick="toggleSection\('scope-content'\)"[^>]*>/.test(html));
            assert(html.includes('Scope'));
            assert(html.includes('id="scope-content"'));
            
            // And Panel displays instructions section
            assert(/<div[^>]*class="[^"]*instructions-section[^"]*"[^>]*>/.test(html));
            assert(/<div[^>]*class="[^"]*collapsible-header[^"]*"[^>]*onclick="toggleSection\('instructions-content'\)"[^>]*>/.test(html));
            assert(html.includes('Instructions'));
            assert(html.includes('id="instructions-content"'));
        } finally {
            pythonProcess.kill();
        }
    });
    
    await t.test('test_user_refreshes_panel_to_see_updated_status', async () => {
        /**
         * SCENARIO: User refreshes panel to see updated status
         * Story: Display Session Status
         * Steps from story-graph.json:
         *   Given Panel is open displaying current bot status
         *   And Bot state has changed since panel was opened
         *   When User clicks refresh button
         *   Then Panel displays updated bot name
         *   And Panel displays updated workspace path
         *   And Panel displays updated behavior action section
         *   And Panel displays updated scope
         *   And Panel displays updated instructions
         */
        const tmpPath = path.join(__dirname, '../../demo/mob_minion');
        const botDir = path.join(__dirname, '../bots/story_bot');
        
        const pythonProcess1 = spawnCLI(tmpPath, botDir);
        
        try {
            // Given Panel is open displaying current bot status
            const initialBotJSON = await sendCommand(pythonProcess1, 'status');
            const botView = new BotView(initialBotJSON, tmpPath);
            const initialHtml = botView.render();
            
            pythonProcess1.kill();
            
            // And Bot state has changed since panel was opened (simulated by getting fresh status)
            // When User clicks refresh button (refresh() is called)
            const pythonProcess2 = spawnCLI(tmpPath, botDir);
            const updatedBotJSON = await sendCommand(pythonProcess2, 'status');
            pythonProcess2.kill();
            
            botView.update(updatedBotJSON);
            const updatedHtml = botView.render();
            
            // Then Panel displays updated bot name
            assert(updatedHtml.includes(updatedBotJSON.name));
            
            // And Panel displays updated workspace path
            assert(/workspace|workspacePath|workspace.*path/i.test(updatedHtml));
            
            // And Panel displays updated behavior action section
            assert(/<div[^>]*class="[^"]*behaviors-section[^"]*"[^>]*>/.test(updatedHtml));
            
            // And Panel displays updated scope
            assert(/<div[^>]*class="[^"]*scope-section[^"]*"[^>]*>/.test(updatedHtml));
            
            // And Panel displays updated instructions
            assert(/<div[^>]*class="[^"]*instructions-section[^"]*"[^>]*>/.test(updatedHtml));
        } finally {
            pythonProcess1.kill();
        }
    });
    
    await t.test('test_user_views_session_status_on_panel_load', async () => {
        /**
         * SCENARIO: User views session status on panel load
         * Story: Display Session Status
         * Steps from story-graph.json:
         *   Given Bot is at behavior shape and action clarify
         *   When Panel opens
         *   Then Panel displays current bot name
         *   And Panel displays current workspace path
         *   And Panel displays shape.clarify as current action
         */
        const tmpPath = path.join(__dirname, '../../demo/mob_minion');
        const botDir = path.join(__dirname, '../bots/story_bot');
        
        const pythonProcess = spawnCLI(tmpPath, botDir);
        
        try {
            // Given Bot is at behavior shape and action clarify
            await sendCommand(pythonProcess, 'shape.clarify');
            pythonProcess.kill();
            
            const statusProcess = spawnCLI(tmpPath, botDir);
            const botJSON = await sendCommand(statusProcess, 'status');
            statusProcess.kill();
            
            // When Panel opens
            const botView = new BotView(botJSON, tmpPath);
            const html = botView.render();
            
            // Then Panel displays current bot name
            assert(html.includes(botJSON.name));
            
            // And Panel displays current workspace path
            assert(/workspace|workspacePath|workspace.*path/i.test(html));
            
            // And Panel displays shape.clarify as current action
            assert(html.includes('shape.clarify') || html.includes('shape') && html.includes('clarify'));
        } finally {
            pythonProcess.kill();
        }
    });
});
```

**Test Files to Create** (matching story-graph.json sub-epic structure):

1. `test/panel/test_manage_panel_session.js` - Sub-epic: Manage Panel Session
   - Story: Open Panel (TestOpenPanel)
   - Story: Display Session Status (TestDisplaySessionStatus)
   - Story: Change Workspace Path (TestChangeWorkspacePath)
   - Story: Switch Bot (TestSwitchBot)
   - Story: Toggle Panel Section (TestTogglePanelSection)
   - Hard-coded HTML verification matching screenshot layout
   
2. `test/panel/test_navigate_and_execute.js` - Sub-epic: Navigate And Execute Behaviors Through Panel
   - Story: Display Hierarchy (TestDisplayHierarchy)
   - Story: Navigate Behavior Action (TestNavigateBehaviorAction)
   - Story: Execute Behavior Action (TestExecuteBehaviorAction)
   - Verify behavior tree structure, action list, navigation buttons
   
3. `test/panel/test_manage_scope.js` - Sub-epic: Manage Scope Through Panel
   - Story: Display Story Scope Hierarchy (TestDisplayStoryScopeHierarchy)
   - Story: Filter Story Scope (TestFilterStoryScope)
   - Verify filter input, story graph tree, file list
   
4. `test/panel/test_display_instructions.js` - Sub-epic: Display Action Instructions Through Panel
   - Story: Display Clarify Instructions (TestDisplayClarifyInstructions)
   - Story: Display Strategy Instructions (TestDisplayStrategyInstructions)
   - Story: Display Build Instructions (TestDisplayBuildInstructions)
   - Story: Display Validate Instructions (TestDisplayValidateInstructions)
   - Story: Display Render Instructions (TestDisplayRenderInstructions)
   - Verify action-specific instruction sections, raw format toggle, submit button

**Hard-Coded HTML Verification Pattern**:

Each test must verify exact HTML structure using hard-coded expectations (like CLI tests). Uses Node.js `assert` module with regex patterns:

```javascript
// test/panel/test_navigate_and_execute.js
// Sub-epic: Navigate And Execute Behaviors Through Panel
// Stories: Display Hierarchy, Navigate Behavior Action, Execute Behavior Action

const { test } = require('node:test');
const assert = require('assert');
const { spawn } = require('child_process');
const path = require('path');
const BehaviorsView = require('../src/behaviors/behaviors_view');

// Helper functions (same as test_bot_view.js)
function spawnCLI(workspacePath, botDirectory) { /* ... */ }
function sendCommand(process, command) { /* ... */ }

test('TestDisplayHierarchy', { concurrency: false }, async (t) => {
    
    await t.test('test_panel_displays_behavior_tree_with_progress_indicators', async () => {
        /**
         * SCENARIO: Panel displays behavior tree with progress indicators
         * Story: Display Hierarchy
         * Steps from story-graph.json:
         *   Given Bot has multiple behaviors with completed and pending actions
         *   And Bot is currently at shape.clarify
         *   When Panel renders hierarchy section
         *   Then User sees behavior names (shape, discovery)
         *   And User sees action names under behaviors
         *   And Current action (clarify) shows in-progress indicator
         *   And Completed actions show checkmark indicator
         *   And Pending actions show empty indicator
         */
        const tmpPath = path.join(__dirname, '../../demo/mob_minion');
        const botDir = path.join(__dirname, '../bots/story_bot');
        
        const pythonProcess = spawnCLI(tmpPath, botDir);
        
        try {
            // Given Bot has multiple behaviors with completed and pending actions
            // And Bot is currently at shape.clarify
            await sendCommand(pythonProcess, 'shape.clarify');
            pythonProcess.kill();
            
            const statusProcess = spawnCLI(tmpPath, botDir);
            const botJSON = await sendCommand(statusProcess, 'status');
            statusProcess.kill();
            
            const behaviorsJSON = botJSON.behaviors;
            
            // When Panel renders hierarchy section
            const view = new BehaviorsView(behaviorsJSON, tmpPath);
            const html = view.render();
    
            // Then User sees behavior names (shape, discovery)
            assert(html.includes('shape'));
            // Check for discovery if it exists in behaviors
            if (behaviorsJSON.some(b => b.name === 'discovery')) {
                assert(html.includes('discovery'));
            }
            
            // And User sees action names under behaviors
            // Verify actions are nested under behaviors in HTML structure
            assert(/<div[^>]*class="[^"]*action-item[^"]*"[^>]*>/.test(html));
            
            // And Current action (clarify) shows in-progress indicator
            assert(/(<img[^>]*alt="Current"[^>]*>|<span[^>]*class="[^"]*status-marker[^"]*marker-current[^"]*"[^>]*>➤<\/span>)/.test(html));
            assert(html.includes('clarify'));
            
            // And Completed actions show checkmark indicator
            assert(/(<img[^>]*alt="Completed"[^>]*>|<span[^>]*class="[^"]*status-marker[^"]*marker-completed[^"]*"[^>]*>☑<\/span>)/.test(html));
            
            // And Pending actions show empty indicator
            assert(/(<img[^>]*alt="Pending"[^>]*>|<span[^>]*class="[^"]*status-marker[^"]*marker-pending[^"]*"[^>]*>☐<\/span>)/.test(html));
            
            // Verify comprehensive HTML structure matching screenshot 2
            // Section header with icon and expand/collapse functionality
            assert(/<span[^>]*class="[^"]*expand-icon[^"]*"[^>]*>▸<\/span>/.test(html));
            assert(html.includes('id="behaviors-content"'));
            assert(/<div[^>]*id="behaviors-content"[^>]*class="[^"]*collapsible-content[^"]*"[^>]*style="[^"]*max-height:[^"]*"[^>]*>/.test(html));
            
            // Behavior items with proper structure
            assert(/<div[^>]*class="[^"]*collapsible-header[^"]*card-item[^"]*"[^>]*>/.test(html));
            
            // Current behavior (shape) - verify marker, classes, and event handlers
            const shapeBehaviorRegex = /<div[^>]*class="[^"]*collapsible-header[^"]*card-item[^"]*active[^"]*"[^>]*title="[^"]*"[^>]*>[\s\S]*?<span[^>]*id="behavior-0-icon"[^>]*class="[^"]*"[^>]*onclick="toggleCollapse\('behavior-0'\)"[^>]*data-plus="[^"]*"[^>]*data-subtract="[^"]*"[^>]*>[\s\S]*?<span[^>]*style="[^"]*cursor:[^"]*pointer[^"]*text-decoration:[^"]*underline[^"]*"[^>]*onclick="navigateToBehavior\('shape'\)"[^>]*>[\s\S]*?shape[\s\S]*?<\/span>/;
            assert(shapeBehaviorRegex.test(html));
            
            // Behavior expansion icon with data attributes
            assert(/<span[^>]*id="behavior-0-icon"[^>]*onclick="toggleCollapse\('behavior-0'\)"[^>]*data-plus="[^"]*"[^>]*data-subtract="[^"]*"[^>]*>/.test(html));
            
            // Behavior name with navigation handler
            assert(/<span[^>]*onclick="navigateToBehavior\('shape'\)"[^>]*>[\s\S]*?shape[\s\S]*?<\/span>/.test(html));
            
            // Actions nested under behavior
            assert(/<div[^>]*id="behavior-0"[^>]*class="[^"]*collapsible-content[^"]*"[^>]*style="[^"]*display:[^"]*"[^>]*>/.test(html));
            
            // Action items with proper structure
            assert(/<div[^>]*class="[^"]*collapsible-header[^"]*action-item[^"]*card-item[^"]*"[^>]*>/.test(html));
            
            // Current action (clarify) - verify marker, classes, and event handlers
            const clarifyActionRegex = /<div[^>]*class="[^"]*collapsible-header[^"]*action-item[^"]*card-item[^"]*active[^"]*"[^>]*title="[^"]*"[^>]*>[\s\S]*?<span[^>]*id="action-0-0-icon"[^>]*onclick="toggleCollapse\('action-0-0'\)"[^>]*>[\s\S]*?<span[^>]*onclick="navigateToAction\('shape',\s*'clarify'\)"[^>]*>[\s\S]*?clarify[\s\S]*?<\/span>/;
            assert(clarifyActionRegex.test(html));
            
            // Action expansion icon
            assert(/<span[^>]*id="action-0-0-icon"[^>]*onclick="toggleCollapse\('action-0-0'\)"[^>]*data-plus="[^"]*"[^>]*data-subtract="[^"]*"[^>]*>/.test(html));
            
            // Action name with navigation handler
            assert(/<span[^>]*onclick="navigateToAction\('shape',\s*'clarify'\)"[^>]*>[\s\S]*?clarify[\s\S]*?<\/span>/.test(html));
            
            // Operations nested under action
            assert(/<div[^>]*id="action-0-0"[^>]*class="[^"]*collapsible-content[^"]*"[^>]*style="[^"]*display:[^"]*"[^>]*>/.test(html));
            
            // Operation items
            assert(/<div[^>]*class="[^"]*operation-item[^"]*card-item[^"]*"[^>]*>/.test(html));
            
            // Current operation (instructions) - verify marker and click handler
            assert(/<div[^>]*class="[^"]*operation-item[^"]*card-item[^"]*active[^"]*"[^>]*onclick="navigateAndExecute\('shape',\s*'clarify',\s*'instructions'\)"[^>]*style="[^"]*cursor:[^"]*pointer[^"]*text-decoration:[^"]*underline[^"]*"[^>]*>[\s\S]*?instructions[\s\S]*?<\/div>/.test(html));
            
            // Navigation buttons (back, current, next)
            assert(/<button[^>]*onclick="executeNavigationCommand\('back'\)"[^>]*title="Back[^"]*"[^>]*>/.test(html));
            assert(/<button[^>]*onclick="executeNavigationCommand\('current'\)"[^>]*title="Current[^"]*"[^>]*>/.test(html));
            assert(/<button[^>]*onclick="executeNavigationCommand\('next'\)"[^>]*title="Next[^"]*"[^>]*>/.test(html));
            
            // Verify tooltips are present
            assert(/title="[^"]*"/.test(html));
            
            // Verify all interactive elements have proper cursor styles
            assert(/style="[^"]*cursor:\s*pointer[^"]*"/.test(html));
        } finally {
            pythonProcess.kill();
        }
    });
    
    await t.test('test_user_expands_and_collapses_behaviors', async () => {
        /**
         * SCENARIO: User expands and collapses behaviors
         * Story: Display Hierarchy
         * Steps from story-graph.json:
         *   Given Panel displays collapsed behavior tree
         *   When User clicks collapsed shape behavior
         *   Then Shape behavior expands showing actions (clarify, strategy)
         *   When User clicks expanded shape behavior again
         *   Then Shape behavior collapses hiding actions
         */
        const tmpPath = path.join(__dirname, '../../demo/mob_minion');
        const botDir = path.join(__dirname, '../bots/story_bot');
        
        const pythonProcess = spawnCLI(tmpPath, botDir);
        
        try {
            // Given Panel displays collapsed behavior tree
            const botJSON = await sendCommand(pythonProcess, 'status');
            const behaviorsJSON = botJSON.behaviors;
            const view = new BehaviorsView(behaviorsJSON, tmpPath);
            const html = view.render();
            
            // Verify behavior has collapse/expand icon with onclick handler
            assert(/<span[^>]*id="behavior-[^"]*-icon"[^>]*onclick="toggleCollapse\('behavior-[^"]*'\)"[^>]*>/.test(html));
            
            // Verify collapsible content div exists with display style
            assert(/<div[^>]*id="behavior-[^"]*"[^>]*class="[^"]*collapsible-content[^"]*"[^>]*style="[^"]*display:[^"]*"[^>]*>/.test(html));
            
            // When User clicks collapsed shape behavior (simulated by checking toggle handler exists)
            // Then Shape behavior expands showing actions (clarify, strategy)
            // When User clicks expanded shape behavior again
            // Then Shape behavior collapses hiding actions
            // (Expansion/collapse state is handled by JavaScript, verified by presence of toggle handler)
        } finally {
            pythonProcess.kill();
        }
    });
    
    await t.test('test_user_expands_and_collapses_actions', async () => {
        /**
         * SCENARIO: User expands and collapses actions
         * Story: Display Hierarchy
         * Steps from story-graph.json:
         *   Given Shape behavior is expanded showing actions
         *   And Clarify action is collapsed
         *   When User clicks collapsed clarify action
         *   Then Clarify action expands showing operations (instructions, execute, confirm)
         *   When User clicks expanded clarify action again
         *   Then Clarify action collapses hiding operations
         */
        const tmpPath = path.join(__dirname, '../../demo/mob_minion');
        const botDir = path.join(__dirname, '../bots/story_bot');
        
        const pythonProcess = spawnCLI(tmpPath, botDir);
        
        try {
            // Given Shape behavior is expanded showing actions
            // And Clarify action is collapsed
            await sendCommand(pythonProcess, 'shape.clarify');
            pythonProcess.kill();
            
            const statusProcess = spawnCLI(tmpPath, botDir);
            const botJSON = await sendCommand(statusProcess, 'status');
            statusProcess.kill();
            
            const behaviorsJSON = botJSON.behaviors;
            const view = new BehaviorsView(behaviorsJSON, tmpPath);
            const html = view.render();
            
            // Verify action has collapse/expand icon with onclick handler
            assert(/<span[^>]*id="action-[^"]*-icon"[^>]*onclick="toggleCollapse\('action-[^"]*'\)"[^>]*>/.test(html));
            
            // When User clicks collapsed clarify action
            // Then Clarify action expands showing operations (instructions, execute, confirm)
            // Verify operations are nested under action
            assert(/<div[^>]*id="action-[^"]*"[^>]*class="[^"]*collapsible-content[^"]*"[^>]*>/.test(html));
            assert(/<div[^>]*class="[^"]*operation-item[^"]*"[^>]*>/.test(html));
            
            // When User clicks expanded clarify action again
            // Then Clarify action collapses hiding operations
            // (Expansion/collapse state is handled by JavaScript, verified by presence of toggle handler)
        } finally {
            pythonProcess.kill();
        }
    });
});
```

**Scope View Example** (matching screenshot 3):

```javascript
// test/panel/test_manage_scope.js
// Sub-epic: Manage Scope Through Panel
// Stories: Display Story Scope Hierarchy, Filter Story Scope

test('TestFilterStoryScope', { concurrency: false }, async (t) => {
    
    await t.test('test_user_filters_scope_by_story_name', async () => {
        /**
         * SCENARIO: User filters scope by story name
         * Story: Filter Story Scope
         * Steps from story-graph.json:
         *   Given Panel displays scope section with full story hierarchy
         *   When User types Open Panel in scope filter
         *   Then Panel displays filtered hierarchy showing Open Panel story
         *   And Panel displays Open Panel parent sub-epic (Manage Panel Session)
         *   And Panel displays parent epic (Invoke Bot Through Panel)
         */
        const tmpPath = path.join(__dirname, '../../demo/mob_minion');
        const botDir = path.join(__dirname, '../bots/story_bot');
        
        const pythonProcess = spawnCLI(tmpPath, botDir);
        
        try {
            // Given Panel displays scope section with full story hierarchy
            const initialScopeJSON = await sendCommand(pythonProcess, 'scope');
            const initialView = new ScopeView(initialScopeJSON, tmpPath);
            const initialHtml = initialView.render();
            assert(/<div[^>]*class="[^"]*scope-section[^"]*"[^>]*>/.test(initialHtml));
            
            pythonProcess.kill();
            
            // When User types Open Panel in scope filter
            const filterProcess = spawnCLI(tmpPath, botDir);
            const filteredScopeJSON = await sendCommand(filterProcess, 'scope "Open Panel"');
            filterProcess.kill();
            
            const filteredView = new ScopeView(filteredScopeJSON, tmpPath);
            const filteredHtml = filteredView.render();
            
            // Then Panel displays filtered hierarchy showing Open Panel story
            assert(filteredHtml.includes('Open Panel'));
            
            // And Panel displays Open Panel parent sub-epic (Manage Panel Session)
            assert(filteredHtml.includes('Manage Panel Session'));
            
            // And Panel displays parent epic (Invoke Bot Through Panel)
            assert(filteredHtml.includes('Invoke Bot Through Panel'));
        } finally {
            pythonProcess.kill();
        }
    });
    
    await t.test('test_user_clears_story_scope_filter', async () => {
        /**
         * SCENARIO: User clears story scope filter
         * Story: Filter Story Scope
         * Steps from story-graph.json:
         *   Given Panel displays filtered scope showing only Open Panel story
         *   When User clicks clear filter button
         *   Then Panel displays all stories in full hierarchy
         *   And All epics are visible
         */
        const tmpPath = path.join(__dirname, '../../demo/mob_minion');
        const botDir = path.join(__dirname, '../bots/story_bot');
        
        const filterProcess = spawnCLI(tmpPath, botDir);
        
        try {
            // Given Panel displays filtered scope showing only Open Panel story
            await sendCommand(filterProcess, 'scope "Open Panel"');
            filterProcess.kill();
            
            const filteredScopeJSON = await sendCommand(filterProcess, 'scope');
            const filteredView = new ScopeView(filteredScopeJSON, tmpPath);
            const filteredHtml = filteredView.render();
            assert(filteredHtml.includes('Open Panel'));
            
            // When User clicks clear filter button (scope all)
            const clearProcess = spawnCLI(tmpPath, botDir);
            const clearedScopeJSON = await sendCommand(clearProcess, 'scope all');
            clearProcess.kill();
            
            const clearedView = new ScopeView(clearedScopeJSON, tmpPath);
            const clearedHtml = clearedView.render();
            
            // Then Panel displays all stories in full hierarchy
            // And All epics are visible
            assert(clearedHtml.length > filteredHtml.length); // More content when showing all
        } finally {
            filterProcess.kill();
        }
    });
});
```
    expect(html).toMatch(/<div[^>]*class="[^"]*collapsible-section[^"]*expanded[^"]*"[^>]*>/);
    expect(html).toMatch(/<div[^>]*class="[^"]*collapsible-header[^"]*"[^>]*onclick="toggleSection\('scope-content'\)"[^>]*>/);
    expect(html).toContain('Scope');
    
    // Section header with icon and clear button
    expect(html).toMatch(/<span[^>]*class="[^"]*expand-icon[^"]*"[^>]*>▸<\/span>/);
    expect(html).toMatch(/(<img[^>]*alt="Scope Icon"[^>]*>|🔍)/);
    expect(html).toMatch(/<button[^>]*onclick="event\.stopPropagation\(\);\s*clearScopeFilter\(\)"[^>]*title="Clear scope filter[^"]*"[^>]*>/);
    expect(html).toMatch(/<img[^>]*alt="Clear Filter"[^>]*style="[^"]*width:\s*24px[^"]*height:\s*24px[^"]*"[^>]*>/);
    
    // Graph links section
    expect(html).toMatch(/<a[^>]*href="javascript:void\(0\)"[^>]*onclick="openFile\('file:\/\/\/workspace\/story-graph\.json'\)"[^>]*style="[^"]*color:[^"]*text-decoration:[^"]*none[^"]*"[^>]*>story-graph\.json<\/a>/);
    
    // Scope content container
    expect(html).toContain('id="scope-content"');
    expect(html).toMatch(/<div[^>]*id="scope-content"[^>]*class="[^"]*collapsible-content[^"]*"[^>]*>/);
    
    // Story tree structure - Epic level
    expect(html).toMatch(/<div[^>]*class="[^"]*story-tree[^"]*"[^>]*>/);
    expect(html).toMatch(/<div[^>]*class="[^"]*epic-item[^"]*"[^>]*>[\s\S]*?Epic A[\s\S]*?<\/div>/);
    
    // Epic icon and expand/collapse
    expect(html).toMatch(/(<img[^>]*alt="Epic"[^>]*>|💡)/);
    expect(html).toMatch(/<span[^>]*onclick="toggleCollapse\('epic-[^']+'\)"[^>]*>/);
    
    // Sub-Epic level
    expect(html).toMatch(/<div[^>]*class="[^"]*sub-epic-item[^"]*"[^>]*>[\s\S]*?Sub-Epic A1[\s\S]*?<\/div>/);
    
    // Story items with file links
    expect(html).toMatch(/<div[^>]*class="[^"]*story-item[^"]*"[^>]*>[\s\S]*?Story A1[\s\S]*?<\/div>/);
    expect(html).toMatch(/<a[^>]*href="javascript:void\(0\)"[^>]*onclick="openFile\('file:\/\/\/workspace\/story-a1\.md'\)"[^>]*>Story A1<\/a>/);
    expect(html).toMatch(/<a[^>]*href="javascript:void\(0\)"[^>]*onclick="openFile\('file:\/\/\/workspace\/story-a2\.md'\)"[^>]*>Story A2<\/a>/);
    
    // Current scope indicator
    expect(html).toMatch(/<div[^>]*class="[^"]*current-scope[^"]*"[^>]*>[\s\S]*?Current Scope:[\s\S]*?Epic A[\s\S]*?Story A1[\s\S]*?<\/div>/);
    
    // File list structure (if type is 'files')
    // expect(html).toMatch(/<div[^>]*class="[^"]*file-list[^"]*"[^>]*>/);
    // expect(html).toMatch(/<div[^>]*class="[^"]*file-item[^"]*"[^>]*>[\s\S]*?<a[^>]*onclick="openFile\('[^']+'\)"[^>]*>/);
    
    // Verify all clickable elements have proper handlers
    expect(html).toMatch(/onclick="[^"]*"/);
    
    // Verify CSS classes for styling
    expect(html).toMatch(/class="[^"]*card-secondary[^"]*"/);
    expect(html).toMatch(/class="[^"]*empty-state[^"]*"/);
});
```

**Instructions View Example** (matching screenshots 4 & 5):

```javascript
// test/panel/test_display_instructions.js
// Sub-epic: Display Action Instructions Through Panel
// Stories: Display Clarify Instructions, Display Strategy Instructions, Display Build Instructions, Display Validate Instructions, Display Render Instructions

test('TestDisplayClarifyInstructions', { concurrency: false }, async (t) => {
    
    await t.test('test_user_views_clarify_instructions_with_key_questions', async () => {
        /**
         * SCENARIO: User views clarify instructions with key questions
         * Story: Display Clarify Instructions
         * Steps from story-graph.json:
         *   Given Bot is at shape.clarify
         *   And Guardrails define key questions and evidence
         *   When Panel displays instructions section
         *   Then Panel displays key questions list
         *   And Panel displays evidence requirements
         *   And Each question has editable textarea for answers
         */
        const tmpPath = path.join(__dirname, '../../demo/mob_minion');
        const botDir = path.join(__dirname, '../bots/story_bot');
        
        const pythonProcess = spawnCLI(tmpPath, botDir);
        
        try {
            // Given Bot is at shape.clarify
            await sendCommand(pythonProcess, 'shape.clarify');
            pythonProcess.kill();
            
            // And Guardrails define key questions and evidence (implicit in JSON)
            // When Panel displays instructions section
            const instructionsProcess = spawnCLI(tmpPath, botDir);
            const instructionsJSON = await sendCommand(instructionsProcess, 'current');
            instructionsProcess.kill();
            
            const view = new ClarifyInstructionsView(instructionsJSON, tmpPath);
            const html = view.render();
            
            // Then Panel displays key questions list
            assert(/<div[^>]*class="[^"]*key-questions[^"]*"[^>]*>/.test(html));
            assert(/<h3[^>]*>Key Questions<\/h3>/.test(html));
            
            // And Panel displays evidence requirements
            assert(/<div[^>]*class="[^"]*evidence[^"]*"[^>]*>/.test(html) || html.includes('evidence'));
            
            // And Each question has editable textarea for answers
            assert(/<textarea[^>]*id="[^"]*answer[^"]*"[^>]*>/.test(html));
            assert(/<label[^>]*>/.test(html));
        } finally {
            pythonProcess.kill();
        }
    });
    
    await t.test('test_user_edits_answer_to_key_question', async () => {
        /**
         * SCENARIO: User edits answer to key question
         * Story: Display Clarify Instructions
         * Steps from story-graph.json:
         *   Given Panel displays clarify instructions with questions
         *   When User types answer in question textarea
         *   Then System saves answer
         *   And Answer persists across panel refreshes
         */
        const tmpPath = path.join(__dirname, '../../demo/mob_minion');
        const botDir = path.join(__dirname, '../bots/story_bot');
        
        const pythonProcess = spawnCLI(tmpPath, botDir);
        
        try {
            // Given Panel displays clarify instructions with questions
            await sendCommand(pythonProcess, 'shape.clarify');
            pythonProcess.kill();
            
            const instructionsProcess = spawnCLI(tmpPath, botDir);
            const instructionsJSON = await sendCommand(instructionsProcess, 'current');
            instructionsProcess.kill();
            
            const view = new ClarifyInstructionsView(instructionsJSON, tmpPath);
            const html = view.render();
            assert(/<textarea[^>]*id="[^"]*answer[^"]*"[^>]*>/.test(html));
            
            // When User types answer in question textarea (simulated via onchange handler)
            // Verify textarea has onchange handler to save answer
            assert(/onchange="[^"]*updateAnswer[^"]*"/.test(html) || /onchange="[^"]*saveAnswer[^"]*"/.test(html));
            
            // Then System saves answer (via CLI command)
            // And Answer persists across panel refreshes (verified by checking save mechanism exists)
        } finally {
            pythonProcess.kill();
        }
    });
});
```

**Note**: No StatusView tests needed - Status domain doesn't exist. All status information is part of Bot JSON.

**Visual Mapping to Screenshots** (from `invoke-bot-panel-screens.md`):

Each story maps to a specific screenshot showing exact UI layout:

| Screenshot | Stories Covered | Key UI Elements to Verify |
|------------|----------------|--------------------------|
| `image1.png` | Open Panel, Display Session Status, Change Workspace Path, Switch Bot, Toggle Panel Section | Bot header, refresh button, workspace path input, bot selector dropdown, collapsible sections |
| `image2.png` | Display Hierarchy, Navigate Behavior Action, Execute Behavior Action | Behavior tree, action list, current markers, execute buttons, navigation controls |
| `image3.png` | Filter Story Scope, Display Story Scope Hierarchy, Filter File Scope, Open Story Files | Filter input, story graph tree, file list, clickable file links |
| `image4.png` | Display Base Instructions, Display Instructions In Raw Format | Instructions text area, raw format toggle |
| `image5.png` | Display Clarify Instructions, Submit Instructions To AI Agent | Key questions list, answer inputs, submit button |

**Test Coverage** (from walkthrough realizations + visual mapping):

**Epic: Invoke Bot Through Panel**

1. **Sub-Epic: Manage Panel Session** (Screenshot 1: `image1.png`)
   - ✅ **Open Panel** - Verify exact HTML structure matches screenshot
     - Bot header with name "story_bot"
     - Refresh button (top right)
     - Workspace path display with edit button
     - Bot selector dropdown
     - All sections visible (behaviors, scope, instructions)
   - ✅ **Display Session Status** - Verify status elements render correctly
     - Current behavior/action displayed
     - Progress indicators visible
   - ✅ **Change Workspace Path** - Verify workspace path input/button exists
     - Input field for workspace path
     - Update button
   - ✅ **Switch Bot** - Verify bot selector dropdown renders
     - Dropdown with available bots
     - Current bot selected
   - ✅ **Toggle Panel Section** - Verify collapse/expand functionality
     - Collapsible headers for each section
     - Expand/collapse icons

2. **Sub-Epic: Navigate And Execute Behaviors Through Panel** (Screenshot 2: `image2.png`)
   - ✅ **Display Hierarchy** - Verify behavior/action tree matches screenshot
     - Behavior list with expand/collapse
     - Actions nested under behaviors
     - Current behavior/action highlighted
     - Status markers (current, completed, pending)
   - ✅ **Navigate Behavior Action** - Verify navigation buttons exist
     - Previous/Next buttons
     - Current position indicator
   - ✅ **Execute Behavior Action** - Verify execute button renders correctly
     - Execute button for each behavior/action
     - Click handlers attached

3. **Sub-Epic: Manage Scope Through Panel** (Screenshot 3: `image3.png`)
   - ✅ **Filter Story Scope** - Verify filter input and results display
     - Filter input field
     - Filter results list
     - Clear filter button
   - ✅ **Display Story Scope Hierarchy** - Verify story graph tree structure
     - Epic/Sub-Epic/Story hierarchy
     - Expandable tree nodes
     - Story links
   - ✅ **Filter File Scope** - Verify file list filtering
     - File list display
     - File filtering
   - ✅ **Open Story Files** - Verify file links render correctly
     - Clickable file links
     - Line number support

4. **Sub-Epic: Display Action Instructions Through Panel** (Screenshots 4 & 5: `image4.png`, `image5.png`)
   - ✅ **Display Base Instructions** - Verify base instructions section (Screenshot 4)
     - Instructions text area
     - Formatting preserved
   - ✅ **Display Clarify Instructions** - Verify clarify-specific UI (Screenshot 5)
     - Key questions list
     - Evidence sections
     - Editable answer fields
   - ✅ **Display Strategy Instructions** - Verify strategy-specific UI
     - Decision criteria
     - Assumptions list
   - ✅ **Display Build Instructions** - Verify build-specific UI
     - Knowledge graph spec
     - Builder instructions
   - ✅ **Display Validate Instructions** - Verify validate-specific UI
     - Rules list
     - Validation results
   - ✅ **Display Render Instructions** - Verify render-specific UI
     - Render spec
     - Template information
   - ✅ **Display Instructions In Raw Format** - Verify raw format toggle
     - Raw format button/toggle
     - Raw text display
   - ✅ **Submit Instructions To AI Agent** - Verify submit button exists
     - Submit button
     - Clipboard copy functionality

---

## Migration Checklist

### Legacy Code to Migrate

- [ ] `status_panel.js` → `bot_view.js` + domain views
- [ ] `status_data_provider.js` → Use `PanelView.execute()` directly
- [ ] `cli_output_adapter.js` → Remove (CLI outputs JSON directly)
- [ ] `html_renderer.js` → Split into domain views
- [ ] `status_parser.js` → Remove (not needed with JSON)
- [ ] `extension.js` → Update to use new views

### New Files to Create

- [ ] `src/bot/bot_view.js` - Main orchestrator
- [ ] `src/bot/bot_header_view.js` - Header section
- [ ] `src/bot/paths_section.js` - Paths section
- [ ] `src/behaviors/behaviors_view.js` - Behaviors section
- [ ] `src/scope/scope_view.js` - Scope section
- [ ] `src/instructions/instructions_view.js` - Instructions section
- [ ] `src/instructions/clarify_instructions_view.js` - Clarify-specific
- [ ] `src/instructions/strategy_instructions_view.js` - Strategy-specific
- [ ] `src/instructions/build_instructions_view.js` - Build-specific
- [ ] `src/instructions/validate_instructions_view.js` - Validate-specific
- [ ] `src/instructions/render_instructions_view.js` - Render-specific
- [ ] `src/panel/extension.js` - VS Code extension entry point
- [ ] `test/panel/test_*.js` - Test files (7+ files)

### Files to Update

- [ ] `src/panel/panel_view.js` - Add workspace directory support
- [ ] `src/status/status_view.js` - **DELETE** (Status domain doesn't exist - everything is in Bot)

---

## Testing Strategy

### Unit Tests (JavaScript)

**Framework**: Jest or Mocha with Chai assertions

**Pattern**: Given-When-Then format matching Python test structure

**Example**:

```javascript
// Additional test class example
test('TestBehaviorsViewDisplayHierarchy', { concurrency: false }, async (t) => {
    
    await t.test('test_render_behavior_hierarchy_from_json', async () => {
        /**
         * SCENARIO: Render behavior hierarchy from JSON
         * GIVEN: Real behaviors JSON from CLI status command
         * WHEN: BehaviorsView renders with real data
         * THEN: HTML structure matches screenshot 2 with comprehensive verification
         */
        const tmpPath = path.join(__dirname, '../../demo/mob_minion');
        const botDir = path.join(__dirname, '../bots/story_bot');
        
        const pythonProcess = spawnCLI(tmpPath, botDir);
        
        try {
            // GIVEN: Real behaviors JSON from CLI status command
            const botJSON = await sendCommand(pythonProcess, 'status');
            const behaviorsJSON = botJSON.behaviors;
            
            // WHEN: BehaviorsView renders with real data
            const view = new BehaviorsView(behaviorsJSON, tmpPath);
            const html = view.render();
            
            // THEN: Verify comprehensive HTML structure matching screenshot 2
            
            // Main section container with proper classes
            assert(/<div[^>]*class="[^"]*section[^"]*card-primary[^"]*"[^>]*>/.test(html));
            
            // Section header with expand/collapse
            assert(/<div[^>]*class="[^"]*collapsible-header[^"]*"[^>]*onclick="toggleSection\('behaviors-content'\)"[^>]*>/.test(html));
            assert(html.includes('Behavior Action Status'));
            assert(html.includes('id="behaviors-content"'));
            
            // Behavior: shape (current) - verify complete structure
            assert(/<div[^>]*class="[^"]*collapsible-header[^"]*card-item[^"]*active[^"]*"[^>]*>/.test(html));
            assert(/<span[^>]*id="behavior-0-icon"[^>]*onclick="toggleCollapse\('behavior-0'\)"[^>]*>/.test(html));
            assert(/<span[^>]*onclick="navigateToBehavior\('shape'\)"[^>]*>[\s\S]*?shape[\s\S]*?<\/span>/.test(html));
            assert(/(<img[^>]*alt="Current"[^>]*>|<span[^>]*class="[^"]*status-marker[^"]*marker-current[^"]*"[^>]*>➤<\/span>)/.test(html));
            
            // Behavior: exploration (completed) - verify complete structure
            assert(/<div[^>]*class="[^"]*collapsible-header[^"]*card-item[^"]*"[^>]*>/.test(html));
            assert(/<span[^>]*onclick="navigateToBehavior\('exploration'\)"[^>]*>[\s\S]*?exploration[\s\S]*?<\/span>/.test(html));
            assert(/(<img[^>]*alt="Completed"[^>]*>|<span[^>]*class="[^"]*status-marker[^"]*marker-completed[^"]*"[^>]*>☑<\/span>)/.test(html));
            
            // Actions nested under behaviors
            assert(/<div[^>]*id="behavior-0"[^>]*class="[^"]*collapsible-content[^"]*"[^>]*>/.test(html));
            assert(/<div[^>]*class="[^"]*collapsible-header[^"]*action-item[^"]*card-item[^"]*"[^>]*>/.test(html));
            
            // Action navigation handlers
            assert(/onclick="navigateToAction\('[^']+',\s*'[^']+'\)"/.test(html));
            
            // Operations nested under actions
            assert(/<div[^>]*id="action-[^"]*"[^>]*class="[^"]*collapsible-content[^"]*"[^>]*>/.test(html));
            assert(/<div[^>]*class="[^"]*operation-item[^"]*card-item[^"]*"[^>]*>/.test(html));
            
            // Operation execution handlers
            assert(/onclick="navigateAndExecute\('[^']+',\s*'[^']+',\s*'[^']+'\)"/.test(html));
            
            // Navigation buttons section
            assert(/<button[^>]*onclick="executeNavigationCommand\('back'\)"[^>]*>/.test(html));
            assert(/<button[^>]*onclick="executeNavigationCommand\('current'\)"[^>]*>/.test(html));
            assert(/<button[^>]*onclick="executeNavigationCommand\('next'\)"[^>]*>/.test(html));
            
            // Verify data attributes for expansion state
            assert(/data-plus="[^"]*"/.test(html));
            assert(/data-subtract="[^"]*"/.test(html));
            
            // Verify tooltips
            assert(/title="[^"]*"/.test(html));
            
            // Verify CSS classes for styling
            assert(/class="[^"]*card-secondary[^"]*"/.test(html));
            assert(/class="[^"]*collapsible-section[^"]*"/.test(html));
            
            // Verify expansion state in style attributes
            assert(/style="[^"]*display:\s*(block|none)[^"]*"/.test(html));
        } finally {
            pythonProcess.kill();
        }
    });
});
```

### Integration Tests

**Test CLI Round-Trip**:
- Spawn actual Python CLI subprocess
- Send commands via stdin
- Parse JSON from stdout
- Verify JSON structure matches domain adapters

**Test Panel Rendering**:
- Create domain views with real JSON
- Verify HTML output
- Test event handling

---

## Success Criteria

### Phase 1 Complete
- [ ] PanelView base class supports domain pattern
- [ ] CLI communication works in JSON mode

### Phase 2 Complete
- [ ] BotView orchestrates all domain views
- [ ] Main panel renders correctly
- [ ] Refresh works end-to-end

### Phase 3 Complete
- [ ] All domain section views created
- [ ] Each view renders HTML correctly
- [ ] Event handling works for each view

### Phase 4 Complete
- [ ] Extension entry point updated
- [ ] Panel opens and displays correctly
- [ ] All legacy functionality preserved

### Phase 5 Complete
- [ ] All test files created
- [ ] Tests follow given-when-then format
- [ ] Test coverage matches walkthrough scenarios
- [ ] All tests passing

---

## References

- **CRC Model**: `agile_bot/docs/crc/crc-model-outline.md`
- **Walkthrough Realizations**: `agile_bot/docs/crc/walkthrough-realizations.md`
- **CLI Domain Refactoring Plan**: `agile_bot/docs/plans/CRC_DOMAIN_REFACTORING_PLAN.md`
- **Status View Example**: `agile_bot/src/status/status_view.js`
- **Legacy Panel Code**: `agile_bot/legacy/src/display_panel/extension/`

---

## Notes

- Panel views follow exact same domain organization as CLI adapters
- Only base classes remain in `panel/` folder
- All domain-specific logic lives in domain folders
- Tests mirror Python test structure (given-when-then)
- CLI communication uses JSON mode exclusively (piped stdin/stdout)
- **Important**: There is NO Status domain - the `status` command returns the Bot object itself. All status information (current_behavior, progress_path, etc.) is part of the Bot JSON structure. The `status_view.js` file should be deleted as it references a non-existent Status domain.

**Visual Mapping Requirements**:
- Each story test must verify HTML structure matches corresponding screenshot in `invoke-bot-panel-screens.md`
- Tests must use hard-coded HTML expectations (like CLI tests: "Verify exact format with hard-coded expectations")
- Verify exact CSS classes, data attributes, button text, and element structure from screenshots
- Reference `html_renderer.js` for exact HTML structure that needs to be replicated
- Ensure all clickable elements (buttons, links, inputs) are present and correctly structured