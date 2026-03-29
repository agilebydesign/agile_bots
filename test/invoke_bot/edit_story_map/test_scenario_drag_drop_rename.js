/**
 * Test Scenario Drag-and-Drop and Rename
 * 
 * Validates that scenarios in the story map panel have:
 * - draggable="true" attribute
 * - story-node class for event handling
 * - data-node-type="scenario" attribute
 * - data-path attribute for command execution
 * - data-position attribute for reordering
 * 
 * This test ensures scenarios have the same drag-and-drop and rename
 * functionality as other node types (Epic, SubEpic, Story).
 * 
 * Story: Display Story Hierarchy Panel
 * Sub-Epic: Manage Story Graph Through Panel
 */

const { test, before, after } = require('node:test');
const assert = require('assert');
const path = require('path');
const os = require('os');
const fs = require('fs');

// Mock vscode before requiring any modules
const Module = require('module');
const originalRequire = Module.prototype.require;
Module.prototype.require = function(...args) {
    if (args[0] === 'vscode') {
        return require('../../helpers/mock_vscode');
    }
    return originalRequire.apply(this, args);
};

const StoryMapView = require('../../../src/panel/story_graph/story_map_view');
const { parseHTML } = require('../../helpers/html_assertions');

// Setup test workspace
const tempWorkspaceDir = fs.mkdtempSync(path.join(os.tmpdir(), 'agile-bots-scenario-test-'));
const repoRoot = path.join(__dirname, '../../..');

function setupTestWorkspace() {
    fs.mkdirSync(path.join(tempWorkspaceDir, 'docs', 'stories', 'map'), { recursive: true });
    
    // Create test story graph with Epic > SubEpic > StoryGroup > Story > Scenarios
    const storyGraphPath = path.join(tempWorkspaceDir, 'docs', 'stories', 'story-graph.json');
    const testStoryGraph = {
        epics: [
            {
                name: 'User Management',
                sequential_order: 0,
                sub_epics: [
                    {
                        name: 'Authentication',
                        sequential_order: 0,
                        story_groups: [
                            {
                                name: 'Login',
                                stories: [
                                    {
                                        name: 'Login Form',
                                        sequential_order: 0,
                                        acceptance_criteria: [
                                            {
                                                text: 'User can enter a username and password',
                                                sequential_order: 0
                                            },
                                            {
                                                text: 'Authentication errors are shown inline',
                                                sequential_order: 1
                                            }
                                        ],
                                        scenarios: [
                                            {
                                                name: 'Valid Login',
                                                sequential_order: 0,
                                                type: 'happy_path',
                                                background: [],
                                                steps: 'Given I am on login page\nWhen I enter valid credentials\nThen I am logged in'
                                            },
                                            {
                                                name: 'Invalid Password',
                                                sequential_order: 1,
                                                type: 'error',
                                                background: [],
                                                steps: 'Given I am on login page\nWhen I enter invalid password\nThen I see error message'
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    };
    fs.writeFileSync(storyGraphPath, JSON.stringify(testStoryGraph, null, 2));
    
    process.env.WORKING_AREA = tempWorkspaceDir;
    
    // Verify WORKING_AREA is set to temp directory
    const { verifyTestWorkspace } = require('../../helpers/prevent_production_writes');
    verifyTestWorkspace();
}

// Cleanup
after(() => {
    if (fs.existsSync(tempWorkspaceDir)) {
        fs.rmSync(tempWorkspaceDir, { recursive: true, force: true });
    }
});

test('Scenario nodes have draggable and story-node attributes', async () => {
    setupTestWorkspace();
    
    const storyMapView = new StoryMapView(repoRoot);
    
    // Load story graph
    const storyGraphPath = path.join(tempWorkspaceDir, 'docs', 'stories', 'story-graph.json');
    const storyGraphData = JSON.parse(fs.readFileSync(storyGraphPath, 'utf8'));
    
    // Generate HTML (pass null for icon paths)
    const html = storyMapView.renderStoryTree(storyGraphData.epics, null, null, null, null, null, null, null);
    
    // Parse HTML
    const doc = parseHTML(html);
    
    // Find all scenario nodes
    const scenarioNodes = Array.from(doc.querySelectorAll('[data-node-type="scenario"]'));
    
    // Should have 2 scenarios
    assert.strictEqual(scenarioNodes.length, 2, 'Should have 2 scenario nodes');
    
    // Check first scenario
    const validLoginNode = scenarioNodes[0];
    assert.ok(validLoginNode.textContent.includes('Valid Login'), 'First scenario should be "Valid Login"');
    assert.ok(validLoginNode.classList.contains('story-node'), 'Scenario should have story-node class');
    assert.strictEqual(validLoginNode.getAttribute('draggable'), 'true', 'Scenario should be draggable');
    assert.strictEqual(validLoginNode.getAttribute('data-node-type'), 'scenario', 'Should have data-node-type="scenario"');
    assert.strictEqual(validLoginNode.getAttribute('data-node-name'), 'Valid Login', 'Should have correct data-node-name');
    assert.strictEqual(validLoginNode.getAttribute('data-position'), '0', 'Should have data-position="0"');
    assert.ok(validLoginNode.getAttribute('data-path'), 'Should have data-path attribute');
    assert.ok(validLoginNode.getAttribute('data-path').includes('Valid Login'), 'data-path should include scenario name');
    
    // Check second scenario
    const invalidPasswordNode = scenarioNodes[1];
    assert.ok(invalidPasswordNode.textContent.includes('Invalid Password'), 'Second scenario should be "Invalid Password"');
    assert.ok(invalidPasswordNode.classList.contains('story-node'), 'Scenario should have story-node class');
    assert.strictEqual(invalidPasswordNode.getAttribute('draggable'), 'true', 'Scenario should be draggable');
    assert.strictEqual(invalidPasswordNode.getAttribute('data-node-type'), 'scenario', 'Should have data-node-type="scenario"');
    assert.strictEqual(invalidPasswordNode.getAttribute('data-node-name'), 'Invalid Password', 'Should have correct data-node-name');
    assert.strictEqual(invalidPasswordNode.getAttribute('data-position'), '1', 'Should have data-position="1"');
    assert.ok(invalidPasswordNode.getAttribute('data-path'), 'Should have data-path attribute');
    assert.ok(invalidPasswordNode.getAttribute('data-path').includes('Invalid Password'), 'data-path should include scenario name');
});

test('Story renders separate acceptance criteria and scenarios branches', async () => {
    setupTestWorkspace();
    
    const storyMapView = new StoryMapView(repoRoot);
    
    const storyGraphPath = path.join(tempWorkspaceDir, 'docs', 'stories', 'story-graph.json');
    const storyGraphData = JSON.parse(fs.readFileSync(storyGraphPath, 'utf8'));
    
    const html = storyMapView.renderStoryTree(storyGraphData.epics, null, null, null, null, null, null, null);
    const doc = parseHTML(html);
    
    const acceptanceCriteriaBranch = doc.querySelector('[data-node-type="acceptance-criteria-group"]');
    const scenariosBranch = doc.querySelector('[data-node-type="scenarios-group"]');
    const acceptanceCriteriaNodes = Array.from(doc.querySelectorAll('[data-node-type="acceptance-criteria"]'));
    
    assert.ok(acceptanceCriteriaBranch, 'Story should render an Acceptance Criteria branch');
    assert.ok(acceptanceCriteriaBranch.textContent.includes('Acceptance Criteria'), 'Acceptance Criteria branch should be labeled');
    assert.ok(scenariosBranch, 'Story should render a Scenarios branch');
    assert.ok(scenariosBranch.textContent.includes('Scenarios'), 'Scenarios branch should be labeled');
    assert.strictEqual(acceptanceCriteriaNodes.length, 2, 'Story should render both acceptance criteria entries');
    assert.ok(acceptanceCriteriaNodes[0].textContent.includes('User can enter a username and password'));
    assert.ok(acceptanceCriteriaNodes[1].textContent.includes('Authentication errors are shown inline'));
});

test('Scenario nodes render nested step rows', async () => {
    setupTestWorkspace();
    
    const storyMapView = new StoryMapView(repoRoot);
    
    const storyGraphPath = path.join(tempWorkspaceDir, 'docs', 'stories', 'story-graph.json');
    const storyGraphData = JSON.parse(fs.readFileSync(storyGraphPath, 'utf8'));
    
    const html = storyMapView.renderStoryTree(storyGraphData.epics, null, null, null, null, null, null, null);
    const doc = parseHTML(html);
    
    const stepNodes = Array.from(doc.querySelectorAll('[data-node-type="step"]'));
    
    assert.strictEqual(stepNodes.length, 6, 'Each scenario should render all of its steps as nested step rows');
    assert.ok(stepNodes.some(node => node.textContent.includes('Given I am on login page')), 'Rendered steps should include the first Given step');
    assert.ok(stepNodes.some(node => node.textContent.includes('Then I see error message')), 'Rendered steps should include the final Then step');
});

test('Shared scenario background renders once at scenarios level', async () => {
    setupTestWorkspace();
    
    const storyMapView = new StoryMapView(repoRoot);
    
    const storyGraphPath = path.join(tempWorkspaceDir, 'docs', 'stories', 'story-graph.json');
    const storyGraphData = JSON.parse(fs.readFileSync(storyGraphPath, 'utf8'));

    const sharedBackground = ['Given I am on the login page'];
    storyGraphData.epics[0].sub_epics[0].story_groups[0].stories[0].scenarios.forEach((scenario) => {
        scenario.background = sharedBackground;
    });
    
    const html = storyMapView.renderStoryTree(storyGraphData.epics, null, null, null, null, null, null, null);
    const doc = parseHTML(html);

    const backgroundGroup = doc.querySelector('[data-node-type="background-group"]');
    const backgroundSteps = Array.from(doc.querySelectorAll('[data-node-type="background-step"]'));
    const stepNodes = Array.from(doc.querySelectorAll('[data-node-type="step"]'));

    assert.ok(backgroundGroup, 'Shared scenario background should render at the scenarios branch level');
    assert.ok(backgroundGroup.classList.contains('story-node'), 'Background group should be selectable like other tree nodes');
    assert.ok(backgroundGroup.textContent.includes('Background'), 'Background group should be labeled');
    assert.strictEqual(backgroundGroup.getAttribute('data-node-name'), 'Background', 'Background group should expose a stable node name');
    assert.strictEqual(backgroundGroup.getAttribute('data-has-children'), 'true', 'Background group should present as expandable/selectable');
    assert.strictEqual(backgroundGroup.getAttribute('draggable'), null, 'Background group should not be draggable');
    assert.strictEqual(backgroundSteps.length, 1, 'Shared background should render only once');
    assert.ok(backgroundSteps[0].textContent.includes('Given I am on the login page'));
    assert.strictEqual(
        stepNodes.filter(node => node.textContent.includes('Background: Given I am on the login page')).length,
        0,
        'Shared background should not be repeated inside each scenario'
    );
});

test('Scenario data-path has correct format for CLI commands', async () => {
    setupTestWorkspace();
    
    const storyMapView = new StoryMapView(repoRoot);
    
    // Load story graph
    const storyGraphPath = path.join(tempWorkspaceDir, 'docs', 'stories', 'story-graph.json');
    const storyGraphData = JSON.parse(fs.readFileSync(storyGraphPath, 'utf8'));
    
    // Generate HTML (pass null for icon paths)
    const html = storyMapView.renderStoryTree(storyGraphData.epics, null, null, null, null, null, null, null);
    
    // Parse HTML
    const doc = parseHTML(html);
    
    // Find scenario node
    const scenarioNode = doc.querySelector('[data-node-name="Valid Login"]');
    const dataPath = scenarioNode.getAttribute('data-path');
    
    // Should have format: story_graph."Epic"."SubEpic"."Story"."Scenario"
    // Note: parseHTML unescapes HTML entities, so &quot; becomes "
    assert.ok(dataPath.startsWith('story_graph.'), 'data-path should start with story_graph.');
    assert.ok(dataPath.includes('"User Management"'), 'data-path should include Epic name');
    assert.ok(dataPath.includes('"Authentication"'), 'data-path should include SubEpic name');
    assert.ok(dataPath.includes('"Login Form"'), 'data-path should include Story name');
    assert.ok(dataPath.includes('"Valid Login"'), 'data-path should include Scenario name');
    
    // Expected format (HTML parser unescapes entities)
    const expectedPath = 'story_graph."User Management"."Authentication"."Login Form"."Valid Login"';
    assert.strictEqual(dataPath, expectedPath, 'data-path should match expected format');
});

test('Scenarios with file links have data-file-link attribute', async () => {
    setupTestWorkspace();
    
    const storyMapView = new StoryMapView(repoRoot);
    
    // Create story file link
    const storyFilePath = path.join(tempWorkspaceDir, 'docs', 'stories', 'map', 'Login Form.md');
    fs.writeFileSync(storyFilePath, '# Login Form\n\n## Valid Login\n\nTest scenario content');
    
    // Load story graph with links
    const storyGraphPath = path.join(tempWorkspaceDir, 'docs', 'stories', 'story-graph.json');
    const storyGraphData = JSON.parse(fs.readFileSync(storyGraphPath, 'utf8'));
    
    // Add story link to story
    storyGraphData.epics[0].sub_epics[0].story_groups[0].stories[0].links = [
        {
            type: 'doc',
            label: 'Story',
            text: 'story',  // This is what the code looks for
            url: storyFilePath,
            icon: 'document'
        }
    ];
    
    // Generate HTML (pass null for icon paths)
    const html = storyMapView.renderStoryTree(storyGraphData.epics, null, null, null, null, null, null, null);
    
    // Parse HTML
    const doc = parseHTML(html);
    
    // Find scenario node
    const scenarioNode = doc.querySelector('[data-node-name="Valid Login"]');
    
    // Should have data-file-link attribute
    assert.ok(scenarioNode.getAttribute('data-file-link'), 'Scenario with story link should have data-file-link attribute');
    
    // data-file-link should include scenario anchor
    const fileLink = scenarioNode.getAttribute('data-file-link');
    assert.ok(fileLink.includes('#'), 'data-file-link should include anchor');
    assert.ok(fileLink.includes('valid-login'), 'data-file-link should include scenario anchor (lowercase with hyphens)');
});
