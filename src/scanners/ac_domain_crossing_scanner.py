"""Scanner for keep_acceptance_criteria_consistent_across_connected_domains rule.

Flags individual AC that describe behaviors of 2+ distinct domain concepts
by detecting behavioral verbs paired with different domain concept names.
"""
from typing import List, Dict, Any, Set
from scanners.story_scanner import StoryScanner
from scanners.story_map import StoryNode, Story
from scanners.violation import Violation


class ACDomainCrossingScanner(StoryScanner):

    BEHAVIORAL_VERBS = {
        'renders', 'extracts', 'validates', 'assigns', 'generates',
        'updates', 'applies', 'detects', 'reports', 'synchronizes',
        'routes', 'processes', 'creates', 'removes', 'moves',
    }

    DOMAIN_KEYWORDS = {
        'epic': 'epic', 'sub-epic': 'sub-epic', 'sub_epic': 'sub-epic',
        'story': 'story', 'stories': 'story',
        'actor': 'actor', 'actors': 'actor',
        'increment': 'increment', 'lane': 'increment',
        'acceptance criteria': 'acceptance_criteria',
        'ac box': 'acceptance_criteria', 'ac cell': 'acceptance_criteria',
    }

    def scan_story_node(self, node: StoryNode) -> List[Dict[str, Any]]:
        violations = []

        if not isinstance(node, Story):
            return violations

        ac_list = node.data.get('acceptance_criteria', [])
        for ac_idx, ac in enumerate(ac_list):
            text = ac.get('name', '') or ac.get('text', '')
            violation = self._check_ac_crosses_domains(node, text, ac_idx)
            if violation:
                violations.append(violation)

        return violations

    def _check_ac_crosses_domains(self, story: Story, ac_text: str,
                                   ac_idx: int) -> Dict[str, Any] | None:
        text_lower = ac_text.lower()
        domains_with_verbs: Set[str] = set()

        for keyword, domain in self.DOMAIN_KEYWORDS.items():
            if keyword in text_lower:
                words = text_lower.split()
                has_verb = any(w in self.BEHAVIORAL_VERBS for w in words)
                if has_verb:
                    domains_with_verbs.add(domain)

        if len(domains_with_verbs) >= 2:
            snippet = ac_text[:80] + '...' if len(ac_text) > 80 else ac_text
            return Violation(
                rule=self.rule,
                violation_message=(
                    f'AC in story "{story.name}" mixes behaviors of '
                    f'{", ".join(sorted(domains_with_verbs))} -- '
                    f'signal to split story by domain. '
                    f'AC: "{snippet}"'
                ),
                location=story.map_location('acceptance_criteria'),
                severity='warning'
            ).to_dict()

        return None
