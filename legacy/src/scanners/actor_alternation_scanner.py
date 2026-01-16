from typing import List, Dict, Any, Optional
from .story_scanner import StoryScanner
from .story_map import StoryNode, Story
from .violation import Violation


class ActorAlternationScanner(StoryScanner):
    """
    Scans acceptance criteria to ensure actors alternate every 1-2 steps.
    Scenarios should show back-and-forth interaction between user and system.
    """
    
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        if isinstance(node, Story):
            acceptance_criteria = node.data.get('acceptance_criteria', [])
            
            for idx, ac in enumerate(acceptance_criteria):
                if not isinstance(ac, str):
                    continue
                
                violation = self._check_actor_alternation(ac, node, idx, rule_obj)
                if violation:
                    violations.append(violation)
        
        return violations
    
    def _check_actor_alternation(self, ac: str, story: Story, ac_index: int, rule_obj: Any) -> Optional[Dict[str, Any]]:
        """Check if actors alternate properly in acceptance criteria."""
        lines = ac.split('\n')
        
        # Extract actor from each line (WHEN/THEN/AND)
        actors = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Determine actor from the line
            actor = self._extract_actor(line)
            if actor:
                actors.append(actor)
        
        if len(actors) < 3:
            # Not enough steps to check alternation
            return None
        
        # Check for runs of same actor longer than 2
        consecutive_count = 1
        prev_actor = actors[0]
        
        for i in range(1, len(actors)):
            current_actor = actors[i]
            
            if current_actor == prev_actor:
                consecutive_count += 1
                
                if consecutive_count > 2:
                    # Found violation: more than 2 consecutive steps from same actor
                    location = story.map_location(f'acceptance_criteria[{ac_index}]')
                    return Violation(
                        rule=rule_obj,
                        violation_message=f'Story "{story.name}" AC #{ac_index + 1} has {consecutive_count} consecutive {prev_actor} steps without alternating',
                        location=location,
                        severity='warning'
                    ).to_dict()
            else:
                consecutive_count = 1
                prev_actor = current_actor
        
        return None
    
    def _extract_actor(self, line: str) -> Optional[str]:
        """Extract the actor (user/system) from a WHEN/THEN/AND line."""
        line_lower = line.lower()
        
        # Skip WHEN/THEN/AND/GIVEN keywords
        for keyword in ['when ', 'then ', 'and ', 'given ']:
            if line_lower.startswith(keyword):
                line_lower = line_lower[len(keyword):].strip()
                break
        
        # Determine actor based on common patterns
        if any(word in line_lower for word in ['user ', 'actor ', 'customer ', 'developer ', 'human ', 'cli ', 'repl ']):
            return 'user'
        elif any(word in line_lower for word in ['system ', 'bot ', 'application ', 'server ', 'workflow ']):
            return 'system'
        
        # Default to system if no clear actor
        return 'system'
