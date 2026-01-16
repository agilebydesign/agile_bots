class NavigationResult:
    def __init__(self, success: bool, message: str = '', new_position: str = ''):
        self._success = success
        self._message = message
        self._new_position = new_position
    
    @property
    def success(self) -> bool:
        return self._success
    
    @property
    def message(self) -> str:
        return self._message
    
    @property
    def new_position(self) -> str:
        return self._new_position
