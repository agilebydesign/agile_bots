"""
Write steps for the 20 remaining domain-unique scenarios.
These have no cross-domain pattern -- each is specific to its domain's mechanics.
"""
import json, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
STORY_GRAPH_PATH = Path(__file__).parent.parent / 'docs' / 'story' / 'story-graph.json'

# test_method -> steps (handwritten for each unique scenario)
UNIQUE_STEPS = {
    # === Epics/Render: nesting depth scenarios ===
    'test_render_4_level_nested_sub_epics_recurses_to_all_depths':
        'Given {StoryMap} has {DrawIOSubEpic} nested 4 levels deep\n'
        'When {DrawIOStoryMap} renders outline from {StoryMap}\n'
        'Then {DrawIOStoryMap} contains {DrawIOSubEpic} at all 4 depth levels\n'
        'And each nested {DrawIOSubEpic} is rendered inside its parent',

    'test_parent_and_leaf_sub_epics_both_rendered':
        'Given {StoryMap} has {DrawIOSubEpic} that contain nested {DrawIOSubEpic} children and leaf {DrawIOSubEpic} that contain {DrawIOStory}\n'
        'When {DrawIOStoryMap} renders outline from {StoryMap}\n'
        'Then both parent {DrawIOSubEpic} containers and leaf {DrawIOSubEpic} with stories are rendered',

    'test_4_level_depth_produces_3_distinct_sub_epic_y_levels':
        'Given {StoryMap} has {DrawIOSubEpic} nested to depth 4\n'
        'When {DrawIOStoryMap} renders outline from {StoryMap}\n'
        'Then {DrawIOSubEpic} Y positions increase at each depth level\n'
        'And 4-level depth produces 3 distinct {DrawIOSubEpic} Y positions',

    'test_flat_graph_sub_epic_at_standard_y':
        'Given {StoryMap} has a single {DrawIOSubEpic} with no nesting\n'
        'When {DrawIOStoryMap} renders outline from {StoryMap}\n'
        'Then {DrawIOSubEpic} is positioned at the standard Y below {DrawIOEpic}',

    'test_nested_containers_horizontal_span_at_every_depth':
        'Given {StoryMap} has {DrawIOSubEpic} nested 3 levels deep\n'
        'When {DrawIOStoryMap} renders outline from {StoryMap}\n'
        'Then every parent {DrawIOSubEpic} horizontal span covers all its children at every depth level',

    # === Epics/Report: cell ID format scenarios ===
    'test_mixed_user_and_tool_ids_only_tool_ids_participate_in_rename':
        'Given {DrawIOStoryMap} has unmatched {DrawIOSubEpic} with both simple cell IDs and hierarchical cell IDs\n'
        'When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs\n'
        'Then only {DrawIOSubEpic} with hierarchical cell IDs participate in rename pairing\n'
        'And {DrawIOSubEpic} with simple cell IDs are treated as new',

    'test_all_simple_id_sub_epics_become_new_when_no_hierarchical_candidates':
        'Given {DrawIOStoryMap} has unmatched {DrawIOSubEpic} all with simple cell IDs\n'
        'When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs\n'
        'Then no {DrawIOSubEpic} participate in rename pairing\n'
        'And all unmatched {DrawIOSubEpic} are treated as new',

    'test_story_rename_still_works_regardless_of_cell_id_format':
        'Given {DrawIOStoryMap} has renamed {DrawIOStory} with any cell ID format\n'
        'When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs\n'
        'Then {DrawIOStory} rename is detected regardless of cell ID format\n'
        'And cell ID type filtering only applies to {DrawIOSubEpic} and {DrawIOEpic}',

    # === Stories/Report: cross-epic and removed sub-epic moves ===
    'test_story_moved_across_epics_detected_as_move':
        'Given {DrawIOStory} has been moved from {DrawIOSubEpic} under one {DrawIOEpic} to {DrawIOSubEpic} under a different {DrawIOEpic}\n'
        'When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs\n'
        'Then {UpdateReport} detects the cross-epic {DrawIOStory} as moved not new plus removed',

    'test_stories_from_removed_sub_epic_detected_as_moves':
        'Given {DrawIOSubEpic} has been removed from {DrawIOStoryMap}\n'
        'And its {DrawIOStory} now appear under the parent {DrawIOEpic} or another {DrawIOSubEpic}\n'
        'When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs\n'
        'Then {UpdateReport} detects the promoted {DrawIOStory} as moves from the removed {DrawIOSubEpic}',

    # === Stories/Update: cross-epic move preserves data ===
    'test_cross_epic_move_preserves_story_data':
        'Given {UpdateReport} contains a {DrawIOStory} move across {DrawIOEpic} boundaries\n'
        'When move is applied to story graph\n'
        'Then {DrawIOStory} acceptance_criteria and scenarios are preserved after cross-epic move',

    # === AC/Update: story split ===
    'test_story_split_ac_distributed_correctly':
        'Given {DrawIOStory} has been split in diagram with some AC {DrawIOElement} moved to a new {DrawIOStory}\n'
        'When {UpdateReport} is applied to story graph\n'
        'Then AC is distributed correctly between original and new {DrawIOStory}\n'
        'And no AC is lost in the split',

    # === Increments/Report: geometry and edge cases ===
    'test_user_created_lane_detected_by_geometry':
        'Given {DrawIOStoryMap} has a user-created lane with simple cell ID and large rectangle geometry\n'
        'When {DrawIOStoryMap} extracts increments from diagram\n'
        'Then the user-created lane is detected as a new increment by its geometry',

    'test_moving_orphan_into_lane_reports_as_added':
        'Given {DrawIOStory} was previously unassigned (orphan) in increments diagram\n'
        'And user drags {DrawIOStory} into an increment lane\n'
        'When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs\n'
        'Then {UpdateReport} reports {DrawIOStory} as added to that increment',

    'test_no_false_new_stories_with_duplicates_across_lanes':
        'Given {DrawIOStory} appears in multiple increment lanes in {DrawIOStoryMap}\n'
        'When {DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs\n'
        'Then {UpdateReport} does not produce false duplicate or new story entries',

    # === Increments/Update: edge cases ===
    'test_apply_increment_move_transfers_story_between_increments':
        'Given {UpdateReport} contains a {DrawIOStory} move from one increment to another\n'
        'When move is applied to story graph\n'
        'Then {DrawIOStory} is removed from source increment and added to target increment\n'
        'And all {DrawIOStory} fields are preserved',

    'test_apply_remove_increment_deletes_entire_increment_from_story_graph':
        'Given {UpdateReport} contains a removed increment\n'
        'When removal is applied to story graph\n'
        'Then the entire increment and its story assignments are deleted from story graph',

    'test_apply_remove_increment_returns_false_for_nonexistent':
        'Given {UpdateReport} references an increment that does not exist in story graph\n'
        'When removal is applied to story graph\n'
        'Then removal returns false and story graph is unchanged',

    'test_apply_increment_order_updates_priorities':
        'Given {DrawIOStoryMap} has increment lanes in a new order different from story graph\n'
        'When {UpdateReport} is applied to story graph\n'
        'Then increment priorities in story graph are updated to match diagram order',

    'test_apply_increment_order_no_change_when_already_correct':
        'Given increment priorities in story graph already match {DrawIOStoryMap} diagram order\n'
        'When {UpdateReport} is applied to story graph\n'
        'Then no priority changes are made to story graph',
}


def main():
    g = json.loads(STORY_GRAPH_PATH.read_text(encoding='utf-8'))

    filled = 0
    still_empty = 0

    for e in g['epics']:
        for se in e.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == 'Synchronize Diagram by Domain':
                        for se3 in se2.get('sub_epics', []):
                            for sg in se3.get('story_groups', []):
                                for st in sg.get('stories', []):
                                    for sc in st.get('scenarios', []):
                                        steps = sc.get('steps', '')
                                        if steps and steps.strip():
                                            continue
                                        tm = sc.get('test_method')
                                        if tm and tm in UNIQUE_STEPS:
                                            sc['steps'] = UNIQUE_STEPS[tm]
                                            filled += 1
                                            print(f'  [WROTE] {sc["name"][:60]}')
                                        else:
                                            still_empty += 1
                                            print(f'  [EMPTY] {sc["name"][:60]} (test={tm})')

    print(f'\n--- Filled {filled} unique scenarios, {still_empty} still empty ---')

    STORY_GRAPH_PATH.write_text(json.dumps(g, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Wrote to {STORY_GRAPH_PATH}')


if __name__ == '__main__':
    main()
