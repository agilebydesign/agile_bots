
from typing import List, Dict, Any, Optional
from scanners.domain_scanner import DomainScanner
from scanners.domain_concept_node import DomainConceptNode
from scanners.violation import Violation
from .vocabulary_helper import VocabularyHelper

class ResourceOrientedDesignScanner(DomainScanner):
    """Domain resource nouns that are standard terms, not agent nouns (e.g. Voucher = coupon, not 'one who vouches')."""
    DOMAIN_RESOURCE_EXCEPTIONS = frozenset({'voucher'})

    def scan_domain_concept(self, node: DomainConceptNode) -> List[Dict[str, Any]]:
        violations = []

        if node.name.lower() in self.DOMAIN_RESOURCE_EXCEPTIONS:
            return violations

        is_agent, base_verb, suffix = VocabularyHelper.is_agent_noun(node.name)

        if is_agent:
            suggested_name = node.name[:-len(suffix)]
            if not suggested_name:
                suggested_name = "[ResourceName]"
            
            violations.append(
                Violation(
                    rule=self.rule,
                    violation_message=f'Domain concept "{node.name}" is an agent noun (doer of action) derived from verb "{base_verb}". Name concepts after resources (what they ARE), not actions (what they DO). Consider: "{suggested_name}" as the resource.',
                    location=node.map_location('name'),
                    line_number=None,
                    severity='error'
                ).to_dict()
            )
        
        return violations

