"""
Snippet Extractor - extracts code snippets with context.
"""
from pathlib import Path


class SnippetExtractor:
    """Extracts readable code snippets from files."""
    
    def __init__(self, context_lines: int = 3, max_lines: int = 80):
        self.context_lines = context_lines
        self.max_lines = max_lines

    def extract(self, file_path: Path, range_: dict) -> dict:
        """Extract snippet with header and highlights."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except (FileNotFoundError, UnicodeDecodeError):
            return {"error": f"Cannot read {file_path}"}
        
        start = max(0, range_["startLine"] - 1 - self.context_lines)
        end = min(len(lines), range_["endLine"] + self.context_lines)
        
        # Limit total lines
        if end - start > self.max_lines:
            end = start + self.max_lines
        
        snippet_lines = lines[start:end]
        
        return {
            "filePath": str(file_path),
            "startLine": start + 1,
            "endLine": end,
            "text": ''.join(snippet_lines),
            "highlightStart": range_["startLine"],
            "highlightEnd": range_["endLine"]
        }
