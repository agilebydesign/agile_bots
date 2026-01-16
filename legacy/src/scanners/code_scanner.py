"""Base CodeScanner class for validating source code files."""

from abc import abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path  # Needed at runtime for Path operations
import ast
from .scanner import Scanner
from .violation import Violation


class CodeScanner(Scanner):
    
    def scan(
        self, 
        knowledge_graph: Dict[str, Any], 
        rule_obj: Any = None,
        test_files: Optional[List['Path']] = None,
        code_files: Optional[List['Path']] = None,
        on_file_scanned: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        if not rule_obj:
            raise ValueError("rule_obj parameter is required for CodeScanner")
        
        # Use base Scanner.scan() which combines files and calls scan_file() for each
        violations = super().scan(knowledge_graph, rule_obj, test_files, code_files, on_file_scanned=on_file_scanned)
        return violations
    
    def scan_file(
        self,
        file_path: Path,
        rule_obj: Any = None,
        knowledge_graph: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        if not rule_obj:
            raise ValueError("rule_obj parameter is required for CodeScanner")
        
        # Store knowledge_graph in instance for scanners that need it
        # Assign directly - let AttributeError propagate if self doesn't support it
        self.knowledge_graph = knowledge_graph
        
        # Default implementation - subclasses must override
        return []
    
    def _extract_domain_terms(self, knowledge_graph: Dict[str, Any]) -> set:
        domain_terms = set()
        
        # These are domain concepts, not technical jargon
        common_domain_terms = {
            'json', 'data', 'param', 'params', 'parameter', 'parameters',
            'var', 'vars', 'variable', 'variables',
            'method', 'methods', 'class', 'classes', 'call', 'calls',
            'config', 'configuration', 'configurations',
            'agent', 'bot', 'workflow', 'story', 'epic', 'scenario', 'action',
            'behavior', 'rule', 'rules', 'validation', 'validate', 'scanner',
            'file', 'files', 'directory', 'directories', 'path', 'paths',
            'state', 'states', 'tool', 'tools', 'server', 'catalog', 'metadata'
        }
        domain_terms.update(common_domain_terms)
        
        if not knowledge_graph:
            return domain_terms
        
        epics = knowledge_graph.get('epics', [])
        for epic in epics:
            if isinstance(epic, dict):
                epic_name = epic.get('name', '')
                if epic_name:
                    domain_terms.update(self._extract_words_from_text(epic_name))
                
                domain_concepts = epic.get('domain_concepts', [])
                for concept in domain_concepts:
                    if isinstance(concept, dict):
                        concept_name = concept.get('name', '')
                        if concept_name:
                            domain_terms.add(concept_name.lower())
                            domain_terms.add(concept_name.lower().replace(' ', '_'))
                            domain_terms.update(self._extract_words_from_text(concept_name))
                            
                            responsibilities = concept.get('responsibilities', [])
                            for resp in responsibilities:
                                if isinstance(resp, dict):
                                    resp_name = resp.get('name', '')
                                    if resp_name:
                                        domain_terms.update(self._extract_words_from_text(resp_name))
                            
                            collaborators = concept.get('collaborators', [])
                            for collab in collaborators:
                                if isinstance(collab, str):
                                    domain_terms.add(collab.lower())
                                    domain_terms.update(self._extract_words_from_text(collab))
                
                sub_epics = epic.get('sub_epics', [])
                for sub_epic in sub_epics:
                    if isinstance(sub_epic, dict):
                        sub_epic_name = sub_epic.get('name', '')
                        if sub_epic_name:
                            domain_terms.update(self._extract_words_from_text(sub_epic_name))
                        
                        # Extract from domain_concepts in sub_epic - CRITICAL: Must extract all domain terms
                        sub_epic_concepts = sub_epic.get('domain_concepts', [])
                        for concept in sub_epic_concepts:
                            if isinstance(concept, dict):
                                concept_name = concept.get('name', '')
                                if concept_name:
                                    domain_terms.add(concept_name.lower())
                                    domain_terms.add(concept_name.lower().replace(' ', '_'))
                                    domain_terms.update(self._extract_words_from_text(concept_name))
                                    
                                    responsibilities = concept.get('responsibilities', [])
                                    for resp in responsibilities:
                                        if isinstance(resp, dict):
                                            resp_name = resp.get('name', '')
                                            if resp_name:
                                                domain_terms.update(self._extract_words_from_text(resp_name))
                                    
                                    collaborators = concept.get('collaborators', [])
                                    for collab in collaborators:
                                        if isinstance(collab, str):
                                            domain_terms.add(collab.lower())
                                            domain_terms.update(self._extract_words_from_text(collab))
                        
                        story_groups = sub_epic.get('story_groups', [])
                        for story_group in story_groups:
                            if isinstance(story_group, dict):
                                stories = story_group.get('stories', [])
                                for story in stories:
                                    if isinstance(story, dict):
                                        story_name = story.get('name', '')
                                        if story_name:
                                            domain_terms.update(self._extract_words_from_text(story_name))
                                        
                                        acceptance_criteria = story.get('acceptance_criteria', [])
                                        for ac in acceptance_criteria:
                                            if isinstance(ac, dict):
                                                ac_text = ac.get('criterion', '')
                                                if ac_text:
                                                    domain_terms.update(self._extract_words_from_text(ac_text))
                                            elif isinstance(ac, str):
                                                domain_terms.update(self._extract_words_from_text(ac))
                                        
                                        scenarios = story.get('scenarios', [])
                                        for scenario in scenarios:
                                            if isinstance(scenario, dict):
                                                steps = scenario.get('steps', [])
                                                for step in steps:
                                                    if isinstance(step, str):
                                                        domain_terms.update(self._extract_words_from_text(step))
        
        return domain_terms
    
    def _extract_words_from_text(self, text: str) -> set:
        if not text:
            return set()
        
        import re
        # Split on spaces, underscores, hyphens, and other separators
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        return set(words)
    
    def _matches_domain_term(self, name: str, domain_terms: set) -> bool:
        if not name or not domain_terms:
            return False
        
        name_lower = name.lower()
        
        name_words = self._extract_words_from_text(name)
        
        for domain_term in domain_terms:
            if domain_term in name_words:
                return True
            # e.g., "assigned_strategy" contains "strategy", "template_manager" contains "template"
            if domain_term in name_lower or name_lower in domain_term:
                return True
        
        return False
    
    def scan_cross_file(
        self,
        rule_obj: Any = None,
        test_files: Optional[List[Path]] = None,
        code_files: Optional[List[Path]] = None,
        all_test_files: Optional[List[Path]] = None,
        all_code_files: Optional[List[Path]] = None,
        status_writer: Optional[Any] = None,
        max_cross_file_comparisons: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        # Default implementation - subclasses override
        return []
    
    def _parse_code_file(self, file_path: Path) -> Optional[Tuple[str, ast.AST]]:
        if not file_path.exists():
            return None
        
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content, filename=str(file_path))
            return (content, tree)
        except (SyntaxError, UnicodeDecodeError):
            return None
    
    def _read_and_parse_file(self, file_path: Path) -> Optional[Tuple[str, List[str], ast.AST]]:
        import logging
        logger = logging.getLogger(__name__)
        
        if not file_path.exists():
            return None
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            tree = ast.parse(content, filename=str(file_path))
            return (content, lines, tree)
        except (SyntaxError, UnicodeDecodeError) as e:
            logger.debug(f'Skipping file {file_path} due to {type(e).__name__}: {e}')
            return None
    
    def _get_all_code_files_parsed(
        self, 
        test_files: Optional[List[Path]] = None,
        code_files: Optional[List[Path]] = None
    ) -> List[Tuple[Path, str, ast.AST]]:
        parsed_files = []
        all_files = []
        if code_files:
            all_files.extend(code_files)
        if test_files:
            all_files.extend(test_files)
        
        for file_path in all_files:
            parsed = self._parse_code_file(file_path)
            if parsed:
                content, tree = parsed
                parsed_files.append((file_path, content, tree))
        
        return parsed_files
    
    def _extract_code_snippet(self, content: str, ast_node: Optional[ast.AST] = None, 
                             start_line: Optional[int] = None, end_line: Optional[int] = None,
                             context_before: int = 2, max_lines: int = 50) -> str:
        lines = content.split('\n')
        
        # Determine start and end lines
        if ast_node is not None:
            # Use AST node to determine lines
            start_line_0 = ast_node.lineno - 1 if hasattr(ast_node, 'lineno') and ast_node.lineno else 0
            
            if hasattr(ast_node, 'end_lineno') and ast_node.end_lineno:
                end_line_0 = ast_node.end_lineno  # end_lineno is 1-indexed, exclusive
            else:
                # Estimate end by finding the maximum line number in the subtree
                end_line_0 = start_line_0 + 1
                for node in ast.walk(ast_node):
                    if hasattr(node, 'lineno') and node.lineno:
                        end_line_0 = max(end_line_0, node.lineno)
        elif start_line is not None:
            # Use provided line numbers (1-indexed, convert to 0-indexed)
            start_line_0 = start_line - 1
            if end_line is not None:
                end_line_0 = end_line  # end_line is 1-indexed, exclusive (like end_lineno)
            else:
                end_line_0 = start_line_0 + 1
        else:
            # No information provided, return empty
            return ""
        
        snippet_start = max(0, start_line_0 - context_before)
        snippet_end = min(len(lines), end_line_0 + 1)
        code_snippet = '\n'.join(lines[snippet_start:snippet_end])
        
        # Truncate if too long
        code_lines = code_snippet.split('\n')
        if len(code_lines) > max_lines:
            code_snippet = '\n'.join(code_lines[:max_lines]) + '\n    # ... (truncated)'
        
        return code_snippet
    
    def _create_violation_with_snippet(
        self, 
        rule_obj: Any,
        violation_message: str,
        file_path: Path,
        line_number: Optional[int] = None,
        severity: str = 'warning',
        content: Optional[str] = None,
        ast_node: Optional[ast.AST] = None,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
        context_before: int = 2,
        max_lines: int = 50
    ) -> Dict[str, Any]:
        from .violation import Violation
        
        code_snippet = ""
        if content is not None:
            if ast_node is not None or start_line is not None:
                code_snippet = self._extract_code_snippet(
                    content=content,
                    ast_node=ast_node,
                    start_line=start_line,
                    end_line=end_line,
                    context_before=context_before,
                    max_lines=max_lines
                )
        
        if code_snippet:
            final_message = f"{violation_message}\n\n```python\n{code_snippet}\n```"
        else:
            final_message = violation_message
        
        return Violation(
            rule=rule_obj,
            violation_message=final_message,
            location=str(file_path),
            line_number=line_number,
            severity=severity
        ).to_dict()

