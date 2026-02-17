"""
Generate traces by analyzing code - traces from Test → Implementation Code.
Walks test methods, finds all calls, locates implementations up to max_depth.
Supports Python and JavaScript (test and src).
"""
import ast
import json
import re
from pathlib import Path
from typing import Optional


def _should_skip_path(file_path: Path) -> bool:
    """Skip generated/external directories."""
    s = str(file_path)
    return any(x in s for x in ['__pycache__', 'node_modules', '.venv', 'site-packages', '.git'])


class TraceGenerator:
    """Generate trace by analyzing code AST - no hardcoding."""
    
    def __init__(self, workspace: Path, max_depth: int = 3):
        self.workspace = workspace
        self.seen_symbols = set()
        self.max_depth = max_depth  # Default to 3 per plan
        self._file_cache = {}  # Cache file contents
        self._method_index = None  # Cache method locations
    
    def _build_method_index(self):
        """Build index of all methods/functions in workspace (Python and JS) - do this once."""
        if self._method_index is not None:
            return
        
        self._method_index = {}  # method_name -> [{class, file, line, end_line}]
        
        search_dirs = [
            self.workspace / "test",  # All test code
            self.workspace / "src",   # All source code
        ]
        
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
            for py_file in search_dir.rglob("*.py"):
                if _should_skip_path(py_file):
                    continue
                try:
                    source = py_file.read_text(encoding='utf-8')
                    self._file_cache[str(py_file)] = source
                    tree = ast.parse(source)
                    
                    for node in ast.iter_child_nodes(tree):
                        if isinstance(node, ast.ClassDef):
                            class_name = node.name
                            for item in node.body:
                                if isinstance(item, ast.FunctionDef):
                                    self._add_to_index(item.name, class_name, py_file, item.lineno, item.end_lineno or item.lineno)
                        elif isinstance(node, ast.FunctionDef):
                            self._add_to_index(node.name, "", py_file, node.lineno, node.end_lineno or node.lineno)
                except Exception:
                    continue
            
            for js_file in search_dir.rglob("*.js"):
                if _should_skip_path(js_file):
                    continue
                try:
                    self._index_javascript_file(js_file)
                except Exception:
                    continue
    
    def _add_to_index(self, method_name: str, class_name: str, file_path: Path, line: int, end_line: int):
        if not method_name:
            return
        rel_path = str(file_path.relative_to(self.workspace)).replace("\\", "/")
        if method_name not in self._method_index:
            self._method_index[method_name] = []
        self._method_index[method_name].append({
            "class": class_name,
            "file": rel_path,
            "line": line,
            "end_line": end_line
        })
    
    _JS_KEYWORDS = frozenset([
        'if', 'for', 'while', 'switch', 'catch', 'return', 'typeof', 'new', 'delete',
        'void', 'function', 'class', 'extends', 'import', 'export', 'await', 'case',
        'else', 'try', 'throw', 'finally', 'with', 'in', 'of', 'instanceof', 'typeof'
    ])

    def _index_javascript_file(self, js_file: Path):
        """Index JS file: functions and class methods."""
        source = js_file.read_text(encoding='utf-8')
        self._file_cache[str(js_file)] = source
        lines = source.split('\n')
        
        func_pattern = re.compile(r'^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(')
        class_pattern = re.compile(r'^\s*(?:export\s+)?class\s+(\w+)')
        method_pattern = re.compile(r'^\s+(?:async\s+)?(\w+)\s*\([^)]*\)\s*\{')
        arrow_method = re.compile(r'^\s+(\w+)\s*=\s*\([^)]*\)\s*=>')
        method_shorthand = re.compile(r'^\s+(\w+)\s*\([^)]*\)\s*\{')
        
        current_class = ""
        i = 0
        while i < len(lines):
            line = lines[i]
            if match := class_pattern.match(line):
                current_class = match.group(1)
                i += 1
                continue
            if match := func_pattern.match(line):
                name = match.group(1)
                if name not in self._JS_KEYWORDS:
                    end_line = self._find_js_block_end(lines, i)
                    self._add_to_index(name, "", js_file, i + 1, end_line)
                i += 1
                continue
            if current_class and (match := method_pattern.match(line) or method_shorthand.match(line) or arrow_method.match(line)):
                name = match.group(1)
                if name not in self._JS_KEYWORDS:
                    end_line = self._find_js_block_end(lines, i)
                    self._add_to_index(name, current_class, js_file, i + 1, end_line)
                i += 1
                continue
            i += 1
    
    def _find_js_block_end(self, lines: list, start_idx: int) -> int:
        """Find the line number (1-based) of the closing brace for a block starting at start_idx."""
        depth = 0
        for j in range(start_idx, len(lines)):
            line = lines[j]
            for c in line:
                if c == '{':
                    depth += 1
                elif c == '}':
                    depth -= 1
                    if depth == 0:
                        return j + 1
        return start_idx + 1
    
    def find_story_by_test_class(self, test_class: str, story_graph_path: str = "docs/story/story-graph.json") -> Optional[dict]:
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
                           story_graph_path: str = "docs/story/story-graph.json") -> dict:
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
                    sections = self._resolve_call(call, depth=1)
                    if sections:
                        code_sections.extend(sections)
            else:
                test_code = f"# Test method '{test_method}' not found"
                test_start = 0
                code_sections = []
            
            scenarios_data.append({
                "name": scenario_name,
                "type": scenario.get('type', 'happy_path'),
                "steps": steps,
                "file": story.get('_file', 'docs/story/story-graph.json'),
                "line": scenario.get('_line', 1),
                "test": {
                    "method": test_method,
                    "file": test_file,
                    "line": test_start
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
            sections = self._resolve_call(call, depth=1)
            if sections:
                code_sections.extend(sections)
        
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
                "line": test_start
            },
            "code": code_sections
        }
    
    def _extract_method_from_class(self, source: str, lines: list, 
                                    class_name: str, method_name: str):
        """Extract a method from a Python class or from a JS test file."""
        # Try Python first
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
    
    def _extract_method_from_js(self, source: str, lines: list, 
                                test_class: str, test_method: str):
        """Extract test callback body from JS test file. Returns (code, start_line, end_line) or (None,0,0)."""
        pattern = re.compile(rf"(?:await\s+)?t\.test\s*\(\s*['\"]({re.escape(test_method)})['\"]")
        pattern2 = re.compile(rf"test\s*\(\s*['\"]({re.escape(test_method)})['\"]")
        start_idx = None
        for i, line in enumerate(lines):
            if pattern.search(line) or pattern2.search(line):
                start_idx = i
                break
        if start_idx is None:
            return None, 0, 0
        end_idx = self._find_js_block_end(lines, start_idx)
        code = '\n'.join(lines[start_idx:end_idx])
        return code, start_idx + 1, end_idx
    
    def _trace_from_js_test_file(self, js_path: Path, test_class: str, workspace: Path) -> list:
        """Collect traces from all test() blocks in describe(test_class). Returns list of trace sections."""
        if not js_path.exists():
            return []
        try:
            source = js_path.read_text(encoding='utf-8')
            lines = source.split('\n')
            rel_path = str(js_path.relative_to(workspace)).replace("\\", "/")
            # Find all test('...', () => {...}) or test('...', async () => {...}) in the file
            test_pattern = re.compile(r"test\s*\(\s*['\"]([^'\"]+)['\"]")
            trace_sections = []
            i = 0
            while i < len(lines):
                m = test_pattern.search(lines[i])
                if m:
                    test_name = m.group(1)
                    end_idx = self._find_js_block_end(lines, i)
                    code = '\n'.join(lines[i:end_idx])
                    calls = self._find_calls_in_code(code, rel_path)
                    for call in calls:
                        sections = self._resolve_call(call, depth=1, shallow=False)
                        if sections:
                            trace_sections.extend(sections)
                    i = end_idx
                else:
                    i += 1
            return trace_sections
        except Exception:
            return []
    
    def _find_calls_in_code(self, code: str, source_file: Optional[str] = None) -> list:
        """Find all function/method calls in code. Uses JS parsing when source_file ends with .js."""
        if source_file and source_file.endswith('.js'):
            return self._find_calls_in_code_js(code)
        import textwrap
        calls = []
        try:
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
    
    def _find_calls_in_code_js(self, code: str) -> list:
        """Find function/method calls in JavaScript code using regex."""
        calls = []
        js_keywords = frozenset([
            'if', 'for', 'while', 'switch', 'catch', 'return', 'typeof', 'new', 'delete',
            'void', 'function', 'class', 'extends', 'import', 'export', 'await', 'case'
        ])
        # Method calls: .methodName(
        for m in re.finditer(r'\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', code):
            name = m.group(1)
            if name not in js_keywords and name not in ('then', 'catch', 'finally'):
                call = {"type": "method", "method": name, "chain": []}
                if call not in calls:
                    calls.append(call)
        # Function calls: identifier( - not preceded by . or :
        for m in re.finditer(r'(?<![.:\w])([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', code):
            name = m.group(1)
            if name not in js_keywords and name not in ('then', 'catch', 'finally'):
                call = {"type": "function", "name": name}
                if call not in calls:
                    calls.append(call)
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
    
    def _resolve_call(self, call: dict, depth: int, shallow: bool = False) -> list:
        """Resolve a call to its implementation(s). Returns list of sections (Python + JS)."""
        if depth > self.max_depth:
            return []
        
        if call["type"] == "function":
            name = call["name"]
            if name in ('print', 'len', 'str', 'int', 'list', 'dict', 'set', 
                       'range', 'isinstance', 'hasattr', 'getattr', 'type', 'open',
                       'describe', 'it', 'test', 'expect', 'require', 'console', 'setTimeout', 'setInterval'):
                return []
            result = self._find_class_init_or_function(name, depth, shallow)
            if result is not None:
                return [result]
            return self._find_method_anywhere(name, depth, shallow)
        
        elif call["type"] == "method":
            method = call["method"]
            if method in ('append', 'extend', 'get', 'keys', 'values', 'items',
                         'split', 'join', 'strip', 'lower', 'upper', 'format',
                         'startswith', 'endswith', 'replace', 'find', 'index'):
                return []
            return self._find_method_anywhere(method, depth, shallow)
        
        return []
    
    def _find_class_init_or_function(self, name: str, depth: int, shallow: bool = False) -> Optional[dict]:
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
                if shallow:
                    return {"symbol": f"{name}.__init__", "file": match["file"], "line": match["line"]}
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
                        children = self._analyze_children(code, depth + 1, match["file"])
                    
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
                    return result
                except Exception:
                    continue
        return None
    
    def _find_method_anywhere(self, method: str, depth: int, shallow: bool = False):
        """Find method definitions using the pre-built index. Returns list of sections (Python + JS)."""
        symbol_key = method
        if symbol_key in self.seen_symbols:
            return []
        self.seen_symbols.add(symbol_key)
        
        if method not in self._method_index:
            return []
        
        sections = []
        for match in self._method_index[method]:
            symbol = f"{match['class']}.{method}" if match["class"] else method
            if shallow:
                sections.append({"symbol": symbol, "file": match["file"], "line": match["line"]})
                continue
            try:
                file_path = self.workspace / match["file"]
                if str(file_path) in self._file_cache:
                    source = self._file_cache[str(file_path)]
                else:
                    source = file_path.read_text(encoding='utf-8')
                lines = source.split('\n')
                start = match["line"]
                end = match["end_line"]
                code = '\n'.join(lines[start - 1:end])
                children = []
                if depth < self.max_depth:
                    children = self._analyze_children(code, depth + 1, match["file"])
                is_lazy = depth >= 3
                result = {
                    "symbol": symbol,
                    "file": match["file"],
                    "line": start,
                    "depth": depth,
                    "children": children
                }
                if is_lazy:
                    result["lazy"] = True
                sections.append(result)
            except Exception:
                continue
        return sections
    
    def _analyze_children(self, code: str, depth: int, source_file: Optional[str] = None) -> list:
        """Analyze code for calls and build children list. Uses JS parsing when source_file ends with .js."""
        if depth > self.max_depth:
            return []
        
        children = []
        calls = self._find_calls_in_code(code, source_file)
        for call in calls:
            sections = self._resolve_call(call, depth)
            if sections:
                children.extend(sections)
        return children


def main():
    """Test harness for trace generation."""
    workspace = Path.cwd()
    
    # Config - use a story that exists in both story-graph.json and test files
    test_class = "TestDisplayRulesUsingCLI"
    test_file = "test/invoke_bot/perform_action/test_use_rules_in_prompt.py"
    
    # Use TraceGenerator with default max_depth=3
    generator = TraceGenerator(workspace)
    
    # Try story-level generation first
    result = generator.generate_for_story(
        test_class=test_class,
        test_file=test_file,
        story_graph_path="docs/story/story-graph.json"
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
            story_file="docs/story/story-graph.json",
            story_line=1
        )
        if "error" in result:
            print(f"Fallback error: {result['error']}")
            return
    
    # Write output (for testing)
    output_path = workspace / "docs" / "traces" / "scenario.strace"
    output_path.parent.mkdir(parents=True, exist_ok=True)
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
