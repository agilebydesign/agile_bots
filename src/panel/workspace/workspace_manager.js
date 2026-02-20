const vscode = require("vscode");
const { Logger } = require("../utils");

class WorkspaceManager {
    
    constructor() {}

    static updateWorkspace(message, botView, botPanel) {
        if (message.workspacePath) {
            botView?.handleEvent('updateWorkspace', { workspacePath: message.workspacePath })
            .then((result) => {
                Logger.log('[WorkspaceManager] updateWorkspace result: ' + JSON.stringify(result));
                botPanel._workspaceRoot = message.workspacePath;
                return true;
            })
            .catch((error) => {
                Logger.log('[WorkspaceManager] ERROR updateWorkspace: ' + error.message);
                Logger.log('[WorkspaceManager] ERROR stack: ' + error.stack);
                vscode.window.showErrorMessage(`Failed to update workspace: ${error.message}`);
            });
            return false;
        }
    }
}

module.exports = WorkspaceManager;