# Validation Report - Shape

**Generated:** 2026-01-11 11:56:35
**Project:** agile_bot
**Behavior:** shape
**Action:** validate

## Summary

Validated content against **8 validation rules**.

## Content Validated

- **Rendered Outputs:**
  - `story-graph.json`

## Scanner Execution Status

### 🟩 Overall Status: HEALTHY

| Status | Count | Description |
|--------|-------|-------------|
| 🟩 Executed Successfully | 4 | Scanners ran without errors |
| 🟩 Clean Rules | 3 | No violations found |
| [i] No Scanner | 4 | Rule has no scanner configured |

**Total Rules:** 8
- **Rules with Scanners:** 4
  - 🟩 **Executed Successfully:** 4
- [i] **Rules without Scanners:** 4

### 🟩 Successfully Executed Scanners

- 🟨 **[Small And Testable](#small-and-testable)** - 13 violation(s) (EXECUTION_SUCCESS) - [View Details](#small-and-testable-violations)
  - Scanner: `agile_bot.bots.base_bot.src.scanners.implementation_details_scanner.ImplementationDetailsScanner`
- 🟩 **[Active Business And Behavioral Language](#active-business-and-behavioral-language)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.bots.base_bot.src.scanners.active_language_scanner.ActiveLanguageScanner`
- 🟩 **[Outcome Oriented Language](#outcome-oriented-language)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.bots.base_bot.src.scanners.communication_verb_scanner.CommunicationVerbScanner`
- 🟩 **[Verb Noun Format](#verb-noun-format)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.bots.base_bot.src.scanners.verb_noun_scanner.VerbNounScanner`

### <span style="color: gray;">[i] Rules Without Scanners</span>

- <span style="color: gray;">[i]</span> **[Lightweight And Precise](#lightweight-and-precise)** - No scanner configured
- <span style="color: gray;">[i]</span> **[Valuable](#valuable)** - No scanner configured
- <span style="color: gray;">[i]</span> **[User And System Behavior](#user-and-system-behavior)** - No scanner configured
- <span style="color: gray;">[i]</span> **[Story Map Existing Code](#story-map-existing-code)** - No scanner configured

## Validation Rules Checked

### 🟩 Rule: <span id="active-business-and-behavioral-language">Active Business And Behavioral Language</span> - CLEAN (0 violations)
**Description:** Use active business language focused on user/system behavior. Describe what actors do with clear action verbs, not technical implementation or passive constructions.
**Scanner:** `agile_bot.bots.base_bot.src.scanners.active_language_scanner.ActiveLanguageScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="outcome-oriented-language">Outcome Oriented Language</span> - CLEAN (0 violations)
**Description:** Use outcome-oriented language over mechanism-oriented language. Focus on what is created or achieved, not how it's shown or communicated.
**Scanner:** `agile_bot.bots.base_bot.src.scanners.communication_verb_scanner.CommunicationVerbScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="verb-noun-format">Verb Noun Format</span> - CLEAN (0 violations)
**Description:** Use verb-noun format consistently across all hierarchy levels. Actor --> verb noun [qualifiers]. Actor is documented separately, NOT in the name. Focus on specific actions with context.
**Scanner:** `agile_bot.bots.base_bot.src.scanners.verb_noun_scanner.VerbNounScanner`
**Execution Status:** EXECUTION_SUCCESS

### [i] Rule: <span id="lightweight-and-precise">Lightweight And Precise</span> - NO SCANNER
**Description:** Create lightweight but precise documentation during shaping. Focus on structure and scope, not detailed specifications.
**Scanner:** Not configured

### 🟨 Rule: <span id="small-and-testable">Small And Testable</span> - 13 VIOLATION(S) - [View Details](#small-and-testable-violations)
**Description:** Stories must be testable as complete interactions and deliverable independently. Balance testability with maintaining value and behavioral focus - stories should be small enough to test but large enough to matter.
**Scanner:** `agile_bot.bots.base_bot.src.scanners.implementation_details_scanner.ImplementationDetailsScanner`
**Execution Status:** EXECUTION_SUCCESS

### [i] Rule: <span id="story-map-existing-code">Story Map Existing Code</span> - NO SCANNER
**Description:** When creating story maps from code, start with the outermost layer (entry points), analyze operations, create epics from higher-order goals, and lay out the story journey.
**Scanner:** Not configured

### [i] Rule: <span id="user-and-system-behavior">User And System Behavior</span> - NO SCANNER
**Description:** Stories should capture both user and system behavior. User-facing stories show user actions with system responses. System stories capture system-to-system interactions and should be marked with story_type: 'system'. NOTE: This rule only applies when strategy decisions in planning.json specify flow_scope_and_granularity as 'Integration boundary level' or 'Intra-system level', OR drill_down_approach includes 'Dig deep on system interactions' or 'Dig deep on architectural pieces'. Check {project_area}/docs/stories/planning.json for these decisions.
**Scanner:** Not configured

### [i] Rule: <span id="valuable">Valuable</span> - NO SCANNER
**Description:** Stories must deliver independent value as complete functional accomplishments. Balance value with testability - stories should be valuable enough to matter but small enough to deliver quickly. Not just data access or isolated operations.
**Scanner:** Not configured

## Violations Found

**Total Violations:** 13
- **File-by-File Violations:** 13
- **Cross-File Violations:** 0

### File-by-File Violations (Pass 1)

These violations were detected by scanning each file individually.

#### <span id="small-and-testable-violations">Small And Testable: 13 violation(s)</span>

- <span style="color: red;">[X]</span> **ERROR** - [`Generate Bot Tools`](vscode://file/C:/dev/augmented-teams/agile_bot/Generate%20Bot%20Tools): Story "Generate Bot Tools" appears to be an implementation operation - should be a step within a story that describes user/system outcome
- <span style="color: red;">[X]</span> **ERROR** - [`Generate Behavior Tools`](vscode://file/C:/dev/augmented-teams/agile_bot/Generate%20Behavior%20Tools): Story "Generate Behavior Tools" appears to be an implementation operation - should be a step within a story that describes user/system outcome
- <span style="color: red;">[X]</span> **ERROR** - [`Generate MCP Bot Server`](vscode://file/C:/dev/augmented-teams/agile_bot/Generate%20MCP%20Bot%20Server): Story "Generate MCP Bot Server" appears to be an implementation operation - should be a step within a story that describes user/system outcome
- <span style="color: red;">[X]</span> **ERROR** - [`Generate Behavior Action Tools`](vscode://file/C:/dev/augmented-teams/agile_bot/Generate%20Behavior%20Action%20Tools): Story "Generate Behavior Action Tools" appears to be an implementation operation - should be a step within a story that describes user/system outcome
- <span style="color: red;">[X]</span> **ERROR** - [`Generate Command Definitions`](vscode://file/C:/dev/augmented-teams/agile_bot/Generate%20Command%20Definitions): Story "Generate Command Definitions" appears to be an implementation operation - should be a step within a story that describes user/system outcome
- <span style="color: red;">[X]</span> **ERROR** - [`Generate CLI Entry Point`](vscode://file/C:/dev/augmented-teams/agile_bot/Generate%20CLI%20Entry%20Point): Story "Generate CLI Entry Point" appears to be an implementation operation - should be a step within a story that describes user/system outcome
- <span style="color: red;">[X]</span> **ERROR** - [`Generate Cursor Commands`](vscode://file/C:/dev/augmented-teams/agile_bot/Generate%20Cursor%20Commands): Story "Generate Cursor Commands" appears to be an implementation operation - should be a step within a story that describes user/system outcome
- <span style="color: red;">[X]</span> **ERROR** - [`Generate Help Documentation`](vscode://file/C:/dev/augmented-teams/agile_bot/Generate%20Help%20Documentation): Story "Generate Help Documentation" appears to be an implementation operation - should be a step within a story that describes user/system outcome
- <span style="color: red;">[X]</span> **ERROR** - [`Set Scope Through Bot API`](vscode://file/C:/dev/augmented-teams/agile_bot/Set%20Scope%20Through%20Bot%20API): Story "Set Scope Through Bot API" appears to be an implementation operation - should be a step within a story that describes user/system outcome
- <span style="color: red;">[X]</span> **ERROR** - [`Store Clarification Data`](vscode://file/C:/dev/augmented-teams/agile_bot/Store%20Clarification%20Data): Story "Store Clarification Data" appears to be an implementation operation - should be a step within a story that describes user/system outcome
- <span style="color: red;">[X]</span> **ERROR** - [`Store Strategy Data`](vscode://file/C:/dev/augmented-teams/agile_bot/Store%20Strategy%20Data): Story "Store Strategy Data" appears to be an implementation operation - should be a step within a story that describes user/system outcome
- <span style="color: red;">[X]</span> **ERROR** - [`Create Build Scope`](vscode://file/C:/dev/augmented-teams/agile_bot/Create%20Build%20Scope): Story "Create Build Scope" appears to be an implementation operation - should be a step within a story that describes user/system outcome
- <span style="color: red;">[X]</span> **ERROR** - [`Generate Violation Report`](vscode://file/C:/dev/augmented-teams/agile_bot/Generate%20Violation%20Report): Story "Generate Violation Report" appears to be an implementation operation - should be a step within a story that describes user/system outcome

## Validation Instructions

The following validation steps were performed:

1. ## Step 1: Scanner Violation Review
2. 
3. {{scanner_output}}
4. 
5. Carefully review all scanner-reported violations as follows:
6. 1. For each violation message, locate the corresponding element in the knowledge graph.
7. 2. Open the relevant rule file and read all DO and DON'T examples thoroughly.
8. 3. Decide if the violation is **Valid** (truly a rule breach per examples) or a **False Positive** (explain why if so).
9. 4. Determine the **Root Cause** (e.g., 'incorrect concept naming', 'missing actor', etc.).
10. 5. Assign a **Theme** grouping based on the type of issue (e.g., 'noun-only naming', 'incomplete acceptance criteria').
*... and 52 more instructions*

## Report Location

This report was automatically generated and saved to:
`C:\dev\augmented-teams\agile_bot\docs\stories\reports\shape-validation-report-2026-01-11_11-56-32.md`

