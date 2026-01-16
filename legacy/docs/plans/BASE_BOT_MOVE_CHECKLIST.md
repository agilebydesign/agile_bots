# Files to Update When Moving base_bot from `agile_bot/bots/base_bot` to `agile_bot/base_bot`

## Summary
- **Old Path**: `agile_bot/bots/base_bot`
- **New Path**: `agile_bot/base_bot`
- **Change**: Remove `bots/` from path

---

## 1. CODE GENERATOR TEMPLATES (Generate code for other bots)

These files contain template strings that generate Python code for other bots. The generated code uses absolute imports, so these templates must be updated.

### base_bot/src/mcp/mcp_code_visitor.py
**Lines 165-171**: Template string that generates MCP server imports
- **Current**: `from agile_bot.bots.base_bot.src.bot.workspace import ...`
- **Change to**: `from agile_bot.base_bot.src.bot.workspace import ...`
- **Also**: `from agile_bot.bots.base_bot.src.bot.bot import ...` → `from agile_bot.base_bot.src.bot.bot import ...`
- **Also**: `from agile_bot.bots.base_bot.src.mcp.server_restart import ...` → `from agile_bot.base_bot.src.mcp.server_restart import ...`

---

## 2. CONFIG FILES (JSON) - baseActionsPath

All these files have `"baseActionsPath": "agile_bot/bots/base_bot/base_actions"` that needs to change to `"agile_bot/base_bot/base_actions"`.

### story_bot
- `agile_bot/bots/story_bot/bot_config.json` (line 16)
- `agile_bot/bots/story_bot/instructions.json` (line 6)
- `agile_bot/bots/story_bot/behaviors/shape/behavior.json` (line 8)
- `agile_bot/bots/story_bot/behaviors/prioritization/behavior.json` (line 8)
- `agile_bot/bots/story_bot/behaviors/discovery/behavior.json` (line 8)
- `agile_bot/bots/story_bot/behaviors/exploration/behavior.json` (line 8)
- `agile_bot/bots/story_bot/behaviors/scenarios/behavior.json` (line 8)
- `agile_bot/bots/story_bot/behaviors/tests/behavior.json` (line 8)
- `agile_bot/bots/story_bot/behaviors/code/behavior.json` (line 8)

### crc_bot
- `agile_bot/bots/crc_bot/bot_config.json` (line 12)
- `agile_bot/bots/crc_bot/instructions.json` (line 6, line 15)
- `agile_bot/bots/crc_bot/behaviors/domain/behavior.json` (line 8)
- `agile_bot/bots/crc_bot/behaviors/design/behavior.json` (line 8)
- `agile_bot/bots/crc_bot/behaviors/walkthrough/behavior.json` (line 8)

### base_bot (documentation/example)
- `agile_bot/bots/base_bot/docs/bots-overvew.md` (line 200) - Example in documentation

---

## 3. CONFIG FILES (JSON) - Scanner Class Paths

These files reference scanner classes using `agile_bot.bots.base_bot.src.scanners.*` or `agile_bot.bots.base_bot.src.actions.*`.

### story_bot behavior rules (scanner paths)
All files in `agile_bot/bots/story_bot/behaviors/*/rules/*.json` that have `"scanner": "agile_bot.bots.base_bot.src.scanners.*"`:
- `behaviors/shape/rules/disabled/story_sizing_guidelines.json` (line 3)
- `behaviors/code/rules/stop_writing_useless_comments.json` (line 3)
- `behaviors/code/rules/prefer_object_model_over_config.json` (line 7)
- `behaviors/code/rules/avoid_unnecessary_parameter_passing.json` (line 56)
- `behaviors/exploration/rules/behavioral_ac_at_story_level.json` (line 55)
- `behaviors/exploration/rules/stories_have_4_to_9_acceptance_criteria.json` (line 50)
- `behaviors/code/rules/detect_legacy_unused_code.json` (line 3)
- `behaviors/exploration/rules/use_and_for_multiple_reactions.json` (line 55)
- `behaviors/exploration/rules/alternate_actors_in_steps.json` (line 56)
- `behaviors/exploration/rules/enumerate_all_ac_permutations.json` (line 56)
- `behaviors/tests/rules/create_parameterized_tests_for_scenarios.json` (line 63)
- `behaviors/tests/rules/helper_extraction_and_reuse.json` (line 65)
- `behaviors/tests/rules/place_imports_at_top.json` (line 61)
- `behaviors/code/rules/enforce_encapsulation.json` (line 60)
- `behaviors/code/rules/hide_calculation_timing.json` (line 3)
- `behaviors/code/rules/hide_business_logic_behind_properties.json` (line 3)
- `behaviors/code/rules/place_imports_at_top.json` (line 63)
- `behaviors/code/rules/use_domain_language.json` (line 3)
- `behaviors/code/rules/use_clear_function_parameters.json` (line 52)
- `behaviors/tests/rules/use_given_when_then_helpers.json` (line 64)
- `behaviors/tests/rules/pytest_bdd_orchestrator_pattern.json` (line 65)
- `behaviors/scenarios/rules/write_plain_english_scenarios.json` (line 42)
- `behaviors/scenarios/rules/use_scenario_outline_when_needed.json` (line 38)
- `behaviors/scenarios/rules/use_domain_rich_language_in_testing_tables.json` (line 52)
- `behaviors/scenarios/rules/use_background_for_common_setup.json` (line 39)
- `behaviors/scenarios/rules/specify_constants_and_stub_values.json` (line 52)
- `behaviors/scenarios/rules/scenario_steps_start_with_scenario_specific_given.json` (line 40)
- `behaviors/scenarios/rules/scenarios_on_story_docs.json` (line 38)
- `behaviors/scenarios/rules/scenarios_cover_all_cases.json` (line 44)
- `behaviors/scenarios/rules/map_table_columns_to_scenario_parameters.json` (line 50)
- `behaviors/scenarios/rules/given_describes_state_not_actions.json` (line 40)
- `behaviors/scenarios/rules/scenarios_cover_all_cases.json` (line 44)
- Plus many more in `behaviors/*/rules/*.json` files

### crc_bot behavior rules
- `behaviors/domain/rules/use_resource_oriented_design.json` (line 5)

### base_bot action configs
- `agile_bot/bots/base_bot/base_actions/rules/action_config.json` (line 5): `"action_class": "agile_bot.bots.base_bot.src.actions.rules.rules_action.RulesAction"`
- `agile_bot/bots/base_bot/base_actions/help/action_config.json` (line 5): `"action_class": "agile_bot.bots.base_bot.src.actions.help_action.HelpAction"`

---

## 4. CONFIG FILES (JSON) - WORKING_AREA Paths

These files have hardcoded WORKING_AREA paths pointing to base_bot.

### story_bot
- `agile_bot/bots/story_bot/bot_config.json` (line 12, line 67): `"WORKING_AREA": "C:\\dev\\augmented-teams\\agile_bot\\bots\\base_bot"`

### crc_bot
- `agile_bot/bots/crc_bot/bot_config.json` (line 8): `"WORKING_AREA": "C:\\dev\\augmented-teams\\agile_bot\\bots\\base_bot"`
- `agile_bot/bots/crc_bot/mcp.json` (line 12): `"WORKING_AREA": "C:\\dev\\augmented-teams\\agile_bot\\bots\\base_bot"`

---

## 5. CONFIG FILES (JSON) - Registry

- `agile_bot/bots/registry.json` (lines 4, 9): `"repl_path": "agile_bot/bots/base_bot/src/repl_cli/repl_main.py"`

---

## 6. GENERATED FILES (Will be regenerated, but need initial update)

These files are generated by base_bot, but may exist and need updating:

- `agile_bot/bots/story_bot/src/story_bot_mcp_server.py` (lines 29-35): Generated MCP server imports
- `agile_bot/bots/crc_bot/src/crc_bot_mcp_server.py` (if exists): Generated MCP server imports

**Note**: These will be regenerated when running `generate.py`, but if they exist, they should be updated or regenerated.

---

## 7. GENERATOR SCRIPTS (Import base_bot)

These scripts import from base_bot to generate code:

### story_bot
- `agile_bot/bots/story_bot/generate.py` (lines 39-41):
  - `from agile_bot.bots.base_bot.src.cli.cli_generator import CliGenerator`
  - `from agile_bot.bots.base_bot.src.cli.cursor.command_generator import CursorCommandGenerator`
  - `from agile_bot.bots.base_bot.src.mcp.mcp_server_generator import MCPServerGenerator`

### crc_bot
- `agile_bot/bots/crc_bot/generate.py` (lines 39-41):
  - `from agile_bot.bots.base_bot.src.cli.cli_generator import CliGenerator`
  - `from agile_bot.bots.base_bot.src.cli.cursor.command_generator import CursorCommandGenerator`
  - `from agile_bot.bots.base_bot.src.mcp.mcp_server_generator import MCPServerGenerator`

### base_bot scripts
- `agile_bot/bots/base_bot/generate_bot.ps1` (lines 60, 86, 120):
  - `from agile_bot.bots.base_bot.src.cli.cli_generator import CliGenerator`
  - `from agile_bot.bots.base_bot.src.mcp.mcp_server_generator import MCPServerGenerator`
- `agile_bot/bots/base_bot/generate_bot.sh` (lines 103, 123, 151):
  - `from agile_bot.bots.base_bot.src.cli.cli_generator import CliGenerator`
  - `from agile_bot.bots.base_bot.src.mcp.mcp_server_generator import MCPServerGenerator`

---

## 8. DOCUMENTATION FILES (MD, TXT)

These contain example paths or references:

### base_bot/docs
- `agile_bot/bots/base_bot/docs/bots-overvew.md` - Multiple references
- `agile_bot/bots/base_bot/docs/plans/langgraph-orchestration.md` - Multiple references
- `agile_bot/bots/base_bot/docs/plans/repl-cli-display-refactoring.md` - Multiple path examples
- `agile_bot/bots/base_bot/docs/plans/repl-cli-refactoring-plan.md` - References
- `agile_bot/bots/base_bot/docs/plans/cli-multi-bot.md` - References
- `agile_bot/bots/base_bot/docs/plans/cli-chain-operations-plan.md` - References
- `agile_bot/bots/base_bot/docs/plans/stdio-cli-redesign.md` - References
- `agile_bot/bots/base_bot/docs/plans/stdio-cli-redesign.txt` - References
- `agile_bot/bots/base_bot/docs/plans/test-suite-summary.md` - References
- `agile_bot/bots/base_bot/docs/UI_Walkthrough.md` - Multiple path examples
- `agile_bot/bots/base_bot/docs/stories/increments/increment-11-plan.md` - Import examples
- `agile_bot/bots/base_bot/docs/stories/increments/increment-11-exploration.md` - Path references
- `agile_bot/bots/base_bot/docs/stories/increments/story-map-increments-backlog.md` - Path references
- `agile_bot/bots/base_bot/docs/stories/increments/increment-2-exploration.txt` - References
- `agile_bot/bots/base_bot/docs/stories/map/🎯 Build Agile Bots/⚙️ Generate REPL CLI/📝 Generate CLI Entry Point.md` - References
- `agile_bot/bots/base_bot/docs/stories/story-graph.json` - Multiple references
- `agile_bot/bots/base_bot/docs/crc/crc-model-outline.md` - References
- `agile_bot/bots/base_bot/docs/crc/crc-model-description.md` - References
- `agile_bot/bots/base_bot/docs/crc/crc-model-diagram.mmd` - References

### story_bot/docs
- `agile_bot/bots/story_bot/behaviors/tests/rules/README.md` (line 368): Import example

### base_bot/base_actions
- `agile_bot/bots/base_bot/base_actions/build/build-instructions.txt` (lines 74-75): Hardcoded paths

---

## 9. TEST FILES

Test files that reference base_bot paths:

### base_bot/test
- `agile_bot/bots/base_bot/test/test_helpers.py` (lines 308, 1979): Test fixtures with paths
- `agile_bot/bots/base_bot/test/test_perform_behavior_action.py` (multiple lines): Test fixtures
- `agile_bot/bots/base_bot/test/test_init_project.py` (line 46): Test fixture
- `agile_bot/bots/base_bot/test/test_build_scope_append.txt` (lines 74-75): Import examples
- `agile_bot/bots/base_bot/test/test_fixtures/bot_directory/behaviors/shape/behavior.json` (line 7): baseActionsPath

### test_base_bot
- `agile_bot/bots/test_base_bot/base_actions/validate/action_config.json` (lines 181, 205): Path references in instructions

---

## 10. PYTHON FILES WITH HARDCODED PATHS

### base_bot/src
- `agile_bot/bots/base_bot/src/repl_cli/repl_main.py` - May have path calculations
- `agile_bot/bots/base_bot/src/repl_cli/cli_scope.py` - May reference paths
- `agile_bot/bots/base_bot/src/repl_cli/generators/generate_repl_commands.py` - May reference paths
- `agile_bot/bots/base_bot/src/repl_cli/repl_session.py` - May reference paths
- `agile_bot/bots/base_bot/src/repl_cli/cli_bot/cli_bot.py` - May reference paths
- `agile_bot/bots/base_bot/src/actions/actions.py` - May reference paths
- `agile_bot/bots/base_bot/src/actions/help_action.py` - May reference paths
- `agile_bot/bots/base_bot/src/actions/activity_tracker.py` - May reference paths
- `agile_bot/bots/base_bot/src/actions/rules/rules.py` - May reference paths
- `agile_bot/bots/base_bot/src/actions/build/build_scope.py` - May reference paths
- `agile_bot/bots/base_bot/src/actions/action_factory.py` - May reference paths
- `agile_bot/bots/base_bot/src/scanners/scanner_orchestrator.py` - May reference paths
- `agile_bot/bots/base_bot/src/scanners/violation.py` - May reference paths
- `agile_bot/bots/base_bot/src/scanners/scanner_loader.py` - May reference paths
- `agile_bot/bots/base_bot/src/scanners/resources/scan.py` - May reference paths
- `agile_bot/bots/base_bot/src/scanners/resources/violation.py` - May reference paths
- `agile_bot/bots/base_bot/src/scanners/scanner.py` - May reference paths
- `agile_bot/bots/base_bot/src/scanners/story_map.py` - May reference paths
- `agile_bot/bots/base_bot/src/scanners/real_implementations_scanner.py` - May reference paths
- `agile_bot/bots/base_bot/src/scanners/scanner_registry.py` - May reference paths
- `agile_bot/bots/base_bot/src/actions/instructions.py` - May reference paths
- `agile_bot/bots/base_bot/src/actions/render/render_instruction_builder.py` - May reference paths
- `agile_bot/bots/base_bot/src/repl_cli/cli_bot/cli_actions/cli_actions.py` - May reference paths
- `agile_bot/bots/base_bot/src/repl_cli/cli_bot/cli_behavior.py` - May reference paths
- `agile_bot/bots/base_bot/src/repl_cli/cli_bot/cli_actions/cli_action_factory.py` - May reference paths
- `agile_bot/bots/base_bot/src/repl_cli/status_display.py` - May reference paths

**Note**: Most of these likely use relative imports now, but may have hardcoded path strings or comments.

---

## 11. STORY_BOT SOURCE FILES (Import base_bot)

### story_bot/src
- `agile_bot/bots/story_bot/src/synchronizers/story_io/examples/*.py` - May import from base_bot
- `agile_bot/bots/story_bot/src/synchronizers/story_tests/*.py` - May import from base_bot

---

## SUMMARY BY PRIORITY

### CRITICAL (Must update before move works)
1. **Template strings** in `mcp_code_visitor.py` (generates code for other bots)
2. **All `baseActionsPath`** in behavior.json and bot_config.json files
3. **All scanner class paths** in rule JSON files
4. **Generator scripts** (generate.py files) that import base_bot
5. **Registry.json** repl_path

### IMPORTANT (Update after move)
6. **WORKING_AREA paths** in bot_config.json and mcp.json
7. **Generated MCP server files** (regenerate after move)
8. **Action class paths** in base_actions/*/action_config.json

### OPTIONAL (Documentation/examples)
9. **Documentation files** (MD, TXT) - Update for accuracy
10. **Test files** - Update test fixtures
11. **Python files** - Check for hardcoded path strings

---

## SEARCH PATTERNS TO FIND ALL REFERENCES

Use these grep patterns to find all references:

```bash
# Find all JSON config files with baseActionsPath
grep -r "baseActionsPath.*bots/base_bot" agile_bot/bots/

# Find all scanner class references
grep -r "agile_bot\.bots\.base_bot\.src\.scanners" agile_bot/bots/

# Find all action class references
grep -r "agile_bot\.bots\.base_bot\.src\.actions" agile_bot/bots/

# Find all WORKING_AREA references
grep -r "WORKING_AREA.*bots/base_bot" agile_bot/bots/

# Find all import statements
grep -r "from agile_bot\.bots\.base_bot" agile_bot/bots/

# Find all path references
grep -r "bots/base_bot" agile_bot/bots/
```
