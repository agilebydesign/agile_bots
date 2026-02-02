// @ts-check
const vscode = require('vscode');

/**
 * Serializer for .trace notebook files.
 * Format: JSON with cells array.
 */
class TraceNotebookSerializer {
    /**
     * @param {Uint8Array} content
     * @returns {Promise<vscode.NotebookData>}
     */
    async deserializeNotebook(content) {
        const text = new TextDecoder().decode(content);
        
        if (!text.trim()) {
            return new vscode.NotebookData([]);
        }

        try {
            const data = JSON.parse(text);
            const cells = (data.cells || []).map(cell => {
                const cellData = new vscode.NotebookCellData(
                    cell.kind === 'code' ? vscode.NotebookCellKind.Code : vscode.NotebookCellKind.Markup,
                    cell.value || '',
                    cell.language || 'python'
                );
                if (cell.metadata) {
                    cellData.metadata = cell.metadata;
                }
                return cellData;
            });
            return new vscode.NotebookData(cells);
        } catch (e) {
            console.error('Failed to parse trace notebook:', e);
            return new vscode.NotebookData([]);
        }
    }

    /**
     * @param {vscode.NotebookData} data
     * @returns {Promise<Uint8Array>}
     */
    async serializeNotebook(data) {
        const cells = data.cells.map(cell => ({
            kind: cell.kind === vscode.NotebookCellKind.Code ? 'code' : 'markdown',
            value: cell.value,
            language: cell.languageId,
            metadata: cell.metadata
        }));

        const json = JSON.stringify({ cells }, null, 2);
        return new TextEncoder().encode(json);
    }
}

module.exports = { TraceNotebookSerializer };
