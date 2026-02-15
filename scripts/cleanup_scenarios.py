"""
Apply all scenario cleanup: kills, moves, renames, mismapping fixes.
Based on manual review of all 107 scenarios.
"""
import json, sys, io, copy
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
STORY_GRAPH_PATH = Path(__file__).parent.parent / 'docs' / 'story' / 'story-graph.json'
NEW_SUB_EPIC = 'Synchronize Diagram by Domain'


def load_stories(graph_data):
    """Return {story_name: story_dict} for new sub-epic."""
    result = {}
    for e in graph_data.get('epics', []):
        for se in e.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == NEW_SUB_EPIC:
                        for se3 in se2.get('sub_epics', []):
                            for sg in se3.get('story_groups', []):
                                for st in sg.get('stories', []):
                                    result[st['name']] = st
    return result


def kill(story, test_method, reason):
    """Remove scenario by test_method."""
    before = len(story.get('scenarios', []))
    story['scenarios'] = [s for s in story['scenarios'] if s.get('test_method') != test_method]
    if len(story['scenarios']) < before:
        print(f'  KILL: {test_method} -- {reason}')
        return True
    return False


def kill_by_name(story, name_fragment, reason):
    """Remove scenario by name substring."""
    before = len(story.get('scenarios', []))
    story['scenarios'] = [s for s in story['scenarios'] if name_fragment not in s.get('name', '')]
    if len(story['scenarios']) < before:
        print(f'  KILL: "{name_fragment}..." -- {reason}')
        return True
    return False


def move(from_story, to_story, test_method, new_name=None):
    """Move scenario from one story to another."""
    sc = None
    for s in from_story.get('scenarios', []):
        if s.get('test_method') == test_method:
            sc = copy.deepcopy(s)
            break
    if not sc:
        return False
    from_story['scenarios'] = [s for s in from_story['scenarios'] if s.get('test_method') != test_method]
    if new_name:
        sc['name'] = new_name
    # Check not already in target
    existing = {s.get('test_method') for s in to_story.get('scenarios', [])}
    if test_method not in existing:
        sc['sequential_order'] = float(len(to_story['scenarios']) + 1)
        to_story['scenarios'].append(sc)
    print(f'  MOVE: {test_method} -> {to_story["name"][:40]}')
    return True


def rename(story, test_method, new_name):
    """Rename scenario by test_method."""
    for sc in story.get('scenarios', []):
        if sc.get('test_method') == test_method:
            old = sc['name']
            if old != new_name:
                sc['name'] = new_name
                print(f'  RENAME: {test_method}')
                return True
    return False


def rename_by_old_name(story, old_fragment, new_name):
    """Rename scenario by old name fragment."""
    for sc in story.get('scenarios', []):
        if old_fragment in sc.get('name', '') and sc['name'] != new_name:
            sc['name'] = new_name
            print(f'  RENAME: "{old_fragment}..." -> "{new_name[:50]}..."')
            return True
    return False


def renumber(story):
    """Renumber all scenarios sequentially."""
    for i, sc in enumerate(story.get('scenarios', []), 1):
        sc['sequential_order'] = float(i)


def main():
    g = json.loads(STORY_GRAPH_PATH.read_text(encoding='utf-8'))
    stories = load_stories(g)

    re = stories['Render epic and sub-epic hierarchy']
    rp_e = stories['Report epic and sub-epic changes']
    ue = stories['Update epics and sub-epics from diagram']
    rs = stories['Render stories and actors']
    rp_sm = stories['Report story moves between parents']
    rp_ac = stories['Report acceptance criteria changes']
    us = stories['Update stories and acceptance criteria from diagram']
    ri = stories['Render increment lanes']
    rp_i = stories['Report increment changes']
    ui = stories['Update increments from diagram']

    # =========================================================================
    # EPICS: RENDER (13 -> 9)
    # =========================================================================
    print('\n=== Render epic and sub-epic hierarchy ===')

    # KILL duplicates of Y positioning (keep #8 as parametric version)
    kill(re, 'test_nested_sub_epics_have_increasing_y_positions_per_depth',
         'duplicate of 4_level_depth Y test')
    kill(re, 'test_nested_sub_epics_at_different_y_levels',
         'duplicate of 4_level_depth Y test')

    # KILL #4 parent width - duplicate of #10 epic span
    kill(re, 'test_parent_sub_epic_width_encompasses_all_nested_children',
         'duplicate of epic_horizontal_span')

    # FIX mismapping: test_sub_epic_horizontal_span_covers_all_stories belongs in Stories/Render
    # It's here with wrong name "All epic and sub-epic cells have required styles"
    # Remove from Epics (it's already in Stories as #8)
    kill(re, 'test_sub_epic_horizontal_span_covers_all_stories',
         'mismapped -- belongs in Stories/Render (already there)')

    # RENAMES
    rename(re, 'test_render_4_level_nested_sub_epics_recurses_to_all_depths',
           'Nested sub-epics render recursively to 4 levels of depth')
    rename(re, 'test_4_level_depth_produces_3_distinct_sub_epic_y_levels',
           'Nested sub-epic Y positions increase with each depth level')
    rename(re, 'test_render_and_save_nested_sub_epics_produces_valid_drawio',
           'Render completes and writes valid DrawIO file for epic hierarchy')
    rename(re, 'test_parent_and_leaf_sub_epics_both_rendered',
           'Both parent and leaf sub-epics rendered in hierarchy')
    rename(re, 'test_flat_graph_sub_epic_at_standard_y',
           'Single-level sub-epic renders at standard Y position')
    rename(re, 'test_nested_containers_horizontal_span_at_every_depth',
           'Nested container spans children at every depth level')

    # =========================================================================
    # EPICS: REPORT (7 -> 9, gaining 2 from Update)
    # =========================================================================
    print('\n=== Report epic and sub-epic changes ===')

    # RENAMES
    rename_by_old_name(rp_e, 'When multiple unmatched',
                       'Only hierarchical cell ID sub-epics participate in rename pairing')
    rename_by_old_name(rp_e, 'If ALL unmatched',
                       'All simple cell ID sub-epics treated as new when no hierarchical candidates')
    rename_by_old_name(rp_e, 'cell-ID check only',
                       'Story rename works regardless of cell ID format')

    # MOVE from Update: report-generation scenarios don't belong in Update
    move(ue, rp_e, 'test_update_report_lists_exact_fuzzy_new_and_removed_stories',
         'Report lists exact fuzzy new and removed entities for epics')
    move(ue, rp_e, 'test_deleted_nodes_listed_as_removed_and_large_deletions_flagged',
         'Removed epics and sub-epics flagged as large deletions in report')

    # =========================================================================
    # EPICS: UPDATE (11 -> 8, losing 2 to Report)
    # =========================================================================
    print('\n=== Update epics and sub-epics from diagram ===')

    # RENAMES
    rename(ue, 'test_extract_outline_assigns_stories_to_sub_epics_by_containment_and_sequential_order',
           'Extract assigns entities to parent sub-epics by containment and sequential order')
    rename(ue, 'test_deleted_sub_epic_reassigns_its_stories_by_position',
           'Removed sub-epic reassigns its stories by position')
    rename(ue, 'test_deleted_epic_removes_all_children_and_flags_large_deletions',
           'Removed epic removes all children from story graph')

    # =========================================================================
    # STORIES: RENDER (8 -> 8, clean)
    # =========================================================================
    print('\n=== Render stories and actors ===')

    rename(rs, 'test_render_exploration_diagram_with_ac_boxes_below_stories',
           'Render acceptance criteria boxes below stories in exploration diagram')
    rename(rs, 'test_ac_boxes_styled_and_positioned_below_story_with_extracted_step_text',
           'AC boxes styled with correct fill stroke and positioned below story')
    rename(rs, 'test_exploration_render_output_contains_story_and_ac_cells_with_correct_containment',
           'Rendered output contains story and AC cells with correct containment')

    # =========================================================================
    # STORIES: REPORT MOVES (8 -> 5, losing 3 to Update)
    # =========================================================================
    print('\n=== Report story moves between parents ===')

    rename_by_old_name(rp_sm, 'sub-epic is removed and its stories',
                       'Stories from removed sub-epic detected as moves to parent')
    rename(rp_sm, 'test_story_moved_across_epics_detected_as_move',
           'Story moved across epics detected as move not new plus removed')

    # MOVE apply/e2e scenarios to Update
    move(rp_sm, us, 'test_apply_move_story_preserves_data',
         'Apply story move preserves all story fields')
    move(rp_sm, us, 'test_end_to_end_move_story_via_report_preserves_data',
         'End-to-end render then report then update for story moves')
    move(rp_sm, us, 'test_cross_epic_move_preserves_story_data',
         'Apply cross-epic story move preserves acceptance criteria and scenarios')

    # =========================================================================
    # STORIES: REPORT AC (9 -> 8, kill 1 dup, move 1 from Update)
    # =========================================================================
    print('\n=== Report acceptance criteria changes ===')

    # KILL duplicate: #7 covers same ground as #2 + #3
    kill(rp_ac, 'test_added_or_removed_ac_boxes_reflected_in_extracted_graph_and_update_report',
         'duplicate of added + removed scenarios')

    rename(rp_ac, 'test_when_then_ac_text_extracted_as_step_descriptions',
           'AC box with When/Then format text extracted as step description')
    rename(rp_ac, 'test_ac_box_text_not_in_when_then_format_treated_as_plain_acceptance_criteria',
           'AC box with plain text format treated as acceptance criteria without step extraction')

    # MOVE extraction scenario from Update to Report (detection is report logic)
    move(us, rp_ac, 'test_extract_exploration_maps_ac_boxes_to_stories_by_position_and_containment',
         'Extract assigns AC boxes to stories by vertical position and containment')

    # =========================================================================
    # STORIES: UPDATE (12 -> 14, gaining 3 from Report Moves, losing 1 to Report AC)
    # =========================================================================
    print('\n=== Update stories and acceptance criteria from diagram ===')

    rename(us, 'test_single_story_deleted_keeps_original_structure_and_flags_if_many_missing',
           'Removed story keeps original structure and flags if many missing from epic')
    rename(us, 'test_move_to_new_sub_epic',
           'Move to new sub-epic creates it and transfers story')
    rename(us, 'test_story_split_ac_distributed_correctly',
           'Story split distributes AC correctly to new and original stories')

    # =========================================================================
    # INCREMENTS: RENDER (7 -> 7, clean)
    # =========================================================================
    print('\n=== Render increment lanes ===')

    rename_by_old_name(ri, 'Lanes ordered by priority',
                       'Increment lanes ordered by priority with Y positions from outline bottom')
    rename_by_old_name(ri, 'Actor labels appear',
                       'Actor labels rendered above stories within each increment lane deduplicated per lane')

    # =========================================================================
    # INCREMENTS: REPORT (17 -> 13, kill 3 dups, move 1 to Update, fix 1 mismap)
    # =========================================================================
    print('\n=== Report increment changes ===')

    rename_by_old_name(rp_i, 'user-created lane background',
                       'User-created lane detected by geometry in diagram')
    rename_by_old_name(rp_i, 'Drag an orphan',
                       'Orphan story dragged into lane reported as added to increment')
    rename_by_old_name(rp_i, 'story in two lanes',
                       'Story in multiple lanes produces no false duplicate reports')
    rename_by_old_name(rp_i, 'UpdateReport lists story-level',
                       'Report lists exact fuzzy new and removed stories for increments view')
    rename_by_old_name(rp_i, 'story is moved between lanes',
                       'Story position change between lanes reflected in extracted graph')
    rename_by_old_name(rp_i, 'Known limitation',
                       'Known limitation inserting between existing lanes uses position-based matching')
    rename_by_old_name(rp_i, 'Story positioned far',
                       'Story not within threshold of any lane remains unassigned')

    # KILL duplicates
    kill(rp_i, 'test_apply_increment_changes_updates_story_graph_json',
         'apply logic belongs in Update (dup of Update scenarios)')
    kill(rp_i, 'test_apply_increment_change_creates_new_increment_if_needed',
         'duplicate of Update #4 (new increment creates)')
    kill(rp_i, 'test_end_to_end_render_move_report_update_verifies_story_graph',
         'duplicate of Update #9 end-to-end')

    # FIX mismap: test_extract_increments... has wrong scenario name
    rename(rp_i, 'test_extract_increments_assigns_stories_to_lanes_by_y_position_with_priority_from_order',
           'Extract assigns stories to increment lanes by Y position with priority from order')

    # KILL duplicate: #14 is same as #8 (both test story movement between lanes)
    kill(rp_i, 'test_story_moved_between_increments_reflected_in_extracted_graph',
         'duplicate of move_story_between_increments_reports_correct_delta')

    # =========================================================================
    # INCREMENTS: UPDATE (14 -> 12, kill 2 dups, move 1 to Report)
    # =========================================================================
    print('\n=== Update increments from diagram ===')

    rename(ui, 'test_apply_remove_increment_returns_false_for_nonexistent',
           'Removing non-existent increment returns false')
    rename(ui, 'test_apply_increment_order_updates_priorities',
           'Update increment order from diagram updates priorities in story graph')
    rename(ui, 'test_apply_increment_order_no_change_when_already_correct',
           'No changes when increment priorities already match diagram order')
    rename_by_old_name(ui, 'Removing a lane from diagram',
                       'Merge preserves removed increment lane in story graph')
    rename_by_old_name(ui, 'Extra lanes appended',
                       'Extra lanes appended and fewer lanes leave original increments unchanged')

    # MOVE report-generation scenarios to Report
    move(ui, rp_i, 'test_report_includes_removed_increments_and_order',
         'Report includes removed increments and new order')

    # KILL duplicates
    kill(ui, 'test_removed_increments_and_order_roundtrip_through_json',
         'roundtrip already covered in Report #7')
    kill(ui, 'test_new_increment_lane_at_bottom_appended_as_new_increment',
         'duplicate of #4 (new increment creates)')

    # =========================================================================
    # RENUMBER ALL
    # =========================================================================
    print('\n=== Renumbering ===')
    for name, story in stories.items():
        renumber(story)

    # =========================================================================
    # FINAL COUNTS
    # =========================================================================
    print('\n=== FINAL COUNTS ===')
    total = 0
    for e in g.get('epics', []):
        for se in e.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == NEW_SUB_EPIC:
                        for se3 in se2.get('sub_epics', []):
                            group_total = 0
                            print(f'\n  {se3["name"]}:')
                            for sg in se3.get('story_groups', []):
                                for st in sg.get('stories', []):
                                    c = len(st.get('scenarios', []))
                                    group_total += c
                                    total += c
                                    print(f'    {c:3d}  {st["name"]}')
                            print(f'    --- {group_total} total')
    print(f'\n  GRAND TOTAL: {total} scenarios')

    STORY_GRAPH_PATH.write_text(json.dumps(g, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'\nWrote to {STORY_GRAPH_PATH}')


if __name__ == '__main__':
    main()
