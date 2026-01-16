# 📝 Forward To Current Action

**Navigation:** [📋 Story Map](../../../../story-map.drawio)

**User:** AI Chat
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Invoke MCP](.)  
**Sequential Order:** 4
**Story Type:** user

## Story Description

Forward To Current Action functionality allows behavior tool to forward to current action within behavior based on workflow state, update workflow when state shows different behavior, or default to first action when state is missing.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** Behavior tool receives invocation

  **and** workflow state shows current_action within behavior

  **then** Behavior tool forwards to current action

- **When** workflow state shows different behavior

  **then** Behavior tool updates workflow to current behavior

- **When** workflow state does NOT exist

  **then** Behavior tool defaults to first action

## Scenarios

### Scenario: Behavior tool forwards to current action within behavior (happy_path)

**Steps:**
```gherkin
Given a behavior tool for 'discovery' behavior
And behavior action state shows current_action='build_knowledge'
When Behavior tool receives invocation
Then Behavior tool forwards to build_knowledge action
```


### Scenario: Behavior tool sets behavior action state to current behavior when state shows different behavior (happy_path)

**Steps:**
```gherkin
Given a behavior tool for 'exploration' behavior
And behavior action state shows current_behavior='discovery'
When Behavior tool receives invocation
Then behavior action state updated to current_behavior='exploration'
```


### Scenario: Behavior tool defaults to first action when state missing (happy_path)

**Steps:**
```gherkin
Given a behavior tool for 'shape' behavior
And behavior action state does NOT exist
When Behavior tool receives invocation
Then Behavior tool defaults to first action
```


### Scenario: Action called directly saves behavior action state (happy_path)

**Steps:**
```gherkin
Given Bot is initialized with WORKING_AREA set
And No behavior action state exists yet
When Action is called directly (e.g., bot.shape.clarify())
Then behavior_action_state.json is created with current_action
And This ensures state is saved whether action is called via forward or directly
```

