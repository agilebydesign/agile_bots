const vscode = require("vscode");
const { Logger } = require("../utils");
const BotPanel = require("../bot/bot_panel");

/**
 * WorkspaceManager handles routing of workspace-related messages from the webview client to the appropriate views
 * workspace_client.js holds the client-side events
 */
function handleError(error, operation) {
        Logger.log(`[WorkspaceManager] ERROR ${operation}: ` + error.message);
        Logger.log(`[WorkspaceManager] ERROR stack: ` + error.stack);
        vscode.window.showErrorMessage(`Failed to ${operation}: ${error.message}`);
    }

async function executeCliCommand(command, botPanel, operationDescription) {
    Logger.log(`[WorkspaceManager] Executing CLI command: ${command}`);
    return botPanel._sharedCLI.execute(command)
        .then((result) => {
            if (result.status === 'error') {
                throw new Error(`CLI error: ${result.message}`);
            }
            Logger.log(`[WorkspaceManager] ${operationDescription} result: ` + JSON.stringify(result));
            return true;
        })
        .catch((error) => {
            handleError(error, operationDescription);
            return false;
        });
}

    /**
 * 
 * @param {Webview.message} message 
 * @param {BotPanel} botPanel 
 */
async function switchBot(message, botPanel) {
    // botPanel._botView.headerView.handleUpdateWorkspaceEvent('updateWorkspace', { workspacePath: message.workspacePath })
    if (typeof message.botName === 'undefined' || message.botName === "") {
        handleError(new Error(`switchBot() called with no botName in message`), 'switch bot');
        return false;
    }

    const botName = message.botName;        
    return executeCliCommand(`bot ${botName}`, botPanel, 'switch bot');                           
}

/**
 * @param {Webview.message} message 
 * @param {BotPanel} botPanel 
 * @returns 
 */
async function updateWorkspace(message, botPanel) {        
    // botPanel._botView.headerView.handleUpdateWorkspaceEvent('updateWorkspace', { workspacePath: message.workspacePath })
    if (typeof message.workspacePath === 'undefined' || message.workspacePath === "") {
        handleError(new Error(`updateWorkspaceEvent() called with no workspacePath in eventData`), 'update workspace');
        return false;
    }

    const workspacePath = message.workspacePath;        
    return executeCliCommand(`workspace ${workspacePath}`, botPanel, 'update workspace');                           
}

/**
 * Opens folder picker dialog, then updates workspace path to first selected folder
 * @param {BotPanel} botPanel 
 */
async function browseAndUpdateWorkspace(botPanel) {
    vscode.window.showOpenDialog({
        canSelectFiles: false,
        canSelectFolders: true,
        canSelectMany: false,
        openLabel: 'Select Workspace Folder'
    }).then(async (folders) => {
        if (folders && folders.length > 0) {
            const folderPath = folders[0].fsPath;
            Logger.log('[WorkspaceManager] User selected folder: ' + folderPath);
            
            // update client-side workspace label
            botPanel._panel.webview.postMessage({
                command: 'setWorkspacePath',
                path: folderPath
            });
            return updateWorkspace({ workspacePath: folderPath }, botPanel);
        }
    })            
    .catch((error) => {
        handleError(error, 'browse/update workspace');
        return false;
    });        
}

module.exports = {
    switchBot,
    updateWorkspace,
    browseAndUpdateWorkspace,        
}