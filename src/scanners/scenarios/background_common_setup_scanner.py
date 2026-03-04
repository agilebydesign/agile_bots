"""
Background Common Setup Scanner

Rule: background_vs_scenario_setup

Validates that:
1. Background only contains Given/And steps (no When/Then)
2. Background is only used when 3+ scenarios share common setup
3. Suggests Background when scenarios repeat the same Given steps
4. Background steps must use parameters from example tables (no hardcoded values)
"""

import re
from typing import List, Dict, Any, Optional
from scanners.story_scanner import StoryScanner
from scanners.story_map import StoryNode, Story
from scanners.violation import Violation


class BackgroundCommonSetupScanner(StoryScanner):
    
    def scan_story_node(self, node: StoryNode) -> List[Dict[str, Any]]:
        violations = []
        
        if isinstance(node, Story):
            story_data = node.data
            scenarios = story_data.get('scenarios', [])
            background = story_data.get('background', [])
            
            bg_steps = background
            if isinstance(background, dict):
                bg_steps = background.get('steps', [])
            
            if bg_steps:
                violation = self._check_background_has_when_then(bg_steps, node)
                if violation:
                    violations.append(violation)
                
                violation = self._check_background_scenario_specific(bg_steps, scenarios, node)
                if violation:
                    violations.append(violation)
                
                violation = self._check_background_missing_parameters(background, scenarios, node)
                if violation:
                    violations.append(violation)
            
            if len(scenarios) >= 3 and not background:
                violation = self._check_missing_background(scenarios, node)
                if violation:
                    violations.append(violation)
        
        return violations
    
    def _check_background_has_when_then(self, background: List[str], node: StoryNode) -> Optional[Dict[str, Any]]:
        for step in background:
            step_lower = step.lower().strip()
            if step_lower.startswith('when ') or step_lower.startswith('then '):
                location = f"{node.map_location()}.background"
                return Violation(
                    rule=self.rule,
                    violation_message=f'Background contains "{step}" - Background should only contain Given/And steps, not When/Then',
                    location=location,
                    severity='error'
                ).to_dict()
        return None
    
    def _check_background_scenario_specific(self, background: List[str], scenarios: List[Dict[str, Any]], node: StoryNode) -> Optional[Dict[str, Any]]:
        if len(scenarios) < 3 and background:
            location = f"{node.map_location()}.background"
            return Violation(
                rule=self.rule,
                violation_message=f'Background exists but story has only {len(scenarios)} scenario(s) - Background should only be used when 3+ scenarios share common setup',
                location=location,
                severity='error'
            ).to_dict()
        
        return None
    
    def _check_background_missing_parameters(self, background, scenarios: List[Dict[str, Any]], node: StoryNode) -> Optional[Dict[str, Any]]:
        """Check if background steps are missing {Concept} references (hardcoded values)."""
        bg_steps = background if isinstance(background, list) else []
        if isinstance(background, dict):
            bg_steps = background.get('steps', [])
        
        if not bg_steps:
            return None
        
        # Get all domain concept names from the story graph context
        available_concepts = set()
        for scenario in scenarios:
            examples = scenario.get('examples', [])
            for example in examples:
                name = example.get('name', '')
                if name:
                    available_concepts.add(name.lower())
        
        hardcoded_steps = []
        for step in bg_steps:
            if not isinstance(step, str):
                continue
            if '{' in step and '}' in step:
                continue
            
            step_lower = step.lower()
            for concept in available_concepts:
                if concept in step_lower:
                    hardcoded_steps.append(step)
                    break
        
        if hardcoded_steps:
            location = f"{node.map_location()}.background"
            return Violation(
                rule=self.rule,
                violation_message=f'Background steps have bare domain terms without {{Concept}} notation: {hardcoded_steps[:2]}',
                location=location,
                severity='error'
            ).to_dict()
        
        return None
    
    def _check_missing_background(self, scenarios: List[Dict[str, Any]], node: StoryNode) -> Optional[Dict[str, Any]]:
        if len(scenarios) >= 3:
            from collections import Counter
            first_givens = []
            for scenario in scenarios:
                given_steps = self._get_given_steps(scenario)
                if given_steps:
                    first_givens.append(given_steps[0])
            
            if first_givens:
                counts = Counter(first_givens)
                most_common, freq = counts.most_common(1)[0]
                if freq >= 3:
                    location = f"{node.map_location()}"
                    return Violation(
                        rule=self.rule,
                        violation_message=f'Story has {freq}/{len(scenarios)} scenarios starting with same Given step - extract to Background: "{most_common[:80]}"',
                        location=location,
                        severity='info'
                    ).to_dict()
        
        return None
    
    def _get_given_steps(self, scenario: Dict[str, Any]) -> List[str]:
        steps = []
        scenario_steps = self._get_scenario_steps(scenario)
        for step in scenario_steps:
            step_lower = step.lower().strip()
            if step_lower.startswith('given ') or step_lower.startswith('and '):
                steps.append(step)
            else:
                break
        return steps
    
    def _get_scenario_steps(self, scenario: Dict[str, Any]) -> List[str]:
        if isinstance(scenario, dict):
            if 'steps' in scenario:
                steps = scenario['steps']
                if isinstance(steps, str):
                    return [s.strip() for s in steps.split('\n') if s.strip()]
                return steps if isinstance(steps, list) else []
            elif 'scenario' in scenario:
                scenario_text = scenario['scenario']
                if isinstance(scenario_text, str):
                    return [s.strip() for s in scenario_text.split('\n') if s.strip()]
        return []
