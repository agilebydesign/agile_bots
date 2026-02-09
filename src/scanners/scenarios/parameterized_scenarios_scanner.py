"""
Parameterized Scenarios Scanner

Rule: write_concrete_scenarios (updated)

Validates that scenarios use {DomainConcept} parameterization with:
1. Domain concept names as parameters (not arbitrary placeholders)
2. Example tables that provide concrete data for each parameter
3. Background steps also have corresponding example tables
4. Parameters trace back to base data dependencies
"""

from typing import List, Dict, Any, Optional, Set
from scanners.scenarios.scenario_scanner_base import ScenarioScannerBase
from scanners.story_map import StoryNode, Story, Scenario
from scanners.violation import Violation
import re


class ParameterizedScenariosScanner(ScenarioScannerBase):
    """
    Scanner that validates parameterized scenarios follow domain-driven rules.
    
    Key principles:
    - {DomainConcept} parameters are ENCOURAGED (not angle brackets)
    - Every parameter MUST have corresponding example table column
    - Background steps need example tables too
    - Parameters should be domain concept names
    """
    
    def scan_story_node(self, node: StoryNode) -> List[Dict[str, Any]]:
        violations = []
        
        if not isinstance(node, Story):
            return violations
        
        # Collect domain concepts for validation
        domain_concepts = self._collect_domain_concepts_for_story(node)
        concept_names = self._extract_concept_names(domain_concepts) if domain_concepts else set()
        
        # Check background for parameter/example alignment
        background_violations = self._check_background_examples(node, concept_names)
        violations.extend(background_violations)
        
        # Scan each scenario
        for scenario in node.scenarios:
            # Check for angle-bracket variables (BAD)
            angle_violations = self._check_angle_bracket_variables(scenario, node)
            violations.extend(angle_violations)
            
            # Check parameter/example alignment
            param_violations = self._check_parameter_example_alignment(scenario, node, concept_names)
            violations.extend(param_violations)
            
            # Check for hardcoded values without parameterization
            hardcode_violations = self._check_hardcoded_domain_values(scenario, node, concept_names)
            violations.extend(hardcode_violations)
            
            # Check for adjacent parameters without relationship language
            adjacent_violations = self._check_adjacent_parameters(scenario, node)
            violations.extend(adjacent_violations)
        
        return violations
    
    def _check_background_examples(self, story: Story, concept_names: Set[str]) -> List[Dict[str, Any]]:
        """Check that background steps have corresponding example tables."""
        violations = []
        
        # Get background from first scenario if it exists
        if not story.scenarios:
            return violations
        
        first_scenario = story.scenarios[0]
        background = first_scenario.background
        
        if not background:
            return violations
        
        # Extract parameters from background
        background_text = ' '.join(background) if isinstance(background, list) else str(background)
        params = self._extract_curly_params(background_text)
        
        if not params:
            return violations
        
        # Get example table names
        example_names = self._get_example_table_names(first_scenario)
        
        # Check each parameter has a corresponding table
        for param in params:
            param_lower = param.lower()
            if not any(param_lower in name.lower() for name in example_names):
                location = f"{story.map_location()}.background"
                violations.append(Violation(
                    rule=self.rule,
                    violation_message=f"Background parameter '{{{param}}}' has no corresponding example table. Add a '{param}' table with concrete data.",
                    location=location,
                    severity='error'
                ).to_dict())
        
        return violations
    
    def _check_angle_bracket_variables(self, scenario: Scenario, story: Story) -> List[Dict[str, Any]]:
        """Flag angle-bracket <variable> placeholders as violations."""
        violations = []
        
        steps_text = self._get_all_steps_text(scenario)
        
        if re.search(r'<[^>]+>', steps_text):
            location = f"{story.map_location()}.scenarios[{scenario.name}]"
            violations.append(Violation(
                rule=self.rule,
                violation_message="Use {DomainConcept} notation, not <variable> angle brackets. Example: {User}, {PaymentAmount}, {Enterprise}",
                location=location,
                severity='error'
            ).to_dict())
        
        return violations
    
    def _check_parameter_example_alignment(self, scenario: Scenario, story: Story, concept_names: Set[str]) -> List[Dict[str, Any]]:
        """Check that {parameters} have matching example table columns."""
        violations = []
        
        steps_text = self._get_all_steps_text(scenario)
        params = self._extract_curly_params(steps_text)
        
        if not params:
            return violations
        
        # Get example columns
        example_columns = set()
        if scenario.examples_columns:
            example_columns = {col.lower().replace('_', '') for col in scenario.examples_columns}
        
        # Get example table names (concepts)
        example_names = self._get_example_table_names(scenario)
        example_names_lower = {name.lower().replace(' ', '').replace('_', '') for name in example_names}
        
        for param in params:
            param_normalized = param.lower().replace('_', '').replace(' ', '')
            
            # Check if parameter matches a table name or column
            has_match = (
                param_normalized in example_names_lower or
                param_normalized in example_columns or
                any(param_normalized in col for col in example_columns)
            )
            
            if not has_match:
                location = f"{story.map_location()}.scenarios[{scenario.name}]"
                violations.append(Violation(
                    rule=self.rule,
                    violation_message=f"Parameter '{{{param}}}' has no matching example table or column. Add a '{param}' table or column with concrete data.",
                    location=location,
                    severity='error'
                ).to_dict())
        
        return violations
    
    def _check_hardcoded_domain_values(self, scenario: Scenario, story: Story, concept_names: Set[str]) -> List[Dict[str, Any]]:
        """Flag hardcoded domain values that should be parameterized."""
        violations = []
        
        steps_text = self._get_all_steps_text(scenario)
        
        # Common patterns that suggest hardcoding
        hardcode_patterns = [
            # Dollar amounts without parameter
            (r'(?<!\{)\$[\d,]+\.?\d*(?!\})', 'Payment amount should be parameterized: {PaymentAmount}'),
            # User names without parameter
            (r'(?<!\{)(Jane Doe|John Smith|Admin User)(?!\})', 'User name should be parameterized: {User}'),
        ]
        
        for pattern, message in hardcode_patterns:
            if re.search(pattern, steps_text, re.IGNORECASE):
                # Only flag if no {parameter} version exists nearby
                has_params = self._extract_curly_params(steps_text)
                if not has_params:
                    location = f"{story.map_location()}.scenarios[{scenario.name}]"
                    violations.append(Violation(
                        rule=self.rule,
                        violation_message=message,
                        location=location,
                        severity='info'
                    ).to_dict())
                    break  # One warning is enough
        
        return violations
    
    def _check_adjacent_parameters(self, scenario: Scenario, story: Story) -> List[Dict[str, Any]]:
        """Flag adjacent {parameters} without relationship language between them.
        
        Examples of violations:
        - {PaymentAmount} {amount} - duplicate concept attribute
        - {WirePayment} {PaymentAmount} - no relationship verb
        - {Enterprise} {User} - concepts jammed together
        
        Should be:
        - {WirePayment} holds {PaymentAmount}
        - {User} belonging to {Enterprise}
        """
        violations = []
        
        steps_text = self._get_all_steps_text(scenario)
        
        # Pattern: } followed by optional whitespace, then {
        # This catches {Concept1} {Concept2} patterns
        adjacent_pattern = r'\{([^}]+)\}\s*\{([^}]+)\}'
        
        matches = re.findall(adjacent_pattern, steps_text)
        
        for param1, param2 in matches:
            location = f"{story.map_location()}.scenarios[{scenario.name}]"
            violations.append(Violation(
                rule=self.rule,
                violation_message=f"Adjacent parameters '{{{param1}}} {{{param2}}}' need relationship language. Use collaboration verbs: '{{{param1}}} holds/references/validates {{{param2}}}' or '{{{param2}}} belonging to {{{param1}}}'",
                location=location,
                severity='error'
            ).to_dict())
        
        return violations
    
    def _get_all_steps_text(self, scenario: Scenario) -> str:
        """Get all step text from a scenario including background."""
        parts = []
        
        if scenario.background:
            if isinstance(scenario.background, list):
                parts.extend(scenario.background)
            else:
                parts.append(str(scenario.background))
        
        if scenario.steps:
            for step in scenario.steps:
                if isinstance(step, dict):
                    parts.append(step.get('text', ''))
                else:
                    parts.append(str(step))
        
        return ' '.join(parts)
    
    def _extract_curly_params(self, text: str) -> Set[str]:
        """Extract {parameter} names from text."""
        matches = re.findall(r'\{([^}]+)\}', text)
        return set(matches)
    
    def _get_example_table_names(self, scenario: Scenario) -> Set[str]:
        """Get names of example tables (domain concept names)."""
        names = set()
        
        if hasattr(scenario, '_data') and isinstance(scenario._data, dict):
            examples = scenario._data.get('examples', [])
            for example in examples:
                if isinstance(example, dict):
                    name = example.get('name', '')
                    if name:
                        names.add(name)
        
        return names
