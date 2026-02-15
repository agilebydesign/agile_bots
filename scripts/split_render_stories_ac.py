"""
Split "Render stories and actors" into:
  - "Render stories and actors" (story/actor positioning and layout)
  - "Render acceptance criteria" (AC box rendering in exploration diagram)

After split, ensure consistent patterns exist in both.
"""
import json, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
STORY_GRAPH_PATH = Path(__file__).parent.parent / 'docs' / 'story' / 'story-graph.json'

# Scenarios that stay with "Render stories and actors" (story/actor rendering)
STORY_RENDER_METHODS = {
    'test_stories_positioned_below_deepest_sub_epic',
    'test_sub_epic_horizontal_span_covers_all_stories',
    'test_sibling_stories_do_not_overlap_horizontally',
}

# Everything else goes to "Render acceptance criteria"
# (AC boxes, exploration diagram, containment, styling)


def main():
    g = json.loads(Path(STORY_GRAPH_PATH).read_text(encoding='utf-8'))

    target_sg = None
    render_story = None
    for e in g['epics']:
        for se in e.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == 'Synchronize Diagram by Domain':
                        for se3 in se2.get('sub_epics', []):
                            if se3.get('name') == 'Synchronize Stories and Actors':
                                for sg in se3.get('story_groups', []):
                                    for st in sg.get('stories', []):
                                        if st['name'] == 'Render stories and actors':
                                            target_sg = sg
                                            render_story = st

    if not render_story:
        print('ERROR: Story not found')
        return 1

    print(f'Found "Render stories and actors" with {len(render_story["scenarios"])} scenarios')

    # Split scenarios
    story_scenarios = []
    ac_scenarios = []
    for sc in render_story.get('scenarios', []):
        if sc.get('test_method') in STORY_RENDER_METHODS:
            story_scenarios.append(sc)
        else:
            ac_scenarios.append(sc)

    # Renumber
    for i, sc in enumerate(story_scenarios, 1):
        sc['sequential_order'] = float(i)
    for i, sc in enumerate(ac_scenarios, 1):
        sc['sequential_order'] = float(i)

    print(f'\nRender stories and actors: {len(story_scenarios)} scenarios')
    for sc in story_scenarios:
        print(f'  - {sc["name"]}')

    print(f'\nRender acceptance criteria: {len(ac_scenarios)} scenarios')
    for sc in ac_scenarios:
        print(f'  - {sc["name"]}')

    # Update existing story to be story-only
    render_story['scenarios'] = story_scenarios
    render_story['acceptance_criteria'] = [
        {'name': 'When stories are rendered then they are positioned below deepest sub-epic',
         'text': 'When stories are rendered then they are positioned below deepest sub-epic',
         'sequential_order': 1.0},
        {'name': 'When stories have users then actor elements are rendered in actor row above stories',
         'text': 'When stories have users then actor elements are rendered in actor row above stories',
         'sequential_order': 2.0},
        {'name': 'When sub-epic contains stories then sub-epic horizontal span covers all its stories',
         'text': 'When sub-epic contains stories then sub-epic horizontal span covers all its stories',
         'sequential_order': 3.0},
        {'name': 'When sibling stories are rendered then no two stories overlap horizontally',
         'text': 'When sibling stories are rendered then no two stories overlap horizontally',
         'sequential_order': 4.0},
    ]

    # Create new AC render story
    ac_render_story = {
        'name': 'Render acceptance criteria',
        'sequential_order': render_story['sequential_order'] + 0.5,
        'connector': 'or',
        'story_type': 'user',
        'users': ['Bot Behavior'],
        'test_class': 'TestRenderAcceptanceCriteria',
        'test_file': 'invoke_bot/perform_action/test_sync_stories_and_actors.py',
        'acceptance_criteria': [
            {'name': 'When story has acceptance criteria then system renders AC boxes below story in exploration diagram',
             'text': 'When story has acceptance criteria then system renders AC boxes below story in exploration diagram',
             'sequential_order': 1.0},
            {'name': 'When AC boxes are rendered then they use correct fill stroke and left-aligned text style',
             'text': 'When AC boxes are rendered then they use correct fill stroke and left-aligned text style',
             'sequential_order': 2.0},
            {'name': 'When layout data exists then system preserves positions of story and AC boxes on re-render',
             'text': 'When layout data exists then system preserves positions of story and AC boxes on re-render',
             'sequential_order': 3.0},
            {'name': 'When story has no acceptance criteria then no AC boxes rendered below it',
             'text': 'When story has no acceptance criteria then no AC boxes rendered below it',
             'sequential_order': 4.0},
        ],
        'scenarios': ac_scenarios,
        'behavior': None,
    }

    # Insert after render story
    stories_list = target_sg['stories']
    idx = stories_list.index(render_story)
    stories_list.insert(idx + 1, ac_render_story)

    # Now add missing consistent patterns to both stories
    # Render stories needs: re-render with layout, render with default
    story_existing = {s.get('test_method') for s in render_story['scenarios']}
    story_names = {s.get('name') for s in render_story['scenarios']}

    if 'Re-render with saved layout data preserves story positions' not in story_names:
        render_story['scenarios'].append({
            'name': 'Re-render with saved layout data preserves story and actor positions',
            'sequential_order': float(len(render_story['scenarios']) + 1),
            'type': '', 'background': [], 'test_method': None, 'steps': '',
        })
        print('\n  ADDED to Render stories: Re-render with saved layout data preserves story and actor positions')

    # Render AC needs: render with default layout
    ac_names = {s.get('name') for s in ac_render_story['scenarios']}
    if not any('default layout' in n for n in ac_names):
        ac_render_story['scenarios'].insert(0, {
            'name': 'Render acceptance criteria with default layout positions AC boxes below stories',
            'sequential_order': 0.5,
            'type': '', 'background': [], 'test_method': None, 'steps': '',
        })
        print('  ADDED to Render AC: Render acceptance criteria with default layout positions AC boxes below stories')

    # Renumber all scenarios in both stories
    for i, sc in enumerate(render_story['scenarios'], 1):
        sc['sequential_order'] = float(i)
    for i, sc in enumerate(ac_render_story['scenarios'], 1):
        sc['sequential_order'] = float(i)

    # Renumber all stories
    for i, st in enumerate(stories_list, 1):
        st['sequential_order'] = float(i)

    print(f'\nStories in Synchronize Stories and Actors:')
    for st in stories_list:
        print(f'  {st["sequential_order"]:.0f}. {st["name"]} ({len(st.get("scenarios",[]))} scenarios)')

    Path(STORY_GRAPH_PATH).write_text(json.dumps(g, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'\nWrote to {STORY_GRAPH_PATH}')


if __name__ == '__main__':
    main()
