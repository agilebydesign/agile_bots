"""
Context Injector - Builds rich, validated context for supervised execution.

Strategies for stronger constraints:
1. Open referenced files - inject directly into prompt (chunked if needed)
2. Open referenced rules - inject incrementally, validate as you go  
3. Open stories/epics from story-graph - inject relevant sections + test code
4. Chunking with "ask for more" - process one chunk, then request next

The goal is to leave NO ROOM for the AI to wander off-task.
"""
import json
import re
from pathlib import Path
from typing import Optional, List, Dict
from dataclasses import dataclass


@dataclass
class ContextChunk:
    """A chunk of context to be injected into the prompt."""
    chunk_number: int
    total_chunks: int
    content: str
    source: str
    chunk_type: str


@dataclass
class InjectionResult:
    """Result of context injection."""
    prompt: str
    chunks_used: List[ContextChunk]
    has_more_chunks: bool
    next_chunk_index: int
    total_tokens_estimate: int


class ContextInjector:
    """
    Builds rich context for AI prompts by injecting referenced content.
    """
    
    CHARS_PER_TOKEN = 4
    DEFAULT_MAX_INJECT_TOKENS = 50000
    
    def __init__(
        self,
        workspace_path: Path,
        max_inject_tokens: int = DEFAULT_MAX_INJECT_TOKENS,
        max_file_lines: int = 500
    ):
        self.workspace_path = workspace_path
        self.max_inject_tokens = max_inject_tokens
        self.max_file_lines = max_file_lines
        self._story_graph: Optional[Dict] = None
        self._loaded_chunks: List[ContextChunk] = []
        self._current_chunk_index: int = 0
    
    def load_story_graph(self) -> Optional[Dict]:
        """Load the story-graph.json if it exists."""
        if self._story_graph is not None:
            return self._story_graph
        
        possible_paths = [
            self.workspace_path / 'docs' / 'stories' / 'story-graph.json',
            self.workspace_path / 'agile_bot' / 'bots' / 'base_bot' / 'docs' / 'stories' / 'story-graph.json',
        ]
        
        for path in possible_paths:
            if path.exists():
                try:
                    self._story_graph = json.loads(path.read_text(encoding='utf-8'))
                    return self._story_graph
                except Exception:
                    continue
        
        return None
    
    def extract_file_references(self, text: str) -> List[Path]:
        """Extract file paths referenced in text."""
        patterns = [
            r'`([^`]+\.[a-z]+)`',
            r'File:\s*[`"]?([^\s`"]+)[`"]?',
            r'\*\*File:\*\*\s*`([^`]+)`',
        ]
        
        found_paths = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                path = self.workspace_path / match
                if path.exists():
                    found_paths.append(path)
        
        return list(set(found_paths))
    
    def extract_rule_references(self, text: str) -> List[Path]:
        """Extract .mdc rule file references from text."""
        patterns = [r'([a-zA-Z0-9_-]+\.mdc)']
        
        found_rules = []
        cursor_rules = self.workspace_path / '.cursor' / 'rules'
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                rule_path = cursor_rules / match
                if rule_path.exists():
                    found_rules.append(rule_path)
        
        return list(set(found_rules))
    
    def read_file_chunked(self, file_path: Path, chunk_type: str = 'file') -> List[ContextChunk]:
        """Read a file and split into chunks if needed."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            return []
        
        lines = content.split('\n')
        
        if len(lines) <= self.max_file_lines:
            return [ContextChunk(
                chunk_number=1,
                total_chunks=1,
                content=content,
                source=str(file_path),
                chunk_type=chunk_type
            )]
        
        chunks = []
        chunk_lines = []
        chunk_number = 0
        
        for i, line in enumerate(lines):
            chunk_lines.append(line)
            
            if len(chunk_lines) >= self.max_file_lines:
                chunk_number += 1
                chunks.append(ContextChunk(
                    chunk_number=chunk_number,
                    total_chunks=0,
                    content='\n'.join(chunk_lines),
                    source=f"{file_path} (chunk {chunk_number})",
                    chunk_type=chunk_type
                ))
                chunk_lines = []
        
        if chunk_lines:
            chunk_number += 1
            chunks.append(ContextChunk(
                chunk_number=chunk_number,
                total_chunks=0,
                content='\n'.join(chunk_lines),
                source=f"{file_path} (chunk {chunk_number})",
                chunk_type=chunk_type
            ))
        
        for chunk in chunks:
            chunk.total_chunks = len(chunks)
        
        return chunks
    
    def build_constrained_prompt(
        self,
        original_prompt: str,
        iteration_number: Optional[int] = None,
        total_iterations: Optional[int] = None
    ) -> str:
        """Build a heavily constrained prompt that leaves no room for deviation."""
        parts = []
        
        parts.append("# CRITICAL CONSTRAINTS - READ FIRST")
        parts.append("")
        parts.append("YOU MUST FOLLOW THESE RULES EXACTLY:")
        parts.append("")
        parts.append("1. DO ONLY what is specified in the ORIGINAL TASK below")
        parts.append("2. DO NOT 'fix' any errors you see in the workspace unless the task says to")
        parts.append("3. DO NOT work on files not mentioned in the task")
        parts.append("4. DO NOT add features, improvements, or 'nice to haves'")
        parts.append("5. DO NOT say 'I also noticed...' or 'While doing this...'")
        parts.append("6. If you see unrelated issues, IGNORE THEM COMPLETELY")
        parts.append("7. When done with ONE step, STOP and report what you did")
        parts.append("")
        
        if iteration_number and total_iterations:
            parts.append(f"## CURRENT ITERATION: {iteration_number} of {total_iterations}")
            parts.append("")
            parts.append("You are processing a plan in chunks. Focus ONLY on this iteration.")
            parts.append(f"When done, say 'ITERATION {iteration_number} COMPLETE' and STOP.")
            parts.append("")
        
        # Inject referenced files
        file_refs = self.extract_file_references(original_prompt)
        rule_refs = self.extract_rule_references(original_prompt)
        
        if file_refs or rule_refs:
            parts.append("# INJECTED CONTEXT")
            parts.append("")
            
            for file_path in file_refs[:3]:
                chunks = self.read_file_chunked(file_path)
                for chunk in chunks[:2]:
                    parts.append(f"## FILE: {chunk.source}")
                    parts.append("```")
                    parts.append(chunk.content[:5000])
                    if len(chunk.content) > 5000:
                        parts.append("... (truncated)")
                    parts.append("```")
                    parts.append("")
            
            for rule_path in rule_refs[:2]:
                chunks = self.read_file_chunked(rule_path, 'rule')
                for chunk in chunks[:1]:
                    parts.append(f"## RULE: {chunk.source}")
                    parts.append("```")
                    parts.append(chunk.content[:3000])
                    parts.append("```")
                    parts.append("")
        
        parts.append("---")
        parts.append("# ORIGINAL TASK")
        parts.append("")
        parts.append(original_prompt)
        
        parts.append("")
        parts.append("---")
        parts.append("# FINAL REMINDER")
        parts.append("")
        parts.append("- Stay on task. Do ONLY what was asked.")
        parts.append("- If you deviate, your changes will be UNDONE and you'll restart.")
        parts.append("- Success = completing the task exactly as specified, nothing more.")
        
        return '\n'.join(parts)
