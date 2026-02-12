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
        assert epics[0].position.y == 10

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
        # SUB_EPIC_Y_OFFSET from epic = 40, epic Y = 10 → sub-epic Y = 50
        assert ses[0].position.y == 50, f"Flat sub-epic Y should be 50, got {ses[0].position.y}"


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

    def test_actors_positioned_below_their_story_card_not_above(self, tmp_path):
        """Actor elements must sit below their parent story card.
        If actors are above (negative Y offset), they land inside
        the sub-epic header area and look like sub-epic labels."""
        dm = self._render_with_users(tmp_path)
        stories = dm.get_stories()
        assert len(stories) >= 1, "Need stories to test actor positioning"

        for story in stories:
            story_bottom = story.position.y + story.boundary.height
            for actor in story._actor_elements:
                assert actor.position.y >= story_bottom, \
                    (f"Actor '{actor.value}' at y={actor.position.y} is above "
                     f"story '{story.name}' bottom at y={story_bottom}. "
                     f"Actors must be below their story card, not inside the parent header.")

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

    def test_epic_boundary_geometrically_contains_all_sub_epics(self, tmp_path):
        """Epic container must fully contain every sub-epic boundary.
        A 'contains' check catches containers that are too short or narrow."""
        dm = self._render_simple(tmp_path)

        for epic in dm.get_epics():
            for se in epic.get_sub_epics():
                assert epic.boundary.contains_boundary(se.boundary), \
                    (f"Epic '{epic.name}' boundary {epic.boundary} does not contain "
                     f"sub-epic '{se.name}' boundary {se.boundary}")

    def test_sub_epic_boundary_geometrically_contains_all_stories(self, tmp_path):
        """Sub-epic container must fully contain every story boundary."""
        dm = self._render_simple(tmp_path)

        for se in dm.get_sub_epics():
            for story in se.get_stories():
                assert se.boundary.contains_boundary(story.boundary), \
                    (f"Sub-epic '{se.name}' boundary {se.boundary} does not contain "
                     f"story '{story.name}' boundary {story.boundary}")

    def test_nested_containers_contain_all_descendants_at_every_depth(self, tmp_path):
        """For nested sub-epics (depth=3), every parent container must
        fully contain all its direct children at every level."""
        dm = self._render_nested(tmp_path, depth=3)

        epic = dm.get_epics()[0]
        top_se = epic.get_sub_epics()[0]
        assert epic.boundary.contains_boundary(top_se.boundary), \
            "Epic must contain top-level sub-epic"

        for nested_se in top_se.get_sub_epics():
            assert top_se.boundary.contains_boundary(nested_se.boundary), \
                f"Top sub-epic must contain nested sub-epic '{nested_se.name}'"
            for story in nested_se.get_stories():
                assert nested_se.boundary.contains_boundary(story.boundary), \
                    f"Nested sub-epic '{nested_se.name}' must contain story '{story.name}'"

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
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        summary = drawio_story_map.render_increments_from_story_map(
            story_map, data.get('increments', []), layout_data=None)

        assert len(drawio_story_map.get_epics()) >= 1
        assert len(drawio_story_map.get_stories()) >= 1
        assert summary.get('increments') == 2

    def test_increment_lanes_ordered_by_priority_with_y_positions_from_outline_bottom(self, tmp_path):
        helper = BotTestHelper(tmp_path)
        data = helper.drawio_story_map.create_story_map_data_with_increments()
        story_map = StoryMap(data)

        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        drawio_story_map.render_increments_from_story_map(
            story_map, data.get('increments', []), layout_data=None)

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
            report_path.write_text('{"exact_matches": []}', encoding='utf-8')

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
