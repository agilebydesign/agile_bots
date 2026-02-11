# Synchronize Graph with Rendered Content - Exploration

**Navigation:** [📋 Story Map](story-map.txt) | [📊 Story Graph](../../story/story-graph.json)

**Scope:** Invoke Bot > Perform Action > Synchronize Graph with Rendered Content

## Stories (6 total)

### 📝 Render story map

**Acceptance Criteria:**
- **WHEN** user requests outline diagram from story graph  
  **THEN** system renders epics sub-epics and stories to DrawIO file  
  **AND** each node has position and size  
  **AND** output is valid DrawIO XML
- **WHEN** layout data from previous render exists  
  **THEN** system applies saved positions to preserve user arrangement  
  **AND** new nodes get default spacing
- **WHEN** render completes  
  **THEN** system writes DrawIO file to specified path  
  **AND** summary reports epics count and sub_epic_count (and diagram_generated)
- **WHEN** story graph has E epics, S sub-epics, and N stories  
  **THEN** diagram contains exactly E epic cells, S sub-epic cells, N story cells  
  **AND** summary reports epics E and sub_epic_count S
- **WHEN** stories and sub-epics have sequential_order  
  **THEN** diagram orders sub-epics left-to-right and stories within each group by sequential_order  
  **AND** and-groups are horizontal, or-groups vertical
- **WHEN** layout data exists  
  **THEN** system applies saved x, y, width, height for epics and sub-epics  
  **AND** new nodes receive default spacing from render constants

### 📝 Render story map increments

**Acceptance Criteria:**
- **WHEN** user requests increments diagram from story graph  
  **THEN** system renders epics sub-epics stories and increment lanes  
  **AND** stories are assigned to lanes from story graph increments[].stories
- **WHEN** story graph has increments with priority  
  **THEN** system preserves priority order in diagram (lane order = increment order)  
  **AND** lane Y positions are derived from outline bottom and lane height
- **WHEN** layout data exists for increments view  
  **THEN** system applies saved positions for epics and sub-epics  
  **AND** increment lane Y positions are computed from outline bottom and lane height (saved layout for increment lanes is not currently applied on re-render)
- **WHEN** render completes  
  **THEN** system writes DrawIO file  
  **AND** summary includes increment count
- **WHEN** increment cells are rendered  
  **THEN** style and position allow extractor to detect them (strokeColor and x &lt; 0 consistent with get_increments_and_boundaries)

### 📝 Render story map with acceptance criteria

**Acceptance Criteria:**
- **WHEN** user requests exploration diagram  
  **THEN** system renders stories and acceptance criteria boxes below stories  
  **AND** AC text is formatted When/Then in boxes
- **WHEN** story has acceptance criteria  
  **THEN** system creates wider AC boxes below story  
  **AND** extracts step text from AC
- **WHEN** layout data exists  
  **THEN** system preserves positions of story and AC boxes
- **WHEN** render completes  
  **THEN** output DrawIO contains both story cells and AC cells with correct containment

### 📝 Update graph from story map

**Acceptance Criteria:**
- **WHEN** user synchronizes from DrawIO outline file  
  **THEN** system extracts epics sub-epics and stories from DrawIO  
  **AND** writes extracted JSON  
  **AND** assigns stories to sub-epics by position and containment
- **WHEN** original story graph path is provided  
  **THEN** system generates merge report comparing extracted to original  
  **AND** report lists exact matches fuzzy matches new stories and removed stories
- **WHEN** merge report exists and user runs merge  
  **THEN** system updates original with extracted structure  
  **AND** preserves acceptance criteria and steps from original for matched stories
- **WHEN** user renames or reorders nodes in DrawIO  
  **THEN** extracted graph reflects new names and order  
  **AND** merge report flags renames as fuzzy matches when names differ
- **WHEN** user deletes nodes in DrawIO  
  **THEN** extracted graph omits those nodes  
  **AND** merge report lists them as removed  
  **AND** large deletion detection flags entire missing epics or sub-epics
- **WHEN** sync runs  
  **THEN** system persists layout data to separate JSON file  
  **AND** layout includes x y width height for nodes for use on next render
- **WHEN** user moves a story in DrawIO and saves  
  **THEN** sync extracts new position and assigns sequential_order from left-to-right and vertical position  
  **AND** merge updates sequential_order for the matched story
- **WHEN** user deletes one story cell  
  **THEN** extracted graph omits that story and merge report lists it in removed_stories  
  **AND** merge output keeps original structure with only matched stories updated
- **WHEN** user deletes a sub-epic box  
  **THEN** extracted graph omits that sub-epic and its stories are reassigned by containment  
  **AND** large_deletions includes missing_sub_epics for that sub-epic
- **WHEN** user deletes an epic box  
  **THEN** extracted graph omits that epic and all its sub-epics and stories  
  **AND** merge report lists those stories as removed and large_deletions includes missing_epics

### 📝 Update graph from map increments

**Acceptance Criteria:**
- **WHEN** user synchronizes from DrawIO increments file  
  **THEN** system extracts increment boxes by style and x &lt; 0 sorted by Y  
  **AND** assigns stories to increments by story Y vs increment Y (closest within tolerance)  
  **AND** increment priority = 1-based position order; name = cell value
- **WHEN** original story graph is provided  
  **THEN** system generates merge report (story-level: exact matches, fuzzy matches, new stories, removed stories); increment membership in extracted reflects DrawIO lane positions
- **WHEN** user moves stories between increments in DrawIO  
  **THEN** extracted graph reflects new increment membership (by Y position)
- **WHEN** merge runs  
  **THEN** system preserves original acceptance criteria and steps  
  **AND** updates story fields (users, connector, sequential_order) from extracted within existing increments  
  **AND** adds extracted increments whose name is not in original; does not remove increments or replace which stories belong to which increment
- **WHEN** sync runs  
  **THEN** system writes extracted JSON with epics and increments  
  **AND** optional merge report when original provided
- **WHEN** user adds an increment lane in DrawIO  
  **THEN** extracted graph has one more increment (by Y order) and merge adds it (new name)
- **WHEN** user removes an increment lane  
  **THEN** extracted graph has fewer increments; merge does not remove increments so removed lane’s name remains in merged with original stories; stories in deleted lane reassign by Y to closest remaining lane in extracted
- **WHEN** user renames an increment  
  **THEN** extracted has new name; merge treats as new (adds it) and does not remove old name so merged graph can contain both until strategy for rename is defined (e.g. match by position or stable id)
- **WHEN** distinguishing original vs new increment  
  **THEN** system uses name only: same label ⇒ same increment (no duplicate add); different label ⇒ add as new (cannot distinguish rename from genuinely new without stable id or position-based matching)

### 📝 Update story graph from map acceptance criteria

**Acceptance Criteria:**
- **WHEN** user synchronizes from DrawIO exploration file  
  **THEN** system extracts stories and acceptance criteria boxes  
  **AND** maps AC text back to story acceptance_criteria or steps
- **WHEN** AC box text is When/Then format  
  **THEN** system extracts step description  
  **AND** associates with story
- **WHEN** merge runs  
  **THEN** system preserves original scenario steps and acceptance criteria (merge does not overwrite AC from extracted)
- **WHEN** user adds or removes AC boxes in DrawIO  
  **THEN** extracted graph reflects new or removed AC  
  **AND** merge report reflects structural changes
- **WHEN** sync runs  
  **THEN** system assigns AC cells to stories by vertical position and containment below story cells

---

## Detailed acceptance criteria (from code)

The following behaviors are derived from the synchronizer and renderer implementation. They define testable conditions for layout, order, move, and delete.

### Render story map – layout and structure

- **Layout constants (outline mode):**
  - Epics: Y = 120 (EPIC_Y); first epic X = 20; height 60px.
  - Sub-epics: directly below epic (epic_y + 60); horizontal placement, side-by-side; FEATURE_SPACING_X = 10; height 60px; SUB_EPIC_VERTICAL_SHIFT = 15.
  - Stories: below sub-epic with STORY_OFFSET_FROM_FEATURE = 90; STORY_WIDTH = 50, STORY_HEIGHT = 50; STORY_SPACING_X = 60, STORY_SPACING_Y = 55.
- **Counts:** For a story graph with E epics, S sub-epics (across all epics), and N stories, the rendered diagram contains exactly E epic cells, S sub-epic (feature) cells, and N story cells (plus optional user labels and estimate boxes). Summary reports `epics: E` and `sub_epic_count: S`.
- **Order:**
  - Sub-epics are sorted by `sequential_order` (ascending) and rendered left to right.
  - Within each sub-epic, story_groups are processed in order; within each group, stories are sorted by `sequential_order` and placed by group type: horizontal (and) = left to right; vertical (or) = top to bottom.
  - Optional stories (flag = true) share one horizontal slot and stack vertically; sequential stories get distinct horizontal positions.
- **When layout data exists:** Layout is applied for **epics** (key `EPIC|{name}`: x, y, width), **sub-epics** (key `FEATURE|{epic}|{sub_epic}`: x, y, width, height), and **users**. Story positions in outline mode are **not** taken from layout_data; they are always computed from sequential_order and group type so left-to-right order is preserved. New nodes (no key in layout) get default calculated positions and spacing.
- **Output:** Valid DrawIO XML (mxfile with diagram, mxGraphModel, root, mxCell elements with geometry); file written to the specified path; summary includes `epics`, `sub_epic_count`, `diagram_generated`.

### Render story map – layout file and re-render

- **Layout file (from sync):** When synchronizing from DrawIO, layout is persisted to `{output_path.stem}-layout.json`. Keys: `EPIC|{name}`; `SUB_EPIC|{epic}|{sub_epic}` (sync uses SUB_EPIC; renderer expects FEATURE for sub-epics – see Known gaps); `{epic}|{sub_epic}|{story}` for story x,y; user keys for epic/feature/story-level users. Values include x, y, and where applicable width, height.
- **Re-render with layout:** When rendering with layout_data loaded from that file, epic and feature positions/sizes from layout are used; new epics/features/stories get default spacing.

### Render story map with acceptance criteria (exploration mode)

- **Scope:** Only stories that have acceptance_criteria are included in the exploration diagram; epics and sub-epics without any such stories are omitted.
- **Layout:** Uses same structure as outline (story_groups, sequential_order) but with AC boxes below each story; AC boxes have minimum width 250px; When/Then formatting in HTML; steps sorted by sequential_order when present.
- **Layout data:** When layout data exists, positions for story and AC boxes are applied (keys include story and AC cell id or name-based keys).

### Update graph from story map – extract and merge

- **Extract:** Epics and sub-epics are detected from DrawIO by style (fillColor/strokeColor); stories by style (yellow story boxes); assignment to sub-epic by containment (story center inside sub-epic bounds). Stories are assigned to story_groups by containment in grey background rectangles; group type (and/or) from relative positions (same Y = and, different Y = or). `sequential_order` is assigned from position: left-to-right by X, then top-to-bottom within same X (within tolerance); vertical stacks get fractional order (e.g. 2.1, 2.2).
- **Move story then save:** User moves a story in DrawIO and saves. On sync: extracted graph contains that story with new x,y; layout JSON contains new position; `sequential_order` is recomputed from new position (left-to-right, vertical stacks). Merge report: story matches original by name (exact match); merge updates `sequential_order` (and users/connector) from extracted; merged graph keeps the story in the same epic/sub_epic (structure from original), with updated order.
- **Delete story:** User deletes one story cell from DrawIO. On sync: extracted graph omits that story; merge report lists it in `removed_stories`. If more than 50% of an epic’s (or a sub-epic’s) stories are missing, large deletion report includes `epics_with_many_missing_stories` or `sub_epics_with_many_missing_stories`. Merge: merged graph is a copy of original with updates only for matched stories; the deleted story remains in the merged output (merge does not remove stories; it only updates matched ones).
- **Delete sub-epic:** User deletes a sub-epic box (feature) from DrawIO. On sync: that sub-epic is not in extracted epics/sub_epics; stories that were under it are assigned by position/containment—if they fall inside another sub-epic’s bounds they attach to that sub-epic, otherwise they attach to the epic by position. Merge report: those stories may appear as removed or under a different sub_epic depending on where they were drawn; large deletion report includes `missing_sub_epics` for the deleted sub-epic.
- **Delete epic:** User deletes an epic box from DrawIO. On sync: that epic is not in extracted; all its sub-epics and stories are absent from extracted. Merge report: all those stories in `removed_stories`; large deletion report includes `missing_epics` with that epic name and its sub_epic/story counts.
- **Layout persistence:** When sync runs with output_path, layout is written to `{output_path.stem}-layout.json` with keys for epics (EPIC|name), sub-epics (SUB_EPIC|epic|sub_epic), stories (epic|sub_epic|story), and users; values include x, y, and width/height where applicable, for use on next render.

### Update graph from map increments

- **Stories to increments (extraction):** Stories are assigned to increments by story Y vs increment lane Y (closest within tolerance 100px). Moving a story vertically in DrawIO changes its increment in the **extracted** graph.
- **Merge and increments:** Merge does **not** replace which stories belong to which increment. It starts from original; updates story fields (users, connector, sequential_order) from extracted within existing increments; and **adds** any extracted increment whose name is not in the original. So if the user moved a story to another lane in DrawIO, the **merged** graph still has the original increment membership unless a different merge strategy (e.g. replace increments from extracted) is used.

### Update story graph from map acceptance criteria

- **AC assignment (extraction):** AC cells are matched to stories by vertical position and containment (AC below story); AC text is parsed for When/Then and mapped to story acceptance_criteria or steps. Adding/removing AC boxes in DrawIO is reflected in the extracted graph.
- **Merge and AC:** Merge **preserves** acceptance_criteria and steps from the original for matched stories; it does **not** overwrite AC from the extracted graph. So AC edits in DrawIO appear in extracted JSON but are not applied into the merged graph by the current merge.

### Render story map increments – layout and extraction consistency

- **Rendering:** Increment lanes are rendered in story_graph order (by priority/index). Lane Y = increment_lane_y_start + (idx − 1) × 100; label = increment.name or "Increment {idx}"; cell id = increment{idx}. Stories are placed in lanes according to story_graph increments[].stories (no position-based assignment at render time). Increment label style: fillColor=#f5f5f5, strokeColor=#666666 (renderer); extractor currently looks for strokeColor=#f8f7f7 and x &lt; 0 – **style must align** for round-trip.
- **Layout for increments:** Layout data is used for epics/sub-epics in increments view; increment lane positions are computed from outline bottom (max_y + 50 or 340). Saved layout for increment boundaries is not currently applied on re-render (increment lanes are recalculated).

### Update graph from map increments – add, remove, rename, identification

- **How increments are identified (extraction):** Increment boxes are detected by style (strokeColor=#f8f7f7) and position (x &lt; 0). Sorted by Y (top to bottom). Each gets **priority = 1-based index** (position order). **Name = cell value** (label text). There is **no stable ID** (e.g. no "increment_uid") tying a DrawIO cell to "original Increment 2". So **original vs new is inferred only by name and position order**, not by identity.
- **Add increment:** User adds a new increment lane (new box on the left with new Y). Extracted list has one more increment (sorted by Y); name = whatever the user typed. Merge: increment matching is **by name only**. New name is not in existing_increment_names, so merged graph **appends** the new increment. So a genuinely new increment is correctly added.
- **Remove increment:** User deletes one increment box. Extracted list has fewer lanes (by Y order). Merge **does not remove** increments from the merged graph; it only **adds** extracted increments whose name is not already present. So the **removed increment (by name) remains in the merged graph** with its original stories. Stories that were in the deleted lane are assigned by Y to the **closest remaining** increment (within tolerance 100px) in the extracted graph; after merge, story membership in increments comes from merging increment content (merge updates story data within existing increments but does not delete existing increments). So: removed increment stays in merged; its stories may appear in another increment in extracted or be outside tolerance.
- **Rename increment:** User renames "Increment 1" to "Sprint 1". Extracted has one increment named "Sprint 1" (priority 1 by position). Merge: existing_increment_names = {"Increment 1", "Increment 2", ...}; "Sprint 1" is not in existing, so merge **appends** the extracted "Sprint 1" increment. **The original "Increment 1" is never removed.** So merged graph contains **both** "Increment 1" (original, with its stories) and "Sprint 1" (extracted, with stories that were in that lane). **System cannot distinguish "renamed" from "new"** – both are treated as "add by name". So rename is effectively treated as add; duplicate increment names are avoided only by the fact that the new name is different.
- **How to know original vs new:** With current logic: **by name only**. If the label in DrawIO matches an existing increment name, that extracted increment is not re-added (so we don’t duplicate). If the label does not match any existing name, the increment is treated as new and added. So: same name ⇒ assume same increment (no re-add); different name ⇒ assume new (add). Rename therefore cannot be reconciled to the original increment without a **stable identifier** (e.g. priority slot, or a stored id in the diagram) or a **merge strategy** that matches by position order (e.g. first extracted lane = first original lane) and then applies name/order updates.

---

## Known gaps and consistency requirements

These must hold for correct round-trip and merge behavior; current code may not satisfy all.

| Area | Requirement | Current state |
|------|--------------|---------------|
| **Layout keys** | Sub-epic layout key must be the same for save (sync) and load (render). | Sync writes `SUB_EPIC|epic|sub_epic`; renderer reads `FEATURE|epic|sub_epic`. Round-trip sub-epic positions are not applied until aligned. |
| **Increment cell style** | Increment labels in DrawIO must be detectable by the extractor. | Renderer uses strokeColor=#666666; extractor looks for strokeColor=#f8f7f7 and x &lt; 0. Align for round-trip. |
| **Merge – stories** | Merge can either update-in-place or replace structure. | Merge never removes stories or epics/sub-epics; only adds new increments by name and updates story fields for matches. |
| **Merge – increments** | Applying DrawIO increment membership to merged graph. | Merge does not replace which stories belong to which increment; it only adds new named increments. Increment membership from DrawIO is in extracted only. |
| **Merge – AC** | Whether AC edits in DrawIO should flow into merged graph. | Merge preserves original acceptance_criteria; it does not overwrite from extracted. |
| **Increment identity** | Distinguish renamed vs new increment. | By name only; rename is treated as add (merged graph can contain both old and new names). |

---

## Source Material

- Story graph: `docs/story/story-graph.json` (Invoke Bot > Perform Action > Synchronize Graph with Rendered Content)
- Synchronizer: `src/synchronizers/story_io/` (story_io_renderer.py, story_io_synchronizer.py, story_map_drawio_synchronizer.py, story_io_diagram.py)
- Examples: `src/synchronizers/story_io/examples/render-examples.ps1`, `sync-examples.ps1`
- Tests: `src/synchronizers/story_io/test_increment_priority.py`, `test_increment_full_cycle.py`
