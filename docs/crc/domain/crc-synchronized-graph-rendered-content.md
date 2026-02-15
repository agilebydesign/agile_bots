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

- **StoryNode (Base)** – module: story_graph.nodes. Read/write stories in JSON knowledge graph; get/update name, node type, node ID, parent, sequential order; contains children; delete self / delete with children; get/update test; serialize via StoryNodeSerializer. NEW: is_new, is_removed (bool properties), has_moved (Optional[Move]), is_renamed (Optional[Rename]) -- state set during comparison, queryable by anyone.
- **StoryNodeChildren** – module: story_graph.nodes. Get children, find child by name, delete child.
- **StoryNodeNavigator** – module: story_graph.nodes. Build node ID from path, get parent, move to parent / move after / move before, determine order.
- **StoryNodeSerializer** – module: story_graph.nodes. File, create/load/update/delete node, from/to JSON.
- **StoryMap** – module: story_graph.story_map. Load from bot directory or story graph file; walk nodes; get all stories/scenarios/domain concepts; find by name, find node by path; get story graph dict; get epics; save/reload; validate graph structure. NEW: increments (IncrementCollection), generate_update_report(other) and merge(other, report=None) convenience wrappers that delegate to StoryMapUpdater.
- **Increment** – module: story_graph.nodes. Prioritized delivery slice with name, priority, and story name references. NEW domain type.
- **IncrementCollection** – module: story_graph.nodes. Iterable collection of Increments with find_by_name, find_by_priority, sorted_by_priority. NEW.
- **StoryMapUpdater** – module: story_graph.updater. Owns comparison and merge logic. Instantiated with target map; generate_report_from(source) compares and stores source+report; update_from_report(opt_source, opt_report) applies changes. NEW.

---

## Module: story_graph (domain extensions)

### Increment

Prioritized delivery slice containing story references.

- name: String
- priority: Int  
- stories: List of story name references
- format_for_cli(): String

### IncrementCollection

Iterable collection of Increments.

- Iterable over Increment objects
- find_by_name(name): Increment
- find_by_priority(priority): Increment
- sorted_by_priority: List[Increment]

### StoryMapUpdater

Owns comparison and merge logic between two story maps. Instantiated with the target map.

- Instantiate with target map: StoryMap
- generate_report_from(source_map): UpdateReport -- compares source against target, stores source and report
- update_from_report(opt source, opt report): applies changes. If no args, uses stored source + last report.
- reconcile_moves(original_map): reclassifies new+removed as moved
- reconcile_ac_moves(): reclassifies AC adds+removes as AC moves

---

## Module: synchronizers.story_io (rendered content)

### DiagramStoryNode: StoryNode

Platform-agnostic diagram rules (Tier 2). Positioning, containment, and formatting without knowledge of any specific diagram tool.

- position: Position
- boundary: Boundary
- containment_rules(): which parent types this node fits inside
- placement_rules(): how to position relative to siblings
- formatting_rules(): fill, stroke, font_color, shape by node type
- compute_container_dimensions_from_children(spacing): Boundary
- create(domain_node, parent): creates diagram node. Same API as StoryNode.create()
- add_child, move_to, delete, rename: same API as StoryNode, enforces diagram rules
- recognizes(element): returns bool -- classification

*Subclasses: DiagramEpic, DiagramSubEpic, DiagramStory, DiagramIncrement*

---

### DrawIOElement (Base)

Base for any element that is read from or written to DrawIO XML. Provides geometry and cell identity; format-specific read/write is implemented by subclasses.

- Get/Set position and size: Position, Boundary, DrawIO Cell
- Read from DrawIO XML: File Path, mxCell Element, DrawIO Tree
- Write to DrawIO XML: DrawIOStoryNodeSerializer, mxCell, DrawIO Tree
- Cell style (fill, stroke, text): Style String, DrawIO Cell
- Identity for matching on re-extract: Cell Id, String

*Note: DrawIOStoryNode and DrawIOStoryMap inherit from this and from StoryNode/StoryMap so they have both the diagram representation and the unified story API.*

---

### DiagramStoryNode: StoryNode

Platform-agnostic diagram rules. Same API as StoryNode but with diagram-specific positioning, containment, and formatting rules. Knows nothing about DrawIO XML or any specific tool format.

- Position and boundary: Position, Boundary
- Containment rules: which parent types this node fits inside
- Placement rules: position relative to siblings (left-to-right by sequential_order, Y offset from parent)
- Formatting rules: fill, stroke, font_color, shape by node type
- Compute container dimensions from children: Boundary, Spacing
- Create, add_child, move_to, delete, rename: same API as StoryNode but enforces diagram rules
- recognizes(element): returns bool -- does this type recognize the element?

*Subclasses: DiagramEpic, DiagramSubEpic, DiagramStory, DiagramIncrement*

---

### DrawIOStoryNode: DiagramStoryNode

Inherits DiagramStoryNode (Tier 2) instead of StoryNode directly. DrawIO-specific XML read/write and coordinate system. All positioning, containment, and formatting come from DiagramStoryNode.

- cell_id: DrawIO cell identity
- element: DrawIOElement (XML backing)
- read_from_xml(mxCell): reads position/style from XML into DiagramStoryNode properties
- write_to_xml(): serializes DiagramStoryNode properties to mxCell

*All positioning, containment, and formatting rules come from DiagramStoryNode. DrawIOStoryNode only handles DrawIO XML specifics.*

*Subclasses: DrawIOEpic, DrawIOSubEpic, DrawIOStory, DrawIOIncrement (renamed from DrawIOIncrementLane).*
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

Base class for DrawIO-backed story maps. Split into diagram-type subclasses (DrawIOOutlineMap, DrawIOExplorationMap, DrawIOIncrementsMap).

Base responsibilities:
- Load from DrawIO file: File Path, DrawIOStoryNodeSerializer
- Save to DrawIO file: File Path, DrawIOStoryNodeSerializer
- Extract layout: LayoutData, DrawIO XML
- Queries: get_epics, get_sub_epics, get_stories

Subclass responsibilities (render, diagram-specific extraction):
- **DrawIOOutlineMap**: render() for outline diagrams
- **DrawIOExplorationMap**: render() for AC diagrams, AC extraction
- **DrawIOIncrementsMap**: render() for increment diagrams, increment extraction

Report generation delegated to StoryMapUpdater.

*Usage via convenience wrappers: `report = storyMap.generate_update_report(drawioMap)` then `storyMap.merge(drawioMap, report)`.*

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

Existing StoryMap gains sync convenience wrappers. Actual logic is in StoryMapUpdater.

- **generate_update_report(other: StoryMap) -> UpdateReport**: Creates StoryMapUpdater(self), calls updater.generate_report_from(other), returns report.
- **merge(other: StoryMap, report: Optional[UpdateReport] = None)**: Creates StoryMapUpdater(self), calls updater.update_from_report(other, report). If no report, generates one first.

*So we can call `storyMap.merge(drawIOMap)` or with explicit report `storyMap.merge(drawIOMap, report)`. Bulk logic is in StoryMapUpdater.*

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

1. **Render:** StoryMap (JSON) → DrawIOOutlineMap.render() → DrawIO file + LayoutData.
2. **User edits diagram** in DrawIO.
3. **Sync (report then update):** `report = storyMap.generate_update_report(drawioMap)` (creates StoryMapUpdater internally); user may edit report; `storyMap.merge(drawioMap, report)`.
4. **Or auto-merge:** `storyMap.merge(drawioMap)` (no report → generates and applies in one call).
5. **Re-render:** Story graph changed → render again using LayoutData so positions are preserved; only add/remove/change.

All node types (Epic, SubEpic, Story) in both JSON and DrawIO (and later Mermaid) emulate the base StoryNode API so that move, rename, delete, and recursive update/report work uniformly.
