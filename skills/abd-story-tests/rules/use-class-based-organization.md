---
title: use-class-based-organization
priority: 1
---

## use-class-based-organization

Class = story (Test<ExactStoryName>)
Method = scenario (test_<scenario_snake_case>). Getting this wrong creates files in wrong locations requiring deletion/recreation. BEFORE writing any test code
identify the parent sub-epic that contains the story.

**DO**

Map story hierarchy to test structure exactly. CRITICAL: File name comes from SUB-EPIC
not story.

BEFORE writing code: Identify parent sub-epic and state file path explicitly

```
# File: test/domain/test_edit_story_graph.py
```

```
# Class: TestCreateChildStoryNode
```

Test file matches sub-epic name in snake_case

```
# Sub-epic: 'Generate Bot Server And Tools'
```

```
# File: test_generate_bot_server_and_tools.py
```

Test class matches story name EXACTLY in PascalCase

```
# Story: 'Inject Guardrails as Part of Clarify Requirements'
```

```
class TestInjectGuardrailsAsPartOfClarifyRequirements:
```

Test method matches scenario name EXACTLY in snake_case

```
# Scenario: 'Generator creates bot tool for test_bot'
```

```
def test_generator_creates_bot_tool_for_test_bot(self):
```

Test classes in same order as stories in story map

```
class TestGenerateBotTools:  # First story
```

```
class TestGenerateBehaviorTools:  # Second story
```

Check if file already exists - add to existing file
don't create duplicate

```
# Add new class TestDeleteStoryNode to existing file
```

```
# Do NOT create test_delete_story_node.py
```

**DO NOT**

Don't use generic/abbreviated names or wrong hierarchy level for file naming. Don't create files in wrong locations.

Don't name file after story - use parent sub-epic

```
# Story: 'Create Child Story Node'
```

```
# WRONG: test_create_child_story_node.py
```

Don't create new test directories

```
# WRONG: test/story_graph/
```

```
# RIGHT: test/domain/ (existing directory)
```

Don't create separate helper files

```
# WRONG: test/story_graph/story_graph_test_helper.py
```

```
# RIGHT: Add methods to test/domain/helpers/story_helper.py
```

Don't abbreviate class names

```
class TestGenBotTools:  # WRONG - use TestGenerateBotTools
```

Don't use generic class names

```
class TestGuardrailsInjection:  # WRONG - story is 'Inject Guardrails as Part of Clarify Requirements'
```

Don't abbreviate method names

```
def test_creates_tool(self):  # WRONG - scenario is 'Generator creates bot tool for test_bot'
```

Don't put test classes out of story map order

```
class TestGenerateMCPBotServer:  # WRONG - should be after TestGenerateBotTools
```