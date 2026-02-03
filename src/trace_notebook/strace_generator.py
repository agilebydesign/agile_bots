"""
Generate .strace files with real code analysis.
Walks the test method, finds all calls, locates implementations.
"""
import ast
import json
import sys
from pathlib import Path
from typing import Optional


class StraceGenerator:
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.found_code = []  # Collected code sections
        self.seen = set()  # Avoid duplicates
    
    def generate(self, test_file: str, test_class: str, test_method: str, 
                 scenario_name: str, scenario_steps: str,
                 story_file: str = None, story_line: int = 1) -> dict:
        """Generate strace data for a test method."""
        
        # Read the test file
        test_path = self.workspace / test_file
        if not test_path.exists():
            return {"error": f"Test file not found: {test_file}"}
        
        source = test_path.read_text(encoding='utf-8')
        lines = source.split('\n')
        
        # Find and extract the test method
        test_code, test_start, test_end = self._extract_method(source, lines, test_class, test_method)
        if not test_code:
            return {"error": f"Test method not found: {test_method}"}
        
        # Analyze the test method for calls
        self._analyze_method(test_code, test_file, depth=0)
        
        # Build the strace structure
        return {
            "scenario": {
                "name": scenario_name,
                "type": "happy_path",
                "steps": scenario_steps,
                "file": story_file,
                "line": story_line
            },
            "test": {
                "method": test_method,
                "file": test_file,
                "line": test_start,
                "code": test_code
            },
            "code": self.found_code
        }
    
    def _extract_method(self, source: str, lines: list, class_name: str, method_name: str):
        """Extract a method from a class."""
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return None, 0, 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == method_name:
                        start = item.lineno
                        end = item.end_lineno or start
                        code = '\n'.join(lines[start - 1:end])
                        return code, start, end
        return None, 0, 0
    
    def _extract_function(self, source: str, lines: list, func_name: str):
        """Extract a top-level function."""
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return None, 0, 0
        
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef) and node.name == func_name:
                start = node.lineno
                end = node.end_lineno or start
                code = '\n'.join(lines[start - 1:end])
                return code, start, end
        return None, 0, 0
    
    def _extract_class_method(self, source: str, lines: list, class_name: str, method_name: str):
        """Extract a method from a class."""
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return None, 0, 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == method_name:
                        start = item.lineno
                        end = item.end_lineno or start
                        code = '\n'.join(lines[start - 1:end])
                        return code, start, end
        return None, 0, 0
    
    def _extract_class(self, source: str, lines: list, class_name: str):
        """Extract entire class definition."""
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return None, 0, 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                start = node.lineno
                end = node.end_lineno or start
                code = '\n'.join(lines[start - 1:end])
                return code, start, end
        return None, 0, 0
    
    def _analyze_method(self, code: str, source_file: str, depth: int):
        """Analyze a method for calls and find their implementations."""
        if depth > 3:  # Limit depth
            return
        
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return
        
        # Find all calls
        calls = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                call_info = self._parse_call(node)
                if call_info and call_info not in calls:
                    calls.append(call_info)
        
        # Try to find implementations
        for call in calls:
            self._find_implementation(call, depth)
    
    def _parse_call(self, node: ast.Call) -> Optional[dict]:
        """Parse a call node into useful info."""
        if isinstance(node.func, ast.Attribute):
            # obj.method() or obj.attr.method()
            method = node.func.attr
            # Try to get the object chain
            obj_chain = self._get_attr_chain(node.func.value)
            return {"type": "method", "method": method, "obj": obj_chain}
        elif isinstance(node.func, ast.Name):
            # function() or ClassName()
            return {"type": "call", "name": node.func.id}
        return None
    
    def _get_attr_chain(self, node) -> list:
        """Get the chain of attribute access like helper.domain.story."""
        chain = []
        while isinstance(node, ast.Attribute):
            chain.insert(0, node.attr)
            node = node.value
        if isinstance(node, ast.Name):
            chain.insert(0, node.id)
        return chain
    
    def _find_implementation(self, call: dict, depth: int):
        """Try to find the implementation of a call."""
        key = str(call)
        if key in self.seen:
            return
        self.seen.add(key)
        
        if call["type"] == "call":
            # Direct function/class call
            name = call["name"]
            # Skip builtins and common
            if name in ('print', 'len', 'str', 'int', 'list', 'dict', 'set', 'tuple', 
                       'range', 'enumerate', 'zip', 'map', 'filter', 'sorted', 'isinstance',
                       'hasattr', 'getattr', 'setattr', 'open', 'type'):
                return
            
            # Look for class or function in test helpers
            impl = self._search_for_class_or_function(name)
            if impl:
                self.found_code.append(impl)
                # Recursively analyze if it's a class __init__
                if impl.get("is_init"):
                    self._analyze_method(impl["code"], impl["file"], depth + 1)
        
        elif call["type"] == "method":
            # Method call like helper.domain.story.create_story_graph()
            obj_chain = call["obj"]
            method = call["method"]
            
            # Skip self calls and common patterns
            if obj_chain and obj_chain[0] in ('self', 'cls'):
                return
            if method.startswith('_'):
                return
            if method in ('append', 'extend', 'get', 'keys', 'values', 'items', 
                         'split', 'join', 'strip', 'lower', 'upper', 'format',
                         'startswith', 'endswith', 'replace'):
                return
            
            # Try to find the method
            impl = self._search_for_method(obj_chain, method)
            if impl:
                self.found_code.append(impl)
                self._analyze_method(impl["code"], impl["file"], depth + 1)
    
    def _search_for_class_or_function(self, name: str) -> Optional[dict]:
        """Search workspace for a class or function definition."""
        # Search in test/helpers first
        search_dirs = [
            self.workspace / "test" / "helpers",
            self.workspace / "test",
            self.workspace / "src",
        ]
        
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
            for py_file in search_dir.rglob("*.py"):
                try:
                    source = py_file.read_text(encoding='utf-8')
                    if f"class {name}" in source or f"def {name}" in source:
                        lines = source.split('\n')
                        
                        # Try class first
                        code, start, end = self._extract_class(source, lines, name)
                        if code:
                            rel_path = str(py_file.relative_to(self.workspace)).replace("\\", "/")
                            # Just get __init__ method if it's a class
                            init_code, init_start, init_end = self._extract_class_method(source, lines, name, "__init__")
                            if init_code:
                                return {
                                    "symbol": f"{name}.__init__",
                                    "file": rel_path,
                                    "line": init_start,
                                    "code": init_code,
                                    "is_init": True
                                }
                            else:
                                # Return first 50 lines of class
                                short_code = '\n'.join(code.split('\n')[:50])
                                if len(code.split('\n')) > 50:
                                    short_code += "\n    # ... more methods ..."
                                return {
                                    "symbol": name,
                                    "file": rel_path,
                                    "line": start,
                                    "code": short_code
                                }
                        
                        # Try function
                        code, start, end = self._extract_function(source, lines, name)
                        if code:
                            rel_path = str(py_file.relative_to(self.workspace)).replace("\\", "/")
                            return {
                                "symbol": name,
                                "file": rel_path,
                                "line": start,
                                "code": code
                            }
                except Exception:
                    continue
        return None
    
    def _search_for_method(self, obj_chain: list, method: str) -> Optional[dict]:
        """Search for a method by scanning all classes in workspace for the method name."""
        if not obj_chain:
            return None
        
        # Skip common non-workspace patterns
        last_obj = obj_chain[-1] if obj_chain else None
        if last_obj in ('output', 'lower', 'upper', 'strip', 'split', 'join', 'format',
                        'keys', 'values', 'items', 'get', 'pop', 'append', 'extend'):
            return None
        
        # Search ALL classes in workspace for this method - no guessing
        search_dirs = [
            self.workspace / "test" / "helpers",
            self.workspace / "test",
            self.workspace / "src",
        ]
        
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
            for py_file in search_dir.rglob("*.py"):
                # Skip __pycache__, .venv, etc
                if '__pycache__' in str(py_file) or '.venv' in str(py_file):
                    continue
                try:
                    source = py_file.read_text(encoding='utf-8')
                    lines = source.split('\n')
                    
                    # Find all classes that have this method
                    tree = ast.parse(source)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            for item in node.body:
                                if isinstance(item, ast.FunctionDef) and item.name == method:
                                    start = item.lineno
                                    end = item.end_lineno or start
                                    code = '\n'.join(lines[start - 1:end])
                                    rel_path = str(py_file.relative_to(self.workspace)).replace("\\", "/")
                                    return {
                                        "symbol": f"{node.name}.{method}",
                                        "file": rel_path,
                                        "line": start,
                                        "code": code
                                    }
                except Exception:
                    continue
        return None


class DynamicStraceGenerator:
    """Generate trace by actually analyzing the code - no hardcoding."""
    
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.seen_symbols = set()
        self.max_depth = 4  # Limit depth for performance
        self._file_cache = {}  # Cache file contents
        self._method_index = None  # Cache method locations
    
    def _build_method_index(self):
        """Build index of all methods in workspace - do this once."""
        if self._method_index is not None:
            return
        
        self._method_index = {}  # method_name -> [(class_name, file_path, line)]
        
        search_dirs = [
            self.workspace / "test",  # All test code
            self.workspace / "src",   # All source code
        ]
        
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
            for py_file in search_dir.rglob("*.py"):
                if '__pycache__' in str(py_file):
                    continue
                try:
                    source = py_file.read_text(encoding='utf-8')
                    self._file_cache[str(py_file)] = source
                    tree = ast.parse(source)
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            class_name = node.name
                            for item in node.body:
                                if isinstance(item, ast.FunctionDef):
                                    method_name = item.name
                                    rel_path = str(py_file.relative_to(self.workspace)).replace("\\", "/")
                                    if method_name not in self._method_index:
                                        self._method_index[method_name] = []
                                    self._method_index[method_name].append({
                                        "class": class_name,
                                        "file": rel_path,
                                        "line": item.lineno,
                                        "end_line": item.end_lineno or item.lineno
                                    })
                except Exception:
                    continue
    
    def find_story_by_test_class(self, test_class: str, story_graph_path: str = "docs/stories/story-graph.json") -> Optional[dict]:
        """Find a story in story-graph.json by its test_class.
        
        Returns the story dict with line numbers for story and each scenario.
        """
        full_path = self.workspace / story_graph_path
        if not full_path.exists():
            return None
        
        content = full_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Parse and find the story first to get the name
        try:
            data = json.loads(content)
            story = self._find_story_recursive(data, test_class)
            if not story:
                return None
            
            story['_file'] = story_graph_path
            
            # Find the story name line (more accurate than test_class line)
            story_name = story.get('name', '')
            story_line = 1
            for i, line in enumerate(lines, start=1):
                if f'"name": "{story_name}"' in line:
                    # Make sure this is the story, not a scenario with same name
                    # Check if test_class appears within next 20 lines
                    for j in range(i, min(i + 20, len(lines))):
                        if f'"test_class": "{test_class}"' in lines[j - 1]:
                            story_line = i
                            break
                    if story_line != 1:
                        break
            
            story['_line'] = story_line
            
            # Find line numbers for each scenario
            for scenario in story.get('scenarios', []):
                scenario_name = scenario.get('name', '')
                for i, line in enumerate(lines, start=1):
                    if f'"name": "{scenario_name}"' in line:
                        scenario['_line'] = i
                        break
            
            return story
        except Exception:
            return None
    
    def _find_story_recursive(self, obj, test_class: str) -> Optional[dict]:
        """Recursively search for a story with the given test_class."""
        if isinstance(obj, dict):
            if obj.get('test_class') == test_class:
                return obj
            for value in obj.values():
                result = self._find_story_recursive(value, test_class)
                if result:
                    return result
        elif isinstance(obj, list):
            for item in obj:
                result = self._find_story_recursive(item, test_class)
                if result:
                    return result
        return None
    
    def generate_for_story(self, test_class: str, test_file: str, 
                           story_graph_path: str = "docs/stories/story-graph.json") -> dict:
        """Generate strace for an entire story with all its scenarios.
        
        Args:
            test_class: The test class name to find the story
            test_file: The test file containing the test methods
            story_graph_path: Path to story-graph.json
        
        Returns:
            Full strace data including story, all scenarios with their tests and code
        """
        # Build method index first
        self._build_method_index()
        
        # Find the story in story-graph.json
        story = self.find_story_by_test_class(test_class, story_graph_path)
        if not story:
            return {"error": f"Story with test_class '{test_class}' not found in {story_graph_path}"}
        
        # Read the test file
        test_path = self.workspace / test_file
        if not test_path.exists():
            return {"error": f"Test file not found: {test_file}"}
        
        source = test_path.read_text(encoding='utf-8')
        lines = source.split('\n')
        
        # Process each scenario
        scenarios_data = []
        for scenario in story.get('scenarios', []):
            scenario_name = scenario.get('name', '')
            test_method = scenario.get('test_method', '')
            steps = scenario.get('steps', '')
            
            # Extract test method code
            test_code, test_start, test_end = self._extract_method_from_class(
                source, lines, test_class, test_method
            )
            
            if test_code:
                # Analyze test method for calls
                # Reset seen symbols for each scenario to allow finding same methods
                self.seen_symbols = set()
                calls = self._find_calls_in_code(test_code)
                code_sections = []
                for call in calls:
                    section = self._resolve_call(call, depth=1)
                    if section:
                        code_sections.append(section)
            else:
                test_code = f"# Test method '{test_method}' not found"
                test_start = 0
                code_sections = []
            
            scenarios_data.append({
                "name": scenario_name,
                "type": scenario.get('type', 'happy_path'),
                "steps": steps,
                "file": story.get('_file', 'docs/stories/story-graph.json'),
                "line": scenario.get('_line', 1),
                "test": {
                    "method": test_method,
                    "file": test_file,
                    "line": test_start,
                    "code": test_code
                },
                "code": code_sections
            })
        
        # Format acceptance criteria as markdown
        acceptance_md = ""
        for ac in story.get('acceptance_criteria', []):
            if isinstance(ac, dict):
                acceptance_md += f"- {ac.get('text', ac.get('name', ''))}\n"
            else:
                acceptance_md += f"- {ac}\n"
        
        # Format users/actors
        users = story.get('users', [])
        users_md = "\n".join(f"- {u}" for u in users) if users else ""
        
        return {
            "story": {
                "name": story.get('name', 'Unknown Story'),
                "story_type": story.get('story_type', 'user'),
                "users": users_md,
                "acceptance_criteria": acceptance_md,
                "behavior": story.get('behavior', ''),
                "test_class": story.get('test_class', ''),
                "file": story.get('_file', story_graph_path),
                "line": story.get('_line', 1)
            },
            "scenarios": scenarios_data
        }
    
    def generate(self, test_file: str, test_class: str, test_method: str,
                 scenario_name: str, scenario_steps: str,
                 story_file: str = None, story_line: int = 1) -> dict:
        """Generate strace by parsing and analyzing the test method.
        
        The caller should provide story_line - the line number where the scenario
        was found in story_file. This avoids redundant searching.
        """
        # Build index first
        self._build_method_index()
        
        test_path = self.workspace / test_file
        if not test_path.exists():
            return {"error": f"Test file not found: {test_file}"}
        
        source = test_path.read_text(encoding='utf-8')
        lines = source.split('\n')
        
        # Extract test method
        test_code, test_start, test_end = self._extract_method_from_class(
            source, lines, test_class, test_method
        )
        if not test_code:
            return {"error": f"Test method not found: {test_class}.{test_method}"}
        
        # Analyze test method for all calls
        calls = self._find_calls_in_code(test_code)
        
        # Build code sections by finding implementations
        code_sections = []
        for call in calls:
            section = self._resolve_call(call, depth=1)
            if section:
                code_sections.append(section)
        
        return {
            "scenario": {
                "name": scenario_name,
                "type": "happy_path", 
                "steps": scenario_steps,
                "file": story_file,
                "line": story_line
            },
            "test": {
                "method": test_method,
                "file": test_file,
                "line": test_start,
                "code": test_code
            },
            "code": code_sections
        }
    
    def _extract_method_from_class(self, source: str, lines: list, 
                                    class_name: str, method_name: str):
        """Extract a method from a class."""
        try:
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == class_name:
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and item.name == method_name:
                            start = item.lineno
                            end = item.end_lineno or start
                            code = '\n'.join(lines[start - 1:end])
                            return code, start, end
        except SyntaxError:
            pass
        return None, 0, 0
    
    def _find_calls_in_code(self, code: str) -> list:
        """Find all function/method calls in code."""
        import textwrap
        calls = []
        try:
            # Dedent the code so it can be parsed
            dedented = textwrap.dedent(code)
            tree = ast.parse(dedented)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    call_info = self._parse_call_node(node)
                    if call_info and call_info not in calls:
                        calls.append(call_info)
        except SyntaxError:
            pass
        return calls
    
    def _parse_call_node(self, node: ast.Call) -> Optional[dict]:
        """Parse an AST Call node into structured info."""
        if isinstance(node.func, ast.Attribute):
            method = node.func.attr
            chain = self._get_attr_chain(node.func.value)
            return {"type": "method", "method": method, "chain": chain}
        elif isinstance(node.func, ast.Name):
            return {"type": "function", "name": node.func.id}
        return None
    
    def _get_attr_chain(self, node) -> list:
        """Get attribute chain like helper.domain.story."""
        chain = []
        while isinstance(node, ast.Attribute):
            chain.insert(0, node.attr)
            node = node.value
        if isinstance(node, ast.Name):
            chain.insert(0, node.id)
        return chain
    
    def _resolve_call(self, call: dict, depth: int) -> Optional[dict]:
        """Resolve a call to its implementation."""
        if depth > self.max_depth:
            return None
        
        if call["type"] == "function":
            name = call["name"]
            # Skip builtins
            if name in ('print', 'len', 'str', 'int', 'list', 'dict', 'set', 
                       'range', 'isinstance', 'hasattr', 'getattr', 'type', 'open'):
                return None
            return self._find_class_init_or_function(name, depth)
        
        elif call["type"] == "method":
            method = call["method"]
            # Skip common string/list methods
            if method in ('append', 'extend', 'get', 'keys', 'values', 'items',
                         'split', 'join', 'strip', 'lower', 'upper', 'format',
                         'startswith', 'endswith', 'replace', 'find', 'index'):
                return None
            return self._find_method_anywhere(method, depth)
        
        return None
    
    def _find_class_init_or_function(self, name: str, depth: int) -> Optional[dict]:
        """Find a class __init__ using the pre-built index."""
        symbol_key = f"{name}.__init__"
        if symbol_key in self.seen_symbols:
            return None
        self.seen_symbols.add(symbol_key)
        
        # Look for __init__ in the index where class matches name
        if "__init__" not in self._method_index:
            return None
        
        for match in self._method_index["__init__"]:
            if match["class"] == name:
                file_path = self.workspace / match["file"]
                try:
                    if str(file_path) in self._file_cache:
                        source = self._file_cache[str(file_path)]
                    else:
                        source = file_path.read_text(encoding='utf-8')
                    
                    lines = source.split('\n')
                    start = match["line"]
                    end = match["end_line"]
                    code = '\n'.join(lines[start - 1:end])
                    
                    # Recursively find calls
                    children = []
                    if depth < self.max_depth:
                        children = self._analyze_children(code, depth + 1)
                    
                    is_lazy = depth >= 3
                    result = {
                        "symbol": f"{name}.__init__",
                        "file": match["file"],
                        "line": start,
                        "depth": depth,
                        "children": children
                    }
                    if is_lazy:
                        result["lazy"] = True
                    else:
                        result["code"] = code
                    return result
                except Exception:
                    continue
        return None
    
    def _find_method_anywhere(self, method: str, depth: int) -> Optional[dict]:
        """Find a method definition using the pre-built index."""
        symbol_key = method
        if symbol_key in self.seen_symbols:
            return None
        self.seen_symbols.add(symbol_key)
        
        # Use the index
        if method not in self._method_index:
            return None
        
        # Take the first match
        match = self._method_index[method][0]
        file_path = self.workspace / match["file"]
        
        try:
            if str(file_path) in self._file_cache:
                source = self._file_cache[str(file_path)]
            else:
                source = file_path.read_text(encoding='utf-8')
            
            lines = source.split('\n')
            start = match["line"]
            end = match["end_line"]
            code = '\n'.join(lines[start - 1:end])
            
            # Recursively find calls (but limit depth)
            children = []
            if depth < self.max_depth:
                children = self._analyze_children(code, depth + 1)
            
            is_lazy = depth >= 3
            result = {
                "symbol": f"{match['class']}.{method}",
                "file": match["file"],
                "line": start,
                "depth": depth,
                "children": children
            }
            if is_lazy:
                result["lazy"] = True
            else:
                result["code"] = code
            return result
        except Exception:
            return None
    
    def _analyze_children(self, code: str, depth: int) -> list:
        """Analyze code for calls and build children list."""
        if depth > self.max_depth:
            return []
        
        children = []
        calls = self._find_calls_in_code(code)
        for call in calls:
            child = self._resolve_call(call, depth)
            if child:
                children.append(child)
        return children


def main():
    workspace = Path.cwd()
    
    # Config - use a story that exists in both story-graph.json and test files
    test_class = "TestDisplayRulesUsingCLI"
    test_file = "test/invoke_bot/perform_action/test_use_rules_in_prompt.py"
    
    # Use dynamic generator
    generator = DynamicStraceGenerator(workspace)
    
    # Try story-level generation first
    result = generator.generate_for_story(
        test_class=test_class,
        test_file=test_file,
        story_graph_path="docs/stories/story-graph.json"
    )
    
    if "error" in result:
        print(f"Error: {result['error']}")
        print("Falling back to sample scenario...")
        # Fallback to old method for testing
        result = generator.generate(
            test_file="test/invoke_bot/perform_action/test_use_rules_in_prompt.py",
            test_class="TestDisplayRulesUsingCLI",
            test_method="test_rules_action_shows_rules_digest",
            scenario_name="Rules action shows rules digest in CLI output",
            scenario_steps="GIVEN: CLI is at shape.validate\nWHEN: user navigates\nTHEN: CLI shows output",
            story_file="docs/stories/story-graph.json",
            story_line=1
        )
        if "error" in result:
            print(f"Fallback error: {result['error']}")
            return
    
    # Write output
    output_path = workspace / "src" / "trace_notebook" / "scenario.strace"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    
    def count_sections(code_list):
        count = len(code_list)
        for c in code_list:
            count += count_sections(c.get("children", []))
        return count
    
    # Handle both story-level and scenario-level output
    if "story" in result:
        # Story-level format
        print(f"Generated: {output_path}")
        print(f"  Story: {result['story'].get('name', 'Unknown')}")
        print(f"  Scenarios: {len(result.get('scenarios', []))}")
        for scenario in result.get('scenarios', []):
            total = count_sections(scenario.get('code', []))
            print(f"    - {scenario.get('name', 'Unknown')} ({total} code sections)")
    else:
        # Old scenario-level format
        total = count_sections(result.get("code", []))
        print(f"Generated: {output_path}")
        print(f"  Scenario: {result.get('scenario', {}).get('name', 'Unknown')}")
        print(f"  Found {total} code sections (nested)")


if __name__ == "__main__":
    main()
