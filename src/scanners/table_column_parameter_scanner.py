"""
Table Column Parameter Scanner

Rule: map_table_columns_to_scenario_parameters

Validates bidirectional mapping between example tables and scenario {Concept} references:
1. Every example table must be referenced as {Concept} in Background/Steps  
2. Every {Concept} in Background/Steps must have a corresponding example table
3. Use {Concept.property} when a specific attribute is important
"""

import re
from typing import List, Dict, Any, Set, TYPE_CHECKING
from scanners.scenarios.scenario_scanner_base import ScenarioScannerBase
from scanners.story_map import StoryNode, Story, Scenario
from scanners.violation import Violation

if TYPE_CHECKING:
    from actions.rules.rule import Rule


class TableColumnParameterScanner(ScenarioScannerBase):
    """
    Scanner that validates {Concept} references match example tables.
    
    Ensures:
    - Every {Concept} in steps/background has a matching example table
    - Every example table is referenced as {Concept} in steps
    - Use {Concept.property} for specific attribute references
    """
    
    def __init__(self, rule: 'Rule'):
        super().__init__(rule)

    def scan_story_node(self, node: StoryNode) -> List[Dict[str, Any]]:
        """Scan a story node for table/parameter mapping violations."""
        violations = []
        
        if not isinstance(node, Story):
            return violations
        
        # Scan each scenario
        for scenario in node.scenarios:
            violations.extend(self._check_concept_table_mapping(scenario, node))
        
        return violations
    
    def _check_concept_table_mapping(
        self, 
        scenario: Scenario, 
        story: Story
    ) -> List[Dict[str, Any]]:
        """Check bidirectional mapping between {Concept} refs and example tables."""
        violations = []
        
        # Get all table names from examples
        table_names = self._get_all_table_names(scenario)
        
        # Get all {Concept} references from background and steps
        # background is on Scenario, not Story
        background_concepts = self._extract_concept_refs(getattr(scenario, 'background', []) or [])
        step_concepts = self._extract_concept_refs(scenario.steps)
        all_concepts = background_concepts.union(step_concepts)
        
        # Get base concept names (without .property)
        all_concept_bases = {self._get_concept_base(c) for c in all_concepts}
        
        # CRITICAL CHECK: If concepts exist but NO tables at all, that's a major violation
        if all_concept_bases and not table_names:
            location = f"{story.map_location()}.scenarios[{scenario.name}].examples"
            missing_concepts = sorted(all_concept_bases)
            violations.append(Violation(
                rule=self.rule,
                violation_message=f'Missing example tables for ALL {len(missing_concepts)} concepts: {missing_concepts}. Every {{Concept}} reference requires a corresponding example table.',
                location=location,
                severity='error'
            ).to_dict())
            return violations
        
        # Normalize for comparison
        table_names_lower = {t.lower() for t in table_names}
        concepts_base = {self._get_concept_base(c).lower() for c in all_concepts}
        
        # Check 1: Tables without matching {Concept} references
        unmapped_tables = []
        for table in table_names:
            if table.lower() not in concepts_base:
                unmapped_tables.append(table)
        
        if unmapped_tables:
            location = f"{story.map_location()}.scenarios[{scenario.name}].examples"
            violations.append(Violation(
                rule=self.rule,
                violation_message=f'Example tables not referenced in steps: {unmapped_tables}. Add {{Concept}} reference like: Given {{{unmapped_tables[0]}}} is...',
                location=location,
                severity='error'
            ).to_dict())
        
        # Check 2: {Concept} refs without matching tables - this is an ERROR, not warning
        unmapped_concepts = []
        for concept in all_concepts:
            concept_base = self._get_concept_base(concept).lower()
            if concept_base not in table_names_lower:
                unmapped_concepts.append(concept)
        
        if unmapped_concepts:
            # Dedupe to base concept names
            unmapped_bases = sorted(set(self._get_concept_base(c) for c in unmapped_concepts))
            location = f"{story.map_location()}.scenarios[{scenario.name}].steps"
            violations.append(Violation(
                rule=self.rule,
                violation_message=f'Missing example tables for {len(unmapped_bases)} concepts: {unmapped_bases}. Every {{Concept}} reference requires a corresponding example table with concrete data.',
                location=location,
                severity='error'
            ).to_dict())
        
        return violations
    
    def _get_all_table_names(self, scenario: Scenario) -> Set[str]:
        """Get all table names from example tables."""
        names = set()
        for example in scenario.examples or []:
            name = example.get('name', '')
            if name:
                names.add(name)
        return names
    
    def _extract_concept_refs(self, steps: List[str]) -> Set[str]:
        """Extract {Concept} and {Concept.property} references from step text."""
        concepts = set()
        concept_pattern = re.compile(r'\{([^}]+)\}')
        for step in steps:
            matches = concept_pattern.findall(step)
            concepts.update(matches)
        return concepts
    
    def _get_concept_base(self, concept_ref: str) -> str:
        """Get base concept name from {Concept} or {Concept.property}."""
        # Split on dot to get base concept
        if '.' in concept_ref:
            return concept_ref.split('.')[0]
        return concept_ref
