# Validation Report - Exploration

**Generated:** 2026-01-05 19:30:39
**Project:** base_bot
**Behavior:** exploration
**Action:** validate

## Summary

Validated content against **6 validation rules**.

## Content Validated

- **Rendered Outputs:**
  - `story-graph.json`

## Scanner Execution Status

### 🟩 Overall Status: HEALTHY

| Status | Count | Description |
|--------|-------|-------------|
| 🟩 Executed Successfully | 6 | Scanners ran without errors |
| 🟩 Clean Rules | 4 | No violations found |

**Total Rules:** 6
- **Rules with Scanners:** 6
  - 🟩 **Executed Successfully:** 6

### 🟩 Successfully Executed Scanners

- 🟨 **[Stories Have 4 To 9 Acceptance Criteria](#stories-have-4-to-9-acceptance-criteria)** - 58 violation(s) (EXECUTION_SUCCESS) - [View Details](#stories-have-4-to-9-acceptance-criteria-violations)
  - Scanner: `agile_bot.bots.base_bot.src.scanners.story_sizing_scanner.StorySizingScanner`
- 🟨 **[Alternate Actors In Steps](#alternate-actors-in-steps)** - 2 violation(s) (EXECUTION_SUCCESS) - [View Details](#alternate-actors-in-steps-violations)
  - Scanner: `agile_bot.bots.base_bot.src.scanners.actor_alternation_scanner.ActorAlternationScanner`
- 🟩 **[Behavioral Ac At Story Level](#behavioral-ac-at-story-level)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.bots.base_bot.src.scanners.behavioral_ac_scanner.BehavioralACScanner`
- 🟩 **[Enumerate All Ac Permutations](#enumerate-all-ac-permutations)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.bots.base_bot.src.scanners.enumerate_ac_permutations_scanner.EnumerateACPermutationsScanner`
- 🟩 **[Use And For Multiple Reactions](#use-and-for-multiple-reactions)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.bots.base_bot.src.scanners.reaction_chaining_scanner.ReactionChainingScanner`
- 🟩 **[Use Verb Noun Format For Story Elements](#use-verb-noun-format-for-story-elements)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.bots.base_bot.src.scanners.verb_noun_scanner.VerbNounScanner`

## Validation Rules Checked

### 🟩 Rule: <span id="behavioral-ac-at-story-level">Behavioral Ac At Story Level</span> - CLEAN (0 violations)
**Description:** Behavioral AC belongs at story level in story-graph.json. Use When/Then format (NO Given - save for scenarios). AC should describe behavioral outcomes, not technical implementation. Example: "WHEN user enters name THEN system saves to character sheet"
**Scanner:** `agile_bot.bots.base_bot.src.scanners.behavioral_ac_scanner.BehavioralACScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="enumerate-all-ac-permutations">Enumerate All Ac Permutations</span> - CLEAN (0 violations)
**Description:** Enumerate ALL acceptance criteria permutations. Apply exhaustive logic decomposition at AC level. Example: Valid input AC, Invalid input AC, Boundary AC, Error AC - cover all paths.
**Scanner:** `agile_bot.bots.base_bot.src.scanners.enumerate_ac_permutations_scanner.EnumerateACPermutationsScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="use-and-for-multiple-reactions">Use And For Multiple Reactions</span> - CLEAN (0 violations)
**Description:** Use 'And' to chain multiple system reactions to a single event. When system responds with more than one action, connect them with And. Example: When user submits → Then system validates And system saves And system sends notification.
**Scanner:** `agile_bot.bots.base_bot.src.scanners.reaction_chaining_scanner.ReactionChainingScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="use-verb-noun-format-for-story-elements">Use Verb Noun Format For Story Elements</span> - CLEAN (0 violations)
**Description:** Use verb-noun format for scenarios and acceptance criteria. Example: 'User submits form' (verb-noun), not 'Form submission' (noun-only).
**Scanner:** `agile_bot.bots.base_bot.src.scanners.verb_noun_scanner.VerbNounScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟨 Rule: <span id="alternate-actors-in-steps">Alternate Actors In Steps</span> - 2 VIOLATION(S) - [View Details](#alternate-actors-in-steps-violations)
**Description:** Alternate between actors every 1-2 steps. Scenarios should show back-and-forth interaction between user and system. Example: When user submits → Then system validates → When system displays → Then user confirms.
**Scanner:** `agile_bot.bots.base_bot.src.scanners.actor_alternation_scanner.ActorAlternationScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟨 Rule: <span id="stories-have-4-to-9-acceptance-criteria">Stories Have 4 To 9 Acceptance Criteria</span> - 58 VIOLATION(S) - [View Details](#stories-have-4-to-9-acceptance-criteria-violations)
**Description:** Stories should have 4-9 acceptance criteria. Fewer than 4 suggests incomplete exploration; more than 9 suggests story is too large and should be split. Example: Story with 6 AC (right-sized), Story with 2 AC (under-explored), Story with 15 AC (too large).
**Scanner:** `agile_bot.bots.base_bot.src.scanners.story_sizing_scanner.StorySizingScanner`
**Execution Status:** EXECUTION_SUCCESS

## Violations Found

**Total Violations:** 60
- **File-by-File Violations:** 60
- **Cross-File Violations:** 0

### File-by-File Violations (Pass 1)

These violations were detected by scanning each file individually.

#### <span id="stories-have-4-to-9-acceptance-criteria-violations">Stories Have 4 To 9 Acceptance Criteria: 58 violation(s)</span>

- <span style="color: red;">[X]</span> **ERROR** - [`epics[0].sub_epics[0].story_groups[0].stories[0].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B0%5D.sub_epics%5B0%5D.story_groups%5B0%5D.stories%5B0%5D.acceptance_criteria): Story "Generate Bot Tools" has 1 1 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[0].sub_epics[0].story_groups[0].stories[1].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B0%5D.sub_epics%5B0%5D.story_groups%5B0%5D.stories%5B1%5D.acceptance_criteria): Story "Generate Behavior Tools" has 1 1 acceptance criteria (should be 4-10)
- <span style="color: orange;">[!]</span> **WARNING** - [`epics[0].sub_epics[0].story_groups[0].stories[2].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B0%5D.sub_epics%5B0%5D.story_groups%5B0%5D.stories%5B2%5D.acceptance_criteria): Story "Generate MCP Bot Server" has 3 3 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[0].story_groups[0].stories[4].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B0%5D.story_groups%5B0%5D.stories%5B4%5D.acceptance_criteria): Story "Track Activity For Workspace" has 1 1 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[0].story_groups[0].stories[0].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B0%5D.story_groups%5B0%5D.stories%5B0%5D.acceptance_criteria): Story "Open Panel" has 12 12 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[0].story_groups[0].stories[1].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B0%5D.story_groups%5B0%5D.stories%5B1%5D.acceptance_criteria): Story "Refresh Panel" has 13 13 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[0].story_groups[0].stories[2].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B0%5D.story_groups%5B0%5D.stories%5B2%5D.acceptance_criteria): Story "Change Workspace Path" has 12 12 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[0].story_groups[0].stories[3].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B0%5D.story_groups%5B0%5D.stories%5B3%5D.acceptance_criteria): Story "Switch Bot" has 13 13 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[0].story_groups[0].stories[4].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B0%5D.story_groups%5B0%5D.stories%5B4%5D.acceptance_criteria): Story "Toggle Panel Section" has 12 12 acceptance criteria (should be 4-10)
- <span style="color: orange;">[!]</span> **WARNING** - [`epics[1].sub_epics[2].sub_epics[1].name`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B1%5D.name): Sub-epic "Navigate Behavior Action Status" has 3 3 stories (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[1].story_groups[0].stories[0].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B1%5D.story_groups%5B0%5D.stories%5B0%5D.acceptance_criteria): Story "Display Hierarchy" has 15 15 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[1].story_groups[0].stories[1].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B1%5D.story_groups%5B0%5D.stories%5B1%5D.acceptance_criteria): Story "Navigate Behavior Action" has 17 17 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[1].story_groups[0].stories[2].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B1%5D.story_groups%5B0%5D.stories%5B2%5D.acceptance_criteria): Story "Execute Behavior Action" has 17 17 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[2].story_groups[0].stories[0].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B2%5D.story_groups%5B0%5D.stories%5B0%5D.acceptance_criteria): Story "Filter Story Scope" has 12 12 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[2].story_groups[0].stories[1].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B2%5D.story_groups%5B0%5D.stories%5B1%5D.acceptance_criteria): Story "Display Story Scope Hierarchy" has 13 13 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[2].story_groups[0].stories[2].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B2%5D.story_groups%5B0%5D.stories%5B2%5D.acceptance_criteria): Story "Filter File Scope" has 12 12 acceptance criteria (should be 4-10)
- <span style="color: orange;">[!]</span> **WARNING** - [`epics[1].sub_epics[2].sub_epics[2].story_groups[0].stories[4].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B2%5D.story_groups%5B0%5D.stories%5B4%5D.acceptance_criteria): Story "Clear Scope Filter" has 11 11 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[2].story_groups[0].stories[5].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B2%5D.story_groups%5B0%5D.stories%5B5%5D.acceptance_criteria): Story "Toggle Scope Hierarchy" has 15 15 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[2].story_groups[0].stories[6].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B2%5D.story_groups%5B0%5D.stories%5B6%5D.acceptance_criteria): Story "Open Story Files" has 12 12 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[2].story_groups[0].stories[7].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B2%5D.story_groups%5B0%5D.stories%5B7%5D.acceptance_criteria): Story "Open Test Files" has 12 12 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[2].story_groups[0].stories[8].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B2%5D.story_groups%5B0%5D.stories%5B8%5D.acceptance_criteria): Story "Open Graph Files" has 12 12 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[3].story_groups[0].stories[0].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B3%5D.story_groups%5B0%5D.stories%5B0%5D.acceptance_criteria): Story "Display Base Instructions" has 13 13 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[3].story_groups[0].stories[1].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B3%5D.story_groups%5B0%5D.stories%5B1%5D.acceptance_criteria): Story "Display Clarify Instructions" has 12 12 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[3].story_groups[0].stories[2].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B3%5D.story_groups%5B0%5D.stories%5B2%5D.acceptance_criteria): Story "Display Strategy Instructions" has 12 12 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[3].story_groups[0].stories[3].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B3%5D.story_groups%5B0%5D.stories%5B3%5D.acceptance_criteria): Story "Display Build Instructions" has 13 13 acceptance criteria (should be 4-10)
- <span style="color: orange;">[!]</span> **WARNING** - [`epics[1].sub_epics[2].sub_epics[3].story_groups[0].stories[4].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B3%5D.story_groups%5B0%5D.stories%5B4%5D.acceptance_criteria): Story "Display Validate Instructions" has 11 11 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[3].story_groups[0].stories[5].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B3%5D.story_groups%5B0%5D.stories%5B5%5D.acceptance_criteria): Story "Display Render Instructions" has 13 13 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[3].story_groups[0].stories[6].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B3%5D.story_groups%5B0%5D.stories%5B6%5D.acceptance_criteria): Story "Display Instructions In Raw Format" has 12 12 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[1].sub_epics[2].sub_epics[3].story_groups[0].stories[7].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B2%5D.sub_epics%5B3%5D.story_groups%5B0%5D.stories%5B7%5D.acceptance_criteria): Story "Submit Instructions To Chat" has 13 13 acceptance criteria (should be 4-10)
- <span style="color: orange;">[!]</span> **WARNING** - [`epics[1].sub_epics[3].sub_epics[1].name`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B3%5D.sub_epics%5B1%5D.name): Sub-epic "Navigate Bot Behaviors and Actions With CLI" has 3 3 stories (should be 4-10)
- <span style="color: orange;">[!]</span> **WARNING** - [`epics[1].sub_epics[3].sub_epics[2].name`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B3%5D.sub_epics%5B2%5D.name): Sub-epic "Navigate Bot Behaviors and Actions Via Domain Model" has 3 3 stories (should be 4-10)
- <span style="color: orange;">[!]</span> **WARNING** - [`epics[1].sub_epics[3].sub_epics[6].name`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B3%5D.sub_epics%5B6%5D.name): Sub-epic "Get Help Using CLI" has 3 3 stories (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[0].story_groups[0].stories[1].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B0%5D.story_groups%5B0%5D.stories%5B1%5D.acceptance_criteria): Story "Track Activity for Gather Context Action" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[0].story_groups[0].stories[4].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B0%5D.story_groups%5B0%5D.stories%5B4%5D.acceptance_criteria): Story "Load Base Action Config" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[0].story_groups[0].stories[5].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B0%5D.story_groups%5B0%5D.stories%5B5%5D.acceptance_criteria): Story "Access Actions" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[0].story_groups[0].stories[6].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B0%5D.story_groups%5B0%5D.stories%5B6%5D.acceptance_criteria): Story "Initialize Action" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[0].story_groups[0].stories[7].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B0%5D.story_groups%5B0%5D.stories%5B7%5D.acceptance_criteria): Story "Load Guardrails" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[1].story_groups[0].stories[0].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B1%5D.story_groups%5B0%5D.stories%5B0%5D.acceptance_criteria): Story "Track Activity for Strategy Action" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[1].story_groups[0].stories[3].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B1%5D.story_groups%5B0%5D.stories%5B3%5D.acceptance_criteria): Story "Inject Strategy Into Instructions" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[1].story_groups[0].stories[4].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B1%5D.story_groups%5B0%5D.stories%5B4%5D.acceptance_criteria): Story "Store Strategy Data" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[2].story_groups[0].stories[2].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B2%5D.story_groups%5B0%5D.stories%5B2%5D.acceptance_criteria): Story "Track Activity for Build Knowledge Action" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: orange;">[!]</span> **WARNING** - [`epics[2].sub_epics[2].story_groups[0].stories[4].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B2%5D.story_groups%5B0%5D.stories%5B4%5D.acceptance_criteria): Story "Proceed To Render Output" has 3 3 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[2].story_groups[0].stories[6].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B2%5D.story_groups%5B0%5D.stories%5B6%5D.acceptance_criteria): Story "Create Build Scope" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[2].story_groups[0].stories[7].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B2%5D.story_groups%5B0%5D.stories%5B7%5D.acceptance_criteria): Story "Filter Knowledge Graph" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[3].name`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B3%5D.name): Sub-epic "Render Output" has 13 13 stories (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[3].story_groups[0].stories[0].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B3%5D.story_groups%5B0%5D.stories%5B0%5D.acceptance_criteria): Story "Track Activity for Render Output Action" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: orange;">[!]</span> **WARNING** - [`epics[2].sub_epics[3].story_groups[0].stories[3].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B3%5D.story_groups%5B0%5D.stories%5B3%5D.acceptance_criteria): Story "Inject Template Instructions" has 3 3 acceptance criteria (should be 4-10)
- <span style="color: orange;">[!]</span> **WARNING** - [`epics[2].sub_epics[3].story_groups[0].stories[5].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B3%5D.story_groups%5B0%5D.stories%5B5%5D.acceptance_criteria): Story "Inject Render Instructions And Configs" has 3 3 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[3].story_groups[0].stories[6].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B3%5D.story_groups%5B0%5D.stories%5B6%5D.acceptance_criteria): Story "Get Render Instructions" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[3].story_groups[0].stories[8].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B3%5D.story_groups%5B0%5D.stories%5B8%5D.acceptance_criteria): Story "Render Output Using Synchronizers" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: orange;">[!]</span> **WARNING** - [`epics[2].sub_epics[3].story_groups[0].stories[9].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B3%5D.story_groups%5B0%5D.stories%5B9%5D.acceptance_criteria): Story "Inject Render Instructions And Configs" has 3 3 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[3].story_groups[0].stories[10].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B3%5D.story_groups%5B0%5D.stories%5B10%5D.acceptance_criteria): Story "Get Render Instructions" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[3].story_groups[0].stories[12].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B3%5D.story_groups%5B0%5D.stories%5B12%5D.acceptance_criteria): Story "Render Output Using Synchronizers" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[4].story_groups[0].stories[1].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B4%5D.story_groups%5B0%5D.stories%5B1%5D.acceptance_criteria): Story "Track Activity for Validate Rules Action" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[4].story_groups[0].stories[3].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B4%5D.story_groups%5B0%5D.stories%5B3%5D.acceptance_criteria): Story "Discovers Scanners" has 12 12 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[4].story_groups[0].stories[5].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B4%5D.story_groups%5B0%5D.stories%5B5%5D.acceptance_criteria): Story "Validate Rules According To Scope" has 2 2 acceptance criteria (should be 4-10)
- <span style="color: orange;">[!]</span> **WARNING** - [`epics[2].sub_epics[4].story_groups[0].stories[6].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B4%5D.story_groups%5B0%5D.stories%5B6%5D.acceptance_criteria): Story "Generate Violation Report" has 3 3 acceptance criteria (should be 4-10)
- <span style="color: red;">[X]</span> **ERROR** - [`epics[2].sub_epics[4].story_groups[0].stories[7].acceptance_criteria`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B2%5D.sub_epics%5B4%5D.story_groups%5B0%5D.stories%5B7%5D.acceptance_criteria): Story "Report Validation and Error Handling" has 16 16 acceptance criteria (should be 4-10)

#### <span id="alternate-actors-in-steps-violations">Alternate Actors In Steps: 2 violation(s)</span>

- <span style="color: orange;">[!]</span> **WARNING** - [`epics[1].sub_epics[3].sub_epics[5].story_groups[0].stories[5].acceptance_criteria[1]`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B3%5D.sub_epics%5B5%5D.story_groups%5B0%5D.stories%5B5%5D.acceptance_criteria%5B1%5D): Story "Display Headless Mode Status in CLI" AC #2 has 3 consecutive user steps without alternating
- <span style="color: orange;">[!]</span> **WARNING** - [`epics[1].sub_epics[3].sub_epics[5].story_groups[0].stories[5].acceptance_criteria[3]`](vscode://file/C:/dev/augmented-teams/agile_bot/bots/base_bot/epics%5B1%5D.sub_epics%5B3%5D.sub_epics%5B5%5D.story_groups%5B0%5D.stories%5B5%5D.acceptance_criteria%5B3%5D): Story "Display Headless Mode Status in CLI" AC #4 has 3 consecutive user steps without alternating

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
*... and 53 more instructions*

## Report Location

This report was automatically generated and saved to:
`c:\dev\augmented-teams\agile_bot\bots\base_bot\docs\stories\reports\exploration-validation-report-2026-01-05_19-30-36.md`

