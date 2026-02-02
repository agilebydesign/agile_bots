"""
Trace CLI - stdio JSON daemon for story→test→code traceability.

Usage:
    python -m trace_notebook.cli.trace_cli

Commands via stdin JSON:
    {"cmd": "init", "workspace": "/path/to/workspace"}
    {"cmd": "resolve_story", "storyName": "Generate Bot Tools"}
    {"cmd": "expand", "nodeId": "py:src/bot.py:10:0:50:0", "offset": 0, "limit": 8}
"""
import sys
import json
from pathlib import Path
from .workspace_index import WorkspaceIndex
from .python_analyzer import PythonAnalyzer
from .snippet_extractor import SnippetExtractor


class TraceCLI:
    def __init__(self):
        self.index: WorkspaceIndex | None = None
        self.analyzer = PythonAnalyzer()
        self.extractor = SnippetExtractor()

    def handle_command(self, cmd: dict) -> dict:
        command = cmd.get("cmd")
        
        if command == "init":
            return self._init(cmd.get("workspace"))
        elif command == "resolve_story":
            return self._resolve_story(cmd.get("storyName"))
        elif command == "expand":
            return self._expand(
                cmd.get("nodeId"),
                cmd.get("offset", 0),
                cmd.get("limit", 8)
            )
        elif command == "get_story_graph":
            return self._get_story_graph()
        else:
            return {"error": f"Unknown command: {command}"}

    def _init(self, workspace: str) -> dict:
        """Index the workspace."""
        workspace_path = Path(workspace)
        if not workspace_path.exists():
            return {"error": f"Workspace not found: {workspace}"}
        
        self.index = WorkspaceIndex(workspace_path)
        self.index.build()
        return {
            "status": "ok",
            "files_indexed": len(self.index.files),
            "symbols": len(self.index.symbols)
        }

    def _get_story_graph(self) -> dict:
        """Load story graph from workspace."""
        if not self.index:
            return {"error": "Workspace not initialized"}
        
        story_graph_path = self.index.workspace / "docs" / "stories" / "story-graph.json"
        if not story_graph_path.exists():
            return {"error": "story-graph.json not found"}
        
        with open(story_graph_path, 'r', encoding='utf-8') as f:
            return {"storyGraph": json.load(f)}

    def _resolve_story(self, story_name: str) -> dict:
        """Map story name to test file/class/method."""
        if not self.index:
            return {"error": "Workspace not initialized"}
        
        # Convention: story "Generate Bot Tools" → TestGenerateBotTools
        test_class = "Test" + story_name.replace(" ", "")
        
        # Find test file containing this class
        for file_path, symbols in self.index.symbols.items():
            for sym in symbols:
                if sym["kind"] == "class" and sym["name"] == test_class:
                    return {
                        "storyName": story_name,
                        "testFile": str(file_path),
                        "testClass": test_class,
                        "nodeId": self._make_node_id("python", file_path, sym["range"]),
                        "scenarios": self._get_test_methods(file_path, test_class)
                    }
        
        return {"error": f"Test class not found for story: {story_name}"}

    def _get_test_methods(self, file_path: str, class_name: str) -> list:
        """Get test methods from a test class."""
        methods = []
        for sym in self.index.symbols.get(file_path, []):
            if sym["kind"] == "method" and sym["parent"] == class_name:
                if sym["name"].startswith("test_"):
                    methods.append({
                        "name": sym["name"],
                        "nodeId": self._make_node_id("python", file_path, sym["range"]),
                        "range": sym["range"]
                    })
        return methods

    def _expand(self, node_id: str, offset: int, limit: int) -> dict:
        """Expand a node to find direct references."""
        if not self.index:
            return {"error": "Workspace not initialized"}
        
        # Parse nodeId: py:path:startLine:startCol:endLine:endCol
        parts = node_id.split(":")
        if len(parts) < 6:
            return {"error": f"Invalid nodeId: {node_id}"}
        
        lang = parts[0]
        file_path = ":".join(parts[1:-4])  # Handle Windows paths with :
        start_line = int(parts[-4])
        end_line = int(parts[-2])
        
        # Get source and analyze
        full_path = self.index.workspace / file_path
        if not full_path.exists():
            return {"error": f"File not found: {file_path}"}
        
        with open(full_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Find references in the code block
        refs = self.analyzer.find_references(
            source, 
            start_line, 
            end_line,
            self.index
        )
        
        # Filter to custom code only
        refs = [r for r in refs if self._is_custom_code(r["filePath"])]
        
        total = len(refs)
        children = refs[offset:offset + limit]
        
        # Generate snippets and nodeIds for each child
        for child in children:
            child["nodeId"] = self._make_node_id(child["lang"], child["filePath"], child["range"])
            child["snippet"] = self.extractor.extract(
                self.index.workspace / child["filePath"],
                child["range"]
            )
        
        return {
            "nodeId": node_id,
            "totalCandidates": total,
            "loaded": len(children),
            "offset": offset,
            "limit": limit,
            "children": children
        }

    def _make_node_id(self, lang: str, file_path: str, range_: dict) -> str:
        """Create deterministic nodeId."""
        rel_path = str(file_path).replace("\\", "/")
        return f"{lang}:{rel_path}:{range_['startLine']}:{range_.get('startCol', 0)}:{range_['endLine']}:{range_.get('endCol', 0)}"

    def _is_custom_code(self, file_path: str) -> bool:
        """Check if file is custom code (not external)."""
        excludes = ["node_modules", ".venv", "site-packages", "__pycache__"]
        path_str = str(file_path)
        return not any(ex in path_str for ex in excludes)


def main():
    """Main loop - read JSON commands from stdin, write responses to stdout."""
    cli = TraceCLI()
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        request_id = None
        try:
            cmd = json.loads(line)
            request_id = cmd.pop("_id", None)
            result = cli.handle_command(cmd)
        except json.JSONDecodeError as e:
            result = {"error": f"Invalid JSON: {e}"}
        except Exception as e:
            result = {"error": str(e)}
        
        # Echo back request ID for correlation
        if request_id is not None:
            result["_id"] = request_id
        
        print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
