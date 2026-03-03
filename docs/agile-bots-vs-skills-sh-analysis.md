# Agile Bots vs skills.sh: Comparative Analysis

**Scope:** Full feature comparison. Agile Bots (`src/`) is a workflow orchestration system with story graph, prompt injection, validation, and UI. skills.sh is a Markdown-based skill format for AI agents.

---

## Part 1: Agile Bots — Full Feature Inventory

### 1. Story Graph (JSON + Python Data Layer)

| Component | Location | Role |
|-----------|----------|------|
| **Artifact** | `docs/story/story-graph.json` (workspace) | Epics → sub_epics → story_groups → stories → scenarios → steps; increments; domain_concepts |
| **StoryGraph** | `src/story_graph/story_graph.py` | Loads JSON, exposes `content`, `path`, `has_epics`, `has_increments` |
| **StoryMap** | `src/story_graph/nodes.py` | Domain model: Epic, SubEpic, StoryGroup, Story, Scenario, Step; `find_node()`, `save()`, `node_to_dict()` |
| **StoryGraphPaths** | `src/story_graph/story_graph_paths.py` | Paths for story-graph.json, docs_root, behavior_path() |
| **JSONStoryGraph** | `src/story_graph/json_story_graph.py` | Serializes to JSON with `include_level`, optional trace |
| **Scope** | `src/scope/scope.py`, `json_scope.py` | Filters by story, increment, files; `StoryGraphFilter`; `graphLinks` for DrawIO |

**Diagram sync (DrawIO):**

- `graphLinks` built in `json_scope.py` via `_add_drawio_links_to_graph()` from `bots/.../content/render/*.json`
- Panel: `workspace_section_view.js` — Render, Save layout, Clear layout, Generate report, Update graph
- Bot: `render_diagram_for_scope()`, `save_layout_to_drawio()`, `update_graph_from_diagram()` in `bot.py`

**skills.sh has none of this** — no story graph, no DrawIO sync, no domain model.

---

### 2. Prompt Injection Hierarchy

Instructions are assembled from multiple levels and injected into the final prompt.

| Level | Source | Content | Files |
|-------|--------|---------|-------|
| **Action (base)** | `base_actions/<action>/action_config.json` | `instructions` — common to ALL behaviors for that action | `base_actions/clarify/`, `strategy/`, `build/`, `validate/`, `render/` |
| **Behavior** | `behaviors/<name>/behavior.json` | `instructions`, `description`, `goal`; `actions_workflow[].instructions` | `bots/story_bot/behaviors/shape/behavior.json` |
| **Action (behavior)** | `behaviors/<name>/actions/<action>/` or `actions_workflow` | `instructions` — overrides/extends base for this behavior | In `behavior.json` under `actions_workflow` |
| **Context** | `Instructions.context_sources_text` | Hardcoded paths: story-graph.json, strategy.json, clarification.json, workspace/test, workspace/src, context/ | `src/instructions/instructions.py` |
| **Guardrails** | `guardrails/required_context/`, `guardrails/strategy/` | Key questions, evidence, decision criteria, assumptions | Injected via `_load_behavior_guardrails()`, `_load_all_saved_guardrails()` |
| **Scope** | `Scope.results` | Filtered story graph or file list; `graphLinks` for DrawIO | `scope/json_scope.py`, `_build_display_content()` |
| **Reminders** | `instructions/reminders.py` | "Next behavior: X" when not final action | `inject_reminder_to_instructions()` |

**Injection flow** (`Action.get_instructions()` in `src/actions/action.py`):

1. `instructions = self.instructions` — base from `base_actions/<action>/action_config.json` + context_sources_text + clarification + strategy + context files
2. Extend with `action_config.instructions` from behavior's actions_workflow
3. `_load_behavior_guardrails()` → required_context, strategy criteria, saved clarification/strategy
4. `_add_behavior_action_metadata()` → `behavior_instructions`, `action_instructions` (from behavior.json and action_config)
5. `_build_display_content()` → MarkdownInstructions → `display_content` (includes scope, graphLinks, etc.)

**skills.sh:** Single SKILL.md + AGENTS.md. No hierarchy, no context injection, no guardrails.

---

### 3. Activity Logging

| Component | Location | Status |
|-----------|----------|--------|
| **ActivityTracker** | `src/actions/activity_tracker.py` | **DISABLED** — `TINYDB_AVAILABLE = False` (was causing file corruption) |
| **Data** | `ActionState` (bot_name, behavior, action, outputs, duration) | Would write to `activity_log.json` |
| **Calls** | `Action.track_activity_on_start()`, `track_activity_on_completion()` | `_track_rules_snapshot()` logs rules used |

**skills.sh:** No activity logging.

---

### 4. Rules and Validation

| Component | Location | Role |
|-----------|----------|------|
| **Rules** | `behaviors/<name>/rules/*.json` | One JSON per rule: priority, description, do/dont, scanner (optional) |
| **RuleLoader** | `src/rules/rule_loader.py` | `load_bot_rules()` + `load_behavior_rules()` — **bot rules dir exists but is EMPTY** (0 files) |
| **Rule** | `src/rules/rule.py` | Loads scanner class via `ScannerRegistry`; `scan()` → violations |
| **ValidationContext** | `src/rules/rules.py` | `ValidationContext`, `ScanConfig`, file-by-file + cross-file scans |

**Inheritance:** Code supports bot + behavior rules. In practice: **only behavior rules exist**; `bots/story_bot/rules/` has 0 files.

---

### 5. Guardrails

| Component | Location | Role |
|-----------|----------|------|
| **RequiredContext** | `guardrails/required_context/` | key_questions.json, evidence.json |
| **Strategy** | `guardrails/strategy/` | decision_criteria/*.json, typical_assumptions.json |
| **Storage** | `docs/story/clarification.json`, `strategy.json` | Saved answers, decisions, assumptions |
| **Panel** | `instructions_view.js` | Editable textareas, radio buttons for criteria |

---

### 6. Scope

| Component | Location | Role |
|-----------|----------|------|
| **ScopeType** | `src/scope/scope.py` | ALL, STORY, INCREMENT, FILES, SHOW_ALL |
| **Scope** | `scope.json` in workspace | Persisted; `apply_to_bot()` |
| **Filtering** | `StoryGraphFilter`, `FileFilter` | By search_terms, increments, globs |
| **Enrichment** | `json_scope.py` | `graphLinks`, `renderOutputLinks`, `_enrich_with_links()` |

---

### 7. Panel (VS Code)

| Component | Location | Role |
|-----------|----------|------|
| **Panel** | `src/panel/` | panel_view.js, instructions_view.js, workspace_section_view.js, diagram_section_view.js |
| **CLI** | Spawns `cli_main.py` | JSON mode, `<<<END_OF_RESPONSE>>>` marker |
| **Commands** | renderDiagram, saveDiagramLayout, generateDiagramReport, updateFromDiagram | Diagram sync from panel |

---

### 8. CLI

| Component | Location | Role |
|-----------|----------|------|
| **CLI** | `src/cli/cli_main.py`, `cli_session.py` | status, save, submit, scope, path, workspace, behavior.action |
| **Adapters** | `AdapterFactory` | JSON/TTY/Markdown per domain type |
| **Navigation** | `src/navigation/` | behavior.action routing, story_graph.* domain commands |

---

### 9. Other

- **Traceability:** `trace_generator.py`, `include_level` for scenario trace
- **Context package:** `rule_file_generator` → `.cursor/rules/` from behaviors
- **Bot paths:** `bot_path.py`, `story_graph_paths.py` — workspace, bot dir, base_actions, story_graph_path, behavior_path()

---

## Part 2: skills.sh / Vercel (Markdown) — Structure

| Layer | Location | Purpose |
|-------|----------|---------|
| **SKILL.md** | Root | Entry point, when to apply, quick reference |
| **AGENTS.md** | Root | Compiled full guide (built from rules + content) |
| **rules/*.md** | Per rule | DO/DO NOT with examples |
| **content/** | Intro, definitions, etc. | Supporting content |

- **Format:** YAML frontmatter + short DO/DO NOT + examples
- **No inheritance** — Flat; categories by filename prefix
- **No scanners** — Pure AI guidance
- **No story graph, no DrawIO, no prompt hierarchy, no activity logging, no panel**

---

## Part 3: Side-by-Side (Expanded)

| Dimension | Agile Bots | skills.sh |
|-----------|------------|-----------|
| **Story graph** | JSON + StoryMap + scope filtering + DrawIO sync | None |
| **Prompt injection** | 3-level hierarchy (base action, behavior, behavior-specific action) + context + guardrails + scope | Single SKILL.md + AGENTS.md |
| **Activity logging** | Present (disabled) — ActionState, rules snapshot | None |
| **Rules** | JSON + scanners → violations | Markdown, guidance only |
| **Guardrails** | Structured (Q&A, options, assumptions) | Not designed |
| **Rule inheritance** | Code supports bot+behavior; **bot rules dir empty** | None |
| **Scope** | Story/increment/file filtering, persistence | None |
| **Panel/CLI** | VS Code panel, CLI | None |
| **Portability** | Tied to story_bot | Installable skill |

---

## Part 4: Should You Convert?

### Short answer: No — different systems. Use a hybrid for rules only.

### 1. Guardrails stay JSON

Structured Q&A, options, assumptions. Keep as-is.

### 2. Rules: hybrid (optional)

- Markdown for guidance text; minimal JSON for scanner config
- Build step: Markdown → AGENTS.md for skills.sh export; JSON for story_bot

### 3. Inheritance

**Reality:** Bot rules dir is empty. Only behavior rules exist. Code supports inheritance but it's unused.

### 4. Portability

- **Internal:** Keep full story_bot (story graph, prompt hierarchy, scope, panel, CLI)
- **External:** Export Markdown skills (e.g. solution-shaping) for use in other agents
- **No conversion** of story graph, prompt injection, or activity logging — those are not in skills.sh format

---

## Part 5: Recommendation

1. **Keep the full system** — Story graph, prompt hierarchy, scope, panel, CLI are core.
2. **Keep guardrails as JSON** — Structured.
3. **Keep scanners** — Programmatic validation.
4. **Optional:** Export selected rule content as Markdown skills for external use.
5. **Do not** try to replicate story graph, prompt injection, or activity logging in skills.sh — they are outside that model.
