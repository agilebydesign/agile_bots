"""
Plain English Scenarios Scanner

Rule: write_plain_english_scenarios

Validates that scenarios use plain English, not parameterized templates
with <variable> placeholders or Scenario Outline syntax.
"""

from typing import List, Dict, Any, Optional
from scanners.story_scanner import StoryScanner
from scanners.story_map import StoryNode, Story
from scanners.violation import Violation
import re


class PlainEnglishScenariosScanner(StoryScanner):
    """Validates scenarios use domain-parameterized language, not arbitrary template placeholders.
    
    ALLOWS:
    - {DomainConcept} notation for parameterized domain concepts
    - Examples tables (now required by write_concrete_scenarios rule)
    
    REJECTS:
    - <variable> angle-bracket placeholders (non-domain style)
    """
    
    def scan_story_node(self, node: StoryNode) -> List[Dict[str, Any]]:
        violations = []
        
        if isinstance(node, Story):
            story_data = node.data
            scenarios = story_data.get('scenarios', [])
            
            for scenario_idx, scenario in enumerate(scenarios):
                scenario_text = self._get_scenario_text(scenario)
                
                # Only check for angle-bracket variables (not curly-brace domain parameters)
                violation = self._check_variables(scenario_text, node, scenario_idx)
                if violation:
                    violations.append(violation)
                
                # Scenario Outline is still not preferred (use individual scenarios with examples)
                violation = self._check_scenario_outline(scenario_text, node, scenario_idx)
                if violation:
                    violations.append(violation)
                
                # NOTE: Examples tables are now REQUIRED by write_concrete_scenarios rule
                # Do NOT check for examples as violations
        
        return violations
    
    def _get_scenario_text(self, scenario: Dict[str, Any]) -> str:
        if isinstance(scenario, dict):
            return scenario.get('scenario', '') or scenario.get('name', '') or str(scenario)
        return str(scenario)
    
    def _check_variables(self, scenario_text: str, node: StoryNode, scenario_idx: int) -> Optional[Dict[str, Any]]:
        if re.search(r'<[^>]+>', scenario_text):
            location = f"{node.map_location()}.scenarios[{scenario_idx}]"
            return Violation(
                rule=self.rule,
                violation_message=f'Scenario contains variable placeholder (e.g., "<variable>") - use plain English instead',
                location=location,
                severity='error'
            ).to_dict()
        
        if re.search(r'"[<][^>]+[>]"', scenario_text):
            location = f"{node.map_location()}.scenarios[{scenario_idx}]"
            return Violation(
                rule=self.rule,
                violation_message=f'Scenario contains quoted placeholder (e.g., "<variable>") - use plain English instead',
                location=location,
                severity='error'
            ).to_dict()
        
        return None
    
    def _check_scenario_outline(self, scenario_text: str, node: StoryNode, scenario_idx: int) -> Optional[Dict[str, Any]]:
        if 'Scenario Outline:' in scenario_text or 'Scenario Outline' in scenario_text:
            location = f"{node.map_location()}.scenarios[{scenario_idx}]"
            return Violation(
                rule=self.rule,
                violation_message='Scenario uses Scenario Outline - use plain English scenarios instead',
                location=location,
                severity='error'
            ).to_dict()
        
        return None
    
    # _check_examples_table REMOVED - Examples tables are now REQUIRED by write_concrete_scenarios rule
    # Every {parameter} in Background/Steps MUST have corresponding example table with concrete data
