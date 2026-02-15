"""Add missing 'Re-render with saved layout data preserves...' scenario to Epics/Render."""
import json, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
STORY_GRAPH_PATH = Path(__file__).parent.parent / 'docs' / 'story' / 'story-graph.json'

g = json.loads(STORY_GRAPH_PATH.read_text(encoding='utf-8'))

for e in g['epics']:
    for se in e.get('sub_epics', []):
        if se.get('name') == 'Perform Action':
            for se2 in se.get('sub_epics', []):
                if se2.get('name') == 'Synchronize Diagram by Domain':
                    for se3 in se2.get('sub_epics', []):
                        if se3.get('name') == 'Synchronize Epics and Sub-Epics':
                            for sg in se3.get('story_groups', []):
                                for st in sg.get('stories', []):
                                    if st['name'] == 'Render epic and sub-epic hierarchy':
                                        existing = {s.get('name') for s in st['scenarios']}
                                        new_name = 'Re-render with saved layout data preserves epic and sub-epic positions'
                                        if new_name not in existing:
                                            order = float(len(st['scenarios']) + 1)
                                            st['scenarios'].append({
                                                'name': new_name,
                                                'sequential_order': order,
                                                'type': '',
                                                'background': [],
                                                'test_method': None,
                                                'steps': '',
                                            })
                                            print(f'ADDED to Epics/Render: "{new_name}"')
                                            print(f'  (needs test method)')
                                        else:
                                            print('Already exists')

# Show all three for comparison
print('\nRe-render pattern across domains:')
for e in g['epics']:
    for se in e.get('sub_epics', []):
        if se.get('name') == 'Perform Action':
            for se2 in se.get('sub_epics', []):
                if se2.get('name') == 'Synchronize Diagram by Domain':
                    for se3 in se2.get('sub_epics', []):
                        for sg in se3.get('story_groups', []):
                            for st in sg.get('stories', []):
                                for sc in st.get('scenarios', []):
                                    if 'Re-render with saved layout' in sc.get('name', ''):
                                        print(f'  [{se3["name"]}] {sc["name"]}')

STORY_GRAPH_PATH.write_text(json.dumps(g, indent=2, ensure_ascii=False), encoding='utf-8')
print('\nWrote to story graph')
