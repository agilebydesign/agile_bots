# 📄 Create Rule Files From Bot Behavior

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** Generator
**Path:** [🎯 Build Agile Bots](../..) / [⚙️ Generate CLI](.)  
**Sequential Order:** 1.0
**Story Type:** user

## Story Description

Create Rule Files From Bot Behavior functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** generate context package command runs on bot,
  **then** Generator iterates over bot behaviors:

- **When** Generator writes rule file header,
  **then** it adds:

- **When** Generator adds trigger words section,
  **then** it:

- **When** Generator adds clarification section,
  **then** it:

- **When** Generator adds strategy section,
  **then** it:

- **When** Generator adds build section,
  **then** it:

- **When** Generator adds render section,
  **then** it:

- **When** Generator processes rules directory,
  **then** it:

- **When** Generator completes,
  **then** output is .mdc rule files saved to workspace .cursor/rules/ folder (one per behavior)

## Scenarios

<a id="scenario-generator-produces-rule-file-per-behavior-when-bot-has-valid-behaviors"></a>
### Scenario: [Generator produces rule file per behavior when bot has valid behaviors](#scenario-generator-produces-rule-file-per-behavior-when-bot-has-valid-behaviors) (happy_path)

**Steps:**
```gherkin
Given Bot {bot_name} exists with behaviors directory
And Behavior {behavior_name} has valid behavior.json with behaviorName, description, goal, inputs, outputs
When Generator runs generate context package command on {bot_name}
Then Generator walks bots/{bot_name}/behaviors/ directory
And Generator reads each behavior.json
And Generator creates one .mdc rule file at .cursor/rules/{bot_name}_{behavior}.mdc per behavior
```


<a id="scenario-generator-writes-rule-file-header-with-title-subtitle-and-sections"></a>
### Scenario: [Generator writes rule file header with title subtitle and sections](#scenario-generator-writes-rule-file-header-with-title-subtitle-and-sections) (happy_path)

**Steps:**
```gherkin
Given Bot story_bot exists with shape behavior
When Generator writes rule file for story_bot shape
Then Generator adds title # story_bot shape Behavior
And Generator adds description as subtitle
And Generator adds sections Goal, Inputs, Outputs
```


<a id="scenario-generator-adds-trigger-words-section-from-behaviorjson-patterns"></a>
### Scenario: [Generator adds trigger words section from behavior.json patterns](#scenario-generator-adds-trigger-words-section-from-behaviorjson-patterns) (happy_path)

**Steps:**
```gherkin
Given Behavior has trigger_words.patterns in behavior.json
When Generator adds trigger words section
Then Generator creates ## When to use this behavior
And Generator extracts trigger_words.patterns from behavior.json
And Generator formats as Use this behavior when: with each pattern as bullet
And Generator converts regex patterns to natural language
```


<a id="scenario-generator-merges-clarification-section-from-guardrails-and-base-actions"></a>
### Scenario: [Generator merges clarification section from guardrails and base actions](#scenario-generator-merges-clarification-section-from-guardrails-and-base-actions) (happy_path)

**Steps:**
```gherkin
Given Behavior has guardrails/required_context/key_questions.json and evidence.json
And Behavior has clarify action in actions_workflow
When Generator adds clarification section
Then Generator reads key_questions.json and evidence.json
And Generator merges clarify action from behavior.json and base_actions/clarify/action_config.json
And Generator adds logic to state NOT ENOUGH INFORMATION when context missing
And Generator specifies save to clarification.strategy
```


<a id="scenario-generator-merges-strategy-section-from-guardrails-and-base-actions"></a>
### Scenario: [Generator merges strategy section from guardrails and base actions](#scenario-generator-merges-strategy-section-from-guardrails-and-base-actions) (happy_path)

**Steps:**
```gherkin
Given Behavior has guardrails/strategy/typical_assumptions.json and decision_criteria
When Generator adds strategy section
Then Generator reads typical_assumptions.json and decision_criteria/*.json
And Generator merges strategy action from behavior.json and base_actions/strategy/action_config.json
And Generator adds logic to state NOT ENOUGH INFORMATION when context insufficient
And Generator specifies save to strategy.json
```


<a id="scenario-generator-adds-build-and-render-sections-from-content-config"></a>
### Scenario: [Generator adds build and render sections from content config](#scenario-generator-adds-build-and-render-sections-from-content-config) (happy_path)

**Steps:**
```gherkin
Given Behavior has build action and content/render/*.json configs
When Generator adds build section
Then Generator merges build action instructions from behavior.json
And Generator specifies templates from content/render/*.json
When Generator adds render section
Then Generator walks content/render/*.json
And Generator extracts template path, output path, instructions per config
And Generator formats as bullets
```


<a id="scenario-generator-processes-rules-directory-and-formats-do-dont-blocks"></a>
### Scenario: [Generator processes rules directory and formats DO DON'T blocks](#scenario-generator-processes-rules-directory-and-formats-do-dont-blocks) (happy_path)

**Steps:**
```gherkin
Given Behavior has rules/*.json files sorted by priority
When Generator processes rules directory
Then Generator walks rules/*.json
And Generator extracts description, do.description, do.guidance, dont.description, dont.guidance
And Generator formats as ## Rules with DO/DON'T blocks
And Generator includes examples as code blocks
```


<a id="scenario-generator-outputs-mdc-files-to-workspace-cursorrules-folder"></a>
### Scenario: [Generator outputs .mdc files to workspace .cursor/rules folder](#scenario-generator-outputs-mdc-files-to-workspace-cursorrules-folder) (happy_path)

**Steps:**
```gherkin
Given Generator has produced rule content for each behavior
When Generator completes
Then Generator saves .mdc rule files to workspace .cursor/rules/ folder
And One .mdc file exists per behavior
```


<a id="scenario-generator-skips-behavior-when-behaviorjson-is-malformed"></a>
### Scenario: [Generator skips behavior when behavior.json is malformed](#scenario-generator-skips-behavior-when-behaviorjson-is-malformed) (error_case)

**Steps:**
```gherkin
Given Bot has behaviors directory
And One behavior.json contains invalid JSON
When Generator runs generate context package command
Then Generator does not crash
And Generator produces rule files for valid behaviors only
And Generator skips or reports malformed behavior
```


<a id="scenario-generator-produces-rule-file-when-bot-has-single-behavior"></a>
### Scenario: [Generator produces rule file when bot has single behavior](#scenario-generator-produces-rule-file-when-bot-has-single-behavior) (edge_case)

**Steps:**
```gherkin
Given Bot has exactly one behavior in behaviors directory
When Generator runs generate context package command
Then Generator creates one .mdc rule file
And Rule file path follows {bot_name}_{behavior}.mdc pattern
```


<a id="scenario-display-cursor-vs-code-test-explorer"></a>
### Scenario: [Display Cursor VS Code Test Explorer](#scenario-display-cursor-vs-code-test-explorer) ()

**Steps:**
```gherkin

```

