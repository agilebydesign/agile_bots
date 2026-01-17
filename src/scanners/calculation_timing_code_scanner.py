"""Scanner for detecting exposed calculation timing in code."""

from scanners.code_scanner import CodeScanner
from scanners.resources.violation import Violation
from scanners.resources.scan_context import ScanContext


class CalculationTimingCodeScanner(CodeScanner):
    """
    Detects when code exposes calculation/computation timing through method names.
    Properties should hide when calculations occur (on-demand, cached, pre-computed).
    """

    def scan(self, context: ScanContext) -> list[Violation]:
        """Scan for exposed calculation timing patterns."""
        # TODO: Implement detection logic
        # Look for methods like calculate_*, compute_*, get_cached_*, get_precomputed_*
        # that should be properties instead
        return []
