
from typing import List, Dict, Any
import re
from scanners.domain_scanner import DomainScanner
from scanners.domain_concept_node import DomainConceptNode
from scanners.violation import Violation


class AtomicResponsibilityScanner(DomainScanner):
    """Scanner for Favor Atomic Responsibilities rule.
    Detects packed conditions (on X, Y, or Z) and outcome phrasing (Prevents, Issues).
    """

    # Packed conditions: "on X, Y, or Z" or ", or " patterns
    PACKED_ON_PATTERN = re.compile(r'\s+on\s+.+,\s*.+', re.IGNORECASE)
    PACKED_OR_PATTERN = re.compile(r',\s+or\s+', re.IGNORECASE)

    # Outcome phrasing (describe what it prevents, not what it does)
    OUTCOME_PATTERNS = [
        re.compile(r'^Prevents\s+', re.IGNORECASE),
        re.compile(r'^Issues\s+', re.IGNORECASE),
    ]

    def scan_domain_concept(self, node: DomainConceptNode) -> List[Dict[str, Any]]:
        violations = []

        for i, resp_data in enumerate(node.responsibilities):
            name = resp_data.get('name', '')
            if not name:
                continue

            # Packed conditions
            if self.PACKED_ON_PATTERN.search(name) or self.PACKED_OR_PATTERN.search(name):
                violations.append(
                    Violation(
                        rule=self.rule,
                        violation_message=(
                            f'Responsibility "{name}" packs multiple conditions. '
                            'Split into separate atomic responsibilities (e.g., Acquires, expires, Releases).'
                        ),
                        location=node.map_location(f'responsibilities[{i}].name'),
                        line_number=None,
                        severity='warning',
                    ).to_dict()
                )

            # Outcome phrasing
            for pattern in self.OUTCOME_PATTERNS:
                if pattern.search(name):
                    violations.append(
                        Violation(
                            rule=self.rule,
                            violation_message=(
                                f'Responsibility "{name}" uses outcome phrasing (Prevents/Issues). '
                                'Describe behavior instead (e.g., Acquires lock, Releases lock).'
                            ),
                            location=node.map_location(f'responsibilities[{i}].name'),
                            line_number=None,
                            severity='warning',
                        ).to_dict()
                    )
                    break

        return violations
