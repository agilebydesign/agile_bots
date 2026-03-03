/**
 * WorkspaceSectionView - Renders Build and Render sections between story map and instructions.
 */

const PanelView = require('./panel_view');
const branding = require('./branding');
const DiagramSectionView = require('./diagram_section_view');
const InstructionsSection = require('./instructions/instructions_view');
const { escapeForHtml, escapeForJs, log } = require('./utils');

class WorkspaceSectionView extends PanelView {
    constructor(botPathOrCli, webview, extensionUri, parentView = null) {
        super(botPathOrCli);
        this.webview = webview || null;
        this.extensionUri = extensionUri || null;
        this.parentView = parentView;
    }

    async render() {
        const botData = this.parentView?.botData;
        if (!botData) return '';

        const lastResponse = PanelView._lastResponse || {};
        let instructionsData = lastResponse.instructions || botData?.instructions || {};
        const currentAction = lastResponse.bot?.current_action || lastResponse.current_action ||
            botData?.current_action || botData?.behaviors?.current_action || '';
        const currentBehavior = botData?.behaviors?.current_behavior || botData?.current_behavior || '';

        // Fetch clarifications, strategies, rules via CLI (shape.clarifications, shape.strategies, shape.rules)
        const executor = this.parentView?.execute?.bind(this.parentView) || this.execute?.bind(this);
        if (currentBehavior && executor) {
            try {
                const [clarResp, stratResp, rulesResp] = await Promise.all([
                    executor(`${currentBehavior}.clarifications`),
                    executor(`${currentBehavior}.strategies`),
                    executor(`${currentBehavior}.rules`)
                ]);
                instructionsData = { ...instructionsData };
                const emptyClarification = { key_questions: { answers: {} }, evidence: { required: [], provided: {} } };
                if (clarResp?.result !== undefined && clarResp.result && typeof clarResp.result === 'object') {
                    instructionsData.clarification = { [currentBehavior]: clarResp.result };
                } else {
                    instructionsData.clarification = { [currentBehavior]: emptyClarification };
                }
                if (stratResp?.result !== undefined) {
                    instructionsData.strategy = stratResp.result && typeof stratResp.result === 'object'
                        ? { [currentBehavior]: stratResp.result }
                        : {};
                }
                if (rulesResp?.result && Array.isArray(rulesResp.result)) {
                    instructionsData.rules = rulesResp.result;
                }
            } catch (e) {
                log('[WorkspaceSectionView] CLI fetch for clarifications/strategies/rules failed: ' + (e?.message || e));
            }
        }

        const getIcon = (name) => branding.getImageUri(this.webview, this.extensionUri, name);
        const renderDiagramIconPath = getIcon('render_diagram.png');
        const saveLayoutIconPath = getIcon('save_layout.png');
        const clearLayoutIconPath = getIcon('clear_layout.png');
        const generateReportIconPath = getIcon('generate_report.png');
        const updateGraphIconPath = getIcon('update_graph.png');
        const jsonIconPath = getIcon('json.png');
        const filesIconPath = getIcon('files.png');
        const gearIconPath = getIcon('gear.png');
        const submitIconPath = getIcon('submit.png');
        const subtractIconPath = getIcon('subtract.png');
        const documentIconPath = getIcon('document.png');
        const testTubeIconPath = getIcon('test_tube.png');

        const graphLinks = botData?.scope?.graphLinks || [];
        const allDrawioLinks = graphLinks.filter(l => l.url && l.url.endsWith('.drawio'));
        // Filter to current behavior (path contains /behavior/ or \behavior\) - restore behavior-scoped display
        const drawioLinks = currentBehavior
            ? allDrawioLinks.filter(l => (l.url || '').includes('/' + currentBehavior + '/') || (l.url || '').includes('\\' + currentBehavior + '\\'))
            : allDrawioLinks;
        const drawioPath = drawioLinks.length > 0 ? escapeForJs(drawioLinks[0].url) : '';

        const getIconMore = (name) => branding.getImageUri(this.webview, this.extensionUri, name);
        const buildDiagramIconPath = getIcon('build_diagram.png');
        const renderSectionIconPath = getIcon('render_section.png');
        const clarifyHtml = this._renderClarifySubsection(instructionsData, currentBehavior, getIconMore);
        const strategyHtml = this._renderStrategySubsection(instructionsData, currentBehavior, getIconMore);
        const buildHtml = this._renderBuildSubsection(instructionsData, currentAction, botData, jsonIconPath, filesIconPath, documentIconPath, testTubeIconPath, buildDiagramIconPath);
        const diagramsHtml = this._renderDiagramsSubsection(instructionsData, botData, currentBehavior, drawioLinks, renderDiagramIconPath, saveLayoutIconPath, clearLayoutIconPath, generateReportIconPath, updateGraphIconPath, drawioPath, renderSectionIconPath);

        if (!diagramsHtml && !buildHtml && !clarifyHtml && !strategyHtml) return '';

        const behaviorNames = botData?.behaviors?.names || botData?.behavior_names || (botData?.behaviors?.all_behaviors || []).map(b => (typeof b === 'string' ? b : b?.name)).filter(Boolean) || [];
        const behaviorIconMap = {
            shape: 'shape_icon.png',
            code: 'code_icon.png',
            prioritization: 'prioritization.png',
            scenarios: 'inject_scenarios.png',
            tests: 'test_tube.png',
            exploration: 'exploration_icon.png',
            domain: 'domain_icon.png',
            design: 'design_icon.png',
            walkthrough: 'walkthrough_icon.png'
        };
        const wsBehaviorExecToggleId = 'ws-behavior-exec-toggle';
        const currentBehaviorIcon = (currentBehavior && behaviorIconMap[currentBehavior] ? getIcon(behaviorIconMap[currentBehavior]) : null) || (behaviorNames[0] && behaviorIconMap[behaviorNames[0]] ? getIcon(behaviorIconMap[behaviorNames[0]]) : null);
        const currentBehaviorLabel = (currentBehavior || behaviorNames[0] || '').charAt(0).toUpperCase() + (currentBehavior || behaviorNames[0] || '').slice(1);
        const behaviorCollapsedBtn = currentBehaviorIcon ? `<button class="execution-toggle-btn active execution-toggle-collapsed" data-action="toggleExecutionToggle" data-target="${wsBehaviorExecToggleId}" title="${escapeForHtml(currentBehaviorLabel)}"><img src="${currentBehaviorIcon}" alt="${escapeForHtml(currentBehaviorLabel)}" style="width: 20px; height: 20px; object-fit: contain; display: block;" /></button>` : '';
        const behaviorExpandedButtons = behaviorNames.length > 0 ? behaviorNames.map(name => {
            const isActive = name === currentBehavior;
            const iconFile = behaviorIconMap[name];
            const iconPath = iconFile ? getIcon(iconFile) : null;
            const label = name.charAt(0).toUpperCase() + name.slice(1);
            const content = iconPath ? `<img src="${iconPath}" style="width: 20px; height: 20px; object-fit: contain;" alt="" />` : `<span style="font-size: 11px; color: ${isActive ? 'var(--accent-color)' : 'var(--text-color-faded)'};">${escapeForHtml(label)}</span>`;
            return `<button class="execution-toggle-btn${isActive ? ' active' : ''}" data-action="navigateToBehavior" data-behavior-name="${escapeForHtml(name)}" title="${escapeForHtml(label)}">${content}</button>`;
        }).join('') : '';
        const behaviorExpandedGroup = `<span class="execution-toggle-expanded" style="display: inline-flex; gap: 4px; align-items: center;" onclick="event.stopPropagation();">${behaviorExpandedButtons}${subtractIconPath ? `<button class="execution-toggle-collapse-btn" data-action="toggleExecutionToggle" data-target="${wsBehaviorExecToggleId}" title="Collapse"><img src="${subtractIconPath}" style="width: 12px; height: 12px; object-fit: contain; display: block;" alt="Collapse" /></button>` : ''}</span>`;
        const behaviorToggleGroupHtml = behaviorNames.length > 0 ? `<span class="execution-toggle-container" id="${wsBehaviorExecToggleId}" style="flex-shrink: 0;" onclick="event.stopPropagation();">${behaviorExpandedGroup}${behaviorCollapsedBtn}</span>` : '';

        return `
    <div class="section card-primary" style="margin-top: 8px;">
        <div class="collapsible-section expanded">
            <div class="collapsible-header" onclick="toggleSection('workspace-content')" style="
                cursor: pointer;
                padding: 2px 4px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                user-select: none;
            ">
                <div style="display: flex; align-items: center;">
                    <span class="expand-icon" style="margin-right: 8px; font-size: 28px; transition: transform 0.15s;">▸</span>
                    ${gearIconPath ? `<img src="${gearIconPath}" style="margin-right: 8px; width: 28px; height: 28px; object-fit: contain;" alt="Workspace" />` : ''}
                    <span style="font-weight: 600; font-size: 20px; color: var(--accent-color);">Workspace</span>
                </div>
                <div style="display: flex; align-items: center; gap: 4px; flex-shrink: 0; margin-left: auto;">
                ${behaviorToggleGroupHtml || ''}
                <button id="ws-submit-btn" onclick="event.stopPropagation(); if(window.submitWorkspaceBehaviorInstructions) window.submitWorkspaceBehaviorInstructions()" style="background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 32px; min-height: 32px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Submit ${escapeForHtml((currentBehavior || '').charAt(0).toUpperCase() + (currentBehavior || '').slice(1))} for all">
                    <img src="${submitIconPath}" style="width: 24px; height: 24px; object-fit: contain; display: block;" alt="Submit" />
                </button>
                </div>
            </div>
            <div id="workspace-content" class="collapsible-content" style="max-height: 400px; overflow-y: auto; overflow-x: hidden; display: block;">
                ${clarifyHtml}
                ${strategyHtml}
                ${buildHtml}
                ${diagramsHtml}
            </div>
        </div>
    </div>`;
    }

    _renderDiagramsSubsection(instructions, botData, currentBehavior, drawioLinks, renderIcon, saveIcon, clearIcon, reportIcon, updateIcon, drawioPath, renderSectionIconPath) {
        let content = '';

        // Diagram action buttons
        content += `<div id="ws-diagram-buttons" style="display: flex; align-items: center; gap: 2px; margin-bottom: 2px;">
                <button class="render-button" onclick="event.stopPropagation(); vscode.postMessage({ command: 'renderDiagram', scope: (window.diagramScope || ''), path: '${drawioPath}' })" style="background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 32px; min-height: 32px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Render diagram">
                    <img src="${renderIcon}" style="width: 24px; height: 24px; object-fit: contain; display: block;" alt="Render Diagram" />
                </button>
                <button class="save-layout-button" onclick="event.stopPropagation(); vscode.postMessage({ command: 'saveDiagramLayout', scope: (window.diagramScope || '') })" style="background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 32px; min-height: 32px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Save layout">
                    <img src="${saveIcon}" style="width: 24px; height: 24px; object-fit: contain; display: block;" alt="Save Layout" />
                </button>
                <button class="clear-layout-button" onclick="event.stopPropagation(); vscode.postMessage({ command: 'clearDiagramLayout', scope: (window.diagramScope || '') })" style="background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 32px; min-height: 32px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Clear layout">
                    <img src="${clearIcon}" style="width: 24px; height: 24px; object-fit: contain; display: block;" alt="Clear Layout" />
                </button>
                <button class="generate-report-button" onclick="event.stopPropagation(); vscode.postMessage({ command: 'generateDiagramReport', scope: (window.diagramScope || ''), path: '${drawioPath}' })" style="background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 32px; min-height: 32px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Generate report">
                    <img src="${reportIcon}" style="width: 24px; height: 24px; object-fit: contain; display: block;" alt="Generate Report" />
                </button>
                <button class="update-button" onclick="event.stopPropagation(); vscode.postMessage({ command: 'updateFromDiagram', scope: (window.diagramScope || '') })" style="background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 32px; min-height: 32px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Update graph">
                    <img src="${updateIcon}" style="width: 24px; height: 24px; object-fit: contain; display: block;" alt="Update Graph" />
                </button>
            </div>`;

        // Diagram files (from drawioLinks - same source as buttons, not instructions.diagrams)
        if (drawioLinks && drawioLinks.length > 0) {
            const diagramsForView = drawioLinks.map(l => ({
                file_path: l.url,
                report_path: null,
                exists: true
            }));
            const diagramView = new DiagramSectionView(diagramsForView);
            content += diagramView.renderSection();
        }

        // Render output links: instructions (behavior-scoped) or scope filtered by current behavior
        const outputPathsFromInstructions = instructions.render_output_paths || [];
        const outputPaths = outputPathsFromInstructions.length > 0
            ? outputPathsFromInstructions
            : (botData?.scope?.renderOutputLinks || [])
                .filter(l => l.exists && (!currentBehavior || (l.url || '').includes('/' + currentBehavior + '/') || (l.url || '').includes('\\' + currentBehavior + '\\')))
                .map(l => l.url);
        if (outputPaths.length > 0) {
            content += '<div style="margin-top: 3px;">';
            outputPaths.forEach((outputPath, idx) => {
                content += `<div style="margin-top: 2px; font-size: 12px;" title="${escapeForHtml(outputPath)}">`;
                content += this._renderFileLink(outputPath);
                content += '</div>';
            });
            content += '</div>';
        }

        return `
        <div class="collapsible-section expanded" style="margin-bottom: 4px;">
            <div class="collapsible-header" onclick="toggleSection('ws-diagrams-content')" style="cursor: pointer; padding: 0 4px 0 4px; display: flex; align-items: center; user-select: none;">
                <span class="expand-icon">▸</span>
                ${renderSectionIconPath ? `<img src="${renderSectionIconPath}" style="margin-right: 8px; width: 20px; height: 20px; object-fit: contain; vertical-align: middle;" alt="Render" />` : ''}
                <span style="font-weight: 600; color: var(--vscode-foreground); font-size: 14px;">Render</span>
            </div>
            <div id="ws-diagrams-content" class="collapsible-content" style="max-height: none; overflow: visible; display: block;">
                <div style="padding: 0 4px 2px 4px;">
                    ${content}
                </div>
            </div>
        </div>`;
    }

    _renderBuildSubsection(instructions, currentAction, botData, jsonIconPath, filesIconPath, documentIconPath, testTubeIconPath, buildDiagramIconPath) {
        let content = '';

        // Build section: Document, Test tube, All files, Open Story Graph (compact like Render buttons)
        content += `<div id="ws-build-buttons" style="display: flex; align-items: center; gap: 2px; margin-bottom: 2px;">
                <button id="ws-btn-open-file" onclick="event.stopPropagation(); handleOpenFile();" style="background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 32px; min-height: 32px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Open file or folder for selected node">
                    <img src="${documentIconPath}" style="width: 24px; height: 24px; object-fit: contain; display: block;" alt="File" />
                </button>
                <button id="ws-btn-open-test" onclick="event.stopPropagation(); handleOpenTest();" style="background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 32px; min-height: 32px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Open test for selected node">
                    <img src="${testTubeIconPath}" style="width: 24px; height: 24px; object-fit: contain; display: block;" alt="Test" />
                </button>
                <button id="ws-btn-open-all" onclick="event.stopPropagation(); handleOpenAll();" style="background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 32px; min-height: 32px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Open all related files in split editors">
                    <img src="${filesIconPath}" style="width: 24px; height: 24px; object-fit: contain; display: block;" alt="All" />
                </button>
                <button id="ws-btn-open-graph" onclick="event.stopPropagation(); handleOpenGraph();" style="background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 40px; min-height: 40px; display: flex; align-items: center; justify-content: center;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Open story graph with selected node expanded">
                    <img src="${jsonIconPath}" style="width: 36px; height: 36px; object-fit: contain; display: block;" alt="Story Graph" />
                </button>
            </div>`;

        // Rules - shown below Build buttons when available (regardless of action), collapsible
        const buildRules = instructions.rules || instructions.build_instructions?.rules || [];
        if (buildRules.length > 0) {
            let rulesLinksHtml = '';
            buildRules.forEach(rule => {
                const rulePath = typeof rule === 'string' ? rule : (rule.rule_file_path || rule.rule_file || '');
                if (rulePath) {
                    rulesLinksHtml += `<div style="margin-top: 2px; font-size: 12px;" title="${escapeForHtml(rulePath)}">`;
                    rulesLinksHtml += this._renderFileLink(rulePath);
                    rulesLinksHtml += '</div>';
                }
            });
            content += `
        <div class="collapsible-section expanded" style="margin-top: 4px; margin-bottom: 2px;">
            <div class="collapsible-header" onclick="toggleSection('ws-build-rules-content')" style="cursor: pointer; padding: 2px 0; display: flex; align-items: center; user-select: none;">
                <span class="expand-icon">▸</span>
                <span style="font-weight: 600; color: var(--vscode-foreground); font-size: 13px;">Rules</span>
            </div>
            <div id="ws-build-rules-content" class="collapsible-content" style="max-height: none; overflow: visible; display: block;">
                <div style="padding-left: 14px;">
                    ${rulesLinksHtml}
                </div>
            </div>
        </div>`;
        }

        // Build content (schema) - shown when build action
        const hasBuildData = instructions.schema || instructions.story_graph_template || instructions.story_graph_config || instructions.build_instructions;
        if (hasBuildData && currentAction === 'build') {
            let schemaData = instructions.schema || instructions.build_instructions?.schema || {};
            if (instructions.story_graph_template) schemaData = { ...schemaData, ...instructions.story_graph_template };
            if (instructions.story_graph_config) schemaData = { ...schemaData, ...instructions.story_graph_config };

            if (Object.keys(schemaData).length > 0) {
                content += `<div style="margin-top: 2px; font-size: 12px; color: var(--text-color-faded);">Story Graph schema loaded</div>`;
            }
        }

        // Clarify content - shown when clarify action
        if (currentAction === 'clarify' && instructions.clarification_data) {
            const clarifyData = instructions.clarification_data;
            if (Array.isArray(clarifyData) && clarifyData.length > 0) {
                content += `<div style="margin-top: 2px; font-size: 12px; color: var(--text-color-faded);">${clarifyData.length} clarification question(s)</div>`;
            }
        }

        return `
        <div class="collapsible-section expanded" style="margin-bottom: 4px;">
            <div class="collapsible-header" onclick="toggleSection('ws-build-content')" style="cursor: pointer; padding: 0 4px 0 4px; display: flex; align-items: center; user-select: none;">
                <span class="expand-icon">▸</span>
                ${buildDiagramIconPath ? `<img src="${buildDiagramIconPath}" style="margin-right: 8px; width: 20px; height: 20px; object-fit: contain; vertical-align: middle;" alt="Build" />` : ''}
                <span style="font-weight: 600; color: var(--vscode-foreground); font-size: 14px;">Build</span>
            </div>
            <div id="ws-build-content" class="collapsible-content" style="max-height: none; overflow: visible; display: block;">
                <div style="padding: 0 4px 2px 4px;">
                    ${content}
                </div>
            </div>
        </div>`;
    }

    _renderClarifySubsection(instructions, currentBehavior, getIcon) {
        const botPathOrCli = this._cli || this._botPath || this.parentView?._cli || this.parentView?._botPath;
        const instrView = new InstructionsSection(botPathOrCli, this.webview, this.extensionUri, this.parentView);
        const rawClarification = instructions.clarification;
        const savedClarification = (rawClarification && currentBehavior && rawClarification[currentBehavior] && !rawClarification.key_questions)
            ? rawClarification[currentBehavior]
            : rawClarification;
        const hasSavedAnswers = savedClarification &&
            savedClarification.key_questions &&
            savedClarification.key_questions.answers &&
            Object.keys(savedClarification.key_questions.answers).length > 0;

        let clarificationDataArray = [];
        if (hasSavedAnswers) {
            clarificationDataArray = Object.keys(savedClarification.key_questions.answers).map(question => ({
                question,
                answer: savedClarification.key_questions.answers[question]
            }));
        }
        if (clarificationDataArray.length === 0 && instructions.guardrails?.required_context?.key_questions) {
            clarificationDataArray = instructions.guardrails.required_context.key_questions.map(q => ({ question: q, answer: '' }));
        }
        const evidenceData = savedClarification?.evidence || { required: [], provided: {} };
        const clarifyData = {
            clarification_data: clarificationDataArray,
            evidence: evidenceData,
            guardrails: instructions.guardrails || instructions.clarify_instructions?.guardrails
        };
        const content = instrView._formatClarifyInstructions(clarifyData, 'ws-');
        const iconPath = getIcon ? getIcon('light_bulb_head.png') : null;

        return `
        <div class="collapsible-section expanded" style="margin-bottom: 4px;">
            <div class="collapsible-header" onclick="toggleSection('ws-clarify-content')" style="cursor: pointer; padding: 0 4px 0 4px; display: flex; align-items: center; user-select: none;">
                <span class="expand-icon">▸</span>
                ${iconPath ? `<img src="${iconPath}" style="margin-right: 8px; width: 20px; height: 20px; object-fit: contain; vertical-align: middle;" alt="Clarify" />` : ''}
                <span style="font-weight: 600; color: var(--vscode-foreground); font-size: 14px;">Clarify</span>
            </div>
            <div id="ws-clarify-content" class="collapsible-content" style="max-height: none; overflow: visible; display: block;">
                <div style="padding: 0 4px 2px 4px;">${content}</div>
            </div>
        </div>`;
    }

    _renderStrategySubsection(instructions, currentBehavior, getIcon) {
        const botPathOrCli = this._cli || this._botPath || this.parentView?._cli || this.parentView?._botPath;
        const instrView = new InstructionsSection(botPathOrCli, this.webview, this.extensionUri, this.parentView);
        const rawStrategy = instructions.strategy;
        const savedStrategy = (rawStrategy && currentBehavior && rawStrategy[currentBehavior] && !rawStrategy.strategy_criteria)
            ? rawStrategy[currentBehavior]
            : rawStrategy;
        // Raw format = strategy.json: { decisions, assumptions|additional_strategies }; full format = behavior.strategies: { strategy_criteria, assumptions: { assumptions_made } }
        const isRawFormat = savedStrategy && savedStrategy.decisions !== undefined && !savedStrategy.strategy_criteria;
        let strategyCriteriaData = savedStrategy?.strategy_criteria?.criteria || {};
        let decisionsMade = isRawFormat ? (savedStrategy.decisions || {}) : (savedStrategy?.strategy_criteria?.decisions_made || {});
        let assumptionsMade = isRawFormat ? (savedStrategy.assumptions || savedStrategy.additional_strategies || []) : (savedStrategy?.assumptions?.assumptions_made || []);
        if (Object.keys(strategyCriteriaData).length === 0) {
            const fallbackData = instructions.strategy_criteria || instructions.guardrails?.decision_criteria || {};
            strategyCriteriaData = fallbackData.criteria || fallbackData;
        }
        const strategyData = {
            strategy_criteria: strategyCriteriaData,
            decisions_made: decisionsMade,
            assumptions_made: assumptionsMade,
            action_instructions: instructions.action_instructions
        };
        const content = instrView._formatStrategyInstructions(strategyData, 'ws-');
        const iconPath = getIcon ? getIcon('lightbulb.png') : null;

        return `
        <div class="collapsible-section expanded" style="margin-bottom: 4px;">
            <div class="collapsible-header" onclick="toggleSection('ws-strategy-content')" style="cursor: pointer; padding: 0 4px 0 4px; display: flex; align-items: center; user-select: none;">
                <span class="expand-icon">▸</span>
                ${iconPath ? `<img src="${iconPath}" style="margin-right: 8px; width: 20px; height: 20px; object-fit: contain; vertical-align: middle;" alt="Strategy" />` : ''}
                <span style="font-weight: 600; color: var(--vscode-foreground); font-size: 14px;">Strategy</span>
            </div>
            <div id="ws-strategy-content" class="collapsible-content" style="max-height: none; overflow: visible; display: block;">
                <div style="padding: 0 4px 2px 4px;">${content}</div>
            </div>
        </div>`;
    }

    _renderFileLink(fullPath) {
        if (!fullPath) return '';
        const fileName = fullPath.split(/[\/\\]/).pop();
        const jsPath = fullPath.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
        return `<a href="#" onclick="openFile('${jsPath}', event); return false;" style="color: var(--vscode-textLink-foreground); text-decoration: none; cursor: pointer; font-size: 12px;">${escapeForHtml(fileName)}</a>`;
    }
}

module.exports = WorkspaceSectionView;
