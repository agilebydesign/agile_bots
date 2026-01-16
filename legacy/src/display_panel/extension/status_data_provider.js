/**
 * Status Data Provider
 * 
 * Interfaces with Python REPL CLI to retrieve status information.
 * Spawns Python subprocess and sends 'status' command via stdin.
 */

const cp = require("child_process");
const path = require("path");
const fs = require("fs");
const Logger = require("./logger.js");

class StatusDataProvider {
  constructor(workspaceRoot) {
    this.workspaceRoot = workspaceRoot;
    this.timeout = 30000; // 30 second timeout
    
    // Track current workspace path (defaults to base_bot)
    this.currentWorkingArea = path.join(workspaceRoot, "agile_bot", "bots", "base_bot");
    
    // Track current bot (defaults to story_bot)
    this.currentBot = "story_bot";
    
    // Load bot registry
    this.botRegistry = this._loadBotRegistry();
    
    // Setup logger
    const logPath = path.join(workspaceRoot, "agile_bot", "bots", "base_bot", "logs", "panel-debug.log");
    this.logger = new Logger(logPath);
    this.logger.log("StatusDataProvider initialized", { workspaceRoot, botRegistry: this.botRegistry });
  }

  /**
   * Load bot registry from registry.json
   * @returns {Object} Bot registry mapping bot names to their configuration
   */
  _loadBotRegistry() {
    try {
      const registryPath = path.join(this.workspaceRoot, "agile_bot", "bots", "registry.json");
      const registryContent = fs.readFileSync(registryPath, "utf-8");
      return JSON.parse(registryContent);
    } catch (error) {
      console.error("Failed to load bot registry:", error);
      // Fallback to story_bot only
      return {
        story_bot: {
          cli_path: "agile_bot/bots/story_bot/src/story_bot_cli.py",
          repl_path: "agile_bot/bots/base_bot/src/repl_cli/repl_main.py"
        }
      };
    }
  }

  /**
   * Get current bot directory path
   * @returns {string} Path to current bot directory
   */
  _getBotDirectory() {
    return path.join(this.workspaceRoot, "agile_bot", "bots", this.currentBot);
  }

  /**
   * Get status data by calling REPL CLI
   * @returns {Promise<string>} Raw status text output from CLI
   */
  async getStatus() {
    this.logger.log("getStatus() called");
    
    return new Promise((resolve, reject) => {
      const replMainPath = path.join(
        this.workspaceRoot,
        "agile_bot",
        "bots",
        "base_bot",
        "src",
        "repl_cli",
        "repl_main.py"
      );

      // Set up environment variables for CLI
      const env = Object.assign({}, process.env, {
        PYTHONPATH: this.workspaceRoot,
        BOT_DIRECTORY: this._getBotDirectory(),
        WORKING_AREA: this.currentWorkingArea
      });

      this.logger.log("Spawning Python process", {
        replMainPath,
        cwd: this.workspaceRoot,
        env: {
          PYTHONPATH: env.PYTHONPATH,
          BOT_DIRECTORY: env.BOT_DIRECTORY,
          WORKING_AREA: env.WORKING_AREA
        }
      });

      // Spawn Python process with environment
      const pythonProcess = cp.spawn("python", [replMainPath], {
        cwd: this.workspaceRoot,
        timeout: this.timeout,
        env: env
      });

      let stdout = "";
      let stderr = "";
      let timedOut = false;

      // Set timeout
      const timeoutId = setTimeout(() => {
        timedOut = true;
        pythonProcess.kill();
        reject(new Error(`Python process timed out after ${this.timeout/1000} seconds`));
      }, this.timeout);

      // Send 'status --format json' command via stdin
      try {
        pythonProcess.stdin.write("status --format json\n");
        pythonProcess.stdin.end();
      } catch (err) {
        clearTimeout(timeoutId);
        this.logger.error("Failed to write to Python stdin", err);
        reject(new Error(`Failed to communicate with Python process: ${err.message}`));
        return;
      }

      // Collect stdout
      pythonProcess.stdout.on("data", (data) => {
        stdout += data.toString();
      });

      // Collect stderr
      pythonProcess.stderr.on("data", (data) => {
        stderr += data.toString();
      });

      // Handle process error
      pythonProcess.on("error", (err) => {
        clearTimeout(timeoutId);
        this.logger.error("Python process error", err);
        reject(new Error(`Python process error: ${err.message}`));
      });

      // Handle process completion
      pythonProcess.on("close", (code) => {
        clearTimeout(timeoutId);
        
        if (timedOut) {
          return; // Already rejected
        }

        this.logger.log("Python process closed", {
          exitCode: code,
          stdoutLength: stdout.length,
          stderrLength: stderr.length
        });

        if (stderr) {
          this.logger.log("STDERR output:", stderr);
        }

        if (code !== 0 && stderr) {
          this.logger.error("Python CLI failed", new Error(`Exit ${code}: ${stderr}`));
          reject(new Error(`Python CLI failed (exit ${code}): ${stderr}`));
          return;
        }

        if (!stdout || stdout.trim().length === 0) {
          this.logger.log("ERROR: No output from Python CLI");
          reject(new Error("No output from Python CLI"));
          return;
        }

        this.logger.log("Raw CLI output received (first 500 chars):", stdout.substring(0, 500));
        this.logger.log("Raw CLI output received (FULL OUTPUT):", stdout);
        resolve(stdout);
      });
    });
  }

  /**
   * Update scope filter by calling REPL CLI
   * @param {string} filterValue - The filter value (epic or story names)
   * @returns {Promise<string>} Result message from CLI
   */
  async updateScope(filterValue) {
    this.logger.log("updateScope() called", { filterValue });
    
    return new Promise((resolve, reject) => {
      const replMainPath = path.join(
        this.workspaceRoot,
        "agile_bot",
        "bots",
        "base_bot",
        "src",
        "repl_cli",
        "repl_main.py"
      );

      // Set up environment variables for CLI
      const env = Object.assign({}, process.env, {
        PYTHONPATH: this.workspaceRoot,
        BOT_DIRECTORY: this._getBotDirectory(),
        WORKING_AREA: this.currentWorkingArea
      });

      // Build scope command with filter
      // CLI expects: scope "Filter Value" (NOT scope --filter "Filter Value")
      const scopeCmd = filterValue && filterValue.trim() 
        ? `scope "${filterValue.replace(/"/g, '\\"')}"\n`
        : `scope all\n`;

      this.logger.log("Executing scope command", { scopeCmd });

      // Spawn Python process with environment
      const pythonProcess = cp.spawn("python", [replMainPath], {
        cwd: this.workspaceRoot,
        timeout: this.timeout,
        env: env
      });

      let stdout = "";
      let stderr = "";
      let timedOut = false;

      // Set timeout
      const timeoutId = setTimeout(() => {
        timedOut = true;
        pythonProcess.kill();
        reject(new Error(`Python process timed out after ${this.timeout/1000} seconds`));
      }, this.timeout);

      // Send scope command via stdin
      try {
        pythonProcess.stdin.write(scopeCmd);
        pythonProcess.stdin.end();
      } catch (err) {
        clearTimeout(timeoutId);
        this.logger.error("Failed to write to Python stdin", err);
        reject(new Error(`Failed to communicate with Python process: ${err.message}`));
        return;
      }

      // Collect stdout
      pythonProcess.stdout.on("data", (data) => {
        stdout += data.toString();
      });

      // Collect stderr
      pythonProcess.stderr.on("data", (data) => {
        stderr += data.toString();
      });

      // Handle process error
      pythonProcess.on("error", (err) => {
        clearTimeout(timeoutId);
        this.logger.error("Python process error", err);
        reject(new Error(`Python process error: ${err.message}`));
      });

      // Handle process completion
      pythonProcess.on("close", (code) => {
        clearTimeout(timeoutId);
        
        if (timedOut) {
          return; // Already rejected
        }

        this.logger.log("Python process closed", {
          exitCode: code,
          stdoutLength: stdout.length,
          stderrLength: stderr.length
        });

        if (stderr) {
          this.logger.log("STDERR output:", stderr);
        }

        if (code !== 0 && stderr) {
          this.logger.error("Scope update failed", new Error(`Exit ${code}: ${stderr}`));
          reject(new Error(`Scope update failed (exit ${code}): ${stderr}`));
          return;
        }

        this.logger.log("Scope filter updated successfully");
        resolve(stdout || "Scope filter updated");
      });
    });
  }

  /**
   * Update a question answer in clarification.json
   * @param {string} question - The question text
   * @param {string} answer - The answer text
   * @returns {Promise<string>} Result message
   */
  async updateQuestionAnswer(question, answer) {
    this.logger.log("updateQuestionAnswer() called", { question, answer });
    
    return new Promise((resolve, reject) => {
      const fs = require('fs');
      const clarificationPath = path.join(
        this.workspaceRoot,
        "docs",
        "stories",
        "clarification.json"
      );

      try {
        // Read current clarification.json
        let clarificationData = {};
        if (fs.existsSync(clarificationPath)) {
          const fileContent = fs.readFileSync(clarificationPath, 'utf8');
          clarificationData = JSON.parse(fileContent);
        }

        // Find the appropriate phase and update the answer
        // Navigate through shape/discovery/exploration phases
        let updated = false;
        for (const phase of ['shape', 'discovery', 'exploration']) {
          if (clarificationData[phase] && 
              clarificationData[phase].key_questions && 
              clarificationData[phase].key_questions.answers) {
            const answers = clarificationData[phase].key_questions.answers;
            if (answers.hasOwnProperty(question)) {
              answers[question] = answer;
              updated = true;
              this.logger.log(`Updated answer in ${phase} phase`);
              break;
            }
          }
        }

        if (!updated) {
          // If question not found in any phase, add to shape phase by default
          if (!clarificationData.shape) {
            clarificationData.shape = {};
          }
          if (!clarificationData.shape.key_questions) {
            clarificationData.shape.key_questions = { answers: {} };
          }
          if (!clarificationData.shape.key_questions.answers) {
            clarificationData.shape.key_questions.answers = {};
          }
          clarificationData.shape.key_questions.answers[question] = answer;
          this.logger.log('Added new answer to shape phase');
        }

        // Write back to file
        const updatedContent = JSON.stringify(clarificationData, null, 2);
        fs.writeFileSync(clarificationPath, updatedContent, 'utf8');
        
        this.logger.log('Successfully updated clarification.json');
        resolve('Answer updated successfully');
      } catch (err) {
        this.logger.error('Failed to update question answer', err);
        reject(new Error(`Failed to update clarification.json: ${err.message}`));
      }
    });
  }

  /**
   * Update workspace path by calling REPL CLI
   * @param {string} workspacePath - The new workspace path
   * @returns {Promise<string>} Result message from CLI
   */
  async updateWorkspace(workspacePath) {
    this.logger.log("updateWorkspace() called", { workspacePath });
    
    return new Promise((resolve, reject) => {
      const replMainPath = path.join(
        this.workspaceRoot,
        "agile_bot",
        "bots",
        "base_bot",
        "src",
        "repl_cli",
        "repl_main.py"
      );

      // Set up environment variables for CLI
      const env = Object.assign({}, process.env, {
        PYTHONPATH: this.workspaceRoot,
        BOT_DIRECTORY: this._getBotDirectory(),
        WORKING_AREA: this.currentWorkingArea
      });

      // Build path command
      const pathCmd = `path "${workspacePath.replace(/"/g, '\\"')}"\n`;

      this.logger.log("Executing path command", { pathCmd });

      // Spawn Python process with environment
      const pythonProcess = cp.spawn("python", [replMainPath], {
        cwd: this.workspaceRoot,
        timeout: this.timeout,
        env: env
      });

      let stdout = "";
      let stderr = "";
      let timedOut = false;

      // Set timeout
      const timeoutId = setTimeout(() => {
        timedOut = true;
        pythonProcess.kill();
        reject(new Error(`Python process timed out after ${this.timeout/1000} seconds`));
      }, this.timeout);

      // Send path command via stdin
      try {
        pythonProcess.stdin.write(pathCmd);
        pythonProcess.stdin.end();
      } catch (err) {
        clearTimeout(timeoutId);
        this.logger.error("Failed to write to Python stdin", err);
        reject(new Error(`Failed to communicate with Python process: ${err.message}`));
        return;
      }

      // Collect stdout
      pythonProcess.stdout.on("data", (data) => {
        stdout += data.toString();
      });

      // Collect stderr
      pythonProcess.stderr.on("data", (data) => {
        stderr += data.toString();
      });

      // Handle process error
      pythonProcess.on("error", (err) => {
        clearTimeout(timeoutId);
        this.logger.error("Python process error", err);
        reject(new Error(`Python process error: ${err.message}`));
      });

      // Handle process completion
      pythonProcess.on("close", (code) => {
        clearTimeout(timeoutId);
        
        if (timedOut) {
          return; // Already rejected
        }

        this.logger.log("Python process closed", {
          exitCode: code,
          stdoutLength: stdout.length,
          stderrLength: stderr.length
        });

        if (stderr) {
          this.logger.log("STDERR output:", stderr);
        }

        if (code !== 0 && stderr) {
          this.logger.error("Workspace update failed", new Error(`Exit ${code}: ${stderr}`));
          reject(new Error(`Workspace update failed (exit ${code}): ${stderr}`));
          return;
        }

        // Save the new workspace path for future CLI calls
        this.currentWorkingArea = workspacePath;
        
        this.logger.log("Workspace path updated successfully", { newPath: workspacePath });
        resolve(stdout || "Workspace path updated");
      });
    });
  }

  /**
   * Execute a command through the REPL CLI
   * @param {string} commandText - The command to execute
   * @returns {Promise<string>} Result output from CLI
   */
  async executeCommand(commandText) {
    this.logger.log("executeCommand() called", { commandText });
    
    return new Promise((resolve, reject) => {
      const replMainPath = path.join(
        this.workspaceRoot,
        "agile_bot",
        "bots",
        "base_bot",
        "src",
        "repl_cli",
        "repl_main.py"
      );

      // Set up environment variables for CLI
      const env = Object.assign({}, process.env, {
        PYTHONPATH: this.workspaceRoot,
        BOT_DIRECTORY: this._getBotDirectory(),
        WORKING_AREA: this.currentWorkingArea
      });

      this.logger.log("Executing command via REPL", { commandText });

      // Spawn Python process with environment
      const pythonProcess = cp.spawn("python", [replMainPath], {
        cwd: this.workspaceRoot,
        timeout: this.timeout,
        env: env
      });

      let stdout = "";
      let stderr = "";
      let timedOut = false;

      // Set timeout
      const timeoutId = setTimeout(() => {
        timedOut = true;
        pythonProcess.kill();
        reject(new Error(`Command execution timed out after ${this.timeout/1000} seconds`));
      }, this.timeout);

      // Send command via stdin
      try {
        pythonProcess.stdin.write(commandText + "\n");
        pythonProcess.stdin.end();
      } catch (err) {
        clearTimeout(timeoutId);
        this.logger.error("Failed to write command to stdin", err);
        reject(new Error(`Failed to send command: ${err.message}`));
        return;
      }

      // Collect stdout
      pythonProcess.stdout.on("data", (data) => {
        stdout += data.toString();
      });

      // Collect stderr
      pythonProcess.stderr.on("data", (data) => {
        stderr += data.toString();
      });

      // Handle process error
      pythonProcess.on("error", (err) => {
        clearTimeout(timeoutId);
        this.logger.error("Python process error during command execution", err);
        reject(new Error(`Failed to execute command: ${err.message}`));
      });

      // Handle process exit
      pythonProcess.on("close", (code) => {
        clearTimeout(timeoutId);

        this.logger.log("Command execution completed", {
          exitCode: code,
          stdoutLength: stdout.length,
          stderrLength: stderr.length
        });

        if (stderr) {
          this.logger.log("STDERR output:", stderr);
        }

        if (code !== 0 && stderr) {
          this.logger.error("Command execution failed", new Error(`Exit ${code}: ${stderr}`));
          reject(new Error(`Command failed (exit ${code}): ${stderr}`));
          return;
        }

        this.logger.log("Command executed successfully");
        resolve(stdout || "Command executed");
      });
    });
  }

  /**
   * Switch to a different bot
   * @param {string} botName - Name of the bot to switch to
   * @returns {boolean} True if successful
   */
  switchBot(botName) {
    if (!this.botRegistry[botName]) {
      this.logger.error(`Bot not found in registry: ${botName}`);
      return false;
    }
    
    this.currentBot = botName;
    this.logger.log(`Switched to bot: ${botName}`);
    return true;
  }

  /**
   * Get available bots from registry
   * @returns {Array<string>} Array of bot names
   */
  getAvailableBots() {
    return Object.keys(this.botRegistry);
  }

  /**
   * Get current bot name
   * @returns {string} Current bot name
   */
  getCurrentBot() {
    return this.currentBot;
  }

  /**
   * Check if Python and REPL CLI are available
   * @returns {Promise<boolean>} True if available
   */
  async checkAvailability() {
    return new Promise((resolve) => {
      try {
        const pythonCheck = cp.spawn("python", ["--version"]);
        pythonCheck.on("close", (code) => {
          this.logger.log("Python availability check", { exitCode: code });
          resolve(code === 0);
        });
        pythonCheck.on("error", () => {
          this.logger.log("Python not found");
          resolve(false);
        });
      } catch (err) {
        this.logger.error("Availability check error", err);
        resolve(false);
      }
    });
  }
}

module.exports = StatusDataProvider;
