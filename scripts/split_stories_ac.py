"""
Split "Update stories and acceptance criteria from diagram" into two stories:
  - "Update stories from diagram" (story move/delete scenarios)
  - "Update acceptance criteria from diagram" (AC apply/merge scenarios)

This makes Stories and Actors consistent: each entity type gets its own
report AND update story, just like epics have their own and increments have theirs.

Before: Report story moves | Report AC changes | Update stories+AC (14 scenarios)
After:  Report story moves | Report AC changes | Update stories from diagram | Update AC from diagram
"""
import json, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
STORY_GRAPH_PATH = Path(__file__).parent.parent / 'docs' / 'story' / 'story-graph.json'

# Scenarios that belong to "Update stories from diagram" (story-level operations)
STORY_UPDATE_METHODS = {
    'test_moved_story_gets_recomputed_sequential_order_from_new_position',
    'test_single_story_deleted_keeps_original_structure_and_flags_if_many_missing',
    'test_stories_preserved_when_sub_epic_removed_but_stories_moved',
    'test_story_not_moved_is_deleted_with_sub_epic',
    'test_move_to_renamed_sub_epic',
    'test_move_to_new_sub_epic',
    'test_apply_move_story_preserves_data',
    'test_end_to_end_move_story_via_report_preserves_data',
    'test_cross_epic_move_preserves_story_data',
}

# Everything else in the combined story goes to "Update acceptance criteria from diagram"


def main():
    g = json.loads(Path(STORY_GRAPH_PATH).read_text(encoding='utf-8'))

    # Find the combined story and its parent story_group
    target_sg = None
    combined_story = None
    for e in g['epics']:
        for se in e.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == 'Synchronize Diagram by Domain':
                        for se3 in se2.get('sub_epics', []):
                            if se3.get('name') == 'Synchronize Stories and Actors':
                                for sg in se3.get('story_groups', []):
                                    for st in sg.get('stories', []):
                                        if st['name'] == 'Update stories and acceptance criteria from diagram':
                                            target_sg = sg
                                            combined_story = st

    if not combined_story:
        print('ERROR: Combined story not found')
        return 1

    print(f'Found combined story with {len(combined_story["scenarios"])} scenarios')

    # Split scenarios
    story_scenarios = []
    ac_scenarios = []
    for sc in combined_story.get('scenarios', []):
        if sc.get('test_method') in STORY_UPDATE_METHODS:
            story_scenarios.append(sc)
        else:
            ac_scenarios.append(sc)

    # Renumber
    for i, sc in enumerate(story_scenarios, 1):
        sc['sequential_order'] = float(i)
    for i, sc in enumerate(ac_scenarios, 1):
        sc['sequential_order'] = float(i)

    print(f'\nUpdate stories from diagram: {len(story_scenarios)} scenarios')
    for sc in story_scenarios:
        print(f'  - [{sc.get("test_method")}] {sc["name"]}')

    print(f'\nUpdate acceptance criteria from diagram: {len(ac_scenarios)} scenarios')
    for sc in ac_scenarios:
        print(f'  - [{sc.get("test_method")}] {sc["name"]}')

    # Replace combined story with story-update story
    combined_story['name'] = 'Update stories from diagram'
    combined_story['test_class'] = 'TestUpdateStoriesFromDiagram'
    combined_story['scenarios'] = story_scenarios
    combined_story['acceptance_criteria'] = [
        {'name': 'When sub-epic is removed but its stories were moved then moves are applied before removes so stories survive',
         'text': 'When sub-epic is removed but its stories were moved then moves are applied before removes so stories survive',
         'sequential_order': 1.0},
        {'name': 'When story is not moved then it is deleted with its sub-epic',
         'text': 'When story is not moved then it is deleted with its sub-epic',
         'sequential_order': 2.0},
        {'name': 'When story move is applied then all story fields including acceptance criteria and scenarios are preserved',
         'text': 'When story move is applied then all story fields including acceptance criteria and scenarios are preserved',
         'sequential_order': 3.0},
        {'name': 'When story moves to renamed or new sub-epic then move resolves correctly',
         'text': 'When story moves to renamed or new sub-epic then move resolves correctly',
         'sequential_order': 4.0},
    ]

    # Create new AC-update story
    ac_update_story = {
        'name': 'Update acceptance criteria from diagram',
        'sequential_order': combined_story['sequential_order'] + 0.5,
        'connector': 'or',
        'story_type': 'user',
        'users': ['Bot Behavior'],
        'test_class': 'TestUpdateAcceptanceCriteriaFromDiagram',
        'test_file': 'invoke_bot/perform_action/test_sync_stories_and_actors.py',
        'acceptance_criteria': [
            {'name': 'When AC is deleted from a story in diagram then story graph removes it',
             'text': 'When AC is deleted from a story in diagram then story graph removes it',
             'sequential_order': 1.0},
            {'name': 'When AC is moved between stories in diagram then both source and target are updated',
             'text': 'When AC is moved between stories in diagram then both source and target are updated',
             'sequential_order': 2.0},
            {'name': 'When story is deleted and its AC redistributed then target stories receive the AC',
             'text': 'When story is deleted and its AC redistributed then target stories receive the AC',
             'sequential_order': 3.0},
            {'name': 'When update is applied then original acceptance criteria for matched stories are preserved',
             'text': 'When update is applied then original acceptance criteria for matched stories are preserved',
             'sequential_order': 4.0},
        ],
        'scenarios': ac_scenarios,
        'behavior': None,
    }

    # Add new story after the renamed one
    stories_list = target_sg['stories']
    idx = stories_list.index(combined_story)
    stories_list.insert(idx + 1, ac_update_story)

    # Renumber all stories in the group
    for i, st in enumerate(stories_list, 1):
        st['sequential_order'] = float(i)

    print(f'\nStories in Synchronize Stories and Actors:')
    for st in stories_list:
        print(f'  {st["sequential_order"]:.0f}. {st["name"]} ({len(st.get("scenarios",[]))} scenarios)')

    Path(STORY_GRAPH_PATH).write_text(json.dumps(g, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'\nWrote to {STORY_GRAPH_PATH}')


if __name__ == '__main__':
    main()
