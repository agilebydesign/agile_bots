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
        if (!message.nodePath || !message.currentName) {
            return false;
        }

        Logger.log(`[StoryGraphManager] ========== RENAME OPERATION RECEIVED ==========`);
        Logger.log(`[StoryGraphManager] [RENAME] Received renameNode message`, {
            nodePath: message.nodePath,
            currentName: message.currentName,
            timestamp: new Date().toISOString()
        });

        Logger.log(`[StoryGraphManager] [RENAME] Prompting user for new name`);
        
        const newName = await vscode.window.showInputBox({
            prompt: `Rename "${message.currentName}"`,
            value: message.currentName,
            placeHolder: 'Enter new name'
        });

        Logger.log(`[StoryGraphManager] [RENAME] User provided new name`, {
            newName: newName,
            currentName: message.currentName,
            changed: newName && newName !== message.currentName
        });

        if (!newName || newName === message.currentName) {
            return false;
        }

        const trimmedName = newName.trim().replace(/^"(.*)"$/, '$1');
        const escapedName = trimmedName.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
        const command = `${message.nodePath}.rename name:"${escapedName}"`;
        
        Logger.log(`[StoryGraphManager] [RENAME] Built rename command: ${command}`);

        // Send optimistic update to webview
        Logger.log(`[StoryGraphManager] [RENAME] Sending optimistic update to webview`);
        botPanel._panel.webview.postMessage({
            command: 'optimisticRename',
            nodePath: message.nodePath,
            oldName: message.currentName,
            newName: trimmedName
        });

        const logPath = path.join(botPanel._workspaceRoot, 'story_graph_operations.log');
        const timestamp = new Date().toISOString();
        const logEntry = `\n${'='.repeat(80)}\n[${timestamp}] RENAME COMMAND: ${command}\n`;

        try {
            fs.appendFileSync(logPath, logEntry);
        } catch (err) {
            Logger.log(`[StoryGraphManager] Failed to write to log file: ${err.message}`);
        }

        // Execute rename command
        Logger.log(`[StoryGraphManager] [RENAME] Executing rename command via backend (optimistic)...`);
        
        try {
            const result = await botPanel._botView?.execute(command);
            
            Logger.log(`[StoryGraphManager] [RENAME] [SUCCESS] Backend rename executed successfully`);
            Logger.log(`[StoryGraphManager] [RENAME] Result: ${JSON.stringify(result).substring(0, 500)}`);

            const resultLog = `[${timestamp}] RESULT: ${JSON.stringify(result, null, 2)}\n`;
            try {
                fs.appendFileSync(logPath, resultLog);
            } catch (err) {
                Logger.log(`[StoryGraphManager] Failed to write result to log file: ${err.message}`);
            }

            // Notify webview of success
            botPanel._panel.webview.postMessage({
                command: 'saveCompleted',
                success: true,
                result: result
            });

            Logger.log(`[StoryGraphManager] [RENAME] Optimistic update - skipping panel refresh`);
            Logger.log(`[StoryGraphManager] ========== RENAME OPERATION COMPLETE ==========`);
            
            return false; // Don't trigger update - optimistic updates handled
            
        } catch (error) {
            Logger.log(`[StoryGraphManager] [RENAME] [ERROR] Rename failed`);
            Logger.log(`[StoryGraphManager] [RENAME] [ERROR] Error: ${error.message}`);
            Logger.log(`[StoryGraphManager] [RENAME] [ERROR] Stack: ${error.stack}`);

            // Notify webview of failure (triggers rollback)
            botPanel._panel.webview.postMessage({
                command: 'saveCompleted',
                success: false,
                error: error.message
            });

            const errorLog = `[${timestamp}] ERROR: ${error.message}\nSTACK: ${error.stack}\n`;
            try {
                fs.appendFileSync(logPath, errorLog);
            } catch (err) {
                Logger.log(`[StoryGraphManager] Failed to write error to log file: ${err.message}`);
            }

            vscode.window.showErrorMessage(`Failed to rename: ${error.message}`);

            // Refresh panel after error to restore correct state
            Logger.log(`[StoryGraphManager] [RENAME] [ERROR] Refreshing panel after error...`);
            try {
                await botPanel._update();
            } catch (err) {
                Logger.log(`[StoryGraphManager] [RENAME] [ERROR] Panel refresh failed: ${err.message}`);
            }

            return false;
        }
    }
}

module.exports = StoryGraphManager;