// Client-side functions for workspace management, called from workspace.html and bot_panel's webView content
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

function setWorkspacePath(path) {
    console.log('[WebView] Received setWorkspacePath message:', path);
    const input = document.getElementById('workspacePathInput');
    if (input) {
        input.value = path;
    }
}

function getWorkspaceDir() {
    if (window.botData && window.botData.workspace_directory) {
        return window.botData.workspace_directory;
    }    
    return '';
}