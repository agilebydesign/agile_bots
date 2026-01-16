# 📝 Generate MCP Bot Server

**Navigation:** [📋 Story Map](../../../../story-map.drawio)

**User:** MCP Server Generator
**Path:** [🎯 Build Agile Bots](../..) / [⚙️ Generate MCP Tools](.)  
**Sequential Order:** 1
**Story Type:** user

## Story Description

Generate MCP Bot Server functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** MCP Server Generator receives Bot Config

  **then** Generator generates unique MCP Server instance with Unique server name from bot name

  **and** Generated server includes Bot Config reference

  **and** Generated server leverages Specific Bot instantiation code

## Scenarios

### Scenario: Generator creates MCP server for test_bot (happy_path)

**Steps:**
```gherkin
Given A bot configuration file with a working directory and behaviors
And A bot that has been initialized with that config file
When MCP Server Generator receives Bot Config
Then Generator creates MCP Server instance with unique server name
```


### Scenario: Generator fails when Bot Config is missing (happy_path)

**Steps:**
```gherkin
Given A bot directory exists
And Bot Config does NOT exist
When MCP Server Generator attempts to receive Bot Config
Then Generator raises FileNotFoundError and does not create MCP Server instance
```


### Scenario: Generator fails when Bot Config is malformed (happy_path)

**Steps:**
```gherkin
Given A bot directory exists
And Bot Config file exists with invalid JSON syntax
When MCP Server Generator attempts to receive Bot Config
Then Generator raises JSONDecodeError and does not create MCP Server instance
```

