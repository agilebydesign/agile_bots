/**
 * Simple file logger for debugging the extension
 */
const fs = require("fs");
const path = require("path");

class Logger {
  constructor(logPath) {
    this.logPath = logPath;
    this.ensureLogDir();
    this.log("=== NEW SESSION ===");
  }

  ensureLogDir() {
    const dir = path.dirname(this.logPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  }

  log(message, data = null) {
    const timestamp = new Date().toISOString();
    let logLine = `[${timestamp}] ${message}`;
    
    if (data !== null) {
      if (typeof data === "string") {
        logLine += `\n${data}`;
      } else {
        logLine += `\n${JSON.stringify(data, null, 2)}`;
      }
    }
    
    logLine += "\n\n";
    
    fs.appendFileSync(this.logPath, logLine);
  }

  error(message, error) {
    this.log(`ERROR: ${message}`, {
      message: error.message,
      stack: error.stack
    });
  }
}

module.exports = Logger;
