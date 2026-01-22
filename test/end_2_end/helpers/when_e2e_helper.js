/**
 * When E2E Helper
 * 
 * Handles user actions and interactions for E2E tests
 * Provides When steps for vscode-extension-tester tests
 */

const BaseE2EHelper = require('./base_e2e_helper');
const { By } = require('selenium-webdriver');
const { InputBox } = require('vscode-extension-tester');

class WhenE2EHelper extends BaseE2EHelper {
    /**
     * User selects epic node
     * @param {string} epicName - Epic name
     */
    async userSelectsEpic(epicName) {
        await this.webview.switchToFrame(5000);
        const epicNode = await this.webview.findWebElement(
            By.css(`[data-node-type="epic"][data-node-name="${epicName}"]`)
        );
        await epicNode.click();
        await this.parent.sleep(100);
        await this.webview.switchBack();
    }
    
    /**
     * User selects sub-epic node
     * @param {string} subEpicName - Sub-Epic name
     */
    async userSelectsSubEpic(subEpicName) {
        await this.webview.switchToFrame(5000);
        const subEpicNode = await this.webview.findWebElement(
            By.css(`[data-node-type="sub-epic"][data-node-name="${subEpicName}"]`)
        );
        await subEpicNode.click();
        await this.parent.sleep(100);
        await this.webview.switchBack();
    }
    
    /**
     * User selects story node
     * @param {string} storyName - Story name
     */
    async userSelectsStory(storyName) {
        await this.webview.switchToFrame(5000);
        const storyNode = await this.webview.findWebElement(
            By.css(`[data-node-type="story"][data-node-name="${storyName}"]`)
        );
        await storyNode.click();
        await this.parent.sleep(100);
        await this.webview.switchBack();
    }
    
    /**
     * User clicks create epic button
     * @param {string} epicName - Name for new epic (will enter in VS Code input box)
     */
    async userClicksCreateEpic(epicName) {
        await this.webview.switchToFrame(5000);
        const createBtn = await this.webview.findWebElement(By.id('btn-create-epic'));
        await createBtn.click();
        await this.webview.switchBack();
        
        // Handle VS Code input box
        await this.parent.sleep(500);
        const inputBox = await InputBox.create();
        await inputBox.setText(epicName);
        await inputBox.confirm();
        
        // Wait for command to execute and panel to refresh
        await this.parent.sleep(1000);
    }
    
    /**
     * User clicks create sub-epic button
     * @param {string} subEpicName - Name for new sub-epic
     */
    async userClicksCreateSubEpic(subEpicName) {
        await this.webview.switchToFrame(5000);
        const createBtn = await this.webview.findWebElement(By.id('btn-create-sub-epic'));
        await createBtn.click();
        await this.webview.switchBack();
        
        await this.parent.sleep(500);
        const inputBox = await InputBox.create();
        await inputBox.setText(subEpicName);
        await inputBox.confirm();
        await this.parent.sleep(1000);
    }
    
    /**
     * User clicks create story button
     * @param {string} storyName - Name for new story
     */
    async userClicksCreateStory(storyName) {
        await this.webview.switchToFrame(5000);
        const createBtn = await this.webview.findWebElement(By.id('btn-create-story'));
        await createBtn.click();
        await this.webview.switchBack();
        
        await this.parent.sleep(500);
        const inputBox = await InputBox.create();
        await inputBox.setText(storyName);
        await inputBox.confirm();
        await this.parent.sleep(1000);
    }
    
    /**
     * User clicks create scenario button
     * @param {string} scenarioName - Name for new scenario
     */
    async userClicksCreateScenario(scenarioName) {
        await this.webview.switchToFrame(5000);
        const createBtn = await this.webview.findWebElement(By.id('btn-create-scenario'));
        await createBtn.click();
        await this.webview.switchBack();
        
        await this.parent.sleep(500);
        const inputBox = await InputBox.create();
        await inputBox.setText(scenarioName);
        await inputBox.confirm();
        await this.parent.sleep(1000);
    }
    
    /**
     * User clicks delete button
     */
    async userClicksDelete() {
        await this.webview.switchToFrame(5000);
        const deleteBtn = await this.webview.findWebElement(By.id('btn-delete'));
        await deleteBtn.click();
        await this.webview.switchBack();
        await this.parent.sleep(1000);
    }
    
    /**
     * User double-clicks node to rename
     * @param {string} nodeName - Node name
     * @param {string} newName - New name to enter
     */
    async userDoubleClicksToRename(nodeName, newName) {
        await this.webview.switchToFrame(5000);
        const node = await this.webview.findWebElement(
            By.css(`[data-node-name="${nodeName}"]`)
        );
        
        // Get driver for actions
        const driver = this.webview.getDriver();
        const actions = driver.actions();
        
        // Double click
        await actions.doubleClick(node).perform();
        await this.webview.switchBack();
        
        // Handle VS Code input box
        await this.parent.sleep(500);
        const inputBox = await InputBox.create();
        await inputBox.setText(newName);
        await inputBox.confirm();
        await this.parent.sleep(500);
    }
    
    /**
     * User drags node to another node
     * @param {string} draggedNodeName - Node being dragged
     * @param {string} targetNodeName - Drop target node
     */
    async userDragsNodeTo(draggedNodeName, targetNodeName) {
        await this.webview.switchToFrame(5000);
        
        const draggedNode = await this.webview.findWebElement(
            By.css(`[data-node-name="${draggedNodeName}"]`)
        );
        const targetNode = await this.webview.findWebElement(
            By.css(`[data-node-name="${targetNodeName}"]`)
        );
        
        // Get driver for drag and drop
        const driver = this.webview.getDriver();
        const actions = driver.actions();
        
        await actions.dragAndDrop(draggedNode, targetNode).perform();
        await this.webview.switchBack();
        
        // Wait for backend to process
        await this.parent.sleep(1000);
    }
    
    /**
     * User expands node
     * @param {string} nodeName - Node name to expand
     */
    async userExpandsNode(nodeName) {
        await this.webview.switchToFrame(5000);
        
        // Find the collapse icon within the node's container
        const collapseIcon = await this.webview.findWebElement(
            By.css(`[data-node-name="${nodeName}"] .collapse-icon`)
        );
        
        await collapseIcon.click();
        await this.parent.sleep(200);
        await this.webview.switchBack();
    }
    
    /**
     * User collapses node
     * @param {string} nodeName - Node name to collapse
     */
    async userCollapsesNode(nodeName) {
        // Same as expand - toggle
        await this.userExpandsNode(nodeName);
    }
}

module.exports = WhenE2EHelper;
