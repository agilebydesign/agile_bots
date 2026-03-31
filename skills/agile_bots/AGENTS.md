---
name: agile_bots
description: Agile Bot CLI — why story_bot and crc_bot exist, what each behavior and action is for, plus workspace/bot/scope/story_graph commands. Use when shaping story maps, prioritizing, exploring AC, scenarios, tests, code, or CRC modeling from the terminal or an agent.
license: MIT
metadata:
  author: agilebydesign
  version: "1.0.1"
---

# Agile Bots CLI

## 1. Outcome (what this skill is for)

Using this skill, the assistant works **through agile_bots** supporting you with a **concrete workflow** for structuring, sculpting, and specifying solutions using **stories** and **CRC (Class–Responsibility–Collaborator)** models. The two bots:

**`story_bot`** — Takes context and helps you build **story maps**, **delivery increments**, **acceptance criteria** and **scenarios**, **linked tests**, and **code** that stays tied to **`story-graph.json`** — then **render** in DrawIO or markdown and apply **rules** that **validate** artifacts against practices, plus scanners that further evaluate quality as you go.

**`crc_bot`** — Takes **story language** from the same graph and helps you build a **CRC model**: **domain** extraction (objects, responsibilities, collaborators), **design** refinement (structure, dependencies, patterns), and **walkthrough** traces (scenarios through the model)—kept in **`story-graph.json`** and CRC artifacts — then **render** CRC docs/diagrams and apply **rules** / **validate** so the object model stays consistent with stories and your practices as you go.

**What the skill itself does:** Tells the **assistant** which **behavior/action** to use, and how to inoke the CLI to generate instructions for the AI as well as perform various backend automation eg rendering

---

## 2. This skill → agile_bots → CLI

- **This skill** = **`SKILL.md`** + **`content/`** (loaded by Cursor etc. as agent instructions).
- **agile_bots** = the **repository and bot runtime** (`bots/`, `src/`, configs).
- You **invoke** agile_bots by running the **CLI** (e.g. **`story_cli.ps1`**, repo **README**, then **`help`**). The assistant (or you) sends **commands**—**`path`**, **`bot`**, **`scope`**, **`shape.build`**, **`story_graph…`**, **`current`**, **`submit`**, …—that call into **`CLISession`**, **`Bot`**, and the configured behaviors. There is no second “skill runtime”; the CLI is the integration point.

### WORKING_AREA — agents (critical)

**Never** set the **`WORKING_AREA`** environment variable when invoking the CLI unless the user **explicitly** asks you to.

- **`cli_main.py`** bootstraps **`WORKING_AREA`** from **`bots/<active_bot>/bot_config.json`** (`mcp.env.WORKING_AREA` or top-level `WORKING_AREA`) when the variable is **unset**. That chooses which project’s **`docs/story/story-graph.json`** is loaded and saved.
- Setting **`WORKING_AREA`** in the shell **overrides** that config and can write the graph to the **wrong** repo.
- **Do:** For piped one-liners, set **`PYTHONPATH`** (and **`BOT_DIRECTORY`** if your shell does not already match the repo’s defaults). **Do not** set **`WORKING_AREA`** unless the user requested a specific override.
- **Do:** In an **interactive** CLI session, use **`path <dir>`** / **`workspace <dir>`** when the user needs to point at a different project than **`bot_config.json`** specifies.
- **Only** set **`WORKING_AREA`** when the user asked for that override, or there is no workspace in config and they told you exactly which project root to use.

The CLI **code** lives in **agile_bots**; the **story graph** on disk is under whatever **`WORKING_AREA`** resolves to—defaulting from **`bot_config.json`**, not from “whichever repo the agent guessed.”

### Story graph in another project — point the CLI first (mandatory for agents)

You often edit **`story-graph.json`** in a **different repo** than agile_bots (e.g. **`abd-answers`**). The assistant **must** aim the CLI at that project **before** running **`story_graph…`** or assuming which epic/stories exist. **Do not** hand-edit JSON for structural changes as a shortcut when the CLI is available.

1. **Interactive CLI session:** Run **`path <absolute-project-root>`** or **`workspace <absolute-project-root>`** first (directory must exist). That reloads **`docs/story/story-graph.json`** and **`scope.json`** from that tree. Then use **`story_graph…`** per **`cli-reference.md`**.
2. **Piped one-liners / automation:** Use the correct **`BOT_DIRECTORY`** (e.g. **`bots/story_bot`**). Leave **`WORKING_AREA` unset** in the shell so **`cli_main.py`** applies **`mcp.env.WORKING_AREA`** from **`bots/story_bot/bot_config.json`** (often already set to e.g. **`C:\dev\abd-answers`**). If commands still resolve the wrong graph, **fix bot/path/env**—not the JSON file on disk by hand.
3. **If** **`path`** / config / bot selection is wrong, symptoms include “epic not found,” empty scope, or stories from the **agile_bots** graph. **Remedy:** correct **`path`** / **`bot`** / **`WORKING_AREA`** policy above; then retry **`story_graph…`**.
4. **Only** edit **`story-graph.json`** directly when the CLI is unavailable **or** for tiny non-structural fixes the user requested—and **reload** (**`reload_story_graph`**) after unavoidable manual edits per project rules.

---

## 3. What agile_bots provides (capabilities / surface)

**Bots**

| Bot | Role |
|-----|------|
| **`story_bot`** | Phased story workflow: **shape → prioritization → exploration → scenarios → tests → code**. |
| **`crc_bot`** | **Domain → design → walkthrough** CRC modeling from story content. |

**Per behavior:** Registered **actions** typically include **`clarify`**, **`strategy`**, **`build`**, **`validate`**, **`render`**, **`rules`** (exact set per behavior—use **`help`** on the active bot).

**Cross-cutting**

- **`scope`** — Narrows which epics/stories/files/increments see instructions and validators; persists **`scope.json`**.
- **`story_graph…`** — **StoryMap API** from the CLI (create/move nodes, save, etc.) instead of hand-editing JSON. **Task → command** table (move, rename, add, `WORKING_AREA`, piped example): **`content/cli-reference.md`** → **Structural edits — task → command**.
- **`current`** / **`submit`** — Load **instructions** for the active **behavior** or **behavior.action**; **`submit`** hands them to chat when you want that step executed in context.
- **Rules & guardrails** — Behavior rules, scanners, renders: tied to **`story-graph.json`** and workspace paths.

**Default action path (story + CRC):** Prefer **`build` → `validate` → `render`** (and **`rules`** when useful). **`clarify`** only for **`shape`** when the workspace still needs clarification; **skip `strategy`** unless someone explicitly asks. Detail: **`content/00-purpose-and-workflows.md`**.

---

## 4. How to use it (assistant + human)

The assistant follows this **`SKILL.md`** and reads **`content/00-purpose-and-workflows.md`** (intent, behaviors, default path) and **`content/cli-reference.md`** (exact commands). In the repo, drive the CLI as above.

**`AGENTS.md`:** Run **`python scripts/build.py`** in this folder to concatenate **`SKILL.md`** + sorted **`content/*.md`**—optional single file for tooling/install.

### When this skill applies

- Shaping, prioritizing, exploring AC, scenarios, tests, or code under **`story_bot`**.
- Domain/design/walkthrough under **`crc_bot`**.
- Workspace/bot/scope/story_graph/submit/save/JSON output operations.

### Quick start (mental model)

1. **Workspace** — **`path`** / **`workspace`** → where **`docs/story/`**, **`scope.json`**, repo root live.
2. **Bot** — **`bot story_bot`** or **`bot crc_bot`**.
3. **Behavior** — e.g. **`shape`** sets active behavior; **`current`** / **`submit`** can target **behavior-only** instructions. Default: **`shape.build`** (or that behavior’s **`build`**) unless **`shape`** clarification is still needed—see **`00-purpose-and-workflows.md`**.
4. **Behavior.action** — e.g. **`shape.build`** loads instructions; **`submit`** sends to chat.
5. **Scope** — **`scope`** / **`scope <filter>`**.
6. **Story graph** — **`story_graph…`** — see **`cli-reference.md`**; for **moves/reorders**, use the **Structural edits** table (do not edit JSON by hand when the CLI is available).

Full command lists: **`content/cli-reference.md`** or generated **`AGENTS.md`**.


---

# What the bots are for

The Agile Bot CLI is a **structured workflow engine** for two related problems:

1. **Story bot (`story_bot`)** — Move from vague product intent to a **durable story map** and then **down into** delivery planning, specification, tests, and code — with `story-graph.json` as the spine and rules/guardrails so the assistant does not freestyle the structure.
2. **CRC bot (`crc_bot`)** — Turn domain language already captured in stories into a **CRC (Class–Responsibility–Collaborator) model**, refine it with **object design**, and **stress-test** it by tracing responsibilities through scenarios — feeding back into `story-graph.json` and CRC artifacts.

Pick the **behavior** (phase of work), **action** (step), optional **scope** (slice of the map or repo), then **submit** when you want that step handed to chat in context—aligned with what your team agreed, not a one-off freestyle.

---

## Story bot: what we do with stories

End-to-end, **story work** is: **shape the map → plan increments → explore requirements in detail → specify scenarios → write tests → write production code**, with build, validation and renders at each stage. Each behavior owns one band of that funnel. **`scope`** narrows which epics/stories/files/increments the instructions and validators see; **`story_graph...`** commands mutate the loaded map through the StoryMap API instead of hand-editing JSON.

### Behaviors (story_bot)

**`shape`** — Build the **story map**: epics, sub-epics, stories, and optional notes that hold detail before you split nodes. Outcomes include `story-graph.json`, outline diagrams, markdown exports. This is where you capture *who needs what* and the backbone structure.

**`prioritization`** — After the map exists, **organize stories into delivery increments** (value, dependency, risk). You get increment-aware views and validation; renders include increment diagrams.

**`exploration`** — **Deepen stories** with **acceptance criteria** and initial scenarios: *what “done” means* in business language before you write full BDD text.

**`scenarios`** (folder name; config may refer to `specification_scenarios`) — Write **detailed, testable scenarios** (Given/When/Then style, domain language, tied to domain concepts). This is specification-level behavior, not the high-level exploration pass.

**`tests`** — Produce **executable test files** from those scenarios and **link** them to the graph (`test_file` / `test_class` / `test_method` fields). Validation checks tests against rules and mapping.

**`code`** — **Implement production source** that matches the stories and domain language, then validate code against scanners and graph linkage. The checked-in workflow for this behavior emphasizes **build** (implementation) and **validate** (quality and mapping).

### Default action flow

The bot **registers** **`clarify`**, **`strategy`**, **`build`**, **`validate`**, **`render`**, and often **`rules`** on many behaviors—the default path is **not** “run every step in order.” Use the ladder below unless someone clearly wants something else.

**`clarify`** — **Only for `shape`**, and **only when** clarification for **this workspace** is not already satisfied (e.g. check `clarification.json` / existing answers for the current behavior: if the important questions are already answered, **skip clarify** and go to **`build`**). **Do not** default to **`clarify`** for **`prioritization`**, **`exploration`**, **`scenarios`**, **`tests`**, **`code`**, or **`crc_bot`** behaviors.

**`strategy`** — **Do not use in the default skill path for any behavior.** Ignore it unless the user explicitly asks to work through strategy (see override note below).

**`build`** — The **usual first real work step** for each behavior (after optional shape-only clarify): edit or extend `story-graph.json` (or code/tests) according to the behavior’s goal — shape structure, assign increments, add AC, add scenarios, write tests, write code.

**`validate`** — Run **behavior rules and scanners** against the current scope (story graph, files, code). Surfaces violations and guidance.

**`render`** — **Generate artifacts**: DrawIO diagrams, markdown, text exports, CRC docs — whatever that behavior’s render configs define.

**`rules`** — Where configured, **pull a rules digest** for the behavior into the instruction stream so the assistant sees project-specific DO/DON’T and priorities.

**Explicit override:** The user can always say they want **`shape.strategy`**, **`tests.clarify`**, or any other **`behavior.action`**—the CLI allows it. Treat that as **intentional and uncommon**: confirm they mean to deviate from the default path, then follow their instruction. Do **not** default to clarify/strategy outside the rules above.

The **`code`** and **`test`** behavior’s config only has on **build** and **validate**; other actions may still exist via shared base actions depending on bot setup—use **`help`** on the active bot to see what is registered.

---

## CRC bot: what we do with CRC models

**CRC** here means **Class–Responsibility–Collaborator** cards: objects, what they do, who they work with. The CRC bot exists to connect **story language** to a **maintainable object model** that can be reviewed, refined, and proven against scenarios.

### Behaviors (crc_bot)

**`domain`** — **Extract and consolidate CRC concepts** from `story-graph.json` (and context): responsibilities, collaborators, modules aligned with source layout. Outputs include CRC outline/description and diagrams. **Goal:** a coherent domain model tied to stories.

**`design`** — **Refine CRC cards** with OO design: encapsulation, patterns, dependencies, SOLID-style checks, while preserving module assignments from domain. **Goal:** an implementation-ready object design, still reflected in `story-graph.json`.

**`walkthrough`** — **Trace the model**: object flows through scenarios, add missing responsibilities or collaborators when gaps appear, record realizations. **Goal:** confidence that the CRC model actually supports the stories.

### Actions (CRC bot)

For CRC, follow the same **default** as story bot: **skip `clarify` and `strategy`** unless the user explicitly asks. Use **`build` → `validate` → `render`** (and **`rules`** when useful). **Build** is where CRC structure is written or updated; **validate** checks CRC rules; **render** emits CRC documents.

---

## How this ties to the CLI reference

**`cli-reference.md`** describes **commands** (`path`, `scope`, `shape.build`, `story_graph...`, `submit`, …). This document describes **intent**: which **`behavior.action`** to use when shaping stories, prioritizing, exploring, specifying, testing, coding, or modeling CRC. Together: “what are we doing?” and “what do we type?”.


---

# Agile Bot CLI — Operations reference

Commands are interpreted by `CLISession` (`src/cli/cli_session.py`) and `Bot` (`src/bot/bot.py`).

**Start:** Run the CLI and type **`help`**. You get TTY help from `src/help/help.py`: navigation, this bot’s behaviors and actions, operations, scope rules, and examples.

**Running:** From the `agile_bots` repo, with `PYTHONPATH` including `src` and `BOT_DIRECTORY` as needed (`src/cli/cli_main.py`, repo README). If **`WORKING_AREA`** is **unset**, **`cli_main.py`** reads it from **`bots/<bot>/bot_config.json`** (`mcp.env.WORKING_AREA` or `WORKING_AREA`). **Agents:** do **not** set **`WORKING_AREA`** in the shell unless the user explicitly asked—overriding it sends graph edits to the wrong project. Tests in `test/` use the same strings against `CLISession`.

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

**Multi-repo / external project:** The graph file lives under **`WORKING_AREA/docs/story/`**.

- **Interactive CLI:** use **`path C:\path\to\project`** or **`workspace C:\path\to\project`** before **`story_graph...`**.
- **Piped commands:** leave **`WORKING_AREA`** **unset** so **`cli_main.py`** uses **`bot_config.json`** (see **WORKING_AREA** note under **Running** above). **Do not** set **`$env:WORKING_AREA`** unless the user explicitly asked for that override.

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

**Example (piped one-liner, Windows):** after **`cd`** to **`agile_bots`** and setting **`PYTHONPATH`** and **`BOT_DIRECTORY`** (if needed). **Do not** set **`WORKING_AREA`** unless the user asked—let **`bot_config.json`** pick the project.

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
