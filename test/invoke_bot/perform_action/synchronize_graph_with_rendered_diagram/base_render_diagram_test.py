"""
Base Render Diagram Test

Shared test methods for all Render stories across domains (Epics, Stories, Increments).
Subclasses override domain_fixtures to provide domain-specific data.
Each domain adds its own unique test methods for domain-specific scenarios.
"""
from helpers.bot_test_helper import BotTestHelper
from synchronizers.story_io.drawio_story_map import DrawIOStoryMap
from synchronizers.story_io.layout_data import LayoutData
from story_graph.nodes import StoryMap


class BaseRenderDiagramTest:
    """Shared render test methods - subclasses provide domain fixtures."""

    @property
    def domain_fixtures(self):
        """Override in subclass. Return dict with:
        - story_map_data: dict for StoryMap constructor
        - diagram_type: 'outline' | 'acceptance_criteria' | 'increments'
        - layout_data: dict of saved positions (key format: 'TYPE|name')
        - expected_epic_count: int
        - expected_sub_epic_count: int
        """
        raise NotImplementedError

    def _create_story_map(self, helper):
        return StoryMap(self.domain_fixtures['story_map_data'])

    def _render_diagram(self, helper, story_map, layout_data=None):
        drawio = DrawIOStoryMap(diagram_type=self.domain_fixtures['diagram_type'])
        if self.domain_fixtures['diagram_type'] == 'increments':
            increments = self.domain_fixtures['story_map_data'].get('increments', [])
            drawio.render_increments_from_story_map(story_map, increments, layout_data=layout_data)
        else:
            drawio.render_from_story_map(story_map, layout_data=layout_data)
        return drawio

    # -- Shared test methods --

    def test_default_layout_renders_valid_output(self, tmp_path):
        """
        SCENARIO: Render with default layout produces valid DrawIO output
        GIVEN: StoryMap exists with domain entities, no LayoutData exists
        WHEN: DrawIOStoryMap renders from StoryMap
        THEN: output is valid DrawIO XML with correct entity structure
        """
        helper = BotTestHelper(tmp_path)
        story_map = self._create_story_map(helper)

        drawio = self._render_diagram(helper, story_map, layout_data=None)

        output_file = tmp_path / 'rendered.drawio'
        drawio.save(output_file)
        assert output_file.exists()
        content = output_file.read_text(encoding='utf-8')
        assert '<?xml' in content
        assert '<mxfile' in content
        assert len(drawio.get_epics()) == self.domain_fixtures['expected_epic_count']

    def test_re_render_with_saved_layout_preserves_positions(self, tmp_path):
        """
        SCENARIO: Re-render with saved layout data preserves positions
        GIVEN: LayoutData exists with saved positions
        WHEN: DrawIOStoryMap renders from StoryMap
        THEN: entities are rendered at saved positions
        """
        helper = BotTestHelper(tmp_path)
        story_map = self._create_story_map(helper)
        layout_file = helper.drawio_story_map.create_layout_data_file(
            layout_data=self.domain_fixtures.get('layout_data'))
        layout_data = LayoutData.load(layout_file)

        drawio = self._render_diagram(helper, story_map, layout_data=layout_data)

        epics = drawio.get_epics()
        assert len(epics) >= 1
        saved = self.domain_fixtures.get('layout_data', {})
        if saved:
            first_key = next(iter(saved))
            assert epics[0].position.x == saved[first_key]['x']

    def test_render_writes_valid_drawio_file(self, tmp_path):
        """
        SCENARIO: Render completes and writes valid DrawIO file
        GIVEN: StoryMap exists with domain entities
        WHEN: DrawIOStoryMap renders and saves to file
        THEN: file exists and contains valid DrawIO XML with correct counts
        """
        helper = BotTestHelper(tmp_path)
        story_map = self._create_story_map(helper)

        drawio = self._render_diagram(helper, story_map, layout_data=None)
        output_file = tmp_path / 'output.drawio'
        drawio.save(output_file)

        assert output_file.exists()
        assert len(drawio.get_epics()) == self.domain_fixtures['expected_epic_count']
        assert len(drawio.get_sub_epics()) == self.domain_fixtures['expected_sub_epic_count']

    def test_cells_have_required_styles(self, tmp_path):
        """
        SCENARIO: All cells have required styles for extractor detection
        GIVEN: StoryMap exists with domain entities
        WHEN: DrawIOStoryMap renders from StoryMap
        THEN: all cells have whiteSpace wrap and html enabled
        """
        helper = BotTestHelper(tmp_path)
        story_map = self._create_story_map(helper)

        drawio = self._render_diagram(helper, story_map, layout_data=None)
        output_file = tmp_path / 'styled.drawio'
        drawio.save(output_file)

        content = output_file.read_text(encoding='utf-8')
        assert 'whiteSpace=wrap' in content
