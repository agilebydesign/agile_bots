## Available Cursor Commands for story_bot:

---

## story_bot

Execute the current action and current behavior in the story_bot workflow.

```
/story_bot
```

## story_bot-continue

Close current action and continue to next action in workflow

```
/story_bot-continue
```

## story_bot-get_working_dir

Get Working Dir

```
/story_bot-get_working_dir
```

## story_bot-help

List all available cursor commands and their parameters

```
/story_bot-help
```

## story_bot-set_working_dir

Set Working Dir

```
/story_bot-set_working_dir
```

## story_bot-shape

Outline a story map made up of epics, sub-epics, and stories

```
/story_bot-shape
```

## story_bot-prioritization

Organize stories into delivery increments based on business value, dependencies, and risk

```
/story_bot-prioritization
```

## story_bot-discovery

Create a complete list of stories with a well defined story flow for one increment

```
/story_bot-discovery
```

## story_bot-exploration

Define acceptance criteria (When/Then) for stories to establish clear success criteria

```
/story_bot-exploration
```

## story_bot-scenarios

Write detailed plain-English scenarios (Given/When/Then) that specify exact behavior for each story

```
/story_bot-scenarios
```

## story_bot-tests

Write test files (.py, .js, etc.) with executable test code from scenarios/examples that validate story behavior

```
/story_bot-tests
```

## story_bot-code

Generate production source code from domain model and story specifications

```
/story_bot-code
```

## story_bot-code-rules

Load code behavior rules into AI context for guidance on writing clean, maintainable production code

```
/story_bot-code-rules
```

## story_bot-discovery-rules

Load discovery behavior rules into AI context for guidance on story decomposition and flow

```
/story_bot-discovery-rules
```

## story_bot-exploration-rules

Load exploration behavior rules into AI context for guidance on defining acceptance criteria

```
/story_bot-exploration-rules
```

## story_bot-prioritization-rules

Load prioritization behavior rules into AI context for guidance on organizing delivery increments

```
/story_bot-prioritization-rules
```

## story_bot-scenarios-rules

Load scenarios behavior rules into AI context for guidance on writing clear, testable scenarios

```
/story_bot-scenarios-rules
```

## story_bot-shape-rules

Load shape behavior rules into AI context for guidance on story mapping and domain modeling

```
/story_bot-shape-rules
```

## story_bot-tests-rules

Load tests behavior rules into AI context for guidance on writing effective, well-structured tests

```
/story_bot-tests-rules
```

## story_bot_repl

Launch the Story Bot interactive REPL session in the background and act as an intermediary between the user and the REPL.

```
/story_bot_repl
```

---

## Action Help

### clarify

Gather context by asking required questions and collecting evidence in order to increase understanding

```
/story_bot-<behavior> clarify [parameters]

--answers <value>:   Dict mapping question keys to answer strings
--evidence-provided <value>:   Dict mapping evidence types to evidence content
--context <value>:   Optional parameter
```

### strategy

decide approach by capturing assumptions and decision criteria

```
/story_bot-<behavior> strategy [parameters]

--decisions-made <value>:   Dict mapping decision criteria keys to selected options/values
--assumptions <value>:   List of assumption strings
--assumptions-made <value>:   List of assumption strings
```

### build

build action

```
/story_bot-<behavior> build [parameters]

--scope <value>:   Scope structure: {'type': 'story'|'epic'|'increment'|'all', 'value': <names|priorities>}
```

### validate

Validate knowledge graph and/or artifacts against behavior-specific rules, checking for violations and compliance

**NOTE:** For code behavior, validation runs in background. You MUST poll the status file every 10 seconds and report progress until complete.

```
/story_bot-<behavior> validate [parameters]

--scope <value>:   Scope structure: {'type': 'story'|'epic'|'increment'|'all'|'files', 'value': <names|priorities|files>, 'exclude': <patterns>}
--background <value>:   Optional parameter
--skip-cross-file <bool>:   Optional parameter
--all-files <bool>:   Optional parameter
--force-full <bool>:   Optional parameter
--max-cross-file-comparisons <int>:   Optional parameter
```

### render

Render output documents and artifacts from knowledge graph using templates and synchronizers

```
/story_bot-<behavior> render [parameters]

--scope <value>:   Scope structure: {'type': 'story'|'epic'|'increment'|'all', 'value': <names|priorities>}
```

---
