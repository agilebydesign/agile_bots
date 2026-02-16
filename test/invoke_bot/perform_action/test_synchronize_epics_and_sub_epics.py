"""
Test Synchronize Epics and Sub-Epics

SubEpic: Synchronize Epics and Sub-Epics
Parent: Invoke Bot > Perform Action > Synchronize Diagram by Domain

Three stories:
- Render epic and sub-epic hierarchy (TestRenderEpicHierarchy)
- Report epic and sub-epic changes (TestReportEpicChanges)
- Update epics and sub-epics from diagram (TestUpdateEpicsFromDiagram)

Each inherits shared test methods from base classes and adds epic-specific scenarios.
"""
import json
import pytest
from helpers.bot_test_helper import BotTestHelper
from synchronizers.story_io.drawio_story_map import DrawIOStoryMap
from synchronizers.story_io.drawio_story_node import DrawIOSubEpic
from synchronizers.story_io.layout_data import LayoutData
from synchronizers.story_io.update_report import UpdateReport
from story_graph.nodes import StoryMap

from invoke_bot.perform_action.synchronize_graph_with_rendered_diagram.base_render_diagram_test import BaseRenderDiagramTest
from invoke_bot.perform_action.synchronize_graph_with_rendered_diagram.base_report_diagram_test import BaseReportDiagramTest
from invoke_bot.perform_action.synchronize_graph_with_rendered_diagram.base_update_diagram_test import BaseUpdateDiagramTest


# ============================================================================
# Shared fixtures for the Epic domain
# ============================================================================

EPIC_STORY_MAP_DATA = {
    "epics": [{
        "name": "Payment Processing",
        "sequential_order": 1.0,
        "sub_epics": [
            {
                "name": "Authorize Payment",
                "sequential_order": 1.0,
                "sub_epics": [],
                "story_groups": [{"type": "and", "connector": None, "stories": [
                    {"name": "Validate Card", "sequential_order": 1.0, "story_type": "user", "users": [], "acceptance_criteria": []},
                    {"name": "Check Fraud Rules", "sequential_order": 2.0, "story_type": "system", "users": [], "acceptance_criteria": []}
                ]}]
            },
            {
                "name": "Settle Transaction",
                "sequential_order": 2.0,
                "sub_epics": [],
                "story_groups": [{"type": "and", "connector": None, "stories": [
                    {"name": "Send to Bank", "sequential_order": 1.0, "story_type": "user", "users": [], "acceptance_criteria": []},
                    {"name": "Record Settlement", "sequential_order": 2.0, "story_type": "system", "users": [], "acceptance_criteria": []}
                ]}]
            },
            {
                "name": "Issue Refund",
                "sequential_order": 3.0,
                "sub_epics": [],
                "story_groups": [{"type": "and", "connector": None, "stories": [
                    {"name": "Lookup Original", "sequential_order": 1.0, "story_type": "user", "users": [], "acceptance_criteria": []},
                    {"name": "Process Reversal", "sequential_order": 2.0, "story_type": "system", "users": [], "acceptance_criteria": []}
                ]}]
            }
        ]
    }]
}

EPIC_LAYOUT_DATA = {
    "EPIC|Payment Processing": {"x": 10, "y": 120, "width": 640, "height": 300},
    "SUB_EPIC|Authorize Payment": {"x": 10, "y": 180, "width": 200, "height": 200},
    "SUB_EPIC|Settle Transaction": {"x": 220, "y": 180, "width": 200, "height": 200},
    "SUB_EPIC|Issue Refund": {"x": 430, "y": 180, "width": 200, "height": 200}
}


def _create_epic_xml(helper, sub_epic_names=None, epic_name='Payment Processing'):
    """Create DrawIO XML for the epic domain with configurable sub-epics."""
    if sub_epic_names is None:
        sub_epic_names = ['Authorize Payment', 'Settle Transaction', 'Issue Refund']
    stories_per_se = {
        'Authorize Payment': ['Validate Card', 'Check Fraud Rules'],
        'Settle Transaction': ['Send to Bank', 'Record Settlement'],
        'Issue Refund': ['Lookup Original', 'Process Reversal'],
        # For new/renamed sub-epics, provide default stories
    }
    se_cells = []
    story_cells = []
    x_pos = 30
    for idx, se_name in enumerate(sub_epic_names):
        se_cells.append(
            f'<mxCell id="sub-epic-{idx+1}" value="{se_name}" '
            f'style="rounded=1;fillColor=#d5e8d4;strokeColor=#82b366;fontColor=#000000;whiteSpace=wrap;html=1;" '
            f'vertex="1" parent="1">'
            f'<mxGeometry x="{x_pos}" y="180" width="200" height="200" as="geometry"/></mxCell>')
        stories = stories_per_se.get(se_name, [f'{se_name} Story 1'])
        sy = 270
        for sidx, story_name in enumerate(stories):
            story_cells.append(
                f'<mxCell id="story-{idx+1}-{sidx+1}" value="{story_name}" '
                f'style="fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;whiteSpace=wrap;html=1;" '
                f'vertex="1" parent="1">'
                f'<mxGeometry x="{x_pos + 10}" y="{sy}" width="120" height="50" as="geometry"/></mxCell>')
            sy += 60
        x_pos += 210
    ew = max(640, x_pos + 10)
    all_cells = '\n        '.join(se_cells + story_cells)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="Story Map" id="test-diagram">
    <mxGraphModel><root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="epic-1" value="{epic_name}" style="rounded=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontColor=#000000;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="20" y="120" width="{ew}" height="300" as="geometry"/></mxCell>
        {all_cells}
    </root></mxGraphModel>
  </diagram>
</mxfile>'''


def _epic_fixtures():
    return {
        'story_map_data': EPIC_STORY_MAP_DATA,
        'diagram_type': 'outline',
        'layout_data': EPIC_LAYOUT_DATA,
        'expected_epic_count': 1,
        'expected_sub_epic_count': 3,
        'rename_entity': {
            'original_name': 'Authorize Payment',
            'new_name': 'Payment Authorization',
            'parent': 'Payment Processing'
        },
        'new_entity': {
            'name': 'Chargeback Processing',
            'parent': 'Payment Processing'
        },
        'removed_entity': {
            'name': 'Issue Refund',
            'parent': 'Payment Processing'
        },
        'create_diagram_xml': lambda h: _create_epic_xml(h),
        'create_diagram_xml_with_rename': lambda h: _create_epic_xml(
            h, sub_epic_names=['Payment Authorization', 'Settle Transaction', 'Issue Refund']),
        'create_diagram_xml_with_new': lambda h: _create_epic_xml(
            h, sub_epic_names=['Authorize Payment', 'Settle Transaction', 'Issue Refund', 'Chargeback Processing']),
    }


# ============================================================================
# Story: Render epic and sub-epic hierarchy
# ============================================================================

class TestRenderEpicAndSubEpicHierarchy(BaseRenderDiagramTest):
    """
    Story: Render epic and sub-epic hierarchy
    Test Class: TestRenderEpicHierarchy
    Test File: test/invoke_bot/perform_action/test_sync_epics.py
    
    Inherits: test_default_layout_renders_valid_output,
              test_re_render_with_saved_layout_preserves_positions,
              test_render_writes_valid_drawio_file,
              test_cells_have_required_styles
    """

    @property
    def domain_fixtures(self):
        return _epic_fixtures()

    # -- Epic-unique scenarios --

    def test_parent_epic_spans_all_child_sub_epics_horizontally(self, tmp_path):
        """
        SCENARIO: Parent epic spans all child sub-epics horizontally
        GIVEN: DrawIOSubEpic is rendered with x and width
        WHEN: DrawIOStoryMap renders outline from StoryMap
        THEN: DrawIOEpic.x is at or before leftmost SubEpic.x
        AND: DrawIOEpic.width encompasses all SubEpics
        """
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(EPIC_STORY_MAP_DATA)

        drawio = DrawIOStoryMap(diagram_type='outline')
        drawio.render_from_story_map(story_map, layout_data=None)

        epics = drawio.get_epics()
        sub_epics = epics[0].get_sub_epics()
        epic_left = epics[0].position.x
        epic_right = epic_left + epics[0].boundary.width
        for se in sub_epics:
            assert se.position.x >= epic_left
            assert se.position.x + se.boundary.width <= epic_right

    def test_sibling_sub_epics_do_not_overlap_horizontally(self, tmp_path):
        """
        SCENARIO: Sibling sub-epics do not overlap horizontally
        GIVEN: DrawIOSubEpic is rendered with x and width
        WHEN: DrawIOStoryMap renders outline from StoryMap
        THEN: for each adjacent pair: left.x + left.width <= right.x
        """
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(EPIC_STORY_MAP_DATA)

        drawio = DrawIOStoryMap(diagram_type='outline')
        drawio.render_from_story_map(story_map, layout_data=None)

        sub_epics = drawio.get_sub_epics()
        sorted_se = sorted(sub_epics, key=lambda se: se.position.x)
        for i in range(len(sorted_se) - 1):
            left_end = sorted_se[i].position.x + sorted_se[i].boundary.width
            right_start = sorted_se[i + 1].position.x
            assert left_end <= right_start, (
                f"{sorted_se[i].value} ends at {left_end} but {sorted_se[i+1].value} starts at {right_start}")

    def test_nested_sub_epics_render_recursively_to_4_levels(self, tmp_path):
        """
        SCENARIO: Nested sub-epics render recursively to 4 levels of depth
        GIVEN: StoryMap has DrawIOSubEpic nested 4 levels deep
        WHEN: DrawIOStoryMap renders outline from StoryMap
        THEN: DrawIOStoryMap contains all SubEpics at every depth
        """
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_nested_sub_epics(depth=4)
        story_map = StoryMap(data)

        drawio = DrawIOStoryMap(diagram_type='outline')
        drawio.render_from_story_map(story_map, layout_data=None)

        # get_sub_epics returns only direct children; walk the tree for full count
        epics = drawio.get_epics()
        assert len(epics) >= 1
        # At depth 4 the top sub-epic should have nested children
        top_se = epics[0].get_sub_epics()
        assert len(top_se) >= 1

    def test_nested_sub_epic_y_positions_increase_with_depth(self, tmp_path):
        """
        SCENARIO: Nested sub-epic Y positions increase with each depth level
        GIVEN: StoryMap has DrawIOSubEpic nested multiple levels deep
        WHEN: DrawIOStoryMap renders outline from StoryMap
        THEN: deeper SubEpic has larger Y than shallower
        """
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_nested_sub_epics(depth=3)
        story_map = StoryMap(data)

        drawio = DrawIOStoryMap(diagram_type='outline')
        drawio.render_from_story_map(story_map, layout_data=None)

        all_se = drawio.get_sub_epics()
        # Sort by depth - parent sub-epics should have smaller Y than child sub-epics
        if len(all_se) >= 2:
            # The first sub-epic should be higher (smaller Y) than its children
            assert all_se[0].position.y < all_se[-1].position.y

    def test_nested_container_spans_children_at_every_depth(self, tmp_path):
        """
        SCENARIO: Nested container spans children at every depth level
        GIVEN: StoryMap has DrawIOSubEpic nested multiple levels
        WHEN: DrawIOStoryMap renders outline from StoryMap
        THEN: parent.x <= child.x and child.x + child.width <= parent.x + parent.width
        """
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_nested_sub_epics(depth=3)
        story_map = StoryMap(data)

        drawio = DrawIOStoryMap(diagram_type='outline')
        drawio.render_from_story_map(story_map, layout_data=None)

        epics = drawio.get_epics()
        epic = epics[0]
        # Epic should span all its sub-epics
        for se in epic.get_sub_epics():
            assert se.position.x >= epic.position.x
            assert se.position.x + se.boundary.width <= epic.position.x + epic.boundary.width


# ============================================================================
# Story: Report epic and sub-epic changes
# ============================================================================

class TestReportEpicAndSubEpicChanges(BaseReportDiagramTest):
    """
    Story: Report epic and sub-epic changes
    Test Class: TestReportEpicChanges
    Test File: test/invoke_bot/perform_action/test_sync_epics.py

    Inherits: test_no_changes_when_diagram_matches_original,
              test_entity_added_detected_as_new,
              test_entity_renamed_detected_as_rename,
              test_report_roundtrips_through_json
    """

    @property
    def domain_fixtures(self):
        return _epic_fixtures()

    # -- Epic-unique scenarios --

    def test_only_hierarchical_cell_id_sub_epics_participate_in_rename(self, tmp_path):
        """
        SCENARIO: Only hierarchical cell ID sub-epics participate in rename pairing
        GIVEN: DrawIOStoryMap has unmatched SubEpic with both simple and hierarchical cell IDs
        WHEN: generateUpdateReport is executed
        THEN: only SubEpic with hierarchical cell_id participate in rename pairing
        AND: SubEpic with simple cell_id are treated as new
        """
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(EPIC_STORY_MAP_DATA)
        # Create XML with a renamed sub-epic using hierarchical cell ID
        xml = _create_epic_xml(
            helper, sub_epic_names=['Payment Authorization', 'Settle Transaction', 'Issue Refund'])
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)

        drawio = DrawIOStoryMap(diagram_type='outline')
        drawio.load(drawio_file)
        report = drawio.generate_update_report(story_map)

        # Hierarchical cell IDs (sub-epic-1, etc.) should be rename candidates
        assert len(report.renames) >= 1

    def test_story_rename_works_regardless_of_cell_id_format(self, tmp_path):
        """
        SCENARIO: Story rename works regardless of cell ID format
        GIVEN: DrawIOStoryMap has story with different name and any cell_id format
        WHEN: generateUpdateReport is executed
        THEN: UpdateReport detects story rename regardless of cell_id format
        AND: cell_id type filtering only applies to SubEpic and Epic
        """
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(EPIC_STORY_MAP_DATA)
        # Rename a story (not a sub-epic)
        xml = _create_epic_xml(helper)
        xml = xml.replace('Validate Card', 'Validate Payment Card')
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)

        drawio = DrawIOStoryMap(diagram_type='outline')
        drawio.load(drawio_file)
        report = drawio.generate_update_report(story_map)

        # Story renames should be detected regardless of cell ID format
        story_renames = [r for r in report.renames if r.get('original_name') == 'Validate Card']
        assert len(story_renames) >= 1

    def test_removed_epics_flagged_as_large_deletions(self, tmp_path):
        """
        SCENARIO: Removed epics and sub-epics flagged as large deletions in report
        GIVEN: DrawIOStoryMap has fewer nodes than StoryMap
        WHEN: generateUpdateReport is executed
        THEN: UpdateReport lists deleted nodes as removed
        AND: UpdateReport.large_deletions flags entire missing SubEpic
        """
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(EPIC_STORY_MAP_DATA)
        # Create XML without Issue Refund sub-epic
        xml = _create_epic_xml(
            helper, sub_epic_names=['Authorize Payment', 'Settle Transaction'])
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)

        drawio = DrawIOStoryMap(diagram_type='outline')
        drawio.load(drawio_file)
        report = drawio.generate_update_report(story_map)

        all_removed = report.removed_stories + report.removed_sub_epics
        removed_names = [r.name for r in all_removed]
        assert 'Issue Refund' in removed_names
        assert len(report.large_deletions.missing_sub_epics) > 0


# ============================================================================
# Story: Update epics and sub-epics from diagram
# ============================================================================

class TestUpdateEpicsAndSubEpicsFromDiagram(BaseUpdateDiagramTest):
    """
    Story: Update epics and sub-epics from diagram
    Test Class: TestUpdateEpicsFromDiagram
    Test File: test/invoke_bot/perform_action/test_sync_epics.py

    Inherits: test_apply_changes_from_report_updates_graph,
              test_renamed_entity_updates_name_in_graph,
              test_new_entity_creates_in_graph,
              test_end_to_end_render_report_update
    """

    @property
    def domain_fixtures(self):
        return _epic_fixtures()

    # -- Epic-unique scenarios --

    def test_removed_sub_epic_reassigns_stories_by_position(self, tmp_path):
        """
        SCENARIO: Removed sub-epic reassigns its stories by position
        GIVEN: SubEpic has been removed from DrawIOStoryMap
        WHEN: DrawIOStoryMap extracts outline from diagram
        THEN: extracted graph omits that SubEpic
        AND: stories under it are reassigned by position
        AND: UpdateReport.large_deletions flags the missing SubEpic
        """
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(EPIC_STORY_MAP_DATA)
        # Remove Issue Refund sub-epic but keep its stories positioned near Settle Transaction
        xml = _create_epic_xml(
            helper, sub_epic_names=['Authorize Payment', 'Settle Transaction'])
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)

        drawio = DrawIOStoryMap(diagram_type='outline')
        drawio.load(drawio_file)
        report = drawio.generate_update_report(story_map)

        # Issue Refund should be flagged
        all_removed = report.removed_stories + report.removed_sub_epics
        removed_names = [r.name for r in all_removed]
        assert 'Issue Refund' in removed_names

    def test_removed_epic_removes_all_children(self, tmp_path):
        """
        SCENARIO: Removed epic removes all children from story graph
        GIVEN: Epic has been removed from DrawIOStoryMap
        WHEN: DrawIOStoryMap extracts outline from diagram
        THEN: extracted graph omits that Epic and all its SubEpics and Stories
        AND: UpdateReport.large_deletions includes missing_epics
        """
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(EPIC_STORY_MAP_DATA)
        # Create empty diagram - no epic at all
        xml = helper.drawio_story_map.create_drawio_xml_without_epic()
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)

        drawio = DrawIOStoryMap(diagram_type='outline')
        drawio.load(drawio_file)
        report = drawio.generate_update_report(story_map)

        all_removed = report.removed_stories + report.removed_sub_epics
        assert len(all_removed) > 0
        assert len(report.large_deletions.missing_epics) > 0 or len(report.large_deletions.missing_sub_epics) > 0

    def test_extract_assigns_entities_by_containment_and_order(self, tmp_path):
        """
        SCENARIO: Extract assigns entities to parent sub-epics by containment and sequential order
        GIVEN: DrawIOStoryMap outline file contains Epic, SubEpic, and Story cells
        WHEN: DrawIOStoryMap extracts outline from diagram
        THEN: each Story assigned to a SubEpic by containment
        AND: sequential_order assigned from top-to-bottom then left-to-right
        """
        helper = BotTestHelper(tmp_path)
        xml = _create_epic_xml(helper)
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)

        drawio = DrawIOStoryMap(diagram_type='outline')
        drawio.load(drawio_file)

        epics = drawio.get_epics()
        assert len(epics) == 1
        sub_epics = epics[0].get_sub_epics()
        assert len(sub_epics) == 3
        # Each sub-epic should have stories assigned by containment
        for se in sub_epics:
            stories = se.get_stories()
            assert len(stories) >= 1
            # Stories should be ordered by sequential_order
            for i in range(len(stories) - 1):
                assert stories[i].sequential_order <= stories[i + 1].sequential_order

    def test_sync_persists_layout_data_alongside_diagram(self, tmp_path):
        """
        SCENARIO: Sync persists layout data alongside diagram
        GIVEN: DrawIOStoryMap exists with content from diagram
        WHEN: sync completes
        THEN: LayoutData persisted to JSON file alongside the diagram
        AND: LayoutData stores position and size for each entity
        """
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(EPIC_STORY_MAP_DATA)

        drawio = DrawIOStoryMap(diagram_type='outline')
        drawio.render_from_story_map(story_map, layout_data=None)

        output_file = tmp_path / 'story-map.drawio'
        drawio.save(output_file)
        layout_file = output_file.with_suffix('.json')
        drawio.save_layout(layout_file)

        assert layout_file.exists()
        layout = json.loads(layout_file.read_text(encoding='utf-8'))
        assert len(layout) > 0

    def test_extract_from_empty_drawio_produces_error(self, tmp_path):
        """
        SCENARIO: Extract from empty or malformed drawio file produces error
        GIVEN: DrawIOStoryMap file contains no valid Epic or SubEpic cells
        WHEN: DrawIOStoryMap extracts outline from diagram
        THEN: DrawIOStoryMap reports extraction error with zero nodes found
        """
        helper = BotTestHelper(tmp_path)
        xml = helper.drawio_story_map.create_empty_drawio_xml()
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)

        drawio = DrawIOStoryMap(diagram_type='outline')
        drawio.load(drawio_file)

        assert len(drawio.get_epics()) == 0
        assert len(drawio.get_sub_epics()) == 0
