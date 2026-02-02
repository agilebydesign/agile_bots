"""
Trace Viewer - Story → Test → Code traceability.

Usage:
    python -m trace_notebook.trace_viewer "Generate Bot Tools"
    python -m trace_notebook.trace_viewer --list
"""
import sys
import json
from pathlib import Path
from .cli.workspace_index import WorkspaceIndex
from .cli.python_analyzer import PythonAnalyzer
from .cli.snippet_extractor import SnippetExtractor


class TraceViewer:
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.index = WorkspaceIndex(workspace)
        self.analyzer = PythonAnalyzer()
        self.extractor = SnippetExtractor()
        
    def load(self):
        """Build workspace index."""
        print(f"Indexing {self.workspace}...")
        self.index.build()
        print(f"  {len(self.index.files)} files, {sum(len(s) for s in self.index.symbols.values())} symbols")

    def load_story_graph(self) -> dict:
        """Load story-graph.json."""
        path = self.workspace / "docs" / "stories" / "story-graph.json"
        if not path.exists():
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def list_stories(self):
        """Print all stories."""
        graph = self.load_story_graph()
        print("\n=== Stories ===\n")
        for epic in graph.get("epics", []):
            self._print_stories(epic, "")

    def _print_stories(self, node: dict, indent: str):
        """Recursively print stories."""
        for group in node.get("story_groups", []):
            for story in group.get("stories", []):
                print(f"{indent}• {story['name']}")
                print(f"{indent}  Test: {story.get('test_class', 'N/A')}")
        for sub in node.get("sub_epics", []):
            print(f"{indent}[{sub['name']}]")
            self._print_stories(sub, indent + "  ")

    def trace(self, story_name: str, max_depth: int = 2):
        """Trace a story through test → code."""
        graph = self.load_story_graph()
        story = self._find_story(graph, story_name)
        
        if not story:
            print(f"Story not found: {story_name}")
            return
        
        print(f"\n{'='*60}")
        print(f"STORY: {story['name']}")
        print(f"{'='*60}\n")
        
        # Show scenarios
        for scenario in story.get("scenarios", []):
            print(f"  SCENARIO: {scenario['name']}")
            if scenario.get("steps"):
                for step in scenario["steps"].split("\n"):
                    print(f"    {step}")
            print()
        
        # Find test class
        test_class = story.get("test_class")
        if not test_class:
            print("  (No test class linked)")
            return
        
        test_info = self._find_test_class(test_class)
        if not test_info:
            print(f"  Test class not found in code: {test_class}")
            return
        
        self._show_card("TEST", test_info["filePath"], test_info["range"], depth=0)
        
        # Expand test methods
        for method in self._get_test_methods(test_info["filePath"], test_class):
            self._show_card("TEST METHOD", test_info["filePath"], method["range"], 
                           symbol=method["name"], depth=1)
            
            # Find references in method (deduplicated)
            if max_depth > 1:
                refs = self._expand(test_info["filePath"], method["range"])
                seen = set()
                for ref in refs:
                    key = f"{ref['filePath']}:{ref['symbol']}"
                    if key in seen:
                        continue
                    seen.add(key)
                    if len(seen) > 3:  # Limit to 3 per method
                        break
                    self._show_card("CODE", ref["filePath"], ref["range"],
                                   symbol=ref["symbol"], depth=2)

    def _find_story(self, graph: dict, name: str) -> dict | None:
        """Find story by name."""
        for epic in graph.get("epics", []):
            result = self._search_stories(epic, name)
            if result:
                return result
        return None

    def _search_stories(self, node: dict, name: str) -> dict | None:
        for group in node.get("story_groups", []):
            for story in group.get("stories", []):
                if story["name"].lower() == name.lower():
                    return story
        for sub in node.get("sub_epics", []):
            result = self._search_stories(sub, name)
            if result:
                return result
        return None

    def _find_test_class(self, class_name: str) -> dict | None:
        """Find test class in index."""
        for file_path, symbols in self.index.symbols.items():
            for sym in symbols:
                if sym["kind"] == "class" and sym["name"] == class_name:
                    return {"filePath": file_path, **sym}
        return None

    def _get_test_methods(self, file_path: str, class_name: str) -> list:
        """Get test methods from class."""
        methods = []
        for sym in self.index.symbols.get(file_path, []):
            if sym["kind"] == "method" and sym["parent"] == class_name:
                if sym["name"].startswith("test_"):
                    methods.append(sym)
        return methods

    def _expand(self, file_path: str, range_: dict) -> list:
        """Find references in a code block."""
        full_path = self.workspace / file_path
        with open(full_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        refs = self.analyzer.find_references(
            source, 
            range_["startLine"], 
            range_["endLine"],
            self.index
        )
        # Filter: keep src/ code and helpers, skip test_*.py files
        def is_relevant_code(r):
            path = r["filePath"].replace("\\", "/")
            filename = path.split("/")[-1]
            # Keep src/ code  
            if path.startswith("src/"):
                return True
            # Keep helper files (not actual tests)
            if "_helper" in filename or "/helpers/" in path:
                return True
            # Skip actual test files
            if filename.startswith("test_"):
                return False
            return True
        
        return [r for r in refs if is_relevant_code(r)]

    def _show_card(self, kind: str, file_path: str, range_: dict, 
                   symbol: str = None, depth: int = 0):
        """Display a code card."""
        indent = "  " * depth
        full_path = self.workspace / file_path
        snippet = self.extractor.extract(full_path, range_)
        
        print(f"{indent}+-- {kind}: {symbol or ''}")
        print(f"{indent}|   {file_path}:{range_['startLine']}-{range_['endLine']}")
        print(f"{indent}+{'-'*50}")
        
        if isinstance(snippet, dict) and "text" in snippet:
            lines = snippet["text"].split("\n")
            for i, line in enumerate(lines[:20]):  # Max 20 lines
                line_num = snippet["startLine"] + i
                marker = ">" if range_["startLine"] <= line_num <= range_["endLine"] else " "
                print(f"{indent}| {marker} {line_num:4} | {line.rstrip()}")
            if len(lines) > 20:
                print(f"{indent}|   ... ({len(lines) - 20} more lines)")
        
        print(f"{indent}+{'-'*50}\n")


def main():
    # Find workspace (current dir or arg)
    workspace = Path.cwd()
    if len(sys.argv) > 1 and sys.argv[1] == "--workspace":
        workspace = Path(sys.argv[2])
        sys.argv = [sys.argv[0]] + sys.argv[3:]
    
    viewer = TraceViewer(workspace)
    viewer.load()
    
    if len(sys.argv) < 2 or sys.argv[1] == "--list":
        viewer.list_stories()
    else:
        story_name = " ".join(sys.argv[1:])
        viewer.trace(story_name)


if __name__ == "__main__":
    main()
