const vscode = require("vscode");
const path = require("path");
const fs = require("fs");
const { Logger } = require("../utils");

/**
 * StoryGraphManager handles routing of story graph-related messages from the webview client
 * Manages view modes, clipboard operations, and node operations
 */
class StoryGraphManager {
    
    constructor() {}

    static handleError(error, operation) {
        Logger.log(`[StoryGraphManager] ERROR ${operation}: ` + error.message);
        Logger.log(`[StoryGraphManager] ERROR stack: ` + error.stack);
        vscode.window.showErrorMessage(`Failed to ${operation}: ${error.message}`);
    }

    /**
     * Toggle between increment view modes
     * @param {Webview.message} message 
     * @param {BotPanel} botPanel 
     * @returns {boolean} true if panel should update
     */
    static toggleIncrementView(message, botPanel) {
        Logger.log('[StoryGraphManager] toggleIncrementView: switching to ' + message.currentView);
        botPanel._currentStoryMapView = message.currentView;
        return true;
    }

    /**
     * Switch view mode (Hierarchy/Increment/Files)
     * @param {Webview.message} message 
     * @param {BotPanel} botPanel 
     * @returns {boolean} true if panel should update
     */
    static switchViewMode(message, botPanel) {
        Logger.log('[StoryGraphManager] switchViewMode: switching to ' + message.viewMode);
        botPanel._currentStoryMapView = message.viewMode;
        return true;
    }

    /**
     * Copy node data to clipboard (name or JSON)
     * @param {Webview.message} message 
     * @param {BotPanel} botPanel 
     * @returns {boolean} false - handles own async flow
     */
    static async copyNodeToClipboard(message, botPanel) {
        const nodePath = message.nodePath;
        const action = message.action;
        
        if (!nodePath || !action) {
            return false;
        }
        
        const method = action === 'json' ? 'copy_json' : 'copy_name';
        const command = nodePath + '.' + method;
        
        const doCopy = async () => {
            const response = await botPanel._botView.execute(command);
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
                    StoryGraphManager.handleError(err, 'copy node to clipboard');
                }
            });
        } else {
            doCopy().catch((err) => {
                StoryGraphManager.handleError(err, 'copy node to clipboard');
            });
        }
        
        return false;
    }

    /**
     * Copy increment stories as JSON to clipboard
     * @param {Webview.message} message 
     * @param {BotPanel} botPanel 
     * @returns {boolean} false - handles own async flow
     */
    static async copyIncrementStoriesJson(message, botPanel) {
        const incName = message.incName;
        
        if (!incName) {
            return false;
        }
        
        const command = 'story_graph.copy_increment_stories_json name:"' + incName + '"';
        
        const doCopy = async () => {
            const response = await botPanel._botView.execute(command);
            const result = response && (response.result !== undefined ? response.result : response);
            const arr = Array.isArray(result) ? result : (result && result.result ? result.result : []);
            const text = JSON.stringify(arr, null, 2);
            await vscode.env.clipboard.writeText(text);
            vscode.window.showInformationMessage('Increment stories JSON copied to clipboard');
        };
        
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Injecting increment stories to clipboard...',
            cancellable: false
        }, async () => {
            try {
                await doCopy();
            } catch (err) {
                StoryGraphManager.handleError(err, 'copy increment stories');
            }
        });
        
        return false;
    }

    /**
     * Handle node rename with input dialog and optimistic updates
     * @param {Webview.message} message 
     * @param {BotPanel} botPanel 
     * @returns {boolean} false - handles own async flow with optimistic updates
     */
    static async renameNode(message, botPanel) {
        Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] ========== RENAME OPERATION RECEIVED ==========`);
        Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Received renameNode message`, {
            nodePath: message.nodePath,
            currentName: message.currentName,
            timestamp: new Date().toISOString()
        });
        if (message.nodePath && message.currentName) {

            Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Prompting user for new name`);
            vscode.window.showInputBox({
            prompt: `Rename "${message.currentName}"`,
            value: message.currentName,
            placeHolder: 'Enter new name'
            }).then((newName) => {
            Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] User provided new name`, {
                newName: newName,
                currentName: message.currentName,
                changed: newName && newName !== message.currentName
            });
            if (newName && newName !== message.currentName) {

                const trimmedName = newName.trim().replace(/^"(.*)"$/, '$1');

                const escapedName = trimmedName.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
                const command = `${message.nodePath}.rename name:"${escapedName}"`;
                Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Built rename command: ${command}`);
                

                Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Sending optimistic update to webview`);
                botPanel._panel.webview.postMessage({
                    command: 'optimisticRename',
                    nodePath: message.nodePath,
                    oldName: message.currentName,
                    newName: trimmedName
                });
                                
                const logEntry = `\n${'='.repeat(80)}\n[RENAME COMMAND: ${command}\n`;
                
                Logger.logStoryGraphOperations(logEntry);
                

                Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Executing rename command via backend (optimistic)...`);
                botPanel._botView?.execute(command)
                .then((result) => {
                    Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] [SUCCESS] Backend rename executed successfully`);
                    Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Result: ${JSON.stringify(result).substring(0, 500)}`);
                    

                    const resultLog = `[ RESULT: ${JSON.stringify(result, null, 2)}\n`;
                    Logger.logStoryGraphOperations(resultLog);
                    

                    botPanel._panel.webview.postMessage({
                        command: 'saveCompleted',
                        success: true,
                        result: result
                    });
                    

                    Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] Optimistic update - skipping panel refresh`);
                    Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] ========== RENAME OPERATION COMPLETE ==========`);
                })
                .catch((error) => {
                    Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] [ERROR] Rename failed`);
                    Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] [ERROR] Error: ${error.message}`);
                    Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] [ERROR] Stack: ${error.stack}`);
                    

                    botPanel._panel.webview.postMessage({
                        command: 'saveCompleted',
                        success: false,
                        error: error.message
                    });
                    

                    const errorLog = `[ERROR: ${error.message}\nSTACK: ${error.stack}\n`;
                    Logger.logStoryGraphOperations(errorLog);
                    
                    vscode.window.showErrorMessage(`Failed to rename: ${error.message}`);                    

                    Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] [ERROR] Refreshing panel after error...`);
                    botPanel._update().catch(err => {
                        Logger.log(`[ASYNC_SAVE] [EXTENSION_HOST] [RENAME] [ERROR] Panel refresh failed: ${err.message}`);
                    });
                });
            }
            });
        }
    }
 
}

module.exports = StoryGraphManager;