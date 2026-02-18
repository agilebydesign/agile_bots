/**
 * PathsSection - Renders workspace path and bot directory paths.
 * 
 * Epic: Invoke Bot Through Panel
 * Sub-Epic: Manage Panel Session
 * Story: Change Workspace Path
 */

const PanelView = require('./panel_view');
const { escapeForHtml, truncatePath } = require('./utils');

class PathsSection extends PanelView {
    /**
     * Paths section view.
     * 
     * @param {string|PanelView} botPathOrCli - Bot path or CLI instance
     */
    constructor(botPathOrCli) {
        super(botPathOrCli);
    }    
    
    /**
     * Render paths section HTML.
     * 
     * @returns {string} HTML string
     */
    async render() {
        console.log('[PathsSection] Starting render');
        console.log('[PathsSection] Executing status command...');
        const response = await this.execute('status');
        console.log('[PathsSection] Status response:', JSON.stringify(response).substring(0, 300));
        
        // Extract bot data from response (handle nested structure)
        const botData = response?.bot || response;
        
        // NO FALLBACKS - let it fail if data is missing
        if (!botData) throw new Error('[PathsSection] botData is null/undefined');
        if (!botData.workspace_directory) throw new Error('[PathsSection] No workspace_directory in response');
        if (!botData.bot_directory) throw new Error('[PathsSection] No bot_directory in response');
        
        const maxPathLength = 80;
        const safeWorkspaceDir = escapeForHtml(botData.workspace_directory);
        const safeBotDir = escapeForHtml(botData.bot_directory);
        const displayWorkspaceDir = truncatePath(safeWorkspaceDir, maxPathLength);
        const displayBotDir = truncatePath(safeBotDir, maxPathLength);
        
        return `
            <div class="card-secondary" style="padding: 1px 5px 2px 5px;">
                <div class="input-container" style="margin-top: 0;">
                    <div class="input-header">Workspace</div>
                    <div style="display: flex; gap: 4px; align-items: center;">
                        <input type="text" id="workspacePathInput" 
                               value="${safeWorkspaceDir}" 
                               placeholder="Path to workspace"
                               style="flex: 1;"
                               onchange="updateWorkspace(this.value)"
                               onkeydown="if(event.key === 'Enter') { event.preventDefault(); updateWorkspace(this.value); }"
                               ondragover="event.preventDefault(); event.dataTransfer.dropEffect = 'copy'; this.classList.add('drag-over');"
                               ondragleave="this.classList.remove('drag-over');"
                               ondrop="event.preventDefault(); this.classList.remove('drag-over'); const items = event.dataTransfer.items || []; for (let i = 0; i < items.length; i++) { const item = items[i]; if (item.kind === 'file') { const entry = item.webkitGetAsEntry ? item.webkitGetAsEntry() : null; if (entry && entry.isDirectory) { this.value = entry.fullPath || event.dataTransfer.getData('text/plain'); updateWorkspace(this.value); return; } } } const text = event.dataTransfer.getData('text/uri-list') || event.dataTransfer.getData('text/plain'); if (text) { let path = text.replace(/^file:\\/\\/\\//, '').replace(/^file:\\/\\//, ''); path = decodeURIComponent(path); this.value = path; updateWorkspace(path); }"
                               title="${safeWorkspaceDir}" />
                        <button onclick="browseWorkspace()" title="Browse for folder" style="padding: 4px 8px; min-width: auto;">📁</button>
                    </div>
                </div>
                <div class="info-display" style="margin-top: 4px;" title="${safeBotDir}">
                    <span class="label">Bot Path:</span>
                    <span class="value">${displayBotDir}</span>
                </div>
            </div>`;
    }
    
    /**
     * Handle events.
     * 
     * @param {string} eventType - Event type
     * @param {Object} eventData - Event data
     * @returns {Promise<Object>} Result
     */
    async handleEvent(eventType, eventData) {
        if (eventType === 'updateWorkspace') {
            // Update workspace logic would go here
            // For now, just return success
            return { success: true, workspace: eventData.workspacePath };
        }
        throw new Error(`Unknown event type: ${eventType}`);
    }
}

module.exports = PathsSection;
