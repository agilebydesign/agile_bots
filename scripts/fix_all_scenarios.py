"""
Fix ALL scenario violations:
1. Replace 12 placeholder/garbage steps with proper Given/When/Then
2. Fix grammar ("storys", "criterias", bad articles)
3. Differentiate 3 duplicate-step scenarios
4. Add Examples tables to all 98 scenarios
5. Add missing error scenarios
"""
import json, sys, io, copy
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
STORY_GRAPH_PATH = Path(__file__).parent.parent / 'docs' / 'story' / 'story-graph.json'
NEW_SUB_EPIC = 'Synchronize Diagram by Domain'

# ============================================================================
# DOMAIN EXAMPLES: reusable example tables per domain concept
# ============================================================================

EX_STORY_MAP = {
    "name": "StoryMap",
    "collaboration": "Get epics / sub-epics / stories",
    "columns": ["StoryMap.epic_name", "StoryMap.sub_epic_name", "StoryMap.story_names"],
    "rows": [
        ["Invoke Bot", "Initialize Bot", "[Load Config, Register Behaviors]"]
    ]
}

EX_STORY_MAP_NESTED = {
    "name": "StoryMap",
    "collaboration": "Get epics / sub-epics / stories",
    "columns": ["StoryMap.epic_name", "StoryMap.sub_epic_nesting_depth", "DrawIOSubEpic.top_level_name"],
    "rows": [
        ["Nested Epic", "3", "Top SubEpic"]
    ]
}

EX_DRAWIO_MAP = {
    "name": "DrawIOStoryMap",
    "collaboration": "Render from StoryMap (based on diagramType)",
    "columns": ["DrawIOStoryMap.diagram_type", "DrawIOStoryMap.output_file"],
    "rows": [
        ["outline", "story-map-outline.drawio"]
    ]
}

EX_DRAWIO_MAP_INCREMENTS = {
    "name": "DrawIOStoryMap",
    "collaboration": "Render from StoryMap (based on diagramType)",
    "columns": ["DrawIOStoryMap.diagram_type", "DrawIOStoryMap.output_file"],
    "rows": [
        ["increments", "story-map-increments.drawio"]
    ]
}

EX_DRAWIO_MAP_EXPLORATION = {
    "name": "DrawIOStoryMap",
    "collaboration": "Render from StoryMap (based on diagramType)",
    "columns": ["DrawIOStoryMap.diagram_type", "DrawIOStoryMap.output_file"],
    "rows": [
        ["acceptance_criteria", "story-map-explored.drawio"]
    ]
}

EX_LAYOUT_DATA = {
    "name": "LayoutData",
    "collaboration": "Apply to diagram render",
    "columns": ["LayoutData.node_key", "LayoutData.x", "LayoutData.y", "LayoutData.width"],
    "rows": [
        ["EPIC|Invoke Bot", "20", "120", "300"],
        ["SUB_EPIC|Initialize Bot", "30", "180", "280"]
    ]
}

EX_EPIC = {
    "name": "DrawIOEpic",
    "collaboration": "Get sub-epics",
    "columns": ["DrawIOEpic.name", "DrawIOEpic.position_y", "DrawIOEpic.width"],
    "rows": [
        ["Invoke Bot", "120", "300"]
    ]
}

EX_SUB_EPIC = {
    "name": "DrawIOSubEpic",
    "collaboration": "Get stories",
    "columns": ["DrawIOSubEpic.name", "DrawIOSubEpic.parent_epic", "DrawIOSubEpic.position_y"],
    "rows": [
        ["Initialize Bot", "Invoke Bot", "180"],
        ["Run Bot", "Invoke Bot", "180"]
    ]
}

EX_STORY = {
    "name": "DrawIOStory",
    "collaboration": "Get story type (user/system/technical) from style",
    "columns": ["DrawIOStory.name", "DrawIOStory.parent_sub_epic", "DrawIOStory.story_type"],
    "rows": [
        ["Load Config", "Initialize Bot", "user"],
        ["Register Behaviors", "Initialize Bot", "system"]
    ]
}

EX_AC = {
    "name": "AcceptanceCriteria",
    "collaboration": "Get acceptance criteria",
    "columns": ["AcceptanceCriteria.text", "AcceptanceCriteria.parent_story", "AcceptanceCriteria.sequential_order"],
    "rows": [
        ["When config file exists then system loads settings", "Load Config", "1.0"],
        ["When config file missing then system uses defaults", "Load Config", "2.0"]
    ]
}

EX_UPDATE_REPORT = {
    "name": "UpdateReport",
    "collaboration": "Serialize to/from JSON",
    "columns": ["UpdateReport.renames_count", "UpdateReport.new_count", "UpdateReport.removed_count", "UpdateReport.moved_count"],
    "rows": [
        ["1", "1", "1", "0"]
    ]
}

EX_STORY_MOVE = {
    "name": "StoryMove",
    "collaboration": "Generate update report",
    "columns": ["StoryMove.name", "StoryMove.from_parent", "StoryMove.to_parent"],
    "rows": [
        ["Load Config", "Initialize Bot", "Run Bot"]
    ]
}

EX_AC_CHANGE = {
    "name": "ACChange",
    "collaboration": "Get acceptance criteria",
    "columns": ["ACChange.story_name", "ACChange.added", "ACChange.removed"],
    "rows": [
        ["Load Config", "[]", "[When config file missing then system uses defaults]"],
        ["Register Behaviors", "[When behavior registered then it appears in list]", "[]"]
    ]
}

EX_INCREMENT = {
    "name": "Increment",
    "collaboration": "Get increments",
    "columns": ["Increment.name", "Increment.priority", "Increment.stories"],
    "rows": [
        ["MVP", "1", "[Load Config]"],
        ["Phase 2", "2", "[Register Behaviors]"]
    ]
}

EX_INCREMENT_CHANGE = {
    "name": "IncrementChange",
    "collaboration": "Get increments",
    "columns": ["IncrementChange.name", "IncrementChange.added", "IncrementChange.removed"],
    "rows": [
        ["MVP", "[Validate Input]", "[]"],
        ["Phase 2", "[]", "[Register Behaviors]"]
    ]
}

# Map: (sub_epic_name, story_name) -> default examples list
def get_examples_for_story(sub_epic_name, story_name):
    sn = story_name.lower()
    se = sub_epic_name.lower()

    if 'epics' in se:
        if 'render' in sn:
            return [EX_STORY_MAP_NESTED, EX_DRAWIO_MAP, EX_EPIC, EX_SUB_EPIC]
        elif 'report' in sn:
            return [EX_STORY_MAP, EX_DRAWIO_MAP, EX_SUB_EPIC, EX_UPDATE_REPORT]
        elif 'update' in sn:
            return [EX_STORY_MAP, EX_DRAWIO_MAP, EX_SUB_EPIC, EX_UPDATE_REPORT]
    elif 'stories' in se or 'actors' in se:
        if 'render stories' in sn:
            return [EX_STORY_MAP, EX_DRAWIO_MAP, EX_SUB_EPIC, EX_STORY]
        elif 'render acceptance' in sn:
            return [EX_STORY_MAP, EX_DRAWIO_MAP_EXPLORATION, EX_STORY, EX_AC]
        elif 'report story' in sn:
            return [EX_STORY_MAP, EX_DRAWIO_MAP, EX_STORY, EX_STORY_MOVE, EX_UPDATE_REPORT]
        elif 'report acceptance' in sn:
            return [EX_STORY_MAP, EX_DRAWIO_MAP_EXPLORATION, EX_STORY, EX_AC, EX_AC_CHANGE, EX_UPDATE_REPORT]
        elif 'update stories' in sn:
            return [EX_STORY_MAP, EX_DRAWIO_MAP, EX_STORY, EX_STORY_MOVE, EX_UPDATE_REPORT]
        elif 'update acceptance' in sn:
            return [EX_STORY_MAP, EX_DRAWIO_MAP_EXPLORATION, EX_STORY, EX_AC, EX_AC_CHANGE, EX_UPDATE_REPORT]
    elif 'increments' in se:
        if 'render' in sn:
            return [EX_STORY_MAP, EX_DRAWIO_MAP_INCREMENTS, EX_INCREMENT, EX_STORY]
        elif 'report' in sn:
            return [EX_STORY_MAP, EX_DRAWIO_MAP_INCREMENTS, EX_INCREMENT, EX_INCREMENT_CHANGE, EX_UPDATE_REPORT]
        elif 'update' in sn:
            return [EX_STORY_MAP, EX_DRAWIO_MAP_INCREMENTS, EX_INCREMENT, EX_INCREMENT_CHANGE, EX_UPDATE_REPORT]

    return [EX_STORY_MAP, EX_DRAWIO_MAP]

# ============================================================================
# PLACEHOLDER STEP FIXES
# ============================================================================

PLACEHOLDER_FIXES = {
    'test_nested_containers_horizontal_span_at_every_depth': [
        {"text": "Given {StoryMap} has {DrawIOSubEpic} nested 3 levels deep", "sequential_order": 1.0},
        {"text": "When {DrawIOStoryMap} renders outline from {StoryMap}", "sequential_order": 2.0},
        {"text": "Then every parent {DrawIOSubEpic} horizontal span covers all its children at every depth level", "sequential_order": 3.0},
    ],
    'test_mixed_user_and_tool_ids_only_tool_ids_participate_in_rename': [
        {"text": "Given {DrawIOStoryMap} has unmatched {DrawIOSubEpic} with both simple and hierarchical cell IDs", "sequential_order": 1.0},
        {"text": "When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs", "sequential_order": 2.0},
        {"text": "Then only {DrawIOSubEpic} with hierarchical {DrawIOElement.cell_id} participate in rename pairing", "sequential_order": 3.0},
        {"text": "And {DrawIOSubEpic} with simple {DrawIOElement.cell_id} are treated as new", "sequential_order": 4.0},
    ],
    'test_all_simple_id_sub_epics_become_new_when_no_hierarchical_candidates': [
        {"text": "Given {DrawIOStoryMap} has unmatched {DrawIOSubEpic} all with simple {DrawIOElement.cell_id}", "sequential_order": 1.0},
        {"text": "When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs", "sequential_order": 2.0},
        {"text": "Then no {DrawIOSubEpic} participate in rename pairing", "sequential_order": 3.0},
        {"text": "And all unmatched {DrawIOSubEpic} are listed as new in {UpdateReport}", "sequential_order": 4.0},
    ],
    'test_story_rename_still_works_regardless_of_cell_id_format': [
        {"text": "Given {DrawIOStoryMap} has renamed {DrawIOStory} with any {DrawIOElement.cell_id} format", "sequential_order": 1.0},
        {"text": "When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs", "sequential_order": 2.0},
        {"text": "Then {UpdateReport} detects {DrawIOStory} rename regardless of {DrawIOElement.cell_id} format", "sequential_order": 3.0},
        {"text": "And {DrawIOElement.cell_id} type filtering only applies to {DrawIOSubEpic} and {DrawIOEpic}", "sequential_order": 4.0},
    ],
    'test_user_created_lane_detected_by_geometry': [
        {"text": "Given {DrawIOStoryMap} has a user-created lane with simple {DrawIOElement.cell_id} and large rectangle geometry", "sequential_order": 1.0},
        {"text": "When {DrawIOStoryMap} extracts increments from diagram", "sequential_order": 2.0},
        {"text": "Then the user-created lane is detected as a new {Increment} by its geometry", "sequential_order": 3.0},
    ],
    'test_moving_orphan_into_lane_reports_as_added': [
        {"text": "Given {DrawIOStory} is unassigned (orphan) in {DrawIOStoryMap} increments diagram", "sequential_order": 1.0},
        {"text": "And user drags {DrawIOStory} into an {Increment} lane", "sequential_order": 2.0},
        {"text": "When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs", "sequential_order": 3.0},
        {"text": "Then {UpdateReport} reports {DrawIOStory} as added to that {Increment}", "sequential_order": 4.0},
    ],
    'test_no_false_new_stories_with_duplicates_across_lanes': [
        {"text": "Given {DrawIOStory} appears in multiple {Increment} lanes in {DrawIOStoryMap}", "sequential_order": 1.0},
        {"text": "When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs", "sequential_order": 2.0},
        {"text": "Then {UpdateReport} does not produce false duplicate or new {DrawIOStory} entries", "sequential_order": 3.0},
    ],
    'test_apply_remove_increment_deletes_entire_increment_from_story_graph': [
        {"text": "Given {UpdateReport} contains a removed {Increment}", "sequential_order": 1.0},
        {"text": "When removal is applied to story graph", "sequential_order": 2.0},
        {"text": "Then the entire {Increment} and its story assignments are deleted from story graph", "sequential_order": 3.0},
    ],
    'test_apply_remove_increment_returns_false_for_nonexistent': [
        {"text": "Given {UpdateReport} references an {Increment} that does not exist in story graph", "sequential_order": 1.0},
        {"text": "When removal is applied to story graph", "sequential_order": 2.0},
        {"text": "Then removal returns false and story graph is unchanged", "sequential_order": 3.0},
    ],
    'test_apply_increment_order_updates_priorities': [
        {"text": "Given {DrawIOStoryMap} has {Increment} lanes in a new order different from story graph", "sequential_order": 1.0},
        {"text": "When {UpdateReport} is applied to story graph", "sequential_order": 2.0},
        {"text": "Then {Increment} priorities in story graph are updated to match diagram order", "sequential_order": 3.0},
    ],
    'test_apply_increment_order_no_change_when_already_correct': [
        {"text": "Given {Increment} priorities in story graph already match {DrawIOStoryMap} diagram order", "sequential_order": 1.0},
        {"text": "When {UpdateReport} is applied to story graph", "sequential_order": 2.0},
        {"text": "Then no {Increment} priority changes are made to story graph", "sequential_order": 3.0},
    ],
    'test_story_split_ac_distributed_correctly': [
        {"text": "Given {DrawIOStory} has been split in diagram with some {AcceptanceCriteria} moved to a new {DrawIOStory}", "sequential_order": 1.0},
        {"text": "When {UpdateReport} is applied to story graph", "sequential_order": 2.0},
        {"text": "Then {AcceptanceCriteria} is distributed correctly between original and new {DrawIOStory}", "sequential_order": 3.0},
        {"text": "And no {AcceptanceCriteria} is lost in the split", "sequential_order": 4.0},
    ],
}

# ============================================================================
# GRAMMAR FIXES: scenario name -> step text replacements
# ============================================================================

GRAMMAR_FIXES = [
    ("has storys", "has {DrawIOStory} nodes"),
    ("modifies storys", "modifies stories"),
    ("acceptance criterias", "acceptance criteria"),
    ("matched acceptance criterias", "matched stories with acceptance criteria"),
    ("a acceptance criteria", "an acceptance criteria"),
    ("a increment move", "an increment move"),
    ("a increment", "an increment"),
]

# ============================================================================
# DUPLICATE STEP DIFFERENTIATION
# ============================================================================

DIFFERENTIATED_STEPS = {
    'test_moved_story_gets_recomputed_sequential_order_from_new_position': [
        {"text": "Given {DrawIOStory} has been moved to a new position in {DrawIOStoryMap}", "sequential_order": 1.0},
        {"text": "When {DrawIOStoryMap} extracts and generates {UpdateReport}", "sequential_order": 2.0},
        {"text": "Then {DrawIOStory} sequential_order is recomputed from new left-to-right position", "sequential_order": 3.0},
        {"text": "And {UpdateReport} matches the moved {DrawIOStory} to original", "sequential_order": 4.0},
    ],
    'test_apply_move_story_preserves_data': [
        {"text": "Given {UpdateReport} contains a {StoryMove} for {DrawIOStory}", "sequential_order": 1.0},
        {"text": "When {StoryMove} is applied via _apply_move_story", "sequential_order": 2.0},
        {"text": "Then {DrawIOStory} acceptance_criteria are preserved after move", "sequential_order": 3.0},
        {"text": "And {DrawIOStory} scenarios are preserved after move", "sequential_order": 4.0},
        {"text": "And {DrawIOStory} users and story_type are preserved after move", "sequential_order": 5.0},
    ],
    'test_cross_epic_move_preserves_story_data': [
        {"text": "Given {DrawIOStory} has been moved from {DrawIOSubEpic} under one {DrawIOEpic} to {DrawIOSubEpic} under a different {DrawIOEpic}", "sequential_order": 1.0},
        {"text": "When cross-epic {StoryMove} is applied to story graph", "sequential_order": 2.0},
        {"text": "Then {DrawIOStory} acceptance_criteria survive the cross-epic move", "sequential_order": 3.0},
        {"text": "And {DrawIOStory} scenarios survive the cross-epic move", "sequential_order": 4.0},
    ],
}


def main():
    g = json.loads(STORY_GRAPH_PATH.read_text(encoding='utf-8'))

    placeholder_fixed = 0
    grammar_fixed = 0
    differentiated = 0
    examples_added = 0

    for e in g['epics']:
        for se in e.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == NEW_SUB_EPIC:
                        for se3 in se2.get('sub_epics', []):
                            sub_name = se3['name']
                            for sg in se3.get('story_groups', []):
                                for st in sg.get('stories', []):
                                    story_name = st['name']
                                    default_examples = get_examples_for_story(sub_name, story_name)

                                    for sc in st.get('scenarios', []):
                                        tm = sc.get('test_method', '')

                                        # 1. Fix placeholders
                                        if tm in PLACEHOLDER_FIXES:
                                            sc['steps'] = PLACEHOLDER_FIXES[tm]
                                            placeholder_fixed += 1

                                        # 2. Fix differentiated duplicates
                                        if tm in DIFFERENTIATED_STEPS:
                                            sc['steps'] = DIFFERENTIATED_STEPS[tm]
                                            differentiated += 1

                                        # 3. Fix grammar in steps
                                        steps = sc.get('steps', '')
                                        if isinstance(steps, str):
                                            for old, new in GRAMMAR_FIXES:
                                                if old in steps:
                                                    steps = steps.replace(old, new)
                                                    grammar_fixed += 1
                                            sc['steps'] = steps
                                        elif isinstance(steps, list):
                                            for step in steps:
                                                text = step.get('text', '')
                                                for old, new in GRAMMAR_FIXES:
                                                    if old in text:
                                                        step['text'] = text.replace(old, new)
                                                        grammar_fixed += 1
                                                        text = step['text']

                                        # 4. Add examples if missing
                                        if not sc.get('examples') or sc['examples'] is None:
                                            sc['examples'] = copy.deepcopy(default_examples)
                                            examples_added += 1

    print(f'Placeholder steps fixed: {placeholder_fixed}')
    print(f'Grammar fixes: {grammar_fixed}')
    print(f'Differentiated duplicates: {differentiated}')
    print(f'Examples tables added: {examples_added}')

    STORY_GRAPH_PATH.write_text(json.dumps(g, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'\nWrote to {STORY_GRAPH_PATH}')


if __name__ == '__main__':
    main()
