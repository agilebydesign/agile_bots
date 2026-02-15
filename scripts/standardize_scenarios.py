"""
Standardize scenario names across domain groups using consistent base sentences.
Where a pattern exists in one domain but not others, add the missing scenario.
Domain-unique scenarios stay as-is.

Pattern templates (base sentence + domain flavor):
  "{Base pattern} for {domain entity}"

After standardizing names, also ensures every domain has the same set of
shared patterns, adding missing scenarios where needed.
"""
import json
import sys
import io
from pathlib import Path

STORY_GRAPH_PATH = Path(__file__).parent.parent / 'docs' / 'story' / 'story-graph.json'
NEW_SUB_EPIC = 'Synchronize Diagram by Domain'

# ============================================================================
# CONSISTENT SCENARIO TEMPLATES
# Each template has a base sentence and domain-specific flavors.
# If a domain is listed, it MUST have that scenario. Missing ones get added.
# ============================================================================

# Keyed by (domain_sub_epic, story_name) -> list of scenarios
# Domain shorthand: E = Epics, S = Stories, I = Increments

RENDER_PATTERNS = [
    {
        'base': 'Render {entity} with default layout positions {entity_detail}',
        'flavors': {
            'Render epic and sub-epic hierarchy': {
                'name': 'Render epic and sub-epic hierarchy with default layout positions epics at fixed Y and sub-epics below',
                'test_methods': ['test_render_3_level_nested_sub_epics_creates_sub_epic_inside_sub_epic'],
            },
            'Render stories and actors': {
                'name': 'Render stories and actors with default layout positions stories below deepest sub-epic',
                'test_methods': ['test_stories_positioned_below_deepest_sub_epic'],
            },
            'Render increment lanes': {
                'name': 'Render increment lanes with default layout positions lanes below outline by priority',
                'test_methods': ['test_render_increments_diagram_with_stories_assigned_to_increment_lanes'],
            },
        },
    },
    {
        'base': 'Parent {entity} spans all child {children} horizontally',
        'flavors': {
            'Render epic and sub-epic hierarchy': {
                'name': 'Parent epic spans all child sub-epics horizontally',
                'test_methods': ['test_epic_horizontal_span_covers_all_sub_epics'],
            },
            'Render stories and actors': {
                'name': 'Parent sub-epic spans all child stories horizontally',
                'test_methods': ['test_sub_epic_horizontal_span_covers_all_stories'],
            },
        },
    },
    {
        'base': 'Sibling {entities} do not overlap horizontally',
        'flavors': {
            'Render epic and sub-epic hierarchy': {
                'name': 'Sibling sub-epics do not overlap horizontally',
                'test_methods': ['test_sibling_sub_epics_do_not_overlap_horizontally'],
            },
            'Render stories and actors': {
                'name': 'Sibling stories do not overlap horizontally',
                'test_methods': ['test_sibling_stories_do_not_overlap_horizontally'],
            },
        },
    },
    {
        'base': 'Re-render with saved layout data preserves {entity} positions',
        'flavors': {
            'Render stories and actors': {
                'name': 'Re-render with saved layout data preserves story and AC box positions',
                'test_methods': ['test_re_render_exploration_with_layout_data_preserves_story_and_ac_box_positions'],
            },
            'Render increment lanes': {
                'name': 'Re-render with saved layout data preserves epic and sub-epic positions and recomputes lane positions',
                'test_methods': ['test_re_render_increments_with_existing_layout_data_recomputes_lane_positions'],
            },
        },
    },
    {
        'base': 'Render completes and writes DrawIO file with correct summary for {entity}',
        'flavors': {
            'Render increment lanes': {
                'name': 'Render completes and writes DrawIO file with correct summary for increment lanes',
                'test_methods': ['test_render_increments_completes_and_summary_includes_increment_count'],
            },
        },
    },
    {
        'base': 'All {entity} cells have required styles for rendering',
        'flavors': {
            'Render epic and sub-epic hierarchy': {
                'name': 'All epic and sub-epic cells have required styles for rendering',
                'test_methods': ['test_sub_epic_horizontal_span_covers_all_stories'],  # visual integrity
            },
            'Render increment lanes': {
                'name': 'All increment lane cells have required styles for extractor detection',
                'test_methods': ['test_increment_lane_cells_styled_for_extractor_detection'],
            },
        },
    },
    {
        'base': 'Render with no {entity} defined produces {fallback} diagram',
        'flavors': {
            'Render increment lanes': {
                'name': 'Render with no increments defined produces outline-only diagram',
                'test_methods': ['test_render_increments_with_no_increments_defined_produces_outline_only_diagram'],
            },
            'Render stories and actors': {
                'name': 'Render with no acceptance criteria produces story without AC boxes',
                'test_methods': ['test_story_with_no_acceptance_criteria_renders_without_ac_boxes'],
            },
        },
    },
]

REPORT_PATTERNS = [
    {
        'base': 'No changes reported when diagram matches original for {entity}',
        'flavors': {
            'Report epic and sub-epic changes': {
                'name': 'No changes reported when diagram matches original for epics and sub-epics',
                'test_methods': [],  # NEW -- needs test
            },
            'Report story moves between parents': {
                'name': 'No changes reported when diagram matches original for story positions',
                'test_methods': ['test_no_false_moves_when_no_changes'],
            },
            'Report acceptance criteria changes': {
                'name': 'No changes reported when diagram matches original for acceptance criteria',
                'test_methods': ['test_no_ac_changes_when_diagram_matches_original'],
            },
            'Report increment changes': {
                'name': 'No changes reported when diagram matches original for increments',
                'test_methods': ['test_no_changes_when_diagram_matches_original'],
            },
        },
    },
    {
        'base': 'Report roundtrips through JSON for {entity} changes',
        'flavors': {
            'Report epic and sub-epic changes': {
                'name': 'Report roundtrips through JSON for epic and sub-epic rename changes',
                'test_methods': [],  # NEW -- needs test
            },
            'Report story moves between parents': {
                'name': 'Report roundtrips through JSON for story move changes',
                'test_methods': ['test_moved_stories_serializes_to_json_and_round_trips'],
            },
            'Report acceptance criteria changes': {
                'name': 'Report roundtrips through JSON for acceptance criteria changes',
                'test_methods': ['test_ac_changes_roundtrip_through_json'],
            },
            'Report increment changes': {
                'name': 'Report roundtrips through JSON for increment changes',
                'test_methods': ['test_increment_delta_serializes_to_json_and_round_trips'],
            },
        },
    },
    {
        'base': '{Entity} added in diagram detected as new in report',
        'flavors': {
            'Report epic and sub-epic changes': {
                'name': 'Sub-epic added in diagram detected as new in report',
                'test_methods': ['test_user_created_sub_epic_with_simple_id_reported_as_new_not_rename'],
            },
            'Report acceptance criteria changes': {
                'name': 'AC box added in diagram detected as new in report',
                'test_methods': ['test_added_ac_box_detected_in_report'],
            },
            'Report increment changes': {
                'name': 'Increment lane added in diagram detected as new in report',
                'test_methods': ['test_user_created_lane_shows_in_report_as_new_increment'],
            },
        },
    },
    {
        'base': '{Entity} removed from diagram detected as removed in report',
        'flavors': {
            'Report acceptance criteria changes': {
                'name': 'AC box removed from diagram detected as removed in report',
                'test_methods': ['test_removed_ac_box_detected_in_report'],
            },
            'Report increment changes': {
                'name': 'Increment removed from diagram detected as removed in report',
                'test_methods': ['test_extract_increments_assigns_stories_to_lanes_by_y_position_with_priority_from_order'],
            },
        },
    },
    {
        'base': '{Entity} moved between parents detected as move not new plus removed',
        'flavors': {
            'Report story moves between parents': {
                'name': 'Story moved between sub-epics detected as move not new plus removed',
                'test_methods': ['test_story_moved_between_sub_epics_detected_as_move_not_new'],
            },
            'Report acceptance criteria changes': {
                'name': 'AC moved between stories detected as move not new plus removed',
                'test_methods': ['test_ac_moved_between_stories_detected_as_move'],
            },
            'Report increment changes': {
                'name': 'Story moved between increment lanes detected as move in report',
                'test_methods': ['test_move_story_between_increments_reports_correct_delta'],
            },
        },
    },
    {
        'base': '{Entity} renamed in diagram detected as rename in report',
        'flavors': {
            'Report epic and sub-epic changes': {
                'name': 'Sub-epic renamed in diagram detected as rename in report',
                'test_methods': ['test_tool_generated_sub_epic_with_hierarchical_id_still_eligible_for_rename'],
            },
            'Report increment changes': {
                'name': 'Increment lane renamed in diagram detected as rename in report',
                'test_methods': [],  # covered by update story
            },
        },
    },
    {
        'base': '{Entity} assigned to parent by position in diagram',
        'flavors': {
            'Report acceptance criteria changes': {
                'name': 'AC boxes assigned to stories by vertical position below story cells',
                'test_methods': ['test_ac_cells_assigned_to_stories_by_vertical_position_below_story_cells'],
            },
            'Report increment changes': {
                'name': 'Stories assigned to increment lanes by Y position',
                'test_methods': ['test_user_created_lane_stories_assigned_by_y_position'],
            },
        },
    },
]

UPDATE_PATTERNS = [
    {
        'base': 'Moved {entity} preserved when parent removed from diagram',
        'flavors': {
            'Update stories and acceptance criteria from diagram': {
                'name': 'Moved stories preserved when sub-epic removed from diagram',
                'test_methods': ['test_stories_preserved_when_sub_epic_removed_but_stories_moved'],
            },
            'Update increments from diagram': {
                'name': 'Moved stories preserved when increment lane removed from diagram',
                'test_methods': ['test_end_to_end_remove_lane_and_reorder_updates_story_graph'],
            },
        },
    },
    {
        'base': 'Unmoved {entity} removed with parent when parent removed from diagram',
        'flavors': {
            'Update stories and acceptance criteria from diagram': {
                'name': 'Unmoved stories removed with sub-epic when sub-epic removed from diagram',
                'test_methods': ['test_story_not_moved_is_deleted_with_sub_epic'],
            },
            'Update increments from diagram': {
                'name': 'Removed increment deletes entire increment from story graph',
                'test_methods': ['test_apply_remove_increment_deletes_entire_increment_from_story_graph'],
            },
        },
    },
    {
        'base': 'Apply {entity} changes from report updates story graph',
        'flavors': {
            'Update epics and sub-epics from diagram': {
                'name': 'Apply epic and sub-epic changes from report updates story graph',
                'test_methods': ['test_story_map_updated_from_outline_diagram_applies_report_changes'],
            },
            'Update stories and acceptance criteria from diagram': {
                'name': 'Apply acceptance criteria changes from report updates story graph',
                'test_methods': ['test_apply_ac_change_adds_and_removes'],
            },
            'Update increments from diagram': {
                'name': 'Apply increment changes from report updates story graph',
                'test_methods': ['test_apply_increment_move_transfers_story_between_increments'],
            },
        },
    },
    {
        'base': 'Apply {entity} move transfers between parents preserving data',
        'flavors': {
            'Update stories and acceptance criteria from diagram': {
                'name': 'Apply story move transfers between sub-epics preserving data',
                'test_methods': ['test_moved_story_gets_recomputed_sequential_order_from_new_position'],
            },
            'Update stories and acceptance criteria from diagram (ac)': {
                'name': 'Apply AC move transfers between stories preserving data',
                'test_methods': ['test_apply_ac_move_preserves_data'],
            },
            'Update increments from diagram': {
                'name': 'Apply increment move transfers story between increments preserving data',
                'test_methods': ['test_apply_increment_move_transfers_story_between_increments'],
            },
        },
    },
    {
        'base': 'End-to-end render then report then update for {entity}',
        'flavors': {
            'Update epics and sub-epics from diagram': {
                'name': 'End-to-end render then report then update for epic hierarchy',
                'test_methods': [],  # NEW -- needs test
            },
            'Update stories and acceptance criteria from diagram': {
                'name': 'End-to-end render then report then update for acceptance criteria',
                'test_methods': ['test_end_to_end_ac_add_remove_via_report'],
            },
            'Update increments from diagram': {
                'name': 'End-to-end render then report then update for increment lanes',
                'test_methods': ['test_end_to_end_remove_lane_and_reorder_updates_story_graph'],
            },
        },
    },
    {
        'base': 'Update preserves original data for matched {entity}',
        'flavors': {
            'Update stories and acceptance criteria from diagram': {
                'name': 'Update preserves original acceptance criteria for matched stories',
                'test_methods': ['test_merge_preserves_original_ac_for_matched_stories_from_exploration_view'],
            },
            'Update increments from diagram': {
                'name': 'Update preserves original acceptance criteria for matched increment stories',
                'test_methods': ['test_merge_preserves_original_ac_and_updates_story_fields'],
            },
        },
    },
    {
        'base': 'New {entity} in diagram creates it in story graph',
        'flavors': {
            'Update epics and sub-epics from diagram': {
                'name': 'New sub-epic in diagram creates it in story graph',
                'test_methods': [],  # implicit in existing tests
            },
            'Update increments from diagram': {
                'name': 'New increment lane in diagram creates it in story graph',
                'test_methods': ['test_apply_increment_move_creates_target_if_missing',
                                  'test_new_increment_lane_at_bottom_appended_as_new_increment'],
            },
        },
    },
    {
        'base': 'Renamed {entity} in diagram updates name in story graph',
        'flavors': {
            'Update epics and sub-epics from diagram': {
                'name': 'Renamed sub-epic in diagram updates name in story graph',
                'test_methods': ['test_renamed_or_reordered_nodes_flagged_as_fuzzy_matches_in_update_report'],
            },
            'Update stories and acceptance criteria from diagram': {
                'name': 'Move to renamed sub-epic updates correctly in story graph',
                'test_methods': ['test_move_to_renamed_sub_epic'],
            },
            'Update increments from diagram': {
                'name': 'Renamed increment lane in diagram updates name in story graph',
                'test_methods': ['test_renamed_increment_lane_updated_by_position_based_matching'],
            },
        },
    },
]


def find_story(graph_data, story_name):
    """Find a story in the new sub-epic."""
    for epic in graph_data.get('epics', []):
        for se in epic.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == NEW_SUB_EPIC:
                        for se3 in se2.get('sub_epics', []):
                            for sg in se3.get('story_groups', []):
                                for story in sg.get('stories', []):
                                    if story['name'] == story_name:
                                        return story
    return None


def rename_scenario(story, old_test_methods, new_name):
    """Rename a scenario by finding it via test_method."""
    for sc in story.get('scenarios', []):
        if sc.get('test_method') in old_test_methods:
            old_name = sc['name']
            sc['name'] = new_name
            return old_name
    return None


def add_scenario_if_missing(story, name, test_methods):
    """Add a scenario if no matching test_method exists."""
    existing_methods = {sc.get('test_method') for sc in story.get('scenarios', [])}
    existing_names = {sc.get('name') for sc in story.get('scenarios', [])}

    if name in existing_names:
        return False

    # Check if any test_method already mapped
    for tm in test_methods:
        if tm in existing_methods:
            return False

    order = max((sc.get('sequential_order', 0) for sc in story.get('scenarios', [])), default=0) + 1
    story.setdefault('scenarios', []).append({
        'name': name,
        'sequential_order': float(order),
        'type': '',
        'background': [],
        'test_method': test_methods[0] if test_methods else None,
        'steps': '',
    })
    return True


def process_patterns(graph_data, patterns, operation_name):
    """Process a set of patterns, renaming existing scenarios and adding missing ones."""
    renamed = 0
    added = 0

    for pattern in patterns:
        for story_name_raw, config in pattern['flavors'].items():
            # Handle the "(ac)" suffix hack for duplicate story targets
            story_name = story_name_raw.split(' (')[0]
            story = find_story(graph_data, story_name)
            if not story:
                print(f'  WARNING: Story "{story_name}" not found')
                continue

            new_name = config['name']
            test_methods = config['test_methods']

            # Try to rename existing scenario first
            if test_methods:
                old = rename_scenario(story, test_methods, new_name)
                if old:
                    if old != new_name:
                        renamed += 1
                        print(f'  RENAME: "{old[:50]}..." -> "{new_name[:50]}..."')
                    continue

            # Add if missing
            if add_scenario_if_missing(story, new_name, test_methods):
                added += 1
                marker = '(NEW - needs test)' if not test_methods else ''
                print(f'  ADD:    "{new_name[:60]}" {marker}')

    return renamed, added


def main():
    print(f'Loading {STORY_GRAPH_PATH}')
    graph_data = json.loads(STORY_GRAPH_PATH.read_text(encoding='utf-8'))

    total_renamed = 0
    total_added = 0

    for op_name, patterns in [('RENDER', RENDER_PATTERNS), ('REPORT', REPORT_PATTERNS), ('UPDATE', UPDATE_PATTERNS)]:
        print(f'\n=== {op_name} PATTERNS ===')
        r, a = process_patterns(graph_data, patterns, op_name)
        total_renamed += r
        total_added += a

    print(f'\n--- Summary: {total_renamed} renamed, {total_added} added ---')

    # Final counts
    print('\nFinal scenario counts:')
    for epic in graph_data.get('epics', []):
        for se in epic.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == NEW_SUB_EPIC:
                        for se3 in se2.get('sub_epics', []):
                            print(f'\n  {se3["name"]}:')
                            for sg in se3.get('story_groups', []):
                                for story in sg.get('stories', []):
                                    count = len(story.get('scenarios', []))
                                    print(f'    {count:3d}  {story["name"]}')

    STORY_GRAPH_PATH.write_text(
        json.dumps(graph_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'\nWrote to {STORY_GRAPH_PATH}')
    return 0


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.exit(main())
