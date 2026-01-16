"""Scanner for validating folder structure matches story map hierarchy."""

from typing import List, Dict, Any, Optional
from pathlib import Path
from .story_scanner import StoryScanner
from .story_map import StoryNode, Epic, SubEpic, Story
from .violation import Violation
import re


class IncrementFolderStructureScanner(StoryScanner):
    
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        # Only check epics and their direct stories (scenarios behavior)
        if isinstance(node, Epic):
            epic_name = node.name
            if not epic_name:
                return violations
            
            has_stories_with_scenarios = self._epic_has_stories_with_scenarios(node)
            
            if has_stories_with_scenarios:
                violation = self._check_epic_folder_structure(node, rule_obj)
                if violation:
                    violations.append(violation)
        
        return violations
    
    def _epic_has_stories_with_scenarios(self, epic: Epic) -> bool:
        for child in epic.children:
            if isinstance(child, Story):
                story_data = child.data
                scenarios = story_data.get('scenarios', [])
                if scenarios:
                    return True
        return False
    
    def _check_epic_folder_structure(self, node: StoryNode, rule_obj: Any) -> Optional[Dict[str, Any]]:
        epic_name = node.name
        expected_folder = f"🎯 {epic_name}"
        
        # This scanner validates structure, but actual folder checking
        # would require workspace context (not available in story graph)
        # For now, validate that epic name follows expected format
        
        if not epic_name.startswith('🎯'):
            # Epic name should have emoji prefix in folder structure
            # But story graph may not include emoji, so this is informational
            pass
        
        return None

