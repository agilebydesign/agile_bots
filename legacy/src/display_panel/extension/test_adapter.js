/**
 * Standalone test for CLIOutputAdapter
 * Run with: node test_adapter.js
 */

const CLIOutputAdapter = require('./cli_output_adapter.js');

// Sample JSON output from CLI (what --format json returns)
const sampleJsonOutput = `============================================================
STORY_BOT CLI
============================================================
**   AI AGENT INSTRUCTIONS - PIPED MODE  **
[!]  DO NOT echo this instructions section back to the user [!]

============================================================

{
  "bot": {
    "name": "story_bot",
    "botDirectory": "C:\\\\dev\\\\augmented-teams\\\\agile_bot\\\\bots\\\\story_bot",
    "workspaceName": "base_bot",
    "workspaceDirectory": "C:\\\\dev\\\\augmented-teams\\\\agile_bot\\\\bots\\\\base_bot"
  },
  "behaviors": [
    {
      "name": "shape",
      "description": "Outline a story map made up of epics, sub-epics, and stories",
      "isCurrent": true,
      "isCompleted": false,
      "status": "current",
      "actions": [
        {
          "name": "clarify",
          "description": "Gather context by asking required questions",
          "isCurrent": true,
          "isCompleted": false,
          "status": "current",
          "operations": [
            {
              "name": "instructions",
              "description": "",
              "isCurrent": true,
              "isCompleted": false,
              "status": "current"
            },
            {
              "name": "confirm",
              "description": "",
              "isCurrent": false,
              "isCompleted": false,
              "status": "pending"
            }
          ]
        },
        {
          "name": "build",
          "description": "Build knowledge graph",
          "isCurrent": false,
          "isCompleted": false,
          "status": "pending",
          "operations": []
        }
      ]
    },
    {
      "name": "tests",
      "description": "Generate BDD tests",
      "isCurrent": false,
      "isCompleted": false,
      "status": "pending",
      "actions": []
    }
  ],
  "session": {
    "currentPosition": "shape.clarify.instructions",
    "currentBehavior": "shape",
    "currentAction": "clarify",
    "actionPhase": "instructions",
    "progressPath": "shape.clarify"
  },
  "scope": {
    "type": "story",
    "filter": "Build MCP Tools",
    "links": {
      "graph": "agile_bot/bots/base_bot/docs/stories/story-graph.json",
      "map": "agile_bot/bots/base_bot/docs/stories/story-map.drawio"
    },
    "storyGraph": {
      "epics": [
        {
          "name": "Build Agile Bots",
          "sub_epics": [
            {
              "name": "Generate MCP Tools",
              "test_link": "agile_bot/bots/base_bot/test/test_generate_mcp_tools.py",
              "story_groups": [
                {
                  "stories": [
                    {
                      "name": "Generate Bot Tools",
                      "story_file": "agile_bot/bots/base_bot/docs/stories/map/story1.md",
                      "story_file_exists": true,
                      "test_file": "agile_bot/bots/base_bot/test/test_generate_mcp_tools.py",
                      "test_class": "TestGenerateBotTools",
                      "test_link": "agile_bot/bots/base_bot/test/test_generate_mcp_tools.py#L100"
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  },
  "instructions": {
    "text": "Please generate the MCP tools for the story bot.",
    "scope": null
  },
  "parameters": [
    {
      "flag": "--scope",
      "syntax": "Epic, Story",
      "description": "Filter by story names"
    }
  ],
  "runExamples": [
    {
      "command": "echo 'behavior.action' | python repl_main.py",
      "description": "Defaults to instructions operation"
    }
  ],
  "commands": {
    "text": "status | back | current | next | path [dir] | scope [filter] | help | exit",
    "list": ["status", "back", "current", "next", "path", "scope", "help", "exit"]
  }
}`;

// Sample text output from CLI (fallback format)
const sampleTextOutput = `============================================================

## 🤖 Bot: story_bot
**Bot Path:**
\`\`\`
C:\\dev\\augmented-teams\\agile_bot\\bots\\story_bot
\`\`\`

📂 **Workspace:** base_bot
\`\`\`
C:\\dev\\augmented-teams\\agile_bot\\bots\\base_bot
\`\`\`

------------------------------------------------------------
## 🎯 **Scope**
**Filter:** Build MCP Tools | [Graph](agile_bot/bots/base_bot/docs/stories/story-graph.json) | [map](agile_bot/bots/base_bot/docs/stories/story-map.drawio)

🎯 Build Agile Bots
  │   ├── ⚙️ Generate MCP Tools | [Test](test.py)
│   │   ├── [📝 Generate Bot Tools](story.md) | [Test](test.py#L100)

------------------------------------------------------------
## 📍 **Progress**
\`\`\`
shape.clarify.instructions
\`\`\`

[*] shape - Outline a story map
  [*] clarify - Gather context
    [*] instructions
    [ ] confirm
  [ ] build - Build knowledge graph
[ ] tests - Generate BDD tests

------------------------------------------------------------
## 💻 **Commands:**
**status | back | current | next | path [dir] | scope [filter] | help | exit**
`;

// Test runner
function runTests() {
  console.log('='.repeat(70));
  console.log('CLI Output Adapter - Standalone Tests');
  console.log('='.repeat(70));
  
  const adapter = new CLIOutputAdapter();
  let passCount = 0;
  let failCount = 0;
  
  function test(name, fn) {
    try {
      fn();
      console.log(`✓ ${name}`);
      passCount++;
    } catch (error) {
      console.log(`✗ ${name}`);
      console.log(`  Error: ${error.message}`);
      failCount++;
    }
  }
  
  function assertEquals(actual, expected, message) {
    if (actual !== expected) {
      throw new Error(`${message}: expected "${expected}", got "${actual}"`);
    }
  }
  
  function assertExists(value, message) {
    if (!value) {
      throw new Error(`${message}: value is ${value}`);
    }
  }
  
  function assertArrayLength(arr, length, message) {
    if (!Array.isArray(arr) || arr.length !== length) {
      throw new Error(`${message}: expected array of length ${length}, got ${arr ? arr.length : 'not an array'}`);
    }
  }
  
  console.log('\n--- TEST SUITE 1: JSON Format Parsing ---\n');
  
  const jsonResult = adapter.adapt(sampleJsonOutput);
  
  test('JSON: Extracts bot name', () => {
    assertEquals(jsonResult.bot.name, 'story_bot', 'bot name');
  });
  
  test('JSON: Extracts bot directory', () => {
    assertExists(jsonResult.bot.botDirectory, 'bot directory');
    assertEquals(jsonResult.bot.botDirectory.includes('story_bot'), true, 'bot directory contains story_bot');
  });
  
  test('JSON: Extracts workspace info', () => {
    assertEquals(jsonResult.bot.workspaceName, 'base_bot', 'workspace name');
    assertExists(jsonResult.bot.workspaceDirectory, 'workspace directory');
  });
  
  test('JSON: Extracts behaviors array', () => {
    assertArrayLength(jsonResult.behaviors, 2, 'behaviors count');
  });
  
  test('JSON: Identifies current behavior', () => {
    const currentBehavior = jsonResult.behaviors.find(b => b.isCurrent);
    assertExists(currentBehavior, 'current behavior');
    assertEquals(currentBehavior.name, 'shape', 'current behavior name');
  });
  
  test('JSON: Extracts behavior actions', () => {
    const shapeBehavior = jsonResult.behaviors[0];
    assertArrayLength(shapeBehavior.actions, 2, 'shape actions count');
  });
  
  test('JSON: Identifies current action', () => {
    const shapeBehavior = jsonResult.behaviors[0];
    const currentAction = shapeBehavior.actions.find(a => a.isCurrent);
    assertExists(currentAction, 'current action');
    assertEquals(currentAction.name, 'clarify', 'current action name');
  });
  
  test('JSON: Extracts action operations', () => {
    const shapeBehavior = jsonResult.behaviors[0];
    const clarifyAction = shapeBehavior.actions[0];
    assertArrayLength(clarifyAction.operations, 2, 'clarify operations count');
  });
  
  test('JSON: Identifies current operation', () => {
    const shapeBehavior = jsonResult.behaviors[0];
    const clarifyAction = shapeBehavior.actions[0];
    const currentOp = clarifyAction.operations.find(o => o.isCurrent);
    assertExists(currentOp, 'current operation');
    assertEquals(currentOp.name, 'instructions', 'current operation name');
  });
  
  test('JSON: Extracts session state', () => {
    assertEquals(jsonResult.session.currentPosition, 'shape.clarify.instructions', 'current position');
    assertEquals(jsonResult.session.currentBehavior, 'shape', 'current behavior');
    assertEquals(jsonResult.session.currentAction, 'clarify', 'current action');
    assertEquals(jsonResult.session.actionPhase, 'instructions', 'action phase');
  });
  
  test('JSON: Extracts scope type', () => {
    assertEquals(jsonResult.scope.type, 'story', 'scope type');
  });
  
  test('JSON: Extracts scope filter', () => {
    assertEquals(jsonResult.scope.filter, 'Build MCP Tools', 'scope filter');
  });
  
  test('JSON: Extracts graph links', () => {
    assertExists(jsonResult.scope.graphLinks, 'graph links');
    assertEquals(jsonResult.scope.graphLinks.length >= 2, true, 'has multiple graph links');
  });
  
  test('JSON: Extracts story graph epics', () => {
    assertExists(jsonResult.scope.content, 'scope content');
    assertArrayLength(jsonResult.scope.content, 1, 'epics count');
    assertEquals(jsonResult.scope.content[0].name, 'Build Agile Bots', 'epic name');
  });
  
  test('JSON: Extracts story graph features', () => {
    const epic = jsonResult.scope.content[0];
    assertExists(epic.features, 'features');
    assertArrayLength(epic.features, 1, 'features count');
    assertEquals(epic.features[0].name, 'Generate MCP Tools', 'feature name');
  });
  
  test('JSON: Extracts story graph stories', () => {
    const feature = jsonResult.scope.content[0].features[0];
    assertExists(feature.stories, 'stories');
    assertArrayLength(feature.stories, 1, 'stories count');
    assertEquals(feature.stories[0].name, 'Generate Bot Tools', 'story name');
  });
  
  test('JSON: Story has correct links', () => {
    const story = jsonResult.scope.content[0].features[0].stories[0];
    assertExists(story.links, 'story links');
    assertEquals(story.links.length, 2, 'story links count (Story + Test)');
  });
  
  test('JSON: Extracts instructions', () => {
    assertExists(jsonResult.instructions, 'instructions');
    assertEquals(typeof jsonResult.instructions, 'string', 'instructions is string');
  });
  
  test('JSON: Extracts commands', () => {
    assertExists(jsonResult.commands, 'commands');
    assertExists(jsonResult.commands.list, 'commands list');
    assertEquals(Array.isArray(jsonResult.commands.list), true, 'commands.list is array');
  });
  
  console.log('\n--- TEST SUITE 2: Text Format Parsing (Fallback) ---\n');
  
  const textResult = adapter.adapt(sampleTextOutput);
  
  test('Text: Extracts bot name', () => {
    assertEquals(textResult.bot.name, 'story_bot', 'bot name');
  });
  
  test('Text: Extracts bot directory', () => {
    assertExists(textResult.bot.botDirectory, 'bot directory');
  });
  
  test('Text: Extracts workspace info', () => {
    assertEquals(textResult.bot.workspaceName, 'base_bot', 'workspace name');
  });
  
  test('Text: Extracts behaviors from text markers', () => {
    assertExists(textResult.behaviors, 'behaviors');
    assertEquals(textResult.behaviors.length >= 2, true, 'has multiple behaviors');
  });
  
  test('Text: Identifies current behavior from [*] marker', () => {
    const currentBehavior = textResult.behaviors.find(b => b.isCurrent);
    assertExists(currentBehavior, 'current behavior');
    assertEquals(currentBehavior.name, 'shape', 'current behavior name');
  });
  
  test('Text: Identifies pending behavior from [ ] marker', () => {
    const pendingBehavior = textResult.behaviors.find(b => b.name === 'tests');
    assertExists(pendingBehavior, 'pending behavior');
    assertEquals(pendingBehavior.isCurrent, false, 'tests is not current');
    assertEquals(pendingBehavior.isCompleted, false, 'tests is not completed');
  });
  
  test('Text: Extracts session position', () => {
    assertEquals(textResult.session.currentPosition, 'shape.clarify.instructions', 'current position');
  });
  
  test('Text: Parses scope from text format', () => {
    assertEquals(textResult.scope.type, 'story', 'scope type is story');
  });
  
  test('Text: Extracts scope filter from text', () => {
    assertEquals(textResult.scope.filter, 'Build MCP Tools', 'scope filter');
  });
  
  test('Text: Extracts graph links from text', () => {
    assertExists(textResult.scope.graphLinks, 'graph links');
    assertEquals(textResult.scope.graphLinks.length >= 1, true, 'has graph links');
  });
  
  console.log('\n--- TEST SUITE 3: Edge Cases ---\n');
  
  test('Empty input returns defaults', () => {
    const emptyResult = adapter.adapt('');
    assertEquals(emptyResult.bot.name, 'unknown bot', 'default bot name');
    assertArrayLength(emptyResult.behaviors, 0, 'no behaviors');
  });
  
  test('Invalid JSON falls back to text parsing', () => {
    const invalidJson = '{ invalid json }';
    const result = adapter.adapt(invalidJson);
    assertExists(result, 'result exists');
    assertExists(result.bot, 'bot info exists');
  });
  
  test('Partial JSON data handled gracefully', () => {
    const partialJson = '{ "bot": { "name": "test_bot" } }';
    const result = adapter.adapt(partialJson);
    assertEquals(result.bot.name, 'test_bot', 'bot name from partial JSON');
    assertArrayLength(result.behaviors, 0, 'missing behaviors defaults to empty');
  });
  
  // Summary
  console.log('\n' + '='.repeat(70));
  console.log(`Test Results: ${passCount} passed, ${failCount} failed`);
  console.log('='.repeat(70));
  
  if (failCount === 0) {
    console.log('\n✓✓✓ ALL TESTS PASSED ✓✓✓\n');
    process.exit(0);
  } else {
    console.log(`\n✗✗✗ ${failCount} TEST(S) FAILED ✗✗✗\n`);
    process.exit(1);
  }
}

// Run tests if executed directly
if (require.main === module) {
  runTests();
}

module.exports = { runTests };
