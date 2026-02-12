# 📄 Render action diagram section

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L836)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Perform Action](..) / [⚙️ Synchronized Graph with Rendered Diagram Content](.)  
**Sequential Order:** 7
**Story Type:** user

## Story Description

Render action diagram section functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-render-action-shows-existing-render-section-without-drawio-config-and-separate-diagram-section"></a>
### Scenario: [Render action shows existing render section without DrawIO config and separate Diagram section](#scenario-render-action-shows-existing-render-section-without-drawio-config-and-separate-diagram-section) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L852)

**Steps:**
```gherkin
Given user is on the render action
And {StoryMap} has been loaded from story graph
When render action displays its sections
Then existing render section shows all current render content except DrawIO diagram config and output
And a Diagram section is shown separately
And Diagram section links to each {DrawIOStoryMap} diagram file
And Diagram section links to generated {UpdateReport} file when one exists
```


<a id="scenario-diagram-stale-when-file-changed-since-last-sync-shows-indicator-and-refresh"></a>
### Scenario: [Diagram stale when file changed since last sync shows indicator and Refresh](#scenario-diagram-stale-when-file-changed-since-last-sync-shows-indicator-and-refresh) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L937)

**Steps:**
```gherkin
Given {DrawIOStoryMap} exists at a file path
And diagram file was last synchronized at {LayoutData} sync time
And diagram file has been modified after that sync time
When render action displays the Diagram section
Then system visually indicates that diagram is stale
And a Refresh button is shown
When user clicks Refresh
Then system re-extracts from diagram and updates last-refresh time for that diagram
```


<a id="scenario-diagram-with-newer-save-than-last-refresh-shows-pending-and-generate-report"></a>
### Scenario: [Diagram with newer save than last refresh shows pending and Generate report](#scenario-diagram-with-newer-save-than-last-refresh-shows-pending-and-generate-report) ()

**Steps:**
```gherkin
Given {DrawIOStoryMap} has a stored last-refresh date per diagram
And diagram file save time is newer than last-refresh date
When render action displays the Diagram section
Then system indicates pending changes for that diagram
And a Generate report button is shown
When user clicks Generate report
Then system calls {StoryMap}.generateUpdateReport({DrawIOStoryMap}) and writes {UpdateReport} to file
And Diagram section shows link to the report file
```


<a id="scenario-user-opens-update-report-in-editor-and-applies-update-then-may-delete-report"></a>
### Scenario: [User opens update report in editor and applies update then may delete report](#scenario-user-opens-update-report-in-editor-and-applies-update-then-may-delete-report) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L912)

**Steps:**
```gherkin
Given an {UpdateReport} has been generated for a {DrawIOStoryMap} and {StoryMap}
And report file path is known
When user clicks the report link in Diagram section
Then system opens the report file in the editor like other files
When user clicks Update
Then system calls {StoryMap}.update({DrawIOStoryMap}, {UpdateReport})
And story graph is updated from diagram
When update completes
Then user may delete the report file
```


<a id="scenario-update-applies-report-so-each-storynode-parent-and-sequential_order-reflect-diagram"></a>
### Scenario: [Update applies report so each StoryNode parent and sequential_order reflect diagram](#scenario-update-applies-report-so-each-storynode-parent-and-sequential_order-reflect-diagram) ()  | [Test](/test/invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py#L991)

**Steps:**
```gherkin
Given {UpdateReport} contains exact and fuzzy matches from {DrawIOStoryMap} vs {StoryMap}
And {StoryMap} has epics with parent and sequential_order and children
When {StoryMap}.update({DrawIOStoryMap}, {UpdateReport}) runs
Then each updated {StoryNode} has parent from diagram containment
And each updated {StoryNode} has sequential_order from diagram position
And {LayoutData} is persisted for re-render
```


<a id="scenario-diagram-file-does-not-exist-shows-missing-indicator"></a>
### Scenario: [Diagram file does not exist shows missing indicator](#scenario-diagram-file-does-not-exist-shows-missing-indicator) ()

**Steps:**
```gherkin
Given {DrawIOStoryMap} file path is configured but file does not exist
When render action displays the Diagram section
Then Diagram section shows missing diagram indicator for that file
And no Refresh or Generate report buttons are shown
```

