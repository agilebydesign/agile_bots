// @ts-check
const vscode = require('vscode');
const path = require('path');
const { execSync } = require('child_process');
const { StoryTraceEditorProvider } = require('./storyTraceEditor');

/**
 * Story Trace Extension
 * 
 * Shows story → scenario → test → code traceability
 * with collapsible nested sections.
 */

function activate(context) {
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspaceRoot) return;

    context.subscriptions.push(
        // Register custom editor for .strace files
        vscode.window.registerCustomEditorProvider(
            StoryTraceEditorProvider.viewType,
            new StoryTraceEditorProvider(context),
            { webviewOptions: { retainContextWhenHidden: true } }
        ),
        
        // Command to open the scenario trace
        vscode.commands.registerCommand('trace.open', () => openScenarioTrace(workspaceRoot)),
        
        // Command to regenerate the trace file
        vscode.commands.registerCommand('trace.regenerate', () => regenerateTrace(workspaceRoot))
    );
}

/**
 * Open the scenario trace file (.strace) with collapsible sections
 */
async function openScenarioTrace(workspaceRoot) {
    const tracePath = path.join(workspaceRoot, 'src', 'trace_notebook', 'scenario.strace');
    
    try {
        const uri = vscode.Uri.file(tracePath);
        await vscode.commands.executeCommand('vscode.openWith', uri, StoryTraceEditorProvider.viewType);
    } catch (e) {
        // File doesn't exist - offer to generate it
        const generate = await vscode.window.showErrorMessage(
            'Trace file not found. Generate it?',
            'Generate'
        );
        if (generate === 'Generate') {
            await regenerateTrace(workspaceRoot);
        }
    }
}

/**
 * Regenerate the trace file using the Python script
 */
async function regenerateTrace(workspaceRoot) {
    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: 'Generating trace...',
        cancellable: false
    }, async () => {
        try {
            execSync('python -m src.trace_notebook.strace_generator', { cwd: workspaceRoot });
            
            // Open the generated file
            const tracePath = path.join(workspaceRoot, 'src', 'trace_notebook', 'scenario.strace');
            const uri = vscode.Uri.file(tracePath);
            await vscode.commands.executeCommand('vscode.openWith', uri, StoryTraceEditorProvider.viewType);
            
            vscode.window.showInformationMessage('Trace generated!');
        } catch (e) {
            vscode.window.showErrorMessage(`Failed to generate trace: ${e.message}`);
        }
    });
}

function deactivate() {}

module.exports = { activate, deactivate };
