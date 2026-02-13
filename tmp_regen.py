"""Render + generate report to verify no false changes."""
import sys, json
sys.path.insert(0, 'src')

from pathlib import Path
from synchronizers.story_io.drawio_story_map import DrawIOStoryMap
from synchronizers.story_io.drawio_story_node_serializer import DrawIOStoryNodeSerializer
from synchronizers.story_io.layout_data import LayoutData
from story_graph.nodes import StoryMap

sg_path = Path('docs/story/story-graph.json')
out_path = Path('docs/story/prioritization/story-map-increments.drawio')
layout_path = out_path.parent / f"{out_path.stem}-layout.json"

graph_data = json.loads(sg_path.read_text(encoding='utf-8'))
story_map = StoryMap(graph_data)
layout_data = LayoutData.load(layout_path) if layout_path.exists() else None
increments_data = graph_data.get('increments', [])

# Step 1: Render
dm = DrawIOStoryMap()
dm.render_increments_from_story_map(story_map, increments_data, layout_data)
xml = DrawIOStoryNodeSerializer.to_drawio_xml(dm._collect_all_nodes())
out_path.write_text(xml, encoding='utf-8')
print("Rendered diagram.")

# Step 2: Load rendered diagram and generate report
dm2 = DrawIOStoryMap.load(out_path)
report = dm2.generate_update_report(story_map)
report_path = out_path.parent / 'story-map-increments-update-report.json'
report.save(report_path)

d = report.to_dict()
print(f"\nReport has_changes: {report.has_changes}")
print(f"Keys in report: {list(d.keys())}")
if report.has_changes:
    print("\n=== CHANGES FOUND (should be empty for clean render) ===")
    print(json.dumps(d, indent=2)[:2000])
else:
    print("\nNo changes - clean round-trip confirmed!")
