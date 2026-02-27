const vscode = require("vscode");
const { Logger } = require("../utils");
const PanelView = require("../panel_view");

/**
 * BehaviorsManager handles routing of behaviors-related messages from the webview client
 * behaviors_client.js holds the client-side events
 */
class BehaviorsManager {
    
    constructor() {}

    static handleError(error, operation) {
        Logger.log(`[BehaviorsManager] ERROR ${operation}: ` + error.message);
        Logger.log(`[BehaviorsManager] ERROR stack: ` + error.stack);
        vscode.window.showErrorMessage(`Failed to ${operation}: ${error.message}`);
    }

    /**
     * Submit behavior rules to chat
     * @param {Webview.message} message 
     * @param {BotPanel} botPanel 
     */
    static async getBehaviorRules(message, botPanel) {
        if (!message.behaviorName) {
            return false;
        }

        Logger.log(`[BehaviorsManager] getBehaviorRules -> ${message.behaviorName}`);
        Logger.log(`[BehaviorsManager] STARTED for behavior: ${message.behaviorName}`);

        try {
            const result = await botPanel._sharedCLI.execute(`submitrules:${message.behaviorName}`);
            Logger.log('[BehaviorsManager] Rules submitted:', result);
            Logger.log(`[BehaviorsManager] Result received: ${JSON.stringify(result, null, 2)}`);

            if (result && typeof result === 'object') {
                Logger.log(`[BehaviorsManager] Result is object with status: ${result.status}`);
                if (result.status === 'success') {
                    const msg = result.message || `${message.behaviorName} rules submitted to chat!`;
                    Logger.log(`[BehaviorsManager] SUCCESS - showing message: ${msg}`);
                    vscode.window.showInformationMessage(msg);
                } else if (result.status === 'error') {
                    const errorMsg = result.message || 'Unknown error';
                    Logger.log(`[BehaviorsManager] ERROR status - showing error: ${errorMsg}`);
                    vscode.window.showErrorMessage(`Failed to submit rules: ${errorMsg}`);
                } else {
                    const outputStr = typeof result.output === 'string' ? result.output : '';
                    Logger.log(`[BehaviorsManager] Legacy format - output: ${outputStr}`);
                    if (outputStr.includes('submitted')) {
                        Logger.log(`[BehaviorsManager] Output includes 'submitted' - SUCCESS`);
                        vscode.window.showInformationMessage(`${message.behaviorName} rules submitted to chat!`);
                    } else {
                        const errorMsg = result.message || outputStr || 'Unknown error';
                        Logger.log(`[BehaviorsManager] Output does NOT include 'submitted' - ERROR: ${errorMsg}`);
                        vscode.window.showErrorMessage(`Failed to submit rules: ${errorMsg}`);
                    }
                }
            } else {
                Logger.log(`[BehaviorsManager] Result is NOT an object - type: ${typeof result}, value: ${result}`);
                vscode.window.showWarningMessage('Submit completed with unknown result');
            }

            Logger.log(`[BehaviorsManager] About to refresh panel`);
            return true;
        } catch (error) {
            Logger.log(`[BehaviorsManager] ERROR getting behavior rules: ${error.message}`);
            Logger.log(`[BehaviorsManager] CATCH BLOCK - Error: ${error.message}, Stack: ${error.stack}`);
            vscode.window.showErrorMessage(`Failed to get rules: ${error.message}`);
            return false;
        }
    }

    /**
     * Execute navigation command (back/current/next)
     * @param {Webview.message} message 
     * @param {BotPanel} botPanel 
     */
    static async executeNavigationCommand(message, botPanel) {
        if (!message.commandText) {
            return false;
        }

        Logger.log(`[BehaviorsManager] executeNavigationCommand -> ${message.commandText}`);
        
        try {
            const result = await botPanel._sharedCLI.execute(message.commandText);
            Logger.log(`[BehaviorsManager] executeNavigationCommand success: ${message.commandText} | result keys: ${Object.keys(result || {})}`);
            return true;
        } catch (error) {
            Logger.log(`[BehaviorsManager] executeNavigationCommand ERROR: ${error.message}`);
            Logger.log(`[BehaviorsManager] executeNavigationCommand STACK: ${error.stack}`);
            vscode.window.showErrorMessage(`Failed to execute ${message.commandText}: ${error.message}`);
            return false;
        }
    }

    /**
     * Set execution mode for an action
     * @param {Webview.message} message 
     * @param {BotPanel} botPanel 
     */
    static async setExecutionMode(message, botPanel) {
        if (!message.behaviorName || !message.actionName || !message.mode) {
            return false;
        }

        const cmd = `${message.behaviorName}.${message.actionName}.set_execution ${message.mode}`;
        Logger.log(`[BehaviorsManager] setExecutionMode -> ${cmd}`);

        try {
            await botPanel._sharedCLI.execute(cmd);
            Logger.log(`[BehaviorsManager] setExecutionMode success: ${cmd}`);
            if (botPanel._botView) botPanel._botView.botData = null;
            return true;
        } catch (error) {
            Logger.log(`[BehaviorsManager] setExecutionMode ERROR: ${error.message}`);
            vscode.window.showErrorMessage(`Failed to set execution mode: ${error.message}`);
            return false;
        }
    }

    /**
     * Set execution mode for a behavior
     * @param {Webview.message} message 
     * @param {BotPanel} botPanel 
     */
    static async setBehaviorExecuteMode(message, botPanel) {
        if (!message.behaviorName || !message.mode) {
            return false;
        }

        const cmd = `${message.behaviorName}.set_execution ${message.mode}`;
        Logger.log(`[BehaviorsManager] setBehaviorExecuteMode -> ${cmd}`);

        try {
            await botPanel._sharedCLI.execute(cmd);
            Logger.log(`[BehaviorsManager] setBehaviorExecuteMode success: ${cmd}`);
            if (botPanel._botView) botPanel._botView.botData = null;
            return true;
        } catch (error) {
            Logger.log(`[BehaviorsManager] setBehaviorExecuteMode ERROR: ${error.message}`);
            vscode.window.showErrorMessage(`Failed to set behavior execution mode: ${error.message}`);
            return false;
        }
    }

    /**
     * Set special instructions for a behavior
     * @param {Webview.message} message 
     * @param {BotPanel} botPanel 
     */
    static async setBehaviorSpecialInstructions(message, botPanel) {
        if (message.behaviorName === undefined) {
            return false;
        }

        const escaped = (message.instructionText || '').replace(/"/g, '\\"');
        const cmd = `${message.behaviorName}.set_special_instructions "${escaped}"`;
        Logger.log(`[BehaviorsManager] setBehaviorSpecialInstructions -> ${cmd}`);

        try {
            await botPanel._sharedCLI.execute(cmd);
            Logger.log(`[BehaviorsManager] setBehaviorSpecialInstructions success`);
            if (botPanel._botView) botPanel._botView.botData = null;
            return true;
        } catch (error) {
            Logger.log(`[BehaviorsManager] setBehaviorSpecialInstructions ERROR: ${error.message}`);
            vscode.window.showErrorMessage(`Failed to set special instructions: ${error.message}`);
            return false;
        }
    }

    /**
     * Set special instructions for an action
     * @param {Webview.message} message 
     * @param {BotPanel} botPanel 
     */
    static async setActionSpecialInstructions(message, botPanel) {
        if (!message.behaviorName || message.actionName === undefined) {
            return false;
        }

        const escaped = (message.instructionText || '').replace(/"/g, '\\"');
        const cmd = `${message.behaviorName}.${message.actionName}.special_instructions "${escaped}"`;
        Logger.log(`[BehaviorsManager] setActionSpecialInstructions -> ${cmd}`);

        try {
            await botPanel._sharedCLI.execute(cmd);
            Logger.log(`[BehaviorsManager] setActionSpecialInstructions success`);
            if (botPanel._botView) botPanel._botView.botData = null;
            return true;
        } catch (error) {
            Logger.log(`[BehaviorsManager] setActionSpecialInstructions ERROR: ${error.message}`);
            vscode.window.showErrorMessage(`Failed to set special instructions: ${error.message}`);
            return false;
        }
    }

    /**
     * Navigate to a specific behavior
     * @param {Webview.message} message 
     * @param {BotPanel} botPanel 
     */
    static async navigateToBehavior(message, botPanel) {
        if (!message.behaviorName) {
            return false;
        }

        const cmd = `${message.behaviorName}`;
        Logger.log(`[BehaviorsManager] navigateToBehavior -> ${cmd}`);

        try {
            const result = await botPanel._sharedCLI.execute(cmd);
            
            if (result?.bot) {
                botPanel._botView.botData = result.bot;
                if (result.instructions) {
                    botPanel._botView.botData.instructions = result.instructions;
                }
                PanelView._lastResponse = result;
            }
            return true;
        } catch (error) {
            Logger.log(`[BehaviorsManager] navigateToBehavior ERROR: ${error.message}`);
            Logger.log(`[BehaviorsManager] navigateToBehavior STACK: ${error.stack}`);
            vscode.window.showErrorMessage(`Failed to navigate to behavior: ${error.message}`);
            return false;
        }
    }

    /**
     * Submit workspace behavior instructions to chat
     * @param {Webview.message} message 
     * @param {BotPanel} botPanel 
     */
    static async submitWorkspaceBehaviorInstructions(message, botPanel) {
        if (!message.behavior || !botPanel._botView) {
            return false;
        }

        const behaviorName = message.behavior;
        Logger.log(`[BehaviorsManager] submitWorkspaceBehaviorInstructions -> ${behaviorName}`);

        try {
            const result = await botPanel._botView.execute(behaviorName);
            
            if (result?.bot) {
                botPanel._botView.botData = result.bot;
                if (result.instructions) {
                    botPanel._botView.botData.instructions = result.instructions;
                }
                PanelView._lastResponse = result;
            }
            
            // This method handles its own update flow
            await botPanel._updateWithCachedData();
            
            const output = await botPanel._botView.execute('submit');
            
            if (output && typeof output === 'object' && output.status) {
                if (output.status === 'success') {
                    vscode.window.showInformationMessage(output.message || 'Instructions submitted to chat!');
                } else {
                    vscode.window.showErrorMessage(`Submit failed: ${output.message || output.error || 'Unknown error'}`);
                }
            } else {
                const outputStr = typeof output === 'string' ? output : JSON.stringify(output || '');
                if (outputStr && (outputStr.includes('SUCCESS:') || outputStr.includes('submitted to Cursor chat successfully'))) {
                    vscode.window.showInformationMessage('Instructions submitted to chat!');
                } else if (outputStr && (outputStr.includes('ERROR:') || outputStr.includes('FAILED:'))) {
                    const errorMatch = outputStr.match(/ERROR:|FAILED:\s*(.+)/);
                    vscode.window.showErrorMessage(`Submit failed: ${errorMatch ? errorMatch[1] : 'Unknown error'}`);
                } else {
                    vscode.window.showWarningMessage('Submit completed with unknown result');
                }
            }
            return false; // Already updated internally
        } catch (error) {
            Logger.log(`[BehaviorsManager] submitWorkspaceBehaviorInstructions ERROR: ${error.message}`);
            vscode.window.showErrorMessage(`Submit failed: ${error.message}`);
            return false;
        }
    }

    /**
     * Navigate to a specific action within a behavior
     * @param {Webview.message} message 
     * @param {BotPanel} botPanel 
     */
    static async navigateToAction(message, botPanel) {
        if (!message.behaviorName || !message.actionName) {
            return false;
        }

        const cmd = `${message.behaviorName}.${message.actionName}`;
        Logger.log(`[BehaviorsManager] navigateToAction: ${cmd}`);

        try {
            const result = await botPanel._sharedCLI.execute(cmd);
            
            Logger.log(`[BehaviorsManager] navigateToAction result keys: ${Object.keys(result || {}).join(', ')}`);
            Logger.log(`[BehaviorsManager] result.bot? ${!!result?.bot}`);
            Logger.log(`[BehaviorsManager] result.instructions? ${!!result?.instructions}`);
            
            if (result?.instructions) {
                Logger.log(`[BehaviorsManager] result.instructions keys: ${Object.keys(result.instructions).join(', ')}`);
            }

            if (result?.bot) {
                botPanel._botView.botData = result.bot;
                if (result.instructions) {
                    botPanel._botView.botData.instructions = result.instructions;
                    Logger.log(`[BehaviorsManager] Copied instructions into botData`);
                } else {
                    Logger.log(`[BehaviorsManager] WARNING: No instructions in result to copy!`);
                }
                PanelView._lastResponse = result;
            } else {
                Logger.log(`[BehaviorsManager] WARNING: No result.bot - not caching!`);
            }

            // Send message to expand instructions section after update
            const expandAfterUpdate = () => {
                setTimeout(() => {
                    try {
                        Logger.log(`[BehaviorsManager] Sending expandInstructionsSection for: ${message.actionName}`);
                        botPanel._panel.webview.postMessage({
                            command: 'expandInstructionsSection',
                            actionName: message.actionName
                        });
                    } catch (postErr) {
                        Logger.log(`[BehaviorsManager] Error sending expandInstructionsSection: ${postErr.message}`);
                    }
                }, 200);
            };
            expandAfterUpdate();
            return true;
        } catch (error) {
            Logger.log(`[BehaviorsManager] navigateToAction ERROR: ${error.message}`);
            Logger.log(`[BehaviorsManager] navigateToAction STACK: ${error.stack}`);
            vscode.window.showErrorMessage(`Failed to navigate to action: ${error.message}`);
            return false;
        }
    }

    /**
     * Navigate to action and execute an operation
     * @param {Webview.message} message 
     * @param {BotPanel} botPanel 
     */
    static async navigateAndExecute(message, botPanel) {
        if (!message.behaviorName || !message.actionName || !message.operationName) {
            return false;
        }

        const command = `${message.behaviorName}.${message.actionName}.${message.operationName}`;
        Logger.log(`[BehaviorsManager] navigateAndExecute -> ${command}`);

        try {
            const result = await botPanel._sharedCLI.execute(command);
            Logger.log(`[BehaviorsManager] navigateAndExecute success: ${command} | result keys: ${Object.keys(result || {})}`);

            if (result?.bot) {
                botPanel._botView.botData = result.bot;
                if (result.instructions) {
                    botPanel._botView.botData.instructions = result.instructions;
                }
                PanelView._lastResponse = result;
            }
            return true;
        } catch (error) {
            Logger.log(`[BehaviorsManager] navigateAndExecute ERROR: ${error.message}`);
            Logger.log(`[BehaviorsManager] navigateAndExecute STACK: ${error.stack}`);
            vscode.window.showErrorMessage(`Failed to execute operation: ${error.message}`);
            return false;
        }
    }
}

module.exports = BehaviorsManager;
