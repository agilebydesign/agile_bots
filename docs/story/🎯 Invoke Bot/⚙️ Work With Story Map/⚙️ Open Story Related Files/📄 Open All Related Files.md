# 📄 Open All Related Files

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/edit_story_map/test_open_story_related_files.py#L20)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Open Story Related Files](.)  
**Sequential Order:** 0.0
**Story Type:** user

## Story Description

Open All Related Files functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** user clicks Graph button
  **then** system opens story-graph.json
  **and** system collapses all nodes
  **and** system expands nodes representing selected node in tree
  **and** system positions edit cursor at line of beginning of expanded section representing selected node

- **When** user clicks Stories button
  **then** system opens story markdown files for single story or all stories under selected node

- **When** user clicks Test button
  **then** system opens test files with methods/classes in scope
  **and** system collapses other methods/classes

- **When** user clicks Code button
  **then** system infers code files associated with tests
  **and** system opens code files (not in story map, must be inferred)

- **When** user clicks All button
  **then** system opens story-graph.json in editor
  **and** system opens exploration file for sub-epic or epic if it exists
  **and** system opens story markdown files for all stories under selected node
  **and** system opens test files for all stories under selected node
  **and** system opens all code files related to opened test files
  **and** system activates story-graph.json tab as last step

- **When** user executes CLI command bot.<story hierarchy>.openStoryFile()
  **then** system opens story markdown files for node
  **and** system opens all story files recursively for children if epic or sub-epic

- **When** user executes CLI command bot.<story hierarchy>.openTest()
  **then** system opens test files for node
  **and** system opens all test files recursively for children if epic or sub-epic

- **When** user executes CLI command bot.<story hierarchy>.openStoryGraph()
  **then** system opens story-graph.json
  **and** system collapses all nodes
  **and** system expands nodes representing node path in tree

## Scenarios

<a id="scenario-graph-button-opens-story-graph-with-selected-node-expanded"></a>
### Scenario: [Graph button opens story graph with selected node expanded](#scenario-graph-button-opens-story-graph-with-selected-node-expanded) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_open_story_related_files.py#L263)

**Steps:**
```gherkin
GIVEN: User has selected a story graph node
WHEN: User clicks Graph button
THEN: System opens story-graph.json file
AND: System collapses all nodes in story graph view
AND: System expands nodes representing selected node path in tree
AND: System positions edit cursor at line of beginning of expanded section representing selected node
```


<a id="scenario-stories-button-opens-story-markdown-files"></a>
### Scenario: [Stories button opens story markdown files](#scenario-stories-button-opens-story-markdown-files) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_open_story_related_files.py#L314)

**Steps:**
```gherkin
GIVEN: User has selected a story graph node (story, sub-epic, or epic)
WHEN: User clicks Stories button
THEN: System opens story markdown file for single story if story selected
OR: System opens all story markdown files for stories under selected node if sub-epic or epic selected
```


<a id="scenario-code-button-infers-and-opens-code-files"></a>
### Scenario: [Code button infers and opens code files](#scenario-code-button-infers-and-opens-code-files) (happy_path)

**Steps:**
```gherkin
GIVEN: User has selected a story graph node with test files
WHEN: User clicks Code button
THEN: System infers code files from test file paths (replace test/ with src/ or remove test_ prefix)
AND: System opens inferred code files
AND: System expands classes/methods referenced in tests
AND: System collapses other code
```


<a id="scenario-all-button-opens-files-in-split-editors"></a>
### Scenario: [All button opens files in split editors](#scenario-all-button-opens-files-in-split-editors) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_open_story_related_files.py#L688)

**Steps:**
```gherkin
GIVEN: User has selected a story graph node
WHEN: User clicks All button
THEN: System opens story-graph.json in editor
AND: System opens exploration file for sub-epic or epic if it exists
AND: System opens story markdown files for all stories under selected node
AND: System opens test files for all stories under selected node
AND: System opens all code files related to opened test files
AND: System activates story-graph.json tab as the last step
```


<a id="scenario-cli-openstoryfile-opens-story-markdown-files"></a>
### Scenario: [CLI openStoryFile opens story markdown files](#scenario-cli-openstoryfile-opens-story-markdown-files) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_open_story_related_files.py#L888)

**Steps:**
```gherkin
GIVEN: User executes CLI command bot.story_graph."Epic Name".openStoryFile()
WHEN: Command executes on epic or sub-epic node
THEN: System opens story markdown files for all stories under node
AND: System recursively opens story files for all nested children (sub-epics and stories)
WHEN: Command executes on story node
THEN: System opens single story markdown file for that story
```


<a id="scenario-cli-opentest-opens-test-files-recursively"></a>
### Scenario: [CLI openTest opens test files recursively](#scenario-cli-opentest-opens-test-files-recursively) (happy_path)

**Steps:**
```gherkin
GIVEN: User executes CLI command bot.story_graph."Epic Name"."SubEpic Name".openTest()
WHEN: Command executes on epic or sub-epic node
THEN: System opens test files for all stories under node
AND: System recursively opens test files for all nested children
AND: System expands test methods/classes in scope for each test file
AND: System collapses other methods/classes
WHEN: Command executes on story node
THEN: System opens test file for that story
AND: System expands test methods/classes in scope (test_class or test_method)
AND: System collapses other methods/classes
```


<a id="scenario-cli-openstorygraph-opens-with-node-expanded"></a>
### Scenario: [CLI openStoryGraph opens with node expanded](#scenario-cli-openstorygraph-opens-with-node-expanded) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_open_story_related_files.py#L1100)

**Steps:**
```gherkin
GIVEN: User executes CLI command bot.story_graph."Epic Name".openStoryGraph()
WHEN: Command executes on any story graph node
THEN: System opens story-graph.json file
AND: System collapses all nodes in story graph view
AND: System expands nodes representing node path in tree
AND: System positions edit cursor at line of beginning of expanded section representing selected node
AND: System highlights selected node in story graph view
```

