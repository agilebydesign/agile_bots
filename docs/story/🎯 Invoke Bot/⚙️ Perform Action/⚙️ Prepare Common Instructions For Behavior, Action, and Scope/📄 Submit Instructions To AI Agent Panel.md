# 📄 Submit Instructions To AI Agent Panel

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/test_prepare_common_instructions_for_behavior_action_and_scope.js#L272)

**User:** User
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Prepare Common Instructions For Behavior, Action, and Scope](.)  
**Sequential Order:** 3.5
**Story Type:** user

## Story Description

Submit Instructions To AI Agent Panel functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** User clicks Submit and behavior is collapsed in Panel
  **then** Panel invokes CLI
  **and** System prepares instructions for the whole behavior (all actions per manual / combine_with_next / skip)

- **When** User clicks Submit and behavior is expanded in Panel
  **then** Panel invokes CLI
  **and** System prepares instructions for the selected action or the first executable action

- **When** User clicks submit button
  **then** Submitted instructions include scope section
  **and** Scope section includes scope type (story/files/all)
  **and** Scope section includes scope filter values
  **and** Scope section includes complete story graph tree when scope is story-based

- **When** User has answered clarify questions or made strategy decisions
  **then** Submitted instructions include all saved guardrails

## Scenarios

<a id="scenario-panel-submit-with-collapsed-behavior-prepares-whole-behavior-instructions"></a>
### Scenario: [Panel submit with collapsed behavior prepares whole-behavior instructions](#scenario-panel-submit-with-collapsed-behavior-prepares-whole-behavior-instructions) (happy_path)

**Steps:**
```gherkin
Given Panel has shape behavior collapsed and selected
When Panel invokes submit (via CLI)
Then CLI/Bot prepares instructions for whole shape behavior (all actions per manual/combine_with_next/skip)
```


<a id="scenario-panel-submit-with-expanded-behavior-prepares-instructions-for-selected-action"></a>
### Scenario: [Panel submit with expanded behavior prepares instructions for selected action](#scenario-panel-submit-with-expanded-behavior-prepares-instructions-for-selected-action) (happy_path)

**Steps:**
```gherkin
Given Panel has shape behavior expanded
And shape.clarify is the selected action
When Panel invokes submit (via CLI)
Then CLI/Bot prepares instructions for shape.clarify
```


<a id="scenario-panel-submit-with-expanded-behavior-prepares-instructions-for-first-executable-when-none-selected"></a>
### Scenario: [Panel submit with expanded behavior prepares instructions for first executable when none selected](#scenario-panel-submit-with-expanded-behavior-prepares-instructions-for-first-executable-when-none-selected) (happy_path)

**Steps:**
```gherkin
Given Panel has shape behavior expanded
And no action is explicitly selected (first action is current)
When Panel invokes submit (via CLI)
Then CLI/Bot prepares instructions for the first executable action in shape
```


<a id="scenario-submit-sends-instructions-to-ai-chat"></a>
### Scenario: [Submit sends instructions to AI chat](#scenario-submit-sends-instructions-to-ai-chat) (happy_path)

**Steps:**
```gherkin
Given Panel displays instructions for current action
When User clicks submit button
Then System sends instructions to Cursor AI chat
And Panel displays success confirmation message
And AI chat receives instructions
```


<a id="scenario-submit-fails-when-chat-unavailable"></a>
### Scenario: [Submit fails when chat unavailable](#scenario-submit-fails-when-chat-unavailable) (error)

**Steps:**
```gherkin
Given Panel displays instructions
And Cursor AI chat is not available
When User clicks submit button
Then Panel displays error message
And Error message indicates chat unavailable
```


<a id="scenario-copy-then-submit"></a>
### Scenario: [Copy then submit](#scenario-copy-then-submit) (happy_path)

**Steps:**
```gherkin
Given Panel displays instructions
When User clicks copy button
Then Instructions are copied to clipboard
When User clicks submit button
Then Instructions are also sent to AI chat
```


<a id="scenario-submitted-instructions-include-scope"></a>
### Scenario: [Submitted instructions include scope](#scenario-submitted-instructions-include-scope) (happy_path)

**Steps:**
```gherkin
Given Bot has scope set to story Open Panel
And Scope.results contains full story graph hierarchy
When User clicks submit in panel
Then Submitted instructions contain Scope section at top
And Scope section shows Story Scope: Open Panel
And Scope section shows complete epic/sub-epic/story hierarchy
```


<a id="scenario-submitted-instructions-include-guardrails"></a>
### Scenario: [Submitted instructions include guardrails](#scenario-submitted-instructions-include-guardrails) (happy_path)

**Steps:**
```gherkin
Given Bot is at shape.build
And User has answered clarify questions
And User has made strategy decisions
When User clicks submit in panel
Then Submitted instructions include Clarify section with answers
And Submitted instructions include Strategy section with decisions and assumptions
And All saved guardrails are visible in submitted markdown
```

