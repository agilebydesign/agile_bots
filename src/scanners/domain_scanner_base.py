"""
Base class for domain-aware scanners.

Provides shared functionality for:
1. Collecting domain concepts from story graph hierarchy
2. Extracting concept names and attributes
3. Text analysis utilities (entity extraction, matching)

Subclasses:
- ScenarioLanguageScanner: Validates scenario step language matches domain
- ExampleTableScanner: Validates example tables match scenario nouns + domain structure
"""

from typing import List, Dict, Any, Optional, Set, TYPE_CHECKING
from scanners.story_scanner import StoryScanner
from scanners.story_map import StoryNode, Story, StoryMap
import re

if TYPE_CHECKING:
    from scanners.resources.scan_context import ScanFilesContext
    from actions.rules.rule import Rule


class DomainScannerBase(StoryScanner):
    """
    Base class for scanners that validate against domain concepts.
    
    Domain concepts are collected from:
    - Global level (story_graph.domain_concepts)
    - Parent epic (epic.domain_concepts)
    - Sub-epic chain (sub_epic.domain_concepts)
    """
    
    # Gherkin and common test words to ignore when extracting entities
    IGNORE_WORDS = {
        # Gherkin keywords
        'given', 'when', 'then', 'and', 'but', 'scenario', 'background',
        'feature', 'examples', 'outline',
        # Common verbs
        'is', 'are', 'has', 'have', 'does', 'do', 'will', 'can', 'should',
        'displays', 'shows', 'enters', 'clicks', 'selects', 'submits', 'creates',
        'updates', 'deletes', 'saves', 'loads', 'validates', 'verifies', 'confirms',
        'navigates', 'views', 'opens', 'closes', 'enables', 'disables',
        # Articles and prepositions
        'the', 'a', 'an', 'to', 'from', 'in', 'on', 'at', 'by', 'for', 'with',
        'of', 'as', 'into', 'through', 'during', 'before', 'after',
        # Common adjectives
        'valid', 'invalid', 'new', 'old', 'first', 'last', 'next', 'previous',
        'active', 'inactive', 'pending', 'current', 'selected', 'available',
        'empty', 'full', 'minimum', 'maximum', 'required', 'optional',
        # UI/behavioral terms (allowed in scenarios)
        'step', 'page', 'screen', 'button', 'link', 'form', 'field', 'input',
        'output', 'message', 'error', 'success', 'warning', 'info', 'list', 'table',
        # Test data patterns
        'inc', 'llc', 'corp', 'corporation', 'company', 'bank',
        # Keyboard keys and interactions
        'tab', 'enter', 'escape', 'space', 'arrow', 'shift', 'ctrl', 'alt',
        'key', 'keys', 'press', 'pressed', 'focus', 'focused', 'hover',
        # Languages
        'english', 'spanish', 'french', 'german', 'portuguese', 'chinese',
        'japanese', 'korean', 'italian', 'russian', 'arabic', 'hindi',
        # Accessibility terms
        'wcag', 'aria', 'contrast', 'ratio', 'screen', 'reader',
    }
    
    # Common table column patterns that are acceptable without domain match
    ACCEPTABLE_COLUMN_PATTERNS = {
        # State/result columns
        'status', 'state', 'result', 'outcome', 'action',
        # Display columns
        'displayed', 'visible', 'shown', 'hidden', 'enabled', 'disabled',
        # Message columns
        'message', 'error_message', 'success_message', 'warning_message',
        # Navigation columns
        'next_step', 'previous_step', 'destination', 'link',
        # Boolean columns
        'is_valid', 'is_active', 'is_enabled', 'has_access',
    }
    
    def __init__(self, rule: 'Rule'):
        super().__init__(rule)
        self._story_map: Optional[StoryMap] = None
        self._global_concepts: List[Dict[str, Any]] = []
        self._concept_cache: Dict[str, Set[str]] = {}

    def scan_with_context(self, context: 'ScanFilesContext') -> List[Dict[str, Any]]:
        """Initialize context and delegate to subclass implementation."""
        story_graph_data = context.story_graph.get('story_graph', context.story_graph)
        self._story_map = StoryMap(story_graph_data)
        self._global_concepts = story_graph_data.get('domain_concepts', [])
        
        violations = []
        for epic in self._story_map.epics():
            for node in self._story_map.walk(epic):
                if isinstance(node, Story):
                    node_violations = self.scan_story_node(node)
                    violations.extend(node_violations)
        
        return violations

    def scan_story_node(self, node: StoryNode) -> List[Dict[str, Any]]:
        """Override in subclass to implement specific scanning logic."""
        raise NotImplementedError("Subclasses must implement scan_story_node")

    # -------------------------------------------------------------------------
    # Domain Concept Collection
    # -------------------------------------------------------------------------
    
    def _collect_domain_concepts_for_story(self, story: Story) -> List[Dict[str, Any]]:
        """
        Collect all domain concepts applicable to this story.
        
        Collection order (local first, then global fallback):
        1. Story's parent sub-epic chain (most specific)
        2. Story's parent epic
        3. Global concepts
        4. ALL other epics and their sub-epics (cross-epic references)
        
        This allows scenarios to reference domain concepts defined in other epics
        (e.g., User/Entitlement from "Onboards Enterprise" used in "Create Wire Payment").
        """
        concepts = []
        seen_names = set()  # Track to avoid duplicates
        
        def add_concepts(concept_list: List[Dict[str, Any]]):
            for concept in concept_list:
                name = concept.get('name', '')
                if name and name not in seen_names:
                    seen_names.add(name)
                    concepts.append(concept)
        
        # Add global concepts first
        add_concepts(self._global_concepts)
        
        if self._story_map:
            epics = self._story_map.epics()
            
            # Phase 1: Collect from story's own epic and sub-epic chain (local context)
            if story.epic_idx < len(epics):
                epic = epics[story.epic_idx]
                add_concepts(epic.data.get('domain_concepts', []))
                
                # Navigate sub-epic chain
                current_data = epic.data
                for sub_idx in story.sub_epic_path:
                    sub_epics = current_data.get('sub_epics', [])
                    if sub_idx < len(sub_epics):
                        current_data = sub_epics[sub_idx]
                        add_concepts(current_data.get('domain_concepts', []))
            
            # Phase 2: Collect from ALL other epics (cross-epic fallback)
            for idx, epic in enumerate(epics):
                if idx == story.epic_idx:
                    continue  # Skip story's own epic (already processed)
                
                # Add epic-level concepts
                add_concepts(epic.data.get('domain_concepts', []))
                
                # Add concepts from all sub-epics recursively
                self._collect_all_sub_epic_concepts(epic.data, add_concepts)
        
        return concepts
    
    def _collect_all_sub_epic_concepts(
        self, 
        parent_data: Dict[str, Any], 
        add_concepts: callable
    ):
        """Recursively collect domain concepts from all sub-epics."""
        for sub_epic in parent_data.get('sub_epics', []):
            add_concepts(sub_epic.get('domain_concepts', []))
            # Recurse into nested sub-epics
            self._collect_all_sub_epic_concepts(sub_epic, add_concepts)
    
    def _extract_concept_names(self, domain_concepts: List[Dict[str, Any]]) -> Set[str]:
        """Extract all concept names (e.g., 'User', 'Enterprise', 'Recipient')."""
        names = set()
        for concept in domain_concepts:
            name = concept.get('name', '')
            if name:
                names.add(name.lower())
                names.add(name.lower() + 's')  # Plural
        return names
    
    def _extract_concept_attributes(self, domain_concepts: List[Dict[str, Any]]) -> Set[str]:
        """
        Extract all attributes from domain concepts.
        Looks at responsibility names, collaborators, and known fields.
        """
        attributes = set()
        
        for concept in domain_concepts:
            concept_name = concept.get('name', '').lower()
            
            # Extract from responsibilities
            for resp in concept.get('responsibilities', []):
                resp_name = resp.get('name', '')
                # Parse "Get X" or "has X" patterns
                attr_match = re.search(r'(?:Get|has|owns|maintains|assigns|grants)\s+(\w+)', resp_name, re.I)
                if attr_match:
                    attributes.add(attr_match.group(1).lower())
                
                # Add collaborators as related concepts
                for collab in resp.get('collaborators', []):
                    attributes.add(collab.lower())
            
            # Common attribute patterns based on concept name
            attributes.add(f"{concept_name}_id")
            attributes.add(f"{concept_name}_name")
            attributes.add(f"{concept_name}_status")
        
        return attributes

    # -------------------------------------------------------------------------
    # Text Analysis Utilities
    # -------------------------------------------------------------------------
    
    def _extract_entities_from_text(self, text: str) -> List[str]:
        """
        Extract potential entity references from scenario text.
        Looks for capitalized words, words after 'the', and common patterns.
        """
        entities = []
        
        # Pattern 1: Capitalized words (likely entities)
        capitalized = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', text)
        entities.extend(capitalized)
        
        # Pattern 2: Words after "the" or "a/an" (likely nouns/entities)
        after_article = re.findall(r'\b(?:the|a|an)\s+(\w+)', text, re.I)
        entities.extend(after_article)
        
        # Pattern 3: Snake_case identifiers
        identifiers = re.findall(r'\b([a-z]+_[a-z_]+)\b', text)
        entities.extend(identifiers)
        
        # Filter using class IGNORE_WORDS constant
        filtered = [e for e in entities if e.lower() not in self.IGNORE_WORDS]
        
        # Also filter out multi-word company names (test data)
        filtered = [e for e in filtered if not self._is_test_data_value(e)]
        
        return list(set(filtered))
    
    def _extract_nouns_from_steps(self, steps: List[str]) -> Set[str]:
        """
        Extract nouns from scenario steps that should be represented in examples.
        These are the concrete things the scenario is talking about.
        """
        nouns = set()
        steps_text = ' '.join(steps)
        
        # Extract entities
        entities = self._extract_entities_from_text(steps_text)
        nouns.update(e.lower() for e in entities)
        
        return nouns
    
    def _is_test_data_value(self, text: str) -> bool:
        """Check if text looks like test data (company names, etc.)."""
        text_lower = text.lower()
        # Company name patterns
        if any(suffix in text_lower for suffix in ['inc', 'llc', 'corp', 'ltd', 'co']):
            return True
        # Bank names typically end with 'bank'
        if text_lower.endswith('bank'):
            return True
        # Multi-word proper nouns (likely test data)
        if ' ' in text and text[0].isupper():
            words = text.split()
            if all(w[0].isupper() for w in words if w):
                return True
        return False
    
    def _matches_domain_term(
        self,
        term: str,
        concept_names: Set[str],
        all_domain_terms: Set[str]
    ) -> bool:
        """Check if a term matches any domain concept or attribute."""
        term_lower = term.lower()
        
        # Skip if it's in ignore words
        if term_lower in self.IGNORE_WORDS:
            return True
        
        # Direct match
        if term_lower in concept_names or term_lower in all_domain_terms:
            return True
        
        # Partial match (e.g., 'recipient_name' contains 'recipient')
        for concept in concept_names:
            if concept in term_lower or term_lower in concept:
                return True
        
        return False
    
    def _matches_domain_attribute(
        self,
        column: str,
        concept_names: Set[str],
        concept_attributes: Set[str]
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
        
        return False

    # -------------------------------------------------------------------------
    # Domain Relationship Extraction
    # -------------------------------------------------------------------------
    
    def _extract_domain_relationships(self, domain_concepts: List[Dict[str, Any]]) -> Dict[str, Set[str]]:
        """
        Extract parent-child relationships from domain concepts.
        
        Returns dict mapping parent concept -> set of child concepts.
        
        Handles both directions:
        - Parent says "owns X" -> Parent owns X
        - Child says "owned by X" -> X owns Child
        """
        relationships: Dict[str, Set[str]] = {}
        concept_names_set = {c.get('name', '').lower() for c in domain_concepts}
        
        for concept in domain_concepts:
            concept_name = concept.get('name', '').lower()
            if not concept_name:
                continue
            
            for resp in concept.get('responsibilities', []):
                resp_name = resp.get('name', '').lower()
                collaborators = resp.get('collaborators', [])
                
                # Pattern 1: "owns X" - this concept owns the collaborator
                if 'owns' in resp_name and 'owned' not in resp_name:
                    for collab in collaborators:
                        collab_lower = collab.lower()
                        if collab_lower in concept_names_set and collab_lower != concept_name:
                            if concept_name not in relationships:
                                relationships[concept_name] = set()
                            relationships[concept_name].add(collab_lower)
                
                # Pattern 2: "owned by X" - the collaborator owns this concept
                elif 'owned by' in resp_name:
                    for collab in collaborators:
                        collab_lower = collab.lower()
                        if collab_lower in concept_names_set and collab_lower != concept_name:
                            if collab_lower not in relationships:
                                relationships[collab_lower] = set()
                            relationships[collab_lower].add(concept_name)
        
        return relationships

    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------
    
    def _find_domain_concepts_in_text(
        self,
        text: str,
        domain_concepts: List[Dict[str, Any]]
    ) -> Set[str]:
        """Find which domain concepts are mentioned in text."""
        found = set()
        text_lower = text.lower()
        
        for concept in domain_concepts:
            concept_name = concept.get('name', '').lower()
            if not concept_name:
                continue
            
            # Check if concept name appears in text
            if concept_name in text_lower:
                found.add(concept_name)
            # Also check plural
            if concept_name + 's' in text_lower:
                found.add(concept_name)
        
        return found
    
    def _find_domain_concepts_in_columns(
        self,
        columns: List[str],
        domain_concepts: List[Dict[str, Any]]
    ) -> Set[str]:
        """Find which domain concepts are represented in example columns."""
        found = set()
        
        concept_names = [c.get('name', '').lower() for c in domain_concepts if c.get('name')]
        
        for column in columns:
            column_lower = column.lower()
            column_parts = column_lower.split('_')
            
            for concept_name in concept_names:
                # Check if concept name is in column
                if concept_name in column_lower:
                    found.add(concept_name)
                # Check column parts
                for part in column_parts:
                    if part == concept_name or part == concept_name + 's':
                        found.add(concept_name)
        
        return found
