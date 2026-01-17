## Module: {module}

{concept}
    {responsibility}: {collaborator},{collaborator},...
    {responsibility}: {collaborator},{collaborator},...

{concept} : {base_class}
    {responsibility}: {collaborator},{collaborator},...
    {responsibility}: {collaborator},{collaborator},...

{concept}
    {responsibility}: {collaborator},{collaborator},...

## Module: {another_module}

{concept}
    {responsibility}: {collaborator},{collaborator},...

Instructions:
- Group domain concepts by module (source folder structure)
- Module names MUST exactly match folder structure using dot notation
  Examples: 'repl_cli', 'repl_cli.cli_bot', 'actions.render', 'bot.workflow'
- Module names follow same naming conventions as classes (clear, descriptive, not generic)
- Use clear, concise domain concepts and responsibilities
- List each responsibility as: {responsibility}: {collaborator},{collaborator},...
- For classes that inherit from a base class, use: {concept} : {base_class}
- Only include meaningful relationships; avoid unnecessary boilerplate or filler
- Ensure each domain concept is followed by its set of responsibilities
