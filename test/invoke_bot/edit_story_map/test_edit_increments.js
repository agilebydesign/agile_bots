const Module = require('module');
const originalRequire = Module.prototype.require;
Module.prototype.require = function(...args) {
    if (args[0] === 'vscode') {
        return require('../../helpers/mock_vscode');
    }
    return originalRequire.apply(this, args);
};

const { test, describe, after } = require('node:test');
const assert = require('node:assert');
const path = require('path');
const os = require('os');
const fs = require('fs');

const repoRoot = path.join(__dirname, '../../..');
const productionBotPath = path.join(repoRoot, 'bots', 'story_bot');
const tempWorkspaceDir = fs.mkdtempSync(path.join(os.tmpdir(), 'agile-bots-increment-test-'));

const IncrementView = require('../../../src/panel/increment_view');
const PanelView = require('../../../src/panel/panel_view');


function setupTestWorkspace() {
    fs.mkdirSync(path.join(tempWorkspaceDir, 'docs', 'story'), { recursive: true });
    const storyGraphPath = path.join(tempWorkspaceDir, 'docs', 'story', 'story-graph.json');
    fs.writeFileSync(storyGraphPath, JSON.stringify({ 
        epics: [],
        increments: [
            {
                name: "MVP Release",
                priority: 1,
                stories: [
                    { name: "Create Profile", sequential_order: 1 },
                    { name: "Authenticate User", sequential_order: 2 }
                ]
            },
            {
                name: "Enhancement Release",
                priority: 2,
                stories: [
                    { name: "Add Payment Method", sequential_order: 1 }
                ]
            },
            {
                name: "Backlog",
                priority: 99,
                stories: []
            }
        ]
    }, null, 2));
    process.env.WORKING_AREA = tempWorkspaceDir;
}

setupTestWorkspace();

const { verifyTestWorkspace } = require('../../helpers/prevent_production_writes');
verifyTestWorkspace();

// Shared backend panel for panel edit tests (uses real CLI, no mock)
const backendPanel = new PanelView(productionBotPath);

/**
 * Create test panel that routes executeCommand to backendPanel.execute (real CLI)
 * Same pattern as test_edit_story_nodes.js
 */
function createTestBotPanel() {
    const executedCommands = [];
    const sentMessages = [];
    let messageHandler = null;

    const mockWebview = {
        postMessage: (msg) => { sentMessages.push(msg); },
        asWebviewUri: (uri) => uri,
        onDidReceiveMessage: (handler) => {
            messageHandler = handler;
            return { dispose: () => {} };
        }
    };

    const mockVscodePanel = {
        webview: mockWebview,
        onDidDispose: () => ({ dispose: () => {} }),
        reveal: () => {},
        visible: true
    };

    const handleMessage = async (message) => {
        if (message.command === 'executeCommand' && message.commandText) {
            executedCommands.push(message.commandText);
            try {
                const result = await backendPanel.execute(message.commandText);
                if (result && result.status === 'error') {
                    mockWebview.postMessage({ command: 'commandError', error: result.message || 'Command failed' });
                } else {
                    mockWebview.postMessage({ command: 'commandResult', data: { result } });
                }
            } catch (error) {
                mockWebview.postMessage({ command: 'commandError', error: error.message });
            }
        }
    };

    mockWebview.onDidReceiveMessage(handleMessage);

    return {
        panel: mockVscodePanel,
        executedCommands,
        sentMessages,
        postMessageFromWebview: async (message) => {
            if (messageHandler) await messageHandler(message);
        }
    };
}

async function queryStoryGraph(testPanel) {
    await new Promise(resolve => setTimeout(resolve, 50));
    const beforeLength = testPanel.sentMessages.length;
    await testPanel.postMessageFromWebview({ command: 'executeCommand', commandText: 'story_graph' });

    const statusMsg = testPanel.sentMessages.slice(beforeLength).find(m =>
        m.command === 'commandResult' || m.command === 'commandError'
    );
    if (!statusMsg) throw new Error('No response from story_graph query');
    if (statusMsg.command === 'commandError') return { epics: [], increments: [] };

    const result = statusMsg.data.result;
    let response = typeof result === 'string' ? JSON.parse(result) : result;
    const data = response.result || response;
    if (!data || typeof data !== 'object') return { epics: [], increments: [] };
    // Handle both top-level and content-wrapped structure
    const content = data.content || data;
    return { epics: content.epics || [], increments: content.increments || [] };
}

async function executeViaEventHandler(testPanel, commandText) {
    await testPanel.postMessageFromWebview({ command: 'executeCommand', commandText });
    const commandExecuted = testPanel.executedCommands.includes(commandText);
    const response = testPanel.sentMessages[testPanel.sentMessages.length - 1];
    const success = response && response.command === 'commandResult';
    return { success, response, commandExecuted };
}

function writeStoryGraphForPanelTest(graphData) {
    const storyGraphPath = path.join(tempWorkspaceDir, 'docs', 'story', 'story-graph.json');
    fs.writeFileSync(storyGraphPath, JSON.stringify(graphData, null, 2));
}

function givenStoryGraphWithIncrements() {
    return JSON.parse(fs.readFileSync(
        path.join(tempWorkspaceDir, 'docs', 'story', 'story-graph.json'), 'utf8'
    ));
}

function storyGraphWithIncrementAndStory(incrementName, storyName) {
    return {
        epics: [{
            name: 'Epic',
            sub_epics: [{
                name: 'SubEpic',
                story_groups: [{ stories: [{ name: storyName, sequential_order: 1 }] }]
            }]
        }],
        increments: [{ name: incrementName, priority: 1, stories: [] }]
    };
}

function storyGraphWithIncrementContainingStory(incrementName, storyName) {
    return {
        epics: [],
        increments: [{ name: incrementName, priority: 1, stories: [{ name: storyName, sequential_order: 1 }] }]
    };
}

function givenPanelInView(initialView) {
    const storyGraph = givenStoryGraphWithIncrements();
    const view = new IncrementView(storyGraph);
    view.currentView = initialView;
    return view;
}

function whenUserClicksViewToggle(view) {
    return view.toggleView();
}

function whenPanelRendersIncrementView(view) {
    return view.renderIncrementColumns();
}

function thenPanelSwitchesToView(result, expectedView) {
    assert.strictEqual(result.current_view, expectedView);
}

function thenToggleButtonShowsLabelAndTooltip(result, expectedLabel, expectedTooltip) {
    assert.strictEqual(result.toggle_label, expectedLabel);
    assert.strictEqual(result.tooltip, expectedTooltip);
}

function thenPanelShowsColumnForIncrement(rendered, incrementName) {
    const column = rendered.columns.find(c => c.name === incrementName);
    assert.ok(column, `Column '${incrementName}' should exist`);
    return column;
}

function thenStoriesDisplayInNaturalOrder(column, expectedStoryNames) {
    const actualNames = column.stories.map(s => s.name);
    assert.deepStrictEqual(actualNames, expectedStoryNames);
}

function thenViewIsReadOnly(column) {
    assert.strictEqual(column.read_only, true);
}

function thenColumnShowsEmptyStateMessage(column, expectedMessage) {
    assert.strictEqual(column.empty_message, expectedMessage);
}

function thenControlsAreNotVisible(rendered) {
    assert.strictEqual(rendered.controls_visible, false);
}


describe('TestDisplayIncrementScopeView', () => {

    describe('User toggles from Hierarchy view to Increment view', () => {

        test('Hierarchy to Increment toggle', () => {
            const view = givenPanelInView('Hierarchy');

            const result = whenUserClicksViewToggle(view);

            thenPanelSwitchesToView(result, 'Increment');
            thenToggleButtonShowsLabelAndTooltip(result, 'Hierarchy', 'Display Hierarchy view');
        });

        test('Increment to Hierarchy toggle', () => {
            const view = givenPanelInView('Increment');

            const result = whenUserClicksViewToggle(view);

            thenPanelSwitchesToView(result, 'Hierarchy');
            thenToggleButtonShowsLabelAndTooltip(result, 'Increment', 'Display Increment view');
        });
    });

    describe('Increment view displays stories in natural order per column', () => {

        test('MVP Release column displays stories in natural order', () => {
            const view = givenPanelInView('Increment');

            const rendered = whenPanelRendersIncrementView(view);

            const column = thenPanelShowsColumnForIncrement(rendered, 'MVP Release');
            thenStoriesDisplayInNaturalOrder(column, ['Create Profile', 'Authenticate User']);
            thenViewIsReadOnly(column);
        });

        test('Enhancement Release column displays stories in natural order', () => {
            const view = givenPanelInView('Increment');

            const rendered = whenPanelRendersIncrementView(view);

            const column = thenPanelShowsColumnForIncrement(rendered, 'Enhancement Release');
            thenStoriesDisplayInNaturalOrder(column, ['Add Payment Method']);
            thenViewIsReadOnly(column);
        });

        test('Each column has increment name at top', () => {
            const view = givenPanelInView('Increment');

            const rendered = whenPanelRendersIncrementView(view);

            thenPanelShowsColumnForIncrement(rendered, 'MVP Release');
            thenPanelShowsColumnForIncrement(rendered, 'Enhancement Release');
            thenPanelShowsColumnForIncrement(rendered, 'Backlog');
        });
    });

    describe('Increment view displays empty column for increment with no stories', () => {

        test('Empty increment shows no stories message', () => {
            const view = givenPanelInView('Increment');

            const rendered = whenPanelRendersIncrementView(view);

            const column = thenPanelShowsColumnForIncrement(rendered, 'Backlog');
            assert.strictEqual(column.stories.length, 0);
            thenColumnShowsEmptyStateMessage(column, '(no stories)');
        });
    });

    describe('Increment view is read-only with no edit controls', () => {

        test('Controls are not visible in increment view', () => {
            const view = givenPanelInView('Increment');

            const rendered = whenPanelRendersIncrementView(view);

            thenControlsAreNotVisible(rendered);
        });

        test('All columns are read-only', () => {
            const view = givenPanelInView('Increment');

            const rendered = whenPanelRendersIncrementView(view);

            for (const column of rendered.columns) {
                thenViewIsReadOnly(column);
            }
        });
    });
});


describe('TestAddIncrement', () => {

    describe('Panel Add button with selection inserts after selected and refreshes', () => {

        test('IncrementView in edit mode shows Add control when increment selected', () => {
            const storyGraph = givenStoryGraphWithIncrements();
            const view = new IncrementView(storyGraph, { editMode: true, initialView: 'Increment' });

            const rendered = whenPanelRendersIncrementView(view);

            assert.strictEqual(rendered.controls_visible, true);
            assert.strictEqual(rendered.columns.some(c => c.name === 'MVP Release'), true);
        });

        test('Increment columns in edit mode are not read-only', () => {
            const storyGraph = givenStoryGraphWithIncrements();
            const view = new IncrementView(storyGraph, { editMode: true, initialView: 'Increment' });

            const rendered = whenPanelRendersIncrementView(view);

            for (const column of rendered.columns) {
                assert.strictEqual(column.read_only, false);
            }
        });
    });
});


describe('TestRemoveIncrement', () => {

    describe('Panel Delete button prompts confirmation and refreshes list', () => {

        test('IncrementView in edit mode shows Delete control', () => {
            const storyGraph = givenStoryGraphWithIncrements();
            const view = new IncrementView(storyGraph, { editMode: true });

            const rendered = whenPanelRendersIncrementView(view);

            assert.strictEqual(rendered.controls_visible, true);
        });
    });
});


describe('TestRenameIncrement', () => {

    describe('Panel inline edit updates increment name on blur or Enter', () => {

        test('IncrementView in edit mode allows name updates', () => {
            const storyGraph = givenStoryGraphWithIncrements();
            const view = new IncrementView(storyGraph, { editMode: true });

            const rendered = whenPanelRendersIncrementView(view);

            assert.strictEqual(rendered.columns.length, 3);
            const mvpColumn = rendered.columns.find(c => c.name === 'MVP Release');
            assert.ok(mvpColumn);
            assert.strictEqual(mvpColumn.read_only, false);
        });
    });
});


describe('TestAddStoryToIncrement', () => {

    describe('Panel drag from unallocated onto increment row adds story and refreshes', () => {

        test('IncrementView shows unallocated stories area when edit mode', () => {
            const storyGraph = storyGraphWithIncrementAndStory('MVP', 'Validate Order');
            const view = new IncrementView(storyGraph, { editMode: true });

            const rendered = whenPanelRendersIncrementView(view);

            assert.strictEqual(rendered.controls_visible, true);
            const mvpColumn = rendered.columns.find(c => c.name === 'MVP');
            assert.ok(mvpColumn);
            assert.strictEqual(mvpColumn.stories.length, 0);
        });
    });
});


describe('TestRenameStoryInIncrement', () => {

    describe('Panel inline edit updates story name in hierarchy and increment view', () => {

        test('IncrementView in edit mode allows story name updates', () => {
            const storyGraph = storyGraphWithIncrementContainingStory('MVP', 'Validate Order');
            const view = new IncrementView(storyGraph, { editMode: true });

            const rendered = whenPanelRendersIncrementView(view);

            const mvpColumn = rendered.columns.find(c => c.name === 'MVP');
            assert.ok(mvpColumn);
            assert.strictEqual(mvpColumn.stories[0].name, 'Validate Order');
            assert.strictEqual(mvpColumn.read_only, false);
        });
    });
});


describe('TestRemoveStoryFromIncrement', () => {

    describe('Panel Remove button moves story to unallocated area', () => {

        test('IncrementView in edit mode shows stories with Remove option', () => {
            const storyGraph = storyGraphWithIncrementContainingStory('MVP', 'Validate Order');
            const view = new IncrementView(storyGraph, { editMode: true });

            const rendered = whenPanelRendersIncrementView(view);

            const mvpColumn = rendered.columns.find(c => c.name === 'MVP');
            assert.ok(mvpColumn);
            assert.strictEqual(mvpColumn.stories.length, 1);
            assert.strictEqual(mvpColumn.stories[0].name, 'Validate Order');
            assert.strictEqual(mvpColumn.read_only, false);
        });
    });
});


// ============================================================================
// Panel Edit Increment Tests (real CLI via PanelView - no mock)
// Maps to: test_panel_* in story-graph.json
// ============================================================================

function getIncrementNames(data) {
    return data.increments.map(i => i.name);
}

function getStoriesInIncrement(data, incrementName) {
    const inc = data.increments.find(i => i.name === incrementName);
    return inc.stories.map(s => (typeof s === 'string' ? s : s.name));
}

function findStoryInHierarchy(data, storyName) {
    function searchStories(stories) {
        return stories.some(s => ((s && typeof s === 'object') ? s.name : s) === storyName);
    }
    function searchNode(node) {
        for (const sg of node.story_groups || []) {
            if (searchStories(sg.stories || [])) return true;
        }
        for (const child of node.sub_epics || []) {
            if (searchNode(child)) return true;
        }
        return false;
    }
    return (data.epics || []).some(searchNode);
}

test('TestPanelEditIncrements', { concurrency: false }, async (t) => {

    await t.test('test_panel_add_increment_after_selected', async () => {
        writeStoryGraphForPanelTest({
            epics: [],
            increments: [{ name: 'MVP', priority: 1, stories: [] }, { name: 'Phase 2', priority: 2, stories: [] }]
        });
        const testPanel = createTestBotPanel();

        const result = await executeViaEventHandler(testPanel, 'story_graph.add_increment name:"Phase 1.5" after:"MVP"');
        assert.ok(result.commandExecuted, 'Command should be executed via message handler');
        assert.ok(result.success, 'Command should succeed');

        const data = await queryStoryGraph(testPanel);
        const names = getIncrementNames(data);
        assert.ok(names.includes('Phase 1.5'), 'Phase 1.5 should exist');
        assert.deepStrictEqual(names, ['MVP', 'Phase 1.5', 'Phase 2']);
    });

    await t.test('test_panel_remove_increment_delete_button', async () => {
        writeStoryGraphForPanelTest({
            epics: [],
            increments: [{ name: 'MVP', priority: 1, stories: [] }]
        });
        const testPanel = createTestBotPanel();

        const result = await executeViaEventHandler(testPanel, 'story_graph.remove_increment increment_name:"MVP"');
        assert.ok(result.commandExecuted, 'Command should be executed via message handler');
        assert.ok(result.success, 'Command should succeed');

        const data = await queryStoryGraph(testPanel);
        const names = getIncrementNames(data);
        assert.ok(!names.includes('MVP'), 'MVP should be removed');
    });

    await t.test('test_panel_rename_increment_inline_edit', async () => {
        writeStoryGraphForPanelTest({
            epics: [],
            increments: [{ name: 'MVP', priority: 1, stories: [] }]
        });
        const testPanel = createTestBotPanel();

        const result = await executeViaEventHandler(testPanel, 'story_graph.rename_increment from_name:"MVP" to_name:"Phase 1"');
        assert.ok(result.commandExecuted, 'Command should be executed via message handler');
        assert.ok(result.success, 'Command should succeed');

        const data = await queryStoryGraph(testPanel);
        const names = getIncrementNames(data);
        assert.ok(!names.includes('MVP'), 'MVP should be renamed');
        assert.ok(names.includes('Phase 1'), 'Phase 1 should exist');
    });

    await t.test('test_panel_drag_story_to_increment', async () => {
        writeStoryGraphForPanelTest({
            epics: [{
                name: 'Epic',
                sequential_order: 1,
                sub_epics: [{
                    name: 'SubEpic',
                    sequential_order: 1,
                    sub_epics: [],
                    story_groups: [{
                        type: 'and',
                        connector: null,
                        stories: [
                            { name: 'Create Profile', sequential_order: 1.0, connector: null },
                            { name: 'Validate Order', sequential_order: 2.0, connector: null }
                        ]
                    }]
                }],
                story_groups: []
            }],
            increments: [{ name: 'MVP', priority: 1, stories: [] }]
        });
        const testPanel = createTestBotPanel();

        const result = await executeViaEventHandler(testPanel, 'story_graph.add_story_to_increment increment_name:"MVP" story_name:"Validate Order"');
        assert.ok(result.commandExecuted, 'Command should be executed via message handler');
        assert.ok(result.success, 'Command should succeed');

        const data = await queryStoryGraph(testPanel);
        const stories = getStoriesInIncrement(data, 'MVP');
        assert.ok(stories.includes('Validate Order'), 'Validate Order should be in MVP');
    });

    await t.test('test_panel_remove_story_from_increment', async () => {
        writeStoryGraphForPanelTest({
            epics: [{
                name: 'Epic',
                sequential_order: 1,
                sub_epics: [{
                    name: 'SubEpic',
                    sequential_order: 1,
                    sub_epics: [],
                    story_groups: [{
                        type: 'and',
                        connector: null,
                        stories: [{ name: 'Validate Order', sequential_order: 1.0, connector: null }]
                    }]
                }],
                story_groups: []
            }],
            increments: [{ name: 'MVP', priority: 1, stories: [{ name: 'Validate Order', sequential_order: 1.0 }] }]
        });
        const testPanel = createTestBotPanel();

        const result = await executeViaEventHandler(testPanel, 'story_graph.remove_story_from_increment increment_name:"MVP" story_name:"Validate Order"');
        assert.ok(result.commandExecuted, 'Command should be executed via message handler');
        assert.ok(result.success, 'Command should succeed');

        const data = await queryStoryGraph(testPanel);
        const stories = getStoriesInIncrement(data, 'MVP');
        assert.ok(!stories.includes('Validate Order'), 'Validate Order should be removed from MVP');
    });

    await t.test('test_panel_rename_story_updates_both_views', async () => {
        writeStoryGraphForPanelTest({
            epics: [{
                name: 'Epic',
                sequential_order: 1,
                sub_epics: [{
                    name: 'SubEpic',
                    sequential_order: 1,
                    sub_epics: [],
                    story_groups: [{
                        type: 'and',
                        connector: null,
                        stories: [{ name: 'Validate Order', sequential_order: 1.0, connector: null }]
                    }]
                }],
                story_groups: []
            }],
            increments: [{ name: 'MVP', priority: 1, stories: [{ name: 'Validate Order', sequential_order: 1.0 }] }]
        });
        const testPanel = createTestBotPanel();

        const result = await executeViaEventHandler(testPanel, 'story_graph.rename_story_in_hierarchy old_name:"Validate Order" new_name:"Validate Order Items"');
        assert.ok(result.commandExecuted, 'Command should be executed via message handler');
        assert.ok(result.success, 'Command should succeed');

        const data = await queryStoryGraph(testPanel);
        const inHierarchy = findStoryInHierarchy(data, 'Validate Order Items');
        const stories = getStoriesInIncrement(data, 'MVP');
        assert.ok(inHierarchy, 'Renamed story should exist in hierarchy');
        assert.ok(!findStoryInHierarchy(data, 'Validate Order'), 'Old name should not exist');
        assert.ok(stories.includes('Validate Order Items'), `Increment should reference renamed story. MVP stories: ${JSON.stringify(stories)}`);
    });
});

after(() => {
    backendPanel.cleanup();
    try {
        fs.rmSync(tempWorkspaceDir, { recursive: true, force: true });
    } catch (err) {
        console.warn('Failed to clean up temp workspace:', err.message);
    }
    delete process.env.WORKING_AREA;
});
