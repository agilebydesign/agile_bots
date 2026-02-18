"""
Increment Test Helper for Edit Increments domain tests.
Provides Given/When/Then helpers for increment operations.
"""
import json
from pathlib import Path
from helpers.base_helper import BaseHelper


def story_graph_with_increments_mvp_phase2():
    """Story graph with increments MVP (priority 1) and Phase 2 (priority 2)."""
    return {
        "increments": [
            {"name": "MVP", "priority": 1, "stories": []},
            {"name": "Phase 2", "priority": 2, "stories": []},
        ],
        "epics": [],
    }


def story_graph_with_increment_named_mvp():
    """Story graph with single increment named MVP."""
    return {
        "increments": [{"name": "MVP", "priority": 1, "stories": []}],
        "epics": [],
    }


def story_graph_with_increment_and_story(increment_name, story_name):
    """Story graph with one increment containing one story."""
    return {
        "increments": [
            {
                "name": increment_name,
                "priority": 1,
                "stories": [{"name": story_name, "sequential_order": 1.0}],
            }
        ],
        "epics": [
            {
                "name": "Epic",
                "sequential_order": 1,
                "sub_epics": [
                    {
                        "name": "SubEpic",
                        "sequential_order": 1,
                        "sub_epics": [],
                        "story_groups": [
                            {
                                "type": "and",
                                "connector": None,
                                "stories": [
                                    {
                                        "name": story_name,
                                        "sequential_order": 1.0,
                                        "connector": None,
                                    }
                                ],
                            }
                        ],
                    }
                ],
                "story_groups": [],
            }
        ],
    }


def story_graph_with_increments_mvp_phase1():
    """Story graph with increments MVP and Phase 1 (for rename duplicate test)."""
    return {
        "increments": [
            {"name": "MVP", "priority": 1, "stories": []},
            {"name": "Phase 1", "priority": 2, "stories": []},
        ],
        "epics": [],
    }


def story_graph_with_two_stories_in_same_parent(story1_name, story2_name):
    """Story graph with two stories in same parent (for rename duplicate test)."""
    return {
        "increments": [
            {"name": "MVP", "priority": 1, "stories": [{"name": story1_name, "sequential_order": 1.0}]}
        ],
        "epics": [
            {
                "name": "Epic",
                "sequential_order": 1,
                "sub_epics": [
                    {
                        "name": "SubEpic",
                        "sequential_order": 1,
                        "sub_epics": [],
                        "story_groups": [
                            {
                                "type": "and",
                                "connector": None,
                                "stories": [
                                    {"name": story1_name, "sequential_order": 1.0, "connector": None},
                                    {"name": story2_name, "sequential_order": 2.0, "connector": None},
                                ],
                            }
                        ],
                    }
                ],
                "story_groups": [],
            }
        ],
    }


def story_graph_with_story_in_multiple_increments(story_name, increment_names):
    """Story graph with story in multiple increments (for cascade delete test)."""
    increments = []
    for i, inc_name in enumerate(increment_names, 1):
        increments.append({
            "name": inc_name,
            "priority": i,
            "stories": [{"name": story_name, "sequential_order": 1.0}],
        })
    return {
        "increments": increments,
        "epics": [
            {
                "name": "Epic",
                "sequential_order": 1,
                "sub_epics": [
                    {
                        "name": "SubEpic",
                        "sequential_order": 1,
                        "sub_epics": [],
                        "story_groups": [
                            {
                                "type": "and",
                                "connector": None,
                                "stories": [
                                    {
                                        "name": story_name,
                                        "sequential_order": 1.0,
                                        "connector": None,
                                    }
                                ],
                            }
                        ],
                    }
                ],
                "story_groups": [],
            }
        ],
    }


class IncrementTestHelper(BaseHelper):
    """Helper for Edit Increments domain tests."""

    @property
    def bot(self):
        return self.parent.bot

    def create_story_graph_with_increments(self, graph_data: dict) -> Path:
        """Create story graph file and load into bot. Uses tmp workspace."""
        return self.parent.story.create_story_graph(graph_data)

    def get_story_map(self):
        """Return bot's story map (reloads from file if needed)."""
        self.bot._story_graph = None
        return self.bot.story_map
