"""
Scenario Language Scanner

Rule: scenario_language_matches_domain

This scanner validates that scenario step text (Given/When/Then) uses
terminology from the domain model rather than UI or technical terms.

Uses ScenarioScannerBase for cross-epic domain concept collection.

Violations are reported when:
- Scenario steps reference entities not defined in domain concepts
- Scenario uses UI-specific terms instead of domain language
"""

from typing import List, Dict, Any, TYPE_CHECKING
from scanners.scenarios.scenario_scanner_base import ScenarioScannerBase
from scanners.story_map import StoryNode, Story, Scenario
from scanners.violation import Violation

if TYPE_CHECKING:
    from actions.rules.rule import Rule


class ScenarioLanguageScanner(ScenarioScannerBase):
    """
    Scanner that validates scenario step language matches domain concepts.
    
    Checks that the language used in Given/When/Then steps references
    domain concepts rather than UI elements or technical implementation.
    
    Uses get_all_steps() to include background in analysis.
    """
    
    def __init__(self, rule: 'Rule'):
        super().__init__(rule)

    def scan_story_node(self, node: StoryNode) -> List[Dict[str, Any]]:
        """Scan a story node for scenario language violations."""
        violations = []
        
        if not isinstance(node, Story):
            return violations
        
        # Collect domain concepts for this story's context (from ALL epics)
        domain_concepts = self._collect_domain_concepts_for_story(node)
        
        if not domain_concepts:
            # No domain concepts defined - skip validation
            return violations
        
        # Build lookup structures
        concept_names = self._extract_concept_names(domain_concepts)
        concept_attributes = self._extract_concept_attributes(domain_concepts)
        all_domain_terms = concept_names | concept_attributes
        
        # Scan each scenario
        for scenario in node.scenarios:
            step_violations = self._check_scenario_steps(
                scenario, concept_names, all_domain_terms, node
            )
            violations.extend(step_violations)
        
        return violations
    
    def _check_scenario_steps(
        self,
        scenario: Scenario,
        concept_names: set,
        all_domain_terms: set,
        story: Story
    ) -> List[Dict[str, Any]]:
        """
        Check if scenario steps reference domain concepts properly.
        
        Extracts entities mentioned in the scenario and validates they
        exist in the domain model.
        
        Uses get_all_steps() to include background steps in analysis.
        """
        violations = []
        
        # Extract entities mentioned in ALL scenario steps (including background)
        steps_text = self.get_steps_text(scenario)
        mentioned_entities = self._extract_entities_from_text(steps_text)
        
        # Check for non-domain entities
        non_domain_entities = []
        for entity in mentioned_entities:
            entity_lower = entity.lower()
            if not self._matches_domain_term(entity_lower, concept_names, all_domain_terms):
                non_domain_entities.append(entity)
        
        if non_domain_entities:
            # Only report top 5 to avoid overwhelming messages
            sample_entities = non_domain_entities[:5]
            sample_concepts = sorted(concept_names)[:8]
            
            violation = Violation(
                rule=self.rule,
                violation_message=(
                    f'Scenario uses terms not in domain model: {", ".join(sample_entities)}. '
                    f'Domain concepts include: {", ".join(sample_concepts)}'
                ),
                location=scenario.map_location('steps'),
                severity='warning'
            ).to_dict()
            violations.append(violation)
        
        return violations
