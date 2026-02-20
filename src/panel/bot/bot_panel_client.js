// This is the main client-side script which acquires the vscode API
// All other client-side scripts can use it (because they assembled into a single script by bot_panel)
// But the other scripts must not call acquireVsCodeApi() themselves

const vscode = acquireVsCodeApi();
console.log('[WebView] ========== SCRIPT LOADING ==========');
console.log('[WebView] vscode API acquired:', !!vscode);
console.log('[WebView] vscode.postMessage available:', typeof vscode.postMessage);


// Restore collapse state and selected node when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    try {
        // Restore collapse state
        const savedState = sessionStorage.getItem('collapseState');
        if (savedState) {
            const state = JSON.parse(savedState);
            // Use setTimeout to ensure DOM is fully rendered
            setTimeout(() => window.restoreCollapseState(state), 50);
            console.log('[WebView] Restored collapse state for', Object.keys(state).length, 'nodes');
        }
        
        // Restore selected node
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
        
        // Restore scroll position after a short delay to ensure content is rendered
        setTimeout(() => {
            if (window.restoreScrollPosition) {
                window.restoreScrollPosition();
            }
        }, 150);
    } catch (err) {
        console.error('[WebView] Error restoring state:', err);
    }
});

// Save scroll position when page loses visibility (e.g., when opening a file)
document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'hidden') {
        if (window.saveScrollPosition) {
            window.saveScrollPosition();
        }
    } else if (document.visibilityState === 'visible') {
        // Restore scroll position when becoming visible again
        setTimeout(() => {
            if (window.restoreScrollPosition) {
                window.restoreScrollPosition();
            }
        }, 50);
    }
});

// Global click handler using event delegation (CSP blocks inline onclick)
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
    
    // Handle story node clicks (epic, sub-epic, story)
    if (target.classList.contains('story-node')) {
        console.log('═══════════════════════════════════════════════════════');
        console.log('[WebView] STORY NODE CLICKED');
        const nodeType = target.getAttribute('data-node-type');
        const nodeName = target.getAttribute('data-node-name');
        const hasChildren = target.getAttribute('data-has-children') === 'true';
        const hasStories = target.getAttribute('data-has-stories') === 'true';
        const hasNestedSubEpics = target.getAttribute('data-has-nested-sub-epics') === 'true';
        const nodePath = target.getAttribute('data-path');
        const fileLink = target.getAttribute('data-file-link');
        const behavior = target.getAttribute('data-behavior-needed') || null;
        const behaviorsAttr = target.getAttribute('data-behaviors-needed');
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
        
        // Call selectNode
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
        
        // Call openFile if there's a file link
        if (window.openFile && fileLink) {
            console.log('[WebView]   Opening file:', fileLink);
            window.openFile(fileLink);
        }
        
        e.stopPropagation();
        console.log('═══════════════════════════════════════════════════════');
    }
    
    // Handle behavior and action clicks (CSP-safe event delegation)
    // Traverse up the DOM tree to find element with data-action attribute
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
            if (behaviorName && window.navigateToBehavior) {
                window.navigateToBehavior(behaviorName);
                e.stopPropagation();
                e.preventDefault();
            }
        } else if (action === 'navigateToAction') {
            const behaviorName = actionElement.getAttribute('data-behavior-name');
            const actionName = actionElement.getAttribute('data-action-name');
            if (behaviorName && actionName && window.navigateToAction) {
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
        }
    }
}, true); // Use capture phase to catch all clicks

// Handle double-click on story nodes to enable edit mode
document.addEventListener('dblclick', function(e) {
    const target = e.target;
    
    // Handle story node double-clicks (epic, sub-epic, story)
    if (target.classList.contains('story-node')) {
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
}, true); // Use capture phase to catch all double-clicks

// Handle drag and drop for moving nodes
let draggedNode = null;
let dropIndicator = null;
let currentDropZone = null; // 'before', 'after', or 'inside'

// Create drop indicator line
function createDropIndicator() {
    if (!dropIndicator) {
        dropIndicator = document.createElement('div');
        dropIndicator.style.position = 'fixed';
        dropIndicator.style.height = '2px';
        dropIndicator.style.backgroundColor = 'rgb(255, 140, 0)'; // Orange to match UI
        dropIndicator.style.pointerEvents = 'none';
        dropIndicator.style.zIndex = '10000';
        dropIndicator.style.transition = 'all 0.1s ease';
        dropIndicator.style.display = 'none'; // Start hidden
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
    
    // Find the story-node element (might be dragging a child element)
    let target = e.target;
    while (target && !target.classList.contains('story-node')) {
        target = target.parentElement;
    }
    
    if (target && target.classList.contains('story-node')) {
        draggedNode = {
            path: target.getAttribute('data-path'),
            name: target.getAttribute('data-node-name'),
            type: target.getAttribute('data-node-type'),
            position: parseInt(target.getAttribute('data-position') || '0')
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
    
    // Find the story-node element
    let target = e.target;
    while (target && !target.classList.contains('story-node')) {
        target = target.parentElement;
    }
    
    if (target && target.classList.contains('story-node')) {
        target.style.opacity = '1';
        draggedNode = null;
        removeDropIndicator();
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] Drag ended, cleared draggedNode'
        });
    }
}, true);

let dragoverLogCounter = 0; // Throttle dragover logs
document.addEventListener('dragover', function(e) {
    // Find the story-node element
    let target = e.target;
    let searchDepth = 0;
    while (target && !target.classList.contains('story-node') && searchDepth < 10) {
        target = target.parentElement;
        searchDepth++;
    }
    
    // Log every 20th dragover event to avoid spam
    if (dragoverLogCounter++ % 20 === 0 && draggedNode) {
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] DRAGOVER - found target: ' + (target ? 'YES' : 'NO') + ', draggedNode: ' + (draggedNode ? draggedNode.name : 'null')
        });
    }
    
    if (target && target.classList.contains('story-node') && draggedNode) {
        const targetType = target.getAttribute('data-node-type');
        const targetPath = target.getAttribute('data-path');
        const targetName = target.getAttribute('data-node-name');
        
        // Don't allow dropping on self
        if (draggedNode.path === targetPath) {
            removeDropIndicator();
            return;
        }
        
        // Check if target can contain dragged node
        const canContain = (targetType === 'epic' && draggedNode.type === 'sub-epic') ||
                            (targetType === 'sub-epic' && (draggedNode.type === 'sub-epic' || draggedNode.type === 'story')) ||
                            (targetType === 'story' && draggedNode.type === 'scenario');
        
        // Check if nodes are same type for reordering
        const sameType = draggedNode.type === targetType;
        
        if (canContain || sameType) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            
            // Get mouse position relative to target element
            const rect = target.getBoundingClientRect();
            const mouseY = e.clientY;
            const targetTop = rect.top;
            const targetHeight = rect.height;
            const relativeY = mouseY - targetTop;
            const percentY = relativeY / targetHeight;
            
            // Determine drop zone based on mouse position
            let dropZone;
            const indicator = createDropIndicator();
            
            // Check if target can contain the dragged node
            const hasStories = target.getAttribute('data-has-stories') === 'true';
            const hasNestedSubEpics = target.getAttribute('data-has-nested-sub-epics') === 'true';
            const isEmptyContainer = !hasStories && !hasNestedSubEpics;
            
            // "ON" vs "AFTER" logic:
            // - If hovering directly on item (middle 60%) AND can nest inside: show "inside" (orange background, no line)
            // - Otherwise: show "after" (orange line below item)
            if (canContain && percentY >= 0.2 && percentY <= 0.8) {
                // Hovering ON the item - nest inside
                dropZone = 'inside';
                target.style.backgroundColor = 'rgba(255, 140, 0, 0.3)'; // Orange tint for nesting
                indicator.style.display = 'none';
                if (dragoverLogCounter % 20 === 0) {
                    vscode.postMessage({
                        command: 'logToFile',
                        message: '[WebView] DRAGOVER ON (inside) - will nest inside ' + target.getAttribute('data-node-name')
                    });
                }
            } else if (sameType) {
                // Same type: insert after
                dropZone = 'after';
                target.style.backgroundColor = '';
                indicator.style.display = 'block';
                indicator.style.left = rect.left + 'px';
                indicator.style.top = (rect.top + rect.height) + 'px';
                indicator.style.width = rect.width + 'px';
                // Log indicator positioning
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
    }
}, true);

document.addEventListener('dragleave', function(e) {
    // Find the story-node element
    let target = e.target;
    while (target && !target.classList.contains('story-node')) {
        target = target.parentElement;
    }
    
    if (target && target.classList.contains('story-node')) {
        target.style.backgroundColor = '';
    }
}, true);

document.addEventListener('drop', function(e) {
    console.log('[WebView] ===== DROP EVENT FIRED =====');
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] ===== DROP EVENT FIRED ===== draggedNode: ' + (draggedNode ? draggedNode.name : 'null') + ', currentDropZone: ' + (currentDropZone || 'null')
    });
    
    // Find the story-node element (might be dropping on a child element)
    let target = e.target;
    while (target && !target.classList.contains('story-node')) {
        target = target.parentElement;
    }
    
    if (target && target.classList.contains('story-node') && draggedNode && currentDropZone) {
        e.preventDefault();
        e.stopPropagation();
        target.style.backgroundColor = '';
        
        // Save dropZone BEFORE removeDropIndicator clears it
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
            
            // Optimistic update disabled - full refresh preserves structure correctly
            console.log('[WebView] Move operation - waiting for backend and full refresh');
            
            let command;
            
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] COMMAND CONSTRUCTION - dropZone: ' + dropZone
            });
            
            if (dropZone === 'inside') {
                // ON: Nest inside the target container - use FULL PATH not just name to avoid ambiguity
                // targetPath is like: story_graph."Epic1"."Child1"
                // Backend expects: target:"Epic1"."Child1" (path with internal quotes, no outer wrapping)
                var targetForCommand = targetPath.replace(/^story_graph\./, '');
                // targetForCommand already has quotes around each segment (e.g., "Epic1"."Child1")
                // Do NOT wrap in additional quotes
                command = draggedNode.path + '.move_to target:' + targetForCommand;
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] INSIDE COMMAND - targetPath: ' + targetPath + ', targetForCommand: ' + targetForCommand + ', command: ' + command
                });
            } else if (dropZone === 'after') {
                var targetPos = parseInt(target.getAttribute('data-position') || '0');
                var draggedPos = draggedNode.position;
                
                // Extract parent path (everything except the last segment)
                // targetPath is like: story_graph."Epic1"."Child1"."Story1"
                // parentPath should be: story_graph."Epic1"."Child1"
                var parentMatch = targetPath.match(/(.*)\."[^"]+"/);
                var parentPath = parentMatch ? parentMatch[1] : 'story_graph';
                
                // Strip off "story_graph." prefix to get the target parameter value
                var targetForCommand = parentPath.replace(/^story_graph\./, '');
                
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] AFTER CALCULATION - targetPos: ' + targetPos + ', draggedPos: ' + draggedPos + ', parentPath: ' + parentPath + ', targetForCommand: ' + targetForCommand
                });
                
                // When moving DOWN (to later position), use targetPos as-is (item shifts down)
                // When moving UP (to earlier position), use targetPos + 1 (drop after target)
                var finalPos = (draggedPos < targetPos) ? targetPos : (targetPos + 1);
                
                command = draggedNode.path + '.move_to target:' + targetForCommand + ' at_position:' + finalPos;
                vscode.postMessage({
                    command: 'logToFile',
                    message: '[WebView] AFTER COMMAND - dragged from ' + draggedPos + ' to position: ' + finalPos + ' (target was at ' + targetPos + '), command: ' + command
                });
            }
            
            // ========== ASYNC SAVE FLOW: MOVE OPERATION ==========
            // Use StoryMapView handler for optimistic updates
            if (dropZone === 'after' && typeof window.handleMoveNode === 'function') {
                // Calculate parent path and position
                var parentMatch = targetPath.match(/(.*)\."[^"]+"/);
                var parentPath = parentMatch ? parentMatch[1] : 'story_graph';
                var finalPos = (draggedNode.position < targetPos) ? targetPos : (targetPos + 1);
                
                // Call StoryMapView handler - pass targetPath so we can insert after the specific node
                window.handleMoveNode({
                    sourceNodePath: draggedNode.path,
                    targetParentPath: parentPath,
                    targetNodePath: targetPath,  // Pass target node path for "after" positioning
                    position: finalPos,
                    dropZone: 'after'
                });
            } else if (dropZone === 'inside' && typeof window.handleMoveNode === 'function') {
                // Moving inside target
                window.handleMoveNode({
                    sourceNodePath: draggedNode.path,
                    targetParentPath: targetPath,
                    position: 0,
                    dropZone: 'inside'
                });
            } else {
                // Fallback: send command directly (defaults to optimistic for story-changing ops)
                console.warn('[WebView] handleMoveNode not available, sending command directly');
                vscode.postMessage({
                    command: 'executeCommand',
                    commandText: command
                    // optimistic defaults to true for story-changing operations
                });
            }
        } else {
            vscode.postMessage({
                command: 'logToFile',
                message: '[WebView] DROP ignored - same node'
            });
        }
    } else {
        removeDropIndicator();
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] DROP ignored - not story-node, no draggedNode, or no dropZone'
        });
    }
}, true);

// Test if onclick handlers can access functions
window.testFunction = function() {
    console.log('[WebView] TEST FUNCTION CALLED - functions are accessible!');
    alert('Test function works!');
};
console.log('[WebView] window.testFunction defined:', typeof window.testFunction);

// Hide panel - sends message to extension to collapse the panel
window.hidePanel = function() {
    console.log('[hidePanel] Requesting panel collapse');
    vscode.postMessage({ command: 'hidePanel' });
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
        
        // Toggle visibility
        if (isExpanded) {
            // Collapsing
            content.style.maxHeight = '0px';
            content.style.overflow = 'hidden';
            content.style.display = 'none';
        } else {
            // Expanding
            content.style.maxHeight = '2000px';
            content.style.overflow = 'visible';
            content.style.display = 'block';
        }
        
        // Toggle expanded class (CSS handles icon rotation - ▸ rotates 90deg when expanded)
        const header = content.previousElementSibling;
        console.log('[toggleSection] Header element:', header);
        if (header && section) {
            section.classList.toggle('expanded', !isExpanded);
            console.log('[toggleSection] After toggle, section classes:', section.className);
            // Keep icon as ▸ always - CSS rotation handles the visual state
            const icon = header.querySelector('.expand-icon');
            console.log('[toggleSection] Icon element:', icon);
            if (icon) {
                icon.textContent = '▸';
                console.log('[toggleSection] Icon transform:', window.getComputedStyle(icon).transform);
            }                    
        }
    }
};

// Expand the instructions section for a specific action (clarify, strategy, build, validate)
// This should ALWAYS expand, never toggle - collapsing is only done by explicit user clicks
window.expandInstructionsSection = function(actionName) {
    console.log('[expandInstructionsSection] Called with actionName:', actionName);
    if (!actionName) return;
    
    // Map action names to section header text
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
    
    // First, collapse all instruction sections (instr-section-*)
    document.querySelectorAll('[id^="instr-section-"]').forEach(content => {
        const section = content.closest('.collapsible-section');
        if (section) {
            content.style.maxHeight = '0px';
            content.style.overflow = 'hidden';
            content.style.display = 'none';
            section.classList.remove('expanded');
        }
    });
    
    // Find the section by looking for header text containing the section name
    const headers = document.querySelectorAll('.collapsible-header');
    for (const header of headers) {
        const headerText = header.textContent || '';
        // Match section name but avoid matching subsections (e.g., "Clarify" but not "Base Instructions")
        if (headerText.includes(sectionName) && !headerText.includes('Base')) {
            const section = header.closest('.collapsible-section');
            const content = header.nextElementSibling;
            
            if (section && content && content.classList.contains('collapsible-content')) {
                console.log('[expandInstructionsSection] Expanding section:', sectionName);
                // Always expand - we already collapsed all sections above
                content.style.maxHeight = '2000px';
                content.style.overflow = 'visible';
                content.style.display = 'block';
                section.classList.add('expanded');
                
                // Update icon
                const icon = header.querySelector('.expand-icon');
                if (icon) {
                    icon.textContent = '▸';
                }
                return; // Found and processed, exit
            }
        }
    }
    console.log('[expandInstructionsSection] Section not found for:', sectionName);
};

// Save/restore collapse state across panel refreshes
window.getCollapseState = function() {
    const state = {};
    document.querySelectorAll('.collapsible-content').forEach(content => {
        if (content.id) {
            state[content.id] = content.style.display !== 'none';
        }
    });
    return state;
};

window.restoreCollapseState = function(state) {
    if (!state) return;
    Object.keys(state).forEach(id => {
        const content = document.getElementById(id);
        if (content) {
            const shouldBeExpanded = state[id];
            content.style.display = shouldBeExpanded ? 'block' : 'none';
            
            // Update icon
            const header = content.previousElementSibling;
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
            }
        }
    });
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
                // Update image src instead of text content - no emojis
                const plusSrc = icon.getAttribute('data-plus');
                const subtractSrc = icon.getAttribute('data-subtract');
                if (plusSrc && subtractSrc) {
                    const img = icon.querySelector('img');
                    if (img) {
                        img.src = isHidden ? subtractSrc : plusSrc;
                    } else {
                        // Create img if it doesn't exist
                        const imgSrc = isHidden ? subtractSrc : plusSrc;
                        const imgAlt = isHidden ? 'Collapse' : 'Expand';
                        icon.innerHTML = '<img src="' + imgSrc + '" style="width: 12px; height: 12px; vertical-align: middle;" alt="' + imgAlt + '" />';
                    }
                }
            }
        }
        
        // Save state to sessionStorage
        const currentState = window.getCollapseState();
        sessionStorage.setItem('collapseState', JSON.stringify(currentState));
    }
};

window.openFile = function(filePath, event) {
    // Prevent default link behavior (scroll to top)
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    console.log('[WebView] openFile called with:', filePath);
    // Save scroll position before opening file (which may cause focus change)
    const savedScrollY = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
    sessionStorage.setItem('scrollPosition', savedScrollY.toString());
    console.log('[WebView] Saved scroll position before file open:', savedScrollY);
    
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] openFile called with: ' + filePath
    });
    vscode.postMessage({
        command: 'openFile',
        filePath: filePath
    });
    
    // Ensure scroll position is preserved after message sending (prevents any DOM reflow issues)
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

// Scroll position preservation functions
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

// Test if updateFilter is defined
console.log('[WebView] updateFilter function exists:', typeof updateFilter);

window.clearScopeFilter = function() {
    vscode.postMessage({
        command: 'clearScopeFilter'
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

function submitToChat() {
    vscode.postMessage({
        command: 'sendToChat'
    });
}

function sendInstructionsToChat(event) {
    if (event) {
        event.stopPropagation();
    }
    console.log('[WebView] sendInstructionsToChat triggered');
    const promptContent = window._promptContent || '';
    if (!promptContent) {
        console.warn('[WebView] No prompt content available to submit');
        return;
    }
    vscode.postMessage({
        command: 'sendToChat',
        content: promptContent
    });
}

function refreshStatus() {
    vscode.postMessage({
        command: 'refresh'
    });
}

// Async save status indicator functions
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

// Optimistic DOM update for move operations
function applyOptimisticMove(draggedNodeElement, targetElement, dropZone, finalPosition) {
    var draggedNodeName = draggedNodeElement ? draggedNodeElement.getAttribute('data-node-name') : null;
    var targetNodeName = targetElement ? targetElement.getAttribute('data-node-name') : null;
    console.log('[ASYNC_SAVE] [OPTIMISTIC] applyOptimisticMove() called dropZone=' + dropZone + ' finalPosition=' + finalPosition + ' draggedNode=' + draggedNodeName + ' targetNode=' + targetNodeName + ' timestamp=' + new Date().toISOString());
    
    if (!draggedNodeElement || !targetElement) {
        console.error('[ASYNC_SAVE] [OPTIMISTIC] [ERROR] Cannot apply optimistic move - missing elements hasDraggedElement=' + !!draggedNodeElement + ' hasTargetElement=' + !!targetElement);
        return;
    }
    
    // Find the parent container
    const draggedParent = draggedNodeElement.parentElement;
    const targetParent = dropZone === 'inside' ? targetElement : targetElement.parentElement;
    
    console.log('[ASYNC_SAVE] [OPTIMISTIC] Found parent elements hasDraggedParent=' + !!draggedParent + ' hasTargetParent=' + !!targetParent + ' sameParent=' + (draggedParent === targetParent));
    
    if (!draggedParent || !targetParent) {
        console.error('[ASYNC_SAVE] [OPTIMISTIC] [ERROR] Cannot apply optimistic move - missing parent elements');
        return;
    }
    
    // If moving within same parent, reorder
    if (draggedParent === targetParent && dropZone === 'after') {
        const targetPos = parseInt(targetElement.getAttribute('data-position') || '0');
        const draggedPos = parseInt(draggedNodeElement.getAttribute('data-position') || '0');
        
        console.log('[ASYNC_SAVE] [OPTIMISTIC] Moving within same parent draggedPos=' + draggedPos + ' targetPos=' + targetPos + ' finalPosition=' + finalPosition + ' dropZone=' + dropZone);
        
        // Remove dragged node from its current position
        const draggedClone = draggedNodeElement.cloneNode(true);
        draggedNodeElement.remove();
        console.log('[ASYNC_SAVE] [OPTIMISTIC] Removed dragged node from original position');
        
        // Find insertion point
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
        
        // Update position attributes
        updateNodePositions(targetParent);
        
        console.log('[ASYNC_SAVE] [OPTIMISTIC] [SUCCESS] Optimistic move applied - node moved in DOM');
    } else if (dropZone === 'inside') {
        // Moving into a container - this is more complex and may require full refresh
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

// function updateWorkspace(workspacePath) {
//     console.log('[WebView] updateWorkspace called with:', workspacePath);
//     vscode.postMessage({
//         command: 'updateWorkspace',
//         workspacePath: workspacePath
//     });
// }

// function browseWorkspace() {
//     console.log('[WebView] browseWorkspace called');
//     vscode.postMessage({
//         command: 'browseWorkspace'
//     });
// }

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

// Story Graph Edit functions
window.createEpic = function() {
    console.log('═══════════════════════════════════════════════════════');
    console.log('[WebView] createEpic CALLED');
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] createEpic called'
    });
    
    // Use optimistic update handler from story_map_view.js if available
    if (typeof window.handleCreateNode === 'function') {
        console.log('[WebView] Using optimistic create handler');
        window.handleCreateNode({
            parentPath: 'story_graph',
            nodeType: 'epic'
            // placeholderName will be auto-generated (Epic1, Epic2, etc.)
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
    
    // Use optimistic update handler from story_map_view.js if available
    if (typeof window.handleDeleteNode === 'function') {
        console.log('[WebView] Using optimistic delete handler');
        window.handleDeleteNode({
            nodePath: nodePath
        });
    } else {
        console.warn('[WebView] handleDeleteNode not available, falling back to direct command');
        // Fallback: send command directly (defaults to optimistic for story-changing ops)
        vscode.postMessage({
            command: 'executeCommand',
            commandText: nodePath + '.delete'
            // optimistic defaults to true for story-changing operations
        });
    }
};

window.deleteNodeIncludingChildren = function(nodePath) {
    console.log('[WebView] deleteNodeIncludingChildren called for:', nodePath);
    
    // Use optimistic update handler from story_map_view.js if available
    // Delete ALWAYS includes children - no version without children
    if (typeof window.handleDeleteNode === 'function') {
        console.log('[WebView] Using optimistic delete handler (always includes children)');
        window.handleDeleteNode({
            nodePath: nodePath
        });
    } else {
        console.warn('[WebView] handleDeleteNode not available, falling back to direct command');
        // Fallback: send command directly (defaults to optimistic for story-changing ops)
        // Backend delete() method defaults to cascade=True (always includes children)
        vscode.postMessage({
            command: 'executeCommand',
            commandText: nodePath + '.delete()'
            // optimistic defaults to true for story-changing operations
        });
    }
};

window.enableEditMode = function(nodePath) {
    console.log('[ASYNC_SAVE] ========== RENAME OPERATION START ==========');
    console.log('[ASYNC_SAVE] [USER_ACTION] User double-clicked node to rename nodePath=' + nodePath + ' timestamp=' + new Date().toISOString());
    // Extract the current node name from the path
    // Path format: story_graph."Epic"."SubEpic"."Story"
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

// Track selected node for contextual actions (initialize window.selectedNode)
window.selectedNode = {
    type: 'root', // root, epic, sub-epic, story
    name: null,
    path: null, // Full path like story_graph."Epic"."SubEpic"
    canHaveSubEpic: false,
    canHaveStory: false,
    canHaveTests: false,
    hasChildren: false,
    hasStories: false,
    hasNestedSubEpics: false
};

// Map behavior names from backend to tooltip text (global function)
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


// Update contextual action buttons based on selection
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
    const btnOpenGraph = document.getElementById('btn-open-graph');
    const btnOpenAll = document.getElementById('btn-open-all');
    
    // Hide all buttons first
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
    
    // Show buttons based on selection
    if (window.selectedNode.type === 'root') {
        if (btnCreateEpic) btnCreateEpic.style.display = 'block';
    } else if (window.selectedNode.type === 'epic') {
        if (btnCreateSubEpic) btnCreateSubEpic.style.display = 'block';
        if (btnDelete) btnDelete.style.display = 'block';
        if (btnScopeTo) btnScopeTo.style.display = 'block';
    } else if (window.selectedNode.type === 'sub-epic') {
        // Sub-epics can have EITHER sub-epics OR stories, not both
        // If it has stories, only show create story button
        // If it has sub-epics, only show create sub-epic button
        // If empty, show both options
        if (window.selectedNode.hasStories) {
            // Has stories - only allow adding more stories
            if (btnCreateStory) btnCreateStory.style.display = 'block';
        } else if (window.selectedNode.hasNestedSubEpics) {
            // Has nested sub-epics - only allow adding more sub-epics
            if (btnCreateSubEpic) btnCreateSubEpic.style.display = 'block';
        } else {
            // Empty - show both options
            if (btnCreateSubEpic) btnCreateSubEpic.style.display = 'block';
            if (btnCreateStory) btnCreateStory.style.display = 'block';
        }
        if (btnDelete) btnDelete.style.display = 'block';
        if (btnScopeTo) btnScopeTo.style.display = 'block';
    } else if (window.selectedNode.type === 'story') {
        // Stories can have both scenarios and acceptance criteria
        if (btnCreateScenario) btnCreateScenario.style.display = 'block';
        if (btnCreateAcceptanceCriteria) btnCreateAcceptanceCriteria.style.display = 'block';
        if (btnDelete) btnDelete.style.display = 'block';
        if (btnScopeTo) btnScopeTo.style.display = 'block';
    } else if (window.selectedNode.type === 'scenario') {
        // Scenarios can also be scoped to and submitted
        if (btnDelete) btnDelete.style.display = 'block';
        if (btnScopeTo) btnScopeTo.style.display = 'block';
        // Note: submit button will be shown below if scenario has behavior_needed
    }
    
    // Show related files buttons for all non-root nodes
    if (window.selectedNode.type !== 'root') {
        if (btnOpenGraph) btnOpenGraph.style.display = 'block';
        if (btnOpenAll) btnOpenAll.style.display = 'block';
    }
    
    // Update submit button based on current behavior and action
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
    
    // btn-submit uses behavior_needed (required next behavior), not current behavior
    const requiredBehavior = window.selectedNode.behaviorNeeded;
    const currentBehavior = window.currentBehavior || window.selectedNode.behavior;
    const currentAction = window.currentAction || 'build'; // Default to 'build' if no action
    
    if (btnSubmit && window.selectedNode.type !== 'root' && requiredBehavior) {
        const behavior = requiredBehavior;
        const action = currentAction;
        const nodeType = window.selectedNode.type;
        const btnSubmitIcon = document.getElementById('btn-submit-icon');
        
        console.log('[SUBMIT BUTTON DEBUG] Proceeding with button update...');
        console.log('[SUBMIT BUTTON DEBUG] btnSubmitIcon exists:', !!btnSubmitIcon);
        
        // Map behavior to icon and tooltip
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
        if (!window.selectedNode.behavior) {
            console.log('[SUBMIT BUTTON DEBUG] ✗ No behavior_needed set on node');
            console.log('[SUBMIT BUTTON DEBUG]   This may indicate behavior_needed is not being read from story graph');
        }
    }
    
    // Update btn-submit-alt button (shows when there are multiple behaviors_needed)
    const btnSubmitAlt = document.getElementById('btn-submit-alt');
    const behaviorsNeeded = window.selectedNode.behaviorsNeeded || [];
    console.log('[SUBMIT BUTTON DEBUG] behaviorsNeeded:', behaviorsNeeded);
    
    if (btnSubmitAlt && behaviorsNeeded.length > 1 && window.selectedNode.type !== 'root') {
        const altBehavior = behaviorsNeeded[1]; // Second behavior option
        const nodeType = window.selectedNode.type;
        const btnSubmitAltIcon = document.getElementById('btn-submit-alt-icon');
        
        // Map behavior to icon and tooltip for alt button
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
            // Store alt behavior for handleSubmitAlt
            btnSubmitAlt.setAttribute('data-current-behavior', altBehavior);
            console.log('[SUBMIT BUTTON DEBUG] Alt button shown for behavior:', altBehavior);
        } else {
            btnSubmitAlt.style.display = 'none';
        }
    } else if (btnSubmitAlt) {
        btnSubmitAlt.style.display = 'none';
    }
    
    // Update btn-submit-current button (shows beside btn-submit)
    const btnSubmitCurrent = document.getElementById('btn-submit-current');
    if (btnSubmitCurrent && window.selectedNode.type !== 'root' && currentBehavior) {
        const behavior = currentBehavior;
        const action = currentAction;
        const btnSubmitCurrentIcon = document.getElementById('btn-submit-current-icon');
        
        // Use refresh icon for now (same as btn-submit)
        const refreshIcon = btnSubmitCurrent.getAttribute('data-refresh-icon') || btnSubmit?.getAttribute('data-refresh-icon');
        
        const tooltip = 'Submit current behavior (' + behavior + '.' + action + ')';
        
        if (refreshIcon && btnSubmitCurrentIcon) {
            btnSubmitCurrentIcon.src = refreshIcon;
            btnSubmitCurrent.title = tooltip;
            btnSubmitCurrent.style.display = 'block';
        } else {
            btnSubmitCurrent.style.display = 'none';
        }
    } else if (btnSubmitCurrent) {
        btnSubmitCurrent.style.display = 'none';
    }
    
    console.log('═══════════════════════════════════════════════════════');
};

// Select a node (called when clicking on node name/icon)
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
    
    // Remove selected class from all nodes
    document.querySelectorAll('.story-node.selected').forEach(node => {
        node.classList.remove('selected');
    });
    
    // Add selected class to the clicked node
    let targetNode = null;
    
    // First try to find by path if available (more specific for nested nodes)
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
    
    // Fallback to name+type if path not found
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
    
    // Store both current behavior and behavior_needed
    const behavior = window.currentBehavior || options.behavior || null;
    const behaviors = options.behaviors || (options.behavior ? [options.behavior] : []);
    
    window.selectedNode = {
        type: type,
        name: name,
        path: options.path || null,
        behavior: behavior, // Current behavior in progress
        behaviorNeeded: options.behavior || null, // Required next behavior from story graph
        behaviorsNeeded: behaviors, // List of applicable behaviors (may have multiple for empty nodes)
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
    
    // Save selection to sessionStorage
    try {
        sessionStorage.setItem('selectedNode', JSON.stringify(window.selectedNode));
    } catch (err) {
        console.error('[WebView] Error saving selection:', err);
    }
    
    window.updateContextualButtons();
    console.log('[WebView]   updateContextualButtons called');
    console.log('═══════════════════════════════════════════════════════');
};

// Handle contextual create actions
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
    
    // Validate path: must contain node name, not just "story_graph."
    const hasValidPath = window.selectedNode.path && 
                        window.selectedNode.path.length > 'story_graph.'.length &&
                        window.selectedNode.path.includes(window.selectedNode.name);
    
    console.log('[WebView]   path:', window.selectedNode.path);
    console.log('[WebView]   hasValidPath:', hasValidPath);
    
    // Use optimistic update handler from story_map_view.js if available
    if (typeof window.handleCreateNode === 'function') {
        var parentPath = hasValidPath ? window.selectedNode.path : `story_graph."${window.selectedNode.name}"`;
        
        console.log('[WebView] Using optimistic create handler for:', actionType);
        window.handleCreateNode({
            parentPath: parentPath,
            nodeType: actionType
            // placeholderName will be auto-generated (Epic1, SubEpic1, Story1, etc.)
        });
    } else {
        console.warn('[WebView] handleCreateNode not available, falling back to direct command');
        // Fallback: send command directly
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

// Handle delete action (always cascade)
window.handleDelete = function() {
    console.log('[WebView] handleDelete called for node:', window.selectedNode);
    
    if (!window.selectedNode || !window.selectedNode.name) {
        console.error('[WebView] ERROR: No node selected for delete');
        return;
    }
    
    // Build node path
    let nodePath = window.selectedNode.path;
    if (!nodePath || nodePath.length <= 'story_graph.'.length) {
        // Fallback: construct path from name
        nodePath = `story_graph."${window.selectedNode.name}"`;
    }
    
    console.log('[WebView] Calling handleDeleteNode with path:', nodePath);
    
    // Call handleDeleteNode for optimistic update (removes from DOM immediately)
    // Delete ALWAYS includes children - no version without children
    if (typeof window.handleDeleteNode === 'function') {
        window.handleDeleteNode({
            nodePath: nodePath
        });
    } else {
        console.warn('[WebView] handleDeleteNode not available, falling back to direct command');
        // Fallback: send command directly (will still work, but no optimistic update)
        // Backend delete() method defaults to cascade=True (always includes children)
        const commandText = nodePath + '.delete()';
        vscode.postMessage({
            command: 'executeCommand',
            commandText: commandText
        });
    }
};

// Handle scope to action - set filter to selected node
window.handleScopeTo = function() {
    console.log('[WebView] handleScopeTo called for node:', window.selectedNode);
    
    if (!window.selectedNode.name) {
        console.error('[WebView] ERROR: No node selected for scope');
        return;
    }
    
    // Build scope command with node type prefix (matches nodes.py _scope_command_for_node)
    const nodeName = window.selectedNode.name;
    const nodeType = window.selectedNode.type;
    let scopeCommand;
    
    if (nodeType === 'story') {
        scopeCommand = 'story ' + nodeName;
    } else if (nodeType === 'sub-epic') {
        scopeCommand = 'subepic ' + nodeName;
    } else if (nodeType === 'epic') {
        scopeCommand = 'epic ' + nodeName;
    } else {
        // Fallback to just the name for unknown types
        scopeCommand = nodeName;
    }
    
    console.log('[WebView] Scope To command:', scopeCommand);
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] SENDING SCOPE TO COMMAND: scope ' + scopeCommand
    });
    
    // Execute scope command with the node type and name
    vscode.postMessage({
        command: 'executeCommand',
        commandText: 'scope ' + scopeCommand
    });
};

window.handleSubmit = function() {
    console.log('[WebView] ========== handleSubmit CALLED ==========');
    console.log('[WebView] handleSubmit called for node:', window.selectedNode);
    console.log('[WebView] Node name:', window.selectedNode?.name);
    console.log('[WebView] Node path:', window.selectedNode?.path);
    console.log('[WebView] Node behavior:', window.selectedNode?.behavior);
    
    if (!window.selectedNode || !window.selectedNode.name) {
        console.error('[WebView] ERROR: No node selected for submit');
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] ERROR: handleSubmit called but no node selected'
        });
        return;
    }
    
    if (!window.selectedNode.behaviorNeeded) {
        console.error('[WebView] ERROR: No behaviorNeeded for selected node');
        vscode.postMessage({
            command: 'logToFile',
            message: '[WebView] ERROR: handleSubmit called but node has no behaviorNeeded: ' + window.selectedNode.name
        });
        return;
    }
    
    const nodeName = window.selectedNode.name;
    const nodePath = window.selectedNode.path;
    
    console.log('[WebView] Submit: Submitting required behavior instructions for', nodeName);
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] SUBMIT: Submitting required behavior instructions for node=' + nodeName + ', path=' + nodePath
    });
    
    // Call submit_required_behavior_instructions with the build action
    const action = 'build';
    const commandText = nodePath 
        ? nodePath + '.submit_required_behavior_instructions action:"' + action + '"'
        : 'story_graph."' + nodeName + '".submit_required_behavior_instructions action:"' + action + '"';
    
    console.log('[WebView] ========== SENDING COMMAND ==========');
    console.log('[WebView] Executing command:', commandText);
    console.log('[WebView] Command type:', typeof commandText);
    console.log('[WebView] Command length:', commandText.length);
    
    vscode.postMessage({
        command: 'executeCommand',
        commandText: commandText
    });
    
    console.log('[WebView] ========== COMMAND SENT ==========');
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] SUBMIT: Command sent: ' + commandText
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
    
    const altBehavior = behaviorsNeeded[1]; // Second behavior option
    const nodeName = window.selectedNode.name;
    const nodePath = window.selectedNode.path;
    
    console.log('[WebView] Submit Alt: Submitting', altBehavior, 'behavior instructions for', nodeName);
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] SUBMIT ALT: Submitting ' + altBehavior + ' behavior instructions for node=' + nodeName
    });
    
    // Navigate to the alt behavior first, then submit
    const action = 'build';
    const commandText = nodePath 
        ? nodePath + '.submit_instructions behavior:"' + altBehavior + '" action:"' + action + '"'
        : 'story_graph."' + nodeName + '".submit_instructions behavior:"' + altBehavior + '" action:"' + action + '"';
    
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
    const nodePath = window.selectedNode.path;
    
    console.log('[WebView] Submit Current: Submitting current instructions for', nodeName);
    console.log('[WebView] Submit Current: nodeName =', nodeName);
    console.log('[WebView] Submit Current: nodePath =', nodePath);
    console.log('[WebView] Submit Current: nodePath exists?', !!nodePath);
    
    vscode.postMessage({
        command: 'logToFile',
        message: '[WebView] SUBMIT CURRENT: node=' + nodeName + ', path=' + nodePath + ', pathExists=' + !!nodePath
    });
    
    // Call submit_current_instructions which uses current behavior and action
    const commandText = nodePath 
        ? nodePath + '.submit_current_instructions'
        : 'story_graph."' + nodeName + '".submit_current_instructions';
    
    console.log('[WebView] ========== SUBMIT CURRENT COMMAND ==========');
    console.log('[WebView] Command constructed:', commandText);
    console.log('[WebView] Command length:', commandText.length);
    
    vscode.postMessage({
        command: 'executeCommand',
        commandText: commandText
    });
    
    console.log('[WebView] ========== COMMAND SENT ==========');
};

// Helper function to get file link from selected node DOM element
function getSelectedNodeFileLink() {
    if (!window.selectedNode || !window.selectedNode.name) return null;
    const nodeElement = document.querySelector('.story-node[data-node-type="' + window.selectedNode.type + '"][data-node-name="' + window.selectedNode.name + '"]');
    return nodeElement ? nodeElement.getAttribute('data-file-link') : null;
}

// Helper function to get workspace directory
function getWorkspaceDir() {
    // Try to get from botData if available
    if (window.botData && window.botData.workspace_directory) {
        return window.botData.workspace_directory;
    }
    // Fallback: try to infer from story graph path
    const storyGraphPath = 'docs/story/story-graph.json';
    return ''; // Will be resolved relative to workspace root
}

// Helper function to open file in specific view column (for split editors)
function openFileInColumn(filePath, viewColumn) {
    vscode.postMessage({
        command: 'openFileInColumn',
        filePath: filePath,
        viewColumn: viewColumn // 'One', 'Two', 'Three', 'Four', 'Beside', 'Active'
    });
}

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
    
    // Open story graph and request to collapse all, expand selected node path, position cursor
    vscode.postMessage({
        command: 'openFileWithState',
        filePath: storyGraphPath,
        state: {
            collapseAll: true,
            expandPath: window.selectedNode.path || null,
            selectedNode: window.selectedNode,
            positionCursor: true // Request cursor positioning at expanded section
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
    
    // Request story files for selected node
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
    
    // Find the selected node element in DOM by iterating (querySelector fails with quoted paths)
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
                // For sub-epics/epics: collect story files and test files from ALL child stories
                // The collapsible content div is a sibling of the node's parent div
                const parentDiv = nodeEl.closest('div');
                const collapsibleDiv = parentDiv ? parentDiv.nextElementSibling : null;
                
                if (collapsibleDiv && collapsibleDiv.classList.contains('collapsible-content')) {
                    // Collect all story file links from child story nodes
                    const childStoryNodes = collapsibleDiv.querySelectorAll('.story-node[data-node-type="story"]');
                    childStoryNodes.forEach(function(storyEl) {
                        const link = storyEl.getAttribute('data-file-link');
                        if (link) {
                            storyFiles.push(link);
                        }
                    });
                    
                    // Collect all test files from child elements
                    const testFileEls = collapsibleDiv.querySelectorAll('[data-test-files]');
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
                // For stories/scenarios: get test files from sibling element
                if (nodeEl.parentElement) {
                    const testFilesEl = nodeEl.parentElement.querySelector('[data-test-files]');
                    if (testFilesEl) {
                        try {
                            testFiles = JSON.parse(testFilesEl.getAttribute('data-test-files'));
                            console.log('[WebView] Found test_files from DOM:', testFiles);
                        } catch (e) {
                            console.error('[WebView] Error parsing test_files:', e);
                        }
                    }
                }
            }
        }
    }
    
    console.log('[WebView] handleOpenAll - selectedNode:', JSON.stringify(window.selectedNode));
    console.log('[WebView] handleOpenAll - fileLink:', fileLink);
    console.log('[WebView] handleOpenAll - storyFiles:', storyFiles);
    console.log('[WebView] handleOpenAll - testFiles:', testFiles);
    
    // Open all files in split editors
    vscode.postMessage({
        command: 'openAllRelatedFiles',
        nodeType: window.selectedNode.type,
        nodeName: window.selectedNode.name,
        nodePath: window.selectedNode.path,
        singleFileLink: fileLink,
        storyFiles: storyFiles,
        testFiles: testFiles,
        storyGraphPath: storyGraphPath,
        selectedNode: window.selectedNode  // Pass full node for story graph positioning
    });
};


// Initialize: show Create Epic button by default
setTimeout(() => {
    window.selectNode('root', null);
}, 100);

// Toggle Q&A expand/collapse
window.toggleQAExpand = function(idx) {
    const textarea = document.getElementById('clarify-answer-' + idx);
    const toggleBtn = document.getElementById('qa-toggle-' + idx);
    if (!textarea) return;
    
    const isCollapsed = textarea.getAttribute('data-collapsed') === 'true';
    const defaultHeight = 60; // Default collapsed height in px
    
    if (isCollapsed) {
        // Expand to full content
        textarea.style.height = 'auto';
        const fullHeight = textarea.scrollHeight;
        textarea.style.height = fullHeight + 'px';
        textarea.style.overflow = 'visible';
        textarea.setAttribute('data-collapsed', 'false');
        if (toggleBtn) toggleBtn.textContent = '▲';
    } else {
        // Collapse to default height
        textarea.style.height = defaultHeight + 'px';
        textarea.style.overflow = 'hidden';
        textarea.setAttribute('data-collapsed', 'true');
        if (toggleBtn) toggleBtn.textContent = '▼';
    }
};

// Save functions for guardrails
window.saveClarifyAnswers = function() {
    console.log('[WebView] saveClarifyAnswers triggered');
    const answers = {};
    const answerElements = document.querySelectorAll('[id^="clarify-answer-"]');
    
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
    const evidenceTextarea = document.getElementById('clarify-evidence');
    if (evidenceTextarea) {
        const evidenceText = evidenceTextarea.value?.trim();
        if (evidenceText) {
            // Parse evidence text as key:value pairs
            const evidenceProvided = {};
            evidenceText.split('\\n').forEach(line => {
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

// Multi-select version: collects all checked checkboxes with given name
window.saveStrategyMultiDecision = function(criteriaKey, inputName) {
    console.log('[WebView] saveStrategyMultiDecision triggered:', criteriaKey, inputName);
    const checkboxes = document.querySelectorAll('input[name="' + inputName + '"]:checked');
    const selectedOptions = [];
    checkboxes.forEach(cb => {
        // Get the option text from the label's span
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
    const assumptionsTextarea = document.getElementById('strategy-assumptions');
    if (assumptionsTextarea) {
        const assumptionsText = assumptionsTextarea.value?.trim();
        if (assumptionsText) {
            const assumptions = assumptionsText.split('\\n').filter(a => a.trim());
            console.log('[WebView] Saving strategy assumptions:', assumptions);
            vscode.postMessage({
                command: 'saveStrategyAssumptions',
                assumptions: assumptions
            });
        }
    }
};
        
// Listen for messages from extension host (e.g. error displays)
window.addEventListener('message', event => {
    const message = event.data;
    console.log('[WebView] Received message from extension:', message);
    
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
        // Use optimistic update handler from story_map_view.js if available
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
        console.log('[WebView] Received setWorkspacePath message:', message.path);
        const input = document.getElementById('workspacePathInput');
        if (input) {
            input.value = message.path;
        }
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
    
    if (message.command === 'displayError') {
        // Display error prominently in the panel
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = 'position: fixed; top: 10px; left: 10px; right: 10px; z-index: 10000; background: #f44336; color: white; padding: 16px; border-radius: 4px; font-family: monospace; font-size: 12px; white-space: pre-wrap; max-height: 80vh; overflow-y: auto;';
        errorDiv.textContent = '[ERROR] ' + message.error;
        
        // Add button container
        const btnContainer = document.createElement('div');
        btnContainer.style.cssText = 'margin-top: 12px; display: flex; gap: 8px;';
        
        // Add retry button
        const retryBtn = document.createElement('button');
        retryBtn.textContent = '🔄 Retry';
        retryBtn.style.cssText = 'background: white; color: #f44336; border: none; padding: 8px 16px; cursor: pointer; border-radius: 3px; font-weight: bold;';
        retryBtn.onclick = () => {
            errorDiv.remove();
            vscode.postMessage({ command: 'refresh' });
        };
        
        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.textContent = 'Close';
        closeBtn.style.cssText = 'background: rgba(255,255,255,0.8); color: #f44336; border: none; padding: 8px 16px; cursor: pointer; border-radius: 3px;';
        closeBtn.onclick = () => errorDiv.remove();
        
        btnContainer.appendChild(retryBtn);
        btnContainer.appendChild(closeBtn);
        errorDiv.appendChild(btnContainer);
        
        document.body.appendChild(errorDiv);
        
        // Auto-remove after 30 seconds
        setTimeout(() => errorDiv.remove(), 30000);
    }
    
    // Handle explicit collapse state restoration after refresh
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
    
    // Optimistic update disabled - full refresh preserves icons and structure
    // (textContent wiped out icon HTML, causing icons to disappear)
    if (message.command === 'optimisticRename') {
        console.log('[WebView] Optimistic rename disabled - waiting for full refresh');
        // Panel will refresh after backend rename completes
    }
    
    // Revert rename disabled - no longer needed without optimistic updates
    if (message.command === 'revertRename') {
        console.log('[WebView] Revert rename command received but not needed');
    }
});

// Switch between Hierarchy, Increment, and Files views
window.switchViewMode = function(viewMode) {
    console.log('[switchViewMode] Switching to', viewMode);
    
    // Get current view from active button
    var previousView = 'Hierarchy';
    var btnHierarchy = document.getElementById('btn-view-hierarchy');
    var btnIncrement = document.getElementById('btn-view-increment');
    var btnFiles = document.getElementById('btn-view-files');
    
    if (btnHierarchy && btnHierarchy.style.color && !btnHierarchy.style.color.includes('faded')) previousView = 'Hierarchy';
    else if (btnIncrement && btnIncrement.style.color && !btnIncrement.style.color.includes('faded')) previousView = 'Increment';
    else if (btnFiles && btnFiles.style.color && !btnFiles.style.color.includes('faded')) previousView = 'Files';
    
    // Update button styles to reflect selected state
    if (btnHierarchy) {
        var isSelected = viewMode === 'Hierarchy';
        btnHierarchy.style.color = isSelected ? 'var(--text-color, #fff)' : 'var(--text-color-faded)';
    }
    if (btnIncrement) {
        var isSelected = viewMode === 'Increment';
        btnIncrement.style.color = isSelected ? 'var(--text-color, #fff)' : 'var(--text-color-faded)';
    }
    if (btnFiles) {
        var isSelected = viewMode === 'Files';
        btnFiles.style.color = isSelected ? 'var(--text-color, #fff)' : 'var(--text-color-faded)';
    }
    
    // Send message to extension to switch view
    if (typeof vscode !== 'undefined') {
        vscode.postMessage({
            command: 'switchViewMode',
            viewMode: viewMode
        });
    }
};

// Switch include level (Stories, Domain, criteria, Scenarios, Examples, Tests, Code)
window.switchIncludeLevel = function(level) {
    var levels = ['stories', 'domain_concepts', 'acceptance', 'scenarios', 'examples', 'tests', 'code'];
    var ids = { stories: 'btn-include-stories', domain_concepts: 'btn-include-domain', acceptance: 'btn-include-acceptance', scenarios: 'btn-include-scenarios', examples: 'btn-include-examples', tests: 'btn-include-tests', code: 'btn-include-code' };
    for (var i = 0; i < levels.length; i++) {
        var btn = document.getElementById(ids[levels[i]]);
        if (btn) {
            var isSelected = level === levels[i];
            btn.style.color = isSelected ? 'var(--text-color, #fff)' : 'var(--text-color-faded)';
        }
    }
    if (typeof updateIncludeLevel === 'function') updateIncludeLevel(level);
};