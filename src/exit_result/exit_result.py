class ExitResult:
    def __init__(self, should_exit: bool, message: str = ''):
        self._should_exit = should_exit
        self._message = message
    
    @property
    def should_exit(self) -> bool:
        return self._should_exit
    
    @property
    def message(self) -> str:
        return self._message
