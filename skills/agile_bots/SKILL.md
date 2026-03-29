---
name: agile_bots
description: Agile Bot CLI — why story_bot and crc_bot exist, what each behavior and action is for, plus workspace/bot/scope/story_graph commands. Use when shaping story maps, prioritizing, exploring AC, scenarios, tests, code, or CRC modeling from the terminal or an agent.
license: MIT
metadata:
  author: agilebydesign
  version: "1.0.0"
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
