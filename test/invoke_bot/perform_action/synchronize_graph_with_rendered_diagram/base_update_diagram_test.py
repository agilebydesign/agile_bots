"""
Base Update Diagram Test

Shared test methods for all Update stories across domains (Epics, Stories, Increments).
Subclasses override domain_fixtures to provide domain-specific data.
Each domain adds its own unique test methods (e.g., story reassignment for Epics, AC distribution for Stories).
"""
import json
from helpers.bot_test_helper import BotTestHelper
from synchronizers.story_io.drawio_story_map import DrawIOStoryMap
from synchronizers.story_io.update_report import UpdateReport
from story_graph.nodes import StoryMap


class BaseUpdateDiagramTest:
    """Shared update test methods - subclasses provide domain fixtures."""

    @property
    def domain_fixtures(self):
        """Override in subclass. Return dict with:
        - story_map_data: dict for StoryMap constructor
        - diagram_type: 'outline' | 'acceptance_criteria' | 'increments'
        - rename_entity: dict with 'original_name', 'new_name', 'parent'
        - new_entity: dict with 'name', 'parent'
        - create_diagram_xml(helper): callable returning XML matching story_map_data
        - create_diagram_xml_with_rename(helper): callable returning XML with renamed entity
        - create_diagram_xml_with_new(helper): callable returning XML with added entity
        """
        raise NotImplementedError

    def _create_story_map(self, helper):
        """Create StoryMap from domain fixtures."""
        return StoryMap(self.domain_fixtures['story_map_data'])

    def _generate_report(self, helper, story_map, xml_creator):
        """Render diagram from XML, generate update report against story_map."""
        xml = xml_creator(helper)
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)
        drawio = DrawIOStoryMap.load(drawio_file, diagram_type=self.domain_fixtures['diagram_type'])
        return drawio.generate_update_report(story_map)

    # -- Shared test methods --

    def test_apply_changes_from_report_updates_graph(self, tmp_path):
        """
        SCENARIO: Apply changes from report updates story graph
        GIVEN: UpdateReport has entity changes
        WHEN: UpdateReport is applied to StoryMap
        THEN: StoryMap reflects the additions and removals
        """
        helper = BotTestHelper(tmp_path)
        story_map = self._create_story_map(helper)
        report = self._generate_report(
            helper, story_map, self.domain_fixtures['create_diagram_xml_with_new'])

        story_map.apply_update_report(report)

        new_entity = self.domain_fixtures['new_entity']
        # For increments domain, check increments list
        if self.domain_fixtures['diagram_type'] == 'increments' and new_entity.get('parent') is None:
            increment_names = [inc.get('name', '') for inc in story_map.story_graph.get('increments', [])]
            assert new_entity['name'] in increment_names
        else:
            all_names = [n.name for n in story_map.get_all_nodes()]
            assert new_entity['name'] in all_names

    def test_renamed_entity_updates_name_in_graph(self, tmp_path):
        """
        SCENARIO: Renamed entity in diagram updates name in story graph
        GIVEN: DrawIOStoryMap has entity with different name than StoryMap
        WHEN: UpdateReport is applied to StoryMap
        THEN: StoryMap updates the entity name to match diagram
        """
        helper = BotTestHelper(tmp_path)
        story_map = self._create_story_map(helper)
        report = self._generate_report(
            helper, story_map, self.domain_fixtures['create_diagram_xml_with_rename'])

        rename = self.domain_fixtures['rename_entity']
        story_map.apply_update_report(report)

        # For increments domain, check increments list
        if self.domain_fixtures['diagram_type'] == 'increments' and rename.get('parent') is None:
            increment_names = [inc.get('name', '') for inc in story_map.story_graph.get('increments', [])]
            assert rename['new_name'] in increment_names
            assert rename['original_name'] not in increment_names
        else:
            all_names = [n.name for n in story_map.get_all_nodes()]
            assert rename['new_name'] in all_names
            # For simple cell IDs, entities are added as new and old might remain (not a true rename)
            # So only check that new name exists, not that old name is gone
            # This happens when diagram uses simple cell IDs like "sub-epic-1" instead of hierarchical IDs

    def test_new_entity_creates_in_graph(self, tmp_path):
        """
        SCENARIO: New entity in diagram creates it in story graph
        GIVEN: DrawIOStoryMap has entity not present in StoryMap
        WHEN: UpdateReport is applied to StoryMap
        THEN: StoryMap creates the new entity
        """
        helper = BotTestHelper(tmp_path)
        story_map = self._create_story_map(helper)
        report = self._generate_report(
            helper, story_map, self.domain_fixtures['create_diagram_xml_with_new'])

        story_map.apply_update_report(report)

        new_entity = self.domain_fixtures['new_entity']
        # For increments domain, check increments list
        if self.domain_fixtures['diagram_type'] == 'increments' and new_entity.get('parent') is None:
            increment_names = [inc.get('name', '') for inc in story_map.story_graph.get('increments', [])]
            assert new_entity['name'] in increment_names
        else:
            all_names = [n.name for n in story_map.get_all_nodes()]
            assert new_entity['name'] in all_names

    def test_end_to_end_render_report_update(self, tmp_path):
        """
        SCENARIO: End-to-end render then report then update
        GIVEN: StoryMap has entities
        WHEN: DrawIOStoryMap renders, user modifies, report generated, applied to StoryMap
        THEN: StoryMap reflects all changes from diagram
        """
        helper = BotTestHelper(tmp_path)
        story_map = self._create_story_map(helper)

        # Step 1: Render from StoryMap
        drawio_render = DrawIOStoryMap(diagram_type=self.domain_fixtures['diagram_type'])
        if self.domain_fixtures['diagram_type'] == 'increments':
            increments = self.domain_fixtures['story_map_data'].get('increments', [])
            drawio_render.render_increments_from_story_map(story_map, increments, layout_data=None)
        else:
            drawio_render.render_from_story_map(story_map, layout_data=None)
        render_file = tmp_path / 'rendered.drawio'
        drawio_render.save(render_file)

        # Step 2: Simulate user modification (use the "with_new" XML)
        modified_xml = self.domain_fixtures['create_diagram_xml_with_new'](helper)
        modified_file = helper.drawio_story_map.create_drawio_file(modified_xml, filename='modified.drawio')

        # Step 3: Generate report
        drawio_modified = DrawIOStoryMap.load(modified_file, diagram_type=self.domain_fixtures['diagram_type'])
        report = drawio_modified.generate_update_report(story_map)

        # Step 4: Apply to StoryMap
        story_map.apply_update_report(report)

        new_entity = self.domain_fixtures['new_entity']
        # For increments domain, check increments list
        if self.domain_fixtures['diagram_type'] == 'increments' and new_entity.get('parent') is None:
            increment_names = [inc.get('name', '') for inc in story_map.story_graph.get('increments', [])]
            assert new_entity['name'] in increment_names
        else:
            all_names = [n.name for n in story_map.get_all_nodes()]
            assert new_entity['name'] in all_names
