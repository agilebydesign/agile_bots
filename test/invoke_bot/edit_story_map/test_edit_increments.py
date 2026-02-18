import pytest
from helpers.bot_test_helper import BotTestHelper
from helpers import TTYBotTestHelper, PipeBotTestHelper, JsonBotTestHelper
from invoke_bot.edit_story_map.increment_helper import (
    story_graph_with_increments_mvp_phase2,
    story_graph_with_increment_named_mvp,
    story_graph_with_increments_mvp_phase1,
    story_graph_with_increment_and_story,
    story_graph_with_story_in_multiple_increments,
    story_graph_with_two_stories_in_same_parent,
)


def get_story_names_from_increment(increment):
    """Return story names from an increment stories array."""
    return [s["name"] if isinstance(s, dict) else s for s in increment.stories]


class TestAddIncrement:
    def test_add_increment_after_selected(self, tmp_path):
        """Add increment after selected increment."""
        helper = BotTestHelper(tmp_path)
        helper.increment.create_story_graph_with_increments(story_graph_with_increments_mvp_phase2())
        story_map = helper.increment.get_story_map()

        story_map.add_increment("Phase 1.5", after="MVP")

        increments = story_map.increments.sorted_by_priority
        names = [inc.name for inc in increments]
        assert names == ["MVP", "Phase 1.5", "Phase 2"]
        phase15 = story_map.increments.find_by_name("Phase 1.5")
        assert phase15.priority == 2
        assert phase15.stories == []

    def test_add_increment_when_nothing_selected_appends_to_back(self, tmp_path):
        """Add increment when nothing selected appends to back."""
        helper = BotTestHelper(tmp_path)
        helper.increment.create_story_graph_with_increments(story_graph_with_increments_mvp_phase2())
        story_map = helper.increment.get_story_map()

        story_map.add_increment("Phase 3", after=None)

        increments = story_map.increments.sorted_by_priority
        names = [inc.name for inc in increments]
        assert names == ["MVP", "Phase 2", "Phase 3"]
        phase3 = story_map.increments.find_by_name("Phase 3")
        assert phase3.priority == 3

    def test_add_increment_duplicate_name_returns_error(self, tmp_path):
        """Add increment with duplicate name returns error."""
        helper = BotTestHelper(tmp_path)
        helper.increment.create_story_graph_with_increments(story_graph_with_increment_named_mvp())
        story_map = helper.increment.get_story_map()

        with pytest.raises(ValueError, match="already exists"):
            story_map.add_increment("MVP", after=None)

    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper,
    ])
    def test_cli_add_increment_after_mvp(self, tmp_path, helper_class):
        """CLI adds increment after MVP with bumped priorities."""
        helper = helper_class(tmp_path)
        helper.domain.increment.create_story_graph_with_increments(
            story_graph_with_increments_mvp_phase2()
        )

        cli_response = helper.cli_session.execute_command(
            'story_graph.add_increment name:"Phase 1.5" after:"MVP"'
        )

        story_map = helper.domain.bot.story_map
        increments = story_map.increments.sorted_by_priority
        names = [inc.name for inc in increments]
        assert names == ["MVP", "Phase 1.5", "Phase 2"]
        phase15 = story_map.increments.find_by_name("Phase 1.5")
        assert phase15.priority == 2
        assert "success" in cli_response.output.lower()

    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper,
    ])
    def test_cli_add_increment_append(self, tmp_path, helper_class):
        """CLI appends increment to end when no after specified."""
        helper = helper_class(tmp_path)
        helper.domain.increment.create_story_graph_with_increments(
            story_graph_with_increments_mvp_phase2()
        )

        cli_response = helper.cli_session.execute_command(
            'story_graph.add_increment name:"Phase 3"'
        )

        story_map = helper.domain.bot.story_map
        increments = story_map.increments.sorted_by_priority
        names = [inc.name for inc in increments]
        assert names == ["MVP", "Phase 2", "Phase 3"]
        phase3 = story_map.increments.find_by_name("Phase 3")
        assert phase3.priority == 3
        assert "success" in cli_response.output.lower()

class TestRemoveIncrement:
    def test_remove_increment_by_name(self, tmp_path):
        """Remove increment by name."""
        helper = BotTestHelper(tmp_path)
        helper.increment.create_story_graph_with_increments(story_graph_with_increment_named_mvp())
        story_map = helper.increment.get_story_map()

        removed = story_map.remove_increment("MVP")

        assert removed is True
        assert story_map.increments.find_by_name("MVP") is None

    def test_remove_nonexistent_increment_returns_error(self, tmp_path):
        """Remove non-existent increment returns error."""
        helper = BotTestHelper(tmp_path)
        helper.increment.create_story_graph_with_increments(story_graph_with_increments_mvp_phase2())
        story_map = helper.increment.get_story_map()

        removed = story_map.remove_increment("Missing")

        assert removed is False

    def test_remove_increment_with_stories_leaves_hierarchy_unchanged(self, tmp_path):
        """Remove increment that contains stories leaves hierarchy unchanged."""
        helper = BotTestHelper(tmp_path)
        helper.increment.create_story_graph_with_increments(
            story_graph_with_increment_and_story("MVP", "Validate Order")
        )
        story_map = helper.increment.get_story_map()

        removed = story_map.remove_increment("MVP")

        assert removed is True
        assert story_map.increments.find_by_name("MVP") is None
        assert any(s.name == "Validate Order" for s in story_map.all_stories)

    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper,
    ])
    def test_cli_remove_increment(self, tmp_path, helper_class):
        """CLI removes increment and displays confirmation."""
        helper = helper_class(tmp_path)
        helper.domain.increment.create_story_graph_with_increments(
            story_graph_with_increment_named_mvp()
        )

        cli_response = helper.cli_session.execute_command(
            'story_graph.remove_increment increment_name:"MVP"'
        )

        story_map = helper.domain.bot.story_map
        assert story_map.increments.find_by_name("MVP") is None
        assert "success" in cli_response.output.lower()


class TestRenameIncrement:
    def test_rename_increment_to_new_name(self, tmp_path):
        """Rename increment to new name, stories array preserved."""
        helper = BotTestHelper(tmp_path)
        helper.increment.create_story_graph_with_increments(
            story_graph_with_increment_and_story("MVP", "Validate Order")
        )
        story_map = helper.increment.get_story_map()
        original_stories = get_story_names_from_increment(story_map.increments.find_by_name("MVP"))

        story_map.rename_increment("MVP", "Phase 1")

        assert story_map.increments.find_by_name("MVP") is None
        phase1 = story_map.increments.find_by_name("Phase 1")
        assert phase1 is not None
        assert get_story_names_from_increment(phase1) == original_stories

    def test_rename_increment_duplicate_name_returns_error(self, tmp_path):
        """Rename increment to duplicate existing name returns error."""
        helper = BotTestHelper(tmp_path)
        helper.increment.create_story_graph_with_increments(story_graph_with_increments_mvp_phase1())
        story_map = helper.increment.get_story_map()

        with pytest.raises(ValueError, match="already exists"):
            story_map.rename_increment("MVP", "Phase 1")

    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper,
    ])
    def test_cli_rename_increment(self, tmp_path, helper_class):
        """CLI renames increment and displays confirmation."""
        helper = helper_class(tmp_path)
        helper.domain.increment.create_story_graph_with_increments(
            story_graph_with_increment_named_mvp()
        )

        cli_response = helper.cli_session.execute_command(
            'story_graph.rename_increment from_name:"MVP" to_name:"Phase 1"'
        )

        story_map = helper.domain.bot.story_map
        assert story_map.increments.find_by_name("MVP") is None
        assert story_map.increments.find_by_name("Phase 1") is not None

class TestAddStoryToIncrement:
    def test_add_story_to_increment_by_name(self, tmp_path):
        """Add story to increment by story name."""
        helper = BotTestHelper(tmp_path)
        # Create Profile is already in MVP; Validate Order is in hierarchy but not assigned
        helper.increment.create_story_graph_with_increments(
            story_graph_with_two_stories_in_same_parent("Create Profile", "Validate Order")
        )
        story_map = helper.increment.get_story_map()

        story_map.add_story_to_increment("MVP", "Validate Order")

        assert "Validate Order" in get_story_names_from_increment(story_map.increments["MVP"])

    def test_add_nonexistent_story_returns_error(self, tmp_path):
        """Add non-existent story to increment returns error."""
        helper = BotTestHelper(tmp_path)
        helper.increment.create_story_graph_with_increments(story_graph_with_increment_named_mvp())
        story_map = helper.increment.get_story_map()

        with pytest.raises(ValueError, match="not found"):
            story_map.add_story_to_increment("MVP", "Missing Story")

    def test_add_story_already_in_increment_returns_error(self, tmp_path):
        """Add story already in increment returns error."""
        helper = BotTestHelper(tmp_path)
        helper.increment.create_story_graph_with_increments(
            story_graph_with_increment_and_story("MVP", "Validate Order")
        )
        story_map = helper.increment.get_story_map()

        with pytest.raises(ValueError, match="already in"):
            story_map.add_story_to_increment("MVP", "Validate Order")

    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper,
    ])
    def test_cli_add_story_to_increment(self, tmp_path, helper_class):
        """CLI adds story to increment and displays confirmation."""
        helper = helper_class(tmp_path)
        helper.domain.increment.create_story_graph_with_increments(
            story_graph_with_two_stories_in_same_parent("Create Profile", "Validate Order")
        )

        cli_response = helper.cli_session.execute_command(
            'story_graph.add_story_to_increment increment_name:"MVP" story_name:"Validate Order"'
        )

        story_map = helper.domain.bot.story_map
        mvp = story_map.increments.find_by_name("MVP")
        assert "Validate Order" in get_story_names_from_increment(mvp)


class TestRemoveStoryFromIncrement:
    def test_remove_story_from_increment(self, tmp_path):
        """Remove story from increment."""
        helper = BotTestHelper(tmp_path)
        helper.increment.create_story_graph_with_increments(
            story_graph_with_increment_and_story("MVP", "Validate Order")
        )
        story_map = helper.increment.get_story_map()

        story_map.remove_story_from_increment("MVP", "Validate Order")

        assert "Validate Order" not in get_story_names_from_increment(story_map.increments["MVP"])
        assert any(s.name == "Validate Order" for s in story_map.all_stories)

    def test_remove_story_not_in_increment_returns_error(self, tmp_path):
        """Remove story not in increment returns error."""
        helper = BotTestHelper(tmp_path)
        helper.increment.create_story_graph_with_increments(story_graph_with_increment_named_mvp())
        story_map = helper.increment.get_story_map()

        with pytest.raises(ValueError, match="not in"):
            story_map.remove_story_from_increment("MVP", "Validate Order")

    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper,
    ])
    def test_cli_remove_story_from_increment(self, tmp_path, helper_class):
        """CLI removes story from increment and displays confirmation."""
        helper = helper_class(tmp_path)
        helper.domain.increment.create_story_graph_with_increments(
            story_graph_with_increment_and_story("MVP", "Validate Order")
        )

        cli_response = helper.cli_session.execute_command(
            'story_graph.remove_story_from_increment increment_name:"MVP" story_name:"Validate Order"'
        )

        story_map = helper.domain.bot.story_map
        mvp = story_map.increments.find_by_name("MVP")
        assert "Validate Order" not in get_story_names_from_increment(mvp)

class TestRenameStoryInIncrement:
    def test_rename_story_updates_increment_references(self, tmp_path):
        """Rename story node updates all increment references."""
        helper = BotTestHelper(tmp_path)
        helper.increment.create_story_graph_with_increments(
            story_graph_with_increment_and_story("MVP", "Validate Order")
        )
        story_map = helper.increment.get_story_map()

        story_map.rename_story_in_hierarchy("Validate Order", "Validate Order Items")

        assert story_map.find_story_by_name("Validate Order") is None
        assert story_map.find_story_by_name("Validate Order Items") is not None
        mvp = story_map.increments["MVP"]
        assert "Validate Order Items" in get_story_names_from_increment(mvp)
        assert "Validate Order" not in get_story_names_from_increment(mvp)

    def test_rename_story_duplicate_name_returns_error(self, tmp_path):
        """Rename story to duplicate name in same parent returns error."""
        helper = BotTestHelper(tmp_path)
        helper.increment.create_story_graph_with_increments(
            story_graph_with_two_stories_in_same_parent("Validate Order", "Validate Order Items")
        )
        story_map = helper.increment.get_story_map()

        with pytest.raises(ValueError, match="already exists|duplicate"):
            story_map.rename_story_in_hierarchy("Validate Order", "Validate Order Items")

    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper,
    ])
    def test_cli_rename_story_updates_increments(self, tmp_path, helper_class):
        """CLI renames story and updates all increment references."""
        helper = helper_class(tmp_path)
        helper.domain.increment.create_story_graph_with_increments(
            story_graph_with_increment_and_story("MVP", "Validate Order")
        )

        cli_response = helper.cli_session.execute_command(
            'story_graph.rename_story_in_hierarchy old_name:"Validate Order" new_name:"Validate Order Items"'
        )

        story_map = helper.domain.bot.story_map
        assert story_map.find_story_by_name("Validate Order") is None
        assert story_map.find_story_by_name("Validate Order Items") is not None
        mvp = story_map.increments.find_by_name("MVP")
        assert "Validate Order Items" in get_story_names_from_increment(mvp)
        assert "Validate Order" not in get_story_names_from_increment(mvp)


class TestStoryDeletedInHierarchyCascadesToIncrement:
    def test_delete_story_in_hierarchy_removes_from_all_increments(self, tmp_path):
        """Delete story in hierarchy removes from all increments."""
        helper = BotTestHelper(tmp_path)
        helper.increment.create_story_graph_with_increments(
            story_graph_with_story_in_multiple_increments("Validate Order", ["MVP", "Phase 2"])
        )
        story_map = helper.increment.get_story_map()

        story = story_map.find_story_by_name("Validate Order")
        assert story is not None
        story.delete()

        assert story_map.find_story_by_name("Validate Order") is None
        for inc in story_map.increments:
            assert "Validate Order" not in get_story_names_from_increment(inc)

        story_map2 = helper.increment.get_story_map()
        assert story_map2.find_story_by_name("Validate Order") is None
        for inc in story_map2.increments:
            assert "Validate Order" not in get_story_names_from_increment(inc)