// @ts-check
const vscode = require('vscode');

/**
 * Notebook controller - handles execution (which we use for expansion).
 */
class TraceNotebookController {
    constructor(cli) {
        this.cli = cli;
        this.id = 'trace-notebook-controller';
        this.label = 'Trace Notebook';
        this.supportedLanguages = ['python', 'javascript', 'markdown'];

        this._controller = vscode.notebooks.createNotebookController(
            this.id,
            'trace-notebook',
            this.label
        );

        this._controller.supportedLanguages = this.supportedLanguages;
        this._controller.executeHandler = this._execute.bind(this);
    }

    dispose() {
        this._controller.dispose();
    }

    /**
     * Execute = expand the cell to show references.
     * @param {vscode.NotebookCell[]} cells
     * @param {vscode.NotebookDocument} notebook
     * @param {vscode.NotebookController} controller
     */
    async _execute(cells, notebook, controller) {
        for (const cell of cells) {
            const execution = controller.createNotebookCellExecution(cell);
            execution.start(Date.now());

            const meta = cell.metadata?.trace;
            if (!meta?.nodeId) {
                execution.replaceOutput([
                    new vscode.NotebookCellOutput([
                        vscode.NotebookCellOutputItem.text('No trace metadata - nothing to expand')
                    ])
                ]);
                execution.end(true, Date.now());
                continue;
            }

            try {
                const result = await this.cli.expand(meta.nodeId, meta.loaded || 0, 8);
                
                if (result.error) {
                    execution.replaceOutput([
                        new vscode.NotebookCellOutput([
                            vscode.NotebookCellOutputItem.error(new Error(result.error))
                        ])
                    ]);
                    execution.end(false, Date.now());
                    continue;
                }

                const summary = `Found ${result.totalCandidates} references, showing ${result.children?.length || 0}`;
                execution.replaceOutput([
                    new vscode.NotebookCellOutput([
                        vscode.NotebookCellOutputItem.text(summary)
                    ])
                ]);
                execution.end(true, Date.now());

                // Insert child cells (via command to avoid execution loop)
                if (result.children?.length) {
                    await vscode.commands.executeCommand('trace.expand');
                }
            } catch (e) {
                execution.replaceOutput([
                    new vscode.NotebookCellOutput([
                        vscode.NotebookCellOutputItem.error(e)
                    ])
                ]);
                execution.end(false, Date.now());
            }
        }
    }

    /**
     * Create initial cells for a story trace.
     * @param {object} story
     * @param {object} resolved - test class info
     * @returns {vscode.NotebookCellData[]}
     */
    createStoryCells(story, resolved) {
        const cells = [];

        // Story header
        cells.push(new vscode.NotebookCellData(
            vscode.NotebookCellKind.Markup,
            `# ${story.name}\n\n${(story.scenarios || []).map(s => `- **${s.name}**`).join('\n')}`,
            'markdown'
        ));

        // Test class cell
        if (resolved.testClass) {
            const testCell = new vscode.NotebookCellData(
                vscode.NotebookCellKind.Code,
                `# Test: ${resolved.testClass}\n# ${resolved.testFile}`,
                'python'
            );
            testCell.metadata = {
                trace: {
                    nodeId: resolved.nodeId,
                    kind: 'test',
                    lang: 'python',
                    filePath: resolved.testFile,
                    symbol: resolved.testClass,
                    range: resolved.range,
                    depth: 0
                }
            };
            cells.push(testCell);
        }

        // Scenario/test method cells
        for (const scenario of resolved.scenarios || []) {
            const scenarioCell = new vscode.NotebookCellData(
                vscode.NotebookCellKind.Code,
                `# ${scenario.name}`,
                'python'
            );
            scenarioCell.metadata = {
                trace: {
                    nodeId: scenario.nodeId,
                    kind: 'test',
                    lang: 'python',
                    filePath: resolved.testFile,
                    symbol: scenario.name,
                    range: scenario.range,
                    depth: 1,
                    parentNodeId: resolved.nodeId
                }
            };
            cells.push(scenarioCell);
        }

        return cells;
    }
}

module.exports = { TraceNotebookController };
