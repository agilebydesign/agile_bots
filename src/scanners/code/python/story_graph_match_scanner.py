"""Scanner for validating test structure matches story graph exactly."""

from typing import List, Dict, Any, Optional, TYPE_CHECKING
from pathlib import Path
import ast
import logging
from scanners.code.python.test_scanner import TestScanner
from scanners.violation import Violation

if TYPE_CHECKING:
    from scanners.resources.scan_context import FileScanContext
from scanners.resources.ast_elements import Classes

logger = logging.getLogger(__name__)

class StoryGraphMatchScanner(TestScanner):
    
    def scan_file_with_context(self, context: 'FileScanContext') -> List[Dict[str, Any]]:
        file_path = context.file_path
        story_graph = context.story_graph

        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        story_names = self._extract_story_names(story_graph)
        
        violations.extend(self._check_test_classes_match_stories(tree, story_names, file_path))
        
        return violations
    
    def _extract_story_names(self, story_graph: Dict[str, Any]) -> List[str]:
        story_names = []
        epics = story_graph.get('epics', [])
        for epic in epics:
            sub_epics = epic.get('sub_epics', [])
            for sub_epic in sub_epics:
                story_groups = sub_epic.get('story_groups', [])
                for story_group in story_groups:
                    stories = story_group.get('stories', [])
                    for story in stories:
                        story_name = story.get('name', '')
                        if story_name:
                            story_names.append(story_name)
        return story_names
    
    def _check_test_classes_match_stories(self, tree: ast.AST, story_names: List[str], file_path: Path) -> List[Dict[str, Any]]:
        violations = []
        
        classes = Classes(tree)
        for cls in classes.get_many_classes:
            if cls.node.name.startswith('Test'):
                story_name_from_class = cls.node.name[4:]
                
                matches = [s for s in story_names if story_name_from_class.lower().replace('_', ' ') in s.lower()]
                
                if not matches:
                    line_number = cls.node.lineno if hasattr(cls.node, 'lineno') else None
                    violation = Violation(
                        rule=self.rule,
                        violation_message=f'Test class "{cls.node.name}" does not match any story in the story graph',
                        location=str(file_path),
                        line_number=line_number,
                        severity='warning'
                    ).to_dict()
                    violations.append(violation)
        
        return violations
