"""Check which scenarios have steps and which are empty."""
import json, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
g = json.loads(Path('docs/story/story-graph.json').read_text(encoding='utf-8'))

has_steps = 0
no_steps = 0
no_test = 0

for e in g['epics']:
    for se in e.get('sub_epics', []):
        if se.get('name') == 'Perform Action':
            for se2 in se.get('sub_epics', []):
                if se2.get('name') == 'Synchronize Diagram by Domain':
                    for se3 in se2.get('sub_epics', []):
                        print(f'\n=== {se3["name"]} ===')
                        for sg in se3.get('story_groups', []):
                            for st in sg.get('stories', []):
                                print(f'\n  {st["name"]}:')
                                for sc in st.get('scenarios', []):
                                    steps = sc.get('steps', '')
                                    tm = sc.get('test_method')
                                    has = bool(steps and steps.strip())
                                    marker = 'OK' if has else 'EMPTY'
                                    test_marker = '' if tm else ' (no test_method)'
                                    if has:
                                        has_steps += 1
                                    else:
                                        no_steps += 1
                                    if not tm:
                                        no_test += 1
                                    print(f'    [{marker}]{test_marker} {sc["name"][:65]}')

print(f'\n--- {has_steps} with steps, {no_steps} empty, {no_test} missing test_method ---')
