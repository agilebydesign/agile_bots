/**
 * Status Parser
 * 
 * Parses raw CLI status text output into structured data object.
 * Handles behavior hierarchy, scope, and commands.
 */

class StatusParser {
  /**
   * Parse CLI status output into structured data
   * @param {string} output - Raw CLI status text
   * @returns {object} Structured status data
   */
  parse(output) {
    const lines = output.split("\n");
    
    const result = {
      header: {
        botName: "",
        botPath: "",
        workingArea: "",
      },
      behaviors: [],
      scope: {
        filter: "",
        links: [],
      },
      commands: "",
    };

    let currentSection = "header";
    let currentBehavior = null;
    let currentAction = null;
    let inCodeBlock = false;

    for (const line of lines) {
      const trimmed = line.trim();
      
      // Skip empty lines and code block markers
      if (trimmed === "" || trimmed === "```") {
        if (trimmed === "```") {
          inCodeBlock = !inCodeBlock;
        }
        continue;
      }

      // Skip lines inside code blocks
      if (inCodeBlock) {
        continue;
      }

      // Parse header section
      if (trimmed.includes("CLI") && !result.header.botName) {
        result.header.botName = trimmed;
        continue;
      }
      if (trimmed.startsWith("Bot Path:")) {
        result.header.botPath = trimmed.replace("Bot Path:", "").trim();
        continue;
      }
      if (trimmed.startsWith("Working Area:")) {
        result.header.workingArea = trimmed.replace("Working Area:", "").trim();
        continue;
      }

      // Parse behaviors, actions, and operations
      const hierarchyMatch = trimmed.match(/^(\[\*?\])\s+(.+)$/);
      if (hierarchyMatch) {
        const isCurrent = hierarchyMatch[1] === "[*]";
        const name = hierarchyMatch[2];
        
        // Determine depth by leading spaces
        const leadingSpaces = line.search(/\S/);
        
        if (leadingSpaces >= 8) {
          // Operation (8+ spaces)
          if (currentAction) {
            currentAction.operations.push({ name, isCurrent });
          }
        } else if (leadingSpaces >= 4) {
          // Action (4+ spaces)
          if (currentBehavior) {
            const action = { name, isCurrent, operations: [] };
            currentBehavior.actions.push(action);
            currentAction = action;
          }
        } else {
          // Behavior (0-3 spaces)
          currentBehavior = { name, isCurrent, actions: [] };
          result.behaviors.push(currentBehavior);
          currentAction = null;
        }
        continue;
      }

      // Parse scope section
      if (trimmed.startsWith("## 🎯") || trimmed.includes("Scope")) {
        currentSection = "scope";
        continue;
      }
      if (currentSection === "scope" && trimmed.startsWith("**Filter:**")) {
        const filterText = trimmed.replace("**Filter:**", "").trim();
        
        // Extract filter and links
        const linkMatch = filterText.match(/^(.+?)(\s+\|.+)?$/);
        if (linkMatch) {
          let filterValue = linkMatch[1].trim();
          
          // Strip out "--filter" flag if present
          filterValue = filterValue.replace(/^--filter\s+/, "");
          
          // Remove quotes if present
          filterValue = filterValue.replace(/^["'](.+)["']$/, "$1");
          
          result.scope.filter = filterValue;
          
          // Parse links if present
          if (linkMatch[2]) {
            const linkParts = linkMatch[2].split("|");
            for (const part of linkParts) {
              const linkTextMatch = part.match(/\[([^\]]+)\]\(([^)]+)\)/);
              if (linkTextMatch) {
                result.scope.links.push({
                  text: linkTextMatch[1],
                  path: linkTextMatch[2],
                });
              }
            }
          }
        }
        continue;
      }


      // Parse commands footer
      if (trimmed.startsWith("## 💻") || trimmed.startsWith("Commands:")) {
        currentSection = "commands";
        continue;
      }
      if (currentSection === "commands" && trimmed.includes("|")) {
        result.commands = trimmed.replace(/^\*\*(.+?)\*\*$/, "$1");
        continue;
      }
    }

    return result;
  }

  /**
   * Validate parsed data structure
   * @param {object} data - Parsed status data
   * @returns {boolean} True if valid
   */
  validate(data) {
    if (!data || typeof data !== "object") return false;
    if (!data.header || typeof data.header !== "object") return false;
    if (!Array.isArray(data.behaviors)) return false;
    if (!data.scope || typeof data.scope !== "object") return false;
    return true;
  }
}

module.exports = StatusParser;
