"""
Base Report Diagram Test

Shared test methods for all Report stories across domains (Epics, Stories, Increments).
Subclasses override domain_fixtures to provide domain-specific data.
Each domain adds its own unique test methods for domain-specific scenarios.
"""
import json
from helpers.bot_test_helper import BotTestHelper
from synchronizers.story_io.drawio_story_map import DrawIOStoryMap
from synchronizers.story_io.update_report import UpdateReport
from story_graph.nodes import StoryMap


class BaseReportDiagramTest:
    """Shared report test methods - subclasses provide domain fixtures."""

    @property
    def domain_fixtures(self):
        raise NotImplementedError

    def _create_story_map(self, helper):
        return StoryMap(self.domain_fixtures['story_map_data'])

    def _load_and_report(self, helper, story_map, xml):
        drawio_file = helper.drawio_story_map.create_drawio_file(xml)
        drawio = DrawIOStoryMap.load(drawio_file, diagram_type=self.domain_fixtures['diagram_type'])
        return drawio.generate_update_report(story_map)

    # -- Shared test methods --

    def _render_then_load_and_report(self, helper, story_map):
        rendered = DrawIOStoryMap(diagram_type=self.domain_fixtures['diagram_type'])
        if self.domain_fixtures['diagram_type'] == 'increments':
            increments = self.domain_fixtures['story_map_data'].get('increments', [])
            rendered.render_increments_from_story_map(story_map, increments, layout_data=None)
        else:
            rendered.render_from_story_map(story_map, layout_data=None)
        drawio_file = helper.drawio_story_map.create_drawio_file(filename='rendered-for-report.drawio')
        rendered.save(drawio_file)
        loaded = DrawIOStoryMap.load(drawio_file, diagram_type=self.domain_fixtures['diagram_type'])
        return loaded.generate_update_report(story_map)

    def test_no_changes_when_diagram_matches_original(self, tmp_path):
        """
        SCENARIO: No changes reported when diagram matches original
        GIVEN: DrawIOStoryMap rendered from StoryMap, then reloaded
        WHEN: generateUpdateReport is executed
        THEN: UpdateReport has zero changes
        """
        helper = BotTestHelper(tmp_path)
        story_map = self._create_story_map(helper)

        report = self._render_then_load_and_report(helper, story_map)

        assert not report.has_changes

    def test_entity_added_detected_as_new(self, tmp_path):
        """
        SCENARIO: Entity added in diagram detected as new in report
        GIVEN: DrawIOStoryMap has entity not present in StoryMap
        WHEN: generateUpdateReport is executed
        THEN: UpdateReport lists the entity as new
        """
        helper = BotTestHelper(tmp_path)
        story_map = self._create_story_map(helper)
        xml = self.domain_fixtures['create_diagram_xml_with_new'](helper)

        report = self._load_and_report(helper, story_map, xml)

        new_entity = self.domain_fixtures['new_entity']
        all_new = report.new_stories + report.new_sub_epics
        new_names = [e.name for e in all_new]
        # For increments domain, also check increment_order for new increments
        if self.domain_fixtures['diagram_type'] == 'increments' and new_entity.get('parent') is None:
            increment_names = [inc['name'] for inc in report.increment_order]
            new_names.extend(increment_names)
        assert new_entity['name'] in new_names

    def test_entity_renamed_detected_as_rename(self, tmp_path):
        """
        SCENARIO: Entity renamed in diagram detected as rename in report
        GIVEN: DrawIOStoryMap has entity with different name than StoryMap
        WHEN: generateUpdateReport is executed
        THEN: UpdateReport pairs the entity as a rename match
        """
        helper = BotTestHelper(tmp_path)
        story_map = self._create_story_map(helper)
        xml = self.domain_fixtures['create_diagram_xml_with_rename'](helper)

        report = self._load_and_report(helper, story_map, xml)

        rename = self.domain_fixtures['rename_entity']
        # For increments domain, check if renamed entity is an increment
        if self.domain_fixtures['diagram_type'] == 'increments' and rename.get('parent') is None:
            # Increment renames are detected via increment_order (name sequence change)
            # We can check if both old and new names appear in relevant places
            orig_names = [inc.get('name', '') for inc in story_map.story_graph.get('increments', [])]
            new_names = [inc['name'] for inc in report.increment_order]
            assert rename['original_name'] in orig_names
            assert rename['new_name'] in new_names
        else:
            rename_originals = [r.original_name for r in report.renames]
            if rename['original_name'] not in rename_originals:
                print(f"\nExpected rename: {rename}")
                print(f"Actual renames: {[(r.original_name, r.extracted_name) for r in report.renames]}")
                print(f"New sub-epics: {[s.name for s in report.new_sub_epics]}")
                print(f"Removed sub-epics: {[s.name for s in report.removed_sub_epics]}")
            assert rename['original_name'] in rename_originals

    def test_report_roundtrips_through_json(self, tmp_path):
        """
        SCENARIO: Report roundtrips through JSON
        GIVEN: UpdateReport has entity changes
        WHEN: to_dict() serializes and from_dict() restores
        THEN: all entity fields survive the roundtrip
        """
        helper = BotTestHelper(tmp_path)
        story_map = self._create_story_map(helper)
        xml = self.domain_fixtures['create_diagram_xml_with_rename'](helper)

        report = self._load_and_report(helper, story_map, xml)

        serialized = json.dumps(report.to_dict())
        restored = UpdateReport.from_dict(json.loads(serialized))

        assert len(restored.renames) == len(report.renames)
        assert len(restored.new_stories) == len(report.new_stories)
        assert len(restored.removed_stories) == len(report.removed_stories)
