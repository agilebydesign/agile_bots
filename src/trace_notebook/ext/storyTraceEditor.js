// @ts-check
const vscode = require('vscode');
const path = require('path');
const fs = require('fs');

/**
 * Custom editor for .strace files
 * Shows collapsible sections like git diff view
 */
class StoryTraceEditorProvider {
    static viewType = 'storyTrace.editor';

    constructor(context) {
        this.context = context;
    }

    /**
     * Called when a .strace file is opened
     */
    async resolveCustomTextEditor(document, webviewPanel, _token) {
        webviewPanel.webview.options = {
            enableScripts: true
        };

        // Load trace data from file
        const traceData = JSON.parse(document.getText());
        
        // Render the webview
        webviewPanel.webview.html = this.getHtmlForWebview(webviewPanel.webview, traceData);

        // Handle messages from webview
        webviewPanel.webview.onDidReceiveMessage(async message => {
            switch (message.command) {
                case 'openFile':
                    this.openFile(message.file, message.line);
                    break;
                case 'loadCode':
                    // Lazy load code for a section
                    console.log('Extension received loadCode:', message);
                    const code = await this.loadCodeForSection(message.file, message.line, message.symbol);
                    console.log('Sending codeLoaded for id:', message.id);
                    webviewPanel.webview.postMessage({
                        command: 'codeLoaded',
                        id: message.id,
                        code: code
                    });
                    break;
                case 'saveCode':
                    // Save edited code back to source file
                    console.log('Extension received saveCode:', message.file, 'line:', message.line);
                    try {
                        await this.saveCodeToFile(message.file, message.line, message.originalCode, message.newCode);
                        webviewPanel.webview.postMessage({
                            command: 'codeSaved',
                            file: message.file
                        });
                        vscode.window.showInformationMessage(`Saved changes to ${message.file}`);
                    } catch (e) {
                        webviewPanel.webview.postMessage({
                            command: 'saveError',
                            error: e.message
                        });
                        vscode.window.showErrorMessage(`Failed to save: ${e.message}`);
                    }
                    break;
                case 'saveScenario':
                    // Save scenario steps to story-graph.json
                    console.log('Extension received saveScenario:', message.scenarioName);
                    try {
                        await this.saveScenarioToStoryGraph(message.file, message.scenarioName, message.newSteps);
                        webviewPanel.webview.postMessage({
                            command: 'scenarioSaved',
                            scenarioName: message.scenarioName
                        });
                        vscode.window.showInformationMessage(`Saved scenario: ${message.scenarioName}`);
                    } catch (e) {
                        webviewPanel.webview.postMessage({
                            command: 'saveError',
                            error: e.message
                        });
                        vscode.window.showErrorMessage(`Failed to save scenario: ${e.message}`);
                    }
                    break;
            }
        });

        // Update webview when document changes
        const changeDocumentSubscription = vscode.workspace.onDidChangeTextDocument(e => {
            if (e.document.uri.toString() === document.uri.toString()) {
                const newData = JSON.parse(document.getText());
                webviewPanel.webview.html = this.getHtmlForWebview(webviewPanel.webview, newData);
            }
        });

        webviewPanel.onDidDispose(() => {
            changeDocumentSubscription.dispose();
        });
    }

    /**
     * Save edited code back to the source file
     */
    async saveCodeToFile(filePath, startLine, originalCode, newCode) {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot) throw new Error('No workspace found');

        const fullPath = path.join(workspaceRoot, filePath);
        
        // Read the current file
        const content = fs.readFileSync(fullPath, 'utf-8');
        
        // Find and replace the original code with new code
        // This is a simple approach - find the original snippet and replace it
        if (content.includes(originalCode)) {
            const newContent = content.replace(originalCode, newCode);
            fs.writeFileSync(fullPath, newContent, 'utf-8');
            console.log('Saved changes to:', fullPath);
        } else {
            // Fallback: try to replace based on line number
            const lines = content.split('\n');
            const originalLines = originalCode.split('\n');
            const newLines = newCode.split('\n');
            
            // Replace lines starting from startLine
            const lineIdx = startLine - 1;
            lines.splice(lineIdx, originalLines.length, ...newLines);
            
            fs.writeFileSync(fullPath, lines.join('\n'), 'utf-8');
            console.log('Saved changes by line to:', fullPath);
        }
    }

    /**
     * Save scenario steps to story-graph.json
     */
    async saveScenarioToStoryGraph(storyGraphPath, scenarioName, newSteps) {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot) throw new Error('No workspace found');

        const fullPath = path.join(workspaceRoot, storyGraphPath);
        
        // Read and parse the story graph
        const content = fs.readFileSync(fullPath, 'utf-8');
        const storyGraph = JSON.parse(content);
        
        // Find and update the scenario
        let found = false;
        const findAndUpdateScenario = (obj) => {
            if (found) return;
            if (Array.isArray(obj)) {
                for (const item of obj) {
                    findAndUpdateScenario(item);
                }
            } else if (obj && typeof obj === 'object') {
                // Check if this is the scenario we're looking for
                if (obj.name === scenarioName && 'steps' in obj) {
                    obj.steps = newSteps;
                    found = true;
                    return;
                }
                // Recurse into all properties
                for (const key of Object.keys(obj)) {
                    findAndUpdateScenario(obj[key]);
                }
            }
        };
        
        findAndUpdateScenario(storyGraph);
        
        if (!found) {
            throw new Error(`Scenario "${scenarioName}" not found in ${storyGraphPath}`);
        }
        
        // Write back with nice formatting
        fs.writeFileSync(fullPath, JSON.stringify(storyGraph, null, 2), 'utf-8');
        console.log('Saved scenario to:', fullPath);
    }

    /**
     * Lazy load code for a section by reading the file
     */
    async loadCodeForSection(filePath, line, symbol) {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot) return '// Could not find workspace';

        // Handle stdlib references
        if (filePath.includes('(stdlib)')) {
            return `// ${symbol}\n// Standard library - code not available`;
        }

        const fullPath = path.join(workspaceRoot, filePath);
        try {
            const content = fs.readFileSync(fullPath, 'utf-8');
            const lines = content.split('\n');
            
            // Extract ~30 lines starting from the given line
            const startLine = Math.max(0, (line || 1) - 1);
            const endLine = Math.min(lines.length, startLine + 30);
            const snippet = lines.slice(startLine, endLine).join('\n');
            
            return snippet || '// No code found';
        } catch (e) {
            return `// Could not load: ${filePath}`;
        }
    }

    /**
     * Open a source file at a specific line
     */
    async openFile(filePath, line) {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot) return;

        const fullPath = path.join(workspaceRoot, filePath);
        try {
            const doc = await vscode.workspace.openTextDocument(fullPath);
            const editor = await vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
            if (line) {
                const position = new vscode.Position(line - 1, 0);
                editor.selection = new vscode.Selection(position, position);
                editor.revealRange(new vscode.Range(position, position), vscode.TextEditorRevealType.InCenter);
            }
        } catch (e) {
            vscode.window.showErrorMessage(`Could not open: ${filePath}`);
        }
    }

    /**
     * Generate HTML for the webview with nested sections
     * Supports both story-level format (story + scenarios array) and 
     * single-scenario format (scenario + test + code)
     */
    getHtmlForWebview(webview, data) {
        // Detect format: story-level or single-scenario
        const isStoryFormat = data.story && data.scenarios;
        
        // Get image URIs for buttons
        const imgFolder = vscode.Uri.joinPath(this.context.extensionUri, 'img');
        const toggleCodeImg = webview.asWebviewUri(vscode.Uri.joinPath(imgFolder, 'toggle_code.png'));
        const expandAllImg = webview.asWebviewUri(vscode.Uri.joinPath(imgFolder, 'expand_all.png'));
        const expandCodeImg = webview.asWebviewUri(vscode.Uri.joinPath(imgFolder, 'expand_code.png'));
        
        // Extract data based on format
        const story = data.story || {};
        const scenarios = data.scenarios || [];
        // For old format compatibility
        const scenario = data.scenario || {};
        const test = data.test || {};
        const code = data.code || [];

        // Recursive function to render nested code sections
        // L1-3: code shown inline
        // L4+: lazy loaded on demand (marked with lazy: true in JSON)
        const renderCodeSection = (c, index, parentId = '') => {
            const id = parentId ? `${parentId}-${index}` : `code-${index}`;
            const depth = c.depth || 1;
            const isLazy = c.lazy === true;  // True lazy loading - code not in JSON
            const hasChildren = c.children && c.children.length > 0;
            const indent = (depth - 1) * 20;
            
            // Render children (always render structure for navigation)
            let childrenHtml = '';
            if (hasChildren) {
                childrenHtml = `<div class="children-container">${c.children.map((child, i) => renderCodeSection(child, i, id)).join('')}</div>`;
            }
            
            // Build code content based on whether it's lazy-loaded or not
            let codeContent;
            const fileAttr = escapeHtml(c.file || '');
            const lineAttr = c.line || 1;
            const symbolAttr = escapeHtml(c.symbol || '');
            const isEditable = c.file && !c.file.includes('(stdlib)');
            const fileTip = c.file ? `${escapeHtml(c.file)}:${c.line || 1}` : '';
            
            if (isLazy) {
                // Lazy: show "Load code" button, code will be fetched on demand
                codeContent = `<div class="lazy-code code-block collapsed" id="${id}-code" data-file="${fileAttr}" data-line="${lineAttr}" data-symbol="${symbolAttr}" data-id="${id}">
                     <button class="load-code-btn" onclick="event.stopPropagation(); requestCodeFromBtn(this)">
                       ▶ Load code
                     </button>
                     <div class="monaco-container" style="display:none; height: 200px;" data-file="${fileAttr}" data-line="${lineAttr}" data-editable="${isEditable}"></div>
                     <div class="loading-indicator" style="display:none;">Loading...</div>
                   </div>`;
            } else {
                // Not lazy: code is already in JSON - wrap in collapsible code-block (starts hidden)
                const codeB64 = Buffer.from(c.code || '// No code').toString('base64');
                codeContent = `<div class="code-block collapsed" id="${id}-code">
                    <div class="monaco-container" style="display:none; height: 200px;" data-file="${fileAttr}" data-line="${lineAttr}" data-editable="${isEditable}" data-code="${codeB64}"></div>
                </div>`;
            }
            
            // All sections start collapsed
            const startCollapsed = 'collapsed';
            
            // Order: toggle_code, expand_all (hierarchy), expand_code (hierarchy + code)
            // All buttons are toggles - collapse if expanded, expand if collapsed
            // For lazy items, the toggle button triggers loading first, then shows code
            const toggleCodeBtn = `<button class="icon-btn toggle-code-btn" onclick="event.stopPropagation(); toggleCodeBlock('${id}')" title="Toggle code"><img src="${toggleCodeImg}" alt="Toggle Code"></button>`;
            const expandAllBtn = hasChildren 
                ? `<button class="icon-btn expand-all-btn" onclick="event.stopPropagation(); toggleHierarchy('${id}')" title="Toggle hierarchy (no code)"><img src="${expandAllImg}" alt="Expand All"></button>`
                : '';
            const expandCodeBtn = hasChildren 
                ? `<button class="icon-btn expand-code-btn" onclick="event.stopPropagation(); toggleAllWithCode('${id}')" title="Toggle hierarchy + code"><img src="${expandCodeImg}" alt="Expand Code"></button>`
                : '';
            
            return `
            <div class="section depth-${depth} ${startCollapsed}" id="${id}" style="margin-left: ${indent}px;">
                <div class="section-header" onclick="toggleSection('${id}')">
                    <span class="chevron">▼</span>
                    <span class="section-title" title="${fileTip}">${escapeHtml(c.symbol || c.file || 'Code')}</span>
                    ${hasChildren ? `<span class="child-count">(${c.children.length})</span>` : ''}
                    ${toggleCodeBtn}
                    ${expandAllBtn}
                    ${expandCodeBtn}
                    ${c.file && !c.file.includes('(stdlib)') ? `<button class="open-file-btn" onclick="event.stopPropagation(); openFile('${escapeHtml(c.file)}', ${c.line || 1})">Open</button>` : ''}
                </div>
                <div class="section-content">
                    ${codeContent}
                    ${childrenHtml}
                </div>
            </div>`;
        };

        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Story Trace</title>
    
    <!-- Monaco Editor Loader -->
    <link rel="stylesheet" data-name="vs/editor/editor.main" href="https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs/editor/editor.main.css">
    <script src="https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs/loader.js"></script>
    
    <style>
        body {
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
            background: var(--vscode-editor-background);
            padding: 0;
            margin: 0;
        }
        
        .section {
            border: 1px solid var(--vscode-panel-border);
            margin: 8px;
            margin-right: 8px;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .section-header {
            background: var(--vscode-sideBarSectionHeader-background);
            padding: 6px 10px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            user-select: none;
            font-size: 0.9em;
        }
        
        .section-header:hover {
            background: var(--vscode-list-hoverBackground);
        }
        
        .section-header .chevron {
            transition: transform 0.2s;
            font-size: 0.8em;
        }
        
        .section.collapsed .chevron {
            transform: rotate(-90deg);
        }
        
        .section.collapsed .section-content {
            display: none;
        }
        
        .section-title {
            flex: 1;
            font-weight: 600;
            cursor: help;
        }
        
        .child-count {
            font-size: 0.8em;
            color: var(--vscode-descriptionForeground);
            margin-right: 4px;
        }
        
        .icon-btn {
            background: none;
            border: none;
            cursor: pointer;
            padding: 4px;
            margin-left: 6px;
            opacity: 0.8;
            vertical-align: middle;
            border-radius: 4px;
        }
        
        .icon-btn:hover {
            opacity: 1;
            background: var(--vscode-toolbar-hoverBackground, rgba(255,255,255,0.1));
        }
        
        .icon-btn img {
            width: 24px;
            height: 24px;
            vertical-align: middle;
        }
        
        .preview-btn {
            background: var(--vscode-button-secondaryBackground);
            color: var(--vscode-button-secondaryForeground);
            border: none;
            padding: 4px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.85em;
            margin-left: 6px;
        }
        
        .preview-btn:hover {
            background: var(--vscode-button-secondaryHoverBackground);
        }
        
        .preview-btn.active {
            background: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
        }
        
        .scenario-preview {
            padding: 8px 12px;
            background: var(--vscode-editor-background);
            border: 1px solid var(--vscode-panel-border);
            border-radius: 4px;
            margin-bottom: 8px;
        }
        
        .scenario-monaco {
            margin-bottom: 8px;
        }
        
        .depth-1 > .section-header,
        .depth-2 > .section-header,
        .depth-3 > .section-header { border-left: 3px solid #f5a623; }
        
        .open-file-btn, .show-code-btn, .expand-btn, .expand-all-btn {
            background: var(--vscode-button-secondaryBackground);
            color: var(--vscode-button-secondaryForeground);
            border: none;
            padding: 4px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.85em;
            margin-left: 6px;
        }
        
        .open-file-btn:hover, .show-code-btn:hover, .expand-btn:hover, .expand-all-btn:hover {
            background: var(--vscode-button-secondaryHoverBackground);
        }
        
        .show-code-btn {
            font-family: monospace;
        }
        
        .code-block.collapsed .monaco-container {
            display: none !important;
        }
        
        .code-block.collapsed {
            height: 0;
            overflow: hidden;
        }
        
        .section:not(.collapsed) .expand-btn {
            display: none;
        }
        
        .child-count {
            font-size: 0.8em;
            color: var(--vscode-descriptionForeground);
            font-weight: normal;
        }
        
        .load-code-btn {
            background: var(--vscode-button-secondaryBackground);
            color: var(--vscode-button-secondaryForeground);
            border: 1px dashed var(--vscode-panel-border);
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.85em;
            width: 100%;
            text-align: left;
        }
        
        .load-code-btn:hover {
            background: var(--vscode-button-secondaryHoverBackground);
            border-style: solid;
        }
        
        .lazy-code.loaded .load-code-btn {
            display: none;
        }
        
        .lazy-code.loaded .hidden-code {
            display: block !important;
        }
        
        .children-container {
            margin-top: 8px;
        }
        
        .section-content {
            padding: 8px;
            background: var(--vscode-editor-background);
        }
        
        .scenario-steps {
            font-family: var(--vscode-editor-font-family);
            background: var(--vscode-textBlockQuote-background);
            padding: 10px;
            border-radius: 4px;
            border-left: 3px solid var(--vscode-textLink-foreground);
        }
        
        .step {
            margin: 3px 0;
        }
        
        .step-keyword {
            color: var(--vscode-symbolIcon-keywordForeground, #c586c0);
            font-weight: 600;
        }
        
        pre {
            background: var(--vscode-textCodeBlock-background);
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
            margin: 0 0 8px 0;
            font-family: var(--vscode-editor-font-family);
            font-size: 12px;
            line-height: 1.4;
        }
        
        .monaco-container {
            border: 1px solid var(--vscode-panel-border);
            border-radius: 4px;
            margin: 0 0 8px 0;
            min-height: 0;
            overflow: hidden;
            transition: height 0.15s ease-out;
        }
        
        .monaco-container[data-editable="true"] {
            border-color: var(--vscode-focusBorder);
        }
        
        .section.collapsed .monaco-container {
            height: 0 !important;
            border: none;
            margin: 0;
        }
        
        /* Clickable method call decoration */
        .clickable-method {
            text-decoration: underline;
            text-decoration-style: dotted;
            cursor: pointer;
        }
        
        .clickable-method:hover {
            text-decoration-style: solid;
            color: var(--vscode-textLink-foreground) !important;
        }
        
        .main-section {
            border-width: 2px;
        }
        
        .story-section {
            border-left: 4px solid #4a9eff;
        }
        
        .story-properties {
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 8px;
            padding: 8px;
            background: var(--vscode-textBlockQuote-background);
            border-radius: 4px;
            margin-bottom: 8px;
        }
        
        .property-label {
            font-weight: 600;
            color: var(--vscode-descriptionForeground);
            padding-top: 4px;
        }
        
        .property-editor {
            min-height: 40px;
        }
    </style>
</head>
<body>
    ${isStoryFormat ? `
    <!-- STORY FORMAT: Story -> Scenarios -> Test -> Code -->
    <div class="section main-section story-section" id="story-section">
        <div class="section-header" onclick="toggleSection('story-section')">
            <span class="chevron">▼</span>
            <span class="section-title" title="${escapeHtml(story.file || '')}:${story.line || ''}">${escapeHtml(story.name || 'Unknown Story')}</span>
            <span class="child-count">(${scenarios.length} scenarios)</span>
            <button class="icon-btn expand-all-btn" onclick="event.stopPropagation(); toggleHierarchy('story-section')" title="Toggle hierarchy"><img src="${expandAllImg}" alt="Expand All"></button>
            <button class="icon-btn expand-code-btn" onclick="event.stopPropagation(); toggleAllWithCode('story-section')" title="Toggle hierarchy + code"><img src="${expandCodeImg}" alt="Expand Code"></button>
            <button class="open-file-btn" onclick="event.stopPropagation(); openFile('${escapeHtml(story.file || '')}', ${story.line || 1})">Open</button>
        </div>
        <div class="section-content">
            <!-- Story properties -->
            <div class="story-properties">
                <span class="property-label">Users:</span>
                <div class="monaco-container property-editor" style="height: 40px;"
                     data-file="${escapeHtml(story.file || '')}"
                     data-line="${story.line || 1}"
                     data-editable="true"
                     data-language="markdown"
                     data-story-property="users"
                     data-code="${Buffer.from(story.users || '').toString('base64')}"></div>
                
                <span class="property-label">Acceptance Criteria:</span>
                <div class="monaco-container property-editor" style="height: 80px;"
                     data-file="${escapeHtml(story.file || '')}"
                     data-line="${story.line || 1}"
                     data-editable="true"
                     data-language="markdown"
                     data-story-property="acceptance_criteria"
                     data-code="${Buffer.from(story.acceptance_criteria || '').toString('base64')}"></div>
            </div>
            
            <!-- Scenarios -->
            ${scenarios.map((s, i) => {
                const scenarioId = `scenario-${i}`;
                const testId = `${scenarioId}-test`;
                const scenarioTest = s.test || {};
                const scenarioCode = s.code || [];
                return `
                <div class="section" id="${scenarioId}">
                    <div class="section-header" onclick="toggleSection('${scenarioId}')">
                        <span class="chevron">▼</span>
                        <span class="section-title" title="${escapeHtml(s.file || story.file || '')}:${s.line || 1}">${escapeHtml(s.name || 'Scenario')}</span>
                        <span class="child-count">(${scenarioCode.length})</span>
                        <button class="preview-btn" onclick="event.stopPropagation(); toggleScenarioPreview('${scenarioId}')" title="Toggle Edit/Preview">Preview</button>
                        <button class="icon-btn expand-all-btn" onclick="event.stopPropagation(); toggleHierarchy('${scenarioId}')" title="Toggle hierarchy"><img src="${expandAllImg}" alt="Expand All"></button>
                        <button class="icon-btn expand-code-btn" onclick="event.stopPropagation(); toggleAllWithCode('${scenarioId}')" title="Toggle hierarchy + code"><img src="${expandCodeImg}" alt="Expand Code"></button>
                        <button class="open-file-btn" onclick="event.stopPropagation(); openFile('${escapeHtml(s.file || story.file || '')}', ${s.line || 1})">Open</button>
                    </div>
                    <div class="section-content">
                        <!-- Scenario steps editor -->
                        <div class="scenario-editor-container" id="${scenarioId}-editor">
                            <div class="monaco-container scenario-monaco" style="height: 100px;"
                                 data-file="${escapeHtml(story.file || '')}"
                                 data-line="${story.line || 1}"
                                 data-editable="true"
                                 data-language="markdown"
                                 data-scenario-name="${escapeHtml(s.name || '')}"
                                 data-code="${Buffer.from(s.steps || '').toString('base64')}"></div>
                        </div>
                        <div class="scenario-preview" id="${scenarioId}-preview" style="display: none;">
                            ${formatSteps(s.steps || '')}
                        </div>
                        
                        <!-- Test nested inside Scenario -->
                        <div class="section" id="${testId}">
                            <div class="section-header" onclick="toggleSection('${testId}')">
                                <span class="chevron">▼</span>
                                <span class="section-title" title="${escapeHtml(scenarioTest.file || '')}:${scenarioTest.line || ''}">${escapeHtml(scenarioTest.method || 'Test')}</span>
                                <span class="child-count">(${scenarioCode.length})</span>
                                <button class="icon-btn toggle-code-btn" onclick="event.stopPropagation(); toggleCodeBlock('${testId}')" title="Toggle code"><img src="${toggleCodeImg}" alt="Toggle Code"></button>
                                <button class="icon-btn expand-all-btn" onclick="event.stopPropagation(); toggleHierarchy('${testId}')" title="Toggle hierarchy"><img src="${expandAllImg}" alt="Expand All"></button>
                                <button class="icon-btn expand-code-btn" onclick="event.stopPropagation(); toggleAllWithCode('${testId}')" title="Toggle hierarchy + code"><img src="${expandCodeImg}" alt="Expand Code"></button>
                                ${scenarioTest.file ? `<button class="open-file-btn" onclick="event.stopPropagation(); openFile('${escapeHtml(scenarioTest.file)}', ${scenarioTest.line || 1})">Open</button>` : ''}
                            </div>
                            <div class="section-content">
                                <div class="code-block collapsed" id="${testId}-code">
                                    <div class="monaco-container" style="display:none; height: 300px;" 
                                         data-file="${escapeHtml(scenarioTest.file || '')}" 
                                         data-line="${scenarioTest.line || 1}" 
                                         data-editable="true" 
                                         data-code="${Buffer.from(scenarioTest.code || '// No test code').toString('base64')}"></div>
                                </div>
                                <div class="children-container">
                                    ${scenarioCode.map((c, j) => renderCodeSection(c, j, `${testId}-code`)).join('')}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`;
            }).join('')}
        </div>
    </div>
    ` : `
    <!-- OLD FORMAT: Single Scenario -> Test -> Code -->
    <div class="section main-section" id="scenario-section">
        <div class="section-header" onclick="toggleSection('scenario-section')">
            <span class="chevron">▼</span>
            <span class="section-title" title="${escapeHtml(scenario.file || test.file || '')}:${scenario.line || test.line || ''}">${escapeHtml(scenario.name || 'Unknown')}</span>
            <span class="child-count">(1)</span>
            <button class="preview-btn" onclick="event.stopPropagation(); toggleScenarioPreview()" title="Toggle Edit/Preview">Preview</button>
            <button class="icon-btn expand-all-btn" onclick="event.stopPropagation(); toggleHierarchy('scenario-section')" title="Toggle hierarchy (no code)"><img src="${expandAllImg}" alt="Expand All"></button>
            <button class="icon-btn expand-code-btn" onclick="event.stopPropagation(); toggleAllWithCode('scenario-section')" title="Toggle hierarchy + code"><img src="${expandCodeImg}" alt="Expand Code"></button>
            <button class="open-file-btn" onclick="event.stopPropagation(); openFile('${escapeHtml(scenario.file || test.file || '')}', ${scenario.line || test.line || 1})">Open</button>
        </div>
        <div class="section-content">
            <div class="scenario-editor-container" id="scenario-editor-container">
                <div class="monaco-container scenario-monaco" style="height: 150px;" 
                     data-file="${escapeHtml(scenario.file || '')}" 
                     data-line="${scenario.line || 1}" 
                     data-editable="true" 
                     data-language="markdown"
                     data-scenario-name="${escapeHtml(scenario.name || '')}"
                     data-code="${Buffer.from(scenario.steps || '').toString('base64')}"></div>
            </div>
            <div class="scenario-preview" id="scenario-preview" style="display: none;">
                ${formatSteps(scenario.steps || '')}
            </div>
            
            <div class="section" id="test-section">
                <div class="section-header" onclick="toggleSection('test-section')">
                    <span class="chevron">▼</span>
                    <span class="section-title" title="${escapeHtml(test.file || '')}:${test.line || ''}">${escapeHtml(test.method || 'Test')}</span>
                    <span class="child-count">(${code.length})</span>
                    <button class="icon-btn toggle-code-btn" onclick="event.stopPropagation(); toggleCodeBlock('test-section')" title="Toggle code"><img src="${toggleCodeImg}" alt="Toggle Code"></button>
                    <button class="icon-btn expand-all-btn" onclick="event.stopPropagation(); toggleHierarchy('test-section')" title="Toggle hierarchy (no code)"><img src="${expandAllImg}" alt="Expand All"></button>
                    <button class="icon-btn expand-code-btn" onclick="event.stopPropagation(); toggleAllWithCode('test-section')" title="Toggle hierarchy + code"><img src="${expandCodeImg}" alt="Expand Code"></button>
                    ${test.file ? `<button class="open-file-btn" onclick="event.stopPropagation(); openFile('${escapeHtml(test.file)}', ${test.line || 1})">Open</button>` : ''}
                </div>
                <div class="section-content">
                    <div class="code-block collapsed" id="test-section-code">
                        <div class="monaco-container" style="display:none; height: 300px;" data-file="${escapeHtml(test.file || '')}" data-line="${test.line || 1}" data-editable="true" data-code="${Buffer.from(test.code || '// No test code').toString('base64')}"></div>
                    </div>
                    <div class="children-container">
                        ${code.map((c, i) => renderCodeSection(c, i)).join('')}
                    </div>
                </div>
            </div>
        </div>
    </div>
    `}

    <script>
        const vscode = acquireVsCodeApi();
        const editors = new Map();  // Track all Monaco editors
        let monacoReady = false;
        
        // Build symbol-to-section map for navigation
        // Store ALL matches for each symbol to handle duplicates
        const symbolMap = {};  // symbol -> [sectionId, ...]
        function buildSymbolMap(items, parentId = '') {
            items.forEach((item, i) => {
                const id = parentId ? parentId + '-' + i : 'code-' + i;
                const symbol = item.symbol || '';
                // Extract just the method/class name (after the last dot)
                const shortName = symbol.split('.').pop();
                
                // Store full symbol name (always unique)
                if (symbol) {
                    if (!symbolMap[symbol]) symbolMap[symbol] = [];
                    symbolMap[symbol].push(id);
                }
                
                // Store short name (may have duplicates)
                if (shortName && shortName !== symbol) {
                    if (!symbolMap[shortName]) symbolMap[shortName] = [];
                    symbolMap[shortName].push(id);
                }
                
                // For __init__ methods, also map the class name
                if (shortName === '__init__' && symbol.includes('.')) {
                    const className = symbol.split('.')[0];
                    if (className) {
                        if (!symbolMap[className]) symbolMap[className] = [];
                        symbolMap[className].push(id);
                    }
                }
                if (item.children && item.children.length) {
                    buildSymbolMap(item.children, id);
                }
            });
        }
        // Initialize symbol map from data
        ${isStoryFormat ? `
        // Story format: build symbol map from all scenarios
        ${JSON.stringify(scenarios)}.forEach((s, i) => {
            const testId = 'scenario-' + i + '-test';
            buildSymbolMap(s.code || [], testId + '-code');
            const testMethod = s.test ? s.test.method : '';
            if (testMethod) {
                if (!symbolMap[testMethod]) symbolMap[testMethod] = [];
                symbolMap[testMethod].push(testId);
            }
        });
        ` : `
        // Single scenario format
        buildSymbolMap(${JSON.stringify(code)});
        if (!symbolMap['${escapeHtml(test.method || '')}']) symbolMap['${escapeHtml(test.method || '')}'] = [];
        symbolMap['${escapeHtml(test.method || '')}'].push('test-section');
        `}
        
        function toggleSection(id) {
            const section = document.getElementById(id);
            const wasCollapsed = section.classList.contains('collapsed');
            section.classList.toggle('collapsed');
            
            // When expanding, restore Monaco heights and layout
            if (wasCollapsed) {
                setTimeout(() => {
                    // Restore Monaco heights
                    section.querySelectorAll('.monaco-container').forEach(container => {
                        const savedHeight = container.dataset.savedHeight;
                        if (savedHeight) {
                            container.style.height = savedHeight;
                        }
                    });
                    editors.forEach(editor => editor.layout());
                }, 50);
            } else {
                // When collapsing, save and minimize Monaco heights
                section.querySelectorAll('.monaco-container').forEach(container => {
                    container.dataset.savedHeight = container.style.height;
                    container.style.height = '0px';
                });
            }
        }
        
        // Toggle scenario between Edit and Preview modes
        // scenarioId is optional - if provided, uses that scenario's elements
        function toggleScenarioPreview(scenarioId) {
            const editorId = scenarioId ? scenarioId + '-editor' : 'scenario-editor-container';
            const previewId = scenarioId ? scenarioId + '-preview' : 'scenario-preview';
            const editorContainer = document.getElementById(editorId);
            const preview = document.getElementById(previewId);
            // Find the button within the section header
            const section = scenarioId ? document.getElementById(scenarioId) : document.getElementById('scenario-section');
            const btn = section ? section.querySelector('.preview-btn') : document.querySelector('.preview-btn');
            
            if (!editorContainer || !preview) return;
            
            const isPreviewMode = preview.style.display !== 'none';
            
            if (isPreviewMode) {
                // Switch to Edit mode
                preview.style.display = 'none';
                editorContainer.style.display = 'block';
                btn.textContent = 'Preview';
                btn.classList.remove('active');
                setTimeout(() => editors.forEach(e => e.layout()), 50);
            } else {
                // Switch to Preview mode - update preview content from editor
                const monacoContainer = editorContainer.querySelector('.monaco-container');
                const editor = editors.get(monacoContainer);
                if (editor) {
                    const markdown = editor.getValue();
                    // Simple markdown to HTML (GIVEN/WHEN/THEN formatting)
                    preview.innerHTML = formatMarkdownSteps(markdown);
                }
                editorContainer.style.display = 'none';
                preview.style.display = 'block';
                btn.textContent = 'Edit';
                btn.classList.add('active');
            }
        }
        
        // Format markdown steps to HTML
        function formatMarkdownSteps(text) {
            if (!text) return '';
            return text.split('\\n').map(line => {
                const trimmed = line.trim();
                if (trimmed.startsWith('GIVEN:')) {
                    return '<div class="step given"><strong>GIVEN:</strong> ' + escapeHtmlJs(trimmed.substring(6).trim()) + '</div>';
                } else if (trimmed.startsWith('WHEN:')) {
                    return '<div class="step when"><strong>WHEN:</strong> ' + escapeHtmlJs(trimmed.substring(5).trim()) + '</div>';
                } else if (trimmed.startsWith('THEN:')) {
                    return '<div class="step then"><strong>THEN:</strong> ' + escapeHtmlJs(trimmed.substring(5).trim()) + '</div>';
                } else if (trimmed.startsWith('AND:')) {
                    return '<div class="step and"><strong>AND:</strong> ' + escapeHtmlJs(trimmed.substring(4).trim()) + '</div>';
                } else if (trimmed) {
                    return '<div class="step">' + escapeHtmlJs(trimmed) + '</div>';
                }
                return '';
            }).join('');
        }
        
        function escapeHtmlJs(str) {
            return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
        }
        
        // Toggle code block visibility (show/hide code without affecting hierarchy)
        // For lazy items, this triggers loading first if not already loaded
        function toggleCodeBlock(sectionId) {
            const codeBlock = document.getElementById(sectionId + '-code');
            if (!codeBlock) return;
            
            // Check if this is a lazy block that needs loading
            if (codeBlock.classList.contains('lazy-code') && !codeBlock.classList.contains('loaded')) {
                // Trigger lazy loading
                const loadBtn = codeBlock.querySelector('.load-code-btn');
                if (loadBtn) {
                    requestCodeFromBtn(loadBtn);
                    return;
                }
            }
            
            const wasCollapsed = codeBlock.classList.contains('collapsed');
            codeBlock.classList.toggle('collapsed');
            
            const container = codeBlock.querySelector('.monaco-container');
            if (wasCollapsed) {
                // Expanding code - show Monaco
                if (container) {
                    container.style.display = 'block';
                    const savedHeight = container.dataset.savedHeight;
                    if (savedHeight) container.style.height = savedHeight;
                }
                setTimeout(() => editors.forEach(e => e.layout()), 50);
            } else {
                // Collapsing code - hide Monaco
                if (container) {
                    container.style.display = 'none';
                }
            }
        }
        
        // Check if a code block has been loaded (not lazy or already loaded)
        function isCodeBlockLoaded(block) {
            // If it has the lazy-code class but NOT the 'loaded' class, it's not loaded yet
            if (block.classList.contains('lazy-code') && !block.classList.contains('loaded')) {
                return false;
            }
            return true;
        }
        
        // Toggle hierarchy (collapse if expanded, expand if collapsed) - no code
        function toggleHierarchy(sectionId) {
            const section = document.getElementById(sectionId);
            if (!section) return;
            
            // Check if any child sections are expanded
            const childSections = section.querySelectorAll('.section');
            const anyExpanded = Array.from(childSections).some(s => !s.classList.contains('collapsed'));
            
            if (anyExpanded) {
                // Collapse all
                childSections.forEach(child => child.classList.add('collapsed'));
            } else {
                // Expand all hierarchy, keep code collapsed
                section.classList.remove('collapsed');
                childSections.forEach(child => child.classList.remove('collapsed'));
                
                // Keep ALL code blocks collapsed
                section.querySelectorAll('.code-block').forEach(block => {
                    if (!isCodeBlockLoaded(block)) return;
                    block.classList.add('collapsed');
                    const container = block.querySelector('.monaco-container');
                    if (container) container.style.display = 'none';
                });
                
                const ownCodeBlock = document.getElementById(sectionId + '-code');
                if (ownCodeBlock && isCodeBlockLoaded(ownCodeBlock)) {
                    ownCodeBlock.classList.add('collapsed');
                    const container = ownCodeBlock.querySelector('.monaco-container');
                    if (container) container.style.display = 'none';
                }
            }
        }
        
        // Toggle hierarchy + code (collapse if expanded, expand if collapsed)
        function toggleAllWithCode(sectionId) {
            const section = document.getElementById(sectionId);
            if (!section) return;
            
            // Check if any code blocks are expanded
            const codeBlocks = section.querySelectorAll('.code-block');
            const anyCodeExpanded = Array.from(codeBlocks).some(b => isCodeBlockLoaded(b) && !b.classList.contains('collapsed'));
            
            if (anyCodeExpanded) {
                // Collapse all
                section.querySelectorAll('.section').forEach(child => child.classList.add('collapsed'));
                codeBlocks.forEach(block => {
                    if (!isCodeBlockLoaded(block)) return;
                    block.classList.add('collapsed');
                    const container = block.querySelector('.monaco-container');
                    if (container) container.style.display = 'none';
                });
            } else {
                // Expand all hierarchy + code
                section.classList.remove('collapsed');
                section.querySelectorAll('.section').forEach(child => child.classList.remove('collapsed'));
                
                codeBlocks.forEach(block => {
                    if (!isCodeBlockLoaded(block)) return;
                    block.classList.remove('collapsed');
                    const container = block.querySelector('.monaco-container');
                    if (container) {
                        container.style.display = 'block';
                        const savedHeight = container.dataset.savedHeight;
                        if (savedHeight) container.style.height = savedHeight;
                    }
                });
                
                const ownCodeBlock = document.getElementById(sectionId + '-code');
                if (ownCodeBlock && isCodeBlockLoaded(ownCodeBlock)) {
                    ownCodeBlock.classList.remove('collapsed');
                    const container = ownCodeBlock.querySelector('.monaco-container');
                    if (container) {
                        container.style.display = 'block';
                        const savedHeight = container.dataset.savedHeight;
                        if (savedHeight) container.style.height = savedHeight;
                    }
                }
            }
            
            setTimeout(() => editors.forEach(e => e.layout()), 100);
        }
        
        // Request code from extension (true lazy loading)
        function requestCodeFromBtn(btn) {
            const lazyCode = btn.parentElement;
            if (!lazyCode) return;
            
            const id = lazyCode.dataset.id;
            const file = lazyCode.dataset.file;
            const line = parseInt(lazyCode.dataset.line, 10) || 1;
            const symbol = lazyCode.dataset.symbol;
            
            const loading = lazyCode.querySelector('.loading-indicator');
            btn.style.display = 'none';
            if (loading) loading.style.display = 'block';
            
            vscode.postMessage({ command: 'loadCode', id, file, line, symbol });
        }
        
        // Create Monaco editor in a container
        function createEditor(container, code, file, line) {
            if (!monacoReady) {
                console.log('Monaco not ready, queuing...');
                setTimeout(() => createEditor(container, code, file, line), 100);
                return;
            }
            
            const isEditable = container.dataset.editable === 'true';
            const language = container.dataset.language || 'python';
            const isMarkdown = language === 'markdown';
            
            // Initial height estimate - will be adjusted after editor renders
            const lineCount = (code.match(/\\n/g) || []).length + 1;
            const initialHeight = Math.min(Math.max(lineCount * 19 + 20, 60), 500);
            container.style.height = initialHeight + 'px';
            container.style.display = 'block';
            
            const startLineNum = parseInt(line, 10) || 1;
            const editor = monaco.editor.create(container, {
                value: code,
                language: language,
                theme: getMonacoTheme(),  // Match VS Code theme
                readOnly: !isEditable,
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                lineNumbers: isMarkdown ? 'off' : (n) => String(n + startLineNum - 1),  // No line numbers for markdown
                lineNumbersMinChars: isMarkdown ? 0 : 4,
                fontSize: 13,
                automaticLayout: true,
                wordWrap: 'on'
            });
            
            editors.set(container, editor);
            
            // Auto-size to content height
            function updateEditorHeight() {
                const contentHeight = Math.min(editor.getContentHeight(), 500);
                const newHeight = Math.max(contentHeight, 40);
                container.style.height = newHeight + 'px';
                editor.layout();
            }
            
            // Update height after initial render
            setTimeout(updateEditorHeight, 50);
            
            // Update height when content changes (e.g., after word wrap recalculates)
            editor.onDidContentSizeChange(updateEditorHeight);
            
            // Add decorations and navigation only for code editors, not markdown
            if (!isMarkdown) {
                addMethodDecorations(editor);
                
                // Double-click to navigate to method section
                editor.onMouseDown(e => {
                    if (e.event.detail === 2) {  // Double-click
                        const position = e.target.position;
                        if (position) {
                            const model = editor.getModel();
                            const word = model.getWordAtPosition(position);
                            if (word && symbolMap[word.word] && symbolMap[word.word].length > 0) {
                                // Navigate to first match
                                const sectionId = symbolMap[word.word][0];
                                navigateToSection(sectionId);
                            }
                        }
                    }
                });
            }
            
            // Save function - used by blur and Ctrl+S
            function saveEditorContent() {
                const newCode = editor.getValue();
                const originalCode = container.dataset.originalCode || code;
                if (newCode !== originalCode) {
                    // Check if this is a scenario editor (markdown with scenario name)
                    const scenarioName = container.dataset.scenarioName;
                    if (isMarkdown && scenarioName) {
                        console.log('Saving scenario:', scenarioName);
                        vscode.postMessage({
                            command: 'saveScenario',
                            file: file,
                            scenarioName: scenarioName,
                            newSteps: newCode
                        });
                    } else {
                        console.log('Saving changes to:', file, 'line:', line);
                        vscode.postMessage({
                            command: 'saveCode',
                            file: file,
                            line: parseInt(line, 10),
                            originalCode: originalCode,
                            newCode: newCode
                        });
                    }
                    container.dataset.originalCode = newCode;
                }
            }
            
            if (isEditable) {
                // Save on blur (tab away or click away)
                editor.onDidBlurEditorWidget(saveEditorContent);
                
                // Save on Ctrl+S (Windows/Linux) or Cmd+S (Mac)
                // Monaco's addCommand doesn't work in VS Code webviews because 
                // VS Code intercepts Ctrl+S before it reaches the webview.
                // Use DOM keydown handler instead.
                container.addEventListener('keydown', function(e) {
                    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                        e.preventDefault();
                        e.stopPropagation();
                        saveEditorContent();
                    }
                });
                
                container.dataset.originalCode = code;
            }
        }
        
        // Handle messages from extension
        window.addEventListener('message', event => {
            const message = event.data;
            if (message.command === 'codeLoaded') {
                const lazyCode = document.getElementById(message.id + '-code');
                if (!lazyCode) return;
                
                const loading = lazyCode.querySelector('.loading-indicator');
                const monacoContainer = lazyCode.querySelector('.monaco-container');
                const btn = lazyCode.querySelector('.load-code-btn');
                
                if (loading) loading.style.display = 'none';
                if (btn) btn.remove();
                
                if (monacoContainer) {
                    createEditor(monacoContainer, message.code, monacoContainer.dataset.file, monacoContainer.dataset.line);
                }
                
                // Mark as loaded and expand the code block
                lazyCode.classList.add('loaded');
                lazyCode.classList.remove('collapsed');
            } else if (message.command === 'codeSaved') {
                console.log('Code saved successfully:', message.file);
            } else if (message.command === 'scenarioSaved') {
                console.log('Scenario saved successfully:', message.scenarioName);
            } else if (message.command === 'saveError') {
                console.error('Save failed:', message.error);
            }
        });
        
        function openFile(file, line) {
            vscode.postMessage({ command: 'openFile', file, line });
        }
        
        // Add underline decorations to method calls that have matching sections
        function addMethodDecorations(editor) {
            const model = editor.getModel();
            const decorations = [];
            const lineCount = model.getLineCount();
            
            for (let lineNum = 1; lineNum <= lineCount; lineNum++) {
                const line = model.getLineContent(lineNum);
                
                // Pattern 1: method calls like .method_name( or .MethodName(
                const dotMethodPattern = /\\.([a-zA-Z_][a-zA-Z0-9_]*)\\s*\\(/g;
                let match;
                while ((match = dotMethodPattern.exec(line)) !== null) {
                    const methodName = match[1];
                    if (methodName && symbolMap[methodName] && symbolMap[methodName].length > 0) {
                        const startCol = match.index + 2;  // +1 for dot, +1 for 1-based
                        decorations.push({
                            range: new monaco.Range(lineNum, startCol, lineNum, startCol + methodName.length),
                            options: {
                                inlineClassName: 'clickable-method',
                                hoverMessage: { value: '**Double-click** to navigate to ' + methodName }
                            }
                        });
                    }
                }
                
                // Pattern 2: constructor calls like ClassName( - uppercase start
                const constructorPattern = /(?:^|[^.a-zA-Z_])([A-Z][a-zA-Z0-9_]*)\\s*\\(/g;
                while ((match = constructorPattern.exec(line)) !== null) {
                    const className = match[1];
                    if (className && symbolMap[className] && symbolMap[className].length > 0) {
                        const startCol = match.index + match[0].indexOf(className) + 1;
                        decorations.push({
                            range: new monaco.Range(lineNum, startCol, lineNum, startCol + className.length),
                            options: {
                                inlineClassName: 'clickable-method',
                                hoverMessage: { value: '**Double-click** to navigate to ' + className + '.__init__' }
                            }
                        });
                    }
                }
                
                // Pattern 3: Property access like .property_name (not followed by paren)
                const propertyPattern = /\\.([a-zA-Z_][a-zA-Z0-9_]*)(?!\\s*\\()/g;
                while ((match = propertyPattern.exec(line)) !== null) {
                    const propName = match[1];
                    if (propName && symbolMap[propName] && symbolMap[propName].length > 0) {
                        const startCol = match.index + 2;  // +1 for dot, +1 for 1-based
                        const alreadyDecorated = decorations.some(d => 
                            d.range.startLineNumber === lineNum && 
                            d.range.startColumn === startCol
                        );
                        if (!alreadyDecorated) {
                            decorations.push({
                                range: new monaco.Range(lineNum, startCol, lineNum, startCol + propName.length),
                                options: {
                                    inlineClassName: 'clickable-method',
                                    hoverMessage: { value: '**Double-click** to navigate to ' + propName + ' (property)' }
                                }
                            });
                        }
                    }
                }
                
                // Pattern 4: Any identifier that matches our symbolMap (assignment targets, etc.)
                const identifierPattern = /(?:^|[^.])([a-zA-Z_][a-zA-Z0-9_]*)/g;
                while ((match = identifierPattern.exec(line)) !== null) {
                    const name = match[1];
                    // Only if in symbolMap and not already decorated (check by position)
                    if (name && symbolMap[name] && symbolMap[name].length > 0 && name.length > 3) {  // Skip short names to reduce noise
                        const startCol = match.index + match[0].indexOf(name) + 1;
                        // Check if this position is already decorated
                        const alreadyDecorated = decorations.some(d => 
                            d.range.startLineNumber === lineNum && 
                            d.range.startColumn === startCol
                        );
                        if (!alreadyDecorated) {
                            decorations.push({
                                range: new monaco.Range(lineNum, startCol, lineNum, startCol + name.length),
                                options: {
                                    inlineClassName: 'clickable-method',
                                    hoverMessage: { value: '**Double-click** to navigate to ' + name }
                                }
                            });
                        }
                    }
                }
            }
            
            console.log('Adding', decorations.length, 'decorations to editor');
            if (decorations.length > 0) {
                editor.deltaDecorations([], decorations);
            }
        }
        
        // Navigate to a section by ID - expand and scroll
        function navigateToSection(sectionId) {
            // First, expand the code-root if collapsed
            const codeRoot = document.getElementById('code-root');
            if (codeRoot && codeRoot.classList.contains('collapsed')) {
                codeRoot.classList.remove('collapsed');
            }
            
            // Expand all parent sections
            let currentId = sectionId;
            const parts = currentId.split('-');
            for (let i = 2; i < parts.length; i++) {
                const parentId = parts.slice(0, i).join('-');
                const parent = document.getElementById(parentId);
                if (parent && parent.classList.contains('collapsed')) {
                    parent.classList.remove('collapsed');
                }
            }
            
            // Now expand and scroll to the target section
            const section = document.getElementById(sectionId);
            if (section) {
                section.classList.remove('collapsed');
                section.scrollIntoView({ behavior: 'smooth', block: 'center' });
                // Highlight briefly
                section.style.outline = '2px solid var(--vscode-focusBorder)';
                setTimeout(() => { section.style.outline = ''; }, 2000);
            }
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        function formatSteps(steps) {
            if (!steps) return '';
            return steps.split('\\n').map(line => {
                const trimmed = line.trim();
                if (!trimmed) return '';
                const keywords = ['GIVEN', 'WHEN', 'THEN', 'AND', 'Given', 'When', 'Then', 'And'];
                for (const kw of keywords) {
                    if (trimmed.startsWith(kw + ':') || trimmed.startsWith(kw + ' ')) {
                        const rest = trimmed.substring(kw.length).replace(/^[:\\s]+/, '');
                        return '<div class="step"><span class="step-keyword">' + kw + '</span> ' + escapeHtml(rest) + '</div>';
                    }
                }
                return '<div class="step">' + escapeHtml(trimmed) + '</div>';
            }).join('');
        }
        
        // Detect VS Code theme
        function getMonacoTheme() {
            const body = document.body;
            if (body.classList.contains('vscode-high-contrast')) return 'hc-black';
            if (body.classList.contains('vscode-dark')) return 'vs-dark';
            return 'vs';  // light theme
        }
        
        // Initialize Monaco
        require.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' } });
        require(['vs/editor/editor.main'], function() {
            monacoReady = true;
            console.log('Monaco loaded');
            
            // Match VS Code theme
            monaco.editor.setTheme(getMonacoTheme());
            
            // Initialize all pre-loaded editors
            document.querySelectorAll('.monaco-container[data-code]').forEach(container => {
                const code = atob(container.dataset.code);
                createEditor(container, code, container.dataset.file, container.dataset.line);
            });
        });
    </script>
</body>
</html>`;
    }
}

// Helper to escape HTML (used in template literal)
function escapeHtml(text) {
    if (!text) return '';
    return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// Helper to format steps (used in template literal)
function formatSteps(steps) {
    if (!steps) return '';
    return steps.split('\n').map(line => {
        const trimmed = line.trim();
        if (!trimmed) return '';
        
        const keywords = ['GIVEN', 'WHEN', 'THEN', 'AND', 'Given', 'When', 'Then', 'And'];
        for (const kw of keywords) {
            if (trimmed.startsWith(kw + ':') || trimmed.startsWith(kw + ' ')) {
                const rest = trimmed.substring(kw.length).replace(/^[:\s]+/, '');
                return `<div class="step"><span class="step-keyword">${kw}</span> ${escapeHtml(rest)}</div>`;
            }
        }
        return `<div class="step">${escapeHtml(trimmed)}</div>`;
    }).join('');
}

module.exports = { StoryTraceEditorProvider };
