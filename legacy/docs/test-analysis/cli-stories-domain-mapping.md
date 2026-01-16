# CLI Stories to Domain Classes Mapping

This document maps CLI-related stories and scenarios to the domain classes that will be impacted by test failures.

## Test Files Analyzed
- `test_initialize_cli_session.py` - 5 test classes, 13 scenarios ✅
- `test_execute_actions_using_cli.py` - 5 test classes, 5 scenarios
- `test_navigate_behaviors_using_cli_commands.py` - 5 test classes, 8 scenarios
- `test_get_help_using_cli.py` - 2 test classes, 2 scenarios
- `test_manage_scope_using_cli.py` - 1 test class, 2 scenarios

**Total: 18 test classes, 30 scenarios**

## Test Methodology: Exact Format Verification

**CRITICAL:** Tests MUST verify the exact format returned by adapters using **hard-coded expected values**, NOT by calling the adapter to generate expected output.

**❌ WRONG Approach (DO NOT DO THIS):**
```python
# DON'T generate expected output from adapter - this doesn't test anything!
tty_bot = AdapterFactory.create(bot, 'tty')
expected_output = tty_bot.serialize()
assert cli_output == expected_output  # This just tests adapter against itself!
```

**✅ CORRECT Approach (USE THIS):**
```python
# Use hard-coded expected values based on adapter format
cli_response = cli_session.execute_command('status')
output = cli_response.output

# Verify exact format with hard-coded expectations
assert "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" in output
assert "CLI STATUS section" in output
assert "🤖 Bot:" in output
assert bot.bot_name in output
assert "Bot Path:" in output
assert str(bot.bot_paths.bot_directory) in output

# Verify section order
header_pos = output.find("CLI STATUS section")
bot_name_pos = output.find("🤖 Bot:")
assert header_pos < bot_name_pos, "Sections must appear in correct order"
```

**What to Verify:**
- Exact ANSI bold codes (`\033[1m` ... `\033[0m`) - check for presence, not exact match
- Exact separator line format (100 chars, specific characters like `━`)
- Exact spacing and newlines
- Exact section order (use `find()` to verify positions)
- Exact text content (including emoji, formatting)
- No extra or missing content
- For JSON: Valid JSON structure with required fields
- For Markdown: Markdown syntax (headers `##`, bold `**text**`, code blocks `` `text` ``)

## Domain Classes in CLI Package
- `CLISession` - Main command router and session manager
- `CLICommandResponse` - Response wrapper for CLI commands
- `AdapterFactory` - Creates adapters for domain objects
- `TTYAdapter` / `JSONAdapter` - Serialization adapters
- `cli_main.py` - Entry point and mode detection

## Domain Classes Referenced (Outside CLI Package)
- `Bot` - Main bot instance
- `Behaviors` - Behavior collection
- `Behavior` - Individual behavior
- `Actions` - Action collection (includes `_non_workflow_actions`)
- `Action` - Individual action
- `Instructions` - Instructions object
- `Scope` - Scope filter
- `Help` - Help object
- `NavigationResult` - Navigation result
- `ActionStateManager` - State persistence

## Story Mappings

**IMPORTANT: Mode-Specific Stories Pattern**

CLI initialization stories are now organized by output mode to ensure all formats (TTY, Markdown, JSON) are properly tested. This pattern was established in the story graph (`agile_bot/docs/stories/story-graph.json`) and should be carried forward for all future CLI features.

**The Three Mode Stories:**

1. **Story 1: Launch CLI in Interactive Mode (TTY Mode)** ✅
   - Test Class: `TestStartCLISessionInTTYMode`
   - Auto-detected when `sys.stdin.isatty() == True`
   - Uses TTY adapters for output formatting
   - 5 scenarios covering initialization, state loading, and format verification

2. **Story 2: Launch CLI in Pipe Mode (Markdown Mode)** ✅
   - Test Class: `TestStartCLISessionInPipeMode`
   - Auto-detected when `sys.stdin.isatty() == False`
   - Uses Markdown adapters for output formatting (AI agents)
   - 4 scenarios covering initialization and markdown format verification

3. **Story 14: Launch CLI in JSON Mode** ✅
   - Test Class: `TestStartCLISessionInJSONMode`
   - Explicitly set via `CLISession(bot=bot, workspace_directory=workspace, mode='json')`
   - Uses JSON adapters for output formatting (web views)
   - 4 scenarios covering initialization and JSON format verification

**Pattern to Carry Forward:**
- When adding new CLI features, create mode-specific test stories following this pattern
- Each mode story verifies the same functionality but with mode-appropriate format expectations
- Tests use **hard-coded expected values**, NOT adapter-generated values
- This ensures all output formats (TTY, Markdown, JSON) are properly tested and maintained
- See `agile_bot/docs/plans/STATUS_TEST_PORTING_GUIDE.md` for detailed guidance

**Story Graph References:**
- Story Graph: `agile_bot/docs/stories/story-graph.json` → Epic "Build Agile Bots" → Sub-Epic "Initialize CLI Session"
- Plan Document: `agile_bot/docs/plans/STATUS_TEST_PORTING_GUIDE.md` → Section "IMPORTANT: Mode-Specific Stories Pattern"

---

### 1. Launch CLI in Interactive Mode (TTY Mode) ✅
**Test File:** `test_initialize_cli_session.py::TestStartCLISessionInTTYMode`

**Scenarios:**
- `test_cli_launches_in_interactive_mode` - Basic initialization ✅
- `test_cli_loads_existing_behavior_action_state_on_launch` - State loading ✅
- `test_cli_displays_status_on_launch` - Status display verification ✅
- `test_cli_displays_header_section` - Header section verification ✅
- `test_cli_displays_bot_section` - Bot section verification ✅

**Test Requirements for Status Display (IMPLEMENTED):**

**Scenario: `test_cli_displays_status_on_launch`** ✅
- **GIVEN:** CLI session initialized in interactive mode
- **WHEN:** `status` command is executed
- **THEN:** Verify complete TTY adapter output format using hard-coded expectations:
  - All sections appear in correct order (header → bot name → bot paths → progress → commands → summary)
  - Verify each section with hard-coded string assertions
  - Verify section order using `find()` position comparisons
  - **Key Learning:** Use hard-coded expected values, NOT adapter-generated values

**Scenario: `test_cli_displays_header_section`** ✅
- **GIVEN:** CLI session initialized
- **WHEN:** `status` command is executed
- **THEN:** Verify header section with hard-coded expectations:
  - Section separator line (100 chars of `━`)
  - Centered bold "CLI STATUS section" text (check for text presence)
  - Description text: "This section contains current scope filter..."
  - Warning text: "☢️  You MUST DISPLAY this entire section..."
  - Closing separator line
  - Verify header appears before bot section using position comparison
  - **Key Learning:** Check for text content and order, not exact ANSI code matching

**Scenario: `test_cli_displays_bot_section`** ✅
- **GIVEN:** CLI session initialized
- **WHEN:** `status` command is executed
- **THEN:** Verify bot section with hard-coded expectations:
  - Bot name: `🤖 Bot: {bot_name}` (check for emoji and bot name)
  - Bot Path section:
    - "Bot Path:" label
    - Bot directory path (check for actual path value)
    - Workspace section: `📂 Workspace:` (check for emoji and label)
    - Workspace name and directory path
    - "To change path:" instructions
    - Example commands
  - Verify section order using position comparisons
  - **Key Learning:** Verify structure and content, not exact formatting codes

**Impacted Domain Classes:**
- `CLISession.__init__()` - Session initialization
- `CLISession.execute_command()` - Command execution
- `CLISession._get_adapter_for_domain()` - Adapter selection (TTY mode)
- `Bot` - Bot initialization
- `Behaviors.load_state()` - State loading
- `ActionStateManager` - State file reading
- `AdapterFactory.create()` - TTY adapter creation
- `TTYBot.serialize()` - Complete status display formatting (MUST match exactly)
- `TTYBot.header` - CLI STATUS section header (MUST match exactly)
- `TTYBot.name` - Bot name display (MUST match format: bold "🤖 Bot:", plain name)
- `TTYBot.bot_paths` - Bot paths section (delegates to TTYBotPath)
- `TTYBotPath.serialize()` - Bot paths formatting (MUST match exactly)
- `TTYBotPath` properties - Bot directory, workspace directory, change path instructions
- `TTYAdapter.add_bold()` - Bold formatting (ANSI codes)
- `TTYAdapter.section_separator()` - Separator lines
- `TTYAdapter.subsection_separator()` - Subsection separators
- `cli_main.py` - Initial header printing (bot name banner, AI instructions)

---

### 2. Launch CLI in Pipe Mode (Markdown Mode) ✅
**Test File:** `test_initialize_cli_session.py::TestStartCLISessionInPipeMode`

**Scenarios:**
- `test_cli_launches_in_pipe_mode` - Pipe mode initialization ✅
- `test_cli_displays_status_in_markdown_format` - Markdown status display ✅
- `test_cli_displays_header_section_in_markdown` - Markdown header section ✅
- `test_cli_displays_bot_section_in_markdown` - Markdown bot section ✅

**Test Requirements (IMPLEMENTED):**
- **GIVEN:** CLI session initialized in pipe mode (non-TTY detected)
- **WHEN:** `status` command is executed
- **THEN:** Verify markdown format output with hard-coded expectations:
  - Markdown separators (`---`)
  - Markdown headers (`##`)
  - Markdown bold (`**text**`)
  - Markdown code blocks (`` `text` `` and ```code blocks```)
  - Markdown list items (`-`)
  - **Key Learning:** Verify markdown syntax elements, not exact content matching

**Impacted Domain Classes:**
- `CLISession.__init__()` - Session initialization (mode-agnostic)
- `CLISession._get_adapter_for_domain()` - Auto-detects markdown for piped input
- `CLISession.mode` - Mode property (None = auto-detect)
- `AdapterFactory.create()` - Markdown adapter creation
- `MarkdownBot.serialize()` - Markdown formatting (matches TTYBot structure)
- `MarkdownScope.serialize()` - Markdown scope formatting

---

### 3. Navigate Using CLI Dot Notation

**Requires Three Mode Stories:** Interactive Mode (TTY), Piped Mode (Markdown), JSON Mode

#### Interactive Mode (TTY)
**Test File:** `test_navigate_behaviors_using_cli_commands.py::TestNavigateToBehaviorActionAndExecuteInTTYMode`

**Scenarios:**
- `test_user_navigates_with_behavior_only` - Single word (behavior name) - Verifies TTY output format
- `test_user_navigates_with_behavior_dot_action` - `behavior.action` format - Verifies TTY output format
- `test_user_navigates_with_full_dot_notation` - `behavior.action.operation` format - Verifies TTY output format
- `test_user_enters_invalid_behavior_in_dot_notation` - Error handling - Verifies TTY error format

#### Piped Mode (Markdown)
**Test File:** `test_navigate_behaviors_using_cli_commands.py::TestNavigateToBehaviorActionAndExecuteInPipeMode`

**Scenarios:**
- `test_user_navigates_with_behavior_only` - Single word (behavior name) - Verifies markdown output format
- `test_user_navigates_with_behavior_dot_action` - `behavior.action` format - Verifies markdown output format
- `test_user_navigates_with_full_dot_notation` - `behavior.action.operation` format - Verifies markdown output format
- `test_user_enters_invalid_behavior_in_dot_notation` - Error handling - Verifies markdown error format

#### JSON Mode
**Test File:** `test_navigate_behaviors_using_cli_commands.py::TestNavigateToBehaviorActionAndExecuteInJSONMode`

**Scenarios:**
- `test_user_navigates_with_behavior_only` - Single word (behavior name) - Verifies JSON output format
- `test_user_navigates_with_behavior_dot_action` - `behavior.action` format - Verifies JSON output format
- `test_user_navigates_with_full_dot_notation` - `behavior.action.operation` format - Verifies JSON output format
- `test_user_enters_invalid_behavior_in_dot_notation` - Error handling - Verifies JSON error format

**Impacted Domain Classes:**
- `CLISession._parse_command()` - Command parsing (verb, args)
- `CLISession._route_to_behavior_action()` - Dot notation routing
- `CLISession._handle_action_shortcut()` - Action shortcut detection
- `CLISession.execute_command()` - Command routing logic
- `Bot.behaviors.navigate_to()` - Behavior navigation
- `Behavior.actions.navigate_to()` - Action navigation (workflow vs non-workflow)
- `Bot.execute()` - Action execution
- `TTYBot` / `TTYBehaviors` / `TTYActions` - Navigation output formatting
- `Actions._non_workflow_actions` - Non-workflow action handling

---

### 4. Navigate Using Next/Back Commands

**Requires Three Mode Stories:** Interactive Mode (TTY), Piped Mode (Markdown), JSON Mode

#### Interactive Mode (TTY)
**Test File:** `test_navigate_behaviors_using_cli_commands.py::TestNavigateSequentiallyInTTYMode`

**Scenarios:**
- `test_user_navigates_with_next_command` - Next action navigation - Verifies TTY output format
- `test_user_navigates_with_back_command` - Back navigation (xfail - not implemented) - Verifies TTY output format

#### Piped Mode (Markdown)
**Test File:** `test_navigate_behaviors_using_cli_commands.py::TestNavigateSequentiallyInPipeMode`

**Scenarios:**
- `test_user_navigates_with_next_command` - Next action navigation - Verifies markdown output format
- `test_user_navigates_with_back_command` - Back navigation (xfail - not implemented) - Verifies markdown output format

#### JSON Mode
**Test File:** `test_navigate_behaviors_using_cli_commands.py::TestNavigateSequentiallyInJSONMode`

**Scenarios:**
- `test_user_navigates_with_next_command` - Next action navigation - Verifies JSON output format
- `test_user_navigates_with_back_command` - Back navigation (xfail - not implemented) - Verifies JSON output format

**Impacted Domain Classes:**
- `CLISession.execute_command()` - Command routing to `Bot.next()`
- `Bot.next()` - Next action/behavior navigation
- `Bot.back()` - Previous navigation (may not exist)
- `Actions.next()` - Next action in workflow
- `Actions.navigate_to()` - Action navigation
- `NavigationResult` - Navigation result object
- `TTYAdapter` - Navigation result formatting
- `ActionStateManager` - State updates after navigation

---

### 5. Get Action Instructions Through CLI

**Requires Three Mode Stories:** Interactive Mode (TTY), Piped Mode (Markdown), JSON Mode

#### Interactive Mode (TTY)
**Test File:** `test_execute_actions_using_cli.py::TestViewInstructionsInTTYMode`

**Scenarios:**
- `test_user_gets_instructions_for_build_action` - Instructions command - Verifies TTY format

#### Piped Mode (Markdown)
**Test File:** `test_execute_actions_using_cli.py::TestViewInstructionsInPipeMode`

**Scenarios:**
- `test_user_gets_instructions_for_build_action` - Instructions command - Verifies markdown format

#### JSON Mode
**Test File:** `test_execute_actions_using_cli.py::TestViewInstructionsInJSONMode`

**Scenarios:**
- `test_user_gets_instructions_for_build_action` - Instructions command - Verifies JSON format

**Impacted Domain Classes:**
- `CLISession.execute_command()` - Command routing
- `CLISession._handle_action_shortcut()` - Action shortcut handling
- `Bot.current()` - Get current instructions
- `Action.get_instructions()` - Instruction generation (workflow actions)
- `Action.execute()` - Action execution (non-workflow actions like 'rules')
- `Instructions` - Instructions object
- `TTYInstructions` - Instructions formatting
- `Actions._non_workflow_actions` - Non-workflow action detection

---

### 6. Confirm Work Through CLI

**Requires Three Mode Stories:** Interactive Mode (TTY), Piped Mode (Markdown), JSON Mode

#### Interactive Mode (TTY)
**Test File:** `test_execute_actions_using_cli.py::TestConfirmWithParametersInTTYMode`

**Scenarios:**
- `test_user_confirms_build_work` - Confirm command execution - Verifies TTY format

#### Piped Mode (Markdown)
**Test File:** `test_execute_actions_using_cli.py::TestConfirmWithParametersInPipeMode`

**Scenarios:**
- `test_user_confirms_build_work` - Confirm command execution - Verifies markdown format

#### JSON Mode
**Test File:** `test_execute_actions_using_cli.py::TestConfirmWithParametersInJSONMode`

**Scenarios:**
- `test_user_confirms_build_work` - Confirm command execution - Verifies JSON format

**Impacted Domain Classes:**
- `CLISession.execute_command()` - Command routing to `Bot.confirm()`
- `Bot.confirm()` - Action confirmation
- `Action.do_execute()` - Action execution
- `Action.execute()` - Action wrapper (tracks activity)
- `ActionStateManager` - State updates
- `Actions.close_current()` - Action completion
- `TTYAdapter` - Confirmation output formatting

---

### 7. Confirm Action Completion
**Test File:** `test_execute_actions_using_cli.py::TestConfirmActionCompletion`

**Scenarios:**
- `test_user_confirms_build_action_completion` - Completion workflow

**Impacted Domain Classes:**
- `CLISession.execute_command()` - Command routing
- `Bot.confirm()` - Action confirmation
- `Actions.close_current()` - Action completion and state advancement
- `ActionStateManager` - State persistence
- `Behaviors` - Behavior state updates
- `Actions._advance_to_next_action()` - Workflow advancement

---

### 8. Filter Work Using Scope

**Requires Three Mode Stories:** Interactive Mode (TTY), Piped Mode (Markdown), JSON Mode

#### Interactive Mode (TTY)
**Test File:** `test_manage_scope_using_cli.py::TestSetScopeInTTYMode`

**Scenarios:**
- `test_user_sets_scope_filter` - Setting scope with quoted arguments - Verifies TTY format
- `test_user_views_current_scope` - Viewing current scope - Verifies TTY format

#### Piped Mode (Markdown)
**Test File:** `test_manage_scope_using_cli.py::TestSetScopeInPipeMode`

**Scenarios:**
- `test_user_sets_scope_filter` - Setting scope with quoted arguments - Verifies markdown format
- `test_user_views_current_scope` - Viewing current scope - Verifies markdown format

#### JSON Mode
**Test File:** `test_manage_scope_using_cli.py::TestSetScopeInJSONMode`

**Scenarios:**
- `test_user_sets_scope_filter` - Setting scope with quoted arguments - Verifies JSON format
- `test_user_views_current_scope` - Viewing current scope - Verifies JSON format

**Impacted Domain Classes:**
- `CLISession.execute_command()` - Command routing to `Bot.scope()`
- `CLISession._parse_command()` - Argument parsing (quoted strings like `story="Story1"`)
- `Bot.scope()` - Scope management (set/view)
- `Scope` - Scope object (filter application)
- `TTYScope` - Scope display formatting
- `Scope.load()` / `Scope.save()` - Scope persistence

---

### 9. View Available Commands (Help)

**Requires Three Mode Stories:** Interactive Mode (TTY), Piped Mode (Markdown), JSON Mode

#### Interactive Mode (TTY)
**Test File:** `test_get_help_using_cli.py::TestDisplayActionHelpUsingCLIInTTYMode`

**Scenarios:**
- `test_user_views_all_available_commands` - Help command - Verifies TTY format
- `test_user_views_examples_in_help` - Help examples display - Verifies TTY format

#### Piped Mode (Markdown)
**Test File:** `test_get_help_using_cli.py::TestDisplayActionHelpUsingCLIInPipeMode`

**Scenarios:**
- `test_user_views_all_available_commands` - Help command - Verifies markdown format
- `test_user_views_examples_in_help` - Help examples display - Verifies markdown format

#### JSON Mode
**Test File:** `test_get_help_using_cli.py::TestDisplayActionHelpUsingCLIInJSONMode`

**Scenarios:**
- `test_user_views_all_available_commands` - Help command - Verifies JSON format
- `test_user_views_examples_in_help` - Help examples display - Verifies JSON format

**Impacted Domain Classes:**
- `CLISession.execute_command()` - Command routing to `Bot.help()`
- `Bot.help()` - Help generation
- `Help` - Help object (command list, examples)
- `TTYAdapter` - Help formatting

---

### 10. Display Status

**Requires Three Mode Stories:** Interactive Mode (TTY), Piped Mode (Markdown), JSON Mode

#### Interactive Mode (TTY)
**Test File:** `test_navigate_behaviors_using_cli_commands.py::TestDisplayBotHierarchyTreeInTTYMode`

**Scenarios:**
- `test_user_views_bot_hierarchy_with_status_command` - Status command - Verifies TTY format
- `test_user_views_current_position_in_status` - Position display - Verifies TTY format
- `test_cli_displays_progress_section_with_current_position` - Progress section - Verifies TTY format
- `test_cli_displays_behavior_in_progress_section` - Behavior display - Verifies TTY format

#### Piped Mode (Markdown)
**Test File:** `test_navigate_behaviors_using_cli_commands.py::TestDisplayBotHierarchyTreeInPipeMode`

**Scenarios:**
- `test_user_views_bot_hierarchy_with_status_command` - Status command - Verifies markdown format
- `test_user_views_current_position_in_status` - Position display - Verifies markdown format
- `test_cli_displays_progress_section_with_current_position` - Progress section - Verifies markdown format
- `test_cli_displays_behavior_in_progress_section` - Behavior display - Verifies markdown format

#### JSON Mode
**Test File:** `test_navigate_behaviors_using_cli_commands.py::TestDisplayBotHierarchyTreeInJSONMode`

**Scenarios:**
- `test_user_views_bot_hierarchy_with_status_command` - Status command - Verifies JSON format
- `test_user_views_current_position_in_status` - Position display - Verifies JSON format
- `test_cli_displays_progress_section_with_current_position` - Progress section - Verifies JSON format
- `test_cli_displays_behavior_in_progress_section` - Behavior display - Verifies JSON format

**Impacted Domain Classes:**
- `CLISession.execute_command()` - Status command routing
- `CLISession.execute_command()` - Auto-status display after navigation
- `Bot` - Bot status (current behavior, action, progress path)
- `TTYBot` - Status formatting (CLI STATUS section, Progress, Commands)
- `TTYBehaviors` - Behavior list formatting (all behaviors with pipes, current bolded)
- `TTYActions` - Action list formatting (all actions with pipes, current bolded, includes 'rules')
- `TTYScope` - Scope display (bold formatting)
- `TTYStoryGraph` - Story graph display
- `TTYAdapter.add_bold()` - Bold formatting method

### 11. Re-execute Current Operation

**Requires Three Mode Stories:** Interactive Mode (TTY), Piped Mode (Markdown), JSON Mode

#### Interactive Mode (TTY)
**Test File:** `test_execute_actions_using_cli.py::TestReExecuteCurrentActionInTTYMode`

**Scenarios:**
- `test_user_re_executes_current_instructions` - Current command - Verifies TTY format

#### Piped Mode (Markdown)
**Test File:** `test_execute_actions_using_cli.py::TestReExecuteCurrentActionInPipeMode`

**Scenarios:**
- `test_user_re_executes_current_instructions` - Current command - Verifies markdown format

#### JSON Mode
**Test File:** `test_execute_actions_using_cli.py::TestReExecuteCurrentActionInJSONMode`

**Scenarios:**
- `test_user_re_executes_current_instructions` - Current command - Verifies JSON format

**Impacted Domain Classes:**
- `CLISession.execute_command()` - Command routing
- `Bot.current()` - Get current instructions
- `Action.get_instructions()` - Instruction generation
- `Instructions` - Instructions object
- `TTYInstructions` - Instructions formatting

### 12. Handle Operation Errors

**Requires Three Mode Stories:** Interactive Mode (TTY), Piped Mode (Markdown), JSON Mode

#### Interactive Mode (TTY)
**Test File:** `test_execute_actions_using_cli.py::TestHandleErrorsAndValidationInTTYMode`

**Scenarios:**
- `test_user_enters_invalid_command` - Error handling - Verifies TTY error format

#### Piped Mode (Markdown)
**Test File:** `test_execute_actions_using_cli.py::TestHandleErrorsAndValidationInPipeMode`

**Scenarios:**
- `test_user_enters_invalid_command` - Error handling - Verifies markdown error format

#### JSON Mode
**Test File:** `test_execute_actions_using_cli.py::TestHandleErrorsAndValidationInJSONMode`

**Scenarios:**
- `test_user_enters_invalid_command` - Error handling - Verifies JSON error format

**Impacted Domain Classes:**
- `CLISession.execute_command()` - Error detection
- `CLISession._route_to_behavior_action()` - Validation errors
- `CLISession._handle_action_shortcut()` - Action not found handling
- `CLICommandResponse` - Error response format

### 13. Exit CLI Session

**Requires Three Mode Stories:** Interactive Mode (TTY), Piped Mode (Markdown), JSON Mode

#### Interactive Mode (TTY)
**Test File:** `test_navigate_behaviors_using_cli_commands.py::TestExitCLIInTTYMode`

**Scenarios:**
- `test_user_exits_cli_with_exit_command` - Exit command - Verifies TTY format

#### Piped Mode (Markdown)
**Test File:** `test_navigate_behaviors_using_cli_commands.py::TestExitCLIInPipeMode`

**Scenarios:**
- `test_user_exits_cli_with_exit_command` - Exit command - Verifies markdown format

#### JSON Mode
**Test File:** `test_navigate_behaviors_using_cli_commands.py::TestExitCLIInJSONMode`

**Scenarios:**
- `test_user_exits_cli_with_exit_command` - Exit command - Verifies JSON format

**Impacted Domain Classes:**
- `CLISession.execute_command()` - Exit command detection
- `CLICommandResponse.cli_terminated` - Termination flag
- `Bot.exit()` - Exit handling (if exists)

### 14. Launch CLI in JSON Mode ✅
**Test File:** `test_initialize_cli_session.py::TestStartCLISessionInJSONMode`

**Scenarios:**
- `test_cli_launches_in_json_mode` - JSON mode initialization ✅
- `test_cli_displays_status_in_json_format` - JSON status display ✅
- `test_cli_displays_header_section_in_json` - JSON header section ✅
- `test_cli_displays_bot_section_in_json` - JSON bot section ✅

**Test Requirements (IMPLEMENTED):**
- **GIVEN:** CLI session initialized with `mode='json'` (explicit JSON mode for web views)
- **WHEN:** `status` command is executed
- **THEN:** Verify JSON format output with hard-coded expectations:
  - Valid JSON structure (parse with `json.loads()`)
  - Required fields present (`name`, `bot_directory`, `workspace_directory`, `behavior_names`, `current_behavior`)
  - **Key Learning:** JSON mode is set explicitly via `mode` parameter, not auto-detected

**Impacted Domain Classes:**
- `CLISession.__init__()` - Accepts `mode` parameter ('tty', 'markdown', 'json')
- `CLISession.mode` - Mode property (explicit or None for auto-detect)
- `CLISession._get_adapter_for_domain()` - Uses explicit mode if set, otherwise auto-detects
- `AdapterFactory.create()` - JSON adapter creation
- `JSONBot.serialize()` - JSON formatting (via `to_dict()` and `json.dumps()`)

### 15. Detect and Configure TTY/Non-TTY Input ✅
**Test File:** `test_initialize_cli_session.py::TestDetectAndConfigureTTYNonTTYInput`

**Scenarios:**
- `test_tty_detector_identifies_interactive_terminal` - TTY detection ✅
- `test_tty_detector_identifies_piped_input` - Non-TTY detection ✅

**Impacted Domain Classes:**
- `CLISession._get_adapter_for_domain()` - Auto-detection logic (`sys.stdin.isatty()`)
- `CLISession.mode` - Mode property (None = auto-detect, 'tty'/'markdown' = explicit)
- `AdapterFactory` - TTY vs Markdown adapter creation (JSON is explicit only)

### 16. Load Workspace Context ✅
**Test File:** `test_initialize_cli_session.py::TestLoadWorkspaceContext`

**Scenarios:**
- `test_cli_loads_workspace_directory_on_launch` - Workspace loading ✅
- `test_cli_loads_story_graph_when_available` - Story graph loading (skipped)

**Impacted Domain Classes:**
- `CLISession.__init__()` - Workspace directory storage
- `Bot` - Workspace context access
- `StoryGraph` - Story graph loading (if implemented)

---

## Key Changes That May Break Tests

### 1. Non-Workflow Actions (Rules)
- **Change:** Added automatic 'rules' action to all behaviors
- **Impact:** `TTYActions.names` now includes non-workflow actions
- **Tests Affected:** Any test checking action lists

### 2. Action Execution for Non-Workflow Actions
- **Change:** Non-workflow actions now call `execute()` instead of `get_instructions()`
- **Impact:** `CLISession._handle_action_shortcut()` behavior changed
- **Tests Affected:** Tests executing non-workflow actions

### 3. Instructions Property vs Method
- **Change:** Instructions handling refactored
- **Impact:** `Action.get_instructions()` vs `Action.instructions` property
- **Tests Affected:** All instruction-related tests

### 4. TTY Formatting Changes
- **Change:** Bold formatting, emoji additions, formatting cleanup
- **Impact:** Output format changed
- **Tests Affected:** Tests checking exact output strings

### 5. Mode Detection and Selection
- **Change:** Added `mode` parameter to `CLISession.__init__()` for explicit mode setting
- **Impact:** 
  - Auto-detection: TTY for interactive (`sys.stdin.isatty() == True`), Markdown for piped (`sys.stdin.isatty() == False`)
  - Explicit mode: Can set `mode='json'` for web views, `mode='markdown'` or `mode='tty'` to override auto-detection
- **Tests Affected:** Tests checking adapter selection (now use `mode` parameter instead of patching)

---

## Summary by Domain Class

### CLISession
**Impacted by:** All scenarios (17 test classes)
- `execute_command()` - Core routing logic
- `_parse_command()` - Command parsing
- `_route_to_behavior_action()` - Dot notation routing
- `_handle_action_shortcut()` - Action shortcuts (including non-workflow)
- `_get_adapter_for_domain()` - Adapter selection

### TTYActions
**Impacted by:** Status display, action listing (5+ scenarios)
- `names` property - Now includes non-workflow actions (rules)
- Action list formatting - Bold current action

### TTYBehaviors
**Impacted by:** Status display, navigation (5+ scenarios)
- `names` property - Now shows all behaviors with pipes, current bolded

### Actions
**Impacted by:** Navigation, execution, non-workflow actions (10+ scenarios)
- `_non_workflow_actions` - New list for independent actions
- `find_by_name()` - Finds both workflow and non-workflow actions
- `navigate_to()` - Skips navigation for non-workflow actions

### Action (RulesAction)
**Impacted by:** Rules action execution (2+ scenarios)
- `execute()` - Now called for non-workflow actions
- `do_execute()` - Loads rules and adds to instructions
- `_add_rules_list_to_display()` - Shows rule names with file paths

### Instructions
**Impacted by:** Instruction display, rules action (5+ scenarios)
- `display_content` - Rules list and digest
- `to_dict()` / `from_dict()` - Serialization for rules action

### TTYAdapter
**Impacted by:** All formatting scenarios (15+ scenarios)
- `add_bold()` - New bold formatting method
- Formatting changes (no colors, no `##`, bold headers)

---

## Next Steps

1. **Run all CLI tests** to identify failures:
   ```bash
   pytest agile_bot/test/test_*cli*.py -v
   ```

2. **For each failing test:**
   - Identify which domain class change caused the failure
   - Check if failure is due to:
     - New behavior (non-workflow actions, formatting changes) → Update test
     - Regression (broken functionality) → Fix code
     - Missing feature → Implement or mark as expected failure

3. **Prioritize fixes by:**
   - **P0:** Core functionality (navigation, execution, instructions)
   - **P1:** User-facing features (help, status display, rules action)
   - **P2:** Edge cases (error handling, mode detection, formatting)

4. **Test categories to check:**
   - Action list includes 'rules' (TTYActions.names)
   - Non-workflow actions execute correctly (rules action)
   - Formatting changes (bold, no colors, emoji)
   - Behavior/action lists show all items with pipes
   - Current items are bolded
   - Instructions property vs method consistency
