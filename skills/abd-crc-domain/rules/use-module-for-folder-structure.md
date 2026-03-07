---
title: use-module-for-folder-structure
priority: 1
---

## use-module-for-folder-structure

Use module field to map domain concepts to source code folder structure. Module names MUST exactly match folder paths where they exist using dot notation for nesting.

**DO**

Module names follow same conventions as classes and match actual folder structure

Module MUST exactly match source code folder structure using dot notation

```
File location: src/repl_cli/repl_session.py
```

```
Module: 'repl_cli'
```

```
File location: src/repl_cli/cli_bot/cli_bot.py
```

```
Module: 'repl_cli.cli_bot'
```

```
File location: src/actions/render/synchronizer.py
```

```
Module: 'actions.render'
```

```
(Use dot notation for nested folders, omit 'src' prefix)
```

Module names are clear
descriptive
and match actual folder names (not generic terms)

```
REPLSession
```

```
    module: 'repl_cli'
```

```
CLIBot
```

```
    module: 'repl_cli.cli_bot'
```

```
BuildKnowledgeAction
```

```
    module: 'actions.build'
```

```
(Clear names that match real folders: repl_cli/, actions/render/, scanners/domain_model/)
```

Every domain concept MUST have a module field - no exceptions

```
ValidateRulesAction
```

```
    module: 'actions.validate'
```

```
    responsibilities: [...]
```

```
Scanner
```

```
    module: 'scanners'
```

```
    responsibilities: [...]
```

```
(All concepts include module field mapping to their source location)
```

**DO NOT**

Don't use generic module names
don't omit module field
don't use slash notation

Don't include 'src' prefix or use slash notation instead of dots

```
REPLSession
```

```
    module: 'src/repl_cli' (WRONG: includes src prefix)
```

```
CLIBot
```

```
    module: 'repl_cli/cli_bot' (WRONG: uses slashes instead of dots)
```

```
(Should be: 'repl_cli' and 'repl_cli.cli_bot' with dots, no src prefix)
```

Don't use generic or vague module names - match actual folder names

```
Scanner
```

```
    module: 'utils' (WRONG: too generic)
```

```
ValidationRule
```

```
    module: 'helpers' (WRONG: generic helper name)
```

```
(Should use actual folder names: 'scanners.domain_model', 'rules.validation')
```

Don't omit the module field - every concept requires it

```
DomainConcept
```

```
    responsibilities: [
```

```
        { name: 'Some responsibility', collaborators: [] }
```

```
    ]
```

```
(WRONG: missing module field)
```

```
(Every concept MUST include module field mapping to source folder)
```