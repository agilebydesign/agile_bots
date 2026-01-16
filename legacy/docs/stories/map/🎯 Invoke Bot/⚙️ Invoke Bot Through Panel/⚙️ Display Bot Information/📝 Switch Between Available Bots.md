# 📝 Switch Between Available Bots

**Navigation:** [📋 Story Map](../../../../../story-map.drawio)

**User:** User
**Path:** [🎯 Invoke Bot](../../..) / [⚙️ Invoke Bot Through Panel](../..) / [⚙️ Display Bot Information](.)  
**Sequential Order:** 6
**Story Type:** user

## Story Description

Allow users to switch between different available bots (e.g., story_bot, crc_bot) through clickable links in the header.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** Multiple bots are available

  **then** Bot selector links are displayed in header

  **and** Current bot link is highlighted as active

- **When** User clicks different bot link

  **then** Panel switches to selected bot

  **and** Panel refreshes to show selected bot's status

## Scenarios

### Scenario: Display available bot links (happy_path)

**Steps:**
```gherkin
Given Workspace has both story_bot and crc_bot available
When User opens Bot Status Panel
Then Bot selector shows "story_bot" and "crc_bot" links
And Currently active bot link is highlighted
```

### Scenario: Switch to different bot (happy_path)

**Steps:**
```gherkin
Given Panel is showing story_bot status
And crc_bot link is visible in header
When User clicks "crc_bot" link
Then Panel switches to display crc_bot
And crc_bot link becomes highlighted as active
And Panel shows crc_bot's behaviors and status
```

### Scenario: Only one bot shows no selector (happy_path)

**Steps:**
```gherkin
Given Workspace has only story_bot available
When User opens Bot Status Panel
Then No bot selector links are displayed
And Bot name is shown prominently without selection options
```

