"""
Analyze scenario patterns across domain groups to find shared vocabulary,
approach, and language opportunities.
"""
import json
import re
from pathlib import Path
from collections import defaultdict

STORY_GRAPH_PATH = Path(__file__).parent.parent / 'docs' / 'story' / 'story-graph.json'
NEW_SUB_EPIC = 'Synchronize Diagram by Domain'


def load_new_stories(graph_data):
    """Load all stories from the new sub-epic, grouped by domain and operation."""
    result = {}
    for epic in graph_data.get('epics', []):
        for se in epic.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                for se2 in se.get('sub_epics', []):
                    if se2.get('name') == NEW_SUB_EPIC:
                        for se3 in se2.get('sub_epics', []):
                            domain = se3['name']
                            for sg in se3.get('story_groups', []):
                                for story in sg.get('stories', []):
                                    # Classify operation
                                    name = story['name'].lower()
                                    if 'render' in name:
                                        op = 'render'
                                    elif 'report' in name:
                                        op = 'report'
                                    elif 'update' in name:
                                        op = 'update'
                                    else:
                                        op = 'other'
                                    result[(domain, op)] = story
    return result


def extract_verbs(scenario_names):
    """Extract action verbs from scenario names."""
    verbs = defaultdict(int)
    for name in scenario_names:
        words = name.lower().split()
        # Common test verbs
        for verb in ['render', 'extract', 'update', 'report', 'apply', 'detect',
                     'assign', 'preserve', 'delete', 'remove', 'move', 'merge',
                     'flag', 'list', 'serialize', 'roundtrip', 'create', 'produce',
                     'recompute', 'style', 'order', 'position', 'span', 'overlap',
                     'show', 'include', 'reflect', 'contain', 'keep', 'stay',
                     'append', 'rename', 'reassign', 'transfer']:
            if verb in words or any(verb in w for w in words):
                verbs[verb] += 1
    return verbs


def main():
    graph_data = json.loads(STORY_GRAPH_PATH.read_text(encoding='utf-8'))
    stories = load_new_stories(graph_data)

    domains = ['Synchronize Epics and Sub-Epics', 'Synchronize Stories and Actors', 'Synchronize Increments']
    ops = ['render', 'report', 'update']

    # === 1. PARALLEL SCENARIOS BY OPERATION TYPE ===
    print('=' * 80)
    print('PARALLEL SCENARIO PATTERNS BY OPERATION')
    print('=' * 80)

    for op in ops:
        print(f'\n--- {op.upper()} scenarios across domains ---\n')
        for domain in domains:
            key = (domain, op)
            story = stories.get(key)
            if not story:
                # Stories group has multiple report stories
                continue
            short_domain = domain.replace('Synchronize ', '')
            scenarios = story.get('scenarios', [])
            print(f'  {short_domain} ({story["name"]}, {len(scenarios)} scenarios):')
            for sc in scenarios:
                print(f'    - {sc["name"]}')
        print()

    # === 2. SHARED VOCABULARY (verbs that appear across multiple domains) ===
    print('=' * 80)
    print('SHARED VOCABULARY ACROSS DOMAINS')
    print('=' * 80)

    domain_verbs = {}
    for domain in domains:
        all_names = []
        for op in ops:
            story = stories.get((domain, op))
            if story:
                all_names.extend(sc['name'] for sc in story.get('scenarios', []))
        domain_verbs[domain] = extract_verbs(all_names)

    # Find verbs used in 2+ domains
    all_verbs = set()
    for v in domain_verbs.values():
        all_verbs.update(v.keys())

    print(f'\n{"Verb":<15} {"Epics":<8} {"Stories":<8} {"Increments":<8} Shared?')
    print('-' * 55)
    for verb in sorted(all_verbs):
        counts = []
        for domain in domains:
            counts.append(domain_verbs[domain].get(verb, 0))
        shared = sum(1 for c in counts if c > 0)
        marker = '<-- shared' if shared >= 2 else ''
        print(f'{verb:<15} {counts[0]:<8} {counts[1]:<8} {counts[2]:<8} {marker}')

    # === 3. PARALLEL PATTERN OPPORTUNITIES ===
    print('\n' + '=' * 80)
    print('PARALLEL PATTERN OPPORTUNITIES')
    print('(Scenarios that follow the same pattern across domains)')
    print('=' * 80)

    patterns = {
        'roundtrip serialization': {
            'pattern': lambda n: 'roundtrip' in n.lower() or 'serializ' in n.lower() or 'round_trip' in n.lower(),
            'description': 'Report roundtrips through JSON',
        },
        'no changes when matching': {
            'pattern': lambda n: 'no_changes' in n.lower() or 'no_false' in n.lower() or 'no false' in n.lower(),
            'description': 'No false positives when diagram matches original',
        },
        'move detection': {
            'pattern': lambda n: 'move' in n.lower() and ('detect' in n.lower() or 'as_move' in n.lower() or 'reflected' in n.lower()),
            'description': 'Moved entity detected as move not new+removed',
        },
        'apply preserves data': {
            'pattern': lambda n: 'preserv' in n.lower() or 'preserve' in n.lower(),
            'description': 'Apply operation preserves entity data',
        },
        'end to end': {
            'pattern': lambda n: 'end_to_end' in n.lower() or 'end to end' in n.lower(),
            'description': 'End-to-end render -> report -> update flow',
        },
        'deleted/removed entity': {
            'pattern': lambda n: 'delet' in n.lower() or 'remov' in n.lower(),
            'description': 'Handling deleted/removed entities',
        },
        'renamed entity': {
            'pattern': lambda n: 'renam' in n.lower(),
            'description': 'Handling renamed entities',
        },
        'position-based assignment': {
            'pattern': lambda n: 'position' in n.lower() or 'containment' in n.lower() or 'y_position' in n.lower(),
            'description': 'Entity assigned by position/containment',
        },
    }

    for pattern_name, config in patterns.items():
        matches = defaultdict(list)
        for domain in domains:
            for op in ops:
                story = stories.get((domain, op))
                if not story:
                    continue
                for sc in story.get('scenarios', []):
                    if config['pattern'](sc.get('test_method', '') + ' ' + sc.get('name', '')):
                        short_domain = domain.replace('Synchronize ', '')
                        matches[short_domain].append(f'{sc["name"][:60]}')

        if len(matches) >= 2:
            print(f'\n  PATTERN: {pattern_name} ({config["description"]})')
            print(f'  Appears in {len(matches)} domains:')
            for domain, scenarios in matches.items():
                for s in scenarios:
                    print(f'    [{domain}] {s}')

    # === 4. STORIES GROUP (Stories and Actors has 4 stories, others have 3) ===
    print('\n' + '=' * 80)
    print('EXTRA REPORT STORY IN STORIES GROUP')
    print('=' * 80)
    print('\n  Stories and Actors has 2 report stories (story moves + AC changes)')
    print('  vs 1 report story each for Epics and Increments')
    print('  This is intentional: story moves and AC changes are distinct operations')

    # === 5. SCENARIO COUNT BALANCE ===
    print('\n' + '=' * 80)
    print('SCENARIO COUNT BALANCE')
    print('=' * 80)
    print(f'\n  {"Domain":<35} {"Render":<10} {"Report":<10} {"Update":<10} {"Total":<10}')
    print('  ' + '-' * 75)
    for domain in domains:
        short = domain.replace('Synchronize ', '')
        counts = {}
        for op in ops:
            story = stories.get((domain, op))
            counts[op] = len(story.get('scenarios', [])) if story else 0
        total = sum(counts.values())
        print(f'  {short:<35} {counts["render"]:<10} {counts["report"]:<10} {counts["update"]:<10} {total:<10}')


if __name__ == '__main__':
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    main()
