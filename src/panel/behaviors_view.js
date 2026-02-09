/**
 * BehaviorsView - Renders behavior hierarchy with actions.
 * 
 * Epic: Invoke Bot Through Panel
 * Sub-Epic: Navigate And Execute Behaviors Through Panel
 * Story: Display Hierarchy, Navigate Behavior Action, Execute Behavior Action
 */

const PanelView = require('./panel_view');
const branding = require('./branding');

class BehaviorsView extends PanelView {
    /**
     * Behaviors view.
     * 
     * @param {string|PanelView} botPathOrCli - Bot path or CLI instance
     * @param {Object} webview - VS Code webview instance (optional)
     * @param {Object} extensionUri - Extension URI (optional)
     * @param {Object} parentView - Parent BotView (optional, for accessing cached botData)
     */
    constructor(botPathOrCli, webview, extensionUri, parentView = null) {
        super(botPathOrCli);
        this.expansionState = {};
        this.webview = webview || null;
        this.extensionUri = extensionUri || null;
        this.parentView = parentView;
    }
    
    /**
     * Get behaviors data from CLI
     */
    async getBehaviors() {
        const botData = await this.execute('status');
        // NO FALLBACKS - let it fail if data is missing
        if (!botData) throw new Error('[BehaviorsView] botData is null/undefined');
        if (!botData.behaviors) throw new Error('[BehaviorsView] No behaviors in response');
        if (!botData.behaviors.all_behaviors) throw new Error('[BehaviorsView] No all_behaviors in response');
        return botData.behaviors.all_behaviors;
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
     * Escape text for use in JavaScript strings.
     * 
     * @param {string} text - Text to escape
     * @returns {string} Escaped text
     */
    escapeForJs(text) {
        if (typeof text !== 'string') {
            text = String(text);
        }
        return text.replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '\\"').replace(/\n/g, '\\n').replace(/\r/g, '\\r');
    }
    
    /**
     * Get status marker for behavior/action/operation.
     * 
     * @param {boolean} isCurrent - Is current item
     * @param {boolean} isCompleted - Is completed item
     * @param {string} tickIconPath - Tick icon path (optional)
     * @param {string} notTickedIconPath - Not ticked icon path (optional)
     * @returns {string} Marker HTML
     */
    getStatusMarker(isCurrent, isCompleted, tickIconPath, notTickedIconPath) {
        if (isCurrent) {
            return tickIconPath 
                ? `<img src="${tickIconPath}" alt="Current" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />`
                : '';
        } else if (isCompleted) {
            return tickIconPath 
                ? `<img src="${tickIconPath}" alt="Completed" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />`
                : '';
        } else {
            return notTickedIconPath 
                ? `<img src="${notTickedIconPath}" alt="Pending" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />`
                : '';
        }
    }
    
    /**
     * Render behaviors hierarchy HTML - gets own data from CLI.
     * 
     * @returns {Promise<string>} HTML string
     */
    async render() {
        // Use cached botData from parent if available, otherwise fetch it
        const botData = this.parentView?.botData || await this.execute('status');
        // NO FALLBACKS - let it fail if data is missing
        if (!botData) throw new Error('[BehaviorsView] botData is null/undefined');
        if (!botData.behaviors) throw new Error('[BehaviorsView] No behaviors in response');
        if (!botData.behaviors.all_behaviors) throw new Error('[BehaviorsView] No all_behaviors in response');
        
        // Log current state from status command
        console.log(`[BehaviorsView] Status returned - current_behavior: ${botData.current_behavior}, current_action: ${botData.current_action}`);
        
        const behaviorsData = botData.behaviors.all_behaviors;
        
        // Get icon URIs using branding utility (handles ABD vs Scotia paths)
        const getIcon = (name) => branding.getImageUri(this.webview, this.extensionUri, name);
        
        const feedbackIconPath = getIcon('feedback.png');
        const gearIconPath = getIcon('gear.png');
        const plusIconPath = getIcon('plus.png');
        const subtractIconPath = getIcon('subtract.png');
        const tickIconPath = getIcon('tick.png');
        const notTickedIconPath = getIcon('not_ticked.png');
        const leftIconPath = getIcon('left.png');
        const pointerIconPath = getIcon('pointer.png');
        const rightIconPath = getIcon('right.png');
        const clipboardIconPath = getIcon('rules.png');
        const submitIconPath = getIcon('submit.png');
        
        console.log(`[BehaviorsView] Branding: ${branding.getBranding()}, icon sample: ${plusIconPath}`);
        
        if (!behaviorsData || behaviorsData.length === 0) {
            return this.renderEmpty(feedbackIconPath, gearIconPath, leftIconPath, pointerIconPath, rightIconPath, submitIconPath);
        }
        
        const behaviorsHtml = behaviorsData.map((behavior, bIdx) => {
            return this.renderBehavior(behavior, bIdx, plusIconPath, subtractIconPath, tickIconPath, notTickedIconPath, clipboardIconPath);
        }).join('');

        // Prepare prompt content (so header submit button can reuse same behavior/instructions payload)
        let promptContentStr = '';
        try {
            const instructions = botData?.instructions || {};
            if (instructions.display_content) {
                promptContentStr = Array.isArray(instructions.display_content) ? instructions.display_content.join('\n') : instructions.display_content;
            } else if (instructions.base_instructions) {
                promptContentStr = Array.isArray(instructions.base_instructions) ? instructions.base_instructions.join('\n') : instructions.base_instructions;
            }
        } catch (e) {
            console.warn('[BehaviorsView] Failed to build promptContentStr', e);
            promptContentStr = '';
        }

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
                <div style="display: flex; align-items: center;" onclick="toggleSection('behaviors-content')">
                    <span class="expand-icon" style="margin-right: 8px; font-size: 28px; transition: transform 0.15s;">▸</span>
                    ${feedbackIconPath ? `<img src="${feedbackIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="Behavior Icon" />` : (gearIconPath ? `<img src="${gearIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="Behavior Icon" />` : '')}
                    <span style="font-weight: 600; font-size: 20px; color: var(--accent-color);">Behavior Action Status</span>
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
                    width: 40px;
                    height: 40px;
                " 
                onmouseover="this.style.backgroundColor='rgba(255, 140, 0, 0.3)'" 
                onmouseout="this.style.backgroundColor='rgba(255, 140, 0, 0.15)'"
                title="Submit instructions to chat">
                    ${submitIconPath ? `<img src="${submitIconPath}" style="width: 100%; height: 100%; object-fit: contain;" alt="Submit to Chat" />` : '📤'}
                </button>
                <script>
                    window._promptContent = ${JSON.stringify(promptContentStr)};
                </script>
            </div>
            <div id="behaviors-content" class="collapsible-content" style="max-height: 2000px; overflow: hidden; transition: max-height 0.3s ease;">
                <div class="card-secondary" style="padding: 5px;">
                    ${behaviorsHtml}
                    <div style="margin-top: 8px; padding-top: 5px; border-top: none; display: flex; gap: 4px; flex-wrap: wrap;">
                        <button class="nav-command-button" data-action="executeNavigationCommand" data-command="back" title="Back - Go to previous action" style="
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
                        ">${leftIconPath ? `<img src="${leftIconPath}" style="width: 20px; height: 20px; object-fit: contain;" alt="Back" />` : ''}</button>
                        <button class="nav-command-button" data-action="executeNavigationCommand" data-command="current" title="Current - Show current action details" style="
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
                        ">${pointerIconPath ? `<img src="${pointerIconPath}" style="width: 20px; height: 20px; object-fit: contain;" alt="Current" />` : ''}</button>
                        <button class="nav-command-button" data-action="executeNavigationCommand" data-command="next" title="Next - Advance to next action" style="
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
                        ">${rightIconPath ? `<img src="${rightIconPath}" style="width: 20px; height: 20px; object-fit: contain;" alt="Next" />` : ''}</button>
                    </div>
                </div>
            </div>
        </div>
    </div>`;
    }
    
    /**
     * Render empty state.
     * 
     * @param {string} feedbackIconPath - Feedback icon path
     * @param {string} gearIconPath - Gear icon path
     * @param {string} leftIconPath - Left icon path
     * @param {string} pointerIconPath - Pointer icon path
     * @param {string} rightIconPath - Right icon path
     * @returns {string} HTML string
     */
    renderEmpty(feedbackIconPath, gearIconPath, leftIconPath, pointerIconPath, rightIconPath, submitIconPath) {
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
                <div style="display: flex; align-items: center;" onclick="toggleSection('behaviors-content')">
                    <span class="expand-icon" style="margin-right: 8px; font-size: 28px; transition: transform 0.15s;">▸</span>
                    ${feedbackIconPath ? `<img src="${feedbackIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="Behavior Icon" />` : (gearIconPath ? `<img src="${gearIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="Behavior Icon" />` : '')}
                    <span style="font-weight: 600; font-size: 20px; color: var(--accent-color);">Behavior Action Status</span>
                </div>
                <button onclick="sendInstructionsToChat(event)" style="
                    background: rgba(255, 140, 0, 0.15);
                    border: none;
                    border-radius: 8px;
                    padding: 6px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: all 0.15s ease;
                    width: 40px;
                    height: 40px;
                " 
                onmouseover="this.style.backgroundColor='rgba(255, 140, 0, 0.3)'" 
                onmouseout="this.style.backgroundColor='rgba(255, 140, 0, 0.15)'"
                title="Submit instructions to chat">
                    ${submitIconPath ? `<img src="${submitIconPath}" style="width: 100%; height: 100%; object-fit: contain;" alt="Submit to Chat" />` : '📤'}
                </button>
            </div>
            <div id="behaviors-content" class="collapsible-content" style="max-height: 2000px; overflow: hidden; transition: max-height 0.3s ease;">
                <div class="card-secondary" style="padding: 5px;">
                    <div class="empty-state">No behaviors available</div>
                    <div style="margin-top: 8px; padding-top: 5px; border-top: none; display: flex; gap: 4px; flex-wrap: wrap;">
                        <button class="nav-command-button" data-action="executeNavigationCommand" data-command="back" title="Back - Go to previous action" style="
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
                        ">${leftIconPath ? `<img src="${leftIconPath}" style="width: 20px; height: 20px; object-fit: contain;" alt="Back" />` : ''}</button>
                        <button class="nav-command-button" data-action="executeNavigationCommand" data-command="current" title="Current - Show current action details" style="
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
                        ">${pointerIconPath ? `<img src="${pointerIconPath}" style="width: 20px; height: 20px; object-fit: contain;" alt="Current" />` : ''}</button>
                        <button class="nav-command-button" data-action="executeNavigationCommand" data-command="next" title="Next - Advance to next action" style="
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
                        ">${rightIconPath ? `<img src="${rightIconPath}" style="width: 20px; height: 20px; object-fit: contain;" alt="Next" />` : ''}</button>
                    </div>
                </div>
            </div>
        </div>
    </div>`;
    }
    
    /**
     * Render a single behavior.
     * 
     * @param {Object} behavior - Behavior object
     * @param {number} bIdx - Behavior index
     * @param {string} plusIconPath - Plus icon path
     * @param {string} subtractIconPath - Subtract icon path
     * @param {string} tickIconPath - Tick icon path
     * @param {string} notTickedIconPath - Not ticked icon path
     * @param {string} clipboardIconPath - Clipboard icon path
     * @returns {string} HTML string
     */
    renderBehavior(behavior, bIdx, plusIconPath, subtractIconPath, tickIconPath, notTickedIconPath, clipboardIconPath) {
        const isCurrent = behavior.isCurrent || behavior.is_current || false;
        const isCompleted = behavior.isCompleted || behavior.is_completed || false;
        const behaviorMarker = isCurrent 
            ? (tickIconPath ? `<img src="${tickIconPath}" alt="Current" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '')
            : isCompleted
            ? (tickIconPath ? `<img src="${tickIconPath}" alt="Completed" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '')
            : (notTickedIconPath ? `<img src="${notTickedIconPath}" alt="Pending" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '');
        
        const behaviorTooltip = behavior.description ? this.escapeHtml(behavior.description) : '';
        const behaviorId = `behavior-${bIdx}`;
        const behaviorNameRaw = behavior.name || '';
        const behaviorName = this.escapeHtml(behaviorNameRaw);
        const behaviorNameJs = this.escapeForJs(behaviorNameRaw);
        
        // Expansion logic:
        // 1. If we have saved state for this item, use it (user's explicit choice)
        // 2. Otherwise, expand if current or completed (don't auto-collapse completed items)
        const hasExpansionState = this.expansionState && (behaviorId in this.expansionState);
        const behaviorExpanded = hasExpansionState ? this.expansionState[behaviorId] : (isCurrent || isCompleted);
        const behaviorIconSrc = behaviorExpanded ? subtractIconPath : plusIconPath;
        const behaviorIconAlt = behaviorExpanded ? 'Collapse' : 'Expand';
        const behaviorIconClass = behaviorExpanded ? 'expanded' : '';
        const behaviorDisplay = behaviorExpanded ? 'block' : 'none';
        
        const behaviorActiveClass = isCurrent ? ' active' : '';
        let html = `<div class="collapsible-header card-item${behaviorActiveClass}" data-behavior="${behaviorName}" title="${behaviorTooltip}"><span id="${behaviorId}-icon" class="${behaviorIconClass}" style="display: inline-block; min-width: 12px; cursor: pointer;" data-action="toggleCollapse" data-target="${behaviorId}" data-plus="${plusIconPath}" data-subtract="${subtractIconPath}">${plusIconPath && subtractIconPath ? `<img src="${behaviorIconSrc}" alt="${behaviorIconAlt}" style="width: 12px; height: 12px; vertical-align: middle;" />` : ''}</span> <span class="behavior-name-clickable" style="cursor: pointer; text-decoration: underline;" data-action="navigateToBehavior" data-behavior-name="${behaviorNameJs}">${behaviorMarker}${behaviorName}</span>${clipboardIconPath ? `<button class="behavior-rules-button" data-action="getBehaviorRules" data-behavior-name="${behaviorNameJs}" style="background: transparent; border: none; padding: 0 0 0 8px; margin: 0; cursor: pointer; vertical-align: middle; display: inline-flex; align-items: center; transition: opacity 0.15s ease;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Get rules for ${behaviorName} and send to chat"><img src="${clipboardIconPath}" style="width: 16px; height: 16px; object-fit: contain;" alt="Get Rules" /></button>` : ''}</div>`;
        
        // Always create collapsible content, even if empty
        const actionsArray = behavior.actions?.all_actions || behavior.actions || [];
        const hasActions = Array.isArray(actionsArray) && actionsArray.length > 0;
        const actionsHtml = hasActions ? actionsArray.map((action, aIdx) => {
            return this.renderAction(action, bIdx, aIdx, behaviorName, plusIconPath, subtractIconPath, tickIconPath, notTickedIconPath);
        }).join('') : '';
        
        html += `<div id="${behaviorId}" class="collapsible-content" style="display: ${behaviorDisplay};">${actionsHtml}</div>`;
        
        return html;
    }
    
    /**
     * Render a single action.
     * 
     * @param {Object} action - Action object
     * @param {number} bIdx - Behavior index
     * @param {number} aIdx - Action index
     * @param {string} behaviorName - Behavior name (escaped)
     * @param {string} plusIconPath - Plus icon path
     * @param {string} subtractIconPath - Subtract icon path
     * @param {string} tickIconPath - Tick icon path
     * @param {string} notTickedIconPath - Not ticked icon path
     * @returns {string} HTML string
     */
    renderAction(action, bIdx, aIdx, behaviorName, plusIconPath, subtractIconPath, tickIconPath, notTickedIconPath) {
        // Log inputs
        const fs = require('fs');
        const path = require('path');
        const logPath = '.\\logs\\render-action-debug.log';
        const timestamp = new Date().toISOString();
        
        const logEntry = `\n${'='.repeat(80)}\n[${timestamp}] renderAction called\n` +
            `  bIdx: ${bIdx}, aIdx: ${aIdx}\n` +
            `  action raw: ${JSON.stringify(action)}\n` +
            `  behaviorName (passed in): "${behaviorName}"\n` +
            `  behaviorName type: ${typeof behaviorName}\n`;
        
        try {
            fs.appendFileSync(logPath, logEntry);
        } catch (err) {
            console.error('[BehaviorsView] Failed to write to log file:', err);
        }
        
        const isCurrent = action.isCurrent || action.is_current || false;
        const isCompleted = action.isCompleted || action.is_completed || false;
        const actionMarker = isCurrent
            ? (tickIconPath ? `<img src="${tickIconPath}" alt="Current" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '')
            : isCompleted
            ? (tickIconPath ? `<img src="${tickIconPath}" alt="Completed" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '')
            : (notTickedIconPath ? `<img src="${notTickedIconPath}" alt="Pending" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '');
        
        const actionTooltip = action.description ? this.escapeHtml(action.description) : '';
        const actionName = this.escapeHtml(action.action_name || action.name || '');
        
        // Log escaped values
        const logEntry2 = `  actionName (escaped): "${actionName}"\n` +
            `  onclick will be: navigateToAction('${behaviorName}', '${actionName}')\n`;
        
        try {
            fs.appendFileSync(logPath, logEntry2);
        } catch (err) {
            console.error('[BehaviorsView] Failed to write to log file:', err);
        }
        
        const actionActiveClass = isCurrent ? ' active' : '';
        const actionNameJs = this.escapeForJs(action.action_name || action.name || '');
        const actionHtml = `<div class="collapsible-header action-item card-item${actionActiveClass}" title="${actionTooltip}"><span class="action-name-clickable" style="cursor: pointer; text-decoration: underline;" data-action="navigateToAction" data-behavior-name="${behaviorName}" data-action-name="${actionNameJs}">${actionMarker}${actionName}</span></div>`;
        
        // Log final HTML
        const logEntry3 = `  Generated HTML: ${actionHtml.substring(0, 200)}...\n`;
        try {
            fs.appendFileSync(logPath, logEntry3);
        } catch (err) {
            console.error('[BehaviorsView] Failed to write to log file:', err);
        }
        
        return actionHtml;
    }
    
    /**
     * Handle events.
     * 
     * @param {string} eventType - Event type
     * @param {Object} eventData - Event data
     * @returns {Promise<Object>} Result
     */
    async handleEvent(eventType, eventData) {
        if (eventType === 'execute') {
            // Execute behavior/action logic would go here
            return { success: true };
        }
        throw new Error(`Unknown event type: ${eventType}`);
    }
}

module.exports = BehaviorsView;
