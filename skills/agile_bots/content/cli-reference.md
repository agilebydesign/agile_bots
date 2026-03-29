# Agile Bot CLI — Operations reference

Commands are interpreted by `CLISession` (`src/cli/cli_session.py`) and `Bot` (`src/bot/bot.py`).

**Start:** Run the CLI and type **`help`**. You get TTY help from `src/help/help.py`: navigation, this bot’s behaviors and actions, operations, scope rules, and examples.

**Running:** From the `agile_bots` repo, with `PYTHONPATH` including `src` and `BOT_DIRECTORY` / `WORKING_AREA` set (`src/cli/cli_main.py`, repo README). Tests in `test/` use the same strings against `CLISession`.

**Line format:** One line per command unless noted; space-separated arguments; quote strings where needed.

Append **`--format json`** anywhere on the line for machine-readable JSON (scripts, tests, agents) instead of TTY text.

---

## Workspace and bot

**`path`** and **`workspace`** are the same command. With no argument, they show the active workspace folder. The response includes status, path, and a short message.

**`path <directory>`** or **`workspace <directory>`** switches the bot to another project tree. The directory must already exist. On success you get the new path and scope is reloaded from that workspace. Instructions, `story-graph.json`, and `scope.json` are all relative to the workspace you set.

**`bot`** with no argument shows the current bot name, the list of registered bots, and a usage hint.

**`bot <name>`** switches the active bot (for example `story_bot` or `crc_bot`). You get success or an error if the name is not registered.

---

## Help, status, current

**`help`** prints the built-in reference for the active bot: patterns, behaviors and actions, operations like instructions and submit, scope rules, examples.

**`status`** prints a snapshot of bot state, behaviors, and current action (TTY or JSON with `--format json`).

**`current`** refreshes instructions for the **current selection**: same combined payload as **`submit`**—if only a **behavior** is selected (e.g. after `shape`), you still get full behavior-level instructions; if an **action** is selected, you get that step (with combine rules per execution mode).

---

## Default path vs full CLI (clarify / strategy)

The CLI exposes every registered **`behavior.action`**. **This skill’s default workflow** is:

- **`clarify`** — Use **only** under **`shape`**, and **only if** clarification for the workspace is **not** already done (e.g. inspect `clarification.json` / existing answers for the behavior; if satisfied, skip to **`build`**). **Do not** steer into **`clarify`** for other behaviors by default.
- **`strategy`** — **Do not use** in the default skill path for **any** behavior. The user can still type **`shape.strategy`** and submit if they want; that is an explicit, uncommon override.

**Override:** If the user clearly asks for a specific **`behavior.action`** (including **`strategy`** or **`tests.clarify`**), follow that—they are choosing the full ladder on purpose.

---

## Behaviors, actions, instructions, execution modes, save, and submit

This is one workflow: **where you are** in the bot (behavior and action), **what instructions** you load, **how** linked steps combine, **what you persist** from guardrail actions when you use them, and **when you push** instructions to chat.

**Navigation.** Typing a **behavior name alone** (e.g. `shape`) switches the active behavior. **`current`** / **`submit`** then treat the selection as **behavior-level** (whole-behavior instructions) when no action is pinned. **`shape.build`** (or any **`behavior.action`**) selects behavior and action and loads **`Instructions`** for that step in the output. If you are already on a behavior, you can type **only the action name** (`build`, `validate`, …) to select that action on the current behavior.

**Loading instructions.** **`behavior.action`** (e.g. **`shape.build`**) is how you load the instruction payload for that step. You can add **`--scope-type=...`** / **`--scope-value=...`** or **`--scope={"type":"story","value":["X"]}`** on execute for explicit scope. **`shape.rules`**, **`shape.clarifications`**, **`shape.strategies`** are two-part **domain getters** — they return domain data for the behavior, not a full execute path.

**Execution modes** control how **combine_next** / **auto** / **skip** / **manual** affect whether the next action’s instructions are merged when you **do** use multi-step flows. **`behavior.set_execution <mode>`** sets the default for a behavior; **`behavior.action.set_execution <mode>`** sets it for one action; **`behavior.action.get_execution`** returns behavior, action, and execution_mode. Valid modes are shown in CLI messages (e.g. combine_with_next, auto, skip, manual).

**Save** persists guardrails when you use clarify/strategy (or panel): **`save --answers '{"Q":"A"}'`** merges into **`clarification.json`**; **`save --decisions`**, **`save --assumptions`**, **`save --evidence_provided`** update strategy / clarification stores under the workspace.

**Submit** is the handoff to chat from the CLI. **`submit`** sends the **current** behavior.action instructions (e.g. to Cursor). **`submit <behavior> <action>`** targets a specific pair. **`submitrules:<behavior>`** or **`submitrules <behavior>`** pushes the rules digest for that behavior. You can skip **`submit`** when the same chat session already has that content.

---

## Scope

**Scope** controls what appears in **instructions** and **validation** so you can focus work without editing JSON by hand.

**`scope`** alone prints current scope settings.

**`scope clear`** or **`scope all`** clears filters so everything is in play.

**`scope showall`** sets scope mode to show the full graph where that applies.

**`scope include_level=<level>`** sets how deep scope renders: levels include stories, domain_concepts, acceptance, scenarios, examples, tests, code. Invalid levels error.

**`scope story "Story Name"`** or comma-separated names focuses on those stories. Alternate spacing like **`scope story Story1, Story2`** works. You can use **dot-separated segments inside a value** (e.g. `Epic.SubEpic.Story`) to match a path in the tree; see `StoryGraphFilter` in `src/scope/scope.py`.

**`scope files`** with paths or globs focuses validation and context on files.

**`scope increment "Increment Name"`** filters by increment / prioritization.

**`scope epic "Epic Name"`** filters by epic label through the same story-type pipeline.

Delimited forms (`story=...`, `files=...`) and spaced lists are parsed in **`Bot.scope()`** in `src/bot/bot.py`.

**`scope` vs `story_graph`:** **`scope`** sets filters stored in **`scope.json`** and parsed by **`Bot.scope()`** — what gets merged into instructions and validation. Commands starting with **`story_graph`** go through **`DomainNavigator`** on **`bot.story_graph`** to navigate or change structure (create, rename, move, delete); use **quoted segments** for names with spaces, e.g. `story_graph."Invoke Bot".create_sub_epic name:"Sub"`. Details are in the story graph section below. That path persists via StoryMap to **`story-graph.json`**.

The default REPL is **`story_bot`** under `bots/story_bot`.

---

## Story graph API (`story_graph...`)

Commands start with **`story_graph`** and are handled by **`DomainNavigator`** (`src/navigation/domain_navigator.py`). Use **dot paths** and **named parameters** after a space. Names with spaces use **quoted segments**, e.g. `story_graph."Invoke Bot".create_sub_epic name:"Auth"`.

Examples: **`story_graph.create_epic name:"Epic Name" at_position:1`**; **`story_graph."Epic".create_sub_epic name:"Sub"`**; **`story_graph."Epic"."Sub".create_story name:"Story"`**; **`rename`**, **`move_to`**, **`delete`** on path segments; persist with StoryMap save when the API exposes it. Method names match **`StoryMap`** and node classes in **`src/story_graph/nodes.py`**. For increments, see **`add_increment`**, **`rename_increment`**, **`reorder_increment`**, **`add_story_to_increment`**, etc.

Prefer **`story_graph...`** for structural edits so validation and saves stay consistent.

### Structural edits — task → command (read this first)

**Do not** hand-edit **`story-graph.json`** for moves, renames, or hierarchy changes when the CLI is available. The CLI runs **`StoryMap`** / **`DomainNavigator`**, persists correctly, and (for stories with **`test_class`**) can relocate tests. **`scope`** is only for *filtering* instructions—use **`story_graph...`** to *change* the tree.

**Multi-repo / external project:** From **`agile_bots`**, set the target workspace **before** graph commands:

- **`path C:\path\to\project`** (inside an interactive CLI session), or  
- **`$env:WORKING_AREA = "C:\path\to\project"`** (PowerShell) then pipe each command to **`python src/cli/cli_main.py`** (see **`bots/cli_execute.ps1`**).

| Task | Command pattern (names with spaces use quoted segments `."Name"`) |
|------|---------------------------------------------------------------------|
| Point CLI at a project | **`path <dir>`** or **`workspace <dir>`** |
| Add epic | **`story_graph.create_epic name:"Epic Name"`** (optional **`at_position:N`**) |
| Add sub-epic under epic | **`story_graph."Epic Name".create_sub_epic name:"Sub Name"`** |
| Add story under sub-epic | **`story_graph."Epic Name"."Sub Name".create_story name:"Story Name"`** |
| **Move story** to another sub-epic (e.g. first slot) | **`story_graph."Epic"."Source Sub"."Story Name".move_to target:story_graph."Epic"."Target Sub" at_position:0`** |
| **Reorder** story within same parent | **`story_graph."Epic"."Sub"."Story Name".move_to_position position:N`** |
| Rename a node | **`story_graph."…".rename name:"New Name"`** (method on the path segment being renamed) |
| Reload JSON after an unavoidable manual edit | **`reload_story_graph`** |

**Example (piped one-liner, Windows):** after **`cd`** to **`agile_bots`** and setting **`PYTHONPATH`**, **`BOT_DIRECTORY`**, **`WORKING_AREA`**:

```powershell
echo 'story_graph."Answers Content Questions"."Manage Chat Space"."Open Chat Session".move_to target:story_graph."Answers Content Questions"."Chats With Assistant" at_position:0' | python src/cli/cli_main.py
```

---

## Diagram helpers (DrawIO)

Call **bot functions** with parentheses and string args, e.g. **`render_diagram_for_scope()`**, **`save_layout_to_drawio()`**, **`update_graph_from_diagram()`**. Exact signatures live on **`Bot`** in **`bot.py`**.

---

## Generate artifacts (advanced)

**`generate context package`** emits Cursor rules / context package from bots. **`generate skills`** is legacy skill regeneration and may be deprecated in favor of maintaining the **`agile_bots`** skill content by hand.

---

## Reload and misc

**`reload_story_graph`** reloads **`story-graph.json`** after an external edit. **`help`** / **`help <topic>`** for built-in help. **`exit`** ends the session.

---

## Avoid

Prefer **`story_graph...`** and **`scope`** over pasting huge raw **`story-graph.json`** edits. Use **`save`** for guardrails; use graph commands and save for structure.

---

## Quick reference

- Set project folder: **`path <path>`** or **`workspace <path>`**
- Pick bot: **`bot story_bot`**
- Default story work: **`shape.build`** (not **`shape.clarify`** / **`shape.strategy`**) unless the workspace still needs **`shape`** clarification—see **`00-purpose-and-workflows.md`**
- Go to step: **`shape.build`** or **`build`** when that behavior is current
- Instructions as JSON: **`shape.build --format json`**
- Focus stories: **`scope story "Name1", "Name2"`** (filter only; does not edit the graph)
- **Change graph structure (move/rename/add/delete/reorder):** see **Structural edits — task → command** above—use **`story_graph...`**, not raw JSON edits
- Add epic: **`story_graph.create_epic name:"..."`**
- Send to AI: **`submit`**
- Next step: **`next`**

Behavior-specific rules still come from the active bot’s **`behaviors/<name>/`** config; this document only describes driving the CLI.
