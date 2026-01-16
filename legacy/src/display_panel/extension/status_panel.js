/**
 * Status Panel Controller
 * 
 * Manages webview panel lifecycle and coordinates data fetching,
 * parsing, and rendering. Implements singleton pattern.
 */

const vscode = require("vscode");
const path = require("path");
const StatusDataProvider = require("./status_data_provider.js");
const CLIOutputAdapter = require("./cli_output_adapter.js");
const HtmlRenderer = require("./html_renderer.js");
const Logger = require("./logger.js");

class StatusPanel {
  static currentPanel = undefined;
  static viewType = "agilebot.statusPanel";

  constructor(panel, workspaceRoot, extensionUri) {
    this._panel = panel;
    this._workspaceRoot = workspaceRoot;
    this._extensionUri = extensionUri;
    this._disposables = [];
    this._lastPromptContent = ''; // Store last prompt to survive re-renders
    this._expansionState = {}; // Track which behaviors/actions are expanded: { 'behavior-0': true, 'action-0-1': false }
    
    // Initialize logger
    const logPath = path.join(workspaceRoot, "agile_bot", "bots", "base_bot", "logs", "panel-debug.log");
    this._logger = new Logger(logPath);
    this._logger.log("StatusPanel constructor called");
    
    // Initialize components
    this._dataProvider = new StatusDataProvider(workspaceRoot);
    this._adapter = new CLIOutputAdapter();
    this._renderer = new HtmlRenderer();

    // Set the webview's initial html content
    this._update();

    // Listen for when the panel is disposed
    this._panel.onDidDispose(() => this.dispose(), null, this._disposables);

    // Update the content when the webview becomes visible
    this._panel.onDidChangeViewState(
      (e) => {
        if (this._panel.visible) {
          this._update();
        }
      },
      null,
      this._disposables
    );

    // Handle messages from the webview
    this._panel.webview.onDidReceiveMessage(
      (message) => {
        this._logger.log('Received message from webview:', message);
        switch (message.command) {
          case "refresh":
            this._update();
            return;
          case "openScope":
            if (message.filePath) {
              // Parse fragment (e.g., #L233 for line number, #method_name for symbol)
              const cleanPath = message.filePath.split('#')[0];
              const fragment = message.filePath.includes('#') 
                ? message.filePath.split('#')[1] 
                : null;
              
              let lineNumber = null;
              let symbolName = null;
              
              if (fragment) {
                if (fragment.startsWith('L')) {
                  // Line number format: #L123
                  lineNumber = parseInt(fragment.substring(1));
                } else {
                  // Symbol/method name format: #test_method_name
                  symbolName = fragment;
                }
              }
              
              // If path is already absolute, use it; otherwise resolve from workspace root
              const absolutePath = path.isAbsolute(cleanPath) 
                ? cleanPath 
                : path.join(this._workspaceRoot, cleanPath);
              const fileUri = vscode.Uri.file(absolutePath);
              
              // Check if this is a special file type that needs custom handling
              const fileExtension = cleanPath.split('.').pop().toLowerCase();
              const binaryOrSpecialExtensions = ['drawio', 'png', 'jpg', 'jpeg', 'gif', 'pdf', 'svg'];
              
              if (binaryOrSpecialExtensions.includes(fileExtension)) {
                // For DrawIO and other binary/special files, use vscode.open to respect file associations
                vscode.commands.executeCommand('vscode.open', fileUri).then(
                  () => {
                    // Success - file opened with appropriate viewer
                  },
                  (error) => {
                    vscode.window.showErrorMessage(`Failed to open file: ${message.filePath}\n${error.message}`);
                  }
                );
              } else {
                // For text files, use openTextDocument to support line numbers and symbols
                vscode.workspace.openTextDocument(fileUri).then(
                  (doc) => {
                    // If we have a symbol name, search for it in the file
                    if (symbolName) {
                      const text = doc.getText();
                      const lines = text.split('\n');
                      let foundLine = -1;
                      
                      // Search for the symbol (method/function/class definition)
                      for (let i = 0; i < lines.length; i++) {
                        const line = lines[i];
                        // Match various patterns: def method_name, class ClassName, etc.
                        if (line.includes(symbolName) && 
                            (line.trim().startsWith('def ') || 
                             line.trim().startsWith('class ') ||
                             line.trim().startsWith('async def ') ||
                             line.includes(`def ${symbolName}(`) ||
                             line.includes(`class ${symbolName}(`))) {
                          foundLine = i;
                          break;
                        }
                      }
                      
                      if (foundLine >= 0) {
                        lineNumber = foundLine + 1; // Convert to 1-based line number
                      }
                    }
                    
                    const options = lineNumber 
                      ? { 
                          selection: new vscode.Range(lineNumber - 1, 0, lineNumber - 1, 0),
                          viewColumn: vscode.ViewColumn.One
                        }
                      : { viewColumn: vscode.ViewColumn.One };
                    vscode.window.showTextDocument(doc, options);
                  },
                  (error) => {
                    vscode.window.showErrorMessage(`Failed to open file: ${message.filePath}\n${error.message}`);
                  }
                );
              }
            }
            return;
          case "updateFilter":
            if (message.filter) {
              this._logger.log(`Updating scope filter to: ${message.filter}`);
              // Execute scope command via CLI
              this._dataProvider.updateScope(message.filter)
                .then(() => {
                  // Refresh panel after scope change
                  this._update();
                })
                .catch((error) => {
                  this._logger.error('Failed to update scope filter', error);
                  vscode.window.showErrorMessage(`Failed to update scope: ${error.message}`);
                });
            }
            return;
          case "clearFilter":
            this._logger.log('Clearing scope filter - executing scope showAll');
            // Execute scope showAll command directly
            this._dataProvider.executeCommand('scope showAll')
              .then((output) => {
                // Refresh panel after scope change
                this._update();
              })
              .catch((error) => {
                this._logger.error('Failed to clear scope filter', error);
                vscode.window.showErrorMessage(`Failed to clear scope: ${error.message}`);
              });
            return;
          case "updateWorkspace":
            if (message.workspacePath) {
              this._logger.log(`Updating workspace path to: ${message.workspacePath}`);
              // Execute path command via CLI
              this._dataProvider.updateWorkspace(message.workspacePath)
                .then(() => {
                  // Update workspace root and refresh
                  this._workspaceRoot = message.workspacePath;
                  this._update();
                })
                .catch((error) => {
                  this._logger.error('Failed to update workspace path', error);
                  vscode.window.showErrorMessage(`Failed to update workspace: ${error.message}`);
                });
            }
            return;
          case "updateQuestionAnswer":
            if (message.question && message.answer !== undefined) {
              this._logger.log(`Updating question answer: "${message.question}" = "${message.answer}"`);
              // Update question/answer via CLI (saves to clarification.json)
              this._dataProvider.updateQuestionAnswer(message.question, message.answer)
                .then(() => {
                  // Refresh panel after update
                  this._update();
                })
                .catch((error) => {
                  this._logger.error('Failed to update question answer', error);
                  vscode.window.showErrorMessage(`Failed to update answer: ${error.message}`);
                });
            }
            return;
          case "switchBot":
            this._logger.log(`[SWITCHBOT] Received switchBot message:`, message);
            if (message.botName) {
              this._logger.log(`[SWITCHBOT] Switching bot to: ${message.botName}`);
              this._dataProvider.currentBot = message.botName;
              this._logger.log(`[SWITCHBOT] Calling _update()`);
              this._update();
              this._logger.log(`[SWITCHBOT] Update complete`);
            } else {
              this._logger.error(`[SWITCHBOT] No botName in message`);
            }
            return;
          case "executeCommand":
            if (message.commandText) {
              this._logger.log(`Executing command: ${message.commandText}`);
              this._dataProvider.executeCommand(message.commandText)
                .then((result) => {
                  this._logger.log('Command executed successfully');
                  // Show result in output channel or notification
                  vscode.window.showInformationMessage(`Command executed: ${message.commandText}`);
                  // Refresh the panel to show any state changes
                  this._update();
                })
                .catch((error) => {
                  this._logger.error('Failed to execute command', error);
                  vscode.window.showErrorMessage(`Failed to execute command: ${error.message}`);
                });
            }
            return;
          case "navigateAndExecute":
            if (message.fullCommand) {
              this._logger.log(`Navigating and executing: ${message.fullCommand}`);
              this._dataProvider.executeCommand(message.fullCommand)
                .then((output) => {
                  this._logger.log('Command executed successfully');
                  // Extract and store prompt content from output
                  this._lastPromptContent = this._extractPromptContent(output);
                  console.log('[PANEL] Extracted instructions length:', this._lastPromptContent ? this._lastPromptContent.length : 0);
                  
                  // Copy to clipboard using VS Code API (more reliable than webview clipboard)
                  if (this._lastPromptContent) {
                    vscode.env.clipboard.writeText(this._lastPromptContent).then(() => {
                      console.log('[PANEL] ✓ Instructions copied to clipboard successfully');
                      this._logger.log('Instructions copied to clipboard');
                    }).catch(err => {
                      console.error('[PANEL] ✗ Failed to copy to clipboard:', err);
                      this._logger.error('Clipboard copy failed', err);
                    });
                  }
                  
                  // Refresh the panel - prompt will be included in render
                  this._update();
                })
                .catch((error) => {
                  this._logger.error('Failed to execute operation', error);
                  vscode.window.showErrorMessage(`Failed to execute: ${error.message}`);
                  this._lastPromptContent = `Error: ${error.message}`;
                  this._update();
                });
            }
            return;
          case "updateExpansionState":
            if (message.expansionState) {
              this._logger.log('Updating expansion state:', message.expansionState);
              // Merge new expansion state with existing
              this._expansionState = { ...this._expansionState, ...message.expansionState };
            }
            return;
          case "sendToChat":
            this._logger.log('sendToChat - calling bot submit command');
            
            // Call the bot's submit command (Python handles everything)
            this._dataProvider.executeCommand('submit')
              .then((output) => {
                this._logger.log('Bot submit command output:', output);
                
                // Check for success
                if (output.includes('SUCCESS:') || output.includes('submitted to Cursor chat successfully')) {
                  vscode.window.showInformationMessage('Instructions submitted to chat!');
                }
                // Check for errors
                else if (output.includes('ERROR:') || output.includes('FAILED:')) {
                  const errorMatch = output.match(/ERROR:|FAILED:\s*(.+)/);
                  const errorMsg = errorMatch ? errorMatch[1] : 'Unknown error';
                  vscode.window.showErrorMessage(`Submit failed: ${errorMsg}`);
                }
                // Unknown result
                else {
                  vscode.window.showWarningMessage('Submit completed with unknown result');
                  console.log('[PANEL] Submit output:', output);
                }
              })
              .catch((error) => {
                this._logger.error('Submit command failed:', error);
                vscode.window.showErrorMessage(`Submit command failed: ${error.message}`);
              });
            return;
        }
      },
      null,
      this._disposables
    );
  }

  static createOrShow(workspaceRoot, extensionUri) {
    const column = vscode.ViewColumn.Two;

    // If we already have a panel, show it
    if (StatusPanel.currentPanel) {
      StatusPanel.currentPanel._panel.reveal(column);
      return;
    }

    // Otherwise, create a new panel
    const panel = vscode.window.createWebviewPanel(
      StatusPanel.viewType,
      "Bot Status Dashboard",
      column,
      {
        enableScripts: true,
        retainContextWhenHidden: false,
        localResourceRoots: [
          extensionUri,
          vscode.Uri.file(path.join(workspaceRoot, 'agile_bot', 'bots', 'base_bot', 'img'))
        ],
      }
    );

    StatusPanel.currentPanel = new StatusPanel(panel, workspaceRoot, extensionUri);
  }

  dispose() {
    StatusPanel.currentPanel = undefined;

    // Clean up resources
    this._panel.dispose();

    while (this._disposables.length) {
      const disposable = this._disposables.pop();
      if (disposable) {
        disposable.dispose();
      }
    }
  }

  _extractPromptContent(output) {
    // Extract the COMPLETE INSTRUCTIONS SECTION (everything between INSTRUCTIONS SECTION and CLI STATUS section)
    // This includes: base instructions, behavior instructions, scope, and all merged content
    const instructionsSectionMatch = /\*\*INSTRUCTIONS SECTION:\*\*[\s\S]*?[━─-]{50,}\s*\n([\s\S]+?)\n\s*[━═=]{50,}\s*\n\s*\*\*\*\s+CLI STATUS section/m.exec(output);
    
    if (instructionsSectionMatch) {
      console.log('[PANEL] Extracted INSTRUCTIONS SECTION');
      return instructionsSectionMatch[1].trim();
      }
    
    console.log('[PANEL] No INSTRUCTIONS SECTION found, returning full output');
    // Fallback: return the full output
    return output;
  }

  _buildPromptFromInstructions(instructions) {
    // Build formatted prompt content from instructions object
    if (!instructions) return '';
    
    const lines = [];
    
    // Helper to safely add array content
    const addLines = (arr) => {
      if (Array.isArray(arr)) {
        arr.forEach(item => lines.push(item));
      } else if (typeof arr === 'string') {
        lines.push(arr);
      }
    };
    
    // Add base instructions
    if (instructions.base_instructions) {
      addLines(instructions.base_instructions);
    }
    
    // Add behavior instructions
    if (instructions.behavior_instructions) {
      lines.push('');
      lines.push('## Behavior Context:');
      addLines(instructions.behavior_instructions);
    }
    
    // Add action instructions
    if (instructions.action_instructions) {
      lines.push('');
      lines.push('## Action Instructions:');
      addLines(instructions.action_instructions);
    }
    
    // Add scope if present
    if (instructions.scope) {
      lines.push('');
      lines.push('## Scope:');
      if (typeof instructions.scope === 'string') {
        lines.push(instructions.scope);
      } else {
        lines.push(JSON.stringify(instructions.scope, null, 2));
      }
    }
    
    return lines.join('\n');
  }


  async _update() {
    const webview = this._panel.webview;
    this._panel.title = "Bot Status Dashboard";
    
    this._logger.log("_update() called");
    
    try {
      // Check availability first
      const isAvailable = await this._dataProvider.checkAvailability();
      this._logger.log("Availability check", { isAvailable });
      
      if (!isAvailable) {
        this._panel.webview.html = this._renderer.renderError(
          "REPL CLI not found or Python not available. Please ensure Python is installed and REPL CLI is in the expected location."
        );
        return;
      }

      // Fetch status data
      const rawStatus = await this._dataProvider.getStatus();
      this._logger.log("Got raw status, length:", rawStatus.length);
      
      // Store raw status for raw instructions display
      this._rawStatusOutput = rawStatus;
      
      // Adapt CLI output to structured JSON
      const structuredData = this._adapter.adapt(rawStatus);
      
      // Add bot selector data
      structuredData.availableBots = this._dataProvider.getAvailableBots();
      structuredData.currentBot = this._dataProvider.getCurrentBot();
      
      // Get promptContent from _lastPromptContent (populated when user runs instructions)
      // If empty, try to get it now by running instructions command
      if (!this._lastPromptContent) {
        try {
          const instructionsOutput = await this._dataProvider.executeCommand('instructions');
          if (instructionsOutput && instructionsOutput.length > 100) {
            this._lastPromptContent = instructionsOutput;
            this._logger.log('Auto-fetched instructions, length:', instructionsOutput.length);
          }
        } catch (error) {
          this._logger.log('Could not auto-fetch instructions:', error.message);
        }
      }
      
      structuredData.promptContent = this._lastPromptContent || '';
      
      // Add expansion state so user's open/close choices survive re-render
      structuredData.expansionState = this._expansionState;
      
      this._logger.log("Adapted data", structuredData);

      // Render HTML (pass webview and extensionUri so renderer can create proper URIs)
      this._panel.webview.html = this._renderer.render(structuredData, this._panel.webview, this._extensionUri);
      this._logger.log("Rendered HTML to webview");
      
    } catch (err) {
      console.error("Status panel update error:", err);
      this._logger.error("Status panel update error", err);
      this._panel.webview.html = this._renderer.renderError(err.message);
    }
  }
}

module.exports = StatusPanel;
