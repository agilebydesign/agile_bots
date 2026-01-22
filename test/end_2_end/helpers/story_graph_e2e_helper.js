/**
 * Story Graph E2E Helper
 * 
 * Handles story graph setup and manipulation for E2E tests
 * Mirrors: test/domain/helpers/story_helper.py
 */

const BaseE2EHelper = require('./base_e2e_helper');
const fs = require('fs');
const path = require('path');

class StoryGraphE2EHelper extends BaseE2EHelper {
    /**
     * Create story graph file in workspace
     * @param {Object} graphData - Story graph data (default: {epics: []})
     * @returns {string} Path to created story graph file
     */
    createStoryGraph(graphData = null) {
        if (graphData === null) {
            graphData = { epics: [] };
        }
        
        const docsDir = path.join(this.workspace, 'docs', 'stories');
        fs.mkdirSync(docsDir, { recursive: true });
        
        const storyGraphFile = path.join(docsDir, 'story-graph.json');
        fs.writeFileSync(storyGraphFile, JSON.stringify(graphData, null, 2), 'utf-8');
        
        return storyGraphFile;
    }
    
    /**
     * Create story graph with single epic
     * @param {string} epicName - Epic name
     * @returns {Object} Story graph data
     */
    givenStoryGraphWithEpic(epicName) {
        const graphData = {
            epics: [
                {
                    name: epicName,
                    sequential_order: 0,
                    sub_epics: [],
                    story_groups: []
                }
            ]
        };
        this.createStoryGraph(graphData);
        return graphData;
    }
    
    /**
     * Create story graph with epic and sub-epic
     * @param {string} epicName - Epic name
     * @param {string} subEpicName - Sub-Epic name
     * @param {Object} options - Additional options (hasChildren, childType)
     * @returns {Object} Story graph data
     */
    givenStoryGraphWithSubEpic(epicName, subEpicName, options = {}) {
        const subEpic = {
            name: subEpicName,
            sequential_order: 0,
            sub_epics: [],
            story_groups: []
        };
        
        // Add children if specified
        if (options.hasChildren && options.childType === 'sub-epic') {
            subEpic.sub_epics.push({
                name: options.childName || 'Nested SubEpic',
                sequential_order: 0,
                sub_epics: [],
                story_groups: []
            });
        } else if (options.hasChildren && options.childType === 'story') {
            subEpic.story_groups.push({
                name: '',
                sequential_order: 0,
                type: 'and',
                connector: null,
                stories: [{
                    name: options.childName || 'Story',
                    sequential_order: 0,
                    connector: null,
                    users: ['User'],
                    story_type: 'user',
                    scenarios: [],
                    scenario_outlines: [],
                    acceptance_criteria: []
                }]
            });
        }
        
        const graphData = {
            epics: [
                {
                    name: epicName,
                    sequential_order: 0,
                    sub_epics: [subEpic],
                    story_groups: []
                }
            ]
        };
        this.createStoryGraph(graphData);
        return graphData;
    }
    
    /**
     * Create story graph with epic, sub-epic, and story
     * @param {string} epicName - Epic name
     * @param {string} subEpicName - Sub-Epic name
     * @param {string} storyName - Story name
     * @returns {Object} Story graph data
     */
    givenStoryGraphWithStory(epicName, subEpicName, storyName) {
        return this.givenStoryGraphWithSubEpic(epicName, subEpicName, {
            hasChildren: true,
            childType: 'story',
            childName: storyName
        });
    }
    
    /**
     * Read current story graph from file
     * @returns {Object} Story graph data
     */
    readStoryGraph() {
        const content = fs.readFileSync(this.storyGraphPath, 'utf-8');
        return JSON.parse(content);
    }
    
    /**
     * Verify epic exists in story graph file
     * @param {string} epicName - Epic name to verify
     * @returns {Object|null} Epic object or null if not found
     */
    assertEpicExists(epicName) {
        const graph = this.readStoryGraph();
        return graph.epics.find(e => e.name === epicName);
    }
    
    /**
     * Verify sub-epic exists under epic
     * @param {string} epicName - Parent epic name
     * @param {string} subEpicName - Sub-epic name to verify
     * @returns {Object|null} Sub-epic object or null if not found
     */
    assertSubEpicExists(epicName, subEpicName) {
        const epic = this.assertEpicExists(epicName);
        if (!epic) return null;
        return epic.sub_epics.find(se => se.name === subEpicName);
    }
}

module.exports = StoryGraphE2EHelper;
