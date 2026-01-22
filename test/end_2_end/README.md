# End-to-End Panel Tests

End-to-end tests for Story Bot panel using **vscode-extension-tester**.

## Overview

These tests verify the **complete UI flow** by:
- Launching **real VS Code** with the extension installed
- Interacting with the **actual webview** using Selenium WebDriver
- Clicking **real buttons** and filling **real forms**
- Verifying **DOM rendering** and **backend persistence**

## Framework

- **vscode-extension-tester**: VS Code extension testing framework
- **Selenium WebDriver**: Browser automation for webview interaction
- **Mocha**: Test framework
- **Chai**: Assertion library

## Test Structure

```
test/end_2_end/
├── helpers/
│   ├── base_e2e_helper.js          # Base helper class
│   ├── panel_e2e_test_helper.js    # Main test helper
│   ├── story_graph_e2e_helper.js   # Story graph setup
│   ├── given_e2e_helper.js         # Given steps (test setup)
│   ├── when_e2e_helper.js          # When steps (user actions)
│   ├── then_e2e_helper.js          # Then steps (assertions)
│   └── index.js                    # Export all helpers
└── test_edit_story_graph_in_panel_e2e.js  # Main test file
```

## Running Tests

### Setup and Run (First Time)

Downloads VS Code and ChromeDriver, then runs tests:

```bash
npm run ui-test
```

### Setup Only

Download VS Code and ChromeDriver:

```bash
npm run ui-test-setup
```

### Run Tests Only

Run tests with existing VS Code installation:

```bash
npm run ui-test-run
```

## Test Helper Pattern

Tests use the **Given/When/Then** pattern:

```javascript
// Given: Set up story graph
await helper.given.storyGraphHasEpic('User Management');
await helper.navigateToPanel();

// When: User interaction
await helper.when.userSelectsEpic('User Management');

// Then: Verify result
await helper.then.panelDisplaysCreateSubEpicButton();
```

## How It Works

1. **Test Setup**: Creates isolated temp workspace
2. **VS Code Launch**: vscode-extension-tester launches real VS Code
3. **Panel Open**: Opens Story Bot panel via command
4. **WebView Access**: Switches into webview frame
5. **User Actions**: Clicks buttons, fills forms using Selenium
6. **Assertions**: Verifies DOM state and file persistence
7. **Cleanup**: Removes temp workspace

## Webview Interaction

To interact with webview elements, switch into the frame:

```javascript
await this.webview.switchToFrame(5000);
const button = await this.webview.findWebElement(By.id('btn-create-epic'));
await button.click();
await this.webview.switchBack();
```

## Key Differences from Unit Tests

| Aspect | Unit Tests | E2E Tests |
|--------|-----------|-----------|
| Environment | Mock webview | Real VS Code |
| Interactions | Simulated messages | Actual clicks |
| Validation | Backend only | UI + Backend |
| Speed | Fast (~seconds) | Slow (~minutes) |
| Scope | Individual functions | Complete flows |

## Test Coverage

These E2E tests cover the stories that **passed unit tests but failed in actual UI**:

1. **Create Child Story Node Under Parent**
   - Button visibility based on node type
   - Create Epic/SubEpic/Story/Scenario
   - UI state preservation

2. **Delete Story Node From Parent**
   - Delete button visibility
   - Cascading delete behavior
   - UI refresh after deletion

3. **Update Story Node Name**
   - Double-click to rename
   - Input box handling
   - Backend persistence

4. **Move Story Node**
   - Drag and drop interactions
   - Reordering logic
   - Sequential order updates

## Debugging

### View Test Execution

Tests run in **non-headless mode** by default, so you can watch VS Code launch and interact with the panel.

### Increase Timeouts

Modify `.mocharc.js`:

```javascript
module.exports = {
    timeout: 60000, // Increase from 30s to 60s
    // ...
};
```

### Add Logging

Use `console.log` in helpers:

```javascript
console.log('[E2E Debug] Button clicked:', buttonId);
```

## Configuration

Test configuration in `.mocharc.js`:

```javascript
module.exports = {
    timeout: 30000,      // Global timeout
    color: true,         // Colored output
    ui: 'bdd',          // BDD style (describe/it)
    reporter: 'spec'    // Detailed output
};
```

## Requirements

- Node.js 18+
- Python 3.8+ (for CLI commands)
- Sufficient disk space (~500MB for VS Code download)

## Notes

- First run downloads VS Code (~200MB) and ChromeDriver
- Downloads are cached in `test-resources/`
- Add `test-resources/` to `.gitignore`
- Tests run in isolated temp workspaces
- Each test gets fresh workspace and story graph
