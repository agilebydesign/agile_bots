/**
 * Panel debug logger utility.
 * 
 * Centralized logging for panel debugging with file output
 * and console logging support.
 */

const fs = require('fs');
const path = require('path');
const vscode = require('vscode');

class Logger {
    static logFilePath = "";
    static debugLogEnabled = "";

    constructor() {}

    /**
     * Initialize static Logger with a default folder passed from extension host.
     * @param {string} defaultLogFolder 
     */
    static initializeLogger(defaultLogFolder) {
        var configLogFolder = vscode.workspace.getConfiguration('agileBotsPanel').get('logFolder');
        if (typeof configLogFolder === 'undefined' || configLogFolder === "") {
            configLogFolder = path.join(defaultLogFolder, 'logs');
        }
        Logger.logFilePath = path.join(configLogFolder, 'panel-debug.log');   

        if (typeof process.env.PWD !== 'undefined') {
            // overwite with debug config
            Logger.logFilePath = path.join(process.env.PWD, 'logs', 'panel-debug.log');
        }

        Logger.debugLogEnabled = vscode.workspace.getConfiguration('agileBotsPanel').get('enableDebugLog', false) 
    }    

    /**
     * Set this to true to enable logging and overwrite VS Code setting - "Agile Bots Panel: Enable Debug Log". 
     * @param {boolean} enableLogging 
     */
    static enableLogging(enableLogging) {
        Logger.debugLogEnabled = enableLogging;
    }

    /**
     * Log message with timestamp to both console and debug file.
     * Writes to panel-debug.log in the current working directory.
     * 
     * @param {string} msg - Message to log
     */
    static log(msg) {
        if (Logger.debugLogEnabled === false) return;
        const timestamp = new Date().toISOString();
        try {        
            fs.appendFileSync(Logger.logFilePath, `${timestamp} ${msg}\n`);
        } catch (e) {
            // Silently ignore file write errors (permissions, disk full, etc.)
        }
        console.log(msg);
    }

    /**
     * Log message with timestamp to VS Code output channel and console.
     * Used by extension.js for VS Code integrated logging.
     * 
     * @param {string} message - Message to log
     * @param {Object|null} outputChannel - VS Code output channel (optional)
     */
    static logToChannel(message, outputChannel = null) {
        const timestamp = new Date().toISOString();
        const logMessage = `[${timestamp}] ${message}`;
        console.log(logMessage);
        if (outputChannel) {
            outputChannel.appendLine(logMessage);
        }
    }
}

module.exports = Logger;
