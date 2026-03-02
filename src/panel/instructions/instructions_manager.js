/**
 * Instructions Manager
 * Server-side handlers for instructions-related messages from the webview.
 * 
 * Extracted from bot_panel.js to centralize instructions domain logic.
 */

const vscode = require('vscode');
const { Logger } = require('../utils');

/**
 * Handle instructions-related messages from the webview.
 * 
 * @param {string} command - The message command
 * @param {Object} message - The full message object
 * @param {Object} botView - The BotView instance for executing commands
 * @returns {boolean} True if the message was handled, false otherwise
 */
function handleInstructionsMessage(command, message, botView) {
    switch (command) {
        case "saveClarifyAnswers":
            return handleSaveClarifyAnswers(message, botView);
        
        case "updateQuestionAnswer":
            return handleUpdateQuestionAnswer(message, botView);
        
        case "saveClarifyEvidence":
            return handleSaveClarifyEvidence(message, botView);
        
        case "saveStrategyDecision":
            return handleSaveStrategyDecision(message, botView);
        
        case "saveStrategyMultiDecision":
            return handleSaveStrategyMultiDecision(message, botView);
        
        case "saveStrategyAssumptions":
            return handleSaveStrategyAssumptions(message, botView);
        
        default:
            return false;
    }
}

/**
 * Save clarify answers (batch).
 */
function handleSaveClarifyAnswers(message, botView) {
    if (message.answers) {
        Logger.log(`[InstructionsManager] saveClarifyAnswers -> ${JSON.stringify(message.answers)}`);
        const answersJson = JSON.stringify(message.answers).replace(/'/g, "\\'");
        const cmd = `save --answers '${answersJson}'`;
        botView?.execute(cmd)
            .then(() => {
                Logger.log(`[InstructionsManager] saveClarifyAnswers success`);
                vscode.window.showInformationMessage('Answers saved successfully');
            })
            .catch((error) => {
                Logger.log(`[InstructionsManager] saveClarifyAnswers ERROR: ${error.message}`);
                vscode.window.showErrorMessage(`Failed to save clarify answers: ${error.message}`);
            });
    }
    return true;
}

/**
 * Update a single question answer.
 */
function handleUpdateQuestionAnswer(message, botView) {
    if (message.question && typeof message.answer !== 'undefined') {
        Logger.log(`[InstructionsManager] updateQuestionAnswer -> ${message.question}: ${message.answer}`);
        const answers = {};
        answers[message.question] = message.answer;
        const answersJson = JSON.stringify(answers).replace(/'/g, "\\'");
        const cmd = `save --answers '${answersJson}'`;
        botView?.execute(cmd)
            .then(() => {
                Logger.log(`[InstructionsManager] updateQuestionAnswer success`);
            })
            .catch((error) => {
                Logger.log(`[InstructionsManager] updateQuestionAnswer ERROR: ${error.message}`);
            });
    }
    return true;
}

/**
 * Save clarify evidence.
 */
function handleSaveClarifyEvidence(message, botView) {
    if (message.evidence_provided) {
        Logger.log(`[InstructionsManager] saveClarifyEvidence -> ${JSON.stringify(message.evidence_provided)}`);
        const evidenceJson = JSON.stringify(message.evidence_provided).replace(/'/g, "\\'");
        const cmd = `save --evidence_provided '${evidenceJson}'`;
        botView?.execute(cmd)
            .then(() => {
                Logger.log(`[InstructionsManager] saveClarifyEvidence success`);
                vscode.window.showInformationMessage('Evidence saved successfully');
            })
            .catch((error) => {
                Logger.log(`[InstructionsManager] saveClarifyEvidence ERROR: ${error.message}`);
                vscode.window.showErrorMessage(`Failed to save clarify evidence: ${error.message}`);
            });
    }
    return true;
}

/**
 * Save a single strategy decision.
 */
function handleSaveStrategyDecision(message, botView) {
    if (message.criteriaKey && message.selectedOption) {
        Logger.log(`[InstructionsManager] saveStrategyDecision -> ${message.criteriaKey}: ${message.selectedOption}`);
        const decisions = {};
        decisions[message.criteriaKey] = message.selectedOption;
        const decisionsJson = JSON.stringify(decisions).replace(/'/g, "\\'");
        const cmd = `save --decisions '${decisionsJson}'`;
        botView?.execute(cmd)
            .then(() => {
                Logger.log(`[InstructionsManager] saveStrategyDecision success`);
                vscode.window.showInformationMessage('Strategy decision saved successfully');
            })
            .catch((error) => {
                Logger.log(`[InstructionsManager] saveStrategyDecision ERROR: ${error.message}`);
                vscode.window.showErrorMessage(`Failed to save strategy decision: ${error.message}`);
            });
    }
    return true;
}

/**
 * Save multi-select strategy decisions.
 */
function handleSaveStrategyMultiDecision(message, botView) {
    if (message.criteriaKey && message.selectedOptions) {
        Logger.log(`[InstructionsManager] saveStrategyMultiDecision -> ${message.criteriaKey}: ${JSON.stringify(message.selectedOptions)}`);
        const multiDecisions = {};
        multiDecisions[message.criteriaKey] = message.selectedOptions;
        const multiDecisionsJson = JSON.stringify(multiDecisions).replace(/'/g, "\\'");
        const cmd = `save --decisions '${multiDecisionsJson}'`;
        botView?.execute(cmd)
            .then(() => {
                Logger.log(`[InstructionsManager] saveStrategyMultiDecision success`);
                vscode.window.showInformationMessage('Strategy decisions saved successfully');
            })
            .catch((error) => {
                Logger.log(`[InstructionsManager] saveStrategyMultiDecision ERROR: ${error.message}`);
                vscode.window.showErrorMessage(`Failed to save strategy decisions: ${error.message}`);
            });
    }
    return true;
}

/**
 * Save strategy assumptions.
 */
function handleSaveStrategyAssumptions(message, botView) {
    if (message.assumptions) {
        Logger.log(`[InstructionsManager] saveStrategyAssumptions -> ${JSON.stringify(message.assumptions)}`);
        const assumptionsJson = JSON.stringify(message.assumptions).replace(/'/g, "\\'");
        const cmd = `save --assumptions '${assumptionsJson}'`;
        botView?.execute(cmd)
            .then(() => {
                Logger.log(`[InstructionsManager] saveStrategyAssumptions success`);
                vscode.window.showInformationMessage('Additional strategies saved successfully');
            })
            .catch((error) => {
                Logger.log(`[InstructionsManager] saveStrategyAssumptions ERROR: ${error.message}`);
                vscode.window.showErrorMessage(`Failed to save additional strategies: ${error.message}`);
            });
    }
    return true;
}

module.exports = {
    handleInstructionsMessage,
    handleSaveClarifyAnswers,
    handleUpdateQuestionAnswer,
    handleSaveClarifyEvidence,
    handleSaveStrategyDecision,
    handleSaveStrategyMultiDecision,
    handleSaveStrategyAssumptions
};
