"""Scanner for validating avoidance of technical abstractions in domain models."""

from typing import List, Dict, Any, Optional
import re
from .domain_scanner import DomainScanner
from .domain_concept_node import DomainConceptNode
from .violation import Violation
from .vocabulary_helper import VocabularyHelper


class TechnicalAbstractionScanner(DomainScanner):
    """
    Validates that domain concepts avoid exposing technical abstractions.
    Uses NLTK to detect agent nouns like Saver, Loader, Storage.
    """
    
    # Technical file operation patterns (regex-based, not derivable from NLTK)
    TECHNICAL_FILE_PATTERNS = [
        r'\bsave\s+.*file\b',
        r'\bload\s+.*file\b',
        r'\bstore\s+.*file\b',
    ]
    
    def scan_domain_concept(self, node: DomainConceptNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        # Check if concept name is an agent noun related to technical operations
        is_agent, base_verb, suffix = VocabularyHelper.is_agent_noun(node.name)
        if is_agent and base_verb in ['save', 'load', 'store']:
            violations.append(
                Violation(
                    rule=rule_obj,
                    violation_message=f'Domain concept "{node.name}" separates technical abstraction (derived from verb "{base_verb}"). Keep technical details (saving, loading) as part of domain concepts instead.',
                    location=node.map_location('name'),
                    line_number=None,
                    severity='warning'
                ).to_dict()
            )
        
        # Check responsibilities for technical file operation patterns
        for i, responsibility_data in enumerate(node.responsibilities):
            responsibility_name = responsibility_data.get('name', '')
            resp_lower = responsibility_name.lower()
            for pattern in self.TECHNICAL_FILE_PATTERNS:
                if re.search(pattern, resp_lower):
                    violations.append(
                        Violation(
                            rule=rule_obj,
                            violation_message=f'Responsibility "{responsibility_name}" exposes technical abstraction. Stay at domain level (e.g., "Saves portfolio" not "Saves portfolio to file").',
                            location=node.map_location(f'responsibilities[{i}].name'),
                            line_number=None,
                            severity='warning'
                        ).to_dict()
                    )
                    break
        
        return violations




