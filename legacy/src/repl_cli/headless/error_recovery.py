import time
from typing import Optional
from .recoverable_error import RecoverableError
from .non_recoverable_error import NonRecoverableError


DEFAULT_MAX_ATTEMPTS = 3
DEFAULT_WAIT_TIME_SECONDS = 60.0


class ErrorRecovery:
    
    def __init__(
        self,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        current_attempts: int = 0,
        wait_time: float = DEFAULT_WAIT_TIME_SECONDS
    ):
        self.max_attempts = max_attempts
        self.current_attempts = current_attempts
        self.wait_time = wait_time
        self.session_terminated = False
    
    def can_retry(self) -> bool:
        return self.current_attempts < self.max_attempts
    
    def increment_attempt(self) -> None:
        self.current_attempts += 1
    
    def wait_before_retry(self, duration: float = 2.0) -> None:
        time.sleep(duration)
    
    def is_recoverable(self, error: Exception) -> bool:
        return isinstance(error, RecoverableError)
    
    def determines_if_error_is_recoverable(self, error: Exception) -> bool:
        return self.is_recoverable(error)
    
    def raise_if_max_attempts_exceeded(self):
        if self.current_attempts >= self.max_attempts:
            raise NonRecoverableError(
                f'Max recovery attempts ({self.max_attempts}) exceeded'
            )
