"""
REPL Typed Results

Domain model types for REPL Session responses.
These define the contract/API between REPL Session and its consumers.

Based on "Typed Results" domain concept from stdio-cli-redesign.md.
"""

from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class REPLStateDisplay:
    output: str
    state_loaded: bool = False
    current_behavior: Optional[str] = None
    current_action: Optional[str] = None
    breadcrumbs: Optional[str] = None


@dataclass
class REPLCommandResponse:
    output: str
    response: str = ""
    status: Optional[str] = None
    action: Optional[str] = None
    scope_stored: bool = False
    scope: Optional[Dict] = None
    context_passed_to_action: Optional[Dict] = None
    repl_terminated: bool = False


@dataclass
class TTYDetectionResult:
    tty_detected: bool
    interactive_prompts_enabled: bool


