/**
 * Base class for all panel views.
 * Provides CLI command execution via a persistent Python process.
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');
const vscode = require("vscode");
const branding = require('./branding');

// Shared log path - set when PanelView is created with bot path (workspace root)
let _panelLogPath = null;

function _getPanelLogPath() {
    return _panelLogPath || path.join(process.cwd(), 'panel-debug.log');
}

function _perfLog(msg) {
    const ts = new Date().toISOString();
    try {
        fs.appendFileSync(_getPanelLogPath(), `${ts} [PERF] ${msg}\n`);
    } catch (_) {}
    console.log(`[PERF] ${msg}`);
}

/**
 * Check if a path is a temp directory
 */
function isTempPath(filePath) {
    if (!filePath) return false;
    const normalized = path.resolve(filePath);
    const tempDir = os.tmpdir();
    return normalized.startsWith(tempDir);
}

/**
 * Check if a path is the production repo root
 * This is used to prevent tests from accidentally using production paths
 */
function isProductionRepoPath(filePath) {
    if (!filePath) return false;
    const normalized = path.resolve(filePath);
    // Check if it's the repo root by looking for src/ and test/ directories
    return fs.existsSync(path.join(normalized, 'src')) && 
           fs.existsSync(path.join(normalized, 'test')) &&
           fs.existsSync(path.join(normalized, 'bots'));
}

// End-of-response marker that Python CLI sends after each JSON response
const END_MARKER = '<<<END_OF_RESPONSE>>>';

/**
 * Sanitize JSON string by removing invalid control characters.
 * JSON only allows \n (0x0A), \r (0x0D), and \t (0x09) as control characters.
 * All other control characters (0x00-0x1F) are invalid and will cause parse errors.
 * 
 * @param {string} jsonString - JSON string that may contain invalid control characters
 * @returns {string} Sanitized JSON string
 */
function sanitizeJsonString(jsonString) {
    if (typeof jsonString !== 'string') {
        return jsonString;
    }
    
    // Remove invalid control characters (0x00-0x1F) except \n (0x0A), \r (0x0D), \t (0x09)
    // This regex matches control chars but preserves newlines, carriage returns, and tabs
    return jsonString.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g, '');
}

class PanelView {
    /**
     * Static logging method for panel views
     * @param {string} message - Message to log
     */
    static _log(message) {
        console.log(message);
    }
    
    /**
     * Create a PanelView.
     * @param {string|PanelView} botPathOrCli - Full path to bot directory, or CLI instance to reuse
     */
    constructor(botPathOrCli) {
        if (botPathOrCli && typeof botPathOrCli === 'object') {
            // CLI instance passed - reuse it
            this._cli = botPathOrCli;
            this._botPath = null;
            this._workspaceDir = null;
            this._pythonProcess = null;
        } else {
            // Bot path passed - create own CLI
            this._cli = null;
            this._botPath = botPathOrCli || process.env.BOT_DIRECTORY;
            // Derive workspace from bot path (bot is at workspace/bots/botname)
            const path = require('path');
            this._workspaceDir = path.resolve(this._botPath, '..', '..');
            this._pythonProcess = null;
            // Use workspace root for panel-debug.log (same as bot_panel)
            _panelLogPath = path.join(this._workspaceDir, 'panel-debug.log');
        }
        this._pendingResolve = null;
        this._pendingReject = null;
        this._responseBuffer = '';
        // Serialize CLI commands to prevent interleaved responses
        this._commandQueue = Promise.resolve();
    }
    
    /**
     * Spawn the persistent Python CLI process
     */
    _spawnProcess() {
        if (this._pythonProcess) {
            return;
        }
        const tSpawnStart = performance.now();
        _perfLog('_spawnProcess START');
        
        const cliPath = path.join(this._workspaceDir, 'src', 'cli', 'cli_main.py');
        
        if (!fs.existsSync(cliPath)) {
            throw new Error(`CLI script not found at: ${cliPath}`);
        }
        
        // PYTHONPATH must point to agile_bots src/test directories
        // _workspaceDir is the agile_bots root (derived from bot path)
        const srcDir = path.join(this._workspaceDir, 'src');
        const testDir = path.join(this._workspaceDir, 'test');
        const pythonPath = `${srcDir}${path.delimiter}${testDir}${path.delimiter}${this._workspaceDir}`;
        
        // DON'T set WORKING_AREA here - let Python load it from bot_config.json
        // The Python BotPath class loads WORKING_AREA from:
        // 1. bot_config.json (mcp.env.WORKING_AREA) - preferred
        // 2. Environment variable (fallback)
        // Only pass through existing env WORKING_AREA if explicitly set by tests
        const envWorkingArea = process.env.WORKING_AREA;
        
        const env = {
            ...process.env,
            PYTHONPATH: pythonPath,
            BOT_DIRECTORY: this._botPath,
            CLI_MODE: 'json',
            SUPPRESS_CLI_HEADER: '1',            
            IDE: vscode.env.uriScheme.toLowerCase().includes('cursor') ? 'cursor' : 'vscode'
        };
                
        let pythonExe = os.platform().includes('darwin') ? 'python3' : 'python';
        if (fs.existsSync(path.join(this._workspaceDir, '.venv', 'bin'))) {            
            pythonExe = path.join(this._workspaceDir, '.venv', 'bin', 'python');
        }
        else if (fs.existsSync(path.join(this._workspaceDir, '.venv', 'Scripts'))) {            
            pythonExe = path.join(this._workspaceDir, '.venv', 'Scripts', 'python.exe');
        }
        else {
            console.log("Could not find Python virtual environment in workspace. Falling back to system Python.");
        }
        
        this._pythonProcess = spawn(pythonExe, [cliPath], {        
            cwd: this._workspaceDir,
            env: env,
            stdio: ['pipe', 'pipe', 'pipe']
        });
        
        _perfLog(`_spawnProcess DONE: ${(performance.now() - tSpawnStart).toFixed(0)}ms`);
        
        this._pythonProcess.stdout.on('data', (data) => {
            const dataStr = data.toString();
            this._responseBuffer += dataStr;
            
            // Log first chunk received with timing
            if (this._responseBuffer.length === dataStr.length) {
                const elapsed = this._perfExecuteStart ? (performance.now() - this._perfExecuteStart).toFixed(0) : '?';
                _perfLog(`First chunk received: ${dataStr.length} bytes, ${elapsed}ms since execute start`);
            }
            
            const markerIndex = this._responseBuffer.indexOf(END_MARKER);
            if (markerIndex !== -1) {
                const elapsed = this._perfExecuteStart ? (performance.now() - this._perfExecuteStart).toFixed(0) : '?';
                _perfLog(`END_MARKER received, response size ${markerIndex}, ${elapsed}ms since execute start`);
                const jsonOutput = this._responseBuffer.substring(0, markerIndex).trim();
                this._responseBuffer = this._responseBuffer.substring(markerIndex + END_MARKER.length);
                
                if (this._pendingResolve) {
                    try {
                        const tParseStart = performance.now();
                        const jsonMatch = jsonOutput.match(/\{[\s\S]*\}/);
                        if (!jsonMatch) {
                            console.error('[PanelView] No JSON found in CLI output');
                            this._pendingReject(new Error('No JSON found in CLI output'));
                        } else {
                            // Sanitize JSON string to remove invalid control characters
                            const rawJson = jsonMatch[0];
                            const sanitizedJson = sanitizeJsonString(rawJson);
                            
                            // Log if sanitization removed characters (for debugging)
                            if (rawJson.length !== sanitizedJson.length) {
                                const removed = rawJson.length - sanitizedJson.length;
                                console.warn(`[PanelView] Removed ${removed} invalid control character(s) from JSON response`);
                            }
                            
                            const jsonData = JSON.parse(sanitizedJson);
                            _perfLog(`JSON parse done: ${(performance.now() - tParseStart).toFixed(0)}ms, size ${jsonOutput.length}`);
                            
                            // Check if response indicates an error from CLI
                            if (jsonData.status === 'error' && jsonData.error) {
                                console.error('[PanelView] CLI returned error:', jsonData.error);
                                // Resolve with the error object so it can be handled gracefully
                                this._pendingResolve(jsonData);
                            } else {
                                console.log('[PanelView] Command executed successfully, response keys:', Object.keys(jsonData));
                                this._pendingResolve(jsonData);
                            }
                        }
                    } catch (parseError) {
                        console.error('[PanelView] JSON parse error:', parseError.message);
                        console.error('[PanelView] JSON parse error stack:', parseError.stack);
                        // Log a sample of the JSON that failed to parse (first 500 chars)
                        const jsonMatch = jsonOutput.match(/\{[\s\S]*\}/);
                        if (jsonMatch) {
                            const sample = jsonMatch[0].substring(0, 500);
                            console.error('[PanelView] Failed JSON sample:', sample);
                        }
                        this._pendingReject(new Error(`Failed to parse CLI JSON: ${parseError.message}`));
                    }
                    this._pendingResolve = null;
                    this._pendingReject = null;
                }
            }
        });
        
        this._pythonProcess.stderr.on('data', (data) => {
            console.error('[PanelView] Python stderr:', data.toString());
        });
        
        this._pythonProcess.on('error', (err) => {
            console.error('[PanelView] Python process error:', err);
            this._pythonProcess = null;
            if (this._pendingReject) {
                this._pendingReject(new Error(`Python process error: ${err.message}`));
                this._pendingResolve = null;
                this._pendingReject = null;
            }
        });
        
        this._pythonProcess.on('close', (code) => {
            console.log('[PanelView] Python process closed with code:', code);
            this._pythonProcess = null;
            if (this._pendingReject) {
                this._pendingReject(new Error(`Python process exited unexpectedly (code ${code})`));
                this._pendingResolve = null;
                this._pendingReject = null;
            }
        });
    }
    
    /**
     * Cleanup - kill the Python process and remove all event listeners
     */
    cleanup() {
        if (this._pythonProcess) {
            console.log('[PanelView] Killing Python process');
            
            // Remove all event listeners to prevent keeping event loop alive
            if (this._pythonProcess.stdout) {
                this._pythonProcess.stdout.removeAllListeners();
                this._pythonProcess.stdout.destroy();
            }
            if (this._pythonProcess.stderr) {
                this._pythonProcess.stderr.removeAllListeners();
                this._pythonProcess.stderr.destroy();
            }
            if (this._pythonProcess.stdin) {
                this._pythonProcess.stdin.removeAllListeners();
                this._pythonProcess.stdin.end();
            }
            
            // Remove process-level listeners
            this._pythonProcess.removeAllListeners();
            
            // Kill the process
            this._pythonProcess.kill('SIGTERM');
            
            // Force kill after a short delay if still running
            setTimeout(() => {
                if (this._pythonProcess && !this._pythonProcess.killed) {
                    console.log('[PanelView] Force killing Python process');
                    this._pythonProcess.kill('SIGKILL');
                }
            }, 100);
            
            this._pythonProcess = null;
            this._pendingResolve = null;
            this._pendingReject = null;
            this._responseBuffer = '';
        }
    }
    
    /**
     * Execute command using the persistent Python process.
     */
    async execute(command) {
        const runCommand = async () => {
            // Delegate to injected CLI if present
            if (this._cli) {
                return this._cli.execute(command);
            }
            
            if (!this._pythonProcess) {
                this._spawnProcess();
            }
            
            const perfCmdStart = performance.now();
            this._perfExecuteStart = perfCmdStart;
            _perfLog(`execute START: "${command}"`);
            
            // Increase timeout for scope/status/copy_json (scope/status enrich scenarios; copy_json can be slow on large graphs)
            const needsLongTimeout = command.includes('scope') || command.includes('status') || command.includes('copy_json');
            const timeoutMs = needsLongTimeout ? 120000 : 30000;
            console.log(`[PanelView] Using timeout: ${timeoutMs}ms for command: "${command}"`);
            
            return new Promise((resolve, reject) => {
                this._pendingResolve = resolve;
                this._pendingReject = reject;
                
                const timeoutId = setTimeout(() => {
                    if (this._pendingReject) {
                        console.error(`[PanelView] Command timed out after ${timeoutMs}ms: "${command}"`);
                        this._pendingReject(new Error(`Command timed out after ${timeoutMs / 1000} seconds: ${command}`));
                        this._pendingResolve = null;
                        this._pendingReject = null;
                    }
                }, timeoutMs);
                
                const originalResolve = resolve;
                const originalReject = reject;
                this._pendingResolve = (value) => {
                    clearTimeout(timeoutId);
                    const perfCmdEnd = performance.now();
                    _perfLog(`execute DONE: "${command}" in ${(perfCmdEnd - perfCmdStart).toFixed(0)}ms`);
                    this._perfExecuteStart = null;
                    originalResolve(value);
                };
                this._pendingReject = (err) => {
                    clearTimeout(timeoutId);
                    const perfCmdEnd = performance.now();
                    _perfLog(`execute FAILED: "${command}" after ${(perfCmdEnd - perfCmdStart).toFixed(0)}ms`);
                    this._perfExecuteStart = null;
                    originalReject(err);
                };
                
                try {
                    const cmd = command.includes('--format json') ? command : `${command} --format json`;
                    const tBeforeWrite = performance.now();
                    this._pythonProcess.stdin.write(cmd + '\n');
                    _perfLog(`stdin.write sent: ${(performance.now() - tBeforeWrite).toFixed(0)}ms, ${(performance.now() - perfCmdStart).toFixed(0)}ms since start`);
                } catch (err) {
                    clearTimeout(timeoutId);
                    this._pendingResolve = null;
                    this._pendingReject = null;
                    reject(new Error(`Failed to send command: ${err.message}`));
                }
            });
        };

        const previous = this._commandQueue;
        const queued = previous.then(() => runCommand());
        // Keep queue alive even if a command fails
        this._commandQueue = queued.catch(() => {});
        return queued;
    }
}

PanelView.getPanelLogPath = _getPanelLogPath;
module.exports = PanelView;
