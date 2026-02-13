"""
DrawIOStoryMap - Domain model for rendering story maps to DrawIO.

Orchestrates rendering by delegating to domain nodes. Each node
(DrawIOEpic, DrawIOSubEpic, DrawIOStory, DrawIOIncrementLane) owns
its own rendering logic.  This class only coordinates creation order
and collects nodes for serialization.
"""
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from story_graph.nodes import StoryMap, Epic, SubEpic, Story, StoryGroup
from .drawio_story_node import (
    DrawIOStoryNode, DrawIOEpic, DrawIOSubEpic, DrawIOStory,
    DrawIOIncrementLane, SPACING, CONTAINER_PADDING, CELL_SIZE,
    _max_sub_epic_depth, _RowPositions, CELL_SPACING, ROW_GAP,
    _compare_node_lists, _collect_all_names,
)
from .drawio_story_node_serializer import DrawIOStoryNodeSerializer
from .layout_data import LayoutData
from .update_report import UpdateReport


class DrawIOStoryMap(StoryMap):

    def __init__(self, diagram_type: str = 'outline', story_graph: Dict[str, Any] = None):
        super().__init__(story_graph or {'epics': []})
        self._diagram_type = diagram_type
        self._drawio_epics: List[DrawIOEpic] = []
        self._extra_nodes: List = []          # increment lanes, AC boxes, etc.
        self._layout_data: Optional[LayoutData] = None

    @property
    def diagram_type(self) -> str:
        return self._diagram_type

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_epics(self) -> List[DrawIOEpic]:
        return list(self._drawio_epics)

    def get_sub_epics(self) -> List[DrawIOSubEpic]:
        result = []
        for epic in self._drawio_epics:
            result.extend(epic.get_sub_epics())
        return result

    def get_stories(self) -> List[DrawIOStory]:
        result = []
        for epic in self._drawio_epics:
            result.extend(epic.get_stories())
        return result

    def get_total_width(self) -> float:
        """Rightmost edge of the rendered outline content."""
        if not self._drawio_epics:
            return 0
        return max(e.boundary.right for e in self._drawio_epics)

    def get_bottom_y(self) -> float:
        """Lowest Y coordinate of any outline element (sub-epics or stories).

        Recursively checks nested sub-epics so that deeply nested elements
        (e.g. second-level sub-epics) are accounted for.
        """
        bottom = 0
        for story in self.get_stories():
            b = story.position.y + story.boundary.height
            if b > bottom:
                bottom = b
        for se in self._all_sub_epics_recursive():
            b = se.position.y + se.boundary.height
            if b > bottom:
                bottom = b
        return bottom

    def _all_sub_epics_recursive(self) -> List[DrawIOSubEpic]:
        """Return all sub-epics at every nesting level."""
        result = []
        stack = list(self.get_sub_epics())
        while stack:
            se = stack.pop()
            result.append(se)
            stack.extend(se.get_sub_epics())
        return result

    # ------------------------------------------------------------------
    # Render – Outline
    # ------------------------------------------------------------------

    def render_from_story_map(self, story_map: StoryMap,
                               layout_data: Optional[LayoutData] = None,
                               skip_stories: bool = False) -> Dict[str, Any]:
        """Render outline diagram.  Each node renders itself.

        Computes global row positions first so all epics share the
        same Y levels, then lays out epics left-to-right.

        When *skip_stories* is True the outline renders epics and
        sub-epics but omits story cells (used by the increments view
        where stories appear only in increment lanes).
        """
        self._layout_data = layout_data
        self._drawio_epics = []
        self._extra_nodes = []

        epics = list(story_map.epics)
        if not epics:
            return {'epics': 0, 'sub_epic_count': 0, 'diagram_generated': True}

        # Global max depth → consistent rows across all epics
        max_depth = max(_max_sub_epic_depth(epic) for epic in epics)
        rows = _RowPositions(max_depth)

        x_pos = DrawIOEpic.X_START
        for epic in epics:
            drawio_epic = DrawIOStoryNodeSerializer.create_epic(
                epic.name, getattr(epic, 'sequential_order', 0) or 0)
            drawio_epic.render_from_domain(epic, x_pos, rows, layout_data,
                                           skip_stories=skip_stories)
            self._drawio_epics.append(drawio_epic)
            x_pos = drawio_epic.boundary.right + CELL_SPACING

        return {
            'epics': len(self._drawio_epics),
            'sub_epic_count': len(self.get_sub_epics()),
            'diagram_generated': True,
        }

    # ------------------------------------------------------------------
    # Render – Increments  (outline + increment lanes below)
    # ------------------------------------------------------------------

    def render_increments_from_story_map(
            self, story_map: StoryMap,
            increments_data: list,
            layout_data: Optional[LayoutData] = None) -> Dict[str, Any]:
        """Render outline with orphaned stories, then increment lanes.

        Stories assigned to an increment appear ONLY in their lane.
        Stories NOT assigned to any increment ("orphaned") appear
        under their sub-epic just like a normal outline, providing
        context for the column structure.

        Increment lanes are positioned below the orphaned story area
        so there is room for potentially multiple rows of unassigned
        stories.
        """
        # Collect all story names that belong to at least one increment
        increment_story_names: set = set()
        for inc_data in increments_data:
            for s in inc_data.get('stories', []):
                increment_story_names.add(
                    s.get('name', '') if isinstance(s, dict) else str(s))

        # Phase 1: render full outline (epics, sub-epics, ALL stories)
        # so that orphaned stories appear under their sub-epics and we
        # get correct positions for every story.
        summary = self.render_from_story_map(story_map, layout_data,
                                             skip_stories=False)
        all_drawio_stories = self.get_stories()

        # Phase 2: remove increment-assigned stories from the outline
        # tree (they will live only in their lanes).  Orphaned stories
        # stay in the tree.
        for epic in self._drawio_epics:
            for se in epic.get_sub_epics():
                self._remove_increment_stories(se, increment_story_names)

        # Collect domain stories for user/actor info
        domain_stories = list(story_map.all_stories)

        # Phase 3: compute where increment lanes start.
        # Use the full story set's bottom (before removal) so column
        # widths are correct; then derive Y from the actual remaining
        # outline bottom which includes orphaned stories.
        outline_bottom = self.get_bottom_y()
        total_width = max(
            self.get_total_width(),
            max((s.position.x + CELL_SIZE for s in all_drawio_stories),
                default=0))

        # Reserve space below the outline for at least one row of orphan
        # stories (CELL_SIZE) plus padding.  This ensures lanes never overlap
        # with the deepest sub-epics or orphan story rows.
        y_start = outline_bottom + CELL_SIZE + ROW_GAP

        for idx, inc_data in enumerate(increments_data):
            story_names = []
            for s in inc_data.get('stories', []):
                story_names.append(s.get('name', '') if isinstance(s, dict) else str(s))

            lane = DrawIOIncrementLane(
                name=inc_data.get('name', f'Increment {idx + 1}'),
                priority=inc_data.get('priority', idx + 1),
                story_names=story_names)
            lane.render(idx, y_start, total_width, all_drawio_stories,
                        domain_stories=domain_stories)
            self._extra_nodes.extend(lane.collect_all_elements())

        summary['increments'] = len(increments_data)
        return summary

    @staticmethod
    def _remove_increment_stories(sub_epic: DrawIOSubEpic,
                                   increment_names: set):
        """Remove stories that belong to increments from a sub-epic tree.

        Recurses into nested sub-epics.  Only leaf sub-epics have stories.
        """
        for nested in sub_epic.get_sub_epics():
            DrawIOStoryMap._remove_increment_stories(nested, increment_names)
        to_remove = [s for s in sub_epic.get_stories()
                     if s.name in increment_names]
        for s in to_remove:
            sub_epic._children.remove(s)

    # ------------------------------------------------------------------
    # Render – Exploration / Acceptance Criteria
    # ------------------------------------------------------------------

    def render_exploration_from_story_map(
            self, story_map: StoryMap,
            layout_data: Optional[LayoutData] = None,
            scope: Optional[str] = None) -> Dict[str, Any]:
        """Render outline first, then add AC boxes below stories."""
        summary = self.render_from_story_map(story_map, layout_data)

        domain_stories = self._collect_domain_stories(story_map, scope)
        for drawio_story in self.get_stories():
            domain_story = domain_stories.get(drawio_story.name)
            if domain_story and domain_story.has_acceptance_criteria():
                ac_elems = drawio_story.render_ac_boxes(domain_story)
                self._extra_nodes.extend(ac_elems)

        summary['exploration'] = True
        if scope:
            summary['scope'] = scope
        return summary

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, file_path: Path):
        all_nodes = self._collect_all_nodes()
        xml_content = DrawIOStoryNodeSerializer.to_drawio_xml(all_nodes)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(xml_content, encoding='utf-8')

    def save_as_json(self, file_path: Path):
        data = self._to_story_graph_dict()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(data, indent=2), encoding='utf-8')

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def extract_layout(self) -> LayoutData:
        layout = LayoutData()
        for epic in self._drawio_epics:
            layout.set_entry(f'EPIC|{epic.name}',
                             epic.position.x, epic.position.y,
                             epic.boundary.width, epic.boundary.height)
            layout.set_entry(epic.cell_id,
                             epic.position.x, epic.position.y,
                             epic.boundary.width, epic.boundary.height)
            for se in epic.get_sub_epics():
                self._extract_layout_for_sub_epic(layout, epic.name, se)
        return layout

    def _extract_layout_for_sub_epic(self, layout: LayoutData, epic_name: str,
                                      se: DrawIOSubEpic):
        layout.set_entry(f'SUB_EPIC|{se.name}',
                         se.position.x, se.position.y,
                         se.boundary.width, se.boundary.height)
        layout.set_entry(se.cell_id,
                         se.position.x, se.position.y,
                         se.boundary.width, se.boundary.height)
        for nested_se in se.get_sub_epics():
            self._extract_layout_for_sub_epic(layout, epic_name, nested_se)
        for story in se.get_stories():
            layout.set_entry(
                f'STORY|{epic_name}|{se.name}|{story.name}',
                story.position.x, story.position.y,
                story.boundary.width, story.boundary.height)
            layout.set_entry(story.cell_id,
                             story.position.x, story.position.y,
                             story.boundary.width, story.boundary.height)

    # ------------------------------------------------------------------
    # Update report
    # ------------------------------------------------------------------

    def generate_update_report(self, original_story_map: StoryMap) -> UpdateReport:
        report = UpdateReport()

        # Pass 1: hierarchy comparison (horizontal position).
        extracted_epics = sorted(self._drawio_epics, key=lambda e: e.sequential_order or 0)
        original_epics = sorted(list(original_story_map.epics), key=lambda e: getattr(e, 'sequential_order', 0) or 0)

        # Collect all names from both trees so rename detection can
        # distinguish genuine renames from moves.
        all_extracted_names = _collect_all_names(extracted_epics)
        all_original_names = _collect_all_names(original_epics)

        _compare_node_lists(extracted_epics, original_epics, report,
                            parent_name='', recurse=True,
                            all_extracted_names=all_extracted_names,
                            all_original_names=all_original_names)

        # Flag large deletions: when entire epics or sub-epics are missing
        # from the diagram, flag them so the consumer can decide how to
        # handle bulk removals (e.g. confirmation prompt).
        for ep in report.removed_epics:
            report.add_missing_epic(ep.name)
        for se in report.removed_sub_epics:
            report.add_missing_sub_epic(se.name)

        # Reconcile moves: stories that appear in both new and removed
        # (or are descendants of removed sub-epics) are reclassified as
        # moved_stories so updateFromDiagram preserves their data.
        report.reconcile_moves(original_story_map)

        # Pass 2: increment assignments (vertical position).
        # Compare extracted state against original to produce the delta.
        extracted = self.extract_increment_assignments()
        if extracted:
            original_increments = original_story_map.story_graph.get('increments', [])
            self._compute_increment_delta(report, extracted, original_increments)
        return report

    def _compute_increment_delta(self, report: UpdateReport,
                                  extracted: list,
                                  original_increments: list):
        """Compare extracted increment assignments against original and
        populate the report with changes, moves, removals, and new order.
        """
        from .update_report import IncrementChange, IncrementMove

        # Build original: story → set of increment names
        orig_by_story: dict = {}  # story_name → set of increment names
        orig_by_inc: dict = {}    # inc_name → set of story names
        for inc in original_increments:
            inc_name = inc.get('name', '')
            stories = set()
            for s in inc.get('stories', []):
                name = s.get('name', '') if isinstance(s, dict) else str(s)
                stories.add(name)
                orig_by_story.setdefault(name, set()).add(inc_name)
            orig_by_inc[inc_name] = stories

        # Build extracted: story → set of increment names
        ext_by_story: dict = {}
        ext_by_inc: dict = {}
        for inc in extracted:
            inc_name = inc['name']
            stories = set(inc['stories'])
            ext_by_inc[inc_name] = stories
            for s in stories:
                ext_by_story.setdefault(s, set()).add(inc_name)

        # Compute per-increment changes (only include increments that changed)
        all_inc_names = list(dict.fromkeys(
            [inc.get('name', '') for inc in original_increments] +
            [inc['name'] for inc in extracted]))

        changes = []
        for inc_name in all_inc_names:
            orig_stories = orig_by_inc.get(inc_name, set())
            ext_stories = ext_by_inc.get(inc_name, set())
            added = sorted(ext_stories - orig_stories)
            removed = sorted(orig_stories - ext_stories)
            if added or removed:
                changes.append(IncrementChange(
                    name=inc_name, added=added, removed=removed))

        # Compute moves (story was in increment A, now in increment B)
        moves = []
        all_stories = set(orig_by_story.keys()) | set(ext_by_story.keys())
        for story in sorted(all_stories):
            orig_incs = orig_by_story.get(story, set())
            ext_incs = ext_by_story.get(story, set())
            if orig_incs == ext_incs:
                continue
            # Story gained new increment(s)
            for inc in sorted(ext_incs - orig_incs):
                from_inc = ''
                # If it was in exactly one before and is now somewhere else,
                # that's a move from old → new
                if len(orig_incs) == 1 and len(ext_incs) == 1:
                    from_inc = next(iter(orig_incs))
                moves.append(IncrementMove(
                    story=story, from_increment=from_inc, to_increment=inc))

        # Compute removed increments: in original but not in extracted
        ext_inc_names = set(ext_by_inc.keys())
        removed_increments = [
            inc.get('name', '') for inc in original_increments
            if inc.get('name', '') not in ext_inc_names
        ]

        # Only include increment_order when the name sequence actually
        # changed.  Compare name order only -- not priority values --
        # because original priorities may not be sequential 1..N.
        new_name_seq = [inc['name'] for inc in extracted]
        orig_name_seq = [inc.get('name', '') for inc in original_increments]
        if new_name_seq != orig_name_seq:
            increment_order = [
                {'name': n, 'priority': i + 1}
                for i, n in enumerate(new_name_seq)
            ]
        else:
            increment_order = []

        report.set_increment_changes(changes, moves,
                                     removed_increments=removed_increments,
                                     increment_order=increment_order)

    # ------------------------------------------------------------------
    # Pass 2 – Increment extraction by vertical position
    # ------------------------------------------------------------------

    def extract_increment_assignments(self) -> list:
        """Determine which increment lane each story belongs to by Y position.

        Completely isolated from the hierarchy (pass 1).  Only looks at
        vertical boundaries of increment lanes vs story Y positions.

        Returns:
            List of dicts ``[{'name': 'CLI', 'stories': ['Story A', ...]}, ...]``
            ordered top-to-bottom by lane Y.
        """
        # 1. Find lane backgrounds (large rectangles with empty value).
        #    Tool-generated lanes have inc-lane/ prefix; user-created lanes
        #    have simple IDs (e.g. "2").  Both are detected by their empty
        #    value, large width, and lane-like height.
        lanes = []
        _LANE_MIN_WIDTH = 200   # lanes are much wider than story cells
        _LANE_MIN_HEIGHT = 50
        for n in self._extra_nodes:
            cid = getattr(n, 'cell_id', '')
            val = getattr(n, 'value', '') or ''
            bnd = getattr(n, 'boundary', None)
            if (val == '' and bnd is not None
                    and bnd.height >= _LANE_MIN_HEIGHT
                    and bnd.width >= _LANE_MIN_WIDTH):
                if cid.startswith('inc-lane/'):
                    slug = cid.replace('inc-lane/', '')
                else:
                    slug = cid  # user-created lane, use raw id as slug
                lanes.append({
                    'slug': slug,
                    'y': n.position.y,
                    'height': bnd.height,
                    'name': '',
                    'cell_id': cid,
                })

        # 2. Match lane labels to get human-readable names.
        #    Tool-generated labels have inc-label/ prefix; user-created
        #    labels have simple IDs with a non-empty value and sit inside
        #    a lane's Y boundaries.
        for n in self._extra_nodes:
            cid = getattr(n, 'cell_id', '')
            val = getattr(n, 'value', '') or ''
            if not val:
                continue
            if cid.startswith('inc-label/'):
                slug = cid.replace('inc-label/', '')
                for lane in lanes:
                    if lane['slug'] == slug:
                        lane['name'] = val
                        break
            elif '/' not in cid and val:
                # Potential user-created label -- match by Y position
                ny = getattr(n, 'position', None)
                if ny is None:
                    continue
                for lane in lanes:
                    if (lane['name'] == ''
                            and lane['y'] <= ny.y <= lane['y'] + lane['height']):
                        lane['name'] = val
                        break

        if not lanes:
            return []

        lanes.sort(key=lambda l: l['y'])

        # Build set of cell IDs used as lane backgrounds or labels
        # so we can skip them when gathering story candidates.
        _lane_bg_ids = {lane['cell_id'] for lane in lanes}
        _lane_label_ids = set()
        for n in self._extra_nodes:
            cid = getattr(n, 'cell_id', '')
            val = getattr(n, 'value', '') or ''
            if val and any(lane['name'] == val for lane in lanes):
                _lane_label_ids.add(cid)

        # 3. Gather every element that could be a story – from the tree
        #    (DrawIOStory instances) and from extra_nodes (raw
        #    DrawIOElement lane copies with a value/name).
        candidates = []
        for story in self.get_stories():
            candidates.append((story.name, story.position.y))
        for n in self._extra_nodes:
            name = getattr(n, 'name', None) or getattr(n, 'value', None) or ''
            if name and hasattr(n, 'position') and n.position.y > 0:
                cid = getattr(n, 'cell_id', '')
                # Skip lane backgrounds and labels
                if cid in _lane_bg_ids or cid in _lane_label_ids:
                    continue
                if cid.startswith('inc-lane/') and not name:
                    continue
                if cid.startswith('inc-label/'):
                    continue
                # Skip actor elements
                if '/actor-' in cid:
                    continue
                candidates.append((name, n.position.y))

        # 4. For each lane, check every candidate.
        TOLERANCE = 20  # px slack for edges
        for lane in lanes:
            lane['stories'] = []
            lane['_seen'] = set()

        for name, y in candidates:
            for lane in lanes:
                top = lane['y'] - TOLERANCE
                bottom = lane['y'] + lane['height'] + TOLERANCE
                if top <= y <= bottom:
                    if name not in lane['_seen']:
                        lane['_seen'].add(name)
                        lane['stories'].append(name)
                    break

        return [{'name': l['name'], 'stories': l['stories']} for l in lanes]

    # ------------------------------------------------------------------
    # Dict conversion
    # ------------------------------------------------------------------

    def _to_story_graph_dict(self) -> Dict[str, Any]:
        epics = []
        for epic in self._drawio_epics:
            epic_dict = {
                'name': epic.name,
                'sequential_order': epic.sequential_order,
                'sub_epics': [self._sub_epic_to_dict(se) for se in epic.get_sub_epics()]
            }
            epics.append(epic_dict)
        return {'epics': epics}

    def _sub_epic_to_dict(self, se: DrawIOSubEpic) -> Dict[str, Any]:
        nested_sub_epics = se.get_sub_epics()
        if nested_sub_epics:
            return {
                'name': se.name,
                'sequential_order': se.sequential_order,
                'sub_epics': [self._sub_epic_to_dict(n) for n in nested_sub_epics],
                'story_groups': []
            }
        return {
            'name': se.name,
            'sequential_order': se.sequential_order,
            'sub_epics': [],
            'story_groups': [{
                'type': 'and', 'connector': None,
                'stories': [
                    {'name': s.name, 'sequential_order': s.sequential_order,
                     'story_type': s.story_type or 'user'}
                    for s in se.get_stories()
                ]
            }]
        }

    # ------------------------------------------------------------------
    # Load from DrawIO file (reverse direction)
    # ------------------------------------------------------------------

    @classmethod
    def load(cls, file_path: Path) -> 'DrawIOStoryMap':
        content = file_path.read_text(encoding='utf-8')
        nodes, parent_map = DrawIOStoryNodeSerializer.parse_nodes_from_xml(content)

        # Resolve group-relative positions: elements whose parent is a group
        # have x/y relative to the group.  Add the group's absolute position
        # so all nodes use absolute coordinates.
        cls._resolve_group_positions(nodes, parent_map)

        story_map = cls()

        nodes_by_id = {}
        for n in nodes:
            nodes_by_id[n.cell_id] = n

        epics = [n for n in nodes if isinstance(n, DrawIOEpic)]
        sub_epics = [n for n in nodes if isinstance(n, DrawIOSubEpic)]
        stories = [n for n in nodes if isinstance(n, DrawIOStory)]

        story_map._assign_by_parent_map(nodes_by_id, parent_map, epics, sub_epics, stories)
        story_map._assign_sequential_order_from_position(epics, sub_epics, stories)
        story_map._drawio_epics = epics

        classified = set()
        for e in epics:
            classified.add(id(e))
            cls._classify_sub_epic_tree(e.get_sub_epics(), classified)
        story_map._extra_nodes = [n for n in nodes if id(n) not in classified]
        return story_map

    @classmethod
    def _classify_sub_epic_tree(cls, sub_epics, classified: set):
        """Recursively walk sub-epics and their children into the classified set."""
        for se in sub_epics:
            classified.add(id(se))
            for s in se.get_stories():
                classified.add(id(s))
            cls._classify_sub_epic_tree(se.get_sub_epics(), classified)

    @staticmethod
    def _resolve_group_positions(nodes, parent_map):
        """Convert group-relative positions to absolute positions.

        DrawIO stores child positions relative to their parent group.
        This method adds the parent group's x/y offset so all nodes
        use absolute coordinates.
        """
        nodes_by_id = {n.cell_id: n for n in nodes}
        for node in nodes:
            pid = parent_map.get(node.cell_id, '')
            if pid in ('', '0', '1'):
                continue  # top-level element, position is already absolute
            parent_node = nodes_by_id.get(pid)
            if parent_node is None:
                continue
            if not hasattr(parent_node, 'position'):
                continue
            # Offset this node by its parent group's position
            abs_x = node.position.x + parent_node.position.x
            abs_y = node.position.y + parent_node.position.y
            node.set_position(abs_x, abs_y)

    # ------------------------------------------------------------------
    # Internal helpers (load direction)
    # ------------------------------------------------------------------

    def _assign_by_parent_map(self, nodes_by_id, parent_map, epics, sub_epics, stories):
        # ── Phase 1: ID-based assignment for epics and sub-epics only ──
        # Stories are intentionally excluded here because their cell IDs
        # become stale when users drag them to a new sub-epic in DrawIO
        # (DrawIO preserves the original ID, only the position changes).
        for node in list(epics) + list(sub_epics):
            cell_id = node.cell_id
            if '/' not in cell_id:
                continue
            found = False
            parts = cell_id.split('/')
            for cut in range(len(parts) - 1, 0, -1):
                candidate = '/'.join(parts[:cut])
                parent_node = nodes_by_id.get(candidate)
                if parent_node and parent_node is not node and hasattr(parent_node, 'add_child'):
                    parent_node.add_child(node)
                    found = True
                    break
            if found:
                continue
            pid = parent_map.get(cell_id, '')
            parent_from_attr = nodes_by_id.get(pid)
            if parent_from_attr and parent_from_attr is not node and hasattr(parent_from_attr, 'add_child'):
                parent_from_attr.add_child(node)
                continue

        # ── Phase 2a: Position-based sub-epic → sub-epic nesting ──
        # For orphan sub-epics without a hierarchical ID (e.g. user-added
        # cells with ids like "3"), try to find a containing *sub-epic*
        # that already has a parent.  Prefer the narrowest container so
        # "Load Bot" (x 559–1025) nests under "Initialize Bot" (x 560–1955)
        # rather than directly under the epic.
        for se in sub_epics:
            if se._parent is not None:
                continue
            se_cx = se.boundary.center.x
            best_parent_se = None
            best_width = float('inf')
            for candidate_se in sub_epics:
                if candidate_se is se or candidate_se._parent is None:
                    continue
                cl = candidate_se.boundary.x
                cr = candidate_se.boundary.x + candidate_se.boundary.width
                if cl <= se_cx <= cr and candidate_se.boundary.width < best_width:
                    best_width = candidate_se.boundary.width
                    best_parent_se = candidate_se
            if best_parent_se:
                best_parent_se.add_child(se)

        # ── Phase 2b: Position-based sub-epic → epic fallback ──
        MARGIN = 200
        for se in sub_epics:
            if se._parent is not None:
                continue
            se_cx = se.boundary.center.x
            best_epic = None
            best_dist = float('inf')
            for epic in epics:
                left = epic.boundary.x - MARGIN
                right = epic.boundary.x + epic.boundary.width + MARGIN
                if left <= se_cx <= right:
                    dist = abs(se_cx - epic.boundary.center.x)
                    if dist < best_dist:
                        best_dist = dist
                        best_epic = epic
            if best_epic:
                best_epic.add_child(se)

        # ── Phase 3: Position-based story → sub-epic assignment ──
        # Always use position for stories (never IDs) because the visual
        # position in the diagram is the source of truth after user edits.
        for story in stories:
            story_cx = story.boundary.center.x
            best_se = None
            best_width = float('inf')
            for se in sub_epics:
                if se._parent is None:
                    continue
                se_left = se.boundary.x
                se_right = se.boundary.x + se.boundary.width
                if se_left <= story_cx <= se_right:
                    if not se.get_sub_epics() and se.boundary.width < best_width:
                        best_width = se.boundary.width
                        best_se = se
            if best_se:
                best_se.add_child(story)

    def _assign_sequential_order_from_position(self, epics, sub_epics, stories):
        Y_TOLERANCE = 30  # nodes within this many px of Y are on the same row

        # Epics: left-to-right by X only, ignore Y
        for idx, node in enumerate(sorted(epics, key=lambda n: n.position.x)):
            node.sequential_order = float(idx + 1)

        # Sub-epics and stories: order within parent, Y tolerance then X
        for group in [sub_epics, stories]:
            by_parent = {}
            for n in group:
                pid = id(n._parent) if n._parent else 0
                by_parent.setdefault(pid, []).append(n)
            for siblings in by_parent.values():
                sorted_nodes = sorted(siblings,
                    key=lambda n: (round(n.position.y / Y_TOLERANCE), n.position.x))
                for idx, node in enumerate(sorted_nodes):
                    node.sequential_order = float(idx + 1)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _collect_all_nodes(self) -> list:
        """Walk the tree and gather every renderable node.

        Serialization order determines visual stacking in DrawIO (later =
        on top).  For increments view we want:
          1. Lane backgrounds (large rectangles) – bottom layer
          2. Epics / sub-epics bars – structural outlines
          3. Lane labels, actors, story copies inside lanes
          4. Orphaned stories in the outline – top layer so the user can
             drag them onto a lane without them being hidden behind it.
        """
        # Separate lane backgrounds from other extra nodes
        lane_bgs = [n for n in self._extra_nodes
                    if hasattr(n, 'cell_id')
                    and n.cell_id.startswith('inc-lane/')
                    and '/' not in n.cell_id.replace('inc-lane/', '', 1)
                    and getattr(n, 'value', '') == '']
        other_extra = [n for n in self._extra_nodes if n not in lane_bgs]

        nodes = []
        nodes.extend(lane_bgs)            # 1. lane backgrounds (bottom)
        for epic in self._drawio_epics:
            nodes.extend(epic.collect_all_nodes())  # 2+4. structure + orphans
        nodes.extend(other_extra)          # 3. labels, actors, lane stories
        return nodes

    def _collect_domain_stories(self, story_map: StoryMap,
                                 scope: Optional[str] = None) -> dict:
        """Build name→Story lookup, optionally filtered by scope (increment name)."""
        result: Dict[str, Story] = {}
        scope_names = None
        if scope:
            for inc in story_map.story_graph.get('increments', []):
                if inc.get('name') == scope:
                    scope_names = set()
                    for s in inc.get('stories', []):
                        scope_names.add(s.get('name', '') if isinstance(s, dict) else str(s))
                    break

        for epic in story_map.epics:
            for sub_epic in epic.sub_epics:
                self._gather_stories(sub_epic, result, scope_names)
        return result

    def _gather_stories(self, sub_epic, result: dict, scope_names):
        for child in sub_epic.children:
            if isinstance(child, Story):
                if scope_names is None or child.name in scope_names:
                    result[child.name] = child
            elif isinstance(child, SubEpic):
                self._gather_stories(child, result, scope_names)
            elif isinstance(child, StoryGroup):
                for story in child.children:
                    if isinstance(story, Story):
                        if scope_names is None or story.name in scope_names:
                            result[story.name] = story
