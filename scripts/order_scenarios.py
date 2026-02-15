"""
Reorder scenarios so consistent patterns come first (same order across all domains),
domain-unique scenarios come after.

Consistent pattern order (shared across 2+ domains):
  1. Render/Report/Update with default layout / core operation
  2. Parent spans all child... horizontally
  3. Sibling... do not overlap horizontally
  4. Re-render with saved layout data preserves...
  5. Render completes and writes valid DrawIO file...
  6. All cells have required styles...
  7. Render with no... defined produces fallback
  ---
  For Report:
  1. No changes reported when diagram matches original...
  2. ...added in diagram detected as new in report
  3. ...removed from diagram detected as removed in report
  4. ...moved between... detected as move not new plus removed
  5. ...renamed in diagram detected as rename in report
  6. ...assigned to parent by position
  7. Report roundtrips through JSON for...
  8. Report lists exact fuzzy new and removed...
  ---
  For Update:
  1. Apply... changes from report updates story graph
  2. Apply... move transfers between... preserving data
  3. Moved... preserved when parent removed from diagram
  4. Unmoved... removed with parent when parent removed
  5. Renamed... in diagram updates name in story graph
  6. New... in diagram creates it in story graph
  7. Update preserves original... for matched...
  8. End-to-end render then report then update for...

  Then unique scenarios after.
"""
import json, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
STORY_GRAPH_PATH = Path(__file__).parent.parent / 'docs' / 'story' / 'story-graph.json'

# Priority patterns: lower number = earlier in list
# Scenarios matching these fragments get sorted to the top in this order
RENDER_PRIORITY = [
    'with default layout',
    'Parent epic spans',
    'Parent sub-epic spans',
    'Sibling',
    'do not overlap',
    'Re-render with saved layout',
    'Render completes and writes',
    'valid DrawIO file',
    'All epic and sub-epic cells have required',
    'All increment lane cells have required',
    'required styles',
    'Render with no',
    'produces outline',
    'produces story without',
]

REPORT_PRIORITY = [
    'No changes reported when diagram matches',
    'added in diagram detected as new',
    'removed from diagram detected as removed',
    'moved between',
    'detected as move not new',
    'renamed in diagram detected as rename',
    'assigned to',
    'by position',
    'by vertical position',
    'by Y position',
    'Report roundtrips through JSON',
    'Report lists exact fuzzy',
    'Report includes removed',
]

UPDATE_PRIORITY = [
    'Apply',
    'changes from report updates',
    'move transfers between',
    'preserving data',
    'Moved',
    'preserved when',
    'removed from diagram',
    'Unmoved',
    'removed with',
    'Renamed',
    'updates name in story graph',
    'updates correctly in story graph',
    'New',
    'creates it in story graph',
    'creates it and transfers',
    'Update preserves original',
    'Merge preserves',
    'End-to-end render then report then update',
]


def get_priority(scenario_name, priority_list):
    """Return sort key: matched pattern index (consistent), or 999 (unique)."""
    name = scenario_name
    for i, pattern in enumerate(priority_list):
        if pattern.lower() in name.lower():
            return i
    return 999


def classify_operation(story_name):
    """Determine if story is render, report, or update."""
    ln = story_name.lower()
    if 'render' in ln:
        return 'render'
    elif 'report' in ln:
        return 'report'
    elif 'update' in ln:
        return 'update'
    return 'other'


def sort_scenarios(story):
    """Sort scenarios: consistent patterns first, unique after."""
    op = classify_operation(story['name'])
    if op == 'render':
        priority_list = RENDER_PRIORITY
    elif op == 'report':
        priority_list = REPORT_PRIORITY
    elif op == 'update':
        priority_list = UPDATE_PRIORITY
    else:
        return

    scenarios = story.get('scenarios', [])

    # Sort by priority (stable sort preserves relative order within same priority)
    scenarios.sort(key=lambda sc: get_priority(sc.get('name', ''), priority_list))

    # Renumber
    for i, sc in enumerate(scenarios, 1):
        sc['sequential_order'] = float(i)

    # Find the split point between consistent and unique
    split = 0
    for sc in scenarios:
        if get_priority(sc.get('name', ''), priority_list) < 999:
            split += 1
        else:
            break

    return split


def main():
    g = json.loads(STORY_GRAPH_PATH.read_text(encoding='utf-8'))

    for e in g['epics']:
        for se in e.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == 'Synchronize Diagram by Domain':
                        for se3 in se2.get('sub_epics', []):
                            print(f'\n=== {se3["name"]} ===')
                            for sg in se3.get('story_groups', []):
                                for st in sg.get('stories', []):
                                    split = sort_scenarios(st)
                                    total = len(st.get('scenarios', []))
                                    print(f'\n  {st["name"]} ({split} consistent + {total - split} unique = {total})')
                                    for i, sc in enumerate(st.get('scenarios', []), 1):
                                        marker = '  ' if i <= split else ' *'
                                        print(f'   {marker} {i:2d}. {sc["name"][:75]}')

    STORY_GRAPH_PATH.write_text(json.dumps(g, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'\nWrote to {STORY_GRAPH_PATH}')


if __name__ == '__main__':
    main()
