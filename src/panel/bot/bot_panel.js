

const vscode = require("vscode");
const path = require("path");
const fs = require("fs");
const BotView = require("./bot_view");
const PanelView = require("../panel_view");
const WorkspaceManager = require("../workspace/workspace_manager");
const BehaviorsManager = require("../behaviors/behaviors_manager");
const StoryGraphManager = require("../story_graph/story_graph_manager");
const branding = require("../branding");
const { escapeForHtml, Logger } = require("../utils");

class BotPanel {
  constructor(panel, repoRoot, extensionUri) {

    const perfConstructorStart = performance.now();
    try {      
      
      this._displayError = (errorMsg) => {
        Logger.log('[BotPanel] Displaying error in webview: ' + errorMsg);
        vscode.window.showErrorMessage('Bot Panel Error: ' + errorMsg);
        if (this._panel && this._panel.webview) {
          this._panel.webview.postMessage({
            command: 'displayError',
            error: errorMsg
          });
        }
      };
      /** Report error to both log and display - never swallow. */
      this._reportError = (err, context = '') => {
        const msg = err?.message || String(err);
        const stack = err?.stack || '';
        const full = context ? `[${context}] ${msg}` : msg;
        Logger.log(`[BotPanel] ERROR: ${full}`);
        if (stack) Logger.log(`[BotPanel] Stack: ${stack}`);
        console.error('[BotPanel]', full, stack);
        vscode.window.showErrorMessage(full);
      };
      
      Logger.log("[BotPanel] Constructor invoked");
      Logger.log(`[PERF] Constructor start`);
      console.log(`[BotPanel] Constructor called - repoRoot: ${repoRoot}`);
      this._panel = panel;
      
      this._repoRoot = repoRoot; // root folder of the repository, we assume it's the first folder in the user's VS Code Workspace
      this._workspaceRoot = repoRoot; // fallback until refresh provides bot workspace_directory
      this._extensionUri = extensionUri;
      this._disposables = [];
      this._expansionState = {};
      this._currentStoryMapView = 'Hierarchy';
      
      // Initialize branding with repo root      
      branding.setRepoRoot(this._repoRoot);
      Logger.log(`[BotPanel] Branding initialized: ${branding.getBranding()}`);
      

      const perfVersionStart = performance.now();
      console.log("[BotPanel] Reading panel version");
      this._panelVersion = this._readPanelVersion();
      const perfVersionEnd = performance.now();
      console.log(`[BotPanel] Panel version: ${this._panelVersion}`);
      Logger.log(`[PERF] Read panel version: ${(perfVersionEnd - perfVersionStart).toFixed(2)}ms`);
      

      let botDirectory = process.env.BOT_DIRECTORY || path.join(this._repoRoot, 'bots', 'story_bot');

      if (!path.isAbsolute(botDirectory)) {
        botDirectory = path.join(this._repoRoot, botDirectory);
      }
      console.log(`[BotPanel] Bot directory: ${botDirectory}`);
      

      const perfPanelViewStart = performance.now();
      console.log("[BotPanel] Creating shared PanelView instance");
      this._sharedCLI = new PanelView(botDirectory);
      const perfPanelViewEnd = performance.now();
      console.log("[BotPanel] Shared PanelView instance created successfully");
      Logger.log(`[PERF] PanelView creation: ${(perfPanelViewEnd - perfPanelViewStart).toFixed(2)}ms`);
      

      this._botView = null;
      

      console.log("[BotPanel] Setting initial loading HTML");
      this._panel.webview.html = this._getWebviewContent('<div style="padding: 20px;">Loading bot panel...</div>');
      

      console.log("[BotPanel] Calling _update()");
      this._update().catch(err => {
        console.error(`[BotPanel] ERROR in async _update: ${err.message}`);
        console.error(`[BotPanel] ERROR stack: ${err.stack}`);
        vscode.window.showErrorMessage(`Bot Panel Error: ${err.message}`);
      });
      

      const perfConstructorEnd = performance.now();
      const constructorDuration = (perfConstructorEnd - perfConstructorStart).toFixed(2);
      console.log("[BotPanel] Constructor completed successfully");
      Logger.log(`[PERF] TOTAL Constructor duration: ${constructorDuration}ms`);
    } catch (error) {
      console.error(`[BotPanel] ERROR in constructor: ${error.message}`);
      console.error(`[BotPanel] ERROR stack: ${error.stack}`);
      vscode.window.showErrorMessage(`Bot Panel Constructor Error: ${error.message}\n${error.stack}`);
      throw error;
    }


    this._panel.onDidDispose(() => this.dispose(), null, this._disposables);




    this._panel.onDidChangeViewState(
      (e) => {

        if (this._isOpeningFile) {
          setTimeout(() => { this._isOpeningFile = false; }, 500);
        }
      },
      null,
      this._disposables
    );


    Logger.log('[BotPanel] Registering onDidReceiveMessage handler');
    this._panel.webview.onDidReceiveMessage(
      (message) => {
        Logger.log('[BotPanel] *** MESSAGE HANDLER FIRED ***');
        Logger.log('[BotPanel] Received message from webview: ' + message.command + ' ' + JSON.stringify(message));
        switch (message.command) {
          case "hidePanel":

            Logger.log('[BotPanel] Closing panel');
            this._panel.dispose();
            return;
          case "refresh":
            const cachePath = path.join(this._workspaceRoot, 'docs', 'stories', '.story-graph-enriched-cache.json');
            try {
              if (fs.existsSync(cachePath)) {
                fs.unlinkSync(cachePath);
                Logger.log('[BotPanel] Deleted enriched cache file');
              }
            } catch (err) {
              this._reportError(err, 'Could not delete cache');
            }

            (async () => {
              try {
                Logger.log('[BotPanel] Clearing story graph cache...');
                await this._botView.execute('reload_story_graph --format json');
                Logger.log('[BotPanel] Story graph cache cleared');
              } catch (err) {
                this._reportError(err, 'Could not clear story graph cache');
              }

              try {
                await this._update();

                const botData = this._botView?.botData;

                // The User's ACE Workspace (not the VS Code workspace)
                this._workspaceRoot = botData.workspace_directory;

                const currentAction = botData?.behaviors?.current_action || botData?.current_action || null;
                if (currentAction) {
                  setTimeout(() => {
                    try {
                      Logger.log(`[BotPanel] Refresh: Re-expanding section for: ${currentAction}`);
                      this._panel.webview.postMessage({
                        command: 'expandInstructionsSection',
                        actionName: currentAction
                      });
                    } catch (postErr) {
                      this._reportError(postErr, 'expandInstructionsSection after refresh');
                    }
                  }, 200);
                }
              } catch (err) {
                this._reportError(err, 'Refresh');
              }
            })();
            return;
          case "toggleIncrementView":
            StoryGraphManager.toggleIncrementView(message, this)
              .then((result) => {
                  if (result) return this._update();
              });
            return;
          case "switchViewMode":
            StoryGraphManager.switchViewMode(message, this)
              return this._update();            
          case "logToFile":
            if (message.message) {
              Logger.logPanelClicks(message.message);
            }
            return;
          case "logScopeDebug":
            if (message.message) {
              Logger.logScopeDebug(message.message);
            }
            return;
          case "showScopeError":
            if (message.message) {
              const errMsg = message.message;
              Logger.log(`[BotPanel] Scope error from webview: ${errMsg}`);
              vscode.window.showErrorMessage(errMsg);
            }
            return;
          case "copyNodeToClipboard":
            StoryGraphManager.copyNodeToClipboard(message, this);
            return;
          case "copyIncrementStoriesJson":
            StoryGraphManager.copyIncrementStoriesJson(message, this);
            return;
          case "copyText":
            vscode.env.clipboard.writeText(message.text || '').then(() => {
              vscode.window.showInformationMessage(message.label || 'Copied to clipboard');
            });
            return;
          case "openFile":
            Logger.log('[BotPanel] openFile message received with filePath: ' + message.filePath);
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
              
              if (fs.existsSync(absolutePath) && fs.statSync(absolutePath).isDirectory()) {

                vscode.commands.executeCommand('revealInExplorer', fileUri).catch((error) => {
                  this._reportError(error, `Failed to reveal folder: ${message.filePath}`);
                });
              } else {
                const fileExtension = cleanPath.split('.').pop().toLowerCase();
                const binaryOrSpecialExtensions = ['drawio', 'png', 'jpg', 'jpeg', 'gif', 'pdf', 'svg'];

                const useVscodeOpenExtensions = ['json'];
                

                const MAX_TEXT_FILE_SIZE = 10 * 1024 * 1024;
                let fileSize = 0;
                try {
                  if (fs.existsSync(absolutePath)) {
                    fileSize = fs.statSync(absolutePath).size;
                  }
                } catch (e) {
                  this._reportError(e, 'Could not stat file for open');
                }
                
                if (binaryOrSpecialExtensions.includes(fileExtension)) {
                  vscode.commands.executeCommand('vscode.open', fileUri).catch((error) => {
                    this._reportError(error, `Failed to open file: ${message.filePath}`);
                  });
                } else if (useVscodeOpenExtensions.includes(fileExtension)) {

                  vscode.commands.executeCommand('vscode.open', fileUri).catch((error) => {
                    this._reportError(error, `Failed to open file: ${message.filePath}`);
                  });
                } else if (fileSize > MAX_TEXT_FILE_SIZE) {

                  Logger.log(`[BotPanel] File exceeds ${MAX_TEXT_FILE_SIZE} bytes (${fileSize}), using vscode.open`);
                  vscode.commands.executeCommand('vscode.open', fileUri).catch((error) => {
                    this._reportError(error, `Failed to open file: ${message.filePath}`);
                  });
                } else if (fileExtension === 'md') {

                  vscode.commands.executeCommand('markdown.showPreview', fileUri).catch((error) => {
                    this._reportError(error, `Failed to open markdown preview: ${message.filePath}`);
                  });
                } else {
                const openOptions = { viewColumn: vscode.ViewColumn.One, preserveFocus: false };
                
                if (lineNumber && !symbolName) {
                  openOptions.selection = new vscode.Range(lineNumber - 1, 0, lineNumber - 1, 0);
                  vscode.window.showTextDocument(fileUri, openOptions).catch((error) => {
                    this._reportError(error, `Failed to open file: ${message.filePath}`);
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
                      this._reportError(error, `Failed to open file: ${message.filePath}`);
                    }
                  );
                } else {
                  vscode.window.showTextDocument(fileUri, openOptions).catch((error) => {
                    this._reportError(error, `Failed to open file: ${message.filePath}`);
                  });
                }
                }
              }
            }
            return;
          case "openFiles":
            Logger.log('[BotPanel] openFiles message received with ' + (message.filePaths && message.filePaths.length) + ' paths');
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
                if (!fs.existsSync(absolutePath) || fs.statSync(absolutePath).isDirectory()) continue;
                const fileExtension = rawPath.split('.').pop().toLowerCase();
                const uri = lineNumber
                  ? vscode.Uri.file(absolutePath).with({ fragment: `L${lineNumber}` })
                  : vscode.Uri.file(absolutePath);
                vscode.commands.executeCommand('vscode.open', uri).catch((err) => {
                  this._reportError(err, `openFiles failed for ${pathStr}`);
                });
              }
            }
            return;
          case "openFileInColumn":
            Logger.log('[BotPanel] openFileInColumn message received');
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
              

              const fileExtension = cleanPath.split('.').pop().toLowerCase();
              if (fileExtension === 'json') {
                vscode.commands.executeCommand('vscode.open', fileUri).catch((error) => {
                  this._reportError(error, `Failed to open file: ${message.filePath}`);
                });
              } else {
                vscode.window.showTextDocument(fileUri, { viewColumn: targetColumn, preserveFocus: false }).catch((error) => {
                  this._reportError(error, `Failed to open file: ${message.filePath}`);
                });
              }
            }
            return;
          case "openFileWithState":
            Logger.log('[BotPanel] openFileWithState message received');
            if (message.filePath) {

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
              

              const fileExtension = cleanPath.split('.').pop().toLowerCase();
              if (fileExtension === 'json' && message.state && message.state.selectedNode) {

                const node = message.state.selectedNode;
                let startLine = 0;
                try {
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
                  this._reportError(e, 'Could not search for node');
                }
                const uriWithFragment = vscode.Uri.file(absolutePath).with({ fragment: `L${startLine + 1}` });
                vscode.commands.executeCommand('vscode.open', uriWithFragment).catch((error) => {
                  this._reportError(error, `Failed to open file: ${message.filePath}`);
                });
                Logger.log(`[BotPanel] JSON file opened with state: selectedNode=${node.name}`);
              } else if (fileExtension === 'json') {

                vscode.commands.executeCommand('vscode.open', fileUri).catch((error) => {
                  this._reportError(error, `Failed to open file: ${message.filePath}`);
                });
              } else if (message.state && message.state.lineNumber) {
                const options = {
                  viewColumn: vscode.ViewColumn.One,
                  selection: new vscode.Range(message.state.lineNumber - 1, 0, message.state.lineNumber - 1, 0),
                  preserveFocus: false
                };
                vscode.window.showTextDocument(fileUri, options).then(() => {
                  Logger.log(`[BotPanel] File opened with state: lineNumber=${message.state.lineNumber}`);
                }).catch((error) => {
                  this._reportError(error, `Failed to open file: ${message.filePath}`);
                });
              } else if (message.state && message.state.selectedNode) {

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
                      

                      const endLineLength = lines[endLine] ? lines[endLine].length : 0;
                      options.selection = new vscode.Range(startLine, 0, endLine, endLineLength);
                    }
                    
                    vscode.window.showTextDocument(doc, options).then(() => {
                      Logger.log(`[BotPanel] File opened with state: selectedNode=${node.name}`);
                    });
                  },
                  (error) => {

                    vscode.window.showTextDocument(fileUri, { viewColumn: vscode.ViewColumn.One, preserveFocus: false }).catch((err) => {
                      this._reportError(err, `Failed to open file: ${message.filePath}`);
                    });
                  }
                );
              } else {

                vscode.window.showTextDocument(fileUri, { viewColumn: vscode.ViewColumn.One, preserveFocus: false }).catch((error) => {
                  this._reportError(error, `Failed to open file: ${message.filePath}`);
                });
              }
            }
            return;
          case "openStoryFiles":
          case "openTestFiles":
          case "openCodeFiles":
          case "openAllRelatedFiles":

            Logger.log(`[BotPanel] ${message.command} message received for node: ${message.nodeName}`);
            this._handleOpenRelatedFiles(message);
            return;
          case "clearScopeFilter":
            if (message.viewMode) {
              this._currentStoryMapView = message.viewMode;
              Logger.log(`[BotPanel] clearScopeFilter: setting view to ${message.viewMode} before clearing`);
            }
            this._botView?.execute('scope all')
              .then(() => this._update())
              .catch((error) => {
                Logger.log(`[BotPanel] ERROR clearScopeFilter: ${error.message}`);
                vscode.window.showErrorMessage(`Failed to clear scope: ${error.message}`);
                this._displayError(`Failed to clear scope: ${error.message}`);
              });
            return;
          case "showAllScope":
            this._botView?.execute('scope showall')
              .then(() => this._update())
              .catch((error) => {
                Logger.log(`[BotPanel] ERROR showAllScope: ${error.message}`);
                vscode.window.showErrorMessage(`Failed to show all: ${error.message}`);
                this._displayError(`Failed to show all: ${error.message}`);
              });
            return;
          case "updateIncludeLevel":
            Logger.log('[BotPanel] Received updateIncludeLevel: ' + message.includeLevel);
            
            if (!this._botView) {
              const errorMsg = '_botView is null, cannot update include_level';
              Logger.log('[BotPanel] ERROR: ' + errorMsg);
              this._displayError(errorMsg);
              return;
            }            

            const scopeIncludeCmd = `scope include_level=${message.includeLevel}`;
            this._botView.execute(scopeIncludeCmd)
              .then(() => {
                Logger.log('[BotPanel] Include level updated: ' + message.includeLevel);
                return this._update();
              })
              .catch((err) => {
                const errorMsg = 'Include level update failed: ' + err.message;
                Logger.log('[BotPanel] ERROR: ' + errorMsg);
                this._displayError(errorMsg);
              });
            return;
          
          case "updateFilter":
            Logger.log('[BotPanel] Received updateFilter: ' + message.filter);
            Logger.log('[BotPanel] _botView is: ' + this._botView);
            
            if (!this._botView) {
              const errorMsg = '_botView is null, cannot execute scope command';
              Logger.log('[BotPanel] ERROR: ' + errorMsg);
              this._displayError(errorMsg);
              return;
            }
            
            if (message.filter && message.filter.trim()) {
              const filterValue = message.filter.trim();

              let prefixedFilter = filterValue;
              if (this._currentStoryMapView === 'Files') {
                prefixedFilter = `file:${filterValue}`;
              } else if (this._currentStoryMapView === 'Increment') {
                prefixedFilter = `increment ${filterValue}`;
              }
              const scopeCmd = `scope "${prefixedFilter}"`;
              Logger.log('[BotPanel] Executing scope command: ' + scopeCmd + ' (view mode: ' + this._currentStoryMapView + ')');
              
              this._botView.execute(scopeCmd)
                .then((result) => {
                  Logger.log('[BotPanel] Scope filter applied, result: ' + JSON.stringify(result).substring(0, 200));
                  return this._update();
                })
                .then(() => {
                  Logger.log('[BotPanel] Update completed after scope filter');
                })
                .catch((err) => {
                  const errorMsg = 'Scope filter failed: ' + err.message;
                  Logger.log('[BotPanel] ERROR: ' + errorMsg);
                  Logger.log('[BotPanel] ERROR stack: ' + err.stack);
                  this._displayError(errorMsg);
                  vscode.window.showErrorMessage(errorMsg);

                });
            } else {

              Logger.log('[BotPanel] Clearing scope filter');
              
              this._botView.execute('scope all')
                .then((result) => {
                  Logger.log('[BotPanel] Scope cleared successfully');
                  return this._update();
                })
                .catch((err) => {
                  const errorMsg = 'Clear scope failed: ' + err.message;
                  Logger.log('[BotPanel] ERROR: ' + errorMsg);
                  Logger.log('[BotPanel] ERROR stack: ' + err.stack);
                  this._displayError(errorMsg);
                  vscode.window.showErrorMessage(errorMsg);

                });
            }
            return;
          case "updateWorkspace":
            Logger.log('[BotPanel] Received updateWorkspace message: ' + message.workspacePath);
            WorkspaceManager.updateWorkspace(message, this)
              .then((result) => {
                if (result) return this._update();
              });
            return;
          case "browseWorkspace":
            Logger.log('[BotPanel] Received browseWorkspace message');
            WorkspaceManager.browseAndUpdateWorkspace(this)
              .then((result) => {
                if (result) return this._update();
              });
            return;
          case "switchBot":
            Logger.log('[BotPanel] Received switchBot message');
            WorkspaceManager.switchBot(message, this)
              .then((result) => {
                if (result) return this._update();
              });
            return;
          case "getBehaviorRules":
            BehaviorsManager.getBehaviorRules(message, this)
              .then((result) => {
                if (result) return this._update();
              });
            return;
          case "executeNavigationCommand":
            BehaviorsManager.executeNavigationCommand(message, this)
              .then((result) => {
                if (result) return this._update();
              });
            return;
          case "setExecutionMode":
            BehaviorsManager.setExecutionMode(message, this)
              .then((result) => {
                if (result) return this._update();
              });
            return;
          case "setBehaviorExecuteMode":
            BehaviorsManager.setBehaviorExecuteMode(message, this)
              .then((result) => {
                if (result) return this._update();
              });
            return;
          case "setBehaviorSpecialInstructions":
            BehaviorsManager.setBehaviorSpecialInstructions(message, this)
              .then((result) => {
                if (result) return this._update();
              });
            return;
          case "setActionSpecialInstructions":
            BehaviorsManager.setActionSpecialInstructions(message, this)
              .then((result) => {
                if (result) return this._update();
              });
            return;
          case "renameNode":
            StoryGraphManager.renameNode(message, this)
            return;
          case "executeCommand":
            if (message.commandText) {
              Logger.log(`\n${'='.repeat(80)}`);
              Logger.log(`[BotPanel] RECEIVED executeCommand MESSAGE`);
              Logger.log(`[BotPanel] commandText: ${message.commandText}`);
              


              const isCreateOp = message.commandText.includes('.create_') || 
                                 message.commandText.includes('.create ') || 
                                 message.commandText.match(/\.create(?:$| name:)/) ||
                                 message.commandText.includes('create child') || 
                                 message.commandText.includes('create epic');
              const isDeleteOp = message.commandText.includes('.delete');
              const isMoveOp = message.commandText.includes('.move_to');
              const isRenameOp = message.commandText.includes('.rename');
              const isStoryGraphOp = isCreateOp || isDeleteOp || isMoveOp || isRenameOp;

              const isSubmitOp = message.commandText.includes('submit_required_behavior_instructions') ||
                message.commandText.includes('submit_instructions') ||
                message.commandText.includes('submit_current_instructions');
              if (isSubmitOp) {
                Logger.log(`[SUBMIT_DEBUG] executeCommand: submit op received, commandText=${message.commandText?.substring(0, 80)}`);
                console.log('[SUBMIT_DEBUG] executeCommand: submit op received');
              }
              if (message.commandText.includes('submit_required_behavior_instructions')) {
                Logger.log(`[BotPanel] *** SUBMIT COMMAND DETECTED ***`);
                Logger.log(`[BotPanel] Command contains 'submit_required_behavior_instructions': YES`);
              }
              
              Logger.log(`[BotPanel] Operation type detected`, {
                isMoveOp,
                isRenameOp,
                isCreateOp,
                isDeleteOp
              });
                            
              const logEntry = `\n${'='.repeat(80)}\n[RECEIVED COMMAND: ${message.commandText}\n`;
              Logger.logStoryGraphOperations(logEntry);
              
              
              Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [STEP 5] Executing command via backend...`);
              const isIncrementCmd = message.commandText.includes('_increment') || message.commandText.includes('add_increment') || message.commandText.includes('rename_story_in');
              if (isIncrementCmd) {
                Logger.log(`[INCREMENT][CLI] Received increment command: ${message.commandText}`);
              }
              const runExecute = () => this._botView?.execute(message.commandText)
                .then((result) => {
                  Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [STEP 6] [SUCCESS] Backend command executed successfully`);
                  Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [STEP 6] Command: ${message.commandText}`);
                  Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [STEP 6] Result: ${JSON.stringify(result).substring(0, 500)}`);
                  if (isIncrementCmd) {
                    Logger.log(`[INCREMENT][CLI->UI] Result for "${message.commandText}": ${JSON.stringify(result)}`);
                    this._panel.webview.postMessage({
                      command: 'incrementCommandResult',
                      commandText: message.commandText,
                      result: result
                    });
                  }
                  Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [STEP 6] Timestamp: ${new Date().toISOString()}`);          
            
                  const resultLog = `SUCCESS RESULT: ${JSON.stringify(result, null, 2)}\n`;
                  Logger.log(resultLog);
                  

                  if (isSubmitOp && result) {
                    Logger.log(`[SUBMIT_DEBUG] executeCommand submit path: result status=${result?.status} clipboard_status=${result?.clipboard_status}`);
                    console.log('[SUBMIT_DEBUG] executeCommand submit path: result status=', result?.status, 'clipboard_status=', result?.clipboard_status);

                    if (result.status === 'success') {
                      const msg = result.message || 'Instructions submitted to chat!';
                      vscode.window.showInformationMessage(msg);
                    } else {
                      const errorMsg = result.message || result.error || 'Failed to submit instructions';
                      vscode.window.showErrorMessage(`Submit failed: ${errorMsg}`);
                    }

                    Logger.log(`[BotPanel] Submit completed - skipping panel refresh (no story graph changes)`);
                    return Promise.resolve();
                  }
                  

                  const timestampFile = path.join(this._workspaceRoot, 'docs', 'stories', '.story-graph-panel-edit-time');
                  try {
                    fs.writeFileSync(timestampFile, Date.now().toString());
                    Logger.log(`[BotPanel] Logged panel edit timestamp: ${Date.now()}`);
                  } catch (err) {
                    Logger.log(`[BotPanel] Failed to write timestamp file: ${err.message}`);
                  }
                  

                  if (isMoveOp || isCreateOp || isDeleteOp || isRenameOp) {
                    Logger.log(`[BotPanel] Sending saveCompleted(success=true) to webview`);
                    this._panel.webview.postMessage({
                      command: 'saveCompleted',
                      success: true,
                      result: result
                    });
                    Logger.log(`[BotPanel] Message sent to webview`);
                  }
                  

                  if (isIncrementCmd) {
                    Logger.log(`[INCREMENT] Refreshing panel after increment command`);
                    return this._update();
                  }
                  



                  if (isStoryGraphOp) {
                    Logger.log(`[BotPanel] Story-changing operation - skipping panel refresh`);
                    Logger.log(`[BotPanel] Operation type: create=${isCreateOp}, move=${isMoveOp}, delete=${isDeleteOp}, rename=${isRenameOp}`);
                    Logger.log(`[BotPanel] Panel will NOT refresh - optimistic updates remain visible`);
                    return Promise.resolve();
                  } else {

                    const isScopeCommand = message.commandText.startsWith('scope ');
                    if (isScopeCommand) {
                      Logger.log(`[BotPanel] Scope command detected - refreshing panel to show filtered view...`);
                      return this._update();
                    }
                    

                    Logger.log(`[BotPanel] Non-story operation - skipping refresh`);
                    return Promise.resolve();
                  }
                })
                .then(() => {
                  Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [STEP 9] Panel refresh completed`);
                  Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] ========== COMMAND FLOW COMPLETE ==========`);
                  Logger.log(`${'='.repeat(80)}\n`);
                })
                .catch((error) => {
                  Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [ERROR] Command execution failed`);
                  Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [ERROR] Command: ${message.commandText}`);
                  Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [ERROR] Error: ${error.message}`);
                  Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [ERROR] Stack: ${error.stack}`);
                  Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [ERROR] Timestamp: ${new Date().toISOString()}`);
                  

                  const errorLog = `[ERROR: ${error.message}\nSTACK: ${error.stack}\n`;
                  Logger.log(errorLog);
                  
                  vscode.window.showErrorMessage(`Failed to execute ${message.commandText}: ${error.message}`);
                  

                  if (isMoveOp || isCreateOp || isDeleteOp || isRenameOp) {
                    Logger.log(`[BotPanel] Sending saveCompleted(success=false) to webview`);
                    this._panel.webview.postMessage({
                      command: 'saveCompleted',
                      success: false,
                      error: error.message
                    });
                    Logger.log(`[BotPanel] Error message sent to webview`);
                  }
                  


                  if (!isOptimistic) {
                    Logger.log(`[BotPanel] Refreshing panel after error...`);
                    this._update().catch(err => {
                      Logger.log(`[BotPanel] ERROR in _update after failure: ${err.message}`);
                    });
                  } else {
                    Logger.log(`[BotPanel] Optimistic operation failed - skipping refresh (rollback handled by SaveQueue)`);
                  }
                  
                  Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] ========== COMMAND FLOW FAILED ==========`);
                  Logger.log(`${'='.repeat(80)}\n`);
                });
              if (isSubmitOp) {
                vscode.window.withProgress({
                  location: vscode.ProgressLocation.Notification,
                  title: 'Injecting scope to instructions...',
                  cancellable: false
                }, () => runExecute());
              } else {
                runExecute();
              }
            } else {
              Logger.log(`[BotPanel] WARNING: executeCommand received with no commandText`);
            }
            return;
          case "navigateToBehavior":
            BehaviorsManager.navigateToBehavior(message, this)
              .then((result) => {
                if (result) return this._updateWithCachedData();
              });
            return;
          case "submitWorkspaceBehaviorInstructions":
            BehaviorsManager.submitWorkspaceBehaviorInstructions(message, this)
              .then((result) => {
                if (result) return this._updateWithCachedData();
                return this._updateWithCachedData();
              });
            return;
          case "navigateToAction":
            BehaviorsManager.navigateToAction(message, this)
              .then((result) => {
                if (result) return this._updateWithCachedData();
              });
            return;
          case "navigateAndExecute":
            BehaviorsManager.navigateAndExecute(message, this)
              .then((result) => {
                if (result) return this._updateWithCachedData();
              });
            return;
          case "toggleSection":
            if (message.sectionId) {

            }
            return;
          case "sectionExpansion":
            if (message.sectionId && typeof message.expanded === 'boolean') {
              this._expansionState[message.sectionId] = message.expanded;
              Logger.log(`[BotPanel] sectionExpansion: ${message.sectionId} = ${message.expanded}`);
            }
            return;
          case "toggleCollapse":
            if (message.elementId) {

            }
            return;
          case "sendToChat":
            Logger.log('[SUBMIT_DEBUG] 1. sendToChat received');
            console.log('[SUBMIT_DEBUG] 1. sendToChat received');
            if (!this._botView) {
              const err = new Error('_botView is null - panel not properly initialized');
              console.error('[BotPanel]', err.message, err.stack);
              vscode.window.showErrorMessage(`Submit failed: ${err.message}`);
              throw err;
            }
            const currentBehavior = this._botView.botData?.behaviors?.current_behavior || this._botView.botData?.current_behavior;
            const currentAction = this._botView.botData?.behaviors?.current_action || this._botView.botData?.current_action;
            const submitCmd = (currentBehavior && currentAction) ? `submit ${currentBehavior} ${currentAction}` : 'submit';
            Logger.log(`[SUBMIT_DEBUG] 2. Calling _botView.execute("${submitCmd}") - panel selection: ${currentBehavior}.${currentAction}`);
            console.log('[SUBMIT_DEBUG] 2. Calling _botView.execute("' + submitCmd + '")');
            this._botView.execute(submitCmd)
              .then((output) => {
                Logger.log(`[SUBMIT_DEBUG] 3. execute resolved, status=${output?.status} clipboard_status=${output?.clipboard_status} instructions_length=${output?.instructions_length}`);
                console.log('[SUBMIT_DEBUG] 3. execute resolved, status:', output?.status, 'clipboard_status:', output?.clipboard_status, 'instructions_length:', output?.instructions_length);
                

                if (output && typeof output === 'object' && output.status) {
                  if (output.status === 'success') {
                    const msg = output.message || 'Instructions submitted to chat!';
                    vscode.window.showInformationMessage(msg);
                  } else {
                    const errorMsg = output.message || output.error || 'Unknown error';
                    vscode.window.showErrorMessage(`Submit failed: ${errorMsg}`);
                  }
                }

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
                    Logger.log('[PANEL] Submit output:', output);
                  }
                }
              })
              .catch((error) => {
                Logger.log(`[SUBMIT_DEBUG] 4. execute REJECTED: ${error?.message}`);
                console.error('[SUBMIT_DEBUG] 4. execute REJECTED:', error?.message, error?.stack);
                vscode.window.showErrorMessage(`Submit command failed: ${error.message}`);
              });
            return;
          case "saveClarifyAnswers":
            if (message.answers) {
              Logger.log(`[BotPanel] saveClarifyAnswers -> ${JSON.stringify(message.answers)}`);
              const answersJson = JSON.stringify(message.answers).replace(/'/g, "\\'");
              const cmd = `save --answers '${answersJson}'`;
              this._botView?.execute(cmd)
                .then(() => {
                  Logger.log(`[BotPanel] saveClarifyAnswers success`);
                  vscode.window.showInformationMessage('Answers saved successfully');
                })
                .catch((error) => {
                  Logger.log(`[BotPanel] saveClarifyAnswers ERROR: ${error.message}`);
                  vscode.window.showErrorMessage(`Failed to save clarify answers: ${error.message}`);
                });
            }
            return;
          case "saveClarifyEvidence":
            if (message.evidence_provided) {
              Logger.log(`[BotPanel] saveClarifyEvidence -> ${JSON.stringify(message.evidence_provided)}`);
              const evidenceJson = JSON.stringify(message.evidence_provided).replace(/'/g, "\\'");
              const cmd = `save --evidence_provided '${evidenceJson}'`;
              this._botView?.execute(cmd)
                .then(() => {
                  Logger.log(`[BotPanel] saveClarifyEvidence success`);
                  vscode.window.showInformationMessage('Evidence saved successfully');
                })
                .catch((error) => {
                  Logger.log(`[BotPanel] saveClarifyEvidence ERROR: ${error.message}`);
                  vscode.window.showErrorMessage(`Failed to save clarify evidence: ${error.message}`);
                });
            }
            return;
          case "saveStrategyDecision":
            if (message.criteriaKey && message.selectedOption) {
              Logger.log(`[BotPanel] saveStrategyDecision -> ${message.criteriaKey}: ${message.selectedOption}`);

              const decisions = {};
              decisions[message.criteriaKey] = message.selectedOption;
              const decisionsJson = JSON.stringify(decisions).replace(/'/g, "\\'");
              const cmd = `save --decisions '${decisionsJson}'`;
              this._botView?.execute(cmd)
                .then(() => {
                  Logger.log(`[BotPanel] saveStrategyDecision success`);
                  vscode.window.showInformationMessage('Strategy decision saved successfully');
                })
                .catch((error) => {
                  Logger.log(`[BotPanel] saveStrategyDecision ERROR: ${error.message}`);
                  vscode.window.showErrorMessage(`Failed to save strategy decision: ${error.message}`);
                });
            }
            return;
          case "saveStrategyMultiDecision":
            if (message.criteriaKey && message.selectedOptions) {
              Logger.log(`[BotPanel] saveStrategyMultiDecision -> ${message.criteriaKey}: ${JSON.stringify(message.selectedOptions)}`);

              const multiDecisions = {};
              multiDecisions[message.criteriaKey] = message.selectedOptions;
              const multiDecisionsJson = JSON.stringify(multiDecisions).replace(/'/g, "\\'");
              const multiCmd = `save --decisions '${multiDecisionsJson}'`;
              this._botView?.execute(multiCmd)
                .then(() => {
                  Logger.log(`[BotPanel] saveStrategyMultiDecision success`);
                  vscode.window.showInformationMessage('Strategy decisions saved successfully');
                })
                .catch((error) => {
                  Logger.log(`[BotPanel] saveStrategyMultiDecision ERROR: ${error.message}`);
                  vscode.window.showErrorMessage(`Failed to save strategy decisions: ${error.message}`);
                });
            }
            return;
          case "renderDiagram": {
            if (!this._findDiagramPathToOpen) {
              this._findDiagramPathToOpen = (result, fallbackPath, scope) => {
                if (result?.results && Array.isArray(result.results)) {
                  const executed = result.results.find(r => r.status === 'executed' && r.path);
                  if (executed) return executed.path;
                  const anyWithPath = result.results.find(r => r.path);
                  if (anyWithPath) return anyWithPath.path;
                }
                if (result?.path) return result.path;
                if (fallbackPath) {
                  let openPath = fallbackPath;
                  if (scope) {
                    const sanitized = scope.toLowerCase().replace(/ /g, '-').replace(/[^a-z0-9-]/g, '');
                    if (openPath.includes('{scope}')) openPath = openPath.replace('{scope}', sanitized);
                    else if (openPath.includes('-all.drawio')) openPath = openPath.replace('-all.drawio', `-${sanitized}.drawio`);
                    else if (openPath.endsWith('.drawio')) openPath = openPath.replace('.drawio', `-${sanitized}.drawio`);
                  } else if (openPath.includes('{scope}')) {
                    openPath = openPath.replace('{scope}', 'all');
                  }
                  return openPath;
                }
                return null;
              };
            }
            const behaviorName = this._botView?.botData?.behaviors?.current_behavior || this._botView?.botData?.current_behavior;
            if (!behaviorName) {
              vscode.window.showErrorMessage('No current behavior set');
              return;
            }
            const diagramScope = message.scope || '';
            const scopeParam = diagramScope ? ` scope:"${diagramScope}"` : '';
            const renderCmd = `${behaviorName}.render.renderDiagram${scopeParam}`;
            Logger.log(`[BotPanel] renderDiagram -> ${renderCmd}`);
            this._renderInProgress = true;
            vscode.window.withProgress({
              location: vscode.ProgressLocation.Notification,
              title: 'Rendering diagram...',
              cancellable: false
            }, async () => {
              try {
                const result = await this._botView.execute(renderCmd);
                Logger.log(`[BotPanel] renderDiagram result keys: ${result ? Object.keys(result).join(', ') : 'null'}`);
                Logger.log(`[BotPanel] renderDiagram result.status: ${result?.status}, result.results: ${JSON.stringify(result?.results || []).substring(0, 500)}`);
                if (result?.status === 'success') {
                  const diagramPath = this._findDiagramPathToOpen(result, message.path, diagramScope);
                  Logger.log(`[BotPanel] renderDiagram resolved path: ${diagramPath || '(none)'}`);
                  if (diagramPath) {
                    try {
                      const diagramUri = vscode.Uri.file(diagramPath);
                      Logger.log(`[BotPanel] renderDiagram opening: ${diagramPath}`);
                      await vscode.commands.executeCommand('vscode.open', diagramUri);
                      vscode.window.showInformationMessage(result.message || 'Diagram rendered and opened');
                    } catch (openErr) {
                      Logger.log(`[BotPanel] renderDiagram open file error: ${openErr.message}`);
                      vscode.window.showErrorMessage(`Diagram rendered but failed to open: ${openErr.message}`);
                    }
                  } else {
                    Logger.log(`[BotPanel] renderDiagram: no path found in result to open`);
                    vscode.window.showInformationMessage(result.message || 'Diagram rendered successfully');
                  }
                } else {
                  vscode.window.showErrorMessage(result?.message || 'Failed to render diagram');
                }
                if (this._botView) this._botView.botData = null;
                await this._update();
              } catch (error) {
                Logger.log(`[BotPanel] renderDiagram ERROR: ${error.message}`);
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
            Logger.log('[BotPanel] saveDiagramLayout -> ' + layoutCmd);
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
                await this._update();
              } catch (error) {
                Logger.log('[BotPanel] saveDiagramLayout ERROR: ' + error.message);
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
            Logger.log('[BotPanel] clearDiagramLayout -> ' + clearCmd);
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
                await this._update();
              } catch (error) {
                Logger.log('[BotPanel] clearDiagramLayout ERROR: ' + error.message);
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
            Logger.log(`[BotPanel] generateDiagramReport -> ${reportCmd}`);
            vscode.window.withProgress({
              location: vscode.ProgressLocation.Notification,
              title: 'Generating update report from diagram...',
              cancellable: false
            }, async () => {
              try {
                const result = await this._botView.execute(reportCmd);
                Logger.log(`[BotPanel] generateDiagramReport result: ${JSON.stringify(result?.results || []).substring(0, 500)}`);
                if (result?.status === 'success') {
                  const reportPath = (result.results || []).find(r => r.status === 'success' && r.report_path)?.report_path || result.report_path;
                  if (reportPath) {
                    try {
                      const reportUri = vscode.Uri.file(reportPath);
                      Logger.log(`[BotPanel] generateDiagramReport opening: ${reportPath}`);
                      await vscode.commands.executeCommand('vscode.open', reportUri);
                      vscode.window.showInformationMessage(result.message || 'Report generated and opened');
                    } catch (openErr) {
                      Logger.log(`[BotPanel] generateDiagramReport open file error: ${openErr.message}`);
                      vscode.window.showInformationMessage(result.message || 'Report generated successfully');
                    }
                  } else {
                    vscode.window.showInformationMessage(result.message || 'Report generated successfully');
                  }
                } else {
                  vscode.window.showErrorMessage(result?.message || 'Failed to generate report');
                }
                await this._update();
              } catch (error) {
                Logger.log(`[BotPanel] generateDiagramReport ERROR: ${error.message}`);
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
            Logger.log(`[BotPanel] updateFromDiagram -> ${updateCmd}`);
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

                if (this._botView) {
                  this._botView.botData = null;
                }
                await this._update();
              } catch (error) {
                Logger.log(`[BotPanel] updateFromDiagram ERROR: ${error.message}`);
                vscode.window.showErrorMessage(`Failed to update from diagram: ${error.message}`);
              }
            });
            return;
          }
          case "saveStrategyAssumptions":
            if (message.assumptions) {
              Logger.log(`[BotPanel] saveStrategyAssumptions -> ${JSON.stringify(message.assumptions)}`);
              const assumptionsJson = JSON.stringify(message.assumptions).replace(/'/g, "\\'");
              const cmd = `save --assumptions '${assumptionsJson}'`;
              this._botView?.execute(cmd)
                .then(() => {
                  Logger.log(`[BotPanel] saveStrategyAssumptions success`);
                  vscode.window.showInformationMessage('Additional strategies saved successfully');
                })
                .catch((error) => {
                  Logger.log(`[BotPanel] saveStrategyAssumptions ERROR: ${error.message}`);
                  vscode.window.showErrorMessage(`Failed to save additional strategies: ${error.message}`);
                });
            }
            return;
        }
      },
      null,
      this._disposables
    );
  }

  static createOrShow(repoRoot, extensionUri) {
    console.log(`[BotPanel] >>> ENTERING createOrShow - repoRoot: ${repoRoot}`);
    console.log(`[BotPanel] >>> extensionUri: ${extensionUri}`);
    
    try {
      const column = vscode.ViewColumn.Two;
      console.log(`[BotPanel] >>> Column set: ${column}`);


      if (BotPanel.currentPanel) {
        console.log("[BotPanel] >>> Reusing existing panel");
        BotPanel.currentPanel._panel.reveal(column);
        return;
      }

      console.log("[BotPanel] >>> Creating new webview panel");

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
      BotPanel.currentPanel = new BotPanel(panel, repoRoot, extensionUri);
      console.log("[BotPanel] >>> BotPanel instance created successfully");
    } catch (error) {
      console.error(`[BotPanel] >>> EXCEPTION in createOrShow: ${error.message}`);
      console.error(`[BotPanel] >>> Stack: ${error.stack}`);
      vscode.window.showErrorMessage(`Bot Panel Error: ${error.message}`);
      throw error;
    }
  }


  static createForSidebar(webviewView, repoRoot, extensionUri) {
    console.log("[BotPanel] Creating for sidebar view");
    

    const panelWrapper = {
      webview: webviewView.webview,
      onDidDispose: webviewView.onDidDispose.bind(webviewView),

      onDidChangeViewState: (callback, thisArg, disposables) => {

        return webviewView.onDidChangeVisibility(() => {

          callback({ webviewView: webviewView });
        }, thisArg, disposables);
      },
      reveal: () => {},
      dispose: () => {}
    };
    

    const botPanel = new BotPanel(panelWrapper, repoRoot, extensionUri);
    

    console.log("[BotPanel] Sidebar instance created successfully");
    
    return botPanel;
  }

  _readPanelVersion() {
    try {

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
      Logger.log(`[BotPanel] _handleOpenRelatedFiles: ${command} for ${nodeType} "${nodeName}"`);
      
      if (!this._botView) {
        vscode.window.showErrorMessage('Bot view not available');
        return;
      }
      

      try {
        const storyGraph = await this._botView.execute('story_graph');
        Logger.log(`[BotPanel] Story graph check result: ${JSON.stringify(storyGraph)}`);
      } catch (error) {
        Logger.log(`[BotPanel] Story graph check failed (continuing anyway): ${error.message}`);
      }
      
      const workspaceRoot = this._workspaceRoot;
      

      const resolvePath = (filePath) => {
        if (!filePath) return null;
        if (path.isAbsolute(filePath)) return filePath;
        return path.join(workspaceRoot, filePath);
      };
      

      const openInColumn = async (filePath, column, options = {}) => {
        const absolutePath = resolvePath(filePath);
        if (!absolutePath || !fs.existsSync(absolutePath)) {
          Logger.log(`[BotPanel] File not found: ${filePath}`);
          return;
        }
        const fileUri = vscode.Uri.file(absolutePath);
        

        const fileExtension = filePath.split('.').pop().toLowerCase();
        if (fileExtension === 'json') {
          await vscode.commands.executeCommand('vscode.open', fileUri);
          return;
        }
        
        const doc = await vscode.workspace.openTextDocument(fileUri);

        const openOptions = { 
          viewColumn: column, 
          preview: false,
          preserveFocus: true,
          ...options 
        };
        await vscode.window.showTextDocument(doc, openOptions);
      };
      
      if (command === 'openStoryFiles') {

        if (singleFileLink) {

          await openInColumn(singleFileLink, vscode.ViewColumn.One);
        } else {

          Logger.log(`[BotPanel] Opening story files for ${nodeType} "${nodeName}"`);
          

          try {
            const result = await this._botView.execute(`story_graph.${nodePath || `"${nodeName}"`}.openStoryFile()`);
            if (result && result.files && Array.isArray(result.files)) {

              for (const filePath of result.files) {
                await openInColumn(filePath, vscode.ViewColumn.One);
              }
              Logger.log(`[BotPanel] Opened ${result.files.length} story files`);
            }
          } catch (error) {
            Logger.log(`[BotPanel] Error getting story files: ${error.message}`);


          }
        }
      } else if (command === 'openTestFiles') {

        Logger.log(`[BotPanel] Opening test files for ${nodeType} "${nodeName}"`);
        
        try {
          const result = await this._botView.execute(`story_graph.${nodePath || `"${nodeName}"`}.openTest()`);
          if (result && result.files && Array.isArray(result.files)) {
            const paths = result.files.map(f => (typeof f === 'string' ? f : f.file)).filter(Boolean);
            await this._openTestFiles(paths);
          }
        } catch (error) {
          Logger.log(`[BotPanel] Error getting test files: ${error.message}`);
          vscode.window.showErrorMessage(`Failed to open test files: ${error.message}`);
        }
      } else if (command === 'openCodeFiles') {

        Logger.log(`[BotPanel] Opening code files traced from tests for ${nodeType} "${nodeName}"`);
        
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
                Logger.log(`[BotPanel] Opened traced code file: ${codeFilePath}`);
              } else {
                Logger.log(`[BotPanel] Traced code file does not exist: ${absolutePath}`);
              }
            }
            Logger.log(`[BotPanel] Opened ${result.files.length} traced code files`);
          }
        } catch (error) {
          Logger.log(`[BotPanel] Error opening code files: ${error.message}`);
          vscode.window.showErrorMessage(`Failed to open code files: ${error.message}`);
        }
      } else if (command === 'openAllRelatedFiles') {

        const graphPath = storyGraphPath || path.join(workspaceRoot, 'docs/story/story-graph.json');
        const testFiles = message.testFiles || [];
        const storyFiles = message.storyFiles || [];
        const selectedNode = message.selectedNode;
        
        Logger.log(`[BotPanel] Opening all related files for ${nodeType} "${nodeName}"`);
        

        await this._openGraphWithNodeSelected(graphPath, selectedNode);
        
        if (nodeType === 'sub-epic' || nodeType === 'epic') {

          if (singleFileLink) {
            Logger.log(`[BotPanel] Opening exploration file for sub-epic "${nodeName}": ${singleFileLink}`);
            await this._openStoryFile(singleFileLink);
          }
          Logger.log(`[BotPanel] Opening ${storyFiles.length} story files for sub-epic "${nodeName}"`);
          for (const storyFilePath of storyFiles) {
            await this._openStoryFile(storyFilePath);
          }
        } else {

          if (singleFileLink) {
            await this._openStoryFile(singleFileLink);
          }
        }
        

        if (testFiles.length > 0) {
          await this._openTestFiles(testFiles);
        }
        

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
                Logger.log(`[BotPanel] Opened traced code file: ${codeFilePath}`);
              } else {
                Logger.log(`[BotPanel] Traced code file does not exist: ${absolutePath}`);
              }
            }
            Logger.log(`[BotPanel] Opened ${codeResult.files.length} traced code files`);
          }
        } catch (codeErr) {
          Logger.log(`[BotPanel] Error tracing code files: ${codeErr.message}`);
        }
        

        const graphAbsPath = path.isAbsolute(graphPath) ? graphPath : path.join(workspaceRoot, graphPath);
        try {
          await vscode.commands.executeCommand('vscode.open', vscode.Uri.file(graphAbsPath));
        } catch (e) {
          Logger.log(`[BotPanel] Could not re-activate story graph tab: ${e.message}`);
        }
      }
    } catch (error) {
      Logger.log(`[BotPanel] ERROR in _handleOpenRelatedFiles: ${error.message}`);
      vscode.window.showErrorMessage(`Failed to open related files: ${error.message}`);
    }
  }


  async _openGraphWithNodeSelected(graphPath, selectedNode) {
    const absolutePath = path.isAbsolute(graphPath) 
      ? graphPath 
      : path.join(this._workspaceRoot, graphPath);
    

    if (!selectedNode || !selectedNode.name) {
      await vscode.commands.executeCommand('vscode.open', vscode.Uri.file(absolutePath));
      return;
    }
    

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
      Logger.log(`[BotPanel] Could not search for node in graph: ${e.message}`);
    }
    
    const uri = vscode.Uri.file(absolutePath).with({ fragment: `L${startLine + 1}` });
    await vscode.commands.executeCommand('vscode.open', uri);
    Logger.log(`[BotPanel] Graph opened with node selected: ${selectedNode.name}`);
  }


  async _openStoryFile(filePath) {
    
    if (!filePath) return;
    
    const cleanPath = filePath.split('#')[0];
    const absolutePath = path.isAbsolute(cleanPath) 
      ? cleanPath 
      : path.join(this._workspaceRoot, cleanPath);
    
    if (!fs.existsSync(absolutePath)) {
      Logger.log(`[BotPanel] Story file not found: ${absolutePath}`);
      return;
    }
    
    const fileUri = vscode.Uri.file(absolutePath);
    const doc = await vscode.workspace.openTextDocument(fileUri);
    await vscode.window.showTextDocument(doc, {
      viewColumn: vscode.ViewColumn.One,
      preview: false,
      preserveFocus: true
    });
    Logger.log(`[BotPanel] Story file opened: ${filePath}`);
  }


  async _openTestFiles(testFiles) {
    
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
          Logger.log(`[BotPanel] Test file not found: ${absolutePath}`);
          continue;
        }
        
        const uri = lineNumber
          ? vscode.Uri.file(absolutePath).with({ fragment: `L${lineNumber}` })
          : vscode.Uri.file(absolutePath);
        await vscode.commands.executeCommand('vscode.open', uri);
      } catch (error) {
        Logger.log(`[BotPanel] Error opening test file ${testFilePath}: ${error.message}`);
      }
    }
    Logger.log(`[BotPanel] Opened ${testFiles.length} test files`);
  }

  dispose() {
    BotPanel.currentPanel = undefined;


      this._botView = null;


    console.log("[BotPanel] Cleaning up shared PanelView CLI");
    if (this._sharedCLI) {
      this._sharedCLI.cleanup();
      this._sharedCLI = null;
    }


    this._panel.dispose();

    while (this._disposables.length) {
      const disposable = this._disposables.pop();
      if (disposable) {
        disposable.dispose();
      }
    }
  }


  async _updateWithCachedData() {
    return vscode.window.withProgress({
      location: vscode.ProgressLocation.Notification,
      title: 'Reloading panel...',
      cancellable: false
    }, async () => {
    const perfUpdateStart = performance.now();
    try {
      Logger.log('[BotPanel] _updateWithCachedData() START - using cached data, skipping refresh');
      console.log("[BotPanel] _updateWithCachedData() called - skipping refresh");
      const webview = this._panel.webview;
      this._panel.title = "Bot Panel";
      

      if (!this._botView) {
        const perfBotViewStart = performance.now();
        this._botView = new BotView(this._sharedCLI, this._panelVersion, webview, this._extensionUri);
        const perfBotViewEnd = performance.now();
        Logger.log(`[PERF] BotView creation: ${(perfBotViewEnd - perfBotViewStart).toFixed(2)}ms`);
      }
      

      Logger.log('[BotPanel] Skipping refresh() - using cached botData from navigation');
      

      if (this._botView.storyMapView) {
        this._botView.storyMapView.currentViewMode = this._currentStoryMapView || 'Hierarchy';
        this._botView.storyMapView.scopeSectionExpanded = this._expansionState['scope-content'] !== false;
      }
      

      const perfRenderStart = performance.now();
      const botData = this._botView.botData;
      const currentBehavior = botData?.behaviors?.current_behavior || botData?.current_behavior || null;
      const currentAction = botData?.behaviors?.current_action || botData?.current_action || null;
      const html = this._getWebviewContent(await this._botView.render(), currentBehavior, currentAction, botData);
      const perfRenderEnd = performance.now();
      Logger.log(`[PERF] HTML rendering: ${(perfRenderEnd - perfRenderStart).toFixed(2)}ms`);
      
      this._lastHtmlLength = html.length;
      this._panel.webview.html = html;
      

      PanelView._lastResponse = null;
      
      const perfUpdateEnd = performance.now();
      Logger.log(`[PERF] TOTAL _updateWithCachedData() duration: ${(perfUpdateEnd - perfUpdateStart).toFixed(2)}ms`);
      Logger.log('[BotPanel] _updateWithCachedData() END');
      
    } catch (err) {
      console.error(`[BotPanel] ERROR in _updateWithCachedData: ${err.message}`);
      Logger.log(`[BotPanel] ERROR in _updateWithCachedData, falling back to full _update: ${err.message}`);

      return this._update();
    }
    });
  }


  async refresh() {
    return this._update();
  }

  _setupDiagramFileWatchers(botData) {

    if (this._diagramWatchers) {
      this._diagramWatchers.forEach(function(w) { w.dispose(); });
    }
    this._diagramWatchers = [];
  }


  async _update() {
    return vscode.window.withProgress({
      location: vscode.ProgressLocation.Notification,
      title: 'Reloading panel...',
      cancellable: false
    }, async () => {

    const perfUpdateStart = performance.now();
    try {
      Logger.log('[BotPanel] _update() START');
      console.log("[BotPanel] _update() called");
      const webview = this._panel.webview;
      this._panel.title = "Bot Panel";
      

      if (!this._botView) {

        const perfBotViewStart = performance.now();
        console.log("[BotPanel] Creating BotView");
        Logger.log('[BotPanel] Creating BotView');
        try {
          this._botView = new BotView(this._sharedCLI, this._panelVersion, webview, this._extensionUri);
          const perfBotViewEnd = performance.now();
          const botViewDuration = (perfBotViewEnd - perfBotViewStart).toFixed(2);
          console.log("[BotPanel] BotView created successfully");
          Logger.log(`[BotPanel] BotView created successfully in ${botViewDuration}ms`);
          Logger.log(`[PERF] BotView creation: ${botViewDuration}ms`);
        } catch (botViewError) {
          console.error(`[BotPanel] ERROR creating BotView: ${botViewError.message}`);
          console.error(`[BotPanel] ERROR stack: ${botViewError.stack}`);
          Logger.log(`[BotPanel] ERROR creating BotView: ${botViewError.message}`);
          throw botViewError;
        }
      }
      

      if (this._botView.storyMapView) {
        this._botView.storyMapView.currentViewMode = this._currentStoryMapView || 'Hierarchy';
        this._botView.storyMapView.scopeSectionExpanded = this._expansionState['scope-content'] !== false;
      }
      


      const perfRefreshStart = performance.now();
      console.log("[BotPanel] Refreshing bot data...");
      Logger.log('[BotPanel] Calling _botView.refresh() to fetch latest data');
      await this._botView.refresh();
      const perfRefreshEnd = performance.now();
      const refreshDuration = (perfRefreshEnd - perfRefreshStart).toFixed(2);
      Logger.log(`[BotPanel] Data refreshed successfully in ${refreshDuration}ms`);
      Logger.log(`[PERF] Data refresh: ${refreshDuration}ms`);
      

      const perfRenderStart = performance.now();
      console.log("[BotPanel] Rendering HTML");
      Logger.log('[BotPanel] _botView.render() starting');

      const botData = this._botView.botData || await this._botView.execute('status');
      const currentBehavior = botData?.behaviors?.current_behavior || botData?.current_behavior || null;
      const currentAction = botData?.behaviors?.current_action || botData?.current_action || null;
      const html = this._getWebviewContent(await this._botView.render(), currentBehavior, currentAction, botData);
      const perfRenderEnd = performance.now();
      const renderDuration = (perfRenderEnd - perfRenderStart).toFixed(2);
      Logger.log(`[PERF] HTML rendering: ${renderDuration}ms`)
      

      const perfHtmlUpdateStart = performance.now();
      

      const htmlPreview = html.substring(0, 500).replace(/\s+/g, ' ');
      Logger.log(`[BotPanel] Setting webview HTML (length: ${html.length}, preview: ${htmlPreview}...)`);
      Logger.log(`[BotPanel] Current HTML length: ${this._lastHtmlLength || 0}, New HTML length: ${html.length}`);
      
      if (this._lastHtmlLength === html.length) {
        Logger.log('[BotPanel] WARNING: HTML length unchanged - content may not have updated');
      } else {
        Logger.log('[BotPanel] HTML length changed - update should be visible');
      }
      
      this._lastHtmlLength = html.length;
      this._panel.webview.html = html;
      
      try { this._setupDiagramFileWatchers(botData); } catch (e) { Logger.log('[BotPanel] watcher setup error: ' + e.message); }
      
      const perfHtmlUpdateEnd = performance.now();
      const htmlUpdateDuration = (perfHtmlUpdateEnd - perfHtmlUpdateStart).toFixed(2);
      Logger.log('[BotPanel] Webview HTML property set');
      Logger.log(`[PERF] HTML update (set webview.html): ${htmlUpdateDuration}ms`);
      

      setTimeout(() => {

        this._panel.webview.postMessage({
          command: 'refreshStatus',
          state: 'refreshing',
          message: 'Refreshing...'
        });
        Logger.log('[BotPanel] Sent refreshStatus refreshing message to webview');
      }, 100);
      

      const perfUpdateEnd = performance.now();
      const totalDuration = (perfUpdateEnd - perfUpdateStart).toFixed(2);
      console.log("[BotPanel] _update() completed successfully");
      Logger.log('[BotPanel] _update() completed successfully');
      Logger.log(`[PERF] TOTAL _update() duration: ${totalDuration}ms`);
      Logger.log('[BotPanel] _update() END');
      Logger.log('[PERF] Python timing: see .cursor/panel-perf.log in workspace');
      
    } catch (err) {
      console.error(`[BotPanel] ERROR in _update: ${err.message}`);
      console.error(`[BotPanel] ERROR stack: ${err.stack}`);
      Logger.log(`[BotPanel] ERROR in _update: ${err.message} | Stack: ${err.stack}`);
      

      const errorMsg = err.isCliError 
        ? `CLI Error: ${err.message}` 
        : `Bot Panel Update Error: ${err.message}`;
      vscode.window.showErrorMessage(errorMsg);
      

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
    });
  }

  _getWebviewContent(contentHtml, currentBehavior = null, currentAction = null, botData = null) {

    const webview = this._panel.webview;   

    // Local path to main script run in the webview
		const botPanelClientPath = vscode.Uri.joinPath(this._extensionUri, 'bot', 'bot_panel_client.js');
    const workspaceClientPath = vscode.Uri.joinPath(this._extensionUri, 'workspace', 'workspace_client.js');
    const behaviorsClientPath = vscode.Uri.joinPath(this._extensionUri, 'behaviors', 'behaviors_client.js');
    const behaviorsStylePath = vscode.Uri.joinPath(this._extensionUri, 'behaviors', 'behaviors.css');
    const storyGraphClientPath = vscode.Uri.joinPath(this._extensionUri, 'story_graph', 'story_graph_client.js');
    const storyMapClientPath = vscode.Uri.joinPath(this._extensionUri, 'story_graph', 'story_map_client.js');
    const storyGraphStylePath = vscode.Uri.joinPath(this._extensionUri, 'story_graph', 'story_graph.css');

		// And the uri we use to load this script in the webview
		const botPanelClientUri = webview.asWebviewUri(botPanelClientPath);
    const workspaceClientUri = webview.asWebviewUri(workspaceClientPath);
    const behaviorsClientUri = webview.asWebviewUri(behaviorsClientPath);
    const behaviorsStyleUri = webview.asWebviewUri(behaviorsStylePath);
    const storyGraphClientUri = webview.asWebviewUri(storyGraphClientPath);
    const storyMapClientUri = webview.asWebviewUri(storyMapClientPath);
    const storyGraphStyleUri = webview.asWebviewUri(storyGraphStylePath);
    
    // Get branding colors for CSS theming
    const brandColor = branding.getTitleColor();
    const bgColor = branding.getBackgroundColor();
    const textColor = branding.getTextColor();
    const textColorFaded = branding.getTextColorFaded();
    const fontWeight = branding.getFontWeight();

    const hexToRgb = (hex) => {
      const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
      return result ? `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}` : '255, 140, 0';
    };
    const brandColorRgb = hexToRgb(brandColor);
    const bgColorRgb = hexToRgb(bgColor);
    const textColorRgb = hexToRgb(textColor);
    const isLightBg = bgColor.toLowerCase() === '#ffffff' || bgColor.toLowerCase() === '#fff';
    
    const hoverBg = isLightBg ? 'rgba(0, 0, 0, 0.05)' : 'rgba(255, 255, 255, 0.03)';
    
    // /* Input styling - chat-like appearance */    
    const inputBg = isLightBg ? 'rgba(0, 0, 0, 0.03)' : 'rgba(255, 255, 255, 0.05)';    
    const inputBgFocus = isLightBg ? 'rgba(0, 0, 0, 0.06)' : 'rgba(255, 255, 255, 0.08)';    
    const inputBorder = isLightBg ? 'rgba(0, 0, 0, 0.15)' : 'rgba(255, 255, 255, 0.1)';

    // replace branding placeholders in css file
    // contentStyles(brandColor, brandColorRgb, bgColor, bgColorRgb, textColor, textColorRgb, textColorFaded, fontWeight, isLightBg)}  
    const stylesPath = vscode.Uri.joinPath(this._extensionUri, 'bot', 'bot_panel.css');
    let contentStyle = fs.readFileSync(stylesPath.fsPath, 'utf-8');    
    
    contentStyle = contentStyle.replace(/{{brandColor}}/g, brandColor)
      .replace(/{{brandColorRgb}}/g, brandColorRgb)
      .replace(/{{bgColor}}/g, bgColor)
      .replace(/{{bgColorRgb}}/g, bgColorRgb)
      .replace(/{{textColor}}/g, textColor)
      .replace(/{{textColorRgb}}/g, textColorRgb)
      .replace(/{{textColorFaded}}/g, textColorFaded)
      .replace(/{{fontWeight}}/g, fontWeight)
      .replace(/{{isLightBg}}/g, isLightBg)
      .replace(/{{hoverBg}}/g, hoverBg)
      .replace(/{{inputBg}}/g, inputBg)
      .replace(/{{inputBgFocus}}/g, inputBgFocus)
      .replace(/{{inputBorder}}/g, inputBorder);    
    
    const nonce = getNonce();
    const currentBehaviorScript = currentBehavior 
      ? '\n        <script>\n            window.currentBehavior = ' + JSON.stringify(currentBehavior) + ';\n            ' + (currentAction ? 'window.currentAction = ' + JSON.stringify(currentAction) + ';' : '') + '\n            ' + (botData ? 'window.botData = ' + JSON.stringify(botData) + ';' : '') + '\n        </script>'
      : (botData ? '\n        <script>\n            window.botData = ' + JSON.stringify(botData) + ';\n        </script>' : '');
    return `<!DOCTYPE html>
      <html lang="en">
      <head>
          <meta charset="UTF-8">
          <!--
              Use a content security policy to only allow loading images from https or from our extension directory,
              and only allow scripts that have a specific nonce.
          -->
          <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src ${webview.cspSource} 'unsafe-inline'; img-src ${webview.cspSource} https:; script-src ${webview.cspSource} 'unsafe-inline';">

          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Bot Panel</title>
          <style nonce="${nonce}">
            ${contentStyle}  
          </style>
          <link rel="stylesheet" href="${behaviorsStyleUri}">
          <link rel="stylesheet" href="${storyGraphStyleUri}">
          ${currentBehaviorScript}
      </head>
      <body>
          ${contentHtml}    
          <script nonce="${nonce}" src="${botPanelClientUri}"></script>
          <script nonce="${nonce}" src="${workspaceClientUri}"></script>
          <script nonce="${nonce}" src="${behaviorsClientUri}"></script>
          <script nonce="${nonce}" src="${storyGraphClientUri}"></script>
          <script nonce="${nonce}" src="${storyMapClientUri}"></script>
      </body>
      </html>`;
  }
}

function getNonce() {
	let text = '';
	const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
	for (let i = 0; i < 32; i++) {
		text += possible.charAt(Math.floor(Math.random() * possible.length));
	}
	return text;
}


BotPanel.currentPanel = undefined;
BotPanel.viewType = "agilebot.botPanel";

module.exports = BotPanel;