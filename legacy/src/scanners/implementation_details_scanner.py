"""Scanner for detecting implementation details as stories."""

from typing import List, Dict, Any
from .story_scanner import StoryScanner
from .story_map import StoryNode, Story
from .violation import Violation
import re


class ImplementationDetailsScanner(StoryScanner):
    
    # Implementation operation verbs (should be steps, not stories)
    IMPLEMENTATION_VERBS = [
        'serialize', 'deserialize', 'convert', 'transform', 'format',
        'calculate', 'compute', 'generate', 'create',  # when referring to technical artifacts
        'apply', 'set', 'configure',  # technical settings
        'save', 'write', 'store'  # without user context
    ]
    
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        # Only scan actual Story nodes, not Epic or SubEpic nodes
        # Sub-epics can have imperative names like "Create Mobs" because they group stories
        if not isinstance(node, Story):
            return violations
        
        if not hasattr(node, 'name') or not node.name:
            return violations
        
        name_lower = node.name.lower()
        
        for verb in self.IMPLEMENTATION_VERBS:
            pattern = rf'\b{verb}\b'
            if re.search(pattern, name_lower):
                # If it's just "Verb Noun" without user context, it's likely implementation
                words = name_lower.split()
                # Check if verb is at the start (most common pattern for implementation operations)
                if verb in words[0] or (len(words) > 1 and verb in words[0:2]):
                    violation = Violation(
                        rule=rule_obj,
                        violation_message=f'Story "{node.name}" appears to be an implementation operation - should be a step within a story that describes user/system outcome',
                        location=node.name,
                        severity='error'
                    ).to_dict()
                    violations.append(violation)
                    break
        
        return violations

