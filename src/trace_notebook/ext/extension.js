// @ts-check
const vscode = require('vscode');
const { TraceNotebookSerializer } = require('./traceNotebookSerializer');
const { TraceNotebookController } = require('./traceNotebookController');
const { TraceCLI } = require('./traceCLI');

let cli;
let controller;

function activate(context) {
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspaceRoot) return;

    cli = new TraceCLI(workspaceRoot);
    
    context.subscriptions.push(
        vscode.workspace.registerNotebookSerializer('trace-notebook', new TraceNotebookSerializer(), { transientOutputs: true }),
        controller = new TraceNotebookController(cli),
        vscode.commands.registerCommand('trace.open', () => openTraceNotebook()),
        vscode.commands.registerCommand('trace.expand', () => expandCell()),
        vscode.commands.registerCommand('trace.collapse', () => collapseCell())
    );
}

async function openTraceNotebook() {
    // Hardcoded: Navigate Sequentially story
    const cells = [
        new vscode.NotebookCellData(
            vscode.NotebookCellKind.Markup,
            `# Navigate Sequentially

**Scenarios:**
- bot.next() moves to next action
- bot.next() progresses through workflow sequence
- bot.next() at final action advances to next behavior
- bot.current() returns current action instructions`,
            'markdown'
        ),
        new vscode.NotebookCellData(
            vscode.NotebookCellKind.Code,
            `# TEST: TestNavigateSequentially
# File: test/invoke_bot/navigate_behavior_actions/test_navigate_behavior_and_actions.py
# Lines: 355-592
#
# Run this cell (Shift+Enter) or use "Trace: Expand Cell" to see code references`,
            'python'
        )
    ];

    // Add metadata for expansion
    cells[1].metadata = {
        trace: {
            nodeId: 'python:test/invoke_bot/navigate_behavior_actions/test_navigate_behavior_and_actions.py:355:0:592:0',
            kind: 'test',
            lang: 'python',
            filePath: 'test/invoke_bot/navigate_behavior_actions/test_navigate_behavior_and_actions.py',
            symbol: 'TestNavigateSequentially',
            range: { startLine: 355, endLine: 592 },
            depth: 0
        }
    };

    const data = new vscode.NotebookData(cells);
    const doc = await vscode.workspace.openNotebookDocument('trace-notebook', data);
    await vscode.window.showNotebookDocument(doc);
}

async function expandCell() {
    const editor = vscode.window.activeNotebookEditor;
    if (!editor) return;

    const cellIndex = editor.selections[0]?.start;
    if (cellIndex === undefined) return;

    const cell = editor.notebook.cellAt(cellIndex);
    const meta = cell.metadata?.trace;
    if (!meta?.nodeId) {
        vscode.window.showInformationMessage('No expandable node in this cell');
        return;
    }

    // Init CLI if needed
    if (!cli.initialized) {
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Indexing workspace...'
        }, () => cli.init());
    }

    // Expand
    const result = await cli.expand(meta.nodeId, meta.loaded || 0, 5);
    if (result.error) {
        vscode.window.showErrorMessage(result.error);
        return;
    }

    if (!result.children?.length) {
        vscode.window.showInformationMessage('No more references found');
        return;
    }

    // Create child cells
    const newCells = result.children.map(child => {
        const cellData = new vscode.NotebookCellData(
            vscode.NotebookCellKind.Code,
            `# CODE: ${child.symbol}\n# File: ${child.filePath}\n# Lines: ${child.range.startLine}-${child.range.endLine}\n\n${child.snippet?.text || ''}`,
            child.lang === 'javascript' ? 'javascript' : 'python'
        );
        cellData.metadata = {
            trace: {
                nodeId: child.nodeId,
                kind: child.kind,
                lang: child.lang,
                filePath: child.filePath,
                symbol: child.symbol,
                range: child.range,
                depth: (meta.depth || 0) + 1,
                parentNodeId: meta.nodeId
            }
        };
        return cellData;
    });

    // Insert after current cell
    const edit = new vscode.WorkspaceEdit();
    edit.set(editor.notebook.uri, [
        vscode.NotebookEdit.insertCells(cellIndex + 1, newCells)
    ]);
    await vscode.workspace.applyEdit(edit);

    vscode.window.showInformationMessage(`Added ${newCells.length} code references`);
}

async function collapseCell() {
    vscode.window.showInformationMessage('Collapse: not implemented yet');
}

function deactivate() {
    cli?.dispose();
}

module.exports = { activate, deactivate };
