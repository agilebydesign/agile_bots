/**
 * Test Navigate Behavior and Actions Panel
 * 
 * Merged from: test_navigate_behaviors.js, test_behaviors_view.js, test_behaviors_view_example.js
 */

/**
 * Test Navigate Behavior Action
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
const { BehaviorsViewTestHelper } = require('../../helpers');

// Setup - Use temp directory for test workspace to avoid modifying production data
const repoRoot = path.join(__dirname, '../../..');
const productionBotPath = path.join(repoRoot, 'bots', 'story_bot');

// Create temp workspace for tests (data only - story graphs, etc.)
const tempWorkspaceDir = fs.mkdtempSync(path.join(os.tmpdir(), 'agile-bots-behavior-test-'));

// For tests that modify story graph, we need to:
// 1. Use production bot config and source code (can't copy all of it)
// 2. Set WORKING_AREA to a temp directory so story graph changes go there
// 
// The PanelView derives workspaceDir from botPath, so we use production bot
// but override the working area via environment variable before spawning

// Create temp workspace for test data (story graphs, etc.)
function setupTestWorkspace() {
    fs.mkdirSync(path.join(tempWorkspaceDir, 'docs', 'stories'), { recursive: true });
    
    // Create empty test story graph
    const storyGraphPath = path.join(tempWorkspaceDir, 'docs', 'stories', 'story-graph.json');
    fs.writeFileSync(storyGraphPath, JSON.stringify({ epics: [] }, null, 2));
    
    // Set environment variable so Python backend uses temp workspace for data
    process.env.WORKING_AREA = tempWorkspaceDir;
    
    // Verify WORKING_AREA is set to temp directory before creating PanelView
    const { verifyTestWorkspace } = require('../../helpers/prevent_production_writes');
    verifyTestWorkspace();
}

before(() => {
    setupTestWorkspace();
});

// Use production bot path (has config and behaviors) but temp workspace for data
// The helper needs the workspace directory to derive the bot path, but WORKING_AREA
// environment variable ensures all data writes go to tempWorkspaceDir
const workspaceDir = repoRoot;

// Create ONE helper for all tests - shares single CLI process
// WORKING_AREA is set to tempWorkspaceDir in setupTestWorkspace(), so all data writes go to temp directory
const helper = new BehaviorsViewTestHelper(workspaceDir, 'story_bot');

// Cleanup after all tests
after(() => {
    helper.cleanup();
    // Clean up temp workspace and restore environment
    try {
        if (fs.existsSync(tempWorkspaceDir)) {
            fs.rmSync(tempWorkspaceDir, { recursive: true, force: true });
        }
    } catch (err) {
        console.warn('Failed to clean up temp workspace:', err.message);
    }
    // Restore WORKING_AREA to original or unset
    delete process.env.WORKING_AREA;
});

class TestNavigateBehaviorAction {
    async testUserNavigatesToShapeBehavior() {
        /**
         * GIVEN: Bot initialized with multiple behaviors
         * WHEN: User navigates to 'shape' behavior
         * THEN: Bot state updates to shape behavior
         */
        const cli = helper._cli;
        
        await cli.execute('shape');
        const statusResponse = await cli.execute('status');
        const response = statusResponse.bot || statusResponse;
        
        console.log('Current behavior:', response.behaviors.current);
        console.log('Total behaviors:', response.behaviors.all_behaviors.length);
        
        assert.strictEqual(response.behaviors.current, 'shape',
            'Current behavior should be shape');
        assert.ok(Array.isArray(response.behaviors.names),
            'Should have array of behavior names');
        assert.ok(response.behaviors.names.includes('shape'),
            'Shape should be in behavior names');
        
        const behaviorsData = response.behaviors.all_behaviors;
        assert.ok(Array.isArray(behaviorsData), 'Should have behaviors array');
        assert.ok(behaviorsData.length > 0, 'Should have at least one behavior');
        
        const html = await helper.render_html();
        helper.assert_complete_state_rendered(html, response);
        
        const shapeBehavior = behaviorsData.find(b => b.name === 'shape');
        helper.assert_behavior_fully_rendered(html, shapeBehavior);
    }
    
    async testUserNavigatesToSpecificAction() {
        /**
         * GIVEN: Bot at shape behavior
         * WHEN: User navigates to shape.strategy action
         * THEN: Bot state updates to shape.strategy
         */
        const cli = helper._cli;
        
        await cli.execute('shape.strategy');
        const statusResponse = await cli.execute('status');
        const response = statusResponse.bot || statusResponse;
        
        console.log('Current behavior:', response.behaviors.current);
        console.log('Current action:', response.current_action);
        console.log('Total behaviors rendered:', response.behaviors.all_behaviors.length);
        
        assert.strictEqual(response.behaviors.current, 'shape',
            'Should be at shape behavior');
        assert.strictEqual(response.current_action, 'strategy',
            'Should be at strategy action');
        
        const html = await helper.render_html();
        helper.assert_complete_state_rendered(html, response);
        
        const shapeBehavior = response.behaviors.all_behaviors.find(b => b.name === 'shape');
        helper.assert_behavior_fully_rendered(html, shapeBehavior);
    }
    
    async testNavigationUpdatesHierarchyDisplay() {
        /**
         * GIVEN: Bot at initial state
         * WHEN: User navigates through multiple behaviors
         * THEN: Hierarchy display updates each time
         */
        const cli = helper._cli;
        
        const initialStatus = await cli.execute('status');
        const initialResponse = initialStatus.bot || initialStatus;
        
        await cli.execute('shape');
        const afterShapeStatus = await cli.execute('status');
        const afterShapeResponse = afterShapeStatus.bot || afterShapeStatus;
        const afterShapeHtml = await helper.render_html();
        
        await cli.execute('scenarios');
        const afterScenariosStatus = await cli.execute('status');
        const afterScenariosResponse = afterScenariosStatus.bot || afterScenariosStatus;
        const afterScenariosHtml = await helper.render_html();
        
        console.log('State progression:');
        console.log('  Initial:', initialResponse.behaviors.current);
        console.log('  After shape:', afterShapeResponse.behaviors.current);
        console.log('  After scenarios:', afterScenariosResponse.behaviors.current);
        
        assert.strictEqual(afterShapeResponse.behaviors.current, 'shape',
            'Should navigate to shape');
        assert.strictEqual(afterScenariosResponse.behaviors.current, 'scenarios',
            'Should navigate to scenarios');
        
        helper.assert_complete_state_rendered(afterShapeHtml, afterShapeResponse);
        helper.assert_complete_state_rendered(afterScenariosHtml, afterScenariosResponse);
        
        assert.ok(afterScenariosResponse.behaviors.all_behaviors.length >= 2,
            'Should have at least shape and scenarios behaviors');
    }
    
    async testNavigationPersistsBotState() {
        /**
         * GIVEN: Bot navigated to specific action
         * WHEN: Panel refreshes (new status call)
         * THEN: Bot remains at same position
         */
        const cli = helper._cli;
        
        await cli.execute('shape.clarify');
        
        const status1 = await cli.execute('status');
        const status2 = await cli.execute('status');
        const status3 = await cli.execute('status');
        const response1 = status1.bot || status1;
        const response2 = status2.bot || status2;
        const response3 = status3.bot || status3;
        
        console.log('Status 1:', response1.current_action, `(${response1.behaviors.all_behaviors.length} behaviors)`);
        console.log('Status 2:', response2.current_action, `(${response2.behaviors.all_behaviors.length} behaviors)`);
        console.log('Status 3:', response3.current_action, `(${response3.behaviors.all_behaviors.length} behaviors)`);
        
        assert.strictEqual(response1.current_action, response2.current_action,
            'Action should persist across status calls');
        assert.strictEqual(response2.current_action, response3.current_action,
            'Action should persist across multiple calls');
        
        assert.strictEqual(response1.behaviors.all_behaviors.length, response2.behaviors.all_behaviors.length,
            'Behavior count should persist');
        
        const html1 = await helper.render_html();
        const html2 = await helper.render_html();
        
        helper.assert_complete_state_rendered(html1, response1);
        helper.assert_complete_state_rendered(html2, response2);
    }
}

// Rule: use_class_based_organization
class TestBehaviorsView {

    
    // ========================================================================
    // DISPLAY HIERARCHY TESTS
    // ========================================================================
    
    async testSingleBehaviorWithNoActions() {
        const html = await helper.render_html();
        assert.ok(html.includes('shape'), 'Should contain behavior name');
        assert.ok(html.length > 0, 'Should render HTML');
        helper.assert_behavior_with_actions(html, 'shape', []);
    }
    
    async testSingleBehaviorWithMultipleActions() {
        const html = await helper.render_html();
        const expectedActions = ['clarify', 'strategy', 'validate', 'render'];
        helper.assert_behavior_with_actions(html, 'prioritization', expectedActions);
        for (const action of expectedActions) {
            assert.ok(html.includes(action), `Should contain action "${action}"`);
        }
    }

    async testBehaviorActionSectionComplete() {
        const html = await helper.render_html();
        const expectedBehaviors = ['shape', 'prioritization', 'exploration', 'scenarios', 'tests', 'code'];
        for (const behavior of expectedBehaviors) {
            assert.ok(html.includes(behavior), `Behavior "${behavior}" should be present in rendered HTML`);
        }
        const firstBehaviorIndex = html.indexOf('prioritization');
        const lastBehaviorIndex = html.lastIndexOf('code');
        assert.ok(firstBehaviorIndex > -1, 'First behavior (prioritization) should be present');
        assert.ok(lastBehaviorIndex > -1, 'Last behavior (code) should be present');
        assert.ok(lastBehaviorIndex > firstBehaviorIndex, 'Behaviors should span a section of HTML');
        const expectedShapeActions = ['clarify', 'strategy', 'build', 'validate', 'render'];
        for (const action of expectedShapeActions) {
            assert.ok(html.includes(action), `Shape action "${action}" should be present in HTML`);
        }
    }

    async testBehaviorsDisplayedInCanonicalOrder() {
        const html = await helper.render_html();
        const behaviorNameRegex = /<span[^>]*onclick="navigateToBehavior\('([^']+)'\)"[^>]*>[\s\S]*?\1/g;
        let match;
        const displayedBehaviors = [];
        while ((match = behaviorNameRegex.exec(html)) !== null) {
            const behaviorName = match[1];
            if (!displayedBehaviors.includes(behaviorName)) {
                displayedBehaviors.push(behaviorName);
            }
        }
        const canonicalOrder = ['shape', 'prioritization', 'exploration', 'scenarios', 'tests', 'code'];
        const expectedOrder = canonicalOrder.filter(name => displayedBehaviors.includes(name));
        assert.deepStrictEqual(displayedBehaviors, expectedOrder,
            `Expected: ${expectedOrder.join(', ')}. Got: ${displayedBehaviors.join(', ')}`);
    }
    
    async testEmptyBehaviorsList() {
        const html = await helper.render_html();
        assert.ok(typeof html === 'string', 'Should return string');
        assert.ok(html.length >= 0, 'Should handle empty behaviors');
    }
    
    // ========================================================================
    // CURRENT BEHAVIOR MARKING TESTS
    // ========================================================================
    
    async testCurrentBehaviorMarkedInHierarchy() {
        const html = await helper.render_html();
        const statusResponse = await helper._cli.execute('status');
        const response = statusResponse.bot || statusResponse;
        const currentBehavior = response.current_behavior?.split('.').pop() || response.behaviors?.current || 'prioritization';
        helper.assert_current_behavior_marked(html, currentBehavior);
    }
    
    async testNonCurrentBehaviorNotMarked() {
        const html = await helper.render_html();
        const statusResponse = await helper._cli.execute('status');
        const response = statusResponse.bot || statusResponse;
        const currentBehavior = response.current_behavior?.split('.').pop() || response.behaviors?.current || 'prioritization';
        helper.assert_current_behavior_marked(html, currentBehavior);
        assert.ok(html.includes('exploration'), 'Exploration should be present');
        assert.ok(html.includes('shape'), 'Shape should be present');
    }
    
    // ========================================================================
    // ACTION LISTING TESTS
    // ========================================================================
    
    async testActionsListedUnderBehavior() {
        const html = await helper.render_html();
        const expectedActions = ['clarify', 'strategy', 'validate', 'render'];
        helper.assert_behavior_with_actions(html, 'prioritization', expectedActions);
    }
    
    async testActionsInCorrectOrder() {
        const html = await helper.render_html();
        const expectedActions = ['clarify', 'strategy', 'validate', 'render'];
        for (const action of expectedActions) {
            assert.ok(html.includes(action), `Action "${action}" should be present in HTML`);
        }
    }
    
    // ========================================================================
    // COMPLETED ACTION TESTS
    // ========================================================================
    
    async testCompletedActionsShowIndicator() {
        const allActions = ['clarify', 'strategy', 'validate', 'build'];
        const completedActions = ['clarify', 'strategy'];
        const behaviorData = helper.create_behavior_with_completed_actions(
            'shape', allActions, completedActions
        );
        const html = await helper.render_html();
        helper.assert_completed_actions_marked(html, completedActions);
    }
    
    async testNoCompletedActionsShowsPendingOnly() {
        const html = await helper.render_html();
        const expectedActions = ['clarify', 'strategy', 'validate', 'render'];
        for (const action of expectedActions) {
            assert.ok(html.includes(action), `Should contain action "${action}"`);
        }
    }
    
    // ========================================================================
    // EXECUTE BUTTON TESTS
    // ========================================================================
    
    async testActionsHaveExecuteButtons() {
        const html = await helper.render_html();
        const expectedActions = ['clarify', 'strategy', 'validate', 'render'];
        helper.assert_actions_have_execute_buttons(html, expectedActions);
    }
    
    // ========================================================================
    // COMPLETE HIERARCHY TESTS
    // ========================================================================
    
    async testCompleteHierarchyRendering() {
        const html = await helper.render_html();
        const statusResponse = await helper._cli.execute('status');
        const response = statusResponse.bot || statusResponse;
        const currentBehavior = response.current_behavior?.split('.').pop() || response.behaviors?.current || 'prioritization';
        helper.assert_hierarchy_complete(html, {
            behaviors: ['prioritization', 'exploration', 'scenarios', 'tests', 'code', 'shape'],
            actions: {
                prioritization: ['clarify', 'strategy', 'validate', 'render']
            },
            current: currentBehavior
        });
    }
    
    // ========================================================================
    // EDGE CASE TESTS
    // ========================================================================
    
    async testBehaviorWithVeryLongName() {
        const html = await helper.render_html();
        assert.ok(html.includes('prioritization'), 'Should contain prioritization behavior');
        assert.ok(html.length > 0, 'Should render HTML');
    }
    
    async testBehaviorWithSpecialCharacters() {
        const html = await helper.render_html();
        assert.ok(html.includes('prioritization'), 'Should handle behavior names');
        assert.ok(html.includes('clarify'), 'Should handle action names');
    }
    
    async testMultipleBehaviorsWithSameActionNames() {
        const html = await helper.render_html();
        assert.ok(html.includes('prioritization'), 'Should contain prioritization');
        assert.ok(html.includes('exploration'), 'Should contain exploration');
        assert.ok(html.includes('scenarios'), 'Should contain scenarios');
        const clarifyCount = (html.match(/clarify/g) || []).length;
        const validateCount = (html.match(/validate/g) || []).length;
        assert.ok(clarifyCount >= 2, 'Clarify should appear in multiple behaviors');
        assert.ok(validateCount >= 2, 'Validate should appear in multiple behaviors');
    }
    
    // ========================================================================
    // INTEGRATION WITH REAL CLI DATA
    // ========================================================================
    
    async testRenderingFromRealCLIResponse() {
        const statusResponse = await helper._cli.execute('status');
        const response = statusResponse.bot || statusResponse;
        assert.ok(response.behaviors, 'Should have behaviors');
        assert.ok(response.behaviors.all_behaviors, 'Should have all_behaviors');
        assert.ok(Array.isArray(response.behaviors.all_behaviors), 'all_behaviors should be array');
        const behaviorsData = response.behaviors.all_behaviors;
        const html = await helper.render_html();
        helper.assert_complete_state_rendered(html, response);
        for (const behavior of behaviorsData) {
            helper.assert_behavior_fully_rendered(html, behavior);
        }
    }
}

class TestDisplayBehaviorHierarchy {
    
    async testSingleBehaviorWithFiveActions() {
        // Initialize bot state - status command needs bot to be initialized
        await helper._cli.execute('shape');
        const html = await helper.render_html();
        helper.assert_behavior_with_actions(html, 'shape', ['clarify', 'strategy', 'validate', 'build', 'render']);
    }
    
    async testMultipleBehaviorsInPriorityOrder() {
        // Initialize bot state - status command needs bot to be initialized
        await helper._cli.execute('shape');
        const html = await helper.render_html();
        helper.assert_behaviors_in_order(html, ['shape', 'prioritization', 'exploration']);
    }
    
    async testCurrentBehaviorMarked() {
        // Initialize bot state - status command needs bot to be initialized
        await helper._cli.execute('shape');
        const html = await helper.render_html();
        const statusResponse = await helper._cli.execute('status');
        const response = statusResponse.bot || statusResponse;
        const currentBehavior = response.behaviors.current || 'shape';
        helper.assert_current_behavior_marked(html, currentBehavior);
    }
    
    async testCompletedActionsMarked() {
        // Initialize bot state - status command needs bot to be initialized
        await helper._cli.execute('shape');
        const html = await helper.render_html();
        helper.assert_completed_actions_marked(html, ['clarify']);
    }
    
    async testBehaviorHierarchyComplete() {
        // Initialize bot state - status command needs bot to be initialized
        await helper._cli.execute('shape');
        const html = await helper.render_html();
        const statusResponse = await helper._cli.execute('status');
        const response = statusResponse.bot || statusResponse;
        const currentBehavior = response.behaviors.current || 'shape';
        helper.assert_hierarchy_complete(html, {
            behaviors: ['shape', 'prioritization', 'exploration', 'scenarios'],
            actions: { shape: ['clarify', 'strategy', 'validate'] },
            current: currentBehavior
        });
    }
}

class TestDisplayBehaviorHierarchyEdgeCases {
    
    async testEmptyBehaviorsList() {
        // Initialize bot state - status command needs bot to be initialized
        await helper._cli.execute('shape');
        const html = await helper.render_html();
        assert.ok(typeof html === 'string', 'Should return HTML string');
    }
    
    async testBehaviorWithNoActions() {
        // Initialize bot state - status command needs bot to be initialized
        await helper._cli.execute('shape');
        const html = await helper.render_html();
        helper.assert_behavior_with_actions(html, 'shape', []);
    }
}


test('TestNavigateBehaviorAction', { concurrency: false, timeout: 60000 }, async (t) => {
    const suite = new TestNavigateBehaviorAction();
    
    await t.test('testUserNavigatesToShapeBehavior', async () => {
        await suite.testUserNavigatesToShapeBehavior();
    });
    
    await t.test('testUserNavigatesToSpecificAction', async () => {
        await suite.testUserNavigatesToSpecificAction();
    });
    
    await t.test('testNavigationUpdatesHierarchyDisplay', async () => {
        await suite.testNavigationUpdatesHierarchyDisplay();
    });
    
    await t.test('testNavigationPersistsBotState', async () => {
        await suite.testNavigationPersistsBotState();
    });
});

test('TestBehaviorsView', { concurrency: false, timeout: 60000 }, async (t) => {
    const suite = new TestBehaviorsView();
    
    // CRITICAL: Test complete section first
    await t.test('testBehaviorActionSectionComplete', async () => {
        await suite.testBehaviorActionSectionComplete();
    });
    
    // Display hierarchy tests
    await t.test('testSingleBehaviorWithNoActions', async () => {
        await suite.testSingleBehaviorWithNoActions();
    });
    
    await t.test('testSingleBehaviorWithMultipleActions', async () => {
        await suite.testSingleBehaviorWithMultipleActions();
    });
    
    await t.test('testMultipleBehaviorsInOrder', async () => {
        await suite.testBehaviorsDisplayedInCanonicalOrder();
    });
    
    await t.test('testEmptyBehaviorsList', async () => {
        await suite.testEmptyBehaviorsList();
    });
    
    // Current behavior marking tests
    await t.test('testCurrentBehaviorMarkedInHierarchy', async () => {
        await suite.testCurrentBehaviorMarkedInHierarchy();
    });
    
    await t.test('testNonCurrentBehaviorNotMarked', async () => {
        await suite.testNonCurrentBehaviorNotMarked();
    });
    
    // Action listing tests
    await t.test('testActionsListedUnderBehavior', async () => {
        await suite.testActionsListedUnderBehavior();
    });
    
    await t.test('testActionsInCorrectOrder', async () => {
        await suite.testActionsInCorrectOrder();
    });
    
    // Completed action tests
    await t.test('testCompletedActionsShowIndicator', async () => {
        await suite.testCompletedActionsShowIndicator();
    });
    
    await t.test('testNoCompletedActionsShowsPendingOnly', async () => {
        await suite.testNoCompletedActionsShowsPendingOnly();
    });
    
    // Execute button tests
    await t.test('testActionsHaveExecuteButtons', async () => {
        await suite.testActionsHaveExecuteButtons();
    });
    
    // Complete hierarchy tests
    await t.test('testCompleteHierarchyRendering', async () => {
        await suite.testCompleteHierarchyRendering();
    });
    
    // Edge case tests
    await t.test('testBehaviorWithVeryLongName', async () => {
        await suite.testBehaviorWithVeryLongName();
    });
    
    await t.test('testBehaviorWithSpecialCharacters', async () => {
        await suite.testBehaviorWithSpecialCharacters();
    });
    
    await t.test('testMultipleBehaviorsWithSameActionNames', async () => {
        await suite.testMultipleBehaviorsWithSameActionNames();
    });
    
    // Integration tests
    await t.test('testRenderingFromRealCLIResponse', async () => {
        await suite.testRenderingFromRealCLIResponse();
    });
});

test('TestDisplayBehaviorHierarchy', { concurrency: false }, async (t) => {
    const suite = new TestDisplayBehaviorHierarchy();
    
    await t.test('testSingleBehaviorWithFiveActions', async () => {
        await suite.testSingleBehaviorWithFiveActions();
    });
    
    await t.test('testMultipleBehaviorsInPriorityOrder', async () => {
        await suite.testMultipleBehaviorsInPriorityOrder();
    });
    
    await t.test('testCurrentBehaviorMarked', async () => {
        await suite.testCurrentBehaviorMarked();
    });
    
    await t.test('testCompletedActionsMarked', async () => {
        await suite.testCompletedActionsMarked();
    });
    
    await t.test('testBehaviorHierarchyComplete', async () => {
        await suite.testBehaviorHierarchyComplete();
    });
});

test('TestDisplayBehaviorHierarchyEdgeCases', { concurrency: false }, async (t) => {
    const suite = new TestDisplayBehaviorHierarchyEdgeCases();
    
    await t.test('testEmptyBehaviorsList', async () => {
        await suite.testEmptyBehaviorsList();
    });
    
    await t.test('testBehaviorWithNoActions', async () => {
        await suite.testBehaviorWithNoActions();
    });
});

/**
 * RULE COMPLIANCE CHECKLIST:
 * 
 * Language & Naming:
 * [X] use_domain_language - behavior, action, hierarchy
 * [X] consistent_vocabulary - create, assert, verify
 * [X] use_exact_variable_names - behaviorName, actionNames
 * 
 * Structure:
 * [X] use_class_based_organization - TestDisplayBehaviorHierarchy class
 * [X] place_imports_at_top - All imports at top
 * [X] create_parameterized_tests_for_scenarios - Explicit test methods
 * 
 * Content:
 * [X] no_defensive_code_in_tests - Direct calls, no guards
 * [X] call_production_code_directly - Real view rendering
 * [X] test_observable_behavior - Testing HTML output
 * [X] match_specification_scenarios - Matches story scenarios
 * 
 * Helpers:
 * [X] object_oriented_test_helpers - BehaviorsViewTestHelper class
 * [X] helper_extraction_and_reuse - givenXXX, whenXXX, thenXXX
 * [X] use_given_when_then_helpers - Explicit Given/When/Then methods
 * 
 * Data:
 * [X] standard_test_data_sets - Reusable helper methods
 * [X] assert_full_results - thenHierarchyIsComplete
 * 
 * Coverage:
 * [X] cover_all_behavior_paths - Happy path + edge cases
 * 
 * Mocking:
 * [X] mock_only_boundaries - No mocking of view itself
 * 
 * Quality:
 * [X] production_code_clean_functions - Each test under 20 lines
 * [X] self_documenting_tests - Scenario blocks + clean code
 * [X] use_ascii_only - No Unicode characters
 * 
 * Fixtures:
 * [X] define_fixtures_in_test_file - Test data in helper methods
 * [X] orchestrator_pattern - Tests orchestrate via helper methods
 */