"""
Write consistent Given/When/Then steps for all 98 scenarios.
Same pattern structure across domains, varying only by domain concepts.

Step patterns by operation:
  RENDER: Given {StoryMap} has {entities} / When renders / Then {layout assertions}
  REPORT: Given {diagram} modified / And original exists / When generateUpdateReport / Then {detection assertions}
  UPDATE: Given {UpdateReport} generated / When apply to graph / Then {graph change assertions}
"""
import json, sys, io, re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
STORY_GRAPH_PATH = Path(__file__).parent.parent / 'docs' / 'story' / 'story-graph.json'

# Domain-specific concept substitutions
DOMAIN = {
    'Synchronize Epics and Sub-Epics': {
        'entities': '{DrawIOEpic} and {DrawIOSubEpic}',
        'entity': '{DrawIOSubEpic}',
        'entity_name': 'sub-epic',
        'parent': '{DrawIOEpic}',
        'parent_name': 'epic',
        'children': '{DrawIOSubEpic}',
        'diagram_type': 'outline',
        'render_action': 'renders outline from {StoryMap}',
    },
    'Synchronize Stories and Actors': {
        'entities': '{DrawIOStory} and actor labels',
        'entity': '{DrawIOStory}',
        'entity_name': 'story',
        'parent': '{DrawIOSubEpic}',
        'parent_name': 'sub-epic',
        'children': '{DrawIOStory}',
        'diagram_type': 'outline',
        'render_action': 'renders outline from {StoryMap}',
    },
    'Synchronize Increments': {
        'entities': 'increment lanes with {DrawIOStory} assigned',
        'entity': 'increment lane',
        'entity_name': 'increment',
        'parent': 'increment lane',
        'parent_name': 'increment',
        'children': '{DrawIOStory}',
        'diagram_type': 'increments',
        'render_action': 'renders increments from {StoryMap}',
    },
}

# AC-specific overrides for Stories and Actors AC stories
AC_DOMAIN = {
    'entities': '{DrawIOStory} with acceptance_criteria',
    'entity': 'AC {DrawIOElement}',
    'entity_name': 'acceptance criteria',
    'parent': '{DrawIOStory}',
    'parent_name': 'story',
    'children': 'AC {DrawIOElement} boxes',
    'diagram_type': 'exploration',
    'render_action': 'renders exploration from {StoryMap}',
}


def is_ac_story(story_name):
    return 'acceptance criteria' in story_name.lower()


def get_domain(sub_epic_name, story_name):
    if is_ac_story(story_name):
        return AC_DOMAIN
    return DOMAIN.get(sub_epic_name, {})


# ============================================================================
# STEP TEMPLATES keyed by scenario name patterns
# ============================================================================

def make_steps(scenario_name, story_name, domain):
    """Generate consistent steps based on scenario name and domain."""
    d = domain
    sn = scenario_name.lower()
    ent = d.get('entity_name', 'entity')
    ENT = d.get('entity', '{Entity}')
    parent = d.get('parent_name', 'parent')
    PARENT = d.get('parent', '{Parent}')

    # === RENDER PATTERNS ===
    if 'with default layout' in sn:
        return (f'Given {{StoryMap}} has {{StoryMap.epics}} with {d["entities"]}\n'
                f'And no {{LayoutData}} exists for this diagram\n'
                f'When {{DrawIOStoryMap}} {d["render_action"]}\n'
                f'Then {{DrawIOStoryMap}} positions {d["entities"]} with correct layout\n'
                f'And output is valid DrawIO XML')

    if 'parent' in sn and 'spans all child' in sn:
        return (f'Given {{StoryMap}} has {PARENT} containing multiple {d["children"]}\n'
                f'When {{DrawIOStoryMap}} {d["render_action"]}\n'
                f'Then {PARENT} horizontal boundary encompasses all {d["children"]}')

    if 'sibling' in sn and 'do not overlap' in sn:
        return (f'Given {{StoryMap}} has multiple sibling {d["children"]} under same parent\n'
                f'When {{DrawIOStoryMap}} {d["render_action"]}\n'
                f'Then no two sibling {d["children"]} have overlapping horizontal boundaries')

    if 're-render with saved layout' in sn:
        return (f'Given {{StoryMap}} has {d["entities"]}\n'
                f'And {{LayoutData}} exists with saved positions from previous render\n'
                f'When {{DrawIOStoryMap}} {d["render_action"]}\n'
                f'Then {{DrawIOStoryMap}} applies {{LayoutData}} saved positions for {d["entities"]}')

    if 'render completes and writes' in sn:
        return (f'Given {{StoryMap}} has {d["entities"]}\n'
                f'When {{DrawIOStoryMap}} {d["render_action"]}\n'
                f'Then {{DrawIOStoryMap}} is written to specified file path\n'
                f'And summary reports correct counts and diagram_generated true')

    if 'all' in sn and 'cells have required styles' in sn:
        return (f'Given {{StoryMap}} has {d["entities"]}\n'
                f'When {{DrawIOStoryMap}} {d["render_action"]}\n'
                f'Then all {ENT} cells have whiteSpace wrap and html enabled and explicit fontSize')

    if 'render with no' in sn and ('produces' in sn or 'without' in sn):
        return (f'Given {{StoryMap}} has no {ent} defined\n'
                f'When {{DrawIOStoryMap}} {d["render_action"]}\n'
                f'Then {{DrawIOStoryMap}} renders without {ent} elements')

    # === REPORT PATTERNS ===
    if 'no changes reported when diagram matches' in sn:
        return (f'Given {{DrawIOStoryMap}} has been rendered from {{StoryMap}}\n'
                f'And no {ent} changes made to diagram\n'
                f'When {{DrawIOStoryMap}}.generateUpdateReport({{StoryMap}}) runs\n'
                f'Then {{UpdateReport}} reports zero {ent} changes')

    if 'added in diagram detected as new' in sn:
        return (f'Given {{DrawIOStoryMap}} has a new {ENT} added by user\n'
                f'And original {{StoryMap}} does not have this {ent}\n'
                f'When {{DrawIOStoryMap}}.generateUpdateReport({{StoryMap}}) runs\n'
                f'Then {{UpdateReport}} lists the {ent} as new')

    if 'removed from diagram detected as removed' in sn:
        return (f'Given {{DrawIOStoryMap}} has had a {ENT} removed by user\n'
                f'And original {{StoryMap}} has this {ent}\n'
                f'When {{DrawIOStoryMap}}.generateUpdateReport({{StoryMap}}) runs\n'
                f'Then {{UpdateReport}} lists the {ent} as removed')

    if 'moved between' in sn and 'detected as move' in sn:
        return (f'Given {ENT} has been moved from one {parent} to another in {{DrawIOStoryMap}}\n'
                f'And original {{StoryMap}} has this {ent} under the original {parent}\n'
                f'When {{DrawIOStoryMap}}.generateUpdateReport({{StoryMap}}) runs\n'
                f'Then {{UpdateReport}} detects the {ent} as moved not new plus removed')

    if 'renamed in diagram detected as rename' in sn:
        return (f'Given {ENT} has been renamed in {{DrawIOStoryMap}}\n'
                f'And original {{StoryMap}} has the original name\n'
                f'When {{DrawIOStoryMap}}.generateUpdateReport({{StoryMap}}) runs\n'
                f'Then {{UpdateReport}} pairs the renamed {ent} as a rename match')

    if 'assigned to' in sn and 'by' in sn and 'position' in sn:
        return (f'Given {{DrawIOStoryMap}} has {ENT} elements positioned below {d["parent"]}\n'
                f'When {{DrawIOStoryMap}} extracts from diagram\n'
                f'Then each {ENT} is assigned to its {parent} by vertical position')

    if 'report roundtrips through json' in sn:
        return (f'Given {{UpdateReport}} has {ent} changes (added, removed, moved)\n'
                f'When {{UpdateReport}}.to_dict() serializes to JSON\n'
                f'And {{UpdateReport}}.from_dict() restores from JSON\n'
                f'Then all {ent} change fields survive the roundtrip')

    if 'report lists exact fuzzy' in sn:
        return (f'Given {{DrawIOStoryMap}} has been extracted from diagram\n'
                f'And original {{StoryMap}} exists with known {ent} names\n'
                f'When {{DrawIOStoryMap}}.generateUpdateReport({{StoryMap}}) runs\n'
                f'Then {{UpdateReport}} lists exact matches and fuzzy matches and new and removed {ent}s')

    if 'report includes removed' in sn:
        return (f'Given {{DrawIOStoryMap}} has fewer {ent}s than original\n'
                f'When {{DrawIOStoryMap}}.generateUpdateReport({{StoryMap}}) runs\n'
                f'Then {{UpdateReport}} includes removed {ent}s and updated order')

    # === UPDATE PATTERNS ===
    if 'apply' in sn and 'changes from report updates' in sn:
        return (f'Given {{UpdateReport}} has been generated with {ent} changes\n'
                f'When {{UpdateReport}} is applied to story graph\n'
                f'Then story graph reflects the {ent} additions and removals from {{UpdateReport}}')

    if 'apply' in sn and 'move transfers between' in sn:
        return (f'Given {{UpdateReport}} contains a {ent} move from one {parent} to another\n'
                f'When move is applied to story graph\n'
                f'Then {ent} is removed from source {parent} and added to target {parent}\n'
                f'And all {ent} fields are preserved')

    if 'apply' in sn and 'preserves all' in sn:
        return (f'Given {ENT} is being moved via {{UpdateReport}}\n'
                f'When move is applied to story graph\n'
                f'Then all {ent} fields including acceptance_criteria and scenarios are preserved')

    if 'moved' in sn and 'preserved when' in sn and 'removed' in sn:
        return (f'Given {ENT} has been moved to another {parent} in {{DrawIOStoryMap}}\n'
                f'And the original {parent} is being removed\n'
                f'When {{UpdateReport}} is applied (moves before removes)\n'
                f'Then moved {ent} survives the {parent} removal')

    if 'unmoved' in sn and 'removed with' in sn:
        return (f'Given {ENT} was NOT moved to another {parent}\n'
                f'And the {parent} is being removed\n'
                f'When {{UpdateReport}} is applied\n'
                f'Then unmoved {ent} is removed along with its {parent}')

    if 'renamed' in sn and 'updates name in story graph' in sn:
        return (f'Given {ENT} has been renamed in {{DrawIOStoryMap}}\n'
                f'When {{UpdateReport}} is applied to story graph\n'
                f'Then story graph updates the {ent} name to match diagram')

    if 'updates correctly in story graph' in sn:
        return (f'Given {ENT} is being moved to a renamed {parent}\n'
                f'When {{UpdateReport}} is applied to story graph\n'
                f'Then move resolves correctly to the renamed {parent}')

    if 'new' in sn and 'creates it in story graph' in sn:
        return (f'Given {{DrawIOStoryMap}} has a new {ent} not in original {{StoryMap}}\n'
                f'When {{UpdateReport}} is applied to story graph\n'
                f'Then story graph creates the new {ent}')

    if 'creates it and transfers' in sn:
        return (f'Given {ENT} is being moved to a {parent} that does not exist yet\n'
                f'When {{UpdateReport}} is applied to story graph\n'
                f'Then story graph creates the new {parent} and transfers the {ent}')

    if 'update preserves original' in sn or 'merge preserves' in sn:
        return (f'Given {{UpdateReport}} has matched {ent}s between diagram and story graph\n'
                f'When {{UpdateReport}} is applied to story graph\n'
                f'Then original acceptance_criteria and scenarios are preserved for matched {ent}s')

    if 'end-to-end render then report then update' in sn:
        return (f'Given {{StoryMap}} has {d["entities"]}\n'
                f'When {{DrawIOStoryMap}} renders {d["diagram_type"]} from {{StoryMap}}\n'
                f'And user modifies {ent}s in diagram\n'
                f'And {{DrawIOStoryMap}}.generateUpdateReport({{StoryMap}}) runs\n'
                f'And {{UpdateReport}} is applied to story graph\n'
                f'Then story graph reflects all {ent} changes from diagram')

    # === DOMAIN-UNIQUE SCENARIOS (no cross-domain pattern) ===
    # Return None to keep existing steps or leave empty
    return None


def main():
    g = json.loads(STORY_GRAPH_PATH.read_text(encoding='utf-8'))

    written = 0
    skipped = 0
    kept_old = 0

    # Also load old steps for fallback
    old_steps = {}
    for e in g['epics']:
        for se in e.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == 'Synchronized Graph with Rendered Diagram Content':
                        for sg in se2.get('story_groups', []):
                            for st in sg.get('stories', []):
                                for sc in st.get('scenarios', []):
                                    tm = sc.get('test_method')
                                    if tm and sc.get('steps'):
                                        old_steps[tm] = sc['steps']

    for e in g['epics']:
        for se in e.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == 'Synchronize Diagram by Domain':
                        for se3 in se2.get('sub_epics', []):
                            domain = get_domain(se3['name'], '')
                            print(f'\n=== {se3["name"]} ===')
                            for sg in se3.get('story_groups', []):
                                for st in sg.get('stories', []):
                                    d = get_domain(se3['name'], st['name'])
                                    print(f'\n  {st["name"]}:')
                                    for sc in st.get('scenarios', []):
                                        steps = make_steps(sc['name'], st['name'], d)
                                        if steps:
                                            sc['steps'] = steps
                                            written += 1
                                            print(f'    [WROTE] {sc["name"][:55]}')
                                        else:
                                            # Try old steps as fallback for unique scenarios
                                            tm = sc.get('test_method')
                                            if tm and tm in old_steps:
                                                sc['steps'] = old_steps[tm]
                                                kept_old += 1
                                                print(f'    [OLD]   {sc["name"][:55]}')
                                            else:
                                                skipped += 1
                                                print(f'    [SKIP]  {sc["name"][:55]}')

    print(f'\n--- {written} consistent steps written, {kept_old} old steps kept, {skipped} need manual steps ---')

    STORY_GRAPH_PATH.write_text(json.dumps(g, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Wrote to {STORY_GRAPH_PATH}')


if __name__ == '__main__':
    main()
