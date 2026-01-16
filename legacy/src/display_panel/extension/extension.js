/**
 * REPL Status Display Panel Extension
 * 
 * Main entry point for VS Code extension that displays REPL CLI status
 * in a rich webview panel above the chat interface.
 */

const vscode = require("vscode");
const StatusPanel = require("./status_panel.js");

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
function activate(context) {
  try {
    outputChannel = vscode.window.createOutputChannel("REPL Status Panel");
    log("Activating REPL Status Display Panel extension");
    
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspaceRoot) {
      vscode.window.showErrorMessage("REPL Status Panel: No workspace folder found");
      return;
    }
    
    // Register the show status command
    const showStatusCommand = vscode.commands.registerCommand(
      "agilebot.showStatus",
      () => {
        log("Show Status command invoked");
        StatusPanel.createOrShow(workspaceRoot, context.extensionUri);
      }
    );
    
    context.subscriptions.push(showStatusCommand);
    
    log("REPL Status Display Panel extension activated successfully");
    vscode.window.showInformationMessage("REPL Status Panel: Ready");
    
  } catch (error) {
    log(`ERROR: Activation failed: ${error.message}`);
    vscode.window.showErrorMessage(`REPL Status Panel Error: ${error.message}`);
  }
}

/**
 * Extension deactivation
 * Called when extension is deactivated
 */
function deactivate() {
  log("Deactivating REPL Status Display Panel extension");
  if (outputChannel) {
    outputChannel.dispose();
    outputChannel = null;
  }
}

module.exports = { activate, deactivate };
