/**
 * Test-Safe Imports Utility
 * 
 * This module provides a safe way to import production code in tests.
 * It validates that tests are using test helpers or explicitly allowed imports,
 * and prevents accidental direct imports of production code.
 * 
 * RULE: Tests must NEVER directly import from src/ - they must use test helpers
 * or explicitly allow imports through this utility.
 */

const path = require('path');
const Module = require('module');

// Track which files are allowed to import production code
const ALLOWED_PRODUCTION_IMPORTERS = new Set([
    // Test helpers are allowed to import production code (they wrap it)
    path.resolve(__dirname, 'bot_view_test_helper.js'),
    path.resolve(__dirname, 'scope_view_test_helper.js'),
    path.resolve(__dirname, 'behaviors_view_test_helper.js'),
    path.resolve(__dirname, 'instructions_view_test_helper.js'),
]);

// Track which production modules are safe to import (for test helpers only)
const SAFE_PRODUCTION_MODULES = new Set([
    'panel_view',
    'bot_view',
    'story_map_view',
    'scope_view',
    'behaviors_view',
    'instructions_view',
    'bot_panel',
    'panel_view',
]);

/**
 * Check if a file is allowed to import production code
 * @param {string} importerPath - Path of the file doing the import
 * @returns {boolean} - True if allowed
 */
function isAllowedImporter(importerPath) {
    const resolvedPath = path.resolve(importerPath);
    return ALLOWED_PRODUCTION_IMPORTERS.has(resolvedPath);
}

/**
 * Check if importing from src/ is allowed
 * @param {string} modulePath - The module path being imported
 * @param {string} importerPath - Path of the file doing the import
 * @throws {Error} - If import is not allowed
 */
function validateImport(modulePath, importerPath) {
    // Check if this is an import from src/
    if (modulePath.includes('/src/') || modulePath.includes('\\src\\')) {
        const resolvedImporter = path.resolve(importerPath || '');
        const isTestHelper = isAllowedImporter(resolvedImporter);
        
        if (!isTestHelper) {
            // Get the calling file's stack trace
            const stack = new Error().stack;
            const callerLine = stack.split('\n')[3] || '';
            
            throw new Error(
                `TEST SAFETY VIOLATION: Direct import of production code detected!\n` +
                `  File: ${resolvedImporter}\n` +
                `  Import: ${modulePath}\n` +
                `  Caller: ${callerLine}\n\n` +
                `RULE: Tests must NEVER directly import from src/\n` +
                `SOLUTION: Use test helpers instead:\n` +
                `  - Use BotViewTestHelper instead of importing bot_view\n` +
                `  - Use ScopeViewTestHelper instead of importing scope_view\n` +
                `  - Use BehaviorsViewTestHelper instead of importing behaviors_view\n` +
                `  - Use InstructionsViewTestHelper instead of importing instructions_view\n` +
                `  - Use PanelViewTestHelper (if exists) instead of importing panel_view\n`
            );
        }
    }
}

/**
 * Safe require wrapper that validates imports
 * @param {string} modulePath - Path to module
 * @returns {*} - Required module
 */
function safeRequire(modulePath) {
    // Get the calling file from stack trace
    const stack = new Error().stack;
    const callerMatch = stack.match(/at .* \((.+):\d+:\d+\)/);
    const callerPath = callerMatch ? callerMatch[1] : '';
    
    // Validate the import
    validateImport(modulePath, callerPath);
    
    // If validation passes, do the actual require
    return require(modulePath);
}

/**
 * Intercept Module.prototype.require to catch direct imports
 * This should be called at the top of test files
 */
function interceptRequires() {
    const originalRequire = Module.prototype.require;
    
    Module.prototype.require = function(...args) {
        const modulePath = args[0];
        
        // Allow vscode mock (already handled elsewhere)
        if (modulePath === 'vscode') {
            return originalRequire.apply(this, args);
        }
        
        // Check for production code imports
        if (modulePath.includes('/src/') || modulePath.includes('\\src\\')) {
            // Get the calling file
            const stack = new Error().stack;
            const callerMatch = stack.match(/at .* \((.+):\d+:\d+\)/);
            const callerPath = callerMatch ? callerMatch[1] : '';
            
            // Validate
            validateImport(modulePath, callerPath);
        }
        
        // Proceed with original require
        return originalRequire.apply(this, args);
    };
}

module.exports = {
    safeRequire,
    interceptRequires,
    validateImport,
    isAllowedImporter,
};
