# 📄 Open All Related Files

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio)

**User:** User
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Open Story Related Files](.)  
**Sequential Order:** 0.0
**Story Type:** user

## Story Description

Open related files for selected story graph node using button group next to submit button. Buttons open story graph, story files, test files, and code files in organized split editors.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **WHEN** user clicks Graph button **THEN** system opens story-graph.json **AND** system collapses all nodes **AND** system expands nodes representing selected node in tree **AND** system positions edit cursor at line of beginning of expanded section representing selected node
- **WHEN** user clicks Stories button **THEN** system opens story markdown files for single story or all stories under selected node
- **WHEN** user clicks Test button **THEN** system opens test files with methods/classes in scope **AND** system collapses other methods/classes
- **WHEN** user clicks Code button **THEN** system infers code files associated with tests **AND** system opens code files (not in story map, must be inferred)
- **WHEN** user clicks All button **THEN** system opens all files in separate split editors **AND** system arranges story graph leftmost **AND** system arranges scenarios in next split **AND** system arranges tests in next split **AND** system arranges code in rightmost split
- **WHEN** user executes CLI command `bot.<story hierarchy>.openStoryFile()` **THEN** system opens story markdown files for node **AND** system opens all story files recursively for children if epic or sub-epic
- **WHEN** user executes CLI command `bot.<story hierarchy>.openTest()` **THEN** system opens test files for node **AND** system opens all test files recursively for children if epic or sub-epic
- **WHEN** user executes CLI command `bot.<story hierarchy>.openStoryGraph()` **THEN** system opens story-graph.json **AND** system collapses all nodes **AND** system expands nodes representing node path in tree

## Scenarios

<a id="scenario-graph-button-opens-story-graph-with-selected-node-expanded"></a>
### Scenario: [Graph button opens story graph with selected node expanded](#scenario-graph-button-opens-story-graph-with-selected-node-expanded) (happy_path)

**Steps:**
```gherkin
GIVEN: User has selected a story graph node
WHEN: User clicks Graph button
THEN: System opens story-graph.json file
AND: System collapses all nodes in story graph view
AND: System expands nodes representing selected node path in tree
AND: System positions edit cursor at line of beginning of expanded section representing selected node
```

**Examples:**

**Example 1: Graph button opens story graph for story node**

**Story node:**
| node_type | node_name | node_path |
| --- | --- | --- |
| story | Open All Related Files | Invoke Bot.Work With Story Map.Open Story Related Files.Open All Related Files |

**Story Graph File:**
- File: `docs/stories/story-graph.json`
- Line 11408: Story "Open All Related Files" definition starts
- System collapses all epic/sub-epic nodes
- System expands path: `Invoke Bot` → `Work With Story Map` → `Open Story Related Files` → `Open All Related Files`
- Edit cursor positioned at line 11408

**Example 2: Graph button opens story graph for sub-epic node**

**Sub-epic "Work With Story Map":**
| node_type | node_name | node_path | line_number |
| --- | --- | --- | --- |
| sub-epic | Work With Story Map | Invoke Bot.Work With Story Map | 3341 |

**Nested sub-epics under "Work With Story Map":**
| sub_epic_name | line_number |
| --- | --- |
| Open Story Related Files | 11400 |
| Scope Files | 3348 |

**Story Graph File:**
- File: `docs/stories/story-graph.json`
- Line 3341: SubEpic "Work With Story Map" definition starts
- System collapses all nodes
- System expands path: `Invoke Bot` → `Work With Story Map` (and all nested sub-epics shown above)
- Edit cursor positioned at line 3341

<a id="scenario-stories-button-opens-story-markdown-files"></a>
### Scenario: [Stories button opens story markdown files](#scenario-stories-button-opens-story-markdown-files) (happy_path)

**Steps:**
```gherkin
GIVEN: User has selected a story graph node (story, sub-epic, or epic)
WHEN: User clicks Stories button
THEN: System opens story markdown file for single story if story selected
OR: System opens all story markdown files for stories under selected node if sub-epic or epic selected
```

**Examples:**

**Example 1: Stories button opens single story file**

**Story node:**
| node_type | node_name | file_link |
| --- | --- | --- |
| story | Open All Related Files | docs/stories/map/Invoke Bot/Work With Story Map/Open Story Related Files/📄 Open All Related Files.md |

**Result:**
- Opens: `docs/stories/map/Invoke Bot/Work With Story Map/Open Story Related Files/📄 Open All Related Files.md`
- Single file opened in editor

**Example 2: Stories button opens all story files for sub-epic**

**Sub-epic "Open Story Related Files":**
| node_type | node_name | story_count |
| --- | --- | --- |
| sub-epic | Open Story Related Files | 2 |

**Stories under "Open Story Related Files":**
| story_name | file_link |
| --- | --- |
| Open All Related Files | docs/stories/map/Invoke Bot/Work With Story Map/Open Story Related Files/📄 Open All Related Files.md |
| Enrich Scope With Links | docs/stories/map/Invoke Bot/Work With Story Map/Open Story Related Files/📄 Enrich Scope With Links.md |

**Result:**
- Both story files opened sequentially in editor

<a id="scenario-test-button-opens-test-files-with-scope-collapsed"></a>
### Scenario: [Test button opens test files with scope collapsed](#scenario-test-button-opens-test-files-with-scope-collapsed) (happy_path)

**Steps:**
```gherkin
GIVEN: User has selected a story graph node with test files
WHEN: User clicks Test button
THEN: System opens test files associated with selected node
AND: System expands methods/classes in scope (test_class or test_method)
AND: System collapses other methods/classes in test files
```

**Examples:**

**Example 1: Test button opens test file for story with test_class**

**Story node:**
| node_type | node_name | test_file | test_class |
| --- | --- | --- | --- |
| story | Enrich Scope With Links | null | TestEnrichScopeWithLinks |

**Test File Structure:**
- File: `test/invoke_bot/edit_story_map/test_manage_story_scope.py`
- Class: `TestEnrichScopeWithLinks` (expanded)
- Other classes collapsed: `TestNavigateStoryGraphUsingCLI`, `TestCreateScopeUsingCLI`, `TestDisplayScopeUsingCLI`, `TestCreateScope`, `TestExecuteActionsWithScope`, `TestExecuteActionScopedToStoryNode`

**Result:**
- Opens test file
- Expands `TestEnrichScopeWithLinks` class
- Collapses all other test classes

**Example 2: Test button opens test file for sub-epic with test_file**

**Sub-epic "Work With Story Map":**
| node_type | node_name | test_file |
| --- | --- | --- |
| sub-epic | Work With Story Map | test/invoke_bot/edit_story_map/ |

**Stories with tests under "Work With Story Map":**
| story_name | test_class | test_file |
| --- | --- | --- |
| Enrich Scope With Links | TestEnrichScopeWithLinks | test/invoke_bot/edit_story_map/test_manage_story_scope.py |
| Add Filter Part To File Scope | TestAddFilterPartToFileScope | test/invoke_bot/edit_story_map/test_scope_files.py |

**Test Files Opened:**
- `test/invoke_bot/edit_story_map/test_manage_story_scope.py`
  - Expanded: `TestEnrichScopeWithLinks` class (for "Enrich Scope With Links" story)
  - Collapsed: Other test classes
- `test/invoke_bot/edit_story_map/test_scope_files.py`
  - Expanded: `TestAddFilterPartToFileScope` class (for "Add Filter Part To File Scope" story)
  - Collapsed: Other test classes

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

**Examples:**

**Example 1: Code button infers code file from test file path**

**Story node:**
| node_type | node_name | test_file | inferred_code_file |
| --- | --- | --- | --- |
| story | Enrich Scope With Links | test/invoke_bot/edit_story_map/test_manage_story_scope.py | src/story_graph/nodes.py |

**Inference Logic:**
- Test file: `test/invoke_bot/edit_story_map/test_manage_story_scope.py`
- Test imports: `from story_graph.nodes import StoryNode, Epic, SubEpic, Story`
- Inferred code file: `src/story_graph/nodes.py`
- Classes expanded: `StoryNode`, `Epic`, `SubEpic`, `Story` (referenced in tests)
- Other classes collapsed

**Example 2: Code button infers multiple code files from sub-epic test directory**

**Sub-epic "Work With Story Map":**
| node_type | node_name | test_file | inferred_code_file_count |
| --- | --- | --- | --- |
| sub-epic | Work With Story Map | test/invoke_bot/edit_story_map/ | 2 |

**Test files under "Work With Story Map" and their inferred code files:**
| test_file | inferred_code_file | classes_expanded |
| --- | --- | --- |
| test/invoke_bot/edit_story_map/test_manage_story_scope.py | src/story_graph/nodes.py | StoryNode, Epic, SubEpic, Story |
| test/invoke_bot/edit_story_map/test_manage_story_scope.py | src/navigation/domain_navigator.py | DomainNavigator |
| test/invoke_bot/edit_story_map/test_scope_files.py | src/story_graph/nodes.py | StoryNode, Epic, SubEpic |

**Inference Logic:**
- Test directory: `test/invoke_bot/edit_story_map/`
- Test files import from: `story_graph.nodes`, `navigation.domain_navigator`
- Inferred code files opened with referenced classes expanded, others collapsed

<a id="scenario-all-button-opens-files-in-split-editors"></a>
### Scenario: [All button opens files in split editors](#scenario-all-button-opens-files-in-split-editors) (happy_path)

**Steps:**
```gherkin
GIVEN: User has selected a story graph node
WHEN: User clicks All button
THEN: System opens story-graph.json in leftmost split editor
AND: System opens story markdown files in next split editor to the right
AND: System opens test files in next split editor to the right
AND: System opens code files in rightmost split editor
AND: System applies Graph button behavior to story graph (collapse all, expand selected)
AND: System applies Test button behavior to test files (expand scope, collapse others)
AND: System applies Code button behavior to code files (expand referenced, collapse others)
```

**Examples:**

**Example 1: All button opens all related files for story node**

**Story node:**
| node_type | node_name | file_link | test_class |
| --- | --- | --- | --- |
| story | Enrich Scope With Links | docs/stories/map/Invoke Bot/Work With Story Map/Open Story Related Files/📄 Enrich Scope With Links.md | TestEnrichScopeWithLinks |

**Files Opened in Split Editors (left to right):**

**Editor 1 (leftmost):**
- File: `docs/stories/story-graph.json`
- Behavior: Collapsed all nodes, expanded path to "Enrich Scope With Links" story
- Cursor: Line 11421 (story definition start)

**Editor 2:**
- File: `docs/stories/map/Invoke Bot/Work With Story Map/Open Story Related Files/📄 Enrich Scope With Links.md`
- Story markdown file content

**Editor 3:**
- File: `test/invoke_bot/edit_story_map/test_manage_story_scope.py`
- Expanded: `TestEnrichScopeWithLinks` class
- Expanded: `test_story_with_test_file_and_class_gets_test_link` method
- Collapsed: All other test classes

**Editor 4 (rightmost):**
- File: `src/story_graph/nodes.py`
- Expanded: Classes referenced in tests (`StoryNode`, `Epic`, `SubEpic`, `Story`)
- Collapsed: Other classes

**Example 2: All button opens all related files for sub-epic node**

**Sub-epic "Work With Story Map":**
| node_type | node_name | test_file | story_count | test_file_count |
| --- | --- | --- | --- | --- |
| sub-epic | Work With Story Map | test/invoke_bot/edit_story_map/ | 20+ | 2+ |

**Stories under "Work With Story Map":**
| story_name | file_link | test_class | test_file |
| --- | --- | --- | --- |
| Open All Related Files | docs/stories/map/Invoke Bot/Work With Story Map/Open Story Related Files/📄 Open All Related Files.md | null | null |
| Enrich Scope With Links | docs/stories/map/Invoke Bot/Work With Story Map/Open Story Related Files/📄 Enrich Scope With Links.md | TestEnrichScopeWithLinks | test/invoke_bot/edit_story_map/test_manage_story_scope.py |
| Add Filter Part To File Scope | docs/stories/map/Invoke Bot/Work With Story Map/Scope Files/Set File Filter/📄 Add Filter Part To File Scope.md | TestAddFilterPartToFileScope | test/invoke_bot/edit_story_map/test_scope_files.py |

**Files Opened in Split Editors (left to right):**

**Editor 1 (leftmost):**
- File: `docs/stories/story-graph.json`
- Expanded: `Invoke Bot` → `Work With Story Map` (and all nested children)
- Cursor: Line 3341

**Editor 2:**
- Story markdown files:
  1. `docs/stories/map/Invoke Bot/Work With Story Map/Open Story Related Files/📄 Open All Related Files.md`
  2. `docs/stories/map/Invoke Bot/Work With Story Map/Open Story Related Files/📄 Enrich Scope With Links.md`
  3. `docs/stories/map/Invoke Bot/Work With Story Map/Scope Files/Set File Filter/📄 Add Filter Part To File Scope.md`
  4. ... (all stories under sub-epic)

**Editor 3:**
- Test files:
  1. `test/invoke_bot/edit_story_map/test_manage_story_scope.py`
     - Expanded: `TestEnrichScopeWithLinks` class
  2. `test/invoke_bot/edit_story_map/test_scope_files.py`
     - Expanded: `TestAddFilterPartToFileScope` class

**Editor 4 (rightmost):**
- Code files inferred from test files:
  1. `src/story_graph/nodes.py` (referenced by tests)
     - Expanded: `StoryNode`, `Epic`, `SubEpic`, `Story` classes
  2. `src/navigation/domain_navigator.py` (referenced by tests)
     - Expanded: `DomainNavigator` class

<a id="scenario-cli-open-story-file-opens-story-markdown-files"></a>
### Scenario: [CLI openStoryFile opens story markdown files](#scenario-cli-open-story-file-opens-story-markdown-files) (happy_path)

**Steps:**
```gherkin
GIVEN: User executes CLI command bot.story_graph."Epic Name".openStoryFile()
WHEN: Command executes on epic or sub-epic node
THEN: System opens story markdown files for all stories under node
AND: System recursively opens story files for all nested children (sub-epics and stories)
WHEN: Command executes on story node
THEN: System opens single story markdown file for that story
```

**Examples:**

**Example 1: CLI openStoryFile on epic opens all story files recursively**

**Epic "Invoke Bot":**
| command | epic_name | story_file_count |
| --- | --- | --- |
| bot.story_graph."Invoke Bot".openStoryFile() | Invoke Bot | 50+ |

**Sub-epics under "Invoke Bot":**
| sub_epic_name | story_count |
| --- | --- |
| Initialize Bot | 10+ |
| Work With Story Map | 20+ |
| Navigate Behavior Actions | 15+ |

**Sample stories under sub-epics:**
| sub_epic_name | story_name | file_link |
| --- | --- | --- |
| Initialize Bot | Resolve Bot Path | docs/stories/map/Invoke Bot/Initialize Bot/Load Bot, Behavior, and Actions/📄 Resolve Bot Path.md |
| Initialize Bot | Resolve Bot Path Using CLI | docs/stories/map/Invoke Bot/Initialize Bot/Load Bot, Behavior, and Actions/📄 Resolve Bot Path Using CLI.md |
| Work With Story Map | Open All Related Files | docs/stories/map/Invoke Bot/Work With Story Map/Open Story Related Files/📄 Open All Related Files.md |
| Work With Story Map | Enrich Scope With Links | docs/stories/map/Invoke Bot/Work With Story Map/Open Story Related Files/📄 Enrich Scope With Links.md |

**Result:**
- All story files under epic opened recursively (50+ files from all sub-epics, including sample stories shown above)

**Example 2: CLI openStoryFile on sub-epic opens stories under that sub-epic**

**Sub-epic "Open Story Related Files":**
| command | sub_epic_name | story_count |
| --- | --- | --- |
| bot.story_graph."Invoke Bot"."Work With Story Map"."Open Story Related Files".openStoryFile() | Open Story Related Files | 2 |

**Stories under "Open Story Related Files":**
| story_name | file_link |
| --- | --- |
| Open All Related Files | docs/stories/map/Invoke Bot/Work With Story Map/Open Story Related Files/📄 Open All Related Files.md |
| Enrich Scope With Links | docs/stories/map/Invoke Bot/Work With Story Map/Open Story Related Files/📄 Enrich Scope With Links.md |

**Result:**
- Both story files opened

**Example 3: CLI openStoryFile on story opens single file**

**Story node:**
| command | story_name |
| --- | --- |
| bot.story_graph."Invoke Bot"."Work With Story Map"."Open Story Related Files"."Open All Related Files".openStoryFile() | Open All Related Files |

**Story File Opened:**
- `docs/stories/map/Invoke Bot/Work With Story Map/Open Story Related Files/📄 Open All Related Files.md`

<a id="scenario-cli-open-test-opens-test-files-recursively"></a>
### Scenario: [CLI openTest opens test files recursively](#scenario-cli-open-test-opens-test-files-recursively) (happy_path)

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

**Examples:**

**Example 1: CLI openTest on sub-epic opens test files recursively**

**Sub-epic "Work With Story Map":**
| command | sub_epic_name | test_file | test_file_count |
| --- | --- | --- | --- |
| bot.story_graph."Invoke Bot"."Work With Story Map".openTest() | Work With Story Map | test/invoke_bot/edit_story_map/ | 2+ |

**Stories with tests under "Work With Story Map":**
| story_name | test_class | test_file |
| --- | --- | --- |
| Enrich Scope With Links | TestEnrichScopeWithLinks | test/invoke_bot/edit_story_map/test_manage_story_scope.py |
| Add Filter Part To File Scope | TestAddFilterPartToFileScope | test/invoke_bot/edit_story_map/test_scope_files.py |

**Scenarios with test methods under stories:**
| story_name | scenario | test_method |
| --- | --- | --- |
| Enrich Scope With Links | Story with test_file and test_class gets test tube icon link | test_story_with_test_file_and_class_gets_test_link |
| Add Filter Part To File Scope | Add filter part to file scope | test_add_filter_part_to_file_scope |

**Test Files Opened:**
1. `test/invoke_bot/edit_story_map/test_manage_story_scope.py`
   - Expanded: `TestEnrichScopeWithLinks` class (for "Enrich Scope With Links" story)
   - Expanded: `test_story_with_test_file_and_class_gets_test_link` method
   - Collapsed: Other test classes
2. `test/invoke_bot/edit_story_map/test_scope_files.py`
   - Expanded: `TestAddFilterPartToFileScope` class (for "Add Filter Part To File Scope" story)
   - Expanded: `test_add_filter_part_to_file_scope` method
   - Collapsed: Other test classes

**Example 2: CLI openTest on story with test_class**

**Story "Enrich Scope With Links":**
| command | story_name | test_class | test_file |
| --- | --- | --- | --- |
| bot.story_graph."Invoke Bot"."Work With Story Map"."Open Story Related Files"."Enrich Scope With Links".openTest() | Enrich Scope With Links | TestEnrichScopeWithLinks | test/invoke_bot/edit_story_map/test_manage_story_scope.py |

**Scenarios with test methods under "Enrich Scope With Links":**
| scenario | test_method |
| --- | --- |
| Story with test_file and test_class gets test tube icon link | test_story_with_test_file_and_class_gets_test_link |
| Story with test_class but no test_file gets no test icon | test_story_with_test_class_but_no_test_file_gets_no_test_icon |

**Test File Opened:**
- File: `test/invoke_bot/edit_story_map/test_manage_story_scope.py`
- Expanded: `TestEnrichScopeWithLinks` class
- Expanded: All test methods (`test_story_with_test_file_and_class_gets_test_link`, `test_story_with_test_class_but_no_test_file_gets_no_test_icon`)
- Collapsed: All other test classes and methods

<a id="scenario-cli-open-story-graph-opens-with-node-expanded"></a>
### Scenario: [CLI openStoryGraph opens with node expanded](#scenario-cli-open-story-graph-opens-with-node-expanded) (happy_path)

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

**Examples:**

**Example 1: CLI openStoryGraph on epic**

**Epic "Invoke Bot":**
| command | epic_name | line_number |
| --- | --- | --- |
| bot.story_graph."Invoke Bot".openStoryGraph() | Invoke Bot | 477 |

**Sub-epics under "Invoke Bot":**
| sub_epic_name | line_number |
| --- | --- |
| Initialize Bot | 483 |
| Work With Story Map | 3341 |
| Navigate Behavior Actions | 4770 |

**Story Graph File:**
- File: `docs/stories/story-graph.json`
- Line 477: Epic "Invoke Bot" definition starts: `"name": "Invoke Bot"`
- System collapses all other epics
- System expands: `Invoke Bot` epic and all its sub-epics
- Edit cursor positioned at line 477

**Example 2: CLI openStoryGraph on story**

**Story node:**
| command | story_name | line_number |
| --- | --- | --- |
| bot.story_graph."Invoke Bot"."Work With Story Map"."Open Story Related Files"."Open All Related Files".openStoryGraph() | Open All Related Files | 11408 |

**Story Graph File:**
- File: `docs/stories/story-graph.json`
- Line 11408: Story "Open All Related Files" definition starts: `"name": "Open All Related Files"`
- System collapses all nodes
- System expands path: `Invoke Bot` → `Work With Story Map` → `Open Story Related Files` → `Open All Related Files`
- Edit cursor positioned at line 11408
