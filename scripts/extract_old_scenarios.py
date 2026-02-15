"""Extract scenario names from old sub-epic as context for writing new scenarios."""
import json
from pathlib import Path

g = json.loads(Path('docs/story/story-graph.json').read_text(encoding='utf-8'))

for epic in g['epics']:
    for se in epic.get('sub_epics', []):
        for se2 in se.get('sub_epics', []):
            if se2['name'] == 'Synchronized Graph with Rendered Diagram Content':
                for sg in se2.get('story_groups', []):
                    for story in sg.get('stories', []):
                        scenarios = story.get('scenarios', [])
                        print(f'STORY: "{story["name"]}" (test_class={story.get("test_class")}, {len(scenarios)} scenarios)')
                        for sc in scenarios:
                            steps = sc.get('steps', '')
                            if isinstance(steps, str):
                                step_lines = [l for l in steps.split('\n') if l.strip()]
                            else:
                                step_lines = steps
                            print(f'  {sc.get("sequential_order", 0):4.0f}. {sc["name"]}')
                            print(f'       test_method={sc.get("test_method")}')
                            for step in step_lines[:3]:
                                text = step if isinstance(step, str) else step.get('text', '')
                                print(f'       {text[:100]}')
                            if len(step_lines) > 3:
                                print(f'       ... +{len(step_lines)-3} more steps')
                        print()
