import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
g = json.loads(open('docs/story/story-graph.json', encoding='utf-8').read())
for e in g['epics']:
    for se in e.get('sub_epics', []):
        for se2 in se.get('sub_epics', []):
            if se2.get('name') != 'Synchronize Diagram by Domain':
                continue
            for se3 in se2.get('sub_epics', []):
                print(f'\n=== {se3["name"]} ===')
                for sg in se3.get('story_groups', []):
                    for st in sg.get('stories', []):
                        print(f'\n  STORY: {st["name"]} ({len(st.get("scenarios",[]))} scenarios)')
                        for i, sc in enumerate(st.get('scenarios', []), 1):
                            tm = sc.get('test_method', '(none)')
                            print(f'    {i:2d}. [{tm}] {sc["name"]}')
