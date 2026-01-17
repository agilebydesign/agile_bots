"""Configuration object for rule scanning operations."""
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ScanConfig:
    """Configuration for scanner execution.
    
    This consolidates scanner parameters to avoid excessive parameter passing.
    """
    
    # Core scan data
    story_graph: Dict[str, Any]
    files: Optional[Dict[str, List[Path]]] = None
    changed_files: Optional[Dict[str, List[Path]]] = None
    
    # Scanner behavior configuration
    skip_cross_file: bool = False
    max_cross_file_comparisons: int = 20
    
    # Callbacks and output
    on_file_scanned: Optional[Callable] = None
    status_writer: Optional[Any] = None
    
    # Derived properties (computed on demand)
    _test_files: Optional[List[Path]] = field(default=None, init=False, repr=False)
    _code_files: Optional[List[Path]] = field(default=None, init=False, repr=False)
    _all_test_files: Optional[List[Path]] = field(default=None, init=False, repr=False)
    _all_code_files: Optional[List[Path]] = field(default=None, init=False, repr=False)
    
    def __post_init__(self):
        """Ensure files dict is initialized."""
        if self.files is None:
            self.files = {}
        if self.changed_files is None:
            self.changed_files = {}
    
    @property
    def test_files(self) -> List[Path]:
        """Get test files from changed_files or files."""
        if self._test_files is None:
            files_to_scan = self.changed_files if self.changed_files else self.files
            self._test_files = files_to_scan.get('test', [])
        return self._test_files
    
    @property
    def code_files(self) -> List[Path]:
        """Get code files from changed_files or files."""
        if self._code_files is None:
            files_to_scan = self.changed_files if self.changed_files else self.files
            self._code_files = files_to_scan.get('src', [])
        return self._code_files
    
    @property
    def all_test_files(self) -> List[Path]:
        """Get all test files (for cross-file scanning)."""
        if self._all_test_files is None:
            self._all_test_files = self.files.get('test', [])
        return self._all_test_files
    
    @property
    def all_code_files(self) -> List[Path]:
        """Get all code files (for cross-file scanning)."""
        if self._all_code_files is None:
            self._all_code_files = self.files.get('src', [])
        return self._all_code_files
