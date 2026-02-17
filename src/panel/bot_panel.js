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
const { escapeForHtml, log } = require("./utils");

class BotPanel {
  constructor(panel, workspaceRoot, extensionUri) {
    // ===== PERFORMANCE: Start constructor timing =====
    const perfConstructorStart = performance.now();
    try {
      this._log = log;
      
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
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_panel.js:19',message:'Constructor ENTRY',data:{workspaceRoot,hasPanel:!!panel,hasExtensionUri:!!extensionUri},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'B,D'})}).catch(()=>{});
      // #endregion
      console.log(`[BotPanel] Constructor called - workspaceRoot: ${workspaceRoot}`);
      this._panel = panel;
      this._workspaceRoot = workspaceRoot;
      this._extensionUri = extensionUri;
      this._disposables = [];
      this._expansionState = {};
      this._currentStoryMapView = 'Hierarchy'; // 'Hierarchy' or 'Increment'
      
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
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_panel.js:43',message:'Before PanelView creation',data:{workspaceRoot,botDirectory},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'D'})}).catch(()=>{});
      // #endregion
      this._sharedCLI = new PanelView(botDirectory);
      const perfPanelViewEnd = performance.now();
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_panel.js:43',message:'After PanelView creation',data:{},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'D'})}).catch(()=>{});
      // #endregion
      console.log("[BotPanel] Shared PanelView instance created successfully");
      this._log(`[PERF] PanelView creation: ${(perfPanelViewEnd - perfPanelViewStart).toFixed(2)}ms`);
      
      // Initialize BotView (uses shared CLI)
      this._botView = null;
      
      // Set initial loading HTML
      console.log("[BotPanel] Setting initial loading HTML");
      this._panel.webview.html = this._getWebviewContent('<div style="padding: 20px;">Loading bot panel...</div>');
      
      // Update content asynchronously (can't await in constructor)
      console.log("[BotPanel] Calling _update()");
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_panel.js:55',message:'Before _update()',data:{},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'E'})}).catch(()=>{});
      // #endregion
      this._update().catch(err => {
        console.error(`[BotPanel] ERROR in async _update: ${err.message}`);
        console.error(`[BotPanel] ERROR stack: ${err.stack}`);
        vscode.window.showErrorMessage(`Bot Panel Error: ${err.message}`);
        // #region agent log
        fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_panel.js:55',message:'_update() threw error',data:{error:err.message,stack:err.stack},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'E'})}).catch(()=>{});
        // #endregion
      });
      
      // ===== PERFORMANCE: End constructor timing =====
      const perfConstructorEnd = performance.now();
      const constructorDuration = (perfConstructorEnd - perfConstructorStart).toFixed(2);
      console.log("[BotPanel] Constructor completed successfully");
      this._log(`[PERF] TOTAL Constructor duration: ${constructorDuration}ms`);
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_panel.js:60',message:'Constructor EXIT',data:{constructorDurationMs:constructorDuration},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'B'})}).catch(()=>{});
      // #endregion
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
            // Toggle between Hierarchy and Increment views
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
                const rawPath = filePath.split('#')[0];
                const fragment = filePath.includes('#') ? filePath.split('#')[1] : null;
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
                const fileUri = vscode.Uri.file(absolutePath);
                const fs = require('fs');
                if (!fs.existsSync(absolutePath) || fs.statSync(absolutePath).isDirectory()) continue;
                const fileExtension = rawPath.split('.').pop().toLowerCase();
                const useVscodeOpenExtensions = ['json'];
                if (useVscodeOpenExtensions.includes(fileExtension)) {
                  vscode.commands.executeCommand('vscode.open', fileUri).catch(() => {});
                } else {
                  const openOptions = { viewColumn: vscode.ViewColumn.One, preserveFocus: false, preview: false };
                  if (lineNumber) {
                    openOptions.selection = new vscode.Range(lineNumber - 1, 0, lineNumber - 1, 0);
                  }
                  vscode.window.showTextDocument(fileUri, openOptions).catch(() => {});
                }
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
              
              // Use vscode.open for JSON files to avoid VS Code's 15MB text editor bug
              // But if we have a selectedNode, we need to search and select it
              const fileExtension = cleanPath.split('.').pop().toLowerCase();
              if (fileExtension === 'json' && message.state && message.state.selectedNode) {
                // JSON with selectedNode - need to search document for node
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
                      this._log(`[BotPanel] JSON file opened with state: selectedNode=${node.name}`);
                    });
                  }
                ).catch((error) => {
                  vscode.window.showErrorMessage(`Failed to open file: ${message.filePath}\n${error.message}`);
                });
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
              const scopeCmd = `scope "${filterValue}"`;
              this._log('[BotPanel] Executing scope command: ' + scopeCmd);
              
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
    // #region agent log
    fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_panel.js:262',message:'createOrShow ENTRY',data:{workspaceRoot,extensionUri:extensionUri?.toString()},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'B'})}).catch(()=>{});
    // #endregion
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
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_panel.js:294',message:'Before new BotPanel()',data:{hasPanel:!!panel},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'B'})}).catch(()=>{});
      // #endregion
      BotPanel.currentPanel = new BotPanel(panel, workspaceRoot, extensionUri);
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_panel.js:294',message:'After new BotPanel()',data:{instanceCreated:!!BotPanel.currentPanel},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'B'})}).catch(()=>{});
      // #endregion
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
        // Open test files with scope expanded
        // Query story graph for test_file and test_class
        this._log(`[BotPanel] Opening test files for ${nodeType} "${nodeName}"`);
        
        try {
          const result = await this._botView.execute(`story_graph.${nodePath || `"${nodeName}"`}.openTest()`);
          if (result && result.files && Array.isArray(result.files)) {
            // Open each test file with scope information
            for (const testFileInfo of result.files) {
              const testFilePath = testFileInfo.file;
              const absolutePath = path.isAbsolute(testFilePath)
                ? testFilePath
                : path.join(workspaceRoot, testFilePath);
              
              const fileUri = vscode.Uri.file(absolutePath);
              
              // Use vscode.open for JSON files to avoid VS Code's 15MB text editor bug
              const fileExtension = testFilePath.split('.').pop().toLowerCase();
              if (fileExtension === 'json') {
                await vscode.commands.executeCommand('vscode.open', fileUri);
              } else {
                const doc = await vscode.workspace.openTextDocument(fileUri);
              
                // Open in Column One
                await vscode.window.showTextDocument(doc, {
                  viewColumn: vscode.ViewColumn.One,
                  preserveFocus: false
                });
              }
              
              // TODO: Implement fold/unfold logic to expand test_class/test_method and collapse others
              // This would require using VS Code's folding API or commands
            }
            this._log(`[BotPanel] Opened ${result.files.length} test files`);
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
        
        // 4. Activate the story graph tab as the last step
        const graphAbsPath = path.isAbsolute(graphPath) ? graphPath : path.join(workspaceRoot, graphPath);
        const graphUri = vscode.Uri.file(graphAbsPath);
        try {
          const graphDoc = await vscode.workspace.openTextDocument(graphUri);
          await vscode.window.showTextDocument(graphDoc, { viewColumn: vscode.ViewColumn.One, preview: false, preserveFocus: false });
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
    const fileUri = vscode.Uri.file(absolutePath);
    
    if (!selectedNode || !selectedNode.name) {
      // No node to select, just open the file
      await vscode.commands.executeCommand('vscode.open', fileUri);
      return;
    }
    
    // Open and search for node
    const doc = await vscode.workspace.openTextDocument(fileUri);
    const text = doc.getText();
    const lines = text.split('\n');
    
    // Find the line with "name": "NodeName"
    let nameLineIndex = -1;
    const escapedName = selectedNode.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const namePattern = new RegExp(`"name"\\s*:\\s*"${escapedName}"`);
    
    for (let i = 0; i < lines.length; i++) {
      if (namePattern.test(lines[i])) {
        nameLineIndex = i;
        break;
      }
    }
    
    let options = { viewColumn: vscode.ViewColumn.One, preview: false, preserveFocus: false };
    
    if (nameLineIndex >= 0) {
      // Find the opening brace of this object
      let startLine = nameLineIndex;
      for (let i = nameLineIndex - 1; i >= 0; i--) {
        const line = lines[i].trim();
        if (line === '{' || line.endsWith('{')) {
          startLine = i;
          break;
        }
        if (line.startsWith('}') || line === '},') break;
      }
      
      // Find the matching closing brace
      let braceCount = 0;
      let endLine = nameLineIndex;
      let started = false;
      
      for (let i = startLine; i < lines.length; i++) {
        for (const char of lines[i]) {
          if (char === '{') { braceCount++; started = true; }
          else if (char === '}') {
            braceCount--;
            if (started && braceCount === 0) { endLine = i; break; }
          }
        }
        if (started && braceCount === 0) break;
      }
      
      const endLineLength = lines[endLine] ? lines[endLine].length : 0;
      options.selection = new vscode.Range(startLine, 0, endLine, endLineLength);
    }
    
    await vscode.window.showTextDocument(doc, options);
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
        const cleanPath = testFilePath.split('#')[0];
        const fragment = testFilePath.includes('#') ? testFilePath.split('#')[1] : null;
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
        
        const fileUri = vscode.Uri.file(absolutePath);
        const doc = await vscode.workspace.openTextDocument(fileUri);
        
        const options = {
          viewColumn: vscode.ViewColumn.One,
          preview: false,
          preserveFocus: true
        };
        if (lineNumber) {
          options.selection = new vscode.Range(lineNumber - 1, 0, lineNumber - 1, 0);
        }
        
        await vscode.window.showTextDocument(doc, options);
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

  async _update() {
    // ===== PERFORMANCE: Start overall timing =====
    const perfUpdateStart = performance.now();
    try {
      this._log('[BotPanel] _update() START');
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_panel.js:384',message:'_update() ENTRY',data:{hasBotView:!!this._botView},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'E'})}).catch(()=>{});
      console.log('[BotPanel] Fetching bot status...');
      // #endregion
      console.log("[BotPanel] _update() called");
      const webview = this._panel.webview;
      this._panel.title = "Bot Panel";
      
      // Initialize BotView if needed (uses shared CLI)
      if (!this._botView) {
        // ===== PERFORMANCE: BotView creation =====
        const perfBotViewStart = performance.now();
        console.log("[BotPanel] Creating BotView");
        this._log('[BotPanel] Creating BotView');
        // #region agent log
        fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_panel.js:394',message:'Before new BotView()',data:{panelVersion:this._panelVersion,hasWebview:!!webview,hasExtensionUri:!!this._extensionUri},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'E'})}).catch(()=>{});
        // #endregion
        try {
          this._botView = new BotView(this._sharedCLI, this._panelVersion, webview, this._extensionUri);
          // #region agent log
          fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_panel.js:394',message:'After new BotView()',data:{botViewCreated:!!this._botView},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'E'})}).catch(()=>{});
          // #endregion
          const perfBotViewEnd = performance.now();
          const botViewDuration = (perfBotViewEnd - perfBotViewStart).toFixed(2);
          console.log("[BotPanel] BotView created successfully");
          this._log(`[BotPanel] BotView created successfully in ${botViewDuration}ms`);
          this._log(`[PERF] BotView creation: ${botViewDuration}ms`);
        } catch (botViewError) {
          console.error(`[BotPanel] ERROR creating BotView: ${botViewError.message}`);
          console.error(`[BotPanel] ERROR stack: ${botViewError.stack}`);
          this._log(`[BotPanel] ERROR creating BotView: ${botViewError.message}`);
          // #region agent log
          fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_panel.js:394',message:'BotView construction failed',data:{error:botViewError.message,stack:botViewError.stack},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'E'})}).catch(()=>{});
          // #endregion
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
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_panel.js:405',message:'Before _botView.render()',data:{},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'E'})}).catch(()=>{});
      // #endregion
      // Render HTML using BotView (async now)
      const botData = this._botView.botData || await this._botView.execute('status');
      const currentBehavior = botData?.behaviors?.current_behavior || botData?.current_behavior || null;
      const currentAction = botData?.behaviors?.current_action || botData?.current_action || null;
      const html = this._getWebviewContent(await this._botView.render(), currentBehavior, currentAction, botData);
      const perfRenderEnd = performance.now();
      const renderDuration = (perfRenderEnd - perfRenderStart).toFixed(2);
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_panel.js:405',message:'After _botView.render()',data:{htmlLength:html?.length||0},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'E'})}).catch(()=>{});
      // #endregion
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
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_panel.js:407',message:'_update() EXIT success',data:{totalDurationMs:totalDuration},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'E'})}).catch(()=>{});
      // #endregion
      
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
      const command = err.command ? `Command: ${escapeForHtml(err.command)}` : '';
      
      this._panel.webview.html = this._getWebviewContent(`
        <div style="padding: 20px; color: var(--vscode-errorForeground);">
          <h2>⚠️ Error Loading Bot Panel</h2>
          <div style="background: var(--vscode-inputValidation-errorBackground); border: 1px solid var(--vscode-inputValidation-errorBorder); padding: 15px; margin: 10px 0; border-radius: 4px;">
            <p><strong>Error:</strong> ${escapeForHtml(err.message)}</p>
            ${command ? `<p style="margin-top: 10px;">${command}</p>` : ''}
            ${err.isCliError ? `<p style="margin-top: 10px;"><strong>Type:</strong> ${escapeForHtml(errorType)}</p>` : ''}
          </div>
          <details style="margin-top: 15px;">
            <summary style="cursor: pointer; color: var(--vscode-textLink-foreground);">Show Stack Trace</summary>
            <pre style="background: var(--vscode-editor-background); padding: 10px; margin-top: 10px; border-radius: 4px; overflow-x: auto;">${escapeForHtml(err.stack || 'No stack trace available')}</pre>
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

  // escapeHtml now imported from ./utils

  _getWebviewContent(contentHtml, currentBehavior = null, currentAction = null, botData = null) {

    const clientScriptPath = vscode.Uri.joinPath(this._extensionUri, 'bot', 'bot_panel_client.js');
    let contentScript = fs.readFileSync(clientScriptPath.fsPath, 'utf-8');
    
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

    // replace branding placeholders in css file
    // contentStyles(brandColor, brandColorRgb, bgColor, bgColorRgb, textColor, textColorRgb, textColorFaded, fontWeight, isLightBg)}  
    const stylesPath = vscode.Uri.joinPath(this._extensionUri, 'styles', 'theme.css');
    let contentStyle = fs.readFileSync(stylesPath.fsPath, 'utf-8');
    
    contentStyle = contentStyle.replace(/{{brandColor}}/g, brandColor)
      .replace(/{{brandColorRgb}}/g, brandColorRgb)
      .replace(/{{bgColor}}/g, bgColor)
      .replace(/{{bgColorRgb}}/g, bgColorRgb)
      .replace(/{{textColor}}/g, textColor)
      .replace(/{{textColorRgb}}/g, textColorRgb)
      .replace(/{{textColorFaded}}/g, textColorFaded)
      .replace(/{{fontWeight}}/g, fontWeight)
      .replace(/{{isLightBg}}/g, isLightBg);
    
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
      ${contentStyle}  
    </style>
    ${currentBehaviorScript}
</head>
<body>
    ${contentHtml}    
    <script>
        ${contentScript}
    </script>
</body>
</html>`;
  }
}

// Static properties (assigned after class definition for compatibility)
BotPanel.currentPanel = undefined;
BotPanel.viewType = "agilebot.botPanel";

module.exports = BotPanel;
