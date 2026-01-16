/**
 * HTML Renderer
 * 
 * Generates HTML/CSS for webview display of status data.
 * Uses VS Code theme-aware CSS variables for styling.
 */

const vscode = require('vscode');
const path = require('path');

class HtmlRenderer {
  constructor() {
    this.escapeHtml = this.escapeHtml.bind(this);
  }

  /**
   * Render complete HTML document for webview
   * @param {object} statusData - Parsed status data
   * @param {object} webview - VS Code webview instance for resource URIs
   * @param {object} extensionUri - Extension URI for bundled resources
   * @returns {string} Complete HTML document
   */
  render(statusData, webview = null, extensionUri = null) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot Status Dashboard</title>
    <style>
        ${this.getStyles()}
    </style>
</head>
<body>
    ${this.renderHeader(statusData.bot, statusData.session, statusData.availableBots || [], statusData.currentBot || 'story_bot', webview, extensionUri)}
    ${this.renderBehaviors(statusData.behaviors, statusData.expansionState || {}, webview, extensionUri)}
    ${this.renderScope(statusData.scope, webview, extensionUri)}
    ${this.renderInstructions(statusData.instructions, statusData.promptContent, webview, extensionUri)}
    ${this.renderScripts()}
</body>
</html>`;
  }

  /**
   * Get CSS styles
   */
  getStyles() {
    return `
        /* ============================================================
           THEME SYSTEM - All styling variables in one place
           ============================================================ */
        
        :root {
            /* Colors */
            --bg-base: #000000;
            --accent-color: #ff8c00;
            --border-color: #ff8c00;
            --divider-color: #ff8c00;
            --hover-bg: rgba(255, 255, 255, 0.03);
            
            /* Input styling - chat-like appearance */
            --input-bg: rgba(255, 255, 255, 0.05);
            --input-bg-focus: rgba(255, 255, 255, 0.08);
            --input-border: rgba(255, 255, 255, 0.1);
            --input-border-focus: var(--accent-color);
            --input-padding: 6px;
            --input-border-radius: 6px;
            --input-border-width: 1px;
            --input-border-width-focus: 2px;
            --input-header-border-width: 1px;
            --input-header-border-width-focus: 2px;
            --input-transition: border-color 150ms ease, background-color 150ms ease;
            
            /* Borders */
            --border-width: 1px;
            --border-radius: 0;
            --border-radius-sm: 0;
            --active-border-width: 2px;
            
            /* Spacing */
            --space-xs: 2px;
            --space-sm: 4px;
            --space-md: 6px;
            --space-lg: 8px;
            
            /* Typography */
            --font-size-base: 13px;
            --font-size-sm: 12px;
            --font-size-xs: 11px;
            --font-size-section: 14px;
            --font-weight-normal: 400;
            --line-height-base: 1.6;
            --line-height-compact: 1.4;
        }
        
        body {
            font-family: var(--vscode-font-family), 'Segoe UI', sans-serif;
            padding: var(--space-md);
            color: var(--vscode-foreground);
            background-color: var(--bg-base);
            line-height: var(--line-height-base);
            margin: 0;
            font-size: var(--font-size-base);
            font-weight: var(--font-weight-normal);
        }
        
        /* ============================================================
           LAYOUT & STRUCTURE
           ============================================================ */
        
        .header {
            border: none;
            padding-bottom: 0;
            margin-bottom: 0;
        }
        .header h1 {
            margin: 0 0 var(--space-xs) 0;
            font-size: var(--font-size-lg);
            color: var(--vscode-foreground);
            font-weight: var(--font-weight-normal);
        }
        .header-info {
            font-size: var(--font-size-sm);
            color: var(--vscode-descriptionForeground);
            margin: var(--space-xs) 0;
        }
        .controls {
            margin-bottom: var(--space-md);
            display: flex;
            gap: var(--space-sm);
        }
        
        button {
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            padding: var(--space-xs) var(--space-md);
            cursor: pointer;
            border-radius: var(--border-radius-sm);
            font-size: var(--font-size-base);
            font-family: inherit;
            transition: all 100ms ease;
        }
        button:hover {
            background-color: var(--vscode-button-hoverBackground);
        }
        button:active {
            background-color: var(--vscode-button-background);
            opacity: 0.8;
            transform: scale(0.98);
        }
        
        /* ============================================================
           CARDS & SECTIONS
           ============================================================ */
        
        .card-primary {
            margin-bottom: var(--space-lg);
            padding: var(--space-lg) 0;
            border: none;
            border-top: var(--border-width) solid var(--divider-color);
            background-color: transparent;
        }
        
        .card-secondary {
            margin: var(--space-sm) 0;
            padding: var(--space-md) 0;
            border: none;
            background-color: transparent;
        }
        
        .card-item {
            margin: var(--space-xs) 0;
            padding: var(--space-xs) var(--space-sm);
            border-radius: 0;
            background-color: transparent;
            transition: background-color 80ms ease;
        }
        .card-item:hover {
            background-color: var(--hover-bg);
        }
        
        .card-item.active,
        .card-secondary.active {
            background-color: transparent;
        }
        
        .section {
            margin-bottom: 0;
            padding: var(--space-lg) 0;
            border: none;
            border-top: var(--border-width) solid var(--divider-color);
            background-color: transparent;
        }
        
        .section.card-primary {
            border-top: var(--border-width) solid var(--divider-color);
        }
        
        .section-title {
            font-weight: var(--font-weight-normal);
            margin-bottom: var(--space-sm);
            font-size: var(--font-size-section);
            color: var(--vscode-foreground);
        }
        
        .section-header {
            padding: var(--space-sm) 0;
            border: none;
            background-color: transparent;
            font-weight: var(--font-weight-normal);
            font-size: var(--font-size-section);
        }
        
        /* ============================================================
           HIERARCHY & COLLAPSIBLE ITEMS
           ============================================================ */
        
        .behavior-item, .action-item, .operation-item {
            margin: var(--space-xs) 0;
            padding: var(--space-xs) var(--space-sm);
            border-radius: var(--border-radius-sm);
            display: flex;
            align-items: center;
            gap: var(--space-sm);
            transition: background-color 80ms ease;
            font-weight: var(--font-weight-normal);
        }
        
        .behavior-item:hover, .action-item:hover {
            background-color: var(--hover-bg);
        }
        
        .collapsible-header {
            margin: var(--space-xs) 0;
            padding: var(--space-sm);
            border-radius: var(--border-radius-sm);
            display: flex;
            align-items: center;
            gap: var(--space-sm);
            cursor: pointer;
            font-weight: var(--font-weight-normal);
            font-size: var(--font-size-base);
            transition: background-color 80ms ease;
        }
        .collapsible-header:hover {
            background-color: var(--hover-bg);
        }
        .collapsible-header.action-item {
            margin-left: var(--space-md);
            font-weight: var(--font-weight-normal);
        }
        .operation-item {
            margin-left: calc(var(--space-md) * 4);
            font-size: var(--font-size-sm);
            color: var(--vscode-descriptionForeground);
        }
        
        .behavior-item.active,
        .action-item.active,
        .operation-item.active {
            background-color: transparent;
        }
        
        .collapsible-section {
            margin-bottom: var(--space-sm);
        }
        
        .collapsible-section .expand-icon {
            transition: transform 150ms ease;
            display: inline-block;
            transform: rotate(0deg);
            font-style: normal;
            min-width: var(--space-md);
            color: #ff8c00 !important;
        }
        .collapsible-section.expanded .expand-icon {
            transform: rotate(90deg);
        }
        .collapsible-content {
            overflow: hidden;
            transition: max-height 0.3s ease;
        }
        
        .status-marker {
            font-family: inherit;
            font-weight: var(--font-weight-normal);
            min-width: 20px;
            font-size: var(--font-size-base);
        }
        
        .scope-section {
            background-color: transparent;
            padding: 0;
            border: none;
        }
        /* ============================================================
           INPUTS & INTERACTIVE ELEMENTS
           ============================================================ */
        
        /* Input container with header like chat code blocks */
        .input-container {
            border: var(--input-border-width) solid var(--accent-color);
            border-radius: var(--input-border-radius);
            overflow: hidden;
            transition: border-width 150ms ease, border-color 150ms ease, background-color 150ms ease;
        }
        .input-container:focus-within {
            border-width: var(--input-border-width-focus);
        }
        
        .input-header {
            padding: 4px var(--input-padding);
            background-color: transparent;
            border-bottom: var(--input-header-border-width) solid var(--accent-color);
            font-size: var(--font-size-base);
            color: var(--vscode-foreground);
            font-weight: 600;
            transition: border-bottom-width 150ms ease;
        }
        .input-container:focus-within .input-header {
            border-bottom-width: var(--input-header-border-width-focus);
        }
        
        /* Info display for read-only fields */
        .info-display {
            padding: var(--space-sm) 0;
            font-size: var(--font-size-base);
            color: var(--vscode-foreground);
        }
        .info-display .label {
            color: var(--vscode-descriptionForeground);
            margin-right: 8px;
        }
        .info-display .value {
            color: var(--vscode-foreground);
        }
        
        /* Main header with company branding */
        .main-header {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 7px 5px 6px 5px;
            border-bottom: 1px solid var(--divider-color);
        }
        .main-header-icon {
            width: 28px;
            height: 28px;
            object-fit: contain;
        }
        .main-header-title {
            font-size: 20px;
            font-weight: 700;
            color: var(--vscode-foreground);
        }
        .main-header-refresh {
            margin-left: auto;
            background-color: transparent;
            border: none;
            color: var(--vscode-foreground);
            font-size: 18px;
            padding: 3px;
            cursor: pointer;
            border-radius: 4px;
            transition: background-color 150ms ease;
        }
        .main-header-refresh:hover {
            background-color: rgba(255, 140, 0, 0.1);
        }
        
        input[type="text"],
        textarea,
        .text-input {
            width: 100%;
            padding: var(--space-sm) var(--input-padding);
            background-color: var(--input-bg);
            color: var(--vscode-foreground);
            border: none;
            border-radius: 0;
            font-family: var(--vscode-editor-font-family, 'Segoe UI', sans-serif);
            font-size: var(--font-size-base);
        }
        textarea {
            resize: vertical;
            min-height: 32px;
            line-height: 1.5;
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-wrap: break-word;
            overflow: hidden;
            box-sizing: border-box;
        }
        input[type="text"]:focus,
        textarea:focus,
        .text-input:focus {
            outline: none;
        }
        
        .scope-filter {
            font-family: var(--vscode-editor-font-family, 'Courier New', monospace);
            font-size: var(--font-size-base);
            margin-top: var(--space-sm);
        }
        .scope-links {
            margin-top: var(--space-sm);
        }
        .scope-links a {
            color: var(--vscode-textLink-foreground);
            text-decoration: none;
            margin-right: var(--space-md);
            font-size: var(--font-size-base);
        }
        .scope-links a:hover {
            text-decoration: underline;
            color: var(--vscode-textLink-activeForeground);
        }
        
        .command-input-container {
            display: flex;
            flex-direction: column;
            gap: var(--space-sm);
        }
        .command-textarea {
            width: 100%;
            padding: var(--input-padding);
            background-color: var(--input-bg);
            color: var(--vscode-foreground);
            border: none;
            border-radius: 0;
            font-family: var(--vscode-editor-font-family, 'Segoe UI', sans-serif);
            font-size: var(--font-size-base);
            resize: none;
            height: 40px;
            line-height: 1.5;
            transition: height 200ms ease;
        }
        .command-textarea:focus {
            outline: none;
            height: 120px;
        }
        .command-textarea.expanded {
            height: 120px;
        }
        
        .execute-button {
            background-color: var(--accent-color);
            color: #000000;
            border: none;
            padding: 4px 10px;
            cursor: pointer;
            border-radius: 4px;
            font-size: var(--font-size-base);
            font-weight: 600;
            font-family: inherit;
            transition: all 100ms ease;
            display: none;
            margin-top: 6px;
            align-self: flex-start;
        }
        .command-input-container.expanded .execute-button {
            display: block;
        }
        .execute-button:hover {
            filter: brightness(1.1);
        }
        .execute-button:active {
            filter: brightness(0.9);
            transform: scale(0.98);
        }
        
        .prompt-display-container {
            margin-top: var(--space-md);
            padding: var(--space-md) 0;
            background-color: transparent;
            border: none;
        }
        .prompt-label {
            font-size: var(--font-size-base);
            font-weight: var(--font-weight-normal);
            color: var(--vscode-foreground);
            margin-bottom: var(--space-sm);
        }
        .prompt-textarea {
            width: 100%;
            padding: var(--input-padding);
            background-color: var(--input-bg);
            color: var(--vscode-foreground);
            border: none;
            border-radius: 0;
            font-family: var(--vscode-editor-font-family, 'Courier New', monospace);
            font-size: var(--font-size-sm);
            resize: vertical;
            min-height: 120px;
            max-height: 300px;
            line-height: 1.5;
        }
        .prompt-textarea:focus {
            outline: none;
        }
        
        /* ============================================================
           UTILITY CLASSES
           ============================================================ */
        
        .commands-footer {
            border: none;
            padding-top: 0;
            margin-top: var(--space-md);
            font-size: var(--font-size-base);
            color: var(--vscode-descriptionForeground);
        }
        .icon {
            font-size: var(--font-size-section);
            margin-right: var(--space-xs);
        }
        .empty-state {
            color: var(--vscode-descriptionForeground);
            font-style: italic;
            padding: var(--space-sm);
        }
        .expand-icon {
            display: inline-block;
            font-size: 14px;
            min-width: var(--space-md);
            color: #ff8c00 !important;
            font-weight: var(--font-weight-normal);
        }
        .tree-icon {
            color: var(--vscode-foreground);
            font-weight: var(--font-weight-normal);
            margin-right: var(--space-xs);
        }
        
        /* ============================================================
           BOT SELECTOR
           ============================================================ */
        
        .bot-selector {
            padding: var(--space-sm) 0;
            margin-bottom: var(--space-md);
            border: none;
        }
        .bot-selector-title {
            font-size: var(--font-size-base);
            color: var(--vscode-descriptionForeground);
            margin-bottom: var(--space-sm);
            font-weight: var(--font-weight-normal);
        }
        .bot-selector-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .bot-links {
            display: flex;
            gap: var(--space-md);
            flex-wrap: wrap;
            align-items: center;
        }
        .refresh-button {
            background: none;
            border: none;
            color: var(--vscode-foreground);
            cursor: pointer;
            font-size: 14px;
            padding: var(--space-xs) var(--space-sm);
            opacity: 0.7;
        }
        .refresh-button:hover {
            opacity: 1;
            background-color: var(--hover-bg);
        }
        .bot-link {
            font-size: var(--font-size-base);
            cursor: pointer;
            text-decoration: underline;
            color: var(--vscode-descriptionForeground);
            opacity: 0.6;
        }
        .bot-link.active {
            color: var(--vscode-foreground);
            font-weight: var(--font-weight-normal);
            text-decoration: none;
            cursor: default;
            opacity: 1;
        }
        .bot-link:not(.active):hover {
            opacity: 0.8;
        }
        .command-suggestion {
            background: rgba(255, 140, 0, 0.1);
            border: 1px solid rgba(255, 140, 0, 0.3);
            border-radius: 4px;
            padding: 2px 4px;
            font-size: 11px;
            color: var(--accent-color);
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .command-suggestion:hover {
            background: rgba(255, 140, 0, 0.2);
            border-color: var(--accent-color);
        }
    `;
  }

  /**
   * Render bot selector section
   * Displays available bots and allows switching between them
   */
  renderBotSelector(availableBots, currentBot, webview = null, extensionUri = null) {
    if (!availableBots || availableBots.length === 0) {
      return '';
    }

    // Get the proper webview URI for the refresh icon
    let refreshIconPath = '';
    if (webview && extensionUri) {
      try {
        const refreshUri = vscode.Uri.joinPath(extensionUri, 'img', 'refresh.png');
        refreshIconPath = webview.asWebviewUri(refreshUri).toString();
      } catch (err) {
        console.error('Failed to create refresh icon URI:', err);
      }
    }

    const botLinks = availableBots.map(botName => {
      const isActive = botName === currentBot;
      const activeClass = isActive ? ' active' : '';
      return `<a href="javascript:void(0)" class="bot-link${activeClass}" onclick="switchBot('${botName}')">${this.escapeHtml(botName)}</a>`;
    }).join('\n        ');

    return `
    <div class="bot-selector">
        <div class="bot-selector-title">Available Bots:</div>
        <div class="bot-selector-row">
            <div class="bot-links">
            ${botLinks}
            </div>
            <button class="refresh-button" onclick="refreshStatus()" title="Refresh">
                ${refreshIconPath ? `<img src="${refreshIconPath}" style="width: 28px; height: 28px; object-fit: contain; filter: saturate(1.3) brightness(0.95) hue-rotate(-5deg);" alt="Refresh" />` : '🔄'}
            </button>
        </div>
    </div>`;
  }

  /**
   * Render header section (now includes bot selector)
   * AC: WHEN bot paths contain special characters THEN panel escapes HTML entities
   * AC: WHEN workspace directory is very long THEN panel truncates with ellipsis
   */
  renderHeader(bot, session, availableBots, currentBot, webview = null, extensionUri = null) {
    const maxPathLength = 80;
    
    // AC: Escape HTML entities for all paths
    const safeBotName = this.escapeHtml(bot.name);
    const safeBotDir = this.escapeHtml(bot.botDirectory);
    const safeWorkspaceName = this.escapeHtml(bot.workspaceName);
    const safeWorkspaceDir = this.escapeHtml(bot.workspaceDirectory);
    
    // AC: Truncate very long directory paths
    const displayBotDir = this.truncatePath(safeBotDir, maxPathLength);
    const displayWorkspaceDir = this.truncatePath(safeWorkspaceDir, maxPathLength);
    
    // Build bot selector HTML if available
    let botLinksHtml = '';
    if (availableBots && availableBots.length > 0) {
      botLinksHtml = availableBots.map(botName => {
        const isActive = botName === currentBot;
        const activeClass = isActive ? ' active' : '';
        return `<a href="javascript:void(0)" class="bot-link${activeClass}" onclick="switchBot('${botName}')">${this.escapeHtml(botName)}</a>`;
      }).join('\n                ');
    }
    
    // Get the proper webview URIs for images (bundled in extension)
    let imagePath = '';
    let refreshIconPath = '';
    let storyIconPath = '';
    let crcIconPath = '';
    if (webview && extensionUri) {
      try {
        const iconUri = vscode.Uri.joinPath(extensionUri, 'img', 'company_icon.png');
        imagePath = webview.asWebviewUri(iconUri).toString();
        console.log('Company icon URI:', imagePath);
        
        const refreshUri = vscode.Uri.joinPath(extensionUri, 'img', 'refresh.png');
        refreshIconPath = webview.asWebviewUri(refreshUri).toString();
        console.log('Refresh icon URI:', refreshIconPath);
        
        const storyUri = vscode.Uri.joinPath(extensionUri, 'img', 'story.png');
        storyIconPath = webview.asWebviewUri(storyUri).toString();
        console.log('Story icon URI:', storyIconPath);
        
        const crcUri = vscode.Uri.joinPath(extensionUri, 'img', 'crc.png');
        crcIconPath = webview.asWebviewUri(crcUri).toString();
        console.log('CRC icon URI:', crcIconPath);
      } catch (err) {
        console.error('Failed to create icon URI:', err);
        imagePath = '';
        refreshIconPath = '';
        storyIconPath = '';
        crcIconPath = '';
      }
    } else {
      console.log('No webview or extensionUri:', { hasWebview: !!webview, hasExtensionUri: !!extensionUri });
    }
    
    return `
    <div class="section card-primary" style="border-top: none; padding-top: 0;">
        <div class="main-header">
            ${imagePath ? `<img src="${imagePath}" class="main-header-icon" alt="Company Icon" onerror="console.error('Failed to load icon:', this.src); this.style.border='1px solid red';" />` : ''}
            <span class="main-header-title">Agile Bots <span style="font-size: 14px; opacity: 0.7; margin-left: 6px;">v0.24.105</span></span>
            <button class="main-header-refresh" onclick="refreshStatus()" title="Refresh">
                ${refreshIconPath ? `<img src="${refreshIconPath}" style="width: 36px; height: 36px; object-fit: contain; filter: saturate(1.3) brightness(0.95) hue-rotate(-5deg);" alt="Refresh" />` : '🔄'}
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
                    ${currentBot === 'story_bot' && storyIconPath
                        ? `<img src="${storyIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="Story Bot Icon" />`
                        : currentBot === 'crc_bot' && crcIconPath
                        ? `<img src="${crcIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="CRC Bot Icon" />`
                        : `<span class="bot-icon" style="margin-right: 8px; font-size: 20px;">${this.getBotIcon(currentBot)}</span>`}
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
   * Render control buttons
   */
  renderControls() {
    return `
    <div class="controls">
        <button onclick="refreshStatus()">🔄 Refresh</button>
        <button onclick="openScope()">💡 View Scope</button>
    </div>`;
  }

  /**
   * Render behaviors hierarchy
   */
  renderBehaviors(behaviors, expansionState, webview = null, extensionUri = null) {
    // Get the proper webview URIs for icons
    let feedbackIconPath = '';
    let gearIconPath = '';
    let plusIconPath = '';
    let subtractIconPath = '';
    let tickIconPath = '';
    let notTickedIconPath = '';
    let leftIconPath = '';
    let pointerIconPath = '';
    let rightIconPath = '';
    if (webview && extensionUri) {
      try {
        const iconUri = vscode.Uri.joinPath(extensionUri, 'img', 'feedback.png');
        feedbackIconPath = webview.asWebviewUri(iconUri).toString();
        
        const gearUri = vscode.Uri.joinPath(extensionUri, 'img', 'gear.png');
        gearIconPath = webview.asWebviewUri(gearUri).toString();
        
        const plusUri = vscode.Uri.joinPath(extensionUri, 'img', 'plus.png');
        plusIconPath = webview.asWebviewUri(plusUri).toString();
        
        const subtractUri = vscode.Uri.joinPath(extensionUri, 'img', 'subtract.png');
        subtractIconPath = webview.asWebviewUri(subtractUri).toString();
        
        const tickUri = vscode.Uri.joinPath(extensionUri, 'img', 'tick.png');
        tickIconPath = webview.asWebviewUri(tickUri).toString();
        
        const notTickedUri = vscode.Uri.joinPath(extensionUri, 'img', 'not_ticked.png');
        notTickedIconPath = webview.asWebviewUri(notTickedUri).toString();
        
        const leftUri = vscode.Uri.joinPath(extensionUri, 'img', 'left.png');
        leftIconPath = webview.asWebviewUri(leftUri).toString();
        
        const pointerUri = vscode.Uri.joinPath(extensionUri, 'img', 'pointer.png');
        pointerIconPath = webview.asWebviewUri(pointerUri).toString();
        
        const rightUri = vscode.Uri.joinPath(extensionUri, 'img', 'right.png');
        rightIconPath = webview.asWebviewUri(rightUri).toString();
      } catch (err) {
        console.error('Failed to create icon URIs:', err);
      }
    }
    
    if (!behaviors || behaviors.length === 0) {
      return `
    <div class="section card-primary">
        <div class="collapsible-section expanded">
            <div class="collapsible-header" onclick="toggleSection('behaviors-content')" style="
                cursor: pointer;
                padding: 4px 5px;
                background-color: transparent;
                border-left: none;
                border-radius: 2px;
                display: flex;
                align-items: center;
                user-select: none;
            ">
                <span class="expand-icon" style="margin-right: 8px; font-size: 28px; transition: transform 0.15s;">▸</span>
                ${feedbackIconPath ? `<img src="${feedbackIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="Behavior Icon" />` : (gearIconPath ? `<img src="${gearIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="Behavior Icon" />` : '<span style="margin-right: 8px; font-size: 20px;">⚙️</span>')}
                <span style="font-weight: 600; font-size: 20px;">Behavior Action Status</span>
            </div>
            <div id="behaviors-content" class="collapsible-content" style="max-height: 2000px; overflow: hidden; transition: max-height 0.3s ease;">
                <div class="card-secondary" style="padding: 5px;">
                    <div class="empty-state">No behaviors available</div>
                    <div style="margin-top: 8px; padding-top: 5px; border-top: none; display: flex; gap: 4px; flex-wrap: wrap;">
                        <button onclick="executeNavigationCommand('back')" title="Back - Go to previous action" style="
                            background-color: var(--vscode-button-secondaryBackground);
                            color: var(--vscode-button-secondaryForeground);
                            border: none;
                            padding: 4px 6px;
                            cursor: pointer;
                            border-radius: 2px;
                            font-size: 16px;
                            font-family: inherit;
                            line-height: 1;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        ">${leftIconPath ? `<img src="${leftIconPath}" style="width: 20px; height: 20px; object-fit: contain;" alt="Back" />` : '⬅️'}</button>
                        <button onclick="executeNavigationCommand('current')" title="Current - Show current action details" style="
                            background-color: var(--vscode-button-secondaryBackground);
                            color: var(--vscode-button-secondaryForeground);
                            border: none;
                            padding: 4px 6px;
                            cursor: pointer;
                            border-radius: 2px;
                            font-size: 16px;
                            font-family: inherit;
                            line-height: 1;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        ">${pointerIconPath ? `<img src="${pointerIconPath}" style="width: 20px; height: 20px; object-fit: contain;" alt="Current" />` : '📍'}</button>
                        <button onclick="executeNavigationCommand('next')" title="Next - Advance to next action" style="
                            background-color: var(--vscode-button-secondaryBackground);
                            color: var(--vscode-button-secondaryForeground);
                            border: none;
                            padding: 4px 6px;
                            cursor: pointer;
                            border-radius: 2px;
                            font-size: 16px;
                            font-family: inherit;
                            line-height: 1;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        ">${rightIconPath ? `<img src="${rightIconPath}" style="width: 20px; height: 20px; object-fit: contain;" alt="Next" />` : '➡️'}</button>
                    </div>
                </div>
            </div>
        </div>
    </div>`;
    }

    const behaviorsHtml = behaviors.map((behavior, bIdx) => {
      const behaviorMarker = behavior.isCurrent 
        ? (tickIconPath ? `<img src="${tickIconPath}" alt="Current" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '<span class="status-marker marker-current">➤</span>')
        : behavior.isCompleted
        ? (tickIconPath ? `<img src="${tickIconPath}" alt="Completed" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '<span class="status-marker marker-completed">☑</span>')
        : (notTickedIconPath ? `<img src="${notTickedIconPath}" alt="Pending" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '<span class="status-marker marker-pending">☐</span>');
      
      const behaviorTooltip = behavior.description ? this.escapeHtml(behavior.description) : '';
      const behaviorId = `behavior-${bIdx}`;
      
      // Expansion logic:
      // 1. If we have saved state for this item, use it (user's explicit choice)
      // 2. Otherwise, expand if current or completed (don't auto-collapse completed items)
      const hasExpansionState = expansionState && (behaviorId in expansionState);
      const behaviorExpanded = hasExpansionState ? expansionState[behaviorId] : (behavior.isCurrent || behavior.isCompleted);
      const behaviorIconSrc = behaviorExpanded ? subtractIconPath : plusIconPath;
      const behaviorIconAlt = behaviorExpanded ? 'Collapse' : 'Expand';
      const behaviorIconClass = behaviorExpanded ? 'expanded' : '';
      const behaviorDisplay = behaviorExpanded ? 'block' : 'none';
      
      const behaviorActiveClass = behavior.isCurrent ? ' active' : '';
      let html = `<div class="collapsible-header card-item${behaviorActiveClass}" title="${behaviorTooltip}"><span id="${behaviorId}-icon" class="${behaviorIconClass}" style="display: inline-block; min-width: 12px; cursor: pointer;" onclick="toggleCollapse('${behaviorId}')" data-plus="${plusIconPath}" data-subtract="${subtractIconPath}">${plusIconPath && subtractIconPath ? `<img src="${behaviorIconSrc}" alt="${behaviorIconAlt}" style="width: 12px; height: 12px; vertical-align: middle;" />` : (behaviorExpanded ? '➖' : '➕')}</span> <span style="cursor: pointer; text-decoration: underline;" onclick="navigateToBehavior('${this.escapeHtml(behavior.name)}')">${behaviorMarker}${this.escapeHtml(behavior.name)}</span></div>`;
      
      // Always create collapsible content, even if empty
      const hasActions = behavior.actions && behavior.actions.length > 0;
      const actionsHtml = hasActions ? behavior.actions.map((action, aIdx) => {
          const actionMarker = action.isCurrent
          ? (tickIconPath ? `<img src="${tickIconPath}" alt="Current" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '<span class="status-marker marker-current">➤</span>')
            : action.isCompleted
          ? (tickIconPath ? `<img src="${tickIconPath}" alt="Completed" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '<span class="status-marker marker-completed">☑</span>')
          : (notTickedIconPath ? `<img src="${notTickedIconPath}" alt="Pending" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '<span class="status-marker marker-pending">☐</span>');
          
        const actionTooltip = action.description ? this.escapeHtml(action.description) : '';
        const actionId = `action-${bIdx}-${aIdx}`;
        const behaviorName = behavior.name;
        
        // Expansion logic:
        // 1. If we have saved state for this item, use it (user's explicit choice)
        // 2. Otherwise, expand if current or completed (don't auto-collapse completed items)
        const hasActionExpansionState = expansionState && (actionId in expansionState);
        const actionExpanded = hasActionExpansionState ? expansionState[actionId] : (action.isCurrent || action.isCompleted);
        const actionIconSrc = actionExpanded ? subtractIconPath : plusIconPath;
        const actionIconAlt = actionExpanded ? 'Collapse' : 'Expand';
        const actionIconClass = actionExpanded ? 'expanded' : '';
        const actionDisplay = actionExpanded ? 'block' : 'none';
        
        const actionActiveClass = action.isCurrent ? ' active' : '';
        let actionHtml = `<div class="collapsible-header action-item card-item${actionActiveClass}" title="${actionTooltip}"><span id="${actionId}-icon" class="${actionIconClass}" style="display: inline-block; min-width: 9px; cursor: pointer;" onclick="toggleCollapse('${actionId}')" data-plus="${plusIconPath}" data-subtract="${subtractIconPath}">${plusIconPath && subtractIconPath ? `<img src="${actionIconSrc}" alt="${actionIconAlt}" style="width: 9px; height: 9px; vertical-align: middle;" />` : (actionExpanded ? '➖' : '➕')}</span> <span style="cursor: pointer; text-decoration: underline;" onclick="navigateToAction('${this.escapeHtml(behaviorName)}', '${this.escapeHtml(action.name)}')">${actionMarker}${this.escapeHtml(action.name)}</span></div>`;
          
        // Always create collapsible content, even if empty
        const hasOperations = action.operations && action.operations.length > 0;
        const operationsHtml = hasOperations ? action.operations.map(op => {
              const opMarker = op.isCurrent
            ? (tickIconPath ? `<img src="${tickIconPath}" alt="Current" style="width: 15px; height: 15px; vertical-align: middle; margin-right: 6px;" />` : '<span class="status-marker marker-current">➤</span>')
                : op.isCompleted
            ? (tickIconPath ? `<img src="${tickIconPath}" alt="Completed" style="width: 15px; height: 15px; vertical-align: middle; margin-right: 6px;" />` : '<span class="status-marker marker-completed">☑</span>')
            : (notTickedIconPath ? `<img src="${notTickedIconPath}" alt="Pending" style="width: 15px; height: 15px; vertical-align: middle; margin-right: 6px;" />` : '<span class="status-marker marker-pending">☐</span>');
          const opTooltip = op.description ? this.escapeHtml(op.description) : '';
          const opClasses = ['operation-item', 'card-item'];
          if (op.isCurrent) {
            opClasses.push('active');
          }
          // Make all operations clickable
          const clickHandler = ` onclick="navigateAndExecute('${this.escapeHtml(behaviorName)}', '${this.escapeHtml(action.name)}', '${this.escapeHtml(op.name)}')" style="cursor: pointer; text-decoration: underline;"`;
          return `<div class="${opClasses.join(' ')}" title="${opTooltip}"${clickHandler}>${opMarker}${this.escapeHtml(op.name)}</div>`;
        }).join('') : '';
        
        actionHtml += `<div id="${actionId}" class="collapsible-content" style="display: ${actionDisplay};">${operationsHtml}</div>`;
          
          return actionHtml;
      }).join('') : '';
      
      html += `<div id="${behaviorId}" class="collapsible-content" style="display: ${behaviorDisplay};">${actionsHtml}</div>`;
      
      return html;
    }).join('');

    return `
    <div class="section card-primary">
        <div class="collapsible-section expanded">
            <div class="collapsible-header" onclick="toggleSection('behaviors-content')" style="
                cursor: pointer;
                padding: 4px 5px;
                background-color: transparent;
                border-left: none;
                border-radius: 2px;
                display: flex;
                align-items: center;
                user-select: none;
            ">
                <span class="expand-icon" style="margin-right: 8px; font-size: 28px; transition: transform 0.15s;">▸</span>
                ${feedbackIconPath ? `<img src="${feedbackIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="Behavior Icon" />` : (gearIconPath ? `<img src="${gearIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="Behavior Icon" />` : '<span style="margin-right: 8px; font-size: 20px;">⚙️</span>')}
                <span style="font-weight: 600; font-size: 20px;">Behavior Action Status</span>
            </div>
            <div id="behaviors-content" class="collapsible-content" style="max-height: 2000px; overflow: hidden; transition: max-height 0.3s ease;">
                <div class="card-secondary" style="padding: 5px;">
                    ${behaviorsHtml}
                    <div style="margin-top: 8px; padding-top: 5px; border-top: none; display: flex; gap: 4px; flex-wrap: wrap;">
                        <button onclick="executeNavigationCommand('back')" title="Back - Go to previous action" style="
                            background-color: var(--vscode-button-secondaryBackground);
                            color: var(--vscode-button-secondaryForeground);
                            border: none;
                            padding: 4px 6px;
                            cursor: pointer;
                            border-radius: 2px;
                            font-size: 16px;
                            font-family: inherit;
                            line-height: 1;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        ">${leftIconPath ? `<img src="${leftIconPath}" style="width: 20px; height: 20px; object-fit: contain;" alt="Back" />` : '⬅️'}</button>
                        <button onclick="executeNavigationCommand('current')" title="Current - Show current action details" style="
                            background-color: var(--vscode-button-secondaryBackground);
                            color: var(--vscode-button-secondaryForeground);
                            border: none;
                            padding: 4px 6px;
                            cursor: pointer;
                            border-radius: 2px;
                            font-size: 16px;
                            font-family: inherit;
                            line-height: 1;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        ">${pointerIconPath ? `<img src="${pointerIconPath}" style="width: 20px; height: 20px; object-fit: contain;" alt="Current" />` : '📍'}</button>
                        <button onclick="executeNavigationCommand('next')" title="Next - Advance to next action" style="
                            background-color: var(--vscode-button-secondaryBackground);
                            color: var(--vscode-button-secondaryForeground);
                            border: none;
                            padding: 4px 6px;
                            cursor: pointer;
                            border-radius: 2px;
                            font-size: 16px;
                            font-family: inherit;
                            line-height: 1;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        ">${rightIconPath ? `<img src="${rightIconPath}" style="width: 20px; height: 20px; object-fit: contain;" alt="Next" />` : '➡️'}</button>
                    </div>
                </div>
            </div>
        </div>
    </div>`;
  }

  /**
   * Render scope section (polymorphic: story tree, file list, or "all")
   */
  renderScope(scope, webview = null, extensionUri = null) {
    const vscode = require('vscode');
    // Get icon URIs for expand/collapse
    let plusIconPath = '';
    let subtractIconPath = '';
    let gearIconPath = '';
    let epicIconPath = '';
    let pageIconPath = '';
    let testTubeIconPath = '';
    let magnifyingGlassIconPath = '';
    let clearIconPath = '';
    if (webview && extensionUri) {
      try {
        const plusUri = vscode.Uri.joinPath(extensionUri, 'img', 'plus.png');
        plusIconPath = webview.asWebviewUri(plusUri).toString();
        
        const subtractUri = vscode.Uri.joinPath(extensionUri, 'img', 'subtract.png');
        subtractIconPath = webview.asWebviewUri(subtractUri).toString();
        
        const gearUri = vscode.Uri.joinPath(extensionUri, 'img', 'gear.png');
        gearIconPath = webview.asWebviewUri(gearUri).toString();
        
        const epicUri = vscode.Uri.joinPath(extensionUri, 'img', 'light_bulb2.png');
        epicIconPath = webview.asWebviewUri(epicUri).toString();
        
        const pageUri = vscode.Uri.joinPath(extensionUri, 'img', 'page.png');
        pageIconPath = webview.asWebviewUri(pageUri).toString();
        
        const testTubeUri = vscode.Uri.joinPath(extensionUri, 'img', 'test_tube.png');
        testTubeIconPath = webview.asWebviewUri(testTubeUri).toString();
        
        const magnifyingGlassUri = vscode.Uri.joinPath(extensionUri, 'img', 'magnifying_glass.png');
        magnifyingGlassIconPath = webview.asWebviewUri(magnifyingGlassUri).toString();
        
        const clearUri = vscode.Uri.joinPath(extensionUri, 'img', 'clear.png');
        clearIconPath = webview.asWebviewUri(clearUri).toString();
      } catch (err) {
        console.error('Failed to create icon URIs:', err);
      }
    }
    const linksHtml = scope.graphLinks && scope.graphLinks.length > 0
      ? scope.graphLinks.map(link => 
          `<a href="javascript:void(0)" onclick="openFile('${this.escapeForJs(link.url)}')" style="color: var(--vscode-foreground); text-decoration: none; margin-left: 6px; font-size: 12px;">${this.escapeHtml(link.text).toLowerCase()}</a>`
        ).join('')
      : '';

    let contentHtml = '';
    let contentSummary = '';
    if ((scope.type === 'story' || scope.type === 'showAll') && scope.content) {
      contentHtml = this.renderStoryTree(scope.content, gearIconPath, epicIconPath, pageIconPath, testTubeIconPath);
      contentSummary = `${scope.content.length} epic${scope.content.length !== 1 ? 's' : ''}`;
    } else if (scope.type === 'files' && scope.content) {
      contentHtml = this.renderFileList(scope.content);
      contentSummary = `${scope.content.length} file${scope.content.length !== 1 ? 's' : ''}`;
    } else {
      contentHtml = '<div class="empty-state">All files in workspace</div>';
      contentSummary = 'all files';
    }

    return `
    <div class="section scope-section card-primary">
        <div class="collapsible-section expanded">
            <div class="collapsible-header" onclick="toggleSection('scope-content')" style="
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
                    ${magnifyingGlassIconPath ? `<img src="${magnifyingGlassIconPath}" style="margin-right: 8px; width: 28px; height: 28px; object-fit: contain;" alt="Scope Icon" />` : '<span style="margin-right: 8px; font-size: 20px;">🔍</span>'}
                    <span style="font-weight: 600; font-size: 20px;">Scope</span>
                    <!-- Clear button: clearIconPath=${!!clearIconPath} -->
                    ${clearIconPath ? `<button onclick="event.stopPropagation(); clearScopeFilter();" style="
                        background: transparent;
                        border: none;
                        padding: 4px 8px;
                        margin-left: 6px;
                        cursor: pointer;
                        display: flex;
                        align-items: center;
                        transition: opacity 0.15s ease;
                    " 
                    onmouseover="this.style.opacity='0.7'" 
                    onmouseout="this.style.opacity='1'"
                    title="Clear scope filter (show all)">
                        <img src="${clearIconPath}" style="width: 24px; height: 24px; object-fit: contain;" alt="Clear Filter" />
                    </button>` : ''}
                </div>
                ${linksHtml ? `<div onclick="event.stopPropagation();" style="display: flex; align-items: center;">${linksHtml}</div>` : ''}
            </div>
            <div id="scope-content" class="collapsible-content" style="max-height: 2000px; overflow: hidden; transition: max-height 0.3s ease;">
                <div class="card-secondary" style="padding: 5px;">
                    <div class="input-container" style="margin-bottom: 6px;">
                        <div class="input-header">Filter</div>
                        <input type="text" id="scopeFilterInput" 
                               value="${this.escapeHtml(scope.filter || '')}" 
                               placeholder="Epic or Story name"
                               onchange="updateFilter(this.value)"
                               onkeydown="if(event.key === 'Enter') { event.preventDefault(); updateFilter(this.value); }" />
                    </div>
                    <input type="hidden" id="plusIconPath" value="${this.escapeHtml(plusIconPath)}" />
                    <input type="hidden" id="subtractIconPath" value="${this.escapeHtml(subtractIconPath)}" />
                    ${contentHtml}
                </div>
            </div>
        </div>
    </div>`;
  }

  renderStoryTree(epics, gearIconPath = '', epicIconPath = '', pageIconPath = '', testTubeIconPath = '') {
    return epics.map((epic, epicIndex) => {
      const epicId = `epic-${epicIndex}`;
      const epicIcon = epicIconPath ? `<img src="${epicIconPath}" style="width: 14px; height: 14px; vertical-align: middle; margin-right: 4px;" alt="Epic" />` : '💡 ';
      let html = `<div style="margin-top: 8px; font-size: 12px;">
        <span class="collapsible-header" onclick="toggleCollapse('${epicId}')" style="cursor: pointer; user-select: none;">
          <span id="${epicId}-icon" style="display: inline-block; min-width: 9px;"><img class="collapse-icon" src="" data-state="collapsed" style="width: 9px; height: 9px; vertical-align: middle;" alt="Expand" /></span> ${epicIcon}${this.escapeHtml(epic.name)}
        </span>
      </div>`;
      
      html += `<div id="${epicId}" class="collapsible-content" style="display: none;">`;
      // Helper function to recursively render a feature (can have nested features)
      const renderFeature = (feature, featureIndex, parentPath, depth = 0) => {
        console.log(`[RENDER_FEATURE] Called for: ${feature.name}, depth: ${depth}, has ${feature.features?.length || 0} nested features, has ${feature.stories?.length || 0} stories`);
        const featureId = `${parentPath}-${featureIndex}`;
        const featureIcon = gearIconPath ? `<img src="${gearIconPath}" style="width: 14px; height: 14px; vertical-align: middle; margin-right: 4px;" alt="Feature" />` : '⚙️ ';
        const featureLinks = (feature.links && feature.links.length > 0) 
          ? ' ' + feature.links.map(link => 
              `<a href="javascript:void(0)" onclick="event.stopPropagation(); openFile('${this.escapeForJs(link.url)}')">[${this.escapeHtml(link.text)}]</a>`
            ).join(' ')
          : '';
        
        const marginLeft = 7 + (depth * 7); // Increase margin for nested features
        
        html += `<div style="margin-left: ${marginLeft}px; margin-top: 4px; font-size: 12px;"><span class="collapsible-header" onclick="toggleCollapse('${featureId}')" style="cursor: pointer; user-select: none;"><span id="${featureId}-icon" style="display: inline-block; min-width: 9px;"><img class="collapse-icon" src="" data-state="collapsed" style="width: 9px; height: 9px; vertical-align: middle;" alt="Expand" /></span> ${featureIcon}${this.escapeHtml(feature.name)}${featureLinks}</span></div>`;
        
        html += `<div id="${featureId}" class="collapsible-content" style="display: none;">`;
        
        // Render nested features if they exist
        if (feature.features && feature.features.length > 0) {
          console.log(`[DEBUG] Rendering ${feature.features.length} nested features for: ${feature.name} at depth ${depth}`);
          feature.features.forEach((nestedFeature, nestedIndex) => {
            console.log(`[DEBUG] - Nested feature: ${nestedFeature.name}`);
            renderFeature(nestedFeature, nestedIndex, featureId, depth + 1);
          });
        } else {
          console.log(`[DEBUG] No nested features for: ${feature.name} (has features: ${!!feature.features}, length: ${feature.features?.length || 0})`);
        }
        
        // Render stories if they exist
        if (feature.stories && feature.stories.length > 0) {
          feature.stories.forEach((story, storyIndex) => {
            const storyId = `${featureId}-story-${storyIndex}`;
            const storyIcon = pageIconPath ? `<img src="${pageIconPath}" style="width: 14px; height: 14px; vertical-align: middle; margin-right: 4px;" alt="Story" />` : '📝 ';
            
            // Check if story has scenarios - if so, make it collapsible
            const hasScenarios = story.scenarios && story.scenarios.length > 0;
            
            html += `<div style="margin-left: ${marginLeft + 7}px; margin-top: 2px; font-size: 12px;">`;
            
            if (hasScenarios) {
              // Collapsible story with scenarios
              html += `<span class="collapsible-header" onclick="toggleCollapse('${storyId}')" style="cursor: pointer; user-select: none;">`;
              html += `<span id="${storyId}-icon" style="display: inline-block; min-width: 9px;"><img class="collapse-icon" src="" data-state="collapsed" style="width: 9px; height: 9px; vertical-align: middle;" alt="Expand" /></span> `;
            }
            
            if (story.links && story.links.length > 0) {
              // First link is the story file itself
              const storyLink = story.links[0];
              html += `<a href="javascript:void(0)" onclick="event.stopPropagation(); openFile('${this.escapeForJs(storyLink.url)}')">${storyIcon}${this.escapeHtml(story.name)}</a>`;
              // Remaining links are test files, etc.
              if (story.links.length > 1) {
                html += ' ' + story.links.slice(1).map(link => 
                  `<a href="javascript:void(0)" onclick="event.stopPropagation(); openFile('${this.escapeForJs(link.url)}')">[${this.escapeHtml(link.text)}]</a>`
                ).join(' ');
              }
            } else {
              html += `${storyIcon}${this.escapeHtml(story.name)}`;
            }
            
            if (hasScenarios) {
              html += `</span>`; // Close collapsible-header span
            }
            
            html += '</div>';
            
            // Render scenarios if they exist
            if (hasScenarios) {
              html += `<div id="${storyId}" class="collapsible-content" style="display: none;">`;
              story.scenarios.forEach((scenario, scenarioIndex) => {
                const testTubeIcon = testTubeIconPath ? `<img src="${testTubeIconPath}" style="width: 14px; height: 14px; vertical-align: middle; margin-right: 4px;" alt="Scenario" />` : '🧪 ';
                html += `<div style="margin-left: ${marginLeft + 21}px; margin-top: 2px; font-size: 12px;">`;
                
                // scenario.test_file now contains the complete absolute path with #test_method
                if (scenario.test_file) {
                  html += `<a href="javascript:void(0)" onclick="event.stopPropagation(); openFile('${this.escapeForJs(scenario.test_file)}')">${testTubeIcon}${this.escapeHtml(scenario.name)}</a>`;
                } else {
                  // No link - just display scenario name
                  html += `${testTubeIcon}${this.escapeHtml(scenario.name)}`;
                }
                
                html += '</div>';
              });
              html += '</div>'; // Close scenario collapsible-content
            }
          });
        }
        
        html += '</div>'; // Close feature collapsible-content
      };
      
      epic.features.forEach((feature, featureIndex) => {
        renderFeature(feature, featureIndex, `epic-${epicIndex}`, 0);
      });
      html += '</div>'; // Close epic collapsible-content
      
      return html;
    }).join('');
  }

  renderFileList(files) {
    return '<div style="margin-top: 5px;">' + files.map(file => 
      `<div style="margin-left: 5px; font-family: monospace; font-size: 12px; margin-top: 2px;">- ${this.escapeHtml(file.path)}</div>`
    ).join('') + '</div>';
  }

  /**
   * Render instructions section
   * Displays the instructions extracted from CLI output
   */
  renderInstructions(instructions, promptContent = '', webview = null, extensionUri = null) {
    if (!instructions || Object.keys(instructions).length === 0) {
      return '';
    }

    // Merge behavior instructions into base_instructions at the top
    if (instructions.behavior && instructions.base_instructions) {
      // Combine behavior at the top of base_instructions
      if (Array.isArray(instructions.behavior) && Array.isArray(instructions.base_instructions)) {
        instructions = { ...instructions, base_instructions: [...instructions.behavior, ...instructions.base_instructions] };
      } else if (typeof instructions.behavior === 'string' && Array.isArray(instructions.base_instructions)) {
        instructions = { ...instructions, base_instructions: [instructions.behavior, ...instructions.base_instructions] };
      } else if (Array.isArray(instructions.behavior) && typeof instructions.base_instructions === 'string') {
        instructions = { ...instructions, base_instructions: [...instructions.behavior, instructions.base_instructions] };
      } else if (typeof instructions.behavior === 'string' && typeof instructions.base_instructions === 'string') {
        instructions = { ...instructions, base_instructions: instructions.behavior + '\n\n' + instructions.base_instructions };
      }
      // Remove the separate behavior key after merging
      delete instructions.behavior;
    } else if (instructions.behavior && !instructions.base_instructions) {
      // If there's only behavior, rename it to base_instructions
      instructions = { ...instructions, base_instructions: instructions.behavior };
      delete instructions.behavior;
    }

    // Load icon images
    let clipboardIconPath = '';
    let documentIconPath = '';
    let lightbulbIconPath = '';
    let lightbulbHeadIconPath = '';
    let bullseyeIconPath = '';
    let storyIconPath = '';
    let botSubmitIconPath = '';
    if (webview && extensionUri) {
      try {
        const clipboardUri = vscode.Uri.joinPath(extensionUri, 'img', 'clipboard.png');
        clipboardIconPath = webview.asWebviewUri(clipboardUri).toString();
        
        const documentUri = vscode.Uri.joinPath(extensionUri, 'img', 'document.png');
        documentIconPath = webview.asWebviewUri(documentUri).toString();
        
        const lightbulbUri = vscode.Uri.joinPath(extensionUri, 'img', 'lightbulb.png');
        lightbulbIconPath = webview.asWebviewUri(lightbulbUri).toString();
        
        const lightbulbHeadUri = vscode.Uri.joinPath(extensionUri, 'img', 'light_bulb_head.png');
        lightbulbHeadIconPath = webview.asWebviewUri(lightbulbHeadUri).toString();
        
        const bullseyeUri = vscode.Uri.joinPath(extensionUri, 'img', 'bullseye.png');
        bullseyeIconPath = webview.asWebviewUri(bullseyeUri).toString();
        
        const storyUri = vscode.Uri.joinPath(extensionUri, 'img', 'story.png');
        storyIconPath = webview.asWebviewUri(storyUri).toString();
        
        const botSubmitUri = vscode.Uri.joinPath(extensionUri, 'img', 'bot submit.png');
        botSubmitIconPath = webview.asWebviewUri(botSubmitUri).toString();
      } catch (err) {
        console.error('Failed to create icon URIs:', err);
      }
    }

    // RESTRUCTURE: Consolidate into EXACTLY 4 sections: Base, Clarify, Strategy, Build
    const restructured = {};

    // 1. BASE INSTRUCTIONS - combine behavior + action + base
    if (instructions.behavior_instructions || instructions.action_instructions || instructions.base_instructions) {
      let baseContent = '';
      
      // Format behavior instructions
      if (instructions.behavior_instructions) {
        baseContent += '**Behavior Instructions**\n\n';
        if (typeof instructions.behavior_instructions === 'string') {
          baseContent += instructions.behavior_instructions;
        } else if (typeof instructions.behavior_instructions === 'object') {
          if (instructions.behavior_instructions.name) {
            baseContent += `**${instructions.behavior_instructions.name}**`;
          }
          if (instructions.behavior_instructions.description) {
            baseContent += `\n\n${instructions.behavior_instructions.description}`;
          }
          if (instructions.behavior_instructions.instructions) {
            baseContent += '\n\n';
            if (Array.isArray(instructions.behavior_instructions.instructions)) {
              baseContent += instructions.behavior_instructions.instructions.map(i => `- ${i}`).join('\n');
            } else {
              baseContent += instructions.behavior_instructions.instructions;
            }
          }
        }
        baseContent += '\n\n';
      }
      
      // Format action instructions
      if (instructions.action_instructions) {
        baseContent += '**Action Instructions**\n\n';
        if (typeof instructions.action_instructions === 'string') {
          baseContent += instructions.action_instructions;
        } else if (typeof instructions.action_instructions === 'object') {
          if (instructions.action_instructions.name) {
            baseContent += `**${instructions.action_instructions.name}**`;
          }
          if (instructions.action_instructions.description) {
            baseContent += `\n\n${instructions.action_instructions.description}`;
          }
          if (instructions.action_instructions.instructions) {
            baseContent += '\n\n';
            if (Array.isArray(instructions.action_instructions.instructions)) {
              baseContent += instructions.action_instructions.instructions.map(i => `- ${i}`).join('\n');
            } else {
              baseContent += instructions.action_instructions.instructions;
            }
          }
        }
        baseContent += '\n\n';
      }
      
      // Add base instructions
      if (instructions.base_instructions) {
        if (Array.isArray(instructions.base_instructions)) {
          baseContent += instructions.base_instructions.map(i => `- ${i}`).join('\n');
        } else if (typeof instructions.base_instructions === 'string') {
          baseContent += instructions.base_instructions;
        }
      }
      
      restructured.base_instructions = baseContent.trim();
    }

    // 2. CLARIFY - Q&A + Evidence
    // Only show when action is 'clarify'
    const currentAction = instructions.action_instructions?.name || '';
    const hasClarificationData = instructions.clarify_instructions?.clarification_data || 
                                  instructions.clarification ||
                                  (instructions.guardrails?.required_context?.key_questions);
    
    // Only show clarify section when we're in clarify action
    if (hasClarificationData && currentAction === 'clarify') {
      restructured.clarify_instructions = {
        clarification_data: instructions.clarify_instructions?.clarification_data || instructions.clarification || {},
        evidence: instructions.clarify_instructions?.evidence || instructions.guardrails?.required_context?.evidence || [],
        guardrails: instructions.guardrails || instructions.clarify_instructions?.guardrails
      };
    }

    // 3. STRATEGY - Decision Criteria + Assumptions (ONLY show during strategy action or when saved strategy exists)
    const hasStrategyData = currentAction === 'strategy' || 
                            instructions.strategy_instructions?.strategy_data || 
                            instructions.strategy;
    if (hasStrategyData) {
      restructured.strategy_instructions = {
        strategy_data: instructions.strategy_instructions?.strategy_data || instructions.strategy,
        strategy_criteria: instructions.strategy_instructions?.strategy_criteria || 
                          instructions.strategy_criteria ||
                          instructions.guardrails?.decision_criteria,
        assumptions: instructions.strategy_instructions?.assumptions || instructions.assumptions,
        action_instructions: instructions.action_instructions
      };
    }

    // 4. BUILD - Knowledge Graph + Rules (ONLY show during build action)
    const buildRelatedKeys = ['schema', 'knowledge_graph_template', 'knowledge_graph_config', 'rules', 'build_instructions'];
    const hasBuildData = buildRelatedKeys.some(key => instructions[key]);
    if (hasBuildData && currentAction === 'build') {
      // Merge knowledge_graph_template and knowledge_graph_config into a single schema object
      let schemaData = instructions.schema || instructions.build_instructions?.schema || {};
      
      // Merge knowledge_graph_template fields
      if (instructions.knowledge_graph_template) {
        schemaData = { ...schemaData, ...instructions.knowledge_graph_template };
      }
      
      // Merge knowledge_graph_config fields
      if (instructions.knowledge_graph_config) {
        schemaData = { ...schemaData, ...instructions.knowledge_graph_config };
      }
      
      restructured.build_instructions = {
        schema: Object.keys(schemaData).length > 0 ? schemaData : null,
        rules: instructions.rules || instructions.build_instructions?.rules || []
      };
    }

    // 5. RENDER - Render Configs (ONLY show during render action)
    if (currentAction === 'render') {
      restructured.render_instructions = {
        render_config: instructions.render_config || null,
        render_config_paths: instructions.render_config_paths || [],
        render_template_paths: instructions.render_template_paths || [],
        render_output_paths: instructions.render_output_paths || []
      };
    }

    // 6. VALIDATE - Rules (ONLY show during validate action)
    if (currentAction === 'validate' && instructions.rules) {
      restructured.validate_instructions = {
        rules: instructions.rules
      };
    }

    // Replace instructions with restructured version
    instructions = restructured;

    // Define colors and display order/names - 6 sections (base + 5 action-specific)
    const propertyConfig = {
      'base_instructions': { name: 'Base Instructions', color: '#ff8c00', icon: '📝', iconPath: documentIconPath, defaultExpanded: true },
      'clarify_instructions': { name: 'Clarify', color: '#569cd6', icon: '❓', iconPath: lightbulbHeadIconPath, defaultExpanded: false },
      'strategy_instructions': { name: 'Strategy', color: '#c586c0', icon: '💡', iconPath: lightbulbIconPath, defaultExpanded: false },
      'build_instructions': { name: 'Build', color: '#4ec9b0', icon: '🔨', iconPath: bullseyeIconPath, defaultExpanded: false },
      'render_instructions': { name: 'Render', color: '#ce9178', icon: '🎨', iconPath: documentIconPath, defaultExpanded: false },
      'validate_instructions': { name: 'Validate', color: '#dcdcaa', icon: '✓', iconPath: lightbulbHeadIconPath, defaultExpanded: false }
    };

    // Get only the 4 main sections in order
    const validKeys = Object.keys(propertyConfig).filter(key => {
      const value = instructions[key];
      if (value === null || value === undefined) return false;
      if (typeof value === 'string' && value.trim() === '') return false;
      if (Array.isArray(value) && value.length === 0) return false;
      if (typeof value === 'object' && Object.keys(value).length === 0) return false;
      return true;
    });

    if (validKeys.length === 0) {
      return '';
    }

    // Generate collapsible sections for each property
    const sections = validKeys.map((key, index) => {
      const value = instructions[key];
      const config = propertyConfig[key] || { 
        name: this._formatPropertyName(key), 
        color: '#4ec9b0', 
        icon: '📄',
        iconPath: storyIconPath,
        defaultExpanded: false 
      };
      
      const sectionId = `instr-section-${index}`;
      const expanded = config.defaultExpanded ? 'true' : 'false';
      const expandedClass = config.defaultExpanded ? 'expanded' : '';
      
      // Format the content based on type
      let contentHtml;
      if (key === 'clarify_instructions') {
        contentHtml = this._formatClarifyInstructions(value);
      } else if (key === 'strategy_instructions') {
        contentHtml = this._formatStrategyInstructions(value);
      } else if (key === 'build_instructions') {
        contentHtml = this._formatBuildInstructions(value);
      } else if (key === 'render_instructions') {
        contentHtml = this._formatRenderInstructions(value);
      } else if (key === 'validate_instructions') {
        contentHtml = this._formatValidateInstructions(value);
      } else if (key === 'combined_behavior_action_instructions') {
        contentHtml = this._formatCombinedInstructions(value);
      } else {
        contentHtml = this._formatInstructionValue(value, config.color);
      }
      
      // Determine icon display - use image if available, fallback to emoji
      const iconHtml = config.iconPath 
        ? `<img src="${config.iconPath}" style="margin-right: 8px; width: 20px; height: 20px; object-fit: contain; vertical-align: middle;" alt="${config.name}" />`
        : `<span style="margin-right: 8px; font-size: 16px;">${config.icon}</span>`;
      
      return `
        <div class="collapsible-section ${expandedClass}" style="margin-bottom: 8px;">
          <div class="collapsible-header" onclick="toggleSection('${sectionId}')" style="
            cursor: pointer;
            padding: 4px 5px;
            background-color: transparent;
            border-left: none;
            border-radius: 2px;
            display: flex;
            align-items: center;
            user-select: none;
          ">
            <span class="expand-icon" style="margin-right: 8px; font-size: 28px; transition: transform 0.15s;">▸</span>
            ${iconHtml}
            <span style="font-weight: 600; color: var(--vscode-foreground); font-size: 14px;">${config.name}</span>
          </div>
          <div id="${sectionId}" class="collapsible-content" style="
            max-height: ${config.defaultExpanded ? 'none' : '0'};
            overflow: ${config.defaultExpanded ? 'visible' : 'hidden'};
            transition: max-height 0.3s ease;
          ">
            <div style="padding: 5px; background-color: transparent; margin-top: 2px;">
              ${contentHtml}
            </div>
          </div>
        </div>`;
    }).join('');

    // Escape prompt content for safe embedding in HTML attribute
    const promptContentStr = typeof promptContent === 'string' ? promptContent : (promptContent ? String(promptContent) : '');
    const escapedPromptContent = promptContentStr.replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '\\"').replace(/\n/g, '\\n').replace(/\r/g, '\\r');
    
    return `
    <div class="section card-primary">
        <div class="collapsible-section expanded">
            <div class="collapsible-header" style="
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
                <div style="display: flex; align-items: center;" onclick="toggleSection('instructions-content')">
                    <span class="expand-icon" style="margin-right: 8px; font-size: 28px; transition: transform 0.15s;">▸</span>
                    ${clipboardIconPath ? `<img src="${clipboardIconPath}" style="margin-right: 8px; width: 28px; height: 28px; object-fit: contain;" alt="Instructions Icon" />` : '<span style="margin-right: 8px; font-size: 20px;">📋</span>'}
                    <span style="font-weight: 600; font-size: 20px;">Instructions</span>
                </div>
                <button id="submit-to-chat-btn" onclick="sendInstructionsToChat(event)" style="
                    background: rgba(255, 140, 0, 0.15);
                    border: none;
                    border-radius: 8px;
                    padding: 6px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: all 0.15s ease;
                    width: 48px;
                    height: 48px;
                    ${!promptContentStr ? 'opacity: 0.5; cursor: not-allowed;' : ''}
                " 
                onmouseover="this.style.backgroundColor='rgba(255, 140, 0, 0.3)'" 
                onmouseout="this.style.backgroundColor='rgba(255, 140, 0, 0.15)'"
                title="${promptContentStr ? 'Submit instructions to chat' : 'Run instructions command first'}">
                    ${botSubmitIconPath ? `<img src="${botSubmitIconPath}" style="width: 100%; height: 100%; object-fit: contain;" alt="Submit to Chat" />` : '<span style="font-size: 28px;">🤖</span>'}
                </button>
                <script>
                    window._promptContent = ${JSON.stringify(promptContentStr)};
                </script>
            </div>
            <div id="instructions-content" class="collapsible-content" style="max-height: 600px; overflow-y: auto; overflow-x: hidden; transition: max-height 0.3s ease;">
                <div class="card-secondary" style="padding: 5px 10px;">
                    ${sections}
                    
                    <!-- Raw Instructions Subsection -->
                    <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1);">
                        <div class="collapsible-section">
                            <div class="collapsible-header" style="
                                cursor: pointer;
                                padding: 8px 0;
                                display: flex;
                                align-items: center;
                                user-select: none;
                            " onclick="toggleSection('raw-instructions-content')">
                                <span class="expand-icon" style="margin-right: 8px; font-size: 20px; transition: transform 0.15s;">▸</span>
                                <img src="${webview && extensionUri ? webview.asWebviewUri(vscode.Uri.joinPath(extensionUri, 'img', 'copy.png')).toString() : ''}" 
                                     style="margin-right: 8px; width: 20px; height: 20px; object-fit: contain; opacity: 0.9;" 
                                     alt="Raw" 
                                     onerror="this.style.display='none'; this.nextElementSibling.style.display='inline';" />
                                <span style="margin-right: 8px; font-size: 14px; display: none;">📄</span>
                                <span style="font-weight: 600; font-size: 14px;">Raw Instructions (Test)</span>
                            </div>
                            <div id="raw-instructions-content" class="collapsible-content" style="max-height: 0; overflow: hidden; transition: max-height 0.3s ease;">
                                <div style="padding: 5px 0; margin-top: 8px;">
                                    <pre style="
                                        white-space: pre-wrap;
                                        word-wrap: break-word;
                                        font-family: 'Courier New', monospace;
                                        font-size: 11px;
                                        line-height: 1.4;
                                        color: rgba(255,255,255,0.8);
                                        background: rgba(0,0,0,0.3);
                                        padding: 6px;
                                        border-radius: 4px;
                                        margin: 0;
                                        max-height: 400px;
                                        overflow-y: auto;
                                    ">${promptContentStr ? promptContentStr.replace(/</g, '&lt;').replace(/>/g, '&gt;') : 'Click 🤖 Submit button or run an instructions command to populate'}</pre>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>`;
  }

  _formatPropertyName(key) {
    // Convert snake_case or camelCase to Title Case
    return key
      .replace(/_/g, ' ')
      .replace(/([A-Z])/g, ' $1')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
      .trim();
  }

  _getValueSummary(value) {
    if (Array.isArray(value)) {
      return `${value.length} items`;
    } else if (typeof value === 'object' && value !== null) {
      const keys = Object.keys(value);
      return `${keys.length} properties`;
    } else if (typeof value === 'string') {
      return `${value.length} chars`;
    }
    return '';
  }

  _formatClarifyInstructions(value) {
    // Format clarify-specific instructions - Q&A and evidence
    if (typeof value !== 'object' || !value) {
      return this.escapeHtml(String(value));
    }

    let html = '';
    let questions = [];
    let evidence = [];

    // Determine source of questions and answers
    if (value.clarification_data && Array.isArray(value.clarification_data) && value.clarification_data.length > 0) {
      // Use clarification.json if present
      questions = value.clarification_data;
    } else if (value.guardrails && value.guardrails.required_context && Array.isArray(value.guardrails.required_context.key_questions)) {
      // Use guardrails questions if clarification.json not present
      questions = value.guardrails.required_context.key_questions.map(q => ({
        question: q,
        answer: ''
      }));
    }

    // Get evidence
    if (value.clarification_data && Array.isArray(value.clarification_data) && value.clarification_data.length > 0) {
      // Evidence from clarification.json
      evidence = value.evidence || [];
    } else if (value.guardrails && value.guardrails.required_context && Array.isArray(value.guardrails.required_context.evidence)) {
      // Evidence from guardrails
      evidence = value.guardrails.required_context.evidence;
    }

    // Render Q&A Section - questions with editable answer textboxes
    if (questions.length > 0) {
      questions.forEach((item, idx) => {
        const questionText = typeof item === 'string' ? item : item.question;
        const answerText = typeof item === 'object' ? (item.answer || '') : '';
        
        if (questionText) {
          html += `<div class="input-container" style="margin-top: ${idx > 0 ? '12px' : '0'};">`;
          html += `<div class="input-header">${this.escapeHtml(questionText)}</div>`;
          html += `<textarea id="clarify-answer-${idx}" rows="3" style="width: 100%; padding: var(--input-padding); background-color: var(--input-bg); border: none; color: var(--vscode-foreground); resize: vertical; font-family: inherit; font-size: var(--font-size-base);">${this.escapeHtml(answerText)}</textarea>`;
          html += `</div>`;
        }
      });
    }

    // Render Evidence Section
    if (evidence.length > 0) {
      html += '<div style="margin-top: 8px;">';
      html += '<div class="input-header">Evidence</div>';
      html += '<div style="margin-top: 8px;">';
      evidence.forEach(item => {
        html += `<div style="margin-bottom: 4px;">• ${this.escapeHtml(String(item))}</div>`;
      });
      html += '</div>';
      html += '</div>';
    }

    return html;
  }

  _formatStrategyInstructions(value) {
    // Format strategy-specific instructions - decision criteria and assumptions
    if (typeof value !== 'object' || !value) {
      return this.escapeHtml(String(value));
    }

    console.log('[DEBUG] Strategy Instructions value:', JSON.stringify(value, null, 2));

    let html = '';
    let strategyCriteriaObj = {};
    let selectedOption = null;
    let assumptions = '';

    // Determine source of strategy data
    if (value.strategy_data && value.strategy_data.decision_criteria) {
      // Use strategy.json if present (saved decisions)
      strategyCriteriaObj = value.strategy_data.decision_criteria;
      selectedOption = value.strategy_data.selected_option || null;
      assumptions = value.strategy_data.assumptions || '';
    } else if (value.strategy_criteria && Object.keys(value.strategy_criteria).length > 0) {
      // Use strategy_criteria from instructions if strategy.json not present
      strategyCriteriaObj = value.strategy_criteria;
      selectedOption = null;
      assumptions = value.assumptions || '';
    } else {
      // No structured decision criteria - just extract assumptions
      assumptions = value.assumptions || '';
    }

    // Render Decision Criteria - radio buttons
    // strategyCriteriaObj format: { 'key1': {question: '...', options: [...], outcome: '...'}, ... }
    const criteriaKeys = Object.keys(strategyCriteriaObj);
    if (criteriaKeys.length > 0) {
      criteriaKeys.forEach((criteriaKey, criteriaIdx) => {
        const criteria = strategyCriteriaObj[criteriaKey];
        if (typeof criteria === 'object' && criteria !== null) {
          html += '<div style="margin-bottom: 10px;">';
          
          // Render the question as header
          const question = criteria.question || criteriaKey;
          html += `<div class="input-header">${this.escapeHtml(question)}</div>`;
          
          // Render options as radio buttons
          const options = criteria.options || [];
          if (options.length > 0) {
            html += '<div style="margin-top: 8px;">';
            options.forEach((option, optionIdx) => {
              const radioName = `decision-criteria-${criteriaIdx}`;
              const isSelected = selectedOption !== null && selectedOption === optionIdx;
              
              // Extract option text (could be string or object with 'name' field)
              let optionText = '';
              if (typeof option === 'string') {
                optionText = option;
              } else if (typeof option === 'object' && option !== null) {
                optionText = option.name || option.id || JSON.stringify(option);
              }
              
              html += `<div style="margin-bottom: 8px;">`;
              html += `<label style="display: flex; align-items: flex-start; cursor: pointer;">`;
              html += `<input type="radio" name="${radioName}" value="${optionIdx}" ${isSelected ? 'checked' : ''} style="margin-right: 8px; margin-top: 4px; cursor: pointer;" />`;
              html += `<span style="flex: 1;">${this.escapeHtml(optionText)}</span>`;
              html += `</label>`;
              html += `</div>`;
            });
            html += '</div>';
          }
          
          html += '</div>';
        }
      });
    }

    // Render Assumptions - editable textarea
    html += '<div class="input-container" style="margin-top: 6px;">';
    html += '<div class="input-header">Assumptions</div>';
    const assumptionsText = Array.isArray(assumptions) 
      ? assumptions.join('\n') 
      : String(assumptions);
    html += `<textarea id="strategy-assumptions" rows="5" style="width: 100%; padding: var(--input-padding); background-color: var(--input-bg); border: none; color: var(--vscode-foreground); resize: vertical; font-family: inherit; font-size: var(--font-size-base);">${this.escapeHtml(assumptionsText)}</textarea>`;
    html += '</div>';

    return html;
  }

  _formatBuildInstructions(value) {
    // Format build-specific instructions - Knowledge Graph and Rules only
    if (typeof value !== 'object' || !value) {
      return this.escapeHtml(String(value));
    }

    let html = '';

    // Knowledge Graph Section - collapsible
    if (value.schema) {
      html += '<div style="margin-bottom: 8px;">';
      html += '<div style="margin-bottom: 8px; cursor: pointer; display: flex; align-items: center;" onclick="toggleSection(\'build-kg-section\')">';
      html += '<span class="expand-icon" style="margin-right: 8px; font-size: 20px; transition: transform 0.15s;">▸</span>';
      html += '<strong style="font-size: 14px;">Knowledge Graph</strong>';
      html += '</div>';
      html += '<div id="build-kg-section" class="collapsible-content" style="max-height: 0; overflow: hidden; transition: max-height 0.3s ease;">';
      html += '<div style="padding-left: 14px;">';
      html += this._formatBuildKnowledgeGraph(value.schema);
      html += '</div>';
      html += '</div>';
      html += '</div>';
    }

    // Rules Section - collapsible
    if (value.rules && Array.isArray(value.rules) && value.rules.length > 0) {
      html += '<div style="margin-bottom: 8px;">';
      html += '<div style="margin-bottom: 8px; cursor: pointer; display: flex; align-items: center;" onclick="toggleSection(\'build-rules-section\')">';
      html += '<span class="expand-icon" style="margin-right: 8px; font-size: 20px; transition: transform 0.15s;">▸</span>';
      html += '<strong style="font-size: 14px;">Rules</strong>';
      html += '</div>';
      html += '<div id="build-rules-section" class="collapsible-content" style="max-height: 0; overflow: hidden; transition: max-height 0.3s ease;">';
      html += '<div style="padding-left: 14px;">';
      html += this._formatBuildRules(value.rules);
      html += '</div>';
      html += '</div>';
      html += '</div>';
    }

    return html;
  }

  _formatBuildKnowledgeGraph(data) {
    const path = require('path');
    if (!data) return '';

    // Merge all items into one - get template, output filename, path directory, and exists
    let mergedItem = {
      template_path: null,
      output_file: null,
      path_dir: null,
      exists: null
    };

    if (Array.isArray(data)) {
      data.forEach(item => {
        if (typeof item === 'object' && item !== null) {
          if (item.template_path && !mergedItem.template_path) {
            mergedItem.template_path = item.template_path;
          }
          // Only use item.template as fallback if it looks like a full path (contains path separators)
          if (item.template && !mergedItem.template_path && (item.template.includes('/') || item.template.includes('\\'))) {
            mergedItem.template_path = item.template;
          }
          if (item.output && !mergedItem.output_file) {
            mergedItem.output_file = item.output;
          }
          if (item.path && !mergedItem.path_dir) {
            mergedItem.path_dir = item.path;
          }
          if (item.exists !== undefined && mergedItem.exists === null) {
            mergedItem.exists = item.exists;
          }
        }
      });
    } else if (typeof data === 'object' && data !== null) {
      if (data.template_path) mergedItem.template_path = data.template_path;
      // Only use data.template as fallback if it looks like a full path (contains path separators)
      if (data.template && !mergedItem.template_path && (data.template.includes('/') || data.template.includes('\\'))) {
        mergedItem.template_path = data.template;
      }
      if (data.output) mergedItem.output_file = data.output;
      if (data.path) mergedItem.path_dir = data.path;
      if (data.exists !== undefined) mergedItem.exists = data.exists;
    }

    // Remove nulls
    Object.keys(mergedItem).forEach(key => {
      if (mergedItem[key] === null) delete mergedItem[key];
    });

    let html = '';
    // Template - show filename, link to full path
    if (mergedItem.template_path) {
      html += `<div class="info-display" style="margin-top: 4px;" title="${this.escapeHtml(mergedItem.template_path)}">`;
      html += `<span class="label">Template:</span>`;
      html += `<span class="value">${this.renderFileLink(mergedItem.template_path)}</span>`;
      html += '</div>';
    }
    // Output - show filename, link to full path (path_dir + output_file)
    if (mergedItem.output_file) {
      const fullOutputPath = mergedItem.path_dir ? path.join(mergedItem.path_dir, mergedItem.output_file) : mergedItem.output_file;
      html += `<div class="info-display" style="margin-top: 4px;" title="${this.escapeHtml(fullOutputPath)}">`;
      html += `<span class="label">Output:</span>`;
      html += `<span class="value">${this.renderFileLink(fullOutputPath)}</span>`;
      html += '</div>';
    }
    // Path - show directory path as clickable link
    if (mergedItem.path_dir) {
      html += `<div class="info-display" style="margin-top: 4px;" title="${this.escapeHtml(mergedItem.path_dir)}">`;
      html += `<span class="label">Path:</span>`;
      const jsEscapedPath = mergedItem.path_dir.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
      html += `<span class="value"><a href="#" onclick="openFile('${jsEscapedPath}'); return false;" style="color: var(--vscode-textLink-foreground); text-decoration: none; cursor: pointer;">${this.escapeHtml(mergedItem.path_dir)}</a></span>`;
      html += '</div>';
    }
    // Existing - Yes/No
    if (mergedItem.exists !== undefined) {
      html += `<div class="info-display" style="margin-top: 4px;">`;
      html += `<span class="label">Existing:</span>`;
      html += `<span class="value">${mergedItem.exists ? 'Yes' : 'No'}</span>`;
      html += '</div>';
    }
    return html;
  }

  _formatBuildRules(rules) {
    if (!Array.isArray(rules) || rules.length === 0) return '';

    let html = '';
    rules.forEach((rule, idx) => {
      const rulePath = typeof rule === 'string' ? rule : rule.rule_file || '';
      if (rulePath) {
        html += `<div class="info-display" style="margin-top: 4px;" title="${this.escapeHtml(rulePath)}">`;
        html += `<span class="label">Rule ${idx + 1}:</span>`;
        html += `<span class="value">${this.renderFileLink(rulePath)}</span>`;
        html += '</div>';
      }
    });
    return html;
  }

  renderFileLink(fullPath) {
    if (!fullPath) return '';
    const fileName = fullPath.split(/[\/\\]/).pop();
    const jsEscapedPath = fullPath.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
    return `<a href="#" onclick="openFile('${jsEscapedPath}'); return false;" style="color: var(--vscode-textLink-foreground); text-decoration: none; cursor: pointer;">${this.escapeHtml(fileName)}</a>`;
  }

  _formatRenderInstructions(value) {
    // Format render-specific instructions - Render Configs
    if (typeof value !== 'object' || !value) {
      return this.escapeHtml(String(value));
    }

    let html = '';

    // Render Config Paths (similar to Build rules)
    if (Array.isArray(value.render_config_paths) && value.render_config_paths.length > 0) {
      value.render_config_paths.forEach((configPath, idx) => {
        html += `<div class="info-display" style="margin-top: 4px;" title="${this.escapeHtml(configPath)}">`;
        html += `<span class="label">Config ${idx + 1}:</span>`;
        html += `<span class="value">${this.renderFileLink(configPath)}</span>`;
        html += '</div>';
      });
    }

    // Render Template Paths (similar to Build template_path)
    if (Array.isArray(value.render_template_paths) && value.render_template_paths.length > 0) {
      value.render_template_paths.forEach((templatePath, idx) => {
        html += `<div class="info-display" style="margin-top: 4px;" title="${this.escapeHtml(templatePath)}">`;
        html += `<span class="label">Template ${idx + 1}:</span>`;
        html += `<span class="value">${this.renderFileLink(templatePath)}</span>`;
        html += '</div>';
      });
    }

    // Render Output Paths (drawio, md, txt files)
    if (Array.isArray(value.render_output_paths) && value.render_output_paths.length > 0) {
      value.render_output_paths.forEach((outputPath, idx) => {
        html += `<div class="info-display" style="margin-top: 4px;" title="${this.escapeHtml(outputPath)}">`;
        html += `<span class="label">Output ${idx + 1}:</span>`;
        html += `<span class="value">${this.renderFileLink(outputPath)}</span>`;
        html += '</div>';
      });
    }

    // Render Config Section - similar to Knowledge Graph
    if (value.render_config) {
      const configs = Array.isArray(value.render_config) ? value.render_config : [value.render_config];
      
      configs.forEach((config, idx) => {
        html += '<div style="margin-bottom: 8px;">';
        html += `<div style="margin-bottom: 8px; cursor: pointer; display: flex; align-items: center;" onclick="toggleSection('render-config-section-${idx}')">`;
        html += '<span class="expand-icon" style="margin-right: 8px; font-size: 20px; transition: transform 0.15s;">▸</span>';
        html += `<strong style="font-size: 14px;">Render Config ${configs.length > 1 ? idx + 1 : ''}</strong>`;
        html += '</div>';
        html += `<div id="render-config-section-${idx}" class="collapsible-content" style="max-height: 0; overflow: hidden; transition: max-height 0.3s ease;">`;
        html += '<div style="padding-left: 14px;">';
        html += this._formatRenderConfig(config);
        html += '</div>';
        html += '</div>';
        html += '</div>';
      });
    }

    return html;
  }

  _formatRenderConfig(config) {
    const path = require('path');
    if (!config) return '';

    let html = '';
    
    // Template
    if (config.template_path || config.template) {
      const templatePath = config.template_path || config.template;
      html += `<div class="info-display" style="margin-top: 4px;" title="${this.escapeHtml(templatePath)}">`;
      html += `<span class="label">Template:</span>`;
      html += `<span class="value">${this.renderFileLink(templatePath)}</span>`;
      html += '</div>';
    }
    
    // Output
    if (config.output || config.output_file) {
      const outputFile = config.output || config.output_file;
      const fullOutputPath = config.path ? path.join(config.path, outputFile) : outputFile;
      html += `<div class="info-display" style="margin-top: 4px;" title="${this.escapeHtml(fullOutputPath)}">`;
      html += `<span class="label">Output:</span>`;
      html += `<span class="value">${this.renderFileLink(fullOutputPath)}</span>`;
      html += '</div>';
    }
    
    // Path
    if (config.path || config.path_dir) {
      const dirPath = config.path || config.path_dir;
      html += `<div class="info-display" style="margin-top: 4px;" title="${this.escapeHtml(dirPath)}">`;
      html += `<span class="label">Path:</span>`;
      const jsEscapedPath = dirPath.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
      html += `<span class="value"><a href="#" onclick="openFile('${jsEscapedPath}'); return false;" style="color: var(--vscode-textLink-foreground); text-decoration: none; cursor: pointer;">${this.escapeHtml(dirPath)}</a></span>`;
      html += '</div>';
    }
    
    // Existing
    if (config.exists !== undefined) {
      html += `<div class="info-display" style="margin-top: 4px;">`;
      html += `<span class="label">Existing:</span>`;
      html += `<span class="value">${config.exists ? 'Yes' : 'No'}</span>`;
      html += '</div>';
    }
    
    return html;
  }

  _formatValidateInstructions(value) {
    // Format validate-specific instructions - Rules only
    if (typeof value !== 'object' || !value) {
      return this.escapeHtml(String(value));
    }

    let html = '';

    // Rules Section - collapsible
    if (value.rules && Array.isArray(value.rules) && value.rules.length > 0) {
      html += '<div style="margin-bottom: 8px;">';
      html += '<div style="margin-bottom: 8px; cursor: pointer; display: flex; align-items: center;" onclick="toggleSection(\'validate-rules-section\')">';
      html += '<span class="expand-icon" style="margin-right: 8px; font-size: 20px; transition: transform 0.15s;">▸</span>';
      html += '<strong style="font-size: 14px;">Rules</strong>';
      html += '</div>';
      html += '<div id="validate-rules-section" class="collapsible-content" style="max-height: 0; overflow: hidden; transition: max-height 0.3s ease;">';
      html += '<div style="padding-left: 14px;">';
      html += this._formatBuildRules(value.rules);
      html += '</div>';
      html += '</div>';
      html += '</div>';
    }

    return html;
  }

  _formatInstructionValue(value, borderColor) {
    if (Array.isArray(value)) {
      // Array: join with newlines and format
      const text = value.join('\n');
      return this.escapeHtml(text)
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    } else if (typeof value === 'object' && value !== null) {
      // Check if this is clarification data with phase-based structure (e.g., shape.key_questions.answers)
      const phaseKeys = Object.keys(value);
      for (const phaseKey of phaseKeys) {
        const phaseData = value[phaseKey];
        if (phaseData && typeof phaseData === 'object' && phaseData.key_questions && phaseData.key_questions.answers) {
          return this._formatClarificationData(value, borderColor);
        }
      }
      
      // Check if this is direct key_questions.answers structure
      if (value.key_questions && value.key_questions.answers) {
        return this._formatQuestionsAndAnswers(value.key_questions.answers, borderColor);
      }
      
      // Check if this is strategy data with assumptions structure
      if (value.assumptions && (value.assumptions.assumptions || value.assumptions.review_status)) {
        return this._formatStrategyData(value, borderColor);
      }
      
      // Object: pretty print JSON
      return `<pre style="margin: 0; white-space: pre-wrap; font-family: monospace; font-size: 11px; line-height: 1.4;">${this.escapeHtml(JSON.stringify(value, null, 2))}</pre>`;
    } else {
      // String or other: escape and format
      return this.escapeHtml(String(value))
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    }
  }

  _formatClarificationData(clarificationData, borderColor) {
    if (!clarificationData || typeof clarificationData !== 'object') {
      return '<div style="color: var(--vscode-descriptionForeground); font-style: italic;">No clarification data available</div>';
    }

    let html = '';

    // Process each phase (e.g., "shape", "discovery", etc.)
    const phases = Object.keys(clarificationData);
    phases.forEach((phaseName, phaseIndex) => {
      const phaseData = clarificationData[phaseName];
      
      if (!phaseData || typeof phaseData !== 'object') return;

      // Phase header
      html += `
        <div style="
          margin-bottom: 6px;
          padding: 8px 0;
          background-color: transparent;
          border-radius: 0;
          border-left: none;
        ">
          <span style="font-weight: 600; color: var(--vscode-foreground); font-size: 13px; text-transform: capitalize;">
            ${this.escapeHtml(phaseName)} Phase
          </span>
        </div>`;

      // Key Questions & Answers
      if (phaseData.key_questions && phaseData.key_questions.answers) {
        html += this._formatQuestionsAndAnswers(phaseData.key_questions.answers, borderColor);
      }

      // Evidence sources
      if (phaseData.evidence && phaseData.evidence.sources && Array.isArray(phaseData.evidence.sources)) {
        html += `
          <div style="
            margin-top: 6px;
            padding: 8px 0;
            background-color: transparent;
            border-radius: 0;
            border-left: none;
          ">
            <div style="font-weight: 600; color: var(--vscode-foreground); margin-bottom: 6px; font-size: 11px;">
              Evidence Sources
            </div>
            <ul style="margin: 0; padding-left: 0; list-style-type: none; font-size: 10px; line-height: 1.6;">
              ${phaseData.evidence.sources.map(source => 
                `<li style="color: var(--vscode-foreground); margin-bottom: 4px;">• ${this.escapeHtml(source)}</li>`
              ).join('')}
            </ul>
          </div>`;
      }

      // Context items
      if (phaseData.context && Array.isArray(phaseData.context)) {
        html += `
          <div style="
            margin-top: 6px;
            padding: 8px 0;
            background-color: transparent;
            border-radius: 0;
            border-left: none;
          ">
            <div style="font-weight: 600; color: var(--vscode-foreground); margin-bottom: 6px; font-size: 11px;">
              Context
            </div>
            <ul style="margin: 0; padding-left: 0; list-style-type: none; font-size: 10px; line-height: 1.6;">
              ${phaseData.context.map(item => 
                `<li style="color: var(--vscode-foreground); margin-bottom: 4px;">• ${this.escapeHtml(item)}</li>`
              ).join('')}
            </ul>
          </div>`;
      }

      // Add spacing between phases
      if (phaseIndex < phases.length - 1) {
        html += '<div style="margin-bottom: 10px;"></div>';
      }
    });

    return html || '<div style="color: var(--vscode-descriptionForeground); font-style: italic;">No clarification details available</div>';
  }

  _formatQuestionsAndAnswers(answers, borderColor) {
    if (!answers || typeof answers !== 'object') {
      return '<div style="color: var(--vscode-descriptionForeground); font-style: italic;">No questions answered yet</div>';
    }

    const entries = Object.entries(answers);
    if (entries.length === 0) {
      return '<div style="color: var(--vscode-descriptionForeground); font-style: italic;">No questions answered yet</div>';
    }

    const qaBlocks = entries.map(([question, answer], index) => {
      const questionId = `question-${index}`;
      const answerId = `answer-${index}`;
      return `<div class="input-container" style="margin-bottom: ${index < entries.length - 1 ? '20px' : '0'};">
        <div class="input-header">${this.escapeHtml(question)}</div>
        <textarea id="${answerId}" placeholder="Enter answer..." oninput="autoResizeTextarea(this)" onchange="updateQuestionAnswer('${this.escapeForJs(question)}', this.value)">${this.escapeHtml(answer || '')}</textarea>
      </div>`;
    }).join('');

    return qaBlocks;
  }

  _formatStrategyData(strategy, borderColor) {
    if (!strategy || typeof strategy !== 'object') {
      return '<div style="color: var(--vscode-descriptionForeground); font-style: italic;">No strategy data available</div>';
    }

    let html = '';

    // Format assumptions section
    if (strategy.assumptions) {
      const assumptions = strategy.assumptions;
      
      // Review status
      if (assumptions.review_status) {
        html += `
          <div style="
            margin-bottom: 6px;
            padding: 8px 0;
            background-color: transparent;
            border-radius: 0;
            border-left: none;
          ">
            <span style="font-weight: 400; color: var(--vscode-foreground);">Review Status:</span>
            <span style="margin-left: 8px; color: var(--vscode-foreground);">${this.escapeHtml(assumptions.review_status)}</span>
          </div>`;
      }

      // Individual assumptions
      if (assumptions.assumptions && Array.isArray(assumptions.assumptions)) {
        assumptions.assumptions.forEach((item, index) => {
          const statusIcon = item.status === 'ACCEPTED' ? '✓' : item.status === 'REJECTED' ? '✗' : '?';
          
          html += `
            <div style="
              margin-bottom: ${index < assumptions.assumptions.length - 1 ? '12px' : '0'};
              padding: 8px 0;
              background-color: transparent;
              border-radius: 0;
              border-left: none;
            ">
              <div style="
                display: flex;
                align-items: flex-start;
                margin-bottom: 8px;
              ">
                <span style="
                  font-weight: 600;
                  color: var(--vscode-foreground);
                  font-size: 12px;
                  line-height: 1.4;
                  flex: 1;
                ">
                  ${this.escapeHtml(item.assumption)}
                </span>
                <span style="
                  padding: 2px 8px;
                  border-radius: 3px;
                  font-size: 10px;
                  font-weight: 400;
                  color: var(--vscode-foreground);
                  border: 1px solid rgba(255, 255, 255, 0.2);
                ">
                  ${statusIcon} ${this.escapeHtml(item.status || 'UNKNOWN')}
                </span>
              </div>
              ${item.justification ? `
                <div style="
                  color: var(--vscode-foreground);
                  font-size: 11px;
                  line-height: 1.5;
                  padding-left: 0;
                  white-space: pre-wrap;
                  word-wrap: break-word;
                  border-left: none;
                  padding: 8px 0;
                  margin-top: 8px;
                ">
                  ${this.escapeHtml(item.justification)}
                </div>` : ''}
            </div>`;
        });
      }
    }

    return html || '<div style="color: var(--vscode-descriptionForeground); font-style: italic;">No strategy details available</div>';
  }

  /**
   * Render parameters table
   */
  renderParameters(parameters) {
    if (!parameters || parameters.length === 0) return '';
    
    const rows = parameters.map(param => `
      <tr>
        <td style="padding: 3px 6px; font-family: monospace;">${this.escapeHtml(param.flag)}</td>
        <td style="padding: 3px 6px; font-family: monospace;">${this.escapeHtml(param.syntax)}</td>
        <td style="padding: 3px 6px;">${this.escapeHtml(param.description)}</td>
      </tr>
    `).join('');

    return `
    <div class="card-primary">
        <div class="section-title">Parameters</div>
        <div class="card-secondary" style="padding: 8px;">
        <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
          <thead>
            <tr>
              <th style="padding: 3px 6px; text-align: left;">Flag</th>
              <th style="padding: 3px 6px; text-align: left;">Syntax</th>
              <th style="padding: 3px 6px; text-align: left;">Description</th>
            </tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>
        </div>
    </div>`;
  }

  /**
   * Render command input text area
   */
  renderCommandInput() {
    return `
    <div class="card-primary">
        <div class="section-title">💻 Execute Command</div>
        <div class="card-secondary command-input-container" style="padding: 5px;">
            <div class="input-container" style="margin-bottom: 0;">
                <div class="input-header">Command</div>
                <textarea id="commandInput" class="command-textarea" 
                    placeholder="Enter command (e.g., behavior.action, status, scope &quot;Story Name&quot;)"
                    onfocus="this.parentElement.parentElement.classList.add('expanded')"
                    onkeydown="if(event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); executeCommand(); }"></textarea>
            </div>
            <button class="execute-button" onclick="executeCommand()">Submit</button>
        </div>
    </div>`;
  }

  /**
   * Render prompt display area
   */
  renderPromptDisplay(promptContent) {
    const escapedContent = this.escapeHtml(promptContent);
    return `
        <div class="prompt-display-container">
            <div class="input-container">
                <div class="input-header">Generated Prompt</div>
            <textarea id="promptDisplay" class="prompt-textarea" readonly placeholder="Click on any operation in the hierarchy to see the generated prompt...">${escapedContent}</textarea>
            </div>
        </div>`;
  }

  /**
   * Render commands footer
   */
  renderCommands(commands) {
    const commandsText = commands && commands.text ? commands.text : 'N/A';
    return `
    <div class="commands-footer">
        💻 Commands: ${this.escapeHtml(commandsText)}
    </div>`;
  }

  /**
   * Render JavaScript for webview interaction
   */
  renderScripts() {
    return `
    <script>
        const vscode = acquireVsCodeApi();

        function refreshStatus() {
            vscode.postMessage({ command: 'refresh' });
        }

        function openScope() {
            vscode.postMessage({ 
                command: 'openScope',
                filePath: 'docs/stories/story-graph.json'
            });
        }

        function openFile(filePath) {
            vscode.postMessage({ 
                command: 'openScope',
                filePath: filePath
            });
        }

        function toggleCollapse(elementId) {
            const content = document.getElementById(elementId);
            const iconSpan = document.getElementById(elementId + '-icon');
            
            let isExpanded = false;
            if (content && content.style.display === 'none') {
                content.style.display = 'block';
                isExpanded = true;
                if (iconSpan) {
                    const img = iconSpan.querySelector('img');
                    if (img) {
                        const subtractPath = iconSpan.dataset.subtract || iconSpan.getAttribute('data-subtract');
                        if (subtractPath) {
                            img.src = subtractPath;
                            img.alt = 'Collapse';
                        }
                    } else {
                        iconSpan.textContent = '➖';
                    }
                    iconSpan.style.color = '#ff8c00';
                    iconSpan.classList.add('expanded');
                }
            } else if (content) {
                content.style.display = 'none';
                isExpanded = false;
                if (iconSpan) {
                    const img = iconSpan.querySelector('img');
                    if (img) {
                        const plusPath = iconSpan.dataset.plus || iconSpan.getAttribute('data-plus');
                        if (plusPath) {
                            img.src = plusPath;
                            img.alt = 'Expand';
                        }
                    } else {
                        iconSpan.textContent = '➕';
                    }
                    iconSpan.style.color = '#ff8c00';
                    iconSpan.classList.remove('expanded');
                }
            }
            
            // Send expansion state to extension
            const expansionState = {};
            expansionState[elementId] = isExpanded;
            vscode.postMessage({ 
                command: 'updateExpansionState',
                expansionState: expansionState
            });
        }

        function toggleSection(sectionId) {
            const content = document.getElementById(sectionId);
            const section = content.closest('.collapsible-section');
            const icon = section.querySelector('.expand-icon');
            
            if (section.classList.contains('expanded')) {
                // Collapse
                section.classList.remove('expanded');
                content.style.maxHeight = '0';
                content.style.overflow = 'hidden';
                icon.style.transform = 'rotate(0deg)';
            } else {
                // Expand
                section.classList.add('expanded');
                content.style.maxHeight = '2000px';
                content.style.overflow = 'visible';
                icon.style.transform = 'rotate(90deg)';
            }
        }

        function updateFilter(filterValue) {
            console.log('[FILTER] updateFilter called with:', filterValue);
            vscode.postMessage({
                command: 'updateFilter',
                filter: filterValue
            });
        }

        function clearScopeFilter() {
            console.log('[FILTER] Clearing scope filter - sending scope showAll');
            vscode.postMessage({
                command: 'clearFilter'
            });
        }

        function sendInstructionsToChat(event) {
            console.log('[HTML] sendInstructionsToChat called');
            event.stopPropagation(); // Prevent toggling the section
            
            const promptContent = window._promptContent || '';
            console.log('[HTML] promptContent length:', promptContent.length);
            
            if (!promptContent || promptContent.trim() === '') {
                console.log('[HTML] No content to submit - ignored');
                alert('No content available. Please run an instructions command first.');
                return;
            }
            console.log('[HTML] Sending message to extension');
            vscode.postMessage({
                command: 'sendToChat',
                promptContent: promptContent
            });
            console.log('[HTML] Message sent');
        }

        function updateWorkspace(workspacePath) {
            vscode.postMessage({
                command: 'updateWorkspace',
                workspacePath: workspacePath
            });
        }

        function updateQuestionAnswer(question, answer) {
            console.log('[Q&A] updateQuestionAnswer called:', {question, answer});
            vscode.postMessage({
                command: 'updateQuestionAnswer',
                question: question,
                answer: answer
            });
        }

        function autoResizeTextarea(textarea) {
            // Reset height to auto to get the correct scrollHeight
            textarea.style.height = 'auto';
            // Set height to scrollHeight to fit content
            textarea.style.height = textarea.scrollHeight + 'px';
        }

        // Auto-resize all textareas on page load
        window.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('textarea').forEach(function(textarea) {
                autoResizeTextarea(textarea);
            });
        });

        function switchBot(botName) {
            console.log('[SWITCHBOT] Switching to bot:', botName);
            vscode.postMessage({ 
                command: 'switchBot',
                botName: botName
            });
            console.log('[SWITCHBOT] Message sent');
        }

        function executeCommand() {
            const textarea = document.getElementById('commandInput');
            const command = textarea.value.trim();
            if (command) {
                vscode.postMessage({ 
                    command: 'executeCommand',
                    commandText: command
                });
                // Optionally clear the textarea after execution
                // textarea.value = '';
            }
        }

        function copyInstructionsToClipboard() {
            console.log('[CLIPBOARD] copyInstructionsToClipboard() called');
            const promptTextarea = document.getElementById('promptDisplay');
            console.log('[CLIPBOARD] promptTextarea found:', !!promptTextarea);
            if (promptTextarea) {
                console.log('[CLIPBOARD] promptTextarea.value length:', promptTextarea.value ? promptTextarea.value.length : 0);
            }
            if (promptTextarea && promptTextarea.value) {
                console.log('[CLIPBOARD] Attempting to copy to clipboard...');
                navigator.clipboard.writeText(promptTextarea.value).then(() => {
                    console.log('[CLIPBOARD] ✓ Instructions successfully copied to clipboard');
                    console.log('[CLIPBOARD] Copied length:', promptTextarea.value.length);
                }).catch(err => {
                    console.error('[CLIPBOARD] ✗ Failed to copy instructions:', err);
                    console.error('[CLIPBOARD] Error details:', err.message, err.stack);
                });
            } else {
                console.warn('[CLIPBOARD] ⚠ No content to copy - textarea empty or not found');
            }
        }

        // Listen for messages from the extension
        window.addEventListener('message', event => {
            console.log('[WEBVIEW] Received message from extension:', event.data);
            const message = event.data;
            if (message.command === 'copyInstructionsToClipboard') {
                console.log('[WEBVIEW] Executing copyInstructionsToClipboard');
                copyInstructionsToClipboard();
            }
        });

        function executeNavigationCommand(cmd) {
            vscode.postMessage({ 
                command: 'executeCommand',
                commandText: cmd
            });
        }

        function navigateToBehavior(behaviorName) {
            vscode.postMessage({ 
                command: 'navigateAndExecute',
                fullCommand: behaviorName
            });
        }

        function navigateToAction(behaviorName, actionName) {
            const fullCommand = behaviorName + '.' + actionName;
            
            vscode.postMessage({ 
                command: 'navigateAndExecute',
                fullCommand: fullCommand
            });
        }

        function navigateAndExecute(behaviorName, actionName, operationName) {
            // Construct full command path
            const fullCommand = behaviorName + '.' + actionName + '.' + operationName;
            
            vscode.postMessage({ 
                command: 'navigateAndExecute',
                behaviorName: behaviorName,
                actionName: actionName,
                operationName: operationName,
                fullCommand: fullCommand
            });
        }

        // Allow Enter key to execute (Ctrl+Enter for newline)
        document.addEventListener('DOMContentLoaded', function() {
            const textarea = document.getElementById('commandInput');
            if (textarea) {
                textarea.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey) {
                        e.preventDefault();
                        executeCommand();
                    }
                });
            }
            
            // Initialize collapse icons in story tree
            const plusPathInput = document.getElementById('plusIconPath');
            const subtractPathInput = document.getElementById('subtractIconPath');
            if (plusPathInput && subtractPathInput) {
                const plusPath = plusPathInput.value;
                const subtractPath = subtractPathInput.value;
                
                document.querySelectorAll('.collapse-icon').forEach(img => {
                    const state = img.dataset.state || 'collapsed';
                    img.src = state === 'expanded' ? subtractPath : plusPath;
                    
                    // Store paths in parent span for toggle function
                    const parentSpan = img.closest('span[id$="-icon"]');
                    if (parentSpan) {
                        parentSpan.dataset.plus = plusPath;
                        parentSpan.dataset.subtract = subtractPath;
                    }
                });
            }
        });

    </script>`;
  }

  /**
   * Escape HTML special characters
   */
  escapeHtml(text) {
    if (!text) return '';
    const map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    };
    return String(text).replace(/[&<>"']/g, m => map[m]);
  }

  /**
   * Get the icon for a specific bot
   * @param {string} botName - The name of the bot
   * @returns {string} The bot's icon emoji
   */
  getBotIcon(botName) {
    const icons = {
      'story_bot': '📖',
      'crc_bot': '🗂️'
    };
    return icons[botName] || '🤖';
  }

  /**
   * Escape string for JavaScript context (inside single quotes)
   * Only escapes single quotes and backslashes
   */
  escapeForJs(text) {
    if (!text) return '';
    return String(text).replace(/\\/g, '\\\\').replace(/'/g, "\\'");
  }

  /**
   * Render error page
   */
  renderError(errorMessage) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 5px;
            color: var(--vscode-errorForeground);
            background-color: var(--vscode-editor-background);
        }
        .error {
            background-color: var(--vscode-inputValidation-errorBackground);
            border: 1px solid var(--vscode-inputValidation-errorBorder);
            padding: 8px;
            border-radius: 4px;
        }
        .error h2 {
            margin-top: 0;
        }
        button {
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            padding: 8px 16px;
            cursor: pointer;
            margin-top: 6px;
            border-radius: 2px;
        }
    </style>
</head>
<body>
    <div class="error">
        <h2>Error Loading Status</h2>
        <p>${this.escapeHtml(errorMessage)}</p>
        <button onclick="retry()">Retry</button>
    </div>
    <script>
        const vscode = acquireVsCodeApi();
        function retry() {
            vscode.postMessage({ command: 'refresh' });
        }
    </script>
</body>
</html>`;
  }
}

module.exports = HtmlRenderer;

