"""
Rewrite ALL scenario steps based on the complete inheritance table.
Every base test method gets consistent steps across all domains.
Domain-unique scenarios keep their existing steps.

Base test patterns (21 methods):
  RENDER (7): default_layout, parent_contains_children, correct_child_count,
              children_in_order, siblings_no_overlap, re_render_layout, completes_writes_file
  REPORT (7): no_changes, added_new, removed, moved, renamed, roundtrip, lists_matches
  UPDATE (7): apply_changes, apply_move, moved_preserved, unmoved_removed,
              renamed_name, preserves_original, end_to_end
"""
import json, sys, io, copy
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
STORY_GRAPH_PATH = Path(__file__).parent.parent / 'docs' / 'story' / 'story-graph.json'

# Domain config: concept names for step generation
DOMAINS = {
    'Synchronize Epics and Sub-Epics': {
        'Render epic and sub-epic hierarchy': {
            'parent': '{DrawIOEpic}', 'child': '{DrawIOSubEpic}', 'child_plural': '{DrawIOSubEpic}s',
            'entity': 'sub-epic', 'diagram_type': 'outline',
            'render_verb': 'renders outline from {StoryMap}',
            'data_desc': '{StoryMap} has {DrawIOEpic} with nested {DrawIOSubEpic}',
            'overlap_axis': 'horizontal', 'order_field': '{DrawIOStoryNode.sequential_order}',
        },
        'Report epic and sub-epic changes': {
            'entity': 'sub-epic', 'entity_concept': '{DrawIOSubEpic}',
            'report_verb': '{DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs',
        },
        'Update epics and sub-epics from diagram': {
            'entity': 'sub-epic', 'entity_concept': '{DrawIOSubEpic}',
            'parent': '{DrawIOEpic}', 'parent_name': 'epic',
        },
    },
    'Synchronize Stories and Actors': {
        'Render stories and actors': {
            'parent': '{DrawIOSubEpic}', 'child': '{DrawIOStory}', 'child_plural': '{DrawIOStory} cells',
            'entity': 'story', 'diagram_type': 'outline',
            'render_verb': 'renders outline from {StoryMap}',
            'data_desc': '{StoryMap} has {DrawIOSubEpic} with {DrawIOStory} and actor labels',
            'overlap_axis': 'horizontal', 'order_field': '{DrawIOStoryNode.sequential_order}',
        },
        'Render acceptance criteria': {
            'parent': '{DrawIOStory}', 'child': 'AC {DrawIOElement}', 'child_plural': 'AC {DrawIOElement} boxes',
            'entity': 'acceptance criteria', 'diagram_type': 'exploration',
            'render_verb': 'renders exploration from {StoryMap}',
            'data_desc': '{StoryMap} has {DrawIOStory} with acceptance_criteria',
            'overlap_axis': 'vertical', 'order_field': '{AcceptanceCriteria.sequential_order}',
        },
        'Report story moves between parents': {
            'entity': 'story', 'entity_concept': '{DrawIOStory}',
            'report_verb': '{DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs',
        },
        'Report acceptance criteria changes': {
            'entity': 'acceptance criteria', 'entity_concept': 'AC {DrawIOElement}',
            'report_verb': '{DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs',
        },
        'Update stories from diagram': {
            'entity': 'story', 'entity_concept': '{DrawIOStory}',
            'parent': '{DrawIOSubEpic}', 'parent_name': 'sub-epic',
        },
        'Update acceptance criteria from diagram': {
            'entity': 'acceptance criteria', 'entity_concept': 'AC {DrawIOElement}',
            'parent': '{DrawIOStory}', 'parent_name': 'story',
        },
    },
    'Synchronize Increments': {
        'Render increment lanes': {
            'parent': 'increment lane', 'child': '{DrawIOStory}', 'child_plural': '{DrawIOStory} cells',
            'entity': 'increment', 'diagram_type': 'increments',
            'render_verb': 'renders increments from {StoryMap}',
            'data_desc': '{StoryMap} has increments with {DrawIOStory} assigned to lanes',
            'overlap_axis': 'vertical', 'order_field': 'increment priority',
        },
        'Report increment changes': {
            'entity': 'increment', 'entity_concept': 'increment lane',
            'report_verb': '{DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs',
        },
        'Update increments from diagram': {
            'entity': 'increment', 'entity_concept': 'increment lane',
            'parent': 'increment lane', 'parent_name': 'increment',
        },
    },
}


def render_steps(scenario_name, d):
    """Generate steps for render scenarios."""
    sn = scenario_name.lower()
    ent = d.get('entity', 'entity')
    parent = d.get('parent', '{Parent}')
    child = d.get('child', '{Child}')
    child_plural = d.get('child_plural', 'children')
    render = d.get('render_verb', 'renders from {StoryMap}')
    data = d.get('data_desc', '{StoryMap} has entities')
    axis = d.get('overlap_axis', 'horizontal')
    order = d.get('order_field', 'sequential_order')
    dtype = d.get('diagram_type', 'outline')

    if 'default layout' in sn:
        return (f'Given {data}\nAnd no {{LayoutData}} exists for this diagram\n'
                f'When {{DrawIOStoryMap}} {render}\n'
                f'Then {{DrawIOStoryMap}} positions {child_plural} with correct layout\n'
                f'And output is valid DrawIO XML')

    if 'parent' in sn and 'contains all children' in sn:
        return (f'Given {data}\nWhen {{DrawIOStoryMap}} {render}\n'
                f'Then each {parent} contains all its expected {child_plural}')

    if 'correct child count' in sn:
        return (f'Given {data}\nWhen {{DrawIOStoryMap}} {render}\n'
                f'Then each {parent} has the correct number of {child_plural} matching {{StoryMap}}')

    if 'rendered in' in sn and 'order' in sn:
        return (f'Given {data} with {order} values\n'
                f'When {{DrawIOStoryMap}} {render}\n'
                f'Then {child_plural} are rendered in the same order as {order} from {{StoryMap}}\n'
                f'And diagram API returns {child_plural} in the same order')

    if 'siblings' in sn and 'overlap' in sn:
        return (f'Given {data}\nWhen {{DrawIOStoryMap}} {render}\n'
                f'Then no two sibling {child_plural} overlap {axis}ly')

    if 're-render' in sn and 'layout' in sn:
        return (f'Given {data}\nAnd {{LayoutData}} exists with saved positions from previous render\n'
                f'When {{DrawIOStoryMap}} {render}\n'
                f'Then {{DrawIOStoryMap}} applies {{LayoutData}} saved positions for {child_plural}')

    if 'completes' in sn and 'writes' in sn:
        return (f'Given {data}\nWhen {{DrawIOStoryMap}} {render}\n'
                f'Then {{DrawIOStoryMap}} is written to specified file path\n'
                f'And output is valid DrawIO XML\nAnd summary reports correct counts')

    return None


def report_steps(scenario_name, d):
    """Generate steps for report scenarios."""
    sn = scenario_name.lower()
    ent = d.get('entity', 'entity')
    ec = d.get('entity_concept', '{Entity}')
    report = d.get('report_verb', '{DrawIOStoryMap}.generateUpdateReport({StoryMap}) runs')

    if 'no changes' in sn and 'matches original' in sn:
        return (f'Given {{DrawIOStoryMap}} has been rendered from {{StoryMap}}\n'
                f'And no {ent} changes made to diagram\n'
                f'When {report}\nThen {{UpdateReport}} reports zero {ent} changes')

    if 'added' in sn and 'detected as new' in sn:
        return (f'Given {{DrawIOStoryMap}} has a new {ec} added by user\n'
                f'And original {{StoryMap}} does not have this {ent}\n'
                f'When {report}\nThen {{UpdateReport}} lists the {ent} as new')

    if 'removed' in sn and 'detected as removed' in sn:
        return (f'Given {{DrawIOStoryMap}} has had a {ec} removed by user\n'
                f'And original {{StoryMap}} has this {ent}\n'
                f'When {report}\nThen {{UpdateReport}} lists the {ent} as removed')

    if 'moved' in sn and ('detected as move' in sn or 'not new plus removed' in sn):
        return (f'Given {ec} has been moved from one parent to another in {{DrawIOStoryMap}}\n'
                f'And original {{StoryMap}} has this {ent} under the original parent\n'
                f'When {report}\nThen {{UpdateReport}} detects the {ent} as moved not new plus removed')

    if 'renamed' in sn and 'detected as rename' in sn:
        return (f'Given {ec} has been renamed in {{DrawIOStoryMap}}\n'
                f'And original {{StoryMap}} has the original name\n'
                f'When {report}\nThen {{UpdateReport}} pairs the renamed {ent} as a rename match')

    if 'roundtrips through json' in sn:
        return (f'Given {{UpdateReport}} has {ent} changes (added, removed, moved)\n'
                f'When {{UpdateReport}}.to_dict() serializes to JSON\n'
                f'And {{UpdateReport}}.from_dict() restores from JSON\n'
                f'Then all {ent} change fields survive the roundtrip')

    if 'lists exact fuzzy' in sn or 'report lists' in sn:
        return (f'Given {{DrawIOStoryMap}} has been extracted from diagram\n'
                f'And original {{StoryMap}} exists with known {ent} names\n'
                f'When {report}\n'
                f'Then {{UpdateReport}} lists exact matches and fuzzy matches and new and removed {ent}s')

    if 'report includes removed' in sn:
        return (f'Given {{DrawIOStoryMap}} has fewer {ent}s than original\n'
                f'When {report}\n'
                f'Then {{UpdateReport}} includes removed {ent}s and updated order')

    return None


def update_steps(scenario_name, d):
    """Generate steps for update scenarios."""
    sn = scenario_name.lower()
    ent = d.get('entity', 'entity')
    ec = d.get('entity_concept', '{Entity}')
    parent = d.get('parent', '{Parent}')
    pname = d.get('parent_name', 'parent')

    if 'apply' in sn and 'changes from report' in sn:
        return (f'Given {{UpdateReport}} has been generated with {ent} changes\n'
                f'When {{UpdateReport}} is applied to story graph\n'
                f'Then story graph reflects the {ent} additions and removals from {{UpdateReport}}')

    if 'apply' in sn and 'move' in sn and 'preserv' in sn:
        return (f'Given {{UpdateReport}} contains a {ent} move from one {pname} to another\n'
                f'When move is applied to story graph\n'
                f'Then {ent} is removed from source {pname} and added to target {pname}\n'
                f'And all {ent} fields are preserved')

    if 'moved' in sn and 'preserved when' in sn and 'removed' in sn:
        return (f'Given {ec} has been moved to another {pname} in {{DrawIOStoryMap}}\n'
                f'And the original {pname} is being removed\n'
                f'When {{UpdateReport}} is applied (moves before removes)\n'
                f'Then moved {ent} survives the {pname} removal')

    if 'unmoved' in sn and 'removed with' in sn:
        return (f'Given {ec} was NOT moved to another {pname}\n'
                f'And the {pname} is being removed\n'
                f'When {{UpdateReport}} is applied\n'
                f'Then unmoved {ent} is removed along with its {pname}')

    if 'renamed' in sn and 'updates' in sn and 'name' in sn and 'story graph' in sn:
        return (f'Given {ec} has been renamed in {{DrawIOStoryMap}}\n'
                f'When {{UpdateReport}} is applied to story graph\n'
                f'Then story graph updates the {ent} name to match diagram')

    if 'updates correctly' in sn:
        return (f'Given {ec} is being moved to a renamed {pname}\n'
                f'When {{UpdateReport}} is applied to story graph\n'
                f'Then move resolves correctly to the renamed {pname}')

    if ('preserves original' in sn or 'merge preserves' in sn) and 'acceptance criteria' in sn:
        return (f'Given {{UpdateReport}} has matched {ent}s between diagram and story graph\n'
                f'When {{UpdateReport}} is applied to story graph\n'
                f'Then original acceptance_criteria and scenarios are preserved for matched {ent}s')

    if 'end-to-end' in sn and 'render' in sn and 'report' in sn and 'update' in sn:
        return (f'Given {{StoryMap}} has {ent}s\n'
                f'When {{DrawIOStoryMap}} renders from {{StoryMap}}\n'
                f'And user modifies {ent}s in diagram\n'
                f'And {{DrawIOStoryMap}}.generateUpdateReport({{StoryMap}}) runs\n'
                f'And {{UpdateReport}} is applied to story graph\n'
                f'Then story graph reflects all {ent} changes from diagram')

    if 'new' in sn and 'creates it' in sn:
        return (f'Given {{DrawIOStoryMap}} has a new {ent} not in original {{StoryMap}}\n'
                f'When {{UpdateReport}} is applied to story graph\n'
                f'Then story graph creates the new {ent}')

    if 'creates it and transfers' in sn:
        return (f'Given {ec} is being moved to a {pname} that does not exist yet\n'
                f'When {{UpdateReport}} is applied to story graph\n'
                f'Then story graph creates the new {pname} and transfers the {ent}')

    return None


def main():
    g = json.loads(STORY_GRAPH_PATH.read_text(encoding='utf-8'))

    consistent = 0
    unique_kept = 0
    unique_empty = 0

    for e in g['epics']:
        for se in e.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == 'Synchronize Diagram by Domain':
                        for se3 in se2.get('sub_epics', []):
                            domain_name = se3['name']
                            domain_config = DOMAINS.get(domain_name, {})
                            print(f'\n=== {domain_name} ===')

                            for sg in se3.get('story_groups', []):
                                for st in sg.get('stories', []):
                                    story_name = st['name']
                                    d = domain_config.get(story_name, {})
                                    print(f'\n  {story_name}:')

                                    # Classify story as render/report/update
                                    sn_lower = story_name.lower()
                                    if 'render' in sn_lower:
                                        step_fn = render_steps
                                    elif 'report' in sn_lower:
                                        step_fn = report_steps
                                    elif 'update' in sn_lower:
                                        step_fn = update_steps
                                    else:
                                        step_fn = lambda n, d: None

                                    for sc in st.get('scenarios', []):
                                        new_steps = step_fn(sc['name'], d)
                                        if new_steps:
                                            sc['steps'] = new_steps
                                            consistent += 1
                                            print(f'    [CONSISTENT] {sc["name"][:55]}')
                                        elif sc.get('steps') and sc['steps'].strip():
                                            unique_kept += 1
                                            print(f'    [UNIQUE-OK]  {sc["name"][:55]}')
                                        else:
                                            unique_empty += 1
                                            print(f'    [EMPTY]      {sc["name"][:55]}')

    print(f'\n--- {consistent} consistent, {unique_kept} unique kept, {unique_empty} empty ---')

    STORY_GRAPH_PATH.write_text(json.dumps(g, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Wrote to {STORY_GRAPH_PATH}')


if __name__ == '__main__':
    main()
