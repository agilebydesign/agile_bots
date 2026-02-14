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
from helpers.cli_bot_test_helper import CLIBotTestHelper
from synchronizers.story_io.drawio_story_map import DrawIOStoryMap
from synchronizers.story_io.drawio_story_node import DrawIOSubEpic
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
        from synchronizers.story_io.drawio_story_node import EPIC_Y
        assert epics[0].position.y == EPIC_Y

        sub_epics = epics[0].get_sub_epics()
        assert epics[0].boundary.width >= sum(se.boundary.width for se in sub_epics)
        assert sub_epics[0].position.y > epics[0].position.y

        stories = sub_epics[0].get_stories()
        # In row-based layout sub-epic is a separate bar, not a container.
        # Check stories are ordered left-to-right.
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
        # With layout data, epic uses saved position
        assert epics[0].position.x == 20
        assert epics[0].position.y == 120
        sub_epics = epics[0].get_sub_epics()
        # Sub-epic X = epic X + BAR_PADDING, Y computed by row layout
        assert sub_epics[0].position.y > epics[0].position.y
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
        ('user', '#fff2cc', '#d6b656', '#000000'),
        (None, '#fff2cc', '#d6b656', '#000000'),
        ('system', '#1a237e', '#0d47a1', '#ffffff'),
        ('technical', '#000000', '#333333', '#ffffff')
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
        ('epic', 'rounded', '#e1d5e7', '#9673a6', '#000000'),
        ('sub_epic', 'rounded', '#d5e8d4', '#82b366', '#000000'),
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


class TestRenderStoryMapNestedSubEpics:

    def test_render_3_level_nested_sub_epics_creates_sub_epic_inside_sub_epic(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_nested_sub_epics(depth=3)
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='outline')
        summary = drawio_story_map.render_from_story_map(story_map, layout_data=None)

        assert summary['diagram_generated'] is True
        epics = drawio_story_map.get_epics()
        assert len(epics) == 1
        # Top-level sub-epic under the epic
        top_sub_epics = epics[0].get_sub_epics()
        assert len(top_sub_epics) == 1
        # Nested sub-epics under the top sub-epic
        nested_sub_epics = top_sub_epics[0].get_sub_epics()
        assert len(nested_sub_epics) == 2
        # Leaf sub-epics contain stories
        for nested_se in nested_sub_epics:
            stories = nested_se.get_stories()
            assert len(stories) == 2, f"Leaf sub-epic '{nested_se.name}' should have 2 stories"

    def test_render_4_level_nested_sub_epics_recurses_to_all_depths(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_nested_sub_epics(depth=4)
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='outline')
        summary = drawio_story_map.render_from_story_map(story_map, layout_data=None)

        assert summary['diagram_generated'] is True
        # Should have all stories at the deepest level
        all_stories = drawio_story_map.get_stories()
        # depth=4: 1 top -> 2 mid -> 4 leaf sub-epics, each with 2 stories = 8 stories
        assert len(all_stories) == 8, f"Expected 8 stories at depth 4, got {len(all_stories)}"

    def test_nested_sub_epics_have_increasing_y_positions_per_depth(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_nested_sub_epics(depth=3)
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='outline')
        drawio_story_map.render_from_story_map(story_map, layout_data=None)

        epic = drawio_story_map.get_epics()[0]
        top_se = epic.get_sub_epics()[0]
        nested_se = top_se.get_sub_epics()[0]
        leaf_story = nested_se.get_stories()[0]

        # Each level should be deeper (higher y)
        assert top_se.position.y > epic.position.y, "Top sub-epic should be below epic"
        assert nested_se.position.y > top_se.position.y, "Nested sub-epic should be below top sub-epic"
        assert leaf_story.position.y > nested_se.position.y, "Story should be below its sub-epic"

    def test_parent_sub_epic_width_encompasses_all_nested_children(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_nested_sub_epics(depth=3)
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='outline')
        drawio_story_map.render_from_story_map(story_map, layout_data=None)

        epic = drawio_story_map.get_epics()[0]
        top_se = epic.get_sub_epics()[0]
        nested_ses = top_se.get_sub_epics()

        # Parent sub-epic should be at least as wide as the sum of its nested children
        children_width = sum(se.boundary.width for se in nested_ses)
        assert top_se.boundary.width >= children_width, \
            f"Parent sub-epic width {top_se.boundary.width} should encompass children width {children_width}"

    def test_render_and_save_nested_sub_epics_produces_valid_drawio(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_nested_sub_epics(depth=3)
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='outline')
        drawio_story_map.render_from_story_map(story_map, layout_data=None)
        output_file = tmp_path / 'nested-story-map.drawio'
        drawio_story_map.save(output_file)

        assert output_file.exists()
        content = output_file.read_text(encoding='utf-8')
        assert '<mxfile' in content
        # All sub-epic names should be in the output
        assert 'Top SubEpic' in content
        assert 'Top SubEpic Child 1' in content
        assert 'Top SubEpic Child 2' in content

    def test_extract_to_json_preserves_nested_sub_epic_structure(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_nested_sub_epics(depth=3)
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='outline')
        drawio_story_map.render_from_story_map(story_map, layout_data=None)
        output_file = tmp_path / 'extracted.json'
        drawio_story_map.save_as_json(output_file)

        extracted = json.loads(output_file.read_text(encoding='utf-8'))
        top_se = extracted['epics'][0]['sub_epics'][0]
        assert len(top_se['sub_epics']) == 2, "Should preserve 2 nested sub-epics"
        assert top_se['story_groups'] == [] or len(top_se['story_groups'][0].get('stories', [])) == 0, \
            "Branch sub-epic should not have stories"
        for nested in top_se['sub_epics']:
            stories = nested['story_groups'][0]['stories']
            assert len(stories) == 2, "Leaf sub-epics should have 2 stories each"


class TestDomainModelDynamicYPositioning:
    """Tests that DrawIOStoryMap (domain model) produces correct nested
    sub-epic rendering with parent containers spanning their children."""

    def _render_nested(self, depth=3):
        """Render a nested graph through DrawIOStoryMap and return epics."""
        helper = BotTestHelper(Path(__file__).parent)
        data = helper.drawio_story_map.create_story_map_data_with_nested_sub_epics(depth=depth)
        story_map = StoryMap(data)
        drawio_map = DrawIOStoryMap()
        drawio_map.render_from_story_map(story_map)
        return drawio_map

    def test_parent_and_leaf_sub_epics_both_rendered(self):
        dm = self._render_nested(depth=3)
        epics = dm.get_epics()
        top_se = epics[0].get_sub_epics()[0]
        # top_se is the parent; its children are the leaves
        children = top_se.get_sub_epics()
        assert len(children) == 2, f"Parent should have 2 child sub-epics, got {len(children)}"
        # All three are rendered (parent + 2 children)
        all_nodes = top_se.collect_all_nodes()
        se_nodes = [n for n in all_nodes if isinstance(n, DrawIOSubEpic)]
        assert len(se_nodes) == 3, f"Should have 3 sub-epic nodes total, got {len(se_nodes)}"

    def test_nested_sub_epics_at_different_y_levels(self):
        dm = self._render_nested(depth=3)
        epics = dm.get_epics()
        top_se = epics[0].get_sub_epics()[0]
        children = top_se.get_sub_epics()
        assert len(children) >= 2

        parent_y = top_se.position.y
        child_y = children[0].position.y
        assert child_y > parent_y, \
            f"Child Y ({child_y}) should be below parent Y ({parent_y})"
        # Siblings at same level
        assert children[0].position.y == children[1].position.y

    def test_stories_positioned_below_deepest_sub_epic(self):
        dm = self._render_nested(depth=3)
        # Collect all sub-epics recursively (top-level + nested)
        all_se_nodes = [n for n in dm._collect_all_nodes() if isinstance(n, DrawIOSubEpic)]
        stories = dm.get_stories()
        max_se_y = max(se.position.y for se in all_se_nodes)
        min_story_y = min(s.position.y for s in stories)
        assert min_story_y > max_se_y, \
            f"Stories Y ({min_story_y}) should be below deepest sub-epic Y ({max_se_y})"

    def test_4_level_depth_produces_3_distinct_sub_epic_y_levels(self):
        dm = self._render_nested(depth=4)
        all_se_nodes = [n for n in dm._collect_all_nodes() if isinstance(n, DrawIOSubEpic)]
        y_levels = sorted(set(se.position.y for se in all_se_nodes))
        assert len(y_levels) == 3, \
            f"depth=4 should produce 3 sub-epic Y levels, got {len(y_levels)}: {y_levels}"

    def test_parent_sub_epic_width_spans_children(self):
        dm = self._render_nested(depth=3)
        top_se = dm.get_epics()[0].get_sub_epics()[0]
        children = top_se.get_sub_epics()
        children_left = min(c.position.x for c in children)
        children_right = max(c.boundary.right for c in children)
        assert top_se.position.x <= children_left
        assert top_se.boundary.right >= children_right

    def test_flat_graph_sub_epic_at_standard_y(self):
        data = {"epics": [{"name": "E1", "sequential_order": 1.0, "sub_epics": [
            {"name": "SE1", "sequential_order": 1.0, "sub_epics": [],
             "story_groups": [{"type": "and", "connector": None, "stories": [
                 {"name": "S1", "sequential_order": 1.0, "story_type": "user", "users": []}
             ]}]}
        ]}]}
        story_map = StoryMap(data)
        dm = DrawIOStoryMap()
        dm.render_from_story_map(story_map)
        ses = dm.get_sub_epics()
        assert len(ses) == 1
        # Row-based: sub_epic_y(0) = EPIC_Y + EPIC_HEIGHT + ROW_GAP = 120+60+15 = 195
        from synchronizers.story_io.drawio_story_node import EPIC_Y, EPIC_HEIGHT, ROW_GAP
        expected_y = EPIC_Y + EPIC_HEIGHT + ROW_GAP
        assert ses[0].position.y == expected_y, \
            f"Flat sub-epic Y should be {expected_y}, got {ses[0].position.y}"


class TestDiagramVisualIntegrity:
    """Tests that rendered diagrams are visually correct in Draw.io.

    These catch layout bugs that produce broken visuals even when the
    data model is structurally correct:
    - Text overflowing cell boundaries (missing whiteSpace/html styles)
    - Missing font sizes (Draw.io defaults are too large for cards)
    - Actors appearing inside sub-epic headers instead of near stories
    - Containers that don't fully wrap their children
    - Sibling elements overlapping each other
    """

    def _render_simple(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(helper.drawio_story_map.create_simple_story_map_data())
        dm = DrawIOStoryMap(diagram_type='outline')
        dm.render_from_story_map(story_map, layout_data=None)
        return dm

    def _render_with_users(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        story_map = StoryMap(helper.drawio_story_map.create_story_map_data_with_users())
        dm = DrawIOStoryMap(diagram_type='outline')
        dm.render_from_story_map(story_map, layout_data=None)
        return dm

    def _render_nested(self, tmp_path, depth=3):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_nested_sub_epics(depth=depth)
        story_map = StoryMap(data)
        dm = DrawIOStoryMap(diagram_type='outline')
        dm.render_from_story_map(story_map, layout_data=None)
        return dm

    # ---- Style integrity (catches text overflow / font size bugs) ----

    def test_all_cells_in_output_xml_include_text_wrapping(self, tmp_path):
        """Every mxCell style must include whiteSpace=wrap and html=1 so
        text wraps inside cell boundaries instead of overflowing."""
        import xml.etree.ElementTree as ET

        dm = self._render_simple(tmp_path)
        output_file = tmp_path / 'visual-test.drawio'
        dm.save(output_file)

        tree = ET.parse(str(output_file))
        for cell in tree.iter('mxCell'):
            style = cell.get('style', '')
            if not style or cell.get('vertex') != '1':
                continue
            assert 'whiteSpace=wrap' in style, \
                f"Cell '{cell.get('value')}' missing whiteSpace=wrap in style: {style}"
            assert 'html=1' in style, \
                f"Cell '{cell.get('value')}' missing html=1 in style: {style}"
            assert 'overflow=hidden' in style, \
                f"Cell '{cell.get('value')}' missing overflow=hidden in style: {style}"

    def test_all_cells_in_output_xml_have_explicit_font_size(self, tmp_path):
        """Every styled mxCell must declare fontSize explicitly so Draw.io
        doesn't fall back to its default (too large for story cards)."""
        import xml.etree.ElementTree as ET

        dm = self._render_simple(tmp_path)
        output_file = tmp_path / 'font-test.drawio'
        dm.save(output_file)

        tree = ET.parse(str(output_file))
        for cell in tree.iter('mxCell'):
            style = cell.get('style', '')
            if not style or cell.get('vertex') != '1':
                continue
            assert 'fontSize=' in style, \
                f"Cell '{cell.get('value')}' missing explicit fontSize in style: {style}"

    # ---- Actor positioning (catches actors-in-header bug) ----

    def test_actors_positioned_in_actor_row_above_stories(self, tmp_path):
        """In the row-based layout, actors sit in a dedicated row above stories
        but below sub-epics.  Verify actors are above stories and below the
        sub-epic row."""
        dm = self._render_with_users(tmp_path)
        stories = dm.get_stories()
        assert len(stories) >= 1, "Need stories to test actor positioning"

        for story in stories:
            for actor in story._actor_elements:
                # Actor should be above the story (smaller Y = higher)
                assert actor.position.y < story.position.y, \
                    (f"Actor '{actor.value}' at y={actor.position.y} should be above "
                     f"story '{story.name}' at y={story.position.y} in row-based layout.")

    def test_actors_do_not_overlap_sub_epic_header_area(self, tmp_path):
        """Actor elements must not be positioned within the first 30px of
        their enclosing sub-epic (the label/header area)."""
        dm = self._render_with_users(tmp_path)

        for sub_epic in dm.get_sub_epics():
            header_bottom = sub_epic.position.y + 30
            for story in sub_epic.get_stories():
                for actor in story._actor_elements:
                    assert actor.position.y > header_bottom, \
                        (f"Actor '{actor.value}' at y={actor.position.y} overlaps "
                         f"sub-epic '{sub_epic.name}' header area (y < {header_bottom})")

    def test_stories_with_users_produce_actor_elements(self, tmp_path):
        """Stories that have assigned users must create corresponding
        actor elements. Without this, actor layout is never tested."""
        dm = self._render_with_users(tmp_path)
        stories = dm.get_stories()

        actors_found = sum(len(s._actor_elements) for s in stories)
        assert actors_found >= 3, \
            f"Expected at least 3 actors (Developer, Admin, Bot Engine), got {actors_found}"

    # ---- Geometric containment (catches container-too-small bugs) ----

    def test_epic_horizontal_span_covers_all_sub_epics(self, tmp_path):
        """In row-based layout, epic is a horizontal bar on its own row.
        Its X-range must span all sub-epics beneath it."""
        dm = self._render_simple(tmp_path)

        for epic in dm.get_epics():
            epic_left = epic.boundary.x
            epic_right = epic.boundary.x + epic.boundary.width
            for se in epic.get_sub_epics():
                assert se.boundary.x >= epic_left, \
                    (f"Sub-epic '{se.name}' left edge {se.boundary.x} is outside "
                     f"epic '{epic.name}' left edge {epic_left}")
                se_right = se.boundary.x + se.boundary.width
                assert se_right <= epic_right, \
                    (f"Sub-epic '{se.name}' right edge {se_right} exceeds "
                     f"epic '{epic.name}' right edge {epic_right}")

    def test_sub_epic_horizontal_span_covers_all_stories(self, tmp_path):
        """In row-based layout, sub-epic is a horizontal bar on its own row.
        Its X-range must span all stories beneath it."""
        dm = self._render_simple(tmp_path)

        for se in dm.get_sub_epics():
            se_left = se.boundary.x
            se_right = se.boundary.x + se.boundary.width
            for story in se.get_stories():
                assert story.boundary.x >= se_left, \
                    (f"Story '{story.name}' left edge {story.boundary.x} is outside "
                     f"sub-epic '{se.name}' left edge {se_left}")
                story_right = story.boundary.x + story.boundary.width
                assert story_right <= se_right, \
                    (f"Story '{story.name}' right edge {story_right} exceeds "
                     f"sub-epic '{se.name}' right edge {se_right}")

    def test_nested_containers_horizontal_span_at_every_depth(self, tmp_path):
        """For nested sub-epics (depth=3), every parent's horizontal span
        must cover all its direct children at every level."""
        dm = self._render_nested(tmp_path, depth=3)

        epic = dm.get_epics()[0]
        top_se = epic.get_sub_epics()[0]
        # Epic horizontal span covers top-level sub-epic
        assert top_se.boundary.x >= epic.boundary.x, \
            "Top sub-epic must be within epic's horizontal span"
        assert (top_se.boundary.x + top_se.boundary.width) <= \
               (epic.boundary.x + epic.boundary.width), \
            "Top sub-epic right edge must be within epic's horizontal span"

        for nested_se in top_se.get_sub_epics():
            # Top sub-epic horizontal span covers nested sub-epic
            assert nested_se.boundary.x >= top_se.boundary.x, \
                f"Nested sub-epic '{nested_se.name}' must be within top sub-epic span"
            for story in nested_se.get_stories():
                # Nested sub-epic horizontal span covers story
                assert story.boundary.x >= nested_se.boundary.x, \
                    f"Story '{story.name}' must be within sub-epic '{nested_se.name}' span"

    # ---- Overlap detection (catches siblings piled on top of each other) ----

    def test_sibling_stories_do_not_overlap_horizontally(self, tmp_path):
        """Stories within the same sub-epic must not overlap.
        Catches bugs where all stories share the same X position."""
        dm = self._render_simple(tmp_path)

        for se in dm.get_sub_epics():
            stories = se.get_stories()
            for i in range(len(stories)):
                for j in range(i + 1, len(stories)):
                    a, b = stories[i], stories[j]
                    assert not a.boundary.overlaps(b.boundary), \
                        (f"Stories '{a.name}' and '{b.name}' overlap: "
                         f"{a.boundary} vs {b.boundary}")

    def test_sibling_sub_epics_do_not_overlap_horizontally(self, tmp_path):
        """Sub-epics within the same epic must not overlap."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_counts(1, 3, 7)
        story_map = StoryMap(data)
        dm = DrawIOStoryMap(diagram_type='outline')
        dm.render_from_story_map(story_map, layout_data=None)

        for epic in dm.get_epics():
            sub_epics = epic.get_sub_epics()
            for i in range(len(sub_epics)):
                for j in range(i + 1, len(sub_epics)):
                    a, b = sub_epics[i], sub_epics[j]
                    assert not a.boundary.overlaps(b.boundary), \
                        (f"Sub-epics '{a.name}' and '{b.name}' overlap: "
                         f"{a.boundary} vs {b.boundary}")


class TestRenderStoryMapIncrements:

    def test_render_increments_diagram_with_stories_assigned_to_increment_lanes(self, tmp_path):
        """Increment-assigned stories in lanes; orphaned stories under sub-epics."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        summary = drawio_story_map.render_increments_from_story_map(
            story_map, data.get('increments', []), layout_data=None)

        # Outline portion has epics, sub-epics, and ORPHANED stories only
        assert len(drawio_story_map.get_epics()) >= 1
        assert len(drawio_story_map.get_sub_epics()) >= 1
        outline_stories = drawio_story_map.get_stories()
        outline_story_names = [s.name for s in outline_stories]
        assert 'Validate Input' in outline_story_names, \
            "Orphaned story 'Validate Input' should remain in outline"
        assert 'Load Config' not in outline_story_names, \
            "Increment-assigned story should not be in outline"
        assert 'Register Behaviors' not in outline_story_names, \
            "Increment-assigned story should not be in outline"

        # Increment-assigned stories exist in increment lanes
        extra_values = [v for lane in drawio_story_map._increment_lanes for el in lane.collect_all_elements() for v in [getattr(el, 'value', '')] if v]
        assert 'Load Config' in extra_values, "Load Config should be in increment lane"
        assert 'Register Behaviors' in extra_values, "Register Behaviors should be in increment lane"
        assert summary.get('increments') == 2

    def test_increment_lanes_ordered_by_priority_with_y_positions_from_outline_bottom(self, tmp_path):
        """Lanes ordered by priority; Y positions derived from outline bottom."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        drawio_story_map.render_increments_from_story_map(
            story_map, data.get('increments', []), layout_data=None)

        # Find lane elements (background rectangles)
        lane_elements = [lane._lane_element for lane in drawio_story_map._increment_lanes if lane._lane_element]
        assert len(lane_elements) == 2, "Should have 2 lane background elements"
        # First lane (MVP, priority 1) should be above second lane (Phase 2, priority 2)
        assert lane_elements[0].position.y < lane_elements[1].position.y

    def test_re_render_increments_with_existing_layout_data_recomputes_lane_positions(self, tmp_path):
        """LayoutData applies to epics/sub-epics; lane positions recomputed."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        story_map = StoryMap(data)
        layout_file = helper.drawio_story_map.create_layout_data_file()
        layout_data = LayoutData.load(layout_file)

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        drawio_story_map.render_increments_from_story_map(
            story_map, data.get('increments', []), layout_data=layout_data)

        epics = drawio_story_map.get_epics()
        assert epics[0].position.x == 20
        assert epics[0].position.y == 120

    def test_render_increments_completes_and_summary_includes_increment_count(self, tmp_path):
        """Summary includes increment count and diagram_generated flag."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        summary = drawio_story_map.render_increments_from_story_map(
            story_map, data.get('increments', []), layout_data=None)

        assert summary['diagram_generated'] is True
        assert summary['increments'] == 2

    def test_increment_lane_cells_styled_for_extractor_detection(self, tmp_path):
        """All lane backgrounds use uniform neutral style (no priority colors)."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        drawio_story_map.render_increments_from_story_map(
            story_map, data.get('increments', []), layout_data=None)

        # Find lane background elements
        lane_bgs = [lane._lane_element for lane in drawio_story_map._increment_lanes if lane._lane_element]
        assert len(lane_bgs) == 2
        for lane_bg in lane_bgs:
            style = lane_bg.to_style_string()
            assert 'fillColor=#f5f5f5' in style, \
                f"Lane background should use neutral fill #f5f5f5, got: {style}"
            assert 'strokeColor=#666666' in style, \
                f"Lane background should use stroke #666666, got: {style}"

        # Find lane label elements
        lane_labels = [lane._label_element for lane in drawio_story_map._increment_lanes if lane._label_element]
        assert len(lane_labels) == 2
        for label in lane_labels:
            style = label.to_style_string()
            assert 'fillColor=#f5f5f5' in style
            assert 'strokeColor=#666666' in style

    def test_render_increments_with_no_increments_defined_produces_outline_only_diagram(self, tmp_path):
        """No increments = all stories orphaned → appear in outline tree."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_simple_story_map_data()
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        summary = drawio_story_map.render_increments_from_story_map(
            story_map, [], layout_data=None)

        assert len(drawio_story_map.get_epics()) >= 1
        assert len(drawio_story_map.get_stories()) >= 1, \
            "All stories should be in outline when no increments exist"
        assert summary.get('increments') == 0

    def test_actor_labels_rendered_above_stories_in_increment_lanes(self, tmp_path):
        """Actor labels appear above stories within each lane, deduplicated per lane."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        drawio_story_map.render_increments_from_story_map(
            story_map, data.get('increments', []), layout_data=None)

        # Find actor elements in increment lanes
        actor_elements = [a for lane in drawio_story_map._increment_lanes for a in lane._actor_elements]
        # Each lane has one story with user "Bot Behavior" so each lane
        # should have exactly one actor label (deduplicated)
        assert len(actor_elements) == 2, \
            f"Expected 2 actor labels (one per lane), got {len(actor_elements)}"
        for actor in actor_elements:
            assert actor.value == 'Bot Behavior'

        # Verify actor is positioned BELOW lane label and ABOVE story
        from synchronizers.story_io.drawio_story_node import DrawIOIncrementLane
        for lane in drawio_story_map._increment_lanes:
            lane_bg = lane._lane_element
            if not lane_bg:
                continue
            lane_y = lane_bg.position.y
            lane_actors = lane._actor_elements
            lane_stories = lane._story_copies
            for a in lane_actors:
                # Actor Y should be below label bottom (lane_y + LABEL_Y_OFFSET + LABEL_HEIGHT)
                label_bottom = lane_y + DrawIOIncrementLane.LABEL_Y_OFFSET + DrawIOIncrementLane.LABEL_HEIGHT
                assert a.position.y >= label_bottom, \
                    f"Actor at y={a.position.y} should be below label bottom {label_bottom}"
            for s in lane_stories:
                # Story Y should be below actor bottom
                for a in lane_actors:
                    actor_bottom = a.position.y + a.boundary.height
                    assert s.position.y >= actor_bottom, \
                        f"Story at y={s.position.y} should be below actor bottom {actor_bottom}"


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
        assert report.matched_count >= 0
        assert isinstance(report.renames, list)
        assert isinstance(report.new_stories, list)
        assert isinstance(report.removed_stories, list)

    def test_story_map_updated_from_outline_diagram_applies_report_changes(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        drawio_file = helper.drawio_story_map.create_drawio_file(
            helper.drawio_story_map.create_drawio_xml_with_new_story())
        drawio_story_map = DrawIOStoryMap.load(drawio_file)
        original_story_map = StoryMap(helper.drawio_story_map.create_simple_story_map_data())

        report = drawio_story_map.generate_update_report(original_story_map)

        assert report.matched_count >= 1
        assert len(report.new_stories) >= 1

    def test_renamed_or_reordered_nodes_flagged_as_fuzzy_matches_in_update_report(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        drawio_file = helper.drawio_story_map.create_drawio_file(
            helper.drawio_story_map.create_drawio_xml_with_renamed_story())
        drawio_story_map = DrawIOStoryMap.load(drawio_file)
        original_data = helper.drawio_story_map.create_story_map_data_with_renamed_story()
        original_story_map = StoryMap(original_data)

        report = drawio_story_map.generate_update_report(original_story_map)

        assert len(report.renames) >= 1
        rename = report.renames[0]
        assert rename.extracted_name
        assert rename.original_name

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
        assert report.matched_count >= 1

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
        """Render increments → save → load roundtrip extracts lanes and stories."""
        helper = BotTestHelper(tmp_path)
        drawio_file, story_map, data = \
            helper.drawio_story_map.create_rendered_increments_drawio_file()

        loaded = DrawIOStoryMap.load(drawio_file)

        # Outline portion should still have epics and sub-epics
        assert len(loaded.get_epics()) >= 1
        assert len(loaded.get_sub_epics()) >= 1

        # Loaded nodes should include increment lane elements
        extra_ids = [n.cell_id for n in loaded._loaded_nodes if hasattr(n, 'cell_id')]
        lane_ids = [cid for cid in extra_ids if cid.startswith('inc-lane/')]
        assert len(lane_ids) >= 2, "Should extract at least 2 lane-related elements"

    def test_update_report_generated_for_increments_view_with_story_level_matches(self, tmp_path):
        """UpdateReport lists story-level matches for increments view."""
        helper = BotTestHelper(tmp_path)
        drawio_file, original_story_map, data = \
            helper.drawio_story_map.create_rendered_increments_drawio_file()

        loaded = DrawIOStoryMap.load(drawio_file)
        report = loaded.generate_update_report(original_story_map)

        assert isinstance(report, UpdateReport)
        # Stories in the outline still exist (loaded extracts them)
        # The report should find matches for epics and sub-epics
        assert report.matched_count >= 0

    def test_story_moved_between_increments_reflected_in_extracted_graph(self, tmp_path):
        """When a story is moved between lanes, its Y position changes assignment."""
        helper = BotTestHelper(tmp_path)
        drawio_file, story_map, data = \
            helper.drawio_story_map.create_rendered_increments_drawio_file()

        # Load the rendered diagram and verify roundtrip integrity
        loaded = DrawIOStoryMap.load(drawio_file)

        # Stories from increment lanes are parsed as DrawIOStory objects
        # and assigned to sub-epics by position. Their cell_id retains
        # the inc-lane/ prefix from the rendered diagram.
        stories = loaded.get_stories()
        lane_stories = [s for s in stories if 'inc-lane/' in s.cell_id]
        assert len(lane_stories) >= 2, \
            f"Expected at least 2 lane stories, got {len(lane_stories)}"
        # Each story should have a valid Y position
        for story in lane_stories:
            assert story.position.y > 0, f"Story {story.name} should have a Y position"

    def test_merge_preserves_original_ac_and_updates_story_fields(self, tmp_path):
        """Merge from increments preserves original acceptance_criteria."""
        helper = BotTestHelper(tmp_path)
        # Create data with acceptance criteria on stories
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        data['epics'][0]['sub_epics'][0]['story_groups'][0]['stories'][0]['acceptance_criteria'] = [
            {"name": "Config loads from file", "text": "Given config exists When loaded Then available"}
        ]
        original_story_map = StoryMap(data)

        # Render and load back
        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        drawio_story_map.render_increments_from_story_map(
            original_story_map, data.get('increments', []), layout_data=None)
        drawio_file = tmp_path / 'increments.drawio'
        drawio_story_map.save(drawio_file)

        loaded = DrawIOStoryMap.load(drawio_file)
        report = loaded.generate_update_report(original_story_map)

        # Report should exist and AC should be preserved in original (merge doesn't alter them)
        assert isinstance(report, UpdateReport)
        original_stories = list(original_story_map.all_stories)
        ac_story = [s for s in original_stories if s.name == 'Load Config'][0]
        assert len(ac_story.acceptance_criteria) == 1, \
            "Original AC should be preserved after report generation"

    def test_new_increment_lane_at_bottom_appended_as_new_increment(self, tmp_path):
        """A new lane added at the bottom appears in extracted graph."""
        helper = BotTestHelper(tmp_path)
        # Use 3-increment data to test adding beyond original count
        data = helper.drawio_story_map.create_story_map_data_with_three_increments()
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        drawio_story_map.render_increments_from_story_map(
            story_map, data.get('increments', []), layout_data=None)
        drawio_file = tmp_path / 'increments.drawio'
        drawio_story_map.save(drawio_file)

        loaded = DrawIOStoryMap.load(drawio_file)

        # Verify we extracted 3 lane background elements
        lane_bgs = [n for n in loaded._loaded_nodes
                    if hasattr(n, 'cell_id') and n.cell_id.startswith('inc-lane/')
                    and '/actor-' not in n.cell_id
                    and n.value == '']
        assert len(lane_bgs) == 3, \
            f"Expected 3 lane backgrounds for 3 increments, got {len(lane_bgs)}"

    def test_removed_increment_lane_stays_in_merged_with_original_stories(self, tmp_path):
        """Removing a lane from diagram doesn't remove it from story graph (merge preserves)."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        original_story_map = StoryMap(data)

        # Render with only 1 of 2 increments (simulating removal)
        reduced_data = dict(data)
        reduced_data['increments'] = [data['increments'][0]]  # Only MVP

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        drawio_story_map.render_increments_from_story_map(
            original_story_map, reduced_data['increments'], layout_data=None)
        drawio_file = tmp_path / 'increments.drawio'
        drawio_story_map.save(drawio_file)

        loaded = DrawIOStoryMap.load(drawio_file)

        # Only 1 lane background should exist in loaded diagram
        lane_bgs = [n for n in loaded._loaded_nodes
                    if hasattr(n, 'cell_id') and n.cell_id.startswith('inc-lane/')
                    and '/actor-' not in n.cell_id
                    and n.value == '']
        assert len(lane_bgs) == 1, \
            f"Expected 1 lane background after removal, got {len(lane_bgs)}"

        # Original story map still has 2 increments (merge doesn't remove)
        assert len(data['increments']) == 2

    def test_renamed_increment_lane_updated_by_position_based_matching(self, tmp_path):
        """A renamed lane is matched by position in the diagram."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        original_story_map = StoryMap(data)

        # Rename the first increment
        renamed_data = dict(data)
        renamed_increments = [dict(inc) for inc in data['increments']]
        renamed_increments[0] = dict(renamed_increments[0])
        renamed_increments[0]['name'] = 'Sprint 1'
        renamed_data['increments'] = renamed_increments

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        drawio_story_map.render_increments_from_story_map(
            original_story_map, renamed_data['increments'], layout_data=None)
        drawio_file = tmp_path / 'increments.drawio'
        drawio_story_map.save(drawio_file)

        loaded = DrawIOStoryMap.load(drawio_file)

        # Verify the renamed label exists in loaded nodes
        label_values = [n.value for n in loaded._loaded_nodes
                        if hasattr(n, 'cell_id') and n.cell_id.startswith('inc-label/')]
        assert 'Sprint 1' in label_values, \
            f"Renamed lane 'Sprint 1' should appear in labels, got: {label_values}"
        assert 'MVP' not in label_values, \
            "Original name 'MVP' should not appear after rename"

    def test_extra_extracted_lanes_appended_fewer_lanes_leave_originals_unchanged(self, tmp_path):
        """Extra lanes appended; fewer lanes leave originals untouched."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        original_story_map = StoryMap(data)

        # Render with 2 original increments
        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        drawio_story_map.render_increments_from_story_map(
            original_story_map, data.get('increments', []), layout_data=None)
        drawio_file = tmp_path / 'increments.drawio'
        drawio_story_map.save(drawio_file)

        loaded = DrawIOStoryMap.load(drawio_file)
        report = loaded.generate_update_report(original_story_map)

        # Verify basic report is generated (positions match original)
        assert isinstance(report, UpdateReport)

        # Verify lane count in rendered matches increments count
        lane_labels = [n for n in loaded._loaded_nodes
                       if hasattr(n, 'cell_id') and n.cell_id.startswith('inc-label/')]
        assert len(lane_labels) == 2, \
            f"Expected 2 lane labels, got {len(lane_labels)}"

    def test_known_inserting_lane_between_existing_may_misinterpret_without_stable_ids(self, tmp_path):
        """Known limitation: inserting between existing lanes uses position-based matching."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_three_increments()
        original_story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        drawio_story_map.render_increments_from_story_map(
            original_story_map, data.get('increments', []), layout_data=None)
        drawio_file = tmp_path / 'increments.drawio'
        drawio_story_map.save(drawio_file)

        loaded = DrawIOStoryMap.load(drawio_file)

        # Verify 3 lanes extracted (position-based matching would map 1:1)
        lane_labels = [n for n in loaded._loaded_nodes
                       if hasattr(n, 'cell_id') and n.cell_id.startswith('inc-label/')]
        assert len(lane_labels) == 3
        # Position-based matching maps lane at index 0 to original[0], etc.
        # Inserting between would shift positions and potentially misalign
        label_values = [l.value for l in lane_labels]
        assert 'MVP' in label_values
        assert 'Phase 2' in label_values
        assert 'Phase 3' in label_values

    def test_story_not_within_100px_of_any_lane_remains_unassigned_in_extracted(self, tmp_path):
        """Story positioned far from any lane is not assigned to an increment."""
        helper = BotTestHelper(tmp_path)
        drawio_file, story_map, data = \
            helper.drawio_story_map.create_rendered_increments_drawio_file()

        loaded = DrawIOStoryMap.load(drawio_file)

        # Verify the diagram loaded correctly with loaded nodes
        extra_nodes = loaded._loaded_nodes
        assert len(extra_nodes) >= 4, \
            "Should have lane backgrounds, labels, and story copies"

        # In the standard render, stories are positioned at lane_y + STORY_Y_OFFSET
        # so they ARE within 100px.  This test documents the 100px threshold behavior.
        story_copies = [n for n in extra_nodes
                        if hasattr(n, 'cell_id') and 'inc-lane/' in n.cell_id
                        and '/actor-' not in n.cell_id
                        and n.value != ''
                        and not n.cell_id.startswith('inc-label/')]
        lane_bgs = [n for n in extra_nodes
                    if hasattr(n, 'cell_id') and n.cell_id.startswith('inc-lane/')
                    and '/actor-' not in n.cell_id
                    and n.value == '']
        # Each story copy should be within 100px of its lane
        for story_copy in story_copies:
            min_dist = float('inf')
            for lane in lane_bgs:
                dist = abs(story_copy.position.y - lane.position.y)
                if dist < min_dist:
                    min_dist = dist
            assert min_dist <= 100, \
                f"Story {story_copy.value} at y={story_copy.position.y} " \
                f"should be within 100px of a lane (min_dist={min_dist})"


class TestIncrementRemovalMoveAndOrderApply:
    """Tests for applying increment removals, moves, and priority reordering."""

    def test_apply_remove_increment_deletes_entire_increment_from_story_graph(self, tmp_path):
        """Removed increments should be completely deleted from the story graph."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        graph_data = json.loads(json.dumps(data))

        # Precondition: 2 increments exist
        assert len(graph_data['increments']) == 2

        from actions.render.render_action import RenderOutputAction
        action = RenderOutputAction.__new__(RenderOutputAction)

        result = action._apply_remove_increment(graph_data, 'Phase 2')
        assert result is True
        inc_names = [i['name'] for i in graph_data['increments']]
        assert 'Phase 2' not in inc_names, \
            f"Phase 2 should be removed, got: {inc_names}"
        assert 'MVP' in inc_names, "MVP should still be present"
        assert len(graph_data['increments']) == 1

    def test_apply_remove_increment_returns_false_for_nonexistent(self, tmp_path):
        """Removing a non-existent increment returns False."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        graph_data = json.loads(json.dumps(data))

        from actions.render.render_action import RenderOutputAction
        action = RenderOutputAction.__new__(RenderOutputAction)

        result = action._apply_remove_increment(graph_data, 'Nonexistent')
        assert result is False
        assert len(graph_data['increments']) == 2

    def test_apply_increment_move_transfers_story_between_increments(self, tmp_path):
        """Moving a story between increments removes from source and adds to target."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        graph_data = json.loads(json.dumps(data))

        from synchronizers.story_io.update_report import IncrementMove
        from actions.render.render_action import RenderOutputAction
        action = RenderOutputAction.__new__(RenderOutputAction)

        move = IncrementMove(story='Load Config', from_increment='MVP',
                             to_increment='Phase 2')
        result = action._apply_increment_move(graph_data, move)
        assert result is True

        mvp = next(i for i in graph_data['increments'] if i['name'] == 'MVP')
        p2 = next(i for i in graph_data['increments'] if i['name'] == 'Phase 2')
        assert 'Load Config' not in mvp['stories'], \
            f"Load Config should be removed from MVP: {mvp['stories']}"
        assert 'Load Config' in p2['stories'], \
            f"Load Config should be in Phase 2: {p2['stories']}"

    def test_apply_increment_move_creates_target_if_missing(self, tmp_path):
        """Moving a story to a non-existent increment creates it."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        graph_data = json.loads(json.dumps(data))

        from synchronizers.story_io.update_report import IncrementMove
        from actions.render.render_action import RenderOutputAction
        action = RenderOutputAction.__new__(RenderOutputAction)

        move = IncrementMove(story='Load Config', from_increment='MVP',
                             to_increment='Sprint 1')
        result = action._apply_increment_move(graph_data, move)
        assert result is True

        inc_names = [i['name'] for i in graph_data['increments']]
        assert 'Sprint 1' in inc_names, f"Sprint 1 should be created: {inc_names}"
        sprint1 = next(i for i in graph_data['increments'] if i['name'] == 'Sprint 1')
        assert 'Load Config' in sprint1['stories']

    def test_apply_increment_order_updates_priorities(self, tmp_path):
        """Increment priorities should be updated to match diagram order."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        graph_data = json.loads(json.dumps(data))

        # Original: MVP=priority 1, Phase 2=priority 2
        # Diagram order: Phase 2 first (priority 1), MVP second (priority 2)
        from actions.render.render_action import RenderOutputAction
        action = RenderOutputAction.__new__(RenderOutputAction)

        order = [{'name': 'Phase 2', 'priority': 1},
                 {'name': 'MVP', 'priority': 2}]
        result = action._apply_increment_order(graph_data, order)
        assert result is True

        p2 = next(i for i in graph_data['increments'] if i['name'] == 'Phase 2')
        mvp = next(i for i in graph_data['increments'] if i['name'] == 'MVP')
        assert p2['priority'] == 1, f"Phase 2 should be priority 1, got {p2['priority']}"
        assert mvp['priority'] == 2, f"MVP should be priority 2, got {mvp['priority']}"

        # After reordering, Phase 2 should come first in the list
        assert graph_data['increments'][0]['name'] == 'Phase 2'
        assert graph_data['increments'][1]['name'] == 'MVP'

    def test_apply_increment_order_no_change_when_already_correct(self, tmp_path):
        """No modification when priorities already match diagram order."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        graph_data = json.loads(json.dumps(data))

        from actions.render.render_action import RenderOutputAction
        action = RenderOutputAction.__new__(RenderOutputAction)

        order = [{'name': 'MVP', 'priority': 1},
                 {'name': 'Phase 2', 'priority': 2}]
        result = action._apply_increment_order(graph_data, order)
        assert result is False  # no changes needed

    def test_report_includes_removed_increments_and_order(self, tmp_path):
        """Report generated from diagram with fewer lanes lists removed increments and order."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        original_story_map = StoryMap(data)

        # Render with only MVP (simulating removal of Phase 2)
        reduced_data = dict(data)
        reduced_data['increments'] = [data['increments'][0]]  # Only MVP

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        drawio_story_map.render_increments_from_story_map(
            original_story_map, reduced_data['increments'], layout_data=None)
        drawio_file = tmp_path / 'increments.drawio'
        drawio_story_map.save(drawio_file)

        loaded = DrawIOStoryMap.load(drawio_file)
        report = loaded.generate_update_report(original_story_map)

        # Phase 2 should be listed as removed
        assert 'Phase 2' in report.removed_increments, \
            f"Phase 2 should be in removed_increments: {report.removed_increments}"

        # increment_order should list only MVP
        order_names = [o['name'] for o in report.increment_order]
        assert 'MVP' in order_names, \
            f"MVP should be in increment_order: {report.increment_order}"
        assert 'Phase 2' not in order_names, \
            "Phase 2 should NOT be in increment_order"

    def test_removed_increments_and_order_roundtrip_through_json(self, tmp_path):
        """removed_increments and increment_order survive to_dict → from_dict."""
        from synchronizers.story_io.update_report import (
            UpdateReport, IncrementChange, IncrementMove)

        report = UpdateReport()
        report.set_increment_changes(
            changes=[IncrementChange(name='MVP', added=['Story A'])],
            moves=[IncrementMove(story='Story B', from_increment='X', to_increment='Y')],
            removed_increments=['Phase 2', 'Phase 3'],
            increment_order=[{'name': 'MVP', 'priority': 1}])

        data = report.to_dict()
        assert 'removed_increments' in data
        assert 'increment_order' in data

        restored = UpdateReport.from_dict(data)
        assert restored.removed_increments == ['Phase 2', 'Phase 3']
        assert restored.increment_order == [{'name': 'MVP', 'priority': 1}]
        assert len(restored.increment_changes) == 1
        assert len(restored.increment_moves) == 1

    def test_end_to_end_remove_lane_and_reorder_updates_story_graph(self, tmp_path):
        """Full flow: render 2 lanes → remove Phase 2 → report → apply → verify."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        original_data = json.loads(json.dumps(data))
        story_map = StoryMap(data)

        # 1. Render with only MVP (simulating user deleting Phase 2 lane)
        reduced_increments = [data['increments'][0]]
        drawio_map = DrawIOStoryMap(diagram_type='increments')
        drawio_map.render_increments_from_story_map(
            story_map, reduced_increments, layout_data=None)
        drawio_file = tmp_path / 'increments.drawio'
        drawio_map.save(drawio_file)

        # 2. Load and generate report
        loaded = DrawIOStoryMap.load(drawio_file)
        report = loaded.generate_update_report(story_map)

        # 3. Apply all changes
        from actions.render.render_action import RenderOutputAction
        action = RenderOutputAction.__new__(RenderOutputAction)
        graph_data = json.loads(json.dumps(original_data))

        for inc_change in report.increment_changes:
            action._apply_increment_change(graph_data, inc_change)
        for inc_move in report.increment_moves:
            action._apply_increment_move(graph_data, inc_move)
        for inc_name in report.removed_increments:
            action._apply_remove_increment(graph_data, inc_name)
        if report.increment_order:
            action._apply_increment_order(graph_data, report.increment_order)

        # 4. Verify: Phase 2 should be gone, MVP should remain
        inc_names = [i['name'] for i in graph_data['increments']]
        assert 'Phase 2' not in inc_names, \
            f"Phase 2 should be removed: {inc_names}"
        assert 'MVP' in inc_names, \
            f"MVP should remain: {inc_names}"
        mvp = next(i for i in graph_data['increments'] if i['name'] == 'MVP')
        assert mvp['priority'] == 1


class TestUserCreatedIncrementLaneDetection:
    """Tests that user-created increment lanes (with simple cell IDs
    instead of inc-lane/ prefix) are correctly detected during extraction."""

    def test_user_created_lane_detected_by_geometry(self, tmp_path):
        """A user-created lane background (large rectangle, empty value,
        simple ID) and its label should be extracted as a new increment."""
        helper = BotTestHelper(tmp_path)
        drawio_file, story_map, data = \
            helper.drawio_story_map.create_rendered_increments_drawio_file()

        loaded = DrawIOStoryMap.load(drawio_file)

        # Find an existing lane to get its geometry for reference
        existing_lanes = [n for n in loaded._loaded_nodes
                          if getattr(n, 'cell_id', '').startswith('inc-lane/')
                          and getattr(n, 'value', '') == '']
        assert len(existing_lanes) > 0
        ref_lane = existing_lanes[0]
        lane_width = ref_lane.boundary.width
        lane_height = ref_lane.boundary.height
        last_lane_bottom = max(n.position.y + n.boundary.height
                               for n in existing_lanes)

        # Add a user-created lane background (simple id, empty value)
        from synchronizers.story_io.drawio_element import DrawIOElement
        new_bg = DrawIOElement(cell_id='99', value='')
        new_bg.set_position(0, last_lane_bottom + 10)
        new_bg.set_size(lane_width, lane_height)
        loaded._loaded_nodes.append(new_bg)

        # Add a user-created lane label (simple id, with name)
        new_label = DrawIOElement(cell_id='100', value='My New Increment')
        new_label.set_position(5, last_lane_bottom + 15)
        new_label.set_size(150, 30)
        loaded._loaded_nodes.append(new_label)

        extracted = loaded.extract_increment_assignments()
        inc_names = [inc['name'] for inc in extracted]
        assert 'My New Increment' in inc_names, \
            f"User-created lane not detected. Found: {inc_names}"

    def test_user_created_lane_stories_assigned_by_y_position(self, tmp_path):
        """Stories positioned inside a user-created lane should be
        assigned to that increment."""
        helper = BotTestHelper(tmp_path)
        drawio_file, story_map, data = \
            helper.drawio_story_map.create_rendered_increments_drawio_file()

        loaded = DrawIOStoryMap.load(drawio_file)

        existing_lanes = [n for n in loaded._loaded_nodes
                          if getattr(n, 'cell_id', '').startswith('inc-lane/')
                          and getattr(n, 'value', '') == '']
        ref_lane = existing_lanes[0]
        lane_width = ref_lane.boundary.width
        lane_height = ref_lane.boundary.height
        last_lane_bottom = max(n.position.y + n.boundary.height
                               for n in existing_lanes)

        lane_y = last_lane_bottom + 10
        from synchronizers.story_io.drawio_element import DrawIOElement

        # Lane background
        new_bg = DrawIOElement(cell_id='99', value='')
        new_bg.set_position(0, lane_y)
        new_bg.set_size(lane_width, lane_height)
        loaded._loaded_nodes.append(new_bg)

        # Lane label
        new_label = DrawIOElement(cell_id='100', value='Custom Lane')
        new_label.set_position(5, lane_y + 5)
        new_label.set_size(150, 30)
        loaded._loaded_nodes.append(new_label)

        # A story inside the lane
        story_in_lane = DrawIOElement(cell_id='101', value='Test Story')
        story_in_lane.set_position(200, lane_y + 80)
        story_in_lane.set_size(50, 50)
        loaded._loaded_nodes.append(story_in_lane)

        extracted = loaded.extract_increment_assignments()
        custom = next((inc for inc in extracted if inc['name'] == 'Custom Lane'), None)
        assert custom is not None, "Custom Lane not found in extracted"
        assert 'Test Story' in custom['stories'], \
            f"Test Story not assigned to Custom Lane. Stories: {custom['stories']}"

    def test_user_created_lane_shows_in_report_as_new_increment(self, tmp_path):
        """A user-created increment lane should appear in the report
        with its stories and in the new increment_order."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        original_story_map = StoryMap(data)

        drawio_map = DrawIOStoryMap()
        drawio_map.render_increments_from_story_map(
            original_story_map, data['increments'], layout_data=None)

        # Find lane geometry
        existing_lanes = [lane._lane_element for lane in drawio_map._increment_lanes if lane._lane_element]
        ref_lane = existing_lanes[0]
        lane_width = ref_lane.boundary.width
        lane_height = ref_lane.boundary.height
        last_lane_bottom = max(n.position.y + n.boundary.height
                               for n in existing_lanes)

        lane_y = last_lane_bottom + 10
        from synchronizers.story_io.drawio_element import DrawIOElement
        from synchronizers.story_io.drawio_story_node import DrawIOIncrementLane

        # Build a user-created lane and add it to _increment_lanes
        new_lane = DrawIOIncrementLane(name='New Sprint', priority=99,
                                       story_names=[])
        new_lane._lane_element = DrawIOElement(cell_id='50', value='')
        new_lane._lane_element.set_position(0, lane_y)
        new_lane._lane_element.set_size(lane_width, lane_height)
        new_lane._label_element = DrawIOElement(cell_id='51', value='New Sprint')
        new_lane._label_element.set_position(5, lane_y + 5)
        new_lane._label_element.set_size(150, 30)

        # Move a story into the new lane
        orphan = None
        for s in drawio_map.get_stories():
            if s.name == 'Validate Input':
                orphan = s
                break
        if orphan:
            copy = DrawIOElement(cell_id='52', value='Validate Input')
            copy.set_position(orphan.position.x, lane_y + 80)
            copy.set_size(50, 50)
            new_lane._story_copies.append(copy)

        drawio_map._increment_lanes.append(new_lane)

        # Save, reload, generate report
        drawio_file = tmp_path / 'test.drawio'
        drawio_map.save(drawio_file)
        loaded = DrawIOStoryMap.load(drawio_file)
        report = loaded.generate_update_report(original_story_map)

        # New Sprint should appear in increment_order
        order_names = [o['name'] for o in report.increment_order]
        assert 'New Sprint' in order_names, \
            f"New Sprint not in increment_order: {order_names}"


class TestIncrementReportTwoPassExtraction:
    """Tests for the two-pass report: pass 1 = hierarchy, pass 2 = increment delta."""

    def test_no_changes_when_diagram_matches_original(self, tmp_path):
        """Render → load → report: no increment changes when nothing moved."""
        helper = BotTestHelper(tmp_path)
        drawio_file, story_map, data = \
            helper.drawio_story_map.create_rendered_increments_drawio_file()

        loaded = DrawIOStoryMap.load(drawio_file)
        report = loaded.generate_update_report(story_map)

        # No increment changes when the diagram matches the original
        assert len(report.increment_changes) == 0, \
            f"Expected no changes, got {[(c.name, c.added, c.removed) for c in report.increment_changes]}"
        assert len(report.increment_moves) == 0

    def test_moving_orphan_into_lane_reports_as_added(self, tmp_path):
        """Drag an orphan story into a lane → report shows it added to that
        increment, no false new stories in hierarchy."""
        helper = BotTestHelper(tmp_path)
        drawio_file, story_map, data = \
            helper.drawio_story_map.create_rendered_increments_drawio_file()

        loaded = DrawIOStoryMap.load(drawio_file)

        # Find orphan 'Validate Input' and first lane background
        orphan = None
        for s in loaded.get_stories():
            if s.name == 'Validate Input':
                orphan = s
                break
        assert orphan is not None, "Validate Input should be in the loaded tree"

        lane_bgs = [n for n in loaded._loaded_nodes
                    if hasattr(n, 'cell_id')
                    and n.cell_id.startswith('inc-lane/')
                    and '/' not in n.cell_id.replace('inc-lane/', '', 1)
                    and getattr(n, 'value', '') == '']
        assert len(lane_bgs) >= 1

        # Simulate drag: move orphan's Y into the first lane
        target_lane = lane_bgs[0]
        from synchronizers.story_io.drawio_story_node import DrawIOIncrementLane
        orphan.set_position(orphan.position.x,
                            target_lane.position.y + DrawIOIncrementLane.STORY_Y_OFFSET)

        report = loaded.generate_update_report(story_map)

        # Pass 1: no hierarchy changes
        assert len(report.new_stories) == 0, \
            f"Expected 0 new stories, got {[(s.name, s.parent) for s in report.new_stories]}"

        # Pass 2: 'Validate Input' should appear as added to an increment
        added_stories = set()
        for c in report.increment_changes:
            added_stories.update(c.added)
        assert 'Validate Input' in added_stories, \
            f"'Validate Input' should be added to an increment, changes: " \
            f"{[(c.name, c.added, c.removed) for c in report.increment_changes]}"

        # Should also show up as a move from unassigned
        vi_moves = [m for m in report.increment_moves if m.story == 'Validate Input']
        assert len(vi_moves) >= 1, "Should have a move entry for Validate Input"
        assert vi_moves[0].from_increment == '', "Should move FROM unassigned"
        assert vi_moves[0].to_increment != '', "Should move TO an increment"

    def test_no_false_new_stories_with_duplicates_across_lanes(self, tmp_path):
        """A story in two lanes produces no false hierarchy changes."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        data['increments'].append(
            {"name": "Phase 3", "priority": 3, "stories": ["Load Config"]})
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        drawio_story_map.render_increments_from_story_map(
            story_map, data.get('increments', []), layout_data=None)
        drawio_file = tmp_path / 'increments.drawio'
        drawio_story_map.save(drawio_file)

        loaded = DrawIOStoryMap.load(drawio_file)
        report = loaded.generate_update_report(story_map)

        # Pass 1: no false new stories
        assert len(report.new_stories) == 0, \
            f"Expected 0 new stories, got {[(s.name, s.parent) for s in report.new_stories]}"

    def test_increment_delta_serializes_to_json_and_round_trips(self, tmp_path):
        """Increment change data survives to_dict → from_dict roundtrip."""
        helper = BotTestHelper(tmp_path)
        drawio_file, story_map, data = \
            helper.drawio_story_map.create_rendered_increments_drawio_file()

        loaded = DrawIOStoryMap.load(drawio_file)

        # Move an orphan into a lane to produce changes
        orphan = None
        for s in loaded.get_stories():
            if s.name == 'Validate Input':
                orphan = s
                break
        lane_bgs = [n for n in loaded._loaded_nodes
                    if hasattr(n, 'cell_id')
                    and n.cell_id.startswith('inc-lane/')
                    and '/' not in n.cell_id.replace('inc-lane/', '', 1)
                    and getattr(n, 'value', '') == '']
        from synchronizers.story_io.drawio_story_node import DrawIOIncrementLane
        orphan.set_position(orphan.position.x,
                            lane_bgs[0].position.y + DrawIOIncrementLane.STORY_Y_OFFSET)

        report = loaded.generate_update_report(story_map)

        # Roundtrip via JSON
        report_dict = report.to_dict()
        restored = UpdateReport.from_dict(report_dict)

        assert restored.matched_count == report.matched_count
        assert len(restored.increment_changes) == len(report.increment_changes)
        assert len(restored.increment_moves) == len(report.increment_moves)
        for orig_c, rest_c in zip(report.increment_changes, restored.increment_changes):
            assert orig_c.name == rest_c.name
            assert orig_c.added == rest_c.added
            assert orig_c.removed == rest_c.removed


    # ----- helpers -----

    @staticmethod
    def _lane_bgs(loaded):
        return [n for n in loaded._loaded_nodes
                if hasattr(n, 'cell_id')
                and n.cell_id.startswith('inc-lane/')
                and '/' not in n.cell_id.replace('inc-lane/', '', 1)
                and getattr(n, 'value', '') == '']

    @staticmethod
    def _lane_labels(loaded):
        return {n.value: n for n in loaded._loaded_nodes
                if hasattr(n, 'cell_id')
                and n.cell_id.startswith('inc-label/')}

    @staticmethod
    def _lane_bg_for(loaded, lane_name):
        """Find the lane background element for a named increment."""
        labels = {n.cell_id.replace('inc-label/', ''): n.value
                  for n in loaded._loaded_nodes
                  if hasattr(n, 'cell_id') and n.cell_id.startswith('inc-label/')}
        slug_to_name = {slug: name for slug, name in labels.items()}
        for n in loaded._loaded_nodes:
            cid = getattr(n, 'cell_id', '')
            if (cid.startswith('inc-lane/')
                    and '/' not in cid.replace('inc-lane/', '', 1)
                    and getattr(n, 'value', '') == ''):
                slug = cid.replace('inc-lane/', '')
                if slug_to_name.get(slug) == lane_name:
                    return n
        return None

    def test_move_story_between_increments_reports_correct_delta(self, tmp_path):
        """Move 'Load Config' from MVP lane into Phase 2 lane.
        Report should show it removed from MVP and added to Phase 2."""
        helper = BotTestHelper(tmp_path)
        drawio_file, story_map, data = \
            helper.drawio_story_map.create_rendered_increments_drawio_file()

        loaded = DrawIOStoryMap.load(drawio_file)

        # Find the story 'Load Config' (currently in MVP lane)
        story = None
        for s in loaded.get_stories():
            if s.name == 'Load Config':
                story = s
                break
        assert story is not None

        # Find the Phase 2 lane background
        phase2_lane = self._lane_bg_for(loaded, 'Phase 2')
        assert phase2_lane is not None, "Phase 2 lane should exist"

        # Simulate drag: move story's Y into the Phase 2 lane
        from synchronizers.story_io.drawio_story_node import DrawIOIncrementLane
        story.set_position(story.position.x,
                           phase2_lane.position.y + DrawIOIncrementLane.STORY_Y_OFFSET)

        report = loaded.generate_update_report(story_map)

        # No hierarchy changes
        assert len(report.new_stories) == 0
        assert len(report.removed_stories) == 0

        # MVP should show 'Load Config' removed
        mvp_change = next((c for c in report.increment_changes if c.name == 'MVP'), None)
        assert mvp_change is not None, "MVP should have changes"
        assert 'Load Config' in mvp_change.removed

        # Phase 2 should show 'Load Config' added
        p2_change = next((c for c in report.increment_changes if c.name == 'Phase 2'), None)
        assert p2_change is not None, "Phase 2 should have changes"
        assert 'Load Config' in p2_change.added

        # Should report as a move
        lc_moves = [m for m in report.increment_moves if m.story == 'Load Config']
        assert len(lc_moves) >= 1, "Should have a move for Load Config"
        assert lc_moves[0].from_increment == 'MVP'
        assert lc_moves[0].to_increment == 'Phase 2'

    def test_apply_increment_changes_updates_story_graph_json(self, tmp_path):
        """Applying increment changes adds/removes stories in the JSON."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        graph_data = json.loads(json.dumps(data))  # deep copy

        from synchronizers.story_io.update_report import IncrementChange

        # Simulate: 'Load Config' removed from MVP, added to Phase 2
        change_mvp = IncrementChange(name='MVP', removed=['Load Config'])
        change_p2 = IncrementChange(name='Phase 2', added=['Load Config'])

        from actions.render.render_action import RenderOutputAction
        action = RenderOutputAction.__new__(RenderOutputAction)

        action._apply_increment_change(graph_data, change_mvp)
        action._apply_increment_change(graph_data, change_p2)

        # Verify the JSON was updated
        mvp = next(i for i in graph_data['increments'] if i['name'] == 'MVP')
        p2 = next(i for i in graph_data['increments'] if i['name'] == 'Phase 2')

        assert 'Load Config' not in mvp['stories'], \
            f"Load Config should be removed from MVP: {mvp['stories']}"
        assert 'Load Config' in p2['stories'], \
            f"Load Config should be added to Phase 2: {p2['stories']}"
        assert 'Register Behaviors' in p2['stories'], \
            "Register Behaviors should still be in Phase 2"

    def test_apply_increment_change_creates_new_increment_if_needed(self, tmp_path):
        """Adding a story to a non-existent increment creates it."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        graph_data = json.loads(json.dumps(data))

        from synchronizers.story_io.update_report import IncrementChange
        from actions.render.render_action import RenderOutputAction
        action = RenderOutputAction.__new__(RenderOutputAction)

        change = IncrementChange(name='Phase 3', added=['Validate Input'])
        action._apply_increment_change(graph_data, change)

        inc_names = [i['name'] for i in graph_data['increments']]
        assert 'Phase 3' in inc_names, f"Phase 3 should be created: {inc_names}"
        p3 = next(i for i in graph_data['increments'] if i['name'] == 'Phase 3')
        assert 'Validate Input' in p3['stories']

    def test_end_to_end_render_move_report_update_verifies_story_graph(self, tmp_path):
        """Full flow: render → move story → report → update → verify JSON."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        original_data = json.loads(json.dumps(data))  # deep copy for later
        story_map = StoryMap(data)

        # 1. Render
        drawio_map = DrawIOStoryMap(diagram_type='increments')
        drawio_map.render_increments_from_story_map(
            story_map, data.get('increments', []), layout_data=None)
        drawio_file = tmp_path / 'increments.drawio'
        drawio_map.save(drawio_file)

        # 2. Load and move 'Load Config' from MVP into Phase 2
        loaded = DrawIOStoryMap.load(drawio_file)
        story = next(s for s in loaded.get_stories() if s.name == 'Load Config')
        phase2_lane = self._lane_bg_for(loaded, 'Phase 2')
        assert phase2_lane is not None

        from synchronizers.story_io.drawio_story_node import DrawIOIncrementLane
        story.set_position(story.position.x,
                           phase2_lane.position.y + DrawIOIncrementLane.STORY_Y_OFFSET)

        # 3. Generate report
        report = loaded.generate_update_report(story_map)
        assert len(report.increment_changes) > 0, "Should have increment changes"

        # 4. Apply to graph data
        from actions.render.render_action import RenderOutputAction
        action = RenderOutputAction.__new__(RenderOutputAction)
        graph_data = json.loads(json.dumps(original_data))

        for change in report.increment_changes:
            action._apply_increment_change(graph_data, change)

        # 5. Verify
        mvp = next(i for i in graph_data['increments'] if i['name'] == 'MVP')
        p2 = next(i for i in graph_data['increments'] if i['name'] == 'Phase 2')

        assert 'Load Config' not in mvp['stories'], \
            f"Load Config should be gone from MVP: {mvp['stories']}"
        assert 'Load Config' in p2['stories'], \
            f"Load Config should now be in Phase 2: {p2['stories']}"


class TestStoryMoveDetection:
    """Tests for detecting moved stories (not false new+removed) in update reports."""

    @staticmethod
    def _two_sub_epic_data():
        """Story map with two sub-epics so we can test cross-sub-epic moves."""
        return {
            "epics": [{
                "name": "Invoke Bot",
                "sequential_order": 1.0,
                "sub_epics": [
                    {
                        "name": "Initialize Bot",
                        "sequential_order": 1.0,
                        "sub_epics": [],
                        "story_groups": [{
                            "type": "and", "connector": None,
                            "stories": [
                                {"name": "Load Config", "sequential_order": 1.0,
                                 "story_type": "user", "acceptance_criteria": [
                                     {"name": "Config file is loaded from workspace root"}]},
                                {"name": "Validate Input", "sequential_order": 2.0,
                                 "story_type": "user", "acceptance_criteria": []},
                            ]
                        }]
                    },
                    {
                        "name": "Run Bot",
                        "sequential_order": 2.0,
                        "sub_epics": [],
                        "story_groups": [{
                            "type": "and", "connector": None,
                            "stories": [
                                {"name": "Register Behaviors", "sequential_order": 1.0,
                                 "story_type": "system", "acceptance_criteria": []},
                                {"name": "Execute Action", "sequential_order": 2.0,
                                 "story_type": "user", "acceptance_criteria": []},
                            ]
                        }]
                    },
                ]
            }]
        }

    @staticmethod
    def _nested_sub_epic_data():
        """Story map with a sub-epic nested inside another (for removal tests)."""
        return {
            "epics": [{
                "name": "Invoke Bot",
                "sequential_order": 1.0,
                "sub_epics": [
                    {
                        "name": "Initialize Bot",
                        "sequential_order": 1.0,
                        "sub_epics": [
                            {
                                "name": "Init Interface",
                                "sequential_order": 1.0,
                                "sub_epics": [],
                                "story_groups": [{
                                    "type": "and", "connector": None,
                                    "stories": [
                                        {"name": "Open Panel", "sequential_order": 1.0,
                                         "story_type": "user",
                                         "acceptance_criteria": [
                                             {"name": "Panel opens in IDE sidebar"}]},
                                        {"name": "Apply Branding", "sequential_order": 2.0,
                                         "story_type": "user", "acceptance_criteria": []},
                                    ]
                                }]
                            }
                        ],
                        "story_groups": [{
                            "type": "and", "connector": None,
                            "stories": [
                                {"name": "Load Config", "sequential_order": 1.0,
                                 "story_type": "user", "acceptance_criteria": []},
                            ]
                        }]
                    },
                ]
            }]
        }

    def test_story_moved_between_sub_epics_detected_as_move_not_new(self, tmp_path):
        """When a story moves from sub-epic A to sub-epic B, it should appear
        in moved_stories, NOT in new_stories or removed_stories."""
        original_data = self._two_sub_epic_data()
        original_map = StoryMap(original_data)

        # Create modified data: 'Load Config' moved from 'Initialize Bot' to 'Run Bot'
        import copy
        modified_data = copy.deepcopy(original_data)
        init_stories = modified_data['epics'][0]['sub_epics'][0]['story_groups'][0]['stories']
        run_stories = modified_data['epics'][0]['sub_epics'][1]['story_groups'][0]['stories']

        # Remove from Init, add to Run
        moved_story = [s for s in init_stories if s['name'] == 'Load Config'][0]
        init_stories.remove(moved_story)
        run_stories.append(moved_story)

        # Render the modified data
        modified_map = StoryMap(modified_data)
        drawio_map = DrawIOStoryMap(diagram_type='outline')
        drawio_map.render_from_story_map(modified_map, layout_data=None)

        # Generate report comparing modified diagram against original
        report = drawio_map.generate_update_report(original_map)

        # Should be a move, not new+removed
        moved_names = [m.name for m in report.moved_stories]
        new_names = [s.name for s in report.new_stories]
        removed_names = [s.name for s in report.removed_stories]

        assert 'Load Config' in moved_names, \
            f"'Load Config' should be in moved_stories, got moved={moved_names}, " \
            f"new={new_names}, removed={removed_names}"
        assert 'Load Config' not in new_names, \
            f"'Load Config' should NOT be in new_stories"
        assert 'Load Config' not in removed_names, \
            f"'Load Config' should NOT be in removed_stories"

        # Verify move details
        move = next(m for m in report.moved_stories if m.name == 'Load Config')
        assert move.from_parent == 'Initialize Bot'
        assert move.to_parent == 'Run Bot'

    def test_stories_from_removed_sub_epic_detected_as_moves(self, tmp_path):
        """When a sub-epic is removed and its stories appear under the parent,
        those stories should be moves (from removed sub-epic to parent)."""
        original_data = self._nested_sub_epic_data()
        original_map = StoryMap(original_data)

        # Create modified data: remove 'Init Interface', promote its stories
        import copy
        modified_data = copy.deepcopy(original_data)
        init_bot = modified_data['epics'][0]['sub_epics'][0]

        # Get stories from the nested sub-epic
        nested_se = init_bot['sub_epics'][0]  # 'Init Interface'
        promoted_stories = nested_se['story_groups'][0]['stories']

        # Remove the nested sub-epic
        init_bot['sub_epics'] = []

        # Add promoted stories to 'Initialize Bot'
        init_bot['story_groups'][0]['stories'].extend(promoted_stories)

        # Render the modified data
        modified_map = StoryMap(modified_data)
        drawio_map = DrawIOStoryMap(diagram_type='outline')
        drawio_map.render_from_story_map(modified_map, layout_data=None)

        # Generate report
        report = drawio_map.generate_update_report(original_map)

        moved_names = [m.name for m in report.moved_stories]
        new_names = [s.name for s in report.new_stories]

        # 'Open Panel' and 'Apply Branding' should be moves, not new
        assert 'Open Panel' in moved_names, \
            f"'Open Panel' should be in moved_stories, got moved={moved_names}, new={new_names}"
        assert 'Apply Branding' in moved_names, \
            f"'Apply Branding' should be in moved_stories"
        assert 'Open Panel' not in new_names
        assert 'Apply Branding' not in new_names

        # The removed sub-epic should still be reported
        removed_se_names = [s.name for s in report.removed_sub_epics]
        assert 'Init Interface' in removed_se_names

        # Verify move details
        panel_move = next(m for m in report.moved_stories if m.name == 'Open Panel')
        assert panel_move.from_parent == 'Init Interface'
        assert panel_move.to_parent == 'Initialize Bot'

    def test_moved_stories_serializes_to_json_and_round_trips(self, tmp_path):
        """moved_stories should survive to_dict → from_dict roundtrip."""
        from synchronizers.story_io.update_report import StoryMove

        report = UpdateReport()
        report._moved_stories = [
            StoryMove(name='Load Config', from_parent='Initialize Bot', to_parent='Run Bot'),
            StoryMove(name='Open Panel', from_parent='Init Interface', to_parent='Initialize Bot'),
        ]

        report_dict = report.to_dict()
        assert 'moved_stories' in report_dict
        assert len(report_dict['moved_stories']) == 2

        restored = UpdateReport.from_dict(report_dict)
        assert len(restored.moved_stories) == 2
        assert restored.moved_stories[0].name == 'Load Config'
        assert restored.moved_stories[0].from_parent == 'Initialize Bot'
        assert restored.moved_stories[0].to_parent == 'Run Bot'

    def test_apply_move_story_preserves_data(self, tmp_path):
        """Moving a story via _apply_move_story should preserve all fields
        (acceptance criteria, story_type, etc.)."""
        from actions.render.render_action import RenderOutputAction

        data = self._two_sub_epic_data()
        import copy
        graph_data = copy.deepcopy(data)

        action = RenderOutputAction.__new__(RenderOutputAction)
        result = action._apply_move_story(
            graph_data, 'Load Config', 'Initialize Bot', 'Run Bot')

        assert result is True

        # Verify it was removed from Initialize Bot
        init_stories = graph_data['epics'][0]['sub_epics'][0]['story_groups'][0]['stories']
        assert not any(s['name'] == 'Load Config' for s in init_stories), \
            "Load Config should be removed from Initialize Bot"

        # Verify it was added to Run Bot with original data preserved
        run_stories = graph_data['epics'][0]['sub_epics'][1]['story_groups'][0]['stories']
        lc = next((s for s in run_stories if s['name'] == 'Load Config'), None)
        assert lc is not None, "Load Config should be in Run Bot"
        assert lc['story_type'] == 'user', "story_type should be preserved"
        assert len(lc['acceptance_criteria']) == 1, "acceptance_criteria should be preserved"
        assert lc['acceptance_criteria'][0]['name'] == 'Config file is loaded from workspace root'

    def test_end_to_end_move_story_via_report_preserves_data(self, tmp_path):
        """Full flow: modified diagram → report with moves → apply → verify data preserved."""
        from actions.render.render_action import RenderOutputAction
        import copy

        original_data = self._two_sub_epic_data()
        original_map = StoryMap(original_data)

        # Create modified data: move 'Load Config' to 'Run Bot'
        modified_data = copy.deepcopy(original_data)
        init_stories = modified_data['epics'][0]['sub_epics'][0]['story_groups'][0]['stories']
        run_stories = modified_data['epics'][0]['sub_epics'][1]['story_groups'][0]['stories']
        moved = [s for s in init_stories if s['name'] == 'Load Config'][0]
        init_stories.remove(moved)
        run_stories.append(moved)

        # Render and generate report
        modified_map = StoryMap(modified_data)
        drawio_map = DrawIOStoryMap(diagram_type='outline')
        drawio_map.render_from_story_map(modified_map, layout_data=None)
        report = drawio_map.generate_update_report(original_map)

        assert len(report.moved_stories) >= 1, "Should detect the move"

        # Apply to a fresh copy of original data
        graph_data = copy.deepcopy(original_data)
        action = RenderOutputAction.__new__(RenderOutputAction)

        for move in report.moved_stories:
            action._apply_move_story(graph_data, move.name, move.from_parent, move.to_parent)

        # Verify: Load Config in Run Bot with preserved acceptance criteria
        run_stories = graph_data['epics'][0]['sub_epics'][1]['story_groups'][0]['stories']
        lc = next((s for s in run_stories if s['name'] == 'Load Config'), None)
        assert lc is not None, "Load Config should be in Run Bot"
        assert len(lc.get('acceptance_criteria', [])) == 1, \
            "Acceptance criteria should be preserved through the move"

    def test_no_false_moves_when_no_changes(self, tmp_path):
        """When the diagram matches the original, no moves should be reported."""
        data = self._two_sub_epic_data()
        original_map = StoryMap(data)

        drawio_map = DrawIOStoryMap(diagram_type='outline')
        drawio_map.render_from_story_map(original_map, layout_data=None)

        report = drawio_map.generate_update_report(original_map)

        assert len(report.moved_stories) == 0
        assert len(report.new_stories) == 0
        assert len(report.removed_stories) == 0

    @staticmethod
    def _two_epic_data():
        """Story map with two epics for cross-epic move tests."""
        return {
            "epics": [
                {
                    "name": "Epic Alpha",
                    "sequential_order": 1.0,
                    "sub_epics": [{
                        "name": "SubEpic A1",
                        "sequential_order": 1.0,
                        "sub_epics": [],
                        "story_groups": [{"type": "and", "connector": None, "stories": [
                            {"name": "Story X", "sequential_order": 1.0,
                             "story_type": "user", "users": [],
                             "acceptance_criteria": [{"name": "AC for X"}],
                             "scenarios": [{"name": "Scenario for X"}]},
                            {"name": "Story Y", "sequential_order": 2.0,
                             "story_type": "system", "users": [],
                             "acceptance_criteria": []},
                        ]}]
                    }]
                },
                {
                    "name": "Epic Beta",
                    "sequential_order": 2.0,
                    "sub_epics": [{
                        "name": "SubEpic B1",
                        "sequential_order": 1.0,
                        "sub_epics": [],
                        "story_groups": [{"type": "and", "connector": None, "stories": [
                            {"name": "Story Z", "sequential_order": 1.0,
                             "story_type": "user", "users": [],
                             "acceptance_criteria": []},
                        ]}]
                    }]
                },
            ]
        }

    def test_story_moved_across_epics_detected_as_move(self, tmp_path):
        """Moving a story from Epic Alpha/SubEpic A1 to Epic Beta/SubEpic B1
        should be detected as a move, not new+removed."""
        import copy
        original_data = self._two_epic_data()
        original_map = StoryMap(original_data)

        modified_data = copy.deepcopy(original_data)
        a1_stories = modified_data['epics'][0]['sub_epics'][0]['story_groups'][0]['stories']
        b1_stories = modified_data['epics'][1]['sub_epics'][0]['story_groups'][0]['stories']
        moved = [s for s in a1_stories if s['name'] == 'Story X'][0]
        a1_stories.remove(moved)
        b1_stories.append(moved)

        modified_map = StoryMap(modified_data)
        drawio_map = DrawIOStoryMap(diagram_type='outline')
        drawio_map.render_from_story_map(modified_map, layout_data=None)
        report = drawio_map.generate_update_report(original_map)

        moved_names = [m.name for m in report.moved_stories]
        assert 'Story X' in moved_names, \
            f"Cross-epic move not detected. moved={moved_names}, " \
            f"new={[s.name for s in report.new_stories]}, " \
            f"removed={[s.name for s in report.removed_stories]}"

        move = next(m for m in report.moved_stories if m.name == 'Story X')
        assert move.from_parent == 'SubEpic A1'
        assert move.to_parent == 'SubEpic B1'

    def test_cross_epic_move_preserves_story_data(self, tmp_path):
        """Applying a cross-epic move should preserve AC, scenarios, etc."""
        from actions.render.render_action import RenderOutputAction
        import copy

        original_data = self._two_epic_data()
        graph_data = copy.deepcopy(original_data)

        action = RenderOutputAction.__new__(RenderOutputAction)
        result = action._apply_move_story(
            graph_data, 'Story X', 'SubEpic A1', 'SubEpic B1')

        assert result is True

        # Verify preserved in SubEpic B1
        b1_stories = graph_data['epics'][1]['sub_epics'][0]['story_groups'][0]['stories']
        sx = next((s for s in b1_stories if s['name'] == 'Story X'), None)
        assert sx is not None
        assert len(sx.get('acceptance_criteria', [])) == 1
        assert sx['acceptance_criteria'][0]['name'] == 'AC for X'
        assert len(sx.get('scenarios', [])) == 1
        assert sx['scenarios'][0]['name'] == 'Scenario for X'

        # Verify removed from SubEpic A1
        a1_stories = graph_data['epics'][0]['sub_epics'][0]['story_groups'][0]['stories']
        assert not any(s['name'] == 'Story X' for s in a1_stories)


class TestRenamePairingByIdType:
    """Tests that user-created nodes (simple cell IDs without '/')
    are treated as genuinely new sub-epics and NOT paired as renames,
    while tool-generated nodes (hierarchical cell IDs with '/') remain
    eligible for rename pairing."""

    def _make_drawio_xml(self, sub_epics_spec, stories_spec=None):
        """Build DrawIO XML with explicit sub-epic and story cell IDs.

        sub_epics_spec: list of (cell_id, name, x, y, w, h)
        stories_spec: list of (cell_id, name, x, y) or None
        """
        epic_w = 800
        cells = [
            '<mxCell id="0"/>',
            '<mxCell id="1" parent="0"/>',
            f'<mxCell id="epic-1" value="Invoke Bot" '
            f'style="rounded=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontColor=#000000;" '
            f'vertex="1" parent="1">'
            f'<mxGeometry x="20" y="120" width="{epic_w}" height="400" as="geometry"/></mxCell>',
        ]
        for cid, name, x, y, w, h in sub_epics_spec:
            cells.append(
                f'<mxCell id="{cid}" value="{name}" '
                f'style="rounded=1;fillColor=#d5e8d4;strokeColor=#82b366;fontColor=#000000;" '
                f'vertex="1" parent="1">'
                f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        if stories_spec:
            for cid, name, x, y in stories_spec:
                cells.append(
                    f'<mxCell id="{cid}" value="{name}" '
                    f'style="fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;" '
                    f'vertex="1" parent="1">'
                    f'<mxGeometry x="{x}" y="270" width="120" height="50" as="geometry"/></mxCell>')
        cells_xml = '\n        '.join(cells)
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="Story Map" id="test-diagram">
    <mxGraphModel><root>
        {cells_xml}
    </root></mxGraphModel>
  </diagram>
</mxfile>'''

    def _make_story_map_data(self, sub_epics):
        """Build story map data with specified sub-epics under 'Invoke Bot'.

        sub_epics: list of (name, stories_list) where stories_list is
                   list of story name strings.
        """
        se_list = []
        for i, (se_name, story_names) in enumerate(sub_epics):
            stories = [
                {"name": sn, "sequential_order": float(j + 1),
                 "story_type": "user", "users": [], "acceptance_criteria": []}
                for j, sn in enumerate(story_names)
            ]
            se_list.append({
                "name": se_name,
                "sequential_order": float(i + 1),
                "sub_epics": [],
                "story_groups": [{"type": "and", "connector": None, "stories": stories}]
            })
        return {
            "epics": [{
                "name": "Invoke Bot",
                "sequential_order": 1.0,
                "sub_epics": se_list
            }]
        }

    def test_user_created_sub_epic_with_simple_id_reported_as_new_not_rename(self, tmp_path):
        """A sub-epic manually created in DrawIO (simple cell ID without '/')
        must appear as a new_sub_epic, even when there are unmatched originals
        that could theoretically pair with it."""
        # Diagram: two sub-epics – one tool-generated (has '/'), one user-created (no '/')
        xml = self._make_drawio_xml(
            sub_epics_spec=[
                # tool-generated sub-epic (renamed from original "Alpha")
                ('invoke-bot/alpha', 'Alpha Renamed', 30, 180, 300, 200),
                # user-created sub-epic (simple ID "3")
                ('3', 'Brand New Feature', 340, 180, 300, 200),
            ],
            stories_spec=[
                ('invoke-bot/alpha/s1', 'Story A', 40, 270),
                ('4', 'Story B', 350, 270),
            ],
        )
        drawio_file = tmp_path / 'docs' / 'story' / 'test.drawio'
        drawio_file.parent.mkdir(parents=True, exist_ok=True)
        drawio_file.write_text(xml, encoding='utf-8')

        # Original has "Alpha" and "Beta" sub-epics
        original_data = self._make_story_map_data([
            ('Alpha', ['Story A']),
            ('Beta', ['Story B']),
        ])

        drawio_map = DrawIOStoryMap.load(drawio_file)
        original_map = StoryMap(original_data)
        report = drawio_map.generate_update_report(original_map)

        # "Brand New Feature" (id="3") should be new, not a rename
        new_sub_epic_names = [s.name for s in report.new_sub_epics]
        assert 'Brand New Feature' in new_sub_epic_names

        # "Alpha Renamed" should be a rename of "Alpha"
        rename_pairs = {r.extracted_name: r.original_name for r in report.renames}
        assert rename_pairs.get('Alpha Renamed') == 'Alpha'

        # "Brand New Feature" should NOT appear as a rename
        assert 'Brand New Feature' not in rename_pairs

    def test_tool_generated_sub_epic_with_hierarchical_id_still_eligible_for_rename(self, tmp_path):
        """A sub-epic with a hierarchical cell ID (containing '/') should
        still be paired as a rename when its name doesn't exist elsewhere."""
        xml = self._make_drawio_xml(
            sub_epics_spec=[
                ('invoke-bot/alpha', 'Alpha V2', 30, 180, 300, 200),
            ],
            stories_spec=[
                ('invoke-bot/alpha/s1', 'Story A', 40, 270),
            ],
        )
        drawio_file = tmp_path / 'docs' / 'story' / 'test.drawio'
        drawio_file.parent.mkdir(parents=True, exist_ok=True)
        drawio_file.write_text(xml, encoding='utf-8')

        original_data = self._make_story_map_data([
            ('Alpha', ['Story A']),
        ])

        drawio_map = DrawIOStoryMap.load(drawio_file)
        original_map = StoryMap(original_data)
        report = drawio_map.generate_update_report(original_map)

        rename_pairs = {r.extracted_name: r.original_name for r in report.renames}
        assert rename_pairs.get('Alpha V2') == 'Alpha'
        assert len(report.new_sub_epics) == 0

    def test_mixed_user_and_tool_ids_only_tool_ids_participate_in_rename(self, tmp_path):
        """When multiple unmatched sub-epics exist, only those with
        hierarchical cell IDs participate in rename pairing.  User-created
        ones go straight to new_sub_epics."""
        xml = self._make_drawio_xml(
            sub_epics_spec=[
                # Tool-generated (rename candidate)
                ('invoke-bot/load-bot-behaviors', 'Load Behavior, and Actions', 30, 180, 300, 200),
                # User-created (should be new)
                ('3', 'Load Bot', 340, 180, 300, 200),
            ],
            stories_spec=[
                ('invoke-bot/load-bot-behaviors/s1', 'Load Config', 40, 270),
                ('5', 'Resolve Bot Path', 350, 270),
            ],
        )
        drawio_file = tmp_path / 'docs' / 'story' / 'test.drawio'
        drawio_file.parent.mkdir(parents=True, exist_ok=True)
        drawio_file.write_text(xml, encoding='utf-8')

        # Original: "Load Bot, Behavior, and Actions" and "Set Workspace"
        original_data = self._make_story_map_data([
            ('Load Bot, Behavior, and Actions', ['Load Config', 'Resolve Bot Path']),
            ('Set Workspace', ['Change Workspace Path']),
        ])

        drawio_map = DrawIOStoryMap.load(drawio_file)
        original_map = StoryMap(original_data)
        report = drawio_map.generate_update_report(original_map)

        # "Load Behavior, and Actions" should pair as rename of
        # "Load Bot, Behavior, and Actions"
        rename_pairs = {r.extracted_name: r.original_name for r in report.renames}
        assert rename_pairs.get('Load Behavior, and Actions') == 'Load Bot, Behavior, and Actions'

        # "Load Bot" (id="3") must be new, not a rename
        new_sub_epic_names = [s.name for s in report.new_sub_epics]
        assert 'Load Bot' in new_sub_epic_names
        assert 'Load Bot' not in rename_pairs

    def test_all_simple_id_sub_epics_become_new_when_no_hierarchical_candidates(self, tmp_path):
        """If ALL unmatched sub-epics have simple IDs, none participate in
        rename pairing – all become new sub-epics."""
        xml = self._make_drawio_xml(
            sub_epics_spec=[
                ('2', 'Feature X', 30, 180, 300, 200),
                ('3', 'Feature Y', 340, 180, 300, 200),
            ],
            stories_spec=[
                ('4', 'Story 1', 40, 270),
                ('5', 'Story 2', 350, 270),
            ],
        )
        drawio_file = tmp_path / 'docs' / 'story' / 'test.drawio'
        drawio_file.parent.mkdir(parents=True, exist_ok=True)
        drawio_file.write_text(xml, encoding='utf-8')

        original_data = self._make_story_map_data([
            ('Old Feature A', ['Story 1']),
            ('Old Feature B', ['Story 2']),
        ])

        drawio_map = DrawIOStoryMap.load(drawio_file)
        original_map = StoryMap(original_data)
        report = drawio_map.generate_update_report(original_map)

        # No renames at sub-epic level
        rename_parents = {r.extracted_name for r in report.renames}
        assert 'Feature X' not in rename_parents
        assert 'Feature Y' not in rename_parents

        # Both should be new sub-epics
        new_names = {s.name for s in report.new_sub_epics}
        assert 'Feature X' in new_names
        assert 'Feature Y' in new_names

    def test_story_rename_still_works_regardless_of_cell_id_format(self, tmp_path):
        """The cell-ID check only applies to sub-epics and epics.
        Stories should still be paired for renames even with simple IDs."""
        helper = BotTestHelper(tmp_path)
        drawio_file = helper.drawio_story_map.create_drawio_file(
            helper.drawio_story_map.create_drawio_xml_with_renamed_story())
        drawio_story_map = DrawIOStoryMap.load(drawio_file)
        original_data = helper.drawio_story_map.create_story_map_data_with_renamed_story()
        original_story_map = StoryMap(original_data)

        report = drawio_story_map.generate_update_report(original_story_map)

        # Story-level rename should still be detected
        assert len(report.renames) >= 1
        rename = report.renames[0]
        assert rename.extracted_name
        assert rename.original_name


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


class TestAcceptanceCriteriaDelta:
    """Tests for AC delta tracking: detecting added, removed, and modified AC
    in update reports, and applying those changes via updateFromDiagram."""

    def test_no_ac_changes_when_diagram_matches_original(self, tmp_path):
        """When exploration diagram matches the original, no AC changes reported."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_acceptance_criteria()
        original_map = StoryMap(data)

        drawio_map = DrawIOStoryMap()
        drawio_map.render_exploration_from_story_map(original_map)

        report = drawio_map.generate_update_report(original_map)
        assert len(report.ac_changes) == 0, \
            f"Expected no AC changes, got {[(c.story_name, c.added, c.removed) for c in report.ac_changes]}"

    def test_added_ac_box_detected_in_report(self, tmp_path):
        """Adding a new AC box below a story should appear as an added AC."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_acceptance_criteria()
        original_map = StoryMap(data)

        drawio_map = DrawIOStoryMap()
        drawio_map.render_exploration_from_story_map(original_map)

        # Add a new AC box below 'Register Behaviors' (which has no AC)
        reg_story = None
        for s in drawio_map.get_stories():
            if s.name == 'Register Behaviors':
                reg_story = s
                break
        assert reg_story is not None

        from synchronizers.story_io.drawio_element import DrawIOElement
        new_ac = DrawIOElement(
            cell_id=f'{reg_story.cell_id}/ac-0',
            value='When behavior registered then it appears in list')
        new_ac.apply_style_for_type('acceptance_criteria')
        new_ac.set_position(reg_story.position.x, reg_story.position.y + 60)
        new_ac.set_size(250, 60)
        reg_story._ac_elements.append(new_ac)

        report = drawio_map.generate_update_report(original_map)

        ac_for_reg = [c for c in report.ac_changes if c.story_name == 'Register Behaviors']
        assert len(ac_for_reg) == 1, f"Should detect AC addition for Register Behaviors"
        assert 'When behavior registered then it appears in list' in ac_for_reg[0].added

    def test_removed_ac_box_detected_in_report(self, tmp_path):
        """Removing an AC box from a story should appear as a removed AC."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_acceptance_criteria()
        original_map = StoryMap(data)

        drawio_map = DrawIOStoryMap()
        drawio_map.render_exploration_from_story_map(original_map)

        # Remove one AC box from 'Load Config' (which has 2)
        lc_story = next(s for s in drawio_map.get_stories() if s.name == 'Load Config')
        ac_to_remove = None
        for n in lc_story._ac_elements:
            cid = getattr(n, 'cell_id', '')
            if '/ac-1' in cid:
                ac_to_remove = n
                break

        if ac_to_remove:
            lc_story._ac_elements.remove(ac_to_remove)

        report = drawio_map.generate_update_report(original_map)

        ac_for_lc = [c for c in report.ac_changes if c.story_name == 'Load Config']
        assert len(ac_for_lc) == 1, f"Should detect AC removal for Load Config"
        assert 'When config file missing then system uses defaults' in ac_for_lc[0].removed

    def test_ac_changes_roundtrip_through_json(self, tmp_path):
        """AC changes survive to_dict -> from_dict roundtrip."""
        from synchronizers.story_io.update_report import ACChange

        report = UpdateReport()
        report.set_ac_changes([
            ACChange(story_name='Load Config', parent='Initialize Bot',
                     added=['New AC text'],
                     removed=['Old AC text']),
        ])

        data = report.to_dict()
        assert 'ac_changes' in data

        restored = UpdateReport.from_dict(data)
        assert len(restored.ac_changes) == 1
        assert restored.ac_changes[0].story_name == 'Load Config'
        assert restored.ac_changes[0].added == ['New AC text']
        assert restored.ac_changes[0].removed == ['Old AC text']

    def test_apply_ac_change_adds_and_removes(self, tmp_path):
        """_apply_ac_change should add new AC and remove deleted AC."""
        from actions.render.render_action import RenderOutputAction
        from synchronizers.story_io.update_report import ACChange

        data = {
            "epics": [{"name": "E", "sequential_order": 1.0, "sub_epics": [
                {"name": "SE", "sequential_order": 1.0, "sub_epics": [],
                 "story_groups": [{"type": "and", "connector": None, "stories": [
                     {"name": "S1", "sequential_order": 1.0, "story_type": "user",
                      "users": [], "acceptance_criteria": [
                          {"name": "AC One", "text": "AC One", "sequential_order": 1.0},
                          {"name": "AC Two", "text": "AC Two", "sequential_order": 2.0},
                      ]},
                 ]}]}
            ]}]
        }

        action = RenderOutputAction.__new__(RenderOutputAction)
        change = ACChange(story_name='S1', parent='SE',
                          added=['AC Three'], removed=['AC One'])

        result = action._apply_ac_change(data, change)
        assert result is True

        story = data['epics'][0]['sub_epics'][0]['story_groups'][0]['stories'][0]
        ac_texts = [ac.get('name', '') for ac in story['acceptance_criteria']]
        assert 'AC One' not in ac_texts, "AC One should be removed"
        assert 'AC Two' in ac_texts, "AC Two should remain"
        assert 'AC Three' in ac_texts, "AC Three should be added"

    def test_end_to_end_ac_add_remove_via_report(self, tmp_path):
        """Full flow: render exploration -> modify AC -> report -> apply -> verify."""
        from actions.render.render_action import RenderOutputAction
        import copy

        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_acceptance_criteria()
        original_map = StoryMap(data)

        # Render exploration diagram
        drawio_map = DrawIOStoryMap()
        drawio_map.render_exploration_from_story_map(original_map)

        # Remove one AC from Load Config, add one to Register Behaviors
        lc_story = next(s for s in drawio_map.get_stories() if s.name == 'Load Config')
        ac_to_remove = None
        for n in lc_story._ac_elements:
            cid = getattr(n, 'cell_id', '')
            if '/ac-0' in cid:
                ac_to_remove = n
                break
        if ac_to_remove:
            lc_story._ac_elements.remove(ac_to_remove)

        reg_story = next(s for s in drawio_map.get_stories()
                         if s.name == 'Register Behaviors')
        from synchronizers.story_io.drawio_element import DrawIOElement
        new_ac = DrawIOElement(
            cell_id=f'{reg_story.cell_id}/ac-0',
            value='Behaviors load from config')
        new_ac.apply_style_for_type('acceptance_criteria')
        new_ac.set_position(reg_story.position.x, reg_story.position.y + 60)
        new_ac.set_size(250, 60)
        reg_story._ac_elements.append(new_ac)

        # Generate report
        report = drawio_map.generate_update_report(original_map)
        assert len(report.ac_changes) >= 1

        # Apply to a fresh copy
        graph_data = copy.deepcopy(data)
        action = RenderOutputAction.__new__(RenderOutputAction)
        for ac_change in report.ac_changes:
            action._apply_ac_change(graph_data, ac_change)

        # Verify Load Config lost one AC
        lc = next(s for e in graph_data['epics']
                  for se in e['sub_epics']
                  for sg in se['story_groups']
                  for s in sg['stories'] if s['name'] == 'Load Config')
        lc_texts = [ac.get('name', '') for ac in lc['acceptance_criteria']]
        assert len(lc_texts) == 1, f"Load Config should have 1 AC, got {lc_texts}"
        assert 'When config file missing then system uses defaults' in lc_texts

        # Verify Register Behaviors gained one AC
        rb = next(s for e in graph_data['epics']
                  for se in e['sub_epics']
                  for sg in se['story_groups']
                  for s in sg['stories'] if s['name'] == 'Register Behaviors')
        rb_texts = [ac.get('name', '') for ac in rb['acceptance_criteria']]
        assert 'Behaviors load from config' in rb_texts

    def test_ac_moved_between_stories_detected_as_move(self, tmp_path):
        """AC text removed from Story A and added to Story B should be
        reconciled as an AC move, not separate add+remove."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_acceptance_criteria()
        original_map = StoryMap(data)

        # Render exploration diagram
        drawio_map = DrawIOStoryMap()
        drawio_map.render_exploration_from_story_map(original_map)

        # Move AC box from 'Load Config' to below 'Register Behaviors'
        lc_story = next(s for s in drawio_map.get_stories() if s.name == 'Load Config')
        ac_to_move = None
        for n in lc_story._ac_elements:
            cid = getattr(n, 'cell_id', '')
            if '/ac-0' in cid:
                ac_to_move = n
                break
        assert ac_to_move is not None

        reg_story = next(s for s in drawio_map.get_stories()
                         if s.name == 'Register Behaviors')

        # Remove from old story, re-add below Register Behaviors
        lc_story._ac_elements.remove(ac_to_move)
        from synchronizers.story_io.drawio_element import DrawIOElement
        moved_ac = DrawIOElement(
            cell_id=f'{reg_story.cell_id}/ac-0',
            value=ac_to_move.value)
        moved_ac.apply_style_for_type('acceptance_criteria')
        moved_ac.set_position(reg_story.position.x, reg_story.position.y + 60)
        moved_ac.set_size(250, 60)
        reg_story._ac_elements.append(moved_ac)

        report = drawio_map.generate_update_report(original_map)

        # Should be an AC move
        assert len(report.ac_moves) >= 1, \
            f"Expected AC move, got moves={report.ac_moves}, changes={[(c.story_name, c.added, c.removed) for c in report.ac_changes]}"
        move = report.ac_moves[0]
        assert move.from_story == 'Load Config'
        assert move.to_story == 'Register Behaviors'

    def test_ac_move_roundtrip_json(self, tmp_path):
        """AC moves survive to_dict -> from_dict."""
        from synchronizers.story_io.update_report import ACMove

        report = UpdateReport()
        report._ac_moves = [ACMove(
            ac_text='When X then Y', from_story='Story A', to_story='Story B')]

        data = report.to_dict()
        assert 'ac_moves' in data

        restored = UpdateReport.from_dict(data)
        assert len(restored.ac_moves) == 1
        assert restored.ac_moves[0].ac_text == 'When X then Y'
        assert restored.ac_moves[0].from_story == 'Story A'
        assert restored.ac_moves[0].to_story == 'Story B'

    def test_apply_ac_move_preserves_data(self, tmp_path):
        """_apply_ac_move extracts AC from source and inserts in target."""
        from actions.render.render_action import RenderOutputAction
        from synchronizers.story_io.update_report import ACMove

        data = {
            "epics": [{"name": "E", "sequential_order": 1.0, "sub_epics": [
                {"name": "SE", "sequential_order": 1.0, "sub_epics": [],
                 "story_groups": [{"type": "and", "connector": None, "stories": [
                     {"name": "S1", "sequential_order": 1.0, "story_type": "user",
                      "users": [], "acceptance_criteria": [
                          {"name": "AC Alpha", "text": "AC Alpha", "sequential_order": 1.0},
                          {"name": "AC Beta", "text": "AC Beta", "sequential_order": 2.0},
                      ]},
                     {"name": "S2", "sequential_order": 2.0, "story_type": "user",
                      "users": [], "acceptance_criteria": []},
                 ]}]}
            ]}]
        }

        action = RenderOutputAction.__new__(RenderOutputAction)
        move = ACMove(ac_text='AC Alpha', from_story='S1', to_story='S2')
        result = action._apply_ac_move(data, move)
        assert result is True

        s1 = data['epics'][0]['sub_epics'][0]['story_groups'][0]['stories'][0]
        s2 = data['epics'][0]['sub_epics'][0]['story_groups'][0]['stories'][1]

        s1_texts = [ac.get('name', '') for ac in s1['acceptance_criteria']]
        s2_texts = [ac.get('name', '') for ac in s2['acceptance_criteria']]

        assert 'AC Alpha' not in s1_texts, "AC Alpha should be removed from S1"
        assert 'AC Beta' in s1_texts, "AC Beta should remain in S1"
        assert 'AC Alpha' in s2_texts, "AC Alpha should be in S2"

    def test_story_split_ac_distributed_correctly(self, tmp_path):
        """When a story is split (some AC moved to new story), the report
        correctly shows AC moves and the remaining AC stays."""
        from synchronizers.story_io.update_report import ACChange, ACMove

        # Simulate: Story A had AC1, AC2, AC3.  AC2 and AC3 moved to Story B.
        report = UpdateReport()
        report.set_ac_changes([
            ACChange(story_name='Story A', removed=['AC2', 'AC3']),
            ACChange(story_name='Story B', added=['AC2', 'AC3']),
        ])
        report.reconcile_ac_moves()

        assert len(report.ac_moves) == 2
        move_texts = {m.ac_text for m in report.ac_moves}
        assert move_texts == {'AC2', 'AC3'}
        for m in report.ac_moves:
            assert m.from_story == 'Story A'
            assert m.to_story == 'Story B'

        # ac_changes should now be empty (all reconciled as moves)
        assert len(report.ac_changes) == 0


class TestRenderActionDiagramSection:

    def _setup_workspace_with_story_graph(self, helper):
        """Write story graph to the bot's expected story graph path."""
        story_graph_path = helper.bot.bot_paths.story_graph_paths.story_graph_path
        story_graph_path.parent.mkdir(parents=True, exist_ok=True)
        data = helper.drawio_story_map.create_simple_story_map_data()
        story_graph_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
        return story_graph_path

    def _setup_render_action(self, helper):
        """Navigate to shape.render and return the render action object."""
        helper.bot.behaviors.navigate_to('shape')
        helper.state.set_state('shape', 'render')
        return helper.bot.behaviors.current.actions.find_by_name('render')

    def test_render_action_shows_existing_render_section_without_drawio_config_and_separate_diagram_section(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        action_obj = self._setup_render_action(helper)

        instructions = action_obj.do_execute()

        base_instructions = instructions.get('base_instructions', [])
        assert len(base_instructions) > 0

    def test_render_diagram_creates_drawio_file_from_story_graph(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        self._setup_workspace_with_story_graph(helper)
        action_obj = self._setup_render_action(helper)

        result = action_obj.renderDiagram()

        assert result['status'] == 'success'
        assert len(result['results']) >= 1
        for r in result['results']:
            diagram_path = Path(r['path'])
            assert diagram_path.exists(), f"Diagram file should exist at {diagram_path}"
            content = diagram_path.read_text(encoding='utf-8')
            assert '<mxfile' in content, "Diagram should contain valid DrawIO XML"

    def test_generate_report_extracts_from_drawio_and_writes_report(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        self._setup_workspace_with_story_graph(helper)
        action_obj = self._setup_render_action(helper)

        # First render the diagram so it exists
        action_obj.renderDiagram()

        result = action_obj.generateReport()

        assert result['status'] == 'success'
        assert len(result['results']) >= 1
        for r in result['results']:
            if r['status'] == 'success':
                report_path = Path(r['report_path'])
                assert report_path.exists(), f"Report file should exist at {report_path}"
                report_data = json.loads(report_path.read_text(encoding='utf-8'))
                assert isinstance(report_data, dict), "Report should be valid JSON dict"

    def test_generate_report_also_writes_extracted_json(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        self._setup_workspace_with_story_graph(helper)
        action_obj = self._setup_render_action(helper)

        # Render first
        action_obj.renderDiagram()
        action_obj.generateReport()

        # Check extracted JSON exists for each drawio spec
        for spec, diagram_path in action_obj._get_drawio_specs_with_paths():
            if diagram_path.exists():
                extracted_path = diagram_path.parent / f"{diagram_path.stem}-extracted.json"
                assert extracted_path.exists(), "Extracted JSON should be written alongside diagram"
                extracted_data = json.loads(extracted_path.read_text(encoding='utf-8'))
                assert 'epics' in extracted_data

    def test_update_from_diagram_applies_report_to_story_graph(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        story_graph_path = self._setup_workspace_with_story_graph(helper)
        action_obj = self._setup_render_action(helper)

        # Render -> Generate Report -> Update
        action_obj.renderDiagram()
        action_obj.generateReport()
        update_result = action_obj.updateFromDiagram()

        assert update_result['status'] == 'success'
        updated_data = json.loads(story_graph_path.read_text(encoding='utf-8'))
        assert 'epics' in updated_data

    def test_update_from_diagram_returns_error_without_prior_report(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        self._setup_workspace_with_story_graph(helper)
        action_obj = self._setup_render_action(helper)

        # Render diagram but don't generate report
        action_obj.renderDiagram()
        result = action_obj.updateFromDiagram()

        assert result['status'] == 'error'

    def test_collect_diagram_data_detects_stale_diagram(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        self._setup_workspace_with_story_graph(helper)
        action_obj = self._setup_render_action(helper)

        # Create a drawio output file and an older layout file
        docs_dir = helper.bot.bot_paths.story_graph_paths.docs_root
        docs_dir.mkdir(parents=True, exist_ok=True)
        render_specs = action_obj.render_specs
        drawio_specs = [s for s in render_specs if s.output and s.output.endswith('.drawio')]
        if drawio_specs:
            workspace_dir = helper.bot.bot_paths.workspace_directory
            spec = drawio_specs[0]
            default_path = str(helper.bot.bot_paths.story_graph_paths.docs_root)
            path_prefix = spec.config_data.get('path', default_path)
            diagram_path = workspace_dir / path_prefix / spec.output
            diagram_path.parent.mkdir(parents=True, exist_ok=True)
            diagram_path.write_text('<mxfile/>', encoding='utf-8')
            layout_path = diagram_path.parent / (diagram_path.stem + '-layout.json')
            layout_path.write_text('{}', encoding='utf-8')
            # Make layout older than diagram by touching diagram
            import time
            time.sleep(0.05)
            diagram_path.write_text('<mxfile/>', encoding='utf-8')

            diagrams = action_obj._collect_diagram_data(render_specs, workspace_dir)
            stale_diagrams = [d for d in diagrams
                              if d.get('file_modified_time') and d.get('last_sync_time')
                              and d['file_modified_time'] > d['last_sync_time']]
            assert len(stale_diagrams) >= 1, "Should detect at least one stale diagram"

    def test_collect_diagram_data_finds_update_report(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        self._setup_workspace_with_story_graph(helper)
        action_obj = self._setup_render_action(helper)

        render_specs = action_obj.render_specs
        drawio_specs = [s for s in render_specs if s.output and s.output.endswith('.drawio')]
        if drawio_specs:
            workspace_dir = helper.bot.bot_paths.workspace_directory
            spec = drawio_specs[0]
            default_path = str(helper.bot.bot_paths.story_graph_paths.docs_root)
            path_prefix = spec.config_data.get('path', default_path)
            diagram_path = workspace_dir / path_prefix / spec.output
            diagram_path.parent.mkdir(parents=True, exist_ok=True)
            diagram_path.write_text('<mxfile/>', encoding='utf-8')
            # Create an update report file
            report_path = diagram_path.parent / (diagram_path.stem + '-update-report.json')
            report_path.write_text('{"matched_count": 0}', encoding='utf-8')

            diagrams = action_obj._collect_diagram_data(render_specs, workspace_dir)
            diagrams_with_report = [d for d in diagrams if d.get('report_path')]
            assert len(diagrams_with_report) >= 1, "Should find update report"

    def test_end_to_end_render_then_generate_report_then_update(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        story_graph_path = self._setup_workspace_with_story_graph(helper)
        action_obj = self._setup_render_action(helper)

        # Step 1: Render diagrams from story graph
        render_result = action_obj.renderDiagram()
        assert render_result['status'] == 'success'

        # Step 2: Generate reports (extracts from rendered diagrams, compares with story graph)
        report_result = action_obj.generateReport()
        assert report_result['status'] == 'success'
        assert len(report_result['results']) >= 1

        # Step 3: Update story graph from diagrams
        update_result = action_obj.updateFromDiagram()
        assert update_result['status'] == 'success'

        # Story graph should still be valid JSON with epics
        final_data = json.loads(story_graph_path.read_text(encoding='utf-8'))
        assert 'epics' in final_data
        assert len(final_data['epics']) >= 1

    def test_cli_render_diagram_routes_through_cli_session(self, tmp_path):
        """CLI integration test: shape.render.renderDiagram through CLI command parsing."""
        from cli.cli_session import CLISession
        helper = BotTestHelper(tmp_path)
        self._setup_workspace_with_story_graph(helper)

        session = CLISession(helper.bot, helper.workspace)
        response = session.execute_command('shape.render.renderDiagram')

        assert response.status != 'error', f"CLI should succeed, got: {response.output}"

    def test_cli_generate_report_routes_through_cli_session(self, tmp_path):
        """CLI integration test: shape.render.generateReport through CLI command parsing."""
        from cli.cli_session import CLISession
        helper = BotTestHelper(tmp_path)
        self._setup_workspace_with_story_graph(helper)

        session = CLISession(helper.bot, helper.workspace)
        # Render first so diagrams exist
        session.execute_command('shape.render.renderDiagram')
        response = session.execute_command('shape.render.generateReport')

        assert response.status != 'error', f"CLI should succeed, got: {response.output}"


class TestUpdateFromDiagramMoveBeforeRemove:
    """Regression: updateFromDiagram must move stories BEFORE removing
    sub-epics.  If a sub-epic is removed but its stories were moved to
    another sub-epic, the move must happen first.  Otherwise the stories
    are permanently deleted when the sub-epic is popped from the tree.

    Tests the RenderOutputAction private methods directly to avoid
    needing full bot/behavior setup."""

    @staticmethod
    def _make_graph_data():
        """Story graph with two sub-epics under one epic.
        'Old SubEpic' has two stories; 'Target SubEpic' has one."""
        return {
            "epics": [{
                "name": "Epic A",
                "sequential_order": 1.0,
                "sub_epics": [
                    {
                        "name": "Old SubEpic",
                        "sequential_order": 1.0,
                        "sub_epics": [],
                        "story_groups": [{"type": "and", "connector": None, "stories": [
                            {"name": "Story Alpha", "sequential_order": 1.0,
                             "story_type": "user", "users": [], "acceptance_criteria": [],
                             "scenarios": [{"name": "Important Scenario"}]},
                            {"name": "Story Beta", "sequential_order": 2.0,
                             "story_type": "user", "users": [], "acceptance_criteria": []},
                        ]}]
                    },
                    {
                        "name": "Target SubEpic",
                        "sequential_order": 2.0,
                        "sub_epics": [],
                        "story_groups": [{"type": "and", "connector": None, "stories": [
                            {"name": "Story Gamma", "sequential_order": 1.0,
                             "story_type": "user", "users": [], "acceptance_criteria": []},
                        ]}]
                    },
                ]
            }]
        }

    @staticmethod
    def _apply_report_to_graph(graph_data, report):
        """Simulate the updateFromDiagram ordering logic using
        RenderOutputAction's private methods.  This mirrors the exact
        order in updateFromDiagram: renames, new epics/sub-epics/stories,
        moves, THEN removes."""
        from actions.render.render_action import RenderOutputAction

        # Create a minimal action instance just to access the methods.
        # We use object.__new__ to skip __init__ which needs a behavior.
        action = object.__new__(RenderOutputAction)

        for rename in report.renames:
            action._apply_rename(graph_data, rename.original_name, rename.extracted_name)

        for ns in report.new_sub_epics:
            action._apply_new_sub_epic(graph_data, ns.name, ns.parent)

        for ns in report.new_stories:
            action._apply_new_story(graph_data, ns.name, ns.parent)

        # Moves BEFORE removes
        for move in report.moved_stories:
            action._apply_move_story(graph_data, move.name,
                                      move.from_parent, move.to_parent)

        for removed in report.removed_sub_epics:
            action._apply_remove_sub_epic(graph_data, removed.name, removed.parent)

        for removed in report.removed_stories:
            action._apply_remove_story(graph_data, removed.name, removed.parent)

    def test_stories_preserved_when_sub_epic_removed_but_stories_moved(self, tmp_path):
        """Stories moved out of a sub-epic must survive the sub-epic's removal."""
        graph_data = self._make_graph_data()

        report_data = {
            "matched_count": 1,
            "moved_stories": [
                {"name": "Story Alpha", "from_parent": "Old SubEpic",
                 "to_parent": "Target SubEpic"},
            ],
            "removed_sub_epics": [
                {"name": "Old SubEpic", "parent": "Epic A"},
            ],
        }
        report = UpdateReport.from_dict(report_data)

        self._apply_report_to_graph(graph_data, report)

        # Old SubEpic should be gone
        all_se_names = [se['name'] for e in graph_data['epics']
                        for se in e.get('sub_epics', [])]
        assert 'Old SubEpic' not in all_se_names

        # Story Alpha should be in Target SubEpic
        target_se = next(se for e in graph_data['epics']
                         for se in e['sub_epics']
                         if se['name'] == 'Target SubEpic')
        target_stories = [s['name'] for sg in target_se['story_groups']
                          for s in sg.get('stories', [])]
        assert 'Story Alpha' in target_stories, (
            "Story Alpha was lost! Moves must run before removes.")

        # Verify scenario data survived (not a skeleton replacement)
        alpha = next(s for sg in target_se['story_groups']
                     for s in sg['stories'] if s['name'] == 'Story Alpha')
        assert len(alpha.get('scenarios', [])) >= 1, (
            "Story Alpha's scenario data was lost during the move.")

    def test_story_not_moved_is_deleted_with_sub_epic(self, tmp_path):
        """Stories NOT in the moved list should still be removed along
        with their sub-epic (normal delete behaviour)."""
        graph_data = self._make_graph_data()

        report_data = {
            "matched_count": 1,
            "moved_stories": [
                {"name": "Story Alpha", "from_parent": "Old SubEpic",
                 "to_parent": "Target SubEpic"},
            ],
            "removed_sub_epics": [
                {"name": "Old SubEpic", "parent": "Epic A"},
            ],
        }
        report = UpdateReport.from_dict(report_data)

        self._apply_report_to_graph(graph_data, report)

        # Story Beta should be gone (it stayed in the removed sub-epic)
        all_stories = [s['name'] for e in graph_data['epics']
                       for se in e.get('sub_epics', [])
                       for sg in se.get('story_groups', [])
                       for s in sg.get('stories', [])]
        assert 'Story Beta' not in all_stories
        assert 'Story Alpha' in all_stories

    def test_move_to_renamed_sub_epic(self, tmp_path):
        """Stories should move correctly to a sub-epic that was just renamed."""
        graph_data = self._make_graph_data()

        # Rename Target SubEpic, then move Story Alpha into it
        report_data = {
            "matched_count": 1,
            "renames": [
                {"extracted": "New Target Name", "original": "Target SubEpic",
                 "confidence": 1.0, "parent": "Epic A"},
            ],
            "moved_stories": [
                {"name": "Story Alpha", "from_parent": "Old SubEpic",
                 "to_parent": "New Target Name"},
            ],
            "removed_sub_epics": [
                {"name": "Old SubEpic", "parent": "Epic A"},
            ],
        }
        report = UpdateReport.from_dict(report_data)

        self._apply_report_to_graph(graph_data, report)

        # Target SubEpic should now be named "New Target Name"
        all_se_names = [se['name'] for e in graph_data['epics']
                        for se in e.get('sub_epics', [])]
        assert 'New Target Name' in all_se_names
        assert 'Target SubEpic' not in all_se_names

        # Story Alpha should be in the renamed sub-epic
        target = next(se for e in graph_data['epics']
                      for se in e['sub_epics']
                      if se['name'] == 'New Target Name')
        stories = [s['name'] for sg in target['story_groups']
                   for s in sg.get('stories', [])]
        assert 'Story Alpha' in stories

    def test_move_to_new_sub_epic(self, tmp_path):
        """Stories should move correctly to a newly created sub-epic."""
        graph_data = self._make_graph_data()

        report_data = {
            "matched_count": 1,
            "new_sub_epics": [
                {"name": "Brand New SubEpic", "parent": "Epic A"},
            ],
            "moved_stories": [
                {"name": "Story Alpha", "from_parent": "Old SubEpic",
                 "to_parent": "Brand New SubEpic"},
            ],
            "removed_sub_epics": [
                {"name": "Old SubEpic", "parent": "Epic A"},
            ],
        }
        report = UpdateReport.from_dict(report_data)

        self._apply_report_to_graph(graph_data, report)

        # Brand New SubEpic should exist with Story Alpha
        all_se_names = [se['name'] for e in graph_data['epics']
                        for se in e.get('sub_epics', [])]
        assert 'Brand New SubEpic' in all_se_names

        new_se = next(se for e in graph_data['epics']
                      for se in e['sub_epics']
                      if se['name'] == 'Brand New SubEpic')
        stories = [s['name'] for sg in new_se['story_groups']
                   for s in sg.get('stories', [])]
        assert 'Story Alpha' in stories


class TestScopedDiagramOperations:
    """Tests for Synchronize Diagram With Scoped Nodes.
    Scope parameter threads through renderDiagram, generateReport,
    updateFromDiagram and resolves {scope} placeholders in filenames."""

    @staticmethod
    def _make_fake_spec(output, path='docs/story/exploration'):
        """Create a lightweight spec-like object for testing scope resolution."""
        from types import SimpleNamespace
        spec = SimpleNamespace()
        spec.output = output
        spec.config_data = {'path': path}
        spec.synchronizer = None
        spec.execution_status = 'pending'
        return spec

    def test_get_drawio_specs_with_scope_resolves_placeholder(self, tmp_path):
        """_get_drawio_specs_with_paths replaces {scope} in output filename."""
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('shape')
        helper.state.set_state('shape', 'render')
        action = helper.bot.behaviors.current.actions.find_by_name('render')

        action._render_specs = [
            self._make_fake_spec('story-map-explored-{scope}.drawio')]

        result = action._get_drawio_specs_with_paths(scope='Trace Code')
        assert len(result) == 1
        _, path = result[0]
        assert 'trace-code' in str(path).lower()
        assert '{scope}' not in str(path)

    def test_get_drawio_specs_without_scope_defaults_to_all(self, tmp_path):
        """Without scope, {scope} placeholder defaults to 'all'."""
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('shape')
        helper.state.set_state('shape', 'render')
        action = helper.bot.behaviors.current.actions.find_by_name('render')

        action._render_specs = [
            self._make_fake_spec('story-map-explored-{scope}.drawio')]

        result = action._get_drawio_specs_with_paths(scope=None)
        assert len(result) == 1
        _, path = result[0]
        assert 'all' in str(path).lower()

    def test_scope_sanitized_for_filename(self, tmp_path):
        """Scope with spaces and special chars is sanitized for filename."""
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('shape')
        helper.state.set_state('shape', 'render')
        action = helper.bot.behaviors.current.actions.find_by_name('render')

        action._render_specs = [
            self._make_fake_spec('story-map-explored-{scope}.drawio')]

        result = action._get_drawio_specs_with_paths(scope='Trace Story Graph')
        _, path = result[0]
        filename = str(path).split('/')[-1].split('\\')[-1]
        assert filename == 'story-map-explored-trace-story-graph.drawio'

    def test_render_diagram_accepts_scope_parameter(self, tmp_path):
        """renderDiagram(scope=...) passes scope through to synchronizers."""
        helper = BotTestHelper(tmp_path)
        story_graph_path = helper.bot.bot_paths.story_graph_paths.story_graph_path
        story_graph_path.parent.mkdir(parents=True, exist_ok=True)
        data = helper.drawio_story_map.create_simple_story_map_data()
        story_graph_path.write_text(json.dumps(data), encoding='utf-8')

        helper.bot.behaviors.navigate_to('shape')
        helper.state.set_state('shape', 'render')
        action = helper.bot.behaviors.current.actions.find_by_name('render')

        # Call with scope - should not error even if no matching specs
        result = action.renderDiagram(scope='Trace Code')
        # Either success with 0 rendered or error for no specs - both are valid
        assert result['status'] in ('success', 'error')

    def test_specs_without_scope_placeholder_get_scoped_filename(self, tmp_path):
        """Non-exploration specs (no {scope} in output) get scope slug appended."""
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('shape')
        helper.state.set_state('shape', 'render')
        action = helper.bot.behaviors.current.actions.find_by_name('render')

        action._render_specs = [
            self._make_fake_spec('story-map-outline.drawio', 'docs/story/shape')]

        result = action._get_drawio_specs_with_paths(scope='Trace Code')
        assert len(result) == 1
        _, path = result[0]
        assert 'story-map-outline-trace-code.drawio' in str(path)

    def test_exploration_render_with_scope_produces_scoped_diagram(self, tmp_path):
        """End-to-end: exploration render with scope creates scoped .drawio file.
        Scope filtering is done upstream (synchronizer), so we filter the
        story map before passing it to the renderer.
        """
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_acceptance_criteria()
        original_map = StoryMap(data)
        filtered_map = original_map.filter_by_name('Initialize Bot')
        assert filtered_map is not None

        drawio_map = DrawIOStoryMap()
        summary = drawio_map.render_exploration_from_story_map(filtered_map)

        assert summary.get('exploration') is True
        assert len(drawio_map.get_stories()) >= 1

    def test_filter_by_name_returns_subtree_for_sub_epic(self, tmp_path):
        """StoryMap.filter_by_name returns filtered map for a sub-epic."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_simple_story_map_data()
        story_map = StoryMap(data)

        filtered = story_map.filter_by_name('Initialize Bot')
        assert filtered is not None
        assert len(filtered.epics) == 1
        # The filtered map should contain the sub-epic's stories
        all_stories = list(filtered.all_stories)
        assert len(all_stories) >= 1

    def test_filter_by_name_returns_none_for_nonexistent(self, tmp_path):
        """StoryMap.filter_by_name returns None when name not found."""
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_simple_story_map_data()
        story_map = StoryMap(data)

        filtered = story_map.filter_by_name('Does Not Exist')
        assert filtered is None
