// Client-side Webview JS for story map section & functionality of bot panel

(function() {
    /**
     * Manages queued save operations with visual feedback
     * Client-side SaveQueue for StoryMapView - handles DOM updates and coordinates with backend
     * ES5-compatible: using function constructor instead of class
     */
    function SaveQueue(executeCallback, statusCallback) {
        this.queue = [];
        this.executing = false;
        this.executeCallback = executeCallback;
        this.statusCallback = statusCallback;
        this.debounceTimer = null;
    }
        
    /**
     * Add operation to queue and schedule processing
     * @param {Object} operation - {command: string, rollback: function, metadata: object}
     */
    SaveQueue.prototype.enqueue = function(operation) {
        console.log("[SaveQueue.enqueue] Operation enqueued:", operation.metadata || "unknown");
        // ES5-compatible: manually copy properties instead of spread operator
        var queuedOp = {
            command: operation.command,
            rollback: operation.rollback,
            metadata: operation.metadata
        };
        queuedOp.timestamp = Date.now();
        this.queue.push(queuedOp);
        
        console.log("[SaveQueue.enqueue] Queue length:", this.queue.length);
        
        // Debounce: wait 500ms after last change before processing
        var self = this;
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
        
        this.debounceTimer = setTimeout(function() {
            console.log("[SaveQueue.enqueue] Debounce timer fired, processing queue...");
            self.processQueue();
        }, 500);
    };
        
    /**
     * Process all queued operations in batch
     * ES5-compatible: using Promise chains instead of async/await
     */
    SaveQueue.prototype.processQueue = function() {
        var self = this;
        console.log("[SaveQueue.processQueue] Called - executing=", this.executing, "queueLength=", this.queue.length);
        if (this.executing || this.queue.length === 0) {
            console.log("[SaveQueue.processQueue] Skipping - executing=", this.executing, "queueLength=", this.queue.length);
            return;
        }
        
        this.executing = true;
        var count = this.queue.length;
        var message = count === 1 ? "Saving change..." : "Saving " + count + " changes...";
        console.log("[SaveQueue.processQueue] Calling statusCallback with saving state, message=", message);
        this.statusCallback("saving", message);
        
        // Update status messages for create operations
        for (var i = 0; i < this.queue.length; i++) {
            var op = this.queue[i];
            if (op.metadata && op.metadata.operation === "create" && op.metadata.tempNodeId) {
                var statusEl = document.getElementById(op.metadata.tempNodeId + "-status");
                if (statusEl) {
                    // Get the actual node name from the DOM
                    var nodeEl = document.getElementById(op.metadata.tempNodeId);
                    var nodeName = "node";
                    if (nodeEl) {
                        var nodeSpan = nodeEl.querySelector(".story-node");
                        if (nodeSpan) {
                            nodeName = nodeSpan.getAttribute("data-node-name") || nodeSpan.textContent;
                        }
                    }
                    statusEl.textContent = "Saving " + nodeName + "...";
                }
            }
        }
        
        // Take snapshot of current queue (ES5-compatible: use slice instead of spread)
        var batch = this.queue.slice();
        this.queue = [];
        
        var results = {
            success: [],
            failed: []
        };
        
        // Execute all operations sequentially using Promise chain
        var executeNext = function(index) {
            if (index >= batch.length) {
                // All operations completed
                if (results.failed.length === 0) {
                    // All succeeded - handle post-save updates
                    for (var i = 0; i < results.success.length; i++) {
                        var op = results.success[i];
                        if (op.metadata && op.metadata.operation === "create" && op.metadata.tempNodeId) {
                            // Remove status messages for create operations
                            var statusEl = document.getElementById(op.metadata.tempNodeId + "-status");
                            if (statusEl) {
                                statusEl.remove();
                            }
                            // IMPORTANT: Keep the temporary node in the DOM - it becomes the permanent node
                            // The node should stay visible after save completes
                            // Since optimistic operations skip panel refresh, the node will persist
                            var tempNode = document.getElementById(op.metadata.tempNodeId);
                            if (tempNode) {
                                console.log("[SaveQueue.processQueue] Create operation succeeded - keeping temporary node:", op.metadata.tempNodeId);
                                // Ensure the node stays visible - mark it as saved so it won"t be removed
                                tempNode.setAttribute("data-saved", "true");
                                // The node will remain in the DOM and be replaced by the real node
                                // when the panel next refreshes (which won"t happen for optimistic operations)
                            } else {
                                console.error("[SaveQueue.processQueue] CRITICAL: Temporary node disappeared after successful save:", op.metadata.tempNodeId);
                                console.error("[SaveQueue.processQueue] This should not happen - the node should persist after save");
                            }
                        } else if (op.metadata && op.metadata.operation === "rename") {
                            // Remove status message for rename operations
                            if (op.metadata.statusId) {
                                var renameStatusEl = document.getElementById(op.metadata.statusId);
                                if (renameStatusEl) {
                                    renameStatusEl.remove();
                                }
                            }
                            // Update data-path attributes after successful rename
                            // This ensures child nodes can be found and renamed correctly
                            updatePathAfterRename(op.metadata.path, op.metadata.oldName, op.metadata.newName);
                        } else if (op.metadata && op.metadata.operation === "delete") {
                            // Remove status message for delete operations
                            if (op.metadata.statusId) {
                                var deleteStatusEl = document.getElementById(op.metadata.statusId);
                                if (deleteStatusEl) {
                                    deleteStatusEl.remove();
                                }
                            }
                        } else if (op.metadata && op.metadata.operation === "move") {
                            // Remove status message for move operations
                            if (op.metadata.statusId) {
                                var moveStatusEl = document.getElementById(op.metadata.statusId);
                                if (moveStatusEl) {
                                    moveStatusEl.remove();
                                }
                            }
                        }
                    }
                    
                    self.statusCallback("success", "Saved");
                    
                    // Auto-hide after 2 seconds
                    setTimeout(function() {
                        self.statusCallback("hidden", "");
                    }, 2000);
                } else {
                    // Some failed - rollback and show error
                    var failedCount = results.failed.length;
                    var errorMsg = failedCount === 1 
                        ? "Save failed - click for details"
                        : failedCount + " saves failed - click for details";
                    
                    var firstError = results.failed[0].error;
                    self.statusCallback("error", errorMsg, firstError);
                    
                    // Update status messages for failed operations
                    for (var i = 0; i < results.failed.length; i++) {
                        var failed = results.failed[i];
                        if (failed.op.metadata && failed.op.metadata.operation === "create" && failed.op.metadata.tempNodeId) {
                            var statusEl = document.getElementById(failed.op.metadata.tempNodeId + "-status");
                            if (statusEl) {
                                statusEl.textContent = "Failed to save";
                                statusEl.style.color = "#c62828";
                            }
                        } else if (failed.op.metadata && failed.op.metadata.operation === "delete" && failed.op.metadata.statusId) {
                            // For delete: update status message to show failure
                            var deleteStatusEl = document.getElementById(failed.op.metadata.statusId);
                            if (deleteStatusEl) {
                                deleteStatusEl.textContent = "Failed to delete";
                                deleteStatusEl.style.color = "#c62828";
                            }
                        } else if (failed.op.metadata && failed.op.metadata.operation === "move" && failed.op.metadata.statusId) {
                            // For move: update status message to show failure
                            var moveStatusEl = document.getElementById(failed.op.metadata.statusId);
                            if (moveStatusEl) {
                                moveStatusEl.textContent = "Failed to move";
                                moveStatusEl.style.color = "#c62828";
                            }
                        }
                    }
                    
                    // Rollback failed operations (ES5-compatible: use traditional for loop)
                    for (var i = 0; i < results.failed.length; i++) {
                        var failed = results.failed[i];
                        if (failed.op.rollback) {
                            try {
                                failed.op.rollback();
                            } catch (rollbackError) {
                                console.error("Rollback failed:", rollbackError);
                            }
                        }
                    }
                }
                
                self.executing = false;
                
                // Process remaining queue if new items added during execution
                if (self.queue.length > 0) {
                    setTimeout(function() {
                        self.processQueue();
                    }, 500);
                }
                return;
            }
            
            var op = batch[index];
            console.log("[SaveQueue.processQueue] Calling executeCallback for command:", op.command);
            var promise = self.executeCallback(op.command);
            console.log("[SaveQueue.processQueue] executeCallback returned promise:", typeof promise, promise && typeof promise.then === "function" ? "Promise" : "not a Promise");
            if (promise && typeof promise.then === "function") {
                promise.then(function(result) {
                    console.log("[SaveQueue.processQueue] Promise resolved for command:", op.command, "result:", result);
                    results.success.push(op);
                    executeNext(index + 1);
                }).catch(function(error) {
                    console.error("[SaveQueue.processQueue] Promise rejected for command:", op.command, "error:", error);
                    results.failed.push({ op: op, error: error });
                    executeNext(index + 1);
                });
            } else {
                // Synchronous callback
                try {
                    promise;
                    results.success.push(op);
                } catch (error) {
                    results.failed.push({ op: op, error: error });
                }
                executeNext(index + 1);
            }
        };
        
        try {
            executeNext(0);
        } catch (error) {
            // Critical error - rollback everything (ES5-compatible: use traditional for loop)
            this.statusCallback("error", "Save failed - click for details", error);
            
            for (var i = 0; i < batch.length; i++) {
                var op = batch[i];
                if (op.rollback) {
                    try {
                        op.rollback();
                    } catch (rollbackError) {
                        console.error("Rollback failed:", rollbackError);
                    }
                }
            }
            
            this.executing = false;
        }
    };
        
    /**
     * Update the status indicator UI
     * @param {string} state - "saving" | "success" | "error" | "hidden"
     * @param {string} message - Display message
     * @param {Error} error - Error object (for error state)
     * ES5-compatible: no default parameters
     */
    SaveQueue.prototype.updateStatus = function(state, message, error) {
        try {
            if (error === undefined) error = null;
            
            console.log("[SaveQueue.updateStatus] Called with state=", state, "message=", message);
            
            var indicator = document.getElementById("story-map-save-status-indicator");
            if (!indicator) {
                console.warn("[SaveQueue.updateStatus] story-map-save-status-indicator element not found in DOM - status indicator may not be rendered yet");
                return;
            }
            
            // Use story map specific IDs
            var spinner = document.getElementById("story-map-save-status-spinner");
            var msg = document.getElementById("story-map-save-status-message");
            
            if (!spinner || !msg) {
                console.warn("[SaveQueue.updateStatus] Missing spinner or message element! spinner=", !!spinner, "msg=", !!msg, " - status indicator may not be fully rendered");
                return;
            }
            
            console.log("[SaveQueue.updateStatus] Updating indicator - state=", state, "message=", message);
            
            if (state === "hidden") {
                indicator.style.display = "none";
                indicator.onclick = null;
                return;
            }
            
            indicator.style.display = "flex";
            // Update classes - keep main-header-status, add state class
            indicator.className = "main-header-status save-status " + state;
            
            // Update spinner visibility and message
            if (state === "saving") {
                spinner.style.display = "inline-block";
                msg.textContent = message || "Saving...";
            } else if (state === "success") {
                spinner.style.display = "none";
                msg.textContent = (message || "Saved") + " ✓";
                // Auto-hide after 2 seconds
                setTimeout(function() {
                    try {
                        var ind = document.getElementById("story-map-save-status-indicator");
                        if (ind && ind.className.indexOf("success") !== -1) {
                            ind.style.display = "none";
                        }
                    } catch (e) {
                        console.warn("[SaveQueue.updateStatus] Error in auto-hide timeout:", e);
                    }
                }, 2000);
            } else if (state === "error") {
                spinner.style.display = "none";
                msg.textContent = (message || "Save failed") + " ✗";
                
                // Make clickable to show error details (ES5-compatible: use function instead of arrow)
                indicator.onclick = function() {
                    try {
                        var errorDetails = error 
                            ? (error.message + "\\\\n\\\\n" + (error.stack || ""))
                            : "Unknown error occurred";
                        
                        // Send to extension host to show error dialog
                        if (typeof vscode !== "undefined") {
                            vscode.postMessage({
                                type: "showErrorDialog",
                                title: "Save Failed",
                                message: errorDetails
                            });
                        }
                    } catch (e) {
                        console.error("[SaveQueue.updateStatus] Error in error click handler:", e);
                    }
                };
            }
        } catch (e) {
            console.error("[SaveQueue.updateStatus] Error updating status indicator:", e);
            // Don"t throw - prevent breaking the panel
        }
    };
    
    // Initialize SaveQueue instance for StoryMapView
    // Execute callback sends commands to backend via postMessage
    // Status callback updates DOM status indicator directly
    // NOTE: vscode may not be available immediately, so we use a retry mechanism
    function initializeSaveQueue() {
        // Use the global vscode instance that was already acquired in bot_panel.js
        // DO NOT call acquireVsCodeApi() again - it can only be called once!
        var vscodeApi = typeof vscode !== "undefined" ? vscode : null;
        
        if (!vscodeApi) {
            // vscode not ready yet - retry after a short delay
            console.log("[SaveQueue Init] vscode not available yet, retrying in 100ms...");
            setTimeout(initializeSaveQueue, 100);
            return;
        }
        
        console.log("[SaveQueue Init] vscode is available, creating SaveQueue instance...");
        window.storyMapSaveQueue = new SaveQueue(
            function(cmd) {
                return new Promise(function(resolve, reject) {
                    console.log("[SaveQueue.executeCallback] Sending command:", cmd);
                    
                    // Add timeout to detect if Promise never resolves
                    var timeoutId = setTimeout(function() {
                        console.error("[SaveQueue.executeCallback] TIMEOUT: Promise never resolved for command:", cmd);
                        window.removeEventListener("message", messageListener);
                        reject(new Error("Save operation timed out after 10 seconds"));
                    }, 10000);
                    
                    vscodeApi.postMessage({
                        command: "executeCommand",
                        commandText: cmd,
                        optimistic: true
                    });
                    
                    // Listen for save completion message (ES5-compatible: use function instead of arrow, var instead of const)
                    var messageListener = function(event) {
                        var message = event.data;
                        console.log("[SaveQueue.executeCallback] Received message:", message.command, "for command:", cmd);
                        if (message.command === "saveCompleted") {
                            console.log("[SaveQueue.executeCallback] saveCompleted received, removing listener and resolving Promise");
                            clearTimeout(timeoutId);
                            window.removeEventListener("message", messageListener);
                            if (message.success) {
                                console.log("[SaveQueue.executeCallback] Resolving Promise with success, result:", message.result);
                                resolve(message.result);
                            } else {
                                console.error("[SaveQueue.executeCallback] Rejecting Promise with error:", message.error);
                                reject(new Error(message.error || "Save failed"));
                            }
                        }
                    };
                    window.addEventListener("message", messageListener);
                    console.log("[SaveQueue.executeCallback] Message listener added for command:", cmd);
                });
            },
                function(state, msg, err) {
                    try {
                        console.log("[SaveQueue.statusCallback] Called with state=", state, "msg=", msg);
                        // Directly call updateStatus to update the DOM (don"t recurse!)
                        if (window.storyMapSaveQueue && typeof window.storyMapSaveQueue.updateStatus === "function") {
                            window.storyMapSaveQueue.updateStatus(state, msg, err);
                        } else {
                            console.warn("[SaveQueue.statusCallback] storyMapSaveQueue or updateStatus not available!");
                        }
                    } catch (e) {
                        console.error("[SaveQueue.statusCallback] Error in status callback:", e);
                        // Don"t throw - prevent breaking the panel
                    }
                }
        );
        console.log("[SaveQueue Init] SaveQueue instance created successfully, typeof window.storyMapSaveQueue:", typeof window.storyMapSaveQueue);
    }
    
    // Start initialization (will retry if vscode not ready)
    initializeSaveQueue();
    
    /**
     * Handle refresh status messages from extension host
     * Shows "Refreshing..." indicator during panel refresh
     */
    var refreshStatusTimeout = null;
    function updateRefreshStatus(state, message) {
        try {
            // Clear any existing timeout
            if (refreshStatusTimeout) {
                clearTimeout(refreshStatusTimeout);
                refreshStatusTimeout = null;
            }
            
            var indicator = document.getElementById("story-map-save-status-indicator");
            if (!indicator) {
                console.warn("[RefreshStatus] story-map-save-status-indicator element not found");
                return;
            }
            
            var spinner = document.getElementById("story-map-save-status-spinner");
            var msg = document.getElementById("story-map-save-status-message");
            
            if (!spinner || !msg) {
                console.warn("[RefreshStatus] Missing spinner or message element");
                return;
            }
            
            if (state === "hidden") {
                indicator.style.display = "none";
                return;
            }
            
            // Show refreshing status
            indicator.style.display = "flex";
            spinner.style.display = "inline-block";
            msg.textContent = message || "Refreshing...";
            indicator.className = "save-status refreshing";
            
            // Auto-hide after refresh completes (if not explicitly hidden)
            if (state === "refreshing") {
                refreshStatusTimeout = setTimeout(function() {
                    var ind = document.getElementById("story-map-save-status-indicator");
                    if (ind && ind.className.indexOf("refreshing") !== -1) {
                        ind.style.display = "none";
                    }
                    refreshStatusTimeout = null;
                }, 1000); // Hide after 1 second
            }
        } catch (e) {
            console.error("[RefreshStatus] Error updating refresh status:", e);
        }
    }
    
    // Listen for refresh status messages
    window.addEventListener("message", function(event) {
        var message = event.data;
        if (message.command === "refreshStatus") {
            updateRefreshStatus(message.state, message.message);
        }
    });
    
    /**
     * StoryMapView handler methods - handle optimistic updates for move/rename/delete operations
     */
    
    /**
     * Find DOM element by node path
     * @param {string} nodePath - e.g., "story_graph.\\"Epic1\\".\\"SubEpic1\\".\\"Story1\\""
     * @returns {HTMLElement|null}
     */
    function findNodeElement(nodePath) {
        console.log("[findNodeElement] Looking for node with path:", nodePath);
        // Handle paths with quotes - need to search iteratively (ES5-compatible: use var)
        var allNodes = document.querySelectorAll(".story-node, [data-path]");
        console.log("[findNodeElement] Found", allNodes.length, "nodes with data-path or story-node class");
        for (var i = 0; i < allNodes.length; i++) {
            var node = allNodes[i];
            var nodePathAttr = node.getAttribute("data-path");
            if (nodePathAttr === nodePath) {
                console.log("[findNodeElement] Found matching node at index", i, "node:", node, "tagName:", node.tagName);
                return node;
            }
        }
        console.warn("[findNodeElement] No node found with path:", nodePath);
        // Debug: log first few paths to help diagnose
        for (var j = 0; j < Math.min(allNodes.length, 5); j++) {
            console.log("[findNodeElement] Sample node", j, "path:", allNodes[j].getAttribute("data-path"), "type:", allNodes[j].getAttribute("data-node-type"));
        }
        return null;
    }
    
    /**
     * Find the wrapper div for a story-node span
     * Story nodes are <span> elements wrapped in <div> containers
     * @param {HTMLElement} storyNodeSpan - The <span> element with class story-node
     * @returns {HTMLElement} The wrapper <div> or the span itself if no wrapper found
     */
    function findNodeWrapper(storyNodeSpan) {
        if (!storyNodeSpan) return null;
        
        // Walk up the DOM tree to find the wrapper div
        // The wrapper is typically a direct parent <div> that contains the story-node
        var current = storyNodeSpan.parentElement;
        
        while (current && current !== document.body) {
            // Stop if we hit a collapsible-content container (that"s the parent of all nodes)
            if (current.classList && current.classList.contains("collapsible-content")) {
                break;
            }
            
            // Check if current is a div element and contains our story-node
            // This avoids using querySelector with data-path (which breaks with quotes)
            if (current.tagName && current.tagName.toLowerCase() === "div" && current.contains && current.contains(storyNodeSpan)) {
                // Check if this div directly contains the story-node or has it as a descendant
                // The wrapper div should contain exactly one story-node with our data-path
                var hasStoryNode = false;
                var storyNodes = current.querySelectorAll ? current.querySelectorAll(".story-node") : [];
                for (var i = 0; i < storyNodes.length; i++) {
                    if (storyNodes[i] === storyNodeSpan) {
                        hasStoryNode = true;
                        break;
                    }
                }
                if (hasStoryNode) {
                    // Found the wrapper div that contains our story-node
                    return current;
                }
            }
            current = current.parentElement;
        }
        
        // If no wrapper found, return the span itself
        return storyNodeSpan;
    }
    
    /**
     * Pure DOM manipulation for moving nodes
     * @param {HTMLElement} sourceNode - Node to move
     * @param {HTMLElement} targetParent - Parent container to move into
     * @param {number} position - Position index (used when targetNode is not provided)
     * @param {HTMLElement} targetNode - Optional: specific node to insert after (for "after" dropZone)
     */
    /**
     * Recalculate margin-left for a node and all its children based on new parent depth
     * Uses the EXACT same formula as backend: marginLeft = 7 + (depth * 7)
     * @param {HTMLElement} nodeWrapper - The wrapper div containing the node
     * @param {HTMLElement} newParent - The new parent node element
     */
    function recalculateMarginLeftForMovedNode(nodeWrapper, newParent) {
        if (!nodeWrapper || !newParent) {
            console.warn("[recalculateMarginLeftForMovedNode] Missing nodeWrapper or newParent");
            return;
        }
        
        // Find the story-node span inside the wrapper
        var storyNode = nodeWrapper.querySelector ? nodeWrapper.querySelector(".story-node") : null;
        if (!storyNode) {
            console.warn("[recalculateMarginLeftForMovedNode] Cannot find story-node in wrapper");
            return;
        }
        
        var nodeType = storyNode.getAttribute ? storyNode.getAttribute("data-node-type") : null;
        if (!nodeType) {
            console.warn("[recalculateMarginLeftForMovedNode] Cannot determine node type");
            return;
        }
        
        // Epics always have margin-left 0
        if (nodeType === "epic") {
            nodeWrapper.style.marginLeft = "0px";
            console.log("[recalculateMarginLeftForMovedNode] Epic node, set margin-left to 0px");
            // Still need to update children
        } else {
            // Calculate margin-left based on new parent"s depth
            var marginLeft = 0;
            
            // First: try to copy from an existing sibling of the same type
            var parentContainer = nodeWrapper.parentElement;
            if (parentContainer) {
                var containerChildren = Array.prototype.slice.call(parentContainer.children);
                for (var i = 0; i < containerChildren.length; i++) {
                    var sibling = containerChildren[i];
                    if (sibling === nodeWrapper) continue; // Skip self
                    var siblingNode = sibling.querySelector ? sibling.querySelector(".story-node[data-node-type= " + nodeType + "]") : null;
                    if (siblingNode) {
                        if (sibling.style && sibling.style.marginLeft) {
                            var siblingMargin = sibling.style.marginLeft;
                            var marginMatch = siblingMargin.match(/(\\d+)px/);
                            if (marginMatch) {
                                marginLeft = parseInt(marginMatch[1], 10);
                                console.log("[recalculateMarginLeftForMovedNode] Copied margin-left from sibling:", marginLeft, "px");
                                break;
                            }
                        }
                    }
                }
            }
            
            // Fallback: calculate using backend formula if no sibling found
            if (!marginLeft) {
                var newParentWrapper = findNodeWrapper(newParent);
                var parentMarginLeft = 0;
                
                if (newParentWrapper && newParentWrapper.style && newParentWrapper.style.marginLeft) {
                    var parentMargin = newParentWrapper.style.marginLeft;
                    var parentMatch = parentMargin.match(/(\\d+)px/);
                    if (parentMatch) {
                        parentMarginLeft = parseInt(parentMatch[1], 10);
                    }
                }
                
                if (nodeType === "sub-epic") {
                    // Backend formula: marginLeft = 7 + (depth * 7)
                    // Calculate depth from parent"s margin-left
                    // parentMarginLeft = 7 + (parentDepth * 7)
                    // So: parentDepth = (parentMarginLeft - 7) / 7
                    var parentDepth = parentMarginLeft >= 7 ? (parentMarginLeft - 7) / 7 : 0;
                    var depth = parentDepth + 1;
                    marginLeft = 7 + (depth * 7);
                    console.log("[recalculateMarginLeftForMovedNode] Calculated depth:", depth, "marginLeft:", marginLeft, "px (backend formula: 7 + (depth * 7))");
                } else {
                    // For stories/scenarios: use parent"s margin + 7
                    marginLeft = parentMarginLeft + 7;
                    console.log("[recalculateMarginLeftForMovedNode] Story/scenario, marginLeft:", marginLeft, "px (parent + 7)");
                }
            }
            
            nodeWrapper.style.marginLeft = marginLeft + "px";
        }
        
        // Recursively update all children
        var collapsibleContent = nodeWrapper.querySelector ? nodeWrapper.querySelector(".collapsible-content") : null;
        if (collapsibleContent) {
            var childWrappers = collapsibleContent.querySelectorAll ? collapsibleContent.querySelectorAll("> div") : [];
            for (var j = 0; j < childWrappers.length; j++) {
                var childWrapper = childWrappers[j];
                var childStoryNode = childWrapper.querySelector ? childWrapper.querySelector(".story-node") : null;
                if (childStoryNode) {
                    // Recursively recalculate for this child (using moved node as its new parent)
                    recalculateMarginLeftForMovedNode(childWrapper, storyNode);
                }
            }
        }
    }
    
    function moveNodeInDOM(sourceNode, targetParent, position, targetNode) {
        console.log("[moveNodeInDOM] Called - sourceNode:", sourceNode, "targetParent:", targetParent, "targetNode:", targetNode);
        
        // Story nodes are <span> elements wrapped in <div> containers
        // We need to move the wrapper <div>, not just the <span>
        var nodeToMove = findNodeWrapper(sourceNode);
        console.log("[moveNodeInDOM] Node to move:", nodeToMove, "isWrapper:", nodeToMove !== sourceNode);
        
        if (!nodeToMove) {
            console.error("[moveNodeInDOM] Cannot find wrapper for sourceNode");
            return;
        }
        
        // Remove from current position
        if (nodeToMove.parentElement) {
            nodeToMove.parentElement.removeChild(nodeToMove);
        }
        
        // If targetNode is provided (dropZone === "after"), insert right after it
        if (targetNode && targetNode.parentElement) {
            // Find the wrapper div for targetNode
            var targetNodeToUse = findNodeWrapper(targetNode);
            
            if (!targetNodeToUse) {
                console.error("[moveNodeInDOM] Cannot find wrapper for targetNode");
                return;
            }
            
            // Find the parent container (should be collapsible-content)
            var targetParentContainer = targetNodeToUse.parentElement;
            
            if (!targetParentContainer) {
                console.error("[moveNodeInDOM] targetNodeToUse has no parent");
                return;
            }
            
            // Find the next sibling of targetNodeToUse
            var nextSibling = targetNodeToUse.nextSibling;
            
            // Skip text nodes and whitespace
            while (nextSibling && nextSibling.nodeType !== 1) {
                nextSibling = nextSibling.nextSibling;
            }
            
            console.log("[moveNodeInDOM] Inserting after targetNodeToUse, nextSibling:", nextSibling, "parent:", targetParentContainer);
            
            if (nextSibling) {
                targetParentContainer.insertBefore(nodeToMove, nextSibling);
            } else {
                // targetNode is the last child, append to end
                targetParentContainer.appendChild(nodeToMove);
            }
            console.log("[moveNodeInDOM] Node moved successfully after target");
            
            // Recalculate margin-left for moved node and all its children based on new parent depth
            recalculateMarginLeftForMovedNode(nodeToMove, targetParent);
            return;
        }
        
        // Fallback: use position-based insertion (for "inside" dropZone)
        // Find the collapsible-content container that holds child nodes
        var targetContainer = null;
        
        // If targetParent is a story-node, find its collapsible-content child
        if (targetParent.classList && targetParent.classList.contains("story-node")) {
            // Use the same logic as create operations: find wrapper, then find collapsible-content
            var targetParentWrapper = findNodeWrapper(targetParent);
            if (targetParentWrapper) {
                // Look for collapsible-content as next sibling of wrapper
                var nextSibling = targetParentWrapper.nextSibling;
                while (nextSibling) {
                    if (nextSibling.nodeType === 1 && nextSibling.classList && nextSibling.classList.contains("collapsible-content")) {
                        targetContainer = nextSibling;
                        break;
                    }
                    nextSibling = nextSibling.nextSibling;
                }
                // If not found as sibling, check if wrapper contains it
                if (!targetContainer) {
                    targetContainer = targetParentWrapper.querySelector ? targetParentWrapper.querySelector(".collapsible-content") : null;
                }
            }
        } else if (targetParent.classList && targetParent.classList.contains("collapsible-content")) {
            // Already the right container
            targetContainer = targetParent;
        } else {
            // Search for collapsible-content in children
            targetContainer = targetParent.querySelector ? targetParent.querySelector(".collapsible-content") : null;
            if (!targetContainer) {
                targetContainer = targetParent;
            }
        }
        
        if (!targetContainer) {
            console.error("[moveNodeInDOM] Cannot find target container");
            return;
        }
        
        console.log("[moveNodeInDOM] Using targetContainer:", targetContainer);
        
        // Insert at new position (ES5-compatible: use slice instead of Array.from)
        var targetChildren = Array.prototype.slice.call(targetContainer.children);
        // Filter to only div wrappers (skip other elements)
        var wrapperChildren = targetChildren.filter(function(child) {
            return child.nodeType === 1 && (child.querySelector && child.querySelector(".story-node") || child.classList && child.classList.contains("story-node"));
        });
        
        console.log("[moveNodeInDOM] targetChildren.length:", targetChildren.length, "wrapperChildren.length:", wrapperChildren.length, "position:", position);
        
        if (position >= wrapperChildren.length) {
            targetContainer.appendChild(nodeToMove);
        } else {
            targetContainer.insertBefore(nodeToMove, wrapperChildren[position]);
        }
        console.log("[moveNodeInDOM] Node moved successfully at position");
        
        // Recalculate margin-left for moved node and all its children based on new parent depth
        recalculateMarginLeftForMovedNode(nodeToMove, targetParent);
    }
    
    /**
     * Build Python command for move operation
     * @param {string} sourceNodePath - Full path like "story_graph.\\"Epic\\".\\"SubEpic\\""
     * @param {string} targetParentPath - Full path to target parent
     * @param {number} position - Target position
     * @returns {string} Command string
     */
    function buildMoveCommand(sourceNodePath, targetParentPath, position) {
        // Extract target name from targetParentPath
        // targetParentPath is like: story_graph."Epic1"."SubEpic1"
        // We need: story_graph."Epic1"."SubEpic1".move_to target:"SubEpic1" at_position:1
        // ES5-compatible: use var
        var targetMatch = targetParentPath.match(/"([^"]+)"/g);
        var targetName = targetMatch && targetMatch.length > 0 
            ? targetMatch[targetMatch.length - 1].replace(/"/g, "")
            : "";
        
        // Build command using the source path
        return sourceNodePath + ".move_to target:" + targetParentPath.replace(/^story_graph\\./, "") + " at_position:" + position;
    }
    
    /**
     * Update data-path attribute after successful rename
     * Also updates all child nodes" paths to reflect parent"s new name
     * @param {string} oldPath - Old full path (e.g., "story_graph."OldEpicName"")
     * @param {string} oldName - Old node name
     * @param {string} newName - New node name
     */
    function updatePathAfterRename(oldPath, oldName, newName) {
        // Calculate new path by replacing old name with new name
        // Handle quoted names in path: story_graph."OldName" -> story_graph."NewName"
        var newPath = oldPath.replace(new RegExp("" + oldName.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&") + "", "g"), "" + newName + "");
        
        // Find the renamed node element
        var nodeElement = findNodeElement(oldPath);
        if (nodeElement) {
            // Update the renamed node"s data-path
            nodeElement.setAttribute("data-path", newPath);
            console.log("[updatePathAfterRename] Updated node path:", oldPath, "->", newPath);
            
            // Update window.selectedNode if this node is currently selected
            if (window.selectedNode && window.selectedNode.path === oldPath) {
                window.selectedNode.name = newName;
                window.selectedNode.path = newPath;
                console.log("[updatePathAfterRename] Updated window.selectedNode:", JSON.stringify(window.selectedNode));
            }
            
            // Find all child nodes and update their paths
            // Child paths contain the parent"s name, so we need to update them too
            var allNodes = document.querySelectorAll(".story-node[data-path]");
            for (var i = 0; i < allNodes.length; i++) {
                var childNode = allNodes[i];
                var childPath = childNode.getAttribute("data-path");
                if (childPath && childPath.indexOf(oldPath) === 0) {
                    // This is a child node - update its path
                    var updatedChildPath = childPath.replace(new RegExp("" + oldName.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&") + "", "g"), "" + newName + "");
                    childNode.setAttribute("data-path", updatedChildPath);
                    console.log("[updatePathAfterRename] Updated child path:", childPath, "->", updatedChildPath);
                    
                    // Also update window.selectedNode if a child is selected
                    if (window.selectedNode && window.selectedNode.path === childPath) {
                        window.selectedNode.path = updatedChildPath;
                        console.log("[updatePathAfterRename] Updated window.selectedNode path for child:", updatedChildPath);
                    }
                }
            }
        } else {
            console.warn("[updatePathAfterRename] Could not find node with path:", oldPath);
        }
    }
    
    /**
     * Build Python command for rename operation
     * @param {string} nodePath - Full path to node
     * @param {string} oldName - Old name
     * @param {string} newName - New name
     * @returns {string} Command string
     */
    function buildRenameCommand(nodePath, oldName, newName) {
        return nodePath + ".rename(" + newName + ")";
    }
    
    /**
     * Build Python command for delete operation
     * @param {string} nodePath - Full path to node
     * @returns {string} Command string
     */
    function buildDeleteCommand(nodePath) {
        // Delete ALWAYS includes children - no version without children
        // Backend delete() method defaults to cascade=True
        return nodePath + ".delete()";
    }
    
    /**
     * Build Python command for create operation
     * @param {string} parentPath - Parent node path
     * @param {string} nodeType - Type of node to create (epic, sub-epic, story, etc.)
     * @returns {string} Command string
     */
    function buildCreateCommand(parentPath, nodeType, placeholderName) {
        // Helper function to check if parentPath is the root story_graph (with or without quotes)
        function isRootStoryGraph(path) {
            // TODO might be an issue
            // return path === "story_graph" || path === "story_graph."Story Map"" || path === "story_graph."root"";
            return path === "story_graph" || path === "story_graph.\"Story Map\"" || path === "story_graph.\"root\"";
        }
        
        if (nodeType === "epic") {
            // Include the name parameter so backend creates epic with the same name as frontend
            if (placeholderName) {
                return "story_graph.create_epic name:" + placeholderName;
            }
            return "story_graph.create_epic";
        } else if (nodeType === "sub-epic") {
            // Sub-epics can be created on epics or other sub-epics, but not on story_graph
            if (isRootStoryGraph(parentPath)) {
                console.error("[buildCreateCommand] Cannot create sub-epic on story_graph root. Select an epic first.");
                return null; // Invalid command
            }
            // Include name parameter if provided
            if (placeholderName) {
                return parentPath + ".create name:" + placeholderName;
            }
            return parentPath + ".create";
        } else if (nodeType === "story") {
            // Stories can only be created on epics or sub-epics, not on story_graph
            if (isRootStoryGraph(parentPath)) {
                console.error("[buildCreateCommand] Cannot create story on story_graph root. Select an epic or sub-epic first.");
                return null; // Invalid command
            }
            // Include name parameter if provided
            if (placeholderName) {
                return parentPath + ".create_story name:" + placeholderName;
            }
            return parentPath + ".create_story";
        } else if (nodeType === "scenario") {
            // Scenarios can only be created on stories, not on story_graph
            if (isRootStoryGraph(parentPath)) {
                console.error("[buildCreateCommand] Cannot create scenario on story_graph root. Select a story first.");
                return null; // Invalid command
            }
            // Include name parameter if provided
            if (placeholderName) {
                return parentPath + ".create_scenario name:" + placeholderName;
            }
            return parentPath + ".create_scenario";
        } else if (nodeType === "acceptance-criteria") {
            // Acceptance criteria can only be created on stories, not on story_graph
            if (isRootStoryGraph(parentPath)) {
                console.error("[buildCreateCommand] Cannot create acceptance-criteria on story_graph root. Select a story first.");
                return null; // Invalid command
            }
            // Include name parameter if provided
            if (placeholderName) {
                // TODO these might need to keep the quotes?
                return parentPath + ".create_acceptance_criteria name:" + placeholderName;
            }
            return parentPath + ".create_acceptance_criteria";
        }
        return parentPath + ".create";
    }
    
    /**
     * Handle node move with optimistic update
     * @param {Object} message - {sourceNodePath, targetParentPath, position}
     */
    window.handleMoveNode = function(message) {
        console.log("[handleMoveNode] Called with:", JSON.stringify(message));
        console.log("[handleMoveNode] storyMapSaveQueue exists:", typeof window.storyMapSaveQueue !== "undefined");
        if (typeof vscode !== "undefined" && vscode.postMessage) {
            vscode.postMessage({ command: "logToFile", message: "[handleMoveNode] source:" + (message.sourceNodePath||"") + " target:" + (message.targetParentPath||"") + " pos:" + (message.position||0) + " saveQueue:" + (typeof window.storyMapSaveQueue !== "undefined") });
        }
        
        // ES5-compatible: use var instead of const
        var sourceNodePath = message.sourceNodePath;
        var targetParentPath = message.targetParentPath;
        var position = message.position;
        var targetNodePath = message.targetNodePath;  // Optional: for "after" dropZone
        var dropZone = message.dropZone || "inside";
        
        // Find DOM elements
        var sourceNode = findNodeElement(sourceNodePath);
        var targetParent = findNodeElement(targetParentPath);
        var targetNode = targetNodePath ? findNodeElement(targetNodePath) : null;
        
        console.log("[handleMoveNode] Found nodes - source:", !!sourceNode, "targetParent:", !!targetParent, "targetNode:", !!targetNode);
        
        if (!sourceNode || !targetParent) {
            console.error("Move failed: Could not find nodes", {
                sourceNodePath: sourceNodePath,
                targetParentPath: targetParentPath,
                targetNodePath: targetNodePath,
                foundSource: !!sourceNode,
                foundTarget: !!targetParent,
                foundTargetNode: !!targetNode
            });
            return;
        }
        
        // 1. Capture current state for rollback (ES5-compatible: use slice instead of Array.from)
        // Find the wrapper div for rollback
        var sourceWrapper = findNodeWrapper(sourceNode);
        if (!sourceWrapper) {
            console.error("[handleMoveNode] Cannot find wrapper for sourceNode");
            return;
        }
        
        var childrenArray = Array.prototype.slice.call(sourceWrapper.parentElement.children);
        var rollback = {
            originalParent: sourceWrapper.parentElement,
            originalPosition: childrenArray.indexOf(sourceWrapper),
            sourceNode: sourceWrapper  // Store wrapper for rollback
        };
        
        // 2. Optimistic UI update (immediate)
        // For "after" dropZone, pass targetNode to insert after it
        // For "inside" dropZone, use position-based insertion
        if (dropZone === "after" && targetNode) {
            moveNodeInDOM(sourceNode, targetParent, position, targetNode);
        } else {
            moveNodeInDOM(sourceNode, targetParent, position);
        }
        
        // Create status message - show beside moved node, or beside parent if node is hidden
        var statusId = "move-status-" + Date.now() + "-" + Math.random().toString(36).substr(2, 9);
        var statusSpan = document.createElement("span");
        statusSpan.id = statusId;
        statusSpan.style.cssText = "font-size: 11px; color: #666; font-style: italic; margin-left: 8px;";
        var nodeName = sourceNode.getAttribute ? sourceNode.getAttribute("data-node-name") : (sourceNode.textContent || "node");
        statusSpan.textContent = "Moving " + nodeName + "...";
        
        // Try to insert after moved node, or after parent if node is hidden/collapsed
        var movedWrapper = findNodeWrapper(sourceNode);
        var statusParent = null;
        if (movedWrapper && movedWrapper.parentElement && movedWrapper.offsetParent !== null) {
            // Node is visible, insert after it
            statusParent = movedWrapper.parentElement;
            var nextSibling = movedWrapper.nextSibling;
            // Skip collapsible-content if present
            while (nextSibling && nextSibling.nodeType === 1 && nextSibling.classList && nextSibling.classList.contains("collapsible-content")) {
                nextSibling = nextSibling.nextSibling;
            }
            if (nextSibling) {
                statusParent.insertBefore(statusSpan, nextSibling);
            } else {
                statusParent.appendChild(statusSpan);
            }
        } else {
            // Node is hidden, show beside parent
            var targetParentWrapper = findNodeWrapper(targetParent);
            if (targetParentWrapper && targetParentWrapper.parentElement) {
                statusParent = targetParentWrapper.parentElement;
                var parentNextSibling = targetParentWrapper.nextSibling;
                while (parentNextSibling && parentNextSibling.nodeType === 1 && parentNextSibling.classList && parentNextSibling.classList.contains("collapsible-content")) {
                    parentNextSibling = parentNextSibling.nextSibling;
                }
                if (parentNextSibling) {
                    statusParent.insertBefore(statusSpan, parentNextSibling);
                } else {
                    statusParent.appendChild(statusSpan);
                }
            }
        }
        
        // 3. Build command
        var command = buildMoveCommand(sourceNodePath, targetParentPath, position);
        if (typeof vscode !== "undefined" && vscode.postMessage) {
            vscode.postMessage({ command: "logToFile", message: "[handleMoveNode] command:" + command });
        }
        
        // 4. Queue backend save (async) (ES5-compatible: use function instead of arrow)
        if (window.storyMapSaveQueue) {
            window.storyMapSaveQueue.enqueue({
                command: command,
                rollback: function() {
                    // Restore original position in DOM
                    var parent = rollback.originalParent;
                    var pos = rollback.originalPosition;
                    var nodeToRestore = rollback.sourceNode;
                    
                    // Make sure node is not already in the DOM
                    if (nodeToRestore.parentElement) {
                        nodeToRestore.parentElement.removeChild(nodeToRestore);
                    }
                    
                    if (pos >= parent.children.length) {
                        parent.appendChild(nodeToRestore);
                    } else {
                        parent.insertBefore(nodeToRestore, parent.children[pos]);
                    }
                },
                metadata: {
                    operation: "move",
                    source: sourceNodePath,
                    target: targetParentPath,
                    position: position,
                    statusId: statusId
                }
            });
        } else {
            console.error("handleMoveNode: storyMapSaveQueue not available - save will not occur");
        }
    };
    
    /**
     * Handle node rename with optimistic update
     * @param {Object} message - {nodePath, oldName, newName}
     */
    window.handleRenameNode = function(message) {
        // ES5-compatible: use var instead of const
        var nodePath = message.nodePath;
        var oldName = message.oldName;
        var newName = message.newName;
        
        var nodeElement = findNodeElement(nodePath);
        if (!nodeElement) {
            console.error("Rename failed: Could not find node", nodePath);
            return;
        }
        
        // Create status message span (similar to create operations)
        var statusId = "rename-status-" + Date.now() + "-" + Math.random().toString(36).substr(2, 9);
        var statusSpan = document.createElement("span");
        statusSpan.id = statusId;
        statusSpan.style.cssText = "font-size: 11px; color: #666; font-style: italic; margin-left: 8px;";
        statusSpan.textContent = "saving...";
        
        // Insert status message after the node element
        if (nodeElement.parentElement) {
            nodeElement.parentElement.insertBefore(statusSpan, nodeElement.nextSibling);
        } else {
            // Fallback: append to node element if no parent
            nodeElement.appendChild(statusSpan);
        }
        
        // 1. Capture for rollback - use the node element itself (it contains the name)
        var rollback = {
            element: nodeElement,
            oldName: oldName,
            statusSpan: statusSpan
        };
        
        // 2. Optimistic UI update
        nodeElement.textContent = newName;
        nodeElement.setAttribute("data-node-name", newName);
        
        // 3. Build command
        var command = buildRenameCommand(nodePath, oldName, newName);
        
        // 4. Queue save (ES5-compatible: use function instead of arrow)
        if (window.storyMapSaveQueue) {
            window.storyMapSaveQueue.enqueue({
                command: command,
                rollback: function() {
                    rollback.element.textContent = rollback.oldName;
                    rollback.element.setAttribute("data-node-name", rollback.oldName);
                    if (rollback.statusSpan && rollback.statusSpan.parentElement) {
                        rollback.statusSpan.remove();
                    }
                },
                metadata: {
                    operation: "rename",
                    path: nodePath,
                    oldName: oldName,
                    newName: newName,
                    statusId: statusId
                }
            });
        }
    };
    
    /**
     * Handle node delete with optimistic update
     * @param {Object} message - {nodePath}
     */
    window.handleDeleteNode = function(message) {
        console.log("[handleDeleteNode] START - Called with:", JSON.stringify(message));
        
        // ES5-compatible: use var instead of const/let, use slice instead of Array.from
        var nodePath = message.nodePath;
        // Delete ALWAYS includes children - no version without children
        
        console.log("[handleDeleteNode] Looking for node with path:", nodePath);
        var nodeElement = findNodeElement(nodePath);
        if (!nodeElement) {
            console.error("[handleDeleteNode] Delete failed: Could not find node element for path:", nodePath);
            console.error("[handleDeleteNode] Available nodes in DOM:");
            var allNodes = document.querySelectorAll("[data-path]");
            for (var i = 0; i < Math.min(allNodes.length, 10); i++) {
                console.error("[handleDeleteNode]   Node:", allNodes[i].getAttribute("data-path"));
            }
            return;
        }
        console.log("[handleDeleteNode] Found nodeElement:", nodeElement, "tagName:", nodeElement.tagName, "className:", nodeElement.className);
        
        // 1. Capture entire node HTML for rollback
        // Find the wrapper div (like handleMoveNode does)
        console.log("[handleDeleteNode] Finding wrapper for nodeElement...");
        var wrapper = findNodeWrapper(nodeElement);
        if (!wrapper) {
            console.error("[handleDeleteNode] Cannot find wrapper for nodeElement");
            console.error("[handleDeleteNode] nodeElement parent:", nodeElement.parentElement);
            console.error("[handleDeleteNode] nodeElement parent tagName:", nodeElement.parentElement ? nodeElement.parentElement.tagName : "null");
            return;
        }
        console.log("[handleDeleteNode] Found wrapper:", wrapper, "tagName:", wrapper.tagName, "id:", wrapper.id);
        
        var parent = wrapper.parentElement;
        console.log("[handleDeleteNode] Parent container:", parent, "tagName:", parent ? parent.tagName : "null", "className:", parent ? parent.className : "null");
        if (!parent) {
            console.error("[handleDeleteNode] Wrapper has no parent element!");
            return;
        }
        var childrenArray = Array.prototype.slice.call(parent.children);
        var position = childrenArray.indexOf(wrapper);
        console.log("[handleDeleteNode] Wrapper position in parent:", position, "total children:", childrenArray.length);
        
        // Delete ALWAYS includes children - capture all nested nodes
        var nodeHTML = wrapper.outerHTML;
        // The outerHTML already includes all children, so we"re good
        
        // Find and capture collapsible-content sibling before removal
        var collapsibleContent = null;
        var nextSibling = wrapper.nextSibling;
        while (nextSibling) {
            if (nextSibling.nodeType === 1 && nextSibling.classList && nextSibling.classList.contains("collapsible-content")) {
                collapsibleContent = nextSibling;
                break;
            }
            nextSibling = nextSibling.nextSibling;
        }
        var collapsibleHTML = collapsibleContent ? collapsibleContent.outerHTML : null;
        
        // Create status message span - show beside parent (not the node being deleted)
        var statusId = "delete-status-" + Date.now() + "-" + Math.random().toString(36).substr(2, 9);
        var statusSpan = document.createElement("span");
        statusSpan.id = statusId;
        statusSpan.style.cssText = "font-size: 11px; color: #666; font-style: italic; margin-left: 8px;";
        var nodeName = nodeElement.getAttribute ? nodeElement.getAttribute("data-node-name") : (nodeElement.textContent || "node");
        statusSpan.textContent = "Deleting " + nodeName + "...";
        
        // Find parent node element to show status beside it
        // The parent container is the collapsible-content, we need to find the parent"s node element
        var parentNodeElement = null;
        if (parent && parent.classList && parent.classList.contains("collapsible-content")) {
            // Find the parent wrapper that contains this collapsible-content
            var parentWrapper = parent.previousSibling;
            while (parentWrapper) {
                if (parentWrapper.nodeType === 1) {
                    var parentNode = parentWrapper.querySelector ? parentWrapper.querySelector(".story-node") : null;
                    if (parentNode) {
                        parentNodeElement = parentNode;
                        break;
                    }
                }
                parentWrapper = parentWrapper.previousSibling;
            }
        }
        
        // Insert status message beside parent node element, or in parent container if parent not found
        if (parentNodeElement && parentNodeElement.parentElement) {
            // Insert after parent node element
            var parentParent = parentNodeElement.parentElement;
            var parentNextSibling = parentNodeElement.nextSibling;
            if (parentNextSibling) {
                parentParent.insertBefore(statusSpan, parentNextSibling);
            } else {
                parentParent.appendChild(statusSpan);
            }
        } else if (parent) {
            // Fallback: insert at start of parent container
            if (parent.firstChild) {
                parent.insertBefore(statusSpan, parent.firstChild);
            } else {
                parent.appendChild(statusSpan);
            }
        }
        
        var rollback = {
            parent: parent,
            position: position,
            nodeHTML: nodeHTML,
            collapsibleHTML: collapsibleHTML,
            statusSpan: statusSpan
        };
        
        // 2. Optimistic UI update (remove wrapper and collapsible-content from DOM)
        console.log("[handleDeleteNode] About to remove wrapper from DOM...");
        console.log("[handleDeleteNode] Wrapper still in DOM before remove:", wrapper.parentElement === parent);
        console.log("[handleDeleteNode] Wrapper still has parent:", !!wrapper.parentElement);
        
        // Use remove() if available, fallback to removeChild() for compatibility
        if (wrapper.remove && typeof wrapper.remove === "function") {
            wrapper.remove();
            console.log("[handleDeleteNode] Used wrapper.remove()");
        } else if (wrapper.parentElement && wrapper.parentElement.removeChild) {
            wrapper.parentElement.removeChild(wrapper);
            console.log("[handleDeleteNode] Used parent.removeChild(wrapper)");
        } else {
            console.error("[handleDeleteNode] Cannot remove wrapper - no remove method available!");
            return;
        }
        
        console.log("[handleDeleteNode] After wrapper removal:");
        console.log("[handleDeleteNode] Wrapper still has parent:", !!wrapper.parentElement);
        console.log("[handleDeleteNode] Wrapper in parent.children:", parent.children ? Array.prototype.slice.call(parent.children).indexOf(wrapper) : "N/A");
        console.log("[handleDeleteNode] Parent children count:", parent.children ? parent.children.length : "N/A");
        
        if (collapsibleContent) {
            console.log("[handleDeleteNode] Removing collapsible-content:", collapsibleContent);
            if (collapsibleContent.remove && typeof collapsibleContent.remove === "function") {
                collapsibleContent.remove();
            } else if (collapsibleContent.parentElement && collapsibleContent.parentElement.removeChild) {
                collapsibleContent.parentElement.removeChild(collapsibleContent);
            }
            console.log("[handleDeleteNode] Collapsible-content removed, still has parent:", !!collapsibleContent.parentElement);
        } else {
            console.log("[handleDeleteNode] No collapsible-content to remove");
        }
        
        // 3. Build command - ALWAYS delete including children
        var command = buildDeleteCommand(nodePath);
        console.log("[handleDeleteNode] Built command:", command);
        
        // 4. Queue save (ES5-compatible: use function instead of arrow)
        console.log("[handleDeleteNode] Checking storyMapSaveQueue...");
        if (window.storyMapSaveQueue) {
            console.log("[handleDeleteNode] storyMapSaveQueue exists, enqueueing delete operation...");
            window.storyMapSaveQueue.enqueue({
                command: command,
                rollback: function() {
                    // Restore deleted node (both wrapper and collapsible-content)
                    var tempDiv = document.createElement("div");
                    tempDiv.innerHTML = rollback.nodeHTML;
                    var restoredNode = tempDiv.firstChild;
                    
                    if (rollback.position >= rollback.parent.children.length) {
                        rollback.parent.appendChild(restoredNode);
                    } else {
                        rollback.parent.insertBefore(restoredNode, rollback.parent.children[rollback.position]);
                    }
                    
                    // Restore collapsible-content if it existed
                    if (rollback.collapsibleHTML) {
                        var collapsibleTempDiv = document.createElement("div");
                        collapsibleTempDiv.innerHTML = rollback.collapsibleHTML;
                        var restoredCollapsible = collapsibleTempDiv.firstChild;
                        // Insert after the restored node
                        if (restoredNode.nextSibling) {
                            rollback.parent.insertBefore(restoredCollapsible, restoredNode.nextSibling);
                        } else {
                            rollback.parent.appendChild(restoredCollapsible);
                        }
                    }
                },
                metadata: {
                    operation: "delete",
                    path: nodePath,
                    statusId: statusId
                }
            });
            console.log("[handleDeleteNode] Delete operation enqueued successfully");
        } else {
            console.error("[handleDeleteNode] storyMapSaveQueue not available - delete will not be saved!");
            console.error("[handleDeleteNode] typeof window.storyMapSaveQueue:", typeof window.storyMapSaveQueue);
        }
        
        // Final verification - check if node is still in DOM
        setTimeout(function() {
            var stillExists = findNodeElement(nodePath);
            if (stillExists) {
                console.error("[handleDeleteNode] WARNING: Node still exists in DOM after removal! Path:", nodePath);
                console.error("[handleDeleteNode] Node element:", stillExists);
            } else {
                console.log("[handleDeleteNode] SUCCESS: Node successfully removed from DOM");
            }
        }, 100);
    };
    
    /**
     * Handle delete button click - calls handleDeleteNode with selected node
     */
    window.handleDelete = function() {
        console.log("[handleDelete] Called, selectedNode:", window.selectedNode);
        
        if (!window.selectedNode || !window.selectedNode.name) {
            console.error("[handleDelete] No node selected for delete");
            if (typeof vscode !== "undefined") {
                vscode.postMessage({
                    type: "showErrorDialog",
                    title: "Delete Failed",
                    message: "No node selected for deletion."
                });
            }
            return;
        }
        
        // Build node path
        var nodePath = window.selectedNode.path;
        if (!nodePath || nodePath.length <= "story_graph.".length) {
            // Fallback: construct path from name
            nodePath = "story_graph./" + window.selectedNode.name;
        }
        
        console.log("[handleDelete] Calling handleDeleteNode with path:", nodePath);
        
        // Call handleDeleteNode for optimistic update (this removes from DOM and queues save)
        // Delete ALWAYS includes children
        window.handleDeleteNode({
            nodePath: nodePath
        });
    };
    
    /**
     * Update parent node"s collapse icon when it gets its first child
     * Replaces empty placeholder with collapse icon (+)
     * @param {string} parentPath - Path to parent node
     */
    function updateParentCollapseIcon(parentPath) {
        console.log("[updateParentCollapseIcon] Updating parent collapse icon for:", parentPath);
        
        var parentElement = findNodeElement(parentPath);
        if (!parentElement) {
            console.warn("[updateParentCollapseIcon] Parent element not found:", parentPath);
            return;
        }
        
        var parentWrapper = findNodeWrapper(parentElement);
        if (!parentWrapper) {
            console.warn("[updateParentCollapseIcon] Parent wrapper not found");
            return;
        }
        
        // Find the collapse icon span (first child of wrapper, or first span)
        var collapseIconSpan = parentWrapper.querySelector ? parentWrapper.querySelector("span:first-child") : null;
        if (!collapseIconSpan) {
            console.warn("[updateParentCollapseIcon] Collapse icon span not found");
            return;
        }
        
        // Check if it has an empty placeholder (img with empty alt)
        var emptyImg = collapseIconSpan.querySelector ? collapseIconSpan.querySelector("img[alt='']") : null;
        if (!emptyImg) {
            // Already has a collapse icon, nothing to do
            console.log("[updateParentCollapseIcon] Parent already has collapse icon");
            return;
        }
        
        // Find plus icon path from existing nodes
        var plusIconPath = null;
        var existingEpicIcon = document.querySelector("#epic-0-icon img.collapse-icon");
        if (existingEpicIcon) {
            plusIconPath = existingEpicIcon.src;
        }
        
        if (!plusIconPath) {
            console.warn("[updateParentCollapseIcon] Plus icon path not found");
            return;
        }
        
        // Find the collapsible-content div that follows the wrapper
        // This is where children are stored
        var parentCollapsibleContent = null;
        var nextSibling = parentWrapper.nextSibling;
        while (nextSibling) {
            if (nextSibling.nodeType === 1 && nextSibling.classList && nextSibling.classList.contains("collapsible-content")) {
                parentCollapsibleContent = nextSibling;
                break;
            }
            nextSibling = nextSibling.nextSibling;
        }
        
        if (!parentCollapsibleContent) {
            console.warn("[updateParentCollapseIcon] Parent collapsible-content not found - parent may not support children");
            return;
        }
        
        var parentId = parentCollapsibleContent.id;
        if (!parentId) {
            console.warn("[updateParentCollapseIcon] Parent collapsible-content has no ID");
            return;
        }
        
        console.log("[updateParentCollapseIcon] Replacing empty placeholder with collapse icon, parentId:", parentId);
        
        // Clear the span and add collapse icon
        collapseIconSpan.innerHTML = "";
        collapseIconSpan.id = parentId + "-icon";
        collapseIconSpan.style.cssText = "display: inline-block; min-width: 9px; cursor: pointer;";
        collapseIconSpan.setAttribute("onclick", "event.stopPropagation(); toggleCollapse('" + parentId + "')");
        collapseIconSpan.setAttribute("data-plus", plusIconPath);
        collapseIconSpan.setAttribute("data-subtract", plusIconPath.replace("plus", "subtract"));
        
        // Create collapse icon image
        var collapseImg = document.createElement("img");
        collapseImg.className = "collapse-icon";
        collapseImg.src = plusIconPath;
        collapseImg.setAttribute("data-state", "collapsed");
        collapseImg.style.cssText = "width: 9px; height: 9px; vertical-align: middle;";
        collapseImg.alt = "Expand";
        collapseIconSpan.appendChild(collapseImg);
        
        // Update data-has-children attribute
        if (parentElement.setAttribute) {
            parentElement.setAttribute("data-has-children", "true");
        }
        
        console.log("[updateParentCollapseIcon] Successfully updated parent collapse icon");
    }
    
    /**
     * Handle node create with optimistic update
     * @param {Object} message - {parentPath, nodeType, placeholderName}
     */
    window.handleCreateNode = function(message) {
        console.log("[handleCreateNode] Called with:", JSON.stringify(message));
        
        var parentPath = message.parentPath || "story_graph";
        var nodeType = message.nodeType || "epic";
        
        // Generate name matching backend pattern (Epic1, Epic2, Child1, Story1, etc.)
        var placeholderName = message.placeholderName;
        if (!placeholderName) {
            // Backend uses: Epic1, Child1 (for sub-epics), Story1, etc.
            var baseName = nodeType === "epic" ? "Epic" : (nodeType === "sub-epic" ? "Child" : (nodeType === "story" ? "Story" : nodeType.charAt(0).toUpperCase() + nodeType.slice(1)));
            
            // Find existing nodes of same type to determine next number
            // Need to check ALL nodes including optimistically created ones
            var existingNodes = null;
            console.log("[handleCreateNode] Starting name generation for", nodeType, "parentPath:", parentPath);
            
            if (nodeType === "sub-epic" && parentPath !== "story_graph") {
                // Find parent element and its collapsible-content
                var parentEl = findNodeElement(parentPath);
                if (parentEl) {
                    var parentWrapper = findNodeWrapper(parentEl);
                    if (parentWrapper) {
                        var nextSibling = parentWrapper.nextSibling;
                        while (nextSibling) {
                            if (nextSibling.nodeType === 1 && nextSibling.classList && nextSibling.classList.contains("collapsible-content")) {
                                existingNodes = nextSibling.querySelectorAll('.story-node[data-node-type="sub-epic"]');
                                break;
                            }
                            nextSibling = nextSibling.nextSibling;
                        }
                    }
                }
            } else if (nodeType === "story" && parentPath !== "story_graph") {
                // Stories are nested under sub-epics - find parent element and its collapsible-content
                var parentEl = findNodeElement(parentPath);
                if (parentEl) {
                    var parentWrapper = findNodeWrapper(parentEl);
                    if (parentWrapper) {
                        var nextSibling = parentWrapper.nextSibling;
                        while (nextSibling) {
                            if (nextSibling.nodeType === 1 && nextSibling.classList && nextSibling.classList.contains("collapsible-content")) {
                                existingNodes = nextSibling.querySelectorAll('.story-node[data-node-type="story"]');
                                console.log("[handleCreateNode] Found", existingNodes.length, "stories in parent sub-epic");
                                break;
                            }
                            nextSibling = nextSibling.nextSibling;
                        }
                    }
                }
            }
            
            if (!existingNodes) {
                // Query ALL nodes of this type in the DOM (including optimistically created ones)
                // For epics at root, search within scope-content container where epics are rendered
                if (nodeType === "epic" && parentPath === "story_graph") {
                    console.log("[handleCreateNode] Searching for epic nodes in scope-content...");
                    // Epics are rendered inside #scope-content (has class collapsible-content)
                    var scopeContent = document.getElementById("scope-content");
                    console.log("[handleCreateNode] scope-content element:", scopeContent ? "found" : "NOT FOUND");
                    if (scopeContent) {
                        // Debug: Check what"s actually in scope-content
                        var allStoryNodes = scopeContent.querySelectorAll(".story-node");
                        console.log("[handleCreateNode] DEBUG: Found", allStoryNodes.length, "total .story-node elements in scope-content");
                        // Check first few nodes to see their types
                        var nodeTypeCounts = {};
                        for (var i = 0; i < Math.min(allStoryNodes.length, 10); i++) {
                            var nodeType = allStoryNodes[i].getAttribute("data-node-type");
                            nodeTypeCounts[nodeType] = (nodeTypeCounts[nodeType] || 0) + 1;
                        }
                        console.log("[handleCreateNode] DEBUG: Node type counts (first 10):", nodeTypeCounts);
                        if (allStoryNodes.length > 0) {
                            console.log("[handleCreateNode] DEBUG: First story-node attributes:", {
                                "data-node-type": allStoryNodes[0].getAttribute("data-node-type"),
                                "data-node-name": allStoryNodes[0].getAttribute("data-node-name"),
                                className: allStoryNodes[0].className
                            });
                            // Also check if we can find epic nodes with a different approach
                            var epicNodesByClass = scopeContent.querySelectorAll('.story-node[data-node-type="epic"]');
                            console.log("[handleCreateNode] DEBUG: Direct epic query in scope-content:", epicNodesByClass.length);
                            if (epicNodesByClass.length === 0) {
                                // Try finding epic nodes by checking all nodes
                                var epicNodesFound = [];
                                for (var j = 0; j < Math.min(allStoryNodes.length, 50); j++) {
                                    if (allStoryNodes[j].getAttribute("data-node-type") === "epic") {
                                        epicNodesFound.push({
                                            name: allStoryNodes[j].getAttribute("data-node-name"),
                                            index: j
                                        });
                                    }
                                }
                                console.log("[handleCreateNode] DEBUG: Epic nodes found by manual check (first 50):", epicNodesFound);
                            }
                        }
                        
                        // Try querySelectorAll first
                        existingNodes = scopeContent.querySelectorAll('.story-node[data-node-type="' + nodeType + '"]');
                        console.log("[handleCreateNode] Found", existingNodes.length, "epic nodes in scope-content container (querySelectorAll)");
                        // If querySelectorAll fails, manually filter all story-node elements
                        if (existingNodes.length === 0 && allStoryNodes.length > 0) {
                            var manualEpicNodes = [];
                            for (var k = 0; k < allStoryNodes.length; k++) {
                                if (allStoryNodes[k].getAttribute("data-node-type") === nodeType) {
                                    manualEpicNodes.push(allStoryNodes[k]);
                                }
                            }
                            console.log("[handleCreateNode] Found", manualEpicNodes.length, "epic nodes by manual filtering");
                            if (manualEpicNodes.length > 0) {
                                // Convert array to NodeList-like object
                                existingNodes = manualEpicNodes;
                            }
                        }
                        // Also check card-secondary inside scope-content
                        if (existingNodes.length === 0) {
                            var cardSecondary = scopeContent.querySelector(".card-secondary");
                            console.log("[handleCreateNode] DEBUG: card-secondary element:", cardSecondary ? "found" : "NOT FOUND");
                            if (cardSecondary) {
                                var cardStoryNodes = cardSecondary.querySelectorAll(".story-node");
                                console.log("[handleCreateNode] DEBUG: Found", cardStoryNodes.length, "total .story-node elements in card-secondary");
                                existingNodes = cardSecondary.querySelectorAll('.story-node[data-node-type="' + nodeType + '"]');
                                console.log("[handleCreateNode] Found", existingNodes.length, "epic nodes in card-secondary");
                            }
                        }
                    }
                    // Also search entire document as fallback (for optimistically created nodes that might be elsewhere)
                    if (!existingNodes || existingNodes.length === 0) {
                        var allDocStoryNodes = document.querySelectorAll(".story-node");
                        console.log("[handleCreateNode] DEBUG: Found", allDocStoryNodes.length, "total .story-node elements in entire document");
                        existingNodes = document.querySelectorAll('.story-node[data-node-type="' + nodeType + '"]');
                        console.log("[handleCreateNode] Fallback: Found", existingNodes.length, "epic nodes in entire document");
                    }
                } else {
                    existingNodes = document.querySelectorAll('.story-node[data-node-type="' + nodeType + '"]');
                    console.log("[handleCreateNode] Searched entire document, found", existingNodes.length, nodeType, "nodes");
                }
            }
            
            // Ensure existingNodes is initialized (should never be null at this point)
            if (!existingNodes) {
                existingNodes = document.querySelectorAll('.story-node[data-node-type="' + nodeType + '"]');
                console.log("[handleCreateNode] Final fallback: Found", existingNodes.length, nodeType, "nodes");
            }
            
            console.log("[handleCreateNode] Found", existingNodes.length, "existing", nodeType, "nodes for name generation");
            
            var maxNum = 0;
            var foundNames = [];
            for (var i = 0; i < existingNodes.length; i++) {
                var nodeName = existingNodes[i].getAttribute("data-node-name");
                console.log("[handleCreateNode] Node", i, "name:", nodeName, "element:", existingNodes[i]);
                if (nodeName) {
                    foundNames.push(nodeName);
                    // Match pattern like "Epic1", "Epic2", "Child3", "Story1", etc.
                    // Also handle "Epic 1" with space (though backend uses "Epic1")
                    var match = nodeName.match(new RegExp("^" + baseName + "[\\s]*([0-9]+)$"));
                    if (match) {
                        var num = parseInt(match[1], 10);
                        console.log("[handleCreateNode] Found", nodeType, "with number:", num, "name:", nodeName);
                        if (num > maxNum) maxNum = num;
                    }
                }
            }
            
            // Also check for optimistically created nodes in SaveQueue (both queue and currently executing)
            if (window.storyMapSaveQueue) {
                // Check currently executing operation
                if (window.storyMapSaveQueue.currentlyExecuting && window.storyMapSaveQueue.currentlyExecuting.metadata) {
                    var execOp = window.storyMapSaveQueue.currentlyExecuting.metadata;
                    if (execOp.operation === "create" && execOp.nodeType === nodeType) {
                        var execNodeEl = document.getElementById(execOp.tempNodeId);
                        if (execNodeEl) {
                            var execNodeSpan = execNodeEl.querySelector(".story-node");
                            if (execNodeSpan) {
                                var execName = execNodeSpan.getAttribute("data-node-name");
                                if (execName) {
                                    foundNames.push("[executing]" + execName);
                                    var execMatch = execName.match(new RegExp("^" + baseName + "[\\s]*([0-9]+)$"));
                                    if (execMatch) {
                                        var execNum = parseInt(execMatch[1], 10);
                                        console.log("[handleCreateNode] Found executing", nodeType, "with number:", execNum);
                                        if (execNum > maxNum) maxNum = execNum;
                                    }
                                }
                            }
                        }
                    }
                }
                // Check queue
                if (window.storyMapSaveQueue.queue) {
                    console.log("[handleCreateNode] Checking SaveQueue queue, length:", window.storyMapSaveQueue.queue.length);
                    for (var j = 0; j < window.storyMapSaveQueue.queue.length; j++) {
                        var queuedOp = window.storyMapSaveQueue.queue[j];
                        if (queuedOp.metadata && queuedOp.metadata.operation === "create" && queuedOp.metadata.nodeType === nodeType) {
                            var queuedNodeEl = document.getElementById(queuedOp.metadata.tempNodeId);
                            if (queuedNodeEl) {
                                var queuedNodeSpan = queuedNodeEl.querySelector(".story-node");
                                if (queuedNodeSpan) {
                                    var queuedName = queuedNodeSpan.getAttribute("data-node-name");
                                    if (queuedName) {
                                        foundNames.push("[queued]" + queuedName);
                                        var queuedMatch = queuedName.match(new RegExp("^" + baseName + "[\\s]*([0-9]+)$"));
                                        if (queuedMatch) {
                                            var queuedNum = parseInt(queuedMatch[1], 10);
                                            console.log("[handleCreateNode] Found queued", nodeType, "with number:", queuedNum);
                                            if (queuedNum > maxNum) maxNum = queuedNum;
                                        }
                                    }
                                }
                            } else {
                                console.log("[handleCreateNode] Queued operation found but DOM element not found for tempNodeId:", queuedOp.metadata.tempNodeId);
                            }
                        }
                    }
                }
            }
            
            placeholderName = baseName + (maxNum + 1);
            console.log("[handleCreateNode] Generated name:", placeholderName, "based on maxNum:", maxNum, "found names:", foundNames.join(", "));
        }
        
        // Find parent element
        var parentElement = null;
        var parentContainer = null;
        
        if (parentPath === "story_graph") {
            // Creating epic at root - epics are rendered inside #scope-content
            parentContainer = document.getElementById("scope-content");
            if (!parentContainer) {
                // Fallback: try to find card-secondary inside scope-content
                var scopeContent = document.querySelector("#scope-content");
                if (scopeContent) {
                    parentContainer = scopeContent.querySelector(".card-secondary");
                }
            }
        } else {
            // Find parent node and its collapsible-content
            parentElement = findNodeElement(parentPath);
            if (parentElement) {
                // Find the collapsible-content div for this parent
                var parentWrapper = findNodeWrapper(parentElement);
                if (parentWrapper) {
                    // Look for collapsible-content within or after the wrapper
                    var nextSibling = parentWrapper.nextSibling;
                    while (nextSibling) {
                        if (nextSibling.nodeType === 1 && nextSibling.classList && nextSibling.classList.contains("collapsible-content")) {
                            parentContainer = nextSibling;
                            break;
                        }
                        nextSibling = nextSibling.nextSibling;
                    }
                    // If not found after, check if wrapper contains it
                    if (!parentContainer) {
                        parentContainer = parentWrapper.querySelector(".collapsible-content");
                    }
                }
            }
        }
        
        if (!parentContainer) {
            console.error("[handleCreateNode] Cannot find parent container for:", parentPath);
            // Fallback: refresh the panel
            if (typeof vscode !== "undefined") {
                vscode.postMessage({ command: "refresh" });
            }
            return;
        }
        
        // Create real node in DOM immediately
        // Generate a temporary path for the new node (will be updated by backend)
        var tempNodeId = "temp-" + Date.now() + "-" + Math.random().toString(36).substr(2, 9);
        var tempPath = parentPath === "story_graph" 
            ? 'story_graph."" + placeholderName + ""'
            : parentPath + '"."" + placeholderName + ""';

         var tempPath = parentPath === 'story_graph'
            ? 'story_graph."' + placeholderName + '"'
            : parentPath + '."' + placeholderName + '"';
        
        // Calculate position (append at end)
        var existingChildren = Array.prototype.slice.call(parentContainer.children);
        var position = existingChildren.length;
        
        // Find icon paths from existing DOM elements
        var plusIconPath = null;
        var subtractIconPath = null;
        var epicIconPath = null;
        var gearIconPath = null;
        var emptyIconPath = null;
        var documentIconPath = null;
        
        // Find plus and subtract icons from existing epic collapse icon
        var existingEpicIcon = document.querySelector("#epic-0-icon img.collapse-icon");
        if (existingEpicIcon) {
            plusIconPath = existingEpicIcon.src;
            // Try to find subtract icon from data attributes or derive from plus icon
            var epicIconSpan = document.querySelector("#epic-0-icon");
            if (epicIconSpan && epicIconSpan.getAttribute) {
                subtractIconPath = epicIconSpan.getAttribute("data-subtract");
            }
            if (!subtractIconPath && plusIconPath) {
                subtractIconPath = plusIconPath.replace("plus", "subtract");
            }
        }
        
        // Find epic icon from existing epic
        var existingEpic = document.querySelector('.story-node[data-node-type="epic"]');
        if (existingEpic && existingEpic.previousSibling && existingEpic.previousSibling.tagName === "IMG") {
            epicIconPath = existingEpic.previousSibling.src;
        } else if (existingEpic) {
            // Look for img before the epic node
            var parent = existingEpic.parentElement;
            if (parent) {
                var epicImg = parent.querySelector('img[alt="Epic"]');
                if (epicImg) epicIconPath = epicImg.src;
            }
        }
        
        // Find gear icon from existing sub-epic
        var existingSubEpic = document.querySelector('.story-node[data-node-type="sub-epic"]');
        if (existingSubEpic) {
            var parent = existingSubEpic.parentElement;
            if (parent) {
                var gearImg = parent.querySelector('img[alt="Sub-Epic"]');
                if (gearImg) gearIconPath = gearImg.src;
            }
        }
        
        // Find empty icon from existing story without scenarios (uses empty placeholder)
        var existingStory = document.querySelector('.story-node[data-node-type="story"]');
        if (existingStory) {
            var storyParent = existingStory.parentElement;
            if (storyParent) {
                // Look for empty icon span (sibling before story node)
                var emptySpan = storyParent.querySelector('span[style*="min-width: 9px"] img[alt=""]');
                if (emptySpan) {
                    emptyIconPath = emptySpan.src;
                }
                // Find document icon from story
                var documentImg = storyParent.querySelector('img[alt="Story"]');
                if (documentImg) {
                    documentIconPath = documentImg.src;
                }
            }
        }
        
        // Use EXACT same margin-top values as backend rendering
        // Backend uses: epic=8px, sub-epic=4px, story=2px, scenario=2px
        var marginTop = nodeType === "epic" ? "8px" : (nodeType === "story" || nodeType === "scenario" ? "2px" : "4px");
        
        // Calculate margin-left by copying from existing sibling (most reliable - uses backend-calculated value)
        // If no sibling exists, calculate using EXACT same formula as backend: marginLeft = 7 + (depth * 7)
        var marginLeft = 0;
        if (nodeType === "epic") {
            marginLeft = 0;
        } else if (parentContainer) {
            // First: try to find an existing node of the same type and copy its margin-left
            // This ensures we use the exact same value the backend calculated
            var existingNodeDiv = null;
            var containerChildren = Array.prototype.slice.call(parentContainer.children);
            for (var i = 0; i < containerChildren.length; i++) {
                var child = containerChildren[i];
                var matchingNode = child.querySelector ? child.querySelector('.story-node[data-node-type="' + nodeType + '"]') : null;
                if (matchingNode) {
                    existingNodeDiv = child;
                    break;
                }
            }
            
            if (existingNodeDiv && existingNodeDiv.style && existingNodeDiv.style.marginLeft) {
                // Copy exact margin-left from existing node (already calculated by backend)
                var existingMargin = existingNodeDiv.style.marginLeft;
                var marginMatch = existingMargin.match(/(\\d+)px/);
                if (marginMatch) {
                    marginLeft = parseInt(marginMatch[1], 10);
                    console.log("[handleCreateNode] Copied margin-left from existing node:", marginLeft, "px");
                }
            }
            
            // Fallback: calculate using backend formula if no existing node found
            if (!existingNodeDiv || !marginLeft) {
                if (nodeType === "sub-epic") {
                    // Backend formula: marginLeft = 7 + (depth * 7)
                    // Calculate depth by counting sub-epic ancestors
                    var depth = 0;
                    if (parentElement) {
                        var parentType = parentElement.getAttribute ? parentElement.getAttribute("data-node-type") : null;
                        if (parentType === "sub-epic") {
                            // Parent is a sub-epic, so we need to find its depth
                            var parentWrapper = findNodeWrapper(parentElement);
                            console.log("[handleCreateNode] Parent wrapper found:", !!parentWrapper, "parentType:", parentType);
                            if (parentWrapper) {
                                // Try multiple ways to read margin-left (cssText, style.marginLeft, computed style)
                                var parentMarginLeft = 0;
                                if (parentWrapper.style && parentWrapper.style.marginLeft) {
                                    var parentMargin = parentWrapper.style.marginLeft;
                                    var parentMatch = parentMargin.match(/(\\d+)px/);
                                    if (parentMatch) {
                                        parentMarginLeft = parseInt(parentMatch[1], 10);
                                    }
                                }
                                // Fallback: try reading from cssText
                                if (!parentMarginLeft && parentWrapper.style && parentWrapper.style.cssText) {
                                    var cssTextMatch = parentWrapper.style.cssText.match(/margin-left:\\s*(\\d+)px/);
                                    if (cssTextMatch) {
                                        parentMarginLeft = parseInt(cssTextMatch[1], 10);
                                    }
                                }
                                // Fallback: try computed style
                                if (!parentMarginLeft && typeof window.getComputedStyle !== "undefined") {
                                    try {
                                        var computedStyle = window.getComputedStyle(parentWrapper);
                                        var computedMargin = computedStyle.marginLeft;
                                        var computedMatch = computedMargin.match(/(\\d+)px/);
                                        if (computedMatch) {
                                            parentMarginLeft = parseInt(computedMatch[1], 10);
                                        }
                                    } catch (e) {
                                        console.warn("[handleCreateNode] Error reading computed style:", e);
                                    }
                                }
                                
                                console.log("[handleCreateNode] Parent margin-left read:", parentMarginLeft, "px");
                                
                                if (parentMarginLeft >= 7) {
                                    // Calculate parent"s depth: parentMarginLeft = 7 + (parentDepth * 7)
                                    // So: parentDepth = (parentMarginLeft - 7) / 7
                                    var parentDepth = (parentMarginLeft - 7) / 7;
                                    // Our depth is parent depth + 1
                                    depth = parentDepth + 1;
                                    console.log("[handleCreateNode] Calculated parentDepth:", parentDepth, "new depth:", depth);
                                } else if (parentMarginLeft === 0) {
                                    // Parent is epic (margin-left 0), so depth is 0
                                    depth = 0;
                                    console.log("[handleCreateNode] Parent is epic (margin-left 0), depth:", depth);
                                } else {
                                    // Unexpected margin-left value, try to infer depth
                                    console.warn("[handleCreateNode] Unexpected parent margin-left:", parentMarginLeft, "assuming depth 1");
                                    depth = 1;
                                }
                            } else {
                                // Parent wrapper not found, try to infer from parent type
                                console.warn("[handleCreateNode] Parent wrapper not found for sub-epic parent, assuming depth 1");
                                depth = 1;
                            }
                        } else if (parentType === "epic") {
                            // Parent is epic, so depth is 0
                            depth = 0;
                        }
                    }
                    // Use EXACT same formula as backend: marginLeft = 7 + (depth * 7)
                    marginLeft = 7 + (depth * 7);
                    console.log("[handleCreateNode] Calculated depth:", depth, "marginLeft:", marginLeft, "px (backend formula: 7 + (depth * 7))");
                } else {
                    // For stories: use parent"s margin + 7
                    if (parentElement) {
                        var parentWrapper = findNodeWrapper(parentElement);
                        if (parentWrapper && parentWrapper.style && parentWrapper.style.marginLeft) {
                            var parentMargin = parentWrapper.style.marginLeft;
                            var parentMatch = parentMargin.match(/(\\d+)px/);
                            if (parentMatch) {
                                marginLeft = parseInt(parentMatch[1], 10) + 7;
                            } else {
                                marginLeft = 14;
                            }
                        } else {
                            marginLeft = 14;
                        }
                    } else {
                        marginLeft = 14;
                    }
                }
            }
        } else {
            // No parent container - use defaults
            marginLeft = nodeType === "epic" ? 0 : (nodeType === "sub-epic" ? 7 : 14);
        }
        
        // Create collapse icon span - nodes that can have children get a collapse icon from the start
        // Epics, sub-epics, and stories can have children, so they get a + icon
        // Scenarios and acceptance-criteria cannot have children, so they get empty placeholder
        var collapseIconSpan = document.createElement("span");
        var collapsibleId = tempNodeId + "-content";
        var canHaveChildren = (nodeType === "epic" || nodeType === "sub-epic" || nodeType === "story");
        
        if (canHaveChildren && plusIconPath) {
            // Node can have children - create clickable collapse icon
            collapseIconSpan.id = collapsibleId + "-icon";
            collapseIconSpan.style.cssText = "display: inline-block; min-width: 9px; cursor: pointer;";
            collapseIconSpan.setAttribute("onclick", "event.stopPropagation(); toggleCollapse('" + collapsibleId + "')");
            collapseIconSpan.setAttribute("data-plus", plusIconPath);
            collapseIconSpan.setAttribute("data-subtract", subtractIconPath || plusIconPath.replace("plus", "subtract"));
            
            var collapseImg = document.createElement("img");
            collapseImg.className = "collapse-icon";
            collapseImg.src = plusIconPath;
            collapseImg.setAttribute("data-state", "collapsed");
            collapseImg.style.cssText = "width: 9px; height: 9px; vertical-align: middle;";
            collapseImg.alt = "Expand";
            collapseIconSpan.appendChild(collapseImg);
        } else if (emptyIconPath) {
            // Node cannot have children - use empty placeholder
            collapseIconSpan.style.cssText = "display: inline-block; min-width: 9px;";
            var emptyImg = document.createElement("img");
            emptyImg.src = emptyIconPath;
            emptyImg.style.cssText = "width: 9px; height: 9px; vertical-align: middle;";
            emptyImg.alt = "";
            collapseIconSpan.appendChild(emptyImg);
        } else {
            // Fallback: create empty span with same width if icon not found
            collapseIconSpan.style.cssText = "display: inline-block; min-width: 9px;";
        }
        
        // Create icon image (epic, gear, or document) - matching backend logic
        var iconImg = null;
        if (nodeType === "epic" && epicIconPath) {
            iconImg = document.createElement("img");
            iconImg.src = epicIconPath;
            iconImg.style.cssText = "width: 14px; height: 14px; vertical-align: middle; margin-right: 4px;";
            iconImg.alt = "Epic";
        } else if (nodeType === "sub-epic" && gearIconPath) {
            iconImg = document.createElement("img");
            iconImg.src = gearIconPath;
            iconImg.style.cssText = "width: 14px; height: 14px; vertical-align: middle; margin-right: 4px;";
            iconImg.alt = "Sub-Epic";
        } else if (nodeType === "story" && documentIconPath) {
            // Stories always get document icon (backend line 2250, 2275)
            iconImg = document.createElement("img");
            iconImg.src = documentIconPath;
            iconImg.style.cssText = "width: 14px; height: 14px; vertical-align: middle; margin-right: 4px;";
            iconImg.alt = "Story";
        }
        
        // Create story-node span
        var nodeSpan = document.createElement("span");
        nodeSpan.className = "story-node";
        nodeSpan.setAttribute("draggable", "true");
        nodeSpan.setAttribute("data-node-type", nodeType);
        nodeSpan.setAttribute("data-node-name", placeholderName);
        nodeSpan.setAttribute("data-path", tempPath);
        nodeSpan.setAttribute("data-position", position.toString());
        nodeSpan.setAttribute("data-has-children", "false");
        // Set behavior_needed and behaviors_needed for new empty nodes
        if (nodeType === "story") {
            nodeSpan.setAttribute("data-behavior-needed", "exploration");
            nodeSpan.setAttribute("data-behaviors-needed", JSON.stringify(["exploration", "scenarios"]));
        } else if (nodeType === "sub-epic") {
            nodeSpan.setAttribute("data-behavior-needed", "shape");
            nodeSpan.setAttribute("data-behaviors-needed", JSON.stringify(["shape", "exploration"]));
        } else if (nodeType === "epic") {
            nodeSpan.setAttribute("data-behavior-needed", "shape");
            nodeSpan.setAttribute("data-behaviors-needed", JSON.stringify(["shape"]));
        }
        nodeSpan.style.cssText = "cursor: pointer;";
        // For stories: icon goes INSIDE the span (backend line 2275: ${storyIcon}${name})
        // For epics/sub-epics: icon goes OUTSIDE the span
        if (nodeType === "story" && iconImg) {
            nodeSpan.appendChild(iconImg);
            nodeSpan.appendChild(document.createTextNode(placeholderName));
        } else {
            nodeSpan.textContent = placeholderName;
        }
        
        // Add click handler for selection
        nodeSpan.onclick = function() {
            if (typeof selectNode === "function") {
                selectNode(nodeType, placeholderName, { path: tempPath });
            }
        };
        
        // Create status message span
        var statusSpan = document.createElement("span");
        statusSpan.id = tempNodeId + "-status";
        statusSpan.style.cssText = "font-size: 11px; color: #666; font-style: italic; margin-left: 8px;";
        // Use the actual placeholderName in the status message
        statusSpan.textContent = placeholderName + " creating...";
        
        // Build the node structure matching epic/sub-epic format
        // For epics: <div style="margin-top: 8px">...</div> followed by <div class="collapsible-content">...</div>
        // For sub-epics: similar but with margin-left
        
        // Create the main node line div (matches exact backend structure)
        // Backend format: <div style="margin-left: Xpx; margin-top: 4px; font-size: 12px;">
        //                <span id="...-icon" ...><img .../></span> ${icon}${nameHtml}
        //                </div>
        var nodeLineDiv = document.createElement("div");
        // Use exact same style format as backend: margin-left in px, margin-top in px, font-size: 12px
        nodeLineDiv.style.cssText = "margin-left: " + marginLeft + "px; margin-top: " + marginTop + "; font-size: 12px;";
        
        // Build structure EXACTLY like backend: collapse icon span, SPACE, then icon img (for epics/sub-epics), then node span
        // For stories: icon goes INSIDE the node span (backend line 2275: ${storyIcon}${name})
        // Backend format: </span> ${icon}${name} - note the space after </span>
        nodeLineDiv.appendChild(collapseIconSpan);
        // Add space text node to match backend rendering (space between collapse icon and gear/epic icon)
        // For epics and sub-epics: icon is outside span, for stories: icon is inside span
        if (iconImg && nodeType !== "story") {
            nodeLineDiv.appendChild(document.createTextNode(" "));
            nodeLineDiv.appendChild(iconImg);
        }
        nodeLineDiv.appendChild(nodeSpan);
        // Add status span after node name (doesn"t affect collapse icon alignment)
        nodeLineDiv.appendChild(statusSpan);
        
        // Insert node line at end of parent container
        parentContainer.appendChild(nodeLineDiv);
        
        // For nodes that can have children (epics, sub-epics, stories), add empty collapsible-content div as sibling
        if (canHaveChildren && collapsibleId) {
            var collapsibleDiv = document.createElement("div");
            collapsibleDiv.id = collapsibleId;
            collapsibleDiv.className = "collapsible-content";
            collapsibleDiv.style.display = "none";
            // Insert as sibling after nodeLineDiv
            parentContainer.appendChild(collapsibleDiv);
        }
        
        // Store nodeLineDiv ID in metadata for rollback
        nodeLineDiv.id = tempNodeId;
        
        // Build command (include placeholderName so backend uses same name as frontend)
        var command = buildCreateCommand(parentPath, nodeType, placeholderName);
        
        // Validate command - if null, the operation is invalid
        if (!command) {
            console.error("[handleCreateNode] Invalid create command for", nodeType, "on", parentPath);
            // Remove optimistically created node
            var createdNode = document.getElementById(tempNodeId);
            if (createdNode) {
                createdNode.remove();
            }
            var collapsibleNode = document.getElementById(tempNodeId + "-content");
            if (collapsibleNode) {
                collapsibleNode.remove();
            }
            // Show error message to user
            var errorMsg = "Cannot create " + nodeType + " on Story Map root. Please select an epic or sub-epic first.";
            if (typeof vscode !== "undefined") {
                vscode.postMessage({
                    type: "showErrorDialog",
                    title: "Invalid Operation",
                    message: errorMsg
                });
            } else {
                alert(errorMsg);
            }
            return;
        }
        
        // Update parent"s collapse icon if this is its first child
        // Only update for nodes that can have children (epics, sub-epics, stories with scenarios)
        if (parentPath !== "story_graph" && (nodeType === "sub-epic" || nodeType === "story" || nodeType === "scenario")) {
            updateParentCollapseIcon(parentPath);
        }
        
        // Queue save
        if (window.storyMapSaveQueue) {
            window.storyMapSaveQueue.enqueue({
                command: command,
                rollback: function() {
                    // Remove created node on error (both node line and collapsible-content)
                    var createdNode = document.getElementById(tempNodeId);
                    if (createdNode) {
                        createdNode.remove();
                    }
                    var collapsibleNode = document.getElementById(tempNodeId + "-content");
                    if (collapsibleNode) {
                        collapsibleNode.remove();
                    }
                    // If this was the parent"s only child, restore empty placeholder
                    // (This is complex - for now, just leave the collapse icon)
                },
                metadata: {
                    operation: "create",
                    parentPath: parentPath,
                    nodeType: nodeType,
                    tempNodeId: tempNodeId
                }
            });
        } else {
            console.error("[handleCreateNode] storyMapSaveQueue not available");
        }
    };
    
    // Switch between Hierarchy, Increment, and Files views
    window.switchViewMode = function(viewMode) {
        console.log("[switchViewMode] Switching to", viewMode);
        
        // Get current view from active button
        var previousView = "Hierarchy";
        var btnHierarchy = document.getElementById("btn-view-hierarchy");
        var btnIncrement = document.getElementById("btn-view-increment");
        var btnFiles = document.getElementById("btn-view-files");
        
        if (btnHierarchy && btnHierarchy.style.color && !btnHierarchy.style.color.includes("faded")) previousView = "Hierarchy";
        else if (btnIncrement && btnIncrement.style.color && !btnIncrement.style.color.includes("faded")) previousView = "Increment";
        else if (btnFiles && btnFiles.style.color && !btnFiles.style.color.includes("faded")) previousView = "Files";
        
        // Update button styles to reflect selected state
        if (btnHierarchy) {
            var isSelected = viewMode === "Hierarchy";
            btnHierarchy.style.color = isSelected ? "var(--text-color, #fff)" : "var(--text-color-faded)";
        }
        if (btnIncrement) {
            var isSelected = viewMode === "Increment";
            btnIncrement.style.color = isSelected ? "var(--text-color, #fff)" : "var(--text-color-faded)";
        }
        if (btnFiles) {
            var isSelected = viewMode === "Files";
            btnFiles.style.color = isSelected ? "var(--text-color, #fff)" : "var(--text-color-faded)";
        }
        
        // Send message to extension to switch view FIRST (sets _currentStoryMapView)
        if (typeof vscode !== "undefined") {
            vscode.postMessage({
                command: "switchViewMode",
                viewMode: viewMode
            });
        }
        
        // If switching to Files view, prepare and apply file filter AFTER view mode is set
        if (viewMode === "Files") {
            var filterInput = document.getElementById("scopeFilterInput");
            if (filterInput) {
                var filterValue = filterInput.value.trim();
                
                // If no filter, default to showing all src files
                if (!filterValue) {
                    filterValue = "src/**/*.py";
                    filterInput.value = filterValue;
                } else {
                    // Add src/ prefix if neither src nor test is at the start
                    if (!filterValue.startsWith("src/") && !filterValue.startsWith("test/")) {
                        filterValue = "src/" + filterValue;
                        filterInput.value = filterValue;
                    }
                }
                
                // Trigger the filter update to switch to file view (after view mode is set)
                console.log("[switchViewMode] Applying file filter:", filterValue);
                // Use setTimeout to ensure switchViewMode message is processed first
                setTimeout(function() { updateFilter(filterValue); }, 50);
            }
        } else if (previousView === "Files" && (viewMode === "Hierarchy" || viewMode === "Increment")) {
            // Switching away from Files view - clear file filter and set view in one update
            console.log("[switchViewMode] Switching from Files to", viewMode, "- clearing file filter");
            clearScopeFilter(viewMode);
            return;
        }
    };
    
    // Switch include level (Stories, Domain, criteria, Scenarios, Examples, Tests, Code)
    window.switchIncludeLevel = function(level) {
        var levels = ["stories", "domain_concepts", "acceptance", "scenarios", "examples", "tests", "code"];
        var ids = { stories: "btn-include-stories", domain_concepts: "btn-include-domain", acceptance: "btn-include-acceptance", scenarios: "btn-include-scenarios", examples: "btn-include-examples", tests: "btn-include-tests", code: "btn-include-code" };
        for (var i = 0; i < levels.length; i++) {
            var btn = document.getElementById(ids[levels[i]]);
            if (btn) {
                var isSelected = level === levels[i];
                btn.style.color = isSelected ? "var(--text-color, #fff)" : "var(--text-color-faded)";
            }
        }
        if (typeof updateIncludeLevel === "function") updateIncludeLevel(level);
        var injectContainer = document.getElementById("inject-level-exec-toggle");
        if (injectContainer && injectContainer.classList.contains("execution-toggle-container") && injectContainer.classList.contains("expanded")) {
            injectContainer.classList.remove("expanded");
            if (window.getCollapseState && sessionStorage) {
                sessionStorage.setItem("collapseState", JSON.stringify(window.getCollapseState()));
            }
        }
    };
})();