/**
 * BotView - Main panel orchestrator that wraps bot JSON and displays all domain views.
 * 
 * Epic: Invoke Bot Through Panel
 * Sub-Epic: Manage Panel Session
 * Story: Open Panel, Display Session Status
 */

const PanelView = require('./panel_view');
const BotHeaderView = require('./bot_header_view');
const BehaviorsView = require('./behaviors_view');
const StoryMapView = require('./story_map_view');
const InstructionsSection = require('./instructions_view');
const fs = require('fs');
const path = require('path');

// Simple file logger - uses same path as bot_panel (workspace root)
function log(msg) {
    const timestamp = new Date().toISOString();
    try {
        const logFile = PanelView.getPanelLogPath ? PanelView.getPanelLogPath() : path.join(process.cwd(), 'panel-debug.log');
        fs.appendFileSync(logFile, `${timestamp} ${msg}\n`);
    } catch (e) {
        // Ignore
    }
    console.log(msg);
}

class BotView extends PanelView {
    /**
     * Main panel orchestrator.
     * 
     * @param {string|PanelView} botPathOrCli - Bot path or CLI instance
     * @param {string} panelVersion - Panel extension version (optional)
     * @param {Object} webview - VS Code webview instance (optional)
     * @param {Object} extensionUri - Extension URI (optional)
     */
    constructor(botPathOrCli, panelVersion, webview, extensionUri) {
        super(botPathOrCli);
        this.panelVersion = panelVersion || null;
        this.webview = webview || null;
        this.extensionUri = extensionUri || null;
        this.botData = null; // Cached bot data - populated during render
        
        // Initialize domain views - pass 'this' so they can access this.botData
        this.headerView = new BotHeaderView(botPathOrCli, this.panelVersion, webview, extensionUri, this);
        this.behaviorsView = new BehaviorsView(botPathOrCli, webview, extensionUri, this);
        this.storyMapView = new StoryMapView(botPathOrCli, webview, extensionUri, this);
        this.instructionsSection = new InstructionsSection(botPathOrCli, webview, extensionUri, this);
    }
    
    /**
     * Render complete bot view HTML.
     * 
     * @returns {Promise<string>} Complete HTML string
     */
    async render() {
        // ===== PERFORMANCE: BotView render =====
        const perfRenderStart = performance.now();
        log('[BotView] Starting render');
        
        // Fetch bot data ONCE and cache it for all child views
        // Skip fetch if botData is already cached (e.g., from navigation)
        const perfFetchStart = performance.now();
        try {
            if (!this.botData) {
                log('[BotView] No cached botData, fetching status');
                this.botData = await this.execute('status');
            } else {
                log('[BotView] Using cached botData, skipping status fetch');
                log('[BotView] Cached botData keys: ' + Object.keys(this.botData).join(', '));
                log('[BotView] Has instructions? ' + (this.botData.instructions ? 'YES - keys: ' + Object.keys(this.botData.instructions).join(', ') : 'NO'));
            }
            // Validate botData has required fields
            if (!this.botData) {
                throw new Error('Status command returned null/undefined bot data');
            }
            if (!this.botData.name && !this.botData.bot_name) {
                log(`[BotView] WARNING: Bot data missing name field. Keys: ${Object.keys(this.botData).join(', ')}`);
                log(`[BotView] Bot data structure: ${JSON.stringify(this.botData).substring(0, 500)}`);
            }
        } catch (error) {
            log(`[BotView] ERROR fetching bot data: ${error.message}`);
            log(`[BotView] ERROR stack: ${error.stack}`);
            throw error;
        }
        const perfFetchEnd = performance.now();
        log(`[BotView] [PERF] Fetch bot data (status): ${(perfFetchEnd - perfFetchStart).toFixed(2)}ms`);
        
        // Header
        const perfHeaderStart = performance.now();
        const header = await this.headerView.render();
        const perfHeaderEnd = performance.now();
        log(`[BotView] [PERF] Header render: ${(perfHeaderEnd - perfHeaderStart).toFixed(2)}ms`);
        
        // Behaviors
        const perfBehaviorsStart = performance.now();
        const behaviors = await this.behaviorsView.render();
        const perfBehaviorsEnd = performance.now();
        log(`[BotView] [PERF] Behaviors render: ${(perfBehaviorsEnd - perfBehaviorsStart).toFixed(2)}ms`);
        
        // Story map
        const perfStoryMapStart = performance.now();
        const storyMap = await this.storyMapView.render();
        const perfStoryMapEnd = performance.now();
        log(`[BotView] [PERF] Story map render: ${(perfStoryMapEnd - perfStoryMapStart).toFixed(2)}ms`);
        
        // Instructions
        const perfInstructionsStart = performance.now();
        const instructions = await this.instructionsSection.render();
        const perfInstructionsEnd = performance.now();
        log(`[BotView] [PERF] Instructions render: ${(perfInstructionsEnd - perfInstructionsStart).toFixed(2)}ms`);
        
        // Final assembly
        const perfAssemblyStart = performance.now();
        const finalHtml = `
            <div class="bot-view">
                ${header}
                ${behaviors}
                ${storyMap}
                ${instructions}
            </div>
        `;
        const perfAssemblyEnd = performance.now();
        log(`[BotView] [PERF] Final HTML assembly: ${(perfAssemblyEnd - perfAssemblyStart).toFixed(2)}ms`);
        
        const perfRenderEnd = performance.now();
        const totalRenderTime = (perfRenderEnd - perfRenderStart).toFixed(2);
        log(`[BotView] [PERF] TOTAL render() duration: ${totalRenderTime}ms`);
        return finalHtml;
    }
    
    /**
     * Execute command and return appropriate data.
     * Overrides PanelView.execute() to extract data from unified JSON response.
     * 
     * @param {string} command - Command to execute
     * @returns {Promise<Object>} Extracted data (bot JSON for status, unified response for actions)
     */
    async execute(command) {
        const response = await super.execute(command);
        
        // Check if response indicates an error from CLI
        if (response.status === 'error' && response.error) {
            const error = new Error(response.error);
            error.errorType = response.error_type;
            error.command = response.command;
            error.isCliError = true;
            throw error;
        }
        
        // In JSON mode, CLI returns unified structure: { execution?, instructions?, bot, scope? }
        // For "status" command, return bot data (response should be { bot: ... })
        if (command === 'status') {
            if (response.bot) {
                return response.bot;
            }
            // If response.bot is missing, check if response itself has bot data structure
            // (sometimes the response IS the bot data directly - legacy support)
            if (response.name || response.bot_name) {
                log(`[BotView] Status response is bot data directly (no .bot wrapper)`);
                return response;
            }
            // Log the actual response structure for debugging
            const responseKeys = Object.keys(response).join(', ');
            const responsePreview = JSON.stringify(response).substring(0, 500);
            log(`[BotView] ERROR: Status command response missing bot data. Response keys: ${responseKeys}`);
            log(`[BotView] Full response structure: ${responsePreview}`);
            // Check if this looks like a submit/action response that got mixed up
            if (response.status === 'success' && (response.behavior || response.action)) {
                log(`[BotView] WARNING: Status command returned what appears to be a submit/action response instead of bot data`);
                log(`[BotView] This may indicate a response buffering issue or command execution error`);
            }
            throw new Error(`Status command returned invalid response: missing bot data. Response structure: ${JSON.stringify(response).substring(0, 200)}`);
        }
        
        // For "scope" command, return scope data with bot
        if (command === 'scope' && response.scope) {
            return response;
        }
        
        // For action commands, return unified response (contains execution, instructions, bot)
        return response;
    }
    
    /**
     * Refresh data from CLI.
     * 
     * @returns {Promise<Object>} Updated bot JSON
     */
    async refresh() {
        // ===== PERFORMANCE: BotView refresh =====
        const perfRefreshStart = performance.now();
        log('[BotView] [PERF] refresh() START');
        
        // "status" command returns the Bot object itself
        try {
            log('[BotView] [PERF] refresh() calling execute("status")...');
            const tStatusStart = performance.now();
            const botJSON = await this.execute('status');
            log(`[BotView] [PERF] refresh() execute("status") DONE: ${(performance.now() - tStatusStart).toFixed(0)}ms`);
            // Update cached botData
            this.botData = botJSON;
            // Validate botData has required fields
            if (!botJSON) {
                throw new Error('Status command returned null/undefined bot data');
            }
            if (!botJSON.name && !botJSON.bot_name) {
                log(`[BotView] WARNING: Refresh returned bot data missing name field. Keys: ${Object.keys(botJSON).join(', ')}`);
            }
            
            // Also fetch instructions based on current behavior and action
            const currentBehavior = botJSON.behaviors?.current_behavior || botJSON.current_behavior;
            const currentAction = botJSON.behaviors?.current_action || botJSON.current_action;
            
            if (currentBehavior && currentAction) {
                log(`[BotView] [PERF] refresh() calling execute("${currentBehavior}.${currentAction}")...`);
                const tInstrStart = performance.now();
                try {
                    // Use the behavior.action command to get instructions
                    const instructionsResponse = await super.execute(`${currentBehavior}.${currentAction}`);
                    log(`[BotView] [PERF] refresh() execute("${currentBehavior}.${currentAction}") DONE: ${(performance.now() - tInstrStart).toFixed(0)}ms`);
                    if (instructionsResponse && instructionsResponse.instructions) {
                        this.botData.instructions = instructionsResponse.instructions;
                        // Also cache for InstructionsSection
                        PanelView._lastResponse = instructionsResponse;
                        log(`[BotView] Instructions loaded: ${Object.keys(instructionsResponse.instructions).join(', ')}`);
                    }
                } catch (instrError) {
                    log(`[BotView] WARNING: Could not fetch instructions: ${instrError.message}`);
                    // Don't fail the whole refresh for instructions
                }
            } else {
                log(`[BotView] No current behavior/action, skipping instructions fetch`);
            }
            
            const perfRefreshEnd = performance.now();
            const refreshDuration = (perfRefreshEnd - perfRefreshStart).toFixed(2);
            log(`[BotView] [PERF] refresh() (execute status + instructions) duration: ${refreshDuration}ms`);
            return botJSON;
        } catch (error) {
            log(`[BotView] ERROR in refresh(): ${error.message}`);
            log(`[BotView] ERROR stack: ${error.stack}`);
            throw error;
        }
    }
    
    /**
     * Handle user events.
     * 
     * @param {string} eventType - Type of event
     * @param {Object} eventData - Event data
     * @returns {Promise<Object>} Updated data or result
     */
    async handleEvent(eventType, eventData) {
        switch (eventType) {
            case 'refresh':
                return await this.refresh();
            case 'executeBehavior':
                return await this.behaviorsView.handleEvent('execute', eventData);
            case 'updateScope':
                return await this.storyMapView.handleEvent('updateFilter', eventData);
            case 'updateWorkspace':
                return await this.headerView.handleEvent('updateWorkspace', eventData);
            case 'switchBot':
                return await this.headerView.handleEvent('switchBot', eventData);
            default:
                throw new Error(`Unknown event type: ${eventType}`);
        }
    }
}

module.exports = BotView;
