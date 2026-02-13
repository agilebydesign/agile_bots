/**
 * Bot Panel Extension
 * 
 * Main entry point for VS Code extension that displays bot status
 * in a rich webview panel above the chat interface.
 */

const vscode = require("vscode");
const BotPanel = require("./bot_panel.js");
const BotPanelSidebarProvider = require("./bot_panel_sidebar.js");

let outputChannel = null;

function log(message) {
  const timestamp = new Date().toISOString();
  const logMessage = `[${timestamp}] ${message}`;
  console.log(logMessage);
  if (outputChannel) {
    outputChannel.appendLine(logMessage);
  }
}

/**
 * Extension activation
 * Called when extension is first activated (command invoked)
 */
/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  try {
    outputChannel = vscode.window.createOutputChannel("Bot Panel");
    log("Activating Bot Panel extension");
    
    // Register the sidebar webview provider (shows in bottom panel next to Chat)
    const sidebarProvider = new BotPanelSidebarProvider(context.extensionUri);
    context.subscriptions.push(
      vscode.window.registerWebviewViewProvider(
        BotPanelSidebarProvider.viewType,
        sidebarProvider,
        {
          webviewOptions: {
            retainContextWhenHidden: true
          }
        }
      )
    );
    log("Sidebar provider registered");
    
    // Register the view panel command - don't check workspace here, let command handle it
    const viewPanelCommand = vscode.commands.registerCommand(
      "agilebot.viewPanel",
      () => {
        try {
          log("View Bot Panel command invoked");
          const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || process.cwd();
          log(`Workspace root: ${workspaceRoot}`);
          if (!workspaceRoot) {
            vscode.window.showErrorMessage("Bot Panel: No workspace folder found. Please open a workspace folder.");
            return;
          }
          log(`Extension URI: ${context.extensionUri}`);
          log("Calling BotPanel.createOrShow...");
          BotPanel.createOrShow(workspaceRoot, context.extensionUri);
          log("BotPanel.createOrShow completed");
        } catch (error) {
          log(`ERROR: Command execution failed: ${error.message}`);
          log(`ERROR: Stack: ${error.stack}`);
          vscode.window.showErrorMessage(`Bot Panel Error: ${error.message}`);
        }
      }
    );
    
    context.subscriptions.push(viewPanelCommand);
    
    // In Cursor, ensure the primary sidebar stays on the left.
    // The extension registers in the secondarySideBar (right) which is correct,
    // but Cursor's layout restore can push the primary sidebar to the right.
    const isCursor = vscode.env.appName?.includes("Cursor");
    if (isCursor) {
      vscode.commands.executeCommand("workbench.action.moveSideBarLeft");
      log("Cursor detected - enforced primary sidebar to left");
    }

    log("Bot Panel extension activated successfully - command registered");
    
  } catch (error) {
    log(`ERROR: Activation failed: ${error.message}`);
    log(`ERROR: Stack: ${error.stack}`);
    vscode.window.showErrorMessage(`Bot Panel Error: ${error.message}`);
  }
}

/**
 * Extension deactivation
 * Called when extension is deactivated
 */
function deactivate() {
  log("Deactivating Bot Panel extension");
  if (outputChannel) {
    outputChannel.dispose();
    outputChannel = null;
  }
}

module.exports = { activate, deactivate };
