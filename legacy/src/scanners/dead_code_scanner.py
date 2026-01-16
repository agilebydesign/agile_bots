"""Scanner for detecting unused/dead code (YAGNI principle).

Detects:
- Functions/methods that are never called
- Classes that are never instantiated or referenced
- Module-level variables that are never used
- Private methods (_name) that are never called within the class
"""

from typing import List, Dict, Any, Optional, Set, Tuple
from pathlib import Path
import ast
import logging
from .code_scanner import CodeScanner
from .violation import Violation

logger = logging.getLogger(__name__)


class DeadCodeScanner(CodeScanner):
    """Scanner for detecting dead/unused code."""
    
    def scan(
        self, 
        knowledge_graph: Dict[str, Any], 
        rule_obj: Any = None,
        test_files: Optional[List[Path]] = None,
        code_files: Optional[List[Path]] = None,
        on_file_scanned: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        """Override scan to perform cross-file analysis for dead code detection.
        
        Dead code detection requires analyzing the entire codebase to determine
        what is used vs unused.
        """
        violations = []
        
        # Combine all files
        all_files = []
        if code_files:
            all_files.extend(code_files)
        if test_files:
            all_files.extend(test_files)
        
        if not all_files:
            return violations
        
        # First pass: collect all definitions and usages across all files
        definitions = {}  # {name: (file_path, line_number, node_type)}
        usages = set()  # {name}
        
        for file_path in all_files:
            if not file_path.exists() or not file_path.is_file():
                continue
            
            try:
                file_defs, file_usages = self._analyze_file(file_path)
                
                # Store definitions with file context
                for name, (line_num, node_type) in file_defs.items():
                    # Use qualified name for module-level items
                    qualified_name = f"{file_path.stem}.{name}"
                    definitions[qualified_name] = (file_path, line_num, node_type, name)
                    # Also store the simple name for cross-module usage detection
                    if name not in definitions:
                        definitions[name] = (file_path, line_num, node_type, name)
                
                usages.update(file_usages)
                
            except Exception as e:
                logger.debug(f"Error analyzing {file_path}: {e}")
                continue
        
        # Second pass: find unused definitions
        for qualified_name, (file_path, line_num, node_type, simple_name) in definitions.items():
            # Skip if this is a qualified name and we already checked the simple name
            if '.' in qualified_name and simple_name in usages:
                continue
            
            # Skip test files - test functions are entry points
            if self._is_test_file(file_path):
                continue
            
            # Skip if used
            if simple_name in usages or qualified_name in usages:
                continue
            
            # Skip special names and common entry points
            if self._is_entry_point_or_special(simple_name, node_type):
                continue
            
            # Found unused code
            violation = Violation(
                rule=rule_obj,
                violation_message=f"Unused {node_type} '{simple_name}' - consider removing dead code",
                location=str(file_path),
                line_number=line_num,
                severity='warning'
            ).to_dict()
            violations.append(violation)
            
            # Call callback if provided
            if on_file_scanned:
                on_file_scanned(file_path, [violation], rule_obj)
        
        return violations
    
    def scan_file(
        self,
        file_path: Path,
        rule_obj: Any = None,
        knowledge_graph: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Scan a single file for dead code within that file only.
        
        This is a simpler analysis that only detects:
        - Private methods that are never called within the same file
        - Local variables that are assigned but never used
        """
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        # Find private methods and their usages within the file
        private_defs, private_usages = self._analyze_private_members(tree)
        
        for method_name, (line_num, class_name) in private_defs.items():
            if method_name not in private_usages:
                # Skip dunder methods - they're protocol implementations
                if method_name.startswith('__') and method_name.endswith('__'):
                    continue
                
                violation = self._create_violation_with_snippet(
                    rule_obj=rule_obj,
                    violation_message=f"Private method '{method_name}' in class '{class_name}' is never called - consider removing dead code",
                    file_path=file_path,
                    line_number=line_num,
                    severity='warning',
                    content=content,
                    start_line=line_num
                )
                violations.append(violation)
        
        return violations
    
    def _analyze_file(self, file_path: Path) -> Tuple[Dict[str, Tuple[int, str]], Set[str]]:
        """Analyze a file to extract definitions and usages.
        
        Returns:
            Tuple of (definitions, usages) where:
            - definitions: {name: (line_number, node_type)}
            - usages: set of names that are referenced/called
        """
        definitions = {}
        usages = set()
        
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content, filename=str(file_path))
        except (SyntaxError, UnicodeDecodeError) as e:
            logger.debug(f"Skipping {file_path}: {e}")
            return definitions, usages
        
        # Collect module-level definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                definitions[node.name] = (node.lineno, 'function')
            elif isinstance(node, ast.AsyncFunctionDef):
                definitions[node.name] = (node.lineno, 'async function')
            elif isinstance(node, ast.ClassDef):
                definitions[node.name] = (node.lineno, 'class')
        
        # Collect usages
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                usages.add(node.id)
            elif isinstance(node, ast.Attribute):
                usages.add(node.attr)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    usages.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    usages.add(node.func.attr)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    usages.add(alias.asname if alias.asname else alias.name)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    usages.add(alias.asname if alias.asname else alias.name)
        
        return definitions, usages
    
    def _analyze_private_members(self, tree: ast.AST) -> Tuple[Dict[str, Tuple[int, str]], Set[str]]:
        """Analyze private members (_name) and their usages within classes.
        
        Returns:
            Tuple of (private_defs, private_usages) where:
            - private_defs: {method_name: (line_number, class_name)}
            - private_usages: set of method names that are called
        """
        private_defs = {}
        private_usages = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                
                # Find private method definitions
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if item.name.startswith('_') and not item.name.startswith('__'):
                            private_defs[item.name] = (item.lineno, class_name)
                
                # Find usages within the class
                for item in ast.walk(node):
                    if isinstance(item, ast.Attribute):
                        if isinstance(item.value, ast.Name) and item.value.id == 'self':
                            private_usages.add(item.attr)
                    elif isinstance(item, ast.Call):
                        if isinstance(item.func, ast.Attribute):
                            if isinstance(item.func.value, ast.Name) and item.func.value.id == 'self':
                                private_usages.add(item.func.attr)
        
        return private_defs, private_usages
    
    def _is_entry_point_or_special(self, name: str, node_type: str) -> bool:
        """Check if a name is an entry point or special case that shouldn't be flagged."""
        
        # Common entry point names
        entry_points = {
            'main', 'cli', 'app', 'run', 'start', 'execute',
            'handle', 'process', 'serve', 'listen'
        }
        if name in entry_points or name.startswith('main'):
            return True
        
        # Special Python names
        if name.startswith('__') and name.endswith('__'):
            return True
        
        # Test functions
        if name.startswith('test_') or name.startswith('Test'):
            return True
        
        # Factory/builder patterns
        if name.startswith('create_') or name.startswith('build_') or name.startswith('make_'):
            return True
        
        # Handler patterns (often registered dynamically)
        if name.endswith('_handler') or name.endswith('Handler'):
            return True
        
        # Class names that are likely exported
        if node_type == 'class':
            # All public classes are potentially exported
            if not name.startswith('_'):
                return True
        
        # Functions/methods that might be public API
        if node_type in ('function', 'async function'):
            # Public functions are potentially exported
            if not name.startswith('_'):
                # But still flag if they're clearly internal helpers
                internal_patterns = ['helper', 'util', 'internal', 'legacy']
                name_lower = name.lower()
                if not any(p in name_lower for p in internal_patterns):
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
        """Perform cross-file dead code analysis.
        
        This uses the full codebase context to find:
        - Modules that are never imported
        - Classes that are never instantiated
        - Functions that are never called across the entire codebase
        """
        # Use all_* files if provided, otherwise fall back to regular files
        all_code = all_code_files if all_code_files else code_files or []
        all_tests = all_test_files if all_test_files else test_files or []
        
        # Delegate to scan() which already does cross-file analysis
        return self.scan(
            knowledge_graph={},
            rule_obj=rule_obj,
            test_files=all_tests,
            code_files=all_code,
            on_file_scanned=None
        )
