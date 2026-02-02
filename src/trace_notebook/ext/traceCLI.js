// @ts-check
const { spawn } = require('child_process');
const path = require('path');

/**
 * Client for Python trace CLI daemon via stdio JSON.
 */
class TraceCLI {
    constructor(workspaceRoot) {
        this.workspaceRoot = workspaceRoot;
        this.process = null;
        this.pending = new Map(); // requestId -> {resolve, reject}
        this.requestId = 0;
        this.buffer = '';
        this.initialized = false;
        this._initPromise = null;
    }

    async init() {
        if (this.initialized) return;
        if (this._initPromise) return this._initPromise;

        this._initPromise = this._doInit();
        return this._initPromise;
    }

    async _doInit() {
        // Spawn Python CLI as daemon
        this.process = spawn('python', ['-m', 'src.trace_notebook.cli.trace_cli'], {
            cwd: this.workspaceRoot,
            stdio: ['pipe', 'pipe', 'pipe']
        });

        this.process.stdout.on('data', (data) => this._onData(data.toString()));
        this.process.stderr.on('data', (data) => console.error('[TraceCLI]', data.toString()));
        this.process.on('error', (err) => console.error('[TraceCLI] Process error:', err));
        this.process.on('exit', (code) => {
            console.log('[TraceCLI] Process exited:', code);
            this.initialized = false;
            this.process = null;
        });

        // Initialize workspace
        const result = await this._send({ cmd: 'init', workspace: this.workspaceRoot });
        this.initialized = !result.error;
        return result;
    }

    /**
     * Resolve story name to test class/methods.
     * @param {string} storyName
     */
    resolveStory(storyName) {
        return this._send({ cmd: 'resolve_story', storyName });
    }

    /**
     * Expand a node to get child references.
     * @param {string} nodeId
     * @param {number} offset
     * @param {number} limit
     */
    expand(nodeId, offset = 0, limit = 8) {
        return this._send({ cmd: 'expand', nodeId, offset, limit });
    }

    /**
     * Get story graph.
     */
    getStoryGraph() {
        return this._send({ cmd: 'get_story_graph' });
    }

    dispose() {
        if (this.process) {
            this.process.kill();
            this.process = null;
        }
    }

    /** @private */
    _send(cmd) {
        return new Promise((resolve, reject) => {
            if (!this.process) {
                reject(new Error('CLI not running'));
                return;
            }

            const id = ++this.requestId;
            cmd._id = id;
            this.pending.set(id, { resolve, reject });

            const line = JSON.stringify(cmd) + '\n';
            this.process.stdin.write(line);

            // Timeout after 30s
            setTimeout(() => {
                if (this.pending.has(id)) {
                    this.pending.delete(id);
                    reject(new Error('CLI timeout'));
                }
            }, 30000);
        });
    }

    /** @private */
    _onData(data) {
        this.buffer += data;
        const lines = this.buffer.split('\n');
        this.buffer = lines.pop() || '';

        for (const line of lines) {
            if (!line.trim()) continue;
            try {
                const result = JSON.parse(line);
                const id = result._id;
                if (id && this.pending.has(id)) {
                    const { resolve } = this.pending.get(id);
                    this.pending.delete(id);
                    resolve(result);
                }
            } catch (e) {
                console.error('[TraceCLI] Parse error:', e, line);
            }
        }
    }
}

module.exports = { TraceCLI };
