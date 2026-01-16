/**
 * Bot Panel Extension
 * 
 * Main entry point for VS Code extension that displays bot status
 * in a rich webview panel above the chat interface.
 */

const vscode = require("vscode");
const BotPanel = require("./bot_panel.js");

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
    // #region agent log
    fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'extension.js:26',message:'Extension activate() called',data:{hasContext:!!context},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'A,C'})}).catch(()=>{});
    // #endregion
    outputChannel = vscode.window.createOutputChannel("Bot Panel");
    log("Activating Bot Panel extension");
    
    // Register the view panel command - don't check workspace here, let command handle it
    const viewPanelCommand = vscode.commands.registerCommand(
      "agilebot.viewPanel",
      () => {
        try {
          // #region agent log
          fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'extension.js:34',message:'viewPanel command invoked',data:{},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'B,C'})}).catch(()=>{});
          // #endregion
          log("View Bot Panel command invoked");
          const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || process.cwd();
          // #region agent log
          fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'extension.js:37',message:'Workspace root resolved',data:{workspaceRoot},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'C'})}).catch(()=>{});
          // #endregion
          log(`Workspace root: ${workspaceRoot}`);
          if (!workspaceRoot) {
            vscode.window.showErrorMessage("Bot Panel: No workspace folder found. Please open a workspace folder.");
            return;
          }
          log(`Extension URI: ${context.extensionUri}`);
          log("Calling BotPanel.createOrShow...");
          // #region agent log
          fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'extension.js:45',message:'Before BotPanel.createOrShow',data:{workspaceRoot,extensionUri:context.extensionUri?.toString()},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'B'})}).catch(()=>{});
          // #endregion
          BotPanel.createOrShow(workspaceRoot, context.extensionUri);
          // #region agent log
          fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'extension.js:46',message:'After BotPanel.createOrShow',data:{},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'B'})}).catch(()=>{});
          // #endregion
          log("BotPanel.createOrShow completed");
        } catch (error) {
          log(`ERROR: Command execution failed: ${error.message}`);
          log(`ERROR: Stack: ${error.stack}`);
          vscode.window.showErrorMessage(`Bot Panel Error: ${error.message}`);
        }
      }
    );
    
    context.subscriptions.push(viewPanelCommand);
    
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
