import sys
from pathlib import Path

sys.path.insert(0, 'c:/dev/agile_bots/src')
from synchronizers.story_scenarios import StoryScenariosSynchronizer

synchronizer = StoryScenariosSynchronizer()

input_json = Path('c:/dev/agile_bots_demo/us_wires/docs/story/story-graph.json')
output_dir = Path('c:/dev/agile_bots_demo/us_wires/docs/story/scenarios')

print(f'Rendering scenarios from: {input_json}')
print(f'Output directory: {output_dir}')

result = synchronizer.render(input_json, output_dir)

print(f"\nRendered {result['summary'].get('created', 0)} new scenarios")
print(f"Updated {result['summary'].get('updated', 0)} existing scenarios")
print(f"Deleted {result['summary'].get('deleted', 0)} obsolete scenarios")
print('Done!')
