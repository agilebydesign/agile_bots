"""
Task Supervisor - Monitors executor bot and ensures it stays on track.

This provides a simple but intelligent supervision loop:
1. BOT 1 (Executor) -> Does work, produces output  
2. BOT 2 (Reviewer) -> Examines output thoroughly
   - On track -> Continue to next step
   - Off track -> UNDO + redirect to original prompt
   - Exception -> Fix code OR chunk if AI-related (context too big)
3. Loop until done, with chunking support for large plans
"""
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum


class ReviewResult(Enum):
    ON_TRACK = "on_track"
    OFF_TRACK = "off_track"
    EXCEPTION = "exception"
    COMPLETE = "complete"
    NEEDS_CHUNKING = "needs_chunking"


@dataclass
class ChunkInfo:
    """Information about a plan chunk for processing."""
    chunk_number: int
    total_chunks: int
    content: str
    start_line: int
    end_line: int


@dataclass 
class SupervisionResult:
    """Result of supervisor's review."""
    result: ReviewResult
    message: str
    should_continue: bool = True
    should_undo: bool = False
    redirect_prompt: Optional[str] = None
    chunk_info: Optional[ChunkInfo] = None
    files_changed: List[str] = field(default_factory=list)
    exception_info: Optional[str] = None


class TaskSupervisor:
    """
    Supervises an executor bot to ensure it stays on track with the original task.
    
    Key behaviors:
    - Reviews all output against original prompt
    - Detects when executor goes off-track
    - Can chunk large plans and process incrementally
    - Can undo changes if executor did wrong things
    - Handles AI exceptions (context too big, etc.)
    """
    
    def __init__(
        self, 
        workspace_path: Path,
        original_prompt: str,
        plan_file: Optional[Path] = None,
        max_chunk_lines: int = 200
    ):
        self.workspace_path = workspace_path
        self.original_prompt = original_prompt
        self.plan_file = plan_file
        self.max_chunk_lines = max_chunk_lines
        self.current_chunk: int = 0
        self.total_chunks: int = 0
        self.chunks: List[ChunkInfo] = []
        self._git_state_before: Optional[str] = None
        
        if plan_file and plan_file.exists():
            self._load_and_chunk_plan(plan_file)
    
    def _load_and_chunk_plan(self, plan_file: Path) -> None:
        """Load plan file and split into manageable chunks."""
        content = plan_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        if len(lines) <= self.max_chunk_lines:
            self.chunks = [ChunkInfo(
                chunk_number=1,
                total_chunks=1,
                content=content,
                start_line=1,
                end_line=len(lines)
            )]
        else:
            self.chunks = self._split_by_iterations(lines)
        
        self.total_chunks = len(self.chunks)
    
    def _split_by_iterations(self, lines: List[str]) -> List[ChunkInfo]:
        """Split plan by ITERATION markers or section headers."""
        chunks = []
        current_chunk_lines = []
        current_start = 1
        chunk_number = 0
        
        for i, line in enumerate(lines, 1):
            is_section_break = (
                line.startswith('### ITERATION') or
                line.startswith('## PART') or
                (line.startswith('---') and len(current_chunk_lines) > 50)
            )
            
            if is_section_break and current_chunk_lines:
                chunk_number += 1
                chunks.append(ChunkInfo(
                    chunk_number=chunk_number,
                    total_chunks=0,
                    content='\n'.join(current_chunk_lines),
                    start_line=current_start,
                    end_line=i - 1
                ))
                current_chunk_lines = [line]
                current_start = i
            else:
                current_chunk_lines.append(line)
        
        if current_chunk_lines:
            chunk_number += 1
            chunks.append(ChunkInfo(
                chunk_number=chunk_number,
                total_chunks=0,
                content='\n'.join(current_chunk_lines),
                start_line=current_start,
                end_line=len(lines)
            ))
        
        for chunk in chunks:
            chunk.total_chunks = len(chunks)
        
        return chunks
    
    def save_git_state(self) -> None:
        """Save current git state for potential undo."""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.workspace_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self._git_state_before = result.stdout.strip()
        except Exception:
            self._git_state_before = None
    
    def undo_changes(self) -> bool:
        """Undo all changes since save_git_state was called."""
        try:
            subprocess.run(
                ['git', 'checkout', '--', '.'],
                cwd=self.workspace_path,
                capture_output=True,
                timeout=30
            )
            subprocess.run(
                ['git', 'clean', '-fd'],
                cwd=self.workspace_path,
                capture_output=True,
                timeout=30
            )
            return True
        except Exception:
            return False
    
    def get_files_changed(self) -> List[str]:
        """Get list of files changed since last commit."""
        try:
            result = subprocess.run(
                ['git', 'status', '--short'],
                cwd=self.workspace_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        except Exception:
            pass
        return []
    
    def get_current_chunk(self) -> Optional[ChunkInfo]:
        """Get the current chunk to process."""
        if self.current_chunk < len(self.chunks):
            return self.chunks[self.current_chunk]
        return None
    
    def advance_to_next_chunk(self) -> bool:
        """Move to next chunk. Returns True if more chunks remain."""
        self.current_chunk += 1
        return self.current_chunk < len(self.chunks)
    
    def build_chunk_prompt(self, chunk: ChunkInfo) -> str:
        """Build a prompt for executing a single chunk."""
        return f"""CRITICAL INSTRUCTIONS - READ BEFORE DOING ANYTHING:

1. YOUR ONLY TASK: Execute chunk {chunk.chunk_number} of {chunk.total_chunks} from the plan
2. DO NOT fix any validation errors you see in the workspace unless the plan says to
3. DO NOT work on files not mentioned in this chunk
4. DO NOT deviate from the plan for ANY reason
5. If you see errors unrelated to this chunk, IGNORE THEM

CHUNK {chunk.chunk_number} OF {chunk.total_chunks}:
(Lines {chunk.start_line}-{chunk.end_line} of the plan)

{chunk.content}

---

When done with THIS CHUNK ONLY, say "CHUNK {chunk.chunk_number} COMPLETE" and stop.
I will then provide the next chunk.
"""
    
    def build_review_prompt(self, executor_output: str, files_changed: List[str]) -> str:
        """Build a prompt for the reviewer bot to analyze executor's work."""
        chunk = self.get_current_chunk()
        chunk_context = ""
        if chunk:
            chunk_context = f"""
CURRENT CHUNK ({chunk.chunk_number} of {chunk.total_chunks}):
{chunk.content[:1000]}{'...' if len(chunk.content) > 1000 else ''}
"""
        
        return f"""You are a TASK REVIEWER. Your ONLY job is to verify the executor stayed on track.

ORIGINAL TASK/PROMPT:
{self.original_prompt[:2000]}{'...' if len(self.original_prompt) > 2000 else ''}
{chunk_context}

EXECUTOR'S OUTPUT (last 3000 chars):
{executor_output[-3000:]}

FILES CHANGED:
{chr(10).join(files_changed[:20]) if files_changed else 'None'}

REVIEW CRITERIA:
1. Did the executor do ONLY what the original task/chunk specified?
2. Did the executor work on files NOT mentioned in the task? (OFF-TRACK!)
3. Did the executor "notice" other issues and try to fix them? (OFF-TRACK!)
4. Did the executor say things like "I also noticed..." or "While doing this..." (OFF-TRACK!)
5. Did the executor skip steps or do them out of order?
6. If there was an exception, what kind? (code error vs AI limit)

Answer with EXACTLY one of these:
- "ON_TRACK" - Executor did exactly what was asked
- "OFF_TRACK: [reason]" - Executor deviated (explain why)
- "COMPLETE" - The task/chunk is fully done correctly
- "EXCEPTION: [type]" - There was an error (CODE_ERROR or AI_LIMIT)
- "NEEDS_UNDO" - Executor made wrong changes that need reverting

Your answer:"""
    
    def parse_review_response(self, response: str) -> SupervisionResult:
        """Parse the reviewer's response into a SupervisionResult."""
        response = response.strip().upper()
        files = self.get_files_changed()
        
        if response.startswith("COMPLETE"):
            return SupervisionResult(
                result=ReviewResult.COMPLETE,
                message="Task/chunk completed successfully",
                should_continue=self.current_chunk + 1 < len(self.chunks),
                files_changed=files
            )
        
        if response.startswith("ON_TRACK"):
            return SupervisionResult(
                result=ReviewResult.ON_TRACK,
                message="Executor is on track",
                should_continue=True,
                files_changed=files
            )
        
        if response.startswith("OFF_TRACK"):
            reason = response.replace("OFF_TRACK:", "").replace("OFF_TRACK", "").strip()
            chunk = self.get_current_chunk()
            redirect = self.build_chunk_prompt(chunk) if chunk else self.original_prompt
            return SupervisionResult(
                result=ReviewResult.OFF_TRACK,
                message=f"Executor went off track: {reason}",
                should_continue=True,
                should_undo=True,
                redirect_prompt=f"STOP! You went off track. {reason}\n\nGo back to the ORIGINAL TASK:\n\n{redirect}",
                files_changed=files
            )
        
        if "NEEDS_UNDO" in response:
            return SupervisionResult(
                result=ReviewResult.OFF_TRACK,
                message="Executor made wrong changes - undo required",
                should_continue=True,
                should_undo=True,
                redirect_prompt=self.original_prompt,
                files_changed=files
            )
        
        if response.startswith("EXCEPTION"):
            exception_type = response.replace("EXCEPTION:", "").replace("EXCEPTION", "").strip()
            needs_chunking = "AI_LIMIT" in exception_type or "CONTEXT" in exception_type
            return SupervisionResult(
                result=ReviewResult.NEEDS_CHUNKING if needs_chunking else ReviewResult.EXCEPTION,
                message=f"Exception occurred: {exception_type}",
                should_continue=True,
                exception_info=exception_type,
                files_changed=files
            )
        
        return SupervisionResult(
            result=ReviewResult.ON_TRACK,
            message="Review inconclusive, continuing",
            should_continue=True,
            files_changed=files
        )
