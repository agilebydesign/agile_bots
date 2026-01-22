/**
 * Panel E2E Test Helper
 * 
 * Main test helper for E2E panel tests with vscode-extension-tester.
 * Provides access to all sub-helpers via property accessors.
 * 
 * Mirrors: test/domain/bot_test_helper.py
 * Usage: 
 *   const helper = new PanelE2ETestHelper(workspace);
 *   await helper.setupPanel();
 *   await helper.given.storyGraphLoadedInPanel();
 *   await helper.when.userSelectsEpic('Build Agile Bots');
 *   await helper.then.panelDisplaysCreateSubEpicButton();
 */

const path = require('path');
const fs = require('fs');
const { WebView, EditorView, Workbench } = require('vscode-extension-tester');
const StoryGraphE2EHelper = require('./story_graph_e2e_helper');
const GivenE2EHelper = require('./given_e2e_helper');
const WhenE2EHelper = require('./when_e2e_helper');
const ThenE2EHelper = require('./then_e2e_helper');

class PanelE2ETestHelper {
    /**
     * Initialize E2E test helper
     * @param {string} workspacePath - Test workspace directory path
     * @param {string} botPath - Bot directory path (defaults to story_bot)
     */
    constructor(workspacePath, botPath = null) {
        this.workspace = workspacePath;
        
        // Default to story_bot in workspace
        if (!botPath) {
            const repoRoot = path.join(__dirname, '../../..');
            this.botDirectory = path.join(repoRoot, 'bots', 'story_bot');
        } else {
            this.botDirectory = botPath;
        }
        
        // Story graph path
        this.storyGraphPath = path.join(this.workspace, 'docs', 'stories', 'story-graph.json');
        
        // WebView instance (set during setupPanel)
        this.webview = null;
        
        // Initialize sub-helpers with parent reference pattern
        this.storyGraph = new StoryGraphE2EHelper(this);
        this.given = new GivenE2EHelper(this);
        this.when = new WhenE2EHelper(this);
        this.then = new ThenE2EHelper(this);
    }
    
    /**
     * Set up test workspace structure
     * Creates necessary directories for bot operation
     */
    setupWorkspace() {
        // Create directory structure
        const docsDir = path.join(this.workspace, 'docs', 'stories');
        fs.mkdirSync(docsDir, { recursive: true });
        
        console.log(`[E2E Setup] Created workspace structure at: ${this.workspace}`);
    }
    
    /**
     * Set up panel for testing
     * Opens the Story Bot panel and gets WebView reference
     */
    async setupPanel() {
        // Close welcome page (it's also a webview and can interfere)
        await new EditorView().closeAllEditors();
        
        // Open Story Bot panel command
        const workbench = new Workbench();
        await workbench.executeCommand('storyBot.showPanel');
        
        // Give panel time to load
        await this.sleep(2000);
        
        // Get WebView reference
        this.webview = new WebView();
        
        console.log('[E2E Setup] Story Bot panel opened');
    }
    
    /**
     * Navigate to panel (alias for setupPanel)
     * Maintains compatibility with existing test structure
     */
    async navigateToPanel() {
        if (!this.webview) {
            await this.setupPanel();
        }
    }
    
    /**
     * Execute Python CLI command in bot workspace
     * @param {string} command - Python CLI command (e.g., "get-help")
     * @param {string[]} args - Command arguments
     * @returns {object} Command result { stdout, stderr, exitCode }
     */
    executeBotCommand(command, args = []) {
        const { spawnSync } = require('child_process');
        const cliPath = path.join(this.botDirectory, 'story_bot_cli');
        
        // Build command
        const fullArgs = [cliPath, '--workspace', this.workspace, command, ...args];
        
        // Execute
        const result = spawnSync('python', fullArgs, {
            cwd: this.botDirectory,
            encoding: 'utf-8'
        });
        
        return {
            stdout: result.stdout || '',
            stderr: result.stderr || '',
            exitCode: result.status || 0
        };
    }
    
    /**
     * Sleep helper for waiting
     * @param {number} ms - Milliseconds to sleep
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    /**
     * Cleanup resources (no server to stop)
     */
    async cleanup() {
        // Switch back from webview if still in it
        if (this.webview) {
            try {
                await this.webview.switchBack();
            } catch (e) {
                // Already switched back
            }
        }
        console.log('[E2E Cleanup] Resources cleaned up');
    }
}

module.exports = { PanelE2ETestHelper };
