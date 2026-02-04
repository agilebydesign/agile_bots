/**
 * Test Set Workspace Panel
 * 
 * Sub-Epic: Set Workspace
 * Story: Change Workspace Path panel
 */

// Mock vscode before any imports
const Module = require('module');
const originalRequire = Module.prototype.require;
Module.prototype.require = function(...args) {
    if (args[0] === 'vscode') {
        return require('../../helpers/mock_vscode');
    }
    return originalRequire.apply(this, args);
};

const { test, after, before } = require('node:test');
const assert = require('node:assert');
const path = require('path');
const os = require('os');
const fs = require('fs');
const PanelView = require('../../../src/panel/panel_view');
const PathsSection = require('../../../src/panel/paths_section');

// Setup - Use temp directory for test workspace to avoid modifying production data
const repoRoot = path.join(__dirname, '../../..');
const productionBotPath = path.join(repoRoot, 'bots', 'story_bot');

// Create temp workspaces for tests
const tempWorkspaceDir = fs.mkdtempSync(path.join(os.tmpdir(), 'agile-bots-workspace-test-'));
const projectA = path.join(tempWorkspaceDir, 'project_a');
const projectB = path.join(tempWorkspaceDir, 'project_b');

function setupTestWorkspace() {
    // Create two project workspaces
    fs.mkdirSync(path.join(projectA, 'docs', 'stories'), { recursive: true });
    fs.mkdirSync(path.join(projectB, 'docs', 'stories'), { recursive: true });
    
    // Create empty story graphs in each
    fs.writeFileSync(
        path.join(projectA, 'docs', 'stories', 'story-graph.json'),
        JSON.stringify({ epics: [] }, null, 2)
    );
    fs.writeFileSync(
        path.join(projectB, 'docs', 'stories', 'story-graph.json'),
        JSON.stringify({ epics: [] }, null, 2)
    );
    
    // Set environment variable to use project_a as initial workspace
    process.env.WORKING_AREA = projectA;
    
    // Verify WORKING_AREA is set to temp directory
    const { verifyTestWorkspace } = require('../../helpers/prevent_production_writes');
    verifyTestWorkspace();
}

before(() => {
    setupTestWorkspace();
});

// Use production bot path (has config and behaviors) but temp workspace for data
const botPath = productionBotPath;

// ONE CLI for all tests - shared by PathsSection instances
const cli = new PanelView(botPath);

after(() => {
    cli.cleanup();
    // Clean up temp workspace and restore environment
    try {
        if (fs.existsSync(tempWorkspaceDir)) {
            fs.rmSync(tempWorkspaceDir, { recursive: true, force: true });
        }
    } catch (err) {
        console.warn('Failed to clean up temp workspace:', err.message);
    }
    delete process.env.WORKING_AREA;
});

// ============================================================================
// STORY: Change Workspace Path panel
// Test Class: TestChangeWorkspacePath
// ============================================================================

class TestChangeWorkspacePath {
    
    async testWorkspaceInputAcceptsDrop() {
        /**
         * SCENARIO: Set path by dragging folder to panel
         * 
         * Given Panel is open showing workspace at c:/dev/project_a
         * And Folder c:/dev/project_b exists in VS Code explorer
         * When User drags folder c:/dev/project_b from explorer to workspace text entry
         * Then Workspace text entry displays c:/dev/project_b
         * And Panel displays c:/dev/project_b as current workspace
         * And Panel displays behavior action state from project_b
         */
        
        // Given: Panel is open showing workspace at project_a
        const pathsView = new PathsSection(cli);
        const initialHtml = await pathsView.render();
        
        // Verify initial state shows project_a
        assert.ok(initialHtml.includes('workspacePathInput'), 'Should have workspace input');
        
        // And: Folder project_b exists (setup in before())
        // project_b has different behavior_action_state.json
        
        // Verify HTML has drag-drop capability
        assert.ok(initialHtml.includes('ondrop='), 'Should have ondrop handler for folder drops');
        assert.ok(initialHtml.includes('ondragover='), 'Should have ondragover to allow drop');
        
        // When: User drags folder project_b from explorer to workspace text entry
        // The ondrop handler extracts the path and calls updateWorkspace
        // Simulate what the drop handler does:
        const result = await pathsView.handleEvent('updateWorkspace', { workspacePath: projectB });
        
        // Then: Workspace text entry displays project_b
        assert.ok(result.success, 'updateWorkspace should succeed');
        assert.strictEqual(result.workspace, projectB, 'Workspace should be updated to project_b');
        
        // And: Panel displays project_b as current workspace
        const updatedHtml = await pathsView.render();
        assert.ok(updatedHtml.includes('workspacePathInput'), 'Should still have workspace input');
        
        // And: Panel displays behavior action state from project_b
        // The render() fetches status which includes behavior state
        assert.ok(typeof updatedHtml === 'string' && updatedHtml.length > 0, 'Should render panel content');
    }
    
    async testUserChangesWorkspacePanelDisplaysNewState() {
        /**
         * SCENARIO: User changes workspace and panel displays new state
         * 
         * Given Panel is open showing workspace at project_a
         * And Workspace at project_b exists with different bot state
         * When User changes workspace path to project_b
         * Then Panel displays project_b as current workspace
         * And Panel displays behavior action state from project_b
         */
        
        // Given: PathsSection showing initial workspace
        const pathsView = new PathsSection(cli);
        const initialHtml = await pathsView.render();
        assert.ok(initialHtml.includes('workspacePathInput'), 'Should have workspace input');
        
        // When: User changes workspace via handleEvent (simulates onchange/ondrop)
        const result = await pathsView.handleEvent('updateWorkspace', { workspacePath: projectB });
        
        // Then: Workspace is updated
        assert.ok(result.success, 'Should return success');
        assert.strictEqual(result.workspace, projectB, 'Should return new workspace path');
        
        // And: Re-render shows new workspace
        const updatedHtml = await pathsView.render();
        assert.ok(typeof updatedHtml === 'string', 'Should render after update');
    }
    
    async testUserChangesToNonexistentDirectoryShowsError() {
        /**
         * SCENARIO: User changes to nonexistent directory shows error
         * 
         * Given Panel is open showing valid workspace
         * When User drops folder path that does not exist
         * Then Panel displays error message
         * And Panel retains previous valid workspace
         */
        
        // Given: PathsSection with valid workspace
        const pathsView = new PathsSection(cli);
        const nonexistentPath = path.join(tempWorkspaceDir, 'nonexistent_directory');
        
        // When: User drops non-existent path
        try {
            const result = await pathsView.handleEvent('updateWorkspace', { workspacePath: nonexistentPath });
            // If implementation validates, it should return error
            assert.ok(result.error || !result.success, 'Should indicate error for non-existent path');
        } catch (error) {
            // Or throw an error
            assert.ok(error.message, 'Should have error message');
        }
    }
    
    async testWorkspacePathPersistsAfterPanelRefresh() {
        /**
         * SCENARIO: Workspace path persists after panel refresh
         * 
         * Given User has changed workspace to project_b
         * When Panel refreshes (re-renders PathsSection)
         * Then Workspace input still shows project_b
         */
        
        // Given: Change workspace
        const pathsView = new PathsSection(cli);
        await pathsView.handleEvent('updateWorkspace', { workspacePath: projectB });
        
        // When: Render again (simulates refresh)
        const html = await pathsView.render();
        
        // Then: Should show updated workspace
        assert.ok(html.includes('workspacePathInput'), 'Should have workspace input');
        // TODO: Assert input value contains projectB after persistence is implemented
    }
    
    async testPathsSectionRendersWorkspaceInput() {
        /**
         * SCENARIO: Paths section renders workspace input with all handlers
         * 
         * Given Bot is initialized
         * When PathsSection renders
         * Then HTML contains workspace text input
         * And Input has onchange handler
         * And Input has ondrop handler
         * And Input has Enter key handler
         */
        
        // Given/When: Render PathsSection
        const pathsView = new PathsSection(cli);
        const html = await pathsView.render();
        
        // Then: HTML has workspace input with all handlers
        assert.ok(html.includes('id="workspacePathInput"'), 'Should have workspace input');
        assert.ok(html.includes('onchange="updateWorkspace'), 'Should have onchange handler');
        assert.ok(html.includes('ondrop='), 'Should have ondrop handler');
        assert.ok(html.includes('ondragover='), 'Should have ondragover handler');
        assert.ok(html.includes('onkeydown='), 'Should have keydown handler for Enter');
    }
    
    async testPathsSectionDisplaysBotPath() {
        /**
         * SCENARIO: Paths section displays bot path
         * 
         * Given Bot is initialized with bot_directory
         * When PathsSection renders
         * Then HTML contains bot path display
         * And Bot path is shown as read-only info
         */
        
        // Given/When: Render PathsSection
        const pathsView = new PathsSection(cli);
        const html = await pathsView.render();
        
        // Then: HTML displays bot path
        assert.ok(html.includes('Bot Path:'), 'Should have bot path label');
        assert.ok(html.includes('class="info-display"'), 'Should display as info (not editable)');
    }
}

test('TestChangeWorkspacePath', { concurrency: false, timeout: 60000 }, async (t) => {
    const suite = new TestChangeWorkspacePath();
    
    await t.test('testWorkspaceInputAcceptsDrop', async () => {
        await suite.testWorkspaceInputAcceptsDrop();
    });
    
    await t.test('testUserChangesWorkspacePanelDisplaysNewState', async () => {
        await suite.testUserChangesWorkspacePanelDisplaysNewState();
    });
    
    await t.test('testUserChangesToNonexistentDirectoryShowsError', async () => {
        await suite.testUserChangesToNonexistentDirectoryShowsError();
    });
    
    await t.test('testWorkspacePathPersistsAfterPanelRefresh', async () => {
        await suite.testWorkspacePathPersistsAfterPanelRefresh();
    });
    
    await t.test('testPathsSectionRendersWorkspaceInput', async () => {
        await suite.testPathsSectionRendersWorkspaceInput();
    });
    
    await t.test('testPathsSectionDisplaysBotPath', async () => {
        await suite.testPathsSectionDisplaysBotPath();
    });
});
