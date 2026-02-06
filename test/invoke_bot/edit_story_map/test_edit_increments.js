const Module = require('module');
const originalRequire = Module.prototype.require;
Module.prototype.require = function(...args) {
    if (args[0] === 'vscode') {
        return require('../../helpers/mock_vscode');
    }
    return originalRequire.apply(this, args);
};

const { test, describe } = require('node:test');
const assert = require('assert');
const path = require('path');
const os = require('os');
const fs = require('fs');

const repoRoot = path.join(__dirname, '../../..');
const productionBotPath = path.join(repoRoot, 'bots', 'story_bot');
const tempWorkspaceDir = fs.mkdtempSync(path.join(os.tmpdir(), 'agile-bots-increment-test-'));

const IncrementView = require('../../../src/panel/increment_view');


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


function givenStoryGraphWithIncrements() {
    return JSON.parse(fs.readFileSync(
        path.join(tempWorkspaceDir, 'docs', 'story', 'story-graph.json'), 'utf8'
    ));
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
