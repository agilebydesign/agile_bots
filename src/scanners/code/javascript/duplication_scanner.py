"""Scanner for detecting code duplication in JavaScript files."""

from typing import List, Dict, Any, Set
from pathlib import Path
from datetime import datetime
from scanners.code.javascript.js_code_scanner import JSCodeScanner
from scanners.resources.violation import Violation
from scanners.resources.scan_context import ScanFilesContext, FileScanContext
import difflib


class DuplicationScanner(JSCodeScanner):
    """Detects duplicate code blocks and functions in JavaScript files."""
    
    SIMILARITY_THRESHOLD = 0.85  # 85% similarity triggers violation
    MIN_BLOCK_LINES = 5  # Minimum lines to consider for duplication
    
    def scan_with_context(self, context: ScanFilesContext) -> List[Dict[str, Any]]:
        """Scan all JavaScript files for duplicate code."""
        violations = []
        
        if not context.files:
            return violations
        
        # Get all JavaScript files from FileCollection
        all_files = context.files.all_files if hasattr(context.files, 'all_files') else []
        js_files = [f for f in all_files if str(f).endswith('.js')]
        
        if len(js_files) < 2:
            # Need at least 2 files to find duplications
            return violations
        
        # Extract functions from all files
        all_functions = {}
        for file_path in js_files:
            functions = self._extract_functions_from_file(file_path)
            if functions:
                all_functions[file_path] = functions
        
        # Check for duplicate functions across files
        for i, file1 in enumerate(js_files):
            for file2 in js_files[i+1:]:
                if file1 in all_functions and file2 in all_functions:
                    dupes = self._find_duplicate_functions(
                        all_functions[file1], 
                        all_functions[file2],
                        file1,
                        file2
                    )
                    violations.extend(dupes)
        
        return violations
    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a single JavaScript file for internal duplication."""
        violations = []
        
        if not context.exists or not str(context.file_path).endswith('.js'):
            return violations
        
        parsed = self._parse_js_file(context.file_path)
        if not parsed:
            return violations
        
        content, ast, lines = parsed
        
        # Extract functions
        functions = self._extract_functions_from_ast(ast, lines)
        
        # Check for duplicate functions within the same file
        for i, func1 in enumerate(functions):
            for func2 in functions[i+1:]:
                similarity = self._calculate_similarity(func1['body'], func2['body'])
                
                if similarity >= self.SIMILARITY_THRESHOLD:
                    violation = self._create_violation(
                        file_path=context.file_path,
                        line_number=func1['start_line'],
                        message=f"Duplicate function: '{func1['name']}' and '{func2['name']}' are {similarity:.0%} similar",
                        details={
                            'function_1': func1['name'],
                            'function_2': func2['name'],
                            'line_1': func1['start_line'],
                            'line_2': func2['start_line'],
                            'similarity': similarity
                        }
                    )
                    violations.append(violation)
        
        # Check for duplicate code blocks
        block_violations = self._find_duplicate_blocks(lines, context.file_path)
        violations.extend(block_violations)
        
        return violations
    
    def _extract_functions_from_file(self, file_path: Path) -> List[Dict]:
        """Extract all functions from a JavaScript file."""
        parsed = self._parse_js_file(file_path)
        if not parsed:
            return []
        
        content, ast, lines = parsed
        return self._extract_functions_from_ast(ast, lines)
    
    def _extract_functions_from_ast(self, ast: Dict, lines: List[str]) -> List[Dict]:
        """Extract function information from AST."""
        functions = []
        
        def visit_node(node, parent_name=None):
            if not isinstance(node, dict):
                return
            
            node_type = node.get('type')
            
            # Handle different function types
            if node_type in ('FunctionDeclaration', 'FunctionExpression', 'ArrowFunctionExpression', 'MethodDefinition'):
                func_info = self._extract_function_info(node, node_type, parent_name, lines)
                if func_info:
                    functions.append(func_info)
            
            # Variable declarations might contain functions
            elif node_type == 'VariableDeclarator':
                var_name = node.get('id', {}).get('name')
                if var_name:
                    visit_node(node.get('init'), var_name)
                    return
            
            # Recursively visit children
            for key, value in node.items():
                if isinstance(value, dict):
                    visit_node(value, parent_name)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            visit_node(item, parent_name)
        
        visit_node(ast)
        return functions
    
    def _extract_function_info(self, node: Dict, node_type: str, parent_name: str, lines: List[str]) -> Dict:
        """Extract function name, location, and body."""
        if node_type == 'FunctionDeclaration':
            name = node.get('id', {}).get('name', '<anonymous>')
        elif node_type == 'MethodDefinition':
            name = node.get('key', {}).get('name', '<method>')
            node = node.get('value', {})  # Get the actual function node
        elif node_type == 'ArrowFunctionExpression':
            name = parent_name or '<arrow>'
        else:  # FunctionExpression
            name = node.get('id', {}).get('name') or parent_name or '<anonymous>'
        
        loc = node.get('loc', {})
        start = loc.get('start', {}).get('line', 0)
        end = loc.get('end', {}).get('line', 0)
        
        if start == 0 or end == 0:
            return None
        
        # Get function body as text
        body_lines = lines[start-1:end]
        body = '\n'.join(body_lines)
        
        return {
            'name': name,
            'start_line': start,
            'end_line': end,
            'body': body,
            'type': node_type
        }
    
    def _find_duplicate_functions(
        self, 
        functions1: List[Dict], 
        functions2: List[Dict],
        file1: Path,
        file2: Path
    ) -> List[Dict[str, Any]]:
        """Find duplicate functions between two files."""
        violations = []
        
        for func1 in functions1:
            for func2 in functions2:
                similarity = self._calculate_similarity(func1['body'], func2['body'])
                
                if similarity >= self.SIMILARITY_THRESHOLD:
                    violation = self._create_violation(
                        file_path=file1,
                        line_number=func1['start_line'],
                        message=f"Duplicate function across files: '{func1['name']}' ({file1.name}:{func1['start_line']}) and '{func2['name']}' ({file2.name}:{func2['start_line']}) are {similarity:.0%} similar",
                        details={
                            'function_1': func1['name'],
                            'function_2': func2['name'],
                            'file_1': str(file1),
                            'file_2': str(file2),
                            'line_1': func1['start_line'],
                            'line_2': func2['start_line'],
                            'similarity': similarity
                        }
                    )
                    violations.append(violation)
        
        return violations
    
    def _find_duplicate_blocks(self, lines: List[str], file_path: Path) -> List[Dict[str, Any]]:
        """Find duplicate code blocks within a file."""
        violations = []
        
        # Create sliding window of code blocks
        for i in range(len(lines) - self.MIN_BLOCK_LINES):
            block1 = lines[i:i + self.MIN_BLOCK_LINES]
            block1_text = '\n'.join(block1).strip()
            
            if not block1_text or len(block1_text) < 20:
                continue
            
            # Compare with all subsequent blocks
            for j in range(i + self.MIN_BLOCK_LINES, len(lines) - self.MIN_BLOCK_LINES):
                block2 = lines[j:j + self.MIN_BLOCK_LINES]
                block2_text = '\n'.join(block2).strip()
                
                if not block2_text:
                    continue
                
                similarity = self._calculate_similarity(block1_text, block2_text)
                
                if similarity >= self.SIMILARITY_THRESHOLD:
                    violation = self._create_violation(
                        file_path=file_path,
                        line_number=i + 1,
                        message=f"Duplicate code block: lines {i+1}-{i+self.MIN_BLOCK_LINES} and {j+1}-{j+self.MIN_BLOCK_LINES} are {similarity:.0%} similar",
                        details={
                            'block_1_start': i + 1,
                            'block_1_end': i + self.MIN_BLOCK_LINES,
                            'block_2_start': j + 1,
                            'block_2_end': j + self.MIN_BLOCK_LINES,
                            'similarity': similarity
                        }
                    )
                    violations.append(violation)
                    break  # Only report first duplicate for each block
        
        return violations
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity ratio between two text blocks."""
        if not text1 or not text2:
            return 0.0
        
        # Normalize whitespace
        text1 = ' '.join(text1.split())
        text2 = ' '.join(text2.split())
        
        # Use difflib's SequenceMatcher
        matcher = difflib.SequenceMatcher(None, text1, text2)
        return matcher.ratio()
