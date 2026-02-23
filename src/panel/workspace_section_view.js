/**
 * WorkspaceSectionView - Renders Build and Render sections between story map and instructions.
 */

const PanelView = require('./panel_view');
const branding = require('./branding');
const DiagramSectionView = require('./diagram_section_view');
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
        const instructionsData = lastResponse.instructions || botData?.instructions || {};
        const currentAction = lastResponse.bot?.current_action || lastResponse.current_action ||
            botData?.current_action || botData?.behaviors?.current_action || '';
        const currentBehavior = botData?.behaviors?.current_behavior || botData?.current_behavior || '';

        const getIcon = (name) => branding.getImageUri(this.webview, this.extensionUri, name);
        const renderDiagramIconPath = getIcon('render_diagram.png');
        const saveLayoutIconPath = getIcon('save_layout.png');
        const clearLayoutIconPath = getIcon('clear_layout.png');
        const generateReportIconPath = getIcon('generate_report.png');
        const updateGraphIconPath = getIcon('update_graph.png');
        const jsonIconPath = getIcon('json.png');
        const filesIconPath = getIcon('files.png');
        const gearIconPath = getIcon('gear.png');
        const documentIconPath = getIcon('document.png');
        const testTubeIconPath = getIcon('test_tube.png');

        const graphLinks = botData?.scope?.graphLinks || [];
        const drawioLinks = graphLinks.filter(l => l.url && l.url.endsWith('.drawio'));
        const drawioPath = drawioLinks.length > 0 ? escapeForJs(drawioLinks[0].url) : '';

        const diagramsHtml = this._renderDiagramsSubsection(instructionsData, botData, drawioLinks, renderDiagramIconPath, saveLayoutIconPath, clearLayoutIconPath, generateReportIconPath, updateGraphIconPath, drawioPath);
        const buildHtml = this._renderBuildSubsection(instructionsData, currentAction, botData, jsonIconPath, filesIconPath, documentIconPath, testTubeIconPath);

        if (!diagramsHtml && !buildHtml) return '';

        return `
    <div class="section card-primary" style="margin-top: 8px;">
        <div class="collapsible-section expanded">
            <div class="collapsible-header" onclick="toggleSection('workspace-content')" style="
                cursor: pointer;
                padding: 2px 4px;
                display: flex;
                align-items: center;
                user-select: none;
            ">
                <span class="expand-icon" style="margin-right: 8px; font-size: 28px; transition: transform 0.15s;">▸</span>
                ${gearIconPath ? `<img src="${gearIconPath}" style="margin-right: 8px; width: 28px; height: 28px; object-fit: contain;" alt="Workspace" />` : ''}
                <span style="font-weight: 600; font-size: 20px; color: var(--accent-color);">Workspace</span>
            </div>
            <div id="workspace-content" class="collapsible-content" style="max-height: none; overflow: visible; display: block;">
                ${buildHtml}
                ${diagramsHtml}
            </div>
        </div>
    </div>`;
    }

    _renderDiagramsSubsection(instructions, botData, drawioLinks, renderIcon, saveIcon, clearIcon, reportIcon, updateIcon, drawioPath) {
        let content = '';

        // Diagram action buttons
        content += `
            <div id="ws-diagram-buttons" style="display: flex; align-items: center; gap: 2px; margin-bottom: 2px;">
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

        // Render output links (from scope if files exist, or from instructions after render)
        const outputPathsFromScope = (instructions.render_output_paths || []).length > 0
            ? instructions.render_output_paths
            : (botData?.scope?.renderOutputLinks || []).filter(l => l.exists).map(l => l.url);
        const outputPaths = outputPathsFromScope;
        if (outputPaths.length > 0) {
            content += '<div style="margin-top: 3px;">';
            outputPaths.forEach((outputPath, idx) => {
                content += `<div style="margin-top: 2px; font-size: 12px;" title="${escapeForHtml(outputPath)}">`;
                content += this._renderFileLink(outputPath);
                content += '</div>';
            });
            content += '</div>';
        }

        // Rules links
        const rules = instructions.rules || [];
        if (rules.length > 0) {
            content += '<div style="margin-top: 3px;">';
            rules.forEach((rule, idx) => {
                const rulePath = typeof rule === 'string' ? rule : rule.rule_file || '';
                if (rulePath) {
                    content += `<div style="margin-top: 2px; font-size: 12px;" title="${escapeForHtml(rulePath)}">`;
                    content += `<span style="color: var(--text-color-faded);">Rule:</span> `;
                    content += this._renderFileLink(rulePath);
                    content += '</div>';
                }
            });
            content += '</div>';
        }

        return `
        <div class="collapsible-section expanded" style="margin-bottom: 4px;">
            <div class="collapsible-header" onclick="toggleSection('ws-diagrams-content')" style="cursor: pointer; padding: 2px 4px; display: flex; align-items: center; user-select: none;">
                <span class="expand-icon">▸</span>
                <span style="font-weight: 600; color: var(--vscode-foreground); font-size: 14px;">Render</span>
            </div>
            <div id="ws-diagrams-content" class="collapsible-content" style="max-height: none; overflow: visible; display: block;">
                <div style="padding: 0 4px 2px 4px;">
                    ${content}
                </div>
            </div>
        </div>`;
    }

    _renderBuildSubsection(instructions, currentAction, botData, jsonIconPath, filesIconPath, documentIconPath, testTubeIconPath) {
        let content = '';

        // Build section: Document, Test tube, All files, Open Story Graph (compact, minimal padding)
        content += `
            <div style="display: flex; align-items: center; gap: 2px; margin-bottom: 2px;">
                <button id="ws-btn-open-file" onclick="event.stopPropagation(); handleOpenFile();" style="background: transparent; border: none; padding: 0; cursor: pointer; transition: opacity 0.15s ease; width: 28px; height: 28px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Open file or folder for selected node">
                    <img src="${documentIconPath}" style="width: 24px; height: 24px; object-fit: contain; display: block;" alt="File" />
                </button>
                <button id="ws-btn-open-test" onclick="event.stopPropagation(); handleOpenTest();" style="background: transparent; border: none; padding: 0; cursor: pointer; transition: opacity 0.15s ease; width: 28px; height: 28px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Open test for selected node">
                    <img src="${testTubeIconPath}" style="width: 24px; height: 24px; object-fit: contain; display: block;" alt="Test" />
                </button>
                <button id="ws-btn-open-all" onclick="event.stopPropagation(); handleOpenAll();" style="background: transparent; border: none; padding: 0; cursor: pointer; transition: opacity 0.15s ease; width: 28px; height: 28px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Open all related files in split editors">
                    <img src="${filesIconPath}" style="width: 24px; height: 24px; object-fit: contain; display: block;" alt="All" />
                </button>
                <button id="ws-btn-open-graph" onclick="event.stopPropagation(); handleOpenGraph();" style="background: transparent; border: none; padding: 0; cursor: pointer; transition: opacity 0.15s ease; width: 56px; height: 56px; display: flex; align-items: center; justify-content: center;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Open story graph with selected node expanded">
                    <img src="${jsonIconPath}" style="width: 52px; height: 52px; object-fit: contain; display: block;" alt="Story Graph" />
                </button>
            </div>`;

        // Build content (schema + rules) - shown when build action
        const hasBuildData = instructions.schema || instructions.story_graph_template || instructions.story_graph_config || instructions.build_instructions;
        if (hasBuildData && currentAction === 'build') {
            let schemaData = instructions.schema || instructions.build_instructions?.schema || {};
            if (instructions.story_graph_template) schemaData = { ...schemaData, ...instructions.story_graph_template };
            if (instructions.story_graph_config) schemaData = { ...schemaData, ...instructions.story_graph_config };
            const buildRules = instructions.rules || instructions.build_instructions?.rules || [];

            if (Object.keys(schemaData).length > 0) {
                content += `<div style="margin-top: 2px; font-size: 12px; color: var(--text-color-faded);">Story Graph schema loaded</div>`;
            }
            if (buildRules.length > 0) {
                buildRules.forEach(rule => {
                    const rulePath = typeof rule === 'string' ? rule : rule.rule_file || '';
                    if (rulePath) {
                        content += `<div style="margin-top: 2px; font-size: 12px;" title="${escapeForHtml(rulePath)}">`;
                        content += `<span style="color: var(--text-color-faded);">Build Rule:</span> `;
                        content += this._renderFileLink(rulePath);
                        content += '</div>';
                    }
                });
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
            <div class="collapsible-header" onclick="toggleSection('ws-build-content')" style="cursor: pointer; padding: 2px 4px; display: flex; align-items: center; user-select: none;">
                <span class="expand-icon">▸</span>
                <span style="font-weight: 600; color: var(--vscode-foreground); font-size: 14px;">Build</span>
            </div>
            <div id="ws-build-content" class="collapsible-content" style="max-height: none; overflow: visible; display: block;">
                <div style="padding: 0 4px 2px 4px;">
                    ${content}
                </div>
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
