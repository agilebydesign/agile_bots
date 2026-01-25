#!/usr/bin/env python3
"""
One-time migration script to add behavior and file_link fields to story-graph.json
"""
import sys
import os
import json
sys.path.insert(0, 'src')

from pathlib import Path
from story_graph.nodes import StoryMap

# Load story graph JSON directly
print("Loading story graph...")
story_graph_path = Path('docs/stories/story-graph.json')
with open(story_graph_path, 'r', encoding='utf-8') as f:
    story_graph_data = json.load(f)

# Create StoryMap (without bot, we can't calculate file_links but we can calculate behaviors)
story_map = StoryMap(story_graph_data, bot=None)

# Calculate missing behaviors (skip file_links since we don't have bot)
print("Calculating missing behaviors...")
for epic in story_map._epics_list:
    for node in story_map.walk(epic):
        from story_graph.nodes import Story
        if isinstance(node, Story) and node.behavior is None:
            if not node.has_acceptance_criteria():
                node.behavior = 'exploration'
            elif not node.has_scenarios():
                node.behavior = 'scenarios'
            elif not node.has_tests():
                node.behavior = 'tests'
            else:
                node.behavior = 'code'

# Calculate epic/sub-epic behaviors
for epic in story_map._epics_list:
    if epic.behavior is None:
        story_map.recalculate_behavior_for_node(epic)

# Update story graph dict
story_map.story_graph['epics'] = [story_map._epic_to_dict(e) for e in story_map._epics_list]

# Save
print("Saving story graph with behaviors...")
with open(story_graph_path, 'w', encoding='utf-8') as f:
    json.dump(story_map.story_graph, f, indent=2, ensure_ascii=False)

print("Done! Migration complete! All nodes now have behavior fields.")
