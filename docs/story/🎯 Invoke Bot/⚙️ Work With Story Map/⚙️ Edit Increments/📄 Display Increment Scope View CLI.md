# 📄 Display Increment Scope View CLI

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/edit_story_map/test_edit_increments.py#L5)

**User:** User
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Edit Increments](.)  
**Sequential Order:** 9
**Story Type:** user

## Story Description

Display Increment Scope View CLI functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-contains-these-stories"></a>
### Scenario: [contains these Stories:](#scenario-contains-these-stories) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_edit_increments.py#L11)

**Steps:**
```gherkin
Given story graph contains increments with stories assigned
And CLI session is active
When User requests increment view via CLI
Then CLI returns Increments object containing collection of Increment
And each Increment contains name, priority, and stories array
And stories array contains Story objects from StoryNode
```

**Example 1: MVP Release with its Stories - The Increment::**

| increment_name | increment_priority |
| --- | --- |
| MVP Release | 1 |


**contains these Stories::**

| increment_name | story_name | sequential_order |
| --- | --- | --- |
| MVP Release | Create Profile | 1 |
| MVP Release | Authenticate User | 2 |


**Example 2: Enhancement Release with its Stories - The Increment::**

| increment_name | increment_priority |
| --- | --- |
| Enhancement Release | 2 |


**contains these Stories::**

| increment_name | story_name | sequential_order |
| --- | --- | --- |
| Enhancement Release | Add Payment Method | 1 |
| Enhancement Release | View History | 2 |


<a id="scenario-producing-this-cli-output"></a>
### Scenario: [producing this CLI output:](#scenario-producing-this-cli-output) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_edit_increments.py#L50)

**Steps:**
```gherkin
Given story graph contains increments with stories assigned
And CLI session is active
When User enters increment view command
Then CLI displays each increment with name as header
And CLI lists stories in natural sequential order under each increment
And output is simple list format without hierarchy nesting
```

**Example 1: MVP Release displays its Stories - The Increment::**

| increment_name | increment_priority |
| --- | --- |
| MVP Release | 1 |


**displays these Stories in natural order::**

| increment_name | story_name | sequential_order |
| --- | --- | --- |
| MVP Release | Create Profile | 1 |
| MVP Release | Authenticate User | 2 |


**producing this CLI output::**

| expected_output |
| --- |
| MVP Release:\n  - Create Profile\n  - Authenticate User |


**Example 2: Enhancement Release displays its Stories - The Increment::**

| increment_name | increment_priority |
| --- | --- |
| Enhancement Release | 2 |


**displays these Stories in natural order::**

| increment_name | story_name | sequential_order |
| --- | --- | --- |
| Enhancement Release | Add Payment Method | 1 |
| Enhancement Release | View History | 2 |


**producing this CLI output::**

| expected_output |
| --- |
| Enhancement Release:\n  - Add Payment Method\n  - View History |


<a id="scenario-produces-this-cli-output"></a>
### Scenario: [produces this CLI output:](#scenario-produces-this-cli-output) (edge_case)  | [Test](/test/invoke_bot/edit_story_map/test_edit_increments.py#L77)

**Steps:**
```gherkin
Given story graph contains an increment with no stories assigned
And CLI session is active
When User enters increment view command
Then CLI displays increment name as header
And CLI shows empty state message for increment with no stories
```

**The Increment with no stories::**

| increment_name | increment_priority |
| --- | --- |
| Backlog | 99 |


**produces this CLI output::**

| expected_output |
| --- |
| Backlog:\n  (no stories) |


<a id="scenario-storynode-integration"></a>
### Scenario: [StoryNode integration](#scenario-storynode-integration) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_edit_increments.py#L105)

**Steps:**
```gherkin
Given story graph contains increments referencing Story nodes
And CLI session is active
When User requests increment view via CLI
Then CLI returns Increments collection
And Increment.stories contains references to existing StoryNode objects
And Story objects include standard StoryNode properties
```

**StoryNode integration:**

| story_property | source | included_in_increment_view |
| --- | --- | --- |
| name | StoryNode.name | yes |
| test_class | StoryNode.test_class | yes |
| sequential_order | StoryNode.sequential_order | yes |


<a id="scenario-story-graph-with-no-increments-defined"></a>
### Scenario: [Story graph with no Increments defined:](#scenario-story-graph-with-no-increments-defined) (error_case)  | [Test](/test/invoke_bot/edit_story_map/test_edit_increments.py#L130)

**Steps:**
```gherkin
Given story graph contains no increments
And CLI session is active
When User requests increment view via CLI
Then CLI displays no increments defined message
And CLI returns empty Increments collection
```

**Story graph with no Increments defined::**

| increment_count | expected_message |
| --- | --- |
| 0 | No increments defined in story graph |

