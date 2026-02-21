

const PanelView = require('./panel_view');
const branding = require('./branding');
const { escapeForHtml, escapeForJs } = require('./utils');

class BehaviorsView extends PanelView {

    constructor(botPathOrCli, webview, extensionUri, parentView = null) {
        super(botPathOrCli);
        this.expansionState = {};
        this.webview = webview || null;
        this.extensionUri = extensionUri || null;
        this.parentView = parentView;
    }
    

    async getBehaviors() {
        const botData = await this.execute('status');

        if (!botData) throw new Error('[BehaviorsView] botData is null/undefined');
        if (!botData.behaviors) throw new Error('[BehaviorsView] No behaviors in response');
        if (!botData.behaviors.all_behaviors) throw new Error('[BehaviorsView] No all_behaviors in response');
        return botData.behaviors.all_behaviors;
    }
    

    

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
    

    async render() {

        const botData = this.parentView?.botData || await this.execute('status');

        if (!botData) throw new Error('[BehaviorsView] botData is null/undefined');
        if (!botData.behaviors) throw new Error('[BehaviorsView] No behaviors in response');
        if (!botData.behaviors.all_behaviors) throw new Error('[BehaviorsView] No all_behaviors in response');
        

        console.log(`[BehaviorsView] Status returned - current_behavior: ${botData.current_behavior}, current_action: ${botData.current_action}`);
        
        const behaviorsData = botData.behaviors.all_behaviors;
        

        const getIcon = (name) => branding.getImageUri(this.webview, this.extensionUri, name);
        
        const valueStreamIconPath = getIcon('value_stream.png');
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
        const combinedIconPath = getIcon('combined.png');
        const skipIconPath = getIcon('skip.png');
        const manualIconPath = getIcon('manual.png');
        
        console.log(`[BehaviorsView] Branding: ${branding.getBranding()}, icon sample: ${plusIconPath}`);
        
        if (!behaviorsData || behaviorsData.length === 0) {
            return this.renderEmpty(valueStreamIconPath || feedbackIconPath, gearIconPath, leftIconPath, pointerIconPath, rightIconPath, submitIconPath);
        }
        
        const executionSettings = botData.execution || {};
        const specialInstructions = botData.special_instructions || {};
        const behaviorsHtml = behaviorsData.map((behavior, bIdx) => {
            return this.renderBehavior(behavior, bIdx, plusIconPath, subtractIconPath, tickIconPath, notTickedIconPath, clipboardIconPath, combinedIconPath, skipIconPath, manualIconPath, executionSettings, specialInstructions);
        }).join('');


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
                    ${valueStreamIconPath ? `<img src="${valueStreamIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="Value Stream" />` : (feedbackIconPath ? `<img src="${feedbackIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="Value Stream" />` : (gearIconPath ? `<img src="${gearIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="Value Stream" />` : ''))}
                    <span style="font-weight: 600; font-size: 20px; color: var(--accent-color);">Value Stream</span>
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
    

    renderEmpty(valueStreamOrFeedbackIconPath, gearIconPath, leftIconPath, pointerIconPath, rightIconPath, submitIconPath) {
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
                    ${valueStreamOrFeedbackIconPath ? `<img src="${valueStreamOrFeedbackIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="Value Stream" />` : (gearIconPath ? `<img src="${gearIconPath}" style="margin-right: 8px; width: 36px; height: 36px; object-fit: contain;" alt="Value Stream" />` : '')}
                    <span style="font-weight: 600; font-size: 20px; color: var(--accent-color);">Value Stream</span>
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
    

    renderBehavior(behavior, bIdx, plusIconPath, subtractIconPath, tickIconPath, notTickedIconPath, clipboardIconPath, combinedIconPath, skipIconPath, manualIconPath, executionSettings = {}, specialInstructions = {}) {
        const isCurrent = behavior.isCurrent || behavior.is_current || false;
        const isCompleted = behavior.isCompleted || behavior.is_completed || false;
        const behaviorMarker = isCurrent 
            ? (tickIconPath ? `<img src="${tickIconPath}" alt="Current" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '')
            : isCompleted
            ? (tickIconPath ? `<img src="${tickIconPath}" alt="Completed" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '')
            : (notTickedIconPath ? `<img src="${notTickedIconPath}" alt="Pending" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '');
        
        const behaviorTooltip = behavior.description ? escapeForHtml(behavior.description) : '';
        const behaviorId = `behavior-${bIdx}`;
        const behaviorNameRaw = behavior.name || '';
        const behaviorName = escapeForHtml(behaviorNameRaw);
        const behaviorNameJs = escapeForJs(behaviorNameRaw);
        



        const hasExpansionState = this.expansionState && (behaviorId in this.expansionState);
        const behaviorExpanded = hasExpansionState ? this.expansionState[behaviorId] : (isCurrent || isCompleted);
        const behaviorIconSrc = behaviorExpanded ? subtractIconPath : plusIconPath;
        const behaviorIconAlt = behaviorExpanded ? 'Collapse' : 'Expand';
        const behaviorIconClass = behaviorExpanded ? 'expanded' : '';
        const behaviorDisplay = behaviorExpanded ? 'block' : 'none';
        
        const behaviorActiveClass = isCurrent ? ' active' : '';
        const behaviorExecutionKey = `_behavior.${behaviorNameRaw}`;
        const behaviorCurrentMode = executionSettings[behaviorExecutionKey] || 'manual';
        const behaviorModes = [
            { value: 'combine_with_next', iconPath: combinedIconPath, tooltip: 'combine with next' },
            { value: 'manual', iconPath: manualIconPath, tooltip: 'manual' },
            { value: 'skip', iconPath: skipIconPath, tooltip: 'skip' }
        ];
        const behaviorCurrentModeObj = behaviorModes.find(m => m.value === behaviorCurrentMode) || behaviorModes[0];
        const behaviorToggleButtons = behaviorModes.map(m => {
            const active = behaviorCurrentMode === m.value;
            const content = m.iconPath ? `<img src="${m.iconPath}" alt="${m.tooltip}" style="width: 22px; height: 22px; object-fit: contain; display: block;" />` : m.tooltip;
            return `<button class="execution-toggle-btn${active ? ' active' : ''}" data-action="setBehaviorExecuteMode" data-behavior-name="${behaviorNameJs}" data-mode="${m.value}" title="${m.tooltip}">${content}</button>`;
        }).join('');
        const behaviorExecToggleId = `${behaviorId}-exec-toggle`;
        const behaviorCollapsedBtn = behaviorCurrentModeObj.iconPath ? `<button class="execution-toggle-btn active execution-toggle-collapsed" data-action="toggleExecutionToggle" data-target="${behaviorExecToggleId}" title="${behaviorCurrentModeObj.tooltip}"><img src="${behaviorCurrentModeObj.iconPath}" alt="${behaviorCurrentModeObj.tooltip}" style="width: 22px; height: 22px; object-fit: contain; display: block;" /></button>` : '';
        const behaviorSpecialInstructions = specialInstructions[behaviorNameRaw] || '';
        const behaviorSpecialInstructionsEscaped = escapeForHtml(behaviorSpecialInstructions);
        const behaviorSpecialInstructionsInput = `<textarea class="special-instructions-input" data-action="setBehaviorSpecialInstructions" data-behavior-name="${behaviorNameJs}" placeholder="Special instructions for ${behaviorName}" title="Special instructions for this behavior" style="min-width: 80px; max-width: 200px; font-size: 10px; padding: 2px 4px; resize: vertical; min-height: 18px; max-height: 80px;" onblur="if(window.setBehaviorSpecialInstructions) window.setBehaviorSpecialInstructions(this)" onclick="event.stopPropagation();">${behaviorSpecialInstructionsEscaped}</textarea>`;
        const behaviorExpandedGroup = `<span class="execution-toggle-expanded" style="display: inline-flex; gap: 4px; align-items: center;" onclick="event.stopPropagation();">${behaviorSpecialInstructionsInput}${behaviorToggleButtons}${subtractIconPath ? `<button class="execution-toggle-collapse-btn" data-action="toggleExecutionToggle" data-target="${behaviorExecToggleId}" title="Collapse"><img src="${subtractIconPath}" style="width: 12px; height: 12px; object-fit: contain; display: block;" alt="Collapse" /></button>` : ''}</span>`;
        const behaviorToggleGroup = `<span class="execution-toggle-container" id="${behaviorExecToggleId}" onclick="event.stopPropagation();">${behaviorCollapsedBtn}${behaviorExpandedGroup}</span>`;
        let html = `<div class="collapsible-header card-item${behaviorActiveClass}" data-behavior="${behaviorName}" title="${behaviorTooltip}" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 4px;"><span><span id="${behaviorId}-icon" class="${behaviorIconClass}" style="display: inline-block; min-width: 12px; cursor: pointer;" data-action="toggleCollapse" data-target="${behaviorId}" data-plus="${plusIconPath}" data-subtract="${subtractIconPath}">${plusIconPath && subtractIconPath ? `<img src="${behaviorIconSrc}" alt="${behaviorIconAlt}" style="width: 12px; height: 12px; vertical-align: middle;" />` : ''}</span> <span class="behavior-name-clickable" style="cursor: pointer; text-decoration: underline;" data-action="navigateToBehavior" data-behavior-name="${behaviorNameJs}">${behaviorMarker}${behaviorName}</span>${clipboardIconPath ? `<button class="behavior-rules-button" data-action="getBehaviorRules" data-behavior-name="${behaviorNameJs}" style="background: #000; border: none; padding: 2px 6px; margin: 0 0 0 8px; cursor: pointer; vertical-align: middle; display: inline-flex; align-items: center; transition: opacity 0.15s ease;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Get rules for ${behaviorName} and send to chat"><img src="${clipboardIconPath}" style="width: 22px; height: 22px; object-fit: contain;" alt="Get Rules" /></button>` : ''}</span>${behaviorToggleGroup}</div>`;
        

        const actionsArray = behavior.actions?.all_actions || behavior.actions || [];
        const hasActions = Array.isArray(actionsArray) && actionsArray.length > 0;
        const actionsHtml = hasActions ? actionsArray.map((action, aIdx) => {
            return this.renderAction(action, bIdx, aIdx, behaviorName, behaviorNameJs, behaviorNameRaw, plusIconPath, subtractIconPath, tickIconPath, notTickedIconPath, combinedIconPath, skipIconPath, manualIconPath, executionSettings, specialInstructions);
        }).join('') : '';
        
        html += `<div id="${behaviorId}" class="collapsible-content" style="display: ${behaviorDisplay};">${actionsHtml}</div>`;
        
        return html;
    }
    

    renderAction(action, bIdx, aIdx, behaviorName, behaviorNameJs, behaviorNameRaw, plusIconPath, subtractIconPath, tickIconPath, notTickedIconPath, combinedIconPath, skipIconPath, manualIconPath, executionSettings = {}, specialInstructions = {}) {
        const isCurrent = action.isCurrent || action.is_current || false;
        const isCompleted = action.isCompleted || action.is_completed || false;
        const actionMarker = isCurrent
            ? (tickIconPath ? `<img src="${tickIconPath}" alt="Current" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '')
            : isCompleted
            ? (tickIconPath ? `<img src="${tickIconPath}" alt="Completed" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '')
            : (notTickedIconPath ? `<img src="${notTickedIconPath}" alt="Pending" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;" />` : '');
        
        const actionTooltip = action.description ? escapeForHtml(action.description) : '';
        const actionNameRaw = action.action_name || action.name || '';
        const actionName = escapeForHtml(actionNameRaw);
        const actionNameJs = escapeForJs(actionNameRaw);
        const executionKey = `${behaviorNameRaw}.${actionNameRaw}`;
        const currentMode = executionSettings[executionKey] || 'manual';
        
        const modes = [
            { value: 'combine_next', iconPath: combinedIconPath, tooltip: 'combine with next' },
            { value: 'manual', iconPath: manualIconPath, tooltip: 'manual' },
            { value: 'skip', iconPath: skipIconPath, tooltip: 'skip' }
        ];
        const currentModeObj = modes.find(m => m.value === currentMode) || modes[0];
        const toggleButtons = modes.map(m => {
            const active = currentMode === m.value;
            const content = m.iconPath ? `<img src="${m.iconPath}" alt="${m.tooltip}" style="width: 22px; height: 22px; object-fit: contain; display: block;" />` : m.tooltip;
            return `<button class="execution-toggle-btn${active ? ' active' : ''}" data-action="setExecutionMode" data-behavior-name="${behaviorNameJs}" data-action-name="${actionNameJs}" data-mode="${m.value}" title="${m.tooltip}">${content}</button>`;
        }).join('');
        const actionExecToggleId = `action-${bIdx}-${aIdx}-exec-toggle`;
        const actionCollapsedBtn = currentModeObj.iconPath ? `<button class="execution-toggle-btn active execution-toggle-collapsed" data-action="toggleExecutionToggle" data-target="${actionExecToggleId}" title="${currentModeObj.tooltip}"><img src="${currentModeObj.iconPath}" alt="${currentModeObj.tooltip}" style="width: 22px; height: 22px; object-fit: contain; display: block;" /></button>` : '';
        const actionSpecialInstructionsKey = `${behaviorNameRaw}.${actionNameRaw}`;
        const actionSpecialInstructions = specialInstructions[actionSpecialInstructionsKey] || '';
        const actionSpecialInstructionsEscaped = escapeForHtml(actionSpecialInstructions);
        const actionSpecialInstructionsInput = `<textarea class="special-instructions-input" data-action="setActionSpecialInstructions" data-behavior-name="${behaviorNameJs}" data-action-name="${actionNameJs}" placeholder="Special instructions for ${behaviorName}.${actionNameRaw}" title="Special instructions for ${behaviorName}.${actionNameRaw}" style="min-width: 80px; max-width: 200px; font-size: 10px; padding: 2px 4px; resize: vertical; min-height: 18px; max-height: 80px;" onblur="if(window.setActionSpecialInstructions) window.setActionSpecialInstructions(this)" onclick="event.stopPropagation();">${actionSpecialInstructionsEscaped}</textarea>`;
        const actionExpandedGroup = `<span class="execution-toggle-expanded" style="display: inline-flex; gap: 4px; align-items: center;" onclick="event.stopPropagation();">${actionSpecialInstructionsInput}${toggleButtons}${subtractIconPath ? `<button class="execution-toggle-collapse-btn" data-action="toggleExecutionToggle" data-target="${actionExecToggleId}" title="Collapse"><img src="${subtractIconPath}" style="width: 12px; height: 12px; object-fit: contain; display: block;" alt="Collapse" /></button>` : ''}</span>`;
        const actionToggleGroup = `<span class="execution-toggle-container" id="${actionExecToggleId}" onclick="event.stopPropagation();">${actionCollapsedBtn}${actionExpandedGroup}</span>`;
        const actionActiveClass = isCurrent ? ' active' : '';
        const actionHtml = `<div class="collapsible-header action-item card-item${actionActiveClass}" title="${actionTooltip}" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 4px;">
            <span class="action-name-clickable" style="cursor: pointer; text-decoration: underline;" data-action="navigateToAction" data-behavior-name="${behaviorNameJs}" data-action-name="${actionNameJs}">${actionMarker}${actionName}</span>
            ${actionToggleGroup}
        </div>`;
        
        return actionHtml;
    }
    

    async handleEvent(eventType, eventData) {
        if (eventType === 'execute') {

            return { success: true };
        }
        throw new Error(`Unknown event type: ${eventType}`);
    }
}

module.exports = BehaviorsView;
