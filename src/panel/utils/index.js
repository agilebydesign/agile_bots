/**
 * Panel shared utilities index.
 * 
 * Central export point for all panel utility functions.
 * Import from this file for cleaner requires:
 *   const { escapeHtml, truncatePath, log } = require('./utils');
 */

const escapes = require('./escapes');
const paths = require('./paths');
const Logger = require('./logger.js');

module.exports = {
    // HTML escaping
    escapeForHtml: escapes.escapeForHtml,
    escapeForJs: escapes.escapeForJs,    
    
    // Path utilities
    truncatePath: paths.truncatePath,
    
    // Logging
    Logger: Logger
};
