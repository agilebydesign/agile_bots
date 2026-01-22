/**
 * Base E2E Test Helper
 * 
 * Base class for all E2E-specific test helpers.
 * Provides parent reference pattern for accessing shared resources.
 * Mirrors: test/domain/helpers/base_helper.py
 */

class BaseE2EHelper {
    /**
     * Initialize with parent reference
     * @param {PanelE2ETestHelper} parent - Parent helper instance
     */
    constructor(parent) {
        this.parent = parent;
    }
    
    /**
     * Access VS Code WebView instance
     * @returns {import('vscode-extension-tester').WebView}
     */
    get webview() {
        return this.parent.webview;
    }
    
    /**
     * Access workspace directory
     * @returns {string}
     */
    get workspace() {
        return this.parent.workspace;
    }
    
    /**
     * Access bot directory
     * @returns {string}
     */
    get botDirectory() {
        return this.parent.botDirectory;
    }
    
    /**
     * Access story graph file path
     * @returns {string}
     */
    get storyGraphPath() {
        return this.parent.storyGraphPath;
    }
}

module.exports = BaseE2EHelper;
