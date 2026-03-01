
from typing import List, Dict, Any, Optional, Set
from scanners.domain_scanner import DomainScanner
from scanners.domain_concept_node import DomainConceptNode
from scanners.story_map import StoryMap
from scanners.violation import Violation

PRIMITIVES = {'String', 'Number', 'Boolean', 'Date', 'Integer'}


def _is_primitive(name: str) -> bool:
    return name.strip() in PRIMITIVES


def _collect_concepts_index(story_map: StoryMap) -> Dict[str, Dict[str, Any]]:
    """Build concept_name -> {data, epic_idx, sub_epic_path, concept_idx, collaborators_set}."""
    index: Dict[str, Dict[str, Any]] = {}

    for epic in story_map.epics():
        for node in story_map.walk(epic):
            if not hasattr(node, 'data') or 'domain_concepts' not in node.data:
                continue
            sub_epic_path = getattr(node, 'sub_epic_path', None)
            if sub_epic_path is None:
                sub_epic_path = []
            for concept_idx, concept_data in enumerate(node.data.get('domain_concepts', [])):
                name = concept_data.get('name', '')
                if not name:
                    continue
                collaborators_set: Set[str] = set()
                for resp in concept_data.get('responsibilities', []):
                    for c in resp.get('collaborators', []):
                        cn = (c if isinstance(c, str) else str(c)).strip()
                        if cn and not _is_primitive(cn):
                            collaborators_set.add(cn)
                index[name] = {
                    'data': concept_data,
                    'epic_idx': epic.epic_idx,
                    'sub_epic_path': sub_epic_path if sub_epic_path else None,
                    'concept_idx': concept_idx,
                    'collaborators_set': collaborators_set,
                }

    return index


def _map_location(epic_idx: int, sub_epic_path: Optional[List[int]], concept_idx: int, field: str = 'name') -> str:
    path_parts = [f'epics[{epic_idx}]']
    if sub_epic_path:
        for idx in sub_epic_path:
            path_parts.append(f'sub_epics[{idx}]')
    path_parts.append(f'domain_concepts[{concept_idx}]')
    if field != 'name':
        path_parts.append(field)
    return '.'.join(path_parts)


class BidirectionalCollaboratorScanner(DomainScanner):
    """Scanner for Map Bidirectional Collaborators rule.
    Ensures non-primitive collaborators are referenced back by the collaborator concept.
    """

    def scan(
        self,
        story_graph: Dict[str, Any] = None,
        test_files: Optional[List] = None,
        code_files: Optional[List] = None,
        on_file_scanned: Optional[Any] = None,
    ) -> List[Dict[str, Any]]:
        if not self.rule:
            raise ValueError('self.rule parameter is required for DomainScanner')

        violations = []
        story_graph_data = story_graph.get('story_graph', story_graph)
        story_map = StoryMap(story_graph_data)
        index = _collect_concepts_index(story_map)

        for concept_name, entry in index.items():
            concept_data = entry['data']
            epic_idx = entry['epic_idx']
            sub_epic_path = entry['sub_epic_path']
            concept_idx = entry['concept_idx']
            collaborators_set = entry['collaborators_set']

            for resp_idx, resp_data in enumerate(concept_data.get('responsibilities', [])):
                resp_name = resp_data.get('name', '')
                collaborators = resp_data.get('collaborators', [])

                for i, collab in enumerate(collaborators):
                    collab_name = (collab if isinstance(collab, str) else str(collab)).strip()
                    if not collab_name or _is_primitive(collab_name):
                        continue
                    if collab_name not in index:
                        continue

                    other_entry = index[collab_name]
                    other_collaborators = other_entry['collaborators_set']

                    if concept_name not in other_collaborators:
                        location = _map_location(
                            epic_idx, sub_epic_path, concept_idx,
                            f'responsibilities[{resp_idx}].collaborators'
                        )
                        violations.append(
                            Violation(
                                rule=self.rule,
                                violation_message=(
                                    f'Concept "{concept_name}" references "{collab_name}" in responsibility '
                                    f'"{resp_name}", but "{collab_name}" does not reference "{concept_name}" back. '
                                    f'Add a responsibility on "{collab_name}" that references "{concept_name}".'
                                ),
                                location=location,
                                line_number=None,
                                severity='warning',
                            ).to_dict()
                        )

        return violations

    def scan_domain_concept(self, node: DomainConceptNode) -> List[Dict[str, Any]]:
        """Not used; logic is in overridden scan()."""
        return []
