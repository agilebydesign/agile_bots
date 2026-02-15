# Create Rule Files From Bot Behavior - Increment Exploration  

**Navigation:** [📋 Story Map](story-map.txt) | [📊 Story Graph](../story-graph.json)  

## Stories (1 total)  

### 📝 Create Rule Files From Bot Behavior  

**Acceptance Criteria:**  
- **WHEN** generate context package command runs on bot  
  **THEN** Generator iterates over bot behaviors  
  **AND** Walks bots/{bot_name}/behaviors/ directory  
  **AND** Reads each behavior.json  
  **AND** Extracts: behaviorName, description, goal, inputs, outputs  
  **AND** Creates one .mdc rule file per behavior in workspace .cursor/rules/{bot_name}_{behavior}.mdc (e.g. story_bot → story_shape.mdc)  
- **WHEN** Generator writes rule file header  
  **THEN** it adds Title: # {bot_name} {behaviorName} Behavior  
  **AND** Subtitle: description  
  **AND** Sections: Goal, Inputs, Outputs  
- **WHEN** Generator adds trigger words section  
  **THEN** it creates Section: ## When to use this behavior  
  **AND** Extracts trigger_words.patterns from behavior.json  
  **AND** Formats as Use this behavior when: with each pattern as bullet  
  **AND** Converts regex patterns to natural language  
- **WHEN** Generator adds clarification section  
  **THEN** it creates Section: ## Clarification  
  **AND** Reads guardrails/required_context/key_questions.json → key questions as bullets  
  **AND** Reads guardrails/required_context/evidence.json → evidence list  
  **AND** Merges clarify action instructions from behavior.json actions_workflow (action name clarify)  
  **AND** Merges instructions from base_actions/clarify/action_config.json  
  **AND** Adds clarification logic: answer each question from context; if you can't answer, state [!] NOT ENOUGH INFORMATION - REQUIRES USER INPUT; store answers to clarification.json for later session; don't guess or infer—be explicit when information is missing; save to clarification.strategy  
- **WHEN** Generator adds strategy section  
  **THEN** it creates Section: ## Strategy  
  **AND** Reads guardrails/strategy/typical_assumptions.json → assumptions as bullets  
  **AND** Reads guardrails/strategy/decision_criteria/*.json → each decision (question, options) as structured bullets  
  **AND** Merges strategy action instructions from behavior.json actions_workflow (action name strategy)  
  **AND** Merges instructions from base_actions/strategy/action_config.json  
  **AND** Adds strategy logic: review context, make decisions, compile assumptions; if insufficient context state [!] NOT ENOUGH INFORMATION; save to strategy.json  
- **WHEN** Generator adds build section  
  **THEN** it creates Section: ## Build  
  **AND** Merges build action instructions from behavior.json actions_workflow (action name build)  
  **AND** Specifies templates from content/render/*.json (template paths, output formats)—no JSON schema for build output  
- **WHEN** Generator adds render section  
  **THEN** it creates Section: ## Render  
  **AND** Walks content/render/*.json  
  **AND** For each: extracts template path, output path, instructions  
  **AND** Formats as bullets (e.g. story-map.md template → story-map.txt)  
- **WHEN** Generator processes rules directory  
  **THEN** it Walks rules/*.json, sorts by priority  
  **AND** For each: extracts description, do.description, do.guidance, dont.description, dont.guidance  
  **AND** Formats as ## Rules with DO/DON'T blocks  
  **AND** Includes examples as code blocks  
- **WHEN** Generator completes  
  **THEN** output is .mdc rule files saved to workspace .cursor/rules/ folder (one per behavior)  

---  

## Source Material  

Scope: Create Rule Files From Bot Behavior  
Epic: Build Agile Bots  
Sub-Epic: Generate CLI > Generate Cursor Context Package  
Story: Create Rule Files From Bot Behavior  
Actor: Generator  
