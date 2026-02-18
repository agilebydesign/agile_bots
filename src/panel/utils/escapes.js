/**
 * HTML/JavaScript escaping utilities for webview content.
 * 
 * Centralized escape functions to prevent XSS and ensure 
 * proper encoding in HTML attributes, content, and JS strings.
 */

/**
 * Escape text for safe HTML content insertion.
 * Prevents XSS attacks by encoding special HTML characters.
 * 
 * @param {*} text - Text to escape (will be converted to string)
 * @returns {string} Escaped text safe for HTML content
 */
function escapeForHtml(text) {
    if (text === null || text === undefined) {
        return '';
    }
    if (typeof text !== 'string') {
        text = String(text);
    }
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Escape text for use in JavaScript string literals.
 * Handles backslashes, quotes, and control characters.
 * 
 * @param {*} text - Text to escape (will be converted to string)
 * @returns {string} Escaped text safe for JS string context
 */
function escapeForJs(text) {
    if (text === null || text === undefined) {
        return '';
    }
    if (typeof text !== 'string') {
        text = String(text);
    }
    return text
        .replace(/\\/g, '\\\\')
        .replace(/'/g, "\\'")
        .replace(/"/g, '\\"')
        .replace(/\n/g, '\\n')
        .replace(/\r/g, '\\r');
}

module.exports = {
    escapeForHtml,
    escapeForJs
};
