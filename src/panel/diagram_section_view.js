class DiagramSectionView {

    constructor(diagrams) {
        this._diagrams = diagrams || [];
    }

    renderSection() {
        if (this._diagrams.length === 0) {
            return '';
        }

        const diagramItems = this._diagrams.map(d => this._renderDiagramItem(d)).join('');
        return `<div id="diagram-section">${diagramItems}</div>`;
    }

    _renderDiagramItem(diagram) {
        const filePath = diagram.file_path || '';
        const reportPath = diagram.report_path || '';
        const exists = diagram.exists !== false;
        const lastSyncTime = diagram.last_sync_time || null;
        const fileModifiedTime = diagram.file_modified_time || null;
        const jsPath = this._escapeForJs(filePath);

        if (!exists) {
            return `<div class="diagram-item" style="margin: 8px 0;">
                <span class="missing-indicator" style="color: var(--vscode-errorForeground);">Diagram file not found: ${this._escapeHtml(this._fileName(filePath))}</span>
                <div style="margin-top: 4px;">
                    <button class="render-button" data-path="${this._escapeHtml(filePath)}" onclick="vscode.postMessage({ command: 'renderDiagram', path: '${jsPath}', scope: (window.diagramScope || '') })" style="margin: 4px 4px 4px 0; cursor: pointer;">Render Diagram</button>
                </div>
            </div>`;
        }

        let buttons = '';

        buttons += `<button class="render-button" data-path="${this._escapeHtml(filePath)}" onclick="vscode.postMessage({ command: 'renderDiagram', path: '${jsPath}', scope: (window.diagramScope || '') })" style="margin: 4px 4px 4px 0; cursor: pointer;">Render Diagram</button>`;
        buttons += `<button class="save-layout-button" data-path="${this._escapeHtml(filePath)}" onclick="vscode.postMessage({ command: 'saveDiagramLayout', path: '${jsPath}', scope: (window.diagramScope || '') })" style="margin: 4px 4px 4px 0; cursor: pointer;">Save Layout</button>`;
        buttons += `<button class="clear-layout-button" data-path="${this._escapeHtml(filePath)}" onclick="vscode.postMessage({ command: 'clearDiagramLayout', path: '${jsPath}', scope: (window.diagramScope || '') })" style="margin: 4px 4px 4px 0; cursor: pointer;">Clear Layout</button>`;
        buttons += `<button class="generate-report-button" data-path="${this._escapeHtml(filePath)}" onclick="vscode.postMessage({ command: 'generateDiagramReport', path: '${jsPath}', scope: (window.diagramScope || '') })" style="margin: 4px 4px 4px 0; cursor: pointer;">Generate Report</button>`;

        if (reportPath) {
            const jsReportPath = this._escapeForJs(reportPath);
            buttons += `<button class="update-button" data-path="${this._escapeHtml(filePath)}" data-report="${this._escapeHtml(reportPath)}" onclick="vscode.postMessage({ command: 'updateFromDiagram', path: '${jsPath}', report: '${jsReportPath}', scope: (window.diagramScope || '') })" style="margin: 4px 4px 4px 0; cursor: pointer;">Update Graph</button>`;
        }

        let fileLinks = '';
        const origName = this._fileName(filePath);
        fileLinks += `<a href="#" class="diagram-link" data-original-name="${this._escapeHtml(origName)}" onclick="openFile('${jsPath}', event); return false;" style="color: var(--vscode-textLink-foreground); cursor: pointer; font-size: 0.9em;">${this._escapeHtml(origName)}</a>`;
        if (reportPath) {
            const jsReportPath = this._escapeForJs(reportPath);
            fileLinks += `<span style="margin: 0 6px; opacity: 0.5;">|</span>`;
            fileLinks += `<a href="#" class="report-link" onclick="openFile('${jsReportPath}', event); return false;" style="color: var(--vscode-textLink-foreground); cursor: pointer; font-size: 0.9em;">${this._escapeHtml(this._fileName(reportPath))}</a>`;
        }

        return `<div class="diagram-item" style="margin: 8px 0; padding: 6px; border: 1px solid var(--vscode-panel-border); border-radius: 4px;">
            <div style="margin-bottom: 4px;">${buttons}</div>
            <div style="display: flex; align-items: center; flex-wrap: wrap;">${fileLinks}</div>
        </div>`;
    }

    _fileName(filePath) {
        if (!filePath) return '';
        return filePath.split(/[/\\]/).pop() || filePath;
    }

    _escapeHtml(text) {
        if (!text) return '';
        const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
        return String(text).replace(/[&<>"']/g, m => map[m]);
    }

    _escapeForJs(text) {
        if (!text) return '';
        return String(text).replace(/\\/g, '\\\\').replace(/'/g, "\\'");
    }
}

module.exports = DiagramSectionView;
