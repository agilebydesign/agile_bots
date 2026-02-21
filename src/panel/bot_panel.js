

const vscode = require("vscode");
const path = require("path");
const fs = require("fs");
const BotView = require("./bot_view");
const PanelView = require("./panel_view");
const branding = require("./branding");

class BotPanel {
  constructor(panel, workspaceRoot, extensionUri) {

    const perfConstructorStart = performance.now();
    try {

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
      /** Report error to both log and display - never swallow. */
      this._reportError = (err, context = '') => {
        const msg = err?.message || String(err);
        const stack = err?.stack || '';
        const full = context ? `[${context}] ${msg}` : msg;
        this._log(`[BotPanel] ERROR: ${full}`);
        if (stack) this._log(`[BotPanel] Stack: ${stack}`);
        console.error('[BotPanel]', full, stack);
        vscode.window.showErrorMessage(full);
      };
      
      this._log("[BotPanel] Constructor invoked");
      this._log(`[PERF] Constructor start`);
      console.log(`[BotPanel] Constructor called - workspaceRoot: ${workspaceRoot}`);
      this._panel = panel;
      this._workspaceRoot = workspaceRoot;
      this._extensionUri = extensionUri;
      this._disposables = [];
      this._expansionState = {};
      this._currentStoryMapView = 'Hierarchy';
      

      branding.setRepoRoot(workspaceRoot);
      this._log(`[BotPanel] Branding initialized: ${branding.getBranding()}`);
      

      const perfVersionStart = performance.now();
      console.log("[BotPanel] Reading panel version");
      this._panelVersion = this._readPanelVersion();
      const perfVersionEnd = performance.now();
      console.log(`[BotPanel] Panel version: ${this._panelVersion}`);
      this._log(`[PERF] Read panel version: ${(perfVersionEnd - perfVersionStart).toFixed(2)}ms`);
      

      let botDirectory = process.env.BOT_DIRECTORY || path.join(workspaceRoot, 'bots', 'story_bot');

      if (!path.isAbsolute(botDirectory)) {
        botDirectory = path.join(workspaceRoot, botDirectory);
      }
      console.log(`[BotPanel] Bot directory: ${botDirectory}`);
      

      const perfPanelViewStart = performance.now();
      console.log("[BotPanel] Creating shared PanelView instance");
      this._sharedCLI = new PanelView(botDirectory);
      const perfPanelViewEnd = performance.now();
      console.log("[BotPanel] Shared PanelView instance created successfully");
      this._log(`[PERF] PanelView creation: ${(perfPanelViewEnd - perfPanelViewStart).toFixed(2)}ms`);
      

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
      this._log(`[PERF] TOTAL Constructor duration: ${constructorDuration}ms`);
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


    this._log('[BotPanel] Registering onDidReceiveMessage handler');
    this._panel.webview.onDidReceiveMessage(
      (message) => {
        this._log('[BotPanel] *** MESSAGE HANDLER FIRED ***');
        this._log('[BotPanel] Received message from webview: ' + message.command + ' ' + JSON.stringify(message));
        switch (message.command) {
          case "hidePanel":

            this._log('[BotPanel] Closing panel');
            this._panel.dispose();
            return;
          case "refresh":
            const cachePath = path.join(this._workspaceRoot, 'docs', 'stories', '.story-graph-enriched-cache.json');
            try {
              if (fs.existsSync(cachePath)) {
                fs.unlinkSync(cachePath);
                this._log('[BotPanel] Deleted enriched cache file');
              }
            } catch (err) {
              this._reportError(err, 'Could not delete cache');
            }

            (async () => {
              try {
                this._log('[BotPanel] Clearing story graph cache...');
                await this._botView.execute('reload_story_graph --format json');
                this._log('[BotPanel] Story graph cache cleared');
              } catch (err) {
                this._reportError(err, 'Could not clear story graph cache');
              }

              try {
                await this._update();

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

            this._log('[BotPanel] toggleIncrementView: switching to ' + message.currentView);
            this._currentStoryMapView = message.currentView;

            (async () => {
              try {
                await this._update();
              } catch (err) {
                this._reportError(err, 'Toggle view');
              }
            })();
            return;
          case "switchViewMode":

            this._log('[BotPanel] switchViewMode: switching to ' + message.viewMode);
            this._currentStoryMapView = message.viewMode;

            (async () => {
              try {
                await this._update();
              } catch (err) {
                this._reportError(err, 'Switch view');
              }
            })();
            return;
          case "logToFile":
            if (message.message) {
              const logPath = path.join(this._workspaceRoot, 'panel_clicks.log');
              const timestamp = new Date().toISOString();
              fs.appendFileSync(logPath, `[${timestamp}] ${message.message}\n`);
            }
            return;
          case "logScopeDebug":
            if (message.message) {
              const logDir = path.join(this._workspaceRoot, 'logs');
              try { fs.mkdirSync(logDir, { recursive: true }); } catch (e) { console.error('[BotPanel] Could not create log dir:', e?.message); vscode.window.showErrorMessage(`Could not create log dir: ${e?.message}`); }
              const scopeLogPath = path.join(logDir, 'scope_debug.log');
              const timestamp = new Date().toISOString();
              fs.appendFileSync(scopeLogPath, `[${timestamp}] [PANEL] ${message.message}\n`);
            }
            return;
          case "showScopeError":
            if (message.message) {
              const errMsg = message.message;
              this._log(`[BotPanel] Scope error from webview: ${errMsg}`);
              vscode.window.showErrorMessage(errMsg);
            }
            return;
          case "copyNodeToClipboard":
            (() => {
              const nodePath = message.nodePath;
              const action = message.action;
              if (!nodePath || !action) return;
              const method = action === 'json' ? 'copy_json' : 'copy_name';
              const command = nodePath + '.' + method;
              const doCopy = async () => {
                const response = await this._botView.execute(command);
                const result = response && (response.result !== undefined ? response.result : response);
                let text;
                if (action === 'json') {
                  text = (typeof result === 'string' ? result : JSON.stringify(result, null, 2));
                } else {

                  if (typeof result === 'string') {
                    text = result;
                  } else if (result && typeof result === 'object') {
                    text = result.result ?? result.node_name ?? result.message ?? result.name ?? '';
                    text = String(text);
                  } else {
                    text = String(result != null ? result : '');
                  }
                }
                await vscode.env.clipboard.writeText(text);
                vscode.window.showInformationMessage(action === 'json' ? 'Node JSON copied to clipboard' : 'Node name copied to clipboard');
              };
              if (action === 'json') {
                vscode.window.withProgress({
                  location: vscode.ProgressLocation.Notification,
                  title: 'Injecting scope to clipboard...',
                  cancellable: false
                }, async () => {
                  try {
                    await doCopy();
                  } catch (err) {
                    this._log(`[BotPanel] copyNodeToClipboard failed: ${err.message}`);
                    vscode.window.showErrorMessage(`Copy failed: ${err.message}`);
                  }
                });
              } else {
                doCopy().catch((err) => {
                  this._log(`[BotPanel] copyNodeToClipboard failed: ${err.message}`);
                  vscode.window.showErrorMessage(`Copy failed: ${err.message}`);
                });
              }
            })();
            return;
          case "copyText":
            vscode.env.clipboard.writeText(message.text || '').then(() => {
              vscode.window.showInformationMessage(message.label || 'Copied to clipboard');
            });
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

                  this._log(`[BotPanel] File exceeds ${MAX_TEXT_FILE_SIZE} bytes (${fileSize}), using vscode.open`);
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
            this._log('[BotPanel] openFileWithState message received');
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
                this._log(`[BotPanel] JSON file opened with state: selectedNode=${node.name}`);
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
                  this._log(`[BotPanel] File opened with state: lineNumber=${message.state.lineNumber}`);
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
                      this._log(`[BotPanel] File opened with state: selectedNode=${node.name}`);
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

            this._log(`[BotPanel] ${message.command} message received for node: ${message.nodeName}`);
            this._handleOpenRelatedFiles(message);
            return;
          case "clearScopeFilter":
            if (message.viewMode) {
              this._currentStoryMapView = message.viewMode;
              this._log(`[BotPanel] clearScopeFilter: setting view to ${message.viewMode} before clearing`);
            }
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

                });
            } else {

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

                this._panel.webview.postMessage({
                  command: 'setWorkspacePath',
                  path: folderPath
                });

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
                  this._reportError(error, 'Failed to switch bot');
                });
            }
            return;
          case "getBehaviorRules":
            if (message.behaviorName) {
              this._log(`[BotPanel] getBehaviorRules -> ${message.behaviorName}`);
              this._log(`[getBehaviorRules] STARTED for behavior: ${message.behaviorName}`);
              

              this._botView?.execute(`submitrules:${message.behaviorName}`)
                .then((result) => {
                  this._log('[BotPanel] Rules submitted:', result);
                  this._log(`[getBehaviorRules] Result received: ${JSON.stringify(result, null, 2)}`);
                  

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
          case "setExecutionMode":
            if (message.behaviorName && message.actionName && message.mode) {
              const cmd = `${message.behaviorName}.${message.actionName}.set_execution ${message.mode}`;
              this._log(`[BotPanel] setExecutionMode -> ${cmd}`);
              this._botView?.execute(cmd)
                .then((result) => {
                  this._log(`[BotPanel] setExecutionMode success: ${cmd}`);
                  if (this._botView) this._botView.botData = null;
                  return this._update();
                })
                .catch((error) => {
                  this._log(`[BotPanel] setExecutionMode ERROR: ${error.message}`);
                  vscode.window.showErrorMessage(`Failed to set execution mode: ${error.message}`);
                });
            }
            return;
          case "setBehaviorExecuteMode":
            if (message.behaviorName && message.mode) {
              const cmd = `${message.behaviorName}.set_execution ${message.mode}`;
              this._log(`[BotPanel] setBehaviorExecuteMode -> ${cmd}`);
              this._botView?.execute(cmd)
                .then((result) => {
                  this._log(`[BotPanel] setBehaviorExecuteMode success: ${cmd}`);
                  if (this._botView) this._botView.botData = null;
                  return this._update();
                })
                .catch((error) => {
                  this._log(`[BotPanel] setBehaviorExecuteMode ERROR: ${error.message}`);
                  vscode.window.showErrorMessage(`Failed to set behavior execution mode: ${error.message}`);
                });
            }
            return;
          case "setBehaviorSpecialInstructions":
            if (message.behaviorName !== undefined) {
              const escaped = (message.instructionText || '').replace(/"/g, '\\"');
              const cmd = `${message.behaviorName}.set_special_instructions "${escaped}"`;
              this._log(`[BotPanel] setBehaviorSpecialInstructions -> ${cmd}`);
              this._botView?.execute(cmd)
                .then((result) => {
                  this._log(`[BotPanel] setBehaviorSpecialInstructions success`);
                  if (this._botView) this._botView.botData = null;
                  return this._update();
                })
                .catch((error) => {
                  this._log(`[BotPanel] setBehaviorSpecialInstructions ERROR: ${error.message}`);
                  vscode.window.showErrorMessage(`Failed to set special instructions: ${error.message}`);
                });
            }
            return;
          case "setActionSpecialInstructions":
            if (message.behaviorName && message.actionName !== undefined) {
              const escaped = (message.instructionText || '').replace(/"/g, '\\"');
              const cmd = `${message.behaviorName}.${message.actionName}.special_instructions "${escaped}"`;
              this._log(`[BotPanel] setActionSpecialInstructions -> ${cmd}`);
              this._botView?.execute(cmd)
                .then((result) => {
                  this._log(`[BotPanel] setActionSpecialInstructions success`);
                  if (this._botView) this._botView.botData = null;
                  return this._update();
                })
                .catch((error) => {
                  this._log(`[BotPanel] setActionSpecialInstructions ERROR: ${error.message}`);
                  vscode.window.showErrorMessage(`Failed to set special instructions: ${error.message}`);
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

                  const trimmedName = newName.trim().replace(/^"(.*)"$/, '$1');

                  const escapedName = trimmedName.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
                  const command = `${message.nodePath}.rename name:"${escapedName}"`;
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Built rename command: ${command}`);
                  

                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Sending optimistic update to webview`);
                  this._panel.webview.postMessage({
                    command: 'optimisticRename',
                    nodePath: message.nodePath,
                    oldName: message.currentName,
                    newName: trimmedName
                  });
                  
                  const logPath = path.join(this._workspaceRoot, 'story_graph_operations.log');
                  const timestamp = new Date().toISOString();
                  const logEntry = `\n${'='.repeat(80)}\n[${timestamp}] RENAME COMMAND: ${command}\n`;
                  
                  try {
                    fs.appendFileSync(logPath, logEntry);
                  } catch (err) {
                    this._log(`[BotPanel] Failed to write to log file: ${err.message}`);
                  }
                  

                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Executing rename command via backend (optimistic)...`);
                  this._botView?.execute(command)
                    .then((result) => {
                      this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] [SUCCESS] Backend rename executed successfully`);
                      this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Result: ${JSON.stringify(result).substring(0, 500)}`);
                      

                      const resultLog = `[${timestamp}] RESULT: ${JSON.stringify(result, null, 2)}\n`;
                      try {
                        fs.appendFileSync(logPath, resultLog);
                      } catch (err) {
                        this._log(`[BotPanel] Failed to write result to log file: ${err.message}`);
                      }
                      

                      this._panel.webview.postMessage({
                        command: 'saveCompleted',
                        success: true,
                        result: result
                      });
                      

                      this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Optimistic update - skipping panel refresh`);
                      this._log(`[ASYNC_SAVE] [EXTENSION_HOST] ========== RENAME OPERATION COMPLETE ==========`);
                    })
                    .catch((error) => {
                      this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] [ERROR] Rename failed`);
                      this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] [ERROR] Error: ${error.message}`);
                      this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] [ERROR] Stack: ${error.stack}`);
                      

                      this._panel.webview.postMessage({
                        command: 'saveCompleted',
                        success: false,
                        error: error.message
                      });
                      

                      const errorLog = `[${timestamp}] ERROR: ${error.message}\nSTACK: ${error.stack}\n`;
                      try {
                        fs.appendFileSync(logPath, errorLog);
                      } catch (err) {
                        this._log(`[BotPanel] Failed to write error to log file: ${err.message}`);
                      }
                      
                      vscode.window.showErrorMessage(`Failed to rename: ${error.message}`);
                      

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
                this._log(`[SUBMIT_DEBUG] executeCommand: submit op received, commandText=${message.commandText?.substring(0, 80)}`);
                console.log('[SUBMIT_DEBUG] executeCommand: submit op received');
              }
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
              
              const logPath = path.join(this._workspaceRoot, 'story_graph_operations.log');
              const timestamp = new Date().toISOString();
              const logEntry = `\n${'='.repeat(80)}\n[${timestamp}] RECEIVED COMMAND: ${message.commandText}\n`;
              
              try {
                fs.appendFileSync(logPath, logEntry);
              } catch (err) {
                this._log(`[BotPanel] Failed to write to log file: ${err.message}`);
              }
              
              this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [STEP 5] Executing command via backend...`);
              const isIncrementCmd = message.commandText.includes('_increment') || message.commandText.includes('add_increment') || message.commandText.includes('rename_story_in');
              if (isIncrementCmd) {
                this._log(`[INCREMENT][CLI] Received increment command: ${message.commandText}`);
              }
              const runExecute = () => this._botView?.execute(message.commandText)
                .then((result) => {
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [STEP 6] [SUCCESS] Backend command executed successfully`);
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [STEP 6] Command: ${message.commandText}`);
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [STEP 6] Result: ${JSON.stringify(result).substring(0, 500)}`);
                  if (isIncrementCmd) {
                    this._log(`[INCREMENT][CLI->UI] Result for "${message.commandText}": ${JSON.stringify(result)}`);
                    this._panel.webview.postMessage({
                      command: 'incrementCommandResult',
                      commandText: message.commandText,
                      result: result
                    });
                  }
                  this._log(`[ASYNC_SAVE] [EXTENSION_HOST] [STEP 6] Timestamp: ${new Date().toISOString()}`);
                  

                  const resultLog = `[${timestamp}] SUCCESS RESULT: ${JSON.stringify(result, null, 2)}\n`;
                  try {
                    fs.appendFileSync(logPath, resultLog);
                  } catch (err) {
                    this._log(`[BotPanel] Failed to write result to log file: ${err.message}`);
                  }
                  

                  if (isSubmitOp && result) {
                    this._log(`[SUBMIT_DEBUG] executeCommand submit path: result status=${result?.status} clipboard_status=${result?.clipboard_status}`);
                    console.log('[SUBMIT_DEBUG] executeCommand submit path: result status=', result?.status, 'clipboard_status=', result?.clipboard_status);

                    if (result.status === 'success') {
                      const msg = result.message || 'Instructions submitted to chat!';
                      vscode.window.showInformationMessage(msg);
                    } else {
                      const errorMsg = result.message || result.error || 'Failed to submit instructions';
                      vscode.window.showErrorMessage(`Submit failed: ${errorMsg}`);
                    }

                    this._log(`[BotPanel] Submit completed - skipping panel refresh (no story graph changes)`);
                    return Promise.resolve();
                  }
                  

                  const timestampFile = path.join(this._workspaceRoot, 'docs', 'stories', '.story-graph-panel-edit-time');
                  try {
                    fs.writeFileSync(timestampFile, Date.now().toString());
                    this._log(`[BotPanel] Logged panel edit timestamp: ${Date.now()}`);
                  } catch (err) {
                    this._log(`[BotPanel] Failed to write timestamp file: ${err.message}`);
                  }
                  

                  if (isMoveOp || isCreateOp || isDeleteOp || isRenameOp) {
                    this._log(`[BotPanel] Sending saveCompleted(success=true) to webview`);
                    this._panel.webview.postMessage({
                      command: 'saveCompleted',
                      success: true,
                      result: result
                    });
                    this._log(`[BotPanel] Message sent to webview`);
                  }
                  

                  if (isIncrementCmd) {
                    this._log(`[INCREMENT] Refreshing panel after increment command`);
                    return this._update();
                  }
                  



                  if (isStoryGraphOp) {
                    this._log(`[BotPanel] Story-changing operation - skipping panel refresh`);
                    this._log(`[BotPanel] Operation type: create=${isCreateOp}, move=${isMoveOp}, delete=${isDeleteOp}, rename=${isRenameOp}`);
                    this._log(`[BotPanel] Panel will NOT refresh - optimistic updates remain visible`);
                    return Promise.resolve();
                  } else {

                    const isScopeCommand = message.commandText.startsWith('scope ');
                    if (isScopeCommand) {
                      this._log(`[BotPanel] Scope command detected - refreshing panel to show filtered view...`);
                      return this._update();
                    }
                    

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
                  

                  const errorLog = `[${timestamp}] ERROR: ${error.message}\nSTACK: ${error.stack}\n`;
                  try {
                    fs.appendFileSync(logPath, errorLog);
                  } catch (err) {
                    this._log(`[BotPanel] Failed to write error to log file: ${err.message}`);
                  }
                  
                  vscode.window.showErrorMessage(`Failed to execute ${message.commandText}: ${error.message}`);
                  

                  if (isMoveOp || isCreateOp || isDeleteOp || isRenameOp) {
                    this._log(`[BotPanel] Sending saveCompleted(success=false) to webview`);
                    this._panel.webview.postMessage({
                      command: 'saveCompleted',
                      success: false,
                      error: error.message
                    });
                    this._log(`[BotPanel] Error message sent to webview`);
                  }
                  


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
              this._log(`[BotPanel] WARNING: executeCommand received with no commandText`);
            }
            return;
          case "navigateToBehavior":
            if (message.behaviorName) {
              const cmd = `${message.behaviorName}`;
              this._botView?.execute(cmd)
                .then((result) => {

                  if (result?.bot) {
                    this._botView.botData = result.bot;

                    if (result.instructions) {
                      this._botView.botData.instructions = result.instructions;
                    }

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

                  if (result?.bot) {
                    this._botView.botData = result.bot;

                    if (result.instructions) {
                      this._botView.botData.instructions = result.instructions;
                      this._log(`[BotPanel] Copied instructions into botData`);
                    } else {
                      this._log(`[BotPanel] WARNING: No instructions in result to copy!`);
                    }

                    PanelView._lastResponse = result;
                  } else {
                    this._log(`[BotPanel] WARNING: No result.bot - not caching!`);
                  }
                  return this._updateWithCachedData().then(() => {


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

                  if (result?.bot) {
                    this._botView.botData = result.bot;

                    if (result.instructions) {
                      this._botView.botData.instructions = result.instructions;
                    }

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

            }
            return;
          case "sectionExpansion":
            if (message.sectionId && typeof message.expanded === 'boolean') {
              this._expansionState[message.sectionId] = message.expanded;
              this._log(`[BotPanel] sectionExpansion: ${message.sectionId} = ${message.expanded}`);
            }
            return;
          case "toggleCollapse":
            if (message.elementId) {

            }
            return;
          case "sendToChat":
            this._log('[SUBMIT_DEBUG] 1. sendToChat received');
            console.log('[SUBMIT_DEBUG] 1. sendToChat received');
            if (!this._botView) {
              const err = new Error('_botView is null - panel not properly initialized');
              console.error('[BotPanel]', err.message, err.stack);
              vscode.window.showErrorMessage(`Submit failed: ${err.message}`);
              throw err;
            }
            this._log('[SUBMIT_DEBUG] 2. Calling _botView.execute("submit")');
            console.log('[SUBMIT_DEBUG] 2. Calling _botView.execute("submit")');
            this._botView.execute('submit')
              .then((output) => {
                this._log(`[SUBMIT_DEBUG] 3. execute resolved, status=${output?.status} clipboard_status=${output?.clipboard_status} instructions_length=${output?.instructions_length}`);
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
                    this._log('[PANEL] Submit output:', output);
                  }
                }
              })
              .catch((error) => {
                this._log(`[SUBMIT_DEBUG] 4. execute REJECTED: ${error?.message}`);
                console.error('[SUBMIT_DEBUG] 4. execute REJECTED:', error?.message, error?.stack);
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

                  if (message.path) {
                    try {


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
      BotPanel.currentPanel = new BotPanel(panel, workspaceRoot, extensionUri);
      console.log("[BotPanel] >>> BotPanel instance created successfully");
    } catch (error) {
      console.error(`[BotPanel] >>> EXCEPTION in createOrShow: ${error.message}`);
      console.error(`[BotPanel] >>> Stack: ${error.stack}`);
      vscode.window.showErrorMessage(`Bot Panel Error: ${error.message}`);
      throw error;
    }
  }


  static createForSidebar(webviewView, workspaceRoot, extensionUri) {
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
    

    const botPanel = new BotPanel(panelWrapper, workspaceRoot, extensionUri);
    

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
      this._log(`[BotPanel] _handleOpenRelatedFiles: ${command} for ${nodeType} "${nodeName}"`);
      
      if (!this._botView) {
        vscode.window.showErrorMessage('Bot view not available');
        return;
      }
      

      try {
        const storyGraph = await this._botView.execute('story_graph');
        this._log(`[BotPanel] Story graph check result: ${JSON.stringify(storyGraph)}`);
      } catch (error) {
        this._log(`[BotPanel] Story graph check failed (continuing anyway): ${error.message}`);
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
          this._log(`[BotPanel] File not found: ${filePath}`);
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

          this._log(`[BotPanel] Opening story files for ${nodeType} "${nodeName}"`);
          

          try {
            const result = await this._botView.execute(`story_graph.${nodePath || `"${nodeName}"`}.openStoryFile()`);
            if (result && result.files && Array.isArray(result.files)) {

              for (const filePath of result.files) {
                await openInColumn(filePath, vscode.ViewColumn.One);
              }
              this._log(`[BotPanel] Opened ${result.files.length} story files`);
            }
          } catch (error) {
            this._log(`[BotPanel] Error getting story files: ${error.message}`);


          }
        }
      } else if (command === 'openTestFiles') {

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

        const graphPath = storyGraphPath || path.join(workspaceRoot, 'docs/story/story-graph.json');
        const testFiles = message.testFiles || [];
        const storyFiles = message.storyFiles || [];
        const selectedNode = message.selectedNode;
        
        this._log(`[BotPanel] Opening all related files for ${nodeType} "${nodeName}"`);
        

        await this._openGraphWithNodeSelected(graphPath, selectedNode);
        
        if (nodeType === 'sub-epic' || nodeType === 'epic') {

          if (singleFileLink) {
            this._log(`[BotPanel] Opening exploration file for sub-epic "${nodeName}": ${singleFileLink}`);
            await this._openStoryFile(singleFileLink);
          }
          this._log(`[BotPanel] Opening ${storyFiles.length} story files for sub-epic "${nodeName}"`);
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
      this._log(`[BotPanel] Could not search for node in graph: ${e.message}`);
    }
    
    const uri = vscode.Uri.file(absolutePath).with({ fragment: `L${startLine + 1}` });
    await vscode.commands.executeCommand('vscode.open', uri);
    this._log(`[BotPanel] Graph opened with node selected: ${selectedNode.name}`);
  }


  async _openStoryFile(filePath) {
    
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
      this._log('[BotPanel] _updateWithCachedData() START - using cached data, skipping refresh');
      console.log("[BotPanel] _updateWithCachedData() called - skipping refresh");
      const webview = this._panel.webview;
      this._panel.title = "Bot Panel";
      

      if (!this._botView) {
        const perfBotViewStart = performance.now();
        this._botView = new BotView(this._sharedCLI, this._panelVersion, webview, this._extensionUri);
        const perfBotViewEnd = performance.now();
        this._log(`[PERF] BotView creation: ${(perfBotViewEnd - perfBotViewStart).toFixed(2)}ms`);
      }
      

      this._log('[BotPanel] Skipping refresh() - using cached botData from navigation');
      

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
      this._log(`[PERF] HTML rendering: ${(perfRenderEnd - perfRenderStart).toFixed(2)}ms`);
      
      this._lastHtmlLength = html.length;
      this._panel.webview.html = html;
      

      PanelView._lastResponse = null;
      
      const perfUpdateEnd = performance.now();
      this._log(`[PERF] TOTAL _updateWithCachedData() duration: ${(perfUpdateEnd - perfUpdateStart).toFixed(2)}ms`);
      this._log('[BotPanel] _updateWithCachedData() END');
      
    } catch (err) {
      console.error(`[BotPanel] ERROR in _updateWithCachedData: ${err.message}`);
      this._log(`[BotPanel] ERROR in _updateWithCachedData, falling back to full _update: ${err.message}`);

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
      this._log('[BotPanel] _update() START');
      console.log("[BotPanel] _update() called");
      const webview = this._panel.webview;
      this._panel.title = "Bot Panel";
      

      if (!this._botView) {

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
      

      if (this._botView.storyMapView) {
        this._botView.storyMapView.currentViewMode = this._currentStoryMapView || 'Hierarchy';
        this._botView.storyMapView.scopeSectionExpanded = this._expansionState['scope-content'] !== false;
      }
      


      const perfRefreshStart = performance.now();
      console.log("[BotPanel] Refreshing bot data...");
      this._log('[BotPanel] Calling _botView.refresh() to fetch latest data');
      await this._botView.refresh();
      const perfRefreshEnd = performance.now();
      const refreshDuration = (perfRefreshEnd - perfRefreshStart).toFixed(2);
      this._log(`[BotPanel] Data refreshed successfully in ${refreshDuration}ms`);
      this._log(`[PERF] Data refresh: ${refreshDuration}ms`);
      

      const perfRenderStart = performance.now();
      console.log("[BotPanel] Rendering HTML");
      this._log('[BotPanel] _botView.render() starting');

      const botData = this._botView.botData || await this._botView.execute('status');
      const currentBehavior = botData?.behaviors?.current_behavior || botData?.current_behavior || null;
      const currentAction = botData?.behaviors?.current_action || botData?.current_action || null;
      const html = this._getWebviewContent(await this._botView.render(), currentBehavior, currentAction, botData);
      const perfRenderEnd = performance.now();
      const renderDuration = (perfRenderEnd - perfRenderStart).toFixed(2);
      this._log(`[PERF] HTML rendering: ${renderDuration}ms`)
      

      const perfHtmlUpdateStart = performance.now();
      

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
      

      setTimeout(() => {

        this._panel.webview.postMessage({
          command: 'refreshStatus',
          state: 'refreshing',
          message: 'Refreshing...'
        });
        this._log('[BotPanel] Sent refreshStatus refreshing message to webview');
      }, 100);
      

      const perfUpdateEnd = performance.now();
      const totalDuration = (perfUpdateEnd - perfUpdateStart).toFixed(2);
      console.log("[BotPanel] _update() completed successfully");
      this._log('[BotPanel] _update() completed successfully');
      this._log(`[PERF] TOTAL _update() duration: ${totalDuration}ms`);
      this._log('[BotPanel] _update() END');
      this._log('[PERF] Python timing: see .cursor/panel-perf.log in workspace');
      
    } catch (err) {
      console.error(`[BotPanel] ERROR in _update: ${err.message}`);
      console.error(`[BotPanel] ERROR stack: ${err.stack}`);
      this._log(`[BotPanel] ERROR in _update: ${err.message} | Stack: ${err.stack}`);
      

      const errorMsg = err.isCliError 
        ? `CLI Error: ${err.message}` 
        : `Bot Panel Update Error: ${err.message}`;
      vscode.window.showErrorMessage(errorMsg);
      

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
    });
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

        
        :root {

            --bg-base: ${bgColor};
            --text-color: ${textColor};
            --text-color-faded: ${textColorFaded};
            --accent-color: ${brandColor};
            --border-color: ${brandColor};
            --divider-color: ${brandColor};
            --hover-bg: ${isLightBg ? 'rgba(0, 0, 0, 0.05)' : 'rgba(255, 255, 255, 0.03)'};
            

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
            

            --border-width: 1px;
            --border-radius: 0;
            --border-radius-sm: 0;
            --active-border-width: 2px;
            

            --space-xs: 2px;
            --space-sm: 4px;
            --space-md: 6px;
            --space-lg: 8px;
            

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
        

        img {
            flex-shrink: 0;
            min-width: 0;
        }
        
        .bot-view {
            display: flex;
            flex-direction: column;
            gap: 0;
        }
        

        
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
        
        .execution-toggle-btn {
            padding: 0;
            font-size: 12px;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 3px;
            background: #000;
            color: var(--text-color-faded);
            cursor: pointer;
            opacity: 0.5;
            min-width: 28px;
            min-height: 28px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            transition: background-color 80ms ease, color 80ms ease, border-color 80ms ease, opacity 80ms ease;
        }
        .execution-toggle-container { display: inline-flex; align-items: center; overflow: visible; }
        .execution-toggle-collapsed { display: inline-flex; align-items: center; justify-content: center; transition: opacity 0.2s ease, max-width 0.25s ease; overflow: hidden; }
        .execution-toggle-container:not(.expanded) .execution-toggle-collapsed { opacity: 1; max-width: 40px; }
        .execution-toggle-container.expanded .execution-toggle-collapsed { opacity: 0; max-width: 0; min-width: 0; padding: 0; margin: 0; border: none; pointer-events: none; }
        .execution-toggle-expanded { display: inline-flex; gap: 4px; align-items: center; min-width: 0; overflow: hidden; transition: max-width 0.28s ease, opacity 0.22s ease; }
        .execution-toggle-container:not(.expanded) .execution-toggle-expanded { max-width: 0; opacity: 0; padding: 0; margin: 0; pointer-events: none; }
        .execution-toggle-container.expanded .execution-toggle-expanded { max-width: 380px; opacity: 1; }
        .execution-toggle-collapse-btn { background: transparent; border: none; padding: 2px; cursor: pointer; opacity: 0.6; }
        .execution-toggle-collapse-btn:hover { opacity: 1; }
        .execution-toggle-btn:hover {
            background: rgba(255,255,255,0.08);
            color: var(--text-color);
        }
        .execution-toggle-btn.active {
            background: rgba(255,255,255,0.12);
            color: var(--text-color);
            opacity: 1;
        }
        

        
        .story-node {
            padding: 2px 4px;
            border-radius: 3px;
            transition: background-color 150ms ease;
        }
        
        .story-node:hover {
            background-color: rgba(${brandColorRgb}, 0.15);
        }
        
        .story-node.selected {
            background-color: rgba(${brandColorRgb}, 0.35);
        }
        
        .increment-column-container.selected {
            background-color: rgba(${brandColorRgb}, 0.2);
            border-top: 2px solid var(--accent-color);
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
        

        .save-status {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            border: var(--input-border-width) solid var(--accent-color);
            border-radius: var(--input-border-radius);
            background-color: rgba(255, 140, 0, 0.1);
            color: var(--text-color);
            font-size: var(--font-size-sm);
            transition: opacity 0.3s, background-color 150ms ease;
            white-space: nowrap;
        }
        
        .save-status.saving,
        .save-status.refreshing {
            background-color: rgba(255, 140, 0, 0.15);
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
        
        

        document.addEventListener('DOMContentLoaded', function() {
            try {

                const savedState = sessionStorage.getItem('collapseState');
                if (savedState) {
                    const state = JSON.parse(savedState);

                    setTimeout(() => window.restoreCollapseState(state), 50);
                    console.log('[WebView] Restored collapse state for', Object.keys(state).length, 'nodes');
                }
                

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
        

        document.addEventListener('visibilitychange', function() {
            if (document.visibilityState === 'hidden') {
                if (window.saveScrollPosition) {
                    window.saveScrollPosition();
                }
            } else if (document.visibilityState === 'visible') {

                setTimeout(() => {
                    if (window.restoreScrollPosition) {
                        window.restoreScrollPosition();
                    }
                }, 50);
            }
        });
        

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
            


            const storyNode = target.closest && target.closest('.story-node');
            if (storyNode) {
                console.log('═══════════════════════════════════════════════════════');
                console.log('[WebView] STORY NODE CLICKED');
                const nodeType = storyNode.getAttribute('data-node-type');
                const nodeName = storyNode.getAttribute('data-node-name');
                const hasChildren = storyNode.getAttribute('data-has-children') === 'true';
                const hasStories = storyNode.getAttribute('data-has-stories') === 'true';
                const hasNestedSubEpics = storyNode.getAttribute('data-has-nested-sub-epics') === 'true';
                const nodePath = storyNode.getAttribute('data-path');
                const fileLink = storyNode.getAttribute('data-file-link');
                const behavior = storyNode.getAttribute('data-behavior-needed') || null;
                const behaviorsAttr = storyNode.getAttribute('data-behaviors-needed');
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
                

                if (window.openFile && fileLink) {
                    console.log('[WebView]   Opening file:', fileLink);
                    window.openFile(fileLink);
                }
                
                e.stopPropagation();
                console.log('═══════════════════════════════════════════════════════');
            }
            


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
                } else if (action === 'toggleExecutionToggle') {
                    const targetId = actionElement.getAttribute('data-target');
                    if (targetId && window.toggleExecutionToggle) {
                        window.toggleExecutionToggle(targetId);
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
                } else if (action === 'setExecutionMode') {
                    const behaviorName = actionElement.getAttribute('data-behavior-name');
                    const actionName = actionElement.getAttribute('data-action-name');
                    const mode = actionElement.getAttribute('data-mode');
                    if (behaviorName && actionName && mode) {
                        const container = actionElement.closest('.execution-toggle-container');
                        if (container && container.id && container.classList.contains('expanded')) {
                            container.classList.remove('expanded');
                            const currentState = window.getCollapseState();
                            sessionStorage.setItem('collapseState', JSON.stringify(currentState));
                        }
                        vscode.postMessage({
                            command: 'setExecutionMode',
                            behaviorName: behaviorName,
                            actionName: actionName,
                            mode: mode
                        });
                        e.stopPropagation();
                        e.preventDefault();
                    }
                } else if (action === 'setBehaviorExecuteMode') {
                    const behaviorName = actionElement.getAttribute('data-behavior-name');
                    const mode = actionElement.getAttribute('data-mode');
                    if (behaviorName && mode) {
                        const container = actionElement.closest('.execution-toggle-container');
                        if (container && container.id && container.classList.contains('expanded')) {
                            container.classList.remove('expanded');
                            const currentState = window.getCollapseState();
                            sessionStorage.setItem('collapseState', JSON.stringify(currentState));
                        }
                        vscode.postMessage({
                            command: 'setBehaviorExecuteMode',
                            behaviorName: behaviorName,
                            mode: mode
                        });
                        e.stopPropagation();
                        e.preventDefault();
                    }
                }
            }
        }, true);
        

        document.addEventListener('dblclick', function(e) {
            const target = e.target;
            


            if (target.classList.contains('story-node') && target.getAttribute('data-inc-source') === null) {
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
        }, true);
        

        function _showCopyMenu(e, items) {
            e.preventDefault();
            e.stopPropagation();
            const existing = document.getElementById('story-node-copy-menu');
            if (existing) existing.remove();
            const menu = document.createElement('div');
            menu.id = 'story-node-copy-menu';
            menu.style.cssText = 'position:fixed;left:' + e.clientX + 'px;top:' + e.clientY + 'px;background:var(--vscode-dropdown-background);border:1px solid var(--vscode-dropdown-border);border-radius:4px;padding:4px 0;z-index:10001;min-width:160px;box-shadow:0 2px 8px rgba(0,0,0,0.2);';
            items.forEach(function(item) {
                const div = document.createElement('div');
                div.textContent = item.label;
                div.style.cssText = 'padding:6px 12px;cursor:pointer;font-size:12px;';
                div.onmouseover = function() { div.style.backgroundColor = 'var(--vscode-list-hoverBackground)'; };
                div.onmouseout = function() { div.style.backgroundColor = ''; };
                div.onclick = function(ev) {
                    ev.preventDefault(); ev.stopPropagation();
                    menu.remove();
                    document.removeEventListener('click', closeMenu);
                    item.action();
                };
                menu.appendChild(div);
            });
            function closeMenu() { if (menu.parentNode) menu.remove(); document.removeEventListener('click', closeMenu); }
            document.body.appendChild(menu);
            setTimeout(function() { document.addEventListener('click', closeMenu); }, 0);
        }

        document.addEventListener('contextmenu', function(e) {

            let incCol = e.target;
            let d = 6;
            while (incCol && d-- > 0 && !incCol.classList.contains('increment-column-container')) incCol = incCol.parentElement;
            if (incCol && incCol.classList.contains('increment-column-container')) {
                const incName = incCol.getAttribute('data-inc');
                const stories = Array.from(incCol.querySelectorAll('.story-node[data-inc-source]'))
                    .map(el => el.getAttribute('data-node-name'));
                _showCopyMenu(e, [
                    { label: 'Copy increment name', action: function() {
                        vscode.postMessage({ command: 'copyText', text: incName, label: 'Increment name copied' });
                    }},
                    { label: 'Copy as JSON', action: function() {
                        vscode.postMessage({ command: 'copyText', text: JSON.stringify({ name: incName, stories: stories }, null, 2), label: 'Increment JSON copied' });
                    }}
                ]);
                return;
            }


            const target = e.target.closest ? e.target.closest('.story-node') : (function() {
                let t = e.target;
                while (t && !t.classList.contains('story-node')) t = t.parentElement;
                return t;
            })();
            if (!target || !target.classList.contains('story-node')) return;

            const incSource = target.getAttribute('data-inc-source');
            const nodeName = target.getAttribute('data-node-name');

            if (incSource !== null) {

                _showCopyMenu(e, [
                    { label: 'Copy story name', action: function() {
                        vscode.postMessage({ command: 'copyText', text: nodeName, label: 'Story name copied' });
                    }},
                    { label: 'Copy as JSON', action: function() {
                        vscode.postMessage({ command: 'copyText', text: JSON.stringify({ name: nodeName }, null, 2), label: 'Story JSON copied' });
                    }}
                ]);
                return;
            }


            const nodePath = target.getAttribute('data-path');
            if (!nodePath) return;
            _showCopyMenu(e, [
                { label: 'Copy node name', action: function() {
                    vscode.postMessage({ command: 'copyNodeToClipboard', nodePath: nodePath, action: 'name' });
                }},
                { label: 'Copy full JSON', action: function() {
                    vscode.postMessage({ command: 'copyNodeToClipboard', nodePath: nodePath, action: 'json' });
                }}
            ]);
        }, true);
        

        let draggedNode = null;
        let draggedIncrement = null;
        let dropIndicator = null;
        let currentDropZone = null;
        let incrementDropTarget = null;
        

        function createDropIndicator() {
            if (!dropIndicator) {
                dropIndicator = document.createElement('div');
                dropIndicator.style.position = 'fixed';
                dropIndicator.style.height = '2px';
                dropIndicator.style.backgroundColor = 'rgb(255, 140, 0)';
                dropIndicator.style.pointerEvents = 'none';
                dropIndicator.style.zIndex = '10000';
                dropIndicator.style.transition = 'all 0.1s ease';
                dropIndicator.style.display = 'none';
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
            

            if (e.target.classList && e.target.classList.contains('increment-drag-handle')) {
                draggedIncrement = e.target.getAttribute('data-inc');
                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('text/plain', 'increment:' + draggedIncrement);
                e.target.style.opacity = '0.5';
                vscode.postMessage({ command: 'logToFile', message: '[INCREMENT] Drag column started: ' + draggedIncrement });
                return;
            }


            let target = e.target;
            while (target && !target.classList.contains('story-node')) {
                target = target.parentElement;
            }
            
            if (target && target.classList.contains('story-node')) {
                draggedNode = {
                    path: target.getAttribute('data-path'),
                    name: target.getAttribute('data-node-name'),
                    type: target.getAttribute('data-node-type'),
                    position: parseInt(target.getAttribute('data-position') || '0'),
                    fromIncrement: target.getAttribute('data-inc-source')
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
            

            let target = e.target;
            while (target && !target.classList.contains('story-node')) {
                target = target.parentElement;
            }
            
            if (target && target.classList.contains('story-node')) {
                target.style.opacity = '1';
            }
            if (e.target.classList && e.target.classList.contains('increment-drag-handle')) {
                e.target.style.opacity = '';
            }
            draggedNode = null;
            draggedIncrement = null;
            if (incrementDropTarget) { incrementDropTarget.style.outline = ''; incrementDropTarget = null; }
            removeDropIndicator();
            document.querySelectorAll('.increment-column-container').forEach(function(c) { c.style.outline = ''; });
            var unallocEl = document.querySelector('.unallocated-column');
            if (unallocEl) unallocEl.style.outline = '';
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] Drag ended, cleared draggedNode'
            });
        }, true);
        
        let dragoverLogCounter = 0;
        document.addEventListener('dragover', function(e) {

            if (draggedIncrement) {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';

                let col = e.target;
                let d = 10;
                while (col && d-- > 0 && !col.classList.contains('increment-column-container')) col = col.parentElement;
                if (col && col.getAttribute('data-inc') !== draggedIncrement) {
                    if (incrementDropTarget) incrementDropTarget.style.outline = '';
                    incrementDropTarget = col;
                    const rect = col.getBoundingClientRect();
                    const isLeft = e.clientX < rect.left + rect.width / 2;
                    col.style.outline = isLeft ? '2px solid orange' : '';
                    col.style.outlineOffset = '-2px';

                    const ind = createDropIndicator();
                    ind.style.width = '3px';
                    ind.style.height = rect.height + 'px';
                    ind.style.top = rect.top + 'px';
                    ind.style.left = (isLeft ? rect.left : rect.right - 3) + 'px';
                    ind.style.display = 'block';
                }
                return;
            }


            let target = e.target;
            let searchDepth = 0;
            while (target && !target.classList.contains('story-node') && searchDepth < 10) {
                target = target.parentElement;
                searchDepth++;
            }
            

            if (dragoverLogCounter++ % 20 === 0 && draggedNode) {
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] DRAGOVER - found target: ' + (target ? 'YES' : 'NO') + ', draggedNode: ' + (draggedNode ? draggedNode.name : 'null')
                });
            }
            

            if (draggedNode && draggedNode.type === 'story') {
                var incEl = e.target;
                var d = 6;
                while (incEl && d-- > 0) {
                    if (incEl.classList && incEl.classList.contains('increment-column-container')) {
                        e.preventDefault();
                        e.dataTransfer.dropEffect = 'copy';
                        incEl.style.outline = '2px solid var(--accent-color)';
                        break;
                    }
                    incEl = incEl.parentElement;
                }
                if (!incEl || !incEl.classList.contains('increment-column-container')) {
                    document.querySelectorAll('.increment-column-container').forEach(function(c) { c.style.outline = ''; });
                }
            }
            
            if (target && target.classList.contains('story-node') && draggedNode) {


                if (draggedNode.fromIncrement) {
                    let unallocCheck = target;
                    while (unallocCheck && !unallocCheck.classList.contains('unallocated-column')) unallocCheck = unallocCheck.parentElement;
                    if (unallocCheck && unallocCheck.classList.contains('unallocated-column')) {
                        e.preventDefault();
                        e.dataTransfer.dropEffect = 'move';
                        removeDropIndicator();
                        document.querySelectorAll('.increment-column-container').forEach(function(c) { c.style.outline = ''; });
                        unallocCheck.style.outline = '2px dashed rgb(255, 140, 0)';
                        return;
                    }
                }

                const targetType = target.getAttribute('data-node-type');
                const targetPath = target.getAttribute('data-path');
                const targetName = target.getAttribute('data-node-name');
                

                if (draggedNode.path === targetPath) {
                    removeDropIndicator();
                    return;
                }
                

                const canContain = (targetType === 'epic' && draggedNode.type === 'sub-epic') ||
                                  (targetType === 'sub-epic' && (draggedNode.type === 'sub-epic' || draggedNode.type === 'story')) ||
                                  (targetType === 'story' && draggedNode.type === 'scenario');
                

                const sameType = draggedNode.type === targetType;
                
                if (canContain || sameType) {
                    e.preventDefault();
                    e.dataTransfer.dropEffect = 'move';
                    

                    const rect = target.getBoundingClientRect();
                    const mouseY = e.clientY;
                    const targetTop = rect.top;
                    const targetHeight = rect.height;
                    const relativeY = mouseY - targetTop;
                    const percentY = relativeY / targetHeight;
                    

                    let dropZone;
                    const indicator = createDropIndicator();
                    

                    const hasStories = target.getAttribute('data-has-stories') === 'true';
                    const hasNestedSubEpics = target.getAttribute('data-has-nested-sub-epics') === 'true';
                    const isEmptyContainer = !hasStories && !hasNestedSubEpics;
                    



                    if (canContain && percentY >= 0.2 && percentY <= 0.8) {

                        dropZone = 'inside';
                        target.style.backgroundColor = 'rgba(255, 140, 0, 0.3)';
                        indicator.style.display = 'none';
                        if (dragoverLogCounter % 20 === 0) {
                            vscode.postMessage({
                                command: 'logToFile',
                                message: '[WebView] DRAGOVER ON (inside) - will nest inside ' + target.getAttribute('data-node-name')
                            });
                        }
                    } else if (sameType) {

                        dropZone = 'after';
                        target.style.backgroundColor = '';
                        indicator.style.display = 'block';
                        indicator.style.left = rect.left + 'px';
                        indicator.style.top = (rect.top + rect.height) + 'px';
                        indicator.style.width = rect.width + 'px';

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
                if (draggedNode && draggedNode.type === 'story') {

                    let incTarget = e.target;
                    let d = 8;
                    while (incTarget && d-- > 0 && !incTarget.classList.contains('increment-column-container')) {
                        incTarget = incTarget.parentElement;
                    }

                    let unallocTarget = e.target;
                    let d2 = 8;
                    while (unallocTarget && d2-- > 0 && !unallocTarget.classList.contains('unallocated-column')) {
                        unallocTarget = unallocTarget.parentElement;
                    }

                    document.querySelectorAll('.increment-column-container').forEach(function(c) { c.style.outline = ''; });
                    var unallocEl = document.querySelector('.unallocated-column');
                    if (unallocEl) unallocEl.style.outline = '';

                    if (incTarget && incTarget.classList.contains('increment-column-container')) {
                        e.preventDefault();
                        e.dataTransfer.dropEffect = 'move';
                        incTarget.style.outline = '2px solid rgb(255, 140, 0)';
                    } else if (unallocTarget && unallocTarget.classList.contains('unallocated-column') && draggedNode.fromIncrement) {

                        e.preventDefault();
                        e.dataTransfer.dropEffect = 'move';
                        unallocTarget.style.outline = '2px dashed rgb(255, 140, 0)';
                    }
                }
            }
        }, true);
        
        document.addEventListener('dragleave', function(e) {

            let target = e.target;
            while (target && !target.classList.contains('story-node')) {
                target = target.parentElement;
            }
            
            if (target && target.classList.contains('story-node')) {
                target.style.backgroundColor = '';
            }

            let incTarget = e.target;
            let d = 8;
            while (incTarget && d-- > 0 && !incTarget.classList.contains('increment-column-container')) {
                incTarget = incTarget.parentElement;
            }
            if (incTarget && incTarget.classList.contains('increment-column-container')) {
                incTarget.style.outline = '';
            }
            let unallocTarget = e.target;
            let d2 = 8;
            while (unallocTarget && d2-- > 0 && !unallocTarget.classList.contains('unallocated-column')) {
                unallocTarget = unallocTarget.parentElement;
            }
            if (unallocTarget && unallocTarget.classList.contains('unallocated-column')) {
                unallocTarget.style.outline = '';
            }
        }, true);
        
        document.addEventListener('drop', function(e) {
            console.log('[WebView] ===== DROP EVENT FIRED =====');



            var transferData = '';
            try { transferData = e.dataTransfer.getData('text/plain') || ''; } catch(_) {}
            var isIncrementDrag = transferData.startsWith('increment:');
            var incDragName = isIncrementDrag ? transferData.slice('increment:'.length) : (draggedIncrement || '');

            if (isIncrementDrag || draggedIncrement) {
                e.preventDefault();

                let col = e.target;
                let d = 10;
                while (col && d-- > 0 && !col.classList.contains('increment-column-container')) col = col.parentElement;
                if (col) {
                    const targetName = col.getAttribute('data-inc');
                    if (targetName && targetName !== incDragName) {
                        const rect = col.getBoundingClientRect();
                        const isLeft = e.clientX < rect.left + rect.width / 2;
                        const cmd = isLeft
                            ? 'story_graph.reorder_increment increment_name:"' + incDragName + '" before:"' + targetName + '"'
                            : 'story_graph.reorder_increment increment_name:"' + incDragName + '" after:"' + targetName + '"';
                        vscode.postMessage({ command: 'logToFile', message: '[INCREMENT] Reorder: ' + cmd });
                        _incCmd(cmd);
                    }
                }
                if (incrementDropTarget) { incrementDropTarget.style.outline = ''; incrementDropTarget = null; }
                removeDropIndicator();
                draggedIncrement = null;
                return;
            }

            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] ===== DROP EVENT FIRED ===== draggedNode: ' + (draggedNode ? draggedNode.name : 'null') + ', currentDropZone: ' + (currentDropZone || 'null')
            });
            

            let target = e.target;
            while (target && !target.classList.contains('story-node')) {
                target = target.parentElement;
            }
            
            if (target && target.classList.contains('story-node') && draggedNode && currentDropZone) {



                const targetIncSource = target.getAttribute('data-inc-source');
                if (draggedNode.fromIncrement !== null && draggedNode.fromIncrement !== undefined && targetIncSource !== null) {
                    e.preventDefault();
                    removeDropIndicator();
                    document.querySelectorAll('.increment-column-container').forEach(function(c) { c.style.outline = ''; });
                    var unallocEl2 = document.querySelector('.unallocated-column');
                    if (unallocEl2) unallocEl2.style.outline = '';

                    let incCol = target;
                    while (incCol && !incCol.classList.contains('increment-column-container') && !incCol.classList.contains('unallocated-column')) {
                        incCol = incCol.parentElement;
                    }
                    const draggedName = draggedNode.name;
                    const sourceInc = draggedNode.fromIncrement;

                    if (incCol && incCol.classList.contains('unallocated-column')) {

                        if (sourceInc) window.removeStoryFromIncrement(sourceInc, draggedName);
                    } else {
                        const incName = incCol ? incCol.getAttribute('data-inc') : null;
                        if (incName && sourceInc === incName) {

                            const targetPos = parseInt(target.getAttribute('data-position') || '0');
                            const rect = target.getBoundingClientRect();
                            const insertPos = e.clientY < rect.top + rect.height / 2 ? targetPos : targetPos + 1;
                            _incCmd('story_graph.reorder_story_in_increment increment_name:"' + incName + '" story_name:"' + draggedName + '" position:' + insertPos);
                        } else if (incName && sourceInc !== incName) {

                            const dropPos = _incrementDropPosition(incCol, e.clientY);
                            if (sourceInc) window.removeStoryFromIncrement(sourceInc, draggedName);
                            window.addStoryToIncrement(incName, draggedName, dropPos);
                        }
                    }
                    draggedNode = null;
                    return;
                }


                if (draggedNode.fromIncrement !== null && draggedNode.fromIncrement !== undefined) {
                    let unallocCheck = target;
                    while (unallocCheck && !unallocCheck.classList.contains('unallocated-column')) unallocCheck = unallocCheck.parentElement;
                    if (unallocCheck && unallocCheck.classList.contains('unallocated-column') && draggedNode.fromIncrement) {
                        e.preventDefault();
                        removeDropIndicator();
                        document.querySelectorAll('.increment-column-container').forEach(function(c) { c.style.outline = ''; });
                        var unallocEl3 = document.querySelector('.unallocated-column');
                        if (unallocEl3) unallocEl3.style.outline = '';
                        window.removeStoryFromIncrement(draggedNode.fromIncrement, draggedNode.name);
                        draggedNode = null;
                        return;
                    }
                }

                e.preventDefault();
                e.stopPropagation();
                target.style.backgroundColor = '';
                

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
                    

                    console.log('[WebView] Move operation - waiting for backend and full refresh');
                    
                    let command;
                    
                    vscode.postMessage({
                        command: 'logToFile',
                        message: '[WebView] COMMAND CONSTRUCTION - dropZone: ' + dropZone
                    });
                    
                    if (dropZone === 'inside') {



                        var targetForCommand = targetPath.replace(/^story_graph\./, '');


                        command = draggedNode.path + '.move_to target:' + targetForCommand;
                        vscode.postMessage({
                            command: 'logToFile',
                            message: '[WebView] INSIDE COMMAND - targetPath: ' + targetPath + ', targetForCommand: ' + targetForCommand + ', command: ' + command
                        });
                    } else if (dropZone === 'after') {
                        var targetPos = parseInt(target.getAttribute('data-position') || '0');
                        var draggedPos = draggedNode.position;
                        



                        var parentMatch = targetPath.match(/(.*)\."[^"]+"/);
                        var parentPath = parentMatch ? parentMatch[1] : 'story_graph';
                        

                        var targetForCommand = parentPath.replace(/^story_graph\./, '');
                        
                        vscode.postMessage({
                            command: 'logToFile',
                            message: '[WebView] AFTER CALCULATION - targetPos: ' + targetPos + ', draggedPos: ' + draggedPos + ', parentPath: ' + parentPath + ', targetForCommand: ' + targetForCommand
                        });
                        


                        var finalPos = (draggedPos < targetPos) ? targetPos : (targetPos + 1);
                        
                        command = draggedNode.path + '.move_to target:' + targetForCommand + ' at_position:' + finalPos;
                        vscode.postMessage({
                            command: 'logToFile',
                            message: '[WebView] AFTER COMMAND - dragged from ' + draggedPos + ' to position: ' + finalPos + ' (target was at ' + targetPos + '), command: ' + command
                        });
                    }
                    


                    if (dropZone === 'after' && typeof window.handleMoveNode === 'function') {

                        var parentMatch = targetPath.match(/(.*)\."[^"]+"/);
                        var parentPath = parentMatch ? parentMatch[1] : 'story_graph';
                        var finalPos = (draggedNode.position < targetPos) ? targetPos : (targetPos + 1);
                        

                        window.handleMoveNode({
                            sourceNodePath: draggedNode.path,
                            targetParentPath: parentPath,
                            targetNodePath: targetPath,
                            position: finalPos,
                            dropZone: 'after'
                        });
                    } else if (dropZone === 'inside' && typeof window.handleMoveNode === 'function') {

                        window.handleMoveNode({
                            sourceNodePath: draggedNode.path,
                            targetParentPath: targetPath,
                            position: 0,
                            dropZone: 'inside'
                        });
                    } else {

                        console.warn('[WebView] handleMoveNode not available, sending command directly');
                        vscode.postMessage({
                            command: 'executeCommand',
                            commandText: command

                        });
                    }
                } else {
                    vscode.postMessage({
                        command: 'logToFile',
                        message: '[WebView] DROP ignored - same node'
                    });
                }
            } else if (draggedNode && draggedNode.type === 'story') {
                function _clearIncrementHighlights() {
                    document.querySelectorAll('.increment-column-container').forEach(function(c) { c.style.outline = ''; });
                    var ua = document.querySelector('.unallocated-column');
                    if (ua) ua.style.outline = '';
                }


                var incTarget = e.target;
                var maxDepth = 8;
                while (incTarget && maxDepth-- > 0) {
                    if (incTarget.classList && (incTarget.classList.contains('increment-column-container') || incTarget.classList.contains('unallocated-column'))) break;
                    incTarget = incTarget.parentElement;
                }

                if (incTarget && incTarget.classList.contains('unallocated-column') && draggedNode.fromIncrement) {

                    e.preventDefault();
                    removeDropIndicator();
                    _clearIncrementHighlights();
                    var storyName = draggedNode.name;
                    var sourceInc = draggedNode.fromIncrement;
                    console.log('[INCREMENT] DROP story onto unallocated (remove from increment):', storyName, 'from:', sourceInc);
                    vscode.postMessage({ command: 'logToFile', message: '[INCREMENT] Drop to unallocated: ' + storyName + ' from:' + sourceInc });
                    window.removeStoryFromIncrement(sourceInc, storyName);
                    draggedNode = null;
                } else if (incTarget && incTarget.classList.contains('increment-column-container')) {
                    e.preventDefault();
                    removeDropIndicator();
                    _clearIncrementHighlights();
                    var incName = incTarget.getAttribute('data-inc');
                    var storyName = draggedNode.name;
                    var sourceInc = draggedNode.fromIncrement;
                    console.log('[INCREMENT] DROP story onto increment:', storyName, '->', incName, '(from:', sourceInc, ')');
                    vscode.postMessage({ command: 'logToFile', message: '[INCREMENT] Drop: ' + storyName + ' -> ' + incName + ' from:' + sourceInc });
                    var dropPos = _incrementDropPosition(incTarget, e.clientY);
                    if (sourceInc && sourceInc !== incName) {

                        window.removeStoryFromIncrement(sourceInc, storyName);
                        window.addStoryToIncrement(incName, storyName, dropPos);
                    } else if (sourceInc !== null) {

                        window.addStoryToIncrement(incName, storyName, dropPos);
                    } else {

                        window.addStoryToIncrement(incName, storyName, dropPos);
                    }
                    draggedNode = null;
                }
            } else {
                removeDropIndicator();
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] DROP ignored - not story-node, no draggedNode, or no dropZone'
                });
            }
        }, true);
        

        window.testFunction = function() {
            console.log('[WebView] TEST FUNCTION CALLED - functions are accessible!');
            alert('Test function works!');
        };
        console.log('[WebView] window.testFunction defined:', typeof window.testFunction);
        

        window.hidePanel = function() {\n            console.log('[hidePanel] Requesting panel collapse');\n            vscode.postMessage({ command: 'hidePanel' });\n        };\n        \n        window.toggleSection = function(sectionId) {
            console.log('[toggleSection] Called with sectionId:', sectionId);
            const content = document.getElementById(sectionId);
            console.log('[toggleSection] Content element:', content);
            if (content) {
                const section = content.closest('.collapsible-section');
                console.log('[toggleSection] Parent section:', section);
                const isExpanded = section && section.classList.contains('expanded');
                console.log('[toggleSection] isExpanded:', isExpanded);
                

                if (isExpanded) {

                    content.style.maxHeight = '0px';
                    content.style.overflow = 'hidden';
                    content.style.display = 'none';
                } else {

                    content.style.maxHeight = '2000px';
                    content.style.overflow = 'visible';
                    content.style.display = 'block';

                    if (content.querySelector('[id^="clarify-answer-"]')) {
                        setTimeout(() => { if (window.expandClarifyBoxes) window.expandClarifyBoxes(); }, 50);
                    }
                }
                

                const header = content.previousElementSibling;
                console.log('[toggleSection] Header element:', header);
                if (header && section) {
                    section.classList.toggle('expanded', !isExpanded);
                    console.log('[toggleSection] After toggle, section classes:', section.className);

                    const icon = header.querySelector('.expand-icon');
                    console.log('[toggleSection] Icon element:', icon);
                    if (icon) {
                        icon.textContent = '▸';
                        console.log('[toggleSection] Icon transform:', window.getComputedStyle(icon).transform);
                    }
                }

                if (sectionId === 'scope-content' && typeof vscode !== 'undefined') {
                    vscode.postMessage({ command: 'sectionExpansion', sectionId: sectionId, expanded: !isExpanded });
                }
            }
        };
        


        window.expandInstructionsSection = function(actionName) {
            console.log('[expandInstructionsSection] Called with actionName:', actionName);
            if (!actionName) return;
            

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
            

            document.querySelectorAll('[id^="instr-section-"]').forEach(content => {
                const section = content.closest('.collapsible-section');
                if (section) {
                    content.style.maxHeight = '0px';
                    content.style.overflow = 'hidden';
                    content.style.display = 'none';
                    section.classList.remove('expanded');
                }
            });
            

            const headers = document.querySelectorAll('.collapsible-header');
            for (const header of headers) {
                const headerText = header.textContent || '';

                if (headerText.includes(sectionName) && !headerText.includes('Base')) {
                    const section = header.closest('.collapsible-section');
                    const content = header.nextElementSibling;
                    
                    if (section && content && content.classList.contains('collapsible-content')) {
                        console.log('[expandInstructionsSection] Expanding section:', sectionName);

                        content.style.maxHeight = '2000px';
                        content.style.overflow = 'visible';
                        content.style.display = 'block';
                        section.classList.add('expanded');
                        

                        if (sectionName === 'Clarify' && content.querySelector('[id^="clarify-answer-"]')) {
                            setTimeout(() => { if (window.expandClarifyBoxes) window.expandClarifyBoxes(); }, 50);
                        }
                        

                        const icon = header.querySelector('.expand-icon');
                        if (icon) {
                            icon.textContent = '▸';
                        }
                        return;
                    }
                }
            }
            console.log('[expandInstructionsSection] Section not found for:', sectionName);
        };
        

        window.getCollapseState = function() {
            const state = {};
            document.querySelectorAll('.collapsible-content').forEach(content => {
                if (content.id) {
                    state[content.id] = content.style.display !== 'none';
                }
            });
            document.querySelectorAll('.execution-toggle-container').forEach(container => {
                if (container.id) {
                    state[container.id] = container.classList.contains('expanded');
                }
            });
            return state;
        };
        
        window.restoreCollapseState = function(state) {
            if (!state) return;
            Object.keys(state).forEach(id => {
                const el = document.getElementById(id);
                if (!el) return;
                const shouldBeExpanded = state[id];
                if (el.classList && el.classList.contains('execution-toggle-container')) {
                    if (shouldBeExpanded) {
                        el.classList.add('expanded');
                    } else {
                        el.classList.remove('expanded');
                    }
                } else if (el.classList && el.classList.contains('collapsible-content')) {
                    el.style.display = shouldBeExpanded ? 'block' : 'none';
                    const header = el.previousElementSibling;
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
        
        window.toggleExecutionToggle = function(containerId) {
            const container = document.getElementById(containerId);
            if (container && container.classList.contains('execution-toggle-container')) {
                container.classList.toggle('expanded');
                const currentState = window.getCollapseState();
                sessionStorage.setItem('collapseState', JSON.stringify(currentState));
            }
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

                        const plusSrc = icon.getAttribute('data-plus');
                        const subtractSrc = icon.getAttribute('data-subtract');
                        if (plusSrc && subtractSrc) {
                            const img = icon.querySelector('img');
                            if (img) {
                                img.src = isHidden ? subtractSrc : plusSrc;
                            } else {

                                const imgSrc = isHidden ? subtractSrc : plusSrc;
                                const imgAlt = isHidden ? 'Collapse' : 'Expand';
                                icon.innerHTML = '<img src="' + imgSrc + '" style="width: 12px; height: 12px; vertical-align: middle;" alt="' + imgAlt + '" />';
                            }
                        }
                    }
                }
                

                const currentState = window.getCollapseState();
                sessionStorage.setItem('collapseState', JSON.stringify(currentState));
            }
        };
        
        window.openFile = function(filePath, event) {

            if (event) {
                event.preventDefault();
                event.stopPropagation();
            }



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
        

        console.log('[WebView] updateFilter function exists:', typeof updateFilter);
        
        window.updateIncludeLevel = function(level) {
            console.log('[WebView] updateIncludeLevel called with:', level);
            vscode.postMessage({
                command: 'updateIncludeLevel',
                includeLevel: level
            });
        };
        
        window.clearScopeFilter = function(viewMode) {
            vscode.postMessage({
                command: 'clearScopeFilter',
                viewMode: viewMode || null
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
        
        window.setBehaviorSpecialInstructions = function(textareaEl) {
            if (!textareaEl || textareaEl.tagName !== 'TEXTAREA') return;
            const behaviorName = textareaEl.getAttribute('data-behavior-name');
            const instructionText = (textareaEl.value || '').trim();
            if (behaviorName !== null) {
                vscode.postMessage({
                    command: 'setBehaviorSpecialInstructions',
                    behaviorName: behaviorName,
                    instructionText: instructionText
                });
            }
        };
        
        window.setActionSpecialInstructions = function(textareaEl) {
            if (!textareaEl || textareaEl.tagName !== 'TEXTAREA') return;
            const behaviorName = textareaEl.getAttribute('data-behavior-name');
            const actionName = textareaEl.getAttribute('data-action-name');
            const instructionText = (textareaEl.value || '').trim();
            if (behaviorName !== null && actionName !== null) {
                vscode.postMessage({
                    command: 'setActionSpecialInstructions',
                    behaviorName: behaviorName,
                    actionName: actionName,
                    instructionText: instructionText
                });
            }
        };
        
        function submitToChat() {
            console.log('[SUBMIT_DEBUG] WebView: submitToChat() posting sendToChat');
            vscode.postMessage({
                command: 'sendToChat'
            });
        }

        function sendInstructionsToChat(event) {
            if (event) {
                event.stopPropagation();
            }
            console.log('[SUBMIT_DEBUG] WebView: sendInstructionsToChat triggered');

            if (window.selectedNode && window.selectedNode.name) {
                const nodePath = resolveNodePath(window.selectedNode);
                if (nodePath) {
                    console.log('[SUBMIT_DEBUG] WebView: taking handleSubmitCurrent path (story map node selected)');
                    handleSubmitCurrent();
                    return;
                }
            }

            console.log('[SUBMIT_DEBUG] WebView: taking submitToChat path (behaviors submit)');
            submitToChat();
        }

        function refreshStatus() {
            vscode.postMessage({
                command: 'refresh'
            });
        }
        

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
        

        function applyOptimisticMove(draggedNodeElement, targetElement, dropZone, finalPosition) {
            var draggedNodeName = draggedNodeElement ? draggedNodeElement.getAttribute('data-node-name') : null;
            var targetNodeName = targetElement ? targetElement.getAttribute('data-node-name') : null;
            console.log('[ASYNC_SAVE] [OPTIMISTIC] applyOptimisticMove() called dropZone=' + dropZone + ' finalPosition=' + finalPosition + ' draggedNode=' + draggedNodeName + ' targetNode=' + targetNodeName + ' timestamp=' + new Date().toISOString());
            
            if (!draggedNodeElement || !targetElement) {
                console.error('[ASYNC_SAVE] [OPTIMISTIC] [ERROR] Cannot apply optimistic move - missing elements hasDraggedElement=' + !!draggedNodeElement + ' hasTargetElement=' + !!targetElement);
                return;
            }
            

            const draggedParent = draggedNodeElement.parentElement;
            const targetParent = dropZone === 'inside' ? targetElement : targetElement.parentElement;
            
            console.log('[ASYNC_SAVE] [OPTIMISTIC] Found parent elements hasDraggedParent=' + !!draggedParent + ' hasTargetParent=' + !!targetParent + ' sameParent=' + (draggedParent === targetParent));
            
            if (!draggedParent || !targetParent) {
                console.error('[ASYNC_SAVE] [OPTIMISTIC] [ERROR] Cannot apply optimistic move - missing parent elements');
                return;
            }
            

            if (draggedParent === targetParent && dropZone === 'after') {
                const targetPos = parseInt(targetElement.getAttribute('data-position') || '0');
                const draggedPos = parseInt(draggedNodeElement.getAttribute('data-position') || '0');
                
                console.log('[ASYNC_SAVE] [OPTIMISTIC] Moving within same parent draggedPos=' + draggedPos + ' targetPos=' + targetPos + ' finalPosition=' + finalPosition + ' dropZone=' + dropZone);
                

                const draggedClone = draggedNodeElement.cloneNode(true);
                draggedNodeElement.remove();
                console.log('[ASYNC_SAVE] [OPTIMISTIC] Removed dragged node from original position');
                

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
                

                updateNodePositions(targetParent);
                
                console.log('[ASYNC_SAVE] [OPTIMISTIC] [SUCCESS] Optimistic move applied - node moved in DOM');
            } else if (dropZone === 'inside') {

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
        

        window.createEpic = function() {
            console.log('═══════════════════════════════════════════════════════');
            console.log('[WebView] createEpic CALLED');
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] createEpic called'
            });
            

            if (typeof window.handleCreateNode === 'function') {
                console.log('[WebView] Using optimistic create handler');
                window.handleCreateNode({
                    parentPath: 'story_graph',
                    nodeType: 'epic'

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
        
        function _incCmd(commandText) {
            console.log('[INCREMENT] >>> Sending command:', commandText);
            vscode.postMessage({ command: 'logToFile', message: '[INCREMENT][UI->CLI] ' + commandText });
            vscode.postMessage({ command: 'executeCommand', commandText: commandText });
        }

        function _applyIncrementCollapse(col, collapse) {
            var body = col.querySelector('.increment-stories-body');
            var btn = col.querySelector('button[title="Collapse / expand"]');
            if (collapse) {
                col.setAttribute('data-collapsed', 'true');
                col.style.minWidth = '28px';
                col.style.maxWidth = '28px';
                col.style.overflowY = 'hidden';
                if (body) body.style.display = 'none';
                if (btn) btn.textContent = '▶';
            } else {
                col.setAttribute('data-collapsed', 'false');
                col.style.minWidth = '160px';
                col.style.maxWidth = '200px';
                col.style.overflowY = 'auto';
                if (body) body.style.display = 'flex';
                if (btn) btn.textContent = '▼';
            }
        }

        window.toggleIncrementCollapse = function(col) {
            if (!col) return;
            var incName = col.getAttribute('data-inc');
            var collapsed = col.getAttribute('data-collapsed') === 'true';
            _applyIncrementCollapse(col, !collapsed);

            try {
                var state = vscode.getState() || {};
                if (!state.collapsedIncrements) state.collapsedIncrements = {};
                if (!collapsed) {
                    state.collapsedIncrements[incName] = true;
                } else {
                    delete state.collapsedIncrements[incName];
                }
                vscode.setState(state);
            } catch(_) {}
        };


        (function restoreIncrementCollapseState() {
            try {
                var state = vscode.getState() || {};
                var collapsed = state.collapsedIncrements || {};
                Object.keys(collapsed).forEach(function(incName) {
                    var col = document.querySelector('.increment-column-container[data-inc="' + incName + '"]');
                    if (col) _applyIncrementCollapse(col, true);
                });
            } catch(_) {}
        })();

        window.selectIncrement = function(name, behaviorNeeded) {
            window.selectNode('increment', name, { name: name, path: 'story_graph.increments."' + name + '"', behavior: behaviorNeeded || 'shape' });
            document.querySelectorAll('.increment-column-container').forEach(function(col) {
                col.classList.toggle('selected', col.getAttribute('data-inc') === name);
            });
        };

        window.addIncrement = function() {
            var wrapper = document.querySelector('.increment-columns-wrapper');
            if (!wrapper) { console.error('[INCREMENT] Cannot find .increment-columns-wrapper'); return; }


            var selectedCol = wrapper.querySelector('.increment-column-container.selected');

            var col = document.createElement('div');
            col.className = 'increment-column-container selected';
            col.style.cssText = 'min-width:160px;max-width:200px;flex-shrink:0;border-right:1px solid var(--text-color-faded,#444);padding:8px;display:flex;flex-direction:column;border-top:2px solid var(--accent-color);';
            col.innerHTML = '<div style="display:flex;align-items:center;gap:4px;margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid var(--text-color-faded,#555);">' +
                '<span contenteditable="true" style="flex:1;font-weight:600;font-size:12px;outline:none;min-width:0;color:var(--accent-color);">New Increment</span></div>' +
                '<div style="font-size:11px;color:var(--text-color-faded);font-style:italic;">(no stories)</div>';

            if (selectedCol) {
                selectedCol.insertAdjacentElement('afterend', col);
            } else {
                wrapper.appendChild(col);
            }

            var span = col.querySelector('span[contenteditable]');
            span.focus();
            document.execCommand('selectAll', false, null);

            var committed = false;
            function commit() {
                if (committed) return;
                committed = true;
                var name = span.innerText.trim();
                if (!name || name === 'New Increment') { col.remove(); return; }

                span.contentEditable = 'false';
                span.style.color = '';
                col.style.borderTop = '';
                col.style.opacity = '0.6';
                var afterName = selectedCol ? selectedCol.getAttribute('data-inc') : null;
                _incCmd('story_graph.add_increment name:"' + name + '"' + (afterName ? ' after:"' + afterName + '"' : ''));
            }

            span.addEventListener('blur', commit, { once: true });
            span.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') { e.preventDefault(); span.blur(); }
                if (e.key === 'Escape') { span.innerText = ''; span.blur(); }
            });
        };


        window.deleteIncrement = function(incrementName) {
            var col = document.querySelector('.increment-column-container[data-inc="' + incrementName + '"]');
            if (col) col.remove();
            _incCmd('story_graph.remove_increment increment_name:"' + incrementName + '"');
        };


        window.renameIncrement = function(el, oldName) {
            var newName = el.innerText.trim();
            if (!newName || newName === oldName) { el.innerText = oldName; return; }
            el.setAttribute('data-increment-name', newName);
            el.closest('.increment-column-container').setAttribute('data-inc', newName);
            _incCmd('story_graph.rename_increment from_name:"' + oldName + '" to_name:"' + newName + '"');
        };


        window.removeStoryFromIncrement = function(incrementName, storyName) {
            var col = document.querySelector('.increment-column-container[data-inc="' + incrementName + '"]');
            if (col) {
                col.querySelectorAll('[data-story]').forEach(function(row) {
                    if (row.getAttribute('data-story') === storyName) row.closest('div').remove();
                });
            }
            _incCmd('story_graph.remove_story_from_increment increment_name:"' + incrementName + '" story_name:"' + storyName + '"');
        };




        function _incrementDropPosition(incColEl, mouseY) {
            if (mouseY === undefined || mouseY === null || !incColEl) return undefined;
            var rows = Array.from(incColEl.querySelectorAll('.story-node[data-inc-source]'));
            if (!rows.length) return 0;
            for (var i = 0; i < rows.length; i++) {
                var rect = rows[i].getBoundingClientRect();
                var mid = rect.top + rect.height / 2;
                if (mouseY < mid) return i;
            }
            return rows.length;
        }



        window.addStoryToIncrement = function(incrementName, storyName, position) {
            var cmd = 'story_graph.add_story_to_increment increment_name:"' + incrementName + '" story_name:"' + storyName + '"';
            if (position !== undefined && position !== null) cmd += ' position:' + position;
            _incCmd(cmd);
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
            

            if (typeof window.handleDeleteNode === 'function') {
                console.log('[WebView] Using optimistic delete handler');
                window.handleDeleteNode({
                    nodePath: nodePath
                });
            } else {
                console.warn('[WebView] handleDeleteNode not available, falling back to direct command');

                vscode.postMessage({
                    command: 'executeCommand',
                    commandText: nodePath + '.delete'

                });
            }
        };
        
        window.deleteNodeIncludingChildren = function(nodePath) {
            console.log('[WebView] deleteNodeIncludingChildren called for:', nodePath);
            


            if (typeof window.handleDeleteNode === 'function') {
                console.log('[WebView] Using optimistic delete handler (always includes children)');
                window.handleDeleteNode({
                    nodePath: nodePath
                });
            } else {
                console.warn('[WebView] handleDeleteNode not available, falling back to direct command');


                vscode.postMessage({
                    command: 'executeCommand',
                    commandText: nodePath + '.delete()'

                });
            }
        };
        
        window.enableEditMode = function(nodePath) {
            console.log('[ASYNC_SAVE] ========== RENAME OPERATION START ==========');
            console.log('[ASYNC_SAVE] [USER_ACTION] User double-clicked node to rename nodePath=' + nodePath + ' timestamp=' + new Date().toISOString());


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
        

        window.selectedNode = {
            type: 'root',
            name: null,
            path: null,
            canHaveSubEpic: false,
            canHaveStory: false,
            canHaveTests: false,
            hasChildren: false,
            hasStories: false,
            hasNestedSubEpics: false
        };
        

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
            

            if (window.selectedNode.type === 'root') {
                if (btnCreateEpic) btnCreateEpic.style.display = 'block';
            } else if (window.selectedNode.type === 'epic') {
                if (btnCreateSubEpic) btnCreateSubEpic.style.display = 'block';
                if (btnDelete) btnDelete.style.display = 'block';
                if (btnScopeTo) btnScopeTo.style.display = 'block';
            } else if (window.selectedNode.type === 'sub-epic') {




                if (window.selectedNode.hasStories) {

                    if (btnCreateStory) btnCreateStory.style.display = 'block';
                } else if (window.selectedNode.hasNestedSubEpics) {

                    if (btnCreateSubEpic) btnCreateSubEpic.style.display = 'block';
                } else {

                    if (btnCreateSubEpic) btnCreateSubEpic.style.display = 'block';
                    if (btnCreateStory) btnCreateStory.style.display = 'block';
                }
                if (btnDelete) btnDelete.style.display = 'block';
                if (btnScopeTo) btnScopeTo.style.display = 'block';
            } else if (window.selectedNode.type === 'story') {

                if (btnCreateScenario) btnCreateScenario.style.display = 'block';
                if (btnCreateAcceptanceCriteria) btnCreateAcceptanceCriteria.style.display = 'block';
                if (btnDelete) btnDelete.style.display = 'block';
                if (btnScopeTo) btnScopeTo.style.display = 'block';
            } else if (window.selectedNode.type === 'scenario') {

                if (btnDelete) btnDelete.style.display = 'block';
                if (btnScopeTo) btnScopeTo.style.display = 'block';

            } else if (window.selectedNode.type === 'increment') {
                if (btnScopeTo) btnScopeTo.style.display = 'block';
            }
            

            if (window.selectedNode.type !== 'root') {
                if (btnOpenGraph) btnOpenGraph.style.display = 'block';
                if (btnOpenAll) btnOpenAll.style.display = 'block';
            }
            




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
            

            const requiredBehavior = window.selectedNode.behaviorNeeded;
            const currentBehavior = window.currentBehavior || window.selectedNode.behavior;
            const currentAction = window.currentAction || 'build';
            // For increments: use current behavior (no behaviorNeeded on increment nodes)
            const effectiveBehavior = window.selectedNode.type === 'increment' ? currentBehavior : requiredBehavior;
            
            if (btnSubmit && window.selectedNode.type !== 'root' && effectiveBehavior) {
                const behavior = effectiveBehavior;
                const action = currentAction;
                const nodeType = window.selectedNode.type;
                const btnSubmitIcon = document.getElementById('btn-submit-icon');
                
                console.log('[SUBMIT BUTTON DEBUG] Proceeding with button update...');
                console.log('[SUBMIT BUTTON DEBUG] btnSubmitIcon exists:', !!btnSubmitIcon);
                

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
                if (!effectiveBehavior) {
                    console.log('[SUBMIT BUTTON DEBUG] ✗ No behavior for submit');
                    if (window.selectedNode.type === 'increment') {
                        console.log('[SUBMIT BUTTON DEBUG]   Increment needs current behavior from bot');
                    } else {
                        console.log('[SUBMIT BUTTON DEBUG]   behavior_needed may not be set on node');
                    }
                }
            }
            

            const btnSubmitAlt = document.getElementById('btn-submit-alt');
            const behaviorsNeeded = window.selectedNode.behaviorsNeeded || [];
            console.log('[SUBMIT BUTTON DEBUG] behaviorsNeeded:', behaviorsNeeded);
            
            if (btnSubmitAlt && behaviorsNeeded.length > 1 && window.selectedNode.type !== 'root') {
                const altBehavior = behaviorsNeeded[1];
                const nodeType = window.selectedNode.type;
                const btnSubmitAltIcon = document.getElementById('btn-submit-alt-icon');
                

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

                    btnSubmitAlt.setAttribute('data-current-behavior', altBehavior);
                    console.log('[SUBMIT BUTTON DEBUG] Alt button shown for behavior:', altBehavior);
                } else {
                    btnSubmitAlt.style.display = 'none';
                }
            } else if (btnSubmitAlt) {
                btnSubmitAlt.style.display = 'none';
            }
            
            console.log('═══════════════════════════════════════════════════════');
        };
        

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
            

            document.querySelectorAll('.story-node.selected').forEach(node => {
                node.classList.remove('selected');
            });
            document.querySelectorAll('.increment-column-container.selected').forEach(col => {
                col.classList.remove('selected');
            });
            

            let targetNode = null;
            

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
            

            const behavior = window.currentBehavior || options.behavior || null;
            const behaviors = options.behaviors || (options.behavior ? [options.behavior] : []);
            
            window.selectedNode = {
                type: type,
                name: name,
                path: options.path || null,
                behavior: behavior,
                behaviorNeeded: options.behavior || null,
                behaviorsNeeded: behaviors,
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
            

            try {
                sessionStorage.setItem('selectedNode', JSON.stringify(window.selectedNode));
            } catch (err) {
                console.error('[WebView] Error saving selection:', err);
            }
            
            window.updateContextualButtons();
            console.log('[WebView]   updateContextualButtons called');
            console.log('═══════════════════════════════════════════════════════');
        };
        

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
            

            const hasValidPath = window.selectedNode.path && 
                                window.selectedNode.path.length > 'story_graph.'.length &&
                                window.selectedNode.path.includes(window.selectedNode.name);
            
            console.log('[WebView]   path:', window.selectedNode.path);
            console.log('[WebView]   hasValidPath:', hasValidPath);
            

            if (typeof window.handleCreateNode === 'function') {
                var parentPath = hasValidPath ? window.selectedNode.path : \`story_graph."\${window.selectedNode.name}"\`;
                
                console.log('[WebView] Using optimistic create handler for:', actionType);
                window.handleCreateNode({
                    parentPath: parentPath,
                    nodeType: actionType

                });
            } else {
                console.warn('[WebView] handleCreateNode not available, falling back to direct command');

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
        

        window.handleDelete = function() {
            console.log('[WebView] handleDelete called for node:', window.selectedNode);
            
            if (!window.selectedNode || !window.selectedNode.name) {
                console.error('[WebView] ERROR: No node selected for delete');
                return;
            }
            

            let nodePath = window.selectedNode.path;
            if (!nodePath || nodePath.length <= 'story_graph.'.length) {

                nodePath = \`story_graph."\${window.selectedNode.name}"\`;
            }
            
            console.log('[WebView] Calling handleDeleteNode with path:', nodePath);
            


            if (typeof window.handleDeleteNode === 'function') {
                window.handleDeleteNode({
                    nodePath: nodePath
                });
            } else {
                console.warn('[WebView] handleDeleteNode not available, falling back to direct command');


                const commandText = nodePath + '.delete()';
                vscode.postMessage({
                    command: 'executeCommand',
                    commandText: commandText
                });
            }
        };
        

        window.handleScopeTo = function() {
            console.log('[WebView] handleScopeTo called for node:', window.selectedNode);
            
            if (!window.selectedNode.name) {
                console.error('[WebView] ERROR: No node selected for scope');
                return;
            }
            

            const nodeName = window.selectedNode.name;
            const nodeType = window.selectedNode.type;
            let scopeCommand;
            
            if (nodeType === 'story') {
                scopeCommand = 'story ' + nodeName;
            } else if (nodeType === 'sub-epic') {
                scopeCommand = 'subepic ' + nodeName;
            } else if (nodeType === 'epic') {
                scopeCommand = 'epic ' + nodeName;
            } else if (nodeType === 'increment') {
                scopeCommand = 'story ' + nodeName;
            } else {

                scopeCommand = nodeName;
            }
            
            console.log('[WebView] Scope To command:', scopeCommand);
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] SENDING SCOPE TO COMMAND: scope ' + scopeCommand
            });
            

            vscode.postMessage({
                command: 'executeCommand',
                commandText: 'scope ' + scopeCommand
            });
        };
        

        function resolveNodePath(selectedNode) {
            if (selectedNode.path && selectedNode.path.length > 'story_graph.'.length) {
                return selectedNode.path;
            }
            const nodes = document.querySelectorAll('.story-node[data-path]');
            for (var i = 0; i < nodes.length; i++) {
                var el = nodes[i];
                if (el.getAttribute('data-node-type') === selectedNode.type && el.getAttribute('data-node-name') === selectedNode.name) {
                    var path = el.getAttribute('data-path');
                    if (path) {
                        console.log('[WebView] Resolved path from DOM:', path);
                        selectedNode.path = path;
                        return path;
                    }
                }
            }
            return null;
        }
        
        window.handleSubmit = function() {
            console.log('[WebView] ========== handleSubmit CALLED ==========');
            vscode.postMessage({
                command: 'logScopeDebug',
                message: 'handleSubmit CALLED | selectedNode=' + JSON.stringify(window.selectedNode || null)
            });
            
            if (!window.selectedNode || !window.selectedNode.name) {
                vscode.postMessage({ command: 'logScopeDebug', message: 'ERROR: No node selected' });
                return;
            }
            
            if (!window.selectedNode.behaviorNeeded) {
                vscode.postMessage({ command: 'logScopeDebug', message: 'ERROR: No behaviorNeeded for ' + window.selectedNode.name });
                return;
            }
            
            const nodeName = window.selectedNode.name;
            const nodePath = resolveNodePath(window.selectedNode);
            
            vscode.postMessage({
                command: 'logScopeDebug',
                message: 'resolveNodePath: nodeName=' + nodeName + ' | nodePath=' + (nodePath || 'NULL') + ' | hadPath=' + !!window.selectedNode.path
            });
            
            if (!nodePath) {
                vscode.postMessage({
                    command: 'logScopeDebug',
                    message: 'ERROR: Could not resolve node path - story map may not be visible. Click the node again to refresh.'
                });
            vscode.postMessage({
                command: 'showScopeError',
                message: 'Scope not available: Could not resolve node path. Try clicking the story/epic node again, then submit.'
            });
                return;
            }
            
            const action = 'build';
            const commandText = nodePath + '.submit_required_behavior_instructions action:"' + action + '"';
            
            vscode.postMessage({
                command: 'logScopeDebug',
                message: 'SENDING COMMAND: ' + commandText
            });
            
            vscode.postMessage({
                command: 'executeCommand',
                commandText: commandText
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
            
            const altBehavior = behaviorsNeeded[1];
            const nodeName = window.selectedNode.name;
            const nodePath = resolveNodePath(window.selectedNode);
            
            if (!nodePath) {
                vscode.postMessage({ command: 'showScopeError', message: 'Scope not available: Could not resolve node path. Click the node again, then submit.' });
                return;
            }
            
            const action = 'build';
            const commandText = nodePath + '.submit_instructions behavior:"' + altBehavior + '" action:"' + action + '"';
            
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
            const behavior = window.currentBehavior || window.selectedNode.behaviorNeeded || null;
            const action = window.currentAction || 'build';
            let commandText;
            
            if (window.selectedNode.type === 'increment') {
                // Increment uses story_graph.submit_increment_instructions (Increment has no submit_instructions)
                commandText = (behavior && action)
                    ? 'story_graph.submit_increment_instructions name:"' + nodeName + '" behavior:"' + behavior + '" action:"' + action + '"'
                    : 'story_graph.submit_increment_instructions name:"' + nodeName + '"';
            } else {
                const nodePath = resolveNodePath(window.selectedNode);
                if (!nodePath) {
                    vscode.postMessage({ command: 'showScopeError', message: 'Scope not available: Could not resolve node path. Click the node again, then submit.' });
                    return;
                }
                commandText = (behavior && action)
                    ? nodePath + '.submit_instructions behavior:"' + behavior + '" action:"' + action + '"'
                    : nodePath + '.submit_current_instructions';
            }
            
            console.log('[WebView] ========== SUBMIT CURRENT COMMAND ==========');
            console.log('[WebView] Command constructed:', commandText);
            console.log('[WebView] Using panel state: behavior=' + (behavior || '(bot current)') + ' action=' + (action || '(bot current)'));
            
            vscode.postMessage({
                command: 'executeCommand',
                commandText: commandText
            });
            
            console.log('[WebView] ========== COMMAND SENT ==========');
        };
        

        function getSelectedNodeFileLink() {
            if (!window.selectedNode || !window.selectedNode.name) return null;
            const nodeElement = document.querySelector('.story-node[data-node-type="' + window.selectedNode.type + '"][data-node-name="' + window.selectedNode.name + '"]');
            return nodeElement ? nodeElement.getAttribute('data-file-link') : null;
        }
        

        function getWorkspaceDir() {

            if (window.botData && window.botData.workspace_directory) {
                return window.botData.workspace_directory;
            }

            const storyGraphPath = 'docs/story/story-graph.json';
            return '';
        }
        

        function openFileInColumn(filePath, viewColumn) {
            vscode.postMessage({
                command: 'openFileInColumn',
                filePath: filePath,
                viewColumn: viewColumn
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
            

            vscode.postMessage({
                command: 'openFileWithState',
                filePath: storyGraphPath,
                state: {
                    collapseAll: true,
                    expandPath: window.selectedNode.path || null,
                    selectedNode: window.selectedNode,
                    positionCursor: true
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


                        const parentDiv = nodeEl.closest('div');
                        const collapsibleDiv = parentDiv ? parentDiv.nextElementSibling : null;
                        
                        if (collapsibleDiv && collapsibleDiv.classList.contains('collapsible-content')) {

                            const childStoryNodes = collapsibleDiv.querySelectorAll('.story-node[data-node-type="story"]');
                            childStoryNodes.forEach(function(storyEl) {
                                const link = storyEl.getAttribute('data-file-link');
                                if (link) {
                                    storyFiles.push(link);
                                }
                            });
                            

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
            

            vscode.postMessage({
                command: 'openAllRelatedFiles',
                nodeType: window.selectedNode.type,
                nodeName: window.selectedNode.name,
                nodePath: window.selectedNode.path,
                singleFileLink: fileLink,
                storyFiles: storyFiles,
                testFiles: testFiles,
                storyGraphPath: storyGraphPath,
                selectedNode: window.selectedNode
            });
        };
        
        

        setTimeout(function() {
            window.selectNode('root', null);
        }, 100);
        

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {

                try { sessionStorage.removeItem('selectedNode'); } catch(err) {}
                window.diagramScope = '';
                window.selectNode('root', null);
            }
        });
        

        window.toggleQAExpand = function(idx) {
            const textarea = document.getElementById('clarify-answer-' + idx);
            const toggleBtn = document.getElementById('qa-toggle-' + idx);
            if (!textarea) return;
            
            const isCollapsed = textarea.getAttribute('data-collapsed') === 'true';
            const defaultHeight = 60;
            
            if (isCollapsed) {

                textarea.style.height = 'auto';
                const fullHeight = textarea.scrollHeight;
                textarea.style.height = fullHeight + 'px';
                textarea.style.overflow = 'visible';
                textarea.setAttribute('data-collapsed', 'false');
                if (toggleBtn) toggleBtn.textContent = '▲';
            } else {

                textarea.style.height = defaultHeight + 'px';
                textarea.style.overflow = 'hidden';
                textarea.setAttribute('data-collapsed', 'true');
                if (toggleBtn) toggleBtn.textContent = '▼';
            }
        };
        

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
        

        window.saveStrategyMultiDecision = function(criteriaKey, inputName) {
            console.log('[WebView] saveStrategyMultiDecision triggered:', criteriaKey, inputName);
            const checkboxes = document.querySelectorAll('input[name="' + inputName + '"]:checked');
            const selectedOptions = [];
            checkboxes.forEach(cb => {

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
        


        window.addEventListener('message', event => {
            const message = event.data;
            console.log('[WebView] Received message from extension:', message);
            
            if (message.command === 'incrementCommandResult') {
                var status = (message.result && message.result.status) ? message.result.status : 'unknown';
                console.log('[INCREMENT][CLI->UI] Response received. command=' + message.commandText + ' status=' + status + ' result=' + JSON.stringify(message.result));
                return;
            }
            
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

                const errorDiv = document.createElement('div');
                errorDiv.style.cssText = 'position: fixed; top: 10px; left: 10px; right: 10px; z-index: 10000; background: #f44336; color: white; padding: 16px; border-radius: 4px; font-family: monospace; font-size: 12px; white-space: pre-wrap; max-height: 80vh; overflow-y: auto;';
                errorDiv.textContent = '[ERROR] ' + message.error;
                

                const btnContainer = document.createElement('div');
                btnContainer.style.cssText = 'margin-top: 12px; display: flex; gap: 8px;';
                

                const retryBtn = document.createElement('button');
                retryBtn.textContent = '🔄 Retry';
                retryBtn.style.cssText = 'background: white; color: #f44336; border: none; padding: 8px 16px; cursor: pointer; border-radius: 3px; font-weight: bold;';
                retryBtn.onclick = () => {
                    errorDiv.remove();
                    vscode.postMessage({ command: 'refresh' });
                };
                

                const closeBtn = document.createElement('button');
                closeBtn.textContent = 'Close';
                closeBtn.style.cssText = 'background: rgba(255,255,255,0.8); color: #f44336; border: none; padding: 8px 16px; cursor: pointer; border-radius: 3px;';
                closeBtn.onclick = () => errorDiv.remove();
                
                btnContainer.appendChild(retryBtn);
                btnContainer.appendChild(closeBtn);
                errorDiv.appendChild(btnContainer);
                
                document.body.appendChild(errorDiv);
                

                setTimeout(() => errorDiv.remove(), 30000);
            }
            

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
            


            if (message.command === 'optimisticRename') {
                console.log('[WebView] Optimistic rename disabled - waiting for full refresh');

            }
            

            if (message.command === 'revertRename') {
                console.log('[WebView] Revert rename command received but not needed');
            }
        });
    </script>
</body>
</html>`;
  }
}


BotPanel.currentPanel = undefined;
BotPanel.viewType = "agilebot.botPanel";

module.exports = BotPanel;
