"""Scanner for background_vs_scenario_setup rule.

Checks:
1. Repeated Givens: When 3+ scenarios share the same Given step, it should be in Background
2. Missing examples: Given steps with {Concept} references must have corresponding example tables
3. Duplicate setup: Steps that repeat Background content
"""
import re
from typing import List, Dict, Any, Set
from scanners.story_scanner import StoryScanner
from scanners.story_map import StoryMap, StoryNode, Story, StoryGroup
from scanners.story_map import Scenario
from scanners.violation import Violation


def _parse_steps(steps: Any) -> List[str]:
    """Parse steps from string or list into list of step texts."""
    if steps is None:
        return []
    if isinstance(steps, list):
        result = []
        for s in steps:
            if isinstance(s, dict):
                result.append(s.get('text', str(s)))
            else:
                result.append(str(s).strip())
        return [t for t in result if t]
    if isinstance(steps, str):
        return [t.strip() for t in steps.split('\n') if t.strip()]
    return []


def _extract_given_steps(steps: List[str]) -> List[str]:
    """Extract Given/And steps (setup) from step list."""
    given_steps = []
    for step in steps:
        step_lower = step.strip().lower()
        if step_lower.startswith('given ') or step_lower.startswith('and '):
            given_steps.append(step.strip())
    return given_steps


def _extract_concepts_from_step(step: str) -> Set[str]:
    """Extract {Concept} and {Concept.property} references from a step."""
    # Match {Concept} or {Concept.property}
    pattern = r'\{([A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)?)\}'
    matches = re.findall(pattern, step)
    # Normalize to base concept (strip .property)
    concepts = set()
    for m in matches:
        base = m.split('.')[0] if '.' in m else m
        concepts.add(base)
    return concepts


def _get_example_table_names(scenario_data: Dict[str, Any]) -> Set[str]:
    """Get concept names from example tables (name or columns)."""
    names = set()
    examples = scenario_data.get('examples', [])
    if not examples:
        return names
    tables = examples if isinstance(examples, list) else [examples]
    for tbl in tables:
        if isinstance(tbl, dict):
            name = tbl.get('name', '')
            if name:
                # "CustomerProfile" or "CustomerProfile (at profile entry step)"
                base = name.split('(')[0].strip()
                names.add(base)
            # Also check columns for concept prefix
            cols = tbl.get('columns', tbl.get('headers', []))
            for c in cols or []:
                if isinstance(c, str) and '_' in c:
                    prefix = c.split('_')[0]
                    if prefix and prefix[0].isupper():
                        names.add(prefix)
    return names


def _story_has_examples(story_data: Dict[str, Any]) -> bool:
    """Check if story has examples at story level (e.g. in background)."""
    bg = story_data.get('background', [])
    if isinstance(bg, list):
        for item in bg:
            if isinstance(item, dict) and item.get('examples'):
                return True
    return False


class BackgroundCommonSetupScanner(StoryScanner):
    """Validates background vs scenario setup rules."""

    def scan_story_node(self, node: StoryNode) -> List[Dict[str, Any]]:
        """Scan a single story for background/common setup violations."""
        violations = []
        if not isinstance(node, Story):
            return violations

        story_data = node.data
        story_name = node.name or 'Unnamed story'
        scenarios_data = story_data.get('scenarios', [])
        scenario_outlines = story_data.get('scenario_outlines', [])
        all_scenarios = list(scenarios_data) + list(scenario_outlines)

        if len(all_scenarios) < 2:
            return violations

        # Story-level background (if any)
        story_background = story_data.get('background', [])
        story_bg_steps = _parse_steps(
            story_background if isinstance(story_background, list)
            else [story_background] if story_background else []
        )
        story_bg_givens = set(s.strip().lower() for s in _extract_given_steps(story_bg_steps))

        # Collect Given steps across all scenarios
        given_to_scenarios: Dict[str, List[str]] = {}
        for sc_data in all_scenarios:
            sc_name = sc_data.get('name', '')
            sc_background = sc_data.get('background', [])
            sc_steps = _parse_steps(sc_data.get('steps', []))
            sc_bg_steps = _parse_steps(sc_background)
            all_givens = _extract_given_steps(sc_bg_steps + sc_steps)
            for g in all_givens:
                key = g.strip().lower()
                if key not in given_to_scenarios:
                    given_to_scenarios[key] = []
                given_to_scenarios[key].append(sc_name or '(unnamed)')

        # Check 1: Given repeated in 3+ scenarios but not in Background
        for given_text, scenario_names in given_to_scenarios.items():
            if len(scenario_names) >= 3:
                in_story_bg = given_text in story_bg_givens
                in_any_scenario_bg = False
                for sc_data in all_scenarios:
                    sc_bg = sc_data.get('background', [])
                    sc_bg_parsed = _parse_steps(sc_bg)
                    for s in _extract_given_steps(sc_bg_parsed):
                        if s.strip().lower() == given_text:
                            in_any_scenario_bg = True
                            break
                if not in_story_bg and not in_any_scenario_bg:
                    violations.append(
                        Violation(
                            rule=self.rule,
                            violation_message=(
                                f'Story "{story_name}": Given step repeated in {len(scenario_names)} scenarios '
                                f'but not in Background. Move to Background: "{given_text[:80]}{"..." if len(given_text) > 80 else ""}"'
                            ),
                            location=story_name,
                            severity='error'
                        ).to_dict()
                    )

        # Check 2: {Concept} in steps without corresponding examples
        for sc_idx, sc_data in enumerate(all_scenarios):
            sc_name = sc_data.get('name', '') or f'scenario[{sc_idx}]'
            sc_steps = _parse_steps(sc_data.get('steps', []))
            sc_bg = sc_data.get('background', [])
            sc_bg_steps = _parse_steps(sc_bg)
            all_steps = sc_bg_steps + sc_steps
            example_concepts = _get_example_table_names(sc_data)
            story_level_examples = _get_example_table_names(story_data)

            for step in all_steps:
                concepts = _extract_concepts_from_step(step)
                for concept in concepts:
                    if concept not in example_concepts and concept not in story_level_examples:
                        violations.append(
                            Violation(
                                rule=self.rule,
                                violation_message=(
                                    f'Story "{story_name}", scenario "{sc_name}": '
                                    f'Step references {{{concept}}} but no example table for {concept}. '
                                    f'Add examples for all {{Concept}} references.'
                                ),
                                location=f'{story_name} / {sc_name}',
                                severity='error'
                            ).to_dict()
                        )

        # Check 3: Hardcoded Given without {Concept} (likely needs examples)
        for sc_data in all_scenarios:
            sc_name = sc_data.get('name', '')
            sc_steps = _parse_steps(sc_data.get('steps', []))
            for step in _extract_given_steps(sc_steps):
                concepts = _extract_concepts_from_step(step)
                # If Given describes state (e.g. "Customer is in onboarding flow") with no {Concept}
                step_lower = step.lower()
                if not concepts and (' is ' in step or ' has ' in step or ' in ' in step):
                    # Check it's not trivial - describes entity state without parameterization
                    if len(step) > 25 and ('customer' in step_lower or 'user' in step_lower):
                        violations.append(
                            Violation(
                                rule=self.rule,
                                violation_message=(
                                    f'Story "{story_name}", scenario "{sc_name}": '
                                    f'Given step has no {{Concept}} and no examples: "{step[:60]}...". '
                                    f'Use {{Concept}} notation and add example table.'
                                ),
                                location=f'{story_name} / {sc_name}',
                                severity='warning'
                            ).to_dict()
                        )

        return violations
