/**
 * Given E2E Helper
 * 
 * Handles test setup and preconditions for E2E tests
 * Provides Given steps for vscode-extension-tester tests
 */

const BaseE2EHelper = require('./base_e2e_helper');
const { By } = require('selenium-webdriver');

class GivenE2EHelper extends BaseE2EHelper {
    /**
     * Set up story graph and load panel
     * @param {Object} graphData - Story graph data
     */
    async storyGraphLoadedInPanel(graphData = null) {
        // Create story graph file
        this.parent.storyGraph.createStoryGraph(graphData);
        
        // Navigate to panel
        await this.parent.navigateToPanel();
    }
    
    /**
     * Given story graph has epic named X
     * @param {string} epicName - Epic name
     */
    async storyGraphHasEpic(epicName) {
        const graphData = this.parent.storyGraph.givenStoryGraphWithEpic(epicName);
        return graphData;
    }
    
    /**
     * Given story graph has epic with sub-epic
     * @param {string} epicName - Epic name
     * @param {string} subEpicName - Sub-Epic name
     * @param {Object} options - Additional options
     */
    async storyGraphHasEpicWithSubEpic(epicName, subEpicName, options = {}) {
        const graphData = this.parent.storyGraph.givenStoryGraphWithSubEpic(epicName, subEpicName, options);
        return graphData;
    }
    
    /**
     * Given epic is selected
     * @param {string} epicName - Epic name
     */
    async epicIsSelected(epicName) {
        await this.webview.switchToFrame(5000);
        const epicNode = await this.webview.findWebElement(
            By.css(`[data-node-type="epic"][data-node-name="${epicName}"]`)
        );
        await epicNode.click();
        await this.parent.sleep(100); // Wait for selection to update
        await this.webview.switchBack();
    }
    
    /**
     * Given sub-epic is selected
     * @param {string} subEpicName - Sub-Epic name
     */
    async subEpicIsSelected(subEpicName) {
        await this.webview.switchToFrame(5000);
        const subEpicNode = await this.webview.findWebElement(
            By.css(`[data-node-type="sub-epic"][data-node-name="${subEpicName}"]`)
        );
        await subEpicNode.click();
        await this.parent.sleep(100);
        await this.webview.switchBack();
    }
    
    /**
     * Given story is selected
     * @param {string} storyName - Story name
     */
    async storyIsSelected(storyName) {
        await this.webview.switchToFrame(5000);
        const storyNode = await this.webview.findWebElement(
            By.css(`[data-node-type="story"][data-node-name="${storyName}"]`)
        );
        await storyNode.click();
        await this.parent.sleep(100);
        await this.webview.switchBack();
    }
}

module.exports = GivenE2EHelper;
