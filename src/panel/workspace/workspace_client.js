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