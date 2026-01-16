from typing import List, Dict, Any, Optional
from .story_scanner import StoryScanner
from .story_map import StoryNode, Story
from .violation import Violation


class ReactionChainingScanner(StoryScanner):
    """
    Scans acceptance criteria to ensure multiple system reactions are chained with 'And'.
    Checks that separate WHEN/THEN blocks aren't created for sequential system actions.
    """
    
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        if isinstance(node, Story):
            acceptance_criteria = node.data.get('acceptance_criteria', [])
            
            for idx, ac in enumerate(acceptance_criteria):
                if not isinstance(ac, str):
                    continue
                
                violation = self._check_reaction_chaining(ac, node, idx, rule_obj)
                if violation:
                    violations.append(violation)
        
        return violations
    
    def _check_reaction_chaining(self, ac: str, story: Story, ac_index: int, rule_obj: Any) -> Optional[Dict[str, Any]]:
        """Check if system reactions are properly chained with And instead of separate WHEN/THEN."""
        lines = [line.strip() for line in ac.split('\n') if line.strip()]
        
        if len(lines) < 2:
            return None
        
        # Look for pattern: THEN system X / WHEN system Y / THEN system Z
        # This should be: THEN system X AND system Y AND system Z
        for i in range(len(lines) - 1):
            current_line = lines[i].lower()
            next_line = lines[i + 1].lower()
            
            # Check if current line is THEN with system action
            if current_line.startswith('then ') and self._is_system_action(current_line):
                # Check if next line is WHEN with system action (should be AND instead)
                if next_line.startswith('when ') and self._is_system_action(next_line):
                    location = story.map_location(f'acceptance_criteria[{ac_index}]')
                    return Violation(
                        rule=rule_obj,
                        violation_message=f'Story "{story.name}" AC #{ac_index + 1} has separate WHEN/THEN for sequential system actions (should use AND to chain reactions)',
                        location=location,
                        severity='warning'
                    ).to_dict()
        
        # Check for excessively long And chains (more than 4 reactions)
        and_chain_count = 0
        for line in lines:
            line_lower = line.lower()
            if line_lower.startswith('and '):
                and_chain_count += 1
                if and_chain_count > 4:
                    location = story.map_location(f'acceptance_criteria[{ac_index}]')
                    return Violation(
                        rule=rule_obj,
                        violation_message=f'Story "{story.name}" AC #{ac_index + 1} has excessive And chain ({and_chain_count} reactions, should be max 4)',
                        location=location,
                        severity='warning'
                    ).to_dict()
            else:
                # Reset count when we hit a new WHEN/THEN
                and_chain_count = 0
        
        return None
    
    def _is_system_action(self, line: str) -> bool:
        """Check if a line describes a system action."""
        line_lower = line.lower()
        
        # Remove WHEN/THEN/AND keywords
        for keyword in ['when ', 'then ', 'and ', 'given ']:
            if line_lower.startswith(keyword):
                line_lower = line_lower[len(keyword):].strip()
                break
        
        # Check for system-related keywords
        system_keywords = ['system ', 'bot ', 'application ', 'server ', 'workflow ', 'action ', 'behavior ']
        return any(keyword in line_lower for keyword in system_keywords)
