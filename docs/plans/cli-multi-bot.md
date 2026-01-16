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


