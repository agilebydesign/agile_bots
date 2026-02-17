"""
Map test methods to scenarios: each test_method = one scenario.
Extract all test methods from mapped classes and create scenarios in the new stories.
Replaces any existing scenarios with the complete set from the test file.

Source: test_render_drawio_diagrams.py
Target: "Synchronize Diagram by Domain" sub-epic stories
"""
import json
import re
import sys
from pathlib import Path

STORY_GRAPH_PATH = Path(__file__).parent.parent / 'docs' / 'story' / 'story-graph.json'
TEST_FILE = Path(__file__).parent.parent / 'test' / 'invoke_bot' / 'perform_action' / 'test_render_drawio_diagrams.py'
NEW_SUB_EPIC = 'Synchronize Diagram by Domain'


def extract_test_methods(content, class_name):
    """Extract test method names and first-line docstrings from a class."""
    pattern = rf'^class {re.escape(class_name)}[\s\S]*?(?=\nclass |\Z)'
    match = re.search(pattern, content, re.MULTILINE)
    if not match:
        return []

    class_block = match.group(0)
    methods = []

    # Find all test methods
    for m in re.finditer(r'def (test_\w+)\(self[^)]*\):', class_block):
        method_name = m.group(1)
        # Try to get docstring
        after = class_block[m.end():]
        doc_match = re.match(r'\s*"""(.*?)"""', after, re.DOTALL)
        if doc_match:
            docstring = doc_match.group(1).strip().split('\n')[0].strip()
        else:
            docstring = None
        methods.append((method_name, docstring))

    return methods


def method_to_scenario_name(method_name, docstring):
    """Convert test method to readable scenario name."""
    if docstring:
        return docstring
    # Fallback: convert method name
    name = method_name
    if name.startswith('test_'):
        name = name[5:]
    return name.replace('_', ' ').capitalize()


# Complete mapping: old_class -> new_story (target test_class)
# For split classes, a filter function decides which methods go where
CLASS_TO_STORY = [
    # --- Group 1: Epics and Sub-Epics ---
    ('TestRenderStoryMapNestedSubEpics', 'Render epic and sub-epic hierarchy', None),
    ('TestDomainModelDynamicYPositioning', 'Render epic and sub-epic hierarchy',
     lambda m: any(k in m for k in ['nested', 'flat_graph', '4_level', 'sub_epic_y', 'parent_and_leaf'])),
    ('TestDiagramVisualIntegrity', 'Render epic and sub-epic hierarchy',
     lambda m: any(k in m for k in ['epic_horizontal', 'sub_epic_overlap', 'sub_epic_cells', 'epic_cells', 'nested_container', 'containers_horizontal'])),
    ('TestRenamePairingByIdType', 'Report epic and sub-epic changes', None),
    ('TestUpdateGraphFromStoryMap', 'Update epics and sub-epics from diagram',
     lambda m: any(k in m for k in ['extract_outline', 'update_report_lists', 'story_map_updated', 'renamed_or_reordered', 'deleted_nodes', 'sync_persists', 'deleted_epic', 'deleted_sub_epic', 'empty_or_malformed'])),

    # --- Group 2: Stories and Actors ---
    ('TestDomainModelDynamicYPositioning', 'Render stories and actors',
     lambda m: any(k in m for k in ['story_y', 'stories_positioned', 'actor'])),
    ('TestDiagramVisualIntegrity', 'Render stories and actors',
     lambda m: any(k in m for k in ['story_cells', 'actor_cells', 'stories_do_not_overlap', 'story_font', 'story_text', 'actor_font', 'actor_text', 'story_overlap'])),
    ('TestRenderStoryMapWithAcceptanceCriteria', 'Render stories and actors', None),
    ('TestStoryMoveDetection', 'Report story moves between parents', None),
    ('TestAcceptanceCriteriaDelta', 'Report acceptance criteria changes',
     lambda m: any(k in m for k in ['no_ac_changes', 'added_ac', 'removed_ac', 'ac_changes_roundtrip', 'ac_moved_between'])),
    ('TestUpdateGraphFromStoryMap', 'Update stories and acceptance criteria from diagram',
     lambda m: any(k in m for k in ['moved_story', 'single_story_deleted'])),
    ('TestUpdateFromDiagramMoveBeforeRemove', 'Update stories and acceptance criteria from diagram', None),
    ('TestUpdateStoryGraphFromMapAcceptanceCriteria', 'Update stories and acceptance criteria from diagram',
     lambda m: any(k in m for k in ['merge_preserves', 'extract_exploration'])),
    ('TestAcceptanceCriteriaDelta', 'Update stories and acceptance criteria from diagram',
     lambda m: any(k in m for k in ['apply_ac', 'end_to_end_ac', 'story_split'])),
    ('TestUpdateStoryGraphFromMapAcceptanceCriteria', 'Report acceptance criteria changes',
     lambda m: any(k in m for k in ['when_then', 'added_or_removed', 'ac_cells_assigned', 'ac_box_text_not'])),

    # --- Group 3: Increments ---
    ('TestRenderStoryMapIncrements', 'Render increment lanes', None),
    ('TestUserCreatedIncrementLaneDetection', 'Report increment changes', None),
    ('TestIncrementReportTwoPassExtraction', 'Report increment changes', None),
    ('TestUpdateGraphFromMapIncrements', 'Report increment changes',
     lambda m: any(k in m for k in ['extract_increments', 'update_report_generated', 'story_moved_between', 'known_inserting', 'story_not_within'])),
    ('TestIncrementRemovalMoveAndOrderApply', 'Update increments from diagram', None),
    ('TestUpdateGraphFromMapIncrements', 'Update increments from diagram',
     lambda m: any(k in m for k in ['merge_preserves', 'new_increment_lane', 'removed_increment', 'renamed_increment', 'extra_extracted'])),
]


def find_story_in_graph(graph_data, story_name):
    """Find a story dict by name in the new sub-epic."""
    for epic in graph_data.get('epics', []):
        for se in epic.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == NEW_SUB_EPIC:
                        for se3 in se2.get('sub_epics', []):
                            for sg in se3.get('story_groups', []):
                                for story in sg.get('stories', []):
                                    if story['name'] == story_name:
                                        return story
    return None


def main():
    print(f'Loading test file: {TEST_FILE.name}')
    content = TEST_FILE.read_text(encoding='utf-8')

    print(f'Loading story graph: {STORY_GRAPH_PATH}')
    graph_data = json.loads(STORY_GRAPH_PATH.read_text(encoding='utf-8'))

    # Clear existing scenarios on all new stories first
    for epic in graph_data.get('epics', []):
        for se in epic.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == NEW_SUB_EPIC:
                        for se3 in se2.get('sub_epics', []):
                            for sg in se3.get('story_groups', []):
                                for story in sg.get('stories', []):
                                    story['scenarios'] = []

    # Process each class -> story mapping
    for class_name, target_story_name, filter_fn in CLASS_TO_STORY:
        methods = extract_test_methods(content, class_name)
        if not methods:
            print(f'\n  WARNING: No methods found in {class_name}')
            continue

        story = find_story_in_graph(graph_data, target_story_name)
        if not story:
            print(f'\n  ERROR: Story "{target_story_name}" not found')
            continue

        existing_methods = {s.get('test_method') for s in story.get('scenarios', [])}

        added = 0
        for method_name, docstring in methods:
            # Apply filter if provided
            if filter_fn and not filter_fn(method_name):
                continue
            # Skip if already added
            if method_name in existing_methods:
                continue

            order = float(len(story['scenarios']) + 1)
            scenario = {
                'name': method_to_scenario_name(method_name, docstring),
                'sequential_order': order,
                'type': '',
                'background': [],
                'test_method': method_name,
                'steps': '',
            }
            story['scenarios'].append(scenario)
            existing_methods.add(method_name)
            added += 1

        if added:
            print(f'  {class_name} -> "{target_story_name}": +{added} scenarios')

    # Summary
    print('\n--- Final scenario counts ---')
    total = 0
    for epic in graph_data.get('epics', []):
        for se in epic.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == NEW_SUB_EPIC:
                        for se3 in se2.get('sub_epics', []):
                            print(f'\n  {se3["name"]}:')
                            for sg in se3.get('story_groups', []):
                                for story in sg.get('stories', []):
                                    count = len(story.get('scenarios', []))
                                    total += count
                                    print(f'    {count:3d}  {story["name"]} (test_class={story.get("test_class")})')
                                    for sc in story['scenarios']:
                                        print(f'         - {sc["test_method"]}')

    print(f'\n  Total: {total} scenarios')

    STORY_GRAPH_PATH.write_text(
        json.dumps(graph_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'\nWrote to {STORY_GRAPH_PATH}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
