/**
 * Instructions Client JavaScript
 * Client-side handlers for instructions panel interactions.
 * 
 * Extracted from bot_panel_client.js to centralize instructions-related functionality.
 */

// ===== Constants =====
const INSTR_QA_COLLAPSE_KEY = 'agileBots_clarifyQACollapse';

// ===== Textarea Utilities =====

/**
 * Auto-resize textarea to fit content.
 * Called on input to dynamically adjust height.
 */
window.autoResizeTextarea = function(textarea) {
    if (!textarea) return;
    textarea.style.overflow = 'hidden';
    textarea.style.height = '0px';
    const height = textarea.scrollHeight;
    textarea.style.height = Math.max(60, height) + 'px';
    textarea.style.overflow = 'visible';
};

/**
 * Expand all clarify answer textareas to fit content.
 */
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

// ===== Clarify Q&A Collapse State =====

/**
 * Save collapse state for clarify Q&A textareas.
 */
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
        const all = JSON.parse(localStorage.getItem(INSTR_QA_COLLAPSE_KEY) || '{}');
        all[behavior] = state;
        localStorage.setItem(INSTR_QA_COLLAPSE_KEY, JSON.stringify(all));
    } catch (e) {
        console.error('[Instructions] saveClarifyQACollapseState error:', e);
    }
};

/**
 * Restore collapse state for clarify Q&A textareas.
 */
window.restoreClarifyQACollapseState = function(behavior) {
    if (!behavior || typeof localStorage === 'undefined') return;
    try {
        const all = JSON.parse(localStorage.getItem(INSTR_QA_COLLAPSE_KEY) || '{}');
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
    } catch (e) {
        console.error('[Instructions] restoreClarifyQACollapseState error:', e);
    }
};

// ===== Clarify Evidence =====

/**
 * Save clarify evidence to backend.
 */
window.saveClarifyEvidence = function() {
    console.log('[Instructions] saveClarifyEvidence triggered');
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
                console.log('[Instructions] Saving clarify evidence:', evidenceProvided);
                vscode.postMessage({
                    command: 'saveClarifyEvidence',
                    evidence_provided: evidenceProvided
                });
            }
        }
    }
};

// ===== Strategy Decisions =====

/**
 * Save a single strategy decision.
 */
window.saveStrategyDecision = function(criteriaKey, selectedOption) {
    console.log('[Instructions] saveStrategyDecision triggered:', criteriaKey, selectedOption);
    vscode.postMessage({
        command: 'saveStrategyDecision',
        criteriaKey: criteriaKey,
        selectedOption: selectedOption
    });
};

/**
 * Save a multi-select strategy decision.
 */
window.saveStrategyMultiDecision = function(criteriaKey, inputName) {
    console.log('[Instructions] saveStrategyMultiDecision triggered:', criteriaKey, inputName);
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
    console.log('[Instructions] Saving multi-select decision:', criteriaKey, selectedOptions);
    vscode.postMessage({
        command: 'saveStrategyMultiDecision',
        criteriaKey: criteriaKey,
        selectedOptions: selectedOptions
    });
};

/**
 * Save strategy assumptions.
 */
window.saveStrategyAssumptions = function() {
    console.log('[Instructions] saveStrategyAssumptions triggered');
    const assumptionsTextarea = document.getElementById('ws-strategy-assumptions') || document.getElementById('strategy-assumptions');
    if (assumptionsTextarea) {
        const assumptionsText = assumptionsTextarea.value?.trim();
        if (assumptionsText) {
            const assumptions = assumptionsText.split(/\n/).filter(a => a.trim());
            console.log('[Instructions] Saving strategy assumptions:', assumptions);
            vscode.postMessage({
                command: 'saveStrategyAssumptions',
                assumptions: assumptions
            });
        }
    }
};

// ===== Q&A Updates =====

/**
 * Update a question answer and save to backend.
 */
window.updateQuestionAnswer = function(question, answer) {
    console.log('[Instructions] updateQuestionAnswer:', question, answer);
    vscode.postMessage({
        command: 'updateQuestionAnswer',
        question: question,
        answer: answer
    });
};

console.log('[Instructions] instructions_client.js loaded');
