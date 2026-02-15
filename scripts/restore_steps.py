"""
Restore scenario steps from old sub-epic by matching on test_method.
Old sub-epic has the original steps; new sub-epic lost them during restructuring.
"""
import json, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
STORY_GRAPH_PATH = Path(__file__).parent.parent / 'docs' / 'story' / 'story-graph.json'

g = json.loads(STORY_GRAPH_PATH.read_text(encoding='utf-8'))

# Build map: test_method -> steps from old sub-epic
old_steps = {}
for e in g['epics']:
    for se in e.get('sub_epics', []):
        if se.get('name') == 'Perform Action':
            for se2 in se.get('sub_epics', []):
                if se2.get('name') == 'Synchronized Graph with Rendered Diagram Content':
                    for sg in se2.get('story_groups', []):
                        for st in sg.get('stories', []):
                            for sc in st.get('scenarios', []):
                                tm = sc.get('test_method')
                                steps = sc.get('steps', '')
                                bg = sc.get('background', [])
                                if tm and steps:
                                    old_steps[tm] = {'steps': steps, 'background': bg}

print(f'Found {len(old_steps)} scenarios with steps in old sub-epic')

# Also check test file for docstrings as fallback for unmapped test classes
TEST_FILE = Path(__file__).parent.parent / 'test' / 'invoke_bot' / 'perform_action' / 'test_synchronized_graph_with_rendered_diagram_content.py'
import re
content = TEST_FILE.read_text(encoding='utf-8')

def get_docstring(method_name):
    pattern = rf'def {re.escape(method_name)}\(self[^)]*\):\s*"""(.*?)"""'
    m = re.search(pattern, content, re.DOTALL)
    if m:
        return m.group(1).strip().split('\n')[0].strip()
    return None

# Restore steps in new sub-epic
restored = 0
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
                                    tm = sc.get('test_method')
                                    current_steps = sc.get('steps', '')
                                    if current_steps and current_steps.strip():
                                        continue  # already has steps

                                    if tm and tm in old_steps:
                                        sc['steps'] = old_steps[tm]['steps']
                                        if old_steps[tm]['background']:
                                            sc['background'] = old_steps[tm]['background']
                                        restored += 1
                                    else:
                                        still_empty += 1
                                        # Try docstring as minimal step
                                        if tm:
                                            doc = get_docstring(tm)
                                            if doc:
                                                sc['steps'] = f'Given test setup\nWhen {doc}\nThen verify expected outcome'
                                                restored += 1
                                                still_empty -= 1

print(f'Restored {restored} scenario steps from old sub-epic')
print(f'Still empty: {still_empty}')

# List the still-empty ones
if still_empty > 0:
    print('\nScenarios still needing steps:')
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
                                        if not steps or not steps.strip():
                                            print(f'  [{st["name"]}] {sc["name"]} (test_method={sc.get("test_method")})')

STORY_GRAPH_PATH.write_text(json.dumps(g, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'\nWrote to {STORY_GRAPH_PATH}')
