const vscode = require("vscode");
const { Logger } = require("../utils");

class WorkspaceManager {
    
    constructor() {}

    static handleError(error, operation) {
        Logger.log(`[WorkspaceManager] ERROR ${operation}: ` + error.message);
        Logger.log(`[WorkspaceManager] ERROR stack: ` + error.stack);
        vscode.window.showErrorMessage(`Failed to ${operation}: ${error.message}`);
    }
    
    static updateWorkspace(message, botPanel) {
        if (message.workspacePath) {
            botPanel._botView.handleEvent('updateWorkspace', { workspacePath: message.workspacePath })
            .then((result) => {
                Logger.log('[WorkspaceManager] updateWorkspace result: ' + JSON.stringify(result));
                botPanel._workspaceRoot = message.workspacePath;
                return true;
            })
            .catch((error) => {
                WorkspaceManager.handleError(error, 'update workspace');
            });
            return false;
        }
    }

    static browseWorkspace(botPanel) {
        vscode.window.showOpenDialog({
            canSelectFiles: false,
            canSelectFolders: true,
            canSelectMany: false,
            openLabel: 'Select Workspace Folder'
        }).then((folders) => {
            if (folders && folders.length > 0) {
                const folderPath = folders[0].fsPath;
                Logger.log('[WorkspaceManager] User selected folder: ' + folderPath);
                
                // update client-side workspace label
                botPanel._panel.webview.postMessage({
                    command: 'setWorkspacePath',
                    path: folderPath
                });
                if (WorkspaceManager.updateWorkspace({ workspacePath: folderPath }, botPanel)) {
                    return true;
                }
                return false;            
            }
        })            
        .catch((error) => {
            WorkspaceManager.handleError(error, 'browse/update workspace');
        });;
    }   
}

module.exports = WorkspaceManager;