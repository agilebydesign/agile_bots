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