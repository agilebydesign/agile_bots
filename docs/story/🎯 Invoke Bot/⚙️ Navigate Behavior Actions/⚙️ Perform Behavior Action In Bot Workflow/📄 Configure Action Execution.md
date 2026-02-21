# 📄 Configure Action Execution

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/navigate_behavior_actions/test_perform_behavior_action_in_bot_workflow.py)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Navigate Behavior Actions](..) / [⚙️ Perform Behavior Action In Bot Workflow](.)  
**Sequential Order:** 12.0
**Story Type:** user

## Story Description

Configure Action Execution functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User selects behavior in Panel and clicks Submit Instructions
  **then** Panel shows list of actions and toggle (Auto | Skip | Manual) per action with current state toggled on

- **When** User sets action to Skip via toggle AND User executes that behavior
  **then** Panel invokes CLI and CLI invokes Bot and Bot runs Behavior and skips that action

- **When** User sets action to Auto via toggle AND User executes that behavior
  **then** Panel invokes CLI and CLI invokes Bot and Bot runs Behavior and executes that action as soon as previous action completes

- **When** User sets action to Manual via toggle AND User executes that behavior
  **then** Panel invokes CLI and CLI invokes Bot and Bot runs Behavior and requires User to submit instructions for that action

- **When** User sets action execution from Panel
  **then** Panel invokes CLI and CLI invokes Bot
  **and** Bot persists the setting for that Behavior and Action
  **and** CLI reports completion
  **and** Panel watches CLI for status

- **When** User runs set_execution from CLI (no Panel)
  **then** CLI invokes Bot and Bot persists the action execution setting
  **and** CLI reports completion or failed to the terminal

- **When** an action (e.g. Clarification) is set to Auto AND User executes that behavior
  **then** Panel invokes CLI and CLI invokes Bot and Bot runs that action automatically without User clicking Execute

- **When** a following action (e.g. Strategy) is set to Auto AND User executes that behavior
  **then** Bot runs current action like normal
  **and** each action has a save_file property (e.g. clarification.json)
  **and** CLI debounce-checks that save_file THEN Bot runs next action
  **and** Panel invokes CLI and CLI invokes Bot and Panel watches status

- **When** the last action of a behavior has execution set to Auto
  **then** Bot runs that action like normal
  **and** Auto does nothing (no next action to run)

- **When** Bot combines Action Instructions because of Combine Next
  **then** Bot shows scope in the instructions only once

- **When** Bot combines Action Instructions because of Combine Next
  **then** Bot shows clarification, questions and answers, assumptions, evidence, strategy decisions, and choices only once

- **When** Bot combines Action Instructions because of Combine Next
  **then** Bot lists context files and instructions only once

- **When** Bot combines Action Instructions because of Combine Next
  **then** Bot lists the overarching behavior instructions only once at the top

- **When** Bot combines Action Instructions because of Combine Next
  **then** Bot includes text at the top or between each Action that clearly indicates multiple actions are combined and performed one after another

- **When** Bot combines Build and Validate actions (or both appear in a combined block)
  **then** Bot mentions rules and describes them only once
  **and** Bot refers to those rules in the other action instead of repeating the full description

## Scenarios

<a id="scenario-panel-shows-actions-and-execution-toggle-per-action"></a>
### Scenario: [Panel shows actions and execution toggle per action](#scenario-panel-shows-actions-and-execution-toggle-per-action) (happy_path)

**Steps:**
```gherkin
Given a Behavior is loaded with at least one Action
When User opens that Behavior in Panel
Then Panel invokes CLI and CLI invokes Bot and Bot loads Behavior and Actions
And Panel shows the list of Actions for that Behavior and a toggle button group (Auto | Skip | Manual) per Action
```


<a id="scenario-user-sets-action-to-skip-via-toggle-and-executes-then-panel-skips-that-action"></a>
### Scenario: [User sets action to Skip via toggle and executes then Panel skips that action](#scenario-user-sets-action-to-skip-via-toggle-and-executes-then-panel-skips-that-action) (happy_path)

**Steps:**
```gherkin
Given a Behavior with at least two Actions is selected in Panel
And the second Action has execution set to Skip
When User clicks Submit Instructions
Then Panel invokes CLI and CLI invokes Bot and Bot runs the Behavior and skips that action
```


<a id="scenario-user-sets-action-to-auto-via-toggle-and-executes-then-panel-runs-it-after-previous-completes"></a>
### Scenario: [User sets action to Auto via toggle and executes then Panel runs it after previous completes](#scenario-user-sets-action-to-auto-via-toggle-and-executes-then-panel-runs-it-after-previous-completes) (happy_path)

**Steps:**
```gherkin
Given a Behavior with at least two Actions is selected in Panel
And the second Action has execution set to Auto
When User clicks Submit Instructions
Then Panel invokes CLI and CLI invokes Bot and Bot runs the Behavior and executes that action as soon as previous action completes
```


<a id="scenario-user-sets-action-to-manual-via-toggle-and-executes-then-panel-requires-execute-click"></a>
### Scenario: [User sets action to Manual via toggle and executes then Panel requires Execute click](#scenario-user-sets-action-to-manual-via-toggle-and-executes-then-panel-requires-execute-click) (happy_path)

**Steps:**
```gherkin
Given a Behavior with at least two Actions is selected in Panel
And the second Action has execution set to Manual
When User clicks Submit Instructions
Then Panel invokes CLI and CLI invokes Bot and Bot runs the Behavior and requires User to submit instructions for that action
```


<a id="scenario-user-sets-action-execution-from-panel-then-panel-invokes-cli-and-cli-persists"></a>
### Scenario: [User sets action execution from Panel then Panel invokes CLI and CLI persists](#scenario-user-sets-action-execution-from-panel-then-panel-invokes-cli-and-cli-persists) (happy_path)

**Steps:**
```gherkin
Given a Behavior and action are selected in Panel (e.g. shape.clarify)
When User sets that action execution to auto via Panel toggle
Then Panel invokes CLI and CLI invokes Bot (e.g. cli.behaviors.shape.clarify.set_execution auto)
And Bot persists the execution setting for that Behavior and Action
And CLI reports completion and Panel watches CLI for status and shows completion or failed
```


<a id="scenario-user-runs-set_execution-from-cli-then-cli-persists-and-reports-to-terminal"></a>
### Scenario: [User runs set_execution from CLI then CLI persists and reports to terminal](#scenario-user-runs-set_execution-from-cli-then-cli-persists-and-reports-to-terminal) (happy_path)

**Steps:**
```gherkin
Given User is in CLI (no Panel)
When User runs cli.behaviors.shape.clarify.set_execution auto
Then CLI invokes Bot and Bot persists that Behavior and Action to auto execution
And CLI reports completion or failed to the terminal so the flow works without Panel
```


<a id="scenario-persisted-execution-setting-is-used-when-user-runs-the-behavior"></a>
### Scenario: [Persisted execution setting is used when User runs the behavior](#scenario-persisted-execution-setting-is-used-when-user-runs-the-behavior) (happy_path)

**Steps:**
```gherkin
Given User has run cli.behaviors.shape.clarify.set_execution skip
When User runs the clarify action (Panel invokes CLI and CLI invokes Bot, or User runs from CLI)
Then Bot uses the persisted setting for that Behavior and Action and skips that action
```


<a id="scenario-when-clarification-is-auto-and-user-executes-behavior-then-it-runs-automatically"></a>
### Scenario: [When Clarification is Auto and User executes behavior then it runs automatically](#scenario-when-clarification-is-auto-and-user-executes-behavior-then-it-runs-automatically) (happy_path)

**Steps:**
```gherkin
Given a Behavior has Clarification action
And Clarification has execution set to Auto
When User executes that Behavior
Then Panel invokes CLI and CLI invokes Bot and Bot runs the Behavior and runs Clarification automatically without User clicking Execute
```


<a id="scenario-when-strategy-is-auto-and-user-executes-behavior-then-it-runs-automatically"></a>
### Scenario: [When Strategy is Auto and User executes behavior then it runs automatically](#scenario-when-strategy-is-auto-and-user-executes-behavior-then-it-runs-automatically) (happy_path)

**Steps:**
```gherkin
Given a Behavior has Strategy action and previous action (e.g. Clarification) has a save_file property (e.g. clarification.json)
And Strategy has execution set to Auto
When User executes that Behavior
Then Panel invokes CLI and CLI invokes Bot and Bot runs the current action like normal and when that action saves to its save_file CLI debounce-checks then Bot runs next action (Strategy)
And Panel watches CLI for status
```


<a id="scenario-when-last-action-of-behavior-is-auto-then-auto-does-nothing"></a>
### Scenario: [When last action of behavior is Auto then Auto does nothing](#scenario-when-last-action-of-behavior-is-auto-then-auto-does-nothing) (happy_path)

**Steps:**
```gherkin
Given a Behavior whose last action (e.g. render) has execution set to Auto
When User executes that Behavior and Bot reaches that last action
Then Bot runs that action like normal
And there is no next action so Auto does nothing (no chained run)
```


<a id="scenario-combined-instructions-deduplicate-shared-content-and-include-combining-text"></a>
### Scenario: [Combined instructions deduplicate shared content and include combining text](#scenario-combined-instructions-deduplicate-shared-content-and-include-combining-text) (happy_path)

**Steps:**
```gherkin
Given a Behavior with actions Clarify, Strategy, Build in order
And Clarify and Strategy have execution set to Combine (combine_next)
And User navigates to shape.clarify and submits instructions
When Bot combines instructions for Clarify and Strategy
Then Bot shows scope in the combined instructions only once
And Bot shows clarification, questions and answers, assumptions, evidence, strategy decisions, and choices only once
And Bot lists context files and instructions only once
And Bot lists the overarching behavior instructions only once at the top
And Bot includes text at the top or between each Action that clearly indicates multiple actions are combined and performed one after another
```


<a id="scenario-build-and-validate-combined-rules-described-once"></a>
### Scenario: [Build and Validate combined rules described once](#scenario-build-and-validate-combined-rules-described-once) (happy_path)

**Steps:**
```gherkin
Given a Behavior with Build and Validate actions
And Build and Validate have execution set to Combine (combine_next)
When Bot combines instructions for Build and Validate
Then Bot mentions rules and describes them only once
And Bot refers to those rules in the other action instead of repeating the full description
```

