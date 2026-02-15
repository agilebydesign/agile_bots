"""
Audit: for each new scenario that has a test_method, find the old scenario's steps
and show what they say vs where they're going now. Flag mismatches.
"""
import json, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
STORY_GRAPH_PATH = Path(__file__).parent.parent / 'docs' / 'story' / 'story-graph.json'

g = json.loads(STORY_GRAPH_PATH.read_text(encoding='utf-8'))

# Build map: test_method -> {old_story, old_scenario_name, steps, background}
old_map = {}
for e in g['epics']:
    for se in e.get('sub_epics', []):
        if se.get('name') == 'Perform Action':
            for se2 in se.get('sub_epics', []):
                if se2.get('name') == 'Synchronized Graph with Rendered Diagram Content':
                    for sg in se2.get('story_groups', []):
                        for st in sg.get('stories', []):
                            for sc in st.get('scenarios', []):
                                tm = sc.get('test_method')
                                if tm:
                                    old_map[tm] = {
                                        'old_story': st['name'],
                                        'old_name': sc['name'],
                                        'steps': sc.get('steps', ''),
                                        'background': sc.get('background', []),
                                    }

print(f'Old sub-epic has {len(old_map)} scenarios with test_methods\n')

# Walk new sub-epic
has_old_steps = 0
no_old_steps = 0
no_test_method = 0

for e in g['epics']:
    for se in e.get('sub_epics', []):
        if se.get('name') == 'Perform Action':
            for se2 in se.get('sub_epics', []):
                if se2.get('name') == 'Synchronize Diagram by Domain':
                    for se3 in se2.get('sub_epics', []):
                        print(f'=== {se3["name"]} ===')
                        for sg in se3.get('story_groups', []):
                            for st in sg.get('stories', []):
                                print(f'\n  {st["name"]}:')
                                for sc in st.get('scenarios', []):
                                    tm = sc.get('test_method')
                                    new_name = sc['name']
                                    
                                    if not tm:
                                        no_test_method += 1
                                        print(f'    [NO TEST] {new_name[:60]}')
                                        continue
                                    
                                    old = old_map.get(tm)
                                    if old and old['steps']:
                                        has_old_steps += 1
                                        # Show first 2 steps
                                        steps_preview = old['steps'][:120].replace('\n', ' | ')
                                        same_story = old['old_story'] == st['name']
                                        moved = '' if same_story else f' (from "{old["old_story"][:30]}")'
                                        print(f'    [HAS STEPS]{moved} {new_name[:55]}')
                                        print(f'               {steps_preview}...')
                                    else:
                                        no_old_steps += 1
                                        print(f'    [UNMAPPED]  {new_name[:60]}')
                        print()

print(f'\n--- Summary ---')
print(f'  {has_old_steps} scenarios have old steps to restore')
print(f'  {no_old_steps} scenarios from unmapped test classes (no old steps exist)')
print(f'  {no_test_method} scenarios with no test_method yet (newly added patterns)')
print(f'  Total: {has_old_steps + no_old_steps + no_test_method}')
