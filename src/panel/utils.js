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

class Logger {
    static logFilePath = '';
    static debugLogEnabled = false;

    constructor() {
        Logger.logFilePath = path.join(
            vscode.workspace.getConfiguration('agileBotsPanel').get('logFolder', './logs'),
            'panel-debug.log'
        );
        if (typeof process.env.PWD !== 'undefined') {
            Logger.logFilePath = path.join(process.env.PWD, 'logs', 'panel-debug.log');
        }
        Logger.debugLogEnabled = vscode.workspace.getConfiguration('agileBotsPanel').get('enableDebugLog', false);
    }

    enableLogging(enableLogging) { Logger.debugLogEnabled = enableLogging; }

    log(msg) {
        if (Logger.debugLogEnabled === false) return;
        const timestamp = new Date().toISOString();
        try { fs.appendFileSync(Logger.logFilePath, `${timestamp} ${msg}\n`); } catch (_) {}
        console.log(msg);
    }

    logToChannel(message, outputChannel = null) {
        const timestamp = new Date().toISOString();
        const logMessage = `[${timestamp}] ${message}`;
        console.log(logMessage);
        if (outputChannel) outputChannel.appendLine(logMessage);
    }
}

const _logger = new Logger();

module.exports = {
    escapeForHtml,
    escapeForJs,
    truncatePath,
    log: _logger.log.bind(_logger),
    logToChannel: _logger.logToChannel.bind(_logger),
    enableLogging: _logger.enableLogging.bind(_logger),
    Logger
};
