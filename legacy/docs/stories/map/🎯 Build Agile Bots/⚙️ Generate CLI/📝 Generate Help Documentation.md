# 📝 Generate Help Documentation

**Navigation:** [📋 Story Map](../../../../story-map.drawio)

**User:** Generator
**Path:** [🎯 Build Agile Bots](../..) / [⚙️ Generate CLI](.)  
**Sequential Order:** 4
**Story Type:** user

## Story Description

Generate Help Documentation functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** generator creates HelpVisitor,
  **then** it generates command reference with all CLI commands

- **When** help is generated,
  **then** it includes parameter reference with descriptions for all action parameters

- **When** examples are generated,
  **then** it includes scope examples with dot-notation syntax

- **When** documentation is output,
  **then** it creates Markdown help files in .cursor/commands/ and terminal help

## Scenarios

### Scenario: Generate Help Documentation (happy_path)

**Steps:**
```gherkin
Given system is ready
When action executes
Then action completes successfully
```
