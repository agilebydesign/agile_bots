/**
 * Panel tests: diagram action bar in story map view.
 * Tests rendering, button layout, visibility when node selected.
 * Routes through CLI. Uses generic fixtures (EpicA, SubEpicB).
 */

// Mock vscode before requiring any modules
const Module = require('module');
const originalRequire = Module.prototype.require;
Module.prototype.require = function (...args) {
    if (args[0] === 'vscode') {
        return require('../../helpers/mock_vscode');
    }
    return originalRequire.apply(this, args);
};

const { test, after, before } = require('node:test');
const assert = require('assert');
const path = require('path');
const os = require('os');
const fs = require('fs');
const { JSDOM } = require('jsdom');
const PanelView = require('../../../src/panel/panel_view');
const StoryMapView = require('../../../src/panel/story_map_view');

const repoRoot = path.join(__dirname, '../../..');
const productionBotPath = path.join(repoRoot, 'bots', 'story_bot');
const tempWorkspaceDir = fs.mkdtempSync(path.join(os.tmpdir(), 'agile-bots-diagram-action-bar-test-'));

function createMinimalStoryGraph() {
    return {
        epics: [
            {
                name: 'EpicA',
                sequential_order: 1,
                sub_epics: [
                    { name: 'SubEpicB', sequential_order: 1, sub_epics: [], story_groups: [] }
                ]
            }
        ]
    };
}

function setupTestWorkspace() {
    fs.mkdirSync(path.join(tempWorkspaceDir, 'docs', 'story'), { recursive: true });
    const storyGraphPath = path.join(tempWorkspaceDir, 'docs', 'story', 'story-graph.json');
    fs.writeFileSync(storyGraphPath, JSON.stringify(createMinimalStoryGraph(), null, 2), 'utf8');
    process.env.WORKING_AREA = tempWorkspaceDir;
    process.env.AGILE_BOTS_REPO_ROOT = repoRoot;
    const { verifyTestWorkspace } = require('../../helpers/prevent_production_writes');
    verifyTestWorkspace();
}

before(() => {
    setupTestWorkspace();
});

const cli = new PanelView(productionBotPath);

after(() => {
    cli.cleanup();
    if (fs.existsSync(tempWorkspaceDir)) {
        fs.rmSync(tempWorkspaceDir, { recursive: true, force: true });
    }
    delete process.env.AGILE_BOTS_REPO_ROOT;
    delete process.env.WORKING_AREA;
});

test('TestDiagramActionBarPanel', { concurrency: false }, async (t) => {
    await t.test('panel_shows_diagram_buttons_when_hierarchy_view_renders', async () => {
        await cli.execute('scope "EpicA"');
        const view = new StoryMapView(cli);
        const html = await view.render();

        assert.ok(html.includes('diagram-action-buttons-group'), 'Panel should have diagram action buttons group');
        assert.ok(html.includes('Render diagram'), 'Panel should show Render diagram button');
        assert.ok(html.includes('Save layout'), 'Panel should show Save layout button');
        assert.ok(html.includes('Clear layout'), 'Panel should show Clear layout button');
        assert.ok(html.includes('Update graph'), 'Panel should show Update graph button');
        assert.ok(html.includes('renderDiagram'), 'Render button should post renderDiagram command');
        assert.ok(html.includes('saveDiagramLayout'), 'Save button should post saveDiagramLayout command');
        assert.ok(html.includes('clearDiagramLayout'), 'Clear button should post clearDiagramLayout command');
        assert.ok(html.includes('updateFromDiagram'), 'Update button should post updateFromDiagram command');
    });

    await t.test('diagram_buttons_use_scope_from_selected_node', async () => {
        await cli.execute('scope "EpicA"');
        const view = new StoryMapView(cli);
        const html = await view.render();
        assert.ok(html.includes('window.diagramScope'), 'Diagram buttons should use window.diagramScope for scope');
    });

    await t.test('diagram_buttons_shown_when_non_root_node_selected', async () => {
        await cli.execute('scope "EpicA"');
        const view = new StoryMapView(cli);
        const html = await view.render();
        const dom = new JSDOM(html);
        const document = dom.window.document;
        const win = dom.window;

        const diagramGroup = document.getElementById('diagram-action-buttons-group');
        assert.ok(diagramGroup, 'Diagram action buttons group must exist in DOM');

        win.selectedNode = { type: 'root', name: null };
        diagramGroup.style.display = (win.selectedNode.type !== 'root') ? 'flex' : 'none';
        assert.strictEqual(diagramGroup.style.display, 'none', 'Diagram buttons hidden when root selected');

        win.selectedNode = { type: 'story', name: 'SubEpicB' };
        diagramGroup.style.display = (win.selectedNode.type !== 'root') ? 'flex' : 'none';
        assert.strictEqual(diagramGroup.style.display, 'flex', 'Diagram buttons shown when story node selected');

        dom.window.close();
    });
});
