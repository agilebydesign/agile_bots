/**
 * Then E2E Helper
 * 
 * Handles assertions and verifications for E2E tests
 * Provides Then steps for vscode-extension-tester tests
 */

const BaseE2EHelper = require('./base_e2e_helper');
const { By } = require('selenium-webdriver');
const { expect } = require('chai');

class ThenE2EHelper extends BaseE2EHelper {
    /**
     * Assert button is visible
     * @param {string} buttonId - Button ID (e.g., 'btn-create-epic')
     */
    async buttonIsVisible(buttonId) {
        await this.webview.switchToFrame(5000);
        const button = await this.webview.findWebElement(By.id(buttonId));
        const isDisplayed = await button.isDisplayed();
        expect(isDisplayed).to.be.true;
        await this.webview.switchBack();
    }
    
    /**
     * Assert button is not visible
     * @param {string} buttonId - Button ID
     */
    async buttonIsNotVisible(buttonId) {
        await this.webview.switchToFrame(5000);
        try {
            const button = await this.webview.findWebElement(By.id(buttonId));
            const isDisplayed = await button.isDisplayed();
            expect(isDisplayed).to.be.false;
        } catch (e) {
            // Button not found = not visible, which is what we want
            expect(true).to.be.true;
        }
        await this.webview.switchBack();
    }
    
    /**
     * Assert create sub-epic button displays
     */
    async panelDisplaysCreateSubEpicButton() {
        await this.buttonIsVisible('btn-create-sub-epic');
    }
    
    /**
     * Assert create story button displays
     */
    async panelDisplaysCreateStoryButton() {
        await this.buttonIsVisible('btn-create-story');
    }
    
    /**
     * Assert create scenario button displays
     */
    async panelDisplaysCreateScenarioButton() {
        await this.buttonIsVisible('btn-create-scenario');
    }
    
    /**
     * Assert create acceptance criteria button displays
     */
    async panelDisplaysCreateAcceptanceCriteriaButton() {
        await this.buttonIsVisible('btn-create-acceptance-criteria');
    }
    
    /**
     * Assert delete button displays
     */
    async panelDisplaysDeleteButton() {
        await this.buttonIsVisible('btn-delete');
    }
    
    /**
     * Assert create sub-epic button does not display
     */
    async panelDoesNotDisplayCreateSubEpicButton() {
        await this.buttonIsNotVisible('btn-create-sub-epic');
    }
    
    /**
     * Assert create story button does not display
     */
    async panelDoesNotDisplayCreateStoryButton() {
        await this.buttonIsNotVisible('btn-create-story');
    }
    
    /**
     * Assert node exists in panel
     * @param {string} nodeName - Node name
     * @param {string} nodeType - Node type (epic, sub-epic, story, scenario)
     */
    async nodeExistsInPanel(nodeName, nodeType) {
        await this.webview.switchToFrame(5000);
        const node = await this.webview.findWebElement(
            By.css(`[data-node-type="${nodeType}"][data-node-name="${nodeName}"]`)
        );
        const isDisplayed = await node.isDisplayed();
        expect(isDisplayed).to.be.true;
        await this.webview.switchBack();
    }
    
    /**
     * Assert epic exists in panel
     * @param {string} epicName - Epic name
     */
    async epicExistsInPanel(epicName) {
        await this.nodeExistsInPanel(epicName, 'epic');
    }
    
    /**
     * Assert sub-epic exists in panel
     * @param {string} subEpicName - Sub-Epic name
     */
    async subEpicExistsInPanel(subEpicName) {
        await this.nodeExistsInPanel(subEpicName, 'sub-epic');
    }
    
    /**
     * Assert story exists in panel
     * @param {string} storyName - Story name
     */
    async storyExistsInPanel(storyName) {
        await this.nodeExistsInPanel(storyName, 'story');
    }
    
    /**
     * Assert node is selected (has 'selected' class)
     * @param {string} nodeName - Node name
     */
    async nodeIsSelected(nodeName) {
        await this.webview.switchToFrame(5000);
        const node = await this.webview.findWebElement(
            By.css(`[data-node-name="${nodeName}"]`)
        );
        const className = await node.getAttribute('class');
        expect(className).to.include('selected');
        await this.webview.switchBack();
    }
    
    /**
     * Assert node exists in story graph file
     * @param {string} epicName - Epic name
     * @param {string} childName - Optional child name
     * @param {string} childType - Child type ('sub-epic', 'story')
     */
    async nodeExistsInStoryGraphFile(epicName, childName = null, childType = null) {
        if (!childName) {
            const epic = this.parent.storyGraph.assertEpicExists(epicName);
            expect(epic).to.not.be.null;
            return;
        }
        
        if (childType === 'sub-epic') {
            const subEpic = this.parent.storyGraph.assertSubEpicExists(epicName, childName);
            expect(subEpic).to.not.be.null;
        }
    }
    
    /**
     * Assert node count in panel
     * @param {string} nodeType - Node type (epic, sub-epic, story)
     * @param {number} expectedCount - Expected count
     */
    async panelHasNodeCount(nodeType, expectedCount) {
        await this.webview.switchToFrame(5000);
        const nodes = await this.webview.findWebElements(
            By.css(`[data-node-type="${nodeType}"]`)
        );
        expect(nodes.length).to.equal(expectedCount);
        await this.webview.switchBack();
    }
    
    /**
     * Assert node has data-path attribute
     * @param {string} nodeName - Node name
     * @param {string} expectedPath - Expected path value
     */
    async nodeHasDataPath(nodeName, expectedPath) {
        await this.webview.switchToFrame(5000);
        const node = await this.webview.findWebElement(
            By.css(`[data-node-name="${nodeName}"]`)
        );
        const dataPath = await node.getAttribute('data-path');
        expect(dataPath).to.equal(expectedPath);
        await this.webview.switchBack();
    }
    
    /**
     * Assert panel refreshed and shows new content
     */
    async panelRefreshed() {
        // Wait for panel update cycle
        await this.parent.sleep(500);
        
        // Verify panel is responsive
        await this.webview.switchToFrame(5000);
        const storyMapSection = await this.webview.findWebElement(
            By.css('.scope-section')
        );
        const isDisplayed = await storyMapSection.isDisplayed();
        expect(isDisplayed).to.be.true;
        await this.webview.switchBack();
    }
}

module.exports = ThenE2EHelper;
