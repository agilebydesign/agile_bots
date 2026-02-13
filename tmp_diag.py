"""Diagnose story misassignment after render+load round-trip."""
import sys, json
sys.path.insert(0, 'src')

from pathlib import Path
from synchronizers.story_io.drawio_story_map import DrawIOStoryMap
from synchronizers.story_io.drawio_story_node_serializer import DrawIOStoryNodeSerializer
from synchronizers.story_io.layout_data import LayoutData
from story_graph.nodes import StoryMap

sg_path = Path('docs/story/story-graph.json')
out_path = Path('docs/story/prioritization/story-map-increments.drawio')

graph_data = json.loads(sg_path.read_text(encoding='utf-8'))
story_map = StoryMap(graph_data)

# Build original parent map from story_map
orig_parent = {}
def collect_stories(se):
    for story in se.stories:
        orig_parent[story.name] = se.name
    for nested in se.sub_epics:
        collect_stories(nested)

for epic in story_map.epics:
    for se in epic.sub_epics:
        collect_stories(se)

# Load the rendered diagram
dm = DrawIOStoryMap.load(out_path)

# Build extracted parent map
ext_parent = {}
for se in dm.get_sub_epics():
    for story in se.get_all_stories_recursive():
        ext_parent[story.name] = se.name

# Find mismatches
mismatches = []
for name, orig_se in sorted(orig_parent.items()):
    ext_se = ext_parent.get(name)
    if ext_se != orig_se:
        mismatches.append((name, orig_se, ext_se))

print(f"Total stories in original: {len(orig_parent)}")
print(f"Total stories in extracted: {len(ext_parent)}")
print(f"Misassigned: {len(mismatches)}")
for name, orig, ext in mismatches[:30]:
    print(f"  '{name}':  ORIG='{orig}'  ->  EXT='{ext}'")
