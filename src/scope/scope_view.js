/**
 * ScopeSection - Renders scope section with filter and story tree or file list.
 * 
 * Epic: Invoke Bot Through Panel
 * Sub-Epic: Manage Scope Through Panel
 * Story: Display Story Scope Hierarchy, Filter Story Scope
 */

const PanelView = require('../panel/panel_view');

class ScopeSection extends PanelView {
    /**
     * Scope section view.
     * 
     * @param {Object} webview - VS Code webview instance (optional)
     * @param {Object} extensionUri - Extension URI (optional)
     */
    constructor(webview, extensionUri) {
        super();
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
     * Escape for JavaScript string.
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
     * Render scope section HTML.
     * 
     * @returns {string} HTML string
     */
    async render() {
        const botData = await this.execute('status');
        const scopeData = botData.scope || { type: 'all', filter: '', content: null, graphLinks: [] };
        const vscode = require('vscode');
        
        // Get the proper webview URIs for icons
        let magnifyingGlassIconPath = '';
        let clearIconPath = '';
        let plusIconPath = '';
        let subtractIconPath = '';
        let gearIconPath = '';
        let epicIconPath = '';
        let pageIconPath = '';
        let testTubeIconPath = '';
        if (this.webview && this.extensionUri) {
            try {
                const magnifyingGlassUri = vscode.Uri.joinPath(this.extensionUri, 'img', 'magnifying_glass.png');
                magnifyingGlassIconPath = this.webview.asWebviewUri(magnifyingGlassUri).toString();
                
                // clear.png doesn't exist - skip it
                clearIconPath = '';
                
                const plusUri = vscode.Uri.joinPath(this.extensionUri, 'img', 'plus.png');
                plusIconPath = this.webview.asWebviewUri(plusUri).toString();
                
                const subtractUri = vscode.Uri.joinPath(this.extensionUri, 'img', 'subtract.png');
                subtractIconPath = this.webview.asWebviewUri(subtractUri).toString();
                
                const gearUri = vscode.Uri.joinPath(this.extensionUri, 'img', 'gear.png');
                gearIconPath = this.webview.asWebviewUri(gearUri).toString();
                
                const epicUri = vscode.Uri.joinPath(this.extensionUri, 'img', 'light_bulb2.png');
                epicIconPath = this.webview.asWebviewUri(epicUri).toString();
                
                const pageUri = vscode.Uri.joinPath(this.extensionUri, 'img', 'page.png');
                pageIconPath = this.webview.asWebviewUri(pageUri).toString();
                
                // test_tube.png doesn't exist - skip it
                testTubeIconPath = '';
            } catch (err) {
                console.error('Failed to create icon URIs:', err);
            }
        }
        
        const linksHtml = scopeData.graphLinks && scopeData.graphLinks.length > 0
            ? scopeData.graphLinks.map(link => 
                `<a href="javascript:void(0)" onclick="openFile('${this.escapeForJs(link.url)}')" style="color: var(--vscode-foreground); text-decoration: none; margin-left: 6px; font-size: 12px;">${this.escapeHtml(link.text).toLowerCase()}</a>`
            ).join('')
            : '';
        
        let contentHtml = '';
        let contentSummary = '';
        if ((scopeData.type === 'story' || scopeData.type === 'showAll') && scopeData.content) {
            contentHtml = this.renderStoryTree(scopeData.content, gearIconPath, epicIconPath, pageIconPath, testTubeIconPath);
            contentSummary = `${scopeData.content.length} epic${scopeData.content.length !== 1 ? 's' : ''}`;
        } else if (scopeData.type === 'files' && scopeData.content) {
            contentHtml = this.renderFileList(scopeData.content);
            contentSummary = `${scopeData.content.length} file${scopeData.content.length !== 1 ? 's' : ''}`;
        } else {
            contentHtml = '<div class="empty-state">All files in workspace</div>';
            contentSummary = 'all files';
        }
        
        const filterValue = this.escapeHtml(scopeData.filter || '');
        const hasFilter = filterValue.length > 0;
        
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
                    ${magnifyingGlassIconPath ? `<img src="${magnifyingGlassIconPath}" style="margin-right: 8px; width: 28px; height: 28px; object-fit: contain;" alt="Scope Icon" />` : ''}
                    <span style="font-weight: 600; font-size: 20px;">Scope</span>
                    <button onclick="event.stopPropagation(); clearScopeFilter();" style="
                        background: transparent;
                        border: none;
                        padding: 4px 8px;
                        margin-left: 6px;
                        cursor: pointer;
                        display: flex;
                        align-items: center;
                        transition: opacity 0.15s ease;
                        font-size: 12px;
                    " 
                    onmouseover="this.style.opacity='0.7'" 
                    onmouseout="this.style.opacity='1'"
                    title="Clear scope filter (show all)">
                        Show All
                    </button>
                </div>
                ${linksHtml ? `<div onclick="event.stopPropagation();" style="display: flex; align-items: center;">${linksHtml}</div>` : ''}
            </div>
            <div id="scope-content" class="collapsible-content" style="max-height: 2000px; overflow: hidden; transition: max-height 0.3s ease;">
                <div class="card-secondary" style="padding: 5px;">
                    <div class="input-container" style="margin-bottom: 6px;">
                        <div class="input-header">Filter</div>
                        <input type="text" id="scopeFilterInput" 
                               value="${filterValue}" 
                               placeholder="Epic or Story name"
                               onchange="updateFilter(this.value)"
                               onkeydown="if(event.key === 'Enter') { event.preventDefault(); updateFilter(this.value); }" />
                    </div>
                    ${contentHtml}
                </div>
            </div>
        </div>
    </div>`;
    }
    
    /**
     * Render story tree (epics -> features -> stories -> scenarios).
     * 
     * @param {Array} epics - Epics array
     * @returns {string} HTML string
     */
    renderStoryTree(epics, gearIconPath, epicIconPath, pageIconPath, testTubeIconPath) {
        return epics.map((epic, epicIndex) => {
            const epicId = `epic-${epicIndex}`;
            const epicIcon = epicIconPath ? `<img src="${epicIconPath}" style="width: 14px; height: 14px; vertical-align: middle; margin-right: 4px;" alt="Epic" />` : '';
            let html = `<div style="margin-top: 8px; font-size: 12px;">
        <span class="collapsible-header" onclick="toggleCollapse('${epicId}')" style="cursor: pointer; user-select: none;">
          <span id="${epicId}-icon" style="display: inline-block; min-width: 9px;"><img class="collapse-icon" src="" data-state="collapsed" style="width: 9px; height: 9px; vertical-align: middle;" alt="Expand" /></span> ${epicIcon}${this.escapeHtml(epic.name)}
        </span>
      </div>`;
            
            html += `<div id="${epicId}" class="collapsible-content" style="display: none;">`;
            // Helper function to recursively render a feature (can have nested features)
            const renderFeature = (feature, featureIndex, parentPath, depth = 0) => {
                const featureId = `${parentPath}-${featureIndex}`;
                const featureIcon = gearIconPath ? `<img src="${gearIconPath}" style="width: 14px; height: 14px; vertical-align: middle; margin-right: 4px;" alt="Feature" />` : '';
                const featureLinks = (feature.links && feature.links.length > 0) 
                    ? ' ' + feature.links.map(link => 
                        `<a href="javascript:void(0)" onclick="event.stopPropagation(); openFile('${this.escapeForJs(link.url)}')">[${this.escapeHtml(link.text)}]</a>`
                    ).join(' ')
                    : '';
                
                const marginLeft = 7 + (depth * 7); // Increase margin for nested features
                
                html += `<div style="margin-left: ${marginLeft}px; margin-top: 4px; font-size: 12px;"><span class="collapsible-header" onclick="toggleCollapse('${featureId}')" style="cursor: pointer; user-select: none;"><span id="${featureId}-icon" style="display: inline-block; min-width: 9px;"><img class="collapse-icon" src="" data-state="collapsed" style="width: 9px; height: 9px; vertical-align: middle;" alt="Expand" /></span> ${featureIcon}${this.escapeHtml(feature.name)}${featureLinks}</span></div>`;
                
                html += `<div id="${featureId}" class="collapsible-content" style="display: none;">`;
                
                // Render nested features (sub_epics) if they exist
                const nestedFeatures = feature.sub_epics || feature.features || [];
                if (nestedFeatures.length > 0) {
                    nestedFeatures.forEach((nestedFeature, nestedIndex) => {
                        renderFeature(nestedFeature, nestedIndex, featureId, depth + 1);
                    });
                }
                
                // Render stories if they exist (may be in story_groups or directly in stories)
                let stories = feature.stories || [];
                if (!stories.length && feature.story_groups) {
                    // Flatten story_groups into stories array
                    stories = feature.story_groups.flatMap(group => group.stories || []);
                }
                if (stories.length > 0) {
                    stories.forEach((story, storyIndex) => {
                        const storyId = `${featureId}-story-${storyIndex}`;
                        const storyIcon = pageIconPath ? `<img src="${pageIconPath}" style="width: 14px; height: 14px; vertical-align: middle; margin-right: 4px;" alt="Story" />` : '';
                        
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
                                const testTubeIcon = testTubeIconPath ? `<img src="${testTubeIconPath}" style="width: 14px; height: 14px; vertical-align: middle; margin-right: 4px;" alt="Scenario" />` : '';
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
            
            // Use sub_epics instead of features (actual JSON structure)
            const subEpics = epic.sub_epics || epic.features || [];
            subEpics.forEach((feature, featureIndex) => {
                renderFeature(feature, featureIndex, `epic-${epicIndex}`, 0);
            });
            html += '</div>'; // Close epic collapsible-content
            
            return html;
        }).join('');
    }
    
    /**
     * Render file list.
     * 
     * @param {Array} files - Files array
     * @returns {string} HTML string
     */
    renderFileList(files) {
        return '<div style="margin-top: 5px;">' + files.map(file => 
            `<div style="margin-left: 5px; font-family: monospace; font-size: 12px; margin-top: 2px;">- ${this.escapeHtml(file.path)}</div>`
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
            // Update filter logic would go here
            return { success: true, filter: eventData.filter };
        }
        throw new Error(`Unknown event type: ${eventType}`);
    }
}

module.exports = ScopeSection;
