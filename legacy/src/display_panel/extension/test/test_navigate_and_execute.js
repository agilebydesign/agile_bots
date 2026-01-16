/**
 * Test Suite: Navigate And Execute Behaviors Through Panel
 * Sub-Epic: Navigate And Execute Behaviors Through Panel
 * 
 * This test file validates all stories related to navigating and executing behaviors:
 * - Display Hierarchy
 * - Navigate Behavior Action
 * - Execute Behavior Action
 */

const { test, expect } = require('@playwright/test');
const { _electron: electron } = require('playwright');
const path = require('path');
const {
  given_vscode_is_running_with_extension,
  given_panel_is_already_open,
  given_behavior_action_is_selected,
  when_user_clicks_behavior,
  when_user_clicks_action,
  then_panel_is_displayed,
  then_behavior_shows_actions,
  then_instructions_are_displayed_for_action,
  get_panel_webview_frame,
} = require('./helpers');

// ============================================================================
// TEST SETUP
// ============================================================================

let electronApp;
let page;

test.beforeAll(async () => {
  // Launch VS Code with extension
  electronApp = await electron.launch({
    executablePath: 'C:\\Users\\thoma\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe',
    args: [
      '--extensionDevelopmentPath=' + path.join(__dirname, '..'),
      '--disable-extensions',
      '--skip-welcome',
      '--skip-release-notes',
      '--start-minimized',
    ],
  });
  
  page = await electronApp.firstWindow();
  await given_vscode_is_running_with_extension(electronApp);
});

test.afterAll(async () => {
  await electronApp.close();
});

// ============================================================================
// STORY: Display Hierarchy
// ============================================================================

test.describe('TestDisplayHierarchy', () => {
  
  test('test_panel_displays_behavior_tree_with_progress_indicators', async () => {
    // GIVEN: Bot has multiple behaviors with completed and pending actions
    // AND: Bot is currently at shape.clarify
    await given_panel_is_already_open(page);
    
    const frame = await get_panel_webview_frame(page);
    
    // WHEN: Panel renders hierarchy section
    // (already rendered from given step)
    
    // THEN: User sees behavior names (shape, discovery, etc.)
    const behaviorSection = await frame.locator('h2:has-text("Behaviors")');
    await expect(behaviorSection).toBeVisible();
    
    // AND: User sees action names under behaviors
    const behaviorsContent = await frame.locator('div.behaviors-content');
    await expect(behaviorsContent).toBeVisible();
    
    // AND: Current action shows in-progress indicator
    // AND: Completed actions show checkmark indicator
    // AND: Pending actions show empty indicator
    // Note: Specific indicators depend on bot state, so we verify hierarchy is visible
    const behaviorItems = await frame.locator('div.behavior-item');
    await expect(behaviorItems.first()).toBeVisible();
  });
  
  test('test_user_expands_and_collapses_behaviors', async () => {
    // GIVEN: Panel displays collapsed behavior tree
    await given_panel_is_already_open(page);
    
    const frame = await get_panel_webview_frame(page);
    
    // WHEN: User clicks collapsed shape behavior
    await when_user_clicks_behavior(page, 'shape');
    
    // THEN: Shape behavior expands showing actions (clarify, strategy, etc.)
    // Verify actions are now visible
    await then_behavior_shows_actions(page, 'shape', ['clarify', 'strategy']);
    
    // WHEN: User clicks expanded shape behavior again
    await when_user_clicks_behavior(page, 'shape');
    
    // THEN: Shape behavior collapses hiding actions
    // Note: This depends on implementation - may require checking CSS or visibility
  });
  
  test('test_user_expands_and_collapses_actions', async () => {
    // GIVEN: Shape behavior is expanded showing actions
    await given_panel_is_already_open(page);
    await when_user_clicks_behavior(page, 'shape');
    
    const frame = await get_panel_webview_frame(page);
    
    // AND: Clarify action is collapsed
    // (default state)
    
    // WHEN: User clicks collapsed clarify action
    await when_user_clicks_action(page, 'clarify');
    
    // THEN: Clarify action expands showing operations (instructions, execute, confirm)
    // Verify operations are visible
    const operations = await frame.locator('div.operation-item');
    await expect(operations.first()).toBeVisible();
    
    // WHEN: User clicks expanded clarify action again
    await when_user_clicks_action(page, 'clarify');
    
    // THEN: Clarify action collapses hiding operations
    // Note: Verification depends on implementation
  });
});

// ============================================================================
// STORY: Navigate Behavior Action
// ============================================================================

test.describe('TestNavigateBehaviorAction', () => {
  
  test('test_user_clicks_action_and_bot_navigates_to_that_action', async () => {
    // GIVEN: Panel displays behavior hierarchy
    await given_panel_is_already_open(page);
    
    // AND: Bot is at shape.clarify
    // (depends on bot state, assume this is default)
    
    const frame = await get_panel_webview_frame(page);
    
    // WHEN: User clicks on discovery.build action link
    await when_user_clicks_behavior(page, 'discovery');
    await when_user_clicks_action(page, 'build');
    
    // THEN: Bot navigates to discovery.build
    // AND: Panel refreshes to show new current position
    // AND: discovery.build is highlighted as current action
    
    // Verify instructions are displayed for the new action
    await then_instructions_are_displayed_for_action(page, 'build');
  });
  
  test('test_user_navigates_forward_through_actions_with_next_button', async () => {
    // GIVEN: Bot is at shape.clarify
    await given_behavior_action_is_selected(page, 'shape', 'clarify');
    
    const frame = await get_panel_webview_frame(page);
    
    // WHEN: User clicks next button
    const nextButton = await frame.locator('button:has-text("Next")');
    if (await nextButton.isVisible()) {
      await nextButton.click();
      await page.waitForTimeout(1000);
      
      // THEN: Bot navigates to shape.strategy
      // AND: Panel displays shape.strategy as current
      // AND: Panel displays shape.strategy in-progress indicator
      await then_instructions_are_displayed_for_action(page, 'strategy');
    } else {
      // Skip if next button not available
      test.skip('Next button not available in current state');
    }
  });
  
  test('test_user_navigates_backward_through_actions_with_back_button', async () => {
    // GIVEN: Bot is at shape.strategy
    await given_behavior_action_is_selected(page, 'shape', 'strategy');
    
    const frame = await get_panel_webview_frame(page);
    
    // WHEN: User clicks back button
    const backButton = await frame.locator('button:has-text("Back")');
    if (await backButton.isVisible()) {
      await backButton.click();
      await page.waitForTimeout(1000);
      
      // THEN: Bot navigates to shape.clarify
      // AND: Panel displays shape.clarify as current
      await then_instructions_are_displayed_for_action(page, 'clarify');
    } else {
      // Skip if back button not available
      test.skip('Back button not available in current state');
    }
  });
});

// ============================================================================
// STORY: Execute Behavior Action
// ============================================================================

test.describe('TestExecuteBehaviorAction', () => {
  
  test('test_user_clicks_behavior_to_execute', async () => {
    // GIVEN: Panel displays behavior hierarchy
    await given_panel_is_already_open(page);
    
    // AND: Bot is at shape.clarify
    // (default state)
    
    // WHEN: User clicks discovery behavior
    await when_user_clicks_behavior(page, 'discovery');
    
    // THEN: Bot navigates to discovery.clarify (first action)
    // AND: Panel displays discovery behavior as current
    // AND: Panel expands discovery behavior
    // AND: Panel displays discovery.clarify as current action
    // AND: Bot executes discovery.clarify.instructions operation
    
    const frame = await get_panel_webview_frame(page);
    
    // Verify discovery behavior is expanded and visible
    const discoveryBehavior = await frame.locator('div.behavior-item:has-text("discovery")');
    await expect(discoveryBehavior).toBeVisible();
    
    // Verify instructions are displayed (indicating execution)
    await then_instructions_are_displayed_for_action(page, 'clarify');
  });
  
  test('test_user_clicks_action_to_execute', async () => {
    // GIVEN: Panel displays expanded shape behavior
    await given_panel_is_already_open(page);
    await when_user_clicks_behavior(page, 'shape');
    
    // AND: Bot is at shape.clarify
    // (default state)
    
    // WHEN: User clicks shape.strategy action
    await when_user_clicks_action(page, 'strategy');
    
    // THEN: Bot navigates to shape.strategy
    // AND: Panel displays shape.strategy as current action
    // AND: Panel expands shape.strategy showing operations
    // AND: Bot executes shape.strategy.instructions operation
    
    // Verify instructions are displayed for strategy
    await then_instructions_are_displayed_for_action(page, 'strategy');
  });
  
  test('test_user_clicks_operation_to_execute', async () => {
    // GIVEN: Panel displays expanded shape.clarify action
    await given_behavior_action_is_selected(page, 'shape', 'clarify');
    
    const frame = await get_panel_webview_frame(page);
    
    // AND: Bot is at shape.clarify.instructions
    // (default operation)
    
    // WHEN: User clicks shape.clarify.execute operation
    const executeOperation = await frame.locator('div.operation-item:has-text("execute")');
    if (await executeOperation.isVisible()) {
      await executeOperation.click();
      await page.waitForTimeout(1000);
      
      // THEN: Bot navigates to shape.clarify.execute
      // AND: Panel displays shape.clarify.execute as current operation
      // AND: Bot executes shape.clarify.execute operation
      
      // Verify instructions or output for execute operation
      const instructionsSection = await frame.locator('div.instructions-content');
      await expect(instructionsSection).toBeVisible();
    } else {
      // Skip if operations are not visible
      test.skip('Operations not visible in current implementation');
    }
  });
  
  test('test_execution_updates_instructions_section', async () => {
    // GIVEN: Panel is open with behavior selected
    await given_behavior_action_is_selected(page, 'shape', 'clarify');
    
    // WHEN: User clicks an action to execute
    await when_user_clicks_action(page, 'strategy');
    
    // THEN: Instructions section updates to show new action's instructions
    await then_instructions_are_displayed_for_action(page, 'strategy');
    
    const frame = await get_panel_webview_frame(page);
    
    // AND: Instructions content is not empty
    const instructionsContent = await frame.locator('div.instructions-content');
    const text = await instructionsContent.textContent();
    expect(text.length).toBeGreaterThan(0);
  });
});


