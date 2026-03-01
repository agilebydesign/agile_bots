window.createEpic = function() {
    console.log('═══════════════════════════════════════════════════════');
    console.log('[WebView] createEpic CALLED');
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] createEpic called'
    });
    

    if (typeof window.handleCreateNode === 'function') {
        console.log('[WebView] Using optimistic create handler');
        window.handleCreateNode({
            parentPath: 'story_graph',
            nodeType: 'epic'

        });
    } else {
        console.warn('[WebView] handleCreateNode not available, falling back to direct command');
        vscode.postMessage({
            command: 'executeCommand',
            commandText: 'story_graph.create_epic',
            optimistic: true
        });
    }
    console.log('[WebView] postMessage sent successfully');
    console.log('═══════════════════════════════════════════════════════');
};

window.createSubEpic = function(parentName) {
    console.log('[WebView] createSubEpic called for:', parentName);
    vscode.postMessage({
        command: 'executeCommand',
        commandText: `story_graph."${parentName}".create`,
        optimistic: true
    });
};

window.createStory = function(parentName) {
    console.log('[WebView] createStory called for:', parentName);
    vscode.postMessage({
        command: 'executeCommand',
        commandText: `story_graph."${parentName}".create_story`,
        optimistic: true
    });
};

window.createScenario = function(storyName) {
    console.log('[WebView] createScenario called for:', storyName);
    vscode.postMessage({
        command: 'executeCommand',
        commandText: `story_graph."${storyName}".create_scenario`,
        optimistic: true
    });
};

window.createScenarioOutline = function(storyName) {
    console.log('[WebView] createScenarioOutline called for:', storyName);
    console.log('[WebView] Note: ScenarioOutline deprecated, creating Scenario instead');
    vscode.postMessage({
        command: 'executeCommand',
        commandText: `story_graph."${storyName}".create_scenario`,
        optimistic: true
    });
};

window.createAcceptanceCriteria = function(storyName) {
    console.log('[WebView] createAcceptanceCriteria called for:', storyName);
    vscode.postMessage({
        command: 'executeCommand',
        commandText: `story_graph."${storyName}".create_acceptance_criteria`,
        optimistic: true
    });
};

window.deleteNode = function(nodePath) {
    console.log('[WebView] deleteNode called for:', nodePath);
    

    if (typeof window.handleDeleteNode === 'function') {
        console.log('[WebView] Using optimistic delete handler');
        window.handleDeleteNode({
            nodePath: nodePath
        });
    } else {
        console.warn('[WebView] handleDeleteNode not available, falling back to direct command');

        vscode.postMessage({
            command: 'executeCommand',
            commandText: nodePath + '.delete'

        });
    }
};

window.deleteNodeIncludingChildren = function(nodePath) {
    console.log('[WebView] deleteNodeIncludingChildren called for:', nodePath);
    


    if (typeof window.handleDeleteNode === 'function') {
        console.log('[WebView] Using optimistic delete handler (always includes children)');
        window.handleDeleteNode({
            nodePath: nodePath
        });
    } else {
        console.warn('[WebView] handleDeleteNode not available, falling back to direct command');


        vscode.postMessage({
            command: 'executeCommand',
            commandText: nodePath + '.delete()'

        });
    }
};

window.enableEditMode = function(nodePath) {
    console.log('[ASYNC_SAVE] ========== RENAME OPERATION START ==========');
    console.log('[ASYNC_SAVE] [USER_ACTION] User double-clicked node to rename nodePath=' + nodePath + ' timestamp=' + new Date().toISOString());


    const matches = nodePath.match(/"([^"]+)"[^"]*$/);
    const currentName = matches ? matches[1] : '';
    
    console.log('[ASYNC_SAVE] [USER_ACTION] Extracted current name currentName=' + currentName);
    console.log('[ASYNC_SAVE] [USER_ACTION] Sending renameNode message to extension host');
    vscode.postMessage({
        command: 'renameNode',
        nodePath: nodePath,
        currentName: currentName
    });
    console.log('[ASYNC_SAVE] ========== RENAME OPERATION INITIATED ==========');
};

function updateNodePositions(container) {
    const nodes = Array.from(container.children).filter(child => 
        child.classList.contains('story-node') || 
        (child.querySelector && child.querySelector('.story-node'))
    );
    nodes.forEach((node, index) => {
        const storyNode = node.classList.contains('story-node') ? node : node.querySelector('.story-node');
        if (storyNode) {
            storyNode.setAttribute('data-position', index.toString());
        }
    });
}

function applyOptimisticMove(draggedNodeElement, targetElement, dropZone, finalPosition) {
    var draggedNodeName = draggedNodeElement ? draggedNodeElement.getAttribute('data-node-name') : null;
    var targetNodeName = targetElement ? targetElement.getAttribute('data-node-name') : null;
    console.log('[ASYNC_SAVE] [OPTIMISTIC] applyOptimisticMove() called dropZone=' + dropZone + ' finalPosition=' + finalPosition + ' draggedNode=' + draggedNodeName + ' targetNode=' + targetNodeName + ' timestamp=' + new Date().toISOString());
    
    if (!draggedNodeElement || !targetElement) {
        console.error('[ASYNC_SAVE] [OPTIMISTIC] [ERROR] Cannot apply optimistic move - missing elements hasDraggedElement=' + !!draggedNodeElement + ' hasTargetElement=' + !!targetElement);
        return;
    }
    

    const draggedParent = draggedNodeElement.parentElement;
    const targetParent = dropZone === 'inside' ? targetElement : targetElement.parentElement;
    
    console.log('[ASYNC_SAVE] [OPTIMISTIC] Found parent elements hasDraggedParent=' + !!draggedParent + ' hasTargetParent=' + !!targetParent + ' sameParent=' + (draggedParent === targetParent));
    
    if (!draggedParent || !targetParent) {
        console.error('[ASYNC_SAVE] [OPTIMISTIC] [ERROR] Cannot apply optimistic move - missing parent elements');
        return;
    }
    

    if (draggedParent === targetParent && dropZone === 'after') {
        const targetPos = parseInt(targetElement.getAttribute('data-position') || '0');
        const draggedPos = parseInt(draggedNodeElement.getAttribute('data-position') || '0');
        
        console.log('[ASYNC_SAVE] [OPTIMISTIC] Moving within same parent draggedPos=' + draggedPos + ' targetPos=' + targetPos + ' finalPosition=' + finalPosition + ' dropZone=' + dropZone);
        

        const draggedClone = draggedNodeElement.cloneNode(true);
        draggedNodeElement.remove();
        console.log('[ASYNC_SAVE] [OPTIMISTIC] Removed dragged node from original position');
        

        const children = Array.from(targetParent.children).filter(child => 
            child.classList.contains('story-node') || 
            child.querySelector && child.querySelector('.story-node')
        );
        
        console.log('[ASYNC_SAVE] [OPTIMISTIC] Found children childrenCount=' + children.length);
        
        let insertIndex = finalPosition;
        if (insertIndex >= children.length) {
            targetParent.appendChild(draggedClone);
            console.log('[ASYNC_SAVE] [OPTIMISTIC] Appended to end');
        } else {
            const insertBefore = children[insertIndex];
            if (insertBefore) {
                targetParent.insertBefore(draggedClone, insertBefore);
                console.log('[ASYNC_SAVE] [OPTIMISTIC] Inserted before child at index', insertIndex);
            } else {
                targetParent.appendChild(draggedClone);
                console.log('[ASYNC_SAVE] [OPTIMISTIC] Fallback: appended to end');
            }
        }
        
        updateNodePositions(targetParent);
        
        console.log('[ASYNC_SAVE] [OPTIMISTIC] [SUCCESS] Optimistic move applied - node moved in DOM');
        } else if (dropZone === 'inside') {

        console.log('[ASYNC_SAVE] [OPTIMISTIC] Moving to inside container - will rely on backend refresh');
        } else {
        console.warn('[ASYNC_SAVE] [OPTIMISTIC] Unhandled move scenario dropZone=' + dropZone + ' sameParent=' + (draggedParent === targetParent));
    }
}

function _applyIncrementCollapse(col, collapse) {
    var body = col.querySelector('.increment-stories-body');
    var btn = col.querySelector('button[title="Collapse / expand"]');
    if (collapse) {
        col.setAttribute('data-collapsed', 'true');
        col.style.minWidth = '28px';
        col.style.maxWidth = '28px';
        col.style.overflowY = 'hidden';
        if (body) body.style.display = 'none';
        if (btn) btn.textContent = '▶';
    } else {
        col.setAttribute('data-collapsed', 'false');
        col.style.minWidth = '160px';
        col.style.maxWidth = '200px';
        col.style.overflowY = 'auto';
        if (body) body.style.display = 'flex';
        if (btn) btn.textContent = '▼';
    }
}

window.toggleIncrementCollapse = function(col) {
    if (!col) return;
    var incName = col.getAttribute('data-inc');
    var collapsed = col.getAttribute('data-collapsed') === 'true';
    _applyIncrementCollapse(col, !collapsed);

    try {
        var state = vscode.getState() || {};
        if (!state.collapsedIncrements) state.collapsedIncrements = {};
        if (!collapsed) {
            state.collapsedIncrements[incName] = true;
        } else {
            delete state.collapsedIncrements[incName];
        }
        vscode.setState(state);
    } catch(_) {}
};

(function restoreIncrementCollapseState() {
    try {
        var state = vscode.getState() || {};
        var collapsed = state.collapsedIncrements || {};
        Object.keys(collapsed).forEach(function(incName) {
            var col = document.querySelector('.increment-column-container[data-inc="' + incName + '"]');
            if (col) _applyIncrementCollapse(col, true);
        });
    } catch(_) {}
})();

window.selectIncrement = function(name, behaviorNeeded) {
    window.selectNode('increment', name, { name: name, path: 'story_graph.increments."' + name + '"', behavior: behaviorNeeded || 'shape' });
    document.querySelectorAll('.increment-column-container').forEach(function(col) {
        col.classList.toggle('selected', col.getAttribute('data-inc') === name);
    });
};

window.addIncrement = function() {
    var wrapper = document.querySelector('.increment-columns-wrapper');
    if (!wrapper) { console.error('[INCREMENT] Cannot find .increment-columns-wrapper'); return; }


    var selectedCol = wrapper.querySelector('.increment-column-container.selected');

    var col = document.createElement('div');
    col.className = 'increment-column-container selected';
    col.style.cssText = 'min-width:160px;max-width:200px;flex-shrink:0;border-right:1px solid var(--text-color-faded,#444);padding:8px;display:flex;flex-direction:column;border-top:2px solid var(--accent-color);';
    col.innerHTML = '<div style="display:flex;align-items:center;gap:4px;margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid var(--text-color-faded,#555);">' +
        '<span contenteditable="true" style="flex:1;font-weight:600;font-size:12px;outline:none;min-width:0;color:var(--accent-color);">New Increment</span></div>' +
        '<div style="font-size:11px;color:var(--text-color-faded);font-style:italic;">(no stories)</div>';

    if (selectedCol) {
        selectedCol.insertAdjacentElement('afterend', col);
    } else {
        wrapper.appendChild(col);
    }

    var span = col.querySelector('span[contenteditable]');
    span.focus();
    document.execCommand('selectAll', false, null);

    var committed = false;
    function commit() {
        if (committed) return;
        committed = true;
        var name = span.innerText.trim();
        if (!name || name === 'New Increment') { col.remove(); return; }

        span.contentEditable = 'false';
        span.style.color = '';
        col.style.borderTop = '';
        col.style.opacity = '0.6';
        var afterName = selectedCol ? selectedCol.getAttribute('data-inc') : null;
        _incCmd('story_graph.add_increment name:"' + name + '"' + (afterName ? ' after:"' + afterName + '"' : ''));
    }

    span.addEventListener('blur', commit, { once: true });
    span.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') { e.preventDefault(); span.blur(); }
        if (e.key === 'Escape') { span.innerText = ''; span.blur(); }
    });
};


window.deleteIncrement = function(incrementName) {
    var col = document.querySelector('.increment-column-container[data-inc="' + incrementName + '"]');
    if (col) col.remove();
    _incCmd('story_graph.remove_increment increment_name:"' + incrementName + '"');
};


window.renameIncrement = function(el, oldName) {
    var newName = el.innerText.trim();
    if (!newName || newName === oldName) { el.innerText = oldName; return; }
    el.setAttribute('data-increment-name', newName);
    el.closest('.increment-column-container').setAttribute('data-inc', newName);
    _incCmd('story_graph.rename_increment from_name:"' + oldName + '" to_name:"' + newName + '"');
};


window.removeStoryFromIncrement = function(incrementName, storyName) {
    var col = document.querySelector('.increment-column-container[data-inc="' + incrementName + '"]');
    if (col) {
        col.querySelectorAll('[data-story]').forEach(function(row) {
            if (row.getAttribute('data-story') === storyName) row.closest('div').remove();
        });
    }
    _incCmd('story_graph.remove_story_from_increment increment_name:"' + incrementName + '" story_name:"' + storyName + '"');
};

function _incrementDropPosition(incColEl, mouseY) {
    if (mouseY === undefined || mouseY === null || !incColEl) return undefined;
    var rows = Array.from(incColEl.querySelectorAll('.story-node[data-inc-source]'));
    if (!rows.length) return 0;
    for (var i = 0; i < rows.length; i++) {
        var rect = rows[i].getBoundingClientRect();
        var mid = rect.top + rect.height / 2;
        if (mouseY < mid) return i;
    }
    return rows.length;
}

window.addStoryToIncrement = function(incrementName, storyName, position) {
    var cmd = 'story_graph.add_story_to_increment increment_name:"' + incrementName + '" story_name:"' + storyName + '"';
    if (position !== undefined && position !== null) cmd += ' position:' + position;
    _incCmd(cmd);
};

window.selectedNode = {
    type: 'root',
    name: null,
    path: null,
    canHaveSubEpic: false,
    canHaveStory: false,
    canHaveTests: false,
    hasChildren: false,
    hasStories: false,
    hasNestedSubEpics: false
};

window.selectNode = function(type, name, options = {}) {
    console.log('═══════════════════════════════════════════════════════');
    console.log('[WebView] selectNode CALLED');
    console.log('[WebView]   type:', type);
    console.log('[WebView]   name:', name);
    console.log('[WebView]   options:', JSON.stringify(options, null, 2));
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] selectNode: type=' + type + ', name=' + name + ', options=' + JSON.stringify(options)
    });
    

    document.querySelectorAll('.story-node.selected').forEach(node => {
        node.classList.remove('selected');
    });
    document.querySelectorAll('.increment-column-container.selected').forEach(col => {
        col.classList.remove('selected');
    });
    

    let targetNode = null;
    

    if (options.path) {
        const allNodes = document.querySelectorAll('.story-node[data-path]');
        for (const node of allNodes) {
            if (node.getAttribute('data-path') === options.path) {
                targetNode = node;
                console.log('[WebView]   Found node by path:', options.path);
                break;
            }
        }
    }
    

    if (!targetNode) {
        const nodeName = name || 'Story Map';
        targetNode = document.querySelector('.story-node[data-node-type="' + type + '"][data-node-name="' + nodeName + '"]');
        console.log('[WebView]   Found node by type+name:', type, nodeName);
    }
    
    if (targetNode) {
        targetNode.classList.add('selected');
        console.log('[WebView]   Added selected class to node');
    } else {
        console.log('[WebView]   WARNING: Target node not found');
    }
    

    const behavior = window.currentBehavior || options.behavior || null;
    const behaviors = options.behaviors || (options.behavior ? [options.behavior] : []);
    
    window.selectedNode = {
        type: type,
        name: name,
        path: options.path || null,
        behavior: behavior,
        behaviorNeeded: options.behavior || null,
        behaviorsNeeded: behaviors,
        canHaveSubEpic: options.canHaveSubEpic || false,
        canHaveStory: options.canHaveStory || false,
        canHaveTests: options.canHaveTests || false,
        hasChildren: options.hasChildren || false,
        hasStories: options.hasStories || false,
        hasNestedSubEpics: options.hasNestedSubEpics || false
    };
    console.log('[WebView]   window.selectedNode updated:', JSON.stringify(window.selectedNode, null, 2));
    console.log('');
    console.log('[NODE CLICK DEBUG] ═══════════════════════════════════════');
    console.log('[NODE CLICK DEBUG] Node clicked:', name);
    console.log('[NODE CLICK DEBUG] Node type:', type);
    console.log('[NODE CLICK DEBUG] Current behavior from bot:', window.currentBehavior || '(none)');
    console.log('[NODE CLICK DEBUG] behavior_needed from node:', options.behavior || '(none)');
    console.log('[NODE CLICK DEBUG] Using behavior:', behavior || '(none)');
    if (!behavior) {
        console.log('[NODE CLICK DEBUG] ⚠️ WARNING: No current behavior - submit button will not show');
    }
    console.log('[NODE CLICK DEBUG] ═══════════════════════════════════════');
    console.log('');
    
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] window.selectedNode.behavior_needed set to: "' + window.selectedNode.behavior + '" for node: ' + name
    });
    

    try {
        sessionStorage.setItem('selectedNode', JSON.stringify(window.selectedNode));
    } catch (err) {
        console.error('[WebView] Error saving selection:', err);
    }
    
    window.updateContextualButtons();
    console.log('[WebView]   updateContextualButtons called');
    console.log('═══════════════════════════════════════════════════════');
};

function resolveNodePath(selectedNode) {
    if (selectedNode.path && selectedNode.path.length > 'story_graph.'.length) {
        return selectedNode.path;
    }
    const nodes = document.querySelectorAll('.story-node[data-path]');
    for (var i = 0; i < nodes.length; i++) {
        var el = nodes[i];
        if (el.getAttribute('data-node-type') === selectedNode.type && el.getAttribute('data-node-name') === selectedNode.name) {
            var path = el.getAttribute('data-path');
            if (path) {
                console.log('[WebView] Resolved path from DOM:', path);
                selectedNode.path = path;
                return path;
            }
        }
    }
    return null;
}

window.handleDelete = function() {
    console.log('[WebView] handleDelete called for node:', window.selectedNode);
    
    if (!window.selectedNode || !window.selectedNode.name) {
        console.error('[WebView] ERROR: No node selected for delete');
        return;
    }
    

    let nodePath = window.selectedNode.path;
    if (!nodePath || nodePath.length <= 'story_graph.'.length) {

        nodePath = `story_graph."${window.selectedNode.name}"`;
    }
    
    console.log('[WebView] Calling handleDeleteNode with path:', nodePath);
    


    if (typeof window.handleDeleteNode === 'function') {
        window.handleDeleteNode({
            nodePath: nodePath
        });
    } else {
        console.warn('[WebView] handleDeleteNode not available, falling back to direct command');


        const commandText = nodePath + '.delete()';
        vscode.postMessage({
            command: 'executeCommand',
            commandText: commandText
        });
    }
};

window.updateContextualButtons = function() {
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] updateContextualButtons called, selectedNode=' + JSON.stringify(window.selectedNode)
    });
    
    const btnCreateEpic = document.getElementById('btn-create-epic');
    const btnCreateSubEpic = document.getElementById('btn-create-sub-epic');
    const btnCreateStory = document.getElementById('btn-create-story');
    const btnCreateScenario = document.getElementById('btn-create-scenario');
    const btnCreateAcceptanceCriteria = document.getElementById('btn-create-acceptance-criteria');
    const btnDelete = document.getElementById('btn-delete');
    const btnScopeTo = document.getElementById('btn-scope-to');
    const btnSubmit = document.getElementById('btn-submit');
    const btnOpenGraph = document.getElementById('btn-open-graph') || document.getElementById('ws-btn-open-graph');
    const btnOpenAll = document.getElementById('btn-open-all') || document.getElementById('ws-btn-open-all');
    const btnOpenFile = document.getElementById('ws-btn-open-file');
    const btnOpenTest = document.getElementById('ws-btn-open-test');
    

    if (btnCreateEpic) btnCreateEpic.style.display = 'none';
    if (btnCreateSubEpic) btnCreateSubEpic.style.display = 'none';
    if (btnCreateStory) btnCreateStory.style.display = 'none';
    if (btnCreateScenario) btnCreateScenario.style.display = 'none';
    if (btnCreateAcceptanceCriteria) btnCreateAcceptanceCriteria.style.display = 'none';
    if (btnDelete) btnDelete.style.display = 'none';
    if (btnScopeTo) btnScopeTo.style.display = 'none';
    if (btnSubmit) btnSubmit.style.display = 'none';
    if (btnOpenGraph) btnOpenGraph.style.display = 'none';
    if (btnOpenAll) btnOpenAll.style.display = 'none';
    if (btnOpenFile) btnOpenFile.style.display = 'none';
    if (btnOpenTest) btnOpenTest.style.display = 'none';


    if (window.selectedNode.type === 'root') {
        if (btnCreateEpic) btnCreateEpic.style.display = 'block';
    } else if (window.selectedNode.type === 'epic') {
        if (btnCreateSubEpic) btnCreateSubEpic.style.display = 'block';
        if (btnDelete) btnDelete.style.display = 'block';
        if (btnScopeTo) btnScopeTo.style.display = 'block';
    } else if (window.selectedNode.type === 'sub-epic') {




        if (window.selectedNode.hasStories) {

            if (btnCreateStory) btnCreateStory.style.display = 'block';
        } else if (window.selectedNode.hasNestedSubEpics) {

            if (btnCreateSubEpic) btnCreateSubEpic.style.display = 'block';
        } else {

            if (btnCreateSubEpic) btnCreateSubEpic.style.display = 'block';
            if (btnCreateStory) btnCreateStory.style.display = 'block';
        }
        if (btnDelete) btnDelete.style.display = 'block';
        if (btnScopeTo) btnScopeTo.style.display = 'block';
    } else if (window.selectedNode.type === 'story') {

        if (btnCreateScenario) btnCreateScenario.style.display = 'block';
        if (btnCreateAcceptanceCriteria) btnCreateAcceptanceCriteria.style.display = 'block';
        if (btnDelete) btnDelete.style.display = 'block';
        if (btnScopeTo) btnScopeTo.style.display = 'block';
    } else if (window.selectedNode.type === 'scenario') {

        if (btnDelete) btnDelete.style.display = 'block';
        if (btnScopeTo) btnScopeTo.style.display = 'block';

    } else if (window.selectedNode.type === 'increment') {
        if (btnScopeTo) btnScopeTo.style.display = 'block';
    }
    

    // Open Graph and Open All work on entire story graph - always show them (including when root selected)
    if (btnOpenGraph) btnOpenGraph.style.display = 'block';
    if (btnOpenAll) btnOpenAll.style.display = 'block';
    // File and Test buttons: show when non-root and selected node has file/test link
    const fileLink = getSelectedNodeFileLink && getSelectedNodeFileLink();
    const testFiles = getSelectedNodeTestFiles && getSelectedNodeTestFiles();
    if (btnOpenFile) btnOpenFile.style.display = (window.selectedNode.type !== 'root' && fileLink) ? 'block' : 'none';
    if (btnOpenTest) btnOpenTest.style.display = (window.selectedNode.type !== 'root' && testFiles && testFiles.length > 0) ? 'block' : 'none';
    
    var diagramActionGroup = document.getElementById('diagram-action-buttons-group');
    if (diagramActionGroup) {
        diagramActionGroup.style.display = (window.selectedNode.type !== 'root') ? 'flex' : 'none';
    }

    var dScope = (window.selectedNode.type !== 'root' && window.selectedNode.name)
        ? window.selectedNode.name : '';
    window.diagramScope = dScope;

    var wsSubmitBtn = document.getElementById('ws-submit-btn');
    if (wsSubmitBtn) {
        var bhv = (window.currentBehavior || '').charAt(0).toUpperCase() + (window.currentBehavior || '').slice(1);
        var scope = (window.selectedNode.type !== 'root' && window.selectedNode.name) ? window.selectedNode.name : 'all';
        wsSubmitBtn.title = 'Submit ' + bhv + ' for ' + scope;
    }
    
    var bhv = window.currentBehavior || 'shape';
    var renderBtns = document.querySelectorAll('.render-button');
    for (var ri = 0; ri < renderBtns.length; ri++) {
        renderBtns[ri].title = dScope ? 'Render ' + bhv + ' diagram for "' + dScope + '"' : 'Render ' + bhv + ' diagram';
    }
    var saveBtns = document.querySelectorAll('.save-layout-button');
    for (var si = 0; si < saveBtns.length; si++) {
        saveBtns[si].title = dScope ? 'Save ' + bhv + ' diagram layout for "' + dScope + '"' : 'Save ' + bhv + ' diagram layout';
    }
    var clearBtns = document.querySelectorAll('.clear-layout-button');
    for (var ci = 0; ci < clearBtns.length; ci++) {
        clearBtns[ci].title = dScope ? 'Clear ' + bhv + ' diagram layout for "' + dScope + '"' : 'Clear ' + bhv + ' diagram layout';
    }
    var reportBtns = document.querySelectorAll('.generate-report-button');
    for (var gi = 0; gi < reportBtns.length; gi++) {
        reportBtns[gi].title = dScope ? 'Generate ' + bhv + ' report for "' + dScope + '"' : 'Generate ' + bhv + ' report';
    }
    var updateBtns = document.querySelectorAll('.update-button');
    for (var ui = 0; ui < updateBtns.length; ui++) {
        updateBtns[ui].title = dScope ? 'Update graph from ' + bhv + ' diagram for "' + dScope + '"' : 'Update graph from ' + bhv + ' diagram';
    }
    

    var scopeSlug = dScope ? dScope.toLowerCase().split(' ').join('-').split('').filter(function(c) {
        return (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') || c === '-';
    }).join('') : '';
    var diagLinks = document.querySelectorAll('.diagram-link');
    for (var di = 0; di < diagLinks.length; di++) {
        var origName = diagLinks[di].getAttribute('data-original-name') || '';
        if (scopeSlug && origName) {
            if (origName.indexOf('-all.drawio') !== -1) {
                diagLinks[di].textContent = origName.split('-all.drawio').join('-' + scopeSlug + '.drawio');
            } else {
                diagLinks[di].textContent = origName.split('.drawio').join('-' + scopeSlug + '.drawio');
            }
        } else if (origName) {
            diagLinks[di].textContent = origName;
        }
    }
    

    console.log('═══════════════════════════════════════════════════════');
    console.log('[SUBMIT BUTTON DEBUG] Starting submit button update');
    console.log('[SUBMIT BUTTON DEBUG] Node clicked:', window.selectedNode.name);
    console.log('[SUBMIT BUTTON DEBUG] Node type:', window.selectedNode.type);
    console.log('[SUBMIT BUTTON DEBUG] Current behavior from bot:', window.currentBehavior || '(none)');
    console.log('[SUBMIT BUTTON DEBUG] Current action from bot:', window.currentAction || '(none)');
    console.log('[SUBMIT BUTTON DEBUG] behavior_needed from node:', window.selectedNode.behaviorNeeded || '(none)');
    console.log('[SUBMIT BUTTON DEBUG] btnSubmit exists:', !!btnSubmit);
    console.log('[SUBMIT BUTTON DEBUG] Is root?', window.selectedNode.type === 'root');
    console.log('[SUBMIT BUTTON DEBUG] Has behaviorNeeded?', !!window.selectedNode.behaviorNeeded);
    

    const requiredBehavior = window.selectedNode.behaviorNeeded;
    const currentBehavior = window.currentBehavior || window.selectedNode.behavior;
    const currentAction = window.currentAction || 'build';
    // For increments: use current behavior (no behaviorNeeded on increment nodes)
    const effectiveBehavior = window.selectedNode.type === 'increment' ? currentBehavior : requiredBehavior;
    
    if (btnSubmit && window.selectedNode.type !== 'root' && effectiveBehavior) {
        const behavior = effectiveBehavior;
        const action = currentAction;
        const nodeType = window.selectedNode.type;
        const btnSubmitIcon = document.getElementById('btn-submit-icon');
        
        console.log('[SUBMIT BUTTON DEBUG] Proceeding with button update...');
        console.log('[SUBMIT BUTTON DEBUG] btnSubmitIcon exists:', !!btnSubmitIcon);
        

        const behaviorMap = {
            'shape': {
                icon: btnSubmit.getAttribute('data-shape-icon'),
                tooltip: btnSubmit.getAttribute('data-shape-tooltip') || 'Submit shape instructions for ' + nodeType
            },
            'exploration': {
                icon: btnSubmit.getAttribute('data-exploration-icon'),
                tooltip: btnSubmit.getAttribute('data-exploration-tooltip') || 'Submit exploration instructions for ' + nodeType
            },
            'scenarios': {
                icon: btnSubmit.getAttribute('data-scenarios-icon'),
                tooltip: btnSubmit.getAttribute('data-scenarios-tooltip') || 'Submit scenarios instructions for ' + nodeType
            },
            'tests': {
                icon: btnSubmit.getAttribute('data-tests-icon'),
                tooltip: btnSubmit.getAttribute('data-tests-tooltip') || 'Submit tests instructions for ' + nodeType
            },
            'code': {
                icon: btnSubmit.getAttribute('data-code-icon'),
                tooltip: btnSubmit.getAttribute('data-code-tooltip') || 'Submit code instructions for ' + nodeType
            }
        };
        
        console.log('[SUBMIT BUTTON DEBUG] Behavior map created for all behaviors');
        console.log('[SUBMIT BUTTON DEBUG] Looking up behavior:', behavior);
        
        const behaviorConfig = behaviorMap[behavior];
        console.log('[SUBMIT BUTTON DEBUG] Behavior config found:', !!behaviorConfig);
        
        if (behaviorConfig) {
            console.log('[SUBMIT BUTTON DEBUG] ✓ Behavior config exists');
            console.log('[SUBMIT BUTTON DEBUG] Image icon path:', behaviorConfig.icon);
            console.log('[SUBMIT BUTTON DEBUG] Hover tooltip:', behaviorConfig.tooltip);
        } else {
            console.log('[SUBMIT BUTTON DEBUG] ✗ No behavior config found for:', behavior);
            console.log('[SUBMIT BUTTON DEBUG] Available behaviors:', Object.keys(behaviorMap));
        }
        
        if (behaviorConfig && btnSubmitIcon) {
            btnSubmitIcon.src = behaviorConfig.icon;
            btnSubmit.title = behaviorConfig.tooltip;
            btnSubmit.style.display = 'block';
            
            console.log('[SUBMIT BUTTON DEBUG] ✓ Submit button updated successfully');
            console.log('[SUBMIT BUTTON DEBUG] ✓ Icon src set to:', behaviorConfig.icon);
            console.log('[SUBMIT BUTTON DEBUG] ✓ Tooltip set to:', behaviorConfig.tooltip);
            console.log('[SUBMIT BUTTON DEBUG] ✓ Button displayed');
            
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] Submit button updated: behavior=' + behavior + ', nodeType=' + nodeType + ', icon=' + behaviorConfig.icon + ', tooltip="' + behaviorConfig.tooltip + '"'
            });
        } else {
            if (!behaviorConfig) {
                console.log('[SUBMIT BUTTON DEBUG] ✗ Missing behaviorConfig');
            }
            if (!btnSubmitIcon) {
                console.log('[SUBMIT BUTTON DEBUG] ✗ Missing btnSubmitIcon element');
            }
        }
    } else {
        console.log('[SUBMIT BUTTON DEBUG] Submit button NOT updated - conditions not met:');
        if (!btnSubmit) {
            console.log('[SUBMIT BUTTON DEBUG] ✗ btnSubmit element not found');
        }
        if (window.selectedNode.type === 'root') {
            console.log('[SUBMIT BUTTON DEBUG] ✗ Node is root (submit not shown for root)');
        }
        if (!effectiveBehavior) {
            console.log('[SUBMIT BUTTON DEBUG] ✗ No behavior for submit');
            if (window.selectedNode.type === 'increment') {
                console.log('[SUBMIT BUTTON DEBUG]   Increment needs current behavior from bot');
            } else {
                console.log('[SUBMIT BUTTON DEBUG]   behavior_needed may not be set on node');
            }
        }
    }
    

    const btnSubmitAlt = document.getElementById('btn-submit-alt');
    const behaviorsNeeded = window.selectedNode.behaviorsNeeded || [];
    console.log('[SUBMIT BUTTON DEBUG] behaviorsNeeded:', behaviorsNeeded);
    
    if (btnSubmitAlt && behaviorsNeeded.length > 1 && window.selectedNode.type !== 'root') {
        const altBehavior = behaviorsNeeded[1];
        const nodeType = window.selectedNode.type;
        const btnSubmitAltIcon = document.getElementById('btn-submit-alt-icon');
        

        const altBehaviorMap = {
            'shape': {
                icon: btnSubmitAlt.getAttribute('data-shape-icon'),
                tooltip: 'Submit shape instructions for ' + nodeType
            },
            'exploration': {
                icon: btnSubmitAlt.getAttribute('data-exploration-icon'),
                tooltip: 'Submit exploration instructions for ' + nodeType
            },
            'scenarios': {
                icon: btnSubmitAlt.getAttribute('data-scenarios-icon'),
                tooltip: 'Submit scenarios instructions for ' + nodeType
            },
            'tests': {
                icon: btnSubmitAlt.getAttribute('data-tests-icon'),
                tooltip: 'Submit tests instructions for ' + nodeType
            },
            'code': {
                icon: btnSubmitAlt.getAttribute('data-code-icon'),
                tooltip: 'Submit code instructions for ' + nodeType
            }
        };
        
        const altBehaviorConfig = altBehaviorMap[altBehavior];
        if (altBehaviorConfig && btnSubmitAltIcon) {
            btnSubmitAltIcon.src = altBehaviorConfig.icon;
            btnSubmitAlt.title = altBehaviorConfig.tooltip;
            btnSubmitAlt.style.display = 'block';

            btnSubmitAlt.setAttribute('data-current-behavior', altBehavior);
            console.log('[SUBMIT BUTTON DEBUG] Alt button shown for behavior:', altBehavior);
        } else {
            btnSubmitAlt.style.display = 'none';
        }
    } else if (btnSubmitAlt) {
        btnSubmitAlt.style.display = 'none';
    }
    
    console.log('═══════════════════════════════════════════════════════');
};


window.handleContextualCreate = function(actionType) {
    console.log('═══════════════════════════════════════════════════════');
    console.log('[WebView] handleContextualCreate CALLED');
    console.log('[WebView]   actionType:', actionType);
    console.log('[WebView]   window.selectedNode:', JSON.stringify(window.selectedNode, null, 2));
    
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] handleContextualCreate: ' + actionType + ' | selectedNode: ' + JSON.stringify(window.selectedNode)
    });
    
    if (!window.selectedNode.name) {
        console.error('[WebView] ERROR: No node name for contextual create');
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] ERROR: No node name for contextual create'
        });
        return;
    }
    

    const hasValidPath = window.selectedNode.path && 
                        window.selectedNode.path.length > 'story_graph.'.length &&
                        window.selectedNode.path.includes(window.selectedNode.name);
    
    console.log('[WebView]   path:', window.selectedNode.path);
    console.log('[WebView]   hasValidPath:', hasValidPath);
    

    if (typeof window.handleCreateNode === 'function') {
        var parentPath = hasValidPath ? window.selectedNode.path : `story_graph."${window.selectedNode.name}"`;
        
        console.log('[WebView] Using optimistic create handler for:', actionType);
        window.handleCreateNode({
            parentPath: parentPath,
            nodeType: actionType

        });
    } else {
        console.warn('[WebView] handleCreateNode not available, falling back to direct command');

        let commandText;
        switch(actionType) {
            case 'sub-epic':
                commandText = hasValidPath ? `${window.selectedNode.path}.create` : `story_graph."${window.selectedNode.name}".create`;
                break;
            case 'story':
                commandText = hasValidPath ? `${window.selectedNode.path}.create_story` : `story_graph."${window.selectedNode.name}".create_story`;
                break;
            case 'scenario':
                commandText = hasValidPath ? `${window.selectedNode.path}.create_scenario` : `story_graph."${window.selectedNode.name}".create_scenario`;
                break;
            case 'acceptance-criteria':
                commandText = hasValidPath ? `${window.selectedNode.path}.create_acceptance_criteria` : `story_graph."${window.selectedNode.name}".create_acceptance_criteria`;
                break;
        }
        
        if (commandText) {
            vscode.postMessage({
                command: 'executeCommand',
                commandText: commandText,
                optimistic: true
            });
        } else {
            console.error('[WebView] ERROR: No commandText generated');
        }
    }
    console.log('═══════════════════════════════════════════════════════');
};


window.handleScopeTo = function() {
    console.log('[WebView] handleScopeTo called for node:', window.selectedNode);
    
    if (!window.selectedNode.name) {
        console.error('[WebView] ERROR: No node selected for scope');
        return;
    }
    

    const nodeName = window.selectedNode.name;
    const nodeType = window.selectedNode.type;
    let scopeCommand;
    
    if (nodeType === 'story') {
        scopeCommand = 'story ' + nodeName;
    } else if (nodeType === 'sub-epic') {
        scopeCommand = 'subepic ' + nodeName;
    } else if (nodeType === 'epic') {
        scopeCommand = 'epic ' + nodeName;
    } else if (nodeType === 'increment') {
        scopeCommand = 'increment "' + nodeName + '"';
    } else {

        scopeCommand = nodeName;
    }
    
    console.log('[WebView] Scope To command:', scopeCommand);
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] SENDING SCOPE TO COMMAND: scope ' + scopeCommand
    });
    

    vscode.postMessage({
        command: 'executeCommand',
        commandText: 'scope ' + scopeCommand
    });
};

window.handleSubmit = function() {
    console.log('[WebView] ========== handleSubmit CALLED ==========');
    vscode.postMessage({
        command: 'logScopeDebug',
        message: 'handleSubmit CALLED | selectedNode=' + JSON.stringify(window.selectedNode || null)
    });
    
    if (!window.selectedNode || !window.selectedNode.name) {
        vscode.postMessage({ command: 'logScopeDebug', message: 'ERROR: No node selected' });
        return;
    }
    
    const nodeName = window.selectedNode.name;
    const nodeType = window.selectedNode.type;
    const action = 'build';
    let commandText;
    
    if (nodeType === 'increment') {
        if (!window.selectedNode.behaviorNeeded) {
            vscode.postMessage({ command: 'logScopeDebug', message: 'ERROR: No behaviorNeeded for increment ' + nodeName });
            return;
        }
        commandText = 'story_graph.submit_increment_instructions name:"' + nodeName + '" behavior:"' + window.selectedNode.behaviorNeeded + '" action:"' + action + '"';
    } else {
        if (!window.selectedNode.behaviorNeeded) {
            vscode.postMessage({ command: 'logScopeDebug', message: 'ERROR: No behaviorNeeded for ' + nodeName });
            return;
        }
        const nodePath = resolveNodePath(window.selectedNode);
        if (!nodePath) {
            vscode.postMessage({
                command: 'showScopeError',
                message: 'Scope not available: Could not resolve node path. Try clicking the story/epic node again, then submit.'
            });
            return;
        }
        commandText = nodePath + '.submit_required_behavior_instructions action:"' + action + '"';
    }
    
    vscode.postMessage({
        command: 'logScopeDebug',
        message: 'SENDING COMMAND: ' + commandText
    });
    
    vscode.postMessage({
        command: 'executeCommand',
        commandText: commandText
    });
};

window.handleSubmitAlt = function() {
    console.log('[WebView] ========== handleSubmitAlt CALLED ==========');
    console.log('[WebView] handleSubmitAlt called for node:', window.selectedNode);
    
    if (!window.selectedNode || !window.selectedNode.name) {
        console.error('[WebView] ERROR: No node selected for submit alt');
        return;
    }
    
    const behaviorsNeeded = window.selectedNode.behaviorsNeeded || [];
    if (behaviorsNeeded.length < 2) {
        console.error('[WebView] ERROR: No alternate behavior available');
        return;
    }
    
    const altBehavior = behaviorsNeeded[1];
    const nodeName = window.selectedNode.name;
    const nodeType = window.selectedNode.type;
    const action = 'build';
    let commandText;
    
    if (nodeType === 'increment') {
        commandText = 'story_graph.submit_increment_instructions name:"' + nodeName + '" behavior:"' + altBehavior + '" action:"' + action + '"';
    } else {
        const nodePath = resolveNodePath(window.selectedNode);
        if (!nodePath) {
            vscode.postMessage({ command: 'showScopeError', message: 'Scope not available: Could not resolve node path. Click the node again, then submit.' });
            return;
        }
        commandText = nodePath + '.submit_instructions behavior:"' + altBehavior + '" action:"' + action + '"';
    }
    
    console.log('[WebView] Executing command:', commandText);
    vscode.postMessage({
        command: 'executeCommand',
        commandText: commandText
    });
};

window.handleSubmitCurrent = function() {
    console.log('[WebView] ========== handleSubmitCurrent CALLED ==========');
    console.log('[WebView] handleSubmitCurrent called for node:', window.selectedNode);
    
    if (!window.selectedNode || !window.selectedNode.name) {
        console.error('[WebView] ERROR: No node selected for submit');
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] ERROR: handleSubmitCurrent called but no node selected'
        });
        return;
    }
    
    const nodeName = window.selectedNode.name;
    const behavior = window.currentBehavior || window.selectedNode.behaviorNeeded || null;
    let action = window.currentAction || 'build';
    const behaviorHeader = behavior && document.querySelector('[data-behavior="' + behavior + '"]');
    const behaviorContent = behaviorHeader && behaviorHeader.nextElementSibling;
    const isBehaviorCollapsed = behaviorContent && behaviorContent.classList && behaviorContent.classList.contains('collapsible-content') && behaviorContent.style.display === 'none';
    if (isBehaviorCollapsed) {
        action = 'first';
    }
    let commandText;
    
    if (window.selectedNode.type === 'increment') {
        // Increment uses story_graph.submit_increment_instructions (Increment has no submit_instructions)
        commandText = (behavior && action)
            ? 'story_graph.submit_increment_instructions name:"' + nodeName + '" behavior:"' + behavior + '" action:"' + action + '"'
            : 'story_graph.submit_increment_instructions name:"' + nodeName + '"';
    } else {
        const nodePath = resolveNodePath(window.selectedNode);
        if (!nodePath) {
            vscode.postMessage({ command: 'showScopeError', message: 'Scope not available: Could not resolve node path. Click the node again, then submit.' });
            return;
        }
        commandText = (behavior && action)
            ? nodePath + '.submit_instructions behavior:"' + behavior + '" action:"' + action + '"'
            : nodePath + '.submit_current_instructions';
    }
    
    console.log('[WebView] ========== SUBMIT CURRENT COMMAND ==========');
    console.log('[WebView] Command constructed:', commandText);
    console.log('[WebView] Using panel state: behavior=' + (behavior || '(bot current)') + ' action=' + (action || '(bot current)'));
    
    vscode.postMessage({
        command: 'executeCommand',
        commandText: commandText
    });
    
    console.log('[WebView] ========== COMMAND SENT ==========');
};

function getSelectedNodeFileLink() {
    if (!window.selectedNode || !window.selectedNode.name) return null;
    const nodeElement = document.querySelector('.story-node[data-node-type="' + window.selectedNode.type + '"][data-node-name="' + window.selectedNode.name + '"]');
    return nodeElement ? nodeElement.getAttribute('data-file-link') : null;
}

function getSelectedNodeTestFiles() {
    if (!window.selectedNode || !window.selectedNode.name) return [];
    const nodeElement = document.querySelector('.story-node[data-node-type="' + window.selectedNode.type + '"][data-node-name="' + window.selectedNode.name + '"]');
    const raw = nodeElement ? nodeElement.getAttribute('data-test-files') : null;
    if (!raw) return [];
    try {
        const arr = JSON.parse(raw);
        return Array.isArray(arr) ? arr : [];
    } catch (e) {
        return [];
    }
} 