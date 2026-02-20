/**
 * Panel shared utilities — flat file so require('./utils') resolves without a subdirectory.
 */

const fs = require('fs');
const path = require('path');
const vscode = require('vscode');

// ── HTML / JS escaping ────────────────────────────────────────────────────────

function escapeForHtml(text) {
    if (text === null || text === undefined) return '';
    if (typeof text !== 'string') text = String(text);
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function escapeForJs(text) {
    if (text === null || text === undefined) return '';
    if (typeof text !== 'string') text = String(text);
    return text
        .replace(/\\/g, '\\\\')
        .replace(/'/g, "\\'")
        .replace(/"/g, '\\"')
        .replace(/\n/g, '\\n')
        .replace(/\r/g, '\\r');
}

// ── Path utilities ────────────────────────────────────────────────────────────

function truncatePath(pathStr, maxLength) {
    if (!pathStr || pathStr.length <= maxLength) return pathStr || '';
    const ellipsis = '...';
    const prefixLength = Math.floor((maxLength - ellipsis.length) / 2);
    const suffixLength = maxLength - ellipsis.length - prefixLength;
    return pathStr.substring(0, prefixLength) + ellipsis + pathStr.substring(pathStr.length - suffixLength);
}

// ── Logger ────────────────────────────────────────────────────────────────────

/**
 * Panel debug logger utility.
 * 
 * Centralized logging for panel debugging with file output
 * and console logging support.
 */
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
            configLogFolder = path.join(defaultLogFolder);
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

module.exports = {
    escapeForHtml,
    escapeForJs,
    truncatePath,
    Logger
};
