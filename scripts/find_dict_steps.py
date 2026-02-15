import sys, os, json
sys.path.insert(0, 'C:/dev/agile_bots/src')
sys.path.insert(0, 'C:/dev/agile_bots')

with open('C:/dev/agile_bots/docs/story/story-graph.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

from synchronizers.story_scenarios.story_scenarios_synchronizer import extract_stories_from_graph

found = 0
for epic in data['epics']:
    stories = extract_stories_from_graph(epic)
    for story in stories:
        for s in story.get('scenarios', []) + story.get('scenario_outlines', []):
            steps = s.get('steps', [])
            if isinstance(steps, list):
                for step in steps:
                    if isinstance(step, dict):
                        print(f'DICT STEP in scenario "{s["name"]}" of story "{story["name"]}":')
                        print(f'  {json.dumps(step, indent=2)[:200]}')
                        found += 1
                        break
            elif isinstance(steps, str) and steps:
                # Check if any newline-split produces something odd
                pass

print(f"\nTotal scenarios with dict steps: {found}")
