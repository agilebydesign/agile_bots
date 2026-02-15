"""
Distribute scenarios from old sub-epic to new domain-based sub-epic.

For each scenario in the old stories, assign it to the correct new domain story
based on which domain concepts it references. Also adds scenarios from unmapped
test classes (from the plan) that have no existing scenarios.

Mapping rules:
- Scenarios about epic/sub-epic hierarchy rendering -> "Render epic and sub-epic hierarchy"
- Scenarios about rename pairing by cell ID type -> "Report epic and sub-epic changes"
- Scenarios about epic/sub-epic update (add/rename/remove sub-epic) -> "Update epics and sub-epics from diagram"
- Scenarios about story/actor positioning and rendering -> "Render stories and actors"
- Scenarios about story move detection -> "Report story moves between parents"
- Scenarios about AC delta detection -> "Report acceptance criteria changes"
- Scenarios about applying story/AC updates (move-before-remove) -> "Update stories and acceptance criteria from diagram"
- Scenarios about increment lane rendering -> "Render increment lanes"
- Scenarios about increment delta/detection -> "Report increment changes"
- Scenarios about applying increment changes -> "Update increments from diagram"
"""
import json
import copy
from pathlib import Path

STORY_GRAPH_PATH = Path(__file__).parent.parent / 'docs' / 'story' / 'story-graph.json'
OLD_SUB_EPIC_NAME = 'Synchronized Graph with Rendered Diagram Content'
NEW_SUB_EPIC_NAME = 'Synchronize Diagram by Domain'

# Map: (old_story_name, scenario_name) -> new_story_name
# When old_story_name is '*', it means "from any old story matching this scenario name"
SCENARIO_ROUTING = {
    # === "Render story map" scenarios stay with "Render story map" (not moved) ===
    # They're in the old sub-epic which we don't touch.
    # But some should be COPIED to the new domain stories.

    # === "Render story map increments" -> "Render increment lanes" (all) ===
    ('Render story map increments', 'Render increments diagram with stories assigned to increment lanes'): 'Render increment lanes',
    ('Render story map increments', 'Increment lanes ordered by priority with Y positions from outline bottom'): 'Render increment lanes',
    ('Render story map increments', 'Re-render increments with existing LayoutData recomputes lane positions'): 'Render increment lanes',
    ('Render story map increments', 'Render increments completes and summary includes increment count'): 'Render increment lanes',
    ('Render story map increments', 'Increment lane cells styled for extractor detection'): 'Render increment lanes',
    ('Render story map increments', 'Render increments with no increments defined produces outline-only diagram'): 'Render increment lanes',
    ('Render story map increments', 'Actor labels rendered above stories in increment lanes'): 'Render increment lanes',

    # === "Render story map with acceptance criteria" -> "Render stories and actors" (AC rendering is property of stories) ===
    ('Render story map with acceptance criteria', 'Render exploration diagram with AC boxes below stories'): 'Render stories and actors',
    ('Render story map with acceptance criteria', 'AC boxes styled and positioned below story with extracted step text'): 'Render stories and actors',
    ('Render story map with acceptance criteria', 'Re-render exploration with LayoutData preserves story and AC box positions'): 'Render stories and actors',
    ('Render story map with acceptance criteria', 'Exploration render output contains story and AC cells with correct containment'): 'Render stories and actors',
    ('Render story map with acceptance criteria', 'Story with no acceptance criteria renders without AC boxes'): 'Render stories and actors',

    # === "Update graph from story map" -> split across epics/stories update + report ===
    ('Update graph from story map', 'Extract outline assigns stories to sub-epics by containment and sequential order'): 'Update epics and sub-epics from diagram',
    ('Update graph from story map', 'UpdateReport lists exact fuzzy new and removed stories'): 'Report epic and sub-epic changes',
    ('Update graph from story map', 'StoryMap updated from outline diagram applies report changes'): 'Update epics and sub-epics from diagram',
    ('Update graph from story map', 'Renamed or reordered nodes flagged as fuzzy matches in UpdateReport'): 'Report epic and sub-epic changes',
    ('Update graph from story map', 'Deleted nodes listed as removed and large deletions flagged'): 'Report epic and sub-epic changes',
    ('Update graph from story map', 'Sync persists LayoutData alongside diagram'): 'Update epics and sub-epics from diagram',
    ('Update graph from story map', 'Moved story gets recomputed sequential order from new position'): 'Update stories and acceptance criteria from diagram',
    ('Update graph from story map', 'Single story deleted keeps original structure and flags if many missing'): 'Update stories and acceptance criteria from diagram',
    ('Update graph from story map', 'Deleted sub-epic reassigns its stories by position'): 'Update stories and acceptance criteria from diagram',
    ('Update graph from story map', 'Deleted epic removes all children and flags large deletions'): 'Update epics and sub-epics from diagram',
    ('Update graph from story map', 'Extract from empty or malformed DrawIO file produces error'): 'Update epics and sub-epics from diagram',

    # === "Update graph from map increments" -> split across report + update ===
    ('Update graph from map increments', 'Extract increments assigns stories to lanes by Y position with priority from order'): 'Report increment changes',
    ('Update graph from map increments', 'UpdateReport generated for increments view with story-level matches'): 'Report increment changes',
    ('Update graph from map increments', 'Story moved between increments reflected in extracted graph'): 'Report increment changes',
    ('Update graph from map increments', 'Merge preserves original AC and updates story fields with position-based increment matching'): 'Update increments from diagram',
    ('Update graph from map increments', 'New increment lane at bottom appended as new increment'): 'Update increments from diagram',
    ('Update graph from map increments', 'Removed increment lane stays in merged with its original stories'): 'Update increments from diagram',
    ('Update graph from map increments', 'Renamed increment lane updated by position-based matching'): 'Update increments from diagram',
    ('Update graph from map increments', 'Extra extracted lanes appended and fewer lanes leave originals unchanged'): 'Update increments from diagram',
    ('Update graph from map increments', 'KNOWN: inserting lane between existing may misinterpret without stable IDs'): 'Report increment changes',
    ('Update graph from map increments', 'Story not within 100px of any lane remains unassigned in extracted'): 'Report increment changes',

    # === "Update story graph from map acceptance criteria" -> split across report + update ===
    ('Update story graph from map acceptance criteria', 'Extract exploration maps AC boxes to stories by position and containment'): 'Report acceptance criteria changes',
    ('Update story graph from map acceptance criteria', 'When/Then AC text extracted as step descriptions'): 'Report acceptance criteria changes',
    ('Update story graph from map acceptance criteria', 'Merge preserves original AC for matched stories from exploration view'): 'Update stories and acceptance criteria from diagram',
    ('Update story graph from map acceptance criteria', 'Added or removed AC boxes reflected in extracted graph and UpdateReport'): 'Report acceptance criteria changes',
    ('Update story graph from map acceptance criteria', 'AC cells assigned to stories by vertical position below story cells'): 'Report acceptance criteria changes',
    ('Update story graph from map acceptance criteria', 'AC box text not in When/Then format treated as plain acceptance_criteria'): 'Report acceptance criteria changes',
}


def find_sub_epic(graph_data, name):
    """Find a sub-epic by name under Perform Action."""
    for epic in graph_data.get('epics', []):
        for se in epic.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == name:
                        return se2
    return None


def get_stories_dict(sub_epic):
    """Return {story_name: story_dict} for all stories in a sub-epic."""
    result = {}
    for sg in sub_epic.get('story_groups', []):
        for story in sg.get('stories', []):
            result[story['name']] = story
    return result


def main():
    print(f'Loading {STORY_GRAPH_PATH}')
    graph_data = json.loads(STORY_GRAPH_PATH.read_text(encoding='utf-8'))

    old_se = find_sub_epic(graph_data, OLD_SUB_EPIC_NAME)
    new_se = find_sub_epic(graph_data, NEW_SUB_EPIC_NAME)

    if not old_se:
        print(f'ERROR: Could not find "{OLD_SUB_EPIC_NAME}"')
        return 1
    if not new_se:
        print(f'ERROR: Could not find "{NEW_SUB_EPIC_NAME}"')
        return 1

    old_stories = get_stories_dict(old_se)
    new_stories = get_stories_dict(new_se)

    print(f'Old sub-epic: {len(old_stories)} stories')
    print(f'New sub-epic: {len(new_stories)} stories')

    # Distribute scenarios
    moved = 0
    unmapped = 0
    for old_story_name, old_story in old_stories.items():
        for scenario in old_story.get('scenarios', []):
            key = (old_story_name, scenario['name'])
            target_name = SCENARIO_ROUTING.get(key)

            if target_name is None:
                # Not in routing table -- skip (stays in old sub-epic only)
                continue

            if target_name not in new_stories:
                print(f'  WARNING: Target "{target_name}" not found for scenario "{scenario["name"]}"')
                unmapped += 1
                continue

            # Deep copy scenario to new story
            new_scenario = copy.deepcopy(scenario)
            # Clear test_method -- will be reassigned in step 3
            new_scenario.pop('test_method', None)

            target_story = new_stories[target_name]
            existing_names = {s['name'] for s in target_story.get('scenarios', [])}
            if new_scenario['name'] in existing_names:
                continue  # already there (idempotent)

            # Assign new sequential_order
            existing = target_story.get('scenarios', [])
            new_scenario['sequential_order'] = float(len(existing) + 1)
            existing.append(new_scenario)
            moved += 1
            print(f'  {old_story_name} -> {target_name}: "{scenario["name"]}"')

    print(f'\nMoved {moved} scenarios, {unmapped} unmapped')

    # Summary
    print('\nNew story scenario counts:')
    for name, story in new_stories.items():
        count = len(story.get('scenarios', []))
        print(f'  {count:3d}  {name}')

    STORY_GRAPH_PATH.write_text(
        json.dumps(graph_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'\nWrote to {STORY_GRAPH_PATH}')
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
