---
name: Refactor Synchronize Architecture
overview: Refactor synchronization code to align with domain model, introduce three-tier node hierarchy (StoryNode -> DiagramNode -> DrawIONode), extract StoryMapUpdater, add Increment domain type, and split DrawIOStoryMap god class. Fixes 144 scanner violations.
todos:
  - id: phase0
    content: "Phase 0: Update domain model (story-graph.json domain_concepts, CRC doc, walkthrough) with deltas below"
    status: pending
  - id: phase1
    content: "Phase 1: Add Increment domain type to nodes.py, delete increment_views.py"
    status: pending
  - id: phase2
    content: "Phase 2: Extract StoryMapUpdater from StoryMap.apply_update_report"
    status: pending
  - id: phase3
    content: "Phase 3: Introduce DiagramNode middle tier (DiagramEpic, DiagramSubEpic, DiagramStory, DiagramIncrement)"
    status: pending
  - id: phase4
    content: "Phase 4: Split DrawIOStoryMap into OutlineMap, ExplorationMap, IncrementsMap subclasses"
    status: pending
  - id: phase5
    content: "Phase 5: Replace isinstance chains with template methods, typed returns, kill comments"
    status: pending
isProject: false
---

# Refactor Synchronize Architecture

## Problem

144 scanner violations across 9 files in `src/synchronizers/story_io/`. Root causes are architectural:

- `DrawIOStoryMap` is 1141 lines (limit: 300) -- god class doing render, load, extract, report, increment, AC
- No separation between diagram-agnostic rules (positioning, containment, formatting) and DrawIO-specific XML read/write
- No `Increment` domain type -- increments are raw `List[Dict]`
- `StoryMap.apply_update_report()` has update/merge logic that belongs in a dedicated updater
- isinstance chains instead of template methods
- Methods return `Dict[str, Any]` instead of typed objects

---

## Adjusted Domain Model

This is the target CRC model after refactoring. Deltas from the current [crc-synchronized-graph-rendered-content.md](docs/crc/domain/crc-synchronized-graph-rendered-content.md) are marked with `[NEW]`, `[MODIFIED]`, or `[REMOVED]`.

### Referenced concepts (existing, with modifications)

**StoryNode (Base)** -- module: story_graph.nodes

- (existing responsibilities unchanged)
- `[NEW]` is_new: bool property -- True when this node exists in the source but not the target. Set during comparison. Queryable by anyone, not just reports.
- `[NEW]` is_removed: bool property -- True when this node exists in the target but not the source.
- `[NEW]` has_moved: Optional[Move] property -- None if not moved; otherwise a Move object with from_parent and to_parent. Richer than a bool because consumers need the locations.
- `[NEW]` is_renamed: Optional[Rename] property -- None if not renamed; otherwise a Rename with original_name and new_name.

These are state properties on the node, not reporting methods. The StoryMapUpdater sets them during comparison; the UpdateReport reads them; future consumers (CLI display, diff views, etc.) can read them too.

**StoryMap** -- module: story_graph.story_map

- (existing responsibilities unchanged)
- `[MODIFIED]` apply_update_report() REMOVED -- replaced by StoryMapUpdater
- `[NEW]` generate_update_report(other_map) -> UpdateReport: convenience wrapper, creates StoryMapUpdater internally
- `[NEW]` merge(other_map, report=None): convenience wrapper. If no report, generates one first. Delegates to StoryMapUpdater.
- `[NEW]` increments: IncrementCollection (was List[Dict])
- `[NEW]` Epics: Pointer to top level Epics Collection, entry point to iterating through the story map hierarchy

### New concepts

**Increment** `[NEW]` -- module: story_graph.nodes

Domain type for a prioritized delivery slice containing story references.

- name: String
- priority: Int
- stories: List of story name references
- format_for_cli(): String (absorbs increment_views.py logic)

**IncrementCollection** `[NEW]` -- module: story_graph.nodes

- Iterable over Increment objects
- find_by_name(name): Increment
- find_by_priority(priority): Increment
- sorted_by_priority: List[Increment]

**StoryMapUpdater** `[NEW]` -- module: story_graph.updater

Owns comparison and merge logic between two story maps. Instantiated with the target map.

- Instantiate with target map: StoryMap
- generate_report_from(source_map): UpdateReport -- compares source against target, stores source + report
- update_from_report(opt source, opt report): applies changes. If no args, uses stored source + last report.
- reconcile_moves(original_map): reclassifies new+removed as moved
- reconcile_ac_moves(): reclassifies AC adds+removes as AC moves

**DiagramStoryNode** `[NEW]` -- module: synchronizers.story_io.diagram_story_node

Platform-agnostic diagram rules. Inherits from StoryNode. Knows positioning, containment, and formatting but nothing about DrawIO XML, mxCell, or any specific tool.

Same API as StoryNode for mutation (create, add_child, move, delete, rename) but operations also enforce diagram rules (placement, containment). Methods that are not yet needed raise NotImplementedError as stubs for future platform implementations.

- position: Position
- boundary: Boundary
- containment_rules(): which parent types this node fits inside
- placement_rules(): how to position relative to siblings (left-to-right by sequential_order, Y offset from parent)
- formatting_rules(): fill, stroke, font_color, shape by node type
- compute_container_dimensions_from_children(spacing): Boundary
- create(domain_node, parent): creates a diagram node from a domain node. Uses serializer internally. Same pattern as StoryNode.create(). Each subclass overrides to produce the right type.
- add_child(child): adds child and applies placement rules
- move_to(new_parent): moves node and re-applies containment/placement rules
- delete(): removes from parent
- rename(new_name): updates name
- recognizes(element): returns bool -- does this node type recognize the element? Used for classification.

Subclasses:

**DiagramEpic** `[NEW]` (Epic, DiagramStoryNode):

- fill #e1d5e7, stroke #9673a6, shape rounded
- Y: EPIC_Y constant, width: spans all child sub-epics

**DiagramSubEpic** `[NEW]` (SubEpic, DiagramStoryNode):

- fill #d5e8d4, stroke #82b366, shape rounded
- Y: parent Y + offset per depth, width: spans all child stories

**DiagramStory** `[NEW]` (Story, DiagramStoryNode):

- fill varies by story_type: user=#fff2cc/#d6b656/black, system=#1a237e/#0d47a1/white, technical=#000000/#333333/white
- Y: below deepest sub-epic, size: CELL_SIZE x CELL_SIZE

**DiagramIncrement** `[NEW]` (Increment, DiagramStoryNode):

- fill #f5f5f5, stroke #666666, bold label
- Y: below outline bottom, ordered by priority, lane height fixed

### Modified concepts

**DrawIOStoryNode** `[MODIFIED]` -- now inherits DiagramStoryNode instead of StoryNode directly

Keeps only DrawIO-specific read/write. All positioning, containment, and formatting rules come from DiagramStoryNode.

- cell_id: String (DrawIO cell identity)
- element: DrawIOElement (DrawIO XML backing)
- read_from_xml(mxCell): reads position/style from DrawIO XML into DiagramStoryNode properties
- write_to_xml(): serializes DiagramStoryNode properties to DrawIO mxCell

Subclasses: DrawIOEpic, DrawIOSubEpic, DrawIOStory, DrawIOIncrement `[RENAMED from DrawIOIncrementLane]`

**DrawIOStoryMap** `[MODIFIED]` -- split into base + diagram-type subclasses

Base keeps: save, load, extract_layout, queries (get_epics, get_sub_epics, get_stories)

Subclasses:

- **DrawIOOutlineMap**: render() for outline diagrams
- **DrawIOExplorationMap**: render() for AC diagrams, AC extraction
- **DrawIOIncrementsMap**: render() for increment diagrams, increment extraction

Report generation moved to StoryMapUpdater.

### Removed concepts

- `[REMOVED]` increment_views.py -- logic absorbed by Increment and IncrementCollection
- `[REMOVED]` StoryMap.apply_update_report() -- replaced by StoryMapUpdater

---

## Round-Trip Walkthrough: Render, Edit, Report, Merge

Full lifecycle: render story map to DrawIO, user edits (rename, add, remove, move), generate update report, merge back.

### Setup

StoryMap has 1 epic "Invoke Bot", 2 sub-epics:
- "Initialize Bot" with stories: "Load Config" (order 1), "Load Configuration" (order 2), "Register Behaviors" (order 3)
- "Perform Action" with stories: "Execute Action" (order 1)

### Step 1: Render Outline to DrawIO

```
StoryMap
    story_map = StoryMap.load('docs/story/story-graph.json')

LayoutData
    layout_data = LayoutData.load('story-map-layout.json')
        -> file not found, returns None

DrawIOOutlineMap
    outline = DrawIOOutlineMap()
    summary = outline.render(story_map, layout_data=None)

        -> epics = story_map.epics
        -> for epic in epics:

            DrawIOEpic
                drawio_epic = DrawIOEpic.create(epic, parent=outline)
                    -> DiagramEpic.formatting_rules()
                        fill: '#e1d5e7', stroke: '#9673a6', font_color: 'black', shape: 'rounded'
                    -> DiagramEpic.placement_rules()
                        position: x=20, y=EPIC_Y(120)
                    -> DrawIOEpic.write_to_xml()
                        serializes to mxCell

                -> for sub_epic in epic.sub_epics:

                    DrawIOSubEpic
                        drawio_se = DrawIOSubEpic.create(sub_epic, parent=drawio_epic)
                            -> DiagramSubEpic.formatting_rules()
                                fill: '#d5e8d4', stroke: '#82b366'
                            -> DiagramSubEpic.placement_rules()
                                y: epic.y + SUB_EPIC_OFFSET(75)

                        -> for story in sub_epic.stories (sorted by sequential_order):

                            DrawIOStory
                                drawio_story = DrawIOStory.create(story, parent=drawio_se)
                                    -> DiagramStory.formatting_rules()
                                        story_type 'user': fill '#fff2cc', stroke '#d6b656', font_color 'black'
                                    -> DiagramStory.placement_rules()
                                        y: rows.story_y, x: cursor_x, size: CELL_SIZE x CELL_SIZE

                            (same for 'Load Configuration', 'Register Behaviors', 'Execute Action')

                        DiagramSubEpic.compute_container_dimensions_from_children([stories])
                            -> width = sum(story widths) + spacing

                    DiagramEpic.compute_container_dimensions_from_children([sub_epics])
                        -> width = sum(sub_epic widths) + spacing

    outline.save('docs/story/story-map-outline.drawio')
        -> DrawIOStoryNodeSerializer.to_drawio_xml(all_nodes)
        -> File.write(path, xml)

    return RenderSummary(epics=1, sub_epic_count=2, diagram_generated=True)
```

### Step 2: User Edits in DrawIO

User opens `story-map-outline.drawio` and:
- Renames "Load Configuration" to "Load Settings"
- Adds new story cell "Validate Config" under "Initialize Bot"
- Deletes "Register Behaviors" cell
- Drags "Load Config" from "Initialize Bot" into "Perform Action"
- Saves

### Step 3: Load Edited Diagram

```
DrawIOOutlineMap
    drawio_map = DrawIOOutlineMap.load('story-map-outline.drawio')

        -> Pass 1a: Read raw XML into DrawIOElement nodes
        -> DrawIOStoryNodeSerializer.read_all_cells(content)
            -> for each mxCell with vertex="1":
                -> raw_node = DrawIOElement.read_from_xml(mxCell)
                    -> reads x, y, width, height, style, value
            -> returns raw_nodes[]

        -> Pass 1b: Classify by asking each type if it recognizes the element
            -> for each raw_node in raw_nodes:
                -> DrawIOEpic.recognizes(raw_node)?
                    -> decides internally
                -> DrawIOSubEpic.recognizes(raw_node)?
                    -> decides internally
                -> DrawIOStory.recognizes(raw_node)?
                    -> decides internally
                -> DrawIOIncrement.recognizes(raw_node)?
                    -> decides internally
                -> first match wins; conflict = error
                -> classified_node = MatchedType.from_element(raw_node)
            -> returns flat lists: epics[], sub_epics[], stories[], increments[]

        -> Pass 2: Build hierarchy top-down by iterating and checking containment

        -> for epic in epics:
            drawio_map.add_child(epic)

            -> for sub_epic in sub_epics:
                -> DiagramSubEpic.containment_rules()
                    sub_epic center inside epic boundary?
                -> 'Initialize Bot' center (200, 160) inside 'Invoke Bot' boundary (20..650, 120..420)
                    -> yes: epic.add_child(sub_epic)
                -> 'Perform Action' center inside 'Invoke Bot' boundary
                    -> yes: epic.add_child(sub_epic)

                -> for story in stories:
                    -> DiagramStory.containment_rules()
                        story center inside sub_epic boundary?

                    For 'Initialize Bot':
                    -> 'Load Settings' center (100, 235) inside 'Initialize Bot' boundary (30..280, 180..380)
                        -> yes: sub_epic.add_child(story)
                    -> 'Validate Config' center (160, 235) inside 'Initialize Bot' boundary
                        -> yes: sub_epic.add_child(story)

                    For 'Perform Action':
                    -> 'Execute Action' center (350, 235) inside 'Perform Action' boundary (310..580, 180..380)
                        -> yes: sub_epic.add_child(story)
                    -> 'Load Config' center (420, 235) inside 'Perform Action' boundary
                        -> yes: sub_epic.add_child(story)
                        -> (user dragged it here)

        -> Sequential order NOT reassigned from position.
        -> Loaded nodes carry sequential_order from original render.
        -> 'Load Config' still has order 1.0.
        -> 'Validate Config' (user-created) has no sequential_order.

        return drawio_map
            -> epics: [DrawIOEpic('Invoke Bot')]
                -> sub_epics:
                    [DrawIOSubEpic('Initialize Bot')]
                        -> stories: [DrawIOStory('Load Settings'), DrawIOStory('Validate Config')]
                    [DrawIOSubEpic('Perform Action')]
                        -> stories: [DrawIOStory('Execute Action'), DrawIOStory('Load Config')]
```

### Step 4: Generate Update Report via StoryMapUpdater

```
StoryMap
    story_map = StoryMap.load('docs/story/story-graph.json')

StoryMapUpdater
    updater = StoryMapUpdater(target_map=story_map)
    report = updater.generate_report_from(source_map=drawio_map)

        -> extracted_epics = drawio_map.epics (sorted by sequential_order)
        -> original_epics = story_map.epics (sorted by sequential_order)

        -> _compare_node_lists(extracted_epics, original_epics, report, recurse=True)

            DrawIOEpic('Invoke Bot').compare_children(Epic('Invoke Bot'), report)
                -> _compare_node_lists(drawio_sub_epics, original_sub_epics, report)

                    DrawIOSubEpic('Initialize Bot').compare_children(SubEpic('Initialize Bot'), report)
                        -> _compare_node_lists(drawio_stories, original_stories, report)
                        -> original: ['Load Config' (1), 'Load Configuration' (2), 'Register Behaviors' (3)]
                        -> extracted: ['Load Settings' (2), 'Validate Config' (None)]

                            Phase 1: Exact matches -- skip, no change
                            No exact name matches.

                            Phase 2: Rename detection
                            DrawIOStory('Load Settings') sequential_order 2.0
                            Story('Load Configuration') sequential_order 2.0
                            Same position, different name -> rename.
                                -> Story('Load Configuration').is_renamed = Rename(
                                       original_name='Load Configuration', new_name='Load Settings')

                            DrawIOStory('Validate Config') has no sequential_order (user-created)
                            No remaining originals to pair
                                -> DrawIOStory('Validate Config').is_new = True

                            Phase 3: Remaining originals = removed (tentative)
                            Story('Load Config') unmatched in 'Initialize Bot'
                                -> Story('Load Config').is_removed = True (tentative)
                            Story('Register Behaviors') unmatched
                                -> Story('Register Behaviors').is_removed = True

                    DrawIOSubEpic('Perform Action').compare_children(SubEpic('Perform Action'), report)
                        -> _compare_node_lists(drawio_stories, original_stories, report)
                        -> original: ['Execute Action' (1)]
                        -> extracted: ['Execute Action' (1), 'Load Config' (1)]

                            Phase 1: Exact matches
                            DrawIOStory('Execute Action') matches Story('Execute Action')
                                -> no change recorded.

                            Phase 2: Remaining extracted
                            DrawIOStory('Load Config') not in original 'Perform Action'
                                -> DrawIOStory('Load Config').is_new = True (tentative)

        -> updater.reconcile_moves(story_map)
            -> 'Load Config' appears as removed from 'Initialize Bot' AND new in 'Perform Action'
            -> same name, different parents -> move, not new+removed
            -> Story('Load Config').is_removed = False
            -> DrawIOStory('Load Config').is_new = False
            -> Story('Load Config').has_moved = Move(
                   from_parent='Initialize Bot', to_parent='Perform Action')

        -> report stored as updater._last_report
        -> source stored as updater._last_source

        return report (built from node state properties):
            renames: [{original: 'Load Configuration', new: 'Load Settings', parent: 'Initialize Bot'}]
            new: [{name: 'Validate Config', parent: 'Initialize Bot'}]
            removed: [{name: 'Register Behaviors', parent: 'Initialize Bot'}]
            moved: [{name: 'Load Config', from: 'Initialize Bot', to: 'Perform Action'}]
```

### Step 5: User Reviews Report (Optional)

User inspects report JSON, approves.

### Step 6: Merge -- Apply Report

```
StoryMapUpdater
    updater.update_from_report()
        -> uses stored _last_source and _last_report

        -> Apply renames
        -> node = story_map.find_node('Load Configuration')
        -> node.name = 'Load Settings'
        -> node.sequential_order unchanged (2.0)

        -> Apply new
        -> parent = story_map.find_node('Initialize Bot')
        -> new_story = parent.create_story(name='Validate Config')
        -> new_story.sequential_order = parent.highest_sequential_order + 1
           -> 3.0 + 1 = 4.0

        -> Apply moves
        -> story = story_map.find_node('Load Config')
        -> target = story_map.find_node('Perform Action')
        -> story.move_to(target)
        -> story.sequential_order = target.highest_sequential_order + 1
           -> 1.0 + 1 = 2.0

        -> Removed (flagged, not deleted)
        -> Story('Register Behaviors').is_removed = True
        -> sequential_order preserved (3.0)
```

### Step 7: Save and Re-render

```
StoryMap
    story_map.save()
        -> writes updated story-graph.json:
            Initialize Bot:
                'Load Settings' (order 2.0, renamed)
                'Register Behaviors' (order 3.0, is_removed=True)
                'Validate Config' (order 4.0, new)
            Perform Action:
                'Execute Action' (order 1.0)
                'Load Config' (order 2.0, moved)

DrawIOOutlineMap
    outline = DrawIOOutlineMap()
    layout_data = LayoutData.load('story-map-outline-layout.json')
    summary = outline.render(story_map, layout_data=layout_data)
        -> saved positions for existing nodes
        -> 'Validate Config' gets default position
        -> 'Register Behaviors' not rendered
    outline.save('story-map-outline.drawio')
    outline.save_layout('story-map-outline-layout.json')
```

---

## Phase 0: Update Domain Model

Update `story-graph.json` domain_concepts, CRC doc, and walkthrough doc with adjusted model and walkthrough above.

## Phase 1: Increment Domain Type

In [src/story_graph/nodes.py](src/story_graph/nodes.py):
- Create `Increment` dataclass
- Create `IncrementCollection`
- Change `StoryMap.increments` from `List[Dict]` to `IncrementCollection`
- Delete [src/synchronizers/story_io/increment_views.py](src/synchronizers/story_io/increment_views.py)

## Phase 2: StoryMapUpdater

Extract from `StoryMap.apply_update_report()` into `StoryMapUpdater`. StoryMap keeps thin wrappers `generate_update_report(other)` and `merge(other, report=None)`.

## Phase 3: DiagramNode Middle Tier

Create [src/synchronizers/story_io/diagram_story_node.py](src/synchronizers/story_io/diagram_story_node.py) with DiagramStoryNode, DiagramEpic, DiagramSubEpic, DiagramStory, DiagramIncrement. DrawIOStoryNode inherits from DiagramStoryNode, keeping only DrawIO XML read/write.

## Phase 4: Split DrawIOStoryMap

Split [src/synchronizers/story_io/drawio_story_map.py](src/synchronizers/story_io/drawio_story_map.py) into base + DrawIOOutlineMap, DrawIOExplorationMap, DrawIOIncrementsMap.

## Phase 5: Node State Properties, Typed Returns, Cleanup

- State properties: `is_new`, `is_removed`, `has_moved`, `is_renamed` on StoryNode
- `participates_in_rename_pairing` property on DiagramStoryNode subclasses
- Typed returns: `RenderSummary`
- Delete 53 comments, fix 4 duplications, fix 1 swallowed exception

## Execution Order

Phase 0 -> 1 -> 2 -> 3 -> 4 -> 5. Each phase keeps 228 tests green.

## False Positives

- `avoid_excessive_guards` line 78 (geometry None check) -- XML parsing needs this
- `provide_meaningful_context` "layout_data" -- this IS the domain term
- Many encapsulation warnings about `List[TypedObject]` -- lower priority
