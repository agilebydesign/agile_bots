/**
 * StoryMapView - Renders story map with filtering and editing capabilities.
 * 
 * Combines scope filtering with story graph editing in one unified view.
 * 
 * Epic: Invoke Bot Through Panel
 * Sub-Epic: Manage Story Graph Through Panel
 * Stories: 
 *   - Display Story Scope Hierarchy, Filter Story Scope
 *   - Edit Story Graph In Panel
 */

const PanelView = require('./panel_view');
const StoryGraphAsyncSaveController = require('./story_graph/async_save_controller.js');
const branding = require('./branding');
const fs = require('fs');
const path = require('path');
const { escapeForHtml, escapeForJs, Logger } = require('./utils');

class StoryMapView extends PanelView {
    /**
     * Story map view with filtering and editing.
     * 
     * @param {string|PanelView} botPathOrCli - Bot path or CLI instance
     * @param {Object} webview - VS Code webview instance (optional)
     * @param {Object} extensionUri - Extension URI (optional)
     * @param {Object} parentView - Parent BotView (optional, for accessing cached botData)
     */
    constructor(botPathOrCli, webview, extensionUri, parentView = null) {
        super(botPathOrCli);
        this.webview = webview || null;
        this.extensionUri = extensionUri || null;
        this.parentView = parentView;
        
        // Initialize save queue using existing StoryGraphAsyncSaveController
        // This manages the backend queue and coordinates with webview for DOM updates
        const backendPanel = this; // StoryMapView extends PanelView, can execute commands
        this.saveQueue = new StoryGraphAsyncSaveController(backendPanel);
    }
    
    /**
     * Render header with save status indicator
     * @param {string} headerHtml - Existing header HTML
     * @returns {string} Header HTML with status indicator
     */
    _renderHeader(headerHtml) {
        return `
            <div class="story-map-header" style="display: flex; justify-content: space-between; align-items: center; padding: 8px 12px;">
                <div>${headerHtml}</div>
            </div>
        `;
    }
    
    /**
     * Create scenario anchor ID from scenario name (matches synchronizer format).
     * 
     * @param {string} scenarioName - Scenario name
     * @returns {string} Anchor ID
     */
    createScenarioAnchor(scenarioName) {
        if (typeof scenarioName !== 'string') {
            scenarioName = String(scenarioName);
        }
        // Normalize for markdown anchor: lowercase, replace spaces/special chars with hyphens
        let anchor = scenarioName.toLowerCase();
        // Replace spaces and common special characters with hyphens
        anchor = anchor.replace(/[^\w\s-]/g, '');
        anchor = anchor.replace(/[-\s]+/g, '-');
        // Remove leading/trailing hyphens
        anchor = anchor.replace(/^-+|-+$/g, '');
        return `scenario-${anchor}`;
    }
    
    /**
     * Render scope section HTML.
     * 
     * @returns {string} HTML string
     */
    async render() {
        // ===== PERFORMANCE: Start story map rendering =====
        const perfRenderStart = performance.now();
        Logger.log('[StoryMapView] [PERF] render() START');
        
        // Use cached botData from parent if available, otherwise fetch it
        const perfStatusStart = performance.now();
        const botData = this.parentView?.botData || await this.execute('status');
        const perfStatusEnd = performance.now();
        const dataSource = this.parentView?.botData ? 'cached' : 'fetched';
        Logger.log(`[StoryMapView] [PERF] Bot data (${dataSource}): ${(perfStatusEnd - perfStatusStart).toFixed(2)}ms`);
        
        const scopeData = botData.scope || { type: 'all', filter: '', content: null, graphLinks: [] };
        
        // Get icon URIs using branding utility (handles ABD vs Scotia paths)
        const perfIconsStart = performance.now();
        const getIcon = (name) => branding.getImageUri(this.webview, this.extensionUri, name);
        
        const clearIconPath = getIcon('close.png');
        const showAllIconPath = getIcon('show_all.png');
        const jsonIconPath = getIcon('json.png');
        const filesIconPath = getIcon('files.png');
        const plusIconPath = getIcon('plus.png');
        const subtractIconPath = getIcon('subtract.png');
        const emptyIconPath = getIcon('empty.png');
        const gearIconPath = getIcon('gear.png');
        const epicIconPath = getIcon('light_bulb2.png');
        const pageIconPath = getIcon('page.png');
        const testTubeIconPath = getIcon('test_tube.png');
        const documentIconPath = getIcon('document.png');
        const addEpicIconPath = getIcon('add_epic.png');
        const addSubEpicIconPath = getIcon('add_sub_epic.png');
        const addStoryIconPath = getIcon('add_story.png');
        const addTestsIconPath = getIcon('add_tests.png');
        const addAcceptanceCriteriaIconPath = getIcon('add_ac.png');
        const deleteIconPath = getIcon('delete.png');
        const deleteChildrenIconPath = getIcon('delete_children.png');
        const scopeToIconPath = getIcon('bullseye.png');
        const scopeMapIconPath = getIcon('scope_map.png');
        const submitShapeIconPath = getIcon('submit_subepic.png');
        const submitExploreIconPath = getIcon('submit_story.png');
        const submitScenarioIconPath = getIcon('submit_ac.png');
        const submitTestIconPath = getIcon('submit_tests.png');
        const submitCodeIconPath = getIcon('submit_code.png');
        const renderDiagramIconPath = getIcon('render_diagram.png');
        const saveLayoutIconPath = getIcon('save_layout.png');
        const clearLayoutIconPath = getIcon('clear_layout.png');
        const generateReportIconPath = getIcon('generate_report.png');
        const updateGraphIconPath = getIcon('update_graph.png');
        const refreshIconPath = getIcon('refresh.png');
        const injectStoriesIconPath = getIcon('inject_stories.png');
        const injectDomainIconPath = getIcon('inject_domain.png');
        const injectCriteriaIconPath = getIcon('inject_criteria.png');
        const injectScenariosIconPath = getIcon('inject_scenarios.png');
        const injectExamplesIconPath = getIcon('inject_examples.png');
        const injectTestsIconPath = getIcon('inject_tests.png');
        const injectCodeIconPath = getIcon('inject_code.png');
        Logger.log(`[StoryMapView] [PERF] Icons loaded: ${(performance.now() - perfIconsStart).toFixed(2)}ms`);
        
        Logger.log(`[StoryMapView] Branding: ${branding.getBranding()}, icon sample: ${gearIconPath}`);

        const drawioLink = (scopeData.graphLinks || []).find(l => l.url && l.url.endsWith('.drawio'));
        const drawioPath = drawioLink ? escapeForJs(drawioLink.url) : '';
        
        // Create contextual action buttons toolbar
        const actionButtonsHtml = `
            <div id="contextual-actions" style="display: flex; align-items: center; margin-left: 12px; margin-right: 12px; gap: 6px;">
                <!-- Left side: Create, delete, scope, and submit buttons -->
                <div style="display: flex; align-items: center; gap: 6px;">
                <!-- Create and delete buttons with tight spacing -->
                <div style="display: flex; align-items: center; gap: 2px;">
                    <button id="btn-create-epic" onclick="event.stopPropagation(); createEpic();" style="display: block; background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 32px; min-height: 32px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Create Epic">
                        <img src="${addEpicIconPath}" style="width: 24px; height: 24px; object-fit: contain; display: block; flex-shrink: 0;" alt="Create Epic" />
                    </button>
                    <button id="btn-create-sub-epic" onclick="event.stopPropagation(); handleContextualCreate('sub-epic');" style="display: none; background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 32px; min-height: 32px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Create Sub-Epic">
                        <img src="${addSubEpicIconPath}" style="width: 24px; height: 24px; object-fit: contain; display: block; flex-shrink: 0;" alt="Create Sub-Epic" />
                    </button>
                    <button id="btn-create-story" onclick="event.stopPropagation(); handleContextualCreate('story');" style="display: none; background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 32px; min-height: 32px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Create Story">
                        <img src="${addStoryIconPath}" style="width: 24px; height: 24px; object-fit: contain; display: block; flex-shrink: 0;" alt="Create Story" />
                    </button>
                    <button id="btn-create-scenario" onclick="event.stopPropagation(); handleContextualCreate('scenario');" style="display: none; background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 32px; min-height: 32px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Create Scenario">
                        <img src="${addTestsIconPath}" style="width: 24px; height: 24px; object-fit: contain; display: block; flex-shrink: 0;" alt="Create Scenario" />
                    </button>
                    <button id="btn-create-acceptance-criteria" onclick="event.stopPropagation(); handleContextualCreate('acceptance-criteria');" style="display: none; background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 32px; min-height: 32px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Create Acceptance Criteria">
                        <img src="${addAcceptanceCriteriaIconPath}" style="width: 24px; height: 24px; object-fit: contain; display: block; flex-shrink: 0;" alt="Create Acceptance Criteria" />
                    </button>
                    <button id="btn-delete" onclick="event.stopPropagation(); handleDelete();" style="display: none; background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 32px; min-height: 32px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Delete (including children)">
                        <img src="${deleteIconPath}" style="width: 24px; height: 24px; object-fit: contain; display: block; flex-shrink: 0;" alt="Delete" />
                    </button>
                </div>
                
                </div>
                
                <!-- Right side: Submit button group -->
                <div id="btn-related-files-group" style="display: flex; align-items: center; gap: 2px; margin-left: auto;">
                    <button id="btn-submit" 
                            onclick="event.stopPropagation(); handleSubmit();" 
                            style="display: none; background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 32px; min-height: 32px;" 
                            onmouseover="this.style.opacity='0.7'" 
                            onmouseout="this.style.opacity='1'" 
                            title=""
                            data-shape-icon="${submitShapeIconPath}"
                            data-exploration-icon="${submitExploreIconPath}"
                            data-scenarios-icon="${submitScenarioIconPath}"
                            data-tests-icon="${submitTestIconPath}"
                            data-code-icon="${submitCodeIconPath}">
                        <img id="btn-submit-icon" src="${submitShapeIconPath}" style="width: 24px; height: 24px; object-fit: contain; display: block; flex-shrink: 0;" alt="Submit" />
                    </button>
                    <button id="btn-submit-alt" 
                            onclick="event.stopPropagation(); handleSubmitAlt();" 
                            style="display: none; background: transparent; border: none; padding: 4px; cursor: pointer; transition: opacity 0.15s ease; min-width: 32px; min-height: 32px;" 
                            onmouseover="this.style.opacity='0.7'" 
                            onmouseout="this.style.opacity='1'" 
                            title=""
                            data-shape-icon="${submitShapeIconPath}"
                            data-exploration-icon="${submitExploreIconPath}"
                            data-scenarios-icon="${submitScenarioIconPath}"
                            data-tests-icon="${submitTestIconPath}"
                            data-code-icon="${submitCodeIconPath}">
                        <img id="btn-submit-alt-icon" src="${submitScenarioIconPath}" style="width: 24px; height: 24px; object-fit: contain; display: block; flex-shrink: 0;" alt="Submit Alt" />
                    </button>
                </div>
            </div>
        `;
        
        
        // ===== PERFORMANCE: Content rendering =====
        const perfContentStart = performance.now();
        let contentHtml = '';
        let contentSummary = '';
        
        // Determine the actual view mode from the toggle (currentViewMode), not scope type
        const actualViewMode = this.currentViewMode || 'Hierarchy';
        const isFilesView = actualViewMode === 'Files';
        const isIncrementView = actualViewMode === 'Increment';
        Logger.log(`[StoryMapView] Rendering view mode: ${actualViewMode} (scopeType: ${scopeData.type})`);
        
        if (isIncrementView) {
            // Render increment columns view (read-only)
            contentHtml = this.renderIncrementView(botData, documentIconPath);
            const increments = botData?.scope?.content?.increments || botData?.increments || [];
            contentSummary = `${increments.length} increment${increments.length !== 1 ? 's' : ''}`;
            // Include epics section with increment's stories when scope is filtered to increment (injection level applies)
            const epics = (scopeData.type === 'increment' && scopeData.content?.epics) || [];
            if (epics.length > 0) {
                const treeHtml = this.renderStoryTree(epics, gearIconPath, epicIconPath, pageIconPath, testTubeIconPath, documentIconPath, plusIconPath, subtractIconPath, emptyIconPath);
                const rootNode = this.renderRootNode(treeHtml, plusIconPath, subtractIconPath);
                contentHtml += '<div style="margin-top: 12px; border-top: 1px solid var(--accent-color); padding-top: 8px;"><span style="font-size: 12px; font-weight: 600; opacity: 0.8;">Epics</span></div>' + rootNode;
            }
        } else if (isFilesView && scopeData.type === 'files' && scopeData.content) {
            // Files view - only when toggle is Files AND scope has file data
            contentHtml = this.renderFileList(scopeData.content);
            contentSummary = `${scopeData.content.length} file${scopeData.content.length !== 1 ? 's' : ''}`;
        } else if (!isFilesView && (scopeData.type === 'story' || scopeData.type === 'showAll') && scopeData.content) {
            // Hierarchy view - content is an object with 'epics' property
            const epics = scopeData.content.epics || [];
            
            const perfTreeStart = performance.now();
            const treeHtml = this.renderStoryTree(epics, gearIconPath, epicIconPath, pageIconPath, testTubeIconPath, documentIconPath, plusIconPath, subtractIconPath, emptyIconPath);
            const perfTreeEnd = performance.now();
            Logger.log(`[StoryMapView] [PERF] renderStoryTree (${epics.length} epics): ${(perfTreeEnd - perfTreeStart).toFixed(2)}ms`);
            
            const perfRootNodeStart = performance.now();
            const rootNode = this.renderRootNode(treeHtml, plusIconPath, subtractIconPath);
            const perfRootNodeEnd = performance.now();
            Logger.log(`[StoryMapView] [PERF] renderRootNode: ${(perfRootNodeEnd - perfRootNodeStart).toFixed(2)}ms`);
            
            contentHtml = actionButtonsHtml + rootNode;
            contentSummary = `${epics.length} epic${epics.length !== 1 ? 's' : ''}`;
        } else {
            contentHtml = '<div class="empty-state">All files in workspace</div>';
            contentSummary = 'all files';
        }
        const perfContentEnd = performance.now();
        Logger.log(`[StoryMapView] [PERF] Content rendering: ${(perfContentEnd - perfContentStart).toFixed(2)}ms`);
        
        const filterValue = escapeForHtml(scopeData.filter || '');
        const hasFilter = filterValue.length > 0;
        
        // ===== PERFORMANCE: Final HTML assembly =====
        const perfAssemblyStart = performance.now();        
        
        const scopeSectionExpanded = this.scopeSectionExpanded !== false;
        const injectLevels = [
            { level: 'stories', icon: injectStoriesIconPath, title: 'Include up to stories' },
            { level: 'domain_concepts', icon: injectDomainIconPath, title: 'Include up to domain concepts' },
            { level: 'acceptance', icon: injectCriteriaIconPath, title: 'Include up to acceptance criteria' },
            { level: 'scenarios', icon: injectScenariosIconPath, title: 'Include up to scenarios' },
            { level: 'examples', icon: injectExamplesIconPath, title: 'Include up to examples' },
            { level: 'tests', icon: injectTestsIconPath, title: 'Include up to tests' },
            { level: 'code', icon: injectCodeIconPath, title: 'Include up to code' }
        ];
        const currentInjectLevel = scopeData.includeLevel || 'examples';
        const currentInjectObj = injectLevels.find(l => l.level === currentInjectLevel) || injectLevels.find(l => l.level === 'examples');
        const injectExecToggleId = 'inject-level-exec-toggle';
        const injectCollapsedBtn = currentInjectObj && currentInjectObj.icon ? `<button class="execution-toggle-btn active execution-toggle-collapsed" data-action="toggleExecutionToggle" data-target="${injectExecToggleId}" title="${currentInjectObj.title}"><img src="${currentInjectObj.icon}" alt="${currentInjectObj.title}" style="width: 22px; height: 22px; object-fit: contain; display: block;" /></button>` : '';
        const levelToId = { stories: 'stories', domain_concepts: 'domain', acceptance: 'acceptance', scenarios: 'scenarios', examples: 'examples', tests: 'tests', code: 'code' };
        const injectExpandedButtons = injectLevels.map(l => {
            const isActive = currentInjectLevel === l.level;
            const imgStyle = l.icon ? `width: ${l.level === 'domain_concepts' ? '28' : '26'}px; height: ${l.level === 'domain_concepts' ? '28' : '26'}px; object-fit: contain; opacity: ${isActive ? '1' : '0.5'};` : '';
            const content = l.icon ? `<img src="${l.icon}" style="${imgStyle}" alt="${l.level}" />` : l.level;
            return `<button id="btn-include-${levelToId[l.level]}" onclick="event.stopPropagation(); switchIncludeLevel('${l.level}');" class="execution-toggle-btn${isActive ? ' active' : ''}" style="display: flex; align-items: center; justify-content: center; padding: 0 1px; line-height: 1; cursor: pointer; border: none; background: transparent; transition: opacity 0.15s ease; width: 28px; height: 28px;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="${l.title}">${content}</button>`;
        }).join('');
        const injectExpandedGroup = `<span class="execution-toggle-expanded" style="display: inline-flex; gap: 1px; align-items: center;" onclick="event.stopPropagation();">${injectExpandedButtons}${subtractIconPath ? `<button class="execution-toggle-collapse-btn" data-action="toggleExecutionToggle" data-target="${injectExecToggleId}" title="Collapse"><img src="${subtractIconPath}" style="width: 12px; height: 12px; object-fit: contain; display: block;" alt="Collapse" /></button>` : ''}</span>`;
        const injectToggleGroupHtml = `<span class="execution-toggle-container" id="${injectExecToggleId}" style="flex-shrink: 0;" onclick="event.stopPropagation();">${injectCollapsedBtn}${injectExpandedGroup}</span>`;
        const result = `
            <div class="section scope-section card-primary">
                <div class="collapsible-section ${scopeSectionExpanded ? 'expanded' : ''}">
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
                        <div style="display: flex; align-items: center; flex: 1;">
                            <span class="expand-icon" style="margin-right: 8px; font-size: 28px; transition: transform 0.15s;">▸</span>
                            ${scopeMapIconPath ? `<img src="${scopeMapIconPath}" style="margin-right: 8px; width: 28px; height: 28px; object-fit: contain;" alt="Scope" />` : ''}
                            <span style="font-weight: 600; font-size: 20px; color: var(--accent-color);">Scope</span>
                            <div style="flex: 1;"></div>
                        </div>
                    </div>
                    <div id="scope-content" class="collapsible-content" style="${isIncrementView ? `overflow: visible; display: ${scopeSectionExpanded ? 'block' : 'none'};` : `max-height: ${scopeSectionExpanded ? '2000px' : '0px'}; overflow: hidden; transition: max-height 0.3s ease; display: ${scopeSectionExpanded ? 'block' : 'none'};`}">
                        <div class="card-secondary" style="padding: 2px 4px;">
                            <div class="input-container" style="margin-bottom: 10px; padding: 6px 8px;">
                                <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap; min-height: 28px;">
                                    <div class="input-header" style="margin-bottom: 0; padding: 2px 6px 2px 0; border-bottom: none;">Filter</div>
                                    <div style="display: flex; gap: 4px; align-items: center;">
                                        <button 
                                            id="btn-view-hierarchy"
                                            onclick="event.stopPropagation(); switchViewMode('Hierarchy');" 
                                            style="
                                                display: flex;
                                                align-items: center;
                                                padding: 2px 6px;
                                                line-height: 1.2;
                                                cursor: pointer;
                                                font-size: 12px;
                                                color: ${actualViewMode === 'Hierarchy' ? 'var(--text-color, #fff)' : 'var(--text-color-faded)'};
                                                border: none;
                                                background: transparent;
                                                transition: all 0.15s ease;
                                            " 
                                            onmouseover="if('${actualViewMode}' !== 'Hierarchy') this.style.color='var(--text-color)'" 
                                            onmouseout="if('${actualViewMode}' !== 'Hierarchy') this.style.color='var(--text-color-faded)'"
                                            title="View story map hierarchy">
                                            hierarchy
                                        </button>
                                        <button 
                                            id="btn-view-increment"
                                            onclick="event.stopPropagation(); switchViewMode('Increment');" 
                                            style="
                                                display: flex;
                                                align-items: center;
                                                padding: 2px 6px;
                                                line-height: 1.2;
                                                cursor: pointer;
                                                font-size: 12px;
                                                color: ${actualViewMode === 'Increment' ? 'var(--text-color, #fff)' : 'var(--text-color-faded)'};
                                                border: none;
                                                background: transparent;
                                                transition: all 0.15s ease;
                                            " 
                                            onmouseover="if('${actualViewMode}' !== 'Increment') this.style.color='var(--text-color)'" 
                                            onmouseout="if('${actualViewMode}' !== 'Increment') this.style.color='var(--text-color-faded)'"
                                            title="View by increments">
                                            increments
                                        </button>
                                        <button 
                                            id="btn-view-files"
                                            onclick="event.stopPropagation(); switchViewMode('Files');" 
                                            style="
                                                display: flex;
                                                align-items: center;
                                                padding: 2px 6px;
                                                line-height: 1.2;
                                                cursor: pointer;
                                                font-size: 12px;
                                                color: ${actualViewMode === 'Files' ? 'var(--text-color, #fff)' : 'var(--text-color-faded)'};
                                                border: none;
                                                background: transparent;
                                                transition: all 0.15s ease;
                                            " 
                                            onmouseover="if('${actualViewMode}' !== 'Files') this.style.color='var(--text-color)'" 
                                            onmouseout="if('${actualViewMode}' !== 'Files') this.style.color='var(--text-color-faded)'"
                                            title="View file list">
                                            files
                                        </button>
                                    </div>
                                </div>
                                <div style="border-top: 1px solid var(--accent-color); padding-top: 6px; display: flex; align-items: center; gap: 4px;">
                                <input type="text" id="scopeFilterInput" style="padding: 4px 8px; flex: 1;"
                                    value="${filterValue}" 
                                    placeholder="Epic or Story name"
                                    onchange="console.log('[ScopeInput] onchange fired with:', this.value); updateFilter(this.value)"
                                    onkeydown="console.log('[ScopeInput] Key pressed:', event.key, 'Value:', this.value); if(event.key === 'Enter') { event.preventDefault(); console.log('[ScopeInput] Enter key - calling updateFilter'); updateFilter(this.value); }" />
                                <button id="btn-scope-to" onclick="event.stopPropagation(); handleScopeTo();" style="display: none; background: transparent; border: none; padding: 2px; cursor: pointer; transition: opacity 0.15s ease; min-width: 28px; min-height: 28px; flex-shrink: 0;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Scope to selected node">
                                    <img src="${scopeToIconPath}" style="width: 22px; height: 22px; object-fit: contain; display: block;" alt="Scope To" />
                                </button>
                                <button onclick="event.stopPropagation(); showAllScope();" style="background: transparent; border: none; padding: 2px; cursor: pointer; transition: opacity 0.15s ease; min-width: 28px; min-height: 28px; flex-shrink: 0;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Show all scope">
                                    <img src="${showAllIconPath}" style="width: 22px; height: 22px; object-fit: contain; display: block;" alt="Show All" />
                                </button>
                                <button onclick="event.stopPropagation(); clearScopeFilter();" style="background: transparent; border: none; padding: 2px; cursor: pointer; transition: opacity 0.15s ease; min-width: 28px; min-height: 28px; flex-shrink: 0;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'" title="Clear scope filter">
                                    <img src="${clearIconPath}" style="width: 22px; height: 22px; object-fit: contain; display: block;" alt="Clear Filter" />
                                </button>
                                </div>
                                <div class="include-level-controls" style="display: flex; flex-wrap: wrap; gap: 4px; align-items: center; min-height: 28px; border-top: 1px solid var(--accent-color); padding-top: 6px; margin-top: 6px;">
                                <span style="font-size: 12px; font-weight: 600; color: var(--text-color, #fff); flex-shrink: 0;">Inject</span>
                                ${injectToggleGroupHtml}
                                </div>
                            </div>
                            ${contentHtml}
                        </div>
                    </div>
                </div>
            </div>`;
        const perfAssemblyEnd = performance.now();
        Logger.log(`[StoryMapView] [PERF] HTML assembly: ${(perfAssemblyEnd - perfAssemblyStart).toFixed(2)}ms`);
        
        // ===== PERFORMANCE: Log total render time =====
        const perfRenderEnd = performance.now();
        const totalRenderTime = (perfRenderEnd - perfRenderStart).toFixed(2);
        Logger.log(`[StoryMapView] [PERF] TOTAL render() duration: ${totalRenderTime}ms`);
        
        return result;
    }
    
    /**
     * Render root "Story Map" node as collapsible container (like epics).
     * When collapsed, all epics are hidden; when expanded, epics are visible.
     * Story Map is the first row of the hierarchy (below the toolbar buttons).
     * Epics are indented one level under Story Map.
     * 
     * @param {string} treeHtml - HTML for epics tree (wrapped in collapsible div)
     * @param {string} plusIconPath - Icon for collapsed state (expand)
     * @param {string} subtractIconPath - Icon for expanded state (collapse)
     * @returns {string} HTML string
     */
    renderRootNode(treeHtml, plusIconPath, subtractIconPath) {
        const headerRow = `<div style="margin-top: 8px; margin-bottom: 4px; font-size: 12px; font-weight: 600; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center;">
                <span id="story-map-root-icon" onclick="event.stopPropagation(); toggleCollapse('story-map-root');" style="display: inline-block; min-width: 9px; cursor: pointer;" data-plus="${plusIconPath || ''}" data-subtract="${subtractIconPath || ''}"><img class="collapse-icon" src="${subtractIconPath || ''}" data-state="expanded" style="width: 9px; height: 9px; vertical-align: middle;" alt="Collapse" /></span>
                <span class="story-node" data-node-type="root" data-node-name="Story Map" style="display: inline-block; cursor: pointer; margin-left: 4px;" onclick="selectNode('root', null)">Story Map</span>
            </div>
            <div id="save-status-indicator" class="save-status" style="display: none;">
                <span id="save-status-spinner" class="save-spinner" style="display: inline-block; width: 16px; height: 16px; border: 2px solid rgba(255, 140, 0, 0.3); border-top-color: #ff8c00; border-radius: 50%;"></span>
                <span id="save-status-message" style="font-size: 12px; color: var(--text-color-faded); margin-left: 6px;"></span>
            </div>
        </div>`;
        const contentDiv = `<div id="story-map-root" class="collapsible-content" style="display: block; padding-left: 12px;">${treeHtml}</div>`;
        return headerRow + contentDiv;
    }
    
    /**
     * Render story tree (epics -> sub-epics -> stories -> scenarios).
     * 
     * @param {Array} epics - Epics array
     * @returns {string} HTML string
     */
    renderStoryTree(epics, gearIconPath, epicIconPath, pageIconPath, testTubeIconPath, documentIconPath, plusIconPath, subtractIconPath, emptyIconPath) {
        return epics.map((epic, epicIndex) => {
            const epicId = `epic-${epicIndex}`;
            const epicIcon = epicIconPath ? `<img src="${epicIconPath}" style="width: 14px; height: 14px; vertical-align: middle; margin-right: 4px;" alt="Epic" />` : '';
            
            // Find document and test links for epic (data attrs for toolbar File/Test buttons)
            const epicDocLink = epic.links && epic.links.find(l => l.icon === 'document');
            const epicTestLink = epic.links && epic.links.find(l => l.icon === 'test_tube');
            const epicTestFilesJson = epicTestLink ? this.escapeHtml(JSON.stringify([epicTestLink.url])) : '';
            
            // Check if epic has children
            const epicHasChildren = (epic.sub_epics && epic.sub_epics.length > 0) || (epic.story_groups && epic.story_groups.some(sg => sg.stories && sg.stories.length > 0));
            
            // Epic name: plain text, clickable to select, double-click to edit (File/Test via toolbar)
            const epicPath = escapeForHtml(`story_graph."${epic.name}"`);
            const epicBehavior = epic.behavior_needed || '';
            const epicNameHtml = `<span class="story-node" draggable="true" data-node-type="epic" data-node-name="${escapeForHtml(epic.name)}" data-behavior-needed="${epicBehavior}" data-has-children="${epicHasChildren}" data-position="${epicIndex}" data-path="${epicPath}"${epicDocLink ? ` data-file-link="${escapeForHtml(epicDocLink.url)}"` : ''}${epicTestFilesJson ? ` data-test-files="${epicTestFilesJson}"` : ''} style="cursor: pointer;">${escapeForHtml(epic.name)}</span>`;
            
            // Epic nodes - no inline links (File/Test via toolbar buttons)
            let html = `<div style="margin-top: 8px; font-size: 12px;"><span id="${epicId}-icon" onclick="event.stopPropagation(); toggleCollapse('${epicId}')" style="display: inline-block; min-width: 9px; cursor: pointer;" data-plus="${plusIconPath}" data-subtract="${subtractIconPath}"><img class="collapse-icon" src="${plusIconPath}" data-state="collapsed" style="width: 9px; height: 9px; vertical-align: middle;" alt="Expand" /></span> ${epicIcon}${epicNameHtml}</div>`;
            
            html += `<div id="${epicId}" class="collapsible-content" style="display: none;">`;
            // Helper function to recursively render a sub-epic (can be nested any number of levels)
            const renderSubEpic = (subEpic, subEpicIndex, parentPath, depth = 0, parentStoryGraphPath = null) => {
                const subEpicId = `${parentPath}-${subEpicIndex}`;
                const subEpicIcon = gearIconPath ? `<img src="${gearIconPath}" style="width: 14px; height: 14px; vertical-align: middle; margin-right: 4px;" alt="Sub-Epic" />` : '';
                
                // Find document and test links (data attrs for toolbar File/Test buttons)
                const subEpicDocLink = subEpic.links && subEpic.links.find(l => l.icon === 'document');
                const subEpicTestLink = subEpic.links && subEpic.links.find(l => l.icon === 'test_tube');
                const subEpicTestFiles = subEpic.test_files?.length > 0 ? subEpic.test_files : (subEpicTestLink ? [subEpicTestLink.url] : []);
                const subEpicTestFilesJson = subEpicTestFiles.length > 0 ? escapeForHtml(JSON.stringify(subEpicTestFiles)) : '';
                
                // Build the full path to this SubEpic
                // For first-level: story_graph."Epic"."SubEpic"
                // For nested: story_graph."Epic"."ParentSubEpic"."NestedSubEpic"
                // CRITICAL: Escape the ENTIRE path including quotes - HTML parser stops at unescaped quotes
                const baseStoryGraphPath = parentStoryGraphPath || `story_graph."${epic.name}"`;
                const subEpicPath = escapeForHtml(`${baseStoryGraphPath}."${subEpic.name}"`);
                
                // Determine which buttons to show for SubEpic based on children
                const nestedSubEpics = subEpic.sub_epics || [];
                const hasStories = subEpic.story_groups && subEpic.story_groups.some(sg => sg.stories && sg.stories.length > 0);
                const hasNestedSubEpics = nestedSubEpics.length > 0;
                const hasNoChildren = !hasStories && !hasNestedSubEpics;
                const subEpicHasChildren = hasStories || hasNestedSubEpics;
                
                // Sub-epic name: plain text, clickable to select (File/Test via toolbar)
                const subEpicBehavior = subEpic.behavior_needed || '';
                const subEpicBehaviors = subEpic.behaviors_needed ? JSON.stringify(subEpic.behaviors_needed) : `["${subEpicBehavior}"]`;
                const subEpicNameHtml = `<span class="story-node" draggable="true" data-node-type="sub-epic" data-node-name="${escapeForHtml(subEpic.name)}" data-behavior-needed="${subEpicBehavior}" data-behaviors-needed='${subEpicBehaviors}' data-has-children="${subEpicHasChildren}" data-has-stories="${hasStories}" data-has-nested-sub-epics="${hasNestedSubEpics}" data-position="${subEpicIndex}" data-path="${subEpicPath}"${subEpicDocLink ? ` data-file-link="${escapeForHtml(subEpicDocLink.url)}"` : ''}${subEpicTestFilesJson ? ` data-test-files="${subEpicTestFilesJson}"` : ''} style="cursor: pointer;">${escapeForHtml(subEpic.name)}</span>`;
                
                const marginLeft = 7 + (depth * 7);
                
                html += `<div style="margin-left: ${marginLeft}px; margin-top: 4px; font-size: 12px;"><span id="${subEpicId}-icon" onclick="event.stopPropagation(); toggleCollapse('${subEpicId}')" style="display: inline-block; min-width: 9px; cursor: pointer;" data-plus="${plusIconPath}" data-subtract="${subtractIconPath}"><img class="collapse-icon" src="${plusIconPath}" data-state="collapsed" style="width: 9px; height: 9px; vertical-align: middle;" alt="Expand" /></span> ${subEpicIcon}${subEpicNameHtml}</div>`;
                
                html += `<div id="${subEpicId}" class="collapsible-content" style="display: none;">`;
                
                // Render nested sub_epics if they exist (recursive)
                // Pass the current sub-epic's full path as the parent for nested children
                if (nestedSubEpics.length > 0) {
                    const currentSubEpicStoryGraphPath = `${baseStoryGraphPath}."${escapeForHtml(subEpic.name)}"`;
                    nestedSubEpics.forEach((nested, nestedIndex) => {
                        renderSubEpic(nested, nestedIndex, subEpicId, depth + 1, currentSubEpicStoryGraphPath);
                    });
                }
                
                // Render story_groups with stories if they exist
                if (subEpic.story_groups && subEpic.story_groups.length > 0) {
                    subEpic.story_groups.forEach(storyGroup => {
                        if (storyGroup.stories && storyGroup.stories.length > 0) {
                            storyGroup.stories.forEach((story, storyIndex) => {
                                const storyId = `${subEpicId}-story-${storyIndex}`;
                                const storyIcon = documentIconPath ? `<img src="${documentIconPath}" style="width: 14px; height: 14px; vertical-align: middle; margin-right: 4px;" alt="Story" />` : '';
                                
                                // Check if story has scenarios - if so, make it collapsible
                                const hasScenarios = story.scenarios && story.scenarios.length > 0;
                                
                                // Build story path for edit mode - use full parent chain for nested sub-epics
                                // CRITICAL: Escape the ENTIRE path including quotes - HTML parser stops at unescaped quotes
                                const storyPath = escapeForHtml(`${baseStoryGraphPath}."${subEpic.name}"."${story.name}"`);
                                
                                html += `<div style="margin-left: ${marginLeft + 7}px; margin-top: 2px; font-size: 12px;">`;
                                
                                if (hasScenarios) {
                                    // Collapsible story with scenarios - only icon is clickable
                                    html += `<span id="${storyId}-icon" onclick="event.stopPropagation(); toggleCollapse('${storyId}')" style="display: inline-block; min-width: 9px; cursor: pointer;" data-plus="${plusIconPath}" data-subtract="${subtractIconPath}"><img class="collapse-icon" src="${plusIconPath}" data-state="collapsed" style="width: 9px; height: 9px; vertical-align: middle;" alt="Expand" /></span> `;
                                } else {
                                    // Empty placeholder for alignment
                                    html += `<span style="display: inline-block; min-width: 9px;"><img src="${emptyIconPath}" style="width: 9px; height: 9px; vertical-align: middle;" alt="" /></span> `;
                                }
                                
                                // Find story doc and test links (data attrs for toolbar File/Test buttons)
                                const storyDocLink = story.links && story.links.find(l => l.text === 'story');
                                const storyTestLink = story.links && story.links.find(l => l.icon === 'test_tube');
                                const storyTestFiles = story.test_files?.length > 0 ? story.test_files : (storyTestLink ? [storyTestLink.url] : []);
                                const storyTestFilesJson = storyTestFiles.length > 0 ? escapeForHtml(JSON.stringify(storyTestFiles)) : '';
                                
                                // Story name: plain text, clickable to select (File/Test via toolbar)
                                const storyBehavior = story.behavior_needed || '';
                                const storyBehaviors = story.behaviors_needed ? JSON.stringify(story.behaviors_needed) : `["${storyBehavior}"]`;
                                html += `<span class="story-node" draggable="true" data-node-type="story" data-node-name="${escapeForHtml(story.name)}" data-behavior-needed="${storyBehavior}" data-behaviors-needed='${storyBehaviors}' data-has-children="${hasScenarios}" data-position="${storyIndex}" data-path="${storyPath}"${storyDocLink ? ` data-file-link="${escapeForHtml(storyDocLink.url)}"` : ''}${storyTestFilesJson ? ` data-test-files="${storyTestFilesJson}"` : ''} style="cursor: pointer;">${storyIcon}${escapeForHtml(story.name)}</span>`;
                                
                                // No inline action buttons (all actions are in the toolbar)
                                html += '</div>';
                                
                                // Render scenarios if they exist
                                if (hasScenarios) {
                                    html += `<div id="${storyId}" class="collapsible-content" style="display: none;">`;
                                    story.scenarios.forEach((scenario, scenarioIndex) => {
                                        html += `<div style="margin-left: ${marginLeft + 21}px; margin-top: 2px; font-size: 12px;">`;
                                        
                                        // Empty placeholder for alignment (scenarios don't have children)
                                        html += `<span style="display: inline-block; min-width: 9px;"><img src="${emptyIconPath}" style="width: 9px; height: 9px; vertical-align: middle;" alt="" /></span> `;
                                        
                                        // Create scenario anchor ID from scenario name (matches synchronizer format)
                                        const scenarioAnchor = this.createScenarioAnchor(scenario.name);
                                        // CRITICAL: Escape the ENTIRE path including quotes - HTML parser stops at unescaped quotes
                                        const scenarioPath = escapeForHtml(`${baseStoryGraphPath}."${escapeForHtml(subEpic.name)}"."${escapeForHtml(story.name)}"."${escapeForHtml(scenario.name)}"`);
                                        
                                        // Scenario: plain text, clickable to select (File/Test via toolbar)
                                        const scenarioBehavior = scenario.behavior_needed || '';
                                        const scenarioLink = storyDocLink ? `${storyDocLink.url}#${scenarioAnchor}` : '';
                                        const scenarioTestFiles = scenario.test_files?.length > 0 ? scenario.test_files : (scenario.test_file ? [scenario.test_file] : []);
                                        const scenarioTestFilesJson = scenarioTestFiles.length > 0 ? escapeForHtml(JSON.stringify(scenarioTestFiles)) : '';
                                        html += `<span class="story-node" draggable="true" data-node-type="scenario" data-node-name="${escapeForHtml(scenario.name)}" data-behavior-needed="${scenarioBehavior}" data-has-children="false" data-position="${scenarioIndex}" data-path="${scenarioPath}"${scenarioLink ? ` data-file-link="${escapeForHtml(scenarioLink)}"` : ''}${scenarioTestFilesJson ? ` data-test-files="${scenarioTestFilesJson}"` : ''} style="cursor: pointer;">${escapeForHtml(scenario.name)}</span>`;
                                        
                                        html += '</div>';
                                    });
                                    html += '</div>'; // Close scenario collapsible-content
                                }
                            });
                        }
                    });
                }
                
                html += '</div>'; // Close sub-epic collapsible-content
            };
            
            // Render sub-epics under this epic
            const subEpics = epic.sub_epics || [];
            subEpics.forEach((subEpic, subEpicIndex) => {
                renderSubEpic(subEpic, subEpicIndex, `epic-${epicIndex}`, 0);
            });
            html += '</div>'; // Close epic collapsible-content
            
            return html;
        }).join('');
    }
    
    /**
     * Render increment view as columns.
     * 
     * @param {Object} botData - Bot data containing increments
     * @param {string} documentIconPath - Path to document icon for stories
     * @returns {string} HTML string for increment columns
     */
    renderIncrementView(botData, documentIconPath) {
        // Always use the full increments list regardless of scope filter
        const allIncrements = botData?.scope?.content?.increments || botData?.increments || [];

        // Filter is applied client-side to increment columns only, not via the scope system
        const filterText = (botData?.scope?.filter || '').toLowerCase().trim();

        // Build the display list: filter matches increment name → full column;
        //   filter matches story name → show that increment with only matching stories
        const displayIncrements = filterText
            ? allIncrements.map(inc => {
                if (inc.name.toLowerCase().includes(filterText)) return inc; // full column
                const matching = (inc.stories || []).filter(s =>
                    (typeof s === 'string' ? s : s.name).toLowerCase().includes(filterText)
                );
                return matching.length ? { ...inc, stories: matching } : null;
            }).filter(Boolean)
            : allIncrements;

        // Unallocated: only shown when no filter is active (filter affects increment columns, not unallocated)
        const assignedStories = new Set(
            allIncrements.flatMap(inc => (inc.stories || []).map(s => typeof s === 'string' ? s : s.name))
        );
        const unallocatedStories = filterText
            ? []
            : this._collectAllStoryNames(botData).filter(name => !assignedStories.has(name));

        const storyIcon = documentIconPath
            ? `<img src="${documentIconPath}" style="width: 14px; height: 14px; vertical-align: middle; margin-right: 4px; flex-shrink: 0;" alt="Story" />`
            : '';

        const filterHint = filterText
            ? `<span style="font-size: 11px; color: var(--accent-color); margin-left: 8px;">filter: "${escapeForHtml(filterText)}" — ${displayIncrements.length} of ${allIncrements.length} increments</span>`
            : '';

        let html = `
            <div style="padding: 8px 12px 4px; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid var(--text-color-faded, #444);">
                <span style="font-size: 12px; font-weight: 600; opacity: 0.7;">INCREMENTS</span>
                ${filterHint}
                <button onclick="addIncrement()" style="font-size: 11px; padding: 2px 8px; cursor: pointer; background: var(--accent-color); color: #fff; border: none; border-radius: 3px; margin-left: auto;">+ Add Increment</button>
            </div>
            <div class="increment-columns-wrapper" style="display: flex; gap: 0; overflow-x: auto; height: 65vh; min-height: 300px;">
        `;

        if (!filterText && (unallocatedStories.length > 0 || allIncrements.length === 0)) {
            html += `
                <div class="unallocated-column" style="min-width: 140px; max-width: 160px; flex-shrink: 0; background: rgba(255,255,255,0.03); border-right: 1px solid var(--text-color-faded, #444); padding: 8px; overflow-y: auto;">
                    <div style="font-size: 11px; font-weight: 600; opacity: 0.6; margin-bottom: 6px; text-transform: uppercase;">Unallocated</div>
                    ${unallocatedStories.length === 0
                        ? `<div style="font-size: 11px; color: var(--text-color-faded); font-style: italic;">(none)</div>`
                        : unallocatedStories.map(name => {
                            const esc = escapeForHtml(name);
                            return `<div class="story-node" draggable="true" data-node-type="story" data-node-name="${esc}" data-path="story_graph.unallocated.${esc}" data-inc-source="" data-position="0" style="display: flex; align-items: flex-start; font-size: 12px; margin-bottom: 4px; gap: 2px; cursor: grab;">
                                ${storyIcon}<span style="flex: 1; word-wrap: break-word; pointer-events: none;">${esc}</span>
                            </div>`;
                        }).join('')
                    }
                    ${allIncrements.length === 0 ? `<div style="margin-top: 12px; font-size: 11px; color: var(--text-color-faded); font-style: italic;">Add an increment to start assigning stories.</div>` : ''}
                </div>
            `;
        }

        for (const increment of displayIncrements) {
            const incName = increment.name;
            const escapedName = escapeForHtml(incName);
            const jsName = incName.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/'/g, "\\'");
            const stories = increment.stories || [];
            const sortedStories = [...stories].sort((a, b) =>
                (a.sequential_order || 0) - (b.sequential_order || 0)
            );
            const behaviorNeeded = increment.behavior_needed || 'shape';

            html += `
                <div class="increment-column-container" data-inc="${escapedName}" data-behavior-needed="${escapeForHtml(behaviorNeeded)}" data-collapsed="false" onclick="event.stopPropagation(); selectIncrement(this.getAttribute('data-inc'), this.getAttribute('data-behavior-needed'));" style="min-width: 160px; max-width: 200px; flex-shrink: 0; border-right: 1px solid var(--text-color-faded, #444); padding: 8px; display: flex; flex-direction: column; overflow-y: auto; cursor: pointer; transition: min-width 0.2s, max-width 0.2s;">
                    <div style="display: flex; align-items: center; gap: 4px; margin-bottom: 8px; padding-bottom: 6px; border-bottom: 1px solid var(--text-color-faded, #555);">
                        <button onclick="event.stopPropagation(); toggleIncrementCollapse(this.closest('.increment-column-container'))" style="font-size: 9px; padding: 1px 4px; cursor: pointer; background: transparent; color: var(--text-color-faded); border: none; flex-shrink: 0; line-height: 1;" title="Collapse / expand">▼</button>
                        <span class="increment-drag-handle" draggable="true" data-inc="${escapedName}" style="cursor: grab; font-size: 11px; color: var(--text-color-faded); flex-shrink: 0; padding: 0 2px; user-select: none;" title="Drag to reorder">⠿</span>
                        <span
                            contenteditable="true"
                            data-increment-name="${escapedName}"
                            onclick="event.stopPropagation();"
                            onblur="renameIncrement(this, this.getAttribute('data-increment-name'))"
                            onkeydown="if(event.key==='Enter'){event.preventDefault();this.blur();} if(event.key==='Escape'){this.innerText=this.getAttribute('data-increment-name');this.blur();}"
                            style="flex: 1; font-weight: 600; font-size: 12px; word-wrap: break-word; outline: none; cursor: text; min-width: 0;"
                            title="Click to rename"
                        >${escapedName}</span>
                        <button data-inc="${escapedName}" onclick="event.stopPropagation(); deleteIncrement(this.getAttribute('data-inc'))" style="font-size: 10px; padding: 1px 5px; cursor: pointer; background: transparent; color: var(--text-color-faded); border: 1px solid var(--text-color-faded); border-radius: 3px; flex-shrink: 0;" title="Delete increment">x</button>
                    </div>
                    <div class="increment-stories-body" style="display: flex; flex-direction: column; gap: 4px; flex: 1;">
                        ${sortedStories.length === 0
                            ? `<div style="font-size: 11px; color: var(--text-color-faded); font-style: italic;">(no stories)</div>`
                            : sortedStories.map((story, si) => {
                                const storyName = typeof story === 'string' ? story : (story.name || '');
                                const escapedStoryName = escapeForHtml(storyName);
                                return `
                                    <div class="story-node" draggable="true" data-node-type="story" data-node-name="${escapedStoryName}" data-path="story_graph.increments.${escapedName}.${escapedStoryName}" data-inc-source="${escapedName}" data-position="${si}" style="display: flex; align-items: flex-start; font-size: 12px; gap: 2px; cursor: grab;">
                                        ${storyIcon}
                                        <span style="flex: 1; word-wrap: break-word; min-width: 0; pointer-events: none;">${escapedStoryName}</span>
                                        <button data-inc="${escapedName}" data-story="${escapedStoryName}" onclick="event.stopPropagation(); removeStoryFromIncrement(this.getAttribute('data-inc'), this.getAttribute('data-story'))" style="font-size: 9px; padding: 0 3px; cursor: pointer; background: transparent; color: var(--text-color-faded); border: none; flex-shrink: 0; opacity: 0.5; line-height: 1; pointer-events: auto;" title="Remove story from increment">x</button>
                                    </div>`;
                            }).join('')
                        }
                    </div>
                </div>
            `;
        }

        html += '</div>';
        return html;
    }

    _collectAllStoryNames(botData) {
        const names = [];
        const epics = botData?.scope?.content?.epics || botData?.epics || [];
        const walk = (nodes) => {
            for (const node of nodes || []) {
                if (node.name && node.story_type) {
                    names.push(node.name);
                }
                walk(node.sub_epics);
                for (const sg of node.story_groups || []) {
                    for (const s of sg.stories || []) {
                        if (s.name) names.push(s.name);
                    }
                }
            }
        };
        walk(epics);
        return [...new Set(names)];
    }
    
    /**
     * Render file list.
     * 
     * @param {Array} files - Files array
     * @returns {string} HTML string
     */
    renderFileList(files) {
        return '<div style="margin-top: 5px;">' + files.map(file => 
            `<div style="margin-left: 5px; font-family: monospace; font-size: 12px; margin-top: 2px;">- ${escapeForHtml(file.path)}</div>`
        ).join('') + '</div>';
    }
    
    
    /**
     * Handle events.
     * 
     * @param {string} eventType - Event type
     * @param {Object} eventData - Event data
     * @returns {Promise<Object>} Result
     */
    async handleEvent(eventType, eventData) {
        if (eventType === 'updateFilter') {
            const filterValue = eventData.filter || '';
            // Execute scope command with filter value
            const command = filterValue ? `scope "${filterValue}"` : 'scope';
            const result = await this.execute(command);
            return result;
        }
        throw new Error(`Unknown event type: ${eventType}`);
    }
}

function getNonce() {
	let text = '';
	const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
	for (let i = 0; i < 32; i++) {
		text += possible.charAt(Math.floor(Math.random() * possible.length));
	}
	return text;
}

module.exports = StoryMapView;