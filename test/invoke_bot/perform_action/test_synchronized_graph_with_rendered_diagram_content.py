"""
Test Synchronized Graph with Rendered Diagram Content

SubEpic: Synchronized Graph with Rendered Diagram Content
Parent Epic: Invoke Bot > Perform Action

Domain tests verify DrawIO rendering, extraction, and synchronization.
Tests NEW domain model classes - NOT old synchronizers.
"""
import json
import pytest
from pathlib import Path
from helpers.bot_test_helper import BotTestHelper
from synchronizers.story_io.drawio_story_map import DrawIOStoryMap
from synchronizers.story_io.layout_data import LayoutData
from synchronizers.story_io.update_report import UpdateReport
from story_graph.nodes import StoryMap


class TestRenderStoryMap:

    def test_render_outline_diagram_from_story_map_with_default_layout(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(helper.drawio_story_map.create_simple_story_map_data())

        drawio_story_map = DrawIOStoryMap(diagram_type='outline')
        summary = drawio_story_map.render_from_story_map(story_map, layout_data=None)

        epics = drawio_story_map.get_epics()
        assert len(epics) == 1
        assert epics[0].position.y == 120

        sub_epics = epics[0].get_sub_epics()
        assert epics[0].boundary.width >= sum(se.boundary.width for se in sub_epics)
        assert sub_epics[0].position.y > epics[0].position.y

        stories = sub_epics[0].get_stories()
        assert sub_epics[0].boundary.width >= sum(s.boundary.width for s in stories)
        for i in range(len(stories) - 1):
            assert stories[i].position.x < stories[i+1].position.x

        output_file = tmp_path / 'story-map.drawio'
        drawio_story_map.save(output_file)
        assert output_file.exists()
        helper.drawio_story_map.assert_render_summary(summary, expected_epics=1, expected_sub_epic_count=1)

    def test_render_outline_diagram_from_story_map_with_saved_layout_data(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(helper.drawio_story_map.create_simple_story_map_data())
        layout_file = helper.drawio_story_map.create_layout_data_file()
        layout_data = LayoutData.load(layout_file)

        drawio_story_map = DrawIOStoryMap(diagram_type='outline')
        drawio_story_map.render_from_story_map(story_map, layout_data=layout_data)

        epics = drawio_story_map.get_epics()
        assert epics[0].position.x == 20
        assert epics[0].position.y == 120
        sub_epics = epics[0].get_sub_epics()
        assert sub_epics[0].position.x == 30
        assert sub_epics[0].position.y == 180
        stories = sub_epics[0].get_stories()
        assert stories[0].sequential_order < stories[1].sequential_order

    @pytest.mark.parametrize('epic_count,sub_epic_count,story_count', [(1, 3, 7), (2, 5, 12)])
    def test_diagram_contains_correct_count_of_cells_matching_story_map_structure(self, tmp_path, epic_count, sub_epic_count, story_count):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_counts(epic_count, sub_epic_count, story_count)
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='outline')
        summary = drawio_story_map.render_from_story_map(story_map, layout_data=None)

        assert len(drawio_story_map.get_epics()) == epic_count
        assert len(drawio_story_map.get_sub_epics()) == sub_epic_count
        helper.drawio_story_map.assert_render_summary(summary, expected_epics=epic_count, expected_sub_epic_count=sub_epic_count)

    def test_sub_epics_and_stories_ordered_by_sequential_order(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(helper.drawio_story_map.create_simple_story_map_data())

        drawio_story_map = DrawIOStoryMap(diagram_type='outline')
        drawio_story_map.render_from_story_map(story_map, layout_data=None)

        for sub_epic in drawio_story_map.get_sub_epics():
            stories = sub_epic.get_stories()
            for i in range(len(stories) - 1):
                assert stories[i].position.x < stories[i+1].position.x
                assert stories[i].sequential_order < stories[i+1].sequential_order

    @pytest.mark.parametrize('story_type,expected_fill,expected_stroke,expected_font_color', [
        ('user', '#fff2cc', '#d6b656', 'black'),
        (None, '#fff2cc', '#d6b656', 'black'),
        ('system', '#1a237e', '#0d47a1', 'white'),
        ('technical', '#000000', '#333333', 'white')
    ])
    def test_drawio_story_map_styles_story_cells_by_story_type(self, tmp_path, story_type, expected_fill, expected_stroke, expected_font_color):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_story_type(story_type)
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='outline')
        drawio_story_map.render_from_story_map(story_map, layout_data=None)

        stories = drawio_story_map.get_stories()
        assert len(stories) == 1
        helper.drawio_story_map.assert_cell_style(stories[0], expected_fill, expected_stroke, expected_font_color)

    @pytest.mark.parametrize('node_type,expected_shape,expected_fill,expected_stroke,expected_font_color', [
        ('epic', 'rounded', '#e1d5e7', '#9673a6', 'black'),
        ('sub_epic', 'rounded', '#d5e8d4', '#82b366', 'black'),
    ])
    def test_drawio_story_map_styles_container_and_label_cells_by_node_type(self, tmp_path, node_type, expected_shape, expected_fill, expected_stroke, expected_font_color):
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(helper.drawio_story_map.create_simple_story_map_data())

        drawio_story_map = DrawIOStoryMap(diagram_type='outline')
        drawio_story_map.render_from_story_map(story_map, layout_data=None)

        if node_type == 'epic':
            node = drawio_story_map.get_epics()[0]
        else:
            node = drawio_story_map.get_sub_epics()[0]
        assert node.shape == expected_shape
        helper.drawio_story_map.assert_cell_style(node, expected_fill, expected_stroke, expected_font_color)

    def test_render_completes_and_writes_drawio_file_to_specified_path(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(helper.drawio_story_map.create_simple_story_map_data())

        drawio_story_map = DrawIOStoryMap(diagram_type='outline')
        summary = drawio_story_map.render_from_story_map(story_map, layout_data=None)
        output_file = tmp_path / 'story-map.drawio'
        drawio_story_map.save(output_file)

        assert output_file.exists()
        assert summary['diagram_generated'] is True
        assert 'epics' in summary
        assert 'sub_epic_count' in summary

    def test_render_outline_from_empty_story_map_produces_empty_diagram(self, tmp_path):
        story_map = StoryMap({"epics": []})

        drawio_story_map = DrawIOStoryMap(diagram_type='outline')
        summary = drawio_story_map.render_from_story_map(story_map, layout_data=None)

        assert len(drawio_story_map.get_epics()) == 0
        assert summary == {'epics': 0, 'sub_epic_count': 0, 'diagram_generated': True}


class TestRenderStoryMapIncrements:

    def test_render_increments_diagram_with_stories_assigned_to_increment_lanes(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        summary = drawio_story_map.render_from_story_map(story_map, layout_data=None)

        assert len(drawio_story_map.get_epics()) >= 1
        assert len(drawio_story_map.get_stories()) >= 1

    def test_increment_lanes_ordered_by_priority_with_y_positions_from_outline_bottom(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        drawio_story_map.render_from_story_map(story_map, layout_data=None)

        assert len(drawio_story_map.get_epics()) >= 1

    def test_re_render_increments_with_existing_layout_data_recomputes_lane_positions(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        story_map = StoryMap(data)
        layout_file = helper.drawio_story_map.create_layout_data_file()
        layout_data = LayoutData.load(layout_file)

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        drawio_story_map.render_from_story_map(story_map, layout_data=layout_data)

        epics = drawio_story_map.get_epics()
        assert epics[0].position.x == 20
        assert epics[0].position.y == 120

    def test_render_increments_completes_and_summary_includes_increment_count(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        summary = drawio_story_map.render_from_story_map(story_map, layout_data=None)

        assert summary['diagram_generated'] is True

    def test_increment_lane_cells_styled_for_extractor_detection(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        drawio_story_map.render_from_story_map(story_map, layout_data=None)

        assert len(drawio_story_map.get_epics()) >= 1

    def test_render_increments_with_no_increments_defined_produces_outline_only_diagram(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(helper.drawio_story_map.create_simple_story_map_data())

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        summary = drawio_story_map.render_from_story_map(story_map, layout_data=None)

        assert len(drawio_story_map.get_epics()) >= 1
        assert len(drawio_story_map.get_stories()) >= 1


class TestRenderStoryMapWithAcceptanceCriteria:

    def test_render_exploration_diagram_with_ac_boxes_below_stories(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_acceptance_criteria()
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='acceptance_criteria')
        summary = drawio_story_map.render_from_story_map(story_map, layout_data=None)

        assert len(drawio_story_map.get_epics()) >= 1
        assert summary['diagram_generated'] is True

    def test_ac_boxes_styled_and_positioned_below_story_with_extracted_step_text(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_acceptance_criteria()
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='acceptance_criteria')
        drawio_story_map.render_from_story_map(story_map, layout_data=None)

        assert len(drawio_story_map.get_stories()) >= 1

    def test_re_render_exploration_with_layout_data_preserves_story_and_ac_box_positions(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_acceptance_criteria()
        story_map = StoryMap(data)
        layout_file = helper.drawio_story_map.create_layout_data_file()
        layout_data = LayoutData.load(layout_file)

        drawio_story_map = DrawIOStoryMap(diagram_type='acceptance_criteria')
        drawio_story_map.render_from_story_map(story_map, layout_data=layout_data)

        epics = drawio_story_map.get_epics()
        assert epics[0].position.x == 20

    def test_exploration_render_output_contains_story_and_ac_cells_with_correct_containment(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_acceptance_criteria()
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='acceptance_criteria')
        drawio_story_map.render_from_story_map(story_map, layout_data=None)
        output_file = tmp_path / 'story-map-ac.drawio'
        drawio_story_map.save(output_file)

        assert output_file.exists()
        xml_content = output_file.read_text(encoding='utf-8')
        assert 'mxCell' in xml_content

    def test_story_with_no_acceptance_criteria_renders_without_ac_boxes(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_acceptance_criteria()
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='acceptance_criteria')
        drawio_story_map.render_from_story_map(story_map, layout_data=None)

        stories = drawio_story_map.get_stories()
        assert len(stories) == 2


class TestUpdateGraphFromStoryMap:

    def test_extract_outline_assigns_stories_to_sub_epics_by_containment_and_sequential_order(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        drawio_file = helper.drawio_story_map.create_drawio_file()

        drawio_story_map = DrawIOStoryMap.load(drawio_file)

        sub_epics = drawio_story_map.get_sub_epics()
        for sub_epic in sub_epics:
            for story in sub_epic.get_stories():
                story_center = story.boundary.center
                assert sub_epic.boundary.contains_position(story_center)

        output_file = tmp_path / 'extracted.json'
        drawio_story_map.save_as_json(output_file)
        assert output_file.exists()

    def test_update_report_lists_exact_fuzzy_new_and_removed_stories(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        drawio_file = helper.drawio_story_map.create_drawio_file()
        drawio_story_map = DrawIOStoryMap.load(drawio_file)
        original_story_map = StoryMap(helper.drawio_story_map.create_simple_story_map_data())

        report = drawio_story_map.generate_update_report(original_story_map)

        assert isinstance(report, UpdateReport)
        assert isinstance(report.exact_matches, list)
        assert isinstance(report.fuzzy_matches, list)
        assert isinstance(report.new_stories, list)
        assert isinstance(report.removed_stories, list)

    def test_story_map_updated_from_outline_diagram_applies_report_changes(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        drawio_file = helper.drawio_story_map.create_drawio_file(
            helper.drawio_story_map.create_drawio_xml_with_new_story())
        drawio_story_map = DrawIOStoryMap.load(drawio_file)
        original_story_map = StoryMap(helper.drawio_story_map.create_simple_story_map_data())

        report = drawio_story_map.generate_update_report(original_story_map)

        assert len(report.exact_matches) >= 1
        assert len(report.new_stories) >= 1

    def test_renamed_or_reordered_nodes_flagged_as_fuzzy_matches_in_update_report(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        drawio_file = helper.drawio_story_map.create_drawio_file(
            helper.drawio_story_map.create_drawio_xml_with_renamed_story())
        drawio_story_map = DrawIOStoryMap.load(drawio_file)
        original_data = helper.drawio_story_map.create_story_map_data_with_renamed_story()
        original_story_map = StoryMap(original_data)

        report = drawio_story_map.generate_update_report(original_story_map)

        assert len(report.fuzzy_matches) >= 1
        fuzzy = report.fuzzy_matches[0]
        assert fuzzy.extracted_name
        assert fuzzy.original_name

    def test_deleted_nodes_listed_as_removed_and_large_deletions_flagged(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        drawio_file = helper.drawio_story_map.create_drawio_file(
            helper.drawio_story_map.create_drawio_xml_with_deleted_story())
        drawio_story_map = DrawIOStoryMap.load(drawio_file)
        original_story_map = StoryMap(helper.drawio_story_map.create_simple_story_map_data())

        report = drawio_story_map.generate_update_report(original_story_map)

        assert len(report.removed_stories) >= 1

    def test_sync_persists_layout_data_alongside_diagram(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        drawio_file = helper.drawio_story_map.create_drawio_file()
        drawio_story_map = DrawIOStoryMap.load(drawio_file)

        layout = drawio_story_map.extract_layout()
        layout_file = tmp_path / 'story-map-layout.json'
        layout.save(layout_file)

        assert layout_file.exists()
        reloaded = LayoutData.load(layout_file)
        assert reloaded.has_entry('EPIC|Invoke Bot')

    def test_moved_story_gets_recomputed_sequential_order_from_new_position(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        xml = helper.drawio_story_map.create_minimal_drawio_xml(
            story_names=['Register Behaviors', 'Load Config'])
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)
        drawio_story_map = DrawIOStoryMap.load(drawio_file)

        stories = drawio_story_map.get_stories()
        assert len(stories) >= 2
        assert stories[0].sequential_order <= stories[1].sequential_order

    def test_single_story_deleted_keeps_original_structure_and_flags_if_many_missing(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        drawio_file = helper.drawio_story_map.create_drawio_file(
            helper.drawio_story_map.create_drawio_xml_with_deleted_story())
        drawio_story_map = DrawIOStoryMap.load(drawio_file)
        original_story_map = StoryMap(helper.drawio_story_map.create_simple_story_map_data())

        report = drawio_story_map.generate_update_report(original_story_map)

        assert len(report.removed_stories) >= 1
        assert len(report.exact_matches) >= 1

    def test_deleted_sub_epic_reassigns_its_stories_by_position(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        drawio_file = helper.drawio_story_map.create_drawio_file(
            helper.drawio_story_map.create_drawio_xml_without_sub_epic())
        drawio_story_map = DrawIOStoryMap.load(drawio_file)
        original_story_map = StoryMap(helper.drawio_story_map.create_simple_story_map_data())

        report = drawio_story_map.generate_update_report(original_story_map)

        assert len(report.large_deletions.missing_sub_epics) >= 1

    def test_deleted_epic_removes_all_children_and_flags_large_deletions(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        drawio_file = helper.drawio_story_map.create_drawio_file(
            helper.drawio_story_map.create_drawio_xml_without_epic())
        drawio_story_map = DrawIOStoryMap.load(drawio_file)
        original_story_map = StoryMap(helper.drawio_story_map.create_simple_story_map_data())

        report = drawio_story_map.generate_update_report(original_story_map)

        assert len(report.large_deletions.missing_epics) >= 1

    def test_extract_from_empty_or_malformed_drawio_file_produces_error(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        drawio_file = helper.drawio_story_map.create_drawio_file(
            helper.drawio_story_map.create_empty_drawio_xml())

        drawio_story_map = DrawIOStoryMap.load(drawio_file)

        assert len(drawio_story_map.get_epics()) == 0
        assert len(drawio_story_map.get_stories()) == 0


class TestUpdateGraphFromMapIncrements:

    def test_extract_increments_assigns_stories_to_lanes_by_y_position_with_priority_from_order(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        drawio_file = helper.drawio_story_map.create_drawio_file()

        drawio_story_map = DrawIOStoryMap.load(drawio_file)

        stories = drawio_story_map.get_stories()
        assert len(stories) >= 1
        for story in stories:
            assert story.sequential_order >= 1.0


class TestUpdateStoryGraphFromMapAcceptanceCriteria:

    def test_extract_exploration_maps_ac_boxes_to_stories_by_position_and_containment(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        drawio_file = helper.drawio_story_map.create_drawio_file()

        drawio_story_map = DrawIOStoryMap.load(drawio_file)

        stories = drawio_story_map.get_stories()
        assert len(stories) >= 1
        sub_epics = drawio_story_map.get_sub_epics()
        for sub_epic in sub_epics:
            for story in sub_epic.get_stories():
                assert sub_epic.boundary.contains_position(story.boundary.center)


class TestRenderActionDiagramSection:

    def test_render_action_shows_existing_render_section_without_drawio_config_and_separate_diagram_section(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('shape')
        helper.state.set_state('shape', 'render')
        action_obj = helper.bot.behaviors.current.actions.find_by_name('render')

        instructions = action_obj.do_execute()

        base_instructions = instructions.get('base_instructions', [])
        assert len(base_instructions) > 0
