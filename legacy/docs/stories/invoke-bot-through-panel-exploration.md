# Invoke Bot Through Panel - Increment Exploration

**Navigation:** [📋 Story Map](story-map.drawio)

**File Name**: `invoke-bot-through-panel-exploration.md`
**Location**: `agile_bot/bots/base_bot/docs/stories/invoke-bot-through-panel-exploration.md`

## Increment Purpose

User invokes bot workflows through visual panel so that behavior actions can be navigated, monitored, and executed within the IDE without switching to terminal.

---

## Stories (20 total)

### ⚙️ Manage Bot Information

#### 📝 Open Panel
- **When** User activates panel command, **then** System displays bot name
- **And** System displays workspace path
- **And** System displays bot path
- **And** System displays available botss
- **And** System displays behavior action section
- **And** System displays scope section
- **And** System displays instructions section

#### 📝 Refresh Panel
- **When** User clicks refresh button, **then** System displays bot name
- **And** System displays updated workspace path
- **And** System displays updated bot path
- **And** System displays updated available botss
- **And** System displays updated behavior action section
- **And** System displays updated scope section
- **And** System displays updated instructions section

#### 📝 Change Workspace Path
- **When** User changes workspace path, **then** System displays updated workspace path
- **And** System displays behavior action state of new workspace

#### 📝 Switch Bot
- **When** User switches bot, **then** System displays updated bot name
- **And** System displays behavior action section for new bot
- **And** System displays behavior action stateof workspace for new bot

#### 📝 Toggle Panel Section
- **When** User clicks section header, **then** System expands or collapses section

---

### ⚙️ Navigate Behavior Action Status

#### 📝 Display Hierarchy
- **When** User views panel, **then** System displays behavior list with actions
- **When** Action is current, **then** System displays current action in-progress indicator
- **When** Action is completed, **then** System displays completed indicator
- **When** Action is pending, **then** System displays pending indicator
- **When** User clicks collapsed behavior, **then** System expands behavior showing actions
- **When** User clicks expanded behavior, **then** System collapses behavior hiding actions
- **When** User clicks collapsed action, **then** System expands action showing operations
- **When** User clicks expanded action, **then** System collapses action hiding operations

#### 📝 Navigate Behavior Action
- **When** User clicks back button, **then** System  sets previous action as current
- **And** System displays previous action in-progress indicator
- **And** System reruns previous action details
- **When** User clicks next button, **then** System sets next action as current
- **And** System displays next action in-progress indicator
- **And** System reruns next action details
- **When** User clicks current button, **then** System reruns current action details
- **When** User is on the last operation of an action, **then** System moves to the next action and selects its first operation
- **When** User is on the last action of a behavior, **then** System moves to the next behavior and selects its first action and first operation
- **When** User is on the last behavior of a bot, **then** System disables next behavior navigation

#### 📝 Execute Behavior Action
- **When** User clicks behavior, **then** System displays that behavior as current
- **And** System expands behavior
- **And** System expands first action to display operations
- **And** System sets first action as current
- **And** System sets first operation as current
- **And** System executes first operation of first action of that behavior
- **When** User clicks action, **then** System displays that action as current
- **And** System expands action to display operations
- **And** System sets first operation as current
- **And** System executes first operation of that action

---

### ⚙️ Filter And Navigate Scope

#### 📝 Filter Story Scope
- **When** User types story name in filter, **then** System refreshes story hierarchy based on new story scope
- **When** Filter matches epic, **then** System displays epic with all sub-epics and stories collapsed beneath it
- **When** Filter matches sub-epic, **then** System displays sub-epic with all stories collapsed beneath it
- **When** Filter matches story, **then** System displays that story with its acceptance criteria
- **When** User clicks story with acceptance criteria, **then** System expands story showing acceptance criteria list
- **When** Filter matches multiple items, **then** System displays all matches in hierarchical format preserving parent-child relationships
- **When** User clicks clear filter button, **then** System displays all stories

#### 📝 Display Story Scope Hierarchy
- **When** User views story scope, **then** System displays epic list collapsed
- **When** User clicks collapsed epic expand icon, **and** epic has sub-epics, **then** System expands epic showing sub-epics collapsed beneath it
- **When** User clicks epic folder link, **and** matching epic folder exists, **then** System opens epic folder in IDE explorer
- **When** User clicks collapsed sub-epic expand icon, **and** matching sub-epic has stories, **then** System expands sub-epic showing stories collapsed beneath it
- **When** Sub-epic has test file, **then** System displays test link next to sub-epic name
- **When** User clicks sub-epic test link, **then** System opens test file in editor
- **When** User clicks sub-epic folder link, **then** System opens sub-epic folder in IDE explorer
- **When** User clicks collapsed story expand icon, **and** matching sub-epic has stories, **then** System expands story showing scenarios collapsed beneath it
- **When** User clicks scenario link, **and** matching scenario has  file, **then** System opens story markdown file in editor
- **When** Story has test file, **then** System displays test link next to story name
- **When** User clicks story test link, **then** System opens test file at test class
- **When** User clicks collapsed story expand icon, **then** System expands story showing scenarios
- **When** User clicks scenario link, **then** System opens test file at scenario test method

#### 📝 Filter File Scope
- **When** User types file pattern in filter, **then** System displays filtered file list
- **And** System displays file list with monospace paths

#### 📝 Open Story Files
- **When** User clicks graph link, **then** System opens story-graph.json in editor
- **When** User clicks map link, **then** System opens story-map.drawio in diagram viewer
- **When** System cannot open file, **then** System displays error message

---

### ⚙️ Display Instructions

#### 📝 Display Base Instructions
- **When** User views panel, **then** System displays base instructions section
- **And** System displays behavior name
- **And** System displays action name

#### 📝 Display Clarify Instructions
- **When** Current action is clarify, **then** System displays key questions with editable answer textareas
- **And** System displays evidence list
- **When** User edits answer textarea, **then** System updates answer
- **When** saved key questions and answers exists, **then** System displays saved key questions and answers

#### 📝 Display Strategy Instructions
- **When** Current action is strategy, **then** System displays decision criteria with radio button options
- **And** System displays assumptions textarea
- **When** Saved strategy exists, **then** System displays selected option for each decision criterion
- **When** User edits assumptions textarea, **then** System updates assumptions

#### 📝 Display Build Instructions
- **When** Current action is build, **then** System displays knowledge graph section with template path link
- **And** System displays knowledge graph output file link
- **And** System displays knowledge graph directory path
- **And** System displays rules list with clickable rule file links

#### 📝 Display Validate Instructions
- **When** Current action is validate, **then** System displays rules list
- **When** User clicks rule file link, **then** System opens rule file in editor

#### 📝 Display Render Instructions
- **When** Current action is render, **then** System displays config file paths as clickable links
- **And** System displays template file paths as clickable links
- **And** System displays output file paths as clickable links
- **When** User clicks on any of these links, **then** System opens the corresponding file in the editor

#### 📝 Display Instructions In Raw Format
- **When** User clicks action instruction in Behavior Action Hierarchy, **then** System displays entire instructions exactly as it should be sent to the AI chat

#### 📝 Submit Instructions To Chat
- **When** user has clicked on a Behavior Action's Instructions, **and** User clicks submit button, **then** System sends instructions to AI chat

---

## Source Material

- **Codebase**: `agile_bot/bots/base_bot/src/display_panel/extension/` - Reviewed actual panel implementation to ensure AC reflect real system behavior
