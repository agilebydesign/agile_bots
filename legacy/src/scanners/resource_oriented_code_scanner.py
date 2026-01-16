"""Scanner for validating resource-oriented design in code."""

from typing import List, Dict, Any, Optional, Set, Tuple
from pathlib import Path
import ast
import re
import logging
from .code_scanner import CodeScanner
from .violation import Violation
from .resources.ast_elements import Classes
from .vocabulary_helper import VocabularyHelper

logger = logging.getLogger(__name__)


class ResourceOrientedCodeScanner(CodeScanner):
    """
    Validates that code classes are named after resources (what they ARE)
    rather than actions (what they DO).
    
    Uses NLTK to detect agent nouns (Manager, Loader, Handler, etc.)
    """
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, knowledge_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        # No violations in single-file scan - all checking happens in cross-file scan
        return []
    
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
        violations = []
        
        all_files = []
        if code_files:
            all_files.extend(code_files)
        if test_files:
            all_files.extend(test_files)
        
        if not all_files:
            return violations
        
        # First pass: collect all loader/manager classes and all classes
        loader_classes = {}  # class_name -> (file_path, class_node, pattern)
        all_classes = {}  # (file_path, class_name) -> class_node
        
        for file_path in all_files:
            if not file_path.exists():
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8')
                tree = ast.parse(content, filename=str(file_path))
                
                classes = Classes(tree)
                for cls in classes.get_many_classes:
                    all_classes[(file_path, cls.node.name)] = cls.node
                    
                    # Check if class name is an agent noun using NLTK
                    is_agent, base_verb, suffix = VocabularyHelper.is_agent_noun(cls.node.name)
                    if is_agent:
                        loader_classes[cls.node.name] = (file_path, cls.node, suffix)
            except (SyntaxError, UnicodeDecodeError) as e:
                logger.debug(f'Skipping file {file_path} due to {type(e).__name__}: {e}')
                continue
        
        # Second pass: check if each agent noun class is owned by a domain object
        for loader_class_name, (loader_file, loader_node, suffix) in loader_classes.items():
            if not self._is_owned_by_domain_object(loader_class_name, loader_node, all_files, all_classes):
                suggested_name = loader_class_name[:-len(suffix)] if loader_class_name.endswith(suffix) else loader_class_name
                # No code snippet for class-level design violations (class definition line)
                violation = Violation(
                    rule=rule_obj,
                    violation_message=f'Class "{loader_class_name}" is an agent noun (doer of action) but is not owned by a domain object. Use resource-oriented design instead (e.g., make it a property of a domain object like "{suggested_name}").',
                    location=str(loader_file),
                    line_number=loader_node.lineno,
                    severity='error'
                ).to_dict()
                violations.append(violation)
        
        return violations
    
    def _is_owned_by_domain_object(
        self, 
        loader_class_name: str, 
        loader_node: ast.ClassDef,
        all_files: List[Path],
        all_classes: Dict[Tuple[Path, str], ast.ClassDef]
    ) -> bool:
        for (file_path, class_name), class_node in all_classes.items():
            # Skip the loader class itself
            if class_node == loader_node:
                continue
            
            if self._class_uses_as_attribute(class_node, loader_class_name, file_path):
                return True
        
        return False
    
    def _class_uses_as_attribute(self, class_node: ast.ClassDef, loader_class_name: str, file_path: Path) -> bool:
        try:
            content = file_path.read_text(encoding='utf-8')
            # Simple check: see if loader class name appears in the file
            if loader_class_name not in content:
                return False
        except (UnicodeDecodeError, IOError):
            return False
        
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef) and node.name == '__init__':
                for stmt in ast.walk(node):
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if isinstance(target, ast.Attribute):
                                if isinstance(target.value, ast.Name) and target.value.id == 'self':
                                    if isinstance(stmt.value, ast.Call):
                                        if isinstance(stmt.value.func, ast.Name) and stmt.value.func.id == loader_class_name:
                                            return True
                                        if isinstance(stmt.value.func, ast.Attribute):
                                            if isinstance(stmt.value.func.attr, str) and stmt.value.func.attr == loader_class_name:
                                                return True
                                    # Also check for direct assignment: self.loader = LoaderClass
                                    if isinstance(stmt.value, ast.Name) and stmt.value.id == loader_class_name:
                                        return True
            
            if isinstance(node, ast.AnnAssign):
                if isinstance(node.annotation, ast.Name) and node.annotation.id == loader_class_name:
                    return True
                if isinstance(node.target, ast.Attribute):
                    if isinstance(node.target.value, ast.Name) and node.target.value.id == 'self':
                        if isinstance(node.annotation, ast.Name) and node.annotation.id == loader_class_name:
                            return True
                        if isinstance(node.annotation, ast.Attribute):
                            if node.annotation.attr == loader_class_name:
                                return True
            
            if isinstance(node, ast.FunctionDef):
                is_property = any(
                    isinstance(dec, ast.Name) and dec.id == 'property'
                    for dec in node.decorator_list
                )
                if is_property:
                    if node.returns:
                        if isinstance(node.returns, ast.Name) and node.returns.id == loader_class_name:
                            return True
                        if isinstance(node.returns, ast.Attribute):
                            if node.returns.attr == loader_class_name:
                                return True
        
        return False
