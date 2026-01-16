"""Scanner for validating resource-oriented design in domain models."""

from typing import List, Dict, Any, Optional
from .domain_scanner import DomainScanner
from .domain_concept_node import DomainConceptNode
from .violation import Violation
from .vocabulary_helper import VocabularyHelper


class ResourceOrientedDesignScanner(DomainScanner):
    """
    Validates that domain concepts are named after resources (what they ARE)
    rather than actions (what they DO).
    
    Uses NLTK to detect agent nouns (Manager, Loader, Handler, etc.)
    which are nouns derived from verbs that describe doers of actions.
    """
    
    def scan_domain_concept(self, node: DomainConceptNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        # Check if concept name is an agent noun (e.g., Manager, Loader, Handler)
        is_agent, base_verb, suffix = VocabularyHelper.is_agent_noun(node.name)
        
        if is_agent:
            suggested_name = node.name[:-len(suffix)]
            if not suggested_name:
                suggested_name = "[ResourceName]"
            
            violations.append(
                Violation(
                    rule=rule_obj,
                    violation_message=f'Domain concept "{node.name}" is an agent noun (doer of action) derived from verb "{base_verb}". Name concepts after resources (what they ARE), not actions (what they DO). Consider: "{suggested_name}" as the resource.',
                    location=node.map_location('name'),
                    line_number=None,
                    severity='error'
                ).to_dict()
            )
        
        return violations





        return violations





        return violations




