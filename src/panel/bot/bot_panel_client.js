const vscode = acquireVsCodeApi();
console.log('[WebView] ========== SCRIPT LOADING ==========');
console.log('[WebView] vscode API acquired:', !!vscode);
console.log('[WebView] vscode.postMessage available:', typeof vscode.postMessage);



document.addEventListener('DOMContentLoaded', function() {
    try {

        const savedState = sessionStorage.getItem('collapseState');
        if (savedState) {
            const state = JSON.parse(savedState);

            setTimeout(() => window.restoreCollapseState(state), 50);
            console.log('[WebView] Restored collapse state for', Object.keys(state).length, 'nodes');
        }
        

        const savedSelection = sessionStorage.getItem('selectedNode');
        if (savedSelection) {
            const selection = JSON.parse(savedSelection);
            setTimeout(() => {
                if (window.selectNode) {
                    window.selectNode(selection.type, selection.name, selection);
                    console.log('[WebView] Restored selection for', selection.name);
                }
            }, 100);
        }

        if (window.currentBehavior && window.restoreWorkspaceCollapseState) {
            setTimeout(() => window.restoreWorkspaceCollapseState(window.currentBehavior), 50);
        }
        

        setTimeout(() => {
            if (window.restoreScrollPosition) {
                window.restoreScrollPosition();
            }
            if (window.expandClarifyBoxes) {
                window.expandClarifyBoxes();
            }
        }, 150);
    } catch (err) {
        console.error('[WebView] Error restoring state:', err);
    }
});


document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'hidden') {
        if (window.saveScrollPosition) {
            window.saveScrollPosition();
        }
    } else if (document.visibilityState === 'visible') {

        setTimeout(() => {
            if (window.restoreScrollPosition) {
                window.restoreScrollPosition();
            }
        }, 50);
    }
});


document.addEventListener('click', function(e) {
    const target = e.target;
    const targetInfo = {
        tagName: target.tagName,
        className: target.className,
        id: target.id,
        nodeType: target.getAttribute && target.getAttribute('data-node-type'),
        nodeName: target.getAttribute && target.getAttribute('data-node-name')
    };
    console.log('[WebView] CLICK DETECTED:', targetInfo);
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] CLICK: ' + JSON.stringify(targetInfo)
    });
    


    const storyNode = target.closest && target.closest('.story-node');
    if (storyNode) {
        console.log('═══════════════════════════════════════════════════════');
        console.log('[WebView] STORY NODE CLICKED');
        const nodeType = storyNode.getAttribute('data-node-type');
        const nodeName = storyNode.getAttribute('data-node-name');
        const hasChildren = storyNode.getAttribute('data-has-children') === 'true';
        const hasStories = storyNode.getAttribute('data-has-stories') === 'true';
        const hasNestedSubEpics = storyNode.getAttribute('data-has-nested-sub-epics') === 'true';
        const nodePath = storyNode.getAttribute('data-path');
        const fileLink = storyNode.getAttribute('data-file-link');
        const behavior = storyNode.getAttribute('data-behavior-needed') || null;
        const behaviorsAttr = storyNode.getAttribute('data-behaviors-needed');
        const behaviors = behaviorsAttr ? JSON.parse(behaviorsAttr) : (behavior ? [behavior] : []);
        
        console.log('[WebView]   nodeType:', nodeType);
        console.log('[WebView]   nodeName:', nodeName);
        console.log('[WebView]   hasChildren:', hasChildren);
        console.log('[WebView]   hasStories:', hasStories);
        console.log('[WebView]   hasNestedSubEpics:', hasNestedSubEpics);
        console.log('[WebView]   nodePath:', nodePath);
        console.log('[WebView]   fileLink:', fileLink);
        console.log('[WebView]   behavior (from DOM):', behavior);
        console.log('[WebView]   behaviors (from DOM):', behaviors);
        
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] Extracted behavior_needed from DOM: "' + behavior + '" for node: ' + nodeName
        });
        
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] Story node clicked: type=' + nodeType + ', name=' + nodeName + ', path=' + nodePath
        });
        

        if (window.selectNode && nodeType && nodeName !== null) {
            const options = {
                hasChildren: hasChildren,
                hasStories: hasStories,
                hasNestedSubEpics: hasNestedSubEpics,
                path: nodePath,
                behavior: behavior,
                behaviors: behaviors
            };
            console.log('[WebView]   Calling selectNode with options:', JSON.stringify(options, null, 2));
            window.selectNode(nodeType, nodeName, options);
        }
        

        e.stopPropagation();
        console.log('═══════════════════════════════════════════════════════');
    }
    


    let actionElement = target;
    let action = actionElement.getAttribute('data-action');
    let searchDepth = 0;
    while (!action && actionElement && actionElement.parentElement && searchDepth < 5) {
        actionElement = actionElement.parentElement;
        action = actionElement.getAttribute('data-action');
        searchDepth++;
    }
    
    if (action) {
        console.log('[WebView] Behavior/Action click detected, action:', action);
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] Behavior/Action click: action=' + action + ', element=' + actionElement.tagName + ', className=' + actionElement.className
        });
        
        if (action === 'navigateToBehavior') {
            const behaviorName = actionElement.getAttribute('data-behavior-name');
            const isSkip = actionElement.getAttribute('data-skip') === 'true';
            if (behaviorName && window.navigateToBehavior && !isSkip) {
                window.navigateToBehavior(behaviorName);
                e.stopPropagation();
                e.preventDefault();
            }
        } else if (action === 'navigateToAction') {
            const behaviorName = actionElement.getAttribute('data-behavior-name');
            const actionName = actionElement.getAttribute('data-action-name');
            const isSkip = actionElement.getAttribute('data-skip') === 'true';
            if (behaviorName && actionName && window.navigateToAction && !isSkip) {
                window.navigateToAction(behaviorName, actionName);
                e.stopPropagation();
                e.preventDefault();
            }
        } else if (action === 'toggleCollapse') {
            const targetId = actionElement.getAttribute('data-target');
            if (targetId && window.toggleCollapse) {
                console.log('[WebView] Calling toggleCollapse with:', targetId);
                window.toggleCollapse(targetId);
                e.stopPropagation();
                e.preventDefault();
            }
        } else if (action === 'toggleExecutionToggle') {
            const targetId = actionElement.getAttribute('data-target');
            if (targetId && window.toggleExecutionToggle) {
                window.toggleExecutionToggle(targetId);
                e.stopPropagation();
                e.preventDefault();
            }
        } else if (action === 'getBehaviorRules') {
            const behaviorName = actionElement.getAttribute('data-behavior-name');
            if (behaviorName && window.getBehaviorRules) {
                console.log('[WebView] Calling getBehaviorRules with:', behaviorName);
                window.getBehaviorRules(behaviorName);
                e.stopPropagation();
                e.preventDefault();
            }
        } else if (action === 'executeNavigationCommand') {
            const command = actionElement.getAttribute('data-command');
            if (command && window.executeNavigationCommand) {
                console.log('[WebView] Calling executeNavigationCommand with:', command);
                window.executeNavigationCommand(command);
                e.stopPropagation();
                e.preventDefault();
            }
        } else if (action === 'toggleSection') {
            const sectionId = actionElement.getAttribute('data-section-id');
            if (sectionId && window.toggleSection) {
                console.log('[WebView] Calling toggleSection with:', sectionId);
                window.toggleSection(sectionId);
                e.stopPropagation();
                e.preventDefault();
            }
        } else if (action === 'setExecutionMode') {
            const behaviorName = actionElement.getAttribute('data-behavior-name');
            const actionName = actionElement.getAttribute('data-action-name');
            const mode = actionElement.getAttribute('data-mode');
            if (behaviorName && actionName && mode) {
                const container = actionElement.closest('.execution-toggle-container');
                if (container && container.id && container.classList.contains('expanded')) {
                    container.classList.remove('expanded');
                    const currentState = window.getCollapseState();
                    sessionStorage.setItem('collapseState', JSON.stringify(currentState));
                }
                vscode.postMessage({
                    command: 'setExecutionMode',
                    behaviorName: behaviorName,
                    actionName: actionName,
                    mode: mode
                });
                e.stopPropagation();
                e.preventDefault();
            }
        } else if (action === 'setBehaviorExecuteMode') {
            const behaviorName = actionElement.getAttribute('data-behavior-name');
            const mode = actionElement.getAttribute('data-mode');
            if (behaviorName && mode) {
                const container = actionElement.closest('.execution-toggle-container');
                if (container && container.id && container.classList.contains('expanded')) {
                    container.classList.remove('expanded');
                    const currentState = window.getCollapseState();
                    sessionStorage.setItem('collapseState', JSON.stringify(currentState));
                }
                vscode.postMessage({
                    command: 'setBehaviorExecuteMode',
                    behaviorName: behaviorName,
                    mode: mode
                });
                e.stopPropagation();
                e.preventDefault();
            }
        }
    }
}, true);


document.addEventListener('dblclick', function(e) {
    const target = e.target;
    


    if (target.classList.contains('story-node') && target.getAttribute('data-inc-source') === null) {
        const nodePath = target.getAttribute('data-path');
        const nodeName = target.getAttribute('data-node-name');
        
        console.log('[WebView] DOUBLE-CLICK on story node:', nodeName, 'path:', nodePath);
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] Double-click on node: ' + nodeName + ', path: ' + nodePath
        });
        
        if (nodePath && window.enableEditMode) {
            window.enableEditMode(nodePath);
        }
        
        e.stopPropagation();
        e.preventDefault();
    }
}, true);


function _showCopyMenu(e, items) {
    e.preventDefault();
    e.stopPropagation();
    const existing = document.getElementById('story-node-copy-menu');
    if (existing) existing.remove();
    const menu = document.createElement('div');
    menu.id = 'story-node-copy-menu';
    menu.style.cssText = 'position:fixed;left:' + e.clientX + 'px;top:' + e.clientY + 'px;background:var(--vscode-dropdown-background);border:1px solid var(--vscode-dropdown-border);border-radius:4px;padding:4px 0;z-index:10001;min-width:160px;box-shadow:0 2px 8px rgba(0,0,0,0.2);';
    items.forEach(function(item) {
        if (item.separator) {
            var hr = document.createElement('div');
            hr.style.cssText = 'height:1px;background:var(--vscode-dropdown-border);margin:4px 0;';
            menu.appendChild(hr);
            return;
        }
        const div = document.createElement('div');
        div.textContent = item.label;
        div.style.cssText = 'padding:6px 12px;cursor:pointer;font-size:12px;';
        div.onmouseover = function() { div.style.backgroundColor = 'var(--vscode-list-hoverBackground)'; };
        div.onmouseout = function() { div.style.backgroundColor = ''; };
        div.onclick = function(ev) {
            ev.preventDefault(); ev.stopPropagation();
            menu.remove();
            document.removeEventListener('click', closeMenu);
            item.action();
        };
        menu.appendChild(div);
    });
    function closeMenu() { if (menu.parentNode) menu.remove(); document.removeEventListener('click', closeMenu); }
    document.body.appendChild(menu);
    setTimeout(function() { document.addEventListener('click', closeMenu); }, 0);
}

document.addEventListener('contextmenu', function(e) {

    const target = e.target.closest ? e.target.closest('.story-node') : (function() {
        let t = e.target;
        while (t && !t.classList.contains('story-node')) t = t.parentElement;
        return t;
    })();
    if (target && target.classList.contains('story-node')) {
        const nodePath = target.getAttribute('data-path');
        if (nodePath) {
            var scope = window.diagramScope || '';
            _showCopyMenu(e, [
                { label: 'Copy node name', action: function() {
                    vscode.postMessage({ command: 'copyNodeToClipboard', nodePath: nodePath, action: 'name' });
                }},
                { label: 'Copy full JSON', action: function() {
                    vscode.postMessage({ command: 'copyNodeToClipboard', nodePath: nodePath, action: 'json' });
                }},
                { separator: true },
                { label: 'Render diagram', action: function() {
                    vscode.postMessage({ command: 'renderDiagram', scope: scope });
                }},
                { label: 'Save layout', action: function() {
                    vscode.postMessage({ command: 'saveDiagramLayout', scope: scope });
                }},
                { label: 'Clear layout', action: function() {
                    vscode.postMessage({ command: 'clearDiagramLayout', scope: scope });
                }},
                { label: 'Generate report', action: function() {
                    vscode.postMessage({ command: 'generateDiagramReport', scope: scope });
                }},
                { label: 'Update graph', action: function() {
                    vscode.postMessage({ command: 'updateFromDiagram', scope: scope });
                }}
            ]);
            return;
        }
    }

    let incCol = e.target;
    let d = 6;
    while (incCol && d-- > 0 && !incCol.classList.contains('increment-column-container')) incCol = incCol.parentElement;
    if (incCol && incCol.classList.contains('increment-column-container')) {
        const incName = incCol.getAttribute('data-inc');
        _showCopyMenu(e, [
            { label: 'Copy increment name', action: function() {
                vscode.postMessage({ command: 'copyText', text: incName, label: 'Increment name copied' });
            }},
            { label: 'Copy as JSON', action: function() {
                vscode.postMessage({ command: 'copyIncrementStoriesJson', incName: incName });
            }}
        ]);
    }
}, true);


let draggedNode = null;
let draggedIncrement = null;
let dropIndicator = null;
let currentDropZone = null;
let incrementDropTarget = null;


function createDropIndicator() {
    if (!dropIndicator) {
        dropIndicator = document.createElement('div');
        dropIndicator.style.position = 'fixed';
        dropIndicator.style.height = '2px';
        dropIndicator.style.backgroundColor = 'rgb(255, 140, 0)';
        dropIndicator.style.pointerEvents = 'none';
        dropIndicator.style.zIndex = '10000';
        dropIndicator.style.transition = 'all 0.1s ease';
        dropIndicator.style.display = 'none';
        document.body.appendChild(dropIndicator);
    }
    return dropIndicator;
}

function removeDropIndicator() {
    if (dropIndicator && dropIndicator.parentNode) {
        dropIndicator.parentNode.removeChild(dropIndicator);
        dropIndicator = null;
    }
    currentDropZone = null;
}

document.addEventListener('dragstart', function(e) {
    console.log('[WebView] DRAGSTART EVENT FIRED');
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] DRAGSTART EVENT - target classList: ' + (e.target.classList ? Array.from(e.target.classList).join(', ') : 'none')
    });
    

    if (e.target.classList && e.target.classList.contains('increment-drag-handle')) {
        draggedIncrement = e.target.getAttribute('data-inc');
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', 'increment:' + draggedIncrement);
        e.target.style.opacity = '0.5';
        vscode.postMessage({ command: 'logToFile', message: '[INCREMENT] Drag column started: ' + draggedIncrement });
        return;
    }


    let target = e.target;
    while (target && !target.classList.contains('story-node')) {
        target = target.parentElement;
    }
    
    if (target && target.classList.contains('story-node')) {
        draggedNode = {
            path: target.getAttribute('data-path'),
            name: target.getAttribute('data-node-name'),
            type: target.getAttribute('data-node-type'),
            position: parseInt(target.getAttribute('data-position') || '0'),
            fromIncrement: target.getAttribute('data-inc-source')
        };
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', draggedNode.path);
        target.style.opacity = '0.5';
        console.log('[WebView] Drag started:', draggedNode);
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] DRAG STARTED: ' + JSON.stringify(draggedNode)
        });
    } else {
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] DRAGSTART ignored - not a story-node'
        });
    }
}, true);

document.addEventListener('dragend', function(e) {
    console.log('[WebView] DRAGEND EVENT FIRED');
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] DRAGEND EVENT'
    });
    

    let target = e.target;
    while (target && !target.classList.contains('story-node')) {
        target = target.parentElement;
    }
    
    if (target && target.classList.contains('story-node')) {
        target.style.opacity = '1';
    }
    if (e.target.classList && e.target.classList.contains('increment-drag-handle')) {
        e.target.style.opacity = '';
    }
    draggedNode = null;
    draggedIncrement = null;
    if (incrementDropTarget) { incrementDropTarget.style.outline = ''; incrementDropTarget = null; }
    removeDropIndicator();
    document.querySelectorAll('.increment-column-container').forEach(function(c) { c.style.outline = ''; });
    var unallocEl = document.querySelector('.unallocated-column');
    if (unallocEl) unallocEl.style.outline = '';
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] Drag ended, cleared draggedNode'
    });
}, true);

let dragoverLogCounter = 0;
document.addEventListener('dragover', function(e) {

    if (draggedIncrement) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';

        let col = e.target;
        let d = 10;
        while (col && d-- > 0 && !col.classList.contains('increment-column-container')) col = col.parentElement;
        if (col && col.getAttribute('data-inc') !== draggedIncrement) {
            if (incrementDropTarget) incrementDropTarget.style.outline = '';
            incrementDropTarget = col;
            const rect = col.getBoundingClientRect();
            const isLeft = e.clientX < rect.left + rect.width / 2;
            col.style.outline = isLeft ? '2px solid orange' : '';
            col.style.outlineOffset = '-2px';

            const ind = createDropIndicator();
            ind.style.width = '3px';
            ind.style.height = rect.height + 'px';
            ind.style.top = rect.top + 'px';
            ind.style.left = (isLeft ? rect.left : rect.right - 3) + 'px';
            ind.style.display = 'block';
        }
        return;
    }


    let target = e.target;
    let searchDepth = 0;
    while (target && !target.classList.contains('story-node') && searchDepth < 10) {
        target = target.parentElement;
        searchDepth++;
    }
    

    if (dragoverLogCounter++ % 20 === 0 && draggedNode) {
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] DRAGOVER - found target: ' + (target ? 'YES' : 'NO') + ', draggedNode: ' + (draggedNode ? draggedNode.name : 'null')
        });
    }
    

    if (draggedNode && draggedNode.type === 'story') {
        var incEl = e.target;
        var d = 6;
        while (incEl && d-- > 0) {
            if (incEl.classList && incEl.classList.contains('increment-column-container')) {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'copy';
                incEl.style.outline = '2px solid var(--accent-color)';
                break;
            }
            incEl = incEl.parentElement;
        }
        if (!incEl || !incEl.classList.contains('increment-column-container')) {
            document.querySelectorAll('.increment-column-container').forEach(function(c) { c.style.outline = ''; });
        }
    }
    
    if (target && target.classList.contains('story-node') && draggedNode) {


        if (draggedNode.fromIncrement) {
            let unallocCheck = target;
            while (unallocCheck && !unallocCheck.classList.contains('unallocated-column')) unallocCheck = unallocCheck.parentElement;
            if (unallocCheck && unallocCheck.classList.contains('unallocated-column')) {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
                removeDropIndicator();
                document.querySelectorAll('.increment-column-container').forEach(function(c) { c.style.outline = ''; });
                unallocCheck.style.outline = '2px dashed rgb(255, 140, 0)';
                return;
            }
        }

        const targetType = target.getAttribute('data-node-type');
        const targetPath = target.getAttribute('data-path');
        const targetName = target.getAttribute('data-node-name');
        

        if (draggedNode.path === targetPath) {
            removeDropIndicator();
            return;
        }
        

        const canContain = (targetType === 'epic' && draggedNode.type === 'sub-epic') ||
                            (targetType === 'sub-epic' && (draggedNode.type === 'sub-epic' || draggedNode.type === 'story')) ||
                            (targetType === 'story' && draggedNode.type === 'scenario');
        

        const sameType = draggedNode.type === targetType;
        
        if (canContain || sameType) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            

            const rect = target.getBoundingClientRect();
            const mouseY = e.clientY;
            const targetTop = rect.top;
            const targetHeight = rect.height;
            const relativeY = mouseY - targetTop;
            const percentY = relativeY / targetHeight;
            

            let dropZone;
            const indicator = createDropIndicator();
            

            const hasStories = target.getAttribute('data-has-stories') === 'true';
            const hasNestedSubEpics = target.getAttribute('data-has-nested-sub-epics') === 'true';
            const isEmptyContainer = !hasStories && !hasNestedSubEpics;
            



            if (canContain && percentY >= 0.2 && percentY <= 0.8) {

                dropZone = 'inside';
                target.style.backgroundColor = 'rgba(255, 140, 0, 0.3)';
                indicator.style.display = 'none';
                if (dragoverLogCounter % 20 === 0) {
                    vscode.postMessage({
                        command: 'logToFile',
                        message: '[WebView] DRAGOVER ON (inside) - will nest inside ' + target.getAttribute('data-node-name')
                    });
                }
            } else if (sameType) {

                dropZone = 'after';
                target.style.backgroundColor = '';
                indicator.style.display = 'block';
                indicator.style.left = rect.left + 'px';
                indicator.style.top = (rect.top + rect.height) + 'px';
                indicator.style.width = rect.width + 'px';

                if (dragoverLogCounter % 20 === 0) {
                    vscode.postMessage({
                        command: 'logToFile',
                        message: '[WebView] DRAGOVER AFTER - hovering over: "' + targetName + '", line at y=' + (rect.top + rect.height) + ' (BOTTOM of node), will insert AFTER this node'
                    });
                }
            } else {
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] DRAGOVER INVALID - canContain: ' + canContain + ', sameType: ' + sameType + ', dragging ' + draggedNode.type + ' onto ' + targetType
                });
                removeDropIndicator();
                return;
            }
            
            currentDropZone = dropZone;
        } else {
            removeDropIndicator();
        }
    } else {
        removeDropIndicator();
        if (draggedNode && draggedNode.type === 'story') {

            let incTarget = e.target;
            let d = 8;
            while (incTarget && d-- > 0 && !incTarget.classList.contains('increment-column-container')) {
                incTarget = incTarget.parentElement;
            }

            let unallocTarget = e.target;
            let d2 = 8;
            while (unallocTarget && d2-- > 0 && !unallocTarget.classList.contains('unallocated-column')) {
                unallocTarget = unallocTarget.parentElement;
            }

            document.querySelectorAll('.increment-column-container').forEach(function(c) { c.style.outline = ''; });
            var unallocEl = document.querySelector('.unallocated-column');
            if (unallocEl) unallocEl.style.outline = '';

            if (incTarget && incTarget.classList.contains('increment-column-container')) {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
                incTarget.style.outline = '2px solid rgb(255, 140, 0)';
            } else if (unallocTarget && unallocTarget.classList.contains('unallocated-column') && draggedNode.fromIncrement) {

                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
                unallocTarget.style.outline = '2px dashed rgb(255, 140, 0)';
            }
        }
    }
}, true);

document.addEventListener('dragleave', function(e) {

    let target = e.target;
    while (target && !target.classList.contains('story-node')) {
        target = target.parentElement;
    }
    
    if (target && target.classList.contains('story-node')) {
        target.style.backgroundColor = '';
    }

    let incTarget = e.target;
    let d = 8;
    while (incTarget && d-- > 0 && !incTarget.classList.contains('increment-column-container')) {
        incTarget = incTarget.parentElement;
    }
    if (incTarget && incTarget.classList.contains('increment-column-container')) {
        incTarget.style.outline = '';
    }
    let unallocTarget = e.target;
    let d2 = 8;
    while (unallocTarget && d2-- > 0 && !unallocTarget.classList.contains('unallocated-column')) {
        unallocTarget = unallocTarget.parentElement;
    }
    if (unallocTarget && unallocTarget.classList.contains('unallocated-column')) {
        unallocTarget.style.outline = '';
    }
}, true);

document.addEventListener('drop', function(e) {
    console.log('[WebView] ===== DROP EVENT FIRED =====');



    var transferData = '';
    try { transferData = e.dataTransfer.getData('text/plain') || ''; } catch(_) {}
    var isIncrementDrag = transferData.startsWith('increment:');
    var incDragName = isIncrementDrag ? transferData.slice('increment:'.length) : (draggedIncrement || '');

    if (isIncrementDrag || draggedIncrement) {
        e.preventDefault();

        let col = e.target;
        let d = 10;
        while (col && d-- > 0 && !col.classList.contains('increment-column-container')) col = col.parentElement;
        if (col) {
            const targetName = col.getAttribute('data-inc');
            if (targetName && targetName !== incDragName) {
                const rect = col.getBoundingClientRect();
                const isLeft = e.clientX < rect.left + rect.width / 2;
                const cmd = isLeft
                    ? 'story_graph.reorder_increment increment_name:"' + incDragName + '" before:"' + targetName + '"'
                    : 'story_graph.reorder_increment increment_name:"' + incDragName + '" after:"' + targetName + '"';
                vscode.postMessage({ command: 'logToFile', message: '[INCREMENT] Reorder: ' + cmd });
                _incCmd(cmd);
            }
        }
        if (incrementDropTarget) { incrementDropTarget.style.outline = ''; incrementDropTarget = null; }
        removeDropIndicator();
        draggedIncrement = null;
        return;
    }

    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] ===== DROP EVENT FIRED ===== draggedNode: ' + (draggedNode ? draggedNode.name : 'null') + ', currentDropZone: ' + (currentDropZone || 'null')
    });
    

    let target = e.target;
    while (target && !target.classList.contains('story-node')) {
        target = target.parentElement;
    }
    
    if (target && target.classList.contains('story-node') && draggedNode && currentDropZone) {



        const targetIncSource = target.getAttribute('data-inc-source');
        if (draggedNode.fromIncrement !== null && draggedNode.fromIncrement !== undefined && targetIncSource !== null) {
            e.preventDefault();
            removeDropIndicator();
            document.querySelectorAll('.increment-column-container').forEach(function(c) { c.style.outline = ''; });
            var unallocEl2 = document.querySelector('.unallocated-column');
            if (unallocEl2) unallocEl2.style.outline = '';

            let incCol = target;
            while (incCol && !incCol.classList.contains('increment-column-container') && !incCol.classList.contains('unallocated-column')) {
                incCol = incCol.parentElement;
            }
            const draggedName = draggedNode.name;
            const sourceInc = draggedNode.fromIncrement;

            if (incCol && incCol.classList.contains('unallocated-column')) {

                if (sourceInc) window.removeStoryFromIncrement(sourceInc, draggedName);
            } else {
                const incName = incCol ? incCol.getAttribute('data-inc') : null;
                if (incName && sourceInc === incName) {

                    const targetPos = parseInt(target.getAttribute('data-position') || '0');
                    const rect = target.getBoundingClientRect();
                    const insertPos = e.clientY < rect.top + rect.height / 2 ? targetPos : targetPos + 1;
                    _incCmd('story_graph.reorder_story_in_increment increment_name:"' + incName + '" story_name:"' + draggedName + '" position:' + insertPos);
                } else if (incName && sourceInc !== incName) {

                    const dropPos = _incrementDropPosition(incCol, e.clientY);
                    if (sourceInc) window.removeStoryFromIncrement(sourceInc, draggedName);
                    window.addStoryToIncrement(incName, draggedName, dropPos);
                }
            }
            draggedNode = null;
            return;
        }


        if (draggedNode.fromIncrement !== null && draggedNode.fromIncrement !== undefined) {
            let unallocCheck = target;
            while (unallocCheck && !unallocCheck.classList.contains('unallocated-column')) unallocCheck = unallocCheck.parentElement;
            if (unallocCheck && unallocCheck.classList.contains('unallocated-column') && draggedNode.fromIncrement) {
                e.preventDefault();
                removeDropIndicator();
                document.querySelectorAll('.increment-column-container').forEach(function(c) { c.style.outline = ''; });
                var unallocEl3 = document.querySelector('.unallocated-column');
                if (unallocEl3) unallocEl3.style.outline = '';
                window.removeStoryFromIncrement(draggedNode.fromIncrement, draggedNode.name);
                draggedNode = null;
                return;
            }
        }

        e.preventDefault();
        e.stopPropagation();
        target.style.backgroundColor = '';
        

        const dropZone = currentDropZone;
        removeDropIndicator();
        
        const targetPath = target.getAttribute('data-path');
        const targetName = target.getAttribute('data-node-name');
        const targetType = target.getAttribute('data-node-type');
        
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] DROP on story-node - dragged: ' + draggedNode.name + ' onto: ' + targetName + ', dropZone: ' + dropZone
        });
        
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] DROP INFO - draggedNode.path: ' + draggedNode.path + ', targetPath: ' + targetPath
        });
        
        if (draggedNode.path !== targetPath) {
            console.log('[WebView] Drop detected: dragged=' + draggedNode.name + ' targetPath=' + targetPath + ' targetName=' + targetName + ' targetType=' + targetType + ' dropZone=' + dropZone);
            
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] DROP DETECTED - Dragged: ' + draggedNode.name + ' (type: ' + draggedNode.type + ', pos: ' + draggedNode.position + ') onto Target: ' + targetName + ' (type: ' + targetType + '), dropZone: ' + dropZone
            });
            

            console.log('[WebView] Move operation - waiting for backend and full refresh');
            
            let command;
            
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] COMMAND CONSTRUCTION - dropZone: ' + dropZone
            });
            
            if (dropZone === 'inside') {



                var targetForCommand = targetPath.replace(/^story_graph\./, '');


                command = draggedNode.path + '.move_to target:' + targetForCommand;
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] INSIDE COMMAND - targetPath: ' + targetPath + ', targetForCommand: ' + targetForCommand + ', command: ' + command
                });
            } else if (dropZone === 'after') {
                var targetPos = parseInt(target.getAttribute('data-position') || '0');
                var draggedPos = draggedNode.position;
                



                var parentMatch = targetPath.match(/(.*)\."[^"]+"/);
                var parentPath = parentMatch ? parentMatch[1] : 'story_graph';
                

                var targetForCommand = parentPath.replace(/^story_graph\./, '');
                
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] AFTER CALCULATION - targetPos: ' + targetPos + ', draggedPos: ' + draggedPos + ', parentPath: ' + parentPath + ', targetForCommand: ' + targetForCommand
                });
                


                var finalPos = (draggedPos < targetPos) ? targetPos : (targetPos + 1);
                
                command = draggedNode.path + '.move_to target:' + targetForCommand + ' at_position:' + finalPos;
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] AFTER COMMAND - dragged from ' + draggedPos + ' to position: ' + finalPos + ' (target was at ' + targetPos + '), command: ' + command
                });
            }
            


            if (dropZone === 'after' && typeof window.handleMoveNode === 'function') {

                var parentMatch = targetPath.match(/(.*)\."[^"]+"/);
                var parentPath = parentMatch ? parentMatch[1] : 'story_graph';
                var finalPos = (draggedNode.position < targetPos) ? targetPos : (targetPos + 1);
                

                window.handleMoveNode({
                    sourceNodePath: draggedNode.path,
                    targetParentPath: parentPath,
                    targetNodePath: targetPath,
                    position: finalPos,
                    dropZone: 'after'
                });
            } else if (dropZone === 'inside' && typeof window.handleMoveNode === 'function') {

                window.handleMoveNode({
                    sourceNodePath: draggedNode.path,
                    targetParentPath: targetPath,
                    position: 0,
                    dropZone: 'inside'
                });
            } else {

                console.warn('[WebView] handleMoveNode not available, sending command directly');
                vscode.postMessage({
                    command: 'executeCommand',
                    commandText: command

                });
            }
        } else {
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] DROP ignored - same node'
            });
        }
    } else if (draggedNode && draggedNode.type === 'story') {
        function _clearIncrementHighlights() {
            document.querySelectorAll('.increment-column-container').forEach(function(c) { c.style.outline = ''; });
            var ua = document.querySelector('.unallocated-column');
            if (ua) ua.style.outline = '';
        }


        var incTarget = e.target;
        var maxDepth = 8;
        while (incTarget && maxDepth-- > 0) {
            if (incTarget.classList && (incTarget.classList.contains('increment-column-container') || incTarget.classList.contains('unallocated-column'))) break;
            incTarget = incTarget.parentElement;
        }

        if (incTarget && incTarget.classList.contains('unallocated-column') && draggedNode.fromIncrement) {

            e.preventDefault();
            removeDropIndicator();
            _clearIncrementHighlights();
            var storyName = draggedNode.name;
            var sourceInc = draggedNode.fromIncrement;
            console.log('[INCREMENT] DROP story onto unallocated (remove from increment):', storyName, 'from:', sourceInc);
            vscode.postMessage({ command: 'logToFile', message: '[INCREMENT] Drop to unallocated: ' + storyName + ' from:' + sourceInc });
            window.removeStoryFromIncrement(sourceInc, storyName);
            draggedNode = null;
        } else if (incTarget && incTarget.classList.contains('increment-column-container')) {
            e.preventDefault();
            removeDropIndicator();
            _clearIncrementHighlights();
            var incName = incTarget.getAttribute('data-inc');
            var storyName = draggedNode.name;
            var sourceInc = draggedNode.fromIncrement;
            console.log('[INCREMENT] DROP story onto increment:', storyName, '->', incName, '(from:', sourceInc, ')');
            vscode.postMessage({ command: 'logToFile', message: '[INCREMENT] Drop: ' + storyName + ' -> ' + incName + ' from:' + sourceInc });
            var dropPos = _incrementDropPosition(incTarget, e.clientY);
            if (sourceInc && sourceInc !== incName) {

                window.removeStoryFromIncrement(sourceInc, storyName);
                window.addStoryToIncrement(incName, storyName, dropPos);
            } else if (sourceInc !== null) {

                window.addStoryToIncrement(incName, storyName, dropPos);
            } else {

                window.addStoryToIncrement(incName, storyName, dropPos);
            }
            draggedNode = null;
        }
    } else {
        removeDropIndicator();
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] DROP ignored - not story-node, no draggedNode, or no dropZone'
        });
    }
}, true);


window.testFunction = function() {
    console.log('[WebView] TEST FUNCTION CALLED - functions are accessible!');
    alert('Test function works!');
};
console.log('[WebView] window.testFunction defined:', typeof window.testFunction);


window.hidePanel = function() {
    console.log('[hidePanel] Requesting panel collapse');
    vscode.postMessage({ command: 'hidePanel' });
};

const WS_SECTION_IDS = ['workspace-content', 'ws-clarify-content', 'ws-clarify-questions-content', 'ws-strategy-content', 'ws-build-content', 'ws-build-rules-content', 'ws-diagrams-content'];
const WS_STORAGE_KEY = 'agileBots_workspaceCollapse';
const WS_QA_COLLAPSE_KEY = 'agileBots_clarifyQACollapse';
const WS_TEXTAREA_COLLAPSE_KEY = 'agileBots_textareaCollapse';

window.saveWorkspaceCollapseState = function(behavior) {
    if (!behavior || typeof localStorage === 'undefined') return;
    const state = {};
    WS_SECTION_IDS.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            const section = el.closest('.collapsible-section');
            state[id] = section && section.classList.contains('expanded');
        }
    });
    document.querySelectorAll('[id^="ws-strategy-decision-"]').forEach(el => {
        const section = el.closest('.collapsible-section');
        if (section) state[el.id] = section.classList.contains('expanded');
    });
    try {
        const all = JSON.parse(localStorage.getItem(WS_STORAGE_KEY) || '{}');
        all[behavior] = state;
        localStorage.setItem(WS_STORAGE_KEY, JSON.stringify(all));
    } catch (e) {}
};

window.restoreWorkspaceCollapseState = function(behavior) {
    if (!behavior || typeof localStorage === 'undefined') return;
    try {
        const all = JSON.parse(localStorage.getItem(WS_STORAGE_KEY) || '{}');
        const state = all[behavior];
        if (state) {
            Object.keys(state).forEach(id => {
                const content = document.getElementById(id);
                if (!content) return;
                const section = content.closest('.collapsible-section');
                if (!section) return;
                const expanded = state[id];
                if (expanded) {
                    const isWorkspaceContent = id === 'workspace-content';
                    content.style.maxHeight = isWorkspaceContent ? '400px' : '2000px';
                    content.style.overflow = isWorkspaceContent ? 'auto' : 'visible';
                    content.style.overflowX = isWorkspaceContent ? 'hidden' : '';
                    content.style.display = 'block';
                    section.classList.add('expanded');
                } else {
                    content.style.maxHeight = '0px';
                    content.style.overflow = 'hidden';
                    content.style.display = 'none';
                    section.classList.remove('expanded');
                }
            });
        }
        if (window.restoreClarifyQACollapseState) {
            window.restoreClarifyQACollapseState(behavior);
        }
        if (window.restoreTextareaCollapseState) {
            window.restoreTextareaCollapseState(behavior);
        }
    } catch (e) {}
};

window.saveTextareaCollapseState = function(behavior) {
    if (!behavior || typeof localStorage === 'undefined') return;
    try {
        const state = {};
        ['ws-clarify-evidence', 'ws-strategy-assumptions'].forEach(id => {
            const ta = document.getElementById(id);
            if (ta) state[id] = ta.getAttribute('data-collapsed') === 'true';
        });
        const all = JSON.parse(localStorage.getItem(WS_TEXTAREA_COLLAPSE_KEY) || '{}');
        all[behavior] = state;
        localStorage.setItem(WS_TEXTAREA_COLLAPSE_KEY, JSON.stringify(all));
    } catch (e) {}
};

window.restoreTextareaCollapseState = function(behavior) {
    if (!behavior || typeof localStorage === 'undefined') return;
    try {
        const all = JSON.parse(localStorage.getItem(WS_TEXTAREA_COLLAPSE_KEY) || '{}');
        const state = all[behavior];
        if (!state) return;
        Object.keys(state).forEach(id => {
            if (!state[id]) return;
            const textarea = document.getElementById(id);
            const toggleBtn = document.getElementById(id + '-toggle');
            if (textarea) {
                textarea.style.display = 'none';
                textarea.style.overflow = 'hidden';
                textarea.setAttribute('data-collapsed', 'true');
                if (toggleBtn) toggleBtn.textContent = '▼';
            }
        });
    } catch (e) {}
};

window.saveClarifyQACollapseState = function(behavior) {
    if (!behavior || typeof localStorage === 'undefined') return;
    try {
        const state = {};
        const textareas = document.querySelectorAll('[id^="ws-clarify-answer-"]');
        textareas.forEach((ta) => {
            const id = ta.id;
            const match = id.match(/ws-clarify-answer-(\d+)/);
            if (match) {
                const idx = parseInt(match[1], 10);
                state[idx] = ta.getAttribute('data-collapsed') === 'true';
            }
        });
        const all = JSON.parse(localStorage.getItem(WS_QA_COLLAPSE_KEY) || '{}');
        all[behavior] = state;
        localStorage.setItem(WS_QA_COLLAPSE_KEY, JSON.stringify(all));
    } catch (e) {}
};

window.restoreClarifyQACollapseState = function(behavior) {
    if (!behavior || typeof localStorage === 'undefined') return;
    try {
        const all = JSON.parse(localStorage.getItem(WS_QA_COLLAPSE_KEY) || '{}');
        const state = all[behavior];
        if (!state) return;
        Object.keys(state).forEach(idxStr => {
            const idx = parseInt(idxStr, 10);
            const collapsed = state[idx];
            if (!collapsed) return;
            const textarea = document.getElementById('ws-clarify-answer-' + idx);
            const toggleBtn = document.getElementById('ws-qa-toggle-' + idx);
            if (textarea) {
                textarea.style.display = 'none';
                textarea.style.height = '';
                textarea.style.overflow = 'hidden';
                textarea.setAttribute('data-collapsed', 'true');
                if (toggleBtn) toggleBtn.textContent = '▼';
            }
        });
    } catch (e) {}
};

window.toggleSection = function(sectionId) {
    console.log('[toggleSection] Called with sectionId:', sectionId);
    const content = document.getElementById(sectionId);
    console.log('[toggleSection] Content element:', content);
    if (content) {
        const section = content.closest('.collapsible-section');
        console.log('[toggleSection] Parent section:', section);
        const isExpanded = section && section.classList.contains('expanded');
        console.log('[toggleSection] isExpanded:', isExpanded);
        

        if (isExpanded) {

            content.style.maxHeight = '0px';
            content.style.overflow = 'hidden';
            content.style.display = 'none';
        } else {
            const isWorkspaceContent = sectionId === 'workspace-content';
            content.style.maxHeight = isWorkspaceContent ? '400px' : '2000px';
            content.style.overflow = isWorkspaceContent ? 'auto' : 'visible';
            content.style.overflowX = isWorkspaceContent ? 'hidden' : '';
            content.style.display = 'block';

            if (content.querySelector('[id*="clarify-answer-"]')) {
                setTimeout(() => { if (window.expandClarifyBoxes) window.expandClarifyBoxes(); }, 50);
            }
        }
        

        const header = content.previousElementSibling;
        console.log('[toggleSection] Header element:', header);
        if (header && section) {
            section.classList.toggle('expanded', !isExpanded);
            console.log('[toggleSection] After toggle, section classes:', section.className);

            const icon = header.querySelector('.expand-icon');
            console.log('[toggleSection] Icon element:', icon);
            if (icon) {
                icon.textContent = '▸';
                console.log('[toggleSection] Icon transform:', window.getComputedStyle(icon).transform);
            }
        }

        const isWorkspaceSection = WS_SECTION_IDS.indexOf(sectionId) >= 0 || (sectionId && sectionId.startsWith('ws-strategy-decision-'));
        if (isWorkspaceSection && window.currentBehavior && window.saveWorkspaceCollapseState) {
            window.saveWorkspaceCollapseState(window.currentBehavior);
        }
        if (sectionId === 'scope-content' && typeof vscode !== 'undefined') {
            vscode.postMessage({ command: 'sectionExpansion', sectionId: sectionId, expanded: !isExpanded });
        }
    }
};



window.expandInstructionsSection = function(actionName) {
    console.log('[expandInstructionsSection] Called with actionName:', actionName);
    if (!actionName) return;
    

    const actionToSectionName = {
        'clarify': 'Clarify',
        'strategy': 'Strategy',
        'build': 'Build',
        'validate': 'Validate',
        'render': 'Render'
    };
    
    const sectionName = actionToSectionName[actionName];
    if (!sectionName) {
        console.log('[expandInstructionsSection] No section mapped for action:', actionName);
        return;
    }
    

    document.querySelectorAll('[id^="instr-section-"]').forEach(content => {
        const section = content.closest('.collapsible-section');
        if (section) {
            content.style.maxHeight = '0px';
            content.style.overflow = 'hidden';
            content.style.display = 'none';
            section.classList.remove('expanded');
        }
    });
    

    const headers = document.querySelectorAll('.collapsible-header');
    for (const header of headers) {
        const headerText = header.textContent || '';

        if (headerText.includes(sectionName) && !headerText.includes('Base')) {
            const section = header.closest('.collapsible-section');
            const content = header.nextElementSibling;
            
            if (section && content && content.classList.contains('collapsible-content')) {
                console.log('[expandInstructionsSection] Expanding section:', sectionName);

                content.style.maxHeight = '2000px';
                content.style.overflow = 'visible';
                content.style.display = 'block';
                section.classList.add('expanded');
                

                if (sectionName === 'Clarify' && content.querySelector('[id*="clarify-answer-"]')) {
                    setTimeout(() => { if (window.expandClarifyBoxes) window.expandClarifyBoxes(); }, 50);
                }
                

                const icon = header.querySelector('.expand-icon');
                if (icon) {
                    icon.textContent = '▸';
                }
                return;
            }
        }
    }
    console.log('[expandInstructionsSection] Section not found for:', sectionName);
};


window.getCollapseState = function() {
    const state = {};
    document.querySelectorAll('.collapsible-content').forEach(content => {
        if (content.id) {
            state[content.id] = content.style.display !== 'none';
        }
    });
    document.querySelectorAll('.execution-toggle-container').forEach(container => {
        if (container.id) {
            state[container.id] = container.classList.contains('expanded');
        }
    });
    return state;
};

window.restoreCollapseState = function(state) {
    if (!state) return;
    Object.keys(state).forEach(id => {
        const el = document.getElementById(id);
        if (!el) return;
        const shouldBeExpanded = state[id];
        if (el.classList && el.classList.contains('execution-toggle-container')) {
            if (shouldBeExpanded) {
                el.classList.add('expanded');
            } else {
                el.classList.remove('expanded');
            }
        } else if (el.classList && el.classList.contains('collapsible-content')) {
            el.style.display = shouldBeExpanded ? 'block' : 'none';
            const header = el.previousElementSibling;
            if (header) {
                const icon = header.querySelector('span[id$="-icon"]');
                if (icon) {
                    const plusSrc = icon.getAttribute('data-plus');
                    const subtractSrc = icon.getAttribute('data-subtract');
                    if (plusSrc && subtractSrc) {
                        const img = icon.querySelector('img');
                        if (img) {
                            img.src = shouldBeExpanded ? subtractSrc : plusSrc;
                        }
                    }
                }
                if (id && id.startsWith('behavior-')) {
                    const behaviorNameSpan = header.querySelector('.behavior-name-clickable');
                    if (behaviorNameSpan) {
                        const isSkip = header.getAttribute('data-skip') === 'true';
                        if (shouldBeExpanded || isSkip) {
                            behaviorNameSpan.removeAttribute('data-action');
                            behaviorNameSpan.removeAttribute('data-behavior-name');
                            behaviorNameSpan.removeAttribute('data-skip');
                            behaviorNameSpan.style.cursor = 'default';
                            behaviorNameSpan.style.textDecoration = 'none';
                        } else {
                            const behaviorName = header.getAttribute('data-behavior') || '';
                            behaviorNameSpan.setAttribute('data-action', 'navigateToBehavior');
                            behaviorNameSpan.setAttribute('data-behavior-name', behaviorName);
                            behaviorNameSpan.setAttribute('data-skip', 'false');
                            behaviorNameSpan.style.cursor = 'pointer';
                            behaviorNameSpan.style.textDecoration = 'underline';
                        }
                    }
                }
            }
        }
    });
};

window.toggleExecutionToggle = function(containerId) {
    const container = document.getElementById(containerId);
    if (container && container.classList.contains('execution-toggle-container')) {
        container.classList.toggle('expanded');
        const currentState = window.getCollapseState();
        sessionStorage.setItem('collapseState', JSON.stringify(currentState));
    }
};

window.toggleCollapse = function(elementId) {
    const content = document.getElementById(elementId);
    if (content) {
        const isHidden = content.style.display === 'none';
        content.style.display = isHidden ? 'block' : 'none';
        
        const header = content.previousElementSibling;
        if (header) {
            const icon = header.querySelector('span[id$="-icon"]');
            if (icon) {

                const plusSrc = icon.getAttribute('data-plus');
                const subtractSrc = icon.getAttribute('data-subtract');
                if (plusSrc && subtractSrc) {
                    const img = icon.querySelector('img');
                    if (img) {
                        img.src = isHidden ? subtractSrc : plusSrc;
                    } else {

                        const imgSrc = isHidden ? subtractSrc : plusSrc;
                        const imgAlt = isHidden ? 'Collapse' : 'Expand';
                        icon.innerHTML = '<img src="' + imgSrc + '" style="width: 12px; height: 12px; vertical-align: middle;" alt="' + imgAlt + '" />';
                    }
                }
            }
            if (elementId && elementId.startsWith('behavior-')) {
                const behaviorNameSpan = header.querySelector('.behavior-name-clickable');
                if (behaviorNameSpan) {
                    const isSkip = header.getAttribute('data-skip') === 'true';
                    const expanded = content.style.display !== 'none';
                    if (expanded || isSkip) {
                        behaviorNameSpan.removeAttribute('data-action');
                        behaviorNameSpan.removeAttribute('data-behavior-name');
                        behaviorNameSpan.removeAttribute('data-skip');
                        behaviorNameSpan.style.cursor = 'default';
                        behaviorNameSpan.style.textDecoration = 'none';
                    } else {
                        const behaviorName = header.getAttribute('data-behavior') || '';
                        behaviorNameSpan.setAttribute('data-action', 'navigateToBehavior');
                        behaviorNameSpan.setAttribute('data-behavior-name', behaviorName);
                        behaviorNameSpan.setAttribute('data-skip', 'false');
                        behaviorNameSpan.style.cursor = 'pointer';
                        behaviorNameSpan.style.textDecoration = 'underline';
                    }
                }
            }
        }
        

        const currentState = window.getCollapseState();
        sessionStorage.setItem('collapseState', JSON.stringify(currentState));
    }
};

window.openFile = function(filePath, event) {

    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }



    var resolvedPath = filePath;
    if (window.diagramScope && filePath && filePath.indexOf('.drawio') !== -1) {
        var slug = window.diagramScope.toLowerCase().split(' ').join('-').split('').filter(function(c) {
            return (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') || c === '-';
        }).join('');
        if (slug && filePath.indexOf('-' + slug + '.drawio') === -1) {
            if (filePath.indexOf('-all.drawio') !== -1) {
                resolvedPath = filePath.split('-all.drawio').join('-' + slug + '.drawio');
            } else {
                resolvedPath = filePath.split('.drawio').join('-' + slug + '.drawio');
            }
        }
    }
    console.log('[WebView] openFile called with:', resolvedPath);

    var savedScrollY = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
    sessionStorage.setItem('scrollPosition', savedScrollY.toString());
    console.log('[WebView] Saved scroll position before file open:', savedScrollY);
    
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] openFile called with: ' + resolvedPath
    });
    vscode.postMessage({
        command: 'openFile',
        filePath: resolvedPath
    });
    

    setTimeout(() => {
        window.scrollTo(0, savedScrollY);
    }, 0);
    
    return false;
};
window.openFiles = function(filePaths, event) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    if (!filePaths || !Array.isArray(filePaths) || filePaths.length === 0) return false;
    const savedScrollY = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
    sessionStorage.setItem('scrollPosition', savedScrollY.toString());
    vscode.postMessage({ command: 'openFiles', filePaths: filePaths });
    setTimeout(() => { window.scrollTo(0, savedScrollY); }, 0);
    return false;
};
window.openFilesFromEl = function(el, event) {
    if (event) { event.preventDefault(); event.stopPropagation(); }
    const raw = el && el.getAttribute && el.getAttribute('data-test-files');
    if (raw) {
        try {
            window.openFiles(JSON.parse(raw));
        } catch (e) {
            console.error('[WebView] openFilesFromEl parse error:', e);
        }
    }
    return false;
};


window.expandClarifyBoxes = function() {
    const textareas = document.querySelectorAll('[id*="clarify-answer-"]');
    textareas.forEach((ta) => {
        if (ta.getAttribute('data-collapsed') === 'false') {
            ta.style.overflow = 'hidden';
            ta.style.height = '0px';
            const h = ta.scrollHeight;
            ta.style.height = Math.max(60, h) + 'px';
            ta.style.overflow = 'visible';
        }
    });
};


window.saveScrollPosition = function() {
    const scrollY = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
    sessionStorage.setItem('scrollPosition', scrollY.toString());
    console.log('[WebView] Saved scroll position:', scrollY);
};

window.restoreScrollPosition = function() {
    const savedPosition = sessionStorage.getItem('scrollPosition');
    if (savedPosition) {
        const scrollY = parseInt(savedPosition, 10);
        window.scrollTo(0, scrollY);
        console.log('[WebView] Restored scroll position:', scrollY);
    }
};

window.updateFilter = function(filterValue) {
    console.log('[WebView] updateFilter called with:', filterValue);
    const message = {
        command: 'updateFilter',
        filter: filterValue
    };
    console.log('[WebView] Sending message:', message);
    vscode.postMessage(message);
    console.log('[WebView] postMessage sent');
};


console.log('[WebView] updateFilter function exists:', typeof updateFilter);

window.updateIncludeLevel = function(level) {
    console.log('[WebView] updateIncludeLevel called with:', level);
    vscode.postMessage({
        command: 'updateIncludeLevel',
        includeLevel: level
    });
};

window.clearScopeFilter = function(viewMode) {
    vscode.postMessage({
        command: 'clearScopeFilter',
        viewMode: viewMode || null
    });
};

window.showAllScope = function() {
    console.log('[WebView] showAllScope called');
    vscode.postMessage({
        command: 'showAllScope'
    });
};

window.executeNavigationCommand = function(command) {
    console.log('[WebView] executeNavigationCommand click ->', command);
    vscode.postMessage({
        command: 'executeNavigationCommand',
        commandText: command
    });
};

window.navigateToBehavior = function(behaviorName) {
    vscode.postMessage({
        command: 'navigateToBehavior',
        behaviorName: behaviorName
    });
};

window.navigateToAction = function(behaviorName, actionName) {
    vscode.postMessage({
        command: 'navigateToAction',
        behaviorName: behaviorName,
        actionName: actionName
    });
};

window.navigateAndExecute = function(behaviorName, actionName, operationName) {
    console.log('[WebView] navigateAndExecute click ->', behaviorName, actionName, operationName);
    vscode.postMessage({
        command: 'navigateAndExecute',
        behaviorName: behaviorName,
        actionName: actionName,
        operationName: operationName
    });
};

window.setBehaviorSpecialInstructions = function(textareaEl) {
    if (!textareaEl || textareaEl.tagName !== 'TEXTAREA') return;
    const behaviorName = textareaEl.getAttribute('data-behavior-name');
    const instructionText = (textareaEl.value || '').trim();
    if (behaviorName !== null) {
        vscode.postMessage({
            command: 'setBehaviorSpecialInstructions',
            behaviorName: behaviorName,
            instructionText: instructionText
        });
    }
};

window.setActionSpecialInstructions = function(textareaEl) {
    if (!textareaEl || textareaEl.tagName !== 'TEXTAREA') return;
    const behaviorName = textareaEl.getAttribute('data-behavior-name');
    const actionName = textareaEl.getAttribute('data-action-name');
    const instructionText = (textareaEl.value || '').trim();
    if (behaviorName !== null && actionName !== null) {
        vscode.postMessage({
            command: 'setActionSpecialInstructions',
            behaviorName: behaviorName,
            actionName: actionName,
            instructionText: instructionText
        });
    }
};

function submitToChat() {
    console.log('[SUBMIT_DEBUG] WebView: submitToChat() posting sendToChat');
    vscode.postMessage({
        command: 'sendToChat'
    });
}

function sendInstructionsToChat(event) {
    if (event) {
        event.stopPropagation();
    }
    console.log('[SUBMIT_DEBUG] WebView: sendInstructionsToChat triggered');

    if (window.selectedNode && window.selectedNode.name) {
        const nodePath = resolveNodePath(window.selectedNode);
        if (nodePath) {
            console.log('[SUBMIT_DEBUG] WebView: taking handleSubmitCurrent path (story map node selected)');
            handleSubmitCurrent();
            return;
        }
    }

    console.log('[SUBMIT_DEBUG] WebView: taking submitToChat path (behaviors submit)');
    submitToChat();
}

function refreshStatus() {
    vscode.postMessage({
        command: 'refresh'
    });
}


let pendingOperations = 0;

function showSaveStatus(operationCount) {
    console.log('[ASYNC_SAVE] [STEP 1] showSaveStatus() called operationCount=' + operationCount + ' timestamp=' + new Date().toISOString());
    pendingOperations = operationCount;
    const indicator = document.getElementById('save-status-indicator');
    const spinner = document.getElementById('save-status-spinner');
    const message = document.getElementById('save-status-message');
    
    if (!indicator) {
        console.error('[ASYNC_SAVE] [ERROR] save-status-indicator element not found!');
        return;
    }
    if (!spinner) {
        console.error('[ASYNC_SAVE] [ERROR] save-status-spinner element not found!');
        return;
    }
    if (!message) {
        console.error('[ASYNC_SAVE] [ERROR] save-status-message element not found!');
        return;
    }
    
    console.log('[ASYNC_SAVE] [STEP 2] Setting indicator display to flex');
    indicator.style.display = 'flex';
    spinner.style.display = 'inline-block';
    const statusMessage = operationCount > 1 
        ? 'Saving ' + operationCount + ' changes...' 
        : 'Saving 1 change...';
    message.textContent = statusMessage;
    console.log('[ASYNC_SAVE] [STEP 3] Status indicator visible indicatorDisplay=' + indicator.style.display + ' spinnerDisplay=' + spinner.style.display + ' messageText=' + statusMessage + ' elementVisible=' + (indicator.offsetParent !== null));
}

function hideSaveStatus() {
    console.log('[ASYNC_SAVE] hideSaveStatus() called timestamp=' + new Date().toISOString());
    const indicator = document.getElementById('save-status-indicator');
    if (indicator) {
        indicator.style.display = 'none';
        console.log('[ASYNC_SAVE] Status indicator hidden');
    }
    pendingOperations = 0;
}

function showSaveSuccess() {
    console.log('[ASYNC_SAVE] [SUCCESS] showSaveSuccess() called timestamp=' + new Date().toISOString());
    const indicator = document.getElementById('save-status-indicator');
    const spinner = document.getElementById('save-status-spinner');
    const message = document.getElementById('save-status-message');
    if (indicator && spinner && message) {
        console.log('[ASYNC_SAVE] [SUCCESS] Updating indicator to show success');
        indicator.style.display = 'flex';
        spinner.style.display = 'none';
        message.textContent = 'Saved';
        message.style.color = '#ff8c00';
        console.log('[ASYNC_SAVE] [SUCCESS] Scheduling auto-hide in 2000ms');
        setTimeout(() => {
            console.log('[ASYNC_SAVE] [SUCCESS] Auto-hide timeout fired, hiding indicator');
            hideSaveStatus();
        }, 2000);
    } else {
        console.error('[ASYNC_SAVE] [ERROR] Cannot show success - elements missing hasIndicator=' + !!indicator + ' hasSpinner=' + !!spinner + ' hasMessage=' + !!message);
    }
}

function showSaveError(errorMessage) {
    console.log('[ASYNC_SAVE] [ERROR] showSaveError() called errorMessage=' + errorMessage + ' timestamp=' + new Date().toISOString());
    const indicator = document.getElementById('save-status-indicator');
    const spinner = document.getElementById('save-status-spinner');
    const message = document.getElementById('save-status-message');
    if (indicator && spinner && message) {
        console.log('[ASYNC_SAVE] [ERROR] Updating indicator to show error');
        indicator.style.display = 'flex';
        spinner.style.display = 'none';
        message.textContent = 'Save failed - click for details';
        message.style.color = '#f48771';
        message.style.cursor = 'pointer';
        message.onclick = function() {
            console.log('[ASYNC_SAVE] [ERROR] Error indicator clicked, showing alert');
            alert('Save Error: ' + errorMessage);
        };
        console.log('[ASYNC_SAVE] [ERROR] Error indicator displayed (will not auto-hide)');
    } else {
        console.error('[ASYNC_SAVE] [ERROR] Cannot show error - elements missing hasIndicator=' + !!indicator + ' hasSpinner=' + !!spinner + ' hasMessage=' + !!message);
    }
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


window.switchBot = function(botName) {
    console.log('[WebView] switchBot called with:', botName);
    vscode.postMessage({
        command: 'switchBot',
        botName: botName
    });
};

window.getBehaviorRules = function(behaviorName) {
    console.log('[WebView] getBehaviorRules called with:', behaviorName);
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] getBehaviorRules BUTTON CLICKED for: ' + behaviorName
    });
    vscode.postMessage({
        command: 'getBehaviorRules',
        behaviorName: behaviorName
    });
};


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

function _incCmd(commandText) {
    console.log('[INCREMENT] >>> Sending command:', commandText);
    vscode.postMessage({ command: 'logToFile', message: '[INCREMENT][UI->CLI] ' + commandText });
    vscode.postMessage({ command: 'executeCommand', commandText: commandText });
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


window.behaviorToTooltipText = function(behavior) {
    var behaviorMap = {
        'shape': 'Shape',
        'exploration': 'Explore',
        'scenarios': 'Write Scenarios for',
        'tests': 'Write Tests for',
        'code': 'Write Code for'
    };
    return behaviorMap[behavior] || 'Submit';
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

window.submitWorkspaceBehaviorInstructions = function() {
    const behavior = window.currentBehavior || null;
    if (!behavior) {
        vscode.postMessage({ command: 'showScopeError', message: 'Select a behavior in Workspace first (click a behavior button).' });
        return;
    }
    const action = window.currentAction || 'build';
    if (window.selectedNode && window.selectedNode.name) {
        const nodePath = resolveNodePath(window.selectedNode);
        if (nodePath) {
            let commandText;
            if (window.selectedNode.type === 'increment') {
                commandText = 'story_graph.submit_increment_instructions name:"' + window.selectedNode.name + '" behavior:"' + behavior + '" action:"' + action + '"';
            } else {
                commandText = nodePath + '.submit_instructions behavior:"' + behavior + '" action:"' + action + '"';
            }
            vscode.postMessage({ command: 'executeCommand', commandText: commandText });
            return;
        }
    }
    vscode.postMessage({ command: 'submitWorkspaceBehaviorInstructions', behavior: behavior });
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


function getWorkspaceDir() {

    if (window.botData && window.botData.workspace_directory) {
        return window.botData.workspace_directory;
    }

    const storyGraphPath = 'docs/story/story-graph.json';
    return '';
}


function openFileInColumn(filePath, viewColumn) {
    vscode.postMessage({
        command: 'openFileInColumn',
        filePath: filePath,
        viewColumn: viewColumn
    });
}

window.handleOpenFile = function() {
    const fileLink = getSelectedNodeFileLink();
    if (!window.selectedNode || !window.selectedNode.name) return;
    if (fileLink && window.openFile) {
        window.openFile(fileLink);
    }
};

window.handleOpenTest = function() {
    const testFiles = getSelectedNodeTestFiles();
    if (!window.selectedNode || !window.selectedNode.name) return;
    if (testFiles.length > 0 && window.openFiles) {
        window.openFiles(testFiles);
    }
};

window.handleOpenGraph = function() {
    console.log('[WebView] handleOpenGraph called');
    console.log('[WebView] selectedNode:', window.selectedNode);
    
    if (!window.selectedNode) {
        console.error('[WebView] No node selected');
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] ERROR: handleOpenGraph called but no node selected'
        });
        return;
    }
    
    const workspaceDir = getWorkspaceDir();
    const storyGraphPath = workspaceDir ? workspaceDir + '/docs/story/story-graph.json' : 'docs/story/story-graph.json';
    
    console.log('[WebView] Opening story graph:', storyGraphPath);
    console.log('[WebView] Node path:', window.selectedNode.path);
    

    vscode.postMessage({
        command: 'openFileWithState',
        filePath: storyGraphPath,
        state: {
            collapseAll: true,
            expandPath: window.selectedNode.path || null,
            selectedNode: window.selectedNode,
            positionCursor: true
        }
    });
};

window.handleOpenStories = function() {
    console.log('[WebView] handleOpenStories called');
    const fileLink = getSelectedNodeFileLink();
    
    if (!window.selectedNode || !window.selectedNode.name) {
        console.error('[WebView] No node selected');
        return;
    }
    

    vscode.postMessage({
        command: 'openStoryFiles',
        nodeType: window.selectedNode.type,
        nodeName: window.selectedNode.name,
        nodePath: window.selectedNode.path,
        singleFileLink: fileLink
    });
};

window.handleOpenAll = function() {
    console.log('[WebView] handleOpenAll called');
    
    if (!window.selectedNode || !window.selectedNode.name) {
        console.error('[WebView] No node selected');
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] ERROR: handleOpenAll called but no node selected'
        });
        return;
    }
    
    const fileLink = getSelectedNodeFileLink();
    const workspaceDir = getWorkspaceDir();
    const storyGraphPath = workspaceDir ? workspaceDir + '/docs/story/story-graph.json' : 'docs/story/story-graph.json';
    

    let testFiles = [];
    let storyFiles = [];
    const selectedNodePath = window.selectedNode.path;
    const nodeType = window.selectedNode.type;
    
    if (selectedNodePath) {
        const allNodes = document.querySelectorAll('.story-node[data-path]');
        let nodeEl = null;
        for (const el of allNodes) {
            if (el.getAttribute('data-path') === selectedNodePath) {
                nodeEl = el;
                break;
            }
        }
        
        if (nodeEl) {
            if (nodeType === 'sub-epic' || nodeType === 'epic') {


                const parentDiv = nodeEl.closest('div');
                const collapsibleDiv = parentDiv ? parentDiv.nextElementSibling : null;
                
                if (collapsibleDiv && collapsibleDiv.classList.contains('collapsible-content')) {

                    const childStoryNodes = collapsibleDiv.querySelectorAll('.story-node[data-node-type="story"]');
                    childStoryNodes.forEach(function(storyEl) {
                        const link = storyEl.getAttribute('data-file-link');
                        if (link) {
                            storyFiles.push(link);
                        }
                    });
                    

                    const testFileEls = collapsibleDiv.querySelectorAll('.story-node[data-test-files]');
                    testFileEls.forEach(function(el) {
                        try {
                            var files = JSON.parse(el.getAttribute('data-test-files'));
                            if (Array.isArray(files)) {
                                files.forEach(function(f) {
                                    if (testFiles.indexOf(f) === -1) testFiles.push(f);
                                });
                            }
                        } catch (e) {
                            console.error('[WebView] Error parsing child test_files:', e);
                        }
                    });
                }
                console.log('[WebView] Sub-epic/epic: found', storyFiles.length, 'story files and', testFiles.length, 'test files');
            } else {

                const testFilesAttr = nodeEl.getAttribute('data-test-files');
                if (testFilesAttr) {
                    try {
                        testFiles = JSON.parse(testFilesAttr);
                        console.log('[WebView] Found test_files from DOM:', testFiles);
                    } catch (e) {
                        console.error('[WebView] Error parsing test_files:', e);
                    }
                }
            }
        }
    }
    
    console.log('[WebView] handleOpenAll - selectedNode:', JSON.stringify(window.selectedNode));
    console.log('[WebView] handleOpenAll - fileLink:', fileLink);
    console.log('[WebView] handleOpenAll - storyFiles:', storyFiles);
    console.log('[WebView] handleOpenAll - testFiles:', testFiles);
    

    vscode.postMessage({
        command: 'openAllRelatedFiles',
        nodeType: window.selectedNode.type,
        nodeName: window.selectedNode.name,
        nodePath: window.selectedNode.path,
        singleFileLink: fileLink,
        storyFiles: storyFiles,
        testFiles: testFiles,
        storyGraphPath: storyGraphPath,
        selectedNode: window.selectedNode
    });
};



setTimeout(function() {
    window.selectNode('root', null);
}, 100);


document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {

        try { sessionStorage.removeItem('selectedNode'); } catch(err) {}
        window.diagramScope = '';
        window.selectNode('root', null);
    }
});


window.toggleQAExpand = function(idx, prefix) {
    const p = prefix || '';
    const textarea = document.getElementById(p + 'clarify-answer-' + idx);
    const toggleBtn = document.getElementById(p + 'qa-toggle-' + idx);
    if (!textarea) return;
    
    const isCollapsed = textarea.getAttribute('data-collapsed') === 'true';
    
    if (isCollapsed) {
        textarea.style.display = '';
        textarea.style.height = 'auto';
        const fullHeight = textarea.scrollHeight;
        textarea.style.height = fullHeight + 'px';
        textarea.style.overflow = 'visible';
        textarea.setAttribute('data-collapsed', 'false');
        if (toggleBtn) toggleBtn.textContent = '▲';
    } else {
        textarea.style.display = 'none';
        textarea.style.height = '';
        textarea.style.overflow = 'hidden';
        textarea.setAttribute('data-collapsed', 'true');
        if (toggleBtn) toggleBtn.textContent = '▼';
    }
    if (p === 'ws-' && window.currentBehavior && window.saveClarifyQACollapseState) {
        window.saveClarifyQACollapseState(window.currentBehavior);
    }
};

window.toggleTextareaExpand = function(textareaId) {
    const textarea = document.getElementById(textareaId);
    const toggleBtn = document.getElementById(textareaId + '-toggle');
    if (!textarea) return;
    
    const isCollapsed = textarea.getAttribute('data-collapsed') === 'true';
    
    if (isCollapsed) {
        textarea.style.display = '';
        textarea.style.overflow = 'visible';
        textarea.setAttribute('data-collapsed', 'false');
        if (toggleBtn) toggleBtn.textContent = '▲';
    } else {
        textarea.style.display = 'none';
        textarea.style.overflow = 'hidden';
        textarea.setAttribute('data-collapsed', 'true');
        if (toggleBtn) toggleBtn.textContent = '▼';
    }
    if (window.currentBehavior && window.saveTextareaCollapseState) {
        window.saveTextareaCollapseState(window.currentBehavior);
    }
};


window.saveClarifyAnswers = function() {
    console.log('[WebView] saveClarifyAnswers triggered');
    const answers = {};
    const answerElements = document.querySelectorAll('[id*="clarify-answer-"]');
    
    answerElements.forEach((textarea) => {
        const question = textarea.getAttribute('data-question');
        const answer = textarea.value?.trim();
        if (question && answer) {
            answers[question] = answer;
        }
    });
    
    if (Object.keys(answers).length > 0) {
        console.log('[WebView] Saving clarify answers:', answers);
        vscode.postMessage({
            command: 'saveClarifyAnswers',
            answers: answers
        });
    }
};

window.saveClarifyEvidence = function() {
    console.log('[WebView] saveClarifyEvidence triggered');
    const evidenceTextarea = document.getElementById('ws-clarify-evidence') || document.getElementById('clarify-evidence');
    if (evidenceTextarea) {
        const evidenceText = evidenceTextarea.value?.trim();
        if (evidenceText) {

            const evidenceProvided = {};
            evidenceText.split(/\n/).forEach(line => {
                const colonIdx = line.indexOf(':');
                if (colonIdx > 0) {
                    const key = line.substring(0, colonIdx).trim();
                    const value = line.substring(colonIdx + 1).trim();
                    if (key && value) {
                        evidenceProvided[key] = value;
                    }
                }
            });
            
            if (Object.keys(evidenceProvided).length > 0) {
                console.log('[WebView] Saving clarify evidence:', evidenceProvided);
                vscode.postMessage({
                    command: 'saveClarifyEvidence',
                    evidence_provided: evidenceProvided
                });
            }
        }
    }
};

window.saveStrategyDecision = function(criteriaKey, selectedOption) {
    console.log('[WebView] saveStrategyDecision triggered:', criteriaKey, selectedOption);
    vscode.postMessage({
        command: 'saveStrategyDecision',
        criteriaKey: criteriaKey,
        selectedOption: selectedOption
    });
};


window.saveStrategyMultiDecision = function(criteriaKey, inputName) {
    console.log('[WebView] saveStrategyMultiDecision triggered:', criteriaKey, inputName);
    const checkboxes = document.querySelectorAll('input[name="' + inputName + '"]:checked');
    const selectedOptions = [];
    checkboxes.forEach(cb => {

        const label = cb.closest('label');
        if (label) {
            const span = label.querySelector('span');
            if (span) {
                selectedOptions.push(span.textContent);
            }
        }
    });
    console.log('[WebView] Saving multi-select decision:', criteriaKey, selectedOptions);
    vscode.postMessage({
        command: 'saveStrategyMultiDecision',
        criteriaKey: criteriaKey,
        selectedOptions: selectedOptions
    });
};

window.saveStrategyAssumptions = function() {
    console.log('[WebView] saveStrategyAssumptions triggered');
    const assumptionsTextarea = document.getElementById('ws-strategy-assumptions') || document.getElementById('strategy-assumptions');
    if (assumptionsTextarea) {
        const assumptionsText = assumptionsTextarea.value?.trim();
        if (assumptionsText) {
            const assumptions = assumptionsText.split(/\n/).filter(a => a.trim());
            console.log('[WebView] Saving strategy assumptions:', assumptions);
            vscode.postMessage({
                command: 'saveStrategyAssumptions',
                assumptions: assumptions
            });
        }
    }
};



window.addEventListener('message', event => {
    const message = event.data;
    console.log('[WebView] Received message from extension:', message);
    
    if (message.command === 'incrementCommandResult') {
        var status = (message.result && message.result.status) ? message.result.status : 'unknown';
        console.log('[INCREMENT][CLI->UI] Response received. command=' + message.commandText + ' status=' + status + ' result=' + JSON.stringify(message.result));
        return;
    }
    
    if (message.command === 'saveCompleted') {
        console.log('[ASYNC_SAVE] [WEBVIEW] [STEP 10] Received saveCompleted message from extension host success=' + message.success + ' error=' + (message.error || 'none') + ' timestamp=' + new Date().toISOString());
        if (message.success) {
            console.log('[ASYNC_SAVE] [WEBVIEW] [STEP 10] Processing success response');
            showSaveSuccess();
        } else {
            console.log('[ASYNC_SAVE] [WEBVIEW] [STEP 10] Processing error response error=' + (message.error || 'Unknown error'));
            showSaveError(message.error || 'Unknown error');
        }
        console.log('[ASYNC_SAVE] [WEBVIEW] ========== SAVE FLOW COMPLETE ==========');
        return;
    }
    
    if (message.command === 'optimisticRename') {
        console.log('[WebView] Received optimisticRename message:', message);

        if (typeof window.handleRenameNode === 'function') {
            console.log('[WebView] Using optimistic rename handler');
            window.handleRenameNode({
                nodePath: message.nodePath,
                oldName: message.oldName,
                newName: message.newName
            });
        } else {
            console.warn('[WebView] handleRenameNode not available');
        }
        return;
    }
    
    if (message.command === 'setWorkspacePath') {
        setWorkspacePath(message.path);
        return;
    }
    
    if (message.command === 'expandInstructionsSection') {
        console.log('[WebView] Received expandInstructionsSection message:', message.actionName);
        try {
            if (message.actionName && typeof window.expandInstructionsSection === 'function') {
                window.expandInstructionsSection(message.actionName);
            }
        } catch (err) {
            console.error('[WebView] Error in expandInstructionsSection handler:', err);
        }
        return;
    }
    
    if (message.command === 'diagramFileChanged') {
        var ds = document.getElementById('diagram-section');
        if (ds && message.diagram) {
            var d = message.diagram;
            var isStale = d.file_modified_time && d.last_sync_time && d.file_modified_time > d.last_sync_time;
            var neverSynced = !d.last_sync_time;
            var needsAction = isStale || neverSynced;
            var staleEl = ds.querySelector('.stale-indicator');
            var linkParent = ds.querySelector('.diagram-link');
            if (linkParent) { linkParent = linkParent.parentElement; }
            if (needsAction && !staleEl && linkParent) {
                var ind = document.createElement('span');
                ind.className = 'stale-indicator';
                ind.style.cssText = 'color: var(--vscode-editorWarning-foreground); margin-left: 8px;';
                ind.textContent = 'Diagram Changes Not In Graph';
                linkParent.appendChild(ind);
            }
            if (needsAction && !ds.querySelector('.generate-report-button')) {
                var btnDiv = ds.querySelector('.diagram-item');
                if (btnDiv) { btnDiv = btnDiv.lastElementChild; }
                if (btnDiv) {
                    var genBtn = document.createElement('button');
                    genBtn.className = 'generate-report-button';
                    genBtn.textContent = 'Generate Report';
                    genBtn.style.cssText = 'margin: 4px 4px 4px 0; cursor: pointer;';
                    genBtn.onclick = function() { vscode.postMessage({ command: 'generateDiagramReport', path: d.file_path }); };
                    btnDiv.appendChild(genBtn);
                }
            }
        }
        return;
    }
    
    if (message.command === 'displayError') {

        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = 'position: fixed; top: 10px; left: 10px; right: 10px; z-index: 10000; background: #f44336; color: white; padding: 16px; border-radius: 4px; font-family: monospace; font-size: 12px; white-space: pre-wrap; max-height: 80vh; overflow-y: auto;';
        errorDiv.textContent = '[ERROR] ' + message.error;
        

        const btnContainer = document.createElement('div');
        btnContainer.style.cssText = 'margin-top: 12px; display: flex; gap: 8px;';
        

        const retryBtn = document.createElement('button');
        retryBtn.textContent = '🔄 Retry';
        retryBtn.style.cssText = 'background: white; color: #f44336; border: none; padding: 8px 16px; cursor: pointer; border-radius: 3px; font-weight: bold;';
        retryBtn.onclick = () => {
            errorDiv.remove();
            vscode.postMessage({ command: 'refresh' });
        };
        

        const closeBtn = document.createElement('button');
        closeBtn.textContent = 'Close';
        closeBtn.style.cssText = 'background: rgba(255,255,255,0.8); color: #f44336; border: none; padding: 8px 16px; cursor: pointer; border-radius: 3px;';
        closeBtn.onclick = () => errorDiv.remove();
        
        btnContainer.appendChild(retryBtn);
        btnContainer.appendChild(closeBtn);
        errorDiv.appendChild(btnContainer);
        
        document.body.appendChild(errorDiv);
        

        setTimeout(() => errorDiv.remove(), 30000);
    }
    
    if (message.command === 'restoreCollapseState') {
        console.log('[WebView] Restoring collapse state after refresh');
        const savedState = sessionStorage.getItem('collapseState');
        if (savedState) {
            try {
                const state = JSON.parse(savedState);
                window.restoreCollapseState(state);
                console.log('[WebView] Restored collapse state for', Object.keys(state).length, 'sections');
            } catch (err) {
                console.error('[WebView] Failed to restore collapse state:', err);
            }
        } else {
            console.log('[WebView] No saved collapse state found');
        }
    }
    
    if (message.command === 'optimisticRename') {
        console.log('[WebView] Optimistic rename disabled - waiting for full refresh');

    }
    

    if (message.command === 'revertRename') {
        console.log('[WebView] Revert rename command received but not needed');
    }
});