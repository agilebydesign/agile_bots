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
     */
    getHtmlForWebview(webview, data) {
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
            
            if (isLazy) {
                // Lazy: show "Load code" button, code will be fetched on demand
                codeContent = `<div class="lazy-code" id="${id}-code" data-file="${fileAttr}" data-line="${lineAttr}" data-symbol="${symbolAttr}" data-id="${id}">
                     <button class="load-code-btn" onclick="event.stopPropagation(); requestCodeFromBtn(this)">
                       ▶ Load code
                     </button>
                     <div class="monaco-container" style="display:none; height: 200px;" data-file="${fileAttr}" data-line="${lineAttr}" data-editable="${isEditable}"></div>
                     <div class="loading-indicator" style="display:none;">Loading...</div>
                   </div>`;
            } else {
                // Not lazy: code is already in JSON - use Monaco editor
                const codeB64 = Buffer.from(c.code || '// No code').toString('base64');
                codeContent = `<div class="monaco-container" style="height: 200px;" data-file="${fileAttr}" data-line="${lineAttr}" data-editable="${isEditable}" data-code="${codeB64}"></div>`;
            }
            
            // All code sections start collapsed except L1
            const startCollapsed = depth > 1 ? 'collapsed' : '';
            
            return `
            <div class="section depth-${depth} ${startCollapsed}" id="${id}" style="margin-left: ${indent}px;">
                <div class="section-header" onclick="toggleSection('${id}')">
                    <span class="chevron">▼</span>
                    <span class="section-title">${escapeHtml(c.symbol || c.file || 'Code')}</span>
                    ${hasChildren ? `<span class="child-count">(${c.children.length} calls)</span>` : ''}
                    <span class="depth-badge">L${depth}</span>
                    <span class="section-meta">${escapeHtml(c.file || '')}:${c.line || ''}</span>
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
        }
        
        .section-meta {
            font-size: 0.8em;
            color: var(--vscode-descriptionForeground);
        }
        
        .depth-badge {
            background: var(--vscode-badge-background);
            color: var(--vscode-badge-foreground);
            padding: 1px 4px;
            border-radius: 3px;
            font-size: 0.7em;
        }
        
        .depth-1 > .section-header { border-left: 3px solid #4ec9b0; }
        .depth-2 > .section-header { border-left: 3px solid #dcdcaa; }
        .depth-3 > .section-header { border-left: 3px solid #9cdcfe; background: var(--vscode-editor-background); }
        
        .open-file-btn {
            background: var(--vscode-button-secondaryBackground);
            color: var(--vscode-button-secondaryForeground);
            border: none;
            padding: 2px 6px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 0.75em;
        }
        
        .open-file-btn:hover {
            background: var(--vscode-button-secondaryHoverBackground);
        }
        
        .expand-btn {
            background: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            padding: 4px 10px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 0.85em;
            margin: 8px 0;
            display: block;
        }
        
        .expand-btn:hover {
            background: var(--vscode-button-hoverBackground);
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
        
        .type-badge {
            background: var(--vscode-badge-background);
            color: var(--vscode-badge-foreground);
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.75em;
        }
        
        .main-section {
            border-width: 2px;
        }
    </style>
</head>
<body>
    <!-- SCENARIO SECTION -->
    <div class="section main-section" id="scenario-section">
        <div class="section-header" onclick="toggleSection('scenario-section')">
            <span class="chevron">▼</span>
            <span class="section-title">Scenario: ${escapeHtml(scenario.name || 'Unknown')}</span>
            <span class="type-badge">${escapeHtml(scenario.type || 'happy_path')}</span>
        </div>
        <div class="section-content">
            <div class="scenario-steps">
                ${formatSteps(scenario.steps || '')}
            </div>
        </div>
    </div>

    <!-- TEST METHOD SECTION -->
    <div class="section main-section" id="test-section">
        <div class="section-header" onclick="toggleSection('test-section')">
            <span class="chevron">▼</span>
            <span class="section-title">Test: ${escapeHtml(test.method || 'Unknown')}</span>
            <span class="section-meta">${escapeHtml(test.file || '')}:${test.line || ''}</span>
            ${test.file ? `<button class="open-file-btn" onclick="event.stopPropagation(); openFile('${escapeHtml(test.file)}', ${test.line || 1})">Open</button>` : ''}
        </div>
        <div class="section-content">
            <div class="monaco-container" style="height: 300px;" data-file="${escapeHtml(test.file || '')}" data-line="${test.line || 1}" data-editable="true" data-code="${Buffer.from(test.code || '// No test code').toString('base64')}"></div>
        </div>
    </div>

    <!-- CODE SECTIONS (nested) - starts collapsed -->
    <div class="section main-section collapsed" id="code-root">
        <div class="section-header" onclick="toggleSection('code-root')">
            <span class="chevron">▼</span>
            <span class="section-title">Code Trace</span>
            <span class="section-meta">${code.length} top-level calls</span>
        </div>
        <div class="section-content">
            ${code.map((c, i) => renderCodeSection(c, i)).join('')}
        </div>
    </div>

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
        buildSymbolMap(${JSON.stringify(code)});
        // Add test section as navigable
        if (!symbolMap['${escapeHtml(test.method || '')}']) symbolMap['${escapeHtml(test.method || '')}'] = [];
        symbolMap['${escapeHtml(test.method || '')}'].push('test-section');
        
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
            // Initial height estimate - will be adjusted after editor renders
            const lineCount = (code.match(/\\n/g) || []).length + 1;
            const initialHeight = Math.min(Math.max(lineCount * 19 + 20, 60), 500);
            container.style.height = initialHeight + 'px';
            container.style.display = 'block';
            
            const startLineNum = parseInt(line, 10) || 1;
            const editor = monaco.editor.create(container, {
                value: code,
                language: 'python',
                theme: getMonacoTheme(),  // Match VS Code theme
                readOnly: !isEditable,
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                lineNumbers: (n) => String(n + startLineNum - 1),  // Show actual source line numbers
                lineNumbersMinChars: 4,
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
            
            // Add decorations for method calls that have sections
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
            
            // Save function - used by blur and Ctrl+S
            function saveEditorContent() {
                const newCode = editor.getValue();
                const originalCode = container.dataset.originalCode || code;
                if (newCode !== originalCode) {
                    console.log('Saving changes to:', file, 'line:', line);
                    vscode.postMessage({
                        command: 'saveCode',
                        file: file,
                        line: parseInt(line, 10),
                        originalCode: originalCode,
                        newCode: newCode
                    });
                    container.dataset.originalCode = newCode;
                }
            }
            
            if (isEditable) {
                // Save on blur (tab away or click away)
                editor.onDidBlurEditorWidget(saveEditorContent);
                
                // Save on Ctrl+S (Windows/Linux) or Cmd+S (Mac)
                editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, saveEditorContent);
                
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
                
                lazyCode.classList.add('loaded');
            } else if (message.command === 'codeSaved') {
                console.log('Code saved successfully:', message.file);
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
