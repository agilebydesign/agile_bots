"""Move 'extract to json' scenario from Render to Report story, rename to match roundtrip pattern."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

STORY_GRAPH_PATH = 'docs/story/story-graph.json'
g = json.loads(open(STORY_GRAPH_PATH, encoding='utf-8').read())

render_story = None
report_story = None

for e in g['epics']:
    for se in e.get('sub_epics', []):
        for se2 in se.get('sub_epics', []):
            if se2.get('name') != 'Synchronize Diagram by Domain':
                continue
            for se3 in se2.get('sub_epics', []):
                for sg in se3.get('story_groups', []):
                    for st in sg.get('stories', []):
                        if st['name'] == 'Render epic and sub-epic hierarchy':
                            render_story = st
                        if st['name'] == 'Report epic and sub-epic changes':
                            report_story = st

# Remove from Render
moved = None
render_story['scenarios'] = [
    sc for sc in render_story['scenarios']
    if sc.get('test_method') != 'test_extract_to_json_preserves_nested_sub_epic_structure'
    or (moved := sc) is None  # walrus trick to capture it
]
# The walrus didn't work cleanly, do it properly
for sc in list(render_story['scenarios']):
    if sc.get('test_method') == 'test_extract_to_json_preserves_nested_sub_epic_structure':
        moved = sc
        render_story['scenarios'].remove(sc)
        break

if moved:
    # Rename to match roundtrip pattern
    moved['name'] = 'Report roundtrips through JSON for epic and sub-epic hierarchy structure'
    moved['sequential_order'] = float(len(report_story['scenarios']) + 1)
    
    # Check if we already have the placeholder roundtrip scenario (no test_method)
    # and replace it with the real one
    report_story['scenarios'] = [
        sc for sc in report_story['scenarios']
        if not (sc['name'] == 'Report roundtrips through JSON for epic and sub-epic rename changes' 
                and not sc.get('test_method'))
    ]
    
    report_story['scenarios'].append(moved)
    print(f'MOVED: test_extract_to_json_preserves_nested_sub_epic_structure')
    print(f'  FROM: Render epic and sub-epic hierarchy')
    print(f'  TO:   Report epic and sub-epic changes')
    print(f'  AS:   Report roundtrips through JSON for epic and sub-epic hierarchy structure')
else:
    print('Scenario not found -- may have already been moved')

# Renumber both stories
for i, sc in enumerate(render_story['scenarios'], 1):
    sc['sequential_order'] = float(i)
for i, sc in enumerate(report_story['scenarios'], 1):
    sc['sequential_order'] = float(i)

print(f'\nRender epic: {len(render_story["scenarios"])} scenarios')
print(f'Report epic: {len(report_story["scenarios"])} scenarios')

open(STORY_GRAPH_PATH, 'w', encoding='utf-8').write(json.dumps(g, indent=2, ensure_ascii=False))
print('Wrote story graph')
