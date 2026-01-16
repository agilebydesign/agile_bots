"""Scanner module for validation rule scanners.

All scanners are lazy-loaded via ScannerRegistry using importlib.
Only base classes and commonly-used types are eagerly imported here.
"""

# Base classes - always needed
from .scanner import Scanner
from .violation import Violation

# Story map data structures - commonly used across many modules
from .story_map import (
    StoryMap, StoryNode, Epic, SubEpic, StoryGroup, Story, Scenario, ScenarioOutline
)

# Scanner base types - used by rule.py for type checking
from .code_scanner import CodeScanner
from .test_scanner import TestScanner

__all__ = [
    'Scanner', 
    'Violation',
    'CodeScanner',
    'TestScanner',
    'StoryMap', 
    'StoryNode', 
    'Epic', 
    'SubEpic', 
    'StoryGroup', 
    'Story', 
    'Scenario', 
    'ScenarioOutline',
]

# All other scanners are lazy-loaded by ScannerRegistry via importlib.import_module()
# This eliminates ~1 second of startup time from NLTK/scipy/sklearn imports

