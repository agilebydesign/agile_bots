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
