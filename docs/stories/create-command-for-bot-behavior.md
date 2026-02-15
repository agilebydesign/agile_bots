# Create Command For Bot Behavior

**Output format:** Commands = `.md` files in `.cursor/commands/`. Rules = `.mdc` files in `.cursor/rules/`.

## Acceptance Criteria

**WHEN Generator Creates Command File For Behavior**

THEN Generator creates `.cursor/commands/{bot_name}_context_{behavior}.md`
AND adds command title `# {bot_name} {behavior} Command`
AND adds syntax section `{bot_name}_context_{behavior} <action> <scope|context>`
AND references rule file "See also: {bot_name}_{behavior}.mdc"

**WHEN Generator Adds Behavior Instructions Section**

THEN Generator creates `## Behavior Overview` section
AND adds behavior.description, behavior.goal
AND adds behavior.instructions as bullets

**WHEN Generator Adds Workflow Section**

THEN Generator creates `## Action Workflow` section
AND walks `actions_workflow.actions` by order
AND creates ordered list showing action sequence
AND for each action adds "then proceeds to {action.next_action}"
AND at end adds "Next behavior: {next_behavior_in_bot_workflow}"

**WHEN Generator Creates Action Sections**

THEN Generator creates `## Actions` header
AND for each action in `actions_workflow.actions` creates `### {action.name} (order: {action.order})` subsection
AND reads `base_actions/{action.name}/instructions.md` (or action_config.json instructions) and adds base action instructions as bullets
AND adds behavior-specific `action.instructions` as bullets
AND specifies "Next: {action.next_action}"

**WHEN Clarify Action Is In Workflow**

THEN Generator creates dedicated `### clarify` section with **instructions and content**
AND includes key questions from `guardrails/required_context/key_questions.json` (full question list as bullets)
AND includes evidence prompts from `guardrails/required_context/evidence.json` (required evidence list)
AND includes answer format from `base_actions/clarify/action_config.json` (JSON template, save-to clarification.json instructions)
AND includes behavior-specific clarify instructions from `action.instructions`
AND when user invokes clarify via command (e.g. `story_bot_context_shape clarify`), this section provides the complete instructions and content the AI needs to execute the clarify action—no need to look elsewhere
