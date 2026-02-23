/**
 * Panel tests: diagram action bar in workspace section view.
 * Tests rendering, button layout, workspace section structure.
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
const PanelView = require('../../../src/panel/panel_view');
const WorkspaceSectionView = require('../../../src/panel/workspace_section_view');

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
    await t.test('workspace_section_shows_diagram_buttons', async () => {
        await cli.execute('scope "EpicA"');
        const botData = await cli.execute('status');
        const view = new WorkspaceSectionView(cli);
        view.parentView = { botData };
        const html = await view.render();

        assert.ok(html.includes('ws-diagram-buttons'), 'Workspace section should have diagram buttons container');
        assert.ok(html.includes('alt="Render Diagram"'), 'Should show Render Diagram icon button');
        assert.ok(html.includes('alt="Save Layout"'), 'Should show Save Layout icon button');
        assert.ok(html.includes('alt="Clear Layout"'), 'Should show Clear Layout icon button');
        assert.ok(html.includes('alt="Generate Report"'), 'Should show Generate Report icon button');
        assert.ok(html.includes('alt="Update Graph"'), 'Should show Update Graph icon button');
        assert.ok(html.includes('renderDiagram'), 'Render button should post renderDiagram command');
        assert.ok(html.includes('saveDiagramLayout'), 'Save button should post saveDiagramLayout command');
        assert.ok(html.includes('clearDiagramLayout'), 'Clear button should post clearDiagramLayout command');
        assert.ok(html.includes('generateDiagramReport'), 'Generate Report button should post generateDiagramReport command');
        assert.ok(html.includes('updateFromDiagram'), 'Update button should post updateFromDiagram command');
    });

    await t.test('workspace_section_has_diagrams_and_build_subsections', async () => {
        await cli.execute('scope "EpicA"');
        const botData = await cli.execute('status');
        const view = new WorkspaceSectionView(cli);
        view.parentView = { botData };
        const html = await view.render();

        assert.ok(html.includes('Diagrams'), 'Workspace section should have Diagrams subsection');
        assert.ok(html.includes('Build'), 'Workspace section should have Build subsection');
        assert.ok(html.includes('Workspace'), 'Should have Workspace section header');
    });

    await t.test('workspace_section_has_open_graph_and_open_all_buttons', async () => {
        await cli.execute('scope "EpicA"');
        const botData = await cli.execute('status');
        const view = new WorkspaceSectionView(cli);
        view.parentView = { botData };
        const html = await view.render();

        assert.ok(html.includes('ws-btn-open-graph'), 'Build subsection should have Open Graph button');
        assert.ok(html.includes('ws-btn-open-all'), 'Build subsection should have Open All button');
        assert.ok(html.includes('alt="Graph"'), 'Open Graph button should have Graph alt text');
        assert.ok(html.includes('alt="All"'), 'Open All button should have All alt text');
    });

    await t.test('diagram_buttons_use_scope', async () => {
        await cli.execute('scope "EpicA"');
        const botData = await cli.execute('status');
        const view = new WorkspaceSectionView(cli);
        view.parentView = { botData };
        const html = await view.render();
        assert.ok(html.includes('window.diagramScope'), 'Diagram buttons should use window.diagramScope for scope');
    });
});
