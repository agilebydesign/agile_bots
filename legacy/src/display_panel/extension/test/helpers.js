/**
 * Test Helpers for VS Code Extension E2E Testing with Playwright
 * 
 * This module provides Given/When/Then helper functions following the orchestrator pattern.
 * Helpers are organized by:
 * - Given: State setup and preconditions
 * - When: User actions and interactions
 * - Then: Assertions and verifications
 */

const { expect } = require('@playwright/test');
const path = require('path');

// ============================================================================
// GIVEN: State Setup and Preconditions
// ============================================================================

/**
 * Setup: VS Code is running with extension installed
 * This is typically called in beforeEach hooks
 * 
 * @param {Object} electronApp - The Electron app instance from @vscode/test-electron
 * @returns {Promise<void>}
 */
async function given_vscode_is_running_with_extension(electronApp) {
  // Wait for VS Code window to be ready
  const window = await electronApp.firstWindow();
  await window.waitForLoadState('domcontentloaded');
  
  // Wait for extension host to be ready (give it time to activate)
  await window.waitForTimeout(2000);
}

/**
 * Given: Workspace is opened
 * 
 * @param {Object} electronApp - The Electron app instance
 * @param {string} workspacePath - Path to workspace to open
 * @returns {Promise<void>}
 */
async function given_workspace_is_opened(electronApp, workspacePath) {
  const window = await electronApp.firstWindow();
  
  // Open workspace via command palette
  await window.keyboard.press('Control+Shift+P');
  await window.keyboard.type('File: Open Folder');
  await window.keyboard.press('Enter');
  await window.waitForTimeout(500);
  
  // Type workspace path
  await window.keyboard.type(workspacePath);
  await window.keyboard.press('Enter');
  await window.waitForTimeout(2000);
}

/**
 * Given: Panel is already open
 * 
 * @param {Object} page - Playwright page instance
 * @returns {Promise<void>}
 */
async function given_panel_is_already_open(page) {
  await when_user_opens_panel_via_command_palette(page);
  await then_panel_is_displayed(page);
}

/**
 * Given: Specific behavior action is selected
 * 
 * @param {Object} page - Playwright page instance
 * @param {string} behaviorName - Name of behavior
 * @param {string} actionName - Name of action
 * @returns {Promise<void>}
 */
async function given_behavior_action_is_selected(page, behaviorName, actionName) {
  // Ensure panel is open
  await given_panel_is_already_open(page);
  
  // Navigate to behavior action
  await when_user_clicks_behavior(page, behaviorName);
  await when_user_clicks_action(page, actionName);
}

// ============================================================================
// WHEN: User Actions and Interactions
// ============================================================================

/**
 * When: User opens Command Palette
 * 
 * @param {Object} page - Playwright page instance
 * @returns {Promise<void>}
 */
async function when_user_opens_command_palette(page) {
  await page.keyboard.press('Control+Shift+P');
  await page.waitForTimeout(500);
}

/**
 * When: User opens panel via command palette
 * 
 * @param {Object} page - Playwright page instance
 * @returns {Promise<void>}
 */
async function when_user_opens_panel_via_command_palette(page) {
  await when_user_opens_command_palette(page);
  await page.keyboard.type('Show Bot Status Dashboard');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1000);
}

/**
 * When: User clicks refresh button
 * 
 * @param {Object} page - Playwright page instance
 * @returns {Promise<void>}
 */
async function when_user_clicks_refresh_button(page) {
  // Find webview frame
  const frame = await get_panel_webview_frame(page);
  
  // Click refresh button
  await frame.click('button:has-text("Refresh")');
  await page.waitForTimeout(1000);
}

/**
 * When: User clicks a behavior in the hierarchy
 * 
 * @param {Object} page - Playwright page instance
 * @param {string} behaviorName - Name of behavior to click
 * @returns {Promise<void>}
 */
async function when_user_clicks_behavior(page, behaviorName) {
  const frame = await get_panel_webview_frame(page);
  
  // Find and click behavior
  await frame.click(`div.behavior-name:has-text("${behaviorName}")`);
  await page.waitForTimeout(500);
}

/**
 * When: User clicks an action in the hierarchy
 * 
 * @param {Object} page - Playwright page instance
 * @param {string} actionName - Name of action to click
 * @returns {Promise<void>}
 */
async function when_user_clicks_action(page, actionName) {
  const frame = await get_panel_webview_frame(page);
  
  // Find and click action
  await frame.click(`div.action-name:has-text("${actionName}")`);
  await page.waitForTimeout(500);
}

/**
 * When: User clicks "Copy Instructions" button
 * 
 * @param {Object} page - Playwright page instance
 * @returns {Promise<void>}
 */
async function when_user_clicks_copy_instructions(page) {
  const frame = await get_panel_webview_frame(page);
  
  // Click copy button
  await frame.click('button:has-text("Copy Instructions")');
  await page.waitForTimeout(500);
}

/**
 * When: User toggles panel section
 * 
 * @param {Object} page - Playwright page instance
 * @param {string} sectionName - Name of section to toggle (e.g., "Behaviors", "Scope", "Instructions")
 * @returns {Promise<void>}
 */
async function when_user_toggles_section(page, sectionName) {
  const frame = await get_panel_webview_frame(page);
  
  // Find and click section header to toggle
  await frame.click(`h2:has-text("${sectionName}")`);
  await page.waitForTimeout(500);
}

// ============================================================================
// THEN: Assertions and Verifications
// ============================================================================

/**
 * Then: Panel is displayed
 * 
 * @param {Object} page - Playwright page instance
 * @returns {Promise<void>}
 */
async function then_panel_is_displayed(page) {
  // Check for panel title or a known element in the panel
  const frame = await get_panel_webview_frame(page);
  
  // Verify panel header exists
  const header = await frame.locator('h1').first();
  await expect(header).toBeVisible();
}

/**
 * Then: Panel displays bot name
 * 
 * @param {Object} page - Playwright page instance
 * @param {string} expectedBotName - Expected bot name
 * @returns {Promise<void>}
 */
async function then_panel_displays_bot_name(page, expectedBotName) {
  const frame = await get_panel_webview_frame(page);
  
  // Check for bot name in session info
  const botNameElement = await frame.locator(`text=${expectedBotName}`);
  await expect(botNameElement).toBeVisible();
}

/**
 * Then: Panel displays workspace path
 * 
 * @param {Object} page - Playwright page instance
 * @returns {Promise<void>}
 */
async function then_panel_displays_workspace_path(page) {
  const frame = await get_panel_webview_frame(page);
  
  // Check for workspace path element
  const workspaceElement = await frame.locator('div.session-info >> text=/Workspace/');
  await expect(workspaceElement).toBeVisible();
}

/**
 * Then: Panel displays behavior action section
 * 
 * @param {Object} page - Playwright page instance
 * @returns {Promise<void>}
 */
async function then_panel_displays_behavior_section(page) {
  const frame = await get_panel_webview_frame(page);
  
  // Check for behaviors section
  const behaviorsSection = await frame.locator('h2:has-text("Behaviors")');
  await expect(behaviorsSection).toBeVisible();
}

/**
 * Then: Panel displays scope section
 * 
 * @param {Object} page - Playwright page instance
 * @returns {Promise<void>}
 */
async function then_panel_displays_scope_section(page) {
  const frame = await get_panel_webview_frame(page);
  
  // Check for scope section
  const scopeSection = await frame.locator('h2:has-text("Scope")');
  await expect(scopeSection).toBeVisible();
}

/**
 * Then: Panel displays instructions section
 * 
 * @param {Object} page - Playwright page instance
 * @returns {Promise<void>}
 */
async function then_panel_displays_instructions_section(page) {
  const frame = await get_panel_webview_frame(page);
  
  // Check for instructions section
  const instructionsSection = await frame.locator('h2:has-text("Instructions")');
  await expect(instructionsSection).toBeVisible();
}

/**
 * Then: Instructions are displayed for action
 * 
 * @param {Object} page - Playwright page instance
 * @param {string} actionName - Name of action whose instructions should be displayed
 * @returns {Promise<void>}
 */
async function then_instructions_are_displayed_for_action(page, actionName) {
  const frame = await get_panel_webview_frame(page);
  
  // Check that instructions section contains the action name
  const instructionsContent = await frame.locator('div.instructions-content');
  await expect(instructionsContent).toContainText(actionName);
}

/**
 * Then: Behavior hierarchy shows actions
 * 
 * @param {Object} page - Playwright page instance
 * @param {string} behaviorName - Name of behavior
 * @param {Array<string>} expectedActions - Array of expected action names
 * @returns {Promise<void>}
 */
async function then_behavior_shows_actions(page, behaviorName, expectedActions) {
  const frame = await get_panel_webview_frame(page);
  
  // Verify each action is visible
  for (const actionName of expectedActions) {
    const actionElement = await frame.locator(`div.action-name:has-text("${actionName}")`);
    await expect(actionElement).toBeVisible();
  }
}

/**
 * Then: Panel displays error message
 * 
 * @param {Object} page - Playwright page instance
 * @param {string} expectedErrorMessage - Expected error message text
 * @returns {Promise<void>}
 */
async function then_panel_displays_error(page, expectedErrorMessage) {
  const frame = await get_panel_webview_frame(page);
  
  // Check for error message
  const errorElement = await frame.locator(`text=${expectedErrorMessage}`);
  await expect(errorElement).toBeVisible();
}

/**
 * Then: Section is collapsed
 * 
 * @param {Object} page - Playwright page instance
 * @param {string} sectionName - Name of section that should be collapsed
 * @returns {Promise<void>}
 */
async function then_section_is_collapsed(page, sectionName) {
  const frame = await get_panel_webview_frame(page);
  
  // Find section and check if it's collapsed (display: none or hidden class)
  const sectionContent = await frame.locator(`h2:has-text("${sectionName}") ~ div`);
  await expect(sectionContent).not.toBeVisible();
}

/**
 * Then: Section is expanded
 * 
 * @param {Object} page - Playwright page instance
 * @param {string} sectionName - Name of section that should be expanded
 * @returns {Promise<void>}
 */
async function then_section_is_expanded(page, sectionName) {
  const frame = await get_panel_webview_frame(page);
  
  // Find section and check if it's expanded (visible)
  const sectionContent = await frame.locator(`h2:has-text("${sectionName}") ~ div`);
  await expect(sectionContent).toBeVisible();
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Get the webview frame from the panel
 * Webviews in VS Code are rendered in iframes
 * 
 * @param {Object} page - Playwright page instance
 * @returns {Promise<Frame>} The webview frame
 */
async function get_panel_webview_frame(page) {
  // Wait for iframe to be present
  await page.waitForSelector('iframe.webview', { timeout: 10000 });
  
  // Get all frames and find the webview frame
  const frames = page.frames();
  const webviewFrame = frames.find(frame => {
    const url = frame.url();
    return url.includes('webview') || url.startsWith('vscode-webview://');
  });
  
  if (!webviewFrame) {
    throw new Error('Could not find webview frame');
  }
  
  return webviewFrame;
}

/**
 * Take a screenshot for debugging
 * 
 * @param {Object} page - Playwright page instance
 * @param {string} screenshotName - Name for the screenshot file
 * @returns {Promise<void>}
 */
async function take_debug_screenshot(page, screenshotName) {
  await page.screenshot({ 
    path: `test/screenshots/${screenshotName}.png`,
    fullPage: true 
  });
}

// ============================================================================
// EXPORTS
// ============================================================================

module.exports = {
  // Given helpers
  given_vscode_is_running_with_extension,
  given_workspace_is_opened,
  given_panel_is_already_open,
  given_behavior_action_is_selected,
  
  // When helpers
  when_user_opens_command_palette,
  when_user_opens_panel_via_command_palette,
  when_user_clicks_refresh_button,
  when_user_clicks_behavior,
  when_user_clicks_action,
  when_user_clicks_copy_instructions,
  when_user_toggles_section,
  
  // Then helpers
  then_panel_is_displayed,
  then_panel_displays_bot_name,
  then_panel_displays_workspace_path,
  then_panel_displays_behavior_section,
  then_panel_displays_scope_section,
  then_panel_displays_instructions_section,
  then_instructions_are_displayed_for_action,
  then_behavior_shows_actions,
  then_panel_displays_error,
  then_section_is_collapsed,
  then_section_is_expanded,
  
  // Utilities
  get_panel_webview_frame,
  take_debug_screenshot,
};

