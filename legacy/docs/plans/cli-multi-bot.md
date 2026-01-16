# CLI Extra Increment Plan

## Overview

This plan documents the "CLI Extra" increment (Priority 13) which adds bot switching, bot discovery, cross-bot command invocation, and independent action access capabilities to the CLI REPL system.

**Increment Goal:** Enable users to switch between different bots (story_bot, crc_bot, etc.) within a single REPL session, invoke commands across bots, and directly access independent actions (like `rules` and `help`) that exist outside the normal workflow.

## Stories Added to Story Graph

This increment includes 6 stories covering bot discovery, navigation, rules behavior invocation (independent action infrastructure), and cross-bot commands.

### 1. Load All Registered Bots
**Epic:** Initialize REPL Session  
**Sequential Order:** 6  
**Story Type:** System  
**Actor:** CLI

**Purpose:** Load all available bots from the registry file at startup so the REPL can display them and allow switching between them.

**Implementation Notes:**
- Registry file location: `agile_bot/bots/registry.json`
- Currently registered bots:
  - `base_bot` - Base bot framework
  - `story_bot` - Story management bot
  - `crc_bot` - CRC design bot
- Registry contains CLI paths and trigger patterns for each bot
- Should load bot metadata (name, cli_path, trigger_patterns) into REPL state
- Enables multi-bot awareness in the REPL session

**Acceptance Criteria:**
- Registry file is read on REPL startup
- All registered bots are parsed and stored in session state
- Invalid or missing bots are logged but don't crash the session
- Bot registry data is available for navigation and display commands

---

### 2. Invoke Specific Bot Behavior Command through CLI
**Epic:** Execute Action Operation Through CLI  
**Sequential Order:** 6  
**Story Type:** User  
**Actor:** User

**Purpose:** Allow users to execute a command on a specific bot without first navigating to it, using syntax like `story_bot.discovery.build` or `crc_bot.design.render`.

**Implementation Notes:**
- Extends existing CLI command parsing
- Syntax: `<bot_name>.<behavior>.<action>` or `<bot_name>.<behavior>`
- Should support full dot notation across bots
- Does NOT change the current bot context - just executes one-off command
- Must validate bot exists in registry before attempting execution
- Should delegate to the target bot's CLI entry point

**Example Commands:**
```bash
# Execute story_bot discovery build without switching context
> story_bot.discovery.build

# Execute crc_bot design render
> crc_bot.design.render

# Navigate within current bot still works
> discovery.build
```

**Acceptance Criteria:**
- Dot notation parser recognizes bot prefix
- Command routes to correct bot's CLI
- Current bot context remains unchanged after execution
- Error handling for invalid bot names
- Works in both interactive and pipe mode

---

### 3. Navigate to Bot using CLI Dot Notation
**Epic:** Navigate Bot Behaviors and Actions With CLI  
**Sequential Order:** 4  
**Story Type:** User  scope all

**Actor:** User

**Purpose:** Allow users to switch the active bot context using dot notation, so subsequent commands apply to the new bot.

**Implementation Notes:**
- Extends navigation system to include bot level
- Syntax: `bot <bot_name>` or just `<bot_name>` (if unambiguous)
- Changes the current bot context for all subsequent commands
- Must update REPL state to reflect new current bot
- Should trigger re-display of state with new bot's hierarchy
- Navigation history should track bot switches

**Example Commands:**
```bash
# Switch to story_bot
> bot story_bot
> story_bot

# Now all commands apply to story_bot
> discovery.build
> exploration.validate

# Switch to crc_bot
> bot crc_bot
> design.render
```

**Acceptance Criteria:**
- `bot <name>` command changes active bot
- Subsequent relative navigation uses new bot context
- State display reflects current bot
- Error handling for invalid bot names
- Can navigate back to previous bot

---

### 4. Display Available Bot in Tree Hierarchy
**Epic:** Display Bot State Using CLI  
**Sequential Order:** 4  
**Story Type:** System  
**Actor:** CLI

**Purpose:** Enhance the REPL tree display to show all available bots at the top level, with the current bot highlighted.

**Implementation Notes:**
- Extends existing tree display rendering
- Shows bot list at top of hierarchy
- Indicates current bot with marker (e.g., `[current]` or `*`)
- Format example:
  ```
  Available Bots:
    [story_bot] (current)
    crc_bot
    base_bot
  
  Current Bot: story_bot
  └── Behaviors
      ├── discovery
      │   ├── clarify
      │   ├── strategy
      │   └── build (current)
      ...
  ```
- Should collapse non-current bots to save screen space
- Expandable view option to show other bots' hierarchies

**Acceptance Criteria:**
- All registered bots appear in tree display
- Current bot is clearly marked
- Tree shows current bot's full hierarchy
- Other bots shown but collapsed
- Display updates when bot context changes

---

### 5. Display CLI Bot Command in Navigation Menu Footer
**Epic:** Display Bot State Using CLI  
**Sequential Order:** 5  
**Story Type:** System  
**Actor:** CLI

**Purpose:** Add the `bot <name>` command to the navigation menu footer so users know how to switch bots.

**Implementation Notes:**
- Extends existing footer/help menu
- Current footer shows navigation commands like:
  - `<behavior>.<action>` - Navigate to action
  - `confirm` - Confirm and advance
  - `help` - Show help
  - `exit` - Exit REPL
- Add new command:
  - `bot <name>` - Switch to different bot
- Should show list of available bots when `help` is invoked
- Include in piped mode instructions for AI agents

**Example Footer:**
```
Commands:
  <behavior>.<action>  Navigate to action
  bot <name>           Switch to bot (story_bot, crc_bot)
  confirm              Confirm and advance
  status               Show current state
  help                 Show this help
  exit                 Exit REPL
```

**Acceptance Criteria:**
- Footer includes `bot <name>` command
- Help text explains bot switching
- Available bots listed in help output
- Documentation reflects new command
- Piped mode instructions include bot commands

---

## Implementation Order

1. **Load All Registered Bots** (Foundation)
   - Implement registry loading logic
   - Store bot metadata in REPL state
   - Add tests for registry parsing

2. **Invoke Rules Action Outside Workflow** (Rules Behavior + Independent Action Infrastructure)
   - Extend action discovery to distinguish workflow vs independent actions
   - Update navigation to allow direct invocation of rules action
   - Implement infrastructure that works for any independent action (workflow: false)
   - Ensure rules (and other independent actions) don't modify workflow state
   - Add tests for rules action invocation
   - Verify rules action loads behavior-specific rules into AI context

3. **Display Available Bot in Tree Hierarchy** (Visual Feedback)
   - Extend tree rendering to show bots
   - Add current bot indicator
   - Mark independent actions in tree display
   - Test display with multiple bots

4. **Display CLI Bot Command in Navigation Menu Footer** (Discoverability)
   - Update footer rendering
   - Add help text for bot commands
   - Document independent vs workflow actions
   - Update documentation

5. **Navigate to Bot using CLI Dot Notation** (Core Navigation)
   - Implement bot context switching
   - Update navigation state management
   - Add bot switching tests

6. **Invoke Specific Bot Behavior Command through CLI** (Advanced Usage)
   - Extend command parser for cross-bot commands
   - Implement command routing to other bots
   - Support cross-bot independent action invocation
   - Add integration tests

## Technical Dependencies

### Files to Modify

1. **Registry Loading:**
   - `agile_bot/bots/base_bot/src/repl_cli/session.py` - Add registry loading
   - New: `agile_bot/bots/base_bot/src/repl_cli/bot_registry.py` - Registry management

2. **Navigation:**
   - `agile_bot/bots/base_bot/src/repl_cli/navigation.py` - Extend navigation
   - `agile_bot/bots/base_bot/src/repl_cli/commands.py` - Add bot command

3. **Display:**
   - `agile_bot/bots/base_bot/src/repl_cli/display.py` - Bot tree rendering
   - `agile_bot/bots/base_bot/src/repl_cli/footer.py` - Footer with bot commands

4. **Command Execution:**
   - `agile_bot/bots/base_bot/src/repl_cli/command_parser.py` - Cross-bot parsing
   - `agile_bot/bots/base_bot/src/repl_cli/executor.py` - Route to other bots

### New Domain Concepts

- **BotRegistry:** Collection of registered bots with metadata
- **BotContext:** Current active bot in REPL session
- **CrossBotCommand:** Command targeting different bot than current
- **BotNavigationHistory:** Track bot switches in navigation history
- **Independent Action:** Action with `workflow: false` that exists outside the behavior_action_flow (e.g., rules, help). Can be invoked at any time without affecting workflow state
- **Workflow Action:** Action with `workflow: true` that participates in the sequential behavior_action_flow with order and next_action

## Testing Strategy

### Unit Tests
- Registry file parsing (valid, invalid, missing)
- Bot context switching logic
- Cross-bot command parsing
- Display rendering with multiple bots

### Integration Tests
- End-to-end bot switching in REPL
- Cross-bot command execution
- State persistence across bot switches
- Navigation history with bot changes

### Manual Testing Scenarios
1. Launch REPL and verify all bots displayed
2. Switch to story_bot, run discovery.build
3. Switch to crc_bot, run design.render
4. Execute cross-bot command: `story_bot.exploration.validate`
5. Verify footer shows bot command
6. Test in both TTY and piped mode

## Related Increments

- **Increment 4 (CLI):** Foundation for CLI infrastructure
- **Increment 10 (Front-End REPL):** Core REPL display and navigation
- **Increment 12 (REPL Real Backend):** Action execution framework

## Success Criteria

- [ ] All 6 stories implemented and tested
- [ ] User can discover available bots
- [ ] User can switch between bots
- [ ] User can execute cross-bot commands
- [ ] User can invoke rules action directly at any time
- [ ] Rules action loads behavior-specific rules into AI context
- [ ] Rules action (and other independent actions) don't disrupt workflow state
- [ ] Infrastructure supports any independent action (workflow: false)
- [ ] Display clearly shows current bot
- [ ] Display distinguishes independent vs workflow actions
- [ ] Help system documents bot commands and independent actions
- [ ] All tests passing
- [ ] Documentation updated

## Notes

- Bot registry is centralized at `agile_bot/bots/registry.json`
- Currently 3 bots registered: base_bot, story_bot, crc_bot
- Future bots can be added by updating registry.json
- Consider auto-discovery of bots vs explicit registration
- May need to handle bot initialization/teardown on switch
- State persistence should track which bot was active

### Independent Actions & Rules Behavior
- Independent actions (`workflow: false`) exist outside the behavior_action_flow
- **Rules Action** (primary focus of this increment):
  - Purpose: Load behavior-specific rules into AI context for validation/guidance
  - Location: `agile_bot/bots/base_bot/base_actions/rules/`
  - Can be invoked at any time: `rules`, `discovery.rules`, `story_bot.rules`
  - Critical for AI agents to understand bot-specific coding rules and standards
  - Does not affect workflow state or current action position
- Other independent actions that benefit from same infrastructure:
  - `help` - Display available commands and workflow status
- Cross-bot independent action calls should work (e.g., `story_bot.rules`, `crc_bot.rules`)
- Tree display should visually distinguish independent from workflow actions
- Infrastructure should be general enough to support future independent actions

---

**Created:** 2025-12-26  
**Increment Priority:** 13  
**Status:** Planning

