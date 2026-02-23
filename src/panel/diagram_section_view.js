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
            return `<div class="diagram-item" style="margin: 4px 0;">
                <span style="color: var(--vscode-errorForeground); font-size: 12px;">Not found: ${this._escapeHtml(this._fileName(filePath))}</span>
            </div>`;
        }

        let fileLinks = '';
        const origName = this._fileName(filePath);
        fileLinks += `<a href="#" class="diagram-link" data-original-name="${this._escapeHtml(origName)}" onclick="openFile('${jsPath}', event); return false;" style="color: var(--vscode-textLink-foreground); cursor: pointer; font-size: 12px;">${this._escapeHtml(origName)}</a>`;
        if (reportPath) {
            const jsReportPath = this._escapeForJs(reportPath);
            fileLinks += `<span style="margin: 0 6px; opacity: 0.5;">|</span>`;
            fileLinks += `<a href="#" class="report-link" onclick="openFile('${jsReportPath}', event); return false;" style="color: var(--vscode-textLink-foreground); cursor: pointer; font-size: 12px;">${this._escapeHtml(this._fileName(reportPath))}</a>`;
        }

        return `<div class="diagram-item" style="margin: 3px 0;">
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
