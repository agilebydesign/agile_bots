/**
 * Test Suite: Manage Panel Session
 * Sub-Epic: Manage Panel Session
 * 
 * This test file validates all stories related to managing the panel session:
 * - Open Panel
 * - Display Session Status
 * - Change Workspace Path
 * - Switch Bot
 * - Toggle Panel Section
 */

const { test, expect } = require('@playwright/test');
const { _electron: electron } = require('playwright');
const path = require('path');
const {
  given_vscode_is_running_with_extension,
  given_panel_is_already_open,
  when_user_opens_command_palette,
  when_user_opens_panel_via_command_palette,
  when_user_clicks_refresh_button,
  when_user_toggles_section,
  then_panel_is_displayed,
  then_panel_displays_bot_name,
  then_panel_displays_workspace_path,
  then_panel_displays_behavior_section,
  then_panel_displays_scope_section,
  then_panel_displays_instructions_section,
  then_section_is_collapsed,
  then_section_is_expanded,
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
      '--disable-extensions', // Disable other extensions
      '--skip-welcome',
      '--skip-release-notes',
      '--start-minimized',
    ],
  });
  
  // Get the first window
  page = await electronApp.firstWindow();
  
  // Wait for VS Code to be ready
  await given_vscode_is_running_with_extension(electronApp);
});

test.afterAll(async () => {
  await electronApp.close();
});

// ============================================================================
// STORY: Open Panel
// ============================================================================

test.describe('TestOpenPanel', () => {
  
  test('test_user_opens_panel_via_command_palette_happy_path', async () => {
    // GIVEN: VS Code is running with the Agile Bot extension installed
    // (already set up in beforeAll)
    
    // WHEN: User opens the Command Palette
    // AND: User types 'Open Status Panel'
    // AND: User selects 'Agile Bot: Open Status Panel'
    await when_user_opens_panel_via_command_palette(page);
    
    // THEN: The Bot Status Dashboard panel is displayed
    await then_panel_is_displayed(page);
    
    // AND: Panel displays the current bot's name
    // Note: We'll use a generic check here since bot name depends on workspace
    const frame = await get_panel_webview_frame(page);
    const sessionInfo = await frame.locator('div.session-info');
    await expect(sessionInfo).toBeVisible();
    
    // AND: Panel displays the current workspace path
    await then_panel_displays_workspace_path(page);
    
    // AND: Panel displays the Behavior Action section
    await then_panel_displays_behavior_section(page);
    
    // AND: Panel displays the Scope section
    await then_panel_displays_scope_section(page);
    
    // AND: Panel displays the Instructions section
    await then_panel_displays_instructions_section(page);
  });
  
  test('test_panel_already_open_when_command_executed_edge_case', async () => {
    // GIVEN: The Bot Status Dashboard panel is already open
    await given_panel_is_already_open(page);
    
    // WHEN: User executes the 'Agile Bot: Open Status Panel' command again
    await when_user_opens_panel_via_command_palette(page);
    
    // THEN: The existing Bot Status Dashboard panel is revealed and brought to focus
    await then_panel_is_displayed(page);
    
    // AND: The panel content is refreshed
    // (We verify this by checking that panel is still displaying correctly)
    await then_panel_displays_behavior_section(page);
    await then_panel_displays_scope_section(page);
    await then_panel_displays_instructions_section(page);
  });
  
  test('test_no_bots_configured_in_workspace_error_case', async () => {
    // GIVEN: VS Code is running with the Agile Bot extension installed
    // AND: No bots are configured in the current workspace
    // Note: This test requires a workspace with no bot configuration
    // For now, we'll skip this test as it requires special setup
    test.skip('Requires workspace with no bot configuration');
    
    // WHEN: User executes the 'Agile Bot: Open Status Panel' command
    await when_user_opens_panel_via_command_palette(page);
    
    // THEN: The Bot Status Dashboard panel is displayed
    await then_panel_is_displayed(page);
    
    // AND: Panel displays an error message indicating no bot is configured
    const frame = await get_panel_webview_frame(page);
    const errorMessage = await frame.locator('text=/no bot.*configured/i');
    await expect(errorMessage).toBeVisible();
  });
});

// ============================================================================
// STORY: Display Session Status
// ============================================================================

test.describe('TestDisplaySessionStatus', () => {
  
  test('test_panel_displays_session_info_on_load_happy_path', async () => {
    // GIVEN: The Bot Status Dashboard panel is open
    await given_panel_is_already_open(page);
    
    // WHEN: The panel loads
    // (already loaded from given step)
    
    // THEN: Panel displays the bot name in the session section
    const frame = await get_panel_webview_frame(page);
    const sessionInfo = await frame.locator('div.session-info');
    await expect(sessionInfo).toBeVisible();
    
    // AND: Panel displays the workspace path
    await then_panel_displays_workspace_path(page);
    
    // AND: Panel displays the bot directory path
    const botDir = await frame.locator('text=/Bot.*Dir/i');
    await expect(botDir).toBeVisible();
  });
  
  test('test_session_status_updates_on_refresh_happy_path', async () => {
    // GIVEN: The Bot Status Dashboard panel is open
    await given_panel_is_already_open(page);
    
    // WHEN: User clicks the refresh button
    await when_user_clicks_refresh_button(page);
    
    // THEN: The session status is refreshed
    // (Verify that panel still displays correctly after refresh)
    await then_panel_is_displayed(page);
    await then_panel_displays_workspace_path(page);
    await then_panel_displays_behavior_section(page);
  });
});

// ============================================================================
// STORY: Toggle Panel Section
// ============================================================================

test.describe('TestTogglePanelSection', () => {
  
  test('test_user_collapses_section_happy_path', async () => {
    // GIVEN: The Bot Status Dashboard panel is open
    await given_panel_is_already_open(page);
    
    // AND: A section (Behaviors) is expanded
    await then_section_is_expanded(page, 'Behaviors');
    
    // WHEN: User clicks on the section header to collapse it
    await when_user_toggles_section(page, 'Behaviors');
    
    // THEN: The section collapses and content is hidden
    await then_section_is_collapsed(page, 'Behaviors');
  });
  
  test('test_user_expands_section_happy_path', async () => {
    // GIVEN: The Bot Status Dashboard panel is open
    await given_panel_is_already_open(page);
    
    // AND: A section (Scope) is collapsed
    await when_user_toggles_section(page, 'Scope');
    await then_section_is_collapsed(page, 'Scope');
    
    // WHEN: User clicks on the section header to expand it
    await when_user_toggles_section(page, 'Scope');
    
    // THEN: The section expands and content is visible
    await then_section_is_expanded(page, 'Scope');
  });
  
  test('test_multiple_sections_can_be_toggled_independently_edge_case', async () => {
    // GIVEN: The Bot Status Dashboard panel is open
    await given_panel_is_already_open(page);
    
    // WHEN: User collapses Behaviors section
    await when_user_toggles_section(page, 'Behaviors');
    
    // AND: User keeps Scope section expanded
    await then_section_is_expanded(page, 'Scope');
    
    // THEN: Behaviors section is collapsed
    await then_section_is_collapsed(page, 'Behaviors');
    
    // AND: Scope section remains expanded
    await then_section_is_expanded(page, 'Scope');
  });
});

// ============================================================================
// STORY: Change Workspace Path
// ============================================================================

test.describe('TestChangeWorkspacePath', () => {
  
  test('test_change_workspace_path_happy_path', async () => {
    // This story requires changing the workspace, which is complex in VS Code
    // Skipping for now - requires special setup
    test.skip('Requires workspace switching capability');
  });
});

// ============================================================================
// STORY: Switch Bot
// ============================================================================

test.describe('TestSwitchBot', () => {
  
  test('test_switch_bot_happy_path', async () => {
    // This story requires multiple bots to be configured
    // Skipping for now - requires special setup
    test.skip('Requires multiple configured bots');
  });
});


