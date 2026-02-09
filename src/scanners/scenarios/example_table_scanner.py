"""
Example Table Scanner

Rule: example_tables_grounded_in_scenario

This scanner validates that example table columns:
1. Reflect nouns/entities mentioned in the scenario steps (including background)
2. Use domain concept terminology (not UI element names)
3. Include parent concepts when child concepts are mentioned (grounded in scenario)

The key principle is GROUNDING: we only check relationships between concepts
that are BOTH mentioned in the scenario text. This avoids creating a web
of dependencies from the domain model.

Uses ScenarioScannerBase.get_all_steps() to include background in analysis.
Uses cross-epic domain concept collection to find User/Entitlement etc.
"""

from typing import List, Dict, Any, Set, TYPE_CHECKING
from scanners.scenarios.scenario_scanner_base import ScenarioScannerBase
from scanners.story_map import StoryNode, Story, Scenario
from scanners.violation import Violation

if TYPE_CHECKING:
    from actions.rules.rule import Rule


class ExampleTableScanner(ScenarioScannerBase):
    """
    Scanner that validates example tables match scenario nouns and domain structure.
    
    Grounded in scenario language: only checks relationships between concepts
    that are mentioned together in the scenario text.
    """
    
    def __init__(self, rule: 'Rule'):
        super().__init__(rule)

    def scan_story_node(self, node: StoryNode) -> List[Dict[str, Any]]:
        """Scan a story node for example table violations."""
        violations = []
        
        if not isinstance(node, Story):
            return violations
        
        # Collect domain concepts for this story's context (from FULL story graph)
        domain_concepts = self._collect_domain_concepts_for_story(node)
        
        if not domain_concepts:
            return violations
        
        # Build lookup structures
        concept_names = self._extract_concept_names(domain_concepts)
        concept_attributes = self._extract_concept_attributes(domain_concepts)
        domain_relationships = self._extract_domain_relationships(domain_concepts)
        
        # Scan each scenario
        for scenario in node.scenarios:
            table_violations = self._check_example_tables(
                scenario, concept_names, concept_attributes, domain_concepts, node
            )
            violations.extend(table_violations)
            
            noun_violations = self._check_scenario_nouns_in_examples(
                scenario, concept_names, domain_concepts, node
            )
            violations.extend(noun_violations)
            
            structure_violations = self._check_examples_match_domain_structure(
                scenario, domain_concepts, domain_relationships, node
            )
            violations.extend(structure_violations)
            
            naming_violations = self._check_example_table_naming(
                scenario, concept_names, domain_concepts, node
            )
            violations.extend(naming_violations)
            
            # Check for implementation ID columns that should be hidden
            id_violations = self._check_implementation_id_columns(
                scenario, node
            )
            violations.extend(id_violations)
        
        return violations
    
    def _check_example_tables(
        self,
        scenario: Scenario,
        concept_names: Set[str],
        concept_attributes: Set[str],
        domain_concepts: List[Dict[str, Any]],
        story: Story
    ) -> List[Dict[str, Any]]:
        """Check that example table columns use domain attribute terminology."""
        violations = []
        
        columns = scenario.examples_columns
        if not columns:
            return violations
        
        non_domain_columns = []
        for column in columns:
            if not self._matches_domain_attribute(column, concept_names, concept_attributes):
                non_domain_columns.append(column)
        
        if non_domain_columns:
            suggestions = self._suggest_domain_terms(non_domain_columns, concept_attributes, concept_names)
            
            violation = Violation(
                rule=self.rule,
                violation_message=(
                    f'Example columns not aligned with domain: {", ".join(non_domain_columns)}. '
                    f'Consider domain terms like: {", ".join(suggestions[:5])}'
                ),
                location=scenario.map_location('examples'),
                severity='error'
            ).to_dict()
            violations.append(violation)
        
        return violations
    
    def _check_scenario_nouns_in_examples(
        self,
        scenario: Scenario,
        concept_names: Set[str],
        domain_concepts: List[Dict[str, Any]],
        story: Story
    ) -> List[Dict[str, Any]]:
        """
        Check that nouns/entities from scenario steps are represented in examples.
        
        Uses get_all_steps() to include background in analysis.
        """
        violations = []
        
        columns = scenario.examples_columns
        if not columns:
            return violations
        
        # Find domain concepts mentioned in ALL steps (background + scenario steps)
        steps_text = self.get_steps_text(scenario)
        concepts_in_scenario = self._find_domain_concepts_in_text(steps_text, domain_concepts)
        
        # Find domain concepts represented in examples
        concepts_in_examples = self._find_domain_concepts_in_columns(columns, domain_concepts)
        
        # Find concepts in scenario but missing from examples
        missing_concepts = concepts_in_scenario - concepts_in_examples
        
        # Filter out truly generic concepts (but NOT if they're actual domain concepts)
        always_generic = {'system', 'application', 'service'}
        domain_concept_names_lower = self._get_domain_concept_names_lower(domain_concepts)
        if 'user' not in domain_concept_names_lower:
            always_generic.add('user')
        if 'entitlement' not in domain_concept_names_lower:
            always_generic.add('entitlement')
        
        missing_concepts = missing_concepts - always_generic
        
        if missing_concepts:
            violation = Violation(
                rule=self.rule,
                violation_message=(
                    f'Scenario mentions domain concepts not in examples: {", ".join(sorted(missing_concepts))}. '
                    f'Add columns like: {", ".join([f"{c}_id" for c in sorted(missing_concepts)[:3]])}'
                ),
                location=scenario.map_location('examples'),
                severity='error'
            ).to_dict()
            violations.append(violation)
        
        return violations
    
    def _check_examples_match_domain_structure(
        self,
        scenario: Scenario,
        domain_concepts: List[Dict[str, Any]],
        domain_relationships: Dict[str, Set[str]],
        story: Story
    ) -> List[Dict[str, Any]]:
        """
        Check domain structure with connected tables.
        
        Uses get_all_steps() to include background in analysis.
        """
        violations = []
        columns = scenario.examples_columns
        if not columns:
            return violations

        steps_text = self.get_steps_text(scenario)
        concepts_in_scenario = self._find_domain_concepts_in_text(steps_text, domain_concepts)
        concepts_in_columns = self._find_domain_concepts_in_columns(columns, domain_concepts, fuzzy=True)

        # Check each concept mentioned in scenario has a table
        normalized_tables = scenario._normalized_examples()
        concept_tables = {}
        for table in normalized_tables:
            table_columns = table.get('columns') or table.get('headers') or []
            for concept in concepts_in_scenario:
                for col in table_columns:
                    if self._matches_domain_attribute(col, {concept}, set(), fuzzy=True):
                        concept_tables.setdefault(concept, []).append(table)

        for concept in concepts_in_scenario:
            if concept not in concept_tables:
                violation = Violation(
                    rule=self.rule,
                    violation_message=(
                        f'No example table found for domain concept "{concept}". Each concept should have its own table.'
                    ),
                    location=scenario.map_location('examples'),
                    severity='error'
                ).to_dict()
                violations.append(violation)

        if len(concept_tables) < len(concepts_in_scenario):
            violation = Violation(
                rule=self.rule,
                violation_message=(
                    f'Flat example table detected: Example tables should be separated for each domain concept. Found {len(concept_tables)} tables for {len(concepts_in_scenario)} concepts.'
                ),
                location=scenario.map_location('examples'),
                severity='error'
            ).to_dict()
            violations.append(violation)

        # Check parent-child relationships
        if len(concepts_in_scenario) < 2:
            return violations
        missing_parents = set()
        for concept in concepts_in_columns:
            for parent, children in domain_relationships.items():
                if concept in children:
                    if parent in concepts_in_scenario and parent not in concepts_in_columns:
                        missing_parents.add(parent)
        if missing_parents:
            violation = Violation(
                rule=self.rule,
                violation_message=(
                    f'Scenario mentions {", ".join(sorted(missing_parents))} but examples missing columns. '
                    f'Since the scenario discusses these concepts, examples should include them.'
                ),
                location=scenario.map_location('examples'),
                severity='error'
            ).to_dict()
            violations.append(violation)
        return violations
    
    def _matches_domain_attribute(
        self,
        column: str,
        concept_names: Set[str],
        concept_attributes: Set[str],
        fuzzy: bool = False
    ) -> bool:
        """Check if a column name matches domain attributes."""
        column_lower = column.lower()
        
        # Check acceptable column patterns first
        if column_lower in self.ACCEPTABLE_COLUMN_PATTERNS:
            return True
        
        # Check if any acceptable pattern is contained
        for pattern in self.ACCEPTABLE_COLUMN_PATTERNS:
            if pattern in column_lower or column_lower in pattern:
                return True
        
        # Direct match
        if column_lower in concept_attributes:
            return True
        
        # Check if column contains concept name
        for concept in concept_names:
            if concept in column_lower:
                return True
        
        # Check underscore-separated parts
        parts = column_lower.split('_')
        for part in parts:
            if part in concept_names or part in concept_attributes:
                return True
        
        # Fuzzy matching if enabled
        if fuzzy:
            for concept in concept_names:
                if self._similar(column_lower, concept):
                    return True
        
        return False

    def _suggest_domain_terms(
        self,
        non_domain_columns: List[str],
        concept_attributes: Set[str],
        concept_names: Set[str]
    ) -> List[str]:
        """Suggest domain terms that might replace non-domain columns."""
        suggestions = []
        
        for column in non_domain_columns:
            column_lower = column.lower()
            for attr in concept_attributes:
                if self._similar(column_lower, attr):
                    suggestions.append(attr)
        
        if not suggestions:
            suggestions = [f"{c}_id" for c in list(concept_names)[:3] if not c.endswith('s')]
        
        return list(set(suggestions))

    def _check_example_table_naming(
        self,
        scenario: Scenario,
        concept_names: Set[str],
        domain_concepts: List[Dict[str, Any]],
        story: Story
    ) -> List[Dict[str, Any]]:
        """
        Check that example table names are concept names, not connecting sentences.
        
        Validates:
        1. The 'name' field should be a domain concept name (e.g., 'Recipient', 'Enterprise')
        2. Connecting sentences like 'has these Recipients' should use 'collaboration' field instead
        3. Collaboration field should reflect domain responsibilities
        """
        violations = []
        
        normalized_tables = scenario._normalized_examples()
        if not normalized_tables:
            return violations
        
        # Extract all responsibility sentences from domain concepts for validation
        responsibility_sentences = self._extract_responsibility_sentences(domain_concepts)
        
        # Patterns that indicate a connecting sentence (not a concept name)
        connecting_patterns = [
            'has these', 'with these', 'each with', 'the ', 'for this',
            'belonging to', 'associated with', 'related to'
        ]
        
        for table in normalized_tables:
            table_name = table.get('name', '')
            if not table_name:
                continue
            
            table_name_lower = table_name.lower().strip()
            collaboration = table.get('collaboration', '')
            
            # Check if the name looks like a connecting sentence instead of a concept name
            is_connecting_sentence = any(
                pattern in table_name_lower for pattern in connecting_patterns
            )
            
            # Check if it's a known concept name
            is_concept_name = table_name_lower in concept_names or any(
                concept.lower() == table_name_lower or 
                concept.lower() == table_name_lower.replace('the ', '') 
                for concept in concept_names
            )
            
            if is_connecting_sentence and not is_concept_name:
                # This looks like a connecting sentence used as a name
                # Suggest using the concept name with collaboration field instead
                suggested_concept = self._guess_concept_from_name(table_name, concept_names)
                
                violation = Violation(
                    rule=self.rule,
                    violation_message=(
                        f'Example table name "{table_name}" looks like a connecting sentence. '
                        f'Use concept name as "name" field (e.g., "{suggested_concept}") and move '
                        f'the connecting sentence to "collaboration" field to reflect domain responsibilities.'
                    ),
                    location=scenario.map_location('examples'),
                    severity='error'
                ).to_dict()
                violations.append(violation)
            
            # If collaboration is provided, check it matches domain responsibilities
            if collaboration and collaboration not in responsibility_sentences:
                # Warn if collaboration doesn't match known responsibilities (but only as info)
                # This is informational - the collaboration might still be valid
                pass  # For now, just validate the structure, not the exact match
        
        return violations
    
    def _extract_responsibility_sentences(
        self,
        domain_concepts: List[Dict[str, Any]]
    ) -> Set[str]:
        """Extract all responsibility sentences from domain concepts."""
        sentences = set()
        
        for concept in domain_concepts:
            for resp in concept.get('responsibilities', []):
                resp_name = resp.get('name', '')
                if resp_name:
                    sentences.add(resp_name.lower())
        
        return sentences
    
    def _guess_concept_from_name(self, table_name: str, concept_names: Set[str]) -> str:
        """
        Try to guess the concept name from a connecting sentence.
        
        E.g., 'has these Recipients' -> 'Recipient'
        """
        table_name_lower = table_name.lower()
        
        # Look for concept names within the table name
        for concept in concept_names:
            # Check for plural or singular variants
            if concept in table_name_lower or concept + 's' in table_name_lower:
                return concept.title()
        
        # Default: extract the last capitalized word
        words = table_name.split()
        for word in reversed(words):
            if word and word[0].isupper():
                # Return singular form
                return word.rstrip('s')
        
        return 'ConceptName'

    def _check_implementation_id_columns(
        self,
        scenario: Scenario,
        story: Story
    ) -> List[Dict[str, Any]]:
        """
        Check for ID columns that are implementation concerns.
        
        ID columns used only for linking tables (foreign keys) should be hidden.
        Table relationships are expressed via collaboration field and ordering.
        """
        violations = []
        columns = scenario.examples_columns
        if not columns:
            return violations
        
        # Patterns that indicate implementation ID columns
        id_patterns = [
            r'^[a-z]+_id$',           # user_id, enterprise_id, recipient_id
            r'^id$',                   # just 'id'
            r'_id$',                   # anything ending in _id
            r'^[A-Z]{2,}[-_]\d+$',    # Patterns like ENT-001, USR-001 (values, not columns)
        ]
        
        import re
        id_columns = []
        for col in columns:
            col_lower = col.lower()
            for pattern in id_patterns:
                if re.match(pattern, col_lower):
                    id_columns.append(col)
                    break
        
        if id_columns:
            violation = Violation(
                rule=self.rule,
                violation_message=(
                    f'ID columns are implementation concerns and should be hidden: {id_columns}. '
                    f'Table relationships are expressed via collaboration field and table ordering, not foreign keys.'
                ),
                location=scenario.map_location('examples'),
                severity='error'
            ).to_dict()
            violations.append(violation)
        
        return violations
