"""Scanner for scale_story_map_by_domain rule.

Flags sub-epics whose stories reference 3+ domain concepts across 8+ stories,
and stories with AC that cross domain boundaries. Soft thresholds -- scaling
warning, not hard error.
"""
from typing import List, Dict, Any, Set
from scanners.story_scanner import StoryScanner
from scanners.story_map import StoryNode, Epic, SubEpic, Story
from scanners.violation import Violation


class DomainOrientedStructureScanner(StoryScanner):

    def scan_story_node(self, node: StoryNode) -> List[Dict[str, Any]]:
        violations = []

        if isinstance(node, SubEpic):
            violation = self._check_sub_epic_domain_spread(node)
            if violation:
                violations.append(violation)

        if isinstance(node, Story):
            violation = self._check_story_ac_domain_crossing(node)
            if violation:
                violations.append(violation)

        return violations

    def _check_sub_epic_domain_spread(self, node: SubEpic) -> Dict[str, Any] | None:
        stories = [c for c in node.children if isinstance(c, Story)]
        if len(stories) < 8:
            return None

        domain_concepts = self._collect_domain_concepts_from_stories(stories)
        if len(domain_concepts) < 3:
            return None

        return Violation(
            rule=self.rule,
            violation_message=(
                f'Sub-epic "{node.name}" references {len(domain_concepts)} domain '
                f'concepts across {len(stories)} stories -- consider breaking out '
                f'by domain (scale_story_map_by_domain). '
                f'Concepts: {", ".join(sorted(domain_concepts)[:5])}'
            ),
            location=node.map_location(),
            severity='warning'
        ).to_dict()

    def _check_story_ac_domain_crossing(self, node: Story) -> Dict[str, Any] | None:
        ac_list = node.data.get('acceptance_criteria', [])
        if len(ac_list) < 2:
            return None

        all_concepts: Set[str] = set()
        for ac in ac_list:
            text = ac.get('name', '') or ac.get('text', '')
            concepts = self._extract_domain_keywords(text)
            all_concepts.update(concepts)

        if len(all_concepts) >= 3:
            return Violation(
                rule=self.rule,
                violation_message=(
                    f'Story "{node.name}" AC references {len(all_concepts)} '
                    f'distinct domain concepts -- consider splitting by domain. '
                    f'Concepts: {", ".join(sorted(all_concepts)[:5])}'
                ),
                location=node.map_location('acceptance_criteria'),
                severity='warning'
            ).to_dict()

        return None

    def _collect_domain_concepts_from_stories(self, stories: List[Story]) -> Set[str]:
        concepts: Set[str] = set()
        for story in stories:
            ac_list = story.data.get('acceptance_criteria', [])
            for ac in ac_list:
                text = ac.get('name', '') or ac.get('text', '')
                concepts.update(self._extract_domain_keywords(text))
        return concepts

    def _extract_domain_keywords(self, text: str) -> Set[str]:
        keywords = {'epic', 'sub-epic', 'story', 'actor', 'increment',
                     'acceptance criteria', 'scenario', 'layout', 'diagram'}
        found: Set[str] = set()
        text_lower = text.lower()
        for kw in keywords:
            if kw in text_lower:
                found.add(kw)
        return found
