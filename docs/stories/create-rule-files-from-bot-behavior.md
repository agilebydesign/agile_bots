# Create Rule Files From Bot Behavior

**Output format:** Generated rule files go to workspace `.cursor/rules/` folder. (Commands deferred.)

## Acceptance Criteria
WHEN generate context pagage command on bot 
**THEN Generator iterates over bot behaviors**
- Walks `bots/{bot_name}/behaviors/` directory
- Reads each `behavior.json`
- Extracts: behaviorName, description, goal, inputs, outputs
- Creates one `.mdc` rule file per behavior in workspace `.cursor/rules/{bot_name}_{behavior}.mdc` (e.g. story_bot → story_shape.mdc)

**AND Generator writes rule file header**
- Title: `# {bot_name} {behaviorName} Behavior`
- Subtitle: description
- Sections: Goal, Inputs, Outputs

**AND enerator adds trigger words section**
- Section: `## When to use this behavior`
- Extracts `trigger_words.patterns` from behavior.json
- Formats as "Use this behavior when:" with each pattern as bullet
- Converts regex patterns to natural language

**AND Generator adds clarification section**
- Section: `## Clarification`
- Reads `guardrails/required_context/key_questions.json` → key questions as bullets
- Reads `guardrails/required_context/evidence.json` → evidence list
- Merges clarify action instructions from `behavior.json` actions_workflow (action name "clarify")
- Merges instructions from `base_actions/clarify/action_config.json`
- Adds clarification logic: answer each question from context; if you can't answer, state "[!] NOT ENOUGH INFORMATION - REQUIRES USER INPUT"; store answers to clarification.json for later session; don't guess or infer—be explicit when information is missing
Important ; save to clarification.strategy

**AND Generator adds strategy section**
- Section: `## Strategy`
- Reads `guardrails/strategy/typical_assumptions.json` → assumptions as bullets
- Reads `guardrails/strategy/decision_criteria/*.json` → each decision (question, options) as structured bullets
- Merges strategy action instructions from `behavior.json` actions_workflow (action name "strategy")
- Merges instructions from `base_actions/strategy/action_config.json`
- Adds strategy logic: review context, make decisions, compile assumptions; if insufficient context state "[!] NOT ENOUGH INFORMATION"; save to strategy.json

**AND Generator adds build section**
- Section: `## Build`
- Merges build action instructions from `behavior.json` actions_workflow (action name "build")
- Specifies templates from `content/render/*.json` (template paths, output formats)—no JSON schema for build output

**Generator adds render section**
- Section: `## Render`
- Walks `content/render/*.json`
- For each: extracts template path, output path, instructions
- Formats as bullets (e.g. "story-map.md template → story-map.txt")

**AND Generator processes rules directory**
- Walks `rules/*.json`, sorts by priority
- For each: extracts description, do.description, do.guidance, dont.description, dont.guidance
- Formats as `## Rules` with DO/DON'T blocks
- Includes examples as code blocks

**AND saved in Output format:** Generated rule files go to workspace `.cursor/rules/` folder. (Commands deferred.)

*(Validate: omit—already covered in rules. Commands: deferred.)*
