**Combined instructions:** The following combines multiple actions. Perform them one after another.

## Scope

**Story Scope:** "Submit Instructions From Workspace"

Please only work on the following scope.

Scope Filter: ""Submit Instructions From Workspace""

Scope:

{
  "path": "C:\\dev\\agile_bots\\docs\\story\\story-graph.json",
  "has_epics": true,
  "has_increments": true,
  "has_domain_concepts": true,
  "epic_count": 1,
  "content": {
    "epics": [
      {
        "name": "Invoke Bot",
        "sub_epics": [
          {
            "name": "Navigate Behavior Actions",
            "sub_epics": [
              {
                "name": "Perform Behavior Action In Bot Workflow",
                "sub_epics": [],
                "story_groups": [
                  {
                    "name": null,
                    "stories": [
                      {
                        "name": "Submit Instructions From Workspace",
                        "acceptance_criteria": [
                          {
                            "name": "WHEN User has instructions visible in workspace section\nTHEN Panel displays Submit button AND User can trigger submit to send instructions to AI agent",
                            "text": "WHEN User has instructions visible in workspace section\nTHEN Panel displays Submit button AND User can trigger submit to send instructions to AI agent",
                            "sequential_order": 0.0
                          },
                          {
                            "name": "WHEN No {Behavior} selected\nTHEN System shows scope error or disables submit",
                            "text": "WHEN No {Behavior} selected\nTHEN System shows scope error or disables submit",
                            "sequential_order": 1.0
                          }
                        ],
                        "scenarios": [
                          {
                            "name": "User submits {Behavior} instructions to AI agent",
                            "background": [],
                            "steps": [
                              {
                                "text": "Given {Behavior} \"shape\" is selected in workspace",
                                "sequential_order": 1.0
                              },
                              {
                                "text": "And {InstructionsSection} displays shape instructions",
                                "sequential_order": 2.0
                              },
                              {
                                "text": "When User triggers submit from workspace",
                                "sequential_order": 3.0
                              },
                              {
                                "text": "Then System sends {Behavior} shape instructions to AI agent",
                                "sequential_order": 4.0
                              },
                              {
                                "text": "And Submit button is visible and enabled",
                                "sequential_order": 5.0
                              }
                            ],
                            "examples": null
                          },
                          {
                            "name": "Submit disabled when no behavior selected",
                            "background": [],
                            "steps": [
                              {
                                "text": "Given no {Behavior} is selected in workspace",
                                "sequential_order": 1.0
                              },
                              {
                                "text": "When User views workspace section",
                                "sequential_order": 2.0
                              },
                              {
                                "text": "Then Submit shows scope error or is disabled",
                                "sequential_order": 3.0
                              },
                              {
                                "text": "And User cannot submit empty instructions",
                                "sequential_order": 4.0
                              }
                            ],
                            "examples": null
                          }
                        ]
                      }
                    ]
                  }
                ],
                "domain_concepts": [
                  {
                    "name": "Base Action",
                    "responsibilities": [
                      {
                        "name": "Inject Instructions",
                        "collaborators": [
                          "Behavior"
                        ]
                      },
                      {
                        "name": "Load Relevant Content + Inject Into Instructions",
                        "collaborators": [
                          "Content"
                        ]
                      },
                      {
                        "name": "Save content changes",
                        "collaborators": [
                          "Content"
                        ]
                      },
                      {
                        "name": "Get save file",
                        "collaborators": [
                          "Path"
                        ]
                      },
                      {
                        "name": "Execution gates on save file watch",
                        "collaborators": [
                          "SaveFileWatcher",
                          "Debounce",
                          "Next Action"
                        ]
                      }
                    ],
                    "module": "actions",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "SaveFileWatcher",
                    "responsibilities": [
                      {
                        "name": "Watch save file for writes",
                        "collaborators": [
                          "Path",
                          "File System"
                        ]
                      },
                      {
                        "name": "Report when file stable past debounce",
                        "collaborators": [
                          "Path",
                          "Debounce",
                          "Boolean"
                        ]
                      }
                    ],
                    "module": "actions",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "ActionStateManager",
                    "responsibilities": [
                      {
                        "name": "Get state file path",
                        "collaborators": [
                          "Path"
                        ]
                      },
                      {
                        "name": "Load or create state",
                        "collaborators": [
                          "State File",
                          "Dict"
                        ]
                      },
                      {
                        "name": "Save state",
                        "collaborators": [
                          "Action",
                          "State File"
                        ]
                      },
                      {
                        "name": "Load state",
                        "collaborators": [
                          "Actions List",
                          "Current Index"
                        ]
                      },
                      {
                        "name": "Find action index",
                        "collaborators": [
                          "Actions List",
                          "Action Name",
                          "Integer"
                        ]
                      },
                      {
                        "name": "Filter completed actions",
                        "collaborators": [
                          "Completed Actions",
                          "Target Index",
                          "Actions List",
                          "List"
                        ]
                      }
                    ],
                    "module": "actions",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "TTYAction",
                    "responsibilities": [
                      {
                        "name": "Serialize action to TTY",
                        "collaborators": [
                          "Action",
                          "String"
                        ]
                      },
                      {
                        "name": "Format action line",
                        "collaborators": [
                          "Action Name",
                          "Marker",
                          "Indent"
                        ]
                      },
                      {
                        "name": "Wraps domain action",
                        "collaborators": [
                          "Action"
                        ]
                      }
                    ],
                    "module": "actions",
                    "inherits_from": "TTYProgressAdapter",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "JSONAction",
                    "responsibilities": [
                      {
                        "name": "Serialize action to JSON dict",
                        "collaborators": [
                          "Action",
                          "Dict"
                        ]
                      },
                      {
                        "name": "Include action metadata",
                        "collaborators": [
                          "Name",
                          "Description",
                          "Status"
                        ]
                      },
                      {
                        "name": "Wraps domain action",
                        "collaborators": [
                          "Action"
                        ]
                      }
                    ],
                    "module": "actions",
                    "inherits_from": "JSONProgressAdapter",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "MarkdownAction",
                    "responsibilities": [
                      {
                        "name": "Serialize action to Markdown",
                        "collaborators": [
                          "Action",
                          "String"
                        ]
                      },
                      {
                        "name": "Format action documentation",
                        "collaborators": [
                          "Action Name",
                          "Description",
                          "Subsection"
                        ]
                      },
                      {
                        "name": "Wraps domain action",
                        "collaborators": [
                          "Action"
                        ]
                      }
                    ],
                    "module": "actions",
                    "inherits_from": "MarkdownProgressAdapter",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  }
                ]
              }
            ],
            "story_groups": []
          }
        ],
        "domain_concepts": []
      }
    ],
    "increments": []
  }
}

---

# Behavior: scenarios

## Behavior Instructions - scenarios

The purpose of this behavior is to write detailed plain-english scenarios (given/when/then) that specify exact behavior for each story

Write detailed plain-English scenarios (Given/When/Then) that specify exact behavior for each story

## Action Instructions - build

The purpose of this action is to build story graph from content area and render using story graph renderer

Follow agile_bot/bots/story_bot/behaviors/scenarios/content/story_graph/instructions.json
specification_scenarios: build scenarios using domain language
Use proper domain terminology in scenario steps - refer to domain concepts and entities
Add/update scenarios and scenario_outlines ONLY in main epics section (single source of truth), NOT in increments section

**STORY GRAPH UPDATE STRATEGY (use when story-graph.json already exists):**

When updating an existing story graph, do NOT read and rewrite the entire story-graph.json manually.
Choose one of these approaches in order of preference:

1. **API approach (preferred for targeted changes):**
   Use the StoryMap node API via CLI dot-notation to make surgical changes.
   - Navigate: story_map.filter_by_name name:"Story Name" to read only the relevant subtree
   - Create:  story_map."Epic"."SubEpic"."Story".create_scenario name:"Scenario Name"
   - Create:  story_map."Epic"."SubEpic"."Story".create_acceptance_criteria name:"WHEN condition THEN outcome"
   - Rename:  story_map."Epic"."SubEpic"."Story".rename name:"New Name"
   - Move:    story_map."Epic"."SubEpic"."Story".move_to target:"Other SubEpic"
   - Reorder: story_map."Epic"."SubEpic"."Story".move_to at_position:2
   - Delete:  story_map."Epic"."SubEpic"."Story"."Old Scenario".delete
   Each call auto-saves the full graph safely through in-memory tree serialization.

2. **Bulk approach (for sweeping changes across many stories):**
   Build a temporary StoryMap with just your changes using the same create API (without bot context),
   then use generate_merge_report() to compare against the original, and merge_story_graphs() to apply.
   The merge preserves all original data (acceptance_criteria, scenarios, steps, metadata) you did not change.

3. **Manual JSON edit (last resort only):**
   Only if the API and bulk approaches cannot handle the situation.
   Use filter_by_name to read a scoped subtree rather than the full file.
   Write changes back through the StoryMap.save() method, as opposed to by editing story-graph.json directly.

---

**Look for context in the following locations:**
- in this message and chat history
- `C:/dev/agile_bots/docs/story/story-graph.json` - the story graph and related  knowledge built so far
- `C:/dev/agile_bots/docs/story/strategy.json` - strategy decisions made
- `C:/dev/agile_bots/docs/story/clarification.json` - clarification answers
- `C:/dev/agile_bots/test/` and `C:/dev/agile_bots/src/` - existing code and tests
- any folder named `context/` anywhere in `C:/dev/agile_bots/` - additional context files

IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

@build-instructions.txt

**BUILD PROCESS:**

**1. Load Context**
Load clarification.json, planning.json, and source material from context sources (listed above).

**2. Load Build Configs**
From `c:\dev\agile_bots\bots\story_bot/behaviors/scenarios/content/`, each folder contains:
- `build_*.json` - Config (name, path, template, output)
- `instructions.json` - Build instructions
- `template-file.json` - Output schema/structure

**3. Execute Build**
1. Load config, instructions, and template (injected as 'story_graph_template')
2. Check if output file exists - read it FIRST
3. Follow instructions.json - match template structure exactly (check '_explanation' section)
4. Apply context from Step 1
5. If file exists: ADD/EXTEND only, never overwrite/delete
6. Validate against template schema
7. Write to `C:\dev\agile_bots/{config.path}/{config.output}`
- Read existing files before changes - preserve all content
- Match template structure exactly - don't invent schemas
- Trace all knowledge to clarification/planning data
- Process builds sequentially - validate each

**4. SOURCE TRACEABILITY**
Knowledge artifacts should include source references when available:
- `context_source` field on epics, sub_epics, story_groups, stories, and domain concepts
- Format: `{"file": "filename.pdf", "page": "12", "section": "3.2.1 Payment Flow"}`
- For multiple sources: use array of source objects
- If source is chat/conversation: `{"type": "chat", "description": "User clarification on approval workflow"}`
- If source is code: `{"file": "path/to/file.py", "lines": "45-67", "function": "process_payment"}`
- Prefer tracing knowledge to a source when possible
- When source is unclear, mark as `{"type": "inferred", "basis": "description of inference basis"}`
Follow agile_bot/bots/story_bot/behaviors/scenarios/content/story_graph/instructions.json
specification_scenarios: build scenarios using domain language
Use proper domain terminology in scenario steps - refer to domain concepts and entities
Add/update scenarios and scenario_outlines ONLY in main epics section (single source of truth), NOT in increments section

**STORY GRAPH UPDATE STRATEGY (use when story-graph.json already exists):**

When updating an existing story graph, do NOT read and rewrite the entire story-graph.json manually.
Choose one of these approaches in order of preference:

1. **API approach (preferred for targeted changes):**
   Use the StoryMap node API via CLI dot-notation to make surgical changes.
   - Navigate: story_map.filter_by_name name:"Story Name" to read only the relevant subtree
   - Create:  story_map."Epic"."SubEpic"."Story".create_scenario name:"Scenario Name"
   - Create:  story_map."Epic"."SubEpic"."Story".create_acceptance_criteria name:"WHEN condition THEN outcome"
   - Rename:  story_map."Epic"."SubEpic"."Story".rename name:"New Name"
   - Move:    story_map."Epic"."SubEpic"."Story".move_to target:"Other SubEpic"
   - Reorder: story_map."Epic"."SubEpic"."Story".move_to at_position:2
   - Delete:  story_map."Epic"."SubEpic"."Story"."Old Scenario".delete
   Each call auto-saves the full graph safely through in-memory tree serialization.

2. **Bulk approach (for sweeping changes across many stories):**
   Build a temporary StoryMap with just your changes using the same create API (without bot context),
   then use generate_merge_report() to compare against the original, and merge_story_graphs() to apply.
   The merge preserves all original data (acceptance_criteria, scenarios, steps, metadata) you did not change.

3. **Manual JSON edit (last resort only):**
   Only if the API and bulk approaches cannot handle the situation.
   Use filter_by_name to read a scoped subtree rather than the full file.
   Write changes back through the StoryMap.save() method, as opposed to by editing story-graph.json directly.

When building or adding to the story graph follow these rules,
Rules to follow:

- **scenario_language_matches_domain**: Scenario language MUST use domain concept terminology. Given/When/Then steps should reference domain entities and concepts, not UI elements or technical implementation details.
  DO: Use domain language in scenario steps - reference domain concepts by name.
  DON'T: Don't use UI element names, technical implementation terms, or generic words instead of domain concepts.

- **example_tables_use_domain_language**: Example tables MUST be grounded in scenario steps AND use domain-rich language. Table columns = nouns from Given/When/Then steps. Use domain terminology, not UI elements. Omit ID columns used purely for linking tables - relationships are expressed via collaboration field and table ordering. Concrete values with domain context, not generic JSON or placeholders. Use source entity data, not aggregated/calculated values - this is the stage where you figure out the real examples.
  DO: Ground tables in scenario nouns, use domain terminology, connect tables using domain responsibility sentences. Omit implementation IDs. Show source entities, not derived counts.
  DON'T: Don't use UI elements, flat lookup tables, generic JSON, abstract descriptions, invented terminology, or aggregated/calculated values.

- **given_describes_state_not_actions**: Given statements describe STATE/PRECONDITIONS, not actions or functionality. Given = what exists before test. When = first action. Then = expected behavior. Example: Given user is logged in (state), not Given user logs in (action).
  DO: Given describes state/preconditions only. Example: 'Given user is logged in' (state), 'Given character sheet exists' (precondition)
  DON'T: Don't describe actions, UI navigation, or functionality in Given. Example: 'Given user logs in' (action - wrong), 'Given User is on PaymentDetails step' (navigation - wrong)

- **background_vs_scenario_setup**: Background = shared setup for 3+ scenarios (Given/And only, no When/Then). Background steps MUST use {Concept} notation to reference domain objects. Use {Concept.property} when a specific attribute is important. Don't repeat Background in Steps.
  DO: Use Background for shared context with {Concept} references to example tables.
  DON'T: Don't use hardcoded values or column names in Background - use {Concept} notation. Don't include When/Then.

- **scenarios_cover_all_cases**: Scenarios must cover happy path, edge cases, and error cases based on acceptance criteria. Example: Valid input → success; Boundary value → validates; Invalid input → error message.
  DO: Cover all case types: happy path, edge cases, error cases. Example: User enters valid data → success; User enters boundary → validates; User enters invalid → error
  DON'T: Don't skip case types. Example: Only happy path scenarios (missing edge and error cases)

- **use_scenario_outline_when_needed**: Use Scenario Outline with Examples when story warrants concrete data: formulas need validation, domain has named entities, parameter variations exist. Example: Calculate ability modifier with Examples table Rank 10→0, Rank 12→+1, Rank 14→+2.
  DO: Scenario Outline for formulas, domain entities, or data variations. Example: Scenario Outline: Calculate modifier with Examples table showing input→output pairs
  DON'T: Don't use Scenario Outline for simple behaviors. Example: Scenario Outline: User clicks button (too simple - use regular scenario)

- **write_concrete_scenarios**: Parameterize domain concepts in scenarios using {Concept} notation for objects and {Concept.property} for specific attributes. Every {parameter} in Background/Steps MUST have corresponding example table. Use object references, not column names directly.
  DO: Use {Concept} for object references, {Concept.property} for specific attributes. Connect to example tables.
  DON'T: Don't hardcode values without examples, don't use non-domain placeholders, don't skip base data dependencies.

- **scenarios_on_story_docs**: Scenarios must be in story-graph.json (in scenarios or scenario_outlines fields), NOT in separate markdown files. NEVER create feature specification documents. Example: story-graph.json epics[].stories[].scenarios[], not docs/story/scenarios.md.
  DO: Add scenarios to story-graph.json. Example: story-graph.json epics[].stories[].scenarios[] array
  DON'T: Dont create separate scenario files or feature specifications. Example: docs/story/Epic/Feature/Feature Specification.md (wrong)

- **map_table_columns_to_scenario_parameters**: Map example tables to {Concept} references bidirectionally. Every example table maps to a {Concept} in Background/Steps. Use {Concept} for object references and {Concept.property} for specific attributes. Keep tables minimal and domain-focused.
  DO: Bidirectional mapping: Example table name ↔ {Concept} reference in steps.
  DON'T: Don't use <column_name> notation - use {Concept} or {Concept.property}. Don't have orphaned tables or references.

### Key Questions

- What system and user actions initiate this story's flow?
- What is the intended system response after each user action?
- What preconditions or data states are required before this story can begin?
- What are the success criteria for the story (from a domain and user perspective)?
- What are the expected alternate flows, error paths, and edge cases?
- Are there any mandatory sequencing constraints within or across stories?
- What domain rules, calculations, or business policies does this story validate?
- Is the story testable independently (including setup and teardown conditions)?
- What external systems or services does this story need to interact with?
- What requests, responses, or contracts are involved in those system interactions?
- Are there system integration points that require validation or simulation?
- How do we handle failures, timeouts, or retries for those system calls?
- What data variations (e.g., boundary conditions, common examples) are required for test coverage?
- What are the input values needed to test each scenario?
- What are the expected output values for each input?
- Are there formulas or calculations that need multiple data points to validate?
- Are there domain entities with named values that should be tested?
- What are the boundary conditions (min, max, edge cases) for each data point?

### Evidence

Acceptance criteria from Exploration stage (Domain AC at feature level, Behavioral AC at story level), High fidelity UX flows, Cross-functional walkthrough outputs, Integration contracts or API mocks, Behavior diagrams (state, sequence)

### Decisions

**Your Decisions:**

**examples_representation:**
  Verification Data Table

**scenario_outline:**
  Scenario Outline with Examples

**scenario_coverage:**
  - Happy Path
  - Edge Cases


### Assumptions

**Your Assumptions:**

- One story is specified at a time
- Acceptance criteria must be testable, unambiguous, and executable
- Gherkin syntax or structured language (Given/When/Then) is preferred
- Scenarios are written in plain English. When using Scenario Outline, variables are clearly marked and defined in Examples tables with actual test data.
- Examples tables when used must include ALL variables used in scenario steps
- Examples tables when used must have exact values for both input AND output variables
- Every variable when used in scenario steps must have a corresponding column in Examples table
- Examples tables when used must have actual test data, not placeholders
- Output/expected result variables must be included in Examples tables when used
- scnarios follow this pattern
- bulk of business logic tests done against the domain layer objects directly
- minimal happy path testing done with separate tgests that go theoiugh CLI
- JS nodetest for panel test focus on rendering and button layout

---
## Next action: validate
**Next:** Perform the following action. Fix any errors found in the Violation.

## Action Instructions - validate

The purpose of this action is to validate story graph and/or artifacts against behavior-specific rules, checking for violations and compliance

specification_scenarios: validate scenario structure and domain language usage
Validate that scenarios use proper domain terminology and reference domain concepts correctly

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

## Step 1: Run Scanners Then Review Violations

**Scanners you must run (with params below). Do not assume pre-run results.**

| Rule | Rule file | Scanner module |
|------|-----------|----------------|
| Scenario Language Matches Domain | `story_bot/behaviors/scenarios/rules/scenario_language_matches_domain.json` | `scanners.scenarios.scenario_language_scanner.ScenarioLanguageScanner` |
| Example Tables Use Domain Language | `story_bot/behaviors/scenarios/rules/example_tables_use_domain_language.json` | `scanners.scenarios.example_table_scanner.ExampleTableScanner` |
| Given Describes State Not Actions | `story_bot/behaviors/scenarios/rules/given_describes_state_not_actions.json` | `scanners.scenarios.given_state_not_actions_scanner.GivenStateNotActionsScanner` |
| Background Vs Scenario Setup | `story_bot/behaviors/scenarios/rules/background_vs_scenario_setup.json` | `scanners.scenarios.background_common_setup_scanner.BackgroundCommonSetupScanner` |
| Scenarios Cover All Cases | `story_bot/behaviors/scenarios/rules/scenarios_cover_all_cases.json` | `scanners.scenarios.scenarios_cover_all_cases_scanner.ScenariosCoverAllCasesScanner` |
| Use Scenario Outline When Needed | `story_bot/behaviors/scenarios/rules/use_scenario_outline_when_needed.json` | `scanners.scenarios.scenario_outline_scanner.ScenarioOutlineScanner` |
| Write Concrete Scenarios | `story_bot/behaviors/scenarios/rules/write_concrete_scenarios.json` | `scanners.scenarios.parameterized_scenarios_scanner.ParameterizedScenariosScanner` |
| Scenarios On Story Docs | `story_bot/behaviors/scenarios/rules/scenarios_on_story_docs.json` | `scanners.scenarios.scenarios_on_story_docs_scanner.ScenariosOnStoryDocsScanner` |
| Map Table Columns To Scenario Parameters | `story_bot/behaviors/scenarios/rules/map_table_columns_to_scenario_parameters.json` | `scanners.table_column_parameter_scanner.TableColumnParameterScanner` |

**Params to pass when running scanners:**
- **Scope:** all epics, sub-epics, stories, and domain concepts in the story graph
- **Workspace:** `C:\dev\agile_bots`
- **Story graph path:** `docs/story/story-graph.json` (or behavior-specific path)

Run each scanner with the above scope and workspace; then report violations and fix the story graph as needed.

Run each scanner with the params above, then review the violations they report as follows:
1. For each violation message, locate the corresponding element in the story graph.
2. Open the relevant rule file and read all DO and DON'T examples thoroughly.
3. Decide if the violation is **Valid** (truly a rule breach per examples) or a **False Positive** (explain why if so).
4. Determine the **Root Cause** (e.g., 'incorrect concept naming', 'missing actor', etc.).
5. Assign a **Theme** grouping based on the type of issue (e.g., 'noun-only naming', 'incomplete acceptance criteria').
6. Extract an **Example** from the actual code/content showing the problem.
7. Suggest a clear, concrete **Fix** with a code example informed by DO examples in the rule.

## Step 2: Manual Rule Review

**Rules to validate against (read each file for full DO/DON'T examples):**

### Rule: Scenario Language Matches Domain (Priority 1) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/scenario_language_matches_domain.json`
**Description:** Scenario language MUST use domain concept terminology. Given/When/Then steps should reference domain entities and concepts, not UI elements or technical implementation details.
**DO:** Use domain language in scenario steps - reference domain concepts by name.
**DON'T:** Don't use UI element names, technical implementation terms, or generic words instead of domain concepts.

### Rule: Example Tables Use Domain Language (Priority 2) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/example_tables_use_domain_language.json`
**Description:** Example tables MUST be grounded in scenario steps AND use domain-rich language. Table columns = nouns from Given/When/Then steps. Use domain terminology, not UI elements. Omit ID columns used purely for linking tables - relationships are expressed via collaboration field and table ordering. Concrete values with domain context, not generic JSON or placeholders. Use source entity data, not aggregated/calculated values - this is the stage where you figure out the real examples.
**DO:** Ground tables in scenario nouns, use domain terminology, connect tables using domain responsibility sentences. Omit implementation IDs. Show source entities, not derived counts.
**DON'T:** Don't use UI elements, flat lookup tables, generic JSON, abstract descriptions, invented terminology, or aggregated/calculated values.

### Rule: Given Describes State Not Actions (Priority 3) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/given_describes_state_not_actions.json`
**Description:** Given statements describe STATE/PRECONDITIONS, not actions or functionality. Given = what exists before test. When = first action. Then = expected behavior. Example: Given user is logged in (state), not Given user logs in (action).
**DO:** Given describes state/preconditions only. Example: 'Given user is logged in' (state), 'Given character sheet exists' (precondition)
**DON'T:** Don't describe actions, UI navigation, or functionality in Given. Example: 'Given user logs in' (action - wrong), 'Given User is on PaymentDetails step' (navigation - wrong)

### Rule: Background Vs Scenario Setup (Priority 4) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/background_vs_scenario_setup.json`
**Description:** Background = shared setup for 3+ scenarios (Given/And only, no When/Then). Background steps MUST use {Concept} notation to reference domain objects. Use {Concept.property} when a specific attribute is important. Don't repeat Background in Steps.
**DO:** Use Background for shared context with {Concept} references to example tables.
**DON'T:** Don't use hardcoded values or column names in Background - use {Concept} notation. Don't include When/Then.

### Rule: Scenarios Cover All Cases (Priority 5) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/scenarios_cover_all_cases.json`
**Description:** Scenarios must cover happy path, edge cases, and error cases based on acceptance criteria. Example: Valid input → success; Boundary value → validates; Invalid input → error message.
**DO:** Cover all case types: happy path, edge cases, error cases. Example: User enters valid data → success; User enters boundary → validates; User enters invalid → error
**DON'T:** Don't skip case types. Example: Only happy path scenarios (missing edge and error cases)

### Rule: Use Scenario Outline When Needed (Priority 6) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/use_scenario_outline_when_needed.json`
**Description:** Use Scenario Outline with Examples when story warrants concrete data: formulas need validation, domain has named entities, parameter variations exist. Example: Calculate ability modifier with Examples table Rank 10→0, Rank 12→+1, Rank 14→+2.
**DO:** Scenario Outline for formulas, domain entities, or data variations. Example: Scenario Outline: Calculate modifier with Examples table showing input→output pairs
**DON'T:** Don't use Scenario Outline for simple behaviors. Example: Scenario Outline: User clicks button (too simple - use regular scenario)

### Rule: Write Concrete Scenarios (Priority 7) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/write_concrete_scenarios.json`
**Description:** Parameterize domain concepts in scenarios using {Concept} notation for objects and {Concept.property} for specific attributes. Every {parameter} in Background/Steps MUST have corresponding example table. Use object references, not column names directly.
**DO:** Use {Concept} for object references, {Concept.property} for specific attributes. Connect to example tables.
**DON'T:** Don't hardcode values without examples, don't use non-domain placeholders, don't skip base data dependencies.

### Rule: Scenarios On Story Docs (Priority 8) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/scenarios_on_story_docs.json`
**Description:** Scenarios must be in story-graph.json (in scenarios or scenario_outlines fields), NOT in separate markdown files. NEVER create feature specification documents. Example: story-graph.json epics[].stories[].scenarios[], not docs/story/scenarios.md.
**DO:** Add scenarios to story-graph.json. Example: story-graph.json epics[].stories[].scenarios[] array
**DON'T:** Dont create separate scenario files or feature specifications. Example: docs/story/Epic/Feature/Feature Specification.md (wrong)

### Rule: Map Table Columns To Scenario Parameters (Priority 9) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/map_table_columns_to_scenario_parameters.json`
**Description:** Map example tables to {Concept} references bidirectionally. Every example table maps to a {Concept} in Background/Steps. Use {Concept} for object references and {Concept.property} for specific attributes. Keep tables minimal and domain-focused.
**DO:** Bidirectional mapping: Example table name ↔ {Concept} reference in steps.
**DON'T:** Don't use <column_name> notation - use {Concept} or {Concept.property}. Don't have orphaned tables or references.


Scanner tools don't cover or catch every rule violation. Do a second pass:
1. Carefully read each rule file, fully reviewing DO and DON'T sections, and every provided example.
2. Inspect all epics, sub-epics, stories, and domain concepts in the story graph for compliance.
3. Compare the properties and content of each element against the rule's requirements.
4. Document any violations the scanner could not find.
5. For each violation, extract an **Example** showing the problem and provide a **Fix** with code example.

## Violations Found

Record ALL findings (scanner + manual) using this readable format. Group by theme for narrow IDE chat panels:

### [Theme Name] (X violations)

**1. [Rule Name]**
- Location: `path.to.element`
- Status: Valid / False Positive
- Source: Scanner / Manual / Both
- Problem: `"actual problematic text"`
- Fix: `"corrected text"`
- Root Cause: Brief explanation

**2. [Rule Name]**
- Location: `path.to.element`
- ...

---

### [Next Theme] (Y violations)
...

Use this list format instead of tables - tables are unreadable in narrow IDE side chat panels.

## Step 3: Summarize Findings & Recommendations

Provide a concise summary:
- Report how many **scanner violations** were valid vs false positives.
- Enumerate any **additional manual findings** not caught by scanners.
- Group all violations by recurring theme or pattern.
- Split violations into **Priority Fixes** (must resolve before continuing) and **Optional Improvements**.

Present your summary and await user confirmation before automatically applying or proposing corrections.
specification_scenarios: validate scenario structure and domain language usage
Validate that scenarios use proper domain terminology and reference domain concepts correctly

---
## Next action: render
**Next:** Perform the following action.

## Action Instructions - render

The purpose of this action is to render output documents and artifacts from story graph using templates and synchronizers

specification_scenarios: render story documents with scenarios

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

Please follow the instructions below in order to manually render output documents using templates

All render configurations are automatically loaded and injected below. Process ALL configs - do not skip any.



**Final Steps:**
- Process ALL configs above - do not skip any
- Priority order: synchronizer > template
- Verify each output file exists after execution
- If execution fails, report the error and continue with other outputs
- After completing all renders, pause and wait for human confirmation before proceeding to next behavior

**Creating New Render Outputs:**
If you need to create code to render a new output format:
1. Create a new synchronizer file in {workspace}/synchronizers/ (create folder if it doesn't exist)
2. Follow this signature pattern: output_file = synchronizer.render(story_graph_file)
3. The synchronizer should read the story-graph.json and produce the desired output file
4. Add the new synchronizer to the behavior's render config to include it in future renders
specification_scenarios: render story documents with scenarios
IMPORTANT: After completing all template-based rendering, you MUST execute the synchronizer-based render specs by running: scenarios.render.renderAll
This will render the following outputs: render_story_scenarios

---
## Next action: tests.build
**Next:** Perform the following action.

## Action Instructions - build

The purpose of this action is to build story graph from content area and render using story graph renderer

write test files (.py, .js, etc.) with executable test code based on the scenarios you have made within the story-graph.json file
After writing test files, update story-graph.json with further test_file, test_class, and test_method mapping changes you have made
| Field | Level | Format | Example |
|-------|-------|--------|---------|
| test_file | sub_epic | "test/<domain|CLI|panel>/test_<sub_epic>.py" | "test/domain/test_edit_story_graph.py" |
| test_class | story | "Test<StoryName>" | "TestCreatesChildStoryNode" |
| test_method | scenario | "test_<scenario_name>" | "test_user_creates_child_under_epic" |

Hierarchy: epic → sub_epic(test_file) → story_group → story(test_class) → scenario(test_method)

Rules:
- One test_file per sub_epic (all stories share it)
- One test_class per story (only if story has scenarios)
- One test_method per scenario
- Read story-graph.json first, preserve existing fields

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

@build-instructions.txt

**BUILD PROCESS:**

**1. Load Context**
Load clarification.json, planning.json, and source material from context sources (listed above).

**2. Load Build Configs**
From `c:\dev\agile_bots\bots\story_bot/behaviors/tests/content/`, each folder contains:
- `build_*.json` - Config (name, path, template, output)
- `instructions.json` - Build instructions
- `template-file.json` - Output schema/structure

**3. Execute Build**
1. Load config, instructions, and template (injected as 'story_graph_template')
2. Check if output file exists - read it FIRST
3. Follow instructions.json - match template structure exactly (check '_explanation' section)
4. Apply context from Step 1
5. If file exists: ADD/EXTEND only, never overwrite/delete
6. Validate against template schema
7. Write to `C:\dev\agile_bots/{config.path}/{config.output}`
- Read existing files before changes - preserve all content
- Match template structure exactly - don't invent schemas
- Trace all knowledge to clarification/planning data
- Process builds sequentially - validate each

**4. SOURCE TRACEABILITY**
Knowledge artifacts should include source references when available:
- `context_source` field on epics, sub_epics, story_groups, stories, and domain concepts
- Format: `{"file": "filename.pdf", "page": "12", "section": "3.2.1 Payment Flow"}`
- For multiple sources: use array of source objects
- If source is chat/conversation: `{"type": "chat", "description": "User clarification on approval workflow"}`
- If source is code: `{"file": "path/to/file.py", "lines": "45-67", "function": "process_payment"}`
- Prefer tracing knowledge to a source when possible
- When source is unclear, mark as `{"type": "inferred", "basis": "description of inference basis"}`
write test files (.py, .js, etc.) with executable test code based on the scenarios you have made within the story-graph.json file
After writing test files, update story-graph.json with further test_file, test_class, and test_method mapping changes you have made
| Field | Level | Format | Example |
|-------|-------|--------|---------|
| test_file | sub_epic | "test/<domain|CLI|panel>/test_<sub_epic>.py" | "test/domain/test_edit_story_graph.py" |
| test_class | story | "Test<StoryName>" | "TestCreatesChildStoryNode" |
| test_method | scenario | "test_<scenario_name>" | "test_user_creates_child_under_epic" |

Hierarchy: epic → sub_epic(test_file) → story_group → story(test_class) → scenario(test_method)

Rules:
- One test_file per sub_epic (all stories share it)
- One test_class per story (only if story has scenarios)
- One test_method per scenario
- Read story-graph.json first, preserve existing fields

When building or adding to the story graph follow these rules,
Rules to follow:

- **use_class_based_organization**: CRITICAL STRUCTURAL RULE: Test structure matches story graph hierarchy. File = sub-epic (test_<sub_epic>.py), Class = story (Test<ExactStoryName>), Method = scenario (test_<scenario_snake_case>). Getting this wrong creates files in wrong locations requiring deletion/recreation. BEFORE writing any test code, identify the parent sub-epic that contains the story.
  DO: Map story hierarchy to test structure exactly. CRITICAL: File name comes from SUB-EPIC, not story.
  DON'T: Don't use generic/abbreviated names or wrong hierarchy level for file naming. Don't create files in wrong locations.

- **use_domain_language**: Use Ubiquitous Language (DDD): Same vocabulary in domain model, stories, scenarios, AND code. Class names = domain entities/nouns. Method names = domain responsibilities/verbs. Test names read like plain English stories. Example: test_agent_loads_configuration_when_file_exists (not test_agt_init_sets_vars)
  DO: Use domain language for classes, methods, and test names. Example: class GatherContextAction, def inject_guardrails(), test_agent_loads_config_when_file_exists
  DON'T: Don't use generic technical terms or implementation-specific names. Example: class StdioHandler (wrong), def execute_with_guardrails (wrong), test_agt_init_sets_vars (wrong)

- **consistent_vocabulary**: Use ONE word per concept across entire codebase. Pick consistent vocabulary: create (not build/make/construct), verify (not check/assert/validate), load (not fetch/get/retrieve). Use intention-revealing names that describe behavior. Example: create_agent(), verify_initialized(), load_config() - same verbs everywhere
  DO: Use same word for same concept everywhere. Example: create_agent(), create_config(), create_workspace() - all use 'create'
  DON'T: Don't mix synonyms for same concept. Example: create_agent() + build_config() + make_workspace() (wrong - pick one verb)

- **domain_oriented_test_inheritance**: Scaling extension of helper_extraction_and_reuse, object_oriented_test_helpers, and standard_test_data_sets. At small scale, a single test class covering multiple domain objects is fine. As domain objects develop distinct behavior, break out into domain-specific test classes. Use abstract base classes for common operations. Share parameter data and fixtures only when there is obvious shared logic across sub-epics. Place shared base files at the appropriate hierarchy level.
  DO: At small scale keep together. As you scale, use abstract bases, share fixtures only with explicit need, and place shared files at the right hierarchy level.
  DON'T: When scaling, do not copy assertion logic, do not create shared files preemptively, and do not group tests by operation or technology.

- **no_defensive_code_in_tests**: Tests must NEVER contain guard clauses, defensive conditionals, or fallback paths. We control test setup - if it's wrong, the test MUST fail immediately. Guard clauses hide problems. Tests should assume positive outcomes. Example: Just call the code directly, don't wrap in if-checks
  DO: Assume correct setup - let test fail if wrong. Example: behavior = Behavior(name='shape') then assert behavior.name == 'shape'
  DON'T: Don't add if-checks, type guards, or fallback handling in tests. Example: if behavior_file.exists(): (wrong - test should fail if it doesn't)

- **production_code_clean_functions**: Production code functions should do ONE thing, be under 20 lines, and have one level of abstraction. No hidden side effects. Name reveals complete behavior. Extract multiple concerns into separate functions. Example: load_config(), validate_config(), apply_config() - each does one thing
  DO: Single responsibility, small focused functions. Example: initialize_from_config() calls validate_exists(), load_config(), validate_structure(), apply_config()
  DON'T: Don't make functions that do multiple unrelated things or are too long. Example: 50-line function that loads, validates, and applies config

- **bug_fix_test_first**: When production code breaks, follow test-first workflow: write failing test, verify failure, fix code, verify success. Never fix bugs without a failing test first. Example: test_mcp_tool_initializes_bot() fails -> fix initialization -> test passes
  DO: Follow RED-GREEN-PRODUCTION workflow. Example: Write test reproducing bug -> Run test (RED) -> Fix minimal code -> Run test (GREEN) -> Run full suite
  DON'T: Don't fix bugs directly without failing test first. Example: Editing production code without test -> deploying -> hoping it works (wrong)

- **call_production_code_directly**: Call production code directly in tests. Let tests fail naturally if code doesn't exist. Don't comment out calls, mock business logic, or fake state. Only mock external boundaries. Example: agent = Agent(); agent.initialize() (not agent = Mock())
  DO: Call production code directly, let it fail naturally. Example: agent = Agent(workspace); agent.initialize(config); assert agent.is_initialized
  DON'T: Don't mock class under test, comment out calls, or fake state. Example: agent = Mock(spec=Agent) (wrong); agent._initialized = True (wrong)

- **cover_all_behavior_paths**: Cover all behavior paths: normal (happy path), edge cases, and failure scenarios. Each distinct behavior needs its own focused test. Tests must be independent. Example: test_loads_valid_config(), test_loads_empty_config(), test_raises_error_when_file_missing()
  DO: Test normal, edge, and failure paths separately. Example: test_loads_valid_config() (happy), test_loads_empty_config() (edge), test_raises_when_missing() (failure)
  DON'T: Don't test only happy path or combine multiple behaviors in one test. Example: Single test for both success and failure (wrong)

- **mock_only_boundaries**: Mock ONLY at architectural boundaries: external APIs, network, uncontrollable services. Don't mock internal business logic, classes under test, or file operations (use temp files). Example: patch('requests.get') (OK); patch('agent.validate') (wrong)
  DO: Mock only external dependencies you can't control. Example: with patch('requests.get') as mock: (external API - OK to mock)
  DON'T: Don't mock internal logic, class under test, or file I/O. Example: with patch('agent.validate_config') (wrong - test the logic!)

- **create_parameterized_tests_for_scenarios**: If scenarios have Examples tables, create parameterized tests using @pytest.mark.parametrize. Each row becomes a test case. Don't write single tests that only test one example. Example: @pytest.mark.parametrize('input,expected', [(1, 2), (3, 4)])
  DO: Create parameterized tests from Examples tables. Example: @pytest.mark.parametrize('paths,count', [(['p1','p2'], 2), (['p3'], 1)])
  DON'T: Don't hardcode single example or duplicate test methods. Example: def test_with_value_1(): (wrong); def test_with_value_2(): (wrong - use parametrize)

- **define_fixtures_in_test_file**: Define fixtures in the test file, not separate conftest.py. Truly reusable fixtures (file ops, location helpers) go in base conftest.py. Example: @pytest.fixture def workspace_root(tmp_path): return tmp_path / 'workspace'
  DO: Define fixtures in same test file. Example: @pytest.fixture def config_file(tmp_path): ... (in test_agent.py)
  DON'T: Don't create separate conftest.py for agent-specific fixtures. Don't create shared files without explicit need.

- **design_api_through_failing_tests**: Write tests against the REAL expected API BEFORE implementing code. Tests MUST fail initially. Set up real test data and call real API. Failure reveals complete API design. Example: project = Project(path=path); project.initialize() (doesn't exist yet -> fails -> drives implementation)
  DO: Write test against real expected API that fails initially. Example: project = Project(path); project.initialize(); assert project.is_ready (fails until implemented)
  DON'T: Don't use placeholders, dummy values, or skip the failing step. Example: project = 'TODO' (wrong); assuming test passes first (wrong)

- **test_observable_behavior**: Test observable behavior, not implementation details. Verify public API and visible state changes. Don't assert on private methods or internal flags. Example: assert agent.config_path.exists() (observable); not assert agent._internal_flag (private)
  DO: Test observable outcomes through public API. Example: assert agent.config_path == expected; assert agent.is_initialized (public properties)
  DON'T: Don't test private state or implementation details. Example: assert agent._initialized (wrong); assert agent._config_cache (wrong)

- **helper_extraction_and_reuse**: Extract duplicate test setup to reusable helper functions. Keep test bodies focused on specific behavior. Example: create_agent_with_config(), create_config_file(), verify_agent_initialized() - reusable across tests
  DO: Extract duplicate setup to reusable helpers. Example: create_agent_with_config(name, workspace, config) returns initialized Agent
  DON'T: Don't duplicate setup code across tests. Example: Same 10 lines of setup in every test method (wrong - extract to helper)

- **match_specification_scenarios**: Tests must match specification scenarios exactly. Test names, steps, and assertions verify exactly what the scenario states. Use exact variable names and terminology from specification. Example: agent_name='story_bot' (from spec), not name='bot'
  DO: Test matches specification exactly. Example: GIVEN config exists, WHEN Agent(agent_name='story_bot'), THEN config_path == agents/base/agent.json
  DON'T: Don't use different terminology or assert things not in specification. Example: assert agent._internal_flag (not in spec - wrong)

- **place_imports_at_top**: Place all imports at top of test file, after docstrings, before code. Group: stdlib, third-party, then local. Example: import json; import pytest; from mymodule import MyClass
  DO: All imports at top, grouped by type. Example: import json; import pytest; from agile_bot.bots... import X
  DON'T: Don't place imports inside functions or after code. Example: def test(): from pathlib import Path (wrong - import inside function)

- **object_oriented_test_helpers**: Consolidate tests around object-oriented helpers/factories (e.g., BotTestHelper test hopper) that build complete domain objects with standard data. Example: helper = BotTestHelper(tmp_path); helper.set_state('shape','clarify'); helper.assert_at_behavior_action('shape','clarify'). Avoid scattering many primitive parameters across parametrize blocks or inline setups.
  DO: Use shared helper objects to create full test fixtures and assert against complete domain objects, not fragments.
  DON'T: Do not spread test setup across many primitive parameters or cherry-pick single values from partial objects.

- **production_code_explicit_dependencies**: Production code: make dependencies explicit through constructor injection. Pass all external dependencies as constructor parameters. No hidden global state. Tests easily inject test doubles. Example: Agent(config_loader=loader, domain_graph=graph)
  DO: Inject all dependencies through constructor. Example: def __init__(self, config_loader, domain_graph): self._loader = config_loader
  DON'T: Don't access globals, singletons, or create dependencies internally. Example: self._loader = ConfigLoader() (wrong - creates internally)

- **self_documenting_tests**: Tests are self-documenting through code structure. Don't add verbose comments explaining failures. Imports, calls, and assertions show the API design. Let code speak for itself. Example: generator = MCPServerGenerator(bot_name, config_path); server = generator.generate_server()
  DO: Let code structure document the test. Example: generator = MCPServerGenerator(name, config); file = generator.generate() - API is clear
  DON'T: Don't add verbose comments explaining obvious things. Example: # This will fail because API doesn't exist yet (unnecessary)

- **standard_test_data_sets**: Use standard, named test data sets across tests instead of recreating ad-hoc values. Example: STANDARD_STATE = {...}; helper.set_state(...); assert helper.get_state() == STANDARD_STATE.
  DO: Define canonical data once (helper constants/factories) and reuse it so every test exercises the full domain object.
  DON'T: Do not create new ad-hoc values per test or assert only one field from a complex object.

- **assert_full_results**: Assert full domain results (state/log/graph objects), not single cherry-picked fields. Example: assert helper.get_state() == STANDARD_STATE, not assert helper.get_state()['current'] == 'shape.clarify'.
  DO: Compare entire objects/dicts/dataclasses against standard data fixtures.
  DON'T: Do not assert single fields or lengths when validating complex results.

- **use_ascii_only**: All test code must use ASCII-only characters. No Unicode symbols, emojis, or special characters. Use plain ASCII alternatives. Example: print('[PASS] Success') not print('[checkmark] Success')
  DO: Use ASCII-only characters. Example: print('[PASS] Agent initialized'); print('[ERROR] Config not found')
  DON'T: Don't use Unicode or emojis. Example: print('[checkmark] Done') (wrong); print('[green_check] OK') (wrong)

- **pytest_bdd_orchestrator_pattern**: Use pytest with orchestrator pattern for story-based tests. NO FEATURE FILES. Test classes contain orchestrator methods (under 20 lines) showing Given-When-Then flow by calling helper functions. Example: def test_agent_loads_config(): given_config_exists(); agent = when_agent_initialized(); then_agent_is_configured(agent)
  DO: Orchestrator pattern: test shows flow, delegates to helpers. Example: # Given; create_config_file(); # When; agent.initialize(); # Then; assert agent.is_initialized
  DON'T: Don't use feature files or inline complex setup. Example: @given('config exists') def step(): ... (wrong - use pytest directly)

- **use_exact_variable_names**: Use exact variable names from specification scenarios. When spec mentions agent_name, workspace_root, config_path - use those exact names in tests and production code. Example: agent_name = 'story_bot' (from spec), not name = 'story_bot'
  DO: Use exact names from specification in tests and production. Example: agent_name, workspace_root, config_path - all from spec
  DON'T: Don't use different names than specification. Example: name = 'bot' when spec says agent_name (wrong)

- **use_given_when_then_helpers**: Use reusable helper functions instead of inline code blocks of 4+ lines. Optimize for reusability, not exact step names. Place helpers at correct scope: story-level in class, sub-epic in module, epic in separate file. Example: given_config_exists(), when_agent_initialized(), then_agent_is_configured()
  DO: Use Given/When/Then helper functions for setup, action, assertion. Example: given_bot_config_exists(); bot = when_bot_instantiated(); then_bot_uses_correct_directories(bot)
  DON'T: Don't use inline operations of 4+ lines. Example: config_dir = ...; config_dir.mkdir(); config_file = ...; config_file.write_text() (wrong - extract to helper)

---
## Next action: tests.validate
**Next:** Perform the following action. Fix any errors found in the Violation.

## Action Instructions - validate

The purpose of this action is to validate story graph and/or artifacts against behavior-specific rules, checking for violations and compliance

specification_tests: validate test code and domain language usage
Validate that test code uses proper domain terminology (class names = domain entities, method names = domain responsibilities)
Validate that all test files, classes, and methods are properly mapped to story-graph.json

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

## Step 1: Run Scanners Then Review Violations

**Scanners you must run (with params below). Do not assume pre-run results.**

| Rule | Rule file | Scanner module |
|------|-----------|----------------|
| Use Class Based Organization | `story_bot/behaviors/tests/rules/use_class_based_organization.json` | `scanners.code.python.class_based_organization_scanner.ClassBasedOrganizationScanner` |
| Use Domain Language | `story_bot/behaviors/tests/rules/use_domain_language.json` | `scanners.code.python.domain_language_code_scanner.DomainLanguageCodeScanner` |
| Consistent Vocabulary | `story_bot/behaviors/tests/rules/consistent_vocabulary.json` | `scanners.code.python.consistent_vocabulary_scanner.ConsistentVocabularyScanner` |
| Domain Oriented Test Inheritance | `story_bot/behaviors/tests/rules/domain_oriented_test_inheritance.json` | `scanners.code.python.duplicate_assertion_scanner.DuplicateAssertionScanner` |
| No Defensive Code In Tests | `story_bot/behaviors/tests/rules/no_defensive_code_in_tests.json` | `scanners.code.python.excessive_guards_scanner.ExcessiveGuardsScanner` |
| Production Code Clean Functions | `story_bot/behaviors/tests/rules/production_code_clean_functions.json` | `scanners.code.python.function_size_scanner.FunctionSizeScanner` |
| Bug Fix Test First | `story_bot/behaviors/tests/rules/bug_fix_test_first.json` | `scanners.bug_fix_test_first_scanner.BugFixTestFirstScanner` |
| Call Production Code Directly | `story_bot/behaviors/tests/rules/call_production_code_directly.json` | `scanners.code.python.real_implementations_scanner.RealImplementationsScanner` |
| Cover All Behavior Paths | `story_bot/behaviors/tests/rules/cover_all_behavior_paths.json` | `scanners.code.python.cover_all_paths_scanner.CoverAllPathsScanner` |
| Mock Only Boundaries | `story_bot/behaviors/tests/rules/mock_only_boundaries.json` | `scanners.code.python.mock_boundaries_scanner.MockBoundariesScanner` |
| Create Parameterized Tests For Scenarios | `story_bot/behaviors/tests/rules/create_parameterized_tests_for_scenarios.json` | `scanners.parameterized_tests_scanner.ParameterizedTestsScanner` |
| Define Fixtures In Test File | `story_bot/behaviors/tests/rules/define_fixtures_in_test_file.json` | `scanners.code.python.fixture_placement_scanner.FixturePlacementScanner` |
| Design Api Through Failing Tests | `story_bot/behaviors/tests/rules/design_api_through_failing_tests.json` | `scanners.failing_test_api_scanner.FailingTestApiScanner` |
| Test Observable Behavior | `story_bot/behaviors/tests/rules/test_observable_behavior.json` | `scanners.code.python.observable_behavior_scanner.ObservableBehaviorScanner` |
| Helper Extraction And Reuse | `story_bot/behaviors/tests/rules/helper_extraction_and_reuse.json` | `scanners.helper_extraction_scanner.HelperExtractionScanner` |
| Match Specification Scenarios | `story_bot/behaviors/tests/rules/match_specification_scenarios.json` | `scanners.specification_match_scanner.SpecificationMatchScanner` |
| Place Imports At Top | `story_bot/behaviors/tests/rules/place_imports_at_top.json` | `scanners.code.python.import_placement_scanner.ImportPlacementScanner` |
| Object Oriented Test Helpers | `story_bot/behaviors/tests/rules/object_oriented_test_helpers.json` | `scanners.code.python.object_oriented_helpers_scanner.ObjectOrientedHelpersScanner` |
| Production Code Explicit Dependencies | `story_bot/behaviors/tests/rules/production_code_explicit_dependencies.json` | `scanners.code.python.explicit_dependencies_scanner.ExplicitDependenciesScanner` |
| Self Documenting Tests | `story_bot/behaviors/tests/rules/self_documenting_tests.json` | `scanners.code.python.intention_revealing_names_scanner.IntentionRevealingNamesScanner` |
| Standard Test Data Sets | `story_bot/behaviors/tests/rules/standard_test_data_sets.json` | `scanners.code.python.standard_data_reuse_scanner.StandardDataReuseScanner` |
| Assert Full Results | `story_bot/behaviors/tests/rules/assert_full_results.json` | `scanners.code.python.full_result_assertions_scanner.FullResultAssertionsScanner` |
| Use Ascii Only | `story_bot/behaviors/tests/rules/use_ascii_only.json` | `scanners.code.python.ascii_only_scanner.AsciiOnlyScanner` |
| Pytest Bdd Orchestrator Pattern | `story_bot/behaviors/tests/rules/pytest_bdd_orchestrator_pattern.json` | `scanners.orchestrator_pattern_scanner.OrchestratorPatternScanner` |
| Use Exact Variable Names | `story_bot/behaviors/tests/rules/use_exact_variable_names.json` | `scanners.code.python.exact_variable_names_scanner.ExactVariableNamesScanner` |
| Use Given When Then Helpers | `story_bot/behaviors/tests/rules/use_given_when_then_helpers.json` | `scanners.code.python.given_when_then_helpers_scanner.GivenWhenThenHelpersScanner` |

**Params to pass when running scanners:**
- **Scope:** all epics, sub-epics, stories, and domain concepts in the story graph
- **Workspace:** `C:\dev\agile_bots`
- **Story graph path:** `docs/story/story-graph.json` (or behavior-specific path)

Run each scanner with the above scope and workspace; then report violations and fix the story graph as needed.

Run each scanner with the params above, then review the violations they report as follows:
1. For each violation message, locate the corresponding element in the story graph.
2. Open the relevant rule file and read all DO and DON'T examples thoroughly.
3. Decide if the violation is **Valid** (truly a rule breach per examples) or a **False Positive** (explain why if so).
4. Determine the **Root Cause** (e.g., 'incorrect concept naming', 'missing actor', etc.).
5. Assign a **Theme** grouping based on the type of issue (e.g., 'noun-only naming', 'incomplete acceptance criteria').
6. Extract an **Example** from the actual code/content showing the problem.
7. Suggest a clear, concrete **Fix** with a code example informed by DO examples in the rule.

## Step 2: Manual Rule Review

**Rules to validate against (read each file for full DO/DON'T examples):**

### Rule: Use Class Based Organization (Priority 1) [Scanner]
**File:** `story_bot/behaviors/tests/rules/use_class_based_organization.json`
**Description:** CRITICAL STRUCTURAL RULE: Test structure matches story graph hierarchy. File = sub-epic (test_<sub_epic>.py), Class = story (Test<ExactStoryName>), Method = scenario (test_<scenario_snake_case>). Getting this wrong creates files in wrong locations requiring deletion/recreation. BEFORE writing any test code, identify the parent sub-epic that contains the story.
**DO:** Map story hierarchy to test structure exactly. CRITICAL: File name comes from SUB-EPIC, not story.
**DON'T:** Don't use generic/abbreviated names or wrong hierarchy level for file naming. Don't create files in wrong locations.

### Rule: Use Domain Language (Priority 1) [Scanner]
**File:** `story_bot/behaviors/tests/rules/use_domain_language.json`
**Description:** Use Ubiquitous Language (DDD): Same vocabulary in domain model, stories, scenarios, AND code. Class names = domain entities/nouns. Method names = domain responsibilities/verbs. Test names read like plain English stories. Example: test_agent_loads_configuration_when_file_exists (not test_agt_init_sets_vars)
**DO:** Use domain language for classes, methods, and test names. Example: class GatherContextAction, def inject_guardrails(), test_agent_loads_config_when_file_exists
**DON'T:** Don't use generic technical terms or implementation-specific names. Example: class StdioHandler (wrong), def execute_with_guardrails (wrong), test_agt_init_sets_vars (wrong)

### Rule: Consistent Vocabulary (Priority 2) [Scanner]
**File:** `story_bot/behaviors/tests/rules/consistent_vocabulary.json`
**Description:** Use ONE word per concept across entire codebase. Pick consistent vocabulary: create (not build/make/construct), verify (not check/assert/validate), load (not fetch/get/retrieve). Use intention-revealing names that describe behavior. Example: create_agent(), verify_initialized(), load_config() - same verbs everywhere
**DO:** Use same word for same concept everywhere. Example: create_agent(), create_config(), create_workspace() - all use 'create'
**DON'T:** Don't mix synonyms for same concept. Example: create_agent() + build_config() + make_workspace() (wrong - pick one verb)

### Rule: Domain Oriented Test Inheritance (Priority 3) [Scanner]
**File:** `story_bot/behaviors/tests/rules/domain_oriented_test_inheritance.json`
**Description:** Scaling extension of helper_extraction_and_reuse, object_oriented_test_helpers, and standard_test_data_sets. At small scale, a single test class covering multiple domain objects is fine. As domain objects develop distinct behavior, break out into domain-specific test classes. Use abstract base classes for common operations. Share parameter data and fixtures only when there is obvious shared logic across sub-epics. Place shared base files at the appropriate hierarchy level.
**DO:** At small scale keep together. As you scale, use abstract bases, share fixtures only with explicit need, and place shared files at the right hierarchy level.
**DON'T:** When scaling, do not copy assertion logic, do not create shared files preemptively, and do not group tests by operation or technology.

### Rule: No Defensive Code In Tests (Priority 3) [Scanner]
**File:** `story_bot/behaviors/tests/rules/no_defensive_code_in_tests.json`
**Description:** Tests must NEVER contain guard clauses, defensive conditionals, or fallback paths. We control test setup - if it's wrong, the test MUST fail immediately. Guard clauses hide problems. Tests should assume positive outcomes. Example: Just call the code directly, don't wrap in if-checks
**DO:** Assume correct setup - let test fail if wrong. Example: behavior = Behavior(name='shape') then assert behavior.name == 'shape'
**DON'T:** Don't add if-checks, type guards, or fallback handling in tests. Example: if behavior_file.exists(): (wrong - test should fail if it doesn't)

### Rule: Production Code Clean Functions (Priority 4) [Scanner]
**File:** `story_bot/behaviors/tests/rules/production_code_clean_functions.json`
**Description:** Production code functions should do ONE thing, be under 20 lines, and have one level of abstraction. No hidden side effects. Name reveals complete behavior. Extract multiple concerns into separate functions. Example: load_config(), validate_config(), apply_config() - each does one thing
**DO:** Single responsibility, small focused functions. Example: initialize_from_config() calls validate_exists(), load_config(), validate_structure(), apply_config()
**DON'T:** Don't make functions that do multiple unrelated things or are too long. Example: 50-line function that loads, validates, and applies config

### Rule: Bug Fix Test First (Priority 5) [Scanner]
**File:** `story_bot/behaviors/tests/rules/bug_fix_test_first.json`
**Description:** When production code breaks, follow test-first workflow: write failing test, verify failure, fix code, verify success. Never fix bugs without a failing test first. Example: test_mcp_tool_initializes_bot() fails -> fix initialization -> test passes
**DO:** Follow RED-GREEN-PRODUCTION workflow. Example: Write test reproducing bug -> Run test (RED) -> Fix minimal code -> Run test (GREEN) -> Run full suite
**DON'T:** Don't fix bugs directly without failing test first. Example: Editing production code without test -> deploying -> hoping it works (wrong)

### Rule: Call Production Code Directly (Priority 6) [Scanner]
**File:** `story_bot/behaviors/tests/rules/call_production_code_directly.json`
**Description:** Call production code directly in tests. Let tests fail naturally if code doesn't exist. Don't comment out calls, mock business logic, or fake state. Only mock external boundaries. Example: agent = Agent(); agent.initialize() (not agent = Mock())
**DO:** Call production code directly, let it fail naturally. Example: agent = Agent(workspace); agent.initialize(config); assert agent.is_initialized
**DON'T:** Don't mock class under test, comment out calls, or fake state. Example: agent = Mock(spec=Agent) (wrong); agent._initialized = True (wrong)

### Rule: Cover All Behavior Paths (Priority 7) [Scanner]
**File:** `story_bot/behaviors/tests/rules/cover_all_behavior_paths.json`
**Description:** Cover all behavior paths: normal (happy path), edge cases, and failure scenarios. Each distinct behavior needs its own focused test. Tests must be independent. Example: test_loads_valid_config(), test_loads_empty_config(), test_raises_error_when_file_missing()
**DO:** Test normal, edge, and failure paths separately. Example: test_loads_valid_config() (happy), test_loads_empty_config() (edge), test_raises_when_missing() (failure)
**DON'T:** Don't test only happy path or combine multiple behaviors in one test. Example: Single test for both success and failure (wrong)

### Rule: Mock Only Boundaries (Priority 8) [Scanner]
**File:** `story_bot/behaviors/tests/rules/mock_only_boundaries.json`
**Description:** Mock ONLY at architectural boundaries: external APIs, network, uncontrollable services. Don't mock internal business logic, classes under test, or file operations (use temp files). Example: patch('requests.get') (OK); patch('agent.validate') (wrong)
**DO:** Mock only external dependencies you can't control. Example: with patch('requests.get') as mock: (external API - OK to mock)
**DON'T:** Don't mock internal logic, class under test, or file I/O. Example: with patch('agent.validate_config') (wrong - test the logic!)

### Rule: Create Parameterized Tests For Scenarios (Priority 9) [Scanner]
**File:** `story_bot/behaviors/tests/rules/create_parameterized_tests_for_scenarios.json`
**Description:** If scenarios have Examples tables, create parameterized tests using @pytest.mark.parametrize. Each row becomes a test case. Don't write single tests that only test one example. Example: @pytest.mark.parametrize('input,expected', [(1, 2), (3, 4)])
**DO:** Create parameterized tests from Examples tables. Example: @pytest.mark.parametrize('paths,count', [(['p1','p2'], 2), (['p3'], 1)])
**DON'T:** Don't hardcode single example or duplicate test methods. Example: def test_with_value_1(): (wrong); def test_with_value_2(): (wrong - use parametrize)

### Rule: Define Fixtures In Test File (Priority 10) [Scanner]
**File:** `story_bot/behaviors/tests/rules/define_fixtures_in_test_file.json`
**Description:** Define fixtures in the test file, not separate conftest.py. Truly reusable fixtures (file ops, location helpers) go in base conftest.py. Example: @pytest.fixture def workspace_root(tmp_path): return tmp_path / 'workspace'
**DO:** Define fixtures in same test file. Example: @pytest.fixture def config_file(tmp_path): ... (in test_agent.py)
**DON'T:** Don't create separate conftest.py for agent-specific fixtures. Don't create shared files without explicit need.

### Rule: Design Api Through Failing Tests (Priority 11) [Scanner]
**File:** `story_bot/behaviors/tests/rules/design_api_through_failing_tests.json`
**Description:** Write tests against the REAL expected API BEFORE implementing code. Tests MUST fail initially. Set up real test data and call real API. Failure reveals complete API design. Example: project = Project(path=path); project.initialize() (doesn't exist yet -> fails -> drives implementation)
**DO:** Write test against real expected API that fails initially. Example: project = Project(path); project.initialize(); assert project.is_ready (fails until implemented)
**DON'T:** Don't use placeholders, dummy values, or skip the failing step. Example: project = 'TODO' (wrong); assuming test passes first (wrong)

### Rule: Test Observable Behavior (Priority 12) [Scanner]
**File:** `story_bot/behaviors/tests/rules/test_observable_behavior.json`
**Description:** Test observable behavior, not implementation details. Verify public API and visible state changes. Don't assert on private methods or internal flags. Example: assert agent.config_path.exists() (observable); not assert agent._internal_flag (private)
**DO:** Test observable outcomes through public API. Example: assert agent.config_path == expected; assert agent.is_initialized (public properties)
**DON'T:** Don't test private state or implementation details. Example: assert agent._initialized (wrong); assert agent._config_cache (wrong)

### Rule: Helper Extraction And Reuse (Priority 13) [Scanner]
**File:** `story_bot/behaviors/tests/rules/helper_extraction_and_reuse.json`
**Description:** Extract duplicate test setup to reusable helper functions. Keep test bodies focused on specific behavior. Example: create_agent_with_config(), create_config_file(), verify_agent_initialized() - reusable across tests
**DO:** Extract duplicate setup to reusable helpers. Example: create_agent_with_config(name, workspace, config) returns initialized Agent
**DON'T:** Don't duplicate setup code across tests. Example: Same 10 lines of setup in every test method (wrong - extract to helper)

### Rule: Match Specification Scenarios (Priority 14) [Scanner]
**File:** `story_bot/behaviors/tests/rules/match_specification_scenarios.json`
**Description:** Tests must match specification scenarios exactly. Test names, steps, and assertions verify exactly what the scenario states. Use exact variable names and terminology from specification. Example: agent_name='story_bot' (from spec), not name='bot'
**DO:** Test matches specification exactly. Example: GIVEN config exists, WHEN Agent(agent_name='story_bot'), THEN config_path == agents/base/agent.json
**DON'T:** Don't use different terminology or assert things not in specification. Example: assert agent._internal_flag (not in spec - wrong)

### Rule: Place Imports At Top (Priority 15) [Scanner]
**File:** `story_bot/behaviors/tests/rules/place_imports_at_top.json`
**Description:** Place all imports at top of test file, after docstrings, before code. Group: stdlib, third-party, then local. Example: import json; import pytest; from mymodule import MyClass
**DO:** All imports at top, grouped by type. Example: import json; import pytest; from agile_bot.bots... import X
**DON'T:** Don't place imports inside functions or after code. Example: def test(): from pathlib import Path (wrong - import inside function)

### Rule: Object Oriented Test Helpers (Priority 16) [Scanner]
**File:** `story_bot/behaviors/tests/rules/object_oriented_test_helpers.json`
**Description:** Consolidate tests around object-oriented helpers/factories (e.g., BotTestHelper test hopper) that build complete domain objects with standard data. Example: helper = BotTestHelper(tmp_path); helper.set_state('shape','clarify'); helper.assert_at_behavior_action('shape','clarify'). Avoid scattering many primitive parameters across parametrize blocks or inline setups.
**DO:** Use shared helper objects to create full test fixtures and assert against complete domain objects, not fragments.
**DON'T:** Do not spread test setup across many primitive parameters or cherry-pick single values from partial objects.

### Rule: Production Code Explicit Dependencies (Priority 16) [Scanner]
**File:** `story_bot/behaviors/tests/rules/production_code_explicit_dependencies.json`
**Description:** Production code: make dependencies explicit through constructor injection. Pass all external dependencies as constructor parameters. No hidden global state. Tests easily inject test doubles. Example: Agent(config_loader=loader, domain_graph=graph)
**DO:** Inject all dependencies through constructor. Example: def __init__(self, config_loader, domain_graph): self._loader = config_loader
**DON'T:** Don't access globals, singletons, or create dependencies internally. Example: self._loader = ConfigLoader() (wrong - creates internally)

### Rule: Self Documenting Tests (Priority 17) [Scanner]
**File:** `story_bot/behaviors/tests/rules/self_documenting_tests.json`
**Description:** Tests are self-documenting through code structure. Don't add verbose comments explaining failures. Imports, calls, and assertions show the API design. Let code speak for itself. Example: generator = MCPServerGenerator(bot_name, config_path); server = generator.generate_server()
**DO:** Let code structure document the test. Example: generator = MCPServerGenerator(name, config); file = generator.generate() - API is clear
**DON'T:** Don't add verbose comments explaining obvious things. Example: # This will fail because API doesn't exist yet (unnecessary)

### Rule: Standard Test Data Sets (Priority 17) [Scanner]
**File:** `story_bot/behaviors/tests/rules/standard_test_data_sets.json`
**Description:** Use standard, named test data sets across tests instead of recreating ad-hoc values. Example: STANDARD_STATE = {...}; helper.set_state(...); assert helper.get_state() == STANDARD_STATE.
**DO:** Define canonical data once (helper constants/factories) and reuse it so every test exercises the full domain object.
**DON'T:** Do not create new ad-hoc values per test or assert only one field from a complex object.

### Rule: Assert Full Results (Priority 18) [Scanner]
**File:** `story_bot/behaviors/tests/rules/assert_full_results.json`
**Description:** Assert full domain results (state/log/graph objects), not single cherry-picked fields. Example: assert helper.get_state() == STANDARD_STATE, not assert helper.get_state()['current'] == 'shape.clarify'.
**DO:** Compare entire objects/dicts/dataclasses against standard data fixtures.
**DON'T:** Do not assert single fields or lengths when validating complex results.

### Rule: Use Ascii Only (Priority 18) [Scanner]
**File:** `story_bot/behaviors/tests/rules/use_ascii_only.json`
**Description:** All test code must use ASCII-only characters. No Unicode symbols, emojis, or special characters. Use plain ASCII alternatives. Example: print('[PASS] Success') not print('[checkmark] Success')
**DO:** Use ASCII-only characters. Example: print('[PASS] Agent initialized'); print('[ERROR] Config not found')
**DON'T:** Don't use Unicode or emojis. Example: print('[checkmark] Done') (wrong); print('[green_check] OK') (wrong)

### Rule: Pytest Bdd Orchestrator Pattern (Priority 19) [Scanner]
**File:** `story_bot/behaviors/tests/rules/pytest_bdd_orchestrator_pattern.json`
**Description:** Use pytest with orchestrator pattern for story-based tests. NO FEATURE FILES. Test classes contain orchestrator methods (under 20 lines) showing Given-When-Then flow by calling helper functions. Example: def test_agent_loads_config(): given_config_exists(); agent = when_agent_initialized(); then_agent_is_configured(agent)
**DO:** Orchestrator pattern: test shows flow, delegates to helpers. Example: # Given; create_config_file(); # When; agent.initialize(); # Then; assert agent.is_initialized
**DON'T:** Don't use feature files or inline complex setup. Example: @given('config exists') def step(): ... (wrong - use pytest directly)

### Rule: Use Exact Variable Names (Priority 21) [Scanner]
**File:** `story_bot/behaviors/tests/rules/use_exact_variable_names.json`
**Description:** Use exact variable names from specification scenarios. When spec mentions agent_name, workspace_root, config_path - use those exact names in tests and production code. Example: agent_name = 'story_bot' (from spec), not name = 'story_bot'
**DO:** Use exact names from specification in tests and production. Example: agent_name, workspace_root, config_path - all from spec
**DON'T:** Don't use different names than specification. Example: name = 'bot' when spec says agent_name (wrong)

### Rule: Use Given When Then Helpers (Priority 22) [Scanner]
**File:** `story_bot/behaviors/tests/rules/use_given_when_then_helpers.json`
**Description:** Use reusable helper functions instead of inline code blocks of 4+ lines. Optimize for reusability, not exact step names. Place helpers at correct scope: story-level in class, sub-epic in module, epic in separate file. Example: given_config_exists(), when_agent_initialized(), then_agent_is_configured()
**DO:** Use Given/When/Then helper functions for setup, action, assertion. Example: given_bot_config_exists(); bot = when_bot_instantiated(); then_bot_uses_correct_directories(bot)
**DON'T:** Don't use inline operations of 4+ lines. Example: config_dir = ...; config_dir.mkdir(); config_file = ...; config_file.write_text() (wrong - extract to helper)


Scanner tools don't cover or catch every rule violation. Do a second pass:
1. Carefully read each rule file, fully reviewing DO and DON'T sections, and every provided example.
2. Inspect all epics, sub-epics, stories, and domain concepts in the story graph for compliance.
3. Compare the properties and content of each element against the rule's requirements.
4. Document any violations the scanner could not find.
5. For each violation, extract an **Example** showing the problem and provide a **Fix** with code example.

## Violations Found

Record ALL findings (scanner + manual) using this readable format. Group by theme for narrow IDE chat panels:

### [Theme Name] (X violations)

**1. [Rule Name]**
- Location: `path.to.element`
- Status: Valid / False Positive
- Source: Scanner / Manual / Both
- Problem: `"actual problematic text"`
- Fix: `"corrected text"`
- Root Cause: Brief explanation

**2. [Rule Name]**
- Location: `path.to.element`
- ...

---

### [Next Theme] (Y violations)
...

Use this list format instead of tables - tables are unreadable in narrow IDE side chat panels.

## Step 3: Summarize Findings & Recommendations

Provide a concise summary:
- Report how many **scanner violations** were valid vs false positives.
- Enumerate any **additional manual findings** not caught by scanners.
- Group all violations by recurring theme or pattern.
- Split violations into **Priority Fixes** (must resolve before continuing) and **Optional Improvements**.

Present your summary and await user confirmation before automatically applying or proposing corrections.
specification_tests: validate test code and domain language usage
Validate that test code uses proper domain terminology (class names = domain entities, method names = domain responsibilities)
Validate that all test files, classes, and methods are properly mapped to story-graph.json**Combined instructions:** The following combines multiple actions. Perform them one after another.

## Scope

**Story Scope:** "Render Diagram In Workspace"

Please only work on the following scope.

Scope Filter: ""Render Diagram In Workspace""

Scope:

{
  "path": "C:\\dev\\agile_bots\\docs\\story\\story-graph.json",
  "has_epics": true,
  "has_increments": true,
  "has_domain_concepts": true,
  "epic_count": 1,
  "content": {
    "epics": [
      {
        "name": "Invoke Bot",
        "sub_epics": [
          {
            "name": "Perform Action",
            "sub_epics": [
              {
                "name": "Render Content",
                "sub_epics": [],
                "story_groups": [
                  {
                    "name": null,
                    "stories": [
                      {
                        "name": "Render Diagram In Workspace",
                        "acceptance_criteria": [
                          {
                            "name": "WHEN Diagram is large\nTHEN Panel provides scroll or zoom AND Diagram remains readable",
                            "text": "WHEN Diagram is large\nTHEN Panel provides scroll or zoom AND Diagram remains readable",
                            "sequential_order": 0.0
                          },
                          {
                            "name": "WHEN User clicks diagram link\nTHEN System opens diagram file in editor",
                            "text": "WHEN User clicks diagram link\nTHEN System opens diagram file in editor",
                            "sequential_order": 1.0
                          }
                        ],
                        "scenarios": [
                          {
                            "name": "Workspace displays {DrawIOElement} diagram for scope",
                            "background": [],
                            "steps": [
                              {
                                "text": "Given {Behavior} \"shape\" is selected",
                                "sequential_order": 1.0
                              },
                              {
                                "text": "And scope has diagram output",
                                "sequential_order": 2.0
                              },
                              {
                                "text": "When workspace section renders",
                                "sequential_order": 3.0
                              },
                              {
                                "text": "Then {DrawIOElement} diagram links are displayed",
                                "sequential_order": 4.0
                              },
                              {
                                "text": "And User can open diagram in editor",
                                "sequential_order": 5.0
                              }
                            ],
                            "examples": null
                          },
                          {
                            "name": "Large diagram has scroll or zoom",
                            "background": [],
                            "steps": [
                              {
                                "text": "Given {DrawIOElement} diagram exceeds viewport",
                                "sequential_order": 1.0
                              },
                              {
                                "text": "When User views diagram in workspace",
                                "sequential_order": 2.0
                              },
                              {
                                "text": "Then Panel provides scroll or zoom",
                                "sequential_order": 3.0
                              },
                              {
                                "text": "And Diagram remains readable",
                                "sequential_order": 4.0
                              }
                            ],
                            "examples": null
                          }
                        ]
                      }
                    ]
                  }
                ],
                "domain_concepts": [
                  {
                    "name": "RenderOutputAction",
                    "responsibilities": [
                      {
                        "name": "Inject render output instructions",
                        "collaborators": [
                          "Behavior",
                          "Content",
                          "Render Spec",
                          "Renderer"
                        ]
                      },
                      {
                        "name": "Inject templates",
                        "collaborators": [
                          "Behavior",
                          "Content",
                          "Render Spec",
                          "Template"
                        ]
                      },
                      {
                        "name": "Inject transformers",
                        "collaborators": [
                          "Behavior",
                          "Content",
                          "Transformer"
                        ]
                      },
                      {
                        "name": "Load + inject structured content",
                        "collaborators": [
                          "Behavior",
                          "Content",
                          "Knowledge Graph"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "TTYRenderOutput",
                    "responsibilities": [
                      {
                        "name": "Serialize render action to TTY",
                        "collaborators": [
                          "RenderOutputAction",
                          "TTY String"
                        ]
                      },
                      {
                        "name": "Format render status",
                        "collaborators": [
                          "Render Spec",
                          "TTY String"
                        ]
                      },
                      {
                        "name": "Wraps domain action",
                        "collaborators": [
                          "RenderOutputAction"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "inherits_from": "TTYProgressAdapter",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "JSONRenderOutput",
                    "responsibilities": [
                      {
                        "name": "Serialize render action to JSON",
                        "collaborators": [
                          "RenderOutputAction",
                          "JSON String"
                        ]
                      },
                      {
                        "name": "Include render spec",
                        "collaborators": [
                          "Render Spec",
                          "Templates",
                          "JSON"
                        ]
                      },
                      {
                        "name": "Wraps domain action",
                        "collaborators": [
                          "RenderOutputAction"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "inherits_from": "JSONProgressAdapter",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "MarkdownRenderOutput",
                    "responsibilities": [
                      {
                        "name": "Serialize render action to Markdown",
                        "collaborators": [
                          "RenderOutputAction",
                          "Markdown String"
                        ]
                      },
                      {
                        "name": "Format render documentation",
                        "collaborators": [
                          "Render Spec",
                          "Templates",
                          "Markdown"
                        ]
                      },
                      {
                        "name": "Wraps domain action",
                        "collaborators": [
                          "RenderOutputAction"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "inherits_from": "MarkdownProgressAdapter",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "Renderer",
                    "responsibilities": [
                      {
                        "name": "Render complex output",
                        "collaborators": [
                          "Template",
                          "Knowledge Graph",
                          "Transformer"
                        ]
                      },
                      {
                        "name": "Render outputs using components in context",
                        "collaborators": [
                          "AI Chat",
                          "Template",
                          "Content"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "Template",
                    "responsibilities": [
                      {
                        "name": "Define output structure",
                        "collaborators": [
                          "Placeholder"
                        ]
                      },
                      {
                        "name": "Transform content",
                        "collaborators": [
                          "Transformer",
                          "Content"
                        ]
                      },
                      {
                        "name": "Load template",
                        "collaborators": [
                          "Behavior",
                          "Content"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "Content",
                    "responsibilities": [
                      {
                        "name": "Render outputs",
                        "collaborators": [
                          "Template",
                          "Renderer",
                          "Render Spec"
                        ]
                      },
                      {
                        "name": "Synchronize formats",
                        "collaborators": [
                          "Synchronizer",
                          "Extractor",
                          "Synchronizer Spec"
                        ]
                      },
                      {
                        "name": "Save knowledge graph",
                        "collaborators": [
                          "Knowledge Graph"
                        ]
                      },
                      {
                        "name": "Load rendered content",
                        "collaborators": [
                          "na"
                        ]
                      },
                      {
                        "name": "Present rendered content",
                        "collaborators": [
                          "na"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "RenderInstructionsSection",
                    "responsibilities": [
                      {
                        "name": "Wraps render subsection",
                        "collaborators": [
                          "RenderDataSubSection"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "inherits_from": "InstructionsSection",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "RenderDataSubSection",
                    "responsibilities": [
                      {
                        "name": "Wraps render JSON",
                        "collaborators": [
                          "Render JSON"
                        ]
                      },
                      {
                        "name": "Displays render spec",
                        "collaborators": [
                          "Object",
                          "RenderSpec JSON"
                        ]
                      },
                      {
                        "name": "Displays templates",
                        "collaborators": [
                          "List",
                          "Template JSON"
                        ]
                      },
                      {
                        "name": "Displays render instructions",
                        "collaborators": [
                          "String",
                          "RenderInstructions JSON"
                        ]
                      },
                      {
                        "name": "Opens template file",
                        "collaborators": [
                          "CLI",
                          "Path JSON"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "inherits_from": "SubSectionView",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  }
                ]
              }
            ],
            "story_groups": []
          }
        ],
        "domain_concepts": []
      }
    ],
    "increments": []
  }
}

---

# Behavior: scenarios

## Behavior Instructions - scenarios

The purpose of this behavior is to write detailed plain-english scenarios (given/when/then) that specify exact behavior for each story

Write detailed plain-English scenarios (Given/When/Then) that specify exact behavior for each story

## Action Instructions - build

The purpose of this action is to build story graph from content area and render using story graph renderer

Follow agile_bot/bots/story_bot/behaviors/scenarios/content/story_graph/instructions.json
specification_scenarios: build scenarios using domain language
Use proper domain terminology in scenario steps - refer to domain concepts and entities
Add/update scenarios and scenario_outlines ONLY in main epics section (single source of truth), NOT in increments section

**STORY GRAPH UPDATE STRATEGY (use when story-graph.json already exists):**

When updating an existing story graph, do NOT read and rewrite the entire story-graph.json manually.
Choose one of these approaches in order of preference:

1. **API approach (preferred for targeted changes):**
   Use the StoryMap node API via CLI dot-notation to make surgical changes.
   - Navigate: story_map.filter_by_name name:"Story Name" to read only the relevant subtree
   - Create:  story_map."Epic"."SubEpic"."Story".create_scenario name:"Scenario Name"
   - Create:  story_map."Epic"."SubEpic"."Story".create_acceptance_criteria name:"WHEN condition THEN outcome"
   - Rename:  story_map."Epic"."SubEpic"."Story".rename name:"New Name"
   - Move:    story_map."Epic"."SubEpic"."Story".move_to target:"Other SubEpic"
   - Reorder: story_map."Epic"."SubEpic"."Story".move_to at_position:2
   - Delete:  story_map."Epic"."SubEpic"."Story"."Old Scenario".delete
   Each call auto-saves the full graph safely through in-memory tree serialization.

2. **Bulk approach (for sweeping changes across many stories):**
   Build a temporary StoryMap with just your changes using the same create API (without bot context),
   then use generate_merge_report() to compare against the original, and merge_story_graphs() to apply.
   The merge preserves all original data (acceptance_criteria, scenarios, steps, metadata) you did not change.

3. **Manual JSON edit (last resort only):**
   Only if the API and bulk approaches cannot handle the situation.
   Use filter_by_name to read a scoped subtree rather than the full file.
   Write changes back through the StoryMap.save() method, as opposed to by editing story-graph.json directly.

---

**Look for context in the following locations:**
- in this message and chat history
- `C:/dev/agile_bots/docs/story/story-graph.json` - the story graph and related  knowledge built so far
- `C:/dev/agile_bots/docs/story/strategy.json` - strategy decisions made
- `C:/dev/agile_bots/docs/story/clarification.json` - clarification answers
- `C:/dev/agile_bots/test/` and `C:/dev/agile_bots/src/` - existing code and tests
- any folder named `context/` anywhere in `C:/dev/agile_bots/` - additional context files

IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

@build-instructions.txt

**BUILD PROCESS:**

**1. Load Context**
Load clarification.json, planning.json, and source material from context sources (listed above).

**2. Load Build Configs**
From `c:\dev\agile_bots\bots\story_bot/behaviors/scenarios/content/`, each folder contains:
- `build_*.json` - Config (name, path, template, output)
- `instructions.json` - Build instructions
- `template-file.json` - Output schema/structure

**3. Execute Build**
1. Load config, instructions, and template (injected as 'story_graph_template')
2. Check if output file exists - read it FIRST
3. Follow instructions.json - match template structure exactly (check '_explanation' section)
4. Apply context from Step 1
5. If file exists: ADD/EXTEND only, never overwrite/delete
6. Validate against template schema
7. Write to `C:\dev\agile_bots/{config.path}/{config.output}`
- Read existing files before changes - preserve all content
- Match template structure exactly - don't invent schemas
- Trace all knowledge to clarification/planning data
- Process builds sequentially - validate each

**4. SOURCE TRACEABILITY**
Knowledge artifacts should include source references when available:
- `context_source` field on epics, sub_epics, story_groups, stories, and domain concepts
- Format: `{"file": "filename.pdf", "page": "12", "section": "3.2.1 Payment Flow"}`
- For multiple sources: use array of source objects
- If source is chat/conversation: `{"type": "chat", "description": "User clarification on approval workflow"}`
- If source is code: `{"file": "path/to/file.py", "lines": "45-67", "function": "process_payment"}`
- Prefer tracing knowledge to a source when possible
- When source is unclear, mark as `{"type": "inferred", "basis": "description of inference basis"}`
Follow agile_bot/bots/story_bot/behaviors/scenarios/content/story_graph/instructions.json
specification_scenarios: build scenarios using domain language
Use proper domain terminology in scenario steps - refer to domain concepts and entities
Add/update scenarios and scenario_outlines ONLY in main epics section (single source of truth), NOT in increments section

**STORY GRAPH UPDATE STRATEGY (use when story-graph.json already exists):**

When updating an existing story graph, do NOT read and rewrite the entire story-graph.json manually.
Choose one of these approaches in order of preference:

1. **API approach (preferred for targeted changes):**
   Use the StoryMap node API via CLI dot-notation to make surgical changes.
   - Navigate: story_map.filter_by_name name:"Story Name" to read only the relevant subtree
   - Create:  story_map."Epic"."SubEpic"."Story".create_scenario name:"Scenario Name"
   - Create:  story_map."Epic"."SubEpic"."Story".create_acceptance_criteria name:"WHEN condition THEN outcome"
   - Rename:  story_map."Epic"."SubEpic"."Story".rename name:"New Name"
   - Move:    story_map."Epic"."SubEpic"."Story".move_to target:"Other SubEpic"
   - Reorder: story_map."Epic"."SubEpic"."Story".move_to at_position:2
   - Delete:  story_map."Epic"."SubEpic"."Story"."Old Scenario".delete
   Each call auto-saves the full graph safely through in-memory tree serialization.

2. **Bulk approach (for sweeping changes across many stories):**
   Build a temporary StoryMap with just your changes using the same create API (without bot context),
   then use generate_merge_report() to compare against the original, and merge_story_graphs() to apply.
   The merge preserves all original data (acceptance_criteria, scenarios, steps, metadata) you did not change.

3. **Manual JSON edit (last resort only):**
   Only if the API and bulk approaches cannot handle the situation.
   Use filter_by_name to read a scoped subtree rather than the full file.
   Write changes back through the StoryMap.save() method, as opposed to by editing story-graph.json directly.

When building or adding to the story graph follow these rules,
Rules to follow:

- **scenario_language_matches_domain**: Scenario language MUST use domain concept terminology. Given/When/Then steps should reference domain entities and concepts, not UI elements or technical implementation details.
  DO: Use domain language in scenario steps - reference domain concepts by name.
  DON'T: Don't use UI element names, technical implementation terms, or generic words instead of domain concepts.

- **example_tables_use_domain_language**: Example tables MUST be grounded in scenario steps AND use domain-rich language. Table columns = nouns from Given/When/Then steps. Use domain terminology, not UI elements. Omit ID columns used purely for linking tables - relationships are expressed via collaboration field and table ordering. Concrete values with domain context, not generic JSON or placeholders. Use source entity data, not aggregated/calculated values - this is the stage where you figure out the real examples.
  DO: Ground tables in scenario nouns, use domain terminology, connect tables using domain responsibility sentences. Omit implementation IDs. Show source entities, not derived counts.
  DON'T: Don't use UI elements, flat lookup tables, generic JSON, abstract descriptions, invented terminology, or aggregated/calculated values.

- **given_describes_state_not_actions**: Given statements describe STATE/PRECONDITIONS, not actions or functionality. Given = what exists before test. When = first action. Then = expected behavior. Example: Given user is logged in (state), not Given user logs in (action).
  DO: Given describes state/preconditions only. Example: 'Given user is logged in' (state), 'Given character sheet exists' (precondition)
  DON'T: Don't describe actions, UI navigation, or functionality in Given. Example: 'Given user logs in' (action - wrong), 'Given User is on PaymentDetails step' (navigation - wrong)

- **background_vs_scenario_setup**: Background = shared setup for 3+ scenarios (Given/And only, no When/Then). Background steps MUST use {Concept} notation to reference domain objects. Use {Concept.property} when a specific attribute is important. Don't repeat Background in Steps.
  DO: Use Background for shared context with {Concept} references to example tables.
  DON'T: Don't use hardcoded values or column names in Background - use {Concept} notation. Don't include When/Then.

- **scenarios_cover_all_cases**: Scenarios must cover happy path, edge cases, and error cases based on acceptance criteria. Example: Valid input → success; Boundary value → validates; Invalid input → error message.
  DO: Cover all case types: happy path, edge cases, error cases. Example: User enters valid data → success; User enters boundary → validates; User enters invalid → error
  DON'T: Don't skip case types. Example: Only happy path scenarios (missing edge and error cases)

- **use_scenario_outline_when_needed**: Use Scenario Outline with Examples when story warrants concrete data: formulas need validation, domain has named entities, parameter variations exist. Example: Calculate ability modifier with Examples table Rank 10→0, Rank 12→+1, Rank 14→+2.
  DO: Scenario Outline for formulas, domain entities, or data variations. Example: Scenario Outline: Calculate modifier with Examples table showing input→output pairs
  DON'T: Don't use Scenario Outline for simple behaviors. Example: Scenario Outline: User clicks button (too simple - use regular scenario)

- **write_concrete_scenarios**: Parameterize domain concepts in scenarios using {Concept} notation for objects and {Concept.property} for specific attributes. Every {parameter} in Background/Steps MUST have corresponding example table. Use object references, not column names directly.
  DO: Use {Concept} for object references, {Concept.property} for specific attributes. Connect to example tables.
  DON'T: Don't hardcode values without examples, don't use non-domain placeholders, don't skip base data dependencies.

- **scenarios_on_story_docs**: Scenarios must be in story-graph.json (in scenarios or scenario_outlines fields), NOT in separate markdown files. NEVER create feature specification documents. Example: story-graph.json epics[].stories[].scenarios[], not docs/story/scenarios.md.
  DO: Add scenarios to story-graph.json. Example: story-graph.json epics[].stories[].scenarios[] array
  DON'T: Dont create separate scenario files or feature specifications. Example: docs/story/Epic/Feature/Feature Specification.md (wrong)

- **map_table_columns_to_scenario_parameters**: Map example tables to {Concept} references bidirectionally. Every example table maps to a {Concept} in Background/Steps. Use {Concept} for object references and {Concept.property} for specific attributes. Keep tables minimal and domain-focused.
  DO: Bidirectional mapping: Example table name ↔ {Concept} reference in steps.
  DON'T: Don't use <column_name> notation - use {Concept} or {Concept.property}. Don't have orphaned tables or references.

### Key Questions

- What system and user actions initiate this story's flow?
- What is the intended system response after each user action?
- What preconditions or data states are required before this story can begin?
- What are the success criteria for the story (from a domain and user perspective)?
- What are the expected alternate flows, error paths, and edge cases?
- Are there any mandatory sequencing constraints within or across stories?
- What domain rules, calculations, or business policies does this story validate?
- Is the story testable independently (including setup and teardown conditions)?
- What external systems or services does this story need to interact with?
- What requests, responses, or contracts are involved in those system interactions?
- Are there system integration points that require validation or simulation?
- How do we handle failures, timeouts, or retries for those system calls?
- What data variations (e.g., boundary conditions, common examples) are required for test coverage?
- What are the input values needed to test each scenario?
- What are the expected output values for each input?
- Are there formulas or calculations that need multiple data points to validate?
- Are there domain entities with named values that should be tested?
- What are the boundary conditions (min, max, edge cases) for each data point?

### Evidence

Acceptance criteria from Exploration stage (Domain AC at feature level, Behavioral AC at story level), High fidelity UX flows, Cross-functional walkthrough outputs, Integration contracts or API mocks, Behavior diagrams (state, sequence)

### Decisions

**Your Decisions:**

**examples_representation:**
  Verification Data Table

**scenario_outline:**
  Scenario Outline with Examples

**scenario_coverage:**
  - Happy Path
  - Edge Cases


### Assumptions

**Your Assumptions:**

- One story is specified at a time
- Acceptance criteria must be testable, unambiguous, and executable
- Gherkin syntax or structured language (Given/When/Then) is preferred
- Scenarios are written in plain English. When using Scenario Outline, variables are clearly marked and defined in Examples tables with actual test data.
- Examples tables when used must include ALL variables used in scenario steps
- Examples tables when used must have exact values for both input AND output variables
- Every variable when used in scenario steps must have a corresponding column in Examples table
- Examples tables when used must have actual test data, not placeholders
- Output/expected result variables must be included in Examples tables when used
- scnarios follow this pattern
- bulk of business logic tests done against the domain layer objects directly
- minimal happy path testing done with separate tgests that go theoiugh CLI
- JS nodetest for panel test focus on rendering and button layout

---
## Next action: validate
**Next:** Perform the following action. Fix any errors found in the Violation.

## Action Instructions - validate

The purpose of this action is to validate story graph and/or artifacts against behavior-specific rules, checking for violations and compliance

specification_scenarios: validate scenario structure and domain language usage
Validate that scenarios use proper domain terminology and reference domain concepts correctly

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

## Step 1: Run Scanners Then Review Violations

**Scanners you must run (with params below). Do not assume pre-run results.**

| Rule | Rule file | Scanner module |
|------|-----------|----------------|
| Scenario Language Matches Domain | `story_bot/behaviors/scenarios/rules/scenario_language_matches_domain.json` | `scanners.scenarios.scenario_language_scanner.ScenarioLanguageScanner` |
| Example Tables Use Domain Language | `story_bot/behaviors/scenarios/rules/example_tables_use_domain_language.json` | `scanners.scenarios.example_table_scanner.ExampleTableScanner` |
| Given Describes State Not Actions | `story_bot/behaviors/scenarios/rules/given_describes_state_not_actions.json` | `scanners.scenarios.given_state_not_actions_scanner.GivenStateNotActionsScanner` |
| Background Vs Scenario Setup | `story_bot/behaviors/scenarios/rules/background_vs_scenario_setup.json` | `scanners.scenarios.background_common_setup_scanner.BackgroundCommonSetupScanner` |
| Scenarios Cover All Cases | `story_bot/behaviors/scenarios/rules/scenarios_cover_all_cases.json` | `scanners.scenarios.scenarios_cover_all_cases_scanner.ScenariosCoverAllCasesScanner` |
| Use Scenario Outline When Needed | `story_bot/behaviors/scenarios/rules/use_scenario_outline_when_needed.json` | `scanners.scenarios.scenario_outline_scanner.ScenarioOutlineScanner` |
| Write Concrete Scenarios | `story_bot/behaviors/scenarios/rules/write_concrete_scenarios.json` | `scanners.scenarios.parameterized_scenarios_scanner.ParameterizedScenariosScanner` |
| Scenarios On Story Docs | `story_bot/behaviors/scenarios/rules/scenarios_on_story_docs.json` | `scanners.scenarios.scenarios_on_story_docs_scanner.ScenariosOnStoryDocsScanner` |
| Map Table Columns To Scenario Parameters | `story_bot/behaviors/scenarios/rules/map_table_columns_to_scenario_parameters.json` | `scanners.table_column_parameter_scanner.TableColumnParameterScanner` |

**Params to pass when running scanners:**
- **Scope:** all epics, sub-epics, stories, and domain concepts in the story graph
- **Workspace:** `C:\dev\agile_bots`
- **Story graph path:** `docs/story/story-graph.json` (or behavior-specific path)

Run each scanner with the above scope and workspace; then report violations and fix the story graph as needed.

Run each scanner with the params above, then review the violations they report as follows:
1. For each violation message, locate the corresponding element in the story graph.
2. Open the relevant rule file and read all DO and DON'T examples thoroughly.
3. Decide if the violation is **Valid** (truly a rule breach per examples) or a **False Positive** (explain why if so).
4. Determine the **Root Cause** (e.g., 'incorrect concept naming', 'missing actor', etc.).
5. Assign a **Theme** grouping based on the type of issue (e.g., 'noun-only naming', 'incomplete acceptance criteria').
6. Extract an **Example** from the actual code/content showing the problem.
7. Suggest a clear, concrete **Fix** with a code example informed by DO examples in the rule.

## Step 2: Manual Rule Review

**Rules to validate against (read each file for full DO/DON'T examples):**

### Rule: Scenario Language Matches Domain (Priority 1) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/scenario_language_matches_domain.json`
**Description:** Scenario language MUST use domain concept terminology. Given/When/Then steps should reference domain entities and concepts, not UI elements or technical implementation details.
**DO:** Use domain language in scenario steps - reference domain concepts by name.
**DON'T:** Don't use UI element names, technical implementation terms, or generic words instead of domain concepts.

### Rule: Example Tables Use Domain Language (Priority 2) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/example_tables_use_domain_language.json`
**Description:** Example tables MUST be grounded in scenario steps AND use domain-rich language. Table columns = nouns from Given/When/Then steps. Use domain terminology, not UI elements. Omit ID columns used purely for linking tables - relationships are expressed via collaboration field and table ordering. Concrete values with domain context, not generic JSON or placeholders. Use source entity data, not aggregated/calculated values - this is the stage where you figure out the real examples.
**DO:** Ground tables in scenario nouns, use domain terminology, connect tables using domain responsibility sentences. Omit implementation IDs. Show source entities, not derived counts.
**DON'T:** Don't use UI elements, flat lookup tables, generic JSON, abstract descriptions, invented terminology, or aggregated/calculated values.

### Rule: Given Describes State Not Actions (Priority 3) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/given_describes_state_not_actions.json`
**Description:** Given statements describe STATE/PRECONDITIONS, not actions or functionality. Given = what exists before test. When = first action. Then = expected behavior. Example: Given user is logged in (state), not Given user logs in (action).
**DO:** Given describes state/preconditions only. Example: 'Given user is logged in' (state), 'Given character sheet exists' (precondition)
**DON'T:** Don't describe actions, UI navigation, or functionality in Given. Example: 'Given user logs in' (action - wrong), 'Given User is on PaymentDetails step' (navigation - wrong)

### Rule: Background Vs Scenario Setup (Priority 4) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/background_vs_scenario_setup.json`
**Description:** Background = shared setup for 3+ scenarios (Given/And only, no When/Then). Background steps MUST use {Concept} notation to reference domain objects. Use {Concept.property} when a specific attribute is important. Don't repeat Background in Steps.
**DO:** Use Background for shared context with {Concept} references to example tables.
**DON'T:** Don't use hardcoded values or column names in Background - use {Concept} notation. Don't include When/Then.

### Rule: Scenarios Cover All Cases (Priority 5) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/scenarios_cover_all_cases.json`
**Description:** Scenarios must cover happy path, edge cases, and error cases based on acceptance criteria. Example: Valid input → success; Boundary value → validates; Invalid input → error message.
**DO:** Cover all case types: happy path, edge cases, error cases. Example: User enters valid data → success; User enters boundary → validates; User enters invalid → error
**DON'T:** Don't skip case types. Example: Only happy path scenarios (missing edge and error cases)

### Rule: Use Scenario Outline When Needed (Priority 6) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/use_scenario_outline_when_needed.json`
**Description:** Use Scenario Outline with Examples when story warrants concrete data: formulas need validation, domain has named entities, parameter variations exist. Example: Calculate ability modifier with Examples table Rank 10→0, Rank 12→+1, Rank 14→+2.
**DO:** Scenario Outline for formulas, domain entities, or data variations. Example: Scenario Outline: Calculate modifier with Examples table showing input→output pairs
**DON'T:** Don't use Scenario Outline for simple behaviors. Example: Scenario Outline: User clicks button (too simple - use regular scenario)

### Rule: Write Concrete Scenarios (Priority 7) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/write_concrete_scenarios.json`
**Description:** Parameterize domain concepts in scenarios using {Concept} notation for objects and {Concept.property} for specific attributes. Every {parameter} in Background/Steps MUST have corresponding example table. Use object references, not column names directly.
**DO:** Use {Concept} for object references, {Concept.property} for specific attributes. Connect to example tables.
**DON'T:** Don't hardcode values without examples, don't use non-domain placeholders, don't skip base data dependencies.

### Rule: Scenarios On Story Docs (Priority 8) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/scenarios_on_story_docs.json`
**Description:** Scenarios must be in story-graph.json (in scenarios or scenario_outlines fields), NOT in separate markdown files. NEVER create feature specification documents. Example: story-graph.json epics[].stories[].scenarios[], not docs/story/scenarios.md.
**DO:** Add scenarios to story-graph.json. Example: story-graph.json epics[].stories[].scenarios[] array
**DON'T:** Dont create separate scenario files or feature specifications. Example: docs/story/Epic/Feature/Feature Specification.md (wrong)

### Rule: Map Table Columns To Scenario Parameters (Priority 9) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/map_table_columns_to_scenario_parameters.json`
**Description:** Map example tables to {Concept} references bidirectionally. Every example table maps to a {Concept} in Background/Steps. Use {Concept} for object references and {Concept.property} for specific attributes. Keep tables minimal and domain-focused.
**DO:** Bidirectional mapping: Example table name ↔ {Concept} reference in steps.
**DON'T:** Don't use <column_name> notation - use {Concept} or {Concept.property}. Don't have orphaned tables or references.


Scanner tools don't cover or catch every rule violation. Do a second pass:
1. Carefully read each rule file, fully reviewing DO and DON'T sections, and every provided example.
2. Inspect all epics, sub-epics, stories, and domain concepts in the story graph for compliance.
3. Compare the properties and content of each element against the rule's requirements.
4. Document any violations the scanner could not find.
5. For each violation, extract an **Example** showing the problem and provide a **Fix** with code example.

## Violations Found

Record ALL findings (scanner + manual) using this readable format. Group by theme for narrow IDE chat panels:

### [Theme Name] (X violations)

**1. [Rule Name]**
- Location: `path.to.element`
- Status: Valid / False Positive
- Source: Scanner / Manual / Both
- Problem: `"actual problematic text"`
- Fix: `"corrected text"`
- Root Cause: Brief explanation

**2. [Rule Name]**
- Location: `path.to.element`
- ...

---

### [Next Theme] (Y violations)
...

Use this list format instead of tables - tables are unreadable in narrow IDE side chat panels.

## Step 3: Summarize Findings & Recommendations

Provide a concise summary:
- Report how many **scanner violations** were valid vs false positives.
- Enumerate any **additional manual findings** not caught by scanners.
- Group all violations by recurring theme or pattern.
- Split violations into **Priority Fixes** (must resolve before continuing) and **Optional Improvements**.

Present your summary and await user confirmation before automatically applying or proposing corrections.
specification_scenarios: validate scenario structure and domain language usage
Validate that scenarios use proper domain terminology and reference domain concepts correctly

---
## Next action: render
**Next:** Perform the following action.

## Action Instructions - render

The purpose of this action is to render output documents and artifacts from story graph using templates and synchronizers

specification_scenarios: render story documents with scenarios

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

Please follow the instructions below in order to manually render output documents using templates

All render configurations are automatically loaded and injected below. Process ALL configs - do not skip any.



**Final Steps:**
- Process ALL configs above - do not skip any
- Priority order: synchronizer > template
- Verify each output file exists after execution
- If execution fails, report the error and continue with other outputs
- After completing all renders, pause and wait for human confirmation before proceeding to next behavior

**Creating New Render Outputs:**
If you need to create code to render a new output format:
1. Create a new synchronizer file in {workspace}/synchronizers/ (create folder if it doesn't exist)
2. Follow this signature pattern: output_file = synchronizer.render(story_graph_file)
3. The synchronizer should read the story-graph.json and produce the desired output file
4. Add the new synchronizer to the behavior's render config to include it in future renders
specification_scenarios: render story documents with scenarios
IMPORTANT: After completing all template-based rendering, you MUST execute the synchronizer-based render specs by running: scenarios.render.renderAll
This will render the following outputs: render_story_scenarios

---
## Next action: tests.build
**Next:** Perform the following action.

## Action Instructions - build

The purpose of this action is to build story graph from content area and render using story graph renderer

write test files (.py, .js, etc.) with executable test code based on the scenarios you have made within the story-graph.json file
After writing test files, update story-graph.json with further test_file, test_class, and test_method mapping changes you have made
| Field | Level | Format | Example |
|-------|-------|--------|---------|
| test_file | sub_epic | "test/<domain|CLI|panel>/test_<sub_epic>.py" | "test/domain/test_edit_story_graph.py" |
| test_class | story | "Test<StoryName>" | "TestCreatesChildStoryNode" |
| test_method | scenario | "test_<scenario_name>" | "test_user_creates_child_under_epic" |

Hierarchy: epic → sub_epic(test_file) → story_group → story(test_class) → scenario(test_method)

Rules:
- One test_file per sub_epic (all stories share it)
- One test_class per story (only if story has scenarios)
- One test_method per scenario
- Read story-graph.json first, preserve existing fields

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

@build-instructions.txt

**BUILD PROCESS:**

**1. Load Context**
Load clarification.json, planning.json, and source material from context sources (listed above).

**2. Load Build Configs**
From `c:\dev\agile_bots\bots\story_bot/behaviors/tests/content/`, each folder contains:
- `build_*.json` - Config (name, path, template, output)
- `instructions.json` - Build instructions
- `template-file.json` - Output schema/structure

**3. Execute Build**
1. Load config, instructions, and template (injected as 'story_graph_template')
2. Check if output file exists - read it FIRST
3. Follow instructions.json - match template structure exactly (check '_explanation' section)
4. Apply context from Step 1
5. If file exists: ADD/EXTEND only, never overwrite/delete
6. Validate against template schema
7. Write to `C:\dev\agile_bots/{config.path}/{config.output}`
- Read existing files before changes - preserve all content
- Match template structure exactly - don't invent schemas
- Trace all knowledge to clarification/planning data
- Process builds sequentially - validate each

**4. SOURCE TRACEABILITY**
Knowledge artifacts should include source references when available:
- `context_source` field on epics, sub_epics, story_groups, stories, and domain concepts
- Format: `{"file": "filename.pdf", "page": "12", "section": "3.2.1 Payment Flow"}`
- For multiple sources: use array of source objects
- If source is chat/conversation: `{"type": "chat", "description": "User clarification on approval workflow"}`
- If source is code: `{"file": "path/to/file.py", "lines": "45-67", "function": "process_payment"}`
- Prefer tracing knowledge to a source when possible
- When source is unclear, mark as `{"type": "inferred", "basis": "description of inference basis"}`
write test files (.py, .js, etc.) with executable test code based on the scenarios you have made within the story-graph.json file
After writing test files, update story-graph.json with further test_file, test_class, and test_method mapping changes you have made
| Field | Level | Format | Example |
|-------|-------|--------|---------|
| test_file | sub_epic | "test/<domain|CLI|panel>/test_<sub_epic>.py" | "test/domain/test_edit_story_graph.py" |
| test_class | story | "Test<StoryName>" | "TestCreatesChildStoryNode" |
| test_method | scenario | "test_<scenario_name>" | "test_user_creates_child_under_epic" |

Hierarchy: epic → sub_epic(test_file) → story_group → story(test_class) → scenario(test_method)

Rules:
- One test_file per sub_epic (all stories share it)
- One test_class per story (only if story has scenarios)
- One test_method per scenario
- Read story-graph.json first, preserve existing fields

When building or adding to the story graph follow these rules,
Rules to follow:

- **use_class_based_organization**: CRITICAL STRUCTURAL RULE: Test structure matches story graph hierarchy. File = sub-epic (test_<sub_epic>.py), Class = story (Test<ExactStoryName>), Method = scenario (test_<scenario_snake_case>). Getting this wrong creates files in wrong locations requiring deletion/recreation. BEFORE writing any test code, identify the parent sub-epic that contains the story.
  DO: Map story hierarchy to test structure exactly. CRITICAL: File name comes from SUB-EPIC, not story.
  DON'T: Don't use generic/abbreviated names or wrong hierarchy level for file naming. Don't create files in wrong locations.

- **use_domain_language**: Use Ubiquitous Language (DDD): Same vocabulary in domain model, stories, scenarios, AND code. Class names = domain entities/nouns. Method names = domain responsibilities/verbs. Test names read like plain English stories. Example: test_agent_loads_configuration_when_file_exists (not test_agt_init_sets_vars)
  DO: Use domain language for classes, methods, and test names. Example: class GatherContextAction, def inject_guardrails(), test_agent_loads_config_when_file_exists
  DON'T: Don't use generic technical terms or implementation-specific names. Example: class StdioHandler (wrong), def execute_with_guardrails (wrong), test_agt_init_sets_vars (wrong)

- **consistent_vocabulary**: Use ONE word per concept across entire codebase. Pick consistent vocabulary: create (not build/make/construct), verify (not check/assert/validate), load (not fetch/get/retrieve). Use intention-revealing names that describe behavior. Example: create_agent(), verify_initialized(), load_config() - same verbs everywhere
  DO: Use same word for same concept everywhere. Example: create_agent(), create_config(), create_workspace() - all use 'create'
  DON'T: Don't mix synonyms for same concept. Example: create_agent() + build_config() + make_workspace() (wrong - pick one verb)

- **domain_oriented_test_inheritance**: Scaling extension of helper_extraction_and_reuse, object_oriented_test_helpers, and standard_test_data_sets. At small scale, a single test class covering multiple domain objects is fine. As domain objects develop distinct behavior, break out into domain-specific test classes. Use abstract base classes for common operations. Share parameter data and fixtures only when there is obvious shared logic across sub-epics. Place shared base files at the appropriate hierarchy level.
  DO: At small scale keep together. As you scale, use abstract bases, share fixtures only with explicit need, and place shared files at the right hierarchy level.
  DON'T: When scaling, do not copy assertion logic, do not create shared files preemptively, and do not group tests by operation or technology.

- **no_defensive_code_in_tests**: Tests must NEVER contain guard clauses, defensive conditionals, or fallback paths. We control test setup - if it's wrong, the test MUST fail immediately. Guard clauses hide problems. Tests should assume positive outcomes. Example: Just call the code directly, don't wrap in if-checks
  DO: Assume correct setup - let test fail if wrong. Example: behavior = Behavior(name='shape') then assert behavior.name == 'shape'
  DON'T: Don't add if-checks, type guards, or fallback handling in tests. Example: if behavior_file.exists(): (wrong - test should fail if it doesn't)

- **production_code_clean_functions**: Production code functions should do ONE thing, be under 20 lines, and have one level of abstraction. No hidden side effects. Name reveals complete behavior. Extract multiple concerns into separate functions. Example: load_config(), validate_config(), apply_config() - each does one thing
  DO: Single responsibility, small focused functions. Example: initialize_from_config() calls validate_exists(), load_config(), validate_structure(), apply_config()
  DON'T: Don't make functions that do multiple unrelated things or are too long. Example: 50-line function that loads, validates, and applies config

- **bug_fix_test_first**: When production code breaks, follow test-first workflow: write failing test, verify failure, fix code, verify success. Never fix bugs without a failing test first. Example: test_mcp_tool_initializes_bot() fails -> fix initialization -> test passes
  DO: Follow RED-GREEN-PRODUCTION workflow. Example: Write test reproducing bug -> Run test (RED) -> Fix minimal code -> Run test (GREEN) -> Run full suite
  DON'T: Don't fix bugs directly without failing test first. Example: Editing production code without test -> deploying -> hoping it works (wrong)

- **call_production_code_directly**: Call production code directly in tests. Let tests fail naturally if code doesn't exist. Don't comment out calls, mock business logic, or fake state. Only mock external boundaries. Example: agent = Agent(); agent.initialize() (not agent = Mock())
  DO: Call production code directly, let it fail naturally. Example: agent = Agent(workspace); agent.initialize(config); assert agent.is_initialized
  DON'T: Don't mock class under test, comment out calls, or fake state. Example: agent = Mock(spec=Agent) (wrong); agent._initialized = True (wrong)

- **cover_all_behavior_paths**: Cover all behavior paths: normal (happy path), edge cases, and failure scenarios. Each distinct behavior needs its own focused test. Tests must be independent. Example: test_loads_valid_config(), test_loads_empty_config(), test_raises_error_when_file_missing()
  DO: Test normal, edge, and failure paths separately. Example: test_loads_valid_config() (happy), test_loads_empty_config() (edge), test_raises_when_missing() (failure)
  DON'T: Don't test only happy path or combine multiple behaviors in one test. Example: Single test for both success and failure (wrong)

- **mock_only_boundaries**: Mock ONLY at architectural boundaries: external APIs, network, uncontrollable services. Don't mock internal business logic, classes under test, or file operations (use temp files). Example: patch('requests.get') (OK); patch('agent.validate') (wrong)
  DO: Mock only external dependencies you can't control. Example: with patch('requests.get') as mock: (external API - OK to mock)
  DON'T: Don't mock internal logic, class under test, or file I/O. Example: with patch('agent.validate_config') (wrong - test the logic!)

- **create_parameterized_tests_for_scenarios**: If scenarios have Examples tables, create parameterized tests using @pytest.mark.parametrize. Each row becomes a test case. Don't write single tests that only test one example. Example: @pytest.mark.parametrize('input,expected', [(1, 2), (3, 4)])
  DO: Create parameterized tests from Examples tables. Example: @pytest.mark.parametrize('paths,count', [(['p1','p2'], 2), (['p3'], 1)])
  DON'T: Don't hardcode single example or duplicate test methods. Example: def test_with_value_1(): (wrong); def test_with_value_2(): (wrong - use parametrize)

- **define_fixtures_in_test_file**: Define fixtures in the test file, not separate conftest.py. Truly reusable fixtures (file ops, location helpers) go in base conftest.py. Example: @pytest.fixture def workspace_root(tmp_path): return tmp_path / 'workspace'
  DO: Define fixtures in same test file. Example: @pytest.fixture def config_file(tmp_path): ... (in test_agent.py)
  DON'T: Don't create separate conftest.py for agent-specific fixtures. Don't create shared files without explicit need.

- **design_api_through_failing_tests**: Write tests against the REAL expected API BEFORE implementing code. Tests MUST fail initially. Set up real test data and call real API. Failure reveals complete API design. Example: project = Project(path=path); project.initialize() (doesn't exist yet -> fails -> drives implementation)
  DO: Write test against real expected API that fails initially. Example: project = Project(path); project.initialize(); assert project.is_ready (fails until implemented)
  DON'T: Don't use placeholders, dummy values, or skip the failing step. Example: project = 'TODO' (wrong); assuming test passes first (wrong)

- **test_observable_behavior**: Test observable behavior, not implementation details. Verify public API and visible state changes. Don't assert on private methods or internal flags. Example: assert agent.config_path.exists() (observable); not assert agent._internal_flag (private)
  DO: Test observable outcomes through public API. Example: assert agent.config_path == expected; assert agent.is_initialized (public properties)
  DON'T: Don't test private state or implementation details. Example: assert agent._initialized (wrong); assert agent._config_cache (wrong)

- **helper_extraction_and_reuse**: Extract duplicate test setup to reusable helper functions. Keep test bodies focused on specific behavior. Example: create_agent_with_config(), create_config_file(), verify_agent_initialized() - reusable across tests
  DO: Extract duplicate setup to reusable helpers. Example: create_agent_with_config(name, workspace, config) returns initialized Agent
  DON'T: Don't duplicate setup code across tests. Example: Same 10 lines of setup in every test method (wrong - extract to helper)

- **match_specification_scenarios**: Tests must match specification scenarios exactly. Test names, steps, and assertions verify exactly what the scenario states. Use exact variable names and terminology from specification. Example: agent_name='story_bot' (from spec), not name='bot'
  DO: Test matches specification exactly. Example: GIVEN config exists, WHEN Agent(agent_name='story_bot'), THEN config_path == agents/base/agent.json
  DON'T: Don't use different terminology or assert things not in specification. Example: assert agent._internal_flag (not in spec - wrong)

- **place_imports_at_top**: Place all imports at top of test file, after docstrings, before code. Group: stdlib, third-party, then local. Example: import json; import pytest; from mymodule import MyClass
  DO: All imports at top, grouped by type. Example: import json; import pytest; from agile_bot.bots... import X
  DON'T: Don't place imports inside functions or after code. Example: def test(): from pathlib import Path (wrong - import inside function)

- **object_oriented_test_helpers**: Consolidate tests around object-oriented helpers/factories (e.g., BotTestHelper test hopper) that build complete domain objects with standard data. Example: helper = BotTestHelper(tmp_path); helper.set_state('shape','clarify'); helper.assert_at_behavior_action('shape','clarify'). Avoid scattering many primitive parameters across parametrize blocks or inline setups.
  DO: Use shared helper objects to create full test fixtures and assert against complete domain objects, not fragments.
  DON'T: Do not spread test setup across many primitive parameters or cherry-pick single values from partial objects.

- **production_code_explicit_dependencies**: Production code: make dependencies explicit through constructor injection. Pass all external dependencies as constructor parameters. No hidden global state. Tests easily inject test doubles. Example: Agent(config_loader=loader, domain_graph=graph)
  DO: Inject all dependencies through constructor. Example: def __init__(self, config_loader, domain_graph): self._loader = config_loader
  DON'T: Don't access globals, singletons, or create dependencies internally. Example: self._loader = ConfigLoader() (wrong - creates internally)

- **self_documenting_tests**: Tests are self-documenting through code structure. Don't add verbose comments explaining failures. Imports, calls, and assertions show the API design. Let code speak for itself. Example: generator = MCPServerGenerator(bot_name, config_path); server = generator.generate_server()
  DO: Let code structure document the test. Example: generator = MCPServerGenerator(name, config); file = generator.generate() - API is clear
  DON'T: Don't add verbose comments explaining obvious things. Example: # This will fail because API doesn't exist yet (unnecessary)

- **standard_test_data_sets**: Use standard, named test data sets across tests instead of recreating ad-hoc values. Example: STANDARD_STATE = {...}; helper.set_state(...); assert helper.get_state() == STANDARD_STATE.
  DO: Define canonical data once (helper constants/factories) and reuse it so every test exercises the full domain object.
  DON'T: Do not create new ad-hoc values per test or assert only one field from a complex object.

- **assert_full_results**: Assert full domain results (state/log/graph objects), not single cherry-picked fields. Example: assert helper.get_state() == STANDARD_STATE, not assert helper.get_state()['current'] == 'shape.clarify'.
  DO: Compare entire objects/dicts/dataclasses against standard data fixtures.
  DON'T: Do not assert single fields or lengths when validating complex results.

- **use_ascii_only**: All test code must use ASCII-only characters. No Unicode symbols, emojis, or special characters. Use plain ASCII alternatives. Example: print('[PASS] Success') not print('[checkmark] Success')
  DO: Use ASCII-only characters. Example: print('[PASS] Agent initialized'); print('[ERROR] Config not found')
  DON'T: Don't use Unicode or emojis. Example: print('[checkmark] Done') (wrong); print('[green_check] OK') (wrong)

- **pytest_bdd_orchestrator_pattern**: Use pytest with orchestrator pattern for story-based tests. NO FEATURE FILES. Test classes contain orchestrator methods (under 20 lines) showing Given-When-Then flow by calling helper functions. Example: def test_agent_loads_config(): given_config_exists(); agent = when_agent_initialized(); then_agent_is_configured(agent)
  DO: Orchestrator pattern: test shows flow, delegates to helpers. Example: # Given; create_config_file(); # When; agent.initialize(); # Then; assert agent.is_initialized
  DON'T: Don't use feature files or inline complex setup. Example: @given('config exists') def step(): ... (wrong - use pytest directly)

- **use_exact_variable_names**: Use exact variable names from specification scenarios. When spec mentions agent_name, workspace_root, config_path - use those exact names in tests and production code. Example: agent_name = 'story_bot' (from spec), not name = 'story_bot'
  DO: Use exact names from specification in tests and production. Example: agent_name, workspace_root, config_path - all from spec
  DON'T: Don't use different names than specification. Example: name = 'bot' when spec says agent_name (wrong)

- **use_given_when_then_helpers**: Use reusable helper functions instead of inline code blocks of 4+ lines. Optimize for reusability, not exact step names. Place helpers at correct scope: story-level in class, sub-epic in module, epic in separate file. Example: given_config_exists(), when_agent_initialized(), then_agent_is_configured()
  DO: Use Given/When/Then helper functions for setup, action, assertion. Example: given_bot_config_exists(); bot = when_bot_instantiated(); then_bot_uses_correct_directories(bot)
  DON'T: Don't use inline operations of 4+ lines. Example: config_dir = ...; config_dir.mkdir(); config_file = ...; config_file.write_text() (wrong - extract to helper)

---
## Next action: tests.validate
**Next:** Perform the following action. Fix any errors found in the Violation.

## Action Instructions - validate

The purpose of this action is to validate story graph and/or artifacts against behavior-specific rules, checking for violations and compliance

specification_tests: validate test code and domain language usage
Validate that test code uses proper domain terminology (class names = domain entities, method names = domain responsibilities)
Validate that all test files, classes, and methods are properly mapped to story-graph.json

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

## Step 1: Run Scanners Then Review Violations

**Scanners you must run (with params below). Do not assume pre-run results.**

| Rule | Rule file | Scanner module |
|------|-----------|----------------|
| Use Class Based Organization | `story_bot/behaviors/tests/rules/use_class_based_organization.json` | `scanners.code.python.class_based_organization_scanner.ClassBasedOrganizationScanner` |
| Use Domain Language | `story_bot/behaviors/tests/rules/use_domain_language.json` | `scanners.code.python.domain_language_code_scanner.DomainLanguageCodeScanner` |
| Consistent Vocabulary | `story_bot/behaviors/tests/rules/consistent_vocabulary.json` | `scanners.code.python.consistent_vocabulary_scanner.ConsistentVocabularyScanner` |
| Domain Oriented Test Inheritance | `story_bot/behaviors/tests/rules/domain_oriented_test_inheritance.json` | `scanners.code.python.duplicate_assertion_scanner.DuplicateAssertionScanner` |
| No Defensive Code In Tests | `story_bot/behaviors/tests/rules/no_defensive_code_in_tests.json` | `scanners.code.python.excessive_guards_scanner.ExcessiveGuardsScanner` |
| Production Code Clean Functions | `story_bot/behaviors/tests/rules/production_code_clean_functions.json` | `scanners.code.python.function_size_scanner.FunctionSizeScanner` |
| Bug Fix Test First | `story_bot/behaviors/tests/rules/bug_fix_test_first.json` | `scanners.bug_fix_test_first_scanner.BugFixTestFirstScanner` |
| Call Production Code Directly | `story_bot/behaviors/tests/rules/call_production_code_directly.json` | `scanners.code.python.real_implementations_scanner.RealImplementationsScanner` |
| Cover All Behavior Paths | `story_bot/behaviors/tests/rules/cover_all_behavior_paths.json` | `scanners.code.python.cover_all_paths_scanner.CoverAllPathsScanner` |
| Mock Only Boundaries | `story_bot/behaviors/tests/rules/mock_only_boundaries.json` | `scanners.code.python.mock_boundaries_scanner.MockBoundariesScanner` |
| Create Parameterized Tests For Scenarios | `story_bot/behaviors/tests/rules/create_parameterized_tests_for_scenarios.json` | `scanners.parameterized_tests_scanner.ParameterizedTestsScanner` |
| Define Fixtures In Test File | `story_bot/behaviors/tests/rules/define_fixtures_in_test_file.json` | `scanners.code.python.fixture_placement_scanner.FixturePlacementScanner` |
| Design Api Through Failing Tests | `story_bot/behaviors/tests/rules/design_api_through_failing_tests.json` | `scanners.failing_test_api_scanner.FailingTestApiScanner` |
| Test Observable Behavior | `story_bot/behaviors/tests/rules/test_observable_behavior.json` | `scanners.code.python.observable_behavior_scanner.ObservableBehaviorScanner` |
| Helper Extraction And Reuse | `story_bot/behaviors/tests/rules/helper_extraction_and_reuse.json` | `scanners.helper_extraction_scanner.HelperExtractionScanner` |
| Match Specification Scenarios | `story_bot/behaviors/tests/rules/match_specification_scenarios.json` | `scanners.specification_match_scanner.SpecificationMatchScanner` |
| Place Imports At Top | `story_bot/behaviors/tests/rules/place_imports_at_top.json` | `scanners.code.python.import_placement_scanner.ImportPlacementScanner` |
| Object Oriented Test Helpers | `story_bot/behaviors/tests/rules/object_oriented_test_helpers.json` | `scanners.code.python.object_oriented_helpers_scanner.ObjectOrientedHelpersScanner` |
| Production Code Explicit Dependencies | `story_bot/behaviors/tests/rules/production_code_explicit_dependencies.json` | `scanners.code.python.explicit_dependencies_scanner.ExplicitDependenciesScanner` |
| Self Documenting Tests | `story_bot/behaviors/tests/rules/self_documenting_tests.json` | `scanners.code.python.intention_revealing_names_scanner.IntentionRevealingNamesScanner` |
| Standard Test Data Sets | `story_bot/behaviors/tests/rules/standard_test_data_sets.json` | `scanners.code.python.standard_data_reuse_scanner.StandardDataReuseScanner` |
| Assert Full Results | `story_bot/behaviors/tests/rules/assert_full_results.json` | `scanners.code.python.full_result_assertions_scanner.FullResultAssertionsScanner` |
| Use Ascii Only | `story_bot/behaviors/tests/rules/use_ascii_only.json` | `scanners.code.python.ascii_only_scanner.AsciiOnlyScanner` |
| Pytest Bdd Orchestrator Pattern | `story_bot/behaviors/tests/rules/pytest_bdd_orchestrator_pattern.json` | `scanners.orchestrator_pattern_scanner.OrchestratorPatternScanner` |
| Use Exact Variable Names | `story_bot/behaviors/tests/rules/use_exact_variable_names.json` | `scanners.code.python.exact_variable_names_scanner.ExactVariableNamesScanner` |
| Use Given When Then Helpers | `story_bot/behaviors/tests/rules/use_given_when_then_helpers.json` | `scanners.code.python.given_when_then_helpers_scanner.GivenWhenThenHelpersScanner` |

**Params to pass when running scanners:**
- **Scope:** all epics, sub-epics, stories, and domain concepts in the story graph
- **Workspace:** `C:\dev\agile_bots`
- **Story graph path:** `docs/story/story-graph.json` (or behavior-specific path)

Run each scanner with the above scope and workspace; then report violations and fix the story graph as needed.

Run each scanner with the params above, then review the violations they report as follows:
1. For each violation message, locate the corresponding element in the story graph.
2. Open the relevant rule file and read all DO and DON'T examples thoroughly.
3. Decide if the violation is **Valid** (truly a rule breach per examples) or a **False Positive** (explain why if so).
4. Determine the **Root Cause** (e.g., 'incorrect concept naming', 'missing actor', etc.).
5. Assign a **Theme** grouping based on the type of issue (e.g., 'noun-only naming', 'incomplete acceptance criteria').
6. Extract an **Example** from the actual code/content showing the problem.
7. Suggest a clear, concrete **Fix** with a code example informed by DO examples in the rule.

## Step 2: Manual Rule Review

**Rules to validate against (read each file for full DO/DON'T examples):**

### Rule: Use Class Based Organization (Priority 1) [Scanner]
**File:** `story_bot/behaviors/tests/rules/use_class_based_organization.json`
**Description:** CRITICAL STRUCTURAL RULE: Test structure matches story graph hierarchy. File = sub-epic (test_<sub_epic>.py), Class = story (Test<ExactStoryName>), Method = scenario (test_<scenario_snake_case>). Getting this wrong creates files in wrong locations requiring deletion/recreation. BEFORE writing any test code, identify the parent sub-epic that contains the story.
**DO:** Map story hierarchy to test structure exactly. CRITICAL: File name comes from SUB-EPIC, not story.
**DON'T:** Don't use generic/abbreviated names or wrong hierarchy level for file naming. Don't create files in wrong locations.

### Rule: Use Domain Language (Priority 1) [Scanner]
**File:** `story_bot/behaviors/tests/rules/use_domain_language.json`
**Description:** Use Ubiquitous Language (DDD): Same vocabulary in domain model, stories, scenarios, AND code. Class names = domain entities/nouns. Method names = domain responsibilities/verbs. Test names read like plain English stories. Example: test_agent_loads_configuration_when_file_exists (not test_agt_init_sets_vars)
**DO:** Use domain language for classes, methods, and test names. Example: class GatherContextAction, def inject_guardrails(), test_agent_loads_config_when_file_exists
**DON'T:** Don't use generic technical terms or implementation-specific names. Example: class StdioHandler (wrong), def execute_with_guardrails (wrong), test_agt_init_sets_vars (wrong)

### Rule: Consistent Vocabulary (Priority 2) [Scanner]
**File:** `story_bot/behaviors/tests/rules/consistent_vocabulary.json`
**Description:** Use ONE word per concept across entire codebase. Pick consistent vocabulary: create (not build/make/construct), verify (not check/assert/validate), load (not fetch/get/retrieve). Use intention-revealing names that describe behavior. Example: create_agent(), verify_initialized(), load_config() - same verbs everywhere
**DO:** Use same word for same concept everywhere. Example: create_agent(), create_config(), create_workspace() - all use 'create'
**DON'T:** Don't mix synonyms for same concept. Example: create_agent() + build_config() + make_workspace() (wrong - pick one verb)

### Rule: Domain Oriented Test Inheritance (Priority 3) [Scanner]
**File:** `story_bot/behaviors/tests/rules/domain_oriented_test_inheritance.json`
**Description:** Scaling extension of helper_extraction_and_reuse, object_oriented_test_helpers, and standard_test_data_sets. At small scale, a single test class covering multiple domain objects is fine. As domain objects develop distinct behavior, break out into domain-specific test classes. Use abstract base classes for common operations. Share parameter data and fixtures only when there is obvious shared logic across sub-epics. Place shared base files at the appropriate hierarchy level.
**DO:** At small scale keep together. As you scale, use abstract bases, share fixtures only with explicit need, and place shared files at the right hierarchy level.
**DON'T:** When scaling, do not copy assertion logic, do not create shared files preemptively, and do not group tests by operation or technology.

### Rule: No Defensive Code In Tests (Priority 3) [Scanner]
**File:** `story_bot/behaviors/tests/rules/no_defensive_code_in_tests.json`
**Description:** Tests must NEVER contain guard clauses, defensive conditionals, or fallback paths. We control test setup - if it's wrong, the test MUST fail immediately. Guard clauses hide problems. Tests should assume positive outcomes. Example: Just call the code directly, don't wrap in if-checks
**DO:** Assume correct setup - let test fail if wrong. Example: behavior = Behavior(name='shape') then assert behavior.name == 'shape'
**DON'T:** Don't add if-checks, type guards, or fallback handling in tests. Example: if behavior_file.exists(): (wrong - test should fail if it doesn't)

### Rule: Production Code Clean Functions (Priority 4) [Scanner]
**File:** `story_bot/behaviors/tests/rules/production_code_clean_functions.json`
**Description:** Production code functions should do ONE thing, be under 20 lines, and have one level of abstraction. No hidden side effects. Name reveals complete behavior. Extract multiple concerns into separate functions. Example: load_config(), validate_config(), apply_config() - each does one thing
**DO:** Single responsibility, small focused functions. Example: initialize_from_config() calls validate_exists(), load_config(), validate_structure(), apply_config()
**DON'T:** Don't make functions that do multiple unrelated things or are too long. Example: 50-line function that loads, validates, and applies config

### Rule: Bug Fix Test First (Priority 5) [Scanner]
**File:** `story_bot/behaviors/tests/rules/bug_fix_test_first.json`
**Description:** When production code breaks, follow test-first workflow: write failing test, verify failure, fix code, verify success. Never fix bugs without a failing test first. Example: test_mcp_tool_initializes_bot() fails -> fix initialization -> test passes
**DO:** Follow RED-GREEN-PRODUCTION workflow. Example: Write test reproducing bug -> Run test (RED) -> Fix minimal code -> Run test (GREEN) -> Run full suite
**DON'T:** Don't fix bugs directly without failing test first. Example: Editing production code without test -> deploying -> hoping it works (wrong)

### Rule: Call Production Code Directly (Priority 6) [Scanner]
**File:** `story_bot/behaviors/tests/rules/call_production_code_directly.json`
**Description:** Call production code directly in tests. Let tests fail naturally if code doesn't exist. Don't comment out calls, mock business logic, or fake state. Only mock external boundaries. Example: agent = Agent(); agent.initialize() (not agent = Mock())
**DO:** Call production code directly, let it fail naturally. Example: agent = Agent(workspace); agent.initialize(config); assert agent.is_initialized
**DON'T:** Don't mock class under test, comment out calls, or fake state. Example: agent = Mock(spec=Agent) (wrong); agent._initialized = True (wrong)

### Rule: Cover All Behavior Paths (Priority 7) [Scanner]
**File:** `story_bot/behaviors/tests/rules/cover_all_behavior_paths.json`
**Description:** Cover all behavior paths: normal (happy path), edge cases, and failure scenarios. Each distinct behavior needs its own focused test. Tests must be independent. Example: test_loads_valid_config(), test_loads_empty_config(), test_raises_error_when_file_missing()
**DO:** Test normal, edge, and failure paths separately. Example: test_loads_valid_config() (happy), test_loads_empty_config() (edge), test_raises_when_missing() (failure)
**DON'T:** Don't test only happy path or combine multiple behaviors in one test. Example: Single test for both success and failure (wrong)

### Rule: Mock Only Boundaries (Priority 8) [Scanner]
**File:** `story_bot/behaviors/tests/rules/mock_only_boundaries.json`
**Description:** Mock ONLY at architectural boundaries: external APIs, network, uncontrollable services. Don't mock internal business logic, classes under test, or file operations (use temp files). Example: patch('requests.get') (OK); patch('agent.validate') (wrong)
**DO:** Mock only external dependencies you can't control. Example: with patch('requests.get') as mock: (external API - OK to mock)
**DON'T:** Don't mock internal logic, class under test, or file I/O. Example: with patch('agent.validate_config') (wrong - test the logic!)

### Rule: Create Parameterized Tests For Scenarios (Priority 9) [Scanner]
**File:** `story_bot/behaviors/tests/rules/create_parameterized_tests_for_scenarios.json`
**Description:** If scenarios have Examples tables, create parameterized tests using @pytest.mark.parametrize. Each row becomes a test case. Don't write single tests that only test one example. Example: @pytest.mark.parametrize('input,expected', [(1, 2), (3, 4)])
**DO:** Create parameterized tests from Examples tables. Example: @pytest.mark.parametrize('paths,count', [(['p1','p2'], 2), (['p3'], 1)])
**DON'T:** Don't hardcode single example or duplicate test methods. Example: def test_with_value_1(): (wrong); def test_with_value_2(): (wrong - use parametrize)

### Rule: Define Fixtures In Test File (Priority 10) [Scanner]
**File:** `story_bot/behaviors/tests/rules/define_fixtures_in_test_file.json`
**Description:** Define fixtures in the test file, not separate conftest.py. Truly reusable fixtures (file ops, location helpers) go in base conftest.py. Example: @pytest.fixture def workspace_root(tmp_path): return tmp_path / 'workspace'
**DO:** Define fixtures in same test file. Example: @pytest.fixture def config_file(tmp_path): ... (in test_agent.py)
**DON'T:** Don't create separate conftest.py for agent-specific fixtures. Don't create shared files without explicit need.

### Rule: Design Api Through Failing Tests (Priority 11) [Scanner]
**File:** `story_bot/behaviors/tests/rules/design_api_through_failing_tests.json`
**Description:** Write tests against the REAL expected API BEFORE implementing code. Tests MUST fail initially. Set up real test data and call real API. Failure reveals complete API design. Example: project = Project(path=path); project.initialize() (doesn't exist yet -> fails -> drives implementation)
**DO:** Write test against real expected API that fails initially. Example: project = Project(path); project.initialize(); assert project.is_ready (fails until implemented)
**DON'T:** Don't use placeholders, dummy values, or skip the failing step. Example: project = 'TODO' (wrong); assuming test passes first (wrong)

### Rule: Test Observable Behavior (Priority 12) [Scanner]
**File:** `story_bot/behaviors/tests/rules/test_observable_behavior.json`
**Description:** Test observable behavior, not implementation details. Verify public API and visible state changes. Don't assert on private methods or internal flags. Example: assert agent.config_path.exists() (observable); not assert agent._internal_flag (private)
**DO:** Test observable outcomes through public API. Example: assert agent.config_path == expected; assert agent.is_initialized (public properties)
**DON'T:** Don't test private state or implementation details. Example: assert agent._initialized (wrong); assert agent._config_cache (wrong)

### Rule: Helper Extraction And Reuse (Priority 13) [Scanner]
**File:** `story_bot/behaviors/tests/rules/helper_extraction_and_reuse.json`
**Description:** Extract duplicate test setup to reusable helper functions. Keep test bodies focused on specific behavior. Example: create_agent_with_config(), create_config_file(), verify_agent_initialized() - reusable across tests
**DO:** Extract duplicate setup to reusable helpers. Example: create_agent_with_config(name, workspace, config) returns initialized Agent
**DON'T:** Don't duplicate setup code across tests. Example: Same 10 lines of setup in every test method (wrong - extract to helper)

### Rule: Match Specification Scenarios (Priority 14) [Scanner]
**File:** `story_bot/behaviors/tests/rules/match_specification_scenarios.json`
**Description:** Tests must match specification scenarios exactly. Test names, steps, and assertions verify exactly what the scenario states. Use exact variable names and terminology from specification. Example: agent_name='story_bot' (from spec), not name='bot'
**DO:** Test matches specification exactly. Example: GIVEN config exists, WHEN Agent(agent_name='story_bot'), THEN config_path == agents/base/agent.json
**DON'T:** Don't use different terminology or assert things not in specification. Example: assert agent._internal_flag (not in spec - wrong)

### Rule: Place Imports At Top (Priority 15) [Scanner]
**File:** `story_bot/behaviors/tests/rules/place_imports_at_top.json`
**Description:** Place all imports at top of test file, after docstrings, before code. Group: stdlib, third-party, then local. Example: import json; import pytest; from mymodule import MyClass
**DO:** All imports at top, grouped by type. Example: import json; import pytest; from agile_bot.bots... import X
**DON'T:** Don't place imports inside functions or after code. Example: def test(): from pathlib import Path (wrong - import inside function)

### Rule: Object Oriented Test Helpers (Priority 16) [Scanner]
**File:** `story_bot/behaviors/tests/rules/object_oriented_test_helpers.json`
**Description:** Consolidate tests around object-oriented helpers/factories (e.g., BotTestHelper test hopper) that build complete domain objects with standard data. Example: helper = BotTestHelper(tmp_path); helper.set_state('shape','clarify'); helper.assert_at_behavior_action('shape','clarify'). Avoid scattering many primitive parameters across parametrize blocks or inline setups.
**DO:** Use shared helper objects to create full test fixtures and assert against complete domain objects, not fragments.
**DON'T:** Do not spread test setup across many primitive parameters or cherry-pick single values from partial objects.

### Rule: Production Code Explicit Dependencies (Priority 16) [Scanner]
**File:** `story_bot/behaviors/tests/rules/production_code_explicit_dependencies.json`
**Description:** Production code: make dependencies explicit through constructor injection. Pass all external dependencies as constructor parameters. No hidden global state. Tests easily inject test doubles. Example: Agent(config_loader=loader, domain_graph=graph)
**DO:** Inject all dependencies through constructor. Example: def __init__(self, config_loader, domain_graph): self._loader = config_loader
**DON'T:** Don't access globals, singletons, or create dependencies internally. Example: self._loader = ConfigLoader() (wrong - creates internally)

### Rule: Self Documenting Tests (Priority 17) [Scanner]
**File:** `story_bot/behaviors/tests/rules/self_documenting_tests.json`
**Description:** Tests are self-documenting through code structure. Don't add verbose comments explaining failures. Imports, calls, and assertions show the API design. Let code speak for itself. Example: generator = MCPServerGenerator(bot_name, config_path); server = generator.generate_server()
**DO:** Let code structure document the test. Example: generator = MCPServerGenerator(name, config); file = generator.generate() - API is clear
**DON'T:** Don't add verbose comments explaining obvious things. Example: # This will fail because API doesn't exist yet (unnecessary)

### Rule: Standard Test Data Sets (Priority 17) [Scanner]
**File:** `story_bot/behaviors/tests/rules/standard_test_data_sets.json`
**Description:** Use standard, named test data sets across tests instead of recreating ad-hoc values. Example: STANDARD_STATE = {...}; helper.set_state(...); assert helper.get_state() == STANDARD_STATE.
**DO:** Define canonical data once (helper constants/factories) and reuse it so every test exercises the full domain object.
**DON'T:** Do not create new ad-hoc values per test or assert only one field from a complex object.

### Rule: Assert Full Results (Priority 18) [Scanner]
**File:** `story_bot/behaviors/tests/rules/assert_full_results.json`
**Description:** Assert full domain results (state/log/graph objects), not single cherry-picked fields. Example: assert helper.get_state() == STANDARD_STATE, not assert helper.get_state()['current'] == 'shape.clarify'.
**DO:** Compare entire objects/dicts/dataclasses against standard data fixtures.
**DON'T:** Do not assert single fields or lengths when validating complex results.

### Rule: Use Ascii Only (Priority 18) [Scanner]
**File:** `story_bot/behaviors/tests/rules/use_ascii_only.json`
**Description:** All test code must use ASCII-only characters. No Unicode symbols, emojis, or special characters. Use plain ASCII alternatives. Example: print('[PASS] Success') not print('[checkmark] Success')
**DO:** Use ASCII-only characters. Example: print('[PASS] Agent initialized'); print('[ERROR] Config not found')
**DON'T:** Don't use Unicode or emojis. Example: print('[checkmark] Done') (wrong); print('[green_check] OK') (wrong)

### Rule: Pytest Bdd Orchestrator Pattern (Priority 19) [Scanner]
**File:** `story_bot/behaviors/tests/rules/pytest_bdd_orchestrator_pattern.json`
**Description:** Use pytest with orchestrator pattern for story-based tests. NO FEATURE FILES. Test classes contain orchestrator methods (under 20 lines) showing Given-When-Then flow by calling helper functions. Example: def test_agent_loads_config(): given_config_exists(); agent = when_agent_initialized(); then_agent_is_configured(agent)
**DO:** Orchestrator pattern: test shows flow, delegates to helpers. Example: # Given; create_config_file(); # When; agent.initialize(); # Then; assert agent.is_initialized
**DON'T:** Don't use feature files or inline complex setup. Example: @given('config exists') def step(): ... (wrong - use pytest directly)

### Rule: Use Exact Variable Names (Priority 21) [Scanner]
**File:** `story_bot/behaviors/tests/rules/use_exact_variable_names.json`
**Description:** Use exact variable names from specification scenarios. When spec mentions agent_name, workspace_root, config_path - use those exact names in tests and production code. Example: agent_name = 'story_bot' (from spec), not name = 'story_bot'
**DO:** Use exact names from specification in tests and production. Example: agent_name, workspace_root, config_path - all from spec
**DON'T:** Don't use different names than specification. Example: name = 'bot' when spec says agent_name (wrong)

### Rule: Use Given When Then Helpers (Priority 22) [Scanner]
**File:** `story_bot/behaviors/tests/rules/use_given_when_then_helpers.json`
**Description:** Use reusable helper functions instead of inline code blocks of 4+ lines. Optimize for reusability, not exact step names. Place helpers at correct scope: story-level in class, sub-epic in module, epic in separate file. Example: given_config_exists(), when_agent_initialized(), then_agent_is_configured()
**DO:** Use Given/When/Then helper functions for setup, action, assertion. Example: given_bot_config_exists(); bot = when_bot_instantiated(); then_bot_uses_correct_directories(bot)
**DON'T:** Don't use inline operations of 4+ lines. Example: config_dir = ...; config_dir.mkdir(); config_file = ...; config_file.write_text() (wrong - extract to helper)


Scanner tools don't cover or catch every rule violation. Do a second pass:
1. Carefully read each rule file, fully reviewing DO and DON'T sections, and every provided example.
2. Inspect all epics, sub-epics, stories, and domain concepts in the story graph for compliance.
3. Compare the properties and content of each element against the rule's requirements.
4. Document any violations the scanner could not find.
5. For each violation, extract an **Example** showing the problem and provide a **Fix** with code example.

## Violations Found

Record ALL findings (scanner + manual) using this readable format. Group by theme for narrow IDE chat panels:

### [Theme Name] (X violations)

**1. [Rule Name]**
- Location: `path.to.element`
- Status: Valid / False Positive
- Source: Scanner / Manual / Both
- Problem: `"actual problematic text"`
- Fix: `"corrected text"`
- Root Cause: Brief explanation

**2. [Rule Name]**
- Location: `path.to.element`
- ...

---

### [Next Theme] (Y violations)
...

Use this list format instead of tables - tables are unreadable in narrow IDE side chat panels.

## Step 3: Summarize Findings & Recommendations

Provide a concise summary:
- Report how many **scanner violations** were valid vs false positives.
- Enumerate any **additional manual findings** not caught by scanners.
- Group all violations by recurring theme or pattern.
- Split violations into **Priority Fixes** (must resolve before continuing) and **Optional Improvements**.

Present your summary and await user confirmation before automatically applying or proposing corrections.
specification_tests: validate test code and domain language usage
Validate that test code uses proper domain terminology (class names = domain entities, method names = domain responsibilities)
Validate that all test files, classes, and methods are properly mapped to story-graph.json**Combined instructions:** The following combines multiple actions. Perform them one after another.

## Scope

**Story Scope:** "Submit Instructions From Workspace"

Please only work on the following scope.

Scope Filter: ""Submit Instructions From Workspace""

Scope:

{
  "path": "C:\\dev\\agile_bots\\docs\\story\\story-graph.json",
  "has_epics": true,
  "has_increments": true,
  "has_domain_concepts": true,
  "epic_count": 1,
  "content": {
    "epics": [
      {
        "name": "Invoke Bot",
        "sub_epics": [
          {
            "name": "Navigate Behavior Actions",
            "sub_epics": [
              {
                "name": "Perform Behavior Action In Bot Workflow",
                "sub_epics": [],
                "story_groups": [
                  {
                    "name": null,
                    "stories": [
                      {
                        "name": "Submit Instructions From Workspace",
                        "acceptance_criteria": [
                          {
                            "name": "WHEN User has instructions visible in workspace section\nTHEN Panel displays Submit button AND User can trigger submit to send instructions to AI agent",
                            "text": "WHEN User has instructions visible in workspace section\nTHEN Panel displays Submit button AND User can trigger submit to send instructions to AI agent",
                            "sequential_order": 0.0
                          },
                          {
                            "name": "WHEN No {Behavior} selected\nTHEN System shows scope error or disables submit",
                            "text": "WHEN No {Behavior} selected\nTHEN System shows scope error or disables submit",
                            "sequential_order": 1.0
                          }
                        ],
                        "scenarios": [
                          {
                            "name": "User submits {Behavior} instructions to AI agent",
                            "background": [],
                            "steps": [
                              {
                                "text": "Given {Behavior} \"shape\" is selected in workspace",
                                "sequential_order": 1.0
                              },
                              {
                                "text": "And {InstructionsSection} displays shape instructions",
                                "sequential_order": 2.0
                              },
                              {
                                "text": "When User triggers submit from workspace",
                                "sequential_order": 3.0
                              },
                              {
                                "text": "Then System sends {Behavior} shape instructions to AI agent",
                                "sequential_order": 4.0
                              },
                              {
                                "text": "And Submit button is visible and enabled",
                                "sequential_order": 5.0
                              }
                            ],
                            "examples": null
                          },
                          {
                            "name": "Submit disabled when no behavior selected",
                            "background": [],
                            "steps": [
                              {
                                "text": "Given no {Behavior} is selected in workspace",
                                "sequential_order": 1.0
                              },
                              {
                                "text": "When User views workspace section",
                                "sequential_order": 2.0
                              },
                              {
                                "text": "Then Submit shows scope error or is disabled",
                                "sequential_order": 3.0
                              },
                              {
                                "text": "And User cannot submit empty instructions",
                                "sequential_order": 4.0
                              }
                            ],
                            "examples": null
                          }
                        ]
                      }
                    ]
                  }
                ],
                "domain_concepts": [
                  {
                    "name": "Base Action",
                    "responsibilities": [
                      {
                        "name": "Inject Instructions",
                        "collaborators": [
                          "Behavior"
                        ]
                      },
                      {
                        "name": "Load Relevant Content + Inject Into Instructions",
                        "collaborators": [
                          "Content"
                        ]
                      },
                      {
                        "name": "Save content changes",
                        "collaborators": [
                          "Content"
                        ]
                      },
                      {
                        "name": "Get save file",
                        "collaborators": [
                          "Path"
                        ]
                      },
                      {
                        "name": "Execution gates on save file watch",
                        "collaborators": [
                          "SaveFileWatcher",
                          "Debounce",
                          "Next Action"
                        ]
                      }
                    ],
                    "module": "actions",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "SaveFileWatcher",
                    "responsibilities": [
                      {
                        "name": "Watch save file for writes",
                        "collaborators": [
                          "Path",
                          "File System"
                        ]
                      },
                      {
                        "name": "Report when file stable past debounce",
                        "collaborators": [
                          "Path",
                          "Debounce",
                          "Boolean"
                        ]
                      }
                    ],
                    "module": "actions",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "ActionStateManager",
                    "responsibilities": [
                      {
                        "name": "Get state file path",
                        "collaborators": [
                          "Path"
                        ]
                      },
                      {
                        "name": "Load or create state",
                        "collaborators": [
                          "State File",
                          "Dict"
                        ]
                      },
                      {
                        "name": "Save state",
                        "collaborators": [
                          "Action",
                          "State File"
                        ]
                      },
                      {
                        "name": "Load state",
                        "collaborators": [
                          "Actions List",
                          "Current Index"
                        ]
                      },
                      {
                        "name": "Find action index",
                        "collaborators": [
                          "Actions List",
                          "Action Name",
                          "Integer"
                        ]
                      },
                      {
                        "name": "Filter completed actions",
                        "collaborators": [
                          "Completed Actions",
                          "Target Index",
                          "Actions List",
                          "List"
                        ]
                      }
                    ],
                    "module": "actions",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "TTYAction",
                    "responsibilities": [
                      {
                        "name": "Serialize action to TTY",
                        "collaborators": [
                          "Action",
                          "String"
                        ]
                      },
                      {
                        "name": "Format action line",
                        "collaborators": [
                          "Action Name",
                          "Marker",
                          "Indent"
                        ]
                      },
                      {
                        "name": "Wraps domain action",
                        "collaborators": [
                          "Action"
                        ]
                      }
                    ],
                    "module": "actions",
                    "inherits_from": "TTYProgressAdapter",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "JSONAction",
                    "responsibilities": [
                      {
                        "name": "Serialize action to JSON dict",
                        "collaborators": [
                          "Action",
                          "Dict"
                        ]
                      },
                      {
                        "name": "Include action metadata",
                        "collaborators": [
                          "Name",
                          "Description",
                          "Status"
                        ]
                      },
                      {
                        "name": "Wraps domain action",
                        "collaborators": [
                          "Action"
                        ]
                      }
                    ],
                    "module": "actions",
                    "inherits_from": "JSONProgressAdapter",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "MarkdownAction",
                    "responsibilities": [
                      {
                        "name": "Serialize action to Markdown",
                        "collaborators": [
                          "Action",
                          "String"
                        ]
                      },
                      {
                        "name": "Format action documentation",
                        "collaborators": [
                          "Action Name",
                          "Description",
                          "Subsection"
                        ]
                      },
                      {
                        "name": "Wraps domain action",
                        "collaborators": [
                          "Action"
                        ]
                      }
                    ],
                    "module": "actions",
                    "inherits_from": "MarkdownProgressAdapter",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  }
                ]
              }
            ],
            "story_groups": []
          }
        ],
        "domain_concepts": []
      }
    ],
    "increments": []
  }
}

---

# Behavior: scenarios

## Behavior Instructions - scenarios

The purpose of this behavior is to write detailed plain-english scenarios (given/when/then) that specify exact behavior for each story

Write detailed plain-English scenarios (Given/When/Then) that specify exact behavior for each story

## Action Instructions - validate

The purpose of this action is to validate story graph and/or artifacts against behavior-specific rules, checking for violations and compliance

specification_scenarios: validate scenario structure and domain language usage
Validate that scenarios use proper domain terminology and reference domain concepts correctly

---

**Look for context in the following locations:**
- in this message and chat history
- `C:/dev/agile_bots/docs/story/story-graph.json` - the story graph and related  knowledge built so far
- `C:/dev/agile_bots/docs/story/strategy.json` - strategy decisions made
- `C:/dev/agile_bots/docs/story/clarification.json` - clarification answers
- `C:/dev/agile_bots/test/` and `C:/dev/agile_bots/src/` - existing code and tests
- any folder named `context/` anywhere in `C:/dev/agile_bots/` - additional context files

IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

## Step 1: Run Scanners Then Review Violations

**Scanners you must run (with params below). Do not assume pre-run results.**

| Rule | Rule file | Scanner module |
|------|-----------|----------------|
| Scenario Language Matches Domain | `story_bot/behaviors/scenarios/rules/scenario_language_matches_domain.json` | `scanners.scenarios.scenario_language_scanner.ScenarioLanguageScanner` |
| Example Tables Use Domain Language | `story_bot/behaviors/scenarios/rules/example_tables_use_domain_language.json` | `scanners.scenarios.example_table_scanner.ExampleTableScanner` |
| Given Describes State Not Actions | `story_bot/behaviors/scenarios/rules/given_describes_state_not_actions.json` | `scanners.scenarios.given_state_not_actions_scanner.GivenStateNotActionsScanner` |
| Background Vs Scenario Setup | `story_bot/behaviors/scenarios/rules/background_vs_scenario_setup.json` | `scanners.scenarios.background_common_setup_scanner.BackgroundCommonSetupScanner` |
| Scenarios Cover All Cases | `story_bot/behaviors/scenarios/rules/scenarios_cover_all_cases.json` | `scanners.scenarios.scenarios_cover_all_cases_scanner.ScenariosCoverAllCasesScanner` |
| Use Scenario Outline When Needed | `story_bot/behaviors/scenarios/rules/use_scenario_outline_when_needed.json` | `scanners.scenarios.scenario_outline_scanner.ScenarioOutlineScanner` |
| Write Concrete Scenarios | `story_bot/behaviors/scenarios/rules/write_concrete_scenarios.json` | `scanners.scenarios.parameterized_scenarios_scanner.ParameterizedScenariosScanner` |
| Scenarios On Story Docs | `story_bot/behaviors/scenarios/rules/scenarios_on_story_docs.json` | `scanners.scenarios.scenarios_on_story_docs_scanner.ScenariosOnStoryDocsScanner` |
| Map Table Columns To Scenario Parameters | `story_bot/behaviors/scenarios/rules/map_table_columns_to_scenario_parameters.json` | `scanners.table_column_parameter_scanner.TableColumnParameterScanner` |

**Params to pass when running scanners:**
- **Scope:** story/stories: "Submit Instructions From Workspace"
- **Workspace:** `C:\dev\agile_bots`
- **Story graph path:** `docs/story/story-graph.json` (or behavior-specific path)

Run each scanner with the above scope and workspace; then report violations and fix the story graph as needed.

Run each scanner with the params above, then review the violations they report as follows:
1. For each violation message, locate the corresponding element in the story graph.
2. Open the relevant rule file and read all DO and DON'T examples thoroughly.
3. Decide if the violation is **Valid** (truly a rule breach per examples) or a **False Positive** (explain why if so).
4. Determine the **Root Cause** (e.g., 'incorrect concept naming', 'missing actor', etc.).
5. Assign a **Theme** grouping based on the type of issue (e.g., 'noun-only naming', 'incomplete acceptance criteria').
6. Extract an **Example** from the actual code/content showing the problem.
7. Suggest a clear, concrete **Fix** with a code example informed by DO examples in the rule.

## Step 2: Manual Rule Review

**Rules to validate against (read each file for full DO/DON'T examples):**

### Rule: Scenario Language Matches Domain (Priority 1) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/scenario_language_matches_domain.json`
**Description:** Scenario language MUST use domain concept terminology. Given/When/Then steps should reference domain entities and concepts, not UI elements or technical implementation details.
**DO:** Use domain language in scenario steps - reference domain concepts by name.
**DON'T:** Don't use UI element names, technical implementation terms, or generic words instead of domain concepts.

### Rule: Example Tables Use Domain Language (Priority 2) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/example_tables_use_domain_language.json`
**Description:** Example tables MUST be grounded in scenario steps AND use domain-rich language. Table columns = nouns from Given/When/Then steps. Use domain terminology, not UI elements. Omit ID columns used purely for linking tables - relationships are expressed via collaboration field and table ordering. Concrete values with domain context, not generic JSON or placeholders. Use source entity data, not aggregated/calculated values - this is the stage where you figure out the real examples.
**DO:** Ground tables in scenario nouns, use domain terminology, connect tables using domain responsibility sentences. Omit implementation IDs. Show source entities, not derived counts.
**DON'T:** Don't use UI elements, flat lookup tables, generic JSON, abstract descriptions, invented terminology, or aggregated/calculated values.

### Rule: Given Describes State Not Actions (Priority 3) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/given_describes_state_not_actions.json`
**Description:** Given statements describe STATE/PRECONDITIONS, not actions or functionality. Given = what exists before test. When = first action. Then = expected behavior. Example: Given user is logged in (state), not Given user logs in (action).
**DO:** Given describes state/preconditions only. Example: 'Given user is logged in' (state), 'Given character sheet exists' (precondition)
**DON'T:** Don't describe actions, UI navigation, or functionality in Given. Example: 'Given user logs in' (action - wrong), 'Given User is on PaymentDetails step' (navigation - wrong)

### Rule: Background Vs Scenario Setup (Priority 4) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/background_vs_scenario_setup.json`
**Description:** Background = shared setup for 3+ scenarios (Given/And only, no When/Then). Background steps MUST use {Concept} notation to reference domain objects. Use {Concept.property} when a specific attribute is important. Don't repeat Background in Steps.
**DO:** Use Background for shared context with {Concept} references to example tables.
**DON'T:** Don't use hardcoded values or column names in Background - use {Concept} notation. Don't include When/Then.

### Rule: Scenarios Cover All Cases (Priority 5) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/scenarios_cover_all_cases.json`
**Description:** Scenarios must cover happy path, edge cases, and error cases based on acceptance criteria. Example: Valid input → success; Boundary value → validates; Invalid input → error message.
**DO:** Cover all case types: happy path, edge cases, error cases. Example: User enters valid data → success; User enters boundary → validates; User enters invalid → error
**DON'T:** Don't skip case types. Example: Only happy path scenarios (missing edge and error cases)

### Rule: Use Scenario Outline When Needed (Priority 6) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/use_scenario_outline_when_needed.json`
**Description:** Use Scenario Outline with Examples when story warrants concrete data: formulas need validation, domain has named entities, parameter variations exist. Example: Calculate ability modifier with Examples table Rank 10→0, Rank 12→+1, Rank 14→+2.
**DO:** Scenario Outline for formulas, domain entities, or data variations. Example: Scenario Outline: Calculate modifier with Examples table showing input→output pairs
**DON'T:** Don't use Scenario Outline for simple behaviors. Example: Scenario Outline: User clicks button (too simple - use regular scenario)

### Rule: Write Concrete Scenarios (Priority 7) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/write_concrete_scenarios.json`
**Description:** Parameterize domain concepts in scenarios using {Concept} notation for objects and {Concept.property} for specific attributes. Every {parameter} in Background/Steps MUST have corresponding example table. Use object references, not column names directly.
**DO:** Use {Concept} for object references, {Concept.property} for specific attributes. Connect to example tables.
**DON'T:** Don't hardcode values without examples, don't use non-domain placeholders, don't skip base data dependencies.

### Rule: Scenarios On Story Docs (Priority 8) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/scenarios_on_story_docs.json`
**Description:** Scenarios must be in story-graph.json (in scenarios or scenario_outlines fields), NOT in separate markdown files. NEVER create feature specification documents. Example: story-graph.json epics[].stories[].scenarios[], not docs/story/scenarios.md.
**DO:** Add scenarios to story-graph.json. Example: story-graph.json epics[].stories[].scenarios[] array
**DON'T:** Dont create separate scenario files or feature specifications. Example: docs/story/Epic/Feature/Feature Specification.md (wrong)

### Rule: Map Table Columns To Scenario Parameters (Priority 9) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/map_table_columns_to_scenario_parameters.json`
**Description:** Map example tables to {Concept} references bidirectionally. Every example table maps to a {Concept} in Background/Steps. Use {Concept} for object references and {Concept.property} for specific attributes. Keep tables minimal and domain-focused.
**DO:** Bidirectional mapping: Example table name ↔ {Concept} reference in steps.
**DON'T:** Don't use <column_name> notation - use {Concept} or {Concept.property}. Don't have orphaned tables or references.


Scanner tools don't cover or catch every rule violation. Do a second pass:
1. Carefully read each rule file, fully reviewing DO and DON'T sections, and every provided example.
2. Inspect story/stories: "Submit Instructions From Workspace" for compliance.
3. Compare the properties and content of each element against the rule's requirements.
4. Document any violations the scanner could not find.
5. For each violation, extract an **Example** showing the problem and provide a **Fix** with code example.

## Violations Found

Record ALL findings (scanner + manual) using this readable format. Group by theme for narrow IDE chat panels:

### [Theme Name] (X violations)

**1. [Rule Name]**
- Location: `path.to.element`
- Status: Valid / False Positive
- Source: Scanner / Manual / Both
- Problem: `"actual problematic text"`
- Fix: `"corrected text"`
- Root Cause: Brief explanation

**2. [Rule Name]**
- Location: `path.to.element`
- ...

---

### [Next Theme] (Y violations)
...

Use this list format instead of tables - tables are unreadable in narrow IDE side chat panels.

## Step 3: Summarize Findings & Recommendations

Provide a concise summary:
- Report how many **scanner violations** were valid vs false positives.
- Enumerate any **additional manual findings** not caught by scanners.
- Group all violations by recurring theme or pattern.
- Split violations into **Priority Fixes** (must resolve before continuing) and **Optional Improvements**.

Present your summary and await user confirmation before automatically applying or proposing corrections.
specification_scenarios: validate scenario structure and domain language usage
Validate that scenarios use proper domain terminology and reference domain concepts correctly

### Key Questions

- What system and user actions initiate this story's flow?
- What is the intended system response after each user action?
- What preconditions or data states are required before this story can begin?
- What are the success criteria for the story (from a domain and user perspective)?
- What are the expected alternate flows, error paths, and edge cases?
- Are there any mandatory sequencing constraints within or across stories?
- What domain rules, calculations, or business policies does this story validate?
- Is the story testable independently (including setup and teardown conditions)?
- What external systems or services does this story need to interact with?
- What requests, responses, or contracts are involved in those system interactions?
- Are there system integration points that require validation or simulation?
- How do we handle failures, timeouts, or retries for those system calls?
- What data variations (e.g., boundary conditions, common examples) are required for test coverage?
- What are the input values needed to test each scenario?
- What are the expected output values for each input?
- Are there formulas or calculations that need multiple data points to validate?
- Are there domain entities with named values that should be tested?
- What are the boundary conditions (min, max, edge cases) for each data point?

### Evidence

Acceptance criteria from Exploration stage (Domain AC at feature level, Behavioral AC at story level), High fidelity UX flows, Cross-functional walkthrough outputs, Integration contracts or API mocks, Behavior diagrams (state, sequence)

### Decisions

**Your Decisions:**

**examples_representation:**
  Verification Data Table

**scenario_outline:**
  Scenario Outline with Examples

**scenario_coverage:**
  - Happy Path
  - Edge Cases


### Assumptions

**Your Assumptions:**

- One story is specified at a time
- Acceptance criteria must be testable, unambiguous, and executable
- Gherkin syntax or structured language (Given/When/Then) is preferred
- Scenarios are written in plain English. When using Scenario Outline, variables are clearly marked and defined in Examples tables with actual test data.
- Examples tables when used must include ALL variables used in scenario steps
- Examples tables when used must have exact values for both input AND output variables
- Every variable when used in scenario steps must have a corresponding column in Examples table
- Examples tables when used must have actual test data, not placeholders
- Output/expected result variables must be included in Examples tables when used
- scnarios follow this pattern
- bulk of business logic tests done against the domain layer objects directly
- minimal happy path testing done with separate tgests that go theoiugh CLI
- JS nodetest for panel test focus on rendering and button layout

---
## Next action: render
**Next:** Perform the following action.

## Action Instructions - render

The purpose of this action is to render output documents and artifacts from story graph using templates and synchronizers

specification_scenarios: render story documents with scenarios

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

Please follow the instructions below in order to manually render output documents using templates

All render configurations are automatically loaded and injected below. Process ALL configs - do not skip any.



**Final Steps:**
- Process ALL configs above - do not skip any
- Priority order: synchronizer > template
- Verify each output file exists after execution
- If execution fails, report the error and continue with other outputs
- After completing all renders, pause and wait for human confirmation before proceeding to next behavior

**Creating New Render Outputs:**
If you need to create code to render a new output format:
1. Create a new synchronizer file in {workspace}/synchronizers/ (create folder if it doesn't exist)
2. Follow this signature pattern: output_file = synchronizer.render(story_graph_file)
3. The synchronizer should read the story-graph.json and produce the desired output file
4. Add the new synchronizer to the behavior's render config to include it in future renders
specification_scenarios: render story documents with scenarios
IMPORTANT: After completing all template-based rendering, you MUST execute the synchronizer-based render specs by running: scenarios.render.renderAll
This will render the following outputs: render_story_scenarios**Combined instructions:** The following combines multiple actions. Perform them one after another.

## Scope

**Story Scope:** "Render Diagram In Workspace"

Please only work on the following scope.

Scope Filter: ""Render Diagram In Workspace""

Scope:

{
  "path": "C:\\dev\\agile_bots\\docs\\story\\story-graph.json",
  "has_epics": true,
  "has_increments": true,
  "has_domain_concepts": true,
  "epic_count": 1,
  "content": {
    "epics": [
      {
        "name": "Invoke Bot",
        "sub_epics": [
          {
            "name": "Perform Action",
            "sub_epics": [
              {
                "name": "Render Content",
                "sub_epics": [],
                "story_groups": [
                  {
                    "name": null,
                    "stories": [
                      {
                        "name": "Render Diagram In Workspace",
                        "acceptance_criteria": [
                          {
                            "name": "WHEN Diagram is large\nTHEN Panel provides scroll or zoom AND Diagram remains readable",
                            "text": "WHEN Diagram is large\nTHEN Panel provides scroll or zoom AND Diagram remains readable",
                            "sequential_order": 0.0
                          },
                          {
                            "name": "WHEN User clicks diagram link\nTHEN System opens diagram file in editor",
                            "text": "WHEN User clicks diagram link\nTHEN System opens diagram file in editor",
                            "sequential_order": 1.0
                          }
                        ],
                        "scenarios": [
                          {
                            "name": "Workspace displays {DrawIOElement} diagram for scope",
                            "background": [],
                            "steps": [
                              {
                                "text": "Given {Behavior} \"shape\" is selected",
                                "sequential_order": 1.0
                              },
                              {
                                "text": "And scope has diagram output",
                                "sequential_order": 2.0
                              },
                              {
                                "text": "When workspace section renders",
                                "sequential_order": 3.0
                              },
                              {
                                "text": "Then {DrawIOElement} diagram links are displayed",
                                "sequential_order": 4.0
                              },
                              {
                                "text": "And User can open diagram in editor",
                                "sequential_order": 5.0
                              }
                            ],
                            "examples": null
                          },
                          {
                            "name": "Large diagram has scroll or zoom",
                            "background": [],
                            "steps": [
                              {
                                "text": "Given {DrawIOElement} diagram exceeds viewport",
                                "sequential_order": 1.0
                              },
                              {
                                "text": "When User views diagram in workspace",
                                "sequential_order": 2.0
                              },
                              {
                                "text": "Then Panel provides scroll or zoom",
                                "sequential_order": 3.0
                              },
                              {
                                "text": "And Diagram remains readable",
                                "sequential_order": 4.0
                              }
                            ],
                            "examples": null
                          }
                        ]
                      }
                    ]
                  }
                ],
                "domain_concepts": [
                  {
                    "name": "RenderOutputAction",
                    "responsibilities": [
                      {
                        "name": "Inject render output instructions",
                        "collaborators": [
                          "Behavior",
                          "Content",
                          "Render Spec",
                          "Renderer"
                        ]
                      },
                      {
                        "name": "Inject templates",
                        "collaborators": [
                          "Behavior",
                          "Content",
                          "Render Spec",
                          "Template"
                        ]
                      },
                      {
                        "name": "Inject transformers",
                        "collaborators": [
                          "Behavior",
                          "Content",
                          "Transformer"
                        ]
                      },
                      {
                        "name": "Load + inject structured content",
                        "collaborators": [
                          "Behavior",
                          "Content",
                          "Knowledge Graph"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "TTYRenderOutput",
                    "responsibilities": [
                      {
                        "name": "Serialize render action to TTY",
                        "collaborators": [
                          "RenderOutputAction",
                          "TTY String"
                        ]
                      },
                      {
                        "name": "Format render status",
                        "collaborators": [
                          "Render Spec",
                          "TTY String"
                        ]
                      },
                      {
                        "name": "Wraps domain action",
                        "collaborators": [
                          "RenderOutputAction"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "inherits_from": "TTYProgressAdapter",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "JSONRenderOutput",
                    "responsibilities": [
                      {
                        "name": "Serialize render action to JSON",
                        "collaborators": [
                          "RenderOutputAction",
                          "JSON String"
                        ]
                      },
                      {
                        "name": "Include render spec",
                        "collaborators": [
                          "Render Spec",
                          "Templates",
                          "JSON"
                        ]
                      },
                      {
                        "name": "Wraps domain action",
                        "collaborators": [
                          "RenderOutputAction"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "inherits_from": "JSONProgressAdapter",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "MarkdownRenderOutput",
                    "responsibilities": [
                      {
                        "name": "Serialize render action to Markdown",
                        "collaborators": [
                          "RenderOutputAction",
                          "Markdown String"
                        ]
                      },
                      {
                        "name": "Format render documentation",
                        "collaborators": [
                          "Render Spec",
                          "Templates",
                          "Markdown"
                        ]
                      },
                      {
                        "name": "Wraps domain action",
                        "collaborators": [
                          "RenderOutputAction"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "inherits_from": "MarkdownProgressAdapter",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "Renderer",
                    "responsibilities": [
                      {
                        "name": "Render complex output",
                        "collaborators": [
                          "Template",
                          "Knowledge Graph",
                          "Transformer"
                        ]
                      },
                      {
                        "name": "Render outputs using components in context",
                        "collaborators": [
                          "AI Chat",
                          "Template",
                          "Content"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "Template",
                    "responsibilities": [
                      {
                        "name": "Define output structure",
                        "collaborators": [
                          "Placeholder"
                        ]
                      },
                      {
                        "name": "Transform content",
                        "collaborators": [
                          "Transformer",
                          "Content"
                        ]
                      },
                      {
                        "name": "Load template",
                        "collaborators": [
                          "Behavior",
                          "Content"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "Content",
                    "responsibilities": [
                      {
                        "name": "Render outputs",
                        "collaborators": [
                          "Template",
                          "Renderer",
                          "Render Spec"
                        ]
                      },
                      {
                        "name": "Synchronize formats",
                        "collaborators": [
                          "Synchronizer",
                          "Extractor",
                          "Synchronizer Spec"
                        ]
                      },
                      {
                        "name": "Save knowledge graph",
                        "collaborators": [
                          "Knowledge Graph"
                        ]
                      },
                      {
                        "name": "Load rendered content",
                        "collaborators": [
                          "na"
                        ]
                      },
                      {
                        "name": "Present rendered content",
                        "collaborators": [
                          "na"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "RenderInstructionsSection",
                    "responsibilities": [
                      {
                        "name": "Wraps render subsection",
                        "collaborators": [
                          "RenderDataSubSection"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "inherits_from": "InstructionsSection",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  },
                  {
                    "name": "RenderDataSubSection",
                    "responsibilities": [
                      {
                        "name": "Wraps render JSON",
                        "collaborators": [
                          "Render JSON"
                        ]
                      },
                      {
                        "name": "Displays render spec",
                        "collaborators": [
                          "Object",
                          "RenderSpec JSON"
                        ]
                      },
                      {
                        "name": "Displays templates",
                        "collaborators": [
                          "List",
                          "Template JSON"
                        ]
                      },
                      {
                        "name": "Displays render instructions",
                        "collaborators": [
                          "String",
                          "RenderInstructions JSON"
                        ]
                      },
                      {
                        "name": "Opens template file",
                        "collaborators": [
                          "CLI",
                          "Path JSON"
                        ]
                      }
                    ],
                    "module": "actions.render",
                    "inherits_from": "SubSectionView",
                    "_source_path": "Invoke Bot.Invoke Bot Directly"
                  }
                ]
              }
            ],
            "story_groups": []
          }
        ],
        "domain_concepts": []
      }
    ],
    "increments": []
  }
}

---

# Behavior: scenarios

## Behavior Instructions - scenarios

The purpose of this behavior is to write detailed plain-english scenarios (given/when/then) that specify exact behavior for each story

Write detailed plain-English scenarios (Given/When/Then) that specify exact behavior for each story

## Action Instructions - validate

The purpose of this action is to validate story graph and/or artifacts against behavior-specific rules, checking for violations and compliance

specification_scenarios: validate scenario structure and domain language usage
Validate that scenarios use proper domain terminology and reference domain concepts correctly

---

**Look for context in the following locations:**
- in this message and chat history
- `C:/dev/agile_bots/docs/story/story-graph.json` - the story graph and related  knowledge built so far
- `C:/dev/agile_bots/docs/story/strategy.json` - strategy decisions made
- `C:/dev/agile_bots/docs/story/clarification.json` - clarification answers
- `C:/dev/agile_bots/test/` and `C:/dev/agile_bots/src/` - existing code and tests
- any folder named `context/` anywhere in `C:/dev/agile_bots/` - additional context files

IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

## Step 1: Run Scanners Then Review Violations

**Scanners you must run (with params below). Do not assume pre-run results.**

| Rule | Rule file | Scanner module |
|------|-----------|----------------|
| Scenario Language Matches Domain | `story_bot/behaviors/scenarios/rules/scenario_language_matches_domain.json` | `scanners.scenarios.scenario_language_scanner.ScenarioLanguageScanner` |
| Example Tables Use Domain Language | `story_bot/behaviors/scenarios/rules/example_tables_use_domain_language.json` | `scanners.scenarios.example_table_scanner.ExampleTableScanner` |
| Given Describes State Not Actions | `story_bot/behaviors/scenarios/rules/given_describes_state_not_actions.json` | `scanners.scenarios.given_state_not_actions_scanner.GivenStateNotActionsScanner` |
| Background Vs Scenario Setup | `story_bot/behaviors/scenarios/rules/background_vs_scenario_setup.json` | `scanners.scenarios.background_common_setup_scanner.BackgroundCommonSetupScanner` |
| Scenarios Cover All Cases | `story_bot/behaviors/scenarios/rules/scenarios_cover_all_cases.json` | `scanners.scenarios.scenarios_cover_all_cases_scanner.ScenariosCoverAllCasesScanner` |
| Use Scenario Outline When Needed | `story_bot/behaviors/scenarios/rules/use_scenario_outline_when_needed.json` | `scanners.scenarios.scenario_outline_scanner.ScenarioOutlineScanner` |
| Write Concrete Scenarios | `story_bot/behaviors/scenarios/rules/write_concrete_scenarios.json` | `scanners.scenarios.parameterized_scenarios_scanner.ParameterizedScenariosScanner` |
| Scenarios On Story Docs | `story_bot/behaviors/scenarios/rules/scenarios_on_story_docs.json` | `scanners.scenarios.scenarios_on_story_docs_scanner.ScenariosOnStoryDocsScanner` |
| Map Table Columns To Scenario Parameters | `story_bot/behaviors/scenarios/rules/map_table_columns_to_scenario_parameters.json` | `scanners.table_column_parameter_scanner.TableColumnParameterScanner` |

**Params to pass when running scanners:**
- **Scope:** story/stories: "Render Diagram In Workspace"
- **Workspace:** `C:\dev\agile_bots`
- **Story graph path:** `docs/story/story-graph.json` (or behavior-specific path)

Run each scanner with the above scope and workspace; then report violations and fix the story graph as needed.

Run each scanner with the params above, then review the violations they report as follows:
1. For each violation message, locate the corresponding element in the story graph.
2. Open the relevant rule file and read all DO and DON'T examples thoroughly.
3. Decide if the violation is **Valid** (truly a rule breach per examples) or a **False Positive** (explain why if so).
4. Determine the **Root Cause** (e.g., 'incorrect concept naming', 'missing actor', etc.).
5. Assign a **Theme** grouping based on the type of issue (e.g., 'noun-only naming', 'incomplete acceptance criteria').
6. Extract an **Example** from the actual code/content showing the problem.
7. Suggest a clear, concrete **Fix** with a code example informed by DO examples in the rule.

## Step 2: Manual Rule Review

**Rules to validate against (read each file for full DO/DON'T examples):**

### Rule: Scenario Language Matches Domain (Priority 1) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/scenario_language_matches_domain.json`
**Description:** Scenario language MUST use domain concept terminology. Given/When/Then steps should reference domain entities and concepts, not UI elements or technical implementation details.
**DO:** Use domain language in scenario steps - reference domain concepts by name.
**DON'T:** Don't use UI element names, technical implementation terms, or generic words instead of domain concepts.

### Rule: Example Tables Use Domain Language (Priority 2) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/example_tables_use_domain_language.json`
**Description:** Example tables MUST be grounded in scenario steps AND use domain-rich language. Table columns = nouns from Given/When/Then steps. Use domain terminology, not UI elements. Omit ID columns used purely for linking tables - relationships are expressed via collaboration field and table ordering. Concrete values with domain context, not generic JSON or placeholders. Use source entity data, not aggregated/calculated values - this is the stage where you figure out the real examples.
**DO:** Ground tables in scenario nouns, use domain terminology, connect tables using domain responsibility sentences. Omit implementation IDs. Show source entities, not derived counts.
**DON'T:** Don't use UI elements, flat lookup tables, generic JSON, abstract descriptions, invented terminology, or aggregated/calculated values.

### Rule: Given Describes State Not Actions (Priority 3) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/given_describes_state_not_actions.json`
**Description:** Given statements describe STATE/PRECONDITIONS, not actions or functionality. Given = what exists before test. When = first action. Then = expected behavior. Example: Given user is logged in (state), not Given user logs in (action).
**DO:** Given describes state/preconditions only. Example: 'Given user is logged in' (state), 'Given character sheet exists' (precondition)
**DON'T:** Don't describe actions, UI navigation, or functionality in Given. Example: 'Given user logs in' (action - wrong), 'Given User is on PaymentDetails step' (navigation - wrong)

### Rule: Background Vs Scenario Setup (Priority 4) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/background_vs_scenario_setup.json`
**Description:** Background = shared setup for 3+ scenarios (Given/And only, no When/Then). Background steps MUST use {Concept} notation to reference domain objects. Use {Concept.property} when a specific attribute is important. Don't repeat Background in Steps.
**DO:** Use Background for shared context with {Concept} references to example tables.
**DON'T:** Don't use hardcoded values or column names in Background - use {Concept} notation. Don't include When/Then.

### Rule: Scenarios Cover All Cases (Priority 5) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/scenarios_cover_all_cases.json`
**Description:** Scenarios must cover happy path, edge cases, and error cases based on acceptance criteria. Example: Valid input → success; Boundary value → validates; Invalid input → error message.
**DO:** Cover all case types: happy path, edge cases, error cases. Example: User enters valid data → success; User enters boundary → validates; User enters invalid → error
**DON'T:** Don't skip case types. Example: Only happy path scenarios (missing edge and error cases)

### Rule: Use Scenario Outline When Needed (Priority 6) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/use_scenario_outline_when_needed.json`
**Description:** Use Scenario Outline with Examples when story warrants concrete data: formulas need validation, domain has named entities, parameter variations exist. Example: Calculate ability modifier with Examples table Rank 10→0, Rank 12→+1, Rank 14→+2.
**DO:** Scenario Outline for formulas, domain entities, or data variations. Example: Scenario Outline: Calculate modifier with Examples table showing input→output pairs
**DON'T:** Don't use Scenario Outline for simple behaviors. Example: Scenario Outline: User clicks button (too simple - use regular scenario)

### Rule: Write Concrete Scenarios (Priority 7) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/write_concrete_scenarios.json`
**Description:** Parameterize domain concepts in scenarios using {Concept} notation for objects and {Concept.property} for specific attributes. Every {parameter} in Background/Steps MUST have corresponding example table. Use object references, not column names directly.
**DO:** Use {Concept} for object references, {Concept.property} for specific attributes. Connect to example tables.
**DON'T:** Don't hardcode values without examples, don't use non-domain placeholders, don't skip base data dependencies.

### Rule: Scenarios On Story Docs (Priority 8) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/scenarios_on_story_docs.json`
**Description:** Scenarios must be in story-graph.json (in scenarios or scenario_outlines fields), NOT in separate markdown files. NEVER create feature specification documents. Example: story-graph.json epics[].stories[].scenarios[], not docs/story/scenarios.md.
**DO:** Add scenarios to story-graph.json. Example: story-graph.json epics[].stories[].scenarios[] array
**DON'T:** Dont create separate scenario files or feature specifications. Example: docs/story/Epic/Feature/Feature Specification.md (wrong)

### Rule: Map Table Columns To Scenario Parameters (Priority 9) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/map_table_columns_to_scenario_parameters.json`
**Description:** Map example tables to {Concept} references bidirectionally. Every example table maps to a {Concept} in Background/Steps. Use {Concept} for object references and {Concept.property} for specific attributes. Keep tables minimal and domain-focused.
**DO:** Bidirectional mapping: Example table name ↔ {Concept} reference in steps.
**DON'T:** Don't use <column_name> notation - use {Concept} or {Concept.property}. Don't have orphaned tables or references.


Scanner tools don't cover or catch every rule violation. Do a second pass:
1. Carefully read each rule file, fully reviewing DO and DON'T sections, and every provided example.
2. Inspect story/stories: "Render Diagram In Workspace" for compliance.
3. Compare the properties and content of each element against the rule's requirements.
4. Document any violations the scanner could not find.
5. For each violation, extract an **Example** showing the problem and provide a **Fix** with code example.

## Violations Found

Record ALL findings (scanner + manual) using this readable format. Group by theme for narrow IDE chat panels:

### [Theme Name] (X violations)

**1. [Rule Name]**
- Location: `path.to.element`
- Status: Valid / False Positive
- Source: Scanner / Manual / Both
- Problem: `"actual problematic text"`
- Fix: `"corrected text"`
- Root Cause: Brief explanation

**2. [Rule Name]**
- Location: `path.to.element`
- ...

---

### [Next Theme] (Y violations)
...

Use this list format instead of tables - tables are unreadable in narrow IDE side chat panels.

## Step 3: Summarize Findings & Recommendations

Provide a concise summary:
- Report how many **scanner violations** were valid vs false positives.
- Enumerate any **additional manual findings** not caught by scanners.
- Group all violations by recurring theme or pattern.
- Split violations into **Priority Fixes** (must resolve before continuing) and **Optional Improvements**.

Present your summary and await user confirmation before automatically applying or proposing corrections.
specification_scenarios: validate scenario structure and domain language usage
Validate that scenarios use proper domain terminology and reference domain concepts correctly

### Key Questions

- What system and user actions initiate this story's flow?
- What is the intended system response after each user action?
- What preconditions or data states are required before this story can begin?
- What are the success criteria for the story (from a domain and user perspective)?
- What are the expected alternate flows, error paths, and edge cases?
- Are there any mandatory sequencing constraints within or across stories?
- What domain rules, calculations, or business policies does this story validate?
- Is the story testable independently (including setup and teardown conditions)?
- What external systems or services does this story need to interact with?
- What requests, responses, or contracts are involved in those system interactions?
- Are there system integration points that require validation or simulation?
- How do we handle failures, timeouts, or retries for those system calls?
- What data variations (e.g., boundary conditions, common examples) are required for test coverage?
- What are the input values needed to test each scenario?
- What are the expected output values for each input?
- Are there formulas or calculations that need multiple data points to validate?
- Are there domain entities with named values that should be tested?
- What are the boundary conditions (min, max, edge cases) for each data point?

### Evidence

Acceptance criteria from Exploration stage (Domain AC at feature level, Behavioral AC at story level), High fidelity UX flows, Cross-functional walkthrough outputs, Integration contracts or API mocks, Behavior diagrams (state, sequence)

### Decisions

**Your Decisions:**

**examples_representation:**
  Verification Data Table

**scenario_outline:**
  Scenario Outline with Examples

**scenario_coverage:**
  - Happy Path
  - Edge Cases


### Assumptions

**Your Assumptions:**

- One story is specified at a time
- Acceptance criteria must be testable, unambiguous, and executable
- Gherkin syntax or structured language (Given/When/Then) is preferred
- Scenarios are written in plain English. When using Scenario Outline, variables are clearly marked and defined in Examples tables with actual test data.
- Examples tables when used must include ALL variables used in scenario steps
- Examples tables when used must have exact values for both input AND output variables
- Every variable when used in scenario steps must have a corresponding column in Examples table
- Examples tables when used must have actual test data, not placeholders
- Output/expected result variables must be included in Examples tables when used
- scnarios follow this pattern
- bulk of business logic tests done against the domain layer objects directly
- minimal happy path testing done with separate tgests that go theoiugh CLI
- JS nodetest for panel test focus on rendering and button layout

---
## Next action: render
**Next:** Perform the following action.

## Action Instructions - render

The purpose of this action is to render output documents and artifacts from story graph using templates and synchronizers

specification_scenarios: render story documents with scenarios

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

Please follow the instructions below in order to manually render output documents using templates

All render configurations are automatically loaded and injected below. Process ALL configs - do not skip any.



**Final Steps:**
- Process ALL configs above - do not skip any
- Priority order: synchronizer > template
- Verify each output file exists after execution
- If execution fails, report the error and continue with other outputs
- After completing all renders, pause and wait for human confirmation before proceeding to next behavior

**Creating New Render Outputs:**
If you need to create code to render a new output format:
1. Create a new synchronizer file in {workspace}/synchronizers/ (create folder if it doesn't exist)
2. Follow this signature pattern: output_file = synchronizer.render(story_graph_file)
3. The synchronizer should read the story-graph.json and produce the desired output file
4. Add the new synchronizer to the behavior's render config to include it in future renders
specification_scenarios: render story documents with scenarios
IMPORTANT: After completing all template-based rendering, you MUST execute the synchronizer-based render specs by running: scenarios.render.renderAll
This will render the following outputs: render_story_scenarios"""
Test Submit Scoped Action

SubEpic: Submit Scoped Action
Parent Epic: Invoke Bot > Edit Story Map

Domain tests verify core scope management logic.
CLI tests verify command parsing and output formatting across TTY, Pipe, and JSON channels.
"""
import pytest
from pathlib import Path
import json
import os
from helpers.bot_test_helper import BotTestHelper
from helpers import TTYBotTestHelper, PipeBotTestHelper, JsonBotTestHelper
from story_graph.nodes import Scenario

# ============================================================================
# DOMAIN TESTS - Core Scope Logic
# ============================================================================

class TestSetScopeToSelectedStoryNodeAndSubmit:
    """
    Story: Set scope to selected story node and submit
    
    Tests the bot's ability to determine what behavior is needed for a story
    based on its completeness state (acceptance criteria, scenarios, tests).
    """
    
    @pytest.mark.parametrize("epic_name,story_name,test_class,acceptance_criteria,scenarios,test_methods,expected_behavior,action,expected_instructions_contain", [
        # All scenarios have tests -> code behavior
        (
            "File Management",
            "Upload File",
            "test_file_upload.py",
            "File size validated; File type checked; Upload progress tracked",
            [
                "User uploads valid file and sees success confirmation",
                "User uploads oversized file and sees size limit error",
                "User uploads invalid file type and sees type error",
                "User cancels upload mid-transfer and sees cancellation confirmation",
                "Upload fails with network error and user sees retry option"
            ],
            [
                "test_user_uploads_valid_file_and_sees_success_confirmation",
                "test_user_uploads_oversized_file_and_sees_size_limit_error",
                "test_user_uploads_invalid_file_type_and_sees_type_error",
                "test_user_cancels_upload_mid_transfer_and_sees_cancellation_confirmation",
                "test_upload_fails_with_network_error_and_user_sees_retry_option"
            ],
            "code",
            "build",
            "code behavior; build action; upload file functionality"
        ),
        # Some scenarios tested -> test behavior
        (
            "File Management",
            "Download File",
            "test_file_download.py",
            "Download initiated; Progress displayed",
            [
                "User downloads file successfully and sees progress",
                "User cancels download mid-transfer",
                "Download fails due to network error and user sees error message"
            ],
            [
                "test_user_downloads_file_successfully_and_sees_progress",
                "test_user_cancels_download_mid_transfer",
                None  # Third scenario has no test
            ],
            "tests",
            "build",
            "tests behavior; build action; download file functionality"
        ),
        # Scenarios exist but no tests -> tests behavior
        (
            "File Management",
            "Delete File",
            "test_file_delete.py",
            "Confirmation required; File removed from storage",
            [
                "User confirms delete and file is removed from system",
                "User cancels delete and file remains",
                "Delete operation fails due to permissions and user sees error"
            ],
            [],
            "tests",
            "validate",
            "tests behavior; validate action; delete file functionality"
        ),
        # Has AC but no scenarios -> scenarios behavior
        (
            "User Management",
            "Create User",
            "",
            "Email validated; Password meets requirements",
            [],
            [],
            "scenarios",
            "build",
            "scenarios behavior; build action; create user functionality"
        ),
        # No AC and no scenarios -> exploration behavior
        (
            "Reporting",
            "View Report",
            "",
            "",
            [],
            [],
            "exploration",
            "clarify",
            "exploration behavior; clarify action; view report functionality"
        ),
        # No AC but scenarios all tested -> code behavior
        (
            "Authentication",
            "Reset Password",
            "test_reset_password.py",
            "",  # No AC
            [
                "User requests password reset and receives reset email",
                "User submits new password meeting requirements and password is updated",
                "User submits invalid password not meeting requirements and sees validation error"
            ],
            [
                "test_user_requests_password_reset_and_receives_reset_email",
                "test_user_submits_new_password_meeting_requirements_and_password_is_updated",
                "test_user_submits_invalid_password_not_meeting_requirements_and_sees_validation_error"
            ],
            "code",
            "validate",
            "code behavior; validate action; reset password functionality"
        ),
        # No AC but some scenarios tested -> tests behavior
        (
            "Data Export",
            "Export CSV",
            "test_export_csv.py",
            "",
            [
                "User exports data to CSV and file downloads successfully",
                "Export handles empty data set and generates valid empty CSV",
                "Export handles large dataset and shows progress indicator",
                "Export with special characters in data and properly escapes them in CSV"
            ],
            [
                "test_user_exports_data_to_csv_and_file_downloads_successfully",
                "test_export_handles_empty_data_set_and_generates_valid_empty_csv",
                None,
                None
            ],
            "tests",
            "clarify",
            "tests behavior; clarify action; export csv functionality"
        ),
        # No AC but scenarios without tests -> tests behavior
        (
            "Payment",
            "Process Payment",
            "test_process_payment.py",
            "",
            [
                "Payment processed with valid card and transaction completes successfully",
                "Payment attempted with expired card and user sees card expired error"
            ],
            [],
            "tests",
            "build",
            "tests behavior; build action; payment processing test coverage; implement test methods"
        ),
    ])
    def test_determine_behavior_for_story_and_get_instructions(
        self,
        tmp_path,
        epic_name,
        story_name,
        test_class,
        acceptance_criteria,
        scenarios,
        test_methods,
        expected_behavior,
        action,
        expected_instructions_contain
    ):
        """
        SCENARIO: Determine Behavior For Story And Get Instructions
        GIVEN: Bot has story map loaded with epic <epic_name>
        AND: Epic contains story <story_name>
        AND: Story has acceptance criteria <acceptance_criteria>
        AND: Story has scenarios <scenarios>
        AND: Story has test class <test_class>
        AND: Story has test methods <test_methods>
        WHEN: Bot determines behavior for the story
        THEN: Bot returns behavior <expected_behavior>
        WHEN: User calls story.get_required_behavior_instructions with action <action>
        THEN: Bot is set to behavior <expected_behavior>
        AND: Bot is set to action <action>
        AND: Instructions for <expected_behavior> behavior and <action> action are returned
        AND: Instructions contain required sections for <expected_behavior> behavior
        
        This test validates the hierarchical logic:
        - If all scenarios have tests -> code behavior
        - If some/no scenarios tested -> test behavior
        - If no scenarios exist -> scenario behavior
        - If no acceptance criteria -> explore behavior
        - Lower level artifacts take precedence (tests > scenarios > AC)
        """
        # Given - Create a test story with the specified state
        helper = BotTestHelper(tmp_path)
        story = helper.story.create_story_with_state_for_behavior_test(
            epic_name,
            story_name,
            test_class,
            acceptance_criteria,
            scenarios,
            test_methods
        )
        
        # When - Bot determines behavior for the story
        actual_behavior = story.behavior_needed
        
        # Then - Bot returns expected behavior
        assert actual_behavior == expected_behavior, (
            f"Expected behavior '{expected_behavior}' but got '{actual_behavior}'"
        )
        
        # Capture scope before operation
        scope_before = helper.bot.scope()
        scope_type_before = scope_before.type.value
        scope_value_before = list(scope_before.value) if scope_before.value else []
        
        # When - User calls story.get_required_behavior_instructions (always uses build)
        instructions = story.get_required_behavior_instructions()
        
        # Then - Bot is set to behavior and action (always build)
        assert helper.bot.behaviors.current.name == expected_behavior
        assert helper.bot.behaviors.current.actions.current.action_name == 'build'
        
        # And - Scope is restored to what it was before
        scope_after = helper.bot.scope()
        assert scope_after.type.value == scope_type_before, f"Expected scope type '{scope_type_before}', got '{scope_after.type.value}'"
        assert list(scope_after.value) == scope_value_before, f"Expected scope value {scope_value_before}, got {list(scope_after.value)}"
        
        # And - Instructions object is returned
        from instructions.instructions import Instructions
        assert isinstance(instructions, Instructions), "Should return Instructions object"
        assert instructions.get('behavior_metadata') is not None, "Instructions should have behavior metadata"
        assert instructions.get('action_metadata') is not None, "Instructions should have action metadata"
        assert instructions.get('behavior_metadata')['name'] == expected_behavior
        assert instructions.get('action_metadata')['name'] == 'build'
        
        # And - Instructions contain the scope that was set during execution
        assert instructions.scope is not None, "Instructions should contain scope"
        assert instructions.scope.type.value == 'story', f"Expected scope type 'story' in instructions, got '{instructions.scope.type.value}'"
        assert story.name in instructions.scope.value, f"Expected story '{story.name}' in instructions scope value {instructions.scope.value}"

    @pytest.mark.parametrize("sub_epic_name,stories_data,expected_behavior,action,expected_instructions_contain", [
        # Example 1: All stories have tests -> code behavior
        (
            "User Authentication",
            [
                {
                    "story_name": "Login User",
                    "test_class": "test_login_user.py",
                    "acceptance_criteria": "Valid credentials accepted; Invalid credentials rejected; Account locked after 3 failures",
                    "scenarios": [
                        "User enters valid username and password and sees dashboard",
                        "User enters invalid password and sees error message",
                        "User fails login 3 times and account is locked"
                    ],
                    "test_methods": [
                        "test_user_enters_valid_username_and_password_and_sees_dashboard",
                        "test_user_enters_invalid_password_and_sees_error_message",
                        "test_user_fails_login_3_times_and_account_is_locked"
                    ]
                },
                {
                    "story_name": "Logout User",
                    "test_class": "test_logout_user.py",
                    "acceptance_criteria": "Session terminated on logout; User redirected to login page; Auth token invalidated",
                    "scenarios": [
                        "User clicks logout button and session ends",
                        "User clicks logout and is redirected to login",
                        "Logged out user cannot access protected pages"
                    ],
                    "test_methods": [
                        "test_user_clicks_logout_button_and_session_ends",
                        "test_user_clicks_logout_and_is_redirected_to_login",
                        "test_logged_out_user_cannot_access_protected_pages"
                    ]
                },
                {
                    "story_name": "Refresh Token",
                    "test_class": "test_refresh_token.py",
                    "acceptance_criteria": "Token refreshed before expiry; Expired token triggers re-login; Refresh token rotated after use",
                    "scenarios": [
                        "User with expiring token gets new token automatically",
                        "User with expired token is prompted to login",
                        "Used refresh token becomes invalid"
                    ],
                    "test_methods": [
                        "test_user_with_expiring_token_gets_new_token_automatically",
                        "test_user_with_expired_token_is_prompted_to_login",
                        "test_used_refresh_token_becomes_invalid"
                    ]
                }
            ],
            "code",
            "build",
            "code behavior; build action; authentication functionality; implement production code for feature"
        ),
        # Example 2: One story needs scenarios, sub-epic follows lowest -> scenarios behavior
        (
            "Payment Processing",
            [
                {
                    "story_name": "Process Payment",
                    "test_class": "test_process_payment.py",
                    "acceptance_criteria": "Card details validated; Payment amount verified; Transaction receipt generated",
                    "scenarios": [
                        "User enters valid card and payment succeeds",
                        "User enters invalid card number and sees validation error",
                        "Payment succeeds and receipt is emailed to user"
                    ],
                    "test_methods": []
                },
                {
                    "story_name": "Refund Payment",
                    "test_class": "",
                    "acceptance_criteria": "Original payment verified; Refund amount calculated; Customer notified of refund",
                    "scenarios": [],
                    "test_methods": []
                }
            ],
            "scenarios",
            "validate",
            "scenarios behavior; validate action; payment processing domain language; verify scenarios are complete"
        ),
        # Example 3: One story at exploration level makes entire sub-epic exploration -> exploration behavior
        (
            "Data Management",
            [
                {
                    "story_name": "Import Data",
                    "test_class": "test_import_data.py",
                    "acceptance_criteria": "CSV file format validated; Data schema verified; Import progress tracked",
                    "scenarios": [
                        "User uploads valid CSV and data is imported",
                        "User uploads invalid CSV and sees format error",
                        "User sees progress bar during import"
                    ],
                    "test_methods": []
                },
                {
                    "story_name": "Export Data",
                    "test_class": "",
                    "acceptance_criteria": "Export format selected; Data filtered before export; Download link generated",
                    "scenarios": [],
                    "test_methods": []
                },
                {
                    "story_name": "Validate Data",
                    "test_class": "",
                    "acceptance_criteria": "Data types checked; Required fields verified; Business rules applied",
                    "scenarios": [],
                    "test_methods": []
                },
                {
                    "story_name": "Archive Data",
                    "test_class": "",
                    "acceptance_criteria": "",
                    "scenarios": [],
                    "test_methods": []
                }
            ],
            "exploration",
            "build",
            "exploration behavior; build action; data management domain concepts; add stories with acceptance criteria"
        ),
        # Example 4: Two stories need tests, sub-epic follows lowest -> tests behavior
        (
            "File Operations",
            [
                {
                    "story_name": "Upload File",
                    "test_class": "test_file_upload.py",
                    "acceptance_criteria": "File size validated; File type checked; Upload progress tracked",
                    "scenarios": [
                        "User uploads valid file and sees success confirmation",
                        "User uploads oversized file and sees size limit error",
                        "User uploads invalid file type and sees type error",
                        "User cancels upload mid-transfer and sees cancellation confirmation",
                        "Upload fails with network error and user sees retry option"
                    ],
                    "test_methods": [
                        "test_user_uploads_valid_file_and_sees_success_confirmation",
                        "test_user_uploads_oversized_file_and_sees_size_limit_error",
                        "test_user_uploads_invalid_file_type_and_sees_type_error",
                        "test_user_cancels_upload_mid_transfer_and_sees_cancellation_confirmation",
                        "test_upload_fails_with_network_error_and_user_sees_retry_option"
                    ]
                },
                {
                    "story_name": "Download File",
                    "test_class": "test_file_download.py",
                    "acceptance_criteria": "Download initiated; Progress displayed",
                    "scenarios": [
                        "User clicks download and file transfer starts",
                        "User sees download progress bar",
                        "Download completes and file appears in downloads folder"
                    ],
                    "test_methods": []
                },
                {
                    "story_name": "Delete File",
                    "test_class": "test_file_delete.py",
                    "acceptance_criteria": "Confirmation required; File removed from storage",
                    "scenarios": [
                        "User clicks delete and sees confirmation dialog",
                        "User confirms deletion and file is removed",
                        "User sees success message after deletion"
                    ],
                    "test_methods": []
                }
            ],
            "tests",
            "clarify",
            "tests behavior; clarify action; file operations test requirements; clarify test coverage expectations"
        ),
        # Example 5: Single story at scenarios level -> scenarios behavior
        (
            "Search",
            [
                {
                    "story_name": "Basic Search",
                    "test_class": "",
                    "acceptance_criteria": "Search term entered; Results displayed; No results message shown when empty",
                    "scenarios": [],
                    "test_methods": []
                }
            ],
            "scenarios",
            "build",
            "scenarios behavior; build action; search domain language; write detailed scenarios"
        ),
    ])
    def test_determine_behavior_for_sub_epic_and_get_instructions(self, tmp_path, sub_epic_name, stories_data, expected_behavior, action, expected_instructions_contain):
        """
        SCENARIO: Determine Behavior For Sub Epic And Get Instructions
        GIVEN: Bot has story map loaded with sub-epic <sub_epic_name>
        AND: Sub-epic contains stories shown in table
        WHEN: Bot determines behavior for the sub-epic
        THEN: Bot returns behavior <expected_behavior>
        WHEN: User calls sub_epic.get_required_behavior_instructions with action <action>
        THEN: Bot is set to behavior <expected_behavior>
        AND: Bot is set to action <action>
        AND: Instructions for <expected_behavior> behavior and <action> action are returned
        AND: Instructions contain required sections for <expected_behavior> behavior
        
        This test validates the hierarchical degradation logic:
        - Sub-epic checks first story for its behavior
        - For each subsequent story, checks at degraded level
        - Returns the lowest behavior needed across all stories
        """
        # Given - Create a test sub-epic with multiple stories
        helper = BotTestHelper(tmp_path)
        sub_epic = helper.story.create_sub_epic_with_stories_for_behavior_test(sub_epic_name, stories_data)
        
        # When - Bot determines behavior for the sub-epic
        actual_behavior = sub_epic.behavior_needed
        
        # Then - Bot returns expected behavior
        assert actual_behavior == expected_behavior, (
            f"Expected behavior '{expected_behavior}' but got '{actual_behavior}' "
            f"for sub-epic '{sub_epic_name}' with {len(stories_data)} stories"
        )
        
        # Capture scope before operation
        scope_before = helper.bot.scope()
        scope_type_before = scope_before.type.value
        scope_value_before = list(scope_before.value) if scope_before.value else []
        
        # When - User calls sub_epic.get_required_behavior_instructions (always uses build)
        instructions = sub_epic.get_required_behavior_instructions()
        
        # Then - Bot is set to behavior and action (always build)
        assert helper.bot.behaviors.current.name == expected_behavior
        assert helper.bot.behaviors.current.actions.current.action_name == 'build'
        
        # And - Scope is restored to what it was before
        scope_after = helper.bot.scope()
        assert scope_after.type.value == scope_type_before, f"Expected scope type '{scope_type_before}', got '{scope_after.type.value}'"
        assert list(scope_after.value) == scope_value_before, f"Expected scope value {scope_value_before}, got {list(scope_after.value)}"
        
        # And - Instructions object is returned
        from instructions.instructions import Instructions
        assert isinstance(instructions, Instructions), "Should return Instructions object"
        assert instructions.get('behavior_metadata') is not None, "Instructions should have behavior metadata"
        assert instructions.get('action_metadata') is not None, "Instructions should have action metadata"
        assert instructions.get('behavior_metadata')['name'] == expected_behavior
        assert instructions.get('action_metadata')['name'] == 'build'

    @pytest.mark.parametrize("scenario_name,test_method,expected_behavior", [
        # Scenario with test method -> code behavior
        (
            "User uploads valid file and sees success confirmation",
            "test_user_uploads_valid_file_and_sees_success_confirmation",
            "code"
        ),
        # Scenario without test method -> tests behavior
        (
            "User downloads file successfully and sees progress",
            None,
            "tests"
        ),
        # Scenario with empty test method -> tests behavior
        (
            "User deletes file and sees confirmation",
            None,
            "tests"
        ),
    ])
    def test_determine_behavior_for_scenario(
        self,
        scenario_name,
        test_method,
        expected_behavior
    ):
        """
        SCENARIO: Determine Behavior For Scenario
        GIVEN: Scenario <scenario_name> with test method <test_method>
        WHEN: Bot determines behavior for the scenario
        THEN: Bot returns behavior <expected_behavior>
        
        This test validates the scenario-level logic:
        - If scenario has test_method -> code behavior
        - If scenario has no test_method -> test behavior
        """
        # Given - Create a scenario with the specified state
        scenario = Scenario(
            name=scenario_name,
            sequential_order=1.0,
            type="happy_path",
            background=[],
            test_method=test_method,
            _parent=None
        )
        
        # When - Bot determines behavior for the scenario
        actual_behavior = scenario.behavior_needed
        
        # Then - Bot returns expected behavior
        assert actual_behavior == expected_behavior, (
            f"Expected behavior '{expected_behavior}' but got '{actual_behavior}'"
        )

    @pytest.mark.parametrize("epic_name,sub_epics_data,expected_behavior,action,expected_instructions_contain", [
        # Example 1: All sub-epics have code behavior -> code behavior
        (
            "File Management",
            [
                {
                    "name": "File Operations",
                    "nested_sub_epics": [],
                    "stories": [
                        {
                            "story_name": "Upload File",
                            "test_class": "test_file_upload.py",
                            "acceptance_criteria": "File size validated; File type checked; Upload progress tracked",
                            "scenarios": [
                                "User uploads valid file and sees success confirmation",
                                "User uploads oversized file and sees size limit error",
                                "User uploads invalid file type and sees type error"
                            ],
                            "test_methods": [
                                "test_user_uploads_valid_file_and_sees_success_confirmation",
                                "test_user_uploads_oversized_file_and_sees_size_limit_error",
                                "test_user_uploads_invalid_file_type_and_sees_type_error"
                            ]
                        },
                        {
                            "story_name": "Download File",
                            "test_class": "test_file_download.py",
                            "acceptance_criteria": "Download initiated; Progress displayed",
                            "scenarios": [
                                "User downloads file successfully and sees progress",
                                "User cancels download mid-transfer",
                                "Download fails due to network error and user sees error message"
                            ],
                            "test_methods": [
                                "test_user_downloads_file_successfully_and_sees_progress",
                                "test_user_cancels_download_mid_transfer",
                                "test_download_fails_due_to_network_error_and_user_sees_error_message"
                            ]
                        }
                    ]
                },
                {
                    "name": "File Search",
                    "nested_sub_epics": [],
                    "stories": [
                        {
                            "story_name": "Search by Name",
                            "test_class": "test_search_by_name.py",
                            "acceptance_criteria": "Search term validated; Results sorted by relevance; Partial matches included",
                            "scenarios": [
                                "User searches for file name and sees matching results",
                                "User searches with partial name and sees partial matches",
                                "User searches nonexistent file and sees no results message"
                            ],
                            "test_methods": [
                                "test_user_searches_for_file_name_and_sees_matching_results",
                                "test_user_searches_with_partial_name_and_sees_partial_matches",
                                "test_user_searches_nonexistent_file_and_sees_no_results_message"
                            ]
                        }
                    ]
                }
            ],
            "code",
            "validate",
            "code behavior; validate action; file management functionality; verify implementation is complete"
        ),
        # Example 2: One sub-epic at exploration level -> exploration behavior (highest wins)
        (
            "Reporting",
            [
                {
                    "name": "Report Generation",
                    "nested_sub_epics": [],
                    "stories": [
                        {
                            "story_name": "Generate Sales Report",
                            "test_class": "test_generate_sales_report.py",
                            "acceptance_criteria": "Date range validated; Data aggregated; Report formatted",
                            "scenarios": [
                                "User generates report for valid date range and sees report",
                                "User generates report with invalid date range and sees error"
                            ],
                            "test_methods": []
                        }
                    ]
                },
                {
                    "name": "Report Scheduling",
                    "nested_sub_epics": [],
                    "stories": [
                        {
                            "story_name": "Schedule Report",
                            "test_class": None,
                            "acceptance_criteria": "Schedule time validated; Recipients specified; Report sent at scheduled time",
                            "scenarios": [],
                            "test_methods": []
                        }
                    ]
                },
                {
                    "name": "Report Export",
                    "nested_sub_epics": [],
                    "stories": [
                        {
                            "story_name": "Export to PDF",
                            "test_class": None,
                            "acceptance_criteria": "",
                            "scenarios": [],
                            "test_methods": []
                        }
                    ]
                }
            ],
            "exploration",
            "clarify",
            "exploration behavior; clarify action; reporting domain concepts; clarify feature requirements"
        ),
        # Example 3: One sub-epic at scenarios level with others at code -> scenarios behavior
        (
            "User Management",
            [
                {
                    "name": "Authentication",
                    "nested_sub_epics": [],
                    "stories": [
                        {
                            "story_name": "Login User",
                            "test_class": "test_login_user.py",
                            "acceptance_criteria": "Valid credentials accepted; Invalid credentials rejected; Account locked after 3 failures",
                            "scenarios": [
                                "User enters valid username and password and sees dashboard",
                                "User enters invalid password and sees error message",
                                "User fails login 3 times and account is locked"
                            ],
                            "test_methods": [
                                "test_user_enters_valid_username_and_password_and_sees_dashboard",
                                "test_user_enters_invalid_password_and_sees_error_message",
                                "test_user_fails_login_3_times_and_account_is_locked"
                            ]
                        }
                    ]
                },
                {
                    "name": "User Profile",
                    "nested_sub_epics": [],
                    "stories": [
                        {
                            "story_name": "Update Profile",
                            "test_class": None,
                            "acceptance_criteria": "Profile fields validated; Changes saved to database; Confirmation displayed",
                            "scenarios": [],
                            "test_methods": []
                        }
                    ]
                }
            ],
            "scenarios",
            "build",
            "scenarios behavior; build action; user management domain language; write detailed scenarios"
        ),
        # Example 4: Multiple sub-epics at tests level -> tests behavior
        (
            "Payment Processing",
            [
                {
                    "name": "Process Payment",
                    "nested_sub_epics": [],
                    "stories": [
                        {
                            "story_name": "Validate Card",
                            "test_class": "test_validate_card.py",
                            "acceptance_criteria": "Card number validated; Expiry date checked; CVV verified",
                            "scenarios": [
                                "User enters valid card and validation passes",
                                "User enters invalid card number and sees error",
                                "User enters expired card and sees expiry error"
                            ],
                            "test_methods": []
                        }
                    ]
                },
                {
                    "name": "Refund Payment",
                    "nested_sub_epics": [],
                    "stories": [
                        {
                            "story_name": "Issue Refund",
                            "test_class": "test_issue_refund.py",
                            "acceptance_criteria": "Original payment verified; Refund amount calculated; Customer notified",
                            "scenarios": [
                                "Admin issues full refund and customer receives confirmation",
                                "Admin issues partial refund and amount is calculated correctly"
                            ],
                            "test_methods": []
                        }
                    ]
                }
            ],
            "tests",
            "build",
            "tests behavior; build action; payment processing test coverage; implement test methods"
        ),
        # Example 5: Empty epic with no sub-epics -> shape behavior
        (
            "Product Catalog",
            [],  # No sub-epics
            "shape",
            "build",
            "shape behavior; build action; product catalog domain concepts; add sub-epics and stories"
        ),
        # Example 6: Epic with nested sub-epics - parent sub-epic follows highest of nested children
        (
            "Product Management",
            [
                {
                    "name": "Product Catalog",
                    "nested_sub_epics": [
                        {
                            "name": "Category Management",
                            "nested_sub_epics": [],
                            "stories": [
                                {
                                    "story_name": "Create Category",
                                    "test_class": "test_create_category.py",
                                    "acceptance_criteria": "Category name validated; Parent category selected; Category saved",
                                    "scenarios": [
                                        "User creates new category with valid name",
                                        "User creates subcategory under parent category"
                                    ],
                                    "test_methods": [
                                        "test_user_creates_new_category_with_valid_name",
                                        "test_user_creates_subcategory_under_parent_category"
                                    ]
                                }
                            ]
                        },
                        {
                            "name": "Product Search",
                            "nested_sub_epics": [],
                            "stories": [
                                {
                                    "story_name": "Search Products",
                                    "test_class": None,
                                    "acceptance_criteria": "Search term entered; Filters applied; Results displayed",
                                    "scenarios": [],
                                    "test_methods": []
                                }
                            ]
                        }
                    ],
                    "stories": []
                },
                {
                    "name": "Inventory Management",
                    "nested_sub_epics": [],
                    "stories": [
                        {
                            "story_name": "Update Stock",
                            "test_class": "test_update_stock.py",
                            "acceptance_criteria": "Stock quantity validated; Inventory updated; Notification sent",
                            "scenarios": [
                                "Admin updates stock quantity and inventory reflects change"
                            ],
                            "test_methods": [
                                "test_admin_updates_stock_quantity_and_inventory_reflects_change"
                            ]
                        }
                    ]
                }
            ],
            "scenarios",
            "validate",
            "scenarios behavior; validate action; product management domain language; verify scenarios are complete"
        ),
        # Example 7: Parent sub-epic with nested sub-epics -> exploration behavior (highest of nested)
        (
            "Data Management Epic",
            [
                {
                    "name": "Data Management",
                    "nested_sub_epics": [
                        {
                            "name": "Data Import",
                            "nested_sub_epics": [],
                            "stories": [
                                {
                                    "story_name": "Import CSV",
                                    "test_class": "test_import_csv.py",
                                    "acceptance_criteria": "File format validated; Data parsed; Import completed",
                                    "scenarios": [
                                        "User imports valid CSV and data is loaded",
                                        "User imports invalid CSV and sees error"
                                    ],
                                    "test_methods": []
                                }
                            ]
                        },
                        {
                            "name": "Data Validation",
                            "nested_sub_epics": [],
                            "stories": [
                                {
                                    "story_name": "Validate Records",
                                    "test_class": None,
                                    "acceptance_criteria": "Data types checked; Required fields verified; Business rules applied",
                                    "scenarios": [],
                                    "test_methods": []
                                }
                            ]
                        },
                        {
                            "name": "Data Archive",
                            "nested_sub_epics": [],
                            "stories": [
                                {
                                    "story_name": "Archive Old Data",
                                    "test_class": None,
                                    "acceptance_criteria": "",
                                    "scenarios": [],
                                    "test_methods": []
                                }
                            ]
                        }
                    ],
                    "stories": []
                }
            ],
            "exploration",
            "clarify",
            "exploration behavior; clarify action; data management domain concepts; clarify feature requirements"
        ),
    ])
    def test_determine_behavior_for_epic_and_get_instructions(self, tmp_path, epic_name, sub_epics_data, expected_behavior, action, expected_instructions_contain):
        """
        SCENARIO: Determine Behavior For Epic And Get Instructions
        GIVEN: Bot has story map loaded with epic <epic_name>
        AND: Epic contains sub-epics shown in table
        WHEN: Bot determines behavior for the epic
        THEN: Bot returns behavior <expected_behavior>
        WHEN: User calls epic.get_required_behavior_instructions with action <action>
        THEN: Bot is set to behavior <expected_behavior>
        AND: Bot is set to action <action>
        AND: Instructions for <expected_behavior> behavior and <action> action are returned
        AND: Instructions contain required sections for <expected_behavior> behavior
        
        This test validates the hierarchical behavior determination:
        - Epic examines all sub-epics (including nested ones)
        - Returns the HIGHEST behavior found (shape > explore > scenario > test > code)
        - Can stop examining a sub-epic once a behavior at or above current highest is found
        """
        # Given - Create an epic with sub-epics (including nested if specified)
        helper = BotTestHelper(tmp_path)
        epic = helper.story.create_epic_with_sub_epics_for_behavior_test(epic_name, sub_epics_data)
        
        # When - Bot determines behavior for the epic
        actual_behavior = epic.behavior_needed
        
        # Then - Bot returns expected behavior (follows highest across all sub-epics)
        assert actual_behavior == expected_behavior, (
            f"Expected behavior '{expected_behavior}' but got '{actual_behavior}' "
            f"for epic '{epic_name}' with {len(sub_epics_data)} sub-epics"
        )
        
        # Capture scope before operation
        scope_before = helper.bot.scope()
        scope_type_before = scope_before.type.value
        scope_value_before = list(scope_before.value) if scope_before.value else []
        
        # When - User calls epic.get_required_behavior_instructions (always uses build)
        instructions = epic.get_required_behavior_instructions()
        
        # Then - Bot is set to behavior and action (always build)
        assert helper.bot.behaviors.current.name == expected_behavior
        assert helper.bot.behaviors.current.actions.current.action_name == 'build'
        
        # And - Scope is restored to what it was before
        scope_after = helper.bot.scope()
        assert scope_after.type.value == scope_type_before, f"Expected scope type '{scope_type_before}', got '{scope_after.type.value}'"
        assert list(scope_after.value) == scope_value_before, f"Expected scope value {scope_value_before}, got {list(scope_after.value)}"
        
        # And - Instructions object is returned
        from instructions.instructions import Instructions
        assert isinstance(instructions, Instructions), "Should return Instructions object"
        assert instructions.get('behavior_metadata') is not None, "Instructions should have behavior metadata"
        assert instructions.get('action_metadata') is not None, "Instructions should have action metadata"
        assert instructions.get('behavior_metadata')['name'] == expected_behavior
        assert instructions.get('action_metadata')['name'] == 'build'

    def test_display_behavior_needed_via_cli_and_get_instructions(self, tmp_path):
        """
        SCENARIO: Display behavior needed via CLI and get instructions
        GIVEN: CLI has story graph with stories at different behavior states
        WHEN: User executes 'scope' command
        THEN: CLI returns JSON with behavior field for each epic, sub-epic, and story
        AND: Behavior values match domain logic (explore/scenario/test/code)
        WHEN: User calls CLI submit command for epic with action "build"
        AND: Node calls get_required_behavior_instructions with action "build"
        THEN: Bot is set to behavior <expected_behavior>
        AND: Bot is set to action "build"
        AND: Instructions for behavior and action are returned
        
        This test validates that behavior_needed is included in CLI JSON output
        and can be used to submit with correct behavior.
        """
        # Given - Create story graph with stories at different behavior states
        helper = JsonBotTestHelper(tmp_path)
        helper.domain.state.set_state('shape', 'clarify')
        
        # Create epic with sub-epic containing stories with different behaviors
        epic_data = {
            "name": "Test Epic",
            "nested_sub_epics": [],
            "stories": [
                # Story with all scenarios tested -> code
                {
                    "story_name": "Story With Tests",
                    "test_class": "test_story.py",
                    "acceptance_criteria": "AC exists",
                    "scenarios": ["Scenario 1"],
                    "test_methods": ["test_scenario_1"]
                },
                # Story with scenarios but no tests -> test
                {
                    "story_name": "Story Needs Tests",
                    "test_class": "test_story.py",
                    "acceptance_criteria": "AC exists",
                    "scenarios": ["Scenario 1"],
                    "test_methods": []
                },
                # Story with AC but no scenarios -> scenario
                {
                    "story_name": "Story Needs Scenarios",
                    "test_class": "",
                    "acceptance_criteria": "AC exists",
                    "scenarios": [],
                    "test_methods": []
                },
                # Story with no AC -> explore
                {
                    "story_name": "Story Needs Exploration",
                    "test_class": "",
                    "acceptance_criteria": "",
                    "scenarios": [],
                    "test_methods": []
                }
            ]
        }
        
        epic = helper.domain.story.create_epic_with_sub_epics_for_behavior_test("Test Epic", [epic_data])
        
        # When - Execute scope command via CLI
        cli_response = helper.cli_session.execute_command('scope showall')
        response_data = json.loads(cli_response.output)
        
        # Then - JSON includes behavior field for all nodes
        assert 'scope' in response_data
        scope_data = response_data['scope']
        assert 'content' in scope_data
        assert 'epics' in scope_data['content']
        
        test_epic = next((e for e in scope_data['content']['epics'] if e['name'] == 'Test Epic'), None)
        assert test_epic is not None, "Test Epic not found in scope output"
        assert 'behavior_needed' in test_epic, "Epic missing 'behavior_needed' field"
        
        # Check sub-epic has behavior_needed
        assert 'sub_epics' in test_epic
        assert len(test_epic['sub_epics']) > 0
        sub_epic = test_epic['sub_epics'][0]
        assert 'behavior_needed' in sub_epic, "Sub-epic missing 'behavior_needed' field"
        
        # Check each story has correct behavior_needed
        stories = sub_epic['story_groups'][0]['stories']
        
        story_with_tests = next(s for s in stories if s['name'] == 'Story With Tests')
        assert 'behavior_needed' in story_with_tests, "Story missing 'behavior_needed' field"
        assert story_with_tests['behavior_needed'] == 'code', f"Expected 'code' but got '{story_with_tests['behavior_needed']}'"
        
        story_needs_tests = next(s for s in stories if s['name'] == 'Story Needs Tests')
        assert 'behavior_needed' in story_needs_tests, "Story missing 'behavior_needed' field"
        assert story_needs_tests['behavior_needed'] == 'tests', f"Expected 'tests' but got '{story_needs_tests['behavior_needed']}'"
        
        story_needs_scenarios = next(s for s in stories if s['name'] == 'Story Needs Scenarios')
        assert 'behavior_needed' in story_needs_scenarios, "Story missing 'behavior_needed' field"
        assert story_needs_scenarios['behavior_needed'] == 'scenarios', f"Expected 'scenarios' but got '{story_needs_scenarios['behavior_needed']}'"
        
        story_needs_exploration = next(s for s in stories if s['name'] == 'Story Needs Exploration')
        assert 'behavior_needed' in story_needs_exploration, "Story missing 'behavior_needed' field"
        assert story_needs_exploration['behavior_needed'] == 'exploration', f"Expected 'exploration' but got '{story_needs_exploration['behavior_needed']}'"
        
        # When - User calls CLI submit command for epic with action "build"
        # (Using the epic's behavior_needed which should be 'explore' based on highest behavior)
        expected_behavior = test_epic['behavior_needed']
        
        # Get instructions using the domain method (always uses build)
        instructions = epic.get_required_behavior_instructions()
        
        # Then - Bot is set to behavior and action (always build)
        assert helper.domain.bot.behaviors.current.name == expected_behavior
        assert helper.domain.bot.behaviors.current.actions.current.action_name == 'build'
        
        # And - Instructions object is returned
        from instructions.instructions import Instructions
        assert isinstance(instructions, Instructions), "Should return Instructions object"
        
        # Format instructions using JSON formatter for CLI
        from instructions.json_instructions import JSONInstructions
        formatter = JSONInstructions(instructions)
        instructions_dict = formatter.to_dict()
        
        assert instructions_dict is not None, "Instructions dict should not be None"
        assert 'behavior_metadata' in instructions_dict
        assert 'action_metadata' in instructions_dict
        assert instructions_dict['behavior_metadata']['name'] == expected_behavior
        assert instructions_dict['action_metadata']['name'] == 'build'


# ============================================================================
# DOMAIN TESTS - Submit Current Behavior Action
# ============================================================================

class TestSubmitCurrentBehaviorActionForSelectedNode:
    """
    Story: Submit Current Behavior Action For Selected Node
    
    Tests the bot's ability to use current behavior and action (from bot/panel selection)
    to submit instructions and set scope to the selected node.
    """
    
    @pytest.mark.parametrize("node_name,node_path,behavior,action", [
        ("Upload File", "File Management.Upload File", "code", "build"),
    ])
    def test_submit_current_behavior_action_for_selected_node(
        self,
        tmp_path,
        node_name,
        node_path,
        behavior,
        action
    ):
        """
        SCENARIO: Submit Current Behavior Action For Selected Node
        GIVEN: Bot has story map loaded with node <node_name>
        AND: Bot has current behavior <behavior>
        AND: Bot has current action <action>
        WHEN: User calls bot.story_graph."<node_path>".submit_current_instructions
        THEN: Bot submits instructions using current behavior <behavior> and action <action>
        AND: Scope is set to node <node_name>
        """
        # Given - Create a test story and set bot to current behavior/action
        helper = BotTestHelper(tmp_path)
        epic_name, story_name = node_path.split('.')
        story = helper.story.create_story_with_state_for_behavior_test(
            epic_name,
            story_name,
            test_class=None,
            acceptance_criteria='',
            scenarios=[],
            test_methods=[]
        )
        
        # Set bot to current behavior and action
        helper.bot.behaviors.navigate_to(behavior)
        helper.bot.behaviors.current.actions.navigate_to(action)
        
        # Capture scope before operation
        scope_before = helper.bot.scope()
        scope_type_before = scope_before.type.value
        scope_value_before = list(scope_before.value) if scope_before.value else []
        
        # When - User calls submit_current_instructions
        story.submit_current_instructions()
        
        # Then - Bot submits instructions using current behavior and action
        assert helper.bot.behaviors.current.name == behavior
        assert helper.bot.behaviors.current.actions.current.action_name == action
        
        # And - Scope is restored to what it was before
        scope_after = helper.bot.scope()
        assert scope_after.type.value == scope_type_before, f"Expected scope type '{scope_type_before}', got '{scope_after.type.value}'"
        assert list(scope_after.value) == scope_value_before, f"Expected scope value {scope_value_before}, got {list(scope_after.value)}"

    @pytest.mark.parametrize("node_name,node_path,behavior,action", [
        ("Upload File", "File Management.Upload File", "code", "build"),
    ])
    def test_submit_current_instructions_via_cli_json_format(
        self,
        tmp_path,
        node_name,
        node_path,
        behavior,
        action
    ):
        """
        SCENARIO: Submit Current Instructions Via CLI JSON Format
        GIVEN: CLI has story map loaded with node <node_name>
        AND: Bot has current behavior <behavior>
        AND: Bot has current action <action>
        WHEN: User executes CLI command story_graph."<node_path>".submit_current_instructions
        THEN: CLI returns JSON with submit result
        AND: Bot submits instructions using current behavior <behavior> and action <action>
        AND: Scope is set to node <node_name>
        """
        # Given - Create story and set bot to current behavior/action
        helper = JsonBotTestHelper(tmp_path)
        epic_name, story_name = node_path.split('.')
        
        story = helper.domain.story.create_story_with_state_for_behavior_test(
            epic_name,
            story_name,
            test_class=None,
            acceptance_criteria='',
            scenarios=[],
            test_methods=[]
        )
        
        helper.domain.bot.behaviors.navigate_to(behavior)
        helper.domain.bot.behaviors.current.actions.navigate_to(action)
        
        # Capture scope before operation
        scope_before = helper.domain.bot.scope()
        scope_type_before = scope_before.type.value
        scope_value_before = list(scope_before.value)
        
        # When - Execute submit_current_instructions via CLI
        command = f'story_graph."{epic_name}"."Test SubEpic"."{story_name}".submit_current_instructions'
        cli_response = helper.cli_session.execute_command(command)
        
        # Then - CLI returns valid JSON with Instructions object
        import json
        response_data = json.loads(cli_response.output.strip())
        assert 'instructions' in response_data, "Response should contain instructions"
        assert 'bot' in response_data, "Response should contain bot data"
        # Verify instructions have the expected structure
        instructions_data = response_data['instructions']
        assert 'behavior_metadata' in instructions_data or 'behavior_instructions' in instructions_data, "Instructions should have behavior metadata"
        assert 'action_metadata' in instructions_data or 'action_instructions' in instructions_data, "Instructions should have action metadata"
        
        # Verify bot submitted instructions using current behavior and action
        assert helper.domain.bot.behaviors.current.name == behavior
        assert helper.domain.bot.behaviors.current.actions.current.action_name == action
        
        # Verify scope is restored to what it was before
        scope_after = story._bot.scope() if story._bot else helper.domain.bot.scope()
        assert scope_after.type.value == scope_type_before, f"Expected scope type '{scope_type_before}', got '{scope_after.type.value}'"
        assert list(scope_after.value) == scope_value_before, f"Expected scope value {scope_value_before}, got {list(scope_after.value)}"


# ============================================================================
# Copy Story Node To Clipboard (Story under Act With Selected Node)
# ============================================================================

class TestCopyStoryNodeToClipboard:
    """Story: Copy Story Node To Clipboard. Domain logic for copy name and copy JSON."""

    def test_copy_name_returns_node_name(self, tmp_path):
        """
        SCENARIO: StoryNode copy_name returns node name for clipboard
        GIVEN: StoryMap is loaded with at least one Epic containing a SubEpic
        AND: Bot has that StoryMap loaded
        WHEN: copy_name is invoked on that SubEpic StoryNode
        THEN: StoryNode.copy_name returns status success
        AND: result is the node name
        AND: the result can be written to system clipboard by the panel
        """
        helper = BotTestHelper(tmp_path)
        graph_data = {
            "epics": [
                {
                    "name": "Invoke Bot",
                    "sub_epics": [
                        {
                            "name": "Act With Selected Node",
                            "sequential_order": 0,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "name": "",
                                    "sequential_order": 0,
                                    "type": "and",
                                    "connector": None,
                                    "stories": [
                                        {
                                            "name": "Copy Story Node To Clipboard",
                                            "sequential_order": 0,
                                            "connector": None,
                                            "story_type": "user",
                                            "users": [],
                                            "scenarios": [
                                                {
                                                    "name": "User copies node name",
                                                    "sequential_order": 0,
                                                    "type": "happy_path",
                                                    "background": [],
                                                    "steps": ""
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.story.create_story_graph(graph_data)
        epic = helper.bot.story_map.epics["Invoke Bot"]
        sub_epic = epic["Act With Selected Node"]
        story = sub_epic["Copy Story Node To Clipboard"]

        for node, expected_name in [
            (epic, "Invoke Bot"),
            (sub_epic, "Act With Selected Node"),
            (story, "Copy Story Node To Clipboard"),
        ]:
            result = node.copy_name()
            assert result["status"] == "success"
            assert result["result"] == expected_name
        if story.children:
            scenario = story.children[0]
            result = scenario.copy_name()
            assert result["status"] == "success"
            assert result["result"] == "User copies node name"

    def test_copy_json_returns_node_as_story_graph_json(self, tmp_path):
        """
        SCENARIO: StoryNode copy_json returns node as story-graph JSON
        GIVEN: StoryMap is loaded with an Epic and a SubEpic with known structure
        AND: Bot has that StoryMap loaded
        WHEN: copy_json is invoked on that SubEpic StoryNode
        THEN: StoryNode.copy_json returns status success
        AND: result is a dict with the same shape as the node in story-graph.json
        AND: the result can be serialized to JSON and written to system clipboard by the panel
        """
        helper = BotTestHelper(tmp_path)
        graph_data = {
            "epics": [
                {
                    "name": "Epic A",
                    "sequential_order": 0,
                    "behavior": None,
                    "sub_epics": [
                        {
                            "name": "SubEpic B",
                            "sequential_order": 0,
                            "behavior": None,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "name": "",
                                    "sequential_order": 0,
                                    "type": "and",
                                    "connector": None,
                                    "stories": [
                                        {
                                            "name": "Story C",
                                            "sequential_order": 0,
                                            "connector": None,
                                            "story_type": "user",
                                            "users": [],
                                            "scenarios": [],
                                            "behavior": None
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.story.create_story_graph(graph_data)
        story_map = helper.bot.story_map
        sub_epic = story_map.epics["Epic A"]["SubEpic B"]

        result = sub_epic.copy_json()
        assert result["status"] == "success"
        d = result["result"]
        assert isinstance(d, dict)
        assert d["name"] == "SubEpic B"
        assert "sub_epics" in d or "story_groups" in d
        assert json.loads(json.dumps(d)) == d

    def test_copy_json_for_story_includes_scenarios(self, tmp_path):
        """copy_json for a Story node includes scenarios and acceptance_criteria when include_level includes them."""
        helper = BotTestHelper(tmp_path)
        helper.bot._scope.include_level = "examples"  # Ensure scenarios/acceptance included
        graph_data = {
            "epics": [
                {
                    "name": "E1",
                    "sub_epics": [],
                    "story_groups": [
                        {
                            "name": "",
                            "sequential_order": 0,
                            "type": "and",
                            "connector": None,
                            "stories": [
                                {
                                    "name": "S1",
                                    "sequential_order": 0,
                                    "connector": None,
                                    "story_type": "user",
                                    "users": [],
                                    "scenarios": [
                                        {
                                            "name": "Scenario one",
                                            "sequential_order": 0,
                                            "type": "happy_path",
                                            "background": [],
                                            "steps": "Given x\nWhen y\nThen z"
                                        }
                                    ],
                                    "acceptance_criteria": [],
                                    "behavior": None
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.story.create_story_graph(graph_data)
        story = helper.bot.story_map.epics["E1"].children[0].children[0]

        result = story.copy_json()
        assert result["status"] == "success"
        d = result["result"]
        assert d["name"] == "S1"
        assert len(d["scenarios"]) == 1
        assert d["scenarios"][0]["name"] == "Scenario one"
        assert "steps" in d["scenarios"][0]

    def test_copy_json_respects_include_level_stories(self, tmp_path):
        """copy_json with scope.include_level='stories' excludes scenarios and acceptance_criteria."""
        helper = BotTestHelper(tmp_path)
        graph_data = {
            "epics": [
                {
                    "name": "E1",
                    "sub_epics": [],
                    "story_groups": [
                        {
                            "name": "",
                            "sequential_order": 0,
                            "type": "and",
                            "connector": None,
                            "stories": [
                                {
                                    "name": "S1",
                                    "sequential_order": 0,
                                    "connector": None,
                                    "story_type": "user",
                                    "users": [],
                                    "scenarios": [
                                        {
                                            "name": "Scenario one",
                                            "sequential_order": 0,
                                            "type": "happy_path",
                                            "background": [],
                                            "steps": "Given x"
                                        }
                                    ],
                                    "acceptance_criteria": [{"text": "AC1"}],
                                    "behavior": None
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.story.create_story_graph(graph_data)
        helper.bot._scope.include_level = "stories"
        story = helper.bot.story_map.epics["E1"].children[0].children[0]

        result = story.copy_json()
        assert result["status"] == "success"
        d = result["result"]
        assert d["name"] == "S1"
        assert d.get("scenarios") == [], "stories level should exclude scenarios"
        assert d.get("acceptance_criteria") == [], "stories level should exclude acceptance_criteria"

    def test_copy_increment_stories_json_respects_include_level(self, tmp_path):
        """copy_increment_stories_json respects scope.include_level (e.g. stories excludes scenarios)."""
        helper = BotTestHelper(tmp_path)
        graph_data = {
            "epics": [
                {
                    "name": "E1",
                    "sub_epics": [],
                    "story_groups": [
                        {
                            "name": "",
                            "sequential_order": 0,
                            "type": "and",
                            "connector": None,
                            "stories": [
                                {
                                    "name": "StoryInInc",
                                    "sequential_order": 0,
                                    "connector": None,
                                    "story_type": "user",
                                    "users": [],
                                    "scenarios": [{"name": "S1", "sequential_order": 0, "type": "happy_path", "background": [], "steps": ""}],
                                    "acceptance_criteria": [{"text": "AC1"}],
                                    "behavior": None
                                }
                            ]
                        }
                    ]
                }
            ],
            "increments": [{"name": "Inc1", "priority": 1, "stories": ["StoryInInc"]}],
        }
        helper.story.create_story_graph(graph_data)
        helper.bot._scope.include_level = "stories"

        result = helper.bot.story_map.copy_increment_stories_json("Inc1")
        assert result["status"] == "success"
        stories = result["result"]
        assert len(stories) == 1
        d = stories[0]
        assert d["name"] == "StoryInInc"
        assert d.get("scenarios") == [], "stories level should exclude scenarios"
        assert d.get("acceptance_criteria") == [], "stories level should exclude acceptance_criteria"

    def test_node_to_dict_serializes_each_node_type(self, tmp_path):
        """StoryMap.node_to_dict dispatches correctly for Epic, SubEpic, Story, Scenario."""
        helper = BotTestHelper(tmp_path)
        graph_data = {
            "epics": [
                {
                    "name": "Epic",
                    "sequential_order": 0,
                    "sub_epics": [
                        {
                            "name": "SubEpic",
                            "sequential_order": 0,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "name": "",
                                    "sequential_order": 0,
                                    "type": "and",
                                    "connector": None,
                                    "stories": [
                                        {
                                            "name": "Story",
                                            "sequential_order": 0,
                                            "connector": None,
                                            "story_type": "user",
                                            "users": [],
                                            "scenarios": [
                                                {
                                                    "name": "Scenario",
                                                    "sequential_order": 0,
                                                    "type": "happy_path",
                                                    "background": [],
                                                    "steps": ""
                                                }
                                            ],
                                            "behavior": None
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        helper.story.create_story_graph(graph_data)
        story_map = helper.bot.story_map
        epic = story_map.epics["Epic"]
        sub_epic = epic["SubEpic"]
        story = sub_epic["Story"]

        for node in (epic, sub_epic, story):
            d = story_map.node_to_dict(node)
            assert isinstance(d, dict)
            assert d["name"] == node.name
        if story.children:
            scenario = story.children[0]
            d = story_map.node_to_dict(scenario)
            assert isinstance(d, dict)
            assert d["name"] == scenario.name

    def test_copy_json_without_bot_context_raises(self, tmp_path):
        """copy_json without bot context raises ValueError."""
        helper = BotTestHelper(tmp_path)
        graph_data = {
            "epics": [{"name": "E1", "sub_epics": [], "story_groups": [{"name": "", "sequential_order": 0, "type": "and", "connector": None, "stories": []}]}]
        }
        helper.story.create_story_graph(graph_data)
        epic = helper.bot.story_map.epics["E1"]
        epic._bot = None
        with pytest.raises(ValueError, match="Cannot serialize node without bot context"):
            epic.copy_json()


class TestCopyStoryNodeToClipboardCLI:
    """
    Story: Copy Story Node To Clipboard (CLI)
    CLI focus: story_graph.<path>.copy_name and copy_json return result in response.
    """

    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper
    ])
    def test_cli_copy_name_returns_node_name(self, tmp_path, helper_class):
        """
        SCENARIO: CLI resolves story_graph path and copy_name returns node name
        GIVEN: StoryMap is loaded with Epic "Invoke Bot" and SubEpic "Manage Bot"
        AND: Bot has that StoryMap loaded
        WHEN: User executes CLI command story_graph."Invoke Bot"."Manage Bot".copy_name
        THEN: CLI returns success
        AND: response result is the SubEpic node name "Manage Bot"
        """
        helper = helper_class(tmp_path)
        helper.domain.story.create_story_graph_with_child("Epic", "Invoke Bot", "Manage Bot")

        cli_response = helper.cli_session.execute_command(
            'story_graph."Invoke Bot"."Manage Bot".copy_name'
        )

        output = cli_response.output
        if output.strip().startswith("{"):
            data = json.loads(output)
            assert data.get("status") == "success"
            assert data.get("result") == "Manage Bot"
        else:
            assert "success" in output.lower()
            assert "Manage Bot" in output

    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper
    ])
    def test_cli_copy_json_returns_node_dict(self, tmp_path, helper_class):
        """
        SCENARIO: CLI resolves story_graph path and copy_json returns node dict
        GIVEN: StoryMap is loaded with Epic "Invoke Bot" and SubEpic "Manage Bot"
        AND: Bot has that StoryMap loaded
        WHEN: User executes CLI command story_graph."Invoke Bot"."Manage Bot".copy_json
        THEN: CLI returns success
        AND: response result is a dict with name "Manage Bot" and story-graph shape for that node
        """
        helper = helper_class(tmp_path)
        helper.domain.story.create_story_graph_with_child("Epic", "Invoke Bot", "Manage Bot")

        cli_response = helper.cli_session.execute_command(
            'story_graph."Invoke Bot"."Manage Bot".copy_json'
        )

        output = cli_response.output
        if output.strip().startswith("{"):
            data = json.loads(output)
            assert data.get("status") == "success"
            result = data.get("result")
            assert isinstance(result, dict)
            assert result.get("name") == "Manage Bot"
        else:
            assert "success" in output.lower()
            assert "Manage Bot" in output

    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper
    ])
    def test_cli_copy_name_nonexistent_node_outputs_error(self, tmp_path, helper_class):
        """
        SCENARIO: CLI copy_name on non-existent node path returns error
        GIVEN: StoryMap is loaded with Epic "Invoke Bot" and SubEpic "Manage Bot"
        AND: Bot has that StoryMap loaded
        WHEN: User executes CLI command story_graph."Invoke Bot"."Non-existent Node".copy_name
        THEN: CLI returns error
        AND: output indicates node not found or path invalid
        AND: no result is written to clipboard
        """
        helper = helper_class(tmp_path)
        helper.domain.story.create_story_graph_with_child("Epic", "Invoke Bot", "Manage Bot")

        cli_response = helper.cli_session.execute_command(
            'story_graph."Invoke Bot"."Non-existent Node".copy_name'
        )

        assert "not found" in cli_response.output or "error" in cli_response.output.lower()
        assert "Non-existent Node" in cli_response.output


