from abc import abstractmethod
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from .scanner import Scanner
from .story_map import StoryMap, StoryNode, StoryGroup
from .domain_concept_node import DomainConceptNode


class StoryScanner(Scanner):
    
    def scan(
        self, 
        knowledge_graph: Dict[str, Any], 
        rule_obj: Any = None,
        test_files: Optional[List['Path']] = None,
        code_files: Optional[List['Path']] = None,
        on_file_scanned: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        if not rule_obj:
            raise ValueError("rule_obj parameter is required for StoryScanner")
        
        violations = []
        story_graph_data = knowledge_graph.get('story_graph', knowledge_graph)
        story_map = StoryMap(story_graph_data)
        
        # Story scanners should only scan story/epic/sub-epic nodes, NOT domain concepts
        # Domain concepts are validated by domain-specific scanners that override scan_domain_concept()
        # If a scanner needs to scan domain concepts, it should override scan() to call _scan_domain_concepts()
        
        for epic in story_map.epics():
            # Walk through all nodes (including sub_epics)
            for node in story_map.walk(epic):
                # Scan story nodes only
                if not isinstance(node, StoryGroup):
                    node_violations = self.scan_story_node(node, rule_obj)
                    violations.extend(node_violations)
        
        return violations
    
    def _scan_domain_concepts(
        self,
        domain_concepts: List[Dict[str, Any]],
        epic_idx: int,
        sub_epic_path: Optional[List[int]],
        rule_obj: Any
    ) -> List[Dict[str, Any]]:
        violations = []
        
        for concept_idx, concept_data in enumerate(domain_concepts):
            concept_name = concept_data.get('name', '')
            responsibilities = concept_data.get('responsibilities', [])
            
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
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        pass
    
    def scan_domain_concept(self, node: 'DomainConceptNode', rule_obj: Any) -> List[Dict[str, Any]]:
        # Story scanners should NOT scan domain concepts by default
        # Domain concepts are validated by domain-specific scanners, not story scanners
        # Override this method if a scanner needs to validate domain concepts
        return []

