// @ts-check
const { defineConfig, devices } = require('@playwright/test');

/**
 * Playwright Configuration for VS Code Extension Testing
 * 
 * This configuration:
 * - Uses a single worker to avoid VS Code instance conflicts
 * - Captures screenshots and videos on failure
 * - Uses Electron to launch VS Code with extension
 * - Sets generous timeouts for VS Code extension startup
 */
module.exports = defineConfig({
  testDir: './test',
  
  // Match test files using Python-style naming convention (test_*.js)
  testMatch: /test_.*\.js$/,
  
  // Run tests in files in parallel, but use single worker to avoid VS Code conflicts
  fullyParallel: false,
  workers: 1,
  
  // Fail the build on CI if you accidentally left test.only in the source code
  forbidOnly: !!process.env.CI,
  
  // Retry on CI only
  retries: process.env.CI ? 2 : 0,
  
  // Reporter to use
  reporter: [
    ['html'],
    ['list']
  ],
  
  // Shared settings for all the projects below
  use: {
    // Collect trace when retrying the failed test
    trace: 'on-first-retry',
    
    // Screenshot on failure
    screenshot: 'only-on-failure',
    
    // Video on failure
    video: 'retain-on-failure',
    
    // Generous timeout for VS Code extension actions
    actionTimeout: 30000,
    
    // Increase navigation timeout for VS Code startup
    navigationTimeout: 30000,
  },
  
  // Configure timeout for each test (VS Code takes time to start)
  timeout: 60000,
  
  // No specific browser project needed - tests use electron.launch() directly
  projects: [
    {
      name: 'vscode-extension',
      testMatch: /test_.*\.js$/,
    },
  ],
});

