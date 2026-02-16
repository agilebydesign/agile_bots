/**
 * Bot Panel Controller
 * 
 * Manages webview panel lifecycle and coordinates data fetching,
 * parsing, and rendering using the new domain-oriented BotView.
 * Implements singleton pattern.
 */

const vscode = require("vscode");
const path = require("path");
const fs = require("fs");
const BotView = require("./bot_view");
const PanelView = require("./panel_view");
const branding = require("./branding");

class BotPanel {
  constructor(panel, workspaceRoot, extensionUri) {
    // ===== PERFORMANCE: Start constructor timing =====
    const perfConstructorStart = performance.now();
    try {
      // Setup file logging first
      const logFile = path.join(workspaceRoot || 'c:\\dev\\augmented-teams', 'panel-debug.log');
      this.logFilePath = logFile;
      this._log = (msg) => {
        const timestamp = new Date().toISOString();
        try {
          fs.appendFileSync(logFile, `${timestamp} ${msg}\n`);
        } catch (e) {
          console.error('[BotPanel] Failed to write to log file:', e);
        }
        console.log(msg);
      };
      
      this._displayError = (errorMsg) => {
        this._log('[BotPanel] Displaying error in webview: ' + errorMsg);
        vscode.window.showErrorMessage('Bot Panel Error: ' + errorMsg);
        if (this._panel && this._panel.webview) {
          this._panel.webview.postMessage({
            command: 'displayError',
            error: errorMsg
          });
        }
      };
      
      this._log("[BotPanel] Constructor invoked");
      this._log(`[PERF] Constructor start`);
      console.log(`[BotPanel] Constructor called - workspaceRoot: ${workspaceRoot}`);
      this._panel = panel;
      this._workspaceRoot = workspaceRoot;
      this._extensionUri = extensionUri;
      this._disposables = [];
      this._expansionState = {};
      this._currentStoryMapView = 'Hierarchy'; // 'Hierarchy', 'Increment', or 'Files'
      
      // Initialize branding with repo root
      branding.setRepoRoot(workspaceRoot);
      this._log(`[BotPanel] Branding initialized: ${branding.getBranding()}`);
      
      // Read panel version from package.json
      const perfVersionStart = performance.now();
      console.log("[BotPanel] Reading panel version");
      this._panelVersion = this._readPanelVersion();
      const perfVersionEnd = performance.now();
      console.log(`[BotPanel] Panel version: ${this._panelVersion}`);
      this._log(`[PERF] Read panel version: ${(perfVersionEnd - perfVersionStart).toFixed(2)}ms`);
      
      // Determine bot directory (from env var or default to story_bot)
      let botDirectory = process.env.BOT_DIRECTORY || path.join(workspaceRoot, 'bots', 'story_bot');
      // Ensure bot directory is absolute
      if (!path.isAbsolute(botDirectory)) {
        botDirectory = path.join(workspaceRoot, botDirectory);
      }
      console.log(`[BotPanel] Bot directory: ${botDirectory}`);
      
      // Create shared PanelView instance for CLI operations
      const perfPanelViewStart = performance.now();
      console.log("[BotPanel] Creating shared PanelView instance");
      this._sharedCLI = new PanelView(botDirectory);
      const perfPanelViewEnd = performance.now();
      console.log("[BotPanel] Shared PanelView instance created successfully");
      this._log(`[PERF] PanelView creation: ${(perfPanelViewEnd - perfPanelViewStart).toFixed(2)}ms`);
      
      // Initialize BotView (uses shared CLI)
      this._botView = null;
      
      // Set initial loading HTML
      console.log("[BotPanel] Setting initial loading HTML");
      this._panel.webview.html = this._getWebviewContent('<div style="padding: 20px;">Loading bot panel...</div>');
      
      // Update content asynchronously (can't await in constructor)
      console.log("[BotPanel] Calling _update()");
      this._update().catch(err => {
        console.error(`[BotPanel] ERROR in async _update: ${err.message}`);
        console.error(`[BotPanel] ERROR stack: ${err.stack}`);
        vscode.window.showErrorMessage(`Bot Panel Error: ${err.message}`);
      });
      
      // ===== PERFORMANCE: End constructor timing =====
      const perfConstructorEnd = performance.now();
      const constructorDuration = (perfConstructorEnd - perfConstructorStart).toFixed(2);
      console.log("[BotPanel] Constructor completed successfully");
      this._log(`[PERF] TOTAL Constructor duration: ${constructorDuration}ms`);
    } catch (error) {
      console.error(`[BotPanel] ERROR in constructor: ${error.message}`);
      console.error(`[BotPanel] ERROR stack: ${error.stack}`);
      vscode.window.showErrorMessage(`Bot Panel Constructor Error: ${error.message}\n${error.stack}`);
      throw error;
    }

    // Listen for when the panel is disposed
    this._panel.onDidDispose(() => this.dispose(), null, this._disposables);

    // Note: We don't refresh when the panel becomes visible - once loaded, the webview content persists
    // This preserves user state (scroll position, expanded nodes, etc.) when switching tabs
    // The panel only refreshes when explicitly requested (refresh button, certain operations)
    this._panel.onDidChangeViewState(
      (e) => {
        // Reset flag after a short delay to allow file opening to complete
        if (this._isOpeningFile) {
          setTimeout(() => { this._isOpeningFile = false; }, 500);
        }
      },
      null,
      this._disposables
    );

    // Handle messages from the webview
    this._log('[BotPanel] Registering onDidReceiveMessage handler');
    this._panel.webview.onDidReceiveMessage(
      (message) => {
        this._log('[BotPanel] *** MESSAGE HANDLER FIRED ***');
        this._log('[BotPanel] Received message from webview: ' + message.command + ' ' + JSON.stringify(message));
        switch (message.command) {
          case "hidePanel":
            // Close/dispose the panel - user can reopen via command
            this._log('[BotPanel] Closing panel');
            this._panel.dispose();
            return;
          case "refresh":
            // Delete the enriched cache to force regeneration of test links
            const fs = require('fs');
            const cachePath = path.join(this._workspaceRoot, 'docs', 'stories', '.story-graph-enriched-cache.json');
            try {
              if (fs.existsSync(cachePath)) {
                fs.unlinkSync(cachePath);
                this._log('[BotPanel] Deleted enriched cache file');
              }
            } catch (err) {
              this._log(`[BotPanel] Warning: Could not delete cache: ${err.message}`);
            }
            // Clear the story graph cache in the Bot instance to force reload
            (async () => {
              try {
                this._log('[BotPanel] Clearing story graph cache...');
                await this._botView.execute('reload_story_graph --format json');
                this._log('[BotPanel] Story graph cache cleared');
              } catch (err) {
                this._log(`[BotPanel] Warning: Could not clear story graph cache: ${err.message}`);
              }
              // Proceed with refresh after clearing cache
              try {
                await this._update();
                // After refresh, re-expand the current action's section
                const botData = this._botView?.botData;
                const currentAction = botData?.behaviors?.current_action || botData?.current_action || null;
                if (currentAction) {
                  setTimeout(() => {
                    try {
                      this._log(`[BotPanel] Refresh: Re-expanding section for: ${currentAction}`);
                      this._panel.webview.postMessage({
                        command: 'expandInstructionsSection',
                        actionName: currentAction
                      });
                    } catch (postErr) {
                      this._log(`[BotPanel] Error sending expandInstructionsSection after refresh: ${postErr.message}`);
                    }
                  }, 200);
                }
              } catch (err) {
                console.error(`[BotPanel] Refresh error: ${err.message}`);
              }
            })();
            return;
          case "toggleIncrementView":
            // Legacy support for toggle (now handled by switchViewMode)
            this._log('[BotPanel] toggleIncrementView: switching to ' + message.currentView);
            this._currentStoryMapView = message.currentView;
            // Refresh the panel to show the new view
            (async () => {
              try {
                await this._update();
              } catch (err) {
                console.error(`[BotPanel] Toggle view error: ${err.message}`);
              }
            })();
            return;
          case "switchViewMode":
            // Switch between Hierarchy, Increment, and Files views
            this._log('[BotPanel] switchViewMode: switching to ' + message.viewMode);
            this._currentStoryMapView = message.viewMode;
            // Refresh the panel to show the new view
            (async () => {
              try {
                await this._update();
              } catch (err) {
                console.error(`[BotPanel] Switch view error: ${err.message}`);
              }
            })();
            return;
          case "logToFile":
            if (message.message) {
              const fs = require('fs');
              const logPath = path.join(this._workspaceRoot, 'panel_clicks.log');
              const timestamp = new Date().toISOString();
              fs.appendFileSync(logPath, `[${timestamp}] ${message.message}\n`);
            }
            return;
          case "copyNodeToClipboard":
            (async () => {
              const nodePath = message.nodePath;
              const action = message.action; // 'name' or 'json'
              if (!nodePath || !action) return;
              const method = action === 'json' ? 'copy_json' : 'copy_name';
              const command = nodePath + '.' + method;
              try {
                const response = await this._botView.execute(command);
                const result = response && (response.result !== undefined ? response.result : response);
                const text = action === 'json'
                  ? (typeof result === 'string' ? result : JSON.stringify(result, null, 2))
                  : String(result != null ? result : '');
                await vscode.env.clipboard.writeText(text);
                vscode.window.setStatusBarMessage(action === 'json' ? 'Node JSON copied to clipboard' : 'Node name copied to clipboard', 2000);
              } catch (err) {
                this._log(`[BotPanel] copyNodeToClipboard failed: ${err.message}`);
                vscode.window.showErrorMessage(`Copy failed: ${err.message}`);
              }
            })();
            return;
          case "openFile":
            this._log('[BotPanel] openFile message received with filePath: ' + message.filePath);
            if (message.filePath) {
              const rawPath = message.filePath;
              const cleanPath = rawPath.split('#')[0];
              const fragment = rawPath.includes('#') 
                ? rawPath.split('#')[1] 
                : null;
              
              let lineNumber = null;
              let symbolName = null;
              
              if (fragment) {
                if (fragment.startsWith('L')) {
                  lineNumber = parseInt(fragment.substring(1));
                } else {
                  symbolName = fragment;
                }
              }
              
              // Normalize file path; handle file:// URIs and encoded characters
              let absolutePath;
              if (cleanPath.startsWith('file://')) {
                absolutePath = vscode.Uri.parse(cleanPath).fsPath;
              } else {
                const decoded = decodeURIComponent(cleanPath);
                absolutePath = path.isAbsolute(decoded) 
                  ? decoded 
                  : path.join(this._workspaceRoot, decoded);
              }
              const fileUri = vscode.Uri.file(absolutePath);
              
              // Check if path is a directory
              const fs = require('fs');
              if (fs.existsSync(absolutePath) && fs.statSync(absolutePath).isDirectory()) {
                // Reveal directory in VS Code file explorer
                vscode.commands.executeCommand('revealInExplorer', fileUri).catch((error) => {
                  vscode.window.showErrorMessage(`Failed to reveal folder: ${message.filePath}\n${error.message}`);
                });
              } else {
                const fileExtension = cleanPath.split('.').pop().toLowerCase();
                const binaryOrSpecialExtensions = ['drawio', 'png', 'jpg', 'jpeg', 'gif', 'pdf', 'svg'];
                // Use vscode.open for JSON files to avoid VS Code's 15MB text editor bug
                const useVscodeOpenExtensions = ['json'];
                
                // Check file size - use vscode.open for large files (>10MB) to avoid VS Code text editor limit
                const MAX_TEXT_FILE_SIZE = 10 * 1024 * 1024; // 10MB
                let fileSize = 0;
                try {
                  if (fs.existsSync(absolutePath)) {
                    fileSize = fs.statSync(absolutePath).size;
                  }
                } catch (e) {
                  // Ignore errors, proceed with default handling
                }
                
                if (binaryOrSpecialExtensions.includes(fileExtension)) {
                  vscode.commands.executeCommand('vscode.open', fileUri).catch((error) => {
                    vscode.window.showErrorMessage(`Failed to open file: ${message.filePath}\n${error.message}`);
                  });
                } else if (useVscodeOpenExtensions.includes(fileExtension)) {
                  // Use vscode.open for JSON to avoid showTextDocument bugs
                  vscode.commands.executeCommand('vscode.open', fileUri).catch((error) => {
                    vscode.window.showErrorMessage(`Failed to open file: ${message.filePath}\n${error.message}`);
                  });
                } else if (fileSize > MAX_TEXT_FILE_SIZE) {
                  // Large file - use vscode.open to avoid text editor memory limit
                  this._log(`[BotPanel] File exceeds ${MAX_TEXT_FILE_SIZE} bytes (${fileSize}), using vscode.open`);
                  vscode.commands.executeCommand('vscode.open', fileUri).catch((error) => {
                    vscode.window.showErrorMessage(`Failed to open file: ${message.filePath}\n${error.message}`);
                  });
                } else if (fileExtension === 'md') {
                  // Open markdown files in preview mode
                  vscode.commands.executeCommand('markdown.showPreview', fileUri).catch((error) => {
                    vscode.window.showErrorMessage(`Failed to open markdown preview: ${message.filePath}\n${error.message}`);
                  });
                } else {
                const openOptions = { viewColumn: vscode.ViewColumn.One, preserveFocus: false };
                
                if (lineNumber && !symbolName) {
                  openOptions.selection = new vscode.Range(lineNumber - 1, 0, lineNumber - 1, 0);
                  vscode.window.showTextDocument(fileUri, openOptions).catch((error) => {
                    vscode.window.showErrorMessage(`Failed to open file: ${message.filePath}\n${error.message}`);
                  });
                } else if (symbolName) {
                  vscode.workspace.openTextDocument(fileUri).then(
                    (doc) => {
                      const text = doc.getText();
                      const lines = text.split('\n');
                      let foundLine = -1;
                      
                      for (let i = 0; i < lines.length; i++) {
                        const line = lines[i];
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
                        openOptions.selection = new vscode.Range(foundLine, 0, foundLine, 0);
                      }
                      vscode.window.showTextDocument(doc, openOptions);
                    },
                    (error) => {
                      vscode.window.showErrorMessage(`Failed to open file: ${message.filePath}\n${error.message}`);
                    }
                  );
                } else {
                  vscode.window.showTextDocument(fileUri, openOptions).catch((error) => {
                    vscode.window.showErrorMessage(`Failed to open file: ${message.filePath}\n${error.message}`);
                  });
                }
                }
              }
            }
            return;
          case "openFiles":
            this._log('[BotPanel] openFiles message received with ' + (message.filePaths && message.filePaths.length) + ' paths');
            if (message.filePaths && Array.isArray(message.filePaths) && message.filePaths.length > 0) {
              for (const filePath of message.filePaths) {
                if (!filePath) continue;
                const pathStr = typeof filePath === 'string' ? filePath : (filePath.url || filePath.file || '');
                if (!pathStr) continue;
                const rawPath = pathStr.split('#')[0];
                const fragment = pathStr.includes('#') ? pathStr.split('#')[1] : null;
                let lineNumber = null;
                if (fragment && fragment.startsWith('L')) {
                  lineNumber = parseInt(fragment.substring(1));
                }
                let absolutePath;
                if (rawPath.startsWith('file://')) {
                  absolutePath = vscode.Uri.parse(rawPath).fsPath;
                } else {
                  const decoded = decodeURIComponent(rawPath);
                  absolutePath = path.isAbsolute(decoded) ? decoded : path.join(this._workspaceRoot, decoded);
                }
                const fs = require('fs');
                if (!fs.existsSync(absolutePath) || fs.statSync(absolutePath).isDirectory()) continue;
                const fileExtension = rawPath.split('.').pop().toLowerCase();
                const uri = lineNumber
                  ? vscode.Uri.file(absolutePath).with({ fragment: `L${lineNumber}` })
                  : vscode.Uri.file(absolutePath);
                vscode.commands.executeCommand('vscode.open', uri).catch((err) => {
                  this._log(`[BotPanel] openFiles failed for ${pathStr}: ${err.message}`);
                });
              }
            }
            return;
          case "openFileInColumn":
            this._log('[BotPanel] openFileInColumn message received');
            if (message.filePath) {
              const rawPath = message.filePath;
              const cleanPath = rawPath.split('#')[0];
              const viewColumn = message.viewColumn || 'Beside';
              
              let absolutePath;
              if (cleanPath.startsWith('file://')) {
                absolutePath = vscode.Uri.parse(cleanPath).fsPath;
              } else {
                const decoded = decodeURIComponent(cleanPath);
                absolutePath = path.isAbsolute(decoded) 
                  ? decoded 
                  : path.join(this._workspaceRoot, decoded);
              }
              const fileUri = vscode.Uri.file(absolutePath);
              
              const columnMap = {
                'One': vscode.ViewColumn.One,
                'Two': vscode.ViewColumn.Two,
                'Three': vscode.ViewColumn.Three,
                'Four': vscode.ViewColumn.Four,
                'Beside': vscode.ViewColumn.Beside,
                'Active': vscode.ViewColumn.Active
              };
              const targetColumn = columnMap[viewColumn] || vscode.ViewColumn.One;
              
              // Use vscode.open for JSON files to avoid VS Code's 15MB text editor bug
              const fileExtension = cleanPath.split('.').pop().toLowerCase();
              if (fileExtension === 'json') {
                vscode.commands.executeCommand('vscode.open', fileUri).catch((error) => {
                  vscode.window.showErrorMessage(`Failed to open file: ${message.filePath}\n${error.message}`);
                });
              } else {
                vscode.window.showTextDocument(fileUri, { viewColumn: targetColumn, preserveFocus: false }).catch((error) => {
                  vscode.window.showErrorMessage(`Failed to open file: ${message.filePath}\n${error.message}`);
                });
              }
            }
            return;
          case "openFileWithState":
            this._log('[BotPanel] openFileWithState message received');
            if (message.filePath) {
              // Open file and apply state (collapse/expand)
              const rawPath = message.filePath;
              const cleanPath = rawPath.split('#')[0];
              let absolutePath;
              if (cleanPath.startsWith('file://')) {
                absolutePath = vscode.Uri.parse(cleanPath).fsPath;
              } else {
                const decoded = decodeURIComponent(cleanPath);
                absolutePath = path.isAbsolute(decoded) 
                  ? decoded 
                  : path.join(this._workspaceRoot, decoded);
              }
              const fileUri = vscode.Uri.file(absolutePath);
              
              // Use vscode.open for JSON files (not openTextDocument) to avoid extension sync / text editor limits
              const fileExtension = cleanPath.split('.').pop().toLowerCase();
              if (fileExtension === 'json' && message.state && message.state.selectedNode) {
                // JSON with selectedNode: read via fs, find line, open with vscode.open + fragment
                const node = message.state.selectedNode;
                let startLine = 0;
                try {
                  const fs = require('fs');
                  const text = fs.readFileSync(absolutePath, 'utf8');
                  const lines = text.split('\n');
                  const escapedName = node.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                  const namePattern = new RegExp(`"name"\\s*:\\s*"${escapedName}"`);
                  let nameLineIndex = -1;
                  for (let i = 0; i < lines.length; i++) {
                    if (namePattern.test(lines[i])) {
                      nameLineIndex = i;
                      break;
                    }
                  }
                  if (nameLineIndex >= 0) {
                    startLine = nameLineIndex;
                    for (let i = nameLineIndex - 1; i >= 0; i--) {
                      const line = lines[i].trim();
                      if (line === '{' || line.endsWith('{')) {
                        startLine = i;
                        break;
                      }
                      if (line.startsWith('}') || line === '},') break;
                    }
                  }
                } catch (e) {
                  this._log(`[BotPanel] Could not search for node: ${e.message}`);
                }
                const uriWithFragment = vscode.Uri.file(absolutePath).with({ fragment: `L${startLine + 1}` });
                vscode.commands.executeCommand('vscode.open', uriWithFragment).catch((error) => {
                  vscode.window.showErrorMessage(`Failed to open file: ${message.filePath}\n${error.message}`);
                });
                this._log(`[BotPanel] JSON file opened with state: selectedNode=${node.name}`);
              } else if (fileExtension === 'json') {
                // JSON files without selectedNode - just open
                vscode.commands.executeCommand('vscode.open', fileUri).catch((error) => {
                  vscode.window.showErrorMessage(`Failed to open file: ${message.filePath}\n${error.message}`);
                });
              } else if (message.state && message.state.lineNumber) {
                const options = {
                  viewColumn: vscode.ViewColumn.One,
                  selection: new vscode.Range(message.state.lineNumber - 1, 0, message.state.lineNumber - 1, 0),
                  preserveFocus: false
                };
                vscode.window.showTextDocument(fileUri, options).then(() => {
                  this._log(`[BotPanel] File opened with state: lineNumber=${message.state.lineNumber}`);
                }).catch((error) => {
                  vscode.window.showErrorMessage(`Failed to open file: ${message.filePath}\n${error.message}`);
                });
              } else if (message.state && message.state.selectedNode) {
                // Need to search document for node - use openTextDocument
                vscode.workspace.openTextDocument(fileUri).then(
                  (doc) => {
                    const node = message.state.selectedNode;
                    const text = doc.getText();
                    const lines = text.split('\n');
                    
                    let nameLineIndex = -1;
                    const escapedName = node.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                    const namePattern = new RegExp(`"name"\\s*:\\s*"${escapedName}"`);
                    
                    for (let i = 0; i < lines.length; i++) {
                      if (namePattern.test(lines[i])) {
                        nameLineIndex = i;
                        break;
                      }
                    }
                    
                    let options = { viewColumn: vscode.ViewColumn.One, preserveFocus: false };
                    
                    if (nameLineIndex >= 0) {
                      // Find the opening brace of this object (search backwards)
                      let startLine = nameLineIndex;
                      for (let i = nameLineIndex - 1; i >= 0; i--) {
                        const line = lines[i].trim();
                        if (line === '{' || line.endsWith('{')) {
                          startLine = i;
                          break;
                        }
                        if (line.startsWith('}') || line === '},') {
                          break;
                        }
                      }
                      
                      // Find the matching closing brace (count braces forward)
                      let braceCount = 0;
                      let endLine = nameLineIndex;
                      let started = false;
                      
                      for (let i = startLine; i < lines.length; i++) {
                        const line = lines[i];
                        for (const char of line) {
                          if (char === '{') {
                            braceCount++;
                            started = true;
                          } else if (char === '}') {
                            braceCount--;
                            if (started && braceCount === 0) {
                              endLine = i;
                              break;
                            }
                          }
                        }
                        if (started && braceCount === 0) break;
                      }
                      
                      // Select from start of opening brace line to end of closing brace line
                      const endLineLength = lines[endLine] ? lines[endLine].length : 0;
                      options.selection = new vscode.Range(startLine, 0, endLine, endLineLength);
                    }
                    
                    vscode.window.showTextDocument(doc, options).then(() => {
                      this._log(`[BotPanel] File opened with state: selectedNode=${node.name}`);
                    });
                  },
                  (error) => {
                    // Fallback: open file without positioning
                    vscode.window.showTextDocument(fileUri, { viewColumn: vscode.ViewColumn.One, preserveFocus: false }).catch(() => {
                      vscode.window.showErrorMessage(`Failed to open file: ${message.filePath}\n${error.message}`);
                    });
                  }
                );
              } else {
                // No state - just open the file directly
                vscode.window.showTextDocument(fileUri, { viewColumn: vscode.ViewColumn.One, preserveFocus: false }).catch((error) => {
                  vscode.window.showErrorMessage(`Failed to open file: ${message.filePath}\n${error.message}`);
                });
              }
            }
            return;
          case "openStoryFiles":
          case "openTestFiles":
          case "openCodeFiles":
          case "openAllRelatedFiles":
            // These commands need to query story graph data, so delegate to bot
            this._log(`[BotPanel] ${message.command} message received for node: ${message.nodeName}`);
            this._handleOpenRelatedFiles(message);
            return;
          case "clearScopeFilter":
            this._botView?.execute('scope all')
              .then(() => this._update())
              .catch((error) => {
                this._log(`[BotPanel] ERROR clearScopeFilter: ${error.message}`);
                vscode.window.showErrorMessage(`Failed to clear scope: ${error.message}`);
                this._displayError(`Failed to clear scope: ${error.message}`);
              });
            return;
          case "showAllScope":
            this._botView?.execute('scope showall')
              .then(() => this._update())
              .catch((error) => {
                this._log(`[BotPanel] ERROR showAllScope: ${error.message}`);
                vscode.window.showErrorMessage(`Failed to show all: ${error.message}`);
                this._displayError(`Failed to show all: ${error.message}`);
              });
            return;
          case "updateIncludeLevel":
            this._log('[BotPanel] Received updateIncludeLevel: ' + message.includeLevel);
            
            if (!this._botView) {
              const errorMsg = '_botView is null, cannot update include_level';
              this._log('[BotPanel] ERROR: ' + errorMsg);
              this._displayError(errorMsg);
              return;
            }
            
            // Execute scope include_level command to update bot and persist to scope.json
            const scopeIncludeCmd = `scope include_level=${message.includeLevel}`;
            this._botView.execute(scopeIncludeCmd)
              .then(() => {
                this._log('[BotPanel] Include level updated: ' + message.includeLevel);
                return this._update();
              })
              .catch((err) => {
                const errorMsg = 'Include level update failed: ' + err.message;
                this._log('[BotPanel] ERROR: ' + errorMsg);
                this._displayError(errorMsg);
              });
            return;
          
          case "updateFilter":
            this._log('[BotPanel] Received updateFilter: ' + message.filter);
            this._log('[BotPanel] _botView is: ' + this._botView);
            
            if (!this._botView) {
              const errorMsg = '_botView is null, cannot execute scope command';
              this._log('[BotPanel] ERROR: ' + errorMsg);
              this._displayError(errorMsg);
              return;
            }
            
            if (message.filter && message.filter.trim()) {
              const filterValue = message.filter.trim();
              // If in Files mode, prefix filter with "file:"
              const prefixedFilter = this._currentStoryMapView === 'Files' ? `file:${filterValue}` : filterValue;
              const scopeCmd = `scope "${prefixedFilter}"`;
              this._log('[BotPanel] Executing scope command: ' + scopeCmd + ' (view mode: ' + this._currentStoryMapView + ')');
              
              this._botView.execute(scopeCmd)
                .then((result) => {
                  this._log('[BotPanel] Scope filter applied, result: ' + JSON.stringify(result).substring(0, 200));
                  return this._update();
                })
                .then(() => {
                  this._log('[BotPanel] Update completed after scope filter');
                })
                .catch((err) => {
                  const errorMsg = 'Scope filter failed: ' + err.message;
                  this._log('[BotPanel] ERROR: ' + errorMsg);
                  this._log('[BotPanel] ERROR stack: ' + err.stack);
                  this._displayError(errorMsg);
                  vscode.window.showErrorMessage(errorMsg);
                  // Don't re-throw - show error but don't crash panel
                });
            } else {
              // Empty filter = clear filter
              this._log('[BotPanel] Clearing scope filter');
              
              this._botView.execute('scope all')
                .then((result) => {
                  this._log('[BotPanel] Scope cleared successfully');
                  return this._update();
                })
                .catch((err) => {
                  const errorMsg = 'Clear scope failed: ' + err.message;
                  this._log('[BotPanel] ERROR: ' + errorMsg);
                  this._log('[BotPanel] ERROR stack: ' + err.stack);
                  this._displayError(errorMsg);
                  vscode.window.showErrorMessage(errorMsg);
                  // Don't re-throw - show error but don't crash panel
                });
            }
            return;
          case "updateWorkspace":
            this._log('[BotPanel] Received updateWorkspace message: ' + message.workspacePath);
            if (message.workspacePath) {
              this._botView?.handleEvent('updateWorkspace', { workspacePath: message.workspacePath })
                .then((result) => {
                  this._log('[BotPanel] updateWorkspace result: ' + JSON.stringify(result));
                  this._workspaceRoot = message.workspacePath;
                  return this._update();
                })
                .catch((error) => {
                  this._log('[BotPanel] ERROR updateWorkspace: ' + error.message);
                  this._log('[BotPanel] ERROR stack: ' + error.stack);
                  vscode.window.showErrorMessage(`Failed to update workspace: ${error.message}`);
                });
            }
            return;
          case "browseWorkspace":
            this._log('[BotPanel] Received browseWorkspace message');
            vscode.window.showOpenDialog({
              canSelectFiles: false,
              canSelectFolders: true,
              canSelectMany: false,
              openLabel: 'Select Workspace Folder'
            }).then((folders) => {
              if (folders && folders.length > 0) {
                const folderPath = folders[0].fsPath;
                this._log('[BotPanel] User selected folder: ' + folderPath);
                // Update the workspace input in the webview
                this._panel.webview.postMessage({
                  command: 'setWorkspacePath',
                  path: folderPath
                });
                // Trigger workspace update
                this._botView?.handleEvent('updateWorkspace', { workspacePath: folderPath })
                  .then((result) => {
                    this._log('[BotPanel] browseWorkspace updateWorkspace result: ' + JSON.stringify(result));
                    this._workspaceRoot = folderPath;
                    return this._update();
                  })
                  .catch((error) => {
                    this._log('[BotPanel] ERROR browseWorkspace: ' + error.message);
                    vscode.window.showErrorMessage(`Failed to update workspace: ${error.message}`);
                  });
              }
            });
            return;
          case "switchBot":
            if (message.botName) {
              this._botView?.headerView?.handleEvent('switchBot', { botName: message.botName })
                .then(() => this._update())
                .catch((error) => {
                  vscode.window.showErrorMessage(`Failed to switch bot: ${error.message}`);
                });
            }
            return;
          case "getBehaviorRules":
            if (message.behaviorName) {
              this._log(`[BotPanel] getBehaviorRules -> ${message.behaviorName}`);
              this._log(`[getBehaviorRules] STARTED for behavior: ${message.behaviorName}`);
              
              // Execute submitrules CLI command to submit rules to chat
              this._botView?.execute(`submitrules:${message.behaviorName}`)
                .then((result) => {
                  this._log('[BotPanel] Rules submitted:', result);
                  this._log(`[getBehaviorRules] Result received: ${JSON.stringify(result, null, 2)}`);
                  
                  // Handle dictionary response from Python
                  if (result && typeof result === 'object') {
                    this._log(`[getBehaviorRules] Result is object with status: ${result.status}`);
                    if (result.status === 'success') {
                      const msg = result.message || `${message.behaviorName} rules submitted to chat!`;
                      this._log(`[getBehaviorRules] SUCCESS - showing message: ${msg}`);
                      vscode.window.showInformationMessage(msg);
                    } else if (result.status === 'error') {
                      const errorMsg = result.message || 'Unknown error';
                      this._log(`[getBehaviorRules] ERROR status - showing error: ${errorMsg}`);
                      vscode.window.showErrorMessage(`Failed to submit rules: ${errorMsg}`);
                    } else {
                      // Legacy format: check output field
                      const outputStr = typeof result.output === 'string' ? result.output : '';
                      this._log(`[getBehaviorRules] Legacy format - output: ${outputStr}`);
                      if (outputStr.includes('submitted')) {
                        this._log(`[getBehaviorRules] Output includes 'submitted' - SUCCESS`);
                        vscode.window.showInformationMessage(`${message.behaviorName} rules submitted to chat!`);
                      } else {
                        const errorMsg = result.message || outputStr || 'Unknown error';
                        this._log(`[getBehaviorRules] Output does NOT include 'submitted' - ERROR: ${errorMsg}`);
                        vscode.window.showErrorMessage(`Failed to submit rules: ${errorMsg}`);
                      }
                    }
                  } else {
                    this._log(`[getBehaviorRules] Result is NOT an object - type: ${typeof result}, value: ${result}`);
                    vscode.window.showWarningMessage('Submit completed with unknown result');
                  }
                  
                  // Refresh panel to show current position
                  this._log(`[getBehaviorRules] About to refresh panel`);
                  return this._update();
                })
                .catch((error) => {
                  this._log(`[BotPanel] ERROR getting behavior rules: ${error.message}`);
                  this._log(`[getBehaviorRules] CATCH BLOCK - Error: ${error.message}, Stack: ${error.stack}`);
                  vscode.window.showErrorMessage(`Failed to get rules: ${error.message}`);
                });
            }
            return;
          case "executeNavigationCommand":
            if (message.commandText) {
              this._log(`[BotPanel] executeNavigationCommand -> ${message.commandText}`);
              this._botView?.execute(message.commandText)
                .then((result) => {
                  this._log(`[BotPanel] executeNavigationCommand success: ${message.commandText} | result keys: ${Object.keys(result || {})}`);
                  return this._update();
                })
                .catch((error) => {
                  this._log(`[BotPanel] executeNavigationCommand ERROR: ${error.message}`);
                  this._log(`[BotPanel] executeNavigationCommand STACK: ${error.stack}`);
                  vscode.window.showErrorMessage(`Failed to execute ${message.commandText}: ${error.message}`);
                });
            }
            return;
          case "renameNode":
            this._log(`[ASYNC_SAVE] [EXTENSION_HOST] ========== RENAME OPERATION RECEIVED ==========`);
            this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Received renameNode message`, {
              nodePath: message.nodePath,
              currentName: message.currentName,
              timestamp: new Date().toISOString()
            });
            if (message.nodePath && message.currentName) {
              // Prompt for new name
              this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Prompting user for new name`);
              vscode.window.showInputBox({
                prompt: `Rename "${message.currentName}"`,
                value: message.currentName,
                placeHolder: 'Enter new name'
              }).then((newName) => {
                this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] User provided new name`, {
                  newName: newName,
                  currentName: message.currentName,
                  changed: newName && newName !== message.currentName
                });
                if (newName && newName !== message.currentName) {
                  // Strip any surrounding quotes from the input first (user shouldn't need to quote the name)
                  const trimmedName = newName.trim().replace(/^"(.*)"$/, '$1');
                  // Escape quotes and backslashes in the new name
                  const escapedName = trimmedName.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
                  const command = `${message.nodePath}.rename name:"${escapedName}"`;
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Built rename command: ${command}`);
                  
                  // Send optimistic update message to webview
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Sending optimistic update to webview`);
                  this._panel.webview.postMessage({
                    command: 'optimisticRename',
                    nodePath: message.nodePath,
                    oldName: message.currentName,
                    newName: trimmedName
                  });
                  
                  // Log to file
                  const fs = require('fs');
                  const logPath = path.join(this._workspaceRoot, 'story_graph_operations.log');
                  const timestamp = new Date().toISOString();
                  const logEntry = `\n${'='.repeat(80)}\n[${timestamp}] RENAME COMMAND: ${command}\n`;
                  
                  try {
                    fs.appendFileSync(logPath, logEntry);
                  } catch (err) {
                    this._log(`[BotPanel] Failed to write to log file: ${err.message}`);
                  }
                  
                  // Execute backend command with optimistic flag
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Executing rename command via backend (optimistic)...`);
                  this._botView?.execute(command)
                    .then((result) => {
                      this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] [SUCCESS] Backend rename executed successfully`);
                      this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Result: ${JSON.stringify(result).substring(0, 500)}`);
                      
                      // Log result to file
                      const resultLog = `[${timestamp}] RESULT: ${JSON.stringify(result, null, 2)}\n`;
                      try {
                        fs.appendFileSync(logPath, resultLog);
                      } catch (err) {
                        this._log(`[BotPanel] Failed to write result to log file: ${err.message}`);
                      }
                      
                      // Send saveCompleted message for optimistic update handling
                      this._panel.webview.postMessage({
                        command: 'saveCompleted',
                        success: true,
                        result: result
                      });
                      
                      // Don't refresh - optimistic update already handled in webview
                      this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Optimistic update - skipping panel refresh`);
                      this._log(`[ASYNC_SAVE] [EXTENSION_HOST] ========== RENAME OPERATION COMPLETE ==========`);
                    })
                    .catch((error) => {
                      this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] [ERROR] Rename failed`);
                      this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] [ERROR] Error: ${error.message}`);
                      this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] [ERROR] Stack: ${error.stack}`);
                      
                      // Send error message to webview for SaveQueue rollback
                      this._panel.webview.postMessage({
                        command: 'saveCompleted',
                        success: false,
                        error: error.message
                      });
                      
                      // Log error to file
                      const errorLog = `[${timestamp}] ERROR: ${error.message}\nSTACK: ${error.stack}\n`;
                      try {
                        fs.appendFileSync(logPath, errorLog);
                      } catch (err) {
                        this._log(`[BotPanel] Failed to write error to log file: ${err.message}`);
                      }
                      
                      vscode.window.showErrorMessage(`Failed to rename: ${error.message}`);
                      
                      // Always refresh on error to show accurate backend state
                      this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] [ERROR] Refreshing panel after error...`);
                      this._update().catch(err => {
                        this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] [ERROR] Panel refresh failed: ${err.message}`);
                      });
                    });
                }
              });
            }
            return;
          case "executeCommand":
            if (message.commandText) {
              this._log(`\n${'='.repeat(80)}`);
              this._log(`[BotPanel] RECEIVED executeCommand MESSAGE`);
              this._log(`[BotPanel] commandText: ${message.commandText}`);
              
              // Detect operation types
              // Create operations can be: .create_epic, .create_story, .create (for sub-epics), create child, create epic
              const isCreateOp = message.commandText.includes('.create_') || 
                                 message.commandText.includes('.create ') || 
                                 message.commandText.match(/\.create(?:$| name:)/) ||
                                 message.commandText.includes('create child') || 
                                 message.commandText.includes('create epic');
              const isDeleteOp = message.commandText.includes('.delete');
              const isMoveOp = message.commandText.includes('.move_to');
              const isRenameOp = message.commandText.includes('.rename');
              const isStoryGraphOp = isCreateOp || isDeleteOp || isMoveOp || isRenameOp;
              
              // ALL story-changing operations use optimistic updates and skip refresh
              // This preserves the optimistic DOM updates made in the frontend
              // No need to check optimistic flag - story-changing ops always skip refresh
              
              // Special debug for submit commands
              if (message.commandText.includes('submit_required_behavior_instructions')) {
                this._log(`[BotPanel] *** SUBMIT COMMAND DETECTED ***`);
                this._log(`[BotPanel] Command contains 'submit_required_behavior_instructions': YES`);
              }
              
              this._log(`[BotPanel] Operation type detected`, {
                isMoveOp,
                isRenameOp,
                isCreateOp,
                isDeleteOp
              });
              
              // Log to file for create/delete/rename operations
              const fs = require('fs');
              const logPath = path.join(this._workspaceRoot, 'story_graph_operations.log');
              const timestamp = new Date().toISOString();
              const logEntry = `\n${'='.repeat(80)}\n[${timestamp}] RECEIVED COMMAND: ${message.commandText}\n`;
              
              try {
                fs.appendFileSync(logPath, logEntry);
              } catch (err) {
                this._log(`[BotPanel] Failed to write to log file: ${err.message}`);
              }
              
              this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [STEP 5] Executing command via backend...`);
              this._botView?.execute(message.commandText)
                .then((result) => {
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [STEP 6] [SUCCESS] Backend command executed successfully`);
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [STEP 6] Command: ${message.commandText}`);
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [STEP 6] Result: ${JSON.stringify(result).substring(0, 500)}`);
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [STEP 6] Timestamp: ${new Date().toISOString()}`);
                  
                  // Log result to file
                  const resultLog = `[${timestamp}] SUCCESS RESULT: ${JSON.stringify(result, null, 2)}\n`;
                  try {
                    fs.appendFileSync(logPath, resultLog);
                  } catch (err) {
                    this._log(`[BotPanel] Failed to write result to log file: ${err.message}`);
                  }
                  
                  // Check if this is submit_required_behavior_instructions - show submit result
                  const isSubmitInstructions = message.commandText.includes('submit_required_behavior_instructions');
                  if (isSubmitInstructions && result) {
                    this._log(`[BotPanel] Submit result from CLI: ${JSON.stringify(result).substring(0, 500)}`);
                    // Show success/error message from CLI submit
                    if (result.status === 'success') {
                      const msg = result.message || 'Instructions submitted to chat!';
                      vscode.window.showInformationMessage(msg);
                    } else {
                      const errorMsg = result.message || result.error || 'Failed to submit instructions';
                      vscode.window.showErrorMessage(`Submit failed: ${errorMsg}`);
                    }
                    // Don't refresh panel after submit - it's a read-only operation that doesn't change the story graph
                    this._log(`[BotPanel] Submit completed - skipping panel refresh (no story graph changes)`);
                    return Promise.resolve();
                  }
                  
                  // Log timestamp for when panel made a change (for behavior cache invalidation)
                  const timestampFile = path.join(this._workspaceRoot, 'docs', 'stories', '.story-graph-panel-edit-time');
                  try {
                    fs.writeFileSync(timestampFile, Date.now().toString());
                    this._log(`[BotPanel] Logged panel edit timestamp: ${Date.now()}`);
                  } catch (err) {
                    this._log(`[BotPanel] Failed to write timestamp file: ${err.message}`);
                  }
                  
                  // Notify webview of successful save
                  if (isMoveOp || isCreateOp || isDeleteOp || isRenameOp) {
                    this._log(`[BotPanel] Sending saveCompleted(success=true) to webview`);
                    this._panel.webview.postMessage({
                      command: 'saveCompleted',
                      success: true,
                      result: result
                    });
                    this._log(`[BotPanel] Message sent to webview`);
                  }
                  
                  // CRITICAL: Always skip refresh for story-changing operations
                  // All story-changing operations use optimistic updates in the frontend
                  // Refreshing would remove those optimistic updates, so we never refresh
                  if (isStoryGraphOp) {
                    this._log(`[BotPanel] Story-changing operation - skipping panel refresh`);
                    this._log(`[BotPanel] Operation type: create=${isCreateOp}, move=${isMoveOp}, delete=${isDeleteOp}, rename=${isRenameOp}`);
                    this._log(`[BotPanel] Panel will NOT refresh - optimistic updates remain visible`);
                    return Promise.resolve();
                  } else {
                    // Check if this is a scope command - needs refresh to show filtered view
                    const isScopeCommand = message.commandText.startsWith('scope ');
                    if (isScopeCommand) {
                      this._log(`[BotPanel] Scope command detected - refreshing panel to show filtered view...`);
                      return this._update();
                    }
                    
                    // Non-story operations (like submit) don't need refresh
                    this._log(`[BotPanel] Non-story operation - skipping refresh`);
                    return Promise.resolve();
                  }
                })
                .then(() => {
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [STEP 9] Panel refresh completed`);
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] ========== COMMAND FLOW COMPLETE ==========`);
                  this._log(`${'='.repeat(80)}\n`);
                })
                .catch((error) => {
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [ERROR] Command execution failed`);
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [ERROR] Command: ${message.commandText}`);
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [ERROR] Error: ${error.message}`);
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [ERROR] Stack: ${error.stack}`);
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [ERROR] Timestamp: ${new Date().toISOString()}`);
                  
                  // Log error to file
                  const errorLog = `[${timestamp}] ERROR: ${error.message}\nSTACK: ${error.stack}\n`;
                  try {
                    fs.appendFileSync(logPath, errorLog);
                  } catch (err) {
                    this._log(`[BotPanel] Failed to write error to log file: ${err.message}`);
                  }
                  
                  vscode.window.showErrorMessage(`Failed to execute ${message.commandText}: ${error.message}`);
                  
                  // Notify webview of save error
                  if (isMoveOp || isCreateOp || isDeleteOp || isRenameOp) {
                    this._log(`[BotPanel] Sending saveCompleted(success=false) to webview`);
                    this._panel.webview.postMessage({
                      command: 'saveCompleted',
                      success: false,
                      error: error.message
                    });
                    this._log(`[BotPanel] Error message sent to webview`);
                  }
                  
                  // Always refresh on error to show accurate backend state
                  // (rollback should have already happened in SaveQueue)
                  if (!isOptimistic) {
                    this._log(`[BotPanel] Refreshing panel after error...`);
                    this._update().catch(err => {
                      this._log(`[BotPanel] ERROR in _update after failure: ${err.message}`);
                    });
                  } else {
                    this._log(`[BotPanel] Optimistic operation failed - skipping refresh (rollback handled by SaveQueue)`);
                  }
                  
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] ========== COMMAND FLOW FAILED ==========`);
                  this._log(`${'='.repeat(80)}\n`);
                });
            } else {
              this._log(`[BotPanel] WARNING: executeCommand received with no commandText`);
            }
            return;
          case "navigateToBehavior":
            if (message.behaviorName) {
              const cmd = `${message.behaviorName}`;
              this._botView?.execute(cmd)
                .then((result) => {
                  // Cache the navigation result to avoid redundant CLI calls
                  if (result?.bot) {
                    this._botView.botData = result.bot;
                    // Copy instructions into botData so InstructionsSection can find them
                    if (result.instructions) {
                      this._botView.botData.instructions = result.instructions;
                    }
                    // Also cache full response for InstructionsSection
                    PanelView._lastResponse = result;
                  }
                  return this._updateWithCachedData();
                })
                .catch((error) => {
                  this._log(`[BotPanel] navigateToBehavior ERROR: ${error.message}`);
                  this._log(`[BotPanel] navigateToBehavior STACK: ${error.stack}`);
                  vscode.window.showErrorMessage(`Failed to navigate to behavior: ${error.message}`);
                });
            }
            return;
          case "navigateToAction":
            if (message.behaviorName && message.actionName) {
              const cmd = `${message.behaviorName}.${message.actionName}`;
              this._log(`[BotPanel] navigateToAction: ${cmd}`);
              this._botView?.execute(cmd)
                .then((result) => {
                  this._log(`[BotPanel] navigateToAction result keys: ${Object.keys(result || {}).join(', ')}`);
                  this._log(`[BotPanel] result.bot? ${!!result?.bot}`);
                  this._log(`[BotPanel] result.instructions? ${!!result?.instructions}`);
                  if (result?.instructions) {
                    this._log(`[BotPanel] result.instructions keys: ${Object.keys(result.instructions).join(', ')}`);
                  }
                  // Cache the navigation result to avoid redundant CLI calls
                  if (result?.bot) {
                    this._botView.botData = result.bot;
                    // Copy instructions into botData so InstructionsSection can find them
                    if (result.instructions) {
                      this._botView.botData.instructions = result.instructions;
                      this._log(`[BotPanel] Copied instructions into botData`);
                    } else {
                      this._log(`[BotPanel] WARNING: No instructions in result to copy!`);
                    }
                    // Also cache full response for InstructionsSection
                    PanelView._lastResponse = result;
                  } else {
                    this._log(`[BotPanel] WARNING: No result.bot - not caching!`);
                  }
                  return this._updateWithCachedData().then(() => {
                    // After panel update, expand the instructions section for this action
                    // Use setTimeout to ensure DOM is ready after webview.html is set
                    setTimeout(() => {
                      try {
                        this._log(`[BotPanel] Sending expandInstructionsSection for: ${message.actionName}`);
                        this._panel.webview.postMessage({
                          command: 'expandInstructionsSection',
                          actionName: message.actionName
                        });
                      } catch (postErr) {
                        this._log(`[BotPanel] Error sending expandInstructionsSection: ${postErr.message}`);
                      }
                    }, 200);
                  });
                })
                .catch((error) => {
                  this._log(`[BotPanel] navigateToAction ERROR: ${error.message}`);
                  this._log(`[BotPanel] navigateToAction STACK: ${error.stack}`);
                  vscode.window.showErrorMessage(`Failed to navigate to action: ${error.message}`);
                });
            }
            return;
          case "navigateAndExecute":
            if (message.behaviorName && message.actionName && message.operationName) {
              const command = `${message.behaviorName}.${message.actionName}.${message.operationName}`;
              this._log(`[BotPanel] navigateAndExecute -> ${command}`);
              this._botView?.execute(command)
                .then((result) => {
                  this._log(`[BotPanel] navigateAndExecute success: ${command} | result keys: ${Object.keys(result || {})}`);
                  // Cache the navigation result to avoid redundant CLI calls
                  if (result?.bot) {
                    this._botView.botData = result.bot;
                    // Copy instructions into botData so InstructionsSection can find them
                    if (result.instructions) {
                      this._botView.botData.instructions = result.instructions;
                    }
                    // Also cache full response for InstructionsSection
                    PanelView._lastResponse = result;
                  }
                  return this._updateWithCachedData();
                })
                .catch((error) => {
                  this._log(`[BotPanel] navigateAndExecute ERROR: ${error.message}`);
                  this._log(`[BotPanel] navigateAndExecute STACK: ${error.stack}`);
                  vscode.window.showErrorMessage(`Failed to execute operation: ${error.message}`);
                });
            }
            return;
          case "toggleSection":
            if (message.sectionId) {
              // Expansion state is handled client-side via JavaScript
            }
            return;
          case "toggleCollapse":
            if (message.elementId) {
              // Expansion state is handled client-side via JavaScript
            }
            return;
          case "sendToChat":
            this._log('sendToChat - calling bot submit command');
            
            // Call the bot's submit command (Python handles everything)
            this._botView?.execute('submit')
              .then((output) => {
                this._log('Bot submit command output:', output);
                
                // Handle dictionary response from Python
                if (output && typeof output === 'object' && output.status) {
                  if (output.status === 'success') {
                    const msg = output.message || 'Instructions submitted to chat!';
                    vscode.window.showInformationMessage(msg);
                  } else {
                    const errorMsg = output.message || 'Unknown error';
                    vscode.window.showErrorMessage(`Submit failed: ${errorMsg}`);
                  }
                }
                // Handle string response (legacy/CLI format)
                else {
                  const outputStr = typeof output === 'string' ? output : JSON.stringify(output || '');
                  
                  if (outputStr && (outputStr.includes('SUCCESS:') || outputStr.includes('submitted to Cursor chat successfully'))) {
                    vscode.window.showInformationMessage('Instructions submitted to chat!');
                  }
                  else if (outputStr && (outputStr.includes('ERROR:') || outputStr.includes('FAILED:'))) {
                    const errorMatch = outputStr.match(/ERROR:|FAILED:\s*(.+)/);
                    const errorMsg = errorMatch ? errorMatch[1] : 'Unknown error';
                    vscode.window.showErrorMessage(`Submit failed: ${errorMsg}`);
                  }
                  else {
                    vscode.window.showWarningMessage('Submit completed with unknown result');
                    this._log('[PANEL] Submit output:', output);
                  }
                }
              })
              .catch((error) => {
                this._log('Submit command failed:', error);
                vscode.window.showErrorMessage(`Submit command failed: ${error.message}`);
              });
            return;
          case "saveClarifyAnswers":
            if (message.answers) {
              this._log(`[BotPanel] saveClarifyAnswers -> ${JSON.stringify(message.answers)}`);
              const answersJson = JSON.stringify(message.answers).replace(/'/g, "\\'");
              const cmd = `save --answers '${answersJson}'`;
              this._botView?.execute(cmd)
                .then(() => {
                  this._log(`[BotPanel] saveClarifyAnswers success`);
                  vscode.window.showInformationMessage('Answers saved successfully');
                })
                .catch((error) => {
                  this._log(`[BotPanel] saveClarifyAnswers ERROR: ${error.message}`);
                  vscode.window.showErrorMessage(`Failed to save clarify answers: ${error.message}`);
                });
            }
            return;
          case "saveClarifyEvidence":
            if (message.evidence_provided) {
              this._log(`[BotPanel] saveClarifyEvidence -> ${JSON.stringify(message.evidence_provided)}`);
              const evidenceJson = JSON.stringify(message.evidence_provided).replace(/'/g, "\\'");
              const cmd = `save --evidence_provided '${evidenceJson}'`;
              this._botView?.execute(cmd)
                .then(() => {
                  this._log(`[BotPanel] saveClarifyEvidence success`);
                  vscode.window.showInformationMessage('Evidence saved successfully');
                })
                .catch((error) => {
                  this._log(`[BotPanel] saveClarifyEvidence ERROR: ${error.message}`);
                  vscode.window.showErrorMessage(`Failed to save clarify evidence: ${error.message}`);
                });
            }
            return;
          case "saveStrategyDecision":
            if (message.criteriaKey && message.selectedOption) {
              this._log(`[BotPanel] saveStrategyDecision -> ${message.criteriaKey}: ${message.selectedOption}`);
              // Build decisions object with just this one decision
              const decisions = {};
              decisions[message.criteriaKey] = message.selectedOption;
              const decisionsJson = JSON.stringify(decisions).replace(/'/g, "\\'");
              const cmd = `save --decisions '${decisionsJson}'`;
              this._botView?.execute(cmd)
                .then(() => {
                  this._log(`[BotPanel] saveStrategyDecision success`);
                  vscode.window.showInformationMessage('Strategy decision saved successfully');
                })
                .catch((error) => {
                  this._log(`[BotPanel] saveStrategyDecision ERROR: ${error.message}`);
                  vscode.window.showErrorMessage(`Failed to save strategy decision: ${error.message}`);
                });
            }
            return;
          case "saveStrategyMultiDecision":
            if (message.criteriaKey && message.selectedOptions) {
              this._log(`[BotPanel] saveStrategyMultiDecision -> ${message.criteriaKey}: ${JSON.stringify(message.selectedOptions)}`);
              // Build decisions object with array of selected options
              const multiDecisions = {};
              multiDecisions[message.criteriaKey] = message.selectedOptions;
              const multiDecisionsJson = JSON.stringify(multiDecisions).replace(/'/g, "\\'");
              const multiCmd = `save --decisions '${multiDecisionsJson}'`;
              this._botView?.execute(multiCmd)
                .then(() => {
                  this._log(`[BotPanel] saveStrategyMultiDecision success`);
                  vscode.window.showInformationMessage('Strategy decisions saved successfully');
                })
                .catch((error) => {
                  this._log(`[BotPanel] saveStrategyMultiDecision ERROR: ${error.message}`);
                  vscode.window.showErrorMessage(`Failed to save strategy decisions: ${error.message}`);
                });
            }
            return;
          case "renderDiagram": {
            const behaviorName = this._botView?.botData?.behaviors?.current_behavior || this._botView?.botData?.current_behavior;
            if (!behaviorName) {
              vscode.window.showErrorMessage('No current behavior set');
              return;
            }
            const diagramScope = message.scope || '';
            const scopeParam = diagramScope ? ` scope:"${diagramScope}"` : '';
            const renderCmd = `${behaviorName}.render.renderDiagram${scopeParam}`;
            this._log(`[BotPanel] renderDiagram -> ${renderCmd}`);
            this._renderInProgress = true;
            vscode.window.withProgress({
              location: vscode.ProgressLocation.Notification,
              title: 'Rendering diagram...',
              cancellable: false
            }, async () => {
              try {
                const result = await this._botView.execute(renderCmd);
                if (result?.status === 'success') {
                  vscode.window.showInformationMessage(result.message || 'Diagram rendered successfully');
                  // Open the rendered diagram file (use vscode.open so DrawIO editor opens, not XML)
                  if (message.path) {
                    try {
                      // Resolve scoped filename using the same logic
                      // the Python backend applies.
                      let openPath = message.path;
                      if (diagramScope) {
                        const sanitized = diagramScope.toLowerCase().replace(/ /g, '-').replace(/[^a-z0-9-]/g, '');
                        if (openPath.includes('{scope}')) {
                          openPath = openPath.replace('{scope}', sanitized);
                        } else if (openPath.includes('-all.drawio')) {
                          openPath = openPath.replace('-all.drawio', `-${sanitized}.drawio`);
                        } else if (openPath.endsWith('.drawio')) {
                          openPath = openPath.replace('.drawio', `-${sanitized}.drawio`);
                        }
                      } else if (openPath.includes('{scope}')) {
                        openPath = openPath.replace('{scope}', 'all');
                      }
                      const diagramUri = vscode.Uri.file(openPath);
                      await vscode.commands.executeCommand('vscode.open', diagramUri);
                    } catch (openErr) {
                      this._log(`[BotPanel] renderDiagram open file error: ${openErr.message}`);
                    }
                  }
                } else {
                  vscode.window.showErrorMessage(result?.message || 'Failed to render diagram');
                }
              } catch (error) {
                this._log(`[BotPanel] renderDiagram ERROR: ${error.message}`);
                vscode.window.showErrorMessage(`Failed to render diagram: ${error.message}`);
              } finally {
                setTimeout(() => { self._renderInProgress = false; }, 2000);
              }
            });
            return;
          }
          case "saveDiagramLayout": {
            const behaviorNameLayout = this._botView?.botData?.behaviors?.current_behavior || this._botView?.botData?.current_behavior;
            if (!behaviorNameLayout) {
              vscode.window.showErrorMessage('No current behavior set');
              return;
            }
            const layoutScope = message.scope || '';
            const layoutScopeParam = layoutScope ? ` scope:"${layoutScope}"` : '';
            const layoutCmd = `${behaviorNameLayout}.render.saveDiagramLayout${layoutScopeParam}`;
            this._log('[BotPanel] saveDiagramLayout -> ' + layoutCmd);
            vscode.window.withProgress({
              location: vscode.ProgressLocation.Notification,
              title: 'Saving diagram layout...',
              cancellable: false
            }, async () => {
              try {
                const result = await this._botView.execute(layoutCmd);
                if (result?.status === 'success') {
                  vscode.window.showInformationMessage(result.message || 'Layout saved');
                } else {
                  vscode.window.showErrorMessage(result?.message || 'Failed to save layout');
                }
              } catch (error) {
                this._log('[BotPanel] saveDiagramLayout ERROR: ' + error.message);
                vscode.window.showErrorMessage('Failed to save layout: ' + error.message);
              }
            });
            return;
          }
          case "clearDiagramLayout": {
            const behaviorNameClear = this._botView?.botData?.behaviors?.current_behavior || this._botView?.botData?.current_behavior;
            if (!behaviorNameClear) {
              vscode.window.showErrorMessage('No current behavior set');
              return;
            }
            const clearScope = message.scope || '';
            const clearScopeParam = clearScope ? ` scope:"${clearScope}"` : '';
            const clearCmd = `${behaviorNameClear}.render.clearLayout${clearScopeParam}`;
            this._log('[BotPanel] clearDiagramLayout -> ' + clearCmd);
            vscode.window.withProgress({
              location: vscode.ProgressLocation.Notification,
              title: 'Clearing diagram layout...',
              cancellable: false
            }, async () => {
              try {
                const result = await this._botView.execute(clearCmd);
                if (result?.status === 'success') {
                  vscode.window.showInformationMessage(result.message || 'Layout cleared');
                } else {
                  vscode.window.showErrorMessage(result?.message || 'Failed to clear layout');
                }
              } catch (error) {
                this._log('[BotPanel] clearDiagramLayout ERROR: ' + error.message);
                vscode.window.showErrorMessage('Failed to clear layout: ' + error.message);
              }
            });
            return;
          }
          case "generateDiagramReport": {
            const behaviorName2 = this._botView?.botData?.behaviors?.current_behavior || this._botView?.botData?.current_behavior;
            if (!behaviorName2) {
              vscode.window.showErrorMessage('No current behavior set');
              return;
            }
            const reportScope = message.scope || '';
            const reportScopeParam = reportScope ? ` scope:"${reportScope}"` : '';
            const reportCmd = `${behaviorName2}.render.generateReport${reportScopeParam}`;
            this._log(`[BotPanel] generateDiagramReport -> ${reportCmd}`);
            vscode.window.withProgress({
              location: vscode.ProgressLocation.Notification,
              title: 'Generating update report from diagram...',
              cancellable: false
            }, async () => {
              try {
                const result = await this._botView.execute(reportCmd);
                if (result?.status === 'success') {
                  vscode.window.showInformationMessage(result.message || 'Report generated successfully');
                } else {
                  vscode.window.showErrorMessage(result?.message || 'Failed to generate report');
                }
                await this._update();
              } catch (error) {
                this._log(`[BotPanel] generateDiagramReport ERROR: ${error.message}`);
                vscode.window.showErrorMessage(`Failed to generate report: ${error.message}`);
              }
            });
            return;
          }
          case "updateFromDiagram": {
            const behaviorName3 = this._botView?.botData?.behaviors?.current_behavior || this._botView?.botData?.current_behavior;
            if (!behaviorName3) {
              vscode.window.showErrorMessage('No current behavior set');
              return;
            }
            const updateScope = message.scope || '';
            const updateScopeParam = updateScope ? ` scope:"${updateScope}"` : '';
            const updateCmd = `${behaviorName3}.render.updateFromDiagram${updateScopeParam}`;
            this._log(`[BotPanel] updateFromDiagram -> ${updateCmd}`);
            vscode.window.withProgress({
              location: vscode.ProgressLocation.Notification,
              title: 'Updating story graph from diagram...',
              cancellable: false
            }, async () => {
              try {
                const result = await this._botView.execute(updateCmd);
                if (result?.status === 'success') {
                  vscode.window.showInformationMessage(result.message || 'Story graph updated successfully');
                } else {
                  vscode.window.showErrorMessage(result?.message || 'Failed to update story graph');
                }
                // Clear cached data so panel reloads fresh story map
                if (this._botView) {
                  this._botView.botData = null;
                }
                await this._update();
              } catch (error) {
                this._log(`[BotPanel] updateFromDiagram ERROR: ${error.message}`);
                vscode.window.showErrorMessage(`Failed to update from diagram: ${error.message}`);
              }
            });
            return;
          }
          case "saveStrategyAssumptions":
            if (message.assumptions) {
              this._log(`[BotPanel] saveStrategyAssumptions -> ${JSON.stringify(message.assumptions)}`);
              const assumptionsJson = JSON.stringify(message.assumptions).replace(/'/g, "\\'");
              const cmd = `save --assumptions '${assumptionsJson}'`;
              this._botView?.execute(cmd)
                .then(() => {
                  this._log(`[BotPanel] saveStrategyAssumptions success`);
                  vscode.window.showInformationMessage('Strategy assumptions saved successfully');
                })
                .catch((error) => {
                  this._log(`[BotPanel] saveStrategyAssumptions ERROR: ${error.message}`);
                  vscode.window.showErrorMessage(`Failed to save strategy assumptions: ${error.message}`);
                });
            }
            return;
        }
      },
      null,
      this._disposables
    );
  }

  static createOrShow(workspaceRoot, extensionUri) {
    console.log(`[BotPanel] >>> ENTERING createOrShow - workspaceRoot: ${workspaceRoot}`);
    console.log(`[BotPanel] >>> extensionUri: ${extensionUri}`);
    
    try {
      const column = vscode.ViewColumn.Two;
      console.log(`[BotPanel] >>> Column set: ${column}`);

      // If we already have a panel, show it
      if (BotPanel.currentPanel) {
        console.log("[BotPanel] >>> Reusing existing panel");
        BotPanel.currentPanel._panel.reveal(column);
        return;
      }

      console.log("[BotPanel] >>> Creating new webview panel");
      // Otherwise, create a new panel
      const panel = vscode.window.createWebviewPanel(
        BotPanel.viewType,
        "Bot Panel",
        column,
        {
          enableScripts: true,
          retainContextWhenHidden: false,
          localResourceRoots: [
            extensionUri
          ],
        }
      );
      console.log("[BotPanel] >>> Webview panel created");

      console.log("[BotPanel] >>> Instantiating BotPanel class");
      BotPanel.currentPanel = new BotPanel(panel, workspaceRoot, extensionUri);
      console.log("[BotPanel] >>> BotPanel instance created successfully");
    } catch (error) {
      console.error(`[BotPanel] >>> EXCEPTION in createOrShow: ${error.message}`);
      console.error(`[BotPanel] >>> Stack: ${error.stack}`);
      vscode.window.showErrorMessage(`Bot Panel Error: ${error.message}`);
      throw error;
    }
  }

  /**
   * Create a BotPanel instance for use in a sidebar WebviewView.
   * Unlike createOrShow, this doesn't create a new WebviewPanel - it uses an existing WebviewView.
   * 
   * @param {vscode.WebviewView} webviewView - The sidebar webview view
   * @param {string} workspaceRoot - Workspace root path
   * @param {vscode.Uri} extensionUri - Extension URI for resources
   * @returns {BotPanel} The BotPanel instance
   */
  static createForSidebar(webviewView, workspaceRoot, extensionUri) {
    console.log("[BotPanel] Creating for sidebar view");
    
    // Create a wrapper object that mimics WebviewPanel interface
    const panelWrapper = {
      webview: webviewView.webview,
      onDidDispose: webviewView.onDidDispose.bind(webviewView),
      // WebviewView doesn't have these, so provide no-ops that return disposables
      onDidChangeViewState: (callback, thisArg, disposables) => {
        // WebviewView has onDidChangeVisibility instead
        return webviewView.onDidChangeVisibility(() => {
          // Create a fake event object
          callback({ webviewView: webviewView });
        }, thisArg, disposables);
      },
      reveal: () => {},
      dispose: () => {}
    };
    
    // Create new BotPanel instance using the wrapper
    const botPanel = new BotPanel(panelWrapper, workspaceRoot, extensionUri);
    
    // Don't set as currentPanel - sidebar and editor panels can coexist
    console.log("[BotPanel] Sidebar instance created successfully");
    
    return botPanel;
  }

  _readPanelVersion() {
    try {
      // Try multiple locations for package.json
      const possiblePaths = [
        path.join(__dirname, "package.json"),
        path.join(__dirname, "..", "package.json"),
        path.join(__dirname, "..", "..", "package.json")
      ];
      
      for (const packageJsonPath of possiblePaths) {
        try {
          if (fs.existsSync(packageJsonPath)) {
            console.log(`[BotPanel] Found package.json at: ${packageJsonPath}`);
      const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, "utf8"));
            if (packageJson.version) {
              console.log(`[BotPanel] Panel version: ${packageJson.version}`);
              return packageJson.version;
            }
          }
        } catch (err) {
          console.log(`[BotPanel] Could not read package.json at ${packageJsonPath}: ${err.message}`);
        }
      }
      
      console.warn("[BotPanel] Could not find package.json in any expected location");
      return null;
    } catch (error) {
      console.error("[BotPanel] Failed to read panel version:", error);
      return null;
    }
  }

  async _handleOpenRelatedFiles(message) {
    try {
      const { command, nodeType, nodeName, nodePath, singleFileLink, storyGraphPath } = message;
      this._log(`[BotPanel] _handleOpenRelatedFiles: ${command} for ${nodeType} "${nodeName}"`);
      
      if (!this._botView) {
        vscode.window.showErrorMessage('Bot view not available');
        return;
      }
      
      // Verify story graph is available (but don't fail if it's not in the expected format)
      try {
        const storyGraph = await this._botView.execute('story_graph');
        this._log(`[BotPanel] Story graph check result: ${JSON.stringify(storyGraph)}`);
      } catch (error) {
        this._log(`[BotPanel] Story graph check failed (continuing anyway): ${error.message}`);
      }
      
      const fs = require('fs');
      const path = require('path');
      const workspaceRoot = this._workspaceRoot;
      
      // Helper to resolve file path
      const resolvePath = (filePath) => {
        if (!filePath) return null;
        if (path.isAbsolute(filePath)) return filePath;
        return path.join(workspaceRoot, filePath);
      };
      
      // Helper to open file in column
      const openInColumn = async (filePath, column, options = {}) => {
        const absolutePath = resolvePath(filePath);
        if (!absolutePath || !fs.existsSync(absolutePath)) {
          this._log(`[BotPanel] File not found: ${filePath}`);
          return;
        }
        const fileUri = vscode.Uri.file(absolutePath);
        
        // Use vscode.open for JSON files to avoid VS Code's 15MB text editor bug
        const fileExtension = filePath.split('.').pop().toLowerCase();
        if (fileExtension === 'json') {
          await vscode.commands.executeCommand('vscode.open', fileUri);
          return;
        }
        
        const doc = await vscode.workspace.openTextDocument(fileUri);
        // Open as a new tab (preview: false) without taking focus (preserveFocus: true)
        const openOptions = { 
          viewColumn: column, 
          preview: false,
          preserveFocus: true,
          ...options 
        };
        await vscode.window.showTextDocument(doc, openOptions);
      };
      
      if (command === 'openStoryFiles') {
        // Open story markdown files
        if (singleFileLink) {
          // Single story - open normally
          await openInColumn(singleFileLink, vscode.ViewColumn.One);
        } else {
          // Query for all story files under node
          this._log(`[BotPanel] Opening story files for ${nodeType} "${nodeName}"`);
          
          // Use the openStoryFile domain API to get all story files
          try {
            const result = await this._botView.execute(`story_graph.${nodePath || `"${nodeName}"`}.openStoryFile()`);
            if (result && result.files && Array.isArray(result.files)) {
              // Open files normally (not in separate panes)
              for (const filePath of result.files) {
                await openInColumn(filePath, vscode.ViewColumn.One);
              }
              this._log(`[BotPanel] Opened ${result.files.length} story files`);
            }
          } catch (error) {
            this._log(`[BotPanel] Error getting story files: ${error.message}`);
            // Fallback: try to discover files from story graph structure
            // TODO: Implement story file discovery from story graph
          }
        }
      } else if (command === 'openTestFiles') {
        // Open test files - use vscode.open (not openTextDocument) to avoid extension sync issues
        this._log(`[BotPanel] Opening test files for ${nodeType} "${nodeName}"`);
        
        try {
          const result = await this._botView.execute(`story_graph.${nodePath || `"${nodeName}"`}.openTest()`);
          if (result && result.files && Array.isArray(result.files)) {
            const paths = result.files.map(f => (typeof f === 'string' ? f : f.file)).filter(Boolean);
            await this._openTestFiles(paths);
          }
        } catch (error) {
          this._log(`[BotPanel] Error getting test files: ${error.message}`);
          vscode.window.showErrorMessage(`Failed to open test files: ${error.message}`);
        }
      } else if (command === 'openCodeFiles') {
        // Trace imports in test files to find and open code files
        this._log(`[BotPanel] Opening code files traced from tests for ${nodeType} "${nodeName}"`);
        
        try {
          const result = await this._botView.execute(`story_graph.${nodePath || `"${nodeName}"`}.openCode()`);
          if (result && result.files && Array.isArray(result.files)) {
            for (const codeFilePath of result.files) {
              const absolutePath = path.isAbsolute(codeFilePath)
                ? codeFilePath
                : path.join(workspaceRoot, codeFilePath);
              
              if (fs.existsSync(absolutePath)) {
                const fileUri = vscode.Uri.file(absolutePath);
                const fileExtension = codeFilePath.split('.').pop().toLowerCase();
                if (fileExtension === 'json') {
                  await vscode.commands.executeCommand('vscode.open', fileUri);
                } else {
                  const doc = await vscode.workspace.openTextDocument(fileUri);
                  await vscode.window.showTextDocument(doc, {
                    viewColumn: vscode.ViewColumn.One,
                    preserveFocus: false
                  });
                }
                this._log(`[BotPanel] Opened traced code file: ${codeFilePath}`);
              } else {
                this._log(`[BotPanel] Traced code file does not exist: ${absolutePath}`);
              }
            }
            this._log(`[BotPanel] Opened ${result.files.length} traced code files`);
          }
        } catch (error) {
          this._log(`[BotPanel] Error opening code files: ${error.message}`);
          vscode.window.showErrorMessage(`Failed to open code files: ${error.message}`);
        }
      } else if (command === 'openAllRelatedFiles') {
        // Use internal helper methods
        const graphPath = storyGraphPath || path.join(workspaceRoot, 'docs/story/story-graph.json');
        const testFiles = message.testFiles || [];
        const storyFiles = message.storyFiles || [];
        const selectedNode = message.selectedNode;
        
        this._log(`[BotPanel] Opening all related files for ${nodeType} "${nodeName}"`);
        
        // 1. Open story graph with node selected
        await this._openGraphWithNodeSelected(graphPath, selectedNode);
        
        if (nodeType === 'sub-epic' || nodeType === 'epic') {
          // For sub-epics/epics: open exploration doc (sub-epic's own file link) + all child story files
          if (singleFileLink) {
            this._log(`[BotPanel] Opening exploration file for sub-epic "${nodeName}": ${singleFileLink}`);
            await this._openStoryFile(singleFileLink);
          }
          this._log(`[BotPanel] Opening ${storyFiles.length} story files for sub-epic "${nodeName}"`);
          for (const storyFilePath of storyFiles) {
            await this._openStoryFile(storyFilePath);
          }
        } else {
          // 2. Open single story file
          if (singleFileLink) {
            await this._openStoryFile(singleFileLink);
          }
        }
        
        // 3. Open test files
        if (testFiles.length > 0) {
          await this._openTestFiles(testFiles);
        }
        
        // 3.5. Open code files traced from imports in test files
        try {
          const codeResult = await this._botView.execute(`story_graph.${nodePath || `"${nodeName}"`}.openCode()`);
          if (codeResult && codeResult.files && Array.isArray(codeResult.files)) {
            for (const codeFilePath of codeResult.files) {
              const absolutePath = path.isAbsolute(codeFilePath)
                ? codeFilePath
                : path.join(workspaceRoot, codeFilePath);
              if (fs.existsSync(absolutePath)) {
                const fileUri = vscode.Uri.file(absolutePath);
                const fileExtension = codeFilePath.split('.').pop().toLowerCase();
                if (fileExtension === 'json') {
                  await vscode.commands.executeCommand('vscode.open', fileUri);
                } else {
                  const doc = await vscode.workspace.openTextDocument(fileUri);
                  await vscode.window.showTextDocument(doc, {
                    viewColumn: vscode.ViewColumn.One,
                    preserveFocus: false
                  });
                }
                this._log(`[BotPanel] Opened traced code file: ${codeFilePath}`);
              } else {
                this._log(`[BotPanel] Traced code file does not exist: ${absolutePath}`);
              }
            }
            this._log(`[BotPanel] Opened ${codeResult.files.length} traced code files`);
          }
        } catch (codeErr) {
          this._log(`[BotPanel] Error tracing code files: ${codeErr.message}`);
        }
        
        // 4. Activate the story graph tab as the last step (use vscode.open for JSON, not openTextDocument)
        const graphAbsPath = path.isAbsolute(graphPath) ? graphPath : path.join(workspaceRoot, graphPath);
        try {
          await vscode.commands.executeCommand('vscode.open', vscode.Uri.file(graphAbsPath));
        } catch (e) {
          this._log(`[BotPanel] Could not re-activate story graph tab: ${e.message}`);
        }
      }
    } catch (error) {
      this._log(`[BotPanel] ERROR in _handleOpenRelatedFiles: ${error.message}`);
      vscode.window.showErrorMessage(`Failed to open related files: ${error.message}`);
    }
  }

  /**
   * Open story graph JSON file with a specific node selected and scrolled into view.
   * @param {string} graphPath - Path to story-graph.json
   * @param {object} selectedNode - Node to select (with name, type, path properties)
   */
  async _openGraphWithNodeSelected(graphPath, selectedNode) {
    const fs = require('fs');
    const path = require('path');
    
    const absolutePath = path.isAbsolute(graphPath) 
      ? graphPath 
      : path.join(this._workspaceRoot, graphPath);
    
    // Use vscode.open for JSON (not openTextDocument) to avoid extension sync / text editor limits
    if (!selectedNode || !selectedNode.name) {
      await vscode.commands.executeCommand('vscode.open', vscode.Uri.file(absolutePath));
      return;
    }
    
    // Read file via fs to find node line - avoids openTextDocument which fails for large JSON
    let startLine = 0;
    try {
      const text = fs.readFileSync(absolutePath, 'utf8');
      const lines = text.split('\n');
      const escapedName = selectedNode.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const namePattern = new RegExp(`"name"\\s*:\\s*"${escapedName}"`);
      
      let nameLineIndex = -1;
      for (let i = 0; i < lines.length; i++) {
        if (namePattern.test(lines[i])) {
          nameLineIndex = i;
          break;
        }
      }
      
      if (nameLineIndex >= 0) {
        for (let i = nameLineIndex - 1; i >= 0; i--) {
          const line = lines[i].trim();
          if (line === '{' || line.endsWith('{')) {
            startLine = i;
            break;
          }
          if (line.startsWith('}') || line === '},') break;
        }
      }
    } catch (e) {
      this._log(`[BotPanel] Could not search for node in graph: ${e.message}`);
    }
    
    const uri = vscode.Uri.file(absolutePath).with({ fragment: `L${startLine + 1}` });
    await vscode.commands.executeCommand('vscode.open', uri);
    this._log(`[BotPanel] Graph opened with node selected: ${selectedNode.name}`);
  }

  /**
   * Open a story markdown file.
   * @param {string} filePath - Path to the story .md file
   */
  async _openStoryFile(filePath) {
    const fs = require('fs');
    const path = require('path');
    
    if (!filePath) return;
    
    const cleanPath = filePath.split('#')[0];
    const absolutePath = path.isAbsolute(cleanPath) 
      ? cleanPath 
      : path.join(this._workspaceRoot, cleanPath);
    
    if (!fs.existsSync(absolutePath)) {
      this._log(`[BotPanel] Story file not found: ${absolutePath}`);
      return;
    }
    
    const fileUri = vscode.Uri.file(absolutePath);
    const doc = await vscode.workspace.openTextDocument(fileUri);
    await vscode.window.showTextDocument(doc, {
      viewColumn: vscode.ViewColumn.One,
      preview: false,
      preserveFocus: true
    });
    this._log(`[BotPanel] Story file opened: ${filePath}`);
  }

  /**
   * Open test files in a split editor.
   * @param {string[]} testFiles - Array of test file paths
   */
  async _openTestFiles(testFiles) {
    const fs = require('fs');
    const path = require('path');
    
    for (const testFilePath of testFiles) {
      try {
        const pathStr = typeof testFilePath === 'string' ? testFilePath : (testFilePath.url || testFilePath.file || '');
        if (!pathStr) continue;
        const cleanPath = pathStr.split('#')[0];
        const fragment = pathStr.includes('#') ? pathStr.split('#')[1] : null;
        let lineNumber = null;
        if (fragment && fragment.startsWith('L')) {
          lineNumber = parseInt(fragment.substring(1));
        }
        
        const absolutePath = path.isAbsolute(cleanPath) 
          ? cleanPath 
          : path.join(this._workspaceRoot, cleanPath);
        
        if (!fs.existsSync(absolutePath)) {
          this._log(`[BotPanel] Test file not found: ${absolutePath}`);
          continue;
        }
        
        const uri = lineNumber
          ? vscode.Uri.file(absolutePath).with({ fragment: `L${lineNumber}` })
          : vscode.Uri.file(absolutePath);
        await vscode.commands.executeCommand('vscode.open', uri);
      } catch (error) {
        this._log(`[BotPanel] Error opening test file ${testFilePath}: ${error.message}`);
      }
    }
    this._log(`[BotPanel] Opened ${testFiles.length} test files`);
  }

  dispose() {
    BotPanel.currentPanel = undefined;

    // Clean up BotView
      this._botView = null;

    // Clean up shared CLI
    console.log("[BotPanel] Cleaning up shared PanelView CLI");
    if (this._sharedCLI) {
      this._sharedCLI.cleanup();
      this._sharedCLI = null;
    }

    // Clean up resources
    this._panel.dispose();

    while (this._disposables.length) {
      const disposable = this._disposables.pop();
      if (disposable) {
        disposable.dispose();
      }
    }
  }

  /**
   * Update panel using already-cached data from navigation.
   * Skips the refresh() call since botData is already populated.
   * This significantly improves performance for navigation clicks.
   */
  async _updateWithCachedData() {
    const perfUpdateStart = performance.now();
    try {
      this._log('[BotPanel] _updateWithCachedData() START - using cached data, skipping refresh');
      console.log("[BotPanel] _updateWithCachedData() called - skipping refresh");
      const webview = this._panel.webview;
      this._panel.title = "Bot Panel";
      
      // Initialize BotView if needed (uses shared CLI)
      if (!this._botView) {
        const perfBotViewStart = performance.now();
        this._botView = new BotView(this._sharedCLI, this._panelVersion, webview, this._extensionUri);
        const perfBotViewEnd = performance.now();
        this._log(`[PERF] BotView creation: ${(perfBotViewEnd - perfBotViewStart).toFixed(2)}ms`);
      }
      
      // Skip refresh - data already cached from navigation command
      this._log('[BotPanel] Skipping refresh() - using cached botData from navigation');
      
      // Render HTML using cached data
      const perfRenderStart = performance.now();
      const botData = this._botView.botData;
      const currentBehavior = botData?.behaviors?.current_behavior || botData?.current_behavior || null;
      const currentAction = botData?.behaviors?.current_action || botData?.current_action || null;
      const html = this._getWebviewContent(await this._botView.render(), currentBehavior, currentAction, botData);
      const perfRenderEnd = performance.now();
      this._log(`[PERF] HTML rendering: ${(perfRenderEnd - perfRenderStart).toFixed(2)}ms`);
      
      this._lastHtmlLength = html.length;
      this._panel.webview.html = html;
      
      // Clear cached response after rendering
      PanelView._lastResponse = null;
      
      const perfUpdateEnd = performance.now();
      this._log(`[PERF] TOTAL _updateWithCachedData() duration: ${(perfUpdateEnd - perfUpdateStart).toFixed(2)}ms`);
      this._log('[BotPanel] _updateWithCachedData() END');
      
    } catch (err) {
      console.error(`[BotPanel] ERROR in _updateWithCachedData: ${err.message}`);
      this._log(`[BotPanel] ERROR in _updateWithCachedData, falling back to full _update: ${err.message}`);
      // Fall back to full update on error
      return this._update();
    }
  }

  /**
   * Public refresh method - can be called from external code (e.g., sidebar provider)
   */
  async refresh() {
    return this._update();
  }

  _setupDiagramFileWatchers(botData) {
    // Disabled – file watchers were overwriting user edits to .drawio files
    if (this._diagramWatchers) {
      this._diagramWatchers.forEach(function(w) { w.dispose(); });
    }
    this._diagramWatchers = [];
  }


  async _update() {
    // ===== PERFORMANCE: Start overall timing =====
    const perfUpdateStart = performance.now();
    try {
      this._log('[BotPanel] _update() START');
      console.log("[BotPanel] _update() called");
      const webview = this._panel.webview;
      this._panel.title = "Bot Panel";
      
      // Initialize BotView if needed (uses shared CLI)
      if (!this._botView) {
        // ===== PERFORMANCE: BotView creation =====
        const perfBotViewStart = performance.now();
        console.log("[BotPanel] Creating BotView");
        this._log('[BotPanel] Creating BotView');
        try {
          this._botView = new BotView(this._sharedCLI, this._panelVersion, webview, this._extensionUri);
          const perfBotViewEnd = performance.now();
          const botViewDuration = (perfBotViewEnd - perfBotViewStart).toFixed(2);
          console.log("[BotPanel] BotView created successfully");
          this._log(`[BotPanel] BotView created successfully in ${botViewDuration}ms`);
          this._log(`[PERF] BotView creation: ${botViewDuration}ms`);
        } catch (botViewError) {
          console.error(`[BotPanel] ERROR creating BotView: ${botViewError.message}`);
          console.error(`[BotPanel] ERROR stack: ${botViewError.stack}`);
          this._log(`[BotPanel] ERROR creating BotView: ${botViewError.message}`);
          throw botViewError;
        }
      }
      
      // Pass current story map view state to the view
      if (this._botView.storyMapView) {
        this._botView.storyMapView.currentViewMode = this._currentStoryMapView || 'Hierarchy';
      }
      
      // CRITICAL: Refresh data BEFORE rendering to show latest changes
      // ===== PERFORMANCE: Data refresh =====
      const perfRefreshStart = performance.now();
      console.log("[BotPanel] Refreshing bot data...");
      this._log('[BotPanel] Calling _botView.refresh() to fetch latest data');
      await this._botView.refresh();
      const perfRefreshEnd = performance.now();
      const refreshDuration = (perfRefreshEnd - perfRefreshStart).toFixed(2);
      this._log(`[BotPanel] Data refreshed successfully in ${refreshDuration}ms`);
      this._log(`[PERF] Data refresh: ${refreshDuration}ms`);
      
      // ===== PERFORMANCE: HTML rendering =====
      const perfRenderStart = performance.now();
      console.log("[BotPanel] Rendering HTML");
      this._log('[BotPanel] _botView.render() starting');
      // Render HTML using BotView (async now)
      const botData = this._botView.botData || await this._botView.execute('status');
      const currentBehavior = botData?.behaviors?.current_behavior || botData?.current_behavior || null;
      const currentAction = botData?.behaviors?.current_action || botData?.current_action || null;
      const html = this._getWebviewContent(await this._botView.render(), currentBehavior, currentAction, botData);
      const perfRenderEnd = performance.now();
      const renderDuration = (perfRenderEnd - perfRenderStart).toFixed(2);
      this._log(`[PERF] HTML rendering: ${renderDuration}ms`)
      
      // ===== PERFORMANCE: HTML update =====
      const perfHtmlUpdateStart = performance.now();
      
      // Log HTML update details
      const htmlPreview = html.substring(0, 500).replace(/\s+/g, ' ');
      this._log(`[BotPanel] Setting webview HTML (length: ${html.length}, preview: ${htmlPreview}...)`);
      this._log(`[BotPanel] Current HTML length: ${this._lastHtmlLength || 0}, New HTML length: ${html.length}`);
      
      if (this._lastHtmlLength === html.length) {
        this._log('[BotPanel] WARNING: HTML length unchanged - content may not have updated');
      } else {
        this._log('[BotPanel] HTML length changed - update should be visible');
      }
      
      this._lastHtmlLength = html.length;
      this._panel.webview.html = html;
      
      try { this._setupDiagramFileWatchers(botData); } catch (e) { this._log('[BotPanel] watcher setup error: ' + e.message); }
      
      const perfHtmlUpdateEnd = performance.now();
      const htmlUpdateDuration = (perfHtmlUpdateEnd - perfHtmlUpdateStart).toFixed(2);
      this._log('[BotPanel] Webview HTML property set');
      this._log(`[PERF] HTML update (set webview.html): ${htmlUpdateDuration}ms`);
      
      // Give webview time to load
      setTimeout(() => {
        // Show refreshing status (will auto-hide after 1 second)
        this._panel.webview.postMessage({
          command: 'refreshStatus',
          state: 'refreshing',
          message: 'Refreshing...'
        });
        this._log('[BotPanel] Sent refreshStatus refreshing message to webview');
      }, 100);
      
      // ===== PERFORMANCE: Log total duration =====
      const perfUpdateEnd = performance.now();
      const totalDuration = (perfUpdateEnd - perfUpdateStart).toFixed(2);
      console.log("[BotPanel] _update() completed successfully");
      this._log('[BotPanel] _update() completed successfully');
      this._log(`[PERF] TOTAL _update() duration: ${totalDuration}ms`);
      this._log('[BotPanel] _update() END');
      
    } catch (err) {
      console.error(`[BotPanel] ERROR in _update: ${err.message}`);
      console.error(`[BotPanel] ERROR stack: ${err.stack}`);
      this._log(`[BotPanel] ERROR in _update: ${err.message} | Stack: ${err.stack}`);
      
      // Show error in VSCode notification
      const errorMsg = err.isCliError 
        ? `CLI Error: ${err.message}` 
        : `Bot Panel Update Error: ${err.message}`;
      vscode.window.showErrorMessage(errorMsg);
      
      // Display error in panel with retry button
      const errorType = err.errorType || err.constructor.name;
      const command = err.command ? `Command: ${this._escapeHtml(err.command)}` : '';
      
      this._panel.webview.html = this._getWebviewContent(`
        <div style="padding: 20px; color: var(--vscode-errorForeground);">
          <h2>⚠️ Error Loading Bot Panel</h2>
          <div style="background: var(--vscode-inputValidation-errorBackground); border: 1px solid var(--vscode-inputValidation-errorBorder); padding: 15px; margin: 10px 0; border-radius: 4px;">
            <p><strong>Error:</strong> ${this._escapeHtml(err.message)}</p>
            ${command ? `<p style="margin-top: 10px;">${command}</p>` : ''}
            ${err.isCliError ? `<p style="margin-top: 10px;"><strong>Type:</strong> ${this._escapeHtml(errorType)}</p>` : ''}
          </div>
          <details style="margin-top: 15px;">
            <summary style="cursor: pointer; color: var(--vscode-textLink-foreground);">Show Stack Trace</summary>
            <pre style="background: var(--vscode-editor-background); padding: 10px; margin-top: 10px; border-radius: 4px; overflow-x: auto;">${this._escapeHtml(err.stack || 'No stack trace available')}</pre>
          </details>
          <div style="margin-top: 20px;">
            <button onclick="vscode.postMessage({ command: 'refresh' })" 
                    style="background: var(--vscode-button-background); color: var(--vscode-button-foreground); border: none; padding: 8px 16px; cursor: pointer; border-radius: 2px; font-size: 13px;">
              🔄 Retry
            </button>
          </div>
          <p style="margin-top: 20px; color: var(--text-color-faded); font-size: 12px;">
            Please ensure Python is installed and the bot CLI is available.
          </p>
        </div>
      `);
    }
  }


  _escapeHtml(text) {
    if (typeof text !== 'string') {
      text = String(text);
    }
    const map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
  }

  _getWebviewContent(contentHtml, currentBehavior = null, currentAction = null, botData = null) {
    // Get branding colors for CSS theming
    const brandColor = branding.getTitleColor();
    const bgColor = branding.getBackgroundColor();
    const textColor = branding.getTextColor();
    const textColorFaded = branding.getTextColorFaded();
    const fontWeight = branding.getFontWeight();
    // Convert hex to RGB for rgba() usage
    const hexToRgb = (hex) => {
      const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
      return result ? `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}` : '255, 140, 0';
    };
    const brandColorRgb = hexToRgb(brandColor);
    const bgColorRgb = hexToRgb(bgColor);
    const textColorRgb = hexToRgb(textColor);
    const isLightBg = bgColor.toLowerCase() === '#ffffff' || bgColor.toLowerCase() === '#fff';
    
    const currentBehaviorScript = currentBehavior 
      ? '\n        <script>\n            window.currentBehavior = ' + JSON.stringify(currentBehavior) + ';\n            ' + (currentAction ? 'window.currentAction = ' + JSON.stringify(currentAction) + ';' : '') + '\n            ' + (botData ? 'window.botData = ' + JSON.stringify(botData) + ';' : '') + '\n        </script>'
      : (botData ? '\n        <script>\n            window.botData = ' + JSON.stringify(botData) + ';\n        </script>' : '');
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot Panel</title>
    <style>
        /* ============================================================
           THEME SYSTEM - All styling variables in one place
           Branding: ${branding.getBranding()} (${brandColor})
           ============================================================ */
        
        :root {
            /* Colors - from branding config */
            --bg-base: ${bgColor};
            --text-color: ${textColor};
            --text-color-faded: ${textColorFaded};
            --accent-color: ${brandColor};
            --border-color: ${brandColor};
            --divider-color: ${brandColor};
            --hover-bg: ${isLightBg ? 'rgba(0, 0, 0, 0.05)' : 'rgba(255, 255, 255, 0.03)'};
            
            /* Input styling - chat-like appearance */
            --input-bg: ${isLightBg ? 'rgba(0, 0, 0, 0.03)' : 'rgba(255, 255, 255, 0.05)'};
            --input-bg-focus: ${isLightBg ? 'rgba(0, 0, 0, 0.06)' : 'rgba(255, 255, 255, 0.08)'};
            --input-border: ${isLightBg ? 'rgba(0, 0, 0, 0.15)' : 'rgba(255, 255, 255, 0.1)'};
            --input-border-focus: var(--accent-color);
            --input-padding: 6px;
            --input-border-radius: 6px;
            --input-border-width: 1px;
            --input-border-width-focus: 2px;
            --input-header-border-width: 1px;
            --input-header-border-width-focus: 2px;
            --input-transition: border-color 150ms ease, background-color 150ms ease;
            
            /* Borders */
            --border-width: 1px;
            --border-radius: 0;
            --border-radius-sm: 0;
            --active-border-width: 2px;
            
            /* Spacing */
            --space-xs: 2px;
            --space-sm: 4px;
            --space-md: 6px;
            --space-lg: 8px;
            
            /* Typography */
            --font-size-base: 13px;
            --font-size-sm: 12px;
            --font-size-xs: 11px;
            --font-size-section: 14px;
            --font-weight-normal: ${fontWeight};
            --line-height-base: 1.6;
            --line-height-compact: 1.4;
        }
        
        body {
            font-family: var(--vscode-font-family), 'Segoe UI', sans-serif;
            padding: var(--space-md);
            color: var(--text-color);
            background-color: var(--bg-base);
            line-height: var(--line-height-base);
            margin: 0;
            font-size: var(--font-size-base);
            font-weight: var(--font-weight-normal);
        }
        
        /* Prevent images from scaling with panel width */
        img {
            flex-shrink: 0;
            min-width: 0;
        }
        
        .bot-view {
            display: flex;
            flex-direction: column;
            gap: 0;
        }
        
        /* ============================================================
           CARDS & SECTIONS
           ============================================================ */
        
        .card-primary {
            margin-bottom: var(--space-lg);
            padding: var(--space-lg) 0;
            border: none;
            border-top: var(--border-width) solid var(--divider-color);
            background-color: transparent;
        }
        
        .card-secondary {
            margin: var(--space-sm) 0;
            padding: var(--space-md) 0;
            border: none;
            background-color: transparent;
        }
        
        .card-item {
            margin: var(--space-xs) 0;
            padding: var(--space-xs) var(--space-sm);
            border-radius: 0;
            background-color: transparent;
            transition: background-color 80ms ease;
        }
        .card-item:hover {
            background-color: var(--hover-bg);
        }
        
        .card-item.active,
        .card-secondary.active {
            background-color: transparent;
        }
        
        .section {
            margin-bottom: 0;
            padding: var(--space-lg) 0;
            border: none;
            border-top: var(--border-width) solid var(--divider-color);
            background-color: transparent;
        }
        
        .section.card-primary {
            border-top: var(--border-width) solid var(--divider-color);
        }
        
        /* ============================================================
           HIERARCHY & COLLAPSIBLE ITEMS
           ============================================================ */
        
        .behavior-item, .action-item, .operation-item {
            margin: var(--space-xs) 0;
            padding: var(--space-xs) var(--space-sm);
            border-radius: var(--border-radius-sm);
            display: flex;
            align-items: center;
            gap: var(--space-sm);
            transition: background-color 80ms ease;
            font-weight: var(--font-weight-normal);
        }
        
        .behavior-item:hover, .action-item:hover {
            background-color: var(--hover-bg);
        }
        
        .collapsible-header {
            margin: var(--space-xs) 0;
            padding: var(--space-sm);
            border-radius: var(--border-radius-sm);
            display: flex;
            align-items: center;
            gap: var(--space-sm);
            cursor: pointer;
            font-weight: var(--font-weight-normal);
            font-size: var(--font-size-base);
            transition: background-color 80ms ease;
        }
        .collapsible-header:hover {
            background-color: var(--hover-bg);
        }
        .collapsible-header.action-item {
            margin-left: 12px;
            font-weight: var(--font-weight-normal);
        }
        .operation-item {
            margin-left: 24px;
            font-size: var(--font-size-sm);
            color: var(--text-color-faded);
        }
        .collapsible-content {
            padding-left: 0;
        }
        #behaviors-content .collapsible-content {
            padding-left: 12px;
        }
        #behaviors-content .collapsible-content .collapsible-content {
            padding-left: 12px;
        }
        
        .behavior-item.active,
        .action-item.active,
        .operation-item.active {
            background-color: transparent;
        }
        
        /* ============================================================
           STORY TREE NODE INTERACTION
           ============================================================ */
        
        .story-node {
            padding: 2px 4px;
            border-radius: 3px;
            transition: background-color 150ms ease;
        }
        
        .story-node:hover {
            background-color: rgba(${brandColorRgb}, 0.15); /* Faded brand color on hover */
        }
        
        .story-node.selected {
            background-color: rgba(${brandColorRgb}, 0.35); /* Distinct brand color when selected */
        }
        
        
        .collapsible-section {
            margin-bottom: var(--space-sm);
        }
        
        .collapsible-section .expand-icon {
            transition: transform 150ms ease;
            display: inline-block;
            transform: rotate(0deg);
            font-style: normal;
            min-width: var(--space-md);
            color: ${brandColor} !important;
            font-size: 28px;
            margin-right: 8px;
        }
        .collapsible-section.expanded .expand-icon {
            transform: rotate(90deg);
        }
        /* Ensure nested subsections have smaller icons */
        .collapsible-content .collapsible-section .expand-icon {
            font-size: 20px;
        }
        .collapsible-content {
            overflow: hidden;
            transition: max-height 0.3s ease;
        }
        
        .collapsible-content[style*="display: none"] {
            display: none !important;
        }
        
        .status-marker {
            font-family: inherit;
            font-weight: var(--font-weight-normal);
            min-width: 20px;
            font-size: var(--font-size-base);
            display: inline-block;
            margin-right: 4px;
        }
        
        .marker-current {
            color: var(--vscode-textLink-foreground);
        }
        
        .marker-completed {
            color: var(--vscode-textLink-foreground);
        }
        
        .marker-pending {
            color: var(--text-color-faded);
        }
        
        .scope-section {
            background-color: transparent;
            padding: 0;
            border: none;
        }
        
        /* ============================================================
           INPUTS & INTERACTIVE ELEMENTS
           ============================================================ */
        
        .input-container {
            border: var(--input-border-width) solid var(--accent-color);
            border-radius: var(--input-border-radius);
            overflow: hidden;
            transition: border-width 150ms ease, border-color 150ms ease, background-color 150ms ease;
        }
        .input-container:focus-within {
            border-width: var(--input-border-width-focus);
        }
        
        .input-header {
            padding: 4px var(--input-padding);
            background-color: transparent;
            border-bottom: var(--input-header-border-width) solid var(--accent-color);
            font-size: var(--font-size-base);
            color: var(--text-color);
            font-weight: 600;
            transition: border-bottom-width 150ms ease;
        }
        .input-container:focus-within .input-header {
            border-bottom-width: var(--input-header-border-width-focus);
        }
        
        .info-display {
            padding: var(--space-sm) 0;
            font-size: var(--font-size-base);
            color: var(--text-color);
        }
        .info-display .label {
            color: var(--text-color-faded);
            margin-right: 8px;
        }
        .info-display .value {
            color: var(--text-color);
        }
        
        .main-header {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 7px 5px 6px 5px;
            border-bottom: 1px solid var(--divider-color);
        }
        .main-header-icon {
            width: 28px;
            height: 28px;
            object-fit: contain;
        }
        .main-header-title {
            font-size: 20px;
            font-weight: 700;
            color: var(--text-color);
        }
        .main-header-collapse {
            background-color: transparent;
            border: none;
            color: var(--text-color);
            font-size: 18px;
            padding: 3px;
            cursor: pointer;
            border-radius: 4px;
            transition: background-color 150ms ease;
            margin-right: 4px;
        }
        .main-header-collapse:hover {
            background-color: rgba(255, 140, 0, 0.1);
        }
        .main-header-refresh {
            background-color: transparent;
            border: none;
            color: var(--text-color);
            font-size: 18px;
            padding: 3px;
            cursor: pointer;
            border-radius: 4px;
            transition: background-color 150ms ease;
        }
        .main-header-refresh:hover {
            background-color: rgba(255, 140, 0, 0.1);
        }
        
        .main-header-status {
            display: flex;
            align-items: center;
            gap: 6px;
            visibility: visible;
            opacity: 1;
        }
        
        .main-header-status[style*="display: none"] {
            display: none !important;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .save-spinner {
            animation: spin 1s linear infinite;
        }
        
        /* Save status indicator styles - matches input container design */
        .save-status {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            border: var(--input-border-width) solid var(--accent-color);
            border-radius: var(--input-border-radius);
            background-color: rgba(255, 140, 0, 0.1); /* Dark black with orange tint */
            color: var(--text-color);
            font-size: var(--font-size-sm);
            transition: opacity 0.3s, background-color 150ms ease;
            white-space: nowrap;
        }
        
        .save-status.saving,
        .save-status.refreshing {
            background-color: rgba(255, 140, 0, 0.15); /* Slightly brighter when active */
            border-color: var(--accent-color);
        }
        
        .save-status.success {
            background-color: rgba(255, 140, 0, 0.1);
            border-color: var(--accent-color);
            color: #ff8c00;
        }
        
        .save-status.success #save-status-message {
            color: #ff8c00;
        }
        
        .save-status.error {
            background-color: rgba(255, 140, 0, 0.15);
            border-color: var(--accent-color);
            cursor: pointer;
        }
        
        .save-status.error:hover {
            background-color: rgba(255, 140, 0, 0.2);
        }
        
        .save-icon {
            width: 16px;
            height: 16px;
            display: inline-block;
            font-size: 16px;
            line-height: 1;
        }
        
        .save-icon.spinner {
            animation: spin 1s linear infinite;
        }
        
        input[type="text"],
        textarea,
        .text-input {
            width: 100%;
            padding: var(--space-sm) var(--input-padding);
            background-color: var(--input-bg);
            color: var(--text-color);
            border: none;
            border-radius: 0;
            font-family: var(--vscode-editor-font-family, 'Segoe UI', sans-serif);
            font-size: var(--font-size-base);
        }
        input[type="text"]:focus,
        textarea:focus,
        .text-input:focus {
            outline: none;
        }
        input[type="text"].drag-over {
            background-color: var(--vscode-editor-selectionBackground, rgba(255, 140, 0, 0.2));
            border: 1px dashed var(--vscode-focusBorder, #ff8c00);
            box-shadow: 0 0 4px rgba(255, 140, 0, 0.4);
        }
        
        button {
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            padding: var(--space-xs) var(--space-md);
            cursor: pointer;
            border-radius: var(--border-radius-sm);
            font-size: var(--font-size-base);
            font-family: inherit;
            transition: all 100ms ease;
        }
        button:hover {
            background-color: var(--vscode-button-hoverBackground);
        }
        button:active {
            background-color: var(--vscode-button-background);
            opacity: 0.8;
            transform: scale(0.98);
        }
        
        /* Ensure button images maintain fixed size */
        button img {
            flex-shrink: 0;
            display: block;
        }
        
        a {
            color: var(--vscode-textLink-foreground);
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        .bot-links {
            display: flex;
            gap: var(--space-md);
            flex-wrap: wrap;
            align-items: center;
        }
        .bot-link {
            font-size: var(--font-size-base);
            cursor: pointer;
            text-decoration: underline;
            color: var(--text-color-faded);
            opacity: 0.6;
        }
        .bot-link.active {
            color: var(--text-color);
            font-weight: var(--font-weight-normal);
            text-decoration: none;
            cursor: default;
            opacity: 1;
        }
        .bot-link:not(.active):hover {
            opacity: 0.8;
        }
        
        .empty-state {
            color: var(--text-color-faded);
            font-style: italic;
            padding: var(--space-sm);
        }
    </style>${currentBehaviorScript}
</head>
<body>
    ${contentHtml}
    
    <script>
        const vscode = acquireVsCodeApi();
        console.log('[WebView] ========== SCRIPT LOADING ==========');
        console.log('[WebView] vscode API acquired:', !!vscode);
        console.log('[WebView] vscode.postMessage available:', typeof vscode.postMessage);
        
        
        // Restore collapse state and selected node when DOM is ready
        document.addEventListener('DOMContentLoaded', function() {
            try {
                // Restore collapse state
                const savedState = sessionStorage.getItem('collapseState');
                if (savedState) {
                    const state = JSON.parse(savedState);
                    // Use setTimeout to ensure DOM is fully rendered
                    setTimeout(() => window.restoreCollapseState(state), 50);
                    console.log('[WebView] Restored collapse state for', Object.keys(state).length, 'nodes');
                }
                
                // Restore selected node
                const savedSelection = sessionStorage.getItem('selectedNode');
                if (savedSelection) {
                    const selection = JSON.parse(savedSelection);
                    setTimeout(() => {
                        if (window.selectNode) {
                            window.selectNode(selection.type, selection.name, selection);
                            console.log('[WebView] Restored selection for', selection.name);
                        }
                    }, 100);
                }
                
                // Restore scroll position and expand clarify boxes after content is rendered
                setTimeout(() => {
                    if (window.restoreScrollPosition) {
                        window.restoreScrollPosition();
                    }
                    if (window.expandClarifyBoxes) {
                        window.expandClarifyBoxes();
                    }
                }, 150);
            } catch (err) {
                console.error('[WebView] Error restoring state:', err);
            }
        });
        
        // Save scroll position when page loses visibility (e.g., when opening a file)
        document.addEventListener('visibilitychange', function() {
            if (document.visibilityState === 'hidden') {
                if (window.saveScrollPosition) {
                    window.saveScrollPosition();
                }
            } else if (document.visibilityState === 'visible') {
                // Restore scroll position when becoming visible again
                setTimeout(() => {
                    if (window.restoreScrollPosition) {
                        window.restoreScrollPosition();
                    }
                }, 50);
            }
        });
        
        // Global click handler using event delegation (CSP blocks inline onclick)
        document.addEventListener('click', function(e) {
            const target = e.target;
            const targetInfo = {
                tagName: target.tagName,
                className: target.className,
                id: target.id,
                nodeType: target.getAttribute && target.getAttribute('data-node-type'),
                nodeName: target.getAttribute && target.getAttribute('data-node-name')
            };
            console.log('[WebView] CLICK DETECTED:', targetInfo);
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] CLICK: ' + JSON.stringify(targetInfo)
            });
            
            // Handle story node clicks (epic, sub-epic, story)
            if (target.classList.contains('story-node')) {
                console.log('═══════════════════════════════════════════════════════');
                console.log('[WebView] STORY NODE CLICKED');
                const nodeType = target.getAttribute('data-node-type');
                const nodeName = target.getAttribute('data-node-name');
                const hasChildren = target.getAttribute('data-has-children') === 'true';
                const hasStories = target.getAttribute('data-has-stories') === 'true';
                const hasNestedSubEpics = target.getAttribute('data-has-nested-sub-epics') === 'true';
                const nodePath = target.getAttribute('data-path');
                const fileLink = target.getAttribute('data-file-link');
                const behavior = target.getAttribute('data-behavior-needed') || null;
                const behaviorsAttr = target.getAttribute('data-behaviors-needed');
                const behaviors = behaviorsAttr ? JSON.parse(behaviorsAttr) : (behavior ? [behavior] : []);
                
                console.log('[WebView]   nodeType:', nodeType);
                console.log('[WebView]   nodeName:', nodeName);
                console.log('[WebView]   hasChildren:', hasChildren);
                console.log('[WebView]   hasStories:', hasStories);
                console.log('[WebView]   hasNestedSubEpics:', hasNestedSubEpics);
                console.log('[WebView]   nodePath:', nodePath);
                console.log('[WebView]   fileLink:', fileLink);
                console.log('[WebView]   behavior (from DOM):', behavior);
                console.log('[WebView]   behaviors (from DOM):', behaviors);
                
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] Extracted behavior_needed from DOM: "' + behavior + '" for node: ' + nodeName
                });
                
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] Story node clicked: type=' + nodeType + ', name=' + nodeName + ', path=' + nodePath
                });
                
                // Call selectNode
                if (window.selectNode && nodeType && nodeName !== null) {
                    const options = {
                        hasChildren: hasChildren,
                        hasStories: hasStories,
                        hasNestedSubEpics: hasNestedSubEpics,
                        path: nodePath,
                        behavior: behavior,
                        behaviors: behaviors
                    };
                    console.log('[WebView]   Calling selectNode with options:', JSON.stringify(options, null, 2));
                    window.selectNode(nodeType, nodeName, options);
                }
                
                // Call openFile if there's a file link
                if (window.openFile && fileLink) {
                    console.log('[WebView]   Opening file:', fileLink);
                    window.openFile(fileLink);
                }
                
                e.stopPropagation();
                console.log('═══════════════════════════════════════════════════════');
            }
            
            // Handle behavior and action clicks (CSP-safe event delegation)
            // Traverse up the DOM tree to find element with data-action attribute
            let actionElement = target;
            let action = actionElement.getAttribute('data-action');
            let searchDepth = 0;
            while (!action && actionElement && actionElement.parentElement && searchDepth < 5) {
                actionElement = actionElement.parentElement;
                action = actionElement.getAttribute('data-action');
                searchDepth++;
            }
            
            if (action) {
                console.log('[WebView] Behavior/Action click detected, action:', action);
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] Behavior/Action click: action=' + action + ', element=' + actionElement.tagName + ', className=' + actionElement.className
                });
                
                if (action === 'navigateToBehavior') {
                    const behaviorName = actionElement.getAttribute('data-behavior-name');
                    if (behaviorName && window.navigateToBehavior) {
                        window.navigateToBehavior(behaviorName);
                        e.stopPropagation();
                        e.preventDefault();
                    }
                } else if (action === 'navigateToAction') {
                    const behaviorName = actionElement.getAttribute('data-behavior-name');
                    const actionName = actionElement.getAttribute('data-action-name');
                    if (behaviorName && actionName && window.navigateToAction) {
                        window.navigateToAction(behaviorName, actionName);
                        e.stopPropagation();
                        e.preventDefault();
                    }
                } else if (action === 'toggleCollapse') {
                    const targetId = actionElement.getAttribute('data-target');
                    if (targetId && window.toggleCollapse) {
                        console.log('[WebView] Calling toggleCollapse with:', targetId);
                        window.toggleCollapse(targetId);
                        e.stopPropagation();
                        e.preventDefault();
                    }
                } else if (action === 'getBehaviorRules') {
                    const behaviorName = actionElement.getAttribute('data-behavior-name');
                    if (behaviorName && window.getBehaviorRules) {
                        console.log('[WebView] Calling getBehaviorRules with:', behaviorName);
                        window.getBehaviorRules(behaviorName);
                        e.stopPropagation();
                        e.preventDefault();
                    }
                } else if (action === 'executeNavigationCommand') {
                    const command = actionElement.getAttribute('data-command');
                    if (command && window.executeNavigationCommand) {
                        console.log('[WebView] Calling executeNavigationCommand with:', command);
                        window.executeNavigationCommand(command);
                        e.stopPropagation();
                        e.preventDefault();
                    }
                } else if (action === 'toggleSection') {
                    const sectionId = actionElement.getAttribute('data-section-id');
                    if (sectionId && window.toggleSection) {
                        console.log('[WebView] Calling toggleSection with:', sectionId);
                        window.toggleSection(sectionId);
                        e.stopPropagation();
                        e.preventDefault();
                    }
                }
            }
        }, true); // Use capture phase to catch all clicks
        
        // Handle double-click on story nodes to enable edit mode
        document.addEventListener('dblclick', function(e) {
            const target = e.target;
            
            // Handle story node double-clicks (epic, sub-epic, story)
            if (target.classList.contains('story-node')) {
                const nodePath = target.getAttribute('data-path');
                const nodeName = target.getAttribute('data-node-name');
                
                console.log('[WebView] DOUBLE-CLICK on story node:', nodeName, 'path:', nodePath);
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] Double-click on node: ' + nodeName + ', path: ' + nodePath
                });
                
                if (nodePath && window.enableEditMode) {
                    window.enableEditMode(nodePath);
                }
                
                e.stopPropagation();
                e.preventDefault();
            }
        }, true); // Use capture phase to catch all double-clicks
        
        // Right-click context menu on story nodes: Copy node name / Copy full JSON (event -> CLI -> bot)
        document.addEventListener('contextmenu', function(e) {
            let target = e.target;
            while (target && !target.classList.contains('story-node')) {
                target = target.parentElement;
            }
            if (!target || !target.classList.contains('story-node')) return;
            const nodePath = target.getAttribute('data-path');
            if (!nodePath) return;
            e.preventDefault();
            e.stopPropagation();
            // Remove any existing copy menu
            const existing = document.getElementById('story-node-copy-menu');
            if (existing) existing.remove();
            const menu = document.createElement('div');
            menu.id = 'story-node-copy-menu';
            menu.style.cssText = 'position:fixed;left:' + e.clientX + 'px;top:' + e.clientY + 'px;background:var(--vscode-dropdown-background);border:1px solid var(--vscode-dropdown-border);border-radius:4px;padding:4px 0;z-index:10001;min-width:160px;box-shadow:0 2px 8px rgba(0,0,0,0.2);';
            const items = [
                { label: 'Copy node name', action: 'name' },
                { label: 'Copy full JSON', action: 'json' }
            ];
            items.forEach(function(item) {
                const div = document.createElement('div');
                div.textContent = item.label;
                div.style.cssText = 'padding:6px 12px;cursor:pointer;font-size:12px;';
                div.onmouseover = function() { div.style.backgroundColor = 'var(--vscode-list-hoverBackground)'; };
                div.onmouseout = function() { div.style.backgroundColor = ''; };
                div.onclick = function(ev) {
                    ev.preventDefault();
                    ev.stopPropagation();
                    menu.remove();
                    document.removeEventListener('click', closeMenu);
                    vscode.postMessage({ command: 'copyNodeToClipboard', nodePath: nodePath, action: item.action });
                };
                menu.appendChild(div);
            });
            function closeMenu() {
                if (menu.parentNode) menu.remove();
                document.removeEventListener('click', closeMenu);
            }
            document.body.appendChild(menu);
            setTimeout(function() { document.addEventListener('click', closeMenu); }, 0);
        }, true);
        
        // Handle drag and drop for moving nodes
        let draggedNode = null;
        let dropIndicator = null;
        let currentDropZone = null; // 'before', 'after', or 'inside'
        
        // Create drop indicator line
        function createDropIndicator() {
            if (!dropIndicator) {
                dropIndicator = document.createElement('div');
                dropIndicator.style.position = 'fixed';
                dropIndicator.style.height = '2px';
                dropIndicator.style.backgroundColor = 'rgb(255, 140, 0)'; // Orange to match UI
                dropIndicator.style.pointerEvents = 'none';
                dropIndicator.style.zIndex = '10000';
                dropIndicator.style.transition = 'all 0.1s ease';
                dropIndicator.style.display = 'none'; // Start hidden
                document.body.appendChild(dropIndicator);
            }
            return dropIndicator;
        }
        
        function removeDropIndicator() {
            if (dropIndicator && dropIndicator.parentNode) {
                dropIndicator.parentNode.removeChild(dropIndicator);
                dropIndicator = null;
            }
            currentDropZone = null;
        }
        
        document.addEventListener('dragstart', function(e) {
            console.log('[WebView] DRAGSTART EVENT FIRED');
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] DRAGSTART EVENT - target classList: ' + (e.target.classList ? Array.from(e.target.classList).join(', ') : 'none')
            });
            
            // Find the story-node element (might be dragging a child element)
            let target = e.target;
            while (target && !target.classList.contains('story-node')) {
                target = target.parentElement;
            }
            
            if (target && target.classList.contains('story-node')) {
                draggedNode = {
                    path: target.getAttribute('data-path'),
                    name: target.getAttribute('data-node-name'),
                    type: target.getAttribute('data-node-type'),
                    position: parseInt(target.getAttribute('data-position') || '0')
                };
                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('text/plain', draggedNode.path);
                target.style.opacity = '0.5';
                console.log('[WebView] Drag started:', draggedNode);
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] DRAG STARTED: ' + JSON.stringify(draggedNode)
                });
            } else {
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] DRAGSTART ignored - not a story-node'
                });
            }
        }, true);
        
        document.addEventListener('dragend', function(e) {
            console.log('[WebView] DRAGEND EVENT FIRED');
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] DRAGEND EVENT'
            });
            
            // Find the story-node element
            let target = e.target;
            while (target && !target.classList.contains('story-node')) {
                target = target.parentElement;
            }
            
            if (target && target.classList.contains('story-node')) {
                target.style.opacity = '1';
                draggedNode = null;
                removeDropIndicator();
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] Drag ended, cleared draggedNode'
                });
            }
        }, true);
        
        let dragoverLogCounter = 0; // Throttle dragover logs
        document.addEventListener('dragover', function(e) {
            // Find the story-node element
            let target = e.target;
            let searchDepth = 0;
            while (target && !target.classList.contains('story-node') && searchDepth < 10) {
                target = target.parentElement;
                searchDepth++;
            }
            
            // Log every 20th dragover event to avoid spam
            if (dragoverLogCounter++ % 20 === 0 && draggedNode) {
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] DRAGOVER - found target: ' + (target ? 'YES' : 'NO') + ', draggedNode: ' + (draggedNode ? draggedNode.name : 'null')
                });
            }
            
            if (target && target.classList.contains('story-node') && draggedNode) {
                const targetType = target.getAttribute('data-node-type');
                const targetPath = target.getAttribute('data-path');
                const targetName = target.getAttribute('data-node-name');
                
                // Don't allow dropping on self
                if (draggedNode.path === targetPath) {
                    removeDropIndicator();
                    return;
                }
                
                // Check if target can contain dragged node
                const canContain = (targetType === 'epic' && draggedNode.type === 'sub-epic') ||
                                  (targetType === 'sub-epic' && (draggedNode.type === 'sub-epic' || draggedNode.type === 'story')) ||
                                  (targetType === 'story' && draggedNode.type === 'scenario');
                
                // Check if nodes are same type for reordering
                const sameType = draggedNode.type === targetType;
                
                if (canContain || sameType) {
                    e.preventDefault();
                    e.dataTransfer.dropEffect = 'move';
                    
                    // Get mouse position relative to target element
                    const rect = target.getBoundingClientRect();
                    const mouseY = e.clientY;
                    const targetTop = rect.top;
                    const targetHeight = rect.height;
                    const relativeY = mouseY - targetTop;
                    const percentY = relativeY / targetHeight;
                    
                    // Determine drop zone based on mouse position
                    let dropZone;
                    const indicator = createDropIndicator();
                    
                    // Check if target can contain the dragged node
                    const hasStories = target.getAttribute('data-has-stories') === 'true';
                    const hasNestedSubEpics = target.getAttribute('data-has-nested-sub-epics') === 'true';
                    const isEmptyContainer = !hasStories && !hasNestedSubEpics;
                    
                    // "ON" vs "AFTER" logic:
                    // - If hovering directly on item (middle 60%) AND can nest inside: show "inside" (orange background, no line)
                    // - Otherwise: show "after" (orange line below item)
                    if (canContain && percentY >= 0.2 && percentY <= 0.8) {
                        // Hovering ON the item - nest inside
                        dropZone = 'inside';
                        target.style.backgroundColor = 'rgba(255, 140, 0, 0.3)'; // Orange tint for nesting
                        indicator.style.display = 'none';
                        if (dragoverLogCounter % 20 === 0) {
                            vscode.postMessage({
                                command: 'logToFile',
                                message: '[WebView] DRAGOVER ON (inside) - will nest inside ' + target.getAttribute('data-node-name')
                            });
                        }
                    } else if (sameType) {
                        // Same type: insert after
                        dropZone = 'after';
                        target.style.backgroundColor = '';
                        indicator.style.display = 'block';
                        indicator.style.left = rect.left + 'px';
                        indicator.style.top = (rect.top + rect.height) + 'px';
                        indicator.style.width = rect.width + 'px';
                        // Log indicator positioning
                        if (dragoverLogCounter % 20 === 0) {
                            vscode.postMessage({
                                command: 'logToFile',
                                message: '[WebView] DRAGOVER AFTER - hovering over: "' + targetName + '", line at y=' + (rect.top + rect.height) + ' (BOTTOM of node), will insert AFTER this node'
                            });
                        }
                    } else {
                        vscode.postMessage({
                            command: 'logToFile',
                            message: '[WebView] DRAGOVER INVALID - canContain: ' + canContain + ', sameType: ' + sameType + ', dragging ' + draggedNode.type + ' onto ' + targetType
                        });
                        removeDropIndicator();
                        return;
                    }
                    
                    currentDropZone = dropZone;
                } else {
                    removeDropIndicator();
                }
            } else {
                removeDropIndicator();
            }
        }, true);
        
        document.addEventListener('dragleave', function(e) {
            // Find the story-node element
            let target = e.target;
            while (target && !target.classList.contains('story-node')) {
                target = target.parentElement;
            }
            
            if (target && target.classList.contains('story-node')) {
                target.style.backgroundColor = '';
            }
        }, true);
        
        document.addEventListener('drop', function(e) {
            console.log('[WebView] ===== DROP EVENT FIRED =====');
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] ===== DROP EVENT FIRED ===== draggedNode: ' + (draggedNode ? draggedNode.name : 'null') + ', currentDropZone: ' + (currentDropZone || 'null')
            });
            
            // Find the story-node element (might be dropping on a child element)
            let target = e.target;
            while (target && !target.classList.contains('story-node')) {
                target = target.parentElement;
            }
            
            if (target && target.classList.contains('story-node') && draggedNode && currentDropZone) {
                e.preventDefault();
                e.stopPropagation();
                target.style.backgroundColor = '';
                
                // Save dropZone BEFORE removeDropIndicator clears it
                const dropZone = currentDropZone;
                removeDropIndicator();
                
                const targetPath = target.getAttribute('data-path');
                const targetName = target.getAttribute('data-node-name');
                const targetType = target.getAttribute('data-node-type');
                
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] DROP on story-node - dragged: ' + draggedNode.name + ' onto: ' + targetName + ', dropZone: ' + dropZone
                });
                
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] DROP INFO - draggedNode.path: ' + draggedNode.path + ', targetPath: ' + targetPath
                });
                
                if (draggedNode.path !== targetPath) {
                    console.log('[WebView] Drop detected: dragged=' + draggedNode.name + ' targetPath=' + targetPath + ' targetName=' + targetName + ' targetType=' + targetType + ' dropZone=' + dropZone);
                    
                    vscode.postMessage({
                        command: 'logToFile',
                        message: '[WebView] DROP DETECTED - Dragged: ' + draggedNode.name + ' (type: ' + draggedNode.type + ', pos: ' + draggedNode.position + ') onto Target: ' + targetName + ' (type: ' + targetType + '), dropZone: ' + dropZone
                    });
                    
                    // Optimistic update disabled - full refresh preserves structure correctly
                    console.log('[WebView] Move operation - waiting for backend and full refresh');
                    
                    let command;
                    
                    vscode.postMessage({
                        command: 'logToFile',
                        message: '[WebView] COMMAND CONSTRUCTION - dropZone: ' + dropZone
                    });
                    
                    if (dropZone === 'inside') {
                        // ON: Nest inside the target container - use FULL PATH not just name to avoid ambiguity
                        // targetPath is like: story_graph."Epic1"."Child1"
                        // Backend expects: target:"Epic1"."Child1" (path with internal quotes, no outer wrapping)
                        var targetForCommand = targetPath.replace(/^story_graph\./, '');
                        // targetForCommand already has quotes around each segment (e.g., "Epic1"."Child1")
                        // Do NOT wrap in additional quotes
                        command = draggedNode.path + '.move_to target:' + targetForCommand;
                        vscode.postMessage({
                            command: 'logToFile',
                            message: '[WebView] INSIDE COMMAND - targetPath: ' + targetPath + ', targetForCommand: ' + targetForCommand + ', command: ' + command
                        });
                    } else if (dropZone === 'after') {
                        var targetPos = parseInt(target.getAttribute('data-position') || '0');
                        var draggedPos = draggedNode.position;
                        
                        // Extract parent path (everything except the last segment)
                        // targetPath is like: story_graph."Epic1"."Child1"."Story1"
                        // parentPath should be: story_graph."Epic1"."Child1"
                        var parentMatch = targetPath.match(/(.*)\."[^"]+"/);
                        var parentPath = parentMatch ? parentMatch[1] : 'story_graph';
                        
                        // Strip off "story_graph." prefix to get the target parameter value
                        var targetForCommand = parentPath.replace(/^story_graph\./, '');
                        
                        vscode.postMessage({
                            command: 'logToFile',
                            message: '[WebView] AFTER CALCULATION - targetPos: ' + targetPos + ', draggedPos: ' + draggedPos + ', parentPath: ' + parentPath + ', targetForCommand: ' + targetForCommand
                        });
                        
                        // When moving DOWN (to later position), use targetPos as-is (item shifts down)
                        // When moving UP (to earlier position), use targetPos + 1 (drop after target)
                        var finalPos = (draggedPos < targetPos) ? targetPos : (targetPos + 1);
                        
                        command = draggedNode.path + '.move_to target:' + targetForCommand + ' at_position:' + finalPos;
                        vscode.postMessage({
                            command: 'logToFile',
                            message: '[WebView] AFTER COMMAND - dragged from ' + draggedPos + ' to position: ' + finalPos + ' (target was at ' + targetPos + '), command: ' + command
                        });
                    }
                    
                    // ========== ASYNC SAVE FLOW: MOVE OPERATION ==========
                    // Use StoryMapView handler for optimistic updates
                    if (dropZone === 'after' && typeof window.handleMoveNode === 'function') {
                        // Calculate parent path and position
                        var parentMatch = targetPath.match(/(.*)\."[^"]+"/);
                        var parentPath = parentMatch ? parentMatch[1] : 'story_graph';
                        var finalPos = (draggedNode.position < targetPos) ? targetPos : (targetPos + 1);
                        
                        // Call StoryMapView handler - pass targetPath so we can insert after the specific node
                        window.handleMoveNode({
                            sourceNodePath: draggedNode.path,
                            targetParentPath: parentPath,
                            targetNodePath: targetPath,  // Pass target node path for "after" positioning
                            position: finalPos,
                            dropZone: 'after'
                        });
                    } else if (dropZone === 'inside' && typeof window.handleMoveNode === 'function') {
                        // Moving inside target
                        window.handleMoveNode({
                            sourceNodePath: draggedNode.path,
                            targetParentPath: targetPath,
                            position: 0,
                            dropZone: 'inside'
                        });
                    } else {
                        // Fallback: send command directly (defaults to optimistic for story-changing ops)
                        console.warn('[WebView] handleMoveNode not available, sending command directly');
                        vscode.postMessage({
                            command: 'executeCommand',
                            commandText: command
                            // optimistic defaults to true for story-changing operations
                        });
                    }
                } else {
                    vscode.postMessage({
                        command: 'logToFile',
                        message: '[WebView] DROP ignored - same node'
                    });
                }
            } else {
                removeDropIndicator();
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] DROP ignored - not story-node, no draggedNode, or no dropZone'
                });
            }
        }, true);
        
        // Test if onclick handlers can access functions
        window.testFunction = function() {
            console.log('[WebView] TEST FUNCTION CALLED - functions are accessible!');
            alert('Test function works!');
        };
        console.log('[WebView] window.testFunction defined:', typeof window.testFunction);
        
        // Hide panel - sends message to extension to collapse the panel
        window.hidePanel = function() {\n            console.log('[hidePanel] Requesting panel collapse');\n            vscode.postMessage({ command: 'hidePanel' });\n        };\n        \n        window.toggleSection = function(sectionId) {
            console.log('[toggleSection] Called with sectionId:', sectionId);
            const content = document.getElementById(sectionId);
            console.log('[toggleSection] Content element:', content);
            if (content) {
                const section = content.closest('.collapsible-section');
                console.log('[toggleSection] Parent section:', section);
                const isExpanded = section && section.classList.contains('expanded');
                console.log('[toggleSection] isExpanded:', isExpanded);
                
                // Toggle visibility
                if (isExpanded) {
                    // Collapsing
                    content.style.maxHeight = '0px';
                    content.style.overflow = 'hidden';
                    content.style.display = 'none';
                } else {
                    // Expanding
                    content.style.maxHeight = '2000px';
                    content.style.overflow = 'visible';
                    content.style.display = 'block';
                    // Expand clarify boxes once visible (they need layout to compute scrollHeight)
                    if (content.querySelector('[id^="clarify-answer-"]')) {
                        setTimeout(() => { if (window.expandClarifyBoxes) window.expandClarifyBoxes(); }, 50);
                    }
                }
                
                // Toggle expanded class (CSS handles icon rotation - ▸ rotates 90deg when expanded)
                const header = content.previousElementSibling;
                console.log('[toggleSection] Header element:', header);
                if (header && section) {
                    section.classList.toggle('expanded', !isExpanded);
                    console.log('[toggleSection] After toggle, section classes:', section.className);
                    // Keep icon as ▸ always - CSS rotation handles the visual state
                    const icon = header.querySelector('.expand-icon');
                    console.log('[toggleSection] Icon element:', icon);
                    if (icon) {
                        icon.textContent = '▸';
                        console.log('[toggleSection] Icon transform:', window.getComputedStyle(icon).transform);
                    }
                }
            }
        };
        
        // Expand the instructions section for a specific action (clarify, strategy, build, validate)
        // This should ALWAYS expand, never toggle - collapsing is only done by explicit user clicks
        window.expandInstructionsSection = function(actionName) {
            console.log('[expandInstructionsSection] Called with actionName:', actionName);
            if (!actionName) return;
            
            // Map action names to section header text
            const actionToSectionName = {
                'clarify': 'Clarify',
                'strategy': 'Strategy',
                'build': 'Build',
                'validate': 'Validate',
                'render': 'Render'
            };
            
            const sectionName = actionToSectionName[actionName];
            if (!sectionName) {
                console.log('[expandInstructionsSection] No section mapped for action:', actionName);
                return;
            }
            
            // First, collapse all instruction sections (instr-section-*)
            document.querySelectorAll('[id^="instr-section-"]').forEach(content => {
                const section = content.closest('.collapsible-section');
                if (section) {
                    content.style.maxHeight = '0px';
                    content.style.overflow = 'hidden';
                    content.style.display = 'none';
                    section.classList.remove('expanded');
                }
            });
            
            // Find the section by looking for header text containing the section name
            const headers = document.querySelectorAll('.collapsible-header');
            for (const header of headers) {
                const headerText = header.textContent || '';
                // Match section name but avoid matching subsections (e.g., "Clarify" but not "Base Instructions")
                if (headerText.includes(sectionName) && !headerText.includes('Base')) {
                    const section = header.closest('.collapsible-section');
                    const content = header.nextElementSibling;
                    
                    if (section && content && content.classList.contains('collapsible-content')) {
                        console.log('[expandInstructionsSection] Expanding section:', sectionName);
                        // Always expand - we already collapsed all sections above
                        content.style.maxHeight = '2000px';
                        content.style.overflow = 'visible';
                        content.style.display = 'block';
                        section.classList.add('expanded');
                        
                        // Expand clarify boxes once visible (need layout for scrollHeight)
                        if (sectionName === 'Clarify' && content.querySelector('[id^="clarify-answer-"]')) {
                            setTimeout(() => { if (window.expandClarifyBoxes) window.expandClarifyBoxes(); }, 50);
                        }
                        
                        // Update icon
                        const icon = header.querySelector('.expand-icon');
                        if (icon) {
                            icon.textContent = '▸';
                        }
                        return; // Found and processed, exit
                    }
                }
            }
            console.log('[expandInstructionsSection] Section not found for:', sectionName);
        };
        
        // Save/restore collapse state across panel refreshes
        window.getCollapseState = function() {
            const state = {};
            document.querySelectorAll('.collapsible-content').forEach(content => {
                if (content.id) {
                    state[content.id] = content.style.display !== 'none';
                }
            });
            return state;
        };
        
        window.restoreCollapseState = function(state) {
            if (!state) return;
            Object.keys(state).forEach(id => {
                const content = document.getElementById(id);
                if (content) {
                    const shouldBeExpanded = state[id];
                    content.style.display = shouldBeExpanded ? 'block' : 'none';
                    
                    // Update icon
                    const header = content.previousElementSibling;
                    if (header) {
                        const icon = header.querySelector('span[id$="-icon"]');
                        if (icon) {
                            const plusSrc = icon.getAttribute('data-plus');
                            const subtractSrc = icon.getAttribute('data-subtract');
                            if (plusSrc && subtractSrc) {
                                const img = icon.querySelector('img');
                                if (img) {
                                    img.src = shouldBeExpanded ? subtractSrc : plusSrc;
                                }
                            }
                        }
                    }
                }
            });
        };
        
        window.toggleCollapse = function(elementId) {
            const content = document.getElementById(elementId);
            if (content) {
                const isHidden = content.style.display === 'none';
                content.style.display = isHidden ? 'block' : 'none';
                
                const header = content.previousElementSibling;
                if (header) {
                    const icon = header.querySelector('span[id$="-icon"]');
                    if (icon) {
                        // Update image src instead of text content - no emojis
                        const plusSrc = icon.getAttribute('data-plus');
                        const subtractSrc = icon.getAttribute('data-subtract');
                        if (plusSrc && subtractSrc) {
                            const img = icon.querySelector('img');
                            if (img) {
                                img.src = isHidden ? subtractSrc : plusSrc;
                            } else {
                                // Create img if it doesn't exist
                                const imgSrc = isHidden ? subtractSrc : plusSrc;
                                const imgAlt = isHidden ? 'Collapse' : 'Expand';
                                icon.innerHTML = '<img src="' + imgSrc + '" style="width: 12px; height: 12px; vertical-align: middle;" alt="' + imgAlt + '" />';
                            }
                        }
                    }
                }
                
                // Save state to sessionStorage
                const currentState = window.getCollapseState();
                sessionStorage.setItem('collapseState', JSON.stringify(currentState));
            }
        };
        
        window.openFile = function(filePath, event) {
            // Prevent default link behavior (scroll to top)
            if (event) {
                event.preventDefault();
                event.stopPropagation();
            }
            // Resolve scoped diagram filename when a node is selected.
            // For specs that had {scope} (resolved to -all), replace -all with -slug.
            // For other specs, append -slug before .drawio.
            var resolvedPath = filePath;
            if (window.diagramScope && filePath && filePath.indexOf('.drawio') !== -1) {
                var slug = window.diagramScope.toLowerCase().split(' ').join('-').split('').filter(function(c) {
                    return (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') || c === '-';
                }).join('');
                if (slug && filePath.indexOf('-' + slug + '.drawio') === -1) {
                    if (filePath.indexOf('-all.drawio') !== -1) {
                        resolvedPath = filePath.split('-all.drawio').join('-' + slug + '.drawio');
                    } else {
                        resolvedPath = filePath.split('.drawio').join('-' + slug + '.drawio');
                    }
                }
            }
            console.log('[WebView] openFile called with:', resolvedPath);
            // Save scroll position before opening file (which may cause focus change)
            var savedScrollY = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
            sessionStorage.setItem('scrollPosition', savedScrollY.toString());
            console.log('[WebView] Saved scroll position before file open:', savedScrollY);
            
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] openFile called with: ' + resolvedPath
            });
            vscode.postMessage({
                command: 'openFile',
                filePath: resolvedPath
            });
            
            // Ensure scroll position is preserved after message sending (prevents any DOM reflow issues)
            setTimeout(() => {
                window.scrollTo(0, savedScrollY);
            }, 0);
            
            return false;
        };
        window.openFiles = function(filePaths, event) {
            if (event) {
                event.preventDefault();
                event.stopPropagation();
            }
            if (!filePaths || !Array.isArray(filePaths) || filePaths.length === 0) return false;
            const savedScrollY = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
            sessionStorage.setItem('scrollPosition', savedScrollY.toString());
            vscode.postMessage({ command: 'openFiles', filePaths: filePaths });
            setTimeout(() => { window.scrollTo(0, savedScrollY); }, 0);
            return false;
        };
        window.openFilesFromEl = function(el, event) {
            if (event) { event.preventDefault(); event.stopPropagation(); }
            const raw = el && el.getAttribute && el.getAttribute('data-test-files');
            if (raw) {
                try {
                    window.openFiles(JSON.parse(raw));
                } catch (e) {
                    console.error('[WebView] openFilesFromEl parse error:', e);
                }
            }
            return false;
        };
        
        // Expand clarification answer boxes to show full content (no scroll) on load/refresh
        window.expandClarifyBoxes = function() {
            const textareas = document.querySelectorAll('[id^="clarify-answer-"]');
            textareas.forEach((ta) => {
                if (ta.getAttribute('data-collapsed') === 'false') {
                    ta.style.overflow = 'hidden';
                    ta.style.height = '0px';
                    const h = ta.scrollHeight;
                    ta.style.height = Math.max(60, h) + 'px';
                    ta.style.overflow = 'visible';
                }
            });
        };
        
        // Scroll position preservation functions
        window.saveScrollPosition = function() {
            const scrollY = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
            sessionStorage.setItem('scrollPosition', scrollY.toString());
            console.log('[WebView] Saved scroll position:', scrollY);
        };
        
        window.restoreScrollPosition = function() {
            const savedPosition = sessionStorage.getItem('scrollPosition');
            if (savedPosition) {
                const scrollY = parseInt(savedPosition, 10);
                window.scrollTo(0, scrollY);
                console.log('[WebView] Restored scroll position:', scrollY);
            }
        };
        
        window.updateFilter = function(filterValue) {
            console.log('[WebView] updateFilter called with:', filterValue);
            const message = {
                command: 'updateFilter',
                filter: filterValue
            };
            console.log('[WebView] Sending message:', message);
            vscode.postMessage(message);
            console.log('[WebView] postMessage sent');
        };
        
        // Test if updateFilter is defined
        console.log('[WebView] updateFilter function exists:', typeof updateFilter);
        
        window.updateIncludeLevel = function(level) {
            console.log('[WebView] updateIncludeLevel called with:', level);
            vscode.postMessage({
                command: 'updateIncludeLevel',
                includeLevel: level
            });
        };
        
        window.clearScopeFilter = function() {
            vscode.postMessage({
                command: 'clearScopeFilter'
            });
        };
        
        window.showAllScope = function() {
            console.log('[WebView] showAllScope called');
            vscode.postMessage({
                command: 'showAllScope'
            });
        };
        
        window.executeNavigationCommand = function(command) {
            console.log('[WebView] executeNavigationCommand click ->', command);
            vscode.postMessage({
                command: 'executeNavigationCommand',
                commandText: command
            });
        };
        
        window.navigateToBehavior = function(behaviorName) {
            vscode.postMessage({
                command: 'navigateToBehavior',
                behaviorName: behaviorName
            });
        };
        
        window.navigateToAction = function(behaviorName, actionName) {
            vscode.postMessage({
                command: 'navigateToAction',
                behaviorName: behaviorName,
                actionName: actionName
            });
        };
        
        window.navigateAndExecute = function(behaviorName, actionName, operationName) {
            console.log('[WebView] navigateAndExecute click ->', behaviorName, actionName, operationName);
            vscode.postMessage({
                command: 'navigateAndExecute',
                behaviorName: behaviorName,
                actionName: actionName,
                operationName: operationName
            });
        };
        
        function submitToChat() {
            vscode.postMessage({
                command: 'sendToChat'
            });
        }

        function sendInstructionsToChat(event) {
            if (event) {
                event.stopPropagation();
            }
            console.log('[WebView] sendInstructionsToChat triggered');
            const promptContent = window._promptContent || '';
            if (!promptContent) {
                console.warn('[WebView] No prompt content available to submit');
                return;
            }
            vscode.postMessage({
                command: 'sendToChat',
                content: promptContent
            });
        }

        function refreshStatus() {
            vscode.postMessage({
                command: 'refresh'
            });
        }
        
        // Async save status indicator functions
        let pendingOperations = 0;
        
        function showSaveStatus(operationCount) {
            console.log('[ASYNC_SAVE] [STEP 1] showSaveStatus() called operationCount=' + operationCount + ' timestamp=' + new Date().toISOString());
            pendingOperations = operationCount;
            const indicator = document.getElementById('save-status-indicator');
            const spinner = document.getElementById('save-status-spinner');
            const message = document.getElementById('save-status-message');
            
            if (!indicator) {
                console.error('[ASYNC_SAVE] [ERROR] save-status-indicator element not found!');
                return;
            }
            if (!spinner) {
                console.error('[ASYNC_SAVE] [ERROR] save-status-spinner element not found!');
                return;
            }
            if (!message) {
                console.error('[ASYNC_SAVE] [ERROR] save-status-message element not found!');
                return;
            }
            
            console.log('[ASYNC_SAVE] [STEP 2] Setting indicator display to flex');
            indicator.style.display = 'flex';
            spinner.style.display = 'inline-block';
            const statusMessage = operationCount > 1 
                ? 'Saving ' + operationCount + ' changes...' 
                : 'Saving 1 change...';
            message.textContent = statusMessage;
            console.log('[ASYNC_SAVE] [STEP 3] Status indicator visible indicatorDisplay=' + indicator.style.display + ' spinnerDisplay=' + spinner.style.display + ' messageText=' + statusMessage + ' elementVisible=' + (indicator.offsetParent !== null));
        }
        
        function hideSaveStatus() {
            console.log('[ASYNC_SAVE] hideSaveStatus() called timestamp=' + new Date().toISOString());
            const indicator = document.getElementById('save-status-indicator');
            if (indicator) {
                indicator.style.display = 'none';
                console.log('[ASYNC_SAVE] Status indicator hidden');
            }
            pendingOperations = 0;
        }
        
        function showSaveSuccess() {
            console.log('[ASYNC_SAVE] [SUCCESS] showSaveSuccess() called timestamp=' + new Date().toISOString());
            const indicator = document.getElementById('save-status-indicator');
            const spinner = document.getElementById('save-status-spinner');
            const message = document.getElementById('save-status-message');
            if (indicator && spinner && message) {
                console.log('[ASYNC_SAVE] [SUCCESS] Updating indicator to show success');
                indicator.style.display = 'flex';
                spinner.style.display = 'none';
                message.textContent = 'Saved';
                message.style.color = '#ff8c00';
                console.log('[ASYNC_SAVE] [SUCCESS] Scheduling auto-hide in 2000ms');
                setTimeout(() => {
                    console.log('[ASYNC_SAVE] [SUCCESS] Auto-hide timeout fired, hiding indicator');
                    hideSaveStatus();
                }, 2000);
            } else {
                console.error('[ASYNC_SAVE] [ERROR] Cannot show success - elements missing hasIndicator=' + !!indicator + ' hasSpinner=' + !!spinner + ' hasMessage=' + !!message);
            }
        }
        
        function showSaveError(errorMessage) {
            console.log('[ASYNC_SAVE] [ERROR] showSaveError() called errorMessage=' + errorMessage + ' timestamp=' + new Date().toISOString());
            const indicator = document.getElementById('save-status-indicator');
            const spinner = document.getElementById('save-status-spinner');
            const message = document.getElementById('save-status-message');
            if (indicator && spinner && message) {
                console.log('[ASYNC_SAVE] [ERROR] Updating indicator to show error');
                indicator.style.display = 'flex';
                spinner.style.display = 'none';
                message.textContent = 'Save failed - click for details';
                message.style.color = '#f48771';
                message.style.cursor = 'pointer';
                message.onclick = function() {
                    console.log('[ASYNC_SAVE] [ERROR] Error indicator clicked, showing alert');
                    alert('Save Error: ' + errorMessage);
                };
                console.log('[ASYNC_SAVE] [ERROR] Error indicator displayed (will not auto-hide)');
            } else {
                console.error('[ASYNC_SAVE] [ERROR] Cannot show error - elements missing hasIndicator=' + !!indicator + ' hasSpinner=' + !!spinner + ' hasMessage=' + !!message);
            }
        }
        
        // Optimistic DOM update for move operations
        function applyOptimisticMove(draggedNodeElement, targetElement, dropZone, finalPosition) {
            var draggedNodeName = draggedNodeElement ? draggedNodeElement.getAttribute('data-node-name') : null;
            var targetNodeName = targetElement ? targetElement.getAttribute('data-node-name') : null;
            console.log('[ASYNC_SAVE] [OPTIMISTIC] applyOptimisticMove() called dropZone=' + dropZone + ' finalPosition=' + finalPosition + ' draggedNode=' + draggedNodeName + ' targetNode=' + targetNodeName + ' timestamp=' + new Date().toISOString());
            
            if (!draggedNodeElement || !targetElement) {
                console.error('[ASYNC_SAVE] [OPTIMISTIC] [ERROR] Cannot apply optimistic move - missing elements hasDraggedElement=' + !!draggedNodeElement + ' hasTargetElement=' + !!targetElement);
                return;
            }
            
            // Find the parent container
            const draggedParent = draggedNodeElement.parentElement;
            const targetParent = dropZone === 'inside' ? targetElement : targetElement.parentElement;
            
            console.log('[ASYNC_SAVE] [OPTIMISTIC] Found parent elements hasDraggedParent=' + !!draggedParent + ' hasTargetParent=' + !!targetParent + ' sameParent=' + (draggedParent === targetParent));
            
            if (!draggedParent || !targetParent) {
                console.error('[ASYNC_SAVE] [OPTIMISTIC] [ERROR] Cannot apply optimistic move - missing parent elements');
                return;
            }
            
            // If moving within same parent, reorder
            if (draggedParent === targetParent && dropZone === 'after') {
                const targetPos = parseInt(targetElement.getAttribute('data-position') || '0');
                const draggedPos = parseInt(draggedNodeElement.getAttribute('data-position') || '0');
                
                console.log('[ASYNC_SAVE] [OPTIMISTIC] Moving within same parent draggedPos=' + draggedPos + ' targetPos=' + targetPos + ' finalPosition=' + finalPosition + ' dropZone=' + dropZone);
                
                // Remove dragged node from its current position
                const draggedClone = draggedNodeElement.cloneNode(true);
                draggedNodeElement.remove();
                console.log('[ASYNC_SAVE] [OPTIMISTIC] Removed dragged node from original position');
                
                // Find insertion point
                const children = Array.from(targetParent.children).filter(child => 
                    child.classList.contains('story-node') || 
                    child.querySelector && child.querySelector('.story-node')
                );
                
                console.log('[ASYNC_SAVE] [OPTIMISTIC] Found children childrenCount=' + children.length);
                
                let insertIndex = finalPosition;
                if (insertIndex >= children.length) {
                    targetParent.appendChild(draggedClone);
                    console.log('[ASYNC_SAVE] [OPTIMISTIC] Appended to end');
                } else {
                    const insertBefore = children[insertIndex];
                    if (insertBefore) {
                        targetParent.insertBefore(draggedClone, insertBefore);
                        console.log('[ASYNC_SAVE] [OPTIMISTIC] Inserted before child at index', insertIndex);
                    } else {
                        targetParent.appendChild(draggedClone);
                        console.log('[ASYNC_SAVE] [OPTIMISTIC] Fallback: appended to end');
                    }
                }
                
                // Update position attributes
                updateNodePositions(targetParent);
                
                console.log('[ASYNC_SAVE] [OPTIMISTIC] [SUCCESS] Optimistic move applied - node moved in DOM');
            } else if (dropZone === 'inside') {
                // Moving into a container - this is more complex and may require full refresh
                console.log('[ASYNC_SAVE] [OPTIMISTIC] Moving to inside container - will rely on backend refresh');
            } else {
                console.warn('[ASYNC_SAVE] [OPTIMISTIC] Unhandled move scenario dropZone=' + dropZone + ' sameParent=' + (draggedParent === targetParent));
            }
        }
        
        function updateNodePositions(container) {
            const nodes = Array.from(container.children).filter(child => 
                child.classList.contains('story-node') || 
                (child.querySelector && child.querySelector('.story-node'))
            );
            nodes.forEach((node, index) => {
                const storyNode = node.classList.contains('story-node') ? node : node.querySelector('.story-node');
                if (storyNode) {
                    storyNode.setAttribute('data-position', index.toString());
                }
            });
        }
        
        function updateWorkspace(workspacePath) {
            console.log('[WebView] updateWorkspace called with:', workspacePath);
            vscode.postMessage({
                command: 'updateWorkspace',
                workspacePath: workspacePath
            });
        }
        
        function browseWorkspace() {
            console.log('[WebView] browseWorkspace called');
            vscode.postMessage({
                command: 'browseWorkspace'
            });
        }
        
        window.switchBot = function(botName) {
            console.log('[WebView] switchBot called with:', botName);
            vscode.postMessage({
                command: 'switchBot',
                botName: botName
            });
        };
        
        window.getBehaviorRules = function(behaviorName) {
            console.log('[WebView] getBehaviorRules called with:', behaviorName);
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] getBehaviorRules BUTTON CLICKED for: ' + behaviorName
            });
            vscode.postMessage({
                command: 'getBehaviorRules',
                behaviorName: behaviorName
            });
        };
        
        // Story Graph Edit functions
        window.createEpic = function() {
            console.log('═══════════════════════════════════════════════════════');
            console.log('[WebView] createEpic CALLED');
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] createEpic called'
            });
            
            // Use optimistic update handler from story_map_view.js if available
            if (typeof window.handleCreateNode === 'function') {
                console.log('[WebView] Using optimistic create handler');
                window.handleCreateNode({
                    parentPath: 'story_graph',
                    nodeType: 'epic'
                    // placeholderName will be auto-generated (Epic1, Epic2, etc.)
                });
            } else {
                console.warn('[WebView] handleCreateNode not available, falling back to direct command');
                vscode.postMessage({
                    command: 'executeCommand',
                    commandText: 'story_graph.create_epic',
                    optimistic: true
                });
            }
            console.log('[WebView] postMessage sent successfully');
            console.log('═══════════════════════════════════════════════════════');
        };
        
        window.createSubEpic = function(parentName) {
            console.log('[WebView] createSubEpic called for:', parentName);
            vscode.postMessage({
                command: 'executeCommand',
                commandText: \`story_graph."\${parentName}".create\`,
                optimistic: true
            });
        };
        
        window.createStory = function(parentName) {
            console.log('[WebView] createStory called for:', parentName);
            vscode.postMessage({
                command: 'executeCommand',
                commandText: \`story_graph."\${parentName}".create_story\`,
                optimistic: true
            });
        };
        
        window.createScenario = function(storyName) {
            console.log('[WebView] createScenario called for:', storyName);
            vscode.postMessage({
                command: 'executeCommand',
                commandText: \`story_graph."\${storyName}".create_scenario\`,
                optimistic: true
            });
        };
        
        window.createScenarioOutline = function(storyName) {
            console.log('[WebView] createScenarioOutline called for:', storyName);
            console.log('[WebView] Note: ScenarioOutline deprecated, creating Scenario instead');
            vscode.postMessage({
                command: 'executeCommand',
                commandText: \`story_graph."\${storyName}".create_scenario\`,
                optimistic: true
            });
        };
        
        window.createAcceptanceCriteria = function(storyName) {
            console.log('[WebView] createAcceptanceCriteria called for:', storyName);
            vscode.postMessage({
                command: 'executeCommand',
                commandText: \`story_graph."\${storyName}".create_acceptance_criteria\`,
                optimistic: true
            });
        };
        
        window.deleteNode = function(nodePath) {
            console.log('[WebView] deleteNode called for:', nodePath);
            
            // Use optimistic update handler from story_map_view.js if available
            if (typeof window.handleDeleteNode === 'function') {
                console.log('[WebView] Using optimistic delete handler');
                window.handleDeleteNode({
                    nodePath: nodePath
                });
            } else {
                console.warn('[WebView] handleDeleteNode not available, falling back to direct command');
                // Fallback: send command directly (defaults to optimistic for story-changing ops)
                vscode.postMessage({
                    command: 'executeCommand',
                    commandText: nodePath + '.delete'
                    // optimistic defaults to true for story-changing operations
                });
            }
        };
        
        window.deleteNodeIncludingChildren = function(nodePath) {
            console.log('[WebView] deleteNodeIncludingChildren called for:', nodePath);
            
            // Use optimistic update handler from story_map_view.js if available
            // Delete ALWAYS includes children - no version without children
            if (typeof window.handleDeleteNode === 'function') {
                console.log('[WebView] Using optimistic delete handler (always includes children)');
                window.handleDeleteNode({
                    nodePath: nodePath
                });
            } else {
                console.warn('[WebView] handleDeleteNode not available, falling back to direct command');
                // Fallback: send command directly (defaults to optimistic for story-changing ops)
                // Backend delete() method defaults to cascade=True (always includes children)
                vscode.postMessage({
                    command: 'executeCommand',
                    commandText: nodePath + '.delete()'
                    // optimistic defaults to true for story-changing operations
                });
            }
        };
        
        window.enableEditMode = function(nodePath) {
            console.log('[ASYNC_SAVE] ========== RENAME OPERATION START ==========');
            console.log('[ASYNC_SAVE] [USER_ACTION] User double-clicked node to rename nodePath=' + nodePath + ' timestamp=' + new Date().toISOString());
            // Extract the current node name from the path
            // Path format: story_graph."Epic"."SubEpic"."Story"
            const matches = nodePath.match(/"([^"]+)"[^"]*$/);
            const currentName = matches ? matches[1] : '';
            
            console.log('[ASYNC_SAVE] [USER_ACTION] Extracted current name currentName=' + currentName);
            console.log('[ASYNC_SAVE] [USER_ACTION] Sending renameNode message to extension host');
            vscode.postMessage({
                command: 'renameNode',
                nodePath: nodePath,
                currentName: currentName
            });
            console.log('[ASYNC_SAVE] ========== RENAME OPERATION INITIATED ==========');
        };
        
        // Track selected node for contextual actions (initialize window.selectedNode)
        window.selectedNode = {
            type: 'root', // root, epic, sub-epic, story
            name: null,
            path: null, // Full path like story_graph."Epic"."SubEpic"
            canHaveSubEpic: false,
            canHaveStory: false,
            canHaveTests: false,
            hasChildren: false,
            hasStories: false,
            hasNestedSubEpics: false
        };
        
        // Map behavior names from backend to tooltip text (global function)
        window.behaviorToTooltipText = function(behavior) {
            var behaviorMap = {
                'shape': 'Shape',
                'exploration': 'Explore',
                'scenarios': 'Write Scenarios for',
                'tests': 'Write Tests for',
                'code': 'Write Code for'
            };
            return behaviorMap[behavior] || 'Submit';
        };
        
        
        // Update contextual action buttons based on selection
        window.updateContextualButtons = function() {
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] updateContextualButtons called, selectedNode=' + JSON.stringify(window.selectedNode)
            });
            
            const btnCreateEpic = document.getElementById('btn-create-epic');
            const btnCreateSubEpic = document.getElementById('btn-create-sub-epic');
            const btnCreateStory = document.getElementById('btn-create-story');
            const btnCreateScenario = document.getElementById('btn-create-scenario');
            const btnCreateAcceptanceCriteria = document.getElementById('btn-create-acceptance-criteria');
            const btnDelete = document.getElementById('btn-delete');
            const btnScopeTo = document.getElementById('btn-scope-to');
            const btnSubmit = document.getElementById('btn-submit');
            const btnOpenGraph = document.getElementById('btn-open-graph');
            const btnOpenAll = document.getElementById('btn-open-all');
            
            // Hide all buttons first
            if (btnCreateEpic) btnCreateEpic.style.display = 'none';
            if (btnCreateSubEpic) btnCreateSubEpic.style.display = 'none';
            if (btnCreateStory) btnCreateStory.style.display = 'none';
            if (btnCreateScenario) btnCreateScenario.style.display = 'none';
            if (btnCreateAcceptanceCriteria) btnCreateAcceptanceCriteria.style.display = 'none';
            if (btnDelete) btnDelete.style.display = 'none';
            if (btnScopeTo) btnScopeTo.style.display = 'none';
            if (btnSubmit) btnSubmit.style.display = 'none';
            if (btnOpenGraph) btnOpenGraph.style.display = 'none';
            if (btnOpenAll) btnOpenAll.style.display = 'none';
            
            // Show buttons based on selection
            if (window.selectedNode.type === 'root') {
                if (btnCreateEpic) btnCreateEpic.style.display = 'block';
            } else if (window.selectedNode.type === 'epic') {
                if (btnCreateSubEpic) btnCreateSubEpic.style.display = 'block';
                if (btnDelete) btnDelete.style.display = 'block';
                if (btnScopeTo) btnScopeTo.style.display = 'block';
            } else if (window.selectedNode.type === 'sub-epic') {
                // Sub-epics can have EITHER sub-epics OR stories, not both
                // If it has stories, only show create story button
                // If it has sub-epics, only show create sub-epic button
                // If empty, show both options
                if (window.selectedNode.hasStories) {
                    // Has stories - only allow adding more stories
                    if (btnCreateStory) btnCreateStory.style.display = 'block';
                } else if (window.selectedNode.hasNestedSubEpics) {
                    // Has nested sub-epics - only allow adding more sub-epics
                    if (btnCreateSubEpic) btnCreateSubEpic.style.display = 'block';
                } else {
                    // Empty - show both options
                    if (btnCreateSubEpic) btnCreateSubEpic.style.display = 'block';
                    if (btnCreateStory) btnCreateStory.style.display = 'block';
                }
                if (btnDelete) btnDelete.style.display = 'block';
                if (btnScopeTo) btnScopeTo.style.display = 'block';
            } else if (window.selectedNode.type === 'story') {
                // Stories can have both scenarios and acceptance criteria
                if (btnCreateScenario) btnCreateScenario.style.display = 'block';
                if (btnCreateAcceptanceCriteria) btnCreateAcceptanceCriteria.style.display = 'block';
                if (btnDelete) btnDelete.style.display = 'block';
                if (btnScopeTo) btnScopeTo.style.display = 'block';
            } else if (window.selectedNode.type === 'scenario') {
                // Scenarios can also be scoped to and submitted
                if (btnDelete) btnDelete.style.display = 'block';
                if (btnScopeTo) btnScopeTo.style.display = 'block';
                // Note: submit button will be shown below if scenario has behavior_needed
            }
            
            // Show related files buttons for all non-root nodes
            if (window.selectedNode.type !== 'root') {
                if (btnOpenGraph) btnOpenGraph.style.display = 'block';
                if (btnOpenAll) btnOpenAll.style.display = 'block';
            }
            
            // Update diagram scope global and button labels.
            // The onclick handlers read window.diagramScope at click time,
            // so we never need to rewrite onclick attributes (avoids
            // backslash/escaping issues inside this template literal).
            var dScope = (window.selectedNode.type !== 'root' && window.selectedNode.name)
                ? window.selectedNode.name : '';
            window.diagramScope = dScope;
            
            var renderBtns = document.querySelectorAll('.render-button');
            for (var ri = 0; ri < renderBtns.length; ri++) {
                renderBtns[ri].textContent = dScope ? 'Render Diagram for "' + dScope + '"' : 'Render Diagram';
            }
            var saveBtns = document.querySelectorAll('.save-layout-button');
            for (var si = 0; si < saveBtns.length; si++) {
                saveBtns[si].textContent = dScope ? 'Save Layout for "' + dScope + '"' : 'Save Layout';
            }
            var clearBtns = document.querySelectorAll('.clear-layout-button');
            for (var ci = 0; ci < clearBtns.length; ci++) {
                clearBtns[ci].textContent = dScope ? 'Clear Layout for "' + dScope + '"' : 'Clear Layout';
            }
            var reportBtns = document.querySelectorAll('.generate-report-button');
            for (var gi = 0; gi < reportBtns.length; gi++) {
                reportBtns[gi].textContent = dScope ? 'Generate Report for "' + dScope + '"' : 'Generate Report';
            }
            var updateBtns = document.querySelectorAll('.update-button');
            for (var ui = 0; ui < updateBtns.length; ui++) {
                updateBtns[ui].textContent = dScope ? 'Update Graph for "' + dScope + '"' : 'Update Graph';
            }
            
            // Update diagram file link to show the scoped filename
            var scopeSlug = dScope ? dScope.toLowerCase().split(' ').join('-').split('').filter(function(c) {
                return (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') || c === '-';
            }).join('') : '';
            var diagLinks = document.querySelectorAll('.diagram-link');
            for (var di = 0; di < diagLinks.length; di++) {
                var origName = diagLinks[di].getAttribute('data-original-name') || '';
                if (scopeSlug && origName) {
                    if (origName.indexOf('-all.drawio') !== -1) {
                        diagLinks[di].textContent = origName.split('-all.drawio').join('-' + scopeSlug + '.drawio');
                    } else {
                        diagLinks[di].textContent = origName.split('.drawio').join('-' + scopeSlug + '.drawio');
                    }
                } else if (origName) {
                    diagLinks[di].textContent = origName;
                }
            }
            
            // Update submit button based on current behavior and action
            console.log('═══════════════════════════════════════════════════════');
            console.log('[SUBMIT BUTTON DEBUG] Starting submit button update');
            console.log('[SUBMIT BUTTON DEBUG] Node clicked:', window.selectedNode.name);
            console.log('[SUBMIT BUTTON DEBUG] Node type:', window.selectedNode.type);
            console.log('[SUBMIT BUTTON DEBUG] Current behavior from bot:', window.currentBehavior || '(none)');
            console.log('[SUBMIT BUTTON DEBUG] Current action from bot:', window.currentAction || '(none)');
            console.log('[SUBMIT BUTTON DEBUG] behavior_needed from node:', window.selectedNode.behaviorNeeded || '(none)');
            console.log('[SUBMIT BUTTON DEBUG] btnSubmit exists:', !!btnSubmit);
            console.log('[SUBMIT BUTTON DEBUG] Is root?', window.selectedNode.type === 'root');
            console.log('[SUBMIT BUTTON DEBUG] Has behaviorNeeded?', !!window.selectedNode.behaviorNeeded);
            
            // btn-submit uses behavior_needed (required next behavior), not current behavior
            const requiredBehavior = window.selectedNode.behaviorNeeded;
            const currentBehavior = window.currentBehavior || window.selectedNode.behavior;
            const currentAction = window.currentAction || 'build'; // Default to 'build' if no action
            
            if (btnSubmit && window.selectedNode.type !== 'root' && requiredBehavior) {
                const behavior = requiredBehavior;
                const action = currentAction;
                const nodeType = window.selectedNode.type;
                const btnSubmitIcon = document.getElementById('btn-submit-icon');
                
                console.log('[SUBMIT BUTTON DEBUG] Proceeding with button update...');
                console.log('[SUBMIT BUTTON DEBUG] btnSubmitIcon exists:', !!btnSubmitIcon);
                
                // Map behavior to icon and tooltip
                const behaviorMap = {
                    'shape': {
                        icon: btnSubmit.getAttribute('data-shape-icon'),
                        tooltip: btnSubmit.getAttribute('data-shape-tooltip') || 'Submit shape instructions for ' + nodeType
                    },
                    'exploration': {
                        icon: btnSubmit.getAttribute('data-exploration-icon'),
                        tooltip: btnSubmit.getAttribute('data-exploration-tooltip') || 'Submit exploration instructions for ' + nodeType
                    },
                    'scenarios': {
                        icon: btnSubmit.getAttribute('data-scenarios-icon'),
                        tooltip: btnSubmit.getAttribute('data-scenarios-tooltip') || 'Submit scenarios instructions for ' + nodeType
                    },
                    'tests': {
                        icon: btnSubmit.getAttribute('data-tests-icon'),
                        tooltip: btnSubmit.getAttribute('data-tests-tooltip') || 'Submit tests instructions for ' + nodeType
                    },
                    'code': {
                        icon: btnSubmit.getAttribute('data-code-icon'),
                        tooltip: btnSubmit.getAttribute('data-code-tooltip') || 'Submit code instructions for ' + nodeType
                    }
                };
                
                console.log('[SUBMIT BUTTON DEBUG] Behavior map created for all behaviors');
                console.log('[SUBMIT BUTTON DEBUG] Looking up behavior:', behavior);
                
                const behaviorConfig = behaviorMap[behavior];
                console.log('[SUBMIT BUTTON DEBUG] Behavior config found:', !!behaviorConfig);
                
                if (behaviorConfig) {
                    console.log('[SUBMIT BUTTON DEBUG] ✓ Behavior config exists');
                    console.log('[SUBMIT BUTTON DEBUG] Image icon path:', behaviorConfig.icon);
                    console.log('[SUBMIT BUTTON DEBUG] Hover tooltip:', behaviorConfig.tooltip);
                } else {
                    console.log('[SUBMIT BUTTON DEBUG] ✗ No behavior config found for:', behavior);
                    console.log('[SUBMIT BUTTON DEBUG] Available behaviors:', Object.keys(behaviorMap));
                }
                
                if (behaviorConfig && btnSubmitIcon) {
                    btnSubmitIcon.src = behaviorConfig.icon;
                    btnSubmit.title = behaviorConfig.tooltip;
                    btnSubmit.style.display = 'block';
                    
                    console.log('[SUBMIT BUTTON DEBUG] ✓ Submit button updated successfully');
                    console.log('[SUBMIT BUTTON DEBUG] ✓ Icon src set to:', behaviorConfig.icon);
                    console.log('[SUBMIT BUTTON DEBUG] ✓ Tooltip set to:', behaviorConfig.tooltip);
                    console.log('[SUBMIT BUTTON DEBUG] ✓ Button displayed');
                    
                    vscode.postMessage({
                        command: 'logToFile',
                        message: '[WebView] Submit button updated: behavior=' + behavior + ', nodeType=' + nodeType + ', icon=' + behaviorConfig.icon + ', tooltip="' + behaviorConfig.tooltip + '"'
                    });
                } else {
                    if (!behaviorConfig) {
                        console.log('[SUBMIT BUTTON DEBUG] ✗ Missing behaviorConfig');
                    }
                    if (!btnSubmitIcon) {
                        console.log('[SUBMIT BUTTON DEBUG] ✗ Missing btnSubmitIcon element');
                    }
                }
            } else {
                console.log('[SUBMIT BUTTON DEBUG] Submit button NOT updated - conditions not met:');
                if (!btnSubmit) {
                    console.log('[SUBMIT BUTTON DEBUG] ✗ btnSubmit element not found');
                }
                if (window.selectedNode.type === 'root') {
                    console.log('[SUBMIT BUTTON DEBUG] ✗ Node is root (submit not shown for root)');
                }
                if (!window.selectedNode.behavior) {
                    console.log('[SUBMIT BUTTON DEBUG] ✗ No behavior_needed set on node');
                    console.log('[SUBMIT BUTTON DEBUG]   This may indicate behavior_needed is not being read from story graph');
                }
            }
            
            // Update btn-submit-alt button (shows when there are multiple behaviors_needed)
            const btnSubmitAlt = document.getElementById('btn-submit-alt');
            const behaviorsNeeded = window.selectedNode.behaviorsNeeded || [];
            console.log('[SUBMIT BUTTON DEBUG] behaviorsNeeded:', behaviorsNeeded);
            
            if (btnSubmitAlt && behaviorsNeeded.length > 1 && window.selectedNode.type !== 'root') {
                const altBehavior = behaviorsNeeded[1]; // Second behavior option
                const nodeType = window.selectedNode.type;
                const btnSubmitAltIcon = document.getElementById('btn-submit-alt-icon');
                
                // Map behavior to icon and tooltip for alt button
                const altBehaviorMap = {
                    'shape': {
                        icon: btnSubmitAlt.getAttribute('data-shape-icon'),
                        tooltip: 'Submit shape instructions for ' + nodeType
                    },
                    'exploration': {
                        icon: btnSubmitAlt.getAttribute('data-exploration-icon'),
                        tooltip: 'Submit exploration instructions for ' + nodeType
                    },
                    'scenarios': {
                        icon: btnSubmitAlt.getAttribute('data-scenarios-icon'),
                        tooltip: 'Submit scenarios instructions for ' + nodeType
                    },
                    'tests': {
                        icon: btnSubmitAlt.getAttribute('data-tests-icon'),
                        tooltip: 'Submit tests instructions for ' + nodeType
                    },
                    'code': {
                        icon: btnSubmitAlt.getAttribute('data-code-icon'),
                        tooltip: 'Submit code instructions for ' + nodeType
                    }
                };
                
                const altBehaviorConfig = altBehaviorMap[altBehavior];
                if (altBehaviorConfig && btnSubmitAltIcon) {
                    btnSubmitAltIcon.src = altBehaviorConfig.icon;
                    btnSubmitAlt.title = altBehaviorConfig.tooltip;
                    btnSubmitAlt.style.display = 'block';
                    // Store alt behavior for handleSubmitAlt
                    btnSubmitAlt.setAttribute('data-current-behavior', altBehavior);
                    console.log('[SUBMIT BUTTON DEBUG] Alt button shown for behavior:', altBehavior);
                } else {
                    btnSubmitAlt.style.display = 'none';
                }
            } else if (btnSubmitAlt) {
                btnSubmitAlt.style.display = 'none';
            }
            
            // Update btn-submit-current button (shows beside btn-submit)
            const btnSubmitCurrent = document.getElementById('btn-submit-current');
            if (btnSubmitCurrent && window.selectedNode.type !== 'root' && currentBehavior) {
                const behavior = currentBehavior;
                const action = currentAction;
                const btnSubmitCurrentIcon = document.getElementById('btn-submit-current-icon');
                
                // Use refresh icon for now (same as btn-submit)
                const refreshIcon = btnSubmitCurrent.getAttribute('data-refresh-icon') || btnSubmit?.getAttribute('data-refresh-icon');
                
                const tooltip = 'Submit current behavior (' + behavior + '.' + action + ')';
                
                if (refreshIcon && btnSubmitCurrentIcon) {
                    btnSubmitCurrentIcon.src = refreshIcon;
                    btnSubmitCurrent.title = tooltip;
                    btnSubmitCurrent.style.display = 'block';
                } else {
                    btnSubmitCurrent.style.display = 'none';
                }
            } else if (btnSubmitCurrent) {
                btnSubmitCurrent.style.display = 'none';
            }
            
            console.log('═══════════════════════════════════════════════════════');
        };
        
        // Select a node (called when clicking on node name/icon)
        window.selectNode = function(type, name, options = {}) {
            console.log('═══════════════════════════════════════════════════════');
            console.log('[WebView] selectNode CALLED');
            console.log('[WebView]   type:', type);
            console.log('[WebView]   name:', name);
            console.log('[WebView]   options:', JSON.stringify(options, null, 2));
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] selectNode: type=' + type + ', name=' + name + ', options=' + JSON.stringify(options)
            });
            
            // Remove selected class from all nodes
            document.querySelectorAll('.story-node.selected').forEach(node => {
                node.classList.remove('selected');
            });
            
            // Add selected class to the clicked node
            let targetNode = null;
            
            // First try to find by path if available (more specific for nested nodes)
            if (options.path) {
                const allNodes = document.querySelectorAll('.story-node[data-path]');
                for (const node of allNodes) {
                    if (node.getAttribute('data-path') === options.path) {
                        targetNode = node;
                        console.log('[WebView]   Found node by path:', options.path);
                        break;
                    }
                }
            }
            
            // Fallback to name+type if path not found
            if (!targetNode) {
                const nodeName = name || 'Story Map';
                targetNode = document.querySelector('.story-node[data-node-type="' + type + '"][data-node-name="' + nodeName + '"]');
                console.log('[WebView]   Found node by type+name:', type, nodeName);
            }
            
            if (targetNode) {
                targetNode.classList.add('selected');
                console.log('[WebView]   Added selected class to node');
            } else {
                console.log('[WebView]   WARNING: Target node not found');
            }
            
            // Store both current behavior and behavior_needed
            const behavior = window.currentBehavior || options.behavior || null;
            const behaviors = options.behaviors || (options.behavior ? [options.behavior] : []);
            
            window.selectedNode = {
                type: type,
                name: name,
                path: options.path || null,
                behavior: behavior, // Current behavior in progress
                behaviorNeeded: options.behavior || null, // Required next behavior from story graph
                behaviorsNeeded: behaviors, // List of applicable behaviors (may have multiple for empty nodes)
                canHaveSubEpic: options.canHaveSubEpic || false,
                canHaveStory: options.canHaveStory || false,
                canHaveTests: options.canHaveTests || false,
                hasChildren: options.hasChildren || false,
                hasStories: options.hasStories || false,
                hasNestedSubEpics: options.hasNestedSubEpics || false
            };
            console.log('[WebView]   window.selectedNode updated:', JSON.stringify(window.selectedNode, null, 2));
            console.log('');
            console.log('[NODE CLICK DEBUG] ═══════════════════════════════════════');
            console.log('[NODE CLICK DEBUG] Node clicked:', name);
            console.log('[NODE CLICK DEBUG] Node type:', type);
            console.log('[NODE CLICK DEBUG] Current behavior from bot:', window.currentBehavior || '(none)');
            console.log('[NODE CLICK DEBUG] behavior_needed from node:', options.behavior || '(none)');
            console.log('[NODE CLICK DEBUG] Using behavior:', behavior || '(none)');
            if (!behavior) {
                console.log('[NODE CLICK DEBUG] ⚠️ WARNING: No current behavior - submit button will not show');
            }
            console.log('[NODE CLICK DEBUG] ═══════════════════════════════════════');
            console.log('');
            
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] window.selectedNode.behavior_needed set to: "' + window.selectedNode.behavior + '" for node: ' + name
            });
            
            // Save selection to sessionStorage
            try {
                sessionStorage.setItem('selectedNode', JSON.stringify(window.selectedNode));
            } catch (err) {
                console.error('[WebView] Error saving selection:', err);
            }
            
            window.updateContextualButtons();
            console.log('[WebView]   updateContextualButtons called');
            console.log('═══════════════════════════════════════════════════════');
        };
        
        // Handle contextual create actions
        window.handleContextualCreate = function(actionType) {
            console.log('═══════════════════════════════════════════════════════');
            console.log('[WebView] handleContextualCreate CALLED');
            console.log('[WebView]   actionType:', actionType);
            console.log('[WebView]   window.selectedNode:', JSON.stringify(window.selectedNode, null, 2));
            
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] handleContextualCreate: ' + actionType + ' | selectedNode: ' + JSON.stringify(window.selectedNode)
            });
            
            if (!window.selectedNode.name) {
                console.error('[WebView] ERROR: No node name for contextual create');
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] ERROR: No node name for contextual create'
                });
                return;
            }
            
            // Validate path: must contain node name, not just "story_graph."
            const hasValidPath = window.selectedNode.path && 
                                window.selectedNode.path.length > 'story_graph.'.length &&
                                window.selectedNode.path.includes(window.selectedNode.name);
            
            console.log('[WebView]   path:', window.selectedNode.path);
            console.log('[WebView]   hasValidPath:', hasValidPath);
            
            // Use optimistic update handler from story_map_view.js if available
            if (typeof window.handleCreateNode === 'function') {
                var parentPath = hasValidPath ? window.selectedNode.path : \`story_graph."\${window.selectedNode.name}"\`;
                
                console.log('[WebView] Using optimistic create handler for:', actionType);
                window.handleCreateNode({
                    parentPath: parentPath,
                    nodeType: actionType
                    // placeholderName will be auto-generated (Epic1, SubEpic1, Story1, etc.)
                });
            } else {
                console.warn('[WebView] handleCreateNode not available, falling back to direct command');
                // Fallback: send command directly
                let commandText;
                switch(actionType) {
                    case 'sub-epic':
                        commandText = hasValidPath ? \`\${window.selectedNode.path}.create\` : \`story_graph."\${window.selectedNode.name}".create\`;
                        break;
                    case 'story':
                        commandText = hasValidPath ? \`\${window.selectedNode.path}.create_story\` : \`story_graph."\${window.selectedNode.name}".create_story\`;
                        break;
                    case 'scenario':
                        commandText = hasValidPath ? \`\${window.selectedNode.path}.create_scenario\` : \`story_graph."\${window.selectedNode.name}".create_scenario\`;
                        break;
                    case 'acceptance-criteria':
                        commandText = hasValidPath ? \`\${window.selectedNode.path}.create_acceptance_criteria\` : \`story_graph."\${window.selectedNode.name}".create_acceptance_criteria\`;
                        break;
                }
                
                if (commandText) {
                    vscode.postMessage({
                        command: 'executeCommand',
                        commandText: commandText,
                        optimistic: true
                    });
                } else {
                    console.error('[WebView] ERROR: No commandText generated');
                }
            }
            console.log('═══════════════════════════════════════════════════════');
        };
        
        // Handle delete action (always cascade)
        window.handleDelete = function() {
            console.log('[WebView] handleDelete called for node:', window.selectedNode);
            
            if (!window.selectedNode || !window.selectedNode.name) {
                console.error('[WebView] ERROR: No node selected for delete');
                return;
            }
            
            // Build node path
            let nodePath = window.selectedNode.path;
            if (!nodePath || nodePath.length <= 'story_graph.'.length) {
                // Fallback: construct path from name
                nodePath = \`story_graph."\${window.selectedNode.name}"\`;
            }
            
            console.log('[WebView] Calling handleDeleteNode with path:', nodePath);
            
            // Call handleDeleteNode for optimistic update (removes from DOM immediately)
            // Delete ALWAYS includes children - no version without children
            if (typeof window.handleDeleteNode === 'function') {
                window.handleDeleteNode({
                    nodePath: nodePath
                });
            } else {
                console.warn('[WebView] handleDeleteNode not available, falling back to direct command');
                // Fallback: send command directly (will still work, but no optimistic update)
                // Backend delete() method defaults to cascade=True (always includes children)
                const commandText = nodePath + '.delete()';
                vscode.postMessage({
                    command: 'executeCommand',
                    commandText: commandText
                });
            }
        };
        
        // Handle scope to action - set filter to selected node
        window.handleScopeTo = function() {
            console.log('[WebView] handleScopeTo called for node:', window.selectedNode);
            
            if (!window.selectedNode.name) {
                console.error('[WebView] ERROR: No node selected for scope');
                return;
            }
            
            // Build scope command with node type prefix (matches nodes.py _scope_command_for_node)
            const nodeName = window.selectedNode.name;
            const nodeType = window.selectedNode.type;
            let scopeCommand;
            
            if (nodeType === 'story') {
                scopeCommand = 'story ' + nodeName;
            } else if (nodeType === 'sub-epic') {
                scopeCommand = 'subepic ' + nodeName;
            } else if (nodeType === 'epic') {
                scopeCommand = 'epic ' + nodeName;
            } else {
                // Fallback to just the name for unknown types
                scopeCommand = nodeName;
            }
            
            console.log('[WebView] Scope To command:', scopeCommand);
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] SENDING SCOPE TO COMMAND: scope ' + scopeCommand
            });
            
            // Execute scope command with the node type and name
            vscode.postMessage({
                command: 'executeCommand',
                commandText: 'scope ' + scopeCommand
            });
        };
        
        window.handleSubmit = function() {
            console.log('[WebView] ========== handleSubmit CALLED ==========');
            console.log('[WebView] handleSubmit called for node:', window.selectedNode);
            console.log('[WebView] Node name:', window.selectedNode?.name);
            console.log('[WebView] Node path:', window.selectedNode?.path);
            console.log('[WebView] Node behavior:', window.selectedNode?.behavior);
            
            if (!window.selectedNode || !window.selectedNode.name) {
                console.error('[WebView] ERROR: No node selected for submit');
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] ERROR: handleSubmit called but no node selected'
                });
                return;
            }
            
            if (!window.selectedNode.behaviorNeeded) {
                console.error('[WebView] ERROR: No behaviorNeeded for selected node');
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] ERROR: handleSubmit called but node has no behaviorNeeded: ' + window.selectedNode.name
                });
                return;
            }
            
            const nodeName = window.selectedNode.name;
            const nodePath = window.selectedNode.path;
            
            console.log('[WebView] Submit: Submitting required behavior instructions for', nodeName);
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] SUBMIT: Submitting required behavior instructions for node=' + nodeName + ', path=' + nodePath
            });
            
            // Call submit_required_behavior_instructions with the build action
            const action = 'build';
            const commandText = nodePath 
                ? nodePath + '.submit_required_behavior_instructions action:"' + action + '"'
                : 'story_graph."' + nodeName + '".submit_required_behavior_instructions action:"' + action + '"';
            
            console.log('[WebView] ========== SENDING COMMAND ==========');
            console.log('[WebView] Executing command:', commandText);
            console.log('[WebView] Command type:', typeof commandText);
            console.log('[WebView] Command length:', commandText.length);
            
            vscode.postMessage({
                command: 'executeCommand',
                commandText: commandText
            });
            
            console.log('[WebView] ========== COMMAND SENT ==========');
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] SUBMIT: Command sent: ' + commandText
            });
        };
        
        window.handleSubmitAlt = function() {
            console.log('[WebView] ========== handleSubmitAlt CALLED ==========');
            console.log('[WebView] handleSubmitAlt called for node:', window.selectedNode);
            
            if (!window.selectedNode || !window.selectedNode.name) {
                console.error('[WebView] ERROR: No node selected for submit alt');
                return;
            }
            
            const behaviorsNeeded = window.selectedNode.behaviorsNeeded || [];
            if (behaviorsNeeded.length < 2) {
                console.error('[WebView] ERROR: No alternate behavior available');
                return;
            }
            
            const altBehavior = behaviorsNeeded[1]; // Second behavior option
            const nodeName = window.selectedNode.name;
            const nodePath = window.selectedNode.path;
            
            console.log('[WebView] Submit Alt: Submitting', altBehavior, 'behavior instructions for', nodeName);
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] SUBMIT ALT: Submitting ' + altBehavior + ' behavior instructions for node=' + nodeName
            });
            
            // Navigate to the alt behavior first, then submit
            const action = 'build';
            const commandText = nodePath 
                ? nodePath + '.submit_instructions behavior:"' + altBehavior + '" action:"' + action + '"'
                : 'story_graph."' + nodeName + '".submit_instructions behavior:"' + altBehavior + '" action:"' + action + '"';
            
            console.log('[WebView] Executing command:', commandText);
            vscode.postMessage({
                command: 'executeCommand',
                commandText: commandText
            });
        };
        
        window.handleSubmitCurrent = function() {
            console.log('[WebView] ========== handleSubmitCurrent CALLED ==========');
            console.log('[WebView] handleSubmitCurrent called for node:', window.selectedNode);
            
            if (!window.selectedNode || !window.selectedNode.name) {
                console.error('[WebView] ERROR: No node selected for submit');
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] ERROR: handleSubmitCurrent called but no node selected'
                });
                return;
            }
            
            const nodeName = window.selectedNode.name;
            const nodePath = window.selectedNode.path;
            
            console.log('[WebView] Submit Current: Submitting current instructions for', nodeName);
            console.log('[WebView] Submit Current: nodeName =', nodeName);
            console.log('[WebView] Submit Current: nodePath =', nodePath);
            console.log('[WebView] Submit Current: nodePath exists?', !!nodePath);
            
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] SUBMIT CURRENT: node=' + nodeName + ', path=' + nodePath + ', pathExists=' + !!nodePath
            });
            
            // Call submit_current_instructions which uses current behavior and action
            const commandText = nodePath 
                ? nodePath + '.submit_current_instructions'
                : 'story_graph."' + nodeName + '".submit_current_instructions';
            
            console.log('[WebView] ========== SUBMIT CURRENT COMMAND ==========');
            console.log('[WebView] Command constructed:', commandText);
            console.log('[WebView] Command length:', commandText.length);
            
            vscode.postMessage({
                command: 'executeCommand',
                commandText: commandText
            });
            
            console.log('[WebView] ========== COMMAND SENT ==========');
        };
        
        // Helper function to get file link from selected node DOM element
        function getSelectedNodeFileLink() {
            if (!window.selectedNode || !window.selectedNode.name) return null;
            const nodeElement = document.querySelector('.story-node[data-node-type="' + window.selectedNode.type + '"][data-node-name="' + window.selectedNode.name + '"]');
            return nodeElement ? nodeElement.getAttribute('data-file-link') : null;
        }
        
        // Helper function to get workspace directory
        function getWorkspaceDir() {
            // Try to get from botData if available
            if (window.botData && window.botData.workspace_directory) {
                return window.botData.workspace_directory;
            }
            // Fallback: try to infer from story graph path
            const storyGraphPath = 'docs/story/story-graph.json';
            return ''; // Will be resolved relative to workspace root
        }
        
        // Helper function to open file in specific view column (for split editors)
        function openFileInColumn(filePath, viewColumn) {
            vscode.postMessage({
                command: 'openFileInColumn',
                filePath: filePath,
                viewColumn: viewColumn // 'One', 'Two', 'Three', 'Four', 'Beside', 'Active'
            });
        }
        
        window.handleOpenGraph = function() {
            console.log('[WebView] handleOpenGraph called');
            console.log('[WebView] selectedNode:', window.selectedNode);
            
            if (!window.selectedNode) {
                console.error('[WebView] No node selected');
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] ERROR: handleOpenGraph called but no node selected'
                });
                return;
            }
            
            const workspaceDir = getWorkspaceDir();
            const storyGraphPath = workspaceDir ? workspaceDir + '/docs/story/story-graph.json' : 'docs/story/story-graph.json';
            
            console.log('[WebView] Opening story graph:', storyGraphPath);
            console.log('[WebView] Node path:', window.selectedNode.path);
            
            // Open story graph and request to collapse all, expand selected node path, position cursor
            vscode.postMessage({
                command: 'openFileWithState',
                filePath: storyGraphPath,
                state: {
                    collapseAll: true,
                    expandPath: window.selectedNode.path || null,
                    selectedNode: window.selectedNode,
                    positionCursor: true // Request cursor positioning at expanded section
                }
            });
        };
        
        window.handleOpenStories = function() {
            console.log('[WebView] handleOpenStories called');
            const fileLink = getSelectedNodeFileLink();
            
            if (!window.selectedNode || !window.selectedNode.name) {
                console.error('[WebView] No node selected');
                return;
            }
            
            // Request story files for selected node
            vscode.postMessage({
                command: 'openStoryFiles',
                nodeType: window.selectedNode.type,
                nodeName: window.selectedNode.name,
                nodePath: window.selectedNode.path,
                singleFileLink: fileLink
            });
        };
        
        window.handleOpenAll = function() {
            console.log('[WebView] handleOpenAll called');
            
            if (!window.selectedNode || !window.selectedNode.name) {
                console.error('[WebView] No node selected');
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] ERROR: handleOpenAll called but no node selected'
                });
                return;
            }
            
            const fileLink = getSelectedNodeFileLink();
            const workspaceDir = getWorkspaceDir();
            const storyGraphPath = workspaceDir ? workspaceDir + '/docs/story/story-graph.json' : 'docs/story/story-graph.json';
            
            // Find the selected node element in DOM by iterating (querySelector fails with quoted paths)
            let testFiles = [];
            let storyFiles = [];
            const selectedNodePath = window.selectedNode.path;
            const nodeType = window.selectedNode.type;
            
            if (selectedNodePath) {
                const allNodes = document.querySelectorAll('.story-node[data-path]');
                let nodeEl = null;
                for (const el of allNodes) {
                    if (el.getAttribute('data-path') === selectedNodePath) {
                        nodeEl = el;
                        break;
                    }
                }
                
                if (nodeEl) {
                    if (nodeType === 'sub-epic' || nodeType === 'epic') {
                        // For sub-epics/epics: collect story files and test files from ALL child stories
                        // The collapsible content div is a sibling of the node's parent div
                        const parentDiv = nodeEl.closest('div');
                        const collapsibleDiv = parentDiv ? parentDiv.nextElementSibling : null;
                        
                        if (collapsibleDiv && collapsibleDiv.classList.contains('collapsible-content')) {
                            // Collect all story file links from child story nodes
                            const childStoryNodes = collapsibleDiv.querySelectorAll('.story-node[data-node-type="story"]');
                            childStoryNodes.forEach(function(storyEl) {
                                const link = storyEl.getAttribute('data-file-link');
                                if (link) {
                                    storyFiles.push(link);
                                }
                            });
                            
                            // Collect all test files from child elements
                            const testFileEls = collapsibleDiv.querySelectorAll('[data-test-files]');
                            testFileEls.forEach(function(el) {
                                try {
                                    var files = JSON.parse(el.getAttribute('data-test-files'));
                                    if (Array.isArray(files)) {
                                        files.forEach(function(f) {
                                            if (testFiles.indexOf(f) === -1) testFiles.push(f);
                                        });
                                    }
                                } catch (e) {
                                    console.error('[WebView] Error parsing child test_files:', e);
                                }
                            });
                        }
                        console.log('[WebView] Sub-epic/epic: found', storyFiles.length, 'story files and', testFiles.length, 'test files');
                    } else {
                        // For stories/scenarios: get test files from sibling element
                        if (nodeEl.parentElement) {
                            const testFilesEl = nodeEl.parentElement.querySelector('[data-test-files]');
                            if (testFilesEl) {
                                try {
                                    testFiles = JSON.parse(testFilesEl.getAttribute('data-test-files'));
                                    console.log('[WebView] Found test_files from DOM:', testFiles);
                                } catch (e) {
                                    console.error('[WebView] Error parsing test_files:', e);
                                }
                            }
                        }
                    }
                }
            }
            
            console.log('[WebView] handleOpenAll - selectedNode:', JSON.stringify(window.selectedNode));
            console.log('[WebView] handleOpenAll - fileLink:', fileLink);
            console.log('[WebView] handleOpenAll - storyFiles:', storyFiles);
            console.log('[WebView] handleOpenAll - testFiles:', testFiles);
            
            // Open all files in split editors
            vscode.postMessage({
                command: 'openAllRelatedFiles',
                nodeType: window.selectedNode.type,
                nodeName: window.selectedNode.name,
                nodePath: window.selectedNode.path,
                singleFileLink: fileLink,
                storyFiles: storyFiles,
                testFiles: testFiles,
                storyGraphPath: storyGraphPath,
                selectedNode: window.selectedNode  // Pass full node for story graph positioning
            });
        };
        
        
        // Initialize: show Create Epic button by default
        setTimeout(function() {
            window.selectNode('root', null);
        }, 100);
        
        // Escape key deselects the current node and resets buttons
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                // Clear session storage so refresh doesn't restore
                try { sessionStorage.removeItem('selectedNode'); } catch(err) {}
                window.diagramScope = '';
                window.selectNode('root', null);
            }
        });
        
        // Toggle Q&A expand/collapse
        window.toggleQAExpand = function(idx) {
            const textarea = document.getElementById('clarify-answer-' + idx);
            const toggleBtn = document.getElementById('qa-toggle-' + idx);
            if (!textarea) return;
            
            const isCollapsed = textarea.getAttribute('data-collapsed') === 'true';
            const defaultHeight = 60; // Default collapsed height in px
            
            if (isCollapsed) {
                // Expand to full content
                textarea.style.height = 'auto';
                const fullHeight = textarea.scrollHeight;
                textarea.style.height = fullHeight + 'px';
                textarea.style.overflow = 'visible';
                textarea.setAttribute('data-collapsed', 'false');
                if (toggleBtn) toggleBtn.textContent = '▲';
            } else {
                // Collapse to default height
                textarea.style.height = defaultHeight + 'px';
                textarea.style.overflow = 'hidden';
                textarea.setAttribute('data-collapsed', 'true');
                if (toggleBtn) toggleBtn.textContent = '▼';
            }
        };
        
        // Save functions for guardrails
        window.saveClarifyAnswers = function() {
            console.log('[WebView] saveClarifyAnswers triggered');
            const answers = {};
            const answerElements = document.querySelectorAll('[id^="clarify-answer-"]');
            
            answerElements.forEach((textarea) => {
                const question = textarea.getAttribute('data-question');
                const answer = textarea.value?.trim();
                if (question && answer) {
                    answers[question] = answer;
                }
            });
            
            if (Object.keys(answers).length > 0) {
                console.log('[WebView] Saving clarify answers:', answers);
                vscode.postMessage({
                    command: 'saveClarifyAnswers',
                    answers: answers
                });
            }
        };
        
        window.saveClarifyEvidence = function() {
            console.log('[WebView] saveClarifyEvidence triggered');
            const evidenceTextarea = document.getElementById('clarify-evidence');
            if (evidenceTextarea) {
                const evidenceText = evidenceTextarea.value?.trim();
                if (evidenceText) {
                    // Parse evidence text as key:value pairs
                    const evidenceProvided = {};
                    evidenceText.split('\\n').forEach(line => {
                        const colonIdx = line.indexOf(':');
                        if (colonIdx > 0) {
                            const key = line.substring(0, colonIdx).trim();
                            const value = line.substring(colonIdx + 1).trim();
                            if (key && value) {
                                evidenceProvided[key] = value;
                            }
                        }
                    });
                    
                    if (Object.keys(evidenceProvided).length > 0) {
                        console.log('[WebView] Saving clarify evidence:', evidenceProvided);
                        vscode.postMessage({
                            command: 'saveClarifyEvidence',
                            evidence_provided: evidenceProvided
                        });
                    }
                }
            }
        };
        
        window.saveStrategyDecision = function(criteriaKey, selectedOption) {
            console.log('[WebView] saveStrategyDecision triggered:', criteriaKey, selectedOption);
            vscode.postMessage({
                command: 'saveStrategyDecision',
                criteriaKey: criteriaKey,
                selectedOption: selectedOption
            });
        };
        
        // Multi-select version: collects all checked checkboxes with given name
        window.saveStrategyMultiDecision = function(criteriaKey, inputName) {
            console.log('[WebView] saveStrategyMultiDecision triggered:', criteriaKey, inputName);
            const checkboxes = document.querySelectorAll('input[name="' + inputName + '"]:checked');
            const selectedOptions = [];
            checkboxes.forEach(cb => {
                // Get the option text from the label's span
                const label = cb.closest('label');
                if (label) {
                    const span = label.querySelector('span');
                    if (span) {
                        selectedOptions.push(span.textContent);
                    }
                }
            });
            console.log('[WebView] Saving multi-select decision:', criteriaKey, selectedOptions);
            vscode.postMessage({
                command: 'saveStrategyMultiDecision',
                criteriaKey: criteriaKey,
                selectedOptions: selectedOptions
            });
        };
        
        window.saveStrategyAssumptions = function() {
            console.log('[WebView] saveStrategyAssumptions triggered');
            const assumptionsTextarea = document.getElementById('strategy-assumptions');
            if (assumptionsTextarea) {
                const assumptionsText = assumptionsTextarea.value?.trim();
                if (assumptionsText) {
                    const assumptions = assumptionsText.split('\\n').filter(a => a.trim());
                    console.log('[WebView] Saving strategy assumptions:', assumptions);
                    vscode.postMessage({
                        command: 'saveStrategyAssumptions',
                        assumptions: assumptions
                    });
                }
            }
        };
        
        // Listen for messages from extension host (e.g. error displays)
        // Listen for messages from extension host (e.g. error displays)
        window.addEventListener('message', event => {
            const message = event.data;
            console.log('[WebView] Received message from extension:', message);
            
            if (message.command === 'saveCompleted') {
                console.log('[ASYNC_SAVE] [WEBVIEW] [STEP 10] Received saveCompleted message from extension host success=' + message.success + ' error=' + (message.error || 'none') + ' timestamp=' + new Date().toISOString());
                if (message.success) {
                    console.log('[ASYNC_SAVE] [WEBVIEW] [STEP 10] Processing success response');
                    showSaveSuccess();
                } else {
                    console.log('[ASYNC_SAVE] [WEBVIEW] [STEP 10] Processing error response error=' + (message.error || 'Unknown error'));
                    showSaveError(message.error || 'Unknown error');
                }
                console.log('[ASYNC_SAVE] [WEBVIEW] ========== SAVE FLOW COMPLETE ==========');
                return;
            }
            
            if (message.command === 'optimisticRename') {
                console.log('[WebView] Received optimisticRename message:', message);
                // Use optimistic update handler from story_map_view.js if available
                if (typeof window.handleRenameNode === 'function') {
                    console.log('[WebView] Using optimistic rename handler');
                    window.handleRenameNode({
                        nodePath: message.nodePath,
                        oldName: message.oldName,
                        newName: message.newName
                    });
                } else {
                    console.warn('[WebView] handleRenameNode not available');
                }
                return;
            }
            
            if (message.command === 'setWorkspacePath') {
                console.log('[WebView] Received setWorkspacePath message:', message.path);
                const input = document.getElementById('workspacePathInput');
                if (input) {
                    input.value = message.path;
                }
                return;
            }
            
            if (message.command === 'expandInstructionsSection') {
                console.log('[WebView] Received expandInstructionsSection message:', message.actionName);
                try {
                    if (message.actionName && typeof window.expandInstructionsSection === 'function') {
                        window.expandInstructionsSection(message.actionName);
                    }
                } catch (err) {
                    console.error('[WebView] Error in expandInstructionsSection handler:', err);
                }
                return;
            }
            
            if (message.command === 'diagramFileChanged') {
                var ds = document.getElementById('diagram-section');
                if (ds && message.diagram) {
                    var d = message.diagram;
                    var isStale = d.file_modified_time && d.last_sync_time && d.file_modified_time > d.last_sync_time;
                    var neverSynced = !d.last_sync_time;
                    var needsAction = isStale || neverSynced;
                    var staleEl = ds.querySelector('.stale-indicator');
                    var linkParent = ds.querySelector('.diagram-link');
                    if (linkParent) { linkParent = linkParent.parentElement; }
                    if (needsAction && !staleEl && linkParent) {
                        var ind = document.createElement('span');
                        ind.className = 'stale-indicator';
                        ind.style.cssText = 'color: var(--vscode-editorWarning-foreground); margin-left: 8px;';
                        ind.textContent = 'Diagram Changes Not In Graph';
                        linkParent.appendChild(ind);
                    }
                    if (needsAction && !ds.querySelector('.generate-report-button')) {
                        var btnDiv = ds.querySelector('.diagram-item');
                        if (btnDiv) { btnDiv = btnDiv.lastElementChild; }
                        if (btnDiv) {
                            var genBtn = document.createElement('button');
                            genBtn.className = 'generate-report-button';
                            genBtn.textContent = 'Generate Report';
                            genBtn.style.cssText = 'margin: 4px 4px 4px 0; cursor: pointer;';
                            genBtn.onclick = function() { vscode.postMessage({ command: 'generateDiagramReport', path: d.file_path }); };
                            btnDiv.appendChild(genBtn);
                        }
                    }
                }
                return;
            }
            
            if (message.command === 'displayError') {
                // Display error prominently in the panel
                const errorDiv = document.createElement('div');
                errorDiv.style.cssText = 'position: fixed; top: 10px; left: 10px; right: 10px; z-index: 10000; background: #f44336; color: white; padding: 16px; border-radius: 4px; font-family: monospace; font-size: 12px; white-space: pre-wrap; max-height: 80vh; overflow-y: auto;';
                errorDiv.textContent = '[ERROR] ' + message.error;
                
                // Add button container
                const btnContainer = document.createElement('div');
                btnContainer.style.cssText = 'margin-top: 12px; display: flex; gap: 8px;';
                
                // Add retry button
                const retryBtn = document.createElement('button');
                retryBtn.textContent = '🔄 Retry';
                retryBtn.style.cssText = 'background: white; color: #f44336; border: none; padding: 8px 16px; cursor: pointer; border-radius: 3px; font-weight: bold;';
                retryBtn.onclick = () => {
                    errorDiv.remove();
                    vscode.postMessage({ command: 'refresh' });
                };
                
                // Add close button
                const closeBtn = document.createElement('button');
                closeBtn.textContent = 'Close';
                closeBtn.style.cssText = 'background: rgba(255,255,255,0.8); color: #f44336; border: none; padding: 8px 16px; cursor: pointer; border-radius: 3px;';
                closeBtn.onclick = () => errorDiv.remove();
                
                btnContainer.appendChild(retryBtn);
                btnContainer.appendChild(closeBtn);
                errorDiv.appendChild(btnContainer);
                
                document.body.appendChild(errorDiv);
                
                // Auto-remove after 30 seconds
                setTimeout(() => errorDiv.remove(), 30000);
            }
            
            // Handle explicit collapse state restoration after refresh
            if (message.command === 'restoreCollapseState') {
                console.log('[WebView] Restoring collapse state after refresh');
                const savedState = sessionStorage.getItem('collapseState');
                if (savedState) {
                    try {
                        const state = JSON.parse(savedState);
                        window.restoreCollapseState(state);
                        console.log('[WebView] Restored collapse state for', Object.keys(state).length, 'sections');
                    } catch (err) {
                        console.error('[WebView] Failed to restore collapse state:', err);
                    }
                } else {
                    console.log('[WebView] No saved collapse state found');
                }
            }
            
            // Optimistic update disabled - full refresh preserves icons and structure
            // (textContent wiped out icon HTML, causing icons to disappear)
            if (message.command === 'optimisticRename') {
                console.log('[WebView] Optimistic rename disabled - waiting for full refresh');
                // Panel will refresh after backend rename completes
            }
            
            // Revert rename disabled - no longer needed without optimistic updates
            if (message.command === 'revertRename') {
                console.log('[WebView] Revert rename command received but not needed');
            }
        });
    </script>
</body>
</html>`;
  }
}

// Static properties (assigned after class definition for compatibility)
BotPanel.currentPanel = undefined;
BotPanel.viewType = "agilebot.botPanel";

module.exports = BotPanel;
