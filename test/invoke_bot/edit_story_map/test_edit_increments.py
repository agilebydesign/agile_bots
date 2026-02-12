import pytest
from helpers.bot_test_helper import BotTestHelper


class TestDisplayIncrementScopeViewCLI:
    
    @pytest.mark.parametrize("increment_name,increment_priority,stories", [
        ("MVP Release", 1, [("Create Profile", 1), ("Authenticate User", 2)]),
        ("Enhancement Release", 2, [("Add Payment Method", 1), ("View History", 2)]),
    ])
    def test_cli_returns_simple_increments_object_with_stories(
        self, tmp_path, increment_name, increment_priority, stories
    ):
        """
        SCENARIO: CLI returns simple Increments object with stories
        
        GIVEN story graph contains increments with stories assigned
        AND CLI session is active
        WHEN User requests increment view via CLI
        THEN CLI returns Increments object containing collection of Increment
        AND each Increment contains name, priority, and stories array
        AND stories array contains Story objects from StoryNode
        """
        helper = BotTestHelper(tmp_path)
        story_graph = given_story_graph_with_increment(
            helper, increment_name, increment_priority, stories
        )
        
        # When
        increments = when_user_requests_increment_view_via_cli(helper, story_graph)
        
        # Then
        then_cli_returns_increments_object(increments)
        then_increment_contains_name_priority_stories(
            increments, increment_name, increment_priority, len(stories)
        )
    
    @pytest.mark.parametrize("increment_name,increment_priority,stories,expected_output", [
        (
            "MVP Release", 1,
            [("Create Profile", 1), ("Authenticate User", 2)],
            "MVP Release:\n  - Create Profile\n  - Authenticate User"
        ),
        (
            "Enhancement Release", 2,
            [("Add Payment Method", 1), ("View History", 2)],
            "Enhancement Release:\n  - Add Payment Method\n  - View History"
        ),
    ])
    def test_cli_displays_increment_list_with_stories_in_natural_order(
        self, tmp_path, increment_name, increment_priority, stories, expected_output
    ):
        """
        SCENARIO: CLI displays increment list with stories in natural order
        
        GIVEN story graph contains increments with stories assigned
        AND CLI session is active
        WHEN User enters increment view command
        THEN CLI displays each increment with name as header
        AND CLI lists stories in natural sequential order under each increment
        AND output is simple list format without hierarchy nesting
        """
        helper = BotTestHelper(tmp_path)
        story_graph = given_story_graph_with_increment(
            helper, increment_name, increment_priority, stories
        )
        
        # When
        output = when_user_enters_increment_view_command(helper, story_graph)
        
        # Then
        then_cli_displays_increment_with_stories_in_order(output, expected_output)
    
    @pytest.mark.parametrize("increment_name,increment_priority,expected_output", [
        ("Backlog", 99, "Backlog:\n  (no stories)"),
    ])
    def test_cli_displays_empty_increment_with_no_stories_message(
        self, tmp_path, increment_name, increment_priority, expected_output
    ):
        """
        SCENARIO: CLI displays empty increment with no stories message
        
        GIVEN story graph contains an increment with no stories assigned
        AND CLI session is active
        WHEN User enters increment view command
        THEN CLI displays increment name as header
        AND CLI shows empty state message for increment with no stories
        """
        helper = BotTestHelper(tmp_path)
        story_graph = given_story_graph_with_empty_increment(
            helper, increment_name, increment_priority
        )
        
        # When
        output = when_user_enters_increment_view_command(helper, story_graph)
        
        # Then
        then_cli_displays_empty_increment_message(output, expected_output)
    
    @pytest.mark.parametrize("story_property,source,included_in_increment_view", [
        ("name", "StoryNode.name", True),
        ("test_class", "StoryNode.test_class", True),
        ("sequential_order", "StoryNode.sequential_order", True),
    ])
    def test_cli_returns_increments_object_using_existing_storynode_domain_objects(
        self, tmp_path, story_property, source, included_in_increment_view
    ):
        """
        SCENARIO: CLI returns Increments object using existing StoryNode domain objects
        
        GIVEN story graph contains increments referencing Story nodes
        AND CLI session is active
        WHEN User requests increment view via CLI
        THEN CLI returns Increments collection
        AND Increment.stories contains references to existing StoryNode objects
        AND Story objects include standard StoryNode properties
        """
        helper = BotTestHelper(tmp_path)
        story_graph = given_story_graph_with_increment_referencing_story_nodes(helper)
        
        # When
        increments = when_user_requests_increment_view_via_cli(helper, story_graph)
        
        # Then
        then_story_objects_include_property(increments, story_property)
    
    @pytest.mark.parametrize("increment_count,expected_message", [
        (0, "No increments defined in story graph"),
    ])
    def test_cli_displays_message_when_no_increments_exist(
        self, tmp_path, increment_count, expected_message
    ):
        """
        SCENARIO: CLI displays message when no increments exist
        
        GIVEN story graph contains no increments
        AND CLI session is active
        WHEN User requests increment view via CLI
        THEN CLI displays no increments defined message
        AND CLI returns empty Increments collection
        """
        helper = BotTestHelper(tmp_path)
        story_graph = given_story_graph_with_no_increments(helper)
        
        # When
        result = when_user_requests_increment_view_via_cli(helper, story_graph)
        
        # Then
        then_cli_displays_no_increments_message(result, expected_message)
        then_increments_collection_is_empty(result)


class TestDisplayIncrementScopeView:
    
    @pytest.mark.parametrize("initial_view,toggle_action,resulting_view,toggle_label,tooltip", [
        ("Hierarchy", "click toggle", "Increment", "Hierarchy", "Display Hierarchy view"),
        ("Increment", "click toggle", "Hierarchy", "Increment", "Display Increment view"),
    ])
    def test_user_toggles_from_hierarchy_view_to_increment_view(
        self, tmp_path, initial_view, toggle_action, resulting_view, toggle_label, tooltip
    ):
        """
        SCENARIO: User toggles from Hierarchy view to Increment view
        
        GIVEN story graph contains increments with stories assigned
        AND Panel is open in Hierarchy view
        WHEN User clicks toggle button beside filter in filter box title
        THEN Panel switches from Hierarchy view to Increment view
        AND toggle button shows Hierarchy label with tooltip Display Hierarchy view
        AND Panel displays one column per increment with increment name at top
        """
        helper = BotTestHelper(tmp_path)
        panel_state = given_panel_open_in_view(helper, initial_view)
        
        # When
        new_state = when_user_clicks_view_toggle(panel_state)
        
        # Then
        then_panel_switches_to_view(new_state, resulting_view)
        then_toggle_button_shows_label_and_tooltip(new_state, toggle_label, tooltip)
    
    @pytest.mark.parametrize("increment_name,increment_priority,stories", [
        ("MVP Release", 1, ["Create Profile", "Authenticate User", "Submit Application"]),
        ("Enhancement Release", 2, ["Add Payment Method", "View History", "Export Report"]),
        ("Future Release", 3, ["Advanced Analytics", "Custom Dashboard"]),
    ])
    def test_increment_view_displays_stories_in_natural_order_per_column(
        self, tmp_path, increment_name, increment_priority, stories
    ):
        """
        SCENARIO: Increment view displays stories in natural order per column
        
        GIVEN story graph contains multiple increments with stories
        AND Panel is in Increment view
        WHEN Panel renders Increment view
        THEN Panel shows one column per increment
        AND each column has increment name at top
        AND stories display in natural order one after another
        AND view is read-only with no edit capability
        """
        # Given
        helper = BotTestHelper(tmp_path)
        panel_state = given_panel_in_increment_view_with_stories(
            helper, increment_name, increment_priority, stories
        )
        
        # When
        rendered = when_panel_renders_increment_view(panel_state)
        
        # Then
        then_panel_shows_column_for_increment(rendered, increment_name)
        then_column_has_increment_name_at_top(rendered, increment_name)
        then_stories_display_in_natural_order(rendered, stories)
        then_view_is_read_only(rendered)
    
    @pytest.mark.parametrize("increment_name,expected_message", [
        ("Backlog", "(no stories)"),
    ])
    def test_increment_view_displays_empty_column_for_increment_with_no_stories(
        self, tmp_path, increment_name, expected_message
    ):
        """
        SCENARIO: Increment view displays empty column for increment with no stories
        
        GIVEN story graph contains an increment with no stories
        AND Panel is in Increment view
        WHEN Panel renders Increment view
        THEN Panel shows column for empty increment
        AND column shows increment name at top
        AND column shows empty state message
        """
        # Given
        helper = BotTestHelper(tmp_path)
        panel_state = given_panel_in_increment_view_with_empty_increment(
            helper, increment_name
        )
        
        # When
        rendered = when_panel_renders_increment_view(panel_state)
        
        # Then
        then_panel_shows_column_for_increment(rendered, increment_name)
        then_column_shows_empty_state_message(rendered, expected_message)
    
    @pytest.mark.parametrize("hidden_control,reason", [
        ("Create Epic button", "Increment view is read-only"),
        ("Delete button", "Increment view is read-only"),
        ("Inline name editor", "Increment view is read-only"),
    ])
    def test_increment_view_is_read_only_with_no_edit_controls(
        self, tmp_path, hidden_control, reason
    ):
        """
        SCENARIO: Increment view is read-only with no edit controls
        
        GIVEN story graph contains increments with stories
        AND Panel is in Increment view
        WHEN Panel renders Increment view
        THEN Panel does not show create buttons
        AND Panel does not show delete buttons
        AND Panel does not show inline edit controls
        AND stories are display-only
        """
        # Given
        helper = BotTestHelper(tmp_path)
        panel_state = given_panel_in_increment_view(helper)
        
        # When
        rendered = when_panel_renders_increment_view(panel_state)
        
        # Then
        then_panel_does_not_show_control(rendered, hidden_control)


def given_story_graph_with_increment(helper, increment_name, increment_priority, stories):
    """Create story graph with an increment containing stories."""
    story_graph = {
        "increments": [
            {
                "name": increment_name,
                "priority": increment_priority,
                "stories": [
                    {"name": name, "sequential_order": order}
                    for name, order in stories
                ]
            }
        ],
        "epics": []
    }
    return story_graph


def given_story_graph_with_empty_increment(helper, increment_name, increment_priority):
    """Create story graph with an empty increment."""
    story_graph = {
        "increments": [
            {
                "name": increment_name,
                "priority": increment_priority,
                "stories": []
            }
        ],
        "epics": []
    }
    return story_graph


def given_story_graph_with_increment_referencing_story_nodes(helper):
    """Create story graph with increment referencing StoryNode objects."""
    story_graph = {
        "increments": [
            {
                "name": "Test Increment",
                "priority": 1,
                "stories": [
                    {
                        "name": "Test Story",
                        "test_class": "TestStory",
                        "sequential_order": 1.0
                    }
                ]
            }
        ],
        "epics": []
    }
    return story_graph


def given_story_graph_with_no_increments(helper):
    """Create story graph with no increments."""
    story_graph = {
        "increments": [],
        "epics": []
    }
    return story_graph


def given_panel_open_in_view(helper, view_name):
    """Create panel state open in specified view."""
    return {
        "current_view": view_name,
        "toggle_label": "Increment" if view_name == "Hierarchy" else "Hierarchy",
        "tooltip": f"Display {'Increment' if view_name == 'Hierarchy' else 'Hierarchy'} view"
    }


def given_panel_in_increment_view_with_stories(helper, increment_name, priority, stories):
    """Create panel state in increment view with stories."""
    return {
        "current_view": "Increment",
        "increments": [
            {
                "name": increment_name,
                "priority": priority,
                "stories": [{"name": s, "sequential_order": i+1} for i, s in enumerate(stories)]
            }
        ]
    }


def given_panel_in_increment_view_with_empty_increment(helper, increment_name):
    """Create panel state in increment view with empty increment."""
    return {
        "current_view": "Increment",
        "increments": [
            {
                "name": increment_name,
                "priority": 99,
                "stories": []
            }
        ]
    }


def given_panel_in_increment_view(helper):
    """Create panel state in increment view."""
    return {
        "current_view": "Increment",
        "increments": [
            {
                "name": "Test Increment",
                "priority": 1,
                "stories": [{"name": "Test Story", "sequential_order": 1}]
            }
        ]
    }


def when_user_requests_increment_view_via_cli(helper, story_graph):
    """Request increment view via CLI."""
    from synchronizers.story_io.increment_views import get_increments_view
    return get_increments_view(story_graph)


def when_user_enters_increment_view_command(helper, story_graph):
    """Enter increment view command via CLI."""
    from synchronizers.story_io.increment_views import format_increments_for_cli
    return format_increments_for_cli(story_graph)


def when_user_clicks_view_toggle(panel_state):
    """Click view toggle button."""
    from synchronizers.story_io.increment_views import toggle_view
    return toggle_view(panel_state)


def when_panel_renders_increment_view(panel_state):
    """Render increment view in panel."""
    from synchronizers.story_io.increment_views import render_increment_view
    return render_increment_view(panel_state)


def then_cli_returns_increments_object(increments):
    """Assert CLI returns Increments object."""
    assert increments is not None
    assert "increments" in increments


def then_increment_contains_name_priority_stories(increments, name, priority, story_count):
    """Assert Increment contains expected properties."""
    increment = next(
        (i for i in increments["increments"] if i["name"] == name),
        None
    )
    assert increment is not None, f"Increment '{name}' not found"
    assert increment["priority"] == priority
    assert len(increment.get("stories", [])) == story_count


def then_cli_displays_increment_with_stories_in_order(output, expected_output):
    """Assert CLI output matches expected format."""
    assert expected_output in output


def then_cli_displays_empty_increment_message(output, expected_output):
    """Assert CLI displays empty increment message."""
    assert expected_output in output


def then_story_objects_include_property(increments, property_name):
    """Assert Story objects include specified property."""
    for increment in increments.get("increments", []):
        for story in increment.get("stories", []):
            assert property_name in story or property_name == "name"


def then_cli_displays_no_increments_message(result, expected_message):
    """Assert CLI displays no increments message."""
    assert result.get("message") == expected_message


def then_increments_collection_is_empty(result):
    """Assert Increments collection is empty."""
    assert len(result.get("increments", [])) == 0


def then_panel_switches_to_view(state, expected_view):
    """Assert panel switches to expected view."""
    assert state["current_view"] == expected_view


def then_toggle_button_shows_label_and_tooltip(state, label, tooltip):
    """Assert toggle button shows correct label and tooltip."""
    assert state["toggle_label"] == label
    assert state["tooltip"] == tooltip


def then_panel_shows_column_for_increment(rendered, increment_name):
    """Assert panel shows column for increment."""
    column_names = [col["name"] for col in rendered.get("columns", [])]
    assert increment_name in column_names


def then_column_has_increment_name_at_top(rendered, increment_name):
    """Assert column has increment name at top."""
    column = next(
        (col for col in rendered["columns"] if col["name"] == increment_name),
        None
    )
    assert column is not None


def then_stories_display_in_natural_order(rendered, expected_stories):
    """Assert stories display in natural order."""
    for column in rendered.get("columns", []):
        story_names = [s["name"] for s in column.get("stories", [])]
        assert story_names == expected_stories


def then_view_is_read_only(rendered):
    """Assert view is read-only."""
    for column in rendered.get("columns", []):
        assert column.get("read_only", False) is True


def then_column_shows_empty_state_message(rendered, expected_message):
    """Assert column shows empty state message."""
    for column in rendered.get("columns", []):
        if not column.get("stories"):
            assert column.get("empty_message") == expected_message


def then_panel_does_not_show_control(rendered, control_name):
    """Assert panel does not show specified control."""
    assert rendered.get("controls_visible", True) is False
