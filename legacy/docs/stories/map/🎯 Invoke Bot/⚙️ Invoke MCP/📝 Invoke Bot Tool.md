# 📝 Invoke Bot Tool

**Navigation:** [📋 Story Map](../../../../story-map.drawio)

**User:** AI Chat
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Invoke MCP](.)  
**Sequential Order:** 1
**Story Type:** user

## Story Description

Invoke Bot Tool functionality allows AI Chat to invoke bot tool with behavior and action parameters, routing to the correct behavior.action method and returning results.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** AI Chat invokes bot tool with behavior and action parameters

  **then** Tool routes to correct behavior.action method

  **and** Tool executes action and returns result

- **When** AI Chat invokes tool for specific behavior

  **then** Tool routes to that behavior only, not other behaviors

## Scenarios

### Scenario: Tool Invokes Behavior Action When Called (happy_path)

**Steps:**
```gherkin
Given Bot has behavior 'shape' with action 'clarify'
When AI Chat invokes tool with parameters
Then Tool routes to test_bot.Shape.GatherContext() method
```


### Scenario: Tool Routes To Correct Behavior Action Method (happy_path)

**Steps:**
```gherkin
Given Bot has multiple behaviors with clarify action
When AI Chat invokes 'test_bot_exploration_clarify'
Then Tool routes to test_bot.Exploration.Clarify() not other behaviors
```

