from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict


@dataclass
class ExecutionResult:
    status: str
    log_path: Optional[Path] = None
    session_id: Optional[str] = None
    message: Optional[str] = None
    action_completed: bool = False
    behavior_completed: bool = False
    context_loaded: bool = False
    instructions: str = ''
    api_called: bool = False
    completed: bool = False
    loop_count: int = 0
    looping: bool = False
    operation: Optional[str] = None
    behavior: Optional[str] = None
    action: Optional[str] = None
    context_included: bool = False
    operations_executed: List[str] = field(default_factory=list)
    operations_status: Dict[str, str] = field(default_factory=dict)
    current_operation: Optional[str] = None
    loop_responses: List[str] = field(default_factory=list)
    blocked: bool = False
    blocked_operation: Optional[str] = None
    blocked_action: Optional[str] = None
    actions_executed: List[str] = field(default_factory=list)
    block_reason: Optional[str] = None
    exit_code: int = 0
    actions_status: Dict[str, str] = field(default_factory=dict)
    
    @property
    def had_not_done_responses(self) -> bool:
        return any('not done' in resp.lower() for resp in self.loop_responses)
    
    def set_blocked_at_operation(self, operation: str, operations_executed: List[str]) -> None:
        self.blocked_operation = operation
        self.operations_executed = operations_executed
        completed_ops = [op for op in operations_executed if op != operation]
        self.operations_status = {op: 'completed' for op in completed_ops}
        self.operations_status[operation] = 'blocked'
    
    def set_blocked_at_action(self, action: str, actions_executed: List[str] = None) -> None:
        self.blocked_action = action
        if actions_executed is not None:
            self.actions_executed = actions_executed.copy()
        else:
            self.actions_executed = [action]
        completed_actions = [a for a in self.actions_executed if a != action]
        self.actions_status = {a: 'completed' for a in completed_actions}
        self.actions_status[action] = 'blocked'
    
    @classmethod
    def creates_blocked(
        cls,
        log_path: Path,
        session_id: str,
        context_loaded: bool,
        instructions: str,
        loop_count: int,
        loop_responses: List[str]
    ) -> 'ExecutionResult':
        return cls(
            status='blocked',
            log_path=log_path,
            session_id=session_id,
            message='AI blocked waiting for input',
            context_loaded=context_loaded,
            instructions=instructions,
            api_called=True,
            completed=False,
            loop_count=loop_count,
            looping=False,
            loop_responses=loop_responses,
            blocked=True,
            block_reason='Waiting for user input',
            exit_code=2
        )
    
    @classmethod
    def creates_completed(
        cls,
        log_path: Path,
        session_id: str,
        context_loaded: bool,
        instructions: str,
        loop_count: int,
        loop_responses: List[str],
        completed: bool = True
    ) -> 'ExecutionResult':
        return cls(
            status='completed',
            log_path=log_path,
            session_id=session_id,
            message='Execution completed successfully',
            context_loaded=context_loaded,
            instructions=instructions,
            api_called=True,
            completed=completed,
            loop_count=loop_count,
            looping=False,
            loop_responses=loop_responses
        )
