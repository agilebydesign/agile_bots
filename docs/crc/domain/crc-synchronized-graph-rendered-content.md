# CRC Domain: Synchronized Graph with Rendered Diagram Content

**Scope:** Invoke Bot → Perform Action → Synchronized Graph with Rendered Diagram Content  
**Stories:** Render story map, Render story map increments, Render story map with acceptance criteria, Update graph from story map, Update graph from map increments, Update story graph from map acceptance criteria.

This domain models **bidirectional sync** between the story graph (JSON knowledge graph) and rendered diagram formats (DrawIO, and later Mermaid). All format-specific story maps and nodes expose the **same API** as the base StoryNode/StoryMap so that update and report generation can work recursively and any format can be source or target.

---

## Design principles

- **Unified API:** Base StoryNode API (get/update name, get node type, get node ID, get parent, sequential order, contains children, delete self, delete with children, move, rename, etc.) is implemented by both JSON-backed nodes and diagram-backed nodes (DrawIO, Mermaid). Platform-specific read/write is hidden behind implementation classes.
- **Recursive responsibility:** Each node is responsible for its own contribution to update reports and for applying updates to itself and its children. So `StoryMap.update(other)` and `StoryMap.generateUpdateReport(other)` delegate recursively to nodes.
- **Report-then-update flow:** User can generate a report, review/edit it (e.g. mark safe edits), then apply: `report = DrawIOStoryMap.generateUpdateReport(storyMap)`; `StoryMap.update(DrawIOStoryMap, report)`. If no report is passed to `update`, the system can generate the report internally and auto-apply (with optional warnings).
- **Re-render preserves layout:** When the story graph changes and the diagram is re-rendered, saved layout data (position/size per node) is applied so only add/remove/change are reflected; positioning is not lost.

---

## Referenced concepts (existing)

These live in the broader story graph domain; this sub-domain extends or uses them.

- **StoryNode (Base)** – module: story_graph.nodes. Read/write stories in JSON knowledge graph; get/update name, node type, node ID, parent, sequential order; contains children; delete self / delete with children; get/update test; serialize via StoryNodeSerializer.
- **StoryNodeChildren** – module: story_graph.nodes. Get children, find child by name, delete child.
- **StoryNodeNavigator** – module: story_graph.nodes. Build node ID from path, get parent, move to parent / move after / move before, determine order.
- **StoryNodeSerializer** – module: story_graph.nodes. File, create/load/update/delete node, from/to JSON.
- **StoryMap** – module: story_graph.story_map. Load from bot directory or story graph file; walk nodes; get all stories/scenarios/domain concepts; find by name, find node by path; get story graph dict; get epics; save/reload; validate graph structure.

---

## Module: synchronizers.story_io (rendered content)

### DrawIOElement (Base)

Base for any element that is read from or written to DrawIO XML. Provides geometry and cell identity; format-specific read/write is implemented by subclasses.

- Get/Set position and size: Position, Boundary, DrawIO Cell
- Read from DrawIO XML: File Path, mxCell Element, DrawIO Tree
- Write to DrawIO XML: DrawIOStoryNodeSerializer, mxCell, DrawIO Tree
- Cell style (fill, stroke, text): Style String, DrawIO Cell
- Identity for matching on re-extract: Cell Id, String

*Note: DrawIOStoryNode and DrawIOStoryMap inherit from this and from StoryNode/StoryMap so they have both the diagram representation and the unified story API.*

---

### DrawIOStoryNode: DrawIOElement, StoryNode

Same API as StoryNode but backed by DrawIO: reads and writes itself and recursively invokes the corresponding read, write, and draw methods on its children nodes. This enables fully hierarchical diagram extraction and update. Does **not** draw scenarios in DrawIO (only epics, sub-epics, stories, and optionally acceptance criteria / increment lanes). Platform-specific read/write is handled in implementation details.

- Load from DrawIO: DrawIOStoryNodeSerializer, File, DrawIO XML
- Serialize to DrawIO: DrawIOStoryNodeSerializer, DrawIO XML
- Get/Update name: String, DrawIO Cell
- Get parent: Parent StoryNode, DrawIO Cell, Boundary
- Get sequential order: Float, Position, DrawIO Tree
- Move, rename: New Parent, Position, DrawIO Tree
- Generate own slice of update report: Other StoryNode, UpdateReport
- Apply update from other node (recursive): Other StoryNode, UpdateReport

*Subclasses: DrawIOEpic, DrawIOSubEpic, DrawIOStory (no DrawIO scenario – scenarios not drawn in DrawIO).*
---

### DrawIOStoryNodeSerializer

Format-specific load and serialize for story nodes; used by every DrawIO node for read and write.

- Load node from DrawIO: File, DrawIO XML, DrawIOStoryNode
- From DrawIO XML: DrawIO XML, DrawIOStoryNode
- To DrawIO XML: DrawIOStoryNode, DrawIO XML
- Create node in DrawIO: File, DrawIOStoryNode, mxCell
- Update node in DrawIO: File, DrawIOStoryNode
- Delete node from DrawIO: File, DrawIOStoryNode

---

### DrawIOEpic: Epic, DrawIOStoryNode

DrawIO-backed epic. Same API as Epic. Responsible for own report generation and update; delegates to children recursively.

- Get sub-epics: List[DrawIOSubEpic]
- Get all stories: List[DrawIOStory]
- Generate update report for this epic subtree: Other Epic/StoryMap, UpdateReport
- Update from other epic (recursive): Other Epic, UpdateReport

---

### DrawIOSubEpic: SubEpic, DrawIOStoryNode

DrawIO-backed sub-epic. Same API as SubEpic.

- Get stories: List[DrawIOStory]
- Generate update report for this sub-epic subtree: Other SubEpic, UpdateReport
- Update from other sub-epic (recursive): Other SubEpic, UpdateReport

---

### DrawIOStory: Story, DrawIOStoryNode

DrawIO-backed story. Same API as Story. Scenarios are not drawn in DrawIO; story is the leaf node in the diagram from a hierarchy perspective.

- Get story type from cell style: String, DrawIO Cell
- Generate update report for this story: Other Story, UpdateReport
- Update from other story: Other Story, UpdateReport

---

### DrawIOStoryMap: StoryMap

Story map backed by a DrawIO file. Same API as StoryMap for structure and navigation; in addition supports rendering, update and report generation, DrawIO read/write, and sync behavior. Renders itself from a StoryMap based on its diagramType. Recursive: each node contributes to the report and applies updates.

- **Diagram type (outline, increments, acceptance_criteria):** DiagramType — determines what the render produces
- Load from DrawIO file: File Path, DrawIOStoryMap, DrawIOStoryNodeSerializer
- Save to DrawIO file: File Path, DrawIOStoryNodeSerializer, DrawIOStoryMap
- **Render from StoryMap (based on diagramType):** StoryMap, DiagramType, LayoutData, DrawIO XML
- Apply layout data (saved positions) during render: LayoutData, DrawIOStoryNode
- Default layout when no layout data: DrawIOStoryNode, Spacing
- **Generate update report:** `generateUpdateReport(other: StoryMap) -> UpdateReport`. Other can be base StoryMap or another format. Recursively builds report (exact matches, fuzzy matches, new, removed, large_deletions).
- **Update from other:** `update(other: StoryMap, report: Optional[UpdateReport] = None)`. If report is None, generate report then apply. Applies report to self (recursive over nodes). User can edit report to mark safe edits before calling update.
- Own layout data (positions and sizes for rendered nodes): LayoutData, DrawIOStoryNode
- Persist layout data alongside diagram file: LayoutData, File Path
- Load layout data for re-render: File Path, LayoutData
- Assign stories to sub-epics by containment on load: Story Center, SubEpic Boundary
- Assign sequential order from position on load (left-to-right, top-to-bottom): DrawIOStoryNode, Float
- Extract layout (position/size per node) on load: DrawIO XML, LayoutData

*Usage: `r = DrawIOStoryMap.generateUpdateReport(storyMap)`; `storyMap.update(drawIOStoryMap, r)`. Or `drawIOStoryMap.update(storyMap)` (no report → generate and auto-apply).*

---

### UpdateReport

Result of comparing a “source” story map (e.g. extracted from diagram) with a “target” (e.g. original story graph). Consumed by `StoryMap.update(other, report)` to apply only intended changes; user can edit report to approve/reject or scope updates.

- Exact matches: List[Match Entry]
- Fuzzy matches: List[Match Entry], Confidence
- New stories (in source, not in target): List[Story Entry]
- Removed stories (in target, not in source): List[Story Entry]
- Large deletions: Missing Epics, Missing Sub-Epics
- Timestamp, source path, target path: Metadata
- Serialize to/from JSON: File Path, Report JSON

---

### LayoutData

Position and size per node for re-render. Persisted alongside the diagram (e.g. JSON file) so that when the story graph is updated and the diagram is re-rendered, positions are preserved and only add/remove/change are applied.

- Store position and size per node: Node Id, Position, Boundary
- Load from file: File Path, LayoutData
- Save to file: File Path
- Apply to diagram render: Renderer, Diagram
- Extract from diagram (on sync): DrawIO Tree, LayoutData

---

### StoryMap (extended responsibilities)

Existing StoryMap gains sync entry points so that any implementation (JSON or DrawIO/Mermaid) can be source or target. These are recursive over nodes.

- **Generate update report:** `generateUpdateReport(other: StoryMap) -> UpdateReport`. Delegates to root/epics; each node contributes its slice.
- **Update from other:** `update(other: StoryMap, report: Optional[UpdateReport] = None)`. If report is None, generate then apply. Delegates recursively (e.g. Epic.update(DrawIOEpic), Story.update(DrawIOStory)) so that the whole graph updates from the diagram (or vice versa).

*So we can call `StoryMap.update(DrawIOStoryMap, r)` or `DrawIOStoryMap.update(StoryMap, r)`; later `MermaidStoryMap.update(DrawIOStoryMap)` etc.*

---

### StoryGraph (extended responsibilities)

Top-level story graph. Update works on every node recursively.

- **Update from diagram map:** e.g. `StoryGraph.update(DrawIOStoryMap)` or equivalently at epic level: each Epic updates from the corresponding DrawIOEpic (and so on for sub-epics and stories). All versions emulate base StoryNode API including move, rename, delete.
- **Generate update report for graph:** Delegates to StoryMap.generateUpdateReport(diagramStoryMap).
- Re-render after update: Preserve layout (LayoutData); only add/remove/change; warn when things go wrong.

---

## Future: other diagram formats

### MermaidStoryMap: StoryMap

Same idea as DrawIOStoryMap but backed by Mermaid. Enables `MermaidStoryMap.update(DrawIOStoryMap)` or `StoryMap.update(MermaidStoryMap, report)` so any format can read/write to any other via the unified StoryNode/StoryMap API. Not in current scope; included for context.

---

## Summary: key flows

1. **Render:** StoryMap (JSON) → DrawIOStoryMap.render() → DrawIO file + LayoutData.
2. **User edits diagram** in DrawIO.
3. **Sync (report then update):** `report = DrawIOStoryMap.generateUpdateReport(StoryMap)`; user may edit report; `StoryMap.update(DrawIOStoryMap, report)`.
4. **Or auto-update:** `DrawIOStoryMap.update(StoryMap)` (no report → generate and apply).
5. **Re-render:** Story graph changed → render again using LayoutData so positions are preserved; only add/remove/change.

All node types (Epic, SubEpic, Story) in both JSON and DrawIO (and later Mermaid) emulate the base StoryNode API so that move, rename, delete, and recursive update/report work uniformly.
