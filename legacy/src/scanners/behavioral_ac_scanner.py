"""Scanner for counting acceptance criteria based on WHEN/THEN/AND keywords."""

from typing import List, Dict, Any, Optional
from .story_scanner import StoryScanner
from .story_map import StoryNode, Story
from .violation import Violation
import re


class BehavioralACScanner(StoryScanner):
    
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        """
        This scanner is disabled - it was counting AC incorrectly.
        The story_sizing_scanner handles AC count validation.
        
        AC counting rules:
        - Each WHEN starts a new AC
        - Each AND adds +1 to the AC count
        - THEN is part of the AC but doesn't add to count
        
        Example:
        WHEN user clicks button
        THEN system validates
        AND system saves
        AND system displays message
        = 3 AC (1 WHEN + 2 ANDs)
        """
        violations = []
        
        # No checks - AC counting is handled by story_sizing_scanner
        
        return violations
    
    def _get_ac_text(self, ac: Any) -> str:
        if isinstance(ac, dict):
            return ac.get('criterion', '') or ac.get('description', '') or str(ac)
        return str(ac)

