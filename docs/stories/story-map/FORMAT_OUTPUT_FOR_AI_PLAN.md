# Format Output for AI - Implementation Plan

## Story Overview

**Story Name:** Format Output for AI  
**Sub-Epic:** Generate REPL CLI  
**Epic:** Build Agile Bot  
**Priority:** High  

## Problem Statement

The new REPL CLI outputs plain text formatting (`[*]`, `[x]`, `[ ]` markers) to both human terminals and AI agents. When AI agents invoke the CLI via piped mode (`echo 'cmd' | python repl_main.py`), they should receive rich Markdown formatting for better parsing and display in chat interfaces.

The system already detects TTY vs piped mode via `sys.stdin.isatty()`, but doesn't use this to change output formatting.

## Acceptance Criteria

Following **behavioral_ac_at_story_level**, **stories_have_4_to_9_acceptance_criteria**, and **use_verb_noun_format_for_story_elements** rules:

1. WHEN REPL session starts THEN session detects TTY mode AND session creates appropriate formatter via factory

2. WHEN TTY mode is detected THEN factory creates terminal formatter AND formatter uses plain text markers AND formatter uses dash separators

3. WHEN piped mode is detected THEN factory creates markdown formatter AND formatter uses emoji markers AND formatter uses markdown separators AND formatter uses markdown headings

4. WHEN formatter is created THEN session injects formatter into REPLStatus

5. WHEN REPLStatus builds hierarchical display THEN status uses formatter for section separators AND status uses formatter for status markers AND status uses formatter for list items


7. WHEN terminal mode displays output THEN output matches current plain text format exactly

8. WHEN piped mode displays output THEN output contains markdown formatting AND output uses rich status markers

9. **WHEN scope display is returned THEN output includes explicit AI instruction to print scope section AND instruction appears before scope content**

10. **WHEN instructions are wrapped with context header THEN output includes explicit AI instruction to print CLI status section AND instruction appears before CLI status content**

11. **WHEN context header is generated THEN output includes reminder at end listing what sections must be displayed**

## Domain Concepts

Following **verb_noun_format**, **active_business_and_behavioral_language**, and **outcome_oriented_language** rules:

- **OutputFormatter** - Formats output text for display
- **TerminalFormatter** - Formats output for terminal display
- **MarkdownFormatter** - Formats output for markdown display
- **FormatterFactory** - Creates formatter based on mode
- **REPLSession** - Manages REPL session and formatter creation
- **REPLStatus** - Displays status using formatter

## Scenarios

Following **given_describes_state_not_actions**, **write_plain_english_scenarios**, and **scenarios_cover_all_cases** rules:

### Background
- Given REPL CLI is initialized
- And bot has behaviors and actions configured

### Scenario 1: Terminal mode uses plain text formatting
- Given user runs REPL in terminal
- When REPL displays status
- Then status uses plain text markers
- And status uses dash separators
- And status uses space indentation

### Scenario 2: Piped mode uses markdown formatting
- Given AI agent pipes command to REPL
- When REPL displays status
- Then status uses emoji markers
- And status uses markdown headings
- And status uses markdown separators
- And status uses markdown lists

### Scenario 3: Formatter created at session initialization
- Given REPL session is starting
- When session detects TTY mode
- Then session creates terminal formatter
- And session injects formatter into status

### Scenario 4: Formatter created for piped mode
- Given REPL session is starting
- When session detects piped mode
- Then session creates markdown formatter
- And session injects formatter into status

### Scenario 5: Status uses formatter for all output
- Given REPLStatus has formatter injected
- When status builds hierarchical display
- Then status uses formatter for separators
- And status uses formatter for status markers
- And status uses formatter for list items

### Scenario 6: Scope display includes explicit AI instruction
- Given scope is set in bot state
- When CLI action formats instructions with scope
- Then output includes "AI AGENT CRITICAL INSTRUCTION" header
- And output includes "You MUST print the SCOPE section" text
- And instruction appears before scope content

### Scenario 8: Context header includes explicit AI instruction
- Given REPL command wraps instructions with context header
- When command builds output response
- Then output includes "AI AGENT CRITICAL INSTRUCTION" header
- And output includes "You MUST display the CLI STATUS section" text
- And instruction appears before CLI status content

### Scenario 8: Context header includes reminder at end
- Given context header is generated
- When header is appended to instructions
- Then header includes "AI AGENT: The above CLI STATUS section contains" text
- And header lists what sections are included
- And header includes "You MUST display this entire section" text

## Test Structure

Following **use_class_based_organization**, **pytest_bdd_orchestrator_pattern**, and **use_given_when_then_helpers** rules:

### File: `test/repl_cli/test_explicit_ai_instructions.py`

```python
class TestScopeDisplayInstructions:
    """Test explicit AI instructions for scope display"""
    
    def test_scope_display_includes_ai_instruction(self):
        # Given scope is set and CLI scope is created
        # When to_formatted_display is called
        # Then output includes "AI AGENT CRITICAL INSTRUCTION"
        # And output includes "You MUST print the SCOPE section"
        pass
    
    def test_scope_instruction_appears_before_content(self):
        # Given scope display is formatted
        # When output is generated
        # Then instruction header appears before scope content
        pass

class TestContextHeaderInstructions:
    """Test explicit AI instructions for context header"""
    
    def test_context_header_wrapper_includes_ai_instruction(self):
        # Given instructions are wrapped with context header
        # When _wrap_with_context_header is called
        # Then output includes "AI AGENT CRITICAL INSTRUCTION"
        # And output includes "You MUST display the CLI STATUS section"
        pass
    
    def test_context_header_instruction_appears_before_status(self):
        # Given context header is wrapped
        # When output is generated
        # Then instruction appears before CLI status content
        pass
    
    def test_context_header_includes_end_reminder(self):
        # Given context header is generated
        # When get_context_header_for_ai is called
        # Then output includes "AI AGENT: The above CLI STATUS section contains"
        # And output lists sections included
        # And output includes "You MUST display this entire section"
        pass

class TestInstructionsWithScopeAndHeader:
    """Integration test for instructions with scope and header"""
    
    def test_full_output_includes_all_instructions(self):
        # Given scope is set and action has instructions
        # When instructions command is executed
        # Then output includes scope AI instruction
        # And output includes scope content
        # And output includes action instructions
        # And output includes context header AI instruction
        # And output includes CLI status
        pass
```

### File: `test/repl_cli/formatters/test_terminal_formatter.py`

```python
class TestTerminalFormatter:
    """Story: Format Output for AI - Terminal Formatter"""
    
    def test_terminal_formatter_returns_plain_text_heading(self):
        # Given
        formatter = given_terminal_formatter()
        # When
        result = when_format_heading(formatter, "Test Heading", level=2)
        # Then
        then_result_is_plain_text(result, "Test Heading")
    
    def test_terminal_formatter_uses_bracket_status_markers(self):
        # Given
        formatter = given_terminal_formatter()
        # When
        current_marker = when_format_status_marker(formatter, is_current=True, is_completed=False)
        completed_marker = when_format_status_marker(formatter, is_current=False, is_completed=True)
        pending_marker = when_format_status_marker(formatter, is_current=False, is_completed=False)
        # Then
        then_marker_equals(current_marker, "[*]")
        then_marker_equals(completed_marker, "[x]")
        then_marker_equals(pending_marker, "[ ]")
    
    def test_terminal_formatter_uses_dash_separator(self):
        # Given
        formatter = given_terminal_formatter()
        # When
        separator = when_format_section_separator(formatter)
        # Then
        then_separator_is_dashes(separator, length=60)
```

### File: `test/repl_cli/formatters/test_markdown_formatter.py`

```python
class TestMarkdownFormatter:
    """Story: Format Output for AI - Markdown Formatter"""
    
    def test_markdown_formatter_returns_markdown_heading(self):
        # Given
        formatter = given_markdown_formatter()
        # When
        result = when_format_heading(formatter, "Test Heading", level=2)
        # Then
        then_result_is_markdown_heading(result, "## Test Heading")
    
    def test_markdown_formatter_uses_emoji_status_markers(self):
        # Given
        formatter = given_markdown_formatter()
        # When
        current_marker = when_format_status_marker(formatter, is_current=True, is_completed=False)
        completed_marker = when_format_status_marker(formatter, is_current=False, is_completed=True)
        pending_marker = when_format_status_marker(formatter, is_current=False, is_completed=False)
        # Then
        then_marker_is_emoji(current_marker, "▶️")
        then_marker_is_emoji(completed_marker, "✅")
        then_marker_is_emoji(pending_marker, "⬜")
    
    def test_markdown_formatter_uses_markdown_separator(self):
        # Given
        formatter = given_markdown_formatter()
        # When
        separator = when_format_section_separator(formatter)
        # Then
        then_separator_is_markdown(separator, "---")
```

### File: `test/repl_cli/formatters/test_formatter_factory.py`

```python
class TestFormatterFactory:
    """Story: Format Output for AI - Formatter Factory"""
    
    def test_factory_creates_terminal_formatter_when_tty_detected(self):
        # Given
        tty_detected = True
        # When
        formatter = when_factory_creates_formatter(tty_detected)
        # Then
        then_formatter_is_terminal_formatter(formatter)
    
    def test_factory_creates_markdown_formatter_when_piped_mode(self):
        # Given
        tty_detected = False
        # When
        formatter = when_factory_creates_formatter(tty_detected)
        # Then
        then_formatter_is_markdown_formatter(formatter)
```

### File: `test/repl_cli/test_repl_session_formatter_integration.py`

```python
class TestREPLSessionFormatterIntegration:
    """Story: Format Output for AI - REPL Session Integration"""
    
    def test_repl_session_creates_formatter_at_initialization(self):
        # Given
        bot = given_bot_with_behaviors()
        workspace = given_workspace_directory()
        # When
        session = when_repl_session_initialized(bot, workspace)
        # Then
        then_session_has_formatter(session)
    
    def test_repl_session_injects_formatter_into_status(self):
        # Given
        bot = given_bot_with_behaviors()
        workspace = given_workspace_directory()
        # When
        session = when_repl_session_initialized(bot, workspace)
        # Then
        then_status_has_formatter(session.status, session.formatter)
```

### File: `test/repl_cli/test_repl_status_uses_formatter.py`

```python
class TestREPLStatusUsesFormatter:
    """Story: Format Output for AI - REPL Status Uses Formatter"""
    
    def test_repl_status_uses_formatter_for_hierarchical_display(self):
        # Given
        formatter = given_mock_formatter()
        bot = given_bot_with_behaviors()
        status = given_repl_status_with_formatter(bot, formatter)
        # When
        output = when_status_builds_hierarchical_display(status)
        # Then
        then_formatter_methods_were_called(formatter, ['section_separator', 'status_marker', 'list_item'])
```

## Production Code Structure

Following **use_explicit_dependencies**, **keep_classes_small_with_single_responsibility**, and **use_domain_language** rules:

### File: `src/repl_cli/formatters/output_formatter.py`

```python
from abc import ABC, abstractmethod

class OutputFormatter(ABC):
    """Formats output text for display."""
    
    @abstractmethod
    def heading(self, text: str, level: int = 1) -> str:
        """Format heading at specified level."""
        pass
    
    @abstractmethod
    def list_item(self, text: str, indent_level: int = 0, marker: str = None) -> str:
        """Format list item with indentation."""
        pass
    
    @abstractmethod
    def section_separator(self) -> str:
        """Format section divider."""
        pass
    
    @abstractmethod
    def status_marker(self, is_current: bool, is_completed: bool) -> str:
        """Format status indicator."""
        pass
    
    @abstractmethod
    def bold(self, text: str) -> str:
        """Format bold text."""
        pass
    
    @abstractmethod
    def code_inline(self, text: str) -> str:
        """Format inline code."""
        pass
```

### File: `src/repl_cli/formatters/terminal_formatter.py`

```python
from agile_bot.bots.base_bot.src.repl_cli.formatters.output_formatter import OutputFormatter

class TerminalFormatter(OutputFormatter):
    """Formats output for terminal display using plain text."""
    
    def heading(self, text: str, level: int = 1) -> str:
        return text
    
    def list_item(self, text: str, indent_level: int = 0, marker: str = None) -> str:
        indent = "  " * indent_level
        return f"{indent}{text}"
    
    def section_separator(self) -> str:
        return "-" * 60
    
    def status_marker(self, is_current: bool, is_completed: bool) -> str:
        if is_completed:
            return "[x]"
        elif is_current:
            return "[*]"
        return "[ ]"
    
    def bold(self, text: str) -> str:
        return text
    
    def code_inline(self, text: str) -> str:
        return text
```

### File: `src/repl_cli/formatters/markdown_formatter.py`

```python
from agile_bot.bots.base_bot.src.repl_cli.formatters.output_formatter import OutputFormatter

class MarkdownFormatter(OutputFormatter):
    """Formats output for markdown display with rich formatting."""
    
    def heading(self, text: str, level: int = 1) -> str:
        return f"{'#' * level} {text}"
    
    def list_item(self, text: str, indent_level: int = 0, marker: str = None) -> str:
        indent = "  " * indent_level
        prefix = marker if marker else "-"
        return f"{indent}{prefix} {text}"
    
    def section_separator(self) -> str:
        return "---"
    
    def status_marker(self, is_current: bool, is_completed: bool) -> str:
        if is_completed:
            return "✅"
        elif is_current:
            return "▶️"
        return "⬜"
    
    def bold(self, text: str) -> str:
        return f"**{text}**"
    
    def code_inline(self, text: str) -> str:
        return f"`{text}`"
```

### File: `src/repl_cli/formatters/formatter_factory.py`

```python
from agile_bot.bots.base_bot.src.repl_cli.formatters.output_formatter import OutputFormatter
from agile_bot.bots.base_bot.src.repl_cli.formatters.terminal_formatter import TerminalFormatter
from agile_bot.bots.base_bot.src.repl_cli.formatters.markdown_formatter import MarkdownFormatter

class FormatterFactory:
    """Creates formatter based on TTY detection."""
    
    @staticmethod
    def create(tty_detected: bool) -> OutputFormatter:
        if tty_detected:
            return TerminalFormatter()
        else:
            return MarkdownFormatter()
```

### Modifications to `src/repl_cli/repl_session.py`

```python
# Add import
from agile_bot.bots.base_bot.src.repl_cli.formatters.formatter_factory import FormatterFactory

class REPLSession:
    def __init__(self, bot, workspace_directory: Path):
        self.cli_bot = CLIBot(bot, self)
        self.workspace_directory = Path(workspace_directory)
        
        # Detect TTY and create formatter
        tty_result = self.detect_tty()
        self.formatter = FormatterFactory.create(tty_result.tty_detected)
        
        # Inject formatter into components
        self.help = REPLHelp(bot)
        self.status = REPLStatus(self.cli_bot, self, self.formatter)
        self._commands = register_commands(self)
        self._dot_notation_handler = DotNotationCommand(self)
```

### Modifications to `src/repl_cli/repl_status.py`

```python
from agile_bot.bots.base_bot.src.repl_cli.formatters.output_formatter import OutputFormatter

class REPLStatus:
    def __init__(self, bot, state_provider, formatter: OutputFormatter):
        self.bot = bot
        self.state = state_provider
        self.formatter = formatter
    
    @property
    def hierarchical_status(self) -> str:
        lines = []
        
        # Use formatter for separator
        lines.append(self.formatter.section_separator())
        
        # ... existing logic ...
        
        for behavior in self.bot.behaviors:
            # Use formatter for status marker
            marker = self.formatter.status_marker(is_current, is_completed)
            # Use formatter for list item
            lines.append(self.formatter.list_item(f"{marker} {b_name}", indent_level=0))
            
            # Actions
            for action in behavior.actions:
                a_marker = self.formatter.status_marker(is_current_action, is_completed_action)
                lines.append(self.formatter.list_item(f"{a_marker} {a_name}", indent_level=1))
        
        lines.append("")
        lines.append(self.formatter.section_separator())
        
        return "\n".join(lines)
```

## Implementation Phases

### Phase 1: Add Explicit AI Instructions for Formatted Sections (1 hour)
**CRITICAL:** AI agents often skip formatted sections unless explicitly told to print them.

**Problem:** When AI agents receive REPL output with formatted sections (scope filters, CLI status, hierarchical displays), they frequently:
- Summarize instead of displaying verbatim
- Skip "boring" technical sections
- Focus only on action instructions and ignore context

**Solution:** Add explicit instructions before and after formatted sections telling the AI it MUST display them exactly as provided. This ensures users see:
- Current scope filter (what they're working on)
- Current progress and workflow state
- Available commands and navigation options

**Locations to Update:**
1. `cli_scope.py` - Scope display formatting (prepends to instructions)
2. `cli_action.py` - Scope integration point (where scope is added)
3. `repl_command.py` - Context header wrapper (wraps all instruction output)
4. `repl_session.py` - Context header generation (generates CLI status)

#### 1.1 Update `cli_scope.py` - Add AI Instructions to Scope Display
**Location:** `agile_bot/bots/base_bot/src/repl_cli/cli_scope.py`  
**Method:** `to_formatted_display()`  
**Current Code:**
```python
def to_formatted_display(self) -> str:
    """Render scope with CLI-specific formatting (warnings, separators)."""
    lines = []
    
    lines.append("-" * 60)
    lines.append("⚠️  SCOPE FILTER ACTIVE - Work ONLY on the following scope:")
    lines.append("-" * 60)
    
    # Get plain scope display lines from domain object
    scope_lines = self._scope.to_display_lines(self._workspace_directory)
    lines.extend(scope_lines)
    
    lines.append("")
    lines.append("⚠️  DO NOT work on all files or the entire story graph")
    lines.append("⚠️  Focus EXCLUSIVELY on the items listed above")
    lines.append("-" * 60)
    lines.append("")
    
    return "\n".join(lines)
```

**Updated Code:**
```python
def to_formatted_display(self) -> str:
    """Render scope with CLI-specific formatting (warnings, separators, and AI instructions)."""
    lines = []
    
    # Add explicit AI instruction at the very top
    lines.append("")
    lines.append("=" * 60)
    lines.append("AI AGENT CRITICAL INSTRUCTION:")
    lines.append("You MUST print the SCOPE section below EXACTLY as shown.")
    lines.append("Do NOT summarize, skip, or modify this section.")
    lines.append("=" * 60)
    lines.append("")
    
    lines.append("-" * 60)
    lines.append("⚠️  SCOPE FILTER ACTIVE - Work ONLY on the following scope:")
    lines.append("-" * 60)
    
    # Get plain scope display lines from domain object
    scope_lines = self._scope.to_display_lines(self._workspace_directory)
    lines.extend(scope_lines)
    
    lines.append("")
    lines.append("⚠️  DO NOT work on all files or the entire story graph")
    lines.append("⚠️  Focus EXCLUSIVELY on the items listed above")
    lines.append("-" * 60)
    lines.append("")
    
    return "\n".join(lines)
```

**Note:** CLI layer handles ALL formatting including AI instructions. Domain `Scope` only provides plain data via `to_display_lines()`.

#### 1.2 Verify `cli_action.py` - Scope Integration (No Changes Needed)
**Location:** `agile_bot/bots/base_bot/src/repl_cli/cli_bot/cli_actions/cli_action.py`  
**Method:** `instructions()`  
**Current Code (Already Correct):**
```python
def instructions(self, args: str = "") -> str:
    try:
        context = self._parse_args_to_context(args)
        result = self._action.get_instructions(context)
        formatted = self._format_result(result)
        
        # Prepend scope display if scope is set (CLI layer adds formatting)
        instructions_obj = self._action.instructions
        if instructions_obj.scope:
            cli_scope = CLIScope(instructions_obj.scope, self._action.behavior.bot_paths.workspace_directory)
            scope_display = cli_scope.to_formatted_display()  # Already includes AI instructions
            formatted = scope_display + formatted
        
        return formatted
    except Exception as e:
        return f"Error getting instructions: {str(e)}"
```

**Explanation:** The `cli_action.py` just checks if scope exists in the `Instructions` object, wraps it in `CLIScope` for formatting, and prepends the result. All formatting logic (including AI instructions) is handled by `CLIScope.to_formatted_display()`. This follows proper separation: domain provides data, CLI provides formatting.

#### 1.3 Update `repl_command.py` - Context Header Wrapper
**Location:** `agile_bot/bots/base_bot/src/repl_cli/repl_commands/repl_command.py`  
**Method:** `_wrap_with_context_header()`  
**Add instruction before header:**
```python
def _wrap_with_context_header(self, content: str, response_msg: str) -> REPLCommandResponse:
    header = self.session.get_context_header_for_ai()
    
    ai_instruction = "\n".join([
        "",
        "=" * 60,
        "AI AGENT CRITICAL INSTRUCTION:",
        "You MUST display the CLI STATUS section below EXACTLY as shown.",
        "This includes: Bot Path, Work Path, Scope, Progress, and Commands.",
        "Do NOT summarize, skip, or modify this section.",
        "=" * 60,
        ""
    ])
    
    output = "\n".join([
        content,
        "",
        ai_instruction,
        header
    ])
    
    return REPLCommandResponse(
        output=output,
        response=response_msg,
        status="success"
    )
```

#### 1.4 Update `repl_session.py` - Context Header Generation
**Location:** `agile_bot/bots/base_bot/src/repl_cli/repl_session.py`  
**Method:** `get_context_header_for_ai()`  
**Add at end before return:**
```python
lines.append("")
lines.append("AI AGENT: The above CLI STATUS section contains:")
lines.append("  - Current scope filter (if set)")
lines.append("  - Current progress in workflow")
lines.append("  - Available commands")
lines.append("You MUST display this entire section in your response to the user exactly as you see it.")
```

### Phase 2: Create Formatter Infrastructure (2 hours)
1. Create `formatters/` directory
2. Implement `OutputFormatter` abstract base class
3. Implement `TerminalFormatter` 
4. Implement `MarkdownFormatter`
5. Implement `FormatterFactory`
6. Write unit tests for all formatters

### Phase 3: Integrate with REPLSession (1 hour)
1. Modify `REPLSession.__init__` to create formatter
2. Pass formatter to `REPLStatus` constructor
3. Update `REPLStatus.__init__` signature

### Phase 4: Update REPLStatus (1 hour)
1. Replace direct string formatting in `hierarchical_status()`
2. Use `formatter.section_separator()`
3. Use `formatter.status_marker()`
4. Use `formatter.list_item()`

### Phase 5: Testing (2 hours)
1. Test TerminalFormatter output matches current
2. Test MarkdownFormatter produces valid markdown
3. Integration test with mocked TTY detection
4. Manual test with actual pipe
5. Test explicit AI instructions are present in output

### Phase 6: Documentation (30 minutes)
1. NO docstrings! or comments in classes
2. Update REPL documentation
3. Document explicit AI instruction pattern

## Estimated Effort

**Total: 7.5 hours**

**Note:** Cursor command generation is now its own separate story: "Generate Cursor Commands for REPL"

## Rules Applied

### Shape Rules
- ✅ verb_noun_format: "Format Output", "Create Formatter", "Display Status"
- ✅ active_business_and_behavioral_language: "Formatter formats output", "Session creates formatter"
- ✅ outcome_oriented_language: Focus on formatted output, not "showing" or "displaying"
- ✅ valuable: Delivers independent value - AI gets better formatted output
- ✅ small_and_testable: Can be tested independently with clear acceptance criteria

### Scenarios Rules
- ✅ given_describes_state_not_actions: "Given REPL is initialized" (state), not "Given REPL initializes" (action)
- ✅ write_plain_english_scenarios: No variables or placeholders in scenarios
- ✅ scenarios_cover_all_cases: Happy path (terminal), edge case (piped), integration

### Tests Rules
- ✅ use_class_based_organization: File=sub-epic, Class=story, Method=scenario
- ✅ pytest_bdd_orchestrator_pattern: Test shows Given-When-Then flow
- ✅ use_given_when_then_helpers: Reusable helper functions
- ✅ call_production_code_directly: No mocking of business logic
- ✅ cover_all_behavior_paths: Normal, edge, and failure scenarios

### Code Rules
- ✅ use_explicit_dependencies: Formatter injected via constructor
- ✅ keep_classes_small_with_single_responsibility: Each formatter does one thing
- ✅ use_domain_language: OutputFormatter, TerminalFormatter, not GenericFormatter
- ✅ eliminate_duplication: Factory pattern eliminates if-else duplication
- ✅ use_clear_function_parameters: 0-2 parameters, typed objects

## Success Criteria

- [ ] Terminal mode produces identical output to current version
- [ ] Piped mode produces rich Markdown output
- [ ] All existing tests pass
- [ ] New tests achieve 80%+ coverage
- [ ] Explicit AI instructions present in formatted output
- [ ] No breaking changes to CLI commands or behavior

# 📝 Generate Cursor Commands for REPL

**Navigation:** [📋 Story Map](../../../story-map-outline.drawio) | [⚙️ Feature Overview](../../../../README.md)

**Epic:** Build Agile Bots
**Feature:** Generate REPL CLI
**User:** Generator
**Sequential Order:** 4
**Story Type:** user

## Story Description

Generate Cursor Command Files for REPL CLI that use piped input syntax (`echo 'command' | python repl_main.py`). Commands provide shortcuts for navigating behaviors, actions, and executing REPL operations through Cursor's command palette.

## Key Design Principles

1. **Emulate Cursor Syntax**: Follow Cursor's command file format as closely as possible for consistency with existing CLI commands
2. **Orchestrator-Visitor Pattern**: Use the existing orchestrator-visitor pattern to traverse bot structure and generate commands
3. **Piped Input Format**: All REPL commands must use `echo 'command' | python repl_main.py` syntax (NOT command-line arguments)
4. **Dot Notation Support**: Generate shortcuts using REPL's dot notation (e.g., `behavior.action.operation`)

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** generator creates REPLCursorCommandVisitor,
  **then** visitor follows orchestrator-visitor pattern from existing CLI command generation

- **When** visitor generates base commands,
  **then** visitor creates `<bot-name>-repl.md` with piped syntax: `echo 'status' | python repl_main.py`

- **When** visitor generates behavior shortcuts,
  **then** visitor creates `<bot-name>-repl-<behavior>.md` for each behavior with piped syntax: `echo '<behavior>' | python repl_main.py`

- **When** visitor generates action shortcuts,
  **then** visitor creates `<bot-name>-repl-<behavior>-<action>.md` for each action with piped dot notation: `echo '<behavior>.<action>.instructions' | python repl_main.py`

- **When** visitor generates operation shortcuts,
  **then** visitor includes instructions, submit, and confirm operations for each action

- **When** visitor generates help shortcuts,
  **then** visitor creates status, help, next, back, and exit commands

- **When** visitor completes generation,
  **then** visitor removes obsolete command files for behaviors/actions that no longer exist

- **When** generator updates bot registry,
  **then** generator adds `repl_path` field pointing to `repl_main.py` relative to workspace root

## Implementation Notes

### Cursor Command File Format

Commands must follow Cursor's syntax for placeholders and parameter prompts:
- `${1:parameter_name}` - First parameter with prompt
- `${2:+ }` - Optional space before second parameter
- `${2:param}` - Second parameter with prompt
- Multi-line commands with instructions for AI

### REPL Command Patterns

```markdown
# Base Status Command
echo 'status' | python agile_bot/bots/base_bot/src/repl_cli/repl_main.py

# Navigate to Behavior
echo '${1:behavior}' | python agile_bot/bots/base_bot/src/repl_cli/repl_main.py

# Navigate to Action
echo '${1:behavior}.${2:action}' | python agile_bot/bots/base_bot/src/repl_cli/repl_main.py

# Execute Operation
echo '${1:behavior}.${2:action}.${3|instructions,submit,confirm|}' | python agile_bot/bots/base_bot/src/repl_cli/repl_main.py

# With Scope Parameter
echo '${1:behavior}.${2:action}.submit --scope "${3:story_name}"' | python agile_bot/bots/base_bot/src/repl_cli/repl_main.py
```

## Scenarios

### Scenario: Generate base REPL command file

**Steps:**
```gherkin
Given: REPLCursorCommandVisitor is initialized
And: commands directory path is .cursor/commands/
And: REPL script path is agile_bot/bots/base_bot/src/repl_cli/repl_main.py
When: visitor generates base commands
Then: visitor creates <bot-name>-repl.md command file
And: command file contains "echo 'status' | python repl_main.py"
And: command file contains "echo 'help' | python repl_main.py"
And: command file contains "echo 'next' | python repl_main.py"
And: command file contains "echo 'back' | python repl_main.py"
And: command file contains "echo 'exit' | python repl_main.py"
```

### Scenario: Generate behavior navigation shortcuts

**Steps:**
```gherkin
Given: bot has behaviors ["shape", "discovery", "exploration"]
When: visitor generates behavior shortcuts
Then: visitor creates story_bot-repl-shape.md
And: visitor creates story_bot-repl-discovery.md
And: visitor creates story_bot-repl-exploration.md
And: each command file contains "echo '<behavior>' | python repl_main.py"
And: each command file lists available actions for that behavior
```

### Scenario: Generate action operation shortcuts

**Steps:**
```gherkin
Given: "discovery" behavior has action "build"
When: visitor generates action shortcuts
Then: visitor creates story_bot-repl-discovery-build.md
And: command file contains "echo 'discovery.build.instructions' | python repl_main.py"
And: command file contains "echo 'discovery.build.submit' | python repl_main.py"
And: command file contains "echo 'discovery.build.confirm' | python repl_main.py"
And: command file includes scope parameter example: --scope "${1:story_name}"
```

### Scenario: Generate cursor commands creates directory if missing

**Steps:**
```gherkin
Given: REPLCursorCommandVisitor is initialized
And: .cursor/commands/ directory does NOT exist
When: visitor generates commands
Then: visitor creates .cursor/commands/ directory
And: visitor creates all REPL command files
```

### Scenario: Remove obsolete command files when behavior removed

**Steps:**
```gherkin
Given: bot previously had behavior "old_behavior"
And: obsolete command file exists: story_bot-repl-old_behavior.md
And: bot no longer has behavior "old_behavior"
When: visitor generates commands
Then: visitor creates new command files for current behaviors
And: visitor removes story_bot-repl-old_behavior.md
And: visitor removes all story_bot-repl-old_behavior-*.md files
```

### Scenario: Update bot registry with REPL path

**Steps:**
```gherkin
Given: generator has created REPL command files
When: generator updates bot registry
Then: generator adds "repl_path" field to bot registry entry
And: repl_path points to "agile_bot/bots/base_bot/src/repl_cli/repl_main.py"
And: registry entry includes existing trigger_patterns
And: registry entry includes existing cli_path
```

## Technical Design

### Class Structure

```python
class REPLCursorCommandVisitor(Visitor):
    """Visitor that generates Cursor command files for REPL CLI using piped syntax."""
    
    def __init__(self, workspace_root: Path, repl_script_path: Path, bot=None):
        super().__init__(bot=bot)
        self.workspace_root = workspace_root
        self.repl_script_path = repl_script_path
        self.commands_dir: Optional[Path] = None
        self.python_command: Optional[str] = None
        self.commands: Dict[str, Path] = {}
        self.current_command_files: Set[Path] = set()
    
    def visit_header(self, bot_name: str) -> None:
        # Create .cursor/commands/ directory
        # Track existing command files for cleanup
        # Generate base REPL commands (status, help, next, back, exit)
        pass
    
    def visit_behavior(self, context: BehaviorHelpContext) -> None:
        # Generate navigation shortcut for behavior
        # Create <bot-name>-repl-<behavior>.md
        pass
    
    def visit_action(self, context: ActionHelpContext) -> None:
        # Generate operation shortcuts for action
        # Create <bot-name>-repl-<behavior>-<action>.md
        # Include instructions, submit, confirm operations
        pass
    
    def visit_footer(self) -> None:
        # Remove obsolete command files
        pass
    
    def get_commands(self) -> Dict[str, Path]:
        # Return mapping of command names to file paths
        pass
```

### Command File Templates

#### Base REPL Command (`story_bot-repl.md`)
```markdown
# story_bot-repl - REPL Status and Navigation

## Status
echo 'status' | python agile_bot/bots/base_bot/src/repl_cli/repl_main.py

## Help
echo 'help' | python agile_bot/bots/base_bot/src/repl_cli/repl_main.py

## Navigation
echo 'next' | python agile_bot/bots/base_bot/src/repl_cli/repl_main.py
echo 'back' | python agile_bot/bots/base_bot/src/repl_cli/repl_main.py

## Exit
echo 'exit' | python agile_bot/bots/base_bot/src/repl_cli/repl_main.py
```

#### Behavior Command (`story_bot-repl-discovery.md`)
```markdown
# story_bot-repl-discovery - Navigate to Discovery Behavior

## Navigate to Behavior
echo 'discovery' | python agile_bot/bots/base_bot/src/repl_cli/repl_main.py

## Navigate to Specific Action
echo 'discovery.${1|build,validate,clarify,strategy|}' | python agile_bot/bots/base_bot/src/repl_cli/repl_main.py

## Available Actions:
- build - Build knowledge graph
- validate - Validate requirements
- clarify - Clarify ambiguities
- strategy - Define strategy
```

#### Action Command (`story_bot-repl-discovery-build.md`)
```markdown
# story_bot-repl-discovery-build - Execute Discovery Build Action

## Get Instructions
echo 'discovery.build.instructions' | python agile_bot/bots/base_bot/src/repl_cli/repl_main.py

## Submit Work
echo 'discovery.build.submit${1:+ }${1:--scope "${2:story_name}"}' | python agile_bot/bots/base_bot/src/repl_cli/repl_main.py

## Confirm and Advance
echo 'discovery.build.confirm' | python agile_bot/bots/base_bot/src/repl_cli/repl_main.py

## Display Instructions
After running 'instructions', the output will include formatted instructions and CLI status.
AI AGENT: You MUST display all sections including:
- Scope filter (if set)
- Current progress
- Available commands
```

## Implementation Steps

### Phase 1: Create REPLCursorCommandVisitor (2 hours)
1. Create `repl_cli/cursor_command_visitor.py`
2. Implement `REPLCursorCommandVisitor` class following `CursorCommandFileVisitor` pattern
3. Implement `visit_header()` for base commands
4. Implement `visit_behavior()` for behavior shortcuts
5. Implement `visit_action()` for action operation shortcuts
6. Implement `visit_footer()` for cleanup
7. Implement command file generation with piped syntax

### Phase 2: Integrate with Generator (1 hour)
1. Create `repl_cli/repl_cursor_command_generator.py`
2. Implement `REPLCursorCommandGenerator` class
3. Wire up orchestrator with `REPLCursorCommandVisitor`
4. Implement bot registry update with `repl_path` field

### Phase 3: Testing (2 hours)
1. Test base command generation
2. Test behavior shortcut generation
3. Test action operation shortcut generation
4. Test obsolete file cleanup
5. Test bot registry update
6. Manual test in Cursor command palette

### Phase 4: Documentation (30 minutes)
1. Document REPL cursor command generation
2. Document piped syntax patterns
3. Update bot registry schema documentation

## Estimated Effort

**Total: 5.5 hours**

## Related Files to Reference

### Existing CLI Command Generation
- `agile_bot/bots/base_bot/src/cli/cursor_command_generator.py` - Main generator
- `agile_bot/bots/base_bot/src/cli/cursor_command_file_visitor.py` - Visitor for CLI commands
- `agile_bot/bots/base_bot/src/cli/cursor_command_renderer_visitor.py` - Renderer for action help
- `agile_bot/bots/base_bot/src/generator/orchestrator.py` - Orchestrator pattern
- `agile_bot/bots/base_bot/src/generator/visitor.py` - Base Visitor class

### REPL Implementation
- `agile_bot/bots/base_bot/src/repl_cli/repl_main.py` - REPL entry point
- `agile_bot/bots/base_bot/src/repl_cli/repl_session.py` - REPL session management
- `agile_bot/bots/base_bot/src/repl_cli/command_parser.py` - Command parsing logic

## Success Criteria

- [ ] REPLCursorCommandVisitor follows orchestrator-visitor pattern
- [ ] Base REPL commands generated with piped syntax
- [ ] Behavior navigation shortcuts generated for all behaviors
- [ ] Action operation shortcuts generated for all actions
- [ ] Commands use correct dot notation (behavior.action.operation)
- [ ] Obsolete command files removed when behaviors/actions removed
- [ ] Bot registry updated with `repl_path` field
- [ ] Commands work correctly in Cursor command palette
- [ ] All tests pass with 90%+ coverage
- [ ] Command files match Cursor syntax conventions

## Source Material

This story was created by analyzing:
1. Existing "Generate Cursor Command Files" story for CLI pattern
2. `CursorCommandGenerator` and `CursorCommandFileVisitor` implementation
3. REPL CLI command syntax and dot notation patterns
4. Cursor command file format and conventions

Generated: 2025-12-26
Context: Part of REPL CLI infrastructure for Cursor IDE integration



