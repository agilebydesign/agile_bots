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
    if (storyNode && !storyNode.getAttribute('data-inc-source')) {
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
                const wsContainer = actionElement.closest('#ws-behavior-exec-toggle');
                if (wsContainer && wsContainer.classList.contains('execution-toggle-container') && wsContainer.classList.contains('expanded')) {
                    wsContainer.classList.remove('expanded');
                    const currentState = window.getCollapseState();
                    sessionStorage.setItem('collapseState', JSON.stringify(currentState));
                }
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
    if (target && target.classList.contains('story-node') && !target.getAttribute('data-inc-source')) {
        const nodePath = target.getAttribute('data-path');
        if (nodePath) {
            var scope = window.diagramScope || '';
            var fileLink = target.getAttribute('data-file-link');
            var nodeType = target.getAttribute('data-node-type') || 'story';
            var nodeName = target.getAttribute('data-node-name') || '';
            var menuItems = [];
            menuItems.push({ label: 'Open Story File', action: function() {
                if (fileLink) {
                    vscode.postMessage({ command: 'openFile', filePath: fileLink });
                } else {
                    vscode.postMessage({
                        command: 'openStoryFiles',
                        nodeType: nodeType,
                        nodeName: nodeName,
                        nodePath: nodePath
                    });
                }
            }});
            menuItems.push({ label: 'Open Test', action: function() {
                vscode.postMessage({
                    command: 'openTestFiles',
                    nodeType: nodeType,
                    nodeName: nodeName,
                    nodePath: nodePath
                });
            }});
            menuItems.push({ separator: true });
            menuItems.push(
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
            );
            _showCopyMenu(e, menuItems);
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

let dragoverLogThrottle = 0;
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
    

    if (dragoverLogThrottle++ % 20 === 0 && draggedNode) {
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
                if (dragoverLogThrottle % 20 === 0) {
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

                if (dragoverLogThrottle % 20 === 0) {
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

// saveClarifyQACollapseState and restoreClarifyQACollapseState moved to instructions_client.js

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


// expandClarifyBoxes moved to instructions_client.js


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

function _incCmd(commandText) {
    console.log('[INCREMENT] >>> Sending command:', commandText);
    vscode.postMessage({ command: 'logToFile', message: '[INCREMENT][UI->CLI] ' + commandText });
    vscode.postMessage({ command: 'executeCommand', commandText: commandText });
}

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

window.submitWorkspaceBehaviorInstructions = function() {
    const behavior = window.currentBehavior || null;
    if (!behavior) {
        vscode.postMessage({ command: 'showScopeError', message: 'Select a behavior in Workspace first (click a behavior button).' });
        return;
    }
    const action = window.currentAction || 'build';
    if (window.selectedNode && window.selectedNode.name) {
        if (window.selectedNode.type === 'increment') {
            const commandText = 'story_graph.submit_increment_instructions name:"' + window.selectedNode.name + '" behavior:"' + behavior + '" action:"' + action + '"';
            vscode.postMessage({ command: 'executeCommand', commandText: commandText });
            return;
        }
        const nodePath = resolveNodePath(window.selectedNode);
        if (nodePath) {
            const commandText = nodePath + '.submit_instructions behavior:"' + behavior + '" action:"' + action + '"';
            vscode.postMessage({ command: 'executeCommand', commandText: commandText });
            return;
        }
    }
    // When behavior is expanded and an action is selected: submit action only (sendToChat).
    // When behavior is collapsed: submit entire behavior.
    const wsToggle = document.getElementById('ws-behavior-exec-toggle');
    const isBehaviorExpanded = wsToggle && wsToggle.classList.contains('execution-toggle-container') && wsToggle.classList.contains('expanded');
    if (isBehaviorExpanded && action) {
        vscode.postMessage({ command: 'sendToChat' });
        return;
    }
    vscode.postMessage({ command: 'submitWorkspaceBehaviorInstructions', behavior: behavior });
};

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
    
    const workspaceDir = getWorkspaceDir(); // from workspace_client.js
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
    const workspaceDir = getWorkspaceDir(); // from workspace_client.js
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

// saveClarifyEvidence moved to instructions_client.js

// saveStrategyDecision, saveStrategyMultiDecision, saveStrategyAssumptions moved to instructions_client.js

window.switchBot = function(botName) {
    console.log('[WebView] switchBot called with:', botName);
    vscode.postMessage({
        command: 'switchBot',
        botName: botName
    });
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
        setWorkspacePath(message.path); // in workspace_client.js
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