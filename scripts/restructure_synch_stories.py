"""
Create a new domain-based sub-epic alongside the old operation-based one.
Old sub-epic stays untouched as reference for scenarios step.

Creates: "Synchronize Diagram by Domain" under "Perform Action"
with 10 domain-based stories in 3 groups.
"""
import json
import sys
from pathlib import Path

STORY_GRAPH_PATH = Path(__file__).parent.parent / 'docs' / 'story' / 'story-graph.json'

NEW_SUB_EPIC = {
    "name": "Synchronize Diagram by Domain",
    "sequential_order": 6.0,
    "behavior": None,
    "domain_concepts": [],
    "test_file": "invoke_bot/perform_action/test_synchronized_graph_with_rendered_diagram_content.py",
    "sub_epics": [],
    "story_groups": [
        {
            "name": "",
            "sequential_order": 0.0,
            "type": "and",
            "connector": None,
            "behavior": None,
            "stories": [
                # --- Group 1: Sync Epics and Sub-Epics ---
                {
                    "name": "Render epic and sub-epic hierarchy",
                    "sequential_order": 1.0,
                    "connector": "or",
                    "story_type": "user",
                    "users": ["Bot Behavior"],
                    "test_class": "TestRenderEpicAndSubEpicHierarchy",
                    "test_file": "invoke_bot/perform_action/test_sync_epics_and_sub_epics.py",
                    "acceptance_criteria": [
                        {"name": "When story graph has nested sub-epics then system renders each depth level with increasing Y positions and parent width encompasses all children", "text": "When story graph has nested sub-epics then system renders each depth level with increasing Y positions and parent width encompasses all children", "sequential_order": 1.0},
                        {"name": "When epic is rendered then epic horizontal span covers all its sub-epics", "text": "When epic is rendered then epic horizontal span covers all its sub-epics", "sequential_order": 2.0},
                        {"name": "When sibling sub-epics are rendered then no two sub-epics overlap horizontally", "text": "When sibling sub-epics are rendered then no two sub-epics overlap horizontally", "sequential_order": 3.0},
                        {"name": "When epic and sub-epic cells are rendered then all cells have whiteSpace wrap and html enabled and explicit fontSize", "text": "When epic and sub-epic cells are rendered then all cells have whiteSpace wrap and html enabled and explicit fontSize", "sequential_order": 4.0},
                    ],
                    "scenarios": [],
                    "behavior": None,
                },
                {
                    "name": "Report epic and sub-epic changes",
                    "sequential_order": 2.0,
                    "connector": "or",
                    "story_type": "user",
                    "users": ["Bot Behavior"],
                    "test_class": "TestReportEpicAndSubEpicChanges",
                    "test_file": "invoke_bot/perform_action/test_sync_epics_and_sub_epics.py",
                    "acceptance_criteria": [
                        {"name": "When user creates a sub-epic manually in DrawIO with simple cell ID then report treats it as new not rename", "text": "When user creates a sub-epic manually in DrawIO with simple cell ID then report treats it as new not rename", "sequential_order": 1.0},
                        {"name": "When tool-generated sub-epic with hierarchical cell ID is unmatched then report pairs it as rename candidate", "text": "When tool-generated sub-epic with hierarchical cell ID is unmatched then report pairs it as rename candidate", "sequential_order": 2.0},
                        {"name": "When rename report is serialized to JSON and restored then all fields survive roundtrip", "text": "When rename report is serialized to JSON and restored then all fields survive roundtrip", "sequential_order": 3.0},
                    ],
                    "scenarios": [],
                    "behavior": None,
                },
                {
                    "name": "Update epics and sub-epics from diagram",
                    "sequential_order": 3.0,
                    "connector": "or",
                    "story_type": "user",
                    "users": ["Bot Behavior"],
                    "test_class": "TestUpdateEpicsAndSubEpicsFromDiagram",
                    "test_file": "invoke_bot/perform_action/test_sync_epics_and_sub_epics.py",
                    "acceptance_criteria": [
                        {"name": "When new sub-epic appears in diagram then story graph adds it", "text": "When new sub-epic appears in diagram then story graph adds it", "sequential_order": 1.0},
                        {"name": "When sub-epic is renamed in diagram then story graph updates name", "text": "When sub-epic is renamed in diagram then story graph updates name", "sequential_order": 2.0},
                        {"name": "When sub-epic is removed from diagram then story graph removes it", "text": "When sub-epic is removed from diagram then story graph removes it", "sequential_order": 3.0},
                        {"name": "When nested sub-epic structure changes in diagram then story graph preserves new structure", "text": "When nested sub-epic structure changes in diagram then story graph preserves new structure", "sequential_order": 4.0},
                    ],
                    "scenarios": [],
                    "behavior": None,
                },
                # --- Group 2: Sync Stories and Actors ---
                {
                    "name": "Render stories and actors",
                    "sequential_order": 4.0,
                    "connector": "or",
                    "story_type": "user",
                    "users": ["Bot Behavior"],
                    "test_class": "TestRenderStoriesAndActors",
                    "test_file": "invoke_bot/perform_action/test_sync_stories_and_actors.py",
                    "acceptance_criteria": [
                        {"name": "When stories are rendered then they are positioned below deepest sub-epic", "text": "When stories are rendered then they are positioned below deepest sub-epic", "sequential_order": 1.0},
                        {"name": "When stories have users then actor elements are rendered in actor row above stories", "text": "When stories have users then actor elements are rendered in actor row above stories", "sequential_order": 2.0},
                        {"name": "When sub-epic contains stories then sub-epic horizontal span covers all its stories", "text": "When sub-epic contains stories then sub-epic horizontal span covers all its stories", "sequential_order": 3.0},
                        {"name": "When sibling stories are rendered then no two stories overlap horizontally", "text": "When sibling stories are rendered then no two stories overlap horizontally", "sequential_order": 4.0},
                        {"name": "When story and actor cells are rendered then all cells have whiteSpace wrap and html enabled and explicit fontSize", "text": "When story and actor cells are rendered then all cells have whiteSpace wrap and html enabled and explicit fontSize", "sequential_order": 5.0},
                    ],
                    "scenarios": [],
                    "behavior": None,
                },
                {
                    "name": "Report story moves between parents",
                    "sequential_order": 5.0,
                    "connector": "or",
                    "story_type": "user",
                    "users": ["Bot Behavior"],
                    "test_class": "TestReportStoryMovesBetweenParents",
                    "test_file": "invoke_bot/perform_action/test_sync_stories_and_actors.py",
                    "acceptance_criteria": [
                        {"name": "When story moves from one sub-epic to another then report detects it as move not new plus removed", "text": "When story moves from one sub-epic to another then report detects it as move not new plus removed", "sequential_order": 1.0},
                        {"name": "When sub-epic is removed and its stories appear under parent then report detects stories as moves", "text": "When sub-epic is removed and its stories appear under parent then report detects stories as moves", "sequential_order": 2.0},
                        {"name": "When moved stories report is serialized to JSON and restored then all fields survive roundtrip", "text": "When moved stories report is serialized to JSON and restored then all fields survive roundtrip", "sequential_order": 3.0},
                        {"name": "When no stories change position then report has no false moves", "text": "When no stories change position then report has no false moves", "sequential_order": 4.0},
                    ],
                    "scenarios": [],
                    "behavior": None,
                },
                {
                    "name": "Report acceptance criteria changes",
                    "sequential_order": 6.0,
                    "connector": "or",
                    "story_type": "user",
                    "users": ["Bot Behavior"],
                    "test_class": "TestReportAcceptanceCriteriaChanges",
                    "test_file": "invoke_bot/perform_action/test_sync_stories_and_actors.py",
                    "acceptance_criteria": [
                        {"name": "When diagram matches original then no AC changes reported", "text": "When diagram matches original then no AC changes reported", "sequential_order": 1.0},
                        {"name": "When AC box is added below a story in diagram then report detects added AC", "text": "When AC box is added below a story in diagram then report detects added AC", "sequential_order": 2.0},
                        {"name": "When AC box is removed from a story in diagram then report detects removed AC", "text": "When AC box is removed from a story in diagram then report detects removed AC", "sequential_order": 3.0},
                        {"name": "When AC moves between stories then report detects it as AC move", "text": "When AC moves between stories then report detects it as AC move", "sequential_order": 4.0},
                        {"name": "When AC change report is serialized to JSON and restored then all fields survive roundtrip", "text": "When AC change report is serialized to JSON and restored then all fields survive roundtrip", "sequential_order": 5.0},
                    ],
                    "scenarios": [],
                    "behavior": None,
                },
                {
                    "name": "Update stories and acceptance criteria from diagram",
                    "sequential_order": 7.0,
                    "connector": "or",
                    "story_type": "user",
                    "users": ["Bot Behavior"],
                    "test_class": "TestUpdateStoriesAndAcceptanceCriteriaFromDiagram",
                    "test_file": "invoke_bot/perform_action/test_sync_stories_and_actors.py",
                    "acceptance_criteria": [
                        {"name": "When sub-epic is removed but its stories were moved then moves are applied before removes so stories survive", "text": "When sub-epic is removed but its stories were moved then moves are applied before removes so stories survive", "sequential_order": 1.0},
                        {"name": "When story is not moved then it is deleted with its sub-epic", "text": "When story is not moved then it is deleted with its sub-epic", "sequential_order": 2.0},
                        {"name": "When AC is deleted from a story in diagram then story graph removes it", "text": "When AC is deleted from a story in diagram then story graph removes it", "sequential_order": 3.0},
                        {"name": "When AC is moved between stories in diagram then both source and target are updated", "text": "When AC is moved between stories in diagram then both source and target are updated", "sequential_order": 4.0},
                        {"name": "When story is deleted and its AC redistributed then target stories receive the AC", "text": "When story is deleted and its AC redistributed then target stories receive the AC", "sequential_order": 5.0},
                        {"name": "When two stories are merged into new story then combined AC from both originals", "text": "When two stories are merged into new story then combined AC from both originals", "sequential_order": 6.0},
                    ],
                    "scenarios": [],
                    "behavior": None,
                },
                # --- Group 3: Sync Increments ---
                {
                    "name": "Render increment lanes",
                    "sequential_order": 8.0,
                    "connector": "or",
                    "story_type": "user",
                    "users": ["Bot Behavior"],
                    "test_class": "TestRenderIncrementLanes",
                    "test_file": "invoke_bot/perform_action/test_sync_increments.py",
                    "acceptance_criteria": [
                        {"name": "When increments are rendered then lanes have correct boundaries and stories assigned by membership", "text": "When increments are rendered then lanes have correct boundaries and stories assigned by membership", "sequential_order": 1.0},
                        {"name": "When increment lanes are rendered then lane order matches increment priority", "text": "When increment lanes are rendered then lane order matches increment priority", "sequential_order": 2.0},
                        {"name": "When user creates a lane manually in DrawIO then it is detected by geometry", "text": "When user creates a lane manually in DrawIO then it is detected by geometry", "sequential_order": 3.0},
                    ],
                    "scenarios": [],
                    "behavior": None,
                },
                {
                    "name": "Report increment changes",
                    "sequential_order": 9.0,
                    "connector": "or",
                    "story_type": "user",
                    "users": ["Bot Behavior"],
                    "test_class": "TestReportIncrementChanges",
                    "test_file": "invoke_bot/perform_action/test_sync_increments.py",
                    "acceptance_criteria": [
                        {"name": "When user-created lane appears in diagram then report includes it as new increment", "text": "When user-created lane appears in diagram then report includes it as new increment", "sequential_order": 1.0},
                        {"name": "When diagram matches original then no increment changes reported", "text": "When diagram matches original then no increment changes reported", "sequential_order": 2.0},
                        {"name": "When story moves between increment lanes then report detects correct delta", "text": "When story moves between increment lanes then report detects correct delta", "sequential_order": 3.0},
                        {"name": "When increment delta report is serialized to JSON and restored then all fields survive roundtrip", "text": "When increment delta report is serialized to JSON and restored then all fields survive roundtrip", "sequential_order": 4.0},
                    ],
                    "scenarios": [],
                    "behavior": None,
                },
                {
                    "name": "Update increments from diagram",
                    "sequential_order": 10.0,
                    "connector": "or",
                    "story_type": "user",
                    "users": ["Bot Behavior"],
                    "test_class": "TestUpdateIncrementsFromDiagram",
                    "test_file": "invoke_bot/perform_action/test_sync_increments.py",
                    "acceptance_criteria": [
                        {"name": "When increment is removed from diagram then story graph deletes it", "text": "When increment is removed from diagram then story graph deletes it", "sequential_order": 1.0},
                        {"name": "When story moves between increments in diagram then story graph transfers it", "text": "When story moves between increments in diagram then story graph transfers it", "sequential_order": 2.0},
                        {"name": "When increment order changes in diagram then story graph updates priorities", "text": "When increment order changes in diagram then story graph updates priorities", "sequential_order": 3.0},
                        {"name": "When increment lane is removed and stories moved then moves apply before removes", "text": "When increment lane is removed and stories moved then moves apply before removes", "sequential_order": 4.0},
                    ],
                    "scenarios": [],
                    "behavior": None,
                },
            ]
        }
    ]
}


def main():
    print(f'Loading {STORY_GRAPH_PATH}')
    graph_data = json.loads(STORY_GRAPH_PATH.read_text(encoding='utf-8'))

    # Find "Perform Action" sub-epic (parent of both old and new)
    perform_action = None
    for epic in graph_data.get('epics', []):
        for se in epic.get('sub_epics', []):
            if se.get('name') == 'Perform Action':
                perform_action = se
                break

    if not perform_action:
        print('ERROR: Could not find "Perform Action" sub-epic')
        return 1

    # Check if new sub-epic already exists
    existing = [s['name'] for s in perform_action.get('sub_epics', [])]
    if NEW_SUB_EPIC['name'] in existing:
        print(f'Sub-epic "{NEW_SUB_EPIC["name"]}" already exists -- skipping')
        return 0

    print(f'Found "Perform Action" with {len(existing)} sub-epics:')
    for name in existing:
        print(f'  - {name}')

    # Add new sub-epic as sibling
    perform_action['sub_epics'].append(NEW_SUB_EPIC)
    story_names = [s['name'] for s in NEW_SUB_EPIC['story_groups'][0]['stories']]
    print(f'\nAdded "{NEW_SUB_EPIC["name"]}" with {len(story_names)} stories:')
    for name in story_names:
        print(f'  + {name}')

    print(f'\nOld sub-epic "Synchronized Graph with Rendered Diagram Content" left untouched.')

    STORY_GRAPH_PATH.write_text(
        json.dumps(graph_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Wrote to {STORY_GRAPH_PATH}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
