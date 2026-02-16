"""
Workspace Index - indexes Python/JS files for symbol lookup.
"""
import ast
from pathlib import Path
from typing import Dict, List


class WorkspaceIndex:
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.files: List[Path] = []
        self.symbols: Dict[str, List[dict]] = {}  # path → [symbols]

    def build(self):
        """Build index of all Python and JS files."""
        self.files = []
        self.symbols = {}
        
        for pattern in ["**/*.py", "**/*.js"]:
            for file_path in self.workspace.glob(pattern):
                if self._should_index(file_path):
                    self.files.append(file_path)
                    self._index_file(file_path)

    def _should_index(self, file_path: Path) -> bool:
        """Skip external/generated code."""
        excludes = ["node_modules", ".venv", "site-packages", "__pycache__", ".git"]
        return not any(ex in str(file_path) for ex in excludes)

    def _index_file(self, file_path: Path):
        """Extract symbols from a file."""
        rel_path = str(file_path.relative_to(self.workspace)).replace("\\", "/")
        
        if file_path.suffix == ".py":
            self._index_python(file_path, rel_path)
        elif file_path.suffix == ".js":
            self._index_javascript(file_path, rel_path)

    def _index_python(self, file_path: Path, rel_path: str):
        """Index Python file using AST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            tree = ast.parse(source)
        except (SyntaxError, UnicodeDecodeError):
            return
        
        symbols = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                symbols.append({
                    "kind": "class",
                    "name": node.name,
                    "parent": None,
                    "range": {
                        "startLine": node.lineno,
                        "startCol": node.col_offset,
                        "endLine": node.end_lineno or node.lineno,
                        "endCol": node.end_col_offset or 0
                    }
                })
                # Index methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        symbols.append({
                            "kind": "method",
                            "name": item.name,
                            "parent": node.name,
                            "range": {
                                "startLine": item.lineno,
                                "startCol": item.col_offset,
                                "endLine": item.end_lineno or item.lineno,
                                "endCol": item.end_col_offset or 0
                            }
                        })
            
            elif isinstance(node, ast.FunctionDef) and not hasattr(node, '_in_class'):
                # Top-level function
                symbols.append({
                    "kind": "function",
                    "name": node.name,
                    "parent": None,
                    "range": {
                        "startLine": node.lineno,
                        "startCol": node.col_offset,
                        "endLine": node.end_lineno or node.lineno,
                        "endCol": node.end_col_offset or 0
                    }
                })
        
        self.symbols[rel_path] = symbols

    def _index_javascript(self, file_path: Path, rel_path: str):
        """Index JS file using regex (simple initial approach)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            return
        
        symbols = []
        import re
        
        # Simple patterns for functions/classes
        func_pattern = re.compile(r'^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)')
        class_pattern = re.compile(r'^\s*(?:export\s+)?class\s+(\w+)')
        method_pattern = re.compile(r'^\s+(\w+)\s*\([^)]*\)\s*{')
        
        current_class = None
        for i, line in enumerate(lines, 1):
            if match := class_pattern.match(line):
                current_class = match.group(1)
                symbols.append({
                    "kind": "class",
                    "name": current_class,
                    "parent": None,
                    "range": {"startLine": i, "startCol": 0, "endLine": i, "endCol": 0}
                })
            elif match := func_pattern.match(line):
                symbols.append({
                    "kind": "function",
                    "name": match.group(1),
                    "parent": None,
                    "range": {"startLine": i, "startCol": 0, "endLine": i, "endCol": 0}
                })
        
        self.symbols[rel_path] = symbols

    def find_symbol(self, name: str) -> List[dict]:
        """Find all occurrences of a symbol."""
        results = []
        for file_path, symbols in self.symbols.items():
            for sym in symbols:
                if sym["name"] == name:
                    results.append({"filePath": file_path, **sym})
        return results
