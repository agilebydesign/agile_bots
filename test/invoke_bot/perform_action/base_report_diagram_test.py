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
        drawio = DrawIOStoryMap(diagram_type=self.domain_fixtures['diagram_type'])
        drawio.load(drawio_file)
        return drawio.generate_update_report(story_map)

    # -- Shared test methods --

    def test_no_changes_when_diagram_matches_original(self, tmp_path):
        """
        SCENARIO: No changes reported when diagram matches original
        GIVEN: DrawIOStoryMap has same structure as StoryMap
        WHEN: generateUpdateReport is executed
        THEN: UpdateReport has zero changes
        """
        helper = BotTestHelper(tmp_path)
        story_map = self._create_story_map(helper)
        xml = self.domain_fixtures['create_diagram_xml'](helper)

        report = self._load_and_report(helper, story_map, xml)

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
        rename_originals = [r.original_name for r in report.renames]
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
