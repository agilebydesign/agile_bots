"""Base class for domain concept scanners."""

from abc import abstractmethod
from typing import List, Dict, Any, Optional
from .scanner import Scanner
from .story_map import StoryMap
from .domain_concept_node import DomainConceptNode


class DomainScanner(Scanner):
    """Base class for scanners that validate domain concepts.
    
    Domain scanners scan domain_concepts arrays in epics and sub_epics.
    They do NOT scan story/epic/sub-epic nodes themselves.
    """
    
    def scan(
        self, 
        knowledge_graph: Dict[str, Any], 
        rule_obj: Any = None,
        test_files: Optional[List['Path']] = None,
        code_files: Optional[List['Path']] = None,
        on_file_scanned: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        """Scan domain concepts in the story graph.
        
        Domain scanners ONLY scan domain concepts, not story/epic/sub-epic nodes.
        """
        if not rule_obj:
            raise ValueError("rule_obj parameter is required for DomainScanner")
        
        violations = []
        story_graph_data = knowledge_graph.get('story_graph', knowledge_graph)
        story_map = StoryMap(story_graph_data)
        
        # Domain scanners should ONLY scan domain concepts
        for epic in story_map.epics():
            # Scan domain concepts at epic level
            epic_violations = self._scan_domain_concepts(
                epic.data.get('domain_concepts', []),
                epic.epic_idx,
                None,
                rule_obj
            )
            violations.extend(epic_violations)
            
            # Walk through sub_epics to find domain concepts
            for node in story_map.walk(epic):
                if hasattr(node, 'data') and 'domain_concepts' in node.data:
                    sub_epic_violations = self._scan_domain_concepts(
                        node.data.get('domain_concepts', []),
                        epic.epic_idx,
                        getattr(node, 'sub_epic_path', None),
                        rule_obj
                    )
                    violations.extend(sub_epic_violations)
        
        return violations
    
    def _scan_domain_concepts(
        self,
        domain_concepts: List[Dict[str, Any]],
        epic_idx: int,
        sub_epic_path: Optional[List[int]],
        rule_obj: Any
    ) -> List[Dict[str, Any]]:
        """Helper method to scan a list of domain concepts."""
        violations = []
        
        for concept_idx, concept_data in enumerate(domain_concepts):
            domain_concept_node = DomainConceptNode(
                concept_data,
                epic_idx,
                sub_epic_path,
                concept_idx
            )
            
            # Scan the domain concept
            concept_violations = self.scan_domain_concept(domain_concept_node, rule_obj)
            violations.extend(concept_violations)
        
        return violations
    
    @abstractmethod
    def scan_domain_concept(self, node: DomainConceptNode, rule_obj: Any) -> List[Dict[str, Any]]:
        """Scan a single domain concept for violations.
        
        This method must be implemented by domain scanners.
        """
        pass




