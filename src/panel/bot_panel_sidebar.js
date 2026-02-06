/**
 * BotPanelSidebarProvider - WebviewViewProvider for sidebar panel
 * 
 * Displays the bot panel in VS Code's bottom panel (alongside Terminal, Output, etc.)
 * This allows side-by-side viewing with Copilot Chat.
 */

const vscode = require("vscode");
const BotPanel = require("./bot_panel.js");
const path = require("path");

class BotPanelSidebarProvider {
    static viewType = "agilebot.botPanelView";
    
    constructor(extensionUri) {
        this._extensionUri = extensionUri;
        this._view = null;
        this._workspaceRoot = null;
        this._botPanel = null;
    }
    
    /**
     * Called when the view is first shown
     * @param {vscode.WebviewView} webviewView 
     * @param {vscode.WebviewViewResolveContext} context 
     * @param {vscode.CancellationToken} token 
     */
    async resolveWebviewView(webviewView, context, token) {
        this._view = webviewView;
        this._workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || process.cwd();
        
        console.log("[BotPanelSidebar] resolveWebviewView called");
        console.log("[BotPanelSidebar] Workspace root:", this._workspaceRoot);
        
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };
        
        // Create a BotPanel instance to handle all the logic
        // We'll use its methods but provide our own webview
        this._botPanel = BotPanel.createForSidebar(
            webviewView, 
            this._workspaceRoot, 
            this._extensionUri
        );
        
        // Handle visibility changes - don't refresh on every visibility change
        // as this resets scroll position. Only refresh if we haven't loaded yet.
        let hasLoaded = false;
        webviewView.onDidChangeVisibility(() => {
            if (webviewView.visible && this._botPanel && !hasLoaded) {
                console.log("[BotPanelSidebar] View became visible for first time, loading");
                hasLoaded = true;
                this._botPanel.refresh();
            }
        });
    }
    
    /**
     * Refresh the panel (can be called externally)
     */
    async refresh() {
        if (this._botPanel) {
            await this._botPanel.refresh();
        }
    }
}

module.exports = BotPanelSidebarProvider;
