from pathlib import Path
from typing import Dict, Any
from .clarify.required_context import RequiredContext
from .strategy.strategy import Strategy

class Guardrails:

    def __init__(self, behavior_config):
        self._behavior_config = behavior_config
        behavior_folder = behavior_config.behavior_directory
        self.required_context = RequiredContext(behavior_folder)
        self.strategy = Strategy(behavior_folder)

    @property
    def instructions(self) -> Dict[str, Any]:
        return {'guardrails': {'required_context': self.required_context.instructions, 'strategy': self.strategy.instructions}}