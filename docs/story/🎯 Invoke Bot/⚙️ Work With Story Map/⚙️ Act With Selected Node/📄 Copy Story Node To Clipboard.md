# 📄 Copy Story Node To Clipboard

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/edit_story_map/test_submit_scoped_action.py#L1212)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Act With Selected Node](.)  
**Sequential Order:** 4.0
**Story Type:** user

## Story Description

Copy Story Node To Clipboard functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-storynode-copy_name-returns-node-name-for-clipboard"></a>
### Scenario: [StoryNode copy_name returns node name for clipboard](#scenario-storynode-copy_name-returns-node-name-for-clipboard) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_submit_scoped_action.py#L1215)

**Steps:**
```gherkin
GIVEN: StoryMap is loaded with at least one Epic containing a SubEpic
AND: Bot has that StoryMap loaded
WHEN: copy_name is invoked on that SubEpic StoryNode
THEN: StoryNode.copy_name returns status success
AND: result is the node name
AND: the result can be written to system clipboard by the panel
```


<a id="scenario-storynode-copy_json-returns-node-as-story-graph-json"></a>
### Scenario: [StoryNode copy_json returns node as story-graph JSON](#scenario-storynode-copy_json-returns-node-as-story-graph-json) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_submit_scoped_action.py#L1285)

**Steps:**
```gherkin
GIVEN: StoryMap is loaded with an Epic and a SubEpic with known structure
AND: Bot has that StoryMap loaded
WHEN: copy_json is invoked on that SubEpic StoryNode
THEN: StoryNode.copy_json returns status success
AND: result is a dict with the same shape as the node in story-graph.json
AND: the result can be serialized to JSON and written to system clipboard by the panel
```


<a id="scenario-cli-resolves-story_graph-path-and-copy_name-returns-node-name"></a>
### Scenario: [CLI resolves story_graph path and copy_name returns node name](#scenario-cli-resolves-story_graph-path-and-copy_name-returns-node-name) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_submit_scoped_action.py#L1574)

**Steps:**
```gherkin
GIVEN: StoryMap is loaded with Epic "Invoke Bot" and SubEpic "Manage Bot"
AND: Bot has that StoryMap loaded
WHEN: User executes CLI command story_graph."Invoke Bot"."Manage Bot".copy_name
THEN: CLI returns success
AND: response result is the SubEpic node name "Manage Bot"
```


<a id="scenario-cli-resolves-story_graph-path-and-copy_json-returns-node-dict"></a>
### Scenario: [CLI resolves story_graph path and copy_json returns node dict](#scenario-cli-resolves-story_graph-path-and-copy_json-returns-node-dict) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_submit_scoped_action.py#L1604)

**Steps:**
```gherkin
GIVEN: StoryMap is loaded with Epic "Invoke Bot" and SubEpic "Manage Bot"
AND: Bot has that StoryMap loaded
WHEN: User executes CLI command story_graph."Invoke Bot"."Manage Bot".copy_json
THEN: CLI returns success
AND: response result is a dict with name "Manage Bot" and story-graph shape for that node
```


<a id="scenario-cli-copy_name-on-non-existent-node-path-returns-error"></a>
### Scenario: [CLI copy_name on non-existent node path returns error](#scenario-cli-copy_name-on-non-existent-node-path-returns-error) (error_case)  | [Test](/test/invoke_bot/edit_story_map/test_submit_scoped_action.py#L1636)

**Steps:**
```gherkin
GIVEN: StoryMap is loaded with Epic "Invoke Bot" and SubEpic "Manage Bot"
AND: Bot has that StoryMap loaded
WHEN: User executes CLI command story_graph."Invoke Bot"."Non-existent Node".copy_name
THEN: CLI returns error
AND: output indicates node not found or path invalid
AND: no result is written to clipboard
```

