"""Verify dynamic Y positioning and parent sub-epic rendering."""
import sys
sys.path.insert(0, r'C:\dev\agile_bots\src')

from synchronizers.story_io.story_io_renderer import DrawIORenderer
from pathlib import Path
import json
import xml.etree.ElementTree as ET
import re

with open(r'C:\dev\agile_bots\docs\story\story-graph.json', 'r', encoding='utf-8') as f:
    graph = json.load(f)

renderer = DrawIORenderer()
output_path = Path(r'C:\dev\agile_bots\_test_render_output.drawio')
result = renderer.render_outline(graph, output_path)
print(f"Render result: {result['summary']}")

tree = ET.parse(str(output_path))
root = tree.getroot()

# Collect all green (sub-epic) boxes with their Y positions
sub_epics = []
for cell in root.iter('mxCell'):
    style = cell.get('style', '')
    value = cell.get('value', '')
    if 'fillColor=#d5e8d4' in style:
        geom = cell.find('mxGeometry')
        y = float(geom.get('y', 0)) if geom is not None else 0
        x = float(geom.get('x', 0)) if geom is not None else 0
        w = float(geom.get('width', 0)) if geom is not None else 0
        name = re.search(r'>([^<]+)<', value)
        name = name.group(1) if name else value[:50]
        sub_epics.append((name, y, x, w))

# Sort by Y then X
sub_epics.sort(key=lambda s: (s[1], s[2]))

print(f"\nSub-epics by Y position ({len(sub_epics)}):")
current_y = None
for name, y, x, w in sub_epics:
    if current_y != y:
        print(f"\n  Y={y}:")
        current_y = y
    print(f"    {name} (x={x}, w={w:.0f})")

# Count stories
stories = []
for cell in root.iter('mxCell'):
    style = cell.get('style', '')
    if 'fillColor=#fff2cc' in style:
        geom = cell.find('mxGeometry')
        y = float(geom.get('y', 0)) if geom is not None else 0
        stories.append(y)

if stories:
    print(f"\nStories: {len(stories)} (Y range: {min(stories):.0f} - {max(stories):.0f})")
    y_counts = {}
    for y in stories:
        y_counts[y] = y_counts.get(y, 0) + 1
    for y in sorted(y_counts):
        print(f"  Y={y}: {y_counts[y]} stories")
