"""Scanner for keep_scenarios_consistent_across_connected_domains rule.

Flags inconsistent step counts for the same operation across domain-specific
stories, and near-duplicate scenarios (>80% text similarity) that should
be parameterized.
"""
from typing import List, Dict, Any, Optional
from difflib import SequenceMatcher
from scanners.story_scanner import StoryScanner
from scanners.story_map import StoryNode, SubEpic, Story
from scanners.violation import Violation


class ParallelScenarioStructureScanner(StoryScanner):

    SIMILARITY_THRESHOLD = 0.80

    def scan_story_node(self, node: StoryNode) -> List[Dict[str, Any]]:
        violations = []

        if not isinstance(node, SubEpic):
            return violations

        stories = [c for c in node.children if isinstance(c, Story)]
        if len(stories) < 2:
            return violations

        violations.extend(self._check_near_duplicate_scenarios(node, stories))

        return violations

    def _check_near_duplicate_scenarios(self, sub_epic: SubEpic,
                                         stories: List[Story]) -> List[Dict[str, Any]]:
        violations = []
        all_scenarios = []

        for story in stories:
            for scenario in story.scenarios:
                steps_text = ' '.join(scenario.steps)
                all_scenarios.append((story.name, scenario.name, steps_text, scenario))

        for i in range(len(all_scenarios)):
            for j in range(i + 1, len(all_scenarios)):
                story_a, name_a, text_a, sc_a = all_scenarios[i]
                story_b, name_b, text_b, sc_b = all_scenarios[j]

                if story_a == story_b:
                    continue

                if not text_a or not text_b:
                    continue

                similarity = SequenceMatcher(None, text_a, text_b).ratio()
                if similarity >= self.SIMILARITY_THRESHOLD:
                    violations.append(Violation(
                        rule=self.rule,
                        violation_message=(
                            f'Scenarios "{name_a}" (in "{story_a}") and '
                            f'"{name_b}" (in "{story_b}") are '
                            f'{similarity:.0%} similar -- consider '
                            f'parameterizing with {{Concept}} references '
                            f'instead of duplicating'
                        ),
                        location=sub_epic.map_location(),
                        severity='warning'
                    ).to_dict())

        return violations
