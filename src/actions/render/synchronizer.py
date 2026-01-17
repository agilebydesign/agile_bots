from typing import Optional

class Synchronizer:

    def __init__(self, synchronizer_class_path: str):
        self._synchronizer_class_path = synchronizer_class_path

    @property
    def synchronizer_class_path(self) -> str:
        return self._synchronizer_class_path