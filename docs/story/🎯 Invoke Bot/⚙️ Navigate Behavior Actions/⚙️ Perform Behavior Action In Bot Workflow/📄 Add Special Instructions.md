# 📄 Add Special Instructions

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/navigate_behavior_actions/test_perform_behavior_action_in_bot_workflow.py)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Navigate Behavior Actions](..) / [⚙️ Perform Behavior Action In Bot Workflow](.)  
**Sequential Order:** 12.6
**Story Type:** user

## Story Description

Add Special Instructions functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User enters text in Panel behavior-level Special Instructions text area (beside shape, before toggle group)
  **then** Panel stores that text for that behavior

- **When** User enters text in Panel action-level Special Instructions text area (e.g. beside shape.clarify, same row)
  **then** Panel stores that text for that behavior and action

- **When** User clicks Submit in Panel
  **then** Panel injects all special instructions from behavior and action levels into the prompt

- **When** User runs cli.behaviors.shape.clarify.special_instructions "focus on edge cases"
  **then** CLI stores that instruction for shape.clarify
  **and** CLI includes it in next prompt

## Scenarios

### Scenario: Panel stores behavior-level special instructions (happy_path)

**Steps:**
```gherkin
Given Panel displays shape Behavior with no special instructions stored
When User enters "focus on edge cases" in Panel behavior-level Special Instructions for shape
Then Panel stores "focus on edge cases" for shape Behavior
```

### Scenario: Panel stores action-level special instructions (happy_path)

**Steps:**
```gherkin
Given Panel displays shape Behavior with clarify Action and no special instructions stored for that Action
When User enters "emphasize validation" in Panel action-level Special Instructions for shape and clarify
Then Panel stores "emphasize validation" for shape Behavior and clarify Action
```

### Scenario: Panel injects special instructions on Submit (happy_path)

**Steps:**
```gherkin
Given Panel has behavior-level special instructions "focus on edge cases" for shape
And Panel has action-level special instructions "emphasize validation" for shape and clarify
When User submits instructions in Panel
Then Panel injects behavior-level and action-level special instructions into Instructions
```

### Scenario: CLI stores and includes special instructions in next prompt (happy_path)

**Steps:**
```gherkin
Given CLI is at shape.clarify
When User runs cli.behaviors.shape.clarify.special_instructions "focus on edge cases"
Then CLI stores that instruction for shape.clarify
And CLI includes it in next prompt
```

### Scenario: Panel injects only behavior-level instructions when no action-level set (edge_case)

**Steps:**
```gherkin
Given Panel has behavior-level special instructions "focus on edge cases" for shape
And Panel has no action-level special instructions for shape
When User submits instructions in Panel
Then Panel injects behavior-level special instructions into Instructions
```

### Scenario: CLI reports failed when special_instructions command fails (error_case)

**Steps:**
```gherkin
Given CLI is at shape.clarify
And Bot or workspace is misconfigured
When User runs cli.behaviors.shape.clarify.special_instructions "focus on edge cases"
Then CLI reports failed to Terminal
```
