import sys; sys.path.insert(0, 'src')
import json
from story_graph.nodes import StoryMap
from synchronizers.story_io.drawio_story_map import DrawIOStoryMap

with open('docs/story/story-graph.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

sm = StoryMap(data)
filtered = sm.filter_by_name('Scope Files')

drawio_map = DrawIOStoryMap()
summary = drawio_map.render_from_story_map(filtered, None)

# Check for duplicate stories
stories = drawio_map.get_stories()
print(f'Stories from get_stories(): {len(stories)}')
seen = {}
for s in stories:
    cid = s.cell_id
    if cid in seen:
        print(f'  DUPLICATE cell_id: {cid} (name={s.name})')
    seen[cid] = s.name

# Now simulate exploration render
domain_stories = drawio_map._collect_domain_stories(filtered, scope=None)
print(f'\nDomain stories with AC:')
for name, ds in domain_stories.items():
    ac = getattr(ds, 'acceptance_criteria', []) or []
    if ac:
        print(f'  {name}: {len(ac)} AC')

# Check how many drawio stories match
matches = 0
for ds in stories:
    domain = domain_stories.get(ds.name)
    if domain and domain.has_acceptance_criteria():
        matches += 1
        print(f'  MATCH: {ds.name} (cell_id={ds.cell_id})')
print(f'\nTotal AC render calls would be: {matches}')
