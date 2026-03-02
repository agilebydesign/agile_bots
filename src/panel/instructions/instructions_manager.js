/**
 * Instructions Manager
 * Server-side handlers for instructions-related messages from the webview.
 * 
 * Extracted from bot_panel.js to centralize instructions domain logic.
 */

const vscode = require('vscode');
const { Logger } = require('../utils');


async function executeCommand(botView, cmd, successMessage, errorMessage) {
    return botView?.execute(cmd)
        .then((result) => {
            if (result.status === 'error') {
                throw new Error(`Command error: ${result.message}`);
            }
            Logger.log(`[InstructionsManager] ${successMessage}`);
            vscode.window.showInformationMessage(successMessage);
        })
        .catch((error) => {
            Logger.log(`[InstructionsManager] ${errorMessage}: ${error.message}`);
            vscode.window.showErrorMessage(`${errorMessage}: ${error.message}`);
        });
}

/**
 * Save clarify answers (batch).
 */
async function saveClarifyAnswers(message, botView) {
    if (message.answers) {
        Logger.log(`[InstructionsManager] saveClarifyAnswers -> ${JSON.stringify(message.answers)}`);
        const answersJson = JSON.stringify(message.answers).replace(/'/g, "\\'");
        const cmd = `save --answers '${answersJson}'`;
        await executeCommand(botView, cmd, 'Answers saved successfully', 'Failed to save clarify answers');
    }    
}

/**
 * Update a single question answer.
 */
async function updateQuestionAnswer(message, botView) {
    if (message.question && typeof message.answer !== 'undefined') {
        Logger.log(`[InstructionsManager] updateQuestionAnswer -> ${message.question}: ${message.answer}`);
        const answers = {};
        answers[message.question] = message.answer;
        const answersJson = JSON.stringify(answers).replace(/'/g, "\\'");
        const cmd = `save --answers '${answersJson}'`;
        await executeCommand(botView, cmd, 'updateQuestionAnswer success', 'updateQuestionAnswer ERROR');
    }    
}

/**
 * Save clarify evidence.
 */
async function saveClarifyEvidence(message, botView) {
    if (message.evidence_provided) {
        Logger.log(`[InstructionsManager] saveClarifyEvidence -> ${JSON.stringify(message.evidence_provided)}`);
        const evidenceJson = JSON.stringify(message.evidence_provided).replace(/'/g, "\\'");
        const cmd = `save --evidence_provided '${evidenceJson}'`;
        await executeCommand(botView, cmd, 'Evidence saved successfully', 'Failed to save clarify evidence');
    }    
}

/**
 * Save a single strategy decision.
 */
async function saveStrategyDecision(message, botView) {
    if (message.criteriaKey && message.selectedOption) {
        Logger.log(`[InstructionsManager] saveStrategyDecision -> ${message.criteriaKey}: ${message.selectedOption}`);
        const decisions = {};
        decisions[message.criteriaKey] = message.selectedOption;
        const decisionsJson = JSON.stringify(decisions).replace(/'/g, "\\'");
        const cmd = `save --decisions '${decisionsJson}'`;
        await executeCommand(botView, cmd, 'Strategy decision saved successfully', 'Failed to save strategy decision');
    }    
}

/**
 * Save multi-select strategy decisions.
 */
async function saveStrategyMultiDecision(message, botView) {
    if (message.criteriaKey && message.selectedOptions) {
        Logger.log(`[InstructionsManager] saveStrategyMultiDecision -> ${message.criteriaKey}: ${JSON.stringify(message.selectedOptions)}`);
        const multiDecisions = {};
        multiDecisions[message.criteriaKey] = message.selectedOptions;
        const multiDecisionsJson = JSON.stringify(multiDecisions).replace(/'/g, "\\'");
        const cmd = `save --decisions '${multiDecisionsJson}'`;
        await executeCommand(botView, cmd, 'Strategy decisions saved successfully', 'Failed to save strategy decisions');
    }    
}

/**
 * Save strategy assumptions.
 */
async function saveStrategyAssumptions(message, botView) {
    if (message.assumptions) {
        Logger.log(`[InstructionsManager] saveStrategyAssumptions -> ${JSON.stringify(message.assumptions)}`);
        const assumptionsJson = JSON.stringify(message.assumptions).replace(/'/g, "\\'");
        const cmd = `save --assumptions '${assumptionsJson}'`;
        await executeCommand(botView, cmd, 'Additional strategies saved successfully', 'Failed to save additional strategies');
    }    
}

module.exports = {    
    saveClarifyAnswers,
    updateQuestionAnswer,
    saveClarifyEvidence,
    saveStrategyDecision,
    saveStrategyMultiDecision,
    saveStrategyAssumptions
};
