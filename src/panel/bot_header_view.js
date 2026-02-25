/**
 * BotHeaderView - Renders bot header section with bot name, version, refresh button, and bot selector.
 * 
 * Epic: Invoke Bot Through Panel
 * Sub-Epic: Manage Panel Session
 * Story: Open Panel, Display Session Status, Switch Bot
 */

const PanelView = require('./panel_view');
const branding = require('./branding');
const fs = require('fs');
const { escapeForHtml, truncatePath, Logger } = require('./utils');

class BotHeaderView extends PanelView {
    /**
     * Bot header view.
     * 
     * @param {string|PanelView} botPathOrCli - Bot path or CLI instance
     * @param {string} panelVersion - Panel extension version (optional)
     * @param {Object} webview - VS Code webview instance (optional)
     * @param {Object} extensionUri - Extension URI (optional)
     * @param {Object} parentView - Parent BotView (optional, for accessing cached botData)
     */
    constructor(botPathOrCli, panelVersion, webview, extensionUri, parentView = null) {
        super(botPathOrCli);
        this.panelVersion = panelVersion || null;
        this.webview = webview || null;
        this.extensionUri = extensionUri || null;
        this.parentView = parentView;
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
     * Render bot header HTML.
     * 
     * @returns {string} HTML string
     */
    async render() {
        console.log('[BotHeaderView] Starting render');
        console.log('[BotHeaderView] Panel version:', this.panelVersion);
        console.log('[BotHeaderView] Has webview:', !!this.webview);
        console.log('[BotHeaderView] Has extensionUri:', !!this.extensionUri);
        
        // Use cached botData from parent if available, otherwise fetch it
        let botData;
        try {
            botData = this.parentView?.botData || await this.execute('status');
            console.log('[BotHeaderView] Bot data source:', this.parentView?.botData ? 'cached' : 'fetched');
            console.log('[BotHeaderView] Status response:', JSON.stringify(botData).substring(0, 300));
        } catch (error) {
            console.error('[BotHeaderView] ERROR fetching bot data:', error.message);
            console.error('[BotHeaderView] ERROR stack:', error.stack);
            throw new Error(`[BotHeaderView] Failed to fetch bot data: ${error.message}`);
        }
        
        const vscode = require('vscode');
        const maxPathLength = 80;
        
        // Validate required fields with detailed error messages
        // TO-DO: Should bot_header_view validate this data?
        if (!botData) {
            console.error('[BotHeaderView] botData is null/undefined');
            throw new Error('[BotHeaderView] botData is null/undefined');
        }
        if (!botData.name && !botData.bot_name) {
            const keys = Object.keys(botData).join(', ');
            const dataPreview = JSON.stringify(botData).substring(0, 500);
            console.error(`[BotHeaderView] No bot name in response. Available keys: ${keys}`);
            console.error(`[BotHeaderView] Response data: ${dataPreview}`);
            throw new Error(`[BotHeaderView] No bot name in response. Available keys: ${keys}. Response: ${dataPreview}`);
        }
        if (!botData.bot_directory) {
            console.error('[BotHeaderView] No bot_directory in response');
            throw new Error('[BotHeaderView] No bot_directory in response');
        }
        if (!botData.workspace_directory) {
            console.error('[BotHeaderView] No workspace_directory in response');
            throw new Error('[BotHeaderView] No workspace_directory in response');
        }
        
        const currentBot = botData.name || botData.bot_name;
        const availableBots = botData.available_bots || [];
        const safeBotName = escapeForHtml(currentBot);
        const safeBotDir = escapeForHtml(botData.bot_directory);
        const safeWorkspaceDir = escapeForHtml(botData.workspace_directory);
        
        // AC: Truncate very long directory paths
        const displayBotDir = truncatePath(safeBotDir, maxPathLength);
        const displayWorkspaceDir = truncatePath(safeWorkspaceDir, maxPathLength);
        
        // Build bot selector links
        let botLinksHtml = '';
        if (availableBots && availableBots.length > 0) {
            botLinksHtml = availableBots.map(botName => {
                const isActive = botName === currentBot;
                const activeClass = isActive ? ' active' : '';
                return '<a href="javascript:void(0)" class="bot-link' + activeClass + '" onclick="switchBot(\'' + escapeForHtml(botName) + '\')">' + escapeForHtml(botName) + '</a>';
            }).join('\n                ');
        }
        
        // Get the proper webview URIs for images using branding utility        
        const imagePath = `<img src="${branding.getImageUri(this.webview, this.extensionUri, 'company_icon.png')}" class="main-header-icon" alt="Company Icon" onerror="console.error('Failed to load icon:', this.src); this.style.border='1px solid red';" />`;        
        const refreshIconPath = `<img src="${branding.getImageUri(this.webview, this.extensionUri, 'refresh.png')}" style="width: 36px; height: 36px; object-fit: contain; filter: saturate(1.3) brightness(0.95) hue-rotate(-5deg);" alt="Refresh" />`;
        
        const storyIconPath = branding.getImageUri(this.webview, this.extensionUri, 'story.png');
        const crcIconPath = branding.getImageUri(this.webview, this.extensionUri, 'crc.png');

        let folderBrowseIconPath = branding.getImageUri(this.webview, this.extensionUri, 'folder_browse.png');
        folderBrowseIconPath = folderBrowseIconPath ? `<img src="${folderBrowseIconPath}" alt="Browse" style="width: 36px; height: 36px;" />` : '📁';        
        
        console.log('[BotHeaderView] Branding:', branding.getBranding());
        console.log('[BotHeaderView] Company icon URI:', imagePath);
        
        const versionHtml = this.panelVersion 
            ? `<span style="font-size: 14px; opacity: 0.7; margin-left: 6px;">v${escapeForHtml(this.panelVersion)}</span>`
            : '';
        
        const botIconPath = this.currentBot === 'story_bot' && storyIconPath
                    ? `<img src="${storyIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="Story Bot Icon" />`
                    : this.currentBot === 'crc_bot' && crcIconPath
                    ? `<img src="${crcIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="CRC Bot Icon" />`
                    : '';
        
        const productName = branding.getProductName();
        const titleStyle = branding.getTitleStyle();

        const htmlPath = vscode.Uri.joinPath(this.extensionUri, 'workspace', 'workspace.html');
        let htmlComponentString = fs.readFileSync(htmlPath.fsPath, 'utf-8');   
                
        return htmlComponentString.replace(/\${safeBotName}/g, safeBotName)
            .replace(/\${displayBotDir}/g, displayBotDir)
            .replace(/\${displayWorkspaceDir}/g, displayWorkspaceDir)
            .replace(/\${botIconPath}/g, botIconPath)
            .replace(/\${productName}/g, productName)
            .replace(/\${titleStyle}/g, titleStyle)
            .replace(/\${imagePath}/g, imagePath)
            .replace(/\${refreshIconPath}/g, refreshIconPath)
            .replace(/\${folderBrowseIconPath}/g, folderBrowseIconPath)
            .replace(/\${versionHtml}/g, versionHtml)
            .replace(/\${botLinksHtml}/g, botLinksHtml)
            .replace(/\${safeBotDir}/g, safeBotDir)
            .replace(/\${safeWorkspaceDir}/g, safeWorkspaceDir);
            
    }
    
}

module.exports = BotHeaderView;
