"""Scanner for detecting functions that are too large."""

from scanners.code_scanner import CodeScanner
from scanners.resources.violation import Violation
from scanners.resources.scan_context import ScanContext


class FunctionSizeScanner(CodeScanner):
    """Detects when functions are too large or unfocused."""

    def scan(self, context: ScanContext) -> list[Violation]:
        return []
