/**
 * BotHeaderView - Renders bot header section with bot name, version, refresh button, and bot selector.
 * 
 * Epic: Invoke Bot Through Panel
 * Sub-Epic: Manage Panel Session
 * Story: Open Panel, Display Session Status, Switch Bot
 */

const PanelView = require('../panel/panel_view');

class BotHeaderView extends PanelView {
    /**
     * Bot header view.
     * 
     * @param {string} panelVersion - Panel extension version (optional)
     * @param {Object} webview - VS Code webview instance (optional)
     * @param {Object} extensionUri - Extension URI (optional)
     */
    constructor(panelVersion, webview, extensionUri) {
        super();
        this.panelVersion = panelVersion || null;
        this.webview = webview || null;
        this.extensionUri = extensionUri || null;
    }
    
    /**
     * Escape HTML entities.
     * 
     * @param {string} text - Text to escape
     * @returns {string} Escaped text
     */
    escapeHtml(text) {
        if (typeof text !== 'string') {
            text = String(text);
        }
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }
    
    /**
     * Get bot icon based on bot name.
     * 
     * @param {string} botName - Bot name
     * @returns {string} Icon emoji or empty string
     */
    getBotIcon(botName) {
        // No emoji fallbacks - use images only
        return '';
    }
    
    /**
     * Truncate path with ellipsis if too long
     */
    truncatePath(path, maxLength) {
        if (!path || path.length <= maxLength) return path;
        const ellipsis = '...';
        const prefixLength = Math.floor((maxLength - ellipsis.length) / 2);
        const suffixLength = maxLength - ellipsis.length - prefixLength;
        return path.substring(0, prefixLength) + ellipsis + path.substring(path.length - suffixLength);
    }
    
    /**
     * Render bot header HTML.
     * 
     * @returns {string} HTML string
     */
    async render() {
        // #region agent log
        fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_header_view.js:73',message:'render() ENTRY',data:{panelVersion:this.panelVersion,hasWebview:!!this.webview,hasExtensionUri:!!this.extensionUri},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'VERSION'})}).catch(()=>{});
        // #endregion
        console.log('[BotHeaderView] Starting render');
        console.log('[BotHeaderView] Panel version:', this.panelVersion);
        console.log('[BotHeaderView] Has webview:', !!this.webview);
        console.log('[BotHeaderView] Has extensionUri:', !!this.extensionUri);
        
        console.log('[BotHeaderView] Executing status command...');
        const botData = await this.execute('status');
        console.log('[BotHeaderView] Status response:', JSON.stringify(botData).substring(0, 300));
        
        const vscode = require('vscode');
        const maxPathLength = 80;
        
        // NO FALLBACKS - let it fail if data is missing
        if (!botData) throw new Error('[BotHeaderView] botData is null/undefined');
        if (!botData.name && !botData.bot_name) throw new Error('[BotHeaderView] No bot name in response');
        if (!botData.bot_directory) throw new Error('[BotHeaderView] No bot_directory in response');
        if (!botData.workspace_directory) throw new Error('[BotHeaderView] No workspace_directory in response');
        
        const currentBot = botData.name || botData.bot_name;
        const availableBots = botData.available_bots || [];
        const safeBotName = this.escapeHtml(currentBot);
        const safeBotDir = this.escapeHtml(botData.bot_directory);
        const safeWorkspaceDir = this.escapeHtml(botData.workspace_directory);
        console.log('[BotHeaderView] workspace_directory from status:', botData.workspace_directory);
        console.log('[BotHeaderView] Escaped workspace_directory:', safeWorkspaceDir);
        
        // AC: Truncate very long directory paths
        const displayBotDir = this.truncatePath(safeBotDir, maxPathLength);
        const displayWorkspaceDir = this.truncatePath(safeWorkspaceDir, maxPathLength);
        console.log('[BotHeaderView] Display workspace_directory:', displayWorkspaceDir);
        
        // Build bot selector links with pipe separators (Bug #3 fix)
        let botLinksHtml = '';
        if (availableBots && availableBots.length > 0) {
            botLinksHtml = availableBots.map((botName, index) => {
                const isActive = botName === currentBot;
                const activeClass = isActive ? ' active' : '';
                const link = `<a href="javascript:void(0)" class="bot-link${activeClass}" onclick="switchBot('${this.escapeHtml(botName)}')">${this.escapeHtml(botName)}</a>`;
                // Add pipe separator before all links except the first one
                const separator = index > 0 ? '<span style="opacity: 0.5; margin: 0 6px;">|</span>' : '';
                return separator + link;
            }).join('');
        }
        
        // Get the proper webview URIs for images (bundled in extension)
        let imagePath = '';
        let refreshIconPath = '';
        let storyIconPath = '';
        let crcIconPath = '';
        if (this.webview && this.extensionUri) {
            try {
                const iconUri = vscode.Uri.joinPath(this.extensionUri, 'img', 'company_icon.png');
                imagePath = this.webview.asWebviewUri(iconUri).toString();
                console.log('[BotHeaderView] Company icon URI:', imagePath);
                
                const refreshUri = vscode.Uri.joinPath(this.extensionUri, 'img', 'refresh.png');
                refreshIconPath = this.webview.asWebviewUri(refreshUri).toString();
                console.log('[BotHeaderView] Refresh icon URI:', refreshIconPath);
                
                const storyUri = vscode.Uri.joinPath(this.extensionUri, 'img', 'story.png');
                storyIconPath = this.webview.asWebviewUri(storyUri).toString();
                console.log('[BotHeaderView] Story icon URI:', storyIconPath);
                
                const crcUri = vscode.Uri.joinPath(this.extensionUri, 'img', 'crc.png');
                crcIconPath = this.webview.asWebviewUri(crcUri).toString();
                console.log('[BotHeaderView] CRC icon URI:', crcIconPath);
            } catch (err) {
                console.error('[BotHeaderView] Failed to create icon URI:', err);
                console.error('[BotHeaderView] webview:', !!this.webview, 'extensionUri:', !!this.extensionUri, 'extensionUri value:', this.extensionUri?.toString());
            }
        } else {
            console.warn('[BotHeaderView] Missing webview or extensionUri:', { hasWebview: !!this.webview, hasExtensionUri: !!this.extensionUri });
        }
        
        const versionHtml = this.panelVersion 
            ? `<span style="font-size: 14px; opacity: 0.7; margin-left: 6px;">v${this.escapeHtml(this.panelVersion)}</span>`
            : '';
        
        // #region agent log
        fetch('http://127.0.0.1:7242/ingest/cc11718e-e210-436d-8aa6-f3e81dc3fdfc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'bot_header_view.js:146',message:'Before return HTML',data:{panelVersion:this.panelVersion,versionHtml:versionHtml,versionHtmlLength:versionHtml.length},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'VERSION'})}).catch(()=>{});
        // #endregion
        
        return `
    <div class="section card-primary" style="border-top: none; padding-top: 0;">
        <div class="main-header">
            ${imagePath ? `<img src="${imagePath}" class="main-header-icon" alt="Company Icon" onerror="console.error('Failed to load icon:', this.src); this.style.border='1px solid red';" />` : ''}
            <span class="main-header-title">Agile Bots <span style="color: red; font-weight: bold;">TEST-v0.1.49</span> ${versionHtml}</span>
            <button class="main-header-refresh" onclick="refreshStatus()" title="Refresh">
                ${refreshIconPath ? `<img src="${refreshIconPath}" style="width: 36px; height: 36px; object-fit: contain; filter: saturate(1.3) brightness(0.95) hue-rotate(-5deg);" alt="Refresh" />` : ''}
            </button>
        </div>
        <div class="collapsible-section expanded">
            <div class="collapsible-header" onclick="toggleSection('header-content')" style="
                cursor: pointer;
                padding: 4px 5px;
                background-color: transparent;
                border-left: none;
                border-radius: 2px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                user-select: none;
            ">
                <div style="display: flex; align-items: center;">
                    <span class="expand-icon" style="margin-right: 8px; font-size: 28px; transition: transform 0.15s;">▸</span>
                    ${this.currentBot === 'story_bot' && storyIconPath
                        ? `<img src="${storyIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="Story Bot Icon" />`
                        : this.currentBot === 'crc_bot' && crcIconPath
                        ? `<img src="${crcIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="CRC Bot Icon" />`
                        : ''}
                    <span style="font-weight: 600; font-size: 20px;">${safeBotName}</span>
                </div>
                <div class="bot-links" onclick="event.stopPropagation();" style="gap: 6px;">
                    ${botLinksHtml}
                </div>
            </div>
            <div id="header-content" class="collapsible-content" style="max-height: 2000px; overflow: hidden; transition: max-height 0.3s ease;">
                <div class="card-secondary" style="padding: 1px 5px 2px 5px;">
                    <div class="input-container" style="margin-top: 0;">
                        <div class="input-header">Workspace</div>
                        <input type="text" id="workspacePathInput" 
                               value="${safeWorkspaceDir}" 
                               placeholder="Path to workspace"
                               onchange="updateWorkspace(this.value)"
                               onkeydown="if(event.key === 'Enter') { event.preventDefault(); updateWorkspace(this.value); }"
                               title="${safeWorkspaceDir}" />
                    </div>
                    <div class="info-display" style="margin-top: 4px;" title="${safeBotDir}">
                        <span class="label">Bot Path:</span>
                        <span class="value">${displayBotDir}</span>
                    </div>
                </div>
            </div>
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
        if (eventType === 'switchBot') {
            // Switch bot logic would go here
            // For now, just return success
            return { success: true, bot: eventData.botName };
        }
        if (eventType === 'updateWorkspace') {
            console.log('[BotHeaderView] updateWorkspace event received');
            // Execute CLI command to update workspace path
            const newPath = eventData.workspacePath;
            console.log('[BotHeaderView] New workspace path:', newPath);
            if (!newPath) {
                throw new Error('No workspace path provided');
            }
            
            // Execute path command to update workspace (no quotes - CLI parser handles path as arg)
            console.log('[BotHeaderView] Executing path command:', `path ${newPath}`);
            const pathResult = await this.execute(`path ${newPath}`);
            console.log('[BotHeaderView] Path command result:', JSON.stringify(pathResult, null, 2));
            
            // Check if path command failed
            if (pathResult && pathResult.status === 'error') {
                throw new Error(pathResult.message || 'Failed to update workspace');
            }
            
            // Update the static workspace directory
            const PanelView = require('../panel/panel_view');
            console.log('[BotHeaderView] Updating PanelView._workspaceDir to:', newPath);
            PanelView._workspaceDir = newPath;
            
            // Refresh bot status to get updated workspace_directory
            console.log('[BotHeaderView] Fetching updated status...');
            const botStatus = await this.execute('status');
            console.log('[BotHeaderView] Status workspace_directory:', botStatus.workspace_directory);
            
            const result = { 
                success: true, 
                workspace: botStatus.workspace_directory || newPath 
            };
            console.log('[BotHeaderView] Returning result:', JSON.stringify(result, null, 2));
            return result;
        }
        throw new Error(`Unknown event type: ${eventType}`);
    }
}

module.exports = BotHeaderView;
