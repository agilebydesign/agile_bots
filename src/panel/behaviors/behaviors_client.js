// Client-side functions for behaviors management, called from behaviors HTML templates

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

window.executeNavigationCommand = function(command) {
    console.log('[WebView] executeNavigationCommand click ->', command);
    vscode.postMessage({
        command: 'executeNavigationCommand',
        commandText: command
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

window.setBehaviorSpecialInstructions = function(textareaEl) {
    if (!textareaEl || textareaEl.tagName !== 'TEXTAREA') return;
    var behaviorName = textareaEl.getAttribute('data-behavior-name');
    var instructionText = (textareaEl.value || '').trim();
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
    var behaviorName = textareaEl.getAttribute('data-behavior-name');
    var actionName = textareaEl.getAttribute('data-action-name');
    var instructionText = (textareaEl.value || '').trim();
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

    // Check if a story map node is selected
    if (window.selectedNode && window.selectedNode.name) {
        if (window.selectedNode.type === 'increment') {
            console.log('[SUBMIT_DEBUG] WebView: increment selected, taking handleSubmitCurrent path');
            if (typeof handleSubmitCurrent === 'function') {
                handleSubmitCurrent();
            }
            return;
        }
        var nodePath = typeof resolveNodePath === 'function' ? resolveNodePath(window.selectedNode) : null;
        if (nodePath) {
            console.log('[SUBMIT_DEBUG] WebView: taking handleSubmitCurrent path (story map node selected)');
            if (typeof handleSubmitCurrent === 'function') {
                handleSubmitCurrent();
            }
            return;
        }
    }

    console.log('[SUBMIT_DEBUG] WebView: taking submitToChat path (behaviors submit)');
    submitToChat();
}

window.behaviorToTooltipText = function(behavior) {
    if (!behavior) return '';
    var name = behavior.name || '';
    var desc = behavior.description || '';
    if (desc) {
        return name + ': ' + desc;
    }
    return name;
}
