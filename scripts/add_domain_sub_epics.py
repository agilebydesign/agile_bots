"""
Restructure "Synchronize Diagram by Domain" from flat story list
into 3 domain sub-epics, each with their own stories.

Before: Synchronize Diagram by Domain -> story_groups -> [10 flat stories]
After:  Synchronize Diagram by Domain -> sub_epics -> [
          Synchronize Epics and Sub-Epics -> [3 stories]
          Synchronize Stories and Actors -> [4 stories]
          Synchronize Increments -> [3 stories]
        ]
"""
import json
import sys
from pathlib import Path

STORY_GRAPH_PATH = Path(__file__).parent.parent / 'docs' / 'story' / 'story-graph.json'
SUB_EPIC_NAME = 'Synchronize Diagram by Domain'

DOMAIN_GROUPS = {
    'Synchronize Epics and Sub-Epics': {
        'sequential_order': 1.0,
        'test_file': 'invoke_bot/perform_action/test_sync_epics_and_sub_epics.py',
        'stories': [
            'Render epic and sub-epic hierarchy',
            'Report epic and sub-epic changes',
            'Update epics and sub-epics from diagram',
        ],
    },
    'Synchronize Stories and Actors': {
        'sequential_order': 2.0,
        'test_file': 'invoke_bot/perform_action/test_sync_stories_and_actors.py',
        'stories': [
            'Render stories and actors',
            'Report story moves between parents',
            'Report acceptance criteria changes',
            'Update stories and acceptance criteria from diagram',
        ],
    },
    'Synchronize Increments': {
        'sequential_order': 3.0,
        'test_file': 'invoke_bot/perform_action/test_sync_increments.py',
        'stories': [
            'Render increment lanes',
            'Report increment changes',
            'Update increments from diagram',
        ],
    },
}


def find_sub_epic(graph_data, name):
    for epic in graph_data.get('epics', []):
        for se in epic.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == name:
                        return se2
    return None


def main():
    print(f'Loading {STORY_GRAPH_PATH}')
    graph_data = json.loads(STORY_GRAPH_PATH.read_text(encoding='utf-8'))

    se = find_sub_epic(graph_data, SUB_EPIC_NAME)
    if not se:
        print(f'ERROR: Could not find "{SUB_EPIC_NAME}"')
        return 1

    # Check if already restructured (has sub_epics with stories)
    if se.get('sub_epics') and len(se['sub_epics']) > 0:
        print(f'Already has {len(se["sub_epics"])} sub-epics -- skipping')
        return 0

    # Get all stories from flat list
    all_stories = {}
    for sg in se.get('story_groups', []):
        for story in sg.get('stories', []):
            all_stories[story['name']] = story
    print(f'Found {len(all_stories)} flat stories to organize')

    # Build domain sub-epics
    new_sub_epics = []
    for group_name, config in DOMAIN_GROUPS.items():
        group_stories = []
        for i, story_name in enumerate(config['stories'], 1):
            story = all_stories.get(story_name)
            if not story:
                print(f'  WARNING: Story "{story_name}" not found')
                continue
            story['sequential_order'] = float(i)
            group_stories.append(story)
            print(f'  {group_name} <- {story_name} ({len(story.get("scenarios", []))} scenarios)')

        new_sub_epics.append({
            'name': group_name,
            'sequential_order': config['sequential_order'],
            'behavior': None,
            'domain_concepts': [],
            'test_file': config['test_file'],
            'sub_epics': [],
            'story_groups': [
                {
                    'name': '',
                    'sequential_order': 0.0,
                    'type': 'and',
                    'connector': None,
                    'behavior': None,
                    'stories': group_stories,
                }
            ],
        })

    # Replace flat structure with sub-epics
    se['sub_epics'] = new_sub_epics
    se['story_groups'] = []  # Clear flat stories
    # Remove test_file from parent -- it's on the sub-epics now
    se.pop('test_file', None)

    print(f'\nRestructured into {len(new_sub_epics)} domain sub-epics:')
    for sub in new_sub_epics:
        story_count = len(sub['story_groups'][0]['stories'])
        print(f'  {sub["name"]} ({story_count} stories, file={sub["test_file"]})')

    STORY_GRAPH_PATH.write_text(
        json.dumps(graph_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'\nWrote to {STORY_GRAPH_PATH}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
