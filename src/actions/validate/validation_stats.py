from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class ValidationStats:
    total_rules: int
    total_with_scanners: int
    executed_count: int
    load_failed_count: int
    execution_failed_count: int
    no_scanner_count: int
    total_violations: int
    rules_clean: int
    rules_with_warnings: int
    rules_with_errors: int
    executed_rules: List[Dict[str, Any]]

    @property
    def has_failures(self) -> bool:
        return self.execution_failed_count > 0 or self.load_failed_count > 0

    @property
    def has_violations(self) -> bool:
        return self.total_violations > 0

