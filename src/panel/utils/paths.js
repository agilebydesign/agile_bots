/**
 * Path formatting utilities for display in webview.
 * 
 * Functions for truncating, formatting, and displaying file paths
 * in the panel UI.
 */

/**
 * Truncate a path with ellipsis in the middle if too long.
 * Preserves both the beginning and end of the path for context.
 * 
 * @param {string} pathStr - Path to truncate
 * @param {number} maxLength - Maximum length before truncation
 * @returns {string} Truncated path with ellipsis if needed
 */
function truncatePath(pathStr, maxLength) {
    if (!pathStr || pathStr.length <= maxLength) {
        return pathStr || '';
    }
    const ellipsis = '...';
    const prefixLength = Math.floor((maxLength - ellipsis.length) / 2);
    const suffixLength = maxLength - ellipsis.length - prefixLength;
    return pathStr.substring(0, prefixLength) + ellipsis + pathStr.substring(pathStr.length - suffixLength);
}

module.exports = {
    truncatePath
};
