"""
Base class for scenario scanners that need domain concept access.

Extends DomainScannerBase with scenario-specific utilities:
- get_all_steps(): returns background + scenario steps combined
- get_steps_text(): returns all steps as single text string
- Cross-epic domain concept collection (User/Entitlement from other epics)

This base class should be used by scanners that need to:
1. Analyze scenario steps INCLUDING background
2. Validate against domain concepts from the full story graph
"""

from typing import List, Dict, Any, Set, TYPE_CHECKING
from scanners.domain_scanner_base import DomainScannerBase
from scanners.story_map import Scenario

if TYPE_CHECKING:
    from actions.rules.rule import Rule


class ScenarioScannerBase(DomainScannerBase):
    """
    Base class for domain-aware scenario scanners.
    
    Provides utilities for analyzing scenarios with full context:
    - Background + steps combined
    - Domain concepts from all epics (not just the scoped one)
    """
    
    def __init__(self, rule: 'Rule'):
        super().__init__(rule)
    
    def get_all_steps(self, scenario: Scenario) -> List[str]:
        """
        Get all steps for a scenario including background.
        
        Returns background steps + scenario steps combined.
        This ensures domain concepts mentioned in background are considered.
        """
        return scenario.all_steps
    
    def get_steps_text(self, scenario: Scenario) -> str:
        """
        Get all steps as a single text string for analysis.
        
        Combines background + scenario steps into one searchable string.
        """
        return ' '.join(self.get_all_steps(scenario))
    
    def _get_domain_concept_names_lower(self, domain_concepts: List[Dict[str, Any]]) -> Set[str]:
        """Get lowercase names of all domain concepts."""
        return {c.get('name', '').lower() for c in domain_concepts if c.get('name')}
    
    def _similar(self, a: str, b: str) -> bool:
        """Check if two strings are similar (for suggestion matching)."""
        a_lower = a.lower()
        b_lower = b.lower()
        return (
            a_lower == b_lower or
            a_lower in b_lower or
            b_lower in a_lower or
            self._levenshtein_ratio(a_lower, b_lower) > 0.7
        )
    
    def _levenshtein_ratio(self, s1: str, s2: str) -> float:
        """Calculate Levenshtein similarity ratio between two strings."""
        if not s1 or not s2:
            return 0.0
        
        if len(s1) > len(s2):
            s1, s2 = s2, s1
        
        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            new_distances = [i2 + 1]
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    new_distances.append(distances[i1])
                else:
                    new_distances.append(1 + min((distances[i1], distances[i1 + 1], new_distances[-1])))
            distances = new_distances
        
        max_len = max(len(s1), len(s2))
        return 1 - (distances[-1] / max_len) if max_len > 0 else 1.0
    
    def _find_domain_concepts_in_columns(
        self,
        columns: List[str],
        domain_concepts: List[Dict[str, Any]],
        fuzzy: bool = False
    ) -> Set[str]:
        """
        Find which domain concepts are represented in example columns.
        
        Args:
            columns: List of column names
            domain_concepts: List of domain concept dicts
            fuzzy: If True, use fuzzy matching for concept names
        """
        found = set()
        
        concept_names = [c.get('name', '').lower() for c in domain_concepts if c.get('name')]
        
        for column in columns:
            column_lower = column.lower()
            column_parts = column_lower.split('_')
            
            for concept_name in concept_names:
                # Check if concept name is in column
                if concept_name in column_lower:
                    found.add(concept_name)
                    continue
                    
                # Check column parts
                for part in column_parts:
                    if part == concept_name or part == concept_name + 's':
                        found.add(concept_name)
                        break
                        
                # Fuzzy matching if enabled
                if fuzzy:
                    for part in column_parts:
                        if self._similar(part, concept_name):
                            found.add(concept_name)
                            break
        
        return found
