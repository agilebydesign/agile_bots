"""
Python Analyzer - finds direct references using AST.
"""
import ast
import textwrap
from pathlib import Path
from typing import List, Set


class ReferenceVisitor(ast.NodeVisitor):
    """Collect=-s all function/method calls, class instantiations, and imports."""
    
    def __init__(self):
        self.calls: List[str] = []          # Function/method names
        self.classes: List[str] = []         # Class instantiations
        self.imports: List[tuple] = []       # (module, name) pairs

    def visit_Call(self, node):
        """Capture function/method calls and class instantiations."""
        if isinstance(node.func, ast.Name):
            name = node.func.id
            # Heuristic: CamelCase = class instantiation
            if name[0].isupper():
                self.classes.append(name)
            else:
                self.calls.append(name)
        elif isinstance(node.func, ast.Attribute):
            self.calls.append(node.func.attr)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append((alias.name, alias.asname or alias.name.split('.')[-1]))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            for alias in node.names:
                self.imports.append((f"{node.module}.{alias.name}", alias.asname or alias.name))
        self.generic_visit(node)


class PythonAnalyzer:
    """Analyzes Python code for references."""

    def find_references(self, source: str, start_line: int, end_line: int, index) -> List[dict]:
        """Find all direct references within a code block."""
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []
        
        # First get imports from the whole file
        file_visitor = ReferenceVisitor()
        file_visitor.visit(tree)
        
        # Build import map: local_name -> module_path
        import_map = {}
        for full_path, local_name in file_visitor.imports:
            import_map[local_name] = full_path
        
        # Extract just the lines we care about and dedent
        lines = source.split('\n')
        block_source = '\n'.join(lines[start_line - 1:end_line])
        block_source = textwrap.dedent(block_source)
        
        try:
            block_tree = ast.parse(block_source)
        except SyntaxError:
            return []
        
        visitor = ReferenceVisitor()
        visitor.visit(block_tree)
        
        # Resolve to actual symbols in the index
        refs = []
        seen: Set[str] = set()
        
        # Look up class instantiations (most valuable)
        for class_name in visitor.classes:
            if class_name in seen:
                continue
            seen.add(class_name)
            
            matches = index.find_symbol(class_name)
            for match in matches:
                refs.append({
                    "kind": "code",
                    "lang": "python",
                    "filePath": match["filePath"],
                    "symbol": match["name"],
                    "range": match["range"],
                    "refType": "class"
                })
        
        # Look up method calls that match indexed functions/methods
        for call_name in visitor.calls:
            if call_name in seen:
                continue
            seen.add(call_name)
            
            matches = index.find_symbol(call_name)
            for match in matches:
                refs.append({
                    "kind": "code",
                    "lang": "python",
                    "filePath": match["filePath"],
                    "symbol": match["name"],
                    "range": match["range"],
                    "refType": "call"
                })
        
        return refs
