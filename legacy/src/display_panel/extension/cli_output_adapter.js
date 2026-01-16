class CLIOutputAdapter {

  adapt(rawOutput) {
    console.log('[ADAPTER] adapt() called, rawOutput length:', rawOutput?.length || 0);
    // First, try to parse as JSON (CLI outputs JSON after header text when using --format json)
    const jsonStartIndex = rawOutput.indexOf('{');
    if (jsonStartIndex >= 0) {
      const jsonText = rawOutput.substring(jsonStartIndex);
      try {
        const jsonData = JSON.parse(jsonText);
        console.log('[ADAPTER] Successfully parsed JSON format');
        return this._adaptFromJson(jsonData);
      } catch (e) {
        console.log('[ADAPTER] JSON parse failed, falling back to text format:', e.message);
      }
    }
    
    // Fallback: parse text format
    console.log('[ADAPTER] Using text format parsing');
    return this._adaptFromText(rawOutput);
  }

  _adaptFromJson(jsonData) {
    // Adapt from JSON format returned by CLI
    console.log('[ADAPTER] Adapting JSON data:', {
      bot: jsonData.bot?.name,
      behaviors: jsonData.behaviors?.length,
      scope: jsonData.scope?.type,
      instructionsKeys: jsonData.instructions ? Object.keys(jsonData.instructions) : []
    });
    
    const botInfo = jsonData.bot || { name: 'unknown bot', botDirectory: '', workspaceName: '', workspaceDirectory: '' };
    
    return {
      bot: botInfo,
      behaviors: jsonData.behaviors || [],
      session: jsonData.session || { currentPosition: '', currentBehavior: '', currentAction: '', actionPhase: '', progressPath: '' },
      scope: this._adaptScopeFromJson(jsonData.scope),
      instructions: jsonData.instructions || {},
      parameters: jsonData.parameters || [],
      runExamples: jsonData.runExamples || [],
      commands: jsonData.commands || { text: '', list: [] }
    };
  }

  _adaptScopeFromJson(scopeData) {
    if (!scopeData) {
      return { type: 'all', filter: 'all (entire project)', content: null, graphLinks: [] };
    }
    
    // Convert JSON scope format to panel format
    const graphLinks = [];
    if (scopeData.links) {
      if (scopeData.links.graph) graphLinks.push({ text: 'Graph', url: scopeData.links.graph });
      if (scopeData.links.map) graphLinks.push({ text: 'map', url: scopeData.links.map });
    }
    
    if ((scopeData.type === 'story' || scopeData.type === 'showAll') && scopeData.storyGraph && scopeData.storyGraph.epics) {
      console.log('[ADAPTER] Processing story graph with', scopeData.storyGraph.epics.length, 'epics');
      // Helper function to process a sub-epic (can be nested)
      const processSubEpic = (subEpic) => {
        // Collect stories from both story_groups and direct stories array
        const allStories = [];
        if (subEpic.story_groups) {
          subEpic.story_groups.forEach(group => {
            if (group.stories) allStories.push(...group.stories);
          });
        }
        if (subEpic.stories) {
          allStories.push(...subEpic.stories);
        }
        
        // Sub-epic: Use test_link if available (already constructed by backend), 
        // otherwise build from test_file
        const subEpicTestFile = subEpic.test_file;
        let subEpicTestLink = null;
        if (subEpic.test_link) {
          // Backend already constructed the full path
          subEpicTestLink = subEpic.test_link;
        } else if (subEpicTestFile) {
          // Check if test_file already contains a path
          if (subEpicTestFile.startsWith('agile_bot/') || subEpicTestFile.includes('/')) {
            // Already a full path, use it directly
            subEpicTestLink = subEpicTestFile;
          } else {
            // Just filename, prepend path
            subEpicTestLink = `agile_bot/bots/base_bot/test/${subEpicTestFile}`;
          }
        }
        
        // Process nested sub_epics if they exist
        const nestedFeatures = (subEpic.sub_epics || []).map(nestedSubEpic => processSubEpic(nestedSubEpic));
        
        console.log(`[ADAPTER] Processing sub-epic: ${subEpic.name}, has ${subEpic.sub_epics?.length || 0} nested sub-epics, generated ${nestedFeatures.length} nested features`);
        
        return {
          icon: '⚙️',
          type: 'feature',
          name: subEpic.name,
          links: subEpicTestLink ? [{ text: 'Test', url: subEpicTestLink }] : [],
          features: nestedFeatures.length > 0 ? nestedFeatures : undefined,
          stories: allStories.map(story => {
            // Story: Build test link from sub-epic test link/file + test_class
            // Stories do NOT have test_file, only test_class
            let storyTestLink = null;
            if (story.test_link) {
              // Backend already constructed the full path
              storyTestLink = story.test_link;
            } else if (subEpicTestLink && story.test_class) {
              // Use sub-epic test link + test_class
              storyTestLink = `${subEpicTestLink}#${story.test_class}`;
            }
            
            return {
              icon: '📝',
              type: 'story',
              name: story.name,
              storyFile: story.story_file,
              storyFileExists: story.story_file_exists,
              testClass: story.test_class,
            links: [
              ...(story.story_file && story.story_file_exists ? [{ text: 'Story', url: story.story_file }] : []),
                ...(storyTestLink ? [{ text: 'Test', url: storyTestLink }] : [])
            ],
              scenarios: (story.scenarios || []).map(scenario => {
                // Scenario: Build test link from sub-epic test link/file + test_method
                // Scenarios inherit test_file from sub-epic, NOT from story
                let scenarioTestLink = null;
                if (scenario.test_file) {
                  // Backend already constructed the full path with test_method
                  scenarioTestLink = scenario.test_file;
                } else if (subEpicTestLink && scenario.test_method) {
                  // Use sub-epic test link + test_method
                  scenarioTestLink = `${subEpicTestLink}#${scenario.test_method}`;
                }
                
                return {
                  name: scenario.name,
                  test_method: scenario.test_method,
                  test_file: scenarioTestLink  // Full relative path with #test_method
                };
              })
            };
          })
        };
      };
      
      // Convert story graph epics to panel format
      const epics = scopeData.storyGraph.epics.map(epic => {
        console.log(`[ADAPTER] Epic: ${epic.name}, has ${epic.sub_epics?.length || 0} sub-epics`);
        return {
          icon: '💡',
          type: 'epic',
          name: epic.name,
          features: (epic.sub_epics || []).map(subEpic => processSubEpic(subEpic))
        };
      });
      
      return {
        type: scopeData.type,  // Keep original type ('story' or 'showAll')
        filter: scopeData.filter || '',
        graphLinks: graphLinks,
        content: epics
      };
    } else if (scopeData.type === 'files' || scopeData.type === 'FILES') {
      return {
        type: 'files',
        filter: scopeData.filter || '',
        graphLinks: graphLinks,
        content: scopeData.files || []
      };
    } else {
      return {
        type: 'all',
        filter: scopeData.filter || 'all (entire project)',
        graphLinks: graphLinks,
        content: null
      };
    }
  }

  _adaptFromText(rawOutput) {
    // Original text parsing logic (fallback)
    const botInfo = this._extractBotInfo(rawOutput);
    
    return {
      bot: botInfo,
      behaviors: this._extractBehaviorsHierarchy(rawOutput),
      session: this._extractSessionState(rawOutput),
      scope: this._extractScopeSection(rawOutput),
      instructions: this._extractInstructions(rawOutput),
      parameters: this._extractParameters(rawOutput),
      runExamples: this._extractRunExamples(rawOutput),
      commands: this._extractCommands(rawOutput)
    };
  }

  _extractBotInfo(rawOutput) {
    // AC: WHEN CLI outputs bot section THEN panel reads bot name
    // Match: ## 🤖 Bot: story_bot or ## Bot: story_bot
    const botMatch = /##\s*[^\n]*?Bot:\s*(.+)/m.exec(rawOutput);
    const botName = botMatch ? botMatch[1].trim() : null;
    
    // AC: WHEN CLI outputs bot section THEN panel reads bot directory path
    const botPathMatch = /\*\*Bot Path:\*\*[^\n]*\n\s*```\s*\n\s*(.+?)\s*\n\s*```/s.exec(rawOutput);
    const botDirectory = botPathMatch ? botPathMatch[1].trim() : '';
    
    // AC: WHEN CLI outputs bot section THEN panel reads workspace name AND workspace directory path
    // Match: 📂 **Workspace:** base_bot or **Workspace:** base_bot
    const workspaceMatch = /\*\*Workspace:\*\*\s+(.+?)\s*\n\s*```\s*(.+?)```/s.exec(rawOutput);
    const workspaceName = workspaceMatch ? workspaceMatch[1].trim() : '';
    const workspaceDirectory = workspaceMatch ? workspaceMatch[2].trim() : '';
    
    // AC: WHEN bot section is missing THEN panel shows "unknown bot" message
    return {
      name: botName || 'unknown bot',
      botDirectory: botDirectory,
      workspaceName: workspaceName,
      workspaceDirectory: workspaceDirectory
    };
  }

  _extractBehaviorsHierarchy(rawOutput) {
    // Extract section starting with ## 📍 **Progress** (with emoji)
    const progressSection = this._extractSection(rawOutput, '##.*Progress', '────');
    if (!progressSection) return [];
    const lines = progressSection.split('\n');
    const behaviors = [];
    let currentBehavior = null;
    let currentAction = null;
    for (const line of lines) {
      // Match behavior: "[*] shape - Description" or "[ ] shape" or "- ➤ shape"
      // Support both text format [*]/[ ] and unicode ➤☑☐
      if (/^\[[\*\s\-]\] \w+/.test(line) || /^- [➤☑☐] \w+/.test(line)) {
        const match = /^(?:\[([\*\s\-])\]|- ([➤☑☐])) (\w+)(?:\s+-\s+(.+))?/.exec(line);
        if (match) {
          const marker = match[1] || match[2]; // Either [*] style or ➤ style
          const isCurrent = marker === '*' || marker === '➤';
          const isCompleted = marker === '-' || marker === '☑';
          currentBehavior = {
            name: match[3],
            description: match[4] || '',
            isCurrent: isCurrent,
            isCompleted: isCompleted,
            status: isCurrent ? 'current' : (isCompleted ? 'completed' : 'pending'),
            actions: []
          };
          behaviors.push(currentBehavior);
          currentAction = null;
        }
      }
      // Match action: "  [*] clarify" or "  - ☑ clarify"
      else if (/^  \[[\*\s\-]\] \w+/.test(line) || /^  - [➤☑☐] \w+/.test(line)) {
        const match = /^  (?:\[([\*\s\-])\]|- ([➤☑☐])) (\w+)(?:\s+-\s+(.+))?/.exec(line);
        if (match && currentBehavior) {
          const marker = match[1] || match[2];
          const isCurrent = marker === '*' || marker === '➤';
          const isCompleted = marker === '-' || marker === '☑';
          currentAction = {
            name: match[3],
            description: match[4] || '',
            isCurrent: isCurrent,
            isCompleted: isCompleted,
            status: isCurrent ? 'current' : (isCompleted ? 'completed' : 'pending'),
            operations: []
          };
          currentBehavior.actions.push(currentAction);
        }
      }
      // Match operation: "    [*] instructions" or "    - ➤ instructions"
      else if (/^    \[[\*\s\-]\] \w+/.test(line) || /^    - [➤☑☐] \w+/.test(line)) {
        const match = /^    (?:\[([\*\s\-])\]|- ([➤☑☐])) (\w+)(?:\s+-\s+(.+))?/.exec(line);
        if (match && currentAction) {
          const marker = match[1] || match[2];
          const isCurrent = marker === '*' || marker === '➤';
          const isCompleted = marker === '-' || marker === '☑';
          currentAction.operations.push({
            name: match[3],
            description: match[4] || '',
            isCurrent: isCurrent,
            isCompleted: isCompleted,
            status: isCurrent ? 'current' : (isCompleted ? 'completed' : 'pending')
          });
        }
      }
    }
    return behaviors;
  }

  _extractSessionState(rawOutput) {
    // Match the code block after the Progress header (without "Current Position:" label)
    const positionMatch = /##\s+[^\n]*\*\*Progress\*\*[^\n]*\n+```\s*(.+?)\s*```/s.exec(rawOutput);
    if (!positionMatch) {
      return { currentPosition: '', currentBehavior: '', currentAction: '', actionPhase: '', progressPath: '' };
    }
    const position = positionMatch[1].trim();
    const parts = position.split('.');
    return {
      currentPosition: position,
      currentBehavior: parts[0] || '',
      currentAction: parts[1] || '',
      actionPhase: parts[2] || '',
      progressPath: parts.slice(0, 2).join('.')
    };
  }

  _extractScopeSection(rawOutput) {
    // AC: Extract scope section from CLI output
    // Try JSON format first (when CLI uses --format json)
    const scopeJsonMatch = /##\s*[^\n]*\*\*Scope\*\*[^\n]*\n```json\s*\n([\s\S]+?)\n```/m.exec(rawOutput);
    
    console.log('[SCOPE DEBUG] Looking for JSON scope block...');
    console.log('[SCOPE DEBUG] JSON Match found:', !!scopeJsonMatch);
    
    if (scopeJsonMatch) {
      try {
        console.log('[SCOPE DEBUG] Parsing JSON:', scopeJsonMatch[1].substring(0, 200));
        const scopeData = JSON.parse(scopeJsonMatch[1]);
        console.log('[SCOPE DEBUG] Parsed scope data:', scopeData);
    
        // Clean up filter value - remove --filter flag and quotes if present
        let filterValue = scopeData.filter || '';
        filterValue = filterValue.replace(/^--filter\s+/, '');  // Remove --filter prefix
        filterValue = filterValue.replace(/^["'](.*)["']$/, '$1');  // Remove surrounding quotes
        filterValue = filterValue.trim();
    
        // Convert JSON format to existing panel format
        const graphLinks = [];
        if (scopeData.links) {
          if (scopeData.links.graph) {
            graphLinks.push({ text: 'Graph', url: scopeData.links.graph });
          }
          if (scopeData.links.map) {
            graphLinks.push({ text: 'map', url: scopeData.links.map });
          }
        }
        
        // Determine type and content based on JSON structure
        if (scopeData.type === 'files' || scopeData.type === 'FILES') {
          return {
            type: 'files',
            filter: filterValue,
            graphLinks: graphLinks,
            content: scopeData.files || []
          };
        } else if (scopeData.storyGraph && scopeData.storyGraph.epics) {
          // Helper function to process a sub-epic (can be nested)
          const processSubEpic = (subEpic) => {
            // Collect stories from both story_groups and direct stories array
            const allStories = [];
            
            // Get stories from story_groups
            if (subEpic.story_groups && Array.isArray(subEpic.story_groups)) {
              subEpic.story_groups.forEach(group => {
                if (group.stories && Array.isArray(group.stories)) {
                  allStories.push(...group.stories);
                }
              });
            }
            
            // Get stories directly at sub_epic level
            if (subEpic.stories && Array.isArray(subEpic.stories)) {
              allStories.push(...subEpic.stories);
            }
            
            // Sub-epic: Use test_link if available (already constructed by backend), 
            // otherwise build from test_file
            const subEpicTestFile = subEpic.test_file;
            let subEpicTestLink = null;
            if (subEpic.test_link) {
              // Backend already constructed the full path
              subEpicTestLink = subEpic.test_link;
            } else if (subEpicTestFile) {
              // Check if test_file already contains a path
              if (subEpicTestFile.startsWith('agile_bot/') || subEpicTestFile.includes('/')) {
                // Already a full path, use it directly
                subEpicTestLink = subEpicTestFile;
              } else {
                // Just filename, prepend path
                subEpicTestLink = `agile_bot/bots/base_bot/test/${subEpicTestFile}`;
              }
            }
            
            // Process nested sub_epics if they exist
            const nestedFeatures = (subEpic.sub_epics || []).map(nestedSubEpic => processSubEpic(nestedSubEpic));
            
            return {
              icon: '⚙️',
              type: 'feature',
              name: subEpic.name,
              links: subEpicTestLink ? [{ text: 'Test', url: subEpicTestLink }] : [],
              features: nestedFeatures.length > 0 ? nestedFeatures : undefined,
              stories: allStories.map(story => {
                const storyLinks = [];
                
                // Debug: Log story properties
                console.log(`Story: ${story.name}, has story_file: ${!!story.story_file}, story_file_exists: ${story.story_file_exists}, story_file value: ${story.story_file}`);
                
                // Use story_file from JSON if available and exists
                if (story.story_file && story.story_file_exists) {
                  console.log(`Adding story link for ${story.name}: ${story.story_file}`);
                  storyLinks.push({ text: 'Story', url: story.story_file });
                }
                
                // Add test link: Use story.test_link if available, otherwise build from sub-epic + test_class
                if (story.test_link) {
                  // Backend already constructed the full path
                  storyLinks.push({ text: 'Test', url: story.test_link });
                } else if (subEpicTestLink && story.test_class) {
                  // Use sub-epic test link + test_class
                  const storyTestLink = `${subEpicTestLink}#${story.test_class}`;
                  storyLinks.push({ text: 'Test', url: storyTestLink });
                }
                
                console.log(`Story ${story.name} final links:`, storyLinks);
                
                return {
                  icon: '📝',
                  type: 'story',
                  name: story.name,
                  storyFile: story.story_file,
                  storyFileExists: story.story_file_exists,
                  testClass: story.test_class,
                  links: storyLinks,
                  scenarios: (story.scenarios || []).map(scenario => {
                    // Scenario: Use scenario.test_file if available, otherwise build from sub-epic + test_method
                    let scenarioTestLink = null;
                    if (scenario.test_file) {
                      // Backend already constructed the full path with test_method
                      scenarioTestLink = scenario.test_file;
                    } else if (subEpicTestLink && scenario.test_method) {
                      // Use sub-epic test link + test_method
                      scenarioTestLink = `${subEpicTestLink}#${scenario.test_method}`;
                    }
                    
                    return {
                      name: scenario.name,
                      test_method: scenario.test_method,
                      test_file: scenarioTestLink  // Full relative path with #test_method
                    };
                  })
                };
              })
            };
          };
          
          // Convert story graph epics to panel format
          const epics = (scopeData.storyGraph.epics || []).map(epic => ({
            icon: 'lightbulb',
            type: 'epic',
            name: epic.name,
            features: (epic.sub_epics || []).map(subEpic => processSubEpic(subEpic))
          }));
          
          const result = {
            type: 'story',
            filter: filterValue,
            graphLinks: graphLinks,
            content: epics
          };
          console.log('[SCOPE DEBUG] Returning story scope with', epics.length, 'epics');
          console.log('[SCOPE DEBUG] First epic:', epics[0]);
          return result;
        } else {
          // Type is 'all' or unknown
          return {
            type: 'all',
            filter: filterValue || 'all (entire project)',
            graphLinks: graphLinks,
            content: null
          };
    }
      } catch (e) {
        // JSON parse failed, fall back to text parsing
        console.error('[SCOPE DEBUG] Failed to parse scope JSON:', e);
      }
    }
    
    // Fallback: Parse text format scope section
    console.log('[SCOPE DEBUG] No JSON found, trying text format parsing...');
    const scopeSectionMatch = /##\s*[🎯]*\s*\*\*Scope\*\*[\s\S]*?\n([\s\S]+?)(?=\n\s*[-─=]{30,}\s*\n|$)/i.exec(rawOutput);
    
    if (scopeSectionMatch) {
      const scopeText = scopeSectionMatch[1];
      console.log('[SCOPE DEBUG] Found text scope section, length:', scopeText.length);
      
      // Extract filter from first line
      const filterMatch = /\*\*Filter:\*\*\s*(.+?)(?:\||$)/i.exec(scopeText);
      const filterValue = filterMatch ? filterMatch[1].trim() : 'all (entire project)';
      
      // Extract graph links
      const graphLinks = [];
      const graphLinkMatch = /\[Graph\]\(([^)]+)\)/i.exec(scopeText);
      if (graphLinkMatch) graphLinks.push({ text: 'Graph', url: graphLinkMatch[1] });
      const mapLinkMatch = /\[map\]\(([^)]+)\)/i.exec(scopeText);
      if (mapLinkMatch) graphLinks.push({ text: 'map', url: mapLinkMatch[1] });
      
      // Check if it's a story tree (has emojis like 🎯, ⚙️, 📝)
      if (/[🎯⚙️📝]/.test(scopeText)) {
        const epics = this._extractStoryTree(scopeText);
        return {
          type: 'story',
          filter: filterValue,
          graphLinks: graphLinks,
          content: epics
        };
      } else if (scopeText.includes('Files in scope:')) {
        const files = this._extractFileList(scopeText);
        return {
          type: 'files',
          filter: filterValue,
          graphLinks: graphLinks,
          content: files
        };
      } else {
        return {
          type: 'all',
          filter: filterValue,
          graphLinks: graphLinks,
          content: null
        };
      }
    }
    
    // No scope found at all - return default
    console.log('[SCOPE DEBUG] No scope section found');
    return { type: 'all', filter: 'all (entire project)', content: null, graphLinks: [] };
  }

  _extractStoryTree(scopeSection) {
    const epics = [];
    const lines = scopeSection.split('\n');
    let currentEpic = null;
    let currentFeature = null;
    for (const line of lines) {
      if (/🎯/.test(line) && !line.includes('Current Scope:')) {
        const name = line.replace(/^[^🎯]*🎯 /, '').trim();
        currentEpic = { icon: 'lightbulb', type: 'epic', name: name, features: [] };
        epics.push(currentEpic);
        currentFeature = null;
      }
      else if (/⚙️/.test(line) && currentEpic) {
        const match = /⚙️ (.+?)(?:\s*\|)?/.exec(line);
        if (match) {
          currentFeature = { icon: '⚙️', type: 'feature', name: match[1].trim(), links: this._extractLinks(line), stories: [] };
          currentEpic.features.push(currentFeature);
        }
      }
      else if (/📝/.test(line) && currentFeature) {
        const nameMatch = /📝 (.+?)[\]\|]/.exec(line);
        if (nameMatch) {
          currentFeature.stories.push({ icon: '📝', type: 'story', name: nameMatch[1].trim(), links: this._extractLinks(line) });
        }
      }
    }
    return epics;
  }

  _extractFileList(scopeSection) {
    const files = [];
    const lines = scopeSection.split('\n');
    let inFileList = false;
    for (const line of lines) {
      if (line.includes('Files in scope:')) {
        inFileList = true;
        continue;
      }
      if (inFileList && line.trim().startsWith('- ')) {
        const path = line.trim().substring(2).trim();
        files.push({ path: path, type: path.split('.').pop() });
      }
    }
    return files;
  }

  _extractLinks(text) {
    const links = [];
    const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
    let match;
    while ((match = linkRegex.exec(text)) !== null) {
      links.push({ text: match[1], url: match[2] });
    }
    return links;
  }

  _extractInstructions(rawOutput) {
    console.log('[INSTRUCTIONS DEBUG] Attempting to extract instructions...');
    console.log('[INSTRUCTIONS DEBUG] Raw output length:', rawOutput.length);
    
    // First try to find JSON format in code block (when --format json is used)
    // Look for ```json block within INSTRUCTIONS SECTION
    const instructionsSectionMatch = /\*\*INSTRUCTIONS SECTION:\*\*[\s\S]*?```json\s*\n([\s\S]+?)\n```/m.exec(rawOutput);
    
    if (instructionsSectionMatch) {
      try {
        console.log('[INSTRUCTIONS DEBUG] Found JSON code block, parsing...');
        const instructionsJson = JSON.parse(instructionsSectionMatch[1]);
        console.log('[INSTRUCTIONS DEBUG] Successfully parsed instructions JSON:', instructionsJson);
        return instructionsJson;
      } catch (e) {
        console.error('[INSTRUCTIONS DEBUG] Failed to parse instructions JSON:', e);
        console.log('[INSTRUCTIONS DEBUG] Raw JSON text:', instructionsSectionMatch[1].substring(0, 500));
      }
    }
    
    console.log('[INSTRUCTIONS DEBUG] No JSON format found, trying text extraction...');
    
    // Fallback: Extract as plain text (for non-JSON format)
    const instructionsMatch = /\*\*INSTRUCTIONS SECTION:\*\*[\s\S]*?[━─=\-]{30,}\s*\n([\s\S]+?)\n\s*[━═=\-]{30,}\s*\n+\s*\*\*\*?\s*CLI STATUS/i.exec(rawOutput);
    if (instructionsMatch) {
      const extracted = instructionsMatch[1].trim();
      console.log('[INSTRUCTIONS DEBUG] Text match found! Length:', extracted.length);
      console.log('[INSTRUCTIONS DEBUG] First 500 chars:', extracted.substring(0, 500));
      console.log('[INSTRUCTIONS DEBUG] Contains "Behavior Instructions"?', extracted.includes('Behavior Instructions'));
      console.log('[INSTRUCTIONS DEBUG] Contains "Action Instructions"?', extracted.includes('Action Instructions'));
      return extracted;
    }
    
    console.log('[INSTRUCTIONS DEBUG] No instructions found - regex did not match');
    console.log('[INSTRUCTIONS DEBUG] Looking for INSTRUCTIONS SECTION header:', rawOutput.includes('INSTRUCTIONS SECTION'));
    console.log('[INSTRUCTIONS DEBUG] Looking for CLI STATUS:', rawOutput.includes('CLI STATUS'));
    return '';
  }

  _extractParameters(rawOutput) {
    const argsSection = this._extractCodeBlock(rawOutput, 'Args:');
    if (!argsSection) return [];
    const parameters = [];
    const lines = argsSection.split('\n');
    for (const line of lines) {
      const match = /^(--\S+)\s*(?:"([^"]+)")?\s*#\s*(.+)/.exec(line.trim());
      if (match) {
        parameters.push({ flag: match[1], syntax: match[2] || '', description: match[3] });
      }
    }
    return parameters;
  }

  _extractRunExamples(rawOutput) {
    const runSection = this._extractCodeBlock(rawOutput, 'Run:');
    if (!runSection) return [];
    const examples = [];
    const lines = runSection.split('\n');
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('//')) continue;
      const parts = trimmed.split('#');
      examples.push({ command: parts[0].trim(), description: parts[1] ? parts[1].trim() : '' });
    }
    return examples;
  }


  _extractCommands(rawOutput) {
    const commandMatch = /Commands[^\n]*\*\*(.+?)\*\*/s.exec(rawOutput);
    if (!commandMatch) return { text: '', list: [] };
    const commandText = commandMatch[1].trim();
    const commandList = commandText.split('|').map(cmd => cmd.trim());
    return { text: commandText, list: commandList };
  }

  _extractSection(text, startMarker, endMarker) {
    const startRegex = new RegExp(startMarker, 'i');
    const startMatch = startRegex.exec(text);
    if (!startMatch) return null;
    const startPos = startMatch.index + startMatch[0].length;
    const remaining = text.substring(startPos);
    const endRegex = new RegExp(endMarker, 'i');
    const endMatch = endRegex.exec(remaining);
    if (endMatch) return remaining.substring(0, endMatch.index);
    return remaining;
  }

  _extractCodeBlock(text, precedingText) {
    const regex = new RegExp(precedingText + '\\s*```[^`]*?\\n([\\s\\S]+?)```', 'i');
    const match = regex.exec(text);
    return match ? match[1].trim() : null;
  }
}

module.exports = CLIOutputAdapter;
