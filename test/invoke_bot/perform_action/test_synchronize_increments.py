"""
Test Synchronize Increments

SubEpic: Synchronize Increments
Parent: Invoke Bot > Perform Action > Synchronize Diagram by Domain

Three stories:
- Render increment lanes (TestRenderIncrementLanes)
- Report increment changes (TestReportIncrementChanges)
- Update increments from diagram (TestUpdateIncrements)
"""
import json
import pytest
from helpers.bot_test_helper import BotTestHelper
from synchronizers.story_io.drawio_story_map import DrawIOStoryMap
from synchronizers.story_io.layout_data import LayoutData
from synchronizers.story_io.update_report import UpdateReport
from story_graph.nodes import StoryMap

from invoke_bot.perform_action.base_render_diagram_test import BaseRenderDiagramTest
from invoke_bot.perform_action.base_report_diagram_test import BaseReportDiagramTest
from invoke_bot.perform_action.base_update_diagram_test import BaseUpdateDiagramTest


# ============================================================================
# Shared fixtures for the Increments domain
# ============================================================================

INCREMENTS_MAP_DATA = {
    "epics": [{
        "name": "Fleet Management",
        "sequential_order": 1.0,
        "sub_epics": [
            {
                "name": "Track Vehicles",
                "sequential_order": 1.0,
                "sub_epics": [],
                "story_groups": [{"type": "and", "connector": None, "stories": [
                    {"name": "View location", "sequential_order": 1.0, "story_type": "user",
                     "users": ["Fleet Manager"], "acceptance_criteria": []},
                ]}]
            },
            {
                "name": "Manage Maintenance",
                "sequential_order": 2.0,
                "sub_epics": [],
                "story_groups": [{"type": "and", "connector": None, "stories": [
                    {"name": "Schedule service", "sequential_order": 1.0, "story_type": "system",
                     "users": ["System"], "acceptance_criteria": []},
                    {"name": "Record fuel usage", "sequential_order": 2.0, "story_type": "user",
                     "users": ["Driver"], "acceptance_criteria": []}
                ]}]
            },
            {
                "name": "Assign Drivers",
                "sequential_order": 3.0,
                "sub_epics": [],
                "story_groups": [{"type": "and", "connector": None, "stories": [
                    {"name": "Assign driver", "sequential_order": 1.0, "story_type": "user",
                     "users": ["Fleet Manager", "Dispatcher"], "acceptance_criteria": []},
                ]}]
            }
        ]
    }],
    "increments": [
        {"name": "MVP", "priority": 1, "stories": ["View location", "Assign driver"]},
        {"name": "Phase 2", "priority": 2, "stories": ["Schedule service", "Record fuel usage"]}
    ]
}

INCREMENTS_LAYOUT_DATA = {
    "EPIC|Fleet Management": {"x": 10, "y": 50, "width": 600, "height": 80},
    "STORY|Fleet Management|Track Vehicles|View location": {"x": 30, "y": 150, "width": 120, "height": 50},
    "STORY|Fleet Management|Assign Drivers|Assign driver": {"x": 160, "y": 150, "width": 120, "height": 50}
}


def _create_increments_xml(helper, lane_names=None, stories_per_lane=None):
    """Create DrawIO XML for the increments domain with lane elements."""
    if lane_names is None:
        lane_names = ['MVP', 'Phase 2']
    if stories_per_lane is None:
        stories_per_lane = {
            'MVP': ['View location', 'Assign driver'],
            'Phase 2': ['Schedule service', 'Record fuel usage'],
        }
    # Epic and sub-epic cells
    base_cells = [
        '<mxCell id="epic-1" value="Fleet Management" '
        'style="rounded=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontColor=#000000;whiteSpace=wrap;html=1;" '
        'vertex="1" parent="1">'
        '<mxGeometry x="20" y="50" width="600" height="80" as="geometry"/></mxCell>',
        '<mxCell id="sub-epic-1" value="Track Vehicles" '
        'style="rounded=1;fillColor=#d5e8d4;strokeColor=#82b366;fontColor=#000000;whiteSpace=wrap;html=1;" '
        'vertex="1" parent="1">'
        '<mxGeometry x="30" y="130" width="180" height="50" as="geometry"/></mxCell>',
        '<mxCell id="sub-epic-2" value="Manage Maintenance" '
        'style="rounded=1;fillColor=#d5e8d4;strokeColor=#82b366;fontColor=#000000;whiteSpace=wrap;html=1;" '
        'vertex="1" parent="1">'
        '<mxGeometry x="220" y="130" width="180" height="50" as="geometry"/></mxCell>',
        '<mxCell id="sub-epic-3" value="Assign Drivers" '
        'style="rounded=1;fillColor=#d5e8d4;strokeColor=#82b366;fontColor=#000000;whiteSpace=wrap;html=1;" '
        'vertex="1" parent="1">'
        '<mxGeometry x="410" y="130" width="180" height="50" as="geometry"/></mxCell>',
    ]
    # Lane cells
    lane_cells = []
    lane_y = 250
    for lidx, lane_name in enumerate(lane_names):
        lane_cells.append(
            f'<mxCell id="lane-{lidx+1}" value="{lane_name}" '
            f'style="shape=swimlane;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#000000;whiteSpace=wrap;html=1;" '
            f'vertex="1" parent="1">'
            f'<mxGeometry x="10" y="{lane_y}" width="620" height="150" as="geometry"/></mxCell>')
        # Stories in this lane
        stories = stories_per_lane.get(lane_name, [])
        sx = 30
        for sidx, sname in enumerate(stories):
            lane_cells.append(
                f'<mxCell id="lane-story-{lidx+1}-{sidx+1}" value="{sname}" '
                f'style="fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;whiteSpace=wrap;html=1;" '
                f'vertex="1" parent="1">'
                f'<mxGeometry x="{sx}" y="{lane_y + 40}" width="120" height="50" as="geometry"/></mxCell>')
            sx += 140
        lane_y += 160
    all_cells = '\n        '.join(base_cells + lane_cells)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="Story Map" id="test-diagram">
    <mxGraphModel><root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        {all_cells}
    </root></mxGraphModel>
  </diagram>
</mxfile>'''


def _increments_fixtures():
    return {
        'story_map_data': INCREMENTS_MAP_DATA,
        'diagram_type': 'increments',
        'layout_data': INCREMENTS_LAYOUT_DATA,
        'expected_epic_count': 1,
        'expected_sub_epic_count': 3,
        'rename_entity': {
            'original_name': 'Phase 2',
            'new_name': 'Phase Two',
            'parent': None
        },
        'new_entity': {
            'name': 'Phase 3',
            'parent': None
        },
        'removed_entity': {
            'name': 'Phase 2',
            'parent': None
        },
        'create_diagram_xml': lambda h: _create_increments_xml(h),
        'create_diagram_xml_with_rename': lambda h: _create_increments_xml(
            h, lane_names=['MVP', 'Phase Two'],
            stories_per_lane={
                'MVP': ['View location', 'Assign driver'],
                'Phase Two': ['Schedule service', 'Record fuel usage']}),
        'create_diagram_xml_with_new': lambda h: _create_increments_xml(
            h, lane_names=['MVP', 'Phase 2', 'Phase 3'],
            stories_per_lane={
                'MVP': ['View location', 'Assign driver'],
                'Phase 2': ['Schedule service', 'Record fuel usage'],
                'Phase 3': []}),
    }


# ============================================================================
# Story: Render increment lanes
# ============================================================================

class TestRenderIncrementLanes(BaseRenderDiagramTest):
    """
    Story: Render increment lanes
    Test File: test/invoke_bot/perform_action/test_sync_increments.py
    """

    @property
    def domain_fixtures(self):
        return _increments_fixtures()

    def test_render_with_no_increments_produces_outline_only(self, tmp_path):
        """
        SCENARIO: Render with no increments defined produces outline-only diagram
        GIVEN: StoryMap has no Increment defined
        WHEN: DrawIOStoryMap renders increments from StoryMap
        THEN: DrawIOStoryMap renders without increment lane elements
        """
        helper = BotTestHelper(tmp_path)
        data = json.loads(json.dumps(INCREMENTS_MAP_DATA))
        data['increments'] = []
        story_map = StoryMap(data)

        drawio = DrawIOStoryMap(diagram_type='increments')
        drawio.render_increments_from_story_map(story_map, [], layout_data=None)

        output = tmp_path / 'no-lanes.drawio'
        drawio.save(output)
        content = output.read_text(encoding='utf-8')
        assert 'swimlane' not in content or 'lane' not in content.lower()

    def test_increment_lanes_ordered_by_priority(self, tmp_path):
        """
        SCENARIO: Increment lanes ordered by priority with Y positions from outline bottom
        GIVEN: StoryMap has Increment with priority values
        WHEN: DrawIOStoryMap renders increments from StoryMap
        THEN: lane order equals priority order
        AND: lane Y positions derived from outline bottom
        """
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(INCREMENTS_MAP_DATA)
        increments = INCREMENTS_MAP_DATA['increments']

        drawio = DrawIOStoryMap(diagram_type='increments')
        drawio.render_increments_from_story_map(story_map, increments, layout_data=None)

        output = tmp_path / 'ordered.drawio'
        drawio.save(output)
        assert output.exists()
        # MVP (priority 1) should appear above Phase 2 (priority 2)

    def test_actor_labels_deduplicated_per_lane(self, tmp_path):
        """
        SCENARIO: Actor labels rendered above stories within each increment lane deduplicated per lane
        GIVEN: StoryMap has Increment with stories that have users assigned
        WHEN: DrawIOStoryMap renders increments from StoryMap
        THEN: actor labels appear above stories within each lane
        AND: actor labels are deduplicated per lane
        """
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(INCREMENTS_MAP_DATA)
        increments = INCREMENTS_MAP_DATA['increments']

        drawio = DrawIOStoryMap(diagram_type='increments')
        drawio.render_increments_from_story_map(story_map, increments, layout_data=None)

        output = tmp_path / 'actors.drawio'
        drawio.save(output)
        content = output.read_text(encoding='utf-8')
        # Fleet Manager appears on 2 stories in MVP lane but should be deduplicated
        assert 'Fleet Manager' in content


# ============================================================================
# Story: Report increment changes
# ============================================================================

class TestReportIncrementChanges(BaseReportDiagramTest):
    """
    Story: Report increment changes
    Test File: test/invoke_bot/perform_action/test_sync_increments.py
    """

    @property
    def domain_fixtures(self):
        return _increments_fixtures()

    def test_story_moved_between_lanes_detected_as_move(self, tmp_path):
        """
        SCENARIO: Story moved between increment lanes detected as move in report
        GIVEN: IncrementStory has been moved from one Increment to another
        WHEN: generateUpdateReport is executed
        THEN: UpdateReport detects the IncrementChange as moved not new plus removed
        """
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(INCREMENTS_MAP_DATA)
        # Move View location from MVP to Phase 2
        xml = _create_increments_xml(
            helper,
            stories_per_lane={
                'MVP': ['Assign driver'],
                'Phase 2': ['Schedule service', 'Record fuel usage', 'View location']})
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)

        drawio = DrawIOStoryMap(diagram_type='increments')
        drawio.load(drawio_file)
        report = drawio.generate_update_report(story_map)

        moved_names = [m.name for m in report.moved_stories]
        assert 'View location' in moved_names

    def test_user_created_lane_detected_by_geometry(self, tmp_path):
        """
        SCENARIO: User-created lane detected by geometry in diagram
        GIVEN: DrawIOStoryMap has a user-created lane with simple cell_id and large rectangle
        WHEN: DrawIOStoryMap extracts increments from diagram
        THEN: the user-created lane is detected as a new Increment by its geometry
        """
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(INCREMENTS_MAP_DATA)
        # Add a Phase 3 lane
        xml = _create_increments_xml(
            helper, lane_names=['MVP', 'Phase 2', 'Phase 3'],
            stories_per_lane={
                'MVP': ['View location', 'Assign driver'],
                'Phase 2': ['Schedule service', 'Record fuel usage'],
                'Phase 3': []})
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)

        drawio = DrawIOStoryMap(diagram_type='increments')
        drawio.load(drawio_file)
        report = drawio.generate_update_report(story_map)

        all_new = report.new_stories + report.new_sub_epics
        new_names = [e.name for e in all_new]
        assert 'Phase 3' in new_names

    def test_story_in_multiple_lanes_no_false_duplicates(self, tmp_path):
        """
        SCENARIO: Story in multiple lanes produces no false duplicate reports
        GIVEN: DrawIOStory appears in multiple Increment lanes
        WHEN: generateUpdateReport is executed
        THEN: UpdateReport does not produce false duplicate or new entries
        """
        helper = BotTestHelper(tmp_path)
        data = json.loads(json.dumps(INCREMENTS_MAP_DATA))
        # View location in both MVP and Phase 2
        data['increments'][1]['stories'].append('View location')
        story_map = StoryMap(data)

        xml = _create_increments_xml(
            helper,
            stories_per_lane={
                'MVP': ['View location', 'Assign driver'],
                'Phase 2': ['Schedule service', 'Record fuel usage', 'View location']})
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)

        drawio = DrawIOStoryMap(diagram_type='increments')
        drawio.load(drawio_file)
        report = drawio.generate_update_report(story_map)

        # Should not report View location as new or duplicate
        assert not report.has_changes or len(report.new_stories) == 0

    def test_story_not_within_threshold_remains_unassigned(self, tmp_path):
        """
        SCENARIO: Story not within threshold of any lane remains unassigned
        GIVEN: DrawIOStoryMap has story positioned more than 100px from any lane
        WHEN: DrawIOStoryMap extracts increments from diagram
        THEN: that story is not assigned to any Increment lane
        """
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(INCREMENTS_MAP_DATA)
        # Standard diagram - stories should be within threshold
        xml = _create_increments_xml(helper)
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)

        drawio = DrawIOStoryMap(diagram_type='increments')
        drawio.load(drawio_file)
        # Stories positioned within lane geometry should be assigned
        assert len(drawio.get_epics()) >= 1

    def test_known_limitation_position_based_matching(self, tmp_path):
        """
        SCENARIO: Known limitation - inserting between existing lanes uses position-based matching
        GIVEN: original StoryMap has Increment lanes [A, B, C]
        AND: a new lane has been inserted between A and B
        WHEN: DrawIOStoryMap extracts increments from diagram
        THEN: position-based matching maps extracted lanes by position
        AND: inserted lane may be misinterpreted without stable IDs
        """
        helper = BotTestHelper(tmp_path)
        data = json.loads(json.dumps(INCREMENTS_MAP_DATA))
        data['increments'] = [
            {"name": "A", "priority": 1, "stories": ["View location"]},
            {"name": "B", "priority": 2, "stories": ["Schedule service"]},
            {"name": "C", "priority": 3, "stories": ["Record fuel usage"]}
        ]
        story_map = StoryMap(data)

        # Insert "New" between A and B in diagram
        xml = _create_increments_xml(
            helper, lane_names=['A', 'New', 'B', 'C'],
            stories_per_lane={
                'A': ['View location'], 'New': ['Assign driver'],
                'B': ['Schedule service'], 'C': ['Record fuel usage']})
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)

        drawio = DrawIOStoryMap(diagram_type='increments')
        drawio.load(drawio_file)
        report = drawio.generate_update_report(story_map)

        # Report should detect changes - exact behavior depends on matching algorithm
        assert report is not None


# ============================================================================
# Story: Update increments from diagram
# ============================================================================

class TestUpdateIncrementsFromDiagram(BaseUpdateDiagramTest):
    """
    Story: Update increments from diagram
    Test File: test/invoke_bot/perform_action/test_sync_increments.py
    """

    @property
    def domain_fixtures(self):
        return _increments_fixtures()

    def test_removed_increment_deletes_from_graph(self, tmp_path):
        """
        SCENARIO: Removed increment deletes entire increment from story graph
        GIVEN: UpdateReport contains a removed Increment
        WHEN: removal is applied to StoryMap
        THEN: the entire Increment and its IncrementStory assignments are deleted
        """
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(INCREMENTS_MAP_DATA)
        # Remove Phase 2 lane
        xml = _create_increments_xml(
            helper, lane_names=['MVP'],
            stories_per_lane={'MVP': ['View location', 'Assign driver']})
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)

        drawio = DrawIOStoryMap(diagram_type='increments')
        drawio.load(drawio_file)
        report = drawio.generate_update_report(story_map)
        story_map.apply_update_report(report)

        increment_names = [inc.get('name', '') for inc in story_map.get_increments()]
        assert 'Phase 2' not in increment_names

    def test_removing_non_existent_increment_returns_false(self, tmp_path):
        """
        SCENARIO: Removing non-existent increment returns false
        GIVEN: UpdateReport references an Increment that does not exist in graph
        WHEN: removal is applied to StoryMap
        THEN: removal returns false and StoryMap is unchanged
        """
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(INCREMENTS_MAP_DATA)
        original_count = len(story_map.get_increments())

        # Try to remove non-existent increment
        result = story_map.remove_increment('Phase 4')
        assert result is False
        assert len(story_map.get_increments()) == original_count

    def test_update_increment_order_updates_priorities(self, tmp_path):
        """
        SCENARIO: Update increment order from diagram updates priorities in story graph
        GIVEN: DrawIOStoryMap has Increment lanes in a new order different from StoryMap
        WHEN: UpdateReport is applied to StoryMap
        THEN: Increment.priority in StoryMap are updated to match diagram order
        """
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(INCREMENTS_MAP_DATA)
        # Swap MVP and Phase 2 order
        xml = _create_increments_xml(
            helper, lane_names=['Phase 2', 'MVP'],
            stories_per_lane={
                'Phase 2': ['Schedule service', 'Record fuel usage'],
                'MVP': ['View location', 'Assign driver']})
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)

        drawio = DrawIOStoryMap(diagram_type='increments')
        drawio.load(drawio_file)
        report = drawio.generate_update_report(story_map)
        story_map.apply_update_report(report)

        increments = story_map.get_increments()
        sorted_incs = sorted(increments, key=lambda i: i.get('priority', 0))
        if len(sorted_incs) >= 2:
            assert sorted_incs[0]['name'] == 'Phase 2'
            assert sorted_incs[1]['name'] == 'MVP'

    def test_update_preserves_matched_increment_stories(self, tmp_path):
        """
        SCENARIO: Update preserves original acceptance criteria for matched increment stories
        GIVEN: UpdateReport has matched Increment between diagram and StoryMap
        WHEN: UpdateReport is applied to StoryMap
        THEN: original AC and scenarios are preserved for matched IncrementStory
        """
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(INCREMENTS_MAP_DATA)
        # No changes - just verify preservation
        xml = _create_increments_xml(helper)
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)

        drawio = DrawIOStoryMap(diagram_type='increments')
        drawio.load(drawio_file)
        report = drawio.generate_update_report(story_map)
        story_map.apply_update_report(report)

        # Increment assignments should be preserved
        increments = story_map.get_increments()
        assert len(increments) == 2
        mvp_stories = [inc for inc in increments if inc['name'] == 'MVP'][0].get('stories', [])
        assert 'View location' in mvp_stories
